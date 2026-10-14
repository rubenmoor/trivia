# Style guide: `de` (German)

How the UI talks in `de.ts`: natural German for whoever sits at the TV, one player or a family, so it never assumes a plural audience. Prompts and buttons are infinitives, notices are impersonal, cheers stay playful. Read this before changing a string in `de.ts`; new bad patterns found in review go into the last section.

## Glossary
Fixed terms; use them as written, never a synonym.
- Modes: «Spielleitermodus» (`mode.gamemaster`, TV check 2026-10-13), «Allein oder in der Gruppe» (`mode.solo`); the role: «die Spielleitung» («Tricks der Spielleitung», «Die Spielleitung steuert alles»)
- Jokers: «Joker»; names «Zaunpfahl» (Z), «Näxt» (N), «Gang runter» (G), «Wunschzeit» (W), «Finte» (F) (decisions 54–58, D-91); plain skip «Nur passen»
- Level: «Stufe»; the tower, the top: «Turm», «Gipfel», «Krone»
- Question, answer, topic: «Frage», «Antwort», «Thema» (category on screen); a question card: «Karte»
- Question bundle: «Fragenpaket» (decision 50; «Paket» once the context is clear); base bundle «Grundpaket»; bundle names from `app/data/names.de.json` («Basis», «Regional: Kolumbien»)
- Age group: «Alter» (label), «Altersgruppe»
- Difficulty: «Schwierigkeit», «Von» / «Bis», «Eigene»
- Flag: «markieren» / «Zum Prüfen markieren», «Markierte Fragen», «Meldung»
- Esc menu: «Pause»; «Zurück zum Hauptmenü» (`overlay.restart`, to the start screen); «Spiel beenden» (`overlay.quit`, desktop only, closes the game)
- Start screen: «Hauptmenü» when named
- Steam terms as Steam writes them in German: «Steam-Erfolge» (never bare «Erfolge»), «Steam Cloud», «Steam Deck», «Steam-Workshop»
- Credits: «Mitwirkende»

## Address
- Never assume a plural: no «ihr», «euch», «euer», no «-t» plural imperatives («Wählt», «Schreibt», «Zielt»)
- Never «Sie»
- Prompts and buttons: infinitive («Frage wählen», «Namen eingeben», «Notiz speichern»)
- Notices, rules, errors, cheers: impersonal or about the thing («Schon bei diesem Thema», «Darauf kann man stolz sein!», «Die Krone wartet schon!»)
- «du» only where no infinitive or impersonal form works; decide per string and list it here
  - none so far

## Buttons and prompts
- Infinitive with the verb last: «Frage überspringen», «Alle senden»; short nouns are fine for toggles («Vollbild», «Ton: an»)
- Short: buttons 1–3 words, about 30 characters (German runs 20–35 % longer, hyphenation on, decision 61); prompts one line at 1280 × 800
- German capitalisation, otherwise sentence style; joker names as written in the glossary
- «!» for cheers only, not for menu rows
- «…» (one character, no space) for rows that open a dialog («Zu Frage gehen…») and for waiting states («Lädt…»)
- Quotes „…“
- Keys and pad glyphs: shown by the `Prompt` chip, never typed into the text; exception `{key}` in `flag.on` / `flag.off`
- Shortcut letters: one letter, mnemonic in German, unique per screen, not A–D where answers show (LUI-4, `check:literals`)

## Bad patterns
Seen in review; guidance, not a lint. Wrong → right.
- Plural address (TV check 2026-10-13; fixed in task 800: `flag.pickerTitle`, `flag.copyFailed`, `joker.*.rule`, `joker.category.title`, `joker.snipe.aim`, `outlook.none`, `outlook.exhausted`, `picker.title`, `screen.player.firstLabel`, `screen.level.again`, `screen.select.title`, `screen.question.prompt`, `copy.*`, `error.category_same`, `error.snipe_no_repeat`):
  - «Wählt eine Frage» → «Frage wählen»
  - «Schreibt euren Namen» → «Namen eingeben»
  - «Welches Thema wollt ihr?» → «Welches Thema soll es sein?»
  - «Ihr kennt schon alle Fragen aus: {list}» → «Alle Fragen schon gesehen: {list}»
  - «Darauf könnt ihr stolz sein.» → «Darauf kann man stolz sein!»
  - «ihr seid schon bei diesem Thema» → «schon bei diesem Thema»
  - «Zielt auf die falsche Antwort» → «Ziel: die falsche Antwort» (`joker.snipe.aim`)
  - «Trefft ihr die richtige, …» → «Ein Treffer auf die richtige: …» (`joker.snipe.rule`)
- Singular «du» imperative where an infinitive works: «wähle genau ein Grundpaket» → «genau ein Grundpaket wählen» (`error.base_bundle_count`)
- Mode name as a phrase: «Mit Spielleitung» → «Spielleitermodus» (TV check)
- Esc row that names the wrong target and clashes with quit: «Spiel beenden (neues einrichten)» → «Zurück zum Hauptmenü» (TV check)
- Bare «Erfolge»: «Ein angepasstes Spiel bringt keine Erfolge.» → «… bringt keine Steam-Erfolge.» (TV check)
- Spanish/French quotes: «{field}» → „{field}“ (`mods.error.bad_field`)
- Ellipsis with a space: «Wird gesendet …» → «Wird gesendet…» (`flag.sending`)
