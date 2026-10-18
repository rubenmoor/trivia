"""The screen gallery for /gallery (plan 100): trivia-gallery's manifest and the developer's flags on UI strings,
authoring/data/ui-flags.json (tracked, so fix passes see them). Written only by the authoring server; a fix pass
sets a flag's fixed_on by hand."""
import datetime, json, re

import layout  # authoring/tools/layout.py
import atomic  # authoring/tools/atomic.py

FILE = layout.UI_FLAGS
FIELDS = ("locale", "key", "text", "shot")  # plus demo: true on a flag from /gallery?demo (plan 176)


def load_flags():
    return json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else []


def root(demo):
    return layout.GALLERY_DEMO if demo else layout.GALLERY


def build(query):
    """GET /api/gallery[?demo=1][&set=<name>]: {"manifest": … or null before the first trivia-gallery run, "flags": [...]};
    with set, the manifest is the review set work/gallery/sets/<name>.json (task 1581), an unknown set an error;
    with demo, work/gallery-demo/ instead of work/gallery/ (plan 176)."""
    base, name = root("demo" in query), query.get("set")
    path = base / "manifest.json"
    if name is not None:
        path = base / "sets" / f"{name}.json"
        if not re.fullmatch(r"[\w-]+", name) or not path.is_file():
            raise ValueError(f"no review set {name!r}: trivia-gallery --set {name} --only <shot>,… makes it")
    manifest = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
    return {"manifest": manifest, "flags": load_flags()}


def shot_path(file):
    """work/gallery[-demo]/[sets/<name>/]<locale>[@<W>x<H>]/<shot>.png (demo/ in front for the demo's), or None for a bad
    name or a missing file."""
    if not re.fullmatch(r"(demo/)?(sets/[\w-]+/)?[\w-]+(@\d+x\d+)?/[\w-]+\.png", file):
        return None
    demo = file.startswith("demo/")
    path = root(demo) / file.removeprefix("demo/")
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
                          "note": note_of(f), **({"demo": True} if f.get("demo") is True else {}), "flagged_on": datetime.date.today().isoformat()})
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
