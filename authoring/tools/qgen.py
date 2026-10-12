#!/usr/bin/env python3
"""Question pipeline (plans/07-question-generation.md, D-10, D-36). Never ships (D-35).

An LLM makes a batch with exactly one command (authoring/RUNBOOK.md):

    qgen batch                      # writes base questions (D-41)
    qgen batch --bundle colombia    # only when the user names a bundle

It runs these steps in a fixed order; they stay available one by one for debugging:

    qgen concepts [--subcategories "Volcanes,Piratas"] [--top-up] [--fill]   # concept lists (D-37)
    qgen bundles                    # sort the pool into bundles (D-39)
    qgen bundle new <id> --name … --description … --kind region|theme --rule …   # an empty bundle (D-41)
    qgen draft --run <run> --subcategories "Volcanes,Piratas" [--bundle <id>]
    qgen draft | rate | factcheck | dedupe | revise | apply | merge --run <run>
    qgen media | sheets | review [--round 2] | fix | research | record | sync | batch-report --run <run>
    qgen audit [--batch <batch>]    # a second LLM reader of a seeded sample (plan 16); changes nothing
    qgen audit --backlog [--slice N] [--dry-run]   # the next slice of unaudited approved questions from before D-56 (plan 57)
    qgen rework [--batch <batch>] [--model fable]   # needs_work questions once more through fix and review (QG-23)
    qgen tighten                    # find long-winded questions in the whole pool, shorten and review them (QG-24)
    qgen export                     # app/data/pool.json from authoring/data/questions.json
    qgen report [--run <run>] [--player <name>] [--bundle <id>] [--subcategories] [--calibration [<batch>…]] [--overlaps] [--batches [<batch>…]]
    qgen report --qc [<batch> [--changes "<task ids>"]]   # spot check vs. LLM review and audit (plan 16)
    qgen validate

Writing steps call `claude -p --json-schema` with prompts from authoring/tools/prompts/. Work files
live in work/<run>/ and every step skips what is already done, so a run can be resumed.

Revising questions that are already in the pool (07, QG-13):

    qgen import --run <run> --batch <batch> [--assign-unbatched]
    qgen rate | factcheck | revise | apply --run <run>
"""
import argparse, concurrent.futures, datetime, difflib, json, random, re, subprocess, sys, threading, time, unicodedata
import urllib.parse
from pathlib import Path
from collections import Counter

import layout  # noqa: F401  (paths; also makes app/server importable, D-35)
from layout import PROMPTS, REPO as ROOT, SOURCE_POOL as POOL, WORK
import age_groups  # authoring/tools/age_groups.py: level ranges per group (plan 27)
import batches  # authoring/tools/batches.py: what the next batch does (D-36)
import concepts  # authoring/tools/concepts.py: concept lists and question axes (D-37)
import progress  # authoring/tools/progress.py: progress bars (QG-18)
import categories  # app/server/categories.py: every bundle's categories (D-19, D-43)
import media_cache as media  # app/server/media_cache.py: the media cache (D-17)
import providers  # authoring/tools/providers/: where candidates come from (D-45)
import selection  # app/server/selection.py: levels and the supply check (GF-5)
import save_file  # authoring/tools/save_file.py: the game's save, read-only (D-59)
import targets  # authoring/tools/targets.py: pool targets (D-53)
from pool_export import export_text  # authoring/tools/pool_export.py (D-35)

# Target share per difficulty level (07, "Difficulty target", D-31): what the 12 levels'
# ranges (D-22) show per game, times 3. These are the focus group's (young teens, window 1–10,
# D-38); drafting stops if the focus group's window changes without new weights (AG-8).
# Without a focus, every level of the scale weighs the same (D-40).
LEVEL_WEIGHTS = {1: 12, 2: 6, 3: 10, 4: 16, 5: 20, 6: 23, 7: 14, 8: 14, 9: 16, 10: 13}
RUBRIC = ["correct", "unambiguous", "no_giveaway", "no_overlap", "distractors", "age_fit", "fun", "description"]
# Below 4 on any of these drops a question (07). The soft scores didn't predict the
# gamemaster's decisions in the pilot, so they are recorded but don't filter by default.
# no_overlap (plan 15): asks a fact the pool or an earlier draft already asks; dropped, not revised.
HARD_CRITERIA = ["correct", "unambiguous", "no_giveaway", "no_overlap"]
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

def load_age_groups():
    return load_json(layout.AGE_GROUPS)


def focus_group():
    """The age group the pipeline writes for (D-38); None writes across the whole scale (D-40)."""
    ag = load_age_groups()
    return next((g for g in ag["groups"] if g["id"] == ag["focus"]), None) if ag["focus"] else None


def ages_text(g):
    lo, hi = g["ages"]
    return f"{lo}–{hi}" if hi else f"{lo}+"


def load_bundles():
    return load_json(layout.BUNDLES)["bundles"]


def bundles_text():
    """The bundles and their membership rules, for prompts (D-39)."""
    return "\n".join(f"- `{b['id']}`: {b['rule']}" for b in load_bundles())


def bundle_text(bundle):
    """The one bundle a batch writes for, as a content limit for the drafter (D-41)."""
    rule = next(b["rule"] for b in load_bundles() if b["id"] == bundle)
    return f"Every question you write is in the `{bundle}` bundle: {rule}"


def check_bundle(bundle):
    """Exit unless the bundle is in app/data/bundles.json and has subcategories."""
    if bundle not in {b["id"] for b in load_bundles()}:
        sys.exit(f"Unknown bundle {bundle!r}: not in app/data/bundles.json")
    if not categories.subcategories(bundle):
        sys.exit(f"Bundle {bundle!r} has no subcategories yet: fill {categories.path(bundle).relative_to(ROOT)}")


def not_in_bundle(subs, bundle=None):
    """The subcategories that aren't in the bundle's categories (any bundle's when None)."""
    known = set(categories.subcategories(bundle))
    return [s for s in subs if s not in known]


def prompt(*names):
    """Prompt files joined; {age_groups} and {players} are filled from app/data/age-groups.json."""
    ag, focus = load_age_groups(), focus_group()
    groups = [f"{g['id'].replace('_', ' ')} ({ages_text(g)})" for g in ag["groups"]]
    if focus:
        lo, hi = focus["window"]
        players = (f"**Focus group:** {focus['id'].replace('_', ' ')}, ages {ages_text(focus)}, who play "
                   f"difficulties {lo}–{hi}. Write for these players: their knowledge, their world, their humour. "
                   '"The players" below means them.')
    else:
        lo, hi = ag["scale"]
        windows = ", ".join(f"{g['id'].replace('_', ' ')} {g['window'][0]}–{g['window'][1]}" for g in ag["groups"])
        players = (f"**No focus group:** questions span the whole scale {lo}–{hi}. Each question is for the groups "
                   f"whose window contains its difficulty ({windows}). Write for those players: their knowledge, "
                   'their world, their humour. "The players" below means them, for the question at hand.')
    text = "\n\n".join((PROMPTS / f"{n}.md").read_text(encoding="utf-8") for n in names)
    return (text.replace("{age_groups}", ", ".join(groups[:-1]) + " and " + groups[-1])
            .replace("{players}", players))

def run_dir(args):
    d = WORK / args.run
    d.mkdir(parents=True, exist_ok=True)
    return d

def parallel(fn, items, jobs, label="items", unit="items"):
    """Run fn over items with a progress bar; report failures without stopping the others.
    Claude's usage limit stops the whole step instead, reported once. Returns the errors."""
    errors, items, limit = [], list(items), []

    def run(it):
        bar.started()
        return fn(it)

    def name(x):
        return str(x.get("id")) if isinstance(x, dict) else str(x)

    with progress.Bar(label, len(items), unit) as bar, concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futures = {ex.submit(run, it): it for it in items}
        for f in concurrent.futures.as_completed(futures):
            if f.cancelled():
                continue
            try:
                f.result()
                bar.finished()
            except UsageLimit as e:
                bar.finished(ok=False)
                if not limit:  # the first one stops the rest; the others say the same thing
                    limit.append(e)
                    for other in futures:
                        other.cancel()
            except Exception as e:  # noqa: BLE001 — keep the batch going
                bar.finished(ok=False)
                errors.append(e)
                it = futures[f]
                label = (name(it[0]) if isinstance(it, tuple)  # list: grouped() files or a group of questions
                         else ", ".join(name(x[0] if isinstance(x, tuple) else x) for x in it)
                         if isinstance(it, list) else name(it))
                print(f"  FAILED {label}: {e}", file=sys.stderr)
    if limit:  # the caller reports it (main, cmd_batch)
        return errors + limit
    if errors:
        print(f"{len(errors)} item(s) failed; rerun the same command to retry them.", file=sys.stderr)
    return errors


class UsageLimit(RuntimeError):
    """Claude reported a usage or session limit: wait for the reset, then rerun."""


LIMIT_WORDS = ("usage limit", "session limit", "rate limit", "hit your limit")
# "resets 11pm (America/Bogota)", "resets 11:30pm", "resets Oct 9, 3am (Europe/Berlin)"
RESET_RE = re.compile(r"resets\s+(?:(?P<mon>[a-z]{3})[a-z]*\.?\s+(?P<day>\d{1,2}),?\s+(?:at\s+)?)?"
                      r"(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s*(?P<ap>[ap]\.?m\.?)?(?:\s*\((?P<tz>[^)]+)\))?", re.I)
LIMIT_MARGIN = datetime.timedelta(minutes=5)  # resume this long after the reset (QG-21)


def limit_reset(msg, now=None):
    """When Claude's usage limit in `msg` resets (an aware datetime), or None if it doesn't say."""
    m = RESET_RE.search(str(msg))
    if not m:
        return None
    tz = None
    if m["tz"]:
        try:
            import zoneinfo
            tz = zoneinfo.ZoneInfo(m["tz"].strip())
        except Exception:  # noqa: BLE001 — unknown zone or no tz data: assume local time
            tz = None
    tz = tz or datetime.datetime.now().astimezone().tzinfo
    now = (now or datetime.datetime.now(datetime.timezone.utc)).astimezone(tz)
    hour, minute = int(m["h"]), int(m["m"] or 0)
    if m["ap"]:
        hour = hour % 12 + (12 if m["ap"][0].lower() == "p" else 0)
    if hour > 23 or minute > 59:
        return None
    try:
        if m["mon"]:
            month = datetime.datetime.strptime(m["mon"][:3].title(), "%b").month
            reset = now.replace(month=month, day=int(m["day"]), hour=hour, minute=minute, second=0, microsecond=0)
            if reset < now - datetime.timedelta(days=1):  # "resets Jan 2" said in December
                reset = reset.replace(year=now.year + 1)
        else:
            reset = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if reset < now - datetime.timedelta(hours=1):  # "resets 2am" said in the evening
                reset += datetime.timedelta(days=1)
    except ValueError:
        return None
    return reset


def wait_for_reset(limit, again="qgen batch"):
    """Sleep until LIMIT_MARGIN after the reset that `limit` names (at least LIMIT_MARGIN).
    Returns False, without waiting, when the message has no reset time (QG-21)."""
    reset = limit_reset(limit)
    if reset is None:
        return False
    until = max(reset + LIMIT_MARGIN, datetime.datetime.now(reset.tzinfo) + LIMIT_MARGIN)
    left = (until - datetime.datetime.now(until.tzinfo)).total_seconds()
    print(f"\nClaude's usage limit ({limit}).\nWaiting until {until:%Y-%m-%d %H:%M} {until.tzname()} "
          f"({progress.duration(left)}), then continuing. Ctrl-C stops; `{again}` continues later.",
          file=sys.stderr, flush=True)
    while (left := (until - datetime.datetime.now(until.tzinfo)).total_seconds()) > 0:
        time.sleep(min(left, 60))  # the wall clock, so a suspended laptop still wakes up on time
    return True


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
    for attempt in range(retries + 1):
        with progress.waiting(f"claude {model}" + (f" (retry {attempt})" if attempt else "")):
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

MEDIA_SCHEMA = {"type": "object", "required": ["type", "role", "query", "note"], "properties": {
    "type": {"type": "string", "enum": ["image", "audio", "video"]},
    "role": {"type": "string", "enum": ["decorative", "illustrative", "essential"]},
    "query": STR, "note": STR}}

QUESTION_SCHEMA = {"type": "object", "required": [
    "slot", "option", "difficulty", "description", "question", "answer", "wrong_answers", "hints",
    "media", "fun_fact", "needs_media", "needs_fact_check", "background_query"], "properties": {
    "slot": INT, "option": INT, "difficulty": INT, "description": STR, "question": STR, "answer": STR,
    "wrong_answers": STR_LIST, "hints": STR_LIST, "media": MEDIA_SCHEMA, "fun_fact": STR,
    "needs_media": {"type": "boolean"}, "needs_fact_check": {"type": "boolean"}, "background_query": STR}}

DRAFT_SCHEMA = {"type": "object", "required": ["questions", "skipped"], "properties": {
    "questions": {"type": "array", "items": QUESTION_SCHEMA},
    "skipped": {"type": "array", "items": {"type": "object", "required": ["slot", "reason", "retire"],
                "properties": {"slot": INT, "reason": STR,
                               "retire": {"type": "string", "enum": ["no", "used_up", "unaskable"]}}}}}}

RATE_SCHEMA = {"type": "object", "required": ["ratings"], "properties": {"ratings": {
    "type": "array", "items": {"type": "object",
        "required": ["id", *RUBRIC, "overlap_with", "difficulty_estimate", "notes"],
        "properties": {"id": STR, **{k: INT for k in RUBRIC}, "overlap_with": STR,
                       "difficulty_estimate": INT, "notes": STR}}}}}

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

CONCEPT_ITEM = {"type": "object", "required": ["name", "facet", "known_at"],
                "properties": {"name": STR, "facet": STR, "known_at": INT}}
TOPUP_SCHEMA = {"type": "object", "required": ["new_facets", "concepts"], "properties": {
    "new_facets": STR_LIST, "concepts": {"type": "array", "items": CONCEPT_ITEM}}}


def axes_schema(axes_def):
    return {"type": "object", "required": concepts.AXES, "properties": {
        a: {"type": "string", "enum": concepts.values(axes_def, a)} for a in concepts.AXES}}


def facets_schema(axes_def):
    fit = {a: {"type": "object", "required": concepts.values(axes_def, a),
               "properties": {v: INT for v in concepts.values(axes_def, a)}} for a in concepts.FIT_AXES}
    return {"type": "object", "required": ["facets", "axis_fit"], "properties": {
        "facets": STR_LIST, "axis_fit": {"type": "object", "required": concepts.FIT_AXES, "properties": fit}}}


def list_schema(axes_def):
    return {"type": "object", "required": ["concepts", "existing"], "properties": {
        "concepts": {"type": "array", "items": CONCEPT_ITEM},
        "existing": {"type": "array", "items": {"type": "object", "required": ["id", "concept", "axes"],
                     "properties": {"id": STR, "concept": STR, "axes": axes_schema(axes_def)}}}}}


def subcategory_header(sub):
    return f"## Subcategory\n{sub} (broad category: {categories.broad_of()[sub]['name']})"


