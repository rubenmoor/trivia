"""The LLM batch's steps: media, sheets, review, fix, research, record (D-36). Never ships (D-35)."""
import concurrent.futures, contextlib, datetime, difflib, json, re

from layout import SOURCE_POOL as POOL, WORK
import atomic  # authoring/tools/atomic.py: .tmp + replace writes, cross-process locks
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import categories  # authoring/tools/categories.py: every bundle's categories (D-19, D-43)
import media_cache as media  # authoring/tools/media_cache.py: the media cache (D-17)
import media as media_tool  # authoring/tools/media.py: candidates, sheets, picks (`media` is the cache)
import providers  # authoring/tools/providers/: where candidates come from (D-45)
import translations  # authoring/tools/translations.py: translated questions (D-81)

from qgen import PROBLEMS, FACT_FIELDS, FACT_SCHEMA, QUESTION_FIELDS, REVISE_SCHEMA, STR, UsageLimit, as_locale, check_question_shape, claude, collect, failed, for_review, load_age_groups, load_json, locale_chunks, named, norm, overlap_norm, parallel, prompt, revise_in_pool, run_dir, save_json  # authoring/tools/qgen.py


# --- the LLM batch's steps: media, sheets, review, fix, research, record (D-36) 

BATCH_SLOTS = 18  # draft slots per subcategory (D-46); base: 57 × 18 slots, about 700 merged questions
REVIEW_MODEL = "opus"

REVIEW_SCHEMA = {"type": "object", "required": ["decision", "feedback", "fix", "pick", "background_pick", "new_query", "reasons", "problems"],
    "properties": {"decision": {"type": "string", "enum": ["approved", "needs_work"]}, "feedback": STR, "fix": STR,
                   "pick": {"type": ["integer", "null"]}, "background_pick": {"type": ["integer", "null"]},
                   "new_query": {"type": ["string", "null"]}, "reasons": STR,
                   "problems": {"type": "array", "items": {"type": "string", "enum": PROBLEMS}}}}

# Keywords in `review.feedback` → problem, for reviews without `problems` (plan 15). Reports only.
_GUESS = [("media", r"imagen (de fondo )?adecuada|ninguna (imagen|candidat|foto)|hoja de contacto|\bsheet\b"),
          ("fact", r"verificaci[oó]n de datos|es fals[oa]|no es (cierto|exact)|incorrect|err[oó]ne|equivocad|est[aá] mal|no se pudo confirmar"),
          ("overlap", r"(?<![/\w])q-\d{4}(?!\.jpg)|duplica|se cruza|misma respuesta|\bduplicate\b"),
          ("giveaway", r"(pistas?|descripci[oó]n|imagen|texto|pregunta|respuesta)\b.{0,120}\b(regala|delata|revela|resuelve|descarta|dan? la respuesta|dice la respuesta|apunta|deja solo|se delata)"),
          ("ambiguity", r"defend|ambig|tambi[eé]n (es|ser[ií]a|podr[ií]a ser) (correct|v[aá]lid)|m[aá]s de una respuesta"),
          ("style", r"en com[uú]n|relleno|larg[oa]|historia|imagina|retirad"),
          ("difficulty", r"dif[ií]cil|f[aá]cil|dificultad")]


def guess_problems(feedback):
    """Problems guessed from free-text feedback; ["other"] if no keyword matches."""
    text = (feedback or "").lower()
    return [p for p, rx in _GUESS if re.search(rx, text)] or ["other"]


def batch_questions(run, statuses=("draft",)):
    """The pool's questions of this run that are still waiting for the given steps.
    A `qgen rework` run's questions are the ids in its run.json (QG-23); a translation run's are its
    entries in the locale file, as played (locale_questions)."""
    if locale := run_locale(WORK / run):
        return [q for q in locale_questions(locale) if q["batch"] == run and q["status"] in statuses]
    ids = set((load_json(WORK / run / "run.json", {}) or {}).get("ids") or [])
    return [q for q in load_json(POOL)["questions"]
            if (q["id"] in ids if ids else q.get("batch") == run) and q["status"] in statuses]


