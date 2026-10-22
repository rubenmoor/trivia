"""`qgen bundle new`, `taxonomy` and `remap` (D-41, plans 138, 184). Never ships (D-35)."""
import json, re, sys
from pathlib import Path
from collections import Counter

import layout  # paths (D-35)
from layout import PROMPTS, REPO as ROOT, SOURCE_POOL as POOL, WORK
import atomic  # authoring/tools/atomic.py: .tmp + replace writes, cross-process locks
import concepts  # authoring/tools/concepts.py: concept lists and question axes (D-37)
import categories  # authoring/tools/categories.py: every bundle's categories (D-19, D-43)
import targets  # authoring/tools/targets.py: pool targets (D-53)
import rekey  # authoring/tools/rekey.py: `qgen rekey` (plan 149)
import translations  # authoring/tools/translations.py: translated questions (D-81)

from qgen import INT, STR, bundle_row, bundle_text, claude, cmd_export, load_age_groups, load_bundles, load_json, save_json, slug, voice_locale  # authoring/tools/qgen.py


CATEGORIES_ABOUT = ("Categories of the {bundle} bundle (D-41, D-43): structure only, keyed by English slugs unique "
                    "within the bundle (decision 259); names in names.<locale>.json.")


def cmd_bundle_new(args):
    """An empty bundle (BN-9, D-41): its entry in app/data/bundles.json, a non-base one's 2000 target
    (D-101) and an empty categories.json, for a regional or theme one filled by `qgen taxonomy` (plan 138), else by hand. Concept lists come from `qgen batch --bundle <id>`; axes stay base's until
    authoring/data/bundles/<id>/question-axes.json exists."""
    if not re.fullmatch(r"[a-z0-9-]+", args.id):
        sys.exit("A bundle id is lowercase letters, digits and dashes.")
    data = load_json(layout.BUNDLES)
    if any(b["id"] == args.id for b in data["bundles"]):
        sys.exit(f"Bundle {args.id!r} already exists.")
    if args.kind == "region" and not (args.language and args.voice and args.country):
        sys.exit("A regional bundle needs --language (the region's), --voice (its language variety) and --country.")
    if args.country and (args.kind != "region" or not re.fullmatch(COUNTRY, args.country)):
        sys.exit("--country: a regional bundle's ISO 3166-1 alpha-2 code in capitals, e.g. CO.")
    if args.icon and (args.kind == "region" or args.icon not in BUNDLE_ICONS):
        sys.exit(f"--icon: not on a regional bundle, else one of {', '.join(BUNDLE_ICONS)}.")
    data["bundles"].append({"id": args.id, "kind": args.kind, **({"country": args.country} if args.country else {}),
                            **({"icon": args.icon} if args.icon else {}),
                            "languages": [args.language or ("en" if args.kind == "theme" else "es")], "name": args.name,
                            "description": args.description, "rule": args.rule,
                            **({"voice": args.voice} if args.voice else {})})
    save_json(layout.BUNDLES, data)
    if args.kind != "base":
        t = targets.load_all()
        save_json(layout.TARGETS, {**t, args.id: targets.scaled(targets.BUNDLE_TOTAL)})
    path = categories.path(args.id)
    if not path.exists():
        save_json(path, {"about": CATEGORIES_ABOUT.format(bundle=args.id), "categories": []})
    nxt = (f"`qgen taxonomy --bundle {args.id}` proposes its categories and subcategories (plan 138), "
           f"`--apply` writes them" if args.kind in {"region", "theme"}
           else f"fill {path.relative_to(ROOT)} with broad categories and subcategories")
    print(f"Created bundle {args.id}. Next: {nxt}, then `qgen batch --bundle {args.id}`.")


