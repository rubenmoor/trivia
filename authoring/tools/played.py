"""Played data from opt-in telemetry (plan 109): `qgen telemetry --pull` folds the report server's
sessions into anonymous counts in state/played/stats.json, then acks them.

No raw session, install id or session id stays on disk (decision 121): only `pending_ack`, the ids
of a folded page until its ack goes through, so a crash between write and ack never counts twice.

`qgen report --played` (decision 122): per age group a monotone curve right rate ← rated difficulty
from clean answers, inverted per question after shrinkage; outliers are review candidates only.
"""
import json, math

import atomic
import layout
import paths  # authoring/tools/paths.py: state/
import translations

STATS = paths.STATE / "played" / "stats.json"
PAGE = 200  # the server's TELEMETRY_PAGE (GET /telemetry and ack maximum)
HELP_JOKERS = {"hint", "snipe"}  # show hints / strike answers; easier, category only pick the question
LENGTH_MIN = [5, 15, 30, 60, 120, 240]  # session length buckets, minutes
MIN_N = 20  # clean answers in a cell before it can be an outlier
BUCKET_MIN = 30  # clean answers per curve bucket, else merged into a neighbour
GROUP_MIN = 300  # clean answers per group before it gets a curve
SHRINK = 8  # pseudo-answers at the curve's rate
DELTA = 2  # |observed − rated| of an outlier
Z = 3.29  # 99.9 % Wilson interval: thousands of cells, few false candidates


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


def _add_level(d, key, right, rated):
    """[n, right, Σ rated difficulty, n with one]; rated None: an unknown id."""
    n, r, ds, dn = (d.get(key, []) + [0, 0, 0, 0])[:4]
    d[key] = [n + 1, r + right, ds + (rated or 0), dn + (rated is not None)]


def rated():
    """{locale: {id: (difficulty, reviewed_on)}}: es from the source pool, the others their own (D-81)."""
    def entry(q):
        return q["difficulty"], (q.get("review") or {}).get("reviewed_on")
    out = {"es": {q["id"]: entry(q) for q in json.loads(layout.SOURCE_POOL.read_text(encoding="utf-8"))["questions"]}}
    for l in translations.LOCALES:
        out[l] = {t["id"]: entry(t) for t in translations.load(l)["questions"] if t.get("difficulty") is not None}
    return out


def length_bucket(seconds):
    m = seconds / 60
    lo = 0
    for hi in LENGTH_MIN:
        if m < hi:
            return f"{lo}-{hi}"
        lo = hi
    return f"{lo}+"


def fold(stats, sessions, known):
    """Add sessions (GET /telemetry rows) to stats in place; known: rated(). → counts."""
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
            _add(g["reached"], f"{day}|{group}|{mode}|{game['reached']}|{game['result']}")
            for joker, uses in game["jokers"].items():
                if uses:
                    g["jokers"][f"{day}|{joker}"] = g["jokers"].get(f"{day}|{joker}", 0) + uses
            if game["customized"]:
                _add(g["customized"], day)
            if game["mods"]:
                _add(g["mods"], day)
            for a in game["answers"]:
                right = int(a["correct"])
                e = known.get(game["locale"], {}).get(a["question"]) or known["es"].get(a["question"])
                _add_level(stats["levels"], f"{group}|{a['level']}|{mode}|{day}", right, e[0] if e else None)
                if a["question"] not in known["es"]:
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


# --- calibration and the report (decision 122) ---------------------------------

def curve(buckets):
    """{d: [n, right]} → [(x, p, n)], p strictly decreasing in x; None below GROUP_MIN.
    Buckets < BUCKET_MIN merge into their smaller neighbour, then pool-adjacent-violators."""
    bs = [[d, n, r] for d, (n, r) in sorted(buckets.items()) if n]
    if sum(b[1] for b in bs) < GROUP_MIN:
        return None
    while len(bs) > 1:
        i = min(range(len(bs)), key=lambda i: bs[i][1])
        if bs[i][1] >= BUCKET_MIN:
            break
        j = i - 1 if i == len(bs) - 1 or (i > 0 and bs[i - 1][1] <= bs[i + 1][1]) else i + 1
        a, b = sorted((i, j))
        x, y = bs[a], bs[b]
        bs[a:b + 1] = [[(x[0] * x[1] + y[0] * y[1]) / (x[1] + y[1]), x[1] + y[1], x[2] + y[2]]]
    blocks = []  # [Σ x·n, n, right]
    for x, n, r in bs:
        blocks.append([x * n, n, r])
        while len(blocks) > 1 and blocks[-2][2] / blocks[-2][1] <= blocks[-1][2] / blocks[-1][1]:
            sx, n2, r2 = blocks.pop()
            blocks[-1] = [blocks[-1][0] + sx, blocks[-1][1] + n2, blocks[-1][2] + r2]
    return [(sx / n, r / n, n) for sx, n, r in blocks]


