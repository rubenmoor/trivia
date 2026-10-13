# Code review (milestone 13)

This report collects the findings of the milestone 13 code review: every tracked code and build file in scope is read once, cheap fixes are made on the spot, and everything else becomes a follow-up task or a decision. Parts 1–11 follow `plan 72: masterplan`; each part appends its rows to its own section, and the inventory at the end maps every file to the part that reviews it.

## Executive summary

PLACEHOLDER(590)

## Format

Each part has one table with one row per finding; every file of the inventory ends up in at least one row.

- Columns: file | finding | category | severity | status
- Category: unused / practice / complexity / performance / bug / inconsistency
- Severity:
  - high: wrong behaviour, data loss, security or offline breakage reachable in play/authoring
  - medium: latent bug, real maintenance cost or measurable slowness
  - low: cosmetic, naming, small dead code
- Status: `fixed (task N)`, `handed to part N`, `follow-up task N`, `decision N`, `superseded by task N`, `won't fix: <why>`
- File reviewed without findings: one row, finding `no findings`, category/severity/status `—`
- Linter evidence: a TS/Svelte/`.mjs`/`.cjs` finding a lint rule or `tsconfig` flag would catch carries the rule in its finding text, e.g. `(lint: noUnusedLocals)`, `(lint: no-floating-promises)`; part 10 counts them
- Duplication candidates: both paths in the row, status `handed to part 10`
- Part 1 rows `handed to part N`: that part logs the final status in its own section, quoting the row

## Part 1: Baseline scans and report skeleton

Plan 73 runs cross-cutting scans over the whole inventory. Each scan adds its rows under a `### <scan>` sub-heading with the exact command; findings in another part's files get status `handed to part N`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 2: Python game server

Plan 74 reviews `app/server/` and `authoring/tools/categories.py`, and logs the referee files deleted by task 302.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 3: TS engine

Plan 75 reviews `app/client/src/engine/` with its tests and `test/` helpers, not the fixture JSON.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 4: Client lib, locales and boot

Plan 76 reviews `app/client/src/lib/`, `locales/`, `main.ts`, `App.svelte`, `app.css`, `vite-env.d.ts` and `scripts/check-literals.mjs`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 5: Game screens

Plan 77 reviews `app/client/src/game/`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 6: Desktop shell and packaging

Plan 78 reviews `app/desktop/` and the Steam release and store tooling in `authoring/steam/` and `authoring/store/`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 7: qgen

Plan 79 reviews `authoring/tools/qgen.py` section by section, then its module structure.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 8: Other authoring tools

Plan 80 reviews `authoring/tools/` minus `qgen.py`, `categories.py` and `prompts/`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 9: Authoring server and UI

Plan 81 reviews `authoring/server/` and `authoring/ui/`, sources and configs.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 10: Cross-cutting: duplication, consistency, build config

Plan 82 consolidates the duplication candidates of parts 2–9, checks naming and error handling across files, reviews the root and `app/client` build config and `app/client/credits.ts`, and checks `directory.md` and `AGENTS.md` against the code. The linter evaluation below ran early (task 616).

| file | finding | category | severity | status |
|---|---|---|---|---|

### Linter evaluation

Task 616 evaluated a linter for the TypeScript trees (`app/client/src`, `authoring/ui/src`, `app/desktop` `.mjs`/`.cjs`; 48 `.ts`, 34 `.svelte`, 6 desktop scripts, ~14.9k lines) on 2026-10-12. Parts 2–9 had logged no findings yet, so the evidence is the trial run alone: every diagnostic of every candidate was triaged by hand.

- Evidence from the report: none yet (no `(lint: …)` tags; part 1 scans not run) → re-check: `task 617: Re-check the linter evaluation against the findings of parts 2–9`.
- Trial: temp copy under `/tmp`, candidates installed there only, deleted afterwards.