def cmd_concepts(args):
    """Concept lists (PE-8, D-37): facets and axis fit, then concepts and the concept and axes of
    every existing question; `--top-up` adds concepts to lists running low. Calls run in parallel
    and save raw results in work/concepts/; `finalize_concepts` then writes the lists one by one."""
    d = WORK / "concepts"
    d.mkdir(parents=True, exist_ok=True)
    if args.subcategories:
        subs = [s.strip() for s in args.subcategories.split(",") if s.strip()]
    elif getattr(args, "run", None):
        subs = load_json(WORK / args.run / "run.json")["subcategories"]
    else:
        subs = categories.subcategories(getattr(args, "bundle", None))
    unknown = not_in_bundle(subs)
    if unknown:
        sys.exit(f"Not in any bundle's categories: {', '.join(unknown)}")
    pool = load_json(POOL)["questions"]
    create = [s for s in subs if concepts.load(s) is None]

    def make(sub):
        path = d / "raw" / f"{slug(sub)}.json"
        r = load_json(path, {})
        axes_def = concepts.load_axes(categories.bundle_of(sub))
        intro = subcategory_header(sub) + "\n\n## Question axes\n" + concepts.axes_text(axes_def)
        if "facets" not in r:
            r.update(claude(prompt("house-style", "concepts-facets"), intro, facets_schema(axes_def), args.model, d))
            save_json(path, r)
        if "concepts" not in r:
            existing = [{"id": q["id"], "question": q["question"], "answer": q["answer"],
                         "media": f"{q['media']['type']}/{q['media']['role']}"}
                        for q in pool if q.get("subcategory") == sub]
            user = (intro + "\n\n## Facets\n" + "\n".join(f"- {f}" for f in r["facets"])
                    + "\n\n## Existing questions\n" + (json.dumps(existing, ensure_ascii=False) if existing else "none"))
            out = claude(prompt("house-style", "concepts-list"), user, list_schema(axes_def), args.model, d)
            missing = {q["id"] for q in existing} - {e["id"] for e in out["existing"]}
            if missing:  # untagged questions would make their concepts look unused
                raise RuntimeError(f"{sub}: no concept for {', '.join(sorted(missing))}")
            r.update(out)
            save_json(path, r)
        progress.detail(f"  concepts: {sub}: {len(r['facets'])} facets, {len(r['concepts'])} concepts")

    def wanted(sub):
        """How many concepts a top-up asks for: up to TARGET_SIZE with --fill, else TOP_UP when low."""
        lst = concepts.load(sub)
        if getattr(args, "fill", False) and len(lst["concepts"]) < concepts.TARGET_SIZE:
            return concepts.TARGET_SIZE - len(lst["concepts"])
        if args.top_up and len(concepts.unused(lst, concepts.uses(pool, sub))) < concepts.LOW_STOCK:
            return concepts.TOP_UP
        return 0

    def top_up(sub):
        path = d / "topup" / f"{slug(sub)}.json"
        if path.exists():
            return
        lst = concepts.load(sub)
        user = (subcategory_header(sub) + f"\n\n## How many\nAdd about {wanted(sub)} new concepts."
                + "\n\n## Facets\n" + "\n".join(f"- {f}" for f in lst["facets"])
                + "\n\n## Concepts already in the list\n" + "\n".join(f"- {c['name']} ({c['facet']})" for c in lst["concepts"]))
        out = claude(prompt("house-style", "concepts-topup"), user, TOPUP_SCHEMA, args.model, d)
        save_json(path, out)
        progress.detail(f"  top-up: {sub}: {len(out['concepts'])} new concepts")

    bundles = sorted({categories.bundle_of(s) for s in subs}, key=categories.bundle_ids().index)
    errors = parallel(make, create, args.jobs, "concepts", "lists")
    for b in bundles:
        finalize_concepts(d, b)
    errors += parallel(top_up, [s for s in subs if concepts.load(s) and wanted(s)], args.jobs, "top-up", "lists")
    for b in bundles:
        finalize_concepts(d, b)
    return errors


def finalize_concepts(d, bundle):
    """Write the bundle's finished raw results and top-ups into its concept folder, one subcategory
    at a time in its categories.json order, so no normalized name is in two of the bundle's lists
    (OQ-40, D-43), except where a question of the later subcategory already uses it. Tags existing
    questions in the pool."""
    order, axes_def = categories.subcategories(bundle), concepts.load_axes(bundle)
    lo, hi = load_age_groups()["scale"]
    seen = {}
    for s in order:
        lst = concepts.load(s)
        for c in (lst or {}).get("concepts", []):
            seen.setdefault(concepts.key(c["name"]), s)
    data, tagged = load_json(POOL), 0
    by_id = {q["id"]: q for q in data["questions"]}
    for s in order:
        raw, topup = load_json(d / "raw" / f"{slug(s)}.json", {}), d / "topup" / f"{slug(s)}.json"
        lst, before = concepts.load(s), None
        if lst is None and "concepts" in raw:
            lst = {"subcategory": s, "facets": raw["facets"], "axis_fit": raw["axis_fit"], "concepts": []}
            tags = raw["existing"]
            items = raw["concepts"] + [{"name": e["concept"], "facet": "Otros", "known_at": by_id[e["id"]]["difficulty"]}
                                       for e in tags if e["id"] in by_id]  # a question's level stands in for the concept's
        elif lst is not None and topup.exists():
            extra = load_json(topup)
            lst["facets"] += [f for f in extra["new_facets"] if f not in lst["facets"]]
            tags, items, before = [], extra["concepts"], len(lst["concepts"])
        else:
            continue
        used = {concepts.key(e["concept"]) for e in tags}
        own = {concepts.key(c["name"]): c["name"] for c in lst["concepts"]}
        shared = []
        for c in items:
            k = concepts.key(c["name"])
            if not k or k in own:
                continue
            if seen.get(k, s) != s and k not in used:
                shared.append(c["name"])
                continue
            if c["facet"] not in lst["facets"]:
                lst["facets"].append(c["facet"])
            lst["concepts"].append({"name": c["name"].strip(), "facet": c["facet"],
                                    "known_at": min(hi, max(lo, c["known_at"]))})
            own[k] = c["name"].strip()
            seen.setdefault(k, s)
        if before is not None:  # for the saturation check (plan 14)
            lst.setdefault("top_ups", []).append({"date": datetime.date.today().isoformat(),
                                                  "added": len(lst["concepts"]) - before,
                                                  "unused": len(concepts.unused(lst, concepts.uses(data["questions"], s)))})
        for e in tags:
            q = by_id.get(e["id"])
            if q is None or q.get("subcategory") != s:
                continue
            q["concept"] = own[concepts.key(e["concept"])]
            if not concepts.axes_problems(e["axes"], axes_def)[0]:
                q["axes"] = e["axes"]
            tagged += 1
        concepts.save(s, lst)
        topup.unlink(missing_ok=True)
        progress.detail(f"  list: {s}: {len(lst['concepts'])} concepts"
                        + (f"; dropped {len(shared)} already in another list: {', '.join(shared)}" if shared else ""))
    if tagged:
        save_json(POOL, data)
        print(f"  tagged {tagged} pool question(s) with a concept and axes")


BUNDLE_SCHEMA = {"type": "object", "required": ["questions"], "properties": {"questions": {
    "type": "array", "items": {"type": "object", "required": ["id", "bundle", "reason"],
                               "properties": {"id": STR, "bundle": STR, "reason": STR}}}}}
BUNDLE_GROUP = 20  # questions per `qgen bundles` call


def cmd_bundles(args):
    """Sort the existing pool into bundles (BN-3, D-39). Questions without `bundle` get `base`;
    then an LLM pass proposes a bundle for every question it hasn't seen yet, and the proposals
    are written into the pool. Proposals stay in work/bundles/proposals.json, so a rerun only
    sends new questions and never overwrites a bundle the gamemaster changed afterwards."""
    d = WORK / "bundles"
    d.mkdir(parents=True, exist_ok=True)
    data = load_json(POOL)
    missing = [q for q in data["questions"] if not q.get("bundle")]
    for q in missing:
        q["bundle"] = "base"
    if missing:
        save_json(POOL, data)
        print(f"  {len(missing)} question(s) without a bundle set to base")
    ids = {b["id"] for b in load_bundles()}
    proposals = load_json(d / "proposals.json", {})
    todo = [q for q in data["questions"] if q["id"] not in proposals and q["status"] != "rejected"]
    system = prompt("house-style", "bundles")
    lock = threading.Lock()

    def work(group):
        items = [{k: q[k] for k in ["id", "subcategory", "question", "answer", "wrong_answers", "hints"]} for q in group]
        user = "## Bundles\n" + bundles_text() + "\n\n## Questions\n" + json.dumps(items, ensure_ascii=False)
        out = claude(system, user, BUNDLE_SCHEMA, args.model, d)
        got = {r["id"]: r for r in out["questions"] if r["bundle"] in ids}
        missing = [q["id"] for q in group if q["id"] not in got]
        with lock:
            proposals.update({i: {"bundle": got[i]["bundle"], "reason": got[i]["reason"], "applied": False}
                              for i in got if i in {q["id"] for q in group}})
            save_json(d / "proposals.json", proposals)
        print(f"  bundles: {group[0]['id']}…{group[-1]['id']}: "
              + ", ".join(f"{b} {sum(1 for i in got if got[i]['bundle'] == b)}" for b in sorted(ids)), flush=True)
        if missing:
            raise RuntimeError(f"no bundle for {', '.join(missing)}")

    errors = parallel(work, [todo[i:i + BUNDLE_GROUP] for i in range(0, len(todo), BUNDLE_GROUP)],
                      args.jobs, "bundles", "calls")
    data = load_json(POOL)  # proposals go in once, in one write
    moved = []
    for q in data["questions"]:
        p = proposals.get(q["id"])
        if p and not p["applied"]:
            if q["bundle"] != p["bundle"]:
                moved.append(f"{q['id']} → {p['bundle']}: {q['question'][:70]} ({p['reason']})")
            q["bundle"], p["applied"] = p["bundle"], True
    save_json(POOL, data)
    save_json(d / "proposals.json", proposals)
    cmd_export(args)
    print("\n".join(f"  {m}" for m in moved))
    print(f"{len(moved)} question(s) moved out of base; check them at /review?bundle=<id> (trivia-authoring)")
    return errors


def target_weights(pool_questions, bundle):
    """{difficulty: weight} for drafting: LEVEL_WEIGHTS for the focus group; without one the
    bundle's deficits vs. its targets (D-54), even over the scale without targets or deficits (D-40)."""
    focus = focus_group()
    if focus is None:
        lo, hi = load_age_groups()["scale"]
        deficit = targets.deficits(pool_questions, bundle)
        if deficit:
            return {lvl: deficit.get(lvl, 0) for lvl in range(lo, hi + 1)}
        return {lvl: 1 for lvl in range(lo, hi + 1)}
    lo, hi = focus["window"]
    if sorted(LEVEL_WEIGHTS) != list(range(lo, hi + 1)):  # AG-8: weights per group
        sys.exit(f"LEVEL_WEIGHTS cover {min(LEVEL_WEIGHTS)}–{max(LEVEL_WEIGHTS)}, "
                 f"but the focus group's window is {lo}–{hi} (app/data/age-groups.json)")
    return LEVEL_WEIGHTS


def level_counts(n, weights):
    """How many of n slots get each level, in proportion to the weights."""
    total = sum(weights.values())
    exact = {lvl: n * w / total for lvl, w in weights.items()}
    counts = {lvl: int(x) for lvl, x in exact.items()}
    for lvl in sorted(exact, key=lambda l: exact[l] - counts[l], reverse=True)[:n - sum(counts.values())]:
        counts[lvl] += 1
    return counts


def assign_difficulties(free, fresh, weights, seed, rounds=50):
    """{subcategory: [target levels]}: `free` slots each, levels per `weights`, each level to the
    subcategories whose unused concepts (`fresh`: their known_at values) carry it (D-54): the
    concepts within ±1 per subcategory and level, scaled to both totals (iterative proportional
    fitting), then rounded slot by slot. A level no list carries goes by distance. Seeded; scarce
    levels come first in each list."""
    rng = random.Random(seed)
    counts = level_counts(sum(free.values()), weights)
    fit = {s: {lvl: sum(abs(k - lvl) <= 1 for k in fresh[s]) for lvl in counts} for s in free}
    for lvl in counts:
        if counts[lvl] and not any(fit[s][lvl] for s in free):
            for s in free:
                fit[s][lvl] = 1 / (1 + min((abs(k - lvl) for k in fresh[s]), default=99))
    for _ in range(rounds):
        for lvl in counts:
            col = sum(fit[s][lvl] for s in free)
            for s in free:
                fit[s][lvl] *= counts[lvl] / col if col else 0
        for s in free:
            row = sum(fit[s].values())
            for lvl in counts:
                fit[s][lvl] *= free[s] / row if row else 0
    supply = {lvl: sum(fit[s][lvl] > 0 for s in free) for lvl in counts}
    order = sorted(((i + 0.5) / c, supply[lvl], lvl) for lvl, c in counts.items() for i in range(c))
    out, left = {s: [] for s in free}, dict(free)
    for *_, lvl in order:
        s = max((s for s in left if left[s]), key=lambda s: (fit[s][lvl] - out[s].count(lvl), rng.random()))
        out[s].append(lvl)
        left[s] -= 1
    for levels in out.values():
        levels.sort(key=lambda l: supply[l])
    return out


def draw_slots(subs, pool_questions, axes_def, n, seed, bundle="base"):
    """{subcategory: slots} for a run (PE-10): a concept, a target difficulty, up to 3 axis
    combinations and the questions already asked about the concept, per slot. Seeded."""
    lists = {s: concepts.load(s) for s in subs}
    used = {s: concepts.uses(pool_questions, s) for s in subs}
    levels = assign_difficulties({s: n for s in subs},
                                 {s: [c["known_at"] for c in concepts.unused(lists[s], used[s])] for s in subs},
                                 target_weights(pool_questions, bundle), seed)
    plan = {}
    for s in subs:
        rng = random.Random(f"{seed}:{s}")
        lst = lists[s]
        picked = concepts.draw_concepts(lst, used[s], levels[s], rng)  # scarce levels pick first
        pairs = list(zip(picked, levels[s]))
        rng.shuffle(pairs)
        usage = concepts.axis_usage(pool_questions, s)
        offered = {a: set() for a in concepts.AXES}
        possible = concepts.possible_combos(axes_def, lst.get("axis_fit", {}))
        if not possible:
            print(f"  {s}: no axis combination fits (see axis_fit in its concept list); no slots", file=sys.stderr)
        slots = []
        for c, target in pairs:
            combos = concepts.draw_combos(axes_def, lst.get("axis_fit", {}), usage, offered, rng,
                                          possible=possible)
            if not combos:
                continue
            asked = [f"{q['question']} → {q['answer']}" for q in pool_questions
                     if q.get("subcategory") == s and q.get("concept") == c["name"]]
            slots.append({"slot": len(slots), "concept": c["name"], "facet": c["facet"], "target_difficulty": target,
                          "options": [{"option": i, **combo} for i, combo in enumerate(combos, 1)],
                          "already_asked": asked})
        plan[s] = slots
    return plan


def existing_answers(pool, sub):
    """The subcategory's own pool questions, all statuses (PE-4); merge's `duplicates()` and the
    review's `related` list still check the whole pool."""
    return sorted({f"{q['answer']} ({q['question'][:60]})" for q in pool["questions"] if q.get("subcategory") == sub})


