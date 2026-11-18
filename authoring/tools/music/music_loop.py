"""Loop finder (plan 221): a track or its Demucs stems -> one seamless N-bar loop per layer, one cut, one gain.

Ported from the sibling project's tools/audio/music_loop.py (from spikes/music-library/loopify.py,
~/code/three-days-until-release; decision 199: no import across repos). Needs numpy, librosa, soundfile, ffmpeg.

Tempo from the drums (beat grid fitted to 0.001 bpm); downbeat = the beat phase (mod 4) with the most bass and kick
energy; start = the downbeat where bars K and K+N sound most alike; the tail after the loop end rings into the head.
Whole mode: the mix is the only layer, tempo and downbeat from it.
"""
import json
import re
import subprocess

import librosa
import numpy as np
import soundfile as sf

SR = 48000
TARGET_LUFS = -18.0  # app/desktop/loudness.mjs TARGET_LUFS (Python can't import it)
TRUE_PEAK = -1.5  # app/desktop/loudness.mjs TRUE_PEAK
MIN_SIMILARITY, MAX_SEAM, MIN_COMB, MAX_BPM_OFF, MIN_S, MAX_S = 0.8, 3.0, 1.5, 0.03, 10.0, 300.0
SEARCH = 0.05  # bpm search ±5 % of the hint, so a fit > 3 % off can show
HOP = 128


def decode(path) -> np.ndarray:
    """Any audio file -> float32 (n, 2) at SR, via ffmpeg."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="<f4").reshape(-1, 2).copy()


def loudness(x: np.ndarray) -> tuple[float, float]:
    """(integrated LUFS, true peak dBTP) by ffmpeg ebur128."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-nostats", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-",
                        "-af", "ebur128=peak=true", "-f", "null", "-"],
                       input=np.ascontiguousarray(x, dtype="<f4").tobytes(), capture_output=True, check=True)
    s = r.stderr.decode()[r.stderr.decode().rindex("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", s).group(1)),
            float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", s).group(1)))


def fit_tempo(y: np.ndarray, hint: float) -> tuple[float, float, float]:
    """(bpm, first beat s, comb score): the straight beat grid with the most onset strength on it."""
    oenv = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP)
    ft = np.arange(len(oenv)) * HOP / SR

    def comb(bpm, t0):
        t = np.arange(t0, ft[-1] - 1, 60.0 / bpm)
        return float(np.interp(t, ft, oenv).sum() / len(t))

    best = (-1.0, hint, 0.0)
    for b in np.arange(hint * (1 - SEARCH), hint * (1 + SEARCH), 0.02):
        for t0 in np.arange(0, 60.0 / b, 0.01):
            sc = comb(b, t0)
            if sc > best[0]:
                best = (sc, b, t0)
    for step_b, step_t in ((0.004, 0.002), (0.001, 0.0005)):
        _, b0, i0 = best
        for b in np.arange(b0 - 0.03, b0 + 0.03, step_b):
            for t0 in np.arange(max(i0 - 0.01, 0), i0 + 0.01, step_t):
                sc = comb(b, t0)
                if sc > best[0]:
                    best = (sc, b, t0)
    sc, b, t0 = best
    return float(b), float(t0), sc


def downbeat(low: np.ndarray, bpm: float, t0: float) -> float:
    """Time of the first downbeat: the beat phase mod 4 with the most low-end onset energy."""
    env = librosa.onset.onset_strength(y=low, sr=SR, hop_length=512)
    P = 60.0 / bpm
    nb = int((len(low) / SR - t0) / P) - 1

    def e(i):
        f = int((t0 + P * i) * SR / 512)
        return env[max(f - 1, 0): f + 2].sum() if 0 <= f < len(env) else 0.0

    E = np.array([e(i) for i in range(nb)])
    return t0 + P * int(np.argmax([E[p::4].mean() for p in range(4)]))


class Grid:
    """Bars of a fitted tempo; bar k starts at db + k * bar seconds."""

    def __init__(self, bpm: float, db: float, bars: int):
        self.bpm, self.db, self.bars = bpm, db, bars
        self.bar = 4 * 60.0 / bpm * SR  # samples
        self.L = int(round(bars * self.bar))

    def start(self, k: int) -> int:
        return int(round(self.db * SR + k * self.bar))


def similarity(mel: np.ndarray, g: Grid, s: int) -> float:
    """Cosine of the log-mel frames of the two bars at s and at s + loop length."""
    n = 2 * int(g.bar / 512)
    v1, v2 = mel[:, s // 512: s // 512 + n].ravel(), mel[:, (s + g.L) // 512: (s + g.L) // 512 + n].ravel()
    if len(v1) != len(v2) or not len(v1):
        return -1.0
    return float(v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9))


def log_mel(mix: np.ndarray) -> np.ndarray:
    return np.log1p(librosa.feature.melspectrogram(y=mix, sr=SR, n_fft=2048, hop_length=512, n_mels=64))


def cut(x: np.ndarray, s0: int, L: int, tail: int) -> np.ndarray:
    """L samples from s0; the tail after the end is cross-faded into the head, so the seam rings on."""
    seg = x[s0:s0 + L].copy()
    if tail > 0:
        w = np.linspace(0, 1, tail)[:, None]
        seg[:tail] = x[s0 + L:s0 + L + tail] * (1 - w) + seg[:tail] * w
    return seg


