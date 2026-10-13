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

The shell's own code stays tiny: create a fullscreen window, load `app/client/dist/`, expose `loadSave`/`writeSave` and the Steam calls to the page through a preload bridge (no Node in the page itself).
- Window option `webPreferences.autoplayPolicy: "no-user-gesture-required"`: a gamepad press isn't user activation in Chromium (HTML spec: only key, mouse, touch), so a pad-only start would stay silent (plan 45, IN-4).
- Credits: the shell adds its own entry (Electron, MIT, plus the Chromium licence file Electron ships) to the generator `app/client/credits.ts` (PUB-5, plan 47).

## Steam features
- **Steam Cloud:** the save (12) is one JSON file per Steam user, `<userData>/save/<steamid64>/game.json` (`%APPDATA%\trivia`, `~/.config/trivia`; D-72, plan 87); without Steam `save/local/game.json`, S3's `save/game.json` migrated there at start. Steam Auto-Cloud syncs it with no code: subdirectory `trivia/save/{64BitSteamID}`, non-recursive, pattern `game.json` (the `.tmp`, `backup/`, `local/` and other users' folders stay local).
  - Auto-Cloud values for SW-7 (plan 87; entered in Steamworks → Steam Cloud by the gamemaster):
    - Quota: 1 file, 20 MB (envelope ≤ 10 MB, D-72).
    - Root path: root `WinAppDataRoaming`, subdirectory `trivia/save/{64BitSteamID}`, pattern `game.json`, OS all, recursive off.
    - Root override: original `WinAppDataRoaming`, OS Linux, new root `LinuxXdgConfigHome` (`~/.config`), path unchanged; if Steamworks doesn't list it: `LinuxHome` with `.config/` prepended. Check Valve's current list on entry.
    - Deck: Linux build → the override; Windows build via Proton (D-92) → Windows path inside the prefix, no override.
  - Expected cloud listing: only `game.json`. If Steam picks up `game.json.tmp` mid-write: rename the temp outside the pattern (small `save.mjs` change), no Cloud API.
  - Conflict (both machines changed offline): Steam's own dialog at launch; the picked side wins whole; no code.
  - Family Sharing borrower: own SteamID → own folder and cloud slot.
  - Dev: `steam_appid.txt` / `TRIVIA_STEAM_APPID` as SW-8 left it (480 until SW-7).
- **Overlay:** Windows only (D-92): `addElectronSteamOverlay` on win32 while Steam is up; Linux without overlay (the native GL window froze the game on XWayland); the Deck runs the Windows build via Proton (SW-12). No pause on overlay open.
- **Achievements:** a few that fit the game (first victory, a win without jokers, a win on Experto, every broad category answered, reaching level 12 in each preset). No grind achievements.
- **On-screen keyboard:** `ShowFloatingGamepadTextInput` for the player name in Big Picture / on the Deck (14, Deck Verified): A on the name field opens it at the field; elsewhere and without Steam the letter picker (plan 46).
- **Glyphs:** Steam Input's `GetInputTypeForHandle` picks PlayStation or Xbox glyphs under Steam (14); without Steam `Gamepad.id`.
- **Language:** a fresh save preselects Steam's language (`GetCurrentGameLanguage`: the game's language in Steam, else the client's) through `guessTag()` in `lib/engine.ts` (`latam` → es, `spanish` → es-ES, `english` → en, `german` → de; unknown → `navigator.language`); the first-start screen still asks (I18N-2, D-86).
- **Rich presence:** «Nivel 7 de 12» while a level is on screen (`#Level`, values `level`, `levels`), cleared otherwise and on quit; Steam shows only uploaded tokens: `app/desktop/steam-presence.vdf` (latam, spanish, english, german; from `screen.level.kicker` + `screen.level.of`), uploaded by the gamemaster in Steamworks.
- **Remote Play Together:** enabled in Steamworks once multi-controller input works (IN-6).
- **No DRM:** the game runs without Steam running (offline living room). Steam binding calls are optional; the game works without them.

