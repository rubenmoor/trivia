# RUNBOOK — Making a batch of questions with an LLM

This is the **only** procedure for an LLM (for example Claude Code) asked to make, generate, add, review or approve new questions. Follow it exactly. Don't add steps, skip steps or improvise around a failure. Why it works this way: `plans/19-repo-layout.md`, D-36.

One command does all the work: choosing subcategories, drafting, rating, fact-checking, revising, merging, finding media, reviewing each question and its media, recording the decisions, exporting the playable pool, and writing a report. The judgement calls happen inside that command, in prompts the developer maintains (`authoring/tools/prompts/`).

## Steps

1. **Check the tree.** Run `git status --porcelain`. If it prints anything, stop and tell the user: "The working tree has uncommitted changes; commit or stash them before a batch." Don't commit or stash them yourself. Under `pm run`: see below.
2. **Run the batch.** In the repo root, run:

   ```sh
   qgen batch
   ```

   Outside the dev shell, use `nix develop -c qgen batch`. This writes questions for the `base` bundle, drafted in English (plan 148). Give it no arguments, with one exception: if the user names a bundle ("make Colombia questions", "a batch for the colombia bundle"), run `qgen batch --bundle <id>` with that bundle's id from `app/data/bundles.json`. If the user names a language ("translate questions into German", "Spanish questions"), run `qgen batch --translate <locale>` with that language's locale instead (D-87): `es` (Latin American Spanish, also plain "Spanish"), `es-ES` (Spain's Spanish), `en`, `de`; if they name a bundle too ("translate the Colombia questions into English"), add `--bundle <id>`. Use the same command, with the same `--bundle` or `--translate`, every time you rerun it in step 3. It takes from several minutes to an hour; let it finish. When Claude's usage limit is hit, it says so, waits until 5 minutes after the reset (possibly hours) and continues by itself; let it wait.
3. **Act on the exit code:**

   | Exit code | Meaning | What you do |
   |---|---|---|
   | 0 | The batch is done | Go to step 4 |
   | 75 | Claude's usage limit without a reset time it could read | Stop. Tell the user the batch stopped at a usage limit and quote the message, including the reset time. When the user says to continue, go back to step 2 (same command) |
   | 1 | A step failed | Run step 2 again. If it fails at the **same step three times in a row**, stop and give the user the last 30 lines of output verbatim (they end with the `claude:` line) |
   | other | Unexpected | Stop and give the user the last 30 lines of output verbatim |

   If the output says "More than one unfinished batch", stop and ask the user which one to finish. If it says a batch "is unfinished and writes for bundle …", stop and tell the user. Run the command it names only if they say so. Under `pm run`, "stop" and "tell the user" mean a pm decision: see below.
4. **Commit.** Run exactly the two `git add` / `git commit` lines printed after "Commit exactly this:". Nothing else goes into the commit. Don't push unless the user asks. Under `pm run`: stage only, see below.
5. **Report.** Tell the user the "Done:" line, the `claude:` line (calls, tokens, $; printed last, also on a failure or stop, decision 208), the path of the report (`authoring/reports/<batch>.md`; `tr-<locale>-<n>.md` for a translation run), and that they can check the questions at http://127.0.0.1:8001/review?batch=<batch> (run `trivia-authoring`). Quality control of the batch follows `authoring/QC.md`; it is the developer's, not part of this procedure. Under `pm run`: into the task's note, see below.

## Under `pm run`

A pm worker (environment `PM_WORKER=1`) follows the steps above with these changes; everything else holds as written. `<task>` is the worker's task id (`PM_TASK`), `<batch>` the run's name from the output.

- **Step 1:** `tasks.sql` alone in `git status --porcelain` doesn't count as dirty; anything else does: stop as below.
- **Step 2:** run it in the foreground with the longest Bash timeout (`3600000`); a timeout isn't a failure: run the same command again (it resumes).
- **Step 3, "stop":** never wait for an answer in the session. Instead:
  - `pm decision add "<subject>" --body - <<'EOF'` with the body below; prints the decision id
  - `pm task-pending-decision <task> <id>`
  - stage nothing, don't `pm task done`; end the turn
  - health ✗ (decision 414: reviews don't gate generation): the run goes on, never a stop. A ✗ warning on stderr (`warning: <run> fails … thresholds`) or a ✗ in the run's report → `pm decision list --grep "<run>: health"`; none → `pm decision add "<run>: health ✗, look at it?"` with the warning verbatim as body (once per run, for every bundle and locale); never `pm task-pending-decision`; finish the task as usual
- **Step 3, exit 1 at the same step three times in a row:** no decision (decision 205); the queue doesn't wait for the developer on script bugs:
  - partial batch: `qgen validate`; passes → `git add authoring/data` (`work/<batch>` stays); fails → stop as above, subject `<batch>: qgen validate fails after <step>`, body its output
  - fix task in the batch task's plan: `pm task add <plan> "Fix qgen <step>: <cause>" --priority 0`; body: failing step, last 30 lines, your read-only diagnosis (file, cause, suggested fix), how to check it
  - resume task in the same plan: `pm task add <plan> "Finish <batch> after task <fix id>: <fix subject>" --priority -99`; body: follow this RUNBOOK, plain `qgen batch` resumes
  - `pm task done <task> "<YYYY-MM-DD>, stopped at <step>; fix: task <id>, resume: task <id>"`
  - still never edit qgen code yourself (Never, below)
- **Subjects and bodies:**

  | Case | Subject | Body |
  |---|---|---|
  | exit 75 | `Continue <batch> after the usage limit?` | the usage-limit message, incl. the reset time |
  | health ✗ (not a stop) | `<run>: health ✗, look at it?` | the warning verbatim |
  | other exit code | `<batch>: exit <code>, how to go on?` | last 30 lines verbatim |
  | "More than one unfinished batch" | `Which unfinished batch to finish?` | the message |
  | "is unfinished and writes for bundle …" | `Unfinished batch for another bundle: run the named command?` | the message |
  | step 1: dirty tree | `Dirty tree before <task>'s batch: what to do?` | `git status --porcelain` |

- **Step 4:** run exactly the printed `git add` line(s); don't run the printed `git commit` (pm commits as "task N: …"). Same for `qgen rework`, `tighten`, `neutralize`, `audit --backlog`.
- **Step 5:** `pm task done <task> "<YYYY-MM-DD>, Done: <the Done: line>, <the claude: line>, report <path>"`.
- **Every stop** (decision, fix task, `pm task done`): the `claude:` line of each `qgen` run in the task goes into the task's note or the decision's body (decision 208).

## Never

- Edit `authoring/data/questions.json`, `app/data/pool.json` or anything in `work/` by hand.
- Pick, change or judge media yourself, or search Commons yourself.
- Change prompts, `qgen.py`, `media.py` or the subcategory list to get past a failure.
- Run single pipeline steps (`qgen concepts`, `qgen review`, …) or pass arguments to `qgen batch` other than a `--bundle` or `--translate` the user named. They exist for the developer's debugging.
- Create bundles (`qgen bundle new`), run `qgen taxonomy`, or edit any bundle's categories or category names (`names.<locale>.json`). That is the developer's call.
- Approve, reject or revise questions that `qgen batch` marked `needs_work`. The developer decides those in the review tool, or asks for `qgen rework`: then run exactly that (with `--batch` only if the user names one), act on the exit code as in step 3, and commit what it prints. The same goes for `qgen tighten` and `qgen neutralize` (no arguments) when the developer asks for them.
- Run `qgen audit --backlog` unless the developer asks for it (with `--slice N` only if they name a size); act on the exit code as in step 3 and commit what it prints.

## What the batch does (for reference)

The fixed rules are in `authoring/tools/qgen.py` (`cmd_batch`):

- **Name:** `batch-<n>`, one more than the highest so far. An unfinished batch is resumed instead.
- **Bundle:** `base` unless `--bundle` names another one (D-41). Every question of the batch is in that bundle.
- **Draft language (plan 148, decision 235):** `base` drafts English (`locale: "en"`, from batch-9 on), a regional bundle its region's language and variety, the first of its `languages` and its `voice` (`colombia`: Colombian Spanish; a British bundle British English); every step works on the question's own language. `base`'s questions up to batch-8 stay es-sourced.
- **Size (D-46):** half of the bundle's subcategories (rounded up), 18 draft slots each; for `base` about 1000 drafts and 700 merged questions. Expect to hit Claude's usage limit and resume (step 3).
- **Subcategories:** the half with the fewest approved questions in that bundle, each weighted by its level's share of the gaps to `authoring/data/targets.json` (D-54; `base`: the draft gap over the four question locales, D-107; ties in the order of the bundle's categories file: `app/data/categories.json` for `base`, `app/data/bundles/<id>/categories.json` for another bundle, D-43). Keys are English slugs (decision 259), the same in every language; prompts and the report show names from `names.<locale>.json`.
- **Steps:** concepts → draft → english-keys (en batches) → rate → factcheck → revise → apply → rate → factcheck → merge → media → sheets → review → fix → research → media → sheets → review → record → audit → export → sync → batch-report → validate. Each skips work already done, so rerunning continues where it stopped.
- **English keys (decision 232):** an en batch's overlap checks (rate's candidates, merge's duplicates) see every source in another language through its en translation, else through `authoring/data/english-keys.json` (English answer + concept, `prompts/english-keys.md`); the step asks only new or changed sources. Commit the file with the batch.
- **Review:** one Claude call per question (`prompts/review.md`). It sees the question, the rater's notes, the fact check, related pool questions, and a contact sheet of the media candidates, and answers with a decision and a pick.
- **Fix (QG-22):** for every text problem it can fix (a giveaway hint, a wrong fact, a second defensible option), the review says how in `fix`; the `fix` step revises the question once, fact-checks changed facts again, and the review looks at it again. Only what can't be fixed stays `needs_work`.
- **Fixed rules on top of the review:** no adequate media after one new search, or a fact check that isn't confirmed, makes a question `needs_work`. Reviews are recorded as `reviewer: "llm"` with the model's id (D-33).
- **Translation runs (`--translate <locale>`, D-87):** run `tr-<locale>-<n>`; 300 approved sources of one bundle (`base`, or the `--bundle` named; the language's first run: a 50-question pilot) in any language but the target (en → `es`, `es-ES`, `de`; es → `en`, `de`, `es-ES`), stale translations first, then the demo list's untranslated ids (`base`), then the subcategories with the fewest approved translations. Steps: translate → rate → factcheck → merge → review → fix → review → record → audit → export → validate → batch-report; rating and fact check for the target's market (`es`: Latin America, `es-ES`: Spain). Translations go to `authoring/data/questions.<locale>.json`, the pool to `app/data/pool.json` (`es`) or `pool.<locale>.json`; a pack's translations go to `app/data/bundles/<id>/pool.<locale>.json` (decision 112). Questions that don't travel (wordplay, about the source language itself) get no translation; once the review confirms, they become `translatable: false`. A run failing a health threshold is reported and raised as a decision, never a stop (decision 414); the developer's `qgen health ack tr-<locale>-<n> "<note>"` records their look; and no spot check or QC follows a `tr-*` run (milestone 9).
- **Audit (plan 16):** after `record`, a second Claude call reads a seeded sample of 60 questions without seeing the review (`prompts/audit.md`). It never approves or rejects anything; its findings go into the report's "Audit" section.
