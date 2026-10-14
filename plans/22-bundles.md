# 22 — Bundles: Question Packs Players Switch On or Off

**Status:** active

A **bundle** is a named set of questions that players can switch on or off before a session. Bundles let players shape their game: a regional bundle for people with a connection to a country, thematic bundles (sports, …) for more of what they like. This replaces the `region` field planned in [15c](15c-regional-questions.md) (D-39).

## Model
- Bundles are listed in `app/data/bundles.json` (it ships; the game offers the choice, BN-6): `id`, Spanish `name` and `description` for the game, `kind` (`base`, `region`, `theme`), `languages` (locales the bundle is offered in, D-85), and `rule`: one English sentence the pipeline uses to decide membership.
- **Every question is in exactly one bundle**: the field `bundle`, default `"base"`.
- Bundles **add** questions; they don't own a topic. A sports question can be in `base`; a sports bundle later just adds many more. "¿Cuál es la capital de Colombia?" stays in `base`; only questions that need a real connection to Colombia go into `colombia`.
- **Exactly one base bundle** (`kind: base`) per session (D-85, decision 38); `base` is the first and today the only one. Non-base bundles are off by default on the configure screen (decision 33).
- A session plays the questions of the active bundles. Difficulty, age groups (D-38) and burning (D-28) work as before inside that set.

## The first bundles
| id | kind | Name | Rule (for the pipeline) |
|---|---|---|---|
| `base` | base | Básico | Everything else: answerable by the players anywhere in the Spanish-speaking world, including well-known facts about Colombia. |
| `colombia` | region | Regional: Colombia | Answering needs a connection to Colombia: places, food, customs, people, music, sport, words or history that the players outside Colombia mostly wouldn't know. |

## In the pipeline
- **Existing pool:** every question gets `bundle: "base"`; then `qgen bundles` (an LLM pass, about 20 questions per call) proposes `colombia` where the rule fits and writes it into the pool. The developer checks the proposals in the review tool (`/review?bundle=colombia`) and changes any that are wrong there.
- **New questions:** until BN-8 the drafter picked the bundle by the rules. Since BN-8 the batch's bundle is set by the command (see "Batches per bundle"); the developer can still change it in the review tool.
- **Checks and output:** `validate` (bundle must exist), `export` (the game needs `bundle`), `report` (questions and supply per bundle).
- **House style:** base questions may use Colombian references that anyone in the Spanish-speaking world knows; anything more goes into `colombia`.

## Batches per bundle (D-41)
The developer's direction (2026-10-07): a batch writes for **one bundle, chosen by the command**, never by the drafter.

- **Default `base`:** `qgen batch` with no arguments writes only `base` questions. The drafter no longer picks a bundle; every question of the batch gets the batch's bundle. The `base` rule still applies to the content: a question that needs a connection to Colombia doesn't belong in a base batch (the drafter skips the slot, the rater or reviewer flags it).
- **Another bundle:** `qgen batch --bundle <id>` writes only for that bundle. The RUNBOOK then allows exactly this one argument, when the user names the bundle.
- **Creating a bundle:** a separate command, e.g. `qgen bundle new <id>`, creates an **empty bundle**: its entry in `app/data/bundles.json` (name, description, kind, rule) and its own setup, independent of `base`:
  - its own **categories and subcategories** (its own `categories.json`);
  - its own **concept lists**, made by `qgen concepts` for its subcategories (the batch makes missing ones, as today);
  - possibly its own **question axes**, falling back to `base`'s `question-axes.json` when it has none.
- **Choosing subcategories:** a bundle batch picks half of the bundle's subcategories (D-46), those with the fewest approved questions *in that bundle* (the same rule as today, applied to the bundle's own list).
- **Taxonomy stays per bundle:** a bundle's subcategories, concepts and axes only feed its own batches. `base`'s lists don't change when a bundle is made.

