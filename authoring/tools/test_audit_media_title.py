"""audit_input's media title for copies and translations (task 2430): from the source's candidates, else the file name."""
import sys, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401
import audit  # noqa: E402

URL = "https://commons.example/File:Lion.jpg"


class MediaTitle(unittest.TestCase):
    def title(self, q, pool, cands):
        with mock.patch.object(audit.media_tool, "load_candidates", lambda qid, slot="media": cands.get(qid)):
            return audit.media_title(q, q["media"], "media", pool)

    def test_copy_uses_source_candidates(self):
        src = {"id": "a", "media": {}}
        cp = {"id": "b", "copied_from": "a", "media": {"source_url": URL, "file_url": "x/y.jpg"}}
        c = {"a": {"candidates": [{"page_url": URL, "title": "File:Lion.jpg"}]}}
        self.assertEqual(self.title(cp, [src, cp], c), "File:Lion.jpg")

    def test_falls_back_to_file_name(self):
        cp = {"id": "b", "copied_from": "a", "media": {"source_url": URL, "file_url": "x/y%20z.jpg?v=1"}}
        self.assertEqual(self.title(cp, [cp], {}), "File:Lion.jpg")
        cp["media"] = {"file_url": "x/y%20z.jpg?v=1"}
        self.assertEqual(self.title(cp, [cp], {}), "y z.jpg")

    def test_unpicked_is_none(self):
        self.assertIsNone(self.title({"id": "b", "media": {}}, [], {}))


if __name__ == "__main__":
    unittest.main()
