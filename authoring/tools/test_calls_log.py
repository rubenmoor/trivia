"""qgen.calls() and the calls log writer survive a cut-off line (task 2165)."""
import sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402


class CallsLog(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.path = self.d / "calls.jsonl"

    def test_cut_off_in_the_middle_keeps_the_glued_record(self):
        self.path.write_text('{"usd": 1}\n{"usd": 2, "cache_rea{"usd": 3}\n{"usd": 4}\n')
        self.assertEqual([c["usd"] for c in qgen.calls(self.d)], [1, 3, 4])

    def test_cut_off_at_the_end_is_dropped(self):
        self.path.write_text('{"usd": 1}\n{"usd": 2, "cache_rea')
        self.assertEqual([c["usd"] for c in qgen.calls(self.d)], [1])

    def test_append_after_cut_off_starts_a_new_line(self):
        self.path.write_text('{"usd": 1}\n{"usd": 2, "cache_rea')
        qgen.media_first.append(self.path, {"usd": 3}, qgen.threading.Lock())
        self.assertEqual([c["usd"] for c in qgen.calls(self.d)], [1, 3])

    def test_log_writer_uses_the_safe_append(self):
        self.path.write_text('{"usd": 1}\n{"usd": 2, "cache')
        qgen.CALLS.log(self.d, "m", "ok", {"total_cost_usd": 5}, 1.0)
        self.assertEqual([c["usd"] for c in qgen.calls(self.d)], [1, 5])


if __name__ == "__main__":
    unittest.main()
