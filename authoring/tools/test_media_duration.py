"""The media step records duration and drops videos over 30 s (task 2432); no network."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media  # noqa: E402


def cand(kind, duration):
    return {"type": kind, "duration": duration, "width": None, "height": None, "page_url": "p", "id": "1", "provider": "commons",
            "title": "t", "author": "a", "license": "CC0", "mime": None}


class Duration(unittest.TestCase):
    def test_acceptable(self):
        self.assertFalse(media.acceptable(cand("video", 59.6), "essential"))
        self.assertTrue(media.acceptable(cand("video", 30), "essential"))
        self.assertTrue(media.acceptable(cand("video", None), "essential"))
        self.assertFalse(media.acceptable(cand("audio", 61), "essential"))

    def test_pick_records_duration(self):
        from unittest import mock
        with mock.patch.object(media.providers, "download_url", return_value="u"), \
                mock.patch.object(media.providers, "licence_fields", return_value={}):
            self.assertEqual(media.pick_fields(cand("video", 12.5))["duration"], 12.5)
            self.assertNotIn("duration", media.pick_fields(cand("video", None)))
            self.assertNotIn("duration", media.pick_fields(cand("image", 3)))

    def test_apply_pick_drops_old_duration(self):
        t = {"type": "video", "duration": 50}
        media.apply_pick(t, {"type": "video", "file_url": "u"})
        self.assertNotIn("duration", t)
