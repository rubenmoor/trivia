"""`qgen batch --bundle <base bundle> --from base`: the fit pass (plan 230). Which approved `base` questions fit another
base bundle's audience (prompts/fit.md), and copies of those that do (decision 217). Never ships (D-35).

select → fit → copy → (adapted copies: rework's revise steps, audit) → export → sync → validate → report.
Verdicts: authoring/data/bundles/<id>/fit.json, the record of what is judged."""
import argparse, datetime, math, sys, time
from collections import Counter

import layout  # paths (D-35)
from layout import PROMPTS, REPO as ROOT, SOURCE_POOL as POOL, WORK
import atomic  # authoring/tools/atomic.py
import categories  # authoring/tools/categories.py
import copies  # authoring/tools/copies.py: the copy helper (decision 217)
import progress  # authoring/tools/progress.py
import translations  # authoring/tools/translations.py

from qgen import (STR, REVIEW_URL, bundle_row, check_bundle, claude, cmd_export, cmd_sync_run, costs, duplicates, fit_item,  # authoring/tools/qgen.py
                  fit_system, fit_text, fit_user, load_json, lock_run, natural_key, parallel, run_steps, save_json, write_report)

FIT_CHUNK = 50  # sources per fit call (the old scans' chunk)
FIT_SIZE = 600  # sources judged per run: plan 230's pilot; the pilot decision sets the full runs'
FIT_MODEL = "opus"
VERDICTS = ("keep", "adapt", "drop")
REASONS = ("euro_centric", "latam_centric", "wordplay", "sensitivity", "too_hard_here", "other")
BY = ("fit", "map", "rule", "developer")
ADAPT = "adapt for a Chinese family"  # the reviser's issue prefix (plan 230)
FIT_SCHEMA = {"type": "object", "required": ["items"], "properties": {"items": {"type": "array", "items": {
    "type": "object", "required": ["id", "verdict", "reason", "note", "issue"],
    "properties": {"id": STR, "verdict": {"type": "string", "enum": list(VERDICTS)},
                   "reason": {"type": ["string", "null"], "enum": [*REASONS, None]}, "note": STR,
                   "issue": {"type": ["string", "null"]}}}}}}


def en_translations():
    return {t["id"]: t for t in translations.load("en")["questions"]}


def verdicts(bundle):
    """{base source id: entry} of fit.json."""
    return (load_json(layout.fit(bundle), {}) or {}).get("sources", {})


def save_verdicts(bundle, entries):
    save_json(layout.fit(bundle), {
        "about": f"Plan 230: the fit verdict per `base` source for `{bundle}` (verdict, reason, note, run, by: fit, map, "
                 "rule or developer; copy: the copy's id). Written by `qgen batch --from base` and the fit view.",
        "sources": dict(sorted(entries.items(), key=lambda kv: natural_key(kv[0])))})


def subcategory_map(bundle):
    return (load_json(layout.from_base(bundle), {}) or {}).get("subcategories", {})


def base_sources(pool):
    """Approved `base` sources (no copies), in id order."""
    return sorted((q for q in pool if q.get("bundle") == "base" and q["status"] == "approved" and not q.get("copied_from")),
                  key=lambda q: natural_key(q["id"]))


def select(bundle, pool, tr, count):
    """The next run's work: `rule` {id: drop entry} (map null, translatable false; no call), `sources` (to judge, at most
    `count`, spread over the subcategories), `flipped` (the developer's keeps without a copy), `not_copyable` (no
    approved, current English text), `left` (to judge in later runs). Already judged sources are skipped."""
    m, seen = subcategory_map(bundle), verdicts(bundle)
    copied = {q["copied_from"] for q in pool if q.get("bundle") == bundle and q.get("copied_from")}
    flipped = [i for i, e in seen.items() if e["by"] == "developer" and e["verdict"] in ("keep", "adapt")
               and not e.get("copy") and i not in copied]
    rule, todo, not_copyable = {}, {}, []
    for q in base_sources(pool):
        if q["id"] in seen:
            continue
        to = m[q["subcategory"]]
        if to["to"] is None:
            rule[q["id"]] = {"verdict": "drop", "reason": to["reason"], "by": to["by"],
                             "note": f"base subcategory {q['subcategory']} has no {bundle} subcategory (from-base.json)"}
        elif not translations.translatable(q):
            rule[q["id"]] = {"verdict": "drop", "reason": "wordplay", "by": "rule",
                             "note": "translatable: false (lives on one language)"}
        elif fit_text(q, tr) is None:
            not_copyable.append(q["id"])
        else:
            todo.setdefault(q["subcategory"], []).append(q["id"])
    order = [s for s in categories.subcategories("base") if s in todo] + sorted(set(todo) - set(categories.subcategories("base")))
    spread = [ids[k] for k in range(max(map(len, todo.values()), default=0)) for s in order if k < len(ids := todo[s])]
    return {"rule": rule, "sources": spread[:count], "flipped": flipped, "not_copyable": not_copyable,
            "left": max(0, len(spread) - count)}


