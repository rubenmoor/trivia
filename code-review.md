# Code review (milestone 13)

This report collects the findings of the code review of milestone 13, part by part. Task 616 (the linter evaluation of part 10) ran ahead of the other parts, so only its section exists yet; `task 524: code-review.md skeleton, inventory and directory.md entry` adds the intro, format, the other parts and the inventory around it.

## Part 10

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
