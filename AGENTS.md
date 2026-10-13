# AGENTS.md

Family trivia party game, shown on a TV: the family plays against the gamemaster, 12 questions to victory. It runs offline; the code is public, media files are a gitignored cache. A Steam release is in the works.

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

## Rules
- Push directly to `main`. No feature branches or pull requests.
- CI is local, no GitHub Actions (D-73): before every commit `npm run check`, `npm test`, `npm run build`, `qgen validate` and the task's own check pass.
- Use comments sparingly and keep them ultra-short.
- Don't write tests by default. Keep only the few, if any, that stay useful long-term; don't verify too much either, use throw-away scripts to verify genuinely complex issues only.
- Style of `.md` files: bullet points, ultra-concise, no full sentences needed. Exception: an intro paragraph in full sentences at the top of the document and under each top-level heading.
- Stop background processes by PID (`kill $!`), never `pkill -f`: the pattern can match your own `claude` process.
- Minimal dependencies; must run offline. No secrets, accounts or telemetry.
- Unpolished game parts: `PLACEHOLDER(<task id>)` in code and on screen.

## Making questions
- Asked to make, add, review or approve questions: follow [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md) exactly, nothing else. One command, `qgen batch` (`--bundle <id>` for a bundle other than `base`; `--translate <locale>` when a language is named).
- Don't run pipeline steps by hand, edit the pools or pick media.
- `qgen rework`, `qgen tighten`, `qgen neutralize`: only when the gamemaster asks.

## Layout
- `app/` ships (game server, game UI, Electron shell, `app/data/`); `authoring/` doesn't (source pool, `qgen` pipeline, review/stats pages).
- `authoring/` may import from `app/`, never the reverse; `app/` never reads `authoring/data/`.
- Every path: [`directory.md`](directory.md).

## Commands
Dev shell from the flake: `direnv allow` or `nix develop`. Human how-tos: `README.md`.
- `trivia` (game, :8000; static files + `/api/save` only, engine in the browser; serves `app/data/` at `/data/`, media from the cache only; save `state/game.json`, no SQLite; `game.sqlite`, `flags.json` kept as backups), `trivia-authoring` (authoring pages, :8001); `/review?licence=replace`: media files to replace (licence)
- `trivia-desktop` (Electron shell), `trivia-desktop-build` (Windows zip + Linux tar.gz → `app/desktop/release/`; `--dir`: also `{win,linux}-unpacked/` for the Steam depots, checked by `trivia-steam stage`)
- `trivia-release-check` (before every Steam upload, SW-6: per-commit checks, licences, release bar, `nix build .#app`, desktop builds, smoke game, manual rows; `--skip <step>`, `--manual <file>`; report `work/steam/<tag>/release-check.md`)
- `npm run build`, `npm run check` (type-check + lint: strict `tsconfig` flags, `code-review.md` "Linter evaluation"), `npm run dev -w app/client|authoring/ui`
- `qgen validate` (also flags a stale `app/data/pool.json`), `qgen export` (the game loads the pool once per page: reload it), `qgen report` (`-h` for its options; needs Node, dev shell); `qgen report --cost` for $ per approved and the projection per language
- `trivia-media sync --status approved` (required before play: the game never downloads media)
- `nix build .#app` → `result/bin/trivia`
