"""`qgen report`: progress, saturation, calibration, QC, simulate, cost, review time, played. Never ships (D-35)."""
import concurrent.futures, datetime, json, os, re, sys, time
from collections import Counter

import layout  # paths (D-35)
from layout import REPO as ROOT, SOURCE_POOL as POOL, WORK
import concepts  # authoring/tools/concepts.py: concept lists and question axes (D-37)
import categories  # authoring/tools/categories.py: every bundle's categories (D-19, D-43)
import engine  # authoring/tools/engine.py: the TS engine under Node (D-60), e.g. the supply check (GF-5)
import save_file  # authoring/tools/save_file.py: the game's save, read-only (D-59)
import targets  # authoring/tools/targets.py: pool targets (D-53)
import translations  # authoring/tools/translations.py: translated questions (D-81)
import played  # authoring/tools/played.py: opt-in telemetry → state/played/ (plan 109)

from qgen import PROBLEMS, REVIEW_URL, RUBRIC, as_locale, collect, costs, drafts, load_age_groups, load_bundles, load_json, natural_key, overlap_candidates, run_dir, work_runs  # authoring/tools/qgen.py


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
    if targets.kind_of(bundle) in {"base", "theme"}:
        report_supply(pool, locale, bundle)


def report_supply(pool, locale, bundle="base"):
    """English drafting for base or a theme (plan 70, decision 236): per question locale its deficit, yield, untranslated
    sources and the drafts it asks for, per level; the draft gap = the largest."""
    supply = targets.source_supply(pool, bundle)
    fmt = lambda d: ", ".join(f"{l}: {n}" for l, n in sorted(d.items()) if n) or "none"
    print(f"en drafting for {bundle} (decision 236; per level; drafts = deficit / yield − untranslated, en 1:1):")
    for l, x in supply.items():
        if locale in (l, "es"):
            gap = {lvl: targets.locale_gap(x, lvl) for lvl in x["deficit"]}
            print(f"  {l}: yield {x['yield']:.2f}; deficit {fmt(x['deficit'])}; untranslated {fmt(x['untranslated'])}; "
                  f"drafts {fmt(gap)}")
    print(f"  draft gap (largest over {', '.join(supply)}): {fmt(targets.draft_gaps(pool, bundle, supply) or {})}")


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
SIM_MULTI = {"rr-coop", "rr-competitive", "timed"}  # sessions; = sim/simulate.ts MULTI


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
          "standard jokers once each at a random level (rr-coop: the team's set; rr-competitive: per player); "
          "multiplayer modes as the engine's sessions (a game = a session; timed: every question claimed by a random player still in)")
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
    """Rows per non-base bundle (decision 110; base is the projection): a region × es, en; a theme × en (its drafting,
    deficit = the draft gap, decision 236) and es, es-ES, de (its translations). $ per approved of its --bundle and
    --translate --bundle runs, deficit to its target, projection; no own run yet → base's rate."""
    rows = []
    for b in load_bundles():
        theme = b.get("kind") == "theme"
        if b.get("kind") != "region" and not theme:
            continue
        gap = sum((targets.draft_gaps(pool, b["id"]) or {}).values()) if theme else None
        for l in (translations.LOCALES if theme else ["es", "en"]):
            drafting = l == "en" if theme else l == "es"
            own = [r for r in runs if r["bundle"] == b["id"] and r["merged"]
                   and (r["kind"] == "batch" and (not theme or r["locale"] == l) if drafting else r["locale"] == l)]
            n = sum(r["approved"] or 0 for r in own)
            rate = sum(r["cost"] for r in own) / n if n else None
            fallback = (rates["draft"].get("en", rates["draft"].get("es")) if theme else rates["draft"].get("es")) \
                if drafting else rates["translation"].get(l)
            use = rate if rate is not None else fallback
            deficit = gap if theme and drafting else sum((targets.deficits(pool, b["id"], l) or {}).values())
            rows.append({"bundle": b["id"], "kind": b["kind"], "locale": l, "runs": [r["run"] for r in own], "approved": n,
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
    print("per regional and theme bundle (its --bundle and --translate --bundle runs; deficit to its target, decision 110; "
          "a theme's en row: drafts = its draft gap; projection as above, * = base's rate, no own run yet):")
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
    players = {}
    for k, v in stats["games"].get("players", {}).items():
        day, m, n = k.split("|")
        if keep(day, None, m):
            players.setdefault(m, Counter())[int(n)] += v
    if players:
        print("  games by players: " + ", ".join(f"{m} {dict(sorted(c.items()))}" for m, c in sorted(players.items())))
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


# the other command groups, after everything here is defined (they import each other)
from audit import audits, is_major, llm_decisions, run_questions  # authoring/tools/audit.py
from translate import text_locale  # authoring/tools/translate.py
from validate import validate_pool  # authoring/tools/validate.py