PER_SUBCATEGORY = 40  # approved per subcategory a regional taxonomy is sized for (plan 138)
NAMES_MODEL = "sonnet"  # names of a taxonomy's new categories and subcategories
KEYED = {"slug": STR, "en": STR, "name": STR}  # key, English name, name in the bundle's language
TAXONOMY_SCHEMA = {"type": "object", "required": ["region", "categories", "left_out"], "properties": {
    "region": STR,
    "categories": {"type": "array", "items": {
        "type": "object", "required": [*KEYED, "origin", "scope", "reason", "subcategories"], "properties": {
            **KEYED, "origin": {"type": "string", "enum": ["general", "region"]}, "scope": STR, "reason": STR,
            "subcategories": {"type": "array", "items": {
                "type": "object", "required": [*KEYED, "scope", "reason", "samples"], "properties": {
                    **KEYED, "scope": STR, "reason": STR,
                    "samples": {"type": "array", "items": {"type": "object", "required": ["name", "known_at"],
                                                           "properties": {"name": STR, "known_at": INT}}}}}}}}},
    "left_out": {"type": "array", "items": {"type": "object", "required": ["name", "reason"],
                                            "properties": {"name": STR, "reason": STR}}}}}
SAMPLES = TAXONOMY_SCHEMA["properties"]["categories"]["items"]["properties"]["subcategories"]["items"]["properties"]["samples"]
THEME_TAXONOMY_SCHEMA = {"type": "object", "required": ["categories"], "properties": {
    "categories": {"type": "array", "items": {
        "type": "object", "required": [*KEYED, "origin", "scope", "reason", "subcategories"], "properties": {
            **KEYED, "origin": {"type": "string", "enum": ["base_extends", "new"]}, "scope": STR, "reason": STR,
            "subcategories": {"type": "array", "items": {
                "type": "object", "required": [*KEYED, "scope", "reason", "base_related", "samples"], "properties": {
                    **KEYED, "scope": STR, "reason": STR, "base_related": {"type": "array", "items": STR},
                    "samples": SAMPLES}}}}}}}}
BASE_RELATED_ABOUT = ("A theme bundle's subcategory → the base subcategories it goes beyond (plan 184); its concept lists "
                      "and drafts keep away from their questions. Authoring only, never exported.")


def names_locale(locale):
    """The names file a locale's names go in: es-ES's in es's, which es-ES reads first (decision 259)."""
    return "es" if locale.startswith("es") else locale


def derived_slug(en, region):
    """A new entry's slug from its English name, without the region: "Rivers of Colombia" → rivers."""
    r = re.escape(slug(region))
    return re.sub(rf"^{r}-|-(of|in|from)-(the-)?{r}$", "", slug(en)) or slug(en)


def off_list(bundle, subs):
    """{subcategory: Counter(status)} of the bundle's questions on a subcategory not in subs."""
    out = {}
    for q in load_json(POOL)["questions"]:
        if q.get("bundle") == bundle and q["subcategory"] not in subs:
            out.setdefault(q["subcategory"], Counter())[q["status"]] += 1
    return out


def off_list_lines(found):
    return [f"- {s}: {sum(c.values())} ({', '.join(f'{n} {st}' for st, n in c.most_common())})"
            for s, c in sorted(found.items(), key=lambda x: -sum(x[1].values()))]


def keyed(x):
    """`slug` English name (own-language name, if another)."""
    return f"`{x['slug']}` {x['en']}" + (f" ({x['name']})" if x["name"] != x["en"] else "")


ORIGIN = {"region": " (region)", "new": " (new)", "base_extends": " (extends base)"}


