#!/usr/bin/env python3
"""Question pipeline (plans/07-question-generation.md, D-10, D-36). Never ships (D-35).

An LLM makes a batch with exactly one command (authoring/RUNBOOK.md):

    qgen batch                      # writes base questions, in English (D-41, plan 148)
    qgen batch --bundle colombia    # only when the user names a bundle
    qgen batch --translate en [--bundle colombia]   # only when the user names a language (plan 66)

It runs these steps in a fixed order; they stay available one by one for debugging:

    qgen concepts [--subcategories "Volcanes,Piratas"] [--top-up] [--fill]   # concept lists (D-37)
    qgen bundles                    # sort the pool into bundles (D-39)
    qgen bundle new <id> --name … --description … --kind region|theme --language <L> --country <CC> --icon <name> --rule … --voice …   # an empty bundle (D-41)
    qgen taxonomy --bundle <id> [--apply work/taxonomy/<id>/proposal.json]   # a regional or theme bundle's categories (plans 138, 184)
    qgen remap --bundle <id> [--apply work/remap/<id>/proposal.json]   # its questions onto a new taxonomy (plan 138)
    qgen rekey --map work/slugs/proposal.json [--apply]   # category and subcategory keys → English slugs (plan 149); dry run by default
    qgen draft --run <run> --subcategories "Volcanes,Piratas" [--bundle <id>]
    qgen draft | rate | factcheck | dedupe | revise | apply | merge --run <run>
    qgen english-keys               # English answer + concept per non-en source, for en runs' overlap checks (decision 232)
    qgen translate --run <run> [--locale en --ids q-0001,…]   # a translation run's first step (plan 66)
    qgen media | sheets | review [--round 2] | fix | research | record | sync | batch-report --run <run>
    qgen audit [--batch <batch>]    # a second LLM reader of a seeded sample (plan 16); changes nothing
    qgen audit --backlog [--slice N] [--dry-run]   # the next slice of unaudited approved questions from before D-56 (plan 57)
    qgen flag [--dry-run] < reports.txt   # pasted player reports become needs_work reviews (plan 93)
    qgen flag --pull [--url URL] [--dry-run]   # the report server's reports, then acked (token: TRIVIA_REPORT_TOKEN or state/report-token)
    qgen telemetry --pull [--url URL] [--from FILE] [--dry-run]   # opt-in telemetry sessions → state/played/stats.json, then acked (plan 109)
    qgen health ack <batch> <note>  # clears a failing batch's stop of `qgen batch` (D-55)
    qgen rework [--batch <batch>] [--model fable]   # needs_work questions once more through fix and review (QG-23)
    qgen tighten                    # find long-winded questions in the whole pool, shorten and review them (QG-24)
    qgen neutralize [--dry-run]     # reword Colombian usage in base's es-sourced questions into neutral Spanish (plan 64)
    qgen export                     # app/data/pool.json (+ packs' bundles/<id>/pool.json) from authoring/data/questions.json
    qgen report [--run <run>] [--bundle <id>] [--locale <locale>] [--subcategories] [--calibration [<batch>…]]
                [--overlaps] [--batches [<batch>…]] [--exit-check]
    qgen report --qc [<batch> [--changes "<task ids>"]]   # spot check vs. LLM review and audit (plan 16)
    qgen report --simulate [--locale …] [--mode …|all] [--json]   # games per new player; exit 1 below D-75's target (plan 62)
    qgen report --cost [--json]     # $ per approved by run kind, projection per launch language and regional and theme bundle (plan 70)
    qgen report --review-time [--bundle <id>] [--run <run>] [--json]   # review minutes per 100 verdicts (plan 98)
    qgen report --played [--locale es|en|de|all] [--age-group …] [--mode …] [--since YYYY-MM-DD] [--all] [--json]
                                    # played vs. rated difficulty, outliers → /review?played=outliers (plan 109)
    qgen validate
    qgen demo --sizes | --propose [--seats S] | --check [<file>] | --replace   # the demo's question list (plan 174)
    qgen patch-notes [<from-ref> [<to-ref>]] [--out FILE] [--json]   # counts-only notes of a content patch (plan 96)

Writing steps call `claude -p --json-schema` with prompts from authoring/tools/prompts/, in the language of
the questions at hand: a batch's draft_locale (run.json), a merged question's `locale`. Work files
live in work/<run>/ and every step skips what is already done, so a run can be resumed. Every Claude call
goes to work/<run>/calls.jsonl; a command that called Claude ends with a `claude:` totals line (decision 208).

Revising questions that are already in the pool (07, QG-13):

    qgen import --run <run> --batch <batch> [--assign-unbatched]
    qgen rate | factcheck | revise | apply --run <run>
"""
import argparse, atexit, concurrent.futures, datetime, difflib, fcntl, hashlib, json, random, re, subprocess, sys, threading, time, unicodedata
from pathlib import Path
from collections import Counter

import layout  # paths (D-35)
from layout import PROMPTS, REPO as ROOT, SOURCE_POOL as POOL, WORK
import atomic  # authoring/tools/atomic.py: .tmp + replace writes, cross-process locks
import batches  # authoring/tools/batches.py: what the next batch does (D-36)
import concepts  # authoring/tools/concepts.py: concept lists and question axes (D-37)
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import categories  # authoring/tools/categories.py: every bundle's categories (D-19, D-43)
import media_cache as media  # authoring/tools/media_cache.py: the media cache (D-17)
import download  # authoring/tools/download.py: fills the media cache
import media as media_tool  # authoring/tools/media.py: candidates, sheets, picks (`media` is the cache)
import targets  # authoring/tools/targets.py: pool targets (D-53)
import pool_export  # authoring/tools/pool_export.py (D-35)
import patch_notes  # authoring/tools/patch_notes.py: `qgen patch-notes` (plan 96)
import rekey  # authoring/tools/rekey.py: `qgen rekey` (plan 149)
import translations  # authoring/tools/translations.py: translated questions (D-81)
import demo  # authoring/tools/demo.py: `qgen demo` (plan 174)
import played  # authoring/tools/played.py: opt-in telemetry → state/played/ (plan 109)

if __name__ == "__main__":
    sys.modules["qgen"] = sys.modules["__main__"]  # the command modules `from qgen import …` this copy

# Target share per difficulty level (07, "Difficulty target", D-31): what the 12 levels'
# ranges (D-22) show per game, times 3. These are the focus group's (young teens, window 1–10,
# D-38); drafting stops if the focus group's window changes without new weights (AG-8).
# Without a focus, every level of the scale weighs the same (D-40).
LEVEL_WEIGHTS = {1: 12, 2: 6, 3: 10, 4: 16, 5: 20, 6: 23, 7: 14, 8: 14, 9: 16, 10: 13}
RUBRIC = ["correct", "unambiguous", "no_giveaway", "no_overlap", "distractors", "age_fit", "fun", "description"]
# Below 4 on any of these drops a question (07). The soft scores didn't predict the
# developer's decisions in the pilot, so they are recorded but don't filter by default.
# no_overlap (plan 15): asks a fact the pool or an earlier draft already asks; dropped, not revised.
HARD_CRITERIA = ["correct", "unambiguous", "no_giveaway", "no_overlap"]
SOFT_CRITERIA = ["distractors", "age_fit", "fun", "description"]
FACT_FIELDS = ["question", "answer", "wrong_answers", "hints", "fun_fact"]
QUESTION_FIELDS = ["difficulty", "description", *FACT_FIELDS]  # a question's text, in prompt order
REVIEW_URL = "http://127.0.0.1:8001/review"  # trivia-authoring on its default port, in reports
# Why a question is needs_work (plan 15): `review.problems`.
PROBLEMS = ["giveaway", "fact", "ambiguity", "overlap", "media", "difficulty", "style", "other"]


# --- helpers ------------------------------------------------------------------

def load_json(path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"{path}: {e.msg}", e.doc, e.pos) from None

_save_lock = threading.Lock()

def save_json(path, data):
    with _save_lock:
        atomic.write_json(path, data)

slug, norm = concepts.slug, concepts.key

def split_list(text):
    """"a, b,,c" → ["a", "b", "c"] (comma-separated flag values)."""
    return [x.strip() for x in (text or "").split(",") if x.strip()]


def natural_key(s):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)]


def work_runs(pattern, marker):
    """work/<run> names matching `pattern` whose `marker` file exists, oldest first."""
    return sorted((p.parent.name for p in WORK.glob(f"*/{marker}") if re.fullmatch(pattern, p.parent.name)),
                  key=natural_key)


def write_report(run, lines):
    """authoring/reports/<run>.md; returns its path."""
    out = layout.REPORTS / f"{run}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def load_age_groups():
    return load_json(layout.AGE_GROUPS)


def focus_group():
    """The age group the pipeline writes for (D-38); None writes across the whole scale (D-40)."""
    ag = load_age_groups()
    return next((g for g in ag["groups"] if g["id"] == ag["focus"]), None) if ag["focus"] else None


def ages_text(g):
    lo, hi = g["ages"]
    return f"{lo}–{hi}" if hi else f"{lo}+"


VOICE = "idiomatic Latin American Spanish (es-419)"


def load_bundles():
    return load_json(layout.BUNDLES)["bundles"]


def bundles_text():
    """The bundles and their membership rules, for prompts (D-39)."""
    return "\n".join(f"- `{b['id']}`: {b['rule']}" for b in load_bundles())


def voice_locale(b):
    """The locale a bundle's `voice` describes (D-78, plan 98): a regional bundle's drafts; base's and a theme's es text."""
    return translations.draft_locale(b) if b["kind"] == "region" else "es"


def voices_text(locale):
    """The voices of the bundles whose text in `locale` has one, for the locale prompts' {voices} (D-78)."""
    return "\n".join(f"  - `{b['id']}`: {b.get('voice') or VOICE}" for b in load_bundles()
                     if voice_locale(b) == locale) or "  - none"


def bundle_row(bundle):
    return next(b for b in load_bundles() if b["id"] == bundle)


def bundle_text(bundle, locale="es"):
    """The one bundle a batch writes for, as a content limit for the drafter (D-41); its voice for text in its voice's locale."""
    b = bundle_row(bundle)
    voice = f"\nVoice: {b.get('voice') or VOICE}" if locale == voice_locale(b) else ""
    return f"Every question you write is in the `{bundle}` bundle: {b['rule']}{voice}"


def check_bundle(bundle):
    """Exit unless the bundle is in app/data/bundles.json and has subcategories."""
    if bundle not in {b["id"] for b in load_bundles()}:
        sys.exit(f"Unknown bundle {bundle!r}: not in app/data/bundles.json")
    if not categories.subcategories(bundle):
        sys.exit(f"Bundle {bundle!r} has no subcategories yet: fill {categories.path(bundle).relative_to(ROOT)}")


