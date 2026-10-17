"""The game's pool (D-35): app/data/pool.<locale>.json (es: pool.json) is generated from the approved sources
in authoring/data/questions.json in that locale and authoring/data/questions.<locale>.json's translations
(D-81, decision 235). base's questions only; each pack (non-base bundle) has its own app/data/bundles/<id>/pool[.<locale>].json (decision 66)."""
import hashlib
import json

import atomic
import layout

PLAY_FIELDS = ["id", "status", "difficulty", "subcategory", "bundle", "description", "question", "answer",
               "wrong_answers", "hints", "fun_fact"]
MEDIA_PLAY_FIELDS = ["type", "role", "file_url", "source_url", "credit", "provider", "license", "license_url", "author",
                     "author_url"]
BACKGROUND_PLAY_FIELDS = ["file_url", "source_url", "credit", "provider", "license", "license_url", "author", "author_url"]


def play_entry(q):
    """An approved question with only what play needs (no reviews, ratings, revisions or pipeline fields)."""
    e = {k: q[k] for k in PLAY_FIELDS}
    e["media"] = {k: q["media"].get(k) for k in MEDIA_PLAY_FIELDS}
    e["background"] = ({k: q["background"].get(k) for k in BACKGROUND_PLAY_FIELDS}
                       if q.get("background") else None)
    return e


def pool_text(entries):
    """hash: first 8 hex of sha256 over the questions' own JSON (indent 2, D-92)."""
    questions = json.dumps(entries, ensure_ascii=False, indent=2)
    digest = hashlib.sha256(questions.encode("utf-8")).hexdigest()[:8]
    return json.dumps({"version": 1, "hash": digest, "questions": entries}, ensure_ascii=False, indent=2) + "\n"


def split(entries, locale="es"):
    """{path: text}: base's entries in its pool file (always), each pack's in its own when it has any."""
    by = {"base": []}
    for e in entries:
        by.setdefault(e["bundle"], []).append(e)
    return {layout.POOL_FILE(locale, b): pool_text(es) for b, es in by.items()}


def exports(pool):
    """{path: text}: every locale with a pool (translations.exports)."""
    import translations  # authoring/tools/translations.py (imports this module)
    return translations.exports(pool)


def demo_ids():
    """The demo list's ids, or None without a list (decision 339)."""
    if not layout.DEMO_LIST.exists():
        return None
    return json.loads(layout.DEMO_LIST.read_text(encoding="utf-8")).get("ids") or []


def demo_exports(pool):
    """{path: text}: app/data/demo/pool[.<locale>].json, base's entries of the listed ids unchanged; {} without a list."""
    import translations  # authoring/tools/translations.py (imports this module)
    ids = demo_ids()
    if ids is None:
        return {}
    want = set(ids)
    return {layout.DEMO_POOL(l): pool_text([e for e in translations.play_entries(l, pool)
                                            if e["id"] in want and e["bundle"] == "base"])
            for l in translations.LOCALES if translations.exported(l, pool)}


def stale_demo(texts):
    """Demo pool files that exist but aren't in texts."""
    return [p for p in layout.DEMO_DATA.glob("pool*.json") if p not in texts]


def stale_packs(texts, locale=None):
    """Pack pool files (of `locale`, else any) that exist but aren't in texts: a pack that lost its questions."""
    names = {"pool.json" if locale == "es" else f"pool.{locale}.json"} if locale else None
    return [p for p in layout.POOL_FILES()
            if p.parent.parent == layout.BUNDLE_DATA and p not in texts and (names is None or p.name in names)]


def write_texts(texts, locale=None):
    """Write texts (atomic per file); delete the stale pack files."""
    for path, text in texts.items():
        atomic.write_text(path, text)
    for p in stale_packs(texts, locale):
        p.unlink()


def write(pool):
    """Write the exports for this source pool (the parsed authoring/data/questions.json)."""
    with atomic.locked(layout.SOURCE_POOL):  # one writer of the exports at a time
        write_texts(exports(pool))
        demo = demo_exports(pool)
        for path, text in demo.items():
            atomic.write_text(path, text)
        for p in stale_demo(demo):
            p.unlink()
        if not demo and layout.DEMO_DATA.is_dir() and not any(layout.DEMO_DATA.iterdir()):
            layout.DEMO_DATA.rmdir()
