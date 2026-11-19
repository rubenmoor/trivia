"""Batch report health names the run's own bundle's deficit (task 2356)."""
import sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import health  # noqa: E402  (import order)


class HealthBundle(unittest.TestCase):
    def test_deficit_of_run_bundle(self):
        work = Path(tempfile.mkdtemp())
        (work / "batch-1").mkdir()
        (work / "batch-1" / "run.json").write_text('{"bundle": "colombia"}', encoding="utf-8")
        (work / "batch-2").mkdir()
        with mock.patch.object(health, "WORK", work), \
             mock.patch.object(health.targets, "deficits", lambda pool, b: {"es": 1} if b else {}):
            self.assertEqual(health.run_bundle("batch-1"), "colombia")
            self.assertEqual(health.run_bundle("batch-2"), "base")
            lines = health.deficit_lines(["batch-1", "batch-2"], [])
            self.assertIn("(base,", lines[0])
            self.assertIn("(colombia,", lines[1])


if __name__ == "__main__":
    unittest.main()