def sub_keys(text, bundle):
    """--subcategories: keys or display names in any locale → the bundle's keys (unknown ones kept as given)."""
    return [categories.resolve(bundle, s) or s for s in split_list(text)]


def named(q, locale):
    """q with its subcategory's display name in the prompt's locale, never the key (decision 259)."""
    return {**q, "subcategory": categories.display(q.get("bundle") or "base", q["subcategory"], locale)}


def not_in_bundle(subs, bundle):
    """The subcategories that aren't in the bundle's categories."""
    known = set(categories.subcategories(bundle))
    return [s for s in subs if s not in known]


def prompt(*names, locale="es", bundle="base", source_locale=None):
    """Prompt files joined; {age_groups} and {players} are filled from app/data/age-groups.json,
    {locale} from prompts/locale-<locale>.md, the language of the questions at hand (else locale-<language>.md;
    + translate-region.md for a regional bundle's translation, decision 167), {voices} from app/data/bundles.json (the
    voices of `locale`), {source_language} from a translation's source locale (plan 148)."""
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
    f = PROMPTS / f"locale-{locale}.md"
    loc = (f if f.exists() else PROMPTS / f"locale-{locale.split('-')[0]}.md").read_text(encoding="utf-8").rstrip()
    b = bundle_row(bundle)
    if b["kind"] == "region" and locale != translations.draft_locale(b):
        loc += "\n\n" + ((PROMPTS / "translate-region.md").read_text(encoding="utf-8").rstrip()
                          .replace("{bundle}", bundle).replace("{rule}", b["rule"]))
    text = text.replace("{locale}", loc)
    if source_locale:
        text = text.replace("{source_language}", LANGUAGES[source_locale])
    return (text.replace("{age_groups}", ", ".join(groups[:-1]) + " and " + groups[-1])
            .replace("{players}", players).replace("{voices}", voices_text(locale)))

def run_dir(args):
    d = WORK / args.run
    d.mkdir(parents=True, exist_ok=True)
    return d

_interrupted = threading.Event()  # Ctrl-C in parallel(): running claude() calls don't retry


def parallel(fn, items, jobs, label="items", unit="items"):
    """Run fn over items, each named in its log lines, with a summary line; report failures without stopping the others.
    Claude's usage limit stops the whole step instead, reported once. Returns the errors."""
    errors, items, limit = [], list(items), []

    def name(x):
        if isinstance(x, tuple) and all(isinstance(p, str) for p in x):
            return "/".join(x)  # (bundle, subcategory)
        return str(x.get("id")) if isinstance(x, dict) else str(x)

    def what(it):
        return (name(it[0]) if isinstance(it, tuple)  # list: grouped() files or a group of questions
                else ", ".join(name(x[0] if isinstance(x, tuple) else x) for x in it)
                if isinstance(it, list) else name(it))

    def run(it):
        with progress.item(label, what(it)):
            return fn(it)

    with progress.Bar(label, len(items), unit) as bar, concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futures = {ex.submit(run, it): it for it in items}
        try:
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
                    progress.fail(f"  FAILED {label} {what(futures[f])}: {progress.short(e, 400)}")
        except KeyboardInterrupt:
            _interrupted.set()
            ex.shutdown(wait=False, cancel_futures=True)
            raise
    if limit:  # the caller reports it (main, cmd_batch)
        return errors + limit
    if errors:
        progress.say(f"{len(errors)} item(s) failed; rerun the same command to retry them.", err=True)
    return errors


def failed(msg):
    """A step's own error (not from parallel()): printed here, returned as the step's errors."""
    progress.fail(f"  FAILED {msg}")
    return [RuntimeError(msg)]


class UsageLimit(RuntimeError):
    """Claude reported a usage or session limit: wait for the reset, then rerun."""


LIMIT_WORDS = ("usage limit", "session limit", "rate limit", "hit your limit")
# "resets 11pm (America/Bogota)", "resets 11:30pm", "resets Oct 9, 3am (Europe/Berlin)"
RESET_RE = re.compile(r"resets\s+(?:(?P<mon>[a-z]{3})[a-z]*\.?\s+(?P<day>\d{1,2}),?\s+(?:at\s+)?)?"
                      r"(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s*(?P<ap>[ap]\.?m\.?)?(?:\s*\((?P<tz>[^)]+)\))?", re.I)
LIMIT_MARGIN = datetime.timedelta(minutes=5)  # resume this long after the reset (QG-21)
EXIT_LIMIT = 75  # exit code: stopped at the usage limit (RUNBOOK)
EXIT_HEALTH = 2  # exit code: batch health stop until `qgen health ack` (D-55, RUNBOOK)


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


CLAUDE_TIMEOUT = 1800  # seconds per `claude -p` call
TOKENS = (("input", "input_tokens", "inputTokens"), ("output", "output_tokens", "outputTokens"),
          ("cache_read", "cache_read_input_tokens", "cacheReadInputTokens"),
          ("cache_write", "cache_creation_input_tokens", "cacheCreationInputTokens"))


def human(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}k" if n >= 1e3 else str(n)


