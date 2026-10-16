"""`qgen rekey --map <proposal.json> [--apply]` (plan 149, decision 259: Category and subcategory keys: English slugs):
category and subcategory keys → English slugs in every file that holds them; dry run by default.

The map is decision 258's list (work/slugs/proposal.json): {bundle: [[old category slug, es name, en name, new slug,
[[old subcategory, en name, new slug], …]], …]}. Writes categories.json (structure only), the names files (keys renamed,
names.es.json from today's Spanish names), questions.json and questions.<locale>.json, concept lists (renamed to
<slug>.json), work files (run.json, slots.json, fit.json, drafts and their ratings/factchecks/revisions/translations,
work/concepts/) and app/data/old-keys.json. Pools: `qgen export` afterwards. Idempotent: a rekeyed bundle is skipped;
once all are, work files still on old keys are mapped through old-keys.json.
"""
import json
import sys
import uuid

import atomic
import categories
import concepts
import layout
import translations
from layout import REPO as ROOT, SOURCE_POOL, WORK

OLD_KEYS = layout.app_paths.OLD_KEYS
CHECKED = [layout.TARGETS, layout.AXES_FILE, layout.SPOT_CHECKS, layout.UI_FLAGS]  # warned about, never rewritten
STEM_DIRS = ["ratings", "factchecks", "revisions"]  # named like the draft files


def rel(p):
    return p.relative_to(ROOT) if p.is_relative_to(ROOT) else p


