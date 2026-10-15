#!/usr/bin/env python3
"""Authoring server: the review tool (plans/08-review-tool.md), the stats pages, the
printable joker cards and the screen gallery (plan 100), with the question API. Never ships (D-35).

    trivia-authoring [--port 8001] [--host 127.0.0.1]   (or: python3 authoring/server/main.py)

It edits authoring/data/questions.json (translations: questions.<locale>.json) and re-exports
app/data/pool.json (pool.<locale>.json) after every change, so the game (port 8000) sees reviews at once.
At startup it turns the questions flagged in the game (the desktop save's flags, save_file.py) into needs-work reviews
(D-47; a flag from an en/de game: of that translation, decision 102) and prints the link to every
question that isn't approved (/review?status=!approved, RV-22).

API:
    GET  /api/categories                           every bundle's broad categories with subcategories (D-19, D-43)
    GET  /api/bundles                              app/data/bundles.json: the question bundles (D-39)
    GET  /api/names?locale=en                      categories.load_names: bundle, category, subcategory names (plan 67)
    GET  /api/age-groups                           app/data/age-groups.json: the difficulty scale and age groups (D-38)
    GET  /api/targets                              authoring/data/targets.json: pool targets per bundle (D-53, plan 12)
    GET  /api/questions?batch=pilot&status=draft   matching questions (all filters optional;
         &reviewer=human|llm|none&bundle=colombia  batch=none selects questions without a batch,
                                                   status=!approved every status but approved;
         &subcategory=Pirámides&media=missing      media=missing: no picked media file;
         &sample=1&audit=flagged                   with batch: sample=1 its spot-check sample in order,
                                                   audit=flagged its audited ones with a major finding, plan 16;
         &run=backaudit-1                          run: a back-audit run's questions, also with sample/audit, plan 57;
         &licence=replace                          licence=replace: not rejected, a picked file to replace, plan 53;
         &played=outliers                          played=outliers: played difficulty outliers of `qgen report --played`
                                                   (too easy / too hard, not mixed), by |Δ|, plan 109)
    GET  /api/questions?locale=en&stale=1          locale (translations.LOCALES; es or absent = the above): one item per
                                                   entry of questions.<locale>.json, the source with the translation's
                                                   text, difficulty(_original), status, batch, review laid over it, plus
                                                   source (Spanish text, difficulty, status), stale, locale; batch, status,
                                                   reviewer, sample, audit filter the translation (audit: its own,
                                                   work/<batch>/audit/<id>.json), bundle, subcategory, media, licence the
                                                   source; stale=1 only stale ones, plays=1 only playing ones
                                                   (translations.plays: the stats pages) (plan 67)
    POST /api/questions/<id>/review                body {"review": null | {"decision", "feedback"}}
                                                   sets review + status as a human review (D-33), returns
                                                   the question; undo sends back a whole earlier review
    POST /api/questions/<id>/difficulty            body {"difficulty": 1-15 (D-38)}; the first change keeps
                                                   the old value in difficulty_original
                                                   review and difficulty take "locale": the translation instead, in
                                                   questions.<locale>.json, re-exporting pool.<locale>.json (plan 67)
    POST /api/questions/<id>/translatable          body {"translatable": bool}: the source's flag (false = doesn't travel);
                                                   false rejects its non-rejected translations ("no viaja"); "locale" in
                                                   the body only picks the item returned (plan 67)
    POST /api/questions/<id>/bundle                body {"bundle": "<id>"}: move it to another bundle
    POST /api/questions/<id>/media                 body {"index": n, "slot": "media"|"background"}:
                                                   download candidate n (06-images.md)
    POST /api/questions/<id>/media/search          body {"query": "...", "slot": ..., "all": bool}: new search term,
                                                   fetch again; all: ask every provider (a licence replacement)
                                                   (bundle, media, media/search refuse a "locale": 400)
    GET  /api/spot-checks                          {"size": n, "problems": [...], "checks": authoring/data/spot-checks.json}
    POST /api/spot-checks/<batch>/<id>             body {"media_changed": bool}: record the spot check from the
                                                   question's human review; {"undo": true} removes it (plan 16);
                                                   <batch> may be a back-audit run (plan 57) or a translation run
                                                   tr-<locale>-<n>: its translation, item with "locale" (plan 67)
    GET  /api/overview                             what the start page shows (RV-12, authoring/server/overview.py);
                                                   rows per locale and its tr-* runs (plan 67)
    GET  /api/stats/media?bundle=colombia          approved questions per media role and image resolution
         &locale=en                                (RV-23, authoring/server/media_stats.py); locale: the sources of
                                                   its playing translations (plan 67)
    GET  /api/gallery                              trivia-gallery's work/gallery/manifest.json (null before its first
                                                   run) and the UI string flags, authoring/data/ui-flags.json (plan 100)
    POST /api/gallery/flags                        body {"flag": {locale, key, text, shot, note}} adds,
                                                   {"id", "note"} edits, {"id", "remove": true} removes; returns all flags
    GET  /gallery/<locale>/<shot>.png              a shot from work/gallery/
    GET  /reports/<batch>.md                       a batch report (authoring/reports/), as plain text
    GET  /media?url=<file_url>                     a picked media file from the cache (any question in the
                                                   source pool, approved or not); downloaded first on a miss
    Other /api/ paths: 404; a bad body or query: 400; a crash: 500 {"error": "server error: …"}.
Questions in responses carry `media_candidates` and `background_candidates`
(from work/media/, or null if not fetched) and `audit` (the newest back-audit, else work/<batch>/audit/<id>.json,
or null; plans 16, 57), `licence`: per picked slot {"verdict": "ok"|"replace", "reasons": [...]}
(providers.licence_verdict, plan 53) and `played`: per age group with played data
[{group, n, right, rated, observed, bound}] (played.review_data, state/played/stats.json; [] without, plan 109).
"""
import argparse, datetime, json, re, sys
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import layout  # noqa: E402  (authoring/tools/layout.py)
import atomic  # noqa: E402  (authoring/tools/atomic.py)
import categories  # noqa: E402  (authoring/tools/categories.py)
from http_base import BaseHandler  # noqa: E402  (authoring/tools/http_base.py)
import download  # noqa: E402  (authoring/tools/download.py)
import media  # noqa: E402  (authoring/tools/media.py)
import media_cache  # noqa: E402  (authoring/tools/media_cache.py)
import media_stats  # noqa: E402  (authoring/server/media_stats.py)
import ui_flags  # noqa: E402  (authoring/server/ui_flags.py)
import overview  # noqa: E402  (authoring/server/overview.py)
import played  # noqa: E402  (authoring/tools/played.py)
import reviews  # noqa: E402  (authoring/tools/reviews.py)
from reviews import (NoQuestion, POOL, load_pool, save_pool, set_review,  # noqa: E402
                     update_question, update_translation)
