"""Where the authoring tools find their files (plans/19-repo-layout.md, D-35).

Importing this module also makes the game's modules in app/server/ importable (categories,
selection, media_cache, paths): authoring may use app/, never the other way round.
"""
import os, sys
from pathlib import Path

AUTHORING = Path(__file__).resolve().parent.parent  # authoring/
REPO = AUTHORING.parent
APP_SERVER = REPO / "app" / "server"
if str(APP_SERVER) not in sys.path:
    sys.path.insert(0, str(APP_SERVER))

import paths as app_paths  # noqa: E402  (app/server/paths.py)

SOURCE_POOL = AUTHORING / "data" / "questions.json"  # every question, with reviews and pipeline fields
AXES_FILE = AUTHORING / "data" / "question-axes.json"  # question styles as axes (D-37)
CONCEPTS = AUTHORING / "data" / "concepts"  # one concept list per subcategory of base (D-37)
BUNDLE_DATA = AUTHORING / "data" / "bundles"  # another bundle's concepts/ and question-axes.json (D-43)
PROMPTS = AUTHORING / "tools" / "prompts"
REPORTS = AUTHORING / "reports"
DIST = AUTHORING / "ui" / "dist"
WORK = Path(os.environ.get("TRIVIA_WORK", REPO / "work"))  # gitignored pipeline work files
CANDIDATES = WORK / "media"  # Commons candidates per question
EXPORT = app_paths.POOL  # what the game reads: app/data/pool.json
AGE_GROUPS = app_paths.AGE_GROUPS  # age groups and the focus group (D-38)
BUNDLES = app_paths.BUNDLES  # question bundles (D-39)
