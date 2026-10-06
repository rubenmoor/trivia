# Trivia

A family trivia party game, shown on the living-room TV. The family plays as one team against the gamemaster and needs 12 correct answers to win. Questions are in Spanish and are drafted with Claude, then reviewed by the gamemaster. Media (images, audio, video) comes from Wikimedia Commons.

It runs locally and offline: a small Python server (standard library only) serves a Svelte client and the question pool in `data/questions.json`.

**Status:** the question pool, the generation pipeline and the review tool exist; the game screen doesn't yet. Plans, decisions and open questions live in [`plans/`](plans/README.md).

## Setup

With Nix and [direnv](https://direnv.net/), run this once in the repo root; the dev shell (Node 22, Python 3) then loads whenever you `cd` in:

```sh
direnv allow
```

Without direnv: `nix develop`. Without Nix: install Node 22+ and Python 3.

Then:

```sh
cd client && npm install && npm run build && cd ..
python3 tools/media.py sync        # download the media files (needs internet once)
python3 server/main.py             # http://127.0.0.1:8000/
```

## Commands

### Run

| Command | What it does |
|---|---|
| `python3 server/main.py` | Serve the built client and the API on http://127.0.0.1:8000/ (`--port`, `--host`) |
| `cd client && npm run dev` | Client with hot reload; forwards `/api` and `/media` to the server above, so run both |
| `cd client && npm run build` | Build the client into `client/dist/` (the server serves it) |
| `cd client && npm run check` | Type-check the client |

The review tool is the start page: `/?batch=pilot` shows one batch, `/?batch=first-120` the first 120 questions. Statistics: `/stats/categories` (questions per category) and `/stats/difficulty` (histogram), both filterable by status.

### Media

Media files are not in the repo. Each question stores the exact URL of its file (`file_url`); `media/` is a local cache named after those URLs. The server downloads missing files when they're first requested; `sync` downloads them ahead of time.

| Command | What it does |
|---|---|
| `python3 tools/media.py sync` | Download every picked file that isn't cached yet. **Run before game night.** |
| `python3 tools/media.py sync --status approved` | Only the files of approved questions |
| `python3 tools/media.py sync --prune` | Also delete cached files no question uses any more |
| `python3 tools/media.py fetch --batch <run>` | Search Commons for candidates for questions without media (`--batch first-120` for the first 120, `--ids q-0001,q-0002`, `--force` to search again) |

### Question pipeline

Writing steps call the `claude` CLI (`claude -p`), so they need Claude Code installed and logged in. Work files go to `work/<run>/` (gitignored); every step skips what's done, so a run can be resumed. Details: [`plans/07-question-generation.md`](plans/07-question-generation.md).

```sh
python3 tools/qgen.py fit       --run <run> --subcategories "Volcanes,Piratas"   # from data/categories.json
python3 tools/qgen.py draft     --run <run>
python3 tools/qgen.py rate      --run <run>
python3 tools/qgen.py factcheck --run <run>
python3 tools/qgen.py dedupe    --run <run>
python3 tools/qgen.py merge     --run <run>     # new questions enter the pool as drafts
python3 tools/media.py fetch    --batch <run>   # media candidates for the review tool
python3 tools/qgen.py report    [--run <run>]
python3 tools/qgen.py validate                  # check the pool; warns about uncached media
```

Revising questions already in the pool (e.g. after review feedback):

```sh
python3 tools/qgen.py import    --run <run> --batch <batch>
python3 tools/qgen.py rate      --run <run>
python3 tools/qgen.py factcheck --run <run>
python3 tools/qgen.py revise    --run <run>
python3 tools/qgen.py apply     --run <run>
```

### Dev environment

| Command | What it does |
|---|---|
| `nix develop` | Enter the dev shell without direnv |
| `nix flake update` | Update the pinned Node/Python versions (`flake.lock`) |
| `direnv reload` | Reload the shell after editing `flake.nix` |

## Layout

| Path | Contents |
|---|---|
| `data/questions.json` | The question pool |
| `data/categories.json` | 24 broad categories and their 140 subcategories |
| `server/main.py` | Local server: static files, question API, media cache |
| `client/` | Svelte 5 + Vite + TypeScript client: review tool, stats pages |
| `tools/qgen.py`, `tools/prompts/` | Question generation pipeline |
| `tools/media.py` | Wikimedia Commons search and the media cache |
| `plans/` | Plans, decisions, open questions, backlog |
| `media/`, `work/` | Local cache and pipeline work files (gitignored) |

Media credits (author, licence) are stored with each question and shown on screen.