import save_file  # noqa: E402  (authoring/tools/save_file.py)
from qgen import PROBLEMS, audit_of, is_major, translation_audit_of  # noqa: E402  (authoring/tools/qgen.py)
import spot_checks  # noqa: E402  (authoring/server/spot_checks.py)
import targets  # noqa: E402  (authoring/tools/targets.py)
import translations  # noqa: E402  (authoring/tools/translations.py)

download.WAIT_ON_RATE_LIMIT = False  # report rate limits to the review tool instead of hanging


def locale_of(value):
    """A translation locale, or None for Spanish (es or absent)."""
    if value in (None, "", "es"):
        return None
    if value not in translations.LOCALES:
        raise ValueError(f"unknown locale {value!r}")
    return value


def with_extras(q, data=None, locale="es"):
    """data: played.review_data, loaded once per request (None: no played data)."""
    found = media.load_candidates(q["id"])
    bg = media.load_candidates(q["id"], "background") if q.get("background") else None
    return {**q, "media_candidates": found["candidates"] if found else None,
            "background_candidates": bg["candidates"] if bg else None, "audit": audit_of(q) or None,
            "licence": media.licence_of(q), "played": data["played"].get((q["id"], locale), []) if data else []}


def locale_item(t, q, locale, data=None):
    """The source with the translation laid over it, plus the Spanish side (plan 67)."""
    own = {k: v for k, v in t.items() if k != "source_hash"}
    return {**with_extras(q, data, locale), "difficulty_original": None, "review": None, "batch": None, **own,
            "audit": translation_audit_of(t), "locale": locale, "stale": translations.is_stale(t, q),
            "source": {k: q.get(k) for k in [*translations.TEXT_FIELDS, "difficulty", "status"]}}


