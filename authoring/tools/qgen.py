#!/usr/bin/env python3
"""Question pipeline (plans/07-question-generation.md, D-10, D-36). Never ships (D-35).

An LLM makes a batch with exactly one command (authoring/RUNBOOK.md):

    qgen batch

It runs these steps in a fixed order; they stay available one by one for debugging:

    qgen fit --run <run> --subcategories "Volcanes,Piratas"
    qgen draft | rate | factcheck | dedupe | revise | apply | merge --run <run>
    qgen media | sheets | review [--round 2] | research | record | sync | batch-report --run <run>
    qgen export                     # app/data/pool.json from authoring/data/questions.json
    qgen report [--run <run>] [--player <name>] [--subcategories]
    qgen validate

Writing steps call `claude -p --json-schema` with prompts from authoring/tools/prompts/. Work files
live in work/<run>/ and every step skips what is already done, so a run can be resumed.

Revising questions that are already in the pool (07, QG-13):

    qgen import --run <run> --batch <batch> [--assign-unbatched]
    qgen rate | factcheck | revise | apply --run <run>
"""
import argparse, concurrent.futures, datetime, difflib, json, random, re, subprocess, sys, threading, unicodedata
from pathlib import Path

import layout  # noqa: F401  (paths; also makes app/server importable, D-35)
from layout import PROMPTS, REPO as ROOT, SOURCE_POOL as POOL, STYLES_FILE, WORK
import categories  # app/server/categories.py: app/data/categories.json (D-19)
import media_cache as media  # app/server/media_cache.py: the media cache (D-17)
import selection  # app/server/selection.py: levels and the supply check (GF-5)
from pool_export import export_text  # authoring/tools/pool_export.py (D-35)

# Target share per difficulty level (07, "Difficulty target", D-31): what the 12 levels'
# ranges (D-22) show per game, times 3.
LEVEL_WEIGHTS = {1: 12, 2: 6, 3: 10, 4: 16, 5: 20, 6: 23, 7: 14, 8: 14, 9: 16, 10: 13}
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
    """Run fn over items; report failures without stopping the others. Returns the errors."""
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futures = {ex.submit(fn, it): it for it in items}
        for f in concurrent.futures.as_completed(futures):
            try:
                f.result()
            except Exception as e:  # noqa: BLE001 — keep the batch going
                errors.append(e)
                label = futures[f][0] if isinstance(futures[f], tuple) else futures[f]
                print(f"  FAILED {label}: {e}", file=sys.stderr)
    if errors:
        print(f"{len(errors)} item(s) failed; rerun the same command to retry them.", file=sys.stderr)
    return errors


class UsageLimit(RuntimeError):
    """Claude reported a usage or session limit: wait for the reset, then rerun."""


LIMIT_WORDS = ("usage limit", "session limit", "rate limit", "hit your limit")


def main_model(out):
    """The model that did the work in a `claude -p` result: the one with the most output tokens
    (Claude Code may also call a small helper model)."""
    usage = out.get("modelUsage") or {}
    return max(usage, key=lambda m: usage[m].get("outputTokens", 0)) if usage else None


