# 16 — Content Target for Release

**Status:** target decided (D-75); CT-2, CT-4, CT-5 done; CT-3 open (S4)

Part of the Steam plan ([11](11-steam.md)). The release target is set per question locale (D-75; `en`, `es`, `es-ES`, `de` since D-107): buyers judge a trivia game by how long it lasts before questions repeat, and by how often an answer is wrong.

## Where we stand (2026-10-12)
- Spanish: 1136 approved (`base` 1034, `colombia` 102); `base` target 5000 is pm milestone 1 (D-52).
- English, German: no pool yet (launch languages, pm decision 26; translation: 15b).
- Since D-107 (2026-10-16): `base` drafts in English from batch-9; `es`, `es-ES`, `de` get those by translation, `en`, `de`, `es-ES` the es sources (≤ batch-8).

## What one game needs
- A game **shows** 48 cards (4 per level × 12) and **sees** at least 12 (seen counters, D-82), plus whatever the jokers swap away (D-27).
- Seen events per mode (D-74, multipliers D-77, timed D-80): «Solo o en grupo» and round-robin co-op = 12 + the standard joker set's skips and swaps (3 × Soplo, 1 × each other joker); round-robin competitive ≈ N players × that; competitive (timed) ≈ N questions per round (N players), up to 12 rounds, fewer after drop-outs, no jokers; gamemaster mode: whatever the configure screen allows.
- The tight spots are the ends of the ladder: level 1 draws only difficulty 1, and level 12 only 9–10 (D-22, D-31). Bájale and Cambiazo also need depth *per subcategory*.

## Metric
- Target metric: approved questions per question locale vs. D-53's mix (`qgen report --locale L`): sources in L + playing translations into L (`targets.approved_entries`, decision 235).
- **Pass/fail = D-75's count**: `qgen report --simulate` ends with a ✓/✗ per question locale (`es`, `es-ES`, `en`, `de`; D-78, D-107): approved in `app/data/pool.<locale>.json` (`es`: `pool.json`) vs. `targets.json` `base` (6000 + per difficulty) until part 9 sets per-locale targets. No pool = ✗. Exit 1 on any ✗; the games numbers never change it.
- Information only (no bar, D-75): "games per new player", CT-2. Headline since D-82: games until the first repeat (seen count ≥ 1 drawn), plus k (fresh games left) for a fresh profile as a cross-check (plan 65, task 426). Session after session on one save on the engine (`authoring/tools/sim/`, D-60, plan 62), selection by seen count, per locale × bundles × mode × age group × player model until the first repeat, at most 500 games (`MAX_GAMES`, capped seeds reported). Columns: median, p10, strong bound (min over seeds) of games until the first repeat; seeds whose first repeat was a Cambiazo card (random subcategory, often thin); games until a level draw repeats (median, strong bound) + `k` beside it; first-draw-repeat level + difficulty + top 3 subcategories all seen there. Default 40 seeds per cell (`--mode all --seeds 2` ≈ 10 s).
- Bundles: default = the locale's default game, its first base bundle with packs off (`base` for es, es-ES, en, de; D-99, pm decision 110); `--bundles base,colombia` for a pack. Regional packs' own 2000 target: `qgen report --bundle <id>` (plan 98 task 828), not this check.
- Player models: `strong` = always right, reaches 12 every game (lower bound); `typical` = p(right) linear 0.95 at level 1 → 0.6 at level 12 (`TYPICAL_P` in `simulate.ts`; only a model, tune from real play).
- Joker policy: standard set (D-74), each joker once at a random level; a joker the engine refuses is skipped. `gamemaster` mode not simulated.
- `qgen report --career [--subjects <file>] [--locale …] [--age-group …] [--player …] [--players N] [--seeds N] [--games N] [--json]` (`plan 193: Career design: subjects, grades and badge list`): career supply figures from `authoring/tools/sim/career.ts`, the same engine sessions; base bundle; bands 1–4, 5–8, 9–12, 13–15 (`BANDS`); players 1, 2, 4 taking turns at solo games on one save (shared seen list, figures and games per player); per category (or subject) × band, exact and "or harder": static approved, correct per game, distinct before the first repeat, games to 25/50/100/200 correct (every answer / distinct). Defaults 3 seeds × 100 games per cell, full matrix ≈ 43 min (≈ 11 min per locale, 2026-11-04, task 1885). A run's output: `work/career/supply-categories.md`.
- Modes: the engine's sessions (`milestone 16: Local multiplayer: game modes and controls`), a game = a session, players `Sim 1…N` (`--players`, default 4); `rr-coop`: turns as the engine rotates them, the team's one joker set (sees like `solo`, D-77); `rr-competitive`: every player's own game and jokers, ends at the first win; `timed`: one question per player still in per round (decision 276), every question claimed by a random player still in, right at p(level) (`strong`: always, so round 12 ends it), the clock never runs out (1 s per action). `--mode all`: 461 s vs. 210 s solo default on the same machine (2026-10-16, task 1429).

