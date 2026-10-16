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
English first (D-74); Spanish forms for `es`. Only «Solo o en grupo» is fixed; the rest are proposals for the developer.
- `gamemaster` Gamemaster mode → «Modo anfitrión» (proposal)
- `solo` Alone or as group → «Solo o en grupo» (fixed)
- `rr-coop` Round-robin co-op → «Por turnos en equipo» (proposal)
- `rr-competitive` Round-robin competitive → «Por turnos, todos contra todos» (proposal)
- `timed` Competitive (timed) → «Contrarreloj» (proposal)

## Joker names
Milestone 9 defines the joker names again (pm decision 188, pm plan 136): one symbol per joker, the same in every language, and a name made in English first to fit it. `es`, `es-ES` and `de` are translated from the English names; `es` is an exception to D-59, so the family's game gets them too. Replaces pm decisions 40–44 and 54–58 (D-89, D-91's names).

- Rules: ≤ 13 characters, playful, fitting the symbol; key letter mnemonic per catalog (pm decision 53), en Question screen keeps `A`–`D`, `R`, `M` free
- English candidates (recommended first, key in brackets; pm decisions 190–194):
  - `hint`, bulb (190): Bright Idea (B), Brainwave (W), Lightbulb (L), Aha! (H), Hint (H, today)
  - `skip`, door (191): Way Out (W), Door Slam (S), Back Door (K), Escape Hatch (E), Pass & Purge (P, today)
  - `easier`, stairs (192): Step Down (S), Easy Steps (E), Downstairs (W), Baby Steps (Y), Fairy (F, today; would need a wand)
  - `category`, compass (193): Change Course (C), True North (N), Detour (T), Compass (O), Ms Picky (K, today)
  - `snipe`, crosshair (194): Trick Shot (T, today), Sharpshooter (S), Long Shot (L), Pot Shot (O)
- Symbols: none of the candidates needs a new one
- English answers (2026-10-15): all kept, Hint (H), Pass & Purge (P), Fairy (F), Ms Picky (K), Trick Shot (T); symbols for them (pm decision 209, task 1135): bulb with rays, broom, wand with a star, hand pointing at a card, crosshair with a curved arrow
- Translations (pm task 1097), recommended first, key in brackets; Question screen keeps `A`–`D`, `R`, `V`, `M` free:
  - `es` (pm decision 210): `hint` Soplo (S), Pista (S), Pistita (S); `skip` Paso y fuera (P), Paso y purga (P), Paso (P); `easier` Hada madrina (H), Hada (H), Bájale (F); `category` Doña Exigente (E), Quisquillosa (Q), Cambiazo (T); `snipe` Tiro mágico (T), Carambola (L), Francotirador (X)
    - plain skip «Solo paso»; purge «Paso y fuera: adiós al tema «{name}»»; title «Doña Exigente: ¿qué tema quieren?»
  - `es-ES` (pm decision 211): same as `es`; only «os»/«queréis» leaves (`error.joker_spent.*`, `joker.category.title`)
  - `de` (pm decision 212): `hint` Zaunpfahl (Z), Tipp (I), Geistesblitz (G); `skip` Näxt & weg (N), Und tschüss! (U), Weg damit! (W); `easier` Gute Fee (F), Glücksfee (F), Fee (F); `category` Frau Pingelig (P), Frau Mäkelig (K), Wunschzeit (W); `snipe` Trickschuss (T), Kunstschuss (S), Finte (F)
    - purge «Näxt & weg: tschüss, Thema „{name}“»; title «Frau Pingelig: Welches Thema soll es sein?»

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

## Wording and review
The developer's TV check (2026-10-13) found catalogs that read like translations: German plural address, terms that differ from screen to screen, an Esc row that says the wrong thing. Pm plan 100 adds style guides, applies the TV-check fixes and builds a screen gallery the developer reviews per language; flags from the review feed fix passes. Runs before the playtest close-out (pm task 459), so the playtest sees the fixed wording.

