# 15b — Question Translation

**Status:** layout (D-81), pipeline (D-87) and review tool (plan 67) done; pilot and full runs open; no human control per run (milestone 9, 2026-10-16)

Sub-plan of [15](15-i18n.md). Translates the question pool between the four question locales `en`, `es` (Latin American), `es-ES` (Spain), `de` (D-78, D-107); Simplified Chinese, Russian and Portuguese (Brazil) later (milestone 12, on hold). This is the big one: a question is more than its text. Its difficulty, distractors, hints and image all have to work in the new language and culture, so every translated question goes through rating, fact-checking and review again.

## Source locale (D-107, decision 235)
- `locale` on every source in `questions.json`, absent = `es`: `base` ≤ batch-8 `es`, `base` from batch-9 `en`, a regional bundle its region's language (`colombia` `es`).
- `questions.<L>.json`: translations into L of sources whose locale ≠ L (`questions.es.json`, `questions.es-ES.json`, `questions.en.json`, `questions.de.json`).
- Pool for L: approved sources in L + playing translations into L; `pool.json` = `es`, `pool.<L>.json` for the others.
- An en source gets three jobs (→ `es`, `es-ES`, `de`), an es source three (→ `en`, `de`, `es-ES`).

## What a translation has to get right
- **Text:** the question, the answer, the three wrong answers, the three hints, the description (D-8) and the `fun_fact`. Adapt, don't translate literally: units, the answer format, idioms.
- **Questions that don't travel:** wordplay, questions about the source language itself ("¿Qué palabra…?"), and local references whose answer only makes sense in one country. The translator says so instead of forcing it; once the review confirms, the source gets `translatable: false` and stays in its source language only. Colombian-only questions are in the `colombia` bundle (D-41), which isn't translated.
- **Distractors:** wrong answers that are plausible in the source language can be absurd in another language (or accidentally correct). The rate step checks them again.
- **Hints:** a hint that plays on the source word ("empieza por B") has to be rewritten.
- **Difficulty:** re-rated per locale (15). The shared scale (D-38) stays the same; the rating is "for that language's main market".
- **Media:** stays the source's. Text in media (any language) is never a problem (decision 35): no flag, no review problem.

## Pipeline
Decided: D-87 (pm plan 66). One command, `qgen batch --translate <locale>` (`authoring/RUNBOOK.md`), reusing the batch steps through the run's `locale`.

- Run `tr-<locale>-<n>`: 300 sources (`TRANSLATE_SIZE`); the locale's first run is the 50-question pilot (QT-5), no stop; a run failing a threshold is warned about, never a stop (superseded by decision 414: no stop); `qgen health ack <run>` records the look.
- Locales: `es`, `es-ES`, `en`, `de`; sources in any locale but the target; `{source_language}` in the prompts; rate and factcheck for the target's market (`es`: Latin America, `es-ES`: Spain).
- Selection: approved, translatable sources of one bundle (`base`, or `--bundle <id>`, plan 98) not in the target locale; stale translations first, then the `base` demo list's ids (`authoring/data/demo.json`, else `work/demo/proposal.json`; plan 174), then subcategories with the fewest approved translations, levels by the locale's deficit (D-84).
- Steps: translate → rate → factcheck (changed facts only) → merge → review 1 → fix → review 2 → record → audit → export → report.
- Prompts: `translate.md`, `translate-review.md`, `locale-<locale>.md` (spelling and usage: `en` US spelling, words US and UK share; `es` idiomatic Latin American; `es-ES` Spain; `de` as in Germany; no player location, decision 35, decision 167); a regional bundle adds `translate-region.md` (players with a link to the region, decision 167).
- Health: decision 45's subset of the batch thresholds; the LLM translation review is the only review, no spot check per run (milestone 9, 2026-10-16; `authoring/QC.md`).
- Cost per approved translation in each run's report and `qgen report --cost` (CT-3).

## Storage (decided: D-81)
Option A is decided in D-81; the options below are kept as history.

- **A: one file per locale** (`authoring/data/questions.en.json`) with the same IDs and only the translated fields plus their own `difficulty`, `status`, `review`. `questions.json` stays the source file (sources in any locale since D-107). Small diffs, easy to review.
- **B: a `translations` map inside each question.** One file, but `questions.json` grows with every language and gets harder to diff.
- Draft preference: **A**. The export (PORT-6) builds one playable pool per locale either way.
- Decided: A (D-81, pm plan 63). `questions.<locale>.json` with `source_hash` (`stale` derived, left out of the export), `translatable: false` on sources, names in `app/data/names.<locale>.json` (+ per bundle; `en`, `es`, `de`, keyed by slug, D-110; `es-ES` reads `names.es.json`, `names.es-ES.json` overrides where Spain differs); export → `app/data/pool.<locale>.json`.
- Whole-pool rewrites of the source (`qgen tighten`, `qgen neutralize` on es sources, masterplan part 8) stale every touched translation: full runs come after them.

