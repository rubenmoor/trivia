"""translate.same_numbers: a translation's number check ignores script and format (task 2377); no network."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import translate  # noqa: E402

same = [("42,195 km", "42195公里"), ("42,000", "4.2万"),
        ("3,000,000", "300万"), ("3", "三"), ("1969", "一九六九年"), ("12", "１２"), ("12,500", "12，500"),
        ("21", "二十一"), ("10", "十"), ("30,000", "三万"), ("100,000,000", "1亿"), ("200", "二百"),
        ("1,5 m", "1,5米"), ("1.234", "1.234"), ("10 m²", "10平方米"), ("2 times", "发生了两次"),
        ("1 province", "一个省"), ("3 km", "3千米"),
        # numeral characters in words, no digit in the source
        ("Sichuan", "四川"), ("the Great Wall", "万里长城"), ("Romance of the Three Kingdoms", "三国演义"),
        ("very famous", "十分有名"), ("May Fourth Movement", "五四运动"), ("World War II", "第二次世界大战"),
        ("seven continents", "七大洲"), ("Sichuan has 3 cities", "四川有三个城市"),
        ("Sichuan, 1969", "1969年，四川"), ("1, 2", "1，2"), ("4 cities", "四个城市")]
differ = [("42,000", "4.3万"), ("3", "四"), ("1969", "1970年"), ("7", "统一"), ("3", "三十"),
          ("3 cities", "4个城市"), ("Sichuan", "四川有3个城市"),
          ("3.5 million", "350万"), ("Sichuan has 4 cities", "四川有三个城市"),
          ("1", "统一"), ("1", "一些"), ("1,2", "12"), ("1，2", "12")]  # English million/billion words are not expanded: a fact-check


class Numbers(unittest.TestCase):
    def test_same(self):
        for a, b in same:
            self.assertTrue(translate.same_numbers(a, b), (a, b))
            self.assertTrue(translate.same_numbers(b, a), (b, a))

    def test_differ(self):
        for a, b in differ:
            self.assertFalse(translate.same_numbers(a, b), (a, b))
            self.assertFalse(translate.same_numbers(b, a), (b, a))


if __name__ == "__main__":
    unittest.main()
