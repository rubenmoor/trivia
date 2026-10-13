#!/usr/bin/env python3
"""Game server: serves the built game client, the game data and the save (plans/03-game-flow.md, plan 50).

    trivia [--port 8000] [--host 127.0.0.1]        (or: python3 app/server/main.py)

It reads app/data/ and serves it under /data/, writes only the game state (TRIVIA_STATE,
default state/), D-35, and reads media from the cache (TRIVIA_MEDIA, default media/) without
downloading: `trivia-media sync --status approved` fills it before play (plan 51).
The referee runs in the browser (app/client/src/engine/, D-69) and saves via /api/save. At start,
game.sqlite + flags.json move to game.json once (save.migrate(), PORT-5); the old files stay as backup.
The review tool and stats pages are authoring tools with their own server (authoring/server).

API:
    GET  /                                         the built client (single-page app: unknown paths get index.html)
    GET  /data/<path>                             a file under app/data/, read-only (plan 50); else 404
    GET  /media?url=<file_url>                     a picked media file from the cache, never downloaded; only
                                                   URLs in the pool (D-17), else 404; not cached: 404 "media_missing"
    GET  /api/save                                 the save document as stored (state/game.json), or 404
                                                   {"error": "not_found"} (plan 49, D-67)
    PUT  /api/save                                 body: the whole save document; replaces it. Envelope check
                                                   only: 400 "bad_save"; 503 "save_locked" when the file stays locked
                                                   or can't be written (disk full)
Any other /api/ path, or POST: 404 {"error": "not_found"}; other methods: 501 (http.server).
Files are streamed; a single Range gets 206 (video seeking).
"""
import argparse
from http.server import ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import media_cache
import paths
import save
from http_base import BaseHandler

NOT_FOUND = {"error": "not_found", "message": "not found"}


def missing_media():
    """The startup line when pool files are missing from the cache, else None."""
    urls = media_cache.pool_urls()
    missing = sum(not media_cache.cache_path(u).is_file() for u in urls)
    if missing:
        return f"media: {missing} of {len(urls)} pool files missing from the cache; run trivia-media sync --status approved"


class Handler(BaseHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/save":
            text = save.load()
            if text is None:
                return self.send_json(404, NOT_FOUND)
            return self.send_raw_json(text.encode("utf-8"))
        if url.path.startswith("/api/"):
            return self.send_json(404, NOT_FOUND)
        if url.path.startswith("/data/"):
            return self.send_data(url.path[len("/data/"):])
        if url.path == "/media":
            return self.send_media(parse_qs(url.query).get("url", [""])[0])
        return self.send_static(url.path)

    def do_POST(self):
        return self.send_json(404, NOT_FOUND)

    def do_PUT(self):
        if urlparse(self.path).path != "/api/save":
            return self.send_json(404, NOT_FOUND)
        try:
            length = self.content_length()
        except ValueError:
            return self.send_json(400, {"error": "bad_save", "message": "bad Content-Length"})
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
            save.write(body)
            return self.send_json(200, {"ok": True})
        except save.SaveError as e:
            return self.send_json(e.status, {"error": e.code, "message": str(e)})
        except OSError as e:  # e.g. disk full: retried with the next action, as on the desktop
            return self.send_json(503, {"error": "save_locked", "message": f"can't write the save: {e}"})

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
    if line := missing_media():
        print(line)
    print(f"Game on http://{args.host}:{args.port}/")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
