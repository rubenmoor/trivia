"""Category list (D-19): broad categories with their subcategories, from app/data/categories.json."""
import json

from paths import CATEGORIES


def load():
    """[{"slug", "name", "subcategories": [...]}, ...] in display order."""
    return json.loads(CATEGORIES.read_text(encoding="utf-8"))["categories"]


def broad_of():
    """subcategory -> its broad category ({"slug", "name", ...})."""
    return {s: c for c in load() for s in c["subcategories"]}