def run_mode(run):
    return (load_json(WORK / run / "run.json", {}) or {}).get("mode")


def update_pool(changes):
    """Apply {qid: change(q)} to the source pool in one write."""
    with atomic.locked(POOL):
        data = load_json(POOL)
        for q in data["questions"]:
            if q["id"] in changes:
                changes[q["id"]](q)
        save_json(POOL, data)


def slots_of(q):
    return ["media"] + (["background"] if q.get("background") else [])


def kept_slots(run, q):
    """A scan run's (SCANS) slots that keep the pool's pick: still picked (revise_in_pool unpicks a slot only
    when its type or query changed) and usable. No search, research, sheet or new pick for them (tasks 1194, 1244)."""
    if run_mode(run) not in SCANS:
        return set()
    return {s for s in slots_of(q) if q[s].get("file_url") and providers.licence_verdict(q[s])[0] == "ok"}


def sheet_path(d, qid, slot):
    return d / "sheets" / (f"{qid}.jpg" if slot == "media" else f"{qid}-background.jpg")


def cmd_media(args):
    """Fetch media candidates for every slot of the run's merged questions, except a scan run's kept slots."""
    errors = []
    slots = [(q, slot) for q in batch_questions(args.run) for slot in slots_of(q) if slot not in kept_slots(args.run, q)]
    todo = [(q, slot) for q, slot in slots if media_tool.load_candidates(q["id"], slot) is None]
    progress.resumed("media", len(slots) - len(todo), len(todo), "slots")
    with progress.Bar("media", len(todo), "searches") as bar:
        for q, slot in todo:
            try:
                with progress.item("media", f"{q['id']} {slot}"):
                    data = media_tool.fetch_for(q, slot)
                progress.detail(f"  media: {q['id']} {slot}: {len(data['candidates'])} candidate(s)")
                bar.finished()
            except Exception as e:  # noqa: BLE001 — rerun retries the rest
                errors.append(e)
                progress.fail(f"  FAILED media {q['id']} {slot}: {e}")
                bar.finished(ok=False)
    return errors


def cmd_sheets(args):
    """One contact sheet per slot (ImageMagick), for the review step to look at; none for a scan run's kept slots."""
    d = run_dir(args)
    errors = []
    slots = [(q, slot) for q in batch_questions(args.run) for slot in slots_of(q) if slot not in kept_slots(args.run, q)]
    done = sum(sheet_path(d, q["id"], slot).exists() for q, slot in slots)
    todo = [(sheet_path(d, q["id"], slot), found) for q, slot in slots
            if not sheet_path(d, q["id"], slot).exists() and (found := media_tool.load_candidates(q["id"], slot))]
    progress.resumed("sheets", done, len(todo), "sheets")
    with progress.Bar("sheets", len(todo), "sheets") as bar:
        for out, found in todo:
            try:
                thumbs = d / "sheets" / "thumbs" / out.stem
                with progress.item("sheets", out.stem):
                    shown = media_tool.make_sheet(found["candidates"], out, thumbs)
                progress.detail(f"  sheets: {out.name}: {len(shown)} picture(s)")
                bar.finished()
            except Exception as e:  # noqa: BLE001
                errors.append(e)
                progress.fail(f"  FAILED sheet {out.name}: {e}")
                bar.finished(ok=False)
    return errors


RELATED_RATIO = 0.7  # answers this similar count as the same
RELATED_MAX = 30


def related_questions(q, pool, pool_en=None):
    """Pool questions the review must compare with: same or similar answer first, then same subcategory.
    An en question's answer against the pool's English keys (as_locale; pool_en: that view, precomputed)."""
    en = translations.source_locale(q) == "en"
    keys = (pool_en if pool_en is not None else as_locale(pool, "en")) if en else pool
    a = overlap_norm(q["answer"], "en") if en else norm(q["answer"])
    ranked = []
    for i, (p, k) in enumerate(zip(pool, keys)):
        if p["id"] == q["id"] or p["status"] == "rejected":
            continue
        b = overlap_norm(k["answer"], "en") if en else norm(p["answer"])
        ratio = 1.0 if a == b else difflib.SequenceMatcher(None, a, b).ratio()
        if ratio >= RELATED_RATIO:
            ranked.append((0, -ratio, i, p))
        elif categories.key(p) == categories.key(q):
            ranked.append((1, 0, i, p))
    ranked.sort(key=lambda r: r[:3])
    loc = translations.source_locale(q)
    return [{k: named(p, loc)[k] for k in ["id", "status", "subcategory", "question", "answer"]}
            for *_, p in ranked[:RELATED_MAX]]


