# 15a — UI Translation

**Status:** stub

Sub-plan of [15](15-i18n.md). Translates everything on screen that isn't a question: buttons, jokers, the overlay, milestone and consolation lines (UI-14), errors, the credits screen, and the Steam store page. This is small, and the extraction can start now without changing what the family sees.

## Approach
- **No i18n library.** A tiny `t(key, params)` in `client/src/lib/i18n.ts` with one catalog per language (`client/src/locales/es.ts`, `en.ts`, …) as typed TypeScript objects, so a missing key is a type error (`npm run check`). Plurals via `Intl.PluralRules`, numbers via `Intl.NumberFormat`.
- **Copy with variants** (`copy.ts`: several milestone and consolation lines per level) stays as arrays per language; translations don't have to match the count.
- **Joker names are content, not labels:** «Soplo», «Paso», «Bájale», «Cambiazo», «Francotirador» are playful Spanish names. Each language gets its own playful names, not literal translations.
- **Keyboard keys follow the names today** (`S` Soplo, `P` Paso, `F`, `T`, `X`). Options: language-dependent keys from the catalog, or neutral keys for all languages (e.g. `Q W E R T` in a row, or `F1`–`F5`). Decide in LUI-4. `A`–`D` stay for the answers everywhere.
- **Fonts:** Baloo 2 and Nunito (VD-3) cover Latin scripts, including Vietnamese with Baloo 2. Cyrillic, Greek, CJK or Arabic would need other fonts and RTL work. The launch stays with Latin-script languages.
- **Text length:** German and French run 20–35 % longer than Spanish or English. Every screen gets a check with the longest language (pseudo-locale `xx` that pads strings by 40 % and adds accents, for testing).
- **Printable cards** (`/comodines`, JK-11) and the review tool: the cards are translated with the rest; the review tool stays Spanish/English for the author.
- **Translation work:** Claude drafts the catalogs; a native speaker checks each launch language (playtest, not only a read-through).

## Tasks
- [ ] LUI-1 `t()` helper and the `es` catalog; move every string from `copy.ts` and the components into it. No visible change (check with `grep` for Spanish characters left in `client/src/game`).
- [ ] LUI-2 Pseudo-locale for length and missing-string tests.
- [ ] LUI-3 `en` catalog with English joker names (draft).
- [ ] LUI-4 Joker keys per language or neutral keys (decision).
- [ ] LUI-5 Further launch languages (after OQ-31); native-speaker playtest each.
- [ ] LUI-6 Store page texts per language (with PUB-8).
