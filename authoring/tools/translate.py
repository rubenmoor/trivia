"""Translation runs: `qgen translate` and `qgen batch --translate` (plan 66, decision 45). Never ships (D-35)."""
import argparse, datetime, json, re, sys, time, urllib.parse
from collections import Counter

import layout  # paths (D-35)
from layout import REPO as ROOT, SOURCE_POOL as POOL, WORK
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import categories  # authoring/tools/categories.py: every bundle's categories (D-19, D-43)
import media as media_tool  # authoring/tools/media.py: candidates, sheets, picks (`media` is the cache)
import targets  # authoring/tools/targets.py: pool targets (D-53)
import translations  # authoring/tools/translations.py: translated questions (D-81)

from qgen import REVIEW_URL, TRANSLATE_SCHEMA, check_bundle, check_question_shape, claude, cmd_export, cmd_factcheck, cmd_merge, cmd_rate, collect, concept_file, costs, load_age_groups, load_json, lock_run, named, natural_key, parallel, prompt, run_dir, run_steps, save_json, split_list, work_runs, write_report  # authoring/tools/qgen.py


# --- translation runs (plan 66, D-81) -----------------------------------------

LANGUAGES = translations.LANGUAGES
TRANSLATE_CHUNK = 15  # questions per translate call, one subcategory each


def run_locale(d):
    """The run's locale (a `--translate` run), or None."""
    return (load_json(d / "run.json", {}) or {}).get("locale")


def text_locale(d):
    """The language of a run's drafts: a translation run's locale, else run.json's draft_locale (plan 148;
    older runs es). Merged questions carry their own (translations.source_locale)."""
    cfg = load_json(d / "run.json", {}) or {}
    return cfg.get("locale") or cfg.get("draft_locale") or "es"


def run_bundle(d):
    """The bundle a `--translate` run translates (base for other runs)."""
    return (load_json(d / "run.json", {}) or {}).get("bundle") or "base"


def numbers(text):
    """The numbers in text, thousands separators and decimal marks dropped: «42 195» = «42,195»."""
    return sorted(re.findall(r"\d+", re.sub(r"(?<=\d)[ ,.  '](?=\d)", "", text)))


def fact_text(q):
    return " ".join([q["question"], q["answer"], *q["wrong_answers"], *q["hints"], q["fun_fact"]])


def translation_needs_check(t, q):
    """A translation changed a number, unit or date (imperial added included), the translator doubts a
    fact, or the source wasn't fact-checked; the rest inherits the source's check."""
    return bool(numbers(fact_text(t)) != numbers(fact_text(q)) or not q.get("fact_checked")
            or re.search(r"\bfacts?\b|doubt", t["notes"], re.I))


def translated_drafts(d):
    src, locale = {q["id"]: q for q in load_json(POOL)["questions"]}, run_locale(d)
    for f in sorted((d / "translations").glob("*.json")):
        out = []
        for t in load_json(f)["items"]:
            if t["travels"] != "yes":
                continue
            q = src[t["id"]]
            out.append({"tmp_id": q["id"], "locale": locale, "source_locale": translations.source_locale(q),
                        "subcategory": q["subcategory"],
                        "bundle": q.get("bundle") or "base", "axes": q.get("axes"), "style": q.get("style"),
                        "difficulty": q["difficulty"], **{k: t[k] for k in translations.TEXT_FIELDS},
                        "media": {k: q["media"].get(k) for k in ("type", "role", "query", "note")},
                        "needs_fact_check": translation_needs_check(t, q), "translator_notes": t["notes"]})
        yield f.stem, out


def media_title(q, slot="media"):
    """The picked file's title from its candidates; without the cache (a pm work tree) its file name."""
    found = media_tool.load_candidates(q["id"], slot) or {"candidates": []}
    url = q[slot].get("source_url")
    if title := next((c["title"] for c in found["candidates"] if url and c.get("page_url") == url), None):
        return title
    picked = url or q[slot].get("file_url")
    return urllib.parse.unquote(picked.split("?")[0].rsplit("/", 1)[-1]) if q[slot].get("file_url") and picked else None


