"""The fit view's API and flips (plan 230): rows, drop sample, drop → keep copied by the next run without a call,
keep → drop rejecting the copy, refusals. Reuses test_fit_batch's fixture."""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))
import test_fit_batch as tb  # noqa: E402
import audit, fit_view, reviews, spot_checks, validate  # noqa: E402


class FitView(tb.Fixture):
    def setUp(self):
        super().setUp()
        self.patch(reviews, "POOL", self.pool)
        self.patch(reviews, "save_pool", lambda d: self.pool.write_text(json.dumps(d)))
        self.patch(audit, "POOL", self.pool)
        self.run_batch()

    def check(self):
        self.assertEqual(validate.fit_problems(list(self.data().values()), [tb.B], lambda b: self.fitfile), [])

    def test_build(self):
        out = fit_view.build({"bundle": tb.B})
        rows = {r["id"]: r for r in out["rows"]}
        self.assertEqual((rows["q-0001"]["verdict"], rows["q-0003"]["verdict"], rows["q-0003"]["reason"]), ("keep", "drop", "euro_centric"))
        self.assertEqual((rows["q-0002"]["verdict"], rows["q-0002"]["copy"]["id"]), ("adapt", self.verdicts()["q-0002"]["copy"]))
        self.assertEqual(rows["q-0002"]["source"]["question"], "Question q-0002 about a vegetable?")
        self.assertEqual(out["runs"], ["fit-1"])
        self.assertEqual(out["drop_sample"], {"fit-1": ["q-0003"]})  # fit drops only, not the rule's

    def test_spot_check_sample_kept_and_adapted(self):
        v = self.verdicts()
        kept, adapted = v["q-0001"]["copy"], v["q-0002"]["copy"]
        self.assertEqual(audit.audit_sample("fit-1", 30), [adapted])  # the audit reads the adapted copies only
        got = spot_checks.sample("fit-1")
        self.assertIn(kept, got)
        self.assertIn(adapted, got)
        self.assertEqual(audit.spot_decisions("fit-1")[kept], "approved")

    def test_drop_to_keep_next_run_copies_without_call(self):
        e = fit_view.flip(tb.B, "q-0003", "keep")
        self.assertEqual((e["verdict"], e["by"], e["copy"]), ("keep", "developer", None))
        self.check()
        calls = len(self.calls)
        self.run_batch()
        self.assertEqual(len(self.calls), calls)
        c = next(c for c in self.data().values() if c.get("copied_from") == "q-0003")
        self.assertEqual((c["status"], c["review"]["reviewer"]), ("approved", "human"))

    def test_keep_to_drop_rejects_copy(self):
        cid = self.verdicts()["q-0001"]["copy"]
        e = fit_view.flip(tb.B, "q-0001", "drop", "euro_centric")
        self.assertEqual((e["verdict"], e["by"], e["copy"]), ("drop", "developer", cid))
        self.assertEqual(self.data()[cid]["status"], "rejected")
        self.check()
        with self.assertRaises(SystemExit):
            self.run_batch()  # nothing left to do: it doesn't copy it again
        self.assertEqual(self.data()[cid]["status"], "rejected")
        self.assertEqual(len([c for c in self.data().values() if c.get("copied_from") == "q-0001"]), 1)
        with self.assertRaises(ValueError):
            fit_view.flip(tb.B, "q-0001", "keep")  # its copy was rejected

    def test_refusals(self):
        for sid, verdict, says in [("q-0002", "drop", "own review"), ("q-0006", "keep", "dropped by map"), ("q-9999", "keep", "no verdict"),
                                   ("q-0001", "adapt", "keep or drop"), ("q-0003", "maybe", "keep or drop")]:
            with self.subTest(sid=sid), self.assertRaises(ValueError) as x:
                fit_view.flip(tb.B, sid, verdict)
            self.assertIn(says, str(x.exception))
        with self.assertRaises(ValueError):
            fit_view.flip(tb.B, "q-0001", "drop", "bogus")


if __name__ == "__main__":
    import unittest
    unittest.main()
