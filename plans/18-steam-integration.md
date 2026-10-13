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
- **Steam Cloud:** the save (12) is one JSON file, `<userData>/save/game.json` (`%APPDATA%\trivia`, `~/.config/trivia`; D-72). Steam Auto-Cloud syncs it with no code: root `save/`, non-recursive, pattern `game.json` (the `.tmp` and `backup/` stay local).
- **Overlay:** the Steam binding needs a call to enable it in Electron; test on Windows and the Deck (fallback on the Deck: the Windows build via Proton).
- **Achievements:** a few that fit the game (first victory, a win without jokers, a win on Experto, every broad category answered, reaching level 12 in each preset). No grind achievements.
- **On-screen keyboard:** `ShowFloatingGamepadTextInput` for the player name on the Deck / Big Picture (IN, Deck Verified).
- **Language:** the default UI and question language come from the Steam client language (I18N-2, D-86): wire it into `guessTag()` in `lib/engine.ts`.
- **Rich presence** (optional): «Nivel 7 de 12».
- **Remote Play Together:** enabled in Steamworks once multi-controller input works (IN-6).
- **No DRM:** the game runs without Steam running (offline living room). Steam binding calls are optional; the game works without them.

## Platforms and display
- **Windows** (x64) and **Linux** (x64) native builds; the **Deck** runs the Linux build. macOS later (needs a $99/year developer account and notarization).
- **Resolutions:** 720p to 4K. The size unit `--u` scales with the width (D-29), so a 16:10 screen (Deck, 1280×800) has more height. Check every screen at 1280×800 and at 1280×720 (smallest). Valve's Deck legibility guideline is text ≥ 9 px at 1280×800.
- **Windows specifics:** set explicit MIME types if any local serving remains; use atomic save writes with a retry (antivirus locks).
- **Media size:** the pool's media is ~2.4 GB for 1102 files (2026-10-12). Resize to at most 3840 px wide (4K, D-48), re-encode to WebP/AVIF, and transcode audio to Opus. Target: under 1 MB per image.