def translate_chunks(ids, src):
    """[(name, questions)]: the run's sources per subcategory and source locale (a non-es one in the name),
    at most TRANSLATE_CHUNK per chunk."""
    by_sub = {}
    for i in ids:
        by_sub.setdefault((*categories.key(src[i]), translations.source_locale(src[i])), []).append(src[i])
    return [(f"{concept_file(b, s)[:-5]}{'' if loc == 'es' else '-' + loc}-{n // TRANSLATE_CHUNK + 1}",
             qs[n:n + TRANSLATE_CHUNK])
            for (b, s, loc), qs in by_sub.items() for n in range(0, len(qs), TRANSLATE_CHUNK)]


def cmd_translate(args):
    """Translate the run's sources into its locale (prompts/translate.md): work/<run>/translations/<chunk>.json.
    A new run needs --locale and --ids (debugging; `qgen batch --translate` makes real runs)."""
    d = run_dir(args)
    cfg = load_json(d / "run.json", {}) or {}
    if not cfg:
        if not (args.locale and args.ids):
            sys.exit(f"{args.run} has no run.json: give --locale and --ids")
        if args.locale not in translations.LOCALES:
            sys.exit(f"--locale must be one of {', '.join(translations.LOCALES)}")
        cfg = {"mode": "translate", "locale": args.locale, "ids": split_list(args.ids),
               "started": datetime.date.today().isoformat()}
        save_json(d / "run.json", cfg)
    locale, src = cfg["locale"], {q["id"]: q for q in load_json(POOL)["questions"]}
    if unknown := [i for i in cfg["ids"] if i not in src]:
        sys.exit(f"no such source id: {', '.join(unknown)}")
    if own := [i for i in cfg["ids"] if translations.source_locale(src[i]) == locale]:
        sys.exit(f"already in {LANGUAGES[locale]}: {', '.join(own)}")
    all_chunks = translate_chunks(cfg["ids"], src)
    todo = [c for c in all_chunks if not (d / "translations" / f"{c[0]}.json").exists()]
    progress.resumed("translate", len(all_chunks) - len(todo), len(todo), "chunks")

    def work(item):
        name, qs = item
        sl = translations.source_locale(qs[0])
        items = [{"id": q["id"], "subcategory": named(q, sl)["subcategory"], "difficulty": q["difficulty"],
                  **{k: q[k] for k in translations.TEXT_FIELDS},
                  "media": {"type": q["media"]["type"], "role": q["media"]["role"], "query": q["media"].get("query"),
                            "title": media_title(q)}} for q in qs]
        system = prompt("house-style", "translate", locale=locale, bundle=run_bundle(d), source_locale=sl)
        out = claude(system, f"## Questions ({LANGUAGES[sl]})\n" + json.dumps(items, ensure_ascii=False),
                     TRANSLATE_SCHEMA, args.model, d)
        got = {t["id"]: t for t in out["items"]}
        if missing := [q["id"] for q in qs if q["id"] not in got]:
            raise RuntimeError(f"no translation for {', '.join(missing)}")
        bad = [f"{q['id']}: {'; '.join(p)}" for q in qs if got[q["id"]]["travels"] == "yes"
               and (p := check_question_shape({**got[q["id"]], "difficulty": q["difficulty"]}))]
        if bad:
            raise RuntimeError(f"malformed translation: {', '.join(bad)}")
        save_json(d / "translations" / f"{name}.json", {"items": [got[q["id"]] for q in qs]})
        progress.detail(f"  translate: {name}: " + ", ".join(f"{t['id']} {t['travels']}" for t in out["items"]))

    return parallel(work, todo, args.jobs, "translate", "calls")


def unmerged(d):
    """Ids of the run's travelling translations when none has an entry in the locale file (merge's output lost), else []."""
    have = {t["id"] for t in translations.load(run_locale(d))["questions"] if t.get("batch") == d.name}
    ids = sorted(q["tmp_id"] for _, qs in translated_drafts(d) for q in qs)
    return [] if have & set(ids) else ids


