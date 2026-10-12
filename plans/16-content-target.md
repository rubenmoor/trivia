# 16 — Content Target for Release

**Status:** target decided (D-75); CT-2..CT-5 open (S4)

Part of the Steam plan ([11](11-steam.md)). The release target is set per launch language (D-75): buyers judge a trivia game by how long it lasts before questions repeat, and by how often an answer is wrong.

## Where we stand (2026-10-12)
- Spanish: 1136 approved (`base` 1034, `colombia` 102); `base` target 5000 is pm milestone 1 (D-52).
- English, German: no pool yet (launch languages, pm decision 26; translation: 15b).

## What one game needs
- A game **shows** 48 cards (4 per level × 12) and **burns** at least 12, plus whatever the jokers swap away (D-27, D-28).
- Burns per mode (D-74, multipliers D-77): «Solo o en grupo» and round-robin co-op = 12 + the standard joker set's burns (3 × Soplo, 1 × each other joker); round-robin competitive ≈ N players × that; competitive (timed) ≈ 1 shared question per round, no jokers; gamemaster mode: whatever the configure screen allows.
- The tight spots are the ends of the ladder: level 1 draws only difficulty 1, and level 12 only 9–10 (D-22, D-31). Bájale and Cambiazo also need depth *per subcategory*.

## Metric
- Target metric: approved questions per launch language vs. D-53's mix (`qgen report`).
- Information only (no bar, D-75): "games per new player", CT-2. `qgen report --simulate` plays game after game per mode (burns above) and age group on the engine until the supply check fails; median and 10th percentile over many seeds. A "strong player" (always reaching level 12) gives the lower bound.

## Target (decided, D-75)
- **5000 approved per launch language** (es, en, de), with D-53's per-level mix (`authoring/data/targets.json`).
- No games-per-player number (pm decision 21). Estimate at 5000, strong player, old Normal joker budget: ≥ 80 games in every age group (bottleneck: adults, difficulty 13–15).
- Later languages (zh-Hans, ru, pt-BR, milestone 12): no target now.
- Open: whether a translated pool counts toward a language's 5000, or only once its own approved pool (re-rated, fact-checked, reviewed, 15b) meets it; follows plan 37's D-entry (OQ-31).
- The release also needs **every subcategory** to have depth at several difficulties, or it is merged into a neighbour (D-19).

## Quality bar
- Every batch: LLM audit and blind human spot check (D-56).
- Family pool (`base`, milestone 1, pm decision 2): human spot check of 30 random questions per batch (plan 16 tooling), ≥ 90 % agreement with the LLM review in each of the last two batches; plus 5000 approved, every difficulty at its target, the last two batches pass plan 15's health thresholds, `qgen validate` clean. Checked by `qgen report --exit-check`.
- Release bar and back-audit of the pre-D-56 pool (1136 approved): pm plan 57; release bar: pm decision 15.
- LLM-reviewed questions (D-33) are allowed, but the AI disclosure (17) must describe the process honestly.
- After release: «Reportar pregunta» (MD-6) plus a manual channel (ST-5) feeds fixes into patches.

## Cost
`costs.log` records the cost per generated question. A full run for 5000 questions × 3 launch languages (with translation, rating and fact-checking) needs a budget estimate before it starts (CT-3).

## Tasks
- [x] CT-1 Decide the target (OQ-32): 5000 approved per launch language, D-53's mix, no games number (2026-10-12, D-75). CT-2 (S4) reports games per player.
- [ ] CT-2 `qgen.py report --simulate` on the engine: games per new player per language, region, mode and age group; information only (D-75).
- [ ] CT-3 Cost estimate per question (draft → approved, and per translation) from `costs.log`; budget for the release.
- [ ] CT-4 Generation plan by gap: which difficulties and subcategories need the most, batch by batch.
- [ ] CT-5 Quality sampling: spot-check size and error limit per batch; `qgen.py` support for drawing the sample.
  - Family pool: closed 2026-10-11 (pm decision 2: 30 per batch, ≥ 90 % agreement; `qgen report --exit-check`). Open for the public release: pm plan 57 (release bar, back-audit).
  - Release bar: D-79 = D-56's numbers (pm decision 15); `qgen report --qc` row "release" (2026-10-12, task 336). Back-audit open.
