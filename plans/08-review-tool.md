# 08 — Question Review Tool

**Status:** draft

## Purpose
A local web page where the gamemaster reviews generated questions one at a time and decides on each with a single key press: **approve**, **reject**, or **give feedback**. It covers QG-11 (reviewing the pilot) and QG-12 (the review page) in `07-question-generation.md`. It is the first piece of the real app, so it sets up the stack and folder layout the game will reuse.

## Stack (D-3, D-4, D-5)
- **Server:** Python, standard library only (`http.server`, `json`). It serves the built client and a small JSON API.
- **Client:** Svelte 5 + Vite + TypeScript. In development, Vite's dev server forwards `/api` to the Python server. For normal use, `vite build` produces static files that the Python server serves.
- **No SQLite yet.** Review results are question content, not game state (see "Where results are stored").

## Folder layout (D-35, `19-repo-layout.md`)
The review tool is an authoring tool and never ships:
```
authoring/server/main.py   authoring server on port 8001: question API + static files
authoring/ui/src/review/   review screen (Svelte); src/lib/ adds the authoring types and API
authoring/data/questions.json
```
After every change the server re-exports `app/data/pool.json`, which the game reads.

## Screen
One question per screen, everything visible at once. Unlike the game, nothing is hidden:
- **Header:** progress ("23 / 100"), counts so far (approved / rejected / feedback), the question's ID, subcategory, style and difficulty.
- **Description:** the humorous intro, styled roughly as on the TV.
- **Question.**
- **Options:** all four. The correct answer is highlighted; the wrong answers are in the same order as in the file (no shuffling).
- **Hints:** 1–3, in order.
- **Media:** the image, audio or video if it has been cached already. Otherwise the type, role, search query and note as text (the pilot has no media yet).
- **Fun fact.**
- **Fact-check status:** confirmed or not checked.
- **Rater scores:** hidden by default, so the review is blind and can be compared with the rating pass (07, "Pilot before scaling"). One key toggles them.
- **Previous decision:** shown if the question was already reviewed, including earlier feedback.

## Keyboard
Single keys, no modifiers:

| Key | Action |
|---|---|
| `a` | Approve, go to the next question |
| `r` | Reject, go to the next question |
| `f` | Open the feedback box |
| `Enter` | (in the feedback box) save the feedback, go to the next question |
| `Esc` | (in the feedback box) cancel |
| `→` / `←` | Next / previous question without deciding |
| `s` | Show / hide rater scores |
| `u` | Undo the last decision and go back to that question |
| `d`, a number, Enter | Set the difficulty on the shared scale 1–15 (D-38): type the number, Enter saves, Backspace corrects, Esc cancels. The first change keeps the generator's value in `difficulty_original` (for calibrating difficulty estimates). |
| `c` | Show / hide the alternative media candidates |
| `b` | Show / hide the alternative background images (audio questions only, D-14) |
| `1`–`6` | (only while alternatives are shown) pick media candidate n; downloads it (`06-images.md`) |
| `m` | New search term for the shown alternatives (background if `b` is open, else media); fetches fresh candidates and shows them |

If no media has been picked yet, the first Commons candidate is shown as the **suggestion**, and `a` picks it automatically before approving. A good suggestion therefore needs no extra key.

Every failed API call (decisions, difficulty, media picks and searches, background downloads) appears in an error panel in the top-right corner, saying what failed, for which question and why. Errors stay until dismissed. A Commons rate limit is reported immediately ("try again in about N s") instead of the server waiting silently; only the batch command `media.py fetch` waits rate limits out.

Browser extensions that grab single keys (e.g. Vimium uses digits as count prefixes, `f` for link hints) must be switched off for `http://127.0.0.1:8001/*`. Opening the tool with `&debug=keys` shows what the browser reports for each key press.

While the feedback box is open, all other shortcuts are off so typing works normally. Each action shows a short confirmation ("✓ approved"), so a mistaken key press is noticed. Buttons with the same actions are on screen too, labelled with their key.