def claude(system, user, schema, model, cwd, web=False, retries=2, read=False, with_model=False):
    """One fresh `claude -p` session returning structured output (and the model id if asked).
    read=True lets the session open files under cwd with the Read tool (contact sheets)."""
    cmd = ["claude", "-p", "--output-format", "json", "--no-session-persistence",
           "--model", model, "--system-prompt", system, "--json-schema", json.dumps(schema)]
    if web:
        cmd += ["--tools", "WebSearch,WebFetch", "--allowedTools", "WebSearch", "WebFetch"]
    elif read:
        cmd += ["--tools", "Read", "--allowedTools", "Read"]
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
            if any(w in last.lower() for w in LIMIT_WORDS):
                raise UsageLimit(last)
            continue
        with open(Path(cwd) / "costs.log", "a", encoding="utf-8") as f:
            f.write(f"{model}\t{out.get('total_cost_usd')}\n")
        return (out["structured_output"], main_model(out)) if with_model else out["structured_output"]
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
            sys.exit(f"Not in app/data/categories.json (add them there first): {', '.join(unknown)}")
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

    errors = parallel(work, batches, args.jobs)
    print(f"fit.json: {len(fit)}/{len(cfg['subcategories'])} subcategories")
    return errors


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

    return parallel(work, todo, args.jobs)


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
        missing = {q["tmp_id"] for q in qs} - {r["id"] for r in out["ratings"]}
        if missing:  # a partial file would count as done and never be retried
            raise RuntimeError(f"no rating for {', '.join(sorted(missing))}")
        save_json(d / "ratings" / f"{name}.json", {r["id"]: r for r in out["ratings"]})
        print(f"  rate: {name}")

    return parallel(work, todo, args.jobs)


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

    return parallel(work, todo, args.jobs)


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
    ids = load_json(d / "ids.json", {})  # tmp_id -> pool id, for the review step
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
            pool.append(new); added.append(new["id"]); merged.add(tid); ids[tid] = new["id"]
    save_json(POOL, data)
    save_json(d / "ids.json", ids)
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
        if name.startswith("revised-") or (d / "revisions" / f"{name}.json").exists():
            continue  # one round only (QG-16): revised drafts are judged by rate/factcheck, not revised again
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

    return parallel(work, todo, args.jobs)


def cmd_apply(args):
    d = run_dir(args)
    cfg = load_json(d / "run.json") or {}
    revisions = {}
    for f in (d / "revisions").glob("*.json"):
        revisions.update(load_json(f))
    applied = set(load_json(d / "applied.json", []))
    if cfg.get("source") != "pool":
        return apply_to_drafts(d, revisions, applied)
    ratings, checks = collect(d)
    data = load_json(POOL)
    today = datetime.date.today().isoformat()
    counts = {"keep": 0, "revise": 0, "drop": 0, "unchanged": 0, "malformed": 0}
    import media as media_tool  # authoring/tools/media.py

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
          + f". Next: trivia-media fetch --batch {cfg['batch']}")


def apply_to_drafts(d, revisions, applied):
    """New drafts (not yet merged): revised questions move to a new draft file and lose their
    rating and fact-check, so `rate` and `factcheck` judge the new version before `merge`.
    Kept and dropped ones stay as they are; merge's hard checks still decide."""
    moved, counts = [], {"keep": 0, "revise": 0, "drop": 0, "malformed": 0}
    for name, qs in list(drafts(d)):
        rest = []
        for q in qs:
            rev = revisions.get(q["tmp_id"])
            if q["tmp_id"] in applied or not rev or rev["action"] != "revise":
                if rev and q["tmp_id"] not in applied:
                    counts[rev["action"]] += 1
                    applied.add(q["tmp_id"])
                rest.append(q)
                continue
            new = rev["question"]
            if check_question_shape(new):
                print(f"  {q['tmp_id']}: revision malformed ({'; '.join(check_question_shape(new))}), kept old")
                counts["malformed"] += 1
                rest.append(q)
                continue
            keys = ["difficulty", "description", "question", "answer", "wrong_answers", "hints", "fun_fact",
                    "needs_media", "background_query"]
            moved.append({**q, **{k: new[k] for k in keys if k in new},
                          "media": {**new["media"], "note": new["media"]["note"] or None},
                          "needs_fact_check": True, "revision_reason": rev["reason"]})
            counts["revise"] += 1
            applied.add(q["tmp_id"])
        if len(rest) != len(qs):
            f = d / "drafts" / f"{name}.json"
            save_json(f, {**load_json(f), "questions": rest})
    gone = {q["tmp_id"] for q in moved}
    for sub in ("ratings", "factchecks"):
        for f in (d / sub).glob("*.json"):
            data = load_json(f)
            if gone & data.keys():
                save_json(f, {k: v for k, v in data.items() if k not in gone})
    if moved:
        n = len(list((d / "drafts").glob("revised-*.json"))) + 1
        for i in range(0, len(moved), 10):
            save_json(d / "drafts" / f"revised-{n:02d}-{i // 10 + 1}.json", {"questions": moved[i:i + 10], "skipped": []})
    save_json(d / "applied.json", sorted(applied))
    print("applied: " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
          + ". Next: rate and factcheck (revised drafts only), then merge")


