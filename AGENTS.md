# AGENTS.md

Family trivia party game, shown on a TV: the family plays against the gamemaster, 12 questions to victory. The code is public, media files are a gitignored cache. A Steam release is in the works.

## Work: `pm`
- Milestones, plans, tasks, decisions: all in `tasks.sql`, only through `pm`. Read `pm instructions` first.
- Start: `pm status`, `pm show <task>`.
- Before a choice: `pm decision list --answered --grep <word>`; answers are binding.
- Question only the human can answer: `pm decision add`, don't guess. Own lasting choice: `pm decision record`.
- Follow-up work: `pm task add`.
- Cite milestones, plans, tasks by id and subject, in backticks: `task 437: Translation prompts and market per locale`.

## Outside pm workers
- Skip this section if `PM_TASK` is set (you are a pm worker).
- Milestones are mine; edit them with pm when we answer decisions: `pm decision list`, `pm milestone set <id> --body - <<'EOF'`, then `pm decision answer <id> …`.
- note that editing a milestones triggers pm to add a task that rewrites its decendant plans and task; this is why editing a milestone is usually enough

## Work trees
- pm runs tasks in `../trivia-worktrees/<name>` (`[worktrees]` in `project-manager.toml`); gitignored state lives only in the main checkout
- Each work tree symlinks it, else `qgen batch` restarts a run from scratch and media steps fail:
  `for x in work media state .env.local; do ln -s "$PWD/$x" ../trivia-worktrees/<name>/$x; done` (from the main checkout)
- `/work`, `/media`, `/state` in `.git/info/exclude` (the `.gitignore` `dir/` patterns miss symlinks; untracked = dirty tree, RUNBOOK step 1)
- Before linking a new work tree: move its own `work/` runs into the main checkout's `work/`

