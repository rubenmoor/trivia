"""fit.md renders for chinese-base with three real base items (an en source, an es source's en translation, a sound):
rule and voice filled, every item field present, no placeholder left. `--print` prints the rendered prompt."""
import json, re, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402

FIELDS = ["id", "subcategory", "difficulty", "description", "question", "answer", "wrong_answers", "hints", "fun_fact", "media"]


def samples():
    """Three approved base sources with their fit items: en, es with an approved en translation, an audio one."""
    pool = [q for q in qgen.load_json(qgen.POOL)["questions"]
            if q["status"] == "approved" and (q.get("bundle") or "base") == "base"]
    tr = {t["id"]: t for t in qgen.translations.load("en")["questions"]}
    en = next(q for q in pool if q.get("locale") == "en")
    es = next(q for q in pool if q.get("locale") == "es" and qgen.fit_text(q, tr))
    audio = next(q for q in pool if q["media"]["type"] == "audio" and qgen.fit_text(q, tr))
    return [(q, qgen.fit_item(q, qgen.fit_text(q, tr))) for q in (en, es, audio)]


def rendered():
    items = samples()
    return qgen.fit_system("chinese-base") + "\n\n" + qgen.fit_user([it for _, it in items]), items


class FitPrompt(unittest.TestCase):
    def test_renders(self):
        text, items = rendered()
        b = qgen.bundle_row("chinese-base")
        self.assertIn(b["rule"], text)
        self.assertIn(b["voice"], text)
        self.assertIn("`chinese-base`", text)
        self.assertIsNone(re.search(r"\{[a-z_]+\}", text), re.findall(r"\{[a-z_]+\}", text))
        for r in ("euro_centric", "latam_centric", "wordplay", "sensitivity", "too_hard_here", "other"):
            self.assertIn(f"`{r}`", text)
        for q, it in items:
            self.assertEqual(list(it), FIELDS)
            for k in FIELDS:
                self.assertTrue(it[k], f"{q['id']}: {k} empty")
            self.assertEqual(len(it["wrong_answers"]), 3)
            self.assertEqual(len(it["hints"]), 3)
            self.assertTrue(it["media"]["type"] and it["media"]["title"] and it["media"]["credit"], it["media"])
            self.assertIn("broad category:", it["subcategory"])
            self.assertIn(json.dumps(it["question"], ensure_ascii=False), text)
        es = items[1]
        self.assertEqual(es[0]["locale"], "es")
        self.assertNotEqual(es[1]["question"], es[0]["question"], "es source: the en translation's text, not the Spanish")
        self.assertEqual(items[2][1]["media"]["type"], "audio")

    def test_not_copyable(self):
        q = {"id": "q-x", "locale": "es", "question": "¿?"}
        self.assertIsNone(qgen.fit_text(q, {}))
        self.assertIsNone(qgen.fit_text(q, {"q-x": {"id": "q-x", "status": "needs_work"}}))


if __name__ == "__main__":
    if "--print" in sys.argv:
        print(rendered()[0])
    else:
        unittest.main()
