"""`qgen rework` and `tighten`: scans and revisions of the whole pool (QG-23, QG-24). Never ships (D-35)."""
import argparse, datetime, json, sys, time

import layout  # paths (D-35)
from layout import REPO as ROOT, SOURCE_POOL as POOL, WORK
import media_first  # authoring/tools/media_first.py: fixed media slot checks (plan 203)
import flag_loop  # authoring/tools/flag_loop.py
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import translations  # authoring/tools/translations.py: translated questions (D-81)

from qgen import STR, claude, cmd_export, cmd_sync_run, load_json, locale_chunks, parallel, prompt, run_dir, run_steps, save_json  # authoring/tools/qgen.py


def revise_steps(ns, model, review_model):
    """fix → fact check → review with a new media search (a media-first question: background only) → record: rework and the scan modes (QG-23);
    a scan run searches only slots without a kept pick (kept_slots)."""
    return [
        ("fix", cmd_fix, ns(model=model, check_model="sonnet")),
        ("giveaway", lambda a: media_first.check_fixed(a.run), ns()),  # media-first questions only (plan 203)
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
        flagged = [q["id"] for q in load_json(POOL)["questions"] if q["id"] in ids
                   and flag_loop.is_player_feedback(q["review"]["feedback"])]
        save_json(WORK / run / "run.json", {"mode": "rework", "ids": ids, "flagged": flagged, "batch": args.batch,
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
    record_flag_causes(run, cfg.get("flagged", []))
    files = ["authoring/data/questions.json", "authoring/data/flag-causes.json", "app/data/pool.json", "app/data/bundles/", "app/data/demo/", *stale_lines(set(cfg["ids"]), by_id)]
    print(f"Commit exactly this:\n  git add {' '.join(files)}\n"
          f"  git commit -m \"{run}: {n_ok} of {len(qs)} needs_work questions fixed and approved (qgen rework)\"")


def record_flag_causes(run, flagged):
    """The reviser's cause for each reworked player flag → authoring/data/flag-causes.json (git add it); repeated causes print a proposal."""
    rows = []
    for i in flagged:
        fix = (load_json(WORK / run / "reviews" / f"{i}.json", {})).get("fix") or {}
        rows.append({"id": i, "cause": fix.get("cause", "other"), "action": fix.get("action"), "reason": fix.get("reason")})
    if flagged and not any(r["run"] == run for r in flag_loop.causes()):  # a resumed run records once
        flag_loop.record_causes(run, rows)
        print(f"Flag causes: {len(rows)} recorded in authoring/data/flag-causes.json (git add it).")
    for line in flag_loop.lesson_lines()[1:]:
        print(line)


SCAN_SCHEMA = {"type": "object", "required": ["flagged"], "properties": {"flagged": {"type": "array", "items": {
    "type": "object", "required": ["id", "issue"], "properties": {"id": STR, "issue": STR}}}}}
SCAN_CHUNK = 50
SCANS = {  # run mode: scan prompt, questions read, their input, the reviser's issue prefix (QG-24)
    "tighten": {"prompt": "tighten", "bundle": None, "issue": "too long", "schema": SCAN_SCHEMA,
                "item": lambda q: {"id": q["id"], "clue": (q.get("axes") or {}).get("clue"), "question": q["question"]}},
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
          and (not scan["bundle"] or (q.get("bundle") or "base") == scan["bundle"]) and (not only or q["id"] in only)]
    groups = [g for g in locale_chunks(qs, SCAN_CHUNK) if not (d / "scan" / f"{g[0]['id']}.json").exists()]

    def work(group):
        items = [scan["item"](q) for q in group]
        system = prompt("house-style", scan["prompt"], locale=translations.source_locale(group[0]))
        out = claude(system, "## Questions\n" + json.dumps(items, ensure_ascii=False), scan["schema"], args.model, d)
        ids = {q["id"] for q in group}
        save_json(d / "scan" / f"{group[0]['id']}.json", [f for f in out["flagged"] if f["id"] in ids])

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
    files = ["authoring/data/questions.json", "app/data/pool.json", "app/data/bundles/", "app/data/demo/", *stale_lines(revised, by_id)]
    print(f"Commit exactly this:\n  git add {' '.join(files)}\n"
          f"  git commit -m \"{run}: {len(revised)} long-winded questions shortened, {n_ok} approved (qgen tighten)\"")


def stale_lines(revised, by_id):
    """Prints per locale how many translations the rewritten questions staled (D-81); returns the
    base pool paths (`es`: pool.json) export rewrote."""
    files = []
    for l in translations.LOCALES:
        if translations.path(l).exists():
            src = translations.load(l)["questions"]
            n = sum(t["id"] in by_id and translations.is_stale(t, by_id[t["id"]]) for t in src if t["id"] in revised)
            print(f"  {l}: {n} translation(s) stale from this run (D-81)")
            files.append(layout.POOL_FILE(l, "base").relative_to(ROOT).as_posix())
    return files


# the other command groups, after everything here is defined (they import each other)
from audit import cmd_audit, mode_run  # authoring/tools/audit.py
from review_steps import REVIEW_MODEL, batch_questions, cmd_fix, cmd_media, cmd_record, cmd_research, cmd_review, cmd_sheets, fixed  # authoring/tools/review_steps.py
