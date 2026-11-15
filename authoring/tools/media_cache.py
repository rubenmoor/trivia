"""The media cache (D-17): picked media files, read-only for the game (moved from app/server/, plan 99).

Files are named after their URL: <TRIVIA_MEDIA or media/>/<sha1(file_url)[:16]><ext>. The game serves only
URLs that a question in the pool uses (`pool_urls`, app/desktop/resolve.mjs) and never downloads;
`trivia-media sync` (authoring/tools/download.py) fills the cache ahead of game night.
"""
import hashlib, json, re, subprocess, threading, urllib.parse
from pathlib import Path

from paths import MEDIA, pool_files


def cache_path(url):
    """Where the file for url is cached. The name depends on the URL alone (D-17); same as app/desktop/resolve.mjs cacheName."""
    ext = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,5}", ext):
        ext = ".bin"
    return MEDIA / (hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ext)


# Chromium doesn't decode these; the review page gets a WebM copy (task 2053).
NEEDS_PLAYABLE = {".ogv", ".mpg", ".mpeg", ".mov", ".mkv", ".mp4"}
# Same args as app/desktop/media-formats.mjs VIDEO plus playable.mjs FAST.
FFMPEG_VIDEO = [
    "-map", "0:v:0", "-map", "0:a:0?",
    "-vf", "scale=w=min(1920\\,iw):h=min(1080\\,ih):force_original_aspect_ratio=decrease:force_divisible_by=2",
    "-c:v", "libvpx-vp9", "-crf", "33", "-b:v", "0", "-row-mt", "1", "-deadline", "good", "-cpu-used", "2",
    "-c:a", "libopus", "-b:a", "96k", "-deadline", "realtime", "-cpu-used", "8",
]
_encode_lock = threading.Lock()


def playable_path(url):
    """The file to serve for url: the cached one, or for Theora and co a WebM copy at media/playable/<stem>.webm
    (same name as app/desktop/playable.mjs playableName), made on first use. Raises OSError when ffmpeg fails."""
    src = cache_path(url)
    if src.suffix not in NEEDS_PLAYABLE or not src.is_file():
        return src
    dst = src.parent / "playable" / (src.stem + ".webm")
    with _encode_lock:
        if not dst.is_file():
            dst.parent.mkdir(exist_ok=True)
            tmp = dst.with_name(dst.stem + ".part.webm")
            r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src), *FFMPEG_VIDEO,
                                "-map_metadata", "-1", str(tmp)], capture_output=True, text=True)
            if r.returncode:
                tmp.unlink(missing_ok=True)
                raise OSError("convert failed: " + (r.stderr.strip().splitlines() or ["ffmpeg"])[0])
            tmp.replace(dst)
    return dst


def picked(q):
    """(label, file_url) for every picked file of a question."""
    out = [(q["id"], q["media"].get("file_url"))]
    if q.get("background"):
        out.append((f"{q['id']} background", q["background"].get("file_url")))
    return [(label, url) for label, url in out if url]


_urls = {}  # pool path -> (mtime_ns, size, urls)


def pool_urls(pool=None):
    """Every file_url in the pool (None: every exported pool file, packs too): the servers only serve these.
    Re-read when the file changes."""
    if pool is None:
        return set().union(*map(pool_urls, pool_files()))
    st = Path(pool).stat()
    key = (st.st_mtime_ns, st.st_size)
    hit = _urls.get(str(pool))
    if hit and hit[0] == key:
        return hit[1]
    qs = json.loads(Path(pool).read_text(encoding="utf-8"))["questions"]
    urls = {url for q in qs for _, url in picked(q)}
    _urls[str(pool)] = (key, urls)
    return urls