def slot_input(d, q, slot, kept=False):
    """The review's view of a slot: its candidates and sheet, or for a kept slot (kept_slots) the kept pick."""
    spec = q["media"] if slot == "media" else q["background"]
    if kept:
        return {"type": spec.get("type", "image"), "role": spec.get("role", "decorative"), "query": spec["query"],
                "note": spec.get("note"), "kept": True, "title": media_title(q, slot)}
    found = media_tool.load_candidates(q["id"], slot) or {"candidates": []}
    sheet = sheet_path(d, q["id"], slot)
    return {"type": spec.get("type", "image"), "role": spec.get("role", "decorative"), "query": spec["query"],
            "note": spec.get("note"), "sheet": sheet.relative_to(d).as_posix() if sheet.exists() else None,
            "candidates": [{"number": i, "type": c["type"], "source": providers.name(c), "title": c["title"],
                            "width": c["width"], "height": c["height"], "duration": c["duration"],
                            "author": c["author"], "license": c["license"]}
                           for i, c in enumerate(found["candidates"], 1)]}


def cmd_review(args):
    """The LLM review (D-32 criteria, prompts/review.md): one call per question.
    Round 1 reviews every merged question; round 2 only those whose media was searched again.
    A translation run (plan 66): the translation with its source and the source's picked media,
    no new search; round 1 also decides its not-travelling ids in one line."""
    d = run_dir(args)
    reviews = d / "reviews"
    tmp_of = tmp_ids(d)
    ratings, checks = collect(d)
    locale = run_locale(d)
    pool = in_locale(locale) if locale else load_json(POOL)["questions"]
    pool_en = None if locale else as_locale(pool, "en")
    names = ["house-style", "review", *(["translate-review"] if locale else [])]
    notes = translator_notes(d) if locale else {}
    mode = run_mode(args.run)
    rework = mode in ("rework", *SCANS)
    todo, done = [], 0
    for q in batch_questions(args.run):
        r = load_json(reviews / f"{q['id']}.json", {})
        done += f"round{args.round}" in r
        if args.round == 1 and "round1" not in r:
            todo.append((q, r))
        if args.round == 2 and (r.get("researched") or fixed(r) and not rework) and "round2" not in r:
            todo.append((q, r))
    if locale and args.round == 1:
        src = {q["id"]: q for q in load_json(POOL)["questions"]}
        todo += [({**x, "not_travelling": True, "source": src[x["id"]],
                   "source_locale": translations.source_locale(src[x["id"]])}, r)
                 for x in load_json(d / "not-travelling.json", [])
                 if "round1" not in (r := load_json(reviews / f"{x['id']}.json", {}))]
    progress.resumed(f"review {args.round}", done, len(todo), "questions")

    def translation_payload(q, r, tmp):
        if q.get("not_travelling"):
            return {"not_travelling": {k: q[k] for k in ["id", "reason", "notes"]},
                    "source": {k: named(q["source"], locale)[k] for k in ["subcategory", "difficulty", *translations.TEXT_FIELDS]}}
        check = fact_check(r, checks.get(tmp))
        return {
            "question": {k: named(q, locale)[k] for k in ["id", "bundle", "subcategory", "difficulty", *translations.TEXT_FIELDS]},
            "source": q["source"],
            "notes": notes.get(q["id"], ""),
            "rater_notes": (ratings.get(tmp) or {}).get("notes"),
            "fact_check": {k: check[k] for k in ["verdict", "problem", "correction"]} if check else "not needed",
            "related": related_questions(q, pool),
            "media": {**{k: q["media"].get(k) for k in ["type", "role", "query", "note"]}, "title": media_title(q)},
            "background": {"title": media_title(q, "background")} if q.get("background") else None,
            "can_search_again": False,
            "can_fix": args.round == 1,
            "only_shortened": False,
            "existing": True,
        }

    def work(item):
        q, r = item
        tmp = tmp_of.get(q["id"])
        kept = set() if locale else kept_slots(args.run, q)
        payload = translation_payload(q, r, tmp) if locale else {
            "question": {k: named(q, translations.source_locale(q))[k] for k in ["id", "bundle", "subcategory", *QUESTION_FIELDS]}
                        | {"locale": translations.source_locale(q)},
            "rater_notes": (ratings.get(tmp) or {}).get("notes") or (q.get("quality") or {}).get("notes"),
            "fact_check": ({k: check[k] for k in ["verdict", "problem", "correction"]}
                           if (check := fact_check(r, checks.get(tmp))) else "not needed (no number, date or record)"),
            "related": related_questions(q, pool, pool_en),
            "media": slot_input(d, q, "media", "media" in kept),
            "background": slot_input(d, q, "background", "background" in kept) if q.get("background") else None,
            "can_search_again": args.round == 1 and "media" not in kept,
            "can_fix": args.round == 1 and not rework,
            "only_shortened": mode in SCANS,  # already in the game, only reworded
            "existing": rework,
        }
        user = "## Question to review\n" + json.dumps(payload, ensure_ascii=False)
        system = prompt(*names, locale=locale or translations.source_locale(q), bundle=run_bundle(d),
                        source_locale=q.get("source_locale"))
        out, model = claude(system, user, REVIEW_SCHEMA, args.model, d, read=True, with_model=True)
        r[f"round{args.round}"] = {**out, "model": model}
        save_json(reviews / f"{q['id']}.json", r)
        progress.detail(f"  review {args.round}: {q['id']}: {out['decision']}, pick {out['pick']}"
                        + (f", new search “{out['new_query']}”" if out["new_query"] and args.round == 1 else ""))

    return parallel(work, todo, args.jobs, f"review {args.round}", "questions")


