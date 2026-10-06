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

## Question selection (GF-2)
The question difficulty (1–10, D-6) is a rating, not a level. Each game level draws from a **range** of difficulties (D-22):

| Level | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Difficulty | 1 | 2–3 | 3–5 | 4–6 | 4–6 | 4–6 | 5–7 | 6–8 | 6–9 | 7–10 | 8–10 | 9–10 |

- Every level offers **exactly 4** questions: approved, unburned, with a difficulty in the level's range.
- Draft rules for picking the 4: prefer 4 different broad categories, and categories not already asked in this game. A question offered earlier in the same game is not offered again, so a game shows 48 different descriptions.
- «Saltar pregunta» (admin overlay) needs one more candidate from the same range.
- **Supply check:** before a new game starts, the server checks that all 12 levels can be filled this way. The ranges overlap, so the check assigns questions level by level, starting with the narrowest ranges (level 1, then 12, 11, 2…). If the check fails, the Start screen tells the gamemaster which levels lack questions and which difficulties to add; the game doesn't quietly fall back to fewer cards. `qgen.py report` shows the same supply per level (GF-5).
- Pool sizing (OQ-17): one game burns 12 questions but needs 48 unburned ones (+ spares for skips), with the most pressure on difficulties 4–6 (levels 4–6 each need 4, plus overlap with levels 3 and 7) and on difficulty 1 (level 1 alone).

## To define (see open-questions.md)
- Jokers or lifelines? Timer? (OQ-4; hints: OQ-15)
- The answer is judged automatically (multiple choice, D-7). The gamemaster can undo it from the admin overlay.

## Tasks
- [~] GF-1 Write the full rule set. *2026-10-06: core rules in D-20; jokers/timer/hints still open.*
- [ ] GF-2 Define the question-selection algorithm (difficulty curve, category mix, skip burned).
- [x] GF-3 Define the screen states and transitions. *2026-10-06: `04-ui-tv-display.md`, D-21.*
- [ ] GF-5 Supply check per level (server, before a new game) and the same report in `qgen.py report`.
- [ ] GF-4 Implement the game state machine (server-side state in SQLite, so a reload resumes the game).
