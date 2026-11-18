"""Stage audition candidates for /sounds (plan 220, plans/25-sound.md "Manifest"): `python3 sound_brief.py <spec.json>`.
Spec: {"round": n, "group": "effects"|"music", "items": [{"name", "direction"|"mood", "stands_for", "src", "source",
"author", "licence", "start"?, "length"?, "bpm"?}]}; `src` is a path, the rest the manifest entry's fields. Each item becomes
work/sound-brief/<group>/<direction|mood>/<name>.m4a: leading silence cut, a 30 ms fade-out, one gain to the target
(effects -16 LUFS, music -18) held under -1.5 dBTP; its numbers go into manifest.json (same file: replaced).
Pack zips and originals stay in work/."""
import json, re, subprocess, sys, tempfile
from pathlib import Path

import atomic  # authoring/tools/atomic.py
from layout import SOUND_BRIEF

TARGET = {"effects": -16, "music": -18}
TRUE_PEAK = -1.5
PAD = 1  # seconds of silence after a short sound while measuring: the loudness gate works on 400 ms blocks


def ffmpeg(*args):
    return subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", *args], capture_output=True, text=True, check=True).stderr


def length_of(err):
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def loudness(path, pad=0):
    """(integrated LUFS, true peak dBTP) of a file, padded with `pad` s of silence."""
    af = (f"apad=pad_dur={pad}," if pad else "") + "ebur128=peak=true"
    summary = ffmpeg("-i", str(path), "-af", af, "-f", "null", "-").rsplit("Summary:", 1)[1]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary).group(1))


def centroid(path):
    """Mean spectral centroid in Hz over the frames that have energy."""
    out = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-af", "aspectralstats=measure=centroid,ametadata=print:key=lavfi.aspectralstats.1.centroid:file=-", "-f", "null", "-"],
                         capture_output=True, text=True, check=True).stdout
    values = [float(v) for v in re.findall(r"centroid=([\d.]+)", out) if float(v) > 0]
    return round(sum(values) / len(values)) if values else 0


def stage(item, group, rnd, tmp):
    folder = item.get("direction") or item["mood"]
    rel = f"{group}/{folder}/{item['name']}.m4a"
    out = SOUND_BRIEF / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    cut = (["-ss", str(item["start"])] if "start" in item else []) + (["-t", str(item["length"])] if "length" in item else [])
    wav = Path(tmp) / "in.wav"
    ffmpeg("-y", *cut, "-i", item["src"], "-af", "silenceremove=start_periods=1:start_threshold=-50dB", "-ar", "44100", "-ac", "1", str(wav))
    length = length_of(ffmpeg("-i", str(wav), "-f", "null", "-"))
    lufs, peak = loudness(wav, PAD)
    gain = min(TARGET[group] - lufs, TRUE_PEAK - 0.3 - peak)  # 0.3 dB for the encoder overshoot
    fade = min(0.03, length / 4)
    ffmpeg("-y", "-i", str(wav), "-af", f"volume={gain:.2f}dB,afade=t=out:st={length - fade:.3f}:d={fade:.3f}", "-c:a", "aac", "-b:a", "96k", str(out))
    lufs, peak = loudness(out, PAD)
    return {"file": rel, "group": group, "direction" if "direction" in item else "mood": folder, "round": rnd,
            "stands_for": item["stands_for"], "source": item["source"], "author": item["author"], "licence": item["licence"],
            "length_s": round(length, 2), "lufs": lufs, "true_peak_db": peak, "centroid_hz": centroid(out),
            **({"bpm": item["bpm"]} if "bpm" in item else {})}


def main(spec_file):
    spec = json.loads(Path(spec_file).read_text(encoding="utf-8"))
    manifest = SOUND_BRIEF / "manifest.json"
    with atomic.locked(manifest):
        entries = json.loads(manifest.read_text(encoding="utf-8")) if manifest.is_file() else []
        for item in spec["items"]:
            with tempfile.TemporaryDirectory() as tmp:
                entry = stage(item, spec["group"], spec["round"], tmp)
            entries = [e for e in entries if e["file"] != entry["file"]] + [entry]
            print(entry["file"], entry["length_s"], entry["lufs"], entry["true_peak_db"], entry["centroid_hz"])
        atomic.write_json(manifest, entries)


if __name__ == "__main__":
    main(sys.argv[1])
