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


if __name__ == "__main__":
    unittest.main()