- **Style guides** `app/client/src/locales/style/{en,es,es-ES,de}.md` (pm task 799): glossary (modes, jokers, bundles, Esc rows, Steam's own terms), address, buttons and prompts, bad patterns (wrong → right); guidance, not a lint
  - `AGENTS.md` rule: changing UI strings → read the locale's guide first; new bad patterns go into it
  - `de`: never plural, infinitive for prompts and buttons, impersonal elsewhere, «du» only per listed string
  - translation prompts (`authoring/tools/prompts/locale-<l>.md`) get the guide's address and glossary after a pm decision (pm task 801)
- **TV-check fixes** (pm task 800): de «Spielleitermodus»; «Steam achievements» / «logros de Steam» / «Steam-Erfolge»; Esc «Back to main menu» / «Volver al menú principal» / «Zurück zum Hauptmenü» → start screen; «Quit game» / «Salir del juego» / «Spiel beenden» in its own colour; `de` plural sweep; `es` changes only in these strings (D-59)
  - done 2026-10-14: catalogs, `restart()` in `Game.svelte` → Start, `--quit` token in `theme.css`; also `en` `flag.copyFailed` (no «yourselves»), `es-ES` `outlook.none`/`outlook.exhausted` overrides, `de` „…“ quotes and «…» without space
- **Screen gallery** (pm tasks 802, 803): `trivia-gallery` renders every screen and dialog per UI language from a demo save into `work/gallery/`, with the catalog key of each visible text; `trivia-authoring` `/gallery` shows the shots, the developer flags a string with a note (`authoring/data/ui-flags.json`)
  - `trivia-gallery` (task 802): 44 shots per language; `work/gallery/manifest.json`: `{run, commit, locales: {<locale>: {<shot>: {file, items, unmatched}}}}`, an item `{text, box: [x, y, w, h], attr?, keys? | glyph | data, unmatched?}` (`attr`: `aria-label`/`title`/`placeholder`; `glyph`: key caps, answer letters; `data`: content such as questions, names, credits)
- **Flag → fix loop** (pm task 804): one pm decision per language "Screen gallery reviewed? (<lang>)"; a fix task reads the open flags, fixes the catalogs per the guide, adds new bad patterns to the guide, sets `fixed_on`, re-runs the gallery; re-runnable any time
  - done 2026-10-14 (pm task 1026): 14 flags (en, de; es, es-ES nothing to fix); en «mark» → «flag», de «markieren» → «melden» (`flag.*`), `overlay.goTo` without «…», `flag.body` «Optional: Tell us the issue», de `screen.start.subtitle`, `mods.held`; beyond catalogs → pm tasks 1104 (supply notice names the bundle), 1105 (final-answer wait animation)

## Playtest
One native speaker per launch catalog (`es` the family, `es-ES`, `en`, `de`), arranged by the developer, plays the real game rather than reading the catalog. The answer goes into that language's pm decision "Playtest passed? (<lang>)"; fixes go to pm task 459 (pm decisions 62 `es`, 63 `es-ES`, 64 `en`, 65 `de`).

- **Setup**: `trivia` (or `trivia-desktop`), media synced; browser/OS language set to the tester's language (`navigator.language`, e.g. `de-DE`, `es-ES`, `en-US`); `es` family: their own save, untouched.
- **First start** (fresh save: move `state/game.json` aside, put it back afterwards):
  - language screen opens, the guess preselected
  - pick another language → screen switches; pick back, confirm
  - reload → no language screen again
  - family save (no `language` field) → never sees the screen
- **Full game** in each mode: Gamemaster mode, Alone or as group; customize dialog, difficulty and bundles
- **Every joker** (`hint`, `skip` incl. the plain pass, `easier`, `category`, `snipe`): name, key letter, prompt, effect line
- **Overlay / Esc menu**: every row (language rows gone since D-96; Start's language button instead)
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
