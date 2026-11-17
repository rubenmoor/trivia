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

    def test_ogg_video_url_query_string(self):
        url = "https://upload.wikimedia.org/x/Lion.ogg?utm_source=commons.wikimedia.org&utm_content=original"
        self.assertEqual(self.checks(self.q(type="video", file_url=url, query="File:Lion"), self.probe()), {"ogg-video"})

    def test_ogg_video(self):
        self.assertEqual(self.checks(self.q(type="video"), self.probe()), {"ogg-video"})

    def test_title_words(self):
        q = self.q(); q["hints"][0] = "it is roaring"
        self.assertEqual(self.checks(q, self.probe()), {"title-words"})
        self.assertFalse(any(x["hard"] for x in mf.media_findings(q, self.probe())))

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


class ResumeRobustness(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.path = self.d / "triage.jsonl"
        p = mock.patch.object(mf, "steps_dir", lambda d: self.d)
        p.start()
        self.addCleanup(p.stop)

    def test_cut_off_last_line_is_ignored_and_dropped(self):
        self.path.write_text('{"title": "a"}\n{"title": "b", "ver')
        self.assertEqual(mf.read_jsonl(self.path), [{"title": "a"}])
        mf.heal_triage(self.d)
        self.assertEqual(self.path.read_text(), '{"title": "a"}\n')

    def test_glued_middle_line_keeps_complete_row(self):
        self.path.write_text('{"title": "a"}\n{"title": "b", "ver{"title": "c"}\n{"title": "d"}\n{"title": "e", "x')
        self.assertEqual([t["title"] for t in mf.read_jsonl(self.path)], ["a", "c", "d"])
        mf.heal_triage(self.d)
        self.assertEqual(self.path.read_text(), '{"title": "a"}\n{"title": "c"}\n{"title": "d"}\n')

    def test_append_after_cut_off_line_starts_new_line(self):
        self.path.write_text('{"title": "a"}\n{"title": "b", "ver')
        mf.append(self.path, {"title": "c"}, mf.threading.Lock())
        self.assertEqual(self.path.read_text(), '{"title": "a"}\n{"title": "b", "ver\n{"title": "c"}\n')
        self.assertEqual([t["title"] for t in mf.read_jsonl(self.path)], ["a", "c"])

    def test_bad_middle_line_fails(self):
        self.path.write_text('{"title": "a"}\n{oops\n{"title": "c"}\n')
        with self.assertRaises(ValueError):
            mf.read_jsonl(self.path)

    def test_disk_full_probe_stops_and_is_not_ledgered(self):
        full = OSError(28, "No space left on device")
        file = {"title": "File:x.ogg", "seed": "s", "class": "general"}
        with mock.patch.object(mf, "probe", side_effect=full), mock.patch.object(mf, "record") as rec:
            with self.assertRaisesRegex(RuntimeError, "free them"):
                mf.probe_or_drop(self.d, "batch-1", file)
        rec.assert_not_called()
        self.assertFalse(self.path.exists())

    def test_other_probe_failure_is_still_dropped(self):
        file = {"title": "File:x.ogg", "seed": "s", "class": "general"}
        with mock.patch.object(mf, "probe", side_effect=ValueError("bad")), mock.patch.object(mf, "record"):
            self.assertIsNone(mf.probe_or_drop(self.d, "batch-1", file))
        self.assertIn("probe failed: bad", self.path.read_text())

    def test_heal_drops_errno_28_rows(self):
        mf.write_jsonl(self.path, [{"title": "a", "why_not": "probe failed: [Errno 28] No space"},
                                   {"title": "b", "why_not": "probe failed: bad"}, {"title": "c"}])
        mf.heal_triage(self.d)
        self.assertEqual([t["title"] for t in mf.read_jsonl(self.path)], ["b", "c"])
