# Trivia

A family trivia party game for the living-room TV. The family plays as one team against the gamemaster: answer 12 questions of rising difficulty to win, with jokers to get out of a tight spot. Questions are in Spanish. They are drafted, fact-checked and illustrated with Claude, and the gamemaster reviews them. Images, audio and video come from Wikimedia Commons.

Everything runs locally and offline: a small Python server (standard library only) serves a Svelte client and the question pool. Media files aren't in the repo; they are downloaded once into a local cache.

## Status

**The family game is done** (October 2026): a full game night on the TV with sound, jokers and the final look, played by player name without touching code.

- **Questions:** about 480 approved, on a difficulty scale tuned for young teens. The top levels (9–10) are thin, and more batches are being made.
- **Media:** about 360 approved questions have a picked image, audio or video; about 120 still have none.
- **Next:** more content, a game engine in TypeScript (so the game runs without Python), UI strings in a catalog, a media license audit, and age groups and bundles in the game. A public Steam release is a separate, later track.

Milestones and open tasks: [`plans/project.md`](plans/project.md). Where each file lives: [`directory.md`](directory.md).

## Getting started

You need [Nix](https://nixos.org/) with flakes. The dev shell has Node 22, Python 3, ImageMagick and Claude Code, plus the commands `trivia`, `trivia-authoring`, `qgen` and `trivia-media`, which run this checkout's scripts.

```sh
git clone https://github.com/rubenmoor/trivia.git && cd trivia
direnv allow             # once; the shell then loads whenever you cd in (without direnv: nix develop)
npm install
npm run build            # builds both web clients: the game and the authoring pages
```

Without Nix, Python 3 and Node 22 are enough to play: run `python3 app/server/main.py` instead of `trivia`, and `python3 authoring/server/main.py` instead of `trivia-authoring`.

## How to …

### Run the game

```sh
trivia                   # http://127.0.0.1:8000/   (--port, --host)
```

Open the page on the TV's browser and go fullscreen. Pick or type a player name and play.

- `Esc` (or the menu button) opens the admin menu: skip, undo, restart, fullscreen, volume, joker budget. It links to the review tool and stats while the authoring server runs.
- `M` (or the faint flag next to the menu button) flags the question for review; the next start of `trivia-authoring` marks it «needs work».
- Game saves and burned questions (questions a player has already seen) live in `state/game.sqlite`. Delete it to reset everything.
- The game plays fine with an empty media cache when online: a missing file is downloaded the first time it's shown. Offline, sync first (next section).

### Sync the media before game night

```sh
trivia-media sync --status approved     # downloads every picked file that isn't cached yet
trivia-media sync --status approved --prune   # also deletes cached files no question uses any more
```

This needs internet once. Files go to `media/` (gitignored); credits (author, licence) are stored with each question and shown on screen.

### Review questions

```sh
trivia-authoring         # http://127.0.0.1:8001/
```

The start page shows what waits for you (new batches, `needs_work` questions, questions without media), batches and game readiness, each as a link into a review queue. You can also open a queue directly: `/review?batch=batch-5`, `/review?status=!approved` (everything not approved; the link prints at startup), `/review?bundle=colombia`, or one question with `/review/<id>`.

The review tool is keyboard-driven:

| Key | Action |
|---|---|
| `a` / `r` | Approve / reject, go to the next question |
| `f` | Write feedback (`Enter` saves, `Esc` cancels) |
| `→` / `←` | Next / previous without deciding |
| `u` | Undo the last decision |
| `d`, number, `Enter` | Set the difficulty (1–15) |
| `c`, then `1`–`6` | Show the alternative media and pick one; `m` searches with a new term |
| `b` | Alternative background images (audio questions) |
| `s` | Show / hide the rater scores |

Every decision is saved into `authoring/data/questions.json` and re-exported to `app/data/pool.json` at once, so the game sees it on its next question. Switch off browser extensions that grab single keys (e.g. Vimium) for `127.0.0.1:8001`. All keys: [`plans/08-review-tool.md`](plans/08-review-tool.md).

Also on the authoring server: stats at `/stats/categories`, `/stats/subcategories` and `/stats/difficulty`, and printable joker cards at `/comodines`.

### Make new questions

```sh
claude                   # log in once (Claude Code is in the dev shell)
qgen batch               # one new batch: concepts, drafts, rating, fact-check, revision, media
qgen batch --bundle colombia   # the same for another bundle's subcategories
qgen bundle new <id> --name … --description … --kind region|theme --rule …   # an empty bundle; then fill app/data/bundles/<id>/categories.json
```

Don't run the pipeline steps by hand; the batch command does it all and can be resumed. Details: [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md). Afterwards, review the batch in the review tool.

`trivia-media fetch --batch <batch>` searches Commons for media candidates for questions that have none yet. The single pipeline steps (`qgen draft`, `rate`, `factcheck`, …, and `qgen import` for revising questions already in the pool) stay available for debugging; work files go to `work/<run>/`. See [`plans/07-question-generation.md`](plans/07-question-generation.md).

Media comes from Wikimedia Commons first, then NASA (space only), Openverse and Freesound (D-45, [`plans/23-media-providers.md`](plans/23-media-providers.md)). Keys go in `.env.local` (gitignored, loaded by direnv): `COMMONS_ACCESS_TOKEN` (an owner-only OAuth 2.0 consumer with basic rights on Meta-Wiki; higher Commons limits, IMG-15), `FREESOUND_API_KEY` (Freesound is skipped without it), and optionally `OPENVERSE_CLIENT_ID`/`OPENVERSE_CLIENT_SECRET` (Openverse works anonymously with 200 requests a day).

### Check the question pool

```sh
qgen validate            # checks the source pool, and that app/data/pool.json is its current export
qgen export              # rewrites app/data/pool.json (the authoring server does this after every change)
qgen report              # supply per level, difficulty and category (--player <name>, --subcategories)
```

### Work on the code

```sh
trivia & npm run dev -w app/client                 # game UI with hot reload
trivia-authoring & npm run dev -w authoring/ui     # authoring UI with hot reload (port 5174)
npm run check                                      # type-check both clients
```

The dev servers forward `/api` and `/media` to the Python servers, so run both. Before changing anything, read [`plans/README.md`](plans/README.md): plans are the source of truth, and decisions (D-numbers) are logged in [`plans/decisions.md`](plans/decisions.md).

### Build the packaged game

```sh
nix build .#app && result/bin/trivia
```

The package contains only `app/`. It keeps its saves and media cache in `$XDG_DATA_HOME/trivia/` instead of the checkout; `TRIVIA_STATE` and `TRIVIA_MEDIA` override both locations.

### Update dependencies

- `nix flake update` updates Node, Python, ImageMagick and Claude Code (`flake.lock`); `direnv reload` after editing `flake.nix`.
- After changing `package-lock.json`, update `npmDepsHash` in `flake.nix` (`nix run nixpkgs#prefetch-npm-deps -- package-lock.json`).
