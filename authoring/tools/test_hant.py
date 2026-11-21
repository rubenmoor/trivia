"""zh-Hant by conversion (decision 762): OpenCC samples, the exceptions list, stale detection, sync."""
import sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import hant, translations, vocab  # noqa: E402


def src(i="q-1", **kw):
    return {"id": i, "status": "approved", "bundle": "chinese-base", "locale": "en", "question": "Q?", "answer": "A",
            "wrong_answers": ["a", "b", "c"], "hints": ["1", "2", "3"], "description": "d", "fun_fact": "f", **kw}


def hans(q, **kw):
    return {"id": q["id"], "question": "视频里的软件", "answer": "出租车", "wrong_answers": ["悉尼", "后来", "头发"],
            "hints": ["h1", "h2", "h3"], "description": "d", "fun_fact": None, "difficulty": 5, "status": "approved",
            "source_hash": translations.source_hash(q), **kw}


class Convert(unittest.TestCase):
    def test_samples(self):
        self.assertEqual(hant.convert_all(["软件", "出租车", "视频", "头发发现", "后来皇后"], {}),
                         ["軟體", "計程車", "影片", "頭髮發現", "後來皇后"])

    def test_exceptions_win(self):
        terms = {"悉尼": "雪梨", "悉尼歌剧院": "雪梨歌劇院"}
        self.assertEqual(hant.convert_all(["悉尼的视频", "悉尼歌剧院"], terms), ["雪梨的影片", "雪梨歌劇院"])
        self.assertEqual(hant.convert_all(["悉尼"], {}), ["悉尼"])  # without the list: unchanged by OpenCC

    def test_shipped_list_fixes_s2twp(self):
        terms = hant.exceptions()
        cases = {"她住在海里": "她住在海裡", "在海里游": "在海裡游",  # 里/裡, and 游 not 遊
                 "是模仿真金币的": "是模仿真金幣的",  # phrase overmatch: 仿真→模擬
                 "印度教历": "印度教曆", "乔治·布尔": "喬治·布爾", "布尔值": "布林值"}
        self.assertNotEqual(hant.convert_all(list(cases), {}), list(cases.values()))  # s2twp alone gets them wrong
        self.assertEqual(hant.convert_all(list(cases), terms), list(cases.values()))

    def test_entry(self):
        q = src()
        t = hant.convert_entries([hans(q)], {"悉尼": "雪梨"})[0]
        self.assertEqual((t["question"], t["answer"], t["wrong_answers"], t["fun_fact"]),
                         ("影片裡的軟體", "計程車", ["雪梨", "後來", "頭髮"], None))
        self.assertEqual((t["status"], t["batch"], t["difficulty"], t["source_hash"]), ("approved", hant.BATCH, 5, hans(q)["source_hash"]))


class Sync(unittest.TestCase):
    def run_sync(self, pool, hs, ts, terms=None):
        with tempfile.TemporaryDirectory() as tmp:
            paths = {l: Path(tmp) / f"{l}.json" for l in translations.LOCALES}
            with mock.patch.object(translations.layout, "translations", paths.get):
                translations.save("zh-Hans", {"questions": hs})
                translations.save("zh-Hant", {"questions": ts})
                out = hant.sync("chinese-base", pool, terms or {})
                return out, translations.load("zh-Hant")["questions"]

    def test_convert_then_current(self):
        q = src()
        (done, gone), ts = self.run_sync([q], [hans(q)], [])
        self.assertEqual((done, gone, len(ts)), (["q-1"], [], 1))
        self.assertEqual(self.run_sync([q], [hans(q)], ts)[0], ([], []))  # up to date: untouched

    def test_stale_zh_hans_text_reconverts(self):
        q = src()
        _, ts = self.run_sync([q], [hans(q)], [])
        (done, _), ts2 = self.run_sync([q], [hans(q, answer="视频")], ts)
        self.assertEqual((done, ts2[0]["answer"]), (["q-1"], "影片"))

    def test_changed_exceptions_reconvert(self):
        q = src()
        _, ts = self.run_sync([q], [hans(q)], [])
        self.assertEqual(self.run_sync([q], [hans(q)], ts, {"悉尼": "雪梨"})[0][0], ["q-1"])

    def test_stale_english_source_withdraws(self):
        q = src()
        _, ts = self.run_sync([q], [hans(q)], [])
        q2 = src(question="Changed?")  # the English source moved on: zh-Hans stale
        (done, gone), ts2 = self.run_sync([q2], [hans(q)], ts)
        self.assertEqual((done, gone, ts2[0]["status"]), ([], ["q-1"], "needs_work"))

    def test_rejected_stays_and_other_bundle_ignored(self):
        q, o = src(), src("q-2", bundle="base")
        rej = {**hant.convert_entries([hans(q)], {})[0], "status": "rejected"}
        (done, gone), _ = self.run_sync([q, o], [hans(q), hans(o)], [rej])
        self.assertEqual((done, gone), ([], []))

    def test_vocab_row_survives_changed_exceptions(self):
        q = src()
        _, ts = self.run_sync([q], [hans(q)], [])
        ts[0]["vocab"] = {"run": "vocab-zh-Hant-1", "verdict": "fix"}
        self.assertEqual(self.run_sync([q], [hans(q)], ts, {"悉尼": "雪梨"})[0], ([], []))


