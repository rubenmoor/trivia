"""Which cached media files to keep, and `trivia-media sync --prune` (task 2139; the cache itself: media_cache.py)."""
import json, re
from pathlib import Path

from batches import unfinished_runs
from layout import CANDIDATES, SOURCE_POOL, WORK
from media_cache import MEDIA, cache_path, pool_urls


_FILE_URL = re.compile(r'"file_url":\s*"([^"]+)"')


def _urls_in(path):
    return set(_FILE_URL.findall(Path(path).read_text(encoding="utf-8", errors="replace")))


def keep_urls():
    """Every file_url the cache must keep (task 2139): picks of every authoring pool (base and bundles
    in questions.json, translations questions.<locale>.json) and every file an unfinished `qgen batch` run
    still references (its files, plus the candidates of its questions in work/media/)."""
    urls = set()
    for pool in SOURCE_POOL.parent.glob("questions*.json"):
        urls |= pool_urls(pool)
    for name in unfinished_runs():
        run = WORK / name
        for f in run.rglob("*"):
            if f.is_file() and f.suffix in (".json", ".jsonl") and f.name != "calls.jsonl":
                urls |= _urls_in(f)
        ids_file = run / "ids.json"
        ids = set(json.loads(ids_file.read_text(encoding="utf-8")).values()) if ids_file.is_file() else set()
        for qid in ids:
            if (CANDIDATES / f"{qid}.json").is_file():
                urls |= _urls_in(CANDIDATES / f"{qid}.json")
    return urls


def prune(dry_run=False):
    """Delete cached files no keep_urls() pick needs (also stray .part files); returns (count, bytes)."""
    if not MEDIA.exists():
        return 0, 0
    keep = {cache_path(u).name for u in keep_urls()}
    stale = [f for f in MEDIA.iterdir() if f.is_file() and f.name not in keep]
    size = sum(f.stat().st_size for f in stale)
    if not dry_run:
        for f in stale:
            f.unlink()
    return len(stale), size
