"""Media-first reports (plan 203): funnel per seed and class, decision 641 count, cost; fixture runs, no network."""
import json, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media_first as mf  # noqa: E402
import report  # noqa: E402


def mq(i, status="approved", seed="s1", cls="general", mtype="audio", excerpt=False, bundle="base"):
    media = {"type": mtype, "role": "essential", **({"excerpt": {"start": 0, "end": 5}} if excerpt else {})}
    return {"id": f"q-{i}", "status": status, "bundle": bundle, "media": media,
            "media_first": {"seed": seed, "class": cls, "kind": "animal", "probe": "p"}}


class Count(unittest.TestCase):
    def test_count(self):
        pool = [mq(1), mq(2, mtype="video", excerpt=True), mq(3, status="needs_work"), mq(4, bundle="t"),
                {"id": "q-5", "status": "approved", "bundle": "base", "media": {"type": "image", "role": "essential"}}]
        m = mf.multimedia_count(pool)
        self.assertEqual((m["count"], m["added"], m["target"], m["total"], m["held"]), (2, 2 - 58, 1058, 3, 1))
        self.assertAlmostEqual(m["share"], 2 / 3)
        self.assertIn("2 approved audio/video", report.media_first_line(pool))
        self.assertIn("1056 to go", report.media_first_line(pool))


class Funnel(unittest.TestCase):
    def test_funnel(self):
        d = Path(tempfile.mkdtemp())
        sd = mf.steps_dir(d)
        tri = lambda t, seed, cls, v: {"title": t, "seed": seed, "class": cls, "verdict": v}
        mf.write_jsonl(sd / "triage.jsonl", [tri("a", "s1", "general", "worth"), tri("b", "s1", "general", "worth"),
                                             tri("c", "s2", "pd-music", "worth"), tri("d", "s2", "pd-music", "not_worth")])
        mf.write_jsonl(sd / "design.jsonl", [{"title": "a", "passed": True}, {"title": "b", "passed": False},
                                             {"title": "c", "passed": True}])
        qs = [mq(1), mq(2, status="needs_work", seed="s2", cls="pd-music", excerpt=True)]
        f = mf.funnel(d, qs)
        keys = mf.FUNNEL
        row = lambda *v: dict(zip(keys, v))
        self.assertEqual(f["seed"]["s1"], row(2, 2, 2, 1, 1, 1, 0))
        self.assertEqual(f["seed"]["s2"], row(2, 1, 1, 1, 1, 0, 1))
        self.assertEqual(f["class"]["pd-music"], f["seed"]["s2"])
        text = "\n".join(mf.funnel_lines(d, qs, 3.0, 1))
        self.assertIn("| s1 | 2 | 2 | 2 | 1 | 1 | 1 | 0 |", text)
        self.assertIn("| total | 4 | 3 | 3 | 2 | 2 | 1 | 1 |", text)
        self.assertIn("$ per approved: $3.00", text)

    def test_empty(self):
        d = Path(tempfile.mkdtemp())
        self.assertEqual(mf.funnel(d, []), {"seed": {}, "class": {}})
        self.assertIn("$ per approved: -", "\n".join(mf.funnel_lines(d, [], 0, 0)))


if __name__ == "__main__":
    unittest.main()
