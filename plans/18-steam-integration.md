# 18 — Steam Integration and Packaging

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). Turns the built client into an installable desktop game with Steam features, and gets builds onto Steam. Depends on the client engine ([12](12-client-engine.md)): once the game runs without Python, the shell only has to show the client and save one file.

## Desktop shell (OQ-29)
Decided: **Electron** (D-63, pm decision 12; facts checked 2026-10-11, sources there). Steam binding: **steamworks-ffi-node** (pm decision 28, picked in SW-2; added in SW-8).

| Option | For | Against |
|---|---|---|
| **Electron** (chosen) | The most common way to ship a web game on Steam. The same Chromium on Windows, Linux and the Deck, so fonts, audio, `backdrop-filter` and animations behave as on the TV today. Overlay works on Windows. A LAN server for phone buzzers (OQ-37) is plain Node `http` in the main process, in TS. | ~125–160 MB download (v44 zip: 158 MB Win, 123 MB Linux). Steam binding: steamworks.js is stale (last release 2024-08; open overlay issues, incl. no overlay on Linux); steamworks-ffi-node is active but young. Overlay on native Linux/Deck is shaky; fallback: Windows build via Proton. |
| Tauri v2 | Small installs, Rust core. | WebView2 on Windows, WebKitGTK on Linux/Deck: two engines to test; WebKitGTK has open `backdrop-filter` and media bugs; no Steam overlay over a system webview (Windows-only community workaround). Phone buzzer server in Rust. |
| Browser + local server (PyInstaller) | Closest to today; already has a LAN server for phone buzzers. | Not a "real" game window, no overlay, two runtimes, antivirus false positives on PyInstaller builds; plans 19/20 remove Python. |

The shell's own code stays tiny: create a fullscreen window, load `app/client/dist/`, expose `loadSave`/`writeSave` and the Steam calls to the page through a preload bridge, `window.triviaShell` (decision 130: `window.trivia` is the mod API); no Node in the page itself.
- Window option `webPreferences.autoplayPolicy: "no-user-gesture-required"`: a gamepad press isn't user activation in Chromium (HTML spec: only key, mouse, touch), so a pad-only start would stay silent (plan 45, IN-4).
- Credits: the shell adds its own entry (Electron, MIT, plus the Chromium licence file Electron ships) to the generator `app/client/credits.ts` (PUB-5, plan 47).

