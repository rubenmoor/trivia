"""Downloads for the authoring tools: provider API calls and media files into the cache (D-17).

Never ships: the game server only reads the cache (app/server/media_cache.py, plan 51).
"""
import os, sys, threading, time, urllib.error, urllib.parse, urllib.request

import layout  # noqa: F401  (makes app/server importable)
from media_cache import MEDIA, cache_path

# Wikimedia requires an identifying User-Agent with contact information.
USER_AGENT = "FamilyTrivia/0.2 (https://github.com/rubenmoor/trivia) python-urllib"
# Owner-only OAuth 2.0 token (IMG-15): API calls with it get higher rate limits. Only the
# authoring tools have it (.env.local via direnv); file downloads never send it.
API_URL = "https://commons.wikimedia.org/w/api.php"
TOKEN = os.environ.get("COMMONS_ACCESS_TOKEN")

# Batch runs (`fetch`) wait out rate limits. The authoring server sets this to False, so the
# review tool gets an immediate error instead of a request that hangs for minutes.
WAIT_ON_RATE_LIMIT = True


class RateLimited(Exception):
    """A media host answered HTTP 429."""

    def __init__(self, retry_after, host="Wikimedia Commons"):
        self.retry_after = retry_after
        super().__init__(f"rate-limited by {host}; try again in about {retry_after} s")


def http_get(url, params=None, headers=None, wait=None):
    """GET with retries on rate limits. File downloads aren't throttled; the authoring tools'
    providers throttle their API calls themselves and pass wait=False to skip a limited one."""
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": USER_AGENT, **(headers or {})}
    if TOKEN and url.startswith(API_URL):
        headers["Authorization"] = f"Bearer {TOKEN}"
    wait = WAIT_ON_RATE_LIMIT if wait is None else wait
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                return res.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            retry = e.headers.get("Retry-After") or ""
            seconds = (int(retry) if retry.isdigit() else 0) or 15 * (attempt + 1)  # may be an HTTP date
            host = urllib.parse.urlparse(url).hostname
            if not wait or attempt == 4:
                raise RateLimited(seconds, host) from e
            print(f"  rate limited by {host}, waiting {seconds} s", file=sys.stderr)
            time.sleep(seconds)


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
