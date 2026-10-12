# 13 — Game Modes

**Status:** modes decided (D-74, multiplayer D-77, timed D-80); MD-6 done; MD-7.. open

Part of the Steam plan ([11](11-steam.md)). Today there is one way to play: the family as a team against the gamemaster, who knows the game and manages the jokers. A Steam player has no gamemaster, so the game itself has to set the rules. There are five modes and no "default mode" (D-74); this file defines them. Spanish names: «Solo o en grupo» fixed, the others proposals ([15a](15a-ui-translation.md) "Mode names").

## Modes
Shared by every mode except gamemaster mode (D-74):
- A question can never be skipped, not even a broken or far too hard one; no undo, no replacement, no joker changes mid-game.
- «Reportar pregunta» only logs; «Abandonar partida» and sound stay.
- Steam achievements, except in customized games.
- Input: gamepads, keyboard, mouse; no phones. Multiplayer modes add a "shared keyboard": one key per player hands them keyboard and mouse until their turn is done ([14](14-input.md)).
- Age group: the mode never shifts the age-group window (D-38, [21](21-age-groups.md)); no change to `age-groups.json`.

### Gamemaster mode (`gamemaster`, today's game; es proposal «Modo anfitrión»)
- One team; one person, the gamemaster, holds every control (keyboard, mouse, gamepad, switchable any time).
- "Configure game" screen with full customization before every game (MD-11).
- Gamemaster menu (`Esc`): arbitrary cheats: manage jokers, skip, replace the current question, undo, … (MD-12; today's overlay, D-30, MD-4).
- No achievements. Its defaults never change without the gamemaster's say.

#### Proposal A: configure game screen (MD-11; pm decision "Configure game screen: which fields?")
Plan 29's Choice screen in gamemaster form; opens on the player's last choice (`playerChoice`) or the defaults, so Enter straight through = today's game. Controls for every row: ↑/↓ (D-pad) move, ←/→ (D-pad) change the value, Enter/A on «Jugar» starts (default focus), Enter/A on a toggle toggles, Esc/B back to Player. Mouse: click a value, − / + buttons.
- Age group (plan 29): default `young_teens`; `settings.age_group`; ←/→ cycles `age-groups.json`.
- Bundles (plan 29): default every bundle, `base` always on; `settings.bundles`; one toggle row per bundle.
- Joker set: default «Sin límite»; `settings.jokers` (existing, `new {jokers}`); ←/→ cycles Sin límite / Como las cartas (`CARDS`) / Estándar (`STANDARD_JOKERS`) / A medida; A medida shows the overlay's per-joker rows (0–9, ∞).
- Media questions on/off: default on; new `settings.media` (missing = on); off = draws skip questions with `media` (background images stay); the supply check counts it.
- Start level (weighed, recommended): default 1; new `settings.start_level` (missing = 1); ←/→ 1–12; the game starts there, the Tower shows lower levels as not played, level 12 still wins. For a short game or a late start.
- Not proposed: cards per level (`PER_LEVEL` = 4; the table layout is built for 4), levels to win (12 is the game), hint count (the questions fix it).
- Option 2 (shorter): age group, bundles, joker set only.

#### Proposal B: gamemaster menu cheats (MD-12; pm decision "Gamemaster menu: which cheats?")
Today's overlay grows; every cheat is an engine action refused outside gamemaster mode (`gamemaster_only`, 409). Undo after any cheat: as after `skip` today, it goes back to the state before the last final answer; seen and blocked rows written by the cheat stay; the budget stays (`settings` survive undo).
- Kept: continue; «Saltar pregunta» (`skip`, seen +1); «Bloquear pregunta» (`skip {everyone}`, blocked, D-82); undo (`undo`); «Reportar pregunta» / «Preguntas reportadas» (`report`); sound; fullscreen; restart (`abandon` + configure screen); quit (desktop).
- Joker budget → «Gestionar comodines»: same `jokers` action, but each row edits uses *left* (−/+ gives back or takes away one; limit = used + left), preset row as today; also usable on the table between questions.
- «Cambiar pregunta» (new `replace {seen?}`): new question at the same level from the same subcategory (`categoryCandidates` + `replacement`, GF-2 kept), any subcategory if none; outcome `admin_replace`; default not seen (the question stays fresh), `seen: true` counts it; refused without a question on screen or without a candidate (`replace_empty`).
- «Saltar a nivel» (candidate, recommended; new `level {level}`): 1–12; table redrawn at that level; no history rows for skipped levels; refused during a question (skip first).
- Age group / bundles mid-game (candidate, recommended; new `settings {age_group?, bundles?}`): only on the table (select phase); supply check as at `new`; the table is redrawn; the question history stays.
- Not proposed: reveal the answer to the gamemaster: the TV is the only screen and the family sees it (UI-13), no phones (D-74).
- Option 2 (shorter): kept items + «Gestionar comodines» + «Cambiar pregunta» only.

### Alone or as group («Solo o en grupo», `solo`)
- One player alone, or everyone together as one team; no gamemaster menu, no cheats.
- The player picks the age group; no difficulty selection, no presets, no checkpoint.
- Standard joker set, the same for every age group: 3 × Soplo, 1 × each other joker.
- Customization possible but discouraged: no configure screen, only a small "Customize game" button on the age group screen; a customized game earns no achievements.

### Multiplayer modes (D-77)
Shared by the three: no skip, no undo, no joker changes mid-game; «Reportar pregunta» only logs (plan 36); achievements unless customized. Input: one gamepad per player, keyboard, mouse, shared keyboard ([14](14-input.md) section 3). Built "Later" (MD-8, MD-9, IN-6).

### Round-robin co-op (`rr-coop`; es proposal «Por turnos en equipo»)
- Turn order: one question per player, in join order, round after round.
- One team, one game, one age group.
- Jokers: one shared standard set (3 × Soplo, 1 × each other joker); any player may use what's left on their turn.
- Drop-out and win: a wrong answer ends the game for the team, as today; level 12 = everyone wins.
- No timer.
- Seen events (D-82): ≈ 1 game's (12 + the standard set's skips and swaps).