def item_of(qid, locale):
    """What a POST returns: the question, or with a locale its translation item."""
    q = find_question(qid)
    data = played.review_data(locale or "es")
    if not locale:
        return with_extras(q, data)
    t = next((t for t in translations.load(locale)["questions"] if t["id"] == qid), None)
    if t is None:
        raise NoQuestion(qid)
    return locale_item(t, q, locale, data)


def played_outliers(items, data, id_of=lambda x: x["id"]):
    """played=outliers: the review candidates, by |Δ| (plan 109)."""
    by_id = {id_of(x): x for x in items}
    return [by_id[i] for i, _, _ in (data or {"outliers": []})["outliers"] if i in by_id]


def locale_questions(locale, query):
    """GET /api/questions?locale=…: the translations as items, filtered (plan 67)."""
    src = {q["id"]: q for q in load_pool()["questions"]}
    pairs = [(t, src[t["id"]]) for t in translations.load(locale)["questions"] if t["id"] in src]
    if "batch" in query:
        want = None if query["batch"] == "none" else query["batch"]
        pairs = [(t, q) for t, q in pairs if t.get("batch") == want]
    if "status" in query:
        pairs = [(t, q) for t, q in pairs if matches_status(t, query["status"])]
    if "reviewer" in query:
        want = None if query["reviewer"] == "none" else query["reviewer"]
        pairs = [(t, q) for t, q in pairs if (t.get("review") or {}).get("reviewer") == want]
    if "bundle" in query:
        pairs = [(t, q) for t, q in pairs if q.get("bundle") == query["bundle"]]
    if "subcategory" in query:
        pairs = [(t, q) for t, q in pairs if q["subcategory"] == query["subcategory"]]
    if query.get("media") == "missing":
        pairs = [(t, q) for t, q in pairs if not q["media"].get("file_url")]
    if query.get("licence") == "replace":
        pairs = [(t, q) for t, q in pairs if media.to_replace(q)]
    if query.get("stale") == "1":
        pairs = [(t, q) for t, q in pairs if translations.is_stale(t, q)]
    if query.get("plays") == "1":
        pairs = [(t, q) for t, q in pairs if translations.plays(t, q)]
    data = played.review_data(locale)
    if query.get("played") == "outliers":
        pairs = played_outliers(pairs, data, lambda p: p[0]["id"])
    if query.get("sample") and query.get("batch"):
        by_id = {t["id"]: (t, q) for t, q in pairs}
        pairs = [by_id[i] for i in spot_checks.sample(query["batch"]) if i in by_id]
    if query.get("audit") == "flagged":
        pairs = [(t, q) for t, q in pairs if (a := translation_audit_of(t)) and is_major(a)]
    return [locale_item(t, q, locale, data) for t, q in pairs]


def source_questions(query):
    """GET /api/questions without a locale: the source pool, filtered."""
    qs = load_pool()["questions"]
    if "batch" in query:
        want = None if query["batch"] == "none" else query["batch"]
        qs = [q for q in qs if q.get("batch") == want]
    if "run" in query:
        ids = spot_checks.run_ids(query["run"]) or []
        by_id = {q["id"]: q for q in qs}
        qs = [by_id[i] for i in ids if i in by_id]
    if "status" in query:
        qs = [q for q in qs if matches_status(q, query["status"])]
    if "bundle" in query:
        qs = [q for q in qs if q.get("bundle") == query["bundle"]]
    if "reviewer" in query:
        want = None if query["reviewer"] == "none" else query["reviewer"]
        qs = [q for q in qs if (q.get("review") or {}).get("reviewer") == want]
    if "subcategory" in query:
        qs = [q for q in qs if q["subcategory"] == query["subcategory"]]
    if query.get("media") == "missing":
        qs = [q for q in qs if not q["media"].get("file_url")]
    if query.get("sample") and (group := query.get("batch") or query.get("run")):
        by_id = {q["id"]: q for q in qs}
        qs = [by_id[i] for i in spot_checks.sample(group) if i in by_id]
    if query.get("licence") == "replace":
        qs = [q for q in qs if media.to_replace(q)]
    if query.get("audit") == "flagged":
        qs = [q for q in qs if (a := audit_of(q)) and is_major(a)]
    data = played.review_data("es")
    if query.get("played") == "outliers":
        qs = played_outliers(qs, data)
    return [with_extras(q, data) for q in qs]