def taxonomy_md(p, found):
    """proposal.md: what goes into the pm decision (decision 18's format)."""
    cats = p["categories"]
    n = sum(len(c["subcategories"]) for c in cats)
    theme = "left_out" not in p
    lines = [f"# Taxonomy proposal: `{p['bundle']}`", "",
             f"{len(cats)} categories, {n} subcategories; target {p['target']} approved, "
             f"≈ {round(p['target'] / max(n, 1))} per subcategory. Each: `slug` English name (name in the bundle's "
             "language). Sample concepts: name (known_at).", "",
             "## Counts per category"]
    lines += [f"- {keyed(c)}{ORIGIN.get(c['origin'], '')}: {len(c['subcategories'])}" for c in cats]
    if theme:
        rel = [s for c in cats for s in c["subcategories"] if s["base_related"]]
        lines += ["", f"Categories: {sum(c['origin'] == 'base_extends' for c in cats)} base_extends, "
                  f"{sum(c['origin'] == 'new' for c in cats)} new; subcategories: {len(rel)} with base_related, "
                  f"{n - len(rel)} without."]
    if p.get("left_out"):
        lines += ["", "## Left out of the general list"] + [f"- {c['name']}: {c['reason']}" for c in p["left_out"]]
    i = 0
    for c in cats:
        lines += ["", f"## {keyed(c)}{ORIGIN.get(c['origin'], '')}", f"{c['scope']}"
                  + (f" Reason: {c['reason']}" if c["reason"] else "")]
        for s in c["subcategories"]:
            i += 1
            samples = ", ".join(f"{x['name']} ({x['known_at']})" for x in sorted(s["samples"], key=lambda x: x["known_at"]))
            base = f" Beyond base: {', '.join(s['base_related']) or 'none'}." if theme else ""
            lines.append(f"{i}. **{keyed(s)}**. {s['scope']} Reason: {s['reason']}{base} Samples: {samples}.")
    if found:
        lines += ["", "## Questions on subcategories not in the proposal (moved by the remap)"] + off_list_lines(found)
    return "\n".join(lines) + "\n"


def cmd_taxonomy(args):
    """A regional or theme bundle's taxonomy (plans 138, 184; decision 259): one opus call proposes categories and
    subcategories (slug, English name, name in the bundle's language) from the bundle's rule and voice and its target,
    a region's from the general list (decision 213), a theme's deeper than base's subcategories (with their approved
    counts and `base_related`) → work/taxonomy/<id>/proposal.{json,md}; `--apply <proposal.json>` writes
    categories.json and names.<locale>.json (a theme's base-related.json too), touching no question or concept list."""
    b = next((x for x in load_bundles() if x["id"] == args.bundle), None)
    if not b or b["kind"] not in ("region", "theme"):
        sys.exit(f"{args.bundle!r} is not a regional or theme bundle in app/data/bundles.json")
    theme = b["kind"] == "theme"
    d = WORK / "taxonomy" / args.bundle
    d.mkdir(parents=True, exist_ok=True)
    if args.apply:
        return apply_taxonomy(args.bundle, Path(args.apply), d)
    total = targets.load_targets(args.bundle)["total"]
    per = PER_SUBCATEGORY
    loc = translations.draft_locale(b)
    system = (PROMPTS / ("taxonomy-theme.md" if theme else "taxonomy.md")).read_text(encoding="utf-8").replace(
        "{per_sub}", str(per)).replace("{subs}", str(round(total / per))).replace("{language}", LANGUAGES[loc])
    approved = {x: Counter(q["subcategory"] for q in load_json(POOL)["questions"]
                           if (q.get("bundle") or "base") == x and q["status"] == "approved") for x in (args.bundle, "base")}
    def own(x, kind):
        en, name = (categories.display(args.bundle, x, l, kind) for l in ("en", loc))
        return keyed({"slug": x, "en": en, "name": name})
    if theme:
        base = ("## base's subcategories (`slug` English name: approved questions)\n" + "\n".join(
            f"- {cat_name(c, 'en')}: " + ", ".join(f"`{s}` {categories.display('base', s, 'en')}: {approved['base'][s]}"
                                                   for s in c["subcategories"]) for c in categories.load("base")))
    else:
        general = load_json(layout.REGIONAL_CATEGORIES)
        base = (f"## General list\n{general['about']}\n" + json.dumps(general["categories"], ensure_ascii=False, indent=1)
                + "\n\n## base's subcategories\n" + "\n".join(
                    f"- {cat_name(c, 'en')}: {', '.join(categories.display('base', s, 'en') for s in c['subcategories'])}"
                    for c in categories.load("base")))
    user = "\n\n".join([
        f"## Bundle\n`{args.bundle}`: {b['name']}\nLanguage: {LANGUAGES[loc]}\n{bundle_text(args.bundle, loc)}",
        f"## Target\n{total} approved questions: ≈ {round(total / per)} subcategories of ≈ {per}.", base,
        "## Existing taxonomy (context only; `slug` English name (own name): approved questions)\n" + ("\n".join(
            f"- {own(c['slug'], 'categories')}: " + ", ".join(f"{own(s, 'subcategories')}: {approved[args.bundle][s]}" for s in c["subcategories"])
            for c in categories.load(args.bundle)) or "none")])
    out = claude(system, user, THEME_TAXONOMY_SCHEMA if theme else TAXONOMY_SCHEMA, args.model, d)
    for x in [c for c in out["categories"]] + [s for c in out["categories"] for s in c["subcategories"]]:
        x["slug"] = slug(x["slug"])
        if "base_related" in x:
            x["base_related"] = [r for r in dict.fromkeys(x["base_related"]) if r in categories.subcategories("base")]
    p = {"bundle": args.bundle, "target": total, **out}
    save_json(d / "proposal.json", p)
    subs = {s["slug"] for c in p["categories"] for s in c["subcategories"]}
    (d / "proposal.md").write_text(taxonomy_md(p, off_list(args.bundle, subs)), encoding="utf-8")
    print(f"{len(p['categories'])} categories, {len(subs)} subcategories → {rekey.rel(d / 'proposal.md')}; "
          f"edit proposal.json to the developer's answer, then `qgen taxonomy --bundle {args.bundle} --apply "
          f"{rekey.rel(d / 'proposal.json')}`")


