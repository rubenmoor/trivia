#!/usr/bin/env python3
"""Question pipeline (plans/07-question-generation.md, D-10, D-36). Never ships (D-35).

An LLM makes a batch with exactly one command (authoring/RUNBOOK.md):

    qgen batch                      # writes base questions, in English (D-41, plan 148)
    qgen batch --bundle colombia    # only when the user names a bundle
    qgen batch --translate en [--bundle colombia]   # only when the user names a language (plan 66)

It runs these steps in a fixed order; they stay available one by one for debugging:

    qgen concepts [--subcategories "Volcanes,Piratas"] [--top-up] [--fill]   # concept lists (D-37)
    qgen bundles                    # sort the pool into bundles (D-39)
    qgen bundle new <id> --name … --description … --kind region|theme --language <L> --country <CC> --rule … --voice …   # an empty bundle (D-41)
    qgen taxonomy --bundle <id> [--apply work/taxonomy/<id>/proposal.json]   # a regional bundle's categories (plan 138)
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
    qgen report --cost [--json]     # $ per approved by run kind, projection per launch language and regional bundle (plan 70)
    qgen report --review-time [--bundle <id>] [--run <run>] [--json]   # review minutes per 100 verdicts (plan 98)
    qgen report --played [--locale es|en|de|all] [--age-group …] [--mode …] [--since YYYY-MM-DD] [--all] [--json]
                                    # played vs. rated difficulty, outliers → /review?played=outliers (plan 109)
    qgen validate
    qgen patch-notes [<from-ref> [<to-ref>]] [--out FILE] [--json]   # counts-only notes of a content patch (plan 96)

Writing steps call `claude -p --json-schema` with prompts from authoring/tools/prompts/, in the language of
the questions at hand: a batch's draft_locale (run.json), a merged question's `locale`. Work files
live in work/<run>/ and every step skips what is already done, so a run can be resumed. Every Claude call
goes to work/<run>/calls.jsonl; a command that called Claude ends with a `claude:` totals line (decision 208).

Revising questions that are already in the pool (07, QG-13):

    qgen import --run <run> --batch <batch> [--assign-unbatched]
    qgen rate | factcheck | revise | apply --run <run>
"""
import argparse, atexit, concurrent.futures, contextlib, datetime, difflib, hashlib, json, os, random, re, subprocess, sys, threading, time, unicodedata
from pathlib import Path
from collections import Counter

import layout  # paths (D-35)
from layout import PROMPTS, REPO as ROOT, SOURCE_POOL as POOL, WORK
import atomic  # authoring/tools/atomic.py: .tmp + replace writes, cross-process locks
import age_groups  # authoring/tools/age_groups.py: level ranges per group (plan 27)
import batches  # authoring/tools/batches.py: what the next batch does (D-36)
import concepts  # authoring/tools/concepts.py: concept lists and question axes (D-37)
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import categories  # authoring/tools/categories.py: every bundle's categories (D-19, D-43)
import media_cache as media  # authoring/tools/media_cache.py: the media cache (D-17)
import download  # authoring/tools/download.py: fills the media cache
import media as media_tool  # authoring/tools/media.py: candidates, sheets, picks (`media` is the cache)
import providers  # authoring/tools/providers/: where candidates come from (D-45)
import engine  # authoring/tools/engine.py: the TS engine under Node (D-60), e.g. the supply check (GF-5)
import save_file  # authoring/tools/save_file.py: the game's save, read-only (D-59)
import paths  # authoring/tools/paths.py: state/ (TRIVIA_STATE)
import targets  # authoring/tools/targets.py: pool targets (D-53)
import pool_export  # authoring/tools/pool_export.py (D-35)
import patch_notes  # authoring/tools/patch_notes.py: `qgen patch-notes` (plan 96)
import rekey  # authoring/tools/rekey.py: `qgen rekey` (plan 149)
import translations  # authoring/tools/translations.py: translated questions (D-81)
import reviews  # authoring/tools/reviews.py: review writes, player reports (plan 93)
import played  # authoring/tools/played.py: opt-in telemetry → state/played/ (plan 109)

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
           "--model", model, "--system-prompt", system, "--json-schema", json.dumps(schema)]
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
                    + "\n\n## Existing questions\n" + (json.dumps(existing, ensure_ascii=False) if existing else "none"))
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
                + "\n\n## Concepts already in the list\n" + "\n".join(f"- {c['name']} ({c['facet']})" for c in lst["concepts"]))
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


def draw_slots(subs, pool_questions, axes_def, n, seed, bundle="base"):
    """{subcategory: slots} for a run (PE-10): a concept, a target difficulty, up to 3 axis
    combinations and the questions already asked about the concept, per slot. Seeded."""
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
            asked = [f"{q['question']} → {q['answer']}" for q in pool_questions
                     if categories.key(q) == (bundle, s) and q.get("concept") == c["name"]]
            slots.append({"slot": len(slots), "concept": c["name"], "facet": c["facet"], "target_difficulty": target,
                          "options": [{"option": i, **combo} for i, combo in enumerate(combos, 1)],
                          "already_asked": asked})
        plan[s] = slots
    return plan


def existing_answers(pool, bundle, sub):
    """The subcategory's own pool questions, all statuses (PE-4); merge's `duplicates()` and the
    review's `related` list still check the whole pool."""
    return sorted({f"{q['answer']} ({q['question'][:60]})" for q in pool["questions"] if categories.key(q) == (bundle, sub)})


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
    plan = load_json(d / "slots.json")
    if plan is None:  # drawn once, so a rerun drafts the same slots
        plan = draw_slots(subs, pool["questions"], axes_def, args.slots, args.seed, bundle)
        save_json(d / "slots.json", plan)
    drawn = Counter(sl["target_difficulty"] for slots in plan.values() for sl in slots)
    print("target difficulty: " + "  ".join(f"{lvl}×{c}" for lvl, c in sorted(drawn.items())), flush=True)
    locale = text_locale(d)
    system = prompt("house-style", "draft", locale=locale, bundle=bundle)
    todo = [s for s in subs if plan.get(s) and not (d / "drafts" / f"{slug(s)}.json").exists()]
    progress.resumed("draft", sum(bool(plan.get(s)) for s in subs) - len(todo), len(todo), "subcategories")

    def work(sub):
        slots = plan[sub]
        shown = {a: {o[a] for sl in slots for o in sl["options"]} for a in concepts.AXES}
        avoid = "\n".join(f"- {a}" for a in existing_answers(pool, bundle, sub)) or "none yet"
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
    """The picked file's title from its candidates, if they are still cached."""
    found = media_tool.load_candidates(q["id"], slot) or {"candidates": []}
    url = q[slot].get("source_url")
    return next((c["title"] for c in found["candidates"] if url and c.get("page_url") == url), None)


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
                if i in merged:
                    continue
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
        user = "## Questions\n" + json.dumps(items, ensure_ascii=False)
        system = prompt("house-style", "rate", locale=text_locale(d), bundle=run_bundle(d),
                        source_locale=qs[0].get("source_locale"))
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


def duplicates(q, pool_questions, locale="es"):
    """Return a reason if q duplicates a pool question, else None. pool_questions in q's language
    (`as_locale`).

    Only questions with the same answer can be duplicates: similar wording with a
    different answer is just a shared template ("Escucha: ¿qué … suena?"). Same
    answer counts when the wording is similar too, or both need the same kind of
    essential picture/sound (e.g. two "Mira la foto" questions about the Komodo dragon).
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
        if sim > 0.6 or both_essential:
            p = p.get("of", p)
            return f"like {p.get('id') or p.get('tmp_id')}: {p['question']} → {p['answer']}"
    return None


def overlap_norm(text, locale="es"):
    """norm(); English also without a leading "the", "a", "an"."""
    t = norm(text)
    return re.sub(r"^(?:the|an?) (?=.)", "", t) if locale == "en" else t


def stem(text, locale="es"):
    """overlap_norm() with every word's plural ending dropped. Spanish: trailing «s», then «e»: Almenas → almena,
    padres → padr. English: -ies → y, -es after s/x/z/ch/sh, else -s (not -ss): cities → city, boxes → box."""
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
    if new_media["type"] == "audio":
        bgq = new.get("background_query") or (q.get("background") or {}).get("query") or new_media["query"]
        old_bg = q.get("background")
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


# --- qgen report --------------------------------------------------------------

def count(items, key):
    out = {}
    for it in items:
        k = key(it); out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (0, kv[0], "") if isinstance(kv[0], int) else (1, 0, str(kv[0]))))


def report_subcategories(avail, ranges):
    """Supply per subcategory × difficulty (JK-10): where «Bájale» (an easier question of the same
    subcategory) and «Cambiazo» (a subcategory with a question in the level's range) run dry (09)."""
    lo, hi = load_age_groups()["scale"]
    scale = range(lo, hi + 1)
    by_sub = {}
    for q in avail:
        by_sub.setdefault(categories.key(q), []).append(q["difficulty"])
    print("supply per subcategory × difficulty (JK-10; '.' = none):")
    print(f"  {'':34}" + "".join(f"{d:>3}" for d in scale) + "  total")
    for c in categories.load():
        print(f"  {categories.sub_key(c['bundle'], c['slug'])}")
        for sub in c["subcategories"]:
            ds = by_sub.get((c["bundle"], sub), [])
            cells = "".join(f"{ds.count(d) or '.':>3}" for d in scale)
            print(f"    {sub[:32]:32}{cells}  {len(ds):5}{'  EMPTY' if not ds else ''}")
    empty = sum(1 for c in categories.load() for sub in c["subcategories"] if (c["bundle"], sub) not in by_sub)
    easier = sum(1 for q in avail if any(d < q["difficulty"] for d in by_sub[categories.key(q)]))
    print(f"  empty subcategories: {empty}")
    print(f"  «Hada madrina» possible on {easier} of {len(avail)} questions "
          f"({easier * 100 // max(len(avail), 1)} %): an easier one exists in the same subcategory")
    print("  «Doña Exigente» choices per level, young teens (subcategories with a question in the level's range):")
    for level, (lo, hi) in ((int(l), r) for l, r in ranges.items()):
        n = sum(1 for ds in by_sub.values() if any(lo <= d <= hi for d in ds))
        print(f"    level {level:2} (difficulty {lo}–{hi}): {n:3}")


# Saturation check (plan 14): a subcategory is saturated when any of these holds.
HARD_AT = 11  # a "hard" concept: known_at ≥ this
SAT_AFTER_TOP_UP = 36  # unused right after its last top-up (2 batches of 18 slots)
SAT_HARD = 10  # unused hard concepts
SAT_OVERLAP = 0.10  # overlaps / drafts in its last batch
SAT_OVERLAP_MIN = 2  # … and at least this many (one is noise)
SAT_ASKED = 60  # questions in any status = avoid-list length


def bundle_runs(bundle, n=2, done=False):
    """The last n merged `qgen batch` runs of the bundle, oldest first; unfinished ones too unless `done`."""
    import health  # authoring/tools/health.py (imports qgen)
    def ok(run):
        cfg = load_json(WORK / run / "run.json", {}) or {}
        return cfg.get("bundle", "base") == bundle and (cfg.get("done") or not done)
    return [r for r in health.batch_runs() if ok(r)][-n:]


def saturation(pool, bundle):
    """{subcategory: row} of the bundle (plan 14): counts, concept supply, overlaps of its last two
    batches and the saturation flags; `list` None = no concept list yet (never saturated)."""
    import health  # authoring/tools/health.py (imports qgen)
    runs = bundle_runs(bundle)
    ovl = [health.overlaps_by_subcategory(r, pool) for r in runs]
    rows = {}
    for sub in categories.subcategories(bundle):
        qs = [q for q in pool if categories.key(q) == (bundle, sub)]
        lst = concepts.load(bundle, sub)
        r = {"approved": sum(q["status"] == "approved" for q in qs), "asked": len(qs), "list": None,
             "unused": None, "hard": None, "top_ups": 0, "overlaps": 0, "drafts": 0, "flags": []}
        for o in ovl:
            r["overlaps"] += o.get(sub, [0, 0])[0]
            r["drafts"] += o.get(sub, [0, 0])[1]
        last = next((o[sub] for o in reversed(ovl) if sub in o), None)  # its last batch
        if lst is not None:
            free = concepts.unused(lst, concepts.uses(pool, bundle, sub))
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
        print(f"  {c['slug']}")
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
        print(f"  {c['slug'][:32]:32}  {len(rs):13}  {sum(r['approved'] for r in rs):8}  "
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
    bundle = (load_json(d / "run.json", {}) or {}).get("bundle", "base")
    rows = {}
    row = lambda lvl: rows.setdefault(lvl, {"slots": 0, "known_at": [], "drafted": [], "rated": [], "final": [],
                                            "merged": 0, "approved": 0})
    for sub, slots in plan.items():
        known = {c["name"]: c["known_at"] for c in (concepts.load(bundle, sub) or {"concepts": []})["concepts"]}
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
    return work_runs(r"batch-\d+", "slots.json")[-n:]


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
    en = [q for q in pool if translations.source_locale(q) == "en"]
    rest, cache, en_cache = [q for q in pool if translations.source_locale(q) != "en"], {}, {}
    seen = as_locale(rest, "en")  # an en question against everything else, through English keys
    pairs = [(p, q, why, rank) for i, q in enumerate(rest) for p, why, rank in overlap_candidates(q, rest[:i], cache)]
    for q in en:
        pairs += [(p.get("of", p), q, why, rank) for p, why, rank in overlap_candidates(q, seen, en_cache, "en")]
        seen.append(q)
    pairs = sorted(((rank, p["id"], q["id"], p, q, why) for p, q, why, rank in pairs), key=lambda x: x[:3])
    print(f"{len(pairs)} overlap candidate pair(s) among {len(pool)} approved questions, strongest first:")
    for *_, p, q, why in pairs:
        print(f"  {p['id']} / {q['id']}  {why}: {p['answer']} | {q['answer']}\n"
              f"      {p['question']}\n      {q['question']}")


def report_progress(pool, bundle, locale="es"):
    """Approved vs. targets per difficulty and per broad category (plan 12), per locale (decision 37);
    quiet without targets."""
    t = targets.load_targets(bundle)
    if t is None:
        return
    approved = targets.approved_entries(pool, bundle, locale)
    print(f"progress vs. targets ({bundle}, {locale}):")

    def line(label, n, goal):
        pct = f"{100 * n / goal:3.0f}%" if goal else "   –"
        miss = f"  missing {goal - n}" if n < goal else ""
        print(f"  {label}: {n:4} / {goal:4}  {pct}{miss}")
    by_diff = Counter(q["difficulty"] for q in approved)
    for d, goal in sorted(t["difficulty"].items()):
        line(f"difficulty {d:2}", by_diff[d], goal)
    line("total        ", len(approved), t["total"])
    broad = categories.broad_of()
    by_cat = Counter(broad[categories.key(q)]["slug"] for q in approved if categories.key(q) in broad)
    shares = targets.category_shares(bundle)
    w = max(map(len, shares), default=0)
    print("  per broad category (derived share, guide only):")
    for slug, share in shares.items():
        line(f"  {slug:{w}}", by_cat[slug], round(share))
    if bundle == "base":
        report_supply(pool, locale)


def report_supply(pool, locale):
    """English drafting for base (plan 70, decision 236): per question locale its deficit, yield, untranslated
    sources and the drafts it asks for, per level; the draft gap = the largest."""
    supply = targets.source_supply(pool)
    fmt = lambda d: ", ".join(f"{l}: {n}" for l, n in sorted(d.items()) if n) or "none"
    print("en drafting for base (decision 236; per level; drafts = deficit / yield − untranslated, en 1:1):")
    for l, x in supply.items():
        if locale in (l, "es"):
            gap = {lvl: targets.locale_gap(x, lvl) for lvl in x["deficit"]}
            print(f"  {l}: yield {x['yield']:.2f}; deficit {fmt(x['deficit'])}; untranslated {fmt(x['untranslated'])}; "
                  f"drafts {fmt(gap)}")
    print(f"  draft gap (largest over {', '.join(supply)}): {fmt(targets.draft_gaps(pool, 'base', supply) or {})}")


def spot_agreement(batch, checks):
    """(decided, agreed) of the batch's spot check: agree = both accept or both don't (plan 16)."""
    items = [i for i in (checks.get(batch) or {}).get("items", {}).values() if i.get("human")]
    return len(items), sum((i["llm"] == "approved") == (i["human"] == "approved") for i in items)


def spot_passes(n, agreed, quality):
    """The release bar on a spot check (D-79): enough decided, enough agreement."""
    return n >= quality["spot_check_size"] and agreed >= quality["min_agreement"] * n


def qc_stats(batch, checks):
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
            "passes": None if not q or not n else spot_passes(n, agreed, q),
            "items": items}


def release_failures(s):
    """Failed limits of the release bar (D-79 = D-56's numbers); [] = release-ready."""
    q, n = targets.load_quality(), s["human_n"]
    if not q:
        return ["no quality keys in targets.json"]
    if not n:
        return ["no spot check"]
    out = [f"spot check {n} < {q['spot_check_size']}"] if n < q["spot_check_size"] else []
    if s["agreed"] < q["min_agreement"] * n:
        out.append(f"agreement {100 * s['agreed'] / n:.0f} % < {100 * q['min_agreement']:.0f} %")
    return out


def qc_pct(n, of):
    return f"{n} of {of} ({100 * n / of:.0f} %)" if of else "–"


QC_CHANGES = "Changes from this QC: "


def qc_section(batch, pool=None):
    """The batch report's "## Quality control" (plan 16): spot check vs. LLM review and audit; [] without a spot check.
    Keeps the report's "Changes from this QC" line (QC step 4, `--changes`)."""
    checks = load_json(layout.SPOT_CHECKS, {}) or {}
    if not (checks.get(batch) or {}).get("items"):
        return []
    pool = pool if pool is not None else run_questions(batch)
    by_id = {q["id"]: q for q in pool}
    s, q = qc_stats(batch, checks), targets.load_quality()
    n = s["human_n"]
    verdict = "" if s["passes"] is None else (
        f" {'✓' if s['passes'] else '✗'} (bar: ≥ {q['spot_check_size']} questions, ≥ {100 * q['min_agreement']:.0f} %)")
    lines = ["## Quality control", "",
             "The developer's blind spot check (`/review?batch=…&sample=1`) against the LLM review and the audit "
             "(plan 16, `qgen report --qc`). Agree = both accept or both don't.", "",
             f"- Spot check: {n} decided of {checks[batch].get('size', '?')}",
             f"- Agreement with the LLM review: {qc_pct(s['agreed'], n)}{verdict}",
             "- Release bar (D-79): " + ("✓ release-ready" if not (fail := release_failures(s))
                                         else "✗ not release-ready: " + ", ".join(fail) + " (→ QC step 4)"),
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
                         f"{': ' + fb if fb else ''} ({REVIEW_URL}/{i})")
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
                                                             *WORK.glob("backaudit-*/audit/q-*.json"),
                                                             *WORK.glob("neutralize-*/audit/q-*.json"),
                                                             *WORK.glob("tr-*/audit/q-*.json")])},
                  key=lambda r: (1, int(r[6:])) if re.fullmatch(r"batch-\d+", r) else (0, natural_key(r)))
    if not runs:
        return []
    pool = pool if pool is not None else load_json(POOL)["questions"]
    cols = [qc_stats(r, checks) for r in runs]
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
    src = {x["id"]: translations.source_locale(x) for x in pool}

    def source(r):
        """The run's source locale(s): its ids' (backaudit, tr-*) or its drafts' (plan 147); tr-*: → target."""
        cfg = load_json(WORK / r / "run.json", {}) or {}
        loc = "/".join(sorted({src[i] for i in cfg.get("ids") or [] if i in src})) or text_locale(WORK / r)
        return f"{loc} → {cfg['locale']}" if cfg.get("locale") else loc
    return ["| metric | " + " | ".join(runs) + " |", "|---|" + "---:|" * len(runs),
            "| source locale | " + " | ".join(map(source, runs)) + " |",
            *[f"| {k} | " + " | ".join(f(s) for s in cols) + " |" for k, f in rows],
            f"| **release** ({bar}, D-79) | " + " | ".join("✗ " + ", ".join(f) if (f := release_failures(s)) else "✓"
                                                            for s in cols) + " |"]


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
    runs = bundle_runs(bundle, done=True)
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
            ok &= spot_passes(n, agreed, quality)
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


