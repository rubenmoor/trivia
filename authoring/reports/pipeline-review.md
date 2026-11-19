# Pipeline review for milestone 12 (task 2339)

This is a review of the question authoring and translation pipeline, done before any China work starts (`plan 229: Pipeline review and cleanup for milestone 12`). It lists what is unused, duplicated or wrong, and the places that would break for a second base bundle or for Chinese text. Each finding is a cleanup task, waits for one of the developer's decisions, or is kept as it is. The close-out (`task 2340: Close-out of plan 229: checks, unchanged output, starting points of plans 139 and 227`) marks each one done.

- Date: 2026-11-19. Baseline at commit `eee362cb` → `pipeline-review-baseline/` (`commit.txt`, `validate.txt`, `report*.txt`, `report-cost.txt`). The close-out deletes it.
- Usage: from `work/*/run.json` and step dirs in the main checkout (302 runs), `calls.jsonl`/`costs.log`, git log, RUNBOOK, QC.md, AGENTS.md, answered decisions.
- Line numbers are from 2026-11-19 (`~`). The cleanups move them.

## Usage summary
Who runs what, by mode, with the last start date.
- `batch`: base es (early) 10-11, base en 10-23, colombia 10-24, stem 10-28, spain and germany 11-11, usa and mexico 11-12, uk 11-14 (17 runs).
- `batch --media-first`: 16 runs 11-15..11-18; batch-93 unfinished.
- `--translate`: base es/es-ES/de 23–30 runs each, last 11-18; base en 6 (10-29); regions → en 7–10 each (11-12); stem 1 each.
- `rework`: 80 opus (last 11-18), 1 fable (10-15).
- Rare: `tighten` 2 (10-11, tighten-2 unfinished), `neutralize` 1 (10-14), `audit --backlog` 6 (10-23), `video-window` 1 (11-17).
- One-offs: `remap`, `english-keys`, `rekey` (slugs), `concepts --fill`, `taxonomy`, `bundles`, `first-120` (import).

## Findings: certain cleanups (plan 229)

| Finding | Where | Why | Change | Risk | Task |
|---|---|---|---|---|---|
| `{max_video_s}`/`{max_audio_s}` not filled in review, fix and audit | `qgen.prompt` vs `media_first.prompt_file`; `media-first-checks.md:8`, `audit.md:34` | bug: the prompts show the literal placeholder | fill in `prompt()`, plus a test | low | 2347 |
| Write order loses work on a crash | `apply_to_drafts`, `cmd_merge`, `cmd_translate_batch` | drafts dropped; self-duplicates on rerun; translation paid twice | reorder the writes, plus tests | low | 2348 |
| Applied one-off migrations | `rekey.py`, `cmd_bundles` + `bundles.md`, `cmd_import`/`--assign-unbatched`/apply's pool branch | each ran once (10-06..10-16); nothing left to do; a rerun of `bundles` would be harmful | delete | low | 2349 |
| Dead CLI entry points | `dedupe`, the `english-keys` subcommand, `merge --min-score` | no caller, or always 0 | delete | low | 2350 |
| Compat code for data that no file has any more | `played.py`, `slug_keys`, `categories._fallback`, `STALE_WHY`, media_survey list pools, `bundle or "base"`, patch-notes pre-slug, the "Otros" facet | dead branches | delete | low | 2351 |
| Five pool-file helpers, one of them checking `pool.es.json` | `paths`, `layout`, `report`, `sim/load.ts`, `validate` | duplicates; the validate check can never fire | one helper | low | 2352 |
| Duplicated helpers in tools | read-json ×6, natural sort, rounding, `_num`, `exports` ×2 | decision 199 | import | low | 2353 |
| Duplicated helpers in the server | `load_bundles`, age groups, filter chain, flag feedback text, report labels without a source comment | decision 199 | import | low | 2354 |
| `report --cost` projection is wrong | `report.py` ~692-750 | regions get es/en rows; rates mix bundles and media-first (~15× too high) | rows per bundle's languages, rates per bundle and mode | info only | 2355 |
| Batch report always shows base's deficit | `health.deficit_line` | colombia reports show base | pass the run's bundle | low | 2356 |
| Related questions rebuilt per call in translation runs | `review_steps` ~188/220, `audit` ~198 | slow, re-reads files | build once per step | low | 2357 |
| `trivia-media sync` works per slot, not per file | `media.py` ~250, ~303-323 | 2316 URLs are already shared; a broken mark misses sharers outside the filter | group by URL | low | 2358 |
| Licence and resolution counts per question | `overview.py` ~126, `media_stats.py` ~62-75, `validate.py` ~79-104 | shared files counted twice, more with copies | count files | low | 2359 |
| `qgen gc` skips rework, tighten and neutralize runs | `work_gc.qualifies` | ~1.8 GB of sheets kept | let them qualify | low | 2360 |
| Stale docs and comments | RUNBOOK batch size, validate-fail row, README `--player` and report routing, `flag_loop` comment, `run_bundle` docstring, `media.py` docstring, `IMAGE_WIDTH` | out of date | fix | none | 2361 |

