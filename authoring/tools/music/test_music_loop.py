"""trivia-music loop: the loop finder on synthetic stems made here (plan 221). Needs numpy, librosa, soundfile, ffmpeg."""
import contextlib, io, json, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).parent))
import music  # noqa: E402
import music_loop as ml  # noqa: E402

SR = ml.SR


def stems(seconds=40.0, bpm0=100.0, bpm1=100.0) -> dict:
    """Kick on every beat, a two-bar bass line, a one-bar tone tune; tempo glides bpm0 -> bpm1."""
    t = np.arange(int(seconds * SR)) / SR
    bpm = bpm0 + (bpm1 - bpm0) * t / seconds
    beat = np.cumsum(bpm / 60.0 / SR)  # beats elapsed
    ph = beat % 1.0
    kick = 0.4 * np.sin(2 * np.pi * 55 * ph * 60 / bpm) * np.exp(-ph * 12)
    bass_notes = np.array([41.2, 41.2, 49.0, 55.0, 36.7, 36.7, 49.0, 41.2])  # per beat, 2 bars
    bass = 0.5 * np.sin(2 * np.pi * np.cumsum(bass_notes[beat.astype(int) % 8]) / SR) * np.exp(-ph)
    tune = np.array([440.0, 523.3, 659.3, 523.3])
    other = 0.3 * np.sin(2 * np.pi * np.cumsum(tune[beat.astype(int) % 4]) / SR) * np.exp(-ph * 0.5)
    st = {"drums": kick, "bass": bass, "other": other, "vocals": np.zeros_like(t)}
    return {k: np.stack([v, v], 1).astype("float32") for k, v in st.items()}


class Loop(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        for name, sub in (("MUSIC_WORK", "work"), ("MUSIC_RECORDS", "rec")):
            p = mock.patch.object(music.layout, name, self.d / sub)
            p.start()
            self.addCleanup(p.stop)

    def make(self, i, st, whole=False):
        orig = self.d / "orig.wav"
        sf.write(orig, sum(st.values()) * 0.5, SR)
        self.cli("record", i, "--file", str(orig), "--page", "https://x/p", "--title", "Fix", "--author", "Test",
                 "--licence", "CC0-1.0", "--bpm", "100", "--read-on-page")
        if not whole:
            d = music.stems_dir(i)
            d.mkdir(parents=True)
            for k, v in st.items():
                sf.write(d / f"{k}.wav", v * 0.5, SR, subtype="FLOAT")

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = music.main(list(args))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), err.getvalue()

    def test_steady_fixture(self):
        self.make("fix-steady", stems())
        code, out, err = self.cli("loop", "fix-steady")
        self.assertEqual(code, 0, out + err)
        info = json.loads((music.work_dir("fix-steady") / "info.json").read_text())
        self.assertAlmostEqual(info["bpm"], 100.0, delta=0.01)
        self.assertGreaterEqual(info["repeat_similarity"], 0.8)
        self.assertEqual(info["bars"], 8)
        loop = music.work_dir("fix-steady") / "loop"
        self.assertEqual(sorted(p.name for p in loop.iterdir()), ["bass.wav", "drums.wav", "full.wav", "other.wav"])
        full, _ = sf.read(loop / "full.wav", dtype="float32")
        self.assertAlmostEqual(len(full) / SR, 19.2, delta=0.001)
        lu, tp = ml.loudness(full)
        self.assertAlmostEqual(lu, -18.0, delta=0.2)
        self.assertLessEqual(tp, -1.5 + 0.05)
        lens = {len(sf.read(p)[0]) for p in loop.iterdir()}
        self.assertEqual(len(lens), 1)
        rec = music.load("fix-steady")["loop"]
        for k in ("bpm", "bars", "start_s", "loop_s", "gain_db", "comb_score", "repeat_similarity", "seam_jump_vs_mean_step"):
            self.assertIn(k, rec)

    def test_drifting_tempo_rejected(self):
        self.make("fix-drift", stems(bpm0=88.0, bpm1=112.0))
        code, out, err = self.cli("loop", "fix-drift")
        self.assertEqual(code, 1, out + err)
        self.assertIn("rejected", err)
        self.assertEqual(music.load("fix-drift")["loop"], {})
        self.assertFalse((music.work_dir("fix-drift") / "loop").exists())

    def test_whole(self):
        self.make("fix-whole", stems(), whole=True)
        code, out, err = self.cli("loop", "fix-whole", "--whole")
        self.assertEqual(code, 0, out + err)
        rec = music.load("fix-whole")["loop"]
        self.assertTrue(rec["whole"])
        self.assertAlmostEqual(rec["bpm"], 100.0, delta=0.01)
        loop = music.work_dir("fix-whole") / "loop"
        self.assertEqual([p.name for p in loop.iterdir()], ["full.wav"])
        self.assertAlmostEqual(ml.loudness(sf.read(loop / "full.wav", dtype="float32")[0])[0], -18.0, delta=0.2)

    def test_refusals(self):
        self.make("fix-nostems", stems(seconds=12), whole=True)
        self.assertEqual(self.cli("loop", "fix-nostems")[0], 2)  # no stems, no --whole

    def test_reasons(self):
        ok = {"repeat_similarity": 0.9, "seam_jump_vs_mean_step": 1.0, "comb_score": 2.0, "bpm": 100.0, "loop_s": 20.0}
        self.assertEqual(ml.reasons(ok, 100.0), [])
        for k, v in (("repeat_similarity", 0.7), ("seam_jump_vs_mean_step", 3.5), ("comb_score", 1.0),
                     ("bpm", 104.0), ("loop_s", 9.0), ("loop_s", 301.0)):
            self.assertEqual(len(ml.reasons({**ok, k: v}, 100.0)), 1, k)


if __name__ == "__main__":
    unittest.main()