SIM_MODES = ["solo", "rr-coop", "rr-competitive", "timed"]  # D-74, without gamemaster; = sim/simulate.ts (engine MODES)
SIM_MULTI = {"rr-competitive", "timed"}


def locale_pool(locale):
    """pool.<locale>.json; es falls back to pool.json (as sim/load.ts)."""
    own = layout.LOCALE_POOL(locale)
    return layout.EXPORT if locale == "es" and not own.exists() else own


def target_check(locale, pool=None):
    """D-75: the locale's approved base questions vs. base's targets (decision 37)."""
    pool = pool if pool is not None else load_json(POOL)["questions"]
    t = targets.load_targets("base")
    by = targets.approved_by_level(pool, "base", locale)
    short = targets.deficits(pool, "base", locale) or {}
    short = {d: n for d, n in short.items() if n}
    n = sum(by.values())
    return {"locale": locale, "ok": n >= t["total"] and not short, "approved": n, "total": t["total"], "short": short}


def report_simulate(args):
    """Games per new player until the first repeat (plan 62, CT-2; plan 65), information only; exit code = D-75's target check."""
    locales = args.locale.split(",") if args.locale else translations.LOCALES
    bundles = load_json(layout.BUNDLES)["bundles"]
    default = {l: [next((b["id"] for b in bundles if b.get("kind") == "base" and l in b.get("languages", [])), "base")]
               for l in locales}  # the locale's default game: its first base bundle, packs off (D-99)
    modes = SIM_MODES if args.mode == "all" else (args.mode or "solo").split(",")
    groups = args.age_group.split(",") if args.age_group else [g["id"] for g in load_age_groups()["groups"]]
    player = args.player or "both"
    if player not in ("strong", "typical", "both") or set(modes) - set(SIM_MODES):
        sys.exit(f"--simulate: --player strong|typical|both, --mode {'|'.join(SIM_MODES)}|all")
    models = ["strong", "typical"] if player == "both" else [player]
    cells = [{"locale": l, "bundles": args.bundles.split(",") if args.bundles else default[l],
              "mode": m, "players": (args.players or 4) if m in SIM_MULTI else 1, "age_group": g, "player": p,
              "seeds": args.seeds}
             for l in locales for m in modes for g in groups for p in models]
    t0 = time.monotonic()
    have = [c for c in cells if locale_pool(c["locale"]).exists()]
    with concurrent.futures.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        done = dict(zip(map(id, have), ex.map(engine.simulate, have)))
    results = [done.get(id(c)) or {**c, "result": "no_pool"} for c in cells]
    pool = load_json(POOL)["questions"]
    checks = [target_check(l, pool) for l in locales]
    ok = all(c["ok"] for c in checks)
    if args.json:
        print(json.dumps({"model": {"typical_p": engine_model(results)}, "seconds": round(time.monotonic() - t0, 1),
                          "cells": results, "target": checks, "ok": ok}, ensure_ascii=False))
        sys.exit(0 if ok else 1)
    lo, hi = engine_model(results) or (None, None)
    cap = next((r["max_games"] for r in results if r.get("result") == "ok"), None)
    print(f"games per new player until the first repeat (plan 62, plan 65, information only, D-75); {args.seeds} seeds "
          f"per cell, each stops at the first game that offers a seen card or after {cap} games; {time.monotonic() - t0:.0f} s")
    print(f"  models: strong = always right; typical = p(right) {lo} at level 1 → {hi} at level 12; "
          "standard jokers once each at a random level; rr-competitive (a game = a round), timed modelled until MD-8/MD-9")
    print("  median/p10/bound: games until the first repeat (bound = min over seeds, strong only); exigente: seeds whose "
          "first repeat was a Doña Exigente card; draw: games until a level draw repeats (median/bound); k = the engine's "
          "fresh games left for a fresh profile (supply outlook), a cross-check of the draw bound")
    rows = [("locale", "bundles", "mode", "n", "age group", "player", "median", "p10", "bound", "exigente", "draw", "k",
             "first draw repeat")]
    for r in results:
        head = (r["locale"], ",".join(r["bundles"] or []), r["mode"], str(r["players"]), r["age_group"], r["player"])
        if r["result"] != "ok":
            if rows[-1][0] != r["locale"]:
                rows.append(head[:2] + ("",) * 4 + ("no pool",) + ("",) * 6)
            continue
        g, d, b = r["games"], r["draw"], r["repeat"]
        strong = r["player"] == "strong"
        if b is None:
            where = f"none in {cap} games"
        else:
            rng = f"{b['lo']}" if b["lo"] == b["hi"] else f"{b['lo']}–{b['hi']}"
            dry = ", ".join(categories.labelled(k, r["locale"]) for k in b["dry"])
            where = f"level {b['level']} (difficulty {rng}): {dry or '–'}"
        if d["capped"]:
            where += f"; {d['capped']} seeds capped"
        rows.append(head + (f"{g['median']:g}", f"{g['p10']:g}", str(g["min"]) if strong else "–", str(g["cambiazo"]),
                            f"{d['median']:g}" + (f"/{d['min']}" if strong else ""), str(r["k"]), where))
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]) - 1)]
    for row in rows:
        print("  " + "  ".join(c.ljust(w) for c, w in zip(row, widths)) + "  " + row[-1])
    print("target check (D-75, decision 37: approved base questions per launch language vs. base's targets):")
    for c in checks:
        short = ", ".join(f"{d}: −{n}" for d, n in c["short"].items())
        print(f"  {'✓' if c['ok'] else '✗'} {c['locale']}: {c['approved']}/{c['total']} approved"
              + (f"; short at difficulty {short}" if short else ""))
    sys.exit(0 if ok else 1)


RUN_KINDS = [("batch", r"batch-\d+"), ("translation", r"tr-[A-Za-z-]+-\d+"), ("rework", r"rework-\d+"),
             ("tighten", r"tighten-\d+"), ("neutralize", r"neutralize-\d+"), ("concepts", r"concepts")]


def run_kind(run):
    return next((k for k, p in RUN_KINDS if re.fullmatch(p, run)), "other")


def cost_runs(pool):
    """Every work/<run> with Claude calls (plan 70, CT-3): $ of the run and of its audit/, approved; and what was skipped.
    `locale`: a batch's draft locale, a translation's target."""
    import health  # authoring/tools/health.py (imports qgen)
    status = {q["id"]: q["status"] for q in pool}
    merged = set(health.batch_runs())
    runs, skipped = [], []
    for d in sorted((p for p in WORK.iterdir() if p.is_dir()), key=lambda p: natural_key(p.name)):
        run, kind = d.name, run_kind(d.name)
        own, audit = costs(d), costs(d / "audit")
        if not own and not audit:
            skipped.append(f"{run}: no calls.jsonl or costs.log")
            continue
        approved, locale = None, None
        bundle = (load_json(d / "run.json", {}) or {}).get("bundle", "base") if kind in ("batch", "translation") else None
        if kind == "batch":
            locale = text_locale(d)
            if run in merged:
                approved = health.batch_health(run, pool)["approved"]
            else:
                skipped.append(f"{run}: not merged yet, left out of the rates")
        elif kind == "translation":
            locale = translations.run_locale(run)
            approved = sum(t.get("batch") == run and t.get("status") == "approved"
                           for t in translations.load(locale)["questions"])
        elif ids := (load_json(d / "run.json", {}) or {}).get("ids"):
            approved = sum(status.get(i) == "approved" for i in ids)
        elif any(q.get("batch") == run for q in pool):
            approved = sum(q.get("batch") == run and q["status"] == "approved" for q in pool)
        runs.append({"run": run, "kind": kind, "bundle": bundle, "locale": locale, "calls": len(own) + len(audit), "cost": sum(own),
                     "audit": sum(audit), "approved": approved, "merged": kind != "batch" or run in merged,
                     "per_approved": sum(own) / approved if approved else None})
    have = {r["run"] for r in runs}
    for b in sorted({q.get("batch") for q in pool} - have - {None}, key=natural_key):
        if not (WORK / b).is_dir():
            skipped.append(f"{b}: in the pool, no work/{b} (cost unknown)")
    return runs, skipped


def cost_report(pool):
    """{runs, rates, projection, skipped} for `qgen report --cost` (plan 70, CT-3)."""
    runs, skipped = cost_runs(pool)
    rated = lambda rs: (sum(r["cost"] for r in rs) / n if (n := sum(r["approved"] or 0 for r in rs)) else None)
    batches = [r for r in runs if r["kind"] == "batch" and r["merged"]]
    last3 = {l: [r for r in batches if r["locale"] == l][-3:] for l in translations.LOCALES}
    tr = {l: [r for r in runs if r["kind"] == "translation" and r["locale"] == l] for l in translations.LOCALES}
    batch_cost = sum(r["cost"] for r in batches)
    overhead = sum(r["cost"] + r["audit"] for r in runs if r["kind"] not in ("batch", "translation")) \
        + sum(r["audit"] for r in batches)
    ratio = overhead / batch_cost if batch_cost else None
    rates = {"draft": {l: rated(rs) for l, rs in last3.items() if rs},
             "draft_runs": {l: [r["run"] for r in rs] for l, rs in last3.items() if rs}, "batch_cost": batch_cost,
             "overhead_cost": overhead, "overhead_ratio": ratio,
             "translation": {l: rated(rs) for l, rs in tr.items()}}
    budget = targets.load_all().get("budget") or {}
    spent = {l: sum(r["cost"] + r["audit"] for r in batches + tr[l] if r["locale"] == l) for l in translations.LOCALES}
    draft = "en"  # base's draft locale (decision 236)
    en_rate = rates["draft"].get(draft, rates["draft"].get("es"))  # es batches' rate until an en batch is merged
    gaps = targets.draft_gaps(pool, "base") or {}
    drafts = sum(gaps.values())
    drafting = {"locale": draft, "count": drafts, "per_approved": en_rate,
                "note": None if draft in rates["draft"] else "es batches' rate",
                "cost": drafts * en_rate * (1 + (ratio or 0)) if en_rate is not None else None}
    projection = []
    for l in translations.LOCALES:
        deficit = sum((targets.deficits(pool, "base", l) or {}).values())
        n = max(0, deficit - drafts) if l == draft else deficit  # translations still needed
        rate = rates["translation"][l]
        projection.append({"locale": l, "deficit": deficit, "translations": n, "per_approved": rate,
                           "cost": n * rate * (1 + (ratio or 0)) if rate is not None else 0 if not n else None,
                           "note": None if tr[l] or not n else "no pilot yet", "spent": spent[l], "budget": budget.get(l)})
    by_bundle = bundle_costs(pool, runs, rates, ratio)
    return {"runs": runs, "rates": rates, "projection": projection, "bundles": by_bundle, "drafting": drafting,
            "skipped": skipped}


