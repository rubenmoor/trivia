# Trivia

A family trivia party game for the living-room TV. The family plays as one team against the gamemaster: answer 12 questions of rising difficulty to win, with jokers to get out of a tight spot. Questions are in Spanish. They are drafted, fact-checked and illustrated with Claude, and the gamemaster reviews them. Images, audio and video come from Wikimedia Commons.

Everything runs locally and offline: the game (a Svelte client with the game engine) runs in the browser, served with the question pool by a small Python server (standard library only), or in the Electron desktop shell without Python. Media files aren't in the repo; they are downloaded once into a local cache.

## Status

**The family game is done** (October 2026): a full game night on the TV with sound, jokers and the final look, played by player name without touching code.

- **Questions:** about 1,140 approved on the shared difficulty scale 1–15 (D-38), each with a picked image, audio or video; more batches are being made. Players choose an age group and bundles before a game.
- **Engine:** the referee runs in the browser (TypeScript, `app/client/src/engine/`); the Python server only serves files and the save (D-90).
- **UI:** every on-screen string comes from a catalog (`es`, `es-ES`, `en`, `de`); question translations aren't shipped yet.
- **Next:** more content, screen polish, code quality, and the Steam release track (desktop build, store, release).

Milestones, plans and open tasks: `pm status` (`tasks.sql`); the older overview is [`plans/project.md`](plans/project.md). Where each file lives: [`directory.md`](directory.md).

## Getting started

