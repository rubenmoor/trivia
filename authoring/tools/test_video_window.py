"""`qgen video-window` (plan 216) with a temp pool, stub probes and a stub claude."""
import argparse, contextlib, io, json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order)
import layout  # noqa: E402
import media_first as mf  # noqa: E402
import review_steps  # noqa: E402
import video_window as vw  # noqa: E402


def video_q(qid, status="approved", **media):
    m = {"type": "video", "role": "essential", "query": f"File:{qid}.webm", "file_url": f"https://x/{qid}.webm",
         "license": "CC0"} | media
    return {"id": qid, "status": status, "bundle": "base", "question": "Watch: which animal is this?", "answer": "Lion",
            "wrong_answers": ["Wolf", "Bear", "Owl"], "hints": [], "description": "d", "fun_fact": "f", "difficulty": 4,
            "concept": None, "media": m, "review": {"decision": "approved", "reviewer": "llm", "previous": None}}


class VideoWindow(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp())
        self.pool = self.work / "questions.json"
        self.said, self.calls, self.probed, self.reply = "", [], [], {"verdict": "keep", "problem": None, "note": "lion seen"}
        self.durations = {}
        for p in [mock.patch.object(layout, "WORK", self.work), mock.patch.object(vw, "POOL", self.pool),
                  mock.patch.object(review_steps, "POOL", self.pool), mock.patch.object(mf, "probe", self.probe),
                  mock.patch.object(mf, "commons_text", lambda t: None), mock.patch.object(qgen, "claude", self.claude),
                  mock.patch.object(vw, "duration", lambda m: self.durations[m["file_url"]])]:
            p.start()
            self.addCleanup(p.stop)

    def probe(self, title, excerpt=None):
        d = self.work / "media-probe" / title
        d.mkdir(parents=True, exist_ok=True)
        (d / "ocr.txt").write_text("")
        self.probed.append((title, excerpt))
        return {"dir": str(d), "window": [excerpt["start"], excerpt["end"]], "has_video": True, "speech": {"text": self.said}}

    def claude(self, system, user, schema, model, cwd, read=False, **kw):
        self.calls.append({"user": json.loads(user), "model": model})
        return self.reply

    def run_cmd(self, qs, dry_run=False):
        self.pool.write_text(json.dumps({"questions": qs}))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            errors = vw.cmd_video_window(argparse.Namespace(dry_run=dry_run, model="opus", jobs=1))
        self.assertEqual(errors, [])
        self.out = out.getvalue()
        return {q["id"]: q for q in json.loads(self.pool.read_text())["questions"]}

    def test_cut_from_excerpt_keeps(self):
        got = self.run_cmd([video_q("q-1", duration=120, excerpt={"start": 10, "end": 70})])["q-1"]
        self.assertEqual(got["media"]["excerpt"], {"start": 10, "end": 40})
        self.assertEqual(got["status"], "approved")
        self.assertEqual(self.probed, [("File:q-1.webm", {"start": 10, "end": 40})])
        self.assertEqual(self.calls[0]["user"]["media_first"]["excerpt"], {"start": 10, "end": 40})
        self.assertEqual(self.calls[0]["user"]["cut_from"]["excerpt"], {"start": 10, "end": 70})

    def test_cut_from_no_excerpt(self):
        got = self.run_cmd([video_q("q-1", duration=90)])["q-1"]
        self.assertEqual(got["media"]["excerpt"], {"start": 0, "end": 30})

    def test_duration_fill(self):
        self.durations = {"https://x/q-1.webm": 20.0, "https://x/q-2.webm": 75.5}
        got = self.run_cmd([video_q("q-1"), video_q("q-2")])
        self.assertEqual(got["q-1"]["media"]["duration"], 20.0)
        self.assertNotIn("excerpt", got["q-1"]["media"])  # short file: only the duration, no re-check
        self.assertEqual(got["q-2"]["media"], got["q-2"]["media"] | {"duration": 75.5, "excerpt": {"start": 0, "end": 30}})
        self.assertEqual(len(self.calls), 1)

    def test_fail_needs_work(self):
        self.reply = {"verdict": "needs_work", "problem": "media", "note": "only the savanna before the lion"}
        got = self.run_cmd([video_q("q-1", duration=90)])["q-1"]
        self.assertEqual(got["status"], "needs_work")
        self.assertEqual(got["media"]["excerpt"], {"start": 0, "end": 30})
        r = got["review"]
        self.assertEqual(r["problems"], ["media"])
        self.assertEqual(r["feedback"], "Clue outside the 30 s window: only the savanna before the lion.")
        self.assertEqual(r["previous"]["decision"], "approved")
        self.assertIn("1 needs_work", self.out)

    def test_giveaway_hit_judged(self):
        self.said = "look a lion"
        got = self.run_cmd([video_q("q-1", duration=90)])["q-1"]
        self.assertEqual(got["status"], "approved")  # judgement keep decides
        self.assertIn("answer-heard", json.dumps(self.calls[0]["user"]["media_first"]["mechanical"]))
        self.reply = {"verdict": "needs_work", "problem": "giveaway", "note": "says lion"}
        got = self.run_cmd([video_q("q-1", duration=90)])["q-1"]
        self.assertEqual((got["status"], got["review"]["problems"]), ("needs_work", ["giveaway", "media"]))

    def test_media_first_probe_ref(self):
        q = video_q("q-1", duration=90, excerpt={"start": 0, "end": 60}) | {"media_first": {"class": "general", "probe": "old"}}
        got = self.run_cmd([q])["q-1"]
        self.assertEqual(got["media_first"]["probe"], "media-probe/File:q-1.webm")

    def test_not_approved_only_cut(self):
        got = self.run_cmd([video_q("q-1", "needs_work", duration=90), video_q("q-2", "rejected", duration=90)])
        self.assertEqual(got["q-1"]["media"]["excerpt"], {"start": 0, "end": 30})
        self.assertNotIn("excerpt", got["q-2"]["media"])
        self.assertEqual((self.calls, self.probed), ([], []))

    def test_untouched(self):
        qs = [video_q("q-1", duration=25), video_q("q-2", duration=90, excerpt={"start": 5, "end": 30}),
              video_q("q-3", duration=90) | {"media": {"type": "audio", "duration": 90}}]
        self.run_cmd(qs)
        self.assertIn("No video question", self.out)

    def test_dry_run(self):
        before = [video_q("q-1", duration=90), video_q("q-2")]
        got = self.run_cmd(before, dry_run=True)
        self.assertEqual(list(got.values()), before)
        self.assertIn("q-1 (approved): cut whole file → 0–30 s", self.out)
        self.assertIn("q-2 (approved): duration unknown", self.out)
        self.assertEqual((self.calls, self.probed), ([], []))

    def test_resume(self):
        self.run_cmd([video_q("q-1", duration=90)])
        pool = json.loads(self.pool.read_text())["questions"]
        self.run_cmd(pool)
        self.assertEqual(len(self.calls), 1)
        self.assertIn("No video question", self.out)
        rows = [json.loads(line) for line in (self.work / "video-window" / "results.jsonl").read_text().splitlines()]
        self.assertEqual([(r["id"], r["verdict"]) for r in rows], [("q-1", "keep")])


if __name__ == "__main__":
    unittest.main()
