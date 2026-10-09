# AGENTS.md — Guide for AI coding assistants

## Project
Family trivia party game. Runs locally and offline; the code is public on GitHub, media files are a gitignored cache (D-17). It is shown on a TV, and the family plays against the gamemaster. 12 questions to victory.

## Where to start
1. [`plans/README.md`](plans/README.md): index, conventions, task status markers.
2. [`plans/project.md`](plans/project.md): milestones, open tasks and open questions at a glance.
3. The plan file that owns the task you're working on.
4. [`plans/open-questions.md`](plans/open-questions.md): don't implement anything that depends on an unanswered question.

## Working rules
- Plans are the source of truth. Update the plan **before** you change direction in code.
- One task ID per change. Mark it `[x]` with a note once it's implemented.
- Log new work in `plans/backlog.md`. Log ambiguities in `plans/open-questions.md`.
- Log architectural choices in `plans/decisions.md`.
- Keep dependencies minimal. This is a hobby project that has to run offline in a living room.
- Never commit secrets. The game needs no accounts and no telemetry.

## Making questions
If you are asked to make, generate, add, review or approve questions, follow [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md) exactly and nothing else (D-36). It is one command, `qgen batch`. Don't run pipeline steps by hand, don't edit the pools, and don't pick media yourself.

## Repo layout (D-35)
- `app/` is what ships: the game server (`app/server/`), the game UI (`app/client/`) and its data (`app/data/categories.json`, `app/data/pool.json`).
- `authoring/` never ships: the source pool (`authoring/data/questions.json`), the pipeline (`authoring/tools/`), the review/stats/print pages (`authoring/server/`, `authoring/ui/`).
- `authoring/` may import from `app/`; `app/` never imports from `authoring/` and never reads `authoring/data/`. Put new code on the side it belongs to: if a player's install needs it, it's `app/`.
- Details: [`plans/19-repo-layout.md`](plans/19-repo-layout.md).

## Tech stack
- Server: Python, standard library only (`http.server`, `sqlite3`) (D-3, D-4).
- State: SQLite in `state/` (gitignored). Questions: `authoring/data/questions.json`, exported for the game to `app/data/pool.json` (D-4, D-35). Categories: `app/data/categories.json` (D-19).
- Client: Svelte 5 + Vite + TypeScript, built to static files (D-5). npm workspaces: `app/client` (game), `authoring/ui` (authoring pages).

## Commands
All tools come from the flake (D-18, D-35): `direnv allow` once (or `nix develop`) gives Node 22, Python 3, ImageMagick, Claude Code and the commands below. Commands for humans: `README.md`.
- Game: `trivia` (http://127.0.0.1:8000/). Authoring: `trivia-authoring` (start page http://127.0.0.1:8001/, `/review?batch=…`, `/review/<id>`, `/stats/categories`, `/stats/subcategories`, `/stats/difficulty`, `/comodines`).
- Clients: `npm install`, `npm run build` (both), `npm run check` (type-check both), `npm run dev -w app/client` or `-w authoring/ui` (hot reload; run the matching server too).
- Pool: `qgen validate` (also fails when `app/data/pool.json` is stale), `qgen export`, `qgen report`.
- Media: `trivia-media sync --status approved` before game night (`--prune` deletes unreferenced files).
- Packaged game: `nix build .#app`, then `result/bin/trivia`.
- Placeholders: unpolished game parts are marked `PLACEHOLDER(<task ID>)` in code and on screen (D-25); `grep -rn PLACEHOLDER app/client/src` lists them.
- Categories: `app/data/categories.json` (broad categories → subcategories, D-19); questions store only `subcategory`.