def questions_of(query):
    locale = locale_of(query.get("locale"))
    return locale_questions(locale, query) if locale else source_questions(query)


def media_stats_of(query):
    """GET /api/stats/media: a bundle's approved questions; with a locale the sources of its playing translations."""
    locale = locale_of(query.get("locale"))
    bundle = query.get("bundle")
    qs = [q for q in load_pool()["questions"] if q["status"] == "approved" and (not bundle or q.get("bundle") == bundle)]
    if locale:
        tr = {t["id"]: t for t in translations.load(locale)["questions"]}
        qs = [q for q in qs if q["id"] in tr and translations.plays(tr[q["id"]], q)]
    return media_stats.build(qs)


def names_of(query):
    locale = locale_of(query.get("locale"))
    return categories.load_names(locale) if locale else None


def slot_of(body):
    slot = body.get("slot", "media")
    if slot not in media.SLOTS:
        raise ValueError(f"unknown slot {slot}")
    return slot


def target(q, slot):
    if slot == "background" and not q.get("background"):
        raise ValueError("this question has no background slot (only audio questions do)")
    return q["media"] if slot == "media" else q["background"]


def find_question(qid):
    for q in load_pool()["questions"]:
        if q["id"] == qid:
            return q
    raise NoQuestion(qid)


def pick_media(qid, index, slot):
    target(find_question(qid), slot)
    found = media.load_candidates(qid, slot)
    if not found or not 0 <= index < len(found["candidates"]):
        raise ValueError(f"no candidate {index + 1}")
    fields = media.download(found["candidates"][index], slot)
    return update_question(qid, lambda q: media.apply_pick(target(q, slot), fields))


def search_media(qid, query, slot, every=False):
    query = (query or "").strip()
    if not query:
        raise ValueError("empty search term")
    target(find_question(qid), slot)
    q = update_question(qid, lambda q: target(q, slot).update(query=query))
    media.fetch_for(q, slot, every)
    return q


def load_bundles():
    return json.loads(layout.BUNDLES.read_text(encoding="utf-8"))["bundles"]


def set_bundle(qid, bundle):
    if bundle not in {b["id"] for b in load_bundles()}:
        raise ValueError(f"unknown bundle {bundle!r} (app/data/bundles.json)")
    return update_question(qid, lambda q: q.update(bundle=bundle))


def set_difficulty(qid, difficulty, update=update_question):
    lo, hi = json.loads(layout.AGE_GROUPS.read_text(encoding="utf-8"))["scale"]
    if type(difficulty) is not int or not lo <= difficulty <= hi:  # bool is an int subclass
        raise ValueError(f"difficulty must be an integer from {lo} to {hi}")

    def change(q):
        if q.get("difficulty_original") is None and difficulty != q["difficulty"]:
            q["difficulty_original"] = q["difficulty"]
        q["difficulty"] = difficulty

    return update(qid, change)


def set_translatable(qid, value):
    """The source's translatable flag (absent = true, D-81); false rejects its non-rejected translations
    as a human review, validate's rule (plan 63). Writes the locale files, then the pool and every export."""
    if not isinstance(value, bool):
        raise ValueError("translatable must be true or false")
    with atomic.locked(POOL):
        data = load_pool()
        q = next((q for q in data["questions"] if q["id"] == qid), None)
        if q is None:
            raise NoQuestion(qid)
        if value:
            q.pop("translatable", None)
        else:
            q["translatable"] = False
            for locale in translations.LOCALES:
                with translations.locked(locale):
                    doc = translations.load(locale)
                    hit = [t for t in doc["questions"] if t["id"] == qid and t.get("status") != "rejected"]
                    for t in hit:
                        reject(t)
                    if hit:
                        translations.save(locale, doc)
        save_pool(data)
    return q


