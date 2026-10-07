# 18 — Steam Integration and Packaging

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). Turns the built client into an installable desktop game with Steam features, and gets builds onto Steam. Depends on the client engine ([12](12-client-engine.md)): once the game runs without Python, the shell only has to show the client and save one file.

## Desktop shell (OQ-29)
| Option | For | Against |
|---|---|---|
| **Electron + steamworks.js** (recommended) | The most common way to ship a web game on Steam. The same Chromium on Windows, Linux and the Deck, so fonts, audio, `backdrop-filter` and animations behave as on the TV today. steamworks.js covers the overlay, achievements, Cloud and the on-screen keyboard. | ~150 MB extra install size; Node in the build toolchain (already there for Vite). |
| Tauri | Small installs, Rust core. | WebView2 on Windows, WebKitGTK on Linux/Deck: two engines to test; WebKitGTK is weaker at media and effects; the Steam overlay is unreliable over a system webview. |
| Browser + local server (PyInstaller) | Closest to today. | Not a "real" game window, no overlay, two runtimes, antivirus false positives on PyInstaller builds. |

The shell's own code stays tiny: create a fullscreen window, load `app/client/dist/`, expose `loadSave`/`writeSave` and the Steam calls to the page through a preload bridge (no Node in the page itself).

## Steam features
- **Steam Cloud:** the save (12) is one JSON file in the user data folder. Steam Auto-Cloud syncs it with no code; only the file path is configured in Steamworks.
- **Overlay:** steamworks.js needs a call to enable it in Electron; test on Windows and the Deck.
- **Achievements:** a few that fit the game (first victory, a win without jokers, a win on Experto, every broad category answered, reaching level 12 in each preset). No grind achievements.
- **On-screen keyboard:** `ShowFloatingGamepadTextInput` for the player name on the Deck / Big Picture (IN, Deck Verified).
- **Language:** the default UI and question language come from the Steam client language (I18N-2).
- **Rich presence** (optional): «Nivel 7 de 12».
- **Remote Play Together:** enabled in Steamworks once multi-controller input works (IN-6).
- **No DRM:** the game runs without Steam running (offline living room, family copy). steamworks.js calls are optional; the game works without them.

## Platforms and display
- **Windows** (x64) and **Linux** (x64) native builds; the **Deck** runs the Linux build. macOS later (needs a $99/year developer account and notarization).
- **Resolutions:** 720p to 4K. The size unit `--u` scales with the width (D-29), so a 16:10 screen (Deck, 1280×800) has more height. Check every screen at 1280×800 and at 1280×720 (smallest). Valve's Deck legibility guideline is text ≥ 9 px at 1280×800.
- **Windows specifics:** set explicit MIME types if any local serving remains; use atomic save writes with a retry (antivirus locks).
- **Media size:** the cache is ~720 MB for ~300 files. Resize to at most 2560 px wide (1440p; 4K upscales well behind glass panels), re-encode to WebP/AVIF, and transcode audio to Opus. Target: under 1 MB per image.

## Builds and depots
- **electron-builder** builds both platforms in GitHub Actions (Windows and Linux runners). The pool export (PORT-6), the media bundle (SW-9) and the credits (PUB-5) are build steps.
- **Upload with SteamCMD** (`run_app_build` with a VDF per depot). Depots: Windows, Linux, shared content (pool and media). Language or region packs can be separate depots or DLC later (15c).
- **Credentials:** a dedicated Steam build account; its login in GitHub Actions secrets. Steam Guard needs a one-time setup. Never commit credentials (AGENTS.md). Alternative: upload from the author's machine by hand.
- **Branches:** `default` (public) and a password-protected `beta`. The family plays the beta first.

## Steam Deck Verified
Requirements to plan for: full controller support with correct glyphs (IN), legible text at 800p, the on-screen keyboard for text entry, no launcher, working default settings, no warnings on start. Test on a real Deck before applying.

## Tasks
- [ ] SW-1 Decide the shell (OQ-29); record it in `decisions.md`.
- [ ] SW-2 Shell skeleton: window, fullscreen toggle, loads `app/client/dist/`, preload bridge.
- [ ] SW-3 `FileStore` for the save in the user data folder (atomic writes, Windows retry).
- [ ] SW-4 Screen check at 1280×800 and 1280×720; fixes.
- [ ] SW-5 Local Windows and Linux builds with electron-builder; offline start test on a clean Windows machine.
- [ ] SW-6 CI build in GitHub Actions for both platforms.
- [ ] SW-7 Steamworks app: App ID, depots, launch options, supported languages, Cloud path.
- [ ] SW-8 steamworks.js: overlay, achievements, on-screen keyboard, language; the game runs without Steam.
- [ ] SW-9 Media bundle: resize, re-encode, size budget; checked by `media.py`.
- [ ] SW-10 SteamCMD upload script; build account; beta branch.
- [ ] SW-11 Achievements: list, icons, Steamworks setup.
- [ ] SW-12 Steam Deck test and the Deck Verified review.
- [ ] SW-13 Remote Play Together (after IN-6).
- [ ] SW-14 macOS build (later; developer account and notarization).
