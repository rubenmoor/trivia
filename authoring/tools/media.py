#!/usr/bin/env python3
"""Media candidates and picks (plans/06-images.md, D-13); the providers are in providers/ (D-45).

    trivia-media fetch [--batch pilot | --ids q-0001,q-0002] [--force]
    trivia-media sync [--status approved] [--prune]
    trivia-media licenses [--status approved] [--json]

`fetch` stores up to 6 candidates per question and slot: work/media/<id>.json for the
question's media, work/media/<id>-background.json for the background image of audio
questions (D-14). The review tool and `qgen review` choose among them; `download()` and
`pick_fields()` turn a chosen candidate into the fields stored in the pool.

Picked files live in the media cache (app/server/media_cache.py, D-17); downloads go through
authoring/tools/download.py. `sync` downloads every picked file that isn't cached yet, ahead
of game night.

`licenses` (plans/52, PUB-1) checks the stored licence record of every picked file (no network):
files to replace before a public release, grouped by reason (providers.licence_verdict),
restriction flags for information, and a tally per licence. Skips rejected questions; exits 1
while the replacement list isn't empty.
"""
import argparse, hashlib, itertools, json, re, subprocess, sys

from layout import CANDIDATES, SOURCE_POOL as POOL
from download import RateLimited, cached, http_get
from media_cache import MEDIA, cache_path, picked, pool_urls
import categories  # authoring/tools/categories.py (D-19, D-43)
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


def find_candidates(media, category=None, every=False):
    """Up to MAX_CANDIDATES for a question's media, from the providers in order (D-45): each one
    with ever shorter queries until there are ENOUGH; the next provider is only asked while there
    are fewer. `every` (a licence replacement, plans/53): every provider is asked as if it were
    the first, and the candidates alternate between them. Videos are topped up with images.
    A rate-limited provider is skipped; if that leaves nothing, RateLimited is raised so a rerun
    retries instead of storing an empty result. `category` is the broad category's slug."""
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
            if i and len(found) >= ENOUGH and not every:
                break  # the providers before gave enough; spare the others' limits
            base = len(found) if every else 0
            for query in query_variants(media["query"]):
                try:
                    results = providers.search(provider, query, kind)
                except RateLimited as e:
                    limited.append(e)
                    break
                for c in results:
                    if acceptable(c, media["role"]):
                        add(c)
                if kind == "image" and len(found) - base < MAX_CANDIDATES:  # rather a smaller image than none
                    for c in results:
                        if (c["width"] or 0) >= MIN_ESSENTIAL_WIDTH:
                            add(c)
                if len(found) >= MAX_CANDIDATES and not every:
                    return found[:MAX_CANDIDATES]
                if len(found) - base >= ENOUGH:
                    break  # good results from this variant; looser ones would add noise
    if not found and limited:
        raise limited[0]
    if every:
        found = alternate(found)
    return found[:MAX_CANDIDATES]


def alternate(found):
    """Candidates taking turns by provider, each provider's own order kept."""
    groups = {}
    for c in found:
        groups.setdefault(c["provider"], []).append(c)
    return [c for row in itertools.zip_longest(*groups.values()) for c in row if c]


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


def fetch_for(q, slot="media", every=False):
    spec = slot_media(q, slot)
    found = find_candidates(spec, category_of(q), every)
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    data = {"query": spec["query"], "type": spec["type"], "candidates": found}
    path = candidates_path(q["id"], slot)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)  # a torn file would count as fetched
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
    fields = {"source_url": candidate["page_url"], "file_url": url, "credit": credit,
              **providers.licence_fields(candidate)}
    return {"type": candidate["type"], **fields} if slot == "media" else fields


def unpicked(slot):
    """The slot with its pick cleared: no file, no credit, no licence fields (plans/26)."""
    out = {k: v for k, v in slot.items() if k not in providers.LICENCE_FIELDS}
    return {**out, "source_url": None, "file_url": None, "credit": None}


def download(candidate, slot="media"):
    """Download a picked candidate into the cache; return the fields to store."""
    fields = pick_fields(candidate, slot)
    cached(fields["file_url"])
    return fields


def make_sheet(candidates, out, thumbs):
    """A contact sheet for an LLM review (D-36): every candidate's 500 px preview in a numbered
    grid, made with ImageMagick. Audio candidates have no picture and are left out (the review
    sees their titles). Returns the numbers on the sheet, or [] when there was nothing to show."""
    thumbs.mkdir(parents=True, exist_ok=True)
    args, shown = [], []
    for i, c in enumerate(candidates, 1):
        if c["type"] == "audio" or not c.get("preview_url"):
            continue
        f = thumbs / (hashlib.sha1(c["preview_url"].encode("utf-8")).hexdigest()[:16] + ".img")  # not by number: a new search renumbers
        if not f.exists():
            with progress.waiting(f"{providers.provider_of(c).NAME} preview"):
                f.write_bytes(http_get(c["preview_url"]))
        args += ["-label", str(i), f"{f}[0]"]
        shown.append(i)
    if not shown:
        return []
    out.parent.mkdir(parents=True, exist_ok=True)
    with progress.waiting("ImageMagick"):
        r = subprocess.run(["magick", "montage", *args, "-tile", "3x", "-geometry", "400x300+6+6",
                            "-pointsize", "28", str(out)], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"magick montage: {r.stderr.strip() or f'exit {r.returncode}'}")
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


