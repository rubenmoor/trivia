"""release_check: the `locale` manual row is asked exactly when a zh pool is new since the previous tag."""
import sys, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release_check as rc  # noqa: E402

BASE = ["app/data/pool.json", "app/data/pool.en.json", "app/data/bundles/base/pool.de.json"]
ZH = "app/data/bundles/chinese-base/pool.zh-Hans.json"


def trees(**by_rev):
    return lambda *a: "\n".join(by_rev[a[3]])


class Locale(unittest.TestCase):
    def new(self, prev_files, head_files):
        with mock.patch.object(rc, "git", trees(v1=prev_files, HEAD=head_files)):
            return rc.new_zh_pool("v1")

    def test_new_pool(self):
        self.assertTrue(self.new(BASE, [*BASE, ZH]))

    def test_no_zh_pool(self):
        self.assertFalse(self.new(BASE, BASE))

    def test_existing_pool_unchanged(self):
        self.assertFalse(self.new([*BASE, ZH], [*BASE, ZH]))

    def test_second_locale_is_new(self):
        self.assertTrue(self.new([*BASE, ZH], [*BASE, ZH, "app/data/pool.zh-Hant.json"]))

    def test_names_file_is_not_a_pool(self):
        self.assertFalse(self.new(BASE, [*BASE, "app/data/names.zh-Hans.json"]))

    def test_no_earlier_tag(self):
        with mock.patch.object(rc, "git", trees(HEAD=[*BASE, ZH])):
            self.assertTrue(rc.new_zh_pool(None))

    def test_checklist_scope(self):
        self.assertIn("locale", rc.checklist("content-only", "v1", False, zh_new=True))
        self.assertNotIn("locale", rc.checklist("content-only", "v1", False))
        self.assertIn("locale", rc.checklist("full", "v1", False, zh_new=True))
        self.assertIsNone(rc.checklist("content-only", "v1", False, zh_new=True)["locale"][1])


if __name__ == "__main__":
    unittest.main()