def bundle_costs(pool, runs, rates, ratio):
    """Rows per regional bundle × es, en (decision 110; base is the projection): $ per approved of its --bundle
    and --translate --bundle runs, deficit to its target, projection; no own run yet → base's rate."""
    rows = []
    for b in load_bundles():
        if b.get("kind") != "region":
            continue
        for l in ["es", "en"]:
            own = [r for r in runs if r["bundle"] == b["id"] and r["merged"]
                   and (r["kind"] == "batch" if l == "es" else r["locale"] == l)]
            n = sum(r["approved"] or 0 for r in own)
            rate = sum(r["cost"] for r in own) / n if n else None
            use = rate if rate is not None else rates["draft"].get("es") if l == "es" else rates["translation"].get(l)
            deficit = sum((targets.deficits(pool, b["id"], l) or {}).values())
            rows.append({"bundle": b["id"], "locale": l, "runs": [r["run"] for r in own], "approved": n,
                         "cost": sum(r["cost"] + r["audit"] for r in own), "per_approved": rate, "deficit": deficit,
                         "projection": deficit * use * (1 + (ratio or 0)) if use is not None else None,
                         "base_rate": rate is None and use is not None})
    return rows


def report_cost(args):
    r = cost_report(load_json(POOL)["questions"])
    if args.json:
        return print(json.dumps(r, ensure_ascii=False))
    usd = lambda x: "–" if x is None else f"${x:.2f}"
    print("cost per run (plan 70, CT-3; work/*/calls.jsonl or costs.log at list price; $/approved = the run's own log, as batches.md)")
    rows = [("run", "kind", "calls", "$", "audit $", "approved", "$/approved")]
    rows += [(x["run"], x["kind"] + (f" {x['locale']}" if x["locale"] else ""), str(x["calls"]), usd(x["cost"]),
              usd(x["audit"]) if x["audit"] else "–", "–" if x["approved"] is None else str(x["approved"]),
              usd(x["per_approved"])) for x in r["runs"]]
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    for row in rows:
        print("  " + "  ".join(c.ljust(w) if i < 2 else c.rjust(w) for i, (c, w) in enumerate(zip(row, widths))))
    k = r["rates"]
    print("per kind:")
    for l, v in k["draft"].items():
        print(f"  draft {l}: {usd(v)} per approved ({', '.join(k['draft_runs'][l])}, weighted by approved)")
    if not k["draft"]:
        print("  draft: no merged batch")
    for l, v in k["translation"].items():
        print(f"  translation {l}: " + (f"{usd(v)} per approved" if v is not None else "no tr-" + l + "-* run yet"))
    ratio = "–" if k["overhead_ratio"] is None else f"{k['overhead_ratio']:.2f}"
    print(f"  overhead: {usd(k['overhead_cost'])} outside batches (incl. audits) / {usd(k['batch_cost'])} in batches = {ratio}")
    print("projection for base ($/approved × (1 + overhead); information only, D-55 caps a batch; decision 236: en drafts "
          "the draft gap, the rest of each locale's deficit to base's targets (decision 37) is translated):")
    x = r["drafting"]
    print(f"  {x['locale']} drafts: {x['count']} × {usd(x['per_approved'])} → {usd(x['cost'])}"
          + (f" ({x['note']})" if x["note"] else ""))
    for p in r["projection"]:
        cost = usd(p["cost"]) + (f" ({p['note']})" if p["note"] else "")
        budget = f", budget {usd(p['budget'])}" if p["budget"] is not None else ""
        print(f"  {p['locale']}: {p['deficit']} to go, {p['translations']} translations × {usd(p['per_approved'])} → {cost}; "
              f"spent {usd(p['spent'])} (its drafts and translations){budget}")
    print("per regional bundle (its --bundle and --translate --bundle runs; deficit to its target, decision 110; "
          "projection as above, * = base's rate, no own run yet):")
    for x in r["bundles"]:
        proj = usd(x["projection"]) + ("*" if x["base_rate"] else "")
        print(f"  {x['bundle']} {x['locale']}: {len(x['runs'])} runs, {x['approved']} approved, spent {usd(x['cost'])}, "
              f"{usd(x['per_approved'])} per approved; {x['deficit']} to go → {proj}")
    if r["skipped"]:
        print("skipped (work/ is local):")
        for s in r["skipped"]:
            print(f"  {s}")


REVIEW_GAP_MIN = 10  # a longer pause between verdicts starts a new review session


def review_time(pool, bundle=None, run=None):
    """The developer's review time (plan 98, decision 110): human verdicts of the sources and every translation
    with `reviewed_at`, gaps on the whole timeline (filters don't make gaps), a session's first verdict has none."""
    src = {q["id"]: q for q in pool}
    items = [(q, q, "es") for q in pool] + [(t, src.get(t["id"], {}), l) for l in translations.LOCALES
                                            for t in translations.load(l)["questions"]]
    stamped, untimed = [], 0
    for x, q, l in items:
        rv = x.get("review") or {}
        if rv.get("reviewer") != "human":
            continue
        keep = (bundle is None or (q.get("bundle") or "base") == bundle) and (run is None or x.get("batch") == run)
        if rv.get("reviewed_at"):
            stamped.append((datetime.datetime.fromisoformat(rv["reviewed_at"]), keep))
        else:
            untimed += keep
    stamped.sort(key=lambda s: s[0])
    gaps, sessions, prev = [], 0, None
    for at, keep in stamped:
        gap = (at - prev).total_seconds() / 60 if prev else None
        prev = at
        if gap is not None and gap <= REVIEW_GAP_MIN:
            gaps += [gap] if keep else []
        elif keep:
            sessions += 1
    timed = sum(k for _, k in stamped)
    return {"timed": timed, "untimed": untimed, "sessions": sessions, "gaps": len(gaps), "minutes": sum(gaps),
            "per_100": 100 * sum(gaps) / len(gaps) if gaps else None}


def report_review_time(args):
    r = review_time(load_json(POOL)["questions"], args.bundle, args.run)
    if args.json:
        return print(json.dumps(r))
    what = " ".join(filter(None, [args.bundle and f"bundle {args.bundle}", args.run and f"run {args.run}"])) or "all"
    print(f"review time ({what}; human verdicts, sources and translations; gap > {REVIEW_GAP_MIN} min = new session):")
    if not r["timed"]:
        print(f"  0 timed verdicts (reviewed_at): nothing to measure yet; {r['untimed']} without a timestamp skipped")
        return
    per = "–" if r["per_100"] is None else f"{r['per_100']:.0f} min"
    print(f"  {r['timed']} timed verdicts in {r['sessions']} sessions; {r['minutes']:.0f} min over {r['gaps']} gaps "
          f"(a session's first verdict has none) → {per} per 100 verdicts")
    print(f"  {r['untimed']} verdicts without a timestamp skipped")


def _quantile(hist, order, q):
    """The bucket holding quantile q of a {bucket: count} histogram."""
    total, acc = sum(hist.values()), 0
    for b in order:
        acc += hist.get(b, 0)
        if acc >= q * total:
            return b
    return None


def report_played(args):
    """`qgen report --played`: played vs. rated difficulty (plan 109, decision 122); information only."""
    if not played.STATS.exists():
        return print("no played data: qgen telemetry --pull")
    stats, known = played.load(), played.rated()
    locales = None if (args.locale or "all") == "all" else args.locale.split(",")
    gids = args.age_group.split(",") if args.age_group else None
    since, mode = args.since or "", args.mode
    a = played.analyse(stats, known, load_age_groups()["groups"], mode, since, locales, gids)
    keep = lambda day, g=None, m=None: day >= since and (not gids or g in gids) and (not mode or m == mode)
    results, reached, levels = Counter(), Counter(), {}
    for k, v in stats["games"]["results"].items():
        day, version, m, g, res = k.split("|")
        if keep(day, g, m):
            results[(version, m, g, res)] += v
    for k, v in stats["games"]["reached"].items():
        day, g, m, lvl, res = k.split("|")
        if keep(day, g, m):
            reached[(g, int(lvl), res)] += v
    for k, v in stats["levels"].items():
        g, lvl, m, day = k.split("|")
        if keep(day, g, m):
            row = levels.setdefault((g, int(lvl)), [0, 0, 0, 0])
            for i, x in enumerate((v + [0, 0])[:4]):
                row[i] += x
    sessions, by_games, by_len = Counter(), Counter(), Counter()
    for k, s in stats["sessions"].items():
        version, day = k.split("|")
        if day >= since:
            sessions[version] += s["n"]
            by_games.update(s["games"])
            by_len.update(s["length"])
    answers, days, locs = Counter(), set(), Counter()
    for k, (n, _) in stats["answers"].items():
        qid, loc, g, m, day, clean = k.split("|")
        if keep(day, g, m) and (not locales or loc in locales):
            answers[clean] += n
            days.add(day)
            locs[loc] += n
    days |= {k.split("|")[1] for k in stats["sessions"] if k.split("|")[1] >= since}
    games = sum(results.values())
    jokers = Counter()
    for k, v in stats["games"]["jokers"].items():
        day, j = k.split("|")
        if day >= since:
            jokers[j] += v
    share = lambda key: sum(v for d, v in stats["games"][key].items() if d >= since)
    cells = [c for c in a["cells"] if c["n"] >= played.MIN_N and c["observed"] is not None]
    src = {q["id"]: translations.source_locale(q) for q in load_json(POOL)["questions"]}
    # per review view: None = the sources (an outlier in its source's language), else that locale's translations
    candidates = Counter(None if src.get(i) == l else l
                         for i, l in {(c["id"], c["locale"]) for o in ("too_easy", "too_hard") for c in a["outliers"][o]})
    if args.json:
        return print(json.dumps({"curves": a["curves"], "outliers": a["outliers"], "cells": cells if args.all else None,
                                 "sessions": dict(sessions), "games": games, "answers": dict(answers),
                                 "levels": {f"{g}|{l}": v for (g, l), v in sorted(levels.items())},
                                 "candidates": {l or "sources": n for l, n in candidates.items()}}, ensure_ascii=False, indent=1))
    pct = lambda r, n: f"{100 * r / n:.0f} %" if n else "–"
    print(f"data: {min(days, default='–')} – {max(days, default='–')}, {sum(sessions.values())} sessions, {games} games, "
          f"{sum(answers.values())} answers ({answers['1']} clean, {answers['0']} with help), "
          f"versions {', '.join(sorted(sessions)) or '–'}, locales {dict(locs)}, "
          f"{stats['unknown']} unknown ids (all days)")
    order = [played.length_bucket(m * 60) for m in [0, *played.LENGTH_MIN]]
    print("sessions:")
    print(f"  per version: {dict(sessions)}")
    print(f"  games per session: {dict(sorted(by_games.items(), key=lambda kv: int(kv[0])))}")
    if by_len:
        print(f"  length (min): median {_quantile(by_len, order, .5)}, quartiles {_quantile(by_len, order, .25)} / "
              f"{_quantile(by_len, order, .75)}")
    for title, i in [("mode", 1), ("result", 3), ("age group", 2)]:
        c = Counter()
        for key, v in results.items():
            c[key[i]] += v
        print(f"  games by {title}: {dict(c.most_common())}")
    if games:
        print(f"  customized {pct(share('customized'), games)}, mods {pct(share('mods'), games)} "
              f"(all modes and groups); joker uses per game: "
              + ", ".join(f"{j} {v / games:.2f}" for j, v in jokers.most_common()))
    print("per age group × level (answers, right, mean rated difficulty, games ending there lost / won / other):")
    for g in sorted({g for g, _ in levels} | {g for g, _, _ in reached}):
        print(f"  {g}:")
        for lvl in sorted({l for gg, l in levels if gg == g} | {l for gg, l, _ in reached if gg == g}):
            n, r, ds, dn = levels.get((g, lvl), [0, 0, 0, 0])
            end = lambda res: reached[(g, lvl, res)]
            other = sum(v for (gg, l, res), v in reached.items() if gg == g and l == lvl and res not in ("lost", "won"))
            print(f"    level {lvl:2}: {n:5} answers, {pct(r, n):>5} right, rated {ds / dn if dn else 0:4.1f}, "
                  f"ended {end('lost')} / {end('won')} / {other}")
    print(f"curves per age group (clean answers{f', mode {mode}' if mode else ''}; rated → right rate, n):")
    for g, c in a["curves"].items():
        if not c["points"]:
            print(f"  {g}: not enough data ({c['n']} clean answers, needs {played.GROUP_MIN})")
            continue
        print(f"  {g} ({c['n']}): " + ", ".join(f"{x:.1f} → {p * 100:.0f} % ({n})" for x, p, n in c["points"]))
    def line(c):
        obs = f"{c['bound'] or ''}{c['observed']:.1f}"
        return (f"    {c['id']} {c['locale']} {c['group']}: n {c['n']}, {pct(c['right'], c['n'])} right, "
                f"rated {c['rated']} → played {obs}, Δ {c['delta']:+.1f}")
    for key, title in [("too_easy", "too easy"), ("too_hard", "too hard"), ("mixed", "mixed (groups disagree, not a candidate)")]:
        print(f"outliers, {title}: {len(a['outliers'][key])}")
        for c in a["outliers"][key]:
            print(line(c))
    if args.all:
        print(f"every cell with n ≥ {played.MIN_N}: {len(cells)}")
        for c in sorted(cells, key=lambda c: -abs(c["delta"])):
            print(line(c))
    url = "http://localhost:8001/review?played=outliers"
    for l, n in sorted(candidates.items(), key=lambda kv: kv[0] or "") or [(None, 0)]:
        print(f"review candidates: {n} → {url}" + (f"&locale={l}" if l else " (sources)"))


def engine_model(results):
    return next((r["model"]["typical_p"] for r in results if r.get("result") == "ok"), None)


def cmd_report(args):
    if args.played:
        return report_played(args)
    if args.cost:
        return report_cost(args)
    if args.review_time:
        return report_review_time(args)
    if args.simulate:
        return report_simulate(args)
    if args.exit_check:
        return report_exit_check(load_json(POOL)["questions"], args.bundle or "base")
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
    cat = lambda q: (c := broad.get(categories.key(q))) and categories.sub_key(c["bundle"], c["slug"])
    print(f"pool: {len(pool)} questions")
    for title, key in [("status", lambda q: q["status"]), ("difficulty", lambda q: q["difficulty"]),
                       ("category", cat), ("style", lambda q: q.get("style")),
                       *[(f"axes.{a}", lambda q, a=a: (q.get("axes") or {}).get(a)) for a in concepts.AXES],
                       ("media", lambda q: f"{q['media']['type']}/{q['media']['role']}"),
                       ("bundle", lambda q: q.get("bundle"))]:
        print(f"  by {title}: {count(pool, key)}")
    blocked = save_file.blocked_ids()
    checked = engine.supply(pool, blocked)
    avail = [q for q in pool if q["status"] == "approved" and q["id"] not in blocked]  # = selection.ts available
    seen = save_file.seen_counts()
    by_seen = Counter(min(seen[q["id"]], 2) for q in avail)
    print(f"approved, not blocked: {len(avail)} ({len(blocked)} blocked)")
    print(f"  unseen approved: {by_seen[0]} (seen once: {by_seen[1]}, twice+: {by_seen[2]})")
    print(f"  by category: {count(avail, cat)}")
    print(f"  by difficulty: {count(avail, lambda q: q['difficulty'])}")
    print(f"  by bundle: {count(avail, lambda q: q.get('bundle'))}")
    print(f"supply per level, default game: young teens, {', '.join(checked['bundles'])} (a game needs 4 per level, D-22):")
    for l in checked["supply"]:
        lo, hi = l["range"]
        flag = f"  MISSING {l['missing']}" if l["missing"] else ""
        print(f"  level {l['level']:2} (difficulty {lo}–{hi}): {l['candidates']:3} candidates{flag}")
    for l in (args.locale or "es").split(","):
        report_progress(pool, args.bundle or "base", l)
    if args.subcategories:
        report_subcategories(avail, checked["ranges"])
        report_saturation(pool, args.bundle or "base")
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