## Findings: unsure deletions (`decision 760: Pipeline cleanup: which unused features may go?`)
Every candidate is in the decision's table with its last use and what goes with it.

| # | Candidate | Rec. | Task |
|---|---|---|---|
| 1 | single-step subcommands (draft … translate) | delete | 2362 |
| 2 | `qgen neutralize` (if kept: fix its cost line, `rework.py` ~266) | delete | 2363 |
| 3 | `qgen tighten` | delete | 2364 |
| 4 | `audit --backlog` (11 questions left) | last slice, then delete | 2365 |
| 5 | `qgen video-window` | delete | 2366 |
| 6, 7 | NASA, Freesound providers (0 picks) | delete | 2367 |
| 8 | `trivia-media fetch` | delete | 2368 |
| 9–12 | `report --exit-check`, `--calibration`, `--overlaps`, `--subcategories` | delete 9–11, keep 12 | 2369 |
| 13, 14 | review-page bundle move with its start-page row, the old `/?batch=` redirect | delete | 2370 |
| 15–17 | `costs.log`, old `run.json` defaults, old media candidate files and the pilot ledger: convert, then drop | convert | 2371 |
| 18 | a source question without `locale` means es (6310 sources) | convert | 2372 |

## Findings: prompt wording (`decision 761: Prompt wording cleanup from the pipeline review: apply?`)
Four fixes, all in the decision's drafts. Applying them is task 2373.
- house-style's media sources still name Freesound.
- The `background_query` bullet in `draft.md` repeats the house style.
- `translate.md`'s same-language rule names only Spanish.
- Spanish examples in the English concept prompts.

## For later parts
| Finding | Where | Owner |
|---|---|---|
| Normalisers delete CJK: every zh answer counts as a duplicate, overlap finds nothing, false "duplicate options", related questions are arbitrary | `concepts.key/slug`, `qgen.norm`, `stem`, `option_key`, `related_questions` | `task 2374: Unicode-aware text normaliser for duplicate, overlap and option checks` (plan 139; `task 1165: Check pass and docs for the Chinese locale(s)` requires it) |
| Review UI: `lang="es"`, no CJK font in the dev shell; joker cards hard-code fonts and paper size | `authoring/ui` | `task 2375: Review and print pages: lang attributes and a CJK font` (plan 139) |
| `qgen flag` report labels have no zh; locale defaults to es | `reviews.py`, `main.py` | `task 2376: qgen flag: Chinese report labels and no es default` (plan 139) |
| The translation number check sends 万/亿 and fullwidth digits to fact check | `translate.numbers` | `task 2377: Translation number check for Chinese numerals and fullwidth digits` (plan 140) |
| "Any base bundle" and es hits not in the task: voice locale, targets exemption, report D-75, `--career`, `--cost`, default locale, `NAMES_LOCALES`, names warnings, demo pools, `bundle new` Spanish names, patch notes, start page supply, review UI `base`/es defaults | many | added to `task 2329: A base bundle other than base in the pipeline` |
| Copies: concept and subcategory checks, own batch and review, media fixed on copies (`kept_slots`, merge, revise, server pick), `--overlaps` | `validate`, `review_steps`, `qgen`, `main.py` | added to `task 2330: Copy model: copied_from, copy helper, validate rules` |
| Prompts name `base` where they mean "a base bundle" (International angle, "every language of the game") | `house-style.md`, `draft.md`, `review.md`, `rate.md`, concept prompts | added to `task 2335: Create the chinese-base bundle: entry, names, rule and voice` (rule/voice decision) |
| Should new chinese-base drafts avoid `base` questions that were not copied (D-111 checks every bundle)? | `draw_slots`, rate, merge | the drafting part of `plan 60: masterplan` raises it; noted in task 2330 |
| Theme bundles' draft gaps count locales they don't list | `targets.source_supply` | already `task 1163: Chinese locale(s) in the locale lists and rules` |
| Fit pass over existing questions | reuses the `rework`/scan shape (`SCANS`, `kept_slots`) | plan 230 tasks 2342–2346 (already planned) |