def refuse(bundle, src, pool):
    """Exit unless `--from src` can copy into `bundle` (plan 230)."""
    import validate  # authoring/tools/validate.py (imports qgen)
    if src != "base":
        sys.exit(f"--from: only base (its map is {layout.from_base(bundle).name})")
    check_bundle(bundle)
    b = bundle_row(bundle)
    if bundle == "base" or b["kind"] != "base":
        sys.exit(f"--from base copies into another base bundle; {bundle} is kind {b['kind']}")
    if not (PROMPTS / "fit.md").exists():
        sys.exit("no fit prompt: authoring/tools/prompts/fit.md is missing (plan 230)")
    if not b.get("rule") or not b.get("voice"):
        sys.exit(f"{bundle} needs a rule and a voice in app/data/bundles.json for the fit prompt")
    if not layout.from_base(bundle).exists():
        sys.exit(f"no subcategory map {layout.from_base(bundle).relative_to(ROOT)}")
    if bad := validate.from_base_problems(pool, [bundle], path=layout.from_base):
        sys.exit("The subcategory map is incomplete:\n" + "\n".join(f"  {e}" for e in bad))


def cmd_fit_batch(args):
    """`qgen batch --bundle <id> --from base` (plan 230). Rerunning it continues where it stopped; --dry-run: the
    next run's sources, counts and a cost estimate, no calls, nothing written."""
    bundle = args.bundle
    if args.translate or args.media_first or args.subcategories or args.ids or args.files or args.until:
        sys.exit("--from takes only --bundle (and --dry-run)")
    pool = load_json(POOL)["questions"]
    refuse(bundle, args.from_bundle, pool)
    run, resuming = mode_run("fit")
    d = WORK / run
    again = f"qgen batch --bundle {bundle} --from base"
    if resuming and load_json(d / "run.json")["bundle"] != bundle:
        sys.exit(f"{run} is unfinished and copies into {load_json(d / 'run.json')['bundle']!r}, not {bundle!r}. "
                 f"Finish it first: qgen batch --bundle {load_json(d / 'run.json')['bundle']} --from base")
    if args.dry_run:
        if resuming:
            print(f"{run} is unfinished; `{again}` resumes it.")
        else:
            print_dry_run(run, bundle, select(bundle, pool, en_translations(), args.count or FIT_SIZE))
        return []
    lock_run(d)
    if resuming:
        print(f"Resuming {run}" + (" (--count ignored)" if args.count else "") + ".", flush=True)
    else:
        sel = select(bundle, pool, en_translations(), args.count or FIT_SIZE)
        if not (sel["sources"] or sel["flipped"] or sel["rule"]):
            sys.exit(f"Nothing to judge for {bundle}: every approved base source with English text has a verdict"
                     + (f" ({len(sel['not_copyable'])} not copyable yet)" if sel["not_copyable"] else "") + ".")
        save_json(d / "run.json", {"mode": "fit", "bundle": bundle, "from": "base", "model": FIT_MODEL,
                                   **{k: sel[k] for k in ("sources", "flipped", "rule", "left")},
                                   "not_copyable": len(sel["not_copyable"]), "started": datetime.date.today().isoformat()})
        print(f"Starting {run}: {len(sel['sources'])} base sources to judge for {bundle}, {len(sel['rule'])} dropped by rule, "
              f"{len(sel['flipped'])} developer flip(s), {len(sel['not_copyable'])} not copyable yet.", flush=True)
    progress.verbose = False

    def ns(**kw):
        return argparse.Namespace(run=run, jobs=args.jobs, **kw)

    # no validate yet: the fit verdicts are written before their copies
    t0 = run_steps([("select", step_select, ns()), ("fit", step_fit, ns(model=load_json(d / "run.json")["model"])),
                    ("copy", step_copy, ns())], again, run, validate=False)
    cfg = load_json(d / "run.json")
    run_steps([
        *(revise_steps(ns, "opus", REVIEW_MODEL) if cfg["ids"] else []),
        ("audit", lambda a: cmd_audit(a) if load_json(d / "recorded.json") else [], ns(model="opus", batch=run)),
        ("export", lambda a: cmd_export(a) or [], ns()),
        ("sync", cmd_sync_run, ns()),
    ], again, run)
    cfg = load_json(d / "run.json")
    save_json(d / "run.json", {**cfg, "done": cfg.get("done") or datetime.date.today().isoformat()})
    out, s = write_fit_report(run)
    print(f"\nDone: {run}: {s['judged']} judged: {s['keep']} kept, {s['adapt']} adapted ({s['adapted_ok']} approved), "
          f"{s['drop']} dropped; {s['rule']} dropped by rule, {s['not_copyable']} not copyable yet "
          f"(took {progress.duration(time.monotonic() - t0)}).")
    print(f"  report: {out.relative_to(ROOT)}")
    files = ["authoring/data/questions.json", layout.fit(bundle).relative_to(ROOT).as_posix(), "app/data/bundles/",
             "app/data/demo/", out.relative_to(ROOT).as_posix()]
    print(f"Commit exactly this:\n  git add {' '.join(files)}\n"
          f"  git commit -m \"{run}: {s['keep'] + s['adapt'] + s['flipped']} base questions copied into {bundle}, "
          f"{s['drop'] + s['rule']} dropped ({again})\"")
    return []


