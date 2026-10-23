# Trivia

A family trivia party game for the living-room TV. The family plays as one team against the gamemaster: answer 12 questions of rising difficulty to win, with jokers to get out of a tight spot. Questions are in Spanish. They are drafted, fact-checked and illustrated with Claude, and the developer reviews them. Images, audio and video come from Wikimedia Commons.

Everything runs locally and offline: the game (a Svelte client with the game engine) runs in the browser, served with the question pool by a small Python server (standard library only), or in the Electron desktop shell without Python. Media files aren't in the repo; they are downloaded once into a local cache.

## Status

**The family game is done** (October 2026): a full game night on the TV with sound, jokers and the final look, played by player name without touching code.

- **Questions:** about 2,140 approved (base ~2,040, «Regional: Colombia» ~100) on the shared difficulty scale 1–15 (D-38), with images, audio or video; more batches are being made.
- **Age groups and bundles:** before each game the Mode screens pick the mode and the Choice screen sets an age group (or a custom difficulty range in gamemaster mode), then the Bundles screen toggles any combination of bundles, base and regional (start needs at least one question); the game offers only the bundles of its language (milestone 5).
- **Modes:** gamemaster mode (configure screen, Esc menu cheats; «Responder para avanzar» off: the padlock only reveals the answer, no win or loss) and «Solo o en grupo» (standard jokers, no skips); the three multiplayer modes are specified, not built (D-74, D-77, D-80, D-105; [`plans/13-game-modes.md`](plans/13-game-modes.md)).
- **Engine:** the referee runs in the browser (TypeScript, `app/client/src/engine/`); the Python server only serves files and the save (D-90).
- **UI:** every on-screen string comes from a catalog (`es`, `es-ES`, `en`, `de`); one language setting for UI and questions, picked at first start; question translations aren't shipped yet, so every language plays the Spanish questions.
- **Code quality:** reviewed file by file (milestone 13, [`code-review.md`](code-review.md)); `npm run check` now also runs knip and ruff.
- **Next:** more content, screen polish, and the Steam release track (desktop build, store, release).

Milestones, plans and open tasks: `pm status` (`tasks.sql`); the older overview is [`plans/project.md`](plans/project.md). Top-level files and directories: [`directory.md`](directory.md).

## Getting started

