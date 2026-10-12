"""The media cache (D-17): picked media files, read-only for the game.

Files are named after their URL: <TRIVIA_MEDIA or media/>/<sha1(file_url)[:16]><ext>. The game
server serves only URLs that a question in the pool uses (`pool_urls`) and never downloads;
`trivia-media sync` (authoring/tools/download.py) fills the cache ahead of game night.
"""
import hashlib, json, re, urllib.parse
from pathlib import Path

from paths import MEDIA, POOL


def cache_path(url):
    """Where the file for url is cached. The name depends on the URL alone (D-17)."""
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,5}", ext):
        ext = ".bin"
    return MEDIA / (hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ext)


def picked(q):
    """(label, file_url) for every picked file of a question."""
    out = [(q["id"], q["media"].get("file_url"))]
    if q.get("background"):
        out.append((f"{q['id']} background", q["background"].get("file_url")))
    return [(label, url) for label, url in out if url]


def pool_urls(pool=POOL):
    """Every file_url in the pool: the server only serves these."""
    qs = json.loads(Path(pool).read_text(encoding="utf-8"))["questions"]
    return {url for q in qs for _, url in picked(q)}
