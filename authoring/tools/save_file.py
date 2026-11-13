"""The game's save, read-only for authoring (plans/49, D-59, D-67, plan 99).

Reads TRIVIA_SAVE_DIR/game.json if set, else every save: state/game.json, state/desktop/<user>/game.json and the
packaged <appData>/trivia/save/<user>/game.json. Flags come from all of them (each named on stderr); seen counts and
blocked questions from the newest. Without a save: none of them. Never writes the save;
only its own ledger:

Version 5 (plan 157) adds multiplayer session rows to `games` (`seats`); this module reads none of that.
Version 6 (plan 195) adds `career` to player and game rows and `demo` to game rows; this module reads none of that.

    flags-applied.json   {"<question id>": "<flagged_on>[ <note>]"}   flags already turned into reviews (stamp())
"""
import json, os, sys
from collections import Counter
from functools import cache
from pathlib import Path

import atomic  # authoring/tools/atomic.py
import layout  # authoring/tools/layout.py
import paths  # authoring/tools/paths.py

APPLIED = paths.STATE / "flags-applied.json"  # gitignored, written by trivia-authoring only
DESKTOP = layout.REPO / "state" / "desktop"  # the dev shell's save folders, one per user (app/desktop/main.mjs)


def saves():
    """Every save file: TRIVIA_SAVE_DIR/game.json alone if set, else state/game.json, the dev shell's
    state/desktop/*/game.json and the packaged build's <appData>/trivia/save/*/game.json (main.mjs)."""
    if os.environ.get("TRIVIA_SAVE_DIR"):
        return [Path(os.environ["TRIVIA_SAVE_DIR"]) / "game.json"]
    app_data = Path(os.environ.get("APPDATA") or os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    found = [layout.REPO / "state" / "game.json", *DESKTOP.glob("*/game.json"), *(app_data / "trivia" / "save").glob("*/game.json")]
    return sorted((f for f in found if f.is_file()), key=lambda f: f.stat().st_mtime)


@cache
def path():
    """The newest save (seen counts, blocked questions), or None."""
    found = saves()
    if not found:
        return None
    print(f"save: {found[-1]}" + (f" (newest of {len(found)})" if len(found) > 1 else ""), file=sys.stderr)
    return found[-1]


def _doc(f=None):
    """A save parsed (default: the newest), or None."""
    f = f or path()
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f else None
    except FileNotFoundError:
        return None


def _seen_blocked():
    """(seen question IDs, one per event; blocked IDs); a v2 save is read as engine/save.ts upgrades it. Mod ids
    (`<mod>:<id>`, decision 128) dropped: player content never enters our counts."""
    doc = _doc()
    if doc is None:
        return [], set()
    if doc["version"] < 3:
        burned = doc["burned"]
        return ([b["question_id"] for b in burned if b["player_id"] is not None],
                {b["question_id"] for b in burned if b["player_id"] is None})
    return ([s["question_id"] for s in doc["seen"] if ":" not in s["question_id"]],
            {b for b in doc["blocked"] if ":" not in b})


def blocked_ids():
    """Questions blocked for everyone («Bloquear pregunta»)."""
    return _seen_blocked()[1]


def seen_counts():
    """{question_id: count} over the whole save (profile = save, plan 65)."""
    return Counter(_seen_blocked()[0])


def flags():
    """Flags of every save (see `_flags`), the latest flagged_on wins per question; each save read is printed."""
    out = {}
    for f in saves():
        found = _flags(_doc(f))
        print(f"save: {f}: {len(found)} flag(s)", file=sys.stderr)
        for k, v in found.items():
            if k not in out or v["flagged_on"] >= out[k]["flagged_on"]:
                out[k] = v
    return out


def _flags(doc):
    """Flagged questions {"<id>": {"flagged_on", "player", "level"?, "note"?, "locale"?, "shown"?}} (decision 102:
    the game's question locale, absent = es; shown = {question, answer, wrong_answers}); a v3 save's reports read as
    engine/save.ts upgrades them (decision 60). Mod ids dropped (decision 128: no flags for player content)."""
    if doc is None:
        return {}
    out = dict(doc.get("flags") or {})
    if doc["version"] < 4:
        names = {p["id"]: p["name"] for p in doc.get("players", [])}
        for r in doc.get("reports", []):
            old = out.get(r["question_id"])
            note = " · ".join(n for n in ((old or {}).get("note"), r.get("note")) if n)
            out[r["question_id"]] = {**(old or {"flagged_on": r["reported_on"], "player": names.get(r["player_id"]),
                                                "level": r["level"]}), **({"note": note} if note else {})}
    return {k: v for k, v in out.items() if ":" not in k}


def stamp(flag):
    """A flag's ledger value: a new note applies it again."""
    return f"{flag['flagged_on']} {flag['note']}" if flag.get("note") else flag["flagged_on"]


def applied():
    try:
        return json.loads(APPLIED.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def record_applied(entries):
    """Add {"<id>": stamp} to the ledger."""
    atomic.write_json(APPLIED, {**applied(), **entries})
