"""fit.md renders for chinese-base: rule and voice filled, no placeholder left."""
import json, re, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402


class FitPrompt(unittest.TestCase):
    def test_renders(self):
        text = qgen.prompt("fit", locale="en", bundle="chinese-base")
        b = qgen.bundle_row("chinese-base")
        self.assertIn(b["rule"], text)
        self.assertIn(b["voice"], text)
        self.assertIn("`chinese-base`", text)
        self.assertIsNone(re.search(r"\{[a-z_]+\}", text), re.findall(r"\{[a-z_]+\}", text))
        for r in ("euro_centric", "latam_centric", "wordplay", "sensitivity", "too_hard_here", "other"):
            self.assertIn(f"`{r}`", text)


if __name__ == "__main__":
    unittest.main()
