# AGENTS.md — Guide for AI coding assistants

## Project
Family trivia party game. Runs locally and offline; the code is public on GitHub, media files are a gitignored cache (D-17). It is shown on a TV, and the family plays against the gamemaster. 12 questions to victory.

## Where to start
1. [`plans/README.md`](plans/README.md): index, conventions, task status markers.
2. The plan file that owns the task you're working on.
3. [`plans/open-questions.md`](plans/open-questions.md): don't implement anything that depends on an unanswered question.

## Working rules
- Plans are the source of truth. Update the plan **before** you change direction in code.
- One task ID per change. Mark it `[x]` with a note once it's implemented.
- Log new work in `plans/backlog.md`. Log ambiguities in `plans/open-questions.md`.
- Log architectural choices in `plans/decisions.md`.
- Keep dependencies minimal. This is a hobby project that has to run offline in a living room.
- Never commit secrets. The game needs no accounts and no telemetry.

## Tech stack
- Server: Python, standard library only (`http.server`, `sqlite3`) (D-3, D-4).
- State: SQLite. Questions: a JSON file (D-4). Categories: `data/categories.json` (D-19).
- Client: Svelte 5 + Vite + TypeScript, built to static files (D-5).

## Commands
- Question pipeline: `python3 tools/qgen.py --help` (steps: fit, draft, rate, factcheck, dedupe, merge, report, validate; see `plans/07-question-generation.md`).
- Validate the pool: `python3 tools/qgen.py validate`.
- Fetch media candidates from Wikimedia Commons: `python3 tools/media.py fetch --batch <run>` (`--batch first-120` for the first 120).
- Fill the media cache (`media/`, gitignored) before game night: `python3 tools/media.py sync` (`--prune` deletes unreferenced files).
- Dev environment (Nix flake, D-18): `direnv allow` once (or `nix develop`) gives Node 22 and Python 3. All commands for humans: `README.md`.
- Client install: `cd client && npm install`.
- Client build: `cd client && npm run build` (output in `client/dist/`, served by the Python server).
- Client type check: `cd client && npm run check`.
- Run: `python3 server/main.py`, then open http://127.0.0.1:8000/ (review tool: `/?batch=pilot`; stats: `/stats/categories`, `/stats/difficulty`).
- Categories: `data/categories.json` (broad categories → subcategories, D-19); questions store only `subcategory`.
- Client dev with hot reload: run the server, then `cd client && npm run dev` (Vite forwards `/api` and `/media` to port 8000).
