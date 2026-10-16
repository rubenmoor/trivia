# Style guide: `en` (English)

How the UI talks in `en.ts`: plain, friendly English for a family or a single player at a TV; playful in cheers and joker names, flat in menus and notices. Read this before changing a string in `en.ts`; new bad patterns found in review go into the last section.

## Glossary
Fixed terms; use them as written, never a synonym.
- Modes: «Gamemaster mode» (`mode.gamemaster`), «Alone or as group» (`mode.solo`, D-74); the role: «the gamemaster» («Gamemaster cheats»)
- Jokers: «joker»; names «Hint» (H), «Pass & Purge» (P), «Fairy» (F), «Ms Picky» (K), «Trick Shot» (T) (D-89, D-91, kept by D-108); plain skip «Just pass»
- Level: «level»; the tower, the top, the crown
- Question, answer, topic: «question», «answer», «topic» (category on screen); a question card: «card»
- Question bundle: «question bundle» (decision 50; «bundle» once the context is clear); base bundle «base bundle»; bundle names from `app/data/names.en.json` («Base bundle», «Regional: Colombia»)
- Age group: «Age» (label), «age group»
- Difficulty: «Difficulty», «From» / «To», «Custom»
- Flag: «flag» / «Flag for review», «Flag this question», «Flagged questions», «report» (gallery review 2026-10-14; never «mark»)
- Esc menu: «Paused»; «Back to main menu» (`overlay.restart`, to the start screen); «Quit game» (`overlay.quit`, desktop only); «Game settings» (`overlay.settings`, gamemaster dialog: difficulty, bundles, answers; task 1127)
- Start screen: «main menu» when named
- Steam terms as Steam writes them: «Steam achievements» (never bare «achievements»), «Steam Cloud», «Steam Deck», «Steam Workshop»
- Spelling: US («Customize», «color»), sheet «Letter»

## Address
- «you» for one player or the whole group; never «you all», «you guys», «yourselves»
- Imperative for prompts («Pick an answer»), statements for notices («Couldn't save.»)

## Buttons and prompts
- Verb first: «Skip question», «Save note», «Turn on»
- Short: buttons 1–3 words, about 25 characters; prompts one line at 1280 × 800
- Sentence case: «Customize game», not «Customize Game»; joker and bundle names capitalized as names
- Contractions are fine («Couldn't», «Who's playing?»)
- «…» (one character, no space) for waiting states only («Loading…»); not on rows that open a dialog («Go to question»)
- Dialog titles that state the action: no «?» («Flag this question»)
- Quotes “…”
- Keys and pad glyphs: shown by the `Prompt` chip, never typed into the text; exception `{key}` in `flag.on` / `flag.off`
- Shortcut letters: one letter, mnemonic in English, unique per screen, not A–D where answers show (LUI-4, `check:literals`)

## Bad patterns
Seen in review; guidance, not a lint. Wrong → right.
- Esc row that names the wrong target: «End game (set up another)» → «Back to main menu» (TV check 2026-10-13)
- Bare «achievements»: «A customized game earns no achievements.» → «… earns no Steam achievements.» (TV check)
- Parenthesized explanations in a row: «End game (set up another)» → say the effect in the name
- Plural-only address: «copy it yourselves» → «copy it yourself» or «copy it by hand» (`flag.copyFailed`)
- «mark» for flagging a question: «Mark this question?», «Marked questions» → «Flag this question», «Flagged questions» (gallery review 2026-10-14)
- Dialog body that restates the title: «It gets noted for review; the question stays.» → «Optional: Tell us the issue» (`flag.body`)
- «…» on a menu row: «Go to question…» → «Go to question» (`overlay.goTo`)
- Vague purge wording: «Pass & Purge: goodbye to “…”» → «Remove all questions of the topic “…”» (`joker.skip.purge`, review 2026-10-16)
