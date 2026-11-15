"""media_first's triage, design and giveaway steps (plan 203) with a stub claude and stub probes; no network."""
import json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order: the command modules import each other)
import categories  # noqa: E402
import layout  # noqa: E402
import media_first as mf  # noqa: E402

CAT = categories.load("base")[0]
SUB = CAT["subcategories"][0]
SAID = {"File:lion.ogg": "listen a lion roars", "File:long.ogg": ""}


def survey_file(name, cls="general", duration=20):
    return {"title": f"File:{name}.ogg", "seed": "s", "class": cls, "type": "audio", "description": name,
            "duration": duration, "width": 0, "height": 0, "page_url": f"https://c/{name}", "file_url": f"https://u/{name}",
            "license": "CC0", "license_url": None, "author": "A", "restrictions": [], "base_categories": [CAT["slug"]]}


def triage_out(subject, verdict="worth"):
    return {"verdict": verdict, "subject": subject, "matches_title": True, "subcategory": SUB, "difficulty": 2,
            "kind": "animal", "excerpt": None, "why_not": None, "duplicate_of": None, "quality": "ok"}


def design_out(answer, excerpt=None, work=None, passes=True):
    return {"question": "Listen: which animal is this?", "answer": answer, "wrong_answers": ["Wolf", "Bear", "Owl"],
            "hints": ["a", "b", "c"], "description": "A sound", "fun_fact": "f", "difficulty": 3, "subcategory": SUB,
            "role": "essential", "excerpt": excerpt, "media_note": "the roar", "background_query": "savanna",
            "work": work, "needs_fact_check": False,
            "giveaway": {"spoken": False, "on_screen_text": False, "title_needed": False, "description": False,
                         "passes": passes, "notes": ""}}


