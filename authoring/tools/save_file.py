"""The game's save, read-only for authoring (plans/49, D-59, D-67).

Reads state/game.json once it exists (after the switch-over, PORT-7); before that game.sqlite and
flags.json (the fallback goes in PORT-8). Never writes the save; only its own ledger:

    flags-applied.json   {"<question id>": "<flagged_on>"}   flags already turned into reviews
"""
import json, sqlite3
from collections import Counter

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


def _legacy():
    """(seen question IDs, blocked IDs) from game.sqlite, mapped like v2 → v3 (plan 65)."""
    if not selection.STATE_DB.is_file():
        return [], set()
    with sqlite3.connect(f"file:{selection.STATE_DB}?mode=ro", uri=True) as con:
        try:
            rows = con.execute("SELECT question_id, player_id FROM burned").fetchall()
        except sqlite3.OperationalError:  # before D-28 every burn counted for everyone
            try:
                rows = [(q, None) for (q,) in con.execute("SELECT question_id FROM burned")]
            except sqlite3.OperationalError:
                return [], set()
    return [q for q, p in rows if p is not None], {q for q, p in rows if p is None}


def _seen_blocked():
    """(seen question IDs, one per event; blocked IDs); a v2 save is read as engine/save.ts upgrades it."""
    doc = _doc()
    if doc is None:
        return _legacy()
    if doc["version"] < 3:
        burned = doc["burned"]
        return ([b["question_id"] for b in burned if b["player_id"] is not None],
                {b["question_id"] for b in burned if b["player_id"] is None})
    return [s["question_id"] for s in doc["seen"]], set(doc["blocked"])


def blocked_ids():
    """Questions blocked for everyone («Bloquear pregunta»)."""
    return _seen_blocked()[1]


def seen_counts():
    """{question_id: count} over the whole save (profile = save, plan 65)."""
    return Counter(_seen_blocked()[0])


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