def reject(t):
    """A human "no viaja" rejection, D-33's shape (keeps an LLM review as previous)."""
    old = t.get("review") or {}
    t.update(status="rejected", review={
        "decision": "rejected", "feedback": "no viaja", "reviewed_on": datetime.date.today().isoformat(),
        "reviewed_at": reviews.now(), "reviewer": "human", "model": None, "previous": old if old.get("reviewer") == "llm" else old.get("previous")})


def apply_flags():
    """Questions flagged in the game become human needs-work reviews (GM-5, D-47); returns their IDs.
    A flag from an en/de game reviews that translation, else the source (decision 102); the feedback quotes
    the question as the player saw it. Runs only at startup: a question that left the pool while on screen
    would break a running game. The flags stay in the save; state/flags-applied.json records the applied ones (D-59)."""
    ledger = save_file.applied()
    pending = {k: v for k, v in save_file.flags().items() if ledger.get(k) != save_file.stamp(v)}
    known = {}
    done = []
    for qid, flag in pending.items():
        locale = flag.get("locale") or "es"
        where = ", ".join([*filter(None, [flag.get("player"), flag["flagged_on"][:10]]),
                           *([locale] if locale != "es" else [])])
        note = f": {flag['note']}" if flag.get("note") else "."
        shown = flag.get("shown")
        seen = (f" · Vista: «{shown['question']}» Respuesta: «{shown['answer']}»; otras: "
                f"{' / '.join(f'«{w}»' for w in shown['wrong_answers'])}." if shown else "")
        if reviews.needs_work(qid, locale, f"Marcada en el juego ({where}){note}{seen}", known) is None:
            print(f"Flag for unknown question {qid} ({locale}) dropped", file=sys.stderr)
            continue
        done.append(qid if locale == "es" else f"{qid} ({locale})")
    if pending:
        save_file.record_applied({k: save_file.stamp(v) for k, v in pending.items()})
    return done


def matches_status(q, want):
    """`want` is a status, or `!` and a status for every other one (RV-22)."""
    return q["status"] != want[1:] if want.startswith("!") else q["status"] == want


GET_API = {
    "/api/questions": questions_of,
    "/api/categories": lambda query: categories.load(),
    "/api/spot-checks": lambda query: {"size": spot_checks.size(), "problems": PROBLEMS, "checks": spot_checks.load()},
    "/api/overview": lambda query: overview.build(load_pool()["questions"], load_bundles()),
    "/api/stats/media": media_stats_of,
    "/api/age-groups": lambda query: json.loads(layout.AGE_GROUPS.read_text(encoding="utf-8")),
    "/api/bundles": lambda query: load_bundles(),
    "/api/names": names_of,
    "/api/targets": lambda query: targets.load_all(),
    "/api/gallery": lambda query: ui_flags.build(),
}


