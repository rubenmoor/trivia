# 00 — Vision

**Status:** implemented

## Goal
A fun, good-looking trivia game for family evenings, played on the living-room TV.

## Core facts (agreed)
- Runs locally and offline in the living room. The source code and question pool are public on GitHub; media files are not committed (D-17).
- Players: the family as **one team** against the **gamemaster** (the author).
- Win condition: answer **12 questions** correctly (exact rules: see `03-game-flow.md`).
- The players have **jokers** (hint, skip, easier, other category, snipe) to get past hard questions (D-26, `09-jokers.md`).
- Every question has a related **background image**.
- A reusable **question pool** supports many sessions. Each game is played under a **player name**; questions a player has seen are **burned** for that player (D-28).

## Constraints
- Runs on a single machine connected to a TV (1080p / 4K, viewed from the couch).
- Should keep working with a flaky internet connection or none at all (see `06-images.md`).
- Low maintenance. Content (questions) matters more than features.

## Non-goals
- Online multiplayer, accounts, publishing, monetisation.
- Mobile app stores.

*2026-10-07: a Steam release is now planned as a separate track (D-34, [`11-steam.md`](11-steam.md)). These non-goals still describe the family game; the Steam track has its own goals.*

## Success criteria
*2026-10-07: met. The gamemaster declared the game living-room ready.*
- [x] A full game of 12 questions runs from start to finish without touching code.
- [x] The text is readable from the couch, and the images look good.
- [x] The pool holds enough unburned questions for several sessions.

## Tasks
- [x] VIS-1 Confirm the vision with the gamemaster after the open questions are resolved. *2026-10-07: the family game is done as described here.*
