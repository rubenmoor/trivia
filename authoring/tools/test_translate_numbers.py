"""translate.numbers: a translation's number check ignores script and format (task 2377); no network."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import translate  # noqa: E402

same = [("42,195 km", "42195公里"), ("42,000", "4.2万"),
        ("3,000,000", "300万"), ("3", "三"), ("1969", "一九六九年"), ("12", "１２"), ("12,500", "12，500"),
        ("21", "二十一"), ("10", "十"), ("30,000", "三万"), ("100,000,000", "1亿"), ("200", "二百"),
        ("1,5 m", "1,5米"), ("1.234", "1.234")]
differ = [("42,000", "4.3万"), ("3", "四"), ("1969", "1970年"), ("7", "统一")]


class Numbers(unittest.TestCase):
    def test_same(self):
        for a, b in same:
            self.assertEqual(translate.numbers(a), translate.numbers(b), (a, b))

    def test_differ(self):
        for a, b in differ:
            self.assertNotEqual(translate.numbers(a), translate.numbers(b), (a, b))

    def test_lone_one(self):
        self.assertEqual(translate.numbers("统一些"), [])


if __name__ == "__main__":
    unittest.main()
