#!/usr/bin/env python3
"""Library music into loop files (plan 221); `trivia-music` runs this. Standard library only.

Ported from the sibling project's tools/audio/music.py (~/code/three-days-until-release, decision 199: no import
across repos). Later steps (split, loop, export, check, credits) are added by their own tasks.

  search [--feel F] [--bpm LO-HI] [--instrument I] [--min-length S]   incompetech catalogue
  fetch <title> <id>                       incompetech download to work/music/<id>/original.mp3 + record
  record <id> --file P --page U --title T --author A --licence SPDX   another library, file downloaded by hand
  record <id> --licence SPDX --read-on-page                            confirm the licence read on the track page

<id> is <set>-<piece>, lower case, e.g. carefree-try. Records: authoring/data/music/<id>.json (committed).
Work files: work/music/<id>/ (gitignored). Licences: CC0, PD, CC BY 3.0/4.0 only (decision 733); no Freesound API
(decision 82).
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import layout  # noqa: E402

BASE = "https://incompetech.com/music/royalty-free"
LICENCES = {  # decision 733: SPDX -> (name, url)
    "CC0-1.0": ("CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "PD": ("public domain", ""),
    "CC-BY-3.0": ("Creative Commons: By Attribution 3.0", "https://creativecommons.org/licenses/by/3.0/"),
    "CC-BY-4.0": ("Creative Commons: By Attribution 4.0", "https://creativecommons.org/licenses/by/4.0/"),
}
ADAPTED = "Adapted: cut to a loop, split into layers and remixed per variant, loudness changed."


def die(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def check_id(i: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", i):
        die(f"id must be <set>-<piece>, lower case: {i!r}", 2)
    return i


def record_path(i: str) -> Path:
    return layout.MUSIC_RECORDS / f"{i}.json"


def work_dir(i: str) -> Path:
    return layout.MUSIC_WORK / i


def get(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "trivia-music"}), timeout=120).read()


def catalogue() -> list:
    f = layout.MUSIC_WORK / "pieces.json"
    if not f.exists():
        layout.MUSIC_WORK.mkdir(parents=True, exist_ok=True)
        f.write_bytes(get(f"{BASE}/pieces.json"))
    return json.loads(f.read_text())


def licence_problem(spdx: str) -> str | None:
    if spdx not in LICENCES:
        return f"licence {spdx!r} not allowed (decision 733: only {', '.join(LICENCES)})"
    return None


def credit_line(title: str, author: str, spdx: str, page: str = "") -> str:
    name, url = LICENCES[spdx]
    if spdx == "PD":
        return f'"{title}" by {author}, {name}. {ADAPTED}'
    return f'"{title}" by {author}{f" ({page})" if page else ""}, licensed under {name}, {url} . {ADAPTED}'


def load(i: str) -> dict:
    f = record_path(i)
    if not f.is_file():
        die(f"no record {f}: run fetch or record first", 2)
    return json.loads(f.read_text())


def save(rec: dict):
    layout.MUSIC_RECORDS.mkdir(parents=True, exist_ok=True)
    record_path(rec["id"]).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")


def require_confirmed(rec: dict):
    """Later steps call this: the licence must be allowed and read on the track page."""
    spdx = rec.get("licence", {}).get("spdx", "")
    bad = licence_problem(spdx)
    if bad:
        die(f"{rec['id']}: {bad}")
    if not rec["licence"].get("read_on_page"):
        die(f"{rec['id']}: licence not confirmed; open {rec['page']}, read its licence line, then "
            f"`trivia-music record {rec['id']} --licence <spdx> --read-on-page`")


def new_record(i, library, title, author, page, download, sha, spdx, listed) -> dict:
    return {
        "id": i, "library": library, "title": title, "author": author, "page": page, "download": download,
        "sha256": sha, "downloaded": str(date.today()),
        "licence": {"spdx": spdx, "read_on_page": None},
        "listed": listed, "adapted": ADAPTED, "credit": credit_line(title, author, spdx, page),
        "loop": {}, "exports": {},
    }


def cmd_search(a) -> int:
    lo, hi = (0.0, 1e9)
    if a.bpm:
        m = re.fullmatch(r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)", a.bpm)
        if not m:
            die("--bpm LO-HI, e.g. 80-110", 2)
        lo, hi = float(m[1]), float(m[2])
    n = 0
    for p in catalogue():
        try:
            bpm = float(p.get("bpm") or 0)
        except ValueError:
            bpm = 0.0
        if not lo <= bpm <= hi:
            continue
        if a.feel and a.feel.lower() not in str(p.get("feel", "")).lower():
            continue
        if a.instrument and a.instrument.lower() not in str(p.get("instruments", "")).lower():
            continue
        if a.min_length and length_s(p.get("length")) < a.min_length:
            continue
        print(f"{p['title']}\t{p.get('bpm')}\t{p.get('feel')}\t{p.get('instruments', '')}\t{p.get('length')}")
        n += 1
    print(f"{n} pieces", file=sys.stderr)
    return 0


def length_s(v) -> float:
    """'3:25' or '205' -> seconds."""
    try:
        parts = [float(x) for x in str(v).split(":")]
    except ValueError:
        return 0.0
    s = 0.0
    for x in parts:
        s = s * 60 + x
    return s


def cmd_fetch(a) -> int:
    check_id(a.id)
    if record_path(a.id).exists():
        die(f"record {a.id} exists")
    row = next((p for p in catalogue() if p["title"].lower() == a.title.lower()), None)
    if not row:
        die(f"no incompetech piece called {a.title!r}")
    w = work_dir(a.id)
    w.mkdir(parents=True, exist_ok=True)
    mp3 = w / "original.mp3"
    url = f"{BASE}/mp3-royaltyfree/{urllib.parse.quote(row['filename'])}"
    if not mp3.exists():
        mp3.write_bytes(get(url))
    page = f"https://incompetech.com/music/royalty-free/index.html?isrc={row['isrc']}"
    rec = new_record(a.id, "incompetech", row["title"], "Kevin MacLeod", page, url,
                     hashlib.sha256(mp3.read_bytes()).hexdigest(), "CC-BY-4.0",
                     {"bpm": row.get("bpm"), "feel": row.get("feel")})
    save(rec)
    print(f"{mp3}\nlength {row.get('length')}, listed bpm {row.get('bpm')}, feel {row.get('feel')}\n"
          f"wrote {record_path(a.id)}\nNOT confirmed: read the licence line on {page}, then\n"
          f"  trivia-music record {a.id} --licence <spdx> --read-on-page")
    return 0


def cmd_record(a) -> int:
    check_id(a.id)
    bad = licence_problem(a.licence)
    if bad:
        die(bad)
    if a.file:
        missing = [k for k in ("page", "title", "author") if not getattr(a, k)]
        if missing:
            die("--file needs --" + ", --".join(missing), 2)
        src = Path(a.file)
        if not src.is_file():
            die(f"no file {src}")
        w = work_dir(a.id)
        w.mkdir(parents=True, exist_ok=True)
        dst = w / f"original{src.suffix.lower()}"
        shutil.copyfile(src, dst)
        rec = new_record(a.id, a.library or "other", a.title, a.author, a.page, a.download or "",
                         hashlib.sha256(dst.read_bytes()).hexdigest(), a.licence, {"bpm": a.bpm, "feel": a.feel})
    else:
        rec = load(a.id)
        rec["licence"]["spdx"] = a.licence
        rec["credit"] = credit_line(rec["title"], rec["author"], a.licence, rec["page"])
    rec["licence"]["read_on_page"] = str(date.today()) if a.read_on_page else None
    save(rec)
    print(f"wrote {record_path(a.id)}" + ("" if a.read_on_page else "\nNOT confirmed: add --read-on-page after reading the page"))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="trivia-music", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("search", help="search the incompetech catalogue")
    p.add_argument("--feel"); p.add_argument("--bpm", help="LO-HI"); p.add_argument("--instrument")
    p.add_argument("--min-length", type=float, help="seconds")
    p = sub.add_parser("fetch", help="incompetech download + record"); p.add_argument("title"); p.add_argument("id")
    p = sub.add_parser("record", help="record a track (file by hand) or confirm its licence")
    p.add_argument("id"); p.add_argument("--file"); p.add_argument("--page"); p.add_argument("--title")
    p.add_argument("--author"); p.add_argument("--licence", required=True, help="CC0-1.0, PD, CC-BY-3.0, CC-BY-4.0")
    p.add_argument("--read-on-page", action="store_true", help="the licence was read on the track page")
    p.add_argument("--library"); p.add_argument("--download"); p.add_argument("--bpm"); p.add_argument("--feel")
    a = ap.parse_args(argv)
    return {"search": cmd_search, "fetch": cmd_fetch, "record": cmd_record}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
