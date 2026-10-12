#!/usr/bin/env python3
"""Parity fixtures for the TypeScript engine (plan 18, PORT-1): scripted games through the
untouched Python referee (app/server/game.py, selection.py), recorded as JSON.

    python3 authoring/tools/record_fixtures.py            write app/client/src/engine/fixtures/
    python3 authoring/tools/record_fixtures.py --check    re-record into a temp dir and diff; exit 1 on a difference

Never touches state/: the game state lives in a temp dir, set before the game modules load.
Randomness is a tape: every `random.shuffle` is recorded as {"site", "n", "perm"} (perm[j] = old
index of the element now at j). Every step has a fixed `now`. Categories and pools are synthetic.
Every step names its `pool` (a scenario may switch pools, always right before a `new`).
"""
import argparse, atexit, contextlib, copy, datetime, inspect, json, os, random, shutil, sqlite3, sys, tempfile
from pathlib import Path

STATE = Path(tempfile.mkdtemp(prefix="trivia-fixtures-")).resolve()
os.environ["TRIVIA_STATE"] = str(STATE)  # before anything imports paths
atexit.register(shutil.rmtree, STATE, True)

import layout  # noqa: E402
import categories, game, selection  # noqa: E402  (app/server/)
import main as server  # noqa: E402

for _db in (game.DB, selection.STATE_DB):
    if not _db.resolve().is_relative_to(STATE):
        shutil.rmtree(STATE, ignore_errors=True)
        sys.exit(f"record_fixtures: refusing to run, game state at {_db} is outside {STATE}")

FIXTURES = layout.REPO / "app" / "client" / "src" / "engine" / "fixtures"
START = datetime.datetime(2026, 1, 1)

SCENARIOS = {}  # name -> (about, seed, pool name, fn(rec))


# Synthetic categories and pools --------------------------------------------------------------------

CATEGORIES = [  # categories.load() output (with "bundle")
    {"slug": "ciencia", "name": "Ciencia", "bundle": "base", "subcategories": ["Planetas", "Inventos"]},
    {"slug": "cultura", "name": "Cultura", "bundle": "base", "subcategories": ["Música", "Fútbol"]},
    {"slug": "colombia", "name": "Colombia", "bundle": "colombia",
     "subcategories": ["Ciudades de Colombia", "Comida colombiana"]},
]
SUBS = [(s, c["bundle"]) for c in CATEGORIES for s in c["subcategories"]]


def media(i):
    kind = ["image", "image", "audio", "video"][i % 4]
    return {"type": kind, "role": "illustrative", "file_url": f"https://example.org/{kind}/{i}",
            "source_url": f"https://example.org/file/{i}", "credit": f"Autor {i} · CC BY 4.0"}


def make_pool(prefix, counts):
    """`counts[d - 1]` approved questions of difficulty d; subcategories rotate per difficulty, hints 0–3."""
    out = []
    for d, count in enumerate(counts, 1):
        for k in range(count):
            i = len(out) + 1
            sub, bundle = SUBS[(k + d) % len(SUBS)]
            out.append({
                "id": f"{prefix}-{i:03d}", "status": "approved", "difficulty": d, "subcategory": sub,
                "bundle": bundle, "description": f"Pista de la carta {i} ({sub}, nivel {d}).",
                "question": f"¿Pregunta {i} sobre {sub.lower()}, dificultad {d}?",
                "answer": f"Respuesta {i}", "wrong_answers": [f"Falsa {i}{x}" for x in "abc"],
                "hints": [f"Pista {i}.{h}" for h in range(1, (i % 4) + 1)],
                "media": media(i), "fun_fact": f"Dato curioso {i}.",
                "background": {"file_url": f"https://example.org/bg/{i}", "source_url": f"https://example.org/file/bg{i}",
                               "credit": f"Fondo {i} · CC BY-SA 4.0"} if i % 7 == 0 else None})
    return out


POOLS = {  # pool name -> questions (pool.json entries)
    # Several games per player, with jokers.
    "main": make_pool("m", [8, 8, 8, 9, 9, 9, 9, 9, 10, 11]),
    # Exactly the 48 cards of one game: every question is needed, so no replacement ever fits
    # (Bájale, Cambiazo, purge, snipe hit) and a player's second game fails the supply check.
    "tight": make_pool("t", [4, 4, 4, 4, 4, 4, 4, 4, 8, 8]),
}


