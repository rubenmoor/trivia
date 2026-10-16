"""The screen gallery for /gallery (plan 100): trivia-gallery's manifest and the developer's flags on UI strings,
authoring/data/ui-flags.json (tracked, so fix passes see them). Written only by the authoring server; a fix pass
sets a flag's fixed_on by hand."""
import datetime, json, re

import layout  # authoring/tools/layout.py
import atomic  # authoring/tools/atomic.py

FILE = layout.UI_FLAGS
MANIFEST = layout.GALLERY / "manifest.json"
FIELDS = ("locale", "key", "text", "shot")


def load_flags():
    return json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else []


def build():
    """GET /api/gallery: {"manifest": … or null before the first trivia-gallery run, "flags": [...]}."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else None
    return {"manifest": manifest, "flags": load_flags()}


def shot_path(locale, shot):
    """work/gallery/<locale>[@<W>x<H>]/<shot>.png, or None for a bad name or a missing file."""
    if not re.fullmatch(r"[\w-]+(@\d+x\d+)?", locale) or not re.fullmatch(r"[\w-]+\.png", shot):
        return None
    path = layout.GALLERY / locale / shot
    return path if path.is_file() else None


def change(body):
    """POST /api/gallery/flags: {"flag": {locale, key, text, shot, note}} adds, {"id", "note"} edits the note,
    {"id", "remove": true} removes; returns every flag."""
    with atomic.locked(FILE):
        flags = load_flags()
        if "flag" in body:
            f = body["flag"]
            if not all(isinstance(f.get(k), str) for k in ("locale", "text", "shot")):
                raise ValueError("a flag needs locale, text and shot")
            if f.get("key") is not None and not isinstance(f["key"], str):
                raise ValueError("key must be a string or null")
            flags.append({"id": max((x["id"] for x in flags), default=0) + 1, **{k: f.get(k) for k in FIELDS},
                          "note": note_of(f), "flagged_on": datetime.date.today().isoformat()})
        else:
            i = next((i for i, x in enumerate(flags) if x["id"] == body.get("id")), None)
            if i is None:
                raise ValueError(f"no flag {body.get('id')!r}")
            if body.get("remove") is True:
                flags.pop(i)
            else:
                flags[i]["note"] = note_of(body)
        atomic.write_json(FILE, flags)
    return flags


def note_of(body):
    note = body.get("note")
    if not isinstance(note, str) or not note.strip():
        raise ValueError("a flag needs a note")
    return note.strip()
