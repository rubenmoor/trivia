#!/usr/bin/env python3
"""Game server: serves the built game client, the game data and the save (plans/03-game-flow.md, plan 50).

    trivia [--port 8000] [--host 127.0.0.1]        (or: python3 app/server/main.py)

It reads app/data/ and serves it under /data/, and writes only the game state
(TRIVIA_STATE, default state/) and the media cache (TRIVIA_MEDIA, default media/), D-35.
The referee runs in the browser (app/client/src/engine/, D-69) and saves via /api/save. At start,
game.sqlite + flags.json move to game.json once (save.migrate(), PORT-5); the old files stay as backup.
The /api/game*, /api/players*, /api/flags routes below are unused since PORT-7 and go in PORT-8.
The review tool and stats pages are authoring tools with their own server (authoring/server).

API:
    GET  /data/<path>                              a file under app/data/, read-only (plan 50); else 404
    GET  /api/categories                           every bundle's broad categories with subcategories (D-19, D-43)
    GET  /media?url=<file_url>                     a picked media file from the cache; downloaded first on a
                                                   cache miss. Only URLs in the pool (D-17).
    GET  /api/game[?player=<name>]                 {"game": the newest game or null, "supply": supply check
                                                   for that player (default: a new player, D-28)}
    GET  /api/players                              known players, most recent first (D-28)
    POST /api/players/delete                       body {"name": name}: delete the player, their games and
                                                   burns (GF-7); returns the remaining players
    POST /api/game/new                             body {"player": name}: start a new game for a known or new
                                                   player (409 with the supply report if it can't)
    POST /api/game/pick                            body {"index": 0-3}: pick a card
    POST /api/game/answer                          body {"index": 0-3}: the final answer
    POST /api/game/skip                            body {"everyone": bool}: skip and burn for the player
                                                   (or for everyone)
    POST /api/game/undo | abandon                  admin overlay actions
    POST /api/game/joker                           body {"joker": "hint"|"skip"|"easier"|"category"|"snipe",
                                                   "purge": bool, "subcategory": name, "index": 0-3}: play a joker
                                                   (09-jokers.md); the response adds {"event": what happened}
    POST /api/game/jokers                          body {"jokers": {joker: count or null}}: the running game's
                                                   joker budget (13-game-modes.md, MD-4); null = unlimited
    GET  /api/flags                                IDs of the questions flagged for review (GM-5, D-47)
    POST /api/flags                                body {"id": question ID, "flagged": bool, "player": name}:
                                                   flag or unflag; returns the flagged IDs (state/flags.json)
    GET  /api/save                                 the save document as stored (state/game.json), or 404
                                                   {"error": "not_found"} (plan 49, D-67)
    PUT  /api/save                                 body: the whole save document; replaces it. Envelope check
                                                   only: 400 "bad_save"; 503 "save_locked" when the file stays locked
Game responses are {"game": ...} (app/server/game.py: never the correct answer before the final answer).
While a question is on screen, the game has `jokers`: per joker {"available", "reason"} (D-27).
Every game has `jokers_left`: per joker the uses left, or null = unlimited (MD-1).
Errors are {"error": code, "params", "message": English, "supply"} (D-57); a joker's `reason` is {"code", "params"}.
"""
import argparse, json, threading
from http.server import ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import categories
import flags
import game
import paths
import save
from http_base import BaseHandler

_lock = threading.Lock()


NOT_FOUND = {"error": "not_found", "message": "not found"}


def error_body(e):
    """A GameError on the wire (D-57): code and params for the client, English message for logs."""
    return {"error": e.code, "params": e.params, "message": str(e), "supply": e.details}


def load_pool():
    return json.loads(paths.POOL.read_text(encoding="utf-8"))


