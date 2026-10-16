# 13 — Game Modes

**Status:** modes decided (D-74, multiplayer D-77, timed D-80); gamemaster mode specced (D-88, «select answer» setting D-105); MD-6, MD-7, MD-10 done; MD-8.. open

Part of the Steam plan ([11](11-steam.md)). Today there is one way to play: the family as a team against the gamemaster, who knows the game and manages the jokers. A Steam player has no gamemaster, so the game itself has to set the rules. There are five modes and no "default mode" (D-74); this file defines them. Spanish names: «Solo o en grupo» fixed, the others proposals ([15a](15a-ui-translation.md) "Mode names").

## Modes
Shared by every mode except gamemaster mode (D-74):
- A question can never be skipped, not even a broken or far too hard one; no undo, no replacement, no joker changes mid-game.
- Flagging a question (decision 60, the flag with its note; was «Reportar pregunta») only logs; «Abandonar partida» and sound stay.
- Steam achievements, except in customized games.
- Input: gamepads, keyboard, mouse; no phones. Multiplayer modes add a "shared keyboard": one key per player hands them keyboard and mouse until their turn is done ([14](14-input.md)).
- Age group: the mode never shifts the age-group window (D-38, [21](21-age-groups.md)); no change to `age-groups.json`.

### Gamemaster mode (`gamemaster`, today's game; es proposal «Modo anfitrión»)
- One team; one person, the gamemaster, holds every control (keyboard, mouse, gamepad, switchable any time).
- "Configure game" screen with full customization before every game (MD-11).
- Gamemaster menu (`Esc`): arbitrary cheats: manage jokers, skip, replace the current question, undo, … (MD-12; today's overlay, D-30, MD-4).
- No achievements. Its defaults never change without the developer's say.

#### Configure game screen (MD-11; D-88, pm decision 33)
Plan 29's Choice screen in gamemaster form, no second screen. Opens on the player's last game's settings (`playerChoice` grows to every field below; a budget changed mid-game counts), else the defaults. A field missing in `settings` = the game before D-88 (old saves and the fixture replay unchanged); the configure screen always sends every field. Controls: ↑/↓ (D-pad, stick) move between rows, ←/→ change the value, Enter/A on «Jugar» starts (default focus), Enter/A toggles a switch, Backspace/B back to Player (`Esc` opens the overlay, as on every screen); mouse: click a value, − / + buttons. Strings `configure.*`.
- **Difficulty:** age group (`settings.age_group`, as today) or «Custom» (`configure.custom`; new `settings.difficulty: {start, end}`, integers 1–15, end ≥ start; with it no `age_group`). Default: the last choice, else `young_teens`. ←/→ cycles the age groups, then «Custom» (two −/+ rows: start, end; shown read-only with the group's span otherwise, plan 125). Ramp: level i of n targets t = start + (end − start)·(i − 1)/(n − 1) (n = 1: start); range [⌊t⌋, ⌈t⌉]. Errors: `difficulty_invalid`.
- **Bundles:** shared bundle selector component (Bundles screen before Choice in every mode, plan 151; menu): `bundlesFor(data)`; base bundles as a radio group, apart from the others (toggles); exactly one base (D-85, `base_bundle_count`). `settings.bundles` as today. Default (fresh player): the locale's first base bundle only (pm decision 33, partly supersedes D-85's default); games without `settings.bundles` keep D-85's default.
- **Jokers:** one row per joker (`TOKENS` order), 0–9 or ∞, clamped (←/→, −/+; `stepUses`, decision 105); `settings.jokers` via `new {jokers}` as today. Default (fresh player): `STANDARD_JOKERS`; `new` without `jokers` in gamemaster mode stays unlimited (fixtures). Preset row above them (decision 99, supersedes decision 33 here): Estándar (`STANDARD_JOKERS`) | Sin límite (all ∞) | Personalizado; ←/→ picks Estándar ↔ Sin límite and fills the rows, edited rows or a saved budget show their preset (`game/jokers.ts` `presetOf`); UI only, same in «Personalizar partida».
- **Allow video questions / allow audio questions:** two switches, default on; new `settings.video` / `settings.audio`, stored only as `false` (missing = allowed). Off: `availableNow` and `supply` drop questions whose `media.type` is `video` / `audio`; images and backgrounds stay.
- **Number of levels:** 1–20, default 12; new `settings.levels` (missing = 12). Won at level `levels`; the Tower draws `levels` steps. With an age group: level i of n uses the group's range at step round(1 + 11·(i − 1)/(n − 1)) (n = 1: step 1; n > 12 repeats steps). `selection.LEVELS` becomes a per-game value (`answer`, `laterLevels`, `selection.draw`, `assign`, `supply`). Errors: `levels_invalid`.
- **Cards per level:** 0–4, default 4; new `settings.cards` (missing = 4). The table shows that many cards (`selection.PER_LEVEL` per game; the supply needs max(cards, 1) per level). 0: one card is drawn and opened at once (no select phase); every return to the table (next level, skip, Paso y fuera, replace, jump) does the same. Errors: `cards_invalid`; switches: `switch_invalid`.
- **Select answer to advance to next level (D-105):** switch, default on; new `settings.answers`, stored only as `false` (missing = on); gamemaster mode only (`new` / `settings` elsewhere → `gamemaster_only`). Off:
  - Question screen: answers not selectable; the padlock is clickable at once (Enter/A, click) → engine `reveal` (no index; question phase, only with answers off, else `answers_on`; `answer` → `answers_off`)
  - reveal: seen row as for an answer; history `revealed: true` (stats, telemetry, achievements skip it as right/wrong); `last` with `chosen: null` + `correct_index`; undo snapshot as for `answer`; level +1, new table
  - after a reveal: neutral «Siguiente ronda», no fanfare, no sad trombone; never game over
  - last level: phase and result `completed` (not a win, not a loss); neutral «Cuestionario completado», fireworks ok, no victory music, no Victory screen
  - jokers stay, except Tiro mágico: unavailable with answers off (reason string)
  - no "game over on false answer" option
- Supply check (GF-5) and outlook (plan 65) run on the whole configuration; «Jugar» disabled with the reason when short (`supply_short`).

#### Gamemaster menu (MD-12; D-88, pm decision 34)
Today's overlay (`Overlay.svelte`) grows into the menu, in two visibly separate parts. Strings `overlay.*`.
- **General (every mode):** continue; «Preguntas marcadas» (MD-6; flagging itself is the flag dialog, decision 60); sound (volumes, mute); fullscreen (no language rows, D-96); restart (`abandon`, then the mode's start screen: configure screen in gamemaster mode); quit (desktop, after `flush`).
- **Gamemaster cheats (gamemaster mode only, hidden elsewhere):** every one an engine action in `engine/api.ts` / `engine/game.ts`, refused `gamemaster_only` (409) when `gameMode(state) !== "gamemaster"`; `lib/api.ts`, `lib/types.ts`.
  - «Saltar pregunta»: `skip` (as today): question phase only; outcome `admin_skip`, seen +1, table refilled.
  - «Bloquear pregunta»: `skip {everyone: true}` (as today, D-82): outcome `admin_block`, blocked, no seen row; confirm («¿Seguro?»).
  - Undo: `undo` (as today): back to the state before the last final answer, its seen row dropped; `settings` survive; seen and blocked rows written by any cheat stay.
  - «Gestionar comodines»: `jokers {joker: limit | null}` (as today); the rows show and edit uses *left* (−/+ gives back or takes one away; the client sends limit = used + left; ∞ = null); no preset row (decision 99: presets only before a game starts); any phase.
  - «Cambiar pregunta»: new `replace {seen?: boolean}`: question phase only; a new question at the same level from the same subcategory (`categoryCandidates` + `replacement`, GF-2 kept), else any subcategory in range; the old one gets history outcome `admin_replace` (new `Outcome`), no seen row unless `seen: true`; nothing to draw → `replace_empty`.
  - «Saltar a nivel»: new `level {level}`: 1..`levels` (`level_invalid`); select phase (with `cards: 0` it also replaces the question on screen, not seen); the table is redrawn at that level (old cards back in the pool); no history rows for skipped levels; the undo snapshot stays.
  - «Select answer to advance to next level» mid-game (D-105): switch in `GameSettings.svelte` (keys, pad, mouse as the configure switches); `settings {answers}` through `changeSettings`, same phase rule as difficulty and bundles.
  - Difficulty and bundles mid-game: new `settings {age_group? | difficulty?, bundles?}`: same validation and supply check as `new` (rest of the game: current level..`levels`); select phase (with `cards: 0` as for «Saltar a nivel»); the table is redrawn; history and level stay. UI: the configure screen's difficulty row and the shared bundle selector.
- Not built: revealing the answer from the menu (the TV is the only screen, UI-13; no phones, D-74); with answers off the padlock reveals (D-105).
- Input: the menu takes ↑/↓, ←/→, Enter/A, Esc/Start closes, B leaves (pad); mouse hover selects, click runs. The flat item list stays; «Cambiar pregunta» and «Saltar a nivel» are rows with ←/→ values; difficulty and bundles open a nested modal scope (`GameSettings.svelte`, `root`, `data-focus-default`) (MD-12).

### Alone or as group («Solo o en grupo», `solo`)
- One player alone, or everyone together as one team; no gamemaster menu, no cheats.
- The player picks the age group; no difficulty selection, no presets, no checkpoint.
- Standard joker set, the same for every age group: 3 × Soplo, 1 × each other joker.
- Customization possible but discouraged: no configure screen, only a small "Customize game" button on the age group screen; a customized game earns no achievements.

### Multiplayer modes (D-77)
Shared by the three: no skip, no undo, no joker changes mid-game; flagging only logs (decision 60); achievements unless customized. Input: one gamepad per player, keyboard, mouse, shared keyboard ([14](14-input.md) section 3). Built "Later" (MD-8, MD-9, IN-6).

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
- `settings.jokers` (MD-1..MD-4, `null` = unlimited) stays; `new` in gamemaster mode without `jokers` stays unlimited; the configure screen's fresh default is the standard set (D-88).
- Standard joker set: one engine constant (3 × Soplo, 1 × Paso y fuera, Hada madrina, Doña Exigente, Tiro mágico); every non-gamemaster game starts with it.
- `settings.customized`: `true` after any change via "Customize game"; feeds achievements (S5).
- Refusals outside gamemaster mode (engine, not only UI): undo, skip, replace, level, settings, joker budget changes (D-88).
- `ReportRow`: logs the current question to a local report list (a page to copy from); not seen-counted, no replacement; the player answers or uses a joker.
- Engine as built (task 376): `settings.mode` stored only when `new` carries it; missing resolved by `gameMode()`, never written back (fixtures unchanged); `customized` only outside gamemaster mode; `new` takes `jokers` overrides; refusal code `gamemaster_only` (409); `report` action (`note?`) needs a question on screen; save version 2 (`reports`).
- Cheats as built (task 498): `replace {seen?}` → `game.replace`, `level {level}` → `game.jumpLevel`, `settings {age_group | difficulty, bundles}` → `game.changeSettings`; `level` / `settings` in the question phase with `cards` > 0: `cheat_not_select`; with `cards: 0` the question on screen gets an `admin_replace` row (keeps its jokers spent, not seen) before the new table; mid-game supply short: `supply_short` with the levels current..`levels`.
- Mode screen as built (task 378): plan 29's Choice screen with a mode row (`BUILT_MODES`; order `solo`, `gamemaster`, decision 50); preset `?mode=` > the player's newest game (`playerMode`) > `gamemaster`; `new` always carries `mode` from there. `solo`: age group (bundles from the Bundles screen before Choice, not customization; preset `playerChoice`; decisions 158, 260, D-97), `jokers` sent only when they differ from `STANDARD_JOKERS` (engine sets `customized`); «Personalizar partida» edits the joker counts only (preset row + 0–9 / ∞, decision 99), no other fields.
- Joker availability (JK-2) has a reason «No te quedan Soplos» when the budget is spent; the tray shows count badges (MD-2, MD-3).

## Tasks
- [x] MD-1 Joker budget in the game state: `settings.jokers`, `null` = unlimited; existing and new family games default to unlimited. Engine: on the TS engine ([12](12-client-engine.md)) if it has landed, otherwise in `app/server/game.py`. *2026-10-07: `app/server/game.py` (`settings`, `jokers_left`: uses counted over the game's history plus the question on screen); the view sends `settings` and `jokers_left`; undo keeps the current budget.*
- [x] MD-2 Availability: a spent joker is disabled with a reason; budget counted per game (Snipe misses count as uses). *2026-10-07: «ya no les quedan Soplos» etc.; `POST /api/game/joker` refuses a spent joker too.*
- [x] MD-3 Joker tray: a count badge on limited jokers; none when unlimited. *2026-10-07: amber badge top left of the token (grey at 0), also on the read-only tray on Level and Select (`JokerTray.svelte`).*
- [x] MD-4 Gamemaster overlay: set the budget for the running game (unlimited / «Como las cartas» / custom). *2026-10-07: `POST /api/game/jokers`; the overlay has a second column (sound, «Comodines de esta partida»): «Comodines: Sin límite / Como las cartas / A medida» toggles the preset, each joker 0–9 or ∞ with ←/→ or −/+, and shows the uses left. Each new game starts unlimited, as planned.*
- [x] MD-5 Define the modes (OQ-30, OQ-36). *2026-10-12: D-74: five modes, no default mode, no presets, no checkpoint; outside gamemaster mode no skip, undo, replace or joker changes; «Reportar pregunta» only logs. Sections and implementation notes above.*
- [x] MD-6 «Reportar pregunta»: local report list only; no burn, no replacement (D-74). *2026-10-12: engine `report` (task 376); overlay by mode (`gamemaster` as before plus «Reportar pregunta» / «Preguntas reportadas»; `solo` without skip, undo and budget editor, read-only joker line); confirm dialog (Enter reports, Esc/⌫ cancel); `Reports.svelte` opens over the overlay instead of a `Screen` (the question below stays mounted), newest first, the answer of the question still on screen hidden, «Copiar» with a selectable `<pre>` fallback. 2026-10-13 (decision 60, task 625): merged into the flag (GM-5): the flag icon / `M` open `FlagDialog.svelte` (optional note, `Enter` flags, `Esc`/⌫ cancel; on a flagged question save the note or unflag; pad: letter picker); the overlay item and the engine action `report` are gone; the list is «Preguntas marcadas» (`FlagList.svelte`) with notes; save version 4: `reports` merged into `flags` (`{flagged_on, player, level?, note?}`); `trivia-authoring` puts the note into the needs-work feedback. 2026-10-13 (plan 93, decision 93): the list sends and copies reports: «Copiar» per flag and «Copiar todo» (text format decision 142), «Enviar» / «Enviar todas» to the report server with a Steam ticket (only with `reportUrl` set and a valid Steam user), confirm with the privacy text once per session, «Enviada <date>» from the flag's `reported_on`; `qgen flag` / `qgen flag --pull` turn reports into `needs_work`.*
- [x] MD-7 Mode screen (five modes); age group screen with "Customize game" in `solo`; `settings.mode`, `settings.customized`. *2026-10-12: mode row on the Choice screen (built modes only), keys `A`/`G` (es); `solo` shows «Personalizar partida» (`Customize.svelte`, joker steppers on a modal scope); preset `?mode=` > newest game > gamemaster; arrows + Enter + Esc/⌫ and mouse walked (task 379's wiring done here). 2026-10-14: `solo` gets the bundle selector too (decision 158).*
- [ ] MD-8 Later: the three multiplayer modes exactly as specced above (D-77, `timed` D-80): turn order, shared vs. per-player joker sets, age groups, drop-out and win rules; `timed`: rounds, claim and 6 s answer timer, lives, sudden death, hint cadence, hearts, ticking clock, red frame; seen events for the save (D-82); engine first, then screens. When a mode ships: enter its win achievement (`WIN_RR_COOP`, `WIN_RR_COMPETITIVE`, `WIN_TIMED`; [18](18-steam-integration.md) "Later") in Steamworks and `steam-achievements.vdf` before the mode joins `BUILT_MODES` (`inSteamworks()` unlocks it from then on; plan 86).
- [ ] MD-9 Later: multiplayer input with IN-6: per-player gamepads, shared keyboard (one key per player takes keyboard and mouse until the turn ends), the claim action in `timed` (any player, any time; per-player claim keys on the shared keyboard; D-80).
- [x] MD-10 Gamemaster mode: the gamemaster holds every control (keyboard, mouse, gamepad, switchable any time) via the action layer (IN-2, IN-3). *2026-10-12: covered by IN-1..IN-5: one scope stack for all three devices, `lastDevice` follows each action, so switching needs nothing; every screen and dialog pushes a scope; the overlay: Esc / Start / ☰ button opens it, ↑/↓ + ←/→ + Enter or D-pad/stick + A, B leaves, mouse hover + click, −/+ and sliders. Left for MD-12: the new editors in the menu (see "Gamemaster menu" Input); real-pad check by the developer still pending (IN-4).*
- [x] MD-11 Gamemaster mode: "configure game" screen before every game, fields as specced above (D-88); opens on the last game's settings, so Enter straight through on an existing save = today's game. *2026-10-12: `Choice.svelte` in gamemaster mode (lines: ↑/↓, ←/→ values, −/+), `BundleSelector.svelte`; `new` gets every field; jokers wrap 0–99 ↔ ∞ (2026-10-14, decision 105: 0–9 then ∞, clamped); outlook display left to task 623.*
- [x] MD-12 Gamemaster menu (`Esc`): general part + gamemaster cheats as specced above (D-88), incl. the input gap noted there. *2026-10-13: `Overlay.svelte`: general column (actions, sound, languages) + dashed panel «Trucos del anfitrión» (skip, block, undo, «Cambiar pregunta» ‹ no vista / vista ›, «Saltar a nivel» ‹ n ›, «Dificultad y paquetes», choice line; jokers: uses left, «n usados», limit = used + left via `fetchJokersUsed`); ←/→ on a plain item jumps column; difficulty and bundles in `GameSettings.svelte` (nested modal scope with `root`, `data-focus-default`; `BundleSelector`); restart = `abandon` + the player's configure screen (2026-10-14, task 800: «Volver al menú principal», `abandon` + Start). Walked headless with keyboard, mouse and a fake pad; ≤ 921 px at 1080 and 614 px at 800, `es` and `xx`.*
- [x] MD-13 Gamemaster mode: «select answer to advance to next level» (D-105) *2026-10-15: engine `settings.answers`, `reveal`, result `completed` (task 1123: `engine/state.ts`, `game.ts`, `api.ts`, `choice.ts`, `achievements.ts`, `telemetry.ts`); switch on the configure screen (`Choice.svelte`) and in `GameSettings.svelte` (task 1124); padlock reveal in `question/FinalAnswer.svelte`, `screens/Question.svelte`, new `screens/Revealed.svelte` («Siguiente ronda» / «Cuestionario completado») (task 1125); strings es/en/de (es-ES inherits, `xx` generated). Walked headless (built client, dev server, muted): answers off, 12 reveals by Enter and click → «Siguiente ronda» ×11 → «Cuestionario completado», result `completed`, no Victory; answers on: today's game; mid-game toggle in the dialog. Fixture replay passes (`npm test`). Screens and keys: `04-ui-tv-display.md`.*