def count(items, key):
    out = {}
    for it in items:
        k = key(it); out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (0, kv[0], "") if isinstance(kv[0], int) else (1, 0, str(kv[0]))))


def report_subcategories(avail):
    """Supply per subcategory × difficulty (JK-10): where «Bájale» (an easier question of the same
    subcategory) and «Cambiazo» (a subcategory with a question in the level's range) run dry (09)."""
    by_sub = {}
    for q in avail:
        by_sub.setdefault(q.get("subcategory"), []).append(q["difficulty"])
    print("supply per subcategory × difficulty (JK-10; '.' = none):")
    print(f"  {'':34}" + "".join(f"{d:>3}" for d in range(1, 11)) + "  total")
    for c in categories.load():
        print(f"  {c['name']}")
        for sub in c["subcategories"]:
            ds = by_sub.get(sub, [])
            cells = "".join(f"{ds.count(d) or '.':>3}" for d in range(1, 11))
            print(f"    {sub[:32]:32}{cells}  {len(ds):5}{'  EMPTY' if not ds else ''}")
    empty = sum(1 for c in categories.load() for sub in c["subcategories"] if sub not in by_sub)
    easier = sum(1 for q in avail if any(d < q["difficulty"] for d in by_sub[q.get("subcategory")]))
    print(f"  empty subcategories: {empty}")
    print(f"  «Bájale» possible on {easier} of {len(avail)} questions "
          f"({easier * 100 // max(len(avail), 1)} %): an easier one exists in the same subcategory")
    print("  «Cambiazo» choices per level (subcategories with a question in the level's range):")
    for level in range(1, selection.LEVELS + 1):
        n = sum(1 for ds in by_sub.values() if any(selection.in_range({"difficulty": d}, level) for d in ds))
        lo, hi = selection.LEVEL_RANGES[level]
        print(f"    level {level:2} (difficulty {lo}–{hi}): {n:3}")


def cmd_report(args):
    pool = load_json(POOL)["questions"]
    broad = categories.broad_of()
    print(f"pool: {len(pool)} questions")
    for title, key in [("status", lambda q: q["status"]), ("difficulty", lambda q: q["difficulty"]),
                       ("category", lambda q: broad[q["subcategory"]]["slug"] if q.get("subcategory") in broad else None), ("style", lambda q: q.get("style")),
                       ("media", lambda q: f"{q['media']['type']}/{q['media']['role']}")]:
        print(f"  by {title}: {count(pool, key)}")
    try:
        burned = selection.burned_ids(args.player)
    except KeyError:
        sys.exit(f"unknown player: {args.player}")
    avail = selection.available(pool, burned)
    who = f"player {args.player}" if args.player else "a new player (global burns only)"
    print(f"unburned approved for {who}: {len(avail)} ({len(burned)} burned)")
    print(f"  by category: {count(avail, lambda q: broad[q['subcategory']]['slug'] if q.get('subcategory') in broad else None)}")
    print(f"  by difficulty: {count(avail, lambda q: q['difficulty'])}")
    print("supply per level (a game needs 4 per level, D-22):")
    for l in selection.supply(avail):
        lo, hi = l["range"]
        flag = f"  MISSING {l['missing']}" if l["missing"] else ""
        print(f"  level {l['level']:2} (difficulty {lo}–{hi}): {l['candidates']:3} candidates{flag}")
    if args.subcategories:
        report_subcategories(avail)
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


# --- the LLM batch (D-36, plans/19-repo-layout.md) ----------------------------------------------

