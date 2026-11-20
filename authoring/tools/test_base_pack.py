"""A second base bundle in a pack directory without es (plan 227 task 1): `qgen bundle new --kind base`, validate,
export and report on a temp copy of the tools with a small data set (base, stem, the new bundle)."""
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
NEW = "pack-base"
LANGS = ["zh-Hans", "zh-Hant", "en"]


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, doc):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class BasePack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = cls.root = Path(cls.tmp.name) / "repo"
        skip = shutil.ignore_patterns("__pycache__", "node_modules", "*.lock")
        shutil.copytree(REPO / "authoring/tools", root / "authoring/tools", ignore=skip)
        shutil.copytree(REPO / "app/client/src", root / "app/client/src", ignore=skip)
        shutil.copytree(REPO / "authoring/steam", root / "authoring/steam", ignore=skip)
        for d in REPO.iterdir():  # read-only rest (modding/, …); copies where code finds files by its own path
            if d.name not in {"app", "authoring", "work", "media", "state", ".git"}:
                (root / d.name).symlink_to(d)
        data, adata = root / "app/data", root / "authoring/data"
        data.mkdir(parents=True)
        for f in ["categories.json", "age-groups.json", "subjects.json", "old-keys.json", *[p.name for p in (REPO / "app/data").glob("names.*.json")]]:
            shutil.copy(REPO / "app/data" / f, data / f)
        shutil.copytree(REPO / "app/data/bundles/stem", data / "bundles/stem", ignore=shutil.ignore_patterns("pool*.json"))
        bundles = read(REPO / "app/data/bundles.json")
        write(data / "bundles.json", {**bundles, "bundles": [b for b in bundles["bundles"] if b["id"] in ("base", "stem")]})
        adata.mkdir(parents=True)
        for f in ["question-axes.json", "regional-categories.json"]:
            shutil.copy(REPO / "authoring/data" / f, adata / f)
        shutil.copytree(REPO / "authoring/data/concepts", adata / "concepts")
        t = read(REPO / "authoring/data/targets.json")
        write(adata / "targets.json", {k: v for k, v in t.items() if k not in {b["id"] for b in bundles["bundles"]} - {"base", "stem"}})
        src = read(REPO / "authoring/data/questions.json")
        base = [q for q in src["questions"] if q.get("bundle") == "base" and q["status"] == "approved" and q["locale"] == "en"
                and q["media"].get("type") == "image"][:3]
        cls.base_ids = [q["id"] for q in base]
        new = {**base[0], "id": "q-90001", "bundle": NEW, "subcategory": "dynasties", "batch": None, "concept": None}
        write(adata / "questions.json", {**{k: v for k, v in src.items() if k != "questions"}, "questions": [*base, new]})
        cls.env = {**os.environ, **{k: str(Path(cls.tmp.name) / d) for k, d in
                                    [("TRIVIA_WORK", "work"), ("TRIVIA_STATE", "state"), ("TRIVIA_MEDIA", "media")]}}
        cls.created = cls.qgen("bundle", "new", NEW, "--kind", "base", "--language", ",".join(LANGS), "--icon", "globe",
                               "--name", "Paquete chino", "--description", "Preguntas de China.",
                               "--rule", "China-centred.", "--voice", "English for a Chinese family; zh: standard written Chinese")
        pack = data / "bundles" / NEW
        write(pack / "categories.json", {"about": "fixture", "categories": [
            {"slug": "history", "subject": "history", "subcategories": ["dynasties"]}]})
        for l in LANGS:
            write(pack / f"names.{l}.json", {"version": 1, "locale": l, "categories": {"history": f"History {l}"},
                                             "subcategories": {"dynasties": f"Dynasties {l}"}})
        for f in data.glob("names.*.json"):  # bundle names: the fixture's bundles; zh: only the new one
            doc, l = read(f), f.name.split(".")[1]
            if "bundles" in doc or l in LANGS:
                doc["bundles"] = {k: v for k, v in (doc.get("bundles") or {}).items() if k in ("base", "stem")}
                doc["bundles"][NEW] = {"name": f"Chinese base {l}", "description": f"China {l}"}
                write(f, doc)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @classmethod
    def qgen(cls, *args):
        return subprocess.run([sys.executable, str(cls.root / "authoring/tools/qgen.py"), *args], cwd=cls.root,
                              env=cls.env, capture_output=True, text=True, timeout=600)

    def ok(self, *args):
        r = self.qgen(*args)
        self.assertEqual(r.returncode, 0, f"qgen {' '.join(args)}:\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
        return r.stdout

    def test_1_bundle_new(self):
        self.assertEqual(self.created.returncode, 0, self.created.stderr)
        rows = read(self.root / "app/data/bundles.json")["bundles"]
        self.assertEqual([b["id"] for b in rows], ["base", NEW, "stem"])  # after the base bundles
        row = rows[1]
        self.assertEqual((row["kind"], row["languages"], row["icon"]), ("base", LANGS, "globe"))
        t = read(self.root / "authoring/data/targets.json")
        self.assertEqual(t[NEW]["total"], t["base"]["total"])
        self.assertEqual(sum(t[NEW]["difficulty"].values()), t["base"]["total"])

    def test_2_export_validate_report(self):
        self.ok("export")
        pack = self.root / "app/data/bundles" / NEW
        self.assertEqual(sorted(p.name for p in pack.glob("pool*.json")), ["pool.en.json"])
        self.assertEqual([q["id"] for q in read(pack / "pool.en.json")["questions"]], ["q-90001"])
        self.assertEqual([q["id"] for q in read(self.root / "app/data/pool.en.json")["questions"]], self.base_ids)
        out = self.ok("validate")
        self.assertIn("OK:", out)
        out = self.ok("report", "--bundle", NEW, "--locale", "en")
        self.assertIn(f"progress vs. targets ({NEW}, en):", out)
        self.assertIn("largest over en, zh-Hans, zh-Hant", out)  # its own languages only
        out = self.ok("report", "--bundle", NEW)  # default: its first language, every drafting line
        self.assertIn(f"progress vs. targets ({NEW}, zh-Hans):", out)
        base = self.ok("report", "--locale", "en")
        self.assertIn("largest over es, es-ES, en, de", base)  # targets separate: base's own locales

    def refused(self, path, change, message):
        keep = path.read_text(encoding="utf-8")
        try:
            doc = read(path)
            change(doc)
            write(path, doc)
            r = self.qgen("validate")
            self.assertNotEqual(r.returncode, 0)
            self.assertIn(message, r.stdout + r.stderr)
        finally:
            path.write_text(keep, encoding="utf-8")

    def test_3_problems(self):
        pack, adata = self.root / "app/data/bundles" / NEW, self.root / "authoring/data"
        self.refused(pack / "categories.json", lambda d: d["categories"][0].pop("subject"), "category without a subject")
        self.refused(adata / "targets.json", lambda d: d.pop(NEW), f"base bundle '{NEW}' has no targets")
        self.refused(adata / "questions.json", lambda d: d["questions"][-1].update(locale="es"), "locale must be en")
        self.refused(pack / "names.zh-Hans.json", lambda d: d["subcategories"].clear(), "name(s) missing")


class Voices(unittest.TestCase):
    def test_voice_locales(self):
        row = lambda kind, langs: {"id": "x", "kind": kind, "languages": langs}
        self.assertEqual(qgen.voice_locales(row("base", ["es", "es-ES", "en", "de"])), ("es",))
        self.assertEqual(qgen.voice_locales(row("base", LANGS)), tuple(LANGS))
        self.assertEqual(qgen.voice_locales(row("theme", ["en"])), ("es",))
        self.assertEqual(qgen.voice_locales(row("region", ["de"])), ("de",))


if __name__ == "__main__":
    unittest.main()
