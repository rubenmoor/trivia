# 18 — Steam Integration and Packaging

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). Turns the built client into an installable desktop game with Steam features, and gets builds onto Steam. Depends on the client engine ([12](12-client-engine.md)): once the game runs without Python, the shell only has to show the client and save one file.

## Desktop shell (OQ-29)
Decided: **Electron** (D-63, pm decision 12; facts checked 2026-10-11, sources there). Steam binding: steamworks-ffi-node or steamworks.js, picked in SW-2.

| Option | For | Against |
|---|---|---|
| **Electron** (chosen) | The most common way to ship a web game on Steam. The same Chromium on Windows, Linux and the Deck, so fonts, audio, `backdrop-filter` and animations behave as on the TV today. Overlay works on Windows. A LAN server for phone buzzers (OQ-37) is plain Node `http` in the main process, in TS. | ~125–160 MB download (v44 zip: 158 MB Win, 123 MB Linux). Steam binding: steamworks.js is stale (last release 2024-08; open overlay issues, incl. no overlay on Linux); steamworks-ffi-node is active but young. Overlay on native Linux/Deck is shaky; fallback: Windows build via Proton. |
| Tauri v2 | Small installs, Rust core. | WebView2 on Windows, WebKitGTK on Linux/Deck: two engines to test; WebKitGTK has open `backdrop-filter` and media bugs; no Steam overlay over a system webview (Windows-only community workaround). Phone buzzer server in Rust. |
| Browser + local server (PyInstaller) | Closest to today; already has a LAN server for phone buzzers. | Not a "real" game window, no overlay, two runtimes, antivirus false positives on PyInstaller builds; plans 19/20 remove Python. |

The shell's own code stays tiny: create a fullscreen window, load `app/client/dist/`, expose `loadSave`/`writeSave` and the Steam calls to the page through a preload bridge (no Node in the page itself).
- Window option `webPreferences.autoplayPolicy: "no-user-gesture-required"`: a gamepad press isn't user activation in Chromium (HTML spec: only key, mouse, touch), so a pad-only start would stay silent (plan 45, IN-4).

## Steam features
- **Steam Cloud:** the save (12) is one JSON file, `<userData>/save/game.json` (`%APPDATA%\trivia`, `~/.config/trivia`; D-72). Steam Auto-Cloud syncs it with no code: root `save/`, non-recursive, pattern `game.json` (the `.tmp` and `backup/` stay local).
- **Overlay:** the Steam binding needs a call to enable it in Electron; test on Windows and the Deck (fallback on the Deck: the Windows build via Proton).
- **Achievements:** a few that fit the game (first victory, a win without jokers, a win on Experto, every broad category answered, reaching level 12 in each preset). No grind achievements.
- **On-screen keyboard:** `ShowFloatingGamepadTextInput` for the player name on the Deck / Big Picture (IN, Deck Verified).
- **Language:** the default UI and question language come from the Steam client language (I18N-2).
- **Rich presence** (optional): «Nivel 7 de 12».
- **Remote Play Together:** enabled in Steamworks once multi-controller input works (IN-6).
- **No DRM:** the game runs without Steam running (offline living room). Steam binding calls are optional; the game works without them.

## Platforms and display
- **Windows** (x64) and **Linux** (x64) native builds; the **Deck** runs the Linux build. macOS later (needs a $99/year developer account and notarization).
- **Resolutions:** 720p to 4K. The size unit `--u` scales with the width (D-29), so a 16:10 screen (Deck, 1280×800) has more height. Check every screen at 1280×800 and at 1280×720 (smallest). Valve's Deck legibility guideline is text ≥ 9 px at 1280×800.
- **Windows specifics:** set explicit MIME types if any local serving remains; use atomic save writes with a retry (antivirus locks).
- **Media size:** the cache is ~720 MB for ~300 files. Resize to at most 3840 px wide (4K, D-48), re-encode to WebP/AVIF, and transcode audio to Opus. Target: under 1 MB per image.