def scenario(name, about, seed, pool="main"):
    def register(fn):
        SCENARIOS[name] = (about, seed, pool, fn)
        return fn
    return register


# Dispatch: what app/server/main.py answers for each route -----------------------------------------

def dispatch(call, args, pool):
    """(status, body) as main.py sends it. Exceptions other than GameError (a 500) propagate."""
    if call == "get_game":
        try:
            return 200, {"game": game.view(pool), "supply": game.supply(pool, args.get("player"))}
        except game.GameError as e:
            return 400, server.error_body(e)
    if call == "players":
        return 200, game.players()
    if call == "delete_player":
        try:
            game.delete_player(args.get("name"))
            return 200, game.players()
        except game.GameError as e:
            return 409, server.error_body(e)
    actions = {"new": lambda: game.new_game(pool, args.get("player")),
               "pick": lambda: game.pick(pool, int(args.get("index", -1))),
               "answer": lambda: game.answer(pool, int(args.get("index", -1))),
               "skip": lambda: game.skip(pool, bool(args.get("everyone"))),
               "undo": lambda: game.undo(),
               "abandon": lambda: game.abandon(),
               "jokers": lambda: game.set_jokers(args.get("jokers")),
               "joker": lambda: game.joker(pool, str(args.get("joker")), **{
                   k: args[k] for k in ("purge", "subcategory", "index") if k in args})}
    if call not in actions:
        raise ValueError(f"unknown call {call!r}")
    try:
        result = actions[call]()
        out = {"game": game.view(pool)}
        if call == "joker":
            out["event"] = result
        return 200, out
    except game.GameError as e:
        return 409, server.error_body(e)


# Recording -----------------------------------------------------------------------------------------

def snapshot():
    """The whole game DB after a step (plan 18, "Fixture layout")."""
    if not game.DB.exists():
        return {"players": [], "games": [], "burned": []}
    con = sqlite3.connect(game.DB)
    try:
        q = lambda sql: con.execute(sql).fetchall()
        return {
            "players": [{"id": i, "name": n, "created_on": c}
                        for i, n, c in q("SELECT id, name, created_on FROM players ORDER BY id")],
            "games": [{"id": i, "started_on": s, "finished_on": f, "result": r, "player_id": p,
                       "state": json.loads(st)}
                      for i, s, f, r, p, st in q("SELECT id, started_on, finished_on, result, player_id, state "
                                                 "FROM games ORDER BY id")],
            "burned": [{"question_id": qid, "player_id": p, "game_id": g, "burned_on": b}
                       for qid, p, g, b in q("SELECT question_id, player_id, game_id, burned_on FROM burned "
                                             "ORDER BY game_id, question_id, player_id")]}
    finally:
        con.close()


class Recorder:
    """One scenario: fresh state, a seeded shuffle tape, a fixed `now` per step."""

    def __init__(self, seed, pool):
        for p in STATE.iterdir():
            p.unlink()
        self.rng = random.Random(seed)
        self.use(pool)
        self.steps, self.tape, self.now = [], [], None

    def use(self, pool):
        self.pool_name, self.pool = pool, POOLS[pool]
        self.by_id = {q["id"]: q for q in self.pool}

    def shuffle(self, xs):
        n = len(xs)
        perm = list(range(n))
        self.rng.shuffle(perm)
        xs[:] = [xs[i] for i in perm]
        self.tape.append({"site": inspect.currentframe().f_back.f_code.co_name, "n": n, "perm": perm})

    @contextlib.contextmanager
    def patched(self):
        saved = random.shuffle, game.now, categories.load
        random.shuffle, game.now = self.shuffle, lambda: self.now
        categories.load = lambda bundle=None: [copy.deepcopy(c) for c in CATEGORIES if bundle in (None, c["bundle"])]
        try:
            yield self
        finally:
            random.shuffle, game.now, categories.load = saved

    def __call__(self, call, **args):
        """Play one step; returns the response body."""
        self.now = (START + datetime.timedelta(minutes=len(self.steps))).isoformat(timespec="seconds")
        self.tape = []
        status, body = dispatch(call, args, copy.deepcopy(self.pool))  # main.py reads the pool per request
        self.steps.append({"now": self.now, "pool": self.pool_name, "call": call, "args": args, "tape": self.tape,
                           "response": {"status": status, "body": body}, "db": snapshot()})
        return body

    def ok(self, call, **args):
        body = self(call, **args)
        assert self.steps[-1]["response"]["status"] == 200, (call, args, body)
        return body

    def fail(self, error, call, status=409, **args):
        before = self.steps[-1]["db"] if self.steps else snapshot()
        body = self(call, **args)
        assert self.steps[-1]["response"]["status"] == status and body["error"] == error, (call, args, error, body)
        assert self.steps[-1]["db"] == before, ("an error changed the DB", call, args)
        return body

    def state(self):
        return self.steps[-1]["db"]["games"][-1]["state"]

    def view(self):
        return next(s["response"]["body"]["game"] for s in reversed(self.steps)
                    if s["response"]["status"] == 200 and isinstance(s["response"]["body"], dict))

    def jokers(self):
        return self.view()["jokers"]

    def current(self):
        return self.by_id[self.state()["current"]]

    def correct(self):
        return self.state()["answers"].index(self.current()["answer"])

    def wrong(self):
        s = self.state()
        return next(i for i in range(len(s["answers"])) if i != self.correct() and i not in s["struck"])

    def card(self, pred=lambda q: True):
        """Index of the first card on the table matching `pred`, or None."""
        return next((i for i, qid in enumerate(self.state()["options"]) if pred(self.by_id[qid])), None)

    def level_up(self, index=0):
        self.ok("pick", index=index)
        self.ok("answer", index=self.correct())

    def find(self, pred):
        """Level up until a card on the table matches `pred`; its index."""
        for _ in range(selection.LEVELS):
            i = self.card(pred)
            if i is not None:
                return i
            self.level_up()
        raise AssertionError("no matching card")


