# 05 — Gamemaster Controls

**Status:** decided (D-30)

## Purpose
The gamemaster runs the game: advance, reveal, mark right or wrong, and undo mistakes. The family must not see the answer before it is revealed.

## Options
- Keyboard shortcuts on the TV machine.
- A separate GM view (laptop or phone browser on the local network) that shows the answer and notes.
- A presenter remote / clicker.

## Tasks
- [x] GM-1 Choose the control method. *2026-10-06: keyboard and mouse of the TV machine, admin overlay on `Esc` (D-30).*
- [x] GM-2 Define the action set (next, reveal, correct, wrong, skip/replace question (burned for the player), skip and burn for everyone (D-28), undo). The admin skip doesn't count as a joker. *2026-10-06: confirmed (D-30): «Saltar pregunta», «Saltar y quemar para todos», «Deshacer», «Abandonar partida». The answer is judged automatically (D-7), so there is no "correct/wrong" button.*
- [x] GM-3 Decide whether there's a GM-only view with the answer and notes. *2026-10-06: no (D-30).*
- [x] GM-4 Implement the controls: add «Saltar y quemar para todos» to the admin overlay (the server has it, GF-6). *2026-10-06: in the `Esc` overlay, with «¿Seguro?».*
- [x] GM-5 Flag a question for review from the game (D-47): a small, faint flag button next to the ☰ (shortcut `M`, «marcar») on the Question screen and on Correct / Wrong / Victory (the question just answered). It toggles; a flagged question shows the flag filled in. The game server stores flags in `state/flags.json` (`GET /api/flags`, `POST /api/flags` with `{"id", "flagged"}`); `trivia-authoring` turns them into human `needs_work` reviews at startup. *2026-10-08: `app/server/flags.py`, routes in `app/server/main.py`, button and key in `app/client/src/game/Game.svelte`; applied by `apply_flags` in `authoring/server/main.py`.*
