# Directory

What lives where. The repo is split into what ships and what doesn't ([`plans/19-repo-layout.md`](plans/19-repo-layout.md), D-35). `authoring/` may use code from `app/`, never the other way round. If a player's install needs it, it belongs in `app/`.

## `app/`: the game, as it ships

| Path | Contents |
|---|---|
| `app/server/` | Game server, Python standard library only: `main.py` (static files, game API, `/api/save`), `save.py` (the save `state/game.json`: store, migration from `game.sqlite`), `game.py` (game rules, the referee), `selection.py` (question selection), `media_cache.py` (media cache, read-only: never downloads), `categories.py`, `paths.py`, `http_base.py` |
| `app/desktop/` | Electron shell (D-63, D-71): `main.mjs` (window, F11, `app://` protocol, offline/security rules, IPC), `resolve.mjs` (`app://` URL → file: `dist`, `/data/`, `/media?url=…`, ranges; pure, testable under `node`), `save.mjs` (the save file: atomic write, lock retry, backups, stale `.tmp`; pure `node:fs`, D-72), `preload.cjs` (bridge `window.trivia`), `package.json` + own `package-lock.json` (`electron`, `electron-builder`; not a workspace, D-73); run with `trivia-desktop`. Local builds (D-73): `electron-builder.yml`, `after-pack.mjs` (Linux `trivia` launcher, `--no-sandbox`), `stage-media.mjs` (pool media → `build/media/`); `build/`, `release/` (artefacts) gitignored; run with `trivia-desktop-build` |
| `app/client/` | Game UI: Svelte 5 + Vite + TypeScript, built to `app/client/dist/` |
| `app/client/credits.ts` | Vite plugin (PUB-5, plan 47): media, sounds, fonts, glyphs, libraries → generated `dist/credits.json` (Credits screen) and `dist/CREDITS.md` (shipped); dev serves `/credits.json`; `node.d.ts`: the Node APIs it uses (no `@types/node`) |
| `app/client/src/game/` | The game screens and their parts (stage, question, jokers, tower, fireworks, sound, copy; `levels.ts`: levels per game, D-88); `LetterPicker.svelte` + `letters.ts`: letter picker for a new name with a pad (plan 46, SW-4); `Prompt.svelte`: key or pad-glyph hint per last device, `Glyph.svelte`: pad button glyphs (IN-5); `LanguageScreen.svelte`: first-start language pick for a fresh save (plan 68); `Choice.svelte`: mode, age group and bundles before a game (plan 29, MD-7); `Customize.svelte`: «Personalizar partida», joker counts in «Solo o en grupo» (MD-7); `Reports.svelte`: «Preguntas reportadas» over the overlay (MD-6); `SupplyReport.svelte`: the pool can't fill a game (GF-5); `Credits.svelte`: Credits screen from the ☰ overlay, reads `credits.json` (PUB-5) |
| `app/client/src/lib/` | API client and types; `store.ts`: `ServerStore` (`/api/save`), `FileStore` (the desktop's save file, D-72); `desktop.ts`: the shell's bridge or null (D-71); `engine.ts`: the in-browser referee, save loading, `guessTag()` (the language guess; Steam's in milestone 10); `errors.ts`: server error codes → `error.*` catalog texts (D-57); `i18n.ts`: `t()`, `variants()`, `lang` (D-70, from the save at boot, plan 68), language endonyms; `names.svelte.ts`: `displayName()`, category/subcategory/bundle names in the question locale (plan 68); `input.svelte.ts`: action layer, keymap, scope stack, the only `keydown` listener (IN-2); `focus.ts`: spatial focus, ring, focus memory (IN-3); `gamepad.ts`: pad core, standard mapping → intents (IN-4); `gamepad.svelte.ts`: pad polling loop, `padStyle` (IN-4, IN-5) |
| `app/client/src/locales/` | UI string catalogs (D-70): `es.ts` (the source catalog, `Catalog`/`Key` types); `xx.ts`: dev-only pseudo-locale `pseudo(es)` for `?lang=xx` (LUI-2); `en.ts`: draft English catalog, dev-only `?lang=en` (LUI-3) |
| `app/client/scripts/check-literals.mjs` | `npm run check:literals -w app/client`: flags on-screen literals outside the catalog (LUI-1) |
| `app/client/src/engine/` | TS game engine (plan 12, D-58): `rng.ts` (seedable shuffle), `pool.ts` (pool and categories), `selection.ts` (port of `selection.py`), `state.ts` (save document, transactions), `save.ts` (`parseSave`, flags), `store.ts` (`Store`, `MemoryStore`), `pycompat.ts` (Python semantics), `game.ts` (referee, port of `game.py`), `outlook.ts` (fresh games left, bottleneck, exhausted subcategories, plan 65), `api.ts` (`main.py`'s game routes, `outlook`, `noteExhausted`); `*.test.ts` next to them (`npm test`, D-64), helpers in `test/` |
| `app/client/src/engine/fixtures/` | Parity fixtures of the Python referee for the TS engine (PORT-1, D-58): synthetic categories and pools, `selection.json`, `game/<scenario>.json`; format in its `README.md` |
| `app/client/public/` | Fonts and audio |
| `app/data/categories.json` | The `base` bundle's 23 broad categories and their 113 subcategories (D-19, D-43) |
| `app/data/age-groups.json` | Age groups, their windows on the shared difficulty scale 1–15 (D-38), `levels`: the 12 difficulty ranges per group the game draws from (D-68), and `level_weights`: weight per difficulty derived from `levels` (D-76) |
| `app/data/bundles.json`, `app/data/bundles/<id>/` | Question bundles (`base`, `colombia`, …, D-39); another bundle's own categories (D-43) |
| `app/data/pool.json` | The playable pool: approved questions only, generated by `qgen export` (don't edit) |
| `app/data/pool.<locale>.json` | Playable pool per translated locale (`en`, `de`): approved, non-stale translations on approved sources, generated by `qgen export` (don't edit, D-81) |
| `app/data/names.<locale>.json`, `app/data/bundles/<id>/names.<locale>.json` | Display names per locale for bundles, categories, subcategories and age groups (base's file, by id; pm decision 48); keys are the Spanish names (hand-maintained, D-81) |

## `authoring/`: tooling that never ships

| Path | Contents |
|---|---|
| `authoring/data/questions.json` | The source pool: every question with its reviews, ratings and history |
| `authoring/data/questions.<locale>.json` | Translations per locale (`en`, `de`): text fields, own `difficulty`, `status`, `review`, `source_hash` (D-81) |
| `authoring/data/concepts/`, `authoring/data/bundles/<id>/concepts/` | Concept lists per subcategory that drafts start from (D-37): `base`'s, then another bundle's (D-43) |
| `authoring/data/question-axes.json` | Question styles as axes (D-37) |
| `authoring/data/targets.json` | Pool targets per bundle: approved total and per difficulty (D-53); batch health thresholds (`batch_health`, D-55) |
| `authoring/data/health-acks.json` | The gamemaster's acks of batches failing the health thresholds (`qgen health ack`, D-55); shown in `authoring/reports/batches.md` |
| `authoring/data/spot-checks.json` | The gamemaster's blind spot checks per batch (`/review?batch=<b>&sample=1`, plan 16); written only by the authoring server |
| `authoring/tools/qgen.py` | The question pipeline (`qgen batch`, `validate`, `export`, `report`, single steps) |
| `authoring/tools/health.py` | Batch health metrics per run (`batch_health`), ✓/✗ against the thresholds, the stop of `qgen batch`, `qgen report --batches`, the Health section and `batches.md` (plan 15) |
| `authoring/tools/translations.py` | Loads/saves the locale files, `source_hash`, staleness, the entries `qgen export` writes per locale (D-81) |
| `authoring/tools/age_groups.py` | `validate`'s check of `age-groups.json`'s `levels` and `level_weights` (D-68, D-76) |
| `authoring/tools/targets.py` | Loads the pool targets (`load_targets`), derived per-category shares, `validate`'s check (D-53) |
| `authoring/tools/media.py` | Commons search, candidate storage, media sync (`trivia-media`) |
| `authoring/tools/download.py` | HTTP for the authoring tools: `http_get` (rate limits, Commons token), `cached` (download into the media cache on a miss) |
| `authoring/tools/record_fixtures.py` | Records the engine parity fixtures through `game.py`/`selection.py` (`--check`: re-record and diff); deleted with `game.py` (PORT-8) |
| `authoring/tools/engine.py`, `supply.ts` | The TS engine under Node for authoring (D-60): `supply` (supply check of `qgen report` and the start page), `simulate` (`sim/`); `package.json` makes the `.ts` files ES modules |
| `authoring/tools/save_file.py` | The game's save for authoring, read-only (D-59): players, burns, flags from `state/game.json`, before the switch-over `game.sqlite`/`flags.json`; keeps `state/flags-applied.json` |
| `authoring/tools/prompts/` | Prompts for drafting, rating, fact-checking, revising, reviewing, auditing and the house style; translation runs (D-87): `translate.md`, `translate-review.md` (added to review and audit), `locale-<locale>.md` (language and market, filled into house style's `{locale}`; `locale-es.md`: the Spanish voice) |
| `authoring/tools/` (rest) | Helpers: `batches.py`, `concepts.py`, `layout.py` (paths), `pool_export.py`, `progress.py` |
| `authoring/server/` | Authoring server on port 8001: question API for the review tool, stats, start page, spot checks (`spot_checks.py`) |
| `authoring/ui/` | Authoring UI (Svelte): `home/` start page, `review/` review tool, `stats/` stats pages, `print/` printable joker cards |
| `authoring/RUNBOOK.md` | How an LLM makes a batch of questions: one command |
| `authoring/QC.md` | Quality control after every batch: audit, blind spot check, `qgen report --qc`, findings → prompt changes (D-56, plan 16) |
| `authoring/reports/` | One generated report per batch or run (`tr-<locale>-<n>.md` for translation runs) |
| `authoring/reports/batches.md` | Generated: batch health of every batch from batch-4 on, side by side (plan 15) |

## Everything else

| Path | Contents |
|---|---|
| `plans/` | Plans, decisions, open questions, backlog; start at [`plans/README.md`](plans/README.md) |
| `CLAUDE.md` | Imports `AGENTS.md` for Claude Code |
| `AGENTS.md` | Guide for AI coding assistants |
| `flake.nix`, `flake.lock` | Dev shell and packages (D-18) |
| `package.json` | npm workspaces: `app/client`, `authoring/ui` |
| `state/` | Game saves (gitignored): `game.sqlite` (until the switch-over, then the backup), `game.json` (players, games, burns, flags; plan 49), `flags.json` (flags before the switch-over), `flags-applied.json` (flags already turned into reviews, written by `trivia-authoring`), `desktop/` (`trivia-desktop`'s save in dev: `game.json`, `backup/`; D-72) |
| `media/` | Media cache (gitignored, D-17) |
| `work/` | Pipeline work files, one folder per run (gitignored) |
| `work/tr-<locale>-<n>/` | One translation run (D-87): `run.json` (`mode: translate`, `locale`, `ids`, `stale`), `translations/`, `not-travelling.json`, the review, record and audit files |
| `work/backaudit-<k>/` | One back-audit slice (plan 57): `run.json` (ids), `audit/<id>.json`, `audit/costs.log` |
