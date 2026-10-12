-- pm database. Change it with pm; after a hand edit run `pm validate`.
PRAGMA user_version = 11;

CREATE TABLE milestone (
    id             INTEGER PRIMARY KEY,
    subject        TEXT NOT NULL CHECK (trim(subject) <> ''),
    status         TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'implemented')),
    body           TEXT NOT NULL DEFAULT '',               -- Markdown
    created_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    implemented_at TEXT,
    CONSTRAINT "implemented_at is set exactly when implemented" CHECK ((status = 'implemented') = (implemented_at IS NOT NULL))
) STRICT;

CREATE TABLE plan (
    id              INTEGER PRIMARY KEY,
    milestone_id    INTEGER NOT NULL REFERENCES milestone (id),
    subject         TEXT NOT NULL CHECK (trim(subject) <> ''),
    priority        INTEGER,                               -- NULL: 0
    body            TEXT NOT NULL CONSTRAINT "a plan needs a body" CHECK (trim(body) <> ''),
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    created_by_task INTEGER REFERENCES task (id)
) STRICT;

CREATE TABLE task (
    id              INTEGER PRIMARY KEY,
    plan_id         INTEGER NOT NULL REFERENCES plan (id),
    subject         TEXT NOT NULL CHECK (trim(subject) <> ''),
    kind            TEXT NOT NULL DEFAULT 'work' CHECK (kind IN ('work', 'plan', 'masterplan', 'split', 'cleanup')),
    status          TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'done', 'dropped')),
    priority        INTEGER,                               -- NULL: the plan's
    note            TEXT,                                  -- done: date, files; dropped: reason
    body            TEXT NOT NULL DEFAULT '',              -- Markdown
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    retired_at      TEXT,                                  -- done or dropped
    created_by_task INTEGER REFERENCES task (id),
    CONSTRAINT "an open task needs a body" CHECK (status <> 'open' OR trim(body) <> ''),
    CONSTRAINT "retired_at is set exactly when done or dropped" CHECK ((status = 'open') = (retired_at IS NULL))
) STRICT;

CREATE TABLE decision (
    id              INTEGER PRIMARY KEY,
    subject         TEXT NOT NULL CHECK (trim(subject) <> ''),
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'answered', 'irrelevant')),
    options         TEXT NOT NULL DEFAULT '[]' CHECK (json_type(options) = 'array'),  -- recommended first
    body            TEXT NOT NULL DEFAULT '',
    answer          TEXT,
    reason          TEXT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    closed_at       TEXT,
    created_by_task INTEGER REFERENCES task (id),
    signoff         TEXT CHECK (signoff IN ('masterplan', 'plan', 'task-queue')),  -- made by pm; NULL: a question
    CONSTRAINT "a sign-off is only approved"
    CHECK (signoff IS NULL OR status <> 'irrelevant' AND coalesce(answer, 'approve') = 'approve'),
    CONSTRAINT "pending: no answer, reason or closed_at; answered: answer and closed_at; irrelevant: reason and closed_at"
    CHECK (status = 'pending' AND answer IS NULL AND reason IS NULL AND closed_at IS NULL
           OR status = 'answered' AND answer IS NOT NULL AND closed_at IS NOT NULL
           OR status = 'irrelevant' AND reason IS NOT NULL AND closed_at IS NOT NULL)
) STRICT;

CREATE TABLE run (                                         -- one worker run of `pm run`
    id                    INTEGER PRIMARY KEY,
    task_id               INTEGER NOT NULL REFERENCES task (id),
    started_at            TEXT NOT NULL,
    ended_at              TEXT,                            -- NULL: running
    result                TEXT NOT NULL CHECK (result IN ('running', 'done', 'blocked', 'failed', 'limit')),
    reason                TEXT,                            -- failed: why; limit: the message
    exit_code             INTEGER,
    base_commit           TEXT,                            -- HEAD when the run started
    model                 TEXT,                            -- from here on: the worker's JSON output, if any
    session_id            TEXT,
    turns                 INTEGER,
    input_tokens          INTEGER,
    output_tokens         INTEGER,
    cache_read_tokens     INTEGER,
    cache_creation_tokens INTEGER,
    cost_usd              REAL,
    pid                   INTEGER,                         -- the `pm run` process
    CONSTRAINT "ended_at is set exactly when not running" CHECK ((result = 'running') = (ended_at IS NULL))
) STRICT;

CREATE TABLE task_decision (                               -- the task waits while the decision is pending
    task_id     INTEGER NOT NULL REFERENCES task (id),
    decision_id INTEGER NOT NULL REFERENCES decision (id),
    PRIMARY KEY (task_id, decision_id)
) STRICT;

CREATE INDEX plan_milestone ON plan (milestone_id);

CREATE INDEX task_plan ON task (plan_id);

CREATE INDEX task_decision_decision ON task_decision (decision_id);

CREATE INDEX run_task ON run (task_id);

CREATE UNIQUE INDEX run_running ON run (result) WHERE result = 'running';

CREATE VIEW queue AS
SELECT coalesce(t.priority, p.priority, 0) AS priority, t.id AS task_id, t.subject, t.kind
FROM task t
JOIN plan p ON p.id = t.plan_id
JOIN milestone m ON m.id = p.milestone_id
WHERE m.status = 'open' AND t.status = 'open'
  AND NOT EXISTS (SELECT 1 FROM task_decision td JOIN decision d ON d.id = td.decision_id
                  WHERE td.task_id = t.id AND d.status = 'pending')
ORDER BY priority DESC, m.id, p.id, t.id;

INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (1, 'Enough content for game nights', 'open', 'we want 5000 questions in the base bundle. note the current difficulty scale (i think from 1 to 15). it''s okay to have fewer questions for higher difficulties, but currently there are way too few questions at high difficulties.

 `qgen batch` creates new questions, so it''s just a matter of running it a couple of times, but there might be improvements necessary along the way. E.g. we are currently assuming that our list of categories is complete. Creating more subcategories might be useful, though. Any task that runs qgen batch should be prioritized at -100. The idea is that any implementation task has higher priority and only when all tasks are blocked by pending decision new questions can be generated.

 also, we need regular quality control. typically ones after the completion of a batch.

 we should also have quality control on the process of creating questions. the typical flow: go ahead, create questions. get human feedback, gather LLM feedback. watch out if question quality deteriorates when running a new batch, e.g. too many duplicates.

 once we have 5000 questions and a good reason to assume the quality is fine, we are done with this.

 cf. those past plans for reference:

 Plan files: `plans/02-question-pool.md`, `plans/06-images.md`, `plans/07-question-generation.md`, `plans/20-pipeline-efficiency.md`, `plans/21-age-groups.md`, `plans/23-media-providers.md`.', '2026-10-11T20:08:18Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (2, 'Game engine in TypeScript', 'open', 'The game referee moves from Python (`app/server/game.py`, `selection.py`) to `app/client/src/engine/` with the same rules and the family''s saves kept. The game then runs without Python, which the Steam desktop shell needs (S3).

## Outcome
- Scenario recorder for the Python referee; fixtures committed (PORT-1).
- `engine/selection.ts` and `engine/game.ts` (state machine, players, burning, jokers, undo), fixture-tested (PORT-2, PORT-3).
- Store interface: `ServerStore` with `GET/PUT /api/save`, `MemoryStore` (PORT-4).
- Migration `game.sqlite` → `game.json`, tested on a copy of the real save (PORT-5).
- Screens use the engine (PORT-7); `game.py` and the game routes deleted, `01-architecture.md` and AGENTS.md updated (PORT-8).

## Constraints
- Same rules as today; the family''s saves survive.
- The client holds the answer; this relaxes D-25 and needs a decision entry.
- No new dependencies beyond what Svelte/Vite already bring.

## Out of scope
- Desktop shell, controller, new game modes.

## Done when
- The family plays a test night on the TS engine.
- `trivia` serves static files plus `/api/save` only.

Plan files: `plans/12-client-engine.md`.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (3, 'UI strings in a catalog', 'open', 'Every on-screen string comes from a catalog, with no visible change. This is the groundwork for translations. Bundles (the other half of the old M9) are done in the pipeline; only the gamemaster''s check of the `colombia` proposals is left.

## Outcome
- `t()` helper and the `es` catalog; every string moved into it (LUI-1).
- Pseudo-locale for length and missing-string tests (LUI-2).
- Draft `en` catalog with English joker names (LUI-3).
- The gamemaster has checked the 84 `colombia` proposals at `/review?bundle=colombia` (D-39).

## Constraints
- No visible change in Spanish.
- No i18n library; a small hand-written helper.

## Out of scope
- Translating questions (`plans/15b-question-translation.md`), choosing launch languages (OQ-31).

## Done when
- No Spanish literals left in `app/client/src/game` outside the catalog.
- Every question has `bundle`, checked by `qgen validate`.

Plan files: `plans/15a-ui-translation.md`, `plans/22-bundles.md`.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (4, 'Media license audit', 'open', 'The full license data of every media file is known and stored, and files with unclear licenses (PD-US only, GFDL, flagged) are replaced. Needed before any public release; small and independent of the other milestones.

## Outcome
- `media.py licenses` report listing the files to replace (PUB-1).
- Full license data per media item in the pool (PUB-2).
- Problem files replaced in the review tool (PUB-3).

## Constraints
- Replacements are picked by the gamemaster in the review tool, not by an LLM.
- Media files stay a gitignored cache (D-17); only metadata lives in the pool.

## Out of scope
- Credits screen and store disclosures (Steam S3, S5).

## Done when
- `qgen validate` requires license data for approved questions.
- The audit''s replacement list is empty.

Plan files: `plans/17-publishing.md`.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (5, 'Age groups and bundles in the game', 'open', 'Before a session, players choose their age group and which bundles to play; selection uses the group''s window on the shared difficulty scale 1–15 and only the active bundles. The family''s default stays young teens with every bundle on, so nothing changes unless they opt in. Easier after the TypeScript engine, since it changes selection.

## Outcome
- Choose an age group; levels map to the group''s window; windows and per-group level weights tuned (AG-7, D-38).
- Choose bundles before a session, `base` always on; selection filters by them (BN-6, D-39).

## Constraints
- Defaults unchanged for the family.
- Every action clickable as well as on the keyboard (IN-1).

## Out of scope
- New bundles, regional packs (`plans/15c-regional-questions.md`).

## Done when
- A session can be played for each age group and with `colombia` off.
- The draft windows are tuned.

Plan files: `plans/21-age-groups.md`, `plans/22-bundles.md`.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (6, 'Screen polish leftovers', 'open', 'Two leftovers from the finished visual and sound milestones (M3, M4).

## Outcome
- The next screen''s media is preloaded before it fades in; `PLACEHOLDER(UI-7)` is gone (UI-7).
- Real sound assets replace the synthesized music loops, whooshes, pops and joker sounds; Kenney.nl CC0 packs are the next source to try (UI-10).

## Constraints
- CC0 or otherwise allowlisted licenses only (D-45); assets stay offline.

## Done when
- `grep -rn PLACEHOLDER app/client/src` is empty.
- The gamemaster approves the new sounds on the TV.

Plan files: `plans/04-ui-tv-display.md`.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (7, 'Steam S2: product definition', 'open', 'The first phase of the Steam track (D-34) is decisions, not code: what the product is before anything Steam-specific gets built. It can run alongside the other milestones.

## Outcome
Answers, each recorded in `plans/decisions.md`, to:
- OQ-29 desktop shell (Electron recommended, Tauri, or browser + local server)
- OQ-30 default mode: joker presets per difficulty, which levels count as won
- OQ-31 launch languages and Spanish variety
- OQ-32 content target per new player and language
- OQ-33 price model; who holds the Steamworks account
- OQ-35 code and content license; whether the pool stays public
- OQ-37 competitive and couch co-op format and input
- OQ-45 Freesound API use for a commercial release
Then the S2 tasks that follow from them: MD-5..MD-7, I18N-1, CT-1, PUB-4.

## Constraints
- The gamemaster answers; workers prepare options and recommendations as pm decisions.

## Out of scope
- S3–S6 (desktop build, release content, Steamworks, launch).

## Done when
- OQ-29..OQ-37 (and OQ-45) are resolved in `decisions.md`, and the later phases in `plans/11-steam.md` are updated to match.

Plan files: `plans/11-steam.md`, `plans/13-game-modes.md`, `plans/15-i18n.md`, `plans/16-content-target.md`, `plans/17-publishing.md`, `plans/18-steam-integration.md`.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (8, 'Steam S3: playable desktop build', 'open', 'A local desktop build of the game that a family can play without the gamemaster''s dev setup: desktop shell, file saves, controller, Steam Deck layout, credits. Needs the TypeScript engine (the shell loads the client without Python) and the shell decision (OQ-29).

## Outcome
- Desktop shell and builds (SW-1..SW-6, `plans/18-steam-integration.md`).
- Controller support and Deck layout (IN-2..IN-5, `plans/14-input.md`).
- Credits screen (PUB-5, `plans/17-publishing.md`).

## Constraints
- Offline, no accounts, no telemetry (AGENTS.md).
- The family game at home keeps working throughout.
- Minimal dependencies: a shell and a Steamworks binding; anything else needs a decision.

## Out of scope
- Steamworks features, store page (S5); translations (S4).

## Done when
- A local build runs on Windows, Linux and the Deck with a controller only.

Plan files: `plans/11-steam.md`, `plans/18-steam-integration.md`, `plans/14-input.md`, `plans/17-publishing.md`.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (9, 'Steam S4: content for release', 'open', 'Enough questions, in every launch language, for a stranger''s family to play many evenings. Depends on the launch languages (OQ-31) and the content target (OQ-32).

## Outcome
- Translated UI catalogs (LUI-4..LUI-6, `plans/15a-ui-translation.md`).
- Translated, re-rated and reviewed questions (QT-*, `plans/15b-question-translation.md`).
- Regional packs (RG-3..RG-5, `plans/15c-regional-questions.md`).
- The content target reached and measurable (CT-*, `plans/16-content-target.md`).

## Constraints
- Questions only through `qgen batch` (D-36); the quality bar in plan 16 applies.

## Out of scope
- Store page translations (S5).

## Done when
- `qgen report --simulate` meets the target for every launch language.

Plan files: `plans/11-steam.md`, `plans/15-i18n.md`, `plans/15a-ui-translation.md`, `plans/15b-question-translation.md`, `plans/15c-regional-questions.md`, `plans/16-content-target.md`.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (10, 'Steam S5: Steamworks and store', 'open', 'The game on Steam as a beta: Steamworks app, Cloud saves, achievements, depots, beta branch, store page and disclosures. Depends on the price model and account holder (OQ-33) and the license decision (OQ-35).

## Outcome
- Steamworks integration and depots (SW-7..SW-14, `plans/18-steam-integration.md`).
- Store page, AI disclosure, rating and the rest of publishing (PUB-6..PUB-11, `plans/17-publishing.md`).

## Constraints
- The game never phones home; Steam only distributes and syncs saves.

## Out of scope
- Public release and marketing (S6).

## Done when
- The beta branch is installed from Steam on a second machine and played by the family.

Plan files: `plans/11-steam.md`, `plans/17-publishing.md`, `plans/18-steam-integration.md`.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO milestone (id, subject, status, body, created_at, implemented_at) VALUES (11, 'Steam S6: release', 'open', 'The public release and what follows it.

## Outcome
- "Coming soon" page live (ST-3).
- Release checklist: build from a tagged commit, `qgen validate` clean, credits complete, offline test, Deck test, family sign-off (ST-4).
- Post-release: content update cadence; question reports collected by hand, no telemetry (ST-5).

## Out of scope
- Competitive mode, couch co-op, more regions and languages (later).

## Done when
- Released; content updates go out as patches.

Plan files: `plans/11-steam.md`.', '2026-10-11T21:55:09Z', NULL);

INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (1, 1, 'masterplan', 1000, 'Milestone 1 grows the `base` bundle from about 1000 to **5000 approved questions** (D-52), with clearly fewer questions at the top of the difficulty scale (1–15, D-38) but still enough of them. It also sets up quality control after every batch, and on the generation process itself, so we can tell whether quality holds as the pool grows.

**This masterplan''s own tasks are not implementation work.** Each one writes the plan for one part below (`pm plan add 1 …`). That plan''s tasks do the work.

## Where we stand (2026-10-11)
- Approved `base` questions: 1035. By difficulty: 1: 36 · 2: 67 · 3: 96 · 4: 104 · 5: 112 · 6: 147 · 7: 101 · 8: 67 · 9: 74 · 10: 57 · 11: 61 · 12: 38 · 13: 48 · 14: 19 · 15: 8.
- `focus: null` in `app/data/age-groups.json`: `draft` already aims evenly at 1–15 (D-40). But high targets come out too easy (B-6), and subcategories are picked by fewest approved, not by difficulty gaps.
- One `base` batch (D-46): about 57 subcategories × 18 slots, ~1000 drafts, ~600 merged, ~500 approved, ~$120 at list price (batch-7). 5000 approved means **about 8 more batches**. batch-8 is in progress (`work/batch-8`, commit d7fb13f).
- batch-7 needs_work reasons: mostly a giveaway hint, overlap with a pool question (q-0644/q-0957, q-0646/q-0217, q-0689/q-0279), or no usable media.
- Leftovers that belong here: PE-6, PE-13, MP-11 (batch comparisons), B-5 (dedupe misses rewordings), B-6 (high difficulties), QP-6 (media for every question), the 33 `needs_work` questions.

## Parts
Rough order: 1 and 2 first, since they steer every later batch; 3–5 alongside; 6 keeps running at the lowest priority.

1. **Targets and progress.** A target count per difficulty that adds up to 5000 and tapers at the top. Draft for the human to decide: ~420 each at 3–8, ~300 at 9–11, ~200 at 12–13, ~100 at 14–15, the rest at 1–2. Plus a progress view: approved vs. target per difficulty and per category (`qgen report` and `/stats/difficulty`). It also states what "quality is fine" means: the exit check of the milestone. Mostly backend/tooling, priority ~700.
2. **Aim batches at difficulty gaps (B-6).** `draft` draws targets weighted by what''s missing against part 1''s targets, not evenly. Also check how well targets come out (target vs. rated vs. reviewed difficulty for batch-7/8), and fix the prompts or concept `known_at` choice where 11–15 drafts land at 7–9. Changes to `qgen.py`/prompts are the gamemaster''s prompts (RUNBOOK): the plan does them as implementation tasks, never as a workaround inside a batch run. Priority ~700.
3. **More subcategories.** The category list is treated as complete, but concept lists and the per-subcategory avoid list run dry as subcategories fill up, and that drives duplicates. Find saturated subcategories (approved count, concept use, duplicate rate) and propose new `base` subcategories, especially ones that carry hard questions. New subcategories are the gamemaster''s call (RUNBOOK): propose them through a decision, then add the approved ones with their concept lists. Priority ~600.
4. **Duplicate and drift detection (B-5).** `dedupe` compares question text only. Compare answers, concepts and topics against the whole approved pool, before merge, so overlaps get dropped rather than ending up `needs_work`. Plus per-batch health metrics in `authoring/reports/<batch>.md` and across batches: drop rate, needs_work rate by reason, duplicate rate, difficulty spread vs. targets, axis/style variety, cost per approved question. Thresholds that say "stop and look before the next batch". Absorbs PE-6, PE-13, MP-11. Priority ~700.
5. **Quality control after every batch.** A fixed procedure run once a batch is committed: (a) an LLM audit with a different prompt from `review.md` on a sample of the batch (facts, ambiguity, giveaways, difficulty, house style); (b) a human spot check of a random sample in the review tool (e.g. `/review?batch=…` with a sample filter), recording agree/disagree; (c) findings turned into prompt or house-style changes before the next batch. Also the trend over batches: the human''s disagreement rate with the LLM review is the main "is quality fine" signal. Tooling priority ~650; the QC runs themselves are tasks in part 6.
6. **Batch runs.** The recurring work: finish batch-8, then one `qgen batch` per task (RUNBOOK, unchanged), each followed by part 5''s QC, until part 1''s targets are met. **Every task that runs `qgen batch` has priority -100**, so it runs only when every implementation task is done or waits for a decision. Add batch tasks one or two at a time, not all eight up front, so the results of parts 2–5 shape later batches. Media yield (no usable media → `needs_work`) is watched here; when it limits throughput, it becomes its own plan with the media plans (`06`, `23`, IMG-16/17). The last task is the exit check.

## Decisions for the human (raised by the part plans)
- Target curve per difficulty (part 1).
- What sample size and disagreement rate count as "quality is fine" (parts 1, 5).
- Which new subcategories to add (part 3).
- Whether the 33 `needs_work` questions and future ones are decided in the review tool or via `qgen rework` (part 6; RUNBOOK: only on the gamemaster''s word).

## Done when
- `qgen report` shows ≥ 5000 approved `base` questions, and every difficulty meets part 1''s target.
- The last two batches pass part 4''s thresholds, and part 5''s human spot checks agree with the LLM review at the agreed rate.
- `qgen validate` is clean; `trivia-media sync --status approved` has filled the cache.', '2026-10-11T20:08:18Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (2, 2, 'masterplan', 1000, 'The game referee moves from Python into `app/client/src/engine/`, a pure TypeScript module, with the same rules and the family''s saves kept; afterwards the game runs without Python, which the Steam desktop shell needs. Source plan: `plans/12-client-engine.md` (tasks PORT-1..PORT-8; PORT-6, the pool export, is done).

**The tasks of this masterplan are not implementation work: each one writes the plan for one part below** (`pm plan add 2 …`), with its own tasks, files and checks.

## Today (what the parts must cover)
- `app/server/game.py` (583 lines): players, one running game as a JSON state in `state/game.sqlite` (tables players, games, burned), pick, answer, skip (for the player / for everyone), undo (one step), abandon, delete player, jokers hint/skip/easier/category/snipe with availability checks (`jokers_view`, `trial`), joker budget per game (MD-1, `set_jokers`). Uses `random.shuffle` for answers and joker replacements.
- `app/server/selection.py` (130 lines): levels, `LEVEL_RANGES`, `available`, bipartite matching `assign`, `draw`, `supply`; also `burned_ids` / `STATE_DB`, read by the authoring side: `authoring/server/overview.py` (start page) and `qgen report`.
- `app/server/main.py`: game routes `/api/game*`, `/api/players*`; also non-referee routes `/api/categories` (all bundles, D-43), `/media` (cache + download on miss, D-17), `/api/flags` (`state/flags.json`, read by `trivia-authoring`, GM-5/D-47).
- Client: `app/client/src/lib/api.ts` (fetch calls), `lib/types.ts`, screens in `app/client/src/game/`.
- Packaging: `flake.nix` `.#app` copies `app/server`, `app/data`, `app/client/dist`.

## Parts

1. **Parity fixtures (PORT-1)**
   - Scenario recorder for `game.py` + `selection.py`: scripted games on a small fixed pool (picks, answers, every joker incl. unavailable ones, skip, burn for everyone, undo, abandon, joker budget, supply failure at new game, several players).
   - Randomness made deterministic (inject the shuffle/draw choices or a seeded RNG whose sequence TS can reproduce); record inputs and resulting states/views as JSON in `app/client/src/engine/fixtures/`.
   - Recorder lives in `authoring/tools/` or as a throw-away script (decide in the plan; fixtures are committed either way).
   - Suggested priority: 700 (first; everything else replays its fixtures).

2. **Engine core: rng, pool, selection (PORT-2)**
   - `engine/rng.ts` (seedable PRNG), `engine/pool.ts` (load `pool.json` + categories files incl. bundles, filter), `engine/selection.ts` (levels, supply, matching, draw).
   - Test runner with no new dependency: `node:test` on Node 22 (type stripping or a `tsc` step; settle in the plan), wired into an `npm` script.
   - Done when: selection fixtures replay identically; invariant tests (every level 4 cards, burned never return).
   - Suggested priority: 600.

3. **Engine game state machine (PORT-3)**
   - `engine/game.ts`: pure functions state → state for new game, pick, answer, skip, undo, abandon, jokers + availability + budget, players and burns; the view the screens need (same shape as today''s `{"game": …}` where practical).
   - Decision entry in `plans/decisions.md`: the client holds the correct answer (relaxes D-25); the UI still never renders hidden data.
   - Done when: all game fixtures replay identically.
   - Suggested priority: 600, after part 2.

4. **Save document, stores and migration (PORT-4, PORT-5)**
   - `SaveData` `{version, players, games, burned}`, one JSON document; `Store` interface `load/save`; `ServerStore` (`GET/PUT /api/save`, atomic write of `state/game.json`, retry on Windows file locks); `MemoryStore` for tests/demo.
   - Migration `state/game.sqlite` → `state/game.json` once on server start; `.sqlite` kept as backup; tested on a copy of the family''s real save (never on the original).
   - Authoring readers switch from SQLite to `game.json`: `authoring/server/overview.py`, `qgen report` (`selection.burned_ids`).
   - Decide where flags live (stay in `state/flags.json` via `/api/flags`, or move into `SaveData`); `trivia-authoring` must still pick them up.
   - Suggested priority: 900 (save format = schema); the plan must still order it after part 1 so fixtures are recorded against the untouched Python state.

5. **Screens on the engine (PORT-7)**
   - Replace the game calls in `lib/api.ts` with engine calls + `ServerStore`; keep categories/media/flags calls as decided in parts 4 and 6.
   - Client loads `pool.json` and categories statically (server serves `app/data/` read-only or the build copies it; settle in the plan).
   - Placeholders (D-25 `PLACEHOLDER(...)`) stay as they are; no UI changes beyond the wiring.
   - Done when: a full game, every joker, undo and admin overlay work in the browser; the family plays a test night on the TS engine.
   - Suggested priority: 500.

6. **Python server cleanup and docs (PORT-8)**
   - Delete `app/server/game.py` and the game routes from `main.py`; decide the fate of `selection.py` (only what `qgen report`/overview still need, or they call the TS engine via Node).
   - Milestone says `trivia` serves static files plus `/api/save` only: resolve against `/media` (download on cache miss) and `/api/flags`; if they stay, record why (decision entry), otherwise move them.
   - Update `plans/01-architecture.md`, `plans/12-client-engine.md` (tasks `[x]`), `AGENTS.md`, `directory.md`, `README.md`, the `main.py` docstring; check `nix build .#app` still runs.
   - Suggested priority: 400 (last).

## Order
1 → 2 → 3 → 4 → 5 → 6. Part 4''s Python side can start after part 1; its TS side needs part 3''s state shape.

## Constraints (from the milestone)
- Same rules; the family''s saves survive (migration tested on a copy).
- No new dependencies beyond Svelte/Vite and Node built-ins.
- Out of scope: desktop shell (`FileStore`, plan 18), controller, new game modes.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (3, 3, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (4, 4, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (5, 5, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (6, 6, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (7, 7, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (8, 8, 'masterplan', 1000, 'tbd.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (9, 9, 'masterplan', 1000, 'tbd.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (10, 10, 'masterplan', 1000, 'tbd.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (11, 11, 'masterplan', 1000, 'tbd.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (12, 1, 'Targets and progress', 700, 'Part 1 of the masterplan (plan 1). The `base` bundle grows to 5000 approved questions (D-52), with a target per difficulty that tapers at the top. This plan stores those targets where the authoring tools can read them, shows approved vs. target in `qgen report` and on `/stats/difficulty`, and turns the milestone''s "done when" into one command that says pass or fail.

## Targets file (D-53)
- New `authoring/data/targets.json`, keyed by bundle: `{"about": "…", "base": {"total": 5000, "difficulty": {"1": n, …, "15": n}}}`.
- Numbers: pm decision 1 (recommended: 1: 250 · 2: 350 · 3–8: 450 each · 9–11: 330 each · 12–13: 230 each · 14–15: 125 each).
- Loader in `authoring/tools/` (e.g. `load_targets(bundle)` in `qgen.py`, or a small `targets.py` if the server also imports it); `None` for a bundle without targets.
- `qgen validate`: levels = the scale in `app/data/age-groups.json`, every value ≥ 0, sum = `total`.
- Per category: no stored number. Derived share = `total × subcategories in category / subcategories in bundle`; shown as a guide, not part of the exit check.
- Part 2 (aim batches at gaps, plan for task 14) reads the same loader for `draft`''s weights; this plan only provides it.

## Progress view
- `qgen report`: new section "progress vs. targets (base)": per difficulty `approved / target`, missing count, percent; total line; per broad category `approved / derived share`. Approved = status `approved`, bundle `base`, regardless of burns. `--bundle <id>` for another bundle with targets.
- Authoring server: `GET /api/targets` (the file as JSON); doc line in `authoring/server/main.py`''s docstring.
- `/stats/difficulty` (`authoring/ui/src/stats/DifficultyChart.svelte`): a target marker per bar (tick or outline) and `approved / target` in the bar''s label, when the selected bundle has targets. `fetchTargets` in `authoring/ui/src/lib/api.ts`, type in `lib/types.ts`.
- `/stats/categories`: approved vs. derived share per broad category, same style. Only if it fits the existing chart without a redesign; otherwise leave it to `qgen report`.
- `npm run check` clean; check the page in the browser with `trivia-authoring`.

## Exit check ("quality is fine")
- `qgen report --exit-check` (or a `qgen milestone` subcommand; pick the one that fits `qgen.py`''s CLI): one line per criterion, ✓/✗, exit 1 if any fails:
  - approved `base` ≥ 5000;
  - every difficulty ≥ its target;
  - the last two committed `base` batches pass part 4''s thresholds (plan for task 16: per-batch health metrics, `authoring/reports/<batch>.md`);
  - the last two batches'' human spot checks agree with the LLM review at the rate of pm decision 2, with at least its sample size (part 5, plan for task 17, records them);
  - `qgen validate` clean.
- Reads part 4''s metrics and part 5''s spot-check records; doesn''t compute them. Until those exist, the criterion prints "not available" and counts as ✗.
- Write the agreed criteria (decision 2''s numbers) into `plans/16-content-target.md` "Quality bar" as the family pool''s bar, and close CT-5''s question there for the family pool.

## Tasks (for the split)
1. Targets file, loader, `validate` check, D-53 already logged. Waits for pm decision 1.
2. `qgen report` progress section. Waits for decision 1 (needs the file).
3. `/api/targets` and target markers on `/stats/difficulty` (+ categories if cheap). Waits for decision 1. Priority 500 (client).
4. Exit check. Waits for decision 2; runs after the tooling of parts 4 and 5 (priority 640).

## Done when
- `qgen report` prints approved vs. target per difficulty and per category for `base`.
- `/stats/difficulty` shows the targets.
- The exit check runs and, today, fails on the count criteria with the right numbers.', '2026-10-11T23:39:28Z', 13);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (13, 1, 'Aim batches at difficulty gaps', 700, 'Part 2 of the masterplan (plan 1, B-6). Batches should fill the pool where it is thin against the targets of plan 12 (D-53), and a question drafted for difficulty 14 should come out near 14. Today `draft` spreads targets evenly (D-40), the concept draw barely follows the target, and the drafter writes hard targets about three levels too easy. This plan measures that, then fixes the drawing (D-54) and the prompts as implementation tasks; never as a workaround inside a batch run (RUNBOOK).

## Baseline (2026-10-11, throw-away script)
- Mean difficulty per target level, batch-7 (drafted · rated · final, merged questions):
  - targets 1–3 → 3.6–4.1 · 3.6–4.1 · 3.6–3.9 (too hard at the bottom)
  - targets 4–8 → roughly on target (±1)
  - targets 9–10 → 8.7 · 8.2 · 8.8–9.0
  - targets 11–12 → 10.0 · 9.0 · 10.1–10.3
  - targets 13–15 → 11.2–11.8 · 10.0–10.8 · 11.3–12.1
- batch-8 drafts (not rated yet): closer at the top (target 15 → 13.2), worse at the bottom (target 1 → 5.1).
- Mean concept `known_at` per target: batch-7 7.0–8.6 at targets 1–8, 10.7–10.8 at 12–15; batch-8 8.4–9.4 at 1–5, 11.5–11.6 at 13–15. The concept draw (`concepts.draw_concepts`, weight `1/(1+uses)² / (1+|known_at−d|/2)`) is dominated by use count; `known_at` hardly matters.
- Concept supply isn''t the problem: the base concept lists have ~1000–3000 unretired concepts at each `known_at` 9–15, but only ~500–1000 at 1–4.
- `prompts/rate.md` asks for `difficulty_estimate` 1–10, so the rater can''t rate above 10; with `DIFFICULTY_GAP = 3` every question at 13+ looks overrated and may get lowered in `revise`.
- House style''s calibration examples are all at 1–6 and all say "AI guessed too high": they push the drafter down, and nothing anchors 10–15.

## Measurement (`qgen report`)
- `qgen report --calibration [<batch>…]`: per target level, n drafted, mean drafted/rated/final difficulty, mean concept `known_at`, merged and approved counts; reads `work/<batch>/slots.json`, `drafts/`, `ratings/`, `ids.json` and the pool. Default: the last two batches.
- Plan for task 16 (part 4, batch health metrics) reuses it for "difficulty spread vs. targets"; don''t build it twice.

## Fixes
- **Rater scale:** `rate.md` `difficulty_estimate` on the shared scale 1–15 (house style). Check `DIFFICULTY_GAP` still makes sense afterwards.
- **Concept draw:** `known_at` must follow the target: prefer concepts within ±1–2 of the target, widen only when none are left; use count breaks ties inside that window. Check with a seeded dry run of `draw_slots` (no LLM calls) that mean `known_at` per target is within ±1.
- **Prompts** (`draft.md`, `house-style.md`): what makes a question hard on this scale (who can answer it, not obscure facts); the ±1 tolerance in `draft.md` must not become a habit of rounding down; calibration anchors at 9–15 next to the existing low ones. Anchors are the gamemaster''s (house style says "Calibration from the gamemaster"): the task proposes ~8 approved questions at 9–15 as a pm decision, the gamemaster confirms or corrects their levels, then they go into the house style.
- **Low end:** targets 1–3 land at ~4; same anchors/draw fix. Not a priority (plan 12''s targets want fewer at 1–2), but measure it.

## Aim at gaps (D-54)
- `target_weights()` in `qgen.py`: with targets for the batch''s bundle (plan 12''s loader), weight per level = `max(0, target − approved)`; even weights (D-40) without targets; the focus-group path (`LEVEL_WEIGHTS`) unchanged.
- `batches.subcategories()` (shared with the authoring start page): rank by approved questions weighted by the level deficits, i.e. `Σ_level approved(sub, level) × deficit_share(level)`, ties as now. Still `batches.SHARE` of the subcategories (D-46); no new `qgen batch` arguments (D-36).
- `assign_difficulties`/`draw_slots`: hand each subcategory the targets its concept list can carry (unused, unretired concepts with `known_at` near the target), instead of a plain shuffle; a subcategory without hard concepts doesn''t get 15s.
- Print the drawn target histogram at the start of `draft`, so the batch log shows the batch''s shape.

## Tasks (for the split)
1. `qgen report --calibration`; record batch-7 and batch-8 numbers here (batch-8 once it''s rated). Priority 710: the baseline comes first.
2. `rate.md` on 1–15; re-check `DIFFICULTY_GAP`.
3. Concept draw follows `known_at`; seeded dry-run check.
4. Hard-question guidance in `draft.md`/`house-style.md`; anchor candidates as a pm decision (`pm decision add`, task pending on it), then write the confirmed anchors in.
5. Deficit weights in `target_weights()`. Needs plan 12''s targets file and loader (plan 12 task 1, pm decision 1): make it pending on decision 1.
6. Subcategory ranking and per-subcategory target assignment by deficit and concept supply. After task 5; also pending on decision 1.
- Every task: `qgen validate` clean; no batch run inside these tasks. The effect is checked on the next batch by plan for task 18 (batch runs) with `qgen report --calibration`.

## Done when
- `qgen report --calibration` exists and the baseline is recorded.
- A seeded dry run draws targets weighted by deficit, and mean concept `known_at` per target is within ±1.
- The first batch after these tasks lands within ±1.5 of the target at every level 11–15 (final difficulty), or the gap is logged with the next fix.', '2026-10-11T23:41:37Z', 14);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (14, 1, 'More subcategories', 600, 'Part 3 of the masterplan (plan 1). The concern was that subcategories run dry as the pool grows to 5000: concept lists and the per-subcategory avoid list wear out, and that leads to duplicates and easy hard questions. The baseline says this hasn''t happened yet: QP-16 (2026-10-10) took `base` to 184 subcategories, so this plan builds the check that spots saturation, proposes new subcategories where the check or the category balance asks for them, and adds the ones the gamemaster approves (RUNBOOK: the subcategory list is the gamemaster''s).

## Baseline (2026-10-11, throw-away script)
- `base`: 28 broad categories, 184 subcategories (QP-16 added 68, 26 of them in 5 new broad categories). 66 subcategories have 0 approved questions; batch-8 (92 subcategories) drafts most of them.
- Most approved in one subcategory: 19 (Plantas, Mundiales de fútbol). At 5000 the mean is ~27 approved and ~50 asked per subcategory.
- Concept lists: 37–255 concepts. Fewest unused: Empresas famosas 37, Origen de las marcas 48, Océanos 51, Fantasía 57, Monumentos famosos 57, Bichos raros 58. `qgen batch` tops up automatically below 30 unused (`LOW_STOCK`).
- 21 old subcategories have no concept list yet (Idioma, Ciencia, Historia, Aves, Anime, …). The batch that picks them creates the list (D-37).
- Hard supply is fine overall: ~14k unused concepts at `known_at` ≥ 11, against roughly 900 wanted at 11–15 (plan 12). Thin spots: Productos del supermercado 8, Planeta Tierra 13, Tecnología 17, Números 18; broad categories Cuerpo humano and Marcas y logotipos ~36 per subcategory.
- Duplicates: merge dropped 1 duplicate in batch-6/7. Overlaps show up at review instead (needs_work). 2 of batch-7''s 3 overlaps span two subcategories with near-synonym concepts (Caballeros «Almena» / Castillos «Almenas»; Caballeros / Héroes griegos «Son constelaciones»). Catching those is part 4''s job (plan for task 16), not this plan''s.
- Broad categories with few subcategories get few questions, because batches pick by subcategory (D-46) and plan 12''s per-category targets follow subcategory count (D-53): Espacio 1, Cuerpo humano 2, Fiestas y tradiciones 2, Fútbol 2, Videojuegos 3, Amazonas 3. At 5000 Espacio would have ~27 questions; Historia would have ~490.

## Saturation check
- `qgen report --subcategories [--bundle <id>]`: one row per subcategory, with approved and asked counts (asked = all statuses = avoid-list length), list size, unused, unused at `known_at` ≥ 11, top-ups so far, and overlaps (merge duplicate drops + review needs_work for overlap, last two batches). Also a row per broad category: subcategories, approved, unused hard concepts.
- A subcategory is **saturated** when any of these holds: unused < 36 (2 batches of 18 slots) right after a top-up; unused at `known_at` ≥ 11 < 10; overlaps ≥ 10 % of its drafts in the last batch; asked ≥ 60 (a long avoid list in the draft prompt). These thresholds are a first guess. Tune them in the report task and write them here.
- Reuse plan 13''s `qgen report` code (`--calibration`) and part 4''s overlap counts once they exist; don''t count things twice.

## Proposals
- Three sources: (a) subcategories the check flags as saturated: split them or add a neighbour; (b) broad categories with ≤ 3 subcategories (category balance in play); (c) topics that carry hard questions (11–15), where a well-informed adult knows the answer and a child doesn''t, e.g. inside Espacio, Cuerpo humano, Ciencia y matemáticas.
- Each proposal has: name (Spanish, like the others), broad category, one-line scope, reason (which source, which numbers), and ~10 sample concepts with `known_at`, at least 3 of them at 11–15.
- Checks before proposing: no name or near-synonym of an existing subcategory in any bundle (unique names, D-43); no Colombia-only topic (D-49, `colombia` bundle); broad enough for ≥ 100 concepts.
- New broad categories are out of scope: they add tiles to the game''s «Cambiazo» picker. Propose one only if the decision''s answer asks for it.

## Tasks (for the split)
1. `qgen report --subcategories` with the saturation flags; record the baseline numbers and the tuned thresholds in this plan (`pm plan edit`). `qgen validate` clean.
2. Proposal round: run the report and write 10–20 proposals by the rules above into the body of a pm decision (`pm decision add "Which new base subcategories?"`, options: "add the recommended ones" first, then "add all", "none for now"). Then make task 3 wait for it (`pm task-pending-decision`). No changes to `categories.json` in this task.
3. Add the approved subcategories to `app/data/categories.json`, in their broad category, then create their concept lists with `qgen concepts --subcategories "<names>"` (one Opus call per list, not a batch run). Log the change as a QP entry in `plans/02-question-pool.md`. `qgen validate` clean. Pending on task 2''s decision.
- Later rounds: the plan for task 18 (batch runs) reruns `qgen report --subcategories` every two batches. When it flags subcategories, it adds a proposal round like task 2 to this plan.

## Done when
- `qgen report --subcategories` shows the flags; baseline and thresholds are recorded here.
- The gamemaster has answered the proposal decision; the approved subcategories are in `categories.json` with concept lists, and `qgen validate` is clean.', '2026-10-11T23:43:50Z', 15);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (15, 1, 'Duplicate and drift detection', 700, 'Part 4 of the masterplan (plan 1, B-5; absorbs PE-6, PE-13, MP-11). Two things get worse quietly as the pool grows to 5000: drafts that ask a fact the pool already asks, and the batch as a whole (more drops, more `needs_work`, narrower styles, higher cost). This plan catches overlaps before merge instead of at review, measures every batch''s health against thresholds, and makes a batch that fails them stop the next one until the gamemaster has looked (D-55).

## Baseline (2026-10-11, throw-away script)
- `dedupe`/`duplicates()` (in `merge`): a duplicate needs the same normalized answer **and** question similarity > 0.6 or the same essential media type. Batch-6/7: 1 duplicate dropped.
- Overlaps caught only by the review (needs_work), none of them by `duplicates()`:
  - q-0646 / q-0217 «Almenas»: same answer, different wording, different subcategory (Caballeros / Castillos); concepts «Almena» / «Almenas».
  - q-0644 / q-0957 «Son constelaciones»: same answer, different topic (Caballeros / Héroes griegos).
  - q-0689 / q-0279 «Ramen»: same answer; the draft''s concept «Fideos chinos», the pool question''s concept «Ramen».
  - q-1210 / q-0315: answers differ (El Imperio contraataca / Darth Vader); the draft''s concept «Yo soy tu padre» is in the pool question''s text.
  - B-5: q-0369 / q-0341 (Rubik → Hungría), q-0420 / q-0328 (silleteros).
- The review sees related questions (`related_questions()`: similar answer or same subcategory, first 30) only after merge, media and sheets have been paid for.
- `review.reasons` is free text and not stored; `needs_work` reasons are only in `review.feedback`. batch-7: 112 needs_work of 616 merged; 96 dropped by the pipeline (hard fails, duplicates, skipped slots); ~$120.74 for 504 approved (~$0.24 each).
- `work/batch-4…7` have drafts, ratings, `dropped.json`, `costs.log`, `run.json` (batch-4 without `slots.json`/reviews); `work/` is gitignored, so old batches are measured locally only.

## Overlap check before merge (B-5)
- **Candidates (code, no LLM):** for each draft, pool questions of every bundle (status ≠ `rejected`) and earlier drafts of the same batch where any of these holds:
  - normalized answers equal or similar (`SequenceMatcher` ≥ 0.8, or one contains the other); numbers and yes/no excluded as now;
  - the draft''s concept or answer stem-matches the other''s concept or answer (Almena/Almenas, Ramen);
  - the draft''s concept or answer occurs in the other''s question or `fun_fact`, or the other way round («Yo soy tu padre»).
  - Cap ~8 candidates per draft, closest first. Stem match: lowercase, no accents, drop a trailing «s»/«es»; no new dependencies.
- **Judge in `rate`, no extra calls:** the grouped `rate` call (PE-1) gets each draft''s candidates and a new hard criterion `no_overlap` (5 = asks a different fact; ≤ 3 = knowing one answer gives the other away, or the same fact asked again). A hard fail is dropped at merge, as today, with reason `overlap like q-…`. The concept isn''t retired. Within-batch pairs: the later draft fails.
- `duplicates()` stays as the cheap exact check in `merge`.
- `prompts/rate.md` and the schema are the gamemaster''s prompts (RUNBOOK): changed here as an implementation task, never inside a batch run.
- Check: replay the candidate finder on batch-7''s merged questions against the pool as it was before batch-7 (ids < q-0596): it must list all four pairs above (and B-5''s two against their pools); report candidates per draft (mean, max). Then rate ~20 batch-7 drafts with and without candidates (one call each way) and check the four overlaps fail `no_overlap` and the others don''t.
- `qgen report --overlaps`: the same candidate finder over the approved pool (pairs, no LLM), so the gamemaster can clean old overlaps in the review tool. Listing only.

## Needs-work reasons
- `REVIEW_SCHEMA`: `problems`, an array of `giveaway`, `fact`, `ambiguity`, `overlap`, `media`, `difficulty`, `style`, `other`; stored in `q.review.problems`. `record` adds `media` (no adequate media) and `fact` (fact check not confirmed) for the fixed rules. `prompts/review.md` says when to use each.
- Older questions without `problems`: a keyword classifier in the report (`No se encontró una imagen adecuada` → media, `q-\d{4}` → overlap, `pista` + `regala|delata|da la respuesta` → giveaway, …), marked as guessed. No backfill into the pool.

## Batch health
- `authoring/tools/health.py`: `batch_health(run) -> dict` from `work/<run>/` and the pool. Shared by `batch-report`, `qgen report --batches` and plan 12''s exit check (which reads, doesn''t recompute).
- Metrics per batch:
  - drafts, dropped (by reason: hard fail per criterion, overlap, duplicate, skipped slot), drop rate;
  - merged, approved, needs_work; needs_work rate by `problems`;
  - overlap rate = (dropped as overlap or duplicate + needs_work for overlap) / drafts;
  - difficulty: merged per target level vs. drawn slots; final vs. target from plan 13''s `qgen report --calibration` code (reuse, don''t rebuild); approved per level vs. the deficit to plan 12''s targets;
  - variety: per axis, the top value''s share and the number of values used; media share (stimulus ≠ `none`); mean `fun` score;
  - cost: total $, $ per approved, calls per approved; wall time per step where `run.json`/the log has it.
- `batch-report`: a "## Health" section at the top of `authoring/reports/<batch>.md`: each metric, its threshold, ✓/✗, and the previous two batches'' values.
- Cross-batch: `qgen report --batches [<batch>…]` (default batch-4 onward) prints one column per batch; `batch-report` also regenerates `authoring/reports/batches.md` with the same table and the gamemaster''s acknowledgements (below).

## Thresholds (first guess; the gamemaster decides)
- drop rate ≤ 20 % of drafts;
- needs_work ≤ 20 % of merged; any one problem ≤ 8 %;
- overlap rate ≤ 3 % of drafts, needs_work for overlap ≤ 1 % of merged;
- merged at 11–15 ≥ 60 % of the slots drawn there; final difficulty within ±1.5 of target at 11–15 (plan 13''s goal);
- top value of any axis ≤ 25 % of merged; media share 20–50 %;
- $ per approved ≤ $0.35;
- trend: no metric worse than the mean of the previous two batches by more than half its threshold''s margin.
- Stored in `authoring/data/targets.json` under `"batch_health"` (plan 12''s file and loader, D-53); `qgen validate` checks the keys.
- **Stop before the next batch (D-55):** when the last committed batch fails a threshold, `qgen batch` exits 2 before `concepts` and names the report. RUNBOOK step 3 already says "other exit code: stop and show the output", so an agent stops without new rules. The gamemaster clears it with `qgen health ack <batch> "<note>"`, which records the note in `authoring/data/health-acks.json` (shown in `batches.md`). Add one line to RUNBOOK''s exit-code table for 2. `qgen rework`/`tighten` aren''t blocked.
- Plan 12''s exit check: "the last two batches pass" = no ✗ in `batch_health` (an ack doesn''t count as a pass).

## Old checks this plan closes
- PE-6 (grouped rate/revise, batch-6 vs. batch-4/5), PE-13 (concepts and axes, batch-7 vs. batch-6), MP-11 (media providers, batch-7 vs. batch-6): answered by `qgen report --batches` over batch-4…7 plus the needs_work `media` share; write the numbers into plans 20 and 23 and mark them `[x]`. Their blind side-by-side and re-rating parts are dropped: part 5''s spot checks (plan for task 17) cover quality.

## Tasks (for the split)
1. Overlap candidate finder (in `qgen.py` or a small `overlap.py`) + `qgen report --overlaps`; replay on batch-7 as above, record recall and candidates per draft here. Priority 710: it shapes the next batch most.
2. `no_overlap` in `rate` (schema, `rate.md`, candidates in the payload, merge drop reason); the 20-draft before/after check. After task 1.
3. `problems` in the review schema, `review.md`, `record`; keyword classifier for old questions.
4. `health.py`, `qgen report --batches`, Health section in `batch-report`, `batches.md`. Run it over batch-4…7, record the baseline here, then close PE-6, PE-13, MP-11 as above. Plan 13''s `--calibration` is reused if it exists; otherwise this task leaves the difficulty-vs-target rows "n/a" and plan 13 task 1 fills them.
5. Threshold decision: from task 4''s baseline, `pm decision add "Batch health thresholds and stop rule?"` with the numbers above adjusted to the baseline (options: the recommended set; looser; warning only, no stop). Then task 6 waits for it.
6. Thresholds into `targets.json`, validate, ✓/✗ in the report, the stop in `qgen batch`, `qgen health ack`, RUNBOOK exit code 2. Needs plan 12 task 1 (targets file) and task 5''s decision.
- Every task: `qgen validate` clean; no batch run inside these tasks. Batch-8 is in progress: tasks 1–2 change `rate`/`merge`, so they land before or after batch-8''s rate step, not during it (check `work/batch-8` first; if batch-8 is mid-rate, wait for plan 18''s batch-run task).

## Done when
- The replay finds the known overlaps before merge, and the next batch''s overlaps are dropped by `rate`, not left `needs_work`.
- Every `authoring/reports/<batch>.md` from the next batch on has a Health section; `batches.md` compares batch-4 onward.
- Thresholds are decided and stored; a failing batch stops the next `qgen batch` until acknowledged.
- PE-6, PE-13, MP-11 and B-5 are closed with numbers.', '2026-10-11T23:45:50Z', 16);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (16, 1, 'Quality control after every batch', 650, 'Part 5 of the masterplan (plan 1). Today the only judge of a batch is the LLM review (`prompts/review.md`, D-33), and nobody measures whether it judges well. This plan adds three checks per batch: an independent LLM audit of a sample, a blind human spot check of a smaller sample, and a fixed procedure that turns their findings into prompt or house-style changes before the next batch. Across batches it tracks the human/LLM agreement rate, the main "quality is fine" signal of the milestone (pm decision 2, plan 12''s exit check). Only tooling and procedure here; the QC runs themselves are tasks of plan for task 18 (batch runs).

## Baseline (2026-10-11)
- Human verdicts already exist: a human review in the review tool replaces the LLM one and keeps it in `review.previous` (`authoring/server/main.py` `set_review`, D-33). But the human picks what to look at (mostly `needs_work`, `/review?status=!approved`), so that is no random sample, and the page shows the LLM verdict before the human decides.
- No second LLM opinion: `review` is the last judge; `factcheck` (sonnet) checks facts only, before review.
- batch-7: 504 approved, 112 needs_work, no record of how many approved ones the gamemaster would have sent back.

## LLM audit (a)
- New prompt `authoring/tools/prompts/audit.md` (the gamemaster''s prompt, RUNBOOK; written here as an implementation task). Different job from `review.md`: a strict second reader of the question **as played**. It doesn''t see the review''s verdict, `fix`, rater notes or fact check, so it is independent. It sees the question, options, hints, fun fact, difficulty, media title/role, `related` pool questions, and the house style.
- Checks: facts (own knowledge + web search, like `factcheck`), ambiguity (second defensible option), giveaways (text, hints, media title), overlap with `related`, difficulty on the shared 1–15 scale (D-38; its own estimate), house style ("Keep it short", retired styles).
- Answer schema: `verdict` `ok` | `problem`; `problems` from plan 15''s list (`giveaway`, `fact`, `ambiguity`, `overlap`, `media`, `difficulty`, `style`, `other`; reuse its constant, don''t copy it); `severity` `minor` | `major` (major = would be `needs_work`); `difficulty_estimate` 1–15; `notes` (English, one or two sentences).
- Sample: seeded by batch name, `AUDIT_SAMPLE` = 60 merged questions with an LLM review (approved and needs_work in proportion), always ⊇ the spot-check sample, so audit, review and human can be compared on the same questions. One opus call per question (~$5 per batch; check against `costs.log` on the baseline run).
- `qgen audit [--batch <b>]`: writes `work/<batch>/audit/<id>.json`; skips done ones like every step. A step of `qgen batch` after `record`, before `export`; so RUNBOOK and D-36 don''t change. Changes nothing in the pool: the audit never approves or rejects (RUNBOOK).
- `batch-report`: a "## Audit" section: sample size, flagged (major) among approved and among needs_work, problems by kind, mean |audit difficulty − final difficulty|, audit/review agreement (both accept or both not), and every major finding on an approved question as `id: problem — notes` with its `/review/<id>` link.
- Review tool: `/review?batch=<b>&audit=flagged` lists the audited questions with a major finding; the audit''s notes show next to the review''s. The gamemaster decides them there.

## Human spot check (b)
- `/review?batch=<b>&sample=1`: the batch''s spot-check sample, `size` from `authoring/data/targets.json` `quality.spot_check_size` (plan 12''s file and loader, D-53; default 30 until pm decision 2 is answered). Seeded by batch name, a subset of the audit sample, same ids on every reload.
- **Blind:** in sample mode the page hides the LLM decision, feedback, reasons and the audit until the human has decided; then it shows them next to the human''s verdict (agree / disagree). Picked media stays visible (it is part of the question as played).
- The human decides as usual (approve / needs_work / reject, feedback, difficulty, media); that is a normal human review (D-33). In addition the server records the spot check in `authoring/data/spot-checks.json`: `{"<batch>": {"size": n, "seed": "<batch>", "items": {"<id>": {"llm": "approved", "audit": "ok"|"problem"|null, "human": "needs_work", "problems": [...], "difficulty": [llm, human], "media_changed": bool, "on": "YYYY-MM-DD"}}}}`. Its own record, so later reworks or re-reviews don''t change past agreement numbers. Undo removes the item.
- `POST /api/spot-checks/<batch>/<id>` (written by the review page on decide), `GET /api/spot-checks`; doc lines in `main.py`''s docstring. `qgen validate` checks the file (ids exist, values in range).
- Agreement: **agree** = both accept (`approved`) or both don''t (`needs_work`/`rejected`). Also counted: **false approve** (LLM approved, human not; the one that puts bad questions on the TV), false needs_work, difficulty |Δ| ≥ 2, media changed.

## Findings → changes (c)
- Procedure in a new `authoring/QC.md` (for the gamemaster and pm workers; RUNBOOK stays the batch procedure, with one line in step 5 pointing to QC.md). D-56.
  1. `qgen batch` finished and committed: the report has the Audit section.
  2. Spot check: the gamemaster opens `/review?batch=<b>&sample=1` (~10–15 min for 30). A pm worker can''t do this: the part-6 task adds a pm decision "Spot check <batch> done?" and waits on it.
  3. `qgen report --qc <batch>`: rewrites the "## Quality control" section of `authoring/reports/<batch>.md`: agreement, false approves, difficulty and media changes, audit vs. human, every disagreement with the human''s feedback, grouped by `problems`.
  4. Findings → proposals: a problem kind with ≥ 2 disagreements or major audit findings, or any false approve for `fact`, gets a concrete proposal: which prompt (`review.md`, `draft.md`, `house-style.md`, `rate.md`, `audit.md`) and the change in a few lines. All proposals go into one pm decision ("QC <batch>: which changes?", options: recommended set / all / none). Approved ones become implementation tasks (their plan''s priority, so above the -100 batch tasks). Prompt changes never happen inside a batch run (RUNBOOK).
  5. The next batch task waits for 2 and for 4''s decision (pm `task-pending-decision`); plan 18 sets that up.
- The report''s QC section ends with "Changes from this QC: …" (task ids), written in step 4, so the trend table can tell batches before and after a change.

## Trend
- `qgen report --qc` without a batch: one column per batch with a spot check or audit: audit n, major findings among approved %, human n, agreement %, false approve %, difficulty |Δ| ≥ 2 %, audit/human agreement %; ✓/✗ against `quality.min_agreement` (pm decision 2). Same table in `authoring/reports/batches.md` (plan 15''s file, task 4 there) when it exists.
- Plan 12''s exit check reads `spot-checks.json` and `quality` for "the last two batches agree at the agreed rate with at least the agreed size"; it doesn''t recompute.
- If the audit agrees with the human clearly better than the review does over two batches, that is a finding for step 4 (move the audit''s checks into `review.md`, or make the audit a gate); not automatic.

## Tasks (for the split)
1. `audit.md`, `AUDIT_SCHEMA`, `qgen audit`, the step in `qgen batch`, the Audit section in `batch-report`. Baseline: `qgen audit --batch batch-7`, record flagged rates, problems by kind, cost and audit/review agreement here (`pm plan edit`). Reuses plan 15''s `problems` constant if it exists, else defines it where plan 15 task 3 will find it. `qgen validate` clean. If batch-8 is mid-run, add the step only after its `record` (check `work/batch-8` first).
2. Spot-check tooling: sample draw (shared by audit and server, seeded), `spot-checks.json`, the two endpoints, validate check, review page sample mode (blind, reveal after decide, undo) and `audit=flagged`. `npm run check` clean; check in the browser with `trivia-authoring` on batch-7. Priority 640 (after task 1, which provides the audit sample).
3. `qgen report --qc [<batch>]`, the QC section in the batch report, the trend table (also in `batches.md` if plan 15 task 4 is done). `quality` keys in `targets.json` with `qgen validate` checks: wait for pm decision 2 (`pm task-pending-decision`) and plan 12 task 1 (targets file).
4. `authoring/QC.md` with the procedure above, D-56 (already logged), RUNBOOK step 5 pointer, AGENTS.md "Making questions" one line, `directory.md` entry. Then tell plan 18 (batch runs) the per-batch task pattern: batch → spot-check decision → `--qc` + proposal decision → changes → next batch.
- No batch run and no QC run inside these tasks; the first real QC run (batch-8, or batch-7 as a baseline) is a plan 18 task.

## Done when
- `qgen batch` audits a sample and the report shows it; batch-7''s audit baseline is recorded here.
- The gamemaster can do a blind spot check of a batch in the review tool, and it is recorded in `spot-checks.json`.
- `qgen report --qc` shows agreement per batch against decision 2''s rate; plan 12''s exit check can read it.
- `authoring/QC.md` describes steps 1–5, and RUNBOOK points to it.', '2026-10-11T23:48:16Z', 17);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (17, 1, 'Batch runs', -100, 'Part 6 of the masterplan (plan 1). The recurring work of the milestone: finish batch-8, then one `qgen batch` per task, each followed by part 5''s QC, until part 1''s targets are met. Every task here runs `qgen batch` or depends on one, so the plan has priority -100: it runs only when every implementation task is done or waits for a decision. Plan 16 calls this plan "plan 18" (it was task 18''s plan).

## State (2026-10-11)
- batch-8: `work/batch-8` (WIP commit d7fb13f, on `main`): 57 subcategories in `run.json`, 61 draft files, ~$1.6 in `costs.log`. Resumes with plain `qgen batch` (RUNBOOK).
- Approved `base`: 1035; needs_work: 33 (batch-7''s reasons: giveaway hints, overlap, no usable media).
- Depends on: plan 12 (targets, exit check), 13 (aim at gaps), 14 (subcategories), 15 (overlap, health, stop rule), 16 (audit, spot check, `authoring/QC.md`). Their tasks run first by priority; a batch task doesn''t wait for unfinished ones, it uses what exists and says what was missing in its note.

## Batch tasks under `pm run`
- RUNBOOK clashes with a pm worker in two places: step 1 stops on a dirty tree, but `pm run` keeps `tasks.sql` modified; step 4 commits, but a worker only stages. Fixed once in RUNBOOK (task below): `tasks.sql` alone doesn''t count as dirty; the worker stages exactly the printed `git add` paths and doesn''t commit (pm commits as "task N: …").
- Exit 75 (usage limit, no reset time): `pm decision add "Continue <batch> after the usage limit?"`, `pm task-pending-decision`, stage nothing, stop. Exit 1 three times at one step, other codes, exit 2 (plan 15''s health stop): same, with the last 30 lines in the decision body.
- Never inside a batch task: prompt, `qgen.py`, subcategory or media changes (RUNBOOK). Findings become decisions or tasks in their own plans.

## Per-batch pattern
1. **Batch task** `run batch-<n>` (-100): RUNBOOK steps 1–5. Note: "Done:" line, report path.
2. **QC task** `QC batch-<n>` (-100): `authoring/QC.md` (plan 16): spot-check decision ("Spot check <batch> done?", the task waits on it), then `qgen report --qc <batch>` and the proposals decision ("QC <batch>: which changes?", the task waits on it too). Approved proposals become tasks in plans 13–16 (their priority, so above -100). Missing tooling: do what exists, list the rest in the note.
   - Also records: approved/target per difficulty (`qgen report`), needs_work by reason, media yield (questions `needs_work` for no usable media / merged).
   - Then adds the next pair: `run batch-<n+1>` and `QC batch-<n+1>`. Both QC decisions are answered by then and the change tasks outrank -100, so the next batch runs after the changes; no extra link needed. If the targets of plan 12 are met (or the next batch would overshoot every remaining gap), it adds the exit-check task instead.
3. **needs_work** per pm decision 3: a task pending on it handles batch-7/8''s; once answered, every QC task does the same for its batch (e.g. `qgen rework` only if decision 3 says so: that answer is the gamemaster''s word, RUNBOOK).
- Only one or two batch tasks open at a time, so plans 13–16''s results shape the next batch.

## Media yield
- QC tasks track no-media `needs_work` / merged per batch (batch-7: part of 112 needs_work).
- If it is ≥ 10% in two batches in a row, or the top needs_work reason: the QC task adds `pm task add 1 "write plan: media yield" --kind plan` (masterplan), pointing to `plans/06-images.md`, `plans/23-media-providers.md`, IMG-16/17. Once.

## Exit check (last task)
- `qgen report --exit-check` (plan 12) passes: ≥ 5000 approved `base`, every difficulty at target, last two batches pass health (plan 15) and spot-check agreement (pm decision 2).
- `qgen validate` clean; `trivia-media sync --status approved` (fills the cache; nothing to stage).
- Fails: add the batch/QC pair the failure calls for, drop the task with the failing lines as the reason; the next QC task re-adds it.

## Done when
- The exit-check task is done.', '2026-10-11T23:49:34Z', 18);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (18, 2, 'Parity fixtures for the Python referee (PORT-1)', 700, 'Before the referee moves to TypeScript, a recorder plays scripted games through today''s untouched `app/server/game.py` + `selection.py` and commits what they produce as JSON fixtures. Parts 2 (selection, plan for task 56) and 3 (game, task 57) replay these fixtures and must match them exactly; part 4 (task 58) reuses the DB snapshots as the shape its `SaveData` migrates. Source: `plans/12-client-engine.md`, "Parity strategy" step 1, PORT-1.

## Decisions taken here
- **Randomness: a recorded shuffle tape, not a shared PRNG.**
  - All randomness in the referee is `random.shuffle` (`selection.draw` via `rng=random`, `game.pick`, `game.swap_in`, `game.replacement`); nothing else random.
  - The recorder monkeypatches `random.shuffle`: shuffles an index list `0..n-1` with `random.Random(scenario seed)`, applies it, and appends `{"site", "n", "perm"}` to the step''s tape (`perm[j]` = old index of the element now at position j; `site` = calling function name from the stack, for debugging).
  - TS side: the engine takes an injected `Rng` with `shuffle(xs, site?)` (in place, like Python). Tests use a `tapeRng(tape)` that applies the recorded perms and fails on a wrong `n` or a site mismatch or a leftover/missing entry. Production `rng.ts` (part 2) is free to be any seedable PRNG (e.g. mulberry32 + Fisher–Yates); no need to reproduce Mersenne Twister.
  - Consequence for parts 2/3: shuffle calls must happen at the same points, in the same order, on arrays of the same length; this includes the shuffles inside `game.view` → `jokers_view` → `trial` (order: hint, skip, easier, snipe, skip+purge, then Cambiazo''s `replacement` per subcategory in `categories.load()` order).
- **Time: one fixed `now` per step**, an input of the step (`2026-01-01T00:00:00` + step index minutes). Recorder patches `game.now`. TS engine functions take `now` as a parameter.
- **Recorder location: `authoring/tools/record_fixtures.py`**, committed (imports `app/server` via `layout`, like the other tools). Not throw-away: parts 2/3 will find gaps and need re-recording. Deleted together with `game.py` in PORT-8 (part 6, task 60).
- **Categories and pool: synthetic, committed with the fixtures.** The recorder patches `categories.load` to return the fixture categories, so the real `app/data/` never leaks in and fixtures stay stable when the real pool changes.
- **Recording level: the HTTP response**, as `main.py`''s `game_action` builds it (`200 {"game": view, "event"?}`, `409 {"error", "supply"}`; `GET /api/game` → `{"game", "supply"}`; players routes). The recorder mirrors `game_action`''s dispatch table; a 500 aborts recording.

## Safety
- The recorder sets `TRIVIA_STATE` to a fresh `tempfile.mkdtemp()` **before** importing `paths`/`game`/`selection`, then asserts `game.DB` and `selection.STATE_DB` are inside that dir; fails loudly otherwise. Never touches `state/game.sqlite`.
- Each scenario gets its own fresh temp state dir; deleted afterwards.

## Fixture layout (`app/client/src/engine/fixtures/`)
- `categories.json`: 2 bundles (`base` + one more, D-43), 3 broad categories, ~6 subcategories; same shape as `categories.load()` output (with `bundle`).
- `pools/main.json`: ~90 synthetic approved questions, difficulties 1–10 across all subcategories, enough for several full games per player with jokers; hints 0–3 per question (so «Soplo» runs out); all `pool.json` fields the referee/view read (`id`, `status`, `difficulty`, `subcategory`, `description`, `question`, `answer`, `wrong_answers`, `hints`, `media`, `background`, `fun_fact`, `bundle`).
- `pools/tight.json`: barely enough for one game (supply failure on the second game, Bájale/Cambiazo/purge/snipe-hit unavailable).
- `selection.json`: direct cases for `in_range`, `assign` (subsets of levels, shortages), `supply` (main, tight, tight minus burns), `draw` (with `keep`, `avoid_categories`, `n` < 4, unfillable → null), each with its tape.
- `game/<scenario>.json`, one per scenario:
  - `{name, about, seed, pool, steps: [...]}`
  - step: `{now, call, args, tape: [...], response: {status, body}, db}`
  - `call` ∈ `get_game` (with `player`), `players`, `new`, `pick`, `answer`, `skip`, `undo`, `abandon`, `jokers` (budget), `joker`, `delete_player`.
  - `db`: full snapshot after the step: `players` `[{id, name, created_on}]`, `games` `[{id, started_on, finished_on, result, player_id, state}]` (state parsed), `burned` `[{question_id, player_id, game_id, burned_on}]` sorted by (game_id, question_id, player_id).
  - Errors leave the DB unchanged (transaction rollback): the snapshot shows it; TS must do the same.
- JSON written deterministically (`sort_keys`, `ensure_ascii=False`), one step per line for readable diffs; total size target < 2 MB.

## Scenarios (minimum)
- `win`: new player, 12 correct answers → won; undo after the win.
- `lose-undo`: wrong answer → lost; undo → question again; undo with nothing to undo → error; undo keeps `settings`.
- `hint`: «Soplo» until "no quedan pistas"; question with 0 hints.
- `skip-purge`: «Paso», «Paso» with purge (other table cards of that subcategory replaced, not burned); purge unavailable.
- `easier`: «Bájale» available and unavailable (easiest in its subcategory).
- `category`: «Cambiazo» ok; same subcategory; unknown subcategory; unavailable; the `categories` groups in the view.
- `snipe`: misses until "solo queda una respuesta"; hit → level repeats (`repeat`); hit with no cards left (tight pool).
- `budget`: `jokers` with the «Como las cartas» preset (`game.CARDS`) and partial budgets; spend to 0 → SPENT reason in view and error on play; invalid budgets (unknown joker, 100, -1, `true`, string).
- `admin-skip`: skip for the player, skip for everyone (burn visible to a second player''s supply); skip with no replacement.
- `players`: several players, per-player burns, `players()` order; name cleanup (spaces, case, casefold «Íngrid»/«íngrid»), empty/too long names; delete player (running game too; global burns stay); delete unknown player; game/player IDs after a delete (SQLite reuses max+1 — TS must match).
- `abandon`: abandon; new game while one runs abandons it; undo after abandon → error; every action with no running game → error.
- `supply`: tight pool, second game for the same player → 409 with the supply report; new player still ok; `get_game` supply for a known, a new and no player.
- `errors`: pick out of range / in question phase, answer a struck index, joker in select phase, unknown joker.
- `soak-<n>`: ~10 seeded random walks of legal actions picked from the view (incl. jokers, undo, admin skip, new players), 30–60 steps each, to catch paths the scripted ones miss.
- Legacy SQLite schemas (pre-D-28, pre-JK-2) are out of scope here: the migration (part 4) reads them in Python.

## Notes for parts 2/3 (put in the fixture README)
- Python `sort` and JS `Array.prototype.sort` are both stable; keep the same sort keys (booleans sort False < True).
- `casefold()` ≠ `toLowerCase()` in general; the `players` scenario pins the cases that matter.
- `players()` sorts by `coalesce(max(started_on), created_on) DESC`; scenarios avoid ties (distinct `now` per step).
- Sets in Python (`later_fill`, `asked_categories`) are only used for membership, so their order doesn''t matter.

## Tasks to split into
1. Recorder skeleton: temp state guard, patches (`random.shuffle` tape, `game.now`, `categories.load`), dispatch mirroring `main.py`, deterministic JSON writer.
2. Synthetic `categories.json`, `pools/main.json`, `pools/tight.json` (generated by the recorder, committed).
3. `selection.json` cases.
4. Scripted game scenarios (list above).
5. Soak scenarios.
6. `fixtures/README.md`: format, tape semantics, how to re-record (`python3 authoring/tools/record_fixtures.py`), notes for parts 2/3. Update `plans/12-client-engine.md` (PORT-1 `[x]`, tape decision in "Parity strategy") and `directory.md`.

## Done when
- `python3 authoring/tools/record_fixtures.py` writes all fixtures from scratch; a second run produces byte-identical files (`--check` mode: re-record into a temp dir and diff).
- Every scenario listed above exists; every joker has at least one available and one unavailable case; no step returned 500.
- `state/game.sqlite` unchanged (mtime + checksum before/after a run).
- No new dependencies (Python standard library only).', '2026-10-11T23:58:59Z', 61);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (19, 2, 'Engine core: rng, pool, selection (PORT-2)', 610, 'The pure core of the TypeScript referee: a seedable shuffle, the pool and category data, and a port of `app/server/selection.py` that produces exactly the same results. Part 3 (`engine/game.ts`, plan for task 57) builds on it; it replays the selection fixtures of plan 18 (PORT-1) and adds invariant tests on the real pool. Source: `plans/12-client-engine.md`, PORT-2, "Parity strategy" steps 2–4.

## Depends on
- Plan 18 (Parity fixtures): tape format, `fixtures/categories.json`, `fixtures/pools/*.json`, `fixtures/selection.json`. Tasks 1–2 below can start before the fixtures exist; task 3 needs `selection.json`.

## Decisions taken here
- **Tests: `node:test` with Node''s built-in type stripping, no `tsc` step.**
  - The flake''s Node 22.23 strips types by default (unflagged since 22.18); no new dependency, no build output.
  - Engine code uses erasable syntax only (no `enum`, `namespace`, parameter properties) and imports with explicit `.ts` extensions; `app/client/tsconfig.json` gets `allowImportingTsExtensions: true` (fine with `noEmit`) and `erasableSyntaxOnly: true` (TS ≥ 5.8; repo has 6.0). `verbatimModuleSyntax` is already on (`import type` where needed).
  - Scripts: `app/client/package.json` `"test": "node --test ''src/engine/**/*.test.ts''"`; root `"test": "npm run test --workspaces --if-present"`.
  - No `@types/node` (would be a new dependency): `*.test.ts` and `src/engine/test/` are excluded from `tsconfig.json`, so `npm run check` type-checks the engine but not the tests. Engine modules themselves import nothing from `node:`; only tests read files (`node:fs`).
  - Decision entry in `plans/decisions.md` (next D number).
- **`Rng` interface = plan 18''s tape semantics.** `interface Rng { shuffle<T>(xs: T[], site: string): void }`, in place like Python''s `random.shuffle`; `site` = the Python function name (`draw`, `pick`, `swap_in`, `replacement`).
  - `seededRng(seed: number)`: mulberry32 + Fisher–Yates; no Mersenne Twister parity needed (plan 18).
  - `randomSeed()`: `crypto.getRandomValues` (browser and Node both have global `crypto`). Whether the seed is stored in the game state is part 3''s call.
  - `tapeRng(tape)` in `engine/test/tape.ts` (test-only): applies `perm` (`xs[j] = old[perm[j]]`), throws on wrong `n`, site mismatch, missing entries; `done()` throws on leftover entries.
- **No hidden globals.** Every function that shuffles takes the `Rng` as a parameter; nothing reads `Math.random` or the clock.
- **`pool.ts` is pure: parsed JSON in, typed data out.** Fetching is part 5. Reuses `Media`, `Background`, `Category`, `Status` from `lib/types.ts`; adds the full question type there or in `pool.ts` (with `answer`, `wrong_answers`, `hints`, which today''s client never sees).
- **No bundle filtering.** The referee today plays all approved questions of every bundle; choosing bundles is BN-6, out of scope ("same rules").
- **DB-side helpers stay out.** `burned_ids`, `burned_for`, `player_id` (casefold name match) read SQLite; their TS counterparts work on the save document and belong to part 3/4 (tasks 57, 58). Burned IDs reach `selection.ts` as a `Set<string>` / array.

## Files
- `app/client/src/engine/rng.ts`: `Rng`, `seededRng`, `randomSeed`.
- `app/client/src/engine/pool.ts`:
  - `PoolQuestion` type (all `pool.json` fields), `parsePool(json)` → `PoolQuestion[]` (checks `version` 1).
  - `loadCategories(bundlesJson, files: Record<bundleId, categoriesJson>)` → `Category[]` in `bundles.json` order, base first, a bundle without a file has none (mirrors `categories.load()`).
  - `subcategories(cats, bundle?)`, `broadOf(cats)` (subcategory → category), `bundleOf(cats, sub)`, `categoryOf(broad)` (question → broad slug or `null`, like `game.category_of`), `byId(pool)`.
- `app/client/src/engine/selection.ts`: `LEVELS`, `PER_LEVEL`, `LEVEL_RANGES`, `inRange`, `available(pool, burned, exclude)`, `assign(questions, levels)` → `{assignment: Map<level, id[]>, missing: Map<level, n>}`, `draw(level, questions, {n, keep, avoidCategories, categoryOf, rng})` → `PoolQuestion[] | null`, `supply(questions)` → `Supply[]` (same shape as `lib/types.ts` `Supply`).
- `app/client/src/engine/test/tape.ts`, `test/fixtures.ts` (read fixture JSON via `node:fs`, relative to `import.meta.dirname`).
- Tests: `rng.test.ts`, `pool.test.ts`, `selection.test.ts`, `invariants.test.ts` next to the modules.

## Parity details for `selection.ts`
- `assign`: levels sorted by `(hi - lo, level)`; slots in that order; candidates in input order; augmenting path recursion as in Python (max 48 slots, no depth issue).
- `owner` must be a `Map` (insertion order kept on re-assignment, like a Python dict); `assignment[level]` lists IDs in `owner` order. Don''t use plain objects for ID-keyed maps.
- `draw`: one `rng.shuffle(cands, "draw")` per call, before the loop, on candidates = in range and not in `keep` (even when empty: Python shuffles a list of length 0 too; the tape records it). Then per pick a stable sort by `(categoryOf(q) ∈ table, categoryOf(q) ∈ avoid)`, false before true; `table` from `keep` + picked; `null` is a valid category value. First candidate, not yet picked, whose removal still lets `assign(…, later levels)` fill everything wins; none → `null`.
- `categoryOf` default: `q.subcategory ?? null`.
- `supply`: `range` as `[lo, hi]`, `candidates` count, `missing` from `assign` over levels 1–12.
- Python JSON turns int keys into strings (`"1"`, `"10"` …, sorted as strings): replay compares per level, converting keys, and list order within a level.

## Tasks to split into
1. **Test runner + `rng.ts`**: tsconfig flags and excludes, npm scripts (client + root), `rng.ts`, `test/tape.ts`, `rng.test.ts` (same seed → same permutations; results are permutations; tape errors on wrong `n`, site, missing/leftover entries; hand-written tape). Decision entry. Check: `npm test` and `npm run check` pass; `npm run build` still works with `.ts` import extensions.
2. **`pool.ts`**: types, `parsePool`, `loadCategories` and helpers. `pool.test.ts` on the real `app/data/` files and on `fixtures/categories.json`: category order equals `categories.load()` output (compare once with a throw-away `python3 -c` dump, not committed), `broadOf`/`categoryOf` on a few known subcategories.
3. **`selection.ts` + fixture replay**: port as above; `selection.test.ts` replays every case in `fixtures/selection.json` (`in_range`, `assign`, `supply`, `draw` with `tapeRng`, incl. `keep`, `avoid_categories`, `n` < 4, unfillable → `null`) and requires each tape to be used up. Gaps found in the fixtures go back to plan 18''s recorder (re-record, don''t hand-edit fixtures).
4. **Invariant tests + docs**: `invariants.test.ts` on the real `app/data/pool.json` (skipped with a message if absent), ~50 `seededRng` seeds: random burned subsets (only where `supply` reports no missing), a 12-level walk drawing 4 cards per level with `offered` excluded and `avoidCategories` from earlier picks; check every level gets 4 distinct cards in range, no burned or already offered ID ever appears, and supply with no shortage never leads to a `null` draw. Runs in a few seconds. Then `plans/12-client-engine.md` (PORT-2 `[x]` with a note), `directory.md` (`app/client/src/engine/`), AGENTS.md Commands (`npm test`), README.md if it lists npm commands.

## Done when
- `npm test` (root) runs all engine tests and passes; every `selection.json` case replays identically with its tape fully consumed.
- Invariant tests pass: every level 4 cards, burned never return.
- `npm run check` and `npm run build` pass; no new entries in `package.json` dependencies.
- Engine modules import nothing outside `src/engine/` and `src/lib/types.ts`, and nothing from `node:`.', '2026-10-12T00:00:50Z', 56);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (20, 2, 'Engine game state machine (PORT-3)', 600, 'The TypeScript referee: `app/client/src/engine/game.ts` ports `app/server/game.py` (state machine, players, burns, jokers, budget, undo) and the game routes of `app/server/main.py`, so the same requests give the same responses and leave the same saved data. It builds on part 2 (plan 19: `rng.ts`, `pool.ts`, `selection.ts`) and replays every `fixtures/game/*.json` scenario of plan 18 (PORT-1). It also defines the save document that part 4 (task 58) stores and migrates into. Source: `plans/12-client-engine.md`, PORT-3.

## Depends on
- Plan 18: `fixtures/game/*.json` (`steps: [{now, call, args, tape, response, db}]`), `fixtures/categories.json`, `fixtures/pools/*.json`.
- Plan 19: `Rng`/`tapeRng`, `PoolQuestion`, `loadCategories`, `broadOf`, `categoryOf`, `byId`, `selection.ts` (`available`, `assign`, `draw`, `supply`, `inRange`, `LEVELS`, `PER_LEVEL`, `LEVEL_RANGES`), the `node:test` setup.

## Decisions taken here
- **Save document = the SQLite tables as JSON** (the fixtures'' `db` snapshot plus `version`):
  - `SaveData {version: 1, players: PlayerRow[], games: GameRow[], burned: BurnRow[]}`
  - `PlayerRow {id, name, created_on}`; `GameRow {id, started_on, finished_on, result, player_id, state: GameState}` (state as an object, not a JSON string); `BurnRow {question_id, player_id, game_id, burned_on}` (`player_id` null = everyone, D-28).
  - `GameState`: the fields of the `game.py` docstring (`level`, `phase`, `options`, `offered`, `current`, `answers`, `history`, `last`, `undo`, `purged`, `hints_shown`, `struck`, `jokers`, `swapped_to`, `repeat`, `settings`), unchanged names (snake_case), so the migration (part 4) copies rows 1:1 and fixture `db` compares directly.
  - Part 4 owns `version` handling, stores and migration; this plan only exports the types, `SAVE_VERSION = 1` and `emptySave()`.
  - IDs like SQLite `INTEGER PRIMARY KEY` without AUTOINCREMENT: `max(id) + 1`, `1` when empty (IDs are reused after a delete; the `players` scenario pins it).
  - Burn uniqueness like `burned_once` + `INSERT OR IGNORE`: no second row with the same `question_id` and the same `player_id` (null equals null).
  - `withDefaults(state)` on every read of a game (like `latest()`), written back only when the action saves.
- **Pure API, mutable inside.** Public functions take `(save, data, io, …)` and return `{save, …}`; the input is never changed. Internally `transact(save, fn)` works on `structuredClone(save)` (= the open SQLite transaction) so the port can mutate like Python; a thrown `GameError` discards the clone (= rollback). `trial` (savepoint) = run on a clone of the working copy, return the message or `null`, discard.
- **Inputs, no globals.** `data = {pool, byId, categories, broad}` built once per pool by `engineData(pool, categories)`; `io = {rng: Rng, now: string}` per action (the Python `now()` calls within one request all read `io.now`). Nothing reads `Math.random` or the clock.
- **No seed in the game state.** Python''s randomness isn''t reproducible either, and a seed field would break `db` equality with the fixtures. Production passes `seededRng(randomSeed())` per action (part 5).
- **`engine/api.ts` mirrors `main.py`''s routes**, so part 5 swaps `lib/api.ts` with the least change and the replay compares `{status, body}` as recorded:
  - `getGame(save, data, io, player?)` → `200 {game, supply}` | `400 {error}` (view first, then supply, like `do_GET`).
  - `getPlayers(save)` → `200 Player[]`; `deletePlayer(save, body)` → `200 Player[]` | `409 {error}`.
  - `gameAction(save, data, io, action, body)` → `200 {game, event?}` | `409 {error, supply}` (`supply` = the report for supply failures, else `null`) | `404 {error: "not found"}`.
  - Argument coercion like `game_action`: `int(…)` for `index` (numbers truncate, bools → 0/1, numeric strings), `bool(…)` / truthiness for `everyone` and `purge`, `str(…)` for the joker name (missing → `"None"`, so «no joker ''None''»). What raises in Python (→ 500) throws a plain `Error` in TS; fixtures contain no 500.
  - Joker args: only `purge`, `subcategory`, `index` are passed; extra ones are ignored (Python would 500; not in fixtures).
- **Reuse `lib/types.ts`** for the responses (`Game`, `Jokers`, `JokerEvent`, `Player`, `Supply`, `JokerBudget`, `JokerName`); the save/state types live in the engine. No change to `Game`''s shape.
- **Decision entry** (next D number in `plans/decisions.md`): the client holds the correct answer and all hints in memory (the engine runs in the browser); relaxes D-25/D-26 "the client never learns the correct answer". Acceptable for an offline family game (devtools only spoil your own game). The view (`Game`) still carries no correct answer before the final answer and only the hints played; screens only render the view, never `PoolQuestion` or the save. Update `12-client-engine.md` "The referee question" to point to it.

## Files
- `app/client/src/engine/state.ts`: `SaveData`, `PlayerRow`, `GameRow`, `BurnRow`, `GameState`, `HistoryEntry`, `SAVE_VERSION`, `emptySave()`, `withDefaults`, `nextId`.
- `app/client/src/engine/pycompat.ts`: the few Python semantics the port needs: `casefold` (`toLowerCase` + `ß`→`ss`, `ς`→`σ`; pinned by the `players` scenario), `pyLen` (code points: `[...s].length`, for the 30-letter name limit), `pySplitJoin` (`" ".join(s.split())`), `pyRepr` (quotes like `repr(str)`), `pyTruthy`, `pyInt`, `pyStr`.
- `app/client/src/engine/game.ts`: `GameError {message, details}`, `cleanName`, `players`, `deletePlayer`, `supply`, `newGame`, `pick`, `answer`, `skip`, `undo`, `abandon`, `setJokers`, `joker` (+ `playHint`, `playSkip`, `playEasier`, `playCategory`, `playSnipe`), `jokersLeft`, `jokersView`, `view`; constants `JOKERS`, `UNLIMITED`, `CARDS`, `SPENT` (Spanish messages verbatim, English ones too: fixtures compare them).
- `app/client/src/engine/api.ts`: the routes above.
- `app/client/src/engine/game.test.ts`: fixture replay; `engine/test/save.ts`: normalize for comparison.

## Parity details
- Rng sites and order (plan 18): `pick` and `swap_in` shuffle `[answer, ...wrong_answers]`; `draw` shuffles once per call; `replacement` shuffles only when the later levels fill (`fill` ok), even an empty list.
- `jokersView` order: trial hint, skip, easier, snipe (index = correct answer: worst case), skip+purge; then per category in `categories` order, per subcategory: skip the current subcategory (short-circuit, no shuffle), else `replacement(…, order 0, shared fill)`. Spent jokers are still tried, then overwritten with the `SPENT` reason.
- `view` only builds `jokers` when `result` is null, phase `question` and `current` is in the pool; `GET` calls `view`, so its tape has these shuffles too.
- `undo` works on the newest game unless `abandoned`, also on a `won`/`lost` one: result and `finished_on` go back to null (the game reopens); un-burns only `(last.question_id, pid, gid)`; keeps the current `settings`.
- `answer`: `before = {...clone(state), undo: null}`; `correct_index` = first index of the answer.
- `newGame`: supply check (409 with report) before anything else; a running game becomes `abandoned`; new player row only if no casefold match.
- `deletePlayer`: their games (also a running one) and their burns go; global burns stay.
- `players()`: sort by `max(started_on)` of their games, else `created_on`, descending; ties by player `id` (fixtures avoid ties).
- `setJokers`: budget must be a plain object (not array/null) with known keys; values `null` or integers 0–99, bools rejected.
- `playSnipe` index check: `Number.isInteger`; Python also accepts `true`/`false` as 1/0 (only matters if a fixture has it).
- Sorts: `Array.prototype.sort` is stable like Python''s; booleans false before true; keys `-difficulty`, `abs(Δdifficulty)`, `0`.
- Pool IDs missing from the pool: `view` skips them like Python; actions throw a plain `Error` (Python: KeyError → 500).

## Replay (`game.test.ts`)
- Per scenario: `save = emptySave()`, `data = engineData(fixture pool, fixture categories)`; per step `io = {rng: tapeRng(step.tape), now: step.now}`; call the `api.ts` route for `step.call` with `step.args`.
- Compare deep-equal (object key order ignored, array order exact): `{status, body}` with `step.response`; `{players, games, burned}` of the new save with `step.db` (both `burned` sorted by `(game_id, question_id, player_id)`, null first); `tape.done()`.
- On a 409/400 the returned save must equal the previous one.
- A mismatch is fixed in the engine; a fixture gap goes back to plan 18''s recorder (re-record, never hand-edit fixtures).

## Tasks to split into
1. **State and helpers**: `state.ts`, `pycompat.ts`, `transact`/`trial`, `engineData`; decision entry; `12-client-engine.md` referee section. Check: `npm run check`; a few `pycompat` asserts in a throw-away script.
2. **Game actions**: `game.ts` without jokers: players, names, delete, supply, new, pick, answer, skip (player/everyone), undo, abandon, `setJokers`, `jokersLeft`, `view` with `jokers: null` stubbed only until task 3.
3. **Jokers**: the five `play*`, `replacement`, `laterFill`, `categoryCandidates`, `swapIn`, `joker` (budget/`SPENT`), `jokersView` in `view`.
4. **`api.ts` + fixture replay**: routes and coercion as above; `game.test.ts` replays every `fixtures/game/*.json` (scripted and soak) until all pass with tapes used up. Then `plans/12-client-engine.md` PORT-3 `[x]` with a note, `directory.md` (engine files).

## Done when
- `npm test` passes, including every `fixtures/game/*.json` step: same response, same save, tape fully consumed.
- `npm run check` and `npm run build` pass; no new dependencies.
- Engine modules import nothing outside `src/engine/` and `src/lib/types.ts`, and nothing from `node:`.
- Decision entry written; screens untouched (part 5 wires them, task 59).', '2026-10-12T00:03:19Z', 57);

INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (1, 1, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, plan 1 body; plans/decisions.md (D-52), plans/open-questions.md, plans/project.md (OQ-17 resolved)', 'Write plan 1, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T20:08:18Z', '2026-10-11T23:15:56Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (2, 2, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, tasks.sql (plan 2 body)', 'Write plan 2, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', '2026-10-11T23:55:45Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (3, 3, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 3, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (4, 4, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 4, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (5, 5, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 5, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:56Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (6, 6, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 6, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:56Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (7, 7, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 7, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:56Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (8, 8, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 8, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (9, 9, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 9, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (10, 10, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 10, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (11, 11, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 11, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (12, 1, 'create tasks for plan 1', 'split', 'done', 1000, '2026-10-11, tasks 13–18 (plans for parts 1–6), decisions 1–3 (difficulty targets, QC threshold, needs_work handling)', 'Split plan 1 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:15:47Z', '2026-10-11T23:16:53Z', 1);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (13, 1, 'write plan: targets and progress', 'plan', 'done', 1000, '2026-10-11, plan 12 (Targets and progress), plans/decisions.md (D-53)', 'Write the plan for part 1 of the masterplan (plan 1): `pm plan add 1 "Targets and progress" --priority 700`.

- Target count per difficulty 1–15, summing to 5000: decision 1. Store them where `qgen` and the authoring server can read them (e.g. a file under `authoring/data/` or `app/data/age-groups.json`; pick and log a D-entry).
- Progress view: approved vs. target per difficulty and per category in `qgen report` and `/stats/difficulty`.
- The milestone''s exit check: ≥ 5000 approved, every level at target, quality criteria from decision 2 (spot-check size, agreement rate) and part 4''s thresholds.
- Tasks that need decision 1 or 2: link them with `pm task-pending-decision`.', '2026-10-11T23:16:50Z', '2026-10-11T23:39:30Z', 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (14, 1, 'write plan: aim batches at difficulty gaps', 'plan', 'done', 1000, '2026-10-11, plan 13 (Aim batches at difficulty gaps), plans/decisions.md (D-54), plans/backlog.md (B-6)', 'Write the plan for part 2 of the masterplan (plan 1, B-6): `pm plan add 1 "Aim batches at difficulty gaps" --priority 700`.

- `draft` draws target difficulties weighted by the gap to part 1''s targets (decision 1), not evenly (D-40); subcategory choice should consider difficulty gaps too.
- Measure first: target vs. rated vs. reviewed difficulty for batch-7 and batch-8; where do 11–15 targets land?
- Fix prompts or concept `known_at` choice where hard drafts come out at 7–9. These are implementation tasks on `qgen.py`/prompts, never workarounds inside a batch run (RUNBOOK).
- Depends on part 1''s target storage; refer to that plan once it exists (`pm plan list`).', '2026-10-11T23:16:50Z', '2026-10-11T23:41:40Z', 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (15, 1, 'write plan: more subcategories', 'plan', 'done', 1000, '2026-10-11, plan 14 (More subcategories)', 'Write the plan for part 3 of the masterplan (plan 1): `pm plan add 1 "More subcategories" --priority 600`.

- Find saturated `base` subcategories: approved count, concept-list use, duplicate rate, avoid-list length.
- Propose new subcategories, especially ones that carry hard (11–15) questions, with draft concept lists.
- Which ones to add is the gamemaster''s call (RUNBOOK): the plan''s analysis task raises a decision with the proposals as options; the task that adds them to `app/data/categories.json` waits for it.', '2026-10-11T23:16:50Z', '2026-10-11T23:43:52Z', 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (16, 1, 'write plan: duplicate and drift detection', 'plan', 'done', 1000, '2026-10-11, pm plan 15; plans/decisions.md (D-55), plans/backlog.md (B-5), plans/20-pipeline-efficiency.md (PE-6, PE-13), plans/23-media-providers.md (MP-11), plans/project.md', 'Write the plan for part 4 of the masterplan (plan 1, B-5; absorbs PE-6, PE-13, MP-11): `pm plan add 1 "Duplicate and drift detection" --priority 700`.

- Pre-merge overlap check of drafts against the whole approved pool by answer, concept and topic, not only question text (`dedupe`), so overlaps get dropped instead of ending up `needs_work` (cf. q-0644/q-0957, q-0646/q-0217, q-0689/q-0279).
- Per-batch health metrics in `authoring/reports/<batch>.md` and a cross-batch comparison: drop rate, needs_work rate by reason, duplicate rate, difficulty spread vs. targets, axis/style variety, cost per approved question.
- Thresholds that say "stop and look before the next batch"; they feed the milestone''s exit check.
- Close or update PE-6, PE-13, MP-11, B-5 in `plans/backlog.md` as the plan covers them.', '2026-10-11T23:16:50Z', '2026-10-11T23:46:07Z', 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (17, 1, 'write plan: quality control after every batch', 'plan', 'done', 1000, '2026-10-11, pm plan 16, plans/decisions.md (D-56)', 'Write the plan for part 5 of the masterplan (plan 1): `pm plan add 1 "Quality control after every batch" --priority 650`.

- (a) LLM audit with its own prompt (not `review.md`) on a sample of a batch: facts, ambiguity, giveaways, difficulty, house style; results into the batch report.
- (b) Human spot check: random sample in the review tool (e.g. a sample filter on `/review?batch=…`), recording agree/disagree with the LLM verdict. Sample size and agreement rate: decision 2.
- (c) Procedure that turns findings into prompt or house-style changes before the next batch; documented in `authoring/RUNBOOK.md` or a plan file.
- Trend over batches of the human/LLM disagreement rate.
- Only the tooling and procedure; the QC runs themselves are tasks of part 6.', '2026-10-11T23:16:50Z', '2026-10-11T23:48:22Z', 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (18, 1, 'write plan: batch runs', 'plan', 'done', 1000, '2026-10-11, tasks.sql (plan 17: Batch runs)', 'Write the plan for part 6 of the masterplan (plan 1): `pm plan add 1 "Batch runs" --priority -100`.

- Plan priority -100: every task that runs `qgen batch` must run only after all implementation work (milestone 1).
- First tasks: finish batch-8 (`work/batch-8`, commit d7fb13f) per `authoring/RUNBOOK.md`, then its QC (part 5''s procedure, once that exists), then the next batch. Add batch tasks one or two at a time, not all ~8 up front; the plan says that each batch task adds the next one while targets (part 1) are unmet.
- needs_work handling per decision 3 (RUNBOOK: `qgen rework` only on the gamemaster''s word).
- Watch media yield; if missing media limits throughput, propose a new plan with `plans/06-images.md`, `plans/23-media-providers.md`, IMG-16/17.
- Last task: the exit check from part 1, plus `qgen validate` and `trivia-media sync --status approved`.', '2026-10-11T23:16:50Z', '2026-10-11T23:49:37Z', 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (19, 12, 'create tasks for plan 12', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 25–28; 25–27 wait for decision 1, 28 for decisions 1 and 2)', 'Split plan 12 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:39:28Z', '2026-10-11T23:50:10Z', 13);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (20, 13, 'create tasks for plan 13', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 29–36; 33 dropped as duplicate of 34; 35, 36 wait for decision 1; 32 waits for the anchor decision task 34 creates)', 'Split plan 13 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:41:37Z', '2026-10-11T23:51:08Z', 14);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (21, 14, 'create tasks for plan 14', 'split', 'done', 1000, '2026-10-11, tasks 37–39 for plan 14; no upfront decision (task 38 creates the proposal decision, task 39 waits for it)', 'Split plan 14 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:43:50Z', '2026-10-11T23:51:42Z', 15);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (22, 15, 'create tasks for plan 15', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 40–45; 43 dropped, re-added as 45 with task 44''s id; plan tasks 4+5 merged into 45; 44 waits for decision 1 and the threshold decision 45 creates)', 'Split plan 15 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:45:50Z', '2026-10-11T23:52:42Z', 16);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (23, 16, 'create tasks for plan 16', 'split', 'done', 1000, '2026-10-11, tasks 46–49 (48 pending on decisions 1, 2)', 'Split plan 16 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:48:16Z', '2026-10-11T23:53:40Z', 17);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (24, 17, 'create tasks for plan 17', 'split', 'done', 1000, '2026-10-11, tasks 50–53; plan 17 body: QC task also waits on the proposals decision', 'Split plan 17 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:49:34Z', '2026-10-11T23:54:45Z', 18);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (25, 12, 'Targets file, loader and validate check', 'work', 'open', NULL, NULL, 'Part "Targets file" of plan 12 (D-53, already logged in `plans/decisions.md`).

- New `authoring/data/targets.json`: `{"about": "…", "base": {"total": 5000, "difficulty": {"1": n, …, "15": n}}}`, numbers from pm decision 1.
- Loader `load_targets(bundle)` in `authoring/tools/` (in `qgen.py`, or a small `targets.py` if the authoring server will import it too, see the `/api/targets` task); returns `None` for a bundle without targets.
- Helper for the derived per-category share: `total × subcategories in category / subcategories in bundle` (guide only).
- `qgen validate`: levels = the scale in `app/data/age-groups.json`, every value ≥ 0, sum = `total`.
- `directory.md`: line for the new file.

Done when: `qgen validate` passes; a throw-away edit (wrong sum, missing level) makes it fail.', '2026-10-11T23:50:08Z', NULL, 19);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (26, 12, 'qgen report: progress vs. targets', 'work', 'open', NULL, NULL, 'Part "Progress view" of plan 12, CLI side. Needs the targets file and loader (previous task).

- `qgen report`: new section "progress vs. targets (base)": per difficulty `approved / target`, missing count, percent; a total line; per broad category `approved / derived share`.
- Approved = status `approved`, bundle `base`, regardless of burns.
- `--bundle <id>` for another bundle with targets; skip the section quietly when the bundle has none.

Done when: `qgen report` prints the section with today''s numbers (well under target at 9–15).', '2026-10-11T23:50:08Z', NULL, 19);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (27, 12, '/api/targets and target markers on /stats/difficulty', 'work', 'open', 500, NULL, 'Part "Progress view" of plan 12, authoring server and UI. Needs the targets file and loader.

- Authoring server: `GET /api/targets` (the file as JSON); doc line in `authoring/server/main.py`''s docstring.
- `fetchTargets` in `authoring/ui/src/lib/api.ts`, type in `lib/types.ts`.
- `/stats/difficulty` (`authoring/ui/src/stats/DifficultyChart.svelte`): a target marker per bar (tick or outline) and `approved / target` in the bar''s label, when the selected bundle has targets.
- `/stats/categories`: approved vs. derived share per broad category, only if it fits the existing chart without a redesign; otherwise leave it to `qgen report`.

Done when: `npm run check` clean; the page shows the markers in the browser with `trivia-authoring`.', '2026-10-11T23:50:08Z', NULL, 19);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (28, 12, 'Exit check for milestone 1', 'work', 'open', 640, NULL, 'Part "Exit check" of plan 12. Runs after the tooling of plan 15 (per-batch health metrics, `authoring/reports/<batch>.md`) and plan 16 (human spot-check records); priority 640 puts it after both.

- `qgen report --exit-check` (or `qgen milestone`; pick what fits `qgen.py`''s CLI): one line per criterion, ✓/✗, exit 1 if any fails:
  - approved `base` ≥ 5000;
  - every difficulty ≥ its target;
  - the last two committed `base` batches pass plan 15''s thresholds;
  - the last two batches'' human spot checks agree with the LLM review at decision 2''s rate, with at least its sample size (records from plan 16);
  - `qgen validate` clean.
- Reads the metrics and spot-check records; doesn''t compute them. Missing data → "not available", counts as ✗.
- `plans/16-content-target.md` "Quality bar": write decision 2''s numbers as the family pool''s bar; close CT-5 for the family pool.

Done when: the check runs and, today, fails on the count criteria with the right numbers.', '2026-10-11T23:50:08Z', NULL, 19);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (29, 13, 'qgen report --calibration and baseline', 'work', 'open', 710, NULL, 'Part "Measurement" of plan 13. The baseline comes first, so the fixes can be measured.

- `qgen report --calibration [<batch>…]` in `authoring/tools/qgen.py`: per target level 1–15: n drafted, mean drafted / rated / final difficulty, mean concept `known_at`, merged and approved counts.
- Reads `work/<batch>/slots.json`, `drafts/`, `ratings/`, `ids.json` and the pool; default: the last two batches. Missing ratings (batch not rated yet) → `–`, no error.
- Write it so plan 16''s batch health metrics ("difficulty spread vs. targets") can call the same function; don''t build it twice.
- Record the batch-7 and batch-8 numbers in plan 13''s "Baseline" section (`pm plan edit 13 --body -`); batch-8 rated numbers once it''s rated, else note that they''re pending.
- `README`/`AGENTS.md` command lists: mention the flag where `qgen report` is listed.

Done when: `qgen report --calibration` prints the table for batch-7 and batch-8, matching the throw-away baseline in plan 13 (±0.1); `qgen validate` clean.', '2026-10-11T23:50:50Z', NULL, 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (30, 13, 'rate.md on the 1–15 scale; re-check DIFFICULTY_GAP', 'work', 'open', NULL, NULL, 'Part "Fixes → Rater scale" of plan 13. `authoring/tools/prompts/rate.md` asks for `difficulty_estimate` 1–10, so the rater can''t rate above 10 and every question at 13+ looks overrated to `revise` (`DIFFICULTY_GAP = 3`, `qgen.py`).

- `rate.md`: `difficulty_estimate` on the shared scale 1–15, as defined in the house style (refer to it, don''t restate it); fix the JSON schema bounds in `qgen.py` if the rating schema has them.
- Re-check `DIFFICULTY_GAP`: with a throw-away script, re-rate ~20 approved questions at 10–15 (few LLM calls; no batch run) and compare estimate vs. stored difficulty. Keep 3 or change it with a short reason in the comment; log a decision in `plans/decisions.md` if the meaning changes.

Done when: rate prompt and schema allow 1–15; the throw-away check shows estimates above 10 for hard questions; `qgen validate` clean.', '2026-10-11T23:50:50Z', NULL, 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (31, 13, 'Concept draw follows known_at', 'work', 'open', NULL, NULL, 'Part "Fixes → Concept draw" of plan 13. `concepts.draw_concepts` (`authoring/tools/concepts.py`) weights `1/(1+uses)² / (1+|known_at−d|/2)`; use count dominates, so mean `known_at` per target sits at 7–9 for targets 1–8 and ~11 for 13–15.

- Draw from a window: concepts with `|known_at − d| ≤ 1`, widen to ±2, ±3 … only when the window has no unused, unretired concept left; use count breaks ties inside the window. Retired concepts never (unchanged).
- Keep the signature, so `draw_slots` and the focus-group path keep working; update the docstring (D-38).
- Throw-away check: a seeded dry run of `draw_slots` (no LLM calls) over the base subcategories; mean `known_at` per target within ±1 at every level 1–15, or report the levels where the supply runs out.

Done when: the dry-run numbers are in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:50:50Z', NULL, 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (32, 13, 'Write the confirmed difficulty anchors into the house style', 'work', 'open', 690, NULL, 'Second half of "Fixes → Prompts" of plan 13. Waits for the gamemaster''s answer to the anchor decision the previous task creates.

- Add the confirmed anchors (questions at 9–15 with the gamemaster''s levels) to the calibration section of `authoring/tools/prompts/house-style.md`, next to the existing 1–6 examples; levels as the gamemaster answered, not as proposed.
- Where the gamemaster corrected a level, set it on the question in `authoring/data/questions.json` only via the existing tooling (not by hand); if there''s none, log it in `plans/backlog.md`.

Done when: house style has anchors spread over 9–15; `qgen validate` clean.', '2026-10-11T23:50:50Z', NULL, 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (33, 13, 'Hard-question guidance in draft.md and house style; propose anchors', 'work', 'dropped', NULL, 're-added as the next task with the follow-up task id filled in', 'First half of "Fixes → Prompts" of plan 13. Hard targets are drafted ~3 levels low; house style''s calibration examples are all at 1–6 and all say "AI guessed too high".

- `authoring/tools/prompts/house-style.md`: what makes a question hard on the 1–15 scale (who can answer it: few adults, specialists; not obscure trivia nobody could know).
- `authoring/tools/prompts/draft.md`: the ±1 tolerance must not become a habit of rounding down; aim at the target, not below it.
- Anchor candidates: pick ~8 approved questions at 9–15 (spread over levels and broad categories) and propose them with `pm decision add "Difficulty anchors 9–15: are these levels right?" --body …` (id, question, answer, stored level each; options e.g. "levels as proposed" / "corrections in the answer"). Then `pm task-pending-decision TASK_4B <decision id>` so the follow-up task waits for the answer.
- Don''t write the anchors into the house style here.

Done when: prompts updated, decision created and task TASK_4B pending on it; `qgen validate` clean; no batch run.', '2026-10-11T23:50:50Z', '2026-10-11T23:51:05Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (34, 13, 'Hard-question guidance in draft.md and house style; propose anchors', 'work', 'open', NULL, NULL, 'First half of "Fixes → Prompts" of plan 13. Hard targets are drafted ~3 levels low; house style''s calibration examples are all at 1–6 and all say "AI guessed too high".

- `authoring/tools/prompts/house-style.md`: what makes a question hard on the 1–15 scale (who can answer it: few adults, specialists; not obscure trivia nobody could know).
- `authoring/tools/prompts/draft.md`: the ±1 tolerance must not become a habit of rounding down; aim at the target, not below it.
- Anchor candidates: pick ~8 approved questions at 9–15 (spread over levels and broad categories) and propose them with `pm decision add "Difficulty anchors 9–15: are these levels right?" --body …` (id, question, answer, stored level each; options e.g. "levels as proposed" / "corrections in the answer"). Then `pm task-pending-decision 32 <decision id>` so task 32 (writes the anchors in) waits for the answer.
- Don''t write the anchors into the house style here.

Done when: prompts updated, decision created and task 32 pending on it; `qgen validate` clean; no batch run.', '2026-10-11T23:51:06Z', NULL, 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (35, 13, 'Deficit weights in target_weights()', 'work', 'open', NULL, NULL, 'Part "Aim at gaps" of plan 13 (D-54), first step. Needs plan 12''s targets file and loader (task 25, same decision).

- `target_weights()` in `authoring/tools/qgen.py`: with targets for the batch''s bundle (`load_targets(bundle)`), weight per level = `max(0, target − approved)`; approved = status `approved` in that bundle. Even weights (D-40) when the bundle has no targets or every deficit is 0; the focus-group path (`LEVEL_WEIGHTS`) unchanged.
- Print the drawn target histogram at the start of `draft`, so the batch log shows the batch''s shape.
- Throw-away check: seeded dry run of `draw_slots` (no LLM calls) draws targets roughly proportional to the deficits.

Done when: dry-run histogram in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:51:06Z', NULL, 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (36, 13, 'Subcategory ranking and per-subcategory targets by deficit and concept supply', 'work', 'open', 690, NULL, 'Part "Aim at gaps" of plan 13 (D-54), second step. After the `target_weights()` task.

- `batches.subcategories()` (`authoring/tools/batches.py`, shared with the authoring start page): rank by `Σ_level approved(sub, level) × deficit_share(level)`, ties as now; still `batches.SHARE` of the subcategories (D-46); no new `qgen batch` arguments (D-36). Without targets: ranking as today.
- `assign_difficulties`/`draw_slots` (`qgen.py`): hand each subcategory the targets its concept list can carry (unused, unretired concepts with `known_at` near the target) instead of a plain shuffle; a subcategory without hard concepts gets no 15s.
- Check the authoring start page still shows the next batch''s subcategories (`trivia-authoring`).
- Throw-away check: seeded dry run of `draw_slots`: targets weighted by deficit, mean concept `known_at` per target within ±1 (plan 13 "Done when").

Done when: dry-run numbers in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:51:06Z', NULL, 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (37, 14, 'qgen report --subcategories with saturation flags', 'work', 'open', NULL, NULL, 'Part 1 of plan 14: the check that spots saturated subcategories.

- Add `qgen report --subcategories [--bundle <id>]` (`authoring/tools/`), next to plan 13''s `--calibration` code (task 29); share its loading/counting helpers, don''t duplicate them.
- One row per subcategory: approved, asked (all statuses = avoid-list length), concept-list size, unused, unused at `known_at` ≥ 11, top-ups so far, overlaps (merge duplicate drops + review needs_work for overlap, last two batches). Reuse plan 15''s overlap counts if they exist by then; otherwise count from batch logs/review notes once, in a helper plan 15 can reuse.
- One row per broad category: subcategories, approved, unused hard concepts.
- Flag **saturated** when any holds: unused < 36 right after a top-up; unused at `known_at` ≥ 11 < 10; overlaps ≥ 10 % of its drafts in the last batch; asked ≥ 60. Tune these against the real numbers.
- Subcategories without a concept list yet: show them as "no list", not saturated.
- Record the baseline output (short summary) and the tuned thresholds in plan 14''s body (`pm plan edit 14 --body -`; keep the rest of the body as is).

Done when: the report prints both tables with flags for `base` and `--bundle colombia`; plan 14 holds baseline and thresholds; `qgen validate` clean.', '2026-10-11T23:51:37Z', NULL, 21);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (38, 14, 'Proposal round: new base subcategories', 'work', 'open', NULL, NULL, 'Part 2 of plan 14. No changes to `categories.json` here.

- Run `qgen report --subcategories` (task above).
- Write 10–20 proposals by plan 14''s "Proposals" rules: sources (a) saturated subcategories (split or neighbour), (b) broad categories with ≤ 3 subcategories (Espacio, Cuerpo humano, Fiestas y tradiciones, Fútbol, Videojuegos, Amazonas, …), (c) topics with hard questions (11–15).
- Each: Spanish name, broad category, one-line scope, reason with numbers, ~10 sample concepts with `known_at` (≥ 3 at 11–15). Mark the recommended ones.
- Checks: no name or near-synonym of an existing subcategory in any bundle (D-43); no Colombia-only topic (D-49); broad enough for ≥ 100 concepts; no new broad categories.
- `did=$(pm decision add "Which new base subcategories?" --body "<proposals>" --option "add the recommended ones" --option "add all" --option "none for now")`, then `pm task-pending-decision <id of the task "Add the approved base subcategories"> "$did"`.

Done when: the decision exists with the proposals and the add task waits for it.', '2026-10-11T23:51:37Z', NULL, 21);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (39, 14, 'Add the approved base subcategories', 'work', 'open', NULL, NULL, 'Part 3 of plan 14. Waits for the decision "Which new base subcategories?" (created by the proposal-round task); read the answer in `pm show`. If the answer is "none for now", drop this task.

- Add the approved subcategories to `app/data/categories.json`, each in its broad category, with the scope from the proposal.
- Create their concept lists: `qgen concepts --subcategories "<names>"` (one Opus call per list; not a batch run).
- Log a QP entry in `plans/02-question-pool.md` (what was added, why, counts).
- `qgen validate` clean (also re-export `app/data/pool.json` if validate asks).

Done when: the subcategories are in `categories.json` with concept lists, QP entry written, `qgen validate` clean.', '2026-10-11T23:51:37Z', NULL, 21);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (40, 15, 'Overlap candidate finder and qgen report --overlaps', 'work', 'open', 710, NULL, 'Part "Overlap check before merge" (B-5) of plan 15, code only, no LLM. Shapes the next batch most, so it runs first.

- Candidate finder in `authoring/tools/qgen.py` or a small `authoring/tools/overlap.py`: for a draft, pool questions of every bundle (status ≠ `rejected`) and earlier drafts of the same batch where:
  - normalized answers equal or similar (`SequenceMatcher` ≥ 0.8, or one contains the other); numbers and yes/no excluded as in `duplicates()`;
  - draft''s concept or answer stem-matches the other''s concept or answer (lowercase, no accents, drop trailing «s»/«es»);
  - draft''s concept or answer occurs in the other''s question or `fun_fact`, or the other way round.
  - Cap ~8 per draft, closest first. No new dependencies. `duplicates()` stays as is.
- `qgen report --overlaps`: the same finder over the approved pool, pairs listed (ids, answers, why matched); listing only. Mention the flag where `qgen report` is listed (README, AGENTS.md).
- Replay (throw-away script): batch-7''s merged questions against the pool before batch-7 (ids < q-0596) must list q-0646/q-0217, q-0644/q-0957, q-0689/q-0279, q-1210/q-0315; B-5''s q-0369/q-0341 and q-0420/q-0328 against their pools. Record recall and candidates per draft (mean, max) in plan 15''s Baseline (`pm plan edit 15 --body -`).
- Not wired into `rate` yet (next task).

Done when: replay finds all six pairs, numbers in plan 15; `qgen validate` clean; no batch run.', '2026-10-11T23:52:31Z', NULL, 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (41, 15, 'no_overlap criterion in rate; drop overlaps at merge', 'work', 'open', NULL, NULL, 'Part "Judge in rate" of plan 15. After the candidate finder task.

- Check `work/batch-8` first: if batch-8 is between `draft` and `merge` (rated partly or not yet merged), don''t change `rate`/`merge` now; stop and note it (plan 17''s batch-run task finishes batch-8 first).
- Grouped `rate` call (PE-1) in `authoring/tools/qgen.py`: each draft''s candidates (id, question, answer, concept) in the payload; new hard criterion `no_overlap` in the rating schema and `authoring/tools/prompts/rate.md` (5 = asks a different fact; ≤ 3 = knowing one answer gives the other away, or the same fact again). Within-batch pairs: the later draft fails.
- `merge`: a `no_overlap` hard fail is dropped with reason `overlap like q-…` in `dropped.json`; the concept isn''t retired.
- Prompts are changed here as an implementation task, never inside a batch run (RUNBOOK).
- Check (throw-away script, two LLM calls): rate ~20 batch-7 drafts incl. the four known overlaps, once without and once with candidates; the four fail `no_overlap`, the others don''t. Result in the task note.

Done when: check passes; `qgen validate` clean; no batch run.', '2026-10-11T23:52:31Z', NULL, 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (42, 15, 'Needs-work problems in review and record; classifier for old questions', 'work', 'open', NULL, NULL, 'Part "Needs-work reasons" of plan 15. Today `needs_work` reasons are only free text in `review.feedback`.

- `REVIEW_SCHEMA` (`authoring/tools/qgen.py`): `problems`, array of `giveaway`, `fact`, `ambiguity`, `overlap`, `media`, `difficulty`, `style`, `other`; stored in `q.review.problems`. One shared constant; plan 16''s audit task may already have defined it: reuse it.
- `record`: adds `media` (no adequate media) and `fact` (fact check not confirmed) for the fixed rules.
- `authoring/tools/prompts/review.md`: when to use each problem.
- Keyword classifier for questions without `problems` (`No se encontró una imagen adecuada` → media, `q-\d{4}` → overlap, `pista` + `regala|delata|da la respuesta` → giveaway, …), results marked as guessed; for the reports only, no backfill into the pool.
- `qgen validate`: `problems` values from the list when present.

Done when: classifier run over batch-7''s needs_work (throw-away script) gives counts per problem, in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:52:31Z', NULL, 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (43, 15, 'Batch health: health.py, qgen report --batches, Health section, baseline; propose thresholds', 'work', 'dropped', 690, 're-added as the next task with task 44''s id filled in', 'Part "Batch health" of plan 15, plus the threshold decision (plan''s tasks 4 and 5). After the problems task (needs_work by problem) and the no_overlap task (overlap drops); without them those rows read "n/a".

- `authoring/tools/health.py`: `batch_health(run) -> dict` from `work/<run>/` and the pool; metrics as listed in plan 15 (drops by reason, merged/approved/needs_work, needs_work by `problems` incl. the guessed classifier, overlap rate, difficulty, variety, media share, mean `fun`, cost, calls, wall time).
- Difficulty vs. target: reuse plan 13''s `--calibration` code (task 29) if it exists; else "n/a". Approved per level vs. deficit: plan 12''s `load_targets` (task 25) if it exists; else "n/a".
- `qgen report --batches [<batch>…]` (default batch-4 onward): one column per batch.
- `batch-report`: "## Health" at the top of `authoring/reports/<batch>.md` with each metric and the previous two batches'' values (✓/✗ comes with the thresholds task); regenerates `authoring/reports/batches.md` with the same table. `directory.md`: lines for `health.py` and `batches.md`.
- Baseline: run over batch-4…7 (and batch-8 if recorded); record the table in plan 15 (`pm plan edit 15 --body -`). Close PE-6, PE-13, MP-11: numbers into `plans/20-pipeline-efficiency.md` and `plans/23-media-providers.md`, mark them `[x]`.
- Decision: `pm decision add "Batch health thresholds and stop rule?"` with the plan''s first-guess thresholds adjusted to the baseline in the body; options: recommended set (first) / looser set / warnings only, no stop. Then `pm task-pending-decision <thresholds task id> <decision id>` (the task "Batch health thresholds, stop rule and ack").

Done when: `qgen report --batches` prints batch-4…7; plan 15 has the baseline; PE-6/PE-13/MP-11 closed; decision created and the thresholds task waits on it; `qgen validate` clean; no batch run.', '2026-10-11T23:52:32Z', '2026-10-11T23:52:38Z', 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (44, 15, 'Batch health thresholds, stop rule and ack', 'work', 'open', 690, NULL, 'Part "Thresholds" of plan 15 (D-55). Waits for the threshold decision (created by the batch-health task) and for pm decision 1 via plan 12''s targets file (task 25).

- `authoring/data/targets.json`: `"batch_health"` with the decided thresholds; `qgen validate` checks the keys.
- `health.py`: ✓/✗ per metric incl. the trend rule; shown in the Health section and `batches.md`.
- `qgen batch` (`authoring/tools/qgen.py`): if the last committed batch fails a threshold and has no ack, exit 2 before `concepts`, naming the report. `qgen rework`/`tighten` not blocked. If the decision chose "warnings only", print instead of exit.
- `qgen health ack <batch> "<note>"` → `authoring/data/health-acks.json` (shown in `batches.md`; `directory.md` line). An ack clears the stop but isn''t a pass for plan 12''s exit check.
- `authoring/RUNBOOK.md`: one line in the exit-code table for 2.
- Log in `plans/decisions.md` only if the answer changes D-55.

Done when: a throw-away failing threshold makes `qgen batch` exit 2 before `concepts` (no LLM calls), and `qgen health ack` clears it; `qgen validate` clean; no batch run.', '2026-10-11T23:52:32Z', NULL, 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (45, 15, 'Batch health: health.py, qgen report --batches, Health section, baseline; propose thresholds', 'work', 'open', 690, NULL, 'Part "Batch health" of plan 15, plus the threshold decision (plan''s tasks 4 and 5). After the problems task (needs_work by problem) and the no_overlap task (overlap drops); without them those rows read "n/a".

- `authoring/tools/health.py`: `batch_health(run) -> dict` from `work/<run>/` and the pool; metrics as listed in plan 15 (drops by reason, merged/approved/needs_work, needs_work by `problems` incl. the guessed classifier, overlap rate, difficulty, variety, media share, mean `fun`, cost, calls, wall time).
- Difficulty vs. target: reuse plan 13''s `--calibration` code (task 29) if it exists; else "n/a". Approved per level vs. deficit: plan 12''s `load_targets` (task 25) if it exists; else "n/a".
- `qgen report --batches [<batch>…]` (default batch-4 onward): one column per batch.
- `batch-report`: "## Health" at the top of `authoring/reports/<batch>.md` with each metric and the previous two batches'' values (✓/✗ comes with the thresholds task); regenerates `authoring/reports/batches.md` with the same table. `directory.md`: lines for `health.py` and `batches.md`.
- Baseline: run over batch-4…7 (and batch-8 if recorded); record the table in plan 15 (`pm plan edit 15 --body -`). Close PE-6, PE-13, MP-11: numbers into `plans/20-pipeline-efficiency.md` and `plans/23-media-providers.md`, mark them `[x]`.
- Decision: `pm decision add "Batch health thresholds and stop rule?"` with the plan''s first-guess thresholds adjusted to the baseline in the body; options: recommended set (first) / looser set / warnings only, no stop. Then `pm task-pending-decision 44 <decision id>`.

Done when: `qgen report --batches` prints batch-4…7; plan 15 has the baseline; PE-6/PE-13/MP-11 closed; decision created and the thresholds task waits on it; `qgen validate` clean; no batch run.', '2026-10-11T23:52:38Z', NULL, 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (46, 16, 'LLM audit: audit.md, qgen audit, batch step, Audit section; batch-7 baseline', 'work', 'open', NULL, NULL, 'Part "LLM audit (a)" of plan 16: an independent second LLM reader of a seeded sample per batch.

- `authoring/tools/prompts/audit.md` (new): strict reader of the question as played; sees question, options, hints, fun fact, difficulty, media title/role, `related` pool questions, house style; not the review verdict, `fix`, rater notes or fact check. Checks facts (web search like `factcheck`), ambiguity, giveaways, overlap, difficulty (1–15, D-38), house style.
- `AUDIT_SCHEMA` in `authoring/tools/qgen.py`: `verdict` ok|problem, `problems` (plan 15''s shared constant; task 42 may define it first: reuse, else define it where task 42 finds it), `severity` minor|major, `difficulty_estimate` 1–15, `notes`.
- Sample draw: seeded by batch name, `AUDIT_SAMPLE` = 60 merged questions with an LLM review, approved/needs_work in proportion; one function, so task "spot-check tooling" can draw its subset from it.
- `qgen audit [--batch <b>]`: one opus call per question, `work/<batch>/audit/<id>.json`, skips done ones; never changes the pool.
- Step in `qgen batch` after `record`, before `export`. `work/batch-8` exists: if batch-8 is mid-run, make sure the new step doesn''t break resuming it.
- `batch-report`: "## Audit" section (sample size, major among approved / among needs_work, problems by kind, mean |audit − final difficulty|, audit/review agreement, every major finding on an approved question as `id: problem — notes` + `/review/<id>` link).

Done when: `qgen audit --batch batch-7` ran; flagged rates, problems by kind, cost (`costs.log`) and audit/review agreement recorded in plan 16''s Baseline (`pm plan edit 16 --body -`); `qgen validate` clean. No batch run.', '2026-10-11T23:53:37Z', NULL, 23);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (47, 16, 'Spot-check tooling: sample, spot-checks.json, endpoints, blind review mode, audit=flagged', 'work', 'open', 640, NULL, 'Part "Human spot check (b)" of plan 16. After the audit task (it provides the sample draw).

- Spot-check sample: subset of the audit sample, seeded by batch name, size `quality.spot_check_size` from `authoring/data/targets.json` (task 25''s loader) or 30 when absent.
- `authoring/data/spot-checks.json` in the format of plan 16; written only by the server; undo removes the item.
- `authoring/server/main.py`: `POST /api/spot-checks/<batch>/<id>`, `GET /api/spot-checks`, doc lines in the docstring.
- `qgen validate`: file checks (batch/ids exist, values in range).
- Review page (`authoring/ui`): `/review?batch=<b>&sample=1` blind (hide LLM decision, feedback, reasons, audit until decided; media stays visible), then reveal next to the human verdict with agree/disagree; decide = normal human review (D-33) + spot-check POST. `/review?batch=<b>&audit=flagged`: audited questions with a major finding, audit notes next to the review''s.

Done when: `npm run check` and `qgen validate` clean; checked in the browser with `trivia-authoring` on batch-7 (decide, reveal, undo; then restore any test entries).', '2026-10-11T23:53:37Z', NULL, 23);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (48, 16, 'qgen report --qc, QC section and trend table; quality keys in targets.json', 'work', 'open', 630, NULL, 'Parts "Findings → changes" step 3 and "Trend" of plan 16. Needs the spot-check file (previous task), task 25 (targets file, waits on decision 1) and pm decision 2 (spot-check size, agreement rate).

- `quality` keys in `authoring/data/targets.json`: `spot_check_size`, `min_agreement` (values from decision 2); `qgen validate` checks them.
- `qgen report --qc <batch>`: rewrites "## Quality control" in `authoring/reports/<batch>.md`: agreement, false approve / false needs_work, difficulty |Δ| ≥ 2, media changed, audit vs. human, disagreements with the human''s feedback grouped by `problems`; ends with "Changes from this QC: …" (filled in by QC step 4).
- `qgen report --qc` without batch: trend table per batch (audit n, major among approved %, human n, agreement %, false approve %, difficulty |Δ| ≥ 2 %, audit/human agreement %, ✓/✗ vs. `min_agreement`); also into `authoring/reports/batches.md` if task 45 made it.
- Output plan 12''s exit check (task 28) can read without recomputing; tell task 28 in a note if it needs a shared function.

Done when: run on batch-7 with a few throw-away spot-check entries (removed afterwards) gives plausible numbers; `qgen validate` clean.', '2026-10-11T23:53:37Z', NULL, 23);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (49, 16, 'authoring/QC.md, RUNBOOK/AGENTS/directory pointers; per-batch pattern for plan 17', 'work', 'open', 620, NULL, 'Part "Findings → changes (c)" of plan 16, the written procedure.

- `authoring/QC.md` (new): steps 1–5 of plan 16 (batch done → blind spot check by the gamemaster, a pm decision "Spot check <batch> done?" for workers → `qgen report --qc <batch>` → proposals by the threshold rule into one pm decision "QC <batch>: which changes?" → approved ones become implementation tasks; next batch waits on both decisions). Prompt changes never inside a batch run.
- D-56 already in `plans/decisions.md`: check it matches.
- One line in `authoring/RUNBOOK.md` step 5 pointing to QC.md; one line in AGENTS.md "Making questions"; `directory.md` entry.
- Plan 17 (batch runs): make sure its tasks follow the pattern batch → spot-check decision → `--qc` + proposal decision → change tasks → next batch (`pm plan edit 17` if its body lacks it; that requeues its split).

Done when: files written and consistent with the commands from the previous tasks as built; no batch or QC run.', '2026-10-11T23:53:37Z', NULL, 23);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (50, 17, 'RUNBOOK: batch runs under pm run', 'work', 'open', NULL, NULL, 'Plan 17 "Batch tasks under `pm run`". RUNBOOK clashes with a pm worker twice; fix it once, so every later batch task can follow RUNBOOK exactly.

- `authoring/RUNBOOK.md`, new short section "Under `pm run`" (env `PM_WORKER=1`), referenced from steps 1, 3, 4:
  - Step 1: `tasks.sql` alone in `git status --porcelain` doesn''t count as dirty.
  - Step 3: exit 75 → `pm decision add "Continue <batch> after the usage limit?"` (body: the message incl. reset time), `pm task-pending-decision <task> <id>`, stage nothing, stop. Exit 1 three times at one step, exit 2 (plan 15''s health stop, if built), other codes, "More than one unfinished batch", "unfinished and writes for bundle": same, decision body = last 30 lines / the message.
  - Step 4: stage exactly the printed `git add` paths; don''t run the printed `git commit` (pm commits as "task N: …").
  - Step 5: the "Done:" line and report path go into `pm task done` note.
- No other RUNBOOK change (task 49 adds the QC.md pointer in step 5; keep both consistent if it''s done).
- No batch run here.

Done when: RUNBOOK has the section; a worker reading only RUNBOOK + its task knows what to do for every exit code.', '2026-10-11T23:54:42Z', NULL, 24);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (51, 17, 'run batch-8', 'work', 'open', NULL, NULL, 'Finish batch-8 (`work/batch-8`, WIP commit d7fb13f: 57 subcategories, 61 draft files, ~$1.6 so far). It resumes with plain `qgen batch`.

- Follow `authoring/RUNBOOK.md` steps 1–5 exactly, with its "Under `pm run`" section (previous task). No arguments.
- Never here: prompt, `qgen.py`, media or subcategory changes; editing pool or `work/`. Findings go into the note (or a pm decision if they block).
- Plans 12–16 tooling (audit step, health stop, targets) is used if it exists; don''t wait for missing parts, list them in the note.

Done when: batch exits 0, printed paths staged; note: "Done:" line, `authoring/reports/batch-8.md`, missing tooling.', '2026-10-11T23:54:42Z', NULL, 24);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (52, 17, 'needs_work of batch-7/8 per decision 3', 'work', 'open', NULL, NULL, 'Resolve the `needs_work` questions (33 at plan time, batch-7''s and older; batch-8''s too if it is merged) the way pm decision 3 says. Waits on decision 3.

- Do exactly what the answer says, nothing more: e.g. `qgen rework` (with `--batch` only if the answer names one) only if the answer asks for it (RUNBOOK "Never": the answer is the gamemaster''s word); act on exit codes as RUNBOOK step 3 / "Under `pm run`"; stage the printed paths.
- If the answer is "the gamemaster decides in the review tool": nothing to run; drop this task with that reason.
- If batch-8 isn''t finished yet, handle what exists; QC batch-8 handles batch-8''s.

Done when: the answer''s action is done; note: count before/after by status.', '2026-10-11T23:54:42Z', NULL, 24);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (53, 17, 'QC batch-8', 'work', 'open', NULL, NULL, 'QC of batch-8 per `authoring/QC.md` (plan 16) and plan 17 "Per-batch pattern" 2. Runs after "run batch-8"; if batch-8 isn''t finished (no `authoring/reports/batch-8.md`), stop without changes (the run order should prevent it).

Phases (the task runs again after each decision is answered; check which decisions exist with `pm show`):
1. `pm decision add "Spot check batch-8 done?"` (body: `/review?batch=batch-8&sample=1` link, size, how to start `trivia-authoring`; option "done"), wait on it, stop.
2. `qgen report --qc batch-8`; proposals by QC.md''s threshold rule into `pm decision add "QC batch-8: which changes?"` (options: recommended set / all / none); wait on it, stop. No proposals: skip the decision.
3. Approved proposals → tasks in plans 13–16 (`pm task add <plan>`, their priority). Record in the note: approved/target per difficulty (`qgen report`), needs_work by reason, media yield (no-media needs_work / merged). If decision 3 is answered: handle batch-8''s needs_work as it says (as the needs_work task does).
4. Media yield ≥ 10% here and in batch-7, or the top needs_work reason: `pm task add 1 "write plan: media yield" --kind plan` pointing to `plans/06-images.md`, `plans/23-media-providers.md`, IMG-16/17; only if no such task exists.
5. Next: if plan 12''s targets are met (or the next batch would overshoot every remaining gap): add the exit-check task (plan 17 "Exit check"). Else add `run batch-9` and `QC batch-9` with bodies like this pair''s.

Missing tooling (audit, `--qc`, spot-check page): do what exists, list the rest in the note. No prompt or `qgen.py` changes here.

Done when: phase 5 done; note lists decisions, change tasks, numbers.', '2026-10-11T23:54:42Z', NULL, 24);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (54, 2, 'create tasks for plan 2', 'split', 'done', 1000, '2026-10-11, tasks 56-61 (55 dropped), decisions 4 5', 'Split plan 2 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:55:44Z', '2026-10-11T23:56:58Z', 2);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (55, 2, 'write plan: Parity fixtures (PORT-1)', 'plan', 'dropped', 1000, 'body had a wrong hint about pm plan add; replaced by the next task', 'Write the plan for part 1 of the masterplan (plan 2): a scenario recorder for the Python referee and the committed fixtures every later part replays.

- Scope: `app/server/game.py` + `app/server/selection.py`, scripted games on a small fixed pool: picks, answers, every joker incl. unavailable ones (`jokers_view`, `trial`), skip for the player / for everyone, undo, abandon, delete player, joker budget (`set_jokers`), supply failure at new game, several players.
- Decide in the plan: how randomness becomes deterministic (inject shuffle/draw choices vs. a seeded PRNG TS can reproduce; must match what part 2''s `engine/rng.ts` will do); where the recorder lives (`authoring/tools/` vs. throw-away script); fixture format in `app/client/src/engine/fixtures/` (inputs, states, views as JSON).
- Recorder runs against today''s untouched SQLite state code, never `state/game.sqlite` of the family (temp dir).
- Plan priority: 700 (must run before parts 2–6).
- `pm plan list` first; `pm plan add 2 …` is wrong: add it to milestone 2 (`pm plan add <milestone> …`).', '2026-10-11T23:56:40Z', '2026-10-11T23:56:49Z', 54);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (56, 2, 'write plan: Engine core: rng, pool, selection (PORT-2)', 'plan', 'done', 1000, '2026-10-11, plan 19 (tasks.sql)', 'Write the plan for part 2 of the masterplan (plan 2): `app/client/src/engine/rng.ts`, `pool.ts`, `selection.ts`.

- `rng.ts`: seedable PRNG, consistent with the determinism chosen in part 1''s plan.
- `pool.ts`: load `app/data/pool.json` + `app/data/categories.json` + `app/data/bundles/<id>/categories.json` (D-43), filter; pure, no fetch (loading happens in part 5).
- `selection.ts`: levels, `LEVEL_RANGES`, `available`, bipartite matching `assign`, `draw`, `supply` (GF-2), same results as `selection.py`.
- Test runner without new dependencies: `node:test` on Node 22; settle type stripping vs. a `tsc` step; wire into an `npm` script.
- Done when: selection fixtures from part 1 replay identically; invariant tests (every level 4 cards, burned never return).
- Plan priority: 610 (after part 1''s plan at 700, before part 3).', '2026-10-11T23:56:40Z', '2026-10-12T00:00:53Z', 54);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (57, 2, 'write plan: Engine game state machine (PORT-3)', 'plan', 'done', 1000, '2026-10-11, plan 20 (tasks.sql)', 'Write the plan for part 3 of the masterplan (plan 2): `app/client/src/engine/game.ts`.

- Pure functions state → state: new game, pick, answer, skip (player / everyone), undo (one step), abandon, delete player, jokers hint/skip/easier/category/snipe with availability and per-game budget (MD-1), burns.
- The view the screens need, same shape as today''s `{"game": …}` from `GET /api/game` where practical; `lib/types.ts` reused.
- Defines the state shape part 4''s `SaveData` stores (`{version, players, games, burned}`).
- Decision entry in `plans/decisions.md`: the client holds the correct answer (relaxes D-25; settled by the milestone), the UI still never renders hidden data.
- Done when: all game fixtures from part 1 replay identically.
- Plan priority: 600 (after part 2).', '2026-10-11T23:56:40Z', '2026-10-12T00:03:22Z', 54);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (58, 2, 'write plan: Save document, stores and migration (PORT-4, PORT-5)', 'plan', 'open', 1000, NULL, 'Write the plan for part 4 of the masterplan (plan 2).

- `SaveData` `{version, players, games, burned}`, one JSON document; `Store` interface `load/save`; `ServerStore` (`GET/PUT /api/save`, atomic write of `state/game.json`, retry on Windows file locks); `MemoryStore` for tests/demo. `FileStore` is out of scope (plan 18).
- Migration `state/game.sqlite` → `state/game.json` once on server start; `.sqlite` kept as backup; tested on a copy of the family''s real save, never the original.
- Authoring readers switch to `game.json`: `authoring/server/overview.py` (`selection.STATE_DB`, `burned_ids`), `qgen report`.
- Where flags live follows the decision linked to this task (`state/flags.json` via `/api/flags`, or inside `SaveData`); `trivia-authoring`''s `apply_flags` (D-47) must still pick them up.
- Ordering: Python side after part 1 (fixtures recorded on untouched state); TS side needs part 3''s state shape.
- Plan priority: 590 (after part 3, despite the schema rule''s 900).', '2026-10-11T23:56:40Z', NULL, 54);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (59, 2, 'write plan: Screens on the engine (PORT-7)', 'plan', 'open', 1000, NULL, 'Write the plan for part 5 of the masterplan (plan 2).

- Replace the game calls in `app/client/src/lib/api.ts` with engine calls + `ServerStore`; categories/media/flags calls as decided (decision linked to this task, part 4''s plan).
- Client loads `pool.json` and categories statically: server serves `app/data/` read-only, or the Vite build copies it; settle in the plan (`flake.nix` `.#app` packaging must still work).
- `PLACEHOLDER(...)` (D-25) stays; no UI changes beyond the wiring.
- Done when: a full game, every joker, undo and admin overlay work in the browser; the family plays a test night on the TS engine (gamemaster''s check).
- Plan priority: 500.', '2026-10-11T23:56:40Z', NULL, 54);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (60, 2, 'write plan: Python server cleanup and docs (PORT-8)', 'plan', 'open', 1000, NULL, 'Write the plan for part 6 of the masterplan (plan 2).

- Delete `app/server/game.py` and the `/api/game*`, `/api/players*` routes from `app/server/main.py`.
- Fate of `selection.py` (used by `qgen report` and `authoring/server/overview.py`) and of `/media`, `/api/flags`, `/api/categories` vs. the milestone''s "`trivia` serves static files plus `/api/save` only": follow the decisions linked to this task; record the outcome in `plans/decisions.md`.
- Update `plans/01-architecture.md`, `plans/12-client-engine.md` (PORT tasks `[x]`), `AGENTS.md`, `directory.md`, `README.md`, the `main.py` docstring; check `nix build .#app` and `result/bin/trivia` still run.
- Plan priority: 400 (last).', '2026-10-11T23:56:40Z', NULL, 54);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (61, 2, 'write plan: Parity fixtures (PORT-1)', 'plan', 'done', 1010, '2026-10-11, plan 18 (tasks.sql)', 'Write the plan for part 1 of the masterplan (plan 2): a scenario recorder for the Python referee and the committed fixtures every later part replays. Priority 1010: runs before the other parts'' plan tasks.

- Scope: `app/server/game.py` + `app/server/selection.py`, scripted games on a small fixed pool: picks, answers, every joker incl. unavailable ones (`jokers_view`, `trial`), skip for the player / for everyone, undo, abandon, delete player, joker budget (`set_jokers`), supply failure at new game, several players.
- Decide in the plan: how randomness becomes deterministic (inject shuffle/draw choices vs. a seeded PRNG TS can reproduce; must match what part 2''s `engine/rng.ts` will do); where the recorder lives (`authoring/tools/` vs. throw-away script); fixture format in `app/client/src/engine/fixtures/` (inputs, states, views as JSON).
- Recorder runs on a temp state dir, never on the family''s `state/game.sqlite`.
- Plan priority: 700 (must run before parts 2–6).', '2026-10-11T23:56:49Z', '2026-10-11T23:59:02Z', 54);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (62, 18, 'create tasks for plan 18', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 65–71)', 'Split plan 18 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:58:59Z', '2026-10-12T00:04:13Z', 61);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (63, 19, 'create tasks for plan 19', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 72–75)', 'Split plan 19 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:00:50Z', '2026-10-12T00:04:51Z', 56);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (64, 20, 'create tasks for plan 20', 'split', 'open', 1000, NULL, 'Split plan 20 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:03:19Z', NULL, 57);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (65, 18, 'Fixture recorder skeleton (PORT-1)', 'work', 'open', NULL, NULL, 'New `authoring/tools/record_fixtures.py` per plan 18 ("Decisions taken here", "Safety"). Python stdlib only.

- Temp state guard: set `TRIVIA_STATE` to `tempfile.mkdtemp()` **before** importing `layout` (it imports `paths`), `game`, `selection`; assert `game.DB` and `selection.STATE_DB` lie inside it, else exit loudly.
- Fresh state per scenario: `selection.burned_ids(db=STATE_DB)` binds the path at def time, so keep one temp dir per process and delete `game.sqlite` between scenarios (not repointing constants); remove the dir at exit.
- Patches:
  - `random.shuffle` → shuffle an index list with `random.Random(seed)`, apply it in place, append `{"site", "n", "perm"}` to the current step''s tape (`perm[j]` = old index now at j; `site` = caller''s function name).
  - `game.now` → the step''s fixed `now` (`2026-01-01T00:00:00` + step index minutes).
  - `categories.load` → fixture categories (wherever `game`/`selection` reference it).
- Dispatch mirroring `main.py` `game_action` (incl. `int(...)` coercions, `event` for `joker`), `GET /api/game` (`{"game", "supply"}`), players routes, delete player. Response `{status, body}`; any 500 aborts recording.
- Step recorder: `{now, call, args, tape, response, db}`; DB snapshot as in plan 18 "Fixture layout" (state parsed, `burned` sorted by (game_id, question_id, player_id)).
- Deterministic JSON writer: `sort_keys`, `ensure_ascii=False`, one step per line.
- CLI: default writes into `app/client/src/engine/fixtures/`; `--check` re-records into a temp dir and diffs, exit 1 on difference.

Done when: a throw-away scenario of 3 steps (new, pick, answer) records with a tape and DB snapshots, and `state/game.sqlite` mtime + checksum are unchanged after the run.', '2026-10-12T00:04:11Z', NULL, 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (66, 18, 'Synthetic fixture categories and pools (PORT-1)', 'work', 'open', NULL, NULL, 'The recorder (`authoring/tools/record_fixtures.py`) generates and writes, deterministically, into `app/client/src/engine/fixtures/` (plan 18, "Fixture layout"):

- `categories.json`: 2 bundles (`base` + one more, D-43), 3 broad categories, ~6 subcategories; same shape as `categories.load()` output (with `bundle`).
- `pools/main.json`: ~90 approved questions, difficulties 1–10 across all subcategories, hints 0–3 (some with 0), all fields the referee and `game.view` read (`id`, `status`, `difficulty`, `subcategory`, `description`, `question`, `answer`, `wrong_answers`, `hints`, `media`, `background`, `fun_fact`, `bundle`).
- `pools/tight.json`: barely one game: the second game hits a supply failure; Bájale, Cambiazo, purge and snipe-hit unavailable.

Check against `selection.supply` / `assign` with a throw-away call: main supports several games per player with jokers; tight supports exactly one.

Done when: the files are written, re-running gives identical bytes, and the supply checks above hold.', '2026-10-12T00:04:11Z', NULL, 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (67, 18, 'Selection fixture cases (PORT-1)', 'work', 'open', NULL, NULL, 'The recorder writes `app/client/src/engine/fixtures/selection.json` (plan 18, "Fixture layout"): direct calls into `app/server/selection.py`, each `{name, fn, args, tape, result}`.

- `in_range`: edges of each level range.
- `assign`: subsets of levels, shortages.
- `supply`: main pool, tight pool, tight minus burns (burns written to the temp DB first).
- `draw`: plain, with `keep`, with `avoid_categories`, `n` < 4, unfillable → `None`.

Done when: every function above has its cases with tapes, and `--check` passes.', '2026-10-12T00:04:11Z', NULL, 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (68, 18, 'Scripted game scenarios: rules and jokers (PORT-1)', 'work', 'open', NULL, NULL, 'Add these scenarios to `authoring/tools/record_fixtures.py`, written to `app/client/src/engine/fixtures/game/<name>.json` (plan 18, "Scenarios"): `win`, `lose-undo`, `hint`, `skip-purge`, `easier`, `category`, `snipe`, `budget`. Each case listed in the plan for these scenarios must appear, incl. one available and one unavailable case per joker, and `snipe`''s hit with no cards left on the tight pool.

Pick answers/indexes from the recorded view (the correct index is in the state), not hard-coded, so scenarios survive pool tweaks.

Done when: all 8 files are written, no step returned 500, `--check` passes.', '2026-10-12T00:04:11Z', NULL, 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (69, 18, 'Scripted game scenarios: players, admin and errors (PORT-1)', 'work', 'open', NULL, NULL, 'Add these scenarios to `authoring/tools/record_fixtures.py`, written to `app/client/src/engine/fixtures/game/<name>.json` (plan 18, "Scenarios"): `admin-skip`, `players`, `abandon`, `supply`, `errors`. Each case listed in the plan for these scenarios must appear, notably: casefold «Íngrid»/«íngrid», empty and too long names, delete player with a running game, IDs after a delete (SQLite max+1), `supply` 409 report on the tight pool, every action with no running game → error, and DB unchanged after each error.

Done when: all 5 files are written, no step returned 500, `--check` passes.', '2026-10-12T00:04:12Z', NULL, 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (70, 18, 'Soak scenarios (PORT-1)', 'work', 'open', NULL, NULL, 'Add ~10 seeded random walks `soak-<n>` to `authoring/tools/record_fixtures.py` (plan 18, "Scenarios"): 30–60 steps each, legal actions chosen from the current view (picks, answers, every joker incl. purge/Cambiazo/snipe, undo, admin skip incl. everyone, new games, new players). The walk''s choices come from a separate `random.Random(seed)`, not the patched shuffle, so the tape only holds referee shuffles.

Done when: the files are written, no step returned 500, the walks cover every action at least once overall, total fixture size < 2 MB, `--check` passes.', '2026-10-12T00:04:12Z', NULL, 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (71, 18, 'Fixture README, plan and directory updates (PORT-1)', 'work', 'open', NULL, NULL, '- `app/client/src/engine/fixtures/README.md`: file format, tape semantics (`perm`, `site`, `tapeRng` contract: fail on wrong `n`, site mismatch, leftover/missing entry), fixed `now` per step, how to re-record and check (`python3 authoring/tools/record_fixtures.py [--check]`), and plan 18''s "Notes for parts 2/3".
- `plans/12-client-engine.md`: PORT-1 `[x]` with a note; "Parity strategy" step 1 states the shuffle-tape choice.
- `plans/decisions.md`: a D-entry for the shuffle tape (no shared PRNG; the TS engine takes an injected `Rng`).
- `directory.md`: the recorder and the fixtures directory.

Final check of plan 18 "Done when": fresh run from an empty fixtures dir, `--check` byte-identical, `state/game.sqlite` mtime + checksum unchanged.

Done when: the above is written and the final check passes.', '2026-10-12T00:04:12Z', NULL, 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (72, 19, 'Test runner and rng.ts (PORT-2)', 'work', 'open', NULL, NULL, 'Set up engine tests with `node:test` and Node''s type stripping, and write the seedable shuffle. See plan 19, "Decisions taken here".

- `app/client/tsconfig.json`: `allowImportingTsExtensions: true`, `erasableSyntaxOnly: true`; exclude `src/**/*.test.ts` and `src/engine/test/` (no `@types/node`).
- Scripts: `app/client/package.json` `"test": "node --test ''src/engine/**/*.test.ts''"`; root `package.json` `"test": "npm run test --workspaces --if-present"`.
- `app/client/src/engine/rng.ts`: `interface Rng { shuffle<T>(xs: T[], site: string): void }` (in place), `seededRng(seed)` (mulberry32 + Fisher–Yates), `randomSeed()` (`crypto.getRandomValues`). No `node:` imports, no `Math.random`, erasable syntax only.
- `app/client/src/engine/test/tape.ts`: `tapeRng(tape)` with plan 18''s tape semantics (`xs[j] = old[perm[j]]`); throws on wrong `n`, site mismatch, missing entries; `done()` throws on leftovers.
- `rng.test.ts`: same seed → same permutations; results are permutations; tape errors; a hand-written tape.
- Decision entry in `plans/decisions.md` (next D number): `node:test` + type stripping, `.ts` imports, tests not type-checked.

Done when: `npm test` and `npm run check` pass at the root; `npm run build` still works; no new dependencies.', '2026-10-12T00:04:49Z', NULL, 63);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (73, 19, 'pool.ts: pool and category data (PORT-2)', 'work', 'open', NULL, NULL, 'Pure typed access to `pool.json` and the category files, mirroring `app/server/categories.py` and `game.category_of`. See plan 19, "Files".

- `app/client/src/engine/pool.ts`: `PoolQuestion` (all `pool.json` fields, incl. `answer`, `wrong_answers`, `hints`; reuse `Media`, `Background`, `Category`, `Status` from `lib/types.ts`), `parsePool(json)` (checks `version` 1), `loadCategories(bundlesJson, files)` (bundles.json order, base first, a bundle without a file has none), `subcategories(cats, bundle?)`, `broadOf(cats)`, `bundleOf(cats, sub)`, `categoryOf(broad)` (question → broad slug or `null`), `byId(pool)`.
- No fetching (part 5), no bundle filtering, no `node:` imports.
- `pool.test.ts` on the real `app/data/` files and on `fixtures/categories.json` (plan 18, task 66): category order equals `categories.load()` (compare once with a throw-away `python3 -c` dump, not committed); `broadOf`/`categoryOf` on a few known subcategories.

Done when: `npm test` and `npm run check` pass.', '2026-10-12T00:04:49Z', NULL, 63);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (74, 19, 'selection.ts and fixture replay (PORT-2)', 'work', 'open', NULL, NULL, 'Port `app/server/selection.py` to `app/client/src/engine/selection.ts` with identical results. Follow plan 19, "Parity details for `selection.ts`", exactly (Map for `owner`, level sort order, one `rng.shuffle(cands, "draw")` per call even when empty, stable sort keys, `null` as category).

- Exports: `LEVELS`, `PER_LEVEL`, `LEVEL_RANGES`, `inRange`, `available(pool, burned, exclude)`, `assign(questions, levels)` → `{assignment, missing}` (Maps), `draw(level, questions, {n, keep, avoidCategories, categoryOf, rng})` → `PoolQuestion[] | null`, `supply(questions)` → `Supply[]`.
- `app/client/src/engine/test/fixtures.ts`: reads fixture JSON via `node:fs` relative to `import.meta.dirname`.
- `selection.test.ts`: replays every case of `fixtures/selection.json` (plan 18, task 67): `in_range`, `assign`, `supply`, `draw` with `tapeRng`, incl. `keep`, `avoid_categories`, `n` < 4, unfillable → `null`; every tape fully consumed. Int keys come back as strings from Python JSON: compare per level, list order within a level.
- Gaps in the fixtures: fix plan 18''s recorder and re-record; never hand-edit fixtures.

Done when: every `selection.json` case replays identically; `npm test` and `npm run check` pass.', '2026-10-12T00:04:49Z', NULL, 63);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (75, 19, 'Selection invariant tests and docs (PORT-2)', 'work', 'open', NULL, NULL, 'Property tests of `selection.ts` on the real pool, then close PORT-2 in the docs. See plan 19, task 4.

- `app/client/src/engine/invariants.test.ts` on `app/data/pool.json` (skip with a message if absent), ~50 `seededRng` seeds: random burned subsets (only where `supply` reports no missing); a 12-level walk drawing 4 cards per level with `offered` excluded and `avoidCategories` from earlier picks.
- Checks: every level gets 4 distinct cards in range; no burned or already offered ID appears; no shortage in `supply` never leads to a `null` draw. Runs in a few seconds.
- Docs: `plans/12-client-engine.md` (PORT-2 `[x]` with a note), `directory.md` (`app/client/src/engine/`), AGENTS.md Commands (`npm test`), README.md if it lists npm commands.
- Check that engine modules import nothing outside `src/engine/` and `src/lib/types.ts`, and nothing from `node:`.

Done when: plan 19''s "Done when" holds: root `npm test`, `npm run check`, `npm run build` pass; no new dependencies.', '2026-10-12T00:04:49Z', NULL, 63);

INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (1, 'Target count per difficulty (1–15) for 5000 approved base questions?', 'pending', '["1: 250 · 2: 350 · 3–8: 450 each · 9–11: 330 each · 12–13: 230 each · 14–15: 125 each (sum 5000)", "masterplan draft: 1–2: 490 each · 3–8: 420 each · 9–11: 300 each · 12–13: 200 each · 14–15: 100 each (sum 5000)", "flat: 333 per level (5 extra at 6–10)"]', 'Milestone 1, part 1 (D-52). Today (2026-10-11) approved base by difficulty: 1: 36 · 2: 67 · 3: 96 · 4: 104 · 5: 112 · 6: 147 · 7: 101 · 8: 67 · 9: 74 · 10: 57 · 11: 61 · 12: 38 · 13: 48 · 14: 19 · 15: 8.
The targets steer `draft` (part 2: aim at the gaps) and are the milestone''s exit check.
Recommended curve tapers at both ends; the masterplan draft puts more at 1–2 than at the middle levels, which is likely more easy questions than game nights need.', NULL, NULL, '2026-10-11T23:16:33Z', NULL, 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (2, 'When is batch quality "fine": human spot-check size and agreement rate with the LLM review?', 'pending', '["30 random questions per batch; ≥ 90% agreement in each of the last two batches", "50 per batch; ≥ 95% agreement", "20 per batch; ≥ 85% agreement"]', 'Milestone 1, parts 1 and 5. After every batch the gamemaster checks a random sample in the review tool and records agree/disagree with the LLM verdict. This rate is the main "quality is fine" signal and part of the milestone''s exit check (last two batches).
30 questions take roughly 10–15 minutes; 50 gives a tighter rate but costs more of the human''s time per batch (~8 batches left).', NULL, NULL, '2026-10-11T23:16:33Z', NULL, 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (3, 'How are needs_work questions (33 now, more per batch) resolved?', 'pending', '["qgen rework once after each batch''s QC, then the gamemaster decides what is still needs_work in the review tool", "the gamemaster decides all of them in the review tool; no qgen rework", "leave them; only approved questions count toward 5000"]', 'Milestone 1, part 6. RUNBOOK: `qgen rework` runs only on the gamemaster''s word; this answer is that word for the batch tasks of this milestone. batch-7 needs_work reasons: mostly giveaway hints, overlap with a pool question, or no usable media.
Rework costs LLM calls but saves the gamemaster''s time; overlaps (once part 4 drops them before merge) and media misses don''t benefit from rework.', NULL, NULL, '2026-10-11T23:16:33Z', NULL, 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (4, 'After the engine port, which routes does the Python game server keep besides static files and /api/save?', 'pending', '["Keep /media (download on cache miss, D-17), /api/flags (state/flags.json, D-47) and /api/categories; amend the milestone''s ''static files plus /api/save only'' accordingly", "Move flags into SaveData (drop /api/flags, trivia-authoring reads game.json); keep /media and /api/categories", "Strictly static + /api/save: flags into SaveData, categories served as static files, media served only from the synced cache (no download on miss; trivia-media sync required before play)"]', 'Milestone 2 "Done when" says `trivia` serves static files plus `/api/save` only. Today `app/server/main.py` also has `/media` (cache + download on miss, D-17), `/api/flags` (game flags questions, `trivia-authoring` turns them into reviews, D-47) and `/api/categories` (all bundles, D-43). Python stays in family mode anyway (plan 12, D-3); the desktop shell (plan 18) is out of scope. Affects parts 4, 5, 6 of the masterplan.', NULL, NULL, '2026-10-11T23:56:57Z', NULL, 54, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (5, 'Where does the supply check for qgen report and the authoring start page live once app/server/selection.py has no game to serve?', 'pending', '["Move selection.py to authoring/tools/ unchanged (reads game.json), parity with engine/selection.ts guarded by the PORT-1 selection fixtures", "Authoring calls the TS engine via node (type stripping), no Python copy", "Keep app/server/selection.py where it is"]', '`qgen report` and `authoring/server/overview.py` use `selection.py` (levels, `LEVEL_RANGES`, `available`, `supply`, `burned_ids`). After PORT-8 the game no longer needs it. A Python copy duplicates the rules in two languages; calling Node from Python tooling adds a runtime hop. Plan 12 (PORT-8) left it open. Affects part 6 (and part 4''s switch of the authoring readers).', NULL, NULL, '2026-10-11T23:56:58Z', NULL, 54, NULL);

INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (1, 1, '2026-10-11T23:14:36Z', '2026-10-11T23:16:05Z', 'done', NULL, 0, 'd7fb13f0580397cd7e3cb79641c26f1f67ace8b0', 'claude-opus-5-5[1m]', '102a6d61-be2f-483e-83e1-57951f33bbef', 14, 28, 8375, 677422, 59914, 0.78240839999999989, 73367);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (2, 12, '2026-10-11T23:16:05Z', '2026-10-11T23:17:00Z', 'done', NULL, 0, 'c4bab21ed411ec2cadb1435ebb3fa8c838bbca71', 'claude-opus-5-5[1m]', 'e075f121-119b-411e-af9c-9034110e6417', 6, 12, 5681, 191036, 29983, 0.3917392, 73367);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (3, 13, '2026-10-11T23:38:39Z', '2026-10-11T23:39:37Z', 'done', NULL, 0, '695c887e9c67db86f9ee0d3940dbc6cdd1f21c7c', 'claude-opus-5-5[1m]', 'cdb8babf-965b-40c1-b805-81625b28c7ff', 10, 20, 5455, 395561, 43117, 0.5332282, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (4, 14, '2026-10-11T23:39:37Z', '2026-10-11T23:41:51Z', 'done', NULL, 0, '3c2593167a0ea1330113d47a576182ad79943b4c', 'claude-opus-5-5[1m]', 'd31a158b-e857-4d3c-af7f-592d06d0b6da', 22, 44, 12603, 1024603, 52175, 0.87455660000000013, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (5, 15, '2026-10-11T23:41:51Z', '2026-10-11T23:44:00Z', 'done', NULL, 0, 'a979e6531d99f0e1e108fd42991906d9b6276453', 'claude-opus-5-5[1m]', '54bd36dd-a66a-4aa3-925f-fb9e8e55c0f8', 16, 32, 12922, 785142, 59246, 0.88956440000000014, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (6, 16, '2026-10-11T23:44:00Z', '2026-10-11T23:46:18Z', 'done', NULL, 0, '935c36d3b4ace0118f044d7942768252932eb593', 'claude-opus-5-5[1m]', 'e0185921-1dee-4604-a220-e5d303e29352', 17, 34, 13786, 823893, 60167, 0.92197059999999986, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (7, 17, '2026-10-11T23:46:18Z', '2026-10-11T23:48:31Z', 'done', NULL, 0, '785f63de17c58a8bd08796231eeca632561842ce', 'claude-opus-5-5[1m]', 'e6f532e2-0f7b-4920-8bb4-37928071b4f0', 13, 24, 12609, 496968, 59600, 0.82846960000000014, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (8, 18, '2026-10-11T23:48:31Z', '2026-10-11T23:49:47Z', 'done', NULL, 0, 'ec3c4411dbc8a830fbcc7b022548022ae86edbc5', 'claude-opus-5-5[1m]', '9a45fda3-74a3-4272-9402-2568736e1756', 10, 18, 6999, 320901, 37758, 0.50629620000000009, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (9, 19, '2026-10-11T23:49:47Z', '2026-10-11T23:50:15Z', 'done', NULL, 0, '29edfcb1393298ba2322f16f6f605a051a4e036e', 'claude-opus-5-5[1m]', '09948f6a-545e-48ed-9d10-3ff1972e22b3', 6, 12, 2859, 175801, 26236, 0.3022762, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (10, 20, '2026-10-11T23:50:15Z', '2026-10-11T23:51:15Z', 'done', NULL, 0, '8fdfc21f0a7e6f58f5050acf29b50fe08158bacf', 'claude-opus-5-5[1m]', '4d70826f-4639-4508-9b2c-6d8111de8f1f', 9, 18, 6170, 311821, 32442, 0.4453722, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (11, 21, '2026-10-11T23:51:15Z', '2026-10-11T23:51:49Z', 'done', NULL, 0, '8975495c4bc7ec1e851d125441f7178b300fb2dd', 'claude-opus-5-5[1m]', '48250d51-c9cd-4467-8b6b-c19264e71694', 5, 10, 2622, 137512, 23878, 0.27100640000000004, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (12, 22, '2026-10-11T23:51:49Z', '2026-10-11T23:52:49Z', 'done', NULL, 0, '3d9fa2fda59849b2763367b9b440ac866818c465', 'claude-opus-5-5[1m]', '17dc73a2-9011-4a4d-88dd-8cd1e998649c', 9, 18, 5816, 355709, 37673, 0.48891779999999996, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (13, 23, '2026-10-11T23:52:49Z', '2026-10-11T23:53:45Z', 'done', NULL, 0, '776787ea570c7b398ba40c2e4da2e7003f323435', 'claude-opus-5-5[1m]', 'f12a1a7f-b761-46de-8040-60e2bd1e05df', 8, 16, 4891, 287815, 34064, 0.427959, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (14, 24, '2026-10-11T23:53:45Z', '2026-10-11T23:54:52Z', 'done', NULL, 0, '3def4ab41f85709722f02ca7b0ffa6e6fc0209d0', 'claude-opus-5-5[1m]', '968a74a2-a95a-4f6b-ae51-6a7fbac8aa99', 9, 18, 6577, 346223, 39040, 0.5131766, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (15, 2, '2026-10-11T23:54:52Z', '2026-10-11T23:55:53Z', 'done', NULL, 0, '00a9a2efc5c7ffc663fcdc31b80b0959bcecee90', 'claude-opus-5-5[1m]', '405770f5-0bf4-48f2-9f6a-bb47813468d9', 10, 20, 5689, 348572, 33337, 0.45027039999999996, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (16, 54, '2026-10-11T23:55:53Z', '2026-10-11T23:57:08Z', 'done', NULL, 0, '76cdfdd3b4b2be8a52558adffa5925b0b01da56d', 'claude-opus-5-5[1m]', '67665ee3-61b2-43f5-a24c-8ab0630b9ff7', 8, 16, 7760, 302651, 36510, 0.5078742, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (17, 61, '2026-10-11T23:57:08Z', '2026-10-11T23:59:10Z', 'done', NULL, 0, '0fef3579bab3dd745acb81b226ed6c4c0d5744a3', 'claude-opus-5-5[1m]', 'e5654647-a002-4ece-8190-adcca9bf52cb', 10, 20, 11845, 431697, 55270, 0.7654794, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (18, 56, '2026-10-11T23:59:10Z', '2026-10-12T00:01:02Z', 'done', NULL, 0, '43f5f4666a0f606e3d1746d0d183e7fdbb82f4f6', 'claude-opus-5-5[1m]', '3e435859-8756-4e90-a382-239bb8c0804f', 13, 26, 9512, 558720, 47366, 0.68101600000000007, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (19, 57, '2026-10-12T00:01:03Z', '2026-10-12T00:03:33Z', 'done', NULL, 0, '9d77fa68242b8cf8cab66bc29da2b042b32deb70', 'claude-opus-5-5[1m]', '13b030d7-c338-41cd-9fa1-15ef264a09a8', 13, 22, 13320, 506931, 62286, 0.8661622, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (20, 62, '2026-10-12T00:03:33Z', '2026-10-12T00:04:21Z', 'done', NULL, 0, '55c09c13403ad0a6b4aae9ade2e8a44acd838591', 'claude-opus-5-5[1m]', 'edf64974-0ddb-46ac-94bb-a99b0c8cd88a', 6, 12, 4886, 190559, 30344, 0.3786318, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (21, 63, '2026-10-12T00:04:21Z', '2026-10-12T00:04:57Z', 'done', NULL, 0, '096e9c39036dc19181f3a734459186398b0b6bb3', 'claude-opus-5-5[1m]', '5725e50f-0d66-41a4-9315-1d9058b3d7f5', 7, 14, 3613, 222573, 27513, 0.33693460000000003, 80113);

INSERT INTO task_decision (task_id, decision_id) VALUES (25, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (26, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (27, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (28, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (28, 2);
INSERT INTO task_decision (task_id, decision_id) VALUES (35, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (36, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (44, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (48, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (48, 2);
INSERT INTO task_decision (task_id, decision_id) VALUES (52, 3);
INSERT INTO task_decision (task_id, decision_id) VALUES (58, 4);
INSERT INTO task_decision (task_id, decision_id) VALUES (58, 5);
INSERT INTO task_decision (task_id, decision_id) VALUES (59, 4);
INSERT INTO task_decision (task_id, decision_id) VALUES (60, 4);
INSERT INTO task_decision (task_id, decision_id) VALUES (60, 5);
