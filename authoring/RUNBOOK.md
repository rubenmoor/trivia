# RUNBOOK — Making a batch of questions with an LLM

This is the **only** procedure for an LLM (for example Claude Code) asked to make, generate, add, review or approve new questions. Follow it exactly. Don't add steps, skip steps or improvise around a failure. Why it works this way: `plans/19-repo-layout.md`, D-36.

One command does all the work: choosing subcategories, drafting, rating, fact-checking, revising, merging, finding media, reviewing each question and its media, recording the decisions, exporting the playable pool, and writing a report. The judgement calls happen inside that command, in prompts the gamemaster maintains (`authoring/tools/prompts/`).

## Steps

1. **Check the tree.** Run `git status --porcelain`. If it prints anything, stop and tell the user: "The working tree has uncommitted changes; commit or stash them before a batch." Don't commit or stash them yourself.
2. **Run the batch.** In the repo root, run:

   ```sh
   qgen batch
   ```

   Outside the dev shell, use `nix develop -c qgen batch`. This writes questions for the `base` bundle. Give it no arguments, with one exception: if the user names a bundle ("make Colombia questions", "a batch for the colombia bundle"), run `qgen batch --bundle <id>` with that bundle's id from `app/data/bundles.json`. Use the same command, with the same `--bundle`, every time you rerun it in step 3. It takes from several minutes to an hour; let it finish.
3. **Act on the exit code:**

   | Exit code | Meaning | What you do |
   |---|---|---|
   | 0 | The batch is done | Go to step 4 |
   | 75 | Claude's usage limit | Stop. Tell the user the batch stopped at a usage limit and quote the message, including the reset time. When the user says to continue, go back to step 2 (same command) |
   | 1 | A step failed | Run step 2 again. If it fails at the **same step three times in a row**, stop and give the user the last 30 lines of output verbatim |
   | other | Unexpected | Stop and give the user the last 30 lines of output verbatim |

   If the output says "More than one unfinished batch", stop and ask the user which one to finish. If it says a batch "is unfinished and writes for bundle …", stop and tell the user. Run the command it names only if they say so.
4. **Commit.** Run exactly the two `git add` / `git commit` lines printed after "Commit exactly this:". Nothing else goes into the commit. Don't push unless the user asks.
5. **Report.** Tell the user the "Done:" line, the path of the report (`authoring/reports/<batch>.md`), and that they can check the questions at http://127.0.0.1:8001/review?batch=<batch> (run `trivia-authoring`).

## Never

- Edit `authoring/data/questions.json`, `app/data/pool.json` or anything in `work/` by hand.
- Pick, change or judge media yourself, or search Commons yourself.
- Change prompts, `qgen.py`, `media.py` or the subcategory list to get past a failure.
- Run single pipeline steps (`qgen concepts`, `qgen review`, …) or pass arguments to `qgen batch` other than a `--bundle` the user named. They exist for the gamemaster's debugging.
- Create bundles (`qgen bundle new`) or edit any bundle's categories. That is the gamemaster's call.
- Approve, reject or revise questions that `qgen batch` marked `needs_work`. The gamemaster decides those in the review tool.

## What the batch does (for reference)

The fixed rules are in `authoring/tools/qgen.py` (`cmd_batch`):

- **Name:** `batch-<n>`, one more than the highest so far. An unfinished batch is resumed instead.
- **Bundle:** `base` unless `--bundle` names another one (D-41). Every question of the batch is in that bundle.
- **Size (D-46):** half of the bundle's subcategories (rounded up), 18 draft slots each; for `base` about 1000 drafts and 700 merged questions. Expect to hit Claude's usage limit and resume (step 3).
- **Subcategories:** the half with the fewest approved questions in that bundle (ties in the order of the bundle's categories file: `app/data/categories.json` for `base`, `app/data/bundles/<id>/categories.json` for another bundle, D-43).
- **Steps:** concepts → draft → rate → factcheck → revise → apply → rate → factcheck → merge → media → sheets → review → research → sheets → review → record → export → sync → batch-report → validate. Each skips work already done, so rerunning continues where it stopped.
- **Review:** one Claude call per question (`prompts/review.md`). It sees the question, the rater's notes, the fact check, related pool questions, and a contact sheet of the media candidates, and answers with a decision and a pick.
- **Fixed rules on top of the review:** no adequate media after one new search, or a fact check that isn't confirmed, makes a question `needs_work`. Reviews are recorded as `reviewer: "llm"` with the model's id (D-33).