BATCH_SUBCATEGORIES = 30  # per batch: the subcategories with the fewest approved questions
REVIEW_MODEL = "opus"

REVIEW_SCHEMA = {"type": "object", "required": ["decision", "feedback", "pick", "background_pick", "new_query", "reasons"],
    "properties": {"decision": {"type": "string", "enum": ["approved", "needs_work"]}, "feedback": STR,
                   "pick": {"type": ["integer", "null"]}, "background_pick": {"type": ["integer", "null"]},
                   "new_query": {"type": ["string", "null"]}, "reasons": STR}}


def batch_questions(run, statuses=("draft",)):
    """The pool's questions of this run that are still waiting for the given steps."""
    return [q for q in load_json(POOL)["questions"] if q.get("batch") == run and q["status"] in statuses]


def update_pool(changes):
    """Apply {qid: change(q)} to the source pool in one write."""
    data = load_json(POOL)
    for q in data["questions"]:
        if q["id"] in changes:
            changes[q["id"]](q)
    save_json(POOL, data)


def slots_of(q):
    return ["media"] + (["background"] if q.get("background") else [])


def sheet_path(d, qid, slot):
    return d / "sheets" / (f"{qid}.jpg" if slot == "media" else f"{qid}-background.jpg")


def cmd_media(args):
    """Fetch Commons candidates for every slot of the run's merged questions."""
    import media as media_tool  # authoring/tools/media.py
    errors = []
    for q in batch_questions(args.run):
        for slot in slots_of(q):
            if media_tool.load_candidates(q["id"], slot) is not None:
                continue
            try:
                data = media_tool.fetch_for(q, slot)
                print(f"  media: {q['id']} {slot}: {len(data['candidates'])} candidate(s)", flush=True)
            except Exception as e:  # noqa: BLE001 — rerun retries the rest
                errors.append(e)
                print(f"  FAILED media {q['id']} {slot}: {e}", file=sys.stderr)
    return errors


def cmd_sheets(args):
    """One contact sheet per slot (ImageMagick), for the review step to look at."""
    import media as media_tool
    d = run_dir(args)
    errors = []
    for q in batch_questions(args.run):
        for slot in slots_of(q):
            out = sheet_path(d, q["id"], slot)
            found = media_tool.load_candidates(q["id"], slot)
            if out.exists() or not found:
                continue
            try:
                thumbs = d / "sheets" / "thumbs" / out.stem
                shown = media_tool.make_sheet(found["candidates"], out, thumbs)
                print(f"  sheets: {out.name}: {len(shown)} picture(s)", flush=True)
            except Exception as e:  # noqa: BLE001
                errors.append(e)
                print(f"  FAILED sheet {out.name}: {e}", file=sys.stderr)
    return errors


def related_questions(q, pool):
    """Pool questions the review must compare with: same or similar answer, or same subcategory."""
    a = norm(q["answer"])
    out = []
    for p in pool:
        if p["id"] == q["id"] or p["status"] == "rejected":
            continue
        b = norm(p["answer"])
        if a == b or difflib.SequenceMatcher(None, a, b).ratio() >= 0.7 or p.get("subcategory") == q["subcategory"]:
            out.append({k: p[k] for k in ["id", "status", "subcategory", "question", "answer"]})
    return out[:30]


def slot_input(d, q, slot):
    import media as media_tool
    found = media_tool.load_candidates(q["id"], slot) or {"candidates": []}
    spec = q["media"] if slot == "media" else q["background"]
    sheet = sheet_path(d, q["id"], slot)
    return {"type": spec.get("type", "image"), "role": spec.get("role", "decorative"), "query": spec["query"],
            "note": spec.get("note"), "sheet": sheet.relative_to(d).as_posix() if sheet.exists() else None,
            "candidates": [{"number": i, "type": c["type"], "title": c["title"], "width": c["width"],
                            "height": c["height"], "duration": c["duration"], "author": c["author"],
                            "license": c["license"]} for i, c in enumerate(found["candidates"], 1)]}