def merge_translations(d):
    """Rated and checked translations into questions.<locale>.json as drafts (difficulty from the rating);
    a stale entry's review is kept as `previous`. Not travelling → not-travelling.json, no entry."""
    cfg = load_json(d / "run.json")
    locale, run = cfg["locale"], d.name
    src = {q["id"]: q for q in load_json(POOL)["questions"]}
    ratings, checks = collect(d)
    lo, hi = load_age_groups()["scale"]
    with translations.locked(locale):
        doc = translations.load(locale)
        by_id = {t["id"]: t for t in doc["questions"]}
        merged = set(load_json(d / "merged.json", []))
        away = load_json(d / "not-travelling.json", [])
        added, waiting, malformed = [], [], []
        for f in sorted((d / "translations").glob("*.json")):
            for t in load_json(f)["items"]:
                i = t["id"]
                if i in merged and (t["travels"] == "no" or by_id.get(i, {}).get("batch") == run):
                    continue  # a merged id whose entry is gone (file not kept) is merged again
                if t["travels"] == "no":
                    away.append({"id": i, "reason": t["reason"], "notes": t["notes"],
                                 "question": src[i]["question"], "answer": src[i]["answer"]})
                    merged.add(i)
                    continue
                if i not in ratings or i not in checks:
                    waiting.append(i)
                    continue
                old = by_id.get(i)
                new = {"id": i, **{k: t[k] for k in translations.TEXT_FIELDS},
                       "difficulty": min(hi, max(lo, ratings[i]["difficulty_estimate"])), "status": "draft",
                       "batch": run, "review": None, "source_hash": translations.source_hash(src[i]),
                       **({"previous": old["review"]} if old and old.get("review") else {})}
                if problems := check_question_shape(new):
                    malformed.append(f"{i} ({'; '.join(problems)})")
                    continue
                by_id[i] = new
                added.append(i)
                merged.add(i)
        doc["questions"] = list(by_id.values())
        translations.save(locale, doc)
    save_json(d / "merged.json", sorted(merged))
    save_json(d / "not-travelling.json", away)
    rel = translations.path(locale).relative_to(ROOT)
    print(f"merged {len(added)} translation(s) into {rel}; {len(away)} not travelling (not-travelling.json)"
          + (f"; waiting for rate/factcheck: {', '.join(waiting)}" if waiting else "")
          + (f"; malformed, skipped: {', '.join(malformed)}" if malformed else ""))


def locale_questions(locale):
    """The locale's translations as played: the source's play fields under the translated text,
    difficulty, status, batch and review; `source` is the source's text, `source_locale` its language."""
    src = {q["id"]: q for q in load_json(POOL)["questions"]}
    return [{**{k: src[t["id"]].get(k) for k in ("id", "subcategory", "bundle", "axes", "style", "media", "background")},
             **{k: t[k] for k in translations.TEXT_FIELDS},
             **{k: t.get(k) for k in ("difficulty", "status", "batch", "review")}, "locale": locale,
             "source_locale": translations.source_locale(src[t["id"]]),
             "source": {k: src[t["id"]][k] for k in translations.TEXT_FIELDS}}
            for t in translations.load(locale)["questions"] if t["id"] in src]


def in_locale(locale):
    """Everything in the locale (decision 235): its translations (locale_questions) and its own sources."""
    return locale_questions(locale) + [q for q in load_json(POOL)["questions"] if translations.source_locale(q) == locale]


def update_translations(locale, changes):
    """Apply {id: change(t)} to the locale file in one write."""
    with translations.locked(locale):
        doc = translations.load(locale)
        for t in doc["questions"]:
            if t["id"] in changes:
                changes[t["id"]](t)
        translations.save(locale, doc)


def translator_notes(d):
    return {t["id"]: t["notes"] for f in sorted((d / "translations").glob("*.json")) for t in load_json(f)["items"]}


def tmp_ids(d):
    """Pool id → the run's draft tmp_id (ids.json); a translation run's drafts carry the source id."""
    if run_locale(d):
        return {i: i for i in load_json(d / "merged.json", [])}
    return {v: k for k, v in load_json(d / "ids.json", {}).items()}




# --- qgen batch --translate (plan 66, decision 45) ----------------------------

TRANSLATE_SIZE = 300  # sources per `qgen batch --translate` run (plan 66)
TRANSLATE_PILOT = 50  # the first run of a locale (QT-5)


