"""Media-first QC and batch health (plan 204, decision 647): spot-check size, QC trend rows, health thresholds; fixture runs, no network."""
import json, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import audit, health, layout, report, review_steps, targets  # noqa: E402


def item(llm, human, problems=()):
    return {"llm": llm, "human": human, "problems": list(problems), "difficulty": [5, 5], "media_changed": False}


class Qc(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp())
        self.saved = [(m, k, getattr(m, k)) for m, k in
                      [(audit, "WORK"), (review_steps, "WORK"), (report, "WORK"), (health, "WORK"), (layout, "SPOT_CHECKS")]]
        audit.WORK = review_steps.WORK = report.WORK = health.WORK = self.work
        layout.SPOT_CHECKS = self.work / "spot-checks.json"
        for run, mode in [("batch-4", "batch"), ("batch-5", "media-first"), ("batch-6", "media-first")]:
            (self.work / run).mkdir()
            (self.work / run / "run.json").write_text(json.dumps({"mode": mode}))
            (self.work / run / "recorded.json").write_text("{}")

    def tearDown(self):
        for m, k, v in self.saved:
            setattr(m, k, v)

    def checks(self, **runs):
        layout.SPOT_CHECKS.write_text(json.dumps({r: {"items": {f"q-{r}-{n}": it for n, it in enumerate(its)}}
                                                  for r, its in runs.items()}))

    def test_targets_valid(self):
        self.assertEqual(targets.quality_problems(), [])
        self.assertEqual(targets.health_problems(health.THRESHOLDABLE), [])
        self.assertEqual(targets.load_quality(), {"spot_check_size": 30, "min_agreement": 0.9})
        q = targets.load_quality(targets.MEDIA_FIRST)
        self.assertEqual((q["spot_check_size"], q["first_run_size"], q["min_agreement"]), (40, 60, 0.9))

    def test_sizes(self):
        self.assertEqual([audit.spot_check_size(r) for r in ("batch-4", "batch-5", "batch-6")], [30, 60, 40])
        self.assertEqual(audit.audit_size("batch-5"), 60)

    def test_qc_trend(self):
        ok, bad = item("approved", "approved"), item("approved", "needs_work", ["media"])
        self.checks(**{"batch-4": [ok] * 30, "batch-5": [ok] * 55 + [bad] * 5, "batch-6": [ok] * 30 + [bad] * 3 + [item("approved", "needs_work", ["giveaway"])] * 7})
        s = report.qc_stats("batch-5", json.loads(layout.SPOT_CHECKS.read_text()))
        self.assertEqual((s["mode"], s["quality"]["spot_check_size"], s["human_n"], s["agreed"]), ("media-first", 60, 60, 55))
        self.assertEqual(report.release_failures(s), [])
        text = "\n".join(report.qc_trend([]))
        self.assertIn("| mode | batch | media-first | media-first |", text)
        self.assertIn("agreement 85/100 (85 %) ✗ over 2 media-first run(s)", text)  # 55+30 of 60+40
        self.assertIn("disagreements: media 8, giveaway 7", text)

    def test_size_bar(self):
        short = item("approved", "approved")
        self.checks(**{"batch-5": [short] * 40, "batch-6": [short] * 40})
        c = json.loads(layout.SPOT_CHECKS.read_text())
        self.assertEqual(report.release_failures(report.qc_stats("batch-5", c)), ["spot check 40 < 60"])
        self.assertEqual(report.release_failures(report.qc_stats("batch-6", c)), [])

    def test_health(self):
        t = health.thresholds("batch-5")
        self.assertNotIn("media share", t)
        self.assertIn("media share", health.thresholds("batch-4"))
        self.assertEqual(t["$ per approved"], {"max": 0.6})
        self.assertNotIn("giveaway-step drop rate", health.thresholds("batch-4"))
        h = {"giveaway-step drop rate": 0.5, "media share": 0.0, "$ per approved": 0.5}
        self.assertEqual(health.failures("batch-5", h=h), ["giveaway-step drop rate"])
        self.assertEqual(health.failures("batch-4", h=h), ["media share", "$ per approved"])

    def test_rows(self):
        d = self.work / "batch-5"
        self.assertEqual(health.media_first_rows(self.work / "batch-4", [], 3), {"giveaway-step drop rate": None, "mechanical-check rate": None})
        import media_first as mf
        mf.write_jsonl(mf.steps_dir(d) / "giveaway.jsonl", [{"tmp_id": "a"}])
        self.assertEqual(health.media_first_rows(d, [], 3), {"giveaway-step drop rate": 0.25, "mechanical-check rate": None})


if __name__ == "__main__":
    unittest.main()