# Selection cases: direct calls into selection.py -------------------------------------------------

def selection_call(fn, args):
    """Questions are `pool` minus `without` (IDs); `burns` are written to the DB before `supply`."""
    pool = POOLS.get(args.get("pool"), [])
    without = set(args.get("without", []))
    questions = [copy.deepcopy(q) for q in pool if q["id"] not in without]
    if fn == "in_range":
        return selection.in_range({"difficulty": args["difficulty"]}, args["level"])
    if fn == "assign":
        assignment, missing = selection.assign(questions, args["levels"])
        return {"assignment": assignment, "missing": missing}
    if fn == "supply":
        with game.connect() as con:
            for i, name in enumerate(args.get("players", []), 1):
                con.execute("INSERT INTO players VALUES (?, ?, ?)", (i, name, START.isoformat()))
            for b in args.get("burns", []):
                pid = selection.player_id(con, b["player"]) if b["player"] else None
                con.execute("INSERT INTO burned VALUES (?, ?, 1, ?)", (b["question_id"], pid, START.isoformat()))
        return selection.supply(selection.available(questions, selection.burned_ids(args.get("player"))))
    if fn == "draw":
        by_id = {q["id"]: q for q in questions}
        keep = [copy.deepcopy(q) for q in pool if q["id"] in args.get("keep", [])]
        category_of = game.category_of(categories.broad_of()) if args.get("category_of") == "broad" else None
        drawn = selection.draw(args["level"], list(by_id.values()), n=args.get("n", selection.PER_LEVEL),
                               keep=keep, avoid_categories=set(args.get("avoid_categories", [])),
                               category_of=category_of)
        return None if drawn is None else [q["id"] for q in drawn]
    raise ValueError(f"unknown selection fn {fn!r}")


def ids(pool, pred):
    return [q["id"] for q in POOLS[pool] if pred(q)]


