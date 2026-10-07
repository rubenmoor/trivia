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
Jokers (plans/09-jokers.md, D-26, D-27, JK-2) add:
    purged      subcategories excluded from later draws in this game («Paso» with purge)
    hints_shown 0–3, the hints of the current question shown so far («Soplo»)
    struck      answer indexes struck out on the current question («Francotirador» misses)
    jokers      jokers played on the current question, in order
    swapped_to  the subcategory the players chose with «Cambiazo» for the current question, or null
    repeat      true from a «Francotirador» hit until a card is picked: the level repeats (JK-3)
Game settings (plans/13-game-modes.md, MD-1):
    settings    {"jokers": {joker: uses per game, or null = unlimited}}; all null by default (D-27).
                A joker's uses are counted over the whole game (history plus the question on
                screen); a «Francotirador» miss counts as a use.
History entries of answered questions have "correct"; questions replaced by a joker or skipped by
the admin have "outcome" (skipped | easier | category | sniped | admin_skip | admin_burn) instead.
The server shuffles the answers and checks the final answer; the client never sees the
correct answer before it submits.
"""
import contextlib, copy, datetime, json, random, sqlite3

import categories
import selection

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
    DB.parent.mkdir(parents=True, exist_ok=True)  # a fresh install has no state/ yet
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


def with_defaults(state):
    """Fill in the joker fields for games saved before JK-2."""
    for key, value in [("purged", []), ("hints_shown", 0), ("struck", []), ("jokers", []), ("swapped_to", None),
                       ("repeat", False), ("settings", {})]:
        state.setdefault(key, value)
    state["settings"]["jokers"] = {**UNLIMITED, **state["settings"].get("jokers", {})}
    return state


def delete_player(name):
    """Delete a player completely (GF-7): the player, all their games (a running one too) and
    everything burned for them. Questions burned for everyone stay burned."""
    with connect() as con:
        pid = selection.player_id(con, clean_name(name))
        if pid is None:
            raise GameError(f"no hay ningún jugador «{name}»")
        con.execute("DELETE FROM burned WHERE player_id = ?", (pid,))
        con.execute("DELETE FROM games WHERE player_id = ?", (pid,))
        con.execute("DELETE FROM players WHERE id = ?", (pid,))


def latest(con):
    """(id, result, state, player_id) of the newest game, or None."""
    row = con.execute("SELECT id, result, state, player_id FROM games ORDER BY id DESC LIMIT 1").fetchone()
    return (row[0], row[1], with_defaults(json.loads(row[2])), row[3]) if row else None


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


def available_now(con, pid, state, pool):
    """Questions that can still come up in this game: approved, not burned for the player or for
    everyone, not offered yet, not in a purged subcategory."""
    purged = set(state["purged"])
    return [q for q in selection.available(pool, selection.burned_for(con, pid), state["offered"])
            if q.get("subcategory") not in purged]


def draw(con, pid, state, pool, n=selection.PER_LEVEL, keep=()):
    """Draw n cards for the state's level from the questions still available to the player in this game."""
    broad = categories.broad_of()
    avail = available_now(con, pid, state, pool)
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
        state = with_defaults({"level": 1, "phase": "select", "options": [], "offered": [], "current": None,
                               "answers": [], "history": [], "last": None, "undo": None})
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
        state.update(phase="question", current=q["id"], answers=answers, repeat=False)
        save(con, gid, state)
    return state


def answer(pool, index):
    """The final answer: check it, burn the question, move on (next level, won or lost)."""
    with connect() as con:
        gid, state, pid = running(con)
        if state["phase"] != "question":
            raise GameError("no question to answer")
        if not 0 <= index < len(state["answers"]) or index in state["struck"]:
            raise GameError(f"no answer {index + 1}")
        q = questions_by_id(pool)[state["current"]]
        before = {**copy.deepcopy(state), "undo": None}
        correct = state["answers"][index] == q["answer"]
        burn(con, q["id"], pid, gid)
        state["history"].append({"level": state["level"], "question_id": q["id"], "correct": correct,
                                 "jokers": state["jokers"]})
        state["last"] = {"question_id": q["id"], "chosen": index, "correct": correct,
                         "correct_index": state["answers"].index(q["answer"])}
        state["undo"] = before
        result = None
        if not correct:
            state["phase"], result = "lost", "lost"
        elif state["level"] == selection.LEVELS:
            state["phase"], result = "won", "won"
        else:
            state.update(level=state["level"] + 1, phase="select")
            leave_question(state)
            state["options"] = draw(con, pid, state, pool)
        save(con, gid, state, result)
    return state


