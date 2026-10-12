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
- [ ] LUI-3 `en` catalog with English joker names (draft; pm plan 24). Ships at launch (D-78); `de.ts` follows the same path.
  - Joker name candidates (2026-10-12, pm task 102), recommended first; keys stay `S P F T X` until LUI-4.
  - `hint` «Soplo» (pm decision 40): Psst (classroom whisper), Little Bird («a little bird told me»), Nudge, Tip-off, Whisper.
  - `skip` «Paso» (pm decision 41): Hard Pass (cheeky idiom, keeps `P`), Nope, Next!, Dodge, Bye-Bye.
  - `easier` «Bájale» (pm decision 42): Dial Down (matches the dial animation), Ease Up, Go Easy, Simmer Down, Baby Steps.
  - `category` «Cambiazo» (pm decision 43): Switcheroo (sneaky swap), Topic Hop, Plot Twist, Swap Shop.
  - `snipe` «Francotirador» (pm decision 44): Trick Shot (shooting a wrong answer), Sharpshooter, Long Shot, Pot Shot.
- [ ] LUI-4 Joker keys per language or neutral keys (decision; pm plan 69).
- [ ] LUI-5 Launch catalogs (D-78): `es` (neutral Latin American, es-419), `es-ES` override (only differing strings: regionalisms, `vosotros`), `en`, `de`; native-speaker playtest each (pm plan 69). Later: `zh-Hans`, `ru`, `pt-BR` (milestone 12; need CJK/Cyrillic fonts).
- [ ] LUI-6 Store page texts per language (with PUB-8). S5, not milestone 9 (S4).
