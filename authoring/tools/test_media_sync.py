"""trivia-media sync works per file: one download and check, broken mark on every question using it (task 2358)."""
import argparse, json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media  # noqa: E402

URL = "https://example.org/a.jpg"


def q(i, status):
    return {"id": i, "status": status, "media": {"file_url": URL}}


class Sync(unittest.TestCase):
    def test_one_check_marks_every_sharer(self):
        pool = Path(tempfile.mkdtemp()) / "questions.json"
        pool.write_text(json.dumps({"questions": [q("q-1", "approved"), q("q-2", "draft")]}), encoding="utf-8")
        checks = []

        def file_problem(path):
            checks.append(path)
            return "broken"
        with mock.patch.object(media, "POOL", pool), \
                mock.patch.object(media, "cache_path", lambda u: Path("/nonexistent/x")), \
                mock.patch.object(media, "cached", lambda u: Path("/nonexistent/x")), \
                mock.patch.object(media, "file_problem", file_problem), \
                mock.patch.object(media, "prune", lambda: (0, 0)):
            media.cmd_sync(argparse.Namespace(status="approved", prune=False))
        self.assertEqual(len(checks), 1)
        got = {x["id"]: x["media"].get("file_problem") for x in json.loads(pool.read_text(encoding="utf-8"))["questions"]}
        self.assertEqual(got, {"q-1": "broken", "q-2": "broken"})


if __name__ == "__main__":
    unittest.main()
