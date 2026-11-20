"""Copies into another bundle (decision 217): the helper, validate's rules, the duplicate exemption."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import copies, qgen, review_steps, validate  # noqa: E402
import translations  # noqa: E402

MEDIA = {"type": "image", "role": "essential", "query": "q", "file_url": "https://x/f.jpg", "credit": "c"}


def q(i, bundle="base", locale="en", **kw):
    return {"id": i, "status": "approved", "bundle": bundle, "locale": locale, "subcategory": "s", "difficulty": 3,
            "question": "Which river runs through Paris?", "answer": "Seine", "wrong_answers": ["a", "b", "c"],
            "hints": ["h1", "h2", "h3"], "description": "d", "fun_fact": "f", "media": dict(MEDIA),
            "background": None, "batch": "batch-9", "review": {"decision": "approved"}, **kw}


def en_entry(src):
    return {"id": src["id"], "question": "EN?", "answer": "Seine", "wrong_answers": ["a", "b", "c"], "hints": ["1", "2", "3"],
            "description": "d", "fun_fact": "f", "difficulty": 4, "status": "approved",
            "source_hash": translations.source_hash(src)}


class Helper(unittest.TestCase):
    def test_en_source(self):
        pool = [q("q-0001")]
        c = copies.copy_question("q-0001", "chinese-base", "geo", pool, "copy-1")
        self.assertEqual((c["id"], c["bundle"], c["locale"], c["copied_from"], c["subcategory"], c["status"]),
                         ("q-0002", "chinese-base", "en", "q-0001", "geo", "needs_work"))
        self.assertEqual((c["media"], c["batch"], c["review"], c["difficulty"]), (MEDIA, "copy-1", None, 3))
        self.assertIsNot(c["media"], pool[0]["media"])
        self.assertEqual(c["question"], pool[0]["question"])

    def test_es_source_with_approved_en(self):
        src = q("q-0001", locale="es", question="¿Qué río?", answer="Sena")
        c = copies.copy_question("q-0001", "chinese-base", "geo", [src], "b", status="draft",
                                 en_translations={"q-0001": en_entry(src)})
        self.assertEqual((c["question"], c["difficulty"], c["locale"], c["status"]), ("EN?", 4, "en", "draft"))

    def test_refusals(self):
        src = q("q-0001", locale="es")
        pool = [src, q("q-0002", "chinese-base", copied_from="q-0009")]
        for args, kw in [(("q-0001",), {}),  # no en translation
                         (("q-0001",), {"en_translations": {"q-0001": {**en_entry(src), "status": "needs_work"}}}),
                         (("q-0001",), {"en_translations": {"q-0001": {**en_entry(src), "source_hash": "old"}}}),
                         (("q-0404",), {}), (("q-0002",), {})]:
            with self.assertRaises(copies.NotCopyable):
                copies.copy_question(*args, "chinese-base", "geo", pool, "b", **kw)
        with self.assertRaises(copies.NotCopyable):  # second copy in the bundle
            copies.copy_question("q-0001", "chinese-base", "geo", [*pool, q("q-0003", "chinese-base", copied_from="q-0001")], "b",
                                 en_translations={"q-0001": en_entry(src)})


class Rules(unittest.TestCase):
    def test_validate(self):
        a = q("q-0001")
        ok = q("q-0002", "chinese-base", copied_from="q-0001")
        self.assertEqual(validate.copy_problems([a, ok]), [])
        self.assertEqual(len(validate.copy_problems([ok])), 1)  # missing source
        self.assertEqual(len(validate.copy_problems([a, ok, q("q-0003", "stem", copied_from="q-0002")])), 1)  # copy of a copy
        self.assertEqual(len(validate.copy_problems([a, ok, q("q-0003", "chinese-base", copied_from="q-0001")])), 1)  # two copies
        self.assertEqual(len(validate.copy_problems([a, q("q-0004", "base", copied_from="q-0001")])), 1)  # same bundle

    def test_duplicates(self):
        a, c = q("q-0001"), q("q-0002", "chinese-base", copied_from="q-0001")
        other = q("q-0003", "chinese-base")
        self.assertIsNone(qgen.duplicates(c, [a]))
        self.assertIsNone(qgen.duplicates(a, [c]))
        self.assertIsNotNone(qgen.duplicates(c, [other]))
        self.assertEqual(qgen.overlap_candidates(c, [a], {}, "en"), [])
        self.assertTrue(qgen.overlap_candidates(c, [other], {}, "en"))
        self.assertEqual(review_steps.related_questions(c, [a], pool_en=[a]), [])
        self.assertEqual(len(review_steps.related_questions(c, [other], pool_en=[other])), 1)


if __name__ == "__main__":
    unittest.main()