def selection_cases():
    """`selection.json`: {name, fn, args, tape, result} per case; each case has a fresh DB and seed."""
    cases = []

    def case(name, fn, **args):
        rec = Recorder(len(cases) + 1, "main")
        rec.now = START.isoformat()
        with rec.patched():
            result = selection_call(fn, args)
        cases.append({"name": name, "fn": fn, "args": args, "tape": rec.tape, "result": result})

    for level, (lo, hi) in selection.LEVEL_RANGES.items():
        for d in sorted({lo - 1, lo, hi, hi + 1}):
            case(f"in_range level {level} difficulty {d}", "in_range", level=level, difficulty=d)

    case("assign all levels, main", "assign", pool="main", levels=list(range(1, 13)))
    case("assign all levels, tight", "assign", pool="tight", levels=list(range(1, 13)))
    case("assign later levels only", "assign", pool="main", levels=list(range(7, 13)))
    case("assign unsorted subset", "assign", pool="main", levels=[12, 3, 9, 1])
    case("assign no levels", "assign", pool="main", levels=[])
    case("assign tight without two of difficulty 1", "assign", pool="tight", levels=list(range(1, 13)),
         without=ids("tight", lambda q: q["difficulty"] == 1)[:2])
    case("assign tight without difficulty 10", "assign", pool="tight", levels=list(range(1, 13)),
         without=ids("tight", lambda q: q["difficulty"] == 10))
    case("assign tight without difficulty 5 and 6", "assign", pool="tight", levels=list(range(2, 13)),
         without=ids("tight", lambda q: q["difficulty"] in (5, 6)))
    case("assign empty pool", "assign", pool="none", levels=[1, 2, 12])

    case("supply main", "supply", pool="main")
    case("supply tight", "supply", pool="tight")
    case("supply tight minus a global burn", "supply", pool="tight",
         burns=[{"question_id": "t-001", "player": None}])
    tight_burns = [{"question_id": q, "player": "Ana"} for q in ids("tight", lambda q: q["difficulty"] >= 9)[:5]]
    case("supply tight minus player burns, that player", "supply", pool="tight", players=["Ana", "Íngrid"],
         burns=tight_burns, player="ana")
    case("supply tight minus player burns, other player", "supply", pool="tight", players=["Ana", "Íngrid"],
         burns=tight_burns, player="íngrid")
    case("supply tight minus player burns, new player", "supply", pool="tight", players=["Ana", "Íngrid"],
         burns=tight_burns)
    case("supply main minus mixed burns", "supply", pool="main", players=["Ana"],
         burns=[{"question_id": q, "player": "Ana" if i % 2 else None}
                for i, q in enumerate(ids("main", lambda q: q["difficulty"] in (1, 10)))], player="Ana")
    case("supply empty pool", "supply", pool="none")

    for level in (1, 2, 6, 11, 12):
        case(f"draw level {level}, main", "draw", pool="main", level=level)
        case(f"draw level {level}, main, broad categories", "draw", pool="main", level=level, category_of="broad")
    case("draw level 1, tight", "draw", pool="tight", level=1, category_of="broad")
    case("draw level 9, tight", "draw", pool="tight", level=9, category_of="broad")
    lvl4 = ids("main", lambda q: 4 <= q["difficulty"] <= 6)
    case("draw keep 3, n 1", "draw", pool="main", level=4, n=1, keep=lvl4[:3], without=lvl4[:3],
         category_of="broad")
    case("draw keep 3, n 1, subcategories", "draw", pool="main", level=4, n=1,
         keep=lvl4[:3], without=lvl4[:3])
    case("draw keep 2, n 2", "draw", pool="main", level=8, n=2, without=ids("main", lambda q: q["difficulty"] == 7)[:2],
         keep=ids("main", lambda q: q["difficulty"] == 7)[:2], category_of="broad")
    case("draw avoid categories", "draw", pool="main", level=5, avoid_categories=["ciencia", "cultura"],
         category_of="broad")
    case("draw avoid every category", "draw", pool="main", level=5,
         avoid_categories=["ciencia", "cultura", "colombia"], category_of="broad")
    case("draw avoid subcategories", "draw", pool="main", level=3, avoid_categories=["Planetas", "Música", "Fútbol"])
    case("draw n 1", "draw", pool="main", level=10, n=1, category_of="broad")
    case("draw n 3", "draw", pool="main", level=7, n=3, category_of="broad")
    case("draw n 0", "draw", pool="main", level=7, n=0)
    case("draw unfillable, no candidates", "draw", pool="main", level=12,
         without=ids("main", lambda q: q["difficulty"] >= 9))
    case("draw unfillable, too few candidates", "draw", pool="main", level=1,
         without=ids("main", lambda q: q["difficulty"] == 1)[3:], category_of="broad")
    case("draw unfillable, later levels need them", "draw", pool="tight", level=11, category_of="broad",
         without=ids("tight", lambda q: q["difficulty"] == 8) + ids("tight", lambda q: q["difficulty"] >= 9)[5:])
    case("draw later levels reject some candidates", "draw", pool="tight", level=10, category_of="broad",
         without=ids("tight", lambda q: q["difficulty"] == 7)[:1] + ids("tight", lambda q: q["difficulty"] >= 8)[9:])
    case("draw empty pool", "draw", pool="none", level=1)
    return cases


# Game scenarios: rules and jokers (plan 18, "Scenarios") -----------------------------------------

