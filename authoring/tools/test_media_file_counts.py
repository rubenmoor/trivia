"""Media counts are per file, not per question (task 2359)."""
import sys, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))
import qgen  # noqa: E402,F401  (import order)
import media_stats  # noqa: E402

URL = "https://example.org/a.jpg"


def q(i):
    return {"id": i, "status": "approved", "media": {"role": "essential", "type": "image", "file_url": URL}}


class FileCounts(unittest.TestCase):
    def test_shared_file_counts_once_in_bands_and_sizes(self):
        with mock.patch.object(media_stats, "band", lambda url: ("< 800", (640, 480))):
            out = media_stats.build([q("q-1"), q("q-2")])
        self.assertEqual(out["questions"], 2)
        self.assertEqual([b["files"] for b in out["bands"] if b["band"] == "< 800"], [1])
        self.assertEqual(out["sizes"], [{"size": "640×480", "files": 1}])


if __name__ == "__main__":
    unittest.main()