def rate_at(c, d):
    """p_g(d): linear between the points, flat beyond."""
    if d <= c[0][0]:
        return c[0][1]
    for (x0, p0, _), (x1, p1, _) in zip(c, c[1:]):
        if d <= x1:
            return p0 + (p1 - p0) * (d - x0) / (x1 - x0)
    return c[-1][1]


def difficulty_at(c, r):
    """(d, bound) with p_g(d) = r; bound "≤" / "≥" beyond the curve's ends, else None."""
    if r > c[0][1]:
        return round(c[0][0], 1), "≤"
    if r < c[-1][1]:
        return round(c[-1][0], 1), "≥"
    for (x0, p0, _), (x1, p1, _) in zip(c, c[1:]):
        if p1 <= r <= p0:
            return round(x0 + (x1 - x0) * (p0 - r) / (p0 - p1), 1), None
    return round(c[0][0], 1), None  # one point, r on it


def wilson(right, n, z=Z):
    p, zz = right / n, z * z
    mid, half = (p + zz / (2 * n)) / (1 + zz / n), z * math.sqrt(p * (1 - p) / n + zz / (4 * n * n)) / (1 + zz / n)
    return mid - half, mid + half


def analyse(stats, known, groups, mode=None, since=None, locales=None, group_ids=None):
    """Curves per group and cells per (id, locale, group) from clean answers on/after the entry's
    last review; groups: age-groups.json's. → {"curves", "cells", "outliers": {too_easy, too_hard, mixed}}."""
    win = {g["id"]: g["window"] for g in groups if not group_ids or g["id"] in group_ids}
    cells = {}
    for k, (n, r) in stats["answers"].items():
        qid, loc, g, m, day, clean = k.split("|")
        e = known.get(loc, {}).get(qid)
        if clean != "1" or g not in win or not e or (mode and m != mode) or day < max(since or "", e[1] or ""):
            continue
        c = cells.setdefault((qid, loc, g), [0, 0])
        c[0] += n
        c[1] += r
    curves = {}
    for g, (lo, hi) in win.items():
        buckets = {}
        for (qid, loc, gg), (n, r) in cells.items():
            d = known[loc][qid][0]
            if gg == g and lo <= d <= hi:
                b = buckets.setdefault(d, [0, 0])
                b[0] += n
                b[1] += r
        curves[g] = {"n": sum(b[0] for b in buckets.values()), "window": [lo, hi], "points": curve(buckets)}
    out = []
    for (qid, loc, g), (n, r) in sorted(cells.items()):
        if locales and loc not in locales:
            continue
        d, c = known[loc][qid][0], curves[g]["points"]
        cell = {"id": qid, "locale": loc, "group": g, "n": n, "right": r, "rated": d,
                "observed": None, "bound": None, "delta": None, "outlier": None}
        if c:
            p = rate_at(c, d)
            obs, bound = difficulty_at(c, (r + SHRINK * p) / (n + SHRINK))
            delta = obs - d
            if bound:  # only a one-sided bound: no direction against it
                delta = min(delta, 0) if bound == "≤" else max(delta, 0)
            lo_w, hi_w = wilson(r, n)
            cell.update(observed=obs, bound=bound, delta=round(delta, 1))
            if n >= MIN_N and abs(delta) >= DELTA and not lo_w <= p <= hi_w:
                cell["outlier"] = "too_easy" if delta < 0 else "too_hard"
        out.append(cell)
    dirs = {}
    for c in out:
        if c["outlier"]:
            dirs.setdefault((c["id"], c["locale"]), set()).add(c["outlier"])
    outliers = {"too_easy": [], "too_hard": [], "mixed": []}
    for c in out:
        if c["outlier"]:
            outliers["mixed" if len(dirs[(c["id"], c["locale"])]) > 1 else c["outlier"]].append(c)
    for v in outliers.values():
        v.sort(key=lambda c: -abs(c["delta"]))
    return {"curves": curves, "cells": out, "outliers": outliers}


def review_data(locale=None):
    """For /review (task 893): {"outliers": [(id, locale, |Δ|)] by |Δ| (one per entry, mixed left out),
    "played": {(id, locale): [{group, n, right, rated, observed, bound}]}}; None without played data."""
    if not STATS.exists():
        return None
    groups = json.loads(layout.AGE_GROUPS.read_text(encoding="utf-8"))["groups"]
    a = analyse(load(), rated(), groups, locales=[locale] if locale else None)
    best = {}
    for c in a["outliers"]["too_easy"] + a["outliers"]["too_hard"]:
        k = (c["id"], c["locale"])
        best[k] = max(best.get(k, 0), abs(c["delta"]))
    played = {}
    for c in a["cells"]:
        played.setdefault((c["id"], c["locale"]), []).append(
            {k: c[k] for k in ("group", "n", "right", "rated", "observed", "bound")})
    return {"outliers": sorted(((i, l, d) for (i, l), d in best.items()), key=lambda o: -o[2]), "played": played}
