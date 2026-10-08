"""The media cache (D-17): picked Wikimedia Commons files, downloaded on first use.

Files are named after their URL: <TRIVIA_MEDIA or media/>/<sha1(file_url)[:16]><ext>. The game
server serves only URLs that a question in the pool uses (`pool_urls`), and downloads a file on
a cache miss. `trivia-media sync` (authoring) fills the cache ahead of game night.
"""
import hashlib, json, os, re, sys, threading, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

from paths import MEDIA, POOL

# Wikimedia requires an identifying User-Agent with contact information.
USER_AGENT = "FamilyTrivia/0.2 (https://github.com/rubenmoor/trivia) python-urllib"
# Owner-only OAuth 2.0 token (IMG-15): API calls with it get higher rate limits. Only the
# authoring tools have it (.env.local via direnv); file downloads and the game never send it.
API_URL = "https://commons.wikimedia.org/w/api.php"
TOKEN = os.environ.get("COMMONS_ACCESS_TOKEN")

# Batch runs (`fetch`) wait out rate limits. The server sets this to False, so the
# review tool gets an immediate error instead of a request that hangs for minutes.
WAIT_ON_RATE_LIMIT = True


class RateLimited(Exception):
    """Wikimedia Commons answered HTTP 429."""

    def __init__(self, retry_after):
        self.retry_after = retry_after
        super().__init__(f"rate-limited by Wikimedia Commons; try again in about {retry_after} s")


def http_get(url, params=None):
    """GET with retries on rate limits. File downloads aren't throttled; API calls go through api()."""
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": USER_AGENT}
    if TOKEN and url.startswith(API_URL):
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                return res.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            wait = int(e.headers.get("Retry-After") or 0) or 15 * (attempt + 1)
            if not WAIT_ON_RATE_LIMIT or attempt == 4:
                raise RateLimited(wait) from e
            print(f"  rate limited by Commons, waiting {wait} s", file=sys.stderr)
            time.sleep(wait)



def cache_path(url):
    """Where the file for url is cached. The name depends on the URL alone (D-17)."""
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,5}", ext):
        ext = ".bin"
    return MEDIA / (hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ext)


_download_locks = {}
_download_locks_lock = threading.Lock()


def cached(url):
    """Path of the cached file for url, downloading it first on a cache miss."""
    path = cache_path(url)
    if path.is_file():
        return path
    with _download_locks_lock:  # one download per URL, even if the server gets parallel requests
        lock = _download_locks.setdefault(url, threading.Lock())
    with lock:
        if not path.is_file():
            MEDIA.mkdir(parents=True, exist_ok=True)
            part = path.with_name(f"{path.name}.{threading.get_ident()}.part")
            part.write_bytes(http_get(url))
            part.replace(path)  # atomic: an interrupted download never looks cached
    return path


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
