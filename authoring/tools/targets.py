"""Pool targets per bundle (plans/12, D-53): shared by qgen.py and the authoring server."""
import json, math
from collections import Counter

from layout import TARGETS
import categories  # authoring/tools/categories.py
import translations  # authoring/tools/translations.py (D-81)

NOT_BUNDLES = {"about", "batch_health", "quality"}  # top-level keys that aren't bundles (D-55, plan 16)


def load_all():
    return json.loads(TARGETS.read_text(encoding="utf-8")) if TARGETS.exists() else {}


def load_targets(bundle):
    """{"total": n, "difficulty": {level (int): n}} for the bundle, or None without targets."""
    t = load_all().get(bundle)
    if t is None:
        return None
    return {"total": t["total"], "difficulty": {int(k): v for k, v in t["difficulty"].items()}}


def load_quality():
    """{"spot_check_size": n, "min_agreement": fraction} (plan 16, pm decision 2), or None before it's stored."""
    t = load_all().get("quality")
    return t and {k: v for k, v in t.items() if k != "about"}


def quality_problems():
    """Errors in targets.json's "quality": spot_check_size an integer ≥ 1, min_agreement a fraction in (0, 1]."""
    t = load_quality()
    if t is None:
        return []
    rel, out = "authoring/data/targets.json", []
    if set(t) != {"spot_check_size", "min_agreement"}:
        out.append(f"{rel}: quality: keys must be spot_check_size and min_agreement")
    n, rate = t.get("spot_check_size"), t.get("min_agreement")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        out.append(f"{rel}: quality: spot_check_size must be an integer ≥ 1")
    if not isinstance(rate, (int, float)) or isinstance(rate, bool) or not 0 < rate <= 1:
        out.append(f"{rel}: quality: min_agreement must be a fraction in (0, 1]")
    return out


def load_batch_health():
    """{metric: {"min"/"max": x}} (plan 15, pm decision 13), or None before it's stored."""
    t = load_all().get("batch_health")
    return t and {k: v for k, v in t.items() if k != "about"}


def health_problems(metrics):
    """Errors in targets.json's "batch_health": known metric names, only numeric min/max."""
    rel = "authoring/data/targets.json"
    out = []
    for k, v in (load_batch_health() or {}).items():
        if k not in metrics:
            out.append(f"{rel}: batch_health: unknown metric {k!r}")
        elif not isinstance(v, dict) or not v or set(v) - {"min", "max"} \
                or not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v.values()):
            out.append(f"{rel}: batch_health: {k}: must be {{\"min\": n, \"max\": n}} (one or both)")
    return out


def approved_by_level(pool_questions, bundle, locale=None):
    """Counter {difficulty: approved} of the bundle; with a locale other than es, its playing
    translations by their own difficulty (D-81, plan 70)."""
    if locale in (None, "es"):
        return Counter(q["difficulty"] for q in pool_questions if q["status"] == "approved" and q.get("bundle") == bundle)
    src = {q["id"]: q for q in pool_questions if q.get("bundle") == bundle}
    return Counter(t["difficulty"] for t in translations.load(locale)["questions"]
                   if t["id"] in src and translations.plays(t, src[t["id"]]))


def deficits(pool_questions, bundle, locale=None):
    """{level: max(0, target − approved)} for the bundle (D-54), per locale (decision 37);
    None without targets or deficits."""
    t = load_targets(bundle)
    if t is None:
        return None
    have = approved_by_level(pool_questions, bundle, locale)
    out = {lvl: max(0, n - have[lvl]) for lvl, n in t["difficulty"].items()}
    return out if any(out.values()) else None


def source_supply(pool_questions, bundle="base"):
    """Per translation locale (plan 70, CT-4): yield, and per source level the es sources its deficit
    needs (deficit / yield) and the approved, translatable ones not yet translated (or stale)."""
    out = {}
    for l in translations.LOCALES:
        ts = {t["id"]: t for t in translations.load(l)["questions"]}
        y = translations.yield_rate(l)
        untranslated = Counter(q["difficulty"] for q in pool_questions
                               if q["status"] == "approved" and q.get("bundle") == bundle and translations.translatable(q)
                               and (q["id"] not in ts or translations.is_stale(ts[q["id"]], q)))
        need = {lvl: math.ceil(n / max(y, 0.1)) for lvl, n in (deficits(pool_questions, bundle, l) or {}).items()}
        out[l] = {"yield": y, "need": need, "untranslated": dict(untranslated)}
    return out


def source_shortfall(pool_questions, bundle="base", pending=None, supply=None):
    """{level: es sources to draft for the translations}: largest over the locales of need −
    untranslated (− `pending`: es deficits still to draft); None when zero (plan 70)."""
    supply = supply or source_supply(pool_questions, bundle)
    pending = pending or {}
    levels = (load_targets(bundle) or {}).get("difficulty", {})
    out = {lvl: max([0] + [s["need"].get(lvl, 0) - s["untranslated"].get(lvl, 0) - pending.get(lvl, 0)
                           for s in supply.values()]) for lvl in levels}
    return out if any(out.values()) else None


def draft_gaps(pool_questions, bundle):
    """What `draft` aims at (D-54, decision 37): the bundle's deficits; for base once they're met,
    the es source shortfall of the translations; None: even weights (D-40)."""
    return deficits(pool_questions, bundle) or (source_shortfall(pool_questions) if bundle == "base" else None)


def category_shares(bundle):
    """{broad category slug: derived share} = total × its subcategories / the bundle's (guide only)."""
    t = load_targets(bundle)
    if t is None:
        return None
    cats = categories.load(bundle)
    n = sum(len(c["subcategories"]) for c in cats)
    return {c["slug"]: t["total"] * len(c["subcategories"]) / n for c in cats} if n else {}


def problems(scale, bundle_ids):
    """Errors in targets.json: bundles known, levels = scale, values ≥ 0, sum = total."""
    rel = "authoring/data/targets.json"
    out = []
    lo, hi = scale
    for b, t in load_all().items():
        if b in NOT_BUNDLES:
            continue
        if b not in bundle_ids:
            out.append(f"{rel}: {b!r} is not a bundle")
            continue
        total, diff = t.get("total"), t.get("difficulty") or {}
        levels = {str(l) for l in range(lo, hi + 1)}
        if set(diff) != levels:
            missing, extra = sorted(levels - set(diff), key=int), sorted(set(diff) - levels)
            out.append(f"{rel}: {b}: levels must be {lo}–{hi}"
                       + (f"; missing {', '.join(missing)}" if missing else "")
                       + (f"; extra {', '.join(extra)}" if extra else ""))
        bad = [k for k, v in diff.items() if not isinstance(v, int) or v < 0]
        if bad:
            out.append(f"{rel}: {b}: targets must be integers ≥ 0: {', '.join(bad)}")
        elif not isinstance(total, int) or sum(diff.values()) != total:
            out.append(f"{rel}: {b}: difficulty targets sum to {sum(diff.values())}, total is {total}")
    return out
