"""NASA Image and Video Library (plans/23-media-providers.md, MP-7): space photos and videos.

No key. NASA's own media is generally not under copyright; items credited to anyone else (a
company, ESA, a news agency) are skipped, since their rights aren't NASA's to give.
"""
import json, re, threading, time, urllib.parse

import layout  # noqa: F401  (makes app/server importable)
from media_cache import RateLimited, http_get

ID = "nasa"
NAME = "NASA"
API_URL = "https://images-api.nasa.gov/search"
LICENSE_URL = "https://www.nasa.gov/nasa-brand-center/images-and-media/"
IMAGE_WIDTH = 2560  # like Commons: the largest size up to this, for 4K TVs
VIDEO_PREFERENCE = ["~large.mp4", "~medium.mp4", "~orig.mp4"]
MIN_API_INTERVAL = 1.0
_last = 0.0
_lock = threading.Lock()
THIRD_PARTY = re.compile(r"©|copyright|\bESA\b|Roscosmos|SpaceX|Rocket Lab|Boeing|Lockheed|Northrop|"
                         r"Getty|\bAP\b|Reuters|AFP|Blue Origin|Sierra Space", re.IGNORECASE)


def available():
    return True


def _get(url, params=None):
    global _last
    with _lock:
        time.sleep(max(0.0, _last + MIN_API_INTERVAL - time.monotonic()))
        _last = time.monotonic()
    return json.loads(http_get(url, params, wait=False))


def nasa_own(d):
    """True when nobody but NASA is credited."""
    credit = " ".join(d.get(k) or "" for k in ("photographer", "secondary_creator"))
    return not THIRD_PARTY.search(credit) and (not credit.strip() or "NASA" in credit.upper())


def best_image(links):
    """(href, width, height): the largest rendition up to IMAGE_WIDTH, else the smallest larger one.
    The thumbnail only when there is nothing else."""
    sized = [(l["href"], l.get("width"), l.get("height")) for l in links if l.get("render") == "image" and l.get("width")]
    full = [x for x in sized if "~thumb." not in x[0]] or sized
    fit = [x for x in full if x[1] <= IMAGE_WIDTH]
    return max(fit, key=lambda x: x[1]) if fit else min(full, key=lambda x: x[1], default=(None, None, None))


def quoted(url):
    """NASA ids may contain spaces: encode the path."""
    u = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(("https", u.netloc, urllib.parse.quote(urllib.parse.unquote(u.path)), u.query, ""))


def search(query, kind, limit=30):
    if kind not in ("image", "video"):
        return []
    data = _get(API_URL, {"q": query, "media_type": kind, "page_size": min(limit, 30)})
    out = []
    for item in data["collection"]["items"]:
        d, links = item["data"][0], item.get("links", [])
        if not nasa_own(d):
            continue
        preview = next((l["href"] for l in links if l.get("rel") == "preview"), None)
        page = "https://images.nasa.gov/details/" + urllib.parse.quote(d["nasa_id"])
        author = d.get("photographer") or d.get("secondary_creator") or f"NASA {d.get('center') or ''}".strip()
        c = {"type": kind, "provider": ID, "id": d["nasa_id"], "title": d.get("title") or d["nasa_id"],
             "page_url": page, "preview_url": preview, "file_url": None, "width": None, "height": None,
             "duration": None, "mime": None, "author": author, "license": "Public domain", "license_url": LICENSE_URL}
        if kind == "image":
            c["file_url"], c["width"], c["height"] = best_image(links)
            c["mime"] = "image/jpeg"
        else:
            try:
                files = _get(quoted(item["href"]))  # the asset list: renditions of the video
            except RateLimited:
                raise
            except Exception:  # noqa: BLE001 — one broken item doesn't spoil the search
                continue
            c["file_url"] = next((f for suffix in VIDEO_PREFERENCE for f in files if f.endswith(suffix)), None)
            c["mime"] = "video/mp4"
        if c["file_url"]:
            c["file_url"] = quoted(c["file_url"])
            c["preview_url"] = c["preview_url"] and quoted(c["preview_url"])
            out.append(c)
    return out


def download_url(candidate):
    return candidate["file_url"]
