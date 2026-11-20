"""validate.from_base_problems: the base → further base bundle map (plan 230)."""
import json, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import validate  # noqa: E402

QS = [{"subcategory": "a", "status": "approved"}, {"subcategory": "b", "status": "approved", "bundle": "base"},
      {"subcategory": "c", "status": "needs_work"}, {"subcategory": "x", "status": "approved", "bundle": "movies"}]
SUBS = {"base": ["a", "b", "c", "d"], "cb": ["t"]}


class FromBase(unittest.TestCase):
    def check(self, subs):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "m.json"
            f.write_text(json.dumps({"subcategories": subs}))
            return validate.from_base_problems(QS, ["cb"], SUBS, lambda b: f)

    def test_ok(self):
        self.assertEqual(self.check({"a": {"to": "t"}, "b": {"to": None, "reason": "euro_centric", "by": "map"}}), [])

    def test_unmapped_approved_refused(self):
        self.assertIn("'b'", " ".join(self.check({"a": {"to": "t"}})))

    def test_unapproved_need_no_entry(self):
        self.assertEqual(self.check({"a": {"to": "t"}, "b": {"to": "t"}}), [])

    def test_unknown_key(self):
        self.assertIn("'zz' is not a base", " ".join(self.check({"a": {"to": "t"}, "b": {"to": "t"}, "zz": {"to": "t"}})))

    def test_unknown_target(self):
        self.assertIn("'nope' is not a cb", " ".join(self.check({"a": {"to": "nope"}, "b": {"to": "t"}})))

    def test_null_needs_reason(self):
        self.assertIn("reason and by", " ".join(self.check({"a": {"to": None}, "b": {"to": "t"}})))


if __name__ == "__main__":
    unittest.main()
