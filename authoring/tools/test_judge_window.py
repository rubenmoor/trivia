"""`media_first.judge_window`: the 30 s re-check's judgement (plan 217) with a stub claude and stub probes."""
import json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order)
import layout  # noqa: E402
import media_first as mf  # noqa: E402

W = {"start": 0, "end": 30}


def video_q(**kw):
    q = {"id": "q-1", "question": "Watch: which animal is this?", "answer": "Lion", "wrong_answers": ["Wolf", "Bear", "Owl"],
         "hints": ["a", "b", "c"], "description": "d", "fun_fact": "f", "difficulty": 4, "concept": None,
         "media": {"type": "video", "role": "essential", "query": "File:Lion.webm", "license": "CC0", "duration": 90,
                   "excerpt": {"start": 0, "end": 60}},
         "media_first": {"class": "general", "kind": "animal", "probe": "x"}}
    return q | kw


class JudgeWindow(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp())
        self.said, self.calls, self.reply = "", [], None
        for p in [mock.patch.object(layout, "WORK", self.work), mock.patch.object(mf, "probe", self.probe),
                  mock.patch.object(mf, "commons_file", lambda t: None),
                  mock.patch.object(mf.commons, "file_records", self.records), mock.patch.object(qgen, "claude", self.claude)]:
            p.start()
            self.addCleanup(p.stop)

    def probe(self, title, excerpt=None):
        d = self.work / "probe"
        d.mkdir(exist_ok=True)
        (d / "ocr.txt").write_text("")
        self.probed = (title, excerpt)
        return {"dir": str(d), "window": [excerpt["start"], excerpt["end"]], "has_video": True, "speech": {"text": self.said}}

    def records(self, titles):
        return [{"title": titles[0], "description": "Moon landing", "categories": ["Apollo 11"]}]

    def claude(self, system, user, schema, model, cwd, read=False, **kw):
        self.calls.append({"system": system, "user": json.loads(user), "model": model, "cwd": cwd, "read": read})
        return self.reply

    def test_keep(self):
        self.reply = {"verdict": "keep", "problem": None, "note": "lion in frames 2-5"}
        self.assertEqual(mf.judge_window(video_q(), W), {"verdict": "keep", "problem": None, "note": "lion in frames 2-5"})
        c = self.calls[0]
        self.assertEqual((c["model"], c["read"]), ("opus", True))
        self.assertIn("still works on the cut one", c["system"])
        self.assertIn("## Checks", c["system"])  # media-first-checks.md included, not copied
        self.assertNotIn("{max_video_s}", c["system"])
        self.assertEqual(c["user"]["media_first"]["excerpt"], W)
        self.assertEqual(c["user"]["cut_from"]["excerpt"], {"start": 0, "end": 60})
        self.assertEqual(self.probed, ("File:Lion.webm", W))
        self.assertTrue(Path(c["cwd"]).is_dir())

    def test_needs_work(self):
        self.reply = {"verdict": "needs_work", "problem": "media", "note": "only the savanna before the lion"}
        self.assertEqual(mf.judge_window(video_q(), W)["problem"], "media")

    def test_heard_answer_goes_to_the_model(self):
        self.said, self.reply = "look a lion", {"verdict": "needs_work", "problem": "giveaway", "note": "said"}
        self.assertEqual(mf.judge_window(video_q(), W)["problem"], "giveaway")
        found = self.calls[0]["user"]["media_first"]["mechanical"]
        self.assertIn("answer-heard", [f["check"] for f in found])

    def test_question_first(self):
        q = video_q()
        del q["media_first"]
        q["media"] = {"type": "video", "role": "illustrative", "query": "Apollo 11 moon landing footage", "license": "Public domain",
                      "source_url": "https://commons.wikimedia.org/wiki/File%3AHistoric_Apollo_11_Moon_Landing_Footage.webm"}
        self.reply = {"verdict": "keep", "problem": None, "note": ""}
        mf.judge_window(q, W)
        u = self.calls[0]["user"]
        self.assertEqual(self.probed[0], "File:Historic Apollo 11 Moon Landing Footage.webm")
        self.assertEqual(u["media_first"]["commons"], {"description": "Moon landing", "categories": ["Apollo 11"]})
        self.assertIsNone(u["media_first"]["class"])
        self.assertEqual(u["cut_from"], {"excerpt": None, "duration": None})

    def test_malformed(self):
        for bad in ({"verdict": "maybe", "problem": None, "note": ""}, {"verdict": "needs_work", "problem": None, "note": ""}, None):
            self.reply = bad
            with self.assertRaises(ValueError):
                mf.judge_window(video_q(), W)


if __name__ == "__main__":
    unittest.main()


class PromptPlaceholders(unittest.TestCase):
    def test_media_prompts_have_no_max_placeholder(self):
        for names in (["review", "media-first-checks"], ["audit", "media-first-checks"], ["house-style", "revise", "media-first-checks"],
                      ["media-window"]):
            self.assertNotIn("{max_", qgen.prompt(*names, locale="en"), names)
