"""`qgen demo` (plan 174, decision 339): the demo's candidates from the source pool, then authoring/tools/demo.ts under Node
(D-60) sizes, picks or checks the list. No LLM.

Candidates: base, approved, translatable; every picked file in the media cache with a shippable licence (media.py
`licence_of`, as `trivia-media licenses`); no human spot check that didn't approve it. Per launch locale the question
plays when it is the source's locale or a playing translation (translations.plays) that no spot check turned down;
full = plays in all four, pending = some missing. Health has no per-question mark (batch level only, D-55)."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import categories  # authoring/tools/categories.py
import engine  # authoring/tools/engine.py
import media  # authoring/tools/media.py: licence_of
import media_cache  # authoring/tools/media_cache.py: cache_path
import translations  # authoring/tools/translations.py
from layout import AUTHORING, DEMO_LIST, DEMO_WORK, REPO, SOURCE_POOL, SPOT_CHECKS

SCRIPT = AUTHORING / "tools" / "demo.ts"
MAX_SEATS = 5  # milestone 16: 4 pads + keyboard and mouse


def load(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def turned_down():
    """{locale or None: ids} a human spot check didn't approve (None: the source)."""
    out = defaultdict(set)
    for run, entry in (load(SPOT_CHECKS) or {}).items():
        for qid, it in (entry.get("items") or {}).items():
            if it.get("human") not in (None, "approved"):
                out[translations.run_locale(run)].add(qid)
    return out


def shippable(q):
    return (all(media_cache.cache_path(url).exists() for _, url in media_cache.picked(q))
            and all(v["verdict"] != "replace" for v in media.licence_of(q).values()))


def candidates(pool=None):
    """([{id, subcategory, category, media, full, difficulty {locale: d}, missing [locales]}], shares) in source order;
    shares over the approved base pool: per category, audio + video."""
    pool = pool or load(SOURCE_POOL)["questions"]
    cat_of = {s: c["slug"] for c in categories.load("base") for s in c["subcategories"]}
    by_locale = {l: {t["id"]: t for t in translations.load(l)["questions"]} for l in translations.LOCALES}
    down = turned_down()
    base = [q for q in pool if (q.get("bundle") or "base") == "base" and q["status"] == "approved"]
    out = []
    for q in base:
        if not translations.translatable(q) or q["id"] in down[None] or not shippable(q):
            continue
        diff, missing = {}, []
        for l in translations.LOCALES:
            t = by_locale[l].get(q["id"])
            if translations.source_locale(q) == l:
                diff[l] = q["difficulty"]
            elif t and translations.plays(t, q) and q["id"] not in down[l]:
                diff[l] = t["difficulty"]
            else:
                diff[l] = q["difficulty"]
                missing.append(l)
        out.append({"id": q["id"], "subcategory": q["subcategory"], "category": cat_of.get(q["subcategory"], "?"),
                    "media": q["media"].get("type"), "full": not missing, "difficulty": diff, "missing": missing})
    cats = Counter(cat_of.get(q["subcategory"], "?") for q in base)
    av = sum(q["media"].get("type") in ("audio", "video") for q in base)
    shares = {"categories": {c: n / len(base) for c, n in cats.items()}, "av": av / len(base) if base else 0}
    return out, shares


def run(cmd, cands, shares, **opts):
    return engine.node(SCRIPT, {"cmd": cmd, "candidates": cands, "locales": list(translations.LOCALES), "shares": shares,
                                **opts})


def mark(ok):
    return "pass" if ok else "**fail**"


def rows_md(rows):
    """Configuration × locale: engine check (cards) and with the reserve."""
    by = defaultdict(dict)
    for r in rows:
        by[r["config"]][r["locale"]] = r
    out = ["| configuration | " + " | ".join(translations.LOCALES) + " |", "|---|" + "---|" * len(translations.LOCALES)]
    for config, per in by.items():
        cells = [f"{mark(r['engine'])} / {mark(r['reserve'])}" + (f" ({r['reserve_short']} short)" if r["reserve_short"] else "")
                 for r in (per[l] for l in translations.LOCALES)]
        out.append(f"| {config} | " + " | ".join(cells) + " |")
    return out


def sizes_md(rows, cands):
    full = sum(c["full"] for c in cands)
    out = [f"Candidates: {full} full, {len(cands) - full} pending (missing translations).", "",
           "| seats | list size | full | pending | binding configuration | unmet |", "|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['seats']} | {r['size']} | {r['full']} | {r['pending']} | {r['binding'] or '–'} | "
                   f"{', '.join(r['unmet']) or '–'} |")
    return out


