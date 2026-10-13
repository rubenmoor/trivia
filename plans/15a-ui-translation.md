# 15a — UI Translation

**Status:** stub

Sub-plan of [15](15-i18n.md). Translates everything on screen that isn't a question: buttons, jokers, the overlay, milestone and consolation lines (UI-14), errors, the credits screen, and the Steam store page. This is small, and the extraction can start now without changing what the family sees.

## Approach
- **No i18n library.** A tiny `t(key, params)` in `app/client/src/lib/i18n.ts` with one catalog per language (`app/client/src/locales/es.ts`, `en.ts`, …) as typed TypeScript objects, so a missing key is a type error (`npm run check`). Plurals via `Intl.PluralRules`, numbers via `Intl.NumberFormat`.
- **Copy with variants** (`copy.ts`: several milestone and consolation lines per level) stays as arrays per language; translations don't have to match the count.
- **Joker names are content, not labels:** «Soplo», «Paso», «Bájale», «Cambiazo», «Francotirador» are playful Spanish names. Each language gets its own playful names, not literal translations.
- **Keyboard keys follow the names today** (`S` Soplo, `P` Paso, `F`, `T`, `X`). Options: language-dependent keys from the catalog, or neutral keys for all languages (e.g. `Q W E R T` in a row, or `F1`–`F5`). Decide in LUI-4. `A`–`D` stay for the answers everywhere.
- **Fonts:** Baloo 2 and Nunito (VD-3) cover Latin scripts, including Vietnamese with Baloo 2. Cyrillic, Greek, CJK or Arabic would need other fonts and RTL work. The launch stays with Latin-script languages.
- **Text length:** German and French run 20–35 % longer than Spanish or English. Every screen gets a check with the longest language (pseudo-locale `xx` that pads strings by 40 % and adds accents, for testing).
- **Printable cards** (`/comodines`, JK-11) and the review tool: the cards are translated with the rest; the review tool stays Spanish/English for the author.
- **Translation work:** Claude drafts the catalogs; a native speaker checks each launch language (playtest, not only a read-through).

## Mode names (Spanish, for the catalog)
English first (D-74); Spanish forms for `es`. Only «Solo o en grupo» is fixed; the rest are proposals for the gamemaster.
- `gamemaster` Gamemaster mode → «Modo anfitrión» (proposal)
- `solo` Alone or as group → «Solo o en grupo» (fixed)
- `rr-coop` Round-robin co-op → «Por turnos en equipo» (proposal)
- `rr-competitive` Round-robin competitive → «Por turnos, todos contra todos» (proposal)
- `timed` Competitive (timed) → «Contrarreloj» (proposal)

## Tasks
- [x] LUI-1 `t()` helper and the `es` catalog; move every string from `copy.ts` and the components into it. No visible change (check with `grep` for Spanish characters left in `app/client/src/game`).
  - Done 2026-10-12 (pm plan 21, D-70): `lib/i18n.ts`, `locales/es.ts`, neutral sound cues, `npm run check:literals -w app/client`. Before/after Playwright run (43 screens incl. every joker, overlay, victory, wrong): pixel-identical, same text, `aria-label`/`title`/`placeholder`.
  - Server errors (pm plan 22, D-57): codes + params on the wire; `lib/errors.ts` renders `error.<code>` from `es.ts` if the key exists, else the English `message`.
- [x] LUI-2 Pseudo-locale for length and missing-string tests.
  - Done 2026-10-12 (pm plan 23): `locales/xx.ts`, dev-only `?lang=xx`. Screen walk (throw-away Playwright, D-6) at 1920 × 1080 and 1280 × 1024: no missed literals; shortcut letters (`*Key`) exempt from `xx` too. Overflow: B-17 (Esc overlay with joker budget), B-18 (corner error over the question).
- [x] LUI-3 `en` catalog with English joker names (draft; pm plan 24). Ships at launch (D-78); `de.ts` follows the same path.
  - Done 2026-10-12 (pm task 104, D-89): Hint, Pass & Purge, Fairy, Ms Picky, Trick Shot. Draft, no native-speaker check (LUI-5). New key `joker.skip.pass` for the plain skip button (`es` «Paso», `en` «Just pass»).
  - Joker name candidates (2026-10-12, pm task 102), recommended first; keys stay `S P F T X` until LUI-4.
  - `hint` «Soplo» (pm decision 40): Psst (classroom whisper), Little Bird («a little bird told me»), Nudge, Tip-off, Whisper.
  - `skip` «Paso» (pm decision 41): Hard Pass (cheeky idiom, keeps `P`), Nope, Next!, Dodge, Bye-Bye.
  - `easier` «Bájale» (pm decision 42): Dial Down (matches the dial animation), Ease Up, Go Easy, Simmer Down, Baby Steps.
  - `category` «Cambiazo» (pm decision 43): Switcheroo (sneaky swap), Topic Hop, Plot Twist, Swap Shop.
  - `snipe` «Francotirador» (pm decision 44): Trick Shot (shooting a wrong answer), Sharpshooter, Long Shot, Pot Shot.
- [x] LUI-4 Joker keys per language or neutral keys (pm decision 53; pm plan 69): keys in the catalog per language, mnemonic; collision rule per catalog (single letter, unique per screen, not `A`–`D` where answers show, no digit).
  - Done 2026-10-12 (pm task 455, D-91): `es`/`es-ES` `S P F T X`, `en` `H P F K T`, `de` `Z N G W F`; replay `R`, flag `M`, new game `N` everywhere.
