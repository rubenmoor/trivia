# 16 — Content Target for Release

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). The family's pool target is open too (OQ-17). A public release needs its own, higher target, set per language: buyers judge a trivia game by how long it lasts before questions repeat, and by how often an answer is wrong.

## Where we stand (2026-10-07)
404 approved questions in Spanish (batches pilot, first-120, batch-3, batch-4), 24 categories / 140 subcategories (D-19). About 290 of them have media with a credit; the rest wait for QP-6.

## What one game needs
- A game **shows** 48 cards (4 per level × 12) and **burns** at least 12, plus whatever the jokers swap away (D-27, D-28). The default mode's joker budget (13) makes this predictable: at most 12 + Paso + Bájale + Cambiazo + Snipe hits.
- The tight spots are the ends of the ladder: level 1 draws only difficulty 1, and level 12 only 9–10 (D-22, D-31). Bájale and Cambiazo also need depth *per subcategory*.
- Competitive mode (13) burns for every player in the game at once, so it multiplies the need.

## Metric
"Games per new player": simulate a new player playing game after game with a typical joker use (the default preset) and random answers that reach a realistic level, until the supply check fails. `qgen.py report --simulate` does this on the engine (12) for a language and region setting, and reports the median and the 10th percentile over many seeds. Losing early burns fewer questions, so a "strong player" setting (always reaching level 12) gives the lower bound.

## Target (to decide, OQ-32)
- Draft for discussion: **≥ 30 games per new player** at the strong-player bound in every launch language, **≥ 50** for the primary language. Very roughly 2,000–3,000 approved questions per language, with the difficulty mix of D-31. The simulation replaces this guess.
- The release also needs **every subcategory** to have depth at several difficulties, or it is merged into a neighbour (D-19).

## Quality bar
- A public product needs a lower error rate than family play. Draft: every question passes the fact-check with certainty (D-32's rule), plus a **human spot check** of a random sample per batch (e.g. 10 %). If the sample shows an error rate above an agreed limit, the batch goes back to review.
- LLM-reviewed questions (D-33) are allowed, but the AI disclosure (17) must describe the process honestly.
- After release: «Reportar pregunta» (MD-6) plus a manual channel (ST-5) feeds fixes into patches.

## Cost
`costs.log` records the cost per generated question. A full run for 3,000 questions × N languages (with translation, rating and fact-checking) needs a budget estimate before it starts (CT-3).

## Tasks
- [ ] CT-1 Decide the target (OQ-32) once the simulation exists.
- [ ] CT-2 `qgen.py report --simulate` on the engine: games per new player per language, region and preset.
- [ ] CT-3 Cost estimate per question (draft → approved, and per translation) from `costs.log`; budget for the release.
- [ ] CT-4 Generation plan by gap: which difficulties and subcategories need the most, batch by batch.
- [ ] CT-5 Quality sampling: spot-check size and error limit per batch; `qgen.py` support for drawing the sample.
