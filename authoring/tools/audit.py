"""`qgen audit` and the back-audit (plan 16, D-56). Never ships (D-35)."""
import datetime, json, random, sys
from collections import Counter

import layout  # paths (D-35)
from layout import REPO as ROOT, SOURCE_POOL as POOL, WORK
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import media as media_tool  # authoring/tools/media.py: candidates, sheets, picks (`media` is the cache)
import targets  # authoring/tools/targets.py: pool targets (D-53)
import translations  # authoring/tools/translations.py: translated questions (D-81)

from qgen import PROBLEMS, INT, QUESTION_FIELDS, REVIEW_URL, STR, UsageLimit, as_locale, claude, costs, failed, load_age_groups, load_json, named, parallel, prompt, save_json, write_report  # authoring/tools/qgen.py


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


# the other command groups, after everything here is defined (they import each other)
from report import qc_section  # authoring/tools/report.py
from review_steps import related_questions, run_mode  # authoring/tools/review_steps.py
from translate import in_locale, run_bundle, run_locale  # authoring/tools/translate.py