def cmd_draft(args):
    d = run_dir(args)
    cfg = load_json(d / "run.json")
    if cfg is None:
        if not args.subcategories:
            sys.exit("First call for a run needs --subcategories.")
        check_bundle(args.bundle)
        cfg = {"bundle": args.bundle, "subcategories": [s.strip() for s in args.subcategories.split(",") if s.strip()]}
        unknown = not_in_bundle(cfg["subcategories"], args.bundle)
        if unknown:
            sys.exit(f"Not in {categories.path(args.bundle).relative_to(ROOT)} (add them there first): {', '.join(unknown)}")
        save_json(d / "run.json", cfg)
    subs, bundle = cfg["subcategories"], cfg.get("bundle", "base")  # runs before D-41 have no bundle
    missing = [s for s in subs if concepts.load(s) is None]
    if missing:
        sys.exit(f"No concept list for {', '.join(missing)}: run `qgen concepts --subcategories ...` first.")
    pool = load_json(POOL)
    axes_def = concepts.load_axes(bundle)
    plan = load_json(d / "slots.json")
    if plan is None:  # drawn once, so a rerun drafts the same slots
        plan = draw_slots(subs, pool["questions"], axes_def, args.slots, args.seed, bundle)
        save_json(d / "slots.json", plan)
    drawn = Counter(sl["target_difficulty"] for slots in plan.values() for sl in slots)
    print("target difficulty: " + "  ".join(f"{lvl}×{c}" for lvl, c in sorted(drawn.items())), flush=True)
    system = prompt("house-style", "draft")
    todo = [s for s in subs if plan.get(s) and not (d / "drafts" / f"{slug(s)}.json").exists()]

    def work(sub):
        slots = plan[sub]
        shown = {a: {o[a] for sl in slots for o in sl["options"]} for a in concepts.AXES}
        avoid = "\n".join(f"- {a}" for a in existing_answers(pool, sub)) or "none yet"
        user = (subcategory_header(sub) + "\n\n## Question axes (the values in these options)\n"
                + concepts.axes_text(axes_def, shown) + "\n\n## Slots\n" + json.dumps(slots, ensure_ascii=False)
                + f"\n\n## Already in the pool for this subcategory (don't repeat these facts)\n{avoid}"
                + "\n\n## Bundle\n" + bundle_text(bundle))
        out = claude(system, user, DRAFT_SCHEMA, args.model, d)
        good = []
        for q in out["questions"]:
            problems = check_question_shape(q)
            if not 0 <= q["slot"] < len(slots):
                problems.append(f"unknown slot {q['slot']}")
            elif not 1 <= q["option"] <= len(slots[q["slot"]]["options"]):
                problems.append(f"unknown option {q['option']}")
            if problems:
                print(f"  {sub}: dropped malformed question ({'; '.join(problems)})", file=sys.stderr)
                continue
            sl = slots[q["slot"]]
            option = {k: v for k, v in sl["options"][q.pop("option") - 1].items() if k != "option"}
            q.update(style=None, axes=option, concept=sl["concept"], tmp_id=f"{slug(sub)}-{q['slot']}", subcategory=sub,
                     bundle=bundle)
            q["media"]["note"] = q["media"]["note"] or None
            if (option["stimulus"] != "none") != (q["media"]["role"] == "essential"):
                print(f"  {sub}: {q['tmp_id']}: stimulus {option['stimulus']} with {q['media']['role']} media "
                      "(left for rate and review)", file=sys.stderr)
            good.append(q)
        retire(sub, slots, out["skipped"])
        save_json(d / "drafts" / f"{slug(sub)}.json", {"questions": good, "skipped": out["skipped"]})
        progress.detail(f"  draft: {sub}: {len(good)} written, {len(out['skipped'])} skipped")

    return parallel(work, todo, args.jobs, "draft", "subcategories")


def retire(sub, slots, skipped):
    """Skips that say a concept is used up or unaskable retire it from its list (PE-10)."""
    why = {slots[x["slot"]]["concept"]: f"{x['retire']}: {x['reason']}" for x in skipped
           if x["retire"] != "no" and 0 <= x["slot"] < len(slots)}
    if not why:
        return
    lst = concepts.load(sub)
    for c in lst["concepts"]:
        if c["name"] in why:
            c["retired"] = why[c["name"]]
    concepts.save(sub, lst)
    progress.detail(f"  {sub}: retired {', '.join(why)}")


def check_question_shape(q):
    problems = []
    if len(q["wrong_answers"]) != 3: problems.append("needs 3 wrong answers")
    if len(q["hints"]) != 3: problems.append("needs 3 hints")
    lo, hi = load_age_groups()["scale"]
    if not lo <= q["difficulty"] <= hi: problems.append("difficulty out of range")
    if len({norm(o) for o in [q["answer"], *q["wrong_answers"]]}) != 4: problems.append("duplicate options")
    return problems


def drafts(d):
    for f in sorted((d / "drafts").glob("*.json")):
        yield f.stem, load_json(f)["questions"]


GROUP_SIZE = 10  # questions per rate/revise call (PE-1, PE-2)


def grouped(files, size=GROUP_SIZE):
    """Pack (name, items) draft files into groups of about `size` items, one call each.
    A file is never split (a draft file is one subcategory); a bigger file is a group of its own."""
    groups, cur, n = [], [], 0
    for name, items in files:
        if cur and n + len(items) > size:
            groups.append(cur)
            cur, n = [], 0
        cur.append((name, items))
        n += len(items)
    return groups + [cur] if cur else groups


def for_review(q):
    keys = ["difficulty", "description", "question", "answer", "wrong_answers", "hints", "media", "fun_fact"]
    form = {"axes": q["axes"]} if q.get("axes") else {"style": q.get("style")}  # older drafts have a style
    return {"id": q["tmp_id"], **form, **{k: q[k] for k in keys}}


def rate_candidates(d):
    """tmp_id → overlap candidates for `rate` (plan 15): pool questions of every bundle (not rejected)
    and earlier drafts of the run; revised drafts count as later than the first round."""
    others = [q for q in load_json(POOL)["questions"] if q["status"] != "rejected"]
    out = {}
    for _, qs in sorted(drafts(d), key=lambda f: (f[0].startswith("revised-"), f[0])):
        for q in qs:
            out[q["tmp_id"]] = [{"id": p.get("id") or p["tmp_id"], "question": p["question"], "answer": p["answer"],
                                 "concept": p.get("concept")}
                                for p, _, _ in overlap_candidates(q, others)
                                if (p.get("id") or p["tmp_id"]) != q["tmp_id"]]
            others.append(q)
    return out


def cmd_rate(args):
    d = run_dir(args)
    system = prompt("house-style", "rate")
    todo = [(name, qs) for name, qs in drafts(d) if qs and not (d / "ratings" / f"{name}.json").exists()]
    cands = rate_candidates(d) if todo else {}

    def work(group):
        qs = [q for _, qq in group for q in qq]
        items = [{**for_review(q), "overlap_candidates": cands.get(q["tmp_id"], [])} for q in qs]
        user = "## Questions\n" + json.dumps(items, ensure_ascii=False)
        out = claude(system, user, RATE_SCHEMA, args.model, d)
        got = {r["id"]: r for r in out["ratings"]}
        missing = []
        for name, qq in group:
            ids = [q["tmp_id"] for q in qq]
            if all(i in got for i in ids):
                save_json(d / "ratings" / f"{name}.json", {i: got[i] for i in ids})
            else:  # a partial file would count as done and never be retried
                missing += [i for i in ids if i not in got]
        progress.detail(f"  rate: {', '.join(name for name, _ in group)} ({len(qs)} questions)")
        if missing:
            raise RuntimeError(f"no rating for {', '.join(sorted(missing))}")

    return parallel(work, grouped(todo), args.jobs, "rate", "calls")


def needs_check(q):
    return bool(q["needs_fact_check"] or re.search(r"\d", q["question"] + q["answer"] + q["fun_fact"]))


def cmd_factcheck(args):
    d = run_dir(args)
    system = prompt("factcheck")
    _, done = collect(d)  # includes verdicts kept through a revision (PE-3)
    todo = []
    for name, qs in drafts(d):
        need = [q for q in qs if needs_check(q) and q["tmp_id"] not in done]
        if need and not (d / "factchecks" / f"{name}.json").exists():
            todo.append((name, need))

    def work(item):
        name, qs = item
        user = "## Questions (Spanish)\n" + json.dumps([for_review(q) for q in qs], ensure_ascii=False)
        out = claude(system, user, FACT_SCHEMA, args.model, d, web=True)
        save_json(d / "factchecks" / f"{name}.json", {c["id"]: c for c in out["checks"]})
        progress.detail(f"  factcheck: {name}: " + ", ".join(c["verdict"] for c in out["checks"]))

    return parallel(work, todo, args.jobs, "factcheck", "calls")


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


def stem(text):
    """norm() with every word's trailing «s», then «e», dropped: Almenas → almena, padres → padr."""
    return " ".join(re.sub(r"e$", "", re.sub(r"s$", "", w)) if len(w) > 3 else w for w in norm(text).split())


_KEYS = {}  # id(q) → (q, keys): the report compares every pair


def _overlap_keys(q, cache=_KEYS):
    k = cache.get(id(q))
    if k is None or k[0] is not q:
        keys = [t for t in (q["answer"], q.get("concept")) if t]
        keys = [t for t in keys if not re.search(r"\d", t) and norm(t) not in {"si", "no"}]
        k = cache[id(q)] = (q, {
            "answer": norm(q["answer"]) if q["answer"] in keys else None,
            "stems": {stem(t) for t in keys} - {""},
            "text": f" {stem(q['question'] + ' ' + q.get('fun_fact', ''))} ",
            "question": norm(q["question"])})
    return k[1]


