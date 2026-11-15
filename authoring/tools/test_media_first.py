"""media_first's inventory, ledger and seed skips (plan 203); no network, no claude."""
import sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media_first as mf  # noqa: E402


def f(seed, i):
    return {"title": f"File:{seed}-{i}.ogg", "seed": seed}


def row(seed, i, worth):
    return {"title": f"File:{seed}-{i}.ogg", "seed": seed, "worth": worth}


class Inventory(unittest.TestCase):
    def test_drops_used_pool_and_orders_by_yield(self):
        files = [f("a", i) for i in range(3)] + [f("b", i) for i in range(3)] + [f("c", 0)]
        rows = [row("a", 0, False), row("b", 0, True)]
        q = mf.inventory(files, rows, {"b-1.ogg"})
        self.assertEqual([x["title"] for x in q], ["File:b-2.ogg", "File:c-0.ogg", "File:a-1.ogg", "File:a-2.ogg"])

    def test_skips(self):
        files = [f("dead", i) for i in range(20)] + [f("q:audio:church bells", 0), f("ok", 0)]
        rows = [row("dead", i, False) for i in range(15)]
        self.assertEqual([x["seed"] for x in mf.inventory(files, rows, set())], ["ok"])
        # a worth-it file lifts a zero-yield seed's skip
        rows = [row("q:audio:church bells", 9, True)]
        self.assertIn("q:audio:church bells", {x["seed"] for x in mf.inventory(files, rows, set())})

    def test_cap_per_seed_and_limit(self):
        files = [f("a", i) for i in range(50)]
        self.assertEqual(len(mf.inventory(files, [], set())), mf.MAX_PER_SEED)
        self.assertEqual(len(mf.inventory(files, [], set(), limit=5)), 5)


class Ledger(unittest.TestCase):
    def setUp(self):
        d = Path(tempfile.mkdtemp())
        self.run = d / "batch-1"
        self.run.mkdir()
        patches = [mock.patch.object(mf, "LEDGER", d / "ml" / "files.jsonl"),
                   mock.patch.object(mf, "SURVEY_FILES", d / "survey.jsonl"),
                   mock.patch.object(mf, "pilot_rows", lambda: [row("a", 0, True)]),
                   mock.patch.object(mf.media_survey, "pool_media", lambda: set())]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        mf.write_jsonl(mf.SURVEY_FILES, [f("a", i) for i in range(4)])

    def test_record_never_twice(self):
        self.assertEqual(mf.record("batch-1", [row("a", 1, True), row("a", 2, False)]), 2)
        self.assertEqual(mf.record("batch-2", [row("a", 2, True), row("a", 3, False)]), 1)
        self.assertEqual([r["run"] for r in mf.ledger()], ["batch-1", "batch-1", "batch-2"])

    def test_select_is_fixed_and_remaining_shrinks(self):
        first = [x["title"] for x in mf.select(self.run, limit=2)]
        self.assertEqual(first, ["File:a-1.ogg", "File:a-2.ogg"])  # the pilot's a-0 is used
        mf.record("batch-1", [row("a", 1, True)])  # a changed ledger doesn't change the queue
        self.assertEqual([x["title"] for x in mf.select(self.run)], first)
        self.assertEqual([x["title"] for x in mf.remaining(self.run, "batch-1")], ["File:a-2.ogg"])

    def test_remaining_drops_a_seed_skipped_meanwhile(self):
        mf.select(self.run)
        mf.record("batch-1", [])
        self.assertEqual(len(mf.remaining(self.run, "batch-1")), 3)
        with mock.patch.object(mf, "SKIP_AFTER", 1), mock.patch.object(mf, "pilot_rows", lambda: [row("a", 0, False)]):
            self.assertEqual(mf.remaining(self.run, "batch-1"), [])


if __name__ == "__main__":
    unittest.main()


class MediaFindings(unittest.TestCase):
    """The mechanical media checks (plan 204); no network."""

    def probe(self, text="", ocr="", **kw):
        d = Path(tempfile.mkdtemp())
        (d / "ocr.txt").write_text(ocr)
        return {"dir": str(d), "has_audio": True, "integrated_lufs": -20.0, "silence_share": 0.05,
                "speech": {"text": text}, **kw}

    def q(self, cls="general", **media):
        m = {"type": "audio", "query": "File:Lion roaring.ogg", "license": "CC BY-SA 4.0", **media}
        return {"question": "Listen: which animal is this?", "answer": "Lion", "wrong_answers": ["Wolf", "Bear", "Owl"],
                "hints": ["big cat", "savanna", "pride"], "description": "A sound", "concept": "lion",
                "media": m, "media_first": {"seed": "s", "class": cls, "kind": "animal", "probe": "x"}}

    def checks(self, q, p):
        return {f["check"] for f in mf.media_findings(q, p)}

    def test_clean(self):
        self.assertEqual(mf.media_findings(self.q(), self.probe()), [])

    def test_title_words(self):
        q = self.q(); q["hints"][0] = "it is roaring"
        self.assertEqual(self.checks(q, self.probe()), {"title-words"})

    def test_answer_heard_and_ocr(self):
        self.assertEqual(self.checks(self.q(), self.probe(text="a lion")), {"answer-heard"})
        self.assertEqual(self.checks(self.q(), self.probe(ocr="01: LION")), {"answer-heard"})

    def test_licence(self):
        self.assertEqual(self.checks(self.q(license="CC BY-NC 4.0"), self.probe()), {"licence"})

    def test_work(self):
        ok = {"title": "Eroica", "creator": "Beethoven", "year": 1804, "basis": "composer died 1827"}
        self.assertEqual(mf.media_findings(self.q("pd-music", work=ok), self.probe()), [])
        self.assertEqual(self.checks(self.q("pd-music"), self.probe()), {"work"})
        bad = {**ok, "basis": "I think it's old"}
        self.assertEqual(self.checks(self.q("pd-music", work=bad), self.probe()), {"work-basis"})
        modern = {**ok, "basis": "composer died 1990"}
        self.assertIsNone(mf.work_basis(modern, 2026))
        self.assertEqual(mf.work_basis({"year": 1902, "basis": "film of 1902"}), "pre-1930-film")
        self.assertEqual(mf.work_basis({"year": 1950, "basis": "film of 1950"}), None)
        self.assertEqual(mf.work_basis({"basis": "US government work"}), "government-work")
        self.assertEqual(mf.work_basis({"basis": "traditional"}), "traditional")
        self.assertEqual(self.checks(self.q("general", work=None), self.probe()), set())

    def test_quiet_and_silent_are_soft(self):
        f = mf.media_findings(self.q(), self.probe(integrated_lufs=-40.0, silence_share=0.7))
        self.assertEqual({x["check"] for x in f}, {"quiet", "silent"})
        self.assertFalse(any(x["hard"] for x in f))
        self.assertEqual(mf.media_findings(self.q(), self.probe(integrated_lufs=-31.0)), [])