# --- the LLM batch's steps: media, sheets, review, fix, research, record (D-36) 

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
    save_json(d / "not-travelling.json", away)
    save_json(d / "recorded.json", snapshot)
    return failed(f"{len(missing)} question(s) without a review: {', '.join(missing)}") if missing else []


# --- audit and back-audit (plan 16, D-56) -------------------------------------

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


SPOT_CHECK_SIZE = 30  # pm decision 2; without targets.json "quality"


def spot_check_size(run=None):
    """The run's spot-check size: its spot-checks.json "size" (e.g. batch-8's 120, decision 228), else quality.spot_check_size."""
    own = (load_json(layout.SPOT_CHECKS, {}) or {}).get(run, {}).get("size") if run else None
    return own or (targets.load_quality() or {}).get("spot_check_size", SPOT_CHECK_SIZE)


def audit_size(run):
    """Questions the run's audit reads: AUDIT_SAMPLE, or the whole spot check if larger."""
    return max(AUDIT_SAMPLE, spot_check_size(run))


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
    """{id: path} of the back-audits (plan 57) and neutralize runs' audits (plan 64), newest file wins; rebuilt only when a run's audit folder changes."""
    global _backaudits
    dirs = sorted([*WORK.glob("backaudit-*/audit"), *WORK.glob("neutralize-*/audit")], key=lambda p: p.stat().st_mtime_ns)
    key = tuple((p, p.stat().st_mtime_ns) for p in dirs)
    if _backaudits[0] != key:
        files = sorted((f for p in dirs for f in p.glob("q-*.json")), key=lambda f: f.stat().st_mtime_ns)
        _backaudits = (key, {f.stem: f for f in files})
    return _backaudits[1]


def audit_path(q):
    """The question's audit file: the newest back-audit or neutralize audit, else its batch's (plan 16); None without."""
    p = backaudit_index().get(q["id"])
    if p is None and q.get("batch"):
        p = WORK / q["batch"] / "audit" / f"{q['id']}.json"
    return p if p and p.exists() else None


def audit_of(q):
    p = audit_path(q)
    return load_json(p) if p else None


def translation_audit_of(t):
    """A translation's own audit: work/<t.batch>/audit/<id>.json (plan 67); never the source's back-audit."""
    return load_json(WORK / t["batch"] / "audit" / f"{t['id']}.json") if t.get("batch") else None


def run_number(name):
    tail = name.rsplit("-", 1)[-1]
    return int(tail) if tail.isdigit() else 0


def mode_run(mode):
    """(run, resuming): the oldest unfinished `<mode>-<n>` run, else the next number."""
    open_runs = sorted((p.parent.name for p in WORK.glob(f"{mode}-*/run.json") if not load_json(p).get("done")),
                       key=run_number)
    if open_runs:
        return open_runs[0], True
    return f"{mode}-{max((run_number(p.name) for p in WORK.glob(f'{mode}-*')), default=0) + 1}", False


def is_major(a):
    return a["verdict"] == "problem" and a["severity"] == "major"


def run_questions(run):
    """The questions a run's audit reads: everything in the locale for a translation run (in_locale), else the pool."""
    locale = run_locale(WORK / run)
    return in_locale(locale) if locale else load_json(POOL)["questions"]


def audit_input(q, pool, pool_en=None):
    """The question as played (plan 16): no review, fix, rater notes or fact check; a translation with its source."""

    def slot(spec, name):
        found = (media_tool.load_candidates(q["id"], name) or {"candidates": []})["candidates"]
        pick = next((c for c in found if spec.get("source_url") and c.get("page_url") == spec["source_url"]), None)
        return {"type": spec.get("type", "image"), "role": spec.get("role", "decorative"),
                "title": pick["title"] if pick else None}
    return {"question": {k: named(q, translations.source_locale(q))[k] for k in ["id", "bundle", "subcategory", *QUESTION_FIELDS]}
                        | ({} if q.get("source") else {"locale": translations.source_locale(q)}),
            "media": slot(q["media"], "media"),
            "background": slot(q["background"], "background") if q.get("background") else None,
            "related": related_questions(q, pool, pool_en), **({"source": q["source"]} if q.get("source") else {})}


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
    ids = audit_sample(run, audit_size(run))
    if not ids:
        return failed(f"{run}: no recorded LLM review to audit")
    return audit_ids(run, ids, args)


def audit_ids(run, ids, args):
    """Audit the ids not yet audited in work/<run>/audit/."""
    d = WORK / run / "audit"
    d.mkdir(parents=True, exist_ok=True)
    pool = run_questions(run)
    pool_en = None if run_locale(WORK / run) else as_locale(pool, "en")
    by_id = {q["id"]: q for q in pool}
    todo = [by_id[i] for i in ids if i in by_id and not (d / f"{i}.json").exists()]
    progress.resumed("audit", sum(i in by_id for i in ids) - len(todo), len(todo), "questions")
    locale = run_locale(WORK / run)
    names = ["house-style", "audit", *(["translate-review"] if locale else [])]
    lo, hi = load_age_groups()["scale"]
    today = datetime.date.today().isoformat()

    def work(q):
        user = "## Question to audit\n" + json.dumps(audit_input(q, pool, pool_en), ensure_ascii=False)
        system = prompt(*names, locale=translations.source_locale(q), bundle=run_bundle(WORK / run),
                        source_locale=q.get("source_locale"))
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
    run, resuming = mode_run("backaudit")
    if resuming:
        ids = load_json(WORK / run / "run.json")["ids"]
        print(f"Resuming {run}: {len(ids)} question(s)" + (" (--slice ignored)" if args.slice else "") + ".", flush=True)
    else:
        ids = backlog(args.slice or BACKAUDIT_SLICE)
        if not ids:
            sys.exit("No approved question from before D-56 without an audit.")
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
    return write_report(run, lines)


def audit_section(run):
    """The batch report's "## Audit" (plan 16); [] before the audit ran."""
    found = audits(run)
    if not found:
        return []
    dec = llm_decisions(run)
    by_id = {q["id"]: q for q in run_questions(run)}
    pct = lambda n, of: f"{n} of {of} ({100 * n / of:.0f} %)" if of else "0 of 0"
    back = run_mode(run) == "backaudit"
    what = "every question of the slice (plan 57" if back else "a seeded sample (plan 16"
    lines = ["## Audit", "", f"A second LLM reader of {what}, `prompts/audit.md`), blind to the review. "
             "It changes nothing in the pool; the developer decides its findings in the review tool.", ""]
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
    c = costs(WORK / run / "audit")
    lines += [f"- {'Slice' if back else 'Sample'}: {len(found)} audited of {len(dec) if back else len(audit_sample(run, audit_size(run)))}; "
              f"{len(c)} Claude calls, about ${sum(c):.2f}",
              "", "Major findings on approved questions:", ""]
    lines += [f"- **{i}**: {', '.join(a['problems']) or 'other'} — {a['notes']} ({REVIEW_URL}/{i})"
              for i, a in found.items() if is_major(a) and dec.get(i) == "approved"] or ["None."]
    return lines + [""]


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
          f"  git add authoring/data/questions.json {pool_file} app/data/bundles/ {concept_dir}/ authoring/reports/{run}.md"
          + (" authoring/data/english-keys.json" if locale == "en" else "") + "\n"
          f"  git commit -m \"{run}: {len(qs)} {'' if args.bundle == 'base' else args.bundle + ' '}questions, "
          f"{n_ok} approved (qgen batch)\"")


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


def translate_selection(locale, n, bundle="base"):
    """(ids, stale ids) for the next run (plan 66, D-36): approved, translatable sources of the bundle in another
    locale (decision 235) without an approved non-stale translation and not rejected in the locale; stale ones
    first, then one at a time from the subcategory with the fewest approved translations (picks count), spread
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
        if stop := health.translate_stop_reason(locale):
            print(stop, file=sys.stderr)
            if not args.dry_run:
                sys.exit(EXIT_HEALTH)
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
    out = write_translate_report(run)
    print(f"  report: {out.relative_to(ROOT)}")
    h = health.translation_health(run)
    print(f"\nDone: {run}: {h['translated']} translated, {h['approved']} approved, {h['needs_work']} need work, "
          f"{h['not travelling']} not travelling ({h['not travelling confirmed']} confirmed) "
          f"(took {progress.duration(time.monotonic() - t0)}).")
    if run == f"tr-{locale}-1":
        print(f"Pilot: the next `{again}` waits for the developer's go (`qgen health ack {run} \"<note>\"`).")
    files = [translations.path(locale), layout.POOL_FILE(locale, bundle), layout.BUNDLE_DATA, out]
    if h["not travelling confirmed"]:
        files.insert(1, POOL)
    print("Commit exactly this:\n  git add " + " ".join(f.relative_to(ROOT).as_posix() for f in files) + "\n"
          f"  git commit -m \"{run}: {h['translated']} {'' if bundle == 'base' else bundle + ' '}questions into "
          f"{LANGUAGES[locale]}, {h['approved']} approved "
          f"(qgen batch --translate)\"")
    return []


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
             f"- Spot check by a native speaker: {REVIEW_URL}?batch={run}&locale={locale}&sample=1",
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


def revise_steps(ns, model, review_model):
    """fix → fact check → review with a new media search → record: rework and the scan modes (QG-23);
    a scan run searches only slots without a kept pick (kept_slots)."""
    return [
        ("fix", cmd_fix, ns(model=model, check_model="sonnet")),
        ("media", cmd_media, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 1", cmd_review, ns(model=review_model, round=1)),
        ("research", cmd_research, ns()),
        ("sheets", cmd_sheets, ns()),
        ("review 2", cmd_review, ns(model=REVIEW_MODEL, round=2)),
        ("record", cmd_record, ns()),
    ]


def cmd_rework(args):
    """Every needs_work question with feedback (of one batch with --batch) once more through
    fix → fact check → review with a new media search → record (QG-23). Rerunning continues."""
    run, resuming = mode_run("rework")
    if resuming:
        ignored = [f for f, v in (("--batch", args.batch), ("--model", args.model)) if v]
        print(f"Resuming {run}" + (f" ({', '.join(ignored)} ignored)" if ignored else "") + ".", flush=True)
    else:
        ids = [q["id"] for q in load_json(POOL)["questions"] if q["status"] == "needs_work"
               and (q.get("review") or {}).get("feedback") and (not args.batch or q.get("batch") == args.batch)]
        if not ids:
            sys.exit("No needs_work questions with feedback.")
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
        *revise_steps(ns, model, model),
        ("export", lambda a: cmd_export(a) or [], ns()),
        ("sync", cmd_sync_run, ns()),
    ], "qgen rework")
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    qs = batch_questions(run, ("approved", "needs_work", "draft", "rejected"))
    n_ok = sum(q["status"] == "approved" for q in qs)
    print(f"\nDone: {run}: {n_ok} of {len(qs)} approved, {len(qs) - n_ok} still need work "
          f"(took {progress.duration(time.monotonic() - t0)}).")
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    files = ["authoring/data/questions.json", "app/data/pool.json", "app/data/bundles/", *stale_lines(set(cfg["ids"]), by_id)]
    print(f"Commit exactly this:\n  git add {' '.join(files)}\n"
          f"  git commit -m \"{run}: {n_ok} of {len(qs)} needs_work questions fixed and approved (qgen rework)\"")


SCAN_SCHEMA = {"type": "object", "required": ["flagged"], "properties": {"flagged": {"type": "array", "items": {
    "type": "object", "required": ["id", "issue"], "properties": {"id": STR, "issue": STR}}}}}
SCAN_CHUNK = 50
NEUTRAL_FIELDS = ["description", *FACT_FIELDS]
SCANS = {  # run mode: scan prompt, questions read, their input, the reviser's issue prefix (QG-24, plan 64)
    "tighten": {"prompt": "tighten", "bundle": None, "issue": "too long", "schema": SCAN_SCHEMA,
                "item": lambda q: {"id": q["id"], "clue": (q.get("axes") or {}).get("clue"), "question": q["question"]}},
    "neutralize": {"prompt": "neutralize", "bundle": "base", "locale": "es", "issue": "not neutral Spanish",
                   "schema": {**SCAN_SCHEMA, "required": ["flagged", "no_neutral_form"], "properties": {
                       **SCAN_SCHEMA["properties"], "no_neutral_form": {"type": "array", "items": {
                           "type": "object", "required": ["id", "words"], "properties": {"id": STR, "words": STR}}}}},
                   "item": lambda q: {"id": q["id"], **{k: q[k] for k in NEUTRAL_FIELDS}}},
}


def cmd_scan(args):
    """Claude reads every approved and needs_work question of the run's scope in chunks of SCAN_CHUNK and flags
    those its mode's prompt asks for (SCANS); run.json gets their ids and issues."""
    d = run_dir(args)
    cfg = load_json(d / "run.json", {})
    if "issues" in cfg:
        return []
    scan, only = SCANS[cfg["mode"]], set(cfg.get("only") or [])
    qs = [q for q in load_json(POOL)["questions"] if q["status"] in ("approved", "needs_work")
          and (not scan["bundle"] or (q.get("bundle") or "base") == scan["bundle"]) and (not only or q["id"] in only)
          and scan.get("locale", translations.source_locale(q)) == translations.source_locale(q)]
    groups = [g for g in locale_chunks(qs, SCAN_CHUNK) if not (d / "scan" / f"{g[0]['id']}.json").exists()]

    def work(group):
        items = [scan["item"](q) for q in group]
        system = prompt("house-style", scan["prompt"], locale=translations.source_locale(group[0]))
        out = claude(system, "## Questions\n" + json.dumps(items, ensure_ascii=False), scan["schema"], args.model, d)
        ids = {q["id"] for q in group}
        save_json(d / "scan" / f"{group[0]['id']}.json", [f for f in out["flagged"] if f["id"] in ids])
        if "no_neutral_form" in out:
            save_json(d / "scan" / "no-neutral-form" / f"{group[0]['id']}.json",
                      [f for f in out["no_neutral_form"] if f["id"] in ids])

    errors = parallel(work, groups, args.jobs, "scan", "calls")
    if not errors:
        issues = {f["id"]: f["issue"] for p in sorted((d / "scan").glob("*.json")) for f in load_json(p)}
        save_json(d / "run.json", {**cfg, "ids": list(issues), "scanned": len(qs), "issues": issues})
        print(f"  {len(issues)} of {len(qs)} questions flagged", flush=True)
    return errors


def cmd_tighten(args):
    """Find long-winded questions in the whole pool, approved ones included, then shorten, fact-check,
    review and record them like `qgen rework` (QG-24). Kept and dropped ones stay as they were."""
    run, resuming = mode_run("tighten")
    if resuming:
        print(f"Resuming {run}.", flush=True)
    else:
        save_json(WORK / run / "run.json", {"mode": "tighten", "started": datetime.date.today().isoformat()})
        print(f"Starting {run}: reading the whole pool.", flush=True)
    d = WORK / run
    progress.verbose = False

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    t0 = run_steps([
        ("scan", cmd_scan, ns(model="opus")),
        *revise_steps(ns, "opus", REVIEW_MODEL),
        ("export", lambda a: cmd_export(a) or [], ns()),
        ("sync", cmd_sync_run, ns()),
    ], "qgen tighten")
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    revised = [p.stem for p in (d / "reviews").glob("*.json") if fixed(load_json(p))]
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    n_ok = sum(by_id[i]["status"] == "approved" for i in revised if i in by_id)
    print(f"\nDone: {run}: {len(cfg.get('ids', []))} flagged, {len(revised)} shortened, {n_ok} of those approved, "
          f"{len(revised) - n_ok} need work (took {progress.duration(time.monotonic() - t0)}).")
    files = ["authoring/data/questions.json", "app/data/pool.json", "app/data/bundles/", *stale_lines(revised, by_id)]
    print(f"Commit exactly this:\n  git add {' '.join(files)}\n"
          f"  git commit -m \"{run}: {len(revised)} long-winded questions shortened, {n_ok} approved (qgen tighten)\"")


