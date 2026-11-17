"""work_gc: a finished batch's sheets go, a probe shared with an unfinished batch keeps its images (task 2182)."""
import json, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (audit and qgen import each other)
import work_gc as g  # noqa: E402

A, B, C = "a" * 16, "b" * 16, "c" * 16  # A shared, B finished only, C nobody


class Gc(unittest.TestCase):
    def test_gc(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        work, probes = d / "work", d / "work" / "media-probe"
        for sha in (A, B, C):
            (probes / sha / "frames").mkdir(parents=True)
            for n in ("probe.json", "sheet.png", "frames/01.png"):
                (probes / sha / n).write_bytes(b"xx")
        for b, done in (("batch-1", True), ("batch-2", False)):
            (work / b / "sheets").mkdir(parents=True)
            (work / b / "sheets" / "q.jpg").write_bytes(b"xx")
            (work / b / "run.json").write_text(json.dumps({"mode": "media-first", "done": done}))
        (work / "batch-1" / "t.jsonl").write_text(f'{{"p": "media-probe/{A}"}}\n{{"p": "media-probe/{B}"}}\n')
        (work / "batch-2" / "t.jsonl").write_text(f'{{"p": "media-probe/{A}"}}\n')
        spot = d / "spot.json"
        spot.write_text(json.dumps({"batch-1": {"items": {"q-1": {}}}}))
        with mock.patch.object(g, "WORK", work), mock.patch.object(g, "PROBES", probes), \
                mock.patch.object(g, "SPOT_CHECKS", spot), mock.patch.object(g, "SOURCE_POOL", d / "none.json"), \
                mock.patch.object(g.audit, "spot_check_size", return_value=1):
            self.assertEqual(g.gc(dry_run=True), (3, 6))
            self.assertEqual(g.gc(), (3, 6))
            self.assertEqual(g.gc(), (0, 0))  # repeat
            self.assertEqual(g.gc(unchecked=True), (0, 0))
        self.assertFalse((work / "batch-1" / "sheets").exists())
        self.assertTrue((work / "batch-2" / "sheets" / "q.jpg").exists())
        self.assertTrue((probes / A / "sheet.png").exists() and (probes / A / "frames" / "01.png").exists())
        self.assertTrue((probes / C / "sheet.png").exists())  # mentioned by nobody
        self.assertFalse((probes / B / "sheet.png").exists() or (probes / B / "frames").exists())
        self.assertTrue((probes / B / "probe.json").exists())


if __name__ == "__main__":
    unittest.main()