def load_map(path):
    """{bundle: {"cats": {old: (new, en)}, "subs": {old: (new, en)}}} of the bundles still on old keys; exits on a bad map."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        out = {b: {"cats": {c[0]: (c[3], c[2]) for c in cats},
                   "subs": {s[0]: (s[2], s[1]) for c in cats for s in c[4]}} for b, cats in raw.items()}
    except (OSError, ValueError, IndexError, TypeError, AttributeError) as e:
        sys.exit(f"{path}: not a slug map ({type(e).__name__}: {e})")
    errors = []
    for b, m in list(out.items()):
        if b not in categories.bundle_ids():
            errors.append(f"{b}: not a bundle")
            continue
        cats, subs = [c["slug"] for c in categories.load(b)], categories.subcategories(b)
        if all(x in {n for n, _ in m[k].values()} and m[k].get(x, (x,))[0] == x for k, xs in [("cats", cats), ("subs", subs)]
               for x in xs):
            print(f"{b}: already on slug keys, skipped")
            del out[b]
            continue
        for kind, have in [("cats", cats), ("subs", subs)]:
            what = "category" if kind == "cats" else "subcategory"
            if missing := [x for x in have if x not in m[kind]]:
                errors.append(f"{b}: {what} not in the map: {', '.join(missing)}")
            if extra := [x for x in m[kind] if x not in have]:
                errors.append(f"{b}: {what} in the map but not in {rel(categories.path(b))}: {', '.join(extra)}")
            new = [n for n, _ in m[kind].values()]
            if bad := [n for n in new if not categories.SLUG.fullmatch(n)]:
                errors.append(f"{b}: not a slug: {', '.join(bad)}")
            if dup := sorted({n for n in new if new.count(n) > 1}):
                errors.append(f"{b}: {what} slug twice: {', '.join(dup)}")
    if errors:
        sys.exit(f"{path}:\n" + "\n".join(f"  {e}" for e in errors))
    return out


class Plan:
    """Files to write and to move (two-phase, so a new name may be another file's old one)."""

    def __init__(self):
        self.writes, self.moves, self.notes = {}, {}, []

    def write(self, path, data, note):
        self.writes[path] = (data, note)

    def move(self, src, dst, data=None, note=""):
        if src != dst:
            self.moves[src] = (dst, data, note)
        elif data is not None:
            self.write(src, data, note)

    def check(self):
        dsts = [d for d, _, _ in self.moves.values()]
        errors = [f"{rel(d)}: two files would get this name" for d in {d for d in dsts if dsts.count(d) > 1}]
        errors += [f"{rel(d)}: exists already" for d in dsts if d.exists() and d not in self.moves]
        return errors

    def show(self):
        for p, (_, note) in sorted(self.writes.items()):
            print(f"  write {rel(p)}: {note}")
        for s, (d, _, note) in sorted(self.moves.items()):
            print(f"  move  {rel(s)} → {d.name}" + (f": {note}" if note else ""))
        for n in self.notes:
            print(f"  note  {n}")

    def apply(self):
        tmp = {}
        for s, (d, _, _) in self.moves.items():
            tmp[s] = s.with_name(f".rekey-{uuid.uuid4().hex}")
            s.rename(tmp[s])
        for s, (d, data, _) in self.moves.items():
            d.parent.mkdir(parents=True, exist_ok=True)
            if data is None:
                tmp[s].rename(d)
            else:
                atomic.write_json(d, data)
                tmp[s].unlink()
        for p, (data, _) in self.writes.items():
            if isinstance(data, str):
                atomic.write_text(p, data)
            else:
                atomic.write_json(p, data)


def categories_text(doc):
    """categories.json in its hand-kept layout: one line per category, one per subcategory."""
    head = f'  "about": {json.dumps(doc["about"], ensure_ascii=False)},\n' if doc.get("about") else ""
    cats = [f'    {{"slug": {json.dumps(c["slug"])}, "subcategories": [\n'
            + ",\n".join(f"      {json.dumps(s, ensure_ascii=False)}" for s in c["subcategories"]) + "\n    ]}"
            for c in doc["categories"]]
    return "{\n" + head + '  "categories": [\n' + ",\n".join(cats) + "\n  ]\n}\n"


def plan_data(m, plan):
    """categories.json, names files, old-keys.json: the app/data side."""
    old_keys = json.loads(OLD_KEYS.read_text(encoding="utf-8")) if OLD_KEYS.exists() else {"categories": {}, "subcategories": {}}
    for b, mb in m.items():
        cats = categories.load(b)
        doc = json.loads(categories.path(b).read_text(encoding="utf-8"))
        new_cats = [{"slug": mb["cats"][c["slug"]][0], "subcategories": [mb["subs"][s][0] for s in c["subcategories"]]}
                    for c in cats]
        about = doc.get("about") and (f"Categories of the {b} bundle (D-41, D-43): structure only, keyed by English slugs "
                                      "unique within the bundle (decision 259); names in names.<locale>.json.")
        plan.write(categories.path(b), categories_text({"about": about, "categories": new_cats}),
                   f"{len(new_cats)} categories, {sum(len(c['subcategories']) for c in new_cats)} subcategories on slugs, no names")
        spanish = {"categories": {mb["cats"][c["slug"]][0]: c.get("name") or c["slug"] for c in cats},
                   "subcategories": {mb["subs"][s][0]: s for c in cats for s in c["subcategories"]}}
        order = {"categories": [c["slug"] for c in new_cats], "subcategories": [s for c in new_cats for s in c["subcategories"]]}
        for loc in [*categories.NAMES_LOCALES, "es-ES"]:
            p = layout.NAMES(loc, b)
            if loc == "es":
                if p.exists():
                    sys.exit(f"{rel(p)} exists but {b} is on old keys")
                plan.write(p, {"version": 1, "locale": "es", **spanish}, "new: today's Spanish names")
                continue
            if not p.exists():
                if loc == "es-ES":
                    continue
                f = {"version": 1, "locale": loc}
            else:
                f = json.loads(p.read_text(encoding="utf-8"))
            filled = 0
            for kind, mk in [("categories", "cats"), ("subcategories", "subs")]:
                have = {mb[mk][k][0]: v for k, v in (f.get(kind) or {}).items() if k in mb[mk]}
                if loc == "en":
                    filled += sum(n not in have for n in order[kind])
                    have = {n: have.get(n) or next(en for k, (x, en) in mb[mk].items() if x == n) for n in order[kind]}
                f[kind] = {n: have[n] for n in order[kind] if n in have}
            plan.write(p, f, "keys renamed" + (f", {filled} en name(s) from the map" if filled else ""))
        for kind, mk in [("categories", "cats"), ("subcategories", "subs")]:
            old_keys[kind] |= {categories.sub_key(b, o): categories.sub_key(b, n) for o, (n, _) in mb[mk].items() if o != n}
    plan.write(OLD_KEYS, old_keys, f"{len(old_keys['categories'])} category and {len(old_keys['subcategories'])} subcategory keys")


def sub_mapper(m):
    """(bundle, old key) → new key, or None when the bundle isn't rekeyed or the key unknown."""
    return lambda b, s: m[b]["subs"].get(s, (None,))[0] if b in m else None


def plan_questions(m, plan):
    new = sub_mapper(m)
    data = json.loads(SOURCE_POOL.read_text(encoding="utf-8"))
    n, unknown = 0, []
    for q in data["questions"]:
        b = q.get("bundle") or "base"
        if b not in m:
            continue
        if (s := new(b, q.get("subcategory"))) is None:
            unknown.append(q["id"])
        elif s != q["subcategory"]:
            q["subcategory"], n = s, n + 1
    if unknown:
        sys.exit(f"{rel(SOURCE_POOL)}: subcategory not in the map: {', '.join(unknown[:10])}")
    plan.write(SOURCE_POOL, data, f"{n} subcategory fields")
    bundle_of = {q["id"]: q.get("bundle") or "base" for q in data["questions"]}
    for loc in translations.LOCALES:
        p = layout.translations(loc)
        if not p.exists():
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        n = 0
        for t in doc["questions"]:
            if "subcategory" in t and (s := new(bundle_of.get(t["id"], "base"), t["subcategory"])) and s != t["subcategory"]:
                t["subcategory"], n = s, n + 1
        if n:
            plan.write(p, doc, f"{n} subcategory fields")


def plan_concepts(m, plan):
    new = sub_mapper(m)
    for b in m:
        for p in sorted(concepts.concepts_dir(b).glob("*.json")):
            lst = json.loads(p.read_text(encoding="utf-8"))
            s = new(b, lst.get("subcategory"))
            if s is None:
                plan.notes.append(f"{rel(p)}: subcategory {lst.get('subcategory')!r} not in {b}'s map, left as is")
                continue
            plan.move(p, concepts.path(b, s), {**lst, "subcategory": s}, "subcategory field")


def work_table(m):
    """{bundle: {old subcategory key: new}} for the work files: from the map, else (already rekeyed) from old-keys.json."""
    if m:
        return {b: {o: n for o, (n, _) in mb["subs"].items()} for b, mb in m.items()}
    out = {}
    if OLD_KEYS.exists():
        for k, v in json.loads(OLD_KEYS.read_text(encoding="utf-8"))["subcategories"].items():
            (b, o), (_, n) = categories.parse_key(k), categories.parse_key(v)
            out.setdefault(b, {})[o] = n
    return out


def work_mapper(table):
    """(run bundle, key) → new key or None: the run's bundle first, else the one other bundle that has it (a base run from
    before D-99 holds today's colombia names bare). Key only, so slots.json and its drafts map alike."""
    def new(rb, k):
        if k in table.get(rb, {}):
            return table[rb][k]
        hits = {t[k] for b, t in table.items() if b != rb and k in t}
        return hits.pop() if len(hits) == 1 else None
    return new


def stems(table):
    """{old work file stem: new} (qgen.concept_file: base's bare, another bundle's <bundle>--<slug>, also for older bare ones)."""
    out = {}
    for b in sorted(table, key=lambda b: b == "base"):  # base last: its bare stems win
        for o, n in table[b].items():
            new = n if b == "base" else f"{b}--{n}"
            out[concepts.slug(o)] = new
            out[f"{b}--{concepts.slug(o)}"] = new
    return out


def plan_work(table, plan):
    new, st = work_mapper(table), stems(table)

    def renamed(name):
        pre = "revised-" if name.startswith("revised-") else ""
        return pre + st[name[len(pre):]] if name[len(pre):] in st else None

    def chunk(name):  # translations/<stem>[-<locale>]-<n>: the longest old stem that prefixes it
        hit = max((s for s in st if name == s or name.startswith(s + "-")), key=len, default=None)
        return hit and st[hit] + name[len(hit):]

    for d in sorted(p.parent for p in WORK.glob("*/run.json")):
        cfg = json.loads((d / "run.json").read_text(encoding="utf-8"))
        rb = cfg.get("bundle", "base")
        if isinstance(cfg.get("subcategories"), list):
            subs = [new(rb, s) or s for s in cfg["subcategories"]]
            if subs != cfg["subcategories"]:
                plan.write(d / "run.json", {**cfg, "subcategories": subs}, "subcategories")
        for f in ["slots.json", "fit.json"]:
            if (d / f).exists():
                doc = json.loads((d / f).read_text(encoding="utf-8"))
                if isinstance(doc, dict) and any(new(rb, k) not in (None, k) for k in doc):
                    plan.write(d / f, {new(rb, k) or k: v for k, v in doc.items()}, "keys")
        for p in sorted((d / "drafts").glob("*.json")):
            doc = json.loads(p.read_text(encoding="utf-8"))
            n = 0
            for q in doc.get("questions") or []:
                s = new(rb, q.get("subcategory"))
                if s and s != q.get("subcategory"):
                    q["subcategory"], n = s, n + 1
            dst = renamed(p.stem)
            plan.move(p, p.with_name(f"{dst}.json") if dst else p, doc if n else None,
                      f"{n} subcategory fields" if n else "")
        for sub in STEM_DIRS:
            for p in sorted((d / sub).glob("*.json")):
                if dst := renamed(p.stem):
                    plan.move(p, p.with_name(f"{dst}.json"))
        for p in sorted((d / "translations").glob("*.json")):
            if dst := chunk(p.stem):
                plan.move(p, p.with_name(f"{dst}.json"))
    for sub in ["raw", "topup"]:
        for p in sorted((WORK / "concepts" / sub).glob("*.json")):
            if dst := renamed(p.stem):
                plan.move(p, p.with_name(f"{dst}.json"))


def plan_checked(m, plan):
    """Files that may hold keys but aren't keyed by them today: a warning if one does."""
    olds = {k for mb in m.values() for kind in ("cats", "subs") for k in mb[kind]}

    def hits(x):
        if isinstance(x, dict):
            return sum((k in olds) + hits(v) for k, v in x.items())
        if isinstance(x, list):
            return sum(hits(v) for v in x)
        return int(isinstance(x, str) and x in olds)

    for p in CHECKED + sorted(layout.BUNDLE_SOURCES.glob("*/question-axes.json")):
        if p.exists() and (n := hits(json.loads(p.read_text(encoding="utf-8")))):
            plan.notes.append(f"{rel(p)}: {n} value(s) equal to an old key; not rewritten, check by hand")


def cmd_rekey(args):
    m = load_map(args.map)
    plan = Plan()
    if m:
        plan_data(m, plan)
        plan_questions(m, plan)
        plan_concepts(m, plan)
    plan_work(work_table(m), plan)
    plan_checked(m, plan)
    if not plan.writes and not plan.moves:
        return print("nothing to do")
    if errors := plan.check():
        sys.exit("cannot rekey:\n" + "\n".join(f"  {e}" for e in errors))
    print(f"{'Rekeying' if args.apply else 'Would rekey'} {', '.join(m) or 'work files (old-keys.json)'}: "
          f"{len(plan.writes)} file(s) written, {len(plan.moves)} moved")
    plan.show()
    if not args.apply:
        return print("dry run: --apply writes them; then `qgen export` and `qgen validate`")
    with atomic.locked(SOURCE_POOL):
        plan.apply()
    print("done: now `qgen export`, then `qgen validate`")
