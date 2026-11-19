"""`qgen rework`: needs_work questions once more through fix and review (QG-23). Never ships (D-35)."""
import argparse, datetime, sys, time

import layout  # paths (D-35)
from layout import REPO as ROOT, SOURCE_POOL as POOL, WORK
import media_first  # authoring/tools/media_first.py: fixed media slot checks (plan 203)
import flag_loop  # authoring/tools/flag_loop.py
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import translations  # authoring/tools/translations.py: translated questions (D-81)

from qgen import cmd_export, cmd_sync_run, load_json, run_steps, save_json  # authoring/tools/qgen.py


def revise_steps(ns, model, review_model):
    """fix → fact check → review with a new media search (a media-first question: background only) → record: rework (QG-23)."""
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
from audit import mode_run  # authoring/tools/audit.py
from review_steps import REVIEW_MODEL, batch_questions, cmd_fix, cmd_media, cmd_record, cmd_research, cmd_review, cmd_sheets  # authoring/tools/review_steps.py