class Calls:
    """This process's Claude calls, summed for the closing `claude:` line (decision 208)."""

    def __init__(self):
        self.lock, self.all = threading.Lock(), []

    def log(self, cwd, model, outcome, out, seconds):
        """One call (attempt) into <cwd>/calls.jsonl and the totals; returns the result line's "$0.84 31k tok"."""
        out = out or {}
        per_model = out.get("modelUsage") or {}
        usage = out.get("usage") or {}
        rec = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
               "step": progress.where()[0], "item": progress.where()[1], "model": model, "outcome": outcome,
               "models": sorted(per_model), "usd": out.get("total_cost_usd"), "turns": out.get("num_turns"),
               "ms": out.get("duration_ms"), "seconds": round(seconds, 1)}
        for key, snake, camel in TOKENS:
            rec[key] = (sum(u.get(camel) or 0 for u in per_model.values()) if per_model
                        else usage.get(snake) if snake in usage else None)
        with self.lock:
            if not self.all:
                atexit.register(self.summary)
            self.all.append(rec)
            with open(Path(cwd) / "calls.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
        tok = sum(rec[k] or 0 for k, *_ in TOKENS)
        return " ".join(([f"${rec['usd']:.2f}"] if rec["usd"] is not None else []) + ([f"{human(tok)} tok"] if tok else []))

    def summary(self):
        """`claude: 112 calls (3 failed, 2 retried), opus 98 / sonnet 14, 412 turns, 4.1M tokens (3.2M cache), $41.20, 2h51m in calls`"""
        with self.lock:
            c = list(self.all)
        if not c:
            return
        n = Counter(r["outcome"] for r in c)
        models = Counter(r["model"] for r in c)
        cache = sum((r["cache_read"] or 0) + (r["cache_write"] or 0) for r in c)
        tok = sum(r[k] or 0 for r in c for k, *_ in TOKENS)
        progress.say(f"claude: {len(c)} calls ({n['failed']} failed, {n['retry']} retried"
                     + (f", {n['limit']} usage limit" if n["limit"] else "") + "), "
                     + " / ".join(f"{m} {k}" for m, k in models.most_common()) + ", "
                     f"{sum(r['turns'] or 0 for r in c)} turns, {human(tok)} tokens ({human(cache)} cache), "
                     f"${sum(r['usd'] or 0 for r in c):.2f}, {progress.duration(sum(r['seconds'] for r in c))} in calls", err=True)


CALLS = Calls()


def claude(system, user, schema, model, cwd, web=False, retries=2, read=False, with_model=False):
    """One fresh `claude -p` session returning structured output (and the model id if asked).
    read=True lets the session open files under cwd with the Read tool (contact sheets).
    Every attempt goes to <cwd>/calls.jsonl and CALLS (decision 208)."""
    cmd = ["claude", "-p", "--output-format", "json", "--no-session-persistence",
           "--model", model, "--system-prompt", system, "--json-schema", json.dumps(schema),
           "--settings", '{"enabledPlugins": {"ponytail@ponytail": false}}']  # coding plugin, not for writing
    if web:
        cmd += ["--tools", "WebSearch,WebFetch", "--allowedTools", "WebSearch", "WebFetch"]
    elif read:
        cmd += ["--tools", "Read", "--allowedTools", "Read"]
    else:
        cmd += ["--tools", ""]
    last = None
    for attempt in range(retries + 1):
        if attempt and _interrupted.is_set():
            break
        with progress.waiting(f"claude {model}") as call:
            t = time.monotonic()
            try:
                p = subprocess.run(cmd, input=user, capture_output=True, text=True, cwd=cwd, timeout=CLAUDE_TIMEOUT)
            except BaseException:  # timeout, Ctrl-C: still a call
                CALLS.log(cwd, model, "failed", None, time.monotonic() - t)
                raise
            seconds = time.monotonic() - t
            more = attempt < retries and not _interrupted.is_set()
            again = f", retry {attempt + 1}/{retries}" if more else ""
            try:
                out = json.loads(p.stdout)
            except json.JSONDecodeError:
                last = f"no JSON from claude (exit {p.returncode}): {p.stderr.strip()[:300] or p.stdout[:300]}"
                call.extra = CALLS.log(cwd, model, "retry" if more else "failed", None, seconds)
                call.result(f"failed (exit {p.returncode}): {progress.short(p.stderr or p.stdout or 'no output')}{again}")
                continue
            if out.get("is_error") or out.get("structured_output") is None:
                last = f"claude error: {str(out.get('result'))[:300]}"
                if any(w in last.lower() for w in LIMIT_WORDS):
                    call.extra = CALLS.log(cwd, model, "limit", out, seconds)
                    call.result("usage limit")
                    raise UsageLimit(last)
                call.extra = CALLS.log(cwd, model, "retry" if more else "failed", out, seconds)
                call.result(f"failed (exit {p.returncode}): {progress.short(out.get('result') or 'no structured output')}{again}")
                continue
            call.extra = CALLS.log(cwd, model, "ok", out, seconds)
        return (out["structured_output"], main_model(out)) if with_model else out["structured_output"]
    raise RuntimeError(last)


def calls(d):
    """Every Claude call logged in the work directory d: calls.jsonl, and costs.log from before task 1134."""
    old, new = d / "costs.log", d / "calls.jsonl"
    cells = [line.split("\t") for line in old.read_text(encoding="utf-8").splitlines()] if old.exists() else []
    return ([{"model": c[0], "usd": None if c[1] in ("None", "") else float(c[1])} for c in cells if len(c) == 2]
            + ([json.loads(line) for line in new.read_text(encoding="utf-8").splitlines() if line.strip()]
               if new.exists() else []))


def costs(d):
    """Dollar amounts of the Claude calls in the work directory d, one per call that reported one."""
    return [c["usd"] for c in calls(d) if c.get("usd") is not None]


# --- schemas ------------------------------------------------------------------

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

_DRAFT_ONLY = {"slot", "option", "needs_fact_check"}
REVISED_SCHEMA = {"type": "object",
                  "required": [k for k in QUESTION_SCHEMA["required"] if k not in _DRAFT_ONLY],
                  "properties": {k: v for k, v in QUESTION_SCHEMA["properties"].items() if k not in _DRAFT_ONLY}}

REVISE_SCHEMA = {"type": "object", "required": ["results"], "properties": {"results": {
    "type": "array", "items": {"type": "object", "required": ["id", "action", "reason", "question"],
        "properties": {"id": STR, "action": {"type": "string", "enum": ["keep", "revise", "drop"]},
                       "reason": STR, "question": REVISED_SCHEMA}}}}}

FACT_SCHEMA = {"type": "object", "required": ["checks"], "properties": {"checks": {
    "type": "array", "items": {"type": "object", "required": ["id", "verdict", "problem", "correction", "sources"],
        "properties": {"id": STR, "verdict": {"type": "string", "enum": ["confirmed", "wrong", "uncertain"]},
                       "problem": STR, "correction": STR, "sources": STR_LIST}}}}}

TRAVEL_REASONS = ["wordplay", "about_language", "needs_local_knowledge", "other"]
TRANSLATE_SCHEMA = {"type": "object", "required": ["items"], "properties": {"items": {
    "type": "array", "items": {"type": "object",
        "required": ["id", "travels", "reason", *translations.TEXT_FIELDS, "notes"],
        "properties": {"id": STR, "travels": {"type": "string", "enum": ["yes", "no"]},
                       "reason": {"type": "string", "enum": ["", *TRAVEL_REASONS]},
                       "question": STR, "answer": STR, "wrong_answers": STR_LIST, "hints": STR_LIST,
                       "description": STR, "fun_fact": STR, "notes": STR}}}}}


# --- steps: concepts, bundles, draft ------------------------------------------

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


def concept_file(bundle, sub):
    """A work file per subcategory: base's by slug, another bundle's prefixed with its id (D-99)."""
    return f"{slug(sub)}.json" if bundle == "base" else f"{bundle}--{slug(sub)}.json"


RELATED_CAP = 60  # base questions a theme subcategory's avoid list and concept calls show (like SAT_ASKED)


def related_text(pool, bundle, sub):
    """The concept calls' "already in the game" section for a theme subcategory; empty without base_related."""
    qs = related_base({"questions": pool}, bundle, sub, "en")
    return ("\n\n## Already in the game (base questions on the same topics: don't list these concepts)\n"
            + "\n".join(f"- {q['answer']} ({q['question'][:80]})" for q in qs)) if qs else ""


def subcategory_header(bundle, sub, locale):
    return (f"## Subcategory\n{categories.display(bundle, sub, locale)} "
            f"(broad category: {categories.category_name(bundle, sub, locale)})")


def cmd_concepts(args):
    """Concept lists (PE-8, D-37): facets and axis fit, then concepts and the concept and axes of
    every existing question; `--top-up` adds concepts to lists running low. Calls run in parallel
    and save raw results in work/concepts/; `finalize_concepts` then writes the lists one by one."""
    d = WORK / "concepts"
    d.mkdir(parents=True, exist_ok=True)
    bundle = getattr(args, "bundle", None)
    if args.subcategories:
        bundle = bundle or "base"
        subs = [(bundle, s) for s in sub_keys(args.subcategories, bundle)]
    elif getattr(args, "run", None):
        run = load_json(WORK / args.run / "run.json")
        bundle = run.get("bundle", "base")
        subs = [(bundle, s) for s in run["subcategories"]]
    else:
        subs = [(c["bundle"], s) for c in categories.load(bundle) for s in c["subcategories"]]
    unknown = [s for b, s in subs if s not in categories.subcategories(b)]
    if unknown:
        sys.exit(f"Not in {bundle}'s categories: {', '.join(unknown)}")
    pool = load_json(POOL)["questions"]
    create = [bs for bs in subs if concepts.load(*bs) is None]

    def make(bs):
        bundle, sub = bs
        path = d / "raw" / concept_file(bundle, sub)
        r = load_json(path, {})
        axes_def = concepts.load_axes(bundle)
        loc = translations.draft_locale(bundle_row(bundle))
        intro = (subcategory_header(bundle, sub, loc) + "\n\n## Bundle\n" + bundle_text(bundle, loc)
                 + "\n\n## Question axes\n" + concepts.axes_text(axes_def))
        if "facets" not in r:
            r.update(claude(prompt("house-style", "concepts-facets", locale=loc, bundle=bundle), intro, facets_schema(axes_def), args.model, d))
            save_json(path, r)
        if "concepts" not in r:
            existing = [{"id": q["id"], "question": q["question"], "answer": q["answer"],
                         "media": f"{q['media']['type']}/{q['media']['role']}"}
                        for q in pool if categories.key(q) == bs]
            user = (intro + "\n\n## Facets\n" + "\n".join(f"- {f}" for f in r["facets"])
                    + "\n\n## Existing questions\n" + (json.dumps(existing, ensure_ascii=False) if existing else "none")
                    + related_text(pool, bundle, sub))
            out = claude(prompt("house-style", "concepts-list", locale=loc, bundle=bundle), user, list_schema(axes_def), args.model, d)
            missing = {q["id"] for q in existing} - {e["id"] for e in out["existing"]}
            if missing:  # untagged questions would make their concepts look unused
                raise RuntimeError(f"{sub}: no concept for {', '.join(sorted(missing))}")
            r.update(out)
            save_json(path, r)
        progress.detail(f"  concepts: {sub}: {len(r['facets'])} facets, {len(r['concepts'])} concepts")

    def wanted(bs):
        """How many concepts a top-up asks for: up to TARGET_SIZE with --fill, else TOP_UP when low."""
        lst = concepts.load(*bs)
        if getattr(args, "fill", False) and len(lst["concepts"]) < concepts.TARGET_SIZE:
            return concepts.TARGET_SIZE - len(lst["concepts"])
        if args.top_up and len(concepts.unused(lst, concepts.uses(pool, *bs))) < concepts.LOW_STOCK:
            return concepts.TOP_UP
        return 0

    def top_up(bs):
        bundle, sub = bs
        path = d / "topup" / concept_file(bundle, sub)
        if path.exists():
            return
        lst = concepts.load(*bs)
        loc = translations.draft_locale(bundle_row(bundle))
        user = (subcategory_header(*bs, loc) + "\n\n## Bundle\n" + bundle_text(bundle, loc) + f"\n\n## How many\nAdd about {wanted(bs)} new concepts."
                + "\n\n## Facets\n" + "\n".join(f"- {f}" for f in lst["facets"])
                + "\n\n## Concepts already in the list\n" + "\n".join(f"- {c['name']} ({c['facet']})" for c in lst["concepts"])
                + related_text(pool, bundle, sub))
        out = claude(prompt("house-style", "concepts-topup", locale=loc, bundle=bundle),
                     user, TOPUP_SCHEMA, args.model, d)
        save_json(path, out)
        progress.detail(f"  top-up: {sub}: {len(out['concepts'])} new concepts")

    bundles = sorted({b for b, _ in subs}, key=categories.bundle_ids().index)
    progress.resumed("concepts", len(subs) - len(create), len(create), "lists")
    errors = parallel(make, create, args.jobs, "concepts", "lists")
    for b in bundles:
        finalize_concepts(d, b)
    topped = [bs for bs in subs if (d / "topup" / concept_file(*bs)).exists()]
    low = [bs for bs in subs if bs not in topped and concepts.load(*bs) and wanted(bs)]
    progress.resumed("top-up", len(topped), len(low), "lists")
    errors += parallel(top_up, low, args.jobs, "top-up", "lists")
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
        lst = concepts.load(bundle, s)
        for c in (lst or {}).get("concepts", []):
            seen.setdefault(concepts.key(c["name"]), s)
    with atomic.locked(POOL):
        data, tagged = load_json(POOL), 0
        by_id = {q["id"]: q for q in data["questions"]}
        for s in order:
            raw, topup = load_json(d / "raw" / concept_file(bundle, s), {}), d / "topup" / concept_file(bundle, s)
            lst, before = concepts.load(bundle, s), None
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
                                                      "unused": len(concepts.unused(lst, concepts.uses(data["questions"], bundle, s)))})
            for e in tags:
                q = by_id.get(e["id"])
                if q is None or categories.key(q) != (bundle, s):
                    continue
                q["concept"] = own[concepts.key(e["concept"])]
                if not concepts.axes_problems(e["axes"], axes_def)[0]:
                    q["axes"] = e["axes"]
                tagged += 1
            concepts.save(bundle, s, lst)
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
    sends new questions and never overwrites a bundle the developer changed afterwards."""
    d = WORK / "bundles"
    d.mkdir(parents=True, exist_ok=True)
    with atomic.locked(POOL):
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
        items = [{k: named(q, translations.source_locale(q))[k] for k in ["id", "subcategory", "question", "answer", "wrong_answers", "hints"]}
                 for q in group]
        user = "## Bundles\n" + bundles_text() + "\n\n## Questions\n" + json.dumps(items, ensure_ascii=False)
        out = claude(system, user, BUNDLE_SCHEMA, args.model, d)
        got = {r["id"]: r for r in out["questions"] if r["bundle"] in ids}
        asked = {q["id"] for q in group}
        unanswered = [q["id"] for q in group if q["id"] not in got]
        with lock:
            proposals.update({i: {"bundle": got[i]["bundle"], "reason": got[i]["reason"], "applied": False}
                              for i in got if i in asked})
            save_json(d / "proposals.json", proposals)
        print(f"  bundles: {group[0]['id']}…{group[-1]['id']}: "
              + ", ".join(f"{b} {sum(1 for i in got if got[i]['bundle'] == b)}" for b in sorted(ids)), flush=True)
        if unanswered:
            raise RuntimeError(f"no bundle for {', '.join(unanswered)}")

    errors = parallel(work, [todo[i:i + BUNDLE_GROUP] for i in range(0, len(todo), BUNDLE_GROUP)],
                      args.jobs, "bundles", "calls")
    with atomic.locked(POOL):
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
    bundle's draft gaps (D-54; base: over the question locales, decision 236), even over the scale
    without any (D-40)."""
    focus = focus_group()
    if focus is None:
        lo, hi = load_age_groups()["scale"]
        deficit = targets.draft_gaps(pool_questions, bundle)
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