def leave_question(state):
    """Reset what belongs to the question on screen."""
    state.update(current=None, answers=[], hints_shown=0, struck=[], jokers=[], swapped_to=None)


def drop_current(con, gid, pid, state, by_id, outcome, burn_for):
    """Burn the question on screen (for `burn_for`: the player's ID, or None = everyone) and log it."""
    burn(con, state["current"], burn_for, gid)
    state["history"].append({"level": state["level"], "question_id": state["current"], "outcome": outcome,
                             "jokers": state["jokers"]})


def back_to_select(con, gid, pid, state, pool, outcome, burn_for, purge=False):
    """Drop the question on screen and refill the table (admin skip, «Paso»). With `purge`, its
    subcategory leaves the game, and other cards of it on the table are replaced too (not burned:
    the players only saw their descriptions)."""
    by_id = questions_by_id(pool)
    sub = by_id[state["current"]].get("subcategory")
    drop_current(con, gid, pid, state, by_id, outcome, burn_for)
    removed = {state["current"]}
    if purge:
        state["purged"].append(sub)
        removed |= {i for i in state["options"] if by_id[i].get("subcategory") == sub}
    keep = [by_id[i] for i in state["options"] if i not in removed]
    try:
        new = draw(con, pid, state, pool, n=len(removed), keep=keep)
    except GameError:
        raise GameError("sin este tema no alcanzan las preguntas" if purge
                        else "no hay otra pregunta para este nivel")
    state["options"] = [new.pop(0) if i in removed else i for i in state["options"]]
    state["phase"] = "select"
    leave_question(state)


def skip(pool, everyone=False):
    """«Saltar pregunta» (admin): the current question is burned for the player (for everyone with
    «Saltar y quemar para todos», D-28) and a new card replaces it. Not a joker."""
    with connect() as con:
        gid, state, pid = running(con)
        if state["phase"] != "question":
            raise GameError("only a question on screen can be skipped")
        back_to_select(con, gid, pid, state, pool, "admin_burn" if everyone else "admin_skip",
                       None if everyone else pid)
        save(con, gid, state)
    return state


# Jokers (plans/09-jokers.md, JK-2) ---------------------------------------------------------------

def later_fill(avail, level):
    """(question IDs the matching uses for the levels after `level`, whether they all fill)."""
    assignment, missing = selection.assign(avail, range(level + 1, selection.LEVELS + 1))
    return {i for ids in assignment.values() for i in ids}, not missing


def replacement(avail, level, cands, order, fill=None):
    """The best of `cands` by `order` (random among ties) whose removal still lets every later
    level fill with 4 cards (GF-2), or None."""
    used, ok = fill or later_fill(avail, level)
    if not ok:
        return None
    later = range(level + 1, selection.LEVELS + 1)
    cands = list(cands)
    random.shuffle(cands)
    cands.sort(key=order)
    for q in cands:
        if q["id"] not in used or not selection.assign([x for x in avail if x["id"] != q["id"]], later)[1]:
            return q
    return None


def category_candidates(avail, level, sub):
    return [q for q in avail if q.get("subcategory") == sub and selection.in_range(q, level)]


def swap_in(con, gid, pid, state, pool, new, outcome):
    """Replace the question on screen in place with `new` (Bájale, Cambiazo)."""
    by_id = questions_by_id(pool)
    old = state["current"]
    drop_current(con, gid, pid, state, by_id, outcome, pid)
    answers = [new["answer"], *new["wrong_answers"]]
    random.shuffle(answers)
    state["options"] = [new["id"] if i == old else i for i in state["options"]]
    state["offered"].append(new["id"])
    leave_question(state)
    state.update(current=new["id"], answers=answers)


def play_hint(con, gid, pid, state, pool):
    """«Soplo»: show the next hint."""
    if state["hints_shown"] >= len(questions_by_id(pool)[state["current"]]["hints"]):
        raise GameError("no quedan pistas")
    state["hints_shown"] += 1
    state["jokers"].append("hint")
    return {"hint": state["hints_shown"]}


def play_skip(con, gid, pid, state, pool, purge=False):
    """«Paso»: back to Select with a new card; optionally the subcategory leaves the game."""
    state["jokers"].append("skip")
    sub = questions_by_id(pool)[state["current"]].get("subcategory")
    back_to_select(con, gid, pid, state, pool, "skipped", pid, purge=purge)
    return {"purged": sub if purge else None}


