"""Wikimedia Commons (plans/06-images.md, D-13): file search through the MediaWiki API.

API calls are throttled here; `download.http_get` adds the account token (IMG-15).
"""
import html, json, re, urllib.parse

from download import API_URL, Throttle, http_get

ID = "commons"
NAME = "Wikimedia Commons"
PREVIEW_WIDTH = 500           # Commons rounds thumbnail widths to standard sizes; 500 is one
IMAGE_WIDTH = 2560            # thumbnail width above which a larger image is thumbnailed; Commons rounds up, so picks are `3840px-` (IMG-16)
VIDEO_PREFERENCE = ["1080p.vp9.webm", "720p.vp9.webm", "1080p.webm", "720p.webm", "480p.vp9.webm", "480p.webm"]

# Templates the PD tags transclude, not tags themselves: subpages, layouts, texts, categories.
PD_HELPER = re.compile(r"/|layout|-text$|-category$|^PD-generic|-X\b", re.IGNORECASE)

_throttle = Throttle(2.0)  # seconds between API requests; the API rate-limits bursts


def available():
    return True


def api(wait=None, **params):
    """One API call; wait=False raises RateLimited at once instead of waiting it out (search)."""
    _throttle.wait()
    return json.loads(http_get(API_URL, {"action": "query", "format": "json", **params}, wait=wait))


def plain(text):
    """Commons metadata is HTML; credits need plain text."""
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip() or None


def author_url(artist):
    """The first link in the Artist HTML; protocol-relative made https."""
    m = re.search(r'href="([^"]+)"', artist or "")
    url = m and html.unescape(m.group(1))
    return "https:" + url if url and url.startswith("//") else url


def restrictions(meta):
    return [r for r in (meta.get("Restrictions", {}).get("value") or "").split("|") if r]


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
        f"{prefix}extmetadatafilter": "Artist|LicenseShortName|LicenseUrl|Restrictions|License|UsageTerms|AttributionRequired|Copyrighted",
        f"{prefix}urlwidth": PREVIEW_WIDTH,
    }
    pages = api(wait=False, **params).get("query", {}).get("pages", {})
    out = []
    for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        i = p[info][0]
        meta = i.get("extmetadata") or {}
        c = {
            "type": kind, "provider": ID, "id": p["title"], "title": p["title"], "page_url": page_url(p["title"]),
            "preview_url": i.get("thumburl") if kind != "audio" else i["url"],
            "file_url": i["url"], "width": i.get("width"), "height": i.get("height"),
            "duration": i.get("duration"), "mime": i.get("mime"),
            "author": plain(meta.get("Artist", {}).get("value")),
            "author_url": author_url(meta.get("Artist", {}).get("value")),
            "license": plain(meta.get("LicenseShortName", {}).get("value")),
            "license_url": meta.get("LicenseUrl", {}).get("value"),
            "restrictions": restrictions(meta),
        }
        if kind == "video":
            by_key = {d.get("transcodekey"): d["src"] for d in i.get("derivatives", []) if d.get("transcodekey")}
            best = next((by_key[k] for k in VIDEO_PREFERENCE if k in by_key), None)
            if not best and not (c["mime"] or "").startswith("video/webm"):
                continue  # no browser-friendly version
            c["file_url"] = best or c["file_url"]
        out.append(c)
    return out


def members(category, kind):
    """Titles directly in a category. kind: subcat | file. Pages through `cmcontinue`."""
    out, cont = [], {}
    while True:
        r = api(list="categorymembers", cmtitle=category, cmtype=kind, cmlimit="max", **cont)
        out += [m["title"] for m in r.get("query", {}).get("categorymembers", [])]
        cont = r.get("continue")
        if not cont:
            return out


def search_titles(query, filetype, limit=100):
    """File titles for a search, best first (filetype: audio | video); no metadata."""
    r = api(list="search", srnamespace=6, srlimit=min(limit, 500), srsearch=f"{query} filetype:{filetype}")
    return [h["title"] for h in r.get("query", {}).get("search", [])]


def file_records(titles):
    """Survey metadata for a batch of file titles in one call: kind, size, duration, licence, author,
    categories, description. Files without imageinfo (deleted) are left out."""
    pages = {}
    params = {"titles": "|".join(titles), "prop": "imageinfo|categories", "cllimit": "max",
              "iiprop": "url|size|mime|mediatype|extmetadata",
              "iiextmetadatafilter": "Artist|LicenseShortName|Restrictions|ImageDescription"}
    cont = {}
    while True:
        r = api(**params, **cont)
        for k, p in r.get("query", {}).get("pages", {}).items():
            have = pages.setdefault(k, p)
            if have is not p:
                have["categories"] = have.get("categories", []) + p.get("categories", [])
        cont = r.get("continue")
        if not cont:
            break
    out = []
    for p in pages.values():
        if not p.get("imageinfo"):
            continue
        i = p["imageinfo"][0]
        m = i.get("extmetadata") or {}
        out.append({
            "title": p["title"], "page_url": page_url(p["title"]), "file_url": i.get("url"),
            "mediatype": (i.get("mediatype") or "").lower(), "mime": i.get("mime"),
            "duration": i.get("duration"), "width": i.get("width"), "height": i.get("height"),
            "license": plain(m.get("LicenseShortName", {}).get("value")),
            "restrictions": restrictions(m), "author": plain(m.get("Artist", {}).get("value")),
            "categories": [c["title"].removeprefix("Category:") for c in p.get("categories", [])],
            "description": (plain(m.get("ImageDescription", {}).get("value")) or "")[:500]})
    return out


def download_url(candidate):
    """Large images as a thumbnail of IMAGE_WIDTH; everything else as found."""
    if candidate["type"] == "image" and (candidate["width"] or 0) > IMAGE_WIDTH:
        info = api(titles=candidate["title"], prop="imageinfo", iiprop="url", iiurlwidth=IMAGE_WIDTH)
        return next(iter(info["query"]["pages"].values()))["imageinfo"][0]["thumburl"]
    return candidate["file_url"]


def pd_reasons(candidate):
    """The file's PD-* licence templates (PD-old-70, PD-US-expired, …)."""
    return lookup(candidate, templates=True, meta=False)["pd_reasons"]


def lookup(candidate, templates, meta=True):
    """One titles query at pick time: the PD templates and/or author_url and restrictions
    (missing on candidates stored before plan 26)."""
    params = {"titles": candidate["title"], "prop": "|".join(
        p for p, on in [("templates", templates), ("imageinfo", meta)] if on)}
    if templates:
        params |= {"tlnamespace": 10, "tllimit": "max"}
    if meta:
        params |= {"iiprop": "extmetadata", "iiextmetadatafilter": "Artist|Restrictions"}
    page = next(iter(api(**params)["query"]["pages"].values()))
    out = {"pd_reasons": pd_templates(page) if templates else []}
    if meta:
        m = (page.get("imageinfo") or [{}])[0].get("extmetadata") or {}
        out |= {"author_url": author_url(m.get("Artist", {}).get("value")), "restrictions": restrictions(m)}
    return out


def pd_templates(page):
    names = [t["title"].removeprefix("Template:") for t in page.get("templates", [])]
    out = {}
    for n in names:
        if n.startswith("PD-") and not PD_HELPER.search(n):
            out.setdefault(n.lower(), n)  # PD-Art and its redirect PD-art count once
    return list(out.values())
