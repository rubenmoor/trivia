# 23 — Media Providers Beyond Commons

**Status:** draft

The pipeline finds all media on Wikimedia Commons (D-13). Commons' rate limits are now the bottleneck of `qgen batch`: the `media`, `research` and `sync` steps wait for minutes. Besides, Commons is weak in two places: good-looking wide photos for decorative images (≥ 1920 px, landscape) and sounds beyond animals and single instruments. This plan adds free providers next to Commons (D-45). Paid providers come later, only for gaps the free ones can't fill (see "Later: paid providers").

## Rules (D-45)
- **Licence allowlist:** a candidate is only used if its licence allows a commercial release with credit: CC0 and "No restrictions", public domain (incl. the Public Domain Mark), CC BY and Commons' "Attribution", CC BY-SA, FAL (Free Art License), the Pexels License, the Pixabay Content License; national CC ports (`CC BY-SA 3.0 de`, `igo`) count as their family. **Never** NC, ND, GFDL, GPL or "editorial use only"; an unknown or missing licence is out too. The check is in code (`providers.licence_kind`), per candidate, before the review sees it. `PD-US`-only files go on the replacement list (`providers.licence_verdict`, D-62, plan 52).
- **Credit everything,** even where the licence doesn't require it: author · licence · provider, as today (06, "Credits on screen").
- **Terms that need hotlinking are out:** the game plays from a local cache (D-17), so a provider that forbids keeping copies (Unsplash's API guidelines) isn't used.
- **No songs, film or TV clips, game footage**: unchanged from D-13. A new provider doesn't change what may be asked.
- **Keys** live in the gitignored `.env.local` (like `COMMONS_ACCESS_TOKEN`, IMG-15). A provider without its key is skipped; the pipeline still runs on Commons alone.
- **Only the authoring tools** talk to providers. The game only downloads picked files by URL, as now; the cache stays keyed by URL (D-17), whatever the host.

## Providers (free)

| Provider | What for | Licence filter | Account / key | Limits (as published) |
|---|---|---|---|---|
| Wikimedia Commons | everything, as now | per file; add the allowlist check | done (`COMMONS_ACCESS_TOKEN`) | Phase-2 limits; higher with the token |
| **Openverse** | images collected from Flickr, Smithsonian, museums and others. Most are Flickr's 1024 px size: enough for essential images (800 px), rarely for decorative ones (1920 px). Its audio is mostly music (Jamendo, ccMixter), which D-13 rules out, so audio isn't used | `license=cc0,pdm,by,by-sa`; `excluded_source=wikimedia` (Commons is asked directly) | none to start; registering through the API (name, description, email) raises the limit | anonymous 20/min, 200/day (response headers, 2026-10-08); registered 10,000/day |
| Pexels (paused) | decorative and illustrative photos; short videos | all content is under the Pexels License | free account, then an API key at pexels.com/api. *2026-10-08: new keys are paused* | 200/h, 20,000/month; more on request |
| **Freesound** | sounds: nature, machines, everyday noises | only `Creative Commons 0` and `Attribution`; at most 60 s | free account, then an API key at freesound.org/apiv2/apply (`FREESOUND_API_KEY`) | token auth is enough for the 128 kbps MP3 previews, which is what the game plays. The API is free for non-commercial use; commercial apps need a licence: out of the audio order before release (D-103); its 2 picks dropped, q-0752 and q-1016 → needs_work (pm decision 184) |
| **NASA Image and Video Library** | space: photos and videos (MP4), only for the Espacio category | NASA media is mostly public domain; items credited to someone other than NASA (a company, ESA, a news agency) are skipped | none | generous |
| Pixabay (later) | decorative photos, videos | Pixabay Content License | free account; key on pixabay.com/api/docs | a normal key gets 1280 px at most, below the 1920 px for decorative images; full access (1920 px and originals) on request |

Not used: Unsplash (requires hotlinking), xeno-canto (mostly CC BY-NC-SA), iNaturalist (mostly NC). The Met, Smithsonian and other museums come through Openverse, so they need no adapter of their own.

## Which provider for which slot
`find_candidates` asks providers in a fixed order per slot and stops once it has `MAX_CANDIDATES` (6). A provider that is rate-limited is **skipped for that search** instead of waited for. This is what removes the bottleneck; a later search tries it again.

| Slot | Order |
|---|---|
| image (any role) | Commons → NASA (Espacio only) → Openverse |
| audio | Commons (D-103) |
| video | Commons → NASA (Espacio only); then images as now |

Commons stays first: its file descriptions are precise, its images are large, and the review prompt is tuned on it. Each provider is asked with the shortened query variants until there are 3 candidates; the next provider is asked only while there are fewer (this spares Openverse's daily limit and keeps Commons' results as they were wherever Commons has enough). At most 6. When Pexels or Pixabay come, they go first for decorative images, which only need to look good and not give anything away.

A provider that answers 429 is put on cooldown for its `Retry-After`, so later searches skip it without asking. A search that ends with no candidates because a provider was skipped fails, so a rerun retries it instead of storing an empty result.

## Data
- **Candidate** (`work/media/<qid>.json`): today's fields plus `provider` (`commons`, `openverse`, `pexels`, `freesound`, `nasa`, `pixabay`), the provider's own `id`, and `license_kind`, the allowlist family (`cc0`, `public-domain`, `by`, `attribution`, `by-sa`, `fal`, `pexels`, `pixabay`). `license` stays the provider's short name as shown in credits (`CC BY-SA 3.0 de`), `license_url` its link. `author_url` (the author's page, may be null) and `restrictions` (Commons' non-copyright restriction codes from extmetadata `Restrictions`, else `[]`; plan 26); candidates stored before plan 26 lack both. Candidates stored before MP-2 have no `provider` and count as `commons`.
- **Pool media and background:** `provider`, `license`, `license_url`, `author`, `author_url`, `restrictions` and `pd_reasons` next to `source_url`, `file_url` and `credit` (plan 26). This is the same data PUB-2 (17) needs. Existing picks migrated once (task 113).
- **`validate`:** every picked slot of an approved question has the full licence record and a licence from the allowlist (error).
- **Credit:** `credit_of` names the provider ("… · Pexels") instead of the fixed "Wikimedia Commons".

## Code
- `authoring/tools/providers/`: one small module per provider with `search(query, kind, limit) → [candidate]` and `download_url(candidate)` (for resizing: Commons `iiurlwidth`, Pexels `?w=`, Pixabay `largeImageURL`, Freesound `previews["preview-hq-mp3"]`). Standard library only (`urllib`), like `media.py`.
- `media.py` keeps the shared parts: `query_variants`, `acceptable`, author limits, contact sheets, `pick_fields`. Commons' code moves into `providers/commons.py` with no change in behaviour (MP-2).
- One throttle per provider (minimum interval, `RateLimited` per provider). `download.http_get` (`authoring/tools/download.py`, D-90) stops naming Commons in its rate-limit message; the bearer token stays limited to Commons' API URL.
- The review tool shows the provider and licence on each candidate; the search modal searches all providers by the same order.
- Prompts (`house-style.md` "Media", `draft.md`, `review.md`, `rate.md`, `revise.md`, `concepts-facets.md`): "Wikimedia Commons" becomes "the media sources", with one line per provider on what it is good for. The rules on essential media stay strict: a clear, recognisable photo or sound of exactly that thing.
- Shipped formats ≠ cache formats (SW-9, D-104): the cache (`media/`, `trivia-media sync`) keeps each provider's file as downloaded; only the desktop build re-encodes (WebP, Opus, WebM) under `shippedName`; keys (`file_url`, D-17) and `cacheName` unchanged, so providers need nothing for shipping.

## How to check it worked (MP-11)
Compare the first batch with providers against batch-6: time spent in `media`/`research`/`sync`, the share of "no adequate media" `needs_work`, picks per provider, and the developer's media rejections in the review tool.

## Later: paid providers
Only for gaps the free ones leave, and only once a Steam release is real (11): exact animal sounds (Macaulay Library, per-clip licence), stock photos (Adobe Stock, Shutterstock; the standard licence caps copies at 500,000 and excludes "editorial use only" images), music and effects (check each provider's terms for games). Each needs its own licence record per file; that is what PUB-2's fields are for.

## Tasks
- [x] MP-1 Decision D-45 and this plan
- [x] MP-2 Provider modules: move Commons into `authoring/tools/providers/commons.py`; candidates get `provider`, `id` and `license_kind`; the allowlist check; otherwise no change in what is found. *2026-10-08: `providers/__init__.py` (registry, allowlist `licence_kind`, `search`, `download_url`, `name`), `providers/commons.py` (API, throttle, search, resize). `media.py` keeps the shared parts with the same functions for its callers. A live search returns the same candidates and credits as the stored ones; of ~3,500 stored candidates the allowlist would drop 10 (GFDL, GPL, OGL, none).*
- [x] MP-3 Per-provider throttle; a rate-limited provider is skipped for the current search; provider order per slot. *2026-10-08: `providers.ORDER`, cooldown per provider from `Retry-After`; `media_cache.http_get(…, headers, wait)`; a search left empty by a limit raises so a rerun retries.*
- [x] MP-4 Openverse (images); anonymous, with optional `OPENVERSE_CLIENT_ID`/`OPENVERSE_CLIENT_SECRET` for the higher limit. *2026-10-08: `providers/openverse.py`; credits name the original site ("Flickr via Openverse").*
- [ ] MP-5 Pexels (images, videos), once new API keys are issued again
- [x] MP-6 Freesound (audio previews). *2026-10-08: `providers/freesound.py`, `FREESOUND_API_KEY`; CC0 and CC BY only, ≤ 60 s, the HQ MP3 preview. 2026-10-14: dropped before release (D-103, plan 42); out of `providers.ORDER["audio"]` since task 1051; its 2 picks dropped (pm decision 184); the module stays, unasked.*
- [x] MP-7 NASA Image and Video Library (space photos and videos, Espacio only; third-party items skipped). *2026-10-08: `providers/nasa.py`; videos as MP4 (`~large`). The third-party check reads the credit fields only: footage filmed by a company but credited to NASA staff still gets through, so the review has to watch for it.*
- [x] MP-8 Pool fields `provider`, `license`, `license_url`, `author` per picked slot; migrate existing picks; `validate` checks the allowlist; credit names the provider (shared with PUB-2). *Done in pm plan 26 (tasks 111–113): 1,202 picks migrated on 2026-10-11.*
- [x] MP-9 Review tool: provider and licence on candidates; search modal over all providers. *2026-10-08; the LLM review also sees each candidate's source.*
- [x] MP-10 Prompts: "the media sources" instead of Commons only. *2026-10-08: house style lists the sources; Freesound allows everyday sounds too.*
- [x] MP-11 Compare the first batch with providers against batch-6. *2026-10-11, `qgen report --batches` (pm plan 15). batch-7 vs. batch-6: needs_work for media 7.3 → 7.0 % of merged (guessed from feedback); picks: Commons 602, Openverse 2, Freesound 2 (batch-6: Commons 84). The providers barely change what gets picked; media share fell 25.6 → 13.8 %. Time per step wasn't recorded; `qgen batch` writes it to `run.json` from batch-8 on. Developer media rejections: not counted.*
- [ ] MP-12 Pixabay, once full API access (≥ 1920 px) is granted
