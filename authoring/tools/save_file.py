"""The game's save, read-only for authoring (plans/49, D-59, D-67).

Reads state/game.json once it exists (after the switch-over, PORT-7); before that game.sqlite and
flags.json (the fallback goes in PORT-8). Never writes the save; only its own ledger:

    flags-applied.json   {"<question id>": "<flagged_on>"}   flags already turned into reviews
"""
import json, sqlite3

import layout  # noqa: F401  (authoring/tools/layout.py; makes app/server importable)
import flags as game_flags  # app/server/flags.py
import paths  # app/server/paths.py
import save  # app/server/save.py
import selection  # app/server/selection.py

APPLIED = paths.STATE / "flags-applied.json"  # gitignored, written by trivia-authoring only


def _doc():
    """game.json parsed, or None before the switch-over."""
    raw = save.load()
    return json.loads(raw) if raw is not None else None


def players():
    """Player names, sorted case-insensitively; [] when no game was ever played (D-28)."""
    doc = _doc()
    if doc is not None:
        return sorted((p["name"] for p in doc["players"]), key=str.casefold)
    if not selection.STATE_DB.is_file():
        return []
    try:
        with sqlite3.connect(f"file:{selection.STATE_DB}?mode=ro", uri=True) as con:
            return [row[0] for row in con.execute("SELECT name FROM players ORDER BY name COLLATE NOCASE")]
    except sqlite3.OperationalError:  # a save from before players existed
        return []


def burned_ids(player=None):
    """Burned question IDs for `player` (None: only the global burns); KeyError for an unknown name."""
    doc = _doc()
    if doc is None:
        return selection.burned_ids(player)
    pid = None
    if player:
        key = player.casefold()
        pid = next((p["id"] for p in doc["players"] if p["name"].casefold() == key), None)
        if pid is None:
            raise KeyError(player)
    return {b["question_id"] for b in doc["burned"] if b["player_id"] is None or b["player_id"] == pid}


def flags():
    """Flagged questions {"<id>": {"flagged_on", "player"}}."""
    doc = _doc()
    return doc.get("flags") or {} if doc is not None else game_flags.load()


def has_save():
    return save.FILE.is_file()


def applied():
    try:
        return json.loads(APPLIED.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def record_applied(entries):
    """Add {"<id>": "<flagged_on>"} to the ledger."""
    APPLIED.parent.mkdir(parents=True, exist_ok=True)
    tmp = APPLIED.with_suffix(".tmp")
    tmp.write_text(json.dumps({**applied(), **entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(APPLIED)
