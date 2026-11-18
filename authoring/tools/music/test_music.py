"""trivia-music: catalogue search, records, licence allowlist, confirmation gate (plan 221). No network."""
import contextlib, hashlib, io, json, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import music  # noqa: E402

CAT = [
    {"title": "Carefree", "filename": "Carefree.mp3", "isrc": "X1", "bpm": "96", "feel": "Calming", "instruments": "Piano, Bass", "length": "3:25"},
    {"title": "Fast One", "filename": "Fast One.mp3", "isrc": "X2", "bpm": "160", "feel": "Aggressive", "instruments": "Guitar", "length": "1:00"},
]


class Music(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)
        for name, sub in (("MUSIC_WORK", "work"), ("MUSIC_RECORDS", "rec")):
            p = mock.patch.object(music.layout, name, self.d / sub)
            p.start()
            self.addCleanup(p.stop)
        p = mock.patch.object(music, "catalogue", lambda: CAT)
        p.start()
        self.addCleanup(p.stop)
        self.f = self.d / "t.mp3"
        self.f.write_bytes(b"fake audio")

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = music.main(list(args))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), err.getvalue()

    def rec(self, *extra, licence="CC-BY-4.0"):
        return self.run_cli("record", "mine-song", "--file", str(self.f), "--page", "https://x/p", "--title", "Song",
                            "--author", "Me", "--licence", licence, *extra)

    def test_search_filters(self):
        titles = lambda *a: [l.split("\t")[0] for l in self.run_cli("search", *a)[1].splitlines()]
        self.assertEqual(titles(), ["Carefree", "Fast One"])
        self.assertEqual(titles("--feel", "calm"), ["Carefree"])
        self.assertEqual(titles("--bpm", "100-200"), ["Fast One"])
        self.assertEqual(titles("--instrument", "piano"), ["Carefree"])
        self.assertEqual(titles("--min-length", "120"), ["Carefree"])
        self.assertEqual(self.run_cli("search", "--bpm", "x")[0], 2)

    def test_record_sha_and_slots(self):
        self.assertEqual(self.rec("--read-on-page")[0], 0)
        r = json.loads(music.record_path("mine-song").read_text())
        self.assertEqual(r["sha256"], hashlib.sha256(b"fake audio").hexdigest())
        self.assertEqual((r["loop"], r["exports"]), ({}, {}))
        self.assertTrue(r["licence"]["read_on_page"])
        self.assertIn("Attribution 4.0", r["credit"])
        self.assertIn("Adapted", r["credit"])
        self.assertTrue((music.work_dir("mine-song") / "original.mp3").is_file())

    def test_disallowed_licences_fail(self):
        for lic in ("CC-BY-NC-4.0", "CC-BY-SA-4.0", "CC-BY-ND-4.0", "proprietary"):
            self.assertEqual(self.rec("--read-on-page", licence=lic)[0], 1, lic)
        self.assertFalse(music.record_path("mine-song").exists())

    def test_gate(self):
        self.rec()
        r = music.load("mine-song")
        with self.assertRaises(SystemExit):
            music.require_confirmed(r)
        self.assertEqual(self.run_cli("record", "mine-song", "--licence", "CC-BY-3.0", "--read-on-page")[0], 0)
        r = music.load("mine-song")
        music.require_confirmed(r)
        self.assertEqual(r["licence"]["spdx"], "CC-BY-3.0")
        self.assertIn("3.0", r["credit"])
        self.assertEqual(self.run_cli("record", "mine-song", "--licence", "CC-BY-NC-4.0", "--read-on-page")[0], 1)

    def test_run_stops_at_gate(self):
        self.rec()
        code, _, err = self.run_cli("run", "mine-song", str(self.d / "out"), "--variant", "full=full")
        self.assertEqual(code, 1)
        self.assertIn("not confirmed", err)

    def test_run_fetch_stops_at_gate(self):
        with mock.patch.object(music, "get", return_value=b"mp3 bytes"):
            code, out, err = self.run_cli("run", "Carefree", str(self.d / "out"), "--variant", "full=full")
        self.assertEqual(code, 1)
        self.assertTrue(music.record_path("carefree-try").exists())
        self.assertIn("not confirmed", err)

    def test_fetch(self):
        with mock.patch.object(music, "get", return_value=b"mp3 bytes"):
            code, out, _ = self.run_cli("fetch", "carefree", "carefree-try")
        self.assertEqual(code, 0)
        r = music.load("carefree-try")
        self.assertEqual((r["author"], r["listed"]["bpm"]), ("Kevin MacLeod", "96"))
        self.assertEqual(r["sha256"], hashlib.sha256(b"mp3 bytes").hexdigest())
        with self.assertRaises(SystemExit):
            music.require_confirmed(r)
        self.assertEqual(self.run_cli("fetch", "nope", "nope-x")[0], 1)

    def test_device_pick(self):
        with mock.patch.object(music, "GPU_LIB", self.d / "nolib"):
            self.assertEqual(music.device(), "cpu")
            self.assertIn("/cpu", music.setup_commands()[1][-1])
            self.assertNotIn("LD_LIBRARY_PATH", music.split_env())
        with mock.patch.object(music, "GPU_LIB", self.d):
            self.assertEqual(music.device(), "cuda")
            self.assertTrue(music.setup_commands()[1][-1].endswith("cu128"))

    def test_split_refusals(self):
        self.assertEqual(self.run_cli("split", "mine-song")[0], 2)  # no record
        self.rec()  # unconfirmed
        with mock.patch.object(music.subprocess, "run") as run:
            self.assertEqual(self.run_cli("split", "mine-song")[0], 1)
            self.run_cli("record", "mine-song", "--licence", "CC-BY-4.0", "--read-on-page")
            self.assertEqual(self.run_cli("split", "mine-song")[0], 3)  # no venv
            run.assert_not_called()

    def test_split_command(self):
        self.rec("--read-on-page")
        py = music.venv_dir() / "bin" / "python"
        py.parent.mkdir(parents=True)
        py.touch()
        c = music.split_command("mine-song")
        self.assertEqual(c[:5], [str(py), "-m", "demucs", "-n", "htdemucs"])
        self.assertEqual(c[-1], str(music.work_dir("mine-song") / "original.mp3"))
        self.assertEqual(c[c.index("-o") + 1], str(music.work_dir("mine-song") / "stems"))

    def test_bad_id(self):
        self.assertEqual(self.run_cli("fetch", "Carefree", "Bad_Id")[0], 2)


if __name__ == "__main__":
    unittest.main()
