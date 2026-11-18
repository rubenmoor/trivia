#!/usr/bin/env python3
"""Library music into loop files (plan 221); `trivia-music` runs this. Standard library only.

Ported from the sibling project's tools/audio/music.py and spikes/music-library/setup.sh
(~/code/three-days-until-release, decision 199: no import across repos). `loop` imports music_loop.py (numpy,
librosa, soundfile). Later steps (check, credits) are added by their own tasks.

  search [--feel F] [--bpm LO-HI] [--instrument I] [--min-length S]   incompetech catalogue
  fetch <title> <id>                       incompetech download to work/music/<id>/original.mp3 + record
  record <id> --file P --page U --title T --author A --licence SPDX   another library, file downloaded by hand
  record <id> --licence SPDX --read-on-page                            confirm the licence read on the track page
  setup                                    Demucs venv work/music/venv (uv, torch, demucs 4.1; CUDA if the driver is there)
  split <id>                               Demucs htdemucs: drums, bass, other, vocals -> work/music/<id>/stems/htdemucs/
  loop <id> [--bars 8] [--bpm B] [--whole] N-bar loop of the stems (--whole: of the unsplit mix), sum at -18 LUFS
                                           -> work/music/<id>/loop/*.wav, info.json, the record's loop slot; exit 1 = rejected
  export <id> <out-dir> --variant NAME=RECIPE ... [--set S]
                                           one musica-<set>-<name>.m4a per variant (AAC LC 96 kbit/s 44.1 kHz stereo, as
                                           plan 33's loops), all the same length, the loop's gain, never per-layer
                                           normalised; written into the record's exports. Recipe: layers joined by +,
                                           a dB cut after a layer (bass+other-3), a leading + = the previous variant
                                           plus (+drums), full = all layers; --whole record: full = the loop, @<bar> =
                                           another stretch of the track from that bar (same length, checked like the loop)

<id> is <set>-<piece>, lower case, e.g. carefree-try. Records: authoring/data/music/<id>.json (committed).
Work files: work/music/<id>/ (gitignored). Licences: CC0, PD, CC BY 3.0/4.0 only (decision 733); no Freesound API
(decision 82).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
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
GPU_LIB = Path("/run/opengl-driver/lib")  # NixOS driver libs; present = CUDA torch
VENV_PY = "3.12"  # demucs 4.1 / torch wheels
TORCH_INDEX = "https://download.pytorch.org/whl/"
STEMS = ("drums", "bass", "other", "vocals")
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


def venv_dir() -> Path:
    return layout.MUSIC_WORK / "venv"


def venv_py() -> Path:
    py = venv_dir() / "bin" / "python"
    if not py.exists():
        die(f"no Demucs venv at {venv_dir()}: run `trivia-music setup`", 3)
    return py


def device() -> str:
    return "cuda" if GPU_LIB.exists() else "cpu"


def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if k not in ("LD_LIBRARY_PATH", "PYTHONPATH")}


def split_env() -> dict:
    """LD_LIBRARY_PATH as the sibling: driver libs plus the C++ runtime torch needs on NixOS."""
    env = clean_env()
    if device() == "cuda":
        libs = [str(GPU_LIB)]
        cc = subprocess.run(["nix", "eval", "--raw", "nixpkgs#stdenv.cc.cc.lib.outPath"], capture_output=True, text=True).stdout
        if cc:
            libs.append(f"{cc}/lib")
        env["LD_LIBRARY_PATH"] = ":".join(libs)
    return env


def setup_commands() -> list:
    v = str(venv_dir())
    idx = TORCH_INDEX + ("cu128" if device() == "cuda" else "cpu")
    return [["uv", "venv", "--python", VENV_PY, v],
            ["uv", "pip", "install", "-p", f"{v}/bin/python", "torch", "torchaudio", "--index-url", idx],
            ["uv", "pip", "install", "-p", f"{v}/bin/python", "demucs", "numpy", "soundfile"]]  # demucs 4.1 imports numpy but does not list it


def cmd_setup(a) -> int:
    if venv_dir().exists() and not a.force:
        print(f"{venv_dir()} exists (--force to rebuild)")
        return 0
    if a.force:
        shutil.rmtree(venv_dir(), ignore_errors=True)
    layout.MUSIC_WORK.mkdir(parents=True, exist_ok=True)
    for c in setup_commands():
        if subprocess.run(c, env=clean_env()).returncode:
            die(f"failed: {' '.join(c)}")
    print(f"Demucs venv ready ({device()}): {venv_dir()}")
    return 0


def original(i: str) -> Path:
    found = sorted(work_dir(i).glob("original.*"))
    if not found:
        die(f"no original in {work_dir(i)}: run fetch or record --file first", 2)
    return found[0]


def split_command(i: str) -> list:
    return [str(venv_py()), "-m", "demucs", "-n", "htdemucs", "-d", device(), "--int24",
            "-o", str(work_dir(i) / "stems"), "--filename", "{stem}.{ext}", str(original(i))]


def cmd_split(a) -> int:
    check_id(a.id)
    require_confirmed(load(a.id))
    cmd = split_command(a.id)
    t0 = time.time()
    if subprocess.run(cmd, env=split_env()).returncode:
        die("demucs failed")
    out = work_dir(a.id) / "stems" / "htdemucs"
    missing = [s for s in STEMS if not (out / f"{s}.wav").is_file()]
    if missing:
        die(f"demucs wrote no {', '.join(missing)} in {out}")
    print(f"split {a.id} on {device()} in {time.time() - t0:.1f} s -> {out}")
    return 0


def stems_dir(i: str) -> Path:
    return work_dir(i) / "stems" / "htdemucs"


def listed_bpm(rec: dict) -> float | None:
    try:
        return float(rec.get("listed", {}).get("bpm") or 0) or None
    except ValueError:
        return None


LOOP_KEYS = ("bpm", "bars", "whole", "start_s", "start_bar", "downbeat_s", "loop_s", "gain_db", "lufs", "true_peak",
             "comb_score", "repeat_similarity", "seam_jump_vs_mean_step")


def cmd_loop(a) -> int:
    check_id(a.id)
    rec = load(a.id)
    require_confirmed(rec)
    listed = listed_bpm(rec)
    hint = a.bpm or listed
    if not hint:
        die(f"{a.id}: no listed bpm in the record: pass --bpm", 2)
    if not a.whole and not all((stems_dir(a.id) / f"{s}.wav").is_file() for s in STEMS):
        die(f"no stems in {stems_dir(a.id)}: run `trivia-music split {a.id}` or pass --whole", 2)
    import music_loop as ml  # numpy, librosa, soundfile: only this step needs them
    t0 = time.time()
    layers = {"full": ml.decode(original(a.id))} if a.whole else ml.load_stems(stems_dir(a.id))
    loops, info = ml.find(layers, hint, a.bars, listed)
    info["seconds"] = round(time.time() - t0, 1)
    out = work_dir(a.id) / "loop"
    shutil.rmtree(out, ignore_errors=True)
    if not info["rejected"]:
        ml.write(loops, info, out, work_dir(a.id) / "info.json")
    else:
        (work_dir(a.id) / "info.json").write_text(json.dumps(info, indent=1) + "\n")
    rec["loop"] = {} if info["rejected"] else {k: info[k] for k in LOOP_KEYS}
    rec["exports"] = {}  # a new cut invalidates old exports
    save(rec)
    print(json.dumps(info))
    if info["rejected"]:
        die(f"{a.id}: loop rejected: " + "; ".join(info["rejected"]))
    print(f"loop {a.id}: {info['bars']} bars at {info['bpm']} bpm, {info['loop_s']} s -> {out}")
    return 0


LAYERS = ("bass", "drums", "other")
TERM = re.compile(r"(bass|drums|other|full|@\d+)(-\d+(?:\.\d+)?)?$")
AAC = ["-c:a", "aac", "-b:a", "96k", "-ar", "44100", "-ac", "2"]  # the loops of plan 33 (musica-*.m4a)


def parse_recipe(text: str, prev: dict | None, whole: bool) -> dict:
    """'bass+other-3' -> {'bass': 0, 'other': -3}; '+drums' extends prev; 'full'; whole: 'full' or '@24' only."""
    if text.startswith("+") and prev is None:
        raise ValueError(f"recipe {text!r} starts with + but there is no previous variant")
    out = dict(prev) if text.startswith("+") else {}
    for term in text.lstrip("+").split("+"):
        m = TERM.match(term)
        if not m:
            raise ValueError(f"bad recipe term {term!r} in {text!r}")
        name, db = m[1], -float(m[2][1:]) if m[2] else 0.0
        if whole and name in LAYERS:
            raise ValueError(f"{term!r}: a whole record has no layers: use full or @<bar>")
        if name.startswith("@") and not whole:
            raise ValueError(f"{term!r}: sections need a --whole record")
        for k in (LAYERS if name == "full" and not whole else (name,)):
            out[k] = db
    if whole and len(out) != 1:
        raise ValueError(f"recipe {text!r}: a whole record takes one of full or @<bar>")
    return out


def recipe_text(r: dict) -> str:
    return "+".join(f"{k}{format(v, 'g') if v else ''}" for k, v in r.items())


def read_wav(p):
    import soundfile as sf
    return sf.read(p, dtype="float32")[0]


def section(i: str, lp: dict, g, bar: int):
    """Whole record: the loop length from bar `bar` of the track at the loop's gain, rejected like the loop."""
    import music_loop as ml
    x = ml.decode(original(i))
    s0 = g.start(bar)
    if s0 + g.L > len(x):
        die(f"@{bar}: the stretch ends after the track")
    tail = int(min(g.bar / 2, len(x) - s0 - g.L))
    seg = ml.cut(x, s0, g.L, tail) * 10 ** (lp["gain_db"] / 20)
    info = {"repeat_similarity": round(ml.similarity(ml.log_mel(x.mean(1)), g, s0), 3),
            "seam_jump_vs_mean_step": round(ml.seam_jump(seg), 2),
            "comb_score": lp["comb_score"], "bpm": lp["bpm"], "loop_s": lp["loop_s"]}
    if bad := ml.reasons(info, None):
        die(f"@{bar}: section rejected: " + "; ".join(bad))
    return seg


