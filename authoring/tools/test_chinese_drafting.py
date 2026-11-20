"""Drafting readiness for chinese-base (plan 232): pick, gaps, concept seeding, overlap, the pilot size, scope and rule
in the prompts. Fixture pool with base, chinese-base copies (a reused subcategory) and new subcategories; the real
chinese-base taxonomy, scopes and related.json; stubbed claude, no network."""
import argparse, contextlib, io, json, math, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order: the command modules import each other)
import batches, categories, concepts, layout, review_steps, targets, translate, translations  # noqa: E402

B = "chinese-base"
REUSED, NEW, NEIGHBOUR, LANG = "vegetables", "spring-festival", "chinese-zodiac", "chinese-characters"
MEDIA = {"type": "image", "role": "decorative", "query": "q", "source_url": None, "file_url": None, "credit": None}
AXES = {"move": "identify", "stimulus": "none", "clue": "direct", "answer_kind": "thing", "lens": "school"}
FIT = {"move": {"identify": 5}, "stimulus": {"none": 5}, "lens": {"school": 5}}


def q(i, bundle="base", sub=REUSED, answer="Carrot", question=None, **kw):
    return {"id": i, "status": "approved", "bundle": bundle, "locale": "en", "subcategory": sub, "difficulty": 4,
            "description": "d", "question": question or f"Which vegetable is {answer}?", "answer": answer,
            "wrong_answers": ["a", "b", "c"], "hints": ["h1", "h2", "h3"], "fun_fact": "f", "media": dict(MEDIA),
            "background": None, "batch": "batch-9", "concept": None, "axes": None,
            "review": {"decision": "approved", "feedback": None, "problems": [], "reviewed_on": "2026-11-01", "reviewer": "human"},
            **kw}


POOL = [q("q-0001", concept="Carrot", axes=AXES, question="Which orange root is rich in vitamin A?"),
        q("q-0002", bundle=B, copied_from="q-0001", question="Which orange root is rich in vitamin A?"),
        q("q-0003", answer="Potato", concept="Potato", axes=AXES),
        q("q-0004", bundle=B, answer="Potato", copied_from="q-0003"),
        q("q-0005", sub="dogs", answer="Year of the Dog", question="Which zodiac animal is loyal?", concept="Dog", axes=AXES),
        q("q-0006", bundle=B, sub=NEIGHBOUR, answer="Year of the Dog", question="Which zodiac animal is loyal?",
          copied_from="q-0005")]


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.work, self.pool, self.sources = self.tmp / "work", self.tmp / "questions.json", self.tmp / "bundles"
        self.work.mkdir()
        self.pool.write_text(json.dumps({"questions": POOL}))
        for obj in (layout, qgen, review_steps, translate, batches):
            self.patch(obj, "WORK", self.work)
        for obj in (qgen, review_steps, translate):
            self.patch(obj, "POOL", self.pool)
        real = layout.BUNDLE_SOURCES / B
        for f in ("related.json", "scopes.json"):
            (self.sources / B).mkdir(parents=True, exist_ok=True)
            (self.sources / B / f).write_text((real / f).read_text(encoding="utf-8"), encoding="utf-8")
        self.patch(layout, "BUNDLE_SOURCES", self.sources)
        self.patch(concepts, "BUNDLE_SOURCES", self.sources)
        self.patch(concepts, "CONCEPTS", self.tmp / "concepts")
        concepts.save("base", REUSED, {"subcategory": REUSED, "facets": ["Roots"], "axis_fit": FIT, "concepts": [
            {"name": "Carrot", "facet": "Roots", "known_at": 3}, {"name": "Potato", "facet": "Roots", "known_at": 2}]})
        self.patch(translations, "load", lambda locale: {"questions": []})
        self.patch(translations, "yield_rate", lambda locale: 0.5)
        self.calls = []
        self.patch(qgen, "claude", self.claude)

    def patch(self, obj, name, value):
        p = mock.patch.object(obj, name, value)
        p.start()
        self.addCleanup(p.stop)

    def claude(self, system, user, schema, model, cwd, **kw):
        self.calls.append((system, user))
        if "facets" in schema["required"]:
            return {"facets": ["Customs"], "axis_fit": FIT}
        if "existing" in schema["required"]:
            ids = [e["id"] for e in json.loads(user.split("## Existing questions\n", 1)[1].split("\n\n", 1)[0] or "[]")] \
                if "## Existing questions\nnone" not in user else []
            return {"concepts": [{"name": f"Custom {i}", "facet": "Customs", "known_at": 4} for i in range(6)],
                    "existing": [{"id": i, "concept": "Custom 0", "axes": AXES} for i in ids]}
        return {"questions": [], "skipped": []}

    def data(self):
        return json.loads(self.pool.read_text())["questions"]

    def save(self, qs):
        self.pool.write_text(json.dumps({"questions": qs}))


