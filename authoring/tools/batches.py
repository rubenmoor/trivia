"""What the next `qgen batch` does (D-36): shared by qgen.py and the authoring start page (RV-12)."""
import json, math

from layout import WORK
import categories  # authoring/tools/categories.py: app/data/categories.json (D-19)
import concepts  # authoring/tools/concepts.py: concept lists (D-37)
import targets  # authoring/tools/targets.py: pool targets (D-53)

MODES = {"batch": "qgen batch", "media-first": "qgen batch --media-first"}  # run.json mode → the command that finishes it (decision 646)
SHARE = 0.5  # per batch: this share of the bundle's subcategories, those with the fewest approved questions (D-46)
# a bundle's first draft run (plan 232): ≈ 50 approved at the 0.62 approved per slot of first en runs (batch-9, 26, 27, 29)
PILOT_SUBCATEGORIES, PILOT_SLOTS = 27, 3


def unfinished_runs():
    """Names of `qgen batch` and `qgen batch --media-first` runs in work/ that haven't finished, sorted."""
    out = []
    for p in WORK.glob("*/run.json"):
        run = json.loads(p.read_text(encoding="utf-8")) or {}
        if run.get("mode") in MODES and not run.get("done"):
            out.append(p.parent.name)
    return sorted(out)


def pilot(pool, bundle):
    """The bundle has no drafted source yet (copies don't count): its next `qgen batch` is a pilot (plan 232)."""
    return not any(q.get("bundle") == bundle and not q.get("copied_from") for q in pool)


def top_up(pool, bundle, locale="en"):
    """{subcategory: [slot specs]} of a top-up run (decision 831), {} without "minimums" or once they and the draft
    gaps are met. Per subcategory short of a band: one slot per missing question, its level inside every short band
    it can fill (the largest draft gap, then the lowest), `difficulty_range` = the band. The draft gaps (D-54) left
    after those: one slot per question, scarce levels first, each to the subcategory with the most unused concepts
    within ±1 per slot it already has (ties: `subcategories` order)."""
    if not targets.load_minimums(bundle):
        return {}
    gaps = dict(targets.draft_gaps(pool, bundle) or {})
    out = {}
    for s, short in targets.minimum_gaps(pool, bundle, locale).items():
        short = dict(short)
        while short:
            fits = lambda lvl: [b for b in short if b[0] <= lvl <= b[1]]
            lvl = min({l for lo, hi in short for l in range(lo, hi + 1)},
                      key=lambda l: (-len(fits(l)), -gaps.get(l, 0), l))
            b = fits(lvl)
            out.setdefault(s, []).append({"target_difficulty": lvl,
                                          "difficulty_range": [max(x[0] for x in b), min(x[1] for x in b)]})
            gaps[lvl] = max(0, gaps.get(lvl, 0) - 1)
            short = {x: n - (x in b) for x, n in short.items() if n - (x in b) > 0}
    order = subcategories(pool, len(categories.subcategories(bundle)), bundle)
    fresh = {s: [c["known_at"] for c in concepts.unused(lst, concepts.uses(pool, bundle, s))]
             for s in order if (lst := concepts.load(bundle, s))}
    for lvl in sorted((l for l in gaps if gaps[l]), key=lambda l: sum(abs(k - l) <= 1 for ks in fresh.values() for k in ks)):
        for _ in range(gaps[lvl]):
            s = max(fresh, key=lambda s: (sum(abs(k - lvl) <= 1 for k in fresh[s]) / (1 + len(out.get(s, []))),
                                          -order.index(s)), default=None)
            if s is None:
                break
            out.setdefault(s, []).append({"target_difficulty": lvl})
    return {s: out[s] for s in order if s in out}


def subcategories(pool, count=None, bundle="base"):
    """The bundle's `count` subcategories (default: SHARE of them, D-46; a pilot's PILOT_SUBCATEGORIES) with the fewest
    approved questions of that bundle in `pool` (copies too), each weighted by its level's share of the deficits to the
    targets (D-54; a base bundle: the draft gap over its question locales, decision 236); ties in its categories.json
    order (D-41), a pilot's spread over the categories (each category's first, then its second …)."""
    deficit = targets.draft_gaps(pool, bundle)
    total = sum(deficit.values()) if deficit else 0
    approved = {}
    for q in pool:
        if q["status"] == "approved" and q.get("bundle") == bundle:
            w = deficit.get(q["difficulty"], 0) / total if deficit else 1
            approved[q["subcategory"]] = approved.get(q["subcategory"], 0) + w
    order = categories.subcategories(bundle)
    first = count is None and pilot(pool, bundle)
    count = count or (PILOT_SUBCATEGORIES if first else math.ceil(len(order) * SHARE))
    rank = {s: i for c in categories.load(bundle) for i, s in enumerate(c["subcategories"])} if first else {}
    return sorted(order, key=lambda s: (approved.get(s, 0), rank.get(s, 0), order.index(s)))[:count]