def overlap_candidates(q, others, cap=8):
    """[(other, why, rank)] for B-5 (plan 15): questions that may ask the same fact as q, closest first.
    Rank 0 same answer, 1 similar answer, 2 stem-equal concept or answer, 3 one's concept/answer in
    the other's text. Answers with digits and yes/no only match through the concept."""
    a, found = _overlap_keys(q), []
    for p in others:
        if p is q:
            continue
        b, why, rank = _overlap_keys(p), None, 9
        if a["answer"] and b["answer"]:
            if a["answer"] == b["answer"]:
                why, rank = "same answer", 0
            elif (difflib.SequenceMatcher(None, a["answer"], b["answer"]).ratio() >= 0.8
                  or min(len(a["answer"]), len(b["answer"])) >= 4
                  and (f" {a['answer']} " in f" {b['answer']} " or f" {b['answer']} " in f" {a['answer']} ")):
                why, rank = "similar answer", 1
        if not why and a["stems"] & b["stems"]:
            why, rank = f"same stem «{min(a['stems'] & b['stems'])}»", 2
        if not why:
            hit = next((s for s in a["stems"] if len(s) >= 4 and f" {s} " in b["text"]), None)
            if hit:
                why, rank = f"«{hit}» in its text", 3
            elif hit := next((s for s in b["stems"] if len(s) >= 4 and f" {s} " in a["text"]), None):
                why, rank = f"its «{hit}» in this text", 3
        if why:
            found.append((rank, -difflib.SequenceMatcher(None, a["question"], b["question"]).ratio(), p, why))
    found.sort(key=lambda f: f[:2])
    return [(p, why, rank) for rank, _, p, why in found[:cap]]


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
    import media as media_tool  # authoring/tools/media.py
    d = run_dir(args)
    data = load_json(POOL)
    pool = data["questions"]
    ratings, checks = collect(d)
    merged = set(load_json(d / "merged.json", []))
    next_id = max(int(q["id"][2:]) for q in pool) + 1
    added, dropped = [], load_json(d / "dropped.json", [])
    ids = load_json(d / "ids.json", {})  # tmp_id -> pool id, for the review step
    by_id = {q["id"]: q for q in pool} | {q["tmp_id"]: q for _, qs in drafts(d) for q in qs}
    for _, qs in drafts(d):
        for q in qs:
            tid = q["tmp_id"]
            if tid in merged: continue
            r, c = ratings.get(tid), checks.get(tid)
            reason = None
            if r is None: reason = "not rated yet"
            elif needs_check(q) and c is None: reason = "not fact-checked yet"
            elif r.get("no_overlap", 5) < 4:  # the concept isn't retired (plan 15)
                other = r.get("overlap_with") or "?"
                p = by_id.get(other)
                reason = f"overlap like {ids.get(other, other)}" + (f": {p['question']} → {p['answer']}" if p else "")
            elif any(r.get(k, 5) < 4 for k in HARD_CRITERIA):
                reason = "hard fail: " + ", ".join(f"{k} {r.get(k, '-')}" for k in HARD_CRITERIA)
            elif c and c["verdict"] == "wrong": reason = f"fact-check wrong: {c['problem']}"
            elif soft_score(r) < args.min_score: reason = f"soft score {soft_score(r):.2f} < {args.min_score}"
            else: reason = duplicates(q, pool) and "duplicate " + duplicates(q, pool)
            if reason:
                if not reason.startswith("not "):
                    dropped.append({"tmp_id": tid, "reason": reason, "question": q["question"], "answer": q["answer"]})
                    merged.add(tid)
                progress.detail(f"  skip {tid}: {reason}")
                continue
            new = {
                "id": f"q-{next_id:04d}", "status": "draft",
                "difficulty": q["difficulty"], "description": q["description"], "question": q["question"],
                "answer": q["answer"], "wrong_answers": q["wrong_answers"], "hints": q["hints"],
                "media": media_tool.unpicked(q["media"]),
                "fun_fact": q["fun_fact"], "subcategory": q["subcategory"], "style": q.get("style"),
                "concept": q.get("concept"), "axes": q.get("axes"),
                "quality": {k: r.get(k) for k in [*RUBRIC, "difficulty_estimate", "notes"]},
                "fact_checked": bool(c and c["verdict"] == "confirmed"), "needs_media": q["needs_media"],
                "batch": args.run, "review": None, "bundle": q.get("bundle", "base"),
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
        w.update(tmp_id=q["id"], style=q.get("style"), axes=q.get("axes"), concept=q.get("concept"), bundle=q.get("bundle"),
                 subcategory=q.get("subcategory"),
                 media={k: q["media"][k] for k in ["type", "role", "query", "note"]},
                 needs_fact_check=True, needs_media=bool(q.get("needs_media")),
                 background_query=(q.get("background") or {}).get("query", ""),
                 feedback=(q.get("review") or {}).get("feedback") if q["status"] == "needs_work" else None)
        work.append(w)
    for i in range(0, len(work), 10):
        save_json(d / "drafts" / f"chunk-{i // 10 + 1:02d}.json", {"questions": work[i:i + 10], "skipped": []})
    save_json(d / "run.json", {"source": "pool", "batch": args.batch})
    print(f"imported {len(work)} question(s) into {len(range(0, len(work), 10))} chunk(s)")


DIFFICULTY_GAP = 3  # rater on 1–15: mean |diff| 1.5 at 10–15 (task 30), so only big gaps count


def issues_of(q, r, c):
    """Reasons to revise a question; empty when it looks fine or overlaps (merge drops it).

    Only what the pilot showed to matter (D-16): the gamemaster's feedback, the fact-check,
    the hard criteria, and big difficulty gaps. Low soft scores (fun, distractors…) didn't
    predict the gamemaster's decisions, so they don't trigger a revision.
    """
    out = []
    if r and r.get("no_overlap", 5) < 4:
        return out  # merge drops it; a revision would only ask another fact (plan 15)
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
    for name, items in todo:
        if not items:  # nothing to revise: saved empty, so the file counts as done
            save_json(d / "revisions" / f"{name}.json", {})

    def work(group):
        items = [it for _, its in group for it in its]
        user = "## Questions with issues\n" + json.dumps(items, ensure_ascii=False)
        out = claude(system, user, REVISE_SCHEMA, args.model, d)
        got = {r["id"]: r for r in out["results"]}
        missing = []
        for name, its in group:
            ids = [it["id"] for it in its]
            if all(i in got for i in ids):
                save_json(d / "revisions" / f"{name}.json", {i: got[i] for i in ids})
            else:  # a partial file would count as done and never be retried
                missing += [i for i in ids if i not in got]
        actions = [r["action"] for r in got.values()]
        progress.detail(f"  revise: {', '.join(name for name, _ in group)}: {len(items)} with issues → "
                        + ", ".join(f"{a} {actions.count(a)}" for a in ["keep", "revise", "drop"] if a in actions))
        if missing:
            raise RuntimeError(f"no revision result for {', '.join(sorted(missing))}")

    return parallel(work, grouped([(n, its) for n, its in todo if its]), args.jobs, "revise", "calls")


def revise_in_pool(q, new, reason, today):
    """Write a revised question into pool question q; `revision.previous` keeps what changed
    (the review tool shows it). Returns the changed keys."""
    import media as media_tool  # authoring/tools/media.py
    new_media = {**q["media"], **new["media"], "note": new["media"]["note"] or None}
    media_changed = any(new_media[k] != q["media"][k] for k in ["type", "query"])
    if media_changed:
        new_media = media_tool.unpicked(new_media)
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
    q["revision"] = {"action": "revise", "reason": reason, "previous": previous, "revised_on": today}
    for slot in ("media", "background"):  # stale candidates for a changed search
        if slot in previous:
            path = media_tool.candidates_path(q["id"], slot)
            if path.exists():
                path.unlink()
    return previous


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
            revise_in_pool(q, new, rev["reason"], today)
        if q["status"] == "needs_work":
            q["status"], q["review"] = "draft", None
        counts[rev["action"]] += 1
        applied.add(qid)
    save_pool(data)
    save_json(d / "applied.json", sorted(applied))
    print("applied: " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
          + f". Next: trivia-media fetch --batch {cfg['batch']}")


FACT_FIELDS = ["question", "answer", "wrong_answers", "hints", "fun_fact"]


def apply_to_drafts(d, revisions, applied):
    """New drafts (not yet merged): revised questions move to a new draft file and lose their
    rating and fact-check, so `rate` and `factcheck` judge the new version before `merge`.
    Kept and dropped ones stay as they are; merge's hard checks still decide.
    A `confirmed` fact-check stays when the revision changed none of the facts (PE-3)."""
    _, checks = collect(d)
    moved, kept_checks, counts = [], set(), {"keep": 0, "revise": 0, "drop": 0, "malformed": 0}
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
            c = checks.get(q["tmp_id"])
            if c and c["verdict"] == "confirmed" and all(new[k] == q[k] for k in FACT_FIELDS):
                kept_checks.add(q["tmp_id"])
            counts["revise"] += 1
            applied.add(q["tmp_id"])
        if len(rest) != len(qs):
            f = d / "drafts" / f"{name}.json"
            save_json(f, {**load_json(f), "questions": rest})
    gone = {q["tmp_id"] for q in moved}
    for sub, drop in (("ratings", gone), ("factchecks", gone - kept_checks)):  # the rating is always redone
        for f in (d / sub).glob("*.json"):
            data = load_json(f)
            if drop & data.keys():
                save_json(f, {k: v for k, v in data.items() if k not in drop})
    if kept_checks:
        print(f"  kept {len(kept_checks)} confirmed fact-check(s): the revision changed no facts")
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
        print(f"  {c['name']}" + (f" ({c['bundle']})" if c["bundle"] != "base" else ""))
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


# Saturation check (plan 14): a subcategory is saturated when any of these holds.
SAT_AFTER_TOP_UP = 36  # unused right after its last top-up (2 batches of 18 slots)
SAT_HARD = 10  # unused concepts at known_at ≥ 11
SAT_OVERLAP = 0.10  # overlaps / drafts in its last batch
SAT_OVERLAP_MIN = 2  # … and at least this many (one is noise)
SAT_ASKED = 60  # questions in any status = avoid-list length
HARD_AT = 11


def bundle_runs(bundle, n=2):
    """The last n merged `qgen batch` runs of the bundle, oldest first (unfinished ones too)."""
    import health  # authoring/tools/health.py (imports qgen)
    return [r for r in health.batch_runs()
            if (load_json(WORK / r / "run.json", {}) or {}).get("bundle", "base") == bundle][-n:]


def saturation(pool, bundle):
    """{subcategory: row} of the bundle (plan 14): counts, concept supply, overlaps of its last two
    batches and the saturation flags; `list` None = no concept list yet (never saturated)."""
    import health  # authoring/tools/health.py (imports qgen)
    runs = bundle_runs(bundle)
    ovl = [health.overlaps_by_subcategory(r, pool) for r in runs]
    rows = {}
    for sub in categories.subcategories(bundle):
        qs = [q for q in pool if q.get("subcategory") == sub]
        lst = concepts.load(sub)
        r = {"approved": sum(q["status"] == "approved" for q in qs), "asked": len(qs), "list": None,
             "unused": None, "hard": None, "top_ups": 0, "overlaps": 0, "drafts": 0, "flags": []}
        for o in ovl:
            r["overlaps"] += o.get(sub, [0, 0])[0]
            r["drafts"] += o.get(sub, [0, 0])[1]
        last = next((o[sub] for o in reversed(ovl) if sub in o), None)  # its last batch
        if lst is not None:
            free = concepts.unused(lst, concepts.uses(pool, sub))
            tops = lst.get("top_ups", [])
            r |= {"list": len(lst["concepts"]), "unused": len(free), "top_ups": len(tops),
                  "hard": sum(c["known_at"] >= HARD_AT for c in free)}
            r["flags"] = [f for f, on in [
                ("top-up dry", tops and tops[-1]["unused"] < SAT_AFTER_TOP_UP),
                ("few hard", r["hard"] < SAT_HARD),
                ("overlaps", last and last[0] >= max(SAT_OVERLAP_MIN, SAT_OVERLAP * last[1])),
                ("long avoid list", r["asked"] >= SAT_ASKED)] if on]
        rows[sub] = r
    return rows


def report_saturation(pool, bundle):
    rows = saturation(pool, bundle)
    runs = bundle_runs(bundle)
    print(f"\nsaturation per subcategory ({bundle}; overlaps = drops + needs_work for overlap / drafts, "
          f"{' and '.join(runs) or 'no batch yet'}):")
    print(f"  {'':34}approved  asked  list  unused  hard  top-ups  overlaps  flags")
    for c in categories.load():
        if c["bundle"] != bundle:
            continue
        print(f"  {c['name']}")
        for sub in c["subcategories"]:
            r = rows[sub]
            supply = (f"{r['list']:4}  {r['unused']:6}  {r['hard']:4}  {r['top_ups']:7}" if r["list"] is not None
                      else f"{'no list':>30}")
            ovl = f"{r['overlaps']}/{r['drafts']}" if r["drafts"] else "–"
            flags = ("SATURATED: " + ", ".join(r["flags"])) if r["flags"] else ""
            print(f"    {sub[:32]:32}{r['approved']:8}  {r['asked']:5}  {supply}  {ovl:>8}  {flags}")
    sat = [s for s, r in rows.items() if r["flags"]]
    print(f"  saturated: {len(sat)} of {len(rows)}{': ' + ', '.join(sat) if sat else ''}; "
          f"no list: {sum(r['list'] is None for r in rows.values())}")
    print(f"  thresholds: unused after last top-up < {SAT_AFTER_TOP_UP}; unused at known_at ≥ {HARD_AT} < {SAT_HARD}; "
          f"overlaps ≥ {100 * SAT_OVERLAP:.0f} % of its drafts in its last batch and ≥ {SAT_OVERLAP_MIN}; asked ≥ {SAT_ASKED}")
    print(f"\nper broad category ({bundle}):")
    print(f"  {'':34}subcategories  approved  unused hard  saturated")
    for c in categories.load():
        if c["bundle"] != bundle:
            continue
        rs = [rows[s] for s in c["subcategories"]]
        print(f"  {c['name'][:32]:32}  {len(rs):13}  {sum(r['approved'] for r in rs):8}  "
              f"{sum(r['hard'] or 0 for r in rs):11}  {sum(bool(r['flags']) for r in rs):9}")


def calibration(run, pool=None):
    """{target level: row} for a run (plan 13): drawn slots and their mean concept `known_at`; n drafted;
    mean drafted, rated and final difficulty (None if there are none); merged and approved counts.
    Plan 16 reuses it."""
    d = WORK / run
    plan = load_json(d / "slots.json", {})
    ratings, _ = collect(d)
    ids = load_json(d / "ids.json", {})
    by_id = {q["id"]: q for q in (pool if pool is not None else load_json(POOL)["questions"])}
    rows = {}
    row = lambda lvl: rows.setdefault(lvl, {"slots": 0, "known_at": [], "drafted": [], "rated": [], "final": [],
                                            "merged": 0, "approved": 0})
    for sub, slots in plan.items():
        known = {c["name"]: c["known_at"] for c in (concepts.load(sub) or {"concepts": []})["concepts"]}
        for sl in slots:
            r = row(sl["target_difficulty"])
            r["slots"] += 1
            if sl["concept"] in known: r["known_at"].append(known[sl["concept"]])
    for _, qs in drafts(d):  # revised drafts too (revised-*.json)
        for q in qs:
            r = row(plan[q["subcategory"]][q["slot"]]["target_difficulty"])
            r["drafted"].append(q["difficulty"])
            if q["tmp_id"] in ratings: r["rated"].append(ratings[q["tmp_id"]]["difficulty_estimate"])
            final = by_id.get(ids.get(q["tmp_id"]))
            if final:
                r["final"].append(final["difficulty"])
                r["merged"] += 1
                r["approved"] += final["status"] == "approved"
    mean = lambda xs: sum(xs) / len(xs) if xs else None
    return {lvl: {"slots": r["slots"], "n": len(r["drafted"]),
                  **{k: mean(r[k]) for k in ("drafted", "rated", "final", "known_at")},
                  "merged": r["merged"], "approved": r["approved"]} for lvl, r in sorted(rows.items())}


def last_batches(n=2):
    runs = [p.name for p in WORK.glob("batch-*") if (p / "slots.json").exists() and re.fullmatch(r"batch-\d+", p.name)]
    return sorted(runs, key=lambda r: int(r[6:]))[-n:]


def report_calibration(runs):
    pool = load_json(POOL)["questions"]
    fmt = lambda x: f"{x:5.1f}" if x is not None else "    –"
    for run in runs:
        if not (WORK / run / "slots.json").exists():
            sys.exit(f"no work/{run}/slots.json")
        print(f"calibration {run} (per target level; means; '–' = none yet):")
        print("  target  slots  known_at  drafts  drafted  rated  final  merged  approved")
        for lvl, r in calibration(run, pool).items():
            print(f"  {lvl:6} {r['slots']:6}     {fmt(r['known_at'])}  {r['n']:6}    {fmt(r['drafted'])}  "
                  f"{fmt(r['rated'])}  {fmt(r['final'])}  {r['merged']:6}  {r['approved']:8}")


def report_overlaps():
    """Overlap candidates among approved questions (plan 15), for cleanup in the review tool. No LLM."""
    pool = [q for q in load_json(POOL)["questions"] if q["status"] == "approved"]
    pairs = sorted(((rank, p["id"], q["id"], p, q, why) for i, q in enumerate(pool)
                    for p, why, rank in overlap_candidates(q, pool[:i])), key=lambda x: x[:3])
    print(f"{len(pairs)} overlap candidate pair(s) among {len(pool)} approved questions, strongest first:")
    for *_, p, q, why in pairs:
        print(f"  {p['id']} / {q['id']}  {why}: {p['answer']} | {q['answer']}\n"
              f"      {p['question']}\n      {q['question']}")


def report_progress(pool, bundle):
    """Approved vs. targets per difficulty and per broad category (plan 12); quiet without targets."""
    t = targets.load_targets(bundle)
    if t is None:
        return
    approved = [q for q in pool if q["status"] == "approved" and q.get("bundle") == bundle]
    print(f"progress vs. targets ({bundle}):")

    def line(label, n, goal):
        pct = f"{100 * n / goal:3.0f}%" if goal else "   –"
        miss = f"  missing {goal - n}" if n < goal else ""
        print(f"  {label}: {n:4} / {goal:4}  {pct}{miss}")
    by_diff = Counter(q["difficulty"] for q in approved)
    for d, goal in sorted(t["difficulty"].items()):
        line(f"difficulty {d:2}", by_diff[d], goal)
    line("total        ", len(approved), t["total"])
    broad = categories.broad_of()
    by_cat = Counter(broad[q["subcategory"]]["slug"] for q in approved if q.get("subcategory") in broad)
    shares = targets.category_shares(bundle)
    w = max(map(len, shares), default=0)
    print("  per broad category (derived share, guide only):")
    for slug, share in shares.items():
        line(f"  {slug:{w}}", by_cat[slug], round(share))


def committed_batches(bundle, n=2):
    """The last n `qgen batch` runs of the bundle that are merged and done, oldest first."""
    import health  # authoring/tools/health.py (imports qgen)
    def ok(run):
        cfg = load_json(WORK / run / "run.json", {}) or {}
        return cfg.get("done") and cfg.get("bundle", "base") == bundle
    return [r for r in health.batch_runs() if ok(r)][-n:]


def spot_agreement(batch, checks):
    """(decided, agreed) of the batch's spot check: agree = both accept or both don't (plan 16)."""
    items = [i for i in (checks.get(batch) or {}).get("items", {}).values() if i.get("human")]
    return len(items), sum((i["llm"] == "approved") == (i["human"] == "approved") for i in items)


def qc_stats(batch, checks, pool):
    """Spot check and audit numbers of a batch (plan 16); counts, rates are left to the reader."""
    items = {i: it for i, it in (checks.get(batch) or {}).get("items", {}).items() if it.get("human")}
    n, agreed = spot_agreement(batch, checks)
    found, dec = audits(batch), llm_decisions(batch) if (WORK / batch).is_dir() else {}
    accept = lambda d: d == "approved"
    audited = [it for it in items.values() if it.get("audit")]
    false_approve = [i for i, it in items.items() if accept(it["llm"]) and not accept(it["human"])]
    q = targets.load_quality()
    return {"audit_n": len(found),
            "audit_approved": len([i for i in found if dec.get(i) == "approved"]),
            "audit_major_approved": sum(is_major(a) for i, a in found.items() if dec.get(i) == "approved"),
            "human_n": n, "agreed": agreed, "false_approve": false_approve,
            "false_needs_work": [i for i, it in items.items() if not accept(it["llm"]) and accept(it["human"])],
            "difficulty_2": sum(abs(it["difficulty"][0] - it["difficulty"][1]) >= 2 for it in items.values()),
            "media_changed": sum(it["media_changed"] for it in items.values()),
            "audit_human_n": len(audited),
            "audit_human_agreed": sum((it["audit"] == "ok") == accept(it["human"]) for it in audited),
            "audit_caught": sum(items[i].get("audit") == "problem" for i in false_approve),
            "passes": None if not q or not n else n >= q["spot_check_size"] and agreed >= q["min_agreement"] * n,
            "items": items}


def qc_pct(n, of):
    return f"{n} of {of} ({100 * n / of:.0f} %)" if of else "–"


QC_CHANGES = "Changes from this QC: "


def qc_section(batch, pool=None):
    """The batch report's "## Quality control" (plan 16): spot check vs. LLM review and audit; [] without a spot check.
    Keeps the report's "Changes from this QC" line (QC step 4, `--changes`)."""
    checks = load_json(layout.SPOT_CHECKS, {}) or {}
    if not (checks.get(batch) or {}).get("items"):
        return []
    pool = pool if pool is not None else load_json(POOL)["questions"]
    by_id = {q["id"]: q for q in pool}
    s, q = qc_stats(batch, checks, pool), targets.load_quality()
    n = s["human_n"]
    verdict = "" if s["passes"] is None else (
        f" {'✓' if s['passes'] else '✗'} (bar: ≥ {q['spot_check_size']} questions, ≥ {100 * q['min_agreement']:.0f} %)")
    lines = ["## Quality control", "",
             "The gamemaster's blind spot check (`/review?batch=…&sample=1`) against the LLM review and the audit "
             "(plan 16, `qgen report --qc`). Agree = both accept or both don't.", "",
             f"- Spot check: {n} decided of {checks[batch].get('size', '?')}",
             f"- Agreement with the LLM review: {qc_pct(s['agreed'], n)}{verdict}",
             f"- False approve (LLM approved, human not): {qc_pct(len(s['false_approve']), n)}"
             + (f"; the audit flagged {s['audit_caught']}" if s["false_approve"] else ""),
             f"- False needs work (LLM not approved, human approved): {qc_pct(len(s['false_needs_work']), n)}",
             f"- Difficulty |Δ| ≥ 2: {qc_pct(s['difficulty_2'], n)}",
             f"- Media changed: {qc_pct(s['media_changed'], n)}",
             f"- Audit/human agreement: {qc_pct(s['audit_human_agreed'], s['audit_human_n'])}", "",
             "Disagreements with the LLM review, by the human's problems:", ""]
    groups = {}
    for i in s["false_approve"] + s["false_needs_work"]:
        for p in s["items"][i]["problems"] or ["no problem given"]:
            groups.setdefault(p, []).append(i)
    for p in [*PROBLEMS, "no problem given"]:
        if p not in groups:
            continue
        lines += [f"### {p} ({len(groups[p])})", ""]
        for i in groups[p]:
            it, rv = s["items"][i], (by_id.get(i) or {}).get("review") or {}
            fb = rv.get("feedback") if rv.get("reviewer") == "human" else None
            lines.append(f"- **{i}** LLM {it['llm']} → human {it['human']}, audit {it.get('audit') or '–'}"
                         f"{': ' + fb if fb else ''} (http://127.0.0.1:8001/review/{i})")
        lines.append("")
    if not groups:
        lines += ["None.", ""]
    old = layout.REPORTS / f"{batch}.md"
    prev = re.search(rf"^{QC_CHANGES}(.*)$", old.read_text(encoding="utf-8"), re.M) if old.exists() else None
    return lines + [QC_CHANGES + (prev.group(1) if prev else "none yet (QC step 4)"), ""]


def write_qc(batch, changes=None):
    """Rewrite "## Quality control" in authoring/reports/<batch>.md (before "## Needs work")."""
    path = layout.REPORTS / f"{batch}.md"
    if not path.exists():
        sys.exit(f"no {path.relative_to(ROOT)}: run `qgen batch-report --run {batch}` first")
    section = qc_section(batch)
    if not section:
        sys.exit(f"no spot check of {batch} in {layout.SPOT_CHECKS.relative_to(ROOT)}")
    if changes is not None:
        section[-2] = QC_CHANGES + changes
    lines = path.read_text(encoding="utf-8").split("\n")
    start = next((k for k, l in enumerate(lines) if l == "## Quality control"), None)
    if start is None:
        start = end = next((k for k, l in enumerate(lines) if l == "## Needs work"), len(lines))
    else:
        end = next((k for k in range(start + 1, len(lines)) if lines[k].startswith("## ")), len(lines))
    path.write_text("\n".join(lines[:start] + section + lines[end:]), encoding="utf-8")
    return path


def qc_trend(pool=None):
    """Markdown table: one column per batch with a spot check or audit (plan 16); [] without any."""
    checks = load_json(layout.SPOT_CHECKS, {}) or {}
    runs = sorted({*checks, *(p.parent.parent.name for p in [*WORK.glob("batch-*/audit/q-*.json"),
                                                             *WORK.glob("backaudit-*/audit/q-*.json")])},
                  key=lambda r: int(r[6:]) if re.fullmatch(r"batch-\d+", r) else 0)
    if not runs:
        return []
    pool = pool if pool is not None else load_json(POOL)["questions"]
    cols = [qc_stats(r, checks, pool) for r in runs]
    q = targets.load_quality()
    pct = lambda n, of: f"{100 * n / of:.0f} %" if of else "–"
    rows = [("audit n", lambda s: str(s["audit_n"])),
            ("major among approved", lambda s: pct(s["audit_major_approved"], s["audit_approved"])),
            ("human n", lambda s: str(s["human_n"])),
            ("agreement", lambda s: pct(s["agreed"], s["human_n"])),
            ("false approve", lambda s: pct(len(s["false_approve"]), s["human_n"])),
            ("difficulty |Δ| ≥ 2", lambda s: pct(s["difficulty_2"], s["human_n"])),
            ("audit/human agreement", lambda s: pct(s["audit_human_agreed"], s["audit_human_n"]))]
    bar = f"≥ {q['spot_check_size']} questions, ≥ {100 * q['min_agreement']:.0f} %" if q else "no quality keys"
    mark = {True: "✓", False: "✗", None: "–"}
    return ["| metric | " + " | ".join(runs) + " |", "|---|" + "---:|" * len(runs),
            *[f"| {k} | " + " | ".join(f(s) for s in cols) + " |" for k, f in rows],
            f"| **quality** ({bar}) | " + " | ".join(mark[s["passes"]] for s in cols) + " |"]


def report_qc(batch, changes=None):
    if batch:
        print(f"  report: {write_qc(batch, changes).relative_to(ROOT)}")
        return print("\n".join(qc_section(batch)))
    if changes is not None:
        sys.exit("--changes needs a batch")
    lines = qc_trend()
    print("\n".join(lines) if lines else "no spot check or audit yet")


def exit_check(pool, bundle):
    """Milestone 1's "done when" (plan 12): [(ok, criterion, detail)]; missing data counts as a fail."""
    import health  # authoring/tools/health.py (imports qgen)
    t = targets.load_targets(bundle)
    if t is None:
        sys.exit(f"no targets for bundle {bundle!r} in authoring/data/targets.json")
    approved = [q for q in pool if q["status"] == "approved" and q.get("bundle") == bundle]
    out = [(len(approved) >= t["total"], f"approved {bundle} ≥ {t['total']}", f"{len(approved)}")]
    have = Counter(q["difficulty"] for q in approved)
    short = [f"{d}: {have[d]}/{goal}" for d, goal in sorted(t["difficulty"].items()) if have[d] < goal]
    out.append((not short, "every difficulty ≥ its target", "short " + ", ".join(short) if short else "all met"))
    runs = committed_batches(bundle)
    if len(runs) < 2:
        out.append((False, "last two batches pass the health thresholds", f"not available (batches: {', '.join(runs) or 'none'})"))
    else:
        fails = {r: health.failures(r, pool) for r in runs}
        if any(f is None for f in fails.values()):
            out.append((False, "last two batches pass the health thresholds", "not available (no thresholds yet)"))
        else:
            bad = [f"{r}: {', '.join(f)}" for r, f in fails.items() if f]
            out.append((not bad, f"{' and '.join(runs)} pass the health thresholds", "; ".join(bad) or "pass"))
    quality, checks = targets.load_quality(), load_json(layout.SPOT_CHECKS)
    if not quality or checks is None or len(runs) < 2:
        why = "no quality keys in targets.json" if not quality else "no spot-checks.json" if checks is None else "fewer than two batches"
        out.append((False, "last two spot checks agree with the LLM review", f"not available ({why})"))
    else:
        size, rate = quality["spot_check_size"], quality["min_agreement"]
        parts, ok = [], True
        for r in runs:
            n, agreed = spot_agreement(r, checks)
            pass_ = n >= size and agreed >= rate * n
            ok &= pass_
            parts.append(f"{r}: {agreed}/{n} ({100 * agreed / n:.0f} %)" if n else f"{r}: no spot check")
        out.append((ok, f"last two spot checks: ≥ {size} questions, ≥ {100 * rate:.0f} % agreement", "; ".join(parts)))
    errors, _ = validate_pool()
    out.append((not errors, "qgen validate clean", f"{len(errors)} error(s)" if errors else "OK"))
    return out


def report_exit_check(pool, bundle):
    results = exit_check(pool, bundle)
    print(f"exit check, milestone 1 ({bundle}):")
    for ok, criterion, detail in results:
        print(f"  {'✓' if ok else '✗'} {criterion}: {detail}")
    sys.exit(0 if all(ok for ok, *_ in results) else 1)


def cmd_report(args):
    if args.exit_check:
        return report_exit_check(load_json(POOL)["questions"], args.bundle)
    if args.qc is not None:
        return report_qc(args.qc, args.changes)
    if args.calibration is not None:
        return report_calibration(args.calibration or last_batches())
    if args.overlaps:
        return report_overlaps()
    if args.batches is not None:
        import health  # authoring/tools/health.py (imports qgen)
        runs = args.batches or health.batch_runs()
        missing = [r for r in runs if not (WORK / r / "dropped.json").exists()]
        if missing:
            sys.exit(f"not merged yet: {', '.join(missing)}")
        print("\n".join(health.table(runs)))
        return print(health.deficit_line())
    pool = load_json(POOL)["questions"]
    broad = categories.broad_of()
    print(f"pool: {len(pool)} questions")
    for title, key in [("status", lambda q: q["status"]), ("difficulty", lambda q: q["difficulty"]),
                       ("category", lambda q: broad[q["subcategory"]]["slug"] if q.get("subcategory") in broad else None), ("style", lambda q: q.get("style")),
                       *[(f"axes.{a}", lambda q, a=a: (q.get("axes") or {}).get(a)) for a in concepts.AXES],
                       ("media", lambda q: f"{q['media']['type']}/{q['media']['role']}"),
                       ("bundle", lambda q: q.get("bundle"))]:
        print(f"  by {title}: {count(pool, key)}")
    try:
        burned = save_file.burned_ids(args.player)
    except KeyError:
        sys.exit(f"unknown player: {args.player}")
    avail = selection.available(pool, burned)
    who = f"player {args.player}" if args.player else "a new player (global burns only)"
    print(f"unburned approved for {who}: {len(avail)} ({len(burned)} burned)")
    print(f"  by category: {count(avail, lambda q: broad[q['subcategory']]['slug'] if q.get('subcategory') in broad else None)}")
    print(f"  by difficulty: {count(avail, lambda q: q['difficulty'])}")
    print(f"  by bundle: {count(avail, lambda q: q.get('bundle'))}")
    print("supply per level (a game needs 4 per level, D-22):")
    for l in selection.supply(avail):
        lo, hi = l["range"]
        flag = f"  MISSING {l['missing']}" if l["missing"] else ""
        print(f"  level {l['level']:2} (difficulty {lo}–{hi}): {l['candidates']:3} candidates{flag}")
    report_progress(pool, args.bundle)
    if args.subcategories:
        report_subcategories(avail)
        report_saturation(pool, args.bundle)
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
        print(f"  by style: {count(qs, lambda q: q.get('style'))}")
        for a in concepts.AXES:
            print(f"  by axes.{a}: {count(qs, lambda q, a=a: (q.get('axes') or {}).get(a))}")


# --- the LLM batch (D-36, plans/19-repo-layout.md) ----------------------------------------------

BATCH_SLOTS = 18  # draft slots per subcategory (D-46); base: 57 × 18 slots, about 700 merged questions
REVIEW_MODEL = "opus"

# Why a question is needs_work (plan 15): `review.problems`.
PROBLEMS = ["giveaway", "fact", "ambiguity", "overlap", "media", "difficulty", "style", "other"]

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


def review_problems(q):
    """(problems, guessed) of a needs_work question; guessed when the review has no `problems`."""
    rv = q.get("review") or {}
    if rv.get("problems"):
        return rv["problems"], False
    return guess_problems(rv.get("feedback")), True


def batch_questions(run, statuses=("draft",)):
    """The pool's questions of this run that are still waiting for the given steps.
    A `qgen rework` run's questions are the ids in its run.json (QG-23)."""
    ids = set((load_json(WORK / run / "run.json", {}) or {}).get("ids") or [])
    return [q for q in load_json(POOL)["questions"]
            if (q["id"] in ids if ids else q.get("batch") == run) and q["status"] in statuses]


def run_mode(run):
    return (load_json(WORK / run / "run.json", {}) or {}).get("mode")


def is_rework(run):
    return run_mode(run) == "rework"


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
    """Fetch media candidates for every slot of the run's merged questions."""
    import media as media_tool  # authoring/tools/media.py
    errors = []
    todo = [(q, slot) for q in batch_questions(args.run) for slot in slots_of(q)
            if media_tool.load_candidates(q["id"], slot) is None]
    with progress.Bar("media", len(todo), "searches") as bar:
        for q, slot in todo:
            try:
                data = media_tool.fetch_for(q, slot)
                progress.detail(f"  media: {q['id']} {slot}: {len(data['candidates'])} candidate(s)")
                bar.finished()
            except Exception as e:  # noqa: BLE001 — rerun retries the rest
                errors.append(e)
                print(f"  FAILED media {q['id']} {slot}: {e}", file=sys.stderr)
                bar.finished(ok=False)
    return errors


def cmd_sheets(args):
    """One contact sheet per slot (ImageMagick), for the review step to look at."""
    import media as media_tool
    d = run_dir(args)
    errors = []
    todo = [(sheet_path(d, q["id"], slot), found) for q in batch_questions(args.run) for slot in slots_of(q)
            if not sheet_path(d, q["id"], slot).exists() and (found := media_tool.load_candidates(q["id"], slot))]
    with progress.Bar("sheets", len(todo), "sheets") as bar:
        for out, found in todo:
            try:
                thumbs = d / "sheets" / "thumbs" / out.stem
                shown = media_tool.make_sheet(found["candidates"], out, thumbs)
                progress.detail(f"  sheets: {out.name}: {len(shown)} picture(s)")
                bar.finished()
            except Exception as e:  # noqa: BLE001
                errors.append(e)
                print(f"  FAILED sheet {out.name}: {e}", file=sys.stderr)
                bar.finished(ok=False)
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
            "candidates": [{"number": i, "type": c["type"], "source": providers.name(c), "title": c["title"],
                            "width": c["width"], "height": c["height"], "duration": c["duration"],
                            "author": c["author"], "license": c["license"]}
                           for i, c in enumerate(found["candidates"], 1)]}


