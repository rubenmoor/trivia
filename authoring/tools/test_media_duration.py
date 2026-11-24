"""The media step records duration and drops videos over 30 s (task 2432); no network."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order: the command modules import each other)
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

    def test_play_problem(self):
        self.assertEqual(media.play_problem({"type": "video", "duration": 59.58}), "59.58 s, over 30 s")
        self.assertEqual(media.play_problem({"type": "video"}), "length unknown")
        self.assertIsNone(media.play_problem({"type": "video", "duration": 30}))
        self.assertIsNone(media.play_problem({"type": "video", "duration": 50, "excerpt": {"start": 0, "end": 20}}))
        self.assertIsNone(media.play_problem({"type": "audio"}))
        self.assertIsNotNone(media.play_problem({"type": "audio", "duration": 61}))
        self.assertIsNone(media.play_problem({"type": "image"}))

    def test_checked_probes(self):
        from unittest import mock
        with mock.patch.object(media, "cached", return_value=Path("x.webm")), \
                mock.patch("media_probe.streams", return_value=(59.583, True, True)):
            self.assertEqual(media.checked({"type": "video", "file_url": "u"})["duration"], 59.58)
            self.assertEqual(media.checked({"type": "video", "file_url": "u", "duration": 12})["duration"], 12)
            self.assertNotIn("duration", media.checked({"file_url": "u"}))
        with mock.patch.object(media, "cached", return_value=Path("x.webm")), \
                mock.patch("media_probe.streams", side_effect=RuntimeError("ffprobe")):
            self.assertNotIn("duration", media.checked({"type": "video", "file_url": "u"}))

    def test_unpicked_drops_duration(self):
        self.assertNotIn("duration", media.unpicked({"type": "video", "file_url": "u", "duration": 59}))


class Record(unittest.TestCase):
    """cmd_record on resume: a new long pick and an earlier approved one without duration (batch-94: q-26168)."""

    def setUp(self):
        import argparse, json, tempfile
        from unittest import mock
        import review_steps
        self.rs, self.json = review_steps, json
        self.work = Path(tempfile.mkdtemp())
        self.pool = self.work / "questions.json"
        self.d = self.work / "batch-1"
        (self.d / "reviews").mkdir(parents=True)
        (self.d / "run.json").write_text(json.dumps({"mode": "batch", "bundle": "base", "draft_locale": "en"}))
        for obj, name, value in [(review_steps, "WORK", self.work), (qgen, "WORK", self.work), (review_steps, "POOL", self.pool)]:
            p = mock.patch.object(obj, name, value)
            p.start()
            self.addCleanup(p.stop)
        self.lengths = {"u-long": 59.58, "u-ok": 20.0}
        for name, fn in [("checked", lambda f: {**f, "duration": self.lengths[f["file_url"]]} if f["file_url"] in self.lengths else f),
                         ("load_candidates", lambda qid, slot="media": {"candidates": [cand("video", None) | {"id": qid}]}),
                         ("pick_fields", lambda c, slot="media": {"type": "video", "source_url": "p", "file_url": "u-long",
                                                                  "credit": "c", "license": "CC0"})]:
            p = mock.patch.object(review_steps.media_tool, name, fn)
            p.start()
            self.addCleanup(p.stop)
        self.args = argparse.Namespace(run="batch-1", jobs=1)

    def q(self, qid, status, file_url, **media_extra):
        m = {"type": "video", "role": "illustrative", "query": "q", "source_url": "p" if file_url else None,
             "file_url": file_url, "credit": "c" if file_url else None, **media_extra}
        return {"id": qid, "status": status, "batch": "batch-1", "locale": "en", "question": {"en": "?"}, "media": m,
                "background": None, "review": {"decision": status, "model": "opus"} if status != "draft" else None}

    def run_record(self, qs, recorded):
        self.pool.write_text(self.json.dumps({"questions": qs}))
        (self.d / "recorded.json").write_text(self.json.dumps(recorded))
        self.assertEqual(self.rs.cmd_record(self.args), [])
        return {x["id"]: x for x in self.json.loads(self.pool.read_text())["questions"]}

    def test_new_long_pick_needs_work(self):
        (self.d / "reviews" / "q-1.json").write_text(self.json.dumps({"round1": {
            "decision": "approved", "feedback": "", "pick": 1, "background_pick": None, "reasons": "r", "problems": [], "model": "opus"}}))
        got = self.run_record([self.q("q-1", "draft", None)], {})["q-1"]
        self.assertEqual(got["status"], "needs_work")
        self.assertIn("59.58 s, over 30 s", got["review"]["feedback"])
        self.assertIsNone(got["media"]["file_url"])
        self.assertNotIn("duration", got["media"])

    def test_earlier_picks_without_duration(self):
        rec = {i: {"decision": "approved", "problems": []} for i in ("q-1", "q-2", "q-3")}
        got = self.run_record([self.q("q-1", "approved", "u-long"), self.q("q-2", "approved", "u-ok"),
                               self.q("q-3", "needs_work", None)], rec)
        self.assertEqual(got["q-1"]["status"], "needs_work")
        self.assertIn("media", got["q-1"]["review"]["problems"])
        self.assertEqual(got["q-1"]["review"]["previous"]["decision"], "approved")
        self.assertIsNone(got["q-1"]["media"]["file_url"])
        self.assertEqual((got["q-2"]["status"], got["q-2"]["media"]["duration"]), ("approved", 20.0))
        self.assertEqual(got["q-3"]["media"]["file_url"], None)
        import validate
        for x in got.values():
            self.assertEqual(validate.media_first_problems(x), [], x["id"])
