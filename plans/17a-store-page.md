# 17a — Store page

**Status:** draft (texts awaiting approval)

Sub-plan of [17](17-publishing.md). Everything the developer pastes into Steamworks' store page admin for the beta (plan 88, PUB-8, LUI-6): texts per store language, AI disclosure, requirements, languages, controller flags, capsules and screenshots. Workers draft and render here; the developer approves through pm decisions and enters them.

## Store texts
Texts per store language for Steamworks → Edit Store Page → "Description" (short description, "About This Game") and the localized name (General Application Settings, D-50). Drafted 2026-10-14 (`task 666`) from the in-game catalogs (`app/client/src/locales/*.ts`) and their style guides; approved per language set through pm decisions "Store texts approved? (<lang>)".

### Fields and limits
- Limits from memory (no web access at the task); recheck in the Steamworks admin at entry
- Name: localized app name, set once before the coming-soon page (D-50); no limit noted
- Short description: max 300 characters, plain text (no BBCode)
- About This Game: BBCode (`[h2]`, `[b]`, `[list][*]`), no hard limit; no links to other stores, no prices
- Feature bullets, privacy line, controller line: inside About This Game (bullets as `[list]`, the two lines as its last paragraphs)
- Steam features named per decision 111: saves need Steam (Steam Cloud per Steam account, plan 87), Steam achievements (plan 86; only uncustomized games outside Gamemaster mode, decisions 19, 74)
- Modes: only the two built ones (`BUILT_MODES`: Gamemaster mode, Alone or as group); the three multiplayer modes of D-74 join the texts when MD-8 ships them, not announced before
- No question count (pool grows; base ~1,000 approved es today)
- Privacy line: says what the build really sends (opt-in telemetry, plan 106; a question report on the player's click, decision 93), not "sends nothing"; the developer confirms in the approval decision
- Language note (en, de): only until `pool.en.json` / `pool.de.json` ship (decision 80; D-96: a language without its pool plays the Spanish questions)

### English (`en`)
- **Name:** Living Room Trivia
- **Short description** (≤ 300):
  > A quiz for the whole family on the TV: answer 12 questions in a row to win. Four age groups from kids to adults, five jokers to get out of a tight spot, and questions with pictures, sounds and videos. Play alone or as a group, or let a gamemaster run the show.
- **About This Game:**
  ```
  [h2]12 in a row to win[/h2]
  Living Room Trivia is a classic quiz for the TV. Everyone in the room plays as one team against the game: answer twelve questions in a row and the crown is yours. One wrong answer and the game is over, so use your jokers well.

  Every game is set for an age group: Kids, Teens, Young adults or Adults. A seven-year-old and a grandparent both get questions they can answer. Some questions show a picture, play a sound or a short video.

  [h2]Two ways to play[/h2]
  [list]
  [*][b]Alone or as group:[/b] one player, or the whole family as one team. Standard jokers, no cheats.
  [*][b]Gamemaster mode:[/b] one person runs the show: sets difficulty, question bundles and jokers, and can skip, swap or undo any question.
  [/list]

  [h2]Five jokers[/h2]
  [list]
  [*][b]Hint:[/b] shows a hint for the question, up to three per question.
  [*][b]Pass & Purge:[/b] swaps the question for another card; if you like, that topic leaves the game.
  [*][b]Fairy:[/b] swaps the question for an easier one on the same topic.
  [*][b]Ms Picky:[/b] you pick another topic.
  [*][b]Trick Shot:[/b] shoot at a wrong answer and it's crossed out. Hit the right one and the level starts over.
  [/list]

  [h2]Features[/h2]
  [list]
  [*]12 questions in a row to the top of the tower
  [*]Two modes: Alone or as group, Gamemaster mode
  [*]Five jokers: Hint, Pass & Purge, Fairy, Ms Picky, Trick Shot
  [*]Four age groups, from kids to adults
  [*]Questions with pictures, sounds and videos
  [*]Free regional question bundles as DLC, off by default
  [*]Made for the family TV, playable on any screen
  [*]Gamepad, keyboard or mouse
  [*]Plays offline
  [*]Saves need Steam: progress is kept per Steam account and synced with Steam Cloud
  [*]Steam achievements in games that aren't customized
  [/list]

  [b]Privacy:[/b] no account of ours, no ads. Player names stay on your computer and in your Steam Cloud. The game only sends something if you allow it: anonymous game stats if you opt in, and a question report when you press Send.

  [b]Controllers:[/b] plays with Xbox and PlayStation gamepads, keyboard or mouse.
  ```
- **Language note** (until `pool.en.json` ships; last paragraph of About This Game):
  > The interface is in English; the questions are in Spanish for now. English questions follow in an update.

### Spanish – Latin America (`es`, es-419)
- **Name:** Trivia en Familia
- **Short description** (≤ 300):
  > Un juego de preguntas para toda la familia frente al televisor: respondan 12 preguntas seguidas para ganar. Cuatro grupos de edad, de niños a adultos, cinco comodines para salir de apuros y preguntas con imagen, sonido y video. Jueguen solos o en grupo, o con un anfitrión que lo maneja todo.
- **About This Game:**
  ```
  [h2]12 seguidas para ganar[/h2]
  Trivia en Familia es un juego de preguntas clásico para el televisor. Todos en la sala juegan como un solo equipo contra el juego: respondan doce preguntas seguidas y la corona es suya. Una respuesta mal y se acaba la partida, así que usen bien sus comodines.

  Cada partida es para un grupo de edad: Niños, Adolescentes, Jóvenes o Adultos. Un niño de siete años y una abuela reciben preguntas que pueden responder. Algunas preguntas muestran una imagen, ponen un sonido o un video corto.

  [h2]Dos formas de jugar[/h2]
  [list]
  [*][b]Solo o en grupo:[/b] un jugador, o toda la familia como un equipo. Comodines estándar, sin trucos.
  [*][b]Modo anfitrión:[/b] una persona lo maneja todo: elige la dificultad, los paquetes de preguntas y los comodines, y puede saltar, cambiar o deshacer cualquier pregunta.
  [/list]

  [h2]Cinco comodines[/h2]
  [list]
  [*][b]Soplo:[/b] muestra una pista de la pregunta, hasta tres por pregunta.
  [*][b]Paso y fuera:[/b] cambia la pregunta por otra carta; si quieren, ese tema sale del juego.
  [*][b]Hada madrina:[/b] cambia la pregunta por una más fácil del mismo tema.
  [*][b]Doña Exigente:[/b] ustedes eligen otro tema.
  [*][b]Tiro mágico:[/b] disparen a una respuesta falsa y queda tachada. Si le dan a la correcta, el nivel vuelve a empezar.
  [/list]

  [h2]Características[/h2]
  [list]
  [*]12 preguntas seguidas hasta la cima de la torre
  [*]Dos modos: Solo o en grupo, Modo anfitrión
  [*]Cinco comodines: Soplo, Paso y fuera, Hada madrina, Doña Exigente, Tiro mágico
  [*]Cuatro grupos de edad, de niños a adultos
  [*]Preguntas con imagen, sonido y video
  [*]Paquetes de preguntas regionales gratis como DLC, apagados por defecto
  [*]Hecho para el televisor de la casa, se juega en cualquier pantalla
  [*]Control, teclado o mouse
  [*]Se juega sin conexión
  [*]Para guardar se necesita Steam: el progreso se guarda por cuenta de Steam y se sincroniza con Steam Cloud
  [*]Logros de Steam en partidas sin personalizar
  [/list]

  [b]Privacidad:[/b] sin cuentas propias, sin anuncios. Los nombres de los jugadores se quedan en su computador y en su Steam Cloud. El juego solo envía algo si ustedes lo permiten: datos anónimos de las partidas si aceptan, y el reporte de una pregunta cuando presionan Enviar.

  [b]Controles:[/b] se juega con controles de Xbox y PlayStation, teclado o mouse.
  ```

### Spanish – Spain (`es-ES`)
Only the fields that differ from `es`: «vosotros», «vídeo», «ordenador», «ratón», «mando» (es-ES style guide); name as `es`.
- **Short description** (≤ 300):
  > Un juego de preguntas para toda la familia frente a la tele: responded 12 preguntas seguidas para ganar. Cuatro grupos de edad, de niños a adultos, cinco comodines para salir de apuros y preguntas con imagen, sonido y vídeo. Jugad solos o en grupo, o con un anfitrión que lo maneja todo.
- **About This Game:** `es` with these replacements
  - «Todos en la sala juegan … respondan doce preguntas seguidas y la corona es suya. … así que usen bien sus comodines.» → «Todos en el salón jugáis como un solo equipo contra el juego: responded doce preguntas seguidas y la corona es vuestra. … así que usad bien vuestros comodines.»
  - «ponen un sonido o un video corto» → «ponen un sonido o un vídeo corto»
  - Paso y fuera: «si quieren» → «si queréis»; Doña Exigente: «ustedes eligen otro tema» → «elegís otro tema»; Tiro mágico: «disparen … Si le dan a la correcta» → «disparad … Si le dais a la correcta»
  - «Preguntas con imagen, sonido y video» → «… vídeo»; «Control, teclado o mouse» → «Mando, teclado o ratón»; «Hecho para el televisor de la casa» → «Hecho para la tele de casa»
  - Privacy: «en su computador y en su Steam Cloud» → «en vuestro ordenador y en vuestro Steam Cloud»; «si ustedes lo permiten: … si aceptan, … cuando presionan Enviar» → «si lo permitís: … si aceptáis, … cuando pulsáis Enviar»
  - Controller: «controles de Xbox y PlayStation, teclado o mouse» → «mandos de Xbox y PlayStation, teclado o ratón»

### German (`de`)
- **Name:** Wohnzimmer-Quiz (decision 78; PUB-7 passed, decision 176)
- No «ihr», no «Sie» (de style guide): impersonal or infinitive
- **Short description** (≤ 300):
  > Ein Quiz für die ganze Familie am Fernseher: zwölf Fragen in Folge richtig beantworten und gewinnen. Vier Altersgruppen von Kindern bis Erwachsenen, fünf Joker für knifflige Momente und Fragen mit Bildern, Tönen und Videos. Allein oder in der Gruppe spielen, oder die Spielleitung übernimmt.
- **About This Game:**
  ```
  [h2]Zwölf in Folge zum Sieg[/h2]
  Wohnzimmer-Quiz ist ein klassisches Quiz für den Fernseher. Alle im Raum spielen als ein Team gegen das Spiel: Zwölf Fragen in Folge richtig, und die Krone gehört dem Team. Eine falsche Antwort, und das Spiel ist vorbei. Die Joker wollen also gut eingesetzt sein.

  Jedes Spiel gilt einer Altersgruppe: Kinder, Jugendliche, Junge Erwachsene oder Erwachsene. So bekommen eine Siebenjährige und ein Großvater Fragen, die sie beantworten können. Manche Fragen zeigen ein Bild, spielen einen Ton oder ein kurzes Video.

  [h2]Zwei Spielarten[/h2]
  [list]
  [*][b]Allein oder in der Gruppe:[/b] eine Person oder die ganze Familie als ein Team. Standard-Joker, keine Tricks.
  [*][b]Spielleitermodus:[/b] Die Spielleitung steuert alles: Schwierigkeit, Fragenpakete und Joker, und sie kann jede Frage überspringen, tauschen oder zurücknehmen.
  [/list]

  [h2]Fünf Joker[/h2]
  [list]
  [*][b]Wink:[/b] zeigt einen Hinweis zur Frage, bis zu drei pro Frage.
  [*][b]Näxt & Weg:[/b] tauscht die Frage gegen eine andere Karte; auf Wunsch fliegt das Thema aus dem Spiel.
  [*][b]Glücksfee:[/b] tauscht die Frage gegen eine leichtere zum selben Thema.
  [*][b]Wunschzeit:[/b] ein anderes Thema wählen.
  [*][b]Finte:[/b] auf eine falsche Antwort zielen, und sie wird gestrichen. Ein Treffer auf die richtige: Die Stufe beginnt von vorn.
  [/list]

  [h2]Features[/h2]
  [list]
  [*]Zwölf Fragen in Folge bis zum Gipfel des Turms
  [*]Zwei Modi: Allein oder in der Gruppe, Spielleitermodus
  [*]Fünf Joker: Wink, Näxt & Weg, Glücksfee, Wunschzeit, Finte
  [*]Vier Altersgruppen, von Kindern bis Erwachsenen
  [*]Fragen mit Bildern, Tönen und Videos
  [*]Kostenlose regionale Fragenpakete als DLC, standardmäßig aus
  [*]Gemacht für den Familienfernseher, spielbar auf jedem Bildschirm
  [*]Gamepad, Tastatur oder Maus
  [*]Spielbar ohne Internet
  [*]Speichern braucht Steam: Der Fortschritt gilt pro Steam-Konto und wird über Steam Cloud synchronisiert
  [*]Steam-Erfolge in nicht angepassten Spielen
  [/list]

  [b]Datenschutz:[/b] kein eigenes Konto, keine Werbung. Die Namen der Spielenden bleiben auf dem eigenen Rechner und in der eigenen Steam Cloud. Das Spiel sendet nur mit Erlaubnis: anonyme Spieldaten nach Zustimmung und eine Fragenmeldung beim Klick auf „Senden“.

  [b]Controller:[/b] spielbar mit Xbox- und PlayStation-Gamepads, Tastatur oder Maus.
  ```
- **Language note** (until `pool.de.json` ships; last paragraph of About This Game):
  > Die Oberfläche ist auf Deutsch; die Fragen sind vorerst auf Spanisch. Deutsche Fragen folgen mit einem Update.

## Free DLC
Store texts for each shipped question bundle, one free DLC app each (decision 66: price model, decision 110: regional packs at launch: `colombia` only, es + en, off by default). Entered on the DLC app's own store page (Steamworks → DLC app → Edit Store Page), same fields as the base game. Drafted 2026-10-14 (`task 783`); approved through pm decision "DLC store texts approved? (colombia)".

### Fields and limits
- Same fields and limits as the base game (above, from memory; recheck in the DLC app's admin at entry): name, short description ≤ 300 characters plain text, "About This Content" in BBCode
- Name: the in-game bundle name (decision 50: «Regional: Colombia» everywhere, Steam DLC included); Steam shows the base game on the DLC page itself, so no base-name prefix
- Say: free, needs the base game, optional install, off by default on the bundle step (switched on per game); Steam only (decision 111)
- No question count (decision 110: launch ships what colombia has then; 102 approved es today, pilot target 2000)
- Content facts: `app/data/bundles.json`, `app/data/bundles/colombia/categories.json` (6 categories), `names.en.json`; `BUNDLE_COLOMBIA` Steam achievement (decision 73, `app/desktop/achievements/`) ships with the DLC
- Voice: `es` in the pack's Colombian voice (decision 27, `bundles.json` `voice`), «ustedes» as in-game; glossary terms from the style guides («paquete de preguntas», «question bundle», «logros de Steam»)

### `colombia` (Regional: Colombia)
- Languages: es (pool today), en (`app/data/bundles/colombia/pool.en.json` doesn't exist yet: en text drafted, **enter once the en pack pool ships**; until then the DLC page lists Spanish only)
- es-ES: the `es` text unchanged (the pack speaks Colombian Spanish; no Spain-specific wording needed)

#### Spanish (`es`, also es-ES)
- **Name:** Regional: Colombia
- **Short description** (≤ 300):
  > Paquete de preguntas gratis para Trivia en Familia, para quien tiene relación con Colombia: lugares, comida, fiestas, costumbres, gente, música, deporte y palabras de allá. Se instala aparte y viene apagado: lo encienden en el paso de paquetes de preguntas cuando quieran jugarlo.
- **About This Content:**
  ```
  [h2]Preguntas de Colombia[/h2]
  Regional: Colombia es un paquete de preguntas gratis para Trivia en Familia. Es para quien tiene relación con Colombia: preguntas que en Colombia se saben y que afuera casi nadie sabría.

  [list]
  [*][b]Colombia:[/b] regiones, ciudades, ríos, parques naturales, símbolos patrios y animales
  [*][b]Fiestas, mitos y tradiciones:[/b] el Carnaval de Barranquilla, la Feria de las Flores, mitos y leyendas
  [*][b]Comida colombiana:[/b] platos típicos, dulces, postres, bebidas y frutas
  [*][b]Música y gente de Colombia:[/b] ritmos, cantantes y colombianos famosos
  [*][b]Deporte colombiano:[/b] la Selección, el ciclismo, los medallistas olímpicos y los deportes tradicionales
  [*][b]Así hablamos en Colombia:[/b] palabras y dichos
  [/list]

  [h2]Cómo se juega[/h2]
  [list]
  [*]Gratis; necesita el juego base Trivia en Familia
  [*]Instalación opcional: se puede quitar y volver a poner en Steam
  [*]Apagado por defecto: lo encienden en el paso «Paquetes de preguntas» antes de cada partida; sus preguntas se mezclan con las del paquete básico
  [*]Un logro de Steam propio: 50 respuestas correctas de este paquete
  [*]El paquete crece con las actualizaciones
  [/list]
  ```

#### English (`en`) — enter once `pool.en.json` of the pack ships
- **Name:** Regional: Colombia
- **Short description** (≤ 300):
  > A free question bundle for Living Room Trivia, for anyone with ties to Colombia: its places, food, festivals, customs, people, music, sport and words. Installs separately and starts switched off: turn it on in the question bundle step whenever you want to play it.
- **About This Content:**
  ```
  [h2]Questions from Colombia[/h2]
  Regional: Colombia is a free question bundle for Living Room Trivia. It's for anyone with ties to Colombia: questions people in Colombia know and hardly anyone outside would.

  [list]
  [*][b]Colombia:[/b] regions, cities, rivers, national parks, national symbols and animals
  [*][b]Colombian festivals, myths and traditions:[/b] the Barranquilla Carnival, the Flower Festival, myths and legends
  [*][b]Colombian food:[/b] traditional dishes, sweets, desserts, drinks and fruit
  [*][b]Colombian music and people:[/b] rhythms, singers and famous Colombians
  [*][b]Colombian sport:[/b] the national team, cycling, Olympic medallists and traditional sports
  [*][b]How Colombians talk:[/b] words and sayings
  [/list]

  [h2]How it plays[/h2]
  [list]
  [*]Free; needs the base game Living Room Trivia
  [*]Optional install: remove it and add it back in Steam any time
  [*]Off by default: turn it on in the “Question bundles” step before a game; its questions mix with the base bundle's
  [*]Its own Steam achievement: 50 right answers from this bundle
  [*]The bundle grows with updates
  [/list]
  ```
- Language note while the en pack pool is missing: none; the en text isn't entered before it ships

### After approval
- Capsules: the DLC store name equals the in-game name, so `dlc-colombia/` capsules from `task 669` stay as rendered (no re-run)

## Modding
Store and Workshop texts for modding (milestone 15, plan 121): one feature bullet per store language, a link line to the modding guide, and the Workshop hub description. Drafted 2026-10-14 (`task 990`); approved through pm decision "Store texts: modding bullet and guide link?"; entered at launch (milestone 11), once the Workshop works for players (`plan 122: Modding end-to-end check and close-out`), never on the beta page.

### Rules and fields
- Guide: `https://github.com/rubenmoor/trivia/blob/main/modding/README.md` (decision 134, English only; decision 108: repo public)
- Link rules, from memory (no web access at the task; recheck in Steamworks at entry):
  - About This Game: BBCode `[url=…]…[/url]` is accepted; Steam routes external links through its link filter (`steamcommunity.com/linkfilter/`, "you are leaving Steam" page); no links to other stores or purchase pages
  - Basic Info: one website field plus social links; the game's website field could take the guide URL only if there is no other website
  - If Valve's review rejects the link in About This Game: keep the bullet, drop the link line; the link lives on the Workshop page only
- Workshop hub description: not known whether Steamworks' Workshop configuration has a text field (recheck at entry under Community → Workshop); else the community hub's first announcement (pinned), same text
- Terms per `locales/style/<locale>.md`: «Steam Workshop» (en), «Workshop de Steam» (es), «Steam-Workshop» (de); «mods» as in the Mods screen
- Place: the bullet goes last-but-one in each Features list (before the Steam achievements bullet); the link line is the paragraph after the list, before Privacy

### English (`en`)
- **Feature bullet:** `[*]Make it yours: question bundles, themes and full mods, shared on the Steam Workshop`
- **Link line:** `[b]Modding:[/b] the modding guide (English) explains everything: [url=https://github.com/rubenmoor/trivia/blob/main/modding/README.md]modding guide[/url]`
- **Workshop description:**
  > Mods for Living Room Trivia: question bundles, themes, rule tweaks and full conversions. Subscribe, then turn mods on in the game's Mods screen and restart. Make your own: the modding guide has the format, examples and how to publish here: https://github.com/rubenmoor/trivia/blob/main/modding/README.md

### Spanish – Latin America (`es`)
- **Feature bullet:** `[*]Háganlo suyo: paquetes de preguntas, temas visuales y mods completos, compartidos en el Workshop de Steam`
- **Link line:** `[b]Mods:[/b] la guía de modding (en inglés) lo explica todo: [url=https://github.com/rubenmoor/trivia/blob/main/modding/README.md]guía de modding[/url]`
- **Workshop description:**
  > Mods para Trivia en Familia: paquetes de preguntas, temas visuales, cambios de reglas y conversiones completas. Suscríbanse, enciendan los mods en la pantalla Mods del juego y reinicien. Para hacer los suyos, la guía de modding (en inglés) tiene el formato, ejemplos y cómo publicarlos aquí: https://github.com/rubenmoor/trivia/blob/main/modding/README.md

### Spanish – Spain (`es-ES`)
- **Feature bullet:** `[*]Hacedlo vuestro: paquetes de preguntas, temas visuales y mods completos, compartidos en el Workshop de Steam`
- **Link line:** as `es`
- **Workshop description:** `es` with «Suscríbanse, enciendan … y reinicien. Para hacer los suyos» → «Suscribíos, encended … y reiniciad. Para hacer los vuestros»

### German (`de`)
- **Feature bullet:** `[*]Ganz nach eigenem Geschmack: Fragenpakete, Themes und komplette Mods, geteilt im Steam-Workshop`
- **Link line:** `[b]Mods:[/b] Die Modding-Anleitung (auf Englisch) erklärt alles: [url=https://github.com/rubenmoor/trivia/blob/main/modding/README.md]Modding-Anleitung[/url]`
- **Workshop description:**
  > Mods für Wohnzimmer-Quiz: Fragenpakete, Themes, Regeländerungen und komplette Umbauten. Abonnieren, im Mods-Bildschirm des Spiels einschalten und neu starten. Eigene Mods bauen: Die Modding-Anleitung (auf Englisch) erklärt Format, Beispiele und das Veröffentlichen hier: https://github.com/rubenmoor/trivia/blob/main/modding/README.md

## AI disclosure
Steamworks content survey, section "AI Generated Content", and the text Steam shows from it on the store page. Drafted 2026-10-14 (`task 667`); approved through pm decision "AI disclosure approved?"; entered with the survey by part 9 (PUB-9, `task 259`). Terms of use for the outputs: plan 17 "AI disclosure" (PUB-10).

### Valve's rules
- From memory: the task had no web access; recheck at entry and cite the page with its date here
  - Valve, "AI Content on Steam" (Steam news, 2024-01-09): two kinds, **pre-generated** (made with AI tools during development) and **live-generated** (made by AI while the game runs; needs guardrails and an in-game report tool); the developer describes both, Steam shows the description on the store page
  - Survey update (reported January 2026): efficiency gains from AI-powered dev tools (code assistants) aren't the focus; disclose AI-generated content players see or hear: in the game, on the store page, in marketing
  - Pages to check: partner.steamgames.com/doc/gettingstarted/contentsurvey, the survey form in Steamworks
- Open (decision body): whether the description is localized (one text field or per language); its length limit; whether each DLC app has its own survey
- Trademark (plan 17, PUB-10): no "Claude" or "Anthropic" in public text; "AI language model", "AI coding assistant"

### Facts behind the text
- Questions (question, answers, hints, fun fact) drafted by an LLM, fact-checked by an LLM with web search (D-7, D-10); translations the same way (D-87)
- Approval: 1,134 approved `base` questions on 2026-10-14: 389 reviewed by the developer, 745 by an LLM review only (D-32, D-33; `review.reviewer`); D-56's independent LLM audit runs per batch; blind human spot checks: none recorded yet (no `authoring/data/spot-checks.json`); player reports → `needs_work` (`qgen flag`, plan 103)
- `colombia` (102 approved es): same pipeline
- UI texts and their translations: drafted with the LLM, checked against `locales/style/<locale>.md`
- Code: written with an AI coding assistant; includes what the code draws or plays: the tower, controller glyphs, the capsule and icon template (`task 669`, decision 77), and the short UI effects synthesized in `app/client/src/game/sound.svelte.ts`
- Not AI: pictures, videos, recorded sounds, music (Wikimedia Commons, Freesound via Commons, US government recordings, public domain), fonts (Baloo 2, Nunito, OFL); credited in the game's Credits screen and `CREDITS.md`
- Live-generated: none; no AI runs in the game, nothing is generated while you play

### Survey answers
- Pre-generated: yes; description = the store text below (`en`, or per language if the field is localized)
- Live-generated: no
- Adult-content live generation: no

### Store text: English (`en`)
> The trivia questions (questions, answers, hints, fun facts), the interface texts and their translations were drafted by an AI language model, which also fact-checks the questions against web sources. Every question is reviewed before it ships, by the developer or by a separate AI review; the developer keeps checking AI-reviewed questions and fixes or removes the ones players report. The game's code was written with an AI coding assistant, including the graphics and short sound effects the code draws and synthesizes, and the typographic store art. Pictures, videos, recorded sounds, music and fonts are not AI-generated: they are people's work from Wikimedia Commons and other free sources, credited in the game. Nothing is generated while you play.

### Store text: Spanish – Latin America (`es`)
> Las preguntas (preguntas, respuestas, pistas, datos curiosos), los textos de la interfaz y sus traducciones los redactó un modelo de lenguaje de IA, que además verifica las preguntas con fuentes de la web. Cada pregunta se revisa antes de publicarse, por el desarrollador o por una revisión aparte con IA; el desarrollador sigue revisando las preguntas aprobadas por IA y corrige o quita las que reportan los jugadores. El código del juego se escribió con un asistente de programación con IA, incluidos los gráficos y los efectos de sonido cortos que el código dibuja y sintetiza, y el arte tipográfico de la tienda. Las imágenes, videos, sonidos grabados, la música y las fuentes no son generados con IA: son obra de personas, de Wikimedia Commons y otras fuentes libres, con créditos en el juego. Nada se genera mientras juegan.

### Store text: Spanish – Spain (`es-ES`)
- `es` with «videos» → «vídeos», «mientras juegan» → «mientras jugáis»

### Store text: German (`de`)
> Die Quizfragen (Fragen, Antworten, Hinweise, Wissenswertes), die Texte der Oberfläche und ihre Übersetzungen hat ein KI-Sprachmodell entworfen, das die Fragen auch mit Quellen aus dem Web prüft. Jede Frage wird vor der Veröffentlichung geprüft, vom Entwickler oder von einer separaten KI-Prüfung; der Entwickler kontrolliert die von der KI freigegebenen Fragen weiter und korrigiert oder entfernt die, die Spieler melden. Der Code des Spiels wurde mit einem KI-Programmierassistenten geschrieben, einschließlich der Grafiken und kurzen Soundeffekte, die der Code zeichnet und erzeugt, und der typografischen Shop-Grafiken. Bilder, Videos, aufgenommene Töne, Musik und Schriften sind nicht KI-generiert: Sie sind Werke von Menschen, von Wikimedia Commons und anderen freien Quellen, im Spiel genannt. Während des Spiels wird nichts generiert.

### Free DLC (`colombia`)
- Only if the DLC app has its own survey (recheck at entry); else the base game's disclosure covers it
- es: «Las preguntas de este paquete las redactó y verificó con fuentes de la web un modelo de lenguaje de IA; cada una se revisa antes de publicarse, por el desarrollador o por una revisión aparte con IA. Las imágenes y sonidos son obra de personas, de Wikimedia Commons y otras fuentes libres, con créditos en el juego. Nada se genera mientras juegan.»
- en (once the en pack pool ships): "This bundle's questions were drafted by an AI language model, which also fact-checks them against web sources; each one is reviewed before it ships, by the developer or by a separate AI review. Pictures and sounds are people's work from Wikimedia Commons and other free sources, credited in the game. Nothing is generated while you play."

## Content survey (PUB-9)
Steamworks content survey: general content (generates Steam's own age ratings), mature content (descriptors that drive customers' filters) and generative AI (section above). Drafted 2026-10-14 (`task 1047`) from Valve's public docs and a scan of the shipped pools; approved through pm decision "Content survey answers approved? (PUB-9)"; entered by `task 1049: Content survey and pricing: entry checklist and the 'entered' decision (PUB-9, PUB-11)`. The form itself is only visible in Steamworks: question wording below is by topic, recheck at entry.

### Valve's rules (read 2026-10-14)
- [Content Survey](https://partner.steamgames.com/doc/gettingstarted/contentsurvey):
  - required before store page and build go to review; Valve compares the answers with the build and the store page
  - three sections, all required: 1) General Content ("generate ratings for several regional rating boards", shown on the store page at release; official ratings go under the app's Ratings section), 2) Mature Content (drives "how your game appears relative to each customer's preferences"; disclose all adult content in the builds, even if not accessible), 3) Generative AI (pre-generated / live-generated; "efficiency gains" from AI dev tools not the focus; content that ships and players consume: "artwork, sound, narrative, localization, etc.")
  - after approval some answers can't be edited without Steam Support (summary of the change, how a tester reaches it)
- [Age Ratings Mandatory in Germany](https://partner.steamgames.com/doc/gettingstarted/contentsurvey/germany): since 2024-11-15 games without a rating are hidden in Germany; rating = USK (rare, only a real USK review of the exact Steam version) or Valve's self-rating from the survey + its review team + customer feedback; no survey → no rating; an IARC-generated USK rating from another store must **not** be entered
- [Age Ratings in Indonesia](https://partner.steamgames.com/doc/gettingstarted/contentsurvey/indonesia): same scheme (IGRS 3+/7+/13+/15+/18+/refused), Valve self-rating from the survey
- IARC: no IARC page in the Steamworks docs; Steam's only mention is the Germany/Indonesia rule above; Steam runs its own survey-based ratings instead
- Ratings seen on store data (`store.steampowered.com/api/appdetails`, 2026-10-14): `steam_germany`, `igrs`, `steam_australia`, `dejus` marked `rating_generated`; DLC apps carry their own descriptors and generated ratings (Cyberpunk 2077: Phantom Liberty, 2138330)
- [Onboarding](https://partner.steamgames.com/doc/gettingstarted/onboarding) "What you shouldn't publish": hate speech, nude or sexually explicit images of real people, unlabelled adult content, content "intended to shock or disgust", content you lack rights to
- Descriptors ([ISteamUGC `EUGCContentDescriptorID`](https://partner.steamgames.com/doc/api/ISteamUGC), same list as the store's):
  - 1 Some Nudity or Sexual Content: "some nudity or sexual themes, but not as the primary focus"
  - 2 Frequent Violence or Gore: "extreme violence or gore"
  - 3 Adult Only Sexual Content (18+ gate)
  - 4 Frequent Nudity or Sexual Content (18+ gate)
  - 5 General Mature Content: "mature topics that may not be appropriate for all audiences"
- [Review Process](https://partner.steamgames.com/doc/store/review_process): review 3–5 business days, plan 7; Adult Only content needs build and page reviewed together (not us)
- Comparables, Steam's generated ratings (appdetails, 2026-10-14): Bible Trivia (2578400) no descriptors, Germany 6, IGRS 3; Trivia Tricks (1404090) Germany 12 "Fantasy-Gewalt"; Trivia About You (3196180) descriptor 5 for "limited alcohol use and mild, non-sexual nudity", Germany 12 "Alkohol / Tabak"; Trivia Murder Party 3 descriptor 5, Germany 12

### Scan (2026-10-14, shipped pools)
- Pools: `app/data/pool.json` 1,032 approved (es; no en/de pool yet), `app/data/bundles/colombia/pool.json` 102 (es); keyword lists es only (en/de lists when their pools ship; rerun then)
- Text, base (counts after reading out false hits; ids are examples):
  - war: ~30 mentions, history and myth only, no description of killing: q-0105 (end of WWII, year), q-0108 (storming of the Bastille), q-0650 (Arc de Triomphe, Austerlitz), q-0330 (Trojan horse), q-0141 (Poseidon's trident)
  - death: Egyptian tombs and mummies (q-0235, q-0237, q-0353, q-0391), blood as biology (q-0039, q-0226); no killing, no gore
  - crime: cartoon and fairy-tale (q-0512 Bowser kidnaps Peach, q-0312 Batman, q-0182 Jolly Roger, q-0636 pirates); history (q-0551 Pompey vs pirates); no real crime, no drugs trade
  - alcohol/tobacco: mentions only, nobody drinks or smokes on screen: q-0291 (the drunkard in «El Principito»), q-1123 (Shirley Temple, alcohol-free cocktail), q-1143 (tequila as a wrong answer in a food analogy)
  - religion: ~50 in question, answer or fun fact, all facts (Greek/Roman/Egyptian myth, Christmas customs, Vatican as smallest country, Gutenberg Bible); no preaching, nothing mocked
  - fear: monsters of games/films/legends (q-0076 Creeper, q-0219 Bran castle/Dracula); no horror imagery
  - sex: none (hits are kisses in fairy tales and Disney, q-0688, q-0709; pregnancy as nutrition, q-1200)
  - gambling: none as a mechanic; two mentions (q-0532 Perudo bets dice, q-1153 Dr. Seuss bet)
  - profanity, slurs: none
- Text, `colombia`: Battle of Boyacá (q-0011), forts against pirates (q-0184, q-0580), legends Mohán (q-0170, smokes in the legend), Madremonte (q-0171), Silbón (q-0482, carries a sack of bones), novena carols (q-0256, q-0297); nothing else
- Media: 1,146 Commons files (base 1,044, colombia 102); categories fetched from the Commons API and matched on nudity/violence/alcohol words, hits viewed:
  - nudity, base only (3):
    - q-0135 (largest organ: skin) `File:Human body proportions.JPG`: figure-drawing study, male and female nudes with genitals sketched; illustrative, not needed for the question
    - q-0747 (Hercules) `File:Herakles Farnese MAN Napoli Inv6001 n01.jpg`: Farnese Hercules, full-frontal marble statue; the picture is the question («Mira la foto»)
    - q-0852 (Uffizi → Florence) `File:Sandro Botticelli 046.jpg`: «El nacimiento de Venus», classical nude (covered by hand and hair); named in the question
  - violence: none graphic; q-0108 storming of the Bastille (1789 watercolour, small figures, smoke, no blood), q-0042 Halloween skeletons at a chess board, q-0391 mummy in a museum case, armour/helmets/cannons in museums (q-0179, q-0744, q-0958, q-1086)
  - alcohol/drugs: none
  - colombia: none
  - not covered: images whose Commons categories don't name the content (no full audit, per plan 131)
- Players' text and online:
  - player names: on the device and in the player's Steam Cloud only; never shown to other players
  - no chat, no multiplayer over the network (one screen, one room; online co-op not planned, decision 111)
  - question reports (`plan 103: Report server (POST /reports)`): text goes to the developer only when the player clicks «Enviar»; never shown to others
  - telemetry: opt-in, per install (decision 121), anonymous game data
  - Workshop mods (milestone 15): players' bundles, themes, code; creators set descriptors per item, the base game sets none for them (decision 135 "Steamworks: enable Workshop", pending)
- No in-game purchases (DLC free, decision 66), no ads, no gambling, no loot boxes, no location data

### Proposed answers
- General Content (by topic; map onto the form's wording at entry):
  - violence: none depicted; history and myth questions name wars and battles in text; one historical painting (storming of the Bastille, no blood) → lowest "references/historical, non-graphic" level if the form has one, else no
  - blood/gore: no (blood as biology only)
  - fear/horror: no (legend monsters named in text, cartoon/game monsters)
  - sexual content: no
  - nudity: see borderline B1
  - language: no profanity
  - alcohol, tobacco, drugs: references only in text, no use shown (3 questions) → "references" level if the form has one, else no
  - gambling, simulated gambling: no
  - discrimination: no
  - in-game purchases: no
  - user interaction / online: no chat or player contact; optional Workshop mods (user-generated content, not reviewed by us); question reports on the player's click, to the developer only
  - personal data / location: no location; player names stay local + Steam Cloud; telemetry opt-in
- Mature Content: no descriptor (B1 and B2 below may change it); no Adult Only sexual content
- Generative AI: section "AI disclosure" above (pre-generated yes, live-generated no), as approved in decision 180 "AI disclosure approved?"
- Expected Steam ratings: Germany 6 or 12, IGRS 3 or 7 (Bible Trivia: 6 / 3); not settable by us, read after submission

### Borderline
- B1 nudity (q-0135, q-0747, q-0852):
  - (a) replace the three pictures before the build goes to review, answer "no nudity" (recommended): one illustrative image, one statue, one painting; the game stays filter-free for families; Valve's "nude images of real people" rule doesn't cover art, but the figure study q-0135 is the weakest case
  - (b) keep them, tick descriptor 1 "Some Nudity or Sexual Content" with the note "classical art and an anatomy drawing, non-sexual, 3 of 1,000+ questions": honest, but family customers with nudity filtered may never see the game, and the Germany/IGRS ratings likely rise
  - (c) keep them, descriptor 5 "General Mature Content" with the same note (Trivia About You's choice): the weaker label; Valve may ask for 1 instead
  - later content: once approved, the survey answer is hard to change (Steam Support); future pools must stay free of nudity, or the answer changes
- B2 war history: q-0108's painting and the WWII/battle questions; answer "no violence" (recommended), alternative "historical references, non-graphic" in General Content; no descriptor either way
- Workshop: Steam filters mod items by their own descriptors; the base survey answers only for our content; if the form asks about user-generated content: "yes, optional Workshop mods; creators tag their items"

### DLC (`colombia`)
- DLC apps show their own descriptors and generated ratings on the store (Phantom Liberty), so expect a survey per DLC app; recheck at entry whether Steamworks pre-fills it from the base game
- Answers: as the base, minus nudity (none in the pack), minus Workshop; AI: the DLC line in "Free DLC (`colombia`)" above
- Without its own rating the DLC page may be hidden in Germany like an unrated game (Valve's Germany page names "games"; recheck in the healthcheck list `partner.steamgames.com/healthcheck/missingratingforgermany`)

### IARC
- Recommendation: none. Steam doesn't offer IARC; Germany and Indonesia accept Valve's survey rating; entering an IARC-generated USK rating from another store is forbidden; a real USK review costs money and is "rare" per Valve; Steam only (decision 111), so no other store's IARC either

### AI disclosure: open points of decision 180 rechecked
- Valve's page confirms the scope: content players consume ("artwork, sound, narrative, localization"), not dev-tool efficiency; the draft's code sentence stays an honest extra (graphics and sounds players see and hear)
- Description field localized or English only, its length limit: not on Valve's public pages (2026-10-14); only in the form: recheck at entry; if English only, enter `en`; if limited, shorten at entry and say so in decision 180's consequences
- Own survey per DLC app: likely (above); the `colombia` line is kept
- No change to the AI draft

## Content survey and pricing: entry
The developer's Steamworks steps for PUB-9 and PUB-11, page by page, written 2026-10-14 (`task 1049: Content survey and pricing: entry checklist and the 'entered' decision (PUB-9, PUB-11)`). Field and menu names are from Valve's public docs (tasks 1047, 1048), not the forms themselves: recheck at entry, Valve's UI wins. Result goes into pm decision "Content survey and prices entered in Steamworks? (PUB-9, PUB-11)"; `task 1050: Close-out of PUB-9 and PUB-11` ticks the rows.

### Before entry
- [ ] decision 177 "Steamworks app created? App ID?" answered (App ID)
- [ ] decision 179 "Steamworks app configured (SW-7)? IDs?" answered (`colombia` DLC app ID)
- [ ] decision 180 "AI disclosure approved?" answered (approved variant of "AI disclosure" above)
- [ ] decision 181 "Content survey answers approved? (PUB-9)" answered; if B1 (a): the 3 pictures (q-0135, q-0747, q-0852) replaced in the build that goes to review
- [ ] decision 182 "Price, regional prices and launch discount? (PUB-11)" answered

### Content survey: base app
Steamworks → the app's landing page → Content Survey (recheck the menu path).
- [ ] General Content: answers per "Proposed answers" above, as approved in decision 181 (B2 variant)
- [ ] Mature Content: descriptors per decision 181 (recommended: none; B1 (b)/(c) → descriptor 1 or 5 with the note from "Borderline")
- [ ] Generative AI: pre-generated yes, description = approved store text (`en`; per language if the field is localized); live-generated no; adult live generation no
  - check the field: localized? length limit? → result in the decision; shortened text → decision 180 consequences
- [ ] user content / online, if asked: "Workshop" line from "Borderline"; no chat; reports on click; telemetry opt-in
- [ ] IARC: none (unless decision 181 says otherwise); never enter an IARC-generated USK rating
- [ ] Submit the survey; note the date

### Content survey: `colombia` DLC app
- [ ] DLC app (decision 179) → its own Content Survey, if Steamworks has one (else note "inherits from base")
- [ ] answers per "DLC (`colombia`)" above: as the base, no nudity, no Workshop; AI line from "Free DLC (`colombia`)"
- [ ] Submit; note the date

### Pricing: base package
Steamworks → Store & release → Pricing → Propose Pricing (recheck).
- [ ] base price USD $9.99 (or decision 182's value)
- [ ] accept Valve's suggested prices for all currencies and region groups (no empty currency: unbuyable there); multi-variable method
- [ ] read off into the decision: USD, EUR, GBP, CHF, MXN, COP, CLP, PEN, `USD_LATAM`; a row far from the plausibility ranges in `17-publishing.md` "Regional prices" → recheck the method
- [ ] submit for Valve's price review (1–2 business days); note approved or pending

### Pricing: `colombia` DLC
- [ ] DLC app free ("This is a free product", set at creation, `17-publishing.md` "Free DLC"); no price rows, no discount
- [ ] if the app wasn't created free: fix via the app's settings or Steam Support before review; note it

### Launch discount
- [ ] not now: entered before release on the landing page, per `11-steam.md` "Launch-day checklist" row "Launch discount" (values from PUB-11, decision 182)

### Publish
- [ ] Publish the Steamworks changes (app landing page → "Publish" / "Prepare for publishing"; recheck); survey and prices of base and DLC included

## Capsules and icon
Typographic capsules, library art and the game icon (decision 77: store capsule art, decision 87: Windows exe icon), rendered 2026-10-14 (`task 669`) by a script, no image generation; approved through pm decision "Capsules and icon approved?". Template: the tower of 12 blocks in its materials with the crown, the amber spotlight, faint «?» glyphs, the store name in Baloo 2 (`plans/10-visual-design.md`).

### Valve's asset list
- Checked 2026-10-14: [Graphical Assets overview](https://partner.steamgames.com/doc/store/assets), [Store assets](https://partner.steamgames.com/doc/store/assets/standard), [Library assets](https://partner.steamgames.com/doc/store/assets/libraryassets), [Community and client icons](https://partner.steamgames.com/doc/store/assets/community), [Asset rules](https://partner.steamgames.com/doc/store/assets/rules); sizes unchanged from the 2024 list, old sizes no longer accepted
- Store: header 920×430, small 462×174 (logo nearly fills it; 120×45 and 184×69 generated), main 1232×706, vertical 748×896, page background 1438×810 (optional, ambient, not too bright)
- Library: capsule 600×900, header 920×430, hero 3840×1240 PNG (no text at all; critical content in the centred 860×380 safe area), logo PNG on transparent, 1280 wide and/or 720 tall (logotype only; position picked in Steamworks' preview)
- Icons: shortcut icon 256×256 or 512×512 PNG/ICO (Valve makes the .ico), app icon 184×184 JPG
- Rules: capsules carry artwork, the game name and an official subtitle only; no review scores, awards, sale or call-to-action text, no other text; PG-13; logo readable at every size
- Community icon: no longer in the list (the 2024 "community icon 184×184" is today's app icon)
- DLC: Valve's DLC page names no own asset set; a DLC's store page uses the store capsules (header, small, main, vertical); recheck the DLC app's "Graphical Assets" tab at entry; library assets: none (shown inside the base game's library page)
- Screenshots: see "Screenshots" below

### Rendering
- `node authoring/store/capsules.mjs [--only <path part>] [--visible]` from the dev shell, after `npm run build` (the shell serves the fonts); ~1 min
- Shell under Xvfb with `--disable-gpu` (GPU compositing under Xvfb stalls CDP captures), raw CDP, viewport 3840×2160; each asset is a page swapped into the game's page
- Names (D-50, decision 78): en «Living Room Trivia», es and es-ES «Trivia en Familia» (shared), de «Wohnzimmer-Quiz» (PUB-7 passed, decision 176); logotype = small amber line + big word
- DLC: base logotype + pack name in a panel, a flag-coloured stripe (amber, sapphire, coral) at the bottom; name from `app/data/names.<lang>.json`, else `bundles.json`; replace with the DLC store name once `task 783: Free DLC store texts in 17a` sets one, then re-run
- Re-run after any palette, font or name change

### Output (`authoring/store/out/capsules/`, gitignored)
| file | Steamworks field |
|---|---|
| `<lang>/header.png` | Store: header capsule; Library: header (or reuse) |
| `<lang>/small.png` | Store: small capsule |
| `<lang>/main.png` | Store: main capsule |
| `<lang>/vertical.png` | Store: vertical capsule |
| `<lang>/library-capsule.png` | Library: capsule |
| `<lang>/library-header.png` | Library: header |
| `<lang>/library-logo.png` | Library: logo (suggested position: left bottom corner) |
| `art/library-hero.png` | Library: hero (all languages) |
| `art/page-background.png` | Store: page background (all languages) |
| `dlc-<id>/<lang>/{header,small,main,vertical}.png` | DLC app's store capsules |
| `icon-1024.png` | Game icon source: exe, Linux, Steam client (`task 683`); tracked copy `app/desktop/icon.png`: copy again after a re-render |
| `icon-256.png` | Community/client: shortcut icon |
| `app-icon-184.jpg` | Community/client: app icon |
| `icon-16.png` | Legibility check only, not uploaded |

- `<lang>`: `en`, `es` (also for Spanish – Spain), `de`; upload as localized versions per store language
- AI note for `task 667: AI disclosure text (Steam survey + store wording)`: the template (layout, tower, icon) was designed and coded by Claude; the font, Baloo 2, is people's work (OFL); no image generation; per decision 77 disclosed as AI-assisted store art

## System requirements, languages, controller
Values for Steamworks → Edit Store Page → "Basic Info" (requirements, languages) and "Controller" (plan 88 task 3). Provisional values for the store page entry and coming-soon page, per `decision 90: Store requirements, languages and controller flags?` (applied 2026-10-14, `task 688`); final values measured on the release candidate (milestone 11), with a Steam Deck test. Field names are from memory (no web access at the task); recheck them at entry.

### Measured
- Depots from the local `trivia-desktop-build --dir` (0.1.0, re-measured 2026-10-14 with the media bundle, `plan 132: Media bundle for shipping (SW-9)`, D-104): `windows` 0.41 GB, `linux` 0.36 GB, `content` (media) 0.63 GB, `colombia` DLC 0.05 GB → installed 1.09 GB (Windows), 1.04 GB (Linux), DLC included; before the bundle 2.96 / 2.91 GB
- Shell: Electron 43 (Chromium); no WebGL, no 3D; the heaviest load is HD video questions (WebM VP9 + Opus ≤ 1080p, CRF 33, D-104; hardware decode where the GPU has VP9, else Chromium's software decode)
- Played on: the author's laptop only (NixOS 26.05, i5-12500H, 64 GB, Iris Xe + RTX 4060 Mobile); Linux build smoke-tested under `steam-run` (FHS runtime, task 678). Clean Windows and Ubuntu start tests (18, "Local build start test"): not filled yet

### Requirements (Windows)
| field | minimum | recommended |
|---|---|---|
| OS | Windows 10 64-bit | Windows 11 64-bit |
| Processor | 64-bit dual-core, 2 GHz | quad-core |
| Memory | 4 GB RAM | 8 GB RAM |
| Graphics | DirectX 11 GPU with VP9 video decode (Intel HD 520 or better; else software decode) | any GPU from 2018 on |
| DirectX | Version 11 | Version 11 |
| Network | none | none |
| Storage | 1.5 GB available space | 1.5 GB available space |
| Additional notes | Plays offline; 1280×720 or larger; keyboard, mouse or gamepads; best on a TV | same |

### Requirements (SteamOS + Linux)
| field | minimum | recommended |
|---|---|---|
| OS | SteamOS 3, or Ubuntu 22.04 64-bit or newer | same |
| Processor | 64-bit dual-core, 2 GHz | quad-core |
| Memory | 4 GB RAM | 8 GB RAM |
| Graphics | GPU with OpenGL/Vulkan and VP9 video decode (else software decode) | any GPU from 2018 on |
| Network | none | none |
| Storage | 1.5 GB available space | 1.5 GB available space |
| Additional notes | Native Linux build; plays offline | same |

- Storage: per decision 90 (estimate, grows with content): 1.5 GB = measured 1.09 GB rounded up; the media budget (`app/desktop/media-budget.json`: 950 + 75 MB) plus the OS depot still fits
- Ubuntu 22.04: Electron's own floor, not tested; the non-Nix start test is the Steam beta test (decision 39, `task 263: write plan: Beta test and S5 close-out`): its distro replaces it
- macOS: none (no build)

### Supported languages
| language (Steam) | Interface | Full audio | Subtitles |
|---|---|---|---|
| English | ✓ | ✗ | ✗ |
| Spanish - Latin America | ✓ | ✗ | ✓ |
| Spanish - Spain | ✓ | ✗ | ✓ |
| German | ✓ | ✗ | ✗ |

- No spoken text in the game; "Subtitles" ✓ as the plan sets it (questions and media captions are text)
- English and German: interface only (decision 90); "Subtitles" ✓ once their question pools ship (`pool.en.json`, `pool.de.json`, decision 80)

### Controller
- **Xbox controllers:** Partial controller support (decision 90); Full once the developer's real-pad run passes (start → new player via the letter picker or Steam's floating keyboard → victory, pad only)
  - Covered so far: headless pad-only walk of a whole game, every joker, overlay, flag, wrong and victory (task 352, IN-4); letter picker for new names, faked pad at 1280×800/720 (plan 46, SW-4); floating keyboard under Steam (SW-8, plan 85)
  - Not yet: a real pad (task 352's developer check; decision 72 for Steam Input and the floating keyboard)
- **PlayStation controllers:** supported (Steam Input, or the standard mapping without Steam), PlayStation button glyphs shown: yes (IN-5, `Glyph.svelte`; all pads PlayStation → ✕○□△)
- **Steam Input API:** used for glyph type only (`GetInputTypeForHandle`); input itself through the browser Gamepad API
- **Gamepad recommended:** no (keyboard and mouse play the whole game too)
- Deck compatibility: plan 90, not here

## Screenshots
- Rendered, not hand-made: `node authoring/store/screenshots.mjs [--lang en,es,es-ES,de] [--visible]` from the dev shell (`npm run build` and `trivia-media sync --status approved` first)
- Shell at 1920×1080 under Xvfb, raw CDP, a throw-away demo save per shot (made-up players), offline
- `TRIVIA_DEV_STEAM_USER=1`: valid user under the save gate (plan 87), so the demo save loads; no "progress needs Steam" notice, flag action shown
- Output: `authoring/store/out/screenshots/<lang>/NN-<screen>.png` (gitignored)
- Set and order (decision 79; the developer approves the order with the render, `task 845: Store media: render screenshots and trailers for approval`):
  1. `question-locked`: a question with a locked-in answer (q-0030)
  2. `joker-snipe`: Tiro mágico aiming (q-0019)
  3. `modes`: mode choice, «Solo o en grupo» with the age groups
  4. `bundles`: bundle selector, Regional: Colombia switched on
  5. `customize`: «Personalizar partida»
  6. `configure`: gamemaster mode's configure screen
  7. `joker-presets`: configure screen, preset «Sin límite»
- en/de until their pools (decision 80): only 3–7, numbered 01–05; the question shots skip with a message
- Questions per shot: `Q` in the script (es: approved, short, image cached)
- Re-run after every visual change; the chosen set re-rendered before upload

## Trailer
- Rendered, not edited by hand: `trivia-trailer [--lang es,es-ES,en,de]` from the dev shell (`npm run build` and `trivia-media sync --status approved` first); final videos late, with the screenshots: `task 845: Store media: render screenshots and trailers for approval`
- Shell under Xvfb (X11, 1920×1080), `TRIVIA_DEV_STEAM_USER=1`, `TRIVIA_SOUND=1`, a throw-away demo save (made-up players), offline
- Sound: a private PulseAudio with a null sink (own runtime dir, no session bus), never the desktop's sound server; ffmpeg grabs the display (x11grab) and the sink's monitor
- Scripted game, fixed questions and seed (es: q-0030, q-0019; `Q` in the script):
  1. Start → level 4 question, Soplo's hint
  2. right answer locked, «Respuesta final», reveal
  3. the tower, level 5
  4. next question: Tiro mágico shoots a wrong answer
  5. a wrong answer locked, reveal, «¡Oh no!»: the loss
- Raw take ≈60 s, cut to ≈20 s by `CUT` (marks set during the walk, 80 ms audio fades at each cut); `--keep-raw` keeps the take
- Output: `authoring/store/out/trailer/<lang>.mp4` (gitignored); on a failed walk `<lang>-failed.png`
- Format: 1920×1080, 30 fps, H.264 High yuv420p ~20 Mbit/s, AAC-LC stereo 192 kbit/s 48 kHz, MP4 with faststart
- Valve's rules (Steamworks "Trailers", https://partner.steamgames.com/doc/store/trailer, checked 2026-10-14):
  - up to 1920×1080, 30/29.97 or 60/59.94 fps, high bit rate (5,000+ kbps), .mov/.wmv/.mp4; H.264 + AAC preferred; 16:9 preferred
  - audio: 44 or 48 kHz, filtered down to stereo; wrong resolution or sample rate = most common processing failures
  - a trailer is required for release; the first two valid trailers show before the screenshots; category «Gameplay» for this one
  - viewers may watch without sound (Valve's advice): our cut reads without it (answers, reveal colours, «¡Oh no!»)
  - poster 600×380 and thumbnail 232×130 made by Steam; a custom one must be a 1920×1080 frame of the video
  - microtrailer: Steam cuts six 1 s clips from the first store video, not customizable
  - per-language trailers via Advanced Settings; the base video should be the English one (en waits for its pool, decision 80)
  - no length limit stated; no autoplay/mute rule stated on the page
- en/de: refuse with a message until `pool.en.json` / `pool.de.json` (decision 80); then add their two questions to `Q`
- Re-run after any UI change; the developer approves before upload (`task 845`)

## Entry checklist
- Steamworks → Store page admin, field by field: `task 672: Store page entry checklist and PUB-8 close-out`
