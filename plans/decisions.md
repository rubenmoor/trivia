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
- Context: Initial brief from the developer.
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
- Context: OQ-6, OQ-7 and OQ-9 were open. The developer described the players.
- Decision: The players are two Colombian kids, aged 11 and 12. All content is in Spanish, Colombian usage ("bombillo", "gripa", "crispetas"), with Colombian references where natural. Difficulty is a 1–10 scale: 1 = a 6-year-old can answer it, 10 = a 16-year-old can answer it. The first pool targets ~120 questions (10 games of 12).
- Consequences: Distractors and hints must suit kids. The pool is spread evenly over the 10 levels (12 per level) until OQ-3 decides the ladder curve.
- Supersedes / related: OQ-6, OQ-7, OQ-9; QP-1, QP-3

## D-7: Question format
- Date: 2026-10-06
- Context: OQ-5 asked about formats. The developer specified the shape of every question.
- Decision: Every question is multiple choice: one correct answer plus exactly three wrong answers (the client shuffles them). Every question has exactly three hints, ordered from vague to strong. Every question has one media item: mostly a decorative image, sometimes audio or video. Media with role `essential` is part of the question ("Escucha: ¿qué instrumento suena?"); `decorative` media must not give the answer away. Questions are AI-drafted and start with `status: "draft"` until the developer approves them.
- Consequences: Schema in `02-question-pool.md`. Image sourcing (`06-images.md`) widens to audio and video. How hints are used in play is open (OQ-15).
- Supersedes / related: OQ-5, OQ-10; QP-1, QG-1, QG-2

## D-8: Question description
- Date: 2026-10-06
- Context: The developer wants each question introduced in the style of "You Don't Know Jack" 1 and 2.
- Decision: Every question has a `description`: one full, humorous Spanish sentence that relates to the question's content. It doesn't have to make perfect sense, and it must not give the answer away outright. The TV shows it before the question, instead of the category. `category` stays in the data for balancing and reports. The first 120 questions are approved by the developer.
- Consequences: Schema in `02-question-pool.md` gains `description`. The question screen (04) shows the description, not the category.
- Supersedes / related: D-7; QP-1, QP-5, UI-2

## D-9: Correction to D-8 — first batch not yet approved
- Date: 2026-10-06
- Context: D-8 recorded the first 120 questions as approved. The developer is keeping them but has not reviewed them yet.
- Decision: All 120 questions stay `status: "draft"` until the developer reviews them (QP-10).
- Consequences: None beyond the status field.
- Supersedes / related: D-8 (approval part only); QP-5, QP-10

## D-10: Question pipeline runs on `claude -p`
- Date: 2026-10-06
- Context: Large batches need code (07, "Strategy for large batches"). The developer chose Claude Code's non-interactive mode over the Claude API.
- Decision: The question pipeline is a Python script (standard library only) in `tools/`. Its writing steps (fit table, drafting, rating, fact-check) call `claude -p` with a prompt file from `tools/prompts/` and `--json-schema` for structured output. Each call is a fresh session, so the rating pass never grades its own writing. The mechanical steps (dedupe, merge, validate, report) are plain code. Intermediate results live in `work/<run>/` so a run can resume.
- Consequences: No API key; usage counts against the developer's Claude subscription, and long runs may hit usage limits. The schema gains `subcategory`, `style`, `quality`, `fact_checked`, `needs_media` (QG-7). Generation needs internet; game night does not.
- Supersedes / related: QG-4, QG-5, QG-7, QP-7

## D-11: Review decisions
- Date: 2026-10-06
- Context: OQ-18 and OQ-19 asked how the review tool's three actions relate. The developer clarified that reject is for unsalvageable questions.
- Decision: Approve = good as it is. Reject = unsalvageable, never reworked, no reason asked. Feedback = salvageable but needs changes; it is its own decision and sets `status: "needs_work"` for a later rework step.
- Consequences: Rejected questions are final. Only `needs_work` questions enter `qgen.py rework`. Feedback text is the main signal for tuning prompts before scaling up.
- Supersedes / related: OQ-18, OQ-19; RV-1, QG-11

## D-12: Dev environment via `shell.nix`
- Date: 2026-10-06
- Context: The developer's machine runs NixOS, without a global Node install. The Svelte client (D-5) needs Node to build.
- Decision: A `shell.nix` at the repo root provides Node 22 and Python 3. Client commands run inside `nix-shell`. Game night only needs Python and the built client.
- Consequences: No global installs. Contributors without Nix just need Node 22+ and Python 3.
- Supersedes / related: D-5; ARC-3, RV-2

## D-13: Media from Wikimedia Commons only, sourced before review
- Date: 2026-10-06
- Context: OQ-16 asked where audio and video come from. Songs and film clips aren't on Commons, and sourcing them by hand is too much work. The developer wants to judge questions together with their media.
- Decision: All media (images, audio, video) comes from Wikimedia Commons and is cached locally. No questions that depend on songs or film clips. Videos only when Commons has a suitable one, otherwise an image. Media candidates are fetched before the developer review and picked in the review tool.
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
- Context: In the pilot review, a decorative image (paper lanterns for a question about the uchuva) looked like a hint and confused the developer. Decorative images only set the mood and need not relate closely to the question.
- Decision: While a question is shown, decorative images (media with role `decorative`, and the background of audio questions) are covered by an overlay over the whole image: blurred, slightly darkened, with a big question mark in the centre. Essential media is shown sharp. The review tool previews decorative images the same way (hover shows them sharp; the alternatives grid stays sharp for judging).
- Consequences: The question screen (04) and the review tool share this look. Decorative images no longer need to avoid being misread as clues.
- Supersedes / related: D-7, D-14; UI-2

## D-16: Lessons from the pilot
- Date: 2026-10-06
- Context: The developer reviewed all 80 pilot questions (QG-11). Results are in `07-question-generation.md`, "Pilot results".
- Decision:
  - No quality-score filter: `merge --min-score` defaults to 0. Only hard checks drop questions: `correct`, `unambiguous`, `no_giveaway` (new) below 4, a failed fact-check, duplicates.
  - The style "guess the person from three clues" is dropped.
  - Superlatives ask about the real-world record holder, never "which of these four is the biggest".
  - Essential media only for things with clear, recognisable Commons photos or sounds; never to convey something abstract (a rhythm from a photo).
  - The house style carries the developer's difficulty corrections as calibration examples.
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
- Context: There were two category lists: 10 main categories in `data/questions.json` (every question had one) and ~140 subcategories in `categories.txt` (only generated questions had one; `fit` asked Claude for the main category). The developer wants one list, and statistics per broad category.
- Decision: `data/categories.json` is the only category list: 24 broad categories (`slug`, `name`), each with its subcategories, in display order. Every question stores only `subcategory`; its broad category is looked up from the file. The `categories` map in `questions.json`, the `category` field on questions and `categories.txt` are removed. `fit` no longer maps subcategories; it only scores styles.
- Consequences: The old 10 categories (and "12 per category" balancing of the first 120) are gone. New subcategories are added to the file under a broad category before `fit` can use them. `qgen.py validate` checks every subcategory against the file. Stats (per broad category, per difficulty) are a page of the web client.
- Supersedes / related: OQ-8, QP-4, QP-11, QP-12; QG-7

## D-20: Core rules — 12 in a row, choose by description, wrong ends the game
- Date: 2026-10-06
- Context: OQ-1..OQ-3 were open. The developer described the game as it should play on the TV.
- Decision: The game has 12 levels, from easiest (1) to hardest (12), and all 12 must be answered in a row. Before each level, the players choose one of 4 questions by their `description`. A wrong final answer ends the game. Only the question actually asked is burned.
- Consequences: Each level needs 4 candidates at a matching difficulty (GF-2), so the pool must hold more than 12 questions per difficulty band over several games. No lives or score. The undo in the admin overlay is the safety net for misclicks.
- Supersedes / related: OQ-1, OQ-2, OQ-3; GF-1, GF-2, UI-*

## D-21: Screen states, transitions and sound
- Date: 2026-10-06
- Context: The developer wants a suspenseful show: music, a sound on every transition, a growing stack as progress, a lock-in mechanic and fireworks.
- Decision: The screens are Start, Level (the stack), Select (4 cards), Question, Correct, Wrong and Victory, with an admin overlay on `Esc` over every screen. Every state change uses one transition routine: music fades out, a sound effect plays, the screen fades to black, then fades back in, and the music returns. Suspenseful music loops at low volume and is off while question media plays. Locking in an answer moves a big padlock away to reveal «Respuesta final». A correct answer gets a fanfare and one of several canvas fireworks overlays. A wrong answer gets a sad sound, a dark animation, a consolation message and «Volver al inicio». Sound is required, not optional. Audio uses the Web Audio API and fireworks use a plain canvas, with no new dependencies.
- Consequences: The first click on Start unlocks audio and autoplay. Sound assets ship with the client (OQ-20). UI-5 is replaced by UI-7..UI-14.
- Supersedes / related: D-8, D-15; GF-3, UI-*, GM-2

## D-22: UI details — unlocking, three music intensities, difficulty ranges, the tower
- Date: 2026-10-06
- Context: The developer answered OQ-20..OQ-24 from the first UI plan (D-21) and added the music intensities.
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
- Context: The developer reviewed the revised first 120 (QG-13): 117 approved, 3 rejected, both proposed drops overruled, 10 difficulty corrections (07, "First-120 review results").
- Decision:
  - The tone rule no longer bans famous historical events or films that involve deaths (Titanic, the end of WWII). Only questions *about* deaths, suffering or gore are out.
  - A question's clue must identify the answer in the real world, not just among the four options ("baila con velas" → cumbia and "raqueta y pelotica amarilla" → tennis fail). The rater scores this under `unambiguous`.
  - Seven new difficulty calibration examples, including two where the revise step lowered the level too far.
- Consequences: `house-style.md`, `rate.md` and `revise.md` changed. Decorative image quality is handled separately (B-4).
- Supersedes / related: D-16; QG-13, QG-14

## D-24: Illustrative images
- Date: 2026-10-06
- Context: After the first-120 review, the developer noted that decorative images don't matter (any mood picture passed), but a picture that actually relates to the question would be better, as long as it doesn't give the answer away.
- Decision: A new media role `illustrative`: the image shows something that belongs to the question (its subject, a place or object it mentions, the setting) without showing the answer or ruling options in or out. Unlike decorative images (D-15), illustrative images are shown sharp, without the question-mark overlay. Decorative stays for questions where any related image would give the answer away. The house style prefers illustrative over decorative where it is safe.
- Consequences: `role` gains `illustrative` in schema, `qgen.py`, `media.py` (same size filter as decorative) and the review tool. The approved first-120 questions get illustrative images where possible (IMG-14), picked by Claude from the thumbnails.
- Supersedes / related: D-15; IMG-14, B-4

## D-25: Playable skeleton with visible placeholders
- Date: 2026-10-06
- Context: The developer wants a playable game soon, without the polish of `04-ui-tv-display.md` (sound, tower animation, fireworks, quirky cards). The missing pieces must be obvious, both on screen and in the code.
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
- Context: OQ-4 asked about jokers or lifelines. The developer wants five jokers, each with UI, an animation for the action and its own transitions.
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
  - Questions skipped or swapped away by a joker are **burned** (for the player, D-28), not returned to the pool. Now: they count as seen (D-82).
- Consequences: The joker tray has no "used up" state. Jokers use up spare questions fast, so the pool and per-subcategory supply matter more (OQ-17, JK-10).
- Supersedes / related: D-26; OQ-15, OQ-25, OQ-26, OQ-27; JK-1..JK-10

## D-28: Players, and burning per player
- **Superseded in part by D-82** (the burn rules → seen counters; player names stay).
- Date: 2026-10-06
- Context: With unlimited jokers, a game burns many more questions. The developer wants every question the players have seen burned for good, but only for whoever played.
- Decision:
  - A new game starts by asking for the **player name** (pick a known one or type a new one). Players live in `data/game.sqlite`.
  - A question is **burned for the player** as soon as it was shown: answered, skipped (joker or admin), swapped away, or lost to a Snipe hit. Descriptions on cards that weren't picked don't count. Other players can still get the question.
  - The admin overlay gets «Saltar y quemar para todos»: skip the current question and burn it for every player.
  - Selection, supply check and undo work per player.
- Consequences: The `burned` table gets a player column (NULL = everyone). Replaces "skipped questions go back to the pool" in D-20 and D-25. New Player screen between Start and Level (UI-16). A new player starts with the whole pool. Tasks GF-6, QP-14.
- Supersedes / related: D-20, D-25 (skip and burn rules); D-27; GF-6, QP-14, UI-16, GM-2

## D-29: Visual design direction
- Date: 2026-10-06
- Context: The playable skeleton (D-25) uses huge type and opaque bands over the images. The developer wants a real look that feels like a game.
- Decision:
  - Text on screen is **much smaller** than in the skeleton: one size unit that scales with the screen width, about 38 px for the question at 1080p instead of 65 px.
  - **Every element over the image is semi-transparent** (frosted glass panels, no full-width bands), so the picture stays visible.
  - Colour scheme: **night blue and slate gray**, with **amber** for stakes and commitment, **sky blue** for focus, **mint green** for right and **coral red** for wrong. Magenta stays reserved for placeholders.
  - A playful, opinionated game-show style ("Noche de concurso"): rounded display font, chunky arcade buttons, tilted paper cards, bouncy motion. Details are a proposal in `10-visual-design.md`, for the developer to confirm (VD-1).
- Consequences: New plan `10-visual-design.md` (VD-1..VD-9) owns the look; `04-ui-tv-display.md` keeps screens and behaviour. Two font files ship with the client (OFL). The game's name is open (OQ-28).
- Supersedes / related: D-15, D-21, D-25; UI-1, UI-2, UI-3, UI-6

## D-30: Developer answers: no timer, one screen, joker names, game name, setup
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
  - **Visual design:** the developer confirms it from the implementation, not from a mock-up (VD-1).
- Consequences: GF-1, GM-1, GM-2, GM-3 close; GM-4 is the admin overlay (UI-13). Joker names change in 03, 04, 09, 10. VD-2..VD-8 go ahead; VD-1 is the developer's review of the result.
- Supersedes / related: D-26 (joker names), D-29; OQ-4, OQ-8, OQ-11, OQ-12, OQ-13, OQ-28; GF-1, GM-1..GM-3, JK-1, VD-1

## D-31: Draft difficulties follow the level ranges
- Date: 2026-10-06
- Context: The difficulty target (15 % at 1–3, 70 % at 4–7, 15 % at 8–10) predates the level ranges of D-22. A game shows 4 questions per level, and the top three levels draw only from 7–10, 8–10 and 9–10. The pool had 10 non-rejected questions at 9–10, about two games' worth for level 12.
- Decision: `draft` assigns target difficulties in the proportions a game shows them: each level's 4 questions spread evenly over its range (07, "Difficulty target"). That is about 19 % at 1–3, 51 % at 4–7 and 30 % at 8–10.
- Consequences: `LEVEL_WEIGHTS` in `qgen.py` changes; runs drafted before this keep their difficulties. The calibration examples still apply, so high targets must be hard for these players, not obscure.
- Supersedes / related: D-22; 07 "Difficulty target"; OQ-17