def cmd_review(args):
    """The LLM review (D-32 criteria, prompts/review.md): one call per question.
    Round 1 reviews every merged question; round 2 only those whose media was searched again."""
    d = run_dir(args)
    reviews = d / "reviews"
    tmp_of = {v: k for k, v in load_json(d / "ids.json", {}).items()}
    ratings, checks = collect(d)
    pool = load_json(POOL)["questions"]
    system = prompt("house-style", "review")
    todo = []
    for q in batch_questions(args.run):
        r = load_json(reviews / f"{q['id']}.json", {})
        if args.round == 1 and "round1" not in r:
            todo.append((q, r))
        if args.round == 2 and r.get("researched") and "round2" not in r:
            todo.append((q, r))

    def work(item):
        q, r = item
        tmp = tmp_of.get(q["id"])
        payload = {
            "question": {k: q[k] for k in ["id", "subcategory", "difficulty", "description", "question", "answer",
                                           "wrong_answers", "hints", "fun_fact"]},
            "rater_notes": (ratings.get(tmp) or {}).get("notes") or (q.get("quality") or {}).get("notes"),
            "fact_check": ({k: checks[tmp][k] for k in ["verdict", "problem", "correction"]}
                           if tmp in checks else "not needed (no number, date or record)"),
            "related": related_questions(q, pool),
            "media": slot_input(d, q, "media"),
            "background": slot_input(d, q, "background") if q.get("background") else None,
            "can_search_again": args.round == 1,
        }
        user = "## Question to review\n" + json.dumps(payload, ensure_ascii=False, indent=2)
        out, model = claude(system, user, REVIEW_SCHEMA, args.model, d, read=True, with_model=True)
        r[f"round{args.round}"] = {**out, "model": model}
        save_json(reviews / f"{q['id']}.json", r)
        print(f"  review {args.round}: {q['id']}: {out['decision']}, pick {out['pick']}"
              + (f", new search “{out['new_query']}”" if out["new_query"] and args.round == 1 else ""), flush=True)

    return parallel(work, todo, args.jobs)


def cmd_research(args):
    """One new Commons search for questions whose round-1 review found no adequate media."""
    import media as media_tool
    d = run_dir(args)
    errors = []
    for q in batch_questions(args.run):
        path = d / "reviews" / f"{q['id']}.json"
        r = load_json(path, {})
        r1 = r.get("round1") or {}
        if r1.get("pick") is not None or not r1.get("new_query") or r.get("researched"):
            continue
        query = r1["new_query"].strip()
        try:
            q["media"]["query"] = query
            media_tool.fetch_for(q, "media")
        except Exception as e:  # noqa: BLE001
            errors.append(e)
            print(f"  FAILED research {q['id']}: {e}", file=sys.stderr)
            continue
        update_pool({q["id"]: lambda x, s=query: x["media"].update(query=s)})
        sheet_path(d, q["id"], "media").unlink(missing_ok=True)  # `sheets` builds the new one
        r["researched"] = query
        save_json(path, r)
        print(f"  research: {q['id']}: “{query}”", flush=True)
    return errors


def final_review(r):
    return r.get("round2") or r.get("round1")


