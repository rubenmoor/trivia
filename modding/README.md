# Modding guide

Mods change the game: new question bundles, a new look, changed rules, or a whole different game. A mod is a folder of files that the game lays over its own files: where your mod has a file at the same path as ours, the game uses yours; everything else falls through to ours. Mods can also run JavaScript in the game's page through a small API, `window.trivia`. You share mods on the Steam Workshop or as folders. This guide covers everything a modder needs; the examples in [`examples/`](examples/) and the bundle template in [`template-bundle/`](template-bundle/) load as they are. No stability promise: any game update may break mods.

## Quick start
- Mods need the Steam version with a signed-in Steam user
- Local mods folder (the game creates it at start):
  - Windows: `%APPDATA%\trivia\mods`
  - Linux, Steam Deck: `~/.config/trivia/mods` (`$XDG_CONFIG_HOME/trivia/mods`)
  - Override: environment variable `TRIVIA_MODS_DIR=<folder>`
- Copy an example folder into it, e.g. `examples/theme/` → `~/.config/trivia/mods/theme/`
  - Examples ship in the game's install folder under `modding/` (Steam: Manage → Browse local files)
- Start the game → «Mods» on the start screen (also in the Esc menu)
- Turn the mod on → «Allow mods?» notice (once per machine) → «Allow mods»
- «Restart to apply»: mods load at start only
- Check a folder without starting the game: `trivia --check-mod <folder>` (below)

## Mod format
- A mod = a folder with `mod.json` at its root, plus any files
- `mod.json` fields:
  - `id` (required): `a-z`, `0-9`, `-`, 2–64 characters, starts with a letter or digit; the key everywhere (settings, question ids, Workshop)
  - `name` (required): 1–80 characters
  - `description` (required): up to 2000 characters (may be empty)
  - `version` (required): your version, 1–32 characters, e.g. `1.0.0`
  - `game` (required): the game version you made it for, `x.y.z`, e.g. `0.1.0`; another version only warns
  - `languages`: UI languages your mod has text for, from `es`, `es-ES`, `en`, `de`
  - `entry`: a `.js` or `.mjs` file inside the mod: makes it a code add-on
  - `kind`: any of `bundle`, `theme`, `code`, `conversion`; left out → derived:
    - `data/bundles/` or `data/bundles.json` → `bundle`
    - any `.css` → `theme`
    - `entry` → `code`
    - root `index.html` → `conversion`
  - `workshopId`: written by `--publish-mod`; don't write it yourself
- Limits: `mod.json` ≤ 64 KB, UTF-8; `entry` must exist inside the mod (symlinks resolved)
- Errors (mod not loaded; mods screen «Invalid: …»):
  - `not_a_folder`, `no_manifest` (no `mod.json`), `bad_json` (unreadable, not an object, too big)
  - `bad_field` + field name: the first field that breaks the rules above
  - `entry_missing`: `entry` file not found inside the mod
  - `duplicate_id`: another mod has the same `id` (see "Sources and load order")
- Warnings (mod still loads):
  - `game_version`: made for another game version
  - `unknown_key`, `unknown_language`: a field or language tag the game doesn't know
  - `bundle_json`, `bundle_row`: `data/bundles.json` unreadable, a bundle row skipped
  - `needs_update`, `workshop_id_mismatch`: Workshop only (below)
  - `load_failed`, `setup_failed`, `timeout`, `hook_failed`: code add-ons (below)
- Check: `trivia --check-mod <folder>` (Windows: `Trivia.exe --check-mod <folder>`)
  - Same checks as the game's loader, plus every bundle question; no Steam, no window, no restart
  - Prints errors and warnings with their codes, dropped questions with reasons, ends with "loads as is" or "N error(s)"
  - Exit 0 ok, 1 errors, 2 usage; Windows: also `<folder>-check.log` beside the folder and a message box