You need [Nix](https://nixos.org/) with flakes. The dev shell has Node 22, Python 3, ruff, ImageMagick and Claude Code, plus Electron and the commands `trivia`, `trivia-desktop`, `trivia-desktop-build`, `trivia-authoring`, `qgen` and `trivia-media`, which run this checkout's scripts, Xvfb, `trivia-trailer`, on x86_64 Linux also `trivia-steam`, `trivia-release-check` and `steamcmd`, and `pm` ([project-manager](https://github.com/rubenmoor/project-manager)).

```sh
git clone https://github.com/rubenmoor/trivia.git && cd trivia
direnv allow             # once; the shell then loads whenever you cd in (without direnv: nix develop)
npm install
npm run build            # builds both web clients: the game and the authoring pages
claude plugin marketplace add DietrichGebert/ponytail && claude plugin install ponytail@ponytail --scope project   # once; Ponytail: off by default, `/ponytail lite` turns it on, pm workers on programming tasks get it (AGENTS.md)
```

Without Nix, Python 3 and Node 22 are enough to play: run `python3 app/server/main.py` instead of `trivia`, and `python3 authoring/server/main.py` instead of `trivia-authoring`.

## How to …

### Run the game

```sh
trivia                   # http://127.0.0.1:8000/   (--port, --host)
```

Open the page on the TV's browser and go fullscreen. Pick or type a player name, then the mode, the age group and the bundles, and play.

- `Esc` (or the menu button) opens the admin menu: skip, undo, restart, full screen and windowed mode, volume, joker budget, «Ajustes de la partida» (difficulty, bundles). It links to the review tool and stats while the authoring server runs.
- `M` (or the faint flag next to the menu button) flags the question for review: a dialog with an optional note, `Enter` flags, `Esc` cancels; on a flagged question it edits the note or unflags. The next start of `trivia-authoring` marks it «needs work» with the note; the menu's «Preguntas marcadas» lists the flags with «Copiar» for players without authoring tools.
- Game saves, seen counters (which questions a player has already seen) and flags live in `state/game.json`. Delete it to reset everything. An old `state/game.sqlite` + `flags.json` is migrated into it once at start; both stay as backups. A broken or newer `game.json` moves to `state/backup/` and the game starts fresh with a notice naming the backup.
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

#### Review in a separate worktree

`pm run` works in the main checkout and moves files it didn't stage, including your reviews and `qgen health ack`s, to a `pm/task-…-left` branch. No `git stash`, `--autostash` or checkout of `tasks.sql` in the main checkout while `pm run` runs (`pm stop` first): pm can overwrite `tasks.sql` with an empty schema meanwhile ([`plans/pm-tasks-sql-safety.md`](plans/pm-tasks-sql-safety.md)). Review in a second worktree instead, so pm never sees your edits:

```sh
# once
git worktree add ../trivia-review -b review
cd ../trivia-review && npm ci && npm run build

# each session, in ../trivia-review
git rebase main
TRIVIA_MEDIA=../trivia/media TRIVIA_STATE=../trivia/state TRIVIA_WORK=../trivia/work trivia-authoring
# afterwards
qgen validate && git add -A authoring/data app/data && git commit -m "Review …"
git -C ../trivia merge --ff-only review    # or rebase first if main moved
git -C ../trivia push
```

- The env vars share the main checkout's media cache, game flags and media candidates
- `../trivia/work` holds every run, pm workers' too: each pm work tree (`../trivia-worktrees/<name>`) has `work/` symlinked to it (AGENTS.md "Work trees"); a work tree with its own real `work/` hides its runs from the review tool (`/review?batch=…` shows 0 questions)
- `--ff-only` fails if `main` moved since: `git rebase main` in the worktree, then merge again

Also on the authoring server: stats at `/stats/categories`, `/stats/subcategories`, `/stats/difficulty` and `/stats/media`, and printable joker cards at `/comodines`.

### Make new questions

```sh
claude                   # log in once (Claude Code is in the dev shell)
qgen batch               # one new batch: concepts, drafts, rating, fact-check, revision, media
qgen batch --bundle colombia   # the same for another bundle's subcategories
qgen health ack <batch> "<note>"  # records the developer's look at a batch that failed the health thresholds (no stop either way, decision 414)
qgen rework              # every needs_work question with feedback once more: Claude fixes it, fact-checks, reviews (--batch <batch>)
qgen audit --backlog     # audit the next 200 approved questions from before D-56 (--slice N, --dry-run)
qgen tighten             # Claude reads the whole pool (approved too), shortens long-winded questions, fact-checks, reviews
qgen bundle new <id> --name … --description … --kind region|theme --rule …   # an empty bundle; then fill app/data/bundles/<id>/categories.json (region, theme: qgen taxonomy)
qgen taxonomy --bundle <id>    # a regional or theme bundle's categories and subcategories proposed (English slugs + en and own-language names; a theme's also `base_related`) → work/taxonomy/<id>/proposal.md
qgen taxonomy --bundle <id> --apply work/taxonomy/<id>/proposal.json   # writes them (proposal edited to the developer's answer): slugs to categories.json, missing en/es/de names drafted into names.<locale>.json
qgen remap --bundle <id> [--apply work/remap/<id>/proposal.json]   # its questions onto a new list: proposal → work/remap/<id>/proposal.md, then applied
```

Don't run the pipeline steps by hand; the batch command does it all and can be resumed. Details: [`authoring/RUNBOOK.md`](authoring/RUNBOOK.md). Afterwards, review the batch in the review tool.

`trivia-media fetch --batch <batch>` searches Commons for media candidates for questions that have none yet. The single pipeline steps (`qgen draft`, `rate`, `factcheck`, …, and `qgen import` for revising questions already in the pool) stay available for debugging; work files go to `work/<run>/`. See [`plans/07-question-generation.md`](plans/07-question-generation.md).

Media comes from Wikimedia Commons first, then NASA (space only) and Openverse (D-45, [`plans/23-media-providers.md`](plans/23-media-providers.md)); Freesound is out of the order before release (D-103). Keys go in `.env.local` (gitignored, loaded by direnv): `COMMONS_ACCESS_TOKEN` (an owner-only OAuth 2.0 consumer with basic rights on Meta-Wiki; higher Commons limits, IMG-15), `FREESOUND_API_KEY` (unused while Freesound is out of the order), and optionally `OPENVERSE_CLIENT_ID`/`OPENVERSE_CLIENT_SECRET` (Openverse works anonymously with 200 requests a day).

### Check the question pool

```sh
qgen validate            # checks the source pool, and that app/data/pool.json is its current export
qgen export              # rewrites app/data/pool.json and the packs' app/data/bundles/<id>/pool.json (the authoring server does this after every change); reload the game page
qgen report              # supply per level, difficulty and category; progress vs. targets (--bundle <id>, --player <name>, --subcategories, --calibration [<batch>…], --overlaps, --exit-check, --qc [<batch>], --cost, --review-time, --batches, --simulate; all: -h)
qgen patch-notes [<from-tag> [<to-tag>]]   # a content patch's counts-only notes + Steam event drafts (default: newest v* tag → working tree)
```

### Pull player reports

```sh
qgen flag --pull --dry-run   # what the report server holds, nothing written
qgen flag --pull             # reports → needs_work reviews, then acknowledged on the server
```

Players send a flagged question with «Enviar» in «Preguntas marcadas»; the game posts it to the report server (`reportUrl` in `app/desktop/package.json`; `--url` overrides it). The pull needs the server's pull token: `export TRIVIA_REPORT_TOKEN=…` (e.g. in `.env.local`) or write it to `state/report-token` (gitignored); never commit it. Each report becomes a `needs_work` review with the feedback «Reporte de jugador (…)» in `/review?status=needs_work`; reports in `en`/`de` go to that translation. Pulled ids are kept in `state/reports-pulled.json`, so a repeated pull adds nothing; mod questions and unknown ids are skipped and acknowledged. Then `qgen rework` picks them up.

### Run the report server locally

```sh
trivia-report-server dev     # 127.0.0.1:8787, local D1, migrations applied, prints the dev pull token
```

Fake tickets `dev-<anything>` work only here (`dev-invalid` → 401, `dev-steamdown` → 502). Point the shell at it with `TRIVIA_DEV_STEAM_USER=1 TRIVIA_REPORT_URL=http://127.0.0.1:8787`, and `qgen flag --pull --url http://127.0.0.1:8787` with the printed token. `--test-scheduled` after `dev` enables the cron at `/__scheduled`.

### Deploy the report server, rotate secrets

Developer only, needs `wrangler login` (Cloudflare account). The live URL is `reportUrl` in `app/desktop/package.json`.

```sh
trivia-report-server deploy            # migrations (remote), then the Worker
trivia-report-server secret STEAM_WEB_API_KEY   # publisher Web API key; also PULL_TOKEN, HASH_SALT
trivia-report-server tail              # live errors, no bodies
curl "$(jq -r .reportUrl app/desktop/package.json)/health"   # {"ok":true,"api":1}
```

- `STEAM_APP_ID` in `report-server/wrangler.toml` must hold the App ID (`authoring/steam/steam.json`), else every report → 502 (copy fallback).
- `PULL_TOKEN` (`openssl rand -base64 32 | tr '+/' '-_' | tr -d '='`): new secret, then the same value in `state/report-token` or `TRIVIA_REPORT_TOKEN`.
- `HASH_SALT` (`openssl rand -hex 32`): rotating only resets today's per-user counts.
- Kill switch: `REPORTS_OPEN = "0"` in `wrangler.toml`, then deploy.

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
npm run check                                      # type-check both clients (strict tsconfig flags) + on-screen literals + knip (unused exports, files, deps; knip.jsonc) + ruff (Python, ruff.toml)
npm test                                           # game engine tests (node:test)
npm run check:literals -w app/client               # on-screen literals outside the UI catalog (src/game by default)
npm run build -w app/client && trivia-desktop      # the game in the Electron desktop shell, no Python (no Steam: nothing saved; TRIVIA_DEV_STEAM_USER=1: state/desktop/dev/game.json; `--rp-probe`: throw-away Remote Play probe, log in `<userData>/rp-probe.log`, plan 168; `--lag-probe`: throw-away input-lag probe page, log in `<userData>/lag-probe.log`, plan 170)
TRIVIA_DEMO=1 npm run dev -w app/client            # the demo client (also `serve`, which previews dist-demo/ after `TRIVIA_DEMO=1 npm run build -w app/client`)
TRIVIA_DEMO=1 npm run build -w app/client && TRIVIA_DEMO=1 trivia-desktop   # the demo in the desktop shell (see "Run the demo")
```

The dev servers forward the Python servers' routes (`/api`, `/data`, `/media`; authoring also `/reports`), so run both. Before changing anything: milestones, plans, tasks and decisions are in `pm` (`pm status`, `pm decision list --answered`; [`AGENTS.md`](AGENTS.md)); older plans and D-numbers in [`plans/README.md`](plans/README.md), [`plans/decisions.md`](plans/decisions.md).

Environment variables (empty = unset):
- `TRIVIA_STATE`, `TRIVIA_MEDIA`: save folder and media cache (default `state/`, `media/`; packaged: `$XDG_DATA_HOME/trivia/`)
- `TRIVIA_WORK`: the pipeline's `work/` folder (authoring tools)
- `TRIVIA_SAVE_DIR`: the desktop shell's save folder
- `TRIVIA_DEVTOOLS=1`: the desktop shell allows its built-in devtools (`webPreferences.devTools`); nothing opens them (no menu, no shortcut); to inspect the page: `--remote-debugging-port=9222` + `chrome://inspect`, works without this variable
- `TRIVIA_STEAM_APPID`: the desktop shell's Steam App ID in dev (a Steam launch's `SteamAppId` wins; default 480)
- `TRIVIA_DEV_STEAM_USER=1`: the desktop shell counts as a valid Steam user without Steam (saves and flags on; dev runs and checks only, decision 111); also dev mode: Esc menu row «Ir a pregunta…» (question id or number → that question on screen)
- `TRIVIA_STEAM_SDK`: Steamworks SDK libs (set by the flake)
- `TRIVIA_STEAM_ACCOUNT`: `trivia-steam upload`'s Steam login; `TRIVIA_STEAMCMD_HOME`: SteamCMD's home (default `$XDG_DATA_HOME/trivia/steamcmd`)
- `VITE_AUTHORING_URL` (build time): the game's links to the authoring pages; `""` hides them (default: same host, port 8001)