def cat_name(c, locale):
    """A loaded category's display name (decision 259)."""
    return categories.display(c["bundle"], c["slug"], locale, "categories")


def taxonomy_errors(p, bundle):
    errors = [] if p.get("bundle") == bundle else [f"bundle must be {bundle!r}"]
    cats = p.get("categories") or []
    for what, items in [("category", cats), ("subcategory", [s for c in cats for s in c.get("subcategories") or []])]:
        for f in KEYED:
            vals = [x.get(f) for x in items]
            if not all(isinstance(v, str) and v.strip() for v in vals):
                errors.append(f"every {what} needs a non-empty {f}")
            elif dup := sorted({v for v in vals if vals.count(v) > 1}):
                errors.append(f"same {what} {f} twice: {', '.join(dup)}")
        if bad := [x["slug"] for x in items if isinstance(x.get("slug"), str) and not categories.SLUG.fullmatch(x["slug"])]:
            errors.append(f"not a slug (decision 259): {', '.join(bad)}")
    errors += [f"{c.get('slug')}: no subcategories" for c in cats if not c.get("subcategories")]
    base = set(categories.subcategories("base"))
    errors += [f"{s.get('slug')}: base_related {r!r} is not a base subcategory" for c in cats
               for s in c.get("subcategories") or [] for r in s.get("base_related") or [] if r not in base]
    return errors + ([] if cats else ["no categories"])


def apply_taxonomy(bundle, src, d):
    """Writes the bundle's categories.json and its names files (stale entries dropped, missing ones drafted)."""
    p = load_json(src)
    if p is None:
        sys.exit(f"{src}: not found")
    if errors := taxonomy_errors(p, bundle):
        sys.exit(f"{src}: " + "; ".join(errors))
    subs = write_taxonomy(bundle, p, d)
    if bundle_row(bundle)["kind"] == "theme":
        rel = {s["slug"]: s.get("base_related") or [] for c in p["categories"] for s in c["subcategories"]}
        save_json(layout.base_related(bundle), {"about": BASE_RELATED_ABOUT, "subcategories": rel})
        print(f"{layout.base_related(bundle).relative_to(ROOT)}: {sum(map(bool, rel.values()))} of {len(rel)} "
              "subcategories go beyond base's")
    if found := off_list(bundle, set(subs)):
        print(f"{sum(sum(c.values()) for c in found.values())} {bundle} question(s) on subcategories not in the list "
              f"(`qgen remap --bundle {bundle}` moves them):\n" + "\n".join(off_list_lines(found)))
    errors, _ = validate_pool()
    if errors:
        print(f"qgen validate fails ({len(errors)} error(s)); expected only for questions on subcategories not in "
              f"the list:\n" + "\n".join(f"  {e}" for e in errors[:20]))


