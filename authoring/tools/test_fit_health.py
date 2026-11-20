"""Health and `qgen health ack` of fit runs (task 2424). Reuses test_fit_batch's fixture."""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import test_fit_batch as tb  # noqa: E402
import health, qgen  # noqa: E402


class FitHealth(tb.Fixture):
    def setUp(self):
        super().setUp()
        self.acks = self.tmp / "acks.json"
        self.patch(health, "WORK", self.work)
        self.patch(health, "HEALTH_ACKS", self.acks)
        self.patch(qgen.layout, "HEALTH_ACKS", self.acks)
        self.patch(health, "REPORTS", self.tmp)
        self.patch(qgen, "ROOT", self.tmp)
        self.patch(health, "batch_runs", lambda: [])
        self.patch(health.report, "qc_trend", lambda pool: [])
        self.patch(health, "deficit_lines", lambda runs, pool=None: [])
        self.patch(health, "table", lambda runs, pool=None: [])

    def test_listed_health_and_ack(self):
        self.assertEqual(health.fit_runs(), [])
        self.run_batch()
        self.assertEqual(health.fit_runs(), ["fit-1"])
        h = health.fit_health("fit-1")
        self.assertEqual((h["judged"], h["kept"], h["adapted"], h["dropped"], h["adapted approved"]), (4, 2, 1, 1, 1))
        self.assertEqual(h["adapted approved rate"], 1)
        qgen.cmd_health_ack(argparse.Namespace(batch="fit-1", note="looked"))
        self.assertEqual(json.loads(self.acks.read_text())["fit-1"]["note"], "looked")
        self.assertIn("| judged | 4 |", (self.tmp / "batches.md").read_text())
        with self.assertRaises(SystemExit):
            qgen.cmd_health_ack(argparse.Namespace(batch="fit-9", note="x"))