class Steps(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp())
        self.run = self.work / "batch-1"
        self.run.mkdir()
        pool = self.work / "questions.json"
        pool.write_text(json.dumps({"questions": [
            {"id": "q-0001", "status": "approved", "bundle": "base", "locale": "en", "subcategory": SUB,
             "answer": "Rooster", "concept": None, "question": "?", "difficulty": 3}]}))
        self.calls = []
        for p in [mock.patch.object(layout, "WORK", self.work), mock.patch.object(mf, "LEDGER", self.work / "ledger.jsonl"),
                  mock.patch.object(mf, "pilot_rows", lambda: []), mock.patch.object(qgen, "POOL", pool),
                  mock.patch.object(mf, "gaps", lambda pool: {"difficulty_gaps": {}, "need": [SUB]}),
                  mock.patch.object(mf, "probe", self.probe), mock.patch.object(qgen, "claude", self.claude)]:
            p.start()
            self.addCleanup(p.stop)

    def probe(self, title, excerpt=None):
        d = self.work / "media-probe" / (title[5:-4] + ("-x" if excerpt else ""))
        d.mkdir(parents=True, exist_ok=True)
        (d / "ocr.txt").write_text("")
        dur = 300 if "long" in title else 20
        info = {"duration": dur, "has_audio": True, "speech": {"text": "" if excerpt else SAID.get(title, "")}}
        (d / "probe.json").write_text(json.dumps(info))
        return info | {"dir": str(d)}

    def claude(self, system, user, schema, model, cwd, read=False, **kw):
        u = json.loads(user)
        self.calls.append((model, u))
        return self.answers[u["file"]["title"]].pop(0)

    def queue(self, *files):
        mf.write_jsonl(self.run / mf.QUEUE, list(files))

    def test_schemas(self):
        for s in (mf.triage_schema(), mf.design_schema()):
            self.assertEqual(set(s["required"]), set(s["properties"]))
            self.assertIn(SUB, s["properties"]["subcategory"]["enum"])
        self.assertEqual(mf.triage_schema()["properties"]["difficulty"]["maximum"], mf.BANDS)

    def test_duplicate_subject(self):
        self.queue(survey_file("rooster"), survey_file("lion"), survey_file("lion2"), survey_file("mud"))
        self.answers = {"File:rooster.ogg": [triage_out("Rooster crowing")], "File:lion.ogg": [triage_out("Lion")],
                        "File:lion2.ogg": [triage_out("Lions roaring")], "File:mud.ogg": [triage_out("x", "not_worth")]}
        self.assertEqual(mf.triage(self.run, "batch-1", jobs=1, target=None), [])
        got = {t["title"]: (t["verdict"], t["duplicate_of"]) for t in mf.triaged(self.run)}
        self.assertEqual(got, {"File:rooster.ogg": ("duplicate", "Rooster"), "File:lion.ogg": ("worth", None),
                               "File:lion2.ogg": ("duplicate", "Lion"), "File:mud.ogg": ("not_worth", None)})
        self.assertIn("Rooster", self.calls[0][1]["base_subjects"][SUB])
        self.assertEqual(self.calls[2][1]["run_subjects"], ["Lion"])
        self.assertEqual({r["title"]: r["worth"] for r in mf.ledger()}["File:lion.ogg"], True)
        self.assertEqual(self.calls[0][0], "sonnet")
        # rerun: nothing left, no calls
        mf.triage(self.run, "batch-1", jobs=1, target=None)
        self.assertEqual(len(self.calls), 4)

    def test_target_stops_triage(self):
        self.queue(*(survey_file(f"f{i}") for i in range(6)))
        self.answers = {f"File:f{i}.ogg": [triage_out(f"Subject{i}")] for i in range(6)}
        mf.triage(self.run, "batch-1", jobs=1, target=1)
        self.assertEqual(len(mf.triaged(self.run)), 2)  # one round: max(jobs, 2 × need)

    def triage_done(self, *rows):
        mf.write_jsonl(mf.steps_dir(self.run) / "triage.jsonl",
                       [{"title": f["title"], "seed": "s", "class": f["class"], "category": CAT["slug"], **triage_out(s)}
                        for f, s in rows])

    def test_giveaway_retry_then_pass(self):
        lion = survey_file("lion")
        self.queue(lion)
        self.triage_done((lion, "Lion"))
        self.answers = {"File:lion.ogg": [design_out("Lion"), design_out("Lion", {"start": 0, "end": 8})]}
        self.assertEqual(mf.design(self.run, jobs=1), [])
        second = self.calls[1][1]
        self.assertIn("giveaway", " ".join(second["previous_attempt"]["problems"]))
        self.assertEqual(self.calls[0][0], "opus")
        q = qgen.load_json(self.run / "drafts" / f"{mf.tmp_id('File:lion.ogg')}.json")["questions"][0]
        self.assertEqual(q["media"]["excerpt"], {"start": 0, "end": 8})  # a window without the spoken name
        self.assertEqual((q["media"]["type"], q["media"]["role"], q["media"]["source_url"]), ("audio", "essential", "https://c/lion"))
        self.assertEqual(q["media_first"], {"seed": "s", "class": "general", "kind": "animal", "probe": "media-probe/lion-x"})
        self.assertEqual(q["background_query"], "savanna")
        self.assertEqual(mf.giveaway(q), [])  # after fix: from the stored window probe
        self.assertEqual(mf.giveaway(q, self.probe("File:lion.ogg")), ["lion"])

    def test_giveaway_twice_dropped(self):
        lion = survey_file("lion")
        self.queue(lion)
        self.triage_done((lion, "Lion"))
        self.answers = {"File:lion.ogg": [design_out("Lion"), design_out("Lion")]}
        mf.design(self.run, jobs=1)
        self.assertEqual([r["passed"] for r in mf.designed(self.run)], [False])
        self.assertFalse((self.run / "drafts").exists())
        mf.design(self.run, jobs=1)  # resume: designed files aren't asked again
        self.assertEqual(len(self.calls), 2)

    def test_long_file_needs_excerpt(self):
        f = survey_file("long", duration=300)
        self.queue(f)
        self.triage_done((f, "Owl"))
        self.answers = {"File:long.ogg": [design_out("Tawny owl"), design_out("Tawny owl", {"start": 10, "end": 40})]}
        mf.design(self.run, jobs=1)
        self.assertIn("excerpt", self.calls[1][1]["previous_attempt"]["problems"][0])
        q = qgen.load_json(self.run / "drafts" / f"{mf.tmp_id(f['title'])}.json")["questions"][0]
        self.assertEqual((q["media"]["excerpt"], q["media"]["duration"]), ({"start": 10, "end": 40}, 300))
        self.assertEqual(q["media_first"]["probe"], "media-probe/long-x")  # the window's probe

    def test_pd_work_required(self):
        f = survey_file("ode", "pd-music")
        self.queue(f)
        self.triage_done((f, "Ode to Joy"))
        work = {"title": "Symphony No. 9", "creator": "Beethoven", "year": 1824, "basis": "composer died 1827"}
        self.answers = {"File:ode.ogg": [design_out("Beethoven"), design_out("Beethoven", work=work)]}
        mf.design(self.run, jobs=1)
        self.assertTrue(any("media.work" in p for p in self.calls[1][1]["previous_attempt"]["problems"]))
        q = qgen.load_json(self.run / "drafts" / f"{mf.tmp_id(f['title'])}.json")["questions"][0]
        self.assertEqual(q["media"]["work"], work)

    def test_known_subject(self):
        self.assertEqual(mf.known_subject("Rooster crowing", ["Cat", "Rooster"]), "Rooster")
        self.assertIsNone(mf.known_subject("Thunderstorm", ["Thunder"]))
        self.assertEqual(mf.known_subject("cats meowing", ["Cat"]), "Cat")


if __name__ == "__main__":
    unittest.main()