## Rules
- Push directly to `main`. No feature branches or pull requests.
- Human review work (`trivia-authoring` reviews, spot checks, `qgen health ack`, the developer's hand edits to the pool): always in `../trivia-review`, then merge into `main` (README "Review in a separate worktree"); never in the main checkout, where `pm run` moves unstaged changes to a `pm/task-…-left` branch.
- CI is local, no GitHub Actions (D-73): before every commit `npm run check`, `npm test`, `npm run build`, `qgen validate` and the task's own check pass.
- Use comments sparingly and keep them ultra-short.
- Import, don't copy (decision 199): before writing a helper, constant, type or CSS block, `rg` for an existing one and import it (`authoring/` may import from `app/`); where importing is impossible (Python ↔ TS, `app/desktop` `.mjs` ↔ client TS, `report-server/`), a comment names the source.
- After moving, renaming or deleting a file, function, constant or decided behaviour, `rg` its old name or path over comments and `.md` files; fix every hit in the same commit (decision 200).
- Don't write tests by default. Keep only the few, if any, that stay useful long-term; don't verify too much either, use throw-away scripts to verify genuinely complex issues only.
- Style of `.md` files: bullet points, ultra-concise, no full sentences needed. Exception: an intro paragraph in full sentences at the top of the document and under each top-level heading.
- Game is muted under `PM_WORKER`; outside pm, launch with `TRIVIA_MUTE=1` unless the work is about sound; `TRIVIA_SOUND=1` for sound checks.
- Stop background processes by PID (`kill $!`), never `pkill -f`: the pattern can match your own `claude` process.
- No secrets in the repo, no accounts of our own; telemetry only opt-in.
- A script that calls claude reports its calls and totals (decision 208: What must a script that calls claude report to its caller?).
- Changing UI strings (`app/client/src/locales/`): read `locales/style/<locale>.md` first; new bad patterns found go into it.
- Unpolished game parts: `PLACEHOLDER(<task id>)` in code and on screen.
- "Gamemaster": only the in-game role (Gamemaster mode); the human is "the developer".
  - Older text (`tasks.sql`: milestones, plans, tasks, decisions) still says "the gamemaster" for the developer: read it as "the developer"; new text says "the developer".

## Making questions
- Asked to make, add, review or approve questions: follow [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md) exactly, nothing else. One command, `qgen batch` (`--bundle <id>` for a bundle other than `base`; `--translate <locale>` when a language is named).
- Don't run pipeline steps by hand, edit the pools or pick media.
- `qgen rework`, `qgen tighten`, `qgen neutralize`: only when the developer asks.

## Layout
- `app/` ships (game server, game UI, Electron shell, `app/data/`); `authoring/` doesn't (source pool, `qgen` pipeline, review/stats pages).
- `authoring/` may import from `app/`, never the reverse; `app/` never reads `authoring/data/`.
- Top-level `.md` files and directories: [`directory.md`](directory.md); no per-file rows (decision 196).

## Commands
Dev shell from the flake: `direnv allow` or `nix develop`. Human how-tos: `README.md`.
- `trivia` (game, :8000; static files + `/api/save` only, engine in the browser; serves `app/data/` at `/data/`, media from the cache only; save `state/game.json`, no SQLite; `game.sqlite`, `flags.json` kept as backups), `trivia-authoring` (authoring pages, :8001); `/review?licence=replace`: media files to replace (licence, broken source file)
- Browser checks of UI changes: Node dev server (plan 99), `npm run dev -w app/client` (dev client, :5173) or `npm run serve -w app/client` (built `dist/`, :4173, after `npm run build`); `/data/`, cache-only `/media`, the save through the desktop's `FileStore` via a page shim (saves and flags on, no Steam); save dir `TRIVIA_SAVE_DIR` or a fresh temp dir, printed as `trivia dev: save <path>`, never `state/`; muted under `PM_WORKER` or `TRIVIA_MUTE=1` (`TRIVIA_SOUND=1` to hear), `?mute` mutes any page
- `trivia-desktop` (Electron shell; `TRIVIA_DEV_STEAM_USER=1`: valid Steam user without Steam, saves and flags on, Esc menu «Ir a pregunta…»; mods from `TRIVIA_MODS_DIR`, else repo `mods/`; with the dev user `TRIVIA_DEV_WORKSHOP_DIR=<dir>`: fake Workshop items; `--no-mods`: safe start without mods (a crashed start with mods does the same once, plan 118); `--rp-probe`: Remote Play probe (plan 168, throw-away; log `<userData>/rp-probe.log`; F9 direct input, F10 guest cursor, F11 flash); `--lag-probe`: input and picture lag probe page (plan 170, throw-away; log `<userData>/lag-probe.log`; flash + press timings); `--check-mod <folder>`: headless mod check, no Steam, exit 0/1/2 (decision 133, player kit `modding/`); `TRIVIA_MUTE=1` muted (default under `PM_WORKER`), `TRIVIA_SOUND=1` sound anyway; `--publish-mod <folder>`: mod → Workshop item, needs a real Steam user, `--dry-run` without Steam), `trivia-desktop-build` (Windows zip + Linux tar.gz → `app/desktop/release/`; media encoded to WebP/Opus/WebM, cache `work/ship-media/`; `--dir`: also `{win,linux}-unpacked/` for the Steam depots, checked by `trivia-steam stage`)
- `trivia-release-check` (before every Steam upload, SW-6: `tag` gate (clean, HEAD `v<version>`), per-commit checks, licences, release bar, `nix build .#app`, desktop builds, `report` (`reportUrl` + `/health`; `--skip report` until the server is set up), credits both ways, smoke game, `multiplayer` (`smoke.mjs --multiplayer`: the three local multiplayer modes × pads, keyboard only, 4 pads + keyboard and mouse, fake pads), `mods` (`smoke.mjs --mods`: shipped examples as local mods, conversion, `--no-mods`), `media-budget` (`stage-media.mjs --check`, `app/desktop/media-budget.json`), manual rows; header: version, pool hash, kind `full`/`content-only` patch since the previous `v*` tag, save version change; `--skip <step>`, `--manual <file>`; report `work/steam/<tag>/release-check.md`)
- `trivia-steam upload --branch beta` (only `beta`; clean tree, tag `v<version>`, `steam.json` IDs → release check → stage → VDFs → `steamcmd run_app_build`; `--checked`, `--preview`, `--dry-run`; output `work/steam/<tag>/`)
- `trivia-report-server` (question report server, plan 103, wrangler: `dev` local on `127.0.0.1:8787`, local D1, fake `dev-*` tickets, prints the pull token, extra args to `wrangler dev` e.g. `--test-scheduled`; `seed-telemetry [N]`: N synthetic telemetry sessions to the local server, localhost only; `deploy`, `tail`, `secret <NAME>`: developer only)
- `trivia-trailer [--lang es,es-ES,en,de] [--keep-raw]` (store trailer, plan 88: shell under Xvfb (X11, window sized by `xdotool`), private PulseAudio null sink, ffmpeg x11grab, `TRIVIA_SOUND=1`, dev Steam user, demo save; scripted game cut to ≈20 s → `authoring/store/out/trailer/<lang>.mp4`, H.264/AAC; en/de refuse until their pools; on a failed walk `<lang>-failed.png`)
- `trivia-gallery` (screen gallery, plan 100: every screen and dialog per UI language from demo saves, built client on the Node dev server, temp save dir, desktop bridge stubbed; `--locale`, `--only <shot>`, `--size WxH` (default 1920x1080), `--list`, `--visible`; `work/gallery/<locale>[@<W>x<H>]/<shot>.png` + `manifest.json`: catalog key per visible text via `?gallery`, unmatched text listed; ~15 min for all four)
- `npm run build`, `npm run check` (type-check with strict `tsconfig` flags, on-screen literals, knip: unused exports/files/deps, ruff: Python; `code-review.md` "Linter evaluation"), `npm run dev -w app/client|authoring/ui`
- `qgen demo` (plan 174: `--sizes`, `--propose [--seats S]`, `--check [<file>]`, `--replace`; the demo's question list `authoring/data/demo.json`, exported by `qgen export` to `app/data/demo/`), `qgen validate` (also flags a stale `app/data/pool.json`, a bad or stale demo list and demo pools), `qgen export` (the game loads the pool once per page: reload it), `qgen report` (`-h` for its options; needs Node, dev shell); `qgen report --cost` for $ per approved and the projection per language; `qgen flag` (pasted player reports → `needs_work`), `qgen flag --pull` (report server's; token `TRIVIA_REPORT_TOKEN` or `state/report-token`)
- `trivia-media sync --status approved` (required before play: the game never downloads media)
- `nix build .#app` → `result/bin/trivia`
