# 16 — Content Target for Release

**Status:** target decided (D-75); CT-2, CT-4 done; CT-3, CT-5 open (S4)

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
- **Pass/fail = D-75's count**: `qgen report --simulate` ends with a ✓/✗ per question locale (`es`, `es-ES`, `en`, `de`; D-78, D-107): approved in `app/data/pool.<locale>.json` (`es`: `pool.json`) vs. `targets.json` `base` (5000 + per difficulty) until part 9 sets per-locale targets. No pool = ✗. Exit 1 on any ✗; the games numbers never change it.
- Information only (no bar, D-75): "games per new player", CT-2. Headline since D-82: games until the first repeat (seen count ≥ 1 drawn), plus k (fresh games left) for a fresh profile as a cross-check (plan 65, task 426). Session after session on one save on the engine (`authoring/tools/sim/`, D-60, plan 62), selection by seen count, per locale × bundles × mode × age group × player model until the first repeat, at most 500 games (`MAX_GAMES`, capped seeds reported). Columns: median, p10, strong bound (min over seeds) of games until the first repeat; seeds whose first repeat was a Cambiazo card (random subcategory, often thin); games until a level draw repeats (median, strong bound) + `k` beside it; first-draw-repeat level + difficulty + top 3 subcategories all seen there. Default 40 seeds per cell (`--mode all --seeds 2` ≈ 10 s).
- Bundles: default = the locale's default game, its first base bundle with packs off (`base` for es, es-ES, en, de; D-99, pm decision 110); `--bundles base,colombia` for a pack. Regional packs' own 2000 target: `qgen report --bundle <id>` (plan 98 task 828), not this check.
- Player models: `strong` = always right, reaches 12 every game (lower bound); `typical` = p(right) linear 0.95 at level 1 → 0.6 at level 12 (`TYPICAL_P` in `simulate.ts`; only a model, tune from real play).
- Joker policy: standard set (D-74), each joker once at a random level; a joker the engine refuses is skipped. `gamemaster` mode not simulated.
- Modes: the engine's sessions (`milestone 16: Local multiplayer: game modes and controls`), a game = a session, players `Sim 1…N` (`--players`, default 4); `rr-coop`: turns as the engine rotates them, the team's one joker set (sees like `solo`, D-77); `rr-competitive`: every player's own game and jokers, ends at the first win; `timed`: one question per player still in per round (decision 276), every question claimed by a random player still in, right at p(level) (`strong`: always, so round 12 ends it), the clock never runs out (1 s per action). `--mode all`: 461 s vs. 210 s solo default on the same machine (2026-10-16, task 1429).

## Target (decided, D-75)
- **5000 approved per question locale** (es, es-ES, en, de; D-107), with D-53's per-level mix (`authoring/data/targets.json`).
- No games-per-player number (pm decision 21). Estimate at 5000, strong player, old Normal joker budget: ≥ 80 games in every age group (bottleneck: adults, difficulty 13–15).
- Later languages (zh-Hans, ru, pt-BR, milestone 12): no target now.
- **Regional packs:** 2000 approved each, D-53's mix scaled (`targets.json` `colombia`: 100 … 50), per locale (region's language + en); progress: `qgen report --bundle <id> [--locale L]` (D-101).
- **Theme bundles** (plan 184: `stem`, `sports`, `history`, `movies`, `geography`): 2000 approved each per question locale (es, es-ES, en, de), the same scaled mix (`targets.json`); progress: `qgen report --bundle <id> [--locale L]`.
- Translations count: a locale's 5000 = approved sources in it + its playing translations (re-rated, fact-checked, reviewed, 15b; decision 235).
- **Gap rule (D-107, pm decision 236):** English drafting for `base` aims at the largest per level over the four locales of deficit / yield − approved translatable sources not yet in that locale (`targets.draft_gaps`, `locale_gap`); theme bundles the same rule on their own deficits (plan 184); regional packs their own deficit (D-101).
- The release also needs **every subcategory** to have depth at several difficulties, or it is merged into a neighbour (D-19).

## Quality bar
- Every batch: LLM audit and blind human spot check (D-56).
- Family pool (`base`, milestone 1, pm decision 2): human spot check of 30 random questions per batch (plan 16 tooling), ≥ 90 % agreement with the LLM review in each of the last two batches; plus 5000 approved, every difficulty at its target, the last two batches pass plan 15's health thresholds, `qgen validate` clean. Checked by `qgen report --exit-check`.
- Release bar and back-audit of the pre-D-56 pool (1136 approved): pm plan 57; release bar: pm decision 15.
- LLM-reviewed questions (D-33) are allowed, but the AI disclosure (17) must describe the process honestly.
- After release: «Reportar pregunta» (MD-6) plus a manual channel (ST-5) feeds fixes into patches.
- Patches (ST-5, [`11`](11-steam.md) "Content updates (ST-5)"): new approved questions per language, fixed questions, dropped ones by status; monthly, only if ≥ 100 new approved per launch language or a reported fix waits; hotfixes any time (decision 96).

