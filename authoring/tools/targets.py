"""Pool targets per bundle (plans/12, D-53): shared by qgen.py and the authoring server."""
import json, math
from collections import Counter

from layout import BUNDLES, TARGETS
import categories  # authoring/tools/categories.py
import translations  # authoring/tools/translations.py (D-81)

NOT_BUNDLES = {"about", "batch_health", "quality"}  # top-level keys that aren't bundles (D-55, plan 16)
REL = "authoring/data/targets.json"  # in messages
MIN_YIELD = 0.1  # floor of a locale's yield: a 0 % pilot asks 10× its deficit, not ∞
BUNDLE_TOTAL = 2000  # every non-base bundle (D-99, plan 184)


def load_all():
    return json.loads(TARGETS.read_text(encoding="utf-8")) if TARGETS.exists() else {}


def load_targets(bundle):
    """{"total": n, "difficulty": {level (int): n}} for the bundle, or None without targets."""
    t = load_all().get(bundle)
    if t is None:
        return None
    return {"total": t["total"], "difficulty": {int(k): v for k, v in t["difficulty"].items()}}


def apportion(n, weights):
    """{key: count}: n split in proportion to the weights, largest remainder."""
    total = sum(weights.values())
    exact = {k: n * w / total for k, w in weights.items()}
    out = {k: int(x) for k, x in exact.items()}
    for k in sorted(exact, key=lambda k: exact[k] - out[k], reverse=True)[:n - sum(out.values())]:
        out[k] += 1
    return out


def scaled(total, like="base"):
    """{"total": total, "difficulty": {level (str): n}}: `like`'s mix scaled to total (largest remainder)."""
    return {"total": total, "difficulty": apportion(total, load_all()[like]["difficulty"])}


MEDIA_FIRST = "media-first"  # run.json mode with its own quality and health numbers (plan 204, decision 647)


def load_quality(mode=None):
    """{"spot_check_size": n, "min_agreement": fraction} (plan 16, pm decision 2), or None before it's stored.
    mode MEDIA_FIRST: the media-first numbers over these, plus "first_run_size" (decision 647)."""
    t = load_all().get("quality")
    base = t and {k: v for k, v in t.items() if k not in ("about", "media_first")}
    own = (t or {}).get("media_first")
    if mode != MEDIA_FIRST or not own:
        return base
    return {**base, **{k: v for k, v in own.items() if k != "about"}}


def number(x, lo=None):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and (lo is None or x >= lo)


def quality_problems():
    """Errors in targets.json's "quality": spot_check_size an integer ≥ 1, min_agreement a fraction in (0, 1];
    "media_first" the same plus first_run_size."""
    t = load_all().get("quality")
    if t is None:
        return []
    out = []

    def check(where, d, keys):
        if set(d) - {"about"} != keys:
            out.append(f"{REL}: {where}: keys must be {', '.join(sorted(keys))}")
        for k in keys & {"spot_check_size", "first_run_size"}:
            if not isinstance(d.get(k), int) or isinstance(d.get(k), bool) or d[k] < 1:
                out.append(f"{REL}: {where}: {k} must be an integer ≥ 1")
        rate = d.get("min_agreement")
        if not number(rate) or not 0 < rate <= 1:
            out.append(f"{REL}: {where}: min_agreement must be a fraction in (0, 1]")
    own = t.get("media_first")
    check("quality", {k: v for k, v in t.items() if k != "media_first"}, {"spot_check_size", "min_agreement"})
    if own is not None:
        check("quality.media_first", own, {"spot_check_size", "first_run_size", "min_agreement"})
    return out


def load_batch_health(mode=None):
    """{metric: {"min"/"max": x}} (plan 15, pm decision 13), or None before it's stored.
    mode MEDIA_FIRST: the media-first block over these; a null there drops the metric (plan 204)."""
    t = load_all().get("batch_health")
    base = t and {k: v for k, v in t.items() if k not in ("about", MEDIA_FIRST)}
    if mode != MEDIA_FIRST or base is None:
        return base
    own = {k: v for k, v in (t.get(MEDIA_FIRST) or {}).items() if k != "about"}
    return {k: v for k, v in {**base, **own}.items() if v is not None}


def health_problems(metrics):
    """Errors in targets.json's "batch_health": known metric names, only numeric min/max (null allowed in the media-first block)."""
    out = []
    t = load_all().get("batch_health") or {}
    for where, block in (("batch_health", {k: v for k, v in t.items() if k not in ("about", MEDIA_FIRST)}),
                         (f"batch_health.{MEDIA_FIRST}", {k: v for k, v in (t.get(MEDIA_FIRST) or {}).items() if k != "about"})):
        for k, v in block.items():
            if k not in metrics:
                out.append(f"{REL}: {where}: unknown metric {k!r}")
            elif v is None and where != "batch_health":
                continue
            elif not isinstance(v, dict) or not v or set(v) - {"min", "max"} or not all(number(x) for x in v.values()):
                out.append(f"{REL}: {where}: {k}: must be {{\"min\": n, \"max\": n}} (one or both)")
    return out