## Target (decided, D-75)
- **6000 approved per question locale** (es, es-ES, en, de; D-107), with D-53's per-level mix (`authoring/data/targets.json`).
- No games-per-player number (pm decision 21). Estimate at 5000, strong player, old Normal joker budget: ≥ 80 games in every age group (bottleneck: adults, difficulty 13–15).
- Later languages (zh-Hans, zh-Hant, milestone 12): no target now; ru, pt-BR no longer planned.
- **Regional packs:** 2000 approved each, D-53's mix scaled (`targets.json` `colombia`: 100 … 50), per locale (region's language + en); progress: `qgen report --bundle <id> [--locale L]` (D-101).
- **Theme bundles** (plan 184: `stem`, `sports`, `history`, `movies`, `geography`): 2000 approved each per question locale (es, es-ES, en, de), the same scaled mix (`targets.json`); progress: `qgen report --bundle <id> [--locale L]`. Shipping rule (decision 520): none of the five ships before all five have 2000+ approved (`plans/22-bundles.md` "Shipping non-base bundles").
- Translations count: a locale's 6000 = approved sources in it + its playing translations (re-rated, fact-checked, reviewed, 15b; decision 235).
- **Gap rule (D-107, pm decision 236):** English drafting for `base` aims at the largest per level over the four locales of deficit / yield − approved translatable sources not yet in that locale (`targets.draft_gaps`, `locale_gap`); theme bundles the same rule on their own deficits (plan 184); regional packs their own deficit (D-101).
- The release also needs **every subcategory** to have depth at several difficulties, or it is merged into a neighbour (D-19).

## Quality bar
- Every batch: LLM audit and blind human spot check (D-56).
- Family pool (`base`, milestone 1, pm decision 2): human spot check of 30 random questions per batch (plan 16 tooling), ≥ 90 % agreement with the LLM review in each of the last two batches; plus 6000 approved, every difficulty at its target, the last two batches pass plan 15's health thresholds, `qgen validate` clean. (The check tool was removed, decision 760.)
- Release bar (D-79, pm decision 15): `quality.spot_check_size` 30, `quality.min_agreement` 0.9 in `targets.json`, D-56's numbers; `qgen report --qc` row "release". Applies to drafted batches (`base` in any source language, regional bundles) and back-audit slices; translation runs (`tr-*`) have no spot check and no release row (milestone 9, 2026-10-16): a translation counts through its source question's batch. Reported only, stops nothing (decision 414).
- Back-audit of the pre-D-56 pool (pm plan 57; pm decision 415: all, slices of 200; `qgen audit --backlog`, opus, `authoring/reports/backaudit-<k>.md`): 1039 audited, 99 major findings (9.5 %), $51.49 (≈ $0.050 per question); nothing stays unaudited. All six spot checks are pending, so no slice has a release row yet; they stay the developer's at `trivia-release-check`.