@scenario("win", "A new player answers all 12 levels right and wins; undo after the win.", 1)
def win(rec):
    rec.ok("get_game", player="Ana")
    rec.ok("new", player="Ana")
    for _ in range(selection.LEVELS):
        rec.level_up()
    assert rec.view()["result"] == "won"
    rec.ok("get_game", player="Ana")
    rec.ok("undo")
    rec.ok("answer", index=rec.correct())


@scenario("lose-undo", "A wrong answer loses; undo brings the question back and keeps the settings; "
          "a second undo has nothing to undo.", 2)
def lose_undo(rec):
    rec.ok("new", player="Ana")
    rec.fail("nothing_to_undo", "undo")
    rec.level_up()
    rec.ok("pick", index=1)
    rec.ok("jokers", jokers={"hint": 2, "snipe": 0})
    rec.ok("answer", index=rec.wrong())
    assert rec.view()["result"] == "lost"
    rec.ok("get_game", player="Ana")
    rec.ok("undo")
    assert rec.view()["phase"] == "question" and rec.view()["settings"]["jokers"]["hint"] == 2
    rec.fail("nothing_to_undo", "undo")
    rec.ok("answer", index=rec.correct())
    rec.ok("undo")


@scenario("hint", "«Soplo» until no hints are left; a question with no hints at all.", 3)
def hint(rec):
    rec.ok("new", player="Ana")
    rec.ok("pick", index=rec.find(lambda q: len(q["hints"]) == 3))
    for _ in range(3):
        rec.ok("joker", joker="hint")
    assert rec.jokers()["hint"]["reason"]["code"] == "hints_used_up"
    rec.fail("hints_used_up", "joker", joker="hint")
    rec.ok("answer", index=rec.correct())
    rec.ok("pick", index=rec.find(lambda q: not q["hints"]))
    assert not rec.jokers()["hint"]["available"]
    rec.fail("hints_used_up", "joker", joker="hint")
    rec.ok("answer", index=rec.correct())


@scenario("skip-purge", "«Paso»; «Paso» with purge replacing the other table cards of that subcategory; "
          "both unavailable on the tight pool.", 4)
def skip_purge(rec):
    rec.ok("new", player="Ana")
    rec.ok("pick", index=0)
    rec.ok("joker", joker="skip")
    rec.ok("pick", index=0)
    rec.ok("joker", joker="skip", purge=True)
    rec.ok("pick", index=rec.find(lambda q: [rec.by_id[i]["subcategory"] for i in rec.state()["options"]]
                                  .count(q["subcategory"]) > 1))
    assert rec.jokers()["skip"]["purge"]["available"]
    rec.ok("joker", joker="skip", purge=True)
    rec.level_up()
    rec.use("tight")
    rec.ok("new", player="Bea")
    rec.ok("pick", index=0)
    assert not rec.jokers()["skip"]["available"] and not rec.jokers()["skip"]["purge"]["available"]
    rec.fail("refill_empty", "joker", joker="skip")
    rec.fail("purge_short", "joker", joker="skip", purge=True)


@scenario("easier", "«Bájale» at level 1 (nothing easier), then twice where it works; "
          "unavailable on the tight pool.", 5)
def easier(rec):
    rec.ok("new", player="Ana")
    rec.ok("pick", index=0)
    assert not rec.jokers()["easier"]["available"]
    rec.fail("easier_none", "joker", joker="easier")
    rec.ok("answer", index=rec.correct())
    played = 0
    for _ in range(selection.LEVELS - 1):
        rec.ok("pick", index=0)
        while played < 2 and rec.jokers()["easier"]["available"]:
            rec.ok("joker", joker="easier")
            played += 1
        if played >= 2:
            break
        rec.ok("answer", index=rec.correct())
    assert played >= 2
    rec.ok("answer", index=rec.correct())
    rec.use("tight")
    rec.ok("new", player="Bea")
    rec.level_up()
    rec.ok("pick", index=0)
    assert not rec.jokers()["easier"]["available"]
    rec.fail("easier_none", "joker", joker="easier")


@scenario("category", "«Cambiazo» to an available subcategory; the same one; an unknown one; an empty one; "
          "no subcategory possible on the tight pool.", 6)