def approved_entries(pool_questions, bundle, locale=None):
    """The bundle's approved questions in a locale (decision 235): its approved sources in that locale and the
    playing translations into it, with the translation's difficulty; without a locale every approved source."""
    src = [q for q in pool_questions if q.get("bundle") == bundle]
    if locale is None:
        return [q for q in src if q["status"] == "approved"]
    ts = {t["id"]: t for t in translations.load(locale)["questions"]}
    return [q if translations.source_locale(q) == locale else {**q, "difficulty": ts[q["id"]]["difficulty"]}
            for q in src if (q["status"] == "approved" if translations.source_locale(q) == locale
                             else q["id"] in ts and translations.plays(ts[q["id"]], q))]


def approved_by_level(pool_questions, bundle, locale=None):
    """Counter {difficulty: approved} of approved_entries (D-81, plan 70, decision 235)."""
    return Counter(q["difficulty"] for q in approved_entries(pool_questions, bundle, locale))


def deficits(pool_questions, bundle, locale=None):
    """{level: max(0, target − approved)} for the bundle (D-54), per locale (decision 37);
    None without targets or deficits."""
    t = load_targets(bundle)
    if t is None:
        return None
    have = approved_by_level(pool_questions, bundle, locale)
    out = {lvl: max(0, n - have[lvl]) for lvl, n in t["difficulty"].items()}
    return out if any(out.values()) else None


def source_supply(pool_questions, bundle="base", draft="en"):
    """Per question locale (plan 70, decision 236): yield, the deficit, and per level the approved, translatable
    sources in another locale not yet translated into it (or stale); `draft`: the drafting locale."""
    out = {}
    for l in translations.LOCALES:
        ts = {t["id"]: t for t in translations.load(l)["questions"]}
        untranslated = Counter(q["difficulty"] for q in pool_questions
                               if q["status"] == "approved" and q.get("bundle") == bundle and translations.translatable(q)
                               and translations.source_locale(q) != l
                               and (q["id"] not in ts or translations.is_stale(ts[q["id"]], q)))
        out[l] = {"yield": translations.yield_rate(l), "deficit": deficits(pool_questions, bundle, l) or {},
                  "untranslated": dict(untranslated), "draft": l == draft}
    return out


def locale_gap(s, lvl):
    """Sources to draft for one locale's deficit at a level (decision 236): deficit / yield − untranslated;
    the drafting locale takes its drafts 1:1 and the others' translations at its yield."""
    y = max(s["yield"], MIN_YIELD)
    d, u = s["deficit"].get(lvl, 0), s["untranslated"].get(lvl, 0)
    return max(0, math.ceil(d - u * y) if s["draft"] else math.ceil(d / y) - u)


def kind_of(bundle):
    """The bundle's `kind` in bundles.json; unknown ids count as base's own."""
    return next((b["kind"] for b in json.loads(BUNDLES.read_text())["bundles"] if b["id"] == bundle), "base")


def draft_gaps(pool_questions, bundle, supply=None):
    """What `draft` aims at (D-54): for base and a theme the largest over the question locales of locale_gap
    (decision 236), for a region its own deficits (D-101); None: even weights (D-40)."""
    if kind_of(bundle) not in {"base", "theme"}:
        return deficits(pool_questions, bundle)
    supply = supply or source_supply(pool_questions, bundle)
    levels = (load_targets(bundle) or {}).get("difficulty", {})
    out = {lvl: max(locale_gap(s, lvl) for s in supply.values()) for lvl in levels}
    return out if any(out.values()) else None


def category_shares(bundle):
    """{broad category slug: derived share} = total × its subcategories / the bundle's (guide only)."""
    t = load_targets(bundle)
    if t is None:
        return None
    cats = categories.load(bundle)
    n = sum(len(c["subcategories"]) for c in cats)
    return {c["slug"]: t["total"] * len(c["subcategories"]) / n for c in cats} if n else {}


def problems(scale, bundles):
    """Errors in targets.json: bundles known, every non-base bundle has an entry (D-99),
    levels = scale, values ≥ 0, sum = total."""
    bundle_ids = {b["id"] for b in bundles}
    all_ = load_all()
    out = [f"{REL}: {b.get('kind')} bundle {b['id']!r} has no targets (D-99: {BUNDLE_TOTAL})"
           for b in bundles if b.get("kind") != "base" and b["id"] not in all_]
    lo, hi = scale
    for b, t in all_.items():
        if b in NOT_BUNDLES:
            continue
        if b not in bundle_ids:
            out.append(f"{REL}: {b!r} is not a bundle")
            continue
        total, diff = t.get("total"), t.get("difficulty") or {}
        levels = {str(l) for l in range(lo, hi + 1)}
        if set(diff) != levels:
            missing, extra = sorted(levels - set(diff), key=int), sorted(set(diff) - levels)
            out.append(f"{REL}: {b}: levels must be {lo}–{hi}"
                       + (f"; missing {', '.join(missing)}" if missing else "")
                       + (f"; extra {', '.join(extra)}" if extra else ""))
        bad = [k for k, v in diff.items() if not isinstance(v, int) or isinstance(v, bool) or v < 0]
        if bad:
            out.append(f"{REL}: {b}: targets must be integers ≥ 0: {', '.join(bad)}")
        elif not isinstance(total, int) or isinstance(total, bool) or sum(diff.values()) != total:
            out.append(f"{REL}: {b}: difficulty targets sum to {sum(diff.values())}, total is {total}")
    return out
