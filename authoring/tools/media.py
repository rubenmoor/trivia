#!/usr/bin/env python3
"""Media from Wikimedia Commons (plans/06-images.md, D-13).

    trivia-media fetch [--batch pilot | --ids q-0001,q-0002] [--force]
    trivia-media sync [--status approved] [--prune]

`fetch` stores up to 6 candidates per question and slot: work/media/<id>.json for the
question's media, work/media/<id>-background.json for the background image of audio
questions (D-14). The review tool and `qgen review` choose among them; `download()` and
`pick_fields()` turn a chosen candidate into the fields stored in the pool.

Picked files live in the media cache (app/server/media_cache.py, D-17). `sync` downloads
every picked file that isn't cached yet, ahead of game night.
"""
import argparse, html, json, re, sys, threading, time, urllib.parse

import layout  # noqa: F401  (also makes app/server importable)
from layout import CANDIDATES, SOURCE_POOL as POOL
from media_cache import (MEDIA, RateLimited, USER_AGENT, cache_path, cached, http_get,  # noqa: F401
                         picked, pool_urls)
import media_cache

API = "https://commons.wikimedia.org/w/api.php"
MAX_CANDIDATES = 6
PREVIEW_WIDTH = 500           # Commons rounds thumbnail widths to standard sizes; 500 is one
IMAGE_WIDTH = 2560            # for 4K TVs; smaller originals are downloaded as they are
MIN_DECORATIVE_WIDTH = 1920
MIN_ESSENTIAL_WIDTH = 800
MAX_AUDIO_SECONDS = 60
VIDEO_PREFERENCE = ["1080p.vp9.webm", "720p.vp9.webm", "1080p.webm", "720p.webm", "480p.vp9.webm", "480p.webm"]


MIN_API_INTERVAL = 2.0  # seconds between search API requests; the API rate-limits bursts
_last_api_request = 0.0
_api_lock = threading.Lock()


def api(**params):
    global _last_api_request
    with _api_lock:  # the server may call this from several threads
        time.sleep(max(0.0, _last_api_request + MIN_API_INTERVAL - time.monotonic()))
        _last_api_request = time.monotonic()
    return json.loads(http_get(API, {"action": "query", "format": "json", **params}))


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
    pages = api(**params).get("query", {}).get("pages", {})
    out = []
    for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        i = p[info][0]
        meta = i.get("extmetadata", {})
        c = {
            "type": kind, "title": p["title"], "page_url": page_url(p["title"]),
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


def acceptable(c, role):
    if c["type"] == "image":
        min_w = MIN_ESSENTIAL_WIDTH if role == "essential" else MIN_DECORATIVE_WIDTH
        landscape = role == "essential" or (c["width"] or 0) > (c["height"] or 0)
        return (c["width"] or 0) >= min_w and landscape
    if c["type"] == "audio":
        return c["duration"] is None or c["duration"] <= MAX_AUDIO_SECONDS
    return True


FILLER_WORDS = {"footage", "video", "clip", "aerial", "photo", "image", "picture", "classic", "solo"}
MAX_PER_AUTHOR = 2
ENOUGH = 3  # stop loosening the query once this many candidates are found


def query_variants(query):
    """Commons matches every word, so long queries often find nothing: try shorter ones too."""
    words = query.split()
    core = [w for w in words if w.lower() not in FILLER_WORDS] or words
    variants = [words, core]
    if len(core) > 2:  # never below two words: single words find unrelated files
        variants += [core[:i] + core[i + 1:] for i in range(len(core))]  # drop one word each
    seen, out = set(), []
    for v in variants:
        q = " ".join(v)
        if q not in seen:
            seen.add(q)
            out.append(q)
    return out


def find_candidates(media):
    """Up to MAX_CANDIDATES for a question's media. Videos fall back to images."""
    kinds = [media["type"]] + (["image"] if media["type"] == "video" else [])
    found, titles, per_author = [], set(), {}

    def add(c):
        author = c["author"] or c["title"]
        if c["title"] in titles or per_author.get(author, 0) >= MAX_PER_AUTHOR:
            return
        titles.add(c["title"])
        per_author[author] = per_author.get(author, 0) + 1
        found.append(c)

    for kind in kinds:
        for query in query_variants(media["query"]):
            results = search(query, kind)
            for c in results:
                if acceptable(c, media["role"]):
                    add(c)
            if kind == "image" and len(found) < MAX_CANDIDATES:  # rather a smaller image than none
                for c in results:
                    if (c["width"] or 0) >= MIN_ESSENTIAL_WIDTH:
                        add(c)
            if len(found) >= MAX_CANDIDATES:
                return found[:MAX_CANDIDATES]
            if len(found) >= ENOUGH:
                break  # good results from this variant; looser ones would add noise
    return found


SLOTS = ("media", "background")


def slot_media(q, slot):
    """The search spec for a slot. The background is always a decorative image."""
    if slot == "media":
        return q["media"]
    return {"type": "image", "role": "decorative", "query": q["background"]["query"]}


def candidates_path(qid, slot="media"):
    return CANDIDATES / (f"{qid}.json" if slot == "media" else f"{qid}-background.json")


def load_candidates(qid, slot="media"):
    path = candidates_path(qid, slot)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def fetch_for(q, slot="media"):
    spec = slot_media(q, slot)
    found = find_candidates(spec)
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    data = {"query": spec["query"], "type": spec["type"], "candidates": found}
    candidates_path(q["id"], slot).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def download_url(candidate):
    """The URL to download for a candidate: large images as a thumbnail of IMAGE_WIDTH."""
    if candidate["type"] == "image" and (candidate["width"] or 0) > IMAGE_WIDTH:
        info = api(titles=candidate["title"], prop="imageinfo", iiprop="url", iiurlwidth=IMAGE_WIDTH)
        return next(iter(info["query"]["pages"].values()))["imageinfo"][0]["thumburl"]
    return candidate["file_url"]


def short_author(author):
    """The author for an on-screen credit. Some Commons author fields hold a whole paragraph
    (contact details, license text): then only a short first line is kept, and if there is none
    the credit leaves the author out; the source link leads to the full attribution (PUB-2)."""
    first = next((line.strip() for line in (author or "").splitlines() if line.strip()), "")
    return first if first and len(first) <= 80 and not first.endswith(":") else None


def credit_of(candidate):
    return " · ".join(x for x in [short_author(candidate["author"]), candidate["license"], "Wikimedia Commons"] if x)


def pick_fields(candidate, slot="media"):
    """The fields to store in the pool for a picked candidate, without downloading it."""
    url = download_url(candidate)
    credit = credit_of(candidate)
    fields = {"source_url": candidate["page_url"], "file_url": url, "credit": credit}
    return {"type": candidate["type"], **fields} if slot == "media" else fields


def download(candidate, slot="media"):
    """Download a picked candidate into the cache; return the fields to store."""
    fields = pick_fields(candidate, slot)
    cached(fields["file_url"])
    return fields


def make_sheet(candidates, out, thumbs):
    """A contact sheet for an LLM review (D-36): every candidate's 500 px preview in a numbered
    grid, made with ImageMagick. Audio candidates have no picture and are left out (the review
    sees their titles). Returns the numbers on the sheet, or [] when there was nothing to show."""
    import subprocess
    thumbs.mkdir(parents=True, exist_ok=True)
    args, shown = [], []
    for i, c in enumerate(candidates, 1):
        if c["type"] == "audio" or not c.get("preview_url"):
            continue
        f = thumbs / f"{i}.img"
        if not f.exists():
            f.write_bytes(http_get(c["preview_url"]))
        args += ["-label", str(i), f"{f}[0]"]
        shown.append(i)
    if not shown:
        return []
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["magick", "montage", *args, "-tile", "3x", "-geometry", "400x300+6+6",
                    "-pointsize", "28", str(out)], check=True, capture_output=True)
    return shown


