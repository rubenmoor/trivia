"""The authoring server's request handling: JSON, files, the built UI (single-page app) and /media from the
cache only (D-17, plan 51; moved from app/server/, plan 99)."""
import json, mimetypes, re
from http.server import BaseHTTPRequestHandler

import layout
import media_cache

CHUNK = 1 << 20


def parse_range(header, size):
    """(start, end) of a single `bytes=` range; None = whole file, False = unsatisfiable.
    Same as app/desktop/resolve.mjs parseRange."""
    m = re.fullmatch(r"bytes=(\d*)-(\d*)", (header or "").strip())
    if not m or m[1] == m[2] == "":
        return None
    if m[1] == "":
        start, end = max(0, size - int(m[2])), size - 1
    else:
        start = int(m[1])
        end = size - 1 if m[2] == "" else min(int(m[2]), size - 1)
    return False if start > end or start >= size else (start, end)


class BaseHandler(BaseHTTPRequestHandler):
    """JSON, files, the built UI and /media."""
    dist = layout.DIST
    pool_file = None  # /media serves only URLs of questions in this file (None: every exported pool)
    build_hint = "authoring UI not built: run `npm run build -w authoring/ui`"

    def send_json(self, status, body):
        raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def send_file(self, path):
        """Streamed in chunks; a single `Range` gets 206 (video seeking)."""
        size = path.stat().st_size
        rng = parse_range(self.headers.get("Range"), size)
        if rng is False:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        start, end = rng or (0, size - 1)
        self.send_response(206 if rng else 200)
        self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream")
        self.send_header("Accept-Ranges", "bytes")
        if rng:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        left = end - start + 1
        try:
            with path.open("rb") as f:
                f.seek(start)
                while left > 0 and (chunk := f.read(min(left, CHUNK))):
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except ConnectionError:  # the browser dropped a video it no longer needs
            pass

    def send_media(self, file_url):
        if file_url not in media_cache.pool_urls(self.pool_file):  # not an open proxy: only files questions use
            return self.send_json(404, {"error": "not_found", "message": "not a media file of any question"})
        path = media_cache.cache_path(file_url)
        if not path.is_file():
            return self.send_json(404, {"error": "media_missing", "message": "not in the media cache; run trivia-media sync"})
        return self.send_file(path)

    def send_static(self, url_path):
        rel = url_path.lstrip("/")
        index = self.dist / "index.html"
        if not index.is_file():
            return self.send_json(503, {"error": "not_built", "message": self.build_hint})
        path = (self.dist / rel).resolve()
        if rel and path.is_file() and path.is_relative_to(self.dist):
            return self.send_file(path)
        return self.send_file(index)  # single-page app

    def content_length(self):
        """The request's Content-Length; ValueError when it isn't a number >= 0."""
        n = int(self.headers.get("Content-Length") or 0)
        if n < 0:
            raise ValueError("negative Content-Length")
        return n

    def read_body(self):
        return json.loads(self.rfile.read(self.content_length()) or b"{}")

    def log_message(self, fmt, *args):
        if not self.path.startswith("/assets/"):
            super().log_message(fmt, *args)