def draft_names(bundle, todo, d):
    """Fills each entry's missing names ({locale: name}) in names.{en,es,de}.json's locales, from its English
    name where it has one, else from its name in the bundle's language."""
    b = bundle_row(bundle)
    by_src = {}
    for i, e in enumerate(todo):
        by_src.setdefault("en" if "en" in e["names"] else next(iter(e["names"])), []).append((str(i), e))
    for src, items in by_src.items():
        locales = [l for l in categories.NAMES_LOCALES if any(l not in e["names"] for _, e in items)]
        rows = [{"key": k, "name": e["names"][src], "scope": e.get("scope", "")} for k, e in items]
        schema = {"type": "object", "required": ["items"], "properties": {"items": {"type": "array", "items": {
            "type": "object", "required": ["key", *locales], "properties": {"key": STR, **{l: STR for l in locales}}}}}}
        vl = names_locale(voice_locale(b))
        voice = f"\n\n## Voice\n`{vl}`: {b['voice']}" if b.get("voice") and vl in locales else ""
        user = ("## Target languages\n" + "\n".join(f"- `{l}`: {'Spanish (Latin America and Spain)' if l == 'es' else LANGUAGES[l]}"
                                                for l in locales) + voice
                + "\n\n## Names\n" + json.dumps(rows, ensure_ascii=False, indent=1))
        system = (PROMPTS / "taxonomy-names.md").read_text(encoding="utf-8").replace("{source}", LANGUAGES[src])
        got = {r["key"]: r for r in claude(system, user, schema, NAMES_MODEL, d)["items"]}
        if missing := [e["names"][src] for k, e in items if k not in got]:
            sys.exit(f"nothing written; no names drafted for {', '.join(missing)}: rerun")
        for k, e in items:
            e["names"] = {l: got[k][l] for l in locales} | e["names"]


def write_taxonomy(bundle, p, d):
    """categories.json (structure only) and names.{en,es,de}.json from a proposal (decision 259): an entry's `en` and
    `name` (the bundle's language) win over the names files, missing names are drafted; an entry without `slug`
    (a remap's new one) gets one from its English name. `scope` only needed for drafted names. Returns the subcategories."""
    own = names_locale(translations.draft_locale(bundle_row(bundle)))
    files = {l: load_json(layout.NAMES(l, bundle)) or {"version": 1, "locale": l} for l in categories.NAMES_LOCALES}
    entries = {k: [] for k in categories.NAME_KINDS}
    for c in p["categories"]:
        entries["categories"].append(c)
        entries["subcategories"] += c["subcategories"]
    for k, es in entries.items():
        for e in es:
            have = {l: n for l in files if e.get("slug") and (n := (files[l].get(k) or {}).get(e["slug"]))}
            e["names"] = have | {l: v for l, v in [("en", e.get("en")), (own, e.get("name"))] if v}
            if not e["names"]:
                e["names"] = {own: e["slug"]}
    draft_names(bundle, [e for es in entries.values() for e in es if len(e["names"]) < len(files)], d)
    for es in entries.values():
        used = {e["slug"] for e in es if e.get("slug")}
        for e in es:
            if not e.get("slug"):
                s = base_ = derived_slug(e["names"]["en"], p.get("region") or bundle)
                n = 1
                while s in used:
                    n += 1
                    s = f"{base_}-{n}"
                used.add(e.setdefault("slug", s))
    path = categories.path(bundle)
    doc = load_json(path, {})
    cats = [{"slug": c["slug"], "subcategories": [s["slug"] for s in c["subcategories"]]} for c in p["categories"]]
    save_json(path, {"about": doc.get("about") or CATEGORIES_ABOUT.format(bundle=bundle), "categories": cats})
    subs = [s for c in cats for s in c["subcategories"]]
    print(f"{path.relative_to(ROOT)}: {len(cats)} categories, {len(subs)} subcategories")
    for l, f in files.items():
        changed = stale = 0
        for k, es in entries.items():
            have = f.get(k) or {}
            stale += len(set(have) - {e["slug"] for e in es})
            changed += sum(have.get(e["slug"]) != e["names"][l] for e in es)
            f[k] = {e["slug"]: e["names"][l] for e in es}
        save_json(layout.NAMES(l, bundle), f)
        print(f"{layout.NAMES(l, bundle).relative_to(ROOT)}: {changed} name(s) new or changed, {stale} dropped")
    return subs


