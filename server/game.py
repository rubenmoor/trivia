"""Game state (plans/03-game-flow.md, GF-4, GF-6, D-25, D-28): one running game at a time, in SQLite.

Every game belongs to a player (`players`). A question the player has seen is burned for that
player only (`burned.player_id`); NULL burns it for everyone (admin «Saltar y quemar para todos»).

A game's state is a JSON document in `games.state`:
    level       1..12, the level being played
    phase       "select" (4 cards on the table) | "question" (one picked) | "won" | "lost"
    options     question IDs on the table at this level
    offered     every question ID offered in this game (never offered twice)
    current     the picked question ID, or null
    answers     the picked question's 4 answers in the order shown
    history     [{"level", "question_id", "correct"}] — one entry per final answer
    last        the last final answer: {"question_id", "chosen", "correct", "correct_index"}
    undo        the state before the last final answer (one undo step), or null
The server shuffles the answers and checks the final answer; the client never sees the
correct answer before it submits.
"""
import contextlib, datetime, json, random, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import categories  # noqa: E402
import selection  # noqa: E402

DB = selection.STATE_DB


class GameError(ValueError):
    """A request that doesn't fit the game's state; `details` goes to the client."""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


@contextlib.contextmanager
def connect():
    """One transaction: committed on success, rolled back on an error; always closed."""
    con = sqlite3.connect(DB)
    try:
        with con:
            yield init(con)
    finally:
        con.close()


def init(con):
    con.executescript("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE COLLATE NOCASE,
            created_on TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            started_on TEXT NOT NULL,
            finished_on TEXT,
            result TEXT,            -- null while running; won | lost | abandoned
            state TEXT NOT NULL,
            player_id INTEGER REFERENCES players(id)  -- null only for games from before D-28
        );
    """)
    columns = lambda table: {row[1] for row in con.execute(f"PRAGMA table_info({table})")}
    if "player_id" not in columns("games"):
        con.execute("ALTER TABLE games ADD COLUMN player_id INTEGER REFERENCES players(id)")
    if "burned" in {row[0] for row in con.execute("SELECT name FROM sqlite_master")} \
            and "player_id" not in columns("burned"):
        # Before D-28 a burn counted for everyone: it keeps doing so (player_id NULL).
        con.execute("ALTER TABLE burned RENAME TO burned_old")
    con.executescript("""
        CREATE TABLE IF NOT EXISTS burned (
            question_id TEXT NOT NULL,
            player_id INTEGER REFERENCES players(id),  -- null: burned for everyone (D-28)
            game_id INTEGER NOT NULL,
            burned_on TEXT NOT NULL
        );
        CREATE UNIQUE INDEX IF NOT EXISTS burned_once ON burned (question_id, ifnull(player_id, 0));
    """)
    if "burned_old" in {row[0] for row in con.execute("SELECT name FROM sqlite_master")}:
        con.execute("INSERT INTO burned SELECT question_id, NULL, game_id, burned_on FROM burned_old")
        con.execute("DROP TABLE burned_old")
    return con


def clean_name(name):
    """A player name as typed: trimmed, inner spaces collapsed; GameError if empty or too long."""
    name = " ".join(str(name or "").split())
    if not name:
        raise GameError("falta el nombre del jugador")
    if len(name) > 30:
        raise GameError("el nombre es demasiado largo (máximo 30 letras)")
    return name


def players():
    """Known players, the most recent first, with their game counts (for the Player screen, UI-16)."""
    with connect() as con:
        rows = con.execute("""
            SELECT p.name, count(g.id), count(CASE WHEN g.result = 'won' THEN 1 END),
                   max(g.started_on), p.created_on
            FROM players p LEFT JOIN games g ON g.player_id = p.id
            GROUP BY p.id ORDER BY coalesce(max(g.started_on), p.created_on) DESC""").fetchall()
    return [{"name": n, "games": g, "won": w, "last_played": last} for n, g, w, last, _ in rows]


def latest(con):
    """(id, result, state, player_id) of the newest game, or None."""
    row = con.execute("SELECT id, result, state, player_id FROM games ORDER BY id DESC LIMIT 1").fetchone()
    return (row[0], row[1], json.loads(row[2]), row[3]) if row else None


def save(con, gid, state, result=None):
    finished = now() if result else None
    con.execute("UPDATE games SET state = ?, result = ?, finished_on = ? WHERE id = ?",
                (json.dumps(state, ensure_ascii=False), result, finished, gid))


def running(con):
    """(id, state, player_id) of the running game."""
    game = latest(con)
    if not game or game[1] is not None:
        raise GameError("no game is running")
    return game[0], game[2], game[3]


def questions_by_id(pool):
    return {q["id"]: q for q in pool}


def category_of(broad):
    return lambda q: broad[q["subcategory"]]["slug"] if q.get("subcategory") in broad else None


def asked_categories(state, by_id, broad):
    cat = category_of(broad)
    return {cat(by_id[h["question_id"]]) for h in state["history"] if h["question_id"] in by_id}


def draw(con, pid, state, pool, n=selection.PER_LEVEL, keep=()):
    """Draw n cards for the state's level from the questions still available to the player in this game."""
    broad = categories.broad_of()
    avail = selection.available(pool, selection.burned_for(con, pid), state["offered"])
    drawn = selection.draw(state["level"], avail, n=n, keep=keep,
                           avoid_categories=asked_categories(state, questions_by_id(pool), broad),
                           category_of=category_of(broad))
    if drawn is None:
        lo, hi = selection.LEVEL_RANGES[state["level"]]
        raise GameError(f"no quedan preguntas para el nivel {state['level']} (dificultad {lo}–{hi})")
    state["offered"] += [q["id"] for q in drawn]
    return [q["id"] for q in drawn]


