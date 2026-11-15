"""Media-first fields (plan 203): qgen validate's checks and the excerpt export hold; no network."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import pool_export  # noqa: E402
import translations  # noqa: E402
import validate  # noqa: E402

WORK = {"title": "Ode", "creator": "Beethoven", "year": 1824, "basis": "d. 1827"}


def q(media=None, mf=None):
    m = {"type": "audio", "role": "essential", "duration": 100, **(media or {})}
    out = {"id": "q-1", "media": {k: v for k, v in m.items() if v is not None}}
    if mf is not False:
        out["media_first"] = {"seed": "s", "class": "general", "kind": "music", "probe": "p", **(mf or {})}
    return out


class Fields(unittest.TestCase):
    def bad(self, question, text):
        self.assertTrue(any(text in p for p in validate.media_first_problems(question)), text)

    def test_valid(self):
        self.assertEqual(validate.media_first_problems(q({"excerpt": {"start": 0, "end": 60}})), [])
        self.assertEqual(validate.media_first_problems(q({"work": WORK}, {"class": "pd-music"})), [])
        self.assertEqual(validate.media_first_problems(q({"type": "image", "duration": None}, False)), [])

    def test_excerpt(self):
        self.bad(q({"excerpt": {"start": 5, "end": 5}}), "start < end")
        self.bad(q({"excerpt": {"start": -1, "end": 5}}), "start < end")
        self.bad(q({"excerpt": {"start": 0, "end": 61}}), "longer")
        self.bad(q({"excerpt": {"start": 50, "end": 101}}), "after media.duration")
        self.bad(q({"excerpt": {"start": "0", "end": 5}}), "numbers")
        self.bad(q({"excerpt": {"start": 0}}), "numbers")
        self.bad(q({"type": "image", "duration": None, "excerpt": {"start": 0, "end": 5}}), "only on audio/video")

    def test_duration(self):
        self.bad(q({"duration": 0}), "duration")
        self.bad(q({"type": "image", "duration": 3}), "duration")

    def test_media_first(self):
        self.bad(q(mf={"class": "weird"}), "class")
        self.bad(q(mf={"seed": ""}), "seed")
        self.bad(q(mf={"extra": 1}), "media_first must be")

    def test_work(self):
        self.bad(q(mf={"class": "pd-film"}), "required")
        self.bad(q({"work": {"title": "x"}}, {"class": "pd-film"}), "required")
        self.bad(q({"work": WORK}), "only for")


class Hold(unittest.TestCase):
    def test_held(self):
        self.assertTrue(pool_export.held(q({"excerpt": {"start": 0, "end": 5}})))
        self.assertFalse(pool_export.held(q()))
        self.assertFalse(pool_export.held(q({"excerpt": None})))

    def test_play_entries_skip_held(self):
        base = {"id": "q-1", "status": "approved", "difficulty": 1, "subcategory": "x", "bundle": "base",
                "description": "", "question": "?", "answer": "a", "wrong_answers": [], "hints": [], "fun_fact": "",
                "background": None}
        ok = {**base, "media": {"type": "audio", "role": "essential"}}
        held = {**base, "id": "q-2", "media": {"type": "audio", "role": "essential", "excerpt": {"start": 0, "end": 5}}}
        out = translations.play_entries("es", {"questions": [ok, held]})
        self.assertEqual([e["id"] for e in out], ["q-1"])


if __name__ == "__main__":
    unittest.main()