def spread(qs, offset=0.0):
    """qs in an order that covers the difficulty scale early: van der Corput steps over qs sorted by
    difficulty, shifted by offset (0–1) so one-pick subcategories don't all start at the same level."""
    qs = sorted(qs, key=lambda q: (q["difficulty"], natural_key(q["id"])))
    out, taken, k = [], set(), 0
    while len(out) < len(qs):
        f, b, x = 0.0, 0.5, k
        while x:
            f, x, b = f + b * (x & 1), x >> 1, b / 2
        j, k = int(((f + offset) % 1) * len(qs)), k + 1
        while j in taken:
            j = (j + 1) % len(qs)
        taken.add(j)
        out.append(qs[j])
    return out


def demo_listed():
    """The demo list's ids (authoring/data/demo.json, else work/demo/proposal.json), or []."""
    for p in (layout.DEMO_LIST, layout.DEMO_WORK / "proposal.json"):
        if p.exists():
            return load_json(p)["ids"]
    return []


def translate_selection(locale, n, bundle="base"):
    """(ids, stale ids) for the next run (plan 66, D-36): approved, translatable sources of the bundle in another
    locale (decision 235) without an approved non-stale translation and not rejected in the locale; stale ones
    first, then the demo list's ids (plan 174; base only), then one at a time from the subcategory with the fewest approved translations (picks count), spread
    over difficulty;
    ties in categories.json order. Within a subcategory, the source whose level has the most locale
    deficit per pick so far (D-84, D'Hondt); levels without deficit last."""
    pool = load_json(POOL)["questions"]
    have = {t["id"]: t for t in translations.load(locale)["questions"]}
    open_, stale, done = [], [], Counter()
    for q in pool:
        if (q.get("bundle") or "base") != bundle:
            continue
        t = have.get(q["id"])
        if t and t["status"] == "approved" and not translations.is_stale(t, q):
            done[q["subcategory"]] += 1
            continue
        if (q["status"] != "approved" or not translations.translatable(q) or translations.source_locale(q) == locale
                or (t and t["status"] == "rejected")):
            continue
        (stale if t and translations.is_stale(t, q) else open_).append(q)
    stale = [q["id"] for q in sorted(stale, key=lambda q: natural_key(q["id"]))][:n]
    order = categories.subcategories(bundle)
    queues = {sub: spread([q for q in open_ if q["subcategory"] == sub], (k * 0.618034) % 1)  # golden-ratio offsets
              for k, sub in enumerate(order)}
    deficit, per_level = targets.deficits(pool, bundle, locale) or {}, Counter()
    picked = list(stale)
    listed = demo_listed() if bundle == "base" else []
    for q in sorted((q for q in open_ if q["id"] in listed), key=lambda q: listed.index(q["id"])):
        if len(picked) >= n:
            break
        picked.append(q["id"])
        queues[q["subcategory"]].remove(q)
        done[q["subcategory"]] += 1
        per_level[q["difficulty"]] += 1
    while len(picked) < n and any(queues.values()):
        sub = min((s for s in order if queues[s]), key=lambda s: (done[s], order.index(s)))
        q = max(queues[sub], key=lambda q: deficit.get(q["difficulty"], 0) / (per_level[q["difficulty"]] + 1))
        queues[sub].remove(q)
        picked.append(q["id"])
        per_level[q["difficulty"]] += 1
        done[sub] += 1
    return picked, stale


def next_translate_run(locale):
    """(run name, resuming?) — an unfinished tr-<locale>-* run is resumed; otherwise tr-<locale>-<n+1>."""
    runs = work_runs(rf"tr-{re.escape(locale)}-\d+", "run.json")
    open_runs = [r for r in runs if not load_json(WORK / r / "run.json").get("done")]
    if len(open_runs) > 1:
        sys.exit(f"More than one unfinished {locale} translation run: {', '.join(open_runs)}. Ask the developer which to finish.")
    if open_runs:
        return open_runs[0], True
    return f"tr-{locale}-{max((run_number(r) for r in runs), default=0) + 1}", False


