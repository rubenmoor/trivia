# Sound

This file is the owner document for everything the game plays: sound effects, music and the engine that plays them. It starts with an inventory of today's sounds, written as the base for the sound rework (milestone 22), and ends with the brief that the rework follows. Later parts of the rework write their outcomes here. Cue names are mod API and stay; new cues are additive.

Music from free library tracks (search, fetch, split, loop, variants, check, credits): `authoring/tools/music/README.md`.

## Inventory

State on 2026-11-18, before the rework. Sources: `app/client/src/game/sound.svelte.ts` (`Cue`, `SAMPLE_FOR`, `SOUNDTRACKS`), `app/client/public/audio/` (files, `CREDITS.md`), `rg` over `app/client/src` for call sites (file:line, relative to `app/client/src/game/`). Loudness: ffmpeg `ebur128`, integrated LUFS and peak (dBTP) of the shipped `.m4a`; for a cue with variants, the first file. Binding: `decision 81: Recorded sound effects: approve on the TV?` (joker sounds say what the joker does: broom, microwave bing, fairy wand); `decision 733: Reworked game audio: CC0, public domain or CC BY only, no audio generators` for new sounds.

### Effect cues

62 cues (`Cue` members). Every cue has a call site. "Synth only": no recording, a recipe in `RECIPES` plays. A cue with a recording falls back to its recipe when the file does not decode. Variants: `SAMPLE_FOR` rate (pitch) functions and random file lists.