def seam_jump(x: np.ndarray) -> float:
    """Step from the last to the first sample (mono) against the mean step within 10 ms either side of the seam.

    Local, not whole-loop: a downbeat kick makes natural steps several times the loop's mean.
    """
    m = x.mean(1)
    w = min(SR // 100, len(m) // 2)
    ring = np.concatenate([m[-w:], m[:w]])
    steps = np.abs(np.diff(ring))
    local = np.delete(steps, w - 1).mean()
    return float(steps[w - 1] / (local + 1e-12))


def find(layers: dict, hint: float, bars: int = 8, listed: float | None = None) -> tuple[dict, dict]:
    """layers: name -> (n, 2), the same length; 'drums' and 'bass' if split, else one 'mix'.

    Returns (loops at the gain, info with 'rejected': [reasons], empty when it passes).
    """
    n = min(len(v) for v in layers.values())
    layers = {k: v[:n] for k, v in layers.items()}
    split = "drums" in layers
    mix = sum(layers.values()).mean(1)
    bpm, t0, comb = fit_tempo(layers["drums"].mean(1) if split else mix, hint)
    db = downbeat((layers["bass"] + layers["drums"]).mean(1) if split else mix, bpm, t0)
    g = Grid(bpm, db, bars)
    mel = log_mel(mix)
    rms = {k: float(np.sqrt((v ** 2).mean())) for k, v in layers.items()}
    best = None
    k = 0
    while (s := g.start(k)) <= n - g.L - 2 * g.bar:
        # skip the intro; in a split track every layer must be audible (not a breakdown)
        if s > 0.1 * n and (not split or all(np.sqrt((layers[c][s:s + g.L] ** 2).mean()) > 0.6 * rms[c]
                                             for c in ("bass", "drums", "other"))):
            sim = similarity(mel, g, s)
            if best is None or sim > best[0]:
                best = (sim, s, k)
        k += 1
    info = {"bpm": round(bpm, 3), "bars": bars, "whole": not split, "comb_score": round(comb, 3),
            "downbeat_s": round(db, 4), "loop_s": round(g.L / SR, 3), "rejected": []}
    if best is None:
        info["rejected"].append("no stretch of the track is long enough" + ("" if not split else " with all layers audible"))
        return {}, info
    sim, s0, k0 = best
    tail = int(min(g.bar / 2, n - s0 - g.L))
    loops = {name: cut(x, s0, g.L, tail) for name, x in layers.items()}
    total = sum(loops.values())
    lu, tp = loudness(total)
    gain_db = min(TARGET_LUFS - lu, TRUE_PEAK - tp)
    gain = 10 ** (gain_db / 20)
    loops = {name: x * gain for name, x in loops.items()}
    info.update(start_bar=k0, start_s=round(s0 / SR, 3), repeat_similarity=round(sim, 3),
                seam_jump_vs_mean_step=round(seam_jump(total * gain), 2), gain_db=round(gain_db, 2),
                lufs=round(lu + gain_db, 2), true_peak=round(tp + gain_db, 2), tail_s=round(tail / SR, 3),
                layer_rms={name: round(float(np.sqrt((x ** 2).mean())), 4) for name, x in loops.items()})
    info["rejected"] = reasons(info, listed)
    return loops, info


def reasons(info: dict, listed: float | None) -> list:
    r = []
    if info["repeat_similarity"] < MIN_SIMILARITY:
        r.append(f"repeat_similarity {info['repeat_similarity']} < {MIN_SIMILARITY}")
    if info["seam_jump_vs_mean_step"] > MAX_SEAM:
        r.append(f"seam jump {info['seam_jump_vs_mean_step']} > {MAX_SEAM}")
    if info["comb_score"] < MIN_COMB:
        r.append(f"comb_score {info['comb_score']} < {MIN_COMB} (no firm beat)")
    if listed and abs(info["bpm"] - listed) / listed > MAX_BPM_OFF:
        r.append(f"fitted bpm {info['bpm']} more than {MAX_BPM_OFF:.0%} off the listed {listed}")
    if not MIN_S <= info["loop_s"] <= MAX_S:
        r.append(f"loop {info['loop_s']} s outside {MIN_S:.0f}-{MAX_S:.0f} s")
    return r


def load_stems(d) -> dict:
    """Demucs stems -> bass, drums, other (vocals folded into other: Demucs puts melody lines there)."""
    st = {s: decode(d / f"{s}.wav") for s in ("bass", "drums", "other", "vocals")}
    n = min(len(v) for v in st.values())
    st = {k: v[:n] for k, v in st.items()}
    st["other"] = st["other"] + st.pop("vocals")
    return st


def write(loops: dict, info: dict, out_dir, info_path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, x in loops.items():
        sf.write(out_dir / f"{name}.wav", x, SR, subtype="FLOAT")
    if len(loops) > 1:
        sf.write(out_dir / "full.wav", sum(loops.values()), SR, subtype="FLOAT")
    info_path.write_text(json.dumps(info, indent=1) + "\n")
