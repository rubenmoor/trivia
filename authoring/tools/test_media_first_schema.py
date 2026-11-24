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

    def test_video_30_s(self):
        v = {"type": "video", "file_url": "https://x/v.webm"}
        self.bad(q(v | {"excerpt": {"start": 0, "end": 31}}), "longer than 30 s")
        self.bad(q(v | {"duration": None}, False), "needs a media.duration")
        self.bad(q(v | {"duration": 40}, False), "at most 30 s")
        self.assertEqual(validate.media_first_problems(q(v | {"excerpt": {"start": 10, "end": 40}})), [])
        self.assertEqual(validate.media_first_problems(q(v | {"duration": 30}, False)), [])
        self.assertEqual(validate.media_first_problems(q({"excerpt": {"start": 0, "end": 60}}, False)), [])

    def test_video_unpicked(self):  # task 2432: no file picked, no duration to demand
        self.assertEqual(validate.media_first_problems(q({"type": "video", "duration": None}, False)), [])

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


class Export(unittest.TestCase):
    def test_play_entry_keeps_excerpt(self):
        base = {"id": "q-1", "status": "approved", "difficulty": 1, "subcategory": "x", "bundle": "base", "locale": "es",
                "description": "", "question": "?", "answer": "a", "wrong_answers": [], "hints": [], "fun_fact": "",
                "background": None}
        ex = {"start": 0, "end": 5}
        e = pool_export.play_entry({**base, "media": {"type": "audio", "role": "essential", "excerpt": ex}})
        self.assertEqual(e["media"]["excerpt"], ex)
        out = translations.play_entries("es", {"questions": [{**base, "media": {"type": "audio", "role": "essential", "excerpt": ex}}]})
        self.assertEqual(out[0]["media"]["excerpt"], ex)


if __name__ == "__main__":
    unittest.main()
