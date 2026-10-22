"""`qgen validate`: checks of the source pool and its export (QP-7). Never ships (D-35)."""
import json, re, subprocess, sys

import layout  # paths (D-35)
from layout import REPO as ROOT, SOURCE_POOL as POOL, WORK
import age_groups  # authoring/tools/age_groups.py: level ranges per group (plan 27)
import concepts  # authoring/tools/concepts.py: concept lists and question axes (D-37)
import categories  # authoring/tools/categories.py: every bundle's categories (D-19, D-43)
import media_cache as media  # authoring/tools/media_cache.py: the media cache (D-17)
import providers  # authoring/tools/providers/: where candidates come from (D-45)
import targets  # authoring/tools/targets.py: pool targets (D-53)
import pool_export  # authoring/tools/pool_export.py (D-35)
import patch_notes  # authoring/tools/patch_notes.py: `qgen patch-notes` (plan 96)
import translations  # authoring/tools/translations.py: translated questions (D-81)
import demo  # authoring/tools/demo.py: `qgen demo` (plan 174)

from qgen import PROBLEMS, check_question_shape, load_age_groups, load_bundles, load_json, natural_key  # authoring/tools/qgen.py


def validate_pool():
    """(errors, warnings) for the whole source pool and its export (QP-7)."""
    data = load_json(POOL)
    errors, warnings, ids, unlicensed = [], [], set(), []
    subcategories = categories.broad_of()
    lists = {}
    axes_of = {b: concepts.load_axes(b) for b in categories.bundle_ids()}
    lo, hi = load_age_groups()["scale"]
    bundles = load_bundles()
    bundle_ids = {b["id"] for b in bundles}
    bundle_of = {b["id"]: b for b in bundles}
    errors += taxonomy_problems()
    errors += slug_problems()
    e, w = bundle_problems(bundles)
    errors += e
    warnings += w
    errors += age_groups.level_problems(load_age_groups())
    errors += targets.problems((lo, hi), bundles)
    import health  # authoring/tools/health.py (imports qgen)
    errors += targets.health_problems(health.THRESHOLDABLE)
    errors += targets.quality_problems()
    errors += spot_check_problems(data["questions"], (lo, hi))
    errors += english_keys_problems(data["questions"])
    for q in data["questions"]:
        qid = q.get("id", "?")
        for k in ["id", "status", "subcategory", "difficulty", "description", "question", "answer",
                  "wrong_answers", "hints", "media", "fun_fact"]:
            if k not in q: errors.append(f"{qid}: missing {k}")
        if qid in ids: errors.append(f"{qid}: duplicate id")
        ids.add(qid)
        if q.get("status") not in {"draft", "approved", "rejected", "needs_work"}: errors.append(f"{qid}: bad status")
        errors += [f"{qid}: {p}" for p in review_problems(q)]
        errors += [f"{qid}: {p}" for p in source_locale_problems(q, bundle_of.get(q.get("bundle")))]
        if "translatable" in q and q["translatable"] is not False: errors.append(f"{qid}: translatable must be false when set (absent = translatable, D-81)")
        key = categories.key(q)
        if key not in subcategories:
            errors.append(f"{qid}: subcategory not in its bundle's categories (D-19, D-49, D-99, D-109)")
        if q.get("bundle") not in bundle_ids: errors.append(f"{qid}: bundle must be one of app/data/bundles.json (D-39)")
        m = q.get("media", {})
        if m.get("type") not in {"image", "audio", "video"} or m.get("role") not in {"decorative", "illustrative", "essential"}:
            errors.append(f"{qid}: bad media type/role")
        bg = q.get("background")
        if (bg is not None) != (m.get("type") == "audio"):
            errors.append(f"{qid}: background must be set exactly for audio questions (D-14)")
        if q.get("status") == "approved":  # warnings only: media/ is a cache (D-17)
            for label, slot in [("media", m), ("background", bg)]:
                if slot is None:
                    continue
                if not slot.get("file_url"):
                    warnings.append(f"{qid}: approved but no {label} picked")
                elif not media.cache_path(slot["file_url"]).is_file():
                    warnings.append(f"{qid}: {label} not cached")
                verdict, reasons = providers.licence_verdict(slot) if slot.get("file_url") else ("ok", [])
                if verdict == "replace":  # plans/26, plans/53
                    unlicensed.append(f"{qid} {label} ({'; '.join(reasons)})")
        if all(k in q for k in ["wrong_answers", "hints", "difficulty", "answer"]):
            errors += [f"{qid}: {p}" for p in check_question_shape(q)]
        if q.get("axes") is not None:  # D-37
            e, w = concepts.axes_problems(q["axes"], axes_of.get(key[0], axes_of["base"]))
            errors += [f"{qid}: {p}" for p in e]
            warnings += [f"{qid}: {p}" for p in w]
        if q.get("concept") is not None and isinstance(q.get("subcategory"), str):
            if key not in lists:
                lists[key] = {c["name"] for c in (concepts.load(*key) or {}).get("concepts", [])}
            if q["concept"] not in lists[key]:
                errors.append(f"{qid}: concept {q['concept']!r} is not in {key[1]}'s concept list ({key[0]})")
    for b, sub in subcategories:
        lst = concepts.load(b, sub)
        keys = [concepts.key(c["name"]) for c in (lst or {}).get("concepts", [])]
        dup = sorted({k for k in keys if keys.count(k) > 1})
        if dup:
            errors.append(f"{concepts.path(b, sub).relative_to(ROOT)}: same concept twice: {', '.join(dup)}")
        bad = [c["name"] for c in (lst or {}).get("concepts", [])
               if not isinstance(c.get("known_at"), int) or not lo <= c["known_at"] <= hi]
        if bad:
            errors.append(f"{concepts.path(b, sub).relative_to(ROOT)}: known_at missing or not {lo}–{hi} (D-38): {first_ids(bad)}")
    if unlicensed:
        errors.append(f"{len(unlicensed)} approved pick(s) on the licence replace list (needs_work and a new file, decision 47): {first_ids(unlicensed)}")
    e, w = translation_problems(data)
    errors += e
    warnings += w
    for path, text in pool_export.exports(data).items():
        if (path.read_text(encoding="utf-8") if path.exists() else None) != text:
            errors.append(f"{path.relative_to(ROOT)} is not the current export of the pool: run `qgen export`")
    for p in pool_export.stale_packs(pool_export.exports(data)):
        errors.append(f"{p.relative_to(ROOT)}: not written by `qgen export` (pack without questions); delete it")
    for l in translations.LOCALES:
        if layout.LOCALE_POOL(l).exists() and not translations.exported(l, data):
            errors.append(f"{layout.LOCALE_POOL(l).relative_to(ROOT)}: no {l} source or translation; delete it")
    e, w = demo_problems(data)
    errors += e
    warnings += w
    tag, released = released_ids()
    gone = sorted(released - ids, key=natural_key) if tag else []
    if gone:
        errors.append(f"{len(gone)} id(s) of {tag}'s pool missing from authoring/data/questions.json "
                      f"(drop = status change, never deletion; plan 91): {', '.join(gone)}")
    return errors, warnings


def demo_problems(data):
    """(errors, warnings) for the demo list (decision 339) and its pools; none without a list."""
    texts = pool_export.demo_exports(data)
    if not layout.DEMO_LIST.exists():
        return [f"{p.relative_to(ROOT)}: no {layout.DEMO_LIST.relative_to(ROOT)}; delete it" for p in pool_export.stale_demo(texts)], []
    doc = load_json(layout.DEMO_LIST)
    rel = layout.DEMO_LIST.relative_to(ROOT)
    by_id = {q["id"]: q for q in data["questions"]}
    errors = [f"{rel}: {i} is not in the pool" for i in doc["ids"] if i not in by_id]
    errors += [f"{rel}: {i} is not a base question" for i in doc["ids"] if i in by_id and (by_id[i].get("bundle") or "base") != "base"]
    if not errors:
        e, w, _ = demo.problems(doc, data["questions"])
        errors += [f"{rel}: {m}" for m in e]
        warnings = [f"{rel}: {m}" for m in w]
    else:
        warnings = []
    for path, text in texts.items():
        if (path.read_text(encoding="utf-8") if path.exists() else None) != text:
            errors.append(f"{path.relative_to(ROOT)} is not the current export of the demo list: run `qgen export`")
    for p in pool_export.stale_demo(texts):
        errors.append(f"{p.relative_to(ROOT)}: not written by `qgen export`; delete it")
    return errors, warnings


def released_ids():
    """(newest v* tag, ids in its app/data/[bundles/<id>/]pool*.json), or (None, None) without a tag or git (plan 91)."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    try:
        tags = git("tag", "--list", "v*", "--sort=-v:refname").stdout.split()
    except OSError:
        return None, None
    if not tags:
        return None, None
    files = git("ls-tree", "-r", "--name-only", tags[0], "app/data/").stdout.split()
    ids = set()
    for f in files:
        if re.fullmatch(r"app/data/(bundles/[^/]+/)?pool(\.[A-Za-z-]+)?\.json", f):
            ids |= {q["id"] for q in json.loads(git("show", f"{tags[0]}:{f}").stdout)["questions"]}
    return tags[0], ids


def source_locale_problems(q, bundle):
    """A source's locale (decision 235): known; base from batch-9 on en; a regional bundle's in its region's
    language, the first of its languages (decision 110)."""
    loc, out = translations.source_locale(q), []
    if loc not in translations.LOCALES:
        return [f"locale must be one of {', '.join(translations.LOCALES)}"]
    m = re.fullmatch(r"batch-(\d+)", q.get("batch") or "")
    if bundle and bundle["kind"] == "base" and m and int(m.group(1)) >= translations.ENGLISH_FROM and loc != "en":
        out.append(f"locale must be en: base drafts in English from batch-{translations.ENGLISH_FROM} on (plan 148)")
    if bundle and bundle["kind"] in {"region", "theme"} and loc != (want := translations.draft_locale(bundle)):
        out.append(f"locale must be {want}, {bundle['id']}'s " + ("language (decision 110)" if bundle["kind"] == "region"
                                                                else "draft language (decision 236)"))
    return out


def review_problems(q):
    """A question's or translation's review vs. its status (D-33, plan 15)."""
    rv, out = q.get("review"), []
    if rv is None:
        return out
    if rv.get("decision") != q.get("status") or "feedback" not in rv or "reviewed_on" not in rv:
        out.append("review does not match status")
    if not set(rv.get("problems") or []) <= set(PROBLEMS):
        out.append(f"review.problems must be from {', '.join(PROBLEMS)}")
    if rv.get("reviewer") not in {"human", "llm"}: out.append("review.reviewer must be human or llm")
    if (rv.get("reviewer") == "llm") != bool(rv.get("model")): out.append("review.model must be set exactly for an llm review")
    prev = rv.get("previous")
    if prev is not None and (prev.get("reviewer") not in {"human", "llm"}
                             or rv.get("reviewer") == "human" and prev.get("reviewer") != "llm"):
        out.append("review.previous must be a review, an llm one under a human one")
    return out


def first_ids(ids, n=5):
    return f"{', '.join(ids[:n])}{' …' if len(ids) > n else ''}"


def translation_problems(data):
    """(errors, warnings) for authoring/data/questions.<locale>.json and the names files (D-81)."""
    errors, warnings = [], []
    src = {q.get("id"): q for q in data["questions"]}
    for p in sorted(layout.translations("*").parent.glob("questions.*.json")):
        if p.name.split(".")[1] not in translations.LOCALES:
            errors.append(f"{p.relative_to(ROOT)}: locale not in {', '.join(translations.LOCALES)} (D-78)")
    for l in translations.LOCALES:
        p = translations.path(l)
        if not p.exists():
            continue
        rel, doc = p.relative_to(ROOT), translations.load(l)
        if doc.get("version") != 1 or doc.get("locale") != l:
            errors.append(f"{rel}: header must be version 1, locale {l!r}")
        ids, stale, orphaned = set(), [], []
        for t in doc.get("questions", []):
            tid = t.get("id", "?")
            where = f"{rel}: {tid}"
            for k in ["id", "source_hash", "status", "difficulty", *translations.TEXT_FIELDS]:
                if k not in t: errors.append(f"{where}: missing {k}")
            if tid in ids: errors.append(f"{where}: duplicate id")
            ids.add(tid)
            q = src.get(tid)
            if q is None:
                errors.append(f"{where}: no such id in the source pool")
                continue
            if t.get("status") not in {"draft", "approved", "rejected", "needs_work"}: errors.append(f"{where}: bad status")
            errors += [f"{where}: {x}" for x in review_problems(t)]
            if all(k in t for k in ["wrong_answers", "hints", "difficulty", "answer"]):
                errors += [f"{where}: {x}" for x in check_question_shape(t)]
            if translations.source_locale(q) == l:
                errors.append(f"{where}: the source is in {l} already; delete the entry (decision 235)")
                continue
            if t.get("status") == "rejected":
                continue
            if q.get("status") == "rejected" or not translations.translatable(q):
                errors.append(f"{where}: source is rejected or translatable: false; reject the translation")
                continue
            if translations.is_stale(t, q): stale.append(tid)
            if t.get("status") == "approved" and q.get("status") != "approved": orphaned.append(tid)
        if stale:
            warnings.append(f"{rel}: {len(stale)} stale translation(s) (source text changed): {first_ids(stale)}")
        if orphaned:
            warnings.append(f"{rel}: {len(orphaned)} approved translation(s) of a source not approved: {first_ids(orphaned)}")
    return errors + names_problems(data), warnings + names_warnings(data)


def names_problems(data):
    """Errors in the names files: header, unknown keys; a name missing for what pool.<locale>.json uses."""
    errors, cats = [], categories.load()
    for l in (*translations.NAMED, "es", "es-ES"):
        for b in categories.bundle_ids():
            p = layout.NAMES(l, b)
            if not p.exists():
                continue
            rel, doc = p.relative_to(ROOT), load_json(p)
            if doc.get("version") != 1 or doc.get("locale") != l:
                errors.append(f"{rel}: header must be version 1, locale {l!r}")
            known = {"categories": {c["slug"] for c in cats if c["bundle"] == b},
                     "subcategories": set(categories.subcategories(b))}
            if b == "base" and l in translations.NAMED:  # es, es-ES: bundles.json, age-groups.json
                known["bundles"] = set(categories.bundle_ids())
                known["age_groups"] = {g["id"] for g in load_age_groups()["groups"]}
            for k in ["bundles", "age_groups"]:
                if b != "base" and k in doc:
                    errors.append(f"{rel}: {k} names go in {layout.NAMES(l).relative_to(ROOT)}")
            for k, keys in known.items():
                names = doc.get(k) or {}
                bad = sorted(set(names) - keys)
                if bad:
                    errors.append(f"{rel}: {k} not in the categories/bundles/age-groups files: {first_ids(bad)}")
                empty = sorted(n for n, v in names.items() if not name_ok(v, k == "bundles"))
                if empty:
                    errors.append(f"{rel}: {k} with an empty or malformed name: {first_ids(empty)}")
        if l not in translations.NAMED or not translations.exported(l, data):
            continue
        names, broad = categories.load_names(l), categories.broad_of()
        missing = set()
        for e in translations.play_entries(l, data):
            b, sub = categories.key(e)
            if categories.sub_key(b, sub) not in names["subcategories"]: missing.add(f"subcategory {categories.sub_key(b, sub)}")
            c = broad.get((b, sub))
            if c and categories.sub_key(b, c["slug"]) not in names["categories"]: missing.add(f"category {categories.sub_key(b, c['slug'])}")
            if e["bundle"] not in names["bundles"]: missing.add(f"bundle {e['bundle']}")
        if missing:
            errors.append(f"{l}: pool.{l}.json uses names missing in names.{l}.json: {first_ids(sorted(missing))}")
    return errors


def name_ok(v, bundle):
    """A non-empty string; a bundle's is {"name", "description"}."""
    if bundle:
        return isinstance(v, dict) and all(isinstance(v.get(k), str) and v[k].strip() for k in ["name", "description"])
    return isinstance(v, str) and bool(v.strip())


def names_warnings(data):
    """Missing names per locale, once the locale has a pool or a names file."""
    out, cats = [], categories.load()
    for l in translations.NAMED:
        if not (translations.exported(l, data) or any(layout.NAMES(l, b).exists() for b in categories.bundle_ids())):
            continue
        names = categories.load_names(l)
        n = (len(set(categories.bundle_ids()) - set(names["bundles"]))
             + len({categories.sub_key(c["bundle"], c["slug"]) for c in cats} - set(names["categories"]))
             + len({categories.sub_key(c["bundle"], s) for c in cats for s in c["subcategories"]} - set(names["subcategories"]))
             + len({g["id"] for g in load_age_groups()["groups"]} - set(names["age_groups"])))
        if n:
            out.append(f"{l}: {n} bundle/category/subcategory/age-group name(s) missing in the names.{l}.json files")
    return out


def english_keys_problems(questions):
    """Shape of authoring/data/english-keys.json (decision 232): version 1; per pool id a 12-hex hash, an answer
    and a concept (string or null). Stale entries are fine: the next `qgen english-keys` drops them."""
    doc = load_json(layout.ENGLISH_KEYS)
    if doc is None:
        return []
    rel = "authoring/data/english-keys.json"
    if doc.get("version") != 1 or not isinstance(doc.get("questions"), dict):
        return [f"{rel}: needs version 1 and a questions object"]
    ids, out = {q["id"] for q in questions}, []
    for i, k in doc["questions"].items():
        if i not in ids:
            out.append(f"{rel}: {i}: not in the pool")
        elif not (isinstance(k, dict) and set(k) == {"hash", "answer", "concept"}
                  and isinstance(k["hash"], str) and re.fullmatch(r"[0-9a-f]{12}", k["hash"])
                  and isinstance(k["answer"], str) and k["answer"].strip()
                  and (k["concept"] is None or isinstance(k["concept"], str))):
            out.append(f"{rel}: {i}: needs hash (12 hex), answer and concept (string or null)")
    return out


def run_ids(run):
    """The ids of a back-audit (plan 57) or neutralize run (plan 64), or None for any other name.
    work/<run>/run.json, else the run's "ids" in spot-checks.json (tracked, for a checkout without work/)."""
    m = re.fullmatch(r"(backaudit|neutralize)-\d+", run)
    if not m:
        return None
    cfg = load_json(WORK / run / "run.json", {}) or {}
    if cfg.get("mode") == m.group(1):
        return cfg.get("ids")
    return ((load_json(layout.SPOT_CHECKS, {}) or {}).get(run) or {}).get("ids")


def spot_check_problems(questions, scale):
    """Errors in authoring/data/spot-checks.json (plan 16): batches (or back-audit, neutralize runs) and ids exist, values in range;
    a translation run's (tr-<locale>-<n>) items are its translations, with "locale" (plan 67);
    a back-audit or neutralize run's members are its entry's "ids", never work/ (gitignored)."""
    checks = load_json(layout.SPOT_CHECKS)
    if checks is None:
        return []
    rel, out = "authoring/data/spot-checks.json", []
    pool_batches = {q["id"]: q.get("batch") for q in questions}
    tr_batches = {}  # locale -> {id: batch} of its translations (plan 67)
    decisions, (lo, hi) = {"approved", "needs_work", "rejected"}, scale
    for b, entry in checks.items():
        locale = translations.run_locale(b)
        if locale and locale not in tr_batches:
            tr_batches[locale] = {t["id"]: t.get("batch") for t in translations.load(locale)["questions"]}
        batch_of = tr_batches[locale] if locale else pool_batches
        if re.fullmatch(r"(backaudit|neutralize)-\d+", b):
            if not (isinstance(entry.get("ids"), list) and entry["ids"]):
                out.append(f"{rel}: {b}: needs its run's ids")
                continue
            batch_of = {i: b for i in entry["ids"]}
        if b not in batch_of.values():
            out.append(f"{rel}: no batch {b!r} in {f'questions.{locale}.json' if locale else 'the pool'}")
            continue
        if not isinstance(entry.get("size"), int) or entry["size"] < 1 or entry.get("seed") != b:
            out.append(f"{rel}: {b}: size must be an integer ≥ 1 and seed the batch name")
        for i, it in (entry.get("items") or {}).items():
            bad = [k for k, ok in [
                ("id", batch_of.get(i) == b),
                ("llm", it.get("llm") in decisions), ("human", it.get("human") in decisions),
                ("audit", it.get("audit") in {"ok", "problem", None}),
                ("problems", isinstance(it.get("problems"), list) and set(it["problems"]) <= set(PROBLEMS)),
                ("difficulty", isinstance(it.get("difficulty"), list) and len(it["difficulty"]) == 2
                 and all(isinstance(d, int) and lo <= d <= hi for d in it["difficulty"])),
                ("media_changed", isinstance(it.get("media_changed"), bool)),
                ("locale", it.get("locale") == locale),
                ("on", isinstance(it.get("on"), str) and re.fullmatch(r"\d{4}-\d\d-\d\d", it["on"]))] if not ok]
            if bad:
                out.append(f"{rel}: {b}: {i}: bad {', '.join(bad)}")
    return out


def taxonomy_problems():
    """Every bundle's categories file belongs to a bundle; names and slugs are unique within a bundle (D-43, D-99);
    a theme's base-related.json names its own and base's subcategories (plan 184)."""
    errors, ids = [], categories.bundle_ids()
    if ids[:1] != ["base"]:
        errors.append("app/data/bundles.json: base must come first")
    for p in sorted(layout.app_paths.BUNDLE_DATA.glob("*/categories.json")):
        if p.parent.name not in ids or p.parent.name == "base":
            errors.append(f"{p.relative_to(ROOT)}: no bundle {p.parent.name!r} in app/data/bundles.json")
    for b in ids:
        for what, items in [("subcategory", categories.subcategories(b)), ("category slug", [c["slug"] for c in categories.load(b)])]:
            dup = sorted({x for x in items if items.count(x) > 1})
            if dup:
                errors.append(f"{categories.path(b).relative_to(ROOT)}: same {what} twice (D-99): {', '.join(dup)}")
    rel = layout.REGIONAL_CATEGORIES.relative_to(ROOT)
    regional = (load_json(layout.REGIONAL_CATEGORIES, {}) or {}).get("categories", [])
    names = [c.get("name") for c in regional]
    if not all(isinstance(n, str) and n and c.get("scope") and c.get("excludes") for n, c in zip(names, regional)):
        errors.append(f"{rel}: every category needs name, scope and excludes (decision 213)")
    if dup := sorted({n for n in names if isinstance(n, str) and names.count(n) > 1}):
        errors.append(f"{rel}: same name twice: {', '.join(dup)}")
    slugs = [c["slug"] for c in regional if "slug" in c]
    if slugs and (len(slugs) < len(regional) or len(set(slugs)) < len(slugs)
                  or not all(isinstance(s, str) and categories.SLUG.fullmatch(s) for s in slugs)):
        errors.append(f"{rel}: every category needs its own slug (decision 259)")
    base = set(categories.subcategories("base"))
    for b in ids:
        f, own = layout.base_related(b), set(categories.subcategories(b))
        for s, rs in ((load_json(f, {}) or {}).get("subcategories") or {}).items():
            if s not in own:
                errors.append(f"{f.relative_to(ROOT)}: {s!r} is not a {b} subcategory")
            errors += [f"{f.relative_to(ROOT)}: {s}: {r!r} is not a base subcategory" for r in rs if r not in base]
    return errors


def slug_problems():
    """The slug rule (decision 259), on once names.es.json exists: keys are slugs, categories.json holds no names,
    names.{en,es,de}.json name every category and subcategory of every bundle (questions: validate_pool's key check)."""
    if not categories.slug_keys():
        return []
    errors = []
    for b in categories.bundle_ids():
        cats = categories.load(b)
        rel = categories.path(b).relative_to(ROOT)
        if bad := [c["slug"] for c in cats if not categories.SLUG.fullmatch(c["slug"])] + \
                  [s for s in categories.subcategories(b) if not (isinstance(s, str) and categories.SLUG.fullmatch(s))]:
            errors.append(f"{rel}: not a slug (decision 259): {first_ids(bad)}")
        if named_ := [c["slug"] for c in cats if "name" in c]:
            errors.append(f"{rel}: names go in the names files, not categories.json (decision 259): {first_ids(named_)}")
        for l in categories.NAMES_LOCALES:
            doc = load_json(layout.NAMES(l, b), {}) or {}
            missing = ([f"category {c['slug']}" for c in cats if c["slug"] not in (doc.get("categories") or {})]
                       + [f"subcategory {s}" for s in categories.subcategories(b) if s not in (doc.get("subcategories") or {})])
            if missing:
                errors.append(f"{layout.NAMES(l, b).relative_to(ROOT)}: {len(missing)} name(s) missing: {first_ids(missing)}")
    return errors


COUNTRY = r"[A-Z]{2}"  # a regional bundle's country (plan 151); COUNTRY in app/client/src/engine/pool.ts
BUNDLE_ICONS = ["book", "pin", "puzzle", "flask", "ball", "scroll", "reel", "globe", "film", "heart", "mic", "headphones"]  # BUNDLE_ICONS in app/client/src/engine/pool.ts (decision 367)


def bundle_problems(bundles):
    """(errors, warnings): bundle languages and base bundles (plan 71)."""
    errors, warnings, rel = [], [], "app/data/bundles.json"
    for b in bundles:
        bid, langs = b.get("id", "?"), b.get("languages")
        if not (isinstance(langs, list) and langs and len(set(langs)) == len(langs) and set(langs) <= set(translations.LOCALES)):
            errors.append(f"{rel}: {bid}: languages must be a non-empty list of distinct codes from {', '.join(translations.LOCALES)}")
        if "always_on" in b:
            errors.append(f"{rel}: {bid}: always_on is gone; kind base marks a base bundle")
        if b.get("kind") not in {"base", "region", "theme"}:
            errors.append(f"{rel}: {bid}: kind must be base, region or theme")
        if b.get("kind") == "region" and not re.fullmatch(COUNTRY, str(b.get("country", ""))):
            errors.append(f"{rel}: {bid}: a regional bundle needs country, ISO 3166-1 alpha-2 in capitals (e.g. CO)")
        if b.get("kind") != "region" and "country" in b:
            errors.append(f"{rel}: {bid}: country only on a regional bundle")
        if "icon" in b and b.get("kind") == "region":
            errors.append(f"{rel}: {bid}: icon not on a regional bundle (its flag is the icon)")
        elif "icon" in b and b["icon"] not in BUNDLE_ICONS:
            errors.append(f"{rel}: {bid}: icon must be one of {', '.join(BUNDLE_ICONS)}")
    listed = {l: {b["id"] for b in bundles if l in (b.get("languages") or [])} for l in translations.LOCALES}
    for l in translations.LOCALES:
        path = layout.POOL_FILE(l, "base")
        if not (listed[l] or path.exists()):  # a locale without pool nor bundle, e.g. es-ES before its pool
            continue
        if not any(b.get("kind") == "base" and b["id"] in listed[l] for b in bundles):
            errors.append(f"{rel}: no base bundle for {l}")
        if l not in patch_notes.EVENT:
            errors.append(f"authoring/tools/patch_notes.py: no Steam event texts (EVENT) for {l}")
        missing = {b for b in listed[l] if not layout.POOL_FILE(l, b).exists()}
        warnings += [f"{layout.POOL_FILE(l, b).relative_to(ROOT)}: missing; {b} is listed for {l}" for b in sorted(missing)]
        pool = [q for p in layout.POOL_FILES() if p.name == path.name for q in load_json(p)["questions"]]
        have = {q.get("bundle") or "base" for q in pool if q.get("status", "approved") == "approved"}
        warnings += [f"{path.name}: no approved {b} question; {b} is listed for {l}" for b in sorted(listed[l] - have - missing)]
        warnings += [f"{path.name}: approved {b} questions, but {b} isn't listed for {l}" for b in sorted(have - listed[l])]
    return errors, warnings



def cmd_validate(args):
    errors, warnings = validate_pool()
    if warnings:
        print("\n".join(f"warning: {w}" for w in warnings))
        print(f"({len(warnings)} warning(s); `trivia-media sync --status approved` fills the cache)")
    tag, _ = released_ids()
    print(f"id continuity: checked against {tag}" if tag else "id continuity: skipped, no v* tag")
    print("\n".join(errors) or f"OK: {len(load_json(POOL)['questions'])} questions")
    sys.exit(1 if errors else 0)


# the other command groups, after everything here is defined (they import each other)