def spread_md(res, shares, cands):
    """Difficulty (es) vs. the age groups' level_weights, categories vs. the pool's shares, subcategories, media."""
    by_id = {c["id"]: c for c in cands}
    lst = [by_id[i] for i in res["ids"]]
    n = len(lst) or 1
    weights = Counter()
    for w in res["groups"].values():
        total = sum(w.values())
        for d, x in w.items():
            weights[int(d)] += x / total / len(res["groups"])
    diff = Counter(c["difficulty"]["es"] for c in lst)
    out = ["### Difficulty (es)", "", "| difficulty | listed | target |", "|---|---|---|"]
    out += [f"| {d} | {diff[d]} | {weights[d] * n:.0f} |" for d in sorted(set(diff) | set(weights))]
    cats = Counter(c["category"] for c in lst)
    out += ["", "### Categories", "", "| category | listed | target |", "|---|---|---|"]
    out += [f"| {c} | {cats[c]} | {s * n:.0f} |" for c, s in sorted(shares["categories"].items(), key=lambda x: -x[1])]
    subs = Counter(c["subcategory"] for c in lst)
    all_subs = {c["subcategory"] for c in cands}
    out += ["", f"Subcategories: {len(subs)} of {len(all_subs)} with candidates; at most {max(subs.values(), default=0)} per subcategory."]
    kinds = Counter(c["media"] or "none" for c in lst)
    out += ["", "### Media", "", f"Listed: {', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))}; "
            f"audio + video target {shares['av'] * n:.1f} (the approved base pool's share)."]
    return out


def propose(seats):
    cands, shares = candidates()
    res = run("propose", cands, shares, seats=seats)
    by_id = {c["id"]: c for c in cands}
    DEMO_WORK.mkdir(parents=True, exist_ok=True)
    proposal = {"version": 1, "seats": seats, "ids": res["ids"],
                "questions": {i: {"subcategory": by_id[i]["subcategory"], "difficulty": by_id[i]["difficulty"],
                                  "media": by_id[i]["media"], "full": by_id[i]["full"]} for i in res["ids"]}}
    (DEMO_WORK / "proposal.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    pending = defaultdict(list)
    for i in res["ids"]:
        for l in by_id[i]["missing"]:
            pending[l].append(i)
    rv = res["reserve"]
    md = [f"# Demo list proposal: {res['size']} questions, up to {seats} seat(s)", "",
          f"{res['full']} full, {res['pending']} pending (missing translations). Binding configuration: {res['binding'] or '–'}.",
          f"Unmet (not enough candidates): {', '.join(res['unmet']) or 'none'}.", "",
          f"Reserve: {rv['cards']} cards + R = {rv['r']} at one level (jokers, «Cambiar pregunta»); timed: R = 0, "
          f"sudden death {rv['sudden_death_rounds']} rounds of every seat at the last level.", "",
          "## Configurations", "", "Engine check (cards) / with the reserve, per locale.", "", *rows_md(res["rows"]), "",
          "## «Bájale»", "", "Listed questions with an easier one of their subcategory in the list: "
          + ", ".join(f"{l} {100 * s:.0f} %" for l, s in res["easier"].items()) + ".", "",
          "## Spread", "", *spread_md(res, shares, cands), "",
          "## Pending translations", ""]
    md += [f"- {l}: {len(ids)}: {', '.join(ids)}" for l, ids in pending.items()] or ["- none"]
    md += ["", "## Added per configuration", ""] + [f"- {k}: {v}" for k, v in sorted(res["added"].items(), key=lambda x: -x[1])]
    (DEMO_WORK / "proposal.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:5]))
    print(f"wrote {(DEMO_WORK / 'proposal.json').relative_to(REPO)} and {(DEMO_WORK / 'proposal.md').relative_to(REPO)}")
    return 0 if not res["unmet"] else 1


def problems(doc, pool=None):
    """(errors, warnings, report lines) for a list: ids that aren't candidates, pending ones, failing configurations."""
    cands, shares = candidates(pool)
    known = {c["id"]: c for c in cands}
    gone = [i for i in doc["ids"] if i not in known]
    pending = [i for i in doc["ids"] if i in known and not known[i]["full"]]
    seats = doc.get("seats") or 1
    res = run("check", cands, shares, seats=seats, ids=doc["ids"])
    failing = [r for r in res["rows"] if not r["reserve"]]
    errors, lines = [], [f"{res['size']} listed candidate(s), {len(pending)} pending, up to {seats} seat(s)"]
    if gone:
        errors.append(f"no longer candidates: {', '.join(gone)}")
    for r in failing:
        errors.append(f"fails: {r['config']} ({r['locale']}): engine {mark(r['engine'])}, reserve {r['reserve_short']} short")
    note = f"{len(pending)} listed id(s) with missing translations: {', '.join(pending)}"
    if pending and doc.get("approved"):
        errors.append(note)
    return errors, ([note] if pending and not doc.get("approved") else []), lines


def check(path):
    """Exit 1 when an id is no candidate any more or a configuration fails at the list's seats."""
    doc = load(path)
    if doc is None:
        print(f"{path}: no demo list")
        return 1
    errors, warnings, lines = problems(doc)
    print(f"{path}: {lines[0]}")
    for m in [*errors, *warnings]:
        print(m)
    print("FAIL" if errors else "OK")
    return 1 if errors else 0


def sizes():
    cands, shares = candidates()
    rows = run("sizes", cands, shares, max_seats=MAX_SEATS)
    print("\n".join(sizes_md(rows, cands)))
    return 0


def main(args):
    if args.sizes:
        sys.exit(sizes())
    if args.propose:
        sys.exit(propose(args.seats))
    sys.exit(check(Path(args.check) if args.check else DEMO_LIST))