TIE_REDRAWS = 5  # draw_slots: redraws of a concept tied to an earlier subcategory's in the run


def draw_slots(subs, pool_questions, axes_def, n, seed, bundle="base", locale="es"):
    """{subcategory: slots} for a run (PE-10): a concept, a target difficulty, up to 3 axis
    combinations and the questions already asked about the concept, per slot. Seeded. `already_asked`:
    the subcategory's questions on the concept plus, from every subcategory and bundle, the non-rejected
    ones a concept probe finds (overlap_candidates rank ≤ 2, decision 350); all in `locale` (as_locale).
    A concept the probe ties to one an earlier subcategory of the run drew is redrawn (TIE_REDRAWS tries);
    still tied, its slot's `already_asked` names the other concept (decision 350 c)."""
    shown = as_locale(pool_questions, locale)
    others = [q for q in shown if q.get("of", q)["status"] != "rejected"]
    cache, taken = {}, []  # taken: probes of earlier subcategories' concepts

    def name_probe(c):
        return {"question": c["name"], "answer": c["name"], "concept": c["name"]}

    def ties(c):
        return [p for p, _, rank in overlap_candidates(name_probe(c), taken, cache, locale) if rank <= 2]
    lists = {s: concepts.load(bundle, s) for s in subs}
    used = {s: concepts.uses(pool_questions, bundle, s) for s in subs}
    levels = assign_difficulties({s: n for s in subs},
                                 {s: [c["known_at"] for c in concepts.unused(lists[s], used[s])] for s in subs},
                                 target_weights(pool_questions, bundle), seed)
    plan = {}
    for s in subs:
        rng = random.Random(f"{seed}:{s}")
        lst = lists[s]
        picked = concepts.draw_concepts(lst, used[s], levels[s], rng)  # scarce levels pick first
        names = {c["name"] for c in picked}
        for i, target in enumerate(levels[s][:len(picked)]):
            tried = set()
            while ties(picked[i]) and len(tried) < TIE_REDRAWS:
                tried.add(picked[i]["name"])
                alt = concepts.draw_concepts({"concepts": [c for c in lst["concepts"] if c["name"] not in names | tried]},
                                             used[s], [target], rng)
                if not alt:
                    break
                names = names - {picked[i]["name"]} | {alt[0]["name"]}
                picked[i] = alt[0]
        tied = {c["name"]: [p["concept"] for p in ties(c)] for c in picked}
        taken += [name_probe(c) for c in picked]
        pairs = list(zip(picked, levels[s]))
        rng.shuffle(pairs)
        usage = concepts.axis_usage(pool_questions, bundle, s)
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
            own = [q for q in shown
                   if categories.key(q) == (bundle, s) and q.get("of", q).get("concept") == c["name"]]
            found = [p for p, _, rank in overlap_candidates(name_probe(c), others, cache, locale) if rank <= 2]
            asked = list(dict.fromkeys(f"{q['question']} → {q['answer']}" for q in own + found))
            asked += [f"(this run, another subcategory: a question about «{t}»)" for t in tied[c["name"]]]
            slots.append({"slot": len(slots), "concept": c["name"], "facet": c["facet"], "target_difficulty": target,
                          "options": [{"option": i, **combo} for i, combo in enumerate(combos, 1)],
                          "already_asked": asked})
        plan[s] = slots
    return plan


def related_base(pool, bundle, sub, locale):
    """A theme subcategory's base_related questions (base-related.json, plan 184), not rejected, in `locale`
    (as_locale), the first RELATED_CAP by id; none without the file or for another kind."""
    rel = (load_json(layout.base_related(bundle), {}) or {}).get("subcategories", {}).get(sub) if bundle != "base" else None
    keys = {("base", r) for r in rel or []}
    qs = sorted((q for q in pool["questions"] if categories.key(q) in keys and q["status"] != "rejected"),
                key=lambda q: q["id"])[:RELATED_CAP]
    return as_locale(qs, locale)


def existing_answers(pool, bundle, sub, locale="es"):
    """The subcategory's own pool questions, all statuses (PE-4), and a theme's base_related ones, in `locale`
    (as_locale); merge's `duplicates()` and the review's `related` list still check the whole pool."""
    own = as_locale([q for q in pool["questions"] if categories.key(q) == (bundle, sub)], locale)
    return sorted({f"{q['answer']} ({q['question'][:60]})" for q in [*own, *related_base(pool, bundle, sub, locale)]})


def cmd_draft(args):
    """Draft questions for the run's slots (PE-10): slots drawn once into slots.json, one call per
    subcategory into drafts/; malformed questions dropped, skips may retire concepts."""
    d = run_dir(args)
    cfg = load_json(d / "run.json")
    if cfg is None:
        if not args.subcategories:
            sys.exit("First call for a run needs --subcategories.")
        check_bundle(args.bundle)
        cfg = {"bundle": args.bundle, "subcategories": sub_keys(args.subcategories, args.bundle),
               "draft_locale": translations.draft_locale(bundle_row(args.bundle))}
        unknown = not_in_bundle(cfg["subcategories"], args.bundle)
        if unknown:
            sys.exit(f"Not in {categories.path(args.bundle).relative_to(ROOT)} (add them there first): {', '.join(unknown)}")
        save_json(d / "run.json", cfg)
    subs, bundle = cfg["subcategories"], cfg.get("bundle", "base")  # runs before D-41 have no bundle
    missing = [s for s in subs if concepts.load(bundle, s) is None]
    if missing:
        sys.exit(f"No concept list for {', '.join(missing)}: run `qgen concepts --bundle {bundle} --subcategories ...` first.")
    pool = load_json(POOL)
    axes_def = concepts.load_axes(bundle)
    locale = text_locale(d)
    plan = load_json(d / "slots.json")
    if plan is None:  # drawn once, so a rerun drafts the same slots
        plan = draw_slots(subs, pool["questions"], axes_def, args.slots, args.seed, bundle, locale)
        save_json(d / "slots.json", plan)
    drawn = Counter(sl["target_difficulty"] for slots in plan.values() for sl in slots)
    print("target difficulty: " + "  ".join(f"{lvl}×{c}" for lvl, c in sorted(drawn.items())), flush=True)
    system = prompt("house-style", "draft", locale=locale, bundle=bundle)
    todo = [s for s in subs if plan.get(s) and not (d / "drafts" / f"{slug(s)}.json").exists()]
    progress.resumed("draft", sum(bool(plan.get(s)) for s in subs) - len(todo), len(todo), "subcategories")

    def work(sub):
        slots = plan[sub]
        shown = {a: {o[a] for sl in slots for o in sl["options"]} for a in concepts.AXES}
        avoid = "\n".join(f"- {a}" for a in existing_answers(pool, bundle, sub, locale)) or "none yet"
        user = (subcategory_header(bundle, sub, locale) + "\n\n## Question axes (the values in these options)\n"
                + concepts.axes_text(axes_def, shown) + "\n\n## Slots\n" + json.dumps(slots, ensure_ascii=False)
                + f"\n\n## Already in the pool for this subcategory (don't repeat these facts)\n{avoid}"
                + "\n\n## Bundle\n" + bundle_text(bundle, locale))
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
        retire(bundle, sub, slots, out["skipped"])
        save_json(d / "drafts" / f"{slug(sub)}.json", {"questions": good, "skipped": out["skipped"]})
        progress.detail(f"  draft: {sub}: {len(good)} written, {len(out['skipped'])} skipped")

    return parallel(work, todo, args.jobs, "draft", "subcategories")


def retire(bundle, sub, slots, skipped):
    """Skips that say a concept is used up or unaskable retire it from its list (PE-10)."""
    why = {slots[x["slot"]]["concept"]: f"{x['retire']}: {x['reason']}" for x in skipped
           if x["retire"] != "no" and 0 <= x["slot"] < len(slots)}
    if not why:
        return
    lst = concepts.load(bundle, sub)
    for c in lst["concepts"]:
        if c["name"] in why:
            c["retired"] = why[c["name"]]
    concepts.save(bundle, sub, lst)
    progress.detail(f"  {sub}: retired {', '.join(why)}")


def option_key(text):
    """norm(), or the casefolded text where norm() drops everything (ß, Ø, Cyrillic)."""
    return norm(text) or unicodedata.normalize("NFKC", text).casefold().strip()


def check_question_shape(q):
    problems = []
    if len(q["wrong_answers"]) != 3: problems.append("needs 3 wrong answers")
    if len(q["hints"]) != 3: problems.append("needs 3 hints")
    lo, hi = load_age_groups()["scale"]
    if not lo <= q["difficulty"] <= hi: problems.append("difficulty out of range")
    if len({option_key(o) for o in [q["answer"], *q["wrong_answers"]]}) != 4: problems.append("duplicate options")
    return problems


def drafts(d):
    """(file stem, questions) per draft file; a translation run's travelling translations as drafts."""
    if run_locale(d):
        yield from translated_drafts(d)
        return
    for f in sorted((d / "drafts").glob("*.json")):
        yield f.stem, load_json(f)["questions"]


# --- steps: rate, fact check, dedupe, merge -----------------------------------

GROUP_SIZE = 10  # questions per rate/revise/fix call and per imported or revised draft file (PE-1, PE-2)


def chunks(items, size=GROUP_SIZE):
    return [items[i:i + size] for i in range(0, len(items), size)]


def locale_chunks(items, size=GROUP_SIZE):
    """chunks() of (q, …) tuples or questions, one text language (and a translation's source locale) per chunk
    (plan 148)."""
    by = {}
    for it in items:
        q = it[0] if isinstance(it, tuple) else it
        by.setdefault((translations.source_locale(q), q.get("source_locale")), []).append(it)
    return [c for its in by.values() for c in chunks(its, size)]


def grouped(files, size=GROUP_SIZE):
    """Pack (name, items) draft files into groups of about `size` items, one call each.
    A file is never split (a draft file is one subcategory); a bigger file is a group of its own."""
    groups, cur, n = [], [], 0
    for name, items in files:
        if cur and (n + len(items) > size or items[:1] and cur[0][1][:1]
                    and items[0].get("source_locale") != cur[0][1][0].get("source_locale")):
            groups.append(cur)
            cur, n = [], 0
        cur.append((name, items))
        n += len(items)
    return groups + [cur] if cur else groups


def for_review(q):
    keys = ["difficulty", "description", "question", "answer", "wrong_answers", "hints", "media", "fun_fact"]
    form = {"axes": q["axes"]} if q.get("axes") else {"style": q.get("style")}  # older drafts have a style
    return {"id": q["tmp_id"], "bundle": q.get("bundle") or "base", **form, **{k: q[k] for k in keys}}


