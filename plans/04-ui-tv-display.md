# 04 — TV Display, Screens, Sound & Motion

**Status:** draft

The game as the family sees it on the TV: screen states, transitions, sound and animation. Rules come from `03-game-flow.md` (D-20). The visual and audio contract is decided in D-21. UI copy is Spanish (D-6). The examples below are suggestions, and the developer has the final say.

## Requirements
- Full-screen, 16:9, readable from the couch with a **compact** type scale and high contrast. The look (colours, type, glass panels, components) is owned by `10-visual-design.md` (D-29).
- A background image for each question, shown at its own size and centred on the night stage: scaled down only when it is bigger than the screen, never up, never stretched; its edges fade softly into the stage (D-51). Everything over it is a separate, semi-transparent glass panel (no full-width scrims), so the picture stays visible (D-29).
- Decorative images are blurred and slightly darkened, with a big question mark in the centre (D-15), so they read as mood, not as a clue. Illustrative and essential media are shown sharp (D-24).
- Progress is shown as a **tower of blocks** that grows by one block per correct answer and gets narrower towards the top (see Level screen).
- Players choose each question by its humorous `description` (D-8). The category is never shown.
- A subtle media credit line in a corner whenever media is shown (IMG-4, `06-images.md`).
- Every screen change is a **transition with its own sound effect** (see Transitions).
- Suspenseful background music on a loop at low volume, in three intensities: normal, question selected and answer submitted (D-22).
- A **joker tray** on the Question screen (read-only on Level and Select), with an animation for every joker (D-26, `09-jokers.md`).
- Everything runs offline: sounds, music, fonts and animations ship with the client. No CDN, and no new npm dependencies (AGENTS.md).

## Screen states

```mermaid
stateDiagram-v2
  [*] --> Language: fresh save, ≥2 languages (D-86, D-96)
  Start --> Language: language button
  Language --> Start: «Atrás» / Backspace
  [*] --> Start
  Language --> Start: confirm (reload if the UI language changed)
  Start --> Player: «¡Jugar!» (new game)
  Player --> Mode: name chosen
  Mode --> Player: «Atrás» / Backspace (first step)
  Mode --> Choice: «Seguir» (solo, gamemaster)
  Mode --> Join: «Seguir» (multiplayer modes, decision 291)
  Join --> Mode: «Atrás» / Backspace (seats kept)
  Join --> Choice: «Seguir» (≥ 2 seats, all named)
  Choice --> Mode: «Atrás» / Backspace (solo, gamemaster)
  Choice --> Join: «Atrás» / Backspace (multiplayer modes)
  Choice --> Bundles: «Seguir»
  Bundles --> Choice: «Atrás» / Backspace (picks kept)
  Bundles --> Level: «¡A jugar!» (new game, «¡Hola, …!»)
  Level --> Select: continue
  Select --> Question: pick a description
  Question --> Correct: final answer right
  Question --> Wrong: final answer wrong
  Question --> Select: joker «Paso y fuera» (09)
  Question --> Level: joker «Tiro mágico» hits the right answer, same level (09)
  Correct --> Level: level < 12 (a block is added)
  Correct --> Victory: level 12 answered
  Wrong --> Start: «Volver al inicio»
  Victory --> Start: «Volver al inicio»
  Question --> Next: answers off, padlock reveal (D-105)
  Next --> Level: continue (a block is added)
  Question --> Completed: answers off, last level revealed
  Completed --> Start: «Volver al inicio»

  state Question {
    [*] --> Presenting
    Presenting --> Answering: media started / text shown
    Answering --> Locked: tap an answer
    Locked --> Answering: unlock (tap an answer or Backspace)
    Locked --> Submitted: «Respuesta final»
    Answering --> Joker: play a joker (Locked unlocks first)
    Joker --> Answering: hint shown, question swapped, answer struck out, or cancel
    Submitted --> [*]: reveal after a wait that grows with the level
  }
```

The joker sub-states (skip choice, category picker, snipe aiming) are detailed in `09-jokers.md`. The **admin overlay** is orthogonal to all of these: `Esc` opens it over any state and pauses that state (see Admin overlay).

| State | Shows | Leaves via | Music |
|---|---|---|---|
| Language | First start (D-86) or Start's language button (D-96): «Elige el idioma», languages by flags + endonym (decision 186), guess preselected | Click / `Enter` / pad A / `1`–`n`; from Start: «Atrás» / `Backspace` / pad B | Normal |
| Start | Title, «¡Jugar!», "continue game" if one is running; along the bottom third a horizon of Commons cut-outs (`Horizon.svelte`, `public/horizon/`, plan 150), same in every language, behind the content | Click / `Enter` | Normal |
| Player | «¿Quién juega?»: known names, new name | Click a name / `1`–`9` / `Enter` (most recent name, nothing focused) / type + `Enter` | Normal |
| Mode | «¿Cómo se juega?»: «Solo o en grupo» or «Multijugador», then «Modo de juego»: Estándar or Modo anfitrión, or the multiplayer modes in two groups (decision 314) | «Seguir» / `Enter`; «Atrás» / `Backspace` | Normal |
| Choice | «¿Cómo juega …?», the age screen: gamemaster mode: the configure game screen (MD-11: difficulty, levels, cards, video, audio, answers (D-105), jokers); the other modes: age group (rr-competitive: one per seat), «Personalizar partida»; no bundles, no supply | «Seguir» / `Enter`; «Atrás» / `Backspace` | Normal |
| Join | Multiplayer modes only: «press A to join» per pad, keyboard card, seat cards (colour, device, name, rr-competitive: age group) | «Seguir» (≥ 2 seats, all named) / `Enter`; «Atrás» / `Backspace` | Normal |
| Bundles | «¿Qué preguntas juega …?»: the question bundles (plan 151); the supply report | «¡A jugar!» / `Enter`; «Atrás» / `Backspace` | Normal |
| Level | The tower, «Nivel N de 12» | Click / `Enter` / `Space` | Normal |
| Select | 4 description cards | Click a card / `1`–`4` | Normal |
| Question | Question, 4 answers, media, lock, final button, joker tray | Final answer; jokers Paso y fuera / Tiro mágico hit | Intense (off while question media plays); after submitting: most intense |
| Correct | Fanfare, fireworks overlay, correct answer, `fun_fact` | Click / `Enter` | Fanfare replaces the music, then Normal |
| Wrong | Dark animation, correct answer, consolation | «Volver al inicio» | Off; a sad sting |
| Victory | Full 12-block tower, big finale | «Volver al inicio» | «Pomp and Circumstance» (`victory`), over cheers |
| Next | Answers off (D-105): «Siguiente ronda», the correct answer, `fun_fact` | Click / `Enter` / A | Normal |
| Completed | Answers off, after the last level: «Cuestionario completado», correct answer, fireworks | «Volver al inicio» | Normal (no victory music) |

