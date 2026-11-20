"""The fit view (plan 230): GET /api/fit?bundle=<id> and the flip, POST /api/fit/<bundle>/<id>.
Reads fit.json (authoring/tools/fit.py) and the pool; a flip writes fit.json with `by: developer`."""
import random

import layout  # authoring/tools/layout.py
import atomic  # authoring/tools/atomic.py
import categories  # authoring/tools/categories.py
import qgen  # noqa: F401  (authoring/tools/qgen.py: loads the command modules, import it first)
import fit  # authoring/tools/fit.py
import reviews  # authoring/tools/reviews.py

DROP_SAMPLE = 30  # drops per run shown as the "did the pass drop too much" sample


def check_bundle(bundle):
    if not layout.fit(bundle).exists():
        raise ValueError(f"no fit verdicts for {bundle!r}: `qgen batch --bundle {bundle} --from base` writes them")


def build(query):
    """{bundle, rows, runs, drop_sample}: a row per judged `base` source with its verdict, the source's text, and for
    keep/adapt the copy's; `drop_sample`: {run: ids}, a seeded sample of the run's fit drops."""
    bundle = query.get("bundle") or "chinese-base"
    check_bundle(bundle)
    pool = {q["id"]: q for q in reviews.load_pool()["questions"]}
    rows, runs = [], {}
    seen = fit.verdicts(bundle)
    for i, e in seen.items():
        src, cp = pool.get(i), pool.get(e.get("copy") or "")
        if src is None:
            continue
        rows.append({"id": i, **{k: e.get(k) for k in ("verdict", "reason", "note", "issue", "run", "by")},
                     "category": categories.category_name("base", src["subcategory"], "en"),
                     "subcategory": categories.display("base", src["subcategory"], "en"),
                     "source": text_of(src), "copy": cp and {**text_of(cp), "id": cp["id"], "status": cp["status"]}})
        runs.setdefault(e["run"], []).append(i)
    rows.sort(key=lambda r: (r["category"], r["subcategory"], qgen.natural_key(r["id"])))
    sample = {run: sorted(random.Random(run).sample(ds, min(DROP_SAMPLE, len(ds))), key=qgen.natural_key)
              for run, ids in runs.items()
              if (ds := [i for i in ids if seen[i]["verdict"] == "drop" and seen[i]["by"] == "fit"])}
    return {"bundle": bundle, "rows": rows, "runs": sorted(runs, key=qgen.natural_key), "drop_sample": sample}


def text_of(q):
    return {"question": q["question"], "answer": q["answer"], "wrong_answers": q["wrong_answers"], "hints": q["hints"],
            "fun_fact": q.get("fun_fact"), "difficulty": q["difficulty"]}


def flip(bundle, source_id, verdict, reason=None):
    """The developer's flip of one source's verdict. drop → keep: the next run copies it (no fit call). keep → drop:
    its copy is rejected now (ids stay, export leaves it out). adapt (either way) goes through the copy's own review;
    a drop by rule or by the map can't be flipped; a rejected copy isn't brought back."""
    check_bundle(bundle)
    if verdict not in ("keep", "drop"):
        raise ValueError("flip to keep or drop")
    with atomic.locked(reviews.POOL):
        seen = fit.verdicts(bundle)
        e = seen.get(source_id)
        if e is None:
            raise ValueError(f"{source_id} has no verdict for {bundle}")
        if e["verdict"] == verdict:
            return e
        if e["verdict"] == "adapt":
            raise ValueError("an adapted copy is changed in its own review (edit it, or reject it there)")
        if e["by"] in ("map", "rule"):
            raise ValueError(f"dropped by {e['by']}: not a judgement to flip")
        data = reviews.load_pool()
        by_id = {q["id"]: q for q in data["questions"]}
        if verdict == "keep":
            if e.get("copy"):
                raise ValueError(f"its copy {e['copy']} was rejected: reopen it in the review page instead")
            new = {**{k: e[k] for k in ("run",) if k in e}, "verdict": "keep", "reason": None, "by": "developer", "copy": None,
                   "note": "kept by the developer (was dropped: " + (e.get("reason") or "other") + ")"}
        else:
            if reason is not None and reason not in fit.REASONS:
                raise ValueError(f"reason must be one of {', '.join(fit.REASONS)}")
            cp = by_id.get(e.get("copy") or "")
            if cp is None:
                raise ValueError(f"{source_id} has no copy to reject")
            cp.update(status="rejected", review={
                "decision": "rejected", "feedback": "Flipped to drop by the developer (fit view)", "problems": [],
                "reviewed_on": reviews.now()[:10], "reviewer": "human", "previous": None})
            new = {**e, "verdict": "drop", "reason": reason or "other", "by": "developer",
                   "note": "dropped by the developer (was kept)"}
            new.pop("issue", None)
            reviews.save_pool(data)
        seen[source_id] = new
        fit.save_verdicts(bundle, seen)
    return new
