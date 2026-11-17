"""`media.play_window` (mirrors playWindow in pool.ts) and the review input's window (plan 217)."""
import sys, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order)
import media as media_tool  # noqa: E402
import media_first as mf  # noqa: E402


def m(kind="video", excerpt=None, duration=100):
    return {"type": kind, "excerpt": excerpt, "duration": duration}


class PlayWindow(unittest.TestCase):
    def test_video(self):
        w = media_tool.play_window
        self.assertEqual(w(m(excerpt={"start": 10, "end": 50})), {"start": 10, "end": 40})
        self.assertEqual(w(m(excerpt={"start": 10, "end": 20})), {"start": 10, "end": 20})
        self.assertEqual(w(m()), {"start": 0, "end": 30})
        self.assertEqual(w(m(duration=12)), {"start": 0, "end": 12})
        self.assertEqual(w(m(duration=None)), {"start": 0, "end": 30})

    def test_audio_unchanged(self):
        self.assertIsNone(media_tool.play_window(m("audio")))
        self.assertEqual(media_tool.play_window(m("audio", {"start": 5, "end": 65})), {"start": 5, "end": 65})


class ReviewInput(unittest.TestCase):
    def q(self, **kw):
        return {"media": {"type": "video", "query": "File:a.webm", "license": "CC0", **kw}, "media_first": {"probe": "x", "kind": "k", "class": "general"}}

    def run_input(self, q, stored_window):
        seen = []

        def probe(title, excerpt=None):
            seen.append(excerpt)
            return {"dir": "/nonexistent", "window": [excerpt["start"], excerpt["end"]]}
        with mock.patch.object(mf, "load_probe", lambda ref: {"dir": "/nonexistent", "window": stored_window}), \
                mock.patch.object(mf, "probe", probe), mock.patch.object(mf, "commons_file", lambda t: None), \
                mock.patch.object(mf, "media_findings", lambda q, p: []):
            return mf.review_input(q), seen

    def test_long_file_probes_capped_window(self):
        inp, seen = self.run_input(self.q(duration=100, excerpt={"start": 10, "end": 50}), [10, 50])
        self.assertEqual(seen, [{"start": 10, "end": 40}])
        self.assertEqual(inp["excerpt"], {"start": 10, "end": 40})
        self.assertEqual(inp["aids"]["window"], [10, 40])

    def test_no_excerpt_unknown_duration(self):
        inp, seen = self.run_input(self.q(duration=None), [0, 200])
        self.assertEqual(inp["excerpt"], {"start": 0, "end": 30})

    def test_matching_probe_is_kept(self):
        _, seen = self.run_input(self.q(duration=12), [0, 12])
        self.assertEqual(seen, [])

    def test_audio_unchanged(self):
        q = self.q(type="audio", duration=40)
        inp, seen = self.run_input(q, [0, 40])
        self.assertEqual(seen, [])
        self.assertIsNone(inp["excerpt"])


if __name__ == "__main__":
    unittest.main()