def cmd_review(args):
    """The LLM review (D-32 criteria, prompts/review.md): one call per question.
    Round 1 reviews every merged question; round 2 only those whose media was searched again."""
    d = run_dir(args)
    reviews = d / "reviews"
    tmp_of = {v: k for k, v in load_json(d / "ids.json", {}).items()}
    ratings, checks = collect(d)
    pool = load_json(POOL)["questions"]
    system = prompt("house-style", "review")
    mode = run_mode(args.run)
    rework = mode in ("rework", "tighten")
    todo = []
    for q in batch_questions(args.run):
        r = load_json(reviews / f"{q['id']}.json", {})
        if args.round == 1 and "round1" not in r:
            todo.append((q, r))
        if args.round == 2 and (r.get("researched") or fixed(r) and not rework) and "round2" not in r:
            todo.append((q, r))

    def work(item):
        q, r = item
        tmp = tmp_of.get(q["id"])
        payload = {
            "question": {k: q[k] for k in ["id", "subcategory", "difficulty", "description", "question", "answer",
                                           "wrong_answers", "hints", "fun_fact"]},
            "rater_notes": (ratings.get(tmp) or {}).get("notes") or (q.get("quality") or {}).get("notes"),
            "fact_check": ({k: check[k] for k in ["verdict", "problem", "correction"]}
                           if (check := fact_check(r, checks.get(tmp))) else "not needed (no number, date or record)"),
            "related": related_questions(q, pool),
            "media": slot_input(d, q, "media"),
            "background": slot_input(d, q, "background") if q.get("background") else None,
            "can_search_again": args.round == 1,
            "can_fix": args.round == 1 and not rework,
            "only_shortened": mode == "tighten",
        }
        user = "## Question to review\n" + json.dumps(payload, ensure_ascii=False)
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


_pool_lock = threading.Lock()


def cmd_fix(args):
    """One revision for every question that round 1 sent back with a fixable problem (QG-22): the
    reviewer's `fix` goes to the revise prompt. Changed facts are checked again; round 2 reviews it.
    Unfixable ones (no `fix`, or the reviser keeps or drops) stay needs_work for the gamemaster.
    In a `qgen rework` run (QG-23) the issue is the needs_work feedback; kept and revised questions
    go back to draft, are all fact-checked and reviewed again, with a new media search if needed."""
    d = run_dir(args)
    rework = is_rework(args.run)
    tighten = load_json(d / "run.json", {}).get("issues") if run_mode(args.run) == "tighten" else None
    tmp_of = {v: k for k, v in load_json(d / "ids.json", {}).items()}
    _, checks = collect(d)
    system = prompt("house-style", "revise")
    today = datetime.date.today().isoformat()
    revise, recheck = [], []
    for q in batch_questions(args.run, ("draft", "needs_work", "approved")):
        path = d / "reviews" / f"{q['id']}.json"
        r = load_json(path, {})
        fix = r.get("fix")
        if fix is None and (issue := f"too long: {tighten[q['id']]}" if tighten else fix_issue(q, r, rework)):
            revise.append((q, path, r, issue))
        elif fix and "factcheck" not in fix and needs_recheck(fix, rework):
            recheck.append((q, path, r))

    def work(group):
        items = []
        for q, _, _, issue in group:
            issues = [issue]
            c = checks.get(tmp_of.get(q["id"]))
            if c and c["verdict"] != "confirmed":
                issues.append(f"fact-check {c['verdict']}: {c['problem']} correction: {c['correction']}")
            items.append({**for_review({**q, "tmp_id": q["id"]}), "issues": issues,
                          "background_query": (q.get("background") or {}).get("query", ""),
                          "needs_media": q.get("needs_media", False)})
        out = claude(system, "## Questions with issues\n" + json.dumps(items, ensure_ascii=False), REVISE_SCHEMA,
                     args.model, d)
        got = {x["id"]: x for x in out["results"]}
        for q, path, r, _ in group:
            rev = got.get(q["id"])
            if rev is None:
                continue
            fix = {"action": rev["action"], "reason": rev["reason"]}
            if rev["action"] == "revise" and (bad := check_question_shape(rev["question"])):
                fix["action"], fix["reason"] = "malformed", "; ".join(bad)
            changed = []
            if fix["action"] == "revise" or (rework and fix["action"] == "keep"):
                def change(x, rev=rev, fix=fix):
                    if fix["action"] == "revise":
                        changed.extend(revise_in_pool(x, rev["question"], rev["reason"], today))
                    if rework or tighten:
                        x["status"], x["review"] = "draft", None
                with _pool_lock:
                    update_pool({q["id"]: change})
            if fix["action"] == "revise":
                fix["changed"] = sorted(changed)
                for slot in ("media", "background"):
                    if slot in changed:
                        sheet_path(d, q["id"], slot).unlink(missing_ok=True)
            r["fix"] = fix
            save_json(path, r)
            if needs_recheck(fix, rework):
                recheck.append((q, path, r))
            progress.detail(f"  fix: {q['id']}: {fix['action']}" + (f" {', '.join(fix['changed'])}" if fixed(r) else ""))
        missing = [q["id"] for q, *_ in group if q["id"] not in got]
        if missing:
            raise RuntimeError(f"no fix result for {', '.join(missing)}")

    def check(group):
        ids = {q["id"] for q, _, _ in group}
        qs = [x for x in load_json(POOL)["questions"] if x["id"] in ids]
        user = "## Questions (Spanish)\n" + json.dumps([for_review({**q, "tmp_id": q["id"]}) for q in qs], ensure_ascii=False)
        out = claude(prompt("factcheck"), user, FACT_SCHEMA, args.check_model, d, web=True)
        got = {c["id"]: c for c in out["checks"]}
        for q, path, r in group:
            if q["id"] in got:
                r["fix"]["factcheck"] = got[q["id"]]
                save_json(path, r)
                progress.detail(f"  fix factcheck: {q['id']}: {got[q['id']]['verdict']}")
        if ids - got.keys():
            raise RuntimeError(f"no fact check for {', '.join(sorted(ids - got.keys()))}")

    errors = parallel(work, chunks(revise), args.jobs, "fix", "calls")
    if any(isinstance(e, UsageLimit) for e in errors):
        return errors
    return errors + parallel(check, chunks(recheck), args.jobs, "fix factcheck", "calls")


