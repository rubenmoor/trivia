# Project — Milestones

**Status:** living

The road from today onward: milestones, every open task, every open question. The plan files stay the source of truth for each task's details and status; this file only groups and orders them. When you tick a task in its plan file, tick it here too.

**The family game is done (2026-10-07).** It is living-room ready: a full game night on the TV with sound, jokers and the final look, played by player name without touching code (success criteria in [`00-vision.md`](00-vision.md)). From here on there are three kinds of work:
1. **Content** (M5): more and better questions, media for every question.
2. **Groundwork** (M7–M10): changes that are useful on their own and don't change how the family plays. The Steam release needs them too, but none of them is Steam-specific.
3. **Steam** (separate track, [`11-steam.md`](11-steam.md), D-34): everything that only matters for a public release.

## Where we stand (2026-10-07)

- **Pool:** 428 questions in `authoring/data/questions.json`: 412 approved (190 reviewed by the gamemaster, 222 by Claude, D-33), 6 `needs_work`, 9 rejected, 1 draft. Batches `first-120`, `pilot`, `batch-3`, `batch-4`. 24 categories / 140 subcategories (D-19). Exported for the game to `app/data/pool.json` (D-35).
- **Difficulty supply (approved):** 1: 25 · 2: 37 · 3: 56 · 4: 55 · 5: 65 · 6: 79 · 7: 47 · 8: 24 · 9: 22 · 10: **2**. The top of the ladder is thin (level 12 draws only 9–10).
- **Media:** 290 approved questions have a picked file; 122 don't (115 in `batch-3`, 7 in `pilot`).
- **Pipeline:** one command, `qgen batch` (D-36, [`authoring/RUNBOOK.md`](../authoring/RUNBOOK.md)); repo split into `app/` (ships) and `authoring/` (doesn't), both packaged by the flake (D-35, [`19`](19-repo-layout.md)).
- **Game:** complete. Server referee in `app/server/game.py`; screens in `app/client/src/game/`. One placeholder left: `PLACEHOLDER(UI-7)` (preloading).

## Milestones

| # | Milestone | Main plans | Status |
|---|-----------|-----------|--------|
| M0 | Foundations: pool, pipeline, review tool, media cache, playable skeleton | 02, 06, 07, 08 | done |
| M1 | Complete rules: players, per-player burning, gamemaster controls | 03, 05, 02 | done |
| M2 | Jokers | 09 | done |
| M3 | Visual design and screen polish | 10, 04 | done (UI-7 preload left) |
| M4 | Sound, music and fireworks | 04, 09 | done (remaining sounds synthesized, fine for now) |
| M5 | Enough content for game nights | 02, 07, 06 | in progress |
| M7 | Game engine in TypeScript | 12 | todo |
| M8 | Mouse everywhere and a joker budget | 14, 13 | done (2026-10-07) |
| M9 | UI strings in a catalog; region tags | 15a, 15c | todo |
| M10 | Media license audit | 17 | todo |

(M6, living-room ready, is done and closed. Milestone numbers aren't reused.)

Suggested order: M5 keeps running alongside everything. M10 is small and independent, so it can go next. M7 is the biggest; MD-1 and RG-1 work on either engine, so M8 and M9 don't have to wait for it. A family test night closes M7 (PORT-7).

---

### Done: M0–M4
Every task is ticked in its plan file: [`02`](02-question-pool.md), [`03`](03-game-flow.md), [`04`](04-ui-tv-display.md), [`05`](05-gamemaster-controls.md), [`06`](06-images.md), [`07`](07-question-generation.md), [`08`](08-review-tool.md), [`09`](09-jokers.md), [`10`](10-visual-design.md), [`19`](19-repo-layout.md). Leftovers:

- [ ] UI-7 follow-up: preload the next screen's media before fading in (`PLACEHOLDER(UI-7)`) — [`04`](04-ui-tv-display.md)
- [~] UI-10 Sound assets: the music loops, whooshes, pops and joker sounds are still synthesized (fine for now, gamemaster 2026-10-06); Kenney.nl CC0 packs are the next source to try — [`04`](04-ui-tv-display.md)

### M5 — Enough content for game nights
**Goal:** a pool large enough that each player gets several games, including joker use (D-27, D-28), with every approved question cached and illustrated.
**Exit:** `qgen report --player <name>` shows enough supply at every level for the target number of games; `qgen validate` is clean; `trivia-media sync` has filled the cache.

- [ ] OQ-17 Decide the target pool size (it sets how many more batches to run)
- [~] QP-9 More batches: `qgen batch`, one per run (D-36) — [`02`](02-question-pool.md), [RUNBOOK](../authoring/RUNBOOK.md)
- [ ] QP-6 An image for every question: 122 approved questions have no picked media (115 in `batch-3`, 7 in `pilot`) — [`02`](02-question-pool.md), [`06`](06-images.md)
- [~] QP-7 Validation script: image check once media is cached — [`02`](02-question-pool.md)
- [ ] Gamemaster decides the 6 `needs_work` questions (q-0256, q-0338, q-0369, q-0384, q-0388, q-0420) and the old pilot draft q-0198 in the review tool (RUNBOOK: an LLM doesn't touch them)
- [ ] Top up difficulties 9–10 (only 24 approved, 2 at 10) — [`backlog`](backlog.md) B-6
- [x] PE-1..PE-5 Fewer Claude calls and tokens per batch (grouped rate and revise, kept fact-checks, per-subcategory avoid list, compact JSON) — [`20`](20-pipeline-efficiency.md)
- [ ] PE-6 Compare the first batch with PE-1..PE-5 against batch-4 and batch-5 — [`20`](20-pipeline-efficiency.md)
- [ ] PE-7..PE-12 Concept lists per subcategory and question styles as axes; `draft` draws concepts and axis combinations by code, after PE-6 — [`20`](20-pipeline-efficiency.md)
- [ ] PE-13 Compare the first concept-based batch against the PE-6 batch — [`20`](20-pipeline-efficiency.md)

No family-specific questions (D-30).

### M7 — Game engine in TypeScript
**Goal:** the game referee moves from Python to `app/client/src/engine/` with the same rules and the family's saves kept. The game then runs without Python, which also lets it run in a desktop shell later.
**Exit:** the family plays a test night on the TS engine; `app/server/game.py` and the game routes are gone; `trivia` serves static files plus `/api/save`.

- [ ] PORT-1 Scenario recorder for `app/server/game.py` + `selection.py`; commit the fixtures — [`12`](12-client-engine.md)
- [ ] PORT-2 `engine/selection.ts`, fixture-tested — [`12`](12-client-engine.md)
- [ ] PORT-3 `engine/game.ts`: state machine, players, burning, jokers, undo; decision: the client holds the answer (relaxes D-25) — [`12`](12-client-engine.md)
- [ ] PORT-4 Store interface; `ServerStore` + `GET/PUT /api/save`; `MemoryStore` — [`12`](12-client-engine.md)
- [ ] PORT-5 Migration `game.sqlite` → `game.json`, tested on a copy of the real save — [`12`](12-client-engine.md)
- [x] PORT-6 Pool export `app/data/pool.json` (done as LP-3) — [`12`](12-client-engine.md)
- [ ] PORT-7 Screens switch to the engine; family test night — [`12`](12-client-engine.md)
- [ ] PORT-8 Delete `game.py` and the game routes; update `01-architecture.md` and AGENTS.md — [`12`](12-client-engine.md)

### M8 — Mouse everywhere and a joker budget
**Goal:** every keyboard action also has a clickable control; the gamemaster can set a joker budget per game, so the printed cards become optional. The family's default stays unlimited, so nothing changes unless the gamemaster opts in.
**Exit:** a whole game can be played with the mouse alone; «Como las cartas» works from the overlay.

- [x] IN-1 Every keyboard action clickable (menu button for `Esc`, «Continuar», «Atrás»/«Cancelar»); the rule goes into `04` — [`14`](14-input.md)
- [x] MD-1 Joker budget in the game state (`null` = unlimited, the default) — [`13`](13-game-modes.md)
- [x] MD-2 A spent joker is disabled with a reason — [`13`](13-game-modes.md)
- [x] MD-3 Count badges on limited jokers, none when unlimited — [`13`](13-game-modes.md)
- [x] MD-4 Overlay: set the budget (unlimited / «Como las cartas» / custom) — [`13`](13-game-modes.md)

### M9 — UI strings in a catalog; region tags
**Goal:** every on-screen string comes from a catalog, with no visible change; every question says whether it's universal or Colombian.
**Exit:** no Spanish literals left in `app/client/src/game` outside the catalog; every question has `region`, checked by `validate`.

- [ ] LUI-1 `t()` helper and the `es` catalog; move every string into it — [`15a`](15a-ui-translation.md)
- [ ] LUI-2 Pseudo-locale for length and missing-string tests — [`15a`](15a-ui-translation.md)
- [ ] LUI-3 Draft `en` catalog with English joker names — [`15a`](15a-ui-translation.md)
- [ ] RG-1 `region` in the schema (`null` default) and `validate` — [`15c`](15c-regional-questions.md)
- [ ] RG-2 Tag the pool: LLM proposals, gamemaster checks in the review tool — [`15c`](15c-regional-questions.md)

### M10 — Media license audit
**Goal:** the full license data of every media file is known and stored, and files with unclear licenses (PD-US only, GFDL, flagged) are replaced.
**Exit:** `validate` requires license data for approved questions; the audit's replacement list is empty.

- [ ] PUB-1 `media.py licenses` report; list the files to replace — [`17`](17-publishing.md)
- [ ] PUB-2 Full license data per media item in the pool; `validate` requires it — [`17`](17-publishing.md)
- [ ] PUB-3 Replace the problem files in the review tool — [`17`](17-publishing.md)

---

### Steam track (separate, D-34)
Everything that only matters for a release on Steam (desktop shell, controller, game modes for players without a gamemaster, translations, content target, store and Steamworks) lives in [`11-steam.md`](11-steam.md), phases S2–S6. It builds on M7–M10. Its first phase, **S2**, is answering OQ-29..OQ-37 (below).

### Backlog
Not yet accepted, see [`backlog.md`](backlog.md): B-1 session log, B-2 backup of the save, B-3 practice/preview mode, B-5 reworded duplicates in `dedupe`, B-6 top-up for difficulties 9–10.

---

## Open questions

From [`open-questions.md`](open-questions.md), with what each one blocks:

| ID | Question | Blocks |
|----|----------|--------|
| OQ-17 | Target total pool size? | M5 (how many batches) |
| OQ-29 | Desktop shell (Electron recommended) | Steam S3 (18) |
| OQ-30 | Default mode: joker presets, checkpoints, admin actions | Steam S2 (13) |
| OQ-31 | Launch languages and Spanish variety | Steam S2 (15, 16) |
| OQ-32 | Content target for release | Steam S4 (16) |
| OQ-33 | Price model; Steamworks account holder | Steam S5 (17) |
| OQ-34 | Store name | Steam S5 (17) |
| OQ-35 | Code and content license | Steam S2 (17) |
| OQ-36 | Audience: families only or an adult track | Steam S2 (13, 16) |
| OQ-37 | Competitive mode and couch co-op format and input | Steam later (13, 14) |
| OQ-38 | Concept list size per subcategory | PE-8 (20) |
| OQ-39 | Question axes: values; axes for existing questions | PE-7, PE-11 (20) |
| OQ-40 | Concept overlap across subcategories: synonyms | PE-8 (20) |
