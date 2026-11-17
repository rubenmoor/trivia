"""media_keep.prune: keeps every pool's picks and unfinished batches' files, deletes the rest (task 2139); no network."""
import json, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import media_cache as mc  # noqa: E402
import media_keep as mk  # noqa: E402


def url(n):
    return f"https://x.org/{n}.webm"


def pool(path, urls):
    qs = [{"id": f"q-{i}", "media": {"file_url": u}} for i, u in enumerate(urls)]
    path.write_text(json.dumps({"questions": qs}), encoding="utf-8")


class Prune(unittest.TestCase):
    def test_prune(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        media, data, work = d / "media", d / "data", d / "work"
        for p in (media, data, work / "batch-1", work / "batch-2", work / "media"):
            p.mkdir(parents=True)
        pool(data / "questions.json", [url("base")])
        pool(data / "questions.de.json", [url("de")])
        (work / "batch-1" / "run.json").write_text('{"mode": "media-first"}')  # in flight
        (work / "batch-1" / "media-first-files.jsonl").write_text(json.dumps({"file_url": url("flight")}) + "\n")
        (work / "batch-1" / "ids.json").write_text('{"mf-1": "q-9"}')
        (work / "media" / "q-9.json").write_text(json.dumps({"candidates": [{"file_url": url("cand")}]}))
        (work / "batch-2" / "run.json").write_text('{"mode": "media-first", "done": true}')  # merged
        (work / "batch-2" / "media-first-files.jsonl").write_text(json.dumps({"file_url": url("old")}) + "\n")
        names = ["base", "de", "flight", "cand", "old", "none"]
        with mock.patch.object(mk, "MEDIA", media), mock.patch.object(mc, "MEDIA", media), \
                mock.patch.object(mk, "SOURCE_POOL", data / "questions.json"), mock.patch.object(mk, "WORK", work), \
                mock.patch.object(mk, "CANDIDATES", work / "media"), \
                mock.patch("batches.WORK", work):
            for n in names:
                mc.cache_path(url(n)).write_bytes(b"xx")
            (work / "batch-2" / "ids.json").write_text("{}")
            (work / "batch-2" / "media-first-files.jsonl").write_text("".join(
                json.dumps({"file_url": url(n)}) + "\n" for n in ["old", "base", "flight", "gone"]))
            self.assertEqual(mk.release_run("batch-2"), (1, 2))  # not the pick, not the in-flight file
            self.assertEqual(mk.release_run("batch-2"), (0, 0))  # repeat: nothing, no error
            mc.cache_path(url("old")).write_bytes(b"xx")
            (media / "stray.part").write_bytes(b"x")
            self.assertEqual(mk.prune(dry_run=True), (3, 5))
            self.assertEqual(mk.prune(), (3, 5))
            left = {f.name for f in media.iterdir()}
        self.assertEqual(left, {mc.cache_path(url(n)).name for n in ["base", "de", "flight", "cand"]})


class OtherSources(unittest.TestCase):
    def test_other_checkouts_app_data_and_mods_kept(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        media, work, data = d / "media", d / "work", d / "main" / "authoring" / "data"
        for p in (media, work / "media", data, d / "wt" / "authoring" / "data", d / "main" / "app" / "data" / "demo",
                  d / "main" / "mods" / "ex"):
            p.mkdir(parents=True)
        pool(data / "questions.json", [url("base")])
        pool(d / "wt" / "authoring" / "data" / "questions.json", [url("other")])
        pool(d / "main" / "app" / "data" / "demo" / "pool.json", [url("appdata")])
        pool(d / "main" / "mods" / "ex" / "questions.json", [url("mod")])
        roots = [d / "main", d / "wt", d / "missing"]
        with mock.patch.object(mk, "MEDIA", media), mock.patch.object(mc, "MEDIA", media), \
                mock.patch.object(mk, "SOURCE_POOL", data / "questions.json"), mock.patch.object(mk, "WORK", work), \
                mock.patch.object(mk, "CANDIDATES", work / "media"), mock.patch("batches.WORK", work), \
                mock.patch.object(mk, "checkout_roots", return_value=roots):
            for n in ["base", "other", "appdata", "mod", "none"]:
                mc.cache_path(url(n)).write_bytes(b"xx")
            self.assertEqual(mk.prune(), (1, 2))
            left = {f.name for f in media.iterdir()}
        self.assertEqual(left, {mc.cache_path(url(n)).name for n in ["base", "other", "appdata", "mod"]})


if __name__ == "__main__":
    unittest.main()
