"""Where the authoring tools find their files (plans/19-repo-layout.md, D-35).

authoring may read app/, never the other way round; the game's paths come from paths.py.
"""
import os
from pathlib import Path

AUTHORING = Path(__file__).resolve().parent.parent  # authoring/
REPO = AUTHORING.parent

import paths as app_paths  # noqa: E402  (authoring/tools/paths.py)

SOURCE_POOL = AUTHORING / "data" / "questions.json"  # every question, with reviews and pipeline fields
TARGETS = AUTHORING / "data" / "targets.json"  # pool targets per bundle (D-53)
HEALTH_ACKS = AUTHORING / "data" / "health-acks.json"  # the developer's acks of failing batches (plan 15, D-55)
SPOT_CHECKS = AUTHORING / "data" / "spot-checks.json"  # human spot checks per batch (plan 16)
ENGLISH_KEYS = AUTHORING / "data" / "english-keys.json"  # English answer + concept per non-en source (decision 232)
UI_FLAGS = AUTHORING / "data" / "ui-flags.json"  # the developer's flags on UI strings in /gallery (plan 100)
AXES_FILE = AUTHORING / "data" / "question-axes.json"  # question styles as axes (D-37)
CONCEPTS = AUTHORING / "data" / "concepts"  # one concept list per subcategory of base (D-37)
BUNDLE_SOURCES = AUTHORING / "data" / "bundles"  # another bundle's concepts/ and question-axes.json (D-43)
PROMPTS = AUTHORING / "tools" / "prompts"
REPORTS = AUTHORING / "reports"
DIST = AUTHORING / "ui" / "dist"
WORK = Path(os.environ.get("TRIVIA_WORK") or REPO / "work")  # gitignored pipeline work files
GALLERY = WORK / "gallery"  # trivia-gallery's shots and manifest (plan 100)
CANDIDATES = WORK / "media"  # Commons candidates per question
EXPORT = app_paths.POOL  # what the game reads: app/data/pool.json
AGE_GROUPS = app_paths.AGE_GROUPS  # age groups and the focus group (D-38)
BUNDLES = app_paths.BUNDLES  # question bundles (D-39)
LOCALE_POOL = app_paths.locale_pool  # app/data/pool.<locale>.json (D-81)
POOL_FILE = app_paths.pool  # a bundle's pool per locale; a pack's in app/data/bundles/<id>/ (decision 66)
POOL_FILES = app_paths.pool_files  # every exported pool file that exists
BUNDLE_DATA = app_paths.BUNDLE_DATA  # app/data/bundles/: a pack's files
NAMES = app_paths.names  # app/data/[bundles/<id>/]names.<locale>.json (D-81)


def translations(locale):
    """authoring/data/questions.<locale>.json: one locale's translations of the source (D-81)."""
    return AUTHORING / "data" / f"questions.{locale}.json"