### Layout (D-43)
| What | `base` | Another bundle `<id>` |
|---|---|---|
| Categories (ship) | `app/data/categories.json` | `app/data/bundles/<id>/categories.json` |
| Pool (ship, `qgen export`, D-94) | `app/data/pool.json`, `pool.<locale>.json` (`base`'s questions only) | `app/data/bundles/<id>/pool.json`, `pool.<locale>.json`; missing = not offered (optional install, pm decision 66) |
| Names (ship) | `app/data/names.<locale>.json` | `app/data/bundles/<id>/names.<locale>.json` |
| Media | content depot | `build/pack-media.json` lists the media only it uses (`stage-media.mjs`) |
| Concept lists | `authoring/data/concepts/` | `authoring/data/bundles/<id>/concepts/` |
| Question axes | `authoring/data/question-axes.json` | `authoring/data/bundles/<id>/question-axes.json`, if present; otherwise `base`'s |

- Subcategory names and broad-category slugs are unique across all bundles (`validate`), so a subcategory names its bundle's taxonomy. Question ids are global; concept names are unique within a bundle.
- The taxonomy steers generation; `bundle` steers play. A `base` question uses a subcategory from `base`'s own list (D-49): "¿Cuál es la capital de Colombia?" is in `base` under «Capitales del mundo», not under a Colombian subcategory. A `colombia` question may still use a `base` subcategory (OQ-46).
- `app/server/categories.py` reads every bundle's categories (each broad category carries its `bundle`), and the engine's «Cambiazo» picker shows only the categories of the game's active bundles (plan 27).
- `colombia`'s list: the 27 Colombian subcategories that were in `base` (Colombia, Fiestas colombianas, Platos típicos colombianos, Selección Colombia, Palabras colombianas, …) in 6 broad categories. Their concept lists moved with them.
- A `base` batch keeps Colombia-only content out through the prompt alone (OQ-43); the developer moves the rest with `n`.

- **One house style for every bundle** (D-44): a session mixes questions from all active bundles, so a bundle's own axes may change *what* is asked, never *how* it is written.

## Player bundles (mods)
Mods carry bundles in our own format, loaded by our own loader (pm plan 115, decision 128: Bundles from mods: the shell merges bundles.json; mod ids namespaced <mod id>:<id>). Player content never mixes with our ids, seen counts, flags, reports or telemetry.
- Format: `<mod>/data/bundles.json` (rows as ours: `id`, `kind`, `languages`, `name`, `description`; `rule`, `voice`, `about` ignored); `<mod>/data/bundles/<id>/`: `categories.json`, `names.<locale>.json` (optional), `pool.json` / `pool.<locale>.json` (`version: 1`), media anywhere below; base bundles too.
- Row checks: `bundleRows()` in `app/desktop/mods.mjs` (≤ 256 KB, slugs, structure); bad row dropped, warning `bundle_row`; bad file `bundle_json`. A mod with bundles has `kind` `bundle`.
- Namespacing: bundle and question ids → `<mod id>:<id>`; `:` never in our ids: `isModId()` / `isOurs()` in `app/client/src/engine/pool.ts`.
- Merge: the shell serves one `/data/bundles.json`: ours first, then loaded mods' rows in load order, tagged `source: "mod"`, `mod`, `modName` (`app/desktop/resolve.mjs`).
- Loading: mod bundles are packs (`withPacks`) in `app/client/src/lib/data.ts`; `modPool()` namespaces, rewrites media, drops invalid questions; offered in `languages` ∩ `LOCALES` with a pool file.
- Kinds and defaults: a non-base mod bundle is a pack: off by default in every mode (decision 33, decision 158); a base mod bundle is a second choice in the base radio group, ours stays the default (decision 38). Mod removed: its bundles vanish, stored choices fall back to defaults.
- Media: relative `file_url` inside the bundle folder (`img/owl.jpg`) → `/data/bundles/<mod>:<id>/img/owl.jpg`; never downloaded; absolute URL or `..` → media dropped, `role: essential` question dropped.
- Credits (decision 129: Credits for mod media: runtime section on the Credits screen from the mod's own pool): `Credits.svelte` adds a section per loaded mod bundle from its questions' `credit` + `source_url` (deduped); `credits.json`, `CREDITS.md` stay ours.
- Marker: `BundleSelector.svelte` shows «Hecho por jugadores · {mod}» (`bundles.playerMade`); flag action hidden for mod questions.
- `modIssues()` (`lib/data.ts`, per mod and bundle, with count): `bad_question`, `bad_media`, `bad_categories`, `no_pool`, `bundle_language`, `taxonomy_clash` (until pm task 995); a broken mod bundle is left out, never breaks the load.
- Save: mod ids stored as strings, no format change; removed mods' rows ignored; `authoring/tools/save_file.py` drops ids with `:`; telemetry keeps `isOurs` only.
- Achievements: player questions count like ours except `BUNDLE_*` and `ALL_CATEGORIES` (ours only) (decision 123: Achievements in games with mods on: allowed or off?; decision 146: Achievements, mods screen and rich presence with mods on).

## Later
- **The game** (BN-6): a choice of bundles before a session, exactly one base bundle (D-38); selection filters by the active bundles. Engine: plan 27; Choice screen and overlay line: plan 29.

## Tasks
- [x] BN-1 Decision D-39 and this plan; 15c's `region` replaced by bundles
- [x] BN-2 `app/data/bundles.json` (base, colombia); `bundle` on every question (`base`); `validate` and `export`
- [x] BN-3 `qgen bundles`: an LLM pass proposes `colombia` for existing questions and writes it. *2026-10-07: 504 questions (rejected ones skipped), 26 calls; 84 moved to `colombia`. Proposals and reasons in `work/bundles/proposals.json`. For the developer to check: `/review?bundle=colombia`. 2026-10-13: checked by the developer (decision 7): 84 kept in `colombia`, 0 moved to `base`.*
- [x] BN-4 `draft` picks the bundle by the rules; house style explains bundles
- [x] BN-5 `report` per bundle; review tool shows the bundle, filters by it (`?bundle=`) and lets the developer change it. *Key `n` moves a question to the next bundle. The server also accepts difficulty 1–15 now (D-38); the review tool's digit keys still set 1–10.*
- [ ] BN-6 The game: choose bundles before a session; selection filters by them *(start screen: plan 29)*
  - 2026-10-11 engine: bundle filter and choice per game, plan 27 (`always_on` bundles always in, «Cambiazo» groups of active bundles only). Open: start screen, play-test (plans 29–30).
- [-] BN-7 `qgen batch` aimed at one bundle. *Replaced by BN-8..BN-12 (D-41).*
- [x] BN-8 `qgen batch` writes `base` by default: `draft` sets the batch's bundle instead of picking one; prompts drop the bundle choice and keep the base rule as a content limit (D-41). *The bundle is stored in `run.json`; runs without one are `base`.*
- [x] BN-9 `qgen bundle new <id>`: creates an empty bundle (entry in `bundles.json` plus its own categories, concept and optional axes files); layout per D-43. *`--name`, `--description`, `--kind`, `--rule`; writes an empty `categories.json` to fill by hand. Axes stay `base`'s until a `question-axes.json` is added.*
- [x] BN-10 Per-bundle categories, concept lists and axes in `qgen` (`concepts`, `draft`, `validate`, `report`, `batch-report`), with fallback to `base`'s axes
- [x] BN-11 `qgen batch --bundle <id>`: subcategory choice inside the bundle; RUNBOOK allows exactly this argument when the user names a bundle (D-36 amended). *Fewest approved questions of that bundle per subcategory.*
- [x] BN-12 What happens to `colombia` today: its questions, and the Colombian subcategories in `base`'s `categories.json` (OQ-42). *2026-10-08 (D-43): 27 subcategories and their concept lists moved to `colombia`; questions keep their bundle. Batch-6 checked by the rule: q-0524 (asks the flower's Colombian name) moved to `colombia`.*
- [x] BN-13 `base` questions out of `colombia`'s subcategories (D-49): 32 questions (27 approved, 2 `needs_work`, 3 rejected) move to a `base` subcategory; the 3 rejected ones are about Colombia and move to `colombia`; three new `base` subcategories; `validate` checks it. *2026-10-10, after batch-7: 29 to `base` subcategories (café, panela, Juan Valdez, Etiopía → «Bebidas»; arepas, empanada, merengón, cocadas, arroz con leche → «Comida latinoamericana»; Llorona and the superstitions → «Leyendas y supersticiones»; Bogotá → «Capitales del mundo», García Márquez → «Literatura», Shakira → «Mundiales de fútbol», Inocentes, pasos, carnavalero → «Celebraciones del mundo», the rest to the animal, plant, sea, football and language subcategories). 10 concepts added to the target lists; 7 cleared (no list yet). Cumbia (q-0071), Barranquilla (q-0133) and joropo (q-0193) → `colombia`.*
