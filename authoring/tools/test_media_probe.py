"""media_probe on a generated tone and test video (plan 201); needs ffmpeg and tesseract (dev shell), no network."""
import shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media_probe as mp  # noqa: E402

TOOLS = all(shutil.which(t) for t in ("ffmpeg", "tesseract", "magick"))


@unittest.skipUnless(TOOLS, "ffmpeg, tesseract, magick not on PATH (dev shell)")
class Probe(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        self.tone, self.video = self.d / "tone.wav", self.d / "test.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=4", str(self.tone)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=duration=5:size=640x360:rate=10",
                        "-f", "lavfi", "-i", "sine=frequency=300:duration=5", "-shortest", "-pix_fmt", "yuv420p", str(self.video)], check=True)
        p = mock.patch.object(mp, "OUT", self.d / "out")
        p.start()
        self.addCleanup(p.stop)

    def test_tone(self):
        info = mp.probe(str(self.tone), with_speech=False)
        out = Path(info["dir"])
        self.assertTrue((out / "spectrogram.png").stat().st_size and (out / "waveform.png").stat().st_size)
        self.assertFalse(info["has_video"])
        self.assertAlmostEqual(info["silence_share"], 0, places=1)
        self.assertLess(info["integrated_lufs"], 0)
        self.assertTrue((out / "probe.json").exists())

    def test_video_excerpt(self):
        info = mp.probe(str(self.video), start=1, end=3, with_speech=False)
        out = Path(info["dir"])
        self.assertEqual(len(info["frames"]), mp.FRAMES)
        self.assertTrue(all(1 <= f["seconds"] <= 3 for f in info["frames"]))
        for name in ("sheet.png", "ocr.txt", "spectrogram.png", "waveform.png"):
            self.assertTrue((out / name).exists(), name)
        self.assertEqual(len(list((out / "frames").glob("*.png"))), mp.FRAMES)

    def test_speech_parse(self):
        out = self.d / "o"
        out.mkdir()
        (out / "speech.txt").write_text(" hello\n world \n")
        r = mock.Mock(stderr="whisper_full: auto-detected language: en (p = 0.97)", stdout="")
        with mock.patch.object(mp, "run", return_value=r), mock.patch.object(mp, "model", return_value=Path("m")):
            self.assertEqual(mp.speech(self.tone, out, 0, 4), {"language": "en", "language_p": 0.97, "text": "hello world"})


if __name__ == "__main__":
    unittest.main()