def stale_lines(revised, by_id):
    """Prints per locale how many translations the rewritten questions staled (D-81); returns the
    app/data/pool.<locale>.json paths export rewrote."""
    files = []
    for l in translations.LOCALES:
        if translations.path(l).exists():
            src = translations.load(l)["questions"]
            n = sum(t["id"] in by_id and translations.is_stale(t, by_id[t["id"]]) for t in src if t["id"] in revised)
            print(f"  {l}: {n} translation(s) stale from this run (D-81)")
            files.append(layout.LOCALE_POOL(l).relative_to(ROOT).as_posix())
    return files


def cmd_neutralize(args):
    """Rewrite Colombian and other national wording in `base`'s es-sourced questions into neutral Spanish (plan 64, D-78):
    scan → fix → review → record → audit → export, like `qgen tighten`. --dry-run: the scan only, then
    the flagged ids and a cost estimate; the next run continues from that scan."""
    run, resuming = mode_run("neutralize")
    if resuming:
        print(f"Resuming {run}" + (" (--ids ignored)" if args.ids else "") + ".", flush=True)
    else:
        only = split_list(args.ids)
        save_json(WORK / run / "run.json", {"mode": "neutralize", "started": datetime.date.today().isoformat(),
                                            **({"only": only} if only else {})})
        print(f"Starting {run}: reading the base bundle's es-sourced questions" + (f" ({len(only)} ids)" if only else "") + ".", flush=True)
    d = WORK / run
    progress.verbose = False

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    again = "qgen neutralize" + (" --dry-run" if args.dry_run else "")
    # no validate: a resume after a partial fix has an unexported pool until the export step
    t0 = run_steps([("scan", cmd_scan, ns(model="opus"))], again, run, validate=False)
    cfg = load_json(d / "run.json")
    if args.dry_run:
        print_neutralize_scan(run)
        return []
    if cfg["ids"]:
        run_steps([
            *revise_steps(ns, "opus", REVIEW_MODEL),
            ("audit", lambda a: cmd_audit(a) if load_json(d / "recorded.json") else [], ns(model="opus", batch=run)),
            ("export", lambda a: cmd_export(a) or [], ns()),
            ("sync", cmd_sync_run, ns()),
        ], "qgen neutralize", run)
    else:
        run_steps([], "qgen neutralize", run)
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    revised = [i for i in cfg["ids"] if fixed(load_json(d / "reviews" / f"{i}.json", {}))]
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    n_ok = sum(by_id[i]["status"] == "approved" for i in revised if i in by_id)
    out = write_neutralize_report(run, revised)
    print(f"\nDone: {run}: {len(cfg['ids'])} flagged, {len(revised)} reworded, {n_ok} of those approved, "
          f"{len(revised) - n_ok} need work (took {progress.duration(time.monotonic() - t0)}).")
    files = ["authoring/data/questions.json", "app/data/pool.json", "app/data/bundles/", out.relative_to(ROOT).as_posix(),
             *stale_lines(revised, by_id)]
    print(f"Commit exactly this:\n  git add {' '.join(files)}\n"
          f"  git commit -m \"{run}: {len(revised)} base questions reworded into neutral Spanish, {n_ok} approved (qgen neutralize)\"")
    return []


def scan_extras(run):
    """[{id, words}] the neutralize scan found no neutral form for (plan 64)."""
    return [f for p in sorted((WORK / run / "scan" / "no-neutral-form").glob("*.json")) for f in load_json(p)]


def print_neutralize_scan(run):
    """--dry-run: flagged ids with their issues, words without a neutral form, cost estimate."""
    cfg = load_json(WORK / run / "run.json")
    ids, issues = cfg["ids"], cfg["issues"]
    print(f"\n{run}: {len(ids)} of {cfg['scanned']} base questions flagged")
    for i in ids:
        print(f"- {i}: {issues[i]}")
    extras = scan_extras(run)
    if extras:
        print(f"\nNo neutral form ({len(extras)}, left as they are):")
        for f in extras:
            print(f"- {f['id']}: {f['words']}")
    scan = sum(costs(WORK / run))
    past = [(p.parent, c) for p in WORK.glob("*/run.json") if (c := load_json(p)) and c.get("done")
            and c.get("mode") in ("rework", *SCANS) and c.get("ids")]
    n = sum(len(c["ids"]) for _, c in past)
    per_q = sum(sum(costs(p)) for p, _ in past) / n if n else None
    audit = [x for p in WORK.glob("*/audit") for x in costs(p)]
    per_audit = sum(audit) / len(audit) if audit else 0
    if per_q is None:
        print(f"\nScan: ${scan:.2f}. No finished rework/tighten/neutralize run yet to estimate the rest from.")
    else:
        rest = per_q * len(ids) + per_audit * min(AUDIT_SAMPLE, len(ids))
        print(f"\nScan: ${scan:.2f}. Estimated rest: about ${rest:.2f} at list price "
              f"(${per_q:.2f} per flagged question from past rework/tighten/neutralize runs, scans included, "
              f"${per_audit:.2f} per audit call × {min(AUDIT_SAMPLE, len(ids))}).")
    print("Run `qgen neutralize` to reword them; it continues from this scan.")


def write_neutralize_report(run, revised):
    """authoring/reports/<run>.md (plan 64); `qgen report --qc <run>` adds its QC section."""
    cfg = load_json(WORK / run / "run.json")
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    work = [i for i in revised if i in by_id and by_id[i]["status"] == "needs_work"]
    c = costs(WORK / run / "costs.log") + costs(WORK / run / "audit")
    lines = [f"# {run}", "",
             f"Made by `qgen neutralize` on {datetime.date.today().isoformat()} (plan 64, D-78): `base` questions "
             "reworded from Colombian or other national usage into neutral Spanish. Generated file: don't edit by hand.", "",
             f"- Scanned: {cfg.get('scanned', 0)}", f"- Flagged: {len(cfg['ids'])}", f"- Reworded: {len(revised)}",
             f"- Approved: {len(revised) - len(work)}", f"- Needs work: {len(work)}",
             f"- Claude calls: {len(c)}, about ${sum(c):.2f} at list price", "",
             "## Reworded", ""]
    lines += [f"- **{i}**: {cfg['issues'][i]}" for i in revised] or ["None."]
    lines += ["", "## No neutral form", ""]
    lines += [f"- {f['id']}: {f['words']}" for f in scan_extras(run)] or ["None."]
    lines += ["", *audit_section(run), *qc_section(run), "## Needs work", ""]
    lines += [f"- **{i}** {by_id[i]['question']} → {by_id[i]['answer']}: {by_id[i]['review']['feedback']}" for i in work] or ["None."]
    return write_report(run, lines)


# --- player reports (plan 93) -------------------------------------------------

def apply_reports(reports, dry_run=False):
    """Reports (reviews.report_feedback's dicts) → human needs_work reviews; returns (applied, already, skipped)."""
    known, n = {}, Counter()
    for r in reports:
        where = f"{r['question']} ({r['lang']})"
        new = reviews.needs_work(r["question"], r["lang"], reviews.report_feedback(r), known, dry_run)
        if new is None:
            print(f"  {where}: unknown question, skipped", file=sys.stderr)
            n["skipped"] += 1
        elif not new:
            print(f"  {where}: already there")
            n["already"] += 1
        else:
            print(f"  {where}: needs_work" + (f" ← {new}" if dry_run else ""))
            n["applied"] += 1
    return n["applied"], n["already"], n["skipped"]


PULLED = paths.STATE / "reports-pulled.json"  # {"<url>": [server ids written, not yet acked]}
TOKEN_FILE = paths.STATE / "report-token"  # gitignored