- [ ] LUI-5 Launch catalogs (D-78): `es` (neutral Latin American, es-419), `es-ES` override (only differing strings: regionalisms, `vosotros`), `en`, `de`; native-speaker playtest each (pm plan 69). Later: `zh-Hans`, `ru`, `pt-BR` (milestone 12; need CJK/Cyrillic fonts).
  - German joker name candidates (2026-10-12, pm task 453), recommended first, ≤ 13 characters, mnemonic key in brackets:
  - `hint` «Soplo» (pm decision 54): Spickzettel (S), Psst! (P), Zaunpfahl (Z), Eselsbrücke (E).
  - `skip` «Paso» (pm decision 55): Weg damit! (W), Ich passe (I), Tschüss! (U), Nächste! (N); plain option `joker.skip.pass` draft «Nur passen».
  - `easier` «Bájale» (pm decision 56): Gang runter (G), Halblang (H), Kinderspiel (K), Sachte! (S).
  - `category` «Cambiazo» (pm decision 57): Extrawurst (E), Wunschthema (W), Kehrtwende (K), Themenhopser (T).
  - `snipe` «Francotirador» (pm decision 58): Scharfschütze (X), Kunstschuss (K), Blattschuss (X), Meisterschuss (X).
  - Neutral `es` (pm decision 59): «¡Qué berraquera!» → «¡Qué maravilla!» (`copy.consolation.9`); «Pulsa otra vez» → «Presiona otra vez» (`overlay.confirm`, `es-ES` keeps «Pulsa»).
  - Answered (pm task 455, D-91): Zaunpfahl (Z), Näxt (N), Gang runter (G), Wunschzeit (W), Finte (F); neutral `es` both applied.
  - `es-ES` joker names: no decision; «Soplo», «Paso», «Bájale», «Cambiazo», «Francotirador» all read fine in Spain.
  - Shipping (2026-10-12, pm task 454): `de.ts` draft (recommended joker names, `es` key letters until LUI-4), `es-ES.ts` override (`vosotros`, «vídeo», «Pulsa»), all four in `CATALOGS`, `xx` dev-only; first-start screen now shows on a fresh save. `check:literals`: keys per screen, `{param}` sets, untranslated leaves. Fonts cover every catalog. Walk `de`/`es-ES` at 1920 × 1080 and 1280 × 800 (full `de` game to victory, jokers, overlay, wrong, customize, report list; fresh save; family save copy → no screen, nothing written): no overflow.
  - Overflow fixes (2026-10-12, pm task 456): B-17 (Esc menu capped at the screen, scrolls, selected row in view; «quedan {n}» one line), B-18 (error line beside the flag/menu buttons). `hyphens: auto` for `de` only (decision 61). Re-walk `es`/`es-ES`/`en`/`de`/`xx` at 1920 × 1080 and 1280 × 800 incl. the language screen: no overflow; `es` pixel-identical except those two spots.
  - `/comodines` per language (2026-10-12, pm task 457): `?lang=es|es-ES|en|de`, language links on screen; names, keys, `joker.<id>.rule` and `cards.*` page text from the app catalogs (`catalogFor` in `lib/i18n.ts`); `@page` Letter (0.5 in) for `es`/`en`, A4 (0.84 in × 0.38 in) for `de`/`es-ES`. Chrome print preview: one page, 12 cards each.
- [ ] LUI-6 Store page texts per language (with PUB-8). S5, not milestone 9 (S4). *Plan: pm plan 88 (`es`, `es-ES`, `en`, `de` in `17a-store-page.md`).*

## Playtest
One native speaker per launch catalog (`es` the family, `es-ES`, `en`, `de`), arranged by the gamemaster, plays the real game rather than reading the catalog. The answer goes into that language's pm decision "Playtest passed? (<lang>)"; fixes go to pm task 459 (pm decisions 62 `es`, 63 `es-ES`, 64 `en`, 65 `de`).

- **Setup**: `trivia` (or `trivia-desktop`), media synced; browser/OS language set to the tester's language (`navigator.language`, e.g. `de-DE`, `es-ES`, `en-US`); `es` family: their own save, untouched.
- **First start** (fresh save: move `state/game.json` aside, put it back afterwards):
  - language screen opens, the guess preselected
  - pick another language → screen switches; pick back, confirm
  - reload → no language screen again
  - family save (no `language` field) → never sees the screen
- **Full game** in each mode: Gamemaster mode, Alone or as group; customize dialog, difficulty and bundles
- **Every joker** (`hint`, `skip` incl. the plain pass, `easier`, `category`, `snipe`): name, key letter, prompt, effect line
- **Overlay / Esc menu**: every row incl. the language rows (UI and question language, «not enough questions»)
- **Prompts**: keyboard (key letters match the names) and pad (glyphs + text)
- **Endings**: victory, wrong answer, milestone and consolation lines (several levels)
- **Report dialog**: mark a question (`M`), note, list of marked questions, copy
- **`/comodines?lang=<lang>`** (authoring, :8001): print preview, one page, 12 cards; names, keys, rules read right
- **What to note** (screen + text + suggested fix):
  - wrong tone (stiff, rude, not playful)
  - too long (cut off, wrapped badly, overflows)
  - wrong register (`du`/`Sie`, `tú`/`usted`/`vosotros`, regionalisms)
  - unclear rule (joker or mode not understood without help)
  - anything else that reads like a translation
