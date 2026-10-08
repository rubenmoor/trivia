"""What the next `qgen batch` does (D-36): shared by qgen.py and the authoring start page (RV-12)."""
import json

import layout  # noqa: F401  (paths; also makes app/server importable, D-35)
from layout import WORK
import categories  # app/server/categories.py: app/data/categories.json (D-19)

SUBCATEGORIES = 30  # per batch: the subcategories with the fewest approved questions


def unfinished_runs():
    """Names of `qgen batch` runs in work/ that haven't finished, sorted."""
    out = []
    for p in WORK.glob("*/run.json"):
        run = json.loads(p.read_text(encoding="utf-8")) or {}
        if run.get("mode") == "batch" and not run.get("done"):
            out.append(p.parent.name)
    return sorted(out)


def subcategories(pool, count=SUBCATEGORIES, bundle="base"):
    """The bundle's `count` subcategories with the fewest approved questions of that bundle in `pool`;
    ties in its categories.json order (D-41)."""
    approved = {}
    for q in pool:
        if q["status"] == "approved" and q.get("bundle") == bundle:
            approved[q["subcategory"]] = approved.get(q["subcategory"], 0) + 1
    order = categories.subcategories(bundle)
    return sorted(order, key=lambda s: (approved.get(s, 0), order.index(s)))[:count]
