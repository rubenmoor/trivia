"""Pasted player reports (decision 142): zh labels parse, the note is split off, the review lands on the translation."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import reviews  # noqa: E402

ZH = """¡Trivia! #q-0007 · zh-Hans · v1.2 · pool abc123 · 2026-11-20
题目: 长城有多长？
答案: 2万公里
备注: 数字不对"""
ZH_HANT = """¡Trivia! #q-0007 · zh-Hant · v1.2 · pool abc123 · 2026-11-20
題目：長城有多長？
答案：2萬公里
備註：數字不對"""


class ReportParse(unittest.TestCase):
    def test_zh_report(self):
        [r] = reviews.parse_reports(ZH)
        self.assertEqual((r["question"], r["lang"], r["note"]), ("q-0007", "zh-Hans", "数字不对"))
        self.assertEqual(r["text"].splitlines(), ["题目: 长城有多长？", "答案: 2万公里"])

    def test_feedback_shows_locale(self):
        [r] = reviews.parse_reports(ZH)
        self.assertIn("zh-Hans", reviews.report_feedback(r))
        self.assertIn("长城", reviews.report_feedback(r))

    def test_zh_hant_fullwidth_colon(self):
        [r] = reviews.parse_reports(ZH_HANT)
        self.assertEqual((r["lang"], r["note"]), ("zh-Hant", "數字不對"))
        self.assertEqual(r["text"].splitlines(), ["題目：長城有多長？", "答案：2萬公里"])


class ReportLands(unittest.TestCase):
    def test_zh_report_needs_work_on_translation(self):
        for text in (ZH, ZH_HANT):
            [r] = reviews.parse_reports(text)
            src = {"id": "q-0007", "locale": "en", "question": "How long is the Great Wall?"}
            tr = {"id": "q-0007", "question": "长城有多长？"}
            known = {None: {"q-0007": dict(src)}, r["lang"]: {"q-0007": dict(tr)}}
            fb = reviews.report_feedback(r)
            self.assertEqual(reviews.needs_work(r["question"], r["lang"], fb, known, dry_run=True), fb)
            self.assertEqual(known[r["lang"]]["q-0007"]["review"]["feedback"], fb)
            self.assertEqual(known[None]["q-0007"], src)


if __name__ == "__main__":
    unittest.main()
