# AGENTS.md

Family trivia party game, shown on a TV: the family plays against the gamemaster, 12 questions to victory. It runs offline; the code is public, media files are a gitignored cache. A Steam release is in the works.

## Work: `pm`
- Milestones, plans, tasks, decisions: all in `tasks.sql`, only through `pm`. Read `pm instructions` first.
- Start: `pm status`, `pm show <task>`.
- Before a choice: `pm decision list --answered --grep <word>`; answers are binding.
- Question only the gamemaster can answer: `pm decision add`, don't guess. Own lasting choice: `pm decision record`.
- Follow-up work: `pm task add`.
- Always consider updating existing milestones and plans (`pm milestone set`, `pm plan edit`); pm then queues a task that rewrites its descendants.
- Cite milestones, plans, tasks by id and subject, in backticks: `task 437: Translation prompts and market per locale`.

## Rules
- Push directly to `main`. No feature branches or pull requests.
- Use comments sparingly and keep them ultra-short.
- Don't write tests by default. Keep only the few, if any, that stay useful long-term; verify everything else with a throw-away script.
- Style of `.md` files: bullet points, ultra-concise, no full sentences needed. Exception: an intro paragraph in full sentences at the top of the document and under each top-level heading.
- Stop background processes by PID (`kill $!`), never `pkill -f`: the pattern can match your own `claude` process.
- Minimal dependencies; must run offline. No secrets, accounts or telemetry.
- Unpolished game parts: `PLACEHOLDER(<task id>)` in code and on screen.

## Making questions
- Asked to make, add, review or approve questions: follow [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md) exactly, nothing else. One command, `qgen batch` (`--bundle <id>` for a bundle other than `base`).
- Don't run pipeline steps by hand, edit the pools or pick media.
- `qgen rework`, `qgen tighten`, `qgen neutralize`: only when the gamemaster asks.

## Layout
- `app/` ships (game server, game UI, Electron shell, `app/data/`); `authoring/` doesn't (source pool, `qgen` pipeline, review/stats pages).
- `authoring/` may import from `app/`, never the reverse; `app/` never reads `authoring/data/`.
- Every path: [`directory.md`](directory.md).

## Commands
Dev shell from the flake: `direnv allow` or `nix develop`. Human how-tos: `README.md`.
- `trivia` (game, :8000), `trivia-authoring` (authoring pages, :8001)
- `npm run build`, `npm run check` (type-check), `npm run dev -w app/client|authoring/ui`
- `qgen validate` (also flags a stale `app/data/pool.json`), `qgen export`, `qgen report` (`-h` for its options)
- `trivia-media sync --status approved`
- `nix build .#app` → `result/bin/trivia`