def burn(con, qid, pid, gid):
    """Burn a question for the player, or for everyone with pid None (D-28)."""
    con.execute("INSERT OR IGNORE INTO burned VALUES (?, ?, ?, ?)", (qid, pid, gid, now()))


def supply(pool, player=None):
    """The supply check before a new game (GF-5), for a player name; None or a new name: the whole pool
    minus the global burns."""
    with connect() as con:
        pid = selection.player_id(con, clean_name(player)) if player else None
        avail = selection.available(pool, selection.burned_for(con, pid))
    levels = selection.supply(avail)
    return {"ok": not any(l["missing"] for l in levels), "available": len(avail), "levels": levels}


def new_game(pool, player):
    """Start a game for `player` (a known name or a new one, D-28); a running game is abandoned."""
    player = clean_name(player)
    report = supply(pool, player)
    if not report["ok"]:
        short = ", ".join(f"nivel {l['level']} (dificultad {l['range'][0]}–{l['range'][1]}): faltan {l['missing']}"
                          for l in report["levels"] if l["missing"])
        raise GameError(f"no hay suficientes preguntas: {short}", report)
    with connect() as con:
        game = latest(con)
        if game and game[1] is None:
            save(con, game[0], game[2], "abandoned")
        pid = selection.player_id(con, player)
        if pid is None:
            pid = con.execute("INSERT INTO players (name, created_on) VALUES (?, ?)", (player, now())).lastrowid
        state = {"level": 1, "phase": "select", "options": [], "offered": [], "current": None,
                 "answers": [], "history": [], "last": None, "undo": None}
        state["options"] = draw(con, pid, state, pool)
        con.execute("INSERT INTO games (started_on, state, player_id) VALUES (?, ?, ?)",
                    (now(), json.dumps(state), pid))
    return state


def pick(pool, index):
    with connect() as con:
        gid, state, _ = running(con)
        if state["phase"] != "select":
            raise GameError("no cards on the table")
        if not 0 <= index < len(state["options"]):
            raise GameError(f"no card {index + 1}")
        q = questions_by_id(pool)[state["options"][index]]
        answers = [q["answer"], *q["wrong_answers"]]
        random.shuffle(answers)
        state.update(phase="question", current=q["id"], answers=answers)
        save(con, gid, state)
    return state