## D-32: Batch-4 is reviewed by Claude, not the developer
- Date: 2026-10-06
- Context: The developer's review time is the bottleneck (07). The first-120 review approved 117 of 120 and every decorative pick was the first suggestion (D-23). The developer asked for the next batch to be approved automatically.
- Decision: For batch-4, Claude does the developer's review (step 8) and picks the media. A question is **approved** unless one of these is true; then it becomes `needs_work` with the reason as feedback:
  - The fact-check is uncertain, or the rater's notes name a defect that is still in the text (a wrong fact, a second defensible answer, a hint that points to a wrong option, a giveaway).
  - Commons has no adequate media. *Essential* media must show the thing clearly and must not name the answer (Claude looks at the candidate). *Illustrative* or *decorative* media must fit the topic and must not give the answer away. Audio questions also need a usable background picture.
  - Low soft scores (dry, weak distractors, difficulty off) are **not** a reason (D-16).
- Consequences: The review record reads `{"decision": ..., "feedback": ..., "reviewed_on": ..., "reviewer": "llm", "model": ...}` (D-33), so auto-reviews can be told apart. D-7 ("the developer reviews every one") still holds for other batches. The developer can still open `/review?batch=batch-4` and override.
- Supersedes / related: D-7, D-16, D-23, D-33; QG-17

## D-33: Human and LLM reviews both make a question playable
- Date: 2026-10-07
- Context: D-32 lets Claude review batch-4. The pool had no way to say who reviewed a question, and the developer may still want to look at LLM-approved questions later.
- Decision: The `review` record gets `reviewer: "human" | "llm"`, plus `model` for an LLM review. `status` stays the one field that decides play: `approved` is playable whoever approved it. A human review of an LLM-reviewed question replaces it and keeps the LLM's review in `review.previous`. The review tool treats a question as open until a human has reviewed it, so LLM-reviewed questions can be checked later at any pace.
- Consequences: Existing reviews are migrated: pilot and first-120 get `reviewer: "human"`; batch-3 (116) gets `reviewer: "llm"`, `model: "claude-opus-5-5"`, because a Claude session approved it, not the developer (commit 0eaa35e). Batch-4 is written as LLM reviews (D-32). `validate` checks the new fields. `GET /api/questions` filters by `reviewer` (`human`, `llm`, `none`). Selection (`tools/selection.py`) doesn't change.
- Supersedes / related: D-7 (the developer no longer has to review every question before play), D-11, D-32; QP-15

## D-34: Plan a Steam release alongside the family game
- Date: 2026-10-07
- Context: The developer wants the game packaged, installable and sold or given away on Steam, not only run natively on Windows. D-2 and `00-vision.md` list publishing and monetisation as non-goals.
- Decision: A Steam release is planned as its own track: master plan `11-steam.md`, sub-plans 12–18. The family game stays the priority. Changes that don't change how the family plays (the TypeScript engine, mouse support, string extraction, the joker budget with "unlimited" as the default, the license audit) can start now. Everything else waits for its open question (OQ-29..OQ-37). The current way of playing stays as the gamemaster mode.
- Consequences: D-2's "no publishing concerns" and the non-goals in `00-vision.md` no longer hold for the Steam track. New task prefixes: ST, PORT, MD, IN, I18N, LUI, QT, RG, CT, PUB, SW. The shell, the default mode and the content target are not decided yet.
- Supersedes / related: D-2 (scope, in part); D-3, D-4, D-25 (revisited by `12-client-engine.md`); OQ-29..OQ-37; superseded in part by D-59 (no family mode)

## D-35: The repo separates what ships from the tooling; the flake packages both
- Date: 2026-10-07
- Context: Game, review tool, pipeline and data lived side by side: `server/main.py` served the game and the authoring API, the game imported `tools/`, the client mixed game and review pages, and the game read the source pool with its review notes. The Steam track (D-34) needs a clean shipped part, and the developer wants the pipeline's tools (including Claude and ImageMagick) packaged.
- Decision: Two top-level trees. `app/` is what ships: game server, game client, `categories.json` and `pool.json` (an export of approved questions with play fields only). `authoring/` never ships: pipeline, prompts, review/stats/print pages and their server, the source pool. `authoring/` may import from `app/`, never the reverse. The flake provides `packages.app`, `packages.authoring` (with `claude-code`, the one allowed unfree package, and ImageMagick) and a dev shell with everything. Game state and the media cache are gitignored at `state/` and `media/`.
- Consequences: Paths change everywhere (`19-repo-layout.md`). The game runs on port 8000, the authoring server on 8001. `qgen.py export` (PORT-6, pulled forward) must run after pool changes; `validate` fails when the export is stale. Supersedes the file layout in `01-architecture.md`.
- Supersedes / related: D-3, D-4, D-5, D-17, D-18, D-25 (layout only); D-34; PORT-6

## D-36: An LLM makes a batch with one command, `qgen batch`
- Date: 2026-10-07
- Context: Batch-4's Claude review (D-32) worked, but it was done by hand in an interactive session: choosing subcategories, running steps, building contact sheets, judging images and writing review records were all improvised. The developer wants the process unambiguous, with no room for variation by the LLM.
- Decision: `qgen batch` runs the whole pipeline in a fixed order with fixed rules (run name, subcategory choice, all steps, review, media pick, export, validate, sync, report). The review is a pipeline step: one `claude -p` call per question with `prompts/review.md` and the contact sheet of its media candidates, answering by JSON schema. An LLM operating the pipeline follows `authoring/RUNBOOK.md` only: run `qgen batch`, rerun it after a usage limit, commit the listed paths. It doesn't edit the pool, pick media or change prompts by hand.
- Consequences: The interactive procedure of batch-4 is retired. Prompt changes are code changes reviewed by the developer. D-32's criteria live in `prompts/review.md`.
- Supersedes / related: D-10, D-16, D-32, D-33; QG-17; amended by D-83 (`qgen neutralize`), D-87 (`qgen batch --translate`, with `--bundle` since plan 98 task 829)

## D-37: New questions start from stored concept lists and multi-axis styles
- Date: 2026-10-07
- Context: Drafts fell back to the most famous facts of each subcategory (all of `Espacio` reads like a textbook), styles bunched up (three of ~30 made up half the pool), and `fun` was the weakest rater score. The content came entirely from Claude in one pass, steered only by an avoid list. An LLM has no reliable sense of what is surprising: asked for a surprising fact about Saturn, it says Saturn would float.
- Decision: Variety comes from code and from the growing pool (`20-pipeline-efficiency.md`, part 2). Each subcategory gets a stored list of about 150–250 concepts in facets, with top-ups (OQ-38), and a stored 1–5 fit for the question axes. The style list becomes five axes (move, stimulus, clue form, answer kind, lens) with compatibility rules in `authoring/data/question-axes.json`, as drafted in plan 20 (OQ-39). `draft` draws concepts (fewer questions first) and axis combinations (rarely used first) by code; every question already asked about a concept is shown to the next draft about it. Concepts are reused, so the obvious facts get used up and later questions have to go further. No prompt asks for "surprising" angles. Concept names are unique across subcategories by normalized name only; synonyms are accepted (OQ-40). Existing questions get a concept and axes too (OQ-39).
- Consequences: `fit` and `question-styles.txt` are retired; old questions keep `style` as history. New fields `concept` and `axes` on questions (authoring only, not exported). `qgen concepts` makes the lists; `qgen batch` creates or tops up the lists it needs. About 2 calls per subcategory once.
- Supersedes / related: D-10, D-16, D-36; OQ-38, OQ-39, OQ-40; PE-7..PE-13

