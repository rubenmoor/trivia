"""Checks app/data/age-groups.json's `levels` and `level_weights` like the engine's parseAgeGroups (plan 27, D-76)."""
import math


def level_weights(window, levels):
    """{"<difficulty>": round(12 × Σ 1/(hi − lo + 1))} over the window (D-31, D-76)."""
    return {str(d): math.floor(12 * sum(1 / (hi - lo + 1) for lo, hi in levels if lo <= d <= hi) + 0.5)  # = JS Math.round
            for d in range(window[0], window[1] + 1)}


def level_problems(ag):
    """Errors: every group 12 levels with window lo ≤ lo ≤ hi ≤ window hi, `level_weights` as derived,
    unique ids, young_teens present."""
    errors, ids = [], [g.get("id") for g in ag.get("groups", [])]
    for g in ag.get("groups", []):
        wlo, whi = g["window"]
        levels = g.get("levels")
        if not isinstance(levels, list) or len(levels) != 12:
            errors.append(f"app/data/age-groups.json: {g['id']}: needs 12 levels")
            continue
        bad = [(i, r) for i, r in enumerate(levels, 1)
               if not (isinstance(r, list) and len(r) == 2 and all(type(x) is int for x in r) and wlo <= r[0] <= r[1] <= whi)]
        errors += [f"app/data/age-groups.json: {g['id']}: level {i} {r} not inside window {wlo}–{whi}" for i, r in bad]
        if not bad:
            want = level_weights(g["window"], levels)
            lw = g.get("level_weights")
            if not isinstance(lw, dict) or list(lw.items()) != list(want.items()):  # key order too, like the engine
                errors.append(f"app/data/age-groups.json: {g['id']}: level_weights must be {want}")
    if len(set(ids)) != len(ids):
        errors.append("app/data/age-groups.json: duplicate group id")
    if "young_teens" not in ids:
        errors.append("app/data/age-groups.json: no young_teens")
    return errors
