# 12 — Client Engine (Python → TypeScript)

**Status:** draft

Milestone M7 in [`project.md`](project.md); the Steam plan ([11](11-steam.md)) builds on it. It moves the game referee from the Python server into TypeScript, so the game runs without Python: in the browser, in a desktop shell ([18](18-steam-integration.md)), on the Steam Deck. **The rules don't change and the family's saves are kept.** This is a pure engineering change and can start now.

## Today
History: the state before the port (D-28 burning, superseded by D-82 seen counters, plan 65).

- `app/server/game.py` (~550 lines): players, games (the state as JSON), burning per player and for everyone, draw, pick, answer, skip, undo, jokers (D-25..D-28).
- `app/server/selection.py` (~130 lines): supply check and draw via exact bipartite matching (GF-2).
- `app/server/categories.py`: loads `app/data/categories.json`.
- `app/server/main.py`: the `/api/game/*` and `/api/players*` routes, and also the authoring API (review tool, stats, media).
- State: `state/game.sqlite` (players, games, burned).
- The server is the referee: the client never sees the correct answer or unrevealed hints before they are played (D-25).

## Target

```mermaid
flowchart LR
  UI[Svelte screens] --> Engine[engine/ TS referee]
  Engine --> Store{{Store interface}}
  Store --> S1[ServerStore: Python, state/game.json]
  Store --> S2[FileStore: desktop shell, userData]
  Store --> S3[MemoryStore: tests, demo]
  Engine --> Pool[pool.json + categories.json, static]
```

- **`app/client/src/engine/`**: a pure TypeScript module with no DOM and no Svelte. It covers `selection.ts` (matching, supply), `game.ts` (state machine, jokers, seen events, undo; D-82), `pool.ts` (loading and filtering), `rng.ts` (a seedable PRNG). Every function takes the state and returns the new state, so undo and saves stay simple.
- **Engine runs under plain Node 22** (D-60): erasable TS only (no `enum`, `namespace`, parameter properties), relative imports with `.ts` extensions, no Vite-only imports. tsconfig: `erasableSyntaxOnly`, `allowImportingTsExtensions`. Authoring calls it via `node` for the supply check.
- **Store interface**: `load(): SaveData` / `save(SaveData)`. `SaveData` is one versioned JSON document that replaces the SQLite tables; save v3 (D-82, plan 65): `{version, players, games, seen, blocked, notified_exhausted, flags, reports, language?}`, v2 `burned` migrates in `parseSave`. `language` (D-86, no version bump): `{ui, questions}`, missing = `es`/`es`; `GameRow.locale` (non-es games only); `lib/engine.ts` `ready()` marks a save with no `language` as fresh, `language()` returns the options and `ask` (first-start screen). The data is small (seen rows, blocked IDs), so one document fits easily, and it suits Steam Cloud (one file) too.
- **`ServerStore`** (current game, until the Steam build replaces it, D-59): the Python server keeps a tiny `GET/PUT /api/save` that writes `state/game.json` atomically. No localStorage: D-3 rejected it as fragile.
- **Pool export** (done, D-35): `qgen export` writes the playable pool (`approved` only, without `review`, `quality` and pipeline fields) to `app/data/pool.json`. The TS engine loads that file; with locales (15b) it becomes one file per locale.
- **Data in the client** (pm plan 50, PORT-7): the server serves `app/data/` read-only at `/data/…`; the client loads pool and categories once per page load (reload after `qgen export`). `lib/api.ts` keeps its signatures and calls the engine + `ServerStore`.
- **Python game server after the port** (pm decision 4, D-59): static files plus `/api/save` only. Flags go into `SaveData`, categories are static files from `qgen export`, media is served from the synced cache only (no download on miss). The authoring API (review, stats, media fetch) stays in `trivia-authoring`. `app/server/game.py` and the game routes are deleted once parity holds.

## The referee question (D-66)
With the engine in the client, the correct answer is in memory before the players answer. Decided in D-66: acceptable for an offline party game, relaxes D-25. The UI still must never *render* hidden data: screens only render the view.