def report_api(url, token, path, body=None):
    """One call to the report server (plan 103, API v1) → parsed JSON; errors exit."""
    import urllib.request, urllib.error
    req = urllib.request.Request(url + path, method="POST" if body is not None else "GET",
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        hint = {401: ": wrong pull token"}.get(e.code, "")
        sys.exit(f"{url}{path}: HTTP {e.code}{hint} {e.read()[:200].decode(errors='replace')}")
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(f"{url}{path}: {getattr(e, 'reason', e)}")


def report_server(url):
    """(base URL, pull token): --url, else reportUrl in app/desktop/package.json; token from env or file."""
    url = (url or json.loads((ROOT / "app" / "desktop" / "package.json").read_text())["reportUrl"]).rstrip("/")
    if not url:
        sys.exit("no report URL: pass --url or set reportUrl in app/desktop/package.json")
    token = os.environ.get("TRIVIA_REPORT_TOKEN", "").strip() or (
        TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else "")
    if not token:
        sys.exit(f"no pull token: set TRIVIA_REPORT_TOKEN or write it to {TOKEN_FILE}")
    return url, token


def pull_reports(args):
    """`qgen flag --pull`: the server's reports → needs_work reviews, then ack (plan 93 task 5).
    Pages are acked one by one: GET returns the same reports until acked."""
    url, token = report_server(args.url)
    ledger = load_json(PULLED) if PULLED.exists() else {}
    done = set(ledger.get(url, []))
    n = Counter()
    while True:
        page = report_api(url, token, "/reports?limit=500")
        rs = page["reports"]
        n["pulled"] += len(rs)
        new = [r for r in rs if r["id"] not in done]
        n["earlier"] += len(rs) - len(new)
        mods = [r for r in new if ":" in r["question"]]  # mod questions aren't ours (decision 128)
        n["mod"] += len(mods)
        a, b, s = apply_reports([{**r, "note": r["note"] or None, "date": r["received_at"][:10]}
                                 for r in new if r not in mods], args.dry_run)
        n["applied"] += a; n["already"] += b; n["unknown"] += s
        if args.dry_run:
            if page["more"]:
                print("  more reports on the server: --dry-run shows only the first page")
            break
        if not rs:
            break
        ids = [r["id"] for r in rs]
        done.update(ids)
        atomic.write_json(PULLED, {**ledger, url: sorted(done)})  # before the ack: a crash can't double feedback
        report_api(url, token, "/reports/ack", {"ids": ids})
        done.difference_update(ids)  # acked = deleted on the server; SQLite may reuse their ids
        ledger = {**ledger, url: sorted(done)}
        atomic.write_json(PULLED, ledger)
        if not page["more"]:
            break
    print(f"{n['pulled']} pulled: {n['applied']} {'would be ' if args.dry_run else ''}applied, "
          f"{n['already'] + n['earlier']} already there, {n['unknown'] + n['mod']} skipped "
          f"({n['unknown']} unknown, {n['mod']} mod questions)")


def cmd_flag(args):
    """Pasted report text (stdin) → needs_work reviews (plan 93, decision 142); --pull: the report server's."""
    if args.pull:
        return pull_reports(args)
    reports = reviews.parse_reports(sys.stdin.read())
    if not reports:
        sys.exit("no report found: paste text with a «¡Trivia! #q-… · …» line")
    applied, already, skipped = apply_reports(reports, args.dry_run)
    print(f"{len(reports)} reports: {applied} {'would be ' if args.dry_run else ''}applied, "
          f"{already} already there, {skipped} skipped")


def cmd_telemetry(args):
    """`qgen telemetry --pull`: telemetry sessions → state/played/stats.json, then ack (plan 109)."""
    if not args.pull:
        sys.exit("qgen telemetry: nothing to do without --pull")
    known = played.rated()
    if args.from_file:
        stats = played.load()
        doc, today = load_json(Path(args.from_file)), datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        sessions = doc["sessions"] if "sessions" in doc else [doc]  # also one POST body, e.g. the fixture
        n = played.fold(stats, [{"received_day": today, **s} for s in sessions], known)
        if not args.dry_run:
            played.save(stats)
        n.update(pages=0, acked=0)
    else:
        url, token = report_server(args.url)
        n = played.pull(lambda path, body=None: report_api(url, token, path, body), known, args.dry_run)
    print(f"{n['sessions']} sessions, {n['games']} games, {n['answers']} answers "
          f"{'would be ' if args.dry_run else ''}folded ({n['unknown']} unknown ids), "
          f"{n['pages']} pages, {n['acked']} acked" + (" (more on the server)" if n.get("more") else ""))


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


def validate_pool():
    """(errors, warnings) for the whole source pool and its export (QP-7)."""
    data = load_json(POOL)
    errors, warnings, ids, unlicensed = [], [], set(), []
    subcategories = categories.broad_of()
    lists = {}
    axes_of = {b: concepts.load_axes(b) for b in categories.bundle_ids()}
    lo, hi = load_age_groups()["scale"]
    bundles = load_bundles()
    bundle_ids = {b["id"] for b in bundles}
    bundle_of = {b["id"]: b for b in bundles}
    errors += taxonomy_problems()
    errors += slug_problems()
    e, w = bundle_problems(bundles)
    errors += e
    warnings += w
    errors += age_groups.level_problems(load_age_groups())
    errors += targets.problems((lo, hi), bundles)
    import health  # authoring/tools/health.py (imports qgen)
    errors += targets.health_problems(health.THRESHOLDABLE)
    errors += targets.quality_problems()
    errors += spot_check_problems(data["questions"], (lo, hi))
    errors += english_keys_problems(data["questions"])
    for q in data["questions"]:
        qid = q.get("id", "?")
        for k in ["id", "status", "subcategory", "difficulty", "description", "question", "answer",
                  "wrong_answers", "hints", "media", "fun_fact"]:
            if k not in q: errors.append(f"{qid}: missing {k}")
        if qid in ids: errors.append(f"{qid}: duplicate id")
        ids.add(qid)
        if q.get("status") not in {"draft", "approved", "rejected", "needs_work"}: errors.append(f"{qid}: bad status")
        errors += [f"{qid}: {p}" for p in review_problems(q)]
        errors += [f"{qid}: {p}" for p in source_locale_problems(q, bundle_of.get(q.get("bundle")))]
        if "translatable" in q and q["translatable"] is not False: errors.append(f"{qid}: translatable must be false when set (absent = translatable, D-81)")
        key = categories.key(q)
        if key not in subcategories:
            errors.append(f"{qid}: subcategory not in its bundle's categories (D-19, D-49, D-99, D-109)")
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
                verdict, reasons = providers.licence_verdict(slot) if slot.get("file_url") else ("ok", [])
                if verdict == "replace":  # plans/26, plans/53
                    unlicensed.append(f"{qid} {label} ({'; '.join(reasons)})")
        if all(k in q for k in ["wrong_answers", "hints", "difficulty", "answer"]):
            errors += [f"{qid}: {p}" for p in check_question_shape(q)]
        if q.get("axes") is not None:  # D-37
            e, w = concepts.axes_problems(q["axes"], axes_of.get(key[0], axes_of["base"]))
            errors += [f"{qid}: {p}" for p in e]
            warnings += [f"{qid}: {p}" for p in w]
        if q.get("concept") is not None and isinstance(q.get("subcategory"), str):
            if key not in lists:
                lists[key] = {c["name"] for c in (concepts.load(*key) or {}).get("concepts", [])}
            if q["concept"] not in lists[key]:
                errors.append(f"{qid}: concept {q['concept']!r} is not in {key[1]}'s concept list ({key[0]})")
    for b, sub in subcategories:
        lst = concepts.load(b, sub)
        keys = [concepts.key(c["name"]) for c in (lst or {}).get("concepts", [])]
        dup = sorted({k for k in keys if keys.count(k) > 1})
        if dup:
            errors.append(f"{concepts.path(b, sub).relative_to(ROOT)}: same concept twice: {', '.join(dup)}")
        bad = [c["name"] for c in (lst or {}).get("concepts", [])
               if not isinstance(c.get("known_at"), int) or not lo <= c["known_at"] <= hi]
        if bad:
            errors.append(f"{concepts.path(b, sub).relative_to(ROOT)}: known_at missing or not {lo}–{hi} (D-38): {first_ids(bad)}")
    if unlicensed:
        errors.append(f"{len(unlicensed)} approved pick(s) on the licence replace list (needs_work and a new file, decision 47): {first_ids(unlicensed)}")
    e, w = translation_problems(data)
    errors += e
    warnings += w
    for path, text in pool_export.exports(data).items():
        if (path.read_text(encoding="utf-8") if path.exists() else None) != text:
            errors.append(f"{path.relative_to(ROOT)} is not the current export of the pool: run `qgen export`")
    for p in pool_export.stale_packs(pool_export.exports(data)):
        errors.append(f"{p.relative_to(ROOT)}: not written by `qgen export` (pack without questions); delete it")
    for l in translations.LOCALES:
        if layout.LOCALE_POOL(l).exists() and not translations.exported(l, data):
            errors.append(f"{layout.LOCALE_POOL(l).relative_to(ROOT)}: no {l} source or translation; delete it")
    tag, released = released_ids()
    gone = sorted(released - ids, key=natural_key) if tag else []
    if gone:
        errors.append(f"{len(gone)} id(s) of {tag}'s pool missing from authoring/data/questions.json "
                      f"(drop = status change, never deletion; plan 91): {', '.join(gone)}")
    return errors, warnings


def released_ids():
    """(newest v* tag, ids in its app/data/[bundles/<id>/]pool*.json), or (None, None) without a tag or git (plan 91)."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    try:
        tags = git("tag", "--list", "v*", "--sort=-v:refname").stdout.split()
    except OSError:
        return None, None
    if not tags:
        return None, None
    files = git("ls-tree", "-r", "--name-only", tags[0], "app/data/").stdout.split()
    ids = set()
    for f in files:
        if re.fullmatch(r"app/data/(bundles/[^/]+/)?pool(\.[A-Za-z-]+)?\.json", f):
            ids |= {q["id"] for q in json.loads(git("show", f"{tags[0]}:{f}").stdout)["questions"]}
    return tags[0], ids


def source_locale_problems(q, bundle):
    """A source's locale (decision 235): known; base from batch-9 on en; a regional bundle's in its region's
    language, the first of its languages (decision 110)."""
    loc, out = translations.source_locale(q), []
    if loc not in translations.LOCALES:
        return [f"locale must be one of {', '.join(translations.LOCALES)}"]
    m = re.fullmatch(r"batch-(\d+)", q.get("batch") or "")
    if bundle and bundle["kind"] == "base" and m and int(m.group(1)) >= translations.ENGLISH_FROM and loc != "en":
        out.append(f"locale must be en: base drafts in English from batch-{translations.ENGLISH_FROM} on (plan 148)")
    if bundle and bundle["kind"] == "region" and loc != (want := translations.draft_locale(bundle)):
        out.append(f"locale must be {want}, {bundle['id']}'s language (decision 110)")
    return out


def review_problems(q):
    """A question's or translation's review vs. its status (D-33, plan 15)."""
    rv, out = q.get("review"), []
    if rv is None:
        return out
    if rv.get("decision") != q.get("status") or "feedback" not in rv or "reviewed_on" not in rv:
        out.append("review does not match status")
    if not set(rv.get("problems") or []) <= set(PROBLEMS):
        out.append(f"review.problems must be from {', '.join(PROBLEMS)}")
    if rv.get("reviewer") not in {"human", "llm"}: out.append("review.reviewer must be human or llm")
    if (rv.get("reviewer") == "llm") != bool(rv.get("model")): out.append("review.model must be set exactly for an llm review")
    prev = rv.get("previous")
    if prev is not None and (prev.get("reviewer") not in {"human", "llm"}
                             or rv.get("reviewer") == "human" and prev.get("reviewer") != "llm"):
        out.append("review.previous must be a review, an llm one under a human one")
    return out


def first_ids(ids, n=5):
    return f"{', '.join(ids[:n])}{' …' if len(ids) > n else ''}"


def translation_problems(data):
    """(errors, warnings) for authoring/data/questions.<locale>.json and the names files (D-81)."""
    errors, warnings = [], []
    src = {q.get("id"): q for q in data["questions"]}
    for p in sorted(layout.translations("*").parent.glob("questions.*.json")):
        if p.name.split(".")[1] not in translations.LOCALES:
            errors.append(f"{p.relative_to(ROOT)}: locale not in {', '.join(translations.LOCALES)} (D-78)")
    for l in translations.LOCALES:
        p = translations.path(l)
        if not p.exists():
            continue
        rel, doc = p.relative_to(ROOT), translations.load(l)
        if doc.get("version") != 1 or doc.get("locale") != l:
            errors.append(f"{rel}: header must be version 1, locale {l!r}")
        ids, stale, orphaned = set(), [], []
        for t in doc.get("questions", []):
            tid = t.get("id", "?")
            where = f"{rel}: {tid}"
            for k in ["id", "source_hash", "status", "difficulty", *translations.TEXT_FIELDS]:
                if k not in t: errors.append(f"{where}: missing {k}")
            if tid in ids: errors.append(f"{where}: duplicate id")
            ids.add(tid)
            q = src.get(tid)
            if q is None:
                errors.append(f"{where}: no such id in the source pool")
                continue
            if t.get("status") not in {"draft", "approved", "rejected", "needs_work"}: errors.append(f"{where}: bad status")
            errors += [f"{where}: {x}" for x in review_problems(t)]
            if all(k in t for k in ["wrong_answers", "hints", "difficulty", "answer"]):
                errors += [f"{where}: {x}" for x in check_question_shape(t)]
            if translations.source_locale(q) == l:
                errors.append(f"{where}: the source is in {l} already; delete the entry (decision 235)")
                continue
            if t.get("status") == "rejected":
                continue
            if q.get("status") == "rejected" or not translations.translatable(q):
                errors.append(f"{where}: source is rejected or translatable: false; reject the translation")
                continue
            if translations.is_stale(t, q): stale.append(tid)
            if t.get("status") == "approved" and q.get("status") != "approved": orphaned.append(tid)
        if stale:
            warnings.append(f"{rel}: {len(stale)} stale translation(s) (source text changed): {first_ids(stale)}")
        if orphaned:
            warnings.append(f"{rel}: {len(orphaned)} approved translation(s) of a source not approved: {first_ids(orphaned)}")
    return errors + names_problems(data), warnings + names_warnings(data)


def names_problems(data):
    """Errors in the names files: header, unknown keys; a name missing for what pool.<locale>.json uses."""
    errors, cats = [], categories.load()
    for l in (*translations.NAMED, "es", "es-ES"):
        for b in categories.bundle_ids():
            p = layout.NAMES(l, b)
            if not p.exists():
                continue
            rel, doc = p.relative_to(ROOT), load_json(p)
            if doc.get("version") != 1 or doc.get("locale") != l:
                errors.append(f"{rel}: header must be version 1, locale {l!r}")
            known = {"categories": {c["slug"] for c in cats if c["bundle"] == b},
                     "subcategories": set(categories.subcategories(b))}
            if b == "base" and l in translations.NAMED:  # es, es-ES: bundles.json, age-groups.json
                known["bundles"] = set(categories.bundle_ids())
                known["age_groups"] = {g["id"] for g in load_age_groups()["groups"]}
            for k in ["bundles", "age_groups"]:
                if b != "base" and k in doc:
                    errors.append(f"{rel}: {k} names go in {layout.NAMES(l).relative_to(ROOT)}")
            for k, keys in known.items():
                names = doc.get(k) or {}
                bad = sorted(set(names) - keys)
                if bad:
                    errors.append(f"{rel}: {k} not in the categories/bundles/age-groups files: {first_ids(bad)}")
                empty = sorted(n for n, v in names.items() if not name_ok(v, k == "bundles"))
                if empty:
                    errors.append(f"{rel}: {k} with an empty or malformed name: {first_ids(empty)}")
        if l not in translations.NAMED or not translations.exported(l, data):
            continue
        names, broad = categories.load_names(l), categories.broad_of()
        missing = set()
        for e in translations.play_entries(l, data):
            b, sub = categories.key(e)
            if categories.sub_key(b, sub) not in names["subcategories"]: missing.add(f"subcategory {categories.sub_key(b, sub)}")
            c = broad.get((b, sub))
            if c and categories.sub_key(b, c["slug"]) not in names["categories"]: missing.add(f"category {categories.sub_key(b, c['slug'])}")
            if e["bundle"] not in names["bundles"]: missing.add(f"bundle {e['bundle']}")
        if missing:
            errors.append(f"{l}: pool.{l}.json uses names missing in names.{l}.json: {first_ids(sorted(missing))}")
    return errors


def name_ok(v, bundle):
    """A non-empty string; a bundle's is {"name", "description"}."""
    if bundle:
        return isinstance(v, dict) and all(isinstance(v.get(k), str) and v[k].strip() for k in ["name", "description"])
    return isinstance(v, str) and bool(v.strip())


def names_warnings(data):
    """Missing names per locale, once the locale has a pool or a names file."""
    out, cats = [], categories.load()
    for l in translations.NAMED:
        if not (translations.exported(l, data) or any(layout.NAMES(l, b).exists() for b in categories.bundle_ids())):
            continue
        names = categories.load_names(l)
        n = (len(set(categories.bundle_ids()) - set(names["bundles"]))
             + len({categories.sub_key(c["bundle"], c["slug"]) for c in cats} - set(names["categories"]))
             + len({categories.sub_key(c["bundle"], s) for c in cats for s in c["subcategories"]} - set(names["subcategories"]))
             + len({g["id"] for g in load_age_groups()["groups"]} - set(names["age_groups"])))
        if n:
            out.append(f"{l}: {n} bundle/category/subcategory/age-group name(s) missing in the names.{l}.json files")
    return out


def english_keys_problems(questions):
    """Shape of authoring/data/english-keys.json (decision 232): version 1; per pool id a 12-hex hash, an answer
    and a concept (string or null). Stale entries are fine: the next `qgen english-keys` drops them."""
    doc = load_json(layout.ENGLISH_KEYS)
    if doc is None:
        return []
    rel = "authoring/data/english-keys.json"
    if doc.get("version") != 1 or not isinstance(doc.get("questions"), dict):
        return [f"{rel}: needs version 1 and a questions object"]
    ids, out = {q["id"] for q in questions}, []
    for i, k in doc["questions"].items():
        if i not in ids:
            out.append(f"{rel}: {i}: not in the pool")
        elif not (isinstance(k, dict) and set(k) == {"hash", "answer", "concept"}
                  and isinstance(k["hash"], str) and re.fullmatch(r"[0-9a-f]{12}", k["hash"])
                  and isinstance(k["answer"], str) and k["answer"].strip()
                  and (k["concept"] is None or isinstance(k["concept"], str))):
            out.append(f"{rel}: {i}: needs hash (12 hex), answer and concept (string or null)")
    return out


def run_ids(run):
    """The ids of a back-audit (plan 57) or neutralize run (plan 64), or None for any other name.
    work/<run>/run.json, else the run's "ids" in spot-checks.json (tracked, for a checkout without work/)."""
    m = re.fullmatch(r"(backaudit|neutralize)-\d+", run)
    if not m:
        return None
    cfg = load_json(WORK / run / "run.json", {}) or {}
    if cfg.get("mode") == m.group(1):
        return cfg.get("ids")
    return ((load_json(layout.SPOT_CHECKS, {}) or {}).get(run) or {}).get("ids")


def spot_check_problems(questions, scale):
    """Errors in authoring/data/spot-checks.json (plan 16): batches (or back-audit, neutralize runs) and ids exist, values in range;
    a translation run's (tr-<locale>-<n>) items are its translations, with "locale" (plan 67);
    a back-audit or neutralize run's members are its entry's "ids", never work/ (gitignored)."""
    checks = load_json(layout.SPOT_CHECKS)
    if checks is None:
        return []
    rel, out = "authoring/data/spot-checks.json", []
    pool_batches = {q["id"]: q.get("batch") for q in questions}
    tr_batches = {}  # locale -> {id: batch} of its translations (plan 67)
    decisions, (lo, hi) = {"approved", "needs_work", "rejected"}, scale
    for b, entry in checks.items():
        locale = translations.run_locale(b)
        if locale and locale not in tr_batches:
            tr_batches[locale] = {t["id"]: t.get("batch") for t in translations.load(locale)["questions"]}
        batch_of = tr_batches[locale] if locale else pool_batches
        if re.fullmatch(r"(backaudit|neutralize)-\d+", b):
            if not (isinstance(entry.get("ids"), list) and entry["ids"]):
                out.append(f"{rel}: {b}: needs its run's ids")
                continue
            batch_of = {i: b for i in entry["ids"]}
        if b not in batch_of.values():
            out.append(f"{rel}: no batch {b!r} in {f'questions.{locale}.json' if locale else 'the pool'}")
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
                ("locale", it.get("locale") == locale),
                ("on", isinstance(it.get("on"), str) and re.fullmatch(r"\d{4}-\d\d-\d\d", it["on"]))] if not ok]
            if bad:
                out.append(f"{rel}: {b}: {i}: bad {', '.join(bad)}")
    return out


def taxonomy_problems():
    """Every bundle's categories file belongs to a bundle; names and slugs are unique within a bundle (D-43, D-99)."""
    errors, ids = [], categories.bundle_ids()
    if ids[:1] != ["base"]:
        errors.append("app/data/bundles.json: base must come first")
    for p in sorted(layout.app_paths.BUNDLE_DATA.glob("*/categories.json")):
        if p.parent.name not in ids or p.parent.name == "base":
            errors.append(f"{p.relative_to(ROOT)}: no bundle {p.parent.name!r} in app/data/bundles.json")
    for b in ids:
        for what, items in [("subcategory", categories.subcategories(b)), ("category slug", [c["slug"] for c in categories.load(b)])]:
            dup = sorted({x for x in items if items.count(x) > 1})
            if dup:
                errors.append(f"{categories.path(b).relative_to(ROOT)}: same {what} twice (D-99): {', '.join(dup)}")
    rel = layout.REGIONAL_CATEGORIES.relative_to(ROOT)
    regional = (load_json(layout.REGIONAL_CATEGORIES, {}) or {}).get("categories", [])
    names = [c.get("name") for c in regional]
    if not all(isinstance(n, str) and n and c.get("scope") and c.get("excludes") for n, c in zip(names, regional)):
        errors.append(f"{rel}: every category needs name, scope and excludes (decision 213)")
    if dup := sorted({n for n in names if isinstance(n, str) and names.count(n) > 1}):
        errors.append(f"{rel}: same name twice: {', '.join(dup)}")
    slugs = [c["slug"] for c in regional if "slug" in c]
    if slugs and (len(slugs) < len(regional) or len(set(slugs)) < len(slugs)
                  or not all(isinstance(s, str) and categories.SLUG.fullmatch(s) for s in slugs)):
        errors.append(f"{rel}: every category needs its own slug (decision 259)")
    return errors


