"""Checks app/data/age-groups.json's `levels` like the engine's parseAgeGroups (plan 27)."""


def level_problems(ag):
    """Errors: every group 12 levels with window lo ≤ lo ≤ hi ≤ window hi, unique ids, young_teens present."""
    errors, ids = [], [g.get("id") for g in ag.get("groups", [])]
    for g in ag.get("groups", []):
        wlo, whi = g["window"]
        levels = g.get("levels")
        if not isinstance(levels, list) or len(levels) != 12:
            errors.append(f"app/data/age-groups.json: {g['id']}: needs 12 levels")
            continue
        for i, r in enumerate(levels, 1):
            if not (isinstance(r, list) and len(r) == 2 and all(type(x) is int for x in r) and wlo <= r[0] <= r[1] <= whi):
                errors.append(f"app/data/age-groups.json: {g['id']}: level {i} {r} not inside window {wlo}–{whi}")
    if len(set(ids)) != len(ids):
        errors.append("app/data/age-groups.json: duplicate group id")
    if "young_teens" not in ids:
        errors.append("app/data/age-groups.json: no young_teens")
    return errors