def cmd_translate_batch(args):
    """`qgen batch --translate <locale>` (plan 66, D-36): translate → rate → factcheck → merge → review 1 →
    fix → review 2 → record → audit → export → validate → report. Rerunning it continues where it stopped."""
    import health  # authoring/tools/health.py (imports qgen)
    locale = args.translate
    bundle = args.bundle
    check_bundle(bundle)
    if args.run:
        run, resuming = args.run, (WORK / args.run / "run.json").exists()
    else:
        run, resuming = next_translate_run(locale)
    d = WORK / run
    if not args.dry_run:
        lock_run(d)
    again = f"qgen batch --translate {locale}" + (f" --bundle {bundle}" if bundle != "base" else "")
    if resuming:
        if run_locale(d) != locale:
            sys.exit(f"{run} is not a {locale} translation run")
        open_bundle = load_json(d / "run.json").get("bundle", "base")
        if open_bundle != bundle:
            sys.exit(f"{run} is unfinished and writes for bundle {open_bundle!r}, not {bundle!r}. Finish it first: "
                     f"qgen batch --translate {locale}" + (f" --bundle {open_bundle}" if open_bundle != "base" else ""))
        if args.dry_run:
            print(f"{run} is unfinished; `{again}` resumes it.")
            return []
        if args.count or args.ids:
            print("(--count and --ids ignored: resuming)", flush=True)
    else:
        if warn := health.translate_unacked_failure(locale):  # decision 414: warning only
            print(warn, file=sys.stderr)
        if args.ids:
            ids, stale = split_list(args.ids), []
            src = {q["id"]: q for q in load_json(POOL)["questions"]}
            if other := [i for i in ids if (src.get(i, {}).get("bundle") or "base") != bundle or i not in src]:
                sys.exit(f"Not {bundle} questions: {', '.join(other)}")
            if own := [i for i in ids if translations.source_locale(src[i]) == locale]:
                sys.exit(f"Already in {LANGUAGES[locale]}: {', '.join(own)}")
        else:
            pilot = not translations.path(locale).exists()
            ids, stale = translate_selection(locale, args.count or (TRANSLATE_PILOT if pilot else TRANSLATE_SIZE), bundle)
        if not ids:
            sys.exit(f"Nothing to translate into {locale}: every approved {bundle} question has a translation.")
        if args.dry_run:
            print(f"{run} would translate {len(ids)} {bundle} questions into {LANGUAGES[locale]}"
                  + (f" ({len(stale)} stale)" if stale else "") + ": " + ", ".join(ids))
            return []
        save_json(d / "run.json", {"mode": "translate", "locale": locale, "bundle": bundle, "ids": ids, "stale": stale,
                                   "started": datetime.date.today().isoformat()})
    cfg = load_json(d / "run.json")
    progress.verbose = False
    print(f"{'Resuming' if resuming else 'Starting'} {run}: {len(cfg['ids'])} {bundle} questions into {LANGUAGES[locale]}"
          + (f" ({len(cfg.get('stale', []))} stale)" if cfg.get("stale") else "")
          + ". This takes from several minutes to an hour.", flush=True)

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    t0 = run_steps([
        ("translate", cmd_translate, ns(model="opus", locale=None, ids=None)),
        ("rate", cmd_rate, ns(model="opus")),
        ("factcheck", cmd_factcheck, ns(model="sonnet")),
        ("merge", lambda a: cmd_merge(a) or [], ns(min_score=0)),
        ("review 1", cmd_review, ns(model=REVIEW_MODEL, round=1)),
        ("fix", cmd_fix, ns(model="opus", check_model="sonnet")),
        ("review 2", cmd_review, ns(model=REVIEW_MODEL, round=2)),
        ("record", cmd_record, ns()),
        ("audit", lambda a: cmd_audit(a) if load_json(d / "recorded.json") else [], ns(model="opus", batch=run)),
        ("export", lambda a: cmd_export(a) or [], ns()),
    ], again, run)
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": cfg.get("done") or datetime.date.today().isoformat()})
    if lost := unmerged(d):
        sys.exit(f"{run}: {len(lost)} translation(s) have no {locale} entry ({', '.join(lost[:5])}…); "
                 f"rerun `{again}`, if it stays so stop and report.")
    out = write_translate_report(run)
    print(f"  report: {out.relative_to(ROOT)}")
    h = health.translation_health(run)
    print(f"\nDone: {run}: {h['translated']} translated, {h['approved']} approved, {h['needs_work']} need work, "
          f"{h['not travelling']} not travelling ({h['not travelling confirmed']} confirmed) "
          f"(took {progress.duration(time.monotonic() - t0)}).")
    files = commit_files(locale, bundle, out, h["not travelling confirmed"])
    print("Commit exactly this:\n  git add " + " ".join(f.relative_to(ROOT).as_posix() for f in files) + "\n"
          f"  git commit -m \"{run}: {h['translated']} {'' if bundle == 'base' else bundle + ' '}questions into "
          f"{LANGUAGES[locale]}, {h['approved']} approved "
          f"(qgen batch --translate)\"")
    return []