REMAP_SCHEMA = {"type": "object", "required": ["questions", "lists"], "properties": {
    "questions": {"type": "array", "items": {"type": "object", "required": ["id", "subcategory", "category", "scope", "reason"],
                                            "properties": {"id": STR, "subcategory": STR, "category": STR, "scope": STR, "reason": STR}}},
    "lists": {"type": "array", "items": {"type": "object", "required": ["subcategory", "target", "reason"],
                                        "properties": {"subcategory": STR, "target": STR, "reason": STR}}}}}


def old_lists(bundle, subs):
    """{subcategory: list} of the bundle's concept lists whose subcategory is not in subs."""
    out = {}
    for p in sorted(concepts.concepts_dir(bundle).glob("*.json")):
        lst = load_json(p)
        if lst.get("subcategory") not in subs:
            out[lst.get("subcategory") or p.stem] = lst
    return out


def remap_errors(p, bundle):
    """Problems of a remap proposal against the bundle's list; new subcategories must agree across questions."""
    loc = translations.draft_locale(bundle_row(bundle))
    subs, cats = set(categories.subcategories(bundle)), {cat_name(c, loc) for c in categories.load(bundle)}
    ids = {q["id"] for q in load_json(POOL)["questions"] if q.get("bundle") == bundle}
    got = {r["id"] for r in p["questions"]}
    errors = [f"no subcategory for {', '.join(sorted(ids - got))}"] if ids - got else []
    errors += [f"{i}: not a {bundle} question" for i in sorted(got - ids)]
    new = {}
    for r in p["questions"]:
        if r["subcategory"] in subs:
            continue
        if not (r["category"].strip() and r["scope"].strip()):
            errors.append(f"{r['id']}: {r['subcategory']!r} is not in the list and has no category and scope")
        elif new.setdefault(r["subcategory"], r["category"]) != r["category"]:
            errors.append(f"{r['subcategory']!r}: in two categories")
    targets_ = subs | set(new)
    errors += [f"list {x['subcategory']!r}: target {x['target']!r} is not a subcategory" for x in p["lists"]
               if x["target"] and x["target"] not in targets_]
    return errors, new, cats


def remap_md(p, new, cats, by_id):
    lines = [f"# Remap proposal: `{p['bundle']}`", "", f"{len(p['questions'])} questions; "
             f"{sum(r['subcategory'] != by_id[r['id']]['subcategory'] for r in p['questions'] if r['id'] in by_id)} change subcategory.", ""]
    if new:
        lines += ["## Additions"] + [f"- {s} → {c}{'' if c in cats else ' (new category)'}" for s, c in sorted(new.items())] + [""]
    lines += ["## Questions"]
    for r in sorted((r for r in p["questions"] if r["id"] in by_id), key=lambda r: (r["subcategory"], r["id"])):
        q = by_id[r["id"]]
        lines.append(f"- {r['id']} ({q['status']}) {q['subcategory']} → **{r['subcategory']}**: {q['question'][:80]} "
                     f"→ {q['answer']}" + (f" ({r['reason']})" if r["reason"] else ""))
    lines += ["", "## Old concept lists"] + [f"- {x['subcategory']} → {x['target'] or 'deleted'} ({x['reason']})" for x in p["lists"]]
    return "\n".join(lines) + "\n"


