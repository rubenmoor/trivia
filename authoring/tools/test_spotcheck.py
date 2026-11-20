"""qgen spotcheck: import checks (hash, unknown id), control planting and scoring, verdict → review (plan 141)."""
import random, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import spotcheck  # noqa: E402

ITEM = {"id": "q-1", "subcategory": "x", "difficulty": 3, "en": {}, "media": None,
        "tr": {"question": "Wie viele Beine hat eine Spinne, 8?", "answer": "Acht", "wrong_answers": ["Sechs", "Zehn", "Vier"],
               "hints": [], "description": None, "fun_fact": None}}


def doc(**kw):
    ids = ["q-1", "q-2", "control-1"]
    d = {"sheet": "s", "hash": spotcheck.sheet_hash("s", ids), "locale": "de", "ids": ids,
         "verdicts": {"q-1": {"decision": "approve"}, "control-1": {"decision": "needs_work"}}}
    return {**d, **kw}


class Checks(unittest.TestCase):
    def test_good(self):
        self.assertEqual(spotcheck.check_verdicts(doc(), None, {"q-1", "q-2"}), [])

    def test_wrong_hash(self):
        self.assertTrue(any("hash" in e for e in spotcheck.check_verdicts(doc(hash="000000000000"), None, {"q-1", "q-2"})))

    def test_unknown_id(self):
        d = doc()
        d["verdicts"]["q-9"] = {"decision": "approve"}
        errs = spotcheck.check_verdicts(d, None, {"q-1", "q-2"})
        self.assertTrue(any("q-9" in e for e in errs))
        d = doc()
        d["verdicts"]["q-2"] = {"decision": "reject"}
        self.assertTrue(any("q-2" in e for e in spotcheck.check_verdicts(d, None, {"q-1"})))

    def test_manifest_mismatch(self):
        m = {"name": "s", "hash": "other", "ids": ["q-1"]}
        self.assertTrue(spotcheck.check_verdicts(doc(), m, {"q-1", "q-2"}))

    def test_bad_decision_and_problem(self):
        d = doc()
        d["verdicts"]["q-1"] = {"decision": "yes", "problems": ["nope"]}
        self.assertEqual(len(spotcheck.check_verdicts(d, None, {"q-1", "q-2"})), 2)


class Controls(unittest.TestCase):
    def test_scoring(self):
        v = {"control-1": {"decision": "approve"}, "control-2": {"decision": "reject"}, "q-1": {"decision": "approve"}}
        self.assertEqual(spotcheck.score_controls(["control-1", "control-2", "q-1"], v), (1, 2))

    def test_undecided_control_not_caught(self):
        ids = ["control-1", "control-2", "control-3", "q-1"]
        self.assertEqual(spotcheck.score_controls(ids, {"control-1": {"decision": "reject"}}), (1, 3))

    def test_make_control_differs_and_keeps_shape(self):
        for seed in range(20):
            c, kind = spotcheck.make_control(ITEM, random.Random(seed))
            self.assertNotEqual(c["tr"], ITEM["tr"], kind)
            self.assertEqual(len(c["tr"]["wrong_answers"]), 3)
        self.assertEqual(ITEM["tr"]["answer"], "Acht")  # the original is untouched

    def test_build_items_plants_ids(self):
        picked = [({"id": f"q-{i}", "difficulty": 1, **ITEM["tr"]}, {"subcategory": "x", "locale": "en", **ITEM["tr"]}) for i in range(5)]
        items, planted = spotcheck.build_items("s", picked, 3)
        self.assertEqual(sorted(planted), ["control-1", "control-2", "control-3"])
        self.assertEqual(len(items), 8)


class Review(unittest.TestCase):
    def test_review_of(self):
        r = spotcheck.review_of({"decision": "needs_work", "feedback": "stiff", "corrected": "Besser", "problems": ["style"]})
        self.assertEqual((r["decision"], r["by"], r["problems"]), ("needs_work", "native", ["style"]))
        self.assertIn("Native correction: Besser", r["feedback"])
        self.assertEqual(spotcheck.review_of({"decision": "no_travel"})["decision"], "rejected")
        self.assertTrue(spotcheck.review_of({"decision": "needs_work"})["feedback"])


if __name__ == "__main__":
    unittest.main()
