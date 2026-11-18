#!/usr/bin/env python3
"""Sound effect files from CC0, public domain or CC BY recordings (plan 223); `trivia-sfx` runs this. Standard library + ffmpeg.

  record <name> --file P --page U --title T --author A --licence SPDX --cue C [--cue C ...]
         [--class effect|jingle|long] [--start S] [--end S] [--gain DB] [--stereo] [--read-on-page] [--library L] [--download U]
                                  file downloaded by hand into work/sfx/<group>/; record authoring/data/sfx/<name>.json
                                  (source page, SHA-256, licence and the date it was read on the page, cues, cut)
  record <name> --licence SPDX --read-on-page   confirm the licence read on the source page
  convert <name>                  the cut + plan 32's chain -> app/client/public/audio/<name>.m4a: trim silence, short
                                  fade-out, loudnorm -16 LUFS / -1.5 dBTP (two passes), mono AAC 80k (--stereo in the record)
  check [<name> ...]              per file: -16 +-1 LUFS (longer than 0.4 s; shorter clips: true peak only), true peak <= -1.5 dBTP, size budget of its
                                  class (effect 40 kB, jingle 80 kB, long 100 kB), licence allowed and read; exit 0/1
  credits [--check]               effect rows of app/client/public/audio/CREDITS.md from the records, between their own
                                  marker comments (hand rows and music rows untouched); --check: rows and records match

<name> is the file name without `.m4a`: lower case ASCII Spanish words joined by `-`, e.g. `golpe-madera`.
Licences and the credits writer are music.py's (decision 199). Licences: CC0, PD, CC BY 3.0/4.0 only (decision 733); no
Freesound API (decision 82). Work files: work/sfx/ (gitignored). Plan 223, plans/25-sound.md "Effects".
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "music"))
import layout  # noqa: E402
import music  # noqa: E402  (records' licence allowlist, credits writer: decision 199)

CLASSES = {"effect": 40_000, "jingle": 80_000, "long": 100_000}  # bytes per file (plan 223)
TARGET_LUFS, TOLERANCE, TRUE_PEAK = -16.0, 1.0, -1.5
MIN_LOUD_S = 0.4  # shorter clips have no integrated loudness (one 400 ms gating block): peak-normalised
FADE_S = 0.05
PEAK_SHORT = -2.5  # dBTP target of clips under MIN_LOUD_S
BEGIN = "<!-- trivia-sfx credits: begin (generated, do not edit) -->"
END = "<!-- trivia-sfx credits: end -->"
ADAPTED = "Adapted: cut, silence trimmed, faded, loudness changed."
die = music.die


def check_name(n: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n):
        die(f"name must be lower case ASCII words joined by '-': {n!r}", 2)
    return n


def record_path(n: str) -> Path:
    return layout.SFX_RECORDS / f"{n}.json"


def out_path(n: str) -> Path:
    return layout.AUDIO / f"{n}.m4a"


def load(n: str) -> dict:
    f = record_path(n)
    if not f.is_file():
        die(f"no record {f}: run record first", 2)
    return json.loads(f.read_text())


def save(rec: dict):
    layout.SFX_RECORDS.mkdir(parents=True, exist_ok=True)
    record_path(rec["name"]).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")


def credit(rec: dict) -> str:
    return music.credit_line(rec["title"], rec["author"], rec["licence"]["spdx"], rec["page"]).replace(music.ADAPTED, ADAPTED)


def cmd_record(a) -> int:
    check_name(a.name)
    if bad := music.licence_problem(a.licence):
        die(bad)
    if a.file:
        missing = [k for k in ("page", "title", "author") if not getattr(a, k)]
        if missing or not a.cue:
            die("--file needs --" + ", --".join(missing + (["cue"] if not a.cue else [])), 2)
        src = Path(a.file)
        if not src.is_file():
            die(f"no file {src}")
        w = layout.SFX_WORK / "originals"
        w.mkdir(parents=True, exist_ok=True)
        dst = w / f"{a.name}{src.suffix.lower()}"
        shutil.copyfile(src, dst)
        rec = {
            "name": a.name, "library": a.library or "other", "title": a.title, "author": a.author, "page": a.page,
            "download": a.download or "", "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
            "downloaded": str(date.today()), "licence": {"spdx": a.licence, "read_on_page": None},
            "cues": a.cue, "class": a.cls, "stereo": a.stereo,
            "cut": {"start": a.start, "end": a.end, "gain_db": a.gain}, "adapted": ADAPTED,
        }
    else:
        rec = load(a.name)
        rec["licence"]["spdx"] = a.licence
    rec["credit"] = credit(rec)
    rec["licence"]["read_on_page"] = str(date.today()) if a.read_on_page else None
    save(rec)
    print(f"wrote {record_path(a.name)}" + ("" if a.read_on_page else "\nNOT confirmed: add --read-on-page after reading the page"))
    return 0


def original(n: str) -> Path:
    found = sorted((layout.SFX_WORK / "originals").glob(f"{n}.*"))
    if not found:
        die(f"no original for {n} in {layout.SFX_WORK / 'originals'}: run record --file first", 2)
    return found[0]


def ffmpeg(*args) -> str:
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        die(f"ffmpeg: {r.stderr[-600:]}")
    return r.stderr


def duration(f: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def measure(f: Path) -> tuple[float, float]:
    """(integrated LUFS, true peak dBTP) of the decoded file."""
    err = ffmpeg("-i", str(f), "-af", "ebur128=peak=true", "-f", "null", "-")
    summary = err[err.rindex("Summary:"):]
    lufs = float(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summary)[1])
    tp = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary)[1])
    return lufs, tp


TRIM = "silenceremove=start_periods=1:start_threshold=-50dB:detection=peak"


def convert(rec: dict, src: Path, dst: Path):
    cut, work = rec["cut"], layout.SFX_WORK / "tmp"
    work.mkdir(parents=True, exist_ok=True)
    ch = "2" if rec.get("stereo") else "1"
    pre = [] if cut.get("start") is None else ["-ss", str(cut["start"])]
    pre += [] if cut.get("end") is None else ["-to", str(cut["end"])]
    gain = f",volume={cut['gain_db']}dB" if cut.get("gain_db") else ""
    trimmed = work / f"{rec['name']}-trim.wav"
    ffmpeg(*pre, "-i", str(src), "-af", f"{TRIM},areverse,{TRIM},areverse{gain}", "-ac", ch, "-ar", "44100", str(trimmed))
    d = duration(trimmed)
    if d <= 0:
        die(f"{rec['name']}: nothing left after trimming silence")
    fade = f"afade=t=out:st={max(d - min(FADE_S, d / 4), 0):.4f}:d={min(FADE_S, d / 4):.4f}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if d <= MIN_LOUD_S:  # too short to measure loudness: true peak to -2.5 dBTP
        faded = work / f"{rec['name']}-fade.wav"
        ffmpeg("-i", str(trimmed), "-af", fade, str(faded))
        db = PEAK_SHORT - measure(faded)[1]
        faded.unlink()
        for _ in range(3):  # AAC can overshoot the peak: encode again, lower
            ffmpeg("-i", str(trimmed), "-af", f"{fade},volume={db:.2f}dB", "-c:a", "aac", "-b:a", "80k", "-ar", "44100", "-ac", ch, str(dst))
            if (tp := measure(dst)[1]) <= TRUE_PEAK - 0.1:
                break
            db -= tp - TRUE_PEAK + 0.5
    else:
        norm = f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA=11"
        err = ffmpeg("-i", str(trimmed), "-af", f"{fade},{norm}:print_format=json", "-f", "null", "-")
        m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
        lin = (f"{norm}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
               f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
        ffmpeg("-i", str(trimmed), "-af", f"{fade},{lin}", "-c:a", "aac", "-b:a", "80k", "-ar", "44100", "-ac", ch, str(dst))
    trimmed.unlink()


def cmd_convert(a) -> int:
    check_name(a.name)
    rec = load(a.name)
    require_confirmed(rec)
    convert(rec, original(a.name), out_path(a.name))
    return check_names([a.name])


def require_confirmed(rec: dict):
    if bad := music.licence_problem(rec.get("licence", {}).get("spdx", "")):
        die(f"{rec['name']}: {bad}")
    if not rec["licence"].get("read_on_page"):
        die(f"{rec['name']}: licence not confirmed; open {rec['page']}, read its licence line, then "
            f"`trivia-sfx record {rec['name']} --licence <spdx> --read-on-page`")


def problems(rec: dict, f: Path) -> list:
    bad = []
    if lic := music.licence_problem(rec.get("licence", {}).get("spdx", "")):
        bad.append(lic)
    elif not rec["licence"].get("read_on_page"):
        bad.append("licence not confirmed on the source page")
    cls = rec.get("class", "effect")
    if cls not in CLASSES:
        bad.append(f"class {cls!r} not one of {', '.join(CLASSES)}")
    if not f.is_file():
        return bad + [f"no file {f}"]
    if cls in CLASSES and f.stat().st_size > CLASSES[cls]:
        bad.append(f"{f.stat().st_size} bytes > {CLASSES[cls]} ({cls})")
    lufs, tp = measure(f)
    if duration(f) > MIN_LOUD_S and abs(lufs - TARGET_LUFS) > TOLERANCE:
        bad.append(f"{lufs:.1f} LUFS outside {TARGET_LUFS:g} +-{TOLERANCE:g}")
    if tp > TRUE_PEAK:
        bad.append(f"true peak {tp:.2f} dBTP > {TRUE_PEAK}")
    print(f"{f.name}: {duration(f):.2f} s, {f.stat().st_size} B, {lufs:.1f} LUFS, {tp:.2f} dBTP ({cls})")
    return bad


def check_names(names: list) -> int:
    n_bad = 0
    for n in names:
        for b in problems(load(n), out_path(n)):
            print(f"FAIL {n}: {b}", file=sys.stderr)
            n_bad += 1
    print(f"check: {len(names)} files, " + ("FAILED" if n_bad else "ok"))
    return 1 if n_bad else 0


def cmd_check(a) -> int:
    return check_names(a.names or sorted(f.stem for f in layout.SFX_RECORDS.glob("*.json")))


def credit_rows() -> list:
    rows = []
    for f in sorted(layout.SFX_RECORDS.glob("*.json")):
        rec = json.loads(f.read_text())
        spdx = rec.get("licence", {}).get("spdx", "")
        if lic := music.licence_problem(spdx):
            die(f"{rec['name']}: {lic}")
        name, url = music.LICENCES[spdx]
        lic_cell = name if spdx == "PD" else f"[{name}]({url})"
        file = f"{rec['name']}.m4a"
        used = f"Sound effect {', '.join(f'`{c}`' for c in rec['cues'])} (adapted: cut, faded, loudness changed)"
        rows.append((file, f"| `{file}` | {used} | [{rec['title']}]({rec['page']}) ({rec['library']}) | {rec['author']} | {lic_cell} |"))
    return rows


def cmd_credits(a) -> int:
    return music.sync_credits(credit_rows(), a.check, "trivia-sfx", BEGIN, END)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="trivia-sfx", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("record", help="record a source file (by hand) or confirm its licence"); p.add_argument("name")
    p.add_argument("--file"); p.add_argument("--page"); p.add_argument("--title"); p.add_argument("--author")
    p.add_argument("--licence", required=True, help="CC0-1.0, PD, CC-BY-3.0, CC-BY-4.0")
    p.add_argument("--cue", action="append", help="the cue(s) this file plays for")
    p.add_argument("--class", dest="cls", default="effect", choices=list(CLASSES))
    p.add_argument("--start", type=float); p.add_argument("--end", type=float); p.add_argument("--gain", type=float, help="dB")
    p.add_argument("--stereo", action="store_true"); p.add_argument("--read-on-page", action="store_true")
    p.add_argument("--library"); p.add_argument("--download")
    p = sub.add_parser("convert", help="cut + chain -> app/client/public/audio/<name>.m4a"); p.add_argument("name")
    p = sub.add_parser("check", help="hard checks of the files"); p.add_argument("names", nargs="*")
    p = sub.add_parser("credits", help="effect rows of CREDITS.md from the records"); p.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    return {"record": cmd_record, "convert": cmd_convert, "check": cmd_check, "credits": cmd_credits}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
