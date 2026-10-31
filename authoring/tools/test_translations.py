"""reject_for_sources: a source marked translatable: false loses its translations in the other locales."""
import sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import translate, translations  # noqa: E402


class RejectForSources(unittest.TestCase):
    def test_rejects_other_locales_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = {l: Path(tmp) / f"{l}.json" for l in translations.LOCALES}
            with mock.patch.object(translations.layout, "translations", paths.get):
                for l in ("de", "es-ES"):
                    translations.save(l, {"questions": [{"id": "q-1", "status": "approved"}, {"id": "q-2", "status": "approved"}]})
                done = translations.reject_for_sources({"q-1"}, skip=("de",))
                self.assertEqual(done, {"es-ES": ["q-1"]})
                es, de = translations.load("es-ES")["questions"], translations.load("de")["questions"]
                self.assertEqual([t["status"] for t in es], ["rejected", "approved"])
                self.assertEqual(es[0]["review"]["reviewer"], "human")
                self.assertEqual([t["status"] for t in de], ["approved", "approved"])


class CommitFiles(unittest.TestCase):
    def test_confirmed_adds_other_locales(self):
        out = Path("out.md")
        plain = translate.commit_files("de", "base", out, 0)
        self.assertNotIn(translations.path("es"), plain)
        files = translate.commit_files("de", "base", out, 1)
        for l in translations.LOCALES:
            self.assertIn(translations.path(l), files)
            self.assertIn(translate.layout.POOL_FILE(l, "base"), files)
        self.assertEqual(len(files), len(set(files)))


class LostMerge(unittest.TestCase):
    def test_unmerged_when_no_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "tr-de-1"
            paths = {l: Path(tmp) / f"{l}.json" for l in translations.LOCALES}
            drafts = [("a", [{"tmp_id": "q-1"}, {"tmp_id": "q-2"}])]
            with mock.patch.object(translations.layout, "translations", paths.get), \
                    mock.patch.object(translate, "run_locale", return_value="de"), \
                    mock.patch.object(translate, "translated_drafts", return_value=drafts):
                self.assertEqual(translate.unmerged(d), ["q-1", "q-2"])
                translations.save("de", {"questions": [{"id": "q-1", "batch": "tr-de-1"}]})
                self.assertEqual(translate.unmerged(d), [])

    def test_limit_words(self):
        self.assertTrue(any(w in "you've hit your weekly limit" for w in qgen.LIMIT_WORDS))


if __name__ == "__main__":
    unittest.main()