| candidate | packages added (lockfile entries) | Svelte | type-aware | time | diagnostics | real bugs | noise |
|---|---|---|---|---|---|---|---|
| stricter `tsconfig` flags | 0 | script + markup (svelte-check) | yes | inside `npm run check` (~3 s each) | 2 (+ ~150 with `noUncheckedIndexedAccess`) | 0 | 2 style; `noUncheckedIndexedAccess`: almost all index-after-length-check |
| Biome 2.5 (recommended, Svelte full support) | 9 (1 + 8 per-platform binaries) | script + markup (experimental) | no | 0.2 s | 213 | 0 | 62 `useButtonType`, 5/5 `noUnusedVariables` false (`class:x` shorthand), 10 `noAssignInExpressions` (Svelte `() => (x = y)` idiom), 13 `useIterableCallbackReturn` (`forEach` arrows) |
| oxlint 1.87 (default `correctness`) | 20 (1 + per-platform bindings) | script only | no (needs `oxlint-tsgolint`, more packages) | 0.06 s | 2 (58 with `suspicious`) | 0 | ternary as statement (`Overlay.svelte:270`), control chars in `pycompat.ts:14` (on purpose: Python's whitespace set); `suspicious`: `no-shadow`, `no-array-sort`, function scoping |
| ESLint 10 + typescript-eslint (`recommendedTypeChecked`) + eslint-plugin-svelte | 132 | script + markup | yes | 6 s | 210 (+11 test files not in a tsconfig) | 0 | 104 `no-unsafe-*` (deliberate `any`/`unknown` at JSON and save parsing), 32 `no-floating-promises` + 7 `no-misused-promises` (fire-and-forget calls whose async functions catch their own errors), 7 `no-base-to-string` (`String(unknown)` in error messages), 8 `prefer-svelte-reactivity` (Sets non-reactive on purpose), 12 `require-each-key` (static lists) |

- Already clean before this task: `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `noImplicitOverride` (0 each); svelte-check reports them in `.svelte` script blocks too (probe checked).
- No candidate caught a bug. Example of what none catches: `authoring/ui/src/review/Review.svelte` `undo()` pops the undo stack before its `busy` check, so `u` pressed while saving drops that undo entry (logged below).
- Unused exports and files (the likeliest drift after worker refactors): none of the four candidates finds them; part 1's scan (`task 526: Scan: unused TS/JS code and npm dependencies`) does.
- `app/desktop` `.mjs`/`.cjs`: no `tsconfig` covers them; only the three linters see them, with 0 findings there.
- Not adopted: Biome, oxlint, ESLint. 0 bugs against 9–132 new packages (minimal-dependencies rule, `npmDepsHash`), and their noise comes from idioms this code uses on purpose. No decision needed.
- Adopted: `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `noImplicitReturns`, `noImplicitOverride` in both `tsconfig.json`s (`authoring/ui` type-checks `app/client/src` too).
  - The lint pass is `npm run check`, already in the pre-commit checks (AGENTS.md, D-73). `project-manager.toml` has no own worker prompt; workers follow AGENTS.md.
  - Existing issues: the 2 `noImplicitReturns` sites, fixed here (behaviour unchanged). No baseline and no follow-up fix task needed: the pass covers everything from the start.
- Not adopted: `noUncheckedIndexedAccess` (133 + 165 errors, almost all on already-checked indexes), `exactOptionalPropertyTypes`.
- `*.test.ts` and `engine/test/` are excluded from both `tsconfig`s, so the flags (and type-checking) don't reach them: task 586 (plan 82 task 7) checks this.

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/src/game/Question.svelte` | `press()` and `aim()` return `fire(…)`'s promise from a `void` function (lint: noImplicitReturns) | practice | low | fixed (task 616): `return void fire(…)` |
| `app/client/tsconfig.json`, `authoring/ui/tsconfig.json` | no unused/fallthrough/implicit-return checks | practice | low | fixed (task 616): five flags |
| `authoring/ui/src/review/Review.svelte` | `undo()` pops `undoStack` before `if (!last \|\| busy) return`: an undo pressed while busy is lost | bug | low | handed to part 9 (`task 575: Review the review page`) |

## Part 11: Executive summary and close-out

Plan 83 checks this report for completeness, proposes process changes, writes the executive summary at the top and runs the final checks.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Inventory

Every `git ls-files` path in scope, mapped to the one part that reviews it (2026-10-13, 174 files; produced by a throw-away script that reported no unassigned file). Files added later are added here by the part that reviews them.

| path | part | review task |
|---|---|---|
| `app/server/` (`http_base.py`, `main.py`, `media_cache.py`, `paths.py`, `save.py`) | 2 | 532, 533 |
| `authoring/tools/categories.py` | 2 | 534 |
| `app/client/src/engine/` (10 modules, 8 `*.test.ts`, `test/` 3 helpers; not `fixtures/`) | 3 | 535–538 |
| `app/client/src/lib/` (`input.svelte.ts`, `gamepad.ts`, `gamepad.svelte.ts`, `focus.ts`) | 4 | 539 |
| `app/client/src/lib/` (`engine.ts`, `store.ts`, `data.ts`, `desktop.ts`), `src/main.ts`, `src/App.svelte`, `src/app.css`, `src/vite-env.d.ts` | 4 | 540 |
| `app/client/src/lib/` (`api.ts`, `types.ts`, `errors.ts`, `names.svelte.ts`) | 4 | 541 |
| `app/client/src/lib/i18n.ts`, `app/client/src/locales/` (5 files), `app/client/scripts/check-literals.mjs` | 4 | 542 |
| `app/client/src/lib/build.ts` | 4 | 722 |
| `app/client/src/game/` (36 files) | 5 | 543–552; files added since plan 77: 553 |
| `app/desktop/` (`main.mjs`, `preload.cjs`, `resolve.mjs`) | 6 | 554 |
| `app/desktop/save.mjs` | 6 | 555 |
| `app/desktop/` (`package.json`, `package-lock.json`, `electron-builder.yml`, `after-pack.mjs`, `stage-media.mjs`, `steam-presence.vdf`) | 6 | 556 |
| `authoring/steam/` (7 files incl. `steam.json`), `authoring/store/screenshots.mjs` | 6 | 720 |
| `authoring/tools/qgen.py` | 7 | 557–566 |
| `authoring/tools/` (`health.py`, `targets.py`, `batches.py`, `age_groups.py`) | 8 | 567 |
| `authoring/tools/` (`concepts.py`, `progress.py`) | 8 | 568 |
| `authoring/tools/` (`layout.py`, `translations.py`, `pool_export.py`, `save_file.py`) | 8 | 569 |
| `authoring/tools/` (`media.py`, `download.py`) | 8 | 570 |
| `authoring/tools/providers/` (5 files) | 8 | 571 |
| `authoring/tools/` (`engine.py`, `supply.ts`, `sim/` 2 files, `package.json`; added since plan 80: `cdp.mjs`, `patch_notes.py`) | 8 | 572 |
| `authoring/server/main.py` | 9 | 573 |
| `authoring/server/` (`overview.py`, `spot_checks.py`, `media_stats.py`) | 9 | 574 |
| `authoring/ui/src/review/Review.svelte` | 9 | 575 |
| `authoring/ui/src/review/` (`MediaPanel.svelte`, `RevisionPanel.svelte`; added since plan 81: `SourcePanel.svelte`) | 9 | 576, 579 |
| `authoring/ui/src/stats/` (8 files) | 9 | 577 |
| `authoring/ui/src/home/Home.svelte`, `authoring/ui/src/print/JokerCards.svelte` | 9 | 578 |
| `authoring/ui/` (`src/App.svelte`, `src/main.ts`, `src/app.css`, `src/lib/` 3 files, `index.html`, `package.json`, `vite.config.ts`, `svelte.config.js`, `tsconfig.json`, `.gitignore`) | 9 | 579 |
| `flake.nix`, `flake.lock`, `package.json`, `package-lock.json`, `.envrc`, `.gitignore` | 10 | 586 |
| `app/client/` (`package.json`, `tsconfig.json`, `vite.config.ts`, `svelte.config.js`, `index.html`, `.gitignore`) | 10 | 586 |
| `app/client/credits.ts`, `app/client/node.d.ts` | 10 | 721 |
| `directory.md`, `AGENTS.md` (vs. the code only) | 10 | 620 |

Out of scope (milestone 13 "Scope", plan 72):
- `*.json` data and fixtures (226: pools, concepts, bundles, `app/client/src/engine/fixtures/`, `app/data/`); in scope: `package*.json`, `tsconfig.json`, `authoring/steam/steam.json`
- `tasks.sql`, `project-manager.toml`, `plans/` (33)
- prompts: `authoring/tools/prompts/` (18)
- media, audio, fonts: `app/client/public/audio/`, `app/client/public/fonts/` (44)
- `*.md` docs (13), except part 10's `directory.md`/`AGENTS.md` check