def commit_files(locale, bundle, out, confirmed):
    """Files a translate run changed; a confirmed not-travelling source rejects its translations in every locale."""
    files = [translations.path(locale), layout.POOL_FILE(locale, bundle), layout.BUNDLE_DATA, layout.DEMO_DATA, out]
    if confirmed:
        others = [l for l in translations.LOCALES if l != locale]
        files[1:1] = [POOL] + [f for l in others for f in (translations.path(l), layout.POOL_FILE(l, bundle))]
    return files


def write_translate_report(run):
    """authoring/reports/tr-<locale>-<n>.md (plan 66); `qgen report --qc <run>` adds its QC section."""
    import health  # authoring/tools/health.py (imports qgen)
    d = WORK / run
    cfg = load_json(d / "run.json")
    locale = cfg["locale"]
    h = health.translation_health(run)
    qs = {q["id"]: q for q in batch_questions(run, ("approved", "needs_work", "draft", "rejected"))}
    work = [q for q in qs.values() if q["status"] == "needs_work"]
    away = load_json(d / "not-travelling.json", [])
    calls = costs(d) + costs(d / "audit")
    usd = lambda x: "–" if x is None else f"${x:.2f}"
    lines = [f"# {run}", "",
             f"Made by `qgen batch --translate {locale}` on {datetime.date.today().isoformat()} (plan 66, D-81): "
             f"`{cfg.get('bundle', 'base')}` questions translated into {LANGUAGES[locale]}. Generated file: don't edit by hand.", "",
             f"- Sources: {h['sources']} ({h['stale re-translated']} stale re-translated)",
             f"- Translated: {h['translated']}", f"- Approved: {h['approved']}", f"- Needs work: {h['needs_work']}",
             f"- Not travelling: {h['not travelling']} ({h['not travelling confirmed']} confirmed → `translatable: false`, "
             f"{h['not travelling'] - h['not travelling confirmed']} translated again next run)",
             f"- Claude calls: {len(calls)}, about ${sum(calls):.2f} at list price; "
             f"{usd(h['$ per approved'])} per approved translation (without the audit)",
             f"- Review (optional): {REVIEW_URL}?batch={run}&locale={locale}",
             "", *health.translation_health_section(run), *audit_section(run), *qc_section(run), "## Needs work", ""]
    lines += [f"- **{q['id']}** ({q['subcategory']}) {q['question']} → {q['answer']}: {q['review']['feedback']}"
              for q in work] or ["None."]
    lines += ["", "## Not travelling", ""]
    lines += [f"- **{x['id']}** {x['reason']}, " + ("confirmed" if x.get("decision") == "approved" else "translate again")
              + f": {x['question']} → {x['answer']} ({x['notes']})" for x in away] or ["None."]
    lines += ["", "## Stale re-translated", ""]
    gone = {x["id"] for x in away}
    lines += [f"- {i}: {qs[i]['status'] if i in qs else 'not travelling' if i in gone else 'not merged'}"
              for i in cfg.get("stale", [])] or ["None."]
    return write_report(run, lines)


# the other command groups, after everything here is defined (they import each other)
from audit import audit_section, cmd_audit, run_number  # authoring/tools/audit.py
from report import qc_section  # authoring/tools/report.py
from review_steps import REVIEW_MODEL, batch_questions, cmd_fix, cmd_record, cmd_review  # authoring/tools/review_steps.py
