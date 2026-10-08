"""Category lists (D-19, D-43): broad categories with their subcategories, one list per bundle.

`base`'s list is app/data/categories.json; another bundle's is app/data/bundles/<id>/categories.json.
Subcategory names and slugs are unique across bundles, so a subcategory names its bundle's list.
"""
import json

from paths import BUNDLES, BUNDLE_DATA, CATEGORIES


def path(bundle):
    return CATEGORIES if bundle == "base" else BUNDLE_DATA / bundle / "categories.json"


def bundle_ids():
    """The bundles in app/data/bundles.json order (base first)."""
    return [b["id"] for b in json.loads(BUNDLES.read_text(encoding="utf-8"))["bundles"]]


def load(bundle=None):
    """[{"slug", "name", "bundle", "subcategories": [...]}, ...] in display order: one bundle's
    categories, or every bundle's (None), base first. A bundle without a file has none."""
    out = []
    for b in [bundle] if bundle else bundle_ids():
        p = path(b)
        if p.exists():
            out += [{**c, "bundle": b} for c in json.loads(p.read_text(encoding="utf-8"))["categories"]]
    return out


def subcategories(bundle=None):
    """Subcategory names in display order, of one bundle or of all."""
    return [s for c in load(bundle) for s in c["subcategories"]]


def broad_of():
    """subcategory -> its broad category ({"slug", "name", "bundle", ...}), across all bundles."""
    return {s: c for c in load() for s in c["subcategories"]}


def bundle_of(sub):
    """The bundle whose list has this subcategory, or None."""
    c = broad_of().get(sub)
    return c["bundle"] if c else None
