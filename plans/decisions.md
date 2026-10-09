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

## D-25: Playable skeleton with visible placeholders
- Date: 2026-10-06
- Context: The gamemaster wants a playable game soon, without the polish of `04-ui-tv-display.md` (sound, tower animation, fireworks, quirky cards). The missing pieces must be obvious, both on screen and in the code.
- Decision:
  - **Routes:** the game is the start page `/`; the review tool moves to `/review` (`/review?batch=pilot`); the stats pages stay at `/stats/…`.
  - **State:** game state and burned questions live in `data/game.sqlite` (D-4). The file is gitignored: it is binary and changes every game. Backing it up is still B-2.
  - **The server is the referee:** it draws the 4 options per level, shuffles the answers, checks the final answer and burns the question. The client never gets the correct answer before it submits. The server keeps one undo step (the state before the last final answer).
  - **Selection** follows GF-2 in `03-game-flow.md`: an exact matching (not a greedy pass) checks that all remaining levels can still get 4 questions each.
  - **«Saltar pregunta»** works on the Question screen: the skipped question goes back to the pool (not burned, but not offered again in this game), and the players return to Select, where a new card replaces it.
  - **Placeholders:** every unpolished part shows a dashed box or caption on screen that reads `PLACEHOLDER · <task ID>`, and the code marks it with a `PLACEHOLDER(<task ID>)` comment, so `grep -rn PLACEHOLDER client/src` lists what is left. Sounds and music aren't played yet; a caption in the corner names the sound that would play.
- Consequences: The `/?batch=…` links of the review tool become `/review?batch=…`. GF-2, GF-4, GF-5, QP-8 and UI-7 are implemented in a basic form. The polish tasks (UI-1..UI-4, UI-8..UI-14) replace placeholders one at a time.
- Supersedes / related: D-4, D-20, D-21, D-22; GF-2, GF-4, GF-5, QP-8, UI-7, UI-13

