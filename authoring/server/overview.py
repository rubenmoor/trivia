"""GET /api/overview: everything the authoring start page shows except the statistics
(plans/08-review-tool.md, "Start page", RV-12). Computed fresh from the pool on every call."""
from collections import Counter

import layout  # noqa: F401  (authoring/tools/layout.py; makes app/server importable)
import batches  # authoring/tools/batches.py
import media_cache  # app/server/media_cache.py
import save_file  # authoring/tools/save_file.py
import selection  # app/server/selection.py


def supply(pool):
    """The profile's supply (profile = save, plan 65): any count and unseen only, pool minus blocked."""
    blocked = save_file.blocked_ids()
    seen = save_file.seen_counts()
    avail = selection.available(pool, blocked)
    by_seen = Counter(min(seen[q["id"]], 2) for q in avail)
    return {"blocked": len(blocked), "unseen": by_seen[0], "seen_once": by_seen[1], "seen_twice": by_seen[2],
            "rows": [{"label": "any", "levels": selection.supply(avail)},
                     {"label": "unseen", "levels": selection.supply([q for q in avail if not seen[q["id"]]])}]}


def batch_rows(pool):
    """One row per batch, newest first (pool order is merge order); batch None is "none"."""
    by_batch = {}
    for q in pool:
        by_batch.setdefault(q.get("batch"), []).append(q)
    rows = []
    for name, qs in reversed(by_batch.items()):
        status = Counter(q["status"] for q in qs)
        reviews = [q.get("review") or {} for q in qs]
        report = name and (layout.REPORTS / f"{name}.md").is_file()
        rows.append({
            "name": name or "none",
            "date": max((r.get("reviewed_on") or "" for r in reviews), default="") or None,
            "merged": len(qs),
            "approved": status["approved"], "needs_work": status["needs_work"],
            "rejected": status["rejected"], "draft": status["draft"],
            "human": sum(r.get("reviewer") == "human" for r in reviews),
            "llm_approved": sum(q["status"] == "approved" and r.get("reviewer") == "llm" for q, r in zip(qs, reviews)),
            "report": f"/reports/{name}.md" if report else None,
        })
    return rows


def build(pool, bundles):
    approved = [q for q in pool if q["status"] == "approved"]
    not_cached = sorted({url for q in approved for _, url in media_cache.picked(q)
                         if not media_cache.cache_path(url).is_file()})
    bundle_rows = []
    for b in bundles:
        if b["always_on"]:
            continue  # base: nothing to check, every question starts there
        qs = [q for q in pool if q.get("bundle") == b["id"] and q["status"] != "rejected"]
        bundle_rows.append({"id": b["id"], "name": b["name"], "questions": len(qs),
                            "unreviewed": sum((q.get("review") or {}).get("reviewer") != "human" for q in qs)})
    return {
        "queues": {
            "needs_work": sum(q["status"] == "needs_work" for q in pool),
            "drafts": sum(q["status"] == "draft" for q in pool),
            "approved_without_media": sum(not q["media"].get("file_url") for q in approved),
            "not_cached": len(not_cached),
            "bundles": bundle_rows,
        },
        "llm_approved": sum((q.get("review") or {}).get("reviewer") == "llm" for q in approved),
        "unfinished_runs": batches.unfinished_runs(),
        "batches": batch_rows(pool),
        "supply": supply(pool),
        "per_level": selection.PER_LEVEL,
        "next_batch_subcategories": batches.subcategories(pool),
        "counts": {"status": dict(Counter(q["status"] for q in pool)),
                   "bundle": dict(Counter(q.get("bundle") for q in approved))},
    }