- JSON Schema for editors; the game's validator (`readManifest` in `app/desktop/mods.mjs`) is the source of truth:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "mod.json",
  "type": "object",
  "required": ["id", "name", "description", "version", "game"],
  "properties": {
    "id": { "type": "string", "pattern": "^[a-z0-9][a-z0-9-]{1,63}$" },
    "name": { "type": "string", "minLength": 1, "maxLength": 80 },
    "description": { "type": "string", "maxLength": 2000 },
    "version": { "type": "string", "minLength": 1, "maxLength": 32 },
    "game": { "type": "string", "pattern": "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)$" },
    "languages": { "type": "array", "items": { "type": "string", "enum": ["es", "es-ES", "en", "de"] } },
    "entry": { "type": "string", "pattern": "\\.m?js$" },
    "kind": {
      "type": "array",
      "uniqueItems": true,
      "items": { "enum": ["bundle", "theme", "code", "conversion"] }
    },
    "workshopId": { "type": "string", "pattern": "^[1-9][0-9]{0,19}$" }
  }
}
```

## Sources and load order
- Two sources:
  - Local folder (Quick start): each direct subfolder with a `mod.json` is a mod
  - Steam Workshop: every subscribed item; Steam downloads it, the game only reads it
- Workshop items:
  - Subscribing turns the mod on (appended at the bottom of the load order)
  - Still downloading → listed «Downloading in Steam», loads next start
  - Updated while the game runs → restart; `needs_update`: an update is pending, the installed files load
  - `workshop_id_mismatch`: `mod.json`'s `workshopId` names another item; still loads
- Same `id` twice: local wins over Workshop; two Workshop items: the lower item id wins; the other is `duplicate_id`
  - So a local copy of your published mod shadows the Workshop one while you work on it
- Settings per machine (not in Steam Cloud): `mods.json` beside the mods folder (`%APPDATA%\trivia\mods.json`, `~/.config/trivia/mods.json`)
  - One ordered list = load order; top wins
  - New mods appended at the bottom, on (off until you allowed mods once)
  - Removed mods stay in the list until you remove them
- Changes apply on the next start

## Overlay rules
- URL ↔ file: the game is `app://trivia/`; `app://trivia/<path>` → `<your mod>/<path>`
- First hit wins, top mod first, our files last; whole files only, no merging (except bundles, "Player bundles")
- Paths are case-sensitive on every OS: match our case exactly
- Our build: one file per source module, unminified, no hashes, source maps; names (source `app/client/src/` → URL):
  - `lib/data.ts` → `lib/data.js`
  - `game/Game.svelte` → `game/Game.svelte.js`; its CSS → `game/Game.svelte.css`
  - `game/sound.svelte.ts` → `game/sound.svelte.js`
  - Global CSS keeps its path: `app.css`, `game/theme.css` (colour variables)
  - Svelte runtime: one file `vendor/svelte.js`; other libraries under `vendor/`; build helpers under `_virtual/`
  - `fonts/`, `audio/` as they are
