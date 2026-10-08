#!/usr/bin/env python3
"""Authoring server: the review tool (plans/08-review-tool.md), the stats pages and the
printable joker cards, with the question API. Never ships (D-35).

    trivia-authoring [--port 8001] [--host 127.0.0.1]   (or: python3 authoring/server/main.py)

It edits authoring/data/questions.json and re-exports app/data/pool.json after every change,
so the game (port 8000) sees reviews at once. At startup it turns the questions flagged in the
game (state/flags.json) into needs-work reviews (D-47) and prints the link to every question
that isn't approved (/review?status=!approved, RV-22).

API:
    GET  /api/categories                           every bundle's broad categories with subcategories (D-19, D-43)
    GET  /api/bundles                              app/data/bundles.json: the question bundles (D-39)
    GET  /api/age-groups                           app/data/age-groups.json: the difficulty scale and age groups (D-38)
    GET  /api/questions?batch=pilot&status=draft   matching questions (all filters optional;
         &reviewer=human|llm|none&bundle=colombia  batch=none selects questions without a batch,
                                                   status=!approved every status but approved;
         &subcategory=Pirámides&media=missing      media=missing: no picked media file)
    POST /api/questions/<id>/review                body {"review": null | {"decision", "feedback"}}
                                                   sets review + status as a human review (D-33), returns
                                                   the question; undo sends back a whole earlier review
    POST /api/questions/<id>/difficulty            body {"difficulty": 1-15 (D-38)}; the first change keeps
                                                   the old value in difficulty_original
    POST /api/questions/<id>/bundle                body {"bundle": "<id>"}: move it to another bundle
    POST /api/questions/<id>/media                 body {"index": n, "slot": "media"|"background"}:
                                                   download candidate n (06-images.md)
    POST /api/questions/<id>/media/search          body {"query": "...", "slot": ...}: new search term, fetch again
    GET  /api/overview                             what the start page shows (RV-12, authoring/server/overview.py)
    GET  /reports/<batch>.md                       a batch report (authoring/reports/), as plain text
    GET  /media?url=<file_url>                     a picked media file from the cache (any question in the
                                                   source pool, approved or not)
Questions in responses carry `media_candidates` and `background_candidates`
(from work/media/, or null if not fetched).
"""
import argparse, datetime, json, re, sys, threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import layout  # noqa: E402,F401  (authoring/tools/layout.py; makes app/server importable)
import categories  # noqa: E402  (app/server/categories.py)
import flags  # noqa: E402  (app/server/flags.py)
from http_base import BaseHandler  # noqa: E402  (app/server/http_base.py)
import media  # noqa: E402  (authoring/tools/media.py)
import media_cache  # noqa: E402  (app/server/media_cache.py)
import overview  # noqa: E402  (authoring/server/overview.py)
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


def load_bundles():
    return json.loads(layout.BUNDLES.read_text(encoding="utf-8"))["bundles"]


def set_bundle(qid, bundle):
    if bundle not in {b["id"] for b in load_bundles()}:
        raise ValueError(f"unknown bundle {bundle!r} (app/data/bundles.json)")
    return update_question(qid, lambda q: q.update(bundle=bundle))


def set_difficulty(qid, difficulty):
    lo, hi = json.loads(layout.AGE_GROUPS.read_text(encoding="utf-8"))["scale"]
    if not isinstance(difficulty, int) or not lo <= difficulty <= hi:
        raise ValueError(f"difficulty must be an integer from {lo} to {hi}")

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


def apply_flags():
    """Questions flagged in the game become human needs-work reviews (GM-5, D-47); returns their IDs.
    Runs only at startup: a question that left the pool while on screen would break a running game."""
    pending = flags.load()
    known = {q["id"]: q for q in load_pool()["questions"]}
    done = []
    for qid, flag in pending.items():
        if qid not in known:
            print(f"Flag for unknown question {qid} dropped", file=sys.stderr)
            continue
        who = f"{flag['player']}, " if flag.get("player") else ""
        feedback = f"Marcada en el juego ({who}{flag['flagged_on'][:10]})."
        old = (known[qid].get("review") or {}).get("feedback")
        set_review(qid, {"decision": "needs_work", "feedback": f"{feedback} Antes: {old}" if old else feedback})
        done.append(qid)
    if pending:  # re-read: the game may have flagged another question meanwhile
        flags.save({k: v for k, v in flags.load().items() if k not in pending})
    return done


def matches_status(q, want):
    """`want` is a status, or `!` and a status for every other one (RV-22)."""
    return q["status"] != want[1:] if want.startswith("!") else q["status"] == want


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
            return self.send_json(200, [with_candidates(q) for q in qs])
        if url.path == "/api/categories":
            return self.send_json(200, categories.load())
        if url.path == "/api/overview":
            return self.send_json(200, overview.build(load_pool()["questions"], load_bundles()))
        if url.path == "/api/age-groups":
            return self.send_json(200, json.loads(layout.AGE_GROUPS.read_text(encoding="utf-8")))
        if url.path == "/api/bundles":
            return self.send_json(200, load_bundles())
        if url.path.startswith("/reports/"):
            return self.send_report(url.path.removeprefix("/reports/"))
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
            elif action == "bundle":
                q = set_bundle(qid, body.get("bundle"))
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
        except OSError as e:  # network problems talking to a media provider (D-45)
            return self.send_json(502, {"error": f"media search: {e}"})
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