### Language (first start, D-86, D-96)
- At first start only for a fresh save (no `language` stored) and only with something to pick (>1 UI language); a stored save, like the family's, never sees it unasked.
- One list of UI languages by endonym, the guessed one (`guessTag()`) preselected and focused; heading and confirm prompt in the guessed language.
- A pick sets the one language (UI and questions, D-96); confirming writes the save, so it asks once. A UI language other than the boot one reloads the app.
- Questions: the language's pool if it exists and passes, else Spanish (`es`).
- No Esc menu here; later changes: Start's language button only (opens this screen with «Atrás» / `Backspace` / pad B).

### Start
- Game title, a short subtitle, a big «¡Jugar!» button.
- The first click is also the **audio unlock**. Browsers block sound and autoplaying video with sound until a user gesture, so nothing plays before it. After this click, autoplay works for the rest of the session.
- Language button top right, under ☰ (D-96, decisions 157, 186): the language's flags (`Flags.svelte`) + endonym, key per catalog (`I`/`L`/`S`), pad Y; opens the Language screen. The only place to change the language; hidden while the save notice shows.
- If an unfinished game exists (server state, GF-4), show «Continuar» with its player and level («Continuar: Sofía, nivel 5») next to «Nueva partida»; a session: its players cut after two and the turn seat's level («Continuar: Ana, Luis y 2 más, nivel 3»), the mode's name small below (plan 163).
- Desktop shell only (`desktop?.mods`): a `secondary` «Mods» button under play/resume (count of loaded mods when > 0); while the notice isn't accepted and mods are held off, a line «N mods found, off until you allow them» under the buttons.
- No supply report (plan 133): the supply check is on the Bundles screen.

