# 13 — Game Modes

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). Today there is one way to play: the family as a team against the gamemaster, who knows the game and manages the jokers. Software jokers are unlimited (D-27); in practice the gamemaster limits them with the printed cards (JK-11: 4 × Soplo, 2 × each other joker). A Steam player has no gamemaster, so the game itself has to set the limits. This file defines the modes. Most of it is still to be decided; the first tasks can be done now.

## Modes

### Gamemaster mode (today's game, kept)
- One team, one screen. A gamemaster runs it with the `Esc` overlay (skip, burn for everyone, undo, abandon; D-30).
- **New:** the joker budget can be set per game: unlimited (today), or a count per joker. A preset «Como las cartas» matches the printed set (4 Soplo, 2 each other), so the family can drop the paper cards if they like, or keep them and leave the budget at unlimited.
- This is the family's mode. Its defaults never change without the gamemaster's say.

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
- A **mode/settings screen** sits between Player and Level (UI-16) in the default mode; in the gamemaster mode it is hidden behind the overlay.

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