## Builds and depots
Local builds since S3 (SW-5, D-73); the release check (SW-6) and Steam uploads come in S5. No GitHub Actions: CI is local (pm decision 14). One command on the gamemaster's Linux machine builds both platforms; the artefacts are plain folders, so Steam (S5) can install them as they are.
- **Command:** `trivia-desktop-build` (dev shell) = `qgen validate`, `npm run build -w app/client`, `stage-media.mjs`, `electron-builder --x64 --linux tar.gz --win zip`. Outside Nix: `npm ci --prefix app/desktop`, then `npm run dist --prefix app/desktop` (no `qgen validate`). First build downloads the Electron zips into `~/.cache/electron`; later builds run offline.
- **Targets:** `app/desktop/release/Trivia-<version>-win-x64.zip` (files at the zip root; `Trivia.exe`, unsigned, Electron's icon until S5) and `Trivia-<version>-linux-x64.tar.gz` (folder `Trivia-<version>-linux-x64/`; `./trivia` = launcher with `--no-sandbox`, binary `trivia-bin`; the Deck runs this one). No installer, no AppImage. ~2.5 GB each today.
- **Layout:** `resources/app.asar` (`package.json`, `main.mjs`, `resolve.mjs`, `save.mjs`, `preload.cjs`), `resources/client/` (client `dist/`), `resources/data/` (`app/data/`), `resources/media/` (only the pool's media and backgrounds, from the cache via `app/desktop/build/media/`; outside the asar for the S5 content depot); `LICENSE.electron.txt`, `LICENSES.chromium.html` at the root. `CREDITS.md` (PUB-5) in `resources/client/` and at the root (`extraFiles` from `../client/dist/CREDITS.md`).
- **Config:** `app/desktop/electron-builder.yml`, `after-pack.mjs` (Linux launcher), own `package-lock.json` (`electron`, `electron-builder`; not a root workspace).
- **Checked (task 330, 2026-10-12):** unpacked Linux build, no network (`unshare -rn`), no Nix env (`env -i` + an FHS runtime), no Python: new player → level 5 with image, audio (playing) and video (playing) questions, no missing-media notice; «Salir del juego» → restart: player resumes, no answered question comes back; save at `~/.config/trivia/save/game.json`; nothing written outside `HOME`. Windows: zip content listed only.
- Later (S5): **upload with SteamCMD** (`run_app_build` with a VDF per depot). Depots: Windows, Linux, shared content (pool and media). Language or region packs can be separate depots or DLC later (15c).
- Later (S5): **credentials:** a dedicated Steam build account; upload by hand with SteamCMD from the author's machine (pm decision 14). Steam Guard needs a one-time setup. Never commit credentials (AGENTS.md).
- Later (S5): **branches:** `default` (public) and a password-protected `beta`. The family plays the beta first.
- **CI (SW-6, pm decision 14):** local, no GitHub Actions.
  - Per commit: `npm run check`, `npm test`, `npm run build`, `qgen validate`, the task's own check (AGENTS.md).
  - Later (S5): release check (e.g. `trivia-release-check`) before every Steam upload: the per-commit checks, `trivia-media licenses`, the release quality bar (pm decision 15), `nix build .#app`, both packaged builds, a scripted smoke game in the packaged Linux build (CDP), and a manual checklist (start test on clean Windows and the Deck, sound, the timed-competitive red frame).

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
| Save at `%APPDATA%\trivia\save\game.json` | | |
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
| Save at `~/.config/trivia/save/game.json` | | |
| `CREDITS.md` in the folder | | |

## Steam Deck Verified
Requirements to plan for: full controller support with correct glyphs (IN), legible text at 800p, the on-screen keyboard for text entry, no launcher, working default settings, no warnings on start. Test on a real Deck before applying.

## Tasks
- [x] SW-1 Decide the shell (OQ-29); record it in `decisions.md`. *Done 2026-10-12: Electron (D-63).*
- [x] SW-2 Electron shell skeleton: window, fullscreen toggle, loads `app/client/dist/`, preload bridge; pick the Steam binding (steamworks-ffi-node or steamworks.js: maintenance, overlay, Electron version). *Done 2026-10-12 (pm plan 54, D-71): `app/desktop/` (`main.mjs`, `resolve.mjs`, `preload.cjs`, `package.json`), `app/client/src/lib/desktop.ts`, `lib/engine.ts` (`MemoryStore`), `Overlay.svelte`, `flake.nix` (`trivia-desktop`, `pkgs.electron` 43); whole game without Python checked over CDP under Xvfb (task 318: level 12, every joker, undo, abandon, media, samples, clean console). Pending: gamemaster play test (pm decision 29, task 355); binding: steamworks-ffi-node (pm decision 28, D-63; task 353).*
- [x] SW-3 `FileStore` for the save in the user data folder (atomic writes, Windows retry). *Done 2026-10-12 (pm plan 55, D-72): `app/desktop/save.mjs`, `main.mjs` (userData path, `save:*` IPC, write queue, quit wait, `--import-save`), `preload.cjs`, `lib/desktop.ts`, `lib/store.ts` (`FileStore`, shared `WriteQueue`), `lib/engine.ts` (store choice, notice, `saveError()`), `engine/save.ts` (`SaveNewerError`), start-screen notice, «Salir» flush, `es` catalog; kill loop (60 × `SIGKILL` of main mid-write, 1–5 MB documents): `game.json` always one of the documents sent, stale `.tmp` dropped, no backup.*
- [ ] SW-4 Screen check at 1280×800 and 1280×720; fixes. *Plan: pm plan 46 (also the letter picker for player names with a pad).*
- [ ] SW-5 Local Windows and Linux builds with electron-builder; offline start test on a clean Windows machine. *Plan: pm plan 56 (Windows zip + Linux tar.gz, media staged from the pool, `trivia-desktop-build`, start-test checklist).*
- [ ] SW-6 Local CI: per-commit checks (AGENTS.md) and a release check before every Steam upload ("Builds and depots"); no GitHub Actions. *Moved to S5 (pm decision 14, D-73); per-commit checks in AGENTS.md since 2026-10-12; release check: pm plan 10 part 7 (task 261).*
- [ ] SW-7 Steamworks app: App ID, depots, launch options, supported languages, Cloud path.
- [ ] SW-8 Steam binding steamworks-ffi-node (D-63): overlay, achievements, on-screen keyboard, language; the game runs without Steam.
- [ ] SW-9 Media bundle: resize, re-encode, size budget; checked by `media.py`.
- [ ] SW-10 SteamCMD upload script; build account; beta branch.
- [ ] SW-11 Achievements: list, icons, Steamworks setup.
- [ ] SW-12 Steam Deck test and the Deck Verified review.
- [ ] SW-13 Remote Play Together (after IN-6).
- [ ] SW-14 macOS build (later; developer account and notarization).