class Vocab(unittest.TestCase):
    old = {"question": "「影片」裡的“軟體”有10個？", "answer": "計程車", "wrong_answers": ["a", "b", "c"], "hints": ["1", "2", "3"],
           "description": "d", "fun_fact": None}

    def new(self, **kw):
        return {**self.old, **kw}

    def test_problems(self):
        ok = self.new(question="「影片」裡的「軟體」有10個？")
        self.assertEqual(vocab.problems(self.old, ok), [])
        self.assertIn("numbers changed", vocab.problems(self.old, self.new(question="影片有11個？")))
        self.assertTrue(vocab.problems(self.old, self.new(hints=["1", "2"])))
        self.assertTrue(vocab.problems(self.old, self.new(fun_fact="x")))
        self.assertTrue(vocab.problems(self.old, self.new(answer="a")))

    def test_pairs(self):
        new = self.new(answer="雪梨")
        pair = lambda a, b: [{"hans": a, "hant": b}]
        self.assertEqual(vocab.good_pairs(new, pair("悉尼", "雪梨"), "悉尼", {}), pair("悉尼", "雪梨"))
        for bad in (pair("悉", "雪"), pair("悉尼", "雪梨")):  # one character; not in the Simplified text
            self.assertEqual(vocab.good_pairs(new, bad, "x", {}), [])
        self.assertEqual(vocab.good_pairs(new, pair("悉尼", "雪梨"), "悉尼", {"悉尼": "西德尼"}), [])  # conflict

    def test_pending_and_apply(self):
        q = src()
        t = hant.convert_entries([hans(q)], {})[0]
        self.assertEqual([x["id"] for x in vocab.pending("chinese-base", [q], [t])], ["q-1"])
        self.assertEqual(vocab.pending("chinese-base", [q], [{**t, "vocab": {"run": "r"}}]), [])
        with tempfile.TemporaryDirectory() as tmp:
            paths = {l: Path(tmp) / f"{l}.json" for l in translations.LOCALES}
            with mock.patch.object(translations.layout, "translations", paths.get):
                translations.save("zh-Hant", {"questions": [t, {**t, "id": "q-2"}]})
                text = {k: t[k] for k in translations.TEXT_FIELDS} | {"answer": "的士"}
                done = vocab.apply({"q-1": {"verdict": "fix", "text": text, "note": "", "pairs": []},
                                    "q-2": {"verdict": "flag", "text": None, "note": "status wording", "pairs": []}}, "vocab-zh-Hant-1", "opus")
                a, b = translations.load("zh-Hant")["questions"]
                self.assertEqual((a["answer"], a["status"], a["vocab"]["verdict"]), ("的士", "approved", "fix"))
                self.assertEqual((b["status"], b["review"]["feedback"], b["vocab"]["verdict"]), ("needs_work", "vocabulary pass: status wording", "flag"))
                self.assertEqual(done["q-1"]["before"]["answer"], "計程車")
                self.assertEqual(vocab.apply({"q-1": {"verdict": "ok", "text": None, "note": "", "pairs": []}}, "r", "opus"), {})  # read once


if __name__ == "__main__":
    unittest.main()
