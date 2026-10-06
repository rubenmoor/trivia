# Decision Log

Lightweight ADRs. Add new entries at the bottom and never edit old ones. If a decision changes, add a new entry that supersedes the old one.

Template:
```
## D-<n>: <title>
- Date:
- Context:
- Decision:
- Consequences:
- Supersedes / related: OQ-x, task IDs
```

## D-1: Plans-first workflow
- Date: 2026-10-06
- Context: The project is built with LLM assistance and needs a stable source of truth.
- Decision: Keep a `plans/` hierarchy with task IDs and status markers, plus `AGENTS.md` at the repo root.
- Consequences: Every change references a task ID, and plans are updated alongside code.

## D-2: Scope fundamentals
- Date: 2026-10-06
- Context: Initial brief from the gamemaster.
- Decision: Local-only private game. Family vs. gamemaster. 12 questions to victory. A background image for each question, sourced primarily from Wikimedia. A reusable pool with burned tracking. The question pool is built first.
- Consequences: No hosting, accounts, or publishing concerns. Content tooling comes first.

## D-3: Local server for persistence
- Date: 2026-10-05
- Context: Burned state and session data must survive restarts. Browser localStorage is fragile and tied to one browser profile.
- Decision: The game runs with a tiny local server that serves the app and persists state. Storage is proposed as SQLite for state only (burned, session log, current game); question content stays in text files keyed by stable IDs. Pending confirmation of the storage split.
- Consequences: A server process is part of `run`. The server language is still open (OQ-14).
- Supersedes / related: ARC-1, QP-2, QP-8, B-1

## D-4: Storage split and server language
- Date: 2026-10-06
- Context: D-3 proposed SQLite for state, pending confirmation. OQ-14 asked for a stack preference.
- Decision: Confirmed: game state (burned, session log, current game) lives in SQLite. Questions live in a JSON file (one object per question), keyed by stable IDs. The server is written in Python.
- Consequences: The server can use only the standard library (`http.server`, `sqlite3`, `json`). The question file stays hand-editable and diffable. The client technology is still open.
- Supersedes / related: confirms D-3; OQ-14 (partially); ARC-1, QP-2

## D-5: Client stack
- Date: 2026-10-06
- Context: Plain JS was rejected because the client is expected to grow. OQ-14 left the client open.
- Decision: Svelte 5 + Vite + TypeScript. `vite build` produces static files that the Python server serves. Node is needed only for development and building, never at game time.
- Consequences: A `package.json` and a build step are part of the project. TypeScript types for the question schema can be shared across the client and validated against the JSON.
- Supersedes / related: OQ-14 (resolved together with D-4); ARC-1

## D-6: Audience, language and difficulty scale
- Date: 2026-10-06
- Context: OQ-6, OQ-7 and OQ-9 were open. The gamemaster described the players.
- Decision: The players are two Colombian kids, aged 11 and 12. All content is in Spanish, Colombian usage ("bombillo", "gripa", "crispetas"), with Colombian references where natural. Difficulty is a 1–10 scale: 1 = a 6-year-old can answer it, 10 = a 16-year-old can answer it. The first pool targets ~120 questions (10 games of 12).
- Consequences: Distractors and hints must suit kids. The pool is spread evenly over the 10 levels (12 per level) until OQ-3 decides the ladder curve.
- Supersedes / related: OQ-6, OQ-7, OQ-9; QP-1, QP-3

## D-7: Question format
- Date: 2026-10-06
- Context: OQ-5 asked about formats. The gamemaster specified the shape of every question.
- Decision: Every question is multiple choice: one correct answer plus exactly three wrong answers (the client shuffles them). Every question has exactly three hints, ordered from vague to strong. Every question has one media item: mostly a decorative image, sometimes audio or video. Media with role `essential` is part of the question ("Escucha: ¿qué instrumento suena?"); `decorative` media must not give the answer away. Questions are AI-drafted and start with `status: "draft"` until the gamemaster approves them.
- Consequences: Schema in `02-question-pool.md`. Image sourcing (`06-images.md`) widens to audio and video. How hints are used in play is open (OQ-15).
- Supersedes / related: OQ-5, OQ-10; QP-1, QG-1, QG-2

## D-8: Question description
- Date: 2026-10-06
- Context: The gamemaster wants each question introduced in the style of "You Don't Know Jack" 1 and 2.
- Decision: Every question has a `description`: one full, humorous Spanish sentence that relates to the question's content. It doesn't have to make perfect sense, and it must not give the answer away outright. The TV shows it before the question, instead of the category. `category` stays in the data for balancing and reports. The first 120 questions are approved by the gamemaster.
- Consequences: Schema in `02-question-pool.md` gains `description`. The question screen (04) shows the description, not the category.
- Supersedes / related: D-7; QP-1, QP-5, UI-2