## Review tool
Done (pm plan 67, RV-24..RV-26). The developer and native speakers review `questions.<locale>.json` in `trivia-authoring` with the source alongside, whichever its language (decision 235).

- `/review?locale=es|es-ES|en|de` (+ the usual filters, `stale=1`): locale switch sources · es · es-ES · en · de, keeps the other params.
- Side by side (`SourcePanel.svelte`): source read-only, in its own language (difficulty, status) | translation; rows question, answer, wrong answers, hints, description, fun fact.
- Subcategory and bundle in the locale's names (`GET /api/names?locale=`) plus the key.
- Same verdicts, feedback, problems, difficulty, undo, keys; writes the locale file, re-exports `app/data/pool.<locale>.json`; `pool.json` untouched.
- Stale translation: banner, no approve; the next `--translate` run redoes it.
- Media: shown, not pickable; link to `/review?id=<id>` to change the source's; `bundle`, `media`, `media/search` with a locale → 400. No `media_text` flag (decision 35).
- "Doesn't travel": source `translatable: false` (confirm, undoable); rejects its non-rejected translations ("no viaja").
- Optional sample by the developer: `/review?batch=tr-<locale>-<n>&locale=<locale>&sample=1`; blind as plan 16, source stays visible; items in `authoring/data/spot-checks.json` with `locale` (`authoring/QC.md`); not offered, not required.
- Stats `/stats/*?locale=` (playing translations, own difficulty, locale's names); start page: a row per locale (status counts, stale, not translatable, untranslated sources) and the `tr-*` runs.

## Tasks
- [x] QT-1 Storage layout (A or B) and schema; `validate` covers translations and `stale`. Done 2026-10-12 (task 415): `authoring/tools/translations.py`, `qgen export`/`validate` per locale (D-81).
  - Schema: D-81 (layout A); `validate`/`export`: pm plan 63.
- [x] QT-2 `qgen.py translate` with `translatable: false` / region detection; prompts in `authoring/tools/prompts/`. Done 2026-10-12 (pm plan 66, D-87): `qgen batch --translate <locale>`.
- [x] QT-3 `rate` and `factcheck` per locale. Done 2026-10-12 (pm plan 66, D-87): through `run.json` `locale`.
- [x] QT-4 Review tool: side-by-side locale view. Done 2026-10-12 (pm plan 67): see "Review tool".
- [x] QT-5 Pilot: 50 questions per target locale (`tr-en-1`, `tr-de-1`, `tr-es-1`, `tr-es-ES-1`), reject rate and cost as information for `qgen report --cost`; no go/no-go (milestone 9, 2026-10-16). Runs: pm plan 84.
  - Done 2026-10-21, task 1506. Pilots, 50 sources each (list price, information only; reports `authoring/reports/tr-<locale>-1.md`):

    | run | source → L | translated | approved | needs_work | rejected | not travelling | $/approved | audit agreement | native spot check |
    |---|---|---:|---:|---:|---:|---:|---:|---:|---|
    | `tr-en-1` | es → en | 49 | 49 | 0 | 0 | 1 (confirmed) | $0.12 | 83.7 % ✗ | all good (decision 305) |
    | `tr-de-1` | es → de | 50 | 50 | 0 | 0 | 0 | $0.14 | 80.0 % ✗ | all good (decision 306) |
    | `tr-es-ES-1` | es → es-ES | 50 | 49 | 1 | 0 | 0 | $0.11 | 74.0 % ✗ | none |
    | `tr-es-1` | en → es | 50 | 50 | 0 | 0 | 0 | $0.11 | 98.0 % ✓ | none |

  - Audit-agreement ✗ in en, de, es-ES (decision 45 threshold ≥ 90 %): mostly false "media missing" findings from `task 1492: Translation audit: media title missing in pm work trees` (6 en, 8 de; es-ES 12 media findings), not re-audited; `tr-es-1` ran after the fix. Their full runs already ran; no ack needed here.
- [ ] QT-6 Full translation per question locale: `en`, `de`, `es`, `es-ES` (D-78, D-107); no native-speaker spot check (LLM review only, milestone 9); runs per pm plan 84. Later: `zh-Hans`, `ru`, `pt-BR` (milestone 12).
  - QT-6 progress `en`: `tr-en-2` (2026-10-24) 291 translated, 282 approved (9 not travelling); 4498 in the `en` pool (incl. en-sourced), target not met; next `tr-en-3`.
  - QT-6 progress `de`: `tr-de-2` (2026-10-23) 297 translated, 290 approved; `qgen report --locale de`: 343 approved in `de`, target not met; next `tr-de-3`.
  - QT-6 progress `es-ES`: `tr-es-ES-2` (2026-10-23) 300 translated, 297 approved; 345 in the `es-ES` pool, target not met; next `tr-es-ES-3`.
  - QT-6 progress `es-ES`: `tr-es-ES-3` (2026-10-24) 300 translated, 296 approved; 641 in the `es-ES` pool, target not met; next `tr-es-ES-4`.
  - QT-6 progress `es-ES`: `tr-es-ES-4` (2026-10-24) 299 translated, 295 approved, 4 needs_work, 1 not travelling; 936 in the `es-ES` pool, target not met; next `tr-es-ES-5`.
  - QT-6 progress `es-ES`: `tr-es-ES-5` (2026-10-24) 300 translated, 299 approved, 1 needs_work; about 1235 in the `es-ES` pool, target not met; next `tr-es-ES-6`.
  - QT-6 progress `es-ES`: `tr-es-ES-6` (2026-10-24) 300 translated, 298 approved, 2 needs_work; 1533 in the `es-ES` pool, target not met; next `tr-es-ES-7`.
  - QT-6 progress `es-ES`: `tr-es-ES-7` (2026-10-24) 299 translated, 297 approved, 2 needs_work, 1 not travelling; about 1830 in the `es-ES` pool, target not met; next `tr-es-ES-8`.
  - QT-6 progress `es-ES`: `tr-es-ES-8` (2026-10-24) 300 translated, 298 approved, 2 needs_work; about 2128 in the `es-ES` pool, target not met; next `tr-es-ES-9`.
  - QT-6 progress `es-ES`: `tr-es-ES-9` (2026-10-24) 300 translated, 297 approved, 3 needs_work; 2425 in the `es-ES` pool, target not met; next `tr-es-ES-10`.
  - QT-6 progress `es-ES`: `tr-es-ES-10` (2026-10-25) 300 translated, 298 approved, 2 needs_work; 2723 in the `es-ES` pool, target not met; next `tr-es-ES-11`.
  - QT-6 progress `es`: `tr-es-2` (2026-10-23) 300 translated, 296 approved; 2351 in the `es` pool (incl. es-sourced), target not met; next `tr-es-3`.
  - QT-6 progress `es`: `tr-es-3` (2026-10-24) 300 translated, 298 approved; 2649 in the `es` pool (incl. es-sourced), target not met; next `tr-es-4`.
  - QT-6 progress `es`: `tr-es-4` (2026-10-24) 300 translated, 298 approved, 2 needs_work; 2947 in the `es` pool (incl. es-sourced), target not met; next `tr-es-5`.
  - QT-6 progress `es`: `tr-es-5` (2026-10-24) 300 translated, 293 approved, 7 needs_work; 3240 in the `es` pool (incl. es-sourced), target not met; next `tr-es-6`.
  - QT-6 progress `es`: `tr-es-6` (2026-10-24) 300 translated, 297 approved, 3 needs_work; 3537 in the `es` pool (incl. es-sourced), target not met; next `tr-es-7`.
  - QT-6 progress `es`: `tr-es-7` (2026-10-24) 300 translated, 296 approved, 4 needs_work; about 3833 in the `es` pool (incl. es-sourced), target not met; next `tr-es-8`.
  - QT-6 progress `es`: `tr-es-8` (2026-10-24) 300 translated, 297 approved, 3 needs_work; 4130 in the `es` pool (incl. es-sourced), target not met; next `tr-es-9`.
  - QT-6 progress `es`: `tr-es-9` (2026-10-25) 300 translated, 295 approved, 5 needs_work; 4425 in the `es` pool (incl. es-sourced), target not met; next `tr-es-10`.
  - QT-6 progress `es`: `tr-es-10` (2026-10-25) 300 translated, 292 approved, 8 needs_work; 4717 in the `es` pool (incl. es-sourced), target not met; next `tr-es-11`.
