#!/usr/bin/env python3
"""Authoring server: the review tool (plans/08-review-tool.md), the stats pages and the
printable joker cards, with the question API. Never ships (D-35).

    trivia-authoring [--port 8001] [--host 127.0.0.1]   (or: python3 authoring/server/main.py)

It edits authoring/data/questions.json and re-exports app/data/pool.json after every change,
so the game (port 8000) sees reviews at once.

API:
    GET  /api/categories                           app/data/categories.json: broad categories with subcategories (D-19)
    GET  /api/questions?batch=pilot&status=draft   matching questions (all filters optional;
         &reviewer=human|llm|none                  batch=none selects questions without a batch)
    POST /api/questions/<id>/review                body {"review": null | {"decision", "feedback"}}
                                                   sets review + status as a human review (D-33), returns
                                                   the question; undo sends back a whole earlier review
    POST /api/questions/<id>/difficulty            body {"difficulty": 1-10}; the first change keeps the
                                                   old value in difficulty_original
    POST /api/questions/<id>/media                 body {"index": n, "slot": "media"|"background"}:
                                                   download candidate n (06-images.md)
    POST /api/questions/<id>/media/search          body {"query": "...", "slot": ...}: new search term, fetch again
    GET  /media?url=<file_url>                     a picked media file from the cache (any question in the
                                                   source pool, approved or not)
Questions in responses carry `media_candidates` and `background_candidates`
(from work/media/, or null if not fetched).
"""
import argparse, datetime, json, sys, threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import layout  # noqa: E402,F401  (authoring/tools/layout.py; makes app/server importable)
import categories  # noqa: E402  (app/server/categories.py)
from http_base import BaseHandler  # noqa: E402  (app/server/http_base.py)
import media  # noqa: E402  (authoring/tools/media.py)
import media_cache  # noqa: E402  (app/server/media_cache.py)
import pool_export  # noqa: E402  (authoring/tools/pool_export.py)

media_cache.WAIT_ON_RATE_LIMIT = False  # report rate limits to the review tool instead of hanging

POOL = layout.SOURCE_POOL
DECISIONS = {"approved", "rejected", "needs_work"}
REVIEWERS = {"human", "llm"}

_lock = threading.Lock()


def load_pool():
    return json.loads(POOL.read_text(encoding="utf-8"))


def save_pool(data):
    tmp = POOL.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(POOL)
    pool_export.write(data)  # the game reads only the export (D-35)


def update_question(qid, change):
    """Re-read the pool, apply change(q) to one question, write atomically (08, "API")."""
    with _lock:
        data = load_pool()
        for q in data["questions"]:
            if q["id"] == qid:
                change(q)
                save_pool(data)
                return q
    raise KeyError(qid)


def with_candidates(q):
    found = media.load_candidates(q["id"])
    bg = media.load_candidates(q["id"], "background") if q.get("background") else None
    return {**q, "media_candidates": found["candidates"] if found else None,
            "background_candidates": bg["candidates"] if bg else None}


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
    raise KeyError(qid)


def pick_media(qid, index, slot):
    target(find_question(qid), slot)
    found = media.load_candidates(qid, slot)
    if not found or not 0 <= index < len(found["candidates"]):
        raise ValueError(f"no candidate {index + 1}")
    fields = media.download(found["candidates"][index], slot)
    return update_question(qid, lambda q: target(q, slot).update(fields))


def search_media(qid, query, slot):
    query = (query or "").strip()
    if not query:
        raise ValueError("empty search term")
    target(find_question(qid), slot)
    q = update_question(qid, lambda q: target(q, slot).update(query=query))
    media.fetch_for(q, slot)
    return q


def set_difficulty(qid, difficulty):
    if not isinstance(difficulty, int) or not 1 <= difficulty <= 10:
        raise ValueError("difficulty must be an integer from 1 to 10")

    def change(q):
        if q.get("difficulty_original") is None and difficulty != q["difficulty"]:
            q["difficulty_original"] = q["difficulty"]
        q["difficulty"] = difficulty

    return update_question(qid, change)


def set_review(qid, review):
    """Re-read the pool, change one question, write atomically (08, "API").
    A new decision is a human review; it keeps the LLM review it replaces as `previous` (D-33).
    A review that names its reviewer is an undo putting an earlier review back as it was."""
    restore = review is not None and "reviewer" in review
    if review is not None:
        if review.get("decision") not in DECISIONS:
            raise ValueError("decision must be approved, rejected or needs_work")
        feedback = (review.get("feedback") or "").strip() or None
        if review["decision"] == "needs_work" and not feedback:
            raise ValueError("needs_work requires feedback")
        if restore and review["reviewer"] not in REVIEWERS:
            raise ValueError("reviewer must be human or llm")
        review = {"decision": review["decision"], "feedback": feedback,
                  "reviewed_on": review.get("reviewed_on") or datetime.date.today().isoformat(),
                  "reviewer": review.get("reviewer", "human"), "model": review.get("model"),
                  "previous": review.get("previous")}

    def change(q):
        if review is not None and not restore:
            old = q.get("review") or {}
            review["previous"] = old if old.get("reviewer") == "llm" else old.get("previous")
        q.update(review=review, status=review["decision"] if review else "draft")

    return update_question(qid, change)


class Handler(BaseHandler):
    dist = layout.DIST
    pool_file = POOL
    build_hint = "authoring UI not built: run `npm run build -w authoring/ui`"

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/questions":
            query = {k: v[0] for k, v in parse_qs(url.query).items()}
            qs = load_pool()["questions"]
            if "batch" in query:
                want = None if query["batch"] == "none" else query["batch"]
                qs = [q for q in qs if q.get("batch") == want]
            if "status" in query:
                qs = [q for q in qs if q["status"] == query["status"]]
            if "reviewer" in query:
                want = None if query["reviewer"] == "none" else query["reviewer"]
                qs = [q for q in qs if (q.get("review") or {}).get("reviewer") == want]
            return self.send_json(200, [with_candidates(q) for q in qs])
        if url.path == "/api/categories":
            return self.send_json(200, categories.load())
        if url.path == "/media":
            return self.send_media(parse_qs(url.query).get("url", [""])[0])
        return self.send_static(url.path)

    def do_POST(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) < 4 or parts[:2] != ["api", "questions"]:
            return self.send_json(404, {"error": "not found"})
        qid, action = parts[2], "/".join(parts[3:])
        try:
            body = self.read_body()
            if action == "review":
                q = set_review(qid, body.get("review"))
            elif action == "difficulty":
                q = set_difficulty(qid, body.get("difficulty"))
            elif action == "media":
                q = pick_media(qid, int(body.get("index", -1)), slot_of(body))
            elif action == "media/search":
                q = search_media(qid, body.get("query"), slot_of(body))
            else:
                return self.send_json(404, {"error": "not found"})
            return self.send_json(200, with_candidates(q))
        except KeyError:
            return self.send_json(404, {"error": f"no question {qid}"})
        except (ValueError, TypeError, AttributeError) as e:
            return self.send_json(400, {"error": str(e)})
        except media_cache.RateLimited as e:
            return self.send_json(429, {"error": str(e)})
        except OSError as e:  # network problems talking to Commons
            return self.send_json(502, {"error": f"Wikimedia Commons: {e}"})
        except Exception as e:  # noqa: BLE001 — never leave the review tool without an answer
            return self.send_json(500, {"error": f"server error: {type(e).__name__}: {e}"})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8001)
    args = ap.parse_args()
    print(f"Authoring on http://{args.host}:{args.port}/  (review: /review?batch=pilot, stats: /stats/categories)")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
