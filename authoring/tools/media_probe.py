"""`qgen media-probe <file or Commons title>…`: what an LLM gets in place of hearing or watching a file (plan 201).

Per file, in work/media-probe/<sha>/ (sha: sha1 of the argument, 16 hex):
- video: `sheet.png` (9–12 numbered frames over the file or the excerpt, `media.make_sheet`), `frames/NN.png`,
  `ocr.txt` (tesseract on each frame), frame times in `probe.json`;
- audio, and a video's sound: `spectrogram.png`, loudness (EBU R128) and silence share in
  `probe.json`, `speech.txt` and the guessed language (whisper.cpp, local, no account, no upload; windows over 180 s: first and last 60 s).
`probe.json` is the summary. `--start`/`--end` probe an excerpt. Tools (dev shell only, nothing ships):
ffmpeg, tesseract, whisper-cli (flake.nix devShell). The speech model, fetched once into work/models/:
https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin (multilingual, ≈ 148 MB).
Downloads of a Commons title go through the media cache (`download.cached`).
"""
import hashlib, json, re, subprocess, urllib.parse
from pathlib import Path

import download, layout, progress
from media import make_sheet  # authoring/tools/media.py
from providers import commons

OUT = layout.WORK / "media-probe"
MODELS = layout.WORK / "models"
MODEL = "ggml-base.bin"
MODEL_URL = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/" + MODEL
FRAMES = 10          # within the plan's 9–12
# greedy decoding, no temperature fallback, no context: ≈ 2.4× faster on long music, same speech found
WHISPER_FAST = ["-bs", "1", "-bo", "1", "-nf", "-mc", "0", "-t", "6"]
SPEECH_LONG = 180    # longer windows: whisper hears the first and last SPEECH_EDGE s (announcements, spoken names)
SPEECH_EDGE = 60
SILENCE = "silencedetect=noise=-40dB:d=0.5"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{cmd[0]}: {r.stderr.strip()[-300:] or f'exit {r.returncode}'}")
    return r


def resolve(arg):
    """A local path, or a Commons title / page URL → its cached file."""
    if Path(arg).is_file():
        return Path(arg)
    title = urllib.parse.unquote(arg.rsplit("/wiki/", 1)[-1]).replace("_", " ")
    if not title.startswith("File:"):
        title = "File:" + title
    recs = commons.file_records([title])
    if not recs:
        raise SystemExit(f"media-probe: no such file {arg}")
    return download.cached(recs[0]["file_url"])


def streams(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type:stream_disposition=attached_pic",
             "-of", "json", str(path)])
    j = json.loads(r.stdout)
    kinds = {s["codec_type"] for s in j["streams"] if not s.get("disposition", {}).get("attached_pic")}  # cover art isn't video
    return float(j["format"].get("duration") or 0), "video" in kinds, "audio" in kinds


def window(duration, start, end):
    s = start or 0.0
    return s, min(end, duration) if end else duration


def frames(path, out, s, e):
    """FRAMES frames spread over [s, e]; returns [(number, seconds)]. Numbers on the sheet match these."""
    (out / "frames").mkdir(parents=True, exist_ok=True)
    times = [round(s + (e - s) * (i + 0.5) / FRAMES, 2) for i in range(FRAMES)]
    for n, t in enumerate(times, 1):
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(path), "-frames:v", "1",
             "-vf", "scale=640:-2", str(out / "frames" / f"{n:02d}.png")])
    cands = [{"type": "video", "preview_url": (out / "frames" / f"{n:02d}.png").resolve().as_uri()}
             for n in range(1, FRAMES + 1)]
    make_sheet(cands, out / "sheet.png", out / "thumbs")
    return list(enumerate(times, 1))


def ocr(out, times):
    lines = []
    for n, t in times:
        r = subprocess.run(["tesseract", str(out / "frames" / f"{n:02d}.png"), "-", "--psm", "11"],
                           capture_output=True, text=True)
        text = " ".join(r.stdout.split())
        lines.append(f"frame {n} @ {t} s: {text}")
    (out / "ocr.txt").write_text("\n".join(lines) + "\n")
    return [l for l in lines if not l.endswith(": ")]


def window_args(s, e):
    return ["-ss", str(s), "-t", str(round(e - s, 3))]


def audio_pictures(path, out, s, e):
    w = window_args(s, e)
    run(["ffmpeg", "-v", "error", "-y", *w, "-i", str(path), "-filter_complex",
         "showspectrumpic=s=1024x512:legend=1", "-frames:v", "1", str(out / "spectrogram.png")])


