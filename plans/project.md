# Project — Milestones to Completion

**Status:** living

The road from today to a finished game: milestones, every open task, every open question. The plan files stay the source of truth for each task's details and status; this file only groups and orders them. When you tick a task in its plan file, tick it here too.

**Done means:** a full game night on the living-room TV, with sound, jokers and the final look, played by player name from start to victory or defeat without touching code, and enough questions for several games per player (success criteria in [`00-vision.md`](00-vision.md)).

## Where we stand (2026-10-06)

- **Pool:** 200 questions in `data/questions.json` (190 approved, 9 rejected, 1 draft), batches `first-120` and `pilot`. 24 categories / 140 subcategories (D-19).
- **Pipeline:** `tools/qgen.py` (fit → draft → rate → factcheck → dedupe → merge, plus revise/apply, report, validate), `tools/media.py` (Commons fetch, cache sync).
- **Review tool and stats pages:** done ([`08-review-tool.md`](08-review-tool.md)).
- **Game:** a playable skeleton (D-25): server referee in `server/game.py`, screens in `client/src/game/`, unpolished parts marked `PLACEHOLDER(<task ID>)`. Players and per-player burning on the server (GF-6); the D-29 look is in place and confirmed (M3); no jokers, no sound yet.

## Milestones

| # | Milestone | Main plans | Status |
|---|-----------|-----------|--------|
| M0 | Foundations: pool, pipeline, review tool, media cache, playable skeleton | 02, 06, 07, 08 | done |
| M1 | Complete rules: players, per-player burning, gamemaster controls | 03, 05, 02 | done (B-1 waits for a decision) |
| M2 | Jokers | 09 | done (sounds: JK-9 in M4) |
| M3 | Visual design and screen polish | 10, 04 | mostly done (UI-11 tear-open, UI-7 preload left) |
| M4 | Sound, music and fireworks | 04, 09 | next |
| M5 | Enough content for game nights | 02, 07, 06 | in progress |
| M6 | Living-room ready (TV test, setup, backup) | 04, 10, backlog | todo |

Suggested order: M1 → M2 → M3 → M4 → M6, with M5 running alongside (content can be generated and reviewed at any time). M2 before M3 because the joker tray needs room in the Question layout. M3 and M4 can swap or interleave.

---

### M0 — Foundations ✅
Done. See the ticked tasks in [`02-question-pool.md`](02-question-pool.md), [`06-images.md`](06-images.md), [`07-question-generation.md`](07-question-generation.md), [`08-review-tool.md`](08-review-tool.md), and GF-2, GF-4, GF-5, UI-7 (D-25).

### M1 — Complete rules
**Goal:** the rules from D-20, D-28 are fully in place; the gamemaster can run a game, including corrections, from the admin overlay.
**Exit:** a player picks or enters a name, plays to the end, and their seen questions are burned for them only; the gamemaster can skip, skip-and-burn-for-everyone and undo.

- [x] GF-6 Players: `players` table, name on new games, burn per player plus global burn, supply and draw per player, undo per player — [`03`](03-game-flow.md)
- [x] QP-14 `burned` table gets a player column; `qgen.py report --player` — [`02`](02-question-pool.md)
- [x] GF-7 Delete a player with all their games and burns — [`03`](03-game-flow.md)
- [x] UI-16 Player screen: name list, new name, greeting; name on Start and Level — [`04`](04-ui-tv-display.md)
- [x] GF-1 Full rule set (no timer, D-30) — [`03`](03-game-flow.md)
- [x] GM-1 Choose the control method (TV keyboard + `Esc` overlay, D-30) — [`05`](05-gamemaster-controls.md)
- [x] GM-2 Define the action set (incl. skip and burn for everyone, D-28; confirmed D-30) — [`05`](05-gamemaster-controls.md)
- [x] GM-3 Decide on a GM-only view with answer and notes (no, D-30) — [`05`](05-gamemaster-controls.md)
- [x] GM-4 Implement the controls («Saltar y quemar para todos» in the overlay) — [`05`](05-gamemaster-controls.md)
- [x] UI-13 Admin overlay on `Esc` — [`04`](04-ui-tv-display.md)
- [ ] B-1 Session log: questions asked, result, date — [`backlog`](backlog.md) *(not yet accepted)*

No blocking questions left (D-30).

### M2 — Jokers
**Goal:** all five jokers (Soplo, Paso, Bájale, Cambiazo, Francotirador) work, server and client, with their animations (D-26, D-27).
**Exit:** every joker can be played on the TV; availability and reasons are correct; replaced questions are burned for the player.

- [x] JK-1 Confirm names, keys and animations (D-30) — [`09`](09-jokers.md)
- [x] JK-2 Server: `POST /api/game/joker`, availability, purge, burn, hints, history — [`09`](09-jokers.md)
- [x] JK-3 Server: Snipe — [`09`](09-jokers.md)
- [x] JK-4 Client: joker tray — [`09`](09-jokers.md)
- [x] JK-5 Client: common play animation and input lock — [`09`](09-jokers.md)
- [x] JK-6 Client: Soplo notes, Paso dialog and purge — [`09`](09-jokers.md)
- [x] JK-7 Client: card-flip swap, difficulty dial, subcategory picker — [`09`](09-jokers.md)
- [x] JK-8 Client: Francotirador — [`09`](09-jokers.md)
- [x] UI-15 Room for the joker tray and hint notes in the layouts — [`04`](04-ui-tv-display.md)
- [x] JK-10 `qgen.py report` per subcategory × difficulty — [`09`](09-jokers.md)

Depends on M1 (per-player burning). Joker sounds (JK-9) are in M4.