def chunks(items, size=GROUP_SIZE):
    return [items[i:i + size] for i in range(0, len(items), size)]


def fix_issue(q, r, rework):
    """What the reviser has to fix, or None."""
    if rework:
        review = q.get("review") or {}
        if q["status"] != "needs_work" or not (review.get("feedback") or "").strip():
            return None
        who = "final reviewer" if review.get("reviewer") == "llm" else "gamemaster feedback"
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
    import media as media_tool
    d = run_dir(args)
    errors, todo = [], []
    for q in batch_questions(args.run):
        path = d / "reviews" / f"{q['id']}.json"
        r = load_json(path, {})
        r1 = r.get("round1") or {}
        if (r1.get("pick") is None and r1.get("new_query") and not r.get("researched")
                and "media" not in (r.get("fix") or {}).get("changed", [])):
            todo.append((q, path, r))
    with progress.Bar("research", len(todo), "searches") as bar:
        for q, path, r in todo:
            query = r["round1"]["new_query"].strip()
            try:
                q["media"]["query"] = query
                media_tool.fetch_for(q, "media")
            except Exception as e:  # noqa: BLE001
                errors.append(e)
                print(f"  FAILED research {q['id']}: {e}", file=sys.stderr)
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
    snapshot = load_json(d / "recorded.json", {})
    for q in batch_questions(args.run):
        full = load_json(d / "reviews" / f"{q['id']}.json", {})
        r = final_review(full)
        if r is None:
            missing.append(q["id"])
            continue
        decision, problems, fields = r["decision"], [r["feedback"].strip()] if r["feedback"].strip() else [], {}
        kinds = set(r.get("problems") or [])
        for slot, key in [("media", "pick"), ("background", "background_pick")]:
            if slot not in slots_of(q):
                continue
            found = (media_tool.load_candidates(q["id"], slot) or {"candidates": []})["candidates"]
            n = r[key]
            if n is None or not 1 <= n <= len(found):
                decision = "needs_work"
                kinds.add("media")
                problems.append("No se encontró una imagen adecuada para esta pregunta." if slot == "media"
                                else "No se encontró una imagen de fondo adecuada.")
                continue
            fields[slot] = media_tool.pick_fields(found[n - 1], slot)
        check = fact_check(full, checks.get(tmp_of.get(q["id"])))
        if check and check["verdict"] != "confirmed":
            decision = "needs_work"
            kinds.add("fact")
            problems.append(f"Verificación de datos: {check['verdict']}. {check['problem']}".strip())
        if decision == "needs_work" and not problems:
            problems.append(r["reasons"])
        review = {"decision": decision, "feedback": " ".join(problems) if decision == "needs_work" else None,
                  "problems": [p for p in PROBLEMS if p in kinds] if decision == "needs_work" else [],
                  "reviewed_on": today, "reviewer": "llm", "model": r["model"], "previous": None}

        def change(x, review=review, fields=fields, check=check if "factcheck" in (full.get("fix") or {}) else None):
            for slot, f in fields.items():
                x[slot].update(f)
            if check:
                x["fact_checked"] = check["verdict"] == "confirmed"
            x.update(review=review, status=review["decision"])
        changes[q["id"]] = change
        snapshot[q["id"]] = {"decision": review["decision"], "problems": review["problems"]}
        progress.detail(f"  record: {q['id']}: {decision}")
    update_pool(changes)
    save_json(d / "recorded.json", snapshot)  # record's decisions, for batch health (plan 15)
    if missing:
        print(f"  no review yet: {', '.join(missing)}", file=sys.stderr)
        return [RuntimeError(f"{len(missing)} question(s) without a review")]
    return []


AUDIT_SAMPLE = 60  # questions per batch the audit reads (plan 16)
AUDIT_SCHEMA = {"type": "object", "required": ["verdict", "problems", "severity", "difficulty_estimate", "notes"],
    "properties": {"verdict": {"type": "string", "enum": ["ok", "problem"]},
                   "problems": {"type": "array", "items": {"type": "string", "enum": PROBLEMS}},
                   "severity": {"type": "string", "enum": ["minor", "major"]},
                   "difficulty_estimate": INT, "notes": STR}}


def llm_decisions(run):
    """{id: decision} of `record`'s LLM review per merged question of the run (plan 16): recorded.json;
    for older runs health.recorded's needs_work and approved for every other question with an llm review.
    A back-audit run (plan 57): approved for its ids."""
    cfg = load_json(WORK / run / "run.json", {}) or {}
    if cfg.get("mode") == "backaudit":
        return {i: "approved" for i in cfg["ids"]}
    rec = load_json(WORK / run / "recorded.json")
    if rec is not None:
        return {i: r["decision"] for i, r in rec.items()}
    import health  # authoring/tools/health.py (imports qgen)
    qs = [q for q in load_json(POOL)["questions"] if q.get("batch") == run]
    work = health.recorded(run, qs)

    def by_llm(r):
        return r is not None and (r.get("reviewer") == "llm" or by_llm(r.get("previous")))
    return {q["id"]: "needs_work" if q["id"] in work else "approved" for q in qs if q["id"] in work or by_llm(q.get("review"))}


def audit_sample(run, n=AUDIT_SAMPLE):
    """The first n ids of the run's audit order (plan 16), seeded by the run's name: LLM-approved and
    needs_work questions interleaved in proportion, so every prefix is a proportional sample and the
    spot check's smaller one is a subset. Drawn once into work/<run>/audit/sample.json."""
    path = WORK / run / "audit" / "sample.json"
    order = load_json(path)
    if order is None:
        rng, strata = random.Random(run), {}
        for i, dec in sorted(llm_decisions(run).items()):
            strata.setdefault(dec, []).append(i)
        keyed = []
        for _, ids in sorted(strata.items()):
            rng.shuffle(ids)
            keyed += [((k + 0.5) / len(ids), rng.random(), i) for k, i in enumerate(ids)]
        order = [i for *_, i in sorted(keyed)]
        if order:
            save_json(path, order)
    return order[:n]


def audits(run):
    """{id: audit} of the run's audited questions."""
    return {p.stem: load_json(p) for p in sorted((WORK / run / "audit").glob("q-*.json"))}


_backaudits = ((), {})  # (folders with mtimes, index)


def backaudit_index():
    """{id: path} of the back-audits (plan 57), newest run wins; rebuilt only when a run's audit folder changes."""
    global _backaudits
    dirs = sorted(WORK.glob("backaudit-*/audit"), key=lambda p: run_number(p.parent.name))
    key = tuple((p, p.stat().st_mtime_ns) for p in dirs)
    if _backaudits[0] != key:
        _backaudits = (key, {f.stem: f for p in dirs for f in sorted(p.glob("q-*.json"))})
    return _backaudits[1]


def audit_path(q):
    """The question's audit file: the newest back-audit, else its batch's (plan 16); None without."""
    p = backaudit_index().get(q["id"])
    if p is None and q.get("batch"):
        p = WORK / q["batch"] / "audit" / f"{q['id']}.json"
    return p if p and p.exists() else None


def audit_of(q):
    p = audit_path(q)
    return load_json(p) if p else None


def run_number(name):
    tail = name.rsplit("-", 1)[-1]
    return int(tail) if tail.isdigit() else 0


def is_major(a):
    return a["verdict"] == "problem" and a["severity"] == "major"


def audit_input(q, pool):
    """The question as played (plan 16): no review, fix, rater notes or fact check."""
    import media as media_tool

    def slot(spec, name):
        found = (media_tool.load_candidates(q["id"], name) or {"candidates": []})["candidates"]
        pick = next((c for c in found if spec.get("source_url") and c.get("page_url") == spec["source_url"]), None)
        return {"type": spec.get("type", "image"), "role": spec.get("role", "decorative"),
                "title": pick["title"] if pick else None}
    return {"question": {k: q[k] for k in ["id", "subcategory", "difficulty", "description", "question", "answer",
                                           "wrong_answers", "hints", "fun_fact"]},
            "media": slot(q["media"], "media"),
            "background": slot(q["background"], "background") if q.get("background") else None,
            "related": related_questions(q, pool)}


def cmd_audit(args):
    """An independent LLM reader of the run's audit sample (plan 16, prompts/audit.md): one call per
    question into work/<run>/audit/<id>.json. Never changes the pool."""
    if getattr(args, "backlog", False):
        return cmd_backaudit(args)
    if getattr(args, "dry_run", False) or getattr(args, "slice", None) is not None:
        sys.exit("--slice and --dry-run need --backlog")
    import health  # authoring/tools/health.py (imports qgen)
    run = args.batch or (health.batch_runs() or [None])[-1]
    if run is None or not (WORK / run).is_dir():
        sys.exit(f"no work/{run}/")
    ids = audit_sample(run)
    if not ids:
        return [RuntimeError(f"{run}: no recorded LLM review to audit")]
    return audit_ids(run, ids, args)


def audit_ids(run, ids, args):
    """Audit the ids not yet audited in work/<run>/audit/."""
    d = WORK / run / "audit"
    d.mkdir(parents=True, exist_ok=True)
    pool = load_json(POOL)["questions"]
    by_id = {q["id"]: q for q in pool}
    todo = [by_id[i] for i in ids if i in by_id and not (d / f"{i}.json").exists()]
    system = prompt("house-style", "audit")
    lo, hi = load_age_groups()["scale"]
    today = datetime.date.today().isoformat()

    def work(q):
        user = "## Question to audit\n" + json.dumps(audit_input(q, pool), ensure_ascii=False)
        out, model = claude(system, user, AUDIT_SCHEMA, args.model, d, web=True, with_model=True)
        if not lo <= out["difficulty_estimate"] <= hi:
            raise RuntimeError(f"difficulty_estimate {out['difficulty_estimate']} not {lo}–{hi}")
        save_json(d / f"{q['id']}.json", {**out, "model": model, "on": today})
        progress.detail(f"  audit: {q['id']}: {out['verdict']} {out['severity']} {', '.join(out['problems'])}")

    return parallel(work, todo, args.jobs, "audit", "questions")


BACKAUDIT_BATCHES = ("pilot", "first-120", "batch-3", "batch-4", "batch-5", "batch-6", "batch-7")  # before D-56, oldest first
BACKAUDIT_SLICE = 200


def backlog(n):
    """The next n approved questions from before D-56 without any audit and in no back-audit run, oldest batch first."""
    taken = {i for p in WORK.glob("backaudit-*/run.json") for i in load_json(p)["ids"]}
    order = {b: k for k, b in enumerate(BACKAUDIT_BATCHES)}
    qs = [q for q in load_json(POOL)["questions"] if q["status"] == "approved" and q.get("batch") in order
          and q["id"] not in taken and audit_path(q) is None]
    return [q["id"] for q in sorted(qs, key=lambda q: order[q["batch"]])][:n]


