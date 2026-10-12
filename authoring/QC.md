# QC — Quality control after every batch

This is the procedure that follows every finished batch (plan 16, D-56). The LLM review decides each question; this procedure measures whether it decides like the gamemaster, and turns what goes wrong into prompt or house-style changes before the next batch. It is for the gamemaster and for pm workers; `RUNBOOK.md` stays the procedure for the batch itself.

## Steps

The steps run in order; a pm worker stops at each decision and continues when it is answered.

1. **Batch done.** `qgen batch` finished and is committed (RUNBOOK). The report `authoring/reports/<batch>.md` has the "## Audit" section (LLM audit of a seeded sample of 60, blind to the review).
   - Major audit findings on approved questions: `http://127.0.0.1:8001/review?batch=<batch>&audit=flagged`.
2. **Blind spot check (gamemaster only).** Run `trivia-authoring`, open `http://127.0.0.1:8001/review?batch=<batch>&sample=1`.
   - 30 questions (`quality.spot_check_size` in `authoring/data/targets.json`), a subset of the audit sample, same ones on every reload; ~10–15 min.
   - The LLM decision, feedback and audit stay hidden until you decide; then they show next to yours. Mark the problem kinds in the feedback box.
   - Recorded in `authoring/data/spot-checks.json`; undo removes the item.
   - pm worker: can't do this. `pm decision add "Spot check <batch> done?"` (body: the link, the size, `trivia-authoring`; option "done"), `pm task-pending-decision <task> <decision>`, stop.
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
   - All proposals in one decision: `pm decision add "QC <batch>: which changes?"`, options "recommended set" (first), "all", "none"; wait on it, stop. No proposals: no decision.
   - Answered: each approved change becomes a task in its plan (`pm task add <plan>`, the plan's priority, so above the -100 batch tasks). Then `qgen report --qc <batch> --changes "<task ids>"` (or `"none"`) writes the report's "Changes from this QC" line.
5. **Next batch waits.** The next batch task runs only after both decisions are answered and the change tasks are done (they outrank it; plan 17 "Per-batch pattern").

## Neutralize runs

A `qgen neutralize` run (D-83) changes approved questions, so it gets the same steps as a batch, with `neutralize-<n>` in place of `<batch>`.

- Report: `authoring/reports/neutralize-<n>.md` (Audit section included).
- Flagged audit findings: `http://127.0.0.1:8001/review?run=neutralize-<n>&audit=flagged`.
- Spot check: `http://127.0.0.1:8001/review?run=neutralize-<n>&sample=1`.
- QC report: `qgen report --qc neutralize-<n>`; the trend table has a column per run.
- Extra check in the spot check: the wording is neutral, the meaning unchanged.

## Translation runs

A `qgen batch --translate <locale>` run (D-87) gets the same steps, with `tr-<locale>-<n>` in place of `<batch>`; the spot check is by a native speaker of the locale.

- Report: `authoring/reports/tr-<locale>-<n>.md` (Health, Audit, Not travelling, Stale re-translated).
- Spot check (native speaker): `http://127.0.0.1:8001/review?batch=tr-<locale>-<n>&locale=<locale>&sample=1`; source and translation side by side (plan 67).
- Extra checks: faithful to the source, natural in the language, hints and wrong answers that work in it, difficulty for the locale's market; text in media is never a problem (decision 35).
- QC report: `qgen report --qc tr-<locale>-<n>`; the trend table has a column per run.
- Proposals: `prompts/translate.md`, `translate-review.md`, `locale-<locale>.md`, `rate.md`.
- Pilot `tr-<locale>-1` (QT-5): the next run waits for `qgen health ack`; the go is the gamemaster's.

## Never

- Change prompts, house style or `qgen.py` inside a batch run or a QC task; only in the change tasks of step 4.
- Answer the spot-check decision or spot-check questions as an LLM; the spot check is the gamemaster's.
- Approve or reject questions because of an audit finding; the gamemaster decides them in the review tool.