## Kept, used
- Kept by decision:
  - `rework --model fable`: `decision 216: Fable for qgen rework: keep, drop or try for batch review? (plan 58)`.
  - Python twins `media_cache.py`, `http_base.py`, the save upgrades in `save_file.py`: `decision 104: Python ↔ Node/TS twins: how to keep save, media cache and serving rules in sync` (leave the Python side alone).
  - Theme translations from all locales: `decision 371: Topic bundles: pace and order of the content runs`.
- Batch modes and steps:
  - `qgen batch` plain, `--bundle`, `--translate`, `--media-first`: steps match the RUNBOOK.
  - `--ids`/`--dry-run` with `--translate`, `--files`/`--until` (media-first, developer only; used in batch-78).
  - `english-keys` as a step: every en and media-first batch; 10590 of 10590 keyed.
  - `concepts` (standalone `--fill`, 10-15).
  - `batch-report`.
- Commands for setup, the demo and QC:
  - `qgen taxonomy`, `qgen remap`: theme and region setup, updated 11-12.
  - `qgen bundle new`.
  - `qgen health ack`: decisions 359, 401, 408.
  - `qgen demo`.
  - `qgen flag`: the QC loop, up to rework-72.
  - `qgen gc` (new).
- Not used yet but planned:
  - `qgen flag --pull`, `qgen telemetry`, `report --played`: post-launch (plan 109).
  - `qgen patch-notes`: called by the release check.
- `qgen report` options:
  - `--qc`, `--batches`, `--flags`: QC.md.
  - `--simulate`, `--career`: plans 16 and 24.
  - `--review-time`: plan 98.
  - `--cost`: AGENTS.md.
  - The `calibration()` function: used by batch health.
- Media:
  - Commons: 21023 picks. Openverse: 55 picks.
  - `media_first`, `media_survey` (~1450 files left), `media_probe`, `media_keep`, `media_cache`, `download`, `http_base`.
  - `trivia-media sync` and `licenses`: release gate.
  - `sound_brief.py`: sound design, plan 220.
- Compat that is still needed:
  - Reading `costs.log` (until candidate 15).
  - `guess_problems`: 57 human and 462 LLM reviews have no `problems`.
  - `for_review`'s `style` fallback: 393 questions.
  - `llm_decisions` and `health.recorded` fallbacks: batch-4..7.
  - `categories.old_keys()` and `old-keys.json`: saves and patch notes.
- Prompts: every file has a loader; `revise.md`'s Spanish feedback tags are fixed internal tags.
- Review UI: every API function and GET endpoint has a caller; locale lists come from `LOCALES` (zh needs no edit there); sorting is count-only.

## Not worth a task
- `style: null` on new questions (20816 of them): harmless, and readers use `.get`.
- Concept prompts repeating the difficulty scale and the "international angle": the repetition is deliberate context; rewording them risks list quality.
- `locale-es.md`'s neutral-Spanish word lists overlapping `review.md` and `neutralize.md`: approved wording (`decision 32: Neutral Spanish prompts for base (plan 64)`).
- `sound_brief` loudness parsing vs `sfx.py`: sfx is out of this plan's scope.