def cmd_backaudit(args):
    """`qgen audit --backlog` (plan 57): the audit of the next slice of approved questions from before D-56
    into work/backaudit-<k>/, then authoring/reports/backaudit-<k>.md. Resumes an unfinished run first.
    Never changes the pool."""
    open_runs = sorted((p.parent.name for p in WORK.glob("backaudit-*/run.json") if not load_json(p).get("done")),
                       key=run_number)
    if open_runs:
        run = open_runs[0]
        ids = load_json(WORK / run / "run.json")["ids"]
        print(f"Resuming {run}: {len(ids)} question(s)" + (" (--slice ignored)" if args.slice else "") + ".", flush=True)
    else:
        ids = backlog(args.slice or BACKAUDIT_SLICE)
        if not ids:
            sys.exit("No approved question from before D-56 without an audit.")
        numbers = [run_number(p.name) for p in WORK.glob("backaudit-*")]
        run = f"backaudit-{max(numbers, default=0) + 1}"
        if not args.dry_run:
            save_json(WORK / run / "run.json", {"mode": "backaudit", "ids": ids,
                                                "started": datetime.date.today().isoformat()})
            print(f"Starting {run}: {len(ids)} approved question(s).", flush=True)
    if args.dry_run:
        print(f"{run}: {len(ids)} question(s)\n" + " ".join(ids))
        return []
    progress.verbose = False
    errors = audit_ids(run, ids, args)
    if errors:
        if not any(isinstance(e, UsageLimit) for e in errors):
            print(f"\n{len(errors)} error(s). Run `qgen audit --backlog` again.", file=sys.stderr)
        return errors
    cfg = load_json(WORK / run / "run.json")
    save_json(WORK / run / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    out = write_backaudit_report(run)
    major = sum(is_major(a) for a in audits(run).values())
    print(f"\nDone: {run}: {len(ids)} audited, {major} with a major finding.\n  report: {out.relative_to(ROOT)}\n"
          f"Commit exactly this:\n  git add {out.relative_to(ROOT)}\n"
          f"  git commit -m \"{run}: {len(ids)} approved questions audited, {major} major (qgen audit --backlog)\"")
    return []


def write_backaudit_report(run):
    """authoring/reports/<run>.md of a back-audit run (plan 57); `qgen report --qc <run>` adds its QC section."""
    cfg = load_json(WORK / run / "run.json")
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    ids = cfg["ids"]
    lines = [f"# {run}", "",
             f"Made by `qgen audit --backlog` on {datetime.date.today().isoformat()} (plan 57): the audit of approved "
             "questions from before D-56. Generated file: don't edit by hand.", "",
             f"- Questions: {len(ids)} ({ids[0]}…{ids[-1]})",
             "- Batches: " + ", ".join(f"{b} {n}" for b, n in Counter(by_id[i].get("batch") for i in ids if i in by_id).items()),
             "", *audit_section(run), *qc_section(run)]
    out = layout.REPORTS / f"{run}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def costs(path):
    """Dollar amounts in a costs.log, one per Claude call."""
    return [float(line.split("\t")[1]) for line in path.read_text().splitlines()
            if line.count("\t") == 1 and line.split("\t")[1] not in ("None", "")] if path.exists() else []


def audit_section(run):
    """The batch report's "## Audit" (plan 16); [] before the audit ran."""
    found = audits(run)
    if not found:
        return []
    dec = llm_decisions(run)
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    pct = lambda n, of: f"{n} of {of} ({100 * n / of:.0f} %)" if of else "0 of 0"
    back = run_mode(run) == "backaudit"
    what = "every question of the slice (plan 57" if back else "a seeded sample (plan 16"
    lines = ["## Audit", "", f"A second LLM reader of {what}, `prompts/audit.md`), blind to the review. "
             "It changes nothing in the pool; the gamemaster decides its findings in the review tool.", ""]
    for label, d in [("approved", "approved")] + ([] if back else [("needs work", "needs_work")]):
        ids = [i for i in found if dec.get(i) == d]
        lines.append(f"- Major among review {label}: {pct(sum(is_major(found[i]) for i in ids), len(ids))}")
    kinds = Counter(p for a in found.values() for p in a["problems"])
    majors = Counter(p for a in found.values() if is_major(a) for p in a["problems"])
    lines.append("- Problems by kind: " + (", ".join(f"{p} {kinds[p]} ({majors[p]} major)" for p in PROBLEMS if kinds[p])
                                          or "none"))
    gaps = [abs(a["difficulty_estimate"] - by_id[i]["difficulty"]) for i, a in found.items() if i in by_id]
    if gaps:
        lines.append(f"- Mean |audit − final difficulty|: {sum(gaps) / len(gaps):.1f}; ≥ 3 on {pct(sum(g >= 3 for g in gaps), len(gaps))}")
    both = [i for i in found if i in dec]
    agree = sum((dec[i] == "approved") == (not is_major(found[i])) for i in both)
    lines.append(f"- Audit/review agreement (both accept or both not): {pct(agree, len(both))}")
    c = costs(WORK / run / "audit" / "costs.log")
    lines += [f"- {'Slice' if back else 'Sample'}: {len(found)} audited of {len(dec) if back else len(audit_sample(run))}; "
              f"{len(c)} Claude calls, about ${sum(c):.2f}",
              "", "Major findings on approved questions:", ""]
    lines += [f"- **{i}**: {', '.join(a['problems']) or 'other'} — {a['notes']} (http://127.0.0.1:8001/review/{i})"
              for i, a in found.items() if is_major(a) and dec.get(i) == "approved"] or ["None."]
    return lines + [""]


def cmd_sync_run(args):
    """Download the run's picked files into the media cache. Rate limits don't fail the batch."""
    missing = []
    todo = [(label, url) for q in batch_questions(args.run, ("approved", "needs_work"))
            for label, url in media.picked(q) if not media.cache_path(url).is_file()]
    with progress.Bar("sync", len(todo), "files") as bar:
        for label, url in todo:
            try:
                with progress.waiting(f"download {urllib.parse.urlparse(url).hostname}"):
                    media.cached(url)
                bar.finished()
            except Exception as e:  # noqa: BLE001 — listed in the report; `trivia-media sync` retries
                missing.append(label)
                print(f"  not cached: {label}: {e}", file=sys.stderr)
                bar.finished(ok=False)
    save_json(run_dir(args) / "not-cached.json", missing)
    return []


def cmd_batch_report(args):
    """authoring/reports/<run>.md: what the batch produced, written by code; also batches.md (plan 15)."""
    import health  # authoring/tools/health.py (imports qgen)
    d = run_dir(args)
    qs = [q for q in load_json(POOL)["questions"] if q.get("batch") == args.run]
    cfg = load_json(d / "run.json", {})
    dropped = load_json(d / "dropped.json", [])
    calls = costs(d / "costs.log") + costs(d / "audit" / "costs.log")
    models = sorted({(q.get("review") or {}).get("model") for q in qs} - {None})
    approved = [q for q in qs if q["status"] == "approved"]
    work = [q for q in qs if q["status"] == "needs_work"]
    not_cached = load_json(d / "not-cached.json", [])
    lines = [f"# {args.run}", "",
             f"Made by `qgen batch` on {datetime.date.today().isoformat()} (plans/19-repo-layout.md, D-36). "
             "Generated file: don't edit by hand.", "",
             f"- Bundle: {cfg.get('bundle', 'base')}",
             f"- Subcategories ({len(cfg.get('subcategories', []))}): {', '.join(cfg.get('subcategories', []))}",
             f"- Merged: {len(qs)} ({qs[0]['id']}…{qs[-1]['id']})" if qs else "- Merged: 0",
             f"- Approved: {len(approved)}", f"- Needs work: {len(work)}",
             f"- Dropped by the pipeline: {len(dropped)}",
             f"- Reviewed by: {', '.join(models) or '-'}",
             f"- Claude calls: {len(calls)}, about ${sum(calls):.2f} at list price",
             f"- Picked files not cached yet: {len(not_cached)}" + (" (run `trivia-media sync --status approved`)" if not_cached else ""),
             "", *health.health_section(args.run), *audit_section(args.run), *qc_section(args.run), "## Needs work", ""]
    lines += [f"- **{q['id']}** ({q['subcategory']}) {q['question']} → {q['answer']}: {q['review']['feedback']}" for q in work] or ["None."]
    lines += ["", "## Question axes", ""]
    lines += [f"- {a}: " + ", ".join(f"{v} {n}" for v, n in count(qs, lambda q, a=a: (q.get('axes') or {}).get(a)).items())
              for a in concepts.AXES]
    lines += ["", "## Dropped by the pipeline", ""]
    lines += [f"- {x['tmp_id']}: {x['reason']}: {x['question']} → {x['answer']}" for x in dropped] or ["None."]
    out = layout.REPORTS / f"{args.run}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  report: {out.relative_to(ROOT)}")
    print(f"  report: {health.write_batches_md().relative_to(ROOT)}")
    return []


def next_batch():
    """(run name, resuming?) — an unfinished `qgen batch` run is resumed; otherwise batch-<n+1>."""
    open_runs = batches.unfinished_runs()
    if len(open_runs) > 1:
        sys.exit(f"More than one unfinished batch: {', '.join(open_runs)}. Ask the gamemaster which to finish.")
    if open_runs:
        return open_runs[0], True
    names = {q.get("batch") for q in load_json(POOL)["questions"]} | {p.name for p in WORK.iterdir() if p.is_dir()}
    numbers = [int(m.group(1)) for n in names if n and (m := re.fullmatch(r"batch-(\d+)", n))]
    return f"batch-{max(numbers, default=0) + 1}", False


def batch_subcategories(count=None, bundle="base"):
    """The bundle's `count` subcategories (default: batches.SHARE of them, D-46) with the fewest
    approved questions of that bundle, weighted by the deficits (D-54); ties in its categories.json order (D-41)."""
    return batches.subcategories(load_json(POOL)["questions"], count, bundle)


def run_steps(steps, again, run=None):
    """Run (name, fn, args) steps in order, then validate; waits out Claude's usage limit (QG-21).
    Exits 75 or 1 on a step that fails; `again` is the command that continues. Returns the start time.
    With `run`, adds each step's seconds to run.json's "seconds" (batch health, plan 15)."""
    t0 = time.monotonic()
    i = 0
    while i < len(steps):
        name, fn, a = steps[i]
        i += 1
        print(f"\n== [{i}/{len(steps) + 1}] {name}", flush=True)
        t = time.monotonic()
        try:
            errors = fn(a) or []
        except UsageLimit as e:  # a call outside parallel()
            errors = [e]
        print(f"   {name} took {progress.duration(time.monotonic() - t)} "
              f"(batch: {progress.duration(time.monotonic() - t0)})", flush=True)
        if run:
            cfg = load_json(WORK / run / "run.json")
            secs = cfg.setdefault("seconds", {})
            secs[name] = round(secs.get(name, 0) + time.monotonic() - t)
            save_json(WORK / run / "run.json", cfg)
        limit = next((e for e in errors if isinstance(e, UsageLimit)), None)
        if limit and wait_for_reset(limit, again):
            i -= 1  # the step skips the work it already did (QG-21)
            continue
        if limit:
            print(f"\nStopped at `{name}`: Claude's usage limit ({limit}).\n"
                  f"Wait for the reset, then run `{again}` again.", file=sys.stderr)
            sys.exit(75)
        if errors:
            print(f"\nStopped at `{name}` with {len(errors)} error(s). Run `{again}` again; "
                  "if the same step fails three times in a row, stop and report the output.", file=sys.stderr)
            sys.exit(1)
    print(f"\n== [{len(steps) + 1}/{len(steps) + 1}] validate", flush=True)
    errors, _ = validate_pool()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print("\n`qgen validate` failed. Stop and report the output.", file=sys.stderr)
        sys.exit(1)
    return t0


