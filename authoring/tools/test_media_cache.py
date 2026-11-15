"""media_cache.playable_path: a WebM copy beside Theora and co (task 2053); needs ffmpeg, no network."""
import shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import media_cache as mc  # noqa: E402


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not on PATH (dev shell)")
class Playable(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        p = mock.patch.object(mc, "MEDIA", self.d)
        p.start()
        self.addCleanup(p.stop)

    def test_copy_beside_original(self):
        url = "https://x.org/a/clip.ogv"
        src = mc.cache_path(url)
        # Matroska stands in for Theora: only the extension decides
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=64x48:rate=10:duration=1",
                        "-c:v", "libvpx", "-f", "matroska", str(src)], check=True)
        out = mc.playable_path(url)
        self.assertEqual(out, self.d / "playable" / (src.stem + ".webm"))
        self.assertEqual(out.read_bytes()[:4], b"\x1a\x45\xdf\xa3")
        self.assertTrue(src.is_file())
        self.assertEqual(mc.playable_path(url), out)

    def test_playable_as_is(self):
        url = "https://x.org/a/clip.webm"
        mc.cache_path(url).write_bytes(b"x")
        self.assertEqual(mc.playable_path(url), mc.cache_path(url))
        self.assertEqual(mc.playable_path("https://x.org/none.ogv"), mc.cache_path("https://x.org/none.ogv"))


if __name__ == "__main__":
    unittest.main()
