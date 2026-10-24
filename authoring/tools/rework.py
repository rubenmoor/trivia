"""`qgen rework`, `tighten` and `neutralize`: scans and revisions of the whole pool (QG-23, QG-24, plan 64). Never ships (D-35)."""
import argparse, datetime, json, sys, time

import layout  # paths (D-35)
from layout import REPO as ROOT, SOURCE_POOL as POOL, WORK
import progress  # authoring/tools/progress.py: the plain log (QG-18, task 1131)
import translations  # authoring/tools/translations.py: translated questions (D-81)

from qgen import FACT_FIELDS, STR, claude, cmd_export, cmd_sync_run, costs, load_json, locale_chunks, parallel, prompt, run_dir, run_steps, save_json, split_list, write_report  # authoring/tools/qgen.py


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
    files = ["authoring/data/questions.json", "app/data/pool.json", "app/data/bundles/", "app/data/demo/", *stale_lines(set(cfg["ids"]), by_id)]
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
    files = ["authoring/data/questions.json", "app/data/pool.json", "app/data/bundles/", "app/data/demo/", *stale_lines(revised, by_id)]
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
    files = ["authoring/data/questions.json", "app/data/pool.json", "app/data/bundles/", "app/data/demo/", out.relative_to(ROOT).as_posix(),
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


# the other command groups, after everything here is defined (they import each other)
from audit import AUDIT_SAMPLE, audit_section, cmd_audit, mode_run  # authoring/tools/audit.py
from report import qc_section  # authoring/tools/report.py
from review_steps import REVIEW_MODEL, batch_questions, cmd_fix, cmd_media, cmd_record, cmd_research, cmd_review, cmd_sheets, fixed  # authoring/tools/review_steps.py