def step_select(a):
    """The run's rule drops into fit.json (once)."""
    cfg = load_json(WORK / a.run / "run.json")
    seen = verdicts(cfg["bundle"])
    new = {i: {**e, "run": a.run, "copy": None} for i, e in cfg["rule"].items() if i not in seen}
    if new:
        save_verdicts(cfg["bundle"], {**seen, **new})
    progress.say(f"  select: {len(cfg['sources'])} to judge, {len(cfg['rule'])} dropped by rule")
    return []


FIT_TRIES = 3


def step_fit(a):
    """fit.md over the run's sources in chunks of FIT_CHUNK → work/<run>/fit/<first id>.json; when all are answered,
    their verdicts into fit.json."""
    d = WORK / a.run
    cfg = load_json(d / "run.json")
    bundle, ids = cfg["bundle"], cfg["sources"]
    by_id, tr = {q["id"]: q for q in load_json(POOL)["questions"]}, en_translations()
    groups = [ids[k:k + FIT_CHUNK] for k in range(0, len(ids), FIT_CHUNK)]
    todo = [g for g in groups if not (d / "fit" / f"{g[0]}.json").exists()]
    progress.resumed("fit", len(groups) - len(todo), len(todo), "calls")
    system = fit_system(bundle)

    def work(group):
        items = []
        for i in group:
            text = fit_text(by_id[i], tr)
            if text is None:
                raise RuntimeError(f"{i}: its English text is gone since select (no approved, current en translation)")
            items.append(fit_item(by_id[i], text))
        got, model = {}, None
        for _ in range(FIT_TRIES):  # the model sometimes skips items: ask again for the missing ones only
            left = [it for it in items if it["id"] not in got]
            if not left:
                break
            out, model = claude(system, fit_user(left), FIT_SCHEMA, a.model, d, with_model=True)
            got |= {x["id"]: x for x in out["items"] if x["id"] in group and x["id"] not in got
                    and not (x["verdict"] == "adapt" and not (x["issue"] or "").strip())}
        bad = [i for i in group if i not in got]
        if bad:
            raise RuntimeError(f"fit: no usable verdict for {', '.join(bad)}")
        save_json(d / "fit" / f"{group[0]}.json", {"model": model, "items": [got[i] for i in group]})

    errors = parallel(work, todo, a.jobs, "fit", "calls")
    if errors:
        return errors
    seen = verdicts(bundle)
    for g in groups:
        f = load_json(d / "fit" / f"{g[0]}.json")
        for x in f["items"]:
            if x["id"] not in seen:
                drop = x["verdict"] == "drop"
                seen[x["id"]] = {"verdict": x["verdict"], "reason": (x["reason"] if x["reason"] in REASONS else "other") if drop else None,
                                 "note": x["note"], **({"issue": x["issue"].strip()} if x["verdict"] == "adapt" else {}),
                                 "run": a.run, "by": "fit", "model": f["model"], "copy": None}
    save_verdicts(bundle, seen)
    n = Counter(seen[i]["verdict"] for i in ids)
    progress.say(f"  fit: {n['keep']} keep, {n['adapt']} adapt, {n['drop']} drop of {len(ids)}")
    return []


