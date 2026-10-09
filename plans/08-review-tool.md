# 08 — Question Review Tool

**Status:** draft

## Purpose
A local web page where the gamemaster reviews generated questions one at a time and decides on each with a single key press: **approve**, **reject**, or **give feedback**. It covers QG-11 (reviewing the pilot) and QG-12 (the review page) in `07-question-generation.md`. It is the first piece of the real app, so it sets up the stack and folder layout the game will reuse.

## Stack (D-3, D-4, D-5)
- **Server:** Python, standard library only (`http.server`, `json`). It serves the built client and a small JSON API.
- **Client:** Svelte 5 + Vite + TypeScript. In development, Vite's dev server forwards `/api` to the Python server. For normal use, `vite build` produces static files that the Python server serves.
- **No SQLite yet.** Review results are question content, not game state (see "Where results are stored").

## Proposed folder layout (ARC-2)
```
server/            Python server (API + static files)
client/            Svelte app (review tool now, game later)
  src/review/      review screen
  src/lib/         shared types (Question) and components
data/questions.json
tools/             question pipeline (qgen.py)
```

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
| `d`, then a digit | Set the difficulty: `1`–`8` as they are, `0` → 1, `9` → 10. The first change keeps the generator's value in `difficulty_original` (for calibrating difficulty estimates). |
| `c` | Show / hide the alternative media candidates |
| `b` | Show / hide the alternative background images (audio questions only, D-14) |
| `1`–`6` | (only while alternatives are shown) pick media candidate n; downloads it (`06-images.md`) |
| `m` | New search term for the shown alternatives (background if `b` is open, else media); fetches fresh candidates and shows them |

If no media has been picked yet, the first Commons candidate is shown as the **suggestion**, and `a` picks it automatically before approving. A good suggestion therefore needs no extra key.

Every failed API call (decisions, difficulty, media picks and searches, background downloads) appears in an error panel in the top-right corner, saying what failed, for which question and why. Errors stay until dismissed. A Commons rate limit is reported immediately ("try again in about N s") instead of the server waiting silently; only the batch command `media.py fetch` waits rate limits out.

Browser extensions that grab single keys (e.g. Vimium uses digits as count prefixes, `f` for link hints) must be switched off for `http://127.0.0.1:8000/*`. Opening the tool with `&debug=keys` shows what the browser reports for each key press.

While the feedback box is open, all other shortcuts are off so typing works normally. Each action shows a short confirmation ("✓ approved"), so a mistaken key press is noticed. Buttons with the same actions are on screen too, labelled with their key.

## What gets reviewed
- By default: every question with `status: "draft"` from one batch, e.g. `?batch=pilot`. The pilot is identified by a new `batch` field (the `qgen.py` run name, set by `merge`).
- Undecided questions come first, in pool order. Already-decided ones stay reachable with `←` so decisions can be changed.
- The tool lives at `/review` (D-25). The URL carries the current question (`/review?batch=pilot&id=q-0123`). Opening or reloading that URL shows that question; without `id`, the first undecided one. Decisions are saved in `data/questions.json` immediately, so nothing is lost when the server restarts.
- When all are decided: a summary screen with the counts and the share kept (the keep rate for QG-11).

## Start page (`/review` without parameters)
**Today:** bare `/review` loads the whole pool (316 questions, every batch and status mixed) and jumps to the first draft anywhere. The stats pages link there, so the most common way in drops the gamemaster into an arbitrary question with no overview. The start page replaces that: it answers "what is waiting for me, and where?" and links straight into the right review run.

**When it shows:** only when the URL has no `batch`, `id` or `queue` parameter. Every existing URL keeps working; `/review?batch=all` opens the old whole-pool run.

**Data:** one `GET /api/questions` call, everything computed in the client (the stats pages already do this; the pool is about 0.7 MB). No new server endpoint, no new stored fields.

**Content, top to bottom:**
1. **Navigation bar** (same style as the stats pages): Review · Stats: categories · Stats: difficulty · Joker cards · Game.
2. **Pool totals:** total questions, then approved / open (draft) / needs work / rejected, as one line of counts. Plus "approved without picked media: n" (QP-6) because it decides what `media.py sync` can cache.
3. **Work queues:** one line per queue with its count and a link; queues with count 0 are greyed out, not hidden. Each link opens the normal review screen over just those questions, across all batches (`/review?queue=<name>`):

   | Queue | Questions | Why |
   |---|---|---|
   | `open` | `status: "draft"` | not decided yet |
   | `revisions` | has a `revision` field (QG-13) | proposed changes waiting for a decision |
   | `needs-work` | `status: "needs_work"` | feedback given, waiting for `qgen.py rework`; useful to re-read before a rework run |
   | `no-media` | approved, media slot (or background for audio, D-14) has no `file_url` | QP-6; pick media with `c` / `1`–`6` |
   | `unchecked` | `fact_checked` not `true` | fact-check uncertain or missing |
   | `claude` | `review.reviewer == "claude"` (D-32) | spot-check Claude's decisions |

