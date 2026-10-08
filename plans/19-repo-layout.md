# 19 — Repo Layout, Packaging and the LLM Batch

**Status:** active

The repo is split into what ships (the game) and what doesn't (the tooling that makes questions). Everything the question pipeline needs, including Claude, comes from the flake. An LLM produces a batch of questions with **one command**; its own judgement is confined to prompts inside that command (D-35, D-36).

## Layout

```
app/                    ships: everything a player's install contains
  server/               main.py (static files, game API, /media), game.py, selection.py,
                        categories.py, media_cache.py
  client/               the game UI (Svelte); builds to app/client/dist/
  data/                 categories.json, pool.json (exported, approved questions only)
authoring/              never ships
  tools/                qgen.py, concepts.py (concept lists, axes), media.py (Commons search, sheets), prompts/
  server/               main.py: review tool, stats and print pages, authoring API
  ui/                   review, stats and print pages (Svelte); builds to authoring/ui/dist/
  data/                 questions.json (the source pool), question-axes.json, concepts/ (D-37)
  reports/              one generated report per batch
  RUNBOOK.md            the LLM batch procedure: the only instructions an LLM follows for questions
state/  media/  work/   gitignored: game saves, media cache, pipeline work files
flake.nix               packages app and authoring; dev shell
package.json            npm workspaces: app/client, authoring/ui (one lockfile)
```

**Dependency rule:** `authoring/` may import from `app/`; `app/` never imports from `authoring/` and never reads `authoring/data/`. The game reads only `app/data/` and the media cache.

- `app/data/pool.json` is written by `qgen.py export`: approved questions with the fields play needs, without `review`, `quality`, `revision` or pipeline fields (this is PORT-6 of [12](12-client-engine.md), pulled forward). `validate` fails when the export is stale.
- `data/categories.json` moves to `app/data/`: the game's category picker needs it, and the pipeline reads it from there.
- The game's admin overlay links to the review tool and stats on the authoring server's port. In a packaged build without the authoring server, the links lead nowhere and are hidden.
- `server/game.py` and `tools/selection.py` move as they are. The TypeScript port ([12](12-client-engine.md)) later replaces them inside `app/`.

## Ports and commands
- Game: `python3 app/server/main.py` → http://127.0.0.1:8000/
- Authoring: `python3 authoring/server/main.py` → http://127.0.0.1:8001/review, /stats, /comodines
- In the dev shell, wrappers: `trivia` (game), `trivia-authoring`, `qgen`, `trivia-media`.

## Flake
- `packages.app` (`nix build .#app`): the built game client plus the Python server, run with `trivia`. Writable state and the media cache default to `$XDG_DATA_HOME/trivia/` when run from the package, and to `state/` and `media/` in the repo.
- `packages.authoring`: `qgen`, `trivia-media`, `trivia-authoring`, with `python3`, `imagemagick` and `claude-code` on their PATH.
- `devShells.default`: Node 22, Python 3, ImageMagick, `claude-code`.
- `claude-code` is unfree. The flake allows exactly that one unfree package. Its version is pinned in `flake.lock`; `nix flake update` moves it forward.

## The LLM batch (D-36)
One command does everything from choosing subcategories to approved questions with picked media:

```
qgen batch
```

Fixed rules, so there is nothing left to decide:
- **Run name:** `batch-<n>`, where n is one more than the highest `batch-<n>` in the pool. An unfinished run is resumed instead of starting a new one.
- **Subcategories:** the 30 with the fewest approved questions, ties in `categories.json` order.
- **Steps, in this order:** concepts (D-37; was fit) → draft → rate → factcheck → dedupe → revise → apply → rate → factcheck → dedupe → merge → media → sheets → review → research → sheets → review (researched only) → record → export → sync → batch-report → validate. Every step skips work that is already done, so rerunning `qgen batch` continues where it stopped.
- **Review (`review`, new):** one `claude -p` call per question with `prompts/review.md` (the D-32 criteria), the question, the rater's notes, the fact-check, the pool questions with the same answer, and the contact sheet of its media candidates (`sheets`, ImageMagick), which Claude opens with the Read tool. Output, by JSON schema: `decision` (approved | needs_work), `feedback` (required for needs_work), `pick` (candidate number, or null) and `new_query` (or null).
- **Research:** a question whose review asks for `new_query` gets one new Commons search and one more review. If it still has no usable media, it becomes `needs_work`.
- **Record:** writes the reviews as `{"reviewer": "llm", "model": <the model id the call reported>}` (D-33) and the picks (without downloading).
- **Sync:** downloads the picked files. A Commons rate limit doesn't fail the batch; the report lists what is still missing.
- **Batch report (`batch-report`):** `authoring/reports/<run>.md`, written by code: counts, the needs_work list with feedback, dropped drafts, cost.
- **Usage limits:** when Claude reports a usage limit, `qgen batch` stops with exit code 75 and prints when to rerun.

The individual steps stay available as subcommands for debugging, but the RUNBOOK uses only `qgen batch`.

## Tasks
- [x] LP-1 Plan and decisions D-35, D-36 (this file). *2026-10-07.*
- [x] LP-2 Move files into `app/` and `authoring/`; split `server/main.py` and the client; npm workspaces; fix every path; `validate`, `npm run check` and the game run. *2026-10-07: shared pieces in `app/server/paths.py`, `http_base.py`, `media_cache.py`; `authoring/tools/layout.py`.*
- [x] LP-3 `qgen.py export` and `app/data/pool.json`; the game reads only `app/data/`; `validate` checks that the export is current. *2026-10-07: `authoring/tools/pool_export.py`; the authoring server re-exports after every change.*
- [x] LP-4 Flake: `packages.app`, `packages.authoring`, dev shell with ImageMagick and `claude-code`; `nix build .#app` and running it tested. *2026-10-07: the package contains no authoring code and hides the overlay's authoring links.*
- [x] LP-5 `media.py sheets`, `qgen.py review`, `research`, `record`, `report`, `batch`; `prompts/review.md`. *2026-10-07: the report step is `batch-report` (`report` is the supply report); `revise` now skips revised drafts (one round, QG-16).*
- [x] LP-6 `authoring/RUNBOOK.md`; AGENTS.md and README point to it; old commands updated everywhere. *2026-10-07: plans too, except the decision log.*
- [x] LP-7 Smoke test: `qgen batch` on 2 subcategories end to end. *2026-10-07, in a throwaway copy: stopped at a usage limit (exit 75) during `revise`, resumed with the same command; 5 merged, 4 approved, 1 needs_work (a real giveaway), audio question with background picked, about $1.90. Found overlong Commons author fields in credits: `short_author` keeps a short first line or leaves the author out; five existing credits fixed.*
