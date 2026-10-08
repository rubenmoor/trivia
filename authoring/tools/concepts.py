"""Concept lists and question axes (plans/20-pipeline-efficiency.md part 2, D-37). Never ships (D-35).

A subcategory's concept list lives in authoring/data/concepts/<slug>.json: its facets, its fit for
the question axes, and its concepts (name, facet, familiarity, maybe `retired`). How often a concept
was used is counted from the pool, never stored. Drawing is plain code: concepts with fewer
questions first, axis values that are rarely used first.
"""
import json, re, unicodedata
from collections import Counter

from layout import AXES_FILE, CONCEPTS

AXES = ["move", "stimulus", "clue", "answer_kind", "lens"]
FIT_AXES = ["move", "stimulus", "lens"]  # scored per subcategory (PE-9)
DRAW_ORDER = ["stimulus", "move", "answer_kind", "clue", "lens"]  # media first: its rules are the tightest
LOW_STOCK = 30  # a list with fewer unused concepts gets a top-up
OPTIONS = 3  # axis combinations offered per slot
OFFERED_FACTOR = 0.3  # weight of a value an earlier slot of the subcategory already offered


def _slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def key(name):
    """Normalized concept name: what has to be unique across subcategories (OQ-40)."""
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    words = [w for w in re.sub(r"[^a-z0-9 ]+", " ", text).split()
             if w not in {"el", "la", "los", "las", "un", "una", "de", "del"}]
    return " ".join(words)


# --- axes ---------------------------------------------------------------------

def load_axes():
    return json.loads(AXES_FILE.read_text(encoding="utf-8"))


def values(axes_def, axis):
    return list(axes_def["axes"][axis]["values"])


def broken_rules(combo, rules):
    """Rules a (possibly partial) combination breaks. A rule counts once all its `if` axes are set."""
    out = []
    for r in rules:
        if any(a not in combo for a in r["if"]) or any(combo[a] not in vs for a, vs in r["if"].items()):
            continue
        if any(a in combo and combo[a] not in vs for a, vs in r["then"].items()):
            out.append(r)
    return out


def axes_problems(axes_value, axes_def):
    """(errors, warnings) for a question's `axes`: unknown values are errors; broken rules only
    warnings, since older questions were tagged after the fact (OQ-39)."""
    if not isinstance(axes_value, dict) or sorted(axes_value) != sorted(AXES):
        return [f"axes must have exactly {', '.join(AXES)}"], []
    errors = [f"axes.{a}: unknown value {axes_value[a]!r}" for a in AXES if axes_value[a] not in values(axes_def, a)]
    if errors:
        return errors, []
    return [], [f"axes break a rule: {json.dumps(r, ensure_ascii=False)}" for r in broken_rules(axes_value, axes_def["rules"])]


def axes_text(axes_def, only=None):
    """The axes and their values as prompt text; `only` limits it to {axis: values used}."""
    lines = []
    for a in AXES:
        ax = axes_def["axes"][a]
        lines.append(f"### {a}: {ax['label']}")
        lines += [f"- `{v}`: {why}" for v, why in ax["values"].items() if only is None or v in only.get(a, ())]
    return "\n".join(lines)


# --- concept lists --------------------------------------------------------------

def path(sub):
    return CONCEPTS / f"{_slug(sub)}.json"


def load(sub):
    p = path(sub)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def save(sub, data):
    p = path(sub)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


def uses(pool_questions, sub):
    """Questions per concept name in this subcategory, all statuses (they all count as asked)."""
    return Counter(q["concept"] for q in pool_questions if q.get("subcategory") == sub and q.get("concept"))


def unused(lst, used):
    return [c for c in lst["concepts"] if not c.get("retired") and not used.get(c["name"])]


def familiarity_target(difficulty):
    """Difficulty 1 → familiarity 5 (every kid knows it), difficulty 10 → 1."""
    return 5 - (difficulty - 1) * 4 / 9


def draw_concepts(lst, used, difficulties, rng):
    """One concept per target difficulty, all different. Fewer questions first (1 / (1 + uses)²),
    familiarity close to the difficulty preferred; retired concepts never."""
    picked, out = set(), []
    for d in difficulties:
        pool = [c for c in lst["concepts"] if not c.get("retired") and c["name"] not in picked]
        if not pool:
            break
        weights = [1 / (1 + used.get(c["name"], 0)) ** 2 / (1 + abs(c["familiarity"] - familiarity_target(d)))
                   for c in pool]
        c = rng.choices(pool, weights)[0]
        picked.add(c["name"])
        out.append(c)
    return out


def axis_usage(pool_questions, sub):
    """How the tagged questions use each value: {"sub": (Counters, n), "pool": (Counters, n)}."""
    tagged = [q for q in pool_questions if q.get("axes")]
    mine = [q for q in tagged if q.get("subcategory") == sub]
    return {scope: ({a: Counter(q["axes"][a] for q in qs) for a in AXES}, len(qs))
            for scope, qs in (("sub", mine), ("pool", tagged))}


def base_weight(axes_def, axis, v):
    return axes_def.get("weights", {}).get(axis, {}).get(v, 1)


def value_weight(axes_def, axis, v, fit, usage, offered):
    """Base weight × fit (move, stimulus, lens) × a factor per scope that drops when the value is
    used more than its expected share (base weight / sum of base weights): 1 / (1 + used / expected).
    A value already offered to an earlier slot of the subcategory counts OFFERED_FACTOR as much."""
    w = base_weight(axes_def, axis, v) * (fit.get(axis, {}).get(v, 3) if axis in FIT_AXES else 1)
    expected = base_weight(axes_def, axis, v) / sum(base_weight(axes_def, axis, x) for x in values(axes_def, axis))
    for counts, n in usage.values():
        if n:
            w /= 1 + counts[axis][v] / (expected * n)
    return w * (OFFERED_FACTOR if v in offered[axis] else 1)


def possible_combos(axes_def, fit):
    """Every compatible combination whose values all fit the subcategory (fit 3 or more)."""
    allowed = {a: [v for v in values(axes_def, a)
                   if a not in FIT_AXES or fit.get(a, {}).get(v, 3) > 2] for a in DRAW_ORDER}
    out = []

    def walk(combo, rest):
        if not rest:
            out.append(dict(combo))
            return
        for v in allowed[rest[0]]:
            combo[rest[0]] = v
            if not broken_rules(combo, axes_def["rules"]):
                walk(combo, rest[1:])
            del combo[rest[0]]

    walk({}, DRAW_ORDER)
    return out


def draw_combos(axes_def, fit, usage, offered, rng, k=OPTIONS, tries=50, possible=None):
    """Up to k different, compatible axis combinations. One value per axis in DRAW_ORDER, each
    weighted on its own, among the values that still lead to a possible combination (so a media
    stimulus isn't outnumbered by the many text-only combinations). `offered` ({axis: set}) is
    updated so later slots of the same subcategory prefer other values."""
    possible = possible_combos(axes_def, fit) if possible is None else possible
    combos = []
    for _ in range(tries):
        if len(combos) == k or not possible:
            break
        left, combo = possible, {}
        for a in DRAW_ORDER:
            ok = sorted({c[a] for c in left}, key=values(axes_def, a).index)
            combo[a] = rng.choices(ok, [value_weight(axes_def, a, v, fit, usage, offered) for v in ok])[0]
            left = [c for c in left if c[a] == combo[a]]
        if combo not in combos:
            combos.append({a: combo[a] for a in AXES})
    for c in combos:
        for a in AXES:
            offered[a].add(c[a])
    return combos
