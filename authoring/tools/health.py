"""Batch health (plan 15, D-55): metrics per `qgen batch` run from work/<run>/ and the pool.
Shared by `qgen batch-report`, `qgen report --batches` and plan 12's exit check. No LLM."""
import datetime, json, re
from collections import Counter

import layout  # noqa: F401  (paths; also makes app/server importable, D-35)
from layout import REPORTS, SOURCE_POOL as POOL, WORK
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


PCT = {"drop rate", "needs_work rate", "overlap rate", "merged/slots 11–15", "media share",
       *(f"needs_work: {p}" for p in qgen.PROBLEMS), *(f"top {a}" for a in concepts.AXES)}


def fmt(key, v):
    if v is None: return "n/a"
    if isinstance(v, bool): return "yes" if v else "no"
    if key in PCT: return f"{100 * v:.1f} %"
    if key.startswith("$") or key == "cost $": return f"${v:.2f}"
    if isinstance(v, float): return f"{v:.2f}"
    return str(v)


def table(runs, pool=None):
    """Markdown table: one row per metric, one column per run."""
    pool = pool if pool is not None else load(POOL)["questions"]
    cols = [batch_health(r, pool) for r in runs]
    lines = ["| metric | " + " | ".join(runs) + " |", "|---|" + "---:|" * len(runs)]
    for key in cols[0]:
        lines.append(f"| {key} | "
                     + " | ".join(fmt(key, c[key]) for c in cols) + " |")
    return lines


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
            "Batch health (plan 15): this batch and the two before it; thresholds come with plan 15's thresholds task. "
            "Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.", "",
            *table(runs, pool), "", deficit_line(pool=pool), ""]


def write_batches_md(pool=None):
    """authoring/reports/batches.md: every batch from batch-4 side by side."""
    runs = batch_runs()
    lines = ["# Batches", "",
             "Batch health of every `qgen batch` run from batch-4 on (plan 15), regenerated by `qgen batch-report`. "
             "Generated file: don't edit by hand. Needs-work counts are `record`'s decisions, before rework and "
             "the gamemaster's review.", "", *table(runs, pool), "", deficit_line(pool=pool), ""]
    out = REPORTS / "batches.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
