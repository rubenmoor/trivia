"""Openverse (plans/23-media-providers.md, MP-4): openly licensed images from Flickr, museums
and others. Commons' own files are left out, since Commons is asked directly.

Works anonymously (20 requests a minute, 200 a day, at most 20 results). With OPENVERSE_CLIENT_ID
and OPENVERSE_CLIENT_SECRET (.env.local; registered through the API) the limits are much higher.
"""
import json, os, threading, time, urllib.parse, urllib.request

import layout  # noqa: F401  (makes app/server importable)
from media_cache import USER_AGENT, http_get

ID = "openverse"
NAME = "Openverse"
API = "https://api.openverse.org/v1"
CLIENT_ID = os.environ.get("OPENVERSE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("OPENVERSE_CLIENT_SECRET")
PREVIEW_MAX_WIDTH = 1600  # larger originals are previewed through Openverse's thumbnail
MIN_API_INTERVAL = 3.0    # the anonymous burst limit is 20 a minute
_last = 0.0
_lock = threading.Lock()
_token = {"value": None, "expires": 0.0}

# Openverse licence codes → the short names the allowlist knows (D-45).
LICENCES = {"cc0": "CC0 {}", "pdm": "Public Domain Mark {}", "by": "CC BY {}", "by-sa": "CC BY-SA {}"}


def available():
    return True


def token():
    """A bearer token for registered credentials, renewed before it expires; None when anonymous."""
    if not (CLIENT_ID and CLIENT_SECRET):
        return None
    if _token["value"] is None or time.time() > _token["expires"] - 60:
        body = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": CLIENT_ID,
                                       "client_secret": CLIENT_SECRET}).encode()
        req = urllib.request.Request(f"{API}/auth_tokens/token/", data=body, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as res:
            out = json.loads(res.read())
        _token.update(value=out["access_token"], expires=time.time() + out.get("expires_in", 3600))
    return _token["value"]


def source_name(source):
    return {"flickr": "Flickr", "met": "The Met", "nasa": "NASA"}.get(source, source.replace("_", " ").title())


def search(query, kind, limit=30):
    if kind != "image":
        return []  # Openverse's audio is mostly music (Jamendo, ccMixter), which D-13 rules out
    global _last
    t = token()
    with _lock:
        time.sleep(max(0.0, _last + (0.5 if t else MIN_API_INTERVAL) - time.monotonic()))
        _last = time.monotonic()
    params = {"q": query, "license": ",".join(LICENCES), "excluded_source": "wikimedia",
              "page_size": min(limit, 30 if t else 20)}
    data = json.loads(http_get(f"{API}/images/", params, headers={"Authorization": f"Bearer {t}"} if t else None,
                               wait=False))
    out = []
    for r in data.get("results", []):
        if r.get("mature") or r["license"] not in LICENCES:
            continue
        width = r.get("width")
        out.append({
            "type": "image", "provider": ID, "id": r["id"], "title": r.get("title") or r["id"],
            "page_url": r.get("foreign_landing_url") or r.get("detail_url"),
            "preview_url": r["url"] if width and width <= PREVIEW_MAX_WIDTH else r.get("thumbnail"),
            "file_url": r["url"], "width": width, "height": r.get("height"), "duration": None,
            "mime": None, "author": r.get("creator"),
            "license": LICENCES[r["license"]].format(r.get("license_version") or "1.0"),
            "license_url": r.get("license_url"), "source": source_name(r.get("source") or r.get("provider") or ""),
        })
    return out


def download_url(candidate):
    return candidate["file_url"]
