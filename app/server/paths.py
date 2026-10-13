"""Where the game finds its files (plans/19-repo-layout.md, D-35).

Read-only files live next to the code in app/. Writable files (game state, the media cache)
default to state/ and media/ in the repo; a packaged build sets TRIVIA_STATE and TRIVIA_MEDIA.
"""
import os
from pathlib import Path

APP = Path(__file__).resolve().parent.parent  # app/
REPO = APP.parent

DATA = APP / "data"
POOL = DATA / "pool.json"  # approved questions, exported by `qgen export`
CATEGORIES = DATA / "categories.json"  # D-19: base's categories
BUNDLE_DATA = DATA / "bundles"  # D-43: another bundle's categories in bundles/<id>/categories.json
AGE_GROUPS = DATA / "age-groups.json"  # D-38
BUNDLES = DATA / "bundles.json"  # D-39


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


def names(locale, bundle="base"):
    """Display names in a locale (D-81): names.<locale>.json, a bundle's in bundles/<id>/."""
    return DATA / f"names.{locale}.json" if bundle == "base" else BUNDLE_DATA / bundle / f"names.{locale}.json"


DIST = APP / "client" / "dist"

STATE = Path(os.environ.get("TRIVIA_STATE") or REPO / "state")  # gitignored (D-25); empty = unset, as the desktop shell
MEDIA = Path(os.environ.get("TRIVIA_MEDIA") or REPO / "media")  # gitignored cache (D-17)
