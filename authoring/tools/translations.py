"""Translated questions (D-81): authoring/data/questions.<locale>.json per locale, keyed by the
Spanish source's ids. The one reader/writer for the pipeline, the review pages and the export.

Each entry has the translated text, its own difficulty, status, batch and review, and the
source_hash of the source text it was made from; everything else comes from the source by id.
"""
import hashlib, json, re

import atomic
import layout
import pool_export

LANGUAGES = {"en": "English", "de": "German"}  # D-78; zh-Hans, ru, pt-BR when milestone 12 resumes
LOCALES = tuple(LANGUAGES)
LAUNCH = ("es", *LOCALES)  # the source first
TEXT_FIELDS = ["question", "answer", "wrong_answers", "hints", "description", "fun_fact"]


def path(locale):
    return layout.translations(locale)


def locked(locale):
    """Hold the locale file's lock for a load … save (atomic.locked; after the pool's)."""
    return atomic.locked(path(locale))


def load(locale):
    """The locale's file, or an empty one when it doesn't exist."""
    p = path(locale)
    if not p.exists():
        return {"version": 1, "locale": locale, "questions": []}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:  # name the file, as qgen.load_json (circular import)
        raise json.JSONDecodeError(f"{p}: {e.msg}", e.doc, e.pos) from None


def save(locale, doc):
    """Write sorted by id, in questions.json's style."""
    rest = {k: v for k, v in doc.items() if k not in ("version", "locale", "questions")}
    doc = {"version": 1, "locale": locale, **rest, "questions": sorted(doc["questions"], key=lambda t: t["id"])}
    atomic.write_json(path(locale), doc)


def run_locale(run):
    """The locale of a translation run's name `tr-<locale>-<n>` (plan 66), or None."""
    m = re.fullmatch(r"tr-([A-Za-z-]+)-\d+", run)
    return m.group(1) if m and m.group(1) in LOCALES else None


def source_hash(q):
    """First 12 hex of sha256 over the canonical JSON of the source's text fields."""
    text = json.dumps({k: q.get(k) for k in TEXT_FIELDS}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def is_stale(t, q):
    """The source text changed since the translation was made."""
    return t.get("source_hash") != source_hash(q)


def translatable(q):
    return q.get("translatable", True) is not False


def plays(t, q):
    """Goes into pool.<locale>.json: source approved and translatable, translation approved, not stale."""
    return (q["status"] == "approved" and translatable(q) and t.get("status") == "approved"
            and not is_stale(t, q))


def play_entries(locale, source_pool):
    """pool.<locale>.json's entries, in source order: the source's play fields (subcategory,
    bundle, media, background) with the translated text and difficulty."""
    by_id = {t["id"]: t for t in load(locale)["questions"]}
    out = []
    for q in source_pool["questions"]:
        t = by_id.get(q["id"])
        if t and plays(t, q):
            out.append(pool_export.play_entry({**q, **{k: t[k] for k in TEXT_FIELDS + ["difficulty"]}}))
    return out


def export_texts(locale, source_pool):
    """{path: text}: pool.<locale>.json and the packs' (decision 66)."""
    return pool_export.split(play_entries(locale, source_pool), locale)


def exports(source_pool):
    """{path: text} for every locale with a translation file (no pool.es.json)."""
    return {p: t for l in LOCALES if path(l).exists() for p, t in export_texts(l, source_pool).items()}


def yield_rate(locale):
    """Approved / decided translations from tr-<locale>-* runs; 1.0 before any (plan 70)."""
    decided = [t for t in load(locale)["questions"] if (t.get("batch") or "").startswith(f"tr-{locale}-")
               and t.get("status") in ("approved", "needs_work", "rejected")]
    return sum(t["status"] == "approved" for t in decided) / len(decided) if decided else 1.0


def counts(locale, source_pool):
    """{"exported", "stale", "left_out"}: stale = non-rejected translations of changed source text;
    left_out = approved, not stale, but the source isn't approved or translatable."""
    src = {q["id"]: q for q in source_pool["questions"]}
    out = {"exported": 0, "stale": 0, "left_out": 0}
    for t in load(locale)["questions"]:
        q = src.get(t["id"])
        if q is None or t.get("status") == "rejected":
            continue
        if is_stale(t, q):
            out["stale"] += 1
        elif t.get("status") == "approved":
            out["exported" if plays(t, q) else "left_out"] += 1
    return out