- Screens: `game/screens/*.svelte.js` (one per full screen), the question screen's parts `game/question/*`
- Scoped CSS classes: `svelte-<component path>`, e.g. `svelte-game-hud` for `game/Hud.svelte`; stable across our CSS changes
- Two ways to theme:
  - Root `style.css` (linked after ours, top mod's wins): add rules, override variables; survives our updates ([`examples/theme/`](examples/theme/))
  - Replace `game/theme.css` by path: a copy of our file; every update that changes ours keeps your old copy, and new variables go missing
- Full conversion: your own `index.html` replaces ours; your files load, everything you don't have falls through to ours (e.g. `/fonts/baloo-2.woff2`, [`examples/conversion/`](examples/conversion/))
- Not overridable:
  - `/mods.js`, `/mods/` (the game's own), `/media`
  - `/data/` (our questions and settings), except bundles ("Player bundles")
  - Your mod's `mod.json`, its `entry` file and its root `style.css`: served only under `/mods/<id>/`, never in place of ours (your `entry: "main.js"` doesn't replace our `/main.js`)
  - Values built into files (the version), the preload list inside `main.js`
- Seeing our source:
  - The public repo at the game's version tag: `https://github.com/rubenmoor/trivia/tree/v<version>/app/client/src` (version: Credits screen)
  - The installed files: `resources/client/` in the install folder, with source maps
  - Devtools (no shortcut in the game): start the game with `--remote-debugging-port=9222` (Steam: Properties → Launch options), then open `chrome://inspect` in Chrome or Chromium; under "Remote Target" (`localhost:9222`, else "Configure..." → add it) click "inspect" on `app://trivia/`
  - Only while you mod: anything on your PC can control the game through that port

## Code add-ons
- `mod.json` `"entry": "main.js"` (any path inside the mod); the entry is an ES module:

```js
export default async function setup(trivia) {
  trivia.on("game:end", ({ result }) => console.log(trivia.mod.id, result));
}
```

- Runs before the game loads its save, data and language; the game mounts after every mod's `setup`
- Root `style.css`: linked automatically, no `entry` needed
- Run order: bottom of the load order first, top last; hooks run in that order; for screens the top mod wins
- Relative imports and `import.meta.url` stay in your folder (`/mods/<id>/…`)
- Errors (on the mods screen, and in the console):
  - `load_failed`: the entry didn't import
  - `setup_failed`: `setup` threw
  - `timeout`: `setup` (with its import) took over 5 s
  - These three remove all of the mod's hooks for this run; the next mod loads, the game always starts
  - `hook_failed`: a hook threw later; that hook is dropped for the run, the game goes on without it
- `trivia` in `setup` is scoped to your mod; `window.trivia` is the same API without `mod`
- Every member returns an `off()` where it registers something:
  - `version`: the game version, `if (trivia.version !== "0.1.0") return;`
  - `mods`: loaded mods `{ id, name, version }[]`, `trivia.mods.some((m) => m.id === "other-mod")`
  - `mod`: your mod, `trivia.mod.id`
  - `modules`: our modules, same instances as by path, read-only:
    - `api` (`lib/api.js`), `engine` (`read`, `run`), `game` (`engine/game.js`), `i18n` (`t`, `lang`, `fill`), `input` (`pushScope`, `lastDevice`), `sound` (`sfx`, `music`), `svelte` (`mount`, `unmount`, `flushSync`)
    - `trivia.modules.i18n.t("mods.title")`
  - `data(fn)`: per language load, on a copy of `{ locale, questions, bundles, ageGroups }`; change it in place or return replacements; sync only
    - `trivia.data((d) => ({ questions: d.questions.filter((q) => q.difficulty <= 10) }))`
  - `actions.before(fn)`: before every game action and joker, on a copy of its body; the engine still checks it
    - `trivia.actions.before((action, body) => { if (action === "new") body.jokers = { ...body.jokers, hint: 4 }; })`
  - `actions.after(fn)`: after every action, a copy of the game (may be null)
    - `trivia.actions.after((action, game) => console.log(action, game?.level))`
  - `i18n.add(locale, catalog, opts?)`: deep-merged over a UI language (`es-ES` is its own), or a new UI language on `opts.base` (default `en`) with `opts.endonym`; questions stay in our languages; call in `setup`
    - `trivia.i18n.add("en", { mods: { title: "Add-ons" } })`
  - `screens.replace(name, component)`: a compiled Svelte component instead of our screen, same props
    - `trivia.screens.replace("Victory", MyVictory)`
  - `screens.dom(name, render)`: plain DOM instead of our screen; `render(el, props)` may return a cleanup
    - `trivia.screens.dom("Correct", (el, props) => { el.textContent = "Right!"; })`
  - Screen names: `Start`, `Language`, `Player`, `Choice`, `Level`, `Select`, `Question`, `Correct`, `Wrong`, `Victory`
  - `screens.show(render)` → `{ close() }`: a full-screen layer over the game with its own input; Esc, pad B or `props.close` close it
    - `const layer = trivia.screens.show((el, props) => { el.textContent = "Paused"; });`
  - `menu.add({ label, onselect })`: a row in the Esc menu; `label` shown as is
    - `trivia.menu.add({ label: "Plum mode", onselect: () => document.body.classList.toggle("plum") })`
  - `on(event, fn)`: payloads are copies, return values ignored
    - `ready`, `screen` `{ name }`, `game:start` `{ game }`, `game:end` `{ game, result }`, `question:shown` `{ id, level }`, `question:answered` `{ id, level, index, correct }`
    - `trivia.on("question:answered", ({ correct }) => correct && trivia.modules.sound.sfx("applause"))`
  - `css(href)`: one more stylesheet after ours
    - `trivia.css(new URL("./extra.css", import.meta.url))`
- Importing our modules by path: `import { t } from "/lib/i18n.js";` (same instances; exports read-only)
- Svelte components: compile against our runtime and import `/vendor/svelte.js`, never your own copy of Svelte
- `window.triviaShell`: the desktop shell's bridge; reachable, but ours, without any promise; conversions use `quit()` and `mods.ready()` (below)

## Mods screen and safe start
- «Mods»: start screen and Esc menu; only in the Steam version
- Per mod: name, source («Local folder» or «Steam Workshop · <id>»), kind, languages, state, warnings, folder
- Turn on/off, move up/down (↑/↓ rows, ←/→ to ▲▼, LB/RB move the row), «All off», «Refresh»; Esc or pad B back
- Changes save at once and apply after «Restart to apply»
- One-time notice «Allow mods?» before the first mod turns on: mods run code with the game's access (save, Steam achievements, Steam features); until then found mods stay off
- Safe start:
  - A start with mods that doesn't finish (crash, hang, closed early) → the next start runs without mods and says so on the mods screen
  - Fix or turn off the mod, then restart
  - Manual: `--no-mods` in Steam (game → Properties → Launch options); remove it to get mods back
- A start counts as finished when our game is up, or when the page still answers 20 s after loading
  - Full conversions: call `window.triviaShell.mods.ready()` once your game runs, so a later crash isn't blamed on the start

## Player bundles
- Question bundles in our own format: [`bundles.md`](bundles.md) (format), [`template-bundle/`](template-bundle/) (15 questions to copy), [`bundle-prompt.md`](bundle-prompt.md) (prompt for your own AI)
- Files: `data/bundles.json` (one row per bundle) and `data/bundles/<bundle>/` (`categories.json`, `pool.json`, `pool.<locale>.json`, pictures inside)
- Add-on bundle (any `kind` but `base`): off by default, players switch it on before a game
- Base bundle (`kind: "base"`): a second choice beside ours; ours stays the default
- Ids become `<mod id>:<id>` in the game (bundles and questions), so they never clash with ours
- Shown as «Player-made · <mod name>» in the bundle selector; media credits from your questions' `credit` and `source_url` on the Credits screen
- Never in our question pool, our seen counts, our question reports or telemetry; the flag action is hidden on player questions
- Check every question: `trivia --check-mod <folder>`

## Achievements, flags and telemetry with mods
- Steam achievements: unlock with mods on, as without
  - Player questions count like ours, except the bundle achievements (our regional bundles) and «all categories» (our base bundle)
- Flags and question reports: our questions only; hidden on player questions
- Telemetry (opt-in): answers to our questions only; a game notes that mods were on

## Publishing
- `trivia --publish-mod <folder> [--changenote <text>] [--visibility public|friends|unlisted|private] [--content-only] [--dry-run]`
  - Run from a terminal, Steam client running and logged in (the game may be closed); Windows: `Trivia.exe` in the install folder
  - The game only reads and copies the folder; Steam uploads it
- First: `--dry-run` (no Steam needed): item id or "new", title, description length, visibility, tags, preview, file count and size
- Steps: checks `mod.json` (errors stop, `--check-mod`'s findings become warnings) → copies the folder without dot files and dot folders (`.git`) → uploads
- Preview: `preview.png`, `.jpg` or `.gif` at the root, ≤ 1 MB; none → Steam's placeholder
- First publish:
  - Creates the item, writes `workshopId` into your `mod.json`, prints the item URL
  - Private by default; `--visibility public` when you're ready
  - Accept the Workshop legal agreement once: `https://steamcommunity.com/sharedfiles/workshoplegalagreement` (until then the item stays hidden)
- Updates: same command; uploads files, title (`name`), description, tags and preview
  - `--content-only`: files only
  - `--changenote "…"`: the change note on the item page
  - Visibility changes only with `--visibility`
- `workshopId`: keep it in `mod.json` (the next publish updates that item); delete it for a new item; a failed first publish keeps it (the next run fills the empty item)
- Tags: from `kind` and `languages` (`bundle`, `theme`, `code`, `conversion`, `es`, `en`, `de`)
- Only the item's owner can update it
- Windows: no console; output goes to `<id>-publish.log` beside the mod folder, the result to a message box
- Exit 0 ok, 1 failed, 2 usage

## Rules
- Page only: mod code runs only in the game's page (sandboxed), never in the desktop shell; a mod that needs something native: open an issue at `https://github.com/rubenmoor/trivia/issues`, we may add it
- Offline: the game's page has no network; mod code can't load or send anything online
- No stability promise: module paths, file names, `window.trivia` and the bundle format may change with any update; renames go into the patch notes
- Licence: the game's code and everything in `modding/` (guide, examples, template) are MIT: copy freely; our questions are not (all rights reserved): don't copy them into your mods

## Examples
- [`template-bundle/`](template-bundle/): a question bundle, 15 questions about the solar system (es, en)
- [`examples/theme/`](examples/theme/): a plum palette by root `style.css`, colour variables and one component class
- [`examples/rules-tweak/`](examples/rules-tweak/): one more hint per game with `actions.before`, `i18n.add`, `on("game:end")`
- [`examples/conversion/`](examples/conversion/): a full conversion, guess the number, with our fonts; Esc or pad B quits
