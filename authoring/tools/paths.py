"""The game's files as authoring sees them (plans/19-repo-layout.md, D-35; moved from app/server/, plan 99).

app/data/ is what the game reads; authoring's own writable files live in state/ (TRIVIA_STATE), the media
cache in media/ (TRIVIA_MEDIA).
"""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
APP = REPO / "app"

DATA = APP / "data"
POOL = DATA / "pool.json"  # approved questions, exported by `qgen export`
CATEGORIES = DATA / "categories.json"  # D-19: base's categories
BUNDLE_DATA = DATA / "bundles"  # D-43: another bundle's categories in bundles/<id>/categories.json
AGE_GROUPS = DATA / "age-groups.json"  # D-38
BUNDLES = DATA / "bundles.json"  # D-39
OLD_KEYS = DATA / "old-keys.json"  # decision 259: old category / subcategory keys → slugs


def locale_pool(locale):
    """pool.<locale>.json: a translated locale's approved questions (D-81)."""
    return DATA / f"pool.{locale}.json"


def pool(locale="es", bundle="base"):
    """A bundle's pool in a locale: base's at the top, a pack's in bundles/<id>/ (decision 66)."""
    name = "pool.json" if locale == "es" else f"pool.{locale}.json"
    return DATA / name if bundle == "base" else BUNDLE_DATA / bundle / name


def pool_files():
    """Every exported pool file that exists: every locale, base and packs."""
    return sorted([*DATA.glob("pool*.json"), *BUNDLE_DATA.glob("*/pool*.json")])


DEMO_DATA = DATA / "demo"  # decision 339: the demo's pools (base's entries of the listed ids)


def demo_pool(locale="es"):
    return DEMO_DATA / ("pool.json" if locale == "es" else f"pool.{locale}.json")


def names(locale, bundle="base"):
    """Display names in a locale (D-81): names.<locale>.json, a bundle's in bundles/<id>/."""
    return DATA / f"names.{locale}.json" if bundle == "base" else BUNDLE_DATA / bundle / f"names.{locale}.json"


STATE = Path(os.environ.get("TRIVIA_STATE") or REPO / "state")  # gitignored (D-25); empty = unset
MEDIA = Path(os.environ.get("TRIVIA_MEDIA") or REPO / "media")  # gitignored cache (D-17)
