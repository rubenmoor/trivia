"""Media providers (plans/23-media-providers.md, D-45). Never ship (D-35).

Each provider is a module with ID, NAME (for credits), `available()` (its key is set),
`search(query, kind, limit)` returning candidates best first, and `download_url(candidate)`.
A candidate is a dict: type, provider, id, title, page_url, preview_url, file_url, width,
height, duration, mime, author, license, license_url, and maybe `source` (the original site,
for credits). `search` here keeps only candidates whose licence is on the allowlist, adds their
`license_kind`, and skips a provider that is cooling down after a rate limit.
"""
import re, sys, threading, time

from media_cache import RateLimited
from providers import commons, freesound, nasa, openverse

PROVIDERS = {m.ID: m for m in [commons, nasa, openverse, freesound]}

# Which providers a search asks, in order, per media type (plans/23, "Which provider for which
# slot"). NASA only for space subcategories.
ORDER = {"image": ["commons", "nasa", "openverse"], "audio": ["commons", "freesound"], "video": ["commons", "nasa"]}
SPACE_CATEGORIES = {"espacio"}

# The allowlist (D-45): licences that allow a commercial release with credit, by family.
# Exact matches only, so NC, ND, GFDL, GPL and unknown licences never pass.
LICENCE_KINDS = [
    ("cc0", r"CC0( 1\.0)?|No restrictions"),
    ("public-domain", r"Public domain|PDM(-owner)?|Public Domain Mark( 1\.0)?"),
    ("by-sa", r"CC BY-SA \d\.\d( [a-z]{2,3})?"),
    ("by", r"CC BY \d\.\d( [a-z]{2,3})?"),
    ("attribution", r"Attribution"),  # Commons' template: free use with attribution
    ("fal", r"FAL( 1\.3)?"),
    ("pexels", r"Pexels License"),
    ("pixabay", r"Pixabay Content License"),
]

_cooldown = {}  # provider id -> time.monotonic() until which it is skipped
_cooldown_lock = threading.Lock()


def licence_kind(name):
    """The allowlist family of a licence short name, or None if it isn't allowed."""
    return next((kind for kind, pattern in LICENCE_KINDS
                 if re.fullmatch(pattern, (name or "").strip(), re.IGNORECASE)), None)


def provider_of(candidate):
    return PROVIDERS[candidate.get("provider", "commons")]  # candidates from before MP-2 are Commons'


def order(kind, category=None):
    """The providers to ask for this media type, in order, leaving out those without a key."""
    ids = [p for p in ORDER[kind] if p != "nasa" or category in SPACE_CATEGORIES]
    return [p for p in ids if PROVIDERS[p].available()]


def cooling(provider):
    with _cooldown_lock:
        return _cooldown.get(provider, 0) > time.monotonic()


def search(provider, query, kind, limit=30):
    """One provider's candidates for the query, allowlisted licences only, best first.
    Raises RateLimited when the provider is limited; it is then skipped until its Retry-After."""
    if cooling(provider):
        raise RateLimited(int(_cooldown[provider] - time.monotonic()) + 1, PROVIDERS[provider].NAME)
    try:
        found = PROVIDERS[provider].search(query, kind, limit)
    except RateLimited as e:
        with _cooldown_lock:
            _cooldown[provider] = time.monotonic() + e.retry_after
        print(f"  {PROVIDERS[provider].NAME} is rate-limited; skipped for {e.retry_after} s", file=sys.stderr)
        raise
    out = []
    for c in found:
        c["license_kind"] = licence_kind(c["license"])
        if c["license_kind"]:
            out.append(c)
    return out


def download_url(candidate):
    """The URL to download for a picked candidate (resized where the provider allows it)."""
    return provider_of(candidate).download_url(candidate)


def name(candidate):
    """Where the file comes from, for credits: "Wikimedia Commons", "Flickr via Openverse", …"""
    p = provider_of(candidate).NAME
    return f"{candidate['source']} via {p}" if candidate.get("source") else p
