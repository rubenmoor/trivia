"""The game's pool (D-35): app/data/pool.json is generated from authoring/data/questions.json."""
import json

import layout

PLAY_FIELDS = ["id", "status", "difficulty", "subcategory", "description", "question", "answer",
               "wrong_answers", "hints", "fun_fact"]
MEDIA_PLAY_FIELDS = ["type", "role", "file_url", "source_url", "credit"]
BACKGROUND_PLAY_FIELDS = ["file_url", "source_url", "credit"]


def export_text(pool):
    """app/data/pool.json: the approved questions with only what play needs (no reviews,
    ratings, revisions or pipeline fields). The game reads nothing else."""
    out = []
    for q in pool["questions"]:
        if q["status"] != "approved":
            continue
        e = {k: q[k] for k in PLAY_FIELDS}
        e["media"] = {k: q["media"].get(k) for k in MEDIA_PLAY_FIELDS}
        e["background"] = ({k: q["background"].get(k) for k in BACKGROUND_PLAY_FIELDS}
                           if q.get("background") else None)
        out.append(e)
    return json.dumps({"version": 1, "questions": out}, ensure_ascii=False, indent=2) + "\n"


def write(pool):
    """Write the export for this source pool (the parsed authoring/data/questions.json)."""
    layout.EXPORT.write_text(export_text(pool), encoding="utf-8")