| Slice | Size | Batches | Major (flagged) | Cost | Spot check | Release row |
|---|---|---|---|---|---|---|
| backaudit-1 | 100 | pilot 73, first-120 27 | 19 (19 %) | $3.77 | pending (decision 203) | spot check pending |
| backaudit-2 | 200 | first-120 87, batch-3 107, batch-4 6 | 16 (8 %) | $10.04 | pending (decision 419) | spot check pending |
| backaudit-3 | 200 | batch-4 89, batch-5 75, batch-6 36 | 19 (10 %) | $9.88 | pending (decision 420) | spot check pending |
| backaudit-4 | 200 | batch-6 41, batch-7 159 | 12 (6 %) | $10.25 | pending (decision 421) | spot check pending |
| backaudit-5 | 200 | batch-7 200 | 23 (12 %) | $10.49 | pending (decision 422) | spot check pending |
| backaudit-6 | 139 | batch-7 139 | 10 (7 %) | $7.06 | pending (decision 423) | spot check pending |
- LLM-reviewed questions (D-33) are allowed, but the AI disclosure (17) must describe the process honestly.
- After release: «Reportar pregunta» (MD-6) plus a manual channel (ST-5) feeds fixes into patches.
- Patches (ST-5, [`11`](11-steam.md) "Content updates (ST-5)"): new approved questions per language, fixed questions, dropped ones by status; monthly, only if ≥ 100 new approved per launch language or a reported fix waits; hotfixes any time (decision 96).

