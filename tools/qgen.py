#!/usr/bin/env python3
"""Question pipeline (plans/07-question-generation.md, D-10).

Writing steps call `claude -p --json-schema` with prompts from tools/prompts/.
Mechanical steps are plain code. Work files live in work/<run>/ and every
step skips what is already done, so a run can be resumed.

    python3 tools/qgen.py fit       --run pilot --subcategories "Volcanes,Piratas"
    python3 tools/qgen.py draft     --run pilot
    python3 tools/qgen.py rate      --run pilot
    python3 tools/qgen.py factcheck --run pilot
    python3 tools/qgen.py dedupe    --run pilot
    python3 tools/qgen.py merge     --run pilot --min-score 0
    python3 tools/qgen.py report    [--run pilot]
    python3 tools/qgen.py validate

Revising questions that are already in the pool (07, QG-13):

    python3 tools/qgen.py import    --run first-120 --batch first-120 [--assign-unbatched]
    python3 tools/qgen.py rate      --run first-120
    python3 tools/qgen.py factcheck --run first-120
    python3 tools/qgen.py revise    --run first-120
    python3 tools/qgen.py apply     --run first-120
"""
import argparse, concurrent.futures, datetime, difflib, json, random, re, subprocess, sys, threading, unicodedata
from pathlib import Path

import categories  # tools/categories.py: data/categories.json (D-19)
import media  # tools/media.py: the media cache (D-17)

ROOT = Path(__file__).resolve().parent.parent
POOL = ROOT / "data" / "questions.json"
PROMPTS = ROOT / "tools" / "prompts"
WORK = ROOT / "work"
STYLES_FILE = ROOT / "question-styles.txt"

# Target share per difficulty level (07, "Difficulty target"): ~70 % at 4–7.
LEVEL_WEIGHTS = {1: 5, 2: 5, 3: 5, 4: 17.5, 5: 17.5, 6: 17.5, 7: 17.5, 8: 5, 9: 5, 10: 5}
RUBRIC = ["correct", "unambiguous", "no_giveaway", "distractors", "age_fit", "fun", "description"]
# Below 4 on any of these drops a question (07). The soft scores didn't predict the
# gamemaster's decisions in the pilot, so they are recorded but don't filter by default.
HARD_CRITERIA = ["correct", "unambiguous", "no_giveaway"]
SOFT_CRITERIA = ["distractors", "age_fit", "fun", "description"]


# --- helpers -----------------------------------------------------------------

