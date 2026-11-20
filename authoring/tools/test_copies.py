"""Copies into another bundle (decision 217): the helper, validate's rules, the duplicate exemption."""
import json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

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

    def test_translation_entry(self):
        src = q("q-0001", locale="es")
        with tempfile.TemporaryDirectory() as d, \
                mock.patch.object(validate.layout, "translations", lambda l: Path(d) / f"questions.{l}.json"), \
                mock.patch.object(validate, "ROOT", Path(d)), \
                mock.patch.object(validate, "names_problems", lambda data: []), \
                mock.patch.object(validate, "names_warnings", lambda data: []):
            def errors(entry):
                (Path(d) / "questions.en.json").write_text(json.dumps({"version": 1, "locale": "en", "questions": [entry]}))
                return [e for e in validate.translation_problems({"questions": [src]})[0] if "copied_from" in e]
            self.assertEqual(errors(en_entry(src)), [])
            self.assertEqual(len(errors({**en_entry(src), "copied_from": "q-0009"})), 1)

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



class FixedMedia(unittest.TestCase):
    def test_helper(self):
        self.assertTrue(copies.media_fixed(q("q-1", copied_from="q-0")))
        self.assertTrue(copies.media_fixed(q("q-1", media_first={"probe": "p"})))
        self.assertFalse(copies.media_fixed(q("q-1")))

    def test_kept_slots(self):
        self.assertEqual(review_steps.kept_slots("batch-1", q("q-2", copied_from="q-1")), {"media"})
        self.assertEqual(review_steps.kept_slots("batch-1", q("q-2")), set())

    def test_revise_keeps_copy_media(self):
        c = q("q-2", copied_from="q-1")
        new = {k: c[k] for k in qgen.QUESTION_FIELDS} | {"needs_media": True, "background_query": None,
               "media": {**c["media"], "type": "audio", "query": "other", "note": None}}
        before = dict(c["media"])
        qgen.revise_in_pool(c, new, "r", "2026-11-20")
        self.assertEqual(c["media"], before)


    def test_merge_keeps_copy_media(self):
        work = Path(tempfile.mkdtemp())
        pool, d = work / "questions.json", work / "batch-1"
        pool.write_text(json.dumps({"questions": [q("q-0001", answer="Rhine")]}))
        (d / "drafts").mkdir(parents=True)
        (d / "ratings").mkdir()
        (d / "run.json").write_text(json.dumps({"bundle": "chinese-base", "draft_locale": "en"}))
        draft = {**{k: v for k, v in q("x").items() if k not in ("id", "status", "review", "batch", "locale")},
                 "tmp_id": "c-1", "copied_from": "q-0001", "needs_media": True, "needs_fact_check": False,
                 "bundle": "chinese-base", "question": "Which river runs through Vienna?", "answer": "Danube"}
        (d / "drafts" / "c-1.json").write_text(json.dumps({"questions": [draft], "skipped": []}))
        (d / "ratings" / "c-1.json").write_text(json.dumps(
            {"c-1": {**{k: 5 for k in qgen.RUBRIC}, "difficulty_estimate": 3, "notes": ""}}))
        with mock.patch.object(qgen, "WORK", work), mock.patch.object(qgen, "POOL", pool), \
                mock.patch.object(qgen, "ROOT", work):
            qgen.cmd_merge(mock.Mock(run="batch-1"))
        new = json.loads(pool.read_text())["questions"][-1]
        self.assertEqual((new["id"], new["media"]), ("q-0002", MEDIA))

    def test_apply_to_drafts_keeps_copy_media(self):
        d = Path(tempfile.mkdtemp())
        (d / "drafts").mkdir()
        draft = {**q("x"), "tmp_id": "c-1", "copied_from": "q-0001", "needs_media": True, "needs_fact_check": False}
        (d / "drafts" / "c-1.json").write_text(json.dumps({"questions": [draft], "skipped": []}))
        new = {k: draft[k] for k in qgen.QUESTION_FIELDS} | {"needs_media": True, "background_query": None,
               "media": {**MEDIA, "type": "audio", "query": "other", "note": None, "file_url": None}}
        qgen.apply_to_drafts(d, {"c-1": {"action": "revise", "question": new, "reason": "r"}}, set())
        (moved,), = [json.loads(f.read_text())["questions"] for f in (d / "drafts").glob("revised-*.json")]
        self.assertEqual(moved["media"], MEDIA)


class ReviewServer(unittest.TestCase):
    """The review page can't pick or search a fixed `media` slot (a copy's, a media-first file)."""
    def setUp(self):
        sys.path.insert(0, str(Path(__file__).parent.parent / "server"))
        import main as server  # noqa: E402
        self.server = server
        self.pool = [q("q-0002", copied_from="q-0001", background={"query": "b"}),
                     q("q-0003", media_first={"probe": "p"}), q("q-0004")]
        self.fetched = []
        for name, value in [("load_pool", lambda: {"questions": self.pool}),
                            ("update_question", lambda qid, fn: fn(server.find_question(qid)) or server.find_question(qid))]:
            p = mock.patch.object(server, name, value)
            p.start()
            self.addCleanup(p.stop)
        for name, value in [("load_candidates", lambda qid, slot: self.fail("candidates read")),
                            ("fetch_for", lambda q, slot, every=False: self.fetched.append((q["id"], slot)))]:
            p = mock.patch.object(server.media, name, value)
            p.start()
            self.addCleanup(p.stop)

    def test_refused(self):
        for qid in ("q-0002", "q-0003"):
            with self.assertRaises(ValueError):
                self.server.pick_media(qid, 0, "media")
            with self.assertRaises(ValueError):
                self.server.search_media(qid, "new", "media")
        self.assertEqual([x["media"] for x in self.pool[:2]], [MEDIA, MEDIA])
        self.assertEqual(self.fetched, [])

    def test_others_searchable(self):
        self.server.search_media("q-0002", "new", "background")
        self.server.search_media("q-0004", "new", "media")
        self.assertEqual(self.fetched, [("q-0002", "background"), ("q-0004", "media")])
        self.assertEqual(self.pool[2]["media"]["query"], "new")


if __name__ == "__main__":
    unittest.main()