### Run the demo

The demo is the same code built with `TRIVIA_DEMO=1` (decisions 335, 338): build-time flag, no runtime toggle. Dev: `TRIVIA_DEMO=1 npm run dev -w app/client` (prints `trivia dev: demo`), or build `dist-demo/` and start `TRIVIA_DEMO=1 trivia-desktop` (without `dist-demo/` it exits, saying so).
- In the demo: window title «¡Trivia! Demo», Steam App ID 480 until the demo app exists
- Off in the demo (decisions 337, 346): mods and Workshop (`--check-mod`, `--publish-mod` exit 2), achievements, telemetry, question reports
- Save: shared with the full game, same folder, mods file and single-instance lock (decisions 336, 345)

### Check the UI wording (screen gallery)

```sh
trivia-gallery                                  # every screen and dialog in en, es, es-ES, de (~15 min)
trivia-gallery --locale de --only menu-gamemaster,victory   # some shots again; --list names them
trivia-gallery --locale es --only start --size 1280x800   # another window size
trivia-gallery --set task-1463 --only join-5,join-8 --size 1920x1080,1280x800 --note "…"   # review set
```

Shots go to `work/gallery/<locale>/<shot>.png` (another `--size`: `<locale>@<W>x<H>/`, its own entry in `/gallery`); `work/gallery/manifest.json` has each visible text with its catalog key, and text without one (a literal) as unmatched. The game runs from demo saves in a temp folder, never your save. `trivia-gallery --demo` (or `TRIVIA_DEMO=1`) shoots the demo client (`dist-demo/`, built if stale) into `work/gallery-demo/`: only the demo's own shots (`--list --demo`: start screens, Esc menu on Start, bundles, level, game settings; saves built from the demo pool; PLACEHOLDER texts it sees are listed in the manifest and on the page). Review at `/gallery?demo`, a review set at `/gallery?demo&set=<name>`; flags there are marked demo and kept apart from the full gallery's.

