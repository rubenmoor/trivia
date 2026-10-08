# 22 — Bundles: Question Packs Players Switch On or Off

**Status:** active

A **bundle** is a named set of questions that players can switch on or off before a session. Bundles let players shape their game: a regional bundle for people with a connection to a country, thematic bundles (sports, …) for more of what they like. This replaces the `region` field planned in [15c](15c-regional-questions.md) (D-39).

## Model
- Bundles are listed in `app/data/bundles.json` (it ships; the game offers the choice, BN-6): `id`, Spanish `name` and `description` for the game, `kind` (`base`, `region`, `theme`), `always_on`, and `rule`: one English sentence the pipeline uses to decide membership.
- **Every question is in exactly one bundle**: the field `bundle`, default `"base"`.
- Bundles **add** questions; they don't own a topic. A sports question can be in `base`; a sports bundle later just adds many more. "¿Cuál es la capital de Colombia?" stays in `base`; only questions that need a real connection to Colombia go into `colombia`.
- **`base`** is always on and can't be switched off.
- A session plays the questions of the active bundles. Difficulty, age groups (D-38) and burning (D-28) work as before inside that set.

## The first bundles
| id | kind | Name | Rule (for the pipeline) |
|---|---|---|---|
| `base` | base | Básico | Everything else: answerable by the players anywhere in the Spanish-speaking world, including well-known facts about Colombia. |
| `colombia` | region | Colombia | Answering needs a connection to Colombia: places, food, customs, people, music, sport, words or history that the players outside Colombia mostly wouldn't know. |

## In the pipeline
- **Existing pool:** every question gets `bundle: "base"`; then `qgen bundles` (an LLM pass, about 20 questions per call) proposes `colombia` where the rule fits and writes it into the pool. The gamemaster checks the proposals in the review tool (`/review?bundle=colombia`) and changes any that are wrong there.
- **New questions (until BN-8):** the drafter picks the bundle by the rules (D-36's batch stays one command). The rater doesn't judge it; the gamemaster can change it in the review tool. D-41 replaces this: see "Batches per bundle".
- **Checks and output:** `validate` (bundle must exist), `export` (the game needs `bundle`), `report` (questions and supply per bundle).
- **House style:** base questions may use Colombian references that anyone in the Spanish-speaking world knows; anything more goes into `colombia`.

## Batches per bundle (D-41)
The gamemaster's direction (2026-10-07): a batch writes for **one bundle, chosen by the command**, never by the drafter.

- **Default `base`:** `qgen batch` with no arguments writes only `base` questions. The drafter no longer picks a bundle; every question of the batch gets the batch's bundle. The `base` rule still applies to the content: a question that needs a connection to Colombia doesn't belong in a base batch (the drafter skips the slot, the rater or reviewer flags it).
- **Another bundle:** `qgen batch --bundle <id>` writes only for that bundle. The RUNBOOK then allows exactly this one argument, when the user names the bundle.
- **Creating a bundle:** a separate command, e.g. `qgen bundle new <id>`, creates an **empty bundle**: its entry in `app/data/bundles.json` (name, description, kind, rule) and its own setup, independent of `base`:
  - its own **categories and subcategories** (its own `categories.json`);
  - its own **concept lists**, made by `qgen concepts` for its subcategories (the batch makes missing ones, as today);
  - possibly its own **question axes**, falling back to `base`'s `question-axes.json` when it has none.
- **Choosing subcategories:** a bundle batch picks the 30 subcategories with the fewest approved questions *in that bundle* (the same rule as today, applied to the bundle's own list).
- **Taxonomy stays per bundle:** a bundle's subcategories, concepts and axes only feed its own batches. `base`'s lists don't change when a bundle is made.

Open: OQ-41..OQ-44.

## Later
- **The game** (BN-6): a choice of bundles before a session, `base` always on; selection filters by the active bundles. Until then the game plays every bundle, as now.

## Tasks
- [x] BN-1 Decision D-39 and this plan; 15c's `region` replaced by bundles
- [x] BN-2 `app/data/bundles.json` (base, colombia); `bundle` on every question (`base`); `validate` and `export`
- [x] BN-3 `qgen bundles`: an LLM pass proposes `colombia` for existing questions and writes it. *2026-10-07: 504 questions (rejected ones skipped), 26 calls; 84 moved to `colombia`. Proposals and reasons in `work/bundles/proposals.json`. For the gamemaster to check: `/review?bundle=colombia`.*
- [x] BN-4 `draft` picks the bundle by the rules; house style explains bundles
- [x] BN-5 `report` per bundle; review tool shows the bundle, filters by it (`?bundle=`) and lets the gamemaster change it. *Key `n` moves a question to the next bundle. The server also accepts difficulty 1–15 now (D-38); the review tool's digit keys still set 1–10.*
- [ ] BN-6 The game: choose bundles before a session; selection filters by them
- [-] BN-7 `qgen batch` aimed at one bundle. *Replaced by BN-8..BN-12 (D-41).*
- [ ] BN-8 `qgen batch` writes `base` by default: `draft` sets the batch's bundle instead of picking one; prompts drop the bundle choice and keep the base rule as a content limit (D-41)
- [ ] BN-9 `qgen bundle new <id>`: creates an empty bundle (entry in `bundles.json` plus its own categories, concept and optional axes files); layout per OQ-41
- [ ] BN-10 Per-bundle categories, concept lists and axes in `qgen` (`concepts`, `draft`, `validate`, `report`, `batch-report`), with fallback to `base`'s axes
- [ ] BN-11 `qgen batch --bundle <id>`: subcategory choice inside the bundle; RUNBOOK allows exactly this argument when the user names a bundle (D-36 amended)
- [ ] BN-12 What happens to `colombia` today: its questions, and the Colombian subcategories in `base`'s `categories.json` (OQ-42)
