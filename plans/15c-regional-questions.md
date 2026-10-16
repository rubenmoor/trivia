# 15c — Regional Questions

**Status:** superseded by [22](22-bundles.md) (D-39): regions are bundles (`colombia`), one bundle per question, no `region` field.

Sub-plan of [15](15-i18n.md). The pool was written for two Colombian kids (D-6), so some questions are about Colombia (Valle de Cocora, Colombian food, history, music) and are easy for them but hard or unfair elsewhere. Regions make those questions an opt-in pack instead of a problem, and they open the door to more regional packs later.

## Model
- `region` on every question: `null` = universal, or an ISO 3166 code (`"co"`). Maybe a list later, e.g. a question about the Andes for `co`, `pe`, `ec`.
- The player picks regions in the settings (15): "universal" is always on, and the default is the region of the UI language's main market (to decide: probably no regions by default outside Spanish).
- **Difficulty is rated for players of that region** (a Colombian kid for `co`). Outside the region the question isn't shown, so it never needs a second rating.
- **Today's game stays:** the gamemaster mode defaults to "universal + Colombia", so nothing changes for current players.
- **Packs:** a region is a set of questions with a name and a flag («Regional: Colombia»). It could later be a free DLC or update; Steam handles DLC as extra depots (18).
- **Supply per region:** `qgen.py report --region co` shows how many games a pack adds; a pack on its own doesn't need to fill a whole game, because it mixes into the universal pool.

## Tasks
- [x] RG-1 Add `region` to the schema (`null` default) and `validate`. *Done as BN-2 (D-39): `bundle` instead of `region`.*
- [x] RG-2 Tag the existing pool: an LLM pass proposes `co` or `null` per question, and the developer checks the proposals in the review tool (filter by proposed region). *Done as BN-3 (D-39): `qgen bundles`, `/review?bundle=colombia`.*
- [x] RG-3 Region filter in the selection (engine, 12) and in `qgen.py report`. *Done as BN-6 (engine plan 27, screen plan 29, close-out plan 30) and plan 62's `qgen report --simulate --bundles`.*
- [x] RG-4 `qgen.py draft --region co`: generate regional questions on purpose. *Done as BN-11: `qgen batch --bundle <id>`.*
- [x] RG-5 Decide which regional packs come next (by launch language). *2026-10-14 (D-99, pm decision 110): every regional bundle 2000 approved, region's language + en, free DLC, off by default, bundle-scoped taxonomy; pilot `colombia`, more packs (`mexico`, `argentina`) by a decision after it; work in pm plan 98.*
- [ ] RG-7 More regional bundles (milestone 9, 2026-10-15; plan 98 tasks 11–15): `usa` (en, 2000, set up by task 1276, runs from task 1268), `germany` (de, 2000, set up by task 1277, runs from task 1269), `uk` (en, 2000, set up by task 1278, runs from task 1270), `spain` (es-ES, 2000, set up by task 1279, runs from task 1271), then `mexico`.
- [x] RG-6 Regional taxonomies (pm decision 166, plan 138). *2026-10-16 (D-109): general list `authoring/data/regional-categories.json` (pm decision 213); `qgen taxonomy --bundle <id>` proposes and applies a region's list; `colombia` 14 categories, 53 subcategories (pm decision 249); `qgen remap --bundle colombia` moved its 109 questions onto it; `validate` requires a question's subcategory in its own bundle's list.*