def cmd_sync(args):
    qs = json.loads(POOL.read_text(encoding="utf-8"))["questions"]
    if args.status:
        qs = [q for q in qs if q["status"] == args.status]
    todo = [(label, url) for q in qs for label, url in picked(q) if not cache_path(url).is_file()]
    print(f"downloading {len(todo)} missing file(s)", flush=True)
    failed = []
    for label, url in todo:
        try:
            print(f"  {label}: {cached(url).name}", flush=True)
        except Exception as e:  # noqa: BLE001 — keep going; rerun retries the rest
            print(f"  {label}: FAILED {e}", file=sys.stderr)
            failed.append(label)
    if args.prune and MEDIA.exists():
        keep = {cache_path(url).name for url in pool_urls(POOL)}  # every pick, not only playable ones
        stale = [f for f in MEDIA.iterdir() if f.is_file() and f.name not in keep]
        for f in stale:
            f.unlink()
        print(f"pruned {len(stale)} unreferenced file(s)")
    if failed:
        print(f"failed: {', '.join(failed)} (rerun to retry)")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="store Commons candidates for questions without media")
    f.add_argument("--batch", help='qgen run name, or "none" for questions without a batch')
    f.add_argument("--ids", help="comma-separated question ids")
    f.add_argument("--force", action="store_true", help="fetch again even if candidates exist")
    s = sub.add_parser("sync", help="download every picked file that isn't in media/ yet")
    s.add_argument("--status", help="only questions with this status, e.g. approved")
    s.add_argument("--prune", action="store_true", help="delete cached files no question references")
    args = ap.parse_args()
    if args.cmd == "sync":
        return cmd_sync(args)

    qs = json.loads(POOL.read_text(encoding="utf-8"))["questions"]
    if args.batch:
        qs = [q for q in qs if q.get("batch") == (None if args.batch == "none" else args.batch)]
    if args.ids:
        wanted = set(args.ids.split(","))
        qs = [q for q in qs if q["id"] in wanted]
    def needed(q, slot):
        target = q["media"] if slot == "media" else q.get("background")
        return target is not None and not target["file_url"] and (args.force or not candidates_path(q["id"], slot).exists())

    todo = [(q, slot) for q in qs for slot in SLOTS if needed(q, slot)]
    print(f"fetching candidates for {len(todo)} slot(s)", flush=True)
    empty = []
    for q, slot in todo:
        label = q["id"] if slot == "media" else f"{q['id']} background"
        try:
            data = fetch_for(q, slot)
        except Exception as e:  # noqa: BLE001 — keep going; rerun retries the rest
            print(f"  {label}: FAILED {e}", file=sys.stderr)
            continue
        kinds = sorted({c["type"] for c in data["candidates"]})
        print(f"  {label}: {len(data['candidates'])} ({', '.join(kinds) or '-'}) for “{data['query']}”", flush=True)
        if not data["candidates"]:
            empty.append(label)
    if empty:
        print(f"no candidates for: {', '.join(empty)} (try a new search term in the review tool, key m)")


if __name__ == "__main__":
    main()
