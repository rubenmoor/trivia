# RUNBOOK — Making a batch of questions with an LLM

This is the **only** procedure for an LLM (for example Claude Code) asked to make, generate, add, review or approve new questions. Follow it exactly. Don't add steps, skip steps or improvise around a failure. Why it works this way: `plans/19-repo-layout.md`, D-36.

One command does all the work: choosing subcategories, drafting, rating, fact-checking, revising, merging, finding media, reviewing each question and its media, recording the decisions, exporting the playable pool, and writing a report. The judgement calls happen inside that command, in prompts the gamemaster maintains (`authoring/tools/prompts/`).

## Steps

1. **Check the tree.** Run `git status --porcelain`. If it prints anything, stop and tell the user: "The working tree has uncommitted changes; commit or stash them before a batch." Don't commit or stash them yourself.
2. **Run the batch.** In the repo root, run:

   ```sh
   qgen batch
   ```

   Outside the dev shell, use `nix develop -c qgen batch`. Give it no arguments. It takes from several minutes to an hour; let it finish.
3. **Act on the exit code:**

   | Exit code | Meaning | What you do |
   |---|---|---|
   | 0 | The batch is done | Go to step 4 |
   | 75 | Claude's usage limit | Stop. Tell the user the batch stopped at a usage limit and quote the message, including the reset time. When the user says to continue, go back to step 2 (same command) |
   | 1 | A step failed | Run step 2 again. If it fails at the **same step three times in a row**, stop and give the user the last 30 lines of output verbatim |
   | other | Unexpected | Stop and give the user the last 30 lines of output verbatim |

   If the output says "More than one unfinished batch", stop and ask the user which one to finish.
4. **Commit.** Run exactly the two `git add` / `git commit` lines printed after "Commit exactly this:". Nothing else goes into the commit. Don't push unless the user asks.
5. **Report.** Tell the user the "Done:" line, the path of the report (`authoring/reports/<batch>.md`), and that they can check the questions at http://127.0.0.1:8001/review?batch=<batch> (run `trivia-authoring`).

## Never

- Edit `authoring/data/questions.json`, `app/data/pool.json` or anything in `work/` by hand.
- Pick, change or judge media yourself, or search Commons yourself.
- Change prompts, `qgen.py`, `media.py` or the subcategory list to get past a failure.
- Run single pipeline steps (`qgen fit`, `qgen review`, …) or pass arguments to `qgen batch`. They exist for the gamemaster's debugging.
- Approve, reject or revise questions that `qgen batch` marked `needs_work`. The gamemaster decides those in the review tool.

## What the batch does (for reference)

The fixed rules are in `authoring/tools/qgen.py` (`cmd_batch`):

- **Name:** `batch-<n>`, one more than the highest so far. An unfinished batch is resumed instead.
- **Subcategories:** the 30 with the fewest approved questions (ties in `app/data/categories.json` order).
- **Steps:** fit → draft → rate → factcheck → revise → apply → rate → factcheck → merge → media → sheets → review → research → sheets → review → record → export → sync → batch-report → validate. Each skips work already done, so rerunning continues where it stopped.
- **Review:** one Claude call per question (`prompts/review.md`). It sees the question, the rater's notes, the fact check, related pool questions, and a contact sheet of the media candidates, and answers with a decision and a pick.
- **Fixed rules on top of the review:** no adequate media after one new search, or a fact check that isn't confirmed, makes a question `needs_work`. Reviews are recorded as `reviewer: "llm"` with the model's id (D-33).