def fixed(r):
    return (r.get("fix") or {}).get("action") == "revise"


def fact_check(r, check):
    """The fact check that holds for the question now: the fix's own when it changed facts (QG-22)."""
    fix = r.get("fix") or {}
    return fix["factcheck"] if "factcheck" in fix else check


def cmd_fix(args):
    """One revision for every question that round 1 sent back with a fixable problem (QG-22): the
    reviewer's `fix` goes to the revise prompt. Changed facts are checked again; round 2 reviews it.
    Unfixable ones (no `fix`, or the reviser keeps or drops) stay needs_work for the developer.
    In a `qgen rework` run (QG-23) the issue is the needs_work feedback; kept and revised questions
    go back to draft, are all fact-checked and reviewed again, with a new media search if needed.
    A translation run (plan 66): the reviser sees the source; only the translated text and
    difficulty are taken (media stays the source's), `fix.previous` keeps the old text."""
    d = run_dir(args)
    mode = run_mode(args.run)
    rework = mode == "rework"
    locale = run_locale(d)
    scanned = load_json(d / "run.json", {}).get("issues") if mode in SCANS else None
    tmp_of = tmp_ids(d)
    _, checks = collect(d)
    lo, hi = load_age_groups()["scale"]
    today = datetime.date.today().isoformat()
    revise, recheck, done = [], [], 0
    for q in batch_questions(args.run, ("draft", "needs_work", "approved")):
        path = d / "reviews" / f"{q['id']}.json"
        r = load_json(path, {})
        fix = r.get("fix")
        done += bool(fix) and ("factcheck" in fix or not needs_recheck(fix, rework))
        if fix is None and (issue := f"{SCANS[mode]['issue']}: {scanned[q['id']]}" if scanned else fix_issue(q, r, rework)):
            revise.append((q, path, r, issue))
        elif fix and "factcheck" not in fix and needs_recheck(fix, rework):
            recheck.append((q, path, r))
    progress.resumed("fix", done, len(revise) + len(recheck), "questions")

    def issues_of(issue, c):
        return [issue] + ([f"fact-check {c['verdict']}: {c['problem']} correction: {c['correction']}"]
                          if c and c["verdict"] != "confirmed" else [])

    def ask(group, items):
        """(q, path, r, rev, fix) per answered question; a malformed revision becomes action `malformed`."""
        system = prompt("house-style", "revise", locale=translations.source_locale(group[0][0]), bundle=run_bundle(d),
                        source_locale=group[0][0].get("source_locale"))
        out = claude(system, "## Questions with issues\n" + json.dumps(items, ensure_ascii=False), REVISE_SCHEMA,
                     args.model, d)
        got = {x["id"]: x for x in out["results"]}
        answered = []
        for q, path, r, _ in group:
            if (rev := got.get(q["id"])) is None:
                continue
            fix = {"action": rev["action"], "reason": rev["reason"]}
            if rev["action"] == "revise" and (bad := check_question_shape(rev["question"])):
                fix["action"], fix["reason"] = "malformed", "; ".join(bad)
            answered.append((q, path, r, rev, fix))
        return answered, [q["id"] for q, *_ in group if q["id"] not in got]

    def done(q, path, r, fix, rework):
        r["fix"] = fix
        save_json(path, r)
        if needs_recheck(fix, rework):
            recheck.append((q, path, r))
        progress.detail(f"  fix: {q['id']}: {fix['action']}" + (f" {', '.join(fix['changed'])}" if fixed(r) else ""))

    def work(group):
        answered, missing = ask(group, [
            {**for_review({**q, "tmp_id": q["id"]}), "issues": issues_of(issue, checks.get(tmp_of.get(q["id"]))),
             "background_query": (q.get("background") or {}).get("query", ""),
             "needs_media": q.get("needs_media", False)} for q, _, _, issue in group])
        changes, changed = {}, {}
        for q, _, _, rev, fix in answered:
            if fix["action"] == "revise" or (rework and fix["action"] == "keep"):
                def change(x, rev=rev, fix=fix):
                    if fix["action"] == "revise":
                        changed[x["id"]] = revise_in_pool(x, rev["question"], rev["reason"], today)
                    if rework or scanned:
                        if x.get("review"):
                            x["previous"] = x["review"]  # record chains it (task 1241)
                        x["status"], x["review"] = "draft", None
                changes[q["id"]] = change
        if changes:
            update_pool(changes)
        for q, path, r, _, fix in answered:
            if fix["action"] == "revise":
                fix["changed"] = sorted(changed.get(q["id"], []))
                for slot in ("media", "background"):
                    if slot in fix["changed"]:
                        sheet_path(d, q["id"], slot).unlink(missing_ok=True)
            done(q, path, r, fix, rework)
        if missing:
            raise RuntimeError(f"no fix result for {', '.join(missing)}")

    def work_translation(group):
        answered, missing = ask(group, [
            {**for_review({**q, "tmp_id": q["id"]}), "source": q["source"],
             "issues": issues_of(f"translation into {LANGUAGES[locale]} of the {LANGUAGES[q['source_locale']]} `source`, "
                                 f"which stays as it is; {issue}",
                                 checks.get(q["id"])),
             "background_query": "", "needs_media": False} for q, _, _, issue in group])
        changes = {}
        for q, path, r, rev, fix in answered:
            if fix["action"] == "revise":
                new = {**{k: rev["question"][k] for k in translations.TEXT_FIELDS},
                       "difficulty": min(hi, max(lo, rev["question"]["difficulty"]))}
                fix["changed"] = sorted(k for k in new if new[k] != q[k])
                fix["previous"] = {k: q[k] for k in fix["changed"]}
                changes[q["id"]] = lambda t, new=new: t.update(new)
            done(q, path, r, fix, False)
        update_translations(locale, changes)
        if missing:
            raise RuntimeError(f"no fix result for {', '.join(missing)}")

    def check(group):
        ids = {q["id"] for q, _, _ in group}
        qs = [x for x in (batch_questions(args.run, ("draft",)) if locale else load_json(POOL)["questions"])
              if x["id"] in ids]
        loc = translations.source_locale(group[0][0])
        user = f"## Questions ({LANGUAGES[loc]})\n" + json.dumps([for_review({**q, "tmp_id": q["id"]}) for q in qs], ensure_ascii=False)
        out = claude(prompt("factcheck", locale=loc, source_locale=group[0][0].get("source_locale")), user, FACT_SCHEMA,
                     args.check_model, d, web=True)
        got = {c["id"]: c for c in out["checks"]}
        for q, path, r in group:
            if q["id"] in got:
                r["fix"]["factcheck"] = got[q["id"]]
                save_json(path, r)
                progress.detail(f"  fix factcheck: {q['id']}: {got[q['id']]['verdict']}")
        if ids - got.keys():
            raise RuntimeError(f"no fact check for {', '.join(sorted(ids - got.keys()))}")

    errors = parallel(work_translation if locale else work, locale_chunks(revise), args.jobs, "fix", "calls")
    if any(isinstance(e, UsageLimit) for e in errors):
        return errors
    return errors + parallel(check, locale_chunks(recheck), args.jobs, "fix factcheck", "calls")