class Handler(BaseHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/game":
            pool = load_pool()["questions"]
            player = parse_qs(url.query).get("player", [None])[0]
            try:
                return self.send_json(200, {"game": game.view(pool), "supply": game.supply(pool, player)})
            except game.GameError as e:
                return self.send_json(400, error_body(e))
        if url.path == "/api/players":
            return self.send_json(200, game.players())
        if url.path == "/api/categories":
            return self.send_json(200, categories.load())
        if url.path == "/api/flags":
            return self.send_json(200, sorted(flags.load()))
        if url.path == "/api/save":
            text = save.load()
            if text is None:
                return self.send_json(404, NOT_FOUND)
            return self.send_raw_json(text.encode("utf-8"))
        if url.path.startswith("/data/"):
            return self.send_data(url.path[len("/data/"):])
        if url.path == "/media":
            return self.send_media(parse_qs(url.query).get("url", [""])[0])
        return self.send_static(url.path)

    def game_action(self, action, body):
        actions = {"new": lambda pool: game.new_game(pool, body.get("player")),
                   "pick": lambda pool: game.pick(pool, int(body.get("index", -1))),
                   "answer": lambda pool: game.answer(pool, int(body.get("index", -1))),
                   "skip": lambda pool: game.skip(pool, bool(body.get("everyone"))),
                   "undo": lambda pool: game.undo(),
                   "abandon": lambda pool: game.abandon(),
                   "jokers": lambda pool: game.set_jokers(body.get("jokers")),
                   "joker": lambda pool: game.joker(pool, str(body.get("joker")), **{
                       k: body[k] for k in ("purge", "subcategory", "index") if k in body})}
        if action not in actions:
            return self.send_json(404, NOT_FOUND)
        try:
            with _lock:
                pool = load_pool()["questions"]
                result = actions[action](pool)
                out = {"game": game.view(pool)}
                if action == "joker":
                    out["event"] = result
                return self.send_json(200, out)
        except game.GameError as e:
            return self.send_json(409, error_body(e))
        except Exception as e:  # noqa: BLE001 — the TV always gets an answer
            return self.send_json(500, {"error": "server_error", "message": f"server error: {type(e).__name__}: {e}"})

    def do_POST(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) == 3 and parts[:2] == ["api", "game"]:
            return self.game_action(parts[2], self.read_body())
        if parts == ["api", "players", "delete"]:
            body = self.read_body()
            try:
                with _lock:
                    game.delete_player(body.get("name"))
                return self.send_json(200, game.players())
            except game.GameError as e:
                return self.send_json(409, error_body(e))
        if parts == ["api", "flags"]:
            body = self.read_body()
            try:
                with _lock:
                    return self.send_json(200, flags.set_flag(body.get("id"), bool(body.get("flagged")),
                                                              body.get("player")))
            except ValueError as e:
                return self.send_json(400, {"error": str(e)})
        return self.send_json(404, NOT_FOUND)

    def do_PUT(self):
        if urlparse(self.path).path != "/api/save":
            return self.send_json(404, NOT_FOUND)
        length = int(self.headers.get("Content-Length", 0))
        if length > save.MAX_BYTES:
            while length > 0:  # drain, so the client reads the answer instead of a reset
                chunk = self.rfile.read(min(length, 1 << 20))
                if not chunk:
                    break
                length -= len(chunk)
            return self.send_json(400, {"error": "bad_save", "message": "save larger than 10 MB"})
        try:
            body = self.read_body()
        except ValueError:
            return self.send_json(400, {"error": "bad_save", "message": "body is not JSON"})
        try:
            with _lock:
                save.write(body)
            return self.send_json(200, {"ok": True})
        except save.SaveError as e:
            return self.send_json(e.status, {"error": e.code, "message": str(e)})

    def send_data(self, rel):
        path = (paths.DATA / rel).resolve()
        if rel and path.is_file() and path.is_relative_to(paths.DATA.resolve()):
            return self.send_file(path)
        return self.send_json(404, NOT_FOUND)

    def send_raw_json(self, raw):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    save.migrate()
    print(f"Game on http://{args.host}:{args.port}/")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
