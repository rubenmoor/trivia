"""`qgen batch --media-first` (plan 203): step order, resume after a kill, cross-mode refusal, fixed media slot.
Stub steps and a stub claude; no network."""
import argparse, json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order: the command modules import each other)
import batches  # noqa: E402
import categories  # noqa: E402
import audit  # noqa: E402
import health  # noqa: E402
import layout  # noqa: E402
import media as media_tool  # noqa: E402
import media_first as mf  # noqa: E402
import review_steps  # noqa: E402
import rework  # noqa: E402

STEPS = ["inventory", "probe", "triage", "design", "giveaway", "english-keys", "rate", "factcheck", "revise", "apply",
         "rate", "factcheck", "merge", "media", "sheets", "review 1", "fix", "giveaway", "research", "media", "sheets",
         "review 2", "record", "audit", "export", "sync", "batch-report", "validate"]
QGEN_STEPS = {"rate": "cmd_rate", "factcheck": "cmd_factcheck", "revise": "cmd_revise", "apply": "cmd_apply",
              "merge": "cmd_merge", "media": "cmd_media", "sheets": "cmd_sheets", "review": "cmd_review", "fix": "cmd_fix",
              "research": "cmd_research", "record": "cmd_record", "audit": "cmd_audit", "export": "cmd_export",
              "sync": "cmd_sync_run", "batch-report": "cmd_batch_report", "english-keys": "cmd_english_keys",
              "concepts": "cmd_concepts", "draft": "cmd_draft"}
MF_STEPS = {"inventory": "inventory_step", "probe": "probe_step", "triage": "triage", "design": "design"}
SUB = categories.load("base")[0]["subcategories"][0]


class Killed(BaseException):
    """A kill: nothing in qgen catches it."""


def args(**kw):
    a = dict(translate=None, ids=None, dry_run=False, media_first=False, files=None, until=None, bundle="base",
             run=None, subcategories=None, count=None, jobs=1)
    return argparse.Namespace(**(a | kw))


class Base(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp())
        self.pool = self.work / "questions.json"
        self.pool.write_text(json.dumps({"questions": []}))
        for obj, name in [(layout, "WORK"), (qgen, "WORK"), (batches, "WORK"), (review_steps, "WORK")]:
            self.patch(obj, name, self.work)
        for obj in (qgen, review_steps):
            self.patch(obj, "POOL", self.pool)

    def patch(self, obj, name, value):
        p = mock.patch.object(obj, name, value)
        p.start()
        self.addCleanup(p.stop)


