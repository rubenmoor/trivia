"""`qgen media-survey`: how much free audio and video Commons holds for media-first questions (plan 201).

Crawls the SEEDS below (Commons categories, depth <= 2, and searches) through `providers.commons`
(every call via `commons.api`), keeps per-file metadata and tallies what survives the filters.
Raw records per seed go to work/media-survey/raw/<seed>.jsonl (a finished seed is kept: `--resume`);
the filters run over all raw records at the end, so a changed filter needs no new crawl.
Output: files.jsonl (kept files), tally.json, tally.md. Writes nothing outside work/media-survey/.
"""
import json, re, time, urllib.parse
from collections import Counter, defaultdict

import atomic, layout, progress, providers
from media import max_seconds  # authoring/tools/media.py
from providers import commons

OUT = layout.WORK / "media-survey"
MIN_AUDIO_S, MAX_S, MIN_VIDEO_HEIGHT = 2, 600, 480
MAX_SUBCATS = 25   # subcategories followed per seed (breadth first)
MAX_FILES = 300    # files kept per seed before --limit
DEPTH = 2
BATCH = 20         # titles per metadata call (long GET URLs fail above ~25)
CLASSES = ("general", "pd-music", "pd-film")


def cat(name, cats, kind, media, cls="general", depth=DEPTH):
    return {"id": f"cat:{name}", "category": f"Category:{name}", "cats": cats, "kind": kind, "type": media,
            "class": cls, "depth": depth}


def search(query, cats, kind, media, cls="general"):
    return {"id": f"q:{media}:{query}", "query": query, "cats": cats, "kind": kind, "type": media, "class": cls}