def fix_issue(q, r, rework):
    """What the reviser has to fix, or None."""
    if rework:
        review = q.get("review") or {}
        if q["status"] != "needs_work" or not (review.get("feedback") or "").strip():
            return None
        who = "final reviewer" if review.get("reviewer") == "llm" else "developer feedback"
        return f"{who}: {review['feedback'].strip()}"
    r1 = r.get("round1") or {}
    if r1.get("decision") == "needs_work" and r1.get("fix", "").strip():
        return f"final reviewer: {r1['fix'].strip()}"
    return None


def needs_recheck(fix, rework):
    if rework:
        return fix["action"] in ("revise", "keep")
    return fix["action"] == "revise" and bool(set(FACT_FIELDS) & set(fix["changed"]))


def cmd_research(args):
    """One new media search for questions whose round-1 review found no adequate media."""
    d = run_dir(args)
    errors, todo, done = [], [], 0
    for q in batch_questions(args.run):
        path = d / "reviews" / f"{q['id']}.json"
        r = load_json(path, {})
        r1 = r.get("round1") or {}
        done += bool(r.get("researched"))
        if (r1.get("pick") is None and r1.get("new_query") and not r.get("researched")
                and "media" not in (r.get("fix") or {}).get("changed", []) and "media" not in kept_slots(args.run, q)):
            todo.append((q, path, r))
    progress.resumed("research", done, len(todo), "searches")
    with progress.Bar("research", len(todo), "searches") as bar:
        for q, path, r in todo:
            query = r["round1"]["new_query"].strip()
            try:
                q["media"]["query"] = query
                with progress.item("research", q["id"]):
                    media_tool.fetch_for(q, "media")
            except Exception as e:  # noqa: BLE001
                errors.append(e)
                progress.fail(f"  FAILED research {q['id']}: {e}")
                bar.finished(ok=False)
                continue
            update_pool({q["id"]: lambda x, s=query: x["media"].update(query=s)})
            sheet_path(d, q["id"], "media").unlink(missing_ok=True)  # `sheets` builds the new one
            r["researched"] = query
            save_json(path, r)
            progress.detail(f"  research: {q['id']}: “{query}”")
            bar.finished()
    return errors


