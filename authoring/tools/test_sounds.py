"""sounds: the /sounds manifest loader and file route (plan 220)."""
import json, shutil, sys, tempfile, threading, unittest, urllib.error, urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))
import qgen  # noqa: E402,F401  (main imports it first)
import main  # noqa: E402
import sounds  # noqa: E402


class Sounds(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        self.root = self.d / "work" / "sound-brief"
        p = mock.patch.object(sounds.layout, "SOUND_BRIEF", self.root)
        p.start()
        self.addCleanup(p.stop)
        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), main.Handler)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.addCleanup(self.srv.server_close)
        self.addCleanup(self.srv.shutdown)

    def get(self, path):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{self.srv.server_port}{path}") as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def test_no_manifest(self):
        self.assertIsNone(sounds.load())
        self.assertEqual(self.get("/api/sounds"), (200, b"null"))

    def test_manifest_and_files(self):
        (self.root / "effects" / "x").mkdir(parents=True)
        (self.root / "effects" / "x" / "a.m4a").write_bytes(b"abc")
        (self.d / "secret.txt").write_text("no")
        entries = [{"file": "effects/x/a.m4a", "group": "effects", "direction": "x", "round": 1}]
        (self.root / "manifest.json").write_text(json.dumps(entries))
        self.assertEqual(sounds.load(), entries)
        status, body = self.get("/api/sounds")
        self.assertEqual((status, json.loads(body)), (200, entries))
        self.assertEqual(self.get("/sounds/effects/x/a.m4a"), (200, b"abc"))
        self.assertEqual(self.get("/sounds/effects/x/missing.m4a")[0], 404)
        self.assertEqual(self.get("/sounds/..%2F..%2Fsecret.txt")[0], 404)
        self.assertIsNone(sounds.file_path("../../secret.txt"))

    def test_bad_manifest(self):
        self.root.mkdir(parents=True)
        (self.root / "manifest.json").write_text("{}")
        self.assertEqual(self.get("/api/sounds")[0], 400)


if __name__ == "__main__":
    unittest.main()