## D-9: Correction to D-8 — first batch not yet approved
- Date: 2026-10-06
- Context: D-8 recorded the first 120 questions as approved. The gamemaster is keeping them but has not reviewed them yet.
- Decision: All 120 questions stay `status: "draft"` until the gamemaster reviews them (QP-10).
- Consequences: None beyond the status field.
- Supersedes / related: D-8 (approval part only); QP-5, QP-10

## D-10: Question pipeline runs on `claude -p`
- Date: 2026-10-06
- Context: Large batches need code (07, "Strategy for large batches"). The gamemaster chose Claude Code's non-interactive mode over the Claude API.
- Decision: The question pipeline is a Python script (standard library only) in `tools/`. Its writing steps (fit table, drafting, rating, fact-check) call `claude -p` with a prompt file from `tools/prompts/` and `--json-schema` for structured output. Each call is a fresh session, so the rating pass never grades its own writing. The mechanical steps (dedupe, merge, validate, report) are plain code. Intermediate results live in `work/<run>/` so a run can resume.
- Consequences: No API key; usage counts against the gamemaster's Claude subscription, and long runs may hit usage limits. The schema gains `subcategory`, `style`, `quality`, `fact_checked`, `needs_media` (QG-7). Generation needs internet; game night does not.
- Supersedes / related: QG-4, QG-5, QG-7, QP-7

## D-11: Review decisions
- Date: 2026-10-06
- Context: OQ-18 and OQ-19 asked how the review tool's three actions relate. The gamemaster clarified that reject is for unsalvageable questions.
- Decision: Approve = good as it is. Reject = unsalvageable, never reworked, no reason asked. Feedback = salvageable but needs changes; it is its own decision and sets `status: "needs_work"` for a later rework step.
- Consequences: Rejected questions are final. Only `needs_work` questions enter `qgen.py rework`. Feedback text is the main signal for tuning prompts before scaling up.
- Supersedes / related: OQ-18, OQ-19; RV-1, QG-11

## D-12: Dev environment via `shell.nix`
- Date: 2026-10-06
- Context: The gamemaster's machine runs NixOS, without a global Node install. The Svelte client (D-5) needs Node to build.
- Decision: A `shell.nix` at the repo root provides Node 22 and Python 3. Client commands run inside `nix-shell`. Game night only needs Python and the built client.
- Consequences: No global installs. Contributors without Nix just need Node 22+ and Python 3.
- Supersedes / related: D-5; ARC-3, RV-2

## D-13: Media from Wikimedia Commons only, sourced before review
- Date: 2026-10-06
- Context: OQ-16 asked where audio and video come from. Songs and film clips aren't on Commons, and sourcing them by hand is too much work. The gamemaster wants to judge questions together with their media.
- Decision: All media (images, audio, video) comes from Wikimedia Commons and is cached locally. No questions that depend on songs or film clips. Videos only when Commons has a suitable one, otherwise an image. Media candidates are fetched before the gamemaster review and picked in the review tool.
- Consequences: Pipeline order changes: media comes before review (07, 06). The generator must not produce song or film-clip questions. q-0072 switches to an image; q-0067 depends on finding a Commons vallenato recording.
- Supersedes / related: OQ-16; IMG-1..IMG-8, QG-12, RV-*

## D-14: Background image for audio questions
- Date: 2026-10-06
- Context: In the pilot review, audio questions ("Escucha: ¿qué ave hace este sonido?") have a sound as their media, so the TV has no picture. A picture of the answer would give it away.
- Decision: Questions whose `media.type` is "audio" get a second media slot, `background`: a generic decorative image (e.g. a forest for a bird call) that doesn't reveal the answer. It uses the same fields as image media: `query`, `source_url`, `local_path`, `credit`. Other questions have `background: null`. Videos fill the screen themselves and need no background.
- Consequences: Generator writes a `background_query` for audio questions. `media.py` fetches candidates for both slots. The review tool shows both, and approving picks both suggestions.
- Supersedes / related: D-7, D-13; IMG-9, IMG-10

## D-15: Decorative images shown blurred with a question mark
- Date: 2026-10-06
- Context: In the pilot review, a decorative image (paper lanterns for a question about the uchuva) looked like a hint and confused the gamemaster. Decorative images only set the mood and need not relate closely to the question.
- Decision: While a question is shown, decorative images (media with role `decorative`, and the background of audio questions) are covered by an overlay over the whole image: blurred, slightly darkened, with a big question mark in the centre. Essential media is shown sharp. The review tool previews decorative images the same way (hover shows them sharp; the alternatives grid stays sharp for judging).
- Consequences: The question screen (04) and the review tool share this look. Decorative images no longer need to avoid being misread as clues.
- Supersedes / related: D-7, D-14; UI-2