def fit_review(decision, feedback, problems, e, run, src):
    """A copy's review from its fit verdict (D-33): llm with the fit call's model, or human for a developer flip;
    names the fit run and the source's review."""
    rv = src.get("review") or {}
    human = e["by"] == "developer"
    return {"decision": decision, "feedback": feedback, "problems": problems,
            "reviewed_on": datetime.date.today().isoformat(), "reviewer": "human" if human else "llm",
            **({} if human else {"model": e.get("model") or FIT_MODEL}), "fit": e.get("run") or run,
            "source_review": {k: rv[k] for k in ("reviewer", "model", "reviewed_on") if rv.get(k)} | {"id": src["id"]}}


def step_copy(a):
    """A copy per keep/adapt verdict of the run and per developer flip (copies.copy_question): keep → approved (a
    near-duplicate within the bundle → needs_work), adapt → needs_work with the fit issue for the revise steps.
    run.json "ids": the adapted copies."""
    d = WORK / a.run
    cfg = load_json(d / "run.json")
    bundle = cfg["bundle"]
    m, tr = subcategory_map(bundle), en_translations()
    with atomic.locked(POOL):
        data = load_json(POOL)
        pool = data["questions"]
        seen = verdicts(bundle)
        by_id = {q["id"]: q for q in pool}
        have = {q["copied_from"]: q["id"] for q in pool if q.get("bundle") == bundle and q.get("copied_from")}
        own = [q for q in pool if q.get("bundle") == bundle and q["status"] != "rejected"]
        made = Counter()
        for i in [*cfg["sources"], *cfg["flipped"]]:
            e = seen[i]
            if e["verdict"] not in ("keep", "adapt") or i in have:
                continue
            src = by_id[i]
            try:
                new = copies.copy_question(i, bundle, m[src["subcategory"]]["to"], pool, a.run, en_translations=tr)
            except copies.NotCopyable as x:
                return [RuntimeError(f"copy: {x}")]
            if e["verdict"] == "adapt":
                status, review = "needs_work", fit_review("needs_work", f"{ADAPT}: {e['issue']}", [], e, a.run, src)
            elif dup := duplicates(new, own, "en"):
                status, review = "needs_work", fit_review("needs_work", f"Duplicate within {bundle}: {dup}", ["overlap"], e, a.run, src)
            else:
                status, review = "approved", fit_review("approved", None, [], e, a.run, src)
            new.update(status=status, review=review)
            pool.append(new)
            own.append(new)
            have[i] = new["id"]
            made[e["verdict"] if status == "approved" or e["verdict"] == "adapt" else "duplicate"] += 1
        save_json(POOL, data)  # the pool first: a rerun finds its copies by copied_from
    for i in [*cfg["sources"], *cfg["flipped"]]:
        if i in have and seen[i]["verdict"] in ("keep", "adapt"):
            seen[i]["copy"] = have[i]
    save_verdicts(bundle, seen)
    ids = [have[i] for i in cfg["sources"] if i in have and seen[i]["verdict"] == "adapt"]
    save_json(d / "run.json", {**cfg, "ids": ids})
    progress.say(f"  copy: {made['keep']} kept (approved), {made['adapt']} to adapt, {made['duplicate']} near-duplicate(s) to needs_work")
    return []


def run_stats(run):
    cfg = load_json(WORK / run / "run.json")
    seen = verdicts(cfg["bundle"])
    by_id = {q["id"]: q for q in load_json(POOL)["questions"]}
    n = Counter(seen[i]["verdict"] for i in cfg["sources"] if i in seen)
    adapted = [by_id[c] for c in cfg.get("ids") or [] if c in by_id]
    return {"judged": len(cfg["sources"]), "keep": n["keep"], "adapt": n["adapt"], "drop": n["drop"],
            "rule": len(cfg["rule"]), "flipped": len(cfg["flipped"]), "not_copyable": cfg["not_copyable"], "left": cfg["left"],
            "adapted_ok": sum(q["status"] == "approved" for q in adapted), "cfg": cfg, "seen": seen, "by_id": by_id}