def slug_problems():
    """The slug rule (decision 259), on once names.es.json exists: keys are slugs, categories.json holds no names,
    names.{en,es,de}.json name every category and subcategory of every bundle (questions: validate_pool's key check)."""
    if not categories.slug_keys():
        return []
    errors = []
    for b in categories.bundle_ids():
        cats = categories.load(b)
        rel = categories.path(b).relative_to(ROOT)
        if bad := [c["slug"] for c in cats if not categories.SLUG.fullmatch(c["slug"])] + \
                  [s for s in categories.subcategories(b) if not (isinstance(s, str) and categories.SLUG.fullmatch(s))]:
            errors.append(f"{rel}: not a slug (decision 259): {first_ids(bad)}")
        if named_ := [c["slug"] for c in cats if "name" in c]:
            errors.append(f"{rel}: names go in the names files, not categories.json (decision 259): {first_ids(named_)}")
        for l in categories.NAMES_LOCALES:
            doc = load_json(layout.NAMES(l, b), {}) or {}
            missing = ([f"category {c['slug']}" for c in cats if c["slug"] not in (doc.get("categories") or {})]
                       + [f"subcategory {s}" for s in categories.subcategories(b) if s not in (doc.get("subcategories") or {})])
            if missing:
                errors.append(f"{layout.NAMES(l, b).relative_to(ROOT)}: {len(missing)} name(s) missing: {first_ids(missing)}")
    return errors


COUNTRY = r"[A-Z]{2}"  # a regional bundle's country (plan 151); COUNTRY in app/client/src/engine/pool.ts


def bundle_problems(bundles):
    """(errors, warnings): bundle languages and base bundles (plan 71)."""
    errors, warnings, rel = [], [], "app/data/bundles.json"
    for b in bundles:
        bid, langs = b.get("id", "?"), b.get("languages")
        if not (isinstance(langs, list) and langs and len(set(langs)) == len(langs) and set(langs) <= set(translations.LOCALES)):
            errors.append(f"{rel}: {bid}: languages must be a non-empty list of distinct codes from {', '.join(translations.LOCALES)}")
        if "always_on" in b:
            errors.append(f"{rel}: {bid}: always_on is gone; kind base marks a base bundle")
        if b.get("kind") not in {"base", "region", "theme"}:
            errors.append(f"{rel}: {bid}: kind must be base, region or theme")
        if b.get("kind") == "region" and not re.fullmatch(COUNTRY, str(b.get("country", ""))):
            errors.append(f"{rel}: {bid}: a regional bundle needs country, ISO 3166-1 alpha-2 in capitals (e.g. CO)")
        if b.get("kind") != "region" and "country" in b:
            errors.append(f"{rel}: {bid}: country only on a regional bundle")
    listed = {l: {b["id"] for b in bundles if l in (b.get("languages") or [])} for l in translations.LOCALES}
    for l in translations.LOCALES:
        path = layout.POOL_FILE(l, "base")
        if not (listed[l] or path.exists()):  # a locale without pool nor bundle, e.g. es-ES before its pool
            continue
        if not any(b.get("kind") == "base" and b["id"] in listed[l] for b in bundles):
            errors.append(f"{rel}: no base bundle for {l}")
        if l not in patch_notes.EVENT:
            errors.append(f"authoring/tools/patch_notes.py: no Steam event texts (EVENT) for {l}")
        missing = {b for b in listed[l] if not layout.POOL_FILE(l, b).exists()}
        warnings += [f"{layout.POOL_FILE(l, b).relative_to(ROOT)}: missing; {b} is listed for {l}" for b in sorted(missing)]
        pool = [q for p in layout.POOL_FILES() if p.name == path.name for q in load_json(p)["questions"]]
        have = {q.get("bundle") or "base" for q in pool if q.get("status", "approved") == "approved"}
        warnings += [f"{path.name}: no approved {b} question; {b} is listed for {l}" for b in sorted(listed[l] - have - missing)]
        warnings += [f"{path.name}: approved {b} questions, but {b} isn't listed for {l}" for b in sorted(have - listed[l])]
    return errors, warnings


CATEGORIES_ABOUT = ("Categories of the {bundle} bundle (D-41, D-43): structure only, keyed by English slugs unique "
                    "within the bundle (decision 259); names in names.<locale>.json.")


def cmd_bundle_new(args):
    """An empty bundle (BN-9, D-41): its entry in app/data/bundles.json, a regional one's 2000 target
    (D-101) and an empty categories.json, for a regional one filled by `qgen taxonomy` (plan 138), else by hand. Concept lists come from `qgen batch --bundle <id>`; axes stay base's until
    authoring/data/bundles/<id>/question-axes.json exists."""
    if not re.fullmatch(r"[a-z0-9-]+", args.id):
        sys.exit("A bundle id is lowercase letters, digits and dashes.")
    data = load_json(layout.BUNDLES)
    if any(b["id"] == args.id for b in data["bundles"]):
        sys.exit(f"Bundle {args.id!r} already exists.")
    if args.kind == "region" and not (args.language and args.voice and args.country):
        sys.exit("A regional bundle needs --language (the region's), --voice (its language variety) and --country.")
    if args.country and (args.kind != "region" or not re.fullmatch(COUNTRY, args.country)):
        sys.exit("--country: a regional bundle's ISO 3166-1 alpha-2 code in capitals, e.g. CO.")
    data["bundles"].append({"id": args.id, "kind": args.kind, **({"country": args.country} if args.country else {}),
                            "languages": [args.language or "es"], "name": args.name,
                            "description": args.description, "rule": args.rule,
                            **({"voice": args.voice} if args.voice else {})})
    save_json(layout.BUNDLES, data)
    if args.kind == "region":
        t = targets.load_all()
        save_json(layout.TARGETS, {**t, args.id: targets.scaled(targets.REGION_TOTAL)})
    path = categories.path(args.id)
    if not path.exists():
        save_json(path, {"about": CATEGORIES_ABOUT.format(bundle=args.id), "categories": []})
    nxt = (f"`qgen taxonomy --bundle {args.id}` proposes its categories and subcategories (plan 138), "
           f"`--apply` writes them" if args.kind == "region"
           else f"fill {path.relative_to(ROOT)} with broad categories and subcategories")
    print(f"Created bundle {args.id}. Next: {nxt}, then `qgen batch --bundle {args.id}`.")


PER_SUBCATEGORY = 40  # approved per subcategory a regional taxonomy is sized for (plan 138)
NAMES_MODEL = "sonnet"  # names of a taxonomy's new categories and subcategories
KEYED = {"slug": STR, "en": STR, "name": STR}  # key, English name, name in the bundle's language
TAXONOMY_SCHEMA = {"type": "object", "required": ["region", "categories", "left_out"], "properties": {
    "region": STR,
    "categories": {"type": "array", "items": {
        "type": "object", "required": [*KEYED, "origin", "scope", "reason", "subcategories"], "properties": {
            **KEYED, "origin": {"type": "string", "enum": ["general", "region"]}, "scope": STR, "reason": STR,
            "subcategories": {"type": "array", "items": {
                "type": "object", "required": [*KEYED, "scope", "reason", "samples"], "properties": {
                    **KEYED, "scope": STR, "reason": STR,
                    "samples": {"type": "array", "items": {"type": "object", "required": ["name", "known_at"],
                                                           "properties": {"name": STR, "known_at": INT}}}}}}}}},
    "left_out": {"type": "array", "items": {"type": "object", "required": ["name", "reason"],
                                            "properties": {"name": STR, "reason": STR}}}}}


def names_locale(locale):
    """The names file a locale's names go in: es-ES's in es's, which es-ES reads first (decision 259)."""
    return "es" if locale.startswith("es") else locale


def derived_slug(en, region):
    """A new entry's slug from its English name, without the region: "Rivers of Colombia" → rivers."""
    r = re.escape(slug(region))
    return re.sub(rf"^{r}-|-(of|in|from)-(the-)?{r}$", "", slug(en)) or slug(en)


def off_list(bundle, subs):
    """{subcategory: Counter(status)} of the bundle's questions on a subcategory not in subs."""
    out = {}
    for q in load_json(POOL)["questions"]:
        if q.get("bundle") == bundle and q["subcategory"] not in subs:
            out.setdefault(q["subcategory"], Counter())[q["status"]] += 1
    return out


def off_list_lines(found):
    return [f"- {s}: {sum(c.values())} ({', '.join(f'{n} {st}' for st, n in c.most_common())})"
            for s, c in sorted(found.items(), key=lambda x: -sum(x[1].values()))]


def keyed(x):
    """`slug` English name (own-language name, if another)."""
    return f"`{x['slug']}` {x['en']}" + (f" ({x['name']})" if x["name"] != x["en"] else "")


def taxonomy_md(p, found):
    """proposal.md: what goes into the pm decision (decision 18's format)."""
    cats = p["categories"]
    n = sum(len(c["subcategories"]) for c in cats)
    lines = [f"# Taxonomy proposal: `{p['bundle']}`", "",
             f"{len(cats)} categories, {n} subcategories; target {p['target']} approved, "
             f"≈ {round(p['target'] / max(n, 1))} per subcategory. Each: `slug` English name (name in the bundle's "
             "language). Sample concepts: name (known_at).", "",
             "## Counts per category"]
    lines += [f"- {keyed(c)}{' (region)' if c['origin'] == 'region' else ''}: {len(c['subcategories'])}" for c in cats]
    if p["left_out"]:
        lines += ["", "## Left out of the general list"] + [f"- {c['name']}: {c['reason']}" for c in p["left_out"]]
    i = 0
    for c in cats:
        lines += ["", f"## {keyed(c)}{' (region)' if c['origin'] == 'region' else ''}", f"{c['scope']}"
                  + (f" Reason: {c['reason']}" if c["reason"] else "")]
        for s in c["subcategories"]:
            i += 1
            samples = ", ".join(f"{x['name']} ({x['known_at']})" for x in sorted(s["samples"], key=lambda x: x["known_at"]))
            lines.append(f"{i}. **{keyed(s)}**. {s['scope']} Reason: {s['reason']} Samples: {samples}.")
    if found:
        lines += ["", "## Questions on subcategories not in the proposal (moved by the remap)"] + off_list_lines(found)
    return "\n".join(lines) + "\n"


def cmd_taxonomy(args):
    """A regional bundle's taxonomy (plan 138, decision 259): one opus call proposes categories and subcategories
    (slug, English name, name in the bundle's language) from the general list (decision 213), the bundle's rule and
    voice and its target → work/taxonomy/<id>/proposal.{json,md}; `--apply <proposal.json>` writes categories.json
    and names.<locale>.json, touching no question or concept list."""
    b = next((x for x in load_bundles() if x["id"] == args.bundle), None)
    if not b or b["kind"] != "region":
        sys.exit(f"{args.bundle!r} is not a regional bundle in app/data/bundles.json")
    d = WORK / "taxonomy" / args.bundle
    d.mkdir(parents=True, exist_ok=True)
    if args.apply:
        return apply_taxonomy(args.bundle, Path(args.apply), d)
    total = targets.load_targets(args.bundle)["total"]
    per = PER_SUBCATEGORY
    loc = translations.draft_locale(b)
    system = (PROMPTS / "taxonomy.md").read_text(encoding="utf-8").replace("{per_sub}", str(per)).replace(
        "{subs}", str(round(total / per))).replace("{language}", LANGUAGES[loc])
    approved = Counter(q["subcategory"] for q in load_json(POOL)["questions"]
                       if q.get("bundle") == args.bundle and q["status"] == "approved")
    general = load_json(layout.REGIONAL_CATEGORIES)
    def own(x, kind):
        en, name = (categories.display(args.bundle, x, l, kind) for l in ("en", loc))
        return keyed({"slug": x, "en": en, "name": name})
    user = "\n\n".join([
        f"## Bundle\n`{args.bundle}`: {b['name']}\nLanguage: {LANGUAGES[loc]}\n{bundle_text(args.bundle, loc)}",
        f"## Target\n{total} approved questions: ≈ {round(total / per)} subcategories of ≈ {per}.",
        f"## General list\n{general['about']}\n" + json.dumps(general["categories"], ensure_ascii=False, indent=1),
        "## base's subcategories\n" + "\n".join(f"- {cat_name(c, 'en')}: {', '.join(categories.display('base', s, 'en') for s in c['subcategories'])}"
                                                 for c in categories.load("base")),
        "## Existing taxonomy (context only; `slug` English name (own name): approved questions)\n" + ("\n".join(
            f"- {own(c['slug'], 'categories')}: " + ", ".join(f"{own(s, 'subcategories')}: {approved[s]}" for s in c["subcategories"])
            for c in categories.load(args.bundle)) or "none")])
    out = claude(system, user, TAXONOMY_SCHEMA, args.model, d)
    for x in [c for c in out["categories"]] + [s for c in out["categories"] for s in c["subcategories"]]:
        x["slug"] = slug(x["slug"])
    p = {"bundle": args.bundle, "target": total, **out}
    save_json(d / "proposal.json", p)
    subs = {s["slug"] for c in p["categories"] for s in c["subcategories"]}
    (d / "proposal.md").write_text(taxonomy_md(p, off_list(args.bundle, subs)), encoding="utf-8")
    print(f"{len(p['categories'])} categories, {len(subs)} subcategories → {(d / 'proposal.md').relative_to(ROOT)}; "
          f"edit proposal.json to the developer's answer, then `qgen taxonomy --bundle {args.bundle} --apply "
          f"{(d / 'proposal.json').relative_to(ROOT)}`")


def cat_name(c, locale):
    """A loaded category's display name (decision 259)."""
    return categories.display(c["bundle"], c["slug"], locale, "categories")


def taxonomy_errors(p, bundle):
    errors = [] if p.get("bundle") == bundle else [f"bundle must be {bundle!r}"]
    cats = p.get("categories") or []
    for what, items in [("category", cats), ("subcategory", [s for c in cats for s in c.get("subcategories") or []])]:
        for f in KEYED:
            vals = [x.get(f) for x in items]
            if not all(isinstance(v, str) and v.strip() for v in vals):
                errors.append(f"every {what} needs a non-empty {f}")
            elif dup := sorted({v for v in vals if vals.count(v) > 1}):
                errors.append(f"same {what} {f} twice: {', '.join(dup)}")
        if bad := [x["slug"] for x in items if isinstance(x.get("slug"), str) and not categories.SLUG.fullmatch(x["slug"])]:
            errors.append(f"not a slug (decision 259): {', '.join(bad)}")
    errors += [f"{c.get('slug')}: no subcategories" for c in cats if not c.get("subcategories")]
    return errors + ([] if cats else ["no categories"])


def apply_taxonomy(bundle, src, d):
    """Writes the bundle's categories.json and its names files (stale entries dropped, missing ones drafted)."""
    p = load_json(src)
    if p is None:
        sys.exit(f"{src}: not found")
    if errors := taxonomy_errors(p, bundle):
        sys.exit(f"{src}: " + "; ".join(errors))
    subs = write_taxonomy(bundle, p, d)
    if found := off_list(bundle, set(subs)):
        print(f"{sum(sum(c.values()) for c in found.values())} {bundle} question(s) on subcategories not in the list "
              f"(`qgen remap --bundle {bundle}` moves them):\n" + "\n".join(off_list_lines(found)))
    errors, _ = validate_pool()
    if errors:
        print(f"qgen validate fails ({len(errors)} error(s)); expected only for questions on subcategories not in "
              f"the list:\n" + "\n".join(f"  {e}" for e in errors[:20]))


