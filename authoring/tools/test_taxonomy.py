"""Taxonomy proposals carry a career subject (plan 194): refused when missing or unknown, kept on a remap."""
import sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import categories, taxonomy  # noqa: E402


def proposal(**subject):
    return {"bundle": "mexico", "categories": [{
        "slug": "geography", "en": "Geography", "name": "Geografía", **subject, "de": "Geografie",
        "subcategories": [{"slug": "landmarks", "en": "Landmarks", "name": "Lugares", "de": "Orte"}]}]}


def draft(bundle, todo, d):
    for e in todo:
        e["names"] = {"de": "x"} | e["names"]


class Subjects(unittest.TestCase):
    def test_missing_or_unknown_refused(self):
        for p in (proposal(), proposal(subject="foo")):
            self.assertTrue(any("subject" in e for e in taxonomy.taxonomy_errors(p, "mexico")))
        self.assertFalse(any("subject" in e for e in taxonomy.taxonomy_errors(proposal(subject="geography"), "mexico")))

    def test_remap_new_category_needs_subject(self):
        row = lambda s: {"id": "q", "subcategory": "new-sub", "category": "New", "scope": "x", "reason": "", "subject": s}
        with mock.patch.object(taxonomy, "load_json", return_value={"questions": [{"id": "q", "bundle": "mexico"}]}):
            for s, ok in (("", False), ("foo", False), ("arts", True)):
                errors, _, _ = taxonomy.remap_errors({"questions": [row(s)], "lists": []}, "mexico")
                self.assertEqual(not any("subject" in e for e in errors), ok, (s, errors))

    def test_write_keeps_existing_subject(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "categories.json"
            path.write_text('{"categories": [{"slug": "geography", "subject": "nature", "subcategories": ["landmarks"]}]}')
            p = proposal()  # no subject: the existing one stays
            p["categories"][0]["subcategories"][0] |= {"scope": ""}
            saved = {}
            with mock.patch.object(categories, "path", return_value=path), \
                 mock.patch.object(taxonomy, "draft_names", side_effect=draft), mock.patch.object(taxonomy, "ROOT", Path("/")), \
                 mock.patch.object(taxonomy, "load_json", side_effect=lambda f, d=None: {} if f != path else qgen.load_json(f, d)), \
                 mock.patch.object(taxonomy, "save_json", side_effect=lambda f, d: saved.setdefault(str(f), d)), \
                 mock.patch.object(taxonomy, "bundle_row", return_value={"id": "mexico"}), \
                 mock.patch.object(taxonomy.translations, "draft_locale", return_value="es"):
                taxonomy.write_taxonomy("mexico", p, Path(tmp))
            self.assertEqual(saved[str(path)]["categories"][0]["subject"], "nature")
            p["categories"][0]["subject"] = "arts"  # the proposal wins
            with mock.patch.object(categories, "path", return_value=path), mock.patch.object(taxonomy, "draft_names", side_effect=draft), mock.patch.object(taxonomy, "ROOT", Path("/")), \
                 mock.patch.object(taxonomy, "load_json", return_value={}), mock.patch.object(taxonomy, "save_json", side_effect=lambda f, d: saved.__setitem__(str(f), d)), \
                 mock.patch.object(taxonomy, "bundle_row", return_value={"id": "mexico"}), \
                 mock.patch.object(taxonomy.translations, "draft_locale", return_value="es"):
                taxonomy.write_taxonomy("mexico", p, Path(tmp))
            self.assertEqual(saved[str(path)]["categories"][0]["subject"], "arts")


def base_proposal():
    sub = lambda slug, origin, **kw: {"slug": slug, "en": slug.title(), "name": slug.title(), "origin": origin, "scope": "s",
                                      "reason": "r", "related": [], "language": False, "samples": [], **kw}
    return {"bundle": "chinese-base", "target": 6000, "expected_keep": 0.5, "categories": [{
        "slug": "nature", "en": "Nature", "name": "Nature", "subject": "nature", "subject_reason": "x", "origin": "reused",
        "scope": "s", "reason": "r", "subcategories": [sub("mammals", "reused"), sub("solar-terms", "new", related=["mammals"])]}],
        "from_base": [{"base": "mammals", "to": "mammals", "reason": ""}, {"base": "castles", "to": None, "reason": "euro_centric"}]}


FAKE_BASE = {"mammals", "castles"}


def base_errors(p, approved=None):
    with mock.patch.object(taxonomy.categories, "subcategories", return_value=list(FAKE_BASE)), \
         mock.patch.object(taxonomy, "base_approved", return_value=approved or {"mammals": 3, "castles": 2}):
        return taxonomy.base_bundle_errors(p)


class BaseBundle(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(base_errors(base_proposal()), [])

    def test_refusals(self):
        def bad(edit, text):
            p = base_proposal()
            edit(p)
            self.assertTrue(any(text in e for e in base_errors(p)), (text, base_errors(p)))
        bad(lambda p: p["categories"][0]["subcategories"][0].update(slug="whales"), "reused, but not a base")
        bad(lambda p: p["from_base"].append({"base": "volcanoes", "to": None, "reason": "wordplay"}), "not a base subcategory")
        bad(lambda p: p["from_base"].pop(), "castles' (2 approved) is missing")
        bad(lambda p: p["from_base"][0].update(to="tea"), "not a proposal subcategory")
        bad(lambda p: p["from_base"][1].update(reason=""), "no target and no reason")
        bad(lambda p: p.update(expected_keep=2), "expected_keep")

    def test_unapproved_base_subcategory_may_be_missing(self):
        p = base_proposal()
        p["from_base"].pop()
        self.assertEqual(base_errors(p, {"mammals": 3}), [])

    def test_apply_writes_related_and_map(self):
        saved = {}
        p = base_proposal()
        with mock.patch.object(taxonomy, "ROOT", Path("/")), \
             mock.patch.object(taxonomy, "write_taxonomy", return_value=["mammals", "solar-terms"]), \
             mock.patch.object(taxonomy, "taxonomy_errors", return_value=[]), mock.patch.object(taxonomy, "load_json", return_value=p), \
             mock.patch.object(taxonomy, "save_json", side_effect=lambda f, d: saved.__setitem__(Path(f).name, d)), \
             mock.patch.object(taxonomy, "off_list", return_value={}), mock.patch.object(taxonomy, "validate_pool", return_value=([], 0)), \
             mock.patch.object(taxonomy, "bundle_row", return_value={"kind": "base"}), \
             mock.patch.object(taxonomy.layout, "related", return_value=Path("/x/related.json")):
            taxonomy.apply_taxonomy("chinese-base", Path("p.json"), Path("/tmp") / "d")
        self.assertEqual(saved["related.json"]["subcategories"], {"mammals": [], "solar-terms": ["mammals"]})
        self.assertEqual(saved["from-base.json"]["subcategories"]["castles"], {"to": None, "reason": "euro_centric"})
        self.assertEqual(saved["from-base.json"]["subcategories"]["mammals"]["to"], "mammals")

    def test_render_without_call(self):
        b = {"id": "chinese-base", "name": "China", "languages": ["zh-Hans", "en"], "kind": "base", "rule": "R", "voice": "V"}
        bases = [{"slug": "animals", "bundle": "base", "subject": "nature", "subcategories": ["mammals", "castles"]}]
        approved = {"mammals": 3, "castles": 2}
        with mock.patch.object(taxonomy, "bundle_text", return_value="rule R"), mock.patch.object(taxonomy.categories, "display", return_value="X"), \
             mock.patch.object(taxonomy, "cat_name", return_value="Animals"):
            user = taxonomy.base_user(b, 6000, 30, "NOTES", bases, approved)
            self.assertIn("## Research notes", user)
            self.assertIn("`mammals` X: 3", user)
            self.assertNotIn("Research notes", taxonomy.base_user(b, 6000, 30, "", bases, approved))
            md = taxonomy.base_taxonomy_md(base_proposal(), bases, approved)
        self.assertIn("| `castles` | 2 | null | euro_centric |", md)
        system = (taxonomy.PROMPTS / "taxonomy-base.md").read_text(encoding="utf-8")
        for key in ("{per_sub}", "{subs}", "{subjects}"):
            self.assertIn(key, system)
        self.assertNotIn("{language}", system)


if __name__ == "__main__":
    unittest.main()
