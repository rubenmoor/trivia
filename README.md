# Trivia

A family trivia party game for the living-room TV. The family plays as one team against the gamemaster: answer 12 questions of rising difficulty to win, with jokers to get out of a tight spot. Questions are in Spanish. They are drafted, fact-checked and illustrated with Claude, and the developer reviews them. Images, audio and video come from Wikimedia Commons.

Everything runs locally and offline: the game (a Svelte client with the game engine) runs in the browser, served with the question pool by a small Python server (standard library only), or in the Electron desktop shell without Python. Media files aren't in the repo; they are downloaded once into a local cache.

## Status

**The family game is done** (October 2026): a full game night on the TV with sound, jokers and the final look, played by player name without touching code.

- **Questions:** about 1,140 approved on the shared difficulty scale 1–15 (D-38), each with a picked image, audio or video; more batches are being made. Players choose an age group and bundles before a game.
- **Engine:** the referee runs in the browser (TypeScript, `app/client/src/engine/`); the Python server only serves files and the save (D-90).
- **UI:** every on-screen string comes from a catalog (`es`, `es-ES`, `en`, `de`); question translations aren't shipped yet.
- **Next:** more content, screen polish, code quality, and the Steam release track (desktop build, store, release).

Milestones, plans and open tasks: `pm status` (`tasks.sql`); the older overview is [`plans/project.md`](plans/project.md). Where each file lives: [`directory.md`](directory.md).

## Getting started

You need [Nix](https://nixos.org/) with flakes. The dev shell has Node 22, Python 3, ImageMagick and Claude Code, plus Electron and the commands `trivia`, `trivia-desktop`, `trivia-desktop-build`, `trivia-authoring`, `qgen` and `trivia-media`, which run this checkout's scripts, Xvfb, on x86_64 Linux also `trivia-steam`, `trivia-release-check` and `steamcmd`, and `pm` ([project-manager](https://github.com/rubenmoor/project-manager)).

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
- Game saves, burned questions (questions a player has already seen) and flags live in `state/game.json`. Delete it to reset everything. An old `state/game.sqlite` + `flags.json` is migrated into it once at start; both stay as backups. A broken or newer `game.json` moves to `state/backup/` and the game starts fresh with a notice naming the backup.
- The game loads the pool once per page: reload the page (F5) after `qgen export` or a review session.
- Desktop shell (`trivia-desktop`, packaged builds): the save is `save/<steamid64>/game.json` per Steam user in `%APPDATA%\trivia` (Windows) or `~/.config/trivia` (Linux, Steam Deck); in this checkout `state/desktop/<steamid64>/game.json`, `state/desktop/dev/game.json` under `TRIVIA_DEV_STEAM_USER=1` without Steam; `TRIVIA_SAVE_DIR` overrides (the save is then `$TRIVIA_SAVE_DIR/game.json`). Without a Steam user nothing is saved (a notice says so) and flags are off. A broken or newer save moves to `backup/` beside it and the game starts fresh.
- Bring the browser game's save over: `trivia-desktop --import-save state/game.json` with the family's Steam account logged in (prints source, target and backup; refuses an existing save, `--force` replaces it and keeps the old one in `backup/game-import-<stamp>.json`; not a save: error, exit 1, nothing written), or copy `state/game.json` into the save folder. Unknown `--import*`/`--save*`/`--export*`/`--trivia*` flags or a missing file: error naming the flag, exit 2, no window (dialog when packaged).
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
qgen export              # rewrites app/data/pool.json and the packs' app/data/bundles/<id>/pool.json (the authoring server does this after every change); reload the game page
qgen report              # supply per level, difficulty and category; progress vs. targets (--bundle <id>, --player <name>, --subcategories, --calibration [<batch>…], --overlaps, --exit-check, --qc [<batch>], --cost, --batches, --simulate; all: -h)
qgen patch-notes [<from-tag> [<to-tag>]]   # a content patch's counts-only notes + Steam event drafts (default: newest v* tag → working tree)
```

### Pull player reports

```sh
qgen flag --pull --dry-run   # what the report server holds, nothing written
qgen flag --pull             # reports → needs_work reviews, then acknowledged on the server
```

Players send a flagged question with «Enviar» in «Preguntas marcadas»; the game posts it to the report server (`reportUrl` in `app/desktop/package.json`; `--url` overrides it). The pull needs the server's pull token: `export TRIVIA_REPORT_TOKEN=…` (e.g. in `.env.local`) or write it to `state/report-token` (gitignored); never commit it. Each report becomes a `needs_work` review with the feedback «Reporte de jugador (…)» in `/review?status=needs_work`; reports in `en`/`de` go to that translation. Pulled ids are kept in `state/reports-pulled.json`, so a repeated pull adds nothing; mod questions and unknown ids are skipped and acknowledged. Then `qgen rework` picks them up.

### A player pasted a report

Without a server (or when sending failed), players copy the report text from «Preguntas marcadas» («Copiar» / «Copiar todo») and paste it somewhere, e.g. the Steam Discussions. Paste it into `qgen flag`:

```sh
qgen flag --dry-run < report.txt   # what would change
qgen flag < report.txt             # or: qgen flag, paste, Ctrl-D
```

Text around the `¡Trivia! #q-… · …` blocks is ignored; one paste can hold many reports. The same report twice adds nothing.

### Work on the code

```sh
trivia & npm run dev -w app/client                 # game UI with hot reload
trivia-authoring & npm run dev -w authoring/ui     # authoring UI with hot reload (port 5174)
npm run check                                      # type-check both clients (strict tsconfig flags) + on-screen literals
npm test                                           # game engine tests (node:test)
npm run check:literals -w app/client               # on-screen literals outside the UI catalog (src/game by default)
npm run build -w app/client && trivia-desktop      # the game in the Electron desktop shell, no Python (no Steam: nothing saved; TRIVIA_DEV_STEAM_USER=1: state/desktop/dev/game.json)
```

The dev servers forward the Python servers' routes (`/api`, `/data`, `/media`; authoring also `/reports`), so run both. Before changing anything: milestones, plans, tasks and decisions are in `pm` (`pm status`, `pm decision list --answered`; [`AGENTS.md`](AGENTS.md)); older plans and D-numbers in [`plans/README.md`](plans/README.md), [`plans/decisions.md`](plans/decisions.md).

Environment variables (empty = unset):
- `TRIVIA_STATE`, `TRIVIA_MEDIA`: save folder and media cache (default `state/`, `media/`; packaged: `$XDG_DATA_HOME/trivia/`)
- `TRIVIA_WORK`: the pipeline's `work/` folder (authoring tools)
- `TRIVIA_SAVE_DIR`: the desktop shell's save folder
- `TRIVIA_DEVTOOLS=1`: the desktop shell opens its devtools
- `TRIVIA_STEAM_APPID`: the desktop shell's Steam App ID in dev (a Steam launch's `SteamAppId` wins; default 480)
- `TRIVIA_DEV_STEAM_USER=1`: the desktop shell counts as a valid Steam user without Steam (saves and flags on; dev runs and checks only, decision 111); also dev mode: Esc menu row «Ir a pregunta…» (question id or number → that question on screen)
- `TRIVIA_STEAM_SDK`: Steamworks SDK libs (set by the flake)
- `TRIVIA_STEAM_ACCOUNT`: `trivia-steam upload`'s Steam login; `TRIVIA_STEAMCMD_HOME`: SteamCMD's home (default `$XDG_DATA_HOME/trivia/steamcmd`)
- `VITE_AUTHORING_URL` (build time): the game's links to the authoring pages; `""` hides them (default: same host, port 8001)

