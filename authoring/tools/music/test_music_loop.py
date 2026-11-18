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

    def test_recipes(self):
        pr = music.parse_recipe
        self.assertEqual(pr("bass+other-3", None, False), {"bass": 0.0, "other": -3.0})
        base = pr("bass+other", None, False)
        self.assertEqual(pr("+drums", base, False), {"bass": 0.0, "other": 0.0, "drums": 0.0})
        self.assertEqual(set(pr("full", None, False)), {"bass", "drums", "other"})
        self.assertEqual(pr("@24-2.5", None, True), {"@24": -2.5})
        for text, prev, whole in (("+drums", None, False), ("kick", None, False), ("@3", None, False),
                                  ("bass", None, True), ("full+@3", None, True)):
            with self.assertRaises(ValueError, msg=text):
                pr(text, prev, whole)

    def test_export_variants(self):
        self.make("fix-exp", stems())
        self.assertEqual(self.cli("loop", "fix-exp")[0], 0)
        out = self.d / "out"
        code, o, err = self.cli("export", "fix-exp", str(out), "--variant", "normal=bass+other", "--variant", "question=+drums",
                                "--variant", "submitted=full")
        self.assertEqual(code, 0, o + err)
        names = ["normal", "question", "submitted"]
        self.assertEqual(sorted(p.name for p in out.iterdir()), [f"musica-fix-{n}.m4a" for n in sorted(names)])
        dec = [ml.decode(out / f"musica-fix-{n}.m4a") for n in names]
        self.assertEqual(len({len(x) for x in dec}), 1)
        self.assertAlmostEqual(len(dec[0]) / SR, 19.2, delta=0.01)
        lufs = [ml.loudness(x)[0] for x in dec]
        self.assertLess(lufs[0], lufs[1])
        self.assertLess(lufs[1], lufs[2] + 0.3)
        self.assertAlmostEqual(lufs[2], -18.0, delta=0.5)  # the loop's gain, full sum
        ex = music.load("fix-exp")["exports"]
        self.assertEqual(ex["question"]["recipe"], "bass+other+drums")
        self.assertEqual(ex["normal"]["file"], "musica-fix-normal.m4a")

    def test_export_whole_section(self):
        self.make("fix-ws", stems(), whole=True)
        self.assertEqual(self.cli("loop", "fix-ws", "--whole")[0], 0)
        out = self.d / "out"
        code, o, err = self.cli("export", "fix-ws", str(out), "--variant", "normal=full", "--variant", "question=@4-2")
        self.assertEqual(code, 0, o + err)
        a, b = (ml.decode(out / f"musica-fix-{n}.m4a") for n in ("normal", "question"))
        self.assertEqual(len(a), len(b))
        code, o, err = self.cli("export", "fix-ws", str(out), "--variant", "x=@900")
        self.assertEqual(code, 1)
        self.assertIn("ends after", err)

    def test_export_refusals(self):
        self.make("fix-ref", stems(seconds=12), whole=True)
        self.assertEqual(self.cli("export", "fix-ref", str(self.d / "o"), "--variant", "a=full")[0], 2)  # no loop yet

    def test_reasons(self):
        ok = {"repeat_similarity": 0.9, "seam_jump_vs_mean_step": 1.0, "comb_score": 2.0, "bpm": 100.0, "loop_s": 20.0}
        self.assertEqual(ml.reasons(ok, 100.0), [])
        for k, v in (("repeat_similarity", 0.7), ("seam_jump_vs_mean_step", 3.5), ("comb_score", 1.0),
                     ("bpm", 104.0), ("loop_s", 9.0), ("loop_s", 301.0)):
            self.assertEqual(len(ml.reasons({**ok, k: v}, 100.0)), 1, k)


class Checks(Loop):
    """check and credits on exported fixture files."""

    def exported(self, i="fix-chk"):
        st = stems()
        st["other"] = st["other"] + np.random.default_rng(1).normal(0, 0.03, st["other"].shape).astype("float32")  # real music has highs
        self.make(i, st)
        self.assertEqual(self.cli("loop", i)[0], 0)
        self.out = self.d / "out"
        code, o, err = self.cli("export", i, str(self.out), "--variant", "normal=bass+other", "--variant", "quiet=+drums-6",
                                "--variant", "submitted=full")
        self.assertEqual(code, 0, o + err)
        return i

    def replace(self, name, x):
        music.encode(x, self.out / f"musica-fix-{name}.m4a")

    def fails(self, i, text):
        code, o, err = self.cli("check", i)
        self.assertEqual(code, 1, o + err)
        self.assertIn(text, err)

    def test_check_passes(self):
        i = self.exported()
        code, o, err = self.cli("check", i)
        self.assertEqual(code, 0, o + err)

    def test_check_too_loud(self):
        i = self.exported()
        self.replace("normal", ml.decode(self.out / "musica-fix-normal.m4a") * 2.5)
        self.fails(i, "true peak")
        self.fails(i, "LUFS outside")

    def test_check_clicking_seam(self):
        i = self.exported()
        x = ml.decode(self.out / "musica-fix-normal.m4a")
        self.replace("normal", x + np.linspace(0, 0.3, len(x), dtype="float32")[:, None])
        self.fails(i, "normal: seam jump")

    def test_check_unequal_length(self):
        i = self.exported()
        self.replace("quiet", ml.decode(self.out / "musica-fix-quiet.m4a")[:-SR])
        self.fails(i, "differ in length")

    def test_check_nc_licence(self):
        i = self.exported()
        rec = music.load(i)
        rec["licence"]["spdx"] = "CC-BY-NC-4.0"
        music.save(rec)
        self.fails(i, "not allowed")

    def test_credits(self):
        self.exported()
        f = self.d / "CREDITS.md"
        hand = "# Audio credits\n\n| File | Used for | Source | Author | Licence |\n|---|---|---|---|---|\n| `a.m4a` | x | y | z | CC0 |\n"
        f.write_text(hand)
        with mock.patch.object(music.layout, "AUDIO_CREDITS", f):
            self.assertEqual(self.cli("credits", "--check")[0], 1)  # record without a row
            self.assertEqual(self.cli("credits")[0], 0)
            self.assertEqual(self.cli("credits", "--check")[0], 0)
            text = f.read_text()
            self.assertTrue(text.startswith(hand))
            rows = [ln for ln in text.splitlines() if ln.startswith("| `musica-")]
            self.assertEqual(len(rows), 3)
            for ln in rows:  # the 5-cell shape app/client/credits.ts parses
                self.assertEqual(len(ln.split("|")[1:-1]), 5)
            self.assertIn("[Fix](https://x/p) (other)", rows[0])
            self.assertIn("adapted", rows[0])
            self.assertEqual(self.cli("credits")[0], 0)  # idempotent
            self.assertEqual(f.read_text(), text)
            f.write_text(text.replace("musica-fix-normal", "musica-fix-gone"))
            code, o, err = self.cli("credits", "--check")
            self.assertEqual(code, 1)
            self.assertIn("row without a record", err)
            self.assertIn("record without a row", err)

    def test_credits_today_passes(self):
        # no records: today's CREDITS.md passes unchanged
        self.assertEqual(self.cli("credits", "--check")[0], 0)
        before = music.layout.AUDIO_CREDITS.read_text()
        self.assertEqual(self.cli("credits")[0], 0)
        self.assertEqual(music.layout.AUDIO_CREDITS.read_text(), before)


if __name__ == "__main__":
    unittest.main()