def cmd_batch(args):
    """The whole pipeline in a fixed order (D-36). Rerunning it continues where it stopped."""
    if args.run:
        run, resuming = args.run, (WORK / args.run / "run.json").exists()
    else:
        run, resuming = next_batch()
    d = WORK / run
    if resuming:
        open_bundle = load_json(d / "run.json").get("bundle", "base")
        if open_bundle != args.bundle:
            sys.exit(f"{run} is unfinished and writes for bundle {open_bundle!r}, not {args.bundle!r}. "
                     f"Finish it first: qgen batch" + (f" --bundle {open_bundle}" if open_bundle != "base" else ""))
    else:
        import health  # authoring/tools/health.py (imports qgen)
        stop = health.stop_reason()  # D-55: before concepts, no LLM calls
        if stop:
            print(stop, file=sys.stderr)
            sys.exit(2)
        check_bundle(args.bundle)
        if args.subcategories:
            subs = [s.strip() for s in args.subcategories.split(",") if s.strip()]
            unknown = not_in_bundle(subs, args.bundle)
            if unknown:
                sys.exit(f"Not in {categories.path(args.bundle).relative_to(ROOT)}: {', '.join(unknown)}")
        else:
            subs = batch_subcategories(args.count, args.bundle)
        save_json(d / "run.json", {"mode": "batch", "bundle": args.bundle, "subcategories": subs,
                                   "started": datetime.date.today().isoformat()})
    subs = load_json(d / "run.json")["subcategories"]
    progress.verbose = False  # one bar per step, no line per item (QG-20)
    print(f"{'Resuming' if resuming else 'Starting'} {run} for bundle {args.bundle}: {len(subs)} subcategories. "
          "This takes from several minutes to an hour.", flush=True)

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    steps = [
        ("concepts", cmd_concepts, ns(model="opus", subcategories=None, top_up=True)),
        ("draft", cmd_draft, ns(model="opus", seed=1, slots=BATCH_SLOTS, subcategories=None, bundle=args.bundle)),
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
        ("fix", cmd_fix, ns(model="opus", check_model="sonnet")),
        ("research", cmd_research, ns()),
        ("media", cmd_media, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 2", cmd_review, ns(model=REVIEW_MODEL, round=2)),
        ("record", cmd_record, ns()),
        ("audit", cmd_audit, ns(model="opus", batch=run)),
        ("export", lambda a: cmd_export(a) or [], ns()),
        ("sync", cmd_sync_run, ns()),
        ("batch-report", cmd_batch_report, ns()),
    ]
    t0 = run_steps(steps, "qgen batch" + (f" --bundle {args.bundle}" if args.bundle != "base" else ""), run)
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    qs = [q for q in load_json(POOL)["questions"] if q.get("batch") == run]
    n_ok = sum(q["status"] == "approved" for q in qs)
    print(f"\nDone: {run}: {len(qs)} merged, {n_ok} approved, {len(qs) - n_ok} needs work "
          f"(took {progress.duration(time.monotonic() - t0)}).")
    concept_dir = concepts.concepts_dir(args.bundle).relative_to(ROOT).as_posix()
    print("Commit exactly this:\n"
          f"  git add authoring/data/questions.json app/data/pool.json {concept_dir}/ authoring/reports/{run}.md\n"
          f"  git commit -m \"{run}: {len(qs)} {'' if args.bundle == 'base' else args.bundle + ' '}questions, "
          f"{n_ok} approved (qgen batch)\"")


def cmd_health_ack(args):
    """The gamemaster has looked at a failing batch: clears the stop of `qgen batch` (D-55)."""
    import health  # authoring/tools/health.py (imports qgen)
    if args.batch not in health.batch_runs():
        sys.exit(f"not a merged batch: {args.batch}")
    a = health.acks()
    a[args.batch] = {"date": datetime.date.today().isoformat(), "note": args.note}
    save_json(layout.HEALTH_ACKS, a)
    print(f"acked {args.batch}; `qgen batch` may start the next batch")
    print(f"  report: {health.write_batches_md().relative_to(ROOT)}")


def cmd_rework(args):
    """Every needs_work question with feedback (of one batch with --batch) once more through
    fix → fact check → review with a new media search → record (QG-23). Rerunning continues."""
    open_runs = sorted(p.parent.name for p in WORK.glob("rework-*/run.json") if not load_json(p).get("done"))
    if open_runs:
        run = open_runs[0]
        ignored = [f for f, v in (("--batch", args.batch), ("--model", args.model)) if v]
        print(f"Resuming {run}" + (f" ({', '.join(ignored)} ignored)" if ignored else "") + ".", flush=True)
    else:
        ids = [q["id"] for q in load_json(POOL)["questions"] if q["status"] == "needs_work"
               and (q.get("review") or {}).get("feedback") and (not args.batch or q.get("batch") == args.batch)]
        if not ids:
            sys.exit("No needs_work questions with feedback.")
        numbers = [int(p.name.split("-")[1]) for p in WORK.glob("rework-*") if p.name.split("-")[1].isdigit()]
        run = f"rework-{max(numbers, default=0) + 1}"
        save_json(WORK / run / "run.json", {"mode": "rework", "ids": ids, "batch": args.batch,
                                            "model": args.model or "opus",
                                            "started": datetime.date.today().isoformat()})
        print(f"Starting {run}: {len(ids)} needs_work question(s).", flush=True)
    d = WORK / run
    model = load_json(d / "run.json").get("model", "opus")  # fix + review 1; review 2 stays REVIEW_MODEL (D-65)
    progress.verbose = False

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    t0 = run_steps([
        ("fix", cmd_fix, ns(model=model, check_model="sonnet")),
        ("media", cmd_media, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 1", cmd_review, ns(model=model, round=1)),
        ("research", cmd_research, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 2", cmd_review, ns(model=REVIEW_MODEL, round=2)),
        ("record", cmd_record, ns()),
        ("export", lambda a: cmd_export(a) or [], ns()),
        ("sync", cmd_sync_run, ns()),
    ], "qgen rework")
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    qs = batch_questions(run, ("approved", "needs_work", "draft", "rejected"))
    n_ok = sum(q["status"] == "approved" for q in qs)
    print(f"\nDone: {run}: {n_ok} of {len(qs)} approved, {len(qs) - n_ok} still need work "
          f"(took {progress.duration(time.monotonic() - t0)}).")
    print("Commit exactly this:\n  git add authoring/data/questions.json app/data/pool.json\n"
          f"  git commit -m \"{run}: {n_ok} of {len(qs)} needs_work questions fixed and approved (qgen rework)\"")


TIGHTEN_SCHEMA = {"type": "object", "required": ["flagged"], "properties": {"flagged": {"type": "array", "items": {
    "type": "object", "required": ["id", "issue"], "properties": {"id": STR, "issue": STR}}}}}


def cmd_scan(args):
    """Claude reads every approved and needs_work question text and flags long-winded ones (QG-24)."""
    d = run_dir(args)
    if "issues" in load_json(d / "run.json", {}):
        return []
    qs = [q for q in load_json(POOL)["questions"] if q["status"] in ("approved", "needs_work")]
    groups = [g for g in chunks(qs, 50) if not (d / "scan" / f"{g[0]['id']}.json").exists()]
    system = prompt("house-style", "tighten")

    def work(group):
        items = [{"id": q["id"], "clue": (q.get("axes") or {}).get("clue"), "question": q["question"]} for q in group]
        out = claude(system, "## Questions\n" + json.dumps(items, ensure_ascii=False), TIGHTEN_SCHEMA, args.model, d)
        ids = {q["id"] for q in group}
        save_json(d / "scan" / f"{group[0]['id']}.json", [f for f in out["flagged"] if f["id"] in ids])

    errors = parallel(work, groups, args.jobs, "scan", "calls")
    if not errors:
        flagged = [f for p in sorted((d / "scan").glob("*.json")) for f in load_json(p)]
        cfg = load_json(d / "run.json")
        save_json(d / "run.json", {**cfg, "ids": [f["id"] for f in flagged],
                                   "issues": {f["id"]: f["issue"] for f in flagged}})
        print(f"  {len(flagged)} of {len(qs)} questions flagged", flush=True)
    return errors


def cmd_tighten(args):
    """Find long-winded questions in the whole pool, approved ones included, then shorten, fact-check,
    review and record them like `qgen rework` (QG-24). Kept and dropped ones stay as they were."""
    open_runs = sorted(p.parent.name for p in WORK.glob("tighten-*/run.json") if not load_json(p).get("done"))
    if open_runs:
        run = open_runs[0]
        print(f"Resuming {run}.", flush=True)
    else:
        numbers = [int(p.name.split("-")[1]) for p in WORK.glob("tighten-*") if p.name.split("-")[1].isdigit()]
        run = f"tighten-{max(numbers, default=0) + 1}"
        save_json(WORK / run / "run.json", {"mode": "tighten", "started": datetime.date.today().isoformat()})
        print(f"Starting {run}: reading the whole pool.", flush=True)
    d = WORK / run
    progress.verbose = False

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    t0 = run_steps([
        ("scan", cmd_scan, ns(model="opus")),
        ("fix", cmd_fix, ns(model="opus", check_model="sonnet")),
        ("media", cmd_media, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 1", cmd_review, ns(model=REVIEW_MODEL, round=1)),
        ("research", cmd_research, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 2", cmd_review, ns(model=REVIEW_MODEL, round=2)),
        ("record", cmd_record, ns()),
        ("export", lambda a: cmd_export(a) or [], ns()),
        ("sync", cmd_sync_run, ns()),
    ], "qgen tighten")
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    fixes = {p.stem: (load_json(p).get("fix") or {}).get("action") for p in (d / "reviews").glob("*.json")}
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    revised = [i for i, a in fixes.items() if a == "revise"]
    n_ok = sum(by_id[i]["status"] == "approved" for i in revised if i in by_id)
    print(f"\nDone: {run}: {len(cfg.get('ids', []))} flagged, {len(revised)} shortened, {n_ok} of those approved, "
          f"{len(revised) - n_ok} need work (took {progress.duration(time.monotonic() - t0)}).")
    print("Commit exactly this:\n  git add authoring/data/questions.json app/data/pool.json\n"
          f"  git commit -m \"{run}: {len(revised)} long-winded questions shortened, {n_ok} approved (qgen tighten)\"")


# --- export (D-35) --------------------------------------------------------------

def cmd_export(args):
    pool = load_json(POOL)
    layout.EXPORT.write_text(export_text(pool), encoding="utf-8")
    n = sum(q["status"] == "approved" for q in pool["questions"])
    print(f"exported {n} approved question(s) to {layout.EXPORT.relative_to(ROOT)}")


def licence_problem(slot):
    """True when a picked slot's licence record (plans/26) is missing or off the allowlist.
    PD-US only and PD without a reason aren't errors yet (plans/53)."""
    return any(r.startswith(("missing-data:", "off-allowlist:")) for r in providers.licence_verdict(slot)[1])


def validate_pool():
    """(errors, warnings) for the whole source pool and its export (QP-7)."""
    data = load_json(POOL)
    errors, warnings, ids, unlicensed = [], [], set(), []
    subcategories = categories.broad_of()
    lists = {}
    axes_of = {b: concepts.load_axes(b) for b in categories.bundle_ids()}
    lo, hi = load_age_groups()["scale"]
    bundle_ids = {b["id"] for b in load_bundles()}
    errors += taxonomy_problems()
    errors += age_groups.level_problems(load_age_groups())
    errors += targets.problems((lo, hi), bundle_ids)
    import health  # authoring/tools/health.py (imports qgen)
    errors += targets.health_problems(health.THRESHOLDABLE)
    errors += targets.quality_problems()
    errors += spot_check_problems(data["questions"], (lo, hi))
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
        if rv is not None and not set(rv.get("problems") or []) <= set(PROBLEMS):  # plan 15
            errors.append(f"{qid}: review.problems must be from {', '.join(PROBLEMS)}")
        if rv is not None:  # who reviewed (D-33)
            if rv.get("reviewer") not in {"human", "llm"}: errors.append(f"{qid}: review.reviewer must be human or llm")
            if (rv.get("reviewer") == "llm") != bool(rv.get("model")): errors.append(f"{qid}: review.model must be set exactly for an llm review")
            prev = rv.get("previous")
            if prev is not None and (rv.get("reviewer") != "human" or prev.get("reviewer") != "llm"):
                errors.append(f"{qid}: review.previous must be an llm review under a human one")
        if q.get("subcategory") not in subcategories: errors.append(f"{qid}: subcategory not in any bundle's categories (D-19, D-43)")
        elif q.get("bundle") == "base" and subcategories[q["subcategory"]]["bundle"] != "base":
            errors.append(f"{qid}: a base question needs a subcategory from base's categories (D-49)")
        if q.get("bundle") not in bundle_ids: errors.append(f"{qid}: bundle must be one of app/data/bundles.json (D-39)")
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
                if slot.get("file_url") and licence_problem(slot):
                    unlicensed.append(qid if label == "media" else f"{qid} background")
        if all(k in q for k in ["wrong_answers", "hints", "difficulty", "answer"]):
            errors += [f"{qid}: {p}" for p in check_question_shape(q)]
        if q.get("axes") is not None:  # D-37
            e, w = concepts.axes_problems(q["axes"], axes_of[subcategories.get(q.get("subcategory"), {}).get("bundle", "base")])
            errors += [f"{qid}: {p}" for p in e]
            warnings += [f"{qid}: {p}" for p in w]
        if q.get("concept") is not None:
            sub = q.get("subcategory")
            if sub not in lists:
                lists[sub] = {c["name"] for c in (concepts.load(sub) or {}).get("concepts", [])}
            if q["concept"] not in lists[sub]:
                errors.append(f"{qid}: concept {q['concept']!r} is not in {sub}'s concept list")
    for sub in subcategories:
        lst = concepts.load(sub)
        keys = [concepts.key(c["name"]) for c in (lst or {}).get("concepts", [])]
        dup = sorted({k for k in keys if keys.count(k) > 1})
        if dup:
            errors.append(f"{concepts.path(sub).relative_to(ROOT)}: same concept twice: {', '.join(dup)}")
        bad = [c["name"] for c in (lst or {}).get("concepts", [])
               if not isinstance(c.get("known_at"), int) or not lo <= c["known_at"] <= hi]
        if bad:
            errors.append(f"{concepts.path(sub).relative_to(ROOT)}: known_at missing or not {lo}–{hi} (D-38): "
                          f"{', '.join(bad[:5])}{' …' if len(bad) > 5 else ''}")
    if unlicensed:  # plans/26
        errors.append(f"{len(unlicensed)} approved pick(s) without a complete, allowlisted licence record: "
                        f"{', '.join(unlicensed[:5])}{' …' if len(unlicensed) > 5 else ''}")
    exported = layout.EXPORT.read_text(encoding="utf-8") if layout.EXPORT.exists() else None
    if exported != export_text(data):
        errors.append(f"{layout.EXPORT.relative_to(ROOT)} is not the current export of the pool: run `qgen export`")
    return errors, warnings


def spot_check_problems(questions, scale):
    """Errors in authoring/data/spot-checks.json (plan 16): batches and ids exist, values in range."""
    checks = load_json(layout.SPOT_CHECKS)
    if checks is None:
        return []
    rel, out = "authoring/data/spot-checks.json", []
    batch_of = {q["id"]: q.get("batch") for q in questions}
    decisions, (lo, hi) = {"approved", "needs_work", "rejected"}, scale
    for b, entry in checks.items():
        if b not in batch_of.values():
            out.append(f"{rel}: no batch {b!r} in the pool")
            continue
        if not isinstance(entry.get("size"), int) or entry["size"] < 1 or entry.get("seed") != b:
            out.append(f"{rel}: {b}: size must be an integer ≥ 1 and seed the batch name")
        for i, it in (entry.get("items") or {}).items():
            bad = [k for k, ok in [
                ("id", batch_of.get(i) == b),
                ("llm", it.get("llm") in decisions), ("human", it.get("human") in decisions),
                ("audit", it.get("audit") in {"ok", "problem", None}),
                ("problems", isinstance(it.get("problems"), list) and set(it["problems"]) <= set(PROBLEMS)),
                ("difficulty", isinstance(it.get("difficulty"), list) and len(it["difficulty"]) == 2
                 and all(isinstance(d, int) and lo <= d <= hi for d in it["difficulty"])),
                ("media_changed", isinstance(it.get("media_changed"), bool)),
                ("on", isinstance(it.get("on"), str) and re.fullmatch(r"\d{4}-\d\d-\d\d", it["on"]))] if not ok]
            if bad:
                out.append(f"{rel}: {b}: {i}: bad {', '.join(bad)}")
    return out


def taxonomy_problems():
    """Every bundle's categories file belongs to a bundle; names and slugs are unique across bundles (D-43)."""
    errors, ids = [], categories.bundle_ids()
    if ids[:1] != ["base"]:
        errors.append("app/data/bundles.json: base must come first")
    for p in sorted(layout.app_paths.BUNDLE_DATA.glob("*/categories.json")):
        if p.parent.name not in ids or p.parent.name == "base":
            errors.append(f"{p.relative_to(ROOT)}: no bundle {p.parent.name!r} in app/data/bundles.json")
    for what, items in [("subcategory", categories.subcategories()), ("category slug", [c["slug"] for c in categories.load()])]:
        dup = sorted({x for x in items if items.count(x) > 1})
        if dup:
            errors.append(f"same {what} in two places (D-43): {', '.join(dup)}")
    return errors


def cmd_bundle_new(args):
    """An empty bundle (BN-9, D-41): its entry in app/data/bundles.json and an empty categories.json
    to fill by hand. Concept lists come from `qgen batch --bundle <id>`; axes stay base's until
    authoring/data/bundles/<id>/question-axes.json exists."""
    if not re.fullmatch(r"[a-z0-9-]+", args.id):
        sys.exit("A bundle id is lowercase letters, digits and dashes.")
    data = load_json(layout.BUNDLES)
    if any(b["id"] == args.id for b in data["bundles"]):
        sys.exit(f"Bundle {args.id!r} already exists.")
    data["bundles"].append({"id": args.id, "kind": args.kind, "always_on": False, "name": args.name,
                            "description": args.description, "rule": args.rule})
    save_json(layout.BUNDLES, data)
    path = categories.path(args.id)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"about": f"Categories of the {args.id} bundle (D-41, D-43). Subcategory names "
                                             "and slugs must be unique across all bundles.", "categories": []},
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created bundle {args.id}. Next: fill {path.relative_to(ROOT)} with broad categories and "
          f"subcategories, then `qgen batch --bundle {args.id}`.")


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
    cp = add("concepts", cmd_concepts, "opus", run=False)
    cp.add_argument("--subcategories", help="comma-separated; default: every subcategory without a list")
    cp.add_argument("--top-up", action="store_true", help=f"also add concepts to lists with fewer than {concepts.LOW_STOCK} unused")
    cp.add_argument("--fill", action="store_true", help=f"also top up lists with fewer than {concepts.TARGET_SIZE} concepts to that size")
    cp.add_argument("--bundle", help="without --subcategories: only this bundle's subcategories (default: every bundle)")
    cp.set_defaults(run=None)
    bp = add("bundles", cmd_bundles, "opus", run=False)
    bp.set_defaults(run=None)
    bn = sub.add_parser("bundle", help="manage bundles (D-41)").add_subparsers(dest="action", required=True)
    bnew = bn.add_parser("new", help="create an empty bundle")
    bnew.set_defaults(fn=cmd_bundle_new)
    bnew.add_argument("id")
    bnew.add_argument("--name", required=True, help="Spanish name shown in the game")
    bnew.add_argument("--description", required=True, help="Spanish description shown in the game")
    bnew.add_argument("--kind", required=True, choices=["region", "theme"])
    bnew.add_argument("--rule", required=True, help="one English sentence: when a question belongs in it")
    dp = add("draft", cmd_draft, "opus")
    dp.add_argument("--subcategories", help="comma-separated, first call only")
    dp.add_argument("--seed", type=int, default=1)
    dp.add_argument("--slots", type=int, default=4, help="slots per subcategory")
    dp.add_argument("--bundle", default="base", help="bundle of the run's questions, first call only (D-41)")
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
    rp.add_argument("--bundle", default="base", help="progress vs. targets and saturation for this bundle (plans 12, 14)")
    rp.add_argument("--subcategories", action="store_true",
                    help="supply per subcategory × difficulty, for the jokers (JK-10); saturation flags (plan 14)")
    rp.add_argument("--calibration", nargs="*", metavar="BATCH",
                    help="drafted/rated/final difficulty per target level (plan 13); default: the last two batches")
    rp.add_argument("--batches", nargs="*", metavar="BATCH",
                    help="batch health side by side (plan 15); default: batch-4 onward")
    rp.add_argument("--overlaps", action="store_true",
                    help="approved questions that may ask the same fact (plan 15); listing only")
    rp.add_argument("--exit-check", action="store_true",
                    help="milestone 1's done-when per criterion, ✓/✗; exit 1 if any fails (plan 12)")
    rp.add_argument("--qc", nargs="?", const="", metavar="BATCH",
                    help="rewrite the batch report's Quality control section; without a batch: the trend table (plan 16)")
    rp.add_argument("--changes", help="with --qc <batch>: the report's \"Changes from this QC\" line (QC step 4)")
    add("validate", cmd_validate, run=False)
    add("export", cmd_export, run=False)
    # the LLM batch (D-36): `batch` runs all of these in order; the others are for debugging
    add("media", cmd_media)
    add("sheets", cmd_sheets)
    add("review", cmd_review, REVIEW_MODEL).add_argument("--round", type=int, choices=[1, 2], default=1)
    add("fix", cmd_fix, "opus").add_argument("--check-model", default="sonnet")
    add("research", cmd_research)
    add("record", cmd_record)
    au = add("audit", cmd_audit, "opus", run=False)
    au.add_argument("--batch", help="default: the newest merged batch")
    au.add_argument("--backlog", action="store_true",
                    help="audit the next slice of approved questions from before D-56 (plan 57); only when the gamemaster asks")
    au.add_argument("--slice", type=int, help=f"with --backlog: questions per slice (default {BACKAUDIT_SLICE})")
    au.add_argument("--dry-run", action="store_true", help="with --backlog: list the slice's ids, change nothing")
    add("sync", cmd_sync_run)
    add("batch-report", cmd_batch_report)
    hp = sub.add_parser("health", help="batch health (plan 15)").add_subparsers(dest="action", required=True)
    ha = hp.add_parser("ack", help="the gamemaster has looked at a failing batch: clears the stop of `qgen batch` (D-55)")
    ha.set_defaults(fn=cmd_health_ack)
    ha.add_argument("batch")
    ha.add_argument("note")
    rw = sub.add_parser("rework", help="needs_work questions once more through fix and review (QG-23)")
    rw.set_defaults(fn=cmd_rework)
    rw.add_argument("--batch", help="only this batch's needs_work questions")
    rw.add_argument("--model", choices=["opus", "fable"],
                    help="model for fix and review 1 (default opus; plan 58); review 2 stays opus")
    rw.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    tg = sub.add_parser("tighten", help="find long-winded questions in the whole pool, shorten and review them (QG-24)")
    tg.set_defaults(fn=cmd_tighten)
    tg.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    b = sub.add_parser("batch", help="the whole pipeline for one new batch (authoring/RUNBOOK.md)")
    b.set_defaults(fn=cmd_batch)
    b.add_argument("--bundle", default="base", help="write for this bundle (default base); only when the user names one")
    b.add_argument("--run", help=argparse.SUPPRESS)  # tests and debugging only
    b.add_argument("--subcategories", help=argparse.SUPPRESS)  # tests and debugging only
    b.add_argument("--count", type=int, help=argparse.SUPPRESS)  # default: batches.SHARE of the bundle's subcategories
    b.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    args = ap.parse_args()
    errors = args.fn(args)
    limit = next((e for e in errors if isinstance(e, UsageLimit)), None) if isinstance(errors, list) else None
    if limit:
        print(f"\nStopped: Claude's usage limit ({limit}).\nWait for the reset, then rerun.", file=sys.stderr)
        sys.exit(75)


if __name__ == "__main__":
    main()