## What gets reviewed
- By default: every question from one batch that no human has reviewed yet, e.g. `?batch=pilot`: drafts and LLM-reviewed questions (D-33). An LLM-reviewed question shows the LLM's decision and feedback; a human decision replaces it and keeps it in `review.previous`. The pilot is identified by a new `batch` field (the `qgen.py` run name, set by `merge`).
- Undecided questions come first, in pool order. Already-decided ones stay reachable with `←` so decisions can be changed.
- The tool lives at `/review` (D-25). The URL carries the current question (`/review?batch=pilot&id=q-0123`). Opening or reloading that URL shows that question; without `id`, the first undecided one. `/review/q-0123` reviews just that one question, whatever its status (linked from the admin overlay, 04): after a decision it stays on the question. Decisions are saved in `authoring/data/questions.json` immediately, so nothing is lost when the server restarts.
- When all are decided: a summary screen with the counts and the share kept (the keep rate for QG-11).

## Revised questions (QG-13)
A question with a `revision` field shows a panel above the question: the reason, and for each changed field the old value next to the new one. A revision with `action: "drop"` shows as **proposed reject**: `r` confirms it, `a` or `f` overrules it.

## Where results are stored
In `authoring/data/questions.json`, on the question itself. Review results describe the question content and must be readable by the pipeline (e.g. to rework questions or tune prompts), so they belong with the questions, not in the game's SQLite state (D-4).

Proposed schema changes (in `02-question-pool.md` once agreed):
- `status` gains the value `"needs_work"`: the question has feedback and should be reworked.
- New field `review`:
  ```jsonc
  "review": {
    "decision": "approved",            // approved | rejected | needs_work
    "feedback": "demasiado difícil",   // free text, null when there is none
    "reviewed_on": "2026-10-07",
    "reviewer": "human"                // human | llm, plus "model" and "previous" (D-33, 02)
  }
  ```
- New field `batch`: the pipeline run that produced the question (`null` for the first 120).

The decision keys set `status` and `review` together. Feedback sets `status: "needs_work"`.

## API
- `GET /api/questions?batch=pilot&status=draft&reviewer=llm`: the matching questions (`reviewer`: human, llm or none).
- `POST /api/questions/<id>/review` with `{decision, feedback}`: updates one question and returns it.
- Every write re-reads `authoring/data/questions.json`, changes the one question, and writes atomically (temp file + rename). That way nothing is lost if `qgen.py` touched the file in the meantime. Don't run `qgen.py merge` while reviewing.

## What happens to feedback afterwards (later, not part of this tool)
- A `qgen.py rework` step sends each `needs_work` question with its feedback to Claude for a revised version. The revision goes back to `draft` for another review.
- For QG-11: collected feedback and rejections show which styles, levels and prompt rules need changing before scaling up.

## Meaning of the three decisions (D-11)
- **Approve:** the question is good as it is.
- **Reject:** the question is unsalvageable; it will never be reworked. No reason needed, so rejecting stays one key press.
- **Feedback:** the question is salvageable but needs changes; the feedback says what. It goes to `needs_work` and later to `qgen.py rework`.

## Start page `/` (RV-12..RV-17)
**Why.** `trivia-authoring` prints `/` first, but `/` is the review screen without a filter: it walks all 513 questions, and the first "open" one is any of the 293 LLM-approved questions (D-33). Nothing tells the gamemaster what is waiting for them. The start page answers "what needs me now?" in one look, and every number on it is a link to the queue that works it off.

**Rules.**
- Read-only: no keys, no decisions. All work happens in the existing pages it links to.
- Computed fresh on every load from `authoring/data/questions.json` (plus `work/`, `authoring/reports/` and the game save where named below). No caching, no new stored state.
- Old links keep working: `/` with `batch`, `bundle` or `id` in the query redirects to `/review` with the same query. `/review` without a filter stays as it is.
- The full charts live on `/stats/…`; the start page shows them compact and links to them.