def category(rec):
    rec.ok("new", player="Ana")
    rec.ok("pick", index=0)
    subs = lambda ok: [s["name"] for g in rec.jokers()["category"]["categories"] for s in g["subcategories"]
                       if s["available"] == ok and s["name"] != rec.current()["subcategory"]]
    rec.ok("joker", joker="category", subcategory=subs(True)[0])
    rec.fail("category_same", "joker", joker="category", subcategory=rec.current()["subcategory"])
    rec.fail("category_unknown", "joker", joker="category", subcategory="Astrología")
    rec.fail("category_unknown", "joker", joker="category")
    for _ in range(selection.LEVELS - 1):
        if subs(False):
            break
        rec.ok("answer", index=rec.correct())
        rec.ok("pick", index=0)
    rec.fail("category_empty", "joker", joker="category", subcategory=subs(False)[0])
    rec.ok("joker", joker="category", subcategory=subs(True)[-1])
    rec.ok("answer", index=rec.correct())
    rec.use("tight")
    rec.ok("new", player="Bea")
    rec.ok("pick", index=0)
    assert rec.jokers()["category"]["reason"]["code"] == "category_none"
    other = next(s for c in CATEGORIES for s in c["subcategories"] if s != rec.current()["subcategory"])
    rec.fail("category_empty", "joker", joker="category", subcategory=other)


@scenario("snipe", "«Francotirador»: misses until one answer is left; a struck answer; a hit repeats the level; "
          "a hit with no cards left on the tight pool.", 7)
def snipe(rec):
    rec.ok("new", player="Ana")
    rec.ok("pick", index=0)
    rec.ok("joker", joker="snipe", index=rec.wrong())
    rec.fail("snipe_invalid", "joker", joker="snipe", index=rec.state()["struck"][0])
    rec.fail("snipe_invalid", "joker", joker="snipe", index=4)
    rec.fail("snipe_invalid", "joker", joker="snipe")
    rec.ok("joker", joker="snipe", index=rec.wrong())
    rec.ok("joker", joker="snipe", index=rec.wrong())
    assert rec.jokers()["snipe"]["reason"]["code"] == "snipe_last"
    rec.fail("snipe_last", "joker", joker="snipe", index=rec.correct())
    rec.ok("answer", index=rec.correct())
    rec.ok("pick", index=0)
    assert rec.jokers()["snipe"]["available"]
    rec.ok("joker", joker="snipe", index=rec.correct())
    assert rec.view()["repeat"] and rec.view()["level"] == 2
    rec.ok("pick", index=1)
    rec.ok("answer", index=rec.correct())
    rec.use("tight")
    rec.ok("new", player="Bea")
    rec.ok("pick", index=0)
    assert rec.jokers()["snipe"]["reason"]["code"] == "snipe_no_repeat"
    rec.fail("snipe_no_repeat", "joker", joker="snipe", index=rec.correct())
    rec.ok("joker", joker="snipe", index=rec.wrong())
    rec.ok("answer", index=rec.correct())


@scenario("budget", "Joker budgets: the «Como las cartas» preset, partial budgets, spending to 0, "
          "invalid budgets.", 8)
def budget(rec):
    rec.ok("new", player="Ana")
    rec.ok("jokers", jokers=game.CARDS)
    rec.ok("jokers", jokers={"hint": 1, "snipe": 1})
    rec.ok("jokers", jokers={"category": None, "easier": 0})
    rec.fail("budget_unknown_joker", "jokers", jokers={"comodin": 1})
    rec.fail("budget_unknown_joker", "jokers", jokers=["hint"])
    rec.fail("budget_unknown_joker", "jokers")
    for bad in (100, -1, True, "2", 1.5):
        rec.fail("budget_invalid", "jokers", jokers={"hint": bad})
    rec.ok("pick", index=rec.find(lambda q: len(q["hints"]) >= 2))
    assert rec.jokers()["easier"]["reason"]["code"] == "joker_spent"
    rec.fail("joker_spent", "joker", joker="easier")
    rec.ok("joker", joker="hint")
    assert rec.jokers()["hint"]["reason"]["code"] == "joker_spent"
    rec.fail("joker_spent", "joker", joker="hint")
    rec.ok("joker", joker="snipe", index=rec.wrong())
    rec.fail("joker_spent", "joker", joker="snipe", index=rec.wrong())
    rec.ok("answer", index=rec.correct())
    rec.ok("pick", index=rec.find(lambda q: q["hints"]))
    assert rec.view()["jokers_left"]["hint"] == 0
    rec.fail("joker_spent", "joker", joker="hint")
    rec.ok("jokers", jokers={"hint": 2, "easier": None})
    rec.ok("joker", joker="hint")
    rec.ok("jokers", jokers={"hint": None})
    rec.ok("answer", index=rec.correct())


# Game scenarios: players, admin and errors (plan 18, "Scenarios") --------------------------------