## Steam features
- **Steam Cloud:** the save (12) is one JSON file per valid Steam user (decision 111), `<userData>/save/<steamid64>/game.json` (`%APPDATA%\trivia`, `~/.config/trivia`; D-72, plan 87). Steam Auto-Cloud syncs it with no code: subdirectory `trivia/save/{64BitSteamID}`, non-recursive, pattern `game.json` (the `.tmp`, `backup/`, `dev/` and other users' folders stay local).
  - No valid user: no save file, no folder; the page plays memory-only (`MemoryStore`), one dismissable notice «Sin Steam no se guarda el progreso» per start, flag action hidden; `--import-save` refuses (exit 1).
  - Dev switch (`TRIVIA_DEV_STEAM_USER=1`) without a SteamID: `TRIVIA_SAVE_DIR` if set, else `save/dev/game.json` (decision 114).
  - No `local/` folder, no migration of S3's `save/game.json`: old files left alone, never read; the family's save comes in via `--import-save` (plan 99).
  - Auto-Cloud values for SW-7 (plan 87; entered in Steamworks → Steam Cloud by the developer):
    - Quota: 1 file, 20 MB (envelope ≤ 10 MB, D-72).
    - Root path: root `WinAppDataRoaming`, subdirectory `trivia/save/{64BitSteamID}`, pattern `game.json`, OS all, recursive off.
    - Root override: original `WinAppDataRoaming`, OS Linux, new root `LinuxXdgConfigHome` (`~/.config`), path unchanged; if Steamworks doesn't list it: `LinuxHome` with `.config/` prepended. Check Valve's current list on entry.
    - Deck: Linux build → the override; Windows build via Proton (D-92) → Windows path inside the prefix, no override.
  - Expected cloud listing: only `game.json`. If Steam picks up `game.json.tmp` mid-write: rename the temp outside the pattern (small `save.mjs` change), no Cloud API.
  - Conflict (both machines changed offline): Steam's own dialog at launch; the picked side wins whole; no code.
  - Family Sharing borrower: own SteamID → own folder and cloud slot.
  - Dev: `steam_appid.txt` / `TRIVIA_STEAM_APPID` as SW-8 left it (480 until SW-7).
- **Overlay:** Windows only (D-92): `addElectronSteamOverlay` on win32 while Steam is up; Linux without overlay (the native GL window froze the game on XWayland); the Deck runs the Windows build via Proton (SW-12). No pause on overlay open.
- **Achievements** (plan 86): the list of decision 73: Achievement list (SW-11)?, table below; only in qualifying games (no gamemaster mode, decision 74; not customized, standard 12 levels and 4 cards, no «Ir a pregunta…»), unlocked only for a valid Steam user (decision 111) with a live bridge. Derived from the save (`earned()` in `engine/achievements.ts`), never stored; unlocked after the save loads and when a game ends (`lib/achievements.ts`), so earlier games in an imported save unlock on the next start. Steam's toast only, no own UI, no stats.
- **On-screen keyboard:** `ShowFloatingGamepadTextInput` for the player name in Big Picture / on the Deck (14, Deck Verified): A on the name field opens it at the field; elsewhere and without Steam the letter picker (plan 46).
- **Glyphs:** Steam Input's `GetInputTypeForHandle` picks PlayStation or Xbox glyphs under Steam (14); without Steam `Gamepad.id`.
- **Language:** a fresh save preselects Steam's language (`GetCurrentGameLanguage`: the game's language in Steam, else the client's) through `guessTag()` in `lib/engine.ts` (`latam` → es, `spanish` → es-ES, `english` → en, `german` → de; unknown → `navigator.language`); the first-start screen still asks (I18N-2, D-86); one language for UI and questions (D-96).
- **Rich presence:** «Nivel 7 de 12» while a level is on screen (`#Level`, values `level`, `levels`), cleared otherwise and on quit; Steam shows only uploaded tokens: `app/desktop/steam-presence.vdf` (latam, spanish, english, german; from `screen.level.kicker` + `screen.level.of`), uploaded by the developer in Steamworks.
- **Remote Play Together:** enabled in Steamworks once multi-controller input works (IN-6).
- **Valid Steam user** (decision 111): `steam.available` and a non-zero SteamID, computed once in `main.mjs` after init → `--trivia-user` → `steam.user`; the page reads only `validUser` (`lib/desktop.ts`; also true under the dev server shim, plan 99). Dev switch `TRIVIA_DEV_STEAM_USER=1`: valid without Steam (`steamId()` stays null), packaged too (soft check); never set by builds, launch options or VDFs. Gates saves (plan 87) and flags (plan 93).
- **Dev mode** (plan 85): the dev switch without a real Steam user → `--trivia-dev` → `steam.dev`; `devMode` (`lib/desktop.ts`, also the dev server shim). Esc menu row «Ir a pregunta…» (`GoToDialog.svelte`, engine `goTo`, action `goto`): id or bare number replaces the question on screen at the current level, any mode, ignores range/group/bundles/seen; old one `admin_replace`; unknown → `question_unknown`.
- **Mute** (plan 123): muted when `PM_WORKER` is set or `TRIVIA_MUTE=1`; `TRIVIA_SOUND=1` overrides both (`app/desktop/mute.mjs` `muteReason`). Shell: `webContents.setAudioMuted(true)`, one stderr line `trivia: muted (PM_WORKER)`; session only, `trivia.volumes` and the Esc-menu volume UI unchanged. Dev server (`vite`, `vite preview`): same rule, `trivia dev: muted (PM_WORKER)`, shim flag `triviaShell.muted` → session mute in `sound.svelte.ts` (master gain 0, `mediaVolume()` 0, nothing stored); `?mute` does the same in any build. Smoke game runs with `TRIVIA_MUTE=1` (checks load, not audio).
- **No DRM:** the game runs without Steam running (offline living room). Steam binding calls are optional; the game works without them.

## Achievements in Steamworks
Values for Steamworks → Stats & Achievements → Achievements (plan 86, SW-11; list per decision 73: Achievement list (SW-11)?), entered by the developer once the real App ID exists (SW-7). Texts are drafts; the developer checks them all in the SW-11 close-out (task 658).
- Every achievement: Hidden no, Set by Client, no progress stat, achieved/unachieved icon `app/desktop/achievements/png/<API>_achieved.png` / `<API>_unachieved.png` (256×256, `render.sh`).
- Order: enter them in the table's order (= `ACHIEVEMENTS` in `engine/achievements.ts`); the edit form takes the English name and description.
- Localization: upload `app/desktop/steam-achievements.vdf` (latam, spanish, english, german). Its tokens `NEW_ACHIEVEMENT_1_<n>_NAME/_DESC` assume Steamworks' ids for that order on a fresh app; compare with Steamworks' localization download first and rename tokens if they differ.
- Then publish (Steamworks → Publish).
- Mods: achievements stay allowed with mods on (decision 123: Achievements in games with mods on: allowed or off?; decision 146: Achievements, mods screen and rich presence with mods on); no mods gate in `earned()` or the unlock gate, no save field; player questions count like ours except `BUNDLE_*` (our regional bundles only) and `ALL_CATEGORIES` (our `base` only).
- Wording: infinitive, no address, so latam/spanish and German need no plural form; joker names from the catalogs (es Soplo/Paso/Bájale/Cambiazo/Francotirador, en Hint/Pass & Purge/Fairy/Ms Picky/Trick Shot, de Zaunpfahl/Näxt/Gang runter/Wunschzeit/Finte).
- `SUPER_PICKY` in English isn't «Super Picky»: Ms Picky is a different joker.

### Now (25)
Name / description per language.

| API name | latam | spanish | english | german |
|---|---|---|---|---|
| `FIRST_WIN` | «¡A la cima!» / «Ganar una partida: 12 preguntas, hasta arriba de la torre.» | = latam | «To the Top!» / «Win a game: 12 questions, all the way up the tower.» | «Auf dem Gipfel!» / «Ein Spiel gewinnen: 12 Fragen, ganz nach oben.» |
| `WINS_10` | «Diez cimas» / «Ganar 10 partidas.» | = latam | «Ten Summits» / «Win 10 games.» | «Zehn Gipfel» / «10 Spiele gewinnen.» |
| `WINS_50` | «Alpinista» / «Ganar 50 partidas.» | = latam | «Mountaineer» / «Win 50 games.» | «Höhenluft» / «50 Spiele gewinnen.» |
| `WIN_ADULTS` | «Ligas mayores» / «Ganar una partida en el grupo de edad Adultos.» | «Primera división» / «Ganar una partida en el grupo de edad Adultos.» | «Big League» / «Win a game in the Adults age group.» | «Oberliga» / «Ein Spiel in der Altersgruppe Erwachsene gewinnen.» |
| `WIN_ALL_AGES` | «Para todas las edades» / «Ganar una partida en cada grupo de edad.» | = latam | «For All Ages» / «Win a game in every age group.» | «Für jedes Alter» / «In jeder Altersgruppe ein Spiel gewinnen.» |
| `FIRST_SOPLO` | «Una ayudita» / «Usar el Soplo por primera vez.» | = latam | «A Little Help» / «Play the Hint joker for the first time.» | «Mit dem Zaunpfahl» / «Zum ersten Mal den Zaunpfahl spielen.» |
| `FIRST_PASO` | «¡Paso!» / «Usar el Paso por primera vez.» | = latam | «Pass!» / «Play Pass & Purge for the first time.» | «Näxt!» / «Zum ersten Mal Näxt spielen.» |
| `FIRST_BAJALE` | «Más suavecito» / «Usar Bájale por primera vez.» | «Más suave» / «Usar Bájale por primera vez.» | «Fairy Dust» / «Play the Fairy for the first time.» | «Einen Gang runter» / «Zum ersten Mal „Gang runter“ spielen.» |
| `FIRST_CAMBIAZO` | «Otro tema, por favor» / «Usar el Cambiazo por primera vez.» | = latam | «Another Topic, Please» / «Play Ms Picky for the first time.» | «Lieber was anderes» / «Zum ersten Mal die Wunschzeit spielen.» |
| `FIRST_FRANCOTIRADOR` | «En la mira» / «Usar el Francotirador por primera vez.» | = latam | «Take Aim» / «Play the Trick Shot for the first time.» | «Im Visier» / «Zum ersten Mal die Finte spielen.» |
| `ALL_HINTS` | «Soplo completo» / «Ver todas las pistas de una pregunta con el Soplo.» | = latam | «Every Last Hint» / «See every hint of one question with the Hint joker.» | «Mit allen Zaunpfählen» / «Alle Hinweise einer Frage mit dem Zaunpfahl aufdecken.» |
| `PURGE` | «Pasar no era suficiente» / «Usar el Paso y sacar todo el tema del juego.» | = latam | «Passing Just Wasn't Enough» / «Play Pass & Purge and send the whole topic out of the game.» | «Passen reichte nicht» / «Mit Näxt das ganze Thema aus dem Spiel werfen.» |
| `SUPER_PICKY` | «Súper exigente» / «Usar el Paso y Bájale en la misma pregunta.» | = latam | «Not That One Either» / «Play Pass & Purge and the Fairy on the same question.» | «Superwählerisch» / «Näxt und „Gang runter“ bei derselben Frage spielen.» |
| `WIN_NO_JOKERS` | «Sin comodines» / «Ganar una partida sin usar ni un solo comodín.» | = latam | «No Jokers Needed» / «Win a game without playing a single joker.» | «Ganz ohne Joker» / «Ein Spiel gewinnen, ohne einen einzigen Joker zu spielen.» |
| `ALL_JOKERS_WIN` | «Baraja completa» / «Ganar una partida usando los cinco comodines.» | = latam | «Full Deck» / «Win a game playing all five jokers.» | «Volles Blatt» / «Ein Spiel gewinnen und dabei alle fünf Joker spielen.» |
| `SNIPER_TOP` | «Fuego amigo» / «Darle a la respuesta correcta con el Francotirador en el último nivel.» | = latam | «Friendly Fire» / «Hit the right answer with the Trick Shot on the last level.» | «Eigentor» / «Auf der letzten Stufe mit der Finte die richtige Antwort treffen.» |
| `SOPLO_SAVE` | «Salvado por el Soplo» / «Ganar la última pregunta después de un Soplo.» | = latam | «Saved by the Hint» / «Win the last question right after a Hint.» | «Der Wink zum Sieg» / «Die letzte Frage nach einem Zaunpfahl gewinnen.» |
| `ALL_CATEGORIES` | «De todo un poco» / «Acertar al menos una pregunta de cada tema.» | = latam | «Jack of All Topics» / «Answer at least one question right in every topic.» | «Von allem etwas» / «In jedem Thema mindestens eine Frage richtig beantworten.» |
| `SPECIALIST` | «Especialista» / «Acertar 50 preguntas de un mismo tema.» | = latam | «Specialist» / «Answer 50 questions right in one topic.» | «Fachgebiet» / «50 Fragen aus einem Thema richtig beantworten.» |
| `QUESTIONS_1000` | «Mil preguntas» / «Ver 1000 preguntas distintas.» | = latam | «A Thousand Questions» / «See 1000 different questions.» | «Tausend Fragen» / «1000 verschiedene Fragen sehen.» |
| `POLYGLOT` | «Políglota» / «Ganar partidas con preguntas en dos idiomas.» | = latam | «Polyglot» / «Win games with questions in two languages.» | «Sprachtalent» / «Spiele mit Fragen in zwei Sprachen gewinnen.» |
| `GAME_NIGHTS` | «Noche de juegos» / «Jugar en 7 días distintos.» | = latam | «Game Night» / «Play on 7 different days.» | «Spieleabend» / «An 7 verschiedenen Tagen spielen.» |
| `CHRISTMAS` | «Trivia navideña» / «Jugar una partida el 24 o el 25 de diciembre.» | = latam | «Christmas Quiz» / «Play a game on 24 or 25 December.» | «Weihnachtsquiz» / «Am 24. oder 25. Dezember ein Spiel spielen.» |
| `NIGHT_OWL` | «Búho nocturno» / «Ganar una partida después de medianoche.» | = latam | «Night Owl» / «Win a game after midnight.» | «Nachteule» / «Nach Mitternacht ein Spiel gewinnen.» |
| `FIRST_FLAG` | «Ojo crítico» / «Marcar una pregunta.» | = latam | «Sharp Eye» / «Flag a question.» | «Adlerauge» / «Eine Frage melden.» |

### Later
Not entered now: Steam shows every defined achievement, unreachable ones look broken (`inSteamworks()`). Each one goes into the VDF when it's entered.

| API name | with | latam | spanish | english | german |
|---|---|---|---|---|---|
| `WIN_RR_COOP` | MD-8 | «Todos a una» / «Ganar una partida Por turnos en equipo.» | = latam | «All for One» / «Win a round-robin co-op game.» | «Alle für einen» / «Ein Spiel reihum im Team gewinnen.» |
| `WIN_RR_COMPETITIVE` | MD-8 | «El último en pie» / «Ganar una partida Por turnos, todos contra todos.» | = latam | «Last One Standing» / «Win a round-robin game, everyone against everyone.» | «Wer zuletzt lacht» / «Ein Spiel reihum, jeder gegen jeden, gewinnen.» |
| `WIN_TIMED` | MD-8 | «Contra el reloj» / «Ganar una partida Contrarreloj.» | = latam | «Beat the Clock» / «Win a timed game.» | «Gegen die Uhr» / «Ein Spiel auf Zeit gewinnen.» |
| `BUNDLE_COLOMBIA` | colombia DLC | «¡Qué chévere!» / «Acertar 50 preguntas del paquete Regional: Colombia.» | = latam | «Colombia, Mi Amor» / «Answer 50 questions right from the Regional: Colombia bundle.» | «Kolumbien-Kenner» / «50 Fragen aus dem Fragenpaket Regional: Kolumbien richtig beantworten.» |

## Platforms and display
- **Windows** (x64) and **Linux** (x64) native builds; the **Deck** runs the Linux build. macOS later (needs a $99/year developer account and notarization).
- **Resolutions:** 720p to 4K. The size unit `--u` scales with the width (D-29), so a 16:10 screen (Deck, 1280×800) has more height. Check every screen at 1280×800 and at 1280×720 (smallest). Valve's Deck legibility guideline is text ≥ 9 px at 1280×800.
- **Windows specifics:** set explicit MIME types if any local serving remains; use atomic save writes with a retry (antivirus locks).
- **Media size (SW-9, D-104):** the raw cache (2549 MB, 1100 files) ships re-encoded by `stage-media.mjs`, keys unchanged (D-17), names `shippedName(url)` (cache stem + shipped extension; resolver tries `cacheName`, then `shippedName`).
  - images: WebP lossy, fit inside 3840×2160, never upscaled (D-48), q 82 → down to q 60 while > 1 MB; GIF, SVG as is
  - audio: Opus in Ogg, 96 kb/s; video: WebM VP9 CRF 33 + Opus 96k, ≤ 1920×1080
  - measured 2026-10-14: 2549 → 679 MB (1079 WebP, 17 Opus, 3 WebM, 1 GIF); `content` 630 MB, `colombia` DLC 50 MB; 58 files > 1 MB: 3 videos (60.7, 27.4, 10.0 MB; Apollo ships its whole 29 min), 55 WebP 1.0–2.3 MB
  - budgets `app/desktop/media-budget.json` (MB): `content` 950, `dlc.colombia` 75, `default_dlc` 75, `file` 5, `video` 100

## Builds and depots
Local builds since S3 (SW-5, D-73); the release check (SW-6) and Steam uploads (SW-10) since S5. No GitHub Actions: CI is local (pm decision 14). One command on the developer's Linux machine builds both platforms; the artefacts are plain folders, so Steam (S5) can install them as they are.
- **Command:** `trivia-desktop-build` (dev shell) = `qgen validate`, `npm run build -w app/client`, `stage-media.mjs` (encodes the pool's media into `build/media/`, cache `work/ship-media/` `<stem>-<settings hash>.<ext>`, only new or changed files, hard links; `ffmpeg-headless`, `libwebp` in the wrapper), `steam-libs.mjs`, `electron-builder --x64 --linux tar.gz --win zip`; `--dir` adds the `dir` target (`release/{win,linux}-unpacked/`, the OS depots; launcher via `after-pack.mjs` too), `trivia-steam stage` checks OS depot (without `resources/media`) + content depot (`build/media/`) = the archives. Outside Nix: `npm ci --prefix app/desktop`, then `npm run dist --prefix app/desktop` (no `qgen validate`). First build downloads the Electron zips into `~/.cache/electron`; later builds run offline.
- **Targets:** `app/desktop/release/Trivia-<version>-win-x64.zip` (files at the zip root; `Trivia.exe`: unsigned, game icon) and `Trivia-<version>-linux-x64.tar.gz` (folder `Trivia-<version>-linux-x64/`; `./trivia` = launcher with `--no-sandbox`, binary `trivia-bin`; the Deck runs this one). No installer, no AppImage. 0.82 GB (tar.gz), 0.84 GB (zip) since SW-9 (were ~2.5 GB).
- **Layout:** `resources/app.asar` (`package.json`, `main.mjs`, `resolve.mjs`, `save.mjs`, `preload.cjs`), `resources/client/` (client `dist/`: the readable tree, decision 124, plain files outside the asar; "Modding: module paths"), `resources/data/` (`app/data/`), `resources/media/` (only the pool's media and backgrounds, encoded from the cache via `app/desktop/build/media/` under `shippedName`; outside the asar for the S5 content depot); `LICENSE.electron.txt`, `LICENSES.chromium.html` at the root. `CREDITS.md` (PUB-5) in `resources/client/` and at the root (`extraFiles` from `../client/dist/CREDITS.md`).
- **Stale client files (task 946):** checked 2026-10-13, Electron 43: `app://` (`protocol.handle`) responses never enter Chromium's HTTP cache and V8's code cache follows changed bytes: a changed module runs on the next start, with or without the header; `resolve.mjs` still sends `cache-control: no-cache` for client and mod-overlay files (unhashed names, decision 124); no `ses.clearCache()` needed.
- **Config:** `app/desktop/electron-builder.yml`, `after-pack.mjs` (Linux launcher), own `package-lock.json` (`electron`, `electron-builder`; not a root workspace).
- **Steam binding (plan 85, task 650):** `asarUnpack` steamworks-ffi-node, koffi, `@koromix/*`; per-platform `files` drop the other OS's native binaries; SDK lib per OS via `extraResources` → `resources/steamworks_sdk/redistributable_bin/{linux64,win64}/` (`main.mjs` `setSdkPath`); `steam-libs.mjs`: fails without the SDK libs, fetches `@koromix/koffi-win32-x64` (koffi's version, `npm pack`) for the zip built on Linux; no `steam_appid.txt` in `release/`.
- **Exe metadata (B-11, task 683):** `win.signExecutable: false`: electron-builder 26 edits `Trivia.exe`'s resources in pure JS (`resedit`, no wine): `ProductName` = `productName`, `FileDescription` = `extraMetadata.description` («Trivia»), `CompanyName` + copyright = `package.json` `author`, `FileVersion`/`ProductVersion` = `version`. Icon (decision 87): `app/desktop/icon.png` (tracked copy of `capsules.mjs`'s `icon-1024.png`) as `win.icon` (exe, 16–256 px) and `linux.icon` (only used by desktop-file targets; the tar.gz/Steam build has none, the Steam client icons are uploaded by hand, 17a). Re-rendered icon: copy it over `app/desktop/icon.png`. `ProductName` follows `productName` («Trivia»); «Living Room Trivia» once PUB-7 passes (artifact names and paths change with it).
- **Signing:** not required by Steam; the exe stays unsigned (SmartScreen only warns for downloads outside Steam).
- **Checked (task 330, 2026-10-12):** unpacked Linux build, no network (`unshare -rn`), no Nix env (`env -i` + an FHS runtime), no Python: new player → level 5 with image, audio (playing) and video (playing) questions, no missing-media notice; «Salir del juego» → restart: player resumes, no answered question comes back; save at `~/.config/trivia/save/game.json`; nothing written outside `HOME`. Windows: zip content listed only.
- **Upload:** `trivia-steam upload --branch beta` (dev shell, `authoring/steam/steam.py`, D-93): gates (clean tree; tag `v<version>` on HEAD, never created by the command; `steam.json` IDs) → `trivia-release-check` (or `--checked`: this commit's passing `release-check.json` on a clean tree) → `trivia-steam stage` → VDFs → `steamcmd +login $TRIVIA_STEAM_ACCOUNT +run_app_build <app vdf> +quit`; prints the BuildID. `--preview` (Valve's `Preview 1`, no tag needed), `--dry-run` (no SteamCMD, no tag, placeholder IDs 480/481… (one per depot, packs included) while `steam.json` is null). Desc `<tag> <sha>` plus `skipped: <steps>`.
- **Version (pm decisions 91, 92; plan 91):** one source, `app/desktop/package.json` `version` (semver); `flake.nix` app version, client (`__APP_VERSION__`, Vite `define`), artifact names, exe `FileVersion` and `steam.py` `version()` read it. Tag `v<version>` per release; build Desc `<tag> <sha>`.
  - Bump: edit `package.json` `version`, commit, `git tag v<version>`.
  - Id continuity: `qgen validate` fails when an id of the newest `v*` tag's `app/data/pool*.json` is missing from `authoring/data/questions.json` (drop = status change, never deletion; no tag → "skipped").
  - Semver: patch `x.y.Z` = content-only or bug fix; minor = new feature or save version bump; `1.0.0` = launch.
  - Pool: `qgen export` writes `"hash"` (first 8 hex of sha256 over the exported questions) into every `pool*.json`; Credits header shows «Versión 0.1.0 · preguntas fa9887b5» (`lib/build.ts` `buildInfo()`; hash of the current game's question locale).
- **Depots (pm decision 84):** `windows` (`release/win-unpacked/` without `resources/media`), `linux` (`release/linux-unpacked/` likewise), `content` (`build/media/` → `resources/media`, shared); one install folder.
- **DLC depots (pm decision 66, D-95):** one per pack (`colombia`, store name «Regional: Colombia», en "Regional: Colombia", de «Regional: Kolumbien», pm decision 110, decision 50), IDs in `steam.json` `dlc: {<id>: {appid, depot}}`, built with the base app's VDF; content root `build/dlc/<id>/` (staged by `trivia-steam stage`: `resources/data/bundles/<id>/` + `build/pack-media.json`'s media); OS depots exclude the pack's data, `content` its media. Not installed = pack not offered (D-94), no Steam call. Stage check: packs in the build = `pack-media.json` = `steam.json` `dlc`; all depots together = each archive. Smoke game: once as built (packs offered), once without the packs' files (none offered, game plays).
- **Credentials:** a dedicated Steam build account, by hand from the author's machine (pm decision 14); account via `TRIVIA_STEAM_ACCOUNT` or a prompt, password and Steam Guard typed into SteamCMD only, cached in its home `~/.local/share/trivia/steamcmd`. Never commit credentials (AGENTS.md).
- **Branches:** `SetLive` is always `beta` (password-protected, set in Steamworks; the family plays it first); `--branch default` or any other is refused. `default` (public) stays empty until S6 and is only set in the Steamworks web UI.
- **Gitignored:** `work/steam/<tag>/` (`release-check.{md,json}`, `logs/`, `vdf/`, `steamcmd.log`, SteamCMD's `output/`); in git only `authoring/steam/` (`steam.json` IDs, templates, scripts; no secrets).
- **CI (SW-6, pm decision 14):** local, no GitHub Actions.
  - Per commit: `npm run check`, `npm test`, `npm run build`, `qgen validate`, the task's own check (AGENTS.md).
  - Before every Steam upload: `trivia-release-check` (dev shell, `authoring/steam/release_check.py`, ~15 min); steps `tag` (first: clean tree, HEAD tagged `v<version>`, pm decision 91; never tags), `checks` (per-commit checks), `licenses` (`trivia-media licenses --status approved`), `quality` (`qgen report --qc` release bar ✓ for the last two batches, pm decision 15), `nix` (`nix build .#app`), `desktop` (`trivia-desktop-build --dir`, stage-media's missing-file check, `trivia-steam stage`), `report` (the build's `reportUrl` non-empty, `GET <url>/health` → `{"ok": true, "api": 1}` within 10 s, plan 104; `--skip report` until plan 103 task 4's setup), `credits` (`credits_check.mjs` on `linux-unpacked` and `win-unpacked`: packaged files ↔ `credits.json` both ways, plan 92), `smoke` (`smoke.mjs` on `linux-unpacked` under `TRIVIA_DEV_STEAM_USER=1`, network off: save in `save/dev/game.json` (decision 114), restart resumes, no «progress needs Steam» notice; again without the packs' files; no start test without Steam and without the switch, decision 39), `media-budget` (`stage-media.mjs --check`: every pool URL's file in `build/media/`, per-depot totals (`content`, each pack per `build/pack-media.json`) and file/video limits against `media-budget.json`, files > 1 MB listed), `manual` (rows `offline`, `report`, `windows`, `deck`, `cloud`, `sound`, `red-frame`, `beta-save`, `signoff`; `deck` best effort per decision 125: `no Deck (decision 125)` passes until the developer has a Deck, then plan 90's real-Deck checklist; full-only ones auto-skipped on a content-only patch; y/n/note or `--manual <file>`; steps: `11-steam.md` "Release checklist (ST-4)").
  - Every ✗ fails (exit 1); `--skip <step>` for a known-broken step, listed in the report and the build Desc. `trivia-steam upload --preview`/`--dry-run` add `--skip tag`.
  - Kind (plan 92): previous tag = newest `v*` reachable from HEAD, not HEAD's own; `content-only` patch if `git diff --name-only <prev>..HEAD` touches nothing shipped (`app/`, `flake.nix`, `flake.lock`, root `package*.json`) outside `app/data/`, else (or no earlier tag) `full`. Save version: `SAVE_VERSION` (`app/client/src/engine/state.ts`) at HEAD vs previous tag. JSON keys `kind`, `previous_tag`, `save_version`.
  - Report `work/steam/<tag-or-sha>/release-check.{md,json}` (header: version, pool hash, previous tag, kind, save version change; commit, clean tree, result, skips) + `logs/<step>.log`; the JSON is what `trivia-steam upload --checked` reuses.

## Steamworks app configuration (SW-7)
The values the developer enters in Steamworks for the base app and the free DLC app, one checklist (plan 130, SW-7). Workers never log in or enter values; the developer ticks the rows and reports the IDs through the decision "Steamworks app configured (SW-7)? IDs?". Steam only (decision 111): no values for running outside Steam, no DRM, no `restartAppIfNecessary`, no anti-tamper.
- Needs the App ID from decision 177: Steamworks app created? App ID?
- Valve's page and field names are from memory: recheck at entry.
- Not here: store fields (`plans/17a-store-page.md`, task 672: Store page entry checklist and PUB-8 close-out; DLC texts decision 173: DLC store texts approved? (colombia)), achievements (decision 140), Workshop (decision 135: Steamworks: enable Workshop …), Deck review (plan 90: Steam Deck review and Deck test (SW-12)), price (PUB-11).

### App (Basic info)
- [ ] App ID: decision 177's; type Game.
- [ ] Names (D-50): default/english «Living Room Trivia»; latam + spanish «Trivia en Familia»; german «Wohnzimmer-Quiz» (decision 78: German store name (PUB-8, D-50): keep «Living Room Trivia» or a localized one?). If PUB-7 fails (decision 176: Store names pass PUB-7?), this row waits for the new OQ-34 decision. In-game `productName` «Trivia» unchanged ("Exe metadata" above).

### Installation → General
- [ ] Install folder: `LivingRoomTrivia` (Cloud paths don't depend on it).
- [ ] Launch option Windows, 64-bit: executable `Trivia.exe`, no arguments.
- [ ] Launch option Linux + SteamOS, 64-bit: executable `trivia` (the `after-pack.mjs` launcher, adds `--no-sandbox`; binary `trivia-bin`), no arguments, no Proton forcing.
- [ ] Linux runtime: Steam Linux Runtime (current "sniper"/3.0 if offered; recheck); the beta test (task 263: write plan: Beta test and S5 close-out) confirms it starts.
- [ ] No other launch options: never `TRIVIA_DEV_STEAM_USER`, `--no-mods` or other dev args; no second "safe start" option (decision 152: Manual safe start: --no-mods only).
- [ ] Redistributables: none (Electron ships its runtime).

### Installation → Depots
Split per decision 84: SteamCMD source and depot split for Steam uploads; build side and `steam.json`: "Builds and depots" above (plan 89).
- [ ] `windows`: OS Windows, 64-bit, language all.
- [ ] `linux`: OS Linux, 64-bit, language all.
- [ ] `content`: OS all, language all.
- [ ] `colombia`: OS all, language all, tied to the colombia DLC app (next block).
- [ ] IDs → `authoring/steam/steam.json` (task 1045 / task 681), via the decision.

### DLC (All Associated Packages, DLC, Demos And Tools → Add New DLC)
Free DLC per shipped pack (decision 66: Price model (OQ-33); decision 110: Regional packs at launch (RG-5, OQ-46)); only packs in `app/data/bundles/` at upload time.
- [ ] `colombia`: name «Regional: Colombia» (es, es-ES, en); de «Regional: Kolumbien» only once a de pack pool ships.
- [ ] Price free; optional (installed when owned and ticked in Properties → DLC).
- [ ] Depot `colombia` linked to it; the base app lists it.
- [ ] Store texts: `plans/17a-store-page.md` "Free DLC" (decision 173).

### SteamPipe → Builds (branches)
- [ ] `default`: empty until S6 (decision 84).
- [ ] `beta`: password-protected; password with the developer only, never in a file or a decision.

### Steam Cloud
- [ ] Auto-Cloud values from "Steam features" → "Auto-Cloud values for SW-7" above (plan 87): quota, root path, Linux root override.
- [ ] Conflicts: Steam's dialog, nothing to set.

### Application → Steam Input
- [ ] Default configuration for every controller type: Valve's **Gamepad** template ("Gamepad" / "Generic Gamepad"); the Deck's controls arrive as a virtual Xbox pad (decision 125: Steam Deck: best effort, review without a Deck at hand).
- [ ] No opt-outs of PlayStation/Xbox/Switch configuration support (glyphs read `GetInputTypeForHandle`, plan 85).
- [ ] No custom action set (the game reads the browser Gamepad API).
- [ ] Deck: nothing else here (fit plan 46, peek plan 113, review plan 90).

### Community → Rich Presence
- [ ] Upload `app/desktop/steam-presence.vdf` (or via Steamworks' localization upload; recheck); a friend's list shows «Nivel N de 12» (decision 71: Upload the rich presence tokens in Steamworks?).

### Achievements
- [ ] "Achievements in Steamworks" above, reported through decision 140: Achievements entered and published in Steamworks?.

### Publish
- [ ] Publish the Steamworks changes after each block.

### Dev (repo side, task 1045)
- [ ] `app/desktop/main.mjs` `STEAM_APP_ID` 480 → the real App ID; `TRIVIA_STEAM_APPID` / `SteamAppId` overrides stay; `--dry-run` keeps 480.
- [ ] No `steam_appid.txt` in the repo or in builds (`steam.py` `EXCLUDE`); a dev run that needs one writes it gitignored.

## Local build start test
The developer's check that the local builds start and play offline on machines without the dev setup (SW-5; pm plan 56 task 3). Skipped, not failed: decision 39 (Steam only, decision 111); the clean-machine start test is covered by the Steam beta test (task 263). Tables kept as the checklist for that test.
- **Artefacts:** `trivia-desktop-build` → `app/desktop/release/Trivia-<version>-win-x64.zip`, `Trivia-<version>-linux-x64.tar.gz`; or copy those two files over (USB stick, ~0.85 GB each).
- **Machines:** Windows x64 without Node/Python; Linux x64 without Nix (e.g. Ubuntu 24.04).
- **Result:** «skipped, decision 39 (Steam only, decision 111); covered by the Steam beta test (task 263)», every row; no rows to fill.

### Windows x64
Date: 2026-10-13 · Build commit: 06c39dc

| check | result | note |
|---|---|---|
| Network off before unpacking | skipped (decision 39) | |
| Unpack the zip, start `Trivia.exe` (SmartScreen «More info → Run anyway» expected: unsigned) | skipped (decision 39) | |
| No console window | skipped (decision 39) | |
| Starts fullscreen; F11 toggles | skipped (decision 39) | |
| Keyboard-only game to level 3, with an image, an audio and a video question; sound plays | skipped (decision 39) | |
| «Salir del juego», restart: the player is still there | skipped (decision 39) | |
| Save at `%APPDATA%\trivia\save\<steamid64 or local>\game.json` | skipped (decision 39) | |
| `CREDITS.md` in the folder | skipped (decision 39) | |

### Linux x64 (no Nix)
Date: 2026-10-13 · Build commit: 06c39dc

| check | result | note |
|---|---|---|
| Network off before unpacking | skipped (decision 39) | |
| `tar xzf`, `cd Trivia-<version>-linux-x64`, `./trivia` | skipped (decision 39) | |
| Starts fullscreen; F11 toggles | skipped (decision 39) | |
| Keyboard-only game to level 3, with an image, an audio and a video question; sound plays | skipped (decision 39) | |
| «Salir del juego», restart: the player is still there | skipped (decision 39) | |
| Save at `~/.config/trivia/save/<steamid64 or local>/game.json` | skipped (decision 39) | |
| `CREDITS.md` in the folder | skipped (decision 39) | |

## Steam Cloud test
The developer's check that Auto-Cloud syncs one save per Steam user between machines (plan 87 part 4). Fill the table once, with date and build commit; agents don't run it.
- **Needs:** the real App ID (masterplan 10 part 1, `task 253`), the Auto-Cloud values above entered in Steamworks (part 2, `task 254`), a packaged Steam build (`task 650` or part 7's upload to `beta`).
- **Machines:** A and B, one Windows and one Linux or the Deck.
- **Result:** ✓, ✗ or n/a; a ✗ gets a note on how to reproduce.

Date: · Build commit:

| check | result | note |
|---|---|---|
| A plays (new player, a few questions) → quit → B shows the same players and seen counts | | |
| Two Steam accounts on one OS login → separate saves (`save/<id>/` each) | | |
| Family Sharing borrower → own save | | |
| Offline on both, play on both, then online → Steam's conflict dialog; the picked side wins whole | | |
| Steam not running → full game, notice shown, no flag action, nothing written under `save/` | | |
| Steam's cloud file list (game properties, or `store.steampowered.com/account/remotestorage`) shows only `game.json`, never `.tmp`, `backup/`, `dev/` | | |

## Steam Deck Verified
Requirements to plan for: full controller support with correct glyphs (IN), legible text at 800p, the on-screen keyboard for text entry, no launcher, working default settings, no warnings on start. Before applying (decision 125: Steam Deck: best effort, review without a Deck at hand):
- Fit at 1280×800 (plan 46, done); image peek on image questions (plan 113, done: every image question's picture whole at 1280×800, task 923); the Gamepad template as Steam Input default (milestone 10; "Steamworks app configuration (SW-7)" → "Application → Steam Input").
- With those in, request Valve's Deck review (SW-12) without a real-Deck test.
- Real-Deck test and tuning: plan 90 once a Deck is at hand.

## Modding
Player-facing: [`modding/README.md`](../modding/README.md).
Mods are folders the shell serves over `app://trivia/` before our own client and data (pm plan 112, milestone 15). The shell only reads mod files as bytes; mod code runs only in the page.
- Code: `app/desktop/mods.mjs` (`readManifest`, `discover`, `readSettings`/`writeSettings`, `arrange`), layers in `resolve.mjs` (`makeResolver({ …, layers })`), wiring in `main.mjs`; test `resolve.test.mjs` (`npm test`).
- Sources: local folder (`TRIVIA_MODS_DIR`, else packaged `<userData>/mods/`, created at start; dev repo `mods/`, gitignored), then Workshop (below); each direct subfolder with a `mod.json` is a mod; local before Workshop on a duplicate id (decision 127).
- Only with a valid Steam user (decision 111): otherwise listed `no_user`, no layers.
- Settings (decision 136: Mod settings: per machine in <userData>/mods.json, one ordered list, top wins): `<userData>/mods.json` (dev `state/desktop/mods.json`); one ordered list = load order, index 0 = top = wins; new mods appended `on`; unknown ids kept (`missing`); read once per run, changes on restart; atomic writes.
- Layers: enabled valid mods top first, ours last; mod root mirrors the URL space (`app://trivia/<rel>` → `<mod>/<rel>`); first hit wins, whole files.
- `/data/` (decision 128: Bundles from mods: the shell merges bundles.json; mod ids namespaced <mod id>:<id>; details in `plans/22-bundles.md` "Player bundles (mods)"):
  - `/data/bundles.json`: merged, ours then loaded mods' rows (`bundleRows()`), ids `<mod>:<id>`; built once per run.
  - `/data/bundles/<mod>:<bundle>/<rel>` → `<mod dir>/data/bundles/<bundle>/<rel>` via `contained()`, only for a loaded mod that lists that bundle; else 404; no colon reaches the file system.
  - Every other `/data/` file: ours only, never overlaid (a mod's `data/pool.json` isn't served).
- Full conversion: a mod's `index.html` wins the SPA fallback too.
- Not overlaid: `/media?url=…`, `/api/*` (404), a mod's own files (decision 148: Overlay: a mod's entry and root style.css never shadow our files): its `mod.json`, its `entry` and its root `style.css` (served under `/mods/<id>/` only; an entry `main.js` never replaces our `/main.js`).
- `--no-mods`: no layers this run (way back from a full conversion); safe starts: "Modding: mods screen and safe start".
- `--check-mod <folder>` (pm plan 120, decision 133: Player bundle kit: check with trivia --check-mod, kit in modding/ shipped in the install folder): the loader's validators on one folder, no install or restart needed.
  - Headless like `--publish-mod`: before the instance lock, no window, no Steam; runs alone; exit 0 no errors, 1 errors, 2 usage; Windows packaged: also `<folder>-check.log` beside the folder + message box.
  - `app/desktop/check-mod.mjs` `checkMod` (pure Node, mod files read as data): `readManifest`, `bundleRows`, per bundle and language `categories.json`, pool file, `modPool` from our built `engine/pool.js` (dev `app/client/dist/`, packaged `resources/client/`; never the mod's), media present and `contained()`.
  - Output: errors/warnings with codes, dropped questions (id + reason code), difficulty coverage per age group, "loads as is" or "N error(s)"; `preparePublish` runs it too (its errors become publish warnings).
- Player kit `modding/` (guide `README.md`, `examples/`, `bundles.md`, `bundle-prompt.md`, `template-bundle/`): shipped in the install folder as `modding/` (`electron-builder.yml` `extraFiles`, beside the executable, Steam "Browse local files"); `trivia-release-check` step `modkit` runs the packaged `--check-mod` on `modding/template-bundle` and each `modding/examples/*`; `credits_check.mjs` skips `modding/` (template image ours, CC0).
- With mods on (decision 123: Achievements in games with mods on: allowed or off?; decision 146: Achievements, mods screen and rich presence with mods on): achievements as without ("Achievements in Steamworks"); flags hidden on player questions; reports ours only; telemetry keeps `isOurs` answers only, `games[].mods` = this run's overlay non-empty; rich presence unchanged (no "modded" token); no achievements line on the mods screen.
- Path safety: `contained()` compares `realpath`s against the layer root's `realpath` (every root, ours too): symlinks out of a layer miss; `..`, encoded `..`, absolute and drive-letter paths stay inside or miss; files only.
- MIME by extension (`MIME` in `resolve.mjs`), unknown → `application/octet-stream`. Paths case-sensitive (Windows: match case).
- stderr: one line per mod (`trivia: mod <id> <state> [warnings]`) and a summary (`trivia: mods: 2 loaded, 1 invalid`).
- Bridge name (decision 130: Preload bridge renamed window.trivia → window.triviaShell; window.trivia is the mod API): the shell's bridge is `window.triviaShell` (`preload.cjs`, read only by `lib/desktop.ts`); `window.trivia` is the page's mod API ("Modding: `window.trivia`"); mods can reach `window.triviaShell` too: accepted.
- Code add-ons (pm plan 117, decision 131: Code add-ons: shell-generated /mods.js, entry default export setup(trivia), mods run before data and language load):
  - `/mods.js`: `modsScript(list)` in `mods.mjs` (pure), served by `resolve.mjs` ahead of every layer (a mod can't override it); `export default [{ id, name, version, entry, style }, …]`: loaded mods only, run order = bottom of the load order first; `entry` from `mod.json` (null if none), `style` = `/mods/<id>/style.css` if the mod has a root `style.css` (null else); no disk paths; `--no-mods`, no valid user, no mods: `export default [];`.
  - `/mods/<id>/<rel>` → `<mod dir>/<rel>` via `contained()`, loaded mods only, files only, `mod.json` never; else 404. Relative imports and `import.meta.url` stay in the mod's folder. Reserved: our `dist/` has no root `mods.js` or `mods/`.
  - Outside the shell (Vite dev, dev server): no `/mods.js` → no mods.
  - Page loader: `app/client/src/lib/mods.ts` `loadMods()`, first in `main.ts`, before `language()` (save + data) and `initLang`; per mod in run order: `style` linked after our CSS (later = stronger, top mod wins the cascade), then `import(entry)` and `await default(trivia)` with a view scoped to that mod; import + setup race a 5 s timeout. Then mods' `i18n.add` catalogs apply, `language()` → `initLang` → `initDocument` → mount `App` → event `ready`.
  - Error codes (`modErrors()`, `console.error`; no UI here, plan 118 maps them to `t()`): `load_failed` (import rejects), `setup_failed` (setup throws), `timeout` (> 5 s): the mod's registrations removed (late ones too), the next mod loads, the game always starts; `hook_failed`: a hook throws later (data, action, event, screen, layer, menu row) → caught at the call site, that registration dropped for the run, the game goes on unhooked.
  - Run order: entries bottom-up, so the top mod registers last; hooks run in run order; for screens the last registration (top mod) wins.
  - No stability promise: `window.trivia`, its types and module paths may change with any update; renames in the patch notes (pm plan 102).

## Modding: `window.trivia`
Player-facing: [`modding/README.md`](../modding/README.md).
The page-side mod API (pm plan 117, decisions 130, 131), defined in `app/client/src/lib/mods.ts` (type `TriviaApi`: the reference, with source maps and the public repo); listed here with the call sites for the modding guide (pm plan 121). No stability promise.
- `setup(trivia)`: an entry's default export; `trivia` is scoped to the mod (`trivia.mod`, registrations tagged with its id); `window.trivia` is the unscoped view. Registrations return an `off()`.
- `version`: `buildInfo().version` (decision 91); `mods`: loaded mods `{ id, name, version }[]`; `mod`: this mod (scoped view only).
- `modules`: same instances as by path (decision 124), exports read-only: `api` (`lib/api.ts`), `engine` (`read`, `run` from `lib/engine.ts`), `game` (`engine/game.ts`), `i18n` (`t`, `lang`, `fill`), `input` (`pushScope`, `lastDevice` from `lib/input.svelte.ts`), `sound` (`sfx`, `music` from `game/sound.svelte.ts`), `svelte` (`mount`, `unmount`, `flushSync`: compiled mod components import our runtime from `/vendor/svelte.js`).
- `data(fn)`: `lib/data.ts` locale load, after the mod-bundle step (plan 115), before `engineData(…)`; `fn({ locale, questions, bundles, ageGroups })` on a copy → change in place or return a partial replacement (arrays); mod questions have `<mod id>:<id>` ids (decision 128); per locale load, in run order; sync only.
- `actions.before(fn)` / `actions.after(fn)`: `lib/api.ts` `hooked()`, behind `gameAction()` and `playJoker()` (action `joker`); `before(action, body)` on a copy → body or void (e.g. `new` with `body.jokers`), the engine still validates; `after(action, game)`: a copy, may be null.
- `i18n.add(locale, catalog, opts?)`: `lib/i18n.ts` `addCatalog()`; existing UI locale → deep-merged over it (`es-ES` is its own); new → `merge(base, catalog)` (`opts.base`, default `en`), added to `CATALOGS`, `UI_LANGS`, `ENDONYMS` (`opts.endonym`); UI language only, question locales stay ours; in `setup` (applied before `initLang`), later calls after a reload.
- `screens.replace(name, component)` / `screens.dom(name, render)`: `game/screens/registry.ts` `screenFor()`, read once when `Game.svelte` mounts; names `Start`, `Language`, `Player`, `Choice`, `Level`, `Select`, `Question`, `Correct`, `Wrong`, `Victory` (`SCREENS`, files `game/screens/*.svelte`); same props as ours; `dom`: `render(el, props) → cleanup?` through `game/screens/DomScreen.svelte`; a throwing replacement → `hook_failed`, ours instead (`screenFailed()`, `Game.svelte`'s boundary).
- `screens.show(render)` → `{ close() }`: a full-screen layer over the game (`DomScreen` in `Game.svelte` via `watchLayers()`), modal with its own input scope; Esc, pad B or `props.close` close it.
- `menu.add({ label, onselect })`: Esc menu rows in a last column (`Overlay.svelte` `menuRows()`); `label` shown as is (not via `t()`, `check:literals` doesn't see it).
- `on(event, fn)` → `off`; payloads `structuredClone`d, return values ignored:
  - `ready`: after mount (`main.ts`)
  - `screen` `{ name }`: after a switch (`Game.svelte` `go()`)
  - `question:shown` `{ id, level }`: after the switch to Question, its media ready or the preload cap (`Game.svelte` `go()`)
  - `game:start` `{ game }`: after a successful `new`; `game:end` `{ game, result }`: `result` null → won/lost/abandoned, a `new` over a running game too; `question:answered` `{ id, level, index, correct }`: after `answer` (all `lib/api.ts` `events()`)
- `css(href)`: a `<link>` after ours, e.g. `trivia.css(new URL("./x.css", import.meta.url))`.
- Internals, not on `window.trivia`: `loadedMods()`, `modErrors()` (mods screen, plan 118), `modsOn()` (telemetry, decision 146).

## Modding: module paths
Player-facing: [`modding/README.md`](../modding/README.md).
The client ships as a readable tree, so a mod replaces any single module, component CSS or stylesheet by putting a file at the same path (pm plan 111, decision 124: Readable client build: output naming rule for mod overrides). The modding guide (pm plan 121) links this section.
- Build: `app/client/vite.config.ts` (`svelteRuntime()` plugin, `preserveModules`, `preserveModulesRoot: "src"`, naming functions, `minify: false`, `sourcemap: true`, `cssCodeSplit: true`), `svelte.config.js` (`cssHash`).
- Naming rule (paths relative to `app/client/src/` and `app://trivia/`):
  - `lib/data.ts` → `lib/data.js`; `game/Game.svelte` → `game/Game.svelte.js`; runes module `game/sound.svelte.ts` → `game/sound.svelte.js`
  - component CSS next to its component: `game/Game.svelte.css`
  - global CSS keeps its path: `app.css`, `game/theme.css` (colour variables)
  - third-party: `vendor/<package>/<path>`; Vite helpers: `_virtual/…`
  - Svelte runtime: one file `vendor/svelte.js` + `.map` (decision 149, decision 159, task 1025): every `svelte`, `svelte/*` import points at it; it re-exports all of `svelte`, `svelte/internal/client`, `svelte/internal/disclose-version` and every other `svelte/*` we import (`svelte/easing`, `svelte/internal/flags/legacy`); one instance; a precompiled mod component rewrites its `svelte…` imports to `/vendor/svelte.js`; not overridable per runtime module
  - `.map` next to each JS file; no hashes; `public/` files where they are (`audio/`, `fonts/`)
- Every export kept: each shipped `src/**/*.{ts,svelte}` (not tests, `engine/test/`, `locales/xx.ts`) is an extra Rolldown input with `preserveEntrySignatures: "strict"` (task 1005); `vendor/svelte.js` is a second build in the `svelteRuntime()` plugin, entry `export *` per specifier (decision 145), so a by-path import sees the source's exports, not only the ones the game uses.
- `index.html`: one `<script type="module" src="/main.js">` + `app.css`; the browser follows imports; a full conversion replaces it.
- Scoped class names: `svelte-<component path>` (e.g. `svelte-game-hud`), stable per component path, not per CSS content: a theme's selectors survive our CSS changes.
- Screen list (plan 116): `game/screens/*.svelte` (one file per full screen, `Game.svelte` mounts them); Question pieces: `game/question/*`; `window.trivia`'s screen names ("Modding: `window.trivia`") and the guide (task 909).
- Not overridable by path (no file of their own):
  - inlined `__APP_VERSION__` and other `define`s
  - the preload helper's dependency list inside `main.js` (a mod adding a module imports it itself)
  - plugin output `credits.json`, `CREDITS.md` (replaceable, meaningless)
  - `/data/` (only bundles, "Modding" above) and `/media`
- Caching: none across updates ("Builds and depots", task 946).
- No stability promise: paths may change with any update and break mods; renames go into the patch notes (pm plan 102).

## Modding: Workshop source
Player-facing: [`modding/README.md`](../modding/README.md).
Subscribed Workshop items are mod sources next to the local folder (pm plan 114); the page reads and orders mods over IPC. Steam's client downloads items, never us; the overlay stays this run's.
- Code: `app/desktop/workshop.mjs` (`workshopItems(ugc)`: `steam.workshop` → `[{ dir, publishedFileId, state, warnings }]`, ids as decimal strings; `fakeUgc(dir)`; pure, no Electron, no binding import), `discover({ local, workshop })` in `mods.mjs`, wiring in `main.mjs`.
- Only with a real Steam user (`hasSteamId()`, decision 111); else no Workshop entries.
- Item states (`EItemState` bits): `Installed` + install folder → `installed` (+ warning `needs_update` with `NeedsUpdate`: installed files load); `Downloading`/`DownloadPending` → `downloading`; neither → `downloadItem(id, false)` once, `downloading`; `DisabledLocally` → `disabled`. `downloading`/`disabled`: listed, not loaded, no error.
- Installed item: `mod.json` at the item's root, else `no_manifest`; `mod.json` `workshopId` ≠ the item's id → warning `workshop_id_mismatch`, still loads.
- Identity (decision 127: Workshop mods: identity and duplicates): key = `mod.json` `id`; published file id beside it (string), never the settings key; local before Workshop; two Workshop items with one id: lower published file id wins, the other `duplicate_id`.
- New items: appended at the end of the load order, `on` (subscribing is the opt-in); unsubscribed ids stay in `mods.json`, omitted from `mods:list`.
- Refresh: no event in the binding, no timer; every `mods:list` re-queries Workshop and re-runs `discover` + `arrange`.
- stderr: `trivia: mod <id> workshop <publishedFileId> <state>`.
- IPC (`handle()`, sender origin `app://trivia/`), bridge `mods` in `preload.cjs`, typed `mods: ModsBridge | null` in `app/client/src/lib/desktop.ts` (null in the dev server):
  - `mods:list` → `{ mods: ModEntry[], noMods, validUser }`; `ModEntry`: `id`, `name`, `version`, `description`, `source` (`local`/`workshop`), `publishedFileId`, `kind`, `languages`, `on` (setting), `active` (in this run's layers), `position`, `state`, `warnings` (codes), `error` (`{ code, field? }`), `dir` (basename only).
  - `mods:set([{ id, on }])` in load order: ≤ 500, slug ids, boolean `on`, no duplicates, else rejects `bad_mods`; ids left out keep their order after the given ones; writes `mods.json` atomically, returns the new list; next start only (`active ≠ on` until then). Writes without a valid user too.
  - Codes stay codes; the mods screen (plan 118) maps them to `t()`.
- Dev: `TRIVIA_DEV_WORKSHOP_DIR=<dir>`, only with `TRIVIA_DEV_STEAM_USER=1` (one stderr line): `<dir>/<numeric id>/` installed item, `<dir>/<id>.downloading/` downloading.
- Steam updating files while running: accepted; restart after updates.

## Modding: mods screen and safe start
Player-facing: [`modding/README.md`](../modding/README.md).
The shell side of the mods screen (pm plan 118; screen: `04-ui-tv-display.md` "Mods"): a one-time notice before any mod runs, a crash marker that makes the next start a safe one, restart to apply. The page only calls IPC; the shell reads and writes `mods.json` and relaunches.
- Code: `app/desktop/mods.mjs` (`noticed`, `withNotice`, `readMarker`/`writeMarker`/`clearMarker`, hold-off in `arrange`), `main.mjs` (safe start, marker, relaunch, IPC), `preload.cjs`, `app/client/src/lib/desktop.ts` (`ModsBridge`), `main.ts` (`ready` → `mods.ready()`).
- Notice (decision 151: Mods notice per install in mods.json; new mods held off until it): `mods.json` gains `notice: true` + `noticeAt`, per machine like decision 136; while missing, `arrange()` appends new mods `on: false`, so no mod code runs before the notice; after it, new mods appended `on`; accepting never touches existing rows.
- Crash marker (decision 153: Mods crash marker: mods-start.json, cleared on ready or a live page after 20 s): `mods-start.json` beside `mods.json` (`<userData>/`, dev `state/desktop/`), `{ at, mods: [active ids] }`, written atomically before `loadURL` only when the run has layers.
  - Cleared on `mods:ready` (our client after `window.trivia`'s `ready`; a full conversion calls `window.triviaShell.mods.ready()`), or when the page answers a ping 20 s after `did-finish-load` (3 s answer window).
  - Relaunch without mods: no ping answer, `render-process-gone` (not `clean-exit`) or a main-frame load failure while the marker is set.
  - Not cleared on quit: closing a broken start early gives a safe next start (intended).
- Start: marker found → deleted, no layers, `safeStart = { reason: "crashed", mods }`; `--no-mods` → `safeStart = { reason: "flag" }`; else `null`; stderr line each. No loop: a safe start writes no marker.
- Manual safe start (decision 152: Manual safe start: --no-mods only): `--no-mods` in Steam's per-game launch options (Properties → Launch options); no held key or pad button, no second Steamworks launch option.
- Restart (decision 154: Mods restart drops our own flags): `mods:restart` and the crash relaunch flush the save queue and telemetry like a quit, `app.relaunch({ args })` without our own flags (`OWN`/`relaunchArgs()`: `--no-mods`, `--import-save <file>`, `--force`, …, with their values), Electron/Chromium/Steam args kept, `app.exit(0)`; `SteamAppId` stays in the environment. Overlay and presence after a relaunch under Steam: manual release row (task 1010).
- IPC (beside `mods:list`/`mods:set`, "Modding: Workshop source"):
  - `mods:list` also returns `safeStart` and `notice`
  - `mods:notice` → sets the notice, returns the list
  - `mods:restart` → relaunch as above
  - `mods:ready` → clears the marker
- Bridge: `window.triviaShell.mods` = `{ list, set, notice, restart, ready }`.

## Modding: Publishing
Player-facing: [`modding/README.md`](../modding/README.md).
Modders publish a mod folder as a Workshop item with the game itself (pm plan 119); Steam's client uploads, we make no network calls of our own. The folder is only read and copied, never run. The modding guide (pm plan 121) copies this section.
- Command: `trivia --publish-mod <folder> [--changenote <text>] [--visibility public|friends|unlisted|private] [--content-only] [--dry-run]`; dev `trivia-desktop --publish-mod …`; packaged: the game executable (Linux `trivia`, Windows `Trivia.exe`) from a terminal, Steam client running.
- Flags: `--changenote`, `--visibility`, `--content-only`, `--dry-run` only with `--publish-mod`; `--publish-mod` not with `--import-save`/`--no-mods`.
- Headless: before the instance lock (game may be closed), no window; exit 0 ok, 1 failed, 2 usage.
- Code: `app/desktop/publish.mjs` (`preparePublish`, `describe`, `publish`, `writeWorkshopId`, `WORKSHOP_TAGS`; pure, no Electron, no binding import), `publishMod` in `main.mjs`.
- Steps:
  1. `readManifest`: errors stop (code + field), warnings printed (`game_version`, unknown keys/languages).
  2. Preview: first of `preview.png`/`.jpg`/`.gif` at the root; > 1 MB → error; none → warning on first publish (Steam placeholder).
  3. Stage: copy into a temp dir; skipped: dot files and dot folders (`.git`, `.DS_Store`), symlinks out of the folder or looping (warning); preview stays; prints file count + size; the upload is the copy; temp dir removed at the end.
  4. Tags: kinds + `languages` base tags (`es-ES` → `es`), only names in `WORKSHOP_TAGS` (the list entered in Steamworks), others dropped with a warning.
  5. `--dry-run` stops: item id or "new", title, description length, visibility, tags, preview, file count/size; no Steam needed.
  6. Steam: real Steam user only (`hasSteamId()`, decision 111); `TRIVIA_DEV_STEAM_USER=1` doesn't count; else "publishing needs the Steam client running and logged in", exit 1.
  7. First publish (no `workshopId`): `createItem`, `workshopId` written into `mod.json` (only that key, atomic) and the staged copy, item URL printed.
  8. Update: content; unless `--content-only` also title (`name`), description, tags, preview; visibility on first publish (default private) or with `--visibility` only (an update never flips a public item back); change note from `--changenote`.
  9. Progress: `preparing config`, `preparing content`, `uploading 40 % (12.3 / 30.1 MB)`, `uploading preview`, `committing` (on status or 10 % step change).
  10. Result: item URL; failure: the binding's reason (e.g. not the item's owner, Workshop off for the app), exit 1. The binding waits 30 s on submit: a longer upload is polled to the end and reported "submitted, check the item page".
- `workshopId` (decision 132: Workshop publishing: where the published file id lives): `mod.json` field, decimal string, written on first publish; travels to subscribers (warning `workshop_id_mismatch` on a copy under another item); failed first publish keeps it (next run updates the empty item); delete it for a fresh item.
- Legal agreement: after every create/submit the command prints `https://steamcommunity.com/sharedfiles/workshoplegalagreement`; the item stays hidden until the modder accepts it.
- Windows (packaged): no console; every line also to `<folder>/../<id>-publish.log` (beside the mod, not inside), result in a message box (ok: URL; failed: reason + log path). Linux/Deck: stdout/stderr only.
- `trivia-steam` is for our own builds only, never for mods.

## Telemetry store
Opt-in telemetry's shell side (pm plan 106, decisions 119, 121): consent, install id and one session buffer per run, per install, never in the Steam Cloud save; sent by main ("Telemetry send").
- Code: `app/desktop/telemetry.mjs` (`makeTelemetry(dir, { version })`; pure `node:fs`), wiring in `main.mjs`.
- Folder: `TRIVIA_TELEMETRY_DIR`, packaged `<userData>/telemetry` (sibling of `save/`, outside Auto-Cloud), dev `state/telemetry/`.
- `install.json`: `{"consent": true, "install": "<uuid v4>"}`, `{"consent": false}`, missing = never asked.
- `sessions/<session>.json`: plan 105's body minus `ticket`, plus `index` (page bookkeeping); `length_s` stamped per write and in `before-quit`; atomic, own queue, `before-quit` waits for it.
- Rollover past 30 games, 500 answers or 60 KiB: new session file, sealed games dropped from later records this run; ≤ 100 answers per game; ≤ 5 `*.json` files, oldest by mtime deleted.
- `pending()` export: earlier runs' files (incl. `.retry.json`), no IPC; `close()`, `outgoing()`, `settle()`: the send's file side.
- Only with a valid user (decision 111); without one every call is a no-op and nothing is created. Logs error codes only, never ids or bodies.
- IPC (`handle()`, sender origin `app://trivia/`), bridge `telemetry` in `preload.cjs`, typed optional `telemetry: TelemetryBridge` in `app/client/src/lib/desktop.ts`:
  - `telemetry:state` → `{ available, consent }` (`{ false, null }` without a valid user).
  - `telemetry:consent(yes)` → state; yes: id if missing, session starts; no: `{"consent": false}`, `sessions/` deleted.
  - `telemetry:load` → current session's `{ games, index }` or null.
  - `telemetry:record({ games, index })`: parallel arrays, plain objects, ≤ 200 games, ≤ 1 MiB, else rejects `bad_telemetry`; ignored without a yes.

## Telemetry send
Main posts each session file to plan 105's `POST /telemetry` (pm plan 107, decision 120: Telemetry send: at quit, one later try at the next start); silent, nothing to the page, no IPC. The page's request block stays.
- Code: `flush`, `sendLeftovers`, `sendSession`, `withTicket` in `main.mjs`; `postJson`, `TELEMETRY_IDENTITY` in `report.mjs`.
- Gate per send: valid user, `install.json` yes, URL set; closed → no ticket, no request; one start line `trivia: telemetry off` if closed at start.
- URL: the reports' base (`reportUrl`, dev `TRIVIA_REPORT_URL`) + `/telemetry`.
- Ticket: fresh per request, `getAuthTicketForWebApi({ genericString: "trivia-telemetry" })` (= server `TELEMETRY_IDENTITY`), cancelled after; no callback in 2 s → status 0 (reports too).
- Body: session file minus `index`, `install` from `install.json`, `ticket`; > 64 KiB → deleted unsent; unreadable → deleted.
- Quit: `before-quit` → window hidden, save queue + last stamp, this run's file sent; 4 s for ticket + request, then quit anyway. `SIGTERM` reaches `before-quit` on its own (checked on Linux).
- Answers: `201`, `200` (duplicate), `400`, `413`, `415`, `503` → deleted; `401`, `429`, `500`, `502`, status 0 → `<session>.retry.json`.
- Next start: 30 s after the page loads, every `pending()` file, oldest first, one at a time, 5 s/10 s timeouts; deleted after this try whatever the answer.
- stderr: `trivia: telemetry → <status> kept|dropped`; never body, ticket, ids or URL.

## Question reports
The shell's half of question reports (pm plan 93, decision 93, decision 111): main posts one report to plan 103's `POST /reports` per player click; the page passes fields, never a URL, and never sees the ticket. The page's request block stays.
- Code: `app/desktop/report.mjs` (`reportTarget`, `reportFields`, `postReport`, `IDENTITY`; pure Node `http`/`https`, no Electron), `sendReport` + `withTicket` (shared with telemetry) in `main.mjs`.
- URL: `reportUrl` beside `version` in `app/desktop/package.json` (base URL, `/reports` appended); empty = no send, copy only. Dev override `TRIVIA_REPORT_URL` only with `TRIVIA_DEV_STEAM_USER=1`, then `dev-<random>` tickets (plan 103's dev check); dev switch without a SteamID: dev tickets too.
- Ticket: fresh per send, `getAuthTicketForWebApi({ genericString: "trivia-reports" })` (= server `TICKET_IDENTITY`), cancelled after the response; never logged.
- Timeouts: 5 s connect, 10 s total; no retry, no request at start, no health check.
- stderr: `trivia: report: sent` / `failed <status> <error>` / `bad field <name>`; never fields or tickets.
- IPC (`handle()`, sender origin `app://trivia/`), bridge `report` in `preload.cjs`, typed optional `report: ReportBridge` in `app/client/src/lib/desktop.ts`:
  - `report:available` → URL set and a valid user (or the dev switch).
  - `report:send({ question, lang, text, note?, version, pool })`: plan 103's field limits, else rejects `bad_report`; → `{ ok: true, id }` or `{ ok: false, status, error, retryAfter? }`; `status: 0` without a response (`no_connection`, `timeout`, `no_ticket`, `unavailable`, `too_large`), else the server's code (`retryAfter` on 429).

## Modding: `mod.json`
Player-facing: [`modding/README.md`](../modding/README.md).
A mod is a folder with a `mod.json` (pm plan 112). The validator `readManifest` in `app/desktop/mods.mjs` is the source of truth; this schema is for the modding guide (plan 121) and editors.
- Also checked by the validator, not by the schema: file ≤ 64 KB UTF-8; `entry` exists inside the mod (symlinks resolved); unknown keys and unknown `languages` tags are warnings; `game` ≠ running version: warning `game_version`, still loaded.
- Errors: `no_manifest`, `bad_json`, `bad_field` (+ field), `duplicate_id` (+ other folder; local before Workshop, then lower published file id, decision 127), `entry_missing`, `not_a_folder`.
- `kind` when missing: `data/bundles/` or `data/bundles.json` → `bundle`, any `.css` → `theme`, `entry` → `code`, root `index.html` → `conversion`.
- Settings: `<userData>/mods.json` (dev `state/desktop/mods.json`), `{ "version": 1, "mods": [{ "id", "on" }] }`, index 0 = top = wins.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "mod.json",
  "type": "object",
  "required": ["id", "name", "description", "version", "game"],
  "properties": {
    "id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9-]{1,63}$" },
    "name": { "type": "string", "minLength": 1, "maxLength": 80 },
    "description": { "type": "string", "maxLength": 2000 },
    "version": { "type": "string", "minLength": 1, "maxLength": 32 },
    "game": { "type": "string", "pattern": "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)$" },
    "languages": { "type": "array", "items": { "type": "string", "enum": ["es", "es-ES", "en", "de"] } },
    "entry": { "type": "string", "pattern": "\\.m?js$" },
    "kind": {
      "type": "array",
      "uniqueItems": true,
      "items": { "enum": ["bundle", "theme", "code", "conversion"] }
    },
    "workshopId": { "type": "string", "pattern": "^[1-9][0-9]{0,19}$" }
  }
}
```

## Tasks
- [x] SW-1 Decide the shell (OQ-29); record it in `decisions.md`. *Done 2026-10-12: Electron (D-63).*
- [x] SW-2 Electron shell skeleton: window, fullscreen toggle, loads `app/client/dist/`, preload bridge; pick the Steam binding (steamworks-ffi-node or steamworks.js: maintenance, overlay, Electron version). *Done 2026-10-12 (pm plan 54, D-71): `app/desktop/` (`main.mjs`, `resolve.mjs`, `preload.cjs`, `package.json`), `app/client/src/lib/desktop.ts`, `lib/engine.ts` (`MemoryStore`), `Overlay.svelte`, `flake.nix` (`trivia-desktop`, `pkgs.electron` 43); whole game without Python checked over CDP under Xvfb (task 318: level 12, every joker, undo, abandon, media, samples, clean console). Developer play test: plays fine (pm decision 29, 2026-10-13). Binding: steamworks-ffi-node (pm decision 28, D-63; task 353).*
- [x] SW-3 `FileStore` for the save in the user data folder (atomic writes, Windows retry). *Done 2026-10-12 (pm plan 55, D-72): `app/desktop/save.mjs`, `main.mjs` (userData path, `save:*` IPC, write queue, quit wait, `--import-save`), `preload.cjs`, `lib/desktop.ts`, `lib/store.ts` (`FileStore`, shared `WriteQueue`), `lib/engine.ts` (store choice, notice, `saveError()`), `engine/save.ts` (`SaveNewerError`), start-screen notice, «Salir» flush, `es` catalog; kill loop (60 × `SIGKILL` of main mid-write, 1–5 MB documents): `game.json` always one of the documents sent, stale `.tmp` dropped, no backup.*
- [x] SW-4 Screen check at 1280×800 and 1280×720; fixes. *Done 2026-10-12 (pm plan 46): letter picker for a pad (`LetterPicker.svelte`); throw-away Playwright walk (pm decision 6) of every screen and state at 1280×800, 1280×720, 1920×1080, 3840×2160, keyboard prompts and Xbox glyphs (faked standard pad), longest pool content, 9 names of 30 characters, 11 levels short, error box; computed font sizes < 9 px reported. Fixes: credit line 0.8 → 0.9 u; «medio no disponible» chip `rem` → `--u`; pad glyph labels (LB/RB/LT/RT) 10.5 → 13.5 viewBox units (7 → 9.2 px at 1280); supply report in four columns when more than 4 levels are short, Choice gaps 0.8 u while it shows (the title left the screen at 720p and 1080p). 1080p unchanged elsewhere (ImageMagick `compare`). Credit line and «Respuesta final» stay in the bottom margin (pm decision 52). Real Deck check: plan 48.*
- [x] SW-5 Local Windows and Linux builds with electron-builder. *Done 2026-10-13 (pm plan 56, D-73): `app/desktop/electron-builder.yml`, `stage-media.mjs`, `after-pack.mjs` (Linux `--no-sandbox` launcher), own `package-lock.json`, `main.mjs` `roots()` packaged branch, `flake.nix` (`trivia-desktop-build`); Windows zip + Linux tar.gz, media staged from the pool; packaged Linux build played offline (task 330); start test outside Steam skipped (decision 39).*
- [ ] SW-6 Local CI: per-commit checks (AGENTS.md) and a release check before every Steam upload ("Builds and depots"); no GitHub Actions. *Moved to S5 (pm decision 14, D-73); per-commit checks in AGENTS.md since 2026-10-12; release check: `trivia-release-check` (2026-10-13, task 679); upload: `trivia-steam upload --branch beta` (2026-10-13, task 680).*
- [ ] SW-7 Steamworks app: App ID, depots, launch options, supported languages, Cloud path.
- [x] SW-8 Steam binding steamworks-ffi-node (D-63): overlay, achievements, on-screen keyboard, language; the game runs without Steam. *Done 2026-10-13 (pm plan 85): bridge `window.trivia.steam` (`main.mjs` init/callbacks/shutdown, `preload.cjs`, `lib/desktop.ts` `SteamBridge`; App ID 480 until SW-7, `TRIVIA_STEAM_APPID`; SDK libs gitignored in `app/desktop/steamworks_sdk/` or the flake's SDK 1.62, decision 69), Steam language → `guessTag()`, overlay Windows only (D-92), floating keyboard for the name, `GetInputTypeForHandle` glyphs, rich presence (`steam-presence.vdf`); `unlock()`/`steamId()` pass-through for SW-11 and Cloud. Packaging: task 650. Developer check under Steam: pm task 652's decision.*
- [x] SW-9 Media bundle: resize, re-encode, size budget; checked by `stage-media.mjs --check`. *Done 2026-10-14 (pm plan 132, D-104): `app/desktop/resolve.mjs` (`shippedName`), `stage-media.mjs` (encode, `--check`), `media-budget.json`, `flake.nix`, `authoring/steam/{credits_check,smoke}.mjs`, `release_check.py` (`media-budget` step); 2549 → 679 MB.*
- [ ] SW-10 SteamCMD upload script; build account; beta branch. *Plan: pm plan 89; `trivia-release-check` and `trivia-steam upload --branch beta` (depots windows/linux/content) since 2026-10-13 (tasks 679, 680); first upload: tasks 681, 682.*
- [x] SW-11 Achievements: list, icons, Steamworks setup. *Done 2026-10-13 (pm plan 86): list per decision 73 (25 now, 3 mode wins with MD-8, one per regional bundle with its DLC); `engine/achievements.ts` (`qualifies`, `earned`, `inSteamworks`), `lib/achievements.ts` (unlock after load and at game end, valid user + live bridge only), triggers without a save change (decision 139); icons `app/desktop/achievements/` (`render.sh`, 256×256); setup values above and `steam-achievements.vdf`. Pending: entering in Steamworks (pm decision 140) and the developer check under Steam (pm decision 141).*
- [ ] SW-12 Steam Deck test and the Deck Verified review. *Plan: pm plan 90 (real-Deck checklist on the Steam-installed `beta`, Valve's criteria, Cloud, suspend/resume; review request or S6 note).*
- [ ] SW-13 Remote Play Together (after IN-6).
- [ ] SW-14 macOS build (later; developer account and notarization).