## D-16: Lessons from the pilot
- Date: 2026-10-06
- Context: The gamemaster reviewed all 80 pilot questions (QG-11). Results are in `07-question-generation.md`, "Pilot results".
- Decision:
  - No quality-score filter: `merge --min-score` defaults to 0. Only hard checks drop questions: `correct`, `unambiguous`, `no_giveaway` (new) below 4, a failed fact-check, duplicates.
  - The style "guess the person from three clues" is dropped.
  - Superlatives ask about the real-world record holder, never "which of these four is the biggest".
  - Essential media only for things with clear, recognisable Commons photos or sounds; never to convey something abstract (a rhythm from a photo).
  - The house style carries the gamemaster's difficulty corrections as calibration examples.
- Consequences: Prompts changed (`house-style.md`, `rate.md`), `question-styles.txt` changed, `qgen.py` hard checks extended. Scaling up is worth it (91 % usable); the target pool size is still open (OQ-17).
- Supersedes / related: QG-11; D-10

## D-17: Public repo; media is a local cache keyed by URL
- Date: 2026-10-06
- Context: The code goes to a public GitHub repo. Media files (images, audio, video) are large and come from Commons, so they shouldn't be committed. The questions must still say exactly which file to show.
- Decision: The source code and the question pool are public; the game itself still runs locally and offline. Every media slot stores `file_url`, the exact URL that was downloaded (often a Commons thumbnail URL), instead of `local_path`. Files are cached in `media/` (gitignored) under a name derived from the URL alone: `<first 16 hex chars of sha1(file_url)><extension>`. No database table: a file exists or it doesn't. On a cache miss, the server downloads the file when it is requested, for the review tool and the game alike. `tools/media.py sync` fills the cache ahead of time, so game night doesn't need internet.
- Consequences: `local_path` leaves the schema (02); `images/` goes away. Re-picking adds a new file, and `sync --prune` removes unreferenced ones. A fresh clone needs `media.py sync` (or internet) before the first game. Supersedes "private, never published" in 00-vision and AGENTS.md.
- Supersedes / related: D-13, IMG-1; IMG-11..IMG-13

## D-18: Dev environment via `flake.nix` and direnv
- Date: 2026-10-06
- Context: D-12 used `shell.nix`, which follows the machine's channel, so Node and Python versions drift between machines. The repo is going public (D-17).
- Decision: A `flake.nix` with a pinned `flake.lock` replaces `shell.nix`. Its default dev shell provides Node 22 and Python 3. `.envrc` (`use flake`) loads it automatically with direnv; `nix develop` works without direnv. Commands are documented in `README.md`.
- Consequences: `shell.nix` is gone; `nix-shell` becomes `nix develop`. Updating tools is `nix flake update`. Flakes only see git-tracked files, so new Nix files must be `git add`ed. Contributors without Nix still just need Node 22+ and Python 3.
- Supersedes / related: D-12

## D-19: Two-level categories in `data/categories.json`
- Date: 2026-10-06
- Context: There were two category lists: 10 main categories in `data/questions.json` (every question had one) and ~140 subcategories in `categories.txt` (only generated questions had one; `fit` asked Claude for the main category). The gamemaster wants one list, and statistics per broad category.
- Decision: `data/categories.json` is the only category list: 24 broad categories (`slug`, `name`), each with its subcategories, in display order. Every question stores only `subcategory`; its broad category is looked up from the file. The `categories` map in `questions.json`, the `category` field on questions and `categories.txt` are removed. `fit` no longer maps subcategories; it only scores styles.
- Consequences: The old 10 categories (and "12 per category" balancing of the first 120) are gone. New subcategories are added to the file under a broad category before `fit` can use them. `qgen.py validate` checks every subcategory against the file. Stats (per broad category, per difficulty) are a page of the web client.
- Supersedes / related: OQ-8, QP-4, QP-11, QP-12; QG-7

## D-20: Core rules — 12 in a row, choose by description, wrong ends the game
- Date: 2026-10-06
- Context: OQ-1..OQ-3 were open. The gamemaster described the game as it should play on the TV.
- Decision: The game has 12 levels, from easiest (1) to hardest (12), and all 12 must be answered in a row. Before each level, the players choose one of 4 questions by their `description`. A wrong final answer ends the game. Only the question actually asked is burned.
- Consequences: Each level needs 4 candidates at a matching difficulty (GF-2), so the pool must hold more than 12 questions per difficulty band over several games. No lives or score. The undo in the admin overlay is the safety net for misclicks.
- Supersedes / related: OQ-1, OQ-2, OQ-3; GF-1, GF-2, UI-*

