"""media_survey filters, tally and pool dedupe (plan 201); no network."""
import json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media_survey as ms  # noqa: E402


def rec(title="File:A.ogg", **kw):
    return {"title": title, "mediatype": "audio", "license": "CC BY-SA 4.0", "restrictions": [], "duration": 10,
            "width": None, "height": None, **kw}


SEED = {"id": "s", "kind": "animal", "class": "general", "cats": ["animals"], "type": "audio"}


class Filters(unittest.TestCase):
    def why(self, **kw):
        return ms.reject(rec(**kw), set())

    def test_kept(self):
        self.assertIsNone(self.why())

    def test_licence_and_restriction(self):
        self.assertEqual(self.why(license="CC BY-NC 4.0"), "licence not on the allowlist")
        self.assertEqual(self.why(restrictions=["personality"]), "restriction")

    def test_lengths(self):
        self.assertIn("shorter", self.why(duration=1))
        self.assertIn("longer", self.why(duration=601))
        self.assertIsNone(self.why(duration=300))  # > 60 s is kept, needs an excerpt

    def test_video_height(self):
        v = dict(mediatype="video", duration=30)
        self.assertIn("below", self.why(**v, height=360))
        self.assertIsNone(self.why(**v, height=720))

    def test_not_media(self):
        self.assertEqual(self.why(mediatype="bitmap"), "not audio or video")

    def test_pool_and_duplicates(self):
        kept, counts = ms.apply_filters([(SEED, [rec("File:A b.ogg"), rec("File:A_b.ogg"), rec("File:C.ogg", duration=90)]),
                                         (SEED, [rec("File:C.ogg")])], {ms.norm_title("File:Z.ogg")})
        self.assertEqual([k["title"] for k in kept], ["File:A b.ogg", "File:C.ogg"])
        self.assertEqual(counts["duplicate across seeds"], 2)
        self.assertEqual([k["needs_excerpt"] for k in kept], [False, True])
        kept, counts = ms.apply_filters([(SEED, [rec("File:Z.ogg")])], {ms.norm_title("File:Z.ogg")})
        self.assertEqual((kept, counts["already in a pool"]), ([], 1))

    def test_tally(self):
        kept, _ = ms.apply_filters([({**SEED, "cats": ["animals", "amazon"]}, [rec("File:A.ogg"), rec("File:B.ogg", duration=90)])], set())
        rows = ms.tally(kept)
        self.assertEqual([(r["category"], r["files"], r["short"], r["excerpt"]) for r in rows],
                         [("amazon", 2, 1, 1), ("animals", 2, 1, 1)])


class PoolDedupe(unittest.TestCase):
    def test_titles_from_urls(self):
        q = {"questions": [{"media": {"source_url": "https://commons.wikimedia.org/wiki/File%3AA_b.ogg", "file_url": None},
                            "background": {"file_url": "https://upload.wikimedia.org/wikipedia/commons/f/fd/C_d.ogg?utm=1"}},
                           {"media": None, "background": None}]}
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / "data").mkdir()
            (base / "data" / "questions.json").write_text(json.dumps(q))
            with mock.patch.object(ms.layout, "AUTHORING", base):
                self.assertEqual(ms.pool_media(), {"a b.ogg", "c d.ogg"})


if __name__ == "__main__":
    unittest.main()
