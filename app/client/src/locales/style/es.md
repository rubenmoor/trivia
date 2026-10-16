# Style guide: `es` (Latin American Spanish)

How the UI talks in `es.ts`, the source catalog: neutral Latin American Spanish (es-419, D-78), playful and short, for a family in front of a TV. Read this before changing a string in `es.ts`; the family's game changes only in strings a pm decision names (D-59, plan 100). New bad patterns found in review go into the last section.

## Glossary
Fixed terms; use them as written, never a synonym.
- Modes: «Modo anfitrión» (`mode.gamemaster`), «Solo o en grupo» (`mode.solo`); the role: «el anfitrión» («Trucos del anfitrión»)
- Jokers: «comodín»; names «Soplo» (S), «Paso y fuera» (P), «Hada madrina» (H), «Doña Exigente» (E), «Tiro mágico» (T) (D-108, decision 210); plain skip «Solo paso»
- Level: «nivel»; the tower, the top: «la torre», «la cima», «la corona»
- Question, answer, topic: «pregunta», «respuesta», «tema» (category on screen); a question card: «carta»
- Question bundle: «paquete de preguntas» (Steam DLC, decision 50; never «Temas»); base bundle «paquete básico»; bundle names from `app/data/bundles.json` («Paquete básico», «Regional: Colombia»)
- Age group: «Edad» (label), «grupo de edad»
- Difficulty: «Dificultad», «Desde» / «Hasta», «A medida»
- Flag: «marcar» / «Marcar para revisar», «Preguntas marcadas», «reporte»
- Esc menu: «Pausa»; «Volver al menú principal» (`overlay.restart`, to the start screen); «Salir del juego» (`overlay.quit`, desktop only); «Ajustes de la partida» (`overlay.settings`, gamemaster dialog: difficulty, bundles, answers; task 1127)
- Start screen: «menú principal» when named
- Steam terms as Steam writes them in Spanish: «logros de Steam» (never bare «logros»), «Steam Cloud», «Steam Deck», «Workshop de Steam»
- Media: «video» (not «vídeo»), «audio», «imagen»
- Mods: «mod», «encender» / «apagar»

## Address
- Players: «ustedes» (D-6), the group in front of the TV: «Elijan una respuesta», «¡Ganaron!», «Escriban su nombre»
- «tú» only in the one-person setup dialogs, as today: language screen («Elige el idioma»), telemetry consent («¿Nos ayudas…?»); don't spread it
- Impersonal or infinitive where nobody is addressed: notices, errors, credits («No se pudo guardar», «Imprimir al 100 %»)
- Neutral words over regionalisms (decision 59): «Presiona», «¡Qué maravilla!», no «berraquera», «pulsa», «vale»

## Buttons and prompts
- Verb first, imperative («Elijan una pregunta») or infinitive for actions on rows («Saltar pregunta», «Copiar»)
- Short: buttons 1–3 words, about 25 characters; prompts one line at 1280 × 800
- Sentence case: «Personalizar partida», not «Personalizar Partida»; joker and bundle names capitalized as names
- «¡…!» and «¿…?» always paired; exclamations for cheers only, not for menu rows
- «…» (one character, no space) for rows that open a dialog («Ir a pregunta…») and for waiting states («Cargando…»)
- Quotes «…»
- Keys and pad glyphs: shown by the `Prompt` chip, never typed into the text; exception `{key}` in `flag.on` / `flag.off`
- Shortcut letters (`*Key`, `joker.*.key`): one letter, mnemonic in Spanish, unique per screen, not A–D where answers show (LUI-4, `check:literals`)

## Bad patterns
Seen in review; guidance, not a lint. Wrong → right.
- Esc row that names the wrong target: «Terminar partida (configurar otra)» → «Volver al menú principal» (TV check 2026-10-13)
- Bare «logros»: «Una partida personalizada no gana logros.» → «… no gana logros de Steam.» (TV check)
- Parenthesized explanations in a row: «Terminar partida (configurar otra)» → say the effect in the name
- Spain-only words in `es`: «Pulsa otra vez» → «Presiona otra vez» (decision 59)
- Old joker names, don't use (D-108): «Paso» → «Paso y fuera», «Bájale» → «Hada madrina», «Cambiazo» → «Doña Exigente», «Francotirador» → «Tiro mágico»