## D-21: Screen states, transitions and sound
- Date: 2026-10-06
- Context: The gamemaster wants a suspenseful show: music, a sound on every transition, a growing stack as progress, a lock-in mechanic and fireworks.
- Decision: The screens are Start, Level (the stack), Select (4 cards), Question, Correct, Wrong and Victory, with an admin overlay on `Esc` over every screen. Every state change uses one transition routine: music fades out, a sound effect plays, the screen fades to black, then fades back in, and the music returns. Suspenseful music loops at low volume and is off while question media plays. Locking in an answer moves a big padlock away to reveal «Respuesta final». A correct answer gets a fanfare and one of several canvas fireworks overlays. A wrong answer gets a sad sound, a dark animation, a consolation message and «Volver al inicio». Sound is required, not optional. Audio uses the Web Audio API and fireworks use a plain canvas, with no new dependencies.
- Consequences: The first click on Start unlocks audio and autoplay. Sound assets ship with the client (OQ-20). UI-5 is replaced by UI-7..UI-14.
- Supersedes / related: D-8, D-15; GF-3, UI-*, GM-2

## D-22: UI details — unlocking, three music intensities, difficulty ranges, the tower
- Date: 2026-10-06
- Context: The gamemaster answered OQ-20..OQ-24 from the first UI plan (D-21) and added the music intensities.
- Decision:
  - All audio that is part of the UI (music, effects) is committed to the repo, with `CREDITS.md`. Question media stays a gitignored cache (D-17).
  - A locked-in answer can be unlocked before the final answer. This plays the lock-in animation in reverse (the padlock goes back in front of «Respuesta final»), and afterwards no answer is locked in.
  - After a wrong final answer, the correct answer is revealed.
  - Question difficulty (1–10) is a rating, not a level. Each of the 12 levels draws from a difficulty range: 1 · 2–3 · 3–5 · 4–6 · 4–6 · 4–6 · 5–7 · 6–8 · 6–9 · 7–10 · 8–10 · 9–10.
  - Every level offers exactly 4 questions; there is no fallback to fewer.
  - Progress is a tower of blocks that gets narrower towards the top.
  - Three music loops: `normal` (Start, Level, Select), `question` (more intense, Question screen) and `submitted` (most intense, from the final answer until the reveal). The wait before the reveal grows with the level (3 s at level 1 to 12 s at level 12, to be tuned), and at the reveal, the music turns straight into the fanfare/jingle or the sad sting.
- Consequences: The drum-roll is replaced by the `submitted` track and the level-dependent wait. A new game needs a supply check that all 12 levels can offer 4 questions (GF-5). The pool needs 48 unburned questions per game, spread over the ranges (OQ-17).
- Supersedes / related: D-20, D-21; OQ-20..OQ-24; GF-2, GF-5, UI-3, UI-8, UI-12

## D-23: Prompt changes after the first-120 review
- Date: 2026-10-06
- Context: The gamemaster reviewed the revised first 120 (QG-13): 117 approved, 3 rejected, both proposed drops overruled, 10 difficulty corrections (07, "First-120 review results").
- Decision:
  - The tone rule no longer bans famous historical events or films that involve deaths (Titanic, the end of WWII). Only questions *about* deaths, suffering or gore are out.
  - A question's clue must identify the answer in the real world, not just among the four options ("baila con velas" → cumbia and "raqueta y pelotica amarilla" → tennis fail). The rater scores this under `unambiguous`.
  - Seven new difficulty calibration examples, including two where the revise step lowered the level too far.
- Consequences: `house-style.md`, `rate.md` and `revise.md` changed. Decorative image quality is handled separately (B-4).
- Supersedes / related: D-16; QG-13, QG-14

## D-24: Illustrative images
- Date: 2026-10-06
- Context: After the first-120 review, the gamemaster noted that decorative images don't matter (any mood picture passed), but a picture that actually relates to the question would be better, as long as it doesn't give the answer away.
- Decision: A new media role `illustrative`: the image shows something that belongs to the question (its subject, a place or object it mentions, the setting) without showing the answer or ruling options in or out. Unlike decorative images (D-15), illustrative images are shown sharp, without the question-mark overlay. Decorative stays for questions where any related image would give the answer away. The house style prefers illustrative over decorative where it is safe.
- Consequences: `role` gains `illustrative` in schema, `qgen.py`, `media.py` (same size filter as decorative) and the review tool. The approved first-120 questions get illustrative images where possible (IMG-14), picked by Claude from the thumbnails.
- Supersedes / related: D-15; IMG-14, B-4
