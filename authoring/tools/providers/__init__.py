"""Media providers (plans/23-media-providers.md, D-45). Never ship (D-35).

Each provider is a module with ID, NAME (for credits), `available()` (its key is set),
`search(query, kind, limit)` returning candidates best first, `download_url(candidate)` and
`pd_reasons(candidate)`. A candidate is a dict: type, provider, id, title, page_url, preview_url,
file_url, width, height, duration, mime, author, author_url, license, license_url, restrictions
(Commons' non-copyright restriction codes, else []), and maybe `source` (the original site,
for credits). `search` here keeps only candidates whose licence is on the allowlist, adds their
`license_kind`, and skips a provider that is cooling down after a rate limit.
"""
import re, sys, threading, time

from download import RateLimited
import progress  # authoring/tools/progress.py: the bar says what a search waits for (QG-20)
from providers import commons, freesound, nasa, openverse

PROVIDERS = {m.ID: m for m in [commons, nasa, openverse, freesound]}

# Which providers a search asks, in order, per media type (plans/23, "Which provider for which
# slot"). NASA only for space subcategories. Freesound out (D-103).
ORDER = {"image": ["commons", "nasa", "openverse"], "audio": ["commons"], "video": ["commons", "nasa"]}
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
        with progress.waiting(f"{PROVIDERS[provider].NAME} search"):
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


def pd_reasons(candidate):
    """Why a public-domain file is public domain (PD-old-70, …), at pick time; [] for other licences."""
    if licence_kind(candidate.get("license")) != "public-domain":
        return []
    return provider_of(candidate).pd_reasons(candidate)


LICENCE_FIELDS = ("provider", "license", "license_url", "author", "author_url", "restrictions", "pd_reasons")

# PD templates that hold in the US only (D-62); PD-USGov* counts as worldwide.
US_ONLY_PD = r"PD-US(?!Gov).*|PD-1923|PD-Harris-Ewing"


def licence_verdict(slot):
    """("ok" | "replace", ["code: text", …]) for a picked slot's licence record (plans/52).
    Restrictions never make a file "replace" (D-61)."""
    missing = [k for k in LICENCE_FIELDS if k not in slot]
    if missing:
        return "replace", [f"missing-data: {', '.join(missing)}"]
    reasons = []
    if slot["provider"] not in PROVIDERS:
        reasons.append(f"missing-data: unknown provider {slot['provider']}")
    for k in ("restrictions", "pd_reasons"):
        if not isinstance(slot[k], list):
            reasons.append(f"missing-data: {k} not a list")
    kind = licence_kind(slot["license"])
    if not kind:
        reasons.append(f"off-allowlist: {slot['license']}")
    elif kind == "public-domain" and isinstance(slot["pd_reasons"], list):
        if not slot["pd_reasons"]:
            reasons.append("pd-no-reason: public domain without a template")
        elif all(re.fullmatch(US_ONLY_PD, r) for r in slot["pd_reasons"]):
            reasons.append(f"pd-us-only: {', '.join(slot['pd_reasons'])}")
    return ("replace" if reasons else "ok"), reasons


def licence_fields(candidate):
    """A pick's licence record (plans/26 "Slot fields"). Commons candidates stored before plan 26
    lack author_url and restrictions: fetched in the same call as the PD templates."""
    p = provider_of(candidate)
    pd = licence_kind(candidate.get("license")) == "public-domain"
    if "restrictions" not in candidate and hasattr(p, "lookup"):
        extra = p.lookup(candidate, templates=pd)
    else:
        extra = {"author_url": candidate.get("author_url"), "restrictions": candidate.get("restrictions", []),
                 "pd_reasons": pd_reasons(candidate)}
    record = {"provider": p.ID, **{k: candidate.get(k) for k in ("license", "license_url", "author")}, **extra}
    return {k: record[k] for k in LICENCE_FIELDS}


def name(candidate):
    """Where the file comes from, for credits: "Wikimedia Commons", "Flickr via Openverse", …"""
    p = provider_of(candidate).NAME
    return f"{candidate['source']} via {p}" if candidate.get("source") else p