| Cue | Group | Game moment | Meaning | Call sites | File(s) | Length / loudness | Author, licence | Variants |
|---|---|---|---|---|---|---|---|---|
| `silence` | other | Francotirador: the beat of silence before the cork shot | nothing: a deliberate gap (no sound) | Question.svelte:291 | synth only | - | synth | - |
| `rocket` | fireworks | Victory fireworks: a rocket climbs | launch, anticipation | Fireworks.svelte:71 | cohete | 1.45 s, -15.9 LUFS, -4.5 dBTP | ReadeOnly CC0 | rate 0.9 + Math.random() * 0.2 |
| `burst` | fireworks | Fireworks: the rocket bursts | celebration | Fireworks.svelte:77 | estallido | 2.56 s, -15.5 LUFS, -1.0 dBTP | mary905 Public domain | rate 0.85 + Math.random() * 0.3 |
| `confetti-cannon` | fireworks | Fireworks: confetti cannon | party pop | Fireworks.svelte:91 | canon-confeti | 0.35 s, -70.0 LUFS, -1.3 dBTP | Breviceps CC0 | rate 0.85 + Math.random() * 0.3 |
| `sparklers` | fireworks | Fireworks: sparklers | crackling glitter | Fireworks.svelte:141 | bengalas | 2.38 s, -18.2 LUFS, -1.2 dBTP | Alex_hears_things CC0 | - |
| `stars` | fireworks | Fireworks: falling stars | twinkle | Fireworks.svelte:151 | estrellas | 2.30 s, -16.1 LUFS, -4.7 dBTP | LilMati CC0 | rate 0.9 + Math.random() * 0.2 |
| `applause` | reveal | Transition into ¡Correcto! | crowd approval | Game.svelte:459,465 | aplausos | 6.40 s, -16.8 LUFS, -0.5 dBTP | Sandermotions CC0 | - |
| `applause-big` | reveal | Transition into Victory | crowd goes wild | Game.svelte:460,461,475,482 | aplausos-gran | 11.70 s, -16.8 LUFS, 4.9 dBTP | starlite Public domain | - |
| `whoosh` | UI | Screen change (start, language, level, timed…) | moving on | Game.svelte:232,241,245,357,370,372 | whoosh | 0.43 s, -18.0 LUFS, -1.7 dBTP | qubodup CC0 | - |
| `swoosh-up` | jokers | Cambiazo: the card flip | card turns over | Game.svelte:342 | swoosh-sube | 0.53 s, -20.7 LUFS, -1.6 dBTP | SlavicMagic CC0 | - |
| `swoosh` | UI | Transition into a question | question arrives | Game.svelte:371,445 | escoba | 0.28 s, -70.0 LUFS, -3.3 dBTP | semccab CC0 | - |
| `tear` | UI | The chosen card's envelope tears open | opening the question | Game.svelte:443 | rasgado | 0.68 s, -18.4 LUFS, -0.9 dBTP | ludde44 CC0 | - |
| `paper` | UI | Transition to Select / Question after a joker or a pick | page turn | Game.svelte:347,567,580,603,621 | papel | 1.31 s, -15.6 LUFS, -1.1 dBTP | planish Public domain | - |
| `ready` | UI | «¡Hola, …!» and «listo» into level 1 | welcome, ready | Game.svelte:372 (as transition),432 | hola | 0.29 s, -70.0 LUFS, 2.3 dBTP | Kenney CC0 | - |
| `boom` | reveal | Transition into wrong; «Respuesta final» lock; sudden death | impact, bad news | Game.svelte:458,462,476; Question.svelte:197; Level.svelte:60 | synth only | - | synth | - |
| `block` | reveal | The new block lands on the tower (pitch rises with the level) | progress, weight | Game.svelte:356 | golpe | 0.39 s, -70.0 LUFS, -1.1 dBTP | gregoryweir Public domain | rate 0.75 + level * 0.06 |
| `cork-pop` | jokers | Francotirador: the shot | the shot is fired | Question.svelte:293 | corcho | 0.52 s, -16.0 LUFS, 2.3 dBTP | KenRT CC0 | - |
| `pop` | UI | Picking a card | card selected | Game.svelte:440 | pop | 0.10 s, -70.0 LUFS, -1.5 dBTP | unfa CC0 | rate 0.9 + Math.random() * 0.25 |
| `padlock-close` | UI | Locking in an answer; Timed: claim locked | answer is locked | Question.svelte:165,179; Timed.svelte:231 | candado-cierra | 0.66 s, -19.0 LUFS, 4.1 dBTP | SpaceJoe CC0 | - |
| `padlock-open` | UI | Unlocking an answer; the lock opens before «Respuesta final» | answer unlocked | Question.svelte:170,221 | candado-abre | 0.27 s, -70.0 LUFS, -3.0 dBTP | SpaceJoe CC0 | - |
| `fanfare` | reveal | Right answer (one of 5 fanfares at random); Timed right; Career | triumph | Question.svelte:203; Timed.svelte:246; Career.svelte:94 | fanfarria + 4 variants (fanfarria-2, fanfarria-3, fanfarria-4, fanfarria-5) | 4.50 s, -12.1 LUFS, -1.5 dBTP (first of 5) | Concert Band of the United States Air Force Heritage of America Band Public domain (US government work); United States Air Force Band of Mid-America Public domain (US government work); United States Air Force Band of the Rockies Public domain (US government work); United States Coast Guard Band Public domain (US government work); United States Navy Band Public domain (US government work) | random of 5 |
| `sad-trombone` | reveal | Wrong answer; Francotirador hit | failure (comic) | Question.svelte:203,297 | trombon-triste | 4.21 s, -10.6 LUFS, -0.9 dBTP | Joe Lamb CC BY 3.0 | - |
| `rewind` | jokers | «Rebobinar» transition (undo, Francotirador hit) | going back in time | Game.svelte:349 (transition effect) | rebobinar | 0.78 s, -16.9 LUFS, -4.2 dBTP | simplewave CC0 | - |
| `menu-open` | UI | Menu or dialog opens | opening | Game.svelte:530,647,664 | menu-abre | 0.23 s, -70.0 LUFS, -3.0 dBTP | Kenney CC0 | - |
| `menu-close` | UI | Menu or dialog closes | closing | Game.svelte:551,664,911 | menu-cierra | 0.23 s, -70.0 LUFS, -1.3 dBTP | Kenney CC0 | - |
| `unlocked` | UI | First click: audio unlocked | the game is awake | Game.svelte:744 | desbloqueado | 0.28 s, -70.0 LUFS, -1.5 dBTP | Kenney CC0 | - |
| `joker-armed` | jokers | Arming Soplo or Bájale («¿Usar …?») | question asked: confirm? | Question.svelte:260 | comodin-preparado | 0.49 s, -16.3 LUFS, -7.2 dBTP | Kenney CC0 | - |
| `joker-open` | jokers | Opening Paso's or Cambiazo's dialog | options fan out | Question.svelte:254 | comodin-abre | 0.72 s, -22.6 LUFS, -1.6 dBTP | Kenney CC0 | - |
| `joker-activate` | jokers | A joker is played | magic shimmer | Question.svelte:276 | comodin | 1.42 s, -15.5 LUFS, -9.2 dBTP | LaurenPonder CC0 | - |
| `whistle-down` | timed | Timed: wrong answer | falling, failed | Timed.svelte:246 | silbato | 1.17 s, -16.0 LUFS, -9.6 dBTP | v0idation CC0 | - |
| `stamp` | jokers | Paso: the «ELIMINADO» stamp; Career stamp | official mark | Shredder.svelte:19; Career.svelte:81 | sello | 0.70 s, -16.7 LUFS, -0.9 dBTP | Subhashish Panigrahi CC BY 3.0 | - |
| `shredder` | jokers | Paso with purge: the shredder | question destroyed | Shredder.svelte:23 | trituradora | 1.20 s, -19.3 LUFS, -1.9 dBTP | Soundscape_Leuphana CC0 | - |
| `heartbeat` | jokers | Francotirador scope opens; Timed claim wait (every 1.2 s) | tension | Question.svelte:254; Timed.svelte:277,278 | latido | 0.95 s, -17.6 LUFS, -1.5 dBTP | Lunardrive CC0 | - |
| `tick` | UI | Stepper, switch, Esc row, bundle tile, level count | small change of a value | GameSettings.svelte:56; Customize.svelte:23; BundleSelector.svelte:88; Overlay.svelte:68,74,209,214,219; screens/Choice.svelte:109; screens/Level.svelte:66; screens/Question.svelte:328 | mira-tic | 0.02 s, -70.0 LUFS, -6.5 dBTP | Kenney CC0 | rate 0.95 + Math.random() * 0.1 |
| `glass-break` | jokers | Francotirador miss: the answer shatters; a heart cracks (Level) | something breaks | Question.svelte:302; Level.svelte:61 | vidrio | 1.49 s, -27.0 LUFS, 6.2 dBTP | Gravity Sound CC BY 4.0 | - |
| `rustle` | jokers | Soplo: the note slides in; Timed: a new hint | a note / hint arrives | Question.svelte:319; Timed.svelte:194 | susurro-papel | 0.66 s, -24.4 LUFS, -1.3 dBTP | Tomoyo Ichijouji CC0 | - |
| `broom` | jokers | Paso y fuera: the broom sweeps the question away | sweeping away (decision 81) | Question.svelte:311 | barrido | 1.60 s, -19.1 LUFS, -0.8 dBTP | esperri CC0 | - |
| `bing` | jokers | Soplo: the microwave bell; RankBar rank up | «ready» / a hint is served (decision 81) | Question.svelte:318; RankBar.svelte:32,43 | microondas | 0.75 s, -23.3 LUFS, -0.4 dBTP | CAT-FOX_ALEX CC0 | - |
| `wand` | jokers | Hada madrina: the wand | magic that makes it easier (decision 81) | Game.svelte:342 | varita | 1.80 s, -18.1 LUFS, -6.7 dBTP | zazz.sound.design CC0 | - |
| `token-back` | jokers | A fresh joker token pops back | a joker is replenished | Question.svelte:281 | ficha | 0.12 s, -70.0 LUFS, -1.6 dBTP | Kenney CC0 | rate 0.95 + Math.random() * 0.15 |
| `claim` | timed | Timed: a player claims the question | buzzer | Timed.svelte:223 | synth only | - | synth | - |
| `countdown` | timed | Timed: last 3 s of the claim (level 1–3) | time running out | Timed.svelte:286 | synth only | - | synth | - |
| `splash-left` | category splash | Splash: flies left (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | whoosh | 0.43 s, -18.0 LUFS, -1.7 dBTP | qubodup CC0 | - |
| `splash-right` | category splash | Splash: flies right (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | escoba | 0.28 s, -70.0 LUFS, -3.3 dBTP | semccab CC0 | - |
| `splash-fade` | category splash | Splash: fades (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | susurro-papel | 0.66 s, -24.4 LUFS, -1.3 dBTP | Tomoyo Ichijouji CC0 | - |
| `splash-spin` | category splash | Splash: spins (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | swoosh-sube | 0.53 s, -20.7 LUFS, -1.6 dBTP | SlavicMagic CC0 | rate 1.2 |
| `splash-dissolve` | category splash | Splash: dissolves into particles (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | disolver | 0.95 s, -18.0 LUFS, -7.7 dBTP | Kenney CC0 | - |
| `splash-explode` | category splash | Splash: explodes (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | estallido | 2.56 s, -15.5 LUFS, -1.0 dBTP | mary905 Public domain | rate 1.1 |
| `splash-rocket` | category splash | Splash: rocket (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | cohete | 1.45 s, -15.9 LUFS, -4.5 dBTP | ReadeOnly CC0 | - |
| `splash-drop` | category splash | Splash: drops (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | golpe | 0.39 s, -70.0 LUFS, -1.1 dBTP | gregoryweir Public domain | rate 0.8 |
| `splash-wind` | category splash | Splash: blown by wind (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | escoba | 0.28 s, -70.0 LUFS, -3.3 dBTP | semccab CC0 | rate 0.8 |
| `splash-blind` | category splash | Splash: blinds close (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | rebobinar | 0.78 s, -16.9 LUFS, -4.2 dBTP | simplewave CC0 | - |
| `splash-drain` | category splash | Splash: drains away (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | silbato | 1.17 s, -16.0 LUFS, -9.6 dBTP | v0idation CC0 | - |
| `splash-pop` | category splash | Splash: pops (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | pop | 0.10 s, -70.0 LUFS, -1.5 dBTP | unfa CC0 | rate 1.1 |
| `splash-zoom` | category splash | Splash: zooms (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | whoosh | 0.43 s, -18.0 LUFS, -1.7 dBTP | qubodup CC0 | rate 1.3 |
| `splash-shatter` | category splash | Splash: shatters (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | vidrio | 1.49 s, -27.0 LUFS, 6.2 dBTP | Gravity Sound CC BY 4.0 | - |
| `splash-melt` | category splash | Splash: melts (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | derretir | 0.50 s, -24.5 LUFS, -2.0 dBTP | Kenney CC0 | - |
| `splash-blackhole` | category splash | Splash: black hole (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | agujero-negro | 0.85 s, -17.9 LUFS, -2.9 dBTP | Kenney CC0 | - |
| `splash-birds` | category splash | Splash: letters scatter like birds (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | pajaros | 0.52 s, -18.0 LUFS, -6.8 dBTP | Kenney CC0 | - |
| `splash-typewriter` | category splash | Splash: typewriter backspace (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | maquina-escribir | 0.57 s, -22.5 LUFS, -1.9 dBTP | Kenney CC0 | - |
| `splash-plane` | category splash | Splash: paper plane (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | papel | 1.31 s, -15.6 LUFS, -1.1 dBTP | planish Public domain | - |
| `splash-jelly` | category splash | Splash: jelly wobble (category title leaving, question.svelte) | the title exits in that style | question/Splash.svelte:100 via question/splash.ts | gelatina | 0.42 s, -18.5 LUFS, -3.0 dBTP | Kenney CC0 | - |

Notes:
- `splash-*` cues reuse files of other cues (whoosh, escoba, vidrio, …) or have their own (`disolver`, `derretir`, `agujero-negro`, `pajaros`, `gelatina`, `maquina-escribir`); the 20 splash styles are in `question/splash.ts`.
- Every file in the folder is referenced by `EFFECT_NAMES` or a soundtrack; every recording is the file of at least one cue.
- `-70.0 LUFS`: the clip is under 0.4 s, too short for an integrated reading; use the peak.
- Cues played by the engine with no `sfx()` call in `app/client/src`: none besides `/?efectos` (`EffectsDemo.svelte:20`, plays any cue).

### Music tracks

| Track | Plays | Meaning | Call sites |
|---|---|---|---|
| `normal` | Start, language, bundles, mode, join, level, select screens | calm background; the TV is waiting | Game.svelte MUSIC map:66-75, 184, 266 |
| `question` | Question screen (before an answer is locked) | thinking; slightly more tension | Question.svelte:149,155,208,230; MUSIC map |
| `submitted` | An answer is locked in | tension rises: decision made | Question.svelte:149,155,208 |
| `roll` | «Respuesta final» until the reveal | drum roll, crescendo (6 s build), then steady | Question.svelte:196 |
| `victory` | Victory screen, once | Elgar finale; the big moment | Game.svelte MUSIC map (victory) |
| `timed` | Competitive (timed) question after its media | faster than `question` (the soundtrack's `question` file plays; synth has its own variant) | Timed.svelte:360 |

- `normal`, `question`, `submitted`, `timed` are loops from the chosen soundtrack (`timed` plays the soundtrack's `question` file; only the generated set has a faster own variant). `roll` and `victory` are shared by every soundtrack:
- `redoble`: 14.00 s, -17.9 LUFS, -4.6 dBTP
- `victoria`: 98.00 s, -13.3 LUFS, -0.8 dBTP
- `victory` plays `victoria` (Elgar, US Marine Band, public domain) at gain 3; `roll` plays `redoble` looped with a 6 s crescendo (US Air Force Band, public domain).
- Switching on the Question screen is a sharp cut (fades 0.08 s, 0.15 s from `roll`); other changes fade 0.6 s. Question media silences the music.

### Soundtracks (`SOUNDTRACKS`, `soundtracks.ts`)

The old recorded sets (`variaciones`, `caja`, `sin-prisa`, `reflejos`) and their files are gone (decision 733, the brief). The brief's three sets are entries (`lofi-tranquilo` default, `acustica-calida`, `jazz-de-concurso`; `chill-lofi`, `warm-acoustic`, `jazz-quiz-show` in the brief), not installed yet: the generated loops (A minor i–VI–III–V pad, 76/96/120/132 bpm) play until `plan 224: New soundtracks` adds files. `sintetizada` left the picker.

- Music file numbers: none yet; the new sets get their rows from part 4.
- Default and picker: per the brief (`chill-lofi`), set by task 2243.

## Engine

Pure data and lookups in `app/client/src/game/soundtracks.ts` (testable without audio); playback in `sound.svelte.ts`.

- `SOUNDTRACKS[id]`: `tracks` (variants it has: `normal`, `question`, `submitted`, `timed`), `loopStart`/`loopEnd`, `level`; loop points come from `authoring/data/music/<set>-<piece>.json`
- File per variant: `musica-<set>-<track>.m4a`, derived (`soundtrackFile`), no name table; `roll` and `victory` are shared files (`redoble`, `victoria`), not per set
- Recorded sets: every variant equal length (decision 734), so `question` ↔ `submitted` keeps the beat (`sameBeat`: set has files)
- `timed`: its own file per set, no `question` stand-in
- Fallback: set without that file, or undecodable → generated loop of the same track; a set with no files ("not installed") is valid
- Unknown stored id (old ids too) or unknown `music(track, { soundtrack })` override → default, no throw (`resolveSoundtrack`)
- `/?efectos`: per set a button per variant (marked `generated` when no file) and the cut `question ↔ submitted` where the set keeps the beat
- Test: `app/client/src/game/sound.test.ts`

### Totals

- 50 `.m4a` files in `app/client/public/audio/` (effects and shared tracks; music loops removed), plus `CREDITS.md`.
- Before the music removal: 5.55 MB; the music loops were 3.1 MB of it. Budget: `app/desktop/media-budget.json` key `audio` is 7 (MB).
- Largest: `victoria` 1.20 MB (98 s), then `redoble` 0.20 MB.
- Cue count 62, not ~66 as the plan guessed; 4 are synth only: `silence`, `boom`, `claim`, `countdown`.

## Effects

The new sound effects (plan 223) are made with `trivia-sfx` from CC0, public domain or CC BY recordings, one listening round per group. Workers can't hear: the tool prints numbers (length, size, loudness, true peak), the developer's ears decide.

- Tool: `trivia-sfx` (`authoring/tools/sfx/sfx.py`, dev shell; tests `test_sfx.py` in `npm test`); `-h` lists the commands
  - `record <name> --file P --page U --title T --author A --licence SPDX --cue C [--cue …] [--class effect|jingle|long] [--start S] [--end S] [--gain DB] [--stereo]`, then `--read-on-page` once the licence is read on the source page
  - `convert <name>`: cut, trim silence, 50 ms fade-out, loudnorm -16 LUFS / -1.5 dBTP (two passes), mono AAC 80k → `app/client/public/audio/<name>.m4a`; `--stereo` in the record keeps two channels
  - `check [<name> …]`: -16 ±1 LUFS (clips over 0.3 s), true peak ≤ -1.5 dBTP, size budget of the class, licence allowed and read
  - `credits [--check]`: effect rows of `CREDITS.md` between `trivia-sfx` marker comments; hand rows and music rows untouched
- Licences and credits code are `music.py`'s (decision 199); allowed: CC0, PD, CC BY 3.0/4.0 (`decision 733: Reworked game audio: CC0, public domain or CC BY only, no audio generators`); no Freesound API (`decision 82: Freesound API for a paid Steam release (OQ-45): replace, ask, or family only?`)
- Record: `authoring/data/sfx/<name>.json` (committed): `name` (file name without `.m4a`, lower case ASCII Spanish words with `-`), source `page`, `title`, `author`, `library`, `sha256`, `downloaded`, `licence` (`spdx`, `read_on_page` date), `cues`, `class`, `stereo`, `cut` (`start`, `end`, `gain_db`), `credit`
- Work files (gitignored): downloads by hand into `work/sfx/<group>/`; the tool copies the original to `work/sfx/originals/<name>.<ext>`
- Budget per file: effect 40 kB, jingle 80 kB, long 100 kB (applause-big, timed countdown); the folder stays within `audio` in `app/desktop/media-budget.json`
- Cue names are mod API and stay; file names may change; variants of frequent cues are a file list in `SAMPLE_FOR` (never the same twice in a row); synth `RECIPES` stay as the fallback
- Groups: `GROUP` in `sound.svelte.ts` maps every cue to a group of the inventory (UI, reveal, jokers, fireworks, splash, timed, other); `/?efectos` lists the cues by group, one block per round
- A group round: the worker installs its pick per cue (by measurement and fit to the brief's theme), stages 1–2 alternates per cue on `/sounds` (manifest group `effects-<group>`, round N); the developer listens on `/?efectos` and in a real game (`TRIVIA_SOUND=1`) and approves or asks for changes per cue; changes start the next round

## Manifest

`work/sound-brief/manifest.json` (gitignored, in the main checkout; work trees symlink `work/`) lists the audition candidates that `/sounds` on `trivia-authoring` plays (`GET /api/sounds`, files at `/sounds/<file>`; `authoring/server/sounds.py`). Without a manifest the page shows «no candidates yet».

- A JSON list of entries; per entry:
  - `file`: relative to `work/sound-brief/`, e.g. `effects/<direction>/<name>.m4a`, `music/<mood>/<name>.m4a`
  - `group`: `effects` or `music`
  - `direction` (effects) or `mood` (music)
  - `round`: feedback round, integer from 1
  - `stands_for`: the cue or track it stands in for
  - `source`: page URL; `author`; `licence` (as read on the page)
  - numbers: `length_s`, `lufs`, `true_peak_db`, `centroid_hz`; `bpm` (music)
  - music, optional: `title`, `full_length_s` (whole track), `excerpt_start_s`, `tension_note` (what could make the tension variants); `/sounds` shows them under the name

## Candidates

Audition candidates per round, staged by `authoring/tools/sound_brief.py <spec.json>` into `work/sound-brief/` (gitignored; packs and the spec stay in `work/sound-brief-src/`) and listed on `/sounds`. The numbers in the manifest: `lufs` is measured with 1 s of silence after the file (the loudness gate works on 400 ms blocks), so very short sounds read low; every file is peak-limited to about -1.5 dBTP, so a click can sit far under -16 LUFS. Workers can't hear: files were picked from the source's names and measured; the developer's ears decide.

### Round 1, effects

Four directions, each from one designer. Kenney's own download page refuses scripts (403), so the packs come from their OpenGameArt mirrors (same CC0 packs); licence read on each page: CC0. No cartoon direction: the OpenGameArt CC0 search found no coherent cartoon pack (only single sounds); a later round can look wider. "Coverage" counts the 62 `Cue` members (inventory above) the source could play with a fitting sound, estimated from the pack contents; no direction has applause, a cork pop or the microwave bing except where noted.

| Direction | Source | Licence | Files staged | Coverage |
|---|---|---|---|---|
| `wooden-tactile` | Kenney, [RPG Audio](https://opengameart.org/content/50-rpg-sound-effects) (51 files: book, cloth, leather, door, coins, metal, knife, creak, chop, footsteps) | CC0 | 10 | ~25: menu, paper, tear, pop, padlock, stamp, tick, swoosh, token-back, broom (cloth sweep), shredder; no jingles, fireworks, applause, boom, bing, wand |
| `casino-table` | Kenney, [Casino Audio](https://opengameart.org/content/54-casino-sound-effects-cards-dice-chips) (55 files: cards, dice, chips) | CC0 | 10 | ~14: menu, pop, paper, swoosh, tick, padlock, token-back, stamp; no jingles, fireworks, jokers with meaning |
| `retro-8bit` | Juhani Junkala (SubspaceAudio), [512 retro sound effects](https://opengameart.org/content/512-sound-effects-8-bit-style) | CC0 | 10 | ~55: UI, fanfares, power-ups (joker shimmer, wand), errors, explosions (burst), portals (whoosh, splash), bleeps (claim, countdown), bling (bing); no applause, no real broom or cork |
| `clean-digital` | Kenney, [UI Audio](https://opengameart.org/content/51-ui-sound-effects-buttons-switches-and-clicks) (clicks, switches, rollovers) and [Digital Audio](https://opengameart.org/content/63-digital-sound-effects-lasers-phasers-space-etc) (tones, power-ups, phasers, zaps) | CC0 | 12 | ~40: UI, tones (fanfare, sting), phasers (wand, whoosh), zaps (splash); no applause, fireworks, broom |

Applause (`applause`, `applause-big`) and the crowd sounds are in none of the four: any theme keeps today's files or needs another source.

### Round 1, music

Four moods around decision 83's reference ("chill and relaxing, with a clear rise in tension on submit"), three tracks each, all Kevin MacLeod ([incompetech](https://incompetech.com/music/royalty-free/music.html)), instrumental, fixed-tempo studio productions with drums + bass + tune, all uploaded 2015 or later. Licence read on the site: CC BY 4.0 (`llms.txt` and the track page markup: `creativecommons.org/licenses/by/4.0/`); credit title, author, link, licence, "adapted". Other sources (Kenney, OpenGameArt, Free Music Archive, Scott Buckley) not used in round 1: Kenney's music is jingles only, and incompetech's catalogue (`pieces.json`: bpm, feel, instruments) has the longest steady, band-style tracks. Workers can't hear: picked from catalogue feel, instruments and bpm; each excerpt is the steadiest 60 s (lowest loudness variation, after the first 10 s) of the track, staged at -18 LUFS where the peak limit (-1.5 dBTP) allows, else quieter (`lufs` in the manifest). Tension variants (part 4): Demucs layer split (decision 732), one mixdown per variant (decision 734); the `tension_note` per track says which layers.

| Mood | Tracks (bpm, full length) | Note |
|---|---|---|
| `chill-lofi` | Late Night Radio (72, 4:24), Smooth Lovin (75, 4:19), Universal (80, 4:30) | slow, relaxed, electric piano/synth; closest to decision 83 |
| `warm-acoustic` | Fretless (100, 5:36), Bossa Antigua (70, 4:43), Shaving Mirror (78, 3:26) | guitar/ukulele/bossa; Fretless has countermelodies that come and go |
| `jazz-quiz-show` | Backbay Lounge (120, 4:27), Lobby Time (128, 3:13), Jazz Brunch (100, 5:23) | piano/vibes/organ trio feel, brighter, game-show friendly |
| `soft-electronic` | Eternity (100, 3:18), ZigZag (80, 3:45), Andreas Theme (90, 3:37) | synth/EP; ZigZag is a little aggressive already, Eternity very even (little dynamics) |

## Brief

The developer's picks after listening on `/sounds` (`decision 735: Sound brief, round 1: effect theme, soundtracks and their moods, tension variants, default, old sounds to keep`, answered 2026-11-18, final after round 1). Parts 3–5 follow it; the developer wants to try the new sounds in a real game next.

| Question | Round | Choice |
|---|---|---|
| Effect theme | 1 | one theme for every group: `clean-digital` (Kenney UI Audio + Digital Audio, CC0); applause and crowd sounds: today's files |
| Soundtrack count, moods | 1 | 3: `chill-lofi` (Late Night Radio), `warm-acoustic` (Bossa Antigua), `jazz-quiz-show` (Backbay Lounge); all Kevin MacLeod, CC BY 4.0 |
| Tension variants | 1 | per set `normal`, `question`, `submitted`, `timed`; `roll` and `victory` shared by all sets |
| `sintetizada`, default | 1 | `sintetizada` leaves the picker; default `chill-lofi` (replaces `decision 361: Soundtracks: take the sets found, or look further?`'s default) |
| Old sounds kept | 1 | Elgar victory (`victoria`), drum roll (`redoble`), applause; fanfares and all other old effects replaced |
| Another round | 1 | no: final |

- Lapse with the brief (applied by part 6): `decision 360: Joker sounds on the TV: approve Paso y fuera, Soplo and Hada madrina?`, `task 146: Developer check of the three new joker sounds on the TV`, `task 1865: Developer check of the fanfare variants on the TV`, `task 150: Close UI-10 in the plans`
- Joker meanings (`decision 81: Recorded sound effects: approve on the TV?`: broom, microwave bing, fairy wand) stay; `clean-digital` has no broom: part 5's joker round finds a fitting sound within the theme or a CC0/PD/CC BY broom
