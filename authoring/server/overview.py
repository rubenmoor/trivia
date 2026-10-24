"""GET /api/overview: everything the authoring start page shows except the statistics
(plans/08-review-tool.md, "Start page", RV-12). Computed fresh from the pool on every call."""
from collections import Counter

import layout  # authoring/tools/layout.py
import batches  # authoring/tools/batches.py
import media  # authoring/tools/media.py
import media_cache  # authoring/tools/media_cache.py
import save_file  # authoring/tools/save_file.py
import engine  # authoring/tools/engine.py: selection.ts under Node (D-60)
import qgen  # authoring/tools/qgen.py: work runs
import translations  # authoring/tools/translations.py
import spot_checks  # authoring/server/spot_checks.py


def supply(pool):
    """The profile's supply (profile = save, plan 65) in the default game (decision 103): any count and
    unseen only, pool minus blocked."""
    blocked = save_file.blocked_ids()
    seen = save_file.seen_counts()
    avail = [q for q in pool if q["status"] == "approved" and q["id"] not in blocked]  # = selection.ts available
    anyc, unseen = engine.supplies((avail, blocked), ([q for q in avail if not seen[q["id"]]], blocked))
    by_seen = Counter(min(seen[q["id"]], 2) for q in avail if q.get("bundle", "base") in anyc["bundles"])
    return {"blocked": len(blocked), "unseen": by_seen[0], "seen_once": by_seen[1], "seen_twice": by_seen[2],
            "bundles": anyc["bundles"], "per_level": anyc["per_level"],
            "rows": [{"label": "any", "levels": anyc["supply"]}, {"label": "unseen", "levels": unseen["supply"]}]}


def unfinished_translate_runs():
    """Unfinished `qgen batch --translate` runs (tr-<locale>-<n>, = translate.next_translate_run), oldest first."""
    return [r for r in qgen.work_runs(r"tr-[A-Za-z-]+-\d+", "run.json")
            if translations.run_locale(r) and not (qgen.load_json(layout.WORK / r / "run.json") or {}).get("done")]


def spot_check_rows(pool):
    """Runs whose blind spot check isn't complete, oldest first: batches with a recorded LLM review, back-audit
    runs, and translation runs already started (they get no new one, milestone 9). {run, kind, decided, size}."""
    done = spot_checks.load()
    unfinished = set(batches.unfinished_runs())
    runs = [(r, "batch") for r in qgen.work_runs(r"batch-\d+", "recorded.json")
            if r not in unfinished and any(q.get("batch") == r for q in pool)]
    runs += [(r, "backaudit") for r in qgen.work_runs(r"backaudit-\d+", "run.json")]
    runs += [(r, "translation") for r in done if translations.run_locale(r)]
    rows = [{"run": r, "kind": k, "decided": len((done.get(r) or {}).get("items") or {}), "size": spot_checks.size(r)}
            for r, k in runs]
    return [r for r in rows if r["decided"] < r["size"]]


def batch_rows(pool, locale=None, src=None):
    """One row per batch, newest first (pool order is merge order); batch None is "none".
    With a locale: its translation entries' tr-* runs, by run number (plan 67); src: {id: source}.
    `sources`: the source locales in the row (decision 235), e.g. ["en"] for batch-9, ["es", "en"] for a tr-de run."""
    by_batch = {}
    for q in pool:
        by_batch.setdefault(q.get("batch"), []).append(q)
    groups = list(reversed(by_batch.items()))
    if locale:
        groups = sorted(((n, qs) for n, qs in groups if (n or "").startswith("tr-")),
                        key=lambda g: int(g[0].rsplit("-", 1)[1]), reverse=True)
    rows = []
    for name, qs in groups:
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
            "locale": locale,
            "sources": sorted({translations.source_locale((src or {}).get(q["id"], q)) for q in qs},
                              key=translations.LOCALES.index),
        })
    return rows


def locale_rows(pool):
    """Per locale with a pool (translations.exported): its entries by status, stale ones, the approved sources
    written in it (`own`), its approved translations per source locale (`from`), and the other approved sources
    that don't travel or have no translation yet (plan 67, decision 235)."""
    approved = [q for q in pool if q["status"] == "approved"]
    src = {q["id"]: q for q in pool}
    rows = []
    for locale in translations.LOCALES:
        if not translations.exported(locale, {"questions": pool}):
            continue
        entries = [t for t in translations.load(locale)["questions"] if t["id"] in src]
        have = {t["id"] for t in entries}
        status = Counter(t.get("status") for t in entries)
        other = [q for q in approved if translations.source_locale(q) != locale]
        rows.append({
            "locale": locale,
            "approved": status["approved"], "needs_work": status["needs_work"],
            "draft": status["draft"], "rejected": status["rejected"],
            "stale": translations.counts(locale, {"questions": pool})["stale"],
            "own": len(approved) - len(other),
            "from": dict(Counter(translations.source_locale(src[t["id"]]) for t in entries if t.get("status") == "approved")),
            "not_translatable": sum(not translations.translatable(q) for q in other),
            "untranslated": sum(translations.translatable(q) and q["id"] not in have for q in other),
        })
    return rows


def build(pool, bundles):
    sup = supply(pool)
    approved = [q for q in pool if q["status"] == "approved"]
    not_cached = sorted({url for q in approved for _, url in media_cache.picked(q)
                         if not media_cache.cache_path(url).is_file()})
    bundle_rows = []
    for b in bundles:
        if b["kind"] == "base":
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
            "licence_replace": sum(media.to_replace(q) for q in pool),
            "bundles": bundle_rows,
        },
        "llm_approved": sum((q.get("review") or {}).get("reviewer") == "llm" for q in approved),
        "spot_checks": spot_check_rows(pool),
        "unfinished_runs": batches.unfinished_runs() + unfinished_translate_runs(),
        "batches": [r for l in translations.LOCALES
                    for r in batch_rows(translations.load(l)["questions"], l, {q["id"]: q for q in pool})]
                   + batch_rows(pool),
        "locales": locale_rows(pool),
        "per_level": sup.pop("per_level"),
        "supply": sup,
        "next_batch_subcategories": batches.subcategories(pool),
        "counts": {"status": dict(Counter(q["status"] for q in pool)),
                   "bundle": dict(Counter(q.get("bundle") for q in approved))},
    }