def rate_candidates(d):
    """tmp_id → overlap candidates for `rate` (plan 15): pool questions of every bundle (not rejected)
    and earlier drafts of the run; revised drafts count as later than the first round.
    A translation run: the locale's approved questions (in_locale) instead of the pool. An en run sees the pool
    through English keys (as_locale)."""
    locale, lang = run_locale(d), text_locale(d)
    others = ([q for q in in_locale(locale) if q["status"] == "approved"] if locale
              else as_locale([q for q in load_json(POOL)["questions"] if q["status"] != "rejected"], lang))
    out, cache = {}, {}
    for _, qs in sorted(drafts(d), key=lambda f: (f[0].startswith("revised-"), f[0])):
        for q in qs:
            out[q["tmp_id"]] = [{"id": p.get("id") or p["tmp_id"], "question": p["question"], "answer": p["answer"],
                                 "concept": p.get("concept")}
                                for p in (p.get("of", p) for p, _, _ in overlap_candidates(q, others, cache, lang))
                                if (p.get("id") or p["tmp_id"]) != q["tmp_id"]]
            others.append(q)
    return out


def cmd_rate(args):
    d = run_dir(args)
    files = [(name, qs) for name, qs in drafts(d) if qs]
    todo = [(name, qs) for name, qs in files if not (d / "ratings" / f"{name}.json").exists()]
    progress.resumed("rate", len(files) - len(todo), len(todo), "draft files")
    cands = rate_candidates(d) if todo else {}

    def work(group):
        qs = [q for _, qq in group for q in qq]
        items = [{**for_review(q), "overlap_candidates": cands.get(q["tmp_id"], []),
                  **({"translated_from": LANGUAGES[q["source_locale"]]} if q.get("source_locale") else {})} for q in qs]
        system = prompt("house-style", "rate", locale=text_locale(d), bundle=run_bundle(d),
                        source_locale=qs[0].get("source_locale"))

        def ask(its):
            user = "## Questions\n" + json.dumps(its, ensure_ascii=False)
            return {r["id"]: r for r in claude(system, user, RATE_SCHEMA, args.model, d)["ratings"]}

        got = ask(items)
        lost = [it for it in items if it["id"] not in got]
        if lost:  # the model sometimes skips one item every time; a narrower call rates it
            got |= ask(lost)
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
    if q.get("locale"):  # a translation: translation_needs_check
        return q["needs_fact_check"]
    return bool(q["needs_fact_check"] or re.search(r"\d", q["question"] + q["answer"] + q["fun_fact"]))


def cmd_factcheck(args):
    d = run_dir(args)
    language = LANGUAGES[text_locale(d)]
    _, done = collect(d)  # includes verdicts kept through a revision (PE-3)
    todo, checked = [], 0
    for name, qs in drafts(d):
        need = [q for q in qs if needs_check(q) and q["tmp_id"] not in done]
        checked += sum(needs_check(q) for q in qs) - len(need)
        if need:
            todo.append((name, need))
    progress.resumed("factcheck", checked, sum(len(qs) for _, qs in todo), "questions")

    def work(item):
        name, qs = item
        user = f"## Questions ({language})\n" + json.dumps([for_review(q) for q in qs], ensure_ascii=False)
        system = prompt("factcheck", locale=text_locale(d), source_locale=qs[0].get("source_locale"))
        out = claude(system, user, FACT_SCHEMA, args.model, d, web=True)
        f = d / "factchecks" / f"{name}.json"
        save_json(f, {**load_json(f, {}), **{c["id"]: c for c in out["checks"]}})  # a rerun asks only the missing
        progress.detail(f"  factcheck: {name}: " + ", ".join(c["verdict"] for c in out["checks"]))
        missing = {q["tmp_id"] for q in qs} - {c["id"] for c in out["checks"]}
        if missing:
            raise RuntimeError(f"no fact-check for {', '.join(sorted(missing))}")

    return parallel(work, todo, args.jobs, "factcheck", "calls")


ESSENTIAL_DUP_SIM = 0.4  # floor for the same-essential-media duplicate; below it only the answer matches


def duplicates(q, pool_questions, locale="es"):
    """Return a reason if q duplicates a pool question, else None. pool_questions in q's language
    (`as_locale`).

    Only questions with the same answer can be duplicates: similar wording with a
    different answer is just a shared template ("Escucha: ¿qué … suena?"). Same
    answer counts when the wording is similar too, or both need the same kind of
    essential picture/sound and the wording is at least loosely alike (e.g. two "Mira la foto" questions about
    the Komodo dragon); a short generic answer (Rock, Iron) with unrelated wording is no duplicate.
    """
    qa, qq = overlap_norm(q["answer"], locale), overlap_norm(q["question"], locale)
    if qa.replace(" ", "").isdigit():
        return None
    for p in pool_questions:
        if qa != overlap_norm(p["answer"], locale):
            continue
        sim = difflib.SequenceMatcher(None, qq, overlap_norm(p["question"], locale)).ratio()
        both_essential = (q["media"]["role"] == p["media"]["role"] == "essential"
                          and q["media"]["type"] == p["media"]["type"])
        if sim > 0.6 or both_essential and sim > ESSENTIAL_DUP_SIM:
            p = p.get("of", p)
            return f"like {p.get('id') or p.get('tmp_id')}: {p['question']} → {p['answer']}"
    return None


def overlap_norm(text, locale="es"):
    """norm(); English also without a leading "the", "a", "an"."""
    t = norm(text)
    return re.sub(r"^(?:the|an?) (?=.)", "", t) if locale == "en" else t


def stem(text, locale="es"):
    """overlap_norm() with every word's plural ending dropped. Spanish: trailing «s», then «e»: Almenas → almena,
    padres → padr; German the same (Hunde → hund). English: -ies → y, -es after s/x/z/ch/sh, else -s (not -ss): cities → city, boxes → box."""
    def en(w):
        return (re.sub(r"ies$", "y", w) if w.endswith("ies") else re.sub(r"(s|x|z|ch|sh)es$", r"\1", w)
                if re.search(r"(s|x|z|ch|sh)es$", w) else re.sub(r"(?<!s)s$", "", w))
    return " ".join((en(w) if locale == "en" else re.sub(r"e$", "", re.sub(r"s$", "", w))) if len(w) > 3 else w
                    for w in overlap_norm(text, locale).split())


def keys_hash(q):
    """First 12 hex of sha256 over a source's answer and concept: when its English keys are stale."""
    return hashlib.sha256(json.dumps([q["answer"], q.get("concept")], ensure_ascii=False).encode()).hexdigest()[:12]


def as_locale(questions, locale):
    """The overlap checks' view of pool questions in `locale` (decision 232). Only en changes: sources in another
    language through their en translation's text and the cached English answer and concept (english-keys.json),
    their own concept kept as a key; "of" is the question itself. es and other locales as they are."""
    if locale != "en":
        return questions
    tr = {t["id"]: t for t in translations.load("en")["questions"]}
    keys = (load_json(layout.ENGLISH_KEYS, {}) or {}).get("questions", {})
    out = []
    for q in questions:
        if translations.source_locale(q) == "en" or "id" not in q:
            out.append(q)
            continue
        t, k = tr.get(q["id"]), keys.get(q["id"])
        k = k if k and k["hash"] == keys_hash(q) else None
        out.append({**q, **({f: t[f] for f in ("question", "answer", "fun_fact")} if t else {}),
                    **({"answer": t["answer"] if t else k["answer"], "concept": k["concept"]} if k else {}),
                    "also": q.get("concept"), "of": q})
    return out


ENGLISH_KEYS_SIZE = 250  # sources per english-keys call
ENGLISH_KEYS_SCHEMA = {"type": "object", "required": ["items"], "properties": {"items": {
    "type": "array", "items": {"type": "object", "required": ["id", "answer", "concept"],
                               "properties": {"id": STR, "answer": STR, "concept": STR}}}}}


def cmd_english_keys(args):
    """english-keys.json (decision 232): an English answer and concept per source question in another language (not
    rejected), for as_locale; new or changed ones (keys_hash) asked, gone ones dropped. Before an en batch's rate."""
    pool = [q for q in load_json(POOL)["questions"]
            if q["status"] != "rejected" and translations.source_locale(q) != "en"]
    have = (load_json(layout.ENGLISH_KEYS, {}) or {}).get("questions", {})
    keys = {q["id"]: have[q["id"]] for q in pool if q["id"] in have and have[q["id"]]["hash"] == keys_hash(q)}
    todo = [q for q in pool if q["id"] not in keys]
    progress.resumed("english keys", len(keys), len(todo), "questions")
    lock = threading.Lock()

    def save():
        save_json(layout.ENGLISH_KEYS, {"version": 1, "about": "decision 232: English answer and concept per source "
                                        "question in another language, for the overlap checks (qgen english-keys)",
                                        "questions": dict(sorted(keys.items(), key=lambda kv: natural_key(kv[0])))})

    def work(qs):
        user = "## Items\n" + json.dumps([{"id": q["id"], "answer": q["answer"], "concept": q.get("concept") or ""}
                                          for q in qs], ensure_ascii=False)
        out = claude(prompt("english-keys"), user, ENGLISH_KEYS_SCHEMA, args.model, run_dir(args))
        got = {r["id"]: r for r in out["items"]}
        with lock:
            for q in qs:
                if q["id"] in got:
                    r = got[q["id"]]
                    keys[q["id"]] = {"hash": keys_hash(q), "answer": r["answer"],
                                     "concept": r["concept"] if q.get("concept") else None}
            save()
        missing = [q["id"] for q in qs if q["id"] not in got]
        if missing:
            raise RuntimeError(f"no English keys for {', '.join(missing)}")

    errors = parallel(work, chunks(todo, ENGLISH_KEYS_SIZE), args.jobs, "english keys", "calls") if todo else []
    save()  # also drops stale entries
    return errors


def _overlap_keys(q, cache, locale):
    k = cache.get(id(q))  # id(q) → (q, keys); holding q keeps its id unique
    if k is None:
        keys = [t for t in (q["answer"], q.get("concept"), q.get("also")) if t]
        keys = [t for t in keys if not re.search(r"\d", t) and norm(t) not in {"si", "no", "yes"}]
        k = cache[id(q)] = (q, {
            "answer": overlap_norm(q["answer"], locale) if q["answer"] in keys else None,
            "stems": {stem(t, locale) for t in keys} - {""},
            "text": f" {stem(q['question'] + ' ' + q.get('fun_fact', ''), locale)} ",
            "question": overlap_norm(q["question"], locale)})
    return k[1]


