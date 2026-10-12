"""Pool targets per bundle (plans/12, D-53): shared by qgen.py and the authoring server."""
import json

import layout  # noqa: F401  (paths; also makes app/server importable, D-35)
from layout import TARGETS
import categories  # app/server/categories.py

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


def deficits(pool_questions, bundle):
    """{level: max(0, target − approved)} for the bundle (D-54); None without targets or deficits."""
    t = load_targets(bundle)
    if t is None:
        return None
    have = {}
    for q in pool_questions:
        if q["status"] == "approved" and q.get("bundle") == bundle:
            have[q["difficulty"]] = have.get(q["difficulty"], 0) + 1
    out = {lvl: max(0, n - have.get(lvl, 0)) for lvl, n in t["difficulty"].items()}
    return out if any(out.values()) else None


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
