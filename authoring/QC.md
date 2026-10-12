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
4. **Findings → proposals.** A proposal for each problem kind with:
   - ≥ 2 disagreements in the QC section, or
   - ≥ 2 major audit findings on approved questions (Audit section), or
   - any false approve for `fact`.
   - Each proposal: which prompt (`authoring/tools/prompts/`: `review.md`, `draft.md`, `house-style.md`, `rate.md`, `audit.md`) and the change in a few lines.
   - Trend: if the audit agrees with the human clearly better than the review over two batches, propose moving the audit's checks into `review.md` or making the audit a gate.
   - All proposals in one decision: `pm decision add "QC <batch>: which changes?"`, options "recommended set" (first), "all", "none"; wait on it, stop. No proposals: no decision.
   - Answered: each approved change becomes a task in its plan (`pm task add <plan>`, the plan's priority, so above the -100 batch tasks). Then `qgen report --qc <batch> --changes "<task ids>"` (or `"none"`) writes the report's "Changes from this QC" line.
5. **Next batch waits.** The next batch task runs only after both decisions are answered and the change tasks are done (they outrank it; plan 17 "Per-batch pattern").

## Never

- Change prompts, house style or `qgen.py` inside a batch run or a QC task; only in the change tasks of step 4.
- Answer the spot-check decision or spot-check questions as an LLM; the spot check is the gamemaster's.
- Approve or reject questions because of an audit finding; the gamemaster decides them in the review tool.