def play_easier(con, gid, pid, state, pool):
    """«Bájale»: an easier question of the same subcategory, the hardest of those below (09)."""
    cur = questions_by_id(pool)[state["current"]]
    avail = available_now(con, pid, state, pool)
    cands = [q for q in avail if q.get("subcategory") == cur.get("subcategory") and q["difficulty"] < cur["difficulty"]]
    new = replacement(avail, state["level"], cands, lambda q: -q["difficulty"])
    if not new:
        raise GameError("no hay preguntas más fáciles de este tema")
    state["jokers"].append("easier")
    swap_in(con, gid, pid, state, pool, new, "easier")
    return {"from": cur["difficulty"], "to": new["difficulty"]}


def play_category(con, gid, pid, state, pool, subcategory=None):
    """«Cambiazo»: a question of the level's range from the subcategory the players chose,
    preferring the current difficulty, then ±1 (09)."""
    cur = questions_by_id(pool)[state["current"]]
    if subcategory not in categories.broad_of():
        raise GameError("ese tema no existe")
    if subcategory == cur.get("subcategory"):
        raise GameError("ya están en ese tema")
    avail = available_now(con, pid, state, pool)
    new = replacement(avail, state["level"], category_candidates(avail, state["level"], subcategory),
                      lambda q: abs(q["difficulty"] - cur["difficulty"]))
    if not new:
        raise GameError("no hay preguntas de ese tema para este nivel")
    state["jokers"].append("category")
    swap_in(con, gid, pid, state, pool, new, "category")
    state["swapped_to"] = subcategory
    return {"subcategory": subcategory}


def play_snipe(con, gid, pid, state, pool, index=None):
    """«Francotirador» (JK-3): shoot an answer. A wrong one is struck out; hitting the right one
    burns the question and repeats the level with 4 fresh cards (D-27)."""
    left = len(state["answers"]) - len(state["struck"])
    if left <= 1:
        raise GameError("solo queda una respuesta")
    if not isinstance(index, int) or not 0 <= index < len(state["answers"]) or index in state["struck"]:
        raise GameError("no se puede apuntar a esa respuesta")
    q = questions_by_id(pool)[state["current"]]
    state["jokers"].append("snipe")
    correct_index = state["answers"].index(q["answer"])
    if index != correct_index:
        state["struck"].append(index)
        return {"outcome": "miss", "index": index}
    drop_current(con, gid, pid, state, questions_by_id(pool), "sniped", pid)
    try:
        state["options"] = draw(con, pid, state, pool)
    except GameError:
        raise GameError("si le dan a la correcta, no quedan preguntas para repetir el nivel")
    state.update(phase="select", repeat=True)
    leave_question(state)
    return {"outcome": "hit", "index": index, "correct_index": correct_index}


JOKERS = {"hint": play_hint, "skip": play_skip, "easier": play_easier, "category": play_category,
          "snipe": play_snipe}


UNLIMITED = {name: None for name in JOKERS}
# «Como las cartas»: the printed card set (JK-11), for the overlay's preset (MD-4).
CARDS = {"hint": 4, "skip": 2, "easier": 2, "category": 2, "snipe": 2}
SPENT = {"hint": "ya no les quedan Soplos", "skip": "ya no les quedan Pasos", "easier": "ya no les quedan Bájales",
         "category": "ya no les quedan Cambiazos", "snipe": "ya no les quedan Francotiradores"}


def jokers_left(state):
    """Per joker: uses left in this game, or None = unlimited (MD-1)."""
    used = [j for h in state["history"] for j in h.get("jokers", [])] + state["jokers"]
    return {name: None if limit is None else max(0, limit - used.count(name))
            for name, limit in state["settings"]["jokers"].items()}


def set_jokers(budget):
    """Set the running game's joker budget (MD-4): {joker: count or null}; missing jokers stay as they are."""
    if not isinstance(budget, dict) or not set(budget) <= set(JOKERS):
        raise GameError("unknown joker in the budget")
    for v in budget.values():
        if v is not None and (not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 99):
            raise GameError("a budget is a count from 0 to 99, or null for unlimited")
    with connect() as con:
        gid, state, _ = running(con)
        state["settings"]["jokers"].update(budget)
        save(con, gid, state)
    return state


def joker(pool, name, **args):
    """Play a joker on the question on screen; returns what happened (for the client's animation)."""
    if name not in JOKERS:
        raise GameError(f"no joker {name!r}")
    with connect() as con:
        gid, state, pid = running(con)
        if state["phase"] != "question":
            raise GameError("los comodines solo se juegan en una pregunta")
        if jokers_left(state)[name] == 0:
            raise GameError(SPENT[name])
        event = JOKERS[name](con, gid, pid, state, pool, **args)
        save(con, gid, state)
    return {"joker": name, **event}