**Sections, top to bottom:**
1. **Waiting for you.** One line per queue, with its count, hidden when it is 0:
   - `needs_work` questions (now 20) → `/review?status=needs_work`. Only a human decides these (RUNBOOK).
   - Drafts nobody reviewed (now 1) → `/review?status=draft`.
   - Approved questions without picked media (now 122, QP-6) → `/review?media=missing`.
   - Bundle proposals not checked by a human (`colombia`, now 79) → `/review?bundle=colombia`.
   - Picked files not in the cache → the command to run: `trivia-media sync --status approved`.
   - An unfinished `qgen batch` run in `work/` (`run.json` without `done`) → "resume with `qgen batch`".
2. **Check the LLM's approvals** (optional, D-42): questions only an LLM has approved so far, all together → `/review?status=approved&reviewer=llm`, and per batch → `/review?batch=<name>&status=approved&reviewer=llm`. Below section 1 on purpose: `needs_work` and the other queues there come first.
3. **Batches.** A table, newest first: name, date (latest `reviewed_on` in the batch), merged, approved, needs_work, rejected, share reviewed by a human; links to `/review?batch=<name>` and the batch report (`authoring/reports/<name>.md`, when it exists). `batch=none` is the first 120.
4. **Game readiness.** Supply per game level 1–12 for a new player (the numbers `qgen report` prints: candidates per level, a game needs 4, D-22), with missing levels flagged; one row per player from the game save when it exists (burned questions, D-28). The difficulty spread itself is in section 5.
5. **Approved questions.** The statistics below ("Statistics on approved questions"), in compact form: the difficulty histogram, the category bars with their subcategories, and the sparse list. Each one links to its full page under `/stats/…`.
6. **Go to.** A box that opens `/review/<id>` for a typed id (`q-0123` or `123`); links to `/stats/categories`, `/stats/difficulty`, `/comodines`; the counts by status and by bundle as a footer line.

**API.** `GET /api/overview` returns everything above except the statistics (they use `/api/questions?status=approved` like the stats pages) in one JSON object, built on the server so the page doesn't fetch the whole pool with media candidates. It reuses `selection.supply` / `selection.burned_ids` (`app/server/`, allowed by D-35) and the same unfinished-run test as `qgen.next_batch`; that test moves into a small shared helper rather than being copied. Reading the game save is read-only; when `state/` doesn't exist the per-player rows are left out.

**New review filters**, so the links above open the right queue: `GET /api/questions` and the review screen accept `status=<status>` and `reviewer=human|llm|none` (the API already does both), `media=missing` (approved questions whose media has no picked file) and `subcategory=<name>` (new in the API too). The URL keeps them like `batch` and `bundle`.


## Statistics on approved questions (RV-18..RV-21)
The stats pages (QP-13, `/stats/categories`, `/stats/difficulty`) count approved questions only, the ones a game can use. They get three fixes and one new page, and the start page shows them compact (section 5 above). Today: 483 approved, 24 categories, 140 subcategories.

- **Difficulty histogram over the whole scale 1–15** (D-38). It stops at 10 today, so a difficulty of 11–15 set in the review tool (AG-9) isn't counted. Mark the young-teen window (1–10, `app/data/age-groups.json`) on the axis, so the thin top end (9: 26, 10: 2, B-6) is visible at a glance.
- **Category and subcategory breakdown.** The category bars stay sorted by count. Clicking a bar opens its subcategories as bars below it, instead of the hover-only tooltip, so the breakdown also works without a mouse and can stay open. A new page, `/stats/subcategories`, lists all 140 subcategories grouped by category, with the count of each and a link to `/review?subcategory=<name>&status=approved`.
- **Sparse areas.** One list, worst first, on `/stats/subcategories` and on the start page:
  - **Categories with fewer than 12 approved questions.** A game asks 12 questions, so below that a category can't cover every level even once. Today that's 5: Amazonas 9, Cuerpo humano 11, Espacio 11, Videojuegos 11, Fútbol 11.
  - **Subcategories with fewer than 3 approved questions.** One player sees them all in one or two games. Today that's 27 (none is empty).
  - Each sparse subcategory is marked if the next `qgen batch` will pick it (the 30 with the fewest approved questions, `qgen.batch_subcategories`). Then the gamemaster can see whether the next batch fixes the gap or whether it needs a bundle or a top-up (B-6).

  The two limits are constants at the top of the component, so they're easy to change.
