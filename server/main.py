#!/usr/bin/env python3
"""Local server: serves the built client, the question API (plans/08-review-tool.md)
and the game API (plans/03-game-flow.md, D-25).

    python3 server/main.py [--port 8000] [--host 127.0.0.1]

API:
    GET  /api/categories                           data/categories.json: broad categories with subcategories (D-19)
    GET  /api/questions?batch=pilot&status=draft   matching questions (both filters optional;
                                                   batch=none selects questions without a batch)
    POST /api/questions/<id>/review                body {"review": null | {"decision", "feedback"}}
                                                   sets review + status, returns the question
    POST /api/questions/<id>/difficulty            body {"difficulty": 1-10}; the first change keeps the
                                                   old value in difficulty_original
    POST /api/questions/<id>/media                 body {"index": n, "slot": "media"|"background"}:
                                                   download candidate n (06-images.md)
    POST /api/questions/<id>/media/search          body {"query": "...", "slot": ...}: new search term, fetch again
    GET  /media?url=<file_url>                     a picked media file from the cache in media/; downloaded
                                                   first on a cache miss. Only URLs in the pool (D-17).
    GET  /api/game[?player=<name>]                 {"game": the newest game or null, "supply": supply check
                                                   for that player (default: a new player, D-28)}
    GET  /api/players                              known players, most recent first (D-28)
    POST /api/game/new                             body {"player": name}: start a new game for a known or new
                                                   player (409 with the supply report if it can't)
    POST /api/game/pick                            body {"index": 0-3}: pick a card
    POST /api/game/answer                          body {"index": 0-3}: the final answer
    POST /api/game/skip                            body {"everyone": bool}: skip and burn for the player
                                                   (or for everyone)
    POST /api/game/undo | abandon                  admin overlay actions
    POST /api/game/joker                           body {"joker": "hint"|"skip"|"easier"|"category",
                                                   "purge": bool, "subcategory": name}: play a joker
                                                   (09-jokers.md); the response adds {"event": what happened}
Game responses are {"game": ...} (server/game.py: never the correct answer before the final answer).
While a question is on screen, the game has `jokers`: per joker {"available", "reason"} (D-27).
Questions in responses carry `media_candidates` and `background_candidates`
(from work/media/, or null if not fetched).
"""
import argparse, datetime, json, mimetypes, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "server"))
import categories  # noqa: E402  (tools/categories.py)
import game  # noqa: E402  (server/game.py)
import media  # noqa: E402  (tools/media.py)

media.WAIT_ON_RATE_LIMIT = False  # report rate limits to the review tool instead of hanging

POOL = ROOT / "data" / "questions.json"
DIST = ROOT / "client" / "dist"
DECISIONS = {"approved", "rejected", "needs_work"}

_lock = threading.Lock()


def load_pool():
    return json.loads(POOL.read_text(encoding="utf-8"))


def save_pool(data):
    tmp = POOL.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(POOL)


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
    """Re-read the pool, change one question, write atomically (08, "API")."""
    if review is not None:
        if review.get("decision") not in DECISIONS:
            raise ValueError("decision must be approved, rejected or needs_work")
        feedback = (review.get("feedback") or "").strip() or None
        if review["decision"] == "needs_work" and not feedback:
            raise ValueError("needs_work requires feedback")
        review = {"decision": review["decision"], "feedback": feedback,
                  "reviewed_on": review.get("reviewed_on") or datetime.date.today().isoformat()}
    return update_question(qid, lambda q: q.update(review=review, status=review["decision"] if review else "draft"))


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, body):
        raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def send_file(self, path):
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def send_media(self, file_url):
        if file_url not in media.pool_urls():  # not an open proxy: only files questions use
            return self.send_json(404, {"error": "not a media file of any question"})
        try:
            path = media.cached(file_url)
        except media.RateLimited as e:
            return self.send_json(429, {"error": str(e)})
        except OSError as e:  # offline, or Commons unreachable
            return self.send_json(502, {"error": f"not cached and download failed: {e}"})
        return self.send_file(path)

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
            return self.send_json(200, [with_candidates(q) for q in qs])
        if url.path == "/api/game":
            pool = load_pool()["questions"]
            player = parse_qs(url.query).get("player", [None])[0]
            try:
                return self.send_json(200, {"game": game.view(pool), "supply": game.supply(pool, player)})
            except game.GameError as e:
                return self.send_json(400, {"error": str(e)})
        if url.path == "/api/players":
            return self.send_json(200, game.players())
        if url.path == "/api/categories":
            return self.send_json(200, categories.load())
        if url.path == "/media":
            return self.send_media(parse_qs(url.query).get("url", [""])[0])
        rel = url.path.lstrip("/")
        if not DIST.exists():
            return self.send_json(503, {"error": "client not built: run `npm run build` in client/"})
        path = (DIST / rel).resolve()
        if rel and path.is_file() and path.is_relative_to(DIST):
            return self.send_file(path)
        return self.send_file(DIST / "index.html")  # single-page app

    def game_action(self, action, body):
        actions = {"new": lambda pool: game.new_game(pool, body.get("player")),
                   "pick": lambda pool: game.pick(pool, int(body.get("index", -1))),
                   "answer": lambda pool: game.answer(pool, int(body.get("index", -1))),
                   "skip": lambda pool: game.skip(pool, bool(body.get("everyone"))),
                   "undo": lambda pool: game.undo(),
                   "abandon": lambda pool: game.abandon(),
                   "joker": lambda pool: game.joker(pool, str(body.get("joker")), **{
                       k: body[k] for k in ("purge", "subcategory") if k in body})}
        if action not in actions:
            return self.send_json(404, {"error": "not found"})
        try:
            with _lock:
                pool = load_pool()["questions"]
                result = actions[action](pool)
                out = {"game": game.view(pool)}
                if action == "joker":
                    out["event"] = result
                return self.send_json(200, out)
        except game.GameError as e:
            return self.send_json(409, {"error": str(e), "supply": e.details})
        except Exception as e:  # noqa: BLE001 — the TV always gets an answer
            return self.send_json(500, {"error": f"server error: {type(e).__name__}: {e}"})

    def do_POST(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) == 3 and parts[:2] == ["api", "game"]:
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            return self.game_action(parts[2], json.loads(raw or b"{}"))
        if len(parts) < 4 or parts[:2] != ["api", "questions"]:
            return self.send_json(404, {"error": "not found"})
        qid, action = parts[2], "/".join(parts[3:])
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
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
        except media.RateLimited as e:
            return self.send_json(429, {"error": str(e)})
        except OSError as e:  # network problems talking to Commons
            return self.send_json(502, {"error": f"Wikimedia Commons: {e}"})
        except Exception as e:  # noqa: BLE001 — never leave the review tool without an answer
            return self.send_json(500, {"error": f"server error: {type(e).__name__}: {e}"})

    def log_message(self, fmt, *args):
        if not self.path.startswith("/assets/"):
            super().log_message(fmt, *args)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    print(f"Serving on http://{args.host}:{args.port}/  (game: /, review: /review?batch=pilot)")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