def final_review(r):
    return r.get("round2") or r.get("round1")


RECORD_TEXT = {  # record's own feedback: Spanish for es-sourced questions, else English (plan 148)
    "es": {"no media": "No se encontró una imagen adecuada para esta pregunta.",
           "no background": "No se encontró una imagen de fondo adecuada.",
           "media pick": "La imagen elegida", "background pick": "La imagen de fondo elegida",
           "broken": " está dañada en la fuente ({}).", "licence": " tiene una licencia no adecuada ({}).",
           "fact": "Verificación de datos"},
    "en": {"no media": "No suitable picture found for this question.", "no background": "No suitable background picture found.",
           "media pick": "The picked picture", "background pick": "The picked background picture",
           "broken": " is broken at the source ({}).", "licence": " has an unsuitable licence ({}).", "fact": "Fact check"},
}


def cmd_record(args):
    """Write the reviews (D-33: reviewer llm + model) and the picks into the pool. Fixed rules on
    top of the model's decision: no adequate media, a pick whose licence verdict is replace or whose file is broken
    (each pick is downloaded to check it, task 1181), or a fact check that isn't confirmed, means needs_work.
    A scan run's kept slots (kept_slots) stay as they are: no pick, no download."""
    d = run_dir(args)
    if run_locale(d):
        return record_translations(args, d)
    tmp_of = tmp_ids(d)
    _, checks = collect(d)
    today = datetime.date.today().isoformat()
    changes, missing, reviewed, picks = {}, [], [], {}
    snapshot = load_json(d / "recorded.json", {})
    for q in batch_questions(args.run):
        full = load_json(d / "reviews" / f"{q['id']}.json", {})
        r = final_review(full)
        if r is None:
            missing.append(q["id"])
            continue
        reviewed.append((q, full, r))
        kept = kept_slots(args.run, q)
        for slot, key in [("media", "pick"), ("background", "background_pick")]:
            if slot not in slots_of(q) or slot in kept:
                continue
            found = (media_tool.load_candidates(q["id"], slot) or {"candidates": []})["candidates"]
            n = r[key]
            picks[q["id"], slot] = media_tool.pick_fields(found[n - 1], slot) if n is not None and 1 <= n <= len(found) else None
    check_picks(picks, args.jobs)
    for q, full, r in reviewed:
        decision, problems, fields = r["decision"], [r["feedback"].strip()] if r["feedback"].strip() else [], {}
        kinds = set(r.get("problems") or [])
        say = RECORD_TEXT["es" if translations.source_locale(q).startswith("es") else "en"]
        for slot in media_tool.SLOTS:
            if (q["id"], slot) not in picks:
                continue
            if picks[q["id"], slot] is None:
                decision = "needs_work"
                kinds.add("media")
                problems.append(say[f"no {slot}"])
                continue
            fields[slot] = picks[q["id"], slot]
            verdict, reasons = providers.licence_verdict(fields[slot])
            if verdict == "replace":  # plan 53
                decision = "needs_work"
                kinds.add("media")
                broken = fields[slot].get("file_problem")
                problems.append(say[f"{slot} pick"] + (say["broken"].format(broken) if broken  # task 1181
                                                       else say["licence"].format("; ".join(reasons))))
        check = fact_check(full, checks.get(tmp_of.get(q["id"])))
        if check and check["verdict"] != "confirmed":
            decision = "needs_work"
            kinds.add("fact")
            problems.append(f"{say['fact']}: {check['verdict']}. {check['problem']}".strip())
        if decision == "needs_work" and not problems:
            problems.append(r["reasons"])
        review = {"decision": decision, "feedback": " ".join(problems) if decision == "needs_work" else None,
                  "problems": [p for p in PROBLEMS if p in kinds] if decision == "needs_work" else [],
                  "reviewed_on": today, "reviewer": "llm", "model": r["model"]}

        def change(x, review=review, fields=fields, check=check if "factcheck" in (full.get("fix") or {}) else None):
            for slot, f in fields.items():
                media_tool.apply_pick(x[slot], f)
            if check:
                x["fact_checked"] = check["verdict"] == "confirmed"
            x.update(review={**review, "previous": review_before(x, snapshot)}, status=review["decision"])
        changes[q["id"]] = change
        snapshot[q["id"]] = {"decision": review["decision"], "problems": review["problems"]}
        progress.detail(f"  record: {q['id']}: {decision}")
    update_pool(changes)
    save_json(d / "recorded.json", snapshot)  # record's decisions, for batch health (plan 15)
    return failed(f"{len(missing)} question(s) without a review: {', '.join(missing)}") if missing else []