class Handler(BaseHandler):
    pool_file = POOL

    def send_media(self, file_url):
        """The base's, after a download on a cache miss (the game never downloads)."""
        if file_url in media_cache.pool_urls(self.pool_file):
            try:
                download.cached(file_url)
            except download.RateLimited as e:
                return self.send_json(429, {"error": str(e)})
            except OSError as e:  # offline, or Commons unreachable
                return self.send_json(502, {"error": f"not cached and download failed: {e}"})
        return super().send_media(file_url)

    def do_GET(self):
        url = urlparse(self.path)
        route = GET_API.get(url.path)
        if route:
            try:
                body = route({k: v[0] for k, v in parse_qs(url.query).items()})
            except ValueError as e:
                return self.send_json(400, {"error": str(e)})
            except Exception as e:  # noqa: BLE001 — an answer, not a dropped connection
                return self.send_json(500, {"error": f"server error: {type(e).__name__}: {e}"})
            return self.send_json(200, body)
        if url.path.startswith("/api/"):
            return self.send_json(404, {"error": "not found"})
        if url.path.startswith("/reports/"):
            return self.send_report(url.path.removeprefix("/reports/"))
        if (m := re.fullmatch(r"/gallery/([^/]+)/([^/]+)", url.path)) and m[2].endswith(".png"):
            path = ui_flags.shot_path(m[1], m[2])
            return self.send_file(path) if path else self.send_json(404, {"error": "no such shot: run trivia-gallery"})
        if url.path == "/media":
            return self.send_media(parse_qs(url.query).get("url", [""])[0])
        return self.send_static(url.path)

    def send_report(self, name):
        """authoring/reports/<name>.md as plain text, so the browser shows it instead of downloading it."""
        path = layout.REPORTS / name
        if not re.fullmatch(r"[\w.-]+\.md", name) or not path.is_file():
            return self.send_json(404, {"error": f"no report {name}"})
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def post_spot_check(self, batch, qid):
        try:
            body = self.read_body()
            if body.get("undo"):
                spot_checks.remove(batch, qid)
                return self.send_json(200, None)
            return self.send_json(200, spot_checks.record(batch, find_question(qid), body.get("media_changed")))
        except KeyError:
            return self.send_json(404, {"error": f"no question {qid}"})
        except (ValueError, TypeError, AttributeError) as e:
            return self.send_json(400, {"error": str(e)})

    def do_POST(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if parts == ["api", "gallery", "flags"]:
            try:
                return self.send_json(200, ui_flags.change(self.read_body()))
            except (ValueError, TypeError, AttributeError) as e:
                return self.send_json(400, {"error": str(e)})
        if len(parts) == 4 and parts[:2] == ["api", "spot-checks"]:
            return self.post_spot_check(parts[2], parts[3])
        if len(parts) < 4 or parts[:2] != ["api", "questions"]:
            return self.send_json(404, {"error": "not found"})
        qid, action = parts[2], "/".join(parts[3:])
        try:
            body = self.read_body()
            locale = locale_of(body.get("locale"))
            update = update_translation(locale) if locale else update_question
            if locale and action in ("bundle", "media", "media/search"):
                raise ValueError(f"{action} lives on the source: change it in the Spanish view, without locale")
            if action == "review":
                set_review(qid, body.get("review"), update)
                return self.send_json(200, item_of(qid, locale))
            if action == "difficulty":
                set_difficulty(qid, body.get("difficulty"), update)
                return self.send_json(200, item_of(qid, locale))
            if action == "translatable":
                set_translatable(qid, body.get("translatable"))
                return self.send_json(200, item_of(qid, locale))
            if action == "bundle":
                q = set_bundle(qid, body.get("bundle"))
            elif action == "media":
                q = pick_media(qid, int(body.get("index", -1)), slot_of(body))
            elif action == "media/search":
                q = search_media(qid, body.get("query"), slot_of(body), body.get("all") is True)
            else:
                return self.send_json(404, {"error": "not found"})
            return self.send_json(200, with_extras(q, played.review_data("es")))
        except NoQuestion:
            return self.send_json(404, {"error": f"no question {qid}"})
        except (ValueError, TypeError, AttributeError) as e:
            return self.send_json(400, {"error": str(e)})
        except download.RateLimited as e:
            return self.send_json(429, {"error": str(e)})
        except OSError as e:  # network problems talking to a media provider (D-45)
            return self.send_json(502, {"error": f"media provider: {e}"})
        except Exception as e:  # noqa: BLE001 — never leave the review tool without an answer
            return self.send_json(500, {"error": f"server error: {type(e).__name__}: {e}"})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8001)
    args = ap.parse_args()
    base = f"http://{args.host}:{args.port}"
    applied = apply_flags()
    if applied:
        print(f"Flagged in the game, now needs work: {', '.join(applied)}")
    open_count = sum(q["status"] != "approved" for q in load_pool()["questions"])
    print(f"Authoring on {base}/  (start page; review: /review, stats: /stats/categories)")
    print(f"Not approved ({open_count}): {base}/review?status=!approved")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
