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
- Push directly to `main`. No feature branches or pull requests.
- Use comments sparingly and keep them ultra-short.
- Don't write tests by default. Keep only the few, if any, that stay useful long-term; verify everything else with a throw-away script.
- Style of `.md` files: bullet points, ultra-concise, no full sentences needed. Exception: an intro paragraph in full sentences at the top of the document and under each top-level heading.
- Stop background processes by PID (`kill $!`), never `pkill -f`: the pattern can match your own `claude` process.

## Making questions
If you are asked to make, generate, add, review or approve questions, follow [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md) exactly and nothing else (D-36). It is one command, `qgen batch`. Don't run pipeline steps by hand, don't edit the pools, and don't pick media yourself. Quality control after a batch: [`authoring/QC.md`](authoring/QC.md) (D-56).

## Repo layout (D-35)
- `app/` is what ships: the game server (`app/server/`), the game UI (`app/client/`) and its data (`app/data/categories.json`, `app/data/bundles/`, `app/data/pool.json`).
- `authoring/` never ships: the source pool (`authoring/data/questions.json`), the pipeline (`authoring/tools/`), the review/stats/print pages (`authoring/server/`, `authoring/ui/`).
- `authoring/` may import from `app/`; `app/` never imports from `authoring/` and never reads `authoring/data/`. Put new code on the side it belongs to: if a player's install needs it, it's `app/`.
- Details: [`plans/19-repo-layout.md`](plans/19-repo-layout.md); every path explained: [`directory.md`](directory.md).

## Tech stack
- Server: Python, standard library only (`http.server`, `sqlite3`) (D-3, D-4).
- State: SQLite in `state/` (gitignored). Questions: `authoring/data/questions.json`, exported for the game to `app/data/pool.json` (D-4, D-35). Categories: `app/data/categories.json` (D-19).
- Client: Svelte 5 + Vite + TypeScript, built to static files (D-5). npm workspaces: `app/client` (game), `authoring/ui` (authoring pages).

## Commands
All tools come from the flake (D-18, D-35): `direnv allow` once (or `nix develop`) gives Node 22, Python 3, ImageMagick, Claude Code and the commands below. Commands for humans: `README.md`.
- Game: `trivia` (http://127.0.0.1:8000/). Authoring: `trivia-authoring` (start page http://127.0.0.1:8001/, `/review?batch=…`, `/review?status=!approved`, `/review?run=backaudit-<k>&audit=flagged` (or `&sample=1`, plan 57), `/review/<id>`, `/stats/categories`, `/stats/subcategories`, `/stats/difficulty`, `/stats/media`, `/comodines`).
- Clients: `npm install`, `npm run build` (both), `npm run check` (type-check both), `npm test` (engine tests, `app/client/src/engine/*.test.ts`, D-64), `npm run check:literals -w app/client` (on-screen literals outside `app/client/src/locales/es.ts`; paths as arguments, default `src/game`; LUI-1), `npm run dev -w app/client` or `-w authoring/ui` (hot reload; run the matching server too).
- Project manager: `pm` ([project-manager](https://github.com/rubenmoor/project-manager), in the dev shell). Run `pm instructions` before you use it: every command with examples.
  - Open decisions: `pm decision list` (context, numbered options, blocked tasks). Answer: `pm decision answer <id> <option number | own text>`; its blocked tasks become workable.
- Pool: `qgen validate` (also fails when `app/data/pool.json` is stale), `qgen export`, `qgen report` (progress vs. `authoring/data/targets.json`, `--bundle <id>`, plan 12; `--subcategories`: supply per subcategory and saturation flags, plan 14; `--calibration [<batch>…]`: difficulty per target level of the last batches, plan 13; `--overlaps`: approved questions that may ask the same fact, plan 15; `--batches [<batch>…]`: batch health side by side, plan 15; `--exit-check`: milestone 1 done or not, ✓/✗ per criterion, exit 1 on any ✗, plan 12; `--qc [<batch>]`: spot check vs. LLM review and audit, the batch report's Quality control section or the trend, plan 16), `qgen health ack <batch> "<note>"` (clears `qgen batch`'s exit 2 after a batch failed the health thresholds, D-55; only the gamemaster), `qgen rework` (needs_work questions once more through fix and review; `--model fable`: Fable for fix and review 1, D-65; only when the gamemaster asks), `qgen tighten` (shortens long-winded questions in the whole pool; only when the gamemaster asks), `qgen audit --backlog [--slice N]` (audits the next slice of approved questions from before D-56, default 200, `--dry-run` lists the ids; report `authoring/reports/backaudit-<k>.md`, plan 57; only when the gamemaster asks).
- Media: `trivia-media sync --status approved` before game night (`--prune` deletes unreferenced files). `trivia-media licenses` (`--status approved`, `--json`): files to replace before a public release, restriction flags, licence tally; exit 1 while anything needs replacing (plan 52).
- Desktop shell: `trivia-desktop` (Electron from the flake, plays `app/client/dist/` without Python; build the client first; `TRIVIA_MEDIA`, `TRIVIA_DEVTOOLS=1`, D-71). Save in memory until SW-3.
- Packaged game: `nix build .#app`, then `result/bin/trivia`.
- Placeholders: none left (D-25 is history); `grep -rn PLACEHOLDER app/client/src` stays empty.
- Categories: `app/data/categories.json` for `base`, `app/data/bundles/<id>/categories.json` for another bundle (broad categories → subcategories, D-19, D-43); questions store only `subcategory` and `bundle`. A batch writes for one bundle: `qgen batch` is `base`, `qgen batch --bundle <id>` another (D-41).