def loudness_silence(path, s, e):
    """Loudness numbers and silence share from one decode of the window."""
    r = run(["ffmpeg", "-hide_banner", "-nostats", *window_args(s, e), "-i", str(path), "-vn",
             "-af", f"ebur128=peak=true,{SILENCE}", "-f", "null", "-"])
    tail = r.stderr.rsplit("Summary:", 1)[-1]
    num = lambda key: (m := re.search(key + r":\s+(-?[\d.]+|-inf)", tail)) and float(m.group(1).replace("-inf", "-120"))
    return {"integrated_lufs": num("I"), "range_lu": num("LRA"), "true_peak_dbfs": num("Peak")} | silence(r.stderr, s, e)


def silence(stderr, s, e):
    total = sum(float(x) for x in re.findall(r"silence_duration: ([\d.]+)", stderr))
    span = e - s
    return {"silence_seconds": round(total, 2), "silence_share": round(min(total / span, 1), 3) if span else 0}


def model():
    path = MODELS / MODEL
    if not path.exists():
        MODELS.mkdir(parents=True, exist_ok=True)
        with progress.waiting(f"whisper model {MODEL}"):
            part = path.with_suffix(".part")
            part.write_bytes(download.http_get(MODEL_URL))
            part.replace(path)
    return path


def speech(path, out, s, e):
    """Local whisper.cpp on 16 kHz mono: text and the language it detected."""
    wav = out / "speech.wav"
    span = e - s
    cut = ["-filter_complex", f"[0:a]atrim=0:{SPEECH_EDGE},asetpts=N/SR/TB[a];[0:a]atrim={span - SPEECH_EDGE},asetpts=N/SR/TB[b];"
           "[a][b]concat=n=2:v=0:a=1"] if span > SPEECH_LONG else []  # long: head and tail only
    run(["ffmpeg", "-v", "error", "-y", *window_args(s, e), "-i", str(path), "-vn", *cut, "-ac", "1", "-ar", "16000", str(wav)])
    r = run(["whisper-cli", "-m", str(model()), "-f", str(wav), "-l", "auto", "-nt", "-otxt", "-of", str(out / "speech"), *WHISPER_FAST])
    wav.unlink(missing_ok=True)
    m = re.search(r"auto-detected language: (\w+) \(p = ([\d.]+)\)", r.stderr + r.stdout)
    text = " ".join((out / "speech.txt").read_text().split())
    return {"language": m and m.group(1), "language_p": m and float(m.group(2)), "text": text,
            **({"heard": f"first and last {SPEECH_EDGE} s"} if cut else {})}


def out_dir(arg, start=None, end=None):
    return OUT / hashlib.sha1(f"{arg}|{start}|{end}".encode()).hexdigest()[:16]


def cached(arg, start=None, end=None):
    """An earlier probe's probe.json dict (with its dir), else None."""
    f = out_dir(arg, start, end) / "probe.json"
    return json.loads(f.read_text()) | {"dir": str(f.parent)} if f.exists() else None


def probe(arg, start=None, end=None, with_speech=True):
    """Write every artefact for one file; returns its probe.json dict."""
    path = resolve(arg)
    out = out_dir(arg, start, end)
    out.mkdir(parents=True, exist_ok=True)
    duration, has_video, has_audio = streams(path)
    s, e = window(duration, start, end)
    info = {"arg": arg, "file": str(path), "duration": round(duration, 2), "window": [s, round(e, 2)],
            "has_video": has_video, "has_audio": has_audio}
    if has_video:
        times = frames(path, out, s, e)
        info["frames"] = [{"n": n, "seconds": t} for n, t in times]
        info["ocr_frames_with_text"] = len(ocr(out, times))
    if has_audio:
        audio_pictures(path, out, s, e)
        info |= loudness_silence(path, s, e)
        if with_speech:
            info["speech"] = speech(path, out, s, e)
    (out / "probe.json").write_text(json.dumps(info, indent=1, ensure_ascii=False))
    return info | {"dir": str(out)}


def cmd_media_probe(args):
    for arg in args.files:
        info = probe(arg, args.start, args.end, not args.no_speech)
        progress.say(f"media-probe: {arg} → {info['dir']}")


def add_parser(sub):
    p = sub.add_parser("media-probe", help="judging aids for a file: frame sheet, OCR, spectrogram, loudness, speech → work/media-probe/ (plan 201)")
    p.set_defaults(fn=cmd_media_probe, run=None)
    p.add_argument("files", nargs="+", metavar="file-or-title", help="a path, a Commons title or a page URL")
    p.add_argument("--start", type=float, help="excerpt start, seconds")
    p.add_argument("--end", type=float, help="excerpt end, seconds")
    p.add_argument("--no-speech", action="store_true", help="skip whisper (no model download)")