def cmd_record(args):
    """Write the reviews (D-33: reviewer llm + model) and the picks into the pool. Fixed rules on
    top of the model's decision: no adequate media, or a fact check that isn't confirmed, means
    needs_work. Picks are recorded without downloading; `sync` fills the cache."""
    import media as media_tool
    d = run_dir(args)
    tmp_of = {v: k for k, v in load_json(d / "ids.json", {}).items()}
    _, checks = collect(d)
    today = datetime.date.today().isoformat()
    changes, missing = {}, []
    for q in batch_questions(args.run):
        r = final_review(load_json(d / "reviews" / f"{q['id']}.json", {}))
        if r is None:
            missing.append(q["id"])
            continue
        decision, problems, fields = r["decision"], [r["feedback"].strip()] if r["feedback"].strip() else [], {}
        for slot, key in [("media", "pick"), ("background", "background_pick")]:
            if slot not in slots_of(q):
                continue
            found = (media_tool.load_candidates(q["id"], slot) or {"candidates": []})["candidates"]
            n = r[key]
            if n is None or not 1 <= n <= len(found):
                decision = "needs_work"
                problems.append("Commons no tiene una imagen adecuada para esta pregunta." if slot == "media"
                                else "Commons no tiene una imagen de fondo adecuada.")
                continue
            fields[slot] = media_tool.pick_fields(found[n - 1], slot)
        check = checks.get(tmp_of.get(q["id"]))
        if check and check["verdict"] != "confirmed":
            decision = "needs_work"
            problems.append(f"Verificación de datos: {check['verdict']}. {check['problem']}".strip())
        if decision == "needs_work" and not problems:
            problems.append(r["reasons"])
        review = {"decision": decision, "feedback": " ".join(problems) if decision == "needs_work" else None,
                  "reviewed_on": today, "reviewer": "llm", "model": r["model"], "previous": None}

        def change(x, review=review, fields=fields):
            for slot, f in fields.items():
                x[slot].update(f)
            x.update(review=review, status=review["decision"])
        changes[q["id"]] = change
        print(f"  record: {q['id']}: {decision}", flush=True)
    update_pool(changes)
    if missing:
        print(f"  no review yet: {', '.join(missing)}", file=sys.stderr)
        return [RuntimeError(f"{len(missing)} question(s) without a review")]
    return []


def cmd_sync_run(args):
    """Download the run's picked files into the media cache. Rate limits don't fail the batch."""
    missing = []
    for q in batch_questions(args.run, ("approved", "needs_work")):
        for label, url in media.picked(q):
            if media.cache_path(url).is_file():
                continue
            try:
                media.cached(url)
            except Exception as e:  # noqa: BLE001 — listed in the report; `trivia-media sync` retries
                missing.append(label)
                print(f"  not cached: {label}: {e}", file=sys.stderr)
    save_json(run_dir(args) / "not-cached.json", missing)
    return []


def cmd_batch_report(args):
    """authoring/reports/<run>.md: what the batch produced, written by code."""
    d = run_dir(args)
    qs = [q for q in load_json(POOL)["questions"] if q.get("batch") == args.run]
    cfg = load_json(d / "run.json", {})
    dropped = load_json(d / "dropped.json", [])
    costs = [float(line.split("\t")[1]) for line in (d / "costs.log").read_text().splitlines()
             if line.count("\t") == 1 and line.split("\t")[1] not in ("None", "")] if (d / "costs.log").exists() else []
    models = sorted({(q.get("review") or {}).get("model") for q in qs} - {None})
    approved = [q for q in qs if q["status"] == "approved"]
    work = [q for q in qs if q["status"] == "needs_work"]
    not_cached = load_json(d / "not-cached.json", [])
    lines = [f"# {args.run}", "",
             f"Made by `qgen batch` on {datetime.date.today().isoformat()} (plans/19-repo-layout.md, D-36). "
             "Generated file: don't edit by hand.", "",
             f"- Subcategories ({len(cfg.get('subcategories', []))}): {', '.join(cfg.get('subcategories', []))}",
             f"- Merged: {len(qs)} ({qs[0]['id']}…{qs[-1]['id']})" if qs else "- Merged: 0",
             f"- Approved: {len(approved)}", f"- Needs work: {len(work)}",
             f"- Dropped by the pipeline: {len(dropped)}",
             f"- Reviewed by: {', '.join(models) or '-'}",
             f"- Claude calls: {len(costs)}, about ${sum(costs):.2f} at list price",
             f"- Picked files not cached yet: {len(not_cached)}" + (" (run `trivia-media sync --status approved`)" if not_cached else ""),
             "", "## Needs work", ""]
    lines += [f"- **{q['id']}** ({q['subcategory']}) {q['question']} → {q['answer']}: {q['review']['feedback']}" for q in work] or ["None."]
    lines += ["", "## Dropped by the pipeline", ""]
    lines += [f"- {x['tmp_id']}: {x['reason']}: {x['question']} → {x['answer']}" for x in dropped] or ["None."]
    out = layout.REPORTS / f"{args.run}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  report: {out.relative_to(ROOT)}")
    return []


