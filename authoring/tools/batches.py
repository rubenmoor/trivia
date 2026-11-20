"""What the next `qgen batch` does (D-36): shared by qgen.py and the authoring start page (RV-12)."""
import json, math

from layout import WORK
import categories  # authoring/tools/categories.py: app/data/categories.json (D-19)
import targets  # authoring/tools/targets.py: pool targets (D-53)

MODES = {"batch": "qgen batch", "media-first": "qgen batch --media-first"}  # run.json mode → the command that finishes it (decision 646)
SHARE = 0.5  # per batch: this share of the bundle's subcategories, those with the fewest approved questions (D-46)
# a bundle's first draft run (plan 232): ≈ 50 approved at the 0.62 approved per slot of first en runs (batch-9, 26, 27, 29)
PILOT_SUBCATEGORIES, PILOT_SLOTS = 27, 3


def unfinished_runs():
    """Names of `qgen batch` and `qgen batch --media-first` runs in work/ that haven't finished, sorted."""
    out = []
    for p in WORK.glob("*/run.json"):
        run = json.loads(p.read_text(encoding="utf-8")) or {}
        if run.get("mode") in MODES and not run.get("done"):
            out.append(p.parent.name)
    return sorted(out)


def pilot(pool, bundle):
    """The bundle has no drafted source yet (copies don't count): its next `qgen batch` is a pilot (plan 232)."""
    return not any(q.get("bundle") == bundle and not q.get("copied_from") for q in pool)


def subcategories(pool, count=None, bundle="base"):
    """The bundle's `count` subcategories (default: SHARE of them, D-46; a pilot's PILOT_SUBCATEGORIES) with the fewest
    approved questions of that bundle in `pool` (copies too), each weighted by its level's share of the deficits to the
    targets (D-54; a base bundle: the draft gap over its question locales, decision 236); ties in its categories.json
    order (D-41), a pilot's spread over the categories (each category's first, then its second …)."""
    deficit = targets.draft_gaps(pool, bundle)
    total = sum(deficit.values()) if deficit else 0
    approved = {}
    for q in pool:
        if q["status"] == "approved" and q.get("bundle") == bundle:
            w = deficit.get(q["difficulty"], 0) / total if deficit else 1
            approved[q["subcategory"]] = approved.get(q["subcategory"], 0) + w
    order = categories.subcategories(bundle)
    first = count is None and pilot(pool, bundle)
    count = count or (PILOT_SUBCATEGORIES if first else math.ceil(len(order) * SHARE))
    rank = {s: i for c in categories.load(bundle) for i, s in enumerate(c["subcategories"])} if first else {}
    return sorted(order, key=lambda s: (approved.get(s, 0), rank.get(s, 0), order.index(s)))[:count]
