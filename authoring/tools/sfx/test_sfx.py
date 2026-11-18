"""trivia-sfx: convert chain, hard checks, licence gate, credits rows (plan 223). Needs ffmpeg; no network."""
import contextlib, io, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import sfx  # noqa: E402


def ff(*args):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args], check=True)


class Sfx(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        (self.d / "audio").mkdir()
        (self.d / "audio" / "CREDITS.md").write_text("# Credits\n\n| File | Used for | Source | Author | Licence |\n|---|---|---|---|---|\n| `hand.m4a` | x | y | z | w |\n")
        for name, sub in (("SFX_WORK", "work"), ("SFX_RECORDS", "rec"), ("AUDIO", "audio"), ("AUDIO_CREDITS", "audio/CREDITS.md")):
            p = mock.patch.object(sfx.layout, name, self.d / sub)
            p.start()
            self.addCleanup(p.stop)
        # 0.5 s silence, 0.6 s quiet 440 Hz stereo tone, 0.5 s silence
        self.src = self.d / "tone.wav"
        ff("-f", "lavfi", "-i", "sine=f=440:d=0.6:r=44100", "-af",
           "volume=-10dB,adelay=500|500,apad=pad_dur=0.5,aformat=channel_layouts=stereo", str(self.src))

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = sfx.main(list(args))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), err.getvalue()

    def rec(self, name="tono", licence="CC-BY-4.0", *extra):
        return self.run_cli("record", name, "--file", str(self.src), "--page", "https://x/p", "--title", "Tone",
                            "--author", "Me", "--licence", licence, "--cue", "pop", "--read-on-page", *extra)

    def test_convert_trims_fades_levels_mono(self):
        self.assertEqual(self.rec()[0], 0)
        code, out, err = self.run_cli("convert", "tono")
        self.assertEqual(code, 0, err)
        f = sfx.out_path("tono")
        self.assertTrue(f.is_file())
        self.assertAlmostEqual(sfx.duration(f), 0.6, delta=0.15)  # both silences gone
        lufs, tp = sfx.measure(f)
        self.assertAlmostEqual(lufs, -16, delta=1)
        self.assertLessEqual(tp, -1.5)
        ch = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=channels", "-of", "csv=p=0", str(f)], capture_output=True, text=True)
        self.assertEqual(ch.stdout.strip(), "1")
        # fade-out: the last 10 ms are far quieter than the middle
        def mean(start):
            e = subprocess.run(["ffmpeg", "-nostdin", "-i", str(f), "-af", f"atrim=start={start}:duration=0.01,volumedetect", "-f", "null", "-"],
                               capture_output=True, text=True).stderr
            return float(e.split("mean_volume:")[1].split()[0])
        self.assertLess(mean(sfx.duration(f) - 0.02), mean(0.2) - 6)

    def test_stereo_record_keeps_two_channels(self):
        self.rec("estereo", "CC0-1.0", "--stereo")
        self.assertEqual(self.run_cli("convert", "estereo")[0], 0)
        ch = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=channels", "-of", "csv=p=0", str(sfx.out_path("estereo"))], capture_output=True, text=True)
        self.assertEqual(ch.stdout.strip(), "2")

    def test_too_large_file_fails(self):
        self.rec("grande")
        self.run_cli("convert", "grande")
        with mock.patch.dict(sfx.CLASSES, {"effect": 100}):
            code, _, err = self.run_cli("check", "grande")
        self.assertEqual(code, 1)
        self.assertIn("bytes >", err)

    def test_wrong_loudness_fails(self):
        self.rec("flojo")
        self.run_cli("convert", "flojo")
        shutil.copyfile(self.src, sfx.out_path("flojo"))  # an unprocessed file at the wrong level
        code, _, err = self.run_cli("check", "flojo")
        self.assertEqual(code, 1)
        self.assertIn("LUFS", err)

    def test_nc_licence_refused(self):
        code, _, err = self.rec("malo", "CC-BY-NC-4.0")
        self.assertNotEqual(code, 0)
        self.assertIn("not allowed", err)
        self.assertFalse(sfx.record_path("malo").exists())

    def test_nc_record_fails_check(self):
        self.rec("tono")
        self.run_cli("convert", "tono")
        r = json.loads(sfx.record_path("tono").read_text())
        r["licence"]["spdx"] = "CC-BY-NC-4.0"
        sfx.record_path("tono").write_text(json.dumps(r))
        code, _, err = self.run_cli("check", "tono")
        self.assertEqual(code, 1)
        self.assertIn("not allowed", err)

    def test_unconfirmed_licence_blocks_convert(self):
        self.run_cli("record", "tono", "--file", str(self.src), "--page", "https://x/p", "--title", "T", "--author", "A",
                     "--licence", "CC0-1.0", "--cue", "pop")
        self.assertNotEqual(self.run_cli("convert", "tono")[0], 0)

    def test_credits_row_generated_and_hand_rows_kept(self):
        self.rec()
        self.assertEqual(self.run_cli("credits")[0], 0)
        text = sfx.layout.AUDIO_CREDITS.read_text()
        self.assertIn("| `hand.m4a`", text)
        self.assertIn("| `tono.m4a` | Sound effect `pop`", text)
        self.assertIn("Attribution 4.0", text)
        self.assertEqual(self.run_cli("credits", "--check")[0], 0)
        sfx.record_path("tono").unlink()
        self.assertEqual(self.run_cli("credits", "--check")[0], 1)


if __name__ == "__main__":
    unittest.main()
