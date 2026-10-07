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
- **Direct buttons:** on the Question screen, `A`/`B`/`X`/`Y` could pick answers directly (answer tiles get a glyph next to the letter), and the bumpers open a joker wheel. To decide when designing (IN-4).
- **Glyphs:** button prompts follow the last-used device: keyboard letters, Xbox glyphs, or PlayStation glyphs (from `Gamepad.id`; later via Steamworks `GetInputTypeForHandle`). The glyph art must be original or from a free set (17).
- **Polling:** the Gamepad API has no events for buttons, so poll it with `requestAnimationFrame` while a gamepad is connected.
- **Steam Deck:** 1280×800 (16:10), built-in controls = gamepad. Deck Verified requires full controller support, readable text and no keyboard needed except for text entry, which means the **player name** needs the on-screen keyboard (Steamworks `ShowFloatingGamepadTextInput`, 18) or an in-game letter picker.

## 3. Couch co-op and competitive input (later)
Depends on the modes in [13](13-game-modes.md) (OQ-37).
- **One controller per player:** the Gamepad API lists up to 4 pads in Chromium (the platform may limit it). Each pad is linked to a player on a "press A to join" screen. 8+ players exceed that, so shared controllers (pass the pad) or phones.
- **Phones as buzzers** (alternative): the game serves a small page on the local network; players join with a QR code. This breaks "offline single machine" only slightly (no internet, just LAN), but it adds a server in the shell and firewall prompts. To decide.
- **Remote Play Together:** Steam streams the game to remote friends and their input arrives as extra virtual controllers, so it works for free once local multi-controller input works.

## Tasks
- [x] IN-1 Audit and fix: every keyboard action has a clickable control (menu button for `Esc`, visible «Continuar», «Atrás»/«Cancelar» in dialogs). Add the rule to `04-ui-tv-display.md`. *2026-10-07: missing were the overlay (now a faint ☰ button top right, never focused, so a stray `Enter` can't open it; the error box moved below it), continue on Level and Correct (now «Seguir» buttons), cancel while aiming the Francotirador («Cancelar» in the aiming hint) and confirming an armed joker (the «¿Usar …?» bubble is clickable). Already clickable: Start, Player (incl. delete), the cards, answers and unlock, «Respuesta final», replay, the Paso dialog and the Cambiazo picker. Rule added to 04 ("Input").*
- [ ] IN-2 Action layer: keyboard and mouse produce actions; screens listen to actions only.
- [ ] IN-3 Focus navigation model for every screen (spatial focus, focus ring, focus memory per screen).
- [ ] IN-4 Gamepad input: polling, standard mapping, direct answer buttons and joker access (design first).
- [ ] IN-5 Button glyphs per last-used device; glyph assets with a clear license.
- [ ] IN-6 Multi-controller join screen and player binding (with MD-8/MD-9).
- [ ] IN-7 Decide on phones as buzzers (OQ-37).
