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
- [ ] RG-7 More regional bundles (milestone 9, 2026-10-15; plan 98 tasks 11–15): `usa` (en, 2000, set up by task 1276, runs from task 1268), `germany` (de, 2000, set up by task 1277, runs from task 1269), `uk` (en, 2000, set up by task 1278, runs from task 1270), `spain` (es-ES, 2000, set up by task 1279, runs from task 1271), `mexico` (es, 2000, set up by task 1280, runs from task 1272).
- [x] RG-6 Regional taxonomies (pm decision 166, plan 138). *2026-10-16 (D-109): general list `authoring/data/regional-categories.json` (pm decision 213); `qgen taxonomy --bundle <id>` proposes and applies a region's list; `colombia` 14 categories, 53 subcategories (pm decision 249); `qgen remap --bundle colombia` moved its 109 questions onto it; `validate` requires a question's subcategory in its own bundle's list.*
- Pilot effort, first numbers (`colombia` batch-12, QC 2026-10-22; chain proven, chain 5 may start):
  - 239 approved, 14 needs_work (rework-7 fixed 7); spot check 28 of 30 agree (93 %), release bar ✓
  - $0.28 per approved (`qgen report --cost`, bundle row; run $12.41 plus factcheck; the bundle row's $69.26 includes earlier spend); 1659 to go → ≈ $575
  - review time: 35 min per 100 verdicts (`qgen report --review-time --bundle colombia`; only 28 timed verdicts, small sample)
  - not too costly for chain 5's pace; no decision
- Pilot effort, es done (`colombia` 2014 approved after batch-25's QC, 2026-10-24; `task 1754: Colombia pilot effort (es) recorded in 15c and 16`):
  - batches: 11 (batch-12, batch-16..25), one `qgen rework` each (rework-7, rework-9..18)
  - cost (`qgen report --cost`, bundle row): 11 runs, 1806 approved by runs, spent $643.00, $0.33 per approved; pool 2014 approved includes the 102 older ones and rework fixes
  - $ per approved per batch rises as the pool fills: $0.28 (batch-12), $0.29–0.34 (16–21), $0.38–0.40 (22–25); draft es trend $0.38 (batch-23..25)
  - yield falls: approved per batch 239 (12), 186 (16), 194, 198, 157, 170, 169, 126, 136, 117, 114 (25)
  - health ✗ trend: drop rate 25 % (batch-12) → 24–33 % (16–21) → 36–42 % (22–25); overlap rate 14.9 % ✓ (12) → 21 % (16) → 35–37 % (22, 24, 25); other ✗: merged/slots 11–15, mean fun, $ per approved above 0.35
  - review time: 35 min per 100 verdicts (`qgen report --review-time --bundle colombia`; 28 timed verdicts in 1 session, 109 untimed skipped; small sample)
  - spot checks: batch-12 answered (decision 409: 28 of 30, ≥ 90 %); batch-16..25 raised (decisions 427, 431, 435, 439, 443, 447, 449, 451, 453, 456), unanswered, nothing waits (decision 414)
  - information only: no budget or pace decision; next: `colombia` en (`qgen batch --translate en --bundle colombia`)
- `colombia` en progress: `tr-en-4` (2026-10-29) 298 translated, 292 approved, 6 needs_work, 2 not travelling; 292 of 2000 approved en; $0.08 per approved; audit 97 %, health pass; next `task 1799`.
- `colombia` en progress: `tr-en-6` (2026-10-29) 300 translated, 295 approved, 5 needs_work, 0 not travelling; 587 of 2000 approved en; $0.08 per approved; audit 98 %, health pass; next `task 1809` (see `pm show 1799`).
- `colombia` en progress: `tr-en-8` (2026-10-29) 297 translated, 288 approved, 9 needs_work, 0 rejected, 3 not travelling; 875 of 2000 approved en; $0.09 per approved; audit 98 %, health pass; next run added after `task 1809`.
- `colombia` en progress: `tr-en-10` (2026-10-29) 298 translated, 290 approved, 8 needs_work, 0 rejected, 2 not travelling; 1165 of 2000 approved en; $0.09 per approved; audit 93 %, health ✗ (overlap 1.0 %, decision raised); next run added after `task 1813`.
- `colombia` en progress: `tr-en-11` (2026-10-30) 299 translated, 281 approved, 18 needs_work, 0 rejected, 1 not travelling; 1446 of 2000 approved en; $0.10 per approved; audit 92 %, health pass; next run added after `task 1816`.
- `colombia` en progress: `tr-en-12` (2026-10-30) 299 translated, 286 approved, 13 needs_work, 0 rejected, 1 not travelling; 1732 of 2000 approved en; $0.09 per approved; audit 93 %, health ✗ (overlap 1.0 %, decision raised); next run added after `task 1819`.