### Mods (plan 118)
- `game/screens/Mods.svelte`: full-screen layer like `Credits.svelte` (own modal scope, `data-focus-default`); from the start screen's «Mods», the Esc menu's «Mods» row, or by itself before the start screen after a crashed start (`safeStart.reason === "crashed"`). Not in the dev server (no `mods` bridge). Shell side: `18-steam-integration.md` "Modding: mods screen and safe start".
- Rows in load order (invalid and pending ones last, no move controls): name, version, source (Local / Workshop + published file id), kind badges, languages (endonyms; none = all); state line (loaded, off, on/off after restart when `on ≠ active`, invalid + reason, downloading, disabled in Steam, needs a Steam user); warnings (plan 112/114 codes, `modErrors()`, per bundle `modIssues()` of this language's load: «{bundle}: N questions skipped», media skipped, categories.json unreadable, no questions for this language, languages ignored); focused row: description, local folder name.
- Codes → `mods.state.*`, `mods.warning.*`, `mods.issue.*`, `mods.error.*`; an unknown code shows as is.
- Controls (IN-1, each a button with `<Prompt>`): on/off per row, ▲▼ move on the focused row (pad LB/RB via `joker-focus`), «Refresh» (`mods:list` again), «All off», «Restart to apply» (enabled when any `on ≠ active` or the order differs from this run's), «Back» (`Esc`/`Backspace`/B → where it came from). Every change calls `mods:set` at once; no save button.
- Top lines: crashed safe start («The last start with mods didn't finish…», names the mods, «All off» focused); `--no-mods`; no valid Steam user (decision 111, rows still toggle); empty list (where mods go, the guide explains; no link).
- One-time notice (`game/ModsNotice.svelte`, decision 151: Mods notice per install in mods.json; new mods held off until it): on the first turn-on or «Restart to apply» with any on while not accepted; mods are made by other players and run code with the game's access; «Allow mods» → `mods.notice()`, then the action; «Cancel» (focus default, `Esc`/B) changes nothing.
- Screen gallery: steps in task 802 (stubbed `mods` list).

### Player (D-28)
- «¿Quién juega?»: the known player names as big buttons (most recent first, keys `1`–`9`), plus «Nuevo jugador» with a text field (the TV machine's keyboard, OQ-11).
- A chosen name goes to the Mode screen; the supply check is on the Bundles screen after it.
- Each name can be deleted with all its games and progress (GF-7): a small trash button on hover or keyboard focus, then a confirmation.
- Letter picker for a pad (plan 46, SW-4): `game/LetterPicker.svelte`, modal over the screen; keyboard and mouse never see it.
  - Opens on pad A with the field focused, or the «Ⓐ Escribir» button next to the field (shown only when the pad was last).
  - 9-column grid `A`–`Z`, `Ñ`, `Á É Í Ó Ú Ü`, `-`; row «Espacio», «⌫ Borrar», «Listo»; spatial focus, default «A».
  - Auto-capital (`game/letters.ts`): first letter and after space or `-` upper case, rest lower; 30 chars.
  - A types; B deletes, on an empty name closes; Start closes; text stays in the field. «Listo» = «¡A jugar!».
  - Mouse clicks on keys; physical letters, `Backspace`, `Enter` (focused key), `Esc` (close) while open.
- Idle animation so the TV doesn't look frozen, e.g. the empty foundation slowly breathing, or floating question marks.

### Bundles (plan 151, BN-6)
- `game/screens/Bundles.svelte`, «¿Qué preguntas juega Sofía?»: after Choice in every mode, also with one offered bundle (decision 264: Bundle screen (two columns) reviewed in /gallery?; D-97; task 1361's layout): Player → Choice → Bundles → Level; multiplayer modes: Player → Choice → Join → Bundles → Level (plural titles «¿Qué preguntas juegan?», supply for the whole session, decision 291).
- The shared `game/BundleSelector.svelte`, `large`: a narrow base column on the left (toggle tiles, no heading), a vertical ruler, the optional bundles as fixed-width tiles (26 units) flowing in a CSS grid (`auto-fill`); icon (flag for regional) + name + question count, no descriptions (decision 263), no headings; selected = the Choice look (dark tile, sky outline + tint, decision 312) with a check mark, hover lifts, focus keeps the global ring; counts per decision 267 (`countShown`: base «5000+», others «2000+», a mod bundle its own rounded-down count from `fetchChoiceOptions`' `count`); the optional area has a fixed height between title and buttons and scrolls (wheel, touch), a fade at a cut edge; fits 1280×720, 1280×800, 1920×1080 with 1 and 15 optional bundles. «Ajustes de la partida» reuses the compact selector with descriptions (MD-12), same order and icons.
- Icons: base a book, a regional bundle its country's flag (mods too), other mod bundles the puzzle.
- Bundles: only those of the new game's question locale (`bundlesFor`; the language's, else `es`, D-96), names in that language; order `orderBundles` (D-97): base bundles in file order (ours, then mods); optional: regional of the player's region, then non-regional, then regional of other countries, file order within each.
  - Player's region: the machine's locale country (shell: `app.getLocaleCountryCode()`, else the system locale's region; `triviaShell.region`); browser and dev server: `navigator.language`'s region; `?region=XX` (`?region=` none) overrides; `playerRegion` in `lib/desktop.ts`.
  - Every bundle, base ones too, is an on/off tile (`role="switch"`, «activado» / «desactivado»); any combination (milestone 8, 2026-10-16), the base bundle may be off.
  - Key per bundle (`bundleKeys`, in displayed order): first letter of its name (after a `Regional:`-style prefix; accents stripped) not taken by an earlier bundle, else its next letter; never the flag key (es `M`). es: `P` Paquete básico, `C` Regional: Colombia; en `B`, `C`; de `G`, `K`.
- Preset: the player's newest game's bundles (`playerChoice`), else the locale's first base bundle, non-base off (decision 33). The pick lives in `Game.svelte` (and Choice's picks as a draft, `choiceDraft.ts`): Bundles → «Atrás» → Choice → «Seguir» shows both unchanged; a name chosen on Player starts fresh.
- Supply (decisions 206, 268): the supply of the whole choice (Choice's picks + these bundles) on entering and on every toggle; short: «¡A jugar!» off, the `SupplyReport.svelte` below; no question for the choice (nothing selected, or the selected bundles hold none for the age group and levels: every level without a candidate): off, with «Ningún paquete elegido tiene preguntas para esta partida» (`bundles.noQuestions`), no report; a refusal of `new` (supply, `no_questions`, `bundle_not_offered`) shows here. Start shows none.
- Supply notice (plan 65, decision 31): «¡A jugar!» first asks `outlook`; tight levels (≤ 1 unseen), none left or chosen bundles running out (≤ 1 unseen in the window, task 1104; «This bundle is running out of questions: Regional: Colombia») → modal `SupplyNotice.svelte` (bundle hint if one helps); Enter plays, `Backspace`/`Esc` back. Every start calls `noteRunningOut` with what it showed (`notified_exhausted`: bundle ids).
- «¡A jugar!» / `Enter`: `new` with `{player, mode, age_group, bundles, jokers?}` («Solo o en grupo»), every field in gamemaster mode (`age_group` or `difficulty`, `bundles`, `levels`, `cards`, `video`, `audio`, `answers`, `jokers`). Then «¡Hola, Sofía!» plays into the transition to Level; the name stays in a corner of the Level screen.
- Input (scope `bundles`): a bundle's letter toggles it and scrolls it into view (focus stays); arrows move spatially: ←/→ and ↑/↓ between tiles in rows and columns, across the ruler, down from the last row to the buttons; a tile scrolled out of view is reached only from inside the scrolling area (`data-nav-scroll`, `lib/focus.ts`), the focused tile scrolls into view; `Enter`/A on a tile toggles, on «¡A jugar!» starts (default focus); `Backspace`/B back to Choice; `Esc` the overlay.

### Mode (MD-7, plan 36, decision 314)
- `game/screens/Mode.svelte`, two steps in one screen. Step 1 «¿Cómo se juega?»: two tiles, «Solo o en grupo» (keys `mode.soloKey`) and «Multijugador» (`mode.multiKey`); skipped while no multiplayer mode is shown. Step 2 «Modo de juego»: single: «Estándar» (mode `solo`) and «Modo anfitrión»; multiplayer: two visually separated groups, one pick across both: «En colaboración» (rr-coop) and «En competencia» (rr-competitive, `timed`); the unbuilt ones only in dev mode, marked `PLACEHOLDER` (decision 293, `BUILT_MODES`).
- Selected state: the tile look everywhere (outline + tint, `.pick-tile.on` in `theme.css`); a pick then «Seguir» / `Enter`. Back from step 2 returns to step 1, from step 1 to Player; coming back from a later screen opens step 2 of the pick.
- Preset: `?mode=` launch option, else the player's newest game's mode (`playerMode`), else gamemaster mode. Focus ids `kind-single`, `kind-multi`, `mode-<id>`.

### Choice (plan 29, AG-7, BN-6)
- `game/Choice.svelte`, «¿Cómo juega Sofía?»: what the next game plays, after Mode (and Join in a multiplayer mode), before Bundles; preset: the player's newest game, else the language's defaults (engine `choice` route, plan 71); returning from Bundles shows the picks kept (`choiceDraft.ts`). «Seguir» is always enabled; no bundle line, no supply report, no short-group marks (decision 268).
- No mode row any more (decision 314): the Mode screens come before, the age screen is this one. Preset of the age: the player's newest game's group; rr-competitive: one stepper line per seat (seat colour, name, group, ←/→; each seat's preset is its player's newest group, set on the Join screen); «Personalizar partida» as before (not in gamemaster mode or timed).
- Gamemaster mode: the configure game screen (MD-11, D-88, decision 33: Configure game screen: which fields?); every field preset from the player's newest game (`playerChoice`), a fresh player: `young_teens`, `STANDARD_JOKERS`, video/audio on, 12 levels, 4 cards.
  - Left «Partida»: Difficulty (age groups, then «A medida»; «Desde» / «Hasta» rows always shown: with a group its span, read-only (no −/+, skipped by ↑/↓ and the focus ring), with «A medida» editable 1–15, end ≥ start, starting at the group's span; plan 125), Niveles 1–20, Cartas por nivel 0–4 (0: «pregunta directa»), Preguntas con video / audio, «Responder para avanzar» (switches; D-105, `answers`, sent only as `false`). Right «Comodines»: «Conjunto» preset row (Estándar | Sin límite | Personalizado, decision 99: ←/→ Estándar ↔ Sin límite fills the rows), then one row per joker (`TOKENS` order), 0–9 or ∞, clamped (← stops at 0, → stops at ∞; decision 105).
  - Lines (`data-line`): ↑/↓ (D-pad, stick) move line by line, left column then right; ←/→ change a value on a stepper or switch; −/+ and switch clicks with the mouse; `Enter`/A on a switch toggles, on a stepper or «Seguir» continues; `1`–`4` pick a group.
  - The supply report with the whole configuration is on the Bundles screen; a long report tightens the gaps so 720p fits.
- «Solo o en grupo»: age group, a small «Personalizar partida» button (`P`) with «Comodines estándar» / «Comodines personalizados» next to it.
  - Dialog `game/Customize.svelte` (modal scope): preset row «Conjunto» (Estándar | Sin límite | Personalizado, decision 99), then one row per joker, 0–9 or ∞ (MD-4 steppers); ↑/↓ rows, ←/→ or −/+ change, «Listo» / `Enter` / `Esc` / `Backspace` close, focus back on the button.
  - `new` gets `mode: "solo"` and `jokers` only when they differ from the standard set; the engine sets `customized` (D-74: no achievements).
- Age group: four tiles in `age-groups.json` order, name + ages («6–10 años», «23+ años»), keys `1`–`4`; the window isn't shown.
- Multiplayer modes (decision 291): plural title «¿Cómo juegan?»; rr-coop, `timed`: the age group line; rr-competitive: no group line, «each player picks on the next screen»; «Personalizar partida» (jokers, same for every seat) in rr-coop and rr-competitive, none in `timed`.
- «Seguir» / `Enter`: the Bundles screen with these picks (multiplayer modes: the Join screen); the game starts on Bundles.

### Join (plan 162, decisions 291, 292)
- `game/screens/Join.svelte`, multiplayer modes only, between Mode and Choice: a grid of seat cards in join order (seat colour from `game/seats.ts`, device glyph or «Teclado y ratón» / the claim key, name, remove), a «press A to join» card per unbound pad, a «join with keyboard» card; the grid scrolls (`data-nav-scroll`), no cap of our own.
- Rules: unbound pad A joins, a bound pad's B leaves; keyboard card (Enter/click): no pad seated → any number of keyboard seats (round-robin `shared`, no key, decision 273; `timed`: «press your key» capture, `claimKeyOk`, decision 290); a pad seated → one keyboard-and-mouse seat only (decision 274); a pad's A is refused with a notice while 2+ keyboard seats exist; a lone keyboard seat becomes `kbm` when a pad joins.
- Names: every seat named, distinct by casefold; the name control opens `NamePicker.svelte` (known players, new name, letter picker / Steam keyboard); first seat preset to the Player screen's name.
- «Seguir» needs ≥ 2 seats, all named (keyboard-only `timed`: all with keys), reason shown under it. Before the session starts every device drives the shared UI; only join/leave are per device.
- Timed ends (plan 164, task 1452): round screen in round 12 = «Muerte súbita» (coral, `boom`; «Otra ronda más: n» after a repeat, decision 281); Timed screen's round line coral in sudden death; Victory: winner's seat tag under the crowned tower, «¡Gana Ana!», «Último en pie» unless the winning answer was the sudden-death one, others' small seat tags with hearts; nobody wins (decision 280): Wrong with «Nadie gana esta vez», all seat tags muted, «Inicio»; Start's resume line `screen.start.resumeTimed` («Continuar: Ana y Luis, ronda 5») with the mode name below; no rich-presence token in timed (no «Ronda» token).
- «Atrás» / `Backspace`: back to Player. `Esc`: the overlay.

### Level (between questions)
Players start at **level 1** (easiest question) and must answer **level 12** to win (D-20). Before every question, they see where they are.

- **The tower (D-22):** a wide foundation at the bottom, with **12 block slots** above it. Each block is **narrower than the one below**, so the tower tapers towards the top (block 1 is about 90 % of the foundation's width, block 12 about 35 %; block heights stay similar, so the tower doesn't look squat). Slots that aren't earned yet are faint dotted outlines, so the goal height is always visible. Each correct answer adds one solid block. Other level counts (D-88, 1–20): one slot per level, same total height (blocks flatter or, up to a cap, taller); materials, milestone lines, reveal waits and the block thud map the level onto the 12-level scale (`game/levels.ts`); `cards: 0` skips Select (the question opens straight from the Level screen).
- **Block arrival:** when the Level screen follows a correct answer, the new block drops from the top of the screen, lands with a squash-and-settle bounce and a **thud**, and the tower wobbles slightly. The thud's pitch rises with each level, so height sounds like progress. On level 1 (the empty foundation), a soft "ready" sound plays instead.
- Blocks look varied: a different colour or texture per level, or per broad category of the question answered (a reason to keep the history, B-1). Higher blocks get fancier (stone → brick → marble → gold). Level 12 gets a crown or flag slot at the top.
- Text: «Nivel 3 de 12». Optional milestone lines at levels 4 and 8 («¡Ya vamos por la mitad!» at 6).
- Level 1: a random get-ready line («¡Prepárense para la primera pregunta!», «¿Ya tienen algo para picar a la mano?», …; `copy.milestone.1`, one per game).
- The camera follows: the view scrolls or scales so the top of the tower and the next empty slot stay in frame.
- **Repeat (09):** after a Snipe hit, the Level screen comes in with a rewind effect instead of black, no block drops, and the text reads «Nivel N de 12 — otra vez».
- The joker tray is shown small and read-only, as a reminder of the jokers (09).
- **Round-robin (plan 163, decision 279):** the Level screen is the turn handover, no screen of its own: «Turno de» and the turn seat's large `SeatTag` (seat colour, name, device glyph) above «Nivel N de 12»; «Seguir» in that seat's glyph, only that seat may press it; the corner HUD (Level, Select, Question) shows the turn seat's small tag. rr-coop: the team's tower, «Del equipo» over the shared joker tray. Paso y fuera, a Tiro mágico hit: same seat keeps the turn.
- **rr-competitive (plan 163):** `Tracks.svelte` instead of the single tower: one small tower per seat in join order, its tag below (2 rows from 5 seats, narrower from 9), the turn seat glowing in its colour, an out seat a muted empty wreck, the answerer's newest block dropping after Correct; «Nivel N de 12», milestone line and joker tray (labelled «Comodines» over the turn seat's tag, on Level, Select and Question) are the turn seat's own.

### Question selection
Four cards, each showing only a question's `description` (D-8). The players pick one.

- **Quirky design:** cards as sealed envelopes, mystery boxes or old library index cards. Each is tilted at a slightly different angle, with a hand-drawn number (1–4), a wax seal or postage stamp, and a gentle idle wobble. Hover or focus lifts a card and straightens it. A random doodle can sit in a corner (a coffee ring, a paper clip, a googly-eyed question mark).
- Cards deal in one at a time with a paper "flick" sound (part of the transition into Select).
- **Picking:** click or press `1`–`4`. An **immediate short sound** plays (a "pop", stamp or seal crack), the chosen card pulses or tears open, the other three slide off, then the transition to the Question screen starts. No confirmation step.
- There are **always 4 cards** (D-22). They come from the level's difficulty range (GF-2, `03-game-flow.md`). The unchosen questions don't count as seen (D-20, D-82). A card that replaces a skipped or purged one deals in highlighted («¡Nueva!», 09).

### Question
- Full-bleed media background (D-15 rules), the question in a floating glass card at the top, four answer tiles (A–D) in a 2×2 grid at the bottom, at most 70 % wide. The credit line is in a corner. Layout sketch and tile states: `10-visual-design.md`.
- The `description` is **not** shown here: it belongs to the Select screen only (D-8). Once the question is on screen, only the question itself is shown.
- **Media autoplays** once the screen has faded in: audio and video start from the start. The intense question music is faded out before the media starts and fades in when the media ends. A small replay button (`R`) restarts the media. Images need nothing.
- **Hints:** only through the «Soplo» joker (D-26). Space under the question band is reserved for the hint notes (09).
- **Joker tray:** five tokens along the left edge (09). Jokers are playable until «Respuesta final»; their animations are in `09-jokers.md`.
- **Locking in:** tapping an answer (click or `A`–`D` / `1`–`4`) locks it in:
  1. A heavy **lock "clunk"** sound plays, and the chosen answer gets a bright frame with a small padlock icon. The other answers dim.
  2. Below the answers sits a **big padlock** (or a vault door / chain) that has been covering the final-answer button. After a short suspense beat (~0.8 s), it unlocks with a click, swings or slides away (~0.6 s) with a metallic sound, and reveals the **«Respuesta final»** button.
- **Going back (D-22):** while an answer is locked in, tapping any answer (or `Backspace`) **unlocks** it. This is the lock-in animation in reverse: the big padlock swings back in front of «Respuesta final» and closes with a clunk, the answer's frame and padlock icon go away, and the other answers brighten again. **No answer is locked in afterwards**; the players tap again to lock in an answer, the same one or another. This leaves room for family debate.
- **Final answer:** «Respuesta final» (click or `Enter`) submits. The answers can't be changed any more, the screen darkens around the question, and the music switches to the **most intense track** (see Music). The players then wait under a drumroll (amber halos beating outwards, the trembling, shimmering «And the answer is…» growing until the reveal; task 1105); the higher the level, the longer the wait:

  | Level | 1–2 | 3–4 | 5–6 | 7–8 | 9–10 | 11 | 12 |
  |---|---|---|---|---|---|---|---|
  | Wait before the reveal | 3 s | 4 s | 5 s | 6 s | 8 s | 10 s | 12 s |

  The values are a starting point, to be tuned on the TV (UI-6). At the reveal, the music transitions straight into the fanfare (right) or the sad sting (wrong), with no silence in between. The right answer flashes green. On a wrong answer, the chosen answer flashes red as well, and the right one flashes green, so the players always see the right answer (D-22). Then the result screen follows.
- **Answers off (D-105, gamemaster mode, `settings.answers: false`):** the tiles show but can't be picked (no `A`–`D` / `1`–`4`, no pad pick glyphs); no «Respuesta final»: the padlock is a button «Mostrar respuesta», clickable at once (`Enter`/A, click) → engine `reveal`. It opens (padlock-open sound), the correct answer flashes green, no drum roll, no fanfare, no sad trombone; then Next («Siguiente ronda»), or at the last level Completed. Jokers stay, Tiro mágico locked (engine reason). Tower: one block per level behind (`level − 1`). Mid-game toggle: «Ajustes de la partida» dialog (task 1124); toggled back on, the tower counts correct answers only again.
- **Peek (plan 113, decision 126):** on a question with a sharp picture (image, not decorative, loaded), holding `R3` or `V` (catalog `screen.question.peekKey`), or pressing and holding the mouse on the bare picture, fades every panel out (~150 ms: HUD, card, answers, tray, prompts, «Respuesta final», credit, corner ☰ and flag) and shows the whole picture (D-51 fit), unfiltered; release brings it back unchanged (focus, locked answer, armed joker). Prompt «Ver imagen» in the HUD row, on image questions only. Not on video/audio/decorative questions, nor with Paso y fuera, Tiro mágico, Doña Exigente, the flag dialog or the overlay open (opening one ends the peek). Timed mode: the clock keeps running. Panels fade by `opacity` + `pointer-events: none`, not `visibility: hidden`, which drops DOM focus. Checked at 1280×800, 1280×720, 1920×1080 on every image question (task 923).
- **Category splash (plan 181, task 1586):** on every new question (Question and Timed, also after a Paso/Cambiazo swap; not on the reveal) the subcategory shows big and centred with its category small below (decision 353; the category alone without a subcategory) (`question/Splash.svelte`, `pointer-events: none`), holds `SPLASH_HOLD_MS` once the question has faded in, then leaves with an exit from `question/splash.ts` (random, none of the last 5 again) and its sound cue (`splash-*`). All 20 exits are in (the per-letter ones split the name into word and letter spans). `reducedMotion()`: plain fade, sound kept. All exits play on `/?efectos`. Timed: independent of the clock's show action (decision 296). Sounds (task 1589): every splash cue is a recording, Kenney CC0 (`disolver`, `derretir`, `agujero-negro`, `pajaros`, `gelatina`, `maquina-escribir`, reusing existing samples for the others); synth recipes stay as fallback; none left synth-only.

### Correct
- A **fanfare / jingle** plays (several variants, picked at random so it doesn't get stale).
- **Fireworks overlay:** one of several animations, picked at random, drawn on a full-screen transparent `<canvas>` **over** the question screen, with the correct answer still visible underneath. Variants: classic rockets with bursts, confetti cannon from both bottom corners, a ring or heart burst, sparkler trails, a falling-stars shower. Each variant runs about 3 s. They are hand-written canvas code with no library (UI-9).
- Then a panel shows the correct answer and the `fun_fact`.
- Continue (click / `Enter`) → transition → Level screen, where the new block drops in. After level 12 → Victory.
- Round-robin: the answerer's `SeatTag` (`last.seat`) under «¡Correcto!»; a session routes on `last.correct` and its end, not the top-level phase.

### Wrong
- The game ends (D-20). The submitted music has already turned into a **sad sound** (a descending trombone "wah-wah", or a low gong) at the reveal. No music plays on this screen.
- **Dark animation:** colour drains from the screen (desaturate), a vignette closes in, and the tower (shown small) crumbles, or its blocks fall away one by one with soft thuds. Rain or a slow fade to deep blue also works. It should be gentle, not scary; the players are 11 and 12 (D-6).
- Then the **correct answer** and the `fun_fact` are shown (D-22), with a **consolation message** that names the level reached: «¡Llegaron al nivel 7! Eso es más alto que la mayoría de las torres…». There are several messages, chosen by how far the players got.
- One button: **«Volver al inicio»** → transition → Start.
- Round-robin: the answerer's `SeatTag`; rr-competitive's out seat: «¡Fuera, Ana!» instead of «¡Oh no!», its track crumbles, no consolation line; rr-coop: the team's tower crumbles, the team lost, «Volver al inicio»; rr-competitive, one seat out: «Seguir» → Level of the next turn, or Victory for the last one standing (decision 279).

### Next and Completed (answers off, D-105)
- `game/screens/Revealed.svelte`, both neutral: neither success nor failure, sky-coloured title, the correct answer and `fun_fact` (`AnswerPanel`), normal music; whoosh in, no applause, no boom.
- **Next** «Siguiente ronda»: «Seguir» / `Enter` → Level, the new block drops in.
- **Completed** «Cuestionario completado» (phase and result `completed`, not a win, not a loss): fireworks, no victory music, no Victory screen; «Volver al inicio» / `Enter` → Start.

### Victory
- After the 12th correct answer: the Level screen shows the 12th block landing, the crown on top, a long fireworks finale (all variants in sequence) and a victory jingle. Text: «¡Ganaron!».
- «Volver al inicio» → Start.
- rr-coop: the line under the title names every player («¡Luna, Mateo y Sofía llegaron a la cima!», after four «y n más»).
- rr-competitive: «¡Gana Ana!», the winner's tower and tag big (crowned when it climbed to the top), the others' tracks small beside it in one row with their final levels; won as the last one standing (decision 278): the line «Último en pie» and no crown.

## Transitions
Every change between the states above uses one transition routine with these steps:

1. **Music fades out** (~600 ms, linear gain ramp to 0).
2. **Transition sound effect** starts. Each state change has its own sound, e.g. whoosh (Start→Level), paper flick (Level→Select), pop (the pick sound itself, then a swoosh into Question), a deep "boom" (into Correct or Wrong, after the reveal).
3. **Fade to black** (~400 ms). Some transitions use a wipe, iris or card-flip instead of black when it fits the next screen. Black is the default.
4. The next screen mounts behind the black, and media and images preload. The transition waits for preloading, up to 2 s.
5. **Fade in** (~400 ms).
6. **Music fades back in** (~800 ms): the track that belongs to the new state (see Music), unless the state keeps it off (Question with media, Wrong, Victory).

Jokers add transitions **inside** the Question state (card flip for swapped questions, sweep for a skip, rewind for a Snipe hit); they use the same input lock and audio fades (09).

Input is ignored while a transition runs, so a double tap can't skip a state. All durations are constants in one file, so they can be tuned on the real TV (UI-6).

## Audio

### Channels
| Channel | Content | Default level | Notes |
|---|---|---|---|
| Music | Three suspenseful loops (see Music) | low, ~15 % | Fades out on transitions and during question media |
| Effects | Transition sounds, lock, thud, fanfare, fireworks pops | ~70 % | Never ducked |
| Question media | Audio and video from the pool (06) | 100 % | Music is off while it plays |

### Music (D-22)
Three loops of the same suspenseful theme, getting more intense. It's best if all three share key and tempo, so they can follow each other without clashing.

| Track | Plays during | Character |
|---|---|---|
| `normal` | Start, Level, Select | Calm but suspenseful: low pads, a soft pulse |
| `question` | Question screen, from the fade-in while no answer is locked in | More intense: faster pulse, ticking, strings |
| `submitted` | While an answer is locked in (developer feedback, 2026-10-06) | Most intense: heartbeat or timpani rolls, rising pitch |
| `roll` | From «Respuesta final» until the reveal | A snare drum roll that builds up to the reveal |
| `victory` | Victory, once | Epic: the grand finale of Elgar's «Pomp and Circumstance» No. 1 (the «Land of Hope and Glory» tune in full force, then the coda), US Marine Band, public domain (developer request, 2026-10-06) |

- **Selecting a question** goes through the normal transition: `normal` fades out, then `question` fades in on the Question screen (after the question media, if any).
- **Locking in** an answer cuts sharply (~80 ms) from `question` to `submitted`; unlocking cuts back. **Submitting** cuts to the drum roll `roll`, with a short "hit" effect on top.
- **The reveal** is where the roll turns into the result: a quick fade-out (~150 ms) of `roll` overlapped with the start of the fanfare/jingle (right) or the sad sting (wrong), so the music turns into the result rather than stopping. The wait (table above) can stretch the roll; it keeps rolling at full strength.
- **After Correct,** `normal` comes back with the transition to the Level screen.

- One shared Web Audio `AudioContext` (no library). Each channel has a gain node, so fades are `linearRampToValueAtTime`. Effects are decoded once into `AudioBuffer`s at startup, so they play instantly. Each music track loops through `AudioBufferSourceNode.loop` for a gapless loop. The three tracks are decoded at startup too.
- The volume per channel and a master mute are set in the admin overlay and remembered in `localStorage` (or the server settings).

### Sound assets
- Files live in `app/client/public/audio/` (`music/`, `sfx/`), go into `app/client/dist/` at build time and are served offline like the rest of the client.
- Only free licences: CC0 preferred, CC BY with a credit in `app/client/public/audio/CREDITS.md` (no credits screen then, developer 2026-10-06; PUB-5 added one for the release). Sources: Wikimedia Commons (as for question media, D-13), freesound.org CC0, OpenGameArt. Unlike question media (D-17), all audio that is part of the UI (music and effects) gets committed to the repo, with a `CREDITS.md` next to it (D-22). Files should be compressed (Ogg Vorbis/Opus, or MP3) to keep the repo small.
- A fallback for every effect that has no asset yet: a short synthesized sound (oscillator + envelope) generated in code, so the game is never silent during development.
- Starter list: music `normal`, `question`, `submitted`; whoosh; paper flick; card pick pop; lock clunk; lock open; padlock close (unlock); submit hit; reveal boom; correct reveal ding; 3+ fanfares; firework launch and burst; block thud; sad trombone; victory jingle; menu open and close; plus the joker sounds listed in `09-jokers.md`.
- Timed mode (plan 164, task 1451), synthesized until recorded: music track `timed` (generated loop, 132 bpm, faster than `question`; no file yet, plan 33: Recorded music loops (UI-10)); cues `claim` (buzzer sting on a claim) and `countdown` (tick of the claim's last 3 s, `level` 1–3: louder and higher; plan 32: Recorded sound effects (UI-10)); reused: `heartbeat`, `glass-break`, `whistle-down`, `fanfare`, `rustle`, `boom`. The music ducks during a claim.

## Admin overlay
`Esc` opens a semi-transparent menu over any screen. It pauses the current state: question media pauses and animations freeze. `Esc` again closes it and resumes. The family sees the overlay, so it never shows the correct answer. A separate GM view is GM-3 (05).

Menu items (keyboard-navigable, large enough for the TV), the gamemaster menu (MD-12, D-88): a general part (every mode) and, in gamemaster mode, the cheats in a dashed amber panel «Trucos del anfitrión» beside it (shown while a game runs or can be undone). Fits without scrolling at 1920 × 1080 and 1280 × 800 (`es`, `xx`).
- **General, left column:** Continuar; «Preguntas marcadas»; Pantalla completa; Créditos; Mods (desktop shell only: the Mods screen, «Back» returns to the menu; "Mods (plan 118)"); «Volver al menú principal» (confirm; `abandon`, then Start; milestone 9 replaces D-88's configure screen); «Salir del juego» (desktop; own colour `--quit` / `--quit-line`, apart from every other button, selected too); under «Sonido»: volumes, mute (no language rows, D-96).
- **Continuar** (close).
- **Volumen:** music, effects and media sliders, plus mute all.
- **Cheats, first column** (`overlay.cheats`; each enabled only in the phase its engine action accepts):
  - **Saltar pregunta:** back to Select with a new card replacing the current question, without using a joker. The skipped question counts as seen (D-82).
  - **Bloquear pregunta** (was «Saltar y quemar para todos», D-82): the same, but the question is blocked for the save, never shown again: for a wrong, broken or ambiguous question. Needs a confirmation.
  - **Deshacer:** take back the last final answer, if the gamemaster misjudged or someone pressed by accident (GM-2); also after a cheat.
  - **Cambiar pregunta** ‹ no vista / vista ›: a new question at the same level (`replace {seen}`), question on screen only.
  - **Saltar a nivel** ‹ n ›: 1..levels, from the current level (`level`); then the Level screen. Select phase (with 0 cards also on the question).
  - **Ajustes de la partida** (task 1127; was «Dificultad y paquetes»): a dialog (`GameSettings.svelte`, own modal scope): the configure screen's difficulty row (age groups, then «A medida» with Desde/Hasta) and the shared bundle selector, plus the «Responder para avanzar» switch (D-105; ←/→, `Enter`/A, click); «Aplicar» (or `Enter` on a row) sends `settings`, a refusal (e.g. supply short) stays in the dialog; a new table, level and history stay. Same phases as «Saltar a nivel».
  - The game's choice below, read-only.
- **Cheats, second column: Comodines de esta partida** (MD-4, MD-12; no preset row, decision 99): one row per joker showing the uses *left* (∞ = unlimited) and «n usados»; −/+ gives back or takes away one use (0–9, then ∞); sent as limit = used + left.
- **Créditos** (PUB-5, pm plan 47), below «Pantalla completa»: opens the Credits screen (`Credits.svelte`) over the overlay, which hides meanwhile. Glass panel, sections with counts (media, sounds, fonts, glyphs, libraries) from the build's `credits.json`; one row per entry (title, author, licence, provider), source URL as plain text, never a link. No focusable rows: ↑/↓ scroll ~70 %, ←/→ jump between sections, wheel and scrollbar; `Esc`/`Backspace`/pad B or the close button go back to the overlay. Generator and `CREDITS.md`: `17-publishing.md`.
- No language rows (D-96): the language changes only on Start.
- **«Preguntas marcadas»** (MD-6, every mode; decision 60 merged «Reportar pregunta» into the flag): the flagged questions (`FlagList.svelte`) over the overlay: newest first, date, id, question, answer (hidden for the question still on screen), player, level, note; «Copiar» per flag and «Copiar todo» (plain text, one block per flag with a `¡Trivia! #<id> · <lang> · v<version> · pool <hash> · <date>` header, decision 142), else a selectable `<pre>`. «Enviar» per flag and «Enviar todas» (unsent ones, stops at the first failure) only when the shell's `report:available` says so (plan 93): confirm with the privacy text before the session's first send; per flag «Enviando…», «Enviada <date>» (`reported_on`, sending again possible) or the failure in words (no connection, try tomorrow, closed, failed) next to the copy buttons.
- **By mode** (D-74): cheats only in gamemaster mode; «Solo o en grupo»: general part plus a read-only column «Comodines de esta partida» (uses left) and the game's choice.
- **The game's choice** (plan 29), read-only (↑/↓ skip it): two labelled rows: «Edad: Adolescentes» (or «Edad: Dificultad 3–9», D-88), «Paquetes de preguntas: Paquete básico, …» (active bundles, base first; plan 125). From `settings` via `gameChoice`; missing keys read as the locale's defaults. Not in the HUD; changed mid-game only with «Ajustes de la partida».
- **Keys:** ↑/↓ walk the items in order (general, cheats, jokers), ←/→ change a row's value (volume, joker, ‹ › of «Cambiar pregunta» / «Saltar a nivel»), on a plain item jump to the next column at the same height; `Enter`/A runs; `Esc`/Start closes, pad B leaves; mouse hover selects, click runs, −/+ and ‹ › buttons.
- **Flag for review** (GM-5, D-47, decision 60) is not in the menu: a small faint flag next to the ☰ (`M`, pad Select) opens a dialog (`FlagDialog.svelte`): «¿Marcar esta pregunta?», an optional note (keyboard straight into the field; pad: A on the field opens the letter picker with digits and punctuation; later the Steam Deck on-screen keyboard), `Enter` flags, `Esc`/`Backspace`/B cancel; media pauses meanwhile. On a flagged question: «Pregunta marcada», save the note or «Quitar marca». The question stays.
- **Question ID** for debugging, in small type: the question on screen, or else the last one answered («última»). The ID gives nothing away, and it finds the question in `authoring/data/questions.json` and the review tool. The ID links to `/review/<id>` (new tab), next to links to the stats pages (`/stats/categories`, `/stats/difficulty`).
- **Demo de efectos** (later): play every transition and effect for testing on the TV (B-3).

The detailed action set and any extra keys are owned by `05-gamemaster-controls.md` (GM-2). This plan only fixes that the overlay exists and opens with `Esc`.

## Input
**Rule (IN-1): no action without a clickable control.** A key is a shortcut shown on its button (`<kbd>`), never the only way. The overlay opens with `Esc` or the faint ☰ button in the top right corner.

Everything works with a mouse and with the keyboard of the TV machine (OQ-11): `Enter`/`Space` = continue or confirm, `1`–`4` / `A`–`D` = pick a card or an answer (Choice: an age group; ↑/↓ lines and ←/→ values on the configure screen; a mode's letter picks it, es `A` `G`; `P` «Personalizar partida»; Bundles: a bundle's letter selects or toggles it), `R` = replay media, `S` `P` `F` `T` `X` = jokers (09, D-30), `Backspace` = unlock or cancel, (answers off, D-105) `Enter` / pad A = the padlock reveal, `M` = flag the question for review (GM-5), `Esc` = admin overlay. A clicker or phone remote can map to these later.

**Rule (IN-2, IN-3): actions, not keys.** Screens and dialogs listen to actions from `app/client/src/lib/input.svelte.ts` (`pushScope`), never to `keydown`; `grep -rn "keydown\|KeyboardEvent" app/client/src` lists only that file. Each screen and dialog declares a focus default (`data-focus-default`) and a `root`, so arrows + `Enter` + `Esc`/`Backspace` play it (spatial focus, ring, memory: `lib/focus.ts`, plan 44). ☰ and flag stay unfocusable (`data-nofocus`).

**Rule (plan 113): actions are press edges, except `peek`.** The one hold intent: `{ type: "peek", down }`, down on press, up on release (key `keyup`, pad release edge); a held peek always releases on window `blur`, hidden page, pad loop inactive or disconnect, and a modal scope push.

**Rule (IN-5): prompts through `<Prompt>`.** A key hint is `<Prompt action="…" />` (`app/client/src/game/Prompt.svelte`): the key with keyboard or mouse, the pad's glyph (`Glyph.svelte`, Xbox or PlayStation set) after any pad input. The switch rule (plan 156): the last input wins: key press, mouse move or click → keys; any pad button or stick past the dead zone → glyphs; a control without a pad binding shows no glyph. No raw `<kbd>` in screens; `grep -rn "<kbd" app/client/src/game` lists only `Prompt.svelte`. Props: `pad` (the pad's action where it differs, e.g. cancel: `Esc` / B), `padOnly`, `hold` (keep the space), `off` (no glyph right now), `fixed`.

**Debugging keys:** the dev browser runs the Vimium extension, which grabs single-letter keys before the page sees them (`r` reloads the page, which lands on Start). When a key press doesn't work, first ask the developer whether Vimium is disabled for the page before you look for a bug in the code.

## Implementation notes
- The game is the start page `/`; the review tool lives at `/review` (D-25). It is a Svelte state machine (`app/client/src/game/`), and each state is a component.
- **Placeholders (D-25):** none left (2026-10-12, plan 31); `grep -rn PLACEHOLDER app/client/src` is empty. The «medio no disponible» chip in `question/Card.svelte` is a runtime fallback for a missing media file, not a placeholder. A `Transition` wrapper owns the black layer and the audio fades.
- Game state lives on the server (SQLite, D-4) and is written on every final answer, so a page reload or crash resumes at the same level (GF-4).
- **Size rule (SW-4, plan 46):** font sizes only as multiples of `--u`, at least 0.9 u (10, "Scale"); no media queries or separate Deck layout. Checked at 1280×800, 1280×720, 1920×1080 and 4K with a throw-away Playwright walk (pm decision 6). Only the credit line and the bottom of «Respuesta final» sit in the 4 % margin (pm decision 52).
- Animations use CSS transitions or keyframes plus the canvas for fireworks. They respect a "reduced motion" admin toggle (no effect on sound).

## Tasks
- [x] UI-1 Define the visual style (fonts, colours, mood board), including the look of the tower blocks (D-22). *2026-10-06: `10-visual-design.md` (D-29), implemented (VD-2..VD-8), confirmed (VD-1).*
- [x] UI-2 Design the question screen layout with the image overlay, answers, padlock and final-answer button. *2026-10-06: VD-4.*
- [x] UI-3 Design the tower component: foundation, 12 tapering block slots, block variants, drop and settle animation. *2026-10-06: VD-7. The whole tower fits on screen, so no camera follow is needed.*
- [x] UI-4 Design the reveal, Correct, Wrong and Victory animations. *2026-10-06: reveal pop/shake, Wrong desaturates with a vignette and the tower crumbles, Victory with crown and gold stage; the fireworks are UI-9. Fireworks done with UI-9.*
- [-] UI-5 ~~Optional: sound effects and music.~~ Sound is now required (D-21); split into UI-8 and UI-10.
- [x] UI-6 Test on the actual TV (overscan, resolution, viewing distance, volume levels, transition timings). *2026-10-07: the developer declared the game living-room ready.*
- [x] UI-7 Implement the screen state machine and the shared transition routine (fade, black, input lock). *2026-10-06: `app/client/src/game/Game.svelte` (D-25); no preloading yet (`PLACEHOLDER(UI-7)`). Fixed: a new game state that the old screen can't show (after an answer, undo, skip, Paso, a Snipe hit) is now applied behind the black (`go(…, apply)`); before, «Esta pantalla no tiene datos» flashed during the fade. 2026-10-12 (plan 31): preloading done; only Question waits (`ready()`, max `PRELOAD_MAX_MS` = 2 s), media starts with the fade-in (`start()`); a page reload and Bájale/Cambiazo swaps inside Question don't wait.*
- [x] UI-8 Audio engine: AudioContext, three channels with gain, fades and crossfades, three gapless music loops, unlock on the first click, synthesized fallbacks. *2026-10-06: `app/client/src/game/sound.svelte.ts`. No sound files yet (UI-10), so all of it is synthesized: the three loops are one generated theme (A minor, i–VI–III–V) at 76/96/120 bpm with a lookahead scheduler (normal: pad + soft pulse; question: + ticking; submitted: heartbeat, timpani roll, a pad that creeps upwards); every effect name maps to a small recipe (whoosh, paper flick, pop, lock clunk/open, boom, block thud rising with the level, fanfare, sad trombone, rewind, menu blips, joker sounds). Developer feedback: the boom into ¡Correcto! didn't fit; it is now synthesized applause (3 s, a longer «gran aplausos» into Victory); Wrong keeps the boom. Menu blips played 15 % lower (developer, 2026-10-17: too high). A stepper or switch change (joker counts, configure lines, Esc rows, bundle tiles) plays `tick`. Music fades 600/800 ms on screen changes, crossfades 300 ms into «submitted», ducks to 50 % while a joker plays. Audio unlocks on the first click or key. The captions placeholder is gone.*
- [x] UI-9 Fireworks overlay: canvas with at least 4 variants, random pick, finale mode. *2026-10-06: `app/client/src/game/Fireworks.svelte`, hand-written particles on a full-screen canvas: rockets with bursts, confetti cannons from both bottom corners, ring and heart bursts, sparkler figure-eights, falling stars (one at random on ¡Correcto!); Victory plays all five in sequence plus a final volley (~13 s). Launch, burst, cannon, sparkler and star sounds are synthesized. Preview over the Start screen: `/?fuegos=rockets|confetti|shapes|sparklers|stars|finale`. Off with reduced motion.*
- [~] UI-10 Source sound assets (CC0/CC BY), add `app/client/public/audio/CREDITS.md`. *2026-10-06: the developer found the synthesized applause and drum roll low quality; recorded ones from Wikimedia Commons now replace them (`aplausos.m4a` CC0, `aplausos-gran.m4a` public domain, `redoble.m4a` US Air Force Band, public domain; AAC, loudness-normalized, credits in `CREDITS.md`). `sound.svelte.ts` decodes them after the unlock and falls back to synthesis if one is missing. Converted with ffmpeg from `nix shell nixpkgs#ffmpeg-headless` (not a project dependency). Second round, also from Commons: fanfare (US Air Force band, public domain), sad trombone (Joe Lamb, CC BY 3.0), padlock close/open (SpaceJoe, CC0), page flick, block thud and firework burst (pdsounds.org, public domain), glass shatter (Gravity Sound, CC BY 4.0), stamp (Subhashish Panigrahi, CC BY 3.0); 12 files, ~700 kB. Still synthesized: the three music loops, whooshes, pops, menu blips, the joker shimmer, slide whistle, shredder, heartbeat, rewind. Commons had no usable whoosh (only spoken-word recordings); Kenney.nl's CC0 packs are the next source to try. CC BY credits stay in `CREDITS.md`; no credits screen in the game (developer, 2026-10-06). The remaining synthesized sounds are fine for now (developer, 2026-10-06).*
- [x] UI-11 Question selection screen: 4 quirky cards, deal-in, pick sound, chosen-card animation. *2026-10-06: envelopes with wax seals, tilt, deal-in, hover lift, chosen card pulses and the others slide off. A replaced card deals in with «¡Nueva!» (JK-6). Tear-open: the seal cracks off, the flap rips away along a ragged edge with a paper-tear sound, and a lined letter with «?» slides out of the envelope; `PICK_MS` is now 1000 ms (`app/client/src/game/Game.svelte`, `timing.ts`).*
- [x] UI-12 Lock-in mechanic: answer lock, padlock reveal of «Respuesta final», unlock (reverse animation), submit, level-dependent wait, reveal. *2026-10-06: the big padlock shakes, opens and swings away; unlocking swings it back.*
- [x] UI-13 Admin overlay on `Esc`: pause/resume, volume, skip, undo, restart, fullscreen. *2026-10-06: `app/client/src/game/Overlay.svelte`; «Saltar y quemar para todos» added (GM-4); volume sliders for music, effects and question media (←/→ in 10 % steps) and «Sonido: encendido/apagado», remembered in `localStorage`.*
- [x] UI-14 Consolation and milestone copy (Spanish), several variants per level band. *2026-10-06: `app/client/src/game/copy.ts`.*
- [x] UI-16 Player screen: name list, new name entry, greeting; player name on Start («Continuar») and Level (D-28). *2026-10-06: `app/client/src/game/Player.svelte`: up to 9 known names (keys `1`–`9`, with games and wins), typing any letter starts a new name, `Enter` plays; the supply report shows if the pool can't fill a game for that player; «¡Hola, …!» before Level. The idle animation is the shared stage (drifting «?»).*
- [x] UI-15 Make room for the joker tray and hint notes in the Question layout (UI-2) and the read-only tray on Level/Select; joker work itself is JK-4..JK-9 (09). *2026-10-06: with JK-4.*