Review them in `trivia-authoring` → `/gallery`: per language every shot; click a text for its catalog key, flag it with a note. Flags go to `authoring/data/ui-flags.json` for the next fix pass.

A review set holds only the shots a change touched, for quick feedback: `--set task-<id>` (the task asking for review) shoots just `--only`'s shots, all four languages at 1920×1080 unless `--locale`/`--size` say otherwise, into `work/gallery/sets/<name>/` and `sets/<name>.json` (same name again overwrites; the full gallery stays as it is). Review it at `/gallery?set=<name>`: only its shots, arrows step through them, flags as usual. A review decision links its set, never a full run (decision 352).

### Store trailer

```sh
npm run build && trivia-media sync --status approved   # first
trivia-trailer --lang es,es-ES                          # ~1 min per language
```

A scripted game in the desktop shell under Xvfb, its sound through a private PulseAudio sink, recorded with ffmpeg and cut to ≈20 s: `authoring/store/out/trailer/<lang>.mp4`. Made-up players in a temp save folder, never your save; your desktop's sound server isn't touched. en/de refuse until their question pools exist.

### Build the packaged game

```sh
nix build .#app && result/bin/trivia
```

The package contains only `app/`. It keeps its saves and media cache in `$XDG_DATA_HOME/trivia/` instead of the checkout; `TRIVIA_STATE` and `TRIVIA_MEDIA` override both locations. The packaged cache starts empty and the game never downloads: run it with `TRIVIA_MEDIA` pointing at a synced cache (e.g. `TRIVIA_MEDIA=$PWD/media result/bin/trivia`).