def db(rec):
    return rec.steps[-1]["db"]


@scenario("admin-skip", "Admin skip for the player and for everyone (the burn shows in a second player's supply); "
          "skip outside a question; skip with no replacement on the tight pool.", 9)
def admin_skip(rec):
    rec.ok("new", player="Ana")
    rec.fail("skip_not_question", "skip")
    rec.ok("pick", index=0)
    rec.ok("skip")
    rec.ok("pick", index=1)
    rec.ok("get_game", player="Bea")
    rec.ok("skip", everyone=True)
    assert [b["player_id"] for b in db(rec)["burned"]] == [1, None]
    rec.ok("get_game", player="Bea")
    rec.ok("get_game", player="Ana")
    rec.level_up()
    rec.ok("new", player="Bea")
    rec.use("tight")
    rec.ok("new", player="Carla")
    rec.ok("pick", index=0)
    rec.fail("refill_empty", "skip")
    rec.fail("refill_empty", "skip", everyone=True)
    rec.ok("answer", index=rec.correct())


@scenario("players", "Several players with their own burns; players() order; name cleanup and casefold "
          "(«Íngrid»/«íngrid», «Straße»/«STRASSE»); bad names; deleting players (with a running game, "
          "unknown, by another case); IDs after a delete.", 10)
def players_(rec):
    rec.ok("players")
    rec.ok("get_game")
    rec.ok("new", player="  Ana   María ")
    rec.level_up()
    rec.level_up()
    rec.ok("new", player="Íngrid")
    rec.level_up()
    rec.ok("new", player="íngrid")
    rec.ok("new", player="Straße")
    rec.ok("new", player="STRASSE")
    assert [p["name"] for p in db(rec)["players"]] == ["Ana María", "Íngrid", "Straße"]
    rec.ok("players")
    for bad in ("", "   ", None, 7 * " "):
        rec.fail("name_missing", "new", player=bad)
    rec.fail("name_missing", "new")
    rec.fail("name_too_long", "new", player="x" * 31)
    rec.fail("name_too_long", "get_game", status=400, player="x" * 31)
    rec.ok("new", player="Abcdefghij Klmnopqrst Uvwxyzab")  # 30 letters with spaces
    rec.ok("new", player=7)
    rec.ok("get_game", player="ana maría")
    rec.ok("get_game", player="ÍNGRID")
    rec.ok("new", player="Bea")
    rec.ok("pick", index=0)
    rec.ok("skip", everyone=True)
    rec.level_up()
    rec.ok("players")
    rec.ok("delete_player", name="BEA")
    assert len(db(rec)["players"]) == 5 and db(rec)["games"][-1]["id"] == 7
    assert [b["player_id"] for b in db(rec)["burned"] if b["game_id"] == 8] == [None]
    rec.ok("get_game")
    rec.ok("new", player="Carla")
    assert db(rec)["players"][-1]["id"] == 6 and db(rec)["games"][-1]["id"] == 8
    rec.fail("player_unknown", "delete_player", name="Zoe")
    rec.fail("name_missing", "delete_player", name="  ")
    rec.fail("name_missing", "delete_player")
    rec.ok("delete_player", name="ana maría")
    rec.ok("new", player="Dani")
    assert [p["id"] for p in db(rec)["players"]] == [2, 3, 4, 5, 6, 7]
    rec.ok("delete_player", name="íngrid")
    rec.ok("players")
    rec.ok("get_game", player="Íngrid")


@scenario("abandon", "Every action on an empty DB; abandon; every action with no running game; "
          "a new game while one runs abandons it; undo after abandon.", 11)
def abandon(rec):
    def no_game():
        rec.fail("no_game", "pick", index=0)
        rec.fail("no_game", "answer", index=0)
        rec.fail("no_game", "skip")
        rec.fail("no_game", "skip", everyone=True)
        rec.fail("no_game", "jokers", jokers={"hint": 1})
        rec.fail("no_game", "joker", joker="hint")
        rec.fail("joker_unknown", "joker", joker="comodin")
        rec.fail("nothing_to_undo", "undo")
        rec.ok("abandon")
    rec.ok("get_game")
    no_game()
    rec.ok("new", player="Ana")
    rec.level_up()
    rec.ok("pick", index=0)
    rec.ok("abandon")
    assert db(rec)["games"][-1]["result"] == "abandoned"
    no_game()
    rec.ok("get_game", player="Ana")
    rec.ok("new", player="Ana")
    rec.level_up()
    rec.ok("new", player="Bea")
    assert [g["result"] for g in db(rec)["games"]] == ["abandoned", "abandoned", None]
    rec.fail("nothing_to_undo", "undo")
    rec.ok("pick", index=0)
    rec.ok("answer", index=rec.wrong())
    rec.fail("no_game", "pick", index=0)
    rec.ok("abandon")
    rec.ok("undo")
    rec.ok("answer", index=rec.correct())