## Cost
`calls.jsonl` records the cost per generated question. A full run for 5000 questions × 4 question locales (English drafts plus three translations each, with translation, rating and fact-checking) needs a budget estimate before it starts (CT-3).
- pm plan 70: `qgen report --cost` (CT-3), per-locale deficits + `es` source shortfall for `en`/`de` (CT-4, pm decision 37; the shortfall replaced by English drafting for the four question locales' deficits, D-107, pm decision 236), release budget per language as a pm decision after the translation pilot, before full runs.
- `qgen report --cost [--json]` (task 461): $ per run (own log + `audit/`), draft $/approved (last 3 batches, weighted), translation $/approved per locale, overhead ratio, projection per language, spent vs. `targets.json` `"budget"`.
- `qgen report --cost` also lists rows per regional bundle (× es, en) and per theme bundle (× en drafting, × es, es-ES, de translations): deficit to its target (a theme's en row: its draft gap), $/approved of its own runs, else base's rate (marked `*`) (plan 184).
- Numbers 2026-10-12 (list price): batch-4..7 $0.16 / $0.37 / $0.30 / $0.24 per approved; draft $0.26 (batch-5..7); overhead $129 (concepts $65, tighten $38, rework $6, pilot/first-120 $16, bundles $2, audit $3) / batches $183 = 0.70; `es` 3966 to go → ~$1750; `en`/`de` no pilot yet; spent $343 (`es`, incl. batch-8 in progress $31); batch-3's cost unknown (no `work/`).
- Numbers 2026-10-21 (`qgen report --cost`, list price, information only, no budget; task 1506): translation $/approved per direction: pilots `tr-en-1` (es → en) $0.12, `tr-de-1` (es → de) $0.14, `tr-es-ES-1` (es → es-ES) $0.11, `tr-es-1` (en → es) $0.11; per locale with full runs: es $0.11, es-ES $0.09, en $0.10, de $0.10; en drafts $0.26 (batch-9..11), es drafts $0.23; overhead 0.24 of batch cost. Projection to base targets: es 2945 to go ≈ $412, es-ES 4655 ≈ $527, en 1506 translations ≈ $186, de 4657 ≈ $567, en drafts ≈ $163.
- Numbers 2026-10-24 (`colombia` es pilot, 2014 approved; details in `plans/15c-regional-questions.md` "Pilot effort, es done"): 11 batches, spent $643.00, $0.33 per approved (batch-12 $0.28 → batch-22..25 $0.38–0.40 as overlap rises, drop rate 25 % → 41 %); review time 35 min per 100 verdicts (28 timed verdicts, small sample); information only.

- Media-first sources in es (plan 205): 2026-11-16, task 2111: `tr-es-18`, 168 translated, 161 approved, 7 need work, 0 not travelling, $0.11 per approved translation (audit $3.31), audit agreement 75 %; 77 of 79 approved media-first sources (batch-78, batch-79) now in es.
- Media-first sources in es (plan 205): 2026-11-16, task 2121: `tr-es-19`, 74 translated, 71 approved, 3 need work, 0 not travelling, $0.12 per approved translation (audit $3.35), audit agreement 55 %, health ✗; 145 of 146 approved media-first sources (batch-78, batch-79, batch-80) now in es.
- Media-first sources in es (plan 205): 2026-11-16, task 2129: `tr-es-20`, 66 translated, 64 approved, 2 need work, 0 not travelling, $0.12 per approved translation (audit $3.36), audit agreement 38.3 %, health ✗; all approved media-first sources (batch-78 to batch-81) now in es.
- Media-first sources in es (plan 205): 2026-11-17, task 2183: `tr-es-21`, 53 translated, 51 approved, 2 need work, 0 not travelling, $0.12 per approved translation (audit $3.02), audit agreement 34 %, health ✗; all approved media-first sources (batch-78 to batch-82) now in es.
- Media-first sources in es-ES (plan 205): 2026-11-17, task 2184: `tr-es-ES-28`, 53 translated, 49 approved, 4 need work, 0 not travelling, $0.12 per approved translation (audit $2.99), audit agreement 45 %, health ✗; all approved media-first sources (batch-78 to batch-82) now in es-ES.
- Media-first sources in de (plan 205): 2026-11-17, task 2185: `tr-de-27`, 58 translated, 49 approved, 9 need work, 0 not travelling, $0.13 per approved translation (audit $3.36), audit agreement 26 %, health ✗; all approved media-first sources (batch-78 to batch-82) now in de.
- Media-first sources in es-ES (plan 205): 2026-11-17, task 2130: `tr-es-ES-27`, 68 translated, 66 approved, 2 need work, 0 not travelling, $0.12 per approved translation (audit $3.37), audit agreement 40.0 %, health ✗; all approved media-first sources (batch-78 to batch-81) now in es-ES.
- Media-first sources in de (plan 205): 2026-11-17, task 2131: `tr-de-26`, 71 translated, 64 approved, 7 need work, 0 not travelling, $0.13 per approved translation (audit $3.50), audit agreement 26.7 %, health ✗; all approved media-first sources (batch-78 to batch-81) now in de.
- Media-first sources in es-ES (plan 205): 2026-11-16, task 2122: `tr-es-ES-26`, 74 translated, 69 approved, 5 need work, 0 not travelling, $0.11 per approved translation (audit $3.35), audit agreement 37 %, health ✗; about 146 of 146 approved media-first sources (batch-78, batch-79, batch-80) now in es-ES.
- Media-first sources in es-ES (plan 205): 2026-11-16, task 2112: `tr-es-ES-25`, 184 translated, 177 approved, 7 need work, 0 not travelling, $0.11 per approved translation (audit $3.33), audit agreement 63.3 %, health ✗; 78 of 79 approved media-first sources (batch-78, batch-79) now in es-ES.

## Tasks
- [x] CT-1 Decide the target (OQ-32): 5000 approved per launch language, D-53's mix, no games number (2026-10-12, D-75). CT-2 (S4) reports games per player.
- [x] CT-2 `qgen.py report --simulate` on the engine: games per new player per language, region, mode and age group; information only (D-75). (2026-10-12, task 412: `authoring/tools/engine.py`, `qgen.py` `report --simulate`; default matrix 56 s; es today: adults typical ≈ 68 solo games, strong 28; exit 1: es 1136/5000, en/de no pool.)
- [ ] CT-3 Cost estimate per question (draft → approved, and per translation) from `calls.jsonl`; budget for the release.
- [x] CT-4 Generation plan by gap: which difficulties and subcategories need the most, batch by batch. *2026-10-12, task 462 (D-84): deficits per locale + `es` source shortfall (`targets.py`), read by `draft` and the subcategory ranking; `qgen report --locale L`, `--simulate`'s target check and `--cost` use them. `--translate`'s weight: plan 66 follow-up. Source shortfall replaced by D-107 (English drafting by the four locales' deficits; plan 148 task 1236).*
- [x] CT-5 Quality sampling: spot-check size and error limit per batch; `qgen.py` support for drawing the sample. *2026-10-24, plan 57: bar 30 / ≥ 90 %, back-audit 1039 questions, 99 major (9.5 %), $51.49; spot checks pending.*
  - Family pool: closed 2026-10-11 (pm decision 2: 30 per batch, ≥ 90 % agreement). Open for the public release: pm plan 57 (release bar, back-audit).
  - Release bar: D-79 = D-56's numbers (pm decision 15); `qgen report --qc` row "release" (2026-10-12, task 336). Back-audit open.
- Media-first sources in de (plan 205): 2026-11-16, task 2113: `tr-de-25`, 258 translated, 250 approved, 8 need work, 0 not travelling, $0.11 per approved translation (audit $3.38), audit agreement 57 %, health ✗; 145 of 146 approved media-first sources (batch-78, batch-79, batch-80) now in de.
- Media-first sources in es (plan 205): 2026-11-17, task 2188: `tr-es-22`, 55 translated, 53 approved, 2 need work, 0 not travelling, $0.12 per approved translation (audit agreement 40.0 %, health ✗); all approved media-first sources (batch-78 to batch-83) now in es.
- Media-first sources in es-ES (plan 205): 2026-11-17, task 2189: `tr-es-ES-29`, 57 translated, 56 approved, 1 need work, 0 not travelling, $0.12 per approved translation, audit agreement 40.0 %, health ✗; all approved media-first sources (batch-78 to batch-83) now in es-ES.
- Media-first sources in de (plan 205): 2026-11-17, task 2190: `tr-de-28`, 62 translated, 55 approved, 7 need work, 0 not travelling, $0.14 per approved translation, audit agreement 26.7 %, health ✗; all approved media-first sources (batch-78 to batch-83) now in de.
- Media-first sources in es (plan 205): 2026-11-18, task 2193: `tr-es-23`, 54 translated, 53 approved, 1 need work, 0 not travelling, $0.12 per approved translation (audit agreement 37 %, health ✗); all approved media-first sources (batch-78 to batch-84) now in es.
- Media-first sources in es-ES (plan 205): 2026-11-18, task 2194: `tr-es-ES-30`, 53 translated, 52 approved, 1 need work, 0 not travelling, $0.11 per approved translation, audit agreement 34 %, health ✗; all approved media-first sources (batch-78 to batch-84) now in es-ES.
- Media-first sources in de (plan 205): 2026-11-18, task 2195: `tr-de-29`, 59 translated, 52 approved, 7 need work, 0 not travelling, $0.14 per approved translation, audit agreement 22 %, health ✗; all approved media-first sources (batch-78 to batch-84) now in de.
- Media-first sources in de (plan 205): 2026-11-18, task 2198: `tr-de-30`, 55 translated, 49 approved, 6 need work, 0 not travelling, $0.14 per approved translation, audit agreement 33 %, health ✗; all approved media-first sources (batch-78 to batch-85) now in de.
- Media-first sources in es (plan 205): 2026-11-18, task 2201: `tr-es-24`, 102 translated, 101 approved, 1 need work, 0 not travelling, $0.12 per approved translation, audit agreement 48.3 %, health ✗; all approved media-first sources (batch-78 to batch-86) now in es.
- Media-first sources in es-ES (plan 205): 2026-11-18, task 2202: `tr-es-ES-31`, 102 translated, 101 approved, 1 need work, 0 not travelling, $0.10 per approved translation, audit agreement 51.7 %, health ✗; all approved media-first sources (batch-78 to batch-86) now in es-ES.
- Media-first sources in de (plan 205): 2026-11-18, task 2203: `tr-de-31`, 59 translated, 53 approved, 6 need work, 0 not travelling, $0.13 per approved translation, audit agreement 28.8 %, health ✗; all approved media-first sources (batch-78 to batch-86) now in de.

## chinese-base media budget (2026-11-20, task 2324)
- Fresh staging (`node stage-media.mjs` after `trivia-media sync --status approved`: 5 files were missing from the cache, 4 `colombia`, 1 `base`), then `stage-media.mjs --check`: ✗ 1 failure.
  - ✓ content 6147 files / 5637 MB (no size line, decision 653), incl. base pack chinese-base 950 files; zh fonts 6.8 of 8 MB, audio 6.1 of 7 MB, horizon 0.5 of 2 MB
  - ✗ `3bfc6750e872574b.webm` 32.2 MB > `video` 32 MB: q-20957 (`base`, not chinese-base); 30 s at the 8 Mbit/s ceiling + audio + VP9 overshoot; can recur with new videos → `decision 805: Shipped videos: one 30 s clip encodes to 32.2 MB, over the 32 MB per-video line: raise the line, tighten the encode, or re-encode only files over it?`: `video` line raised to 34 MB, encode unchanged (2026-11-21)
  - fixed: `.mpg` videos shipped unencoded (227.5 MB and 57.2 MB); `resolve.mjs` `SHIPPED` now maps `.mpg`/`.mpeg` → WebM: 4.1 and 6.3 MB
- chinese-base now: 962 approved in en (50 each in zh-Hans, zh-Hant), all with media; 950 distinct files: 948 shared with `base` (copies, plan 227), 2 own (`6a32fb75660fb57b.webp` 1.1 MB, `fa5e1b1bdaf04690.webp` 0.9 MB); 479 MB in all. zh pools reuse the same files.
- Estimate at 6000 per locale: ~5040 new en questions. Base: 0.84 MB per approved (5619 MB / 6724; images 3205 MB, audio 128 MB, video 291 clips 2619 MB). chinese-base so far 0.50 MB per approved (fewer videos). Own files ≈ 2.5 GB (chinese-base mix) to ≈ 4.2 GB (base mix, every question its own file); zh adds none.
- No total line for the content depot (decision 653): the only budget that bit is the per-video line, now 34 MB (decision 805).
- After decision 805 (2026-11-21): `stage-media.mjs --check` ✓, 0 failures; largest video 32.2 MB of 34 MB.
- Recheck on a fresh staging once part 7's new questions land.

## chinese-base drafting close-out (2026-11-26, task 2388)
- `qgen report --bundle chinese-base --locale en`: 6338 approved in en (copies + new) of 6000, 106 %; every difficulty 98–140 % of target except level 15 (124 / 150, missing 26).
  - 36 short at levels 1 (6), 3 (4) and 15 (26): closed as is (`decision 826`); ahead of target elsewhere.
  - Subcategory mix: new China subcategories mostly 56–88 % of their derived share (nature-of-china, chinese-sport, geography-of-china, chinese-science); reused `base` categories 100–176 %. Guide only, no stop.
- `qgen report --simulate --locale en --bundles chinese-base`: the full run (all age groups × both players, 40 seeds) hits the 1800 s per-cell timeout; narrowed `--age-group young_teens --seeds 10`: 412 s, strong median 61 games, bound 36; typical median 43, p10 15; k 193.
  - Its D-75 target check reads the locale's first base bundle (`base`), not `--bundles` → ✗ on `base` (6214/6000, short at 3–9, 11); follow-up task. `chinese-base` itself ends short by the 36 above, so ✗ there too until reworked.