## Cost
`costs.log` records the cost per generated question. A full run for 5000 questions × 4 question locales (English drafts plus three translations each, with translation, rating and fact-checking) needs a budget estimate before it starts (CT-3).
- pm plan 70: `qgen report --cost` (CT-3), per-locale deficits + `es` source shortfall for `en`/`de` (CT-4, pm decision 37; the shortfall replaced by English drafting for the four question locales' deficits, D-107, pm decision 236), release budget per language as a pm decision after the translation pilot, before full runs.
- `qgen report --cost [--json]` (task 461): $ per run (own log + `audit/`), draft $/approved (last 3 batches, weighted), translation $/approved per locale, overhead ratio, projection per language, spent vs. `targets.json` `"budget"`.
- `qgen report --cost` also lists rows per regional bundle (× es, en) and per theme bundle (× en drafting, × es, es-ES, de translations): deficit to its target (a theme's en row: its draft gap), $/approved of its own runs, else base's rate (marked `*`) (plan 184).
- Numbers 2026-10-12 (list price): batch-4..7 $0.16 / $0.37 / $0.30 / $0.24 per approved; draft $0.26 (batch-5..7); overhead $129 (concepts $65, tighten $38, rework $6, pilot/first-120 $16, bundles $2, audit $3) / batches $183 = 0.70; `es` 3966 to go → ~$1750; `en`/`de` no pilot yet; spent $343 (`es`, incl. batch-8 in progress $31); batch-3's cost unknown (no `work/`).
- Numbers 2026-10-21 (`qgen report --cost`, list price, information only, no budget; task 1506): translation $/approved per direction: pilots `tr-en-1` (es → en) $0.12, `tr-de-1` (es → de) $0.14, `tr-es-ES-1` (es → es-ES) $0.11, `tr-es-1` (en → es) $0.11; per locale with full runs: es $0.11, es-ES $0.09, en $0.10, de $0.10; en drafts $0.26 (batch-9..11), es drafts $0.23; overhead 0.24 of batch cost. Projection to base targets: es 2945 to go ≈ $412, es-ES 4655 ≈ $527, en 1506 translations ≈ $186, de 4657 ≈ $567, en drafts ≈ $163.
- Numbers 2026-10-24 (`colombia` es pilot, 2014 approved; details in `plans/15c-regional-questions.md` "Pilot effort, es done"): 11 batches, spent $643.00, $0.33 per approved (batch-12 $0.28 → batch-22..25 $0.38–0.40 as overlap rises, drop rate 25 % → 41 %); review time 35 min per 100 verdicts (28 timed verdicts, small sample); information only.

## Tasks
- [x] CT-1 Decide the target (OQ-32): 5000 approved per launch language, D-53's mix, no games number (2026-10-12, D-75). CT-2 (S4) reports games per player.
- [x] CT-2 `qgen.py report --simulate` on the engine: games per new player per language, region, mode and age group; information only (D-75). (2026-10-12, task 412: `authoring/tools/engine.py`, `qgen.py` `report --simulate`; default matrix 56 s; es today: adults typical ≈ 68 solo games, strong 28; exit 1: es 1136/5000, en/de no pool.)
- [ ] CT-3 Cost estimate per question (draft → approved, and per translation) from `costs.log`; budget for the release.
- [x] CT-4 Generation plan by gap: which difficulties and subcategories need the most, batch by batch. *2026-10-12, task 462 (D-84): deficits per locale + `es` source shortfall (`targets.py`), read by `draft` and the subcategory ranking; `qgen report --locale L`, `--simulate`'s target check and `--cost` use them. `--translate`'s weight: plan 66 follow-up. Source shortfall replaced by D-107 (English drafting by the four locales' deficits; plan 148 task 1236).*
- [ ] CT-5 Quality sampling: spot-check size and error limit per batch; `qgen.py` support for drawing the sample.
  - Family pool: closed 2026-10-11 (pm decision 2: 30 per batch, ≥ 90 % agreement; `qgen report --exit-check`). Open for the public release: pm plan 57 (release bar, back-audit).
  - Release bar: D-79 = D-56's numbers (pm decision 15); `qgen report --qc` row "release" (2026-10-12, task 336). Back-audit open.