def encode(x, f: Path):
    import numpy as np
    import music_loop as ml
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "f32le", "-ac", "2", "-ar", str(ml.SR), "-i", "-",
                        *AAC, "-y", str(f)], input=np.ascontiguousarray(x, dtype="<f4").tobytes(), capture_output=True)
    if r.returncode:
        die(f"ffmpeg: {r.stderr.decode()}")


def cmd_export(a) -> int:
    check_id(a.id)
    rec = load(a.id)
    require_confirmed(rec)
    lp = rec.get("loop")
    if not lp:
        die(f"{a.id}: no loop in the record: run `trivia-music loop {a.id}` first", 2)
    recipes, prev = {}, None
    for v in a.variant:
        name, sep, text = v.partition("=")
        if not sep or not re.fullmatch(r"[a-z0-9]+", name) or name in recipes:
            die(f"--variant NAME=RECIPE, name lower case and unique: {v!r}", 2)
        try:
            recipes[name] = prev = parse_recipe(text, prev, lp["whole"])
        except ValueError as e:
            die(str(e), 2)
    import music_loop as ml
    loop_dir = work_dir(a.id) / "loop"
    if not loop_dir.is_dir():
        die(f"no loop files in {loop_dir}: run `trivia-music loop {a.id}`", 2)
    g = ml.Grid(lp["bpm"], lp["downbeat_s"], lp["bars"])
    parts = {}  # layer or @bar -> samples
    for r in recipes.values():
        for k in r:
            if k not in parts:
                parts[k] = section(a.id, lp, g, int(k[1:])) if k.startswith("@") else read_wav(loop_dir / f"{k}.wav")
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    set_name = a.set or a.id.rsplit("-", 1)[0]
    exports, lens = {}, set()
    for name, r in recipes.items():
        f = out / f"musica-{set_name}-{name}.m4a"
        encode(sum(parts[k] * 10 ** (db / 20) for k, db in r.items()), f)
        dec = ml.decode(f)
        lu, tp = ml.loudness(dec)
        lens.add(len(dec))
        exports[name] = {"file": f.name, "recipe": recipe_text(r), "samples": len(dec), "lufs": lu, "true_peak": tp}
        print(f"{f.name}: {len(dec) / ml.SR:.3f} s, {lu:.1f} LUFS, {tp:.1f} dBTP  ({recipe_text(r)})")
    if len(lens) != 1:
        die(f"variants differ in length: {sorted(lens)}")
    rec["exports"] = exports
    save(rec)
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
    p = sub.add_parser("setup", help="make the Demucs venv"); p.add_argument("--force", action="store_true")
    p = sub.add_parser("split", help="Demucs layer split"); p.add_argument("id")
    p = sub.add_parser("loop", help="find the loop, level it"); p.add_argument("id")
    p.add_argument("--bars", type=int, default=8); p.add_argument("--bpm", type=float, help="tempo hint (default: listed)")
    p.add_argument("--whole", action="store_true", help="no stems: one cut over the original mix")
    p = sub.add_parser("export", help="one .m4a per tension variant"); p.add_argument("id"); p.add_argument("out_dir")
    p.add_argument("--variant", action="append", required=True, metavar="NAME=RECIPE")
    p.add_argument("--set", help="file name set (default: the id without its last part)")
    a = ap.parse_args(argv)
    return {"search": cmd_search, "fetch": cmd_fetch, "record": cmd_record, "setup": cmd_setup, "split": cmd_split, "loop": cmd_loop, "export": cmd_export}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