def check_picks(picks, jobs):
    """Download and check record's picks in place ({(qid, slot): fields or None}), `jobs` at a time, a log line
    per download (tasks 1242, 1243). A failed download leaves the pick unchecked: the sync step checks it again."""
    todo = {k for k, f in picks.items() if f and not media.cache_path(f["file_url"]).is_file()}
    if todo:
        progress.say(f"  record: {len(todo)} pick(s) to download")

    def check(key):
        qid, slot = key
        f = picks[key]
        try:
            with media_tool.downloading("record", qid, slot, f["file_url"]) if key in todo else contextlib.nullcontext():
                picks[key] = media_tool.checked(f)
            ok = True
        except Exception as e:  # noqa: BLE001 — see the docstring
            progress.say(f"  not checked: {qid} {slot}: {e}", err=True)
            ok = False
        if key in todo:
            bar.finished(ok)

    with progress.Bar("record", len(todo), "downloads") as bar, \
            concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        list(ex.map(check, [k for k, f in picks.items() if f]))


def review_before(x, recorded):
    """The review x had before this run, for record's `previous`: kept by fix or merge as top-level `previous`;
    on a second record of the run the one it chained already."""
    if "previous" in x:
        return x.pop("previous")
    return (x.get("review") or {}).get("previous") if x["id"] in recorded else None


