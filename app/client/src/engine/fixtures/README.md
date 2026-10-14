# Engine parity fixtures (PORT-1)

Recorded output of the Python referee (`app/server/game.py` + `selection.py`, deleted in PORT-8), played through scripted and random games on synthetic data. The TS engine (PORT-2 `selection.ts`, PORT-3 `game.ts`) replays them and must match exactly. Written by `authoring/tools/record_fixtures.py` (plan 18); don't edit by hand.

## Frozen (plan 51)
The referee and the recorder are gone; the fixtures stay as they are and `npm test` keeps replaying them.
- Recorded from the Python referee up to commit `c3b683f16f5fb191c476aec0765fd368fe1a0fef`
- To re-record: check out that commit, run `python3 authoring/tools/record_fixtures.py` (`--check`: diff only), copy the fixtures back
- Bundle-scoped keys (D-100): `game.test.ts` sends recorded subcategory names as keys and compares bodies and saves without `key`s and with bare names

## Files
Synthetic categories and pools, never the real pool; the replays take bundles and age groups from the real `app/data/` (`young_teens` = D-22, pinned in `pool.test.ts`).
- `categories.json`: `categories.load()` output (with `bundle`); 2 bundles (`base`, `colombia`), 3 broad categories, 6 subcategories
- `pools/main.json`, `pools/tight.json`: `{"questions": [...]}`, `pool.json` entries
  - `main`: several games per player, with jokers
  - `tight`: exactly the 48 cards of one game; no replacement ever fits (Bájale, Cambiazo, purge, snipe hit), a player's second game fails the supply check
- `selection.json`: direct `selection.py` calls, `[{name, fn, args, tape, result}]`
  - `fn` ∈ `in_range`, `assign`, `supply`, `draw`; fresh DB + seed per case
  - `args.pool`: pool name (`none` = empty); `without`: IDs removed from it
  - `supply`: `players` (IDs 1.., in order) and `burns` (`player` null = global, game 1) written first; `player` = whose burns count
  - `draw`: `keep` (IDs from the pool), `n` (default 4), `avoid_categories`, `category_of: "broad"` (broad category instead of subcategory); `result` IDs or null (unfillable)
- `game/<scenario>.json`: `{name, about, seed, pool, steps}`

## Game steps
One step = one HTTP request, recorded as `main.py` answers it.
- `{now, pool, call, args, tape, response: {status, body}, db}`
- `pool`: the pool for this step; a scenario may switch pools, always right before a `new`
- `call` ∈ `get_game` (`player`), `players`, `new` (`player`), `pick` (`index`), `answer` (`index`), `skip` (`everyone`), `undo`, `abandon`, `jokers` (`jokers`: budget), `joker` (`joker`, optional `purge`/`subcategory`/`index`), `delete_player` (`name`)
- `response`:
  - action ok: `200 {"game": view}`, `joker` adds `"event"`
  - `get_game`: `200 {"game", "supply"}`; error `400`
  - `players`, `delete_player`: `200 [players]`
  - error: `409 {"error": code, "params", "message", "supply"}` (D-57); compare `error`/`params`, not `message`
- `db`: full snapshot after the step
  - `players` `[{id, name, created_on}]` by id
  - `games` `[{id, started_on, finished_on, result, player_id, state}]` by id, `state` parsed
  - `burned` `[{question_id, player_id, game_id, burned_on}]` sorted by (game_id, question_id, player_id)
  - an error leaves it unchanged (rollback); the engine must do the same
  - `soak-<n>`: only on every 10th and the last step (size)
- IDs: SQLite gives max+1 after a delete; the `players` scenario pins it
- Save v3+ (plan 65): the engine stores `seen` rows and `blocked`, the recordings `burned`; `test/save.ts` compares those tables
  - `upgradeDb`: the recorded `db` through `parseSave`'s v2 → v3 upgrade; history outcome `admin_burn` → `admin_block`
  - `withoutOrphans`: GF-7 now keeps the player's seen rows (`game_id` 0), Python deleted the burns; compared without them
- Selection by seen count (plan 65): Python excluded burned questions, the engine offers them again, lowest count first; the recorder stays frozen (plan 51)
  - `game.test.ts` replays a scenario only up to the first step where a seen question of the step's pool could be offered again (a later game; undo after a swap); `get_game`'s player-scoped `supply` isn't compared once a seen question is in the pool
  - Retired that way: `supply` from step 7 (second game refused), the later games of `players`, `abandon`, `admin-skip`, the soaks; TS-native instead: the supply test in `game.test.ts`, `invariants.test.ts` (random counts 0–3), the sort test in `selection.test.ts`
  - `selection.json` `supply`/`draw` cases still match: their `burns` go in as `blocked`

## Time
- One fixed `now` per step: `2026-01-01T00:00:00` + step index minutes (`selection.json`: always the start)
- The engine takes `now` as a parameter, never reads the clock

## Shuffle tape (D-58)
All referee randomness is `random.shuffle`; the recorder replaces it and logs every call. No shared PRNG.
- Tape entry: `{"site", "n", "perm"}`
  - `n`: length of the shuffled list
  - `perm[j]`: old index of the element now at position j (`xs = perm.map(i => old[i])`)
  - `site`: name of the Python function that called `shuffle` (`draw`, `pick`, `swap_in`, `replacement`, …)
- Engine: injected `Rng` with `shuffle(xs, site?)`, in place
- Tests: `tapeRng(tape)` applies the perms in order and fails on
  - a wrong `n`
  - a `site` mismatch
  - a missing entry (more shuffles than recorded) or a leftover one (fewer)
- So shuffles must happen at the same points, in the same order, on arrays of the same length
  - including those inside `view` → `jokers_view` → `trial`: hint, skip, easier, snipe, skip+purge, then Cambiazo's `replacement` per subcategory in `categories.load()` order
- Production `rng.ts`: mulberry32 + Fisher–Yates

## Scenarios
Scripted ones pin one rule each; soak walks catch paths they miss.
- `win`, `lose-undo`, `hint`, `skip-purge`, `easier`, `category`, `snipe`, `budget`: rules and jokers; every joker has an available and an unavailable case
- `admin-skip`, `players`, `abandon`, `supply`, `errors`: players, admin skip, supply failures, errors
- `soak-1` … `soak-10`: seeded random walks of legal actions, 30–40 steps (choices from `random.Random("soak-<n>")`, not the tape); `soak-10` on `tight`
- Configure settings and gamemaster cheats (D-88), newer than the recordings: TS-native in `settings.test.ts` (synthetic pool)

## Notes for the port (parts 2/3)
- Python `sort` and JS `Array.prototype.sort` are both stable; keep the same sort keys (booleans: False < True)
- `casefold()` ≠ `toLowerCase()` in general; `players` pins the cases that matter («Íngrid»/«íngrid»)
- `players()` sorts by `coalesce(max(started_on), created_on) DESC`; scenarios avoid ties (distinct `now` per step)
- Python sets (`later_fill`, `asked_categories`) are only used for membership; their order doesn't matter
- Legacy SQLite schemas (pre-D-28, pre-JK-2) aren't here; the migration (PORT-5) reads them in Python