You need [Nix](https://nixos.org/) with flakes. The dev shell has Node 22, Python 3, ImageMagick and Claude Code, plus Electron and the commands `trivia`, `trivia-desktop`, `trivia-desktop-build`, `trivia-authoring`, `qgen` and `trivia-media`, which run this checkout's scripts, and `pm` ([project-manager](https://github.com/rubenmoor/project-manager)).

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
- `M` (or the faint flag next to the menu button) flags the question for review: a dialog with an optional note, `Enter` flags, `Esc` cancels; on a flagged question it edits the note or unflags. The next start of `trivia-authoring` marks it «needs work» with the note; the menu's «Preguntas marcadas» lists the flags with «Copiar» for players without authoring tools.
- Game saves, burned questions (questions a player has already seen) and flags live in `state/game.json`. Delete it to reset everything. An old `state/game.sqlite` + `flags.json` is migrated into it once at start; both stay as backups.
- The game loads the pool once per page: reload the page (F5) after `qgen export` or a review session.
- Desktop shell (`trivia-desktop`, packaged builds): the save is `save/<steamid64>/game.json` per Steam user, `save/local/game.json` without Steam, in `%APPDATA%\trivia` (Windows) or `~/.config/trivia` (Linux, Steam Deck); in this checkout `state/desktop/<steamid64 or local>/game.json`; `TRIVIA_SAVE_DIR` overrides (the save is then `$TRIVIA_SAVE_DIR/game.json`). An older `save/game.json` moves to `save/local/` at start. A broken or newer save moves to `backup/` beside it and the game starts fresh.
- Bring the browser game's save over: `trivia-desktop --import-save state/game.json` (only when no desktop save exists yet), or copy `state/game.json` into the save folder.
- The game never downloads media: sync before game night (next section). `trivia` prints at start how many pool files are missing from the cache; a missing file shows the question's media-failed state.

### Sync the media before game night (required)

```sh
trivia-media sync --status approved     # downloads every picked file that isn't cached yet
trivia-media sync --status approved --prune   # also deletes cached files no question uses any more
trivia-media licenses                   # files to replace before a public release (licence audit)
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

Also on the authoring server: stats at `/stats/categories`, `/stats/subcategories`, `/stats/difficulty` and `/stats/media`, and printable joker cards at `/comodines`.

### Make new questions

```sh
claude                   # log in once (Claude Code is in the dev shell)
qgen batch               # one new batch: concepts, drafts, rating, fact-check, revision, media
qgen batch --bundle colombia   # the same for another bundle's subcategories
qgen health ack <batch> "<note>"  # after looking at a batch that failed the health thresholds: lets `qgen batch` start the next one
qgen rework              # every needs_work question with feedback once more: Claude fixes it, fact-checks, reviews (--batch <batch>)
qgen audit --backlog     # audit the next 200 approved questions from before D-56 (--slice N, --dry-run)
qgen tighten             # Claude reads the whole pool (approved too), shortens long-winded questions, fact-checks, reviews
qgen bundle new <id> --name … --description … --kind region|theme --rule …   # an empty bundle; then fill app/data/bundles/<id>/categories.json
```

Don't run the pipeline steps by hand; the batch command does it all and can be resumed. Details: [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md). Afterwards, review the batch in the review tool.

`trivia-media fetch --batch <batch>` searches Commons for media candidates for questions that have none yet. The single pipeline steps (`qgen draft`, `rate`, `factcheck`, …, and `qgen import` for revising questions already in the pool) stay available for debugging; work files go to `work/<run>/`. See [`plans/07-question-generation.md`](plans/07-question-generation.md).

Media comes from Wikimedia Commons first, then NASA (space only), Openverse and Freesound (D-45, [`plans/23-media-providers.md`](plans/23-media-providers.md)). Keys go in `.env.local` (gitignored, loaded by direnv): `COMMONS_ACCESS_TOKEN` (an owner-only OAuth 2.0 consumer with basic rights on Meta-Wiki; higher Commons limits, IMG-15), `FREESOUND_API_KEY` (Freesound is skipped without it), and optionally `OPENVERSE_CLIENT_ID`/`OPENVERSE_CLIENT_SECRET` (Openverse works anonymously with 200 requests a day).

### Check the question pool

```sh
qgen validate            # checks the source pool, and that app/data/pool.json is its current export
qgen export              # rewrites app/data/pool.json (the authoring server does this after every change); reload the game page
qgen report              # supply per level, difficulty and category; progress vs. targets (--bundle <id>, --player <name>, --subcategories, --calibration [<batch>…], --overlaps, --exit-check, --qc [<batch>])
```

### Work on the code

```sh
trivia & npm run dev -w app/client                 # game UI with hot reload
trivia-authoring & npm run dev -w authoring/ui     # authoring UI with hot reload (port 5174)
npm run check                                      # type-check both clients
npm test                                           # game engine tests (node:test)
npm run check:literals -w app/client               # on-screen literals outside the UI catalog (src/game by default)
npm run build -w app/client && trivia-desktop      # the game in the Electron desktop shell, no Python (save: state/desktop/local/game.json)
```

The dev servers forward `/api` and `/media` to the Python servers, so run both. Before changing anything, read [`plans/README.md`](plans/README.md): plans are the source of truth, and decisions (D-numbers) are logged in [`plans/decisions.md`](plans/decisions.md).

### Build the packaged game

```sh
nix build .#app && result/bin/trivia
```

The package contains only `app/`. It keeps its saves and media cache in `$XDG_DATA_HOME/trivia/` instead of the checkout; `TRIVIA_STATE` and `TRIVIA_MEDIA` override both locations. The packaged cache starts empty and the game never downloads: run it with `TRIVIA_MEDIA` pointing at a synced cache (e.g. `TRIVIA_MEDIA=$PWD/media result/bin/trivia`).

### Build the desktop game

```sh
trivia-media sync --status approved   # the pool's media must be in the cache
trivia-desktop-build                  # → app/desktop/release/Trivia-<version>-win-x64.zip, …-linux-x64.tar.gz
trivia-desktop-build --dir            # also win-unpacked/, linux-unpacked/ for the Steam depots
trivia-steam stage                    # depot folders + build/media = the archives
```

Each artefact (~2.5 GB) holds the game, the data and the pool's media, and plays offline. Unpack it and start `Trivia.exe` (Windows; SmartScreen: «More info → Run anyway») or `./trivia` (Linux, Steam Deck). The first build downloads Electron for both platforms; later builds run offline. Outside Nix: `npm ci --prefix app/desktop && npm run dist --prefix app/desktop`.

### Update dependencies

- `nix flake update` updates Node, Python, ImageMagick, Claude Code and `pm` (`flake.lock`); `direnv reload` after editing `flake.nix`.
- After changing `package-lock.json`, update `npmDepsHash` in `flake.nix` (`nix run nixpkgs#prefetch-npm-deps -- package-lock.json`).
