"""`qgen batch --media-first`'s file inventory and ledger (plan 203, step 2; the steps themselves come in later tasks).

A run starts from surveyed Commons files (`media_survey`: work/media-survey/files.jsonl). The ledger
work/media-first/files.jsonl holds every file any run triaged, so none is offered twice. `select` picks a run's
files, seed by seed in yield order, and writes the queue to the run dir so a resume takes the same files.
"""
import json
from collections import defaultdict
from types import SimpleNamespace

import atomic, layout
import media_survey

MF_DESIGNED = 120        # designed questions per run (≈ 100 approved at the pilot's look share)
SKIP_AFTER = 15          # a seed with 0 worth it after this many triaged files is skipped from then on
MAX_PER_SEED = 30        # files of one seed in a run's queue (spread over seeds)
PRIOR = 0.24             # pilot's worth-it share (authoring/reports/media-first-feasibility.md), smooths seed yield
SURVEY_FILES = media_survey.OUT / "files.jsonl"
LEDGER = layout.WORK / "media-first" / "files.jsonl"
QUEUE = "media-first-files.jsonl"  # in the run dir
# Zero-yield seeds of the feasibility report: Lingua Libre, newsreels, church bells, trains/cars/aircraft audio,
# ambience, bird-song search, city names. Skipped until the ledger shows one worth it.
ZERO_YIELD = {
    "cat:Lingua Libre pronunciation", "q:audio:pronunciation of city name", "q:audio:spoken language sample",
    "q:video:newsreel", "cat:Newsreels by country", "q:audio:church bells",
    "q:audio:train sound", "q:audio:car engine sound", "q:audio:aircraft sound", "q:audio:machine noise",
    "q:audio:ocean waves wind", "q:audio:rainforest sounds", "q:audio:city ambience street sounds",
    "q:audio:bird song",
}


def read_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").split("\n") if l] if path.exists() else []


def write_jsonl(path, rows):
    atomic.write_text(path, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def ledger():
    """Ledger rows: {title, seed, run, worth (bool), verdict}."""
    return read_jsonl(LEDGER)


def record(run, rows):
    """Add triaged files to the ledger: rows {title, seed, worth, verdict}; a title already in it is kept as is."""
    with atomic.locked(LEDGER):
        have = ledger()
        known = {media_survey.norm_title(r["title"]) for r in have}
        new = [{**r, "run": run} for r in rows if media_survey.norm_title(r["title"]) not in known]
        if new:
            write_jsonl(LEDGER, have + new)
    return len(new)


def pilot_rows():
    """The media pilot's triaged files (aided verdict, else blind): {title, seed, worth}."""
    by = {}
    for f in sorted((layout.WORK / "media-pilot").glob("*/triage.jsonl")):
        for r in read_jsonl(f):
            if r["title"] not in by or r.get("mode") == "aided":
                by[r["title"]] = {"title": r["title"], "seed": r["seed"], "worth": bool(r["worth"])}
    return list(by.values())


def seed_stats(rows):
    """{seed: [triaged, worth]} over rows."""
    st = defaultdict(lambda: [0, 0])
    for r in rows:
        st[r["seed"]][0] += 1
        st[r["seed"]][1] += bool(r["worth"])
    return st


def seed_yield(stat):
    """Worth-it share, smoothed toward the pilot's overall share."""
    n, w = stat
    return (w + PRIOR * 2) / (n + 2)


def skipped(seed, stats):
    n, w = stats.get(seed, (0, 0))
    return w == 0 and (n >= SKIP_AFTER or seed in ZERO_YIELD)


def used_titles(rows=None):
    return {media_survey.norm_title(r["title"]) for r in (pilot_rows() + ledger() if rows is None else rows)}


def survey_files(crawl=True):
    """The survey's kept files; a missing file is crawled first (resumable: `qgen media-survey --resume`)."""
    if not SURVEY_FILES.exists() and crawl:
        media_survey.cmd_media_survey(SimpleNamespace(limit=None, resume=True))
    return read_jsonl(SURVEY_FILES)


def inventory(files, rows, in_pool, limit=None):
    """Files a run may triage, in queue order: not triaged before, not in a pool, seed not skipped; seeds by
    descending yield (ties by id), at most MAX_PER_SEED per seed, survey order within a seed. `limit` cuts the queue."""
    stats = seed_stats(rows)
    seen = used_titles(rows)
    by = defaultdict(list)
    for f in files:
        key = media_survey.norm_title(f["title"])
        if key in seen or key in in_pool or skipped(f["seed"], stats):
            continue
        by[f["seed"]].append(f)
    order = sorted(by, key=lambda s: (-seed_yield(stats.get(s, (0, 0))), s))
    queue = [f for s in order for f in by[s][:MAX_PER_SEED]]
    return queue[:limit] if limit else queue


def select(run_dir, limit=None):
    """The run's queue: written to run_dir on first call, read back after (a resume takes the same files)."""
    path = run_dir / QUEUE
    if path.exists():
        return read_jsonl(path)
    queue = inventory(survey_files(), pilot_rows() + ledger(), media_survey.pool_media(), limit)
    write_jsonl(path, queue)
    return queue


def remaining(run_dir, run):
    """The queue's files not yet in the ledger and whose seed isn't skipped by now (the ledger grows during the run)."""
    done = {media_survey.norm_title(r["title"]) for r in ledger() if r["run"] == run}
    stats = seed_stats(pilot_rows() + ledger())
    return [f for f in select(run_dir) if media_survey.norm_title(f["title"]) not in done and not skipped(f["seed"], stats)]