def record_translations(args, d):
    """cmd_record for a translation run (plan 66): reviews into the locale file; no media rules, a fact
    check that isn't confirmed means needs_work. A confirmed not-travelling id → `translatable: false`
    on the source (an older translation of it is rejected); else it is translated again next run."""
    locale = run_locale(d)
    _, checks = collect(d)
    today = datetime.date.today().isoformat()
    changes, missing = {}, []
    snapshot = load_json(d / "recorded.json", {})

    def review_of(decision, feedback, kinds, model):
        return {"decision": decision, "feedback": feedback if decision != "approved" else None,
                "problems": [p for p in PROBLEMS if p in kinds] if decision != "approved" else [],
                "reviewed_on": today, "reviewer": "llm", "model": model}

    def record(t, review, status):
        t.update(review={**review, "previous": review_before(t, snapshot)}, status=status)

    for q in batch_questions(args.run):
        full = load_json(d / "reviews" / f"{q['id']}.json", {})
        r = final_review(full)
        if r is None:
            missing.append(q["id"])
            continue
        decision, kinds = r["decision"], set(r.get("problems") or [])
        problems = [r["feedback"].strip()] if r["feedback"].strip() else []
        check = fact_check(full, checks.get(q["id"]))
        if check and check["verdict"] != "confirmed":
            decision = "needs_work"
            kinds.add("fact")
            problems.append(f"Fact check: {check['verdict']}. {check['problem']}".strip())
        if decision == "needs_work" and not problems:
            problems.append(r["reasons"])
        review = review_of(decision, " ".join(problems), kinds, r["model"])
        changes[q["id"]] = lambda t, review=review: record(t, review, review["decision"])
        snapshot[q["id"]] = {"decision": decision, "problems": review["problems"]}
        progress.detail(f"  record: {q['id']}: {decision}")
    away, confirmed = load_json(d / "not-travelling.json", []), {}
    for x in away:
        r = load_json(d / "reviews" / f"{x['id']}.json", {}).get("round1")
        if r is None:
            missing.append(x["id"])
            continue
        x["decision"], x["feedback"] = r["decision"], r["feedback"].strip() or None
        if r["decision"] == "approved":
            confirmed[x["id"]] = review_of("rejected", f"Doesn't travel ({x['reason']}): {r['reasons']}", {"other"}, r["model"])
        progress.detail(f"  record: {x['id']}: not travelling, " + ("confirmed" if x["id"] in confirmed else "translate again"))
    for i, review in confirmed.items():
        changes.setdefault(i, lambda t, review=review: record(t, review, "rejected"))
    update_translations(locale, changes)
    if confirmed:
        update_pool({i: lambda q: q.update(translatable=False) for i in confirmed})
        translations.reject_for_sources(set(confirmed), skip=(locale,))
    save_json(d / "not-travelling.json", away)
    save_json(d / "recorded.json", snapshot)
    return failed(f"{len(missing)} question(s) without a review: {', '.join(missing)}") if missing else []


# the other command groups, after everything here is defined (they import each other)
from rework import SCANS  # authoring/tools/rework.py
from translate import LANGUAGES, in_locale, locale_questions, media_title, run_bundle, run_locale, tmp_ids, translator_notes, update_translations  # authoring/tools/translate.py