## Platforms and display
- **Windows** (x64) and **Linux** (x64) native builds; the **Deck** runs the Linux build. macOS later (needs a $99/year developer account and notarization).
- **Resolutions:** 720p to 4K. The size unit `--u` scales with the width (D-29), so a 16:10 screen (Deck, 1280×800) has more height. Check every screen at 1280×800 and at 1280×720 (smallest). Valve's Deck legibility guideline is text ≥ 9 px at 1280×800.
- **Windows specifics:** set explicit MIME types if any local serving remains; use atomic save writes with a retry (antivirus locks).
- **Media size:** the pool's media is ~2.4 GB for 1102 files (2026-10-12). Resize to at most 3840 px wide (4K, D-48), re-encode to WebP/AVIF, and transcode audio to Opus. Target: under 1 MB per image.

## Builds and depots
Local builds since S3 (SW-5, D-73); the release check (SW-6) and Steam uploads (SW-10) since S5. No GitHub Actions: CI is local (pm decision 14). One command on the gamemaster's Linux machine builds both platforms; the artefacts are plain folders, so Steam (S5) can install them as they are.
- **Command:** `trivia-desktop-build` (dev shell) = `qgen validate`, `npm run build -w app/client`, `stage-media.mjs`, `electron-builder --x64 --linux tar.gz --win zip`; `--dir` adds the `dir` target (`release/{win,linux}-unpacked/`, the OS depots; launcher via `after-pack.mjs` too), `trivia-steam stage` checks OS depot (without `resources/media`) + content depot (`build/media/`) = the archives. Outside Nix: `npm ci --prefix app/desktop`, then `npm run dist --prefix app/desktop` (no `qgen validate`). First build downloads the Electron zips into `~/.cache/electron`; later builds run offline.
- **Targets:** `app/desktop/release/Trivia-<version>-win-x64.zip` (files at the zip root; `Trivia.exe`: unsigned, Electron's icon until pm decision 87 gives a game icon) and `Trivia-<version>-linux-x64.tar.gz` (folder `Trivia-<version>-linux-x64/`; `./trivia` = launcher with `--no-sandbox`, binary `trivia-bin`; the Deck runs this one). No installer, no AppImage. ~2.5 GB each today.
- **Layout:** `resources/app.asar` (`package.json`, `main.mjs`, `resolve.mjs`, `save.mjs`, `preload.cjs`), `resources/client/` (client `dist/`), `resources/data/` (`app/data/`), `resources/media/` (only the pool's media and backgrounds, from the cache via `app/desktop/build/media/`; outside the asar for the S5 content depot); `LICENSE.electron.txt`, `LICENSES.chromium.html` at the root. `CREDITS.md` (PUB-5) in `resources/client/` and at the root (`extraFiles` from `../client/dist/CREDITS.md`).
- **Config:** `app/desktop/electron-builder.yml`, `after-pack.mjs` (Linux launcher), own `package-lock.json` (`electron`, `electron-builder`; not a root workspace).
- **Exe metadata (B-11, task 683):** `win.signExecutable: false`: electron-builder 26 edits `Trivia.exe`'s resources in pure JS (`resedit`, no wine): `ProductName`/`FileDescription` = `productName`, `CompanyName` + copyright = `package.json` `author`, `FileVersion`/`ProductVersion` = `version`. Icon: `win.icon`, pending (pm decision 87). `ProductName` follows `productName` («Trivia»); «Living Room Trivia» once PUB-7 passes (artifact names and paths change with it).
- **Signing:** not required by Steam; the exe stays unsigned (SmartScreen only warns for downloads outside Steam).
- **Checked (task 330, 2026-10-12):** unpacked Linux build, no network (`unshare -rn`), no Nix env (`env -i` + an FHS runtime), no Python: new player → level 5 with image, audio (playing) and video (playing) questions, no missing-media notice; «Salir del juego» → restart: player resumes, no answered question comes back; save at `~/.config/trivia/save/game.json`; nothing written outside `HOME`. Windows: zip content listed only.
- **Upload:** `trivia-steam upload --branch beta` (dev shell, `authoring/steam/steam.py`, D-93): gates (clean tree; tag `v<version>` on HEAD, never created by the command; `steam.json` IDs) → `trivia-release-check` (or `--checked`: this commit's passing `release-check.json` on a clean tree) → `trivia-steam stage` → VDFs → `steamcmd +login $TRIVIA_STEAM_ACCOUNT +run_app_build <app vdf> +quit`; prints the BuildID. `--preview` (Valve's `Preview 1`, no tag needed), `--dry-run` (no SteamCMD, no tag, placeholder IDs 480/481–483 while `steam.json` is null). Desc `<tag> <sha>` plus `skipped: <steps>`.
- **Version (pm decisions 91, 92; plan 91):** one source, `app/desktop/package.json` `version` (semver); `flake.nix` app version, client (`__APP_VERSION__`, Vite `define`), artifact names, exe `FileVersion` and `steam.py` `version()` read it. Tag `v<version>` per release; build Desc `<tag> <sha>`.
  - Bump: edit `package.json` `version`, commit, `git tag v<version>`.
  - Id continuity: `qgen validate` fails when an id of the newest `v*` tag's `app/data/pool*.json` is missing from `authoring/data/questions.json` (drop = status change, never deletion; no tag → "skipped").
  - Semver: patch `x.y.Z` = content-only or bug fix; minor = new feature or save version bump; `1.0.0` = launch.
  - Pool: `qgen export` writes `"hash"` (first 8 hex of sha256 over the exported questions) into every `pool*.json`; Credits header shows «Versión 0.1.0 · preguntas fa9887b5» (`lib/build.ts` `buildInfo()`; hash of the current game's question locale).
- **Depots (pm decision 84):** `windows` (`release/win-unpacked/` without `resources/media`), `linux` (`release/linux-unpacked/` likewise), `content` (`build/media/` → `resources/media`, shared); one install folder. Language or region packs can be separate depots or DLC later (15c).
- **Credentials:** a dedicated Steam build account, by hand from the author's machine (pm decision 14); account via `TRIVIA_STEAM_ACCOUNT` or a prompt, password and Steam Guard typed into SteamCMD only, cached in its home `~/.local/share/trivia/steamcmd`. Never commit credentials (AGENTS.md).
- **Branches:** `SetLive` is always `beta` (password-protected, set in Steamworks; the family plays it first); `--branch default` or any other is refused. `default` (public) stays empty until S6 and is only set in the Steamworks web UI.
- **Gitignored:** `work/steam/<tag>/` (`release-check.{md,json}`, `logs/`, `vdf/`, `steamcmd.log`, SteamCMD's `output/`); in git only `authoring/steam/` (`steam.json` IDs, templates, scripts; no secrets).
- **CI (SW-6, pm decision 14):** local, no GitHub Actions.
  - Per commit: `npm run check`, `npm test`, `npm run build`, `qgen validate`, the task's own check (AGENTS.md).
  - Before every Steam upload: `trivia-release-check` (dev shell, `authoring/steam/release_check.py`, ~15 min); steps `tag` (first: clean tree, HEAD tagged `v<version>`, pm decision 91; never tags), `checks` (per-commit checks), `licenses` (`trivia-media licenses --status approved`), `quality` (`qgen report --qc` release bar ✓ for the last two batches, pm decision 15), `nix` (`nix build .#app`), `desktop` (`trivia-desktop-build --dir`, stage-media's missing-file check, `trivia-steam stage`), `credits` (`credits_check.mjs` on `linux-unpacked` and `win-unpacked`: packaged files ↔ `credits.json` both ways, plan 92), `smoke` (`smoke.mjs` on `linux-unpacked`), `media-budget` (always skipped until masterplan 10 part 6, task 260), `manual` (clean Windows, Deck, sound, timed-competitive red frame; y/n/note or `--manual <file>`).
  - Every ✗ fails (exit 1); `--skip <step>` for a known-broken step, listed in the report and the build Desc. `trivia-steam upload --preview`/`--dry-run` add `--skip tag`.
  - Kind (plan 92): previous tag = newest `v*` reachable from HEAD, not HEAD's own; `content-only` patch if `git diff --name-only <prev>..HEAD` touches nothing shipped (`app/`, `flake.nix`, `flake.lock`, root `package*.json`) outside `app/data/`, else (or no earlier tag) `full`. Save version: `SAVE_VERSION` (`app/client/src/engine/state.ts`) at HEAD vs previous tag. JSON keys `kind`, `previous_tag`, `save_version`.
  - Report `work/steam/<tag-or-sha>/release-check.{md,json}` (header: version, pool hash, previous tag, kind, save version change; commit, clean tree, result, skips) + `logs/<step>.log`; the JSON is what `trivia-steam upload --checked` reuses.

## Local build start test
The gamemaster's check that the local builds start and play offline on machines without the dev setup (SW-5; pm plan 56 task 3). Plan 48 merges it into the S3 platform test. Fill one table per machine, with date and build commit.
- **Artefacts:** `trivia-desktop-build` → `app/desktop/release/Trivia-<version>-win-x64.zip`, `Trivia-<version>-linux-x64.tar.gz`; or copy those two files over (USB stick, ~2.5 GB each).
- **Machines:** Windows x64 without Node/Python; Linux x64 without Nix (e.g. Ubuntu 24.04).
- **Result:** ✓, ✗ or n/a; a ✗ gets a note on how to reproduce.

### Windows x64
Date: · Build commit:

| check | result | note |
|---|---|---|
| Network off before unpacking | | |
| Unpack the zip, start `Trivia.exe` (SmartScreen «More info → Run anyway» expected: unsigned) | | |
| No console window | | |
| Starts fullscreen; F11 toggles | | |
| Keyboard-only game to level 3, with an image, an audio and a video question; sound plays | | |
| «Salir del juego», restart: the player is still there | | |
| Save at `%APPDATA%\trivia\save\<steamid64 or local>\game.json` | | |
| `CREDITS.md` in the folder | | |

### Linux x64 (no Nix)
Date: · Build commit:

| check | result | note |
|---|---|---|
| Network off before unpacking | | |
| `tar xzf`, `cd Trivia-<version>-linux-x64`, `./trivia` | | |
| Starts fullscreen; F11 toggles | | |
| Keyboard-only game to level 3, with an image, an audio and a video question; sound plays | | |
| «Salir del juego», restart: the player is still there | | |
| Save at `~/.config/trivia/save/<steamid64 or local>/game.json` | | |
| `CREDITS.md` in the folder | | |

## Steam Cloud test
The gamemaster's check that Auto-Cloud syncs one save per Steam user between machines (plan 87 part 4). Fill the table once, with date and build commit; agents don't run it.
- **Needs:** the real App ID (masterplan 10 part 1, `task 253`), the Auto-Cloud values above entered in Steamworks (part 2, `task 254`), a packaged Steam build (`task 650` or part 7's upload to `beta`).
- **Machines:** A and B, one Windows and one Linux or the Deck.
- **Result:** ✓, ✗ or n/a; a ✗ gets a note on how to reproduce.

Date: · Build commit:

| check | result | note |
|---|---|---|
| A plays (new player, a few questions) → quit → B shows the same players and seen counts | | |
| Two Steam accounts on one OS login → separate saves (`save/<id>/` each) | | |
| Family Sharing borrower → own save | | |
| First Steam start with an S3 or `local/` save → «Usar el progreso de este equipo» offered | | |
| Second machine with a cloud save → no question | | |
| Offline on both, play on both, then online → Steam's conflict dialog; the picked side wins whole | | |
| Steam's cloud file list (game properties, or `store.steampowered.com/account/remotestorage`) shows only `game.json`, never `.tmp`, `backup/`, `local/` | | |

## Steam Deck Verified
Requirements to plan for: full controller support with correct glyphs (IN), legible text at 800p, the on-screen keyboard for text entry, no launcher, working default settings, no warnings on start. Test on a real Deck before applying.

## Tasks
- [x] SW-1 Decide the shell (OQ-29); record it in `decisions.md`. *Done 2026-10-12: Electron (D-63).*
- [x] SW-2 Electron shell skeleton: window, fullscreen toggle, loads `app/client/dist/`, preload bridge; pick the Steam binding (steamworks-ffi-node or steamworks.js: maintenance, overlay, Electron version). *Done 2026-10-12 (pm plan 54, D-71): `app/desktop/` (`main.mjs`, `resolve.mjs`, `preload.cjs`, `package.json`), `app/client/src/lib/desktop.ts`, `lib/engine.ts` (`MemoryStore`), `Overlay.svelte`, `flake.nix` (`trivia-desktop`, `pkgs.electron` 43); whole game without Python checked over CDP under Xvfb (task 318: level 12, every joker, undo, abandon, media, samples, clean console). Gamemaster play test: plays fine (pm decision 29, 2026-10-13). Binding: steamworks-ffi-node (pm decision 28, D-63; task 353).*
- [x] SW-3 `FileStore` for the save in the user data folder (atomic writes, Windows retry). *Done 2026-10-12 (pm plan 55, D-72): `app/desktop/save.mjs`, `main.mjs` (userData path, `save:*` IPC, write queue, quit wait, `--import-save`), `preload.cjs`, `lib/desktop.ts`, `lib/store.ts` (`FileStore`, shared `WriteQueue`), `lib/engine.ts` (store choice, notice, `saveError()`), `engine/save.ts` (`SaveNewerError`), start-screen notice, «Salir» flush, `es` catalog; kill loop (60 × `SIGKILL` of main mid-write, 1–5 MB documents): `game.json` always one of the documents sent, stale `.tmp` dropped, no backup.*
- [x] SW-4 Screen check at 1280×800 and 1280×720; fixes. *Done 2026-10-12 (pm plan 46): letter picker for a pad (`LetterPicker.svelte`); throw-away Playwright walk (pm decision 6) of every screen and state at 1280×800, 1280×720, 1920×1080, 3840×2160, keyboard prompts and Xbox glyphs (faked standard pad), longest pool content, 9 names of 30 characters, 11 levels short, error box; computed font sizes < 9 px reported. Fixes: credit line 0.8 → 0.9 u; «medio no disponible» chip `rem` → `--u`; pad glyph labels (LB/RB/LT/RT) 10.5 → 13.5 viewBox units (7 → 9.2 px at 1280); supply report in four columns when more than 4 levels are short, Choice gaps 0.8 u while it shows (the title left the screen at 720p and 1080p). 1080p unchanged elsewhere (ImageMagick `compare`). Credit line and «Respuesta final» stay in the bottom margin (pm decision 52). Real Deck check: plan 48.*
- [ ] SW-5 Local Windows and Linux builds with electron-builder; offline start test on a clean Windows machine. *Plan: pm plan 56 (Windows zip + Linux tar.gz, media staged from the pool, `trivia-desktop-build`, start-test checklist).*
- [ ] SW-6 Local CI: per-commit checks (AGENTS.md) and a release check before every Steam upload ("Builds and depots"); no GitHub Actions. *Moved to S5 (pm decision 14, D-73); per-commit checks in AGENTS.md since 2026-10-12; release check: `trivia-release-check` (2026-10-13, task 679); upload: `trivia-steam upload --branch beta` (2026-10-13, task 680).*
- [ ] SW-7 Steamworks app: App ID, depots, launch options, supported languages, Cloud path.
- [x] SW-8 Steam binding steamworks-ffi-node (D-63): overlay, achievements, on-screen keyboard, language; the game runs without Steam. *Done 2026-10-13 (pm plan 85): bridge `window.trivia.steam` (`main.mjs` init/callbacks/shutdown, `preload.cjs`, `lib/desktop.ts` `SteamBridge`; App ID 480 until SW-7, `TRIVIA_STEAM_APPID`; SDK libs gitignored in `app/desktop/steamworks_sdk/` or the flake's SDK 1.62, decision 69), Steam language → `guessTag()`, overlay Windows only (D-92), floating keyboard for the name, `GetInputTypeForHandle` glyphs, rich presence (`steam-presence.vdf`); `unlock()`/`steamId()` pass-through for SW-11 and Cloud. Packaging: task 650. Gamemaster check under Steam: pm task 652's decision.*
- [ ] SW-9 Media bundle: resize, re-encode, size budget; checked by `media.py`.
- [ ] SW-10 SteamCMD upload script; build account; beta branch. *Plan: pm plan 89; `trivia-release-check` and `trivia-steam upload --branch beta` (depots windows/linux/content) since 2026-10-13 (tasks 679, 680); first upload: tasks 681, 682.*
- [ ] SW-11 Achievements: list, icons, Steamworks setup.
- [ ] SW-12 Steam Deck test and the Deck Verified review. *Plan: pm plan 90 (real-Deck checklist on the Steam-installed `beta`, Valve's criteria, Cloud, suspend/resume; review request or S6 note).*
- [ ] SW-13 Remote Play Together (after IN-6).
- [ ] SW-14 macOS build (later; developer account and notarization).
