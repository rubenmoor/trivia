"""Question selection per level (plans/03-game-flow.md, GF-2, GF-5, D-22, D-25).

Each of the 12 levels offers 4 questions from its difficulty range. An exact bipartite
matching (augmenting paths) decides whether the levels can be filled from a set of questions.
"""
import random
import sqlite3

from paths import STATE

STATE_DB = STATE / "game.sqlite"  # gitignored (D-25)

LEVELS = 12
PER_LEVEL = 4
LEVEL_RANGES = {1: (1, 1), 2: (2, 3), 3: (3, 5), 4: (4, 6), 5: (4, 6), 6: (4, 6),
                7: (5, 7), 8: (6, 8), 9: (6, 9), 10: (7, 10), 11: (8, 10), 12: (9, 10)}


def in_range(q, level):
    lo, hi = LEVEL_RANGES[level]
    return lo <= q["difficulty"] <= hi


def burned_for(con, player_id):
    """Question IDs burned for this player or for everyone (D-28); player_id None: only the global burns."""
    rows = con.execute("SELECT question_id FROM burned WHERE player_id IS NULL OR player_id = ?", (player_id,))
    return {row[0] for row in rows}


def player_id(con, name):
    """The ID of a known player, or None. Names ignore case, also in «Í»/«í» (SQLite's NOCASE is ASCII only)."""
    key = name.casefold()
    return next((pid for pid, n in con.execute("SELECT id, name FROM players") if n.casefold() == key), None)


def burned_ids(player=None, db=STATE_DB):
    """Burned question IDs for `player` (a name; None: a new player, so only the global burns).

    Empty if no game was ever played. Raises KeyError for an unknown player name.
    """
    if not db.is_file():
        if player:
            raise KeyError(player)
        return set()
    with sqlite3.connect(db) as con:
        try:
            pid = player_id(con, player) if player else None
            if player and pid is None:
                raise KeyError(player)
            return burned_for(con, pid)
        except sqlite3.OperationalError:  # state from before D-28 (the server migrates it on start)
            if player:
                raise KeyError(player)
            try:  # back then every burn counted for everyone
                return {row[0] for row in con.execute("SELECT question_id FROM burned")}
            except sqlite3.OperationalError:
                return set()


def available(pool, burned, exclude=()):
    """Questions that can be offered: approved, not burned, not in `exclude`."""
    skip = set(burned) | set(exclude)
    return [q for q in pool if q["status"] == "approved" and q["id"] not in skip]


def assign(questions, levels):
    """Fill PER_LEVEL slots per level with distinct questions from the level's range.

    Returns (assignment {level: [ids]}, missing {level: n}); `missing` is empty when every
    slot is filled. Narrow ranges go first, so shortages show up where they really are.
    """
    levels = sorted(levels, key=lambda l: (LEVEL_RANGES[l][1] - LEVEL_RANGES[l][0], l))
    slots = [l for l in levels for _ in range(PER_LEVEL)]
    cands = {l: [q["id"] for q in questions if in_range(q, l)] for l in levels}
    owner = {}  # question id -> slot index

    def augment(i, seen):
        for qid in cands[slots[i]]:
            if qid not in seen:
                seen.add(qid)
                if qid not in owner or augment(owner[qid], seen):
                    owner[qid] = i
                    return True
        return False

    missing = {}
    for i, level in enumerate(slots):
        if not augment(i, set()):
            missing[level] = missing.get(level, 0) + 1
    assignment = {l: [] for l in levels}
    for qid, i in owner.items():
        assignment[slots[i]].append(qid)
    return assignment, missing


def draw(level, questions, n=PER_LEVEL, keep=(), avoid_categories=(), category_of=None, rng=random):
    """Draw n questions for `level` from `questions` (already filtered by `available`).

    `keep`: questions already on the table at this level (a skip replaces one card).
    Prefers broad categories that are neither on the table nor in `avoid_categories`, and
    takes a candidate only if all later levels can still be filled without it.
    Returns the drawn questions, or None if the level can't be filled.
    """
    category_of = category_of or (lambda q: q.get("subcategory"))
    later = range(level + 1, LEVELS + 1)
    taken = {q["id"] for q in keep}
    cands = [q for q in questions if in_range(q, level) and q["id"] not in taken]
    rng.shuffle(cands)
    picked = []
    for _ in range(n):
        table = {category_of(q) for q in [*keep, *picked]}
        cands.sort(key=lambda q: (category_of(q) in table, category_of(q) in avoid_categories))
        for q in cands:
            if q in picked:
                continue
            gone = taken | {p["id"] for p in picked} | {q["id"]}
            if not assign([x for x in questions if x["id"] not in gone], later)[1]:
                picked.append(q)
                break
        else:
            return None
    return picked


def supply(questions):
    """Per-level supply for the supply check (GF-5): candidates and shortages per level."""
    _, missing = assign(questions, range(1, LEVELS + 1))
    return [{"level": l, "range": list(LEVEL_RANGES[l]),
             "candidates": sum(in_range(q, l) for q in questions),
             "missing": missing.get(l, 0)} for l in range(1, LEVELS + 1)]