- **Filters.** Every page keeps "approved questions only" (gamemaster, 2026-10-06). A bundle switch (all / `base` / `colombia`) reads `?bundle=`, so the family's default (every bundle on) and a single bundle can both be checked (M11).

## Tasks
- [x] RV-1 Agree the schema changes (`needs_work`, `review`, `batch`) and record them in `02-question-pool.md`. *2026-10-06.*
- [x] RV-2 Scaffold `server/` and `client/` (ARC-2, ARC-3) with run commands in `AGENTS.md`. *2026-10-06, `server/`, `client/`, `shell.nix` (D-12).*
- [x] RV-3 Server: static files + `GET /api/questions` + `POST /api/questions/<id>/review` with atomic writes. *2026-10-06, then `server/main.py`, now `authoring/server/main.py` (D-35); media paths restricted to `images/` and `media/`.*
- [x] RV-4 Client: review screen showing every part of a question. *2026-10-06, `authoring/ui/src/review/Review.svelte`.*
- [x] RV-5 Client: keyboard shortcuts, feedback box, undo, confirmation messages. *2026-10-06.*
- [x] RV-6 Client: summary screen at the end of a batch. *2026-10-06.*
- [x] RV-7 `qgen.py merge` sets `batch`; `validate` knows the new fields and status. *2026-10-06.*
- [x] RV-8 Try it on the 120 existing questions before the pilot runs (`/?batch=none`). *2026-10-06, approved by the gamemaster; "level" renamed to "difficulty n/10".*
- [x] RV-9 Show revisions (reason, old → new per field, proposed reject). *2026-10-06, `authoring/ui/src/review/RevisionPanel.svelte`.*
- [x] RV-10 Single-question review at `/review/<id>`; links between the review tool and the stats pages. *2026-10-07.*
- [x] RV-11 Human review of LLM-reviewed questions (D-33): they count as open, show the LLM's verdict, and the summary counts them. *2026-10-07, QP-15.*

### Start page and statistics: order of work
One task = one commit, top to bottom (each builds only on the ones above it):

- [x] RV-13 Review filters `status`, `reviewer`, `subcategory` and `media=missing` in the API and the review screen (URL, empty-queue message). *2026-10-09, `authoring/server/main.py`, `authoring/ui/src/review/Review.svelte`.*
- [x] RV-15 Serve batch reports at `/reports/<name>.md` (plain text, names restricted to `authoring/reports/*.md`) for the batches table. *2026-10-09, `authoring/server/main.py` (`send_report`).*
- [ ] RV-12 `GET /api/overview`: queues, unfinished run, batches table, supply per level (new player + players from the save), the next batch's subcategories. The unfinished-run test and the subcategory choice move from `qgen.py` into a shared helper.
- [ ] RV-18 Difficulty histogram over 1–15 with the young-teen window marked.
- [ ] RV-19 Category bars open their subcategories on click; new page `/stats/subcategories` with links to review.
- [ ] RV-20 Sparse list (categories < 12, subcategories < 3, marked if the next batch picks them) on `/stats/subcategories`.
- [ ] RV-21 Bundle switch (`?bundle=`) on the stats pages.
- [ ] RV-14 Start page `authoring/ui/src/home/Home.svelte`: sections 1–6, with compact versions of the histogram, category bars and sparse list; `App.svelte` routes exactly `/` to it; `/` with `batch`/`bundle`/`id` redirects to `/review`.
- [ ] RV-16 One nav bar on the start page, the stats pages and the review summary ("Start", "Stats", "Review"); the server's startup line and AGENTS.md name `/` as the start page.
- [ ] RV-17 (later, not in this round) `qgen validate` result on the start page: errors and warnings, without the exit. Needs `cmd_validate` split into a function that returns its findings.
