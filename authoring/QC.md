# QC — Quality control after every batch

This is the procedure that follows every finished batch (plan 16, D-56). The LLM review decides each question; this procedure measures whether it decides like the developer, and turns what goes wrong into prompt or house-style changes before the next batch. It is for the developer and for pm workers; `RUNBOOK.md` stays the procedure for the batch itself.

## Steps

The steps run in order; a pm worker raises each decision and never waits on it (decision 414: reviews don't gate generation); the next QC task acts on the answers.

1. **Batch done.** `qgen batch` finished and is committed (RUNBOOK). The report `authoring/reports/<batch>.md` has the "## Audit" section (LLM audit of a seeded sample of 60, or of the whole spot check if larger, blind to the review).
   - Major audit findings on approved questions: `http://127.0.0.1:8001/review?batch=<batch>&audit=flagged`.
2. **Blind spot check (developer only).** Run `trivia-authoring`, open `http://127.0.0.1:8001/review?batch=<batch>&sample=1`.
   - 30 questions (`quality.spot_check_size` in `authoring/data/targets.json`), a subset of the audit sample, same ones on every reload; ~10–15 min.
   - Per source locale (plan 148): a batch's questions are in its source locale (`base` ≤ batch-8 `es`, from batch-9 `en`; a regional bundle its region's), checked in that language; batch-9 and batch-10 keep 30 (decision 234); `qgen report --qc` shows each batch's source locale, so en agreement is read apart from es.
   - Larger check of one run (decision 228: batch-8, 120): its `"size"` in `authoring/data/spot-checks.json`; the first 30 stay a prefix; `qgen audit --batch <batch>` audits up to that size.
   - The LLM decision, feedback and audit stay hidden until you decide; then they show next to yours. Mark the problem kinds in the feedback box.
   - Recorded in `authoring/data/spot-checks.json`; undo removes the item; a back-audit run also keeps its `ids` there (`qgen validate` needs no `work/`).
   - pm worker: can't do this. `pm decision add "Spot check <batch> done?"` (body: the link, the size, `trivia-authoring`; option "done"), no `pm task-pending-decision`, no stop; the next QC task reads the answer.