def load_json(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

_save_lock = threading.Lock()

def save_json(path, data):
    with _save_lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(path)

def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def norm(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    words = [w for w in text.split() if w not in {"el", "la", "los", "las", "un", "una", "de", "del"}]
    return " ".join(words)

def read_lines(path):
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

def prompt(*names):
    return "\n\n".join((PROMPTS / f"{n}.md").read_text(encoding="utf-8") for n in names)

def run_dir(args):
    d = WORK / args.run
    d.mkdir(parents=True, exist_ok=True)
    return d

def parallel(fn, items, jobs):
    """Run fn over items; report failures without stopping the others."""
    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futures = {ex.submit(fn, it): it for it in items}
        for f in concurrent.futures.as_completed(futures):
            try:
                f.result()
            except Exception as e:  # noqa: BLE001 — keep the batch going
                failures += 1
                print(f"  FAILED {futures[f]}: {e}", file=sys.stderr)
    if failures:
        print(f"{failures} item(s) failed; rerun the same command to retry them.", file=sys.stderr)


def claude(system, user, schema, model, cwd, web=False, retries=2):
    """One fresh `claude -p` session returning structured output."""
    cmd = ["claude", "-p", "--output-format", "json", "--no-session-persistence",
           "--model", model, "--system-prompt", system, "--json-schema", json.dumps(schema)]
    if web:
        cmd += ["--tools", "WebSearch,WebFetch", "--allowedTools", "WebSearch", "WebFetch"]
    else:
        cmd += ["--tools", ""]
    last = None
    for _ in range(retries + 1):
        p = subprocess.run(cmd, input=user, capture_output=True, text=True, cwd=cwd, timeout=1800)
        try:
            out = json.loads(p.stdout)
        except json.JSONDecodeError:
            last = f"no JSON from claude (exit {p.returncode}): {p.stderr.strip()[:300] or p.stdout[:300]}"
            continue
        if out.get("is_error") or out.get("structured_output") is None:
            last = f"claude error: {str(out.get('result'))[:300]}"
            continue
        with open(Path(cwd) / "costs.log", "a", encoding="utf-8") as f:
            f.write(f"{model}\t{out.get('total_cost_usd')}\n")
        return out["structured_output"]
    raise RuntimeError(last)


# --- schemas -----------------------------------------------------------------

STR = {"type": "string"}
INT = {"type": "integer"}
STR_LIST = {"type": "array", "items": STR}

FIT_SCHEMA = {"type": "object", "required": ["subcategories"], "properties": {"subcategories": {
    "type": "array", "items": {"type": "object", "required": ["subcategory", "styles"], "properties": {
        "subcategory": STR,
        "styles": {"type": "array", "items": {"type": "object", "required": ["style", "score", "idea"],
                   "properties": {"style": STR, "score": INT, "idea": STR}}}}}}}}

MEDIA_SCHEMA = {"type": "object", "required": ["type", "role", "query", "note"], "properties": {
    "type": {"type": "string", "enum": ["image", "audio", "video"]},
    "role": {"type": "string", "enum": ["decorative", "illustrative", "essential"]},
    "query": STR, "note": STR}}

QUESTION_SCHEMA = {"type": "object", "required": [
    "slot", "style", "difficulty", "description", "question", "answer", "wrong_answers", "hints",
    "media", "fun_fact", "needs_media", "needs_fact_check", "background_query"], "properties": {
    "slot": INT, "style": STR, "difficulty": INT, "description": STR, "question": STR, "answer": STR,
    "wrong_answers": STR_LIST, "hints": STR_LIST, "media": MEDIA_SCHEMA, "fun_fact": STR,
    "needs_media": {"type": "boolean"}, "needs_fact_check": {"type": "boolean"}, "background_query": STR}}

DRAFT_SCHEMA = {"type": "object", "required": ["questions", "skipped"], "properties": {
    "questions": {"type": "array", "items": QUESTION_SCHEMA},
    "skipped": {"type": "array", "items": {"type": "object", "required": ["slot", "reason"],
                "properties": {"slot": INT, "reason": STR}}}}}

RATE_SCHEMA = {"type": "object", "required": ["ratings"], "properties": {"ratings": {
    "type": "array", "items": {"type": "object",
        "required": ["id", *RUBRIC, "difficulty_estimate", "notes"],
        "properties": {"id": STR, **{k: INT for k in RUBRIC}, "difficulty_estimate": INT, "notes": STR}}}}}

REVISED_SCHEMA = {"type": "object", "required": [
    "difficulty", "description", "question", "answer", "wrong_answers", "hints", "media", "fun_fact",
    "needs_media", "background_query"], "properties": {
    "difficulty": INT, "description": STR, "question": STR, "answer": STR, "wrong_answers": STR_LIST,
    "hints": STR_LIST, "media": MEDIA_SCHEMA, "fun_fact": STR, "needs_media": {"type": "boolean"},
    "background_query": STR}}

REVISE_SCHEMA = {"type": "object", "required": ["results"], "properties": {"results": {
    "type": "array", "items": {"type": "object", "required": ["id", "action", "reason", "question"],
        "properties": {"id": STR, "action": {"type": "string", "enum": ["keep", "revise", "drop"]},
                       "reason": STR, "question": REVISED_SCHEMA}}}}}

FACT_SCHEMA = {"type": "object", "required": ["checks"], "properties": {"checks": {
    "type": "array", "items": {"type": "object", "required": ["id", "verdict", "problem", "correction", "sources"],
        "properties": {"id": STR, "verdict": {"type": "string", "enum": ["confirmed", "wrong", "uncertain"]},
                       "problem": STR, "correction": STR, "sources": STR_LIST}}}}}


# --- steps -------------------------------------------------------------------

def cmd_fit(args):
    d = run_dir(args)
    cfg = load_json(d / "run.json")
    if cfg is None:
        if not args.subcategories:
            sys.exit("First call for a run needs --subcategories.")
        cfg = {"subcategories": [s.strip() for s in args.subcategories.split(",") if s.strip()]}
        unknown = [s for s in cfg["subcategories"] if s not in categories.broad_of()]
        if unknown:
            sys.exit(f"Not in data/categories.json (add them there first): {', '.join(unknown)}")
        save_json(d / "run.json", cfg)
    styles = read_lines(STYLES_FILE)
    fit = load_json(d / "fit.json", {})
    todo = [s for s in cfg["subcategories"] if s not in fit]
    batches = [todo[i:i + 8] for i in range(0, len(todo), 8)]
    system = prompt("house-style", "fit").replace("{max_styles}", str(args.max_styles))

    def work(batch):
        user = ("## Question styles (best first)\n" + "\n".join(f"- {s}" for s in styles)
                + "\n\n## Subcategories\n" + "\n".join(f"- {s}" for s in batch))
        out = claude(system, user, FIT_SCHEMA, args.model, d)
        for row in out["subcategories"]:
            if row["subcategory"] not in batch:
                print(f"  ignoring bad fit row: {row['subcategory']}", file=sys.stderr)
                continue
            row["styles"] = [s for s in row["styles"] if s["style"] in styles and s["score"] >= 4][:args.max_styles]
            fit[row["subcategory"]] = row
        save_json(d / "fit.json", fit)
        print(f"  fit: {', '.join(batch)}")

    parallel(work, batches, args.jobs)
    print(f"fit.json: {len(fit)}/{len(cfg['subcategories'])} subcategories")


def assign_difficulties(fit, seed):
    """Spread target levels over all slots to match LEVEL_WEIGHTS."""
    slots = [(sub, i) for sub in sorted(fit) for i in range(len(fit[sub]["styles"]))]
    n, total = len(slots), sum(LEVEL_WEIGHTS.values())
    exact = {lvl: n * w / total for lvl, w in LEVEL_WEIGHTS.items()}
    counts = {lvl: int(x) for lvl, x in exact.items()}
    for lvl in sorted(exact, key=lambda l: exact[l] - counts[l], reverse=True)[:n - sum(counts.values())]:
        counts[lvl] += 1
    levels = [lvl for lvl, c in counts.items() for _ in range(c)]
    random.Random(seed).shuffle(levels)
    return dict(zip(slots, levels))


def existing_answers(pool):
    return sorted({f"{q['answer']} ({q['question'][:60]})" for q in pool["questions"]})


def cmd_draft(args):
    d = run_dir(args)
    fit = load_json(d / "fit.json") or sys.exit("Run `fit` first.")
    pool = load_json(POOL)
    targets = assign_difficulties(fit, args.seed)
    avoid = "\n".join(f"- {a}" for a in existing_answers(pool))
    system = prompt("house-style", "draft")
    todo = [s for s in sorted(fit) if fit[s]["styles"] and not (d / "drafts" / f"{slug(s)}.json").exists()]
    broad = categories.broad_of()

    def work(sub):
        row = fit[sub]
        slots = [{"slot": i, "style": s["style"], "target_difficulty": targets[(sub, i)], "idea": s["idea"]}
                 for i, s in enumerate(row["styles"])]
        user = (f"## Subcategory\n{sub} (broad category: {broad[sub]['name']})\n\n## Slots\n"
                + json.dumps(slots, ensure_ascii=False, indent=2)
                + f"\n\n## Already in the pool (avoid these answers and topics)\n{avoid}")
        out = claude(system, user, DRAFT_SCHEMA, args.model, d)
        good = []
        for q in out["questions"]:
            problems = check_question_shape(q)
            if problems:
                print(f"  {sub}: dropped malformed question ({'; '.join(problems)})", file=sys.stderr)
                continue
            if not 0 <= q["slot"] < len(slots):
                print(f"  {sub}: dropped question with unknown slot {q['slot']}", file=sys.stderr)
                continue
            q["style"] = slots[q["slot"]]["style"]  # the model sometimes shortens style names
            q["tmp_id"] = f"{slug(sub)}-{q['slot']}"
            q["subcategory"] = sub
            q["media"]["note"] = q["media"]["note"] or None
            good.append(q)
        save_json(d / "drafts" / f"{slug(sub)}.json", {"questions": good, "skipped": out["skipped"]})
        print(f"  draft: {sub}: {len(good)} written, {len(out['skipped'])} skipped")

    parallel(work, todo, args.jobs)


def check_question_shape(q):
    problems = []
    if len(q["wrong_answers"]) != 3: problems.append("needs 3 wrong answers")
    if len(q["hints"]) != 3: problems.append("needs 3 hints")
    if not 1 <= q["difficulty"] <= 10: problems.append("difficulty out of range")
    if len({norm(o) for o in [q["answer"], *q["wrong_answers"]]}) != 4: problems.append("duplicate options")
    return problems


def drafts(d):
    for f in sorted((d / "drafts").glob("*.json")):
        yield f.stem, load_json(f)["questions"]


def for_review(q):
    keys = ["style", "difficulty", "description", "question", "answer", "wrong_answers", "hints", "media", "fun_fact"]
    return {"id": q["tmp_id"], **{k: q[k] for k in keys}}


def cmd_rate(args):
    d = run_dir(args)
    system = prompt("house-style", "rate")
    todo = [(name, qs) for name, qs in drafts(d) if qs and not (d / "ratings" / f"{name}.json").exists()]

    def work(item):
        name, qs = item
        user = "## Questions\n" + json.dumps([for_review(q) for q in qs], ensure_ascii=False, indent=2)
        out = claude(system, user, RATE_SCHEMA, args.model, d)
        save_json(d / "ratings" / f"{name}.json", {r["id"]: r for r in out["ratings"]})
        print(f"  rate: {name}")

    parallel(work, todo, args.jobs)


def cmd_factcheck(args):
    d = run_dir(args)
    system = prompt("factcheck")
    todo = []
    for name, qs in drafts(d):
        need = [q for q in qs if q["needs_fact_check"] or re.search(r"\d", q["question"] + q["answer"] + q["fun_fact"])]
        if need and not (d / "factchecks" / f"{name}.json").exists():
            todo.append((name, need))

    def work(item):
        name, qs = item
        user = "## Questions (Spanish)\n" + json.dumps([for_review(q) for q in qs], ensure_ascii=False, indent=2)
        out = claude(system, user, FACT_SCHEMA, args.model, d, web=True)
        save_json(d / "factchecks" / f"{name}.json", {c["id"]: c for c in out["checks"]})
        print(f"  factcheck: {name}: " + ", ".join(c["verdict"] for c in out["checks"]))

    parallel(work, todo, args.jobs)


def duplicates(q, pool_questions):
    """Return a reason if q duplicates a pool question, else None.

    Only questions with the same answer can be duplicates: similar wording with a
    different answer is just a shared template ("Escucha: ¿qué … suena?"). Same
    answer counts when the wording is similar too, or both need the same kind of
    essential picture/sound (e.g. two "Mira la foto" questions about the Komodo dragon).
    """
    qa, qq = norm(q["answer"]), norm(q["question"])
    if qa.replace(" ", "").isdigit():
        return None
    for p in pool_questions:
        if qa != norm(p["answer"]):
            continue
        sim = difflib.SequenceMatcher(None, qq, norm(p["question"])).ratio()
        both_essential = (q["media"]["role"] == p["media"]["role"] == "essential"
                          and q["media"]["type"] == p["media"]["type"])
        if sim > 0.6 or both_essential:
            return f"like {p.get('id') or p.get('tmp_id')}: {p['question']} → {p['answer']}"
    return None


def collect(d):
    ratings, checks = {}, {}
    for f in (d / "ratings").glob("*.json"): ratings.update(load_json(f))
    for f in (d / "factchecks").glob("*.json"): checks.update(load_json(f))
    return ratings, checks


def cmd_dedupe(args):
    d = run_dir(args)
    pool = load_json(POOL)["questions"]
    seen = list(pool)
    for _, qs in drafts(d):
        for q in qs:
            why = duplicates(q, seen)
            if why: print(f"  {q['tmp_id']}: {q['question']} → {q['answer']}\n      {why}")
            seen.append(q)


def soft_score(r):
    return sum(r[k] for k in SOFT_CRITERIA) / len(SOFT_CRITERIA)


def cmd_merge(args):
    d = run_dir(args)
    data = load_json(POOL)
    pool = data["questions"]
    ratings, checks = collect(d)
    merged = set(load_json(d / "merged.json", []))
    next_id = max(int(q["id"][2:]) for q in pool) + 1
    added, dropped = [], load_json(d / "dropped.json", [])
    for _, qs in drafts(d):
        for q in qs:
            tid = q["tmp_id"]
            if tid in merged: continue
            r, c = ratings.get(tid), checks.get(tid)
            needs_check = q["needs_fact_check"] or bool(re.search(r"\d", q["question"] + q["answer"] + q["fun_fact"]))
            reason = None
            if r is None: reason = "not rated yet"
            elif needs_check and c is None: reason = "not fact-checked yet"
            elif any(r.get(k, 5) < 4 for k in HARD_CRITERIA):
                reason = "hard fail: " + ", ".join(f"{k} {r.get(k, '-')}" for k in HARD_CRITERIA)
            elif c and c["verdict"] == "wrong": reason = f"fact-check wrong: {c['problem']}"
            elif soft_score(r) < args.min_score: reason = f"soft score {soft_score(r):.2f} < {args.min_score}"
            else: reason = duplicates(q, pool) and "duplicate " + duplicates(q, pool)
            if reason:
                if not reason.startswith("not "):
                    dropped.append({"tmp_id": tid, "reason": reason, "question": q["question"], "answer": q["answer"]})
                    merged.add(tid)
                print(f"  skip {tid}: {reason}")
                continue
            new = {
                "id": f"q-{next_id:04d}", "status": "draft",
                "difficulty": q["difficulty"], "description": q["description"], "question": q["question"],
                "answer": q["answer"], "wrong_answers": q["wrong_answers"], "hints": q["hints"],
                "media": {**q["media"], "source_url": None, "file_url": None, "credit": None},
                "fun_fact": q["fun_fact"], "subcategory": q["subcategory"], "style": q["style"],
                "quality": {k: r.get(k) for k in [*RUBRIC, "difficulty_estimate", "notes"]},
                "fact_checked": bool(c and c["verdict"] == "confirmed"), "needs_media": q["needs_media"],
                "batch": args.run, "review": None,
                "background": ({"query": q.get("background_query") or q["media"]["query"], "source_url": None,
                                "file_url": None, "credit": None} if q["media"]["type"] == "audio" else None),
            }
            next_id += 1
            pool.append(new); added.append(new["id"]); merged.add(tid)
    save_json(POOL, data)
    save_json(d / "merged.json", sorted(merged))
    save_json(d / "dropped.json", dropped)
    print(f"merged {len(added)} question(s) into {POOL.relative_to(ROOT)}; {len(dropped)} dropped in total (see dropped.json)")


# --- revising pool questions (QG-13) -------------------------------------------

REVISABLE = ["difficulty", "description", "question", "answer", "wrong_answers", "hints", "media", "fun_fact",
             "needs_media", "background"]


def save_pool(data):
    save_json(POOL, data)


def cmd_import(args):
    """Copy a batch's draft/needs_work pool questions into work/<run>/drafts/ for rate/factcheck/revise."""
    d = run_dir(args)
    data = load_json(POOL)
    if args.assign_unbatched:
        n = 0
        for q in data["questions"]:
            if q.get("batch") is None:
                q["batch"] = args.batch
                n += 1
        save_pool(data)
        print(f"assigned batch {args.batch!r} to {n} question(s) without a batch")
    qs = [q for q in data["questions"] if q.get("batch") == args.batch and q["status"] in ("draft", "needs_work")]
    work = []
    for q in qs:
        w = {k: q[k] for k in ["difficulty", "description", "question", "answer", "wrong_answers", "hints",
                               "fun_fact"]}
        w.update(tmp_id=q["id"], style=q.get("style"), subcategory=q.get("subcategory"),
                 media={k: q["media"][k] for k in ["type", "role", "query", "note"]},
                 needs_fact_check=True, needs_media=bool(q.get("needs_media")),
                 background_query=(q.get("background") or {}).get("query", ""),
                 feedback=(q.get("review") or {}).get("feedback") if q["status"] == "needs_work" else None)
        work.append(w)
    for i in range(0, len(work), 10):
        save_json(d / "drafts" / f"chunk-{i // 10 + 1:02d}.json", {"questions": work[i:i + 10], "skipped": []})
    save_json(d / "run.json", {"source": "pool", "batch": args.batch})
    print(f"imported {len(work)} question(s) into {len(range(0, len(work), 10))} chunk(s)")


DIFFICULTY_GAP = 3  # rater estimates are rough (pilot: ~2.4 levels off), so only big gaps count


def issues_of(q, r, c):
    """Reasons to revise a question; empty when it looks fine.

    Only what the pilot showed to matter (D-16): the gamemaster's feedback, the fact-check,
    the hard criteria, and big difficulty gaps. Low soft scores (fun, distractors…) didn't
    predict the gamemaster's decisions, so they don't trigger a revision.
    """
    out = []
    if q.get("feedback"):
        out.append(f"gamemaster feedback: {q['feedback']}")
    if c and c["verdict"] != "confirmed":
        out.append(f"fact-check {c['verdict']}: {c['problem']} correction: {c['correction']}")
    if r:
        hard = [f"{k} {r[k]}" for k in HARD_CRITERIA if r.get(k) is not None and r[k] < 4]
        if hard:
            out.append(f"rater: hard criteria below 4: {', '.join(hard)}")
        if abs(r["difficulty_estimate"] - q["difficulty"]) >= DIFFICULTY_GAP:
            out.append(f"difficulty: currently {q['difficulty']}, rater estimates {r['difficulty_estimate']}; "
                       "judge it yourself with the calibration examples")
        if out:
            out.append(f"rater notes: {r['notes']}")
    return out


def cmd_revise(args):
    d = run_dir(args)
    ratings, checks = collect(d)
    system = prompt("house-style", "revise")
    todo = []
    for name, qs in drafts(d):
        if (d / "revisions" / f"{name}.json").exists():
            continue
        items = []
        for q in qs:
            found = issues_of(q, ratings.get(q["tmp_id"]), checks.get(q["tmp_id"]))
            if found:
                items.append({**for_review(q), "background_query": q.get("background_query", ""),
                              "needs_media": q.get("needs_media", False), "issues": found})
        todo.append((name, items))

    def work(item):
        name, items = item
        results = {}
        if items:
            user = "## Questions with issues\n" + json.dumps(items, ensure_ascii=False, indent=2)
            out = claude(system, user, REVISE_SCHEMA, args.model, d)
            results = {r["id"]: r for r in out["results"]}
        save_json(d / "revisions" / f"{name}.json", results)
        actions = [r["action"] for r in results.values()]
        print(f"  revise: {name}: {len(items)} with issues → "
              + ", ".join(f"{a} {actions.count(a)}" for a in ["keep", "revise", "drop"] if a in actions))

    parallel(work, todo, args.jobs)


def cmd_apply(args):
    d = run_dir(args)
    cfg = load_json(d / "run.json") or {}
    if cfg.get("source") != "pool":
        sys.exit("apply is for imported pool questions; use merge for new drafts.")
    ratings, checks = collect(d)
    revisions = {}
    for f in (d / "revisions").glob("*.json"):
        revisions.update(load_json(f))
    applied = set(load_json(d / "applied.json", []))
    data = load_json(POOL)
    today = datetime.date.today().isoformat()
    counts = {"keep": 0, "revise": 0, "drop": 0, "unchanged": 0, "malformed": 0}
    sys.path.insert(0, str(ROOT / "tools"))
    import media as media_tool

    for q in data["questions"]:
        qid = q["id"]
        if qid in applied or q.get("batch") != cfg["batch"] or q["status"] not in ("draft", "needs_work"):
            continue
        r, c, rev = ratings.get(qid), checks.get(qid), revisions.get(qid)
        if r:
            q["quality"] = {k: r.get(k) for k in [*RUBRIC, "difficulty_estimate", "notes"]}
        if c:
            q["fact_checked"] = c["verdict"] == "confirmed"
        if not rev or rev["action"] == "keep":
            counts["keep" if rev else "unchanged"] += 1
            applied.add(qid)
            continue
        if rev["action"] == "drop":
            q["revision"] = {"action": "drop", "reason": rev["reason"], "previous": {}, "revised_on": today}
        else:
            new = rev["question"]
            if check_question_shape(new):
                print(f"  {qid}: revision malformed ({'; '.join(check_question_shape(new))}), skipped")
                counts["malformed"] += 1
                continue
            new_media = {**q["media"], **new["media"], "note": new["media"]["note"] or None}
            media_changed = any(new_media[k] != q["media"][k] for k in ["type", "query"])
            if media_changed:
                new_media.update(source_url=None, file_url=None, credit=None)
            if new_media["type"] == "audio":
                bgq = new.get("background_query") or (q.get("background") or {}).get("query") or new_media["query"]
                old_bg = q.get("background")
                new_bg = old_bg if old_bg and old_bg["query"] == bgq else {
                    "query": bgq, "source_url": None, "file_url": None, "credit": None}
            else:
                new_bg = None
            proposed = {**{k: new[k] for k in ["difficulty", "description", "question", "answer", "wrong_answers",
                                               "hints", "fun_fact", "needs_media"]},
                        "media": new_media, "background": new_bg}
            previous = {k: q.get(k) for k in REVISABLE if proposed[k] != q.get(k)}
            if "difficulty" in previous and q.get("difficulty_original") is None:
                q["difficulty_original"] = q["difficulty"]
            q.update(proposed)
            q["revision"] = {"action": "revise", "reason": rev["reason"], "previous": previous, "revised_on": today}
            for slot in ("media", "background"):  # stale candidates for a changed search
                if slot in previous:
                    path = media_tool.candidates_path(qid, slot)
                    if path.exists():
                        path.unlink()
        if q["status"] == "needs_work":
            q["status"], q["review"] = "draft", None
        counts[rev["action"]] += 1
        applied.add(qid)
    save_pool(data)
    save_json(d / "applied.json", sorted(applied))
    print("applied: " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
          + f". Next: python3 tools/media.py fetch --batch {cfg['batch']}")


def count(items, key):
    out = {}
    for it in items:
        k = key(it); out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (0, kv[0], "") if isinstance(kv[0], int) else (1, 0, str(kv[0]))))