class Orchestration(Base):
    def setUp(self):
        super().setUp()
        self.calls, self.kill_at = [], None
        self.patch(health, "unacked_failure", lambda: None)
        self.patch(qgen, "validate_pool", lambda: (self.step("validate"), None))
        for step, fn in QGEN_STEPS.items():
            self.patch(qgen, fn, lambda a, step=step: self.step(step if step != "review" else f"review {a.round}", a))
        for step, fn in MF_STEPS.items():
            self.patch(mf, fn, lambda *a, step=step, **kw: self.step(step))
        self.patch(mf, "check_drafts", lambda d: self.step("giveaway"))
        self.patch(mf, "check_fixed", lambda run: self.step("giveaway"))

    def step(self, name, a=None):
        if a is not None:
            self.assertEqual(a.run, "batch-1")
        if len(self.calls) == self.kill_at:
            self.kill_at = None
            raise Killed
        self.calls.append(name)
        return []

    def batch(self, **kw):
        if qgen._run_lock:
            qgen._run_lock.close()  # the killed process's lock goes with it
        qgen.cmd_batch(args(**kw))

    def cfg(self, run="batch-1"):
        return json.loads((self.work / run / "run.json").read_text())

    def test_step_order(self):
        self.batch(media_first=True)
        self.assertEqual(self.calls, STEPS)
        self.assertEqual(self.cfg()["mode"], "media-first")
        self.assertEqual(self.cfg()["draft_locale"], "en")
        self.assertIn("done", self.cfg())

    def test_resume_after_kill_at_each_step(self):
        for k in range(len(STEPS)):
            with self.subTest(step=STEPS[k], at=k):
                self.setUp()
                self.kill_at = k
                with self.assertRaises(Killed):
                    self.batch(media_first=True)
                self.assertNotIn("done", self.cfg())
                self.calls = []
                self.batch(media_first=True)  # every step again; each skips its own finished work
                self.assertEqual(self.calls, STEPS)
                self.assertIn("done", self.cfg())
                self.assertEqual(sorted(p.name for p in self.work.glob("batch-*")), ["batch-1"])

    def test_one_counter(self):
        (self.work / "batch-4").mkdir()
        (self.work / "batch-4" / "run.json").write_text(json.dumps({"mode": "batch", "done": "2026-11-01"}))
        self.patch(qgen, "run_steps", lambda *a, **kw: 0)
        self.batch(media_first=True)
        self.assertEqual(self.cfg("batch-5")["mode"], "media-first")

    def test_cross_mode_refusal(self):
        for open_mode, flag, says in [("media-first", False, "qgen batch --media-first"), ("batch", True, "qgen batch")]:
            with self.subTest(open=open_mode):
                (self.work / "batch-2").mkdir(exist_ok=True)
                (self.work / "batch-2" / "run.json").write_text(json.dumps({"mode": open_mode, "bundle": "base"}))
                with self.assertRaises(SystemExit) as e:
                    self.batch(media_first=flag)
                self.assertIn(f"Finish it first: {says}", str(e.exception))
                self.assertEqual(self.calls, [])

    def test_until(self):
        self.batch(media_first=True, files=40, until="design")
        self.assertEqual(self.calls, STEPS[:4])
        self.assertNotIn("done", self.cfg())
        self.assertEqual(self.cfg()["files"], 40)
        for bad in ("merge", "record"):
            with self.assertRaises(SystemExit):
                self.batch(media_first=True, until=bad)
        with self.assertRaises(SystemExit):
            self.batch(until="design")  # needs --media-first


def media_first_question(qid="q-0001"):
    f = {"title": "File:lion.ogg", "type": "audio", "page_url": "https://c/lion", "file_url": "https://u/lion.ogg",
         "license": "CC0", "license_url": None, "author": "A", "restrictions": []}
    media = {**media_tool.pick_fields(f), "role": "essential", "query": "File:lion.ogg", "note": None, "duration": 20.0}
    return {"id": qid, "status": "draft", "batch": "batch-1", "bundle": "base", "locale": "en", "subcategory": SUB,
            "difficulty": 3, "description": "A sound", "question": "Listen: which animal is this?", "answer": "Lion",
            "wrong_answers": ["Wolf", "Bear", "Owl"], "hints": ["a", "b", "c"], "fun_fact": "f", "concept": "Lion",
            "needs_media": True, "media": media,
            "background": {"query": "savanna", "source_url": None, "file_url": None, "credit": None},
            "media_first": {"seed": "s", "class": "general", "kind": "animal", "probe": "media-probe/lion"}}