def overlap_candidates(q, others, cache, locale="es", cap=8):
    """[(other, why, rank)] for B-5 (plan 15): questions that may ask the same fact as q, closest first.
    Rank 0 same answer, 1 similar answer, 2 stem-equal concept or answer, 3 one's concept/answer in
    the other's text. Answers with digits and yes/no only match through the concept. q and others in `locale`
    (`as_locale`); one cache per locale."""
    a, found = _overlap_keys(q, cache, locale), []
    for p in others:
        if p is q:
            continue
        b, why, rank = _overlap_keys(p, cache, locale), None, 9
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
            hit = min((s for s in a["stems"] if len(s) >= 4 and f" {s} " in b["text"]), default=None)
            if hit:
                why, rank = f"«{hit}» in its text", 3
            elif hit := min((s for s in b["stems"] if len(s) >= 4 and f" {s} " in a["text"]), default=None):
                why, rank = f"its «{hit}» in this text", 3
        if why:
            found.append((rank, -difflib.SequenceMatcher(None, a["question"], b["question"]).ratio(), p, why))
    found.sort(key=lambda f: f[:2])
    return [(p, why, rank) for rank, _, p, why in found[:cap]]


def collect(d):
    ratings, checks = {}, {}
    for f in (d / "ratings").glob("*.json"): ratings.update(load_json(f))
    for f in (d / "factchecks").glob("*.json"): checks.update(load_json(f))
    if run_locale(d):  # translations that keep the source's facts inherit its check
        for _, qs in drafts(d):
            for q in qs:
                if not q["needs_fact_check"]:
                    checks.setdefault(q["tmp_id"], {"id": q["tmp_id"], "verdict": "confirmed", "problem": "",
                                                    "correction": "", "sources": [], "inherited": True})
    return ratings, checks


def cmd_dedupe(args):
    d = run_dir(args)
    locale = text_locale(d)
    seen = as_locale(load_json(POOL)["questions"], locale)
    for _, qs in drafts(d):
        for q in qs:
            why = duplicates(q, seen, locale)
            if why: print(f"  {q['tmp_id']}: {q['question']} → {q['answer']}\n      {why}")
            seen.append(q)


def soft_score(r):
    return sum(r[k] for k in SOFT_CRITERIA) / len(SOFT_CRITERIA)


def cmd_merge(args):
    d = run_dir(args)
    if run_locale(d):
        return merge_translations(d)
    with atomic.locked(POOL):
        data = load_json(POOL)
        pool = data["questions"]
        ratings, checks = collect(d)
        merged = set(load_json(d / "merged.json", []))
        next_id = max(int(q["id"][2:]) for q in pool) + 1
        added, dropped = [], load_json(d / "dropped.json", [])
        ids = load_json(d / "ids.json", {})  # tmp_id -> pool id, for the review step
        locale = text_locale(d)
        seen = as_locale(pool, locale)  # merged drafts are appended to both
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
                else: reason = (dup := duplicates(q, seen, locale)) and "duplicate " + dup
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
                    **({"locale": locale} if locale != "es" else {}),  # absent = es (decision 235)
                    "background": ({"query": q.get("background_query") or q["media"]["query"], "source_url": None,
                                    "file_url": None, "credit": None} if q["media"]["type"] == "audio" else None),
                }
                next_id += 1
                pool.append(new); added.append(new["id"]); merged.add(tid); ids[tid] = new["id"]
                if seen is not pool: seen.append(new)
        save_json(POOL, data)
    save_json(d / "ids.json", ids)
    save_json(d / "merged.json", sorted(merged))
    save_json(d / "dropped.json", dropped)
    print(f"merged {len(added)} question(s) into {POOL.relative_to(ROOT)}; {len(dropped)} dropped in total (see dropped.json)")


# --- revising pool questions (QG-13) ------------------------------------------

REVISABLE = ["difficulty", "description", "question", "answer", "wrong_answers", "hints", "media", "fun_fact",
             "needs_media", "background"]


def cmd_import(args):
    """Copy a batch's draft/needs_work pool questions into work/<run>/drafts/ for rate/factcheck/revise."""
    d = run_dir(args)
    with atomic.locked(POOL):
        data = load_json(POOL)
        if args.assign_unbatched:
            n = 0
            for q in data["questions"]:
                if q.get("batch") is None:
                    q["batch"] = args.batch
                    n += 1
            save_json(POOL, data)
            print(f"assigned batch {args.batch!r} to {n} question(s) without a batch")
    qs = [q for q in data["questions"] if q.get("batch") == args.batch and q["status"] in ("draft", "needs_work")]
    locales = {translations.source_locale(q) for q in qs}
    if len(locales) > 1:
        sys.exit(f"{args.batch} has questions in {', '.join(sorted(locales))}: one language per run")
    work = []
    for q in qs:
        w = {k: q[k] for k in QUESTION_FIELDS}
        w.update(tmp_id=q["id"], style=q.get("style"), axes=q.get("axes"), concept=q.get("concept"), bundle=q.get("bundle"),
                 subcategory=q.get("subcategory"),
                 media={k: q["media"][k] for k in ["type", "role", "query", "note"]},
                 needs_fact_check=True, needs_media=bool(q.get("needs_media")),
                 background_query=(q.get("background") or {}).get("query", ""),
                 feedback=(q.get("review") or {}).get("feedback") if q["status"] == "needs_work" else None)
        work.append(w)
    files = chunks(work)
    for i, qs in enumerate(files, 1):
        save_json(d / "drafts" / f"chunk-{i:02d}.json", {"questions": qs, "skipped": []})
    save_json(d / "run.json", {"source": "pool", "batch": args.batch, "draft_locale": min(locales, default="es")})
    print(f"imported {len(work)} question(s) into {len(files)} chunk(s)")


DIFFICULTY_GAP = 3  # rater on 1–15: mean |diff| 1.5 at 10–15 (task 30), so only big gaps count


def issues_of(q, r, c):
    """Reasons to revise a question; empty when it looks fine or overlaps (merge drops it).

    Only what the pilot showed to matter (D-16): the developer's feedback, the fact-check,
    the hard criteria, and big difficulty gaps. Low soft scores (fun, distractors…) didn't
    predict the developer's decisions, so they don't trigger a revision.
    """
    out = []
    if r and r.get("no_overlap", 5) < 4:
        return out  # merge drops it; a revision would only ask another fact (plan 15)
    if q.get("feedback"):
        out.append(f"developer feedback: {q['feedback']}")
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
    system = prompt("house-style", "revise", locale=text_locale(d), bundle=run_bundle(d))
    todo, revised = [], 0
    for name, qs in drafts(d):
        if name.startswith("revised-") or (d / "revisions" / f"{name}.json").exists():
            revised += not name.startswith("revised-")
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
    progress.resumed("revise", revised, sum(bool(its) for _, its in todo), "draft files")

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
    new_media = {**q["media"], **new["media"], "note": new["media"]["note"] or None}
    media_changed = any(new_media[k] != q["media"][k] for k in ["type", "query"])
    if media_changed:
        new_media = media_tool.unpicked(new_media)
    old_bg = q.get("background")
    if new_media["type"] == "audio":
        bgq = new.get("background_query") or (q.get("background") or {}).get("query") or new_media["query"]
        new_bg = old_bg if old_bg and old_bg["query"] == bgq else {
            "query": bgq, "source_url": None, "file_url": None, "credit": None}
    else:
        new_bg = None
    proposed = {**{k: new[k] for k in [*QUESTION_FIELDS, "needs_media"]},
                "media": new_media, "background": new_bg}
    previous = {k: q.get(k) for k in REVISABLE if proposed[k] != q.get(k)}
    if "difficulty" in previous and q.get("difficulty_original") is None:
        q["difficulty_original"] = q["difficulty"]
    q.update(proposed)
    q["revision"] = {"action": "revise", "reason": reason, "previous": previous, "revised_on": today}
    searched = {"media": media_changed, "background": bool(old_bg) and new_bg is not old_bg}
    for slot in ("media", "background"):  # stale candidates for a changed search (a note change keeps them)
        if searched[slot]:
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
    with atomic.locked(POOL):
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
                if bad := check_question_shape(new):
                    print(f"  {qid}: revision malformed ({'; '.join(bad)}), skipped")
                    counts["malformed"] += 1
                    continue
                revise_in_pool(q, new, rev["reason"], today)
            if q["status"] == "needs_work":
                q["status"], q["review"] = "draft", None
            counts[rev["action"]] += 1
            applied.add(qid)
        save_json(POOL, data)
    save_json(d / "applied.json", sorted(applied))
    print("applied: " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
          + f". Next: trivia-media fetch --batch {cfg['batch']}")


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
            if bad := check_question_shape(new):
                print(f"  {q['tmp_id']}: revision malformed ({'; '.join(bad)}), kept old")
                counts["malformed"] += 1
                rest.append(q)
                continue
            keys = [*QUESTION_FIELDS, "needs_media", "background_query"]
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
        for i, qs in enumerate(chunks(moved), 1):
            save_json(d / "drafts" / f"revised-{n:02d}-{i}.json", {"questions": qs, "skipped": []})
    save_json(d / "applied.json", sorted(applied))
    print("applied: " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
          + ". Next: rate and factcheck (revised drafts only), then merge")


# --- qgen batch: sync, batch report, orchestration (D-36) ---------------------

def cmd_sync_run(args):
    """Download the run's picked files into the media cache. Rate limits don't fail the batch."""
    missing, broken = [], {}
    picks = [(q["id"], slot, q[slot]["file_url"]) for q in batch_questions(args.run, ("approved", "needs_work"))
             for slot in slots_of(q) if q[slot].get("file_url")]
    todo = [(qid, slot, url) for qid, slot, url in picks if not media.cache_path(url).is_file()]
    progress.resumed("sync", len(picks) - len(todo), len(todo), "files")
    with progress.Bar("sync", len(todo), "files") as bar:
        for qid, slot, url in todo:
            label = qid if slot == "media" else f"{qid} background"
            try:
                with media_tool.downloading("sync", qid, slot, url):
                    problem = download.file_problem(download.cached(url))
                if problem:
                    broken[qid, slot] = problem
                bar.finished()
            except Exception as e:  # noqa: BLE001 — listed in the report; `trivia-media sync` retries
                missing.append(label)
                progress.say(f"  not cached: {label}: {e}", err=True)
                bar.finished(ok=False)
    media_tool.mark_broken(broken)  # approved ones then fail qgen validate (decision 47)
    save_json(run_dir(args) / "not-cached.json", missing)
    return []


