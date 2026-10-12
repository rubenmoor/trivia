"""The family's save as one JSON document, written whole by the client (plans/49, D-67).

    game.json   {"version": 3, "players": [...], "games": [...], "seen": [...], "blocked": [...],
                 "notified_exhausted": [...], "flags": {...}, "reports": [...]}

Version 3 (plan 65) replaces `burned` with `seen` rows and `blocked`. `migrate()` still writes version 2;
the client upgrades it on load (engine/save.ts) and writes version 3 back.

The server only checks the envelope; the game rules live in the client's engine.
`migrate()` carries game.sqlite + flags.json over once (PORT-5); main.py calls it from PORT-7 on.
"""
import json, os, sqlite3, tempfile, time

import paths

FILE = paths.STATE / "game.json"
VERSION = 3  # the client upgrades older saves (engine/save.ts)
MIGRATE_VERSION = 2  # what migrate() writes
LISTS = {2: ("players", "games", "burned", "reports"), 3: ("players", "games", "seen", "blocked", "reports")}
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
    version = doc.get("version")
    if type(version) is not int or version not in LISTS:
        bad(f"version must be {MIGRATE_VERSION} or {VERSION}")
    for key in LISTS[version]:
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


def migrate():
    """One-time move game.sqlite + flags.json → game.json (PORT-5); the old files stay as the backup."""
    import game, flags  # game.py goes in PORT-8; only its init() is needed here
    db = paths.STATE / "game.sqlite"
    if FILE.exists() or not db.exists():
        return
    with tempfile.TemporaryDirectory() as tmpdir:
        src = sqlite3.connect(f"{db.as_uri()}?mode=ro", uri=True)  # read-only: reads -wal, never writes
        con = sqlite3.connect(os.path.join(tmpdir, "copy.sqlite"))
        try:
            src.backup(con)
            with con:
                game.init(con)  # upgrades legacy schemas on the copy
            q = lambda sql: con.execute(sql).fetchall()
            doc = {
                "version": MIGRATE_VERSION,
                "players": [{"id": i, "name": n, "created_on": c}
                            for i, n, c in q("SELECT id, name, created_on FROM players ORDER BY id")],
                "games": [{"id": i, "started_on": s, "finished_on": f, "result": r, "player_id": p,
                           "state": json.loads(st)}
                          for i, s, f, r, p, st in q("SELECT id, started_on, finished_on, result, player_id, state "
                                                     "FROM games ORDER BY id")],
                "burned": [{"question_id": qid, "player_id": p, "game_id": g, "burned_on": b}
                           for qid, p, g, b in q("SELECT question_id, player_id, game_id, burned_on FROM burned "
                                                 "ORDER BY game_id, question_id, player_id")],
                "flags": flags.load(),
                "reports": [],
            }
        finally:
            src.close()
            con.close()
    write(doc)
    print(f"migrated game.sqlite → game.json: {len(doc['players'])} players, {len(doc['games'])} games, "
          f"{len(doc['burned'])} burns, {len(doc['flags'])} flags")