def write_fit_report(run):
    """authoring/reports/<run>.md: counts, per base category and subcategory, drop reasons, needs work, cost (plan 230)."""
    s = run_stats(run)
    cfg, seen, by_id, bundle = s["cfg"], s["seen"], s["by_id"], s["cfg"]["bundle"]
    mine = [*cfg["sources"], *cfg["rule"]]
    copies_ = [by_id[e["copy"]] for i in [*cfg["sources"], *cfg["flipped"]] if (e := seen.get(i)) and e.get("copy") in by_id]
    c = costs(WORK / run) + costs(WORK / run / "audit")
    lines = [f"# {run}", "",
             f"Made by `qgen batch --bundle {bundle} --from base` on {datetime.date.today().isoformat()} (plan 230): approved "
             f"`base` questions judged for `{bundle}` (`prompts/fit.md`); kept and adapted ones copied. Verdicts: "
             f"`{layout.fit(bundle).relative_to(ROOT).as_posix()}`. Generated file: don't edit by hand.", "",
             f"- Judged by the fit pass: {s['judged']}: kept {s['keep']}, adapted {s['adapt']}, dropped {s['drop']}",
             f"- Dropped by rule (no call): {s['rule']}", f"- Developer flips copied: {s['flipped']}",
             f"- Not copyable yet (no approved, current English text): {s['not_copyable']}",
             f"- Left for later runs: {s['left']}",
             f"- Copies: {len(copies_)}, {sum(q['status'] == 'approved' for q in copies_)} approved, "
             f"{sum(q['status'] == 'needs_work' for q in copies_)} needs work; adapted {s['adapt']}, {s['adapted_ok']} approved after revision",
             f"- Claude calls: {len(c)}, about ${sum(c):.2f} at list price", "",
             "## Drop reasons", ""]
    reasons = Counter((seen[i]["reason"], seen[i]["by"]) for i in mine if seen.get(i, {}).get("verdict") == "drop")
    lines += [f"- {r} ({by}): {k}" for (r, by), k in sorted(reasons.items(), key=lambda kv: -kv[1])] or ["None."]
    lines += ["", "## Per base category and subcategory", "",
              "| Category | Subcategory | Judged | Keep | Adapt | Drop | By rule |", "|---|---|---|---|---|---|---|"]
    rows = {}
    for i in mine:
        e, sub = seen.get(i), by_id[i]["subcategory"]
        r = rows.setdefault(sub, Counter())
        if e:
            r["rule" if e["by"] in ("map", "rule") else e["verdict"]] += 1
            r["judged"] += e["by"] == "fit"
    order = {s_: k for k, s_ in enumerate(categories.subcategories("base"))}
    for sub in sorted(rows, key=lambda x: order.get(x, len(order))):
        r = rows[sub]
        lines.append(f"| {categories.category_name('base', sub, 'en')} | {categories.display('base', sub, 'en')} | {r['judged']} "
                     f"| {r['keep']} | {r['adapt']} | {r['drop']} | {r['rule']} |")
    lines += ["", *audit_section(run), *qc_section(run), "## Needs work", ""]
    lines += [f"- **{q['id']}** (from {q['copied_from']}) {q['question']} → {q['answer']}: {q['review']['feedback']} ({REVIEW_URL}/{q['id']})"
              for q in copies_ if q["status"] == "needs_work"] or ["None."]
    return write_report(run, lines), s


def print_dry_run(run, bundle, sel):
    """--dry-run: what `run` would do, and what it would cost from finished fit and rework runs."""
    n = len(sel["sources"])
    pool = {q["id"]: q for q in load_json(POOL)["questions"]}
    print(f"{run} would judge {n} base sources for {bundle} ({math.ceil(n / FIT_CHUNK)} fit calls), drop "
          f"{len(sel['rule'])} by rule, copy {len(sel['flipped'])} developer flip(s); {len(sel['not_copyable'])} not "
          f"copyable yet, {sel['left']} left for later runs.")
    by_sub = Counter(pool[i]["subcategory"] for i in sel["sources"])
    print("Sources by base subcategory:")
    for sub, k in sorted(by_sub.items(), key=lambda kv: natural_key(kv[0])):
        print(f"  {sub}: {k}")
    done = [load_json(p) | {"dir": p.parent} for p in WORK.glob("*/run.json") if (load_json(p) or {}).get("done")]
    fits = [c for c in done if c.get("mode") == "fit" and c.get("sources")]
    if fits:
        per = sum(sum(costs(c["dir"])) + sum(costs(c["dir"] / "audit")) for c in fits) / sum(len(c["sources"]) for c in fits)
        print(f"Estimate: about ${per * n:.2f} at list price (${per:.3f} per judged source over {len(fits)} finished fit run(s), "
              "revise and audit included).")
        return
    reworks = [c for c in done if c.get("mode") == "rework" and c.get("ids")]
    per_q = sum(sum(costs(c["dir"])) for c in reworks) / sum(len(c["ids"]) for c in reworks) if reworks else None
    print("Estimate: no finished fit run to price the fit calls from yet"
          + (f"; each adapted copy then costs about ${per_q:.2f} (finished rework runs)." if per_q is not None else "."))


# the other command groups, after everything here is defined (they import each other)
from audit import audit_section, cmd_audit, mode_run  # authoring/tools/audit.py
from report import qc_section  # authoring/tools/report.py
from review_steps import REVIEW_MODEL  # authoring/tools/review_steps.py
from rework import revise_steps  # authoring/tools/rework.py
