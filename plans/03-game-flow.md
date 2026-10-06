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
- **Jokers (D-26, D-27):** on the Question screen, the players can play jokers, as often as they like: «Soplo» (reveal the next hint), «Paso» (skip, optionally purging the whole subcategory), «Bájale» (an easier question of the same subcategory), «Cambiazo» (similar difficulty, subcategory of their choice) and «Francotirador» (shoot an answer: a wrong one is struck out; hitting the right one repeats the level with fresh cards). Rules in `09-jokers.md`.
- **Players (D-28):** every game starts by asking for the **player name** (pick a known one or type a new one). The family can play as one name or each kid under their own.
- **Burning (D-28):** every question the player has **seen** is burned **for that player**: answered, skipped (joker or admin), swapped away by a joker, or lost to a Snipe hit. Only the descriptions on cards that weren't picked stay unburned. Other players can still get the question. The gamemaster can also burn a question **for everyone** (admin «Saltar y quemar para todos», GM-2), e.g. a wrong or broken one.

## Flow
The screen states and transitions are in `04-ui-tv-display.md` (Start → Level → Select → Question → Correct/Wrong → … → Victory).

## Question selection (GF-2)
The question difficulty (1–10, D-6) is a rating, not a level. Each game level draws from a **range** of difficulties (D-22):

| Level | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Difficulty | 1 | 2–3 | 3–5 | 4–6 | 4–6 | 4–6 | 5–7 | 6–8 | 6–9 | 7–10 | 8–10 | 9–10 |

- Every level offers **exactly 4** questions: approved, not burned for this player nor globally, with a difficulty in the level's range.
- Draft rules for picking the 4: prefer 4 different broad categories, and categories not already asked in this game. A question offered earlier in the same game is not offered again, so a game shows 48 different descriptions.
- «Saltar pregunta» (admin overlay, burns for the player) and «Saltar y quemar para todos» need one more candidate from the same range.
- **Jokers (09):** Paso, Bájale, Cambiazo and a Snipe hit take extra questions from the pool (and burn the replaced ones for the player), and a purge removes a subcategory from later draws. The server offers a joker only if the matching still fills every later level with 4 cards afterwards; otherwise it is shown disabled. Bájale may go below the level's range; Cambiazo stays inside it.
- **Supply check:** before a new game starts, the server checks that all 12 levels can be filled this way. The ranges overlap, so the check assigns questions level by level, starting with the narrowest ranges (level 1, then 12, 11, 2…). If the check fails, the Start screen tells the gamemaster which levels lack questions and which difficulties to add; the game doesn't quietly fall back to fewer cards. `qgen.py report` shows the same supply per level (GF-5).
- **Algorithm (D-25):** the available questions are the approved ones that aren't burned (for this game's player or globally, D-28) and weren't offered earlier in this game. Each level's 4 slots are filled by an exact bipartite matching (augmenting paths over 12 × 4 slots), narrowest ranges first. The **supply check** runs this matching over all 12 levels. To **draw** a level's 4 cards, the server shuffles the level's candidates, prefers broad categories that are neither among the cards already picked nor asked earlier in this game, and accepts a candidate only if the matching still fills every later level without it.
- **Skip (D-25, D-28):** only on the Question screen. The skipped question is burned for the player (globally with «Saltar y quemar para todos»). One new card from the same range replaces it, and the players choose again on the Select screen.
- **State (GF-4, D-25):** `data/game.sqlite` (gitignored) holds the players, the games (one running at a time, as a JSON state, with its player) and the burned questions (per player, or for everyone, D-28). The server shuffles the answers, checks the final answer and burns the question; one undo step restores the state before the last final answer and un-burns that question for the player.
- Pool sizing (OQ-17): one game burns 12 questions but needs 48 unburned ones per player (+ spares for skips and jokers, which are unlimited and burn what they replace, D-27; Bájale needs lower-difficulty questions in the same subcategory). Burning per player means a new player starts with the whole pool, with the most pressure on difficulties 4–6 (levels 4–6 each need 4, plus overlap with levels 3 and 7) and on difficulty 1 (level 1 alone).

## To define (see open-questions.md)
- ~~Jokers or lifelines?~~ Five jokers, unlimited (D-26, D-27, `09-jokers.md`). No timer (D-30).
- The answer is judged automatically (multiple choice, D-7). The gamemaster can undo it from the admin overlay.

## Tasks
- [x] GF-1 Write the full rule set. *2026-10-06: core rules in D-20; jokers in D-26/D-27 / `09-jokers.md`; players and burning in D-28; no timer (D-30).*
- [x] GF-2 Define the question-selection algorithm (difficulty curve, category mix, skip burned). *2026-10-06: exact matching + category preference (D-25), `tools/selection.py`.*
- [x] GF-3 Define the screen states and transitions. *2026-10-06: `04-ui-tv-display.md`, D-21.*
- [x] GF-5 Supply check per level (server, before a new game) and the same report in `qgen.py report`. *2026-10-06: `GET /api/game` → `supply`, shown on the Start screen; `qgen.py report` prints the supply per level.*
- [x] GF-4 Implement the game state machine (server-side state in SQLite, so a reload resumes the game). *2026-10-06: `server/game.py`, `data/game.sqlite`; new/pick/answer/skip/undo/abandon under `/api/game/…` (D-25).*
- [x] GF-6 Players (D-28): `players` table, player name on new games, burned per player plus global burn, supply check and draw per player, undo per player. *2026-10-06: `server/game.py`: `players` table (names ignore case, also «Í»/«í»), `games.player_id`, `burned (question_id, player_id NULL = everyone, game_id)`; old `data/game.sqlite` migrates on start, earlier burns count for everyone. API: `POST /api/game/new {"player"}`, `GET /api/game?player=` (supply per player), `GET /api/players`, `POST /api/game/skip {"everyone"}` (burns for the player or for all). The client still plays as «Familia» until UI-16 (`PLACEHOLDER(UI-16)`); the «para todos» button is GM-2.*