## Parity strategy
1. **Fixtures first (PORT-1):** before porting, write a scenario recorder for the Python engine. It plays scripted games (picks, answers, every joker, skip, burn for everyone (history, D-28), undo, supply failures) on a small fixed pool and stores the inputs and outputs as JSON in `app/client/src/engine/fixtures/`. Randomness is a recorded shuffle tape, not a shared PRNG (D-58): every `random.shuffle` is logged as `{site, n, perm}`; the TS engine takes an injected `Rng`, and tests replay the tape. Format: `fixtures/README.md`.
2. **Port module by module:** `selection` first (pure, easy to compare), then `game`.
3. **Fixture tests:** the TS engine replays every fixture and must produce the same states. Tests use Node's built-in `node:test` (no new dependency).
   - Errors (D-57): PORT-3 throws the same codes as `game.py` (`GameError(code, params)`); parity compares `error`/`params`, not `message`. Joker `reason`s too.
4. **Invariant tests:** for random seeds on the real pool, check that every level gets 4 cards, never a count-k card while a count-<k card fits the slot and keeps the later levels fillable (D-82; was "burned questions never come back"), and an available joker never breaks the supply.

## Migration
- `app/server/save.py` `migrate()` turns `state/game.sqlite` + `state/flags.json` into `state/game.json` once (players, games with the running one, burns per player and for everyone, flags; history: v2, the engine migrates v2 → v3 seen rows, D-82); runs on a copy, the `.sqlite` and `flags.json` stay as the backup (plan 49, D-67).
- Switch-over: `main.py` calls `save.migrate()` before `serve_forever` in PORT-7's switch-over change (plan 50), not earlier; until then `game.py` still writes `game.sqlite` and an early `game.json` would go stale.
- Rollback: delete `state/game.json`, go back to the commit before the switch; `game.sqlite` is untouched.
- v2 → v3 (D-82, plan 65): `parseSave` turns each `burned` row with a player into one `seen` row and `player_id: null` into `blocked`; `save.py` only checks the envelope (D-67). The Python referee `game.py` keeps its SQLite burn rules until plan 51 deletes it (divergence, D-82).
- `SaveData.version` makes later migrations possible (game modes in 13, multiple locales in 15).

## Tasks
- [x] PORT-1 Scenario recorder for `app/server/game.py` + `app/server/selection.py`; commit the fixtures. Done 2026-10-11 (plan 18): `authoring/tools/record_fixtures.py` (`--check`), fixtures + README in `app/client/src/engine/fixtures/`.
- [x] PORT-2 `engine/selection.ts`: supply check and draw (GF-2, D-25), fixture-tested.
  - 2026-10-11: `rng.ts`, `pool.ts`, `selection.ts`; every `selection.json` case replays with its tape used up; `invariants.test.ts`: 50 seeded 12-level walks on the real pool (plan 19).
- [x] PORT-3 `engine/game.ts`: state machine, players, burning, jokers, undo. Decision: the client holds the answer (relaxes D-25). *2026-10-11 (plan 20): `state.ts`, `pycompat.ts`, `game.ts`, `api.ts` (the `main.py` game routes); `game.test.ts` replays every `fixtures/game/*.json` (response, db, tape); D-66.*
- [x] PORT-4 Store interface; `ServerStore` + Python `GET/PUT /api/save` (atomic write, with a retry for Windows file locks); `MemoryStore` for tests. *2026-10-11 (plan 49): `app/server/save.py` + routes in `main.py`, `engine/save.ts`, `engine/store.ts` (`MemoryStore`), `lib/store.ts` (`ServerStore`), flags in the save (D-59, D-67); authoring reads it via `authoring/tools/save_file.py`.*
- [x] PORT-5 Migration `game.sqlite` → `game.json`, tested on a copy of the family's real save. *2026-10-11 (plan 49): `save.migrate()`, not wired into startup yet (see "Migration"); rehearsal on a copy: 2 players, 14 games (none running), 44 burns, 0 flags; players, burns per player and `getGame` (view + supply) equal in Python and TS; original checksum unchanged.*
- [x] PORT-6 `qgen.py export`: the playable pool for the client; `validate` checks that the export is current. *2026-10-07, pulled forward as LP-3 (`19-repo-layout.md`): `app/data/pool.json`; the Python game server reads it too.*
- [x] PORT-7 Switch the screens from `lib/api.ts` game calls to the engine. Family test night on the TS engine. *2026-10-12 (plan 50): `/data/` route in `main.py`, `lib/data.ts`, `lib/engine.ts`, `lib/api.ts` on the engine + `ServerStore`; `save.migrate()` at server start (D-69); test night played fine (pm decision 25).*
- [ ] PORT-8 Delete `app/server/game.py` and the game routes; `app/server/selection.py` goes too: `qgen report` and `authoring/server/overview.py` get the supply from the TS engine via `node` (D-60, pm decision 5). Update `01-architecture.md` and AGENTS.md.
