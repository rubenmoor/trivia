"""Batch health (plan 15, D-55): metrics per `qgen batch` run from work/<run>/ and the pool.
Shared by `qgen batch-report`, `qgen report --batches` and plan 12's exit check. No LLM."""
import datetime, json, re
from collections import Counter

from layout import HEALTH_ACKS, REPORTS, SOURCE_POOL as POOL, WORK
import concepts  # authoring/tools/concepts.py
import targets  # authoring/tools/targets.py
import qgen  # authoring/tools/qgen.py: work files, calibration, problems

HIGH = range(11, 16)  # the levels plan 13 aims at


def load(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def batch_runs():
    """work/batch-N (N ≥ 4) that got as far as merge, oldest first."""
    runs = [p.name for p in WORK.glob("batch-*") if re.fullmatch(r"batch-\d+", p.name)
            and int(p.name[6:]) >= 4 and (p / "dropped.json").exists()]
    return sorted(runs, key=lambda r: int(r[6:]))


def recorded(run, qs):
    """{id: (problems, guessed)} of the questions `record` left needs_work. Sources, best first:
    work/<run>/recorded.json; the batch report's needs-work list (feedback, guessed); the oldest
    llm review in the pool (batch-4)."""
    rec = load(WORK / run / "recorded.json")
    if rec is not None:
        return {i: (r["problems"] or ["other"], False) for i, r in rec.items() if r["decision"] == "needs_work"}
    md = REPORTS / f"{run}.md"
    if md.exists():
        out = {}
        for m in re.finditer(r"^- \*\*(q-\d+)\*\* .*? → [^:\n]*: (.*)$", md.read_text(encoding="utf-8"), re.M):
            out[m.group(1)] = (qgen.guess_problems(m.group(2)), True)
        return out
    out = {}
    for q in qs:
        r, first = q.get("review"), None
        while r:
            first = r if r.get("reviewer") == "llm" else first
            r = r.get("previous")
        if first and first["decision"] == "needs_work":
            out[q["id"]] = (first.get("problems") or qgen.guess_problems(first.get("feedback")),
                            not first.get("problems"))
    return out


def drop_kind(reason):
    if reason.startswith("overlap"): return ["overlap"]
    if reason.startswith("duplicate"): return ["duplicate"]
    if reason.startswith("fact-check"): return ["fact-check wrong"]
    if reason.startswith("hard fail"):
        return [f"hard fail {k}" for k, v in re.findall(r"(\w+) (\d|-)", reason[10:]) if v != "-" and int(v) < 4]
    return ["other"]


def overlaps_by_subcategory(run, pool=None):
    """{subcategory: [overlaps, drafts]} of one run: merge's overlap/duplicate drops plus `record`'s
    needs_work for overlap (plan 14's saturation check)."""
    pool = pool if pool is not None else load(POOL)["questions"]
    sub_of = {q["tmp_id"]: q["subcategory"] for _, qq in qgen.drafts(WORK / run) for q in qq}
    out = {}
    for s in sub_of.values():
        out.setdefault(s, [0, 0])[1] += 1
    for x in load(WORK / run / "dropped.json", []):
        if {"overlap", "duplicate"} & set(drop_kind(x["reason"])) and x["tmp_id"] in sub_of:
            out[sub_of[x["tmp_id"]]][0] += 1
    qs = {q["id"]: q for q in pool if q.get("batch") == run}
    for i, (ps, _) in recorded(run, qs.values()).items():
        if "overlap" in ps and i in qs and qs[i].get("subcategory") in out:
            out[qs[i]["subcategory"]][0] += 1
    return out


def rate(n, of):
    return n / of if of else None


def batch_health(run, pool=None):
    """{metric: value} for one run; None = n/a. Keys and order: ROWS."""
    d = WORK / run
    pool = pool if pool is not None else load(POOL)["questions"]
    cfg = load(d / "run.json", {}) or {}
    qs = [q for q in pool if q.get("batch") == run]
    drafted = {q["tmp_id"]: q for _, qq in qgen.drafts(d) for q in qq}
    skipped = sum(len(load(f)["skipped"]) for f in (d / "drafts").glob("*.json"))
    dropped = load(d / "dropped.json", [])
    ratings, _ = qgen.collect(d)
    work = recorded(run, qs)
    approved = [q for q in qs if q["id"] not in work]
    n, m = len(drafted), len(qs)
    h = {"drafts": n, "skipped slots": skipped, "dropped": len(dropped), "drop rate": rate(len(dropped), n)}
    kinds = Counter(k for x in dropped for k in drop_kind(x["reason"]))
    for k in [*(f"hard fail {c}" for c in qgen.HARD_CRITERIA if c != "no_overlap"), "overlap", "duplicate", "fact-check wrong"]:
        h[f"dropped: {k}"] = kinds[k]
    h |= {"merged": m, "approved": len(approved), "needs_work": len(work), "needs_work rate": rate(len(work), m)}
    by_problem = Counter(p for ps, _ in work.values() for p in ps)
    guessed = any(g for _, g in work.values())
    for p in qgen.PROBLEMS:
        h[f"needs_work: {p}"] = rate(by_problem[p], m)
    h["problems guessed"] = guessed if work else None
    h["overlap rate"] = rate(kinds["overlap"] + kinds["duplicate"] + by_problem["overlap"], n)
    if (d / "slots.json").exists():
        cal = {lvl: r for lvl, r in qgen.calibration(run, pool).items() if lvl in HIGH}
        slots = sum(r["slots"] for r in cal.values())
        h["merged/slots 11–15"] = rate(sum(r["merged"] for r in cal.values()), slots)
        off = [abs(r["final"] - lvl) for lvl, r in cal.items() if r["final"] is not None]
        h["max final−target gap 11–15"] = max(off) if off else None
    else:
        h["merged/slots 11–15"] = h["max final−target gap 11–15"] = None
    h["approved 11–15"] = sum(q["difficulty"] in HIGH for q in approved)
    with_axes = [q for q in qs if q.get("axes")]
    for a in concepts.AXES:
        c = Counter(q["axes"].get(a) for q in with_axes)
        h[f"top {a}"] = rate(c.most_common(1)[0][1], len(with_axes)) if c else None
        h[f"values {a}"] = len(c) if c else None
    h["media share"] = rate(sum(q["axes"].get("stimulus") != "none" for q in with_axes), len(with_axes))
    fun = [r["fun"] for r in ratings.values() if "fun" in r]
    h["mean fun"] = sum(fun) / len(fun) if fun else None
    costs = [line.split("\t")[1] for line in (d / "costs.log").read_text().splitlines()
             if line.count("\t") == 1] if (d / "costs.log").exists() else []
    dollars = sum(float(c) for c in costs if c not in ("None", ""))
    h |= {"cost $": dollars, "$ per approved": rate(dollars, len(approved)),
          "calls": len(costs), "calls per approved": rate(len(costs), len(approved))}
    secs = cfg.get("seconds")
    h["wall time h"] = sum(secs.values()) / 3600 if secs else None
    day = datetime.date.fromisoformat
    h["days"] = (day(cfg["done"]) - day(cfg["started"])).days + 1 if cfg.get("started") and cfg.get("done") else None
    return h


EACH_PROBLEM = "needs_work: each problem"
THRESHOLDABLE = {"drop rate", "needs_work rate", "overlap rate", "merged/slots 11–15", "max final−target gap 11–15",
                 "media share", "mean fun", "$ per approved", EACH_PROBLEM,
                 *(f"needs_work: {p}" for p in qgen.PROBLEMS), *(f"top {a}" for a in concepts.AXES)}


def thresholds():
    """{metric: {"min"/"max": x}} from targets.json, «each problem» spread out; None before they're stored."""
    t = targets.load_batch_health()
    if t is None: return None
    each = t.get(EACH_PROBLEM)
    spread = {f"needs_work: {p}": each for p in qgen.PROBLEMS} if each else {}
    return spread | {k: v for k, v in t.items() if k != EACH_PROBLEM}


def passes(value, bounds):
    """True/False; None when the metric is n/a (not a fail)."""
    if value is None: return None
    return bounds.get("min", value) <= value <= bounds.get("max", value)


def failures(run, pool=None, h=None):
    """Names of the thresholds the run fails ([] = pass), None while targets.json has no thresholds.
    An ack doesn't change this (plan 12's exit check)."""
    t = thresholds()
    if t is None: return None
    h = h or batch_health(run, pool)
    return [k for k, b in t.items() if passes(h.get(k), b) is False]


def acks():
    return load(HEALTH_ACKS, {})


def last_done_run():
    """The newest batch run that `qgen batch` finished (any bundle), or None."""
    done = [r for r in batch_runs() if (load(WORK / r / "run.json", {}) or {}).get("done")]
    return done[-1] if done else None


def stop_reason():
    """Why the next `qgen batch` must stop (D-55), or None: the last done batch fails a threshold
    and the gamemaster hasn't acked it."""
    run = last_done_run()
    if run is None or run in acks(): return None
    bad = failures(run)
    if not bad: return None
    return (f"{run} fails the batch health thresholds: {', '.join(bad)}.\n"
            f"See `qgen report --batches` or authoring/reports/batches.md. The gamemaster looks at it and "
            f"clears the stop with: qgen health ack {run} \"<note>\"")


PCT = {"drop rate", "needs_work rate", "overlap rate", "rejected rate", "audit/review agreement", "merged/slots 11–15", "media share",
       *(f"needs_work: {p}" for p in qgen.PROBLEMS), *(f"top {a}" for a in concepts.AXES)}


def fmt(key, v):
    if v is None: return "n/a"
    if isinstance(v, bool): return "yes" if v else "no"
    if key in PCT: return f"{100 * v:.1f} %"
    if key.startswith("$") or key == "cost $": return f"${v:.2f}"
    if isinstance(v, float): return f"{v:.2f}"
    return str(v)


def bound_text(key, b):
    if b is None: return ""
    if "min" in b and "max" in b: return f"{fmt(key, b['min'])}–{fmt(key, b['max'])}"
    return f"≥ {fmt(key, b['min'])}" if "min" in b else f"≤ {fmt(key, b['max'])}"


def table(runs, pool=None):
    """Markdown table: one row per metric, one column per run; ✓/✗ against the thresholds."""
    if not runs: return ["No batch yet."]
    pool = pool if pool is not None else load(POOL)["questions"]
    cols = [batch_health(r, pool) for r in runs]
    t, acked = thresholds() or {}, acks()
    mark = {True: " ✓", False: " ✗", None: ""}
    lines = ["| metric | threshold | " + " | ".join(runs) + " |", "|---|---|" + "---:|" * len(runs)]
    for key in cols[0]:
        b = t.get(key)
        lines.append(f"| {key} | {bound_text(key, b)} | "
                     + " | ".join(fmt(key, c[key]) + (mark[passes(c[key], b)] if b else "") for c in cols) + " |")
    if t:
        verdict = lambda r, c: ("✓ pass" if not failures(r, h=c) else "✗ fail, acked" if r in acked else "✗ fail")
        lines.append("| **health** | | " + " | ".join(verdict(r, c) for r, c in zip(runs, cols)) + " |")
    return lines


def ack_lines():
    a = acks()
    return [f"- {r} ({x['date']}): {x['note']}" for r, x in sorted(a.items(), key=lambda kv: qgen.natural_key(kv[0]))] or ["None."]


# --- translation runs (plan 66): `qgen batch --translate <locale>` ---------------
# Thresholds that apply to a tr-* run (no drafts, slots, axes or media search): «needs_work rate» and
# «needs_work: <problem>» as for batches; «rejected rate» (confirmed not travelling / sources) under
# «drop rate»'s bound; audit/review agreement ≥ quality.min_agreement once ≥ spot_check_size are audited
# (D-56/D-79). «$ per approved» is shown, not a threshold: the batch bound is for drafting.

def translation_runs(locale=None):
    """work/tr-<locale>-N that got as far as merge, oldest first."""
    pat = rf"tr-{re.escape(locale) if locale else '[A-Za-z-]+'}-\d+"
    return sorted((p.name for p in WORK.glob("tr-*") if re.fullmatch(pat, p.name) and (p / "merged.json").exists()),
                  key=qgen.natural_key)


def translation_health(run):
    """{metric: value} of one translation run; None = n/a."""
    d = WORK / run
    cfg = load(d / "run.json", {}) or {}
    rec = load(d / "recorded.json", {}) or {}
    away = load(d / "not-travelling.json", []) or []
    n_src, m = len(cfg.get("ids", [])), len(rec)
    work = {i: r for i, r in rec.items() if r["decision"] == "needs_work"}
    confirmed = sum(x.get("decision") == "approved" for x in away)
    h = {"sources": n_src, "stale re-translated": len(cfg.get("stale", [])), "translated": m,
         "not travelling": len(away), "not travelling confirmed": confirmed, "rejected rate": rate(confirmed, n_src),
         "approved": m - len(work), "needs_work": len(work), "needs_work rate": rate(len(work), m)}
    by_problem = Counter(p for r in work.values() for p in r["problems"] or ["other"])
    for p in qgen.PROBLEMS:
        h[f"needs_work: {p}"] = rate(by_problem[p], m)
    found, dec = qgen.audits(run), qgen.llm_decisions(run) if rec else {}
    both = [i for i in found if i in dec]
    h["audited"] = len(found)
    h["audit/review agreement"] = rate(sum((dec[i] == "approved") == (not qgen.is_major(found[i])) for i in both), len(both))
    dollars = sum(qgen.costs(d / "costs.log"))
    h |= {"cost $": dollars, "$ per approved": rate(dollars, m - len(work))}
    return h


def translation_thresholds():
    """{metric: bounds} that apply to a translation run; {} before targets.json has thresholds."""
    t = thresholds()
    if t is None: return {}
    out = {k: v for k, v in t.items() if k == "needs_work rate" or k.startswith("needs_work: ")}
    if "drop rate" in t:
        out["rejected rate"] = t["drop rate"]
    q = targets.load_quality()
    if q:
        out["audit/review agreement"] = {"min": q["min_agreement"]}
    return out


def translation_failures(run, h=None):
    h = h or translation_health(run)
    q = targets.load_quality() or {}
    return [k for k, b in translation_thresholds().items() if passes(h.get(k), b) is False
            and (k != "audit/review agreement" or h["audited"] >= q.get("spot_check_size", 0))]


def translate_stop_reason(locale):
    """Why the next `qgen batch --translate <locale>` must stop, or None: the pilot tr-<locale>-1 until the
    gamemaster's go (plan 66, QT-5), or the last done run fails a threshold, both until `qgen health ack`."""
    done = [r for r in translation_runs(locale) if (load(WORK / r / "run.json", {}) or {}).get("done")]
    if not done or done[-1] in acks(): return None
    run = done[-1]
    if run == f"tr-{locale}-1":
        return (f"{run} was the pilot of {locale} (QT-5). The gamemaster decides on it (report: "
                f"authoring/reports/{run}.md) and gives the go with: qgen health ack {run} \"<note>\"")
    bad = translation_failures(run)
    if not bad: return None
    return (f"{run} fails the health thresholds: {', '.join(bad)} (authoring/reports/{run}.md). The gamemaster looks "
            f"at it and clears the stop with: qgen health ack {run} \"<note>\"")


def translation_health_section(run):
    """«## Health» of a translation run's report: this run and the two of its locale before it."""
    locale = run[3:].rsplit("-", 1)[0]
    runs = [r for r in translation_runs(locale) if qgen.natural_key(r) < qgen.natural_key(run)][-2:] + [run]
    cols, t = [translation_health(r) for r in runs], translation_thresholds()
    mark = {True: " ✓", False: " ✗", None: ""}
    lines = ["| metric | threshold | " + " | ".join(runs) + " |", "|---|---|" + "---:|" * len(runs)]
    for key in cols[0]:
        b = t.get(key)
        lines.append(f"| {key} | {bound_text(key, b)} | "
                     + " | ".join(fmt(key, c[key]) + (mark[passes(c[key], b)] if b else "") for c in cols) + " |")
    if t:
        lines.append("| **health** | | " + " | ".join("✓ pass" if not translation_failures(r, c) else "✗ fail"
                                                    for r, c in zip(runs, cols)) + " |")
    return ["## Health", "",
            "Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the "
            "thresholds that apply to translations (`health.py`); audit/review agreement only counts from "
            "the spot-check size on. The pilot (`-1`) and a ✗ stop the next `qgen batch --translate` until "
            "`qgen health ack` (D-55).", "", *lines, ""]


def deficit_line(bundle="base", pool=None):
    pool = pool if pool is not None else load(POOL)["questions"]
    d = targets.deficits(pool, bundle)
    if not d: return "Deficit to the targets: none."
    return f"Deficit to the targets ({bundle}, approved now): " + ", ".join(f"{l}: {n}" for l, n in sorted(d.items()))


def health_section(run, pool=None):
    """Lines of «## Health» for authoring/reports/<run>.md: this run and the two before it."""
    num = lambda r: int(r[6:]) if re.fullmatch(r"batch-\d+", r) else 0
    runs = [r for r in batch_runs() if num(r) < num(run)][-2:] + [run]
    return ["## Health", "",
            "Batch health (plan 15): this batch and the two before it, ✓/✗ against the thresholds in "
            "`authoring/data/targets.json`; a ✗ stops the next `qgen batch` until `qgen health ack` (D-55). "
            "Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.", "",
            *table(runs, pool), "", deficit_line(pool=pool), ""]


def write_batches_md(pool=None):
    """authoring/reports/batches.md: every batch from batch-4 side by side."""
    runs = batch_runs()
    lines = ["# Batches", "",
             "Batch health of every `qgen batch` run from batch-4 on (plan 15), regenerated by `qgen batch-report`. "
             "Generated file: don't edit by hand. Needs-work counts are `record`'s decisions, before rework and "
             "the gamemaster's review. ✓/✗ against the thresholds in `authoring/data/targets.json` (D-55).", "",
             *table(runs, pool), "", deficit_line(pool=pool), "", "## Acknowledgements", "",
             "Failing batches the gamemaster has looked at (`qgen health ack`): the stop is cleared, the batch still fails.", "",
             *ack_lines(), ""]
    qc = qgen.qc_trend(pool)
    if qc:
        lines += ["## Quality control", "",
                  "Spot check and audit per batch (plan 16, `qgen report --qc`): human agreement with the LLM review "
                  "against `quality` in `authoring/data/targets.json` (pm decision 2); the same numbers are the release bar (D-79).", "", *qc, ""]
    out = REPORTS / "batches.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
