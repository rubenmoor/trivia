# 14 — Input: Mouse, Controller, Couch Co-op

**Status:** draft

Part of the Steam plan ([11](11-steam.md)). The keyboard keys shown on the buttons (`A`–`D`, `1`–`4`, the joker letters, `Enter`, `Esc`) are good and stay. Three steps follow, in this order.

## 1. Everything clickable (now)
Every action that has a key must also have a visible control that works with a mouse click or a touch tap. The key chip on a button doesn't change; it is a hint, not the only way.
- Audit: every `keydown` branch in `app/client/src/game/Game.svelte` (Start `N`, Select `1`–`4`, `Enter`/`Space` to continue, `Esc` overlay) and the dialogs (Paso, Cambiazo picker, Francotirador aiming, `Backspace` = back/cancel, the arming timeout).
- Missing today: likely «continue» on Level/Correct screens (it is `Enter`/`Space`), `Esc` for the overlay (needs a small, unobtrusive menu button in a corner), and `Backspace` in dialogs (needs a visible «Atrás»/«Cancelar»).
- Rule for new UI from now on: no action without a clickable control (add to `04-ui-tv-display.md`).

## 2. Controller support (S3)
**How it works:** the browser [Gamepad API](https://developer.mozilla.org/docs/Web/API/Gamepad_API) works in Chromium, and so inside Electron (18). With the "standard" mapping, Xbox-style controllers show up the same everywhere. On Steam, **Steam Input** translates almost every controller (PlayStation, Switch, Steam Controller, the Deck's own controls) into a virtual Xbox controller by default. So the game only needs to handle one layout. There is no need to talk to the Steam Input API at first.

- **An action layer** between devices and screens: `confirm`, `back`, `menu`, `answer(1..4)`, `joker(name)`, `navigate(direction)`. The keyboard, mouse and gamepad all produce these actions; screens listen only to actions. This replaces the key handling scattered in `Game.svelte`.
- **Focus navigation:** with a controller, the D-pad / left stick moves a visible focus ring (the sky-blue focus of D-29) between buttons; `A` = confirm, `B` = back, `Start` = menu.
- **Direct buttons** (pm decision 9): on the Question screen `Y`/`B`/`X`/`A` pick answers by position (top-left, top-right, bottom-left, bottom-right; tiles get a glyph next to the letter), `RT` submits, `LT` unlocks; `LB`/`RB` move focus through the joker tray, where `A` arms and plays, `B` disarms. Per-scope pad map: `Scope.pad` in `lib/input.svelte.ts`.
- **Glyphs:** button prompts follow the last-used device: keyboard letters, Xbox glyphs, or PlayStation glyphs (from `Gamepad.id`; later via Steamworks `GetInputTypeForHandle`). The glyph art must be original or from a free set (17).
- **Polling:** the Gamepad API has no events for buttons, so poll it with `requestAnimationFrame` while a gamepad is connected.
- **Steam Deck:** 1280×800 (16:10), built-in controls = gamepad. Deck Verified requires full controller support, readable text and no keyboard needed except for text entry, which means the **player name** needs the on-screen keyboard (Steamworks `ShowFloatingGamepadTextInput`, 18) or an in-game letter picker. *S3: in-game letter picker, plan 46 (`LetterPicker.svelte`, shown only for a pad; 04 "Player"); the Steamworks keyboard may replace it under Steam in S5 (SW-8). Screen check at 1280×800/720 done (SW-4, 18): text ≥ 9 px incl. pad glyph labels; real-Deck check in plan 48.*

## 3. Multiplayer input (later)
For the multiplayer modes in [13](13-game-modes.md) (D-77, `timed` D-80). No phones, no LAN server.
- **One gamepad per player:** the Gamepad API lists up to 4 pads in Chromium (the platform may limit it). Each pad is bound to a player on a "press A to join" screen.
- **Keyboard and mouse:** usable by any player whose turn it is.
- **Shared keyboard:** every player gets one dedicated key (picked on the join screen); pressing it hands that player keyboard and mouse until their turn is done. Covers players without a pad.
- **`timed`:** a claim action that any player can trigger at any time (D-80): a pad button each, or a claim key per player on the shared keyboard (layout in IN-6); the claiming player then gets keyboard and mouse (or answers on their pad) for the 6 s.
- **Remote Play Together:** Steam streams the game to remote friends and their input arrives as extra virtual controllers, so it works for free once local multi-controller input works.

## Tasks
- [x] IN-1 Audit and fix: every keyboard action has a clickable control (menu button for `Esc`, visible «Continuar», «Atrás»/«Cancelar» in dialogs). Add the rule to `04-ui-tv-display.md`. *2026-10-07: missing were the overlay (now a faint ☰ button top right, never focused, so a stray `Enter` can't open it; the error box moved below it), continue on Level and Correct (now «Seguir» buttons), cancel while aiming the Francotirador («Cancelar» in the aiming hint) and confirming an armed joker (the «¿Usar …?» bubble is clickable). Already clickable: Start, Player (incl. delete), the cards, answers and unlock, «Respuesta final», replay, the Paso dialog and the Cambiazo picker. Rule added to 04 ("Input").*
- [x] IN-2 Action layer: keyboard and mouse produce actions; screens listen to actions only. *Plan: pm plan 44. 2026-10-12: `lib/input.svelte.ts` (actions, keymap, scope stack); Game, Overlay, Player, Question (answering, armed joker, Paso, Francotirador) and the Cambiazo picker push scopes; no `keydown` elsewhere.*
- [x] IN-3 Focus navigation model for every screen (spatial focus, focus ring, focus memory per screen). *Plan: pm plan 44. 2026-10-12: `lib/focus.ts` (nearest control by rects, ring via `[data-nav]`, memory per scope, dialogs give focus back); every screen and dialog declares `data-focus-default`; `Enter` presses the ring's control, else the screen's default (as before); on a locked answer it submits. Rule in 04 ("Input"). Choice, report and settings screens: follow-up tasks in pm plans 29 and 36.*
- [x] IN-4 Gamepad input: polling, standard mapping, direct answer buttons and joker access (design first). *Plan: pm plan 45; design: pm decision 9. 2026-10-12: `lib/gamepad.ts` (pure core: `step`, mapping) + `lib/gamepad.svelte.ts` (rAF loop, `padStyle`); `Scope.pad` per screen (Question: Y/B/X/A pick, RT submit, LT unlock, LB/RB into the tray); B leaves the overlay (pad only). Full game walked headless with a fake pad (task 352); real-pad check by the gamemaster pending.*
- [x] IN-5 Button glyphs per last-used device; glyph assets with a clear license. *Plan: pm plan 45. 2026-10-12: `Glyph.svelte` (xbox + playstation, drawn in-house), `Prompt.svelte` replaces every `<kbd>`; with a pad, A shows only on the ringed control and glyphs hide where the button does nothing (dialog up, struck answer).*
- [ ] IN-6 Later: join screen ("press A to join" per pad, a dedicated key per keyboard player), player binding (pad ↔ player, key ↔ player), shared-keyboard handover, the claim action for `timed` (per-player claim keys; the claimer holds keyboard and mouse for the 6 s; with MD-8/MD-9, D-77, D-80).
- [x] IN-7 Phones as buzzers? *2026-10-12: no phones (D-77); per-player gamepads + shared keyboard instead.*