def draft_names(bundle, todo, d):
    """Fills each entry's missing names ({locale: name}) in names.{en,es,de}.json's locales, from its English
    name where it has one, else from its name in the bundle's language."""
    b = bundle_row(bundle)
    by_src = {}
    for i, e in enumerate(todo):
        by_src.setdefault("en" if "en" in e["names"] else next(iter(e["names"])), []).append((str(i), e))
    for src, items in by_src.items():
        locales = [l for l in categories.NAMES_LOCALES if any(l not in e["names"] for _, e in items)]
        rows = [{"key": k, "name": e["names"][src], "scope": e.get("scope", "")} for k, e in items]
        schema = {"type": "object", "required": ["items"], "properties": {"items": {"type": "array", "items": {
            "type": "object", "required": ["key", *locales], "properties": {"key": STR, **{l: STR for l in locales}}}}}}
        vl = names_locale(voice_locale(b))
        voice = f"\n\n## Voice\n`{vl}`: {b['voice']}" if b.get("voice") and vl in locales else ""
        user = ("## Target languages\n" + "\n".join(f"- `{l}`: {'Spanish (Latin America and Spain)' if l == 'es' else LANGUAGES[l]}"
                                                for l in locales) + voice
                + "\n\n## Names\n" + json.dumps(rows, ensure_ascii=False, indent=1))
        system = (PROMPTS / "taxonomy-names.md").read_text(encoding="utf-8").replace("{source}", LANGUAGES[src])
        got = {r["key"]: r for r in claude(system, user, schema, NAMES_MODEL, d)["items"]}
        if missing := [e["names"][src] for k, e in items if k not in got]:
            sys.exit(f"nothing written; no names drafted for {', '.join(missing)}: rerun")
        for k, e in items:
            e["names"] = {l: got[k][l] for l in locales} | e["names"]


def write_taxonomy(bundle, p, d):
    """categories.json (structure only) and names.{en,es,de}.json from a proposal (decision 259): an entry's `en` and
    `name` (the bundle's language) win over the names files, missing names are drafted; an entry without `slug`
    (a remap's new one) gets one from its English name. `scope` only needed for drafted names. Returns the subcategories."""
    own = names_locale(translations.draft_locale(bundle_row(bundle)))
    files = {l: load_json(layout.NAMES(l, bundle)) or {"version": 1, "locale": l} for l in categories.NAMES_LOCALES}
    entries = {k: [] for k in categories.NAME_KINDS}
    for c in p["categories"]:
        entries["categories"].append(c)
        entries["subcategories"] += c["subcategories"]
    for k, es in entries.items():
        for e in es:
            have = {l: n for l in files if e.get("slug") and (n := (files[l].get(k) or {}).get(e["slug"]))}
            e["names"] = have | {l: v for l, v in [("en", e.get("en")), (own, e.get("name"))] if v}
            if not e["names"]:
                e["names"] = {own: e["slug"]}
    draft_names(bundle, [e for es in entries.values() for e in es if len(e["names"]) < len(files)], d)
    for es in entries.values():
        used = {e["slug"] for e in es if e.get("slug")}
        for e in es:
            if not e.get("slug"):
                s = base_ = derived_slug(e["names"]["en"], p.get("region") or bundle)
                n = 1
                while s in used:
                    n += 1
                    s = f"{base_}-{n}"
                used.add(e.setdefault("slug", s))
    path = categories.path(bundle)
    doc = load_json(path, {})
    cats = [{"slug": c["slug"], "subcategories": [s["slug"] for s in c["subcategories"]]} for c in p["categories"]]
    save_json(path, {"about": doc.get("about") or CATEGORIES_ABOUT.format(bundle=bundle), "categories": cats})
    subs = [s for c in cats for s in c["subcategories"]]
    print(f"{path.relative_to(ROOT)}: {len(cats)} categories, {len(subs)} subcategories")
    for l, f in files.items():
        changed = stale = 0
        for k, es in entries.items():
            have = f.get(k) or {}
            stale += len(set(have) - {e["slug"] for e in es})
            changed += sum(have.get(e["slug"]) != e["names"][l] for e in es)
            f[k] = {e["slug"]: e["names"][l] for e in es}
        save_json(layout.NAMES(l, bundle), f)
        print(f"{layout.NAMES(l, bundle).relative_to(ROOT)}: {changed} name(s) new or changed, {stale} dropped")
    return subs


REMAP_SCHEMA = {"type": "object", "required": ["questions", "lists"], "properties": {
    "questions": {"type": "array", "items": {"type": "object", "required": ["id", "subcategory", "category", "scope", "reason"],
                                            "properties": {"id": STR, "subcategory": STR, "category": STR, "scope": STR, "reason": STR}}},
    "lists": {"type": "array", "items": {"type": "object", "required": ["subcategory", "target", "reason"],
                                        "properties": {"subcategory": STR, "target": STR, "reason": STR}}}}}


def old_lists(bundle, subs):
    """{subcategory: list} of the bundle's concept lists whose subcategory is not in subs."""
    out = {}
    for p in sorted(concepts.concepts_dir(bundle).glob("*.json")):
        lst = load_json(p)
        if lst.get("subcategory") not in subs:
            out[lst.get("subcategory") or p.stem] = lst
    return out


def remap_errors(p, bundle):
    """Problems of a remap proposal against the bundle's list; new subcategories must agree across questions."""
    loc = translations.draft_locale(bundle_row(bundle))
    subs, cats = set(categories.subcategories(bundle)), {cat_name(c, loc) for c in categories.load(bundle)}
    ids = {q["id"] for q in load_json(POOL)["questions"] if q.get("bundle") == bundle}
    got = {r["id"] for r in p["questions"]}
    errors = [f"no subcategory for {', '.join(sorted(ids - got))}"] if ids - got else []
    errors += [f"{i}: not a {bundle} question" for i in sorted(got - ids)]
    new = {}
    for r in p["questions"]:
        if r["subcategory"] in subs:
            continue
        if not (r["category"].strip() and r["scope"].strip()):
            errors.append(f"{r['id']}: {r['subcategory']!r} is not in the list and has no category and scope")
        elif new.setdefault(r["subcategory"], r["category"]) != r["category"]:
            errors.append(f"{r['subcategory']!r}: in two categories")
    targets_ = subs | set(new)
    errors += [f"list {x['subcategory']!r}: target {x['target']!r} is not a subcategory" for x in p["lists"]
               if x["target"] and x["target"] not in targets_]
    return errors, new, cats


def remap_md(p, new, cats, by_id):
    lines = [f"# Remap proposal: `{p['bundle']}`", "", f"{len(p['questions'])} questions; "
             f"{sum(r['subcategory'] != by_id[r['id']]['subcategory'] for r in p['questions'] if r['id'] in by_id)} change subcategory.", ""]
    if new:
        lines += ["## Additions"] + [f"- {s} → {c}{'' if c in cats else ' (new category)'}" for s, c in sorted(new.items())] + [""]
    lines += ["## Questions"]
    for r in sorted((r for r in p["questions"] if r["id"] in by_id), key=lambda r: (r["subcategory"], r["id"])):
        q = by_id[r["id"]]
        lines.append(f"- {r['id']} ({q['status']}) {q['subcategory']} → **{r['subcategory']}**: {q['question'][:80]} "
                     f"→ {q['answer']}" + (f" ({r['reason']})" if r["reason"] else ""))
    lines += ["", "## Old concept lists"] + [f"- {x['subcategory']} → {x['target'] or 'deleted'} ({x['reason']})" for x in p["lists"]]
    return "\n".join(lines) + "\n"


def cmd_remap(args):
    """A regional bundle's questions onto its new taxonomy (plan 138, decision 166): one opus call proposes a
    subcategory per question (all statuses) and a target for every concept list whose subcategory is gone
    → work/remap/<id>/proposal.{json,md}; `--apply <proposal.json>` adds new subcategories to categories.json
    (names drafted), renames or deletes old concept lists, moves the questions and their concepts (BN-13)."""
    b = next((x for x in load_bundles() if x["id"] == args.bundle), None)
    if not b or b["kind"] != "region":
        sys.exit(f"{args.bundle!r} is not a regional bundle in app/data/bundles.json")
    d = WORK / "remap" / args.bundle
    d.mkdir(parents=True, exist_ok=True)
    if args.apply:
        return apply_remap(args, Path(args.apply), d)
    subs = categories.subcategories(args.bundle)
    tx = load_json(WORK / "taxonomy" / args.bundle / "proposal.json", {}) or {}
    scopes = {s.get("slug") or s["name"]: s["scope"] for c in tx.get("categories", []) for s in c["subcategories"]}
    qs = [q for q in load_json(POOL)["questions"] if q.get("bundle") == args.bundle]
    lists = old_lists(args.bundle, set(subs))
    loc = translations.draft_locale(b)
    shown = lambda s: categories.display(args.bundle, s, loc) if s in subs else categories.display("base", s, loc)
    user = "\n\n".join([
        f"## Bundle\n`{args.bundle}`: {b['name']}\n{bundle_text(args.bundle, loc)}",
        "## New list\n" + "\n".join(f"### {cat_name(c, loc)}\n" + "\n".join(
            f"- {shown(s)}" + (f": {sc}" if (sc := scopes.get(s) or scopes.get(shown(s))) else "")
            for s in c["subcategories"]) for c in categories.load(args.bundle)),
        "## Questions\n" + json.dumps([{k: q.get(k) for k in ["id", "question", "answer", "hints", "concept"]}
                                       | {"subcategory": shown(q["subcategory"])} for q in qs], ensure_ascii=False),
        "## Old concept lists\n" + (json.dumps([{"subcategory": shown(s), "facets": l.get("facets", []), "concepts": len(l["concepts"]),
                                                 "examples": [c["name"] for c in l["concepts"][:25]]}
                                                for s, l in lists.items()], ensure_ascii=False) if lists else "none")])
    out = claude((PROMPTS / "remap.md").read_text(encoding="utf-8"), user, REMAP_SCHEMA, args.model, d)
    for r in out["questions"]:  # names back to keys; a new subcategory keeps its name
        r["subcategory"] = categories.resolve(args.bundle, r["subcategory"]) or r["subcategory"]
    by_name = {shown(s): s for s in lists}
    for x in out["lists"]:
        x["subcategory"] = by_name.get(x["subcategory"], x["subcategory"])
        x["target"] = x["target"] and (categories.resolve(args.bundle, x["target"]) or x["target"])
    p = {"bundle": args.bundle, **out}
    save_json(d / "proposal.json", p)
    errors, new, cats = remap_errors(p, args.bundle)
    (d / "proposal.md").write_text(remap_md(p, new, cats, {q["id"]: q for q in qs}), encoding="utf-8")
    print(f"{(d / 'proposal.md').relative_to(ROOT)}: {len(new)} new subcategories; then `qgen remap --bundle "
          f"{args.bundle} --apply {(d / 'proposal.json').relative_to(ROOT)}`")
    if errors:
        sys.exit("proposal has problems (edit proposal.json or rerun):\n" + "\n".join(f"  {e}" for e in errors))


def apply_remap(args, src, d):
    bundle = args.bundle
    p = load_json(src)
    if p is None or p.get("bundle") != bundle:
        sys.exit(f"{src}: no remap proposal for {bundle}")
    errors, new, cats = remap_errors(p, bundle)
    if errors:
        sys.exit(f"{src}:\n" + "\n".join(f"  {e}" for e in errors))
    lo, hi = load_age_groups()["scale"]
    data = load_json(POOL)
    sources = {}  # concept key → its entry in the list the question used before
    for q in data["questions"]:
        if q.get("bundle") == bundle and q.get("concept"):
            lst = concepts.load(*categories.key(q)) or concepts.load("base", q["subcategory"]) or {}
            sources |= {concepts.key(c["name"]): c for c in lst.get("concepts", []) if c["name"] == q["concept"]}
    if new:  # new subcategories (and categories) come as names in the bundle's language: slugs from their en names
        scope = {r["subcategory"]: r["scope"] for r in p["questions"]}
        cats_ = [{"slug": c["slug"], "scope": "", "subcategories": [{"slug": s, "scope": ""} for s in c["subcategories"]]}
                 for c in categories.load(bundle)]
        for s, c in new.items():
            cid = categories.resolve(bundle, c, "categories")
            cat = next((x for x in cats_ if (x.get("slug") == cid if cid else x.get("name") == c)), None)
            if not cat:
                cat = {"name": c, "scope": scope[s], "subcategories": []}
                cats_.append(cat)
            cat["subcategories"].append({"name": s, "scope": scope[s]})
        tx = load_json(WORK / "taxonomy" / bundle / "proposal.json", {}) or {}
        write_taxonomy(bundle, {"bundle": bundle, "region": tx.get("region"), "categories": cats_}, d)
    key_of = lambda t: t and (categories.resolve(bundle, t) or t)
    subs = set(categories.subcategories(bundle))
    for s, lst in old_lists(bundle, subs).items():
        t = key_of(next((x["target"] for x in p["lists"] if x["subcategory"] == s), ""))
        concepts.path(bundle, s).unlink()
        if not t:
            print(f"  concept list {s}: deleted ({len(lst['concepts'])} concepts)")
            continue
        have = concepts.load(bundle, t)
        if have:  # a second list for the same target: merged
            own = {concepts.key(c["name"]) for c in have["concepts"]}
            have["concepts"] += [c for c in lst["concepts"] if concepts.key(c["name"]) not in own]
            have["facets"] += [f for f in lst.get("facets", []) if f not in have["facets"]]
            lst = have
        concepts.save(bundle, t, {**lst, "subcategory": t})
        print(f"  concept list {s} → {t}")
    moved, kept, cleared = [], 0, 0
    with atomic.locked(POOL):
        data = load_json(POOL)
        target = {r["id"]: key_of(r["subcategory"]) for r in p["questions"]}
        for q in data["questions"]:
            if q.get("bundle") != bundle:
                continue
            if q["subcategory"] != target[q["id"]]:
                moved.append(f"{q['id']}: {q['subcategory']} → {target[q['id']]}")
                q["subcategory"] = target[q["id"]]
            if not q.get("concept"):
                continue
            lst = concepts.load(bundle, q["subcategory"])
            if lst is None:
                q.pop("concept")
                cleared += 1
                continue
            k = concepts.key(q["concept"])
            if same := next((c["name"] for c in lst["concepts"] if concepts.key(c["name"]) == k), None):
                q["concept"] = same
            else:
                src_ = sources.get(k, {})
                facet = src_.get("facet") or (lst.get("facets") or ["general"])[0]
                if facet not in lst.setdefault("facets", []):
                    lst["facets"].append(facet)
                lst["concepts"].append({"name": q["concept"], "facet": facet,
                                        "known_at": min(hi, max(lo, src_.get("known_at") or q["difficulty"]))})
                concepts.save(bundle, q["subcategory"], lst)
            kept += 1
        save_json(POOL, data)
        cmd_export(args)
    print("\n".join(f"  {m}" for m in moved))
    print(f"{len(moved)} question(s) moved, {len(new)} subcategories added; concepts: {kept} kept, {cleared} cleared (BN-13)")


def cmd_validate(args):
    errors, warnings = validate_pool()
    if warnings:
        print("\n".join(f"warning: {w}" for w in warnings))
        print(f"({len(warnings)} warning(s); `trivia-media sync --status approved` fills the cache)")
    tag, _ = released_ids()
    print(f"id continuity: checked against {tag}" if tag else "id continuity: skipped, no v* tag")
    print("\n".join(errors) or f"OK: {len(load_json(POOL)['questions'])} questions")
    sys.exit(1 if errors else 0)


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
                      help="region: the locale it drafts in, its only `languages` entry until en joins (decision 110); theme: default es")
    bnew.add_argument("--country", help="region: its ISO 3166-1 alpha-2 code in capitals, e.g. CO; the game shows its flag")
    bnew.add_argument("--rule", required=True, help="one English sentence: when a question belongs in it")
    bnew.add_argument("--voice", help="English: the language variety of its own text in prompts, e.g. \"British English: …\" "
                      f"(region: required; theme: its es text, default: {VOICE})")
    tx = add("taxonomy", cmd_taxonomy, "opus", run=False)
    tx.add_argument("--bundle", required=True, help="a regional bundle")
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
    rp.add_argument("--players", type=int, help="with --simulate: players in rr-competitive and timed (default 4)")
    rp.add_argument("--seeds", type=int, default=40, help="with --simulate: runs per cell")
    rp.add_argument("--cost", action="store_true",
                    help="$ per run and per approved by run kind, projection per launch language and per regional bundle "
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


if __name__ == "__main__":
    main()