class Pick(Fixture):
    def test_draft_locale_en(self):
        self.assertEqual(translations.draft_locale(qgen.bundle_row(B)), "en")

    def test_pilot_while_only_copies(self):
        pool = self.data()
        self.assertTrue(batches.pilot(pool, B))
        self.assertFalse(batches.pilot(pool, "base"))
        subs = batches.subcategories(pool, bundle=B)
        self.assertEqual(len(subs), batches.PILOT_SUBCATEGORIES)
        self.assertNotIn(REUSED, subs)  # its copies count as approved
        cats = {s: c["slug"] for c in categories.load(B) for s in c["subcategories"]}
        self.assertEqual(len({cats[s] for s in subs}), min(len(subs), len(categories.load(B))))  # spread: one per category first

    def test_full_run_after_a_drafted_source(self):
        pool = self.data() + [q("q-0007", bundle=B, sub=NEW, answer="Red packet", batch="batch-500")]
        self.assertFalse(batches.pilot(pool, B))
        order = categories.subcategories(B)
        subs = batches.subcategories(pool, bundle=B)
        self.assertEqual(len(subs), math.ceil(len(order) * batches.SHARE))
        self.assertTrue({REUSED, NEW, NEIGHBOUR}.isdisjoint(subs))  # each has an approved question
        self.assertEqual(subs, [s for s in order if s not in {REUSED, NEW, NEIGHBOUR}][:len(subs)])  # ties: file order (D-46)

    def test_base_pick_unchanged(self):
        base = batches.subcategories(self.data(), bundle="base")
        order = categories.subcategories("base")
        self.assertEqual(len(base), math.ceil(len(order) * batches.SHARE))  # D-46, no pilot
        self.assertEqual(base, [s for s in order if s not in {"vegetables", "dogs"}][:len(base)])  # copies don't count for base

    def test_gaps_from_own_targets_and_pool(self):
        pool = self.data()
        own = targets.load_targets(B)["difficulty"]
        self.assertEqual(targets.deficits(pool, B, "en")[4], own[4] - 3)  # three copies at level 4
        self.assertEqual(targets.deficits(pool, "base", "en")[4], targets.load_targets("base")["difficulty"][4] - 3)
        gaps = targets.draft_gaps(pool, B)
        self.assertEqual(set(gaps), set(own))
        self.assertLess(gaps[4] / own[4], gaps[1] / own[1])  # level 4 has approved copies, level 1 none


class Concepts(Fixture):
    def test_new_subcategory_concept_call_shows_scope_samples_neighbours(self):
        qgen.cmd_concepts(argparse.Namespace(bundle=B, subcategories=NEW, run=None, top_up=False, jobs=1, model="opus"))
        user = self.calls[0][1]
        scope = qgen.scope_of(B, NEW)
        self.assertIn("Scope: " + scope["scope"], user)
        self.assertIn("## Sample concepts (from the taxonomy)\n- " + scope["samples"][0], user)
        self.assertIn(qgen.bundle_row(B)["rule"], user)
        lst_user = self.calls[1][1]
        self.assertIn("## Existing questions\nnone", lst_user)
        self.assertIn("questions of neighbouring subcategories", lst_user)
        self.assertIn("Year of the Dog", lst_user)  # the copy in the neighbour chinese-zodiac
        self.assertEqual(len(concepts.load(B, NEW)["concepts"]), 6)

    def test_reused_subcategory_list_tags_its_copies(self):
        qgen.cmd_concepts(argparse.Namespace(bundle=B, subcategories=REUSED, run=None, top_up=False, jobs=1, model="opus"))
        self.assertIn('"id": "q-0002"', self.calls[1][1])  # the copies are the list call's existing questions
        by = {x["id"]: x for x in self.data()}
        self.assertEqual((by["q-0002"]["concept"], by["q-0004"]["concept"]), ("Custom 0", "Custom 0"))

    def test_later_copies_seeded_from_their_source(self):
        concepts.save(B, REUSED, {"subcategory": REUSED, "facets": ["Roots"], "axis_fit": FIT,
                                  "concepts": [{"name": "potato", "facet": "Roots", "known_at": 2}]})
        qgen.seed_copies(B)
        by = {x["id"]: x for x in self.data()}
        self.assertEqual((by["q-0002"]["concept"], by["q-0002"]["axes"]), ("Carrot", AXES))
        self.assertEqual(by["q-0004"]["concept"], "potato")  # same key: the list's own name
        self.assertIsNone(by["q-0006"]["concept"])  # chinese-zodiac has no list yet
        lst = concepts.load(B, REUSED)
        self.assertIn({"name": "Carrot", "facet": "Other", "known_at": 3}, lst["concepts"])
        self.assertEqual(concepts.unused(lst, concepts.uses(self.data(), B, REUSED)), [])  # drafts can't draw a copy's concept
        qgen.seed_copies(B)
        self.assertEqual(len(concepts.load(B, REUSED)["concepts"]), 2)  # idempotent