3. **QC report.** `qgen report --qc <batch>`: rewrites "## Quality control" in `authoring/reports/<batch>.md`.
   - Agreement (both accept or both don't) against `quality.min_agreement` (90 %), false approves, false needs_work, difficulty |Δ| ≥ 2, media changed, audit/human agreement.
   - Every disagreement with the human's feedback, grouped by problem kind.
   - `qgen report --qc` (no batch): the trend table, one column per batch.
   - **Release bar (D-79):** the same numbers (pm decision 15), per batch and per back-audit slice (`backaudit-<k>`). Section line "Release bar": ✓ release-ready or ✗ with the failed limit; trend row "release".
     - ✗ → not release-ready; family play and statuses unchanged.
     - Consequence: only step 4's proposals; no full audit, no second spot check.
4. **Findings → proposals.** A proposal for each problem kind with:
   - ≥ 2 disagreements in the QC section, or
   - ≥ 2 major audit findings on approved questions (Audit section), or
   - any false approve for `fact`.
   - Each proposal: which prompt (`authoring/tools/prompts/`: `review.md`, `draft.md`, `house-style.md`, `rate.md`, `audit.md`) and the change in a few lines.
   - Trend: if the audit agrees with the human clearly better than the review over two batches, propose moving the audit's checks into `review.md` or making the audit a gate.
   - All proposals in one decision: `pm decision add "QC <batch>: which changes?"`, options "recommended set" (first), "all", "none"; raise it, don't wait. No proposals: no decision.
   - Once answered (by the next QC task): each approved change becomes a task in its plan (`pm task add <plan>`, the plan's priority, so above the -100 batch tasks). Then `qgen report --qc <batch> --changes "<task ids>"` (or `"none"`) writes the report's "Changes from this QC" line.
5. **Next batch doesn't wait.** The next batch task runs without the answers (decision 414); answered decisions become change tasks, which outrank it (plan 17 "Per-batch pattern"), so they run first if they exist by then.

## Media-first runs

`qgen batch --media-first` runs (`batch-<n>`, `run.json` `"mode": "media-first"`, plan 203, decision 646) follow the steps above with their own numbers (decision 647) and a spot check that plays sound and video. Pacing (500 first, then steps of 100) is the content runs' (decision 643), not this file's.

- Same steps 1–5; `qgen report --qc` and `qgen report --batches` read the mode from `run.json`.
- Spot-check size (`quality.media_first` in `authoring/data/targets.json`): 40 per run, 60 for the first media-first run while new (`first_run_size`); the first 30 stay a prefix of the audit sample; the audit reads up to that size; `size` in `spot-checks.json` still overrides.
- Agreement ≥ 90 % as for any batch (`quality.media_first.min_agreement`); the release bar per run uses the run's own size.
- The spot check (`/review?batch=<run>&sample=1`) plays `media.excerpt` start→end as the game does, with the background picture; aids (transcript, OCR, sheets), the LLM verdict and the mechanical findings stay hidden until you decide.
  - Check by ear and eye: recognisable from the window, no giveaway (spoken name, caption, logo, file name in the picture), content matches the answer, licence and `media.work` for public-domain music/film, sound quality, speech only where the words needn't be understood (decision 648). Mark the problem kinds: `giveaway`, `media`, `fact`, `ambiguity`.
- `qgen report --qc` trend: a "mode" row marks each column; below the table one row sums agreement across all media-first runs (✓/✗ against the bar) and counts their disagreements per problem kind.
- Batch health (`batch_health.media-first` in `targets.json`, over the base thresholds): `media share` not applied; new rows `giveaway-step drop rate` (drafts the giveaway step removed, of those designed) and `mechanical-check rate` (questions with a hard mechanical finding at record); `$ per approved` ≤ $0.60. Starting numbers from the pilot and trial: adjust after the first runs.
- Findings → proposals (step 4) as above; the media prompts are `review.md` and `audit.md` media-first sections and `media-design.md`.

## Fit runs

A `qgen batch --bundle chinese-base --from base` run (`fit-<n>`, plan 230) judges `base` questions for `chinese-base` and copies what fits. Its check is the developer's read of the lists and samples, and the flips that correct the pass; there is no agreement bar beyond the review sample's.

- Report: `authoring/reports/fit-<n>.md`: judged, kept, adapted, dropped, by rule, not copyable, per `base` category and subcategory, drop reasons, the copies left `needs_work`, the audit of the adapted copies, cost.
- Lists: the copies at `http://127.0.0.1:8001/review?batch=fit-<n>`; verdicts in `authoring/data/bundles/chinese-base/fit.json`; the fit view with flips at `/review?fit=chinese-base` (filters verdict, reason, run; a drop sample of 30 per run; the spot-check sample of a run at `/review?batch=fit-<n>&sample=1`).
- Samples: the spot check (`&sample=1`) over kept and adapted copies (the audit reads the adapted only); the fit view's drop sample (30 per run) to see the pass doesn't drop too much.
- Flips: drop → keep (the next run copies it, no fit call); keep → drop (the copy `rejected` at once, in the fit view); adapt ↔ keep only through the copy's own review. Flips are `by: developer` in `fit.json`.
- Health: `authoring/reports/batches.md` "Fit runs" (rates, $ per judged source; no thresholds, no gate); the developer records the look with `qgen health ack fit-<n> "<note>"`.
- Prompt changes only after a decision on `prompts/fit.md` (D-36).

## Translation runs

A `qgen batch --translate <locale>` run (D-87; `es`, `es-ES`, `en`, `de`, from sources in any other locale, D-107) has no QC steps. The LLM translation review (D-32, D-33) is its only review (milestone 9, developer 2026-10-16): no spot check, no QC decision, no pilot go/no-go.

- Report: `authoring/reports/tr-<locale>-<n>.md` (Health, Audit, Not travelling, Stale re-translated).
- Health ✗: reported in the Health table and raised as a decision, never a stop (decision 414); the developer's `qgen health ack <run> "<note>"` records their look; the first run (50-source pilot) is no exception, and its numbers only inform `qgen report --cost`.
- Optional review by the developer: `http://127.0.0.1:8001/review?batch=tr-<locale>-<n>&locale=<locale>`; source and translation side by side (plan 67).
  - Stale translation: no approve (the next run redoes it); a question that only works in its source language: "doesn't travel".
  - `&sample=1` (blind sample) still works by URL; existing records in `authoring/data/spot-checks.json` stay.
- Native check, zh only (decision 754: Native checks of Chinese translation runs: pilot and release sample, not every run): the pilot run, the Chinese-language subcategories and one release sample go to a volunteer as an offline sheet; nothing waits for it (decision 414).
  - Export: `qgen spotcheck export <run> [--controls N]` → `work/<run>/spotcheck-<run>.html`; `--release <zh>` or `--subcategory <key>… --locale <zh>` → `work/spotcheck/<name>.html`; brief `authoring/NATIVE-REVIEW.md`.
  - A pm worker that exports raises `pm decision add "Spot check <sheet> done?"` (body: sheet path, `qgen spotcheck import <name>.verdicts.json`), never `pm task-pending-decision`.
  - Import (the developer, in `../trivia-review`): `qgen spotcheck import <file> [--dry-run]` → human reviews (`by: native`) and spot checks; `qgen report --qc` shows "controls caught k/N" per sheet.
- Player reports: `qgen flag` sets `needs_work` (below).
- Prompt changes only in a change task: `prompts/translate.md`, `translate-review.md`, `locale-<locale>.md`, `rate.md`.

## Player reports

Players report questions from the game (plan 93); each report becomes a human `needs_work` review, outside the batch steps.

- Pasted report text (copied from «Preguntas marcadas»): `qgen flag [--dry-run] < reports.txt`; feedback «Reporte de jugador (…)» in `/review?status=needs_work`, older feedback after «Antes:»; a report in the source's locale → source, else that locale's translation (decision 235); unknown ids skipped, a repeated report adds nothing.
- Sent reports (report server, plan 103): `qgen flag --pull [--url URL] [--dry-run]`; same feedback, then acked; token `TRIVIA_REPORT_TOKEN` or `state/report-token`; ledger `state/reports-pulled.json`; mod and unknown ids skipped and acked.
- Flag loop (open flags → rework → causes → lessons):
  - Open flags: `qgen report --flags` lists the `needs_work` questions with player feedback and their age in days; `qgen report` and `qgen patch-notes` print the count (patch-notes also the list, on stderr; ids never enter the notes, decision 97). Read it before every patch.
  - Video length: `qgen validate` rejects a video that would play > 30 s (audio keeps 60 s).
  - Rework (only when the developer asks): the reviser names a `cause` for each flagged question (`flag_loop.CAUSES`: wrong_fact, ambiguous, second_correct_option, difficulty, language, media, tone, not_a_defect, other); `qgen rework` appends it to `authoring/data/flag-causes.json` (commit it) and prints the lessons.
  - Lessons: a cause seen 3 times (`flag_loop.REPEATED`; not_a_defect and other excluded) prints a proposal. Raise a decision for the developer (`pm decision add`) with the cause, its question ids and the prompt (`draft.md`, `review.md`, `house-style.md`) or QC rule change; apply it only in a change task after the answer ("Never" below).
- Played outliers (opt-in telemetry, plan 109, decision 122): `qgen telemetry --pull`, then `qgen report --played`; candidates in `/review?played=outliers[&locale=…]`; the developer changes the difficulty or sets `needs_work` by hand, nothing automatic.

## Never

- Change prompts, house style or `qgen.py` inside a batch run or a QC task; only in the change tasks of step 4.
- Answer the spot-check decision or spot-check questions as an LLM; the spot check of a drafted batch is the developer's.
- Approve or reject questions because of an audit finding; the developer decides them in the review tool.
- Delete a question from `authoring/data/questions.json`; dropping one = status change (`rejected`), so ids are never reused; `qgen validate` fails on an id of the newest `v*` tag's pool that is gone (plan 91).