def answer(pool, index):
    """The final answer: check it, burn the question, move on (next level, won or lost)."""
    with connect() as con:
        gid, state, pid = running(con)
        if state["phase"] != "question":
            raise GameError("no question to answer")
        if not 0 <= index < len(state["answers"]):
            raise GameError(f"no answer {index + 1}")
        q = questions_by_id(pool)[state["current"]]
        before = {**state, "undo": None}
        correct = state["answers"][index] == q["answer"]
        burn(con, q["id"], pid, gid)
        state["history"].append({"level": state["level"], "question_id": q["id"], "correct": correct})
        state["last"] = {"question_id": q["id"], "chosen": index, "correct": correct,
                         "correct_index": state["answers"].index(q["answer"])}
        state["undo"] = before
        result = None
        if not correct:
            state["phase"], result = "lost", "lost"
        elif state["level"] == selection.LEVELS:
            state["phase"], result = "won", "won"
        else:
            state.update(level=state["level"] + 1, phase="select", current=None, answers=[])
            state["options"] = draw(con, pid, state, pool)
        save(con, gid, state, result)
    return state


def skip(pool, everyone=False):
    """«Saltar pregunta»: the current question is burned for the player (for everyone with
    «Saltar y quemar para todos», D-28) and a new card replaces it."""
    with connect() as con:
        gid, state, pid = running(con)
        if state["phase"] != "question":
            raise GameError("only a question on screen can be skipped")
        by_id = questions_by_id(pool)
        rest = [i for i in state["options"] if i != state["current"]]
        burn(con, state["current"], None if everyone else pid, gid)
        new = draw(con, pid, state, pool, n=1, keep=[by_id[i] for i in rest])
        state["options"] = [new[0] if i == state["current"] else i for i in state["options"]]
        state.update(phase="select", current=None, answers=[])
        save(con, gid, state)
    return state


def undo():
    """Take back the last final answer: restore the state before it and un-burn the question for the player."""
    with connect() as con:
        game = latest(con)
        if not game or game[1] == "abandoned" or not game[2].get("undo"):
            raise GameError("nothing to undo")
        gid, _, state, pid = game
        con.execute("DELETE FROM burned WHERE question_id = ? AND player_id IS ? AND game_id = ?",
                    (state["last"]["question_id"], pid, gid))
        save(con, gid, state["undo"])
        return state["undo"]


def abandon():
    with connect() as con:
        game = latest(con)
        if game and game[1] is None:
            save(con, game[0], game[2], "abandoned")


def view(pool):
    """The newest game as the client sees it: no correct answer before the final answer."""
    with connect() as con:
        game = latest(con)
        if not game:
            return None
        gid, result, state, pid = game
        row = con.execute("SELECT name FROM players WHERE id = ?", (pid,)).fetchone()
    by_id = questions_by_id(pool)
    out = {"id": gid, "player": row[0] if row else None, "result": result,
           "level": state["level"], "phase": state["phase"],
           "options": [{"description": by_id[i]["description"]} for i in state["options"] if i in by_id],
           "history": [{"level": h["level"], "correct": h["correct"]} for h in state["history"]],
           "can_undo": bool(state.get("undo")) and result != "abandoned",
           "question": None, "last": None}
    if state["current"] in by_id:
        q = by_id[state["current"]]
        # No hints: they are only shown through the «Pista» joker, one at a time (D-26, JK-2).
        # No description: it belongs to the Select screen only (04, "Question").
        out["question"] = {k: q[k] for k in ["id", "question", "media", "background"]}
        out["question"]["answers"] = state["answers"]
    if state["last"] and state["last"]["question_id"] in by_id:
        q = by_id[state["last"]["question_id"]]
        out["last"] = {**state["last"], "answer": q["answer"], "fun_fact": q["fun_fact"]}
    return out
