#!/usr/bin/env python3
"""Media candidates and picks (plans/06-images.md, D-13); the providers are in providers/ (D-45).

    trivia-media fetch [--batch pilot | --ids q-0001,q-0002] [--force]
    trivia-media sync [--status approved] [--prune]

`fetch` stores up to 6 candidates per question and slot: work/media/<id>.json for the
question's media, work/media/<id>-background.json for the background image of audio
questions (D-14). The review tool and `qgen review` choose among them; `download()` and
`pick_fields()` turn a chosen candidate into the fields stored in the pool.

Picked files live in the media cache (app/server/media_cache.py, D-17). `sync` downloads
every picked file that isn't cached yet, ahead of game night.
"""
import argparse, json, sys

import layout  # noqa: F401  (also makes app/server importable)
from layout import CANDIDATES, SOURCE_POOL as POOL
from media_cache import (MEDIA, RateLimited, USER_AGENT, cache_path, cached, http_get,  # noqa: F401
                         picked, pool_urls)
import categories  # app/server/categories.py (D-19, D-43)
import progress  # authoring/tools/progress.py: the bar says what a step waits for (QG-20)
import providers  # authoring/tools/providers/: Commons and the other media providers (D-45)

MAX_CANDIDATES = 6
MIN_DECORATIVE_WIDTH = 1920
MIN_ESSENTIAL_WIDTH = 800
MAX_AUDIO_SECONDS = 60


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
    """Searches match every word, so long queries often find nothing: try shorter ones too."""
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


def find_candidates(media, category=None):
    """Up to MAX_CANDIDATES for a question's media, from the providers in order (D-45): each one
    with ever shorter queries until there are ENOUGH; the next provider is only asked while there
    are fewer. Videos fall back to images. A rate-limited provider is skipped; if that leaves
    nothing, RateLimited is raised so a rerun retries instead of storing an empty result.
    `category` is the broad category's slug."""
    kinds = [media["type"]] + (["image"] if media["type"] == "video" else [])
    found, seen, per_author, limited = [], set(), {}, []

    def add(c):
        author = c["author"] or c["title"]
        if (c["provider"], c["id"]) in seen or per_author.get(author, 0) >= MAX_PER_AUTHOR:
            return
        seen.add((c["provider"], c["id"]))
        per_author[author] = per_author.get(author, 0) + 1
        found.append(c)

    for kind in kinds:
        for i, provider in enumerate(providers.order(kind, category)):
            if i and len(found) >= ENOUGH:
                break  # the providers before gave enough; spare the others' limits
            for query in query_variants(media["query"]):
                try:
                    results = providers.search(provider, query, kind)
                except RateLimited as e:
                    limited.append(e)
                    break
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
    if not found and limited:
        raise limited[0]
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


def category_of(q):
    c = categories.broad_of().get(q.get("subcategory"))
    return c["slug"] if c else None


def fetch_for(q, slot="media"):
    spec = slot_media(q, slot)
    found = find_candidates(spec, category_of(q))
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    data = {"query": spec["query"], "type": spec["type"], "candidates": found}
    candidates_path(q["id"], slot).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def short_author(author):
    """The author for an on-screen credit. Some Commons author fields hold a whole paragraph
    (contact details, license text): then only a short first line is kept, and if there is none
    the credit leaves the author out; the source link leads to the full attribution (PUB-2)."""
    first = next((line.strip() for line in (author or "").splitlines() if line.strip()), "")
    return first if first and len(first) <= 80 and not first.endswith(":") else None


def credit_of(candidate):
    return " · ".join(x for x in [short_author(candidate["author"]), candidate["license"], providers.name(candidate)] if x)


def pick_fields(candidate, slot="media"):
    """The fields to store in the pool for a picked candidate, without downloading it."""
    url = providers.download_url(candidate)
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
            with progress.waiting(f"{providers.provider_of(c).NAME} preview"):
                f.write_bytes(http_get(c["preview_url"]))
        args += ["-label", str(i), f"{f}[0]"]
        shown.append(i)
    if not shown:
        return []
    out.parent.mkdir(parents=True, exist_ok=True)
    with progress.waiting("ImageMagick"):
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
    f = sub.add_parser("fetch", help="store media candidates for questions without media")
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