class Overlap(Fixture):
    def test_avoid_list_has_copies_and_neighbours(self):
        pool = {"questions": self.data()}
        self.assertIn("Carrot (Which orange root is rich in vitamin A?)", qgen.existing_answers(pool, B, REUSED, "en"))
        self.assertTrue(any(a.startswith("Year of the Dog") for a in qgen.existing_answers(pool, B, NEW, "en")))
        self.assertEqual([x["id"] for x in qgen.neighbours(pool, "base", REUSED, "en")], [])

    def test_merge_and_rate_see_copies(self):
        draft = {**q(None, bundle=B, sub=NEW, answer="Carrot", question="Which orange root is rich in vitamin A?"), "tmp_id": "t-1"}
        del draft["id"]
        self.assertIn("like q-0002:", qgen.duplicates(draft, [x for x in self.data() if x["bundle"] == B], "en"))
        cands = qgen.overlap_candidates(draft, qgen.as_locale(self.data(), "en"), {}, "en")
        self.assertIn("q-0002", [p.get("of", p)["id"] for p, _, _ in cands])

    def test_already_asked_sees_the_copy(self):
        concepts.save(B, REUSED, {"subcategory": REUSED, "facets": ["Roots"], "axis_fit": FIT,
                                  "concepts": [{"name": "Carrot", "facet": "Roots", "known_at": 4}]})
        plan = qgen.draw_slots([REUSED], self.data(), concepts.load_axes(B), 1, 1, B, "en")
        self.assertTrue(any("vitamin A" in a for a in plan[REUSED][0]["already_asked"]))


class Prompts(Fixture):
    def start(self, subs):
        d = self.work / "batch-900"
        d.mkdir()
        (d / "run.json").write_text(json.dumps({"mode": "batch", "bundle": B, "subcategories": subs, "draft_locale": "en",
                                                "pilot": True, "slots": batches.PILOT_SLOTS}))
        for s in subs:
            concepts.save(B, s, {"subcategory": s, "facets": ["Customs"], "axis_fit": FIT,
                                 "concepts": [{"name": f"{s} {i}", "facet": "Customs", "known_at": 4} for i in range(5)]})
        return d

    def test_pilot_run_json_and_size(self):
        def stop(steps, again, run=None, validate=True):
            raise SystemExit("stopped")
        self.patch(qgen, "run_steps", stop)
        self.patch(qgen, "lock_run", lambda d: d.mkdir(parents=True, exist_ok=True))
        a = argparse.Namespace(from_bundle=None, translate=None, ids=None, dry_run=False, media_first=False, files=None,
                               until=None, bundle=B, run=None, subcategories=None, count=None, jobs=1)
        with self.assertRaises(SystemExit):
            qgen.cmd_batch(a)
        run = json.loads(next(self.work.glob("batch-*/run.json")).read_text())
        self.assertEqual((run["pilot"], run["slots"], run["draft_locale"], len(run["subcategories"])),
                         (True, batches.PILOT_SLOTS, "en", batches.PILOT_SUBCATEGORIES))

    def test_draft_prompt_renders_scope_rule_voice_and_slots(self):
        d = self.start([LANG, NEW])
        qgen.cmd_draft(argparse.Namespace(run=d.name, jobs=1, model="opus"))
        users = {u.split("\n")[1].split(" (")[0]: u for _, u in self.calls}
        lang = users[categories.display(B, LANG, "en")]
        self.assertIn("Scope: " + qgen.scope_of(B, LANG)["scope"], lang)  # language subcategory: never what a character means
        self.assertIn("never what a shown character means", lang)
        self.assertIn(qgen.bundle_row(B)["rule"], lang)
        self.assertIn("Voice: " + qgen.bundle_row(B)["voice"], lang)
        slots = json.loads(lang.split("## Slots\n", 1)[1].split("\n\n", 1)[0])
        self.assertEqual(len(slots), batches.PILOT_SLOTS)
        self.assertIn("Year of the Dog", users[categories.display(B, NEW, "en")])  # neighbour's copy in the avoid list
        system = self.calls[0][0]  # decision 789: house-style's format rule for Chinese words
        self.assertIn('画蛇添足 (huà shé tiān zú, "drawing legs on a snake")', system)
        self.assertIn("it asks their origin story, author, dynasty", system)

    def test_rule_reaches_judging_calls_only_for_further_base(self):
        self.assertIn(qgen.bundle_row(B)["rule"], qgen.rule_section(B, "en"))
        self.assertIn("Every question here is in the `chinese-base` bundle", qgen.rule_section(B, "en"))
        self.assertEqual(qgen.rule_section("base", "en"), "")
        self.assertEqual(qgen.rule_section("colombia", "es"), "")

    def test_dry_run_makes_no_call(self):
        a = argparse.Namespace(from_bundle=None, translate=None, ids=None, dry_run=True, media_first=False, files=None,
                               until=None, bundle=B, run=None, subcategories=None, count=None, jobs=1)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            qgen.cmd_batch(a)
        self.assertIn("27 subcategories × 3 slots = 81 (the bundle's first draft run, a pilot)", out.getvalue())
        self.assertEqual(self.calls, [])
        self.assertEqual(list(self.work.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
