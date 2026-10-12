# 13 — Game Modes

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). Today there is one way to play: the family as a team against the gamemaster, who knows the game and manages the jokers. Software jokers are unlimited (D-27); in practice the gamemaster limits them with the printed cards (JK-11: 4 × Soplo, 2 × each other joker). A Steam player has no gamemaster, so the game itself has to set the limits. This file defines the modes. Most of it is still to be decided; the first tasks can be done now.

## Modes

### Gamemaster mode (today's game, its own mode; D-73)
- **Separate from all other modes:** its own entry on the mode screen; the rules, presets and limits of the default and competitive modes don't apply to it.
- **The gamemaster holds every control:** one person drives the game (the family answers out loud). Keyboard, mouse and gamepad all work, and the gamemaster switches between them at will, mid-screen too (IN-2/IN-3 action layer). Players never touch an input.
- **Configure game screen** before every game (after Player, before Level). Full customization, every field with today's family value as default, so «Empezar» right away plays today's game. Proposal (gamemaster to trim):
  - Team / player name (as today's Player screen)
  - Age group and bundles (AG, BN; family default young teens, every bundle on)
  - Categories and subcategories on/off
  - Levels to victory (default 12) and the difficulty per level (age group's window, or shifted −/+)
  - Joker budget per joker: ∞ / 0–9 (today's MD-4 controls; presets «Sin límite», «Como las cartas»)
  - Wrong answer: ends the game (default) / fall back to a checkpoint level / play on
  - Show the correct answer after a wrong one (default on, OQ-22); unlock a locked answer (default on, OQ-21)
  - Media questions on/off; music, effects and question audio volume
  - Allow burned questions again when a level runs dry (default off)
  - Saved as the gamemaster's last configuration; «Restablecer» returns to the family defaults
- **Gamemaster menu** (`Esc`, Start on the pad; today's overlay, extended). Cheats are allowed without limit. Proposal (gamemaster to trim):
  - Jokers: set the budget mid-game (MD-4), give back a used joker, take one away
  - Skip the question: burn for the player (today) / for everyone (today) / no burn
  - Replace the current question: new card same level / same subcategory / harder / easier / pick from a list
  - Mark the answer correct or wrong (disputed answers), undo the last answer (today)
  - Jump to a level (up or down)
  - Show the next hint, eliminate wrong answers, reveal the correct answer
  - Flag the question (today's flag), sound, fullscreen, abandon, back to start, quit (today)
- This is how the family plays. Its defaults never change without the gamemaster's say.

### Default mode (Steam's first choice, to define, OQ-30)
- One team (one player name, or the family as one name), no gamemaster.
- **Difficulty presets** set the effective difficulty, mostly through the joker budget. Draft:

  | Preset | Soplo | Paso | Bájale | Cambiazo | Francotirador | Notes |
  |---|---|---|---|---|---|---|
  | Fácil | ∞ | 3 | 3 | 3 | 3 | for young kids |
  | Normal | 4 | 2 | 2 | 2 | 2 | = the printed card set (JK-11) |
  | Difícil | 2 | 1 | 1 | 1 | 1 | |
  | Experto | 0 | 0 | 0 | 0 | 0 | |

- Other levers that could join the presets (to decide): the level → difficulty ranges (D-22) shifted down or up; a "checkpoint" at level 6 on Fácil, so a wrong answer drops you back there instead of ending the game.
- **Admin actions in the default mode:** no undo (it would be a cheat button) and no «Saltar y quemar para todos». Instead **«Reportar pregunta»**: it burns the question for everyone on this machine, writes it to a local report list (shown on a page the player can copy from) and draws a replacement. «Abandonar partida» stays.
- **Audience** (OQ-36, D-38): four age groups (kids, young teens, young adults, adults), each playing a window of the shared difficulty scale 1–15 ([21](21-age-groups.md)).

### Competitive mode (later, stub; OQ-37)
- 2 to 8 or more players take turns, on one screen. Ideas to choose from:
  - **Relay ladder:** one shared tower; players answer in turn; a wrong answer knocks that player out and the next one continues the level. The last one standing, or whoever climbs highest, wins.
  - **Parallel ladders:** each player has their own tower and plays one level per round; all players see all questions (spectators can't call out answers, so that's a social rule).
  - **Buzzer round:** everyone sees the question, and the first to buzz (controller button) answers. This needs one controller per player or phones ([14](14-input.md)).
- Jokers per player (each with their own budget), and maybe "attack" jokers (give the next player a harder card).
- **Burning:** a question seen by everyone is burned for every player in the game (D-28 still holds), so supply runs out N times faster. The supply check needs per-game union rules, and the content target (16) must account for it.
- Player count vs. supply: 8 players × 12 levels × extras may exceed the pool. Limit the players per difficulty band or allow reuse in this mode (to decide).

### Couch co-op
- Possibly just the default mode with several controllers: anyone can move the focus and propose an answer, and a team "confirm" needs a majority. Owned here for the rules and by [14](14-input.md) for input.

## Implementation notes
- The game state gets `settings: {mode, jokers: {hint: number|null, ...}, preset?}`. `null` = unlimited, the default for existing saves (no change for the family).
- Joker availability (JK-2) gains a reason «No te quedan Soplos» when the budget is spent.
- The joker tray shows the remaining count on each token (a small badge); unlimited shows no badge, so the family's screen looks the same.
- A **mode screen** picks gamemaster, default or competitive mode. The default mode's settings screen sits between Player and Level (UI-16); the gamemaster mode has its own configure game screen there (D-73).
- Gamemaster settings extend `settings` (levels, wrong-answer rule, filters, reuse); unknown fields default to today's behaviour, so old saves play unchanged.

## Tasks
- [x] MD-1 Joker budget in the game state: `settings.jokers`, `null` = unlimited; existing and new family games default to unlimited. Engine: on the TS engine ([12](12-client-engine.md)) if it has landed, otherwise in `app/server/game.py`. *2026-10-07: `app/server/game.py` (`settings`, `jokers_left`: uses counted over the game's history plus the question on screen); the view sends `settings` and `jokers_left`; undo keeps the current budget.*
- [x] MD-2 Availability: a spent joker is disabled with a reason; budget counted per game (Snipe misses count as uses). *2026-10-07: «ya no les quedan Soplos» etc.; `POST /api/game/joker` refuses a spent joker too.*
- [x] MD-3 Joker tray: a count badge on limited jokers; none when unlimited. *2026-10-07: amber badge top left of the token (grey at 0), also on the read-only tray on Level and Select (`JokerTray.svelte`).*
- [x] MD-4 Gamemaster overlay: set the budget for the running game (unlimited / «Como las cartas» / custom). *2026-10-07: `POST /api/game/jokers`; the overlay has a second column (sound, «Comodines de esta partida»): «Comodines: Sin límite / Como las cartas / A medida» toggles the preset, each joker 0–9 or ∞ with ←/→ or −/+, and shows the uses left. Each new game starts unlimited, as planned.*
- [ ] MD-5 Define the default mode: presets, checkpoints, which admin actions remain (OQ-30, OQ-36).
- [ ] MD-6 «Reportar pregunta»: local report list + burn for everyone on this machine + replacement.
- [ ] MD-7 Mode and settings screen; the gamemaster mode reachable from it (or from a launch option).
- [ ] MD-8 Competitive mode: choose the format (OQ-37), the per-game burning and supply rules, joker budgets per player.
- [ ] MD-9 Couch co-op rules (team confirm), with IN-6.
- [ ] MD-10 Gamemaster mode as its own mode on the mode screen (D-73); every input works for the gamemaster, switchable at any time.
- [ ] MD-11 Configure game screen for the gamemaster mode: the gamemaster confirms the field list; settings in the engine; family defaults; last configuration kept.
- [ ] MD-12 Gamemaster menu: the gamemaster confirms the cheat list; engine actions and overlay (keyboard, mouse, pad).
