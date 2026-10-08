"""Wikimedia Commons (plans/06-images.md, D-13): file search through the MediaWiki API.

API calls are throttled here; `media_cache.http_get` adds the account token (IMG-15).
"""
import html, json, re, threading, time, urllib.parse

import layout  # noqa: F401  (makes app/server importable)
from media_cache import API_URL, http_get

ID = "commons"
NAME = "Wikimedia Commons"
PREVIEW_WIDTH = 500           # Commons rounds thumbnail widths to standard sizes; 500 is one
IMAGE_WIDTH = 2560            # for 4K TVs; smaller originals are downloaded as they are
VIDEO_PREFERENCE = ["1080p.vp9.webm", "720p.vp9.webm", "1080p.webm", "720p.webm", "480p.vp9.webm", "480p.webm"]

MIN_API_INTERVAL = 2.0  # seconds between search API requests; the API rate-limits bursts
_last_api_request = 0.0
_api_lock = threading.Lock()


def available():
    return True


def api(wait=None, **params):
    """One API call; wait=False raises RateLimited at once instead of waiting it out (search)."""
    global _last_api_request
    with _api_lock:  # the server may call this from several threads
        time.sleep(max(0.0, _last_api_request + MIN_API_INTERVAL - time.monotonic()))
        _last_api_request = time.monotonic()
    return json.loads(http_get(API_URL, {"action": "query", "format": "json", **params}, wait=wait))


def plain(text):
    """Commons metadata is HTML; credits need plain text."""
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip() or None


def page_url(title):
    return "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))


def search(query, kind, limit=30):
    """Commons file search. kind: image | audio | video. Returns raw candidates, best first."""
    filetype = {"image": "bitmap", "audio": "audio", "video": "video"}[kind]
    info = "videoinfo" if kind == "video" else "imageinfo"
    prefix = "vi" if kind == "video" else "ii"
    params = {
        "generator": "search", "gsrnamespace": 6, "gsrlimit": limit,
        "gsrsearch": f"{query} filetype:{filetype}", "prop": info,
        f"{prefix}prop": "url|size|mime|extmetadata" + ("|derivatives" if kind == "video" else ""),
        f"{prefix}extmetadatafilter": "Artist|LicenseShortName|LicenseUrl",
        f"{prefix}urlwidth": PREVIEW_WIDTH,
    }
    pages = api(wait=False, **params).get("query", {}).get("pages", {})
    out = []
    for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        i = p[info][0]
        meta = i.get("extmetadata", {})
        c = {
            "type": kind, "provider": ID, "id": p["title"], "title": p["title"], "page_url": page_url(p["title"]),
            "preview_url": i.get("thumburl") if kind != "audio" else i["url"],
            "file_url": i["url"], "width": i.get("width"), "height": i.get("height"),
            "duration": i.get("duration"), "mime": i.get("mime"),
            "author": plain(meta.get("Artist", {}).get("value")),
            "license": plain(meta.get("LicenseShortName", {}).get("value")),
            "license_url": meta.get("LicenseUrl", {}).get("value"),
        }
        if kind == "video":
            by_key = {d.get("transcodekey"): d["src"] for d in i.get("derivatives", []) if d.get("transcodekey")}
            best = next((by_key[k] for k in VIDEO_PREFERENCE if k in by_key), None)
            if not best and not c["mime"].startswith("video/webm"):
                continue  # no browser-friendly version
            c["file_url"] = best or c["file_url"]
        out.append(c)
    return out


def download_url(candidate):
    """Large images as a thumbnail of IMAGE_WIDTH; everything else as found."""
    if candidate["type"] == "image" and (candidate["width"] or 0) > IMAGE_WIDTH:
        info = api(titles=candidate["title"], prop="imageinfo", iiprop="url", iiurlwidth=IMAGE_WIDTH)
        return next(iter(info["query"]["pages"].values()))["imageinfo"][0]["thumburl"]
    return candidate["file_url"]