def next_batch():
    """(run name, resuming?) — an unfinished `qgen batch` run is resumed; otherwise batch-<n+1>."""
    open_runs = sorted(p.parent.name for p in WORK.glob("*/run.json")
                       if (load_json(p) or {}).get("mode") == "batch" and not load_json(p).get("done"))
    if len(open_runs) > 1:
        sys.exit(f"More than one unfinished batch: {', '.join(open_runs)}. Ask the gamemaster which to finish.")
    if open_runs:
        return open_runs[0], True
    names = {q.get("batch") for q in load_json(POOL)["questions"]} | {p.name for p in WORK.iterdir() if p.is_dir()}
    numbers = [int(m.group(1)) for n in names if n and (m := re.fullmatch(r"batch-(\d+)", n))]
    return f"batch-{max(numbers, default=0) + 1}", False


def batch_subcategories(count):
    """The `count` subcategories with the fewest approved questions; ties in categories.json order."""
    approved = {}
    for q in load_json(POOL)["questions"]:
        if q["status"] == "approved":
            approved[q["subcategory"]] = approved.get(q["subcategory"], 0) + 1
    order = [s for c in categories.load() for s in c["subcategories"]]
    return sorted(order, key=lambda s: (approved.get(s, 0), order.index(s)))[:count]