### Check the UI wording (screen gallery)

```sh
trivia-gallery                                  # every screen and dialog in en, es, es-ES, de (~15 min)
trivia-gallery --locale de --only menu-gamemaster,victory   # some shots again; --list names them
```

Shots go to `work/gallery/<locale>/<shot>.png`; `work/gallery/manifest.json` has each visible text with its catalog key, and text without one (a literal) as unmatched. The game runs from demo saves in a temp folder, never your save.

Review them in `trivia-authoring` → `/gallery`: per language every shot; click a text for its catalog key, flag it with a note. Flags go to `authoring/data/ui-flags.json` for the next fix pass.

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
trivia-steam stage                    # stages build/dlc/<pack>/; depot folders + build/media + DLC = the archives
```

Before every Steam upload, on a clean, tagged commit: `trivia-release-check` (~15 min; per-commit checks, licences, release quality bar, `nix build .#app`, both desktop builds, the report server's `/health` at the build's `reportUrl` (`--skip report` until it is set up), a smoke game in `linux-unpacked`, then asks the manual checklist). Exit 1 on any ✗; `--skip <step>` for a known-broken step, `--manual <file>` for answers (`<row>: y|n|note` per line). Report: `work/steam/<tag>/release-check.md`.

Each artefact (~2.5 GB) holds the game, the data and the pool's media, and plays offline. Unpack it and start `Trivia.exe` (Windows; SmartScreen: «More info → Run anyway») or `./trivia` (Linux, Steam Deck). The first build downloads Electron for both platforms; later builds run offline. Outside Nix: `npm ci --prefix app/desktop && npm run dist --prefix app/desktop`.

### Publish a mod to the Workshop

- Steam client running and logged in; `--dry-run` checks and stages without Steam.
- First publish creates a private item and writes its id into `mod.json` (`workshopId`, decision 132); later runs update it.
- Accept the Workshop legal agreement at the printed URL, check the item page, then `--visibility public`.

```sh
trivia-desktop --publish-mod mods/<mod> [--changenote <text>] [--visibility public|friends|unlisted|private] [--content-only] [--dry-run]
```

Packaged: the game executable (`trivia`, `Trivia.exe`) with the same flags; Windows writes `<mod>-publish.log` beside the mod folder. Details: `plans/18-steam-integration.md` "Modding: Publishing".

### Update dependencies

- `nix flake update` updates Node, Python, ImageMagick, Claude Code and `pm` (`flake.lock`); `direnv reload` after editing `flake.nix`.
- After changing `package-lock.json`, update `npmDepsHash` in `flake.nix` (`nix run nixpkgs#prefetch-npm-deps -- package-lock.json`).