class FixedSlot(Base):
    def setUp(self):
        super().setUp()
        self.d = self.work / "batch-1"
        self.d.mkdir()
        (self.d / "run.json").write_text(json.dumps({"mode": "media-first", "bundle": "base", "draft_locale": "en"}))
        self.q = media_first_question()
        self.pool.write_text(json.dumps({"questions": [self.q]}))
        self.fetched = []
        self.patch(media_tool, "fetch_for", lambda q, slot="media", **kw: self.fetched.append((q["id"], slot)) or {"candidates": []})
        self.patch(media_tool, "load_candidates", lambda qid, slot="media": None)
        p = self.work / "media-probe" / "lion"
        p.mkdir(parents=True)
        (p / "probe.json").write_text(json.dumps({"duration": 20, "speech": {"text": "a lion roars"}}))
        (p / "ocr.txt").write_text("")

    def pooled(self):
        return json.loads(self.pool.read_text())["questions"][0]

    def review(self, r):
        (self.d / "reviews").mkdir(exist_ok=True)
        (self.d / "reviews" / "q-0001.json").write_text(json.dumps(r))

    def test_media_and_research_search_only_the_background(self):
        a = argparse.Namespace(run="batch-1", jobs=1)
        self.assertEqual(review_steps.kept_slots("batch-1", self.q), {"media"})
        review_steps.cmd_media(a)
        self.assertEqual(self.fetched, [("q-0001", "background")])
        self.review({"round1": {"decision": "needs_work", "pick": None, "background_pick": None, "new_query": "grassland"}})
        review_steps.cmd_research(a)
        self.assertEqual(self.fetched[1:], [("q-0001", "background")])
        self.assertEqual(self.pooled()["background"]["query"], "grassland")
        self.assertEqual(self.pooled()["media"], self.q["media"])

    def test_rework_run_keeps_media(self):
        (self.d / "run.json").write_text(json.dumps({"mode": "rework", "ids": ["q-0001"]}))
        self.pool.write_text(json.dumps({"questions": [{**self.q, "status": "draft", "batch": "batch-1"}]}))  # fix made it a draft
        a = argparse.Namespace(run="batch-1", jobs=1)
        self.assertEqual(review_steps.kept_slots("batch-1", self.q), {"media"})
        review_steps.cmd_media(a)
        self.assertEqual(self.fetched, [("q-0001", "background")])
        self.review({"round1": {"decision": "needs_work", "pick": None, "background_pick": None, "new_query": "grassland"}})
        review_steps.cmd_research(a)
        self.assertEqual(self.fetched[1:], [("q-0001", "background")])
        self.assertEqual(self.pooled()["media"], self.q["media"])
        self.assertIn("giveaway", [n for n, *_ in rework.revise_steps(lambda **kw: None, "opus", "opus")])

    def test_mixed_rework_research_uses_each_questions_slot(self):
        (self.d / "run.json").write_text(json.dumps({"mode": "rework", "ids": ["q-0002", "q-0001"]}))
        plain = {**self.q, "id": "q-0002", "media": {"type": "image", "role": "illustrative", "query": "old", "note": None,
                 "file_url": None}, "background": None, "status": "draft", "batch": "batch-1"}
        del plain["media_first"]
        self.pool.write_text(json.dumps({"questions": [plain, {**self.q, "status": "draft", "batch": "batch-1"}]}))
        for qid in ("q-0002", "q-0001"):
            (self.d / "reviews").mkdir(exist_ok=True)
            (self.d / "reviews" / f"{qid}.json").write_text(json.dumps(
                {"round1": {"decision": "needs_work", "pick": None, "background_pick": None, "new_query": f"new {qid}"}}))
        self.assertEqual(review_steps.cmd_research(argparse.Namespace(run="batch-1", jobs=1)), [])
        by_id = {x["id"]: x for x in json.loads(self.pool.read_text())["questions"]}
        self.assertEqual(by_id["q-0002"]["media"]["query"], "new q-0002")
        self.assertIsNone(by_id["q-0002"]["background"])
        self.assertEqual(by_id["q-0001"]["background"]["query"], "new q-0001")
        self.assertEqual(by_id["q-0001"]["media"], self.q["media"])

    def test_revise_keeps_media(self):
        q = json.loads(json.dumps(self.q))
        new = {**{k: q[k] for k in qgen.QUESTION_FIELDS}, "needs_media": True, "background_query": "savanna",
               "media": {"type": "image", "role": "illustrative", "query": "lion photo", "note": "x"}}
        qgen.revise_in_pool(q, new, "r", "2026-11-15")
        self.assertEqual(q["media"], self.q["media"])

    def test_fixed_giveaway_makes_needs_work(self):
        self.pool.write_text(json.dumps({"questions": [self.q]}))
        self.review({"round1": {"decision": "needs_work", "feedback": "", "fix": "x", "pick": None, "background_pick": None,
                                "new_query": None, "reasons": "r", "problems": [], "model": "opus"},
                     "fix": {"action": "revise", "changed": ["answer"]},
                     "round2": {"decision": "approved", "feedback": "", "fix": "", "pick": None, "background_pick": 1,
                                "new_query": None, "reasons": "r", "problems": [], "model": "opus"}})
        mf.check_fixed("batch-1")
        self.assertEqual(json.loads((self.d / "reviews" / "q-0001.json").read_text())["giveaway"], ["lion"])
        self.patch(review_steps, "check_picks", lambda picks, jobs: None)
        review_steps.cmd_record(argparse.Namespace(run="batch-1", jobs=1))
        q = self.pooled()
        self.assertEqual(q["status"], "needs_work")
        self.assertIn("giveaway", q["review"]["problems"])
        self.assertEqual({k: q["media"][k] for k in self.q["media"]}, self.q["media"])

    def test_record_demotes_an_approved_recorded_question_with_a_hard_finding(self):
        ogg = {**self.q["media"], "type": "video", "file_url": "https://upload.wikimedia.org/x/lion.ogg?v=1"}
        was = {"decision": "approved", "feedback": None, "problems": [], "reviewed_on": "2026-11-01", "reviewer": "llm",
               "model": "opus"}
        q = {**self.q, "media": ogg, "status": "approved", "batch": "batch-1", "review": was}
        self.pool.write_text(json.dumps({"questions": [q]}))
        (self.d / "recorded.json").write_text(json.dumps({"q-0001": {"decision": "approved", "problems": []}}))
        self.assertEqual(review_steps.cmd_record(argparse.Namespace(run="batch-1", jobs=1)), [])
        got = self.pooled()
        self.assertEqual(got["status"], "needs_work")
        self.assertEqual(got["review"]["decision"], "needs_work")
        self.assertIn("media", got["review"]["problems"])
        self.assertIn("can't play it", got["review"]["feedback"])
        self.assertEqual(got["review"]["previous"], was)
        self.assertEqual(json.loads((self.d / "recorded.json").read_text())["q-0001"]["decision"], "needs_work")

    def test_review_and_fix_see_the_aids(self):
        (self.work / "media-probe" / "lion" / "spectrogram.png").write_bytes(b"png")
        self.patch(mf, "LEDGER", self.work / "media-first" / "files.jsonl")
        mf.record("batch-1", [{"title": "File:lion.ogg", "seed": "s", "worth": True, "verdict": "worth"}])
        mf.write_jsonl(self.d / mf.QUEUE, [{"title": "File:lion.ogg", "description": "A lion roaring at dusk",
                                            "categories": ["Panthera leo"]}])
        seen = []

        def stub(system, user, schema, model, cwd, read=False, **kw):
            seen.append((system, json.loads(user.split("\n", 1)[1]), read))
            if "results" in schema["properties"]:
                return {"results": []}
            out = {"decision": "needs_work", "feedback": "f", "fix": "x", "pick": None, "background_pick": None,
                   "new_query": None, "reasons": "r", "problems": ["giveaway"]}
            return (out, "opus") if kw.get("with_model") else out
        self.patch(review_steps, "claude", stub)
        review_steps.cmd_review(argparse.Namespace(run="batch-1", round=1, jobs=1, model="opus"))
        review_steps.cmd_fix(argparse.Namespace(run="batch-1", jobs=1, model="opus"))  # the stub answers no fix
        (rs, review, rread), (fs, fix, fread) = seen
        mfi, fixed = review["media_first"], fix[0]["media_first"]
        self.assertTrue(rread and fread)
        self.assertIn("Media-first questions", rs)
        self.assertIn("Media-first questions", fs)
        self.assertEqual(mfi["aids"]["pictures_to_read"], [str(self.work / "media-probe" / "lion" / "spectrogram.png")])
        self.assertEqual(mfi["aids"]["speech"]["text"], "a lion roars")
        self.assertEqual(mfi["commons"], {"description": "A lion roaring at dusk", "categories": ["Panthera leo"]})
        self.assertEqual((mfi["file"], mfi["class"]), ("File:lion.ogg", "general"))
        self.assertEqual([f["check"] for f in mfi["mechanical"]], ["answer-heard"])
        self.assertEqual(fixed, mfi)

    def test_audit_sees_the_aids_not_the_review(self):
        self.patch(audit, "WORK", self.work)
        self.patch(audit, "POOL", self.pool)
        self.patch(mf, "LEDGER", self.work / "media-first" / "files.jsonl")
        self.review({"round1": {"decision": "needs_work", "feedback": "SECRET-VERDICT", "fix": "x", "problems": []}})
        seen = []

        def stub(system, user, schema, model, cwd, read=False, **kw):
            seen.append((system, json.loads(user.split("\n", 1)[1]), read, user))
            return ({"verdict": "ok", "problems": [], "severity": "minor", "difficulty_estimate": 3, "notes": "n"}, "opus")
        self.patch(audit, "claude", stub)
        self.patch(audit, "related_questions", lambda *a: [])
        audit.audit_ids("batch-1", ["q-0001"], argparse.Namespace(jobs=1, model="opus"))
        (system, inp, read, raw), = seen
        self.assertTrue(read)
        self.assertIn("Media-first questions", system)
        self.assertEqual(inp["media_first"], mf.review_input(self.q))
        self.assertEqual(inp["media_first"]["aids"]["speech"]["text"], "a lion roars")
        self.assertNotIn("SECRET-VERDICT", raw)
        self.assertNotIn("review", inp)

    def test_review_page_aids(self):
        sys.path.insert(0, str(Path(__file__).parent.parent / "server"))
        import main as server  # noqa: E402
        self.patch(server.layout, "WORK", self.work)
        (self.work / "media-probe" / "lion" / "spectrogram.png").write_bytes(b"png")
        a = server.media_aids(self.q)
        self.assertEqual(a["pictures"], ["/probe/lion/spectrogram.png"])
        self.assertEqual(a["speech"]["text"], "a lion roars")
        self.assertEqual([f["check"] for f in a["mechanical"]], ["answer-heard"])
        self.assertIsNone(server.media_aids({"id": "q-2"}))
        self.assertIsNone(server.media_aids({**self.q, "media_first": {**self.q["media_first"], "probe": "media-probe/none"}}))

    def test_merge_keeps_media_and_provenance(self):
        self.pool.write_text(json.dumps({"questions": [{**self.q, "id": "q-0100", "status": "approved", "batch": "x",
                                                       "answer": "Zebra", "concept": "Zebra"}]}))
        draft = {**{k: self.q[k] for k in ("subcategory", "difficulty", "description", "question", "answer",
                                            "wrong_answers", "hints", "fun_fact", "concept", "needs_media", "media",
                                            "media_first", "bundle")},
                 "tmp_id": "mf-1", "style": None, "axes": None, "needs_fact_check": False, "background_query": "savanna"}
        (self.d / "drafts").mkdir()
        (self.d / "drafts" / "mf-1.json").write_text(json.dumps({"questions": [draft], "skipped": []}))
        (self.d / "ratings").mkdir()
        (self.d / "ratings" / "mf-1.json").write_text(json.dumps(
            {"mf-1": {**{k: 5 for k in qgen.RUBRIC}, "difficulty_estimate": 3, "notes": ""}}))
        self.patch(qgen, "ROOT", self.work)
        qgen.cmd_merge(argparse.Namespace(run="batch-1", min_score=0))
        new = json.loads(self.pool.read_text())["questions"][-1]
        self.assertEqual((new["id"], new["media"], new["media_first"]), ("q-0101", self.q["media"], self.q["media_first"]))
        self.assertEqual(new["background"]["query"], "savanna")


if __name__ == "__main__":
    unittest.main()
