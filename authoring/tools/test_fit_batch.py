"""`qgen batch --bundle chinese-base --from base` (plan 230) on a fixture: keep, adapt, drop, not copyable,
`translatable: false`, map null, a near-duplicate keep, unmapped refused, resume mid-run, --dry-run, a developer flip,
and validate's fit.json rule. Stub claude and revise steps; no network."""
import argparse, json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order: the command modules import each other)
import audit, fit, layout, review_steps, validate  # noqa: E402

B = "chinese-base"
SUB, NULL_SUB = "vegetables", "christmas"  # from-base.json: vegetables → vegetables, christmas → null
MEDIA = {"type": "image", "role": "decorative", "query": "q", "source_url": None, "file_url": None, "credit": None}
VERDICT = {"q-0001": ("keep", None, None), "q-0002": ("adapt", None, "hint 2: a vegetable known in China"),
           "q-0003": ("drop", "euro_centric", None), "q-0007": ("keep", None, None)}


def q(i, sub=SUB, locale="en", question=None, answer=None, **kw):
    return {"id": i, "status": "approved", "bundle": "base", "locale": locale, "subcategory": sub, "difficulty": 4,
            "description": "d", "question": question or f"Question {i} about a vegetable?", "answer": answer or f"Answer {i}",
            "wrong_answers": ["a", "b", "c"], "hints": ["h1", "h2", "h3"], "fun_fact": "f", "media": dict(MEDIA),
            "background": None, "batch": "batch-9",
            "review": {"decision": "approved", "feedback": None, "problems": [], "reviewed_on": "2026-11-01",
                       "reviewer": "human"}, **kw}


POOL = [q("q-0001", question="Which root is orange?", answer="Carrot"), q("q-0002"), q("q-0003"),
        q("q-0004", locale="es"),  # no en translation: not copyable
        q("q-0005", translatable=False), q("q-0006", sub=NULL_SUB),
        q("q-0007", question="Which root is orange?", answer="Carrot"),  # same fact as q-0001
        q("q-0008", status="needs_work", review=None), q("q-0009", bundle="stem")]


class Killed(BaseException):
    """A kill: nothing in qgen catches it."""


def args(**kw):
    a = dict(translate=None, ids=None, dry_run=False, media_first=False, files=None, until=None, bundle=B,
             run=None, subcategories=None, count=None, jobs=1, from_bundle="base")
    return argparse.Namespace(**(a | kw))


class Fixture(unittest.TestCase):
    """The fixture pool, patched paths and stubs (test_fit_view reuses it)."""
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.work, self.pool, self.fitfile = self.tmp / "work", self.tmp / "questions.json", self.tmp / "fit.json"
        self.work.mkdir()
        self.pool.write_text(json.dumps({"questions": POOL}))
        for obj in (layout, qgen, audit, review_steps, fit):
            self.patch(obj, "WORK", self.work)
        for obj in (qgen, review_steps, fit):
            self.patch(obj, "POOL", self.pool)
        self.patch(layout, "fit", lambda b: self.fitfile)
        self.patch(layout, "REPORTS", self.tmp)
        self.patch(fit, "ROOT", self.tmp)
        self.patch(fit, "en_translations", lambda: {})
        self.patch(fit, "FIT_CHUNK", 2)
        self.patch(fit, "claude", self.claude)
        self.patch(fit, "revise_steps", lambda ns, m, rm: [("revise", self.revise, ns())])
        self.patch(fit, "cmd_audit", lambda a: self.steps.append("audit") or [])
        self.patch(fit, "cmd_export", lambda a: self.steps.append("export") or [])
        self.patch(fit, "cmd_sync_run", lambda a: self.steps.append("sync") or [])
        self.patch(qgen, "validate_pool", lambda: (self.steps.append("validate") or [], []))
        self.calls, self.steps, self.kill_call = [], [], None

    def patch(self, obj, name, value):
        p = mock.patch.object(obj, name, value)
        p.start()
        self.addCleanup(p.stop)

    def claude(self, system, user, schema, model, cwd, with_model=False, **kw):
        self.assertIn(fit.bundle_row(B)["rule"], system)
        items = json.loads(user.split("\n", 1)[1])
        if len(self.calls) == self.kill_call:
            self.kill_call = None
            raise Killed
        self.calls.append([x["id"] for x in items])
        out = {"items": [{"id": x["id"], "verdict": VERDICT[x["id"]][0], "reason": VERDICT[x["id"]][1],
                          "note": "n", "issue": VERDICT[x["id"]][2]} for x in items]}
        return (out, "claude-opus-test") if with_model else out

    def revise(self, a):
        """The revise steps' outcome: the adapted copies approved."""
        self.steps.append("revise")
        ids = set(json.loads((self.work / a.run / "run.json").read_text())["ids"])
        review_steps.update_pool({i: lambda x: x.update(status="approved", review={**x["review"], "decision": "approved",
                                                                                   "feedback": None}) for i in ids})
        (self.work / a.run / "recorded.json").write_text(json.dumps({i: {"decision": "approved"} for i in ids}))
        return []

    def run_batch(self, **kw):
        if qgen._run_lock:
            qgen._run_lock.close()  # a killed process's lock goes with it
        return fit.cmd_fit_batch(args(**kw))

    def data(self):
        return {x["id"]: x for x in json.loads(self.pool.read_text())["questions"]}

    def verdicts(self):
        return json.loads(self.fitfile.read_text())["sources"]


