"""Questions flagged for review during a game (plans/05-gamemaster-controls.md, GM-5, D-47).

The game never writes the source pool (D-35), so flags go to the game state:

    flags.json   {"flags": {"<question id>": {"flagged_on": "<iso time>", "player": name or null}}}

`trivia-authoring` turns them into needs-work reviews when it starts and removes them here.
"""
import datetime, json

import paths

FILE = paths.STATE / "flags.json"


def load():
    try:
        return json.loads(FILE.read_text(encoding="utf-8"))["flags"]
    except FileNotFoundError:
        return {}


def save(flags):
    FILE.parent.mkdir(parents=True, exist_ok=True)  # a fresh install has no state/ yet
    tmp = FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"flags": flags}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(FILE)


def set_flag(qid, flagged, player=None):
    """Flag or unflag one question; returns every flagged question ID."""
    if not isinstance(qid, str) or not qid:
        raise ValueError("id must be a question ID")
    flags = load()
    if flagged:
        flags.setdefault(qid, {"flagged_on": datetime.datetime.now().isoformat(timespec="seconds"),
                               "player": player})
    else:
        flags.pop(qid, None)
    save(flags)
    return sorted(flags)
