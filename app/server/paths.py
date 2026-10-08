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
AGE_GROUPS = DATA / "age-groups.json"  # D-38; the game reads it from AG-7 on
BUNDLES = DATA / "bundles.json"  # D-39; the game reads it from BN-6 on
DIST = Path(os.environ.get("TRIVIA_DIST", APP / "client" / "dist"))

STATE = Path(os.environ.get("TRIVIA_STATE", REPO / "state"))  # gitignored (D-25)
MEDIA = Path(os.environ.get("TRIVIA_MEDIA", REPO / "media"))  # gitignored cache (D-17)