def cmd_remap(args):
    """A regional bundle's questions onto its new taxonomy (plan 138, decision 166): one opus call proposes a
    subcategory per question (all statuses) and a target for every concept list whose subcategory is gone
    → work/remap/<id>/proposal.{json,md}; `--apply <proposal.json>` adds new subcategories to categories.json
    (names drafted), renames or deletes old concept lists, moves the questions and their concepts (BN-13)."""
    b = next((x for x in load_bundles() if x["id"] == args.bundle), None)
    if not b or b["kind"] != "region":
        sys.exit(f"{args.bundle!r} is not a regional bundle in app/data/bundles.json")
    d = WORK / "remap" / args.bundle
    d.mkdir(parents=True, exist_ok=True)
    if args.apply:
        return apply_remap(args, Path(args.apply), d)
    subs = categories.subcategories(args.bundle)
    tx = load_json(WORK / "taxonomy" / args.bundle / "proposal.json", {}) or {}
    scopes = {s.get("slug") or s["name"]: s["scope"] for c in tx.get("categories", []) for s in c["subcategories"]}
    qs = [q for q in load_json(POOL)["questions"] if q.get("bundle") == args.bundle]
    lists = old_lists(args.bundle, set(subs))
    loc = translations.draft_locale(b)
    shown = lambda s: categories.display(args.bundle, s, loc) if s in subs else categories.display("base", s, loc)
    user = "\n\n".join([
        f"## Bundle\n`{args.bundle}`: {b['name']}\n{bundle_text(args.bundle, loc)}",
        "## New list\n" + "\n".join(f"### {cat_name(c, loc)}\n" + "\n".join(
            f"- {shown(s)}" + (f": {sc}" if (sc := scopes.get(s) or scopes.get(shown(s))) else "")
            for s in c["subcategories"]) for c in categories.load(args.bundle)),
        "## Questions\n" + json.dumps([{k: q.get(k) for k in ["id", "question", "answer", "hints", "concept"]}
                                       | {"subcategory": shown(q["subcategory"])} for q in qs], ensure_ascii=False),
        "## Old concept lists\n" + (json.dumps([{"subcategory": shown(s), "facets": l.get("facets", []), "concepts": len(l["concepts"]),
                                                 "examples": [c["name"] for c in l["concepts"][:25]]}
                                                for s, l in lists.items()], ensure_ascii=False) if lists else "none")])
    out = claude((PROMPTS / "remap.md").read_text(encoding="utf-8"), user, REMAP_SCHEMA, args.model, d)
    for r in out["questions"]:  # names back to keys; a new subcategory keeps its name
        r["subcategory"] = categories.resolve(args.bundle, r["subcategory"]) or r["subcategory"]
    by_name = {shown(s): s for s in lists}
    for x in out["lists"]:
        x["subcategory"] = by_name.get(x["subcategory"], x["subcategory"])
        x["target"] = x["target"] and (categories.resolve(args.bundle, x["target"]) or x["target"])
    p = {"bundle": args.bundle, **out}
    save_json(d / "proposal.json", p)
    errors, new, cats = remap_errors(p, args.bundle)
    (d / "proposal.md").write_text(remap_md(p, new, cats, {q["id"]: q for q in qs}), encoding="utf-8")
    print(f"{rekey.rel(d / 'proposal.md')}: {len(new)} new subcategories; then `qgen remap --bundle "
          f"{args.bundle} --apply {rekey.rel(d / 'proposal.json')}`")
    if errors:
        sys.exit("proposal has problems (edit proposal.json or rerun):\n" + "\n".join(f"  {e}" for e in errors))


