"""A provider's 5xx or timeout leaves the slot without candidates (errors stored); a rate limit still raises."""
import sys, tempfile, unittest, urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import qgen  # noqa: E402,F401  (import order: the command modules import each other)
import download, media, providers  # noqa: E402

SPEC = {"type": "image", "role": "essential", "query": "fruit crates market"}
Q = {"id": "q-1", "media": SPEC}


def raising(exc):
    def search(provider, query, kind):
        raise exc
    return search


class FailingProvider(unittest.TestCase):
    def fetch(self, exc, tolerate=True):
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(providers, "order", lambda kind, category: ["openverse"]), \
                mock.patch.object(providers, "search", raising(exc)), \
                mock.patch.object(media, "CANDIDATES", Path(tmp)), \
                mock.patch.object(media, "category_of", lambda q: None):
            return media.fetch_for(Q, "media", tolerate=tolerate)

    def test_server_error_and_timeout_store_no_candidates(self):
        for exc in (urllib.error.HTTPError("u", 500, "Server Error", {}, None), TimeoutError("timed out")):
            data = self.fetch(exc)
            self.assertEqual(data["candidates"], [])
            self.assertIn(str(exc), data["errors"][0])
            self.assertIn("Openverse", data["errors"][0])

    def test_not_tolerated_raises(self):
        with self.assertRaises(TimeoutError):
            self.fetch(TimeoutError("timed out"), tolerate=False)

    def test_rate_limit_still_raises(self):
        with self.assertRaises(download.RateLimited):
            self.fetch(download.RateLimited(30, "Openverse"))


class HttpGetRetry(unittest.TestCase):
    def test_one_retry_on_5xx(self):
        err = urllib.error.HTTPError("u", 500, "Server Error", {}, None)
        with mock.patch.object(download.urllib.request, "urlopen", side_effect=[err, err]) as m, \
                mock.patch.object(download.time, "sleep"):
            with self.assertRaises(urllib.error.HTTPError):
                download.http_get("http://x")
        self.assertEqual(m.call_count, 2)


if __name__ == "__main__":
    unittest.main()
