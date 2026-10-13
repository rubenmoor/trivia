# 17a — Store page

**Status:** stub

Sub-plan of [17](17-publishing.md). Everything the developer pastes into Steamworks' store page admin for the beta (plan 88, PUB-8, LUI-6): texts per store language, AI disclosure, requirements, languages, controller flags, capsules and screenshots. Workers draft and render here; the developer approves through pm decisions and enters them.

## System requirements, languages, controller
Values for Steamworks → Edit Store Page → "Basic Info" (requirements, languages) and "Controller" (plan 88 task 3). Proposed 2026-10-13; the developer approves or fixes them through pm decision "Store requirements, languages and controller flags?". Field names are from memory (no web access at the task); recheck them at entry.

### Measured
- Depots from the local `trivia-desktop-build --dir` (0.1.0, 2026-10-13; part 6's media bundle not built yet, decision 82): `windows` 0.40 GB, `linux` 0.35 GB, `content` (media) 2.55 GB → installed 2.95 GB (Windows), 2.90 GB (Linux)
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

- Storage: placeholder until part 6's bundle (SW-9); then the installed size rounded up
- Ubuntu 22.04: Electron's own floor, not tested; replace with the distro of the first non-Nix start test
- macOS: none (no build)

### Supported languages
| language (Steam) | Interface | Full audio | Subtitles |
|---|---|---|---|
| English | ✓ | ✗ | ✓ |
| Spanish - Latin America | ✓ | ✗ | ✓ |
| Spanish - Spain | ✓ | ✗ | ✓ |
| German | ✓ | ✗ | ✓ |

- No spoken text in the game; "Subtitles" ✓ as the plan sets it (questions and media captions are text)
- English and German need their question pools (`pool.en.json`, `pool.de.json`, decision 80) before the beta goes public; until then only the interface is translated

### Controller
- **Xbox controllers:** Full controller support, if the developer's real-pad run passes (start → new player via the letter picker or Steam's floating keyboard → victory, pad only); else Partial
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
