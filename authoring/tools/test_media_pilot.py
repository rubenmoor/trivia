"""media_pilot's sample, giveaway check and look.html paths (plan 201); no network, no claude."""
import sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media_pilot as mp  # noqa: E402


def files():
    return [{"title": f"File:{c}-{s}-{i}", "class": c, "seed": f"{c}:{s}"}
            for c, seeds in (("general", 5), ("pd-music", 2), ("pd-film", 1)) for s in range(seeds) for i in range(30)]


class Pilot(unittest.TestCase):
    def test_sample_stratified_and_fixed(self):
        a, b = mp.sample(files(), 50, 7), mp.sample(files(), 50, 7)
        self.assertEqual([f["title"] for f in a], [f["title"] for f in b])
        by = {c: [f for f in a if f["class"] == c] for c in mp.CLASSES}
        self.assertEqual({c: len(v) for c, v in by.items()}, {"general": 32, "pd-music": 9, "pd-film": 9})
        self.assertEqual({f["seed"] for f in by["general"]}, {f"general:{s}" for s in range(5)})
        self.assertLessEqual(max(sum(f["seed"] == f"general:{s}" for f in by["general"]) for s in range(5)), 7)

    def test_heard_giveaway(self):
        d = Path(tempfile.mkdtemp())
        (d / "ocr.txt").write_text("frame 1 @ 2 s: LONDON 1939\n")
        p = {"dir": str(d), "speech": {"text": "Here is the tower of Pisa"}}
        self.assertEqual(mp.heard_giveaway("Leaning Tower of Pisa", p), ["pisa", "tower"])
        self.assertEqual(mp.heard_giveaway("London", p), ["london"])
        self.assertEqual(mp.heard_giveaway("Paris", p), [])

    def test_look_paths(self):
        d = Path("/x/work/media-pilot/run")
        self.assertEqual(mp.rel("/y/questions/media/ab.ogg", d), "../../../media/ab.ogg")
        self.assertEqual(mp.rel("/x/work/media-probe/12/sheet.png", d), "../../media-probe/12/sheet.png")


if __name__ == "__main__":
    unittest.main()
