"""What the next `qgen batch` does (D-36): shared by qgen.py and the authoring start page (RV-12)."""
import json, math

import layout  # noqa: F401  (paths; also makes app/server importable, D-35)
from layout import WORK
import categories  # app/server/categories.py: app/data/categories.json (D-19)

SHARE = 0.5  # per batch: this share of the bundle's subcategories, those with the fewest approved questions (D-46)


def unfinished_runs():
    """Names of `qgen batch` runs in work/ that haven't finished, sorted."""
    out = []
    for p in WORK.glob("*/run.json"):
        run = json.loads(p.read_text(encoding="utf-8")) or {}
        if run.get("mode") == "batch" and not run.get("done"):
            out.append(p.parent.name)
    return sorted(out)


def subcategories(pool, count=None, bundle="base"):
    """The bundle's `count` subcategories (default: SHARE of them, D-46) with the fewest approved
    questions of that bundle in `pool`; ties in its categories.json order (D-41)."""
    approved = {}
    for q in pool:
        if q["status"] == "approved" and q.get("bundle") == bundle:
            approved[q["subcategory"]] = approved.get(q["subcategory"], 0) + 1
    order = categories.subcategories(bundle)
    count = count or math.ceil(len(order) * SHARE)
    return sorted(order, key=lambda s: (approved.get(s, 0), order.index(s)))[:count]
