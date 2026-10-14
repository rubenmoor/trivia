"""Played data from opt-in telemetry (plan 109): `qgen telemetry --pull` folds the report server's
sessions into anonymous counts in state/played/stats.json, then acks them.

No raw session, install id or session id stays on disk (decision 121): only `pending_ack`, the ids
of a folded page until its ack goes through, so a crash between write and ack never counts twice.
"""
import json

import atomic
import layout  # noqa: F401  (makes app/server importable)
import paths  # app/server/paths.py: state/

STATS = paths.STATE / "played" / "stats.json"
PAGE = 200  # the server's GET /telemetry and ack maximum
HELP_JOKERS = {"hint", "snipe"}  # show hints / strike answers; easier, category only pick the question
LENGTH_MIN = [5, 15, 30, 60, 120, 240]  # session length buckets, minutes


def empty():
    return {"version": 1, "answers": {}, "levels": {},
            "games": {"results": {}, "reached": {}, "jokers": {}, "customized": {}, "mods": {}},
            "sessions": {}, "pending_ack": [], "unknown": 0}


def load():
    if not STATS.exists():
        return empty()
    stats = json.loads(STATS.read_text(encoding="utf-8"))
    if stats.get("version") != 1:
        raise SystemExit(f"{STATS}: unknown version {stats.get('version')}")
    return stats


def save(stats):
    atomic.write_json(STATS, stats)


def _add(d, key, right=None):
    """right None: a count; else an [n, right] pair."""
    if right is None:
        d[key] = d.get(key, 0) + 1
    else:
        n, r = d.get(key, [0, 0])
        d[key] = [n + 1, r + right]


def length_bucket(seconds):
    m = seconds / 60
    lo = 0
    for hi in LENGTH_MIN:
        if m < hi:
            return f"{lo}-{hi}"
        lo = hi
    return f"{lo}+"


def fold(stats, sessions, known):
    """Add sessions (GET /telemetry rows) to stats in place; known: the pool's ids. → counts."""
    n = {"sessions": 0, "games": 0, "answers": 0, "unknown": 0}
    g = stats["games"]
    for s in sessions:
        day = s["received_day"]
        n["sessions"] += 1
        sess = stats["sessions"].setdefault(f"{s['version']}|{day}", {"n": 0, "games": {}, "length": {}})
        sess["n"] += 1
        _add(sess["games"], str(len(s["games"])))
        _add(sess["length"], length_bucket(s["length_s"]))
        for game in s["games"]:
            n["games"] += 1
            group, mode = game["age_group"] or "custom", game["mode"]
            _add(g["results"], f"{day}|{s['version']}|{mode}|{group}|{game['result']}")
            _add(g["reached"], f"{day}|{group}|{game['reached']}")
            for joker, uses in game["jokers"].items():
                if uses:
                    g["jokers"][f"{day}|{joker}"] = g["jokers"].get(f"{day}|{joker}", 0) + uses
            if game["customized"]:
                _add(g["customized"], day)
            if game["mods"]:
                _add(g["mods"], day)
            for a in game["answers"]:
                right = int(a["correct"])
                _add(stats["levels"], f"{group}|{a['level']}|{mode}|{day}", right)
                if a["question"] not in known:
                    stats["unknown"] += 1
                    n["unknown"] += 1
                    continue
                clean = int(not any(a["jokers"].get(j) for j in HELP_JOKERS))
                _add(stats["answers"], f"{a['question']}|{game['locale']}|{group}|{mode}|{day}|{clean}", right)
                n["answers"] += 1
    return n


def pull(api, known, dry_run=False):
    """The pull loop (plan 109); api(path, body=None) → JSON, exits on failure. → counts."""
    stats = load()
    n = {"sessions": 0, "games": 0, "answers": 0, "unknown": 0, "pages": 0, "acked": 0}
    if stats["pending_ack"] and not dry_run:  # left by a crash after the write: already counted
        n["acked"] += ack(api, stats)
    while True:
        page = api(f"/telemetry?limit={PAGE}")
        n["pages"] += 1
        for k, v in fold(stats, page["sessions"], known).items():
            n[k] += v
        if dry_run or not page["sessions"]:
            n["more"] = page["more"]
            return n
        stats["pending_ack"] = [s["session"] for s in page["sessions"]]
        save(stats)
        n["acked"] += ack(api, stats)
        if not page["more"]:
            return n


def ack(api, stats):
    """Ack pending_ack, then clear it on disk. → acked on the server."""
    ids, acked = stats["pending_ack"], 0
    for i in range(0, len(ids), PAGE):
        acked += api("/telemetry/ack", {"sessions": ids[i:i + PAGE]})["acked"]
    stats["pending_ack"] = []
    save(stats)
    return acked
