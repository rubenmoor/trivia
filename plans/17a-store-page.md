# 17a — Store page

**Status:** stub

Sub-plan of [17](17-publishing.md). Everything the gamemaster pastes into Steamworks' store page admin for the beta (plan 88, PUB-8, LUI-6): texts per store language, AI disclosure, requirements, languages, controller flags, capsules and screenshots. Workers draft and render here; the gamemaster approves through pm decisions and enters them.

## Screenshots
- Rendered, not hand-made: `node authoring/store/screenshots.mjs [--lang en,es,es-ES,de] [--visible]` from the dev shell (`npm run build` and `trivia-media sync --status approved` first)
- Shell at 1920×1080 under Xvfb, raw CDP, a throw-away demo save per shot (made-up players), offline
- Output: `authoring/store/out/screenshots/<lang>/NN-<screen>.png` (gitignored)
- Screens: start, player, modes, customize, tower (level 11); with a question pool of the language also cards, image question, video question, Francotirador aiming, victory
- Questions per shot: `Q` in the script
- Re-run after every visual change; the chosen set re-rendered before upload