@scenario("supply", "Tight pool: a second game for the same player fails with the supply report; a new player "
          "can still play; get_game's supply for a known, a new and no player.", 12, pool="tight")
def supply_(rec):
    rec.ok("get_game")
    rec.ok("new", player="Ana")
    rec.level_up()
    rec.ok("get_game", player="Ana")
    rec.ok("get_game", player="Bea")
    rec.ok("get_game")
    body = rec.fail("supply_short", "new", player="ana")
    assert body["supply"] and not body["supply"]["ok"]
    assert db(rec)["games"][-1]["result"] is None
    rec.ok("new", player="Bea")
    rec.ok("get_game", player="Carla")
    rec.ok("players")


@scenario("errors", "Bad picks and answers: out of range, wrong phase, a struck answer; jokers in the select "
          "phase; an unknown joker.", 13)
def errors(rec):
    rec.ok("new", player="Ana")
    rec.fail("no_question", "answer", index=0)
    rec.fail("joker_not_question", "joker", joker="hint")
    rec.fail("joker_unknown", "joker", joker="comodin")
    rec.fail("card_invalid", "pick", index=4)
    rec.fail("card_invalid", "pick", index=-1)
    rec.fail("card_invalid", "pick")
    rec.ok("pick", index=3)
    rec.fail("no_cards", "pick", index=0)
    rec.fail("joker_unknown", "joker", joker="comodin")
    rec.fail("joker_unknown", "joker")
    rec.fail("answer_invalid", "answer", index=4)
    rec.fail("answer_invalid", "answer", index=-1)
    rec.fail("answer_invalid", "answer")
    rec.ok("joker", joker="snipe", index=rec.wrong())
    rec.fail("answer_invalid", "answer", index=rec.state()["struck"][0])
    rec.ok("answer", index=rec.correct())
    rec.fail("no_question", "answer", index=0)
    rec.ok("pick", index=0)
    rec.ok("answer", index=rec.wrong())
    rec.fail("no_game", "answer", index=0)
    rec.fail("no_game", "joker", joker="hint")


def dumps(obj):
    """Deterministic JSON: sorted keys, one list item (step, question, case) per line."""
    one = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)
    lines = lambda xs: "[\n" + ",\n".join(one(x) for x in xs) + "\n]"
    if isinstance(obj, list):
        return lines(obj) + "\n"
    return "{\n" + ",\n".join(f"{one(k)}: {lines(v) if isinstance(v, list) and v else one(v)}"
                              for k, v in sorted(obj.items())) + "\n}\n"


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(obj), encoding="utf-8")


def record(out):
    """Write every fixture into `out`."""
    if CATEGORIES:
        write(out / "categories.json", CATEGORIES)
    for name, questions in POOLS.items():
        write(out / "pools" / f"{name}.json", {"questions": questions})
    write(out / "selection.json", selection_cases())
    for name, (about, seed, pool, fn) in SCENARIOS.items():
        rec = Recorder(seed, pool)
        with rec.patched():
            fn(rec)
        write(out / "game" / f"{name}.json",
              {"name": name, "about": about, "seed": seed, "pool": pool, "steps": rec.steps})


def json_files(root):
    return {p.relative_to(root) for p in root.rglob("*.json")} if root.exists() else set()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="re-record into a temp dir and diff against the fixtures")
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        new = Path(tmp)
        record(new)
        if args.check:
            old_files, new_files = json_files(FIXTURES), json_files(new)
            diff = sorted(old_files ^ new_files) + sorted(
                f for f in old_files & new_files if (FIXTURES / f).read_bytes() != (new / f).read_bytes())
            for f in diff:
                print(f"differs: {f}")
            return 1 if diff else 0
        for f in json_files(FIXTURES):
            (FIXTURES / f).unlink()
        for f in json_files(new):
            (FIXTURES / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(new / f, FIXTURES / f)
        print(f"wrote {len(json_files(new))} fixtures to {FIXTURES.relative_to(layout.REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
