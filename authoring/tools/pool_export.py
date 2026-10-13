"""The game's pool (D-35): app/data/pool.json is generated from authoring/data/questions.json;
app/data/pool.<locale>.json from it and authoring/data/questions.<locale>.json (D-81)."""
import hashlib
import json

import atomic
import layout

PLAY_FIELDS = ["id", "status", "difficulty", "subcategory", "bundle", "description", "question", "answer",
               "wrong_answers", "hints", "fun_fact"]
MEDIA_PLAY_FIELDS = ["type", "role", "file_url", "source_url", "credit", "provider", "license", "license_url", "author",
                     "author_url"]
BACKGROUND_PLAY_FIELDS = ["file_url", "source_url", "credit", "provider", "license", "license_url", "author", "author_url"]


def play_entry(q):
    """An approved question with only what play needs (no reviews, ratings, revisions or pipeline fields)."""
    e = {k: q[k] for k in PLAY_FIELDS}
    e["media"] = {k: q["media"].get(k) for k in MEDIA_PLAY_FIELDS}
    e["background"] = ({k: q["background"].get(k) for k in BACKGROUND_PLAY_FIELDS}
                       if q.get("background") else None)
    return e


def pool_text(entries):
    """hash: first 8 hex of sha256 over the questions' own JSON (indent 2, D-92)."""
    questions = json.dumps(entries, ensure_ascii=False, indent=2)
    digest = hashlib.sha256(questions.encode("utf-8")).hexdigest()[:8]
    return json.dumps({"version": 1, "hash": digest, "questions": entries}, ensure_ascii=False, indent=2) + "\n"


def export_text(pool):
    """app/data/pool.json: the approved questions. The game reads nothing else."""
    return pool_text([play_entry(q) for q in pool["questions"] if q["status"] == "approved"])


def exports(pool):
    """{path: text}: pool.json and pool.<locale>.json for every locale with a translation file."""
    import translations  # authoring/tools/translations.py (imports this module)
    return {layout.EXPORT: export_text(pool), **translations.exports(pool)}


def write(pool):
    """Write the exports for this source pool (the parsed authoring/data/questions.json); atomic per file."""
    for path, text in exports(pool).items():
        atomic.write_text(path, text)