def trial(con, fn, *args, **kwargs):
    """Run `fn` without keeping anything: None if it works, else its GameError message."""
    con.execute("SAVEPOINT trial")
    try:
        fn(con, *args, **kwargs)
        return None
    except GameError as e:
        return str(e)
    finally:
        con.execute("ROLLBACK TO trial")
        con.execute("RELEASE trial")


def jokers_view(con, gid, pid, state, pool):
    """Per joker: available, and the reason if not (09, "Availability"). «Cambiazo» also lists
    the subcategories possible right now, grouped by broad category."""
    def check(fn, **args):
        reason = trial(con, lambda c: fn(c, gid, pid, copy.deepcopy(state), pool, **args))
        return {"available": reason is None, "reason": reason}

    cur = questions_by_id(pool)[state["current"]]
    out = {"hint": check(play_hint), "skip": check(play_skip), "easier": check(play_easier),
           # Availability tries the worst case, a hit; the client only learns yes or no.
           "snipe": check(play_snipe, index=state["answers"].index(cur["answer"]))}
    out["skip"]["purge"] = {**check(play_skip, purge=True), "subcategory": cur.get("subcategory")}

    avail = available_now(con, pid, state, pool)
    fill = later_fill(avail, state["level"])
    groups = []
    for c in categories.load():
        subs = [{"name": s, "available": s != cur.get("subcategory") and replacement(
                    avail, state["level"], category_candidates(avail, state["level"], s), lambda q: 0, fill) is not None}
                for s in c["subcategories"]]
        groups.append({"slug": c["slug"], "name": c["name"], "available": any(s["available"] for s in subs),
                       "subcategories": subs})
    possible = any(g["available"] for g in groups)
    out["category"] = {"available": possible, "reason": None if possible else "no hay preguntas de otros temas para este nivel",
                       "categories": groups}
    for name, left in jokers_left(state).items():
        if left == 0:
            out[name].update(available=False, reason=SPENT[name])
    return out


def undo():
    """Take back the last final answer: restore the state before it and un-burn the question for the player."""
    with connect() as con:
        game = latest(con)
        if not game or game[1] == "abandoned" or not game[2].get("undo"):
            raise GameError("nothing to undo")
        gid, _, state, pid = game
        con.execute("DELETE FROM burned WHERE question_id = ? AND player_id IS ? AND game_id = ?",
                    (state["last"]["question_id"], pid, gid))
        restored = {**state["undo"], "settings": state["settings"]}
        save(con, gid, restored)
        return restored


def abandon():
    with connect() as con:
        game = latest(con)
        if game and game[1] is None:
            save(con, game[0], game[2], "abandoned")


def view(pool):
    """The newest game as the client sees it: no correct answer before the final answer."""
    by_id = questions_by_id(pool)
    with connect() as con:
        game = latest(con)
        if not game:
            return None
        gid, result, state, pid = game
        row = con.execute("SELECT name FROM players WHERE id = ?", (pid,)).fetchone()
        playing = result is None and state["phase"] == "question" and state["current"] in by_id
        jokers = jokers_view(con, gid, pid, state, pool) if playing else None
    out = {"id": gid, "player": row[0] if row else None, "result": result,
           "level": state["level"], "phase": state["phase"],
           "options": [{"description": by_id[i]["description"]} for i in state["options"] if i in by_id],
           "history": [{"level": h["level"], "correct": h["correct"]} for h in state["history"] if "correct" in h],
           "can_undo": bool(state.get("undo")) and result != "abandoned",
           "purged": state["purged"], "repeat": state["repeat"], "jokers": jokers,
           "settings": state["settings"], "jokers_left": jokers_left(state), "question": None, "last": None}
    if state["current"] in by_id:
        q = by_id[state["current"]]
        # Only the hints shown through «Soplo», one per use (D-26, D-27).
        # No description: it belongs to the Select screen only (04, "Question").
        out["question"] = {k: q[k] for k in ["id", "question", "media", "background"]}
        out["question"].update(answers=state["answers"], hints=q["hints"][:state["hints_shown"]],
                               struck=state["struck"], swapped_to=state["swapped_to"])
    if state["last"] and state["last"]["question_id"] in by_id:
        q = by_id[state["last"]["question_id"]]
        out["last"] = {**state["last"], "answer": q["answer"], "fun_fact": q["fun_fact"]}
    return out