class FitBatch(Fixture):
    def check_end_state(self):
        v, pool = self.verdicts(), self.data()
        self.assertEqual(sorted(v), ["q-0001", "q-0002", "q-0003", "q-0005", "q-0006", "q-0007"])  # q-0004 not copyable
        self.assertEqual((v["q-0003"]["verdict"], v["q-0003"]["reason"], v["q-0003"]["by"]), ("drop", "euro_centric", "fit"))
        self.assertEqual((v["q-0005"]["reason"], v["q-0005"]["by"]), ("wordplay", "rule"))
        self.assertEqual((v["q-0006"]["reason"], v["q-0006"]["by"]), ("euro_centric", "map"))
        copies_ = {c["copied_from"]: c for c in pool.values() if c.get("copied_from")}
        self.assertEqual(sorted(copies_), ["q-0001", "q-0002", "q-0007"])
        for src, c in copies_.items():
            self.assertEqual((c["bundle"], c["locale"], c["subcategory"], c["batch"], v[src]["copy"]), (B, "en", SUB, "fit-1", c["id"]))
            self.assertEqual(c["media"], MEDIA)
            self.assertEqual(c["review"]["fit"], "fit-1")
            self.assertEqual(c["review"]["source_review"]["id"], src)
        self.assertEqual(copies_["q-0001"]["status"], "approved")
        self.assertEqual(copies_["q-0002"]["status"], "approved")  # after the (stub) revise steps
        self.assertTrue(copies_["q-0002"]["review"]["fit"])
        self.assertEqual(copies_["q-0007"]["status"], "needs_work")  # near-duplicate of q-0001's copy
        self.assertIn(copies_["q-0001"]["id"], copies_["q-0007"]["review"]["feedback"])
        self.assertEqual(len(pool), len(POOL) + 3)
        cfg = json.loads((self.work / "fit-1" / "run.json").read_text())
        self.assertEqual(cfg["ids"], [copies_["q-0002"]["id"]])
        self.assertEqual((cfg["not_copyable"], cfg["left"]), (1, 0))
        self.assertIn("done", cfg)
        self.assertEqual(validate.fit_problems(list(pool.values()), [B], lambda b: self.fitfile), [])
        report = (self.tmp / "fit-1.md").read_text()
        self.assertIn("kept 2, adapted 1, dropped 1", report)
        self.assertIn("Not copyable yet (no approved, current English text): 1", report)

    def test_run(self):
        self.run_batch()
        self.assertEqual(sorted(sum(self.calls, [])), ["q-0001", "q-0002", "q-0003", "q-0007"])
        self.assertEqual(self.steps, ["revise", "audit", "export", "sync", "validate"])
        self.check_end_state()
        adapt = next(c for c in self.data().values() if c.get("copied_from") == "q-0002")
        self.assertEqual(adapt["review"]["model"], "claude-opus-test")
        with self.assertRaises(SystemExit) as e:  # all judged
            self.run_batch()
        self.assertIn("Nothing to judge", str(e.exception))

    def test_resume_after_kill_in_fit(self):
        self.kill_call = 1  # the second chunk
        with self.assertRaises(Killed):
            self.run_batch()
        self.assertEqual(len(self.calls), 1)
        self.run_batch()
        self.assertEqual(len(self.calls), 2)  # the first chunk not asked again
        self.check_end_state()

    def test_resume_after_kill_in_copy(self):
        real, n = fit.save_verdicts, []

        def save(b, e):
            n.append(1)
            if len(n) == 3:  # select, fit, copy: the pool is written, fit.json not yet
                raise Killed
            real(b, e)
        with mock.patch.object(fit, "save_verdicts", save), self.assertRaises(Killed):
            self.run_batch()
        self.run_batch()
        self.check_end_state()  # no second copy

    def test_dry_run(self):
        with mock.patch("sys.stdout") as out:
            self.run_batch(dry_run=True)
        text = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("fit-1 would judge 4 base sources", text)
        self.assertIn("drop 2 by rule", text)
        self.assertIn("1 not copyable yet", text)
        self.assertEqual((self.calls, list(self.work.iterdir()), self.fitfile.exists()), ([], [], False))

    def test_count(self):
        self.run_batch(count=2)
        self.assertEqual(sum(self.calls, []), ["q-0001", "q-0002"])
        cfg = json.loads((self.work / "fit-1" / "run.json").read_text())
        self.assertEqual(cfg["left"], 2)

    def test_unmapped_refused(self):
        m = self.tmp / "from-base.json"
        m.write_text(json.dumps({"subcategories": {NULL_SUB: {"to": None, "reason": "euro_centric", "by": "map"}}}))
        with mock.patch.object(layout, "from_base", lambda b: m), self.assertRaises(SystemExit) as e:
            self.run_batch()
        self.assertIn(f"'{SUB}'", str(e.exception))
        self.assertEqual(self.calls, [])

    def test_refusals(self):
        for kw, says in [({"bundle": "base"}, "another base bundle"), ({"bundle": "stem"}, "kind theme"),
                         ({"from_bundle": "stem"}, "only base"), ({"translate": "en"}, "only --bundle")]:
            with self.subTest(kw=kw), self.assertRaises(SystemExit) as e:
                self.run_batch(**kw)
            self.assertIn(says, str(e.exception))
        with mock.patch.object(fit, "PROMPTS", self.tmp), self.assertRaises(SystemExit) as e:
            self.run_batch()
        self.assertIn("fit.md", str(e.exception))

    def test_developer_flip(self):
        self.run_batch()
        v = self.verdicts()
        v["q-0003"] = {**v["q-0003"], "verdict": "keep", "reason": None, "by": "developer", "copy": None}
        self.fitfile.write_text(json.dumps({"sources": v}))
        self.assertEqual(validate.fit_problems(list(self.data().values()), [B], lambda b: self.fitfile), [])
        calls = len(self.calls)
        self.run_batch()
        self.assertEqual(len(self.calls), calls)  # no fit call for a flip
        c = next(c for c in self.data().values() if c.get("copied_from") == "q-0003")
        self.assertEqual((c["status"], c["review"]["reviewer"], c["batch"]), ("approved", "human", "fit-2"))
        self.assertEqual(self.verdicts()["q-0003"]["copy"], c["id"])


