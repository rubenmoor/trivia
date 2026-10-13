"""The media cache (D-17): picked media files, read-only for the game.

Files are named after their URL: <TRIVIA_MEDIA or media/>/<sha1(file_url)[:16]><ext>. The game
server serves only URLs that a question in the pool uses (`pool_urls`) and never downloads;
`trivia-media sync` (authoring/tools/download.py) fills the cache ahead of game night.
"""
import hashlib, json, re, urllib.parse
from pathlib import Path

from paths import MEDIA, pool_files


def cache_path(url):
    """Where the file for url is cached. The name depends on the URL alone (D-17); same as app/desktop/resolve.mjs cacheName."""
    ext = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,5}", ext):
        ext = ".bin"
    return MEDIA / (hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ext)


def picked(q):
    """(label, file_url) for every picked file of a question."""
    out = [(q["id"], q["media"].get("file_url"))]
    if q.get("background"):
        out.append((f"{q['id']} background", q["background"].get("file_url")))
    return [(label, url) for label, url in out if url]


_urls = {}  # pool path -> (mtime_ns, size, urls)


def pool_urls(pool=None):
    """Every file_url in the pool (None: every exported pool file, packs too): the server only serves these.
    Re-read when the file changes."""
    if pool is None:
        return set().union(*map(pool_urls, pool_files()))
    st = Path(pool).stat()
    key = (st.st_mtime_ns, st.st_size)
    hit = _urls.get(str(pool))
    if hit and hit[0] == key:
        return hit[1]
    qs = json.loads(Path(pool).read_text(encoding="utf-8"))["questions"]
    urls = {url for q in qs for _, url in picked(q)}
    _urls[str(pool)] = (key, urls)
    return urls
