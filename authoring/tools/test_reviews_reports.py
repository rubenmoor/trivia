"""Pasted player reports (decision 142): zh labels parse, the note is split off."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import reviews  # noqa: E402

ZH = """¡Trivia! #q-0007 · zh-Hans · v1.2 · pool abc123 · 2026-11-20
题目: 长城有多长？
答案: 2万公里
备注: 数字不对"""


class ReportParse(unittest.TestCase):
    def test_zh_report(self):
        [r] = reviews.parse_reports(ZH)
        self.assertEqual((r["question"], r["lang"], r["note"]), ("q-0007", "zh-Hans", "数字不对"))
        self.assertEqual(r["text"].splitlines(), ["题目: 长城有多长？", "答案: 2万公里"])

    def test_feedback_shows_locale(self):
        [r] = reviews.parse_reports(ZH)
        self.assertIn("zh-Hans", reviews.report_feedback(r))
        self.assertIn("长城", reviews.report_feedback(r))


if __name__ == "__main__":
    unittest.main()
