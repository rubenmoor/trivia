"""The simulate target check (D-75) follows `--bundles`' base bundles per locale, else the locale's default."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import report  # noqa: E402

CATALOGUE = [
    {"id": "base", "kind": "base", "languages": ["es", "es-ES", "en", "de"]},
    {"id": "chinese-base", "kind": "base", "languages": ["zh-Hans", "zh-Hant", "en"]},
    {"id": "colombia", "kind": "pack", "languages": ["es", "en"]},
]


def check(bundles, locale, default=("base",)):
    return report.target_bundles(bundles, locale, list(default), CATALOGUE)


class TargetBundles(unittest.TestCase):
    def test_default_when_not_given(self):
        self.assertEqual(check(None, "en"), ["base"])

    def test_base_bundle_given(self):
        self.assertEqual(check("chinese-base", "en"), ["chinese-base"])

    def test_pack_not_checked(self):
        self.assertEqual(check("base,colombia", "es"), ["base"])
        self.assertEqual(check("chinese-base,colombia", "en"), ["chinese-base"])

    def test_locale_not_listed_falls_back(self):
        self.assertEqual(check("chinese-base", "es"), ["base"])
        self.assertEqual(check("chinese-base", "zh-Hans", ["chinese-base"]), ["chinese-base"])

    def test_unknown_bundle_dropped(self):
        self.assertEqual(check("no-such-bundle", "en"), ["base"])

    def test_real_catalogue(self):
        self.assertEqual(report.target_bundles("chinese-base,colombia", "en", ["base"]), ["chinese-base"])
        self.assertEqual(report.target_bundles("base,colombia", "es", ["base"]), ["base"])


class Unoffered(unittest.TestCase):
    def test_skips_locales_a_bundle_lacks(self):
        got = report.unoffered("chinese-base", ["es", "en", "zh-Hans", "de"], CATALOGUE)
        self.assertEqual(got, {"es": "chinese-base", "de": "chinese-base"})

    def test_every_bundle_must_offer(self):
        got = report.unoffered("base,chinese-base", ["es", "en", "zh-Hans"], CATALOGUE)
        self.assertEqual(got, {"es": "chinese-base", "zh-Hans": "base"})

    def test_none_given(self):
        self.assertEqual(report.unoffered(None, ["es"], CATALOGUE), {})


if __name__ == "__main__":
    unittest.main()
