"""Shared request handling for the game server and the authoring server: JSON, files,
the built client (single-page app) and /media from the cache (D-17)."""
import json, mimetypes
from http.server import BaseHTTPRequestHandler

import media_cache
import paths


class BaseHandler(BaseHTTPRequestHandler):
    """JSON, files, the built client and /media. The authoring server reuses it."""
    dist = paths.DIST
    pool_file = paths.POOL  # /media serves only URLs of questions in this file
    build_hint = "client not built: run `npm run build -w app/client`"

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
        if file_url not in media_cache.pool_urls(self.pool_file):  # not an open proxy: only files questions use
            return self.send_json(404, {"error": "not a media file of any question"})
        try:
            path = media_cache.cached(file_url)
        except media_cache.RateLimited as e:
            return self.send_json(429, {"error": str(e)})
        except OSError as e:  # offline, or Commons unreachable
            return self.send_json(502, {"error": f"not cached and download failed: {e}"})
        return self.send_file(path)

    def send_static(self, url_path):
        rel = url_path.lstrip("/")
        if not self.dist.exists():
            return self.send_json(503, {"error": self.build_hint})
        path = (self.dist / rel).resolve()
        if rel and path.is_file() and path.is_relative_to(self.dist):
            return self.send_file(path)
        return self.send_file(self.dist / "index.html")  # single-page app

    def read_body(self):
        return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")

    def log_message(self, fmt, *args):
        if not self.path.startswith("/assets/"):
            super().log_message(fmt, *args)
