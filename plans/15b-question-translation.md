# 15b — Question Translation

**Status:** layout (D-81) and pipeline (D-87) done; review tool, pilot and full runs open

Sub-plan of [15](15-i18n.md). Translates the question pool into the launch languages: English and German (D-78); Simplified Chinese, Russian and Portuguese (Brazil) later (milestone 12, on hold). This is the big one: a question is more than its text. Its difficulty, distractors, hints and image all have to work in the new language and culture, so every translated question goes through rating, fact-checking and review again.

## What a translation has to get right
- **Text:** the question, the answer, the three wrong answers, the three hints, the description (D-8) and the `fun_fact`. Adapt, don't translate literally: units, the answer format, idioms.
- **Questions that don't travel:** wordplay, questions about the Spanish language itself ("¿Qué palabra…?"), and Colombian references whose answer only makes sense to Colombians. The translator says so instead of forcing it; once the review confirms, the source gets `translatable: false` and stays in Spanish only. Colombian-only questions are in the `colombia` bundle (D-41), which isn't translated.
- **Distractors:** wrong answers that are plausible in Spanish can be absurd in another language (or accidentally correct). The rate step checks them again.
- **Hints:** a hint that plays on the Spanish word ("empieza por B") has to be rewritten.
- **Difficulty:** re-rated per locale (15). The shared scale (D-38) stays the same; the rating is "for that language's main market".
- **Media:** stays the source's. Text in media (Spanish or any language) is never a problem (decision 35): no flag, no review problem.

## Pipeline
Decided: D-87 (pm plan 66). One command, `qgen batch --translate <locale>` (`authoring/RUNBOOK.md`), reusing the batch steps through the run's `locale`.

- Run `tr-<locale>-<n>`: 300 sources (`TRANSLATE_SIZE`); the locale's first run is the 50-question pilot (QT-5), after which the next run exits 2 until `qgen health ack tr-<locale>-1`.
- Selection: approved, translatable `base` sources; stale translations first, then subcategories with the fewest approved translations, levels by the locale's deficit (D-84).
- Steps: translate → rate → factcheck (changed facts only) → merge → review 1 → fix → review 2 → record → audit → export → report.
- Prompts: `translate.md`, `translate-review.md`, `locale-<locale>.md` (market: `en` US + UK, US spelling; `de` Germany, Austria, Switzerland; decision 35).
- Health: decision 45's subset of the batch thresholds; native-speaker spot check per run (`authoring/QC.md`).
- Cost per approved translation in each run's report and `qgen report --cost` (CT-3).

## Storage (decided: D-81)
Option A is decided in D-81; the options below are kept as history.

- **A: one file per locale** (`authoring/data/questions.en.json`) with the same IDs and only the translated fields plus their own `difficulty`, `status`, `review`. The Spanish file stays the source. Small diffs, easy to review.
- **B: a `translations` map inside each question.** One file, but `questions.json` grows with every language and gets harder to diff.
- Draft preference: **A**. The export (PORT-6) builds one playable pool per locale either way.
- Decided: A (D-81, pm plan 63). `questions.<locale>.json` with `source_hash` (`stale` derived, left out of the export), `translatable: false` on sources, names in `app/data/names.<locale>.json` (+ per bundle); export → `app/data/pool.<locale>.json`.
- Whole-pool rewrites of the source (`qgen tighten`, neutral Spanish rewrite, masterplan part 8) stale every touched translation: full runs come after them.

## Review tool
- `/review?batch=…&locale=en` shows the source and the translation side by side, with the same approve / needs work / reject decisions (RV-*).

## Tasks
- [x] QT-1 Storage layout (A or B) and schema; `validate` covers translations and `stale`. Done 2026-10-12 (task 415): `authoring/tools/translations.py`, `qgen export`/`validate` per locale (D-81).
  - Schema: D-81 (layout A); `validate`/`export`: pm plan 63.
- [x] QT-2 `qgen.py translate` with `translatable: false` / region detection; prompts in `authoring/tools/prompts/`. Done 2026-10-12 (pm plan 66, D-87): `qgen batch --translate <locale>`.
- [x] QT-3 `rate` and `factcheck` per locale. Done 2026-10-12 (pm plan 66, D-87): through `run.json` `locale`.
- [ ] QT-4 Review tool: side-by-side locale view.
- [ ] QT-5 Pilot: translate 50 questions to English, review them, and measure the reject rate and cost before the full run.
- [ ] QT-6 Full translation per launch language: `en`, `de` (D-78); native-speaker spot check. Later: `zh-Hans`, `ru`, `pt-BR` (milestone 12).