def cmd_batch(args):
    """The whole pipeline in a fixed order (D-36). Rerunning it continues where it stopped."""
    if args.run:
        run, resuming = args.run, (WORK / args.run / "run.json").exists()
    else:
        run, resuming = next_batch()
    d = WORK / run
    if not resuming:
        if args.subcategories:
            subs = [s.strip() for s in args.subcategories.split(",") if s.strip()]
            unknown = [s for s in subs if s not in categories.broad_of()]
            if unknown:
                sys.exit(f"Not in app/data/categories.json: {', '.join(unknown)}")
        else:
            subs = batch_subcategories(args.count)
        save_json(d / "run.json", {"mode": "batch", "subcategories": subs,
                                   "started": datetime.date.today().isoformat()})
    print(f"{'Resuming' if resuming else 'Starting'} {run}", flush=True)

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    steps = [
        ("fit", cmd_fit, ns(model="opus", subcategories=None, max_styles=4)),
        ("draft", cmd_draft, ns(model="opus", seed=1)),
        ("rate", cmd_rate, ns(model="opus")),
        ("factcheck", cmd_factcheck, ns(model="sonnet")),
        ("revise", cmd_revise, ns(model="opus")),
        ("apply", cmd_apply, ns()),
        ("rate", cmd_rate, ns(model="opus")),
        ("factcheck", cmd_factcheck, ns(model="sonnet")),
        ("merge", cmd_merge, ns(min_score=0)),
        ("media", cmd_media, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 1", cmd_review, ns(model=REVIEW_MODEL, round=1)),
        ("research", cmd_research, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 2", cmd_review, ns(model=REVIEW_MODEL, round=2)),
        ("record", cmd_record, ns()),
        ("export", lambda a: cmd_export(a) or [], ns()),
        ("sync", cmd_sync_run, ns()),
        ("batch-report", cmd_batch_report, ns()),
    ]
    for name, fn, a in steps:
        print(f"== {name}", flush=True)
        errors = fn(a) or []
        if any(isinstance(e, UsageLimit) for e in errors):
            print(f"\nStopped at `{name}`: Claude's usage limit ({next(e for e in errors if isinstance(e, UsageLimit))}).\n"
                  "Wait for the reset, then run `qgen batch` again.", file=sys.stderr)
            sys.exit(75)
        if errors:
            print(f"\nStopped at `{name}` with {len(errors)} error(s). Run `qgen batch` again; "
                  "if the same step fails three times in a row, stop and report the output.", file=sys.stderr)
            sys.exit(1)
    errors, _ = validate_pool()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print("\n`qgen validate` failed. Stop and report the output.", file=sys.stderr)
        sys.exit(1)
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    qs = [q for q in load_json(POOL)["questions"] if q.get("batch") == run]
    n_ok = sum(q["status"] == "approved" for q in qs)
    print(f"\nDone: {run}: {len(qs)} merged, {n_ok} approved, {len(qs) - n_ok} needs work.")
    print("Commit exactly this:\n"
          f"  git add authoring/data/questions.json app/data/pool.json authoring/reports/{run}.md\n"
          f"  git commit -m \"{run}: {len(qs)} questions, {n_ok} approved (qgen batch)\"")


# --- export (D-35) --------------------------------------------------------------

def cmd_export(args):
    pool = load_json(POOL)
    layout.EXPORT.write_text(export_text(pool), encoding="utf-8")
    n = sum(q["status"] == "approved" for q in pool["questions"])
    print(f"exported {n} approved question(s) to {layout.EXPORT.relative_to(ROOT)}")


def validate_pool():
    """(errors, warnings) for the whole source pool and its export (QP-7)."""
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
        if rv is not None:  # who reviewed (D-33)
            if rv.get("reviewer") not in {"human", "llm"}: errors.append(f"{qid}: review.reviewer must be human or llm")
            if (rv.get("reviewer") == "llm") != bool(rv.get("model")): errors.append(f"{qid}: review.model must be set exactly for an llm review")
            prev = rv.get("previous")
            if prev is not None and (rv.get("reviewer") != "human" or prev.get("reviewer") != "llm"):
                errors.append(f"{qid}: review.previous must be an llm review under a human one")
        if q.get("subcategory") not in subcategories: errors.append(f"{qid}: subcategory not in app/data/categories.json (D-19)")
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
    exported = layout.EXPORT.read_text(encoding="utf-8") if layout.EXPORT.exists() else None
    if exported != export_text(data):
        errors.append(f"{layout.EXPORT.relative_to(ROOT)} is not the current export of the pool: run `qgen export`")
    return errors, warnings


def cmd_validate(args):
    errors, warnings = validate_pool()
    if warnings:
        print("\n".join(f"warning: {w}" for w in warnings))
        print(f"({len(warnings)} warning(s); `trivia-media sync --status approved` fills the cache)")
    print("\n".join(errors) or f"OK: {len(load_json(POOL)['questions'])} questions")
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
    rp = add("report", cmd_report, run=False)
    rp.add_argument("--run")
    rp.add_argument("--player", help="supply for this player (D-28); default: a new player")
    rp.add_argument("--subcategories", action="store_true",
                    help="supply per subcategory × difficulty, for the jokers (JK-10)")
    add("validate", cmd_validate, run=False)
    add("export", cmd_export, run=False)
    # the LLM batch (D-36): `batch` runs all of these in order; the others are for debugging
    add("media", cmd_media)
    add("sheets", cmd_sheets)
    add("review", cmd_review, REVIEW_MODEL).add_argument("--round", type=int, choices=[1, 2], default=1)
    add("research", cmd_research)
    add("record", cmd_record)
    add("sync", cmd_sync_run)
    add("batch-report", cmd_batch_report)
    b = sub.add_parser("batch", help="the whole pipeline for one new batch (authoring/RUNBOOK.md)")
    b.set_defaults(fn=cmd_batch)
    b.add_argument("--run", help=argparse.SUPPRESS)  # tests and debugging only
    b.add_argument("--subcategories", help=argparse.SUPPRESS)  # tests and debugging only
    b.add_argument("--count", type=int, default=BATCH_SUBCATEGORIES, help=argparse.SUPPRESS)
    b.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
