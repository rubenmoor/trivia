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
  [*][b]Paso:[/b] cambia la pregunta por otra carta; si quieren, ese tema sale del juego.
  [*][b]Bájale:[/b] cambia la pregunta por una más fácil del mismo tema.
  [*][b]Cambiazo:[/b] ustedes eligen otro tema.
  [*][b]Francotirador:[/b] disparen a una respuesta falsa y queda tachada. Si le dan a la correcta, el nivel vuelve a empezar.
  [/list]

  [h2]Características[/h2]
  [list]
  [*]12 preguntas seguidas hasta la cima de la torre
  [*]Dos modos: Solo o en grupo, Modo anfitrión
  [*]Cinco comodines: Soplo, Paso, Bájale, Cambiazo, Francotirador
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
  - Paso: «si quieren» → «si queréis»; Cambiazo: «ustedes eligen otro tema» → «elegís otro tema»; Francotirador: «disparen … Si le dan a la correcta» → «disparad … Si le dais a la correcta»
  - «Preguntas con imagen, sonido y video» → «… vídeo»; «Control, teclado o mouse» → «Mando, teclado o ratón»; «Hecho para el televisor de la casa» → «Hecho para la tele de casa»
  - Privacy: «en su computador y en su Steam Cloud» → «en vuestro ordenador y en vuestro Steam Cloud»; «si ustedes lo permiten: … si aceptan, … cuando presionan Enviar» → «si lo permitís: … si aceptáis, … cuando pulsáis Enviar»
  - Controller: «controles de Xbox y PlayStation, teclado o mouse» → «mandos de Xbox y PlayStation, teclado o ratón»

### German (`de`)
- **Name:** Wohnzimmer-Quiz (provisional: decision 78 picked it; stands only once PUB-7's name and trademark check passes, `task 253: write plan: Partner account, name check and AI terms`)
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
  [*][b]Zaunpfahl:[/b] zeigt einen Hinweis zur Frage, bis zu drei pro Frage.
  [*][b]Näxt:[/b] tauscht die Frage gegen eine andere Karte; auf Wunsch fliegt das Thema aus dem Spiel.
  [*][b]Gang runter:[/b] tauscht die Frage gegen eine leichtere zum selben Thema.
  [*][b]Wunschzeit:[/b] ein anderes Thema wählen.
  [*][b]Finte:[/b] auf eine falsche Antwort zielen, und sie wird gestrichen. Ein Treffer auf die richtige: Die Stufe beginnt von vorn.
  [/list]

  [h2]Features[/h2]
  [list]
  [*]Zwölf Fragen in Folge bis zum Gipfel des Turms
  [*]Zwei Modi: Allein oder in der Gruppe, Spielleitermodus
  [*]Fünf Joker: Zaunpfahl, Näxt, Gang runter, Wunschzeit, Finte
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
- Store texts per shipped pack (decision 110: `colombia`, es + en): `task 783: Free DLC store texts in 17a`

## AI disclosure
- Steam content-survey AI section and store wording per language: `task 667: AI disclosure text (Steam survey + store wording)`

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
- Names (D-50, decision 78): en «Living Room Trivia», es and es-ES «Trivia en Familia» (shared), de «Wohnzimmer-Quiz» (provisional until PUB-7's check); logotype = small amber line + big word
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
| `icon-1024.png` | Game icon source: exe, Linux, Steam client (`task 683`) |
| `icon-256.png` | Community/client: shortcut icon |
| `app-icon-184.jpg` | Community/client: app icon |
| `icon-16.png` | Legibility check only, not uploaded |

- `<lang>`: `en`, `es` (also for Spanish – Spain), `de`; upload as localized versions per store language
- AI note for `task 667: AI disclosure text (Steam survey + store wording)`: the template (layout, tower, icon) was designed and coded by Claude; the font, Baloo 2, is people's work (OFL); no image generation; per decision 77 disclosed as AI-assisted store art

## System requirements, languages, controller
Values for Steamworks → Edit Store Page → "Basic Info" (requirements, languages) and "Controller" (plan 88 task 3). Provisional values for the store page entry and coming-soon page, per `decision 90: Store requirements, languages and controller flags?` (applied 2026-10-14, `task 688`); final values measured on the release candidate (milestone 11), with a Steam Deck test. Field names are from memory (no web access at the task); recheck them at entry.

### Measured
- Depots from the local `trivia-desktop-build --dir` (0.1.0, rechecked 2026-10-14; part 6's media bundle not built yet, `task 260: write plan: Media bundle for shipping (SW-9)`): `windows` 0.41 GB, `linux` 0.36 GB, `content` (media) 2.55 GB → installed 2.96 GB (Windows), 2.91 GB (Linux)
- Shell: Electron 43 (Chromium); no WebGL, no 3D; the heaviest load is HD video questions (hardware decode)
- Played on: the author's laptop only (NixOS 26.05, i5-12500H, 64 GB, Iris Xe + RTX 4060 Mobile); Linux build smoke-tested under `steam-run` (FHS runtime, task 678). Clean Windows and Ubuntu start tests (18, "Local build start test"): not filled yet

### Requirements (Windows)
| field | minimum | recommended |
|---|---|---|
| OS | Windows 10 64-bit | Windows 11 64-bit |
| Processor | 64-bit dual-core, 2 GHz | quad-core |
| Memory | 4 GB RAM | 8 GB RAM |
| Graphics | DirectX 11 GPU with H.264 video decode (Intel HD 520 or better) | any GPU from 2018 on |
| DirectX | Version 11 | Version 11 |
| Network | none | none |
| Storage | 3 GB available space | 3 GB available space |
| Additional notes | Plays offline; 1280×720 or larger; keyboard, mouse or gamepads; best on a TV | same |

### Requirements (SteamOS + Linux)
| field | minimum | recommended |
|---|---|---|
| OS | SteamOS 3, or Ubuntu 22.04 64-bit or newer | same |
| Processor | 64-bit dual-core, 2 GHz | quad-core |
| Memory | 4 GB RAM | 8 GB RAM |
| Graphics | GPU with OpenGL/Vulkan and H.264 video decode | any GPU from 2018 on |
| Network | none | none |
| Storage | 3 GB available space | 3 GB available space |
| Additional notes | Native Linux build; plays offline | same |

- Storage: estimate per decision 90 (3 GB now, grows with content); the installed size rounded up once part 6's bundle (SW-9) exists
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
- Output: `authoring/store/out/screenshots/<lang>/NN-<screen>.png` (gitignored)
- Screens: start, player, modes, customize, tower (level 11); with a question pool of the language also cards, image question, video question, Francotirador aiming, victory
- Questions per shot: `Q` in the script
- Re-run after every visual change; the chosen set re-rendered before upload

## Trailer
- `trivia-trailer`, 20 s per store language, rendered late: `task 844: Store trailer command trivia-trailer`, `task 845: Store media: render screenshots and trailers for approval`

## Entry checklist
- Steamworks → Store page admin, field by field: `task 672: Store page entry checklist and PUB-8 close-out`