def cmd_report(args):
    pool = load_json(POOL)["questions"]
    broad = categories.broad_of()
    print(f"pool: {len(pool)} questions")
    for title, key in [("status", lambda q: q["status"]), ("difficulty", lambda q: q["difficulty"]),
                       ("category", lambda q: broad[q["subcategory"]]["slug"] if q.get("subcategory") in broad else None), ("style", lambda q: q.get("style")),
                       ("media", lambda q: f"{q['media']['type']}/{q['media']['role']}")]:
        print(f"  by {title}: {count(pool, key)}")
    if args.run:
        d = run_dir(args)
        ratings, checks = collect(d)
        qs = [q for _, qq in drafts(d) for q in qq]
        skipped = sum(len(load_json(f)["skipped"]) for f in (d / "drafts").glob("*.json"))
        print(f"run {args.run}: {len(qs)} drafted, {skipped} slots skipped, {len(ratings)} rated, {len(checks)} fact-checked")
        if ratings:
            for k in RUBRIC:
                vals = [r[k] for r in ratings.values() if k in r]  # older runs lack newer criteria
                if vals:
                    print(f"  avg {k}: {sum(vals) / len(vals):.2f}")
        print(f"  fact-check verdicts: {count(checks.values(), lambda c: c['verdict'])}")
        print(f"  target difficulty: {count(qs, lambda q: q['difficulty'])}")
        print(f"  by style: {count(qs, lambda q: q['style'])}")