def apply_remap(args, src, d):
    bundle = args.bundle
    p = load_json(src)
    if p is None or p.get("bundle") != bundle:
        sys.exit(f"{src}: no remap proposal for {bundle}")
    errors, new, cats = remap_errors(p, bundle)
    if errors:
        sys.exit(f"{src}:\n" + "\n".join(f"  {e}" for e in errors))
    lo, hi = load_age_groups()["scale"]
    data = load_json(POOL)
    sources = {}  # concept key → its entry in the list the question used before
    for q in data["questions"]:
        if q.get("bundle") == bundle and q.get("concept"):
            lst = concepts.load(*categories.key(q)) or concepts.load("base", q["subcategory"]) or {}
            sources |= {concepts.key(c["name"]): c for c in lst.get("concepts", []) if c["name"] == q["concept"]}
    if new:  # new subcategories (and categories) come as names in the bundle's language: slugs from their en names
        scope = {r["subcategory"]: r["scope"] for r in p["questions"]}
        cats_ = [{"slug": c["slug"], "scope": "", "subcategories": [{"slug": s, "scope": ""} for s in c["subcategories"]]}
                 for c in categories.load(bundle)]
        for s, c in new.items():
            cid = categories.resolve(bundle, c, "categories")
            cat = next((x for x in cats_ if (x.get("slug") == cid if cid else x.get("name") == c)), None)
            if not cat:
                cat = {"name": c, "scope": scope[s], "subcategories": []}
                cats_.append(cat)
            cat["subcategories"].append({"name": s, "scope": scope[s]})
        tx = load_json(WORK / "taxonomy" / bundle / "proposal.json", {}) or {}
        write_taxonomy(bundle, {"bundle": bundle, "region": tx.get("region"), "categories": cats_}, d)
    key_of = lambda t: t and (categories.resolve(bundle, t) or t)
    subs = set(categories.subcategories(bundle))
    for s, lst in old_lists(bundle, subs).items():
        t = key_of(next((x["target"] for x in p["lists"] if x["subcategory"] == s), ""))
        concepts.path(bundle, s).unlink()
        if not t:
            print(f"  concept list {s}: deleted ({len(lst['concepts'])} concepts)")
            continue
        have = concepts.load(bundle, t)
        if have:  # a second list for the same target: merged
            own = {concepts.key(c["name"]) for c in have["concepts"]}
            have["concepts"] += [c for c in lst["concepts"] if concepts.key(c["name"]) not in own]
            have["facets"] += [f for f in lst.get("facets", []) if f not in have["facets"]]
            lst = have
        concepts.save(bundle, t, {**lst, "subcategory": t})
        print(f"  concept list {s} → {t}")
    moved, kept, cleared = [], 0, 0
    with atomic.locked(POOL):
        data = load_json(POOL)
        target = {r["id"]: key_of(r["subcategory"]) for r in p["questions"]}
        for q in data["questions"]:
            if q.get("bundle") != bundle:
                continue
            if q["subcategory"] != target[q["id"]]:
                moved.append(f"{q['id']}: {q['subcategory']} → {target[q['id']]}")
                q["subcategory"] = target[q["id"]]
            if not q.get("concept"):
                continue
            lst = concepts.load(bundle, q["subcategory"])
            if lst is None:
                q.pop("concept")
                cleared += 1
                continue
            k = concepts.key(q["concept"])
            if same := next((c["name"] for c in lst["concepts"] if concepts.key(c["name"]) == k), None):
                q["concept"] = same
            else:
                src_ = sources.get(k, {})
                facet = src_.get("facet") or (lst.get("facets") or ["general"])[0]
                if facet not in lst.setdefault("facets", []):
                    lst["facets"].append(facet)
                lst["concepts"].append({"name": q["concept"], "facet": facet,
                                        "known_at": min(hi, max(lo, src_.get("known_at") or q["difficulty"]))})
                concepts.save(bundle, q["subcategory"], lst)
            kept += 1
        save_json(POOL, data)
        cmd_export(args)
    print("\n".join(f"  {m}" for m in moved))
    print(f"{len(moved)} question(s) moved, {len(new)} subcategories added; concepts: {kept} kept, {cleared} cleared (BN-13)")


# the other command groups, after everything here is defined (they import each other)
from translate import LANGUAGES  # authoring/tools/translate.py
from validate import BUNDLE_ICONS, COUNTRY, validate_pool  # authoring/tools/validate.py