### Build the desktop game

```sh
trivia-media sync --status approved   # the pool's media must be in the cache
trivia-desktop-build                  # → app/desktop/release/LivingRoomTrivia-<version>-win-x64.zip, …-linux-x64.tar.gz
trivia-desktop-build --dir            # also win-unpacked/, linux-unpacked/ for the Steam depots
trivia-desktop-build --dir --demo    # the demo: app/desktop/release/demo/LivingRoomTriviaDemo-<version>-…, `demo: true` in its package.json (`--demo` without `--dir`: archives only)
trivia-steam stage                    # stages build/dlc/<pack>/; depot folders + build/media + DLC = the archives
```

Before every Steam upload, on a clean, tagged commit: `trivia-release-check` (~15 min; per-commit checks, licences, release quality bar, `nix build .#app`, both desktop builds, the report server's `/health` at the build's `reportUrl` (`--skip report` until it is set up), a smoke game in `linux-unpacked` and one with the shipped example mods, then asks the manual checklist). Exit 1 on any ✗; `--skip <step>` for a known-broken step, `--manual <file>` for answers (`<row>: y|n|note` per line). Report: `work/steam/<tag>/release-check.md`.
The demo has its own check, `trivia-release-check --demo`, on the same tagged commit: `tag`, `checks`, `licenses`, `desktop` (`--dir --demo` build and `trivia-steam stage --demo`), `media-budget`, `credits`, `smoke` and `determinism` (two demo smoke runs whose `--trace` files must be identical; ✗ names the first difference), `multiplayer`, `matrix` (`smoke.mjs --demo --matrix` twice side by side: every built mode × age group to a win and a loss, traces equal; ~40 min); manual rows `offline`, `windows`, `sound`, `cloud`, `start-line`, `signoff`; report in `work/steam/<tag>/demo/release-check.{md,json}`; `--skip`, `--manual` as the full check (`trivia-steam upload --demo` comes with plan 177).

Each artefact (~2.5 GB) holds the game, the data and the pool's media, and plays offline. Unpack it and start `LivingRoomTrivia.exe` (Windows; SmartScreen: «More info → Run anyway») or `./living-room-trivia` (Linux, Steam Deck). The first build downloads Electron for both platforms; later builds run offline. Outside Nix: `npm ci --prefix app/desktop && npm run dist --prefix app/desktop`.

### Send a content patch

Steps, rules and the Steamworks part: [`plans/11-steam.md`](plans/11-steam.md) "Content updates (ST-5)".

```sh
qgen flag --pull && qgen export && qgen validate
qgen patch-notes                                   # draft: newest v* tag → working tree
# bump version in app/desktop/package.json (patch; minor on a save change), per-commit checks, commit
git tag v<x> && qgen patch-notes v<prev> v<x>      # → work/steam/v<x>/patch-notes.md
trivia-steam upload --branch beta                  # then the manual rows on beta, then default by hand in Steamworks
trivia-steam upload --demo --branch beta           # the demo app, same commit and tag: its release check, steam.json `demo` IDs, work/steam/<tag>/demo/
```

### Mod the game

Question bundles, themes, rules tweaks and full conversions, shared on the Steam Workshop: the modding guide [`modding/README.md`](modding/README.md), with example mods in [`modding/examples/`](modding/examples/).

### Update dependencies

- `nix flake update` updates Node, Python, ImageMagick, Claude Code and `pm` (`flake.lock`); `direnv reload` after editing `flake.nix`.
- After changing `package-lock.json`, update `npmDepsHash` in `flake.nix` (`nix run nixpkgs#prefetch-npm-deps -- package-lock.json`).

## License

The code is MIT, the questions are not; media, fonts and sounds keep their own licences (D-102).
- Code, `modding/`: MIT, [`LICENSE`](LICENSE)
- Questions (`authoring/data/`, `app/data/`): all rights reserved, personal non-commercial play allowed, [`LICENSE-content.md`](LICENSE-content.md)
- Media, fonts, sounds: per file, `CREDITS.md` in the build