# kinds: animal | instrument | language | machine | place | event-person | piece-film | video-scene
SEEDS = [
    cat("Audio files of Aves", ["animals"], "animal", "audio"),
    cat("Birds calling", ["animals"], "animal", "audio", depth=1),
    search("bird song", ["animals"], "animal", "audio"),
    search("mammal vocalization", ["animals"], "animal", "audio"),
    search("lion roar", ["animals"], "animal", "audio"),
    search("whale song", ["animals", "planet-earth"], "animal", "audio"),
    search("dog bark", ["pets-and-farm"], "animal", "audio"),
    search("cat meow purr", ["pets-and-farm"], "animal", "audio"),
    search("farm animal sound cow sheep horse", ["pets-and-farm"], "animal", "audio"),
    search("insect sound cricket cicada", ["animals"], "animal", "audio"),
    search("frog call", ["animals", "amazon"], "animal", "audio"),
    search("rainforest sounds", ["amazon", "plants-and-environment"], "animal", "audio"),
    search("musical instrument sample", ["music"], "instrument", "audio"),
    search("piano recording", ["music"], "instrument", "audio"),
    search("guitar recording", ["music"], "instrument", "audio"),
    search("violin cello recording", ["music"], "instrument", "audio"),
    search("drum percussion recording", ["music"], "instrument", "audio"),
    search("flute clarinet saxophone trumpet", ["music"], "instrument", "audio"),
    search("traditional folk instrument", ["music", "holidays-and-traditions"], "instrument", "audio"),
    cat("Lingua Libre pronunciation", ["languages-and-words"], "language", "audio", depth=1),
    search("spoken language sample", ["languages-and-words"], "language", "audio"),
    search("pronunciation of city name", ["world-geography", "languages-and-words"], "place", "audio"),
    search("city ambience street sounds", ["world-geography", "architecture-and-landmarks"], "place", "audio"),
    search("church bells", ["architecture-and-landmarks", "religion-and-philosophy"], "place", "audio"),
    search("train sound", ["transport"], "machine", "audio"),
    search("car engine sound", ["transport", "inventions-and-technology"], "machine", "audio"),
    search("aircraft sound", ["transport"], "machine", "audio"),
    search("ship horn", ["transport"], "machine", "audio"),
    search("machine noise", ["inventions-and-technology"], "machine", "audio"),
    search("telephone typewriter sound", ["inventions-and-technology"], "machine", "audio"),
    search("thunder rain storm", ["planet-earth"], "place", "audio"),
    search("ocean waves wind", ["planet-earth", "plants-and-environment"], "place", "audio"),
    search("volcano earthquake sound", ["planet-earth"], "place", "audio"),
    search("sports crowd stadium", ["football", "sports"], "event-person", "audio"),
    search("video game music sound effect", ["video-games"], "piece-film", "audio"),
    search("historic speech", ["history"], "event-person", "audio"),
    cat("Speeches by speaker", ["history"], "event-person", "audio", depth=1),
    search("radio broadcast historic", ["history"], "event-person", "audio"),
    cat("Audio files of national anthems", ["world-geography", "history"], "piece-film", "audio", "pd-music"),
    search("national anthem instrumental", ["world-geography", "music"], "piece-film", "audio", "pd-music"),
    search("classical music recording symphony", ["music"], "piece-film", "audio", "pd-music"),
    search("opera aria recording", ["music", "art-and-literature"], "piece-film", "audio", "pd-music"),
    search("piano sonata public domain", ["music"], "piece-film", "audio", "pd-music"),
    search("folk song historic recording", ["music", "holidays-and-traditions"], "piece-film", "audio", "pd-music"),
    cat("Videos by NASA", ["space"], "video-scene", "video"),
    search("NASA video launch", ["space"], "video-scene", "video"),
    search("space station astronaut video", ["space"], "video-scene", "video"),
    search("rover mars video", ["space"], "video-scene", "video"),
    search("animal video wildlife", ["animals"], "video-scene", "video"),
    cat("Videos of animals", ["animals"], "video-scene", "video"),
    cat("Videos of nature", ["planet-earth", "plants-and-environment"], "video-scene", "video"),
    search("underwater video fish coral", ["animals", "planet-earth"], "video-scene", "video"),
    search("volcano eruption video", ["planet-earth"], "video-scene", "video"),
    search("time-lapse video", ["planet-earth", "plants-and-environment"], "video-scene", "video"),
    search("machine working video", ["inventions-and-technology"], "video-scene", "video"),
    search("train video", ["transport"], "video-scene", "video"),
    search("aircraft takeoff video", ["transport"], "video-scene", "video"),
    search("city timelapse video", ["world-geography", "architecture-and-landmarks"], "video-scene", "video"),
    search("traditional dance video", ["holidays-and-traditions", "music"], "video-scene", "video"),
    search("cooking video", ["food-and-drink"], "video-scene", "video"),
    search("sport video match", ["sports", "football"], "video-scene", "video"),
    search("experiment science video", ["science-and-maths"], "video-scene", "video"),
    search("newsreel", ["history"], "event-person", "video", "pd-film"),
    cat("Newsreels by country", ["history"], "event-person", "video", "pd-film", depth=1),
    cat("Silent films", ["film-tv-and-superheroes", "history"], "piece-film", "video", "pd-film", depth=1),
    search("silent film 1920s", ["film-tv-and-superheroes"], "piece-film", "video", "pd-film"),
    search("historic film footage 1900s", ["history"], "event-person", "video", "pd-film"),
    search("early animation cartoon 1930", ["film-tv-and-superheroes"], "piece-film", "video", "pd-film"),
]

TYPE_OF = {"audio": "audio", "video": "video"}


# --- crawl ---------------------------------------------------------------------

def crawl_titles(seed, limit):
    """File titles of a seed: category crawl (breadth first, depth and subcategory caps) or search."""
    cap = limit or MAX_FILES
    if "query" in seed:
        return commons.search_titles(seed["query"], seed["type"], min(cap, 500))
    titles, seen, level, followed = [], set(), [seed["category"]], 0
    for depth in range(seed["depth"] + 1):
        nxt = []
        for c in level:
            if c in seen:
                continue
            seen.add(c)
            for t in commons.members(c, "file"):
                if t not in titles:
                    titles.append(t)
            if len(titles) >= cap:
                return titles[:cap]
            if depth < seed["depth"] and followed < MAX_SUBCATS:
                subs = commons.members(c, "subcat")[:MAX_SUBCATS - followed]
                followed += len(subs)
                nxt += subs
        level = nxt
    return titles


