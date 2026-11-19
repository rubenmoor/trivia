"""Crash-safe write order (task 2348): apply, merge and translate's done mark; a failure between writes loses nothing."""
import argparse, json, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402  (import order)
import translate  # noqa: E402

REAL_SAVE = qgen.save_json


def draft(tid):
    return {"tmp_id": tid, "difficulty": 3, "description": "d", "question": f"Question {tid}?", "answer": f"Answer {tid}",
            "wrong_answers": ["a", "b", "c"], "hints": ["h1", "h2", "h3"], "fun_fact": "f", "subcategory": "x", "style": None,
            "needs_fact_check": False, "needs_media": False,
            "media": {"type": "none", "query": None, "note": None, "role": None, "license": None}}


def failing(name_part):
    def save(path, data):
        if name_part in Path(path).name:
            raise KeyboardInterrupt
        REAL_SAVE(path, data)
    return save


class WriteOrder(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp()) / "run"
        for sub in ("drafts", "ratings", "factchecks"):
            (self.d / sub).mkdir(parents=True)

    def test_apply_writes_revised_before_drafts(self):
        REAL_SAVE(self.d / "drafts" / "01.json", {"questions": [draft("ta"), draft("tb")], "skipped": []})
        new = draft("ta") | {"question": "Better question?"}
        revs = {"ta": {"action": "revise", "question": new, "reason": "r"}}
        with mock.patch.object(qgen, "save_json", failing("applied.json")), mock.patch.object(qgen, "check_question_shape", lambda q: []):
            with self.assertRaises(KeyboardInterrupt):
                qgen.apply_to_drafts(self.d, revs, set())
        every = [q["tmp_id"] for f in (self.d / "drafts").glob("*.json") for q in json.loads(f.read_text())["questions"]]
        self.assertIn("ta", every)
        self.assertIn("tb", every)
        # crash right after the revised file: t1 still in the old draft too (duplicated, not lost)
        with mock.patch.object(qgen, "save_json", failing("01.json")), mock.patch.object(qgen, "check_question_shape", lambda q: []):
            (self.d / "drafts" / "01.json").write_text(json.dumps({"questions": [draft("ta"), draft("tb")], "skipped": []}))
            for f in (self.d / "drafts").glob("revised-*"):
                f.unlink()
            with self.assertRaises(KeyboardInterrupt):
                qgen.apply_to_drafts(self.d, revs, set())
        self.assertEqual(len(list((self.d / "drafts").glob("revised-*.json"))), 1)
        self.assertFalse((self.d / "applied.json").exists())

    def test_merge_saves_run_state_before_pool(self):
        pool = self.d.parent / "pool.json"
        REAL_SAVE(pool, {"questions": [{"id": "q-0001", "question": "Other?", "answer": "Zzz", "locale": "es"}]})
        REAL_SAVE(self.d / "run.json", {"mode": "batch"})
        REAL_SAVE(self.d / "drafts" / "01.json", {"questions": [draft("ta")], "skipped": []})
        REAL_SAVE(self.d / "ratings" / "01.json", {"ta": {k: 5 for k in qgen.RUBRIC}})
        args = argparse.Namespace(run="run")
        with mock.patch.object(qgen, "POOL", pool), mock.patch.object(qgen, "WORK", self.d.parent), \
                mock.patch.object(qgen, "save_json", failing("pool.json")):
            with self.assertRaises(KeyboardInterrupt):
                qgen.cmd_merge(args)
        self.assertEqual(json.loads((self.d / "merged.json").read_text()), ["ta"])
        self.assertEqual(json.loads((self.d / "ids.json").read_text()), {"ta": "q-0002"})
        self.assertEqual(len(json.loads(pool.read_text())["questions"]), 1)

    def test_translate_done_only_after_unmerged_check(self):
        src = Path(translate.__file__).read_text(encoding="utf-8")
        body = src[src.index("def cmd_translate_batch"):]
        self.assertLess(body.index("if lost := unmerged(d)"), body.index('"done": cfg.get("done")'))


if __name__ == "__main__":
    unittest.main()