### Round-robin competitive (`rr-competitive`; es proposal «Por turnos, todos contra todos»)
- Turn order: one question per player, in join order; each turn plays that player's own game.
- Every player: own game, own level, own standard joker set, own age group.
- Drop-out and win: a wrong answer ends only that player's game; first to level 12 wins.
- No timer.
- Seen events (D-82): ≈ N players × 1 game's; every seen event counts for the save, whichever player saw it.

### Competitive timed (`timed`; es proposal «Contrarreloj»; D-80, replaces D-77's timed part)
- 12 rounds; round = level (the question's difficulty follows the round); questions per round = number of players.
- One age group for everyone; no jokers.
- Every question shown to all players: 30 s, a hint every 8 s; unclaimed after 30 s = next question, nothing else.
- Claim: own action, any player, any time → that player has 6 s to answer; 6 s timeout = wrong answer; once the answer is shown, the next question comes; players may claim again after scoring.
- Lives: three each; round end: no correct answer in that round = −1 life; wrong answer (or claim timeout) = out at once; third life lost = out.
- Win: round 12 is sudden death (first claim + correct answer wins at once); only one player left = wins at once.
- Visuals: rounds and hearts; a heart pulses at a player's last chance in a round without a correct answer, stronger on their last heart; last 3 s of a claim: a clock ticks once per second, louder each tick, plus a pulsing red frame (impending-death warning of a first-person shooter); the same red frame when everyone is at risk at once (all on their last life, nobody correct this round yet).
- Seen events (D-82): ≈ N questions per round (N players), up to 12 rounds, fewer after drop-outs; no jokers.
- Open detail (not a decision): after drop-outs, do questions per round follow the players still in?

## Implementation notes
Spec for MD-6/MD-7 (plan 36) and MD-10..MD-12 (plan 59).
- `settings.mode`: `gamemaster` | `solo` | `rr-coop` | `rr-competitive` | `timed`; missing = `gamemaster`, old saves unchanged. Today's game = gamemaster mode.
- `settings.jokers` (MD-1..MD-4, `null` = unlimited) stays; gamemaster mode keeps unlimited as its default.
- Standard joker set: one engine constant (3 × Soplo, 1 × Paso, Bájale, Cambiazo, Francotirador); every non-gamemaster game starts with it.
- `settings.customized`: `true` after any change via "Customize game"; feeds achievements (S5).
- Refusals outside gamemaster mode (engine, not only UI): undo, skip, replace, joker budget changes.
- `ReportRow`: logs the current question to a local report list (a page to copy from); not seen-counted, no replacement; the player answers or uses a joker.
- Engine as built (task 376): `settings.mode` stored only when `new` carries it; missing resolved by `gameMode()`, never written back (fixtures unchanged); `customized` only outside gamemaster mode; `new` takes `jokers` overrides; refusal code `gamemaster_only` (409); `report` action (`note?`) needs a question on screen; save version 2 (`reports`); `replace` gets its guard with plan 59.
- Joker availability (JK-2) has a reason «No te quedan Soplos» when the budget is spent; the tray shows count badges (MD-2, MD-3).

## Tasks
- [x] MD-1 Joker budget in the game state: `settings.jokers`, `null` = unlimited; existing and new family games default to unlimited. Engine: on the TS engine ([12](12-client-engine.md)) if it has landed, otherwise in `app/server/game.py`. *2026-10-07: `app/server/game.py` (`settings`, `jokers_left`: uses counted over the game's history plus the question on screen); the view sends `settings` and `jokers_left`; undo keeps the current budget.*
- [x] MD-2 Availability: a spent joker is disabled with a reason; budget counted per game (Snipe misses count as uses). *2026-10-07: «ya no les quedan Soplos» etc.; `POST /api/game/joker` refuses a spent joker too.*
- [x] MD-3 Joker tray: a count badge on limited jokers; none when unlimited. *2026-10-07: amber badge top left of the token (grey at 0), also on the read-only tray on Level and Select (`JokerTray.svelte`).*
- [x] MD-4 Gamemaster overlay: set the budget for the running game (unlimited / «Como las cartas» / custom). *2026-10-07: `POST /api/game/jokers`; the overlay has a second column (sound, «Comodines de esta partida»): «Comodines: Sin límite / Como las cartas / A medida» toggles the preset, each joker 0–9 or ∞ with ←/→ or −/+, and shows the uses left. Each new game starts unlimited, as planned.*
- [x] MD-5 Define the modes (OQ-30, OQ-36). *2026-10-12: D-74: five modes, no default mode, no presets, no checkpoint; outside gamemaster mode no skip, undo, replace or joker changes; «Reportar pregunta» only logs. Sections and implementation notes above.*
- [x] MD-6 «Reportar pregunta»: local report list only; no burn, no replacement (D-74). *2026-10-12: engine `report` (task 376); overlay by mode (`gamemaster` as before plus «Reportar pregunta» / «Preguntas reportadas»; `solo` without skip, undo and budget editor, read-only joker line); confirm dialog (Enter reports, Esc/⌫ cancel); `Reports.svelte` opens over the overlay instead of a `Screen` (the question below stays mounted), newest first, the answer of the question still on screen hidden, «Copiar» with a selectable `<pre>` fallback.*
- [ ] MD-7 Mode screen (five modes); age group screen with "Customize game" in `solo`; `settings.mode`, `settings.customized`.
- [ ] MD-8 Later: the three multiplayer modes exactly as specced above (D-77, `timed` D-80): turn order, shared vs. per-player joker sets, age groups, drop-out and win rules; `timed`: rounds, claim and 6 s answer timer, lives, sudden death, hint cadence, hearts, ticking clock, red frame; seen events for the save (D-82); engine first, then screens.
- [ ] MD-9 Later: multiplayer input with IN-6: per-player gamepads, shared keyboard (one key per player takes keyboard and mouse until the turn ends), the claim action in `timed` (any player, any time; per-player claim keys on the shared keyboard; D-80).
- [ ] MD-10 Gamemaster mode: the gamemaster holds every control (keyboard, mouse, gamepad, switchable any time) via the action layer (IN-2, IN-3). *pm plan for milestone 7 part 11.*
- [ ] MD-11 Gamemaster mode: "configure game" screen before every game, full customization; defaults = today's game (Enter straight through).
- [ ] MD-12 Gamemaster menu (`Esc`): today's overlay (undo, skip, «Bloquear pregunta» (D-82), joker budget, MD-4) + manage jokers, replace the current question, further decided cheats.
