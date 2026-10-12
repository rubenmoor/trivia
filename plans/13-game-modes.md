# 13 — Game Modes

**Status:** modes decided (D-74); MD-6.. open

Part of the Steam plan ([11](11-steam.md)). Today there is one way to play: the family as a team against the gamemaster, who knows the game and manages the jokers. A Steam player has no gamemaster, so the game itself has to set the rules. There are five modes and no "default mode" (D-74); this file defines them.

## Modes
Shared by every mode except gamemaster mode (D-74):
- A question can never be skipped, not even a broken or far too hard one; no undo, no replacement, no joker changes mid-game.
- «Reportar pregunta» only logs; «Abandonar partida» and sound stay.
- Steam achievements, except in customized games.
- Input: gamepads, keyboard, mouse; no phones. Multiplayer modes add a "shared keyboard": one key per player hands them keyboard and mouse until their turn is done ([14](14-input.md)).
- Age group: the mode never shifts the age-group window (D-38, [21](21-age-groups.md)); no change to `age-groups.json`.

### Gamemaster mode (`gamemaster`, today's game)
- One team; one person, the gamemaster, holds every control (keyboard, mouse, gamepad, switchable any time).
- "Configure game" screen with full customization before every game (MD-11).
- Gamemaster menu (`Esc`): arbitrary cheats: manage jokers, skip, replace the current question, undo, … (MD-12; today's overlay, D-30, MD-4).
- No achievements. Its defaults never change without the gamemaster's say.

### Alone or as group («Solo o en grupo», `solo`)
- One player alone, or everyone together as one team; no gamemaster menu, no cheats.
- The player picks the age group; no difficulty selection, no presets, no checkpoint.
- Standard joker set, the same for every age group: 3 × Soplo, 1 × each other joker.
- Customization possible but discouraged: no configure screen, only a small "Customize game" button on the age group screen; a customized game earns no achievements.

### Round-robin co-op (`rr-coop`)
- Players take turns, all on one team, one age group, one shared standard joker set. Spec: plan 41 (OQ-37).

### Round-robin competitive (`rr-competitive`)
- Players take turns, each with their own game, jokers and age group. Spec: plan 41 (OQ-37).

### Competitive timed (`timed`)
- All answer the same question at once, 30 s, hints every 8 s, no jokers, first to level 12 wins. Spec: plan 41 (OQ-37).

## Implementation notes
Spec for MD-6/MD-7 (plan 36) and MD-10..MD-12 (plan 59).
- `settings.mode`: `gamemaster` | `solo` | `rr-coop` | `rr-competitive` | `timed`; missing = `gamemaster`, old saves unchanged. Today's game = gamemaster mode.
- `settings.jokers` (MD-1..MD-4, `null` = unlimited) stays; gamemaster mode keeps unlimited as its default.
- Standard joker set: one engine constant (3 × Soplo, 1 × Paso, Bájale, Cambiazo, Francotirador); every non-gamemaster game starts with it.
- `settings.customized`: `true` after any change via "Customize game"; feeds achievements (S5).
- Refusals outside gamemaster mode (engine, not only UI): undo, skip, replace, joker budget changes.
- `ReportRow`: logs the current question to a local report list (a page to copy from); no burn, no replacement; the player answers or uses a joker.
- Joker availability (JK-2) has a reason «No te quedan Soplos» when the budget is spent; the tray shows count badges (MD-2, MD-3).

## Tasks
- [x] MD-1 Joker budget in the game state: `settings.jokers`, `null` = unlimited; existing and new family games default to unlimited. Engine: on the TS engine ([12](12-client-engine.md)) if it has landed, otherwise in `app/server/game.py`. *2026-10-07: `app/server/game.py` (`settings`, `jokers_left`: uses counted over the game's history plus the question on screen); the view sends `settings` and `jokers_left`; undo keeps the current budget.*
- [x] MD-2 Availability: a spent joker is disabled with a reason; budget counted per game (Snipe misses count as uses). *2026-10-07: «ya no les quedan Soplos» etc.; `POST /api/game/joker` refuses a spent joker too.*
- [x] MD-3 Joker tray: a count badge on limited jokers; none when unlimited. *2026-10-07: amber badge top left of the token (grey at 0), also on the read-only tray on Level and Select (`JokerTray.svelte`).*
- [x] MD-4 Gamemaster overlay: set the budget for the running game (unlimited / «Como las cartas» / custom). *2026-10-07: `POST /api/game/jokers`; the overlay has a second column (sound, «Comodines de esta partida»): «Comodines: Sin límite / Como las cartas / A medida» toggles the preset, each joker 0–9 or ∞ with ←/→ or −/+, and shows the uses left. Each new game starts unlimited, as planned.*
- [x] MD-5 Define the modes (OQ-30, OQ-36). *2026-10-12: D-74: five modes, no default mode, no presets, no checkpoint; outside gamemaster mode no skip, undo, replace or joker changes; «Reportar pregunta» only logs. Sections and implementation notes above.*
- [ ] MD-6 «Reportar pregunta»: local report list only; no burn, no replacement (D-74).
- [ ] MD-7 Mode screen (five modes); age group screen with "Customize game" in `solo`; `settings.mode`, `settings.customized`.
- [ ] MD-8 Multiplayer modes (`rr-coop`, `rr-competitive`, `timed`): per-game burning and supply rules, joker sets per player (plan 41, OQ-37).
- [ ] MD-9 Shared keyboard and multiplayer input, with IN-6 (plan 41).
- [ ] MD-10 Gamemaster mode: the gamemaster holds every control (keyboard, mouse, gamepad, switchable any time) via the action layer (IN-2, IN-3). *pm plan for milestone 7 part 11.*
- [ ] MD-11 Gamemaster mode: "configure game" screen before every game, full customization; defaults = today's game (Enter straight through).
- [ ] MD-12 Gamemaster menu (`Esc`): today's overlay (undo, skip, burn for everyone, joker budget, MD-4) + manage jokers, replace the current question, further decided cheats.
