"""The simulate target check (D-75) follows `--bundles`, else the locale's default base bundle."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import report  # noqa: E402


class TargetBundles(unittest.TestCase):
    def test_default_when_not_given(self):
        self.assertEqual(report.target_bundles(None, ["base"]), ["base"])

    def test_bundles_given(self):
        self.assertEqual(report.target_bundles("chinese-base", ["base"]), ["chinese-base"])

    def test_bundle_without_targets_dropped(self):
        self.assertEqual(report.target_bundles("chinese-base,no-such-bundle", ["base"]), ["chinese-base"])
        self.assertEqual(report.target_bundles("no-such-bundle", ["base"]), ["base"])


if __name__ == "__main__":
    unittest.main()