def cmd_validate(args):
    data = load_json(POOL)
    errors, warnings, ids = [], [], set()
    subcategories = categories.broad_of()
    for q in data["questions"]:
        qid = q.get("id", "?")
        for k in ["id", "status", "subcategory", "difficulty", "description", "question", "answer",
                  "wrong_answers", "hints", "media", "fun_fact"]:
            if k not in q: errors.append(f"{qid}: missing {k}")
        if qid in ids: errors.append(f"{qid}: duplicate id")
        ids.add(qid)
        if q.get("status") not in {"draft", "approved", "rejected", "needs_work"}: errors.append(f"{qid}: bad status")
        rv = q.get("review")
        if rv is not None and (rv.get("decision") != q.get("status") or "feedback" not in rv or "reviewed_on" not in rv):
            errors.append(f"{qid}: review does not match status")
        if q.get("subcategory") not in subcategories: errors.append(f"{qid}: subcategory not in data/categories.json (D-19)")
        m = q.get("media", {})
        if m.get("type") not in {"image", "audio", "video"} or m.get("role") not in {"decorative", "illustrative", "essential"}:
            errors.append(f"{qid}: bad media type/role")
        bg = q.get("background")
        if (bg is not None) != (m.get("type") == "audio"):
            errors.append(f"{qid}: background must be set exactly for audio questions (D-14)")
        if q.get("status") == "approved":  # warnings only: media/ is a cache (D-17)
            for label, slot in [("media", m), ("background", bg)]:
                if slot is None:
                    continue
                if not slot.get("file_url"):
                    warnings.append(f"{qid}: approved but no {label} picked")
                elif not media.cache_path(slot["file_url"]).is_file():
                    warnings.append(f"{qid}: {label} not cached")
        if all(k in q for k in ["wrong_answers", "hints", "difficulty", "answer"]):
            errors += [f"{qid}: {p}" for p in check_question_shape(q)]
    if warnings:
        print("\n".join(f"warning: {w}" for w in warnings))
        print(f"({len(warnings)} warning(s); `python3 tools/media.py sync --status approved` fills the cache)")
    print("\n".join(errors) or f"OK: {len(data['questions'])} questions")
    sys.exit(1 if errors else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    def add(name, fn, model=None, run=True):
        p = sub.add_parser(name)
        p.set_defaults(fn=fn)
        if run: p.add_argument("--run", required=True, help="name of the work/<run>/ directory")
        if model:
            p.add_argument("--model", default=model)
            p.add_argument("--jobs", type=int, default=3, help="parallel claude calls")
        return p
    add("fit", cmd_fit, "opus").add_argument("--subcategories", help="comma-separated, first call only")
    sub.choices["fit"].add_argument("--max-styles", type=int, default=4)
    add("draft", cmd_draft, "opus").add_argument("--seed", type=int, default=1)
    add("rate", cmd_rate, "opus")
    add("factcheck", cmd_factcheck, "sonnet")
    add("dedupe", cmd_dedupe)
    add("merge", cmd_merge).add_argument("--min-score", type=float, default=0,
                                         help="minimum mean of distractors/age_fit/fun/description "
                                              "(default 0: off; the pilot showed it doesn't predict the gamemaster)")
    imp = add("import", cmd_import)
    imp.add_argument("--batch", required=True, help="pool batch to revise")
    imp.add_argument("--assign-unbatched", action="store_true", help="give questions without a batch this batch name first")
    add("revise", cmd_revise, "opus")
    add("apply", cmd_apply)
    add("report", cmd_report, run=False).add_argument("--run")
    add("validate", cmd_validate, run=False)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