4. **Batches table:** one row per `batch` value (`first-120`, `pilot`, `batch-3`, …; questions without a batch as `none`). Columns: name · total · open · approved · needs work · rejected · keep rate (as on the summary screen) · media picked (n / total) · last `reviewed_on`. The name links to `/review?batch=<name>` (opens at the first undecided question, or the summary screen when there is none). Order: batches with open questions first, then by last `reviewed_on`, newest first. A last row "all" links to `/review?batch=all`.
5. **Jump to a question:** a text field for a question ID (`q-0123`); `Enter` opens `/review?id=q-0123` (whole pool, so `←` / `→` still work). Unknown IDs show "not found" under the field.

**Keyboard on the start page:** `Enter` opens the first non-empty queue in table order (`open`, then `revisions`, …), `/` focuses the ID field. Nothing else, so typing in the field never triggers anything.

**Getting back:** the review screen header and the "Batch done" summary get a "← overview" link to `/review`; key `o` does the same (not while the feedback or search box is open). The stats pages' "Review tool →" link then lands on the start page by itself.

**Review screen changes for queues:** `queue=<name>` filters the loaded list in the client by the rule in the table; it combines with `batch` (`?batch=pilot&queue=no-media`). The header shows the queue name next to the progress ("no-media · 3 / 14"). A question that leaves the queue through a decision stays in the list until reload, so `u` and `←` still work. For `no-media` and `revisions` the "first undecided" rule doesn't fit (they are often approved already): the run starts at the first question of the queue, and "done" means the queue is empty after reload.

## Revised questions (QG-13)
A question with a `revision` field shows a panel above the question: the reason, and for each changed field the old value next to the new one. A revision with `action: "drop"` shows as **proposed reject**: `r` confirms it, `a` or `f` overrules it.

## Where results are stored
In `data/questions.json`, on the question itself. Review results describe the question content and must be readable by the pipeline (e.g. to rework questions or tune prompts), so they belong with the questions, not in the game's SQLite state (D-4).

Proposed schema changes (in `02-question-pool.md` once agreed):
- `status` gains the value `"needs_work"`: the question has feedback and should be reworked.
- New field `review`:
  ```jsonc
  "review": {
    "decision": "approved",            // approved | rejected | needs_work
    "feedback": "demasiado difícil",   // free text, null when there is none
    "reviewed_on": "2026-10-07"
  }
  ```
- New field `batch`: the pipeline run that produced the question (`null` for the first 120).

The decision keys set `status` and `review` together. Feedback sets `status: "needs_work"`.

## API
- `GET /api/questions?batch=pilot&status=draft`: the matching questions.
- `POST /api/questions/<id>/review` with `{decision, feedback}`: updates one question and returns it.
- Every write re-reads `data/questions.json`, changes the one question, and writes atomically (temp file + rename). That way nothing is lost if `qgen.py` touched the file in the meantime. Don't run `qgen.py merge` while reviewing.

## What happens to feedback afterwards (later, not part of this tool)
- A `qgen.py rework` step sends each `needs_work` question with its feedback to Claude for a revised version. The revision goes back to `draft` for another review.
- For QG-11: collected feedback and rejections show which styles, levels and prompt rules need changing before scaling up.

## Meaning of the three decisions (D-11)
- **Approve:** the question is good as it is.
- **Reject:** the question is unsalvageable; it will never be reworked. No reason needed, so rejecting stays one key press.
- **Feedback:** the question is salvageable but needs changes; the feedback says what. It goes to `needs_work` and later to `qgen.py rework`.

## Tasks
- [x] RV-1 Agree the schema changes (`needs_work`, `review`, `batch`) and record them in `02-question-pool.md`. *2026-10-06.*
- [x] RV-2 Scaffold `server/` and `client/` (ARC-2, ARC-3) with run commands in `AGENTS.md`. *2026-10-06, `server/`, `client/`, `shell.nix` (D-12).*
- [x] RV-3 Server: static files + `GET /api/questions` + `POST /api/questions/<id>/review` with atomic writes. *2026-10-06, `server/main.py`; media paths restricted to `images/` and `media/`.*
- [x] RV-4 Client: review screen showing every part of a question. *2026-10-06, `client/src/review/Review.svelte`.*
- [x] RV-5 Client: keyboard shortcuts, feedback box, undo, confirmation messages. *2026-10-06.*
- [x] RV-6 Client: summary screen at the end of a batch. *2026-10-06.*
- [x] RV-7 `qgen.py merge` sets `batch`; `validate` knows the new fields and status. *2026-10-06.*
- [x] RV-8 Try it on the 120 existing questions before the pilot runs (`/?batch=none`). *2026-10-06, approved by the gamemaster; "level" renamed to "difficulty n/10".*
- [x] RV-9 Show revisions (reason, old → new per field, proposed reject). *2026-10-06, `client/src/review/RevisionPanel.svelte`.*
- [ ] RV-10 Start page skeleton: `App.svelte` routes bare `/review` to a new `client/src/review/Overview.svelte`; navigation bar, pool totals; `?batch=all` keeps the whole-pool run.
- [ ] RV-11 Start page: batches table with counts, keep rate, media picked, last review date and links.
- [ ] RV-12 Queues: queue rules in one shared module (`client/src/review/queues.ts`) used by the start page counts and by `Review.svelte` for `?queue=`; header label; start position and "done" rule for `no-media` and `revisions`.
- [ ] RV-13 Jump-to-ID field, start page keys (`Enter`, `/`), "← overview" link and key `o` on the review screen and summary.
- [ ] RV-14 Update `AGENTS.md`, `README.md` and the server's start message (`/review` instead of `/review?batch=pilot`).