class Rules(unittest.TestCase):
    def test_fit_problems(self):
        src, cp = q("q-0001"), {**q("q-0002", bundle=B), "copied_from": "q-0001"}
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "fit.json"

            def errors(entries, qs=(src, cp)):
                f.write_text(json.dumps({"sources": entries}))
                return validate.fit_problems(list(qs), [B], lambda b: f)
            ok = {"verdict": "keep", "reason": None, "by": "fit", "run": "fit-1", "copy": "q-0002"}
            self.assertEqual(errors({"q-0001": ok}), [])
            self.assertTrue(errors({}))  # a copy without an entry
            self.assertTrue(errors({"q-0001": {**ok, "copy": None}}))  # keep by fit without a copy
            self.assertEqual(errors({"q-0001": {**ok, "copy": None, "by": "developer"}}, (src,)), [])  # flip pending
            self.assertTrue(errors({"q-0001": {**ok, "verdict": "drop"}}))  # drop without reason (and the copy)
            self.assertTrue(errors({"q-0001": ok, "q-0404": {**ok, "verdict": "drop", "reason": "other", "copy": None}}))
            self.assertTrue(errors({"q-0001": {**ok, "verdict": "maybe"}}))
            self.assertEqual(errors({"q-0001": {**ok, "copy": "q-0002"}}, (src, {**cp, "status": "rejected"})), [])
            flip = {**ok, "verdict": "drop", "reason": "other", "by": "developer"}  # keep → drop: the copy rejected
            self.assertEqual(errors({"q-0001": flip}, (src, {**cp, "status": "rejected"})), [])
            self.assertTrue(errors({"q-0001": flip}))  # its copy still live
            self.assertTrue(errors({"q-0001": {**flip, "by": "fit"}}, (src, {**cp, "status": "rejected"})))

    def test_fix_issue(self):
        x = {"status": "needs_work", "review": {"fit": "fit-1", "feedback": f"{fit.ADAPT}: hint 2", "reviewer": "llm"}}
        self.assertEqual(review_steps.fix_issue(x, {}, True), f"{fit.ADAPT}: hint 2")
        self.assertIn("fit", review_steps.REWORK_MODES)


if __name__ == "__main__":
    unittest.main()
