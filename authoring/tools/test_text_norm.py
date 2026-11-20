"""Unicode-aware text normaliser: Han text keeps its characters, Latin results as before (task 2374)."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import concepts  # noqa: E402


def q(question, answer, role="decorative"):
    return {"question": question, "answer": answer, "media": {"role": role, "type": "image"}}


class Latin(unittest.TestCase):
    def test_unchanged(self):
        self.assertEqual(concepts.key("La Edad Média"), "edad media")
        self.assertEqual(concepts.key("Straße, der Große"), "strasse grosse")
        self.assertEqual(concepts.key("Año 1492!"), "ano 1492")

    def test_two_marks_fold(self):  # Vietnamese: a letter's second mark folds too
        self.assertEqual(concepts.key("Hồ Chí Minh"), concepts.key("Ho Chi Minh"))
        self.assertEqual(concepts.key("Nguyễn"), "nguyen")
        self.assertEqual(concepts.key("Ệ"), "e")

    def test_modifier_letters_vanish(self):  # ʻokina, as before
        self.assertEqual(concepts.key("Kauaʻi"), concepts.key("Kauai"))
        self.assertEqual(concepts.key("ʻOhana"), "ohana")

    def test_letters_kept(self):  # changed: the ASCII fold deleted these letters
        self.assertEqual(concepts.key("Søren Kierkegaard"), "søren kierkegaard")
        self.assertEqual(concepts.key("Đà Nẵng"), "đa nang")
        self.assertEqual(concepts.key("Sacré-Cœur"), "sacre cœur")
        self.assertEqual(concepts.key("Ægir"), "ægir")
        self.assertEqual(concepts.key("Lech Wałęsa"), "lech wałesa")
        self.assertEqual(concepts.key("Москва"), "москва")

    def test_slug_ascii(self):
        self.assertEqual(concepts.slug("Música y Cine"), "musica-y-cine")

    def test_stem_plurals(self):
        self.assertEqual(qgen.stem("cities boxes", "en"), "city box")
        self.assertEqual(qgen.stem("Almenas padres"), "almena padr")


class Han(unittest.TestCase):
    def test_key_keeps_characters(self):
        self.assertEqual(concepts.key("长城"), "长城")
        self.assertEqual(concepts.key("ゴスロリ"), "ゴスロリ")  # dakuten kept
        self.assertNotEqual(concepts.key("长城"), concepts.key("故宫"))

    def test_options_distinct(self):
        for a, b in (("第1名", "1号"), ("约100万", "100多万"), ("长城", "故宫")):
            self.assertNotEqual(qgen.option_key(a), qgen.option_key(b))
        self.assertEqual(qgen.option_key("长城"), qgen.option_key("长城 "))

    def test_duplicates(self):
        pool = [q("中国最长的城墙叫什么？", "长城"), q("故宫位于哪个城市？", "北京")]
        self.assertIsNotNone(qgen.duplicates(q("中国最长的城墙叫什么名字？", "长城"), pool, "zh-Hans"))
        self.assertIsNone(qgen.duplicates(q("哪座古建筑在北京？", "故宫"), pool, "zh-Hans"))

    def test_stem_bigrams(self):
        self.assertEqual(qgen.stem("万里长城 abc", "zh-Hans"), "万里 里长 长城 abc")
        self.assertEqual(qgen.stem("山", "zh-Hans"), "山")

    def test_overlap(self):
        a = {"question": "长城全长大约多少公里？", "answer": "两万一千公里", "fun_fact": ""}
        b = {"question": "万里长城有多长？", "answer": "两万一千公里", "fun_fact": ""}
        c = {"question": "故宫建于哪个朝代？", "answer": "明朝", "fun_fact": ""}
        found = qgen.overlap_candidates(a, [b, c], {}, "zh-Hans")
        self.assertEqual([p for p, *_ in found], [b])

    def test_overlap_answer_in_text(self):  # rank 3 with 2-character answers
        a = {"question": "唐朝最有名的诗人是谁？", "answer": "李白", "fun_fact": ""}
        b = {"question": "李白生活在哪个朝代？", "answer": "唐朝", "fun_fact": ""}
        self.assertEqual([r for _, _, r in qgen.overlap_candidates(a, [b], {}, "zh-Hans")], [3])
        c = {"question": "万里长城大约有多长？", "answer": "两万公里", "fun_fact": ""}
        self.assertEqual([r for _, _, r in qgen.overlap_candidates({**a, "answer": "长城"}, [c], {}, "zh-Hans")], [3])

    def test_overlap_similar_answer(self):  # rank 1: 长城 inside 万里长城
        a = {"question": "哪座建筑在中国北方？", "answer": "长城", "fun_fact": ""}
        b = {"question": "哪个古迹可以从山海关走起？", "answer": "万里长城", "fun_fact": ""}
        self.assertEqual([r for _, _, r in qgen.overlap_candidates(a, [b], {}, "zh-Hans")], [1])

    def test_overlap_single_character_no_hit(self):  # one Han character is too short to count
        a = {"question": "中国哪座名山最高？", "answer": "山", "fun_fact": ""}
        b = {"question": "泰山在哪个省？", "answer": "山东", "fun_fact": ""}
        self.assertEqual(qgen.overlap_candidates(a, [b], {}, "zh-Hans"), [])


if __name__ == "__main__":
    unittest.main()