## Builds and depots
- **electron-builder** builds both platforms in GitHub Actions (Windows and Linux runners). The pool export (PORT-6), the media bundle (SW-9) and the credits (PUB-5) are build steps.
- **Upload with SteamCMD** (`run_app_build` with a VDF per depot). Depots: Windows, Linux, shared content (pool and media). Language or region packs can be separate depots or DLC later (15c).
- **Credentials:** a dedicated Steam build account; its login in GitHub Actions secrets. Steam Guard needs a one-time setup. Never commit credentials (AGENTS.md). Alternative: upload from the author's machine by hand.
- **Branches:** `default` (public) and a password-protected `beta`. The family plays the beta first.

## Steam Deck Verified
Requirements to plan for: full controller support with correct glyphs (IN), legible text at 800p, the on-screen keyboard for text entry, no launcher, working default settings, no warnings on start. Test on a real Deck before applying.

## Tasks
- [x] SW-1 Decide the shell (OQ-29); record it in `decisions.md`. *Done 2026-10-12: Electron (D-63).*
- [x] SW-2 Electron shell skeleton: window, fullscreen toggle, loads `app/client/dist/`, preload bridge; pick the Steam binding (steamworks-ffi-node or steamworks.js: maintenance, overlay, Electron version). *Done 2026-10-12 (pm plan 54, D-71): `app/desktop/` (`main.mjs`, `resolve.mjs`, `preload.cjs`, `package.json`), `app/client/src/lib/desktop.ts`, `lib/engine.ts` (`MemoryStore`), `Overlay.svelte`, `flake.nix` (`trivia-desktop`, `pkgs.electron` 43); whole game without Python checked over CDP under Xvfb (task 318: level 12, every joker, undo, abandon, media, samples, clean console). Pending: gamemaster play test (pm decision 29, task 355); binding answer (pm decision 28, recorded by task 353).*
- [x] SW-3 `FileStore` for the save in the user data folder (atomic writes, Windows retry). *Done 2026-10-12 (pm plan 55, D-72): `app/desktop/save.mjs`, `main.mjs` (userData path, `save:*` IPC, write queue, quit wait, `--import-save`), `preload.cjs`, `lib/desktop.ts`, `lib/store.ts` (`FileStore`, shared `WriteQueue`), `lib/engine.ts` (store choice, notice, `saveError()`), `engine/save.ts` (`SaveNewerError`), start-screen notice, «Salir» flush, `es` catalog; kill loop (60 × `SIGKILL` of main mid-write, 1–5 MB documents): `game.json` always one of the documents sent, stale `.tmp` dropped, no backup.*
- [ ] SW-4 Screen check at 1280×800 and 1280×720; fixes. *Plan: pm plan 46 (also the letter picker for player names with a pad).*
- [ ] SW-5 Local Windows and Linux builds with electron-builder; offline start test on a clean Windows machine. *Plan: pm plan 56 (Windows zip + Linux tar.gz, media staged from the pool, `trivia-desktop-build`, start-test checklist).*
- [ ] SW-6 CI build in GitHub Actions for both platforms. *S3 or S5, with or without media: pm decision 14; plan 56 task 5.*
- [ ] SW-7 Steamworks app: App ID, depots, launch options, supported languages, Cloud path.
- [ ] SW-8 Steam binding (SW-2): overlay, achievements, on-screen keyboard, language; the game runs without Steam.
- [ ] SW-9 Media bundle: resize, re-encode, size budget; checked by `media.py`.
- [ ] SW-10 SteamCMD upload script; build account; beta branch.
- [ ] SW-11 Achievements: list, icons, Steamworks setup.
- [ ] SW-12 Steam Deck test and the Deck Verified review.
- [ ] SW-13 Remote Play Together (after IN-6).
- [ ] SW-14 macOS build (later; developer account and notarization).