def fetch_seed(seed, limit):
    titles = crawl_titles(seed, limit)
    records = []
    for i in range(0, len(titles), BATCH):
        records += commons.file_records(titles[i:i + BATCH])
    return records


def raw_path(seed):
    return OUT / "raw" / (re.sub(r"[^A-Za-z0-9]+", "-", seed["id"]).strip("-")[:80] + ".jsonl")


# --- filters ---------------------------------------------------------------------

def norm_title(t):
    t = urllib.parse.unquote(t or "").replace("_", " ")
    return t.removeprefix("File:").strip().lower()


def pool_media():
    """Normalised file titles of every file in a source pool's media or background (page title or file_url)."""
    out = set()
    for f in layout.AUTHORING.glob("data/**/questions*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        for q in data["questions"]:
            for slot in ("media", "background"):
                m = q.get(slot) or {}
                for key in ("source_url", "file_url"):
                    u = m.get(key)
                    if not u:
                        continue
                    base = urllib.parse.unquote(u.split("?")[0])
                    if key == "source_url":
                        out.add(norm_title(base.rsplit("/wiki/", 1)[-1]))
                    else:
                        out.add(norm_title(base.rsplit("/", 1)[-1]))
    return out


def reject(rec, in_pool):
    """The reason a file is filtered out, or None. Order: kind, pool, licence, restriction, length, size."""
    t = TYPE_OF.get(rec["mediatype"])
    if not t:
        return "not audio or video"
    if rec.get("mime") == "audio/midi" or rec["title"].lower().endswith((".mid", ".midi")):
        return "MIDI (no player, no probe)"
    if t == "video" and rec["title"].lower().endswith(".ogg"):
        return "Ogg video named .ogg (ships as audio, decision 185)"
    if norm_title(rec["title"]) in in_pool:
        return "already in a pool"
    if not providers.licence_kind(rec["license"]):
        return "licence not on the allowlist"
    if rec["restrictions"]:
        return "restriction"
    d = rec["duration"] or 0
    if d > MAX_S:
        return f"{t} longer than {MAX_S} s"
    if t == "audio" and d < MIN_AUDIO_S:
        return f"audio shorter than {MIN_AUDIO_S} s"
    if t == "video" and (rec["height"] or 0) < MIN_VIDEO_HEIGHT:
        return f"video below {MIN_VIDEO_HEIGHT}p"
    return None


def apply_filters(by_seed, in_pool):
    """by_seed: [(seed, records)] in seed order. Returns (kept rows, filter counts)."""
    kept, counts, seen = [], Counter(), set()
    for seed, records in by_seed:
        for rec in records:
            key = norm_title(rec["title"])
            if key in seen:
                counts["duplicate across seeds"] += 1
                continue
            seen.add(key)
            why = "type differs from the seed's" if TYPE_OF.get(rec["mediatype"]) not in (None, seed["type"]) else reject(rec, in_pool)
            if why:
                counts[why] += 1
                continue
            t = TYPE_OF[rec["mediatype"]]
            kept.append({**rec, "provider": providers.commons.ID, "licence_kind": providers.licence_kind(rec["license"]), "type": t,
                         "needs_excerpt": (rec["duration"] or 0) > max_seconds(t),
                         "seed": seed["id"], "kind": seed["kind"], "class": seed["class"], "base_categories": seed["cats"]})
    return kept, counts


def tally(kept):
    """Rows per (category, kind, class, type): files, short (<= max_seconds(type)) and needing an excerpt.
    A file counts under each of its seed's categories."""
    rows = defaultdict(lambda: {"files": 0, "short": 0, "excerpt": 0})
    for f in kept:
        for c in f["base_categories"]:
            r = rows[(c, f["kind"], f["class"], f["type"])]
            r["files"] += 1
            r["excerpt" if f["needs_excerpt"] else "short"] += 1
    return [{"category": c, "kind": k, "class": cl, "type": t, **v} for (c, k, cl, t), v in sorted(rows.items())]


def tally_md(kept, rows, counts, calls, seconds):
    lines = ["# Commons media survey", "",
             f"Kept files after filters: {len(kept)} (a file counts once here, under each of its seed's categories in the tables).", ""]
    for t in ("audio", "video"):
        for cls in CLASSES:
            sub = [r for r in rows if r["type"] == t and r["class"] == cls]
            if not sub:
                continue
            lines += [f"## {t}, class {cls}", "", "| category | kind | files | ≤ limit | needs excerpt |", "|---|---|---|---|---|"]
            lines += [f"| {r['category']} | {r['kind']} | {r['files']} | {r['short']} | {r['excerpt']} |" for r in sub]
            lines.append("")
    by_class = Counter((f["type"], f["class"]) for f in kept)
    lines += ["## Kept files per type and class", "", "| type | class | files |", "|---|---|---|"]
    lines += [f"| {t} | {c} | {n} |" for (t, c), n in sorted(by_class.items())]
    lines += ["", "## Filter counts", "", "| filter | files |", "|---|---|"]
    lines += [f"| {k} | {n} |" for k, n in counts.most_common()]
    lines += ["", f"API calls: {calls}; wall time: {seconds / 60:.1f} min (all runs of this crawl; a crawl restarted without --resume counts afresh)", ""]
    return "\n".join(lines)


# --- command ---------------------------------------------------------------------

def cmd_media_survey(args):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "raw").mkdir(exist_ok=True)
    ledger = OUT / "calls.json"  # calls and seconds of all runs, a resumed run adds to it
    before = json.loads(ledger.read_text()) if ledger.exists() and args.resume else {"calls": 0, "seconds": 0}
    calls, start = [0], time.monotonic()
    real_api = commons.api

    def counted(*a, **k):
        calls[0] += 1
        return real_api(*a, **k)
    commons.api = counted
    try:
        by_seed = []
        for n, seed in enumerate(SEEDS, 1):
            path = raw_path(seed)
            if args.resume and path.exists():
                records = [json.loads(l) for l in path.read_text().split("\n") if l]
                progress.say(f"media-survey: {n}/{len(SEEDS)} {seed['id']}: kept, {len(records)} records")
            else:
                records = fetch_seed(seed, args.limit)
                atomic.write_text(path, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
                progress.say(f"media-survey: {n}/{len(SEEDS)} {seed['id']}: {len(records)} records, {calls[0]} calls")
            by_seed.append((seed, records))
    finally:
        commons.api = real_api
    total = {"calls": before["calls"] + calls[0], "seconds": before["seconds"] + round(time.monotonic() - start)}
    atomic.write_text(ledger, json.dumps(total))
    kept, counts = apply_filters(by_seed, pool_media())
    rows = tally(kept)
    atomic.write_text(OUT / "files.jsonl", "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in kept))
    atomic.write_text(OUT / "tally.json", json.dumps({"kept": len(kept), "rows": rows, "filters": dict(counts),
                                                      "api_calls": total["calls"], "seconds": total["seconds"]}, indent=1))
    atomic.write_text(OUT / "tally.md", tally_md(kept, rows, counts, total["calls"], total["seconds"]))
    progress.say(f"media-survey: {len(kept)} files kept, tally at {OUT / 'tally.md'}")


def add_parser(sub):
    p = sub.add_parser("media-survey", help="Commons audio/video supply for media-first questions → work/media-survey/ (plan 201)")
    p.set_defaults(fn=cmd_media_survey, run=None)
    p.add_argument("--limit", type=int, help=f"files per seed (default {MAX_FILES})")
    p.add_argument("--resume", action="store_true", help="keep seeds already fetched")
