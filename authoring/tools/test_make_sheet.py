"""make_sheet: an empty cached or downloaded preview is a dead thumbnail, never handed to magick."""
import hashlib, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import media  # noqa: E402


def cand(url):
    return {"type": "image", "preview_url": url, "provider": "commons"}


def cache_file(thumbs, url):
    return thumbs / (hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ".img")


class EmptyPreview(unittest.TestCase):
    def test_empty_cached_refetched_and_empty_download_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            thumbs = tmp / "thumbs"
            thumbs.mkdir()
            cache_file(thumbs, "u1").write_bytes(b"")  # cut-off earlier download
            fetch = {"u1": b"", "u2": b"img"}
            with mock.patch.object(media, "http_get", lambda u: fetch[u]), \
                    mock.patch.object(media.providers, "provider_of", lambda c: mock.Mock(NAME="X")), \
                    mock.patch.object(media.subprocess, "run", return_value=mock.Mock(returncode=0)) as run:
                shown = media.make_sheet([cand("u1"), cand("u2")], tmp / "out.png", thumbs)
            self.assertEqual(shown, [2])
            self.assertFalse(cache_file(thumbs, "u1").stat().st_size)
            self.assertNotIn(str(cache_file(thumbs, "u1")) + "[0]", run.call_args[0][0])
            self.assertEqual(cache_file(thumbs, "u2").read_bytes(), b"img")


if __name__ == "__main__":
    unittest.main()