## D-26: Jokers
- Date: 2026-10-06
- Context: OQ-4 asked about jokers or lifelines. The gamemaster wants five jokers, each with UI, an animation for the action and its own transitions.
- Decision:
  - Five jokers, played on the Question screen until «Respuesta final»: **Pista** (reveal a hint), **Saltar** (skip back to Select, optionally purging the question's broad category for the rest of the game), **Más fácil** (swap for an easier question of the same broad category), **Otro tema** (swap for a question of similar difficulty from a broad category the players choose), **Francotirador** (target one answer: a wrong one is revealed as wrong; the right one means the level repeats with fresh cards, not a lost game).
  - The server is the referee for jokers too (D-25): it decides availability, carries them out and never sends the correct answer or unrevealed hints. A joker is only available if the matching (GF-2) can still fill every later level with 4 cards afterwards.
  - Hints are only shown through the Pista joker (answers the play side of OQ-15).
- Consequences: Rules, state, API, UI and animations live in the new `09-jokers.md` (JK-1..JK-10). Jokers consume spare questions, so the pool needs more than 48 unburned per game (OQ-17). The game view stops sending all hints. Uses per game and hint charges are open (OQ-25, OQ-26).
- Supersedes / related: OQ-4 (jokers part), OQ-15; D-8, D-20, D-22, D-25; GF-1, GM-2, UI-2

## D-27: Joker details
- Date: 2026-10-06
- Context: D-26 left the joker counts open (OQ-25..OQ-27), and "category" was ambiguous.
- Decision:
  - Every joker can be used **any number of times** per game and per question. Only the question and the pool limit them (shown as disabled, with a reason).
  - Each Pista reveals one hint of the current question, until all three are shown.
  - A Francotirador hit on the correct answer costs nothing beyond repeating the level.
  - "Category" in the jokers means the **subcategory** (D-19): Más fácil stays in the same subcategory, Saltar purges a subcategory, and Otro tema lets the players choose a subcategory (picked in two steps, broad category first).
  - Questions skipped or swapped away by a joker are **burned** (for the player, D-28), not returned to the pool.
- Consequences: The joker tray has no "used up" state. Jokers use up spare questions fast, so the pool and per-subcategory supply matter more (OQ-17, JK-10).
- Supersedes / related: D-26; OQ-15, OQ-25, OQ-26, OQ-27; JK-1..JK-10

## D-28: Players, and burning per player
- Date: 2026-10-06
- Context: With unlimited jokers, a game burns many more questions. The gamemaster wants every question the players have seen burned for good, but only for whoever played.
- Decision:
  - A new game starts by asking for the **player name** (pick a known one or type a new one). Players live in `data/game.sqlite`.
  - A question is **burned for the player** as soon as it was shown: answered, skipped (joker or admin), swapped away, or lost to a Snipe hit. Descriptions on cards that weren't picked don't count. Other players can still get the question.
  - The admin overlay gets «Saltar y quemar para todos»: skip the current question and burn it for every player.
  - Selection, supply check and undo work per player.
- Consequences: The `burned` table gets a player column (NULL = everyone). Replaces "skipped questions go back to the pool" in D-20 and D-25. New Player screen between Start and Level (UI-16). A new player starts with the whole pool. Tasks GF-6, QP-14.
- Supersedes / related: D-20, D-25 (skip and burn rules); D-27; GF-6, QP-14, UI-16, GM-2

## D-29: Visual design direction
- Date: 2026-10-06
- Context: The playable skeleton (D-25) uses huge type and opaque bands over the images. The gamemaster wants a real look that feels like a game.
- Decision:
  - Text on screen is **much smaller** than in the skeleton: one size unit that scales with the screen width, about 38 px for the question at 1080p instead of 65 px.
  - **Every element over the image is semi-transparent** (frosted glass panels, no full-width bands), so the picture stays visible.
  - Colour scheme: **night blue and slate gray**, with **amber** for stakes and commitment, **sky blue** for focus, **mint green** for right and **coral red** for wrong. Magenta stays reserved for placeholders.
  - A playful, opinionated game-show style ("Noche de concurso"): rounded display font, chunky arcade buttons, tilted paper cards, bouncy motion. Details are a proposal in `10-visual-design.md`, for the gamemaster to confirm (VD-1).
- Consequences: New plan `10-visual-design.md` (VD-1..VD-9) owns the look; `04-ui-tv-display.md` keeps screens and behaviour. Two font files ship with the client (OFL). The game's name is open (OQ-28).
- Supersedes / related: D-15, D-21, D-25; UI-1, UI-2, UI-3, UI-6

## D-30: Gamemaster answers: no timer, one screen, joker names, game name, setup
- Date: 2026-10-06
- Context: The open questions blocking M1–M6 (OQ-4, OQ-8, OQ-11, OQ-12, OQ-13, OQ-28, GM-2, JK-1, VD-1).
- Decision:
  - **No timer** per question (OQ-4).
  - **One screen:** no separate gamemaster device, no GM-only view (OQ-13, GM-3). The gamemaster controls the game with the keyboard and mouse of the TV machine; the admin actions live in the `Esc` overlay (GM-1).
  - **Admin actions confirmed** (GM-2): «Saltar pregunta» (burns for the player), «Saltar y quemar para todos», «Deshacer» (the last final answer), «Abandonar partida».
  - **Joker names** were left to us (JK-1): «Soplo» (hint, `S`), «Paso» (skip, `P`), «Bájale» (easier, `F`), «Cambiazo» (subcategory of choice, `T`), «Francotirador» (snipe, `X`). `A`–`D` stay reserved for the answers.
  - **No family-specific questions** (OQ-8).
  - The game is called **«¡Trivia!»** (OQ-28).
  - **Setup:** a computer connected to the TV via HDMI (OQ-11); internet is available during play (OQ-12), though the game still runs from the local media cache (D-17).
  - **Visual design:** the gamemaster confirms it from the implementation, not from a mock-up (VD-1).
- Consequences: GF-1, GM-1, GM-2, GM-3 close; GM-4 is the admin overlay (UI-13). Joker names change in 03, 04, 09, 10. VD-2..VD-8 go ahead; VD-1 is the gamemaster's review of the result.
- Supersedes / related: D-26 (joker names), D-29; OQ-4, OQ-8, OQ-11, OQ-12, OQ-13, OQ-28; GF-1, GM-1..GM-3, JK-1, VD-1

## D-31: Draft difficulties follow the level ranges
- Date: 2026-10-06
- Context: The difficulty target (15 % at 1–3, 70 % at 4–7, 15 % at 8–10) predates the level ranges of D-22. A game shows 4 questions per level, and the top three levels draw only from 7–10, 8–10 and 9–10. The pool had 10 non-rejected questions at 9–10, about two games' worth for level 12.
- Decision: `draft` assigns target difficulties in the proportions a game shows them: each level's 4 questions spread evenly over its range (07, "Difficulty target"). That is about 19 % at 1–3, 51 % at 4–7 and 30 % at 8–10.
- Consequences: `LEVEL_WEIGHTS` in `qgen.py` changes; runs drafted before this keep their difficulties. The calibration examples still apply, so high targets must be hard for these players, not obscure.
- Supersedes / related: D-22; 07 "Difficulty target"; OQ-17

## D-32: Batch-4 is reviewed by Claude, not the gamemaster
- Date: 2026-10-06
- Context: The gamemaster's review time is the bottleneck (07). The first-120 review approved 117 of 120 and every decorative pick was the first suggestion (D-23). The gamemaster asked for the next batch to be approved automatically.
- Decision: For batch-4, Claude does the gamemaster's review (step 8) and picks the media. A question is **approved** unless one of these is true; then it becomes `needs_work` with the reason as feedback:
  - The fact-check is uncertain, or the rater's notes name a defect that is still in the text (a wrong fact, a second defensible answer, a hint that points to a wrong option, a giveaway).
  - Commons has no adequate media. *Essential* media must show the thing clearly and must not name the answer (Claude looks at the candidate). *Illustrative* or *decorative* media must fit the topic and must not give the answer away. Audio questions also need a usable background picture.
  - Low soft scores (dry, weak distractors, difficulty off) are **not** a reason (D-16).
- Consequences: The review record reads `{"decision": ..., "feedback": ..., "reviewed_on": ..., "reviewer": "llm", "model": ...}` (D-33), so auto-reviews can be told apart. D-7 ("the gamemaster reviews every one") still holds for other batches. The gamemaster can still open `/review?batch=batch-4` and override.
- Supersedes / related: D-7, D-16, D-23, D-33; QG-17

## D-33: Human and LLM reviews both make a question playable
- Date: 2026-10-07
- Context: D-32 lets Claude review batch-4. The pool had no way to say who reviewed a question, and the gamemaster may still want to look at LLM-approved questions later.
- Decision: The `review` record gets `reviewer: "human" | "llm"`, plus `model` for an LLM review. `status` stays the one field that decides play: `approved` is playable whoever approved it. A human review of an LLM-reviewed question replaces it and keeps the LLM's review in `review.previous`. The review tool treats a question as open until a human has reviewed it, so LLM-reviewed questions can be checked later at any pace.
- Consequences: Existing reviews are migrated: pilot and first-120 get `reviewer: "human"`; batch-3 (116) gets `reviewer: "llm"`, `model: "claude-opus-5-5"`, because a Claude session approved it, not the gamemaster (commit 0eaa35e). Batch-4 is written as LLM reviews (D-32). `validate` checks the new fields. `GET /api/questions` filters by `reviewer` (`human`, `llm`, `none`). Selection (`tools/selection.py`) doesn't change.
- Supersedes / related: D-7 (the gamemaster no longer has to review every question before play), D-11, D-32; QP-15

## D-34: Plan a Steam release alongside the family game
- Date: 2026-10-07
- Context: The gamemaster wants the game packaged, installable and sold or given away on Steam, not only run natively on Windows. D-2 and `00-vision.md` list publishing and monetisation as non-goals.
- Decision: A Steam release is planned as its own track: master plan `11-steam.md`, sub-plans 12–18. The family game stays the priority. Changes that don't change how the family plays (the TypeScript engine, mouse support, string extraction, the joker budget with "unlimited" as the default, the license audit) can start now. Everything else waits for its open question (OQ-29..OQ-37). The current way of playing stays as the gamemaster mode.
- Consequences: D-2's "no publishing concerns" and the non-goals in `00-vision.md` no longer hold for the Steam track. New task prefixes: ST, PORT, MD, IN, I18N, LUI, QT, RG, CT, PUB, SW. The shell, the default mode and the content target are not decided yet.
- Supersedes / related: D-2 (scope, in part); D-3, D-4, D-25 (revisited by `12-client-engine.md`); OQ-29..OQ-37

## D-35: The repo separates what ships from the tooling; the flake packages both
- Date: 2026-10-07
- Context: Game, review tool, pipeline and data lived side by side: `server/main.py` served the game and the authoring API, the game imported `tools/`, the client mixed game and review pages, and the game read the source pool with its review notes. The Steam track (D-34) needs a clean shipped part, and the gamemaster wants the pipeline's tools (including Claude and ImageMagick) packaged.
- Decision: Two top-level trees. `app/` is what ships: game server, game client, `categories.json` and `pool.json` (an export of approved questions with play fields only). `authoring/` never ships: pipeline, prompts, review/stats/print pages and their server, the source pool. `authoring/` may import from `app/`, never the reverse. The flake provides `packages.app`, `packages.authoring` (with `claude-code`, the one allowed unfree package, and ImageMagick) and a dev shell with everything. Game state and the media cache are gitignored at `state/` and `media/`.
- Consequences: Paths change everywhere (`19-repo-layout.md`). The game runs on port 8000, the authoring server on 8001. `qgen.py export` (PORT-6, pulled forward) must run after pool changes; `validate` fails when the export is stale. Supersedes the file layout in `01-architecture.md`.
- Supersedes / related: D-3, D-4, D-5, D-17, D-18, D-25 (layout only); D-34; PORT-6

## D-36: An LLM makes a batch with one command, `qgen batch`
- Date: 2026-10-07
- Context: Batch-4's Claude review (D-32) worked, but it was done by hand in an interactive session: choosing subcategories, running steps, building contact sheets, judging images and writing review records were all improvised. The gamemaster wants the process unambiguous, with no room for variation by the LLM.
- Decision: `qgen batch` runs the whole pipeline in a fixed order with fixed rules (run name, subcategory choice, all steps, review, media pick, export, validate, sync, report). The review is a pipeline step: one `claude -p` call per question with `prompts/review.md` and the contact sheet of its media candidates, answering by JSON schema. An LLM operating the pipeline follows `authoring/RUNBOOK.md` only: run `qgen batch`, rerun it after a usage limit, commit the listed paths. It doesn't edit the pool, pick media or change prompts by hand.
- Consequences: The interactive procedure of batch-4 is retired. Prompt changes are code changes reviewed by the gamemaster. D-32's criteria live in `prompts/review.md`.
- Supersedes / related: D-10, D-16, D-32, D-33; QG-17

## D-37: New questions start from stored concept lists and multi-axis styles
- Date: 2026-10-07
- Context: Drafts fell back to the most famous facts of each subcategory (all of `Espacio` reads like a textbook), styles bunched up (three of ~30 made up half the pool), and `fun` was the weakest rater score. The content came entirely from Claude in one pass, steered only by an avoid list. An LLM has no reliable sense of what is surprising: asked for a surprising fact about Saturn, it says Saturn would float.
- Decision: Variety comes from code and from the growing pool (`20-pipeline-efficiency.md`, part 2). Each subcategory gets a stored list of about 150–250 concepts in facets, with top-ups (OQ-38), and a stored 1–5 fit for the question axes. The style list becomes five axes (move, stimulus, clue form, answer kind, lens) with compatibility rules in `authoring/data/question-axes.json`, as drafted in plan 20 (OQ-39). `draft` draws concepts (fewer questions first) and axis combinations (rarely used first) by code; every question already asked about a concept is shown to the next draft about it. Concepts are reused, so the obvious facts get used up and later questions have to go further. No prompt asks for "surprising" angles. Concept names are unique across subcategories by normalized name only; synonyms are accepted (OQ-40). Existing questions get a concept and axes too (OQ-39).
- Consequences: `fit` and `question-styles.txt` are retired; old questions keep `style` as history. New fields `concept` and `axes` on questions (authoring only, not exported). `qgen concepts` makes the lists; `qgen batch` creates or tops up the lists it needs. About 2 calls per subcategory once.
- Supersedes / related: D-10, D-16, D-36; OQ-38, OQ-39, OQ-40; PE-7..PE-13

## D-38: Four age groups on one shared difficulty scale; the pipeline writes for a focus group
- Date: 2026-10-07
- Context: The project was built for one audience, two Colombian kids aged 11 and 12 (D-6), and the house style, prompts and concept lists said so. The gamemaster wants four age groups in the game, with young teens as the current focus.
- Decision: Four age groups in `app/data/age-groups.json`: kids (6–10), young teens (11–14), young adults (15–22), adults (23+). Difficulty stays one number per question on one shared scale, extended from 1–10 to 1–15 (1 = a 6-year-old can answer it, 10 = a 16-year-old, 15 = trivia specialists); each group plays a window of it. The focus group (`young_teens`, window 1–10) is set in the same file; the pipeline writes for it, and no prompt names a fixed age. Concepts carry `known_at` (1–15) instead of `familiarity` for 11–12-year-olds. Content stays family-friendly in every group.
- Consequences: The existing pool keeps its difficulties (the old scale is the shared scale's 1–10). The game is unchanged until AG-7 adds the choice of group. The other groups' windows are a draft. `21-age-groups.md` has the tasks.
- Supersedes / related: D-6 (audience and scale; Spanish and Colombian usage stay), D-31, D-37; OQ-36

## D-39: Bundles: every question is in exactly one, switched on or off before a session
- Date: 2026-10-07
- Context: Plan 15c planned a `region` field so that Colombian questions become an opt-in pack. The gamemaster wants the general idea: packs of questions (regional like Colombia, thematic like sports) that players switch on or off before a session, with a base pack that is always on.
- Decision: Bundles are listed in `app/data/bundles.json` (`base`, `colombia` for now). Every question has exactly one `bundle`, default `base`. Bundles add questions and don't own a topic: a sports question can be in `base`, and well-known facts about Colombia stay in `base`; only questions that need a real connection to Colombia go into `colombia`. `base` is always on. Membership is decided by each bundle's rule: the drafter picks it for new questions, an LLM pass proposes it for the existing pool, the gamemaster corrects it in the review tool.
- Consequences: `bundle` is a play field (exported). The game plays every bundle until BN-6 adds the choice. 15c's `region` field (RG-1, RG-2) is replaced by bundles. `22-bundles.md` has the tasks.
- Supersedes / related: 15c (region model); D-28, D-36, D-38

## D-40: No focus group: the pipeline can write across the whole scale
- Date: 2026-10-07
- Context: D-38 has the pipeline write only for the focus group (young teens, 1–10), so nothing aims at 11–15. The gamemaster wants questions across the whole difficulty range now, before per-group batches (AG-8).
- Decision: `"focus": null` in `app/data/age-groups.json` means no focus. `draft` then spreads target difficulties evenly over the whole scale 1–15, and the prompts say that each question is written for the groups whose window contains its difficulty. `focus` only steers the pipeline; the game plays young teens until AG-7. `qgen batch` still takes no arguments (D-36).
- Consequences: Batches made without a focus add questions at 11–15 that the game doesn't play yet. Even targets are temporary; `21-age-groups.md` proposes a demand-based distribution for AG-7/AG-8.
- Supersedes / related: D-31, D-36, D-38; AG-8, AG-10

## D-41: A batch writes for one bundle, named by the command; bundles have their own taxonomy
- Date: 2026-10-07
- Context: Under D-39 the drafter picks each question's bundle, so a batch over the subcategories with the fewest approved questions mixes `base` and `colombia` questions without anyone asking for `colombia` (batch-6: 13 of its 30 subcategories are Colombian). The gamemaster wants bundles to be deliberate.
- Decision: `qgen batch` writes `base` questions by default; questions for another bundle are made only with the bundle named on the command (`qgen batch --bundle <id>`). A separate command creates an empty bundle, which is set up with its own categories, subcategories and concept lists, and possibly its own question axes, independent of `base`'s.
- Consequences: The drafter no longer picks a bundle (BN-4 is undone by BN-8). The RUNBOOK's "no arguments" (D-36) gets one exception, `--bundle`, used only when the user names a bundle. `22-bundles.md` has the design and tasks BN-8..BN-12; open points OQ-41..OQ-44. Not implemented yet: batch-6 still follows D-39.
- Supersedes / related: D-39 (who picks the bundle), D-36, D-37, D-19

## D-42: The start page offers LLM approvals for human review; open work comes first
- Date: 2026-10-09
- Context: 293 approved questions have only an LLM review (D-33). The authoring start page (08, RV-12..RV-17) has to say whether they are the gamemaster's work (OQ-45).
- Decision: They are an option, not a to-do. The start page links to a queue of questions only an LLM has approved, for all batches and per batch, below the queues that need the gamemaster: `needs_work`, unreviewed drafts, missing media and unchecked bundle proposals.
- Consequences: The review screen gets a `reviewer` filter (RV-13). A human review of an LLM-approved question works as today: it replaces the LLM review and keeps it in `review.previous` (D-33).
- Supersedes / related: D-33, OQ-45