def cmd_batch_report(args):
    """authoring/reports/<run>.md: what the batch produced, written by code; also batches.md (plan 15)."""
    import health  # authoring/tools/health.py (imports qgen)
    d = run_dir(args)
    qs = [q for q in load_json(POOL)["questions"] if q.get("batch") == args.run]
    cfg = load_json(d / "run.json", {})
    dropped = load_json(d / "dropped.json", [])
    calls = costs(d) + costs(d / "audit")
    models = sorted({(q.get("review") or {}).get("model") for q in qs} - {None})
    approved = [q for q in qs if q["status"] == "approved"]
    work = [q for q in qs if q["status"] == "needs_work"]
    not_cached = load_json(d / "not-cached.json", [])
    lines = [f"# {args.run}", "",
             f"Made by `qgen batch` on {datetime.date.today().isoformat()} (plans/19-repo-layout.md, D-36). "
             "Generated file: don't edit by hand.", "",
             f"- Bundle: {cfg.get('bundle', 'base')}",
             f"- Language: {LANGUAGES[text_locale(d)]}",
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
    out = write_report(args.run, lines)
    print(f"  report: {out.relative_to(ROOT)}")
    print(f"  report: {health.write_batches_md().relative_to(ROOT)}")
    return []


def next_batch():
    """(run name, resuming?) — an unfinished `qgen batch` run is resumed; otherwise batch-<n+1>."""
    open_runs = batches.unfinished_runs()
    if len(open_runs) > 1:
        sys.exit(f"More than one unfinished batch: {', '.join(open_runs)}. Ask the developer which to finish.")
    if open_runs:
        return open_runs[0], True
    names = {q.get("batch") for q in load_json(POOL)["questions"]} | {p.name for p in WORK.glob("batch-*") if p.is_dir()}
    numbers = [int(m.group(1)) for n in names if n and (m := re.fullmatch(r"batch-(\d+)", n))]
    return f"batch-{max(numbers, default=0) + 1}", False


def run_steps(steps, again, run=None, validate=True):
    """Run (name, fn, args) steps in order, then validate (unless `validate` is false); waits out Claude's usage limit (QG-21).
    Exits EXIT_LIMIT or 1 on a step that fails; `again` is the command that continues. Returns the start time.
    With `run`, adds each step's seconds to run.json's "seconds" (batch health, plan 15)."""
    t0 = time.monotonic()
    total = len(steps) + validate
    i = 0
    while i < len(steps):
        name, fn, a = steps[i]
        i += 1
        print(f"\n== [{i}/{total}] {name}", flush=True)
        progress.failures.clear()
        t = time.monotonic()
        try:
            with progress.item(name, None):
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
            sys.exit(EXIT_LIMIT)
        if errors:
            lines = progress.failures or [str(e) for e in errors]
            print(f"\nFailures in `{name}`" + (f" (last 20 of {len(lines)})" if len(lines) > 20 else "") + ":\n"
                  + "\n".join(f"  {progress.short(x, 300)}" for x in lines[-20:]), file=sys.stderr)
            print(f"\nStopped at `{name}` with {len(errors)} error(s). Run `{again}` again; "
                  "if the same step fails three times in a row, stop and report the output.", file=sys.stderr)
            sys.exit(1)
    if not validate:
        return t0
    print(f"\n== [{total}/{total}] validate", flush=True)
    errors, _ = validate_pool()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print("\n`qgen validate` failed. Stop and report the output.", file=sys.stderr)
        sys.exit(1)
    return t0


_run_lock = None


def lock_run(d):
    """Hold d/run.lock until the process ends; the OS frees it on a crash. Exits if another qgen holds it."""
    global _run_lock
    d.mkdir(parents=True, exist_ok=True)
    _run_lock = open(d / "run.lock", "w", encoding="utf-8")
    try:
        fcntl.flock(_run_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit(f"{d.name} is in use by another qgen process")


def cmd_batch(args):
    """The whole pipeline in a fixed order (D-36). Rerunning it continues where it stopped."""
    if args.translate:
        return cmd_translate_batch(args)
    if args.ids or args.dry_run:
        sys.exit("--ids and --dry-run need --translate")
    if args.run:
        run, resuming = args.run, (WORK / args.run / "run.json").exists()
    else:
        run, resuming = next_batch()
    d = WORK / run
    lock_run(d)
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
            sys.exit(EXIT_HEALTH)
        check_bundle(args.bundle)
        if args.subcategories:
            subs = sub_keys(args.subcategories, args.bundle)
            unknown = not_in_bundle(subs, args.bundle)
            if unknown:
                sys.exit(f"Not in {categories.path(args.bundle).relative_to(ROOT)}: {', '.join(unknown)}")
        else:
            subs = batches.subcategories(load_json(POOL)["questions"], args.count, args.bundle)  # D-46, D-54
        save_json(d / "run.json", {"mode": "batch", "bundle": args.bundle, "subcategories": subs,
                                   "draft_locale": translations.draft_locale(bundle_row(args.bundle)),
                                   "started": datetime.date.today().isoformat()})
    subs, locale = load_json(d / "run.json")["subcategories"], text_locale(d)
    progress.verbose = False  # one summary per step, no detail line per item (QG-20)
    print(f"{'Resuming' if resuming else 'Starting'} {run} for bundle {args.bundle} in {LANGUAGES[locale]}: {len(subs)} subcategories. "
          "This takes from several minutes to an hour.", flush=True)

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    steps = [
        ("concepts", cmd_concepts, ns(model="opus", subcategories=None, top_up=True)),
        ("draft", cmd_draft, ns(model="opus", seed=1, slots=BATCH_SLOTS, subcategories=None, bundle=args.bundle)),
        *([("english-keys", cmd_english_keys, ns(model="sonnet"))] if locale == "en" else []),
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
    pool_file = layout.POOL_FILE(locale, "base").relative_to(ROOT).as_posix()
    print("Commit exactly this:\n"
          f"  git add authoring/data/questions.json {pool_file} app/data/bundles/ {concept_dir}/ authoring/reports/{run}.md authoring/reports/batches.md"
          + (" authoring/data/english-keys.json" if locale == "en" else "") + "\n"
          f"  git commit -m \"{run}: {len(qs)} {'' if args.bundle == 'base' else args.bundle + ' '}questions, "
          f"{n_ok} approved (qgen batch)\"")


# --- health ack, rework, scans: tighten, neutralize ---------------------------

def cmd_health_ack(args):
    """The developer has looked at a failing batch: clears the stop of `qgen batch` (D-55)."""
    import health  # authoring/tools/health.py (imports qgen)
    if args.batch not in health.batch_runs() + health.translation_runs():
        sys.exit(f"not a merged batch or translation run: {args.batch}")
    a = health.acks()
    a[args.batch] = {"date": datetime.date.today().isoformat(), "note": args.note}
    save_json(layout.HEALTH_ACKS, a)
    print(f"acked {args.batch}; `qgen batch" + (f" --translate {args.batch[3:].rsplit('-', 1)[0]}"
                                                 if args.batch.startswith("tr-") else "") + "` may start the next run")
    print(f"  report: {health.write_batches_md().relative_to(ROOT)}")


# --- export, validate, bundle new (D-35) --------------------------------------

def cmd_export(args):
    pool = load_json(POOL)
    pool_export.write(pool)
    for l in translations.LOCALES:
        if not translations.exported(l, pool):
            continue
        n = Counter(e["bundle"] for e in translations.play_entries(l, pool))
        for b in ["base", *sorted(set(n) - {"base"})]:
            print(f"exported {n[b]} {l} question(s) to {layout.POOL_FILE(l, b).relative_to(ROOT)}")
        if translations.path(l).exists():
            c = translations.counts(l, pool)
            print(f"  {l} translations: {c['stale']} stale, {c['left_out']} left out (source not approved or not translatable)")
    for path in pool_export.demo_exports(pool):
        print(f"exported {len(load_json(path)['questions'])} demo question(s) to {path.relative_to(ROOT)}")



# --- CLI ----------------------------------------------------------------------

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
    cp.add_argument("--bundle", help="the bundle of --subcategories (default base); without them: only this bundle's (default: every bundle)")
    cp.set_defaults(run=None)
    bp = add("bundles", cmd_bundles, "opus", run=False)
    bp.set_defaults(run=None)
    bn = sub.add_parser("bundle", help="manage bundles (D-41)").add_subparsers(dest="action", required=True)
    bnew = bn.add_parser("new", help="create an empty bundle")
    bnew.set_defaults(fn=cmd_bundle_new)
    bnew.add_argument("id")
    bnew.add_argument("--name", required=True, help="name shown in the game, in Spanish (es, es-ES; en and de in names.<locale>.json)")
    bnew.add_argument("--description", required=True, help="description shown in the game, in Spanish like --name")
    bnew.add_argument("--kind", required=True, choices=["region", "theme"])
    bnew.add_argument("--language", choices=translations.LOCALES,
                      help="region: the locale it drafts in, its only `languages` entry until en joins (decision 110); theme: default en")
    bnew.add_argument("--icon", help="not region: the tile's symbol, one of BUNDLE_ICONS (default pin)")
    bnew.add_argument("--country", help="region: its ISO 3166-1 alpha-2 code in capitals, e.g. CO; the game shows its flag")
    bnew.add_argument("--rule", required=True, help="one English sentence: when a question belongs in it")
    bnew.add_argument("--voice", help="English: the language variety of its own text in prompts, e.g. \"British English: …\" "
                      f"(region: required; theme: its es text, default: {VOICE})")
    tx = add("taxonomy", cmd_taxonomy, "opus", run=False)
    tx.add_argument("--bundle", required=True, help="a regional or theme bundle")
    tx.add_argument("--apply", metavar="PROPOSAL", help="write categories.json and names from this proposal.json "
                    "(edited to the developer's answer); no LLM call but the names")
    rk = sub.add_parser("rekey", help="category and subcategory keys → English slugs (plan 149); dry run by default")
    rk.set_defaults(fn=rekey.cmd_rekey)
    rk.add_argument("--map", required=True, type=Path, help="the slug list (decision 258), e.g. work/slugs/proposal.json")
    rk.add_argument("--apply", action="store_true", help="write the files (default: print what would change)")
    rm = add("remap", cmd_remap, "opus", run=False)
    rm.add_argument("--bundle", required=True, help="a regional bundle")
    rm.add_argument("--apply", metavar="PROPOSAL", help="move the questions as this proposal.json says "
                    "(edited if needed); no LLM call but names of new subcategories")
    dp = add("draft", cmd_draft, "opus")
    dp.add_argument("--subcategories", help="comma-separated, first call only")
    dp.add_argument("--seed", type=int, default=1)
    dp.add_argument("--slots", type=int, default=4, help="slots per subcategory")
    dp.add_argument("--bundle", default="base", help="bundle of the run's questions, first call only (D-41)")
    tp = add("translate", cmd_translate, "opus")
    tp.add_argument("--locale", help="new run only: one of " + ", ".join(translations.LOCALES))
    tp.add_argument("--ids", help="new run only: comma-separated source ids")
    add("rate", cmd_rate, "opus")
    add("factcheck", cmd_factcheck, "sonnet")
    add("dedupe", cmd_dedupe)
    add("english-keys", cmd_english_keys, "sonnet", run=False).add_argument(
        "--run", default="english-keys", help="work/<run>/ for the calls log")
    add("merge", cmd_merge).add_argument("--min-score", type=float, default=0,
                                         help="minimum mean of distractors/age_fit/fun/description "
                                              "(default 0: off; the pilot showed it doesn't predict the developer)")
    imp = add("import", cmd_import)
    imp.add_argument("--batch", required=True, help="pool batch to revise")
    imp.add_argument("--assign-unbatched", action="store_true", help="give questions without a batch this batch name first")
    add("revise", cmd_revise, "opus")
    add("apply", cmd_apply)
    rp = add("report", cmd_report, run=False)
    rp.add_argument("--run")
    rp.add_argument("--player", help="with --simulate: strong|typical|both (default both)")
    rp.add_argument("--simulate", action="store_true",
                    help="games per new player until the first repeat on the engine (plan 62, plan 65, information only); exit 1 if a launch language misses D-75's target")
    rp.add_argument("--locale", help="progress vs. targets for this locale (default es); with --simulate: "
                    "comma-separated (default: every question locale, decision 235)")
    rp.add_argument("--bundles", help="with --simulate: comma-separated (default: the locale's first base bundle, packs off)")
    rp.add_argument("--age-group", help="with --simulate: comma-separated (default: all four)")
    rp.add_argument("--mode", help="with --simulate: solo|rr-coop|rr-competitive|timed|all (default solo); "
                    "with --played: one mode (default every mode)")
    rp.add_argument("--players", type=int, help="with --simulate: players in rr-coop, rr-competitive and timed (default 4)")
    rp.add_argument("--seeds", type=int, default=40, help="with --simulate: runs per cell")
    rp.add_argument("--cost", action="store_true",
                    help="$ per run and per approved by run kind, projection per launch language and per regional and theme bundle "
                    "(plan 70, CT-3; plan 98)")
    rp.add_argument("--json", action="store_true", help="with --simulate, --cost, --review-time or --played: JSON on stdout")
    rp.add_argument("--played", action="store_true",
                    help="played vs. rated difficulty from opt-in telemetry, outliers as review candidates (plan 109, "
                    "decision 122); --locale es|en|de|all, --age-group, --mode, --since, --all")
    rp.add_argument("--since", metavar="YYYY-MM-DD", help="with --played: answers received on or after this day")
    rp.add_argument("--all", action="store_true", help=f"with --played: every cell with n ≥ {played.MIN_N}, not only outliers")
    rp.add_argument("--bundle", help="progress vs. targets and saturation for this bundle (default base; plans 12, 14); "
                    "with --review-time: only its verdicts (default every bundle)")
    rp.add_argument("--review-time", action="store_true",
                    help=f"the developer's review minutes per 100 verdicts from reviewed_at (plan 98): mean gap between "
                    f"consecutive verdicts, a gap > {REVIEW_GAP_MIN} min starts a new session; --bundle, --run filter")
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
    pn = sub.add_parser("patch-notes", help="a content patch's notes: added/fixed/dropped per locale and category, "
                        "Steam event drafts (plan 96); counts only")
    pn.set_defaults(fn=patch_notes.cmd_patch_notes)
    pn.add_argument("from_ref", nargs="?", metavar="from-ref", help="default: the newest v* tag")
    pn.add_argument("to_ref", nargs="?", metavar="to-ref", help="default: the working tree")
    pn.add_argument("--out", metavar="FILE", help="also write the Markdown here (default for a tag: work/steam/<tag>/patch-notes.md)")
    pn.add_argument("--json", action="store_true", help="JSON on stdout")
    # the LLM batch (D-36): `batch` runs all of these in order; the others are for debugging
    add("media", cmd_media)
    add("sheets", cmd_sheets)
    add("review", cmd_review, REVIEW_MODEL).add_argument("--round", type=int, choices=[1, 2], default=1)
    add("fix", cmd_fix, "opus").add_argument("--check-model", default="sonnet")
    add("research", cmd_research)
    add("record", cmd_record).add_argument("--jobs", type=int, default=3, help="parallel downloads")
    au = add("audit", cmd_audit, "opus", run=False)
    au.add_argument("--batch", help="default: the newest merged batch")
    au.add_argument("--backlog", action="store_true",
                    help="audit the next slice of approved questions from before D-56 (plan 57); only when the developer asks")
    au.add_argument("--slice", type=int, help=f"with --backlog: questions per slice (default {BACKAUDIT_SLICE})")
    au.add_argument("--dry-run", action="store_true", help="with --backlog: list the slice's ids, change nothing")
    add("sync", cmd_sync_run)
    add("batch-report", cmd_batch_report)
    hp = sub.add_parser("health", help="batch health (plan 15)").add_subparsers(dest="action", required=True)
    ha = hp.add_parser("ack", help="the developer has looked at a failing batch: clears the stop of `qgen batch` (D-55)")
    ha.set_defaults(fn=cmd_health_ack)
    ha.add_argument("batch")
    ha.add_argument("note")
    fl = sub.add_parser("flag", help="pasted player reports (stdin) become needs_work reviews (plan 93)")
    fl.set_defaults(fn=cmd_flag)
    fl.add_argument("--dry-run", action="store_true", help="print the changes, write nothing")
    fl.add_argument("--pull", action="store_true", help="the report server's reports instead of stdin, then ack them")
    fl.add_argument("--url", help="report server for --pull (default: reportUrl in app/desktop/package.json)")
    tm = sub.add_parser("telemetry", help="opt-in telemetry → state/played/stats.json (plan 109)")
    tm.set_defaults(fn=cmd_telemetry)
    tm.add_argument("--pull", action="store_true", help="fold the report server's sessions, then ack them")
    tm.add_argument("--dry-run", action="store_true", help="one page: print counts, write nothing, ack nothing")
    tm.add_argument("--from", dest="from_file", metavar="FILE", help='a {"sessions": [...]} file (or one session) instead of the server, no ack')
    tm.add_argument("--url", help="report server (default: reportUrl in app/desktop/package.json)")
    rw = sub.add_parser("rework", help="needs_work questions once more through fix and review (QG-23)")
    rw.set_defaults(fn=cmd_rework)
    rw.add_argument("--batch", help="only this batch's needs_work questions")
    rw.add_argument("--model", choices=["opus", "fable"],
                    help="model for fix and review 1 (default opus; plan 58); review 2 stays opus")
    rw.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    tg = sub.add_parser("tighten", help="find long-winded questions in the whole pool, shorten and review them (QG-24)")
    tg.set_defaults(fn=cmd_tighten)
    tg.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    nz = sub.add_parser("neutralize", help="reword Colombian usage in base into neutral Spanish (plan 64); only when the developer asks")
    nz.set_defaults(fn=cmd_neutralize)
    nz.add_argument("--dry-run", action="store_true", help="scan only: flagged ids, issues and a cost estimate")
    nz.add_argument("--ids", help=argparse.SUPPRESS)  # debugging: scan only these ids (new run only)
    nz.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    dm = sub.add_parser("demo", help="the demo's question list: size, propose, check (plan 174)")
    dm.set_defaults(fn=demo.main)
    dmx = dm.add_mutually_exclusive_group(required=True)
    dmx.add_argument("--sizes", action="store_true", help="per seat count 1..5: the minimum list size and what binds")
    dmx.add_argument("--propose", action="store_true", help="write work/demo/proposal.json and proposal.md")
    dmx.add_argument("--replace", action="store_true",
                     help="propose the nearest full candidate for every listed id that is no candidate any more")
    dmx.add_argument("--check", nargs="?", const="", metavar="FILE",
                     help="check a list (default authoring/data/demo.json) at its seats; exit 1 on failure")
    dm.add_argument("--seats", type=int, default=1, choices=range(1, 6), help="with --propose: sessions up to S seats")
    b = sub.add_parser("batch", help="the whole pipeline for one new batch (authoring/RUNBOOK.md)")
    b.set_defaults(fn=cmd_batch)
    b.add_argument("--bundle", default="base", help="write for this bundle (default base); only when the user names one")
    b.add_argument("--run", help=argparse.SUPPRESS)  # tests and debugging only
    b.add_argument("--subcategories", help=argparse.SUPPRESS)  # tests and debugging only
    b.add_argument("--count", type=int, help=argparse.SUPPRESS)  # default: batches.SHARE of the bundle's subcategories
    b.add_argument("--jobs", type=int, default=3, help=argparse.SUPPRESS)
    b.add_argument("--translate", metavar="LOCALE", choices=translations.LOCALES,
                   help="translate the bundle's approved questions into this locale (plan 66); only when the user names a language")
    b.add_argument("--dry-run", action="store_true", help="with --translate: print the next run's sources, no LLM calls")
    b.add_argument("--ids", help=argparse.SUPPRESS)  # with --translate: these source ids (tests and debugging only)
    args = ap.parse_args()
    errors = args.fn(args)
    limit = next((e for e in errors if isinstance(e, UsageLimit)), None) if isinstance(errors, list) else None
    if limit:
        print(f"\nStopped: Claude's usage limit ({limit}).\nWait for the reset, then rerun.", file=sys.stderr)
        sys.exit(EXIT_LIMIT)
    if isinstance(errors, list) and any(isinstance(e, Exception) for e in errors):
        sys.exit(1)  # each error was printed where it happened


# the command groups, after every name they import from here
from audit import BACKAUDIT_SLICE, audit_section, cmd_audit
from player_reports import cmd_flag, cmd_telemetry
from report import REVIEW_GAP_MIN, cmd_report, count, qc_section
from review_steps import BATCH_SLOTS, REVIEW_MODEL, batch_questions, cmd_fix, cmd_media, cmd_record, cmd_research, cmd_review, cmd_sheets, slots_of
from rework import cmd_neutralize, cmd_rework, cmd_tighten
from taxonomy import cmd_bundle_new, cmd_remap, cmd_taxonomy
from translate import LANGUAGES, cmd_translate, cmd_translate_batch, in_locale, merge_translations, run_bundle, run_locale, text_locale, translated_drafts
from validate import cmd_validate, validate_pool


if __name__ == "__main__":
    main()