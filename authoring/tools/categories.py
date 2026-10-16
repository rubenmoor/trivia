"""Category lists (D-19, D-43): broad categories with their subcategories, one list per bundle.

`base`'s list is app/data/categories.json; another bundle's is app/data/bundles/<id>/categories.json.
A subcategory is bundle + key, unique within a bundle only (D-99). Keys are English slugs (decision 259:
Category and subcategory keys: English slugs) with display names in names.<locale>.json; until the migration,
and in mods, a plain string is key and Spanish name, a category's `name` its name.
"""
import json
import re

from paths import BUNDLES, BUNDLE_DATA, CATEGORIES, names  # authoring/tools/paths.py


def path(bundle):
    return CATEGORIES if bundle == "base" else BUNDLE_DATA / bundle / "categories.json"


def _read(p, key=None):
    """A JSON file (its `key`); errors name the file."""
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        return doc[key] if key else doc
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"{p}: {type(e).__name__}: {e}") from e


def bundle_ids():
    """The bundles in app/data/bundles.json order (base first)."""
    return [b["id"] for b in _read(BUNDLES, "bundles")]


def load(bundle=None):
    """[{"slug", "bundle", "subcategories": [...]}, ...] (old format and mods: also "name") in display order:
    one bundle's categories, or every bundle's (None), base first. A bundle without a file has none."""
    out = []
    for b in [bundle] if bundle else bundle_ids():
        p = path(b)
        if p.exists():
            out += [{**c, "bundle": b} for c in _read(p, "categories")]
    return out


def subcategories(bundle=None):
    """Subcategory names in display order, of one bundle or of all."""
    return [s for c in load(bundle) for s in c["subcategories"]]


def key(q):
    """A question's subcategory as (bundle, key) (D-99)."""
    return (q.get("bundle") or "base", q.get("subcategory"))


def sub_key(bundle, name):
    """A subcategory's or category's key in one string, as the engine's subKey: base's bare, else <bundle>/<key>."""
    return name if bundle == "base" else f"{bundle}/{name}"


def broad_of():
    """(bundle, subcategory) -> its broad category ({"slug", "name", "bundle", ...}), across all bundles."""
    return {(c["bundle"], s): c for c in load() for s in c["subcategories"]}


def category_of(bundle, sub):
    """The broad category of the bundle's subcategory, or None."""
    return broad_of().get((bundle, sub))


NAMES_LOCALES = ("en", "es", "de")  # own names files; es-ES reads es's, then names.es-ES.json overrides
NAME_KINDS = ("categories", "subcategories")
SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


def slug_keys():
    """True once the slug migration ran (names.es.json exists): `qgen validate`'s slug rule is on."""
    return names("es").exists()


def _names_files(locale, bundle):
    """The bundle's names files for a locale, the overriding one last: es-ES reads es's, then its own."""
    return [names(l, bundle) for l in (["es", "es-ES"] if locale == "es-ES" else [locale])]


def load_names(locale):
    """{"bundles", "categories", "subcategories", "age_groups"}: display names in a locale (D-81), base's file
    merged with every bundle's; "categories" and "subcategories" keyed by sub_key (bundle + key, D-99).
    es-ES: names.es.json, then names.es-ES.json where Spain differs (decision 259)."""
    out = {"bundles": {}, "categories": {}, "subcategories": {}, "age_groups": {}}
    for b in bundle_ids():
        for p in _names_files(locale, b):
            if p.exists():
                doc = _read(p)
                for k in out:
                    keyed = k in NAME_KINDS
                    out[k].update({sub_key(b, n) if keyed else n: v for n, v in (doc.get(k) or {}).items()})
    return out


_cache = {}


def _cached(what, files, make):
    """make()'s result, made again when one of the files changed (long-running server, rewritten data)."""
    stamp = tuple(p.stat().st_mtime_ns if p.exists() else 0 for p in files)
    hit = _cache.get(what)
    if not hit or hit[0] != stamp:
        hit = _cache[what] = (stamp, make())
    return hit[1]


def _all_files(locale=None):
    files = [BUNDLES] + [path(b) for b in bundle_ids()]
    locales = [locale] if locale else [*NAMES_LOCALES, "es-ES"]
    return files + [p for b in bundle_ids() for l in locales for p in _names_files(l, b)]


def _fallback():
    """{(kind, sub_key): name}: `name` fields of categories.json and plain-string keys (old format, mods)."""
    out = {}
    for c in load():
        out[("categories", sub_key(c["bundle"], c["slug"]))] = c.get("name") or c["slug"]
        out |= {("subcategories", sub_key(c["bundle"], s)): s for s in c["subcategories"]}
    return out


def display(bundle, key, locale="es", kind="subcategories"):
    """A category's or subcategory's display name in a locale (decision 259): the locale's names file
    → es's for es-ES → a `name` field in categories.json → the key itself."""
    k = sub_key(bundle, key)
    own = _cached(("names", locale), _all_files(locale), lambda: load_names(locale))[kind]
    if k in own:
        return own[k]
    return _cached("fallback", _all_files("es"), _fallback).get((kind, k), key)


def category_name(bundle, sub, locale="es"):
    """The display name of the subcategory's broad category, or None."""
    c = category_of(bundle, sub)
    return c and display(bundle, c["slug"], locale, "categories")


def resolve(bundle, text, kind="subcategories"):
    """A key of the bundle for a key or a display name in any locale (CLI input, model output), or None."""
    def make():
        out = {}
        for c in load():
            b = c["bundle"]
            for k, keys in [("categories", [c["slug"]]), ("subcategories", c["subcategories"])]:
                for x in keys:
                    for l in (*NAMES_LOCALES, "es-ES"):
                        out.setdefault((k, b, display(b, x, l, k).casefold()), x)
                    out[(k, b, x.casefold())] = x
        return out
    return _cached("resolve", _all_files(), make).get((kind, bundle, text.strip().casefold()))
