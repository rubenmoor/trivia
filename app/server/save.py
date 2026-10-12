"""The family's save as one JSON document, written whole by the client (plans/49, D-67).

    game.json   {"version": 1, "players": [...], "games": [...], "burned": [...], "flags": {...}}

The server only checks the envelope; the game rules live in the client's engine.
"""
import json, os, time

import paths

FILE = paths.STATE / "game.json"
VERSION = 1
MAX_BYTES = 10 * 1024 * 1024
RETRIES, RETRY_SLEEP = 10, 0.1  # Windows: antivirus/backup may hold the file


class SaveError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status, self.code = status, code


def load():
    """The stored document as text, or None."""
    try:
        return FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def check(doc):
    def bad(msg):
        raise SaveError(400, "bad_save", msg)
    if not isinstance(doc, dict):
        bad("save must be a JSON object")
    if doc.get("version") != VERSION:
        bad(f"version must be {VERSION}")
    for key in ("players", "games", "burned"):
        if not isinstance(doc.get(key), list):
            bad(f"{key} must be a list")
    if not isinstance(doc.get("flags"), dict):
        bad("flags must be an object")


def write(doc):
    """Replace the save atomically; SaveError 400 (bad envelope) or 503 (file locked)."""
    check(doc)
    raw = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(raw) > MAX_BYTES:
        raise SaveError(400, "bad_save", "save larger than 10 MB")
    FILE.parent.mkdir(parents=True, exist_ok=True)  # a fresh install has no state/ yet
    tmp = FILE.with_name(FILE.name + ".tmp")
    with open(tmp, "wb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    for attempt in range(RETRIES + 1):
        try:
            os.replace(tmp, FILE)
            return
        except PermissionError:
            if attempt < RETRIES:
                time.sleep(RETRY_SLEEP)
    tmp.unlink(missing_ok=True)
    raise SaveError(503, "save_locked", "game.json is locked by another program")
