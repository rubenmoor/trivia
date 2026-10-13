"""Freesound (plans/23-media-providers.md, MP-6): sounds under CC0 or CC BY, up to 60 s.

Needs FREESOUND_API_KEY (.env.local). Search sends it as a header; the game plays the 128 kbps
MP3 preview, which the CDN serves without a key. The API is free for non-commercial use (OQ-45).
"""
import json, os, re

from download import Throttle, http_get

ID = "freesound"
NAME = "Freesound"
KEY = os.environ.get("FREESOUND_API_KEY")
API_URL = "https://freesound.org/apiv2/search/text/"
MAX_SECONDS = 60
_throttle = Throttle(1.0)  # the API allows 60 requests a minute

# Freesound gives licences as URLs; only these two families are asked for (the allowlist, D-45).
LICENCES = [(r"creativecommons\.org/publicdomain/zero/(\d\.\d)", "CC0 {}"),
            (r"creativecommons\.org/licenses/by/(\d\.\d)", "CC BY {}")]


def available():
    return bool(KEY)


def licence(url):
    for pattern, name in LICENCES:
        m = re.search(pattern, url or "")
        if m:
            return name.format(m.group(1))
    return None


def search(query, kind, limit=30):
    if kind != "audio":
        return []
    _throttle.wait()
    params = {"query": query, "page_size": min(limit, 30),
              "fields": "id,name,username,license,duration,previews,url",
              "filter": f'license:("Creative Commons 0" OR "Attribution") duration:[0 TO {MAX_SECONDS}]'}
    data = json.loads(http_get(API_URL, params, headers={"Authorization": f"Token {KEY}"}, wait=False))
    return [{
        "type": "audio", "provider": ID, "id": str(s["id"]), "title": s["name"], "page_url": s["url"],
        "preview_url": s["previews"]["preview-hq-mp3"], "file_url": s["previews"]["preview-hq-mp3"],
        "width": None, "height": None, "duration": s.get("duration"), "mime": "audio/mpeg",
        "author": s.get("username"), "author_url": f"https://freesound.org/people/{s['username']}/",
        "restrictions": [], "license": licence(s.get("license")), "license_url": s.get("license"),
    } for s in data.get("results", [])]


def download_url(candidate):
    return candidate["file_url"]


def pd_reasons(candidate):
    return []  # CC0 and CC BY only