### M3 — Visual design and screen polish
**Goal:** the D-29 look (smaller text, glass panels, gray/dark blue) on every screen; the placeholders for visuals and animation are gone.
**Exit:** `grep -rn PLACEHOLDER client/src` lists only sound-related items (M4).

- [x] VD-1 Gamemaster confirms palette, fonts, type scale from the implementation (D-30) — [`10`](10-visual-design.md)
- [x] VD-2 Theme file: tokens, `--u`, glass classes — [`10`](10-visual-design.md)
- [x] VD-3 Ship Baloo 2 and Nunito — [`10`](10-visual-design.md)
- [x] VD-4 / UI-2 Question screen layout — [`10`](10-visual-design.md), [`04`](04-ui-tv-display.md)
- [x] VD-5 Candy buttons and answer tile states — [`10`](10-visual-design.md)
- [x] VD-6 Stage backgrounds — [`10`](10-visual-design.md)
- [x] VD-7 / UI-3 Tower: materials, drop-and-settle, crown — [`10`](10-visual-design.md), [`04`](04-ui-tv-display.md)
- [x] VD-8 SVG icon set — [`10`](10-visual-design.md)
- [x] UI-1 Visual style (confirmed, VD-1) — [`04`](04-ui-tv-display.md)
- [~] UI-4 Reveal, Correct, Wrong and Victory animations (fireworks left, UI-9) — [`04`](04-ui-tv-display.md)
- [~] UI-11 Quirky question cards with deal-in (tear-open left) — [`04`](04-ui-tv-display.md)
- [x] UI-12 Padlock animations — [`04`](04-ui-tv-display.md)
- [x] UI-14 Consolation and milestone copy in Spanish — [`04`](04-ui-tv-display.md)
- [ ] UI-7 follow-up: preload the next screen's media before fading in (`PLACEHOLDER(UI-7)`) — [`04`](04-ui-tv-display.md)

The game is called «¡Trivia!» (D-30).

### M4 — Sound, music and fireworks
**Goal:** the audio contract from D-21/D-22: three music intensities, effects, unlock on first click; fireworks.
**Exit:** no sound placeholders left; a full game sounds right at living-room volume.

- [x] UI-8 Audio engine: AudioContext, three channels, fades, gapless loops, synthesized fallbacks — [`04`](04-ui-tv-display.md)
- [ ] UI-10 Source CC0/CC BY sound assets, `client/public/audio/CREDITS.md` — [`04`](04-ui-tv-display.md)
- [ ] UI-9 Fireworks overlay, 4+ variants, finale mode — [`04`](04-ui-tv-display.md)
- [x] JK-9 Joker sounds — [`09`](09-jokers.md)
- [x] UI-13 rest: volume sliders and mute in the admin overlay — [`04`](04-ui-tv-display.md)

### M5 — Enough content for game nights
**Goal:** a pool large enough that each player gets several games, including joker use (D-27, D-28), with every approved question cached and illustrated.
**Exit:** `qgen.py report --player <name>` shows enough supply at every level for the target number of games; `qgen.py validate` is clean; `media.py sync` has filled the cache.

- [ ] OQ-17 Decide the target pool size (first, it sets the scale of QP-9)
- [~] QP-9 Second batch of questions, step by step with the gamemaster — [`02`](02-question-pool.md)
- [ ] QP-10 Gamemaster reviews the first 120 *(looks done: all are approved or rejected; tick it in 02)* — [`02`](02-question-pool.md)
- [ ] QP-6 An image for every question — [`02`](02-question-pool.md), [`06`](06-images.md)
- [~] QP-7 Validation script: image check once media is cached — [`02`](02-question-pool.md)
- [x] JK-10 Supply report per subcategory × difficulty (shared with M2): `qgen.py report --subcategories` — [`09`](09-jokers.md)

No family-specific questions (D-30).

### M6 — Living-room ready
**Goal:** the game runs on the real TV setup, offline, with state that can't get lost.
**Exit:** a dress rehearsal on the TV, then the first real game night; success criteria in `00-vision.md` ticked.

- [ ] UI-6 Test on the actual TV: overscan, resolution, distance, volume, timings — [`04`](04-ui-tv-display.md)
- [ ] VD-9 TV check: legibility, glass contrast, `backdrop-filter` performance — [`10`](10-visual-design.md)
- [ ] B-2 Backup of pool and `data/game.sqlite` — [`backlog`](backlog.md) *(not yet accepted)*
- [ ] B-3 Practice/preview mode to check questions and images on the TV — [`backlog`](backlog.md) *(not yet accepted)*
- [ ] Run `media.py sync` and `qgen.py validate` before game night (checklist item, no task ID yet)
- [ ] VIS-1 Confirm the vision with the gamemaster — [`00`](00-vision.md)

Setup: a computer on the TV via HDMI, internet available (D-30).

---

## Open questions

From [`open-questions.md`](open-questions.md), with the milestone each one blocks:

| ID | Question | Blocks |
|----|----------|--------|
| OQ-17 | Target total pool size? | M5 (QP-9) |

## Plan housekeeping

Found while gathering this list; fix them in the plan files:

- **QP-10** is still open, yet all 120 first-batch questions are approved or rejected. Tick it.
- **ARC-1** (choose the tech stack) is still open, although D-3, D-4, D-5 decided it. Tick it.
- **QG-6** (review and accept step) and **QG-12** (review page) look covered by the review tool (RV-1..RV-9). Tick or drop them.
- File statuses: `00-vision.md`, `01-architecture.md`, `05-gamemaster-controls.md` are still `stub`.