## D-38: Four age groups on one shared difficulty scale; the pipeline writes for a focus group
- Date: 2026-10-07
- Context: The project was built for one audience, two Colombian kids aged 11 and 12 (D-6), and the house style, prompts and concept lists said so. The developer wants four age groups in the game, with young teens as the current focus.
- Decision: Four age groups in `app/data/age-groups.json`: kids (6–10), young teens (11–14), young adults (15–22), adults (23+). Difficulty stays one number per question on one shared scale, extended from 1–10 to 1–15 (1 = a 6-year-old can answer it, 10 = a 16-year-old, 15 = trivia specialists); each group plays a window of it. The focus group (`young_teens`, window 1–10) is set in the same file; the pipeline writes for it, and no prompt names a fixed age. Concepts carry `known_at` (1–15) instead of `familiarity` for 11–12-year-olds. Content stays family-friendly in every group.
- Consequences: The existing pool keeps its difficulties (the old scale is the shared scale's 1–10). The game is unchanged until AG-7 adds the choice of group. The other groups' windows are a draft. `21-age-groups.md` has the tasks.
- Supersedes / related: D-6 (audience and scale; Spanish and Colombian usage stay), D-31, D-37; OQ-36

## D-39: Bundles: every question is in exactly one, switched on or off before a session
- Date: 2026-10-07
- Context: Plan 15c planned a `region` field so that Colombian questions become an opt-in pack. The developer wants the general idea: packs of questions (regional like Colombia, thematic like sports) that players switch on or off before a session, with a base pack that is always on.
- Decision: Bundles are listed in `app/data/bundles.json` (`base`, `colombia` for now). Every question has exactly one `bundle`, default `base`. Bundles add questions and don't own a topic: a sports question can be in `base`, and well-known facts about Colombia stay in `base`; only questions that need a real connection to Colombia go into `colombia`. `base` is always on. Membership is decided by each bundle's rule: the drafter picks it for new questions, an LLM pass proposes it for the existing pool, the developer corrects it in the review tool.
- Consequences: `bundle` is a play field (exported). The game plays every bundle until BN-6 adds the choice. 15c's `region` field (RG-1, RG-2) is replaced by bundles. `22-bundles.md` has the tasks.
- Supersedes / related: 15c (region model); D-28, D-36, D-38

## D-40: No focus group: the pipeline can write across the whole scale
- Date: 2026-10-07
- Context: D-38 has the pipeline write only for the focus group (young teens, 1–10), so nothing aims at 11–15. The developer wants questions across the whole difficulty range now, before per-group batches (AG-8).
- Decision: `"focus": null` in `app/data/age-groups.json` means no focus. `draft` then spreads target difficulties evenly over the whole scale 1–15, and the prompts say that each question is written for the groups whose window contains its difficulty. `focus` only steers the pipeline; the game plays young teens until AG-7. `qgen batch` still takes no arguments (D-36).
- Consequences: Batches made without a focus add questions at 11–15 that the game doesn't play yet. Even targets are temporary; `21-age-groups.md` proposes a demand-based distribution for AG-7/AG-8.
- Supersedes / related: D-31, D-36, D-38; AG-8, AG-10

## D-41: A batch writes for one bundle, named by the command; bundles have their own taxonomy
- Date: 2026-10-07
- Context: Under D-39 the drafter picks each question's bundle, so a batch over the subcategories with the fewest approved questions mixes `base` and `colombia` questions without anyone asking for `colombia` (batch-6: 13 of its 30 subcategories are Colombian). The developer wants bundles to be deliberate.
- Decision: `qgen batch` writes `base` questions by default; questions for another bundle are made only with the bundle named on the command (`qgen batch --bundle <id>`). A separate command creates an empty bundle, which is set up with its own categories, subcategories and concept lists, and possibly its own question axes, independent of `base`'s.
- Consequences: The drafter no longer picks a bundle (BN-4 is undone by BN-8). The RUNBOOK's "no arguments" (D-36) gets one exception, `--bundle`, used only when the user names a bundle. `22-bundles.md` has the design and tasks BN-8..BN-12; open points OQ-41..OQ-44. Not implemented yet: batch-6 still follows D-39.
- Supersedes / related: D-39 (who picks the bundle), D-36, D-37, D-19

## D-42: The start page offers LLM approvals for human review; open work comes first
- Date: 2026-10-09
- Context: 293 approved questions have only an LLM review (D-33). The authoring start page (08, RV-12..RV-17) has to say whether they are the developer's work (OQ-45).
- Decision: They are an option, not a to-do. The start page links to a queue of questions only an LLM has approved, for all batches and per batch, below the queues that need the developer: `needs_work`, unreviewed drafts, missing media and unchecked bundle proposals.
- Consequences: The review screen gets a `reviewer` filter (RV-13). A human review of an LLM-approved question works as today: it replaces the LLM review and keeps it in `review.previous` (D-33).
- Supersedes / related: D-33, OQ-45

## D-43: Where a bundle's taxonomy lives; Colombian subcategories leave `base`
- Date: 2026-10-08
- Context: Batch-6 wrote `base` questions with a Colombian flavour because 27 of `base`'s subcategories are about Colombia (OQ-42). D-41 gives each bundle its own taxonomy but left the layout open (OQ-41).
- Decision: `base`'s categories stay in `app/data/categories.json`. Another bundle's categories are in `app/data/bundles/<id>/categories.json`. They ship because the game's «Cambiazo» picker shows every bundle's categories while the game plays every bundle (until BN-6). Its concept lists are in `authoring/data/bundles/<id>/concepts/`, and its optional question axes in `authoring/data/bundles/<id>/question-axes.json` (otherwise `base`'s). Subcategory names and broad-category slugs are unique across all bundles, and question ids stay global. Concept names are unique within a bundle. The taxonomy steers generation; the question's `bundle` steers play. A question may keep a subcategory from another bundle's list (a well-known fact about Colombia stays in `base`). The 27 Colombian subcategories move into `colombia`'s own list (6 broad categories), and their concept lists move with them. Existing questions keep their bundle. A `base` batch keeps Colombia-only content out through the prompt alone (OQ-43); the developer moves the rest with `n` in the review tool.
- Consequences: `qgen batch` picks from `base`'s 113 subcategories; `qgen batch --bundle colombia` picks from the 27 Colombian ones. `qgen bundle new <id>` creates the entry and an empty `categories.json`. `validate` checks the uniqueness rules. The game's picker gets 6 more tiles (29 broad categories).
- Supersedes / related: D-19, D-37, D-39, D-41; OQ-41, OQ-42, OQ-43; BN-8..BN-12; amended by D-49, D-99 (names unique per bundle only; a `colombia` question uses a `colombia` subcategory), D-100 (keys: bundle + name)

## D-44: One house style for every bundle
- Date: 2026-10-08
- Context: OQ-44 asked whether a bundle with its own question axes also gets its own house style (e.g. a sports bundle allowing more statistics).
- Decision: No. Bundles are mixed in play: a session draws from every active bundle together, so all questions must read and play the same way. `prompts/house-style.md` applies to every bundle; a bundle's own axes (D-43) may change what is asked, not how it is written.
- Consequences: No per-bundle prompt files. A bundle's `rule` only decides membership.
- Supersedes / related: D-39, D-41, D-43; OQ-44

## D-45: More media providers next to Commons, with a licence allowlist
- Date: 2026-10-08
- Context: Commons' rate limits are the bottleneck of `qgen batch`, and Commons has few good wide photos for decorative images and few sounds beyond animals and instruments. D-13 allowed Commons only.
- Decision: The authoring tools also search free providers (Openverse, Pexels, Freesound, NASA; Pixabay later) in a fixed order per slot, and skip a rate-limited provider instead of waiting. A candidate is only used if its licence is on an allowlist that permits a commercial release with credit (CC0 and "No restrictions", public domain, CC BY and Commons' "Attribution", CC BY-SA, FAL, Pexels License, Pixabay Content License); NC, ND, GFDL, GPL, editorial-only and unknown licences are out, and so are providers that require hotlinking. Every picked file records its provider and licence, and is credited. D-13's other rules stand: no songs, film or TV clips, or game footage; media is found before review; the game plays from the local cache.
- Consequences: `23-media-providers.md` has the design and tasks MP-1..MP-12. Pool media gets `provider`, `license`, `license_url`, `author` (shared with PUB-2). API keys go in the gitignored `.env.local`. Paid providers come later, only for gaps.
- Supersedes / related: D-13 (Commons only), D-17, IMG-15, PUB-2

## D-46: Bigger batches: half the bundle's subcategories, 18 slots each
- Date: 2026-10-08
- Context: A batch of 30 subcategories × 4 slots gives about 80 merged questions (batch-6: 120 slots, 91 drafted, 82 merged, 66 approved). The developer wants batches of 600–800 questions, while still writing for the thinnest subcategories first so coverage evens out.
- Decision: A batch takes half of its bundle's subcategories (rounded up), the ones with the fewest approved questions in that bundle (D-41), and drafts 18 slots per subcategory (`BATCH_SHARE`, `BATCH_SLOTS` in `qgen.py`). For `base` (113 subcategories) that is 57 × 18 = 1026 slots, about 700 merged questions at batch-6's yield (0.68).
- Consequences: About 8× the per-question Claude calls of a 30-subcategory batch; a batch will usually hit the usage limit and be resumed (exit 75, RUNBOOK step 3). The draft prompt gets 18 slots in one call per subcategory. A `colombia` batch (27 subcategories → 14) gets about 250 slots, about 170 questions. Concept lists (150–250 concepts, top-up below 30 unused) cover 18 draws per batch.
- Supersedes / related: D-36, D-37, D-41; PE-10, PE-14

## D-47: Flags from the game go through the game state; the authoring server turns them into reviews
- Date: 2026-10-08
- Context: The developer wants to flag a question for review during a game night (it needs work), without leaving the game. The game must not write `authoring/data/` (D-35), and a question that leaves the pool while it is on screen breaks the running game.
- Decision: The game writes flags to `flags.json` in the game state (`TRIVIA_STATE`, default `state/`): one entry per question with the player and the date; flagging again removes the flag. `trivia-authoring` applies the flags **when it starts**: each flagged question gets a human `needs_work` review with the feedback «Marcada en el juego …» (any earlier feedback is kept in the text), and the applied flags are removed from the file. The review tool lists every question that isn't approved, across batches, at `/review?status=!approved`; the server prints that link with the count at startup.
- Consequences: A flagged question stays playable until `trivia-authoring` is (re)started, so the game never loses its question on screen. The packaged game has no authoring server; its flags stay in its state directory. When M7 moves the game state to the client, flags move with it (PORT-4's store). Decision 102: a flag records the game's question locale and the text shown (`locale`, `shown`); an en/de flag reviews that translation, not the source.
- Supersedes / related: D-30, D-33, D-35; GM-5, RV-22; decision 102

## D-48: 4K is the image target
- Date: 2026-10-08
- Context: The game is shown on a 4K TV. Images were downloaded at up to 2560 px wide, and 1920 px was the only size rule, so 129 of 428 cached images are below 4K.
- Decision: Images target 4K: 3840 px wide (or 2160 px tall for a portrait image). Larger files are downloaded as a 3840 px thumbnail; among fitting candidates the larger one wins. 1920 px stays the minimum for decorative and illustrative images, and essential images may still be smaller if nothing better exists.
- Consequences: Bigger media cache; the Steam build's re-encode resizes to 3840 px, not 2560 (18). IMG-16 changes the providers and ranking; IMG-17 brings existing picks up to 4K where their source allows it.
- Supersedes / related: D-13, D-17, D-45; IMG-3, IMG-16, IMG-17

## D-49: A `base` question uses a `base` subcategory
- Date: 2026-10-09
- Context: D-43 let a question keep a subcategory from another bundle's list, so 32 `base` questions (the capital of Colombia, coffee, Shakira, arepas, …) still sat in `colombia`'s subcategories. The developer wants `colombia`'s categories and subcategories to have no `base` questions: a broad category belongs to one bundle, and so do its questions.
- Decision: A `base` question's subcategory comes from `base`'s own list. A question that fits `base` but sits in a Colombian subcategory moves to the `base` subcategory that fits it. One that needs a connection to Colombia moves to `colombia` and keeps its subcategory. Where `base` has no fitting subcategory, `base` gets a new one: «Bebidas», «Comida latinoamericana» (Comida y bebida) and «Leyendas y supersticiones» (Mitos y leyendas). A moved question keeps its concept when the target subcategory has a concept list, and the concept is added to that list if it's missing. Without a list the concept is cleared, and the next `base` batch makes the list (D-37). `validate` fails on a `base` question in another bundle's subcategory.
- Consequences: `base` has 116 subcategories. The three new ones are the thinnest, so the next `base` batch picks them (D-46). The other direction (a `colombia` question in a `base` subcategory) is still allowed, see OQ-46.
- Supersedes / related: D-43 (the sentence "a question may keep a subcategory from another bundle's list", for `base` questions); D-19, D-37, D-39; BN-13

## D-50: Store name «Living Room Trivia», «Trivia en Familia» in Spanish
- Date: 2026-10-09
- Context: OQ-34: «¡Trivia!» is generic and hard to find on Steam. The game will get single-player modes and a competitive couch mode with timers (13), so a name built on the family co-op or the 12-in-a-row ladder (e.g. «Doce en Raya») would set the wrong expectations. The name should say: a classic quiz, best played as a group on the TV, no twist, no gimmick, a smooth game that rewards knowing things. Steamworks lets a game set a localized name per language; a customer whose Steam runs in that language sees it in the store and the library, and it follows the same limits as a name change.
- Decision: The store name is **Living Room Trivia**. Its Spanish localized name is **«Trivia en Familia»**: a literal «Trivia de Sala» splits Spanish (Latin American «sala», Spain «salón», OQ-31) and reads less naturally. The logo makes the word "Trivia" the main element, so both names look like the same game. Other languages get a localized name when they launch (15a). In-game, the title comes from the UI string catalog. The name stands only once PUB-7 (Steam search, trademark registers, domain) passes for both names; if it fails, OQ-34 reopens. Candidates considered: «Doce en Raya» / «Doce Seguidas» (only fit the co-op ladder), "Trivia Together" (doesn't fit competitive or single-player), "Trivia Night" (taken by an app and a Steam group), "Just Trivia", "Couch Trivia".
- Consequences: Set both names in Steamworks' General Application Settings before the coming-soon page, since a later change is restricted. Localized capsule art per language (PUB-8). The family game keeps showing «¡Trivia!» until the UI catalog (15a) carries the title.
- Supersedes / related: D-30 (OQ-28, «¡Trivia!»), D-34; OQ-31, OQ-34; PUB-7, PUB-8

## D-51: Sharp images keep their size and fade into the stage
- Date: 2026-10-11
- Context: Question images filled the screen with `object-fit: cover`, which crops wide and tall images and upscales small ones.
- Decision: A sharp image (illustrative, essential) is shown at its native size in device pixels, scaled down only when bigger than the screen, never upscaled, aspect ratio kept, centred. Behind it the night stage (VD-6). Its edges fade into the stage with a rounded feather. Decorative images stay blurred and full-bleed (D-15); video stays full-bleed.
- Consequences: Small images show small; D-48 (4K target) keeps them big on the TV.
- Supersedes / related: D-15, D-29 (full-bleed picture), D-48; VD-6, VD-10

## D-52: Target 5000 approved `base` questions
- Date: 2026-10-11
- Context: OQ-17. The pool has ~1000 approved `base` questions, thin at the top of the scale 1–15.
- Decision: The `base` bundle grows to 5000 approved questions. Fewer at high difficulties is fine, but each level gets a target (pm milestone 1, part 1).
- Consequences: About 8 more `base` batches (D-46). Each batch is followed by quality control; batch runs have the lowest priority (-100), after any implementation work.
- Supersedes / related: D-6 (~120 questions), D-22, D-38, D-46; OQ-17, B-6

## D-53: Pool targets live in `authoring/data/targets.json`
- Date: 2026-10-11
- Context: D-52 sets 5000 approved `base` questions with a target per difficulty (pm milestone 1, part 1). `qgen` (report, `draft`'s gap weighting) and the authoring server (`/stats/difficulty`) both need the numbers; the game doesn't.
- Decision: A new file `authoring/data/targets.json`, keyed by bundle: `{"base": {"total": 5000, "difficulty": {"1": n, …, "15": n}}}`. Authoring-only, so not in `app/data/age-groups.json` (D-35: what the game doesn't need stays in `authoring/`). Per-category targets aren't stored: they follow from the total and the bundle's subcategory count. A bundle without an entry has no targets.
- Consequences: `qgen validate` checks the file (levels match the scale, sum = total). The authoring server serves it at `/api/targets`. The difficulty numbers come from pm decision 1.
- Supersedes / related: D-35, D-38, D-40, D-52; amended by D-99 (every regional bundle: 2000), D-101 (regional entries in code)

## D-54: `draft` aims at the gaps to the pool targets
- Date: 2026-10-11
- Context: D-40 spreads target difficulties evenly over 1–15, and `qgen batch` picks subcategories by fewest approved (D-46). With targets per level (D-53) the pool still fills 5–8 fastest; hard targets land ~3 levels low (B-6; batch-7: target 15 → final 12.1).
- Decision: When the bundle has targets, `draft` weights each level by its deficit, `max(0, target − approved)`; even weights stay for bundles without targets (D-40). `qgen batch` ranks subcategories by approved questions weighted by the same deficits, so subcategories thin where the pool is thin come first. Slot targets go to subcategories whose concept lists can carry them (unused concepts with `known_at` near the target).
- Consequences: `qgen batch` still takes no arguments (D-36). Batches change shape as the pool fills. pm plan 13 (Aim batches at difficulty gaps) has the tasks.
- Supersedes / related: D-36, D-40, D-46, D-53; B-6; amended by D-84 (base past its target: the `es` source shortfall)

## D-55: Batch health thresholds stop the next batch
- Date: 2026-10-11
- Context: D-52 grows `base` by ~8 batches. Overlaps with the pool reach the review as `needs_work` (B-5), and nothing says when a batch got worse than the ones before (pm milestone 1, part 4).
- Decision: `rate` judges each draft against pool questions that share its answer or concept (`no_overlap`, a hard criterion), so overlaps are dropped before merge. Every batch report gets health metrics with thresholds stored in `authoring/data/targets.json` (`batch_health`). When the last batch fails one, `qgen batch` exits 2 before drafting until the developer acknowledges it (`qgen health ack`). Threshold numbers: a pm decision of plan 15.
- Consequences: No new `qgen batch` arguments (D-36); RUNBOOK's "other exit code: stop" covers the stop. Plan 12's exit check reads the same health data. pm plan 15 (Duplicate and drift detection) has the tasks.
- Supersedes / related: D-33, D-36, D-46, D-52, D-53; B-5, PE-6, PE-13, MP-11

## D-56: Every batch gets an LLM audit and a blind human spot check
- Date: 2026-10-11
- Context: D-52 grows `base` by ~8 batches, judged only by the LLM review (D-33). Nothing measures whether that review judges like the developer (pm milestone 1, part 5).
- Decision: `qgen batch` runs an independent LLM audit (`prompts/audit.md`, blind to the review) on a seeded sample of the batch; it never changes a status. The developer spot-checks a smaller subset of that sample in the review tool (`/review?batch=…&sample=1`), blind to the LLM verdict until deciding; the results go to `authoring/data/spot-checks.json`. Agreement (both accept or both don't) per batch is the main quality signal. Findings become prompt changes through a pm decision before the next batch; procedure in `authoring/QC.md`.
- Consequences: `qgen batch` still takes no arguments (D-36); one opus call more per sampled question. Sample size and agreement rate: pm decision 2. Plan 12's exit check reads the spot checks. pm plan 16 (Quality control after every batch) has the tasks.
- Supersedes / related: D-33, D-36, D-38, D-52, D-53, D-55

## D-57: Server errors are codes; the client renders them
- Date: 2026-10-11
- Context: the game server sent Spanish error texts and joker reasons, outside the UI catalog (M3, plan 22).
- Decision: `GameError(code, params)`; codes in `ERRORS` (`app/server/game.py`) with English templates. Error bodies are `{"error": code, "params", "message": English, "supply"}`; 404/500 are `not_found`/`server_error`. Joker `reason`s are `{"code", "params"}`. The client turns player-facing codes into Spanish (`app/client/src/lib/errors.ts`, later the `es` catalog); internal codes show the English `message`.
- Consequences: `str(e)` is English (logs). PORT-1 fixtures and PORT-3 carry the same codes; parity compares `error`/`params`. `/api/flags` and authoring errors unchanged.
- Supersedes / related: D-25; plan 12, plan 21 (LUI-1)

## D-58: Engine randomness is an injected `Rng`; parity uses a recorded shuffle tape
- Date: 2026-10-11
- Context: PORT-1 fixtures must make the Python referee's randomness replayable in the TS engine (plan 12, plan 18). Reproducing Python's Mersenne Twister in TS is work with no value for the game.
- Decision: No shared PRNG. All referee randomness is `random.shuffle`; the recorder logs each call as `{site, n, perm}` (`perm[j]` = old index now at j). The TS engine takes an injected `Rng` with `shuffle(xs, site?)` (in place); tests use `tapeRng(tape)`, which fails on a wrong `n`, a site mismatch or a missing/leftover entry. Production `rng.ts` is any seedable PRNG.
- Consequences: PORT-2/3 shuffle at the same points, in the same order, on arrays of the same length (also inside `view`). Format: `app/client/src/engine/fixtures/README.md`.
- Supersedes / related: plan 12 (PORT-1–3), plan 18

## D-59: No family mode; the Python server is a bridge to the Steam build
- Date: 2026-10-12
- Context: Plans spoke of a "family mode" or family version that would live on next to the Steam release (D-34, plan 12's `ServerStore` "family mode, the default for now"). The developer: the game will be a Steam application; there won't be a family mode.
- Decision: Two implementations only: the current one (`trivia`, Python server + browser) and the Steam build (desktop shell, S3+). The current one keeps working until the Steam build replaces it; it gets nothing the Steam build won't have. The Python game server after the port: static files plus `/api/save` only (pm decision 4, option 3): flags move into `SaveData`, categories become static files from `qgen export`, media is served from the synced cache only (no download on miss; `trivia-media sync` before play).
- Consequences: `trivia-authoring` reads flags from `game.json` and never writes it (it skips flags it already turned into reviews). "The family" in plans means the people who play and test, not a separate product or pool. Supersedes D-34's "the family game stays the priority" and the family half of D-47's flag file.
- Supersedes / related: D-3, D-17 (download on miss, for the game), D-34, D-47; plan 12, plan 11

## D-60: Authoring gets the supply check from the TS engine via Node
- Date: 2026-10-12
- Context: After the port, only `qgen report` and the authoring start page use `app/server/selection.py`. Age groups (M5), bundles and per-language supply will change the selection rules, in TS first.
- Decision: No Python copy (pm decision 5, option 2). A small Node entry point runs `engine/selection.ts` and prints the supply as JSON; `qgen report` and `authoring/server/overview.py` call it. The engine stays runnable under plain Node 22 (type stripping): erasable syntax only, `.ts` import extensions.
- Consequences: Node is needed for `qgen report` (it's in the flake). `selection.py` is deleted with PORT-8. The selection fixtures guard only the Python → TS port, not a second copy.
- Supersedes / related: D-59; plan 12 (PORT-2, PORT-8)

## D-61: Media with Commons restriction flags stays
- Date: 2026-10-12
- Context: Commons marks some files with non-copyright restrictions (personality rights, trademark, insignia, …). Milestone 4 listed them among the files to replace; plan 17 suggested checking each one.
- Decision: Keep every flagged file (pm decision 8). The developer checked them: no problem in any. The licence audit shows the flags for information; they never put a file on the replacement list.
- Consequences: No per-file "checked, keep" mark, no review-tool control for it. Replacement list: PD-US only, GFDL, off-allowlist licences, missing data.
- Supersedes / related: D-59; plan 17 (PUB-1), milestone 4

## D-62: PD-US-only media is replaced; US government works count as free
- Date: 2026-10-12
- Context: Public-domain files carry Commons PD templates (`pd_reasons`). Some only say the work is PD in the US (expired US copyright, no notice, not renewed); a worldwide release needs more. US government works (`PD-USGov*`, ~55 files) are PD in the US by law, abroad less clear-cut.
- Decision: A PD file goes on the replacement list when every reason is US-only: `PD-US*` except `PD-USGov*`, `PD-1923`, `PD-Harris-Ewing` (`providers.US_ONLY_PD`). Any other reason (`PD-old-*` incl. `PD-old-70-1923`, `PD-self`, `PD-author`, `PD-Art`, `PD-USGov*`, `PD-NASA`, `PD-Highsmith`, …) makes the file ok. `PD-USGov*` is ok: generally treated as free elsewhere, as in plan 17.
- Consequences: `providers.licence_verdict` is the one check for the audit report, the review tool and `qgen validate`. Today: q-1100, q-1194 replace (PD-US only).
- Supersedes / related: D-45, D-61; plans 17 (PUB-1), 52, 53

## D-63: The desktop shell is Electron; the Steam binding is picked in SW-2
- Date: 2026-10-12
- Context: The Steam build needs a desktop shell around `app/client/dist/` (OQ-29, plan 18). Options: Electron, Tauri v2, browser + local server (facts in pm decision 12, checked 2026-10-11).
- Decision: Electron (pm decision 12). One Chromium on Windows, Linux and the Deck, so the client behaves as on the TV today; a LAN server for phone buzzers (OQ-37) would be Node `http` in the main process. Steam binding: steamworks-ffi-node or steamworks.js, chosen in SW-2 (steamworks.js stale since 2024-08, steamworks-ffi-node active but young).
- Consequences: ~125–160 MB download for the shell. Builds with electron-builder (SW-5, SW-6); the page talks to the shell through a preload bridge (no Node in the page). Overlay on native Linux/Deck is uncertain; fallback: the Windows build via Proton (SW-12). No Tauri or PyInstaller build. Steam binding: steamworks-ffi-node (pm decision 28, 2026-10-12; added in SW-8), main process only; electron-builder needs `asarUnpack` for it, `koffi`/`@koromix/koffi-*` and our Steamworks SDK `redistributable_bin`. Its overlay is experimental (offscreen render, X11 only).
- Supersedes / related: D-59; plans 11, 12, 18; OQ-29, OQ-37

## D-64: Engine tests run on `node:test` with Node's type stripping
- Date: 2026-10-12
- Context: The TS engine (PORT-2/3) needs tests that replay the parity fixtures. Vitest or `tsc` builds would add dependencies or build output; the flake's Node 22.23 strips types unflagged.
- Decision: `node --test 'src/engine/**/*.test.ts'` (`npm test`, root and `app/client`). Engine code uses erasable syntax only and imports with `.ts` extensions (`allowImportingTsExtensions`, `erasableSyntaxOnly` in both client tsconfigs). No `@types/node`: `*.test.ts` and `src/engine/test/` are excluded from the tsconfigs, so tests aren't type-checked; engine modules never import from `node:`.
- Consequences: No new dependency, no build step for tests. `GameError` in `lib/api.ts` lost its parameter properties. Same setup lets authoring run the engine under plain Node (D-60).
- Supersedes / related: D-58, D-60; plan 19 (PORT-2), task 72

## D-65: `qgen rework --model fable` is opt-in for fix and review 1
- Date: 2026-10-12
- Context: Rework handles the hardest needs_work cases at small volume (rework-1: 43 questions, $5.57); a stronger model may pay off there first. Fable costs 2.5× Opus per token (plan 58).
- Decision: `qgen rework --model {opus,fable}`, default `opus`. Switches fix and review 1 (it decides keep/fix after the reworked fix); fact check stays `sonnet`; review 2 stays `REVIEW_MODEL` (opus) so the final verdict is comparable to rework-1. Model stored in `run.json`; on resume `--model` is ignored with a notice.
- Consequences: `qgen batch`, `qgen tighten`, `REVIEW_MODEL` unchanged. Model per call already in `costs.log` and `review.model`. RUNBOOK unchanged until the experiment (task 345) changes the default.
- Supersedes / related: QG-23; plans 16, 58

## D-66: The client holds the correct answer; the view still hides it
- Date: 2026-10-12
- Context: The TS referee (PORT-3, plan 20) runs in the browser, so the pool with answers and all hints is in client memory. D-25/D-26 said the client never learns the correct answer before the final answer.
- Decision: Accepted for an offline party game: devtools only spoil your own game. The view (`Game`) still carries no correct answer before the final answer and only the hints played; screens render only the view, never `PoolQuestion` or the save.
- Consequences: Relaxes D-25/D-26 "the client never learns the correct answer". Engine modules (`app/client/src/engine/`) may hold the pool; screens go through the view only (PORT-7).
- Supersedes / related: D-25, D-26; plans 12, 20

## D-67: The save is one JSON document, written whole by the client
- Date: 2026-10-12
- Context: The TS engine (PORT-3) runs the rules in the browser; the Python server becomes a store (PORT-4). Today's state is `state/game.sqlite` plus `state/flags.json` (D-47).
- Decision: `state/game.json` `{version: 1, players, games, burned, flags}`. The client writes it whole via `PUT /api/save`; the server checks only the envelope (object, `version` 1, three lists, `flags` object, ≤ 10 MB), no game logic, no merge. Atomic write (tmp + fsync + replace, retry on Windows locks → 503 `save_locked`). Flags live in the document. Authoring reads it, never writes it, and keeps its own applied-flags ledger (`state/flags-applied.json`). Migration from SQLite runs once on a copy; `game.sqlite` and `flags.json` stay as the backup.
- Consequences: One writer (one TV tab), no revision check; `ServerStore` serializes its PUTs. `migrate()` is wired into startup only at the switch-over (PORT-7). The desktop shell's `FileStore` writes the same document.
- Consequence (pm decision 98, 2026-10-13): a `game.json` the client can't parse (corrupt, newer version) moves via `POST /api/save/backup?kind=corrupt|newer` to `state/backup/game-<kind>-<stamp>.json`, as on the desktop (D-72); the game starts fresh and names the backup path once on the start screen.
- Supersedes / related: D-4, D-25, D-47, D-59, D-66; plans 12, 49 (PORT-4, PORT-5)

## D-68: Age group and bundles are settings per game
- Date: 2026-10-11
- Context: The TS referee plays one audience: 12 levels with D-22's fixed ranges over every bundle. Milestone 5 lets players pick an age group (AG-7) and bundles (BN-6) before a session; old saves and plan 18's fixtures must keep playing unchanged.
- Decision: `age_group` and `bundles` live in each game's `settings`, next to `jokers`. Missing keys mean `young_teens` and every bundle in `bundles.json`, resolved on read, never written back. Every `always_on` bundle (only `base`) is always on. Level ranges per group live in `app/data/age-groups.json` (`levels`, 12 `[lo, hi]` pairs); `young_teens` = D-22, the others a draft until tuned (plan 28). Burns stay per player across groups and bundles (D-28).
- Consequences: The engine drops its `LEVEL_RANGES` constant; the Python referee keeps its copy until PORT-8. `parseAgeGroups` and `qgen validate` check the `levels` rules. Plan 27 (engine), 29 (start screen), 28 (tuning).
- Supersedes / related: D-22, D-28, D-38, D-39; plans 21, 22, 27

## D-69: The engine runs in the browser behind `lib/api.ts`; data from `/data/`
- Date: 2026-10-11
- Context: PORT-7 (plan 50) moves the screens from the Python referee to the TS engine (D-66, D-67).
- Decision: The game data (`pool.json`, `bundles.json`, `age-groups.json`, categories files) comes from `GET /data/…`, served read-only from `app/data/`, loaded once per page load. `lib/api.ts` keeps its exports and runs `engine/api.ts` on an in-memory save, one call at a time (promise-chain mutex). Each successful action PUTs the whole document (`/api/save`); reads never PUT; a failed PUT keeps the new save in memory and shows the server's error. `trivia` runs `save.migrate()` at every start (no-op once `game.json` exists).
- Consequences: A new `qgen export` needs a page reload (F5). The Python game routes are unused until PORT-8 deletes them. Rollback: delete `state/game.json`, check out the commit before the switch.
- Supersedes / related: D-25, D-35, D-59, D-66, D-67; plans 12, 49, 50

## D-70: UI strings in a typed nested catalog, read through `t()`
- Date: 2026-10-11
- Context: LUI-1 (plan 21) moves every on-screen string out of the game code, with no i18n library (M3).
- Decision: One catalog per language in `app/client/src/locales/<lang>.ts`, a nested object; `es.ts` is the source, `as const`, and defines `Catalog` (string leaves widened). Leaves: string, plural map (`{ one, other, … }`, picked by `params.n` via `Intl.PluralRules`) or `string[]` of variants (`variants(key)`). Keys are dotted paths; `TextKey`/`VariantsKey` (union `Key`) make a typo fail `npm run check`. `{name}` placeholders, numbers via `Intl.NumberFormat(lang)`. Missing at runtime → `⟦key⟧`, no fallback. `lang` is `es`; `?lang=` only in dev. `main.ts` sets `<html lang>` and `document.title` (`app.title`).
- Consequences: Level brackets and lists (which levels have a line) stay in code, texts in the catalog. Namespace `error` reserved for plan 22. `xx` (plan 23) and `en` (plan 24) must satisfy `Catalog`.
- Supersedes / related: D-6, D-57; plans 21, 22, 23, 24; LUI-1

## D-71: The desktop shell serves the client's own URLs over `app://`, offline
- Date: 2026-10-12
- Context: SW-2 (plan 54): the Electron shell (D-63) plays `app/client/dist/` with no Python process; the client must stay unchanged for the browser game (D-59).
- Decision: `protocol.handle("app")` (privileged: standard, secure, fetch, stream); the window loads `app://trivia/`. `app/desktop/resolve.mjs` answers the same URLs as `app/server/main.py`: `/data/…` from `app/data/`, `/media?url=…` only for pool URLs, `cache_path` file names, `404 media_missing`, no download; `Range` → 206; `/api/…` → 404; else `dist`, SPA fallback. No network: every `http(s)`/`ws(s)` request cancelled, navigation and new windows blocked, permissions denied except fullscreen; `contextIsolation`, `sandbox`, no Node in the page. Bridge `window.trivia` = `{desktop, toggleFullscreen, quit}` over fixed IPC channels, sender origin checked. Store `MemoryStore` when `desktop` is set, until SW-3. Dev Electron from nixpkgs (`pkgs.electron`, 43) via `trivia-desktop`; the npm binary doesn't run on NixOS.
- Consequences: No URL adapter in the client; `lib/desktop.ts` is the only desktop branch (overlay fullscreen, «Salir del juego», authoring links hidden, store). The save is lost on quit until `FileStore` (SW-3). SW-3 adds `loadSave`/`writeSave` to the bridge, S5 the Steam calls. Packaged roots under `resourcesPath` are part 3's (SW-5). Electron's dev-only "Insecure Content-Security-Policy" console warning shows until packaged.
- Supersedes / related: D-35, D-59, D-63, D-67, D-69; plans 18 (SW-2), 54

## D-72: The desktop save is one file in the user's config folder; main stores, the client validates
- Date: 2026-10-12
- Context: SW-3 (plan 55): the desktop shell (D-71) kept the save in memory; it must survive a restart and a crash, and later sync via Steam Auto-Cloud (S5).
- Decision: `<userData>/save/game.json`, userData fixed to `<appData>/trivia` when packaged (`%APPDATA%\trivia`, `~/.config/trivia`), `<repo>/state/desktop/game.json` in dev, `TRIVIA_SAVE_DIR` overrides both. Per Steam user since plan 87 (2026-10-13, decisions 111, 114): `save/<steamid64>/game.json` for a valid Steam user (SteamID fixed per session); dev switch without a SteamID `save/dev/game.json`; `TRIVIA_SAVE_DIR` is the folder itself (no subfolder); no valid user → no save file, no folder, `save:*` refused, the page plays memory-only (`MemoryStore`) with a notice; no `local/`, no migration (S3's `save/game.json` and old `local/` left alone, never read); Steam starts before the folder is picked. `app/desktop/save.mjs` is a dumb store like the Python server (D-67): envelope check only (≤ 10 MB, object, numeric `version`) → `bad_save`; tmp + fsync + rename, lock retry 10 × 100 ms → `save_locked`; one write in flight, quit waits for it; a stale `.tmp` is dropped at start. The client's `parseSave` validates; corrupt or newer-version file → `backup/game-<kind>-<stamp>.json`, fresh save, message. `game.json.tmp`, `backup/` and `dev/` sit outside Auto-Cloud's pattern (subdirectory `trivia/save/{64BitSteamID}`, `game.json`, non-recursive). `--import-save <file>` copies a browser save into the user's folder when none exists, else refuses on stderr; without a valid user it exits 1.
- Consequences: IPC `save:load`/`save:write`/`save:backup`, rejections carry the code as the message. `FileStore` (plan 55 part 2) replaces `MemoryStore` in the shell. `save_locked` doesn't fail the action: `lib/engine.ts` adopts the reply, keeps the error (`saveError()`), the screens show it in the error corner until a write succeeds; the next action writes the whole document again. S5's Auto-Cloud config points at this path.
- Supersedes / related: D-63, D-67, D-71; plans 18 (SW-3), 55

## D-73: Local desktop builds: Windows zip and Linux tar.gz from Linux, media beside the asar
- Date: 2026-10-12
- Context: SW-5 (plan 56): the desktop shell (D-71) with file saves (D-72) must become artefacts a family unpacks and plays offline, built on the developer's NixOS machine.
- Decision: electron-builder, `app/desktop/electron-builder.yml`; `trivia-desktop-build` (dev shell) = `qgen validate`, client build, `stage-media.mjs`, `electron-builder --x64 --linux tar.gz --win zip` → `app/desktop/release/Trivia-<version>-{win,linux}-x64.{zip,tar.gz}`.
  - Targets: Windows x64 `zip` (Steam installs folders, no installer), Linux x64 `tar.gz` (no AppImage: needs FUSE, its tooling fails on NixOS; the Deck runs the Linux folder). No wine: `win.signAndEditExecutable: false` → Electron's icon and file metadata, unsigned exe (SmartScreen warns) until S5 (B-11).
  - Own lockfile: `app/desktop/package-lock.json` with devDependencies `electron` (exact 43.7.7, the flake's) and `electron-builder`; not a root workspace (overrides plan 54's "part 3 makes it a workspace"). Root `npm install` and `nix build .#app` stay untouched (D-59).
  - Layout: `resources/app.asar` = `package.json`, `main.mjs`, `resolve.mjs`, `save.mjs`, `preload.cjs` only; `resources/client` (client `dist/`), `resources/data` (`app/data/`), `resources/media` outside the asar (S5 ships media as the shared content depot without repacking). `roots()` packaged branch reads them under `process.resourcesPath`; `TRIVIA_MEDIA` overrides media.
  - Staging: only the pool's `media` + `background` `file_url`s (`poolUrls`, `cacheName` shared with the resolver), hard-linked (fallback copy) from `TRIVIA_MEDIA` or `<repo>/media` into an emptied `app/desktop/build/media/`; missing → exit 1, `--allow-missing` builds anyway. As is, no resizing (SW-9): 1102 files, ~2.5 GB today.
  - Linux sandbox: a `tar.gz` has no SUID `chrome-sandbox` and Ubuntu ≥ 24.04 / Steam's runtime block user namespaces → `after-pack.mjs` renames the binary to `trivia-bin` and writes a `trivia` shell launcher adding `--no-sandbox` (`linux.executableArgs` only reaches desktop files). Same as AppImage's default; the page is local, no Node, no network (D-71). Windows keeps the sandbox.
  - Offline: Electron zips are cached in `~/.cache/electron`; their sha256s are pinned in `electron-builder.yml` (`electronDownload.checksums`, with `force: false` so electron-builder passes them on), else `@electron/get` fetches `SHASUMS256.txt` every build. Electron's npm binary is skipped (`ELECTRON_SKIP_BINARY_DOWNLOAD=1`, useless on NixOS). No `steam-run` needed: the builder's helpers run on NixOS.
- Consequences: an Electron bump updates `package.json`, the flake's major and the pinned checksums together. `qgen validate` lives in the flake wrapper, not the npm script (`app/` never calls `authoring/`). No auto-updater, no crash upload, `publish: null`.
- CI (SW-6, pm decision 14, 2026-10-12): no GitHub Actions; CI is local. Per commit: `npm run check`, `npm test`, `npm run build`, `qgen validate`, the task's own check (AGENTS.md). Before every Steam upload (S5): a release check (per-commit checks, `trivia-media licenses`, release bar of pm decision 15, `nix build .#app`, both packaged builds, scripted CDP smoke game, manual checklist); upload by hand with SteamCMD. SW-6 moved to S5 (plan 10 part 7); no GitHub Actions secrets.
- Supersedes / related: D-59, D-71, D-72; plans 18 (SW-5), 54, 56

## D-74: Five game modes, no default mode; no skip outside gamemaster mode
- Date: 2026-10-12
- Context: OQ-30 (default mode: presets, checkpoints, admin actions), MD-5 (plan 35); pm decisions 19 and 20, milestone 7 "Game modes".
- Decision:
  - **Five modes**, no "default mode"; ids in `settings.mode`: `gamemaster`, `solo`, `rr-coop`, `rr-competitive`, `timed`. English names first, Spanish with i18n.
    - **Gamemaster mode** (`gamemaster`, today's game): one person holds every control; "configure game" screen before every game; `Esc` menu with arbitrary cheats (jokers, skip, replace, undo, …).
    - **Alone or as group** («Solo o en grupo», `solo`): one player or everyone as one team; the player picks the age group, no difficulty selection; standard joker set; customization only via a small "Customize game" button on the age group screen.
    - **Round-robin co-op** (`rr-coop`), **round-robin competitive** (`rr-competitive`), **competitive timed** (`timed`): specs in plan 41 (OQ-37).
  - **No presets** (Fácil/Normal/Difícil/Experto dropped), **no checkpoint**, no difficulty knob besides the age group; the mode never shifts the age-group window (D-38).
  - **Standard joker set**, the same for every age group: 3 × Soplo, 1 × each other joker.
  - **Outside gamemaster mode:** a question can never be skipped, not even a broken or far too hard one; no undo, no free skip, no replacement, no joker changes mid-game. «Reportar pregunta» only logs the question to a local report list (no burn, no replacement). «Abandonar partida» and sound stay.
  - **Steam achievements** in every mode except gamemaster mode and customized games (`settings.customized`).
  - **Input:** gamepads, keyboard, mouse; no phones. Multiplayer modes add a "shared keyboard": one dedicated key per player hands them keyboard and mouse until their turn is done.
- Consequences: Plan 13 rewritten (one section per mode, implementation notes for MD-6/MD-7 and MD-10..MD-12). `settings.mode` missing = `gamemaster`, old saves unchanged; `settings.jokers` (MD-1..MD-4) stays. Plans 36 (MD-6, MD-7), 41 (OQ-37), 59 (MD-10..MD-12) build on this; S5 reads `settings.customized` for achievements.
- Supersedes / related: D-27, D-28, D-30, D-38; plans 13, 35, 36, 41, 59

## D-75: Release content target: 5000 approved per launch language, no games-per-player number
- Date: 2026-10-12
- Context: OQ-32, CT-1 (plan 38); pm decision 21 (target), pm decision 26 (launch languages: Spanish, English, German).
- Decision:
  - **Target:** 5000 approved questions per launch language (es, en, de), with D-53's per-level mix (`authoring/data/targets.json`).
  - **No games-per-player number:** no bar a simulation must meet.
  - CT-2 (`qgen report --simulate`, S4) reports games per new player per mode, for information only. Burns per game: «Solo o en grupo» and round-robin co-op = 12 + the standard joker set's burns (3 × Soplo, 1 × each other joker, D-74); round-robin competitive ≈ N players × that; competitive (timed) ≈ 1 shared question per round, no jokers.
  - Later languages (zh-Hans, ru, pt-BR, milestone 12): no target now.
  - Quality bar unchanged: D-56, pm decision 2, release bar plan 57 (CT-5, pm decision 15).
- Consequences: S4's exit = every launch language reaches the target, not a simulated games number. Whether a translated pool counts toward a language's 5000 follows plan 37's D-entry (OQ-31); open until then.
- Supersedes / related: D-52, D-53, D-56, D-74; plans 16, 37, 38, 57

## D-76: Tuned age-group windows, level ranges and level weights
- Date: 2026-10-12
- Context: AG-7, plan 28; D-68's ranges for `kids`, `young_adults`, `adults` were a draft. Measured on the pool (plan 21, "Measured windows"); pm decision 22: approve the proposal.
- Decision:
  - `young_teens`: unchanged, window 1–10, D-22's ranges.
  - `kids`: window 1–6; 1, 2, 2–3, 2–4, 3–4 ×2, 3–5, 4–5 ×2, 4–6, 5–6 ×2.
  - `young_adults`: window 4–13; 4, 5–6, 6–8, 7–9 ×3, 8–10, 9–11, 9–12, 10–13, 11–13 ×2.
  - `adults`: window 5–15; 5, 6–7, 7–9, 8–10 ×2, 8–11, 9–11, 10–12, 10–13, 11–14, 12–15, 13–15 (top widened downward, not the window shrunk).
  - `level_weights` per group in `age-groups.json`: per difficulty of the window, round(12 × Σ 1/(hi − lo + 1)) over the levels containing it, half up (= 3 × expected cards per game, D-31's method); each sums to 144. `young_teens` = `qgen.LEVEL_WEIGHTS`.
  - `parseAgeGroups` and `qgen validate` require `level_weights` = what `levels` derive.
- Consequences: Thin top (14: 19, 15: 8 approved) limits adults to ~8 games per player; reported for milestone 1, not fixed. `qgen` keeps `LEVEL_WEIGHTS` until AG-8 (B-12). Windows feed authoring targets only with a `focus` (D-40); `focus` is null. Plan 21's demand table recomputed.
- Supersedes / related: D-22, D-31, D-38, D-40, D-53, D-68; plans 21, 27, 28

## D-77: Three multiplayer modes; per-player gamepads and a shared keyboard, no phones
- Date: 2026-10-12
- Context: OQ-37 (competitive and couch co-op: format and input), plan 41; pm decisions 23 and 24, milestone 7 "Game modes"; modes and ids from D-74.
- Decision:
  - **All three:** no skip, no undo, no replacement, no joker changes mid-game; «Reportar pregunta» only logs (plan 36); achievements unless customized (`settings.customized`); the mode never shifts the age-group window (D-38).
  - **Round-robin co-op** (`rr-coop`): players take turns, one question each, in join order; one team, one game, one age group; one shared standard joker set (3 × Soplo, 1 × each other joker); a wrong answer ends the game for the team as today; level 12 = everyone wins.
  - **Round-robin competitive** (`rr-competitive`): players take turns in join order; each player plays their own independent game with their own jokers (standard set) and own age group; a wrong answer ends only that player's game, the others go on; first to level 12 wins.
  - **Competitive (timed)** (`timed`): everyone answers the same question at once, each with their own input; own track per player; one age group; the question's difficulty = average of the active players' levels; 30 s to answer, a hint every 8 s; no jokers; a wrong answer = out at once; three levels behind the leader = out; first to level 12 wins; timeout = all players lose at once; pulsing red frame around the screen during the last 3 s.
  - **Input:** one gamepad per player (Gamepad API), keyboard, mouse; **shared keyboard**: every player has one dedicated key; pressing it hands that player keyboard and mouse until their turn is done. No phones, no buzzers.
  - **Burn multiplier per mode** (D-28 burning, D-75 simulation): round-robin co-op ≈ 1 game's burns (12 + the standard set's burns); round-robin competitive ≈ N players × that; competitive (timed) ≈ 1 shared question per round, no joker burns.
  - **Shell needs:** several gamepads via the Gamepad API and the shared keyboard, nothing more; no LAN server, no firewall prompt (D-63's phone-buzzer server dropped).
- Consequences: Plan 13 specs the three modes (MD-8, MD-9), plan 14 section 3 the input (IN-6); IN-7 closed (no phones). Building them stays "Later", after the release (plan 43). Remote Play Together works once local multi-pad input works.
- Supersedes / related: D-28, D-38, D-63 (LAN server note), D-74, D-75; plans 13, 14, 16, 34, 38, 41

## D-78: Launch languages es, en, de; base in es-419 with an es-ES variant
- Date: 2026-10-12
- Context: OQ-31, I18N-1 (plan 37); pm decisions 26 (launch languages) and 27 (Spanish variety, store languages). Today: Spanish with Colombian usage (D-6); regions are bundles (D-39, D-49); store names D-50.
- Decision:
  - **Launch languages:** Spanish, English, German (`es`, `en`, `de`). Later: Simplified Chinese, Russian, Portuguese (Brazil) (`zh-Hans`, `ru`, `pt-BR`), milestone 12 "Conquer the world" (on hold).
  - **Spanish variety:** two variants.
    - `base` in neutral Latin American Spanish (`es-419`); the ~40 Colombianisms are rewritten through the pipeline (D-36), S4 content work.
    - `es-ES` variant only where the wording differs: regionalisms, `vosotros` in the UI.
    - The `colombia` bundle keeps its Colombian voice.
    - No finer variants; regional flavour comes from bundles (later e.g. `mexico`, `argentina`).
  - **Steam store languages:** Spanish – Latin America, Spanish – Spain, English, German.
- Consequences: LUI-5 = `en`, `de` catalogs plus an `es-ES` override of `es`; QT-6 targets `en`, `de`; the house style says neutral Latin American Spanish for `base`. D-75's target applies to es, en, de; whether a translated pool counts toward a language's 5000 is left to 15b/S4 (not decided here). Plan 24 (`en.ts`) becomes launch work.
- Supersedes / related: D-6 (Colombian usage, now `colombia` only), D-39, D-49, D-50, D-75; plans 15, 15a, 15b, 15c, 24, 37, 38

## D-79: The Steam release bar is D-56's quality bar
- Date: 2026-10-12
- Context: CT-5, plan 57; pm decision 15 (release bar: D-56's numbers or stricter).
- Decision:
  - **Release bar:** D-56's numbers only: spot check ≥ `quality.spot_check_size` (30), agreement ≥ `quality.min_agreement` (90 %); no new keys, no false-approve limits.
  - Per batch and per back-audit slice (`backaudit-<k>`); release-ready derived from `authoring/data/spot-checks.json`, not stored.
  - Below it: not release-ready; it only feeds QC step 4 (prompt changes). No full audit (`audit --all`), no second spot check.
  - Back-audit of the pre-D-56 pool: `qgen audit --backlog`, slices, developer asks (plan 57).
- Consequences: `qgen report --qc`: row "release" (✓ or ✗ + failed limit), "Release bar" line in the QC section. QC.md step 3. S4 close-out reads the release row.
- Supersedes / related: D-56, D-75; plans 16, 57

## D-80: Competitive (timed): claim-based rounds with lives
- Date: 2026-10-12
- Context: OQ-37 follow-up, plan 61; milestone 7 "Game modes", "Competitive (timed)" (task 394) replaces the timed part of pm decision 23's answer recorded in D-77.
- Decision:
  - **Format:** 12 rounds; round = level (the question's difficulty follows the round); questions per round = number of players; one age group for everyone; no jokers.
  - **Questions:** every question shown to all players; 30 s per question, a hint every 8 s; unclaimed after 30 s = next question, nothing else.
  - **Claim:** own action; any player, any time → that player has 6 s to answer; 6 s timeout = wrong answer; once the answer is shown, the next question comes; players may claim again after scoring.
  - **Lives:** three per player; round end: no correct answer in that round = −1 life; wrong answer (or claim timeout) = out at once; third life lost = out.
  - **End:** round 12 is sudden death: first claim + correct answer wins at once; only one player left = wins at once.
  - **Visuals:** rounds and lives (hearts); a heart pulses at a player's last chance in a round without a correct answer, stronger on their last heart; last 3 s of a claim: a clock ticks once per second, louder each tick, plus a pulsing red frame; the same red frame when everyone is at risk at once (all on their last life, nobody correct this round yet).
  - **Burns** (D-28 burning, D-75 simulation): ≈ N questions per round (N players) for up to 12 rounds, fewer after drop-outs; no joker burns.
  - Open detail (not a decision): after drop-outs, do questions per round follow the players still in?
- Consequences: Plan 13 "Competitive timed", MD-8, MD-9 and plan 14 section 3, IN-6 (claim action, per-player claim keys on the shared keyboard) follow this entry; plan 16 burns per mode updated. D-75's target (5000 per language) unchanged.
- Supersedes / related: D-77 (timed part), D-75 (timed burns), pm decision 23

## D-81: Translated questions: one file per locale, derived staleness, names files
- Date: 2026-10-12
- Context: QT-1 (15b "Storage", preference A), I18N-3 (plan 15), plan 63; launch languages D-78; `app/` never reads `authoring/` (D-35).
- Decision:
  - **Source:** `authoring/data/questions.json` stays the Spanish source, unchanged.
  - **Locale files:** `authoring/data/questions.<locale>.json` per translated locale (`en`, `de`, D-78): `{"version": 1, "locale": "en", "questions": [...]}`, sorted by id, same ids as the source.
  - **Entry fields:** `id`, `source_hash`, `status` (as the source), `difficulty` (own, D-38 scale, rated for that language's market), `batch`, `review`; translated `question`, `answer`, `wrong_answers`, `hints`, `description`, `fun_fact`. Nothing else: `subcategory`, `bundle`, `media`, `background`, `concept`, `axes` come from the source by id; no media fields.
  - **`source_hash`:** first 12 hex of sha256 over the canonical JSON of the source's text fields (the six above); written when translated.
  - **`stale`:** derived (hash ≠ source's current hash), never stored; left out of the export until re-translated; `validate` warns per locale.
  - **`translatable: false`** on a source question (absent = translatable): wordplay, questions about Spanish, Colombian-only answers; a non-rejected translation of it is a `validate` error.
  - **Export:** `app/data/pool.<locale>.json`, same shape as `pool.json`: source play fields (`id`, `subcategory`, `bundle`, `media`, `background`) + translated text and `difficulty`; only when source approved and translatable, translation approved and not stale. No `pool.es.json`; `pool.json` unchanged.
  - **Names:** Spanish subcategory names stay the keys everywhere. Hand-maintained, shipped `app/data/names.<locale>.json` (`bundles`, `categories`, `subcategories`, `age_groups` by id, pm decision 48) and `app/data/bundles/<id>/names.<locale>.json` (same without `bundles`, `age_groups`), mirroring D-43.
- Consequences: `authoring/tools/translations.py` is the one reader/writer; `qgen validate` checks locale files, names and export staleness. Whole-pool rewrites of the source (`qgen tighten`, neutral Spanish) stale every touched translation, so full translation runs come after them.
- Supersedes / related: D-35, D-36, D-38, D-39, D-43, D-78; plans 15, 15b, 62, 63

## D-82: Seen counters instead of burning
- Date: 2026-10-12
- Context: Burning (D-28) makes a profile's pool a dead end: once a level's supply runs dry the game refuses to start. The developer's call (2026-10-12, plan 65): repeats become a fallback, ordered by how often a question was seen.
- Decision:
  - **Profile = save:** one save = one profile (on Steam one per SteamID; otherwise `state/game.json` or the desktop save). Player names stay labels («Continuar: Sofía, nivel 5», history, turn order); they no longer scope selection. Every seen event counts for the whole save, in every mode.
  - **Seen events:** the ones that burned under D-28: answered, skipped (joker or admin), swapped away, Snipe hit. Descriptions on unpicked cards don't count.
  - **Save v3:** `seen: {question_id, game_id, seen_on}[]` replaces `burned`; count(q) = rows for q; one row per event, so undo removes exactly that game's row. `blocked: string[]`: hard exclusion; «Saltar y quemar para todos» becomes «Bloquear pregunta». `notified_exhausted`: subcategories already announced as exhausted. Migration v2 → v3 in `parseSave`: each `burned` row with `player_id` → one `seen` row; `player_id: null` → `blocked`.
  - **GF-7 «Borrar jugador»:** deletes the name and its games, keeps their seen rows.
  - **Selection:** `available` = approved, active bundles, not blocked, not offered this game, not purged; seen questions stay in. `draw` sorts the shuffled candidates by `(count, category key)`: lowest count always wins, category variety only breaks ties; then the first candidate that keeps the later levels fillable. Jokers draw the same way.
  - **Supply check:** the hard failure stays only for "the whole pool minus blocked, any count, can't fill 12 levels".
  - **Low-supply warning** (game start, informational, «Jugar» stays; decision 31): warn only when a level the planned session needs (mode, bundles, age group or custom range, levels) has ≤ 1 unseen question under one Hall assignment, with those levels' difficulty ranges; none left at some level: «En esta partida pueden salir preguntas que ya vieron.» No early-notice threshold, for every running-out message. Fresh games left k stays an engine/simulation figure, not a warning trigger.
  - **Exhausted subcategories** (informational): every approved question of it in the active bundles, within the age group's difficulty span, has count ≥ 1 → listed once at game start; no effect on selection.
  - **Python referee:** `app/server/game.py` (unused since PORT-7, deleted by plan 51) keeps its SQLite burn rules; divergence accepted. `app/server/save.py` only checks the envelope (D-67).
- Consequences: Plan 65 (tasks 421–429). Engine invariant "burned never comes back" becomes "never a count-k card while a count-<k card fits and keeps the later levels fillable". CT-2 headline: games until the first repeat.
- Supersedes / related: D-28 (burn rules); D-27, D-59, D-67, D-75; plan 65

## D-83: Neutral Spanish rewrite via `qgen neutralize`; voice per bundle
- Date: 2026-10-12
- Context: D-78 puts `base` in es-419; the house style said Colombian usage for every bundle, so each `base` batch added Colombianisms. Plan 64, pm decision 32 (prompts approved as drafted, numbers RAE style).
- Decision:
  - **Voice per bundle:** `voice` string per bundle in `app/data/bundles.json`, filled into `house-style.md`'s `{voices}`. `base`: neutral Latin American Spanish (a word understood across Latin America and Spain where one exists; "tú"); `colombia`: Colombian usage.
  - **Numbers (all bundles, RAE):** no separator up to 9999 ("2640"), a space from 10 000 ("42 195"), decimal comma ("42,195").
  - **Review/audit:** a `base` question in Colombian or other national wording is `needs_work` (`review.md`, `audit.md`).
  - **`qgen neutralize`:** one more developer-asked command (amends D-36), like `qgen tighten`: run `neutralize-<n>`, scan of `base` (approved + needs_work, `prompts/neutralize.md`) → fix → review 1 → research → review 2 → record → audit → export → sync; report `authoring/reports/neutralize-<n>.md`. `--dry-run`: scan, flagged ids, cost estimate.
  - **`es-ES` for questions:** no `questions.es-ES.json` at launch; the scan lists words with no pan-Hispanic form, a sparse override can follow if there are many.
- Consequences: RUNBOOK and AGENTS.md list `qgen neutralize` (only when the developer asks); a run gets a batch's QC (`authoring/QC.md`). It stales touched translations (D-81), so full translation runs come after it. The run itself is masterplan part 11.
- Supersedes / related: D-6, D-36, D-56, D-78, D-79, D-81; B-13; plan 64; pm decision 32

## D-84: Per-locale targets and gaps
- Date: 2026-10-12
- Context: D-75 sets one target per launch language; `en`/`de` fill only by translating `es` sources (D-81). Plan 70 (CT-4), pm decision 37.
- Decision:
  - Every launch language uses `targets.json` `base` (D-75); no locale block, no per-mode, per-age-group or per-preset targets.
  - Deficits per locale: `targets.deficits(pool, bundle, locale)` counts the locale's playing translations by their own difficulty.
  - Source shortfall per level = largest over `en`/`de` of (locale deficit / yield − untranslated approved, translatable `es` sources); yield = approved / decided `tr-<L>-*` translations, 1.0 before a pilot.
  - `draft` and the subcategory ranking for `base`: the `es` deficit while any (D-54); then the source shortfall, so `es` drafting goes past its target; even weights (D-40) when both are zero.
  - Simulation bottlenecks are information, not weights.
- Consequences: `qgen report --locale L`, `--simulate`'s target check and `--cost` (`es` sources past the target) use it. Whether `es` grows past 5000 is part of the release budget (plan 70 task 463).
- Supersedes / related: D-40, D-53, D-54 (amends), D-75, D-78, D-81; pm decision 37; amended by D-99 (regional bundles: 2000 approved each)

## D-85: Base bundles and bundle languages
- Date: 2026-10-12
- Context: Every bundle was offered in every language, and `always_on` forced `base` into each session. Milestone 5 adds per-language bundles and base bundles (`chinese-base` later, milestone 12). Plan 71.
- Decision:
  - **Base bundles:** `kind: base` marks a base bundle; replaces `always_on`. Exactly one per session; zero or two → `base_bundle_count`.
  - **Languages:** every bundle in `app/data/bundles.json` lists `languages`; the game offers only the bundles of its locale (`bundlesFor`); others → `bundle_not_offered`. `base`: es, en, de; `colombia`: es.
  - **Default:** the locale's first base bundle (file order) plus every non-base bundle offered in the locale. es → `base` + `colombia` (unchanged), en/de → `base`.
  - **Nothing added:** `[]` and `["colombia"]` are refused, not completed with `base`.
  - **Stored choices that no longer resolve:** read as the locale's defaults (stored age group kept if known); never written back. Same for the player preset.
  - **`qgen validate`:** errors for missing/invalid `languages`, a leftover `always_on`, an unknown `kind`, a launch language without a base bundle; warnings for a listed bundle without approved questions in `pool.<locale>.json` and for approved questions of an unlisted bundle.
- Consequences: Plan 71 (tasks 480, 481). Start screen (plan 29) picks among `bundlesFor`; docs in plan 30.
- Supersedes / related: D-68 ("every always_on bundle is always on", auto-adding `base`); D-39, D-78; pm decision 26

## D-86: Language setting, per-locale pool and first-start language screen
- Date: 2026-10-12
- Context: I18N-2 (plan 15), plan 68 (tasks 449, 450, 490); launch languages D-78, decision 26: Launch languages (OQ-31); `es-ES` UI-only, decision 27: Spanish variety; files per locale D-81; seen counts by id D-82.
- Decision:
  - **Save field, no version bump:** `SaveData.language?: {ui, questions}`. A stored save without it parses as `{es, es}` (`parseSave`): the family's save and fixtures stay Spanish whatever the browser says. Profile = save (D-82).
  - **Default for a fresh save** (`emptySave()`: no file, 404, backed-up broken file): `defaultLanguage(tag, ui, questions)` per list: exact tag, then its language part (`es-CO` → `es`, `de-AT` → `de`, `es-ES` → UI `es-ES` + questions `es`), else `en` if present, else `es`. Tag: `guessTag()` in `lib/engine.ts` = `navigator.language`; milestone 10 swaps in Steam's client language there.
  - **A game keeps its locale:** `GameRow.locale` (written only for non-es games, decision 36: GameRow.locale: written only for non-es games?; missing = `es`), set by `newGame` from `language.questions`. Continuing loads the game's own locale; a change applies to the next game; no mid-game pool swap.
  - **Options:** UI = `CATALOGS` minus `xx` (`UI_LANGS`); questions = locales with a pool file (`pool.json` for `es`, always). Languages shown by endonym (`lib/i18n.ts`).
  - **Esc menu:** rows «Idioma» / «Idioma de las preguntas» in every mode, each only with ≥2 options. A question locale whose pool fails the supply check for the default bundles is listed, disabled, with the reason.
  - **First-start language screen** (`LanguageScreen.svelte`): before Start, only for a fresh save with something to pick (>1 UI option or >1 question locale); nothing written when skipped, so it asks once a second language ships. UI languages by endonym, guess preselected and focused; Enter / pad A / click / `1`–`n`. A pick sets `ui` and `questions = defaultLanguage(pick)` over the locales whose supply passes (`es` always). Confirming writes `language`: asked once. No Esc menu on it. A stored save never sees it.
  - **UI language change reloads the app** (Esc menu: on Enter; screen: if it differs from the boot language); `lang` is a boot constant set in `main.ts`, no reactive catalog.
  - **Names:** `displayName(kind, key)` (`lib/names.svelte.ts`) from the loaded locale's names files; fallback the Spanish key / `categories.json` / `bundles.json` name.
  - **Seen across locales:** ids are shared, so a switch never repeats a question before unseen ones run out; supply, outlook and low-supply warning run on the loaded locale's pool.
- Consequences: only `es` ships today, so no rows and no screen; `en`, `de`, `es-ES` catalogs (plans 24, 69) and translated pools (plan 66) turn them on with no code change. Steam client language: milestone 10, `guessTag()`.
- Supersedes / related: plan 68's earlier "no first-start language screen"; D-59, D-70, D-78, D-81, D-82; pm decisions 26, 27, 36
- **Superseded in part by D-96** (one language for UI and questions: no question-language setting or option list, no Esc menu rows; changed only on Start).

## D-87: Translations through `qgen batch --translate`
- Date: 2026-10-12
- Context: QT-2, QT-3 (plan 15b); plan 66 (tasks 437–441, 464); files per locale D-81; prompts and markets: decision 35: Translation prompts and markets per locale; thresholds and order: decision 45: Health thresholds and selection order for qgen batch --translate runs.
- Decision:
  - **Command:** `qgen batch --translate <locale>` (`en`, `de`), one more exception to D-36's "no arguments", used only when the user names a language; `--bundle <id>` translates that bundle's sources instead of `base`'s (decision 110, plan 98 task 829), export to the pack's `app/data/bundles/<id>/pool.<locale>.json` (decision 112).
  - **Run:** `tr-<locale>-<n>`, also the translations' `batch`; an unfinished run of that locale is resumed. `work/tr-<locale>-<n>/run.json` `{mode: "translate", locale, bundle, ids, stale, started, done}`; one run sequence per locale across bundles; an unfinished run of another bundle stops the command.
  - **Selection (code):** approved, translatable sources of the run's bundle (`base` by default) without an approved non-stale translation, not rejected in the locale. Stale translations first (old review kept as `previous`). Then one source at a time from the subcategory with the fewest approved translations (picks count; ties in `categories.json` order); within it the source whose level has the most locale deficit per pick (D-84), van der Corput order over difficulty as tie-break.
  - **Size:** `TRANSLATE_SIZE` 300 sources; the locale's first run (no `questions.<locale>.json` yet) is the pilot, `TRANSLATE_PILOT` 50 (QT-5).
  - **Steps:** translate (opus, chunks of 15 per subcategory, `prompts/translate.md` + `locale-<l>.md`) → rate → factcheck (changed numbers, units, dates, records only) → merge → review 1 → fix → review 2 → record → audit → export → validate → report `authoring/reports/tr-<locale>-<n>.md`. No concepts, draft, media search or sheets; media stays the source's.
  - **Not travelling:** the translator says so instead of forcing it → no entry, `work/<run>/not-travelling.json`; review 1 confirms → `translatable: false` on the source (`questions.json`), else translated again next run.
  - **Stop (exit 2, D-55):** after the pilot `tr-<locale>-1` always, and after a run failing a threshold that applies (decision 45), until `qgen health ack <run> "<note>"`.
  - **Text in media** is never a problem (decision 35): no `media_text` flag, no media problem for it.
- Consequences: RUNBOOK step 2 names `--translate`; QC adds a native-speaker spot check for `tr-*` runs (review view per locale: plan 67). Commit lines: the locale file, `pool.<locale>.json`, the report, `questions.json` when `translatable` changed.
- Supersedes / related: D-36 (amends), D-55, D-56, D-79, D-81, D-84; plan 66; pm decisions 35, 45, 110, 112

## D-88: Gamemaster mode: configure screen fields and gamemaster menu
- Date: 2026-10-12
- Context: MD-11, MD-12 (plan 13 "Gamemaster mode"); plan 59; decision 33: Configure game screen: which fields?; decision 34: Gamemaster menu: which cheats?
- Decision:
  - **Configure screen** (plan 29's Choice screen in gamemaster mode; opens on the player's last game's settings, else the defaults below):
    - Difficulty: an age group, or «Custom»: start and end difficulty 1–15, end ≥ start, levels ramp evenly.
    - Bundles: a shared bundle selector (also in the menu and elsewhere): the locale's bundles, base bundles apart, exactly one base bundle (D-85). Default: the locale's first base bundle, non-base off.
    - Jokers: one row per joker, 0–99 or ∞; default the standard set (`STANDARD_JOKERS`); no presets.
    - Allow video questions, allow audio questions: on/off, default on; no general media switch.
    - Number of levels 1–20, default 12; the Tower adapts. No start level.
    - Cards per level 0–4, default 4; 0 = no choice, a question at once.
  - **Old games unchanged:** each field optional in `settings`, missing = before (12 levels, 4 cards, media allowed, unlimited jokers in gamemaster mode, D-85's default bundles); new defaults only on the configure screen.
  - **Menu in two parts:** general (every mode): continue, «Reportar pregunta» / «Preguntas reportadas», sound, languages (D-86), fullscreen, restart, quit (desktop). Gamemaster cheats (gamemaster mode only, apart): «Saltar pregunta», «Bloquear pregunta», undo, «Gestionar comodines», «Cambiar pregunta», «Saltar a nivel», difficulty and bundles mid-game. Not: reveal the answer.
  - **Cheats in the engine:** one action each, refused `gamemaster_only` (409) outside gamemaster mode.
- Consequences: spec in plan 13 "Gamemaster mode"; MD-11 (task 391), MD-12 (task 392). `LEVELS` and `PER_LEVEL` become per game. MD-10 covered by the action layer (IN-1..IN-5).
- Supersedes / related: D-85 (default bundles, configure screen only), D-74, D-82, D-86; MD-4; pm decisions 33, 34

## D-89: English joker names
- Date: 2026-10-12
- Context: LUI-3 (pm plan 24); task 102's candidates; pm decisions 40–44
- Decision:
  - `hint` «Soplo» → Hint; `skip` «Paso» → Pass & Purge; `easier` «Bájale» → Fairy; `category` «Cambiazo» → Ms Picky; `snipe` «Francotirador» → Trick Shot.
  - Keys stay `S P F T X` until LUI-4.
  - Skip dialog: the plain option is its own key `joker.skip.pass` («Just pass»), since the name says purge.
- Consequences: `app/client/src/locales/en.ts` (names, hint notes «Hint 1/2/3», «no … left» errors, category title, purge line); `joker.skip.pass` in `es.ts` («Paso», no visible change) and `Question.svelte`. Draft, native check in LUI-5.
- Supersedes / related: D-78; LUI-3, LUI-4, LUI-5; pm decisions 40, 41, 42, 43, 44

## D-90: The game server after PORT-8: static files, cached media, `/api/save`
- Date: 2026-10-12
- Context: PORT-8 (plan 51), the last part of milestone 2. The family test night on the TS engine went fine (pm decision 25), so the Python referee, kept as rollback until then, goes. D-59 set the target: static files plus `/api/save`.
- Decision:
  - **Routes of `trivia`** (`app/server/main.py`): `GET /` + built client, `GET /data/…` (read-only `app/data/`), `GET /media?url=…`, `GET/PUT /api/save`. Anything else under `/api/`: 404 `not_found`. Gone: `/api/game*`, `/api/players*`, `/api/flags`, `/api/categories`.
  - **`/media` is a cache lookup, never a download:** only URLs from `pool.json`; file from `TRIVIA_MEDIA` or `404 media_missing`. Not a `/media/<hash>.<ext>` path: the client would need SHA-1 (`crypto.subtle` is missing on plain-http LAN addresses) or a pool format change. Start line: `media: N of M pool files missing from the cache; run trivia-media sync --status approved`.
  - **Download code leaves `app/`:** `http_get`, `cached`, rate limits, user agent, Commons token in `authoring/tools/download.py`; `app/server/media_cache.py` keeps `cache_path`, `picked`, `pool_urls`. The authoring server overrides `send_media` to download on a miss.
  - **`categories.py` → `authoring/tools/categories.py`:** only authoring uses it; the game reads categories as static files.
  - **Deleted:** `app/server/game.py`, `selection.py` (D-60: supply via `authoring/tools/supply.ts` under Node), `flags.py` (flags live in `SaveData`; `save_file.py` reads only `game.json`, no SQLite/`flags.json` fallback).
  - **Fixture recorder deleted** (`authoring/tools/record_fixtures.py`); fixtures in `app/client/src/engine/fixtures/` are frozen and still replay (`npm test`).
  - **`save.migrate()` stays** with its own schema upgrade `_upgrade(con)` (copied from `game.init`, run on a temp copy only): an old install may still start with only `game.sqlite`.
  - **Packaged `.#app`** needs `TRIVIA_MEDIA` pointing at a synced cache (its `$XDG_DATA_HOME/trivia/media` starts empty); accepted for a pre-Steam test build, the Steam build bundles media (plan 34).
- Consequences: `trivia-media sync --status approved` before game night is required, not optional. `qgen report` and the authoring start page need Node. `state/game.sqlite` and `state/flags.json` stay on disk as backups; only `migrate()` reads them. D-4's SQLite state is history.
- Supersedes / related: D-4 (SQLite state), D-17 (download on miss in the game), D-25, D-35, D-47, D-59, D-60, D-67, D-69; plan 51; pm decisions 4, 5, 25

## D-91: Shortcut keys per UI language; German joker names
- Date: 2026-10-12
- Context: LUI-4, LUI-5 (pm plan 69); pm decisions 53–59
- Decision:
  - **Keys per catalog** (pm decision 53): `joker.<id>.key`, `flag.key`, `screen.question.replayKey`, `screen.start.newKey`, `mode.*Key`, `customize.openKey`; mnemonic for the name. `toIntent` matches `e.key`, so letters work on QWERTZ/AZERTY.
  - **Rule** (`npm run check:literals -w app/client`): single letter, unique per screen with `flag.key`, not `A`–`D` on the Question screen, no digit.
  - **Joker keys**: `es`/`es-ES` `S P F T X` (unchanged), `en` Hint `H`, Pass & Purge `P`, Fairy `F`, Ms Picky `K`, Trick Shot `T`; `de` see below.
  - **German joker names** (pm decisions 54–58): Zaunpfahl `Z`, Näxt `N`, Gang runter `G`, Wunschzeit `W`, Finte `F`.
  - **Neutral `es`** (pm decision 59): «¡Qué maravilla!» for «¡Qué berraquera!», «Presiona otra vez» for «Pulsa otra vez» (`es-ES` keeps «Pulsa»).
- Consequences: `app/client/src/locales/{es,es-ES,en,de}.ts`; D-89's "keys stay `S P F T X`" no longer holds for `en`. `picker.letters` per catalog (`de` + `ÄÖÜß`, `en` + `-'`), read by `LetterPicker.svelte`.
- Supersedes / related: D-6, D-78, D-89; LUI-4, LUI-5; pm decisions 53, 54, 55, 56, 57, 58, 59

## D-92: Steam overlay in the Electron shell: Windows only
- Date: 2026-10-13
- Context: SW-8, pm plan 85 task 647. steamworks-ffi-node 0.11.3 `addElectronSteamOverlay` copies every frame (`beginFrameSubscription` + `getBitmap`) into a native OpenGL window Steam hooks; experimental (D-63).
- Spike (Linux, NixOS, COSMIC Wayland → XWayland via `--ozone-platform=x11`, Intel Iris Xe/Mesa 26, Electron 43.7.7, Steam 480):
  - Subscribing before the page load gets no frames at all; after `did-finish-load` frames arrive.
  - With the native window attached the main process freezes within seconds (window stops painting, timers stop, SIGTERM ignored); windowed and fullscreen alike.
  - Gameoverlayrenderer preloaded outside a Steam launch: Electron dies at start. Shift+Tab, video and audio not reachable on Linux.
  - Frame copy rate in a bare test page: far below 60 fps (≈ 0.2–9 fps), so even a working Linux path would lag.
- Decision:
  - **Overlay on Windows only** (`process.platform === "win32"`), attached after `did-finish-load`, only while Steam is up; `steam.overlay.enabled()` = attached and `ISteamUtils::IsOverlayEnabled`.
  - **Linux without overlay** (no native window, no X11 switch); the Deck plays the Windows build via Proton when the overlay is wanted there (D-63, SW-12); Deck check in masterplan 10 part 10.
  - Nothing pauses on overlay open (no timer outside `timed`).
  - Windows result pending a developer check (pm decision); if it fails there too: no overlay anywhere, achievements still show Steam's own toast.
- Consequences: `app/desktop/main.mjs`; without Steam nothing changes.
- Supersedes / related: D-63, D-71; SW-8, SW-12; pm decision 28, plan 85

## D-93: Steam uploads: SteamCMD, three depots, `beta` only
- Date: 2026-10-13
- Context: SW-10, SW-6, pm plan 89 (task 676); pm decision 84
- Decision:
  - **SteamCMD from nixpkgs** (`steamcmd`, FHS via `steam-run`; unfree: `steamcmd`, `steam-unwrapped`), dev shell, x86_64-linux only; `steamcmd +quit` runs on NixOS, so no SDK ContentBuilder fallback.
  - **Own HOME for SteamCMD:** the dev shell's `steamcmd` wraps nixpkgs' with `HOME=${TRIVIA_STEAMCMD_HOME:-$XDG_DATA_HOME/trivia/steamcmd}`; nixpkgs' default `~/.local/share/Steam` is the Steam client's root, whose `linux32/` SteamCMD would overwrite. Self-update, login cache, logs live there, never in the repo.
  - **Three depots, one install folder:** `windows` (`release/win-unpacked/`), `linux` (`release/linux-unpacked/`), both minus `resources/media/*`; `content` (`app/desktop/build/media/`, `DepotPath` `resources/media`), shared by both OSes. All exclude `*.pdb`, `steam_appid.txt`. No language/bundle depots.
  - **Unpacked folders** from electron-builder's `dir` target (`trivia-desktop-build --dir`), archives stay for hand-copied builds.
  - **Files in git** (`authoring/steam/`, never ships): `steam.json` (IDs, `null` until SW-7), `app_build.vdf.in`, `depot_build.vdf.in`, `steam.py` (`trivia-steam`), later `release_check`, `smoke.mjs`. Generated VDFs (`work/steam/<tag>/vdf/`), `BuildOutput` (`work/steam/<tag>/output`), logs, the release-check report: `work/steam/<tag>/`, gitignored.
  - **No secrets in files:** account via `TRIVIA_STEAM_ACCOUNT` or a prompt; password, Steam Guard only typed into SteamCMD; beta password only in Steamworks.
  - **`SetLive` `beta` only**, fixed in the template; `default` never from the repo (Steamworks web UI, S6).
  - **`Desc`:** `<tag> <short sha>` (+ `skipped: <steps>` from the release check).
  - **Release check:** every automated step fails it; `--skip <step>` (repeatable) shows in the report and `Desc`; manual rows interactive or `--manual <file>`, a "no" fails.
  - **Clean tagged commit** for an upload: empty `git status --porcelain`, `v<version>` on HEAD; never creates/pushes tags; `--preview` (`Preview 1`) and `--dry-run` skip the tag gate.
- Consequences: `flake.nix` (`steamcmd`, `trivia-steam`, unfree predicate); `trivia-steam vdf` renders the VDFs with absolute paths; SteamCMD parses them (`+run_app_build -preview` without login stops at "Not logged on"). Task 680: `trivia-steam upload --branch beta` applies the gates; `--checked` only accepts a passing `release-check.json` of HEAD on a clean tree; `--dry-run` uses placeholder IDs 480/481–483 while `steam.json` is null; tracked files changed by the release check refuse the upload.
- Supersedes / related: D-59, D-63, D-73; SW-6, SW-10; pm decisions 14, 84; plans 56, 89

## D-94: Packs as optional file sets (pool per bundle)
- Date: 2026-10-13
- Context: pm decision 66 (bundles ship as free DLC, optional install); plan 98 task 751. One `pool.json` with every bundle and one media folder: a DLC depot couldn't carry a pack.
- Decision:
  - **Pack** = every bundle besides `base`; its files all live in `app/data/bundles/<id>/`: `categories.json`, `names.<locale>.json`, and now `pool.json` / `pool.<locale>.json`.
  - **`qgen export`** splits per bundle: `app/data/pool[.<locale>].json` keeps only `base`'s questions (always written); a pack's file only when it has questions in that locale; a pack file that would no longer be written is deleted (`qgen validate`: error). Each file has its own `hash` (D-92); the game's pool hash (Credits) stays `base`'s.
  - **Loader** (`lib/data.ts`, `withPacks` in `engine/pool.ts`; also `sim/load.ts`, store screenshots): `base`'s pool plus each pack offered in the locale whose file exists. Missing file: the locale leaves the pack's `languages`, so it isn't offered and a stored choice naming it reads as the defaults (D-85, pm decision 38), never written back; no error.
  - **Media:** `/media` (Python server, desktop `resolve.mjs`) serves URLs of every pool file present. `stage-media.mjs` still stages every pack's media into `build/media/` and writes `build/pack-media.json` (`{<id>: [cache file names]}`): media only that pack uses, for its DLC depot; media shared with `base` or another pack stay in the content depot.
  - **Browser game** (`trivia`, `nix build .#app`) and desktop builds ship every pack (`app/data/` copied whole).
  - **Release tools:** release check lists a pack's hash as `<locale>/<id>`; patch notes and `released_ids` merge pack files into their locale.
- Consequences: removing `app/data/bundles/colombia/pool.json` → es offers only `base`, the family's save plays on; restoring it → offered again. DLC depots (plan 89, task 748): `resources/data/bundles/<id>/` + `pack-media.json`'s files under `resources/media/`.
- Supersedes / related: D-35, D-39, D-43, D-81, D-85, D-92, D-93; pm decisions 38, 66; plans 89, 98

## D-95: DLC depots for packs
- Date: 2026-10-13
- Context: pm decision 66 (bundles ship as free DLC, optional install), D-94 (pack = `app/data/bundles/<id>/` + `build/pack-media.json`), D-93 (three depots); plan 89 task 748. Launching packs: `colombia` (pm decision 110).
- Decision:
  - **One depot per pack**, listed in `authoring/steam/steam.json` `dlc: {<id>: {appid, depot}}` (`null` until SW-7); uploaded with the base app's build VDF (DLC depots belong to the base app; the DLC App ID isn't in any VDF, only kept for the record).
  - **Staged folder** `app/desktop/build/dlc/<id>/` (gitignored, hard links), written by `trivia-steam stage`: `resources/data/bundles/<id>/` from `linux-unpacked` plus `pack-media.json`'s files under `resources/media/`; depot path `.`.
  - **Exclusions:** OS depots `resources/data/bundles/<id>/*`; `content` each pack-only media file name.
  - **Checks:** `trivia-steam stage` fails unless packs in the build = `pack-media.json` = `steam.json` `dlc` (every shipped bundle is DLC), and OS depot + content + DLC depots = each archive. `--depots W,L,C,<packs in steam.json order>`; `--dry-run` placeholders 480 / 481… per depot.
  - **Smoke game:** with packs in the build, a second run on a hard-link copy without the packs' data and media; each run checks gamemaster mode's bundle selector offers exactly the packs with a pool file in the questions locale. Shell started with `--lang=es` (the packs' language).
  - The game itself never asks Steam about DLC (D-94: files present = pack offered).
- Consequences: a new pack needs a `steam.json` `dlc` entry before `trivia-steam stage` passes; a pack's media shared with `base` or another pack stays in `content`.
- Supersedes / related: D-93, D-94; pm decisions 66, 109, 110, 112; plans 89, 98

## D-96: One language for UI and questions
- Date: 2026-10-14
- Context: item 7 of pm decision 50 (Play-test of age groups and bundles); plan 126 (tasks 1019, 1020); pm decisions 156 (One language for UI and questions), 157 (Start's language button: globe and endonym, key per catalog, pad Y). Bundles depend on the language, so it can't change once bundles are chosen.
- Decision:
  - **One setting:** the game's language = UI language = question language. `SaveData.language` is one tag; an old `{ui, questions}` save reads as `ui` (`parseSave`), missing = `es`; no save-version bump. Options = `UI_LANGS`.
  - **First start:** `Language.svelte` picks it for a fresh save (default `guessTag()`: Steam's language, else the browser's), as before.
  - **Afterwards only on Start:** a button top right under ☰: globe + endonym (no national flag), key per catalog (`I` es/es-ES, `L` en, `S` de), pad Y; opens the same picker with «Atrás». A different UI language reloads the app. Not on later screens.
  - **No language rows in the Esc menu**, in any mode.
  - **Fixed in a game:** a game keeps `GameRow.locale`; the language can't change once bundles are chosen.
  - **Question locale** (`localeOf` / `nextLocale` in `lib/engine.ts`): the language if `pool.<language>.json` exists and its default bundles' supply passes, else `es` (`pool.json`, es bundles via `bundlesFor`). Used for `loadEngineData`, `newGame`'s locale (from the loaded data) and the bundles offered. All UI languages stay selectable; en, de, es-ES and mod UI languages play the Spanish questions until their translation ships.
  - **POLYGLOT** counts `GameRow.locale`: a de UI on Spanish questions is an `es` game.
- Consequences: «Idioma de las preguntas» and its strings gone; the play-test's en/de question language check is replaced by this (plan 30).
- Supersedes / related: D-86 in part (two settings, the question-language option list, the Esc menu rows, first start setting both); D-70, D-78, D-82, D-85; pm decisions 36, 50, 156, 157

## D-97: Bundle selection in every mode
- Date: 2026-10-14
- Context: problem 5 of pm decision 50 (Play-test of age groups and bundles); plan 125, task 1017; pm decision 158.
- Decision:
  - **Every mode** shows the shared `BundleSelector` on the Choice screen: «Solo o en grupo» too, with the same letter keys (`keyOf`), mouse and pad.
  - **Not customization:** its own section like the age group; not in «Personalizar partida», not counted in `customized`; in gamemaster mode below the configure fields.
  - **Preset** in both modes: `playerChoice`, the player's newest game's bundles, else the locale's first base bundle, non-base off (pm decision 33).
- Consequences: a fresh solo game plays base only (was: every offered bundle); a non-base mod bundle is off by default in solo too.
- Supersedes / related: pm decision 51 (solo plays the defaults); pm decisions 33, 38 in part (fresh default on the configure screen only); D-85, D-88

## D-98: Paid one-time purchase, $9.99; free DLC packs; a person holds the Steamworks account
- Date: 2026-10-14
- Context: OQ-33, plan 39 (task 193 prep, task 194); pm decisions 66 (Price model (OQ-33)), 67 (Steamworks account holder (OQ-33)). Not legal or tax advice.
- Decision:
  - **Price:** paid one-time purchase, base price $9.99 for now; final check at PUB-11. Valve's recommended regional matrix; a launch discount. No in-game store, no IAP.
  - **Packs:** every bundle besides `base` ships as **free DLC** (own store entry, optional install; D-94, D-95), never paid: paid packs would push players to their own AI-made questions instead. No paid DLC planned. Player-made bundles: Steam Workshop and modding (own milestone).
  - **Account holder:** the developer as a private person, after a tax advisor check (advisor questions: pm decision 67's body); W-8BEN; store Developer/Publisher as a free-text label.
  - **Switch to a company** (app transfer) if revenue passes the advisor's threshold, a partner joins, or the EU DSA trader address can't be kept private.
- Consequences:
  - OQ-35 (plan 40): a paid game with a public pool → anyone can copy the content; the store sells the game, not the questions.
  - OQ-45 (plan 42): paid → "commercial" under Freesound API / CC NC terms; CC BY credits stay required.
  - $100 app credit recouped at $1,000 gross; free DLC costs no app credit.
  - Professional checks still owed before PUB-6 signup: tax advisor (business registration, W-8BEN treaty rate, VAT/small-business threshold, income tax, DSA address); re-check the ≈ figures (regional matrix, discount rules, comparable prices) in Steamworks at PUB-11.
- Supersedes / related: D-50, D-94, D-95; OQ-33; PUB-6, PUB-11; pm decisions 66, 67; plans 39, 40, 42

## D-99: Regional packs: 2000 approved each, region's language + en, bundle-scoped taxonomy
- Date: 2026-10-14
- Context: RG-5 (15c) with OQ-46 folded in; pm decision 110 (Regional packs at launch (RG-5, OQ-46)), plan 98 (tasks 749, 750). Packs ship as free DLC (pm decision 66, D-98).
- Decision:
  - **Target:** every regional bundle 2000 approved questions (`targets.json` entry per bundle, plan 98 task 828). Amends pm decision 37 / D-84's "packs have no target" and D-53's "a bundle without an entry has no targets" for regional bundles.
  - **Languages:** the region's language + en (`colombia`: es + en); en via `qgen batch --translate en --bundle <id>` (plan 98 task 829).
  - **Default:** off on the configure screen in every locale (pm decision 33, D-97 unchanged); the family's save keeps base + `colombia` (D-85, D-59).
  - **Free DLC**, optional install (D-94, D-95, D-98).
  - **Bundle-scoped taxonomy:** a category or subcategory is bundle + name; names may repeat verbatim across bundles («Historia» in `base` and in `colombia`), still separate entries; unique within a bundle. The 19 `colombia` questions on `base` subcategories move to `colombia`'s own (plan 98 tasks 826, 827).
  - **Pilot `colombia`:** 102 → 2000 via `qgen batch --bundle colombia`, then its en translation; effort measured: $ per approved (`qgen report --cost`) and the developer's review time per 100 (review tool timestamps, plan 98 task 830).
  - **More packs** (candidates `mexico`, `argentina`): a new pm decision "More regional bundles at launch?" after the pilot, with its numbers (plan 84).
  - **Launch doesn't wait:** it ships what `colombia` has then; updates bring the rest.
- Consequences: `qgen report --simulate` defaults to the locale's default game (`base` for every locale); `--bundles` for packs. Plan 98 builds the rest (taxonomy, `colombia` list, target, `--translate --bundle`, effort report).
- Supersedes / related: D-43 (uniqueness across bundles), D-49, D-53, D-84 (amends); D-39, D-85, D-94, D-95, D-97, D-98; OQ-46; RG-5; pm decisions 33, 37, 66, 110; plans 84, 98

## D-100: Subcategory keys: bundle + name in code
- Date: 2026-10-14
- Context: D-99 makes a category or subcategory bundle + name; code looked subcategories up by name alone (D-43). Plan 98 task 826.
- Decision:
  - **Python:** a subcategory is `(bundle, name)` (`categories.key(q)`, `broad_of()`, `category_of(bundle, sub)`); concept lists, drafts, saturation, reports and `validate` take the bundle; `validate` checks uniqueness within each bundle only.
  - **One-string key** (engine, names, patch notes, `--simulate` output): `subKey` / `categories.sub_key`: `base`'s bare name or slug, another bundle's `<bundle>/<name>`. Saves keep their keys: a `base` subcategory's key is unchanged, so purged subcategories, `swapped_to` and `notified_exhausted` of existing saves stay valid without a save migration.
  - **Names:** each names file keys its own bundle's slugs and Spanish names; merged by key (`mergeNames`, `load_names`).
  - **Joker view:** «Cambiazo» categories and subcategories carry `key`; the client sends the subcategory's key. Frozen engine fixtures (plan 51) replay through a normalizer in `game.test.ts` (bare names, no `key`).
  - **Work files** of a non-`base` subcategory (`work/concepts/`, translation chunks) are prefixed `<bundle>--`.
- Consequences: Until plan 98 task 827, the 19 `colombia` questions on `base` subcategories pass `validate` (D-49's other direction) but have no broad category in play or reports (`None`); a `colombia` name already in a save's `notified_exhausted` is pruned and may be shown once more. Mods: `taxonomy_clash` goes in task 995.
- Supersedes / related: D-43 (amends: lookups by name alone), D-49, D-81, D-99; pm decision 110; plan 98

## D-101: Regional bundle targets in `targets.json`
- Date: 2026-10-14
- Context: D-99 gives every regional bundle 2000 approved; `targets.json` had `base` only (D-53). Plan 98 task 828.
- Decision:
  - **Entry per regional bundle:** `{"total": 2000, "difficulty": …}`, D-53's `base` mix scaled to 2000 (largest remainder, `targets.scaled`); `colombia`: 100, 140, 180 ×6, 132 ×3, 92 ×2, 50 ×2.
  - **Required:** `qgen validate` errors on a `kind: region` bundle without an entry; `qgen bundle new --kind region` writes it. Theme bundles: no target.
  - **Per locale:** the same numbers for each of the bundle's languages (`deficits(..., locale)`), as pm decision 37 for `base`.
  - **Read by** `--bundle` drafting (`target_weights`, the subcategory ranking) and `qgen report --bundle <id> [--locale L]`. No `es` source shortfall for packs (`base` only, D-84).
- Consequences: `qgen report --bundle colombia` shows progress vs. 2000; `qgen batch --bundle colombia` aims at its deficits.
- Supersedes / related: D-53 (amends: a regional bundle always has an entry), D-54, D-84, D-99; pm decisions 37, 110; plan 98

## D-102: Code MIT; questions all rights reserved; whole repo stays public
- Date: 2026-10-14
- Context: OQ-35, plan 40 (task 198 prep, task 199); pm decisions 107 (Licence (OQ-35)), 108 (Is release content public (OQ-35)). Paid game, packs as free DLC (D-98). Not legal advice.
- Decision:
  - **Code:** MIT, in `LICENSE` at the repo root; covers `modding/` and its examples too (pm decision 134).
  - **Questions:** all rights reserved, in `LICENSE-content.md`: `authoring/data/`, `app/data/` (pool, bundles, translations); personal, non-commercial play from the repo allowed.
  - **Never covered** by either: media (own licence per file, PUB-2), fonts (OFL), UI audio (`CREDITS.md`), npm dependencies.
  - **Public:** the whole repo, release content included (new batches, translations, packs); D-17 stays: the licence, not a private repo, protects the pool.
- Consequences:
  - Files: `LICENSE`, `LICENSE-content.md`, README "License", `directory.md`; both copied into `result/` and the desktop builds; credits "Game" section (PUB-4, PUB-5; plan 40 task 3).
  - No build change; no private content repo, no backlog row.
  - Commits public before `LICENSE` stay unlicensed: copies exist, no rights granted.
  - Professional checks still owed (lawyer, the developer's country + US): is the AI-drafted, human-reviewed pool protectable (copyright, database right); wording of "reserved, personal play allowed" next to MIT code; implied licence for forks of unlicensed commits; Anthropic's terms for commercial use of outputs (PUB-10).
- Supersedes / related: D-17 (confirms), D-98; OQ-35; PUB-4, PUB-10; pm decisions 66, 107, 108, 134; plan 40

## D-103: Freesound out before release; its 2 picks re-picked from Commons
- Date: 2026-10-14
- Context: OQ-45 (Freesound), plan 42 (task 204 prep, task 205); pm decision 82 (Freesound API for a paid Steam release (OQ-45): replace, ask, or family only?). Paid release (D-98) = commercial use of the API, which needs a UPF licence; authoring-only use is a grey zone. 2 Freesound picks (q-0752 mosquito, q-1016 turkey; both CC0, approved) of 17 audio picks.
- Decision:
  - Replace the 2 Freesound picks with allowlisted sources (Commons first) through the review tool's search modal (D-36), before release.
  - Drop `freesound` from `providers.ORDER["audio"]`: audio is Commons only.
  - No contact with Freesound/UPF.
- Consequences:
  - Follow-up task in plan 42: re-pick both slots, remove Freesound from the order, `qgen validate` passes.
  - `providers/freesound.py` may stay as code but isn't asked; no SW-9 exclusion rule needed.
  - Slightly fewer everyday sounds in future batches.
- Supersedes / related: D-36, D-45, D-98; OQ-45 (Freesound); MP-6; pm decisions 66, 82; plan 42