def cmd_fetch(args):
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



def licence_rows(qs):
    """One row per distinct picked file_url, with its verdict and every question/slot using it."""
    rows = {}
    for q in qs:
        for slot in SLOTS:
            s = q.get(slot)
            if not s or not s.get("file_url"):
                continue
            row = rows.get(s["file_url"])
            if not row:
                verdict, reasons = providers.licence_verdict(s)
                lic = s.get("license")
                row = rows[s["file_url"]] = {
                    "file_url": s["file_url"], "verdict": verdict, "reasons": reasons, "license": lic,
                    "family": providers.licence_kind(lic) if lic else None,
                    "pd_reasons": s.get("pd_reasons"), "restrictions": s.get("restrictions"),
                    "provider": s.get("provider"), "source_url": s.get("source_url"), "uses": []}
            row["uses"].append({"id": q["id"], "slot": slot, "status": q["status"]})
    return list(rows.values())


def licence_of(q):
    """{slot: {"verdict", "reasons"}} for each picked slot (plans/53)."""
    out = {}
    for slot in SLOTS:
        s = q.get(slot)
        if s and s.get("file_url"):
            verdict, reasons = providers.licence_verdict(s)
            out[slot] = {"verdict": verdict, "reasons": reasons}
    return out


def to_replace(q):
    """A question on the licence replacement list: not rejected, some slot `replace` (plans/52)."""
    return q["status"] != "rejected" and any(v["verdict"] == "replace" for v in licence_of(q).values())


def pd_group(reason):
    if re.fullmatch(providers.US_ONLY_PD, reason):
        return "US only"
    return "US government" if reason.startswith("PD-USGov") else "worldwide"


def cmd_licenses(args):
    qs = [q for q in json.loads(POOL.read_text(encoding="utf-8"))["questions"] if q["status"] != "rejected"]
    if args.status:
        qs = [q for q in qs if q["status"] == args.status]
    rows = licence_rows(qs)
    replace = [r for r in rows if r["verdict"] == "replace"]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        sys.exit(1 if replace else 0)

    def uses(r):
        return ", ".join(f"{u['id']}{' background' if u['slot'] == 'background' else ''} ({u['status']})"
                         for u in r["uses"])

    print(f"Replacement list ({len(replace)} of {len(rows)} files)")
    by_code = {}
    for r in replace:
        for reason in r["reasons"]:
            by_code.setdefault(reason.split(":")[0], []).append((reason, r))
    for code, items in sorted(by_code.items()):
        print(f"  {code}")
        for reason, r in items:
            print(f"    {uses(r)}: {reason.split(': ', 1)[-1]}\n      {r['source_url']}")
    if not replace:
        print("  nothing to replace")

    flagged = [r for r in rows if isinstance(r["restrictions"], list) and r["restrictions"]]
    print(f"\nRestriction flags ({len(flagged)} files, information only, D-61)")
    by_flag = {}
    for r in flagged:
        for f in r["restrictions"]:
            by_flag.setdefault(f, []).append(r)
    for f, rs in sorted(by_flag.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"  {f} ({len(rs)}): " + "; ".join(uses(r) for r in rs))

    def tally(title, counts):
        print(f"\n{title}")
        for k, n in sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0]))):
            print(f"  {n:5}  {k}")

    count = lambda keys: {k: keys.count(k) for k in set(keys)}  # noqa: E731
    tally("Files per licence family", count([r["family"] or "off allowlist" for r in rows]))
    tally("Files per licence", count([r["license"] or "missing" for r in rows]))
    pd = [r for r in rows if r["family"] == "public-domain" and isinstance(r["pd_reasons"], list)]
    for group in ("worldwide", "US government", "US only"):
        tally(f"PD reasons, {group} (files)", count([p for r in pd for p in r["pd_reasons"] if pd_group(p) == group]))
    sys.exit(1 if replace else 0)


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
    lc = sub.add_parser("licenses", help="files to replace before a public release, restriction flags, tally")
    lc.add_argument("--status", help="only questions with this status, e.g. approved")
    lc.add_argument("--json", action="store_true", help="rows as JSON")
    args = ap.parse_args()
    {"fetch": cmd_fetch, "sync": cmd_sync, "licenses": cmd_licenses}[args.cmd](args)


if __name__ == "__main__":
    main()
