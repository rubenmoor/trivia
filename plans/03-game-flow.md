# 03 — Game Flow & Rules

**Status:** draft

## Known
- Family (one team) vs. gamemaster.
- 12 questions to victory.

## Rules (D-20)
- The game is a ladder of **12 levels**. Players start at level 1 (easiest) and must answer all 12 **in a row**. Difficulty rises with the level.
- Before each level, the players choose **one of 4 questions**, shown only by their `description` (D-8).
- The players pick an answer, can change it until they confirm, and then confirm it as their final answer.
- **A wrong final answer ends the game.** There are no lives.
- Only the question that was actually asked is burned. The 3 descriptions that weren't chosen, and skipped questions (admin overlay), go back to the pool.

## Flow
The screen states and transitions are in `04-ui-tv-display.md` (Start → Level → Select → Question → Correct/Wrong → … → Victory).

## Question selection (GF-2, draft)
- Map level to difficulty (1–10): proposal `round(1 + (level − 1) × 9 / 11)` → 1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10 (OQ-23).
- The 4 candidates are approved, unburned questions at the target difficulty (±1 if there are too few), preferably from 4 different broad categories, and from categories not already asked in this game.

## To define (see open-questions.md)
- Jokers or lifelines? Timer? (OQ-4; hints: OQ-15)
- The answer is judged automatically (multiple choice, D-7). The gamemaster can undo it from the admin overlay.

## Tasks
- [~] GF-1 Write the full rule set. *2026-10-06: core rules in D-20; jokers/timer/hints still open.*
- [ ] GF-2 Define the question-selection algorithm (difficulty curve, category mix, skip burned).
- [x] GF-3 Define the screen states and transitions. *2026-10-06: `04-ui-tv-display.md`, D-21.*
- [ ] GF-4 Implement the game state machine (server-side state in SQLite, so a reload resumes the game).
