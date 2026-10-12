#!/usr/bin/env python3
"""Parity fixtures for the TypeScript engine (plan 18, PORT-1): scripted games through the
untouched Python referee (app/server/game.py, selection.py), recorded as JSON.

    python3 authoring/tools/record_fixtures.py            write app/client/src/engine/fixtures/
    python3 authoring/tools/record_fixtures.py --check    re-record into a temp dir and diff; exit 1 on a difference

Never touches state/: the game state lives in a temp dir, set before the game modules load.
Randomness is a tape: every `random.shuffle` is recorded as {"site", "n", "perm"} (perm[j] = old
index of the element now at j). Every step has a fixed `now`. Categories and pools are synthetic.
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
        self.pool = POOLS[pool]
        self.steps, self.tape, self.now = [], [], None

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
        self.steps.append({"now": self.now, "call": call, "args": args, "tape": self.tape,
                           "response": {"status": status, "body": body}, "db": snapshot()})
        return body


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
