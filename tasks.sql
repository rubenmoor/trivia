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
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (3, 3, 'masterplan', 1000, 'Milestone 3 moves every on-screen string of the game into a catalog, with no visible change in Spanish, and closes the bundle work with the gamemaster''s check of the `colombia` proposals. Design source: `plans/15a-ui-translation.md` (LUI-1..LUI-3) and `plans/22-bundles.md` (D-39).

**The tasks of this masterplan are not implementation work: each of them writes the plan for one part** (`pm plan add 3 …`, priority per the project rules). The part plans then get split into implementation tasks.

## State today (2026-10-11)
- Spanish literals in 13 files of `app/client/src/game` (`copy.ts`, `Game.svelte`, `Question.svelte`, `Overlay.svelte`, `JokerTray.svelte`, `Player.svelte`, `CategoryPicker.svelte`, `DifficultyDial.svelte`, `Shredder.svelte`, `Fireworks.svelte`, `swap.ts`, `timing.ts`, `sound.svelte.ts`), incl. `aria-label`/`title` attributes.
- `sound.svelte.ts` matches Spanish cue descriptions by regex (`/trombón|Ups/`, `/menú abierto/`, …): internal keys, not on screen, but they trip the milestone''s grep check.
- The server sends Spanish error texts that the client shows in the corner as is: `app/server/game.py` (`GameError("ya no les quedan Soplos")`, `"no hay preguntas más fáciles de este tema"`, …), via `app/server/main.py` → `app/client/src/lib/api.ts` → `error` in `Game.svelte`.
- `app/client/index.html`: `<title>Trivia</title>`.
- Bundles: every question in `authoring/data/questions.json` has `bundle`, and `validate_pool()` in `authoring/tools/qgen.py` already rejects a missing or unknown one. 84 `colombia` proposals of BN-3 (`work/bundles/proposals.json`) are unchecked.

## Parts

### 1. `t()` helper and the `es` catalog (LUI-1, client, ~500)
- `app/client/src/lib/i18n.ts`: `t(key, params)`, plurals via `Intl.PluralRules`, numbers via `Intl.NumberFormat`; no library.
- `app/client/src/locales/es.ts`: typed object; its type is the `Catalog` every other language must satisfy, so a missing key fails `npm run check`.
- Move every string: `copy.ts` variant arrays (milestones, consolation; `choose()`/seed logic unchanged), all component text, `aria-label`/`title`, joker names and their key hints (keys themselves stay as today; LUI-4 is out of scope), `index.html` title.
- Sound cues: switch the regex-on-Spanish-text lookup to neutral cue ids, so `sound.svelte.ts` holds no Spanish.
- Language choice: `es` by default; a dev-only override (e.g. `?lang=xx`) for parts 3 and 4. No language menu (OQ-31).
- Check: a small script or documented `grep` for Spanish characters and quoted Spanish words in `app/client/src/game` (the milestone''s "done when"); screen-by-screen comparison before/after shows no visible change.
- Split by component group so each task fits one run.

### 2. Server errors as codes (backend, ~700; before or alongside part 1)
- `GameError` carries a stable code plus params (e.g. `{"error": "joker_spent", "joker": "hint"}`); the client renders it with `t()`. Keep a readable English fallback text for logs and the authoring side.
- Files: `app/server/game.py`, `app/server/main.py`, `app/client/src/lib/api.ts`, `Game.svelte`.
- Without this, on-screen error lines stay Spanish outside the catalog.

### 3. Pseudo-locale `xx` (LUI-2, client, after part 1)
- Generated from `es` at runtime or build: pads each string by ~40 % and adds accents, keeps `{params}` intact.
- Missing-string test: every key resolved through `t()` shows visibly (e.g. `⟦key⟧`) when absent; type check covers the static side.
- Walk every screen on the TV layout with `?lang=xx`; log overflow found as backlog items (`plans/backlog.md`), don''t redesign here.

### 4. Draft `en` catalog (LUI-3, client, after part 1)
- `app/client/src/locales/en.ts`, satisfies `Catalog`; Claude drafts it.
- Playful English joker names, not literal translations (15a); a short list of candidates per joker for the gamemaster, if unsure raise a pm decision.
- Draft only: no native-speaker check, no launch (LUI-5, OQ-31).

### 5. Gamemaster check of the `colombia` proposals (D-39, human)
- The gamemaster reviews the 84 BN-3 proposals at `/review?bundle=colombia` (key `n` moves a question to the next bundle).
- Agent side only: a pm decision/sign-off that asks for the check and waits; afterwards note the result in `plans/22-bundles.md` (BN-3) and `plans/project.md`, run `qgen validate` and `qgen export`.
- "Every question has `bundle`" is already enforced by `validate`; confirm, don''t rebuild.

## Across all parts
- Update `plans/15a-ui-translation.md` (mark LUI-1..LUI-3), `plans/project.md` (M3 status), `directory.md` (new files `lib/i18n.ts`, `locales/`), and `plans/decisions.md` if the catalog shape or error codes become a decision.
- `npm run check` and `npm run build` pass after every task.

## Out of scope
- Translating questions, categories, bundle names (content; `plans/15b-question-translation.md`).
- Launch languages and the Spanish variety (OQ-31), joker keys per language (LUI-4), store texts (LUI-6).
- `/comodines` printable cards and the review tool (`authoring/`): stay Spanish for now; log in backlog if needed.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (4, 4, 'masterplan', 1000, 'Milestone 4 makes the licence of every picked media file known, stored and clean before any public release. Today the pool keeps only a `credit` string per slot (`author · licence · provider`); the full data lives in the candidate files (`work/media/<qid>.json`) or not at all, and the Commons query (`providers/commons.py`) reads only `Artist`, `LicenseShortName`, `LicenseUrl`.

**The tasks of this masterplan are not implementation work: each of them writes the plan for one part** (`pm plan add 4 …`), with its own tasks queued by pm.

## Part 1: Licence data in the pool (PUB-2, takes over MP-8 of `plans/23-media-providers.md`)
- Per picked slot (`media`, `background`, all bundles): `provider`, `license`, `license_url`, `author`, `author_url`, `restrictions` (Commons non-copyright templates: personality rights, trademark, …), and for public domain the reason (`PD-old-70`, `PD-US`, `PD-USGov`, …), next to `source_url`, `file_url`, `credit`.
- `media.pick_fields` writes them on every new pick (pipeline and review tool); `providers/commons.py` asks Commons for the extra extmetadata (`Restrictions`, `AttributionRequired`, `UsageTerms`, PD templates/categories); other providers fill what they have.
- One migration for existing picks: from the stored candidate, else a live Commons lookup by `source_url`.
- `qgen validate`: missing licence data on an approved question is an error (milestone "done when"); before the migration a warning. `qgen export`: only what the game needs (decide in the plan; credits screen PUB-5 is out of scope).
- Priority: schema of the pool, 900; runs first, parts 2 and 3 read its fields.

## Part 2: Audit report `media.py licenses` (PUB-1)
- Per file in the pool: licence, family (`providers.licence_kind`), PD reason, restrictions, question ids and status.
- Classifies into ok / replace: PD-US only, GFDL (and anything else off the MP allowlist), flagged restrictions, missing data. Prints the replacement list (empty list = milestone done) and a tally like the one in `plans/17-publishing.md`.
- Reads the pool fields of part 1, no network at report time.
- Priority: backend tooling, 700.

## Part 3: Replace the problem files in the review tool (PUB-3)
- Review tool (`authoring/server/`, `authoring/ui/`): a filter for questions whose media is on the replacement list (e.g. `/review?licence=replace`), the reason shown next to the slot, replacement through the existing candidate list and search modal over all providers.
- The gamemaster picks; no LLM pick, no automatic swap (milestone constraint). The new pick gets the part 1 fields through `pick_fields`.
- Then the human work: go through the list until `media.py licenses` reports nothing to replace; `trivia-media sync --status approved --prune` drops the old files from the cache (D-17).
- Optional gate: `qgen validate` errors on approved questions with a file on the replacement list, so it can''t come back.
- Priority: review UI, 400; after parts 1 and 2.

## Not in this milestone
- Credits screen, `CREDITS.md`, store disclosures (PUB-5, Steam S3/S5); code licence (PUB-4).
- Audio UI sounds and fonts (`app/client/public/audio/CREDITS.md`, OFL): not pool media.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (5, 5, 'masterplan', 1000, 'Milestone 5 lets players choose an age group and the bundles to play before a session. Today the referee plays one audience: 12 levels with fixed `LEVEL_RANGES` over difficulty 1–10 (D-22), from every approved question of every bundle (1136 approved: `base` 1035 over 1–15, `colombia` 101 over 2–13). The groups and their draft windows already ship in `app/data/age-groups.json` (D-38), the bundles in `app/data/bundles.json` (D-39); nothing in the game reads them yet. Design sources: `plans/21-age-groups.md` (AG-7), `plans/22-bundles.md` (BN-6).

**The tasks of this masterplan are not implementation work: each of them writes the plan for one part** (`pm plan add 5 …`), with its own tasks queued by pm.

## Depends on milestone 2 (TypeScript engine)
- Every part builds on the TS referee, not on `app/server/game.py` / `selection.py`: plan 19 (`engine/selection.ts`, `pool.ts`: `LEVEL_RANGES`, `assign`, `draw`, `supply`, `loadCategories`), plan 20 (`engine/game.ts`, `state.ts`: `GameState.settings`, `newGame`, `jokersView`, `engine/api.ts`), and M2 parts 4–5 (save document, screens on the engine; plans not written yet).
- No part changes the Python referee. If M2 slips, the part plans wait; they don''t port to Python.
- Plan 19 explicitly leaves bundle filtering out ("same rules"); part 1 adds it.

## Part 1: Group windows and bundle filter in the engine (AG-7, BN-6; core mechanics)
- **Data:** per group in `age-groups.json` the 12 level ranges (`levels`), so every group keeps the shape of D-22 (level 1 narrow, 4 cards per level). `young_teens` = today''s `LEVEL_RANGES` exactly; the other groups a first mapping of the same shape onto their window (tuned in part 3). One source for the ranges; the engine reads them instead of a constant.
- **Settings:** `GameState.settings` gets `age_group` and `bundles` (list of active ids, `base` always in). Defaults when missing (`withDefaults`): `young_teens` and every bundle on, so old saves and plan 18''s fixtures replay unchanged (milestone constraint "defaults unchanged").
- **Selection:** `available` / `draw` / `assign` / `supply` take the group''s ranges and the active bundles; everything that uses levels follows the game''s group (draw, the replacement for «Cambiazo» and the other jokers, supply check at new game). Burns stay per player across groups and bundles (D-28).
- **Cambiazo:** the picker offers only the categories of active bundles (`jokersView`; plan 22 says "all of them until BN-6").
- **API:** `newGame` accepts `age_group` and `bundles`, validates them against the data files; `getGame` / `supply` report for a given group and bundle set, so the start screen can warn before a session can''t be filled.
- **Checks:** fixture replay still identical with defaults; new tests per group (every level 4 cards in its range) and with `colombia` off (no `colombia` question ever drawn, Cambiazo without its categories).
- Decision entry: settings per game, defaults, `base` always on.
- Suggested priority: 590, after plan 20 (600) and before M2''s screens part (500).

## Part 2: Choice before a session (start screen; user interface)
- After choosing the player and before the first level: age group (four tiles: name and ages from `age-groups.json`) and bundles (one toggle per bundle with `name` and `description` from `bundles.json`; `base` shown on and locked).
- Preset: the player''s last game''s choice, else the defaults; the family can press Enter straight through as today ("nothing changes unless they opt in").
- Supply per choice from part 1: a group or bundle set that can''t fill 12 levels is shown as such and can''t start (same message style as today''s supply failure).
- IN-1: every choice clickable and on the keyboard (e.g. digits/arrows for groups, letters for bundles; the plan settles keys), with `<kbd>` hints like the rest of the start screen.
- The HUD or admin overlay shows the running game''s group and bundles (plan decides where); undo and abandon keep them.
- Spanish texts through the catalog if milestone 3 (plan 21, `t()`) has landed, else literals marked for it.
- Suggested priority: 400, after M2''s screens part (500).

## Part 3: Tune the windows and per-group level weights (AG-7)
- Measure per group and bundle set (`base` alone, `base`+`colombia`): candidates per level, missing slots, games until the pool runs dry for one player; a throw-away script on the engine (`node`) over `app/data/pool.json`.
- Compare with plan 21''s long-term distribution proposal (demand per level from overlapping windows) and the difficulty scale''s anchors (1 = 6-year-old … 15 = specialists).
- Adjust windows and level ranges in `age-groups.json`; derive each group''s level weights from its ranges as D-31 did for young teens and store them there (`level_weights`), for AG-8 and the D-53 targets later; consumers outside the game are out of scope.
- The gamemaster approves the final windows (decision with the measured table); then plan 21 drops "draft", `about` in `age-groups.json` updated, a decision entry.
- Thin top of the scale (14–15: 27 approved) is reported, not fixed here: questions are milestone 1''s work.
- Suggested priority: 580, after part 1 (needs its per-group ranges), before part 2''s UI so the screen shows tuned windows.

## Part 4: Play-test and close-out
- The milestone''s "done when": one session per age group, and one with `colombia` off, in the browser on the real pool. Human work: a decision asks the gamemaster to confirm; the agent side records it.
- Docs: `plans/21-age-groups.md` (AG-7 `[x]`, "The game plays young teens until AG-7" removed), `plans/22-bundles.md` (BN-6 `[x]`, "Later" section), `plans/project.md`, `directory.md`, the `about` texts of both data files.
- Authoring readers that assume levels 1–10 or one range table (`/stats/difficulty`, `qgen report` supply) checked; changes only if they break, otherwise logged in `plans/backlog.md`.
- Suggested priority: 390, last (after part 2).

## Not in this milestone
- New bundles, regional packs (`plans/15c-regional-questions.md`).
- Batches per age group (AG-8), targets from the windows (plan 21''s distribution proposal, D-53).
- Mixed-age sessions (one game, several groups at once); log in `plans/open-questions.md` if it comes up.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (6, 6, 'masterplan', 1000, 'Milestone 6 closes the two leftovers of M3/M4: preloading before a screen fades in (UI-7) and recorded sounds for everything still synthesized (UI-10). Owner plan file: `plans/04-ui-tv-display.md` ("Transitions", "Sound assets", tasks UI-7, UI-10).

**This masterplan''s tasks are not implementation work: each of them writes the plan for one part below** (`pm plan add 6 …`), with that part''s tasks.

## Part 1: Preload the next screen''s media (UI-7), priority 500
- Today: `go()` in `app/client/src/game/Game.svelte` switches the screen behind the black and fades in at once (`PLACEHOLDER(UI-7)`, line ~117).
- Spec (04, "Transitions", step 4): the next screen mounts behind the black, its media and images preload, the fade-in waits for that, at most 2 s.
- What preloads: mainly the Question screen (`Question.svelte`: image, decorative background, video, audio via `/media?url=…`); check the other screens for images worth waiting for.
- Shape to decide in the plan: a preload helper (`Image.decode()`, `canplaythrough` for audio/video, timeout) that `go()` awaits, or a promise the next screen hands back. Constant for the 2 s cap in `timing.ts`.
- Missing or failing media must not block: timeout, then fade in as today (the «medio no disponible» chip stays).
- Done-when catch: `grep -rn PLACEHOLDER app/client/src` also hits `Placeholder.svelte` itself (comment + `PLACEHOLDER · {task}` tag), used only for the missing-media chip (`task="IMG"`, a runtime fallback, not unfinished work). The plan turns that chip into a plain notice (no `PLACEHOLDER` tag, own component or inline) and removes `Placeholder.svelte`, or the milestone''s grep never comes up empty. Update D-25 references (AGENTS.md "Placeholders" line, 04 "Implementation notes") to say none are left.
- Overlap: plan 21 (LUI-1) task 95 moves `Placeholder.svelte` labels into the i18n catalog (`placeholder.*`). Coordinate: whichever runs second adapts; note it in the plan.
- Check: throttled network / large video in the dev browser; the fade waits, never longer than 2 s.

## Part 2: Recorded sound effects (UI-10), priority 200
- Still synthesized (`app/client/src/game/sound.svelte.ts`, recipes from line ~480): whooshes (incl. «swoosh que sube»), pops (card pick), menu blips, joker shimmer, slide whistle (silbato), shredder (trituradora), heartbeat (latido), rewind (rebobinar), scope tick, cork shot, firework launch/cannon/sparkler/star sounds; still silent: Soplo''s paper rustle and the token pop-back (JK-9).
- Source: Kenney.nl CC0 packs first (e.g. Interface Sounds, UI Audio, Impact Sounds, Digital Audio), then Freesound CC0 / OpenGameArt; only D-45 allowlisted licences, CC0 preferred.
- Pipeline as in UI-10''s first rounds: trim, loudness-normalize, AAC `.m4a` via `nix shell nixpkgs#ffmpeg-headless` (not a project dependency); files in `app/client/public/audio/`, committed; row in `CREDITS.md` per file (CC0 too, for provenance).
- Wiring: add to `SAMPLE_NAMES` and `SAMPLE_FOR`; synthesized recipes stay as the fallback. Keep the folder small (current ~700 kB; set a budget in the plan).
- An audition aid for the TV check (a URL param like `/?fuegos=…` that plays every effect, or B-3''s «Demo de efectos») is the plan''s call; keep it minimal.
- Done when the gamemaster approves the effects on the TV.

## Part 3: Recorded music loops (UI-10), priority 190
- Still generated: `normal`, `question`, `submitted` (04, "Music"): one theme at three intensities, gapless loops, ideally same key and tempo family so the ~80 ms cuts between `question` and `submitted` don''t clash. `roll` and `victory` are already recordings.
- Harder than effects: needs a matched set of loops. Sources: Kenney.nl (music jingles/loops), OpenGameArt CC0, Freesound CC0; D-45 allowlist. If no matched set exists, options for the plan: one CC0 loop at three tempos/filters, or keep the synthesized loops; ask the gamemaster via a decision rather than guessing.
- Seamless loop points matter (`AudioBufferSourceNode.loop`, set `loopStart`/`loopEnd` if needed); test on the TV for clicks at the seam.
- Wiring in `sound.svelte.ts` (the music scheduler falls back to synthesis if a file is missing); `CREDITS.md` rows.
- Runs after part 2 (shared conventions, same audition aid).
- Done when the gamemaster approves the music on the TV; then UI-10 `[x]` in 04 and `plans/project.md` updated.

## Order and constraints
- Part 1 is independent of 2 and 3. Parts 2 → 3.
- D-45 licences only; everything offline; no new npm or Python dependencies.', '2026-10-11T21:54:56Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (7, 7, 'masterplan', 1000, 'Milestone 7 is S2 of the Steam track (D-34, `plans/11-steam.md`): it settles what the product is before anything Steam-specific gets built. Most of it is decisions, not code. Workers research each question, write the options with a recommendation as a pm decision, and record the gamemaster''s answer in `plans/decisions.md` (next free D-number). Then they resolve the question in `plans/open-questions.md` and update the owning plan file. The few S2 tasks that are code or files (MD-6, MD-7, PUB-4''s `LICENSE`) follow once their decision is in.

**The tasks of this masterplan are not implementation work: each one writes the plan for one part below** (`pm plan add 7 …`, priority as suggested), and that plan''s tasks do the work.

## How a decision part works (all parts 1–8)
- Prep task: read the owning plan file, gather the facts the options need (pool counts, prices, docs, licence terms), write the decision with `pm decision add` (recommended option first, body = context + trade-offs, ultra-short), then `pm task-pending-decision` on the follow-up task.
- Follow-up task (waits for the answer): D-entry in `decisions.md`; OQ moved to "Resolved" in `open-questions.md`; owning plan file updated (draft tables → decided, tasks `[x]` with a note); `plans/project.md` kept in sync.
- Workers never answer a decision themselves and never contact anyone outside the project (Valve, Freesound, a lawyer). If a part needs outside contact, it prepares the text and the gamemaster sends it.
- No Steam-specific code (S3–S6 are out of scope).

## Parts

1. **Desktop shell (OQ-29, SW-1)**
   - Owner: `plans/18-steam-integration.md` ("Desktop shell"): Electron + steamworks.js recommended, Tauri, browser + local server.
   - Refresh the facts before deciding: steamworks.js maintenance status and Electron support, install size, Deck/Proton notes, overlay in Electron. Fold in OQ-37''s answer if phones as buzzers need a LAN server inside the shell (note it in the decision as a dependency, not a blocker).
   - Done when: D-entry; SW-1 `[x]`; plan 18''s table marked decided; S3 tasks (SW-2..SW-6) still match the choice.
   - Suggested priority: 700.

2. **Default mode (OQ-30, MD-5)**
   - Owner: `plans/13-game-modes.md` ("Default mode"): joker presets per difficulty (draft table Fácil/Normal/Difícil/Experto), checkpoints (e.g. level 6 on Fácil), which levels count as won, which admin actions remain (no undo, no «Saltar y quemar para todos», «Reportar pregunta», «Abandonar partida»).
   - Must fit D-38 (four age groups, scale 1–15; `plans/21-age-groups.md`) and the age-group windows of milestone 5 (plans 27, 28): does a preset shift the window, or only the joker budget?
   - Decision may be split in two (presets + checkpoints; admin actions) if one is too big to answer at once.
   - Done when: D-entry; MD-5 `[x]`; plan 13''s default-mode section is a spec MD-6/MD-7 can implement.
   - Suggested priority: 600.

3. **«Reportar pregunta» and the mode/settings screen (MD-6, MD-7)**
   - Implementation, after part 2''s answer. MD-6: burn for everyone on this machine, local report list (a page the player can copy from), replacement draw. MD-7: mode and settings screen between Player and Level; the gamemaster mode reachable from it or a launch option; the family''s defaults unchanged.
   - Builds on the TS engine (milestone 2): depends on plan 20 "Engine game state machine (PORT-3)" and the save document (`SaveData`). If the engine hasn''t landed when this plan is split, its tasks wait for it (no second implementation in `app/server/game.py`).
   - Strings go through the catalog (milestone 3, plan 21 "t() helper and the es catalog").
   - Done when: in the default mode a report burns, lists and replaces; the settings screen starts a default-mode game with a preset; a gamemaster-mode game plays exactly as today.
   - Suggested priority: 500 (below plan 20 at 600).

4. **Launch languages and Spanish variety (OQ-31, I18N-1)**
   - Owner: `plans/15-i18n.md` ("Spanish varieties", "Model"), with 15a/15b/15c.
   - Options: Spanish only; Spanish + English; more. Spanish as Colombian today vs. neutral with Colombian variants. Facts to bring: Steam language shares (Steam hardware survey), translation cost per question (part 5 / `costs.log`), how much of the pool is Colombian-flavoured (`colombia` bundle vs. `base`, D-39, D-49), D-50''s localized name.
   - Done when: D-entry; I18N-1 `[x]`; 15/15a/15b note the launch languages; plan 24 "Draft en catalog (LUI-3)" checked against the answer (still needed or not).
   - Suggested priority: 500.

5. **Content target per new player and language (OQ-32, CT-1)**
   - Owner: `plans/16-content-target.md`. Needs parts 2 (joker budget → cards burned per game) and 4 (languages).
   - The simulation (CT-2, `qgen report --simulate`) belongs to S4 (milestone 9). In S2, decide the target in games per new player from an estimate: approved counts per level and age-group window today, D-52''s 5000 `base` target and its per-level targets (D-53), burns per game from the default preset. State that CT-2 verifies it later.
   - Also decide the quality bar''s draft numbers or point to milestone 1''s (D-56 spot checks, pm decision 2) instead of duplicating them.
   - Done when: D-entry; CT-1 `[x]` with a note that CT-2 confirms it; plan 16''s target section decided.
   - Suggested priority: 590 (after part 2).

6. **Price model and Steamworks account holder (OQ-33)**
   - Owner: `plans/17-publishing.md` ("Steamworks and store"). Options: paid (price band), free, free + paid packs (bundles as DLC, D-39); account held by a person or a company (tax interview, W-8BEN, $100 app credit).
   - Facts: Steam''s fees and payout rules, comparable trivia games'' prices; note what each option means for parts 7 (licence) and 8 (Freesound: "commercial").
   - Not legal or tax advice: the decision body says where a professional must check.
   - Done when: D-entry; PUB-6 and PUB-11 in plan 17 rewritten to match (they stay S5 tasks).
   - Suggested priority: 300.

7. **Code and content licence; is the pool public (OQ-35, PUB-4)**
   - Owner: `plans/17-publishing.md` ("Code and content license"). Needs part 6 (a paid game with a public pool is a different trade-off).
   - Options: code (MIT, GPL, all rights reserved) × questions (CC BY-SA, CC BY-NC, reserved) × repo (public, release content in a private repo/submodule, whole repo private). Respect media licences: they stay per file (plan 26 "Licence data in the pool", milestone 4).
   - After the answer: add `LICENSE` (and a content licence file if separate), mention it in `README.md` and `directory.md`.
   - Done when: D-entry; PUB-4 `[x]`; the licence files exist.
   - Suggested priority: 290 (after part 6).

8. **Competitive and couch co-op format and input (OQ-37)**
   - Owner: `plans/13-game-modes.md` ("Competitive mode", "Couch co-op") and `plans/14-input.md` (section 3, IN-7).
   - Only the format and input choice: relay ladder, parallel ladders, buzzer; hot-seat, one controller per player, phones as buzzers. Building it stays "Later" (MD-8, MD-9, IN-6); the decision notes the burn multiplier for part 5 and the shell needs for part 1.
   - Done when: D-entry; plans 13 and 14 say which format and input the later tasks build.
   - Suggested priority: 580.

9. **Freesound API for a commercial release (OQ-45)**
   - Owner: `plans/23-media-providers.md` (Freesound row, MP-6). Today: 9 questions in `authoring/data/questions.json` reference Freesound (6 in `app/data/pool.json`); the game ships the CC0/CC BY files, not the API.
   - Options: ask Freesound/UPF (the worker drafts the email, the gamemaster sends it); replace the Freesound picks with other allowlisted sources (D-45) and drop Freesound from the pipeline before release; keep it for the family only and exclude it from the Steam media bundle (SW-9).
   - Housekeeping: `open-questions.md` uses OQ-45 twice (the resolved one is D-42''s); give the Freesound question a free number and update the references.
   - Done when: D-entry; plan 23 and the provider order reflect the answer; if replacing, the replacement is a task in the plan (picks through the review tool, never by hand, D-36).
   - Suggested priority: 200.

10. **S2 close-out**
    - `plans/11-steam.md`: "Open questions" table resolved with D-numbers; S3–S6 phases and the track table updated to the answers (e.g. Electron vs. other shell, languages in S4''s exit, price in S5); ST-1 `[x]`.
    - `plans/project.md`, `plans/README.md` statuses (13, 15, 16, 17, 18 no longer stubs where decided); the masterplans of milestones 8–11 (plans 8–11) get a note if their scope changed.
    - Done when: the milestone''s "Done when" holds: OQ-29..OQ-37 and OQ-45 resolved in `decisions.md`, later phases in `11-steam.md` match.
    - Suggested priority: 150 (last).

## Order
- 1, 2, 4, 6, 8, 9 can be prepared in parallel; their decisions wait for the gamemaster.
- 2 → 3 (also needs milestone 2''s engine), 2 + 4 → 5, 6 → 7, then 10.

## Constraints (from the milestone)
- The gamemaster answers; workers prepare options and recommendations as pm decisions.
- Out of scope: S3–S6 (desktop build, release content, Steamworks, launch).', '2026-10-11T21:54:56Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (8, 8, 'masterplan', 1000, 'Milestone 8 is S3 of the Steam track (D-34, `plans/11-steam.md`): the first build a family can install and play without the gamemaster''s dev setup (no Nix, no Python, no browser). It wraps the built client in the desktop shell chosen in S2, saves to a file, and is playable with a controller only, including on the Steam Deck. A credits screen covers the licences. No Steamworks yet: the build runs without Steam (S5 adds the binding).

**The tasks of this masterplan are not implementation work: each one writes the plan for one part below** (`pm plan add 8 …`, priority as suggested), and that plan''s tasks do the work.

## Preconditions (other milestones; a part''s tasks stop and say so if one is missing)
- TS engine (milestone 2): screens on the engine (part 5, PORT-7) and the Store interface + `SaveData` (part 4, PORT-4/5). Plans 19 "Engine core" and 20 "Engine game state machine" today; parts 4–5 have no plan yet (tasks 58, 59). The shell must load the client without Python.
- Shell decision (OQ-29): plan 34 "Desktop shell (OQ-29)" (milestone 7). Parts 1–3 write their plans against the answer; until it is in, they assume nothing beyond "a Chromium-like window that loads `app/client/dist/`". If OQ-29 is still pending when a part''s plan task runs, it makes the task pending on that decision.
- Licence data per media file: plan 26 "Licence data in the pool" (milestone 4), for part 7.

## Rules for every part
- The family game at home (`trivia`, Python server + browser on the TV) keeps working after every task: same keys, same screens, same save (`ServerStore`).
- New shipped code goes under `app/` (D-35, e.g. `app/desktop/`); `directory.md` and `plans/19-repo-layout.md` updated with it. Nothing in `app/` reads `authoring/`.
- Dependencies: the shell and its builder only (OQ-29''s answer). Anything else (a gamepad library, a focus library, a glyph pack with code) needs a `pm decision`.
- Offline, no accounts, no telemetry. No Steamworks calls (S5).
- Owning plan files get their tasks `[x]` with a note (`18-steam-integration.md`, `14-input.md`, `17-publishing.md`); `plans/project.md` kept in sync.

## Parts

1. **Desktop shell skeleton (SW-2)**
   - Owner: `plans/18-steam-integration.md` ("Desktop shell").
   - Window, fullscreen by default with a toggle (F11 / menu), loads `app/client/dist/` without a server; a minimal preload bridge (no Node in the page).
   - Data and media without Python: the client''s data files (pool, categories, age groups, bundles) and `/media?url=…` (today `app/server/main.py` + `media_cache.py`) need a shell-side resolver, e.g. a custom protocol mapping a media URL to a file in a bundled media folder. Same URLs for the client in both setups, or one small adapter in `lib/`.
   - Dev on NixOS: the npm Electron binary doesn''t run there; the flake provides the shell runtime (e.g. `pkgs.electron`) and a dev command (`trivia-desktop`). Linux/Windows builds still use the builder''s binaries (part 3).
   - Done when: the dev command opens the game fullscreen and a whole game plays with media and sound, no Python process running.
   - Suggested priority: 480 (after M2''s PORT-7, ~500).

2. **File saves (SW-3)**
   - Owner: `plans/18-steam-integration.md`; interface from `plans/12-client-engine.md` (Store, `SaveData`, PORT-4).
   - `FileStore` behind the bridge: one JSON file in the shell''s user data folder (Steam Auto-Cloud later syncs it with no code); atomic write (temp + rename) with a retry for Windows file locks; corrupt or newer-version file → keep a backup, start fresh, show a message (strings through the catalog, milestone 3).
   - Optional: import a save file (the family''s `state/game.json`) — only if cheap; otherwise backlog.
   - Done when: players and burned questions survive a restart and a crash during write (throw-away script kills the process mid-write).
   - Suggested priority: 470 (after part 1).

3. **Local builds for Windows and Linux (SW-5, SW-6)**
   - Owner: `plans/18-steam-integration.md` ("Builds and depots").
   - Builder per OQ-29 (electron-builder in the draft): Windows x64 (installer or portable zip) and Linux x64 (AppImage or tar.gz; the Deck runs this one). Build steps: client build, `app/data/` export current (`qgen validate`), media bundled.
   - Media for S3: the approved media cache as is (`trivia-media sync --status approved`, ~720 MB) is fine for a local build; resizing/re-encoding is SW-9 (S5). Media is gitignored (D-17), so a CI build has no media: the plan decides (pm decision if unclear) whether CI builds without media (content added locally or as a later depot) or fetches it with `trivia-media sync`.
   - SW-6 CI in GitHub Actions: no secrets needed in S3 (no upload). If CI is more work than it''s worth before S5, the plan may move SW-6 to S5 via a decision.
   - Offline start test on a clean Windows machine and a Linux machine without Nix: written checklist; the gamemaster runs it (workers don''t own such machines).
   - Done when: `nix` or `npm` command produces both artefacts; each starts offline and plays a game.
   - Suggested priority: 460 (after parts 1–2).

4. **Action layer and focus navigation (IN-2, IN-3)**
   - Owner: `plans/14-input.md` (section 2).
   - Action layer in `app/client/src/lib/` (e.g. `input.ts`): `confirm`, `back`, `menu`, `answer(1..4)`, `joker(name)`, `navigate(dir)`; keyboard and mouse produce actions; screens listen only to actions. Replaces the `keydown` branches in `Game.svelte` and the dialogs (IN-1''s audit lists them). Keys unchanged for the family.
   - Focus model: spatial focus between controls, the sky-blue focus ring (D-29), focus memory per screen, focus never lands on the ☰ overlay button by accident (IN-1).
   - Independent of the shell; works in the browser setup too. New screens from milestones 5 and 7 (plans 29, 36) use it if they land later; if they landed earlier, this part converts them.
   - Done when: every screen and dialog plays with arrow keys + Enter + Esc/Backspace only; the family''s keys behave as before.
   - Suggested priority: 500 (client code; no dependency on the engine).

5. **Gamepad input and button glyphs (IN-4, IN-5)**
   - Owner: `plans/14-input.md`. Builds on part 4.
   - Gamepad API polling (`requestAnimationFrame` while a pad is connected), standard mapping (Steam Input presents an Xbox pad): D-pad/stick → `navigate`, A/B/Start → `confirm`/`back`/`menu`.
   - Design first (IN-4): direct answer buttons (A/B/X/Y on the Question screen) and joker access (bumpers, wheel or focus row); a pm decision with a recommendation if the plan can''t settle it from 14.
   - Glyphs follow the last-used device (keyboard letters, Xbox, PlayStation from `Gamepad.id`); art original or from a free set with a clear licence (D-45 style), listed for part 7.
   - Done when: a full game, every joker and every dialog work with an Xbox-style pad in Chromium on Linux and Windows; the prompts switch when the device changes.
   - Suggested priority: 490 (after part 4).

6. **Deck layout and controller-only text entry (SW-4)**
   - Owner: `plans/18-steam-integration.md` ("Platforms and display"), `plans/14-input.md` (Deck), `plans/04-ui-tv-display.md`.
   - Screen check of every screen at 1280×800 and 1280×720 (and 4K as a sanity check); text ≥ 9 px at 800p (Valve''s guideline); fixes in the `--u` system (D-29), no separate Deck layout unless needed.
   - Player name without a keyboard: the Steamworks on-screen keyboard is S5 (SW-8), so S3 needs an in-game letter picker or another controller-only way (pick existing player, preset names); the plan proposes one, pm decision if it changes the Player screen visibly for the family.
   - Done when: screenshots at both sizes pass (Playwright or the shell at a fixed window size); a new player can be created with a pad only.
   - Suggested priority: 380 (after parts 4–5 and the screen changes of milestones 5–6).

7. **Credits screen and generated `CREDITS.md` (PUB-5)**
   - Owner: `plans/17-publishing.md` ("Credits in the game").
   - Generated at build time from the pool''s licence data (plan 26) plus fixed lists: audio (`app/client/public/audio/CREDITS.md`, Elgar note), fonts (`app/client/public/fonts/`), glyphs (part 5), libraries (Svelte, the shell; their licences), and the code/content licence (OQ-35, plan 40) if decided. Generator lives in `app/` or the build step, not in `authoring/` if the shipped build runs it.
   - Screen reachable from the start screen or the ☰ overlay, scrollable with a pad (part 4); `CREDITS.md` in the shipped files.
   - Done when: every media file in `app/data/pool.json` appears with author, licence and source link; the build contains `CREDITS.md`; the screen works with keyboard, mouse and pad.
   - Suggested priority: 400.

8. **S3 close-out and platform test**
   - Test checklist for the gamemaster: Windows, Linux, Deck (Linux build; also via Proton if cheap), controller only, offline, a full game to level 12 or a loss, a restart keeps the save. Workers prepare it and record the results the gamemaster reports (pm decision "S3 test passed?" with the checklist in the body).
   - `plans/11-steam.md` S3 row done; 14, 17, 18 statuses and tasks; `plans/project.md`; `plans/README.md`. Masterplans of milestones 9–11 (plans 9–11) get a note if S3 changed their scope (e.g. SW-6 moved, media bundle needs).
   - Done when: the milestone''s "Done when" holds.
   - Suggested priority: 140 (last; below plan 43 "S2 close-out" at 150).

## Order
- Parts 4 → 5 → 6 can start before the engine lands (client only).
- Plan 34 (OQ-29) + M2 PORT-7 → part 1 → part 2 → part 3.
- Part 7 after plan 26 and part 5 (glyph credits); its screen needs part 4.
- Part 8 last.

## Out of scope (from the milestone)
- Steamworks (overlay, Cloud setup, achievements, on-screen keyboard, SW-7..SW-14), store page (S5); translations (S4); media resizing (SW-9, S5); couch co-op input (IN-6, IN-7, later).', '2026-10-11T21:55:09Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (9, 9, 'masterplan', 1000, 'Milestone 9 is S4 of the Steam track (D-34, `plans/11-steam.md`): enough reviewed questions, in every launch language, that a stranger''s family plays many evenings before questions repeat, plus a measurement that proves it. It needs translated UI catalogs, translated, re-rated and reviewed questions, regional packs (bundles, D-39), and `qgen report --simulate` passing the content target for every launch language. Today: 1136 approved (`base` 1035, `colombia` 101), Spanish only; milestone 1 takes `base` to 5000 (D-52).

**The tasks of this masterplan are not implementation work: each one writes the plan for one part below** (`pm plan add 9 …`, priority as suggested), and that plan''s tasks do the work.

## Preconditions (other milestones; a part''s plan task checks them first)
- OQ-31 launch languages + Spanish variety: plan 37 (milestone 7). OQ-32 content target: plan 38. Default preset → burns per game: plan 35 (OQ-30). Burn multiplier for several players: plan 41 (OQ-37). If a needed decision is still pending, the plan task makes itself pending on it (`pm task-pending-decision`) and stops.
- **If OQ-31 = Spanish only:** parts 3–7 shrink to nothing: their plan tasks drop with that reason (`pm task drop`), except what the Spanish variety needs (part 8). The rest still applies to Spanish.
- TS engine (milestone 2, plans 19, 20; screens on the engine PORT-7): the simulation runs on it. Age-group windows and bundle filter in the engine (plan 27, milestone 5): the simulation and the bundle filter (RG-3) use them.
- Catalog (milestone 3: plans 21, 22, 23, 24): `t()`, `es`, `xx`, draft `en`. Settings screen (plan 36, MD-7): the language setting goes there.
- Pool growth and QC (milestone 1: plans 12 targets, 13 gap-aimed drafting, 15 drift, 16 QC/D-56, 17 batch runs). This milestone reuses them per language; it doesn''t rebuild them.
- Licence/price (plans 39, 40: OQ-33, OQ-35): whether packs are DLC and whether release content (translations) stays public. A part that writes files depending on it checks the D-entry.

## Rules for every part
- Questions only through `qgen batch` (D-36). New pipeline steps (translate, re-rate, neutral Spanish) become `qgen batch` modes, with RUNBOOK and D-36 amended as an implementation task (like BN-11). Workers never edit pools or pick media by hand.
- Quality bar of plan 16 / D-56 applies per language: LLM audit + blind human spot check per batch; for a translation, the human is a native speaker (the gamemaster arranges them; workers prepare the sample and a pm decision "spot check done?").
- `app/` never reads `authoring/` (D-35): per-locale pools and category/bundle names are exported to `app/data/`.
- The family''s game keeps working after every task: Spanish, Colombia on, same keys (unless LUI-4 changes them by decision).
- Owning plan files get tasks `[x]` with a note (`15-i18n.md`, `15a`, `15b`, `15c`, `16-content-target.md`, `22-bundles.md`); `plans/project.md` in sync. Store page texts (LUI-6) are S5 (milestone''s out of scope); note it in 15a, don''t do it.

## Parts

1. **Simulation: games per new player (CT-2)**
   - Owner: `plans/16-content-target.md` ("Metric").
   - `qgen report --simulate [--locale L] [--bundles …] [--age-group G] [--preset P] [--players N] [--seeds K]`: a new player plays game after game on the TS engine (Node, `authoring/` imports `app/`) with the default preset''s joker use, until supply fails. Median and 10th percentile; strong-player bound (always reaches 12); bottleneck level and subcategory.
   - Pass/fail against the target of OQ-32''s D-entry, per launch language, default bundle set and every age group; exit 1 on fail. Feeds part 9 (gaps) and part 12 (exit).
   - No second referee in Python: if the engine can''t run under Node without the client, the plan decides the small adapter.
   - Suggested priority: 570 (after plans 20 and 27).

2. **Release quality bar and back-audit (CT-5)**
   - Owner: `plans/16-content-target.md` ("Quality bar"). D-56 covers new batches; the ~1100 questions approved before it never had an audit or a spot check.
   - Release bar: D-56''s numbers (pm decision 2) or stricter for release (pm decision if the plan proposes stricter); error limit and what happens to a batch above it.
   - Back-audit: `qgen audit` over the pre-D-56 approved pool in slices, through `qgen` (gamemaster asks, like `qgen rework`), findings → review tool (`audit=flagged`). Cost estimate first.
   - Suggested priority: 640 (after plan 16 at 650).

3. **Translation layout and schema (QT-1, I18N-3)**
   - Owner: `plans/15b-question-translation.md` ("Storage"; draft preference A: `authoring/data/questions.<locale>.json`, same ids, translated fields + own `difficulty`, `status`, `review`, `source_hash` for `stale`).
   - Also: `translatable: false` on source questions; translated category, subcategory and bundle names (`categories.json`, `bundles.json`, per bundle); `qgen export` writes `app/data/pool.<locale>.json` (+ names); `qgen validate` checks translations, `stale`, missing names. D-entry for the layout.
   - Suggested priority: 890 (schema; after plan 26 at 900, which also changes pool fields).

4. **Translation pipeline (QT-2, QT-3)**
   - Owner: `plans/15b-question-translation.md` ("Pipeline").
   - Steps `translate --to L` (adapt units, answer format, hints that play on Spanish words; detect non-travelling questions → propose `translatable: false`) → `rate --locale L` (difficulty for that language''s main market, D-38 scale) → `factcheck --locale L` → review (D-32/D-33) → audit (D-56) → merge into the locale file. Only `approved`, translatable sources; skips done ones; costs in `costs.log`.
   - Entry point `qgen batch --translate L` (size like a batch, picks untranslated approved sources, fewest translated subcategories first); RUNBOOK + D-36 amended. Prompts in `authoring/tools/prompts/` (new prompts are the gamemaster''s: drafted here, approved by pm decision).
   - Suggested priority: 700.

5. **Review tool for translations (QT-4)**
   - Owner: `plans/15b-question-translation.md` ("Review tool"); `authoring/ui`, `authoring/server`.
   - `/review?batch=…&locale=L`: source and translation side by side; same approve / needs work / reject; flag media with visible text per locale; blind spot-check sample mode per locale (plan 16''s sample mode, reused). Stats pages filter by locale.
   - Suggested priority: 400.

6. **Language setting and per-locale pool in the game (I18N-2)**
   - Owner: `plans/15-i18n.md` ("Model").
   - UI language and question language in the save (`SaveData`), default from `navigator.language` (the Steam language is S5, SW-*); on the settings screen (plan 36). Engine loads `pool.<locale>.json`; burns by id, so switching languages never repeats a question. Category/bundle names from the locale''s names. Supply check per locale.
   - Family: `es` fixed unless changed; the gamemaster mode unchanged.
   - Suggested priority: 480 (after plan 36 at 490).

7. **UI catalogs for the launch languages (LUI-4, LUI-5)**
   - Owner: `plans/15a-ui-translation.md`. Builds on plans 21, 23, 24 (draft `en`).
   - LUI-4: joker keys per language or neutral keys: pm decision with a recommendation (also gamepad glyphs from milestone 8, plan 45).
   - LUI-5: one catalog per launch language beyond `es`/`en` draft; playful joker names per language (pm decision per joker, like plan 24); fonts checked for each script (Latin only at launch, 15a); length check with `xx`; `/comodines` cards per language; native-speaker playtest per language (gamemaster runs it; workers write the checklist and a pm decision "playtest passed?").
   - Suggested priority: 390 (after plans 23, 24 at 400).

8. **Spanish variety (only if OQ-31 picks neutral Spanish)**
   - Owner: `plans/15-i18n.md` ("Spanish varieties").
   - A `qgen batch` mode (e.g. `--neutralize`) that rewrites Colombian wording in `base` to neutral Latin American Spanish, through review; `colombia` keeps its wording. If OQ-31 keeps Colombian Spanish: the plan task drops with that reason.
   - Suggested priority: 690 (tooling; the runs go to part 11).

9. **Cost, budget and generation plan by gap (CT-3, CT-4)**
   - Owner: `plans/16-content-target.md` ("Cost").
   - Cost per approved question (draft → approved) and per translated question (from part 11''s pilot) from `costs.log`; budget for the release per language as a pm decision before full runs.
   - Gap plan: the simulation''s bottlenecks (part 1) → release targets per language/age group in `authoring/data/targets.json` (D-53, extended per locale), read by `draft` (D-54) and `--translate`. No new mechanism if plan 13''s covers it.
   - Suggested priority: 560 (after part 1).

10. **Regional packs (RG-3..RG-5)**
    - Owner: `plans/15c-regional-questions.md` (superseded by bundles, D-39) and `plans/22-bundles.md`. RG-3 is BN-6 (plan 27, milestone 5) plus part 1''s `--bundles`; RG-4 is `qgen batch --bundle` (BN-11, done): mark them so.
    - RG-5: which packs launch and which bundles are on by default per language (e.g. `colombia` on for `es`, off elsewhere; is `colombia` translated?): pm decision with a recommendation from OQ-31 and OQ-33 (DLC or free). OQ-46 (`colombia` subcategories) answered first or folded in.
    - New bundles: `qgen bundle new`, their taxonomy for the gamemaster to approve (subcategory lists are the gamemaster''s); the batches go to part 11.
    - Suggested priority: 300.

11. **Release content runs**
    - The recurring `qgen batch` tasks: translation pilot (QT-5: 50 questions per language, measure reject rate and cost, go/no-go pm decision), then full translation per language (QT-6), neutral Spanish (part 8), regional pack batches (part 10), and `base` top-ups where the simulation fails after milestone 1''s 5000. Each batch followed by D-56''s QC (plan 16 procedure, `authoring/QC.md`), native-speaker spot checks for translations.
    - Order inside: pilot first (priority -90, above the runs, so part 9''s budget has its cost); full runs after milestone 1''s batch runs (plan 17) so translations don''t go stale.
    - Suggested priority: -110 (after plan 17''s -100).

12. **S4 close-out**
    - `qgen report --simulate` passes for every launch language (the milestone''s "Done when"); result recorded in `plans/16-content-target.md`.
    - `plans/11-steam.md` S4 row done; 15, 15a, 15b, 15c, 16 statuses and tasks; `plans/project.md`, `plans/README.md`; masterplans of milestones 10–11 (plans 10, 11) get a note if S4 changed their scope (store languages, DLC packs, install size of several pools).
    - Suggested priority: -130 (last, after part 11).

## Order
- Decisions first: plans 35, 37, 38, 41 (milestone 7) → parts 1, 3, 8, 10 can be written.
- Engine (M2) + plan 27 → part 1 → part 9.
- Part 3 → part 4 → part 5 → part 11''s pilot → part 9''s budget → full runs.
- Plan 36 + part 3 → part 6; plans 23/24 → part 7.
- Part 2 any time after plan 16. Part 12 last.

## Out of scope (from the milestone)
- Store page translations (LUI-6, S5); Steamworks language detection (S5); competitive mode and couch co-op (Later).', '2026-10-11T21:55:09Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (10, 10, 'masterplan', 1000, 'Milestone 10 is S5 of the Steam track (D-34, `plans/11-steam.md`): the desktop build from S3 (milestone 8) becomes a Steam app. That means a partner account and an App ID, the Steamworks binding (overlay, Cloud, achievements, on-screen keyboard, language), a shippable media bundle, depots uploaded with SteamCMD to a password-protected `beta` branch, and the store page with its disclosures, survey and price. The milestone is done when the family installs the beta from Steam on a second machine and plays it.

**The tasks of this masterplan are not implementation work: each one writes the plan for one part below** (`pm plan add 10 …`, priority as suggested), and that plan''s tasks do the work.

## Preconditions (other milestones; a part''s plan task checks them first)
- Decisions (milestone 7): OQ-33 price + account holder (plan 39), OQ-35 licence + public pool (plan 40), OQ-45/47 Freesound (plan 42), OQ-31 launch languages (plan 37), OQ-29 shell (plan 34). If a needed decision is still pending, the plan task makes itself pending on it (`pm task-pending-decision`) and stops. S2 close-out (plan 43) may have rewritten SW-*/PUB-* in plans 17/18: read the current files, not this summary.
- Desktop build (milestone 8): shell skeleton, `FileStore`, local builds (plans from tasks 209–211), gamepad + glyphs (plan 45), Deck layout + letter picker (plan 46), credits screen (plan 47), S3 platform test (plan 48). Part 3 adds to the shell; it doesn''t rebuild it.
- Licence data (milestone 4, plan 26): `CREDITS.md` and the media bundle read it.
- Content (milestone 9): which languages and bundles ship sets the store''s language table, the depots and the install size. Store texts per language (LUI-6) are this milestone''s (milestone 9 excluded them).
- If milestone 8 moved SW-6 (CI) or anything else to S5 (plan 48''s note), the part that owns it here takes it over.

## Rules for every part
- **Never phones home.** The game talks only to the local Steam client through the binding; no own server, no telemetry, no crash reporter, no auto-updater (Steam updates the game), no remote content. Network off must still play a full game.
- **No DRM:** the game runs without Steam running (family copy, offline living room). Every Steam call is optional; no `restartAppIfNecessary`. Without Steam, behaviour is S3''s (letter picker, `Gamepad.id` glyphs, browser language).
- **The gamemaster does what needs a person:** partner signup, tax/identity, payments, the Steamworks web UI, credentials, uploads that need Steam Guard, the Deck, the family test. Workers prepare checklists, exact field values and texts (in the owning plan file or a pm decision body) and record the result the gamemaster reports. Workers never enter credentials, never contact Valve, a lawyer or a tax advisor; text for them goes in a decision body.
- **Secrets never in git** (AGENTS.md): build account login, beta password, `steam_appid.txt` is fine (public), Steam Guard files are not. Gitignore what the upload script writes.
- The family game at home (`trivia`, browser on the TV) keeps working after every task.
- Shipped code under `app/` (D-35); dependencies: the Steamworks binding chosen with OQ-29 (steamworks.js in the draft) and nothing else without a pm decision.
- Owning plan files get tasks `[x]` with a note (`17-publishing.md`, `18-steam-integration.md`, `15a-ui-translation.md`, `14-input.md`); `plans/project.md` in sync.

## Parts

1. **Partner account, name check and AI terms (PUB-6, PUB-7, PUB-10)**
   - Owner: `plans/17-publishing.md` ("Steamworks and store", "AI disclosure").
   - PUB-6: signup checklist for the holder decided in OQ-33 (person/company, tax interview form, bank, $100 app credit); the gamemaster does it; result (App ID) recorded via pm decision "Steamworks app created? App ID?".
   - PUB-7: name and trademark check for «Living Room Trivia» / «Trivia en Familia» (D-50): Steam store search, EUIPO/USPTO/WIPO, domains; findings in a pm decision; if it fails, OQ-34 reopens (new decision, stores names wait).
   - PUB-10: Anthropic''s commercial-use terms for the pipeline''s outputs (`claude -p` on the author''s plan type); one-line finding + source in plan 17; anything unclear → decision body for a professional.
   - Suggested priority: 720 (everything else needs the App ID; the name before the store page).

2. **Steamworks app configuration (SW-7)**
   - Owner: `plans/18-steam-integration.md` ("Builds and depots", "Steam features").
   - Exact values for the gamemaster, as a checklist in plan 18: App ID, localized names (D-50), depots (Windows, Linux, shared content; language/bundle depots only if milestone 9 or OQ-33 call for them), launch options per OS (executable, args, e.g. the mode flag of plan 36), supported languages (OQ-31), branches `default` + password-protected `beta`, controller support flags, Steam Input default config (gamepad template), Deck settings.
   - Steam Cloud: Auto-Cloud root and pattern per OS for the `FileStore` file (Electron `userData`: `%APPDATA%` / `~/.config`); quota; what happens on a conflict (one JSON file: Steam''s conflict dialog; local wins by default). `steam_appid.txt` for dev runs.
   - Done when: the gamemaster confirms the values are entered (pm decision); plan 18 holds them.
   - Suggested priority: 700.

3. **Steamworks binding in the shell (SW-8)**
   - Owner: `plans/18-steam-integration.md` ("Steam features"); touches `14-input.md`, `15-i18n.md`.
   - Binding in the shell''s main process (steamworks.js or OQ-29''s alternative), exposed through the preload bridge as one optional `steam` object; the page checks `steam?.available`. Init failure (no Steam, wrong App ID, offline) → silent fallback.
   - Overlay in Electron (known workarounds; Windows and Deck); on-screen keyboard (`ShowFloatingGamepadTextInput`) for the player name under Steam, letter picker stays the fallback (plan 46); per-device glyphs via `GetInputTypeForHandle` where they beat `Gamepad.id` (plan 45); default UI/question language from the Steam language (I18N-2''s setting from milestone 9 wins once set); rich presence «Nivel 7 de 12» optional (strings via `t()`).
   - Dev on NixOS: test with the real App ID or Spacewar (480); the binding''s native library from the npm package in the builds, from the flake in dev (like part 1 of masterplan 8).
   - Done when: under Steam the overlay opens, the keyboard fills the name, the language follows Steam; without Steam a full game plays as in S3.
   - Suggested priority: 690.

4. **Steam Cloud saves**
   - Owner: `plans/18-steam-integration.md` ("Steam features"); save format from `plans/12-client-engine.md`.
   - Auto-Cloud only (no Cloud API code) unless the test shows a need. Check: `FileStore`''s atomic write (temp + rename) leaves only the real file in the synced pattern; temp/backup files excluded; one save per OS user vs. per Steam user (decide; pm decision if it changes behaviour for two Steam accounts on one PC).
   - Test checklist for the gamemaster: play on machine A, quit, start on machine B (Windows ↔ Linux/Deck) → players and burns there; offline on both then online → conflict dialog behaves.
   - Suggested priority: 680 (after parts 2–3).

5. **Achievements (SW-11)**
   - Owner: `plans/18-steam-integration.md` ("Steam features").
   - List (few, no grind; plan 18''s draft: first victory, a win without jokers, a win on Experto, every broad category answered, level 12 in each preset), each with its exact trigger as an engine event (preset names from OQ-30''s D-entry; gamemaster mode counts or not: decide in the plan). Names and descriptions per launch language.
   - Unlock through part 3''s bridge; offline unlocks are cached by Steam; nothing in the save depends on Steam. Optional: unlock retroactively from the save on first start under Steam.
   - Icons: 64×64 achieved + unachieved, original art (credits, plan 47); Steamworks setup values in plan 18 for the gamemaster.
   - The list goes to the gamemaster as a pm decision before icons are made.
   - Suggested priority: 590.

6. **Media bundle for shipping (SW-9)**
   - Owner: `plans/18-steam-integration.md` ("Platforms and display" → media size); `plans/23-media-providers.md`.
   - Build step that turns the approved media cache into the shipped bundle: images ≤ 3840 px wide (D-48), WebP/AVIF, < 1 MB target; audio → Opus; video re-encoded; size budget per depot; `trivia-media` (`app/`, no `authoring/` imports) gains the command and a check that fails over budget or on a missing file.
   - Same lookup keys as the cache (D-17) so the shell''s media resolver (masterplan 8 part 1) needs no change, or one adapter.
   - Applies the Freesound answer (plan 42: exclude or replace) and the licence rules (GFDL/PD-US replaced in milestone 4); `CREDITS.md` lists exactly the shipped files.
   - Suggested priority: 640 (before part 7; a build step, not asset work).

7. **Builds, depots and upload (SW-10, SW-6 if moved)**
   - Owner: `plans/18-steam-integration.md` ("Builds and depots").
   - SteamCMD app/depot VDFs in the repo (no secrets), one upload command (e.g. `trivia-steam upload --branch beta`) that builds from a clean tagged commit, runs `qgen validate` and `npm run check`, builds both platforms + the media bundle, and calls `run_app_build`. SteamCMD from nixpkgs (unfree) or Valve''s SDK tools; the plan decides.
   - Where it runs: the author''s machine first (recommended; Steam Guard once, no CI secrets); CI upload only with a pm decision. The dedicated build account is the gamemaster''s.
   - `beta` branch: password with the gamemaster, never in git; `default` stays empty until S6.
   - Suggested priority: 620.

8. **Store page and AI disclosure (PUB-8, LUI-6)**
   - Owner: `plans/17-publishing.md` ("Steamworks and store", "AI disclosure"); `plans/15a-ui-translation.md` (LUI-6).
   - Texts per launch language: short and long description, feature list, system requirements (from part 7''s builds), controller support, privacy line ("collects nothing, sends nothing"), AI disclosure (pre-generated questions drafted and fact-checked by Claude, reviewed per D-32/D-33/D-56; no live AI; images by people from Commons) using PUB-10''s finding. Drafts in a file under `plans/` or `docs/`; the gamemaster approves via pm decision and pastes them in.
   - Assets: capsule sizes per Valve''s current list, screenshots (shell at 1920×1080, scripted where possible), trailer optional (backlog unless cheap). Who makes capsule art (gamemaster, commissioned, or AI-made, which then needs disclosing) is a pm decision.
   - Suggested priority: 300.

9. **Content survey, rating and price (PUB-9, PUB-11)**
   - Owner: `plans/17-publishing.md`.
   - Survey answers drafted from the game (no violence, gambling, user content; question topics that may need a note, e.g. history of wars); IARC optional per Valve.
   - Price and regional prices from OQ-33''s D-entry (Valve''s matrix); DLC entries if bundles are paid DLC. The gamemaster enters both; result via pm decision.
   - Suggested priority: 290 (after part 8).

10. **Steam Deck test and Deck Verified (SW-12)**
    - Owner: `plans/18-steam-integration.md` ("Steam Deck Verified"), `plans/14-input.md`.
    - Checklist on a real Deck with the Steam-installed beta: Valve''s Verified criteria (controller glyphs, on-screen keyboard, text ≥ 9 px at 800p, no launcher, default config works, no warnings on start), Cloud sync with a PC, suspend/resume. Builds on plan 48''s S3 rows; no copy.
    - Request the review once the store page exists (or note it for S6 if Valve requires release first; check the docs).
    - Suggested priority: 370.

11. **Beta test and S5 close-out**
    - Beta test: the gamemaster installs the `beta` branch from Steam on a second machine (not the dev machine), offline start, family plays a full game; Cloud carries the save to another machine. Workers write the checklist into plan 18 and record the result (pm decision "S5 beta test passed?"); failures become tasks in the owning parts.
    - Docs: `plans/11-steam.md` S5 row done; SW-13 (Remote Play Together, needs IN-6, Later) and SW-14 (macOS, later) marked deferred with a note, not done; 17, 18, 15a statuses; `plans/project.md`, `plans/README.md`; masterplan 11 (plan 11) gets a note if S5 changed S6''s scope (coming-soon page needs part 8, App ID, names).
    - Done when: the milestone''s "Done when" holds.
    - Suggested priority: 130 (last; below plan 48 at 140).

## Order
- Part 1 first (App ID, names, terms) → part 2 → parts 3, 4, 7.
- Part 3 → part 4 (Cloud test) and part 5 (unlocks).
- Part 6 → part 7 → first `beta` upload → part 10 and part 11.
- Part 1 (PUB-7, PUB-10) → part 8 → part 9.
- Part 11 last.

## Out of scope (from the milestone)
- Public release: coming-soon page, wishlists, release checklist, patches (S6, milestone 11). Remote Play Together (SW-13) and macOS (SW-14): later. Marketing.', '2026-10-11T21:55:09Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (11, 11, 'masterplan', 1000, 'Milestone 11 is S6 of the Steam track (D-34, `plans/11-steam.md`, ST-3..ST-5): the Steam app from S5 (milestone 10) goes public. That means a "Coming soon" page that collects wishlists, a release checklist that every public build passes, the launch itself, and a way to ship content updates as patches and take in question reports without telemetry. The milestone is done when the game is released and the first content update has gone out as a patch.

**The tasks of this masterplan are not implementation work: each one writes the plan for one part below** (`pm plan add 11 …`, priority as suggested), and that plan''s tasks do the work.

## Preconditions (other milestones; a part''s plan task checks them first)
- Milestone 10 (S5), masterplan 10 (plan 10): App ID and names (part 1), app config + branches (part 2), media bundle (part 6), builds + upload command (part 7), store page + AI disclosure (part 8), survey + price (part 9), Deck test (part 10), beta test (part 11). Their plans may not exist yet: read `pm plan list` and plans 17/18, not this summary. S6 adds to the upload command; it doesn''t rebuild it.
- Milestone 7 decisions: OQ-33 price + account holder (plan 39), OQ-35 licence + public pool (plan 40). If a needed decision is still pending, the plan task makes itself pending on it (`pm task-pending-decision`) and stops.
- Milestone 9 (S4): content target met for every launch language (plan 38, `qgen report --simulate`); the release waits for it.
- «Reportar pregunta» (MD-6, plan 36): the local report list part 5 builds on.
- Credits (PUB-5, plan 47) and licence data (plan 26): part 3''s "credits complete" check reads them.

## Rules for every part
- **Never phones home.** No update check, no crash reporter, no report upload, no analytics, no remote content. Steam delivers updates; reports reach the gamemaster only when a player sends them by hand.
- **The gamemaster does what needs a person:** Steamworks web UI (coming-soon request, release date, the Release button, events/announcements), Valve''s store and build reviews, uploads that need Steam Guard, the Deck, the family test, answering players. Workers prepare checklists, exact texts and field values (owning plan file or a pm decision body) and record the result the gamemaster reports. Workers never enter credentials or contact Valve or players.
- **Secrets never in git** (AGENTS.md): build account, beta password, Steam Guard files.
- The family game at home (`trivia`, browser on the TV) keeps working after every task; a patch never breaks a save.
- Shipped code under `app/`, release tooling under `authoring/` or the flake (D-35); no new dependency without a pm decision.
- Owning plan files get tasks `[x]` with a note (`11-steam.md` ST-3..ST-5, `17-publishing.md`, `18-steam-integration.md`); `plans/project.md` in sync.

## Parts

1. **"Coming soon" page (ST-3)**
   - Owner: `plans/11-steam.md` (ST-3); store texts in `plans/17-publishing.md` (PUB-8).
   - Needs: masterplan 10 part 8 (store page approved by the gamemaster), part 1 (names cleared, App ID), part 9 (survey).
   - Checklist for the gamemaster: store page complete, submit for Valve''s store review, fix what Valve returns, then "Coming soon" with a release date or "to be announced"; record the date it went live (pm decision "Coming soon page live? date?").
   - Timing: Valve requires the page live at least two weeks before release (check the current rule in the Steamworks docs, note the source); aim for longer. The release date in part 4 counts from this date.
   - Wishlists: only what Steam offers itself (wishlist button, follow); no mailing list, no own website, no marketing (out of scope).
   - Suggested priority: 450 (first in time; mostly gamemaster steps).

2. **Version numbers and patch-safe saves**
   - Owner: `plans/18-steam-integration.md` ("Builds and depots"); save format in `plans/12-client-engine.md`.
   - One version per release (semver; today `0.1.0` in `flake.nix`): one source of truth, stamped into the build, shown on the credits/settings screen and in the report text (part 5). Pool version (export hash or tag) next to it.
   - Git tag per release (`v1.0.0`); the Steam build description = tag.
   - Saves across patches: a patch may add, fix or drop questions. Burns and history keyed by question id must survive: unknown ids are ignored, not errors; a dropped question never comes back as "new"; save format version + migration if the shape changes. Check what the engine (milestone 2) already does; add only what''s missing, with a throw-away script that loads an old save against a new pool.
   - Suggested priority: 600 (core; part 3 checks it).

3. **Release checklist (ST-4)**
   - Owner: `plans/11-steam.md` (ST-4); upload command from masterplan 10 part 7.
   - Automated, in one command (extend the upload command, e.g. `trivia-steam release-check`, or a flag of it): clean tree on a tagged commit matching part 2''s version; `qgen validate` clean; `npm run check`; pool export fresh; credits complete (every shipped media file, font, sound, glyph and library has an entry in `CREDITS.md`/`credits.json`, nothing extra); media bundle within budget; both platform builds succeed. Fails loudly, prints what''s left for the human.
   - Manual, as a checklist in `plans/11-steam.md` with the result via one pm decision per release candidate: offline test (network off, Steam off, full game to level 12 or a won checkpoint), Deck test (reuse masterplan 10 part 10''s rows), Windows test, Cloud sync, family sign-off (they play the release candidate from the `beta` branch).
   - Same checklist for every later patch; a short "patch" variant (skip what a content-only patch can''t break) is allowed if the plan says why.
   - Suggested priority: 700.

4. **Launch**
   - Owner: `plans/11-steam.md` (S6 row).
   - Release candidate: tag, upload to `beta`, run part 3, family sign-off; then Valve''s build review (check current lead time in the docs) and the gamemaster sets the build live on `default` and presses Release on the date from part 1.
   - Launch-day checklist: price and discounts from OQ-33 (masterplan 10 part 9) live; store languages match the build; Steam discussions open with the report thread from part 5 pinned; a launch announcement text drafted per launch language (gamemaster posts it).
   - First week: watch the discussions and reviews by hand (gamemaster); bugs become tasks in `plans/backlog.md`; a hotfix goes through part 3.
   - Result via pm decision "Released? date, build id".
   - Suggested priority: 160 (after every other part except 7; above plan 48 at 140 is fine since milestone 10 gates it).

5. **Question reports by hand (ST-5)**
   - Owner: `plans/11-steam.md` (ST-5); in-game part in `plans/13-game-modes.md` (MD-6).
   - Channel: a pinned Steam discussions thread (recommended) and/or an email address shown in the game; pm decision for the gamemaster (an email address in a public game is personal data of the gamemaster).
   - In the game: the MD-6 report list page offers "copy" text per report and for all of them: question id, language, version + pool version (part 2), the player''s reason if any; plus where to send it (no link that opens a network request on its own; a `mailto:` or Steam overlay URL only on a click, and only under Steam if overlay). Strings via `t()` for every launch language.
   - In authoring: one way to turn a pasted report into a `needs_work` flag with the report as review note (a `qgen` command or the review tool''s existing form; reuse `qgen rework` for the fix). No new storage beyond `authoring/data/questions.json`.
   - Suggested priority: 550 (client + small authoring tool; before launch).

6. **Content updates as patches (ST-5)**
   - Owner: `plans/11-steam.md` (ST-5); `plans/16-content-target.md` for what a patch adds.
   - Cadence: a pm decision for the gamemaster (e.g. monthly, or every N new approved questions per launch language, plus hotfixes for wrong answers any time); the plan records the answer.
   - Patch = new version (part 2) + part 3 + upload: new approved questions (batches as usual, `qgen batch`), fixes from part 5, dropped questions; never changes rules or saves silently.
   - Patch notes: a `qgen` command that diffs the pool between two tags (added/fixed/dropped per language and category) and drafts the note; the gamemaster posts it as a Steam event/announcement.
   - Done when: the first content patch after launch went out through this path (pm decision with version and date).
   - Suggested priority: 250.

7. **S6 close-out**
   - Docs: `plans/11-steam.md` (ST-3..ST-5 `[x]`, S6 row done, status), `plans/17-publishing.md` and `plans/18-steam-integration.md` leftovers marked done or deferred with a note, `plans/project.md`, `plans/README.md`, `README.md` (how to cut a release, how to send a patch: commands for humans).
   - Leftovers go to `plans/backlog.md` (competitive mode, couch co-op, more regions/languages, SW-13, SW-14).
   - Done when: the milestone''s "Done when" holds.
   - Suggested priority: 120 (last).

## Order
- Part 2 → part 3 → part 4 (release candidate) and part 6.
- Part 1 at least two weeks (better months) before part 4''s release date; it can start as soon as masterplan 10 part 8 is approved.
- Part 5 before part 4 (the report thread and the copy text ship in the launch build).
- Part 6 after part 4; part 7 last.

## Out of scope (from the milestone)
- Competitive mode, couch co-op, more regions and languages (later); Remote Play Together (SW-13), macOS (SW-14); marketing beyond Steam''s own wishlist and follow features; any telemetry or online reporting.', '2026-10-11T21:55:09Z', NULL);
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

## Baseline (2026-10-11, `qgen report --calibration batch-7 batch-8`)
- Columns: drawn slots · mean concept `known_at` (all slots) · drafts · mean drafted / rated / final difficulty (all drafts, revised ones included) · merged · approved.
- batch-7 (rated, merged, reviewed):
  - target 1–3: known_at 8.2 / 7.4 / 7.0; drafted 3.6 / 3.7 / 4.1; rated 3.6 / 3.7 / 4.1; final 3.6 / 3.7 / 3.9 (too hard at the bottom)
  - target 4–8: drafted 5.3 / 6.0 / 6.9 / 7.6 / 7.6; final 5.2 / 6.0 / 6.7 / 7.8 / 7.8 (roughly on target, 8 one low)
  - target 9–10: known_at 9.7 / 9.9; drafted 8.8 / 8.7; rated 8.5 / 8.2; final 9.0 / 8.8
  - target 11–12: known_at 10.1 / 10.7; drafted 9.9 / 10.0; rated 9.2 / 8.9; final 10.1 / 10.3
  - target 13–15: known_at 10.8 / 10.7 / 10.8; drafted 11.2 / 11.3 / 11.8; rated 10.4 / 10.0 / 10.8; final 11.3 / 11.5 / 12.1
  - 712 drafts, 616 merged, 568 approved; known_at 7.0–8.6 at targets 1–8
- batch-8 (drafted only; rated and final numbers pending until it''s rated):
  - drafted 5.1 / 4.3 / 5.3 at targets 1–3 (worse at the bottom); 6.6 / 6.1 / 7.0 / 7.8 / 8.6 at 4–8
  - drafted 9.5 / 9.8 / 10.6 / 11.6 at 9–12; 12.1 / 12.6 / 13.2 at 13–15 (closer at the top)
  - known_at 8.4–9.4 at targets 1–5, 11.5–11.6 at 13–15
- The concept draw (`concepts.draw_concepts`, weight `1/(1+uses)² / (1+|known_at−d|/2)`) is dominated by use count; `known_at` hardly matters.
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
- Candidate finder (task 40, `overlap_candidates()` in `qgen.py`), replay: recall 6/6 (the four batch-7 pairs against ids < q-0596 plus earlier batch-7 questions; B-5''s two against the pool before their batch).
  - Matched by: same answer (Almenas, constelaciones, Ramen, Hungría), the pool question''s text («yo soy tu padre»; «silleteros» in q-0328).
  - batch-7, 616 merged: candidates per draft mean 1.9, median 1, max 8 (cap; 36 drafts at cap); 419 with at least one.
  - Answers with digits, not only pure numbers, excluded (7.000 años ~ 9.000 años).
  - `qgen report --overlaps` on the approved pool (1136): 1490 pairs, 47 same answer, 101 similar answer, 26 same stem, the rest text containment (noisy: «Bogotá» in a fun fact). Sorted strongest first.

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
  - `soak-<n>` only: `db` on every 10th and the last step, absent on the others (size); the recorder still asserts errors leave the DB unchanged.
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
- `soak-<n>`: ~10 seeded random walks of legal actions picked from the view (incl. jokers, undo, admin skip, new players), 30–40 steps each (size), choices from `random.Random("soak-<n>")`, not the tape; `soak-10` on the tight pool; to catch paths the scripted ones miss.
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
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (21, 3, 't() helper and the es catalog (LUI-1)', 500, 'Every on-screen string of the game moves into a typed `es` catalog read through a small `t()` helper, with no visible change in Spanish. Part 1 of plan 3 (masterplan M3); design source `plans/15a-ui-translation.md` (LUI-1). Parts 3 (pseudo-locale `xx`, LUI-2) and 4 (draft `en`, LUI-3) build on it; part 2 (server errors as codes) puts its error keys into the same catalog.

## Design
- `app/client/src/lib/i18n.ts`, no library:
  - `t(key, params?)`: dotted key (`"joker.hint.name"`), `{name}` placeholders replaced from `params`.
  - Plurals: a catalog value may be `{ one, other, … }` (an `Intl.PluralRules` category map), picked by `params.n`.
  - Numbers in params go through `Intl.NumberFormat(lang)`; strings as is.
  - `variants(key)`: the `string[]` of a variant entry (milestone/consolation lines); `copy.ts` keeps `choose()` and the seed logic.
  - Missing key at runtime: returns `⟦key⟧` (part 3 builds on it); static side is the type check.
  - `lang`: `"es"` by default; `?lang=xx` override only when `import.meta.env.DEV` (parts 3, 4). No language menu (OQ-31).
  - Sets `document.documentElement.lang` and `document.title` from the catalog at startup (`index.html` keeps `<title>Trivia</title>` as the pre-JS fallback).
- `app/client/src/locales/es.ts`: nested object `as const satisfies`-style; `export type Catalog` derived from it with string leaves widened (so `en` may differ in wording and variant count). `Key` = union of dotted leaf paths, so `t("typo")` fails `npm run check`.
- Namespaces (suggested): `app`, `screen.*` (start, player, level, select, question, result, victory), `joker.<id>` (`name`, `key`, `hint`, `aria`), `overlay`, `copy.milestone.<level>`, `copy.consolation.<maxLevel>`, `error` (empty, filled by part 2), `a11y` for `aria-label`/`title` not covered elsewhere.
- Joker keys (`S`, `P`, `F`, `T`, `X`) move into the catalog as `joker.<id>.key` but keep today''s values; key handling reads them from there (LUI-4 decides later).
- Sound cues: `sfx(name: string)` with regex on Spanish descriptions becomes `sfx(cue: Cue)`, `Cue` a union of neutral ids (`"applause"`, `"applause-big"`, `"sad-trombone"`, `"padlock-close"`, `"menu-open"`, `"joker-armed"`, …); `SAMPLE_FOR` and `RECIPES` become `Record`/`Map` lookups by cue id. The level thud takes the level as an argument (`sfx("block", { level })` or `sfx(\`block-${n}\`)` typed). Sample file names in `public/audio/` stay (asset paths, not text). Same sound for every call site as today.
- Comments may keep Spanish names in «…» (not on screen); the check ignores comments.
- Log the catalog shape as a decision in `plans/decisions.md` (next free D-number) in task 1.

## Coordination with part 2 (server errors as codes)
- Part 2''s plan adds `error.<code>` keys to `es.ts` and switches `Game.svelte`''s `error` display to `t()`. This plan leaves the server message display as is and doesn''t touch `app/server/`.
- Whichever runs second rebases onto the other''s catalog; key namespace `error` is reserved for part 2.

## Tasks (one per worker run, in this order)
1. Helper + catalog skeleton: `lib/i18n.ts`, `locales/es.ts` with `Catalog`/`Key` types, `?lang` dev override, `document.title`/`lang`; move `copy.ts` arrays into `copy.*` (`milestone()`/`consolation()` unchanged in behaviour). Decision entry in `plans/decisions.md`; `directory.md` (new `lib/i18n.ts`, `locales/`).
2. Sound cues to neutral ids: `sound.svelte.ts` (`Cue` type, lookup tables) and every `sfx(...)` call site (`Game.svelte`, `Question.svelte`, `Shredder.svelte`, `Fireworks.svelte`). Check: each cue plays the same sample/recipe as before (throw-away mapping script or a side-by-side list in the task note).
3. Jokers: `JokerTray.svelte` (names, key hints, aria), `JokerFlight.svelte`, `CategoryPicker.svelte`, `DifficultyDial.svelte`, `Shredder.svelte`; key handling in `Question.svelte` reads keys from `joker.<id>.key`.
4. `Question.svelte`: all remaining text (hints «Soplo {n}», «Respuesta final», buttons, aria/title).
5. `Game.svelte` and `Player.svelte`: screen texts, greeting, start/level/result/victory, aria/title. Also leftovers in `Stage.svelte`, `swap.ts`, `timing.ts` if any are strings (today only comments).
6. `Overlay.svelte` (admin overlay); then the check and close-out:
   - A kept script `app/client/scripts/check-literals.mjs` (`npm run check:literals -w app/client`): strips `//`, `/* */`, `<!-- -->` comments in `app/client/src/game`, flags Spanish characters (`áéíóúñÁÉÍÓÚÑ¡¿`) and text between tags or in `aria-label`/`title`/`placeholder` attributes that isn''t a `{…}` expression. Exit 1 with file:line. Document it in `README.md`/AGENTS.md command list.
   - Screen-by-screen before/after comparison (screenshots of start, player, level, select, question incl. every joker, result, victory, overlay) shows no visible change.
   - Mark LUI-1 `[x]` in `plans/15a-ui-translation.md`, update `plans/project.md` (M3 status).

## Every task
- `npm run check` and `npm run build` pass.
- No visible change in Spanish: same text, same punctuation (`¡`, `¿`, «»), same `aria-label`/`title`.
- No new dependencies.

## Out of scope
- `?lang=xx` content (part 3), `en.ts` (part 4), server error codes (part 2).
- Joker keys per language (LUI-4), translating questions/categories/bundle names, `authoring/` pages and `/comodines`.', '2026-10-12T00:08:37Z', 81);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (22, 3, 'Server errors as codes', 710, 'The game server stops sending Spanish error texts: every `GameError` carries a stable code plus params, and the client turns it into Spanish through the catalog of part 1 (plan 21, LUI-1), with no visible change. Part 2 of plan 3 (masterplan M3). Without it, error lines in the corner and the joker trays'' «why not» reasons stay Spanish outside the catalog.

## Priority and order
- Plan priority 710, not 700: plan 18 (PORT-1, milestone 2) records the HTTP error bodies into fixtures at 700 and sorts first at equal priority. Landing codes first means the fixtures carry codes and the TS engine (plan 20, PORT-3) throws the same codes; no re-recording.
- If PORT-1 fixtures already exist when task 1 runs: re-run `authoring/tools/record_fixtures.py` in task 1 and commit the new fixtures.
- Part 1 (plan 21, priority 500) doesn''t exist yet when task 1 runs. So: task 1 puts the Spanish texts in an interim client map (`app/client/src/lib/errors.ts`); task 2 waits for part 1 (priority 490, after plan 21''s tasks) and moves them into `es.ts` under `error.*`. Plan 21 reserves the `error` namespace for this.

## Design
- `app/server/game.py`:
  - `GameError(code, params=None, details=None)`: `code` a snake_case string, `params` a JSON-safe dict, `details` as today (supply report).
  - `ERRORS = {code: "English template with {param}"}`; `str(e)` = the filled English text (logs, `trial`, authoring side). Unknown code = bug, assert in `__init__`.
  - Re-raises keep their own code (`back_to_select`, `play_snipe`): `raise GameError("purge_short") from None`.
- Responses (`app/server/main.py`, every route that catches `GameError`: `GET /api/game` 400, `game_action` 409, `/api/players/delete` 409): `{"error": code, "params": {...}, "message": english, "supply": details}`.
  - `not found` (404) and the 500 handler: `{"error": "not_found" | "server_error", "message": …}` (English as today).
  - `/api/flags` `ValueError` stays as is (English, dev-only).
- Joker availability: `trial()` returns `{"code", "params"}` or None; `jokers_view` reasons become that object (incl. the literal Cambiazo reason → `category_none`, and `SPENT` → `joker_spent`). `types.ts`: `reason: ErrorInfo | null`, `ErrorInfo = { code: string; params: Record<string, string | number> }`.
- `SPENT` dict goes away; `joker_spent` with `{joker}`; client key per joker (`error.joker_spent.<id>`), so «ya no les quedan Bájales» etc. stay word for word.
- Client:
  - `lib/api.ts`: `GameError` gets `code`, `params`, `message` (English); `json()`, `playJoker`, `gameAction` all throw it when the body has `error`. Network failure (`call`) and bodies without `error` stay plain `Error` as today.
  - `errorText(e: unknown): string`: GameError with a known code → Spanish text; unknown code or plain Error → its message (as today).
  - `Game.svelte` (every `error = …`), `JokerTray.svelte` (reason), `Question.svelte` (purge reason), `Player.svelte` if it shows delete errors: use `errorText`/reason rendering.
- Only player-facing codes get Spanish text; codes whose text is English today (malformed requests, admin/dev states) keep the English `message` on screen, so nothing visible changes. Mark them `internal` in the table.

## Every `GameError` today → code
| where (`game.py`) | text today | code | params |
|---|---|---|---|
| `clean_name` | falta el nombre del jugador | `name_missing` | |
| `clean_name` | el nombre es demasiado largo (máximo 30 letras) | `name_too_long` | `max` |
| `delete_player` | no hay ningún jugador «{name}» | `player_unknown` | `name` |
| `running` | no game is running (internal) | `no_game` | |
| `draw` | no quedan preguntas para el nivel {level} (dificultad {lo}–{hi}) | `level_empty` | `level`, `lo`, `hi` |
| `new_game` | no hay suficientes preguntas: nivel {l} (dificultad {lo}–{hi}): faltan {n}, … | `supply_short` | `levels: [{level, lo, hi, missing}]`; client joins `error.supply_level` items with ", " |
| `pick` | no cards on the table (internal) | `no_cards` | |
| `pick` | no card {n} (internal) | `card_invalid` | `n` |
| `answer` | no question to answer (internal) | `no_question` | |
| `answer` | no answer {n} (internal) | `answer_invalid` | `n` |
| `back_to_select` | sin este tema no alcanzan las preguntas | `purge_short` | |
| `back_to_select` | no hay otra pregunta para este nivel | `refill_empty` | |
| `skip` | only a question on screen can be skipped (internal) | `skip_not_question` | |
| `play_hint` | no quedan pistas | `hints_used_up` | |
| `play_easier` | no hay preguntas más fáciles de este tema | `easier_none` | |
| `play_category` | ese tema no existe | `category_unknown` | |
| `play_category` | ya están en ese tema | `category_same` | |
| `play_category` | no hay preguntas de ese tema para este nivel | `category_empty` | |
| `jokers_view` (reason literal) | no hay preguntas de otros temas para este nivel | `category_none` | |
| `play_snipe` | solo queda una respuesta | `snipe_last` | |
| `play_snipe` | no se puede apuntar a esa respuesta | `snipe_invalid` | |
| `play_snipe` | si le dan a la correcta, no quedan preguntas para repetir el nivel | `snipe_no_repeat` | |
| `set_jokers` | unknown joker in the budget (internal) | `budget_unknown_joker` | |
| `set_jokers` | a budget is a count from 0 to 99, or null for unlimited (internal) | `budget_invalid` | |
| `joker` | no joker {name!r} (internal) | `joker_unknown` | `joker` |
| `joker` | los comodines solo se juegan en una pregunta | `joker_not_question` | |
| `joker`, `jokers_view` | `SPENT[name]` (ya no les quedan Soplos/Pasos/Bájales/Cambiazos/Francotiradores) | `joker_spent` | `joker` |
| `undo` | nothing to undo (internal) | `nothing_to_undo` | |
- Task 1 re-greps `raise GameError` and adds any new one.

## Tasks (one per worker run, in this order)
1. Server + client wiring, interim Spanish map (priority 710):
   - `game.py` (`GameError`, `ERRORS`, every raise, `trial`, `jokers_view`, drop `SPENT`), `main.py` (response shape on all three routes, 404/500).
   - `lib/api.ts`, `lib/types.ts`, new `lib/errors.ts` (`errorText`, `reasonText`, Spanish map for the player-facing codes, texts moved verbatim), `Game.svelte`, `JokerTray.svelte`, `Question.svelte`, `Player.svelte`.
   - Decision in `plans/decisions.md` (next free D-number): error code scheme (codes + params on the wire, English `message` for logs, client renders). `directory.md`: `lib/errors.ts`.
   - PORT-1 fixtures: if they exist, re-record; note in `plans/12-client-engine.md` that PORT-3 throws the same codes and parity compares `error`/`params`, not `message`.
   - Check: throw-away script that hits every code over HTTP against a temp `TRIVIA_STATE` and prints code, params, message, and the client''s Spanish text next to the old text; they must match word for word.
2. Errors into the catalog (priority 490, after plan 21''s tasks; waits for part 1''s `lib/i18n.ts` and `locales/es.ts`):
   - `error.<code>` keys in `es.ts` (`error.joker_spent.<id>`, `error.supply_level`), Spanish map removed from `errors.ts`; `errorText`/`reasonText` call `t()`. Known-code check: a code is player-facing iff its key exists in the catalog (typed lookup, no `⟦key⟧` for internal codes).
   - Literal check of part 1 (`check:literals`) passes for `lib/errors.ts` too.
   - Close-out: `plans/project.md` (M3: part 2 done).

## Every task
- `npm run check`, `npm run build` pass; the game server starts.
- No visible change in Spanish: same corner error lines and joker reasons.
- No new dependencies.

## Out of scope
- Translating the English internal messages; `authoring/` and `/api/flags` errors; client-side literal texts (part 1).', '2026-10-12T00:10:24Z', 82);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (23, 3, 'Pseudo-locale xx (LUI-2)', 400, 'A dev-only pseudo-locale `xx`, generated from the `es` catalog, makes every catalog string visibly different and ~40 % longer, so missed literals and text overflow show up on the TV layout before any real translation exists. Part 3 of plan 3 (masterplan M3); design source `plans/15a-ui-translation.md` (LUI-2). Builds on plan 21 (`t()` helper and the `es` catalog, LUI-1: `lib/i18n.ts`, `locales/es.ts`, `?lang=` dev override, `⟦key⟧` for missing keys) and, for error lines, plan 22 (server errors as codes).

## Order
- Priority 400: after all tasks of plan 21 (500) and plan 22 (710/490). Task 1 starts only when `lib/i18n.ts`, `locales/es.ts` and the `?lang=` override exist; if not, drop back with a note instead of building them here.

## Design
- `app/client/src/locales/xx.ts`: `pseudo(es): Catalog`, generated at runtime from `es`, no hand-written file.
  - Walks every leaf: plain strings, plural maps (`{ one, other, … }`) and variant arrays (`copy.*`), keeping the shape so it satisfies `Catalog`.
  - Accents: ASCII letters → look-alikes (`a→å`, `e→é`, `o→ø`, `c→ç`, `n→ñ`, `A→Å`, …); readable, but plainly not Spanish.
  - Padding: ~40 % extra length (rounded up, min. 2 chars), appended as `~` runs inside the brackets.
  - Brackets `[` … `]` around each string, so clipping at either end is visible.
  - `{param}` placeholders stay byte-for-byte; only text outside `{…}` is changed.
  - Exempt: single-letter joker keys (`joker.<id>.key`), so key handling still works (LUI-4 decides keys later); keep a small exempt list in `xx.ts`.
- Loaded only in dev: `i18n.ts` picks `xx` when `import.meta.env.DEV && ?lang=xx`, via dynamic `import()`, so the production bundle doesn''t grow. Check with `npm run build` that `xx` isn''t in `dist/`.
- `document.documentElement.lang` stays `es` for `xx` (no real language; avoids odd hyphenation/fonts).
- Missing keys: plan 21 returns `⟦key⟧`; here add a dev-only `console.warn` once per missing key. Static side: `npm run check` already fails on unknown keys.
- What stays Spanish under `xx` (expected, not bugs): question/answer text, category and subcategory names, bundle names (content, `15b`), English `message` fallbacks of internal error codes (plan 22).
- Anything else still in plain Spanish under `xx` is a literal LUI-1 missed: fix it in place (move into `es.ts`), note it in the task.

## Tasks (one per worker run, in this order)
1. Generator + wiring: `locales/xx.ts` (`pseudo()`), `?lang=xx` in `i18n.ts`, missing-key `console.warn`. Throw-away script (not kept) that runs `pseudo()` over `es` and checks: every leaf changed, `{params}` unchanged, length ≥ 1.4× (except exempt), shape equal. `npm run check`, `npm run build` (no `xx` in `dist/`). Update `directory.md` (`locales/xx.ts`).
2. Screen walk on the TV layout (1920 × 1080, `theme.css`) with `npm run dev -w app/client` + `trivia`, `?lang=xx`: start, player, level, select (every joker tray state incl. reasons), question (every joker armed and used, hints, final answer), result, victory, overlay, error line in the corner.
   - Use the same screenshot method as plan 21''s before/after comparison; no new dependency in the flake.
   - Also check one tight case: the narrowest supported window (`theme.css` height bound).
   - Fix missed literals in place (see Design). Log each overflow/clipping as one row in `plans/backlog.md` (`B-n`, origin `LUI-2`, status `new`): screen, element, key, what breaks. No redesign, no CSS changes here.
   - Mark LUI-2 `[x]` in `plans/15a-ui-translation.md` with a note (date, backlog rows); update `plans/project.md` (M3 status). If no overflow is found, say so in the note.

## Every task
- `npm run check` and `npm run build` pass; `es` output unchanged (no visible change in Spanish).
- No new dependencies.

## Out of scope
- Fixing the overflow found (backlog), the `en` catalog (part 4, LUI-3), language menu or launch languages (OQ-31), joker keys per language (LUI-4), `authoring/` pages and `/comodines`.', '2026-10-12T00:11:32Z', 83);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (24, 3, 'Draft en catalog (LUI-3)', 400, 'A draft English catalog `app/client/src/locales/en.ts`, written by Claude, that satisfies the `Catalog` type of part 1, with playful English joker names chosen by the gamemaster. Part 4 of plan 3 (masterplan M3); design source `plans/15a-ui-translation.md` (LUI-3). Draft only: no native-speaker check, no launch, no language menu (LUI-5, OQ-31).

## Order and dependencies
- Priority 400, like plan 23 (pseudo-locale `xx`); plan 23 has the lower id and runs first at equal priority. Doesn''t depend on it, only on:
  - plan 21 (LUI-1): `lib/i18n.ts`, `locales/es.ts`, `Catalog`/`Key` types, `?lang=` dev override, `⟦key⟧` for missing keys;
  - plan 22 task 2 (priority 490): `error.<code>` keys in `es.ts`, so `en` covers them too.
- Task 1 starts only when those exist; if not, drop back with a note instead of building them here.

## Design
- `app/client/src/locales/en.ts`: `export const en = { … } satisfies Catalog`; same shape and keys as `es`, own wording.
  - Plural maps: English `one`/`other`; `{param}` placeholders as in `es` (same set per leaf).
  - Variant arrays (`copy.milestone.*`, `copy.consolation.*`): own English lines in the game''s tone (family, warm, a bit cheeky), not literal translations; count may differ (15a).
  - Joker keys (`joker.<id>.key`): same letters as `es` (`S`, `P`, `F`, `T`, `X`), even where they don''t match the English name; LUI-4 decides keys later. Note it in a one-line comment.
  - Error texts: only player-facing codes (those with an `es` key); internal codes keep the server''s English `message`.
- Loaded only in dev: `i18n.ts` picks `en` when `import.meta.env.DEV && ?lang=en`, via dynamic `import()` (same mechanism as `xx`); production stays `es` only. `document.documentElement.lang = "en"` under `?lang=en`.
- What stays Spanish under `en` (expected, not bugs): questions, answers, hints, category/subcategory and bundle names (content, `15b`), `/comodines` and `authoring/`.
- Joker names are content (15a): playful English names, not literal translations of «Soplo», «Paso», «Bájale», «Cambiazo», «Francotirador». The gamemaster picks them.

## Tasks (one per worker run, in this order)
1. Joker name candidates (priority 400):
   - Per joker (`hint`, `skip`, `easier`, `category`, `snipe`): 3–5 playful English candidates, short enough for the tray (≤ the length of «Francotirador»), each with a one-line reason (pun, tone, what it evokes). Recommended one first.
   - One `pm decision add` per joker, candidates as `--option`s (recommended first), body: the Spanish name, what the joker does, why the candidates.
   - Link task 3 to all five decisions (`pm task-pending-decision`).
   - Record the candidate lists in `plans/15a-ui-translation.md` under LUI-3 (bullets).
2. Draft `en.ts` (priority 400; doesn''t wait for the decisions):
   - Every key of `es`; joker names use the recommended candidates for now.
   - `?lang=en` dev override in `i18n.ts`; `npm run build` shows no `en` in the main chunk.
   - Throw-away check script (not kept): every leaf non-empty, same `{param}` set as `es`, no Spanish characters (`áéíóúñÁÉÍÓÚÑ¡¿«»`), no `⟦` in rendered output.
   - Screen walk with `npm run dev -w app/client` + `trivia`, `?lang=en`, TV layout (1920 × 1080): start, player, level, select (joker reasons), question (every joker armed and used, hints, final answer), result, victory, overlay, error line. Same screenshot method as plans 21/23. Fix wording that reads off; log overflow as `plans/backlog.md` rows (origin `LUI-3`), no CSS changes.
   - `directory.md`: `locales/en.ts`.
3. Joker names in (waits for the five decisions from task 1):
   - Put the chosen names into `en.ts` (`joker.<id>.name`, aria/hint texts and any copy lines that name a joker).
   - Mark LUI-3 `[x]` in `plans/15a-ui-translation.md` with a note (date, chosen names, "draft, no native-speaker check"); update `plans/project.md` (M3 status). If the names become a decision, log it in `plans/decisions.md` (next free D-number).

## Every task
- `npm run check` and `npm run build` pass; `es` output unchanged (no visible change in Spanish).
- No new dependencies.

## Out of scope
- Native-speaker check and playtest (LUI-5), launch languages and a language menu (OQ-31), joker keys per language (LUI-4), store texts (LUI-6), translating questions/categories/bundles (`15b`), `/comodines` and `authoring/`.', '2026-10-12T00:12:45Z', 84);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (25, 3, 'Gamemaster check of the colombia proposals (D-39)', 200, 'The gamemaster checks the 84 `colombia` proposals of BN-3 and closes the bundle half of milestone 3. This is human work: the agent side only asks for the check, waits, and records the result. Part 5 of the masterplan (plan 3); design source `plans/22-bundles.md` (D-39). No other plan depends on it.

## State (2026-10-11)
- `work/bundles/proposals.json`: 504 entries `{bundle, reason, applied}`; 84 propose `colombia`, all 84 still in `colombia` in `authoring/data/questions.json`.
- `/review?bundle=colombia` shows 109 questions (101 approved, 6 rejected, 2 `needs_work`): the 84 proposals plus questions moved by BN-12/BN-13 (q-0524, q-0071, q-0133, q-0193, …) and ones written by `qgen batch --bundle colombia`. Checking all of them is fine; the 84 are what the milestone asks for.
- Review tool (BN-5): shows the bundle; key `n` moves a question to the next bundle (`colombia` → `base`).
- Rule for `colombia` (D-39, `22-bundles.md`): answering needs a connection to Colombia that players outside Colombia mostly wouldn''t know. A `base` question must use a `base` subcategory (D-49), so moving one back may need a new subcategory: `qgen validate` reports it.
- "Every question has `bundle`": already enforced by `validate_pool()` in `authoring/tools/qgen.py` (`bundle must be one of app/data/bundles.json`). Confirm with `qgen validate`; don''t rebuild.

## Tasks
1. **Ask for the check** (one task, waits): `pm decision add "Have you checked the colombia proposals at /review?bundle=colombia?"` with a body naming the 84 proposals, the rule, key `n`, and that `trivia-authoring` must run; options e.g. "checked, all moves done in the review tool" / "checked, list the ones to move in the answer". `pm task-pending-decision` the same task on it; it does nothing else before the answer.
2. **Record the result** (same task, after the answer):
   - Count the 84: still `colombia` vs. moved to `base` (compare `proposals.json` with `questions.json`); if the answer lists ids instead, move them with the review server''s bundle API or tell the gamemaster, never by editing the pool by hand (AGENTS.md).
   - `qgen validate`; if a moved question''s subcategory isn''t in `base` (D-49), log it in `plans/backlog.md` or `plans/open-questions.md` and leave the fix to the gamemaster.
   - `qgen export` so `app/data/pool.json` is current.
   - Note in `plans/22-bundles.md` (BN-3 line: date, kept/moved counts) and `plans/project.md` (M3 line "Gamemaster checks the 84 `colombia` proposals" → `[x]`; bundle counts under State).

## Done when
- The decision is answered and the result is noted in `22-bundles.md` and `project.md`.
- `qgen validate` passes and `app/data/pool.json` is fresh.

## Out of scope
- BN-6 (choosing bundles in the game), new `colombia` questions, re-running `qgen bundles`.', '2026-10-12T00:13:19Z', 85);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (26, 4, 'Licence data in the pool', 900, 'Every picked media file in the source pool carries its full licence record, not just the `credit` string, so the audit (part 2) and the replacements (part 3) can run without the network. Takes over MP-8 of `plans/23-media-providers.md` and is PUB-2 of `plans/17-publishing.md`. State on 2026-10-11: 1,202 picks (1,186 `media`, 16 `background`, bundles `base` and `colombia` in the one `authoring/data/questions.json`); 1,198 Commons, 2 Freesound, 2 Openverse (Flickr); 1,195 match a stored candidate in `work/media/`.

## Slot fields
Added next to `source_url`, `file_url`, `credit` in every picked `media` and `background` slot (all bundles):
- `provider`: `commons` | `openverse` | `freesound` | `nasa` (… `pexels`, `pixabay` later).
- `license`: the provider''s short name as in credits (`CC BY-SA 3.0 de`); must pass `providers.licence_kind`.
- `license_url`: link to the licence; may be null (public domain, Commons files without one).
- `author`: full plain-text author (the credit keeps using `short_author`); may be null (unknown author).
- `author_url`: link to the author''s page; may be null.
- `restrictions`: list of Commons non-copyright restriction codes (`personality`, `trademarked`, `insignia`, …, from extmetadata `Restrictions`, split on `|`); `[]` when none or the provider has no such notion.
- `pd_reasons`: list of public-domain reasons, i.e. Commons PD licence template names (`PD-old-70`, `PD-US-expired`, `PD-USGov-NASA`, …); `[]` for non-PD licences. For other providers: NASA `["PD-USGov-NASA"]`, Openverse `pdm` `["PDM"]` (uploader''s claim; part 2 decides). A PD licence with `[]` means "reason unknown" (part 2 flags it).
- Not stored: `license_kind` (derived; part 2 calls `providers.licence_kind`).
- Unpicked slots (`file_url` null) keep the fields absent; when a pick is cleared (`qgen.py` ~855, ~987) the new fields are cleared too.

## Providers (`authoring/tools/providers/`)
- Candidates get `author_url` and `restrictions` from search (cheap: same request), so the review tool (part 3) can show them.
- `commons.py` search: `extmetadatafilter` adds `Restrictions|License|UsageTerms|AttributionRequired|Copyrighted`; `author_url` from the first `href` in the `Artist` HTML (before `plain()`), protocol-relative made `https:`.
- PD reasons only at pick time (they need the page''s templates, too heavy for 30 search results): new `providers.pd_reasons(candidate)` → the provider''s `pd_reasons(candidate)`. Commons: one `api(titles=…, prop="templates", tlnamespace=10, tllimit="max")`, keep names matching `PD-*` (strip `Template:`). Called only when `licence_kind` is `public-domain`.
- `openverse.py`: `author_url` from `creator_url`; `restrictions: []`. `freesound.py`: `author_url` = `https://freesound.org/people/<username>/`; `restrictions: []`. `nasa.py`: `author_url: None`, `restrictions: []`, `pd_reasons` constant.
- Update the candidate field list in the `providers/__init__.py` docstring and in `plans/23` "Data".

## `media.pick_fields`
- Writes all fields above on every new pick; both pick paths go through it (`authoring/server/main.py` `pick_media` → `media.download`, `qgen.py` review ~1532).
- Candidates stored before this plan lack `author_url`/`restrictions`: for Commons, `pick_fields` fetches them with the same titles query as the templates (one call per pick, like `download_url` already does for large images); for others, null / `[]`.
- `credit` and `credit_of` unchanged.

## Migration (one-time, `qgen migrate-licences`, deleted again after it ran)
- Commons picks: live lookup by title from `source_url` (`File:…`, URL-unquoted), batched 50 titles per `api()` call (~25 calls): extmetadata + templates → all fields. Stored candidates don''t help here: they lack `Restrictions` and PD templates.
- Other providers: from the stored candidate matching `source_url` (`load_candidates`), else the live provider page where cheap (Freesound sound id), else left out and listed.
- Prints a tally (per provider, per licence family, PD reasons, restrictions) and the picks it couldn''t fill; `--dry-run` prints without writing. Re-runnable: skips slots that already have `provider`.
- Does not touch `credit`, `file_url`, or the cache.
- Runs over all statuses; a pick whose licence fails the allowlist is written as found (part 2 lists it for replacement).

## `qgen validate` (`validate_pool`)
- Per picked slot of an approved question: the keys `provider`, `license`, `license_url`, `author`, `author_url`, `restrictions`, `pd_reasons` present; `provider` known; `license` non-null and on the allowlist; `restrictions`, `pd_reasons` lists.
- Until the migration has run: these are **warnings** (one summary line with the count plus the first few ids, not 1,200 lines). The migration task switches them to **errors** in the same change (no runtime flag). Non-approved questions: not checked.
- Not here: classification (PD-US only, flagged restrictions) is part 2''s report; the optional validate gate on it is part 3''s.

## `qgen export` (`authoring/tools/pool_export.py`)
- Decided: no change. `app/data/pool.json` keeps `type, role, file_url, source_url, credit` (media) and `file_url, source_url, credit` (background): the game shows only the credit, and the source link leads to the full attribution.
- The credits screen (PUB-5, out of scope) adds the fields it needs to `MEDIA_PLAY_FIELDS` / `BACKGROUND_PLAY_FIELDS` when it comes.

## Order of work
1. Providers: new candidate fields and `pd_reasons` (all four providers).
2. `pick_fields` writes the slot fields; clearing a pick clears them; validate warns.
3. Migration run over the pool; validate errors; delete the migration command; mark MP-8 in `plans/23` and PUB-2 in `plans/17` done.

## Done when
- `qgen validate` passes on the current pool with the licence checks as errors.
- A new pick in the review tool and in `qgen review` stores all fields, including `pd_reasons` for a PD Commons file.', '2026-10-12T00:19:16Z', 107);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (27, 5, 'Group windows and bundle filter in the engine', 590, 'The TypeScript referee plays one audience today: 12 levels with the fixed `LEVEL_RANGES` of D-22 over every approved question of every bundle. This plan turns the age group and the active bundles into settings of each game. The level ranges come from `app/data/age-groups.json`, one table of 12 per group, and selection, supply and every joker use the game''s group and bundles. Defaults (`young_teens`, every bundle on) leave old saves and plan 18''s fixtures unchanged. Part 1 of masterplan 5 (AG-7, BN-6). Part 2 (start screen) builds on the API here, and part 3 (tuning) edits the tables written here.

## Depends on
- Plan 19 (PORT-2): `selection.ts` (`LEVELS`, `PER_LEVEL`, `LEVEL_RANGES`, `inRange`, `available`, `assign`, `draw`, `supply`), `pool.ts` (`PoolQuestion`, `loadCategories`, `broadOf`, `categoryOf`), `invariants.test.ts`, the `node:test` setup.
- Plan 20 (PORT-3): `state.ts` (`GameState.settings`, `withDefaults`), `game.ts` (`supply`, `newGame`, `draw`, `availableNow`, `laterFill`, `categoryCandidates`, `replacement`, `play*`, `jokersView`, `undo`), `api.ts` (`getGame`, `gameAction`), `engineData`, `game.test.ts` (fixture replay).
- If their files aren''t there yet, the tasks wait; they don''t port anything to Python. `app/server/game.py` / `selection.py` stay as they are, and the fixtures are never re-recorded for this plan.

## Decisions taken here
- **Level ranges per group in `age-groups.json`**: each group gets `levels`, 12 `[lo, hi]` pairs (index 0 = level 1). The engine reads them; `selection.ts` loses the `LEVEL_RANGES` constant. `LEVELS = 12` and `PER_LEVEL = 4` stay constants (D-22: 4 cards per level, no fallback).
- **First mapping = D-22''s shape scaled onto the window**: `lo + round((x − 1) × (hi − lo) / 9)` for every bound `x` of D-22''s table (no .5 cases occur). `young_teens` comes out as D-22 exactly. Tuned in part 3 (masterplan 5).

  | level | kids 1–7 | young_teens 1–10 | young_adults 3–13 | adults 4–15 |
  |---|---|---|---|---|
  | 1 | 1–1 | 1–1 | 3–3 | 4–4 |
  | 2 | 2–2 | 2–3 | 4–5 | 5–6 |
  | 3 | 2–4 | 3–5 | 5–7 | 6–9 |
  | 4–6 | 3–4 | 4–6 | 6–9 | 8–10 |
  | 7 | 4–5 | 5–7 | 7–10 | 9–11 |
  | 8 | 4–6 | 6–8 | 9–11 | 10–13 |
  | 9 | 4–6 | 6–9 | 9–12 | 10–14 |
  | 10 | 5–7 | 7–10 | 10–13 | 11–15 |
  | 11 | 6–7 | 8–10 | 11–13 | 13–15 |
  | 12 | 6–7 | 9–10 | 12–13 | 14–15 |

  - Measured 2026-10-11 on `app/data/pool.json` (1136 approved) with `selection.supply`: every group fills all 12 levels with `base` alone and with `base`+`colombia`. Thinnest: adults level 12, 27 candidates (≈6 games per player); kids level 1 and young_teens level 1, 36 each.
- **Settings per game**: `GameState.settings` gets `age_group` (a group id) and `bundles` (active bundle ids, in `bundles.json` order, `base` always in), next to `jokers`.
  - **Missing = default, applied on read and never written back**: `young_teens`, and every bundle in `bundles.json`. `withDefaults` stays the port of Python''s `with_defaults` (jokers only). `gameChoice(state, data)` → `{age_group, bundles}` resolves the defaults. Why not fill them in `withDefaults`: the fixtures'' `db` snapshots and the view''s `settings` would no longer match plan 18''s recordings, and the milestone needs the replay to stay identical.
  - `newGame` writes both keys only when the request carries them. Part 2''s screen always sends them; the fixtures never do.
  - `view` returns `settings` as stored (like today). The HUD resolves missing keys with `gameChoice`''s defaults, exported for part 2.
  - `undo` keeps the current `settings` (already true for `jokers`); abandon and delete don''t touch them.
- **`base` is always on**: input without `base` gets it added, an empty list means `[base]`, duplicates are dropped, and the order is normalized to `bundles.json`. `always_on: true` in `bundles.json` marks bundles that can''t be switched off (only `base` today); the rule reads that flag, not the id.
- **Validation errors are `GameError`s** (→ `409 {error, supply: null}`, save unchanged), with Spanish messages: «grupo de edad desconocido: ''x''», «paquete desconocido: ''x''», «los paquetes deben ser una lista». A non-string `age_group` is rejected the same way.
- **Bundle of a question**: `q.bundle ?? "base"`. Bundles filter questions, not categories: a `colombia` question in a `base` subcategory (OQ-46) leaves with `colombia`, and the subcategory stays as long as `base` has questions for it.
- **Burns stay per player across groups and bundles** (D-28): a question seen in a kids game is burned for that player in every later game. Nothing changes in burning.
- **Decision entry** (next D number in `plans/decisions.md`): age group and bundles are settings per game; missing keys mean `young_teens` and every bundle, resolved on read; `base` (every `always_on` bundle) is always on; level ranges per group live in `age-groups.json` (`levels`), `young_teens` = D-22; burns stay per player (D-28). Related: D-22, D-28, D-38, D-39.

## Changes

### Data (`app/data/age-groups.json`, `pool.ts`)
- `levels` per group as in the table; `about` updated: "levels: 12 difficulty ranges per group, level 1 first; young_teens = D-22; the others are a draft until tuned (AG-7)".
- `pool.ts`:
  - `AgeGroup {id, name, ages, window, levels}` and `LevelRanges = readonly (readonly [number, number])[]`.
  - `parseAgeGroups(json)` throws unless every group has 12 levels with `window[0] ≤ lo ≤ hi ≤ window[1]`, the ids are unique and `young_teens` exists.
  - `parseBundles(json)` → `Bundle {id, kind, always_on, name, description}[]`, if `loadCategories` doesn''t already parse it.
- `engineData(pool, categories, bundles, ageGroups)`: `data` gains `bundles`, `ageGroups` and `groupById`.
- `qgen validate` checks the same `levels` rules (small Python check in `authoring/tools/`), so part 3''s hand edits fail early. Authoring code that reads `window` / `focus` is unchanged.

### Selection (`selection.ts`)
- `inRange(q, level, ranges)`; `assign(questions, levels, ranges)` sorts slots by `(hi − lo, level)` of the given ranges; `draw(level, questions, {ranges, n, keep, avoidCategories, categoryOf, rng})`; `supply(questions, ranges)`. Each `range` in the report comes from `ranges`.
- `available(pool, burned, exclude, bundles: ReadonlySet<string>)`: approved, not burned, not excluded, and `q.bundle ?? "base"` in `bundles`. One place filters bundles. Everything downstream (draw, supply, jokers) only sees the filtered list.
- Shuffle sites, order and lengths stay as plan 18 records them for the default choice, so tapes still match.

### Game (`game.ts`, `state.ts`)
- `GameState.settings: {jokers, age_group?, bundles?}`; `lib/types.ts` `Game.settings` gets the same optional keys.
- `gameChoice(state, data)` and `resolveChoice(data, input)` (validation and normalization as above), used by:
  - `availableNow` (bundles), `draw` (ranges; the error «no quedan preguntas para el nivel N (dificultad lo–hi)» names the group''s range), `laterFill`, `categoryCandidates`, `replacement`;
  - every `play*`: «Paso» (with purge), «Bájale» (candidates from the bundle-filtered list; still "easier than the current card", not bounded by the window), «Cambiazo», «Francotirador» (repeat draw), admin skip''s replacement;
  - `supply(save, data, player?, choice?)` and `newGame` (supply check for the requested choice before anything else).
- `jokersView`: the «Cambiazo» groups are `data.categories` whose `bundle` is active, in the same order. With every bundle on, the list and shuffles are identical to today''s.

### API (`api.ts`)
- `gameAction(…, "new", {player, age_group?, bundles?})`: coercion like the other args; missing → defaults (not written).
- New route `choice(save, data, {player?, age_group?, bundles?})` → `200 {choice: {age_group, bundles}, supply}` | `409 {error, supply: null}`. A missing field comes from the player''s newest game (`gameChoice`), else the defaults. Part 2 uses it for the preset and for a warning per choice before a session can''t be filled. `getGame` is unchanged (its `supply` stays the default choice, so fixtures match).

## Checks
- Plans 18–20''s replays pass unchanged: `selection.test.ts` with `young_teens`'' ranges from `age-groups.json` and every fixture bundle on; `game.test.ts` with no choice in any request. No fixture is re-recorded.
- `pool.test.ts`: `parseAgeGroups` on the real file; `young_teens.levels` equals D-22''s table (written out in the test; compared once with a throw-away `python3 -c` dump of `selection.LEVEL_RANGES`, not committed); bad files (11 levels, range outside the window, lo > hi) throw.
- `invariants.test.ts` (real pool, skipped if absent): the seeded 12-level walks run per group × `{base}`, `{base, colombia}`. Every level gets 4 distinct cards inside the group''s range, and with `colombia` off no `colombia` question is ever drawn.
- `choice.test.ts` (real pool and data, skipped if absent; on the engine, not the fixtures):
  - per group: a new game played to `won` with correct answers, using every joker once where available. Every offered card is in the group''s range at its level, and the stored settings are what was sent.
  - `colombia` off: no `colombia` question in `offered` or `history`; `jokersView.category.categories` has no group with `bundle: "colombia"`.
  - `bundles: []` and `["colombia"]` become `[base]` / `[base, colombia]`; unknown group or bundle → 409, save unchanged.
  - a state without `age_group` / `bundles` plays like `young_teens` with every bundle (draws equal the explicit default with the same seed).
  - `choice` route: preset from the player''s newest game, defaults for a new player, supply per choice.
- `npm test`, `npm run check`, `npm run build`, `qgen validate` pass; no new dependencies.

## Tasks to split into
1. **Data and decision**: `levels` in `age-groups.json` (table above) and `about`; `parseAgeGroups` / `parseBundles` and `engineData`''s new fields; `pool.test.ts` additions; `qgen validate` check; decision entry; `directory.md` (`levels`). Check: `npm test`, `npm run check`, `qgen validate`.
2. **Selection with ranges and bundles**: `selection.ts` signatures above, `LEVEL_RANGES` removed; selection fixture replay passes with young_teens ranges and all bundles; `invariants.test.ts` per group × bundle set.
3. **Game and API**: settings keys, `gameChoice` / `resolveChoice`, every draw, joker and supply path on the game''s choice, `jokersView` filter, `newGame` args, `choice` route, `lib/types.ts` settings type; `choice.test.ts`; game fixture replay unchanged. Then `plans/21-age-groups.md` (AG-7: note "engine: group ranges and choice per game, plan N"; stays `[ ]` until part 4), `plans/22-bundles.md` (BN-6 likewise; the "Later" sentence on Cambiazo), `plans/12-client-engine.md` if it lists engine functions.

## Done when
- Each group''s 12 level ranges live only in `age-groups.json` (the Python referee keeps its own copy until PORT-8); the engine has no `LEVEL_RANGES` constant.
- A game can be started and played for each of the four groups and with `colombia` off: cards always in the group''s range, no `colombia` question or Cambiazo category when it''s off.
- Plans 18–20''s fixture replays pass byte-for-byte with defaults; old states without the new keys play as `young_teens` with every bundle.
- Decision entry written; screens untouched (part 2).', '2026-10-12T00:25:09Z', 115);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (28, 5, 'Tune the age-group windows and level weights', 580, 'Plan 27 gives every age group 12 level ranges in `app/data/age-groups.json` (`levels`), a first mapping of D-22''s shape onto each draft window. This plan measures what those ranges can play on the real pool, adjusts the windows and ranges of `kids`, `young_adults` and `adults`, stores per-group `level_weights` derived from the ranges (as D-31 did for young teens), and has the gamemaster approve the final windows. Part 3 of masterplan 5 (AG-7); runs after plan 27 and before part 2''s start screen, so the screen shows tuned windows.

## Depends on
- Plan 27: `levels` per group in `age-groups.json`, `parseAgeGroups`, `available(…, bundles)`, `supply(questions, ranges)`, `draw(level, questions, {ranges, …})`, and the `levels` check in `qgen validate`. If they aren''t there yet, the tasks wait.
- Plans 19/20 for the engine runner (`node:test` setup; the script runs the same way).
- Sources: `plans/21-age-groups.md` (scale anchors, "Long-term difficulty distribution"), D-22, D-31, `authoring/tools/qgen.py` `LEVEL_WEIGHTS`.

## Fixed, not tuned
- **`young_teens` stays D-22 exactly** (window 1–10, today''s `LEVEL_RANGES`): the family''s default and plan 18''s fixtures must not change. Only `kids`, `young_adults`, `adults` move.
- **Shape of D-22** for every group: 12 levels, 4 cards each, level 1 narrow, ranges widen through the middle and narrow at the top; ranges non-decreasing in `lo` and `hi`; inside the window.
- No question work here: thin difficulties are reported, not fixed (milestone 1).

## Measure (throw-away script, not committed)
- `node` script on the engine over `app/data/pool.json` + `app/data/age-groups.json`, per group × bundle set `{base}`, `{base, colombia}`:
  - per level: range, candidates (`supply`), missing slots (4 − candidates if < 4);
  - **games until dry for one player**: seeded walks of whole games (draw 4 per level with `draw`, burn every card shown), repeated until a level can''t be filled; report the median over ~20 seeds and the level that runs out first;
  - per difficulty 1–15: approved count and the group''s expected cards per game (from `levels`).
- Comparison, in the same output:
  - plan 21''s demand table (share per difficulty from overlapping windows) vs. the pool''s share per difficulty;
  - each window against the scale''s anchors (1 = 6-year-old, 3 = 9, 5 = 11, 7 = 13, 10 = 16, 12 = most adults, 15 = specialists): the top levels should reach the oldest of the group (kids 10 → ~4, young adults 22 → ~12–13, adults → 15); level 1 is a warm-up and may sit below the youngest''s anchor.
- Results go into plan 21, new section "Measured windows (AG-7)": one table per bundle set, date, pool size. Script deleted afterwards.

## Adjust
- Targets for a proposal (per group, `{base}` alone):
  - every level ≥ 20 candidates (≈5 games per player) where the pool allows; a level below that is named in the table;
  - windows consistent with the anchors; overlap with neighbouring groups kept, so most questions serve several groups (D-38);
  - where the pool can''t carry a range (e.g. adults'' 14–15: 27 approved), widen that level downward rather than shrink the window; the thin top is reported for milestone 1 (plan 21 section and the decision body), not fixed.
- Windows may change (`window` in `age-groups.json`), not just `levels`. Authoring reads `window` for targets (`focus`, D-40); with `"focus": null` nothing in a batch changes. Note any effect on plan 21''s demand table (recompute it with the new windows).

## Level weights
- New key per group: `level_weights`, `{"<difficulty>": n}` over the group''s window, `n = round(12 × Σ 1/(hi − lo + 1))` over the levels whose range contains the difficulty: 3 × the expected cards per game, as D-31 computed `LEVEL_WEIGHTS`. `young_teens` must equal `qgen.LEVEL_WEIGHTS` exactly (sum 144); the script asserts it.
- Stored for AG-8 and the D-53 targets later; no consumer reads them in this plan (`qgen` keeps its constant; a backlog line says `qgen` should read `young_teens.level_weights` once AG-8 starts).
- Checks: `parseAgeGroups` (plan 27) and `qgen validate`''s `levels` check also check `level_weights`: keys exactly the window, values equal to what `levels` derive. A hand edit of `levels` without new weights fails early.

## Gamemaster approval
- A pm decision "Approve the age-group windows": body with the measured table (current draft vs. proposal, per group: window, 12 ranges, thinnest level, games until dry, `{base}` and `{base, colombia}`), and the thin top. Options: approve the proposal (recommended); keep the draft windows; adjust (gamemaster names the change).
- The applying task waits on it (`pm task-pending-decision`).
- After the answer:
  - `age-groups.json`: approved `window`, `levels`, `level_weights`; `about` without "draft" ("levels: … tuned 2026-…, AG-7").
  - `plans/21-age-groups.md`: table header "Window on the scale" (no "(draft)"), "The windows of the other groups are a first draft…" removed; demand table recomputed if windows changed. AG-7 stays `[ ]` (part 4 closes it).
  - Decision entry in `plans/decisions.md` (next D number): the approved windows and ranges, `level_weights` derivation, `young_teens` = D-22; related D-22, D-31, D-38, D-53, plan 27''s entry.
  - Plan 27''s `choice.test.ts` / `invariants.test.ts` still pass with the new ranges (they read the file).

## Suggested tasks
1. Measure the draft ranges and write a proposal (script, plan 21 section with both tables); raise the decision; the next task waits on it.
2. Apply the approved windows: `levels`, `level_weights`, `about`, the `level_weights` check in `parseAgeGroups` and `qgen validate`, plan 21, decision entry, backlog line; engine tests and `qgen validate` pass.

## Done when
- `age-groups.json` holds approved windows, ranges and `level_weights` for all four groups; `young_teens` unchanged from D-22.
- Plan 21 shows the measured table and no longer calls the windows a draft; the decision entry exists.', '2026-10-12T00:26:19Z', 116);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (29, 5, 'Age group and bundle choice on the start screen', 400, 'Before a session, the family picks an age group and which bundles to play, on a new Choice screen between Player and Level. It reads `app/data/age-groups.json` and `app/data/bundles.json`, presets the player''s last choice, checks supply per choice through plan 27''s `choice` route, and starts the game with `newGame({player, age_group, bundles})`. Enter straight through keeps today''s game: preset or defaults (`young_teens`, every bundle). Part 2 of masterplan 5 (AG-7, BN-6, IN-1); runs after plan 28 (tuned windows) and M2''s screens part (PORT-7).

## Depends on
- Plan 27: `AgeGroup` / `Bundle` / `parseAgeGroups` / `parseBundles` in `engine/pool.ts`, `engineData`''s `ageGroups` / `bundles`, `gameChoice` defaults, the `choice` route (`{player?, age_group?, bundles?}` → `{choice, supply}` | `409 {error, supply: null}`), `newGame` with `age_group` / `bundles`, `Game.settings` keys in `lib/types.ts`.
- Plan 28: tuned `window` / `levels` (the screen shows whatever the file holds; nothing hard-coded).
- M2 part 5 (PORT-7, screens on the engine; plan not written yet, ~500): `lib/api.ts` calls the engine; the client has the data files. If it hasn''t landed, the tasks wait; no Python route is added for this.
- Plan 21 (LUI-1, `t()` and `es` catalog, 500): if `app/client/src/lib/i18n.ts` exists at task time, every new string goes through `t()` with `choice.*` keys and passes `check:literals`; else Spanish literals, each marked `// LUI-1`, and a line in `plans/15a-ui-translation.md` lists the file.

## Decisions taken here
- **A screen of its own, "Choice"**, after the name: the preset depends on the player, so it can''t sit on the Player screen. Flow: Start → Player → **Choice** → «¡Hola, …!» → Level. One more `Enter` for the family than today; nothing else changes.
- **Title**: «¿Cómo juega {name}?».
- **Group tiles**: four, in file order: `name` and ages («6–10 años», «23+ años» for `[23, null]`). One selected (highlight like the name buttons'' focus). The window isn''t shown (family-facing).
- **Bundle toggles**: one per bundle in file order: `name`, `description`, on/off. `always_on` bundles shown on, locked, no key, `title` «Siempre activo».
- **Keys** (`<kbd>` on every control, IN-1):
  - `1`–`4` and `←`/`→`: group.
  - Bundles: the first letter of `name` (case-insensitive, accents stripped) not yet taken by an earlier switchable bundle, else the next letter of the name; computed in one helper, never one of `M`, `N`, `R`, `S`. Today: `C` = Colombia.
  - `Enter` / `Space`: «¡A jugar!» (disabled while the choice can''t fill a game). `Backspace` / «Atrás»: back to Player.
  - `Esc` keeps opening the overlay.
- **Preset**: `choice({player})` on entering the screen: the player''s newest game (finished, lost or abandoned), else the defaults. A new name gets the defaults.
- **Supply per choice**:
  - On entering and on every change: `choice` for the current `{age_group, bundles}` and once per group with the current bundles (5 calls, on the in-client engine).
  - A group tile that can''t fill 12 levels is dimmed with «Faltan preguntas» but stays selectable; when the selected choice fails, «¡A jugar!» is disabled and the supply report shows below, in today''s wording («No hay suficientes preguntas para una partida completa (N disponibles): Nivel L (dificultad lo–hi): faltan k»).
  - A `409` from `new` (race, stale data) shows the same report here, not on the Player screen.
- **Supply report as one component**: `SupplyReport.svelte` replaces the copies in `Game.svelte` (Start) and `Player.svelte`; same text and style.
- **Where the running game''s choice shows**: the admin overlay, one read-only line under the joker budget: «Adolescentes · Básico, Colombia». Not in the HUD: the TV stays as it is for the family. A game''s choice can''t change mid-game (ranges would change under the tower); a new game is the way.
- **Undo and abandon keep the choice**: undo keeps `settings` (plan 27); after «Reiniciar partida», the next Choice screen presets the abandoned game''s choice. Games without the keys show the defaults (`gameChoice`).

## Changes
- `app/client/src/game/Choice.svelte` (new): props `player`, `busy`, `refused`; `onstart(choice)`, `onback()`; exported `key(e)` like `Player.svelte`. Arrive animations and glass tiles as on the Player screen.
- `app/client/src/game/SupplyReport.svelte` (new), used by Start, Choice; `Player.svelte` loses `refused` and its report.
- `Game.svelte`: `Screen` gains `"choice"`; `choosePlayer(name)` → `go("choice", "whoosh")`; `startGame(choice)` does today''s `act("new", …)` + greeting + Level; keyboard routing for `"choice"`; Backspace/«Atrás» → `go("player", …)`.
- `lib/api.ts`: `fetchChoice({player?, age_group?, bundles?})`, `gameAction("new", {player, age_group, bundles})` (if part 5 hasn''t already typed them).
- `Overlay.svelte`: the choice line (from `game.settings` via `gameChoice`''s defaults, names from the data files).
- Docs: `plans/04-ui-tv-display.md` (state diagram, table row, a "Choice" section, keys in "Input"); `plans/21-age-groups.md` / `plans/22-bundles.md`: AG-7 / BN-6 note "start screen: plan N" (stay `[ ]` until part 4); `directory.md` for the new files.

## Checks
- `npm run check`, `npm run build`, `npm test`; `check:literals` if it exists.
- Browser, real pool, throw-away walk (not committed):
  - existing player, Enter, Enter: plays as today (`young_teens`, every bundle); the overlay shows «Adolescentes · Básico, Colombia».
  - each group by key and by click; `C` and a click toggle Colombia; Básico doesn''t toggle; the started game''s `settings` are what was shown.
  - a choice that can''t fill a game (e.g. a test player with most questions burned, or a hand-edited copy of `pool.json` in dev): tile dimmed, report shown, «¡A jugar!» disabled.
  - Backspace and «Atrás» return to Player; Esc opens the overlay from Choice.
  - after undo and after «Reiniciar partida», the preset is the previous game''s choice.
- Mouse only, then keyboard only: every action reachable (IN-1).

## Suggested tasks
1. **Choice screen**: `Choice.svelte`, `SupplyReport.svelte`, `Game.svelte` flow and keys, `lib/api.ts`, strings (`t()` or marked literals); docs in `04`.
2. **Choice in the overlay and close-out**: the overlay line, undo/abandon preset walk, `21` / `22` / `directory.md` notes.

## Done when
- A session can be started for each group and with `colombia` off, by mouse and by keyboard, and Enter straight through plays the defaults or the player''s last choice.
- A choice that can''t fill 12 levels can''t start and says why, in today''s wording.
- The overlay shows the running game''s group and bundles.', '2026-10-12T00:28:05Z', 117);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (30, 5, 'Play-test and close-out of age groups and bundles', 390, 'The last part of milestone 5: prove the milestone''s "done when" in the browser, then close AG-7 and BN-6 in the docs. Plans 27 (engine: group ranges, bundle filter, `choice` API), 28 (tuned windows, `level_weights`) and 29 (choice screen, overlay line) do the work; each leaves AG-7 / BN-6 `[ ]` with a "plan N" note for this part to close. Runs last (390, below plan 29 at 400).

## Depends on
- Plans 27, 28, 29 done; the game runs on the TS engine (milestone 2).
- Pm decision 5 (where the authoring supply check lives) may still be pending; the readers check works on whatever is there.

## Play-test (the milestone''s "done when")
- **Agent pre-check** first, so the gamemaster''s time isn''t spent on crashes: a throw-away `node` script on the engine API over the real `app/data/pool.json`, a fresh player per run: for each of the 4 groups with every bundle, and `young_teens` with `{base}` only: `newGame` with the choice, play 12 levels to the end (answer right, use each joker once where allowed), check every drawn question is in the group''s level range and an active bundle, Cambiazo offers no `colombia` category when it''s off. Plus `npm run build`, `npm run check`, `qgen validate`. Failures → a task in the owning plan (27/29), not a fix here.
- **Gamemaster session**: a pm decision "Play-test of age groups and bundles". Body: the pre-check''s result table; the checklist: `trivia`, one session per age group (choice screen by mouse and by keyboard once, IN-1), one with `colombia` off; defaults straight through with Enter look as before; overlay shows group and bundles; undo/abandon keep the choice. Options: "all sessions played fine" (recommended); "problems (listed in the answer)".
- The close-out task waits on it (`pm task-pending-decision`).
- Answer "problems": the close-out worker adds one fix task per problem to plan 27 or 29, raises the decision again, makes itself pending on it, and stops.

## Close-out docs (after "played fine")
- `plans/21-age-groups.md`: AG-7 `[x]` with date and plans 27/28/29; drop "The game plays young teens (levels 1–10) until AG-7, whatever the focus" and other "until AG-7" wording.
- `plans/22-bundles.md`: BN-6 `[x]`; "Later" section: the BN-6 bullet goes (section removed if empty); the Cambiazo sentence ("all of them until BN-6") in the present tense.
- `plans/project.md`: AG-7, BN-6 `[x]`.
- `directory.md`: rows for `age-groups.json` / `bundles.json` say the game reads them (group ranges, choice); new files from plans 27–29 listed (they add their own; check only).
- `about` in `app/data/age-groups.json`: no "The game plays young teens until AG-7", no "draft"; `about` in `app/data/bundles.json`: "players switch on or off" stays true, `base` always on. `qgen validate` passes.
- Decision entry in `plans/decisions.md` (next D number): play-test confirmed (date), milestone 5 done-when met; related D-38, D-39 and plans 27/28''s entries. Only if the gamemaster''s answer adds something beyond "fine"; else the AG-7/BN-6 notes are enough.

## Authoring readers (levels 1–10, one range table)
- Known readers: `qgen report` supply (`authoring/tools/qgen.py`: `selection.LEVEL_RANGES`, `selection.supply`), the authoring start page supply table (`authoring/server/overview.py` `supply_for`, `authoring/ui/src/home/Home.svelte`), `/stats/difficulty` (`authoring/ui/src/stats/DifficultyChart.svelte`: `PLAYED_GROUP = "young_teens"` shading). Grep for others: `LEVEL_RANGES`, `young_teens`, `1–10`, `range(1, 11)`.
- Broken = crashes, wrong numbers for what it claims to show, or text that is now false (e.g. "the window the game plays"). Fix those minimally (wording, or read `young_teens` from `age-groups.json` `levels`).
- Not broken but young-teens-only (supply per group or bundle set, shading every window): one line each in `plans/backlog.md`, linked to pm decision 5 where it depends on where the supply check lives.

## Tasks
1. **Readers check**: grep and run `qgen report`, `trivia-authoring` start page and `/stats/difficulty`; fix what''s broken, backlog the rest. Independent of the play-test.
2. **Pre-check and play-test decision**: the script, build/check/validate, the decision with the table and checklist; script deleted.
3. **Close-out** (waits on task 2''s decision): the docs above; AG-7, BN-6 `[x]`.

## Done when
- The gamemaster confirmed the play-test; AG-7 and BN-6 are `[x]` in plans 21, 22 and `project.md`; no "until AG-7/BN-6" wording left in plans, `directory.md` or the data files'' `about`.
- Authoring readers checked: fixed or logged in `plans/backlog.md`.', '2026-10-12T00:29:06Z', 118);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (31, 6, 'Preload the next screen''s media (UI-7)', 500, 'The fade-in after a screen change waits until the next screen''s media has loaded, at most 2 s (04, "Transitions", step 4). Today `go()` in `app/client/src/game/Game.svelte` switches the screen behind the black and fades in at once (`PLACEHOLDER(UI-7)`, line ~117). The plan also removes the last `PLACEHOLDER` hits, so the milestone''s `grep -rn PLACEHOLDER app/client/src` comes up empty.

## Shape (decided here)
- The screen hands back a promise; no separate preload helper, so the element that shows the media is the one that loads it (no second request, no cache guessing on `/media?url=…`).
- `Question.svelte` exports `ready(): Promise<void>`: resolves when the picture is decoded (`onload` / `img.decode()`), the video or audio reached `canplaythrough`, or any of them failed (`onerror`, `mediaFailed`). No media (text question) → resolves at once.
- Only Question has media worth waiting for: other screens have no `<img>`, no backgrounds from `/media` (checked 2026-10-11). Other screens: no `ready()`, `go()` doesn''t wait.
- `go()`: after `screen = next`, `await tick()`, then `await Promise.race([questionRef?.ready() ?? Promise.resolve(), sleep(PRELOAD_MAX_MS)])`, then fade in as today.
- `timing.ts`: `PRELOAD_MAX_MS = 2000` with a one-line comment.
- Video/audio must not play behind the black: drop `autoplay` on `<video>`/`<audio>`; Question exports `start()` (or a `shown` prop) that `go()` calls when `black = false`. Same moment media starts today (start of fade-in), so the first seconds aren''t lost.
- Paths into Question that don''t go through `go()` (page reload on a running game, `{#key game.question.id}` swaps by Bájale/Cambiazo inside Question): media still starts; the card flip doesn''t wait (out of scope, note in 04).
- Overlay pause (`pausedMedia`) and `replay()` keep working with the deferred start.

## Missing media notice (no more `Placeholder.svelte`)
- `Placeholder.svelte` is used once: the «medio no disponible (¿falta `trivia-media sync`?)» chip in `Question.svelte` (`task="IMG"`), a runtime fallback, not unfinished work.
- Replace it with a plain inline notice in `Question.svelte` (same text, same chip look, no `PLACEHOLDER · …` tag); delete `Placeholder.svelte`.
- Overlap with plan 21 (LUI-1), task 95 (moves `Placeholder.svelte` labels into the catalog as `placeholder.*`): whichever runs second adapts. If 95 ran first, the notice keeps its catalog key (rename `placeholder.*` → e.g. `question.mediaMissing`); if this runs first, 95 has no `Placeholder.svelte` left and catalogs the inline notice text.
- Docs (D-25 references): AGENTS.md "Placeholders" line, 04 "Implementation notes" (Placeholders bullet), `plans/project.md` ("One placeholder left", M3 row, UI-7 follow-up line) say none are left; D-25 itself stays as history.

## Files
- `app/client/src/game/Game.svelte`, `Question.svelte`, `timing.ts`; delete `Placeholder.svelte`.
- `AGENTS.md`, `plans/04-ui-tv-display.md` (UI-7 note), `plans/project.md`.

## Tasks (suggested split)
1. Preload: `ready()`/`start()` in Question, `go()` waits with `PRELOAD_MAX_MS`, no autoplay behind the black; remove `PLACEHOLDER(UI-7)`.
2. Missing-media notice inline, delete `Placeholder.svelte`, update the D-25 references and project.md; UI-7 note in 04.

## Done when
- `grep -rn PLACEHOLDER app/client/src` is empty; `npm run check` and `npm run build` pass.
- Dev browser, throttled network (DevTools "Slow 4G") and a large video/image: the fade waits for the media, never longer than 2 s; video and audio start with the fade-in, not behind the black.
- Missing file (`/media` 404): fade in after at most 2 s, the «medio no disponible» notice shows.
- Text questions and screens without media fade in as fast as today.
- No new dependencies.', '2026-10-12T00:33:12Z', 134);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (32, 6, 'Recorded sound effects (UI-10)', 200, 'Replaces the effects that are still synthesized with CC0 (or D-45 allowlisted) recordings, mainly from Kenney.nl, and gives Soplo''s paper rustle and the token pop-back a sound. Owner plan file: `plans/04-ui-tv-display.md` ("Sound assets", UI-10); joker sounds: `plans/09-jokers.md` ("Sound assets", JK-9). Music loops are plan "Recorded music loops (UI-10)" (masterplan part 3), which runs after this one and reuses its pipeline and audition aid.

## Scope
- Effects still synthesized (`app/client/src/game/sound.svelte.ts`, `RECIPES`), by name pattern:
  - whooshes: `whoosh`, «swoosh que sube», `swoosh|escoba` («escoba: fuuush»)
  - `pop|carta` (card pick), `menú abierto` / `menú cerrado`, `desbloqueado`, `listo|hola`
  - jokers: `comodín` shimmer, `comodín: preparado`, `comodín: abrir`, `silbato`, `trituradora`, `latido`, `rebobinar`, `mira: tic`, `disparo|corcho`, `rasgado` (envelope tear)
  - fireworks: `cohete`, `cañón de confeti`, `bengalas`, `estrellas`
- Still silent: Soplo''s note paper rustle, token pop-back (JK-9); add a name at the call site + recording (+ a tiny synth fallback).
- Out of scope: the 13 existing recordings (keep), music (part 3), credits screen (none, gamemaster 2026-10-06).

## Sources and licences
- Kenney.nl CC0 first: Interface Sounds, UI Audio, Impact Sounds, Digital Audio, Casino Audio, Sci-fi Sounds (whoosh/rewind candidates).
- Then Freesound CC0, OpenGameArt CC0; D-45 allowlist only (CC0 preferred; CC BY ok with credit; no NC/ND/unknown).
- Download once by hand (a downloaded pack zip is not committed); keep only the converted files.
- Not every effect must be replaced: if no recording beats the synth, keep the recipe and note it in UI-10.

## Pipeline (as UI-10 rounds 1–2)
- `nix shell nixpkgs#ffmpeg-headless` (not a project dependency).
- Trim silence, short fade-out, loudness-normalize (`loudnorm`, same target as the existing files), mono unless stereo matters, AAC `.m4a`.
- Files: `app/client/public/audio/<spanish-name>.m4a` (flat, like the existing ones), committed.
- `app/client/public/audio/CREDITS.md`: one row per file, CC0 too (source URL, pack, author, licence).
- Budget: new effects ≤ 400 kB in total, ≤ 40 kB per file (folder is ~1.9 MB today, 1.2 MB of it `victoria.m4a`).

## Wiring
- `SAMPLE_NAMES` + `SAMPLE_FOR` entries per file; `rate` callback where pitch should vary (pops, stars, cannon).
- Recipes stay as the fallback (missing file, offline decode failure).
- Several variants of one effect (e.g. 3 pops) only if repetition is audible; pick at random.

## Audition aid
- `/?efectos` on the Start screen, next to `?fuegos` in `Game.svelte`: a small list of every effect name, each with «grabado» and «sintetizado» buttons, so the gamemaster can compare on the TV.
- Needs a way to force the synth path: an optional flag on `sfx()` (or an exported helper) in `sound.svelte.ts`.
- Minimal, plain styling; dev/check only, not in the admin overlay (B-3 «Demo de efectos» stays backlog).
- Part 3 adds the music loops to the same list.

## Tasks (suggested split)
1. Audition aid `/?efectos` with recorded/synth toggle (first, so every later pick can be compared).
2. Whooshes, pops, menu blips, `desbloqueado`, `hola`: source, convert, wire, credit.
3. Joker sounds (shimmer, preparado, abrir, silbato, trituradora, latido, rebobinar, mira, corcho, rasgado) + the two silent ones (Soplo rustle, token pop-back; JK-9 note in 09).
4. Firework sounds (cohete, cañón, bengalas, estrellas).
5. Gamemaster check on the TV via `/?efectos` and a real game: make it pending on a decision listing what was replaced and what stayed synthesized; apply the feedback; then update UI-10''s note in 04 and `plans/project.md` (UI-10 stays `[~]` until part 3 is done).

## Done when
- Every listed effect is either a recording or deliberately kept synthesized (noted in UI-10).
- Soplo''s rustle and the token pop-back are audible.
- `CREDITS.md` has a row per new file; audio folder within budget; `npm run check` and `npm run build` pass.
- The gamemaster approves the effects on the TV.', '2026-10-12T00:34:28Z', 135);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (33, 6, 'Recorded music loops (UI-10)', 190, 'Replaces the three generated music loops (`normal`, `question`, `submitted`) with CC0 (or D-45 allowlisted) recordings, as one matched set: one theme at three intensities, same key and tempo family, gapless. Owner plan file: `plans/04-ui-tv-display.md` ("Music", "Sound assets", UI-10). Runs after plan 32 "Recorded sound effects (UI-10)", whose pipeline, budget conventions and `/?efectos` audition aid it reuses; closes UI-10.

## Scope
- Generated today in `app/client/src/game/sound.svelte.ts` (`startTrack`, lookahead scheduler, `CHORDS`, `TEMPO`): A minor i–VI–III–V at 76/96/120 bpm; normal = pad + soft pulse, question = + ticking, submitted = heartbeat/timpani roll, pad creeping upwards.
- Replace: `normal`, `question`, `submitted`.
- Out of scope: `roll` (`redoble.m4a`) and `victory` (`victoria.m4a`) are already recordings; effects (plan 32).
- Behaviour stays as in 04 "Music": 600/800 ms fades on screen changes, ~80 ms sharp cuts `question` ↔ `submitted`, cut to `roll` on submit, ducking for jokers.

## Sources and licences
- Kenney.nl CC0 first (music loops / jingles packs), then OpenGameArt CC0, Freesound CC0; D-45 allowlist only (CC0 preferred; CC BY ok with credit; no NC/ND/unknown).
- Need: a matched set (one piece with calm / tense / most-tense variants or stems), or loops close enough in key and tempo that the 80 ms cuts don''t clash.
- If no matched set exists, don''t guess: a decision for the gamemaster with options
  1. one CC0 loop for all three, varied by playback rate / low-pass filter / an added layer (e.g. the existing synth ticks/heartbeat on top);
  2. recordings for some tracks, synth for the rest;
  3. keep the synthesized loops (UI-10 closes with music noted as synthesized).
- Download by hand; don''t commit pack zips; keep only the converted files.

## Pipeline (as plan 32)
- `nix shell nixpkgs#ffmpeg-headless` (not a project dependency).
- Cut to a whole number of bars at the loop point, loudness-normalize to the same target as the other music (`redoble.m4a`), stereo ok, AAC `.m4a`.
- AAC adds encoder padding at the start: check the seam; if it clicks, store the loop points (`loopStart`/`loopEnd` in seconds per track in `sound.svelte.ts`) instead of relying on the file length.
- Files: `app/client/public/audio/musica-normal.m4a`, `musica-pregunta.m4a`, `musica-enviada.m4a` (flat, like the existing files).
- `app/client/public/audio/CREDITS.md`: one row per file (source URL, pack, author, licence), CC0 too.
- Budget: the three loops ≤ 900 kB together (loop length 20–40 s, ~96–128 kbit/s); whole folder ≤ 3.5 MB.

## Wiring
- `SAMPLE_NAMES` gets the three files; `startTrack()` plays the decoded buffer with `AudioBufferSourceNode.loop = true` (+ loop points) into the track''s gain, like the `redoble` branch; the scheduler stays as the fallback when a file is missing or fails to decode.
- A per-track level constant if the recordings don''t sit right against the music bus (as `redoble` uses 2.2).
- Sharp cuts `question` ↔ `submitted`: if the loops share tempo, start the new one at the old one''s position modulo its length so the beat continues; otherwise start at 0. Decide by ear.
- Update the header comment of `sound.svelte.ts` (what is still synthesized).

## Audition aid
- Add the three tracks to plan 32''s `/?efectos` list: «grabado» / «sintetizado» per track, plus a «corte» button that toggles `question` ↔ `submitted` to hear the cut, and a loop that runs long enough to hear the seam.

## Tasks (suggested split)
1. Source a matched set; if none, the decision above (task pending on it); credit rows.
2. Convert, set loop points, wire into `startTrack()` with synth fallback; extend `/?efectos`.
3. Gamemaster check on the TV (`/?efectos` and a real game; clicks at the seam, the cuts, level against effects and question media): pending on a decision; apply the feedback.
4. Close UI-10: `[x]` with a note in 04 (incl. what stayed synthesized), `plans/project.md` line, 04 "Sound assets" (`music/`, `sfx/` subfolders were never used: say flat folder).

## Done when
- The three loops are recordings (or the gamemaster chose another option via the decision), gapless, no click at the seam on the TV.
- Synth fallback works with the files removed.
- `CREDITS.md` rows; folder within budget; `npm run check` and `npm run build` pass.
- The gamemaster approves the music on the TV; UI-10 `[x]` in 04 and `plans/project.md` updated.', '2026-10-12T00:35:05Z', 136);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (34, 7, 'Desktop shell (OQ-29)', 700, 'Part 1 of the masterplan (plan 7): decide the desktop shell that turns the built client into a Steam game (OQ-29, SW-1). Decision only; no shell code (S3 is out of scope).

- Owner: `plans/18-steam-integration.md` ("Desktop shell" table: Electron + steamworks.js recommended, Tauri, browser + local server).
- Context: the shell only shows `app/client/dist/` and saves one file once the TS engine runs without Python (milestone 2, plans 19 and 20; `plans/12-client-engine.md`). Not a blocker for the decision.

## Tasks
1. **Prep: refresh facts, write the decision**
   - Facts (with sources and dates): steamworks.js maintenance status (last release, open issues, Electron versions supported, alternatives such as steamworks-ffi or the Steamworks SDK via a native module); Electron install size today; Tauri v2 state on Windows (WebView2) and Linux/Deck (WebKitGTK: media, `backdrop-filter`); Steam overlay in Electron (known workarounds) and over a system webview; Deck/Proton notes (native Linux build vs. Windows build via Proton).
   - OQ-37 (part 8) as a dependency, not a blocker: phones as buzzers would need a LAN server inside the shell (Electron: Node `http` in the main process; Tauri: Rust side; browser + local server: already has one). Say how each option handles it.
   - `pm decision add "Desktop shell (OQ-29)?"` with the recommended option first; body = facts + trade-offs, ultra-short. Then `pm task-pending-decision` on task 2.
   - Update the "For/Against" cells in plan 18''s table if the facts changed (still marked draft).
2. **Follow-up: record the answer** (waits for the decision)
   - D-entry in `plans/decisions.md` (next free D-number).
   - OQ-29 moved to "Resolved" in `plans/open-questions.md` with the D-number.
   - Plan 18: table marked decided (D-number); SW-1 `[x]` with a note; SW-2..SW-6 checked against the choice and reworded if needed (e.g. electron-builder → Tauri bundler; preload bridge → Tauri commands).
   - `plans/11-steam.md` open-questions row and `plans/project.md` kept in sync (the full S3–S6 rewrite stays with part 10, the S2 close-out).

## Done when
- Decision answered; D-entry exists; OQ-29 resolved; SW-1 `[x]`; plan 18''s table says decided; SW-2..SW-6 match the choice.', '2026-10-12T00:39:17Z', 162);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (35, 7, 'Default mode (OQ-30)', 600, 'Part 2 of the masterplan (plan 7): define the default mode, Steam''s first choice (one team, no gamemaster), so MD-6 and MD-7 (plan for part 3) can implement it (OQ-30, MD-5). Decision only; no code.

- Owner: `plans/13-game-modes.md` ("Default mode": draft preset table Fácil/Normal/Difícil/Experto, checkpoint idea, admin actions; "Implementation notes").
- Fit: D-38 (four age groups, scale 1–15, `plans/21-age-groups.md`) and the per-group level ranges of milestone 5 (plan 27 "Group windows and bundle filter in the engine", plan 28 "Tune the age-group windows and level weights"). Key question: does a preset shift the group''s window/level ranges, or only the joker budget? Age group and preset are separate settings either way.
- Existing pieces: joker budget in `settings.jokers` (MD-1..MD-4, `null` = unlimited); «Como las cartas» = Normal row (JK-11).
- Feeds part 5 (OQ-32, content target): cards burned per game under the default preset.

## Tasks
1. **Prep: options and recommendation as pm decisions**
   - Facts: what each joker burns or saves (Soplo, Paso, Bájale, Cambiazo, Francotirador; plan 13, D-28 burning); how a checkpoint interacts with burning and with "12 to victory"; what plans 27/28 put in `age-groups.json` (`levels` per group) so a preset can or can''t shift them.
   - Questions to settle: (a) joker counts per preset (confirm or change the draft table, number of presets, which is the default); (b) presets shift difficulty or only jokers; (c) checkpoints: none, Fácil only (level 6), or per preset; (d) which levels count as won (only 12, or a reached checkpoint shown as a partial win, e.g. for stats/achievements later); (e) admin actions: no undo, no «Saltar y quemar para todos», «Reportar pregunta» (burn for everyone on this machine, local report list, replacement), «Abandonar partida» stays; anything else (sound, pause).
   - Split into two decisions if one is too big: "Presets, checkpoints and won levels (OQ-30)" and "Admin actions in the default mode (OQ-30)". Recommended option first; body = context + trade-offs, ultra-short.
   - `pm task-pending-decision` on task 2 for each decision.
2. **Follow-up: record the answer** (waits for the decisions)
   - D-entry (or two) in `plans/decisions.md` (next free D-number).
   - OQ-30 moved to "Resolved" in `plans/open-questions.md` with the D-number(s).
   - Plan 13 "Default mode": draft table → decided; checkpoints, won levels and admin actions written as a spec MD-6/MD-7 can build (settings fields in "Implementation notes", e.g. `settings.preset`, `settings.checkpoint`); MD-5 `[x]` with a note.
   - If presets shift difficulty: note it in plan 21''s age-group section and as input for plan 28 (no change to `age-groups.json` here).
   - `plans/11-steam.md` open-questions row and `plans/project.md` kept in sync.

## Done when
- Decision(s) answered; D-entry exists; OQ-30 resolved; MD-5 `[x]`; plan 13''s default-mode section is a spec MD-6/MD-7 can implement.', '2026-10-12T00:39:47Z', 163);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (36, 7, 'Reportar pregunta and settings screen (MD-6, MD-7)', 490, 'Part 3 of the masterplan (plan 7): the default mode becomes playable. MD-6 «Reportar pregunta» (burn for everyone on this machine, local report list, replacement draw) and MD-7 the mode and settings screen (preset choice; the gamemaster mode still reachable). Owner: `plans/13-game-modes.md` (MD-6, MD-7, "Implementation notes"). The spec comes from part 2''s answer (plan 35, OQ-30, MD-5): presets, checkpoints, won levels, admin actions. This plan doesn''t re-decide them.

## Depends on (tasks wait; no second implementation in `app/server/game.py`)
- Plan 35 (Default mode, OQ-30): its decision(s) answered and plan 13''s default-mode section written as a spec. Each task first checks `pm show` of plan 35: if a decision is still pending, `pm task-pending-decision <this task> <decision id>`, stage nothing, stop.
- Plan 20 (Engine game state machine, PORT-3): `engine/game.ts`, `engine/api.ts`, `SaveData` / `GameState` / `BurnRow` in `engine/state.ts`.
- M2 part 4 (save document, stores and migration, PORT-4/5) for the `version` bump; M2 part 5 (screens on the engine, PORT-7): the client calls the engine. If either hasn''t landed, the task stops and says so in its note (`pm task drop` is wrong; leave it open and stop).
- Plan 21 (t() helper and es catalog, LUI-1): new strings via `t()` (`mode.*`, `report.*` keys); if `lib/i18n.ts` doesn''t exist yet, Spanish literals marked `// LUI-1`.
- Plan 29 (Choice screen between Player and Level, priority 400): MD-7 puts the preset on that screen instead of adding a second screen. Hence task 3''s priority 380 (after plans 29 and 30).
- Plan priority 490: after plan 20 (600), plan 21 and PORT-7 (~500).

## Decisions taken here (unless plan 35''s answer says otherwise)
- **Mode is a game setting**: `settings.mode: "gamemaster" | "default"`, missing = `"gamemaster"` (`withDefaults`), so old saves and fixtures are unchanged. Preset in `settings.preset`; `settings.jokers` filled from the preset table (one constant in the engine, the decided table of plan 13). Checkpoint fields as plan 13 specifies them.
- **Rules live in the engine**, not only in the UI: in the default mode `undo`, skip for everyone and `setJokers` return `409` with a reason; `report` is refused in the gamemaster mode (it has skip + burn for everyone).
- **«Reportar pregunta» = skip for everyone + a report row.** Reuse the engine''s skip-everyone path (`BurnRow` with `player_id: null`, replacement draw at the same level, same supply check); add `ReportRow {question_id, game_id, player_id, level, reported_on, note?}` in `SaveData.reports`. No undo of a report. Confirm step on screen («¿Reportar esta pregunta? Se quema para todos.»), Enter/Esc.
- **Report list is a client screen**, not a server route (the Python server keeps static files and `/api/save`, decision 4): reachable from the overlay in the default mode; newest first: date, question id, question text, answer, player; «Copiar» copies the list as plain text (one block per report) via `navigator.clipboard`, with a selectable `<pre>` fallback. Works offline.
- **Mode switch**: on the Choice screen (plan 29) in both modes, one toggle «Con presentador / Sin presentador» (key `M`, not used there). Launch option `?mode=default|gamemaster` presets it (the desktop shell, S3, passes it). The choice is preset from the player''s newest game like plan 29''s age group; a new player and a fresh save get `gamemaster` until S3 decides the Steam build''s default. The family: Enter straight through = today''s game.
- **Preset row** on the Choice screen, only in the default mode: one tile per preset (name, joker counts as small badges), keys per plan 13 or `F`/`N`/`D`/`E` if free; default preset as decided. Hidden in the gamemaster mode (budget stays in the overlay, MD-4).
- **Overlay by mode**: gamemaster mode exactly as today; default mode: sound, «Reportar pregunta», «Preguntas reportadas», «Abandonar partida»; no undo, no skip/burn, no budget editor (read-only preset line).

## Tasks
1. **Engine: mode, preset, report (MD-6 engine part)**
   - `engine/state.ts`: `settings.mode`, `settings.preset` (+ checkpoint per spec), `ReportRow`, `SaveData.reports`; version bump + migration step in part 4''s store (`reports: []`, games untouched).
   - `engine/game.ts` / `api.ts`: `newGame` accepts `mode` / `preset` and fills `settings.jokers`; `report` action; refusals per mode; checkpoint and won-level rules if plan 13 specifies them; `view` exposes `settings.mode` / `preset`; `lib/types.ts` to match.
   - Check: `npm test` (fixture replay unchanged: gamemaster mode identical), `npm run check`; throw-away script: default-mode game, report burns for everyone, replacement at the same level, row in `reports`, undo/skip-everyone refused, empty supply → `409` with report.
2. **«Reportar pregunta» and the report list (MD-6 UI)**
   - `Overlay.svelte` by mode; confirm step; `Reports.svelte` (new) list + «Copiar»; `Game.svelte` routing (`Screen` gains `"reports"`, back with Backspace/Esc); `lib/api.ts`.
   - Check: browser walk in both modes (gamemaster overlay unchanged; default: report → confirm → new question at the same level, list shows it, copy works); keyboard only and mouse only (IN-1).
   - Then plan 13 MD-6 `[x]` with a note.
3. **Mode and settings screen (MD-7)** — priority 380 (after plan 29''s Choice screen)
   - `Choice.svelte`: mode toggle, preset row (default mode), `newGame({…, mode, preset})`; `?mode=` launch option; preset from the newest game.
   - Docs: plan 13 MD-7 `[x]` and "Implementation notes" (mode/settings fields as built); `plans/04-ui-tv-display.md` (Choice section, Reports screen, overlay by mode, keys); `directory.md` (new files); `plans/project.md` if MD-6/MD-7 are listed.
   - Check: Enter straight through on an existing family save plays today''s game; each preset starts with its joker budget; `?mode=default` presets the toggle.

## Done when
- In the default mode a report burns the question for everyone, lists it on the report page and draws a replacement.
- The settings screen starts a default-mode game with a preset.
- A gamemaster-mode game plays exactly as today (fixture replay passes, overlay unchanged, Enter straight through).', '2026-10-12T00:41:03Z', 164);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (37, 7, 'Launch languages and Spanish variety (OQ-31)', 500, 'Part 4 of the masterplan (plan 7): decide which languages the Steam release launches with and which Spanish the pool speaks (OQ-31, I18N-1). Decision only; no code, no translation. Owner: `plans/15-i18n.md` ("Model", "Spanish varieties"), with `15a-ui-translation.md` (LUI-*), `15b-question-translation.md` (QT-*), `15c-regional-questions.md` (RG-5).

## Context
- Today: everything Spanish, Colombian usage and references where natural (D-6). Bundles replace 15c''s `region` (D-39): `colombia` holds what needs a real connection to Colombia, `base` holds the rest (D-49 moved Colombian-subcategory `base` questions out).
- D-50: store name «Living Room Trivia», Spanish localized «Trivia en Familia» (chosen partly because «sala»/«salón» splits Spanish); other languages get a localized name when they launch.
- Feeds part 5 (OQ-32, content target per language, plan "Content target per player and language") and part 10 (S4''s exit in `plans/11-steam.md`).
- Related: plan 24 "Draft en catalog (LUI-3)" (milestone 3) drafts `en.ts` without launching it.

## Tasks
1. **Prep: facts, options and recommendation as a pm decision**
   - Facts (numbers in the decision body, sources one line each):
     - Steam language shares: latest Steam Hardware & Software Survey (English, Simplified Chinese, Russian, Spanish – Spain, Spanish – Latin America, Portuguese – Brazil, German, …); note Steam lists "Spanish – Spain" and "Spanish – Latin America" as separate store languages.
     - Translation cost per question: estimate from `work/*/costs.log` (gitignored; generation, fix and review cost per approved question) as a proxy for translate + re-rate + fact-check + review (15b); times the content target draft of plan 16 (2,000–3,000 per language) → cost per language.
     - Pool flavour: approved and total counts per bundle (`base` vs `colombia`) from `authoring/data/questions.json` (throw-away script or `qgen report`); a rough count of Colombian vocabulary in `base` wording (e.g. "bombillo", "crispetas", "carro", "celular" vs neutral) from a sample, to size a neutral-Spanish rewrite.
     - UI side: size of `es` catalog (plan 21) if it exists; LUI work per language is small (15a).
   - Questions to settle (one decision, or two if too big: "Launch languages (OQ-31)" and "Spanish variety (OQ-31)"):
     - (a) Launch languages: Spanish only (recommended unless the facts say otherwise: the pool and the review loop are Spanish, the family checks it); Spanish + English (biggest Steam share, doubles content and review cost, needs a native check); more.
     - (b) Spanish variety: ship as "Spanish – Latin America" with Colombian usage as is; neutral Latin American Spanish in `base` with Colombian wording kept in `colombia`; or neutral + per-variety variants. Which Steam store languages to tick (Latin America only, or Spain too).
     - (c) If a later language is planned: name it as the first post-launch language, so plan 24 and 15b know whether `en` is launch or later work.
   - Recommended option first; body = context + facts + trade-offs, ultra-short. Note what each option means for part 5 (content target per language) and D-50 (localized names).
   - `pm task-pending-decision` on task 2 for each decision.
2. **Follow-up: record the answer** (waits for the decision(s))
   - D-entry in `plans/decisions.md` (next free D-number).
   - OQ-31 moved to "Resolved" in `plans/open-questions.md` with the D-number.
   - `plans/15-i18n.md`: "Spanish varieties" bullet decided, launch languages stated, I18N-1 `[x]` with a note; status no longer "stub" if the model is settled.
   - `15a`: LUI-5 names the launch languages (or "none beyond es"); `15b`: QT-6 and the intro name the target languages (or "after launch"); `15c`: RG-5 checked against the answer.
   - If the answer changes `base` wording (neutral Spanish): log the rewrite as a backlog row in `plans/backlog.md` (it is S4 content work, through the pipeline, D-36), no pool edits here.
   - Plan 24 "Draft en catalog (LUI-3)": check against the answer. English at launch or as first later language → keep, add a one-line note to its body (`pm plan edit 24 --body`) if the scope changes; no English planned → say so in plan 24 and leave dropping it to the gamemaster (note in the task''s done note).
   - `plans/11-steam.md` open-questions row and `plans/project.md` kept in sync (S4''s exit wording stays with part 10).

## Done when
- Decision(s) answered; D-entry exists; OQ-31 resolved; I18N-1 `[x]`; 15/15a/15b name the launch languages; plan 24 checked against the answer.', '2026-10-12T00:41:48Z', 165);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (38, 7, 'Content target per player and language (OQ-32)', 590, 'Part 5 of the masterplan (plan 7). OQ-32 asks how many games a new player gets before questions repeat, per launch language, and how good the release pool must be. In S2 the target is decided from an estimate, not a simulation: the simulation (CT-2, `qgen report --simulate`) belongs to S4 (milestone 9) and confirms or corrects the number later. Owner: `plans/16-content-target.md` (CT-1).

## Depends on
- Plan 35 "Default mode (OQ-30)": the default joker preset → cards burned per game (12 + Paso + Bájale + Cambiazo + Snipe hits), and whether a preset shifts the age-group window.
- Plan 37 "Launch languages and Spanish variety (OQ-31)": which languages need a target; whether a translation counts as a full pool.
- Masterplan part 8 (OQ-37, competitive/co-op), if already answered: burn multiplier per extra player. Not known yet → the decision states the target for solo play and names the multiplier as open.
- pm decision 1 (per-level counts for D-52''s 5000, stored per D-53) and pm decision 2 (spot-check size and agreement rate, D-56): use their answers if given, else the draft numbers, and say so.

## Tasks
1. **Prep: estimate and decision** (can start now; only the follow-up waits)
   - Facts: approved counts per level (1–15) and per age-group window (D-38, `app/data/age-groups.json`) for `base` today (`qgen report`); D-52''s 5000 and D-53''s per-level targets from `authoring/data/targets.json` if present; per-level draw of a game (4 shown, ≥ 1 burned per ladder level, D-22, D-27, D-28, D-31); burns per game from the default preset (plan 35''s draft if not yet decided).
   - Estimate: games per new player = min over ladder levels of (approved in that level''s window ÷ burns per game at that level), today and at 5000. Throw-away script, deleted after; numbers go in the decision body. Name the bottleneck level.
   - Options: e.g. ≥ 30 games per new player in every launch language, ≥ 50 in the primary (16''s draft); a lower bar met by 5000 `base`; a target per age group. Recommended first. State that CT-2 in S4 verifies it.
   - Quality bar: point to D-56 and pm decision 2; no new numbers in 16.
   - `pm decision add`, then `pm task-pending-decision` on task 2.
2. **Follow-up: record the answer** (waits on the decision from task 1)
   - D-entry in `plans/decisions.md` (next free number).
   - OQ-32 moved to "Resolved" in `plans/open-questions.md`.
   - `plans/16-content-target.md`: "Target" section decided (numbers, per language), "Quality bar" points to D-56; "Where we stand" refreshed; CT-1 `[x]` with a note that CT-2 (S4) confirms it; status no longer stub.
   - `plans/project.md` in sync; `plans/11-steam.md` S4 exit names the target if it mentions one.

## Done when
- D-entry; OQ-32 resolved; CT-1 `[x]`; 16''s target section is decided.', '2026-10-12T00:42:23Z', 166);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (39, 7, 'Price model and Steamworks account (OQ-33)', 300, 'Part 6 of the masterplan (plan 7). OQ-33 asks how the game is sold on Steam (paid, free, or free with paid packs) and who holds the Steamworks account (a person or a company, with its tax consequences). The answer is a decision, not code; the signup and the price setting themselves stay S5 tasks (PUB-6, PUB-11). Owner: `plans/17-publishing.md` ("Steamworks and store"). Not legal or tax advice: the decision body names where a professional must check.

## Depends on
- Nothing blocks the prep. Feeds plan "Code and content licence (OQ-35)" (part 7: a paid game with a public pool is a different trade-off) and plan "Freesound API for a commercial release (OQ-45)" (part 9: whether the release is "commercial").
- Related: D-39/D-49 bundles (`colombia` as a candidate paid DLC), D-50 (store names), plan 38 "Content target per player and language (OQ-32)" (how much content a base game vs a pack carries).

## Tasks
1. **Prep: facts, options and recommendation as a pm decision**
   - Facts (numbers in the decision body, one source line each; Valve''s Steamworks docs first):
     - Steam fees and payout: revenue share (30 % → 25 % above $10 M → 20 % above $50 M), $100 app credit per app (recouped after $1,000 gross), DLC costs no app credit; monthly payout threshold and timing; refunds (2 h / 14 days); VAT/sales tax handled by Valve.
     - Regional pricing: Valve''s recommended price matrix; what a USD price band means in COP/MXN/ARS/EUR (Spanish-speaking markets, plan 37).
     - Comparable trivia/party games on Steam: 5–8 titles with price and review count (e.g. Trivia Murder Party via Jackbox packs, Quiplash-like, smaller solo trivia titles); note which use DLC question packs.
     - Free-to-play on Steam: what "free" means for wishlists, visibility and refund-free reviews; free + paid DLC (bundles as DLC per D-39: `colombia`, later bundles) vs paid base + paid DLC.
     - Account holder: person (individual tax interview, W-8BEN for non-US, income in personal tax return, real name/address visible to Valve; store "Developer/Publisher" can still be a label) vs company (W-8BEN-E, company formation and bookkeeping cost, liability). Flag for a tax advisor: country of residence, US withholding under the treaty, VAT/Kleinunternehmer-like thresholds, whether a hobby income needs registration.
   - Options (one decision, or two if too big: "Price model (OQ-33)" and "Steamworks account holder (OQ-33)"):
     - (a) Price model: paid, low band (e.g. $4.99–$7.99) with regional pricing (recommended unless the facts say otherwise: one-time purchase, no store/IAP code, fits a living-room game); free; free base + paid DLC bundles; paid base + paid DLC bundles later.
     - (b) Account: person (recommended for a hobby launch, cheapest) vs company; name what would trigger switching later (Steamworks allows transferring an app to another partner account, check the doc).
   - Each option states its consequence for part 7 (licence: paid + public pool → anyone can copy the content; free → public pool costs nothing) and part 9 (paid or DLC → "commercial" under Freesound/CC NC terms; free still counts as distribution).
   - Recommended option first; body = context + facts + trade-offs, ultra-short. Never contact Valve or an advisor; if a question for an advisor is needed, put its text in the decision body for the gamemaster.
   - `pm task-pending-decision` on task 2 for each decision.
2. **Follow-up: record the answer** (waits for the decision(s))
   - D-entry in `plans/decisions.md` (next free D-number); note the professional checks still owed.
   - OQ-33 moved to "Resolved" in `plans/open-questions.md` with the D-number; `plans/11-steam.md` open-questions row and `plans/project.md` kept in sync (S5 wording stays with part 10).
   - `plans/17-publishing.md`: "Steamworks and store" account bullet decided; PUB-6 rewritten to the holder (person/company, which tax form, app credit, any advisor check before signup); PUB-11 rewritten to the price model (price band, regional pricing, launch discount, DLC pricing if bundles become DLC). Both stay S5 tasks, unchecked.
   - If the answer makes bundles DLC: one backlog row in `plans/backlog.md` (DLC depots/app IDs for bundles, S5, plan 18 SW tasks), no code here.

## Done when
- Decision(s) answered; D-entry exists; OQ-33 resolved; PUB-6 and PUB-11 match the answer and stay S5; parts 7 and 9 can read the consequence from the D-entry.', '2026-10-12T00:43:13Z', 167);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (40, 7, 'Code and content licence (OQ-35)', 290, 'Part 7 of the masterplan (plan 7). The repo is public on GitHub (D-17) but has no `LICENSE`, so today it is "all rights reserved" by default; the question pool (`authoring/data/questions.json`, `app/data/pool.json`, bundles) is public too. OQ-35 asks which licence the code and the questions get, and whether release content (new batches, translations, paid bundles) stays public. The answer is a decision, then a few files. Owner: `plans/17-publishing.md` ("Code and content license", PUB-4). Not legal advice: the decision body names where a professional must check.

## Depends on
- Plan 39 "Price model and Steamworks account (OQ-33)": its D-entry (paid / free / DLC bundles) changes the trade-off. Task 1 may gather facts before it, but writes the decision only once OQ-33 is answered; if it is still pending, `pm task-pending-decision` task 1 on OQ-33''s decision.
- Plan 26 "Licence data in the pool": media licences stay per file (CC BY, CC BY-SA, CC0, PD, Freesound CC0/CC BY); the repo licence never covers media. Bundled fonts keep their OFL (`app/client/public/fonts/OFL-*.txt`).
- Feeds plan "Freesound API for a commercial release (OQ-45)" only indirectly (commercial vs not is plan 39''s).

## Tasks
1. **Prep: options and recommendation as a pm decision**
   - Facts (one line each, with source): what "no licence" means on GitHub (ToS lets others view and fork, nothing else); MIT vs GPL-3.0 vs AGPL vs all rights reserved for a paid Steam game (GPL lets anyone rebuild and redistribute the game; MIT lets anyone ship a closed fork); CC BY-SA 4.0 vs CC BY-NC 4.0 vs reserved for the questions (SA/BY allow a competitor to resell the pool; NC blocks commercial reuse but not copying; copyright on short factual questions is thin, the curated set and hints/explanations are the protectable part); AI-generated text and copyright (drafted by Claude, reviewed by a person: protection uncertain, flag for a professional; links to PUB-10).
   - Pool size today (approved per bundle, `qgen report`), so the decision says what is at stake.
   - Options (code × questions × repo; one decision, or two if too big: "Licence (OQ-35)" and "Is release content public (OQ-35)"):
     - code: MIT (recommended if the game is paid: the value is the content, not the code; easy for contributors), GPL-3.0, all rights reserved.
     - questions: reserved (recommended if paid), CC BY-NC-SA 4.0, CC BY-SA 4.0.
     - repo: public code + current pool public, release content (new batches, translations, paid bundles) in a private repo or submodule; whole repo public; whole repo private before release.
   - Each option notes what it means for the build (`nix build .#app`, packaging step reading a private pool), for D-17''s "pool is public", and for existing forks (what is already public stays copyable under whatever was implied).
   - Recommended option first; body = context + facts + trade-offs, ultra-short. Never contact a lawyer; questions for one go in the body for the gamemaster.
   - `pm task-pending-decision` on task 2.
2. **Follow-up: record the answer** (waits for the decision)
   - D-entry in `plans/decisions.md` (next free D-number); amends D-17 if the pool or release content goes private.
   - OQ-35 moved to "Resolved" in `plans/open-questions.md`; `plans/11-steam.md` open-questions row and `plans/project.md` kept in sync.
   - `plans/17-publishing.md`: "Code and content license" section decided; PUB-4 `[x]` with a note once task 3 is done.
   - If release content goes private: one backlog row in `plans/backlog.md` (private content repo/submodule, how `qgen export` and the build find it, S4/S5); no restructuring here.
3. **Licence files and mentions** (after task 2)
   - `LICENSE` at the repo root with the code licence''s full text (or an "all rights reserved" notice).
   - A separate content licence file if the questions differ from the code (e.g. `LICENSE-content.md`: which paths it covers, i.e. `authoring/data/`, `app/data/`; that media and fonts keep their own licences per file).
   - `README.md`: short "License" section. `directory.md`: the new file(s).
   - `nix build .#app` still builds; the packaged `result/` includes the licence file(s) if the chosen licence requires it.

## Done when
- Decision answered; D-entry exists; OQ-35 resolved; PUB-4 `[x]`; `LICENSE` (and the content licence file, if any) exist and are linked from `README.md` and `directory.md`.', '2026-10-12T00:43:52Z', 168);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (41, 7, 'Competitive and couch co-op format (OQ-37)', 580, 'Part 8 of the masterplan (plan 7). OQ-37 asks how several players play without a gamemaster: the competitive format (relay ladder, parallel ladders, buzzer round) and the couch co-op rules, plus the input (hot-seat on one pad, one controller per player, phones as buzzers). Only the choice is made here; building it stays "Later" (MD-8, MD-9, IN-6). Owners: `plans/13-game-modes.md` ("Competitive mode", "Couch co-op") and `plans/14-input.md` (section 3, IN-7).

## Depends on
- Nothing blocks the prep. Related: plan 35 "Default mode (OQ-30)" (joker presets per player, admin actions), D-28 (burning), D-38 (age-group windows: can players of different groups share one game?).
- Feeds plan 38 "Content target per player and language (OQ-32)" (burn multiplier per game) and plan 34 "Desktop shell (OQ-29)" (does the shell need a LAN server for phones; a dependency, not a blocker).

## Tasks
1. **Prep: options and recommendation as a pm decision**
   - Facts (one line each, with source): Gamepad API pad limit in Chromium/Electron (4 on most platforms; Steam Input/Deck); Remote Play Together (remote input arrives as extra pads, so any per-pad format works online for free; plan 18 SW-13); phones as buzzers (LAN HTTP/WebSocket server in the shell, QR join, firewall prompt on Windows, breaks "no network" slightly; Jackbox as the reference); how comparable party trivia games on Steam handle 2–8 players.
   - Burn multiplier per format: questions seen per game vs. single player (relay: ~1×, every player sees the shared tower; parallel ladders: ~N×; buzzer: ~1× per round but more rounds). Use today''s approved counts per level (`qgen report`) to say for how many games of N players each format lasts.
   - Options (one decision, or two if too big: "Competitive format (OQ-37)" and "Multiplayer input (OQ-37)"):
     - format: relay ladder on one shared tower (recommended unless the facts say otherwise: one screen, ~1× burn, works hot-seat, fits the 12-level tower); parallel ladders; buzzer round; plus per-player joker budgets (from the default preset) and whether "attack" jokers exist.
     - couch co-op: default mode with several pads and a team confirm (majority / any player / one captain) vs. no separate co-op (hot-seat the default mode).
     - input: hot-seat with one pad or mouse (recommended baseline, always works, Deck-friendly); one pad per player up to 4 (+ Remote Play Together); phones as buzzers (adds the LAN server; would need its own later task).
     - mixed age groups (D-38): one window for the game (the youngest player''s) vs. per-player windows.
   - Each option notes its burn multiplier (for plan 38) and its shell needs (for plan 34).
   - Recommended option first; body = context + facts + trade-offs, ultra-short.
   - `pm task-pending-decision` on task 2 for each decision.
2. **Follow-up: record the answer** (waits for the decision(s))
   - D-entry in `plans/decisions.md` (next free D-number): format, co-op rule, input, burn multiplier, shell needs.
   - OQ-37 moved to "Resolved" in `plans/open-questions.md`; `plans/11-steam.md` open-questions row and `plans/project.md` kept in sync ("Later" phase wording stays with part 10).
   - `plans/13-game-modes.md`: "Competitive mode" stub → the chosen format (players, turn order, win rule, jokers per player, burning and supply rules); "Couch co-op" → the chosen rule. MD-8 and MD-9 rewritten to build exactly that; they stay unchecked and "Later".
   - `plans/14-input.md` section 3: the chosen input; IN-7 `[x]` with a note; IN-6 rewritten to match (join screen or hot-seat only) and stays "Later". If phones are chosen, one backlog row in `plans/backlog.md` (LAN buzzer page, Later).
   - `plans/16-content-target.md`: the burn multiplier line points to the D-entry (plan 38 uses it).

## Done when
- Decision(s) answered; D-entry exists; OQ-37 resolved; plans 13 and 14 name the format and input that MD-8, MD-9 and IN-6 build later; plans 34 and 38 can read the shell need and burn multiplier from the D-entry.', '2026-10-12T00:44:27Z', 169);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (42, 7, 'Freesound API for a commercial release (OQ-45)', 200, 'Part 9 of the masterplan (plan 7). Freesound''s API is free for non-commercial use; commercial apps need a licence from UPF. Our pipeline uses the API only to find sounds (MP-6, `authoring/tools/providers/freesound.py`); the game ships the picked CC0/CC BY files, never the API. Before a paid Steam release the gamemaster decides whether to ask Freesound, replace the Freesound picks, or keep Freesound for the family only. Owner: `plans/23-media-providers.md` (Freesound row, provider order, MP-6).

## Depends on
- Plan 39 "Price model and Steamworks account (OQ-33)": whether the release is "commercial" (paid, DLC). Prep doesn''t wait for it; the decision names it as a dependency.
- Plan 26 "Licence data in the pool" (`provider` per picked slot) makes the Freesound picks countable and excludable; until then count by `freesound.org` in the URLs.
- Related: SW-9 media bundle (`plans/18-steam-integration.md`), D-45 allowlist, D-36 (picks only through the review tool), D-17 (media cache keyed by URL).

## Tasks
1. **Housekeeping: give the Freesound question its own number**
   - `plans/open-questions.md` uses OQ-45 twice; the resolved one belongs to D-42. Renumber the open Freesound one to the next free number (OQ-47 as of 2026-10-11; check), keep D-42''s.
   - Update the Freesound references: `plans/open-questions.md`, `plans/23-media-providers.md` (Freesound row), `plans/project.md` (open-questions table), plan 7''s body and this plan''s subject/body (`pm plan edit`), any other hit of `grep -rn ''OQ-45'' plans`. Leave references meaning D-42''s OQ-45 as they are (e.g. D-42''s context in `decisions.md`).
   - Done when: each OQ number is used once; every Freesound reference uses the new one.
2. **Prep: facts, options and recommendation as a pm decision**
   - Facts (ultra-short, one source line each):
     - Freesound API terms of use and the commercial-licence page (what counts as "commercial use of the API"; whether using it in an internal authoring tool for a paid product counts); CC0/CC BY sound licences themselves allow commercial use with credit.
     - Count today: questions with a Freesound pick in `authoring/data/questions.json` and `app/data/pool.json`, by status (2026-10-11: 2 approved, q-0752, q-1016; the masterplan''s 9/6 needs a recount), plus how many future audio slots Freesound would fill (share of Freesound picks among audio picks in the last batches).
     - What Commons and other allowlisted sources (D-45) offer for those sounds: a quick review-tool search per question, no picks.
   - Options (recommended first; recommendation from the facts, e.g. replace if the count stays small):
     - (a) Replace the Freesound picks with allowlisted sources before release and drop Freesound from the audio order (`providers.ORDER`) or from release batches.
     - (b) Ask Freesound/UPF: the worker drafts the email (English, short: what the tool does, that only CC0/CC BY files ship, no API in the game, the expected volume, the question); the gamemaster sends it. The draft goes in the decision body.
     - (c) Keep Freesound for the family only: tag its picks and exclude them from the Steam media bundle (SW-9); questions without their sound then don''t ship or need another pick.
   - Each option notes its consequence for plan 39''s answer (free release vs paid).
   - `pm decision add`, then `pm task-pending-decision` on task 3. Never contact Freesound/UPF.
3. **Follow-up: record the answer** (waits for the decision)
   - D-entry in `plans/decisions.md` (next free D-number); the Freesound OQ moved to "Resolved" in `plans/open-questions.md`; `plans/project.md` and `plans/11-steam.md`''s open-questions row in sync.
   - `plans/23-media-providers.md`: Freesound row and the "Which provider for which slot" table match the answer; MP-6 note updated.
   - If (a): add a task to this plan that re-picks each Freesound slot through the review tool (search modal, D-36; the gamemaster or `qgen` picks, never by hand in the pool) and then removes Freesound from the order; `qgen validate` passes.
   - If (b): add a task "send the email and record the reply" pending on the gamemaster; the provider stays until the reply.
   - If (c): add the exclusion rule to SW-9 in `plans/18-steam-integration.md`.

## Done when
- The OQ numbers are unique; D-entry exists; plan 23 and the provider order reflect the answer; a replacement, if chosen, is a task in this plan.', '2026-10-12T00:45:18Z', 170);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (43, 7, 'S2 close-out', 150, 'Part 10 of the masterplan (plan 7): the last step of milestone 7. Once parts 1, 2, 4–9 have their answers in `plans/decisions.md`, this plan brings the Steam master plan and the indexes in line with them, so S3–S6 (milestones 8–11) start from the decided product. Docs and pm only; no code.

## Depends on (every task waits)
- Plans 34 "Desktop shell (OQ-29)", 35 "Default mode (OQ-30)", 37 "Launch languages and Spanish variety (OQ-31)", 38 "Content target per player and language (OQ-32)", 39 "Price model and Steamworks account (OQ-33)", 40 "Code and content licence (OQ-35)", 41 "Competitive and couch co-op format (OQ-37)", 42 "Freesound API for a commercial release (OQ-45)": their follow-up tasks done (D-entry, OQ resolved, owning plan file updated).
- Not plan 36 (MD-6, MD-7): implementation, may land later (it waits for milestone 2''s engine). The close-out notes its state, doesn''t wait for it.
- Guard at the start of each task: `pm show` of plans 34, 35, 37–42. If a decision is still pending, `pm task-pending-decision <this task> <decision id>` and stop. If a decision is answered but its follow-up task is still open, stop without changes (drop nothing) and say so; the queue brings the task back.
- The Freesound question gets a new number in plan 42 (OQ-45 is used twice today); use that number.

## Tasks
1. **`plans/11-steam.md` to the answers**
   - "Open questions (blocking)" table: each row → answer + D-number (OQ-34, OQ-36 already done); the Freesound row added with its new number.
   - "Tracks" table: "Steam part starts" and "What it covers" match the answers (e.g. shell named in 18''s row, languages in 15''s, competitive/co-op format in 13/14''s).
   - "Phases": S3 names the chosen shell (not "Electron" if it wasn''t); S4''s exit names the launch languages and the CT-1 target (CT-2 verifies); S5 names price model, account holder, licence files, Freesound outcome; "Later" names the chosen co-op/competitive format.
   - Risks: update the ones an answer changed (media licensing → Freesound outcome; scope creep → co-op format).
   - ST-1 `[x]` with date and D-numbers; file status `draft` → `agreed`.
   - Done when: no "open"/"recommended" wording left for OQ-29..OQ-37 or the Freesound question.
2. **Indexes and later milestones**
   - `plans/project.md`: "Open questions" table loses the resolved rows; "Steam track" paragraph says S2 is done (D-numbers); any ticked task (SW-1, MD-5, I18N-1, CT-1, PUB-4) ticked here too.
   - `plans/README.md`: status column for 13, 15, 15a/15b/15c, 16, 17, 18 (and 23 if changed) to what the files now say (`stub` → `draft`/`agreed` where decided).
   - `plans/open-questions.md`: OQ-29..OQ-37 and the Freesound question under "Resolved"; nothing left open for S2.
   - Milestones 8–11 (S3–S6): compare each milestone body and its masterplan (plans 8–11, `pm show`) with the answers. If the masterplan is still "tbd.", do nothing (its writer reads `decisions.md`). If it is written and its scope changed (e.g. shell other than Electron, languages, licence files, Freesound replacement), add a short dated note with `pm plan edit <id> --body -`. Change a milestone body only if it names something the answers ruled out; list such changes in the task note.
   - Done when: milestone 7''s "Done when" holds (OQ-29..OQ-37 and OQ-45 resolved in `decisions.md`, later phases in `11-steam.md` match); `qgen validate` unaffected (no data touched).', '2026-10-12T00:46:09Z', 171);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (44, 8, 'Action layer and focus navigation (IN-2, IN-3)', 500, 'Keyboard (and later gamepad) input goes through one action layer, and every screen and dialog can be played with arrow keys, Enter and Esc/Backspace via a visible focus ring. Part 4 of masterplan 8 (S3); owner `plans/14-input.md` (section 2, IN-2, IN-3). Client only: no engine, no shell. Part 5 (gamepad, IN-4/IN-5) adds a third device on top of this layer; the family''s keys behave exactly as today.

## Today (IN-1 audit, code as of 2026-10-11)
- `app/client/src/game/Game.svelte` `onkeydown` (≈ l. 304): `e.repeat` ignored; first key unlocks audio; chain overlay → Player dialog → Question dialog → `Esc` overlay → `M` flag → `busy` guard → per screen (Start `Enter`/`Space`/`N`, Level/Correct/Wrong/Victory `Enter`/`Space`, Select `1`–`4`), Question and Player forwarded raw.
- `Question.svelte` `key(e)`: `A`–`D`/`1`–`4` tap, `S P F T X` jokers (`JokerTray.TOKENS`), armed joker `Enter`/`Esc`/`Backspace`, Paso dialog `1`/`2`, Francotirador aim (letters, arrows, `Enter`), `Backspace` unlock, `Enter`/`Space` submit, `R` replay; Cambiazo forwards to `CategoryPicker.key` (arrows move DOM focus over tiles, `Esc` cancel, `Backspace` back a level, Enter native).
- `Player.svelte` `key(e)`: `1`–`9` pick a name, a letter focuses the name field, delete dialog `Esc`/`Backspace` cancel (Enter/Tab native on its buttons, «Cancelar» focused first).
- `Overlay.svelte` `key(e)`: own selection model (`selected`, ↑/↓ items, ←/→ volume/jokers/preset, `Enter` with «¿Seguro?», `Esc` close); its controls are `tabindex="-1"`.
- Focus ring: `.game button:focus-visible` in `theme.css` (sky, D-29) plus per-component `:focus-visible` rules (card, answer, tile, token, name-button, delete, danger). ☰ and flag buttons: `tabindex="-1"` + `mousedown` preventDefault (IN-1).

## Design
- **`app/client/src/lib/input.ts`** (new, no dependency):
  - `type Action = { type: "confirm" } | { type: "back" } | { type: "menu" } | { type: "pick"; n: number } | { type: "joker"; name: JokerName } | { type: "navigate"; dir: "up" | "down" | "left" | "right" } | { type: "replay" } | { type: "flag" } | { type: "new" }`.
  - The masterplan''s `answer(1..4)` is `pick(n)`, n 1–9: cards, answers, player names and the Paso options all use number keys. `replay`, `flag`, `new` cover the remaining shortcuts (`R`, `M`, `N`).
  - Every action carries `device: "keyboard" | "mouse" | "gamepad"`; `lastDevice` is an exported `$state` (part 5''s glyphs read it; mouse = any `pointerdown`).
  - **Keymap** (unchanged keys): `Enter`/`Space` → confirm, `Backspace` → back, `Esc` → menu, arrows → navigate, `1`–`9` → pick, `M` → flag. Scope-dependent extras: `question`: `A`–`D` → pick 1–4, `S P F T X` → joker (letters from `TOKENS`, later the catalog, plan 21), `R` → replay; `start`: `N` → new; `text`: none (see below).
  - **Scopes**: a stack; `pushScope({ name, keys, handle, root?, modal? })` returns a `pop`; components push in `$effect` (Game per screen, Overlay, Player delete dialog, Paso, Francotirador, armed joker, Cambiazo). The top scope gets the action; `handle` returns `false` to pass it down, unless `modal` (overlay and dialogs are modal, as today). Replaces the `overlayOpen`/`dialogOpen()` chain.
  - Dialogs treat `menu` as `back` (`Esc` cancels a dialog today); the overlay treats `menu` as close.
  - **Text entry**: while an `<input>` has focus, printable keys, `Backspace` and ←/→ stay native; only `Enter` → confirm, `Esc` → menu, ↑/↓ → navigate. On Player, a letter outside the field still focuses it (the `text` fallback lives in `input.ts`, not in `Player.svelte`).
  - Kept in one place: `e.repeat` ignored, the first key/click unlocks audio, `busy` (transition running, 04) drops actions except `menu` and `flag` as today, `preventDefault` when an action was handled.
  - **Mouse**: buttons keep their `onclick` (IN-1); the click and the action call the same function. No synthetic action dispatch for clicks.
  - No `keydown` listener outside `input.ts` after this plan (`grep -rn "keydown\|KeyboardEvent" app/client/src` lists only it).
- **Focus navigation (`app/client/src/lib/focus.ts`, new)**:
  - Spatial: `navigate(dir)` moves DOM focus to the nearest candidate in that direction inside the top scope''s `root` (bounding rects; primary axis distance + 2 × cross-axis offset; no wrap). Pure function over rects so it can be checked with a throw-away script.
  - Candidates: enabled `button`, `input`, `a[href]`, `[data-focusable]`; never `tabindex="-1"` or `[data-nofocus]`. ☰ and flag stay `tabindex="-1"` and gain `data-nofocus`, so neither Tab nor navigate lands on them (IN-1).
  - Scopes may handle `navigate` themselves and return `true`: the Overlay (its list model), the Francotirador (crosshair, `moveTarget`), the Cambiazo grid (row/column move; `CategoryPicker.move` becomes a call to the spatial helper if it gives the same result).
  - **First press**: with nothing focused, the first `navigate` focuses the scope''s default control (`data-focus-default`: «¡Jugar!»/«Continuar», «Seguir», the first card, the first answer, «Cancelar» in the delete dialog) instead of moving. So nothing looks different until someone presses an arrow.
  - **Confirm with focus**: `confirm` clicks the focused control only if focus came from navigate/Tab (the ring is showing); otherwise the screen''s default (today''s `Enter` behaviour). A control focused by a mouse click never steals the family''s `Enter`.
  - **Focus ring**: the sky outline of `theme.css` for every candidate; programmatic focus must show it in Chromium (`focus({ focusVisible: true })` or a `.nav-focus` class styled like `:focus-visible`; the task checks which one works in Chromium and Firefox).
  - **Focus memory**: per scope name, the last focused control (`data-focus-id`, else its index among candidates); restored when the scope is on top again (overlay or dialog closed, Cambiazo back a level, return to Start). Cleared when the screen''s content changes (new question, new cards). Dialogs return focus to their opener on close.
- Strings: no new on-screen text expected. If one is needed and `app/client/src/lib/i18n.ts` exists (plan 21), it goes through `t()`; else a Spanish literal marked `// LUI-1`.

## Coordination
- **PORT-7 (M2 part 5, plan not written yet, task 59)** also edits `Game.svelte` (`act`, `refresh`, `lib/api.ts` calls). This plan touches only input handling: `onkeydown`, the components'' `key()` exports, focus attributes and CSS. It never edits `lib/api.ts` or the data flow; handlers call whatever functions exist when the task runs (`newGame`, `pick`, `skip`, …). Whichever lands second keeps the other''s change; pm runs one task at a time, so a worker always sees the other''s code. Equal priority (500) puts PORT-7 first when both are queued (milestone 2 before 8).
- **Plan 21 (LUI-1)** moves joker letters to `joker.<id>.key`: the `question` keymap reads the letters from wherever they live at task time (`TOKENS` or the catalog), never a second copy.
- **Plans 29 (Choice screen) and 36 (Reportar pregunta, settings screen)**: neither screen exists today. Task 4 converts any that landed by then and, for those still open, adds a follow-up task to that plan (see task 4). Rule written into `04-ui-tv-display.md` ("Input") for every screen from now on.
- **Part 5 (gamepad, plan from task 213)** adds a gamepad source producing the same actions; this plan leaves a `dispatch(action)` export for it.
- No new dependency (no focus or hotkey library).

## Tasks
1. **Action layer core; Game, Overlay and Player on actions (IN-2)**
   - `lib/input.ts` as above (actions, keymap, scopes, `text` handling, `lastDevice`, `dispatch`); one `svelte:window` listener moves from `Game.svelte` into it (or `Game.svelte` calls `input.ts`''s handler).
   - `Game.svelte`: one scope per screen (start, level, select, correct, wrong, victory) plus the global `menu`/`flag`; `Overlay.svelte` and `Player.svelte` (incl. delete dialog) push their own scopes.
   - Question and Cambiazo still get the raw event through a temporary passthrough scope, removed in task 2.
   - Check: `npm run check`, `npm run build`; throw-away script for the keymap (key + scope → action); in the browser (`trivia` + `npm run dev -w app/client`), every key of 04 "Input" on these screens does what it did.
2. **Question, jokers and Cambiazo on actions (IN-2)**
   - `Question.svelte` scopes: answering, armed joker, Paso, Francotirador, Cambiazo (`CategoryPicker.svelte`); `key(e)` exports and the passthrough removed.
   - Check: the grep above lists only `input.ts`; every joker (incl. unavailable ones), Paso 1/2, aim with letters and arrows, unlock, replay, submit, flag, undo/skip from the overlay work as before; `IN-2` `[x]` in `plans/14-input.md`.
3. **Spatial focus, ring and memory (IN-3)**
   - `lib/focus.ts`; `data-focus-default` / `data-focus-id` / `data-nofocus` on the screens and dialogs; ring visible on every candidate; ☰/flag never focused.
   - Check: throw-away script for the rect logic (a 2×2 answer grid, the 4 cards, the Cambiazo grid with disabled tiles); in the browser every screen and dialog plays with arrows + Enter + Esc/Backspace only, the ring is always visible where focus is, and `Enter` without arrows behaves as today.
4. **Audit, docs and later screens (IN-3)**
   - Walk a full game with arrows + Enter + Esc/Backspace only (start → player incl. new name and delete → levels → every joker → wrong and victory → overlay incl. undo, skip, restart, volumes, jokers); fix what''s missing.
   - Plans 29/36: if the Choice, settings or report screens exist, put them on actions and focus; for each that doesn''t, `pm task add <plan> "<screen> on the action layer (IN-2, IN-3)"` with a body pointing here and a priority 10 below the task that builds the screen.
   - Docs: `04-ui-tv-display.md` "Input" gets the rule ("screens listen to actions from `lib/input.ts` and declare a focus default; no `keydown` elsewhere"); `14-input.md` IN-3 `[x]`; `directory.md` lists `lib/input.ts` and `lib/focus.ts`; `plans/project.md` in sync.
   - Done when: every screen and dialog plays with arrow keys + Enter + Esc/Backspace only; the family''s keys behave as before (gamemaster''s check on the TV at the next game night; the worker lists what to try in the task note).', '2026-10-12T00:56:02Z', 212);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (45, 8, 'Gamepad input and button glyphs (IN-4, IN-5)', 490, 'A standard (Xbox-style) gamepad becomes a third input device next to keyboard and mouse: it produces the same actions as the keyboard through plan 44''s action layer, and the on-screen key prompts switch to pad glyphs when the pad was used last. Part 5 of masterplan 8 (S3); owner `plans/14-input.md` (section 2, IN-4, IN-5). Client only; works in the browser setup (Chromium) and later in the desktop shell. Keyboard and mouse behave exactly as today.

## Depends on
- Plan 44 (action layer, focus; priority 500): `dispatch(action)`, `Action` with `device`, `lastDevice`, scopes, `navigate` + focus defaults, the "confirm clicks the focused control only if focus came from navigate/Tab" rule. Every task here starts only after plan 44''s tasks are done; if one isn''t, the task stops and says so.
- pm decision 9 (Question screen with a pad: focus only / direct face buttons / joker wheel; recommended focus only). Tasks 2 and 3 wait for it.

## Design
- **`app/client/src/lib/gamepad.ts`** (new, no dependency):
  - `gamepadconnected` starts a `requestAnimationFrame` loop, `gamepaddisconnected` of the last pad stops it. Reads `navigator.getGamepads()`; only `mapping === "standard"` pads (others: one `console.warn`, ignored). Any connected pad drives the game (one team; per-player pads are IN-6).
  - Pure core `step(prev, pad) → { next, actions }` (button edges, stick state), so a throw-away script can feed fake pads; the loop only calls it and `dispatch`es with `device: "gamepad"`.
  - Mapping (standard indices): D-pad 12–15 and left stick → `navigate` (dead zone 0.5, release below 0.3, dominant axis wins); 0 A → `confirm`; 1 B → `back`; 9 Start → `menu`; 3 Y → `replay`; 8 View/Back → `flag` (gamemaster); 4/5 LB/RB per decision 9 (option 1: `joker-focus` prev/next, a new action plan 44''s `Action` gains); triggers, X and the right stick unused unless decision 9 says otherwise.
  - Edges only, no auto-repeat (the keyboard ignores `e.repeat` too).
  - Ignored while `document.hidden` or the window has no focus; on focus return, held buttons don''t fire (prev state reset to "pressed").
  - `padStyle: "xbox" | "playstation"` (`$state`), from the `id` of the pad that last produced an action: `/054c|playstation|dualshock|dualsense|wireless controller/i` → playstation, anything else (Xbox, Steam Virtual Gamepad, the Deck, generic) → xbox. Under Steam Input every pad looks like Xbox; real per-device glyphs via Steamworks `GetInputTypeForHandle` are S5.
- **Screens with a pad** (no new screens, plan 44''s focus does the work):
  - Start, Level, Select, Correct, Wrong, Victory, Overlay, Paso, Cambiazo, Player''s delete dialog: `navigate` + A/B/Start as the keyboard''s arrows + Enter/Backspace/Esc.
  - Question per decision 9. Option 1: A on a focused answer locks it (`tap`), then focus moves to «Respuesta final» as soon as it is enabled (padlock open), so A, A = lock, submit; B unlocks; focus on a locked answer + A would unlock (`tap` on a locked answer unlocks), so the focus move is required. LB/RB move focus into the joker tray (prev/next available token); A arms, A again plays (two-tap arming, 09); B disarms. Francotirador: `navigate` moves the crosshair, A fires, B cancels.
  - Player screen: picking an existing name works by focus; typing a new name with a pad is part 6 (plan from task 214, SW-4). Until then the done-when below excludes "new player".
- **Audio unlock**: Chromium may not count a gamepad press as user activation, so a pad-only start may stay silent. Task 1 checks it in Chromium. If silent: the browser setup keeps today''s hint (first key/click); the shell sets `autoplayPolicy: "no-user-gesture-required"` (task 1 adds this line to `plans/18-steam-integration.md` "Desktop shell" for part 1''s plan, task 209).
- **Glyphs (IN-5)**:
  - Art: drawn in-house as inline SVG in `app/client/src/game/Glyph.svelte`, same style as `Icon.svelte` (VD-8: rounded, `currentColor`, 24×24 viewBox). Sets: xbox (A, B, X, Y as letter discs, LB, RB, View, Menu/Start, D-pad), playstation (✕ ○ □ △ as shapes, L1, R1, Create, Options, D-pad). No console makers'' art, no glyph pack (17: "CC0 set or draw them"), so no licence entry beyond "original" and no decision needed. If a worker finds drawing them clearly worse than a CC0 set (e.g. Kenney "Input Prompts", CC0, assets only, no code), it stops and adds a pm decision instead of switching.
  - **`Prompt.svelte`** (new, `game/`): `<Prompt action="confirm" />` renders the binding of an action for the current device: keyboard/mouse → today''s `<kbd>` text (`Enter`, `Esc`, `⌫`, `R`, `N`, `1`…), gamepad → `<Glyph>` of `padStyle`. Keyboard labels come from `input.ts`''s keymap (one copy); actions without a pad binding (`new`, `pick n`) render nothing with a pad (the control is reached by focus).
  - Device = plan 44''s `lastDevice`; mouse counts as keyboard for prompts. Switching is instant, no animation; sizes match today''s `kbd` chips so layouts don''t move.
  - Replaces every `<kbd>` in `app/client/src/game/*.svelte` (today: Game, Question, Player, CategoryPicker, JokerTray, Overlay) and the joker tokens'' `.key` letter (hidden with a pad unless decision 9 binds jokers to buttons). Answer tiles keep their A–D labels (they name answers, not keys), unless decision 9 picks option 2 (glyph next to the letter).
  - Credits: `plans/17-publishing.md` "Controller glyphs" gets "original, drawn for the game (`Glyph.svelte`)", so part 7 (task 215, PUB-5) lists them.
- Strings: none expected; if one is needed and `lib/i18n.ts` exists (plan 21), through `t()`, else a Spanish literal marked `// LUI-1`.
- No new dependency (no gamepad or glyph library).

## Coordination
- Plan 44 owns `input.ts`/`focus.ts`; this plan adds the gamepad source, a new action only if decision 9 needs one, and the focus move after a lock. Its keymap stays the one copy of key labels.
- Part 6 (task 214): letter picker for names, 1280×800 check of the glyph sizes. Part 7 (task 215): credits read 17''s glyph line.
- Plans 29 and 36 (Choice, settings, report screens): they use `<Prompt>` instead of `<kbd>` once it exists; task 4 converts any that landed and adds the rule to `04-ui-tv-display.md` "Input".

## Tasks (for the split)
1. **Gamepad source (IN-4)**: `lib/gamepad.ts` as above (loop, `step`, standard mapping for navigate/confirm/back/menu/replay/flag, `padStyle`, focus/hidden handling); started once from `Game.svelte` (or `main.ts`). Audio-unlock check and the 18 note. Check: `npm run check`, `npm run build`; throw-away script feeding fake pads to `step` (edges, stick dead zone and hysteresis, no repeat, two buttons at once); in Chromium with a pad if the worker has one, else the task note lists what the gamemaster should try. Not waiting for decision 9.
2. **Question screen and jokers with the pad (IN-4)**: per decision 9 (option 1: focus jump to «Respuesta final» after a lock, LB/RB into the tray, arming with A); Francotirador and Cambiazo checked with `navigate`/A/B. Waits for decision 9.
3. **Glyphs and prompts (IN-5)**: `Glyph.svelte` (both sets), `Prompt.svelte`, every `<kbd>` and the token letters replaced, 17''s glyph line. Check: `npm run check`; screenshots of Start, Question (incl. armed joker, Paso, aiming) and Cambiazo with `lastDevice` forced to keyboard, xbox and playstation (throw-away flag or devtools), no layout shift. Waits for decision 9.
4. **Audit and docs (IN-4, IN-5)**: walk a full game with a pad only (start → existing player → levels → every joker incl. unavailable ones → wrong and victory → overlay incl. undo, skip, volumes) and fix what''s missing; plans 29/36 screens on `<Prompt>` if they exist. Docs: `14-input.md` IN-4/IN-5 `[x]`, `04-ui-tv-display.md` "Input" (prompts through `<Prompt>`, no raw `<kbd>`), `directory.md` (`lib/gamepad.ts`, `Glyph.svelte`, `Prompt.svelte`), `plans/project.md`. Gamemaster check in Chromium on Linux and Windows with an Xbox-style pad (task note lists the steps).

## Done when
- A full game, every joker and every dialog work with an Xbox-style pad in Chromium on Linux and Windows (new player names: part 6); the prompts switch between keyboard, Xbox and PlayStation glyphs when the device changes; the family''s keyboard and mouse behave as before.', '2026-10-12T00:58:22Z', 213);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (46, 8, 'Deck layout and controller-only text entry (SW-4)', 380, 'The game reads well and plays with a pad only on the Steam Deck: every screen is checked at 1280×800 (Deck), 1280×720 (smallest) and 4K, text is at least 9 px at 800p (Valve''s Deck guideline), and a new player name can be entered without a keyboard. Part 6 of masterplan 8 (S3); owners `plans/18-steam-integration.md` (SW-4, "Platforms and display"), `plans/14-input.md` (Steam Deck), `plans/04-ui-tv-display.md` (Player, Input). The family''s TV game looks and plays as today: the fixes stay inside the `--u` system (D-29), the letter picker shows only for a pad.

## Depends on (a task stops and says so in its note if one is missing; leave it open)
- Plan 44 (action layer, focus, 500) and plan 45 (gamepad, `<Prompt>`, glyphs, 490): the picker is a focus grid driven by actions; the check covers the glyph sizes.
- Screens that change before S3 ends, so the check sees the final set: plan 29 (Choice screen, 400), plan 30 (390), plan 31 (UI-7, `Placeholder.svelte` gone, 500), plan 36 (report list, settings on Choice, 490/380). Task 2 only; task 1 doesn''t need them.
- Part 1 (desktop shell, plan from task 209) for the screenshots unless pm decision 6 says Playwright (see "Screenshots").
- Plan 21 (LUI-1): new strings through `t()` (`picker.*` keys) if `lib/i18n.ts` exists, else Spanish literals marked `// LUI-1`.

## Today (code as of 2026-10-11)
- `--u: min(100vw / 120, 100vh / 67.5)` (`app/client/src/game/theme.css`). At 1280×800 and 1280×720 the width wins: `--u` = 10.67 px, so the layout is the 720p layout with 80 px more height on the Deck. At 3840×2160: 32 px.
- 9 px at 1280 wide = 0.84 `--u`. Smallest sizes: `.credit` in `Question.svelte` at `0.8 * --u` (8.5 px, fails); `kbd`, joker `.key`, overlay hint at `0.9 * --u` (9.6 px, pass); `Placeholder.svelte` in `rem` (goes with plan 31).
- Player screen: name buttons (1–9) work by focus with a pad (plan 45); the «¿Alguien nuevo?» field needs a keyboard. Steamworks'' on-screen keyboard (`ShowFloatingGamepadTextInput`) is SW-8 (S5).

## Design
- **Size rule**: no `font-size` below `0.9 * var(--u)` (9.6 px at 1280 wide), no `px`/`rem` font sizes in `app/client/src/game/`. Fix = a bigger multiple of `--u`, never a media query or a separate Deck layout; one exception only if the 16:10 height leaves a screen visibly empty or broken, and then by `--u`-based layout (flex/grid), not a breakpoint. Rule written into `plans/10-visual-design.md` (type scale) and `04` ("Implementation notes").
- **Check sizes**: 1280×800, 1280×720, 1920×1080 (reference, the TV), 3840×2160 (sanity: nothing in px stays tiny, no blur on SVG/fonts; pictures stay at their own size per D-51, that''s intended).
- **What to look for**: text ≥ 9 px (computed style, not eyeballed), nothing clipped or overlapping, nothing outside the safe area (`--safe-x`/`--safe-y`), long content fits: the longest question text and longest answers of `app/data/pool.json` (worker picks them by script), 9 player names of 30 characters, the supply report with many levels missing, an error box.
- **Screens and states**: Start; Player (no players, 9 players, delete dialog, letter picker); Choice (plan 29/36: groups, bundles, mode, presets); Level; Select (4 cards); Question (text, image, video, audio; locked, armed joker, Paso, Francotirador aiming, Cambiazo both levels, «medio no disponible»); Correct; Wrong; Victory; Overlay (gamemaster and default mode); report list (plan 36); Credits (part 7) if it exists. Each with keyboard prompts and with Xbox glyphs (plan 45''s `lastDevice` forced).
- **Screenshots**: pm decision 6 (pending, asked by plan 21) picks the tool for screen checks; this plan follows its answer:
  - "Playwright": the same throw-away Playwright outside the project (temp dir, nothing in `package.json`), viewport per size.
  - Otherwise (or still pending): the desktop shell (part 1) at a fixed window size: a throw-away Electron main script (not committed) that opens the built client at each size without fullscreen, drives the screens by `webContents.sendInputEvent` (keys as the family presses them) and saves `webContents.capturePage()` PNGs. Text sizes from `executeJavaScript` over `getComputedStyle` of every visible text node''s element. Whatever the tool, the script also prints every element whose computed `font-size` is < 9 px.
  - PNGs go to a temp dir, not the repo; the task note lists findings and fixes.
- **Letter picker (controller-only names)** — decided here, no pm decision: the Player screen doesn''t change for the family (keyboard and mouse see exactly today''s field), the picker appears only for a pad.
  - Opens when `confirm` comes from the gamepad (`device: "gamepad"`) while the name field is focused (with no players the field gets focus on mount, as today), or from the field''s pad prompt («Ⓐ Escribir», `<Prompt action="confirm">`, shown only when `lastDevice` is the pad).
  - `app/client/src/game/LetterPicker.svelte` (new): modal dialog (plan 44 scope, glass panel as the delete dialog) over the Player screen; above the grid the name as typed (same look as the field). Grid of buttons, 9 columns: `A`–`Z`, `Ñ`, `Á É Í Ó Ú Ü`, `-`, then a row «Espacio», «⌫ Borrar», «Listo». Focus navigation is plan 44''s spatial focus (no own grid code); focus default «A», memory per open.
  - Writes into Player''s `name` (same `typed` cleanup, `maxlength` 30). Auto-capital: first letter and the letter after a space or `-` are upper case, the rest lower case (`maría josé` never happens by accident; «Ana-Sofía» works).
  - Pad: A types the focused key; B = delete the last letter, on an empty name closes the picker; Start (`menu`) closes it (dialogs treat `menu` as `back`, plan 44); Y (`replay`) unused. «Listo» (reached by focus, no extra button binding) submits like «¡A jugar!» (`onchoose(typed)`), disabled while `typed` is empty. Closing keeps the text in the field.
  - Mouse clicks work on every key (IN-1); physical keys while it is open: letters and `Backspace` type and delete (so a Deck with a USB keyboard still works), `Enter` = focused key, `Esc` closes.
  - Same name rules as the field: the server/engine checks are unchanged; an existing name chosen by typing picks that player as today.
  - S5 (SW-8): under Steam, `ShowFloatingGamepadTextInput` may replace the picker; the picker stays the fallback without Steam. One line in 18 ("Steamworks", on-screen keyboard).
- Strings: «Escribir», «Espacio», «Borrar», «Listo», picker title «Escribe tu nombre» via `t()` or marked literals (see "Depends on").
- No new dependency (no on-screen keyboard library).

## Tasks (for the split)
1. **Letter picker for player names with a pad (SW-4, IN-4)** — priority 380
   - `LetterPicker.svelte`, the hook in `Player.svelte` (gamepad `confirm` on the field, pad prompt), auto-capital helper (pure function), strings.
   - Check: `npm run check`, `npm run build`; throw-away script for the auto-capital helper («ana sofía» → «Ana Sofía», «-», «ñ», 30-char limit); in Chromium with a pad (or devtools forcing `device: "gamepad"` on dispatched actions): a new player created with the pad only, B deletes, Start closes and keeps the text, mouse clicks on keys work; with the keyboard the Player screen looks and behaves as today (no picker, no new prompt).
   - Docs: `04` "Player" (picker for a pad), `directory.md` (`LetterPicker.svelte`), `14-input.md` Steam Deck paragraph ("in-game letter picker, plan N").
2. **Screen check at 1280×800, 1280×720 and 4K, fixes (SW-4)** — priority 370 (after task 1, so the picker is checked)
   - Screenshot script per "Screenshots"; every screen and state above at the four sizes, keyboard prompts and Xbox glyphs; small-text report.
   - Fixes in `--u` multiples (at least `.credit` 0.8 → 0.9); repeat until the small-text report is empty and nothing clips at 720p.
   - Check: the 1920×1080 screenshots before and after differ only where a fix was intended (ImageMagick `compare` on the two sets); the family''s TV look is unchanged otherwise.
   - Docs: size rule in `10-visual-design.md` and `04` "Implementation notes"; `18-steam-integration.md` SW-4 `[x]` with a note (sizes, tool, fixes); `14-input.md` Deck paragraph; `plans/project.md` in sync. Real-Deck check goes to part 8''s checklist (task 216): the task note lists what to look at on the Deck (Linux build, Game Mode, built-in controls only).

## Done when
- Screenshots of every screen at 1280×800 and 1280×720 pass: no text below 9 px, nothing clipped or outside the safe area; 4K sane; the 1080p TV look unchanged except intended fixes.
- A new player can be created with a pad only; the family''s Player screen with keyboard and mouse is unchanged.
- SW-4 `[x]` in `plans/18-steam-integration.md`; the size rule in 10 and 04.', '2026-10-12T01:00:20Z', 214);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (47, 8, 'Credits screen and generated CREDITS.md (PUB-5)', 400, 'The build generates the game''s credits, `credits.json` for a new Credits screen and `CREDITS.md` for the shipped files. It lists every media file in `app/data/pool.json` (author, licence, source link) plus the fixed lists: sounds, fonts, controller glyphs, libraries, and the game''s own licence if decided. Part 7 of masterplan 8 (S3); owner `plans/17-publishing.md` ("Media licenses" → "Credits in the game", PUB-5). Works in the browser setup and later in the desktop shell. The family''s game is unchanged except for one new overlay item.

## Depends on
- Plan 26 "Licence data in the pool" (priority 900): slot fields `provider`, `license`, `license_url`, `author`, `author_url` (plus `restrictions`, `pd_reasons`). Task 1 waits until plan 26''s migration task (113) is done; if it isn''t, task 1 stops and says so.
- Plan 44 "Action layer and focus navigation" (500): `navigate`, `back`, scopes. Task 2 waits for plan 44''s tasks.
- Plan 45 "Gamepad input and button glyphs" (490): its task 3 writes "original, drawn for the game (`Glyph.svelte`)" into 17''s "Controller glyphs" line. The glyph entry here is conditional (only if `Glyph.svelte` exists), so no wait; the pad check in task 2 needs plan 45''s task 1 (otherwise the task note lists it for the gamemaster).
- Plan 40 "Code and content licence (OQ-35)" (290): conditional. If `LICENSE` (and a content licence file) exist at build time, the generator adds a "Game" section; if not, nothing. No wait.
- Plan 34 "Desktop shell (OQ-29)" and part 1 (task 209''s plan): the shell''s own entry (e.g. Electron, MIT, plus Chromium''s licence file that Electron ships) is added by whoever adds the shell. Task 1 adds one line to `plans/18-steam-integration.md` "Desktop shell" saying so.
- Plan 21 "t() helper" (500): screen strings through `t()` if `lib/i18n.ts` exists, else Spanish literals marked `// LUI-1`.

## Design
- **Data for the generator.** `app/data/pool.json` today keeps only `credit` per slot. Task 1 adds `provider`, `license`, `license_url`, `author`, `author_url` to `MEDIA_PLAY_FIELDS` and `BACKGROUND_PLAY_FIELDS` in `authoring/tools/pool_export.py` (as plan 26 foresaw), then `qgen export`; `qgen validate` passes. `restrictions` and `pd_reasons` stay in the source pool (audit data, not credits). Size: ~1,150 slots × ~150 bytes, fine.
- **Generator: a Vite plugin** `app/client/credits.ts` (new, imported by `vite.config.ts`; TypeScript, no dependency).
  - Why Vite: `npm run build` runs everywhere (dev shell, `nix build .#app`, the shell builder of part 3, CI); no Python at build time; lives in `app/` (D-35). `app/` is in the nix fileset already.
  - `build`: emits `credits.json` and `CREDITS.md` at the root of `dist/` (next to `index.html`). Dev (`npm run dev`): a `configureServer` middleware serves `/credits.json` from the same function.
  - Media: one entry per distinct `file_url` across `media` and `background` of all questions (all bundles; pool.json has only approved ones). Fields: kind (image/audio/video/background), title (from `source_url`: Commons `File:` name without extension, URL-decoded; others the last path segment), author (`author`, else `credit`''s author part, else «Autor desconocido»), `author_url`, `license`, `license_url`, `source_url`, provider name. Sorted by kind, then title.
  - Build fails (clear message, ids listed) when a picked slot lacks `license` or `source_url`; warns for GFDL (needs the full text; PUB-3 replaces such files).
  - Sounds: parsed from `app/client/public/audio/CREDITS.md` (one source; columns File, Used for, Source, Author, Licence; Markdown links kept). Build fails if a row doesn''t parse or an `.m4a` in `public/audio/` has no row. Elgar note: its own line under Sounds (composition public domain, Elgar † 1934; recording by the US Marine Band, a US government work).
  - Fonts: constant entries Baloo 2 and Nunito, SIL OFL 1.1, linking the shipped `fonts/OFL-*.txt`.
  - Controller glyphs: «original, dibujados para el juego» if `src/game/Glyph.svelte` exists.
  - Libraries: Svelte (only runtime code in the bundle; version and licence from `node_modules/svelte/package.json`, full MIT text from its `LICENSE.md` into `CREDITS.md`, since MIT asks for the notice in copies). Build tools (Vite, TypeScript) don''t ship: not listed. The shell entry: see "Depends on".
  - Game: `LICENSE` / content licence from the repo root if present (plan 40); `CREDITS.md` names them and their scope.
  - `CREDITS.md`: short intro (licences per file; CC BY-SA adaptations such as the blurred backgrounds (D-15) and crops are offered under the same licence), then sections Game, Media in the questions (table: title, author with link, licence with link, source link), Sounds, Fonts, Controller glyphs, Libraries. English (shipped legal text; translations are S4).
- **Credits screen** `app/client/src/game/Credits.svelte` (new).
  - Opened from a new ☰ overlay item «Créditos» (`Overlay.svelte` `items`, left column, below «Pantalla completa»); the overlay is reachable from every screen incl. start (Esc, ☰ button, pad Start). No change to the start screen.
  - Fetches `credits.json` with a relative URL on first open (works from the Python server and from the shell''s `dist/`), keeps it in memory; error line if it fails.
  - Full-screen glass panel over the current screen (the game underneath stays as it was); sections as headings; one row per entry: title, author, licence, provider; source URL as small text, not a link (the TV/shell must not navigate away). Counts per section in the heading.
  - Input via plan 44: own scope; `navigate` up/down scrolls by ~70 % of the panel, left/right jump to the previous/next section; `back` (Esc, Backspace, pad B) and `menu` close it and return to the overlay; mouse wheel and scrollbar work. No focusable rows (1,000+ entries).
  - Text ≥ 9 px at 1280×800 in the `--u` system (D-29; part 6, plan 46); rows use `content-visibility: auto` so the long list scrolls smoothly on the Deck.
- **Shipped files:** `CREDITS.md` sits in `dist/`, so the nix package (`share/trivia/app/client/dist/`) and the shell build (part 3, which bundles `dist/`) contain it. Part 3 may also copy it to the artefact''s root; task 3 adds that line to plan 18 "Builds and depots".

## Tasks (for the split)
1. **Licence fields in the export and the credits generator (PUB-5)** — waits for plan 26 task 113.
   - `pool_export.py` fields, `qgen export`, `qgen validate` green; `app/client/credits.ts` and its use in `vite.config.ts` as above; line in plan 18 "Desktop shell" (shell entry).
   - Check: `npm run build` → `dist/credits.json` and `dist/CREDITS.md`; throw-away script: every distinct `file_url` in `app/data/pool.json` appears once with author, licence and source link; every `.m4a` in `public/audio/`; removing a `license` in a temp copy of the pool fails the build. `nix build .#app` contains `CREDITS.md`. `npm run check`.
   - Docs: `directory.md` (`credits.ts`, generated `credits.json`/`CREDITS.md`), `plans/19-repo-layout.md` if it lists client build files.
2. **Credits screen (PUB-5)** — waits for plan 44''s tasks; after task 1.
   - `Credits.svelte`, overlay item, scope and actions as above; strings per plan 21''s state.
   - Check: `npm run check`; screenshots at 1920×1080 and 1280×800 (top, middle of the media list, sounds); keyboard (arrows, Esc), mouse (wheel, close button) and, if plan 45 task 1 is done, a pad (D-pad, B) in Chromium; otherwise the task note lists the pad steps for the gamemaster. The family''s keys and the overlay''s other items behave as before.
3. **Docs and close-out (PUB-5)** — after task 2.
   - `plans/17-publishing.md`: "Credits in the game" says how it works (generator, screen, `CREDITS.md`); PUB-5 `[x]` with a note. `plans/04-ui-tv-display.md` (overlay item, Credits screen) and `plans/05-gamemaster-controls.md` if it lists the overlay items. Plan 18 "Builds and depots": `CREDITS.md` at the artefact root (part 3). `plans/project.md` in sync.

## Done when
- Every media file in `app/data/pool.json` appears in `credits.json` and `CREDITS.md` with author, licence and source link; sounds (incl. the Elgar note), fonts, glyphs (if drawn) and Svelte too.
- `npm run build` and `nix build .#app` contain `CREDITS.md`; the shell build (part 3) does because it ships `dist/`.
- The Credits screen opens from the ☰ overlay and scrolls and closes with keyboard, mouse and pad.', '2026-10-12T01:02:33Z', 215);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (48, 8, 'S3 close-out and platform test', 140, 'The last step of milestone 8 (S3). Part 8 of masterplan 8. Once every other S3 part is implemented, this plan hands the gamemaster one test checklist (Windows, Linux, Deck; controller only; offline; a full game; the save survives a restart), records what they report through a pm decision, and brings the docs in line. Workers own no Windows machine or Deck: they prepare the checklist and record results; they never tick a row themselves. Docs and pm only; no code (failures become tasks in the owning plans).

## Depends on (every task waits)
- Plans 44 "Action layer and focus navigation", 45 "Gamepad input and button glyphs", 46 "Deck layout and controller-only text entry", 47 "Credits screen and generated CREDITS.md", and the plans written by tasks 209 (desktop shell, SW-2), 210 (file saves, SW-3), 211 (local builds, SW-5/SW-6): all their tasks done or dropped.
- Guard at the start of each task: `pm show` of this plan and `pm plans list`. If another milestone-8 plan still has open tasks: if one of them waits for a pending decision, `pm task-pending-decision <this task> <that decision>`; otherwise stop without changes and say so (the queue brings the task back). Never drop tasks of other plans.
- Not the milestone''s "post-milestone cleanup" (pm queues it once nothing is open); this plan doesn''t set the milestone status.

## The checklist
- Lives in `plans/18-steam-integration.md`, new section "S3 platform test" (after "Steam Deck Verified"); one table per platform, columns: check, result (pass / fail / skipped), note. Short intro: build commit, date, artefact names.
- Reuses, doesn''t copy: part 3''s offline start checklist (plan from task 211) is linked or merged in; the "what the gamemaster should try" items in the task notes of plans 45 and 46 (`pm show` of their tasks; plan 46 task 3: real Deck in Game Mode) become rows.
- Before the test (worker checks what it can): artefacts built from one commit (part 3''s command); `qgen validate` clean; `trivia-media sync --status approved` run before the build; `CREDITS.md` in the artefact.
- Platforms: Windows x64 (clean machine, no Node/Python), Linux x64 without Nix, Steam Deck in Game Mode (Linux build added as a non-Steam game; built-in controls only). Optional row: Windows build on the Deck via Proton, marked "if cheap".
- Rows per platform:
  - Offline: network off before install and start; no error, no launcher, no console window.
  - Start: fullscreen; F11/menu toggles windowed and back.
  - Controller only (keyboard and mouse unplugged; Xbox-style pad on Windows/Linux): create a new player with the letter picker; pick an existing player; play to level 12 or a loss.
  - Every joker once, including Paso dialog, Francotirador aim and Cambiazo both levels; the ☰ overlay via Start (volume, presets); every dialog closes with B.
  - Glyphs match the pad (Xbox; PlayStation pad if at hand); after a key press they switch to keyboard prompts and back on a pad press.
  - Media: an image, a video and an audio question play; music and sounds audible.
  - Credits screen opens and scrolls with the pad.
  - Save: quit mid-game and restart → players and burned questions kept; force-quit (Deck: Steam button → exit game) and restart → same.
  - Deck only: text readable at arm''s length (800p), nothing cut off, suspend and resume mid-question.
- Family check (once, not per platform): `trivia` + browser on the TV with keyboard plays a round as before; `state/` save intact.

## Tasks
1. **Checklist and the test decision**
   - Guard (above). Write the "S3 platform test" section in `18-steam-integration.md` as above, results empty.
   - Run what a worker can (build command, `qgen validate`, artefact contains `CREDITS.md`); note it in the section''s intro.
   - `did=$(pm decision add "S3 test passed?" --body - …)` with the whole checklist in the body (platform tables as Markdown, how to report: copy the tables, fill result and note; "skipped" needs a reason) and options `passed`, `passed with minor issues (list them; they go to the backlog)`, `failed (list the failing rows)`.
   - `pm task-pending-decision` for tasks 2 and 3 of this plan on `did`.
   - Done when: the section exists, the decision is pending, tasks 2 and 3 wait for it.
2. **Record the result**
   - Copy the reported results into the section''s tables (date, build commit); add a D-entry in `plans/decisions.md` only if the answer settles something (e.g. Proton row dropped for good).
   - `passed`: done. `passed with minor issues`: each issue into `plans/backlog.md` with the owning plan file''s task ID prefix; done.
   - `failed`: per failing row a `pm task add` in the plan that owns it (shell/saves/builds plans from tasks 209–211, or 44–47) with the row, the note and how to reproduce, at that plan''s priority; then a new decision "S3 re-test passed?" with only the failed rows (plus the full-game row), `pm task-pending-decision` for this task and task 3 on it; stage and stop without closing. Repeat until passed.
   - Done when: the section shows a passing result for every non-optional row.
3. **Docs close-out** (after task 2)
   - `plans/11-steam.md`: S3 row marked done with the date and the checklist link; ST-4 (release checklist) notes that it starts from the S3 checklist.
   - `plans/14-input.md`, `17-publishing.md`, `18-steam-integration.md`: IN-2..IN-5, PUB-5, SW-2..SW-6 ticked with notes (check, don''t redo, the parts'' own ticks); status lines brought up to date (e.g. `stub` → `draft`, or `agreed` where everything for S3 is decided); `plans/README.md` status column to match.
   - `plans/project.md`: "Steam track" paragraph says S3 done (date); any ticked task ticked there too; open-questions rows that S3 resolved removed.
   - Masterplans 9–11 (S4–S6): if still "tbd.", nothing (their writers read the plan files). If written and S3 changed their scope (SW-6 CI moved to S5, media bundle size or depot layout, Proton or Deck findings for SW-12, letter picker vs. on-screen keyboard for SW-8), add a short dated note with `pm plan edit <id> --body -`. Milestone bodies change only if they name something S3 ruled out; listed in the task note.
   - Done when: the milestone''s "Done when" holds and is cited in the task note (decision id, date); `qgen validate` unaffected.', '2026-10-12T01:03:55Z', 216);

INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (1, 1, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, plan 1 body; plans/decisions.md (D-52), plans/open-questions.md, plans/project.md (OQ-17 resolved)', 'Write plan 1, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T20:08:18Z', '2026-10-11T23:15:56Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (2, 2, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, tasks.sql (plan 2 body)', 'Write plan 2, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', '2026-10-11T23:55:45Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (3, 3, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, tasks.sql (plan 3 body)', 'Write plan 3, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', '2026-10-12T00:06:58Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (4, 4, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, plan 4 body (tasks.sql)', 'Write plan 4, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', '2026-10-12T00:17:17Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (5, 5, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, plan 5 body (tasks.sql)', 'Write plan 5, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:56Z', '2026-10-12T00:21:52Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (6, 6, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, tasks.sql (plan 6 body; tasks 134-136)', 'Write plan 6, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:56Z', '2026-10-12T00:32:24Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (7, 7, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-12, plan 7 body (10 parts); tasks.sql', 'Write plan 7, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:56Z', '2026-10-12T00:38:11Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (8, 8, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-12, tasks.sql (plan 8 body: 8 parts)', 'Write plan 8, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', '2026-10-12T00:52:44Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (9, 9, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, masterplan 9 (tasks.sql)', 'Write plan 9, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', '2026-10-12T01:09:35Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (10, 10, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, masterplan 10 (tasks.sql)', 'Write plan 10, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', '2026-10-12T01:12:46Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (11, 11, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, masterplan 11 (tasks.sql)', 'Write plan 11, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:55:09Z', '2026-10-12T01:15:15Z', NULL);
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
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (25, 12, 'Targets file, loader and validate check', 'work', 'done', NULL, '2026-10-11, authoring/data/targets.json (decision 1 numbers), authoring/tools/targets.py (load_targets, category_shares, problems; skips about/batch_health keys for D-55), layout.TARGETS, qgen validate check, directory.md. Throw-away edits (level 15 missing, sum 5001) fail validate with the right messages; otherwise validate''s only error is the known q-0021 licence (plan 26)', 'Part "Targets file" of plan 12 (D-53, already logged in `plans/decisions.md`).

- New `authoring/data/targets.json`: `{"about": "…", "base": {"total": 5000, "difficulty": {"1": n, …, "15": n}}}`, numbers from pm decision 1.
- Loader `load_targets(bundle)` in `authoring/tools/` (in `qgen.py`, or a small `targets.py` if the authoring server will import it too, see the `/api/targets` task); returns `None` for a bundle without targets.
- Helper for the derived per-category share: `total × subcategories in category / subcategories in bundle` (guide only).
- `qgen validate`: levels = the scale in `app/data/age-groups.json`, every value ≥ 0, sum = `total`.
- `directory.md`: line for the new file.

Done when: `qgen validate` passes; a throw-away edit (wrong sum, missing level) makes it fail.', '2026-10-11T23:50:08Z', '2026-10-12T02:12:00Z', 19);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (26, 12, 'qgen report: progress vs. targets', 'work', 'done', NULL, '2026-10-11, authoring/tools/qgen.py (report_progress, --bundle), README.md, AGENTS.md', 'Part "Progress view" of plan 12, CLI side. Needs the targets file and loader (previous task).

- `qgen report`: new section "progress vs. targets (base)": per difficulty `approved / target`, missing count, percent; a total line; per broad category `approved / derived share`.
- Approved = status `approved`, bundle `base`, regardless of burns.
- `--bundle <id>` for another bundle with targets; skip the section quietly when the bundle has none.

Done when: `qgen report` prints the section with today''s numbers (well under target at 9–15).', '2026-10-11T23:50:08Z', '2026-10-12T02:12:43Z', 19);
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
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (29, 13, 'qgen report --calibration and baseline', 'work', 'done', 710, '2026-10-11, authoring/tools/qgen.py (qgen report --calibration, calibration()), README.md, AGENTS.md, plan 13 baseline; qgen validate''s only error is q-0021 (pre-existing, decision 10)', 'Part "Measurement" of plan 13. The baseline comes first, so the fixes can be measured.

- `qgen report --calibration [<batch>…]` in `authoring/tools/qgen.py`: per target level 1–15: n drafted, mean drafted / rated / final difficulty, mean concept `known_at`, merged and approved counts.
- Reads `work/<batch>/slots.json`, `drafts/`, `ratings/`, `ids.json` and the pool; default: the last two batches. Missing ratings (batch not rated yet) → `–`, no error.
- Write it so plan 16''s batch health metrics ("difficulty spread vs. targets") can call the same function; don''t build it twice.
- Record the batch-7 and batch-8 numbers in plan 13''s "Baseline" section (`pm plan edit 13 --body -`); batch-8 rated numbers once it''s rated, else note that they''re pending.
- `README`/`AGENTS.md` command lists: mention the flag where `qgen report` is listed.

Done when: `qgen report --calibration` prints the table for batch-7 and batch-8, matching the throw-away baseline in plan 13 (±0.1); `qgen validate` clean.', '2026-10-11T23:50:50Z', '2026-10-12T01:28:17Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (30, 13, 'rate.md on the 1–15 scale; re-check DIFFICULTY_GAP', 'work', 'done', NULL, '2026-10-11, authoring/tools/prompts/rate.md, authoring/tools/qgen.py: difficulty_estimate on 1–15 (schema has no bounds); re-rated 24 approved at 10–15 with opus: 16 estimates >10, mean diff −0.8, mean |diff| 1.5, 4 gaps ≥3 (all rater lower); DIFFICULTY_GAP kept at 3', 'Part "Fixes → Rater scale" of plan 13. `authoring/tools/prompts/rate.md` asks for `difficulty_estimate` 1–10, so the rater can''t rate above 10 and every question at 13+ looks overrated to `revise` (`DIFFICULTY_GAP = 3`, `qgen.py`).

- `rate.md`: `difficulty_estimate` on the shared scale 1–15, as defined in the house style (refer to it, don''t restate it); fix the JSON schema bounds in `qgen.py` if the rating schema has them.
- Re-check `DIFFICULTY_GAP`: with a throw-away script, re-rate ~20 approved questions at 10–15 (few LLM calls; no batch run) and compare estimate vs. stored difficulty. Keep 3 or change it with a short reason in the comment; log a decision in `plans/decisions.md` if the meaning changes.

Done when: rate prompt and schema allow 1–15; the throw-away check shows estimates above 10 for hard questions; `qgen validate` clean.', '2026-10-11T23:50:50Z', '2026-10-12T01:45:35Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (31, 13, 'Concept draw follows known_at', 'work', 'done', NULL, '2026-10-11, authoring/tools/concepts.py. Dry run (draw_slots, 160 base subs, seeds dry31-a/b, 10 slots each, ~213 per level), mean known_at − target: 1 +1.41, 2 +0.83, 3 +0.49, 4 +0.29, 5 +0.21, 6 +0.14, 7 +0.12, 8 +0.23, 9 +0.12, 10 +0.06, 11 −0.02, 12 +0.09, 13 −0.06, 14 −0.42, 15 −0.76 (was 7–9 at 1–8, ~11 at 13–15). Within ±1 except level 1: supply runs out there (473 unused at known_at 1, 604 at 2; 38 of 160 subs have none at 1–2) and the ±1 window at the scale edge only reaches upward. qgen validate: only the known pre-existing error (q-0021 GFDL licence, PUB-2), same without this change', 'Part "Fixes → Concept draw" of plan 13. `concepts.draw_concepts` (`authoring/tools/concepts.py`) weights `1/(1+uses)² / (1+|known_at−d|/2)`; use count dominates, so mean `known_at` per target sits at 7–9 for targets 1–8 and ~11 for 13–15.

- Draw from a window: concepts with `|known_at − d| ≤ 1`, widen to ±2, ±3 … only when the window has no unused, unretired concept left; use count breaks ties inside the window. Retired concepts never (unchanged).
- Keep the signature, so `draw_slots` and the focus-group path keep working; update the docstring (D-38).
- Throw-away check: a seeded dry run of `draw_slots` (no LLM calls) over the base subcategories; mean `known_at` per target within ±1 at every level 1–15, or report the levels where the supply runs out.

Done when: the dry-run numbers are in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:50:50Z', '2026-10-12T01:46:51Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (32, 13, 'Write the confirmed difficulty anchors into the house style', 'work', 'done', 690, '2026-10-11, authoring/tools/prompts/house-style.md (10 anchors at 9–15, levels as proposed: decision 11 answered yes, no corrections); qgen validate: only the pre-existing q-0021 licence error (plan 26)', 'Second half of "Fixes → Prompts" of plan 13. Waits for the gamemaster''s answer to the anchor decision the previous task creates.

- Add the confirmed anchors (questions at 9–15 with the gamemaster''s levels) to the calibration section of `authoring/tools/prompts/house-style.md`, next to the existing 1–6 examples; levels as the gamemaster answered, not as proposed.
- Where the gamemaster corrected a level, set it on the question in `authoring/data/questions.json` only via the existing tooling (not by hand); if there''s none, log it in `plans/backlog.md`.

Done when: house style has anchors spread over 9–15; `qgen validate` clean.', '2026-10-11T23:50:50Z', '2026-10-12T02:14:00Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (33, 13, 'Hard-question guidance in draft.md and house style; propose anchors', 'work', 'dropped', NULL, 're-added as the next task with the follow-up task id filled in', 'First half of "Fixes → Prompts" of plan 13. Hard targets are drafted ~3 levels low; house style''s calibration examples are all at 1–6 and all say "AI guessed too high".

- `authoring/tools/prompts/house-style.md`: what makes a question hard on the 1–15 scale (who can answer it: few adults, specialists; not obscure trivia nobody could know).
- `authoring/tools/prompts/draft.md`: the ±1 tolerance must not become a habit of rounding down; aim at the target, not below it.
- Anchor candidates: pick ~8 approved questions at 9–15 (spread over levels and broad categories) and propose them with `pm decision add "Difficulty anchors 9–15: are these levels right?" --body …` (id, question, answer, stored level each; options e.g. "levels as proposed" / "corrections in the answer"). Then `pm task-pending-decision TASK_4B <decision id>` so the follow-up task waits for the answer.
- Don''t write the anchors into the house style here.

Done when: prompts updated, decision created and task TASK_4B pending on it; `qgen validate` clean; no batch run.', '2026-10-11T23:50:50Z', '2026-10-11T23:51:05Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (34, 13, 'Hard-question guidance in draft.md and house style; propose anchors', 'work', 'done', NULL, '2026-10-11, authoring/tools/prompts/house-style.md (hard-question guidance 11–15), authoring/tools/prompts/draft.md (aim at target, ±1 not a habit of rounding down); decision 11 proposes 10 anchors at 9–15, task 32 pending on it; qgen validate errors only on q-0021 licence (pre-existing, plan 26)', 'First half of "Fixes → Prompts" of plan 13. Hard targets are drafted ~3 levels low; house style''s calibration examples are all at 1–6 and all say "AI guessed too high".

- `authoring/tools/prompts/house-style.md`: what makes a question hard on the 1–15 scale (who can answer it: few adults, specialists; not obscure trivia nobody could know).
- `authoring/tools/prompts/draft.md`: the ±1 tolerance must not become a habit of rounding down; aim at the target, not below it.
- Anchor candidates: pick ~8 approved questions at 9–15 (spread over levels and broad categories) and propose them with `pm decision add "Difficulty anchors 9–15: are these levels right?" --body …` (id, question, answer, stored level each; options e.g. "levels as proposed" / "corrections in the answer"). Then `pm task-pending-decision 32 <decision id>` so task 32 (writes the anchors in) waits for the answer.
- Don''t write the anchors into the house style here.

Done when: prompts updated, decision created and task 32 pending on it; `qgen validate` clean; no batch run.', '2026-10-11T23:51:06Z', '2026-10-12T01:47:52Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (35, 13, 'Deficit weights in target_weights()', 'work', 'done', NULL, '2026-10-11, authoring/tools/qgen.py: target_weights(pool, bundle) = max(0, target − approved) per level for bundles with targets (focus path unchanged; even weights without targets or deficits); draft prints the drawn target histogram. Seeded dry run (seed 42, 40 subs × 12 slots = 480, base): deficits 1–15 = 214/283/354/346/338/303/349/383/256/273/269/192/182/106/117 → drawn 26/34/43/42/41/37/42/46/31/33/33/23/22/13/14 (expected within ±0.5). qgen validate: only the known q-0021 licence error (PUB-2), same before the change; no batch run.', 'Part "Aim at gaps" of plan 13 (D-54), first step. Needs plan 12''s targets file and loader (task 25, same decision).

- `target_weights()` in `authoring/tools/qgen.py`: with targets for the batch''s bundle (`load_targets(bundle)`), weight per level = `max(0, target − approved)`; approved = status `approved` in that bundle. Even weights (D-40) when the bundle has no targets or every deficit is 0; the focus-group path (`LEVEL_WEIGHTS`) unchanged.
- Print the drawn target histogram at the start of `draft`, so the batch log shows the batch''s shape.
- Throw-away check: seeded dry run of `draw_slots` (no LLM calls) draws targets roughly proportional to the deficits.

Done when: dry-run histogram in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:51:06Z', '2026-10-12T02:13:35Z', 20);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (36, 13, 'Subcategory ranking and per-subcategory targets by deficit and concept supply', 'work', 'done', 690, '2026-10-11, authoring/tools/{batches,qgen,targets}.py, authoring/RUNBOOK.md. targets.deficits() shared by target_weights() and batches.subcategories() (rank by Σ approved × deficit share; 85/92 same as before, new: Baloncesto, Tenis, Videojuegos, Pixar, Disney …). assign_difficulties: concepts within ±1 per sub × level, iterative proportional fitting to slots per sub and deficit counts per level, rounded slot by slot; draw_concepts picks scarce levels first, slots shuffled after. Seeded dry run (85 subs with concept lists, 18 slots, seed 1): counts per level ∝ deficits (1:83 … 8:148 … 14:41 15:45); mean known_at 1.6 2.3 3.4 4.4 5.3 6.2 7.1 8.2 9.3 10.1 11.3 12.0 13.0 13.8 14.4, all within ±1 (seed 2 and 4 slots likewise; before fitting, greedy gave 14→12.3). 15s only to subs with hard concepts (37 subs, 1–3 each). Start page shows 92 next-batch subs. qgen validate: only the known q-0021 licence error (PUB-2), same before the change; no batch run.', 'Part "Aim at gaps" of plan 13 (D-54), second step. After the `target_weights()` task.

- `batches.subcategories()` (`authoring/tools/batches.py`, shared with the authoring start page): rank by `Σ_level approved(sub, level) × deficit_share(level)`, ties as now; still `batches.SHARE` of the subcategories (D-46); no new `qgen batch` arguments (D-36). Without targets: ranking as today.
- `assign_difficulties`/`draw_slots` (`qgen.py`): hand each subcategory the targets its concept list can carry (unused, unretired concepts with `known_at` near the target) instead of a plain shuffle; a subcategory without hard concepts gets no 15s.
- Check the authoring start page still shows the next batch''s subcategories (`trivia-authoring`).
- Throw-away check: seeded dry run of `draw_slots`: targets weighted by deficit, mean concept `known_at` per target within ±1 (plan 13 "Done when").

Done when: dry-run numbers in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:51:06Z', '2026-10-12T02:17:05Z', 20);
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
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (40, 15, 'Overlap candidate finder and qgen report --overlaps', 'work', 'done', 710, '2026-10-11, authoring/tools/qgen.py (overlap_candidates, stem, qgen report --overlaps), README.md, AGENTS.md; replay 6/6, numbers in plan 15 Baseline', 'Part "Overlap check before merge" (B-5) of plan 15, code only, no LLM. Shapes the next batch most, so it runs first.

- Candidate finder in `authoring/tools/qgen.py` or a small `authoring/tools/overlap.py`: for a draft, pool questions of every bundle (status ≠ `rejected`) and earlier drafts of the same batch where:
  - normalized answers equal or similar (`SequenceMatcher` ≥ 0.8, or one contains the other); numbers and yes/no excluded as in `duplicates()`;
  - draft''s concept or answer stem-matches the other''s concept or answer (lowercase, no accents, drop trailing «s»/«es»);
  - draft''s concept or answer occurs in the other''s question or `fun_fact`, or the other way round.
  - Cap ~8 per draft, closest first. No new dependencies. `duplicates()` stays as is.
- `qgen report --overlaps`: the same finder over the approved pool, pairs listed (ids, answers, why matched); listing only. Mention the flag where `qgen report` is listed (README, AGENTS.md).
- Replay (throw-away script): batch-7''s merged questions against the pool before batch-7 (ids < q-0596) must list q-0646/q-0217, q-0644/q-0957, q-0689/q-0279, q-1210/q-0315; B-5''s q-0369/q-0341 and q-0420/q-0328 against their pools. Record recall and candidates per draft (mean, max) in plan 15''s Baseline (`pm plan edit 15 --body -`).
- Not wired into `rate` yet (next task).

Done when: replay finds all six pairs, numbers in plan 15; `qgen validate` clean; no batch run.', '2026-10-11T23:52:31Z', '2026-10-12T01:31:01Z', 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (41, 15, 'no_overlap criterion in rate; drop overlaps at merge', 'work', 'dropped', NULL, 're-added with the plan''s batch-8 guard (only mid-rate blocks) and task 40''s overlap_candidates()', 'Part "Judge in rate" of plan 15. After the candidate finder task.

- Check `work/batch-8` first: if batch-8 is between `draft` and `merge` (rated partly or not yet merged), don''t change `rate`/`merge` now; stop and note it (plan 17''s batch-run task finishes batch-8 first).
- Grouped `rate` call (PE-1) in `authoring/tools/qgen.py`: each draft''s candidates (id, question, answer, concept) in the payload; new hard criterion `no_overlap` in the rating schema and `authoring/tools/prompts/rate.md` (5 = asks a different fact; ≤ 3 = knowing one answer gives the other away, or the same fact again). Within-batch pairs: the later draft fails.
- `merge`: a `no_overlap` hard fail is dropped with reason `overlap like q-…` in `dropped.json`; the concept isn''t retired.
- Prompts are changed here as an implementation task, never inside a batch run (RUNBOOK).
- Check (throw-away script, two LLM calls): rate ~20 batch-7 drafts incl. the four known overlaps, once without and once with candidates; the four fail `no_overlap`, the others don''t. Result in the task note.

Done when: check passes; `qgen validate` clean; no batch run.', '2026-10-11T23:52:31Z', '2026-10-12T01:31:50Z', 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (42, 15, 'Needs-work problems in review and record; classifier for old questions', 'work', 'done', NULL, '2026-10-11, authoring/tools/qgen.py (PROBLEMS, review schema, record, guess_problems/review_problems, validate), prompts/review.md, authoring/server/main.py (undo keeps problems). Classifier over batch-7''s 112 needs_work (reviews + fixed rules rebuilt from work/batch-7; multi-label, guessed): giveaway 55, media 43, overlap 19, fact 18, style 4, other 3. qgen validate: only the known q-0021 licence error (PUB-2), unchanged; no batch run.', 'Part "Needs-work reasons" of plan 15. Today `needs_work` reasons are only free text in `review.feedback`.

- `REVIEW_SCHEMA` (`authoring/tools/qgen.py`): `problems`, array of `giveaway`, `fact`, `ambiguity`, `overlap`, `media`, `difficulty`, `style`, `other`; stored in `q.review.problems`. One shared constant; plan 16''s audit task may already have defined it: reuse it.
- `record`: adds `media` (no adequate media) and `fact` (fact check not confirmed) for the fixed rules.
- `authoring/tools/prompts/review.md`: when to use each problem.
- Keyword classifier for questions without `problems` (`No se encontró una imagen adecuada` → media, `q-\d{4}` → overlap, `pista` + `regala|delata|da la respuesta` → giveaway, …), results marked as guessed; for the reports only, no backfill into the pool.
- `qgen validate`: `problems` values from the list when present.

Done when: classifier run over batch-7''s needs_work (throw-away script) gives counts per problem, in the task note; `qgen validate` clean; no batch run.', '2026-10-11T23:52:31Z', '2026-10-12T01:49:37Z', 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (43, 15, 'Batch health: health.py, qgen report --batches, Health section, baseline; propose thresholds', 'work', 'dropped', 690, 're-added as the next task with task 44''s id filled in', 'Part "Batch health" of plan 15, plus the threshold decision (plan''s tasks 4 and 5). After the problems task (needs_work by problem) and the no_overlap task (overlap drops); without them those rows read "n/a".

- `authoring/tools/health.py`: `batch_health(run) -> dict` from `work/<run>/` and the pool; metrics as listed in plan 15 (drops by reason, merged/approved/needs_work, needs_work by `problems` incl. the guessed classifier, overlap rate, difficulty, variety, media share, mean `fun`, cost, calls, wall time).
- Difficulty vs. target: reuse plan 13''s `--calibration` code (task 29) if it exists; else "n/a". Approved per level vs. deficit: plan 12''s `load_targets` (task 25) if it exists; else "n/a".
- `qgen report --batches [<batch>…]` (default batch-4 onward): one column per batch.
- `batch-report`: "## Health" at the top of `authoring/reports/<batch>.md` with each metric and the previous two batches'' values (✓/✗ comes with the thresholds task); regenerates `authoring/reports/batches.md` with the same table. `directory.md`: lines for `health.py` and `batches.md`.
- Baseline: run over batch-4…7 (and batch-8 if recorded); record the table in plan 15 (`pm plan edit 15 --body -`). Close PE-6, PE-13, MP-11: numbers into `plans/20-pipeline-efficiency.md` and `plans/23-media-providers.md`, mark them `[x]`.
- Decision: `pm decision add "Batch health thresholds and stop rule?"` with the plan''s first-guess thresholds adjusted to the baseline in the body; options: recommended set (first) / looser set / warnings only, no stop. Then `pm task-pending-decision <thresholds task id> <decision id>` (the task "Batch health thresholds, stop rule and ack").

Done when: `qgen report --batches` prints batch-4…7; plan 15 has the baseline; PE-6/PE-13/MP-11 closed; decision created and the thresholds task waits on it; `qgen validate` clean; no batch run.', '2026-10-11T23:52:32Z', '2026-10-11T23:52:38Z', 22);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (44, 15, 'Batch health thresholds, stop rule and ack', 'work', 'open', 680, NULL, 'Part "Thresholds" of plan 15 (D-55). Waits for the threshold decision (created by the batch-health task) and for pm decision 1 via plan 12''s targets file (task 25).

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
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (64, 20, 'create tasks for plan 20', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 76–79)', 'Split plan 20 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:03:19Z', '2026-10-12T00:05:40Z', 57);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (65, 18, 'Fixture recorder skeleton (PORT-1)', 'work', 'done', NULL, '2026-10-11, authoring/tools/record_fixtures.py: temp state guard, shuffle tape/now/categories patches, main.py dispatch, DB snapshots, deterministic writer, --check; registries CATEGORIES/POOLS/SCENARIOS + @scenario for tasks 66–70; throw-away 3-step run deterministic, state/game.sqlite unchanged', 'New `authoring/tools/record_fixtures.py` per plan 18 ("Decisions taken here", "Safety"). Python stdlib only.

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

Done when: a throw-away scenario of 3 steps (new, pick, answer) records with a tape and DB snapshots, and `state/game.sqlite` mtime + checksum are unchanged after the run.', '2026-10-12T00:04:11Z', '2026-10-12T01:51:28Z', 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (66, 18, 'Synthetic fixture categories and pools (PORT-1)', 'work', 'done', NULL, '2026-10-11, authoring/tools/record_fixtures.py (CATEGORIES, make_pool, POOLS), app/client/src/engine/fixtures/{categories.json,pools/main.json,pools/tight.json}; main: 3 won games/player with jokers, 4 without; tight: exactly 48, every card needed', 'The recorder (`authoring/tools/record_fixtures.py`) generates and writes, deterministically, into `app/client/src/engine/fixtures/` (plan 18, "Fixture layout"):

- `categories.json`: 2 bundles (`base` + one more, D-43), 3 broad categories, ~6 subcategories; same shape as `categories.load()` output (with `bundle`).
- `pools/main.json`: ~90 approved questions, difficulties 1–10 across all subcategories, hints 0–3 (some with 0), all fields the referee and `game.view` read (`id`, `status`, `difficulty`, `subcategory`, `description`, `question`, `answer`, `wrong_answers`, `hints`, `media`, `background`, `fun_fact`, `bundle`).
- `pools/tight.json`: barely one game: the second game hits a supply failure; Bájale, Cambiazo, purge and snipe-hit unavailable.

Check against `selection.supply` / `assign` with a throw-away call: main supports several games per player with jokers; tight supports exactly one.

Done when: the files are written, re-running gives identical bytes, and the supply checks above hold.', '2026-10-12T00:04:11Z', '2026-10-12T01:53:00Z', 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (67, 18, 'Selection fixture cases (PORT-1)', 'work', 'done', NULL, '2026-10-11, authoring/tools/record_fixtures.py (selection_cases), app/client/src/engine/fixtures/selection.json: 105 cases (in_range edges, assign subsets/shortages, supply main/tight/burns, draw keep/avoid/n/unfillable); --check passes', 'The recorder writes `app/client/src/engine/fixtures/selection.json` (plan 18, "Fixture layout"): direct calls into `app/server/selection.py`, each `{name, fn, args, tape, result}`.

- `in_range`: edges of each level range.
- `assign`: subsets of levels, shortages.
- `supply`: main pool, tight pool, tight minus burns (burns written to the temp DB first).
- `draw`: plain, with `keep`, with `avoid_categories`, `n` < 4, unfillable → `None`.

Done when: every function above has its cases with tapes, and `--check` passes.', '2026-10-12T00:04:11Z', '2026-10-12T01:55:45Z', 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (68, 18, 'Scripted game scenarios: rules and jokers (PORT-1)', 'work', 'done', NULL, '2026-10-11, authoring/tools/record_fixtures.py (8 scenarios + Recorder helpers ok/fail/state/view/correct/wrong/find; steps now carry a ''pool'' field, switched only right before ''new'', because snipe/category/skip-purge/easier need the tight pool for their unavailable cases; task 71: document it in the fixture README), app/client/src/engine/fixtures/game/{win,lose-undo,hint,skip-purge,easier,category,snipe,budget}.json; --check passes, no 500', 'Add these scenarios to `authoring/tools/record_fixtures.py`, written to `app/client/src/engine/fixtures/game/<name>.json` (plan 18, "Scenarios"): `win`, `lose-undo`, `hint`, `skip-purge`, `easier`, `category`, `snipe`, `budget`. Each case listed in the plan for these scenarios must appear, incl. one available and one unavailable case per joker, and `snipe`''s hit with no cards left on the tight pool.

Pick answers/indexes from the recorded view (the correct index is in the state), not hard-coded, so scenarios survive pool tweaks.

Done when: all 8 files are written, no step returned 500, `--check` passes.', '2026-10-12T00:04:11Z', '2026-10-12T01:58:44Z', 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (69, 18, 'Scripted game scenarios: players, admin and errors (PORT-1)', 'work', 'done', NULL, '2026-10-11, authoring/tools/record_fixtures.py (5 scenarios; Recorder.fail now asserts the DB snapshot is unchanged after every error and takes status= for get_game''s 400), app/client/src/engine/fixtures/game/{admin-skip,players,abandon,supply,errors}.json; --check passes, no 500. Notes for parts 2/3: abandon with no running game is a 200 no-op; casefold also pinned with Straße/STRASSE; a global burn outlives its deleted player''s game (dangling game_id)', 'Add these scenarios to `authoring/tools/record_fixtures.py`, written to `app/client/src/engine/fixtures/game/<name>.json` (plan 18, "Scenarios"): `admin-skip`, `players`, `abandon`, `supply`, `errors`. Each case listed in the plan for these scenarios must appear, notably: casefold «Íngrid»/«íngrid», empty and too long names, delete player with a running game, IDs after a delete (SQLite max+1), `supply` 409 report on the tight pool, every action with no running game → error, and DB unchanged after each error.

Done when: all 5 files are written, no step returned 500, `--check` passes.', '2026-10-12T00:04:12Z', '2026-10-12T02:00:25Z', 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (70, 18, 'Soak scenarios (PORT-1)', 'work', 'done', NULL, '2026-10-11, authoring/tools/record_fixtures.py (soak_walk, soak-1..10), app/client/src/engine/fixtures/game/soak-*.json; plan 18: soak db every 10th + last step, 30–40 steps (size 1.89 MB total)', 'Add ~10 seeded random walks `soak-<n>` to `authoring/tools/record_fixtures.py` (plan 18, "Scenarios"): 30–60 steps each, legal actions chosen from the current view (picks, answers, every joker incl. purge/Cambiazo/snipe, undo, admin skip incl. everyone, new games, new players). The walk''s choices come from a separate `random.Random(seed)`, not the patched shuffle, so the tape only holds referee shuffles.

Done when: the files are written, no step returned 500, the walks cover every action at least once overall, total fixture size < 2 MB, `--check` passes.', '2026-10-12T00:04:12Z', '2026-10-12T02:08:03Z', 62);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (71, 18, 'Fixture README, plan and directory updates (PORT-1)', 'work', 'done', NULL, '2026-10-11, app/client/src/engine/fixtures/README.md, plans/12-client-engine.md (PORT-1 [x]), plans/decisions.md (D-58), directory.md; final check: fresh run, --check identical, state/game.sqlite unchanged', '- `app/client/src/engine/fixtures/README.md`: file format, tape semantics (`perm`, `site`, `tapeRng` contract: fail on wrong `n`, site mismatch, leftover/missing entry), fixed `now` per step, how to re-record and check (`python3 authoring/tools/record_fixtures.py [--check]`), and plan 18''s "Notes for parts 2/3".
- `plans/12-client-engine.md`: PORT-1 `[x]` with a note; "Parity strategy" step 1 states the shuffle-tape choice.
- `plans/decisions.md`: a D-entry for the shuffle tape (no shared PRNG; the TS engine takes an injected `Rng`).
- `directory.md`: the recorder and the fixtures directory.

Final check of plan 18 "Done when": fresh run from an empty fixtures dir, `--check` byte-identical, `state/game.sqlite` mtime + checksum unchanged.

Done when: the above is written and the final check passes.', '2026-10-12T00:04:12Z', '2026-10-12T02:09:38Z', 62);
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
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (76, 20, 'Engine save state and Python helpers (PORT-3)', 'work', 'open', NULL, NULL, 'Save document types, Python-compat helpers and the transaction helpers for the TS referee. See plan 20, "Decisions taken here" and "Files".

- `app/client/src/engine/state.ts`: `SaveData {version: 1, players, games, burned}`, `PlayerRow`, `GameRow` (`state: GameState` as an object), `BurnRow` (`player_id` null = everyone), `GameState` (the `game.py` docstring fields, snake_case), `HistoryEntry`, `SAVE_VERSION = 1`, `emptySave()`, `withDefaults(state)` (like `latest()`), `nextId(rows)` (`max(id) + 1`, `1` when empty).
- `app/client/src/engine/pycompat.ts`: `casefold`, `pyLen` (code points), `pySplitJoin`, `pyRepr`, `pyTruthy`, `pyInt`, `pyStr`.
- `transact(save, fn)` (on `structuredClone`, a thrown `GameError` discards it), `trial` (savepoint: clone of the working copy, returns message or `null`), `engineData(pool, categories)` → `{pool, byId, categories, broad}`, the `Io {rng, now}` type. Put them in `state.ts` or `game.ts` as fits; `GameError {message, details}` here if `transact` needs it.
- Decision entry in `plans/decisions.md` (next D number): the client holds the correct answer and all hints; relaxes D-25/D-26; the view still hides the answer; screens render only the view. Point `plans/12-client-engine.md` "The referee question" to it.
- No `node:` imports; nothing outside `src/engine/` and `src/lib/types.ts`.

Done when: `npm run check` passes; a throw-away script asserts a few `pycompat` cases against `python3 -c` (`casefold` of `ß`/`ς`, `pyRepr` with quotes, `pyInt` of floats/bools/strings), then is deleted.', '2026-10-12T00:05:37Z', NULL, 64);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (77, 20, 'Game actions without jokers (PORT-3)', 'work', 'open', NULL, NULL, 'Port the non-joker part of `app/server/game.py` to `app/client/src/engine/game.ts`, using plan 19''s `selection.ts`/`pool.ts` and the helpers of the previous task. Follow plan 20, "Parity details", exactly.

- `cleanName`, `players` (sort by latest `started_on`, else `created_on`, descending; ties by `id`), `deletePlayer` (their games and burns go, global burns stay), `supply`, `newGame` (supply check first → `GameError` with the report; running game → `abandoned`; casefold player match), `pick`, `answer` (`before` = clone with `undo: null`; first index of the answer), `skip` (player/everyone burns, `INSERT OR IGNORE` uniqueness), `undo` (newest non-abandoned game, also won/lost; un-burns only `(last.question_id, pid, gid)`; keeps current `settings`), `abandon`, `setJokers` (plain object, known keys, `null` or int 0–99, no bools), `jokersLeft`, `view`.
- Constants `JOKERS`, `UNLIMITED`, `CARDS`, `SPENT`; error messages verbatim from Python (Spanish and English).
- Public functions are pure: `(save, data, io, …)` → `{save, …}`, input unchanged. Rng only through `io.rng` at the Python sites (`pick` shuffles `[answer, ...wrong_answers]`), time only `io.now`.
- `view` returns `jokers: null` for now (task "Jokers" fills it). Response types from `lib/types.ts`, no change to `Game`.

Done when: `npm run check` passes; a throw-away script plays a short game on `fixtures/pools/main.json` (new, pick, answer, skip, undo) with `seededRng` and prints the views; deleted afterwards. Full parity is checked by the replay task.', '2026-10-12T00:05:37Z', NULL, 64);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (78, 20, 'Jokers in the TS engine (PORT-3)', 'work', 'open', NULL, NULL, 'Add the jokers to `app/client/src/engine/game.ts`, ported from `app/server/game.py`. Follow plan 20, "Parity details" (rng sites, `jokersView` order).

- `playHint`, `playSkip`, `playEasier`, `playCategory`, `playSnipe` (index check `Number.isInteger`), `replacement` (shuffles only when the later levels fill, even an empty list), `laterFill`, `categoryCandidates`, `swapIn` (shuffles `[answer, ...wrong_answers]`), `joker` (budget, `SPENT`).
- `jokersView` with `trial`: hint, skip, easier, snipe (index = correct answer), skip+purge; then per category in `categories` order, per subcategory: current one short-circuits (no shuffle), else `replacement(…, order 0, shared fill)`. Spent jokers are tried, then overwritten with `SPENT`.
- `view` builds `jokers` only when `result` is null, phase `question` and `current` is in the pool.

Done when: `npm run check` passes; a throw-away script plays each joker once on `fixtures/pools/main.json` and prints the events; deleted afterwards.', '2026-10-12T00:05:37Z', NULL, 64);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (79, 20, 'engine/api.ts and game fixture replay (PORT-3)', 'work', 'open', NULL, NULL, 'The `main.py` game routes in TS and the replay of every recorded game scenario. See plan 20, "`engine/api.ts` mirrors `main.py`''s routes" and "Replay".

- `app/client/src/engine/api.ts`: `getGame` (200 `{game, supply}` | 400; view first, then supply), `getPlayers`, `deletePlayer` (200 | 409), `gameAction(save, data, io, action, body)` (200 `{game, event?}` | 409 `{error, supply}` | 404 `{error: "not found"}`). Coercion like `game_action`: `pyInt` for `index`, truthiness for `everyone`/`purge`, `pyStr` for the joker name; joker args only `purge`, `subcategory`, `index`.
- `app/client/src/engine/game.test.ts`: per `app/client/src/engine/fixtures/game/*.json` (scripted and soak): `emptySave()`, `engineData(fixture pool, fixture categories)`; per step `io = {rng: tapeRng(step.tape), now: step.now}`; compare `{status, body}` with `response`, `{players, games, burned}` with `db` (`burned` sorted by `(game_id, question_id, player_id)`, null first; normalize in `engine/test/save.ts`), `tape.done()`; on 409/400 the save is unchanged. Use plan 19''s `engine/test/fixtures.ts` reader.
- Mismatches are fixed in the engine; fixture gaps go back to plan 18''s recorder (re-record, never hand-edit).
- Docs: `plans/12-client-engine.md` PORT-3 `[x]` with a note; `directory.md` (engine files).
- Check that engine modules import nothing outside `src/engine/` and `src/lib/types.ts`, and nothing from `node:` (tests and `engine/test/` excepted).

Done when: plan 20''s "Done when" holds: root `npm test` passes with every step identical and every tape used up; `npm run check` and `npm run build` pass; no new dependencies; screens untouched.', '2026-10-12T00:05:37Z', NULL, 64);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (80, 3, 'create tasks for plan 3', 'split', 'done', 1000, '2026-10-11, tasks 81-85', 'Split plan 3 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:06:56Z', '2026-10-12T00:07:35Z', 3);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (81, 3, 'write plan: t() helper and the es catalog (LUI-1)', 'plan', 'done', 1000, '2026-10-11, plan 21 (tasks.sql)', 'Write the plan for part 1 of the masterplan (plan 3): `pm plan list`, then `pm plan add 3 "t() helper and the es catalog (LUI-1)" --priority 500` (client-side code), with the full body.

- Scope as in part 1: `app/client/src/lib/i18n.ts` (`t(key, params)`, `Intl.PluralRules`, `Intl.NumberFormat`, no library), `app/client/src/locales/es.ts` whose type is `Catalog`, every string of the 13 files in `app/client/src/game` plus `index.html` title, `aria-label`/`title`, joker names and key hints, `copy.ts` variant arrays (`choose()`/seed logic unchanged).
- Sound cues in `sound.svelte.ts`: neutral cue ids instead of regex on Spanish text.
- `es` by default; dev-only `?lang=xx` override for parts 3 and 4; no language menu (OQ-31).
- Check: script or documented `grep` for Spanish literals in `app/client/src/game`; before/after screen comparison, no visible change.
- Split the plan''s work by component group so each task fits one worker run; first task: helper + catalog skeleton.
- Coordinate with part 2 (server errors as codes): error keys live in the same catalog.
- Across all parts: `plans/15a-ui-translation.md` (LUI-1), `directory.md`, `plans/decisions.md` if the catalog shape is a decision.

Done when: the plan exists with priority 500 and its "create tasks" task is queued.', '2026-10-12T00:07:33Z', '2026-10-12T00:08:39Z', 80);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (82, 3, 'write plan: server errors as codes', 'plan', 'done', 1000, '2026-10-11, plan 22 (tasks.sql); priority 710 so error codes land before PORT-1 fixtures', 'Write the plan for part 2 of the masterplan (plan 3): `pm plan list`, then `pm plan add 3 "Server errors as codes" --priority 700` (backend), with the full body.

- `GameError` in `app/server/game.py` carries a stable code plus params (e.g. `{"error": "joker_spent", "joker": "hint"}`), with a readable English fallback text for logs and the authoring side.
- Wire through `app/server/main.py` → `app/client/src/lib/api.ts` → `error` in `Game.svelte`, rendered with `t()` from part 1.
- List every `GameError` raised today and its code.
- Runs before or alongside part 1 (priority 700 puts it first); if `t()` doesn''t exist yet when its client task runs, it adds the error keys to the catalog from part 1 or waits for it: say which in the plan.
- Log the code scheme in `plans/decisions.md` if it becomes a decision.

Done when: the plan exists with priority 700 and its "create tasks" task is queued.', '2026-10-12T00:07:33Z', '2026-10-12T00:10:26Z', 80);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (83, 3, 'write plan: pseudo-locale xx (LUI-2)', 'plan', 'done', 1000, '2026-10-11, plan 23 (tasks.sql)', 'Write the plan for part 3 of the masterplan (plan 3): `pm plan list`, then `pm plan add 3 "Pseudo-locale xx (LUI-2)" --priority N`, N below the part-1 plan''s (it runs after part 1; e.g. 400), with the full body.

- `xx` generated from `es` at runtime or build: ~40 % padding, accents, `{params}` intact.
- Missing keys resolved through `t()` show visibly (e.g. `⟦key⟧`); the type check covers the static side.
- Walk every screen on the TV layout with `?lang=xx`; log overflow in `plans/backlog.md`, no redesign.
- Mark LUI-2 in `plans/15a-ui-translation.md` when done.

Done when: the plan exists, ordered after part 1, and its "create tasks" task is queued.', '2026-10-12T00:07:33Z', '2026-10-12T00:11:51Z', 80);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (84, 3, 'write plan: draft en catalog (LUI-3)', 'plan', 'done', 1000, '2026-10-11, plan 24 (tasks.sql)', 'Write the plan for part 4 of the masterplan (plan 3): `pm plan list`, then `pm plan add 3 "Draft en catalog (LUI-3)" --priority N`, N below the part-1 plan''s (it runs after part 1; e.g. 400), with the full body.

- `app/client/src/locales/en.ts` satisfies `Catalog`; Claude drafts it.
- Joker names: playful English, not literal (15a); the plan names a task that proposes a short list of candidates per joker and raises a pm decision for the gamemaster to pick.
- Draft only: no native-speaker check, no launch (LUI-5, OQ-31).
- Mark LUI-3 in `plans/15a-ui-translation.md` when done.

Done when: the plan exists, ordered after part 1, and its "create tasks" task is queued.', '2026-10-12T00:07:33Z', '2026-10-12T00:12:47Z', 80);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (85, 3, 'write plan: gamemaster check of the colombia proposals (D-39)', 'plan', 'done', 1000, '2026-10-11, plan 25 (tasks.sql)', 'Write the plan for part 5 of the masterplan (plan 3): `pm plan list`, then `pm plan add 3 "Gamemaster check of the colombia proposals (D-39)" --priority 200` (content; no code depends on it), with the full body.

- Human work: the gamemaster reviews the 84 BN-3 proposals (`work/bundles/proposals.json`) at `/review?bundle=colombia` (key `n` moves a question to the next bundle).
- Agent side: one task raises a pm decision that asks for the check and waits on it; after the answer, note the result in `plans/22-bundles.md` (BN-3) and `plans/project.md`, run `qgen validate` and `qgen export`.
- "Every question has `bundle`" is already enforced by `validate_pool()` in `authoring/tools/qgen.py`: confirm, don''t rebuild.

Done when: the plan exists with its priority and its "create tasks" task is queued.', '2026-10-12T00:07:33Z', '2026-10-12T00:13:21Z', 80);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (86, 21, 'create tasks for plan 21', 'split', 'done', 1000, '2026-10-11, tasks.sql: tasks 91–97 for plan 21, decision 6 (task 97 waits)', 'Split plan 21 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:08:37Z', '2026-10-12T00:14:32Z', 81);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (87, 22, 'create tasks for plan 22', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 98, 99)', 'Split plan 22 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:10:24Z', '2026-10-12T00:15:01Z', 82);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (88, 23, 'create tasks for plan 23', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 100, 101; 101 waits on decision 6)', 'Split plan 23 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:11:32Z', '2026-10-12T00:15:30Z', 83);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (89, 24, 'create tasks for plan 24', 'split', 'done', 1000, '2026-10-11, tasks.sql: tasks 102–104 for plan 24; joker-name decisions are created by task 102', 'Split plan 24 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:12:45Z', '2026-10-12T00:16:08Z', 84);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (90, 25, 'create tasks for plan 25', 'split', 'done', 1000, '2026-10-11, tasks.sql: task 105, decision 7', 'Split plan 25 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:13:19Z', '2026-10-12T00:16:31Z', 85);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (91, 21, 'LUI-1: i18n helper, es catalog skeleton, copy.* lines', 'work', 'open', NULL, NULL, 'Lay the groundwork of plan 21: the `t()` helper, the typed `es` catalog, and the milestone/consolation lines moved into it. Design: plan 21 «Design».

- New `app/client/src/lib/i18n.ts` (no library): `t(key, params?)` with `{name}` placeholders, plural maps picked by `params.n` (`Intl.PluralRules`), numbers via `Intl.NumberFormat(lang)`, `variants(key)` for `string[]` entries, missing key → `⟦key⟧`.
- `lang`: `"es"` default; `?lang=` override only when `import.meta.env.DEV` (unknown lang → `es`; `xx`/`en` come in plans 23/24). At startup (`main.ts` or `App.svelte`): `document.documentElement.lang`, `document.title` from `app.title`; `index.html` keeps `<title>Trivia</title>`.
- New `app/client/src/locales/es.ts`: nested object, `as const`-style; `export type Catalog` (string leaves widened, variant arrays as `string[]`), `Key` = union of dotted leaf paths. Namespaces from the plan; `error` reserved for plan 22 (leave it out or empty; if plan 22 task 1 already added `lib/errors.ts`, don''t touch it).
- `game/copy.ts`: `MILESTONES`/`CONSOLATION` texts → `copy.milestone.<level>`, `copy.consolation.<maxLevel>` read with `variants()`; `choose()`, seeds, level brackets and `milestone()`/`consolation()` signatures unchanged. `{n}` filled through `t`-style substitution (same output: plain `String(level)` for 1–12).
- `plans/decisions.md`: next free D-number, catalog shape (typed nested object, dotted keys, `Key` union, `⟦key⟧`, plurals/variants, dev-only `?lang`). `directory.md`: `lib/i18n.ts`, `locales/`.

Done when:
- `npm run check`, `npm run build` pass; `t("typo")` fails the check (try it, then remove).
- Throw-away script: for every level 1–12 and seeds 0–5, old `milestone()`/`consolation()` (from `git show HEAD:…`) and new return the same string.', '2026-10-12T00:14:29Z', NULL, 86);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (92, 21, 'LUI-1: sound cues to neutral ids', 'work', 'open', NULL, NULL, '`sfx()` stops matching Spanish descriptions by regex; it takes a typed cue id. Plan 21 «Design», sound cues.

- `app/client/src/game/sound.svelte.ts`: `type Cue` = union of neutral ids (`"applause"`, `"applause-big"`, `"sad-trombone"`, `"padlock-close"`, `"menu-open"`, `"joker-armed"`, …, one per distinct sound today); `SAMPLE_FOR`, `RECIPES` become lookups by cue id. Level thud: typed level argument (`sfx("block", { level })` or `` `block-${n}` ``). Sample file names in `public/audio/` stay.
- Every call site (`grep -rn "sfx(" app/client/src`; today ~30 in `Game.svelte`, `Question.svelte`, `Shredder.svelte`, `Fireworks.svelte`) switches to cue ids.
- Comments may keep the Spanish name in «…».

Done when:
- `npm run check`, `npm run build` pass; no Spanish string left in `sound.svelte.ts` outside comments.
- Same sound per call site as before: throw-away script resolving each old call''s string through the old regex table and each new cue through the new table, or a side-by-side list (call site, old string, cue, sample/recipe) in the task note.', '2026-10-12T00:14:29Z', NULL, 86);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (93, 21, 'LUI-1: joker texts and keys into the catalog', 'work', 'open', NULL, NULL, 'Joker names, key hints and aria texts come from `joker.<id>.*`. Plan 21 «Design», jokers.

- `JokerTray.svelte` (names, key hints, aria), `JokerFlight.svelte`, `CategoryPicker.svelte`, `DifficultyDial.svelte`, `Shredder.svelte`: every on-screen string and `aria-label`/`title` via `t()`.
- `joker.<id>.key` holds today''s keys (`S`, `P`, `F`, `T`, `X`); key handling in `Question.svelte` reads them from the catalog (case handling as today).
- Joker «why not» reasons come from the server (plan 22 renders them via `lib/errors.ts`); leave that path alone.

Done when:
- `npm run check`, `npm run build` pass; no Spanish literal left in these five files outside comments.
- Throw-away check: every literal removed (from `git diff`) appears verbatim as a catalog value; each joker key still plays its joker.', '2026-10-12T00:14:29Z', NULL, 86);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (94, 21, 'LUI-1: Question.svelte texts into the catalog', 'work', 'open', NULL, NULL, 'All remaining text of `app/client/src/game/Question.svelte` comes from the catalog (`screen.question.*`, `a11y.*`).

- Hints («Soplo {n}», plurals via `{ one, other }` if the text varies with `n`), «Respuesta final», buttons, aria-labels, titles.
- Error display: leave plan 22''s `errorText`/reason rendering as is.

Done when:
- `npm run check`, `npm run build` pass; no Spanish literal in `Question.svelte` outside comments.
- Throw-away check: every removed literal appears verbatim as a catalog value; parametrised texts give the same output for the values the game uses.', '2026-10-12T00:14:29Z', NULL, 86);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (95, 21, 'LUI-1: Game.svelte and Player.svelte texts into the catalog', 'work', 'open', NULL, NULL, 'Screen texts of `Game.svelte` and `Player.svelte` come from the catalog (`screen.start`, `screen.player`, `screen.level`, `screen.select`, `screen.result`, `screen.victory`, `a11y.*`).

- Greeting, start/level/result/victory texts, buttons, aria/title. Milestone/consolation already go through `copy.ts` (task 1).
- Leftovers in `Stage.svelte`, `swap.ts`, `timing.ts`, `Hud.svelte`, `Tower.svelte`, `Placeholder.svelte`, `Icon.svelte`, `App.svelte` if any are on-screen strings (`PLACEHOLDER(<task ID>)` labels: into the catalog too, `placeholder.*`).
- Server error display: plan 22''s `errorText`; leave it.

Done when:
- `npm run check`, `npm run build` pass; no Spanish literal in these files outside comments.
- Throw-away check: every removed literal appears verbatim as a catalog value.', '2026-10-12T00:14:29Z', NULL, 86);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (96, 21, 'LUI-1: Overlay texts and the check:literals script', 'work', 'open', NULL, NULL, 'The admin overlay moves into the catalog, and a kept script guards against new literals.

- `Overlay.svelte`: all texts, aria/title → `overlay.*`.
- New `app/client/scripts/check-literals.mjs`, `npm run check:literals -w app/client`: strips `//`, `/* */`, `<!-- -->` comments; flags Spanish characters (`áéíóúñÁÉÍÓÚÑ¡¿`), text between tags, and `aria-label`/`title`/`placeholder` values that aren''t a `{…}` expression. Exit 1 with `file:line`. Paths as arguments, default `src/game` (plan 22 task 2 adds `src/lib/errors.ts`). No dependencies.
- Document it in `README.md` and the AGENTS.md command list.

Done when:
- `npm run check`, `npm run build`, `npm run check:literals -w app/client` pass.
- The script fails on a planted literal (try, then remove).', '2026-10-12T00:14:29Z', NULL, 86);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (97, 21, 'LUI-1: before/after comparison and close-out', 'work', 'open', NULL, NULL, 'Show that plan 21 changed nothing visible in Spanish, then close LUI-1.

- Comparison per decision (see `pm show`): screens start, player, level, select, question incl. every joker, result, victory, overlay; "before" from the commit before plan 21''s first task (`git log --grep "LUI-1: i18n helper"`, its parent; a `git worktree`, removed afterwards).
- Any difference: fix it here if small, else a task in plan 21.
- Mark LUI-1 `[x]` in `plans/15a-ui-translation.md`; `plans/project.md` (M3: part 1 done).

Done when: the comparison shows no difference; plans updated; temp files and worktree gone.', '2026-10-12T00:14:30Z', NULL, 86);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (98, 22, 'Server errors as codes: server + client wiring, interim Spanish map', 'work', 'done', NULL, '2026-10-11, app/server/game.py, app/server/main.py, app/client/src/lib/{api,types,errors}.ts, Game/JokerTray/Question/Player.svelte, D-57, plans/12-client-engine.md, directory.md; 28 codes checked over HTTP, Spanish word for word; no PORT-1 fixtures yet; ErrorInfo.params is Record<string, unknown> (supply_short carries a list)', 'Part 2 of M3, task 1 of plan 22 (see the plan for the design and the full code table). Runs at 710, before PORT-1''s fixture tasks (700), so fixtures record codes.

- `app/server/game.py`:
  - `GameError(code, params=None, details=None)`; `ERRORS = {code: English template}`; `str(e)` = filled English text; assert unknown code in `__init__`.
  - Every `raise GameError` → its code from the plan''s table; re-grep and add any raise not in the table.
  - Re-raises keep their own code (`back_to_select`, `play_snipe`): `raise GameError("…") from None`.
  - `trial()` returns `{"code", "params"}` or None; `jokers_view` reasons become that object (Cambiazo literal → `category_none`, `SPENT` → `joker_spent` with `{joker}`); drop `SPENT`.
- `app/server/main.py`: `GET /api/game` (400), `game_action` (409), `/api/players/delete` (409) answer `{"error": code, "params": {...}, "message": english, "supply": details}`; 404 → `not_found`, 500 → `server_error` (English message). `/api/flags` unchanged.
- Client:
  - `lib/types.ts`: `ErrorInfo = { code: string; params: Record<string, string | number> }`, joker `reason: ErrorInfo | null`.
  - `lib/api.ts`: `GameError` with `code`, `params`, `message`; `json()`, `playJoker`, `gameAction` throw it when the body has `error`; network failures and bodies without `error` stay plain `Error`.
  - New `lib/errors.ts`: `errorText(e)`, `reasonText(info)`, interim Spanish map for player-facing codes only (texts moved verbatim; `joker_spent` per joker id; `supply_short` joins `supply_level` items with ", "). Unknown code or plain Error → its message.
  - `Game.svelte` (every `error = …`), `JokerTray.svelte` (reason), `Question.svelte` (purge reason), `Player.svelte` (delete errors, if shown).
- Docs: new D-number in `plans/decisions.md` (codes + params on the wire, English `message` for logs, client renders); `directory.md`: `lib/errors.ts`; mark the internal codes in the plan''s table if anything changed.
- PORT-1: if fixtures exist, re-run `authoring/tools/record_fixtures.py` and commit them; note in `plans/12-client-engine.md` that PORT-3 throws the same codes and parity compares `error`/`params`, not `message`.

Done when:
- Throw-away script hits every code over HTTP against a temp `TRIVIA_STATE`, prints code, params, message and the client''s Spanish text next to the old text; they match word for word. Delete the script after.
- `npm run check`, `npm run build` pass; `trivia` starts; no visible change in Spanish; no new dependencies.', '2026-10-12T00:15:00Z', '2026-10-12T01:43:42Z', 87);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (99, 22, 'Server error texts into the es catalog', 'work', 'open', 490, NULL, 'Task 2 of plan 22. Priority 490: runs after plan 21''s tasks (LUI-1, 500), which create `app/client/src/lib/i18n.ts`, `locales/es.ts` and `check:literals`, and reserve the `error` namespace. If they don''t exist yet, stop and say so.

- `es.ts`: `error.<code>` keys for every player-facing code from `lib/errors.ts`, incl. `error.joker_spent.<id>` per joker and `error.supply_level`; texts verbatim.
- `lib/errors.ts`: drop the interim Spanish map; `errorText`/`reasonText` call `t()`. A code is player-facing iff its key exists in the catalog (typed lookup, no `⟦key⟧` for internal codes, which keep the English `message`).
- `check:literals` passes with `lib/errors.ts` included.
- Close-out: `plans/project.md` (M3: part 2 done); mark the plan file''s tasks done.

Done when: `npm run check`, `npm run build` and `check:literals` pass; `trivia` starts; same corner error lines and joker reasons in Spanish as before (spot-check `name_missing`, `joker_spent`, `supply_short`, a Cambiazo reason, and an internal code showing English).', '2026-10-12T00:15:00Z', NULL, 87);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (100, 23, 'pseudo-locale xx: generator and dev wiring', 'work', 'open', NULL, NULL, 'Part 1 of plan 23 (LUI-2). Precondition: `app/client/src/lib/i18n.ts`, `app/client/src/locales/es.ts` and the `?lang=` dev override from plan 21 exist. If they don''t, drop this task with a note (`pm task drop`) instead of building them here.

- `app/client/src/locales/xx.ts` (new): `pseudo(es): Catalog`, generated at runtime from `es`, no hand-written catalog.
  - Walks every leaf: plain strings, plural maps (`{ one, other, … }`), variant arrays (`copy.*`); same shape, so it satisfies `Catalog`.
  - ASCII letters → look-alikes (`a→å`, `e→é`, `o→ø`, `c→ç`, `n→ñ`, `A→Å`, …).
  - ~40 % extra length (rounded up, min. 2 chars) as `~` runs, inside `[` … `]`.
  - `{param}` placeholders stay byte-for-byte; only text outside `{…}` changes.
  - Small exempt list in `xx.ts`: single-letter joker keys (`joker.<id>.key`), left unchanged.
- `app/client/src/lib/i18n.ts`: picks `xx` only when `import.meta.env.DEV && ?lang=xx`, via dynamic `import()`. `document.documentElement.lang` stays `es` for `xx`.
- Missing keys: keep plan 21''s `⟦key⟧`; add a dev-only `console.warn` once per missing key.
- `directory.md`: add `app/client/src/locales/xx.ts`.

Verify with a throw-away script (delete it afterwards) that runs `pseudo()` over `es`: every leaf changed (except exempt), `{params}` unchanged, length ≥ 1.4× (except exempt), shape equal.

Done when: `npm run check` and `npm run build` pass; no `xx`/`pseudo` code in `app/client/dist/` (grep the build); `es` output unchanged.', '2026-10-12T00:15:27Z', NULL, 88);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (101, 23, 'pseudo-locale xx: screen walk, missed literals, overflow rows', 'work', 'open', NULL, NULL, 'Part 2 of plan 23 (LUI-2). Needs task "pseudo-locale xx: generator and dev wiring" done, and the screenshot method from plan 21 (decision 6).

- Run `npm run dev -w app/client` + `trivia`, open with `?lang=xx`, TV layout 1920 × 1080 (`theme.css`). Screens: start, player, level, select (every joker tray state incl. reasons), question (every joker armed and used, hints, final answer), result, victory, overlay, error line in the corner.
- Also one tight case: the narrowest supported window (height bound in `theme.css`).
- Screenshots: the same method plan 21 uses for its before/after comparison (decision 6); no new dependency in the flake or `package.json`.
- Expected to stay Spanish (not bugs): question/answer text, category/subcategory names, bundle names, English `message` fallbacks of internal error codes (plan 22).
- Any other plain Spanish under `xx` is a literal LUI-1 missed: move it into `es.ts` and use `t()`, list it in the task note.
- Each overflow/clipping: one row in `plans/backlog.md` (`B-n`, origin `LUI-2`, status `new`): screen, element, key, what breaks. No CSS changes, no redesign.
- Mark LUI-2 `[x]` in `plans/15a-ui-translation.md` with a note (date, backlog rows, or "no overflow found"); update M3 status in `plans/project.md`.

Done when: every screen above checked under `xx`; `npm run check` and `npm run build` pass; `es` output unchanged; screenshots and scripts not committed.', '2026-10-12T00:15:27Z', NULL, 88);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (102, 24, 'LUI-3: English joker name candidates and decisions', 'work', 'open', NULL, NULL, 'Task 1 of plan 24. Needs plan 21 (LUI-1: `app/client/src/lib/i18n.ts`, `locales/es.ts`, `Catalog`/`Key` types) and plan 22 task 2 (`error.<code>` keys in `es.ts`). If they don''t exist yet, stop and say so (`pm task drop` with a note); don''t build them here.

- Per joker (`hint` «Soplo», `skip` «Paso», `easier` «Bájale», `category` «Cambiazo», `snipe` «Francotirador»): 3–5 playful English candidates, not literal translations, ≤ 13 characters (length of «Francotirador», tray width); each with a one-line reason (pun, tone, what it evokes). Recommended one first.
- One `pm decision add` per joker: subject e.g. "English name for the hint joker «Soplo»?", candidates as `--option`s (recommended first), body: Spanish name, what the joker does (from the catalog/joker code), why these candidates.
- Link the plan''s task "LUI-3: chosen joker names into en.ts" (task 3 of plan 24; id via `pm show <this task>`) to all five decisions with `pm task-pending-decision`.
- `plans/15a-ui-translation.md` under LUI-3: candidate lists as bullets (recommended first, decision id per joker).

Done when: five pending decisions exist, task 3 waits on all five, 15a lists the candidates.', '2026-10-12T00:16:05Z', NULL, 89);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (103, 24, 'LUI-3: draft en.ts catalog and ?lang=en dev override', 'work', 'open', NULL, NULL, 'Task 2 of plan 24. Doesn''t wait for the joker-name decisions: joker names use the recommended candidates from task 1 (in `plans/15a-ui-translation.md`, LUI-3) for now. Needs plan 21 (LUI-1) and plan 22 task 2 done; if not, stop and say so.

- `app/client/src/locales/en.ts`: `export const en = { … } satisfies Catalog`; every key of `es`, own English wording.
  - Plural maps `one`/`other`; same `{param}` set per leaf as `es`.
  - Variant arrays (`copy.milestone.*`, `copy.consolation.*`): own English lines in the game''s tone (family, warm, a bit cheeky); count may differ.
  - `joker.<id>.key`: same letters as `es` (`S`, `P`, `F`, `T`, `X`), one-line comment: keys per language are LUI-4.
  - Errors: only player-facing codes (keys present in `es`).
- `lib/i18n.ts`: `en` when `import.meta.env.DEV && ?lang=en`, via dynamic `import()` (same mechanism as `xx` from plan 23, if it exists); `document.documentElement.lang = "en"`. Production stays `es` only: `npm run build` shows no `en` strings in the main chunk.
- Throw-away check script (not kept): every leaf non-empty, same `{param}` set as `es`, no `áéíóúñÁÉÍÓÚÑ¡¿«»`, no `⟦` in rendered output.
- Screen walk: `npm run dev -w app/client` + `trivia`, `?lang=en`, 1920 × 1080: start, player, level, select (joker reasons), question (every joker armed and used, hints, final answer), result, victory, overlay, error line. Same screenshot method as plans 21/23. Fix wording that reads off; overflow → `plans/backlog.md` rows (origin `LUI-3`), no CSS changes.
- Expected Spanish under `en` (not bugs): questions, answers, hints, category/subcategory/bundle names, `/comodines`, `authoring/`.
- `directory.md`: `locales/en.ts`.

Done when: `npm run check` and `npm run build` pass; `es` output unchanged; no new dependencies; the screen walk shows no `⟦…⟧`.', '2026-10-12T00:16:05Z', NULL, 89);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (104, 24, 'LUI-3: chosen joker names into en.ts', 'work', 'open', NULL, NULL, 'Task 3 of plan 24. Waits for the five joker-name decisions from task 1 (`pm show` lists them with answers). If it isn''t linked to five answered decisions, or `locales/en.ts` doesn''t exist yet (task 2), stop and say so.

- `app/client/src/locales/en.ts`: chosen names in `joker.<id>.name`, aria/hint/reason texts and any copy lines that name a joker. Keys (`joker.<id>.key`) stay as in `es`.
- `plans/15a-ui-translation.md`: LUI-3 `[x]` with a note (date, chosen names, "draft, no native-speaker check").
- `plans/decisions.md`: the chosen English joker names (next free D-number).
- `plans/project.md`: M3 status (part 4 done).

Done when: `npm run check` and `npm run build` pass; `es` output unchanged; quick `?lang=en` look at select and question screens shows the new names without overflow (overflow → `plans/backlog.md`, origin `LUI-3`).', '2026-10-12T00:16:05Z', NULL, 89);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (105, 25, 'record the gamemaster''s check of the colombia proposals (D-39)', 'work', 'open', NULL, NULL, 'Waits on the decision "Have you checked the colombia proposals at /review?bundle=colombia?" (created by task 90, linked to this task). Do nothing before it is answered.

After the answer:
- Count the 84 `colombia` proposals in `work/bundles/proposals.json`: still `colombia` vs. moved to `base` in `authoring/data/questions.json`. If the answer lists ids to move instead, move them with the review server''s bundle API (`trivia-authoring`) or tell the gamemaster; never edit the pool by hand (AGENTS.md).
- `qgen validate` (also confirms every question has `bundle`). A moved question whose subcategory isn''t in `base` (D-49): log it in `plans/backlog.md` or `plans/open-questions.md`, leave the fix to the gamemaster.
- `qgen export` so `app/data/pool.json` is current.
- `plans/22-bundles.md`: BN-3 line gets date and kept/moved counts.
- `plans/project.md`: M3 line "Gamemaster checks the 84 `colombia` proposals" → `[x]`; bundle counts under State (Bundles line).

Done when: notes in `22-bundles.md` and `project.md`; `qgen validate` passes; `app/data/pool.json` fresh.', '2026-10-12T00:16:29Z', NULL, 90);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (106, 4, 'create tasks for plan 4', 'split', 'done', 1000, '2026-10-11, tasks 107-109, decision 8', 'Split plan 4 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:17:15Z', '2026-10-12T00:17:49Z', 4);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (107, 4, 'write plan: Licence data in the pool (PUB-2)', 'plan', 'done', 1000, '2026-10-11, pm plan 26, plans/23-media-providers.md', 'Write the plan for part 1 of the masterplan (plan 4): `pm plan add 4 "Licence data in the pool" --priority 900`.

- Takes over MP-8 of `plans/23-media-providers.md`; mark MP-8 there as moved to this plan.
- Cover: the slot fields (`provider`, `license`, `license_url`, `author`, `author_url`, `restrictions`, PD reason), `media.pick_fields`, the extra Commons extmetadata in `providers/commons.py`, what the other providers fill, the one-time migration (stored candidate, else live Commons lookup by `source_url`), `qgen validate` (warning before migration, error after for approved questions), and which fields `qgen export` passes to `app/data/pool.json` (decide in the plan; credits screen PUB-5 out of scope).
- Files to read first: `authoring/tools/media.py`, `authoring/tools/providers/`, the validate/export code of `qgen`, `plans/17-publishing.md`, `plans/23-media-providers.md`.', '2026-10-12T00:17:47Z', '2026-10-12T00:19:30Z', 106);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (108, 4, 'write plan: Audit report media.py licenses (PUB-1)', 'plan', 'open', 1000, NULL, 'Write the plan for part 2 of the masterplan (plan 4): `pm plan add 4 "Audit report media.py licenses" --priority 700`.

- Depends on part 1''s pool fields; no network at report time.
- Cover: per-file rows (licence, `providers.licence_kind` family, PD reason, restrictions, question ids, status), the ok/replace classification (PD-US only, GFDL and anything off the MP allowlist, flagged restrictions per the linked decision, missing data), the replacement list (empty = milestone done) and a tally like the one in `plans/17-publishing.md`.
- Expose the classification as a function the review tool (part 3) and `qgen validate` can reuse.', '2026-10-12T00:17:47Z', NULL, 106);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (109, 4, 'write plan: Replace problem files in the review tool (PUB-3)', 'plan', 'open', 1000, NULL, 'Write the plan for part 3 of the masterplan (plan 4): `pm plan add 4 "Replace problem licence files in the review tool" --priority 400`.

- After parts 1 and 2; uses part 2''s classification function.
- Cover: a review filter for questions with media on the replacement list (e.g. `/review?licence=replace`), the reason next to the slot, replacement via the existing candidate list and search modal over all providers (`authoring/server/`, `authoring/ui/`); the new pick gets part 1''s fields via `pick_fields`.
- Gamemaster picks only: no LLM pick, no automatic swap.
- The human pass through the list until `media.py licenses` reports nothing, then `trivia-media sync --status approved --prune`; a task for the human or a note in the plan.
- Optional `qgen validate` gate against files on the replacement list.
- If flagged files can be kept per the linked decision: how the gamemaster marks one as checked and where that is stored.', '2026-10-12T00:17:48Z', NULL, 106);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (110, 26, 'create tasks for plan 26', 'split', 'done', 1000, '2026-10-11, tasks.sql: tasks 111-113, no decisions needed', 'Split plan 26 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:19:16Z', '2026-10-12T00:20:09Z', 107);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (111, 26, 'Providers: author_url, restrictions and pd_reasons', 'work', 'done', NULL, '2026-10-11, authoring/tools/providers/{__init__,commons,openverse,freesound,nasa}.py, plans/23-media-providers.md; Commons pd_reasons drops transcluded helper templates (subpages, layout, -text, -category, PD-generic, -X) and case-duplicates', 'Part 1 of plan 26 ("Providers" section). Candidates from every provider carry `author_url` and `restrictions`; new `providers.pd_reasons(candidate)` returns the public-domain reasons at pick time.

- `authoring/tools/providers/commons.py`: search `extmetadatafilter` adds `Restrictions|License|UsageTerms|AttributionRequired|Copyrighted`; `restrictions` = extmetadata `Restrictions` split on `|` (`[]` when empty); `author_url` = first `href` in the `Artist` HTML before `plain()`, protocol-relative → `https:`. `pd_reasons(candidate)`: one `api(titles=…, prop="templates", tlnamespace=10, tllimit="max")`, keep `PD-*` names, strip `Template:`.
- `openverse.py`: `author_url` from `creator_url`, `restrictions: []`, `pd_reasons`: `["PDM"]` for `pdm`, else `[]`.
- `freesound.py`: `author_url` = `https://freesound.org/people/<username>/`, `restrictions: []`.
- `nasa.py`: `author_url: None`, `restrictions: []`, `pd_reasons` → `["PD-USGov-NASA"]`.
- `providers/__init__.py`: `pd_reasons(candidate)` dispatches to the provider (only meaningful when `licence_kind` is `public-domain`; `[]` otherwise); update the candidate field list in the docstring.
- `plans/23-media-providers.md` "Data": add the new candidate fields.

Not here: writing the fields into the pool (next task).

Done when: a throw-away script searches each provider once and shows `author_url`/`restrictions` on the candidates, and `pd_reasons` returns e.g. `PD-old-70` for a known PD Commons file.', '2026-10-12T00:20:05Z', '2026-10-12T01:17:26Z', 110);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (112, 26, 'pick_fields writes the licence fields; clearing clears them; validate warns', 'work', 'done', NULL, '2026-10-11, authoring/tools/{media.py,qgen.py,providers/__init__.py,providers/commons.py}, plans/02-question-pool.md: providers.licence_fields + commons.lookup (one call for PD templates and missing author_url/restrictions); media.pick_fields writes them, media.unpicked clears; validate warns in one line (1152 approved picks unmigrated)', 'Part 2 of plan 26 ("Slot fields", "`media.pick_fields`", "`qgen validate`" sections). Depends on the providers task.

- `authoring/tools/media.py` `pick_fields`: writes `provider`, `license`, `license_url`, `author`, `author_url`, `restrictions`, `pd_reasons` for `media` and `background` slots. `pd_reasons` via `providers.pd_reasons` only for `public-domain` licences, else `[]`. Commons candidates stored before plan 26 (no `author_url`/`restrictions`): fetch them in the same titles query as the templates (one call per pick); other providers: `None` / `[]`. `credit`, `credit_of` unchanged.
- Both pick paths go through it: `authoring/server/main.py` `pick_media` → `media.download`, and `qgen.py` review (~1532); check nothing bypasses it.
- Clearing a pick (`qgen.py` ~855, ~987, and any server path that clears) removes the new fields too; unpicked slots keep them absent.
- `validate_pool`: for picked slots of approved questions check keys present, `provider` known, `license` non-null and on the allowlist (`providers.licence_kind`), `restrictions`/`pd_reasons` lists. **Warnings** for now, as one summary line (count + first few ids). Non-approved questions not checked.
- `qgen export` unchanged (decided in the plan).

Done when: a pick in the review tool and one via `qgen review` (or a throw-away script calling the same paths) store all fields, incl. `pd_reasons` for a PD Commons file; clearing removes them; `qgen validate` passes with one warning line about the unmigrated picks.', '2026-10-12T00:20:06Z', '2026-10-12T01:19:17Z', 110);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (113, 26, 'Migrate licence data of existing picks; validate errors', 'work', 'done', NULL, '2026-10-11, authoring/data/questions.json, app/data/pool.json, plans/17-publishing.md: migration, validate errors and plan marks were already in ef824b4 (1,202 picks migrated). This run: q-0021 (GFDL 1.2 only) set to needs_work per decision 10 (problems: media); qgen validate passes with licence checks as errors.', 'Part 3 of plan 26 ("Migration" section). Depends on the two tasks before. One change: write the one-time command, run it, switch validate to errors, delete the command.

- `qgen migrate-licences [--dry-run]` over all statuses and bundles in `authoring/data/questions.json`:
  - Commons picks: title from `source_url` (`File:…`, URL-unquoted), batched 50 per `api()` call: extmetadata (`Artist`, `LicenseShortName`, `LicenseUrl`, `Restrictions`, …) + templates → all slot fields, same mapping as the providers/`pick_fields` code (reuse it).
  - Other providers (2 Freesound, 2 Openverse): from the stored candidate matching `source_url` (`load_candidates`), else the live page where cheap (Freesound sound id), else leave out and list.
  - Skips slots that already have `provider`; doesn''t touch `credit`, `file_url`, the cache. A licence failing the allowlist is written as found.
  - Prints a tally (per provider, licence family, PD reasons, restrictions) and the unfilled picks.
- Run `--dry-run`, check the tally, then run for real. Fix unfilled approved picks by hand only if trivially possible; otherwise report them in the done note.
- `validate_pool`: licence checks become **errors** (no flag).
- Delete the migration command again.
- Mark MP-8 in `plans/23-media-providers.md`, PUB-2 in `plans/17-publishing.md` and `plans/project.md` done; `qgen export` stays unchanged.

Done when: `qgen validate` passes on the pool with the licence checks as errors; the tally is in the done note.', '2026-10-12T00:20:06Z', '2026-10-12T02:36:18Z', 110);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (114, 5, 'create tasks for plan 5', 'split', 'done', 1000, '2026-10-11, tasks 115-118; no decisions needed yet (window approval and play-test confirmation are raised by the part plans)', 'Split plan 5 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:21:49Z', '2026-10-12T00:22:32Z', 5);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (115, 5, 'write plan: Group windows and bundle filter in the engine (AG-7, BN-6)', 'plan', 'done', 1000, '2026-10-11, plan 27 (tasks.sql)', 'Write the plan for part 1 of the masterplan (plan 5): `pm plan add 5 "Group windows and bundle filter in the engine" --priority 590` (after plan 20 at 600, before M2''s screens part at 500).

- Builds on plans 19 (`engine/selection.ts`, `pool.ts`) and 20 (`engine/game.ts`, `state.ts`, `engine/api.ts`); no change to the Python referee. Read those plans first; if their files don''t exist yet, the plan names the functions it changes as plans 19/20 define them.
- Cover: `levels` (12 ranges) per group in `app/data/age-groups.json`, `young_teens` = today''s `LEVEL_RANGES` exactly, a first mapping of the same D-22 shape for `kids`, `young_adults`, `adults`; the engine reads the ranges instead of a constant.
- `GameState.settings`: `age_group`, `bundles` (`base` always in); `withDefaults` → `young_teens`, every bundle on; old saves and plan 18''s fixtures replay unchanged.
- `available` / `draw` / `assign` / `supply` and every joker replacement follow the game''s group and bundles; burns stay per player (D-28).
- Cambiazo picker (`jokersView`) only offers categories of active bundles.
- API: `newGame` takes and validates `age_group` and `bundles`; `supply` for a given group and bundle set (for part 2''s start screen).
- Checks: fixture replay with defaults; per group every level 4 cards in range; with `colombia` off no `colombia` question and no `colombia` category in Cambiazo.
- A decision entry in `plans/decisions.md`: settings per game, defaults, `base` always on.', '2026-10-12T00:22:30Z', '2026-10-12T00:25:12Z', 114);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (116, 5, 'write plan: Tune the age-group windows and level weights (AG-7)', 'plan', 'done', 1000, '2026-10-11, plan 28 (tasks.sql)', 'Write the plan for part 3 of the masterplan (plan 5): `pm plan add 5 "Tune the age-group windows and level weights" --priority 580` (after part 1''s plan at 590, before part 2''s UI at 400).

- Needs part 1''s per-group `levels` in `app/data/age-groups.json` and the engine''s `supply`.
- Cover: a throw-away `node` script on the engine over `app/data/pool.json`, per group and bundle set (`base`, `base`+`colombia`): candidates per level, missing slots, games until the pool runs dry for one player.
- Compare with plan 21''s long-term distribution proposal (`plans/21-age-groups.md`) and the scale''s anchors (1 = 6-year-old … 15 = specialists).
- Adjust windows and level ranges; store per-group `level_weights` derived from the ranges as D-31 did for young teens; consumers outside the game out of scope.
- A task that raises a decision for the gamemaster with the measured table to approve the final windows; after it: plan 21 drops "draft", `about` in `age-groups.json`, a decision entry.
- Thin top of the scale (14–15) reported, not fixed (milestone 1''s work).', '2026-10-12T00:22:30Z', '2026-10-12T00:26:28Z', 114);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (117, 5, 'write plan: Age group and bundle choice on the start screen', 'plan', 'done', 1000, '2026-10-11, plan 29 (tasks.sql)', 'Write the plan for part 2 of the masterplan (plan 5): `pm plan add 5 "Age group and bundle choice on the start screen" --priority 400`. Check `pm plan list` for M2''s screens part (plan 19/20''s successors, ~500) and stay below it.

- Uses part 1''s API (`newGame` with `age_group`, `bundles`; `supply` per choice); the screen shows part 3''s tuned windows.
- Cover: after the player, before the first level: four group tiles (name, ages from `age-groups.json`), one toggle per bundle (`name`, `description` from `bundles.json`; `base` on and locked).
- Preset: the player''s last game''s choice, else the defaults; Enter goes straight through as today.
- A choice that can''t fill 12 levels is marked and can''t start (today''s supply-failure message style).
- IN-1: every choice clickable and on the keyboard; the plan settles the keys; `<kbd>` hints.
- Where the running game''s group and bundles show (HUD or admin overlay); undo and abandon keep them.
- Texts through `t()` if milestone 3''s plan 21 has landed, else literals marked for it.', '2026-10-12T00:22:30Z', '2026-10-12T00:28:07Z', 114);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (118, 5, 'write plan: Play-test and close-out of age groups and bundles', 'plan', 'done', 1000, '2026-10-11, plan 30 (tasks.sql)', 'Write the plan for part 4 of the masterplan (plan 5): `pm plan add 5 "Play-test and close-out of age groups and bundles" --priority 390` (last, after part 2''s plan at 400).

- Cover: the milestone''s "done when": one session per age group and one with `colombia` off in the browser on the real pool; a task that raises a decision for the gamemaster to confirm, then records it.
- Docs: `plans/21-age-groups.md` (AG-7 `[x]`, drop "The game plays young teens until AG-7"), `plans/22-bundles.md` (BN-6 `[x]`, "Later" section), `plans/project.md`, `directory.md`, `about` texts of `app/data/age-groups.json` and `app/data/bundles.json`.
- Authoring readers that assume levels 1–10 or one range table (`/stats/difficulty`, `qgen report` supply; see decision 5) checked; fix only if broken, else log in `plans/backlog.md`.', '2026-10-12T00:22:30Z', '2026-10-12T00:29:08Z', 114);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (119, 27, 'create tasks for plan 27', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 123–125)', 'Split plan 27 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:25:09Z', '2026-10-12T00:29:47Z', 115);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (120, 28, 'create tasks for plan 28', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 126–127; decision raised by task 126 after measuring)', 'Split plan 28 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:26:19Z', '2026-10-12T00:30:18Z', 116);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (121, 29, 'create tasks for plan 29', 'split', 'done', 1000, '2026-10-12, tasks.sql (tasks 128, 129; no open decisions)', 'Split plan 29 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:28:05Z', '2026-10-12T00:30:53Z', 117);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (122, 30, 'create tasks for plan 30', 'split', 'done', 1000, '2026-10-11, tasks 130, 131, 132; play-test decision raised by task 131 (needs the pre-check table), task 132 waits on it', 'Split plan 30 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:29:06Z', '2026-10-12T00:31:25Z', 118);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (123, 27, 'Level ranges per age group in age-groups.json and the decision entry', 'work', 'open', NULL, NULL, 'Part 1 of plan 27 (AG-7, BN-6): the data that the selection and game tasks read. Needs plan 19''s `pool.ts` and plan 20''s `engineData`. If those files are missing, stop and leave the task open.

- `app/data/age-groups.json`: add `levels` to each group, 12 `[lo, hi]` pairs taken exactly from plan 27''s table (index 0 = level 1). `young_teens` = D-22. Set `about` to "levels: 12 difficulty ranges per group, level 1 first; young_teens = D-22; the others are a draft until tuned (AG-7)".
- `pool.ts`:
  - `AgeGroup {id, name, ages, window, levels}`, `LevelRanges = readonly (readonly [number, number])[]`.
  - `parseAgeGroups(json)` throws unless every group has 12 levels with `window[0] ≤ lo ≤ hi ≤ window[1]`, the ids are unique and `young_teens` exists.
  - `parseBundles(json)` → `Bundle {id, kind, always_on, name, description}[]`, unless `loadCategories` already parses bundles.
- `engineData(pool, categories, bundles, ageGroups)`: `data` gains `bundles`, `ageGroups`, `groupById`. Update its callers.
- `pool.test.ts`:
  - `parseAgeGroups` on the real file.
  - `young_teens.levels` equals D-22''s table, written out in the test. Compare it once against a throw-away `python3 -c` dump of `app/server/selection.LEVEL_RANGES` and don''t commit the script.
  - Bad files throw: 11 levels, a range outside the window, lo > hi.
- `qgen validate`: a small Python check in `authoring/tools/` with the same `levels` rules, so later hand edits (plan 28) fail early. Leave the authoring code that reads `window` / `focus` unchanged.
- `plans/decisions.md`: a new entry with the next D number, text as in plan 27''s "Decision entry". Related: D-22, D-28, D-38, D-39.
- `directory.md`: mention `levels` under `age-groups.json`.

Done when: `npm test`, `npm run check` and `qgen validate` pass, and `selection.ts` is still untouched.', '2026-10-12T00:29:45Z', NULL, 119);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (124, 27, 'Selection with per-group ranges and a bundle filter', 'work', 'open', NULL, NULL, 'Part 2 of plan 27: `selection.ts` takes the level ranges and the active bundles as arguments. Needs the task "Level ranges per age group in age-groups.json" (`AgeGroup.levels`, `LevelRanges`).

- Signatures:
  - `inRange(q, level, ranges)`
  - `assign(questions, levels, ranges)`: sort the slots by `(hi − lo, level)` of the given ranges
  - `draw(level, questions, {ranges, n, keep, avoidCategories, categoryOf, rng})`
  - `supply(questions, ranges)`: each `range` in the report comes from `ranges`
- Remove `LEVEL_RANGES`. `LEVELS = 12` and `PER_LEVEL = 4` stay.
- `available(pool, burned, exclude, bundles: ReadonlySet<string>)`: approved, not burned, not excluded, and `q.bundle ?? "base"` in `bundles`. Bundles are filtered only here.
- Keep the shuffle sites, their order and their lengths as plan 18 records them, so the tapes still match.
- Callers in `game.ts`: pass `young_teens`'' ranges and every bundle for now. Task 3 switches them to the game''s choice. The game must keep compiling and its replay must keep passing.
- `selection.test.ts`: the fixture replay uses `young_teens`'' ranges from `age-groups.json` with every bundle on. No fixture is re-recorded.
- `invariants.test.ts` (real pool, skipped if absent): run the seeded 12-level walks for each of the 4 groups × `{base}` and `{base, colombia}`. Every level gets 4 distinct cards inside the group''s range, and with `colombia` off no `colombia` question is ever drawn.

Done when: `npm test` and `npm run check` pass, every replay passes byte for byte, and `grep -rn LEVEL_RANGES app/client/src` finds nothing in the engine.', '2026-10-12T00:29:45Z', NULL, 119);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (125, 27, 'Age group and bundles as game settings, choice route', 'work', 'open', NULL, NULL, 'Part 3 of plan 27: each game plays its own age group and bundles. Needs the task "Selection with per-group ranges and a bundle filter". Follow plan 27''s "Game" and "API" sections exactly.

- `state.ts`: `GameState.settings: {jokers, age_group?, bundles?}`. `withDefaults` stays jokers-only, the port of Python''s `with_defaults`. `lib/types.ts` `Game.settings` gets the same optional keys.
- `game.ts`:
  - `gameChoice(state, data)` → `{age_group, bundles}`. A missing key is resolved on read (`young_teens`, every bundle in `bundles.json`) and never written back. Export the defaults for part 2''s HUD.
  - `resolveChoice(data, input)`:
    - Bundles: every `always_on` bundle is added (read the flag, not the id), `[]` becomes `[base]`, duplicates are dropped, and the order follows `bundles.json`.
    - Errors are `GameError`s: «grupo de edad desconocido: ''x''» (also for a non-string group), «paquete desconocido: ''x''», «los paquetes deben ser una lista».
  - Paths that use the game''s choice:
    - `availableNow` (bundles)
    - `draw` (ranges; the error «no quedan preguntas para el nivel N (dificultad lo–hi)» names the group''s range)
    - `laterFill`, `categoryCandidates`, `replacement`
    - «Paso» (with purge)
    - «Bájale»: candidates come from the bundle-filtered list and are still only "easier than the current card", with no window bound
    - «Cambiazo», «Francotirador» (repeat draw), and the replacement after an admin skip
  - `supply(save, data, player?, choice?)`.
  - `newGame`: check supply for the requested choice before anything else, and write `age_group` / `bundles` only when the request carries them.
  - `jokersView`: «Cambiazo» groups are the `data.categories` whose `bundle` is active, in the same order.
  - `undo` keeps the current settings.
- `api.ts`:
  - `gameAction(…, "new", {player, age_group?, bundles?})`, with coercion like the other args.
  - New route `choice(save, data, {player?, age_group?, bundles?})` → `200 {choice, supply}` | `409 {error, supply: null}`. A missing field comes from the player''s newest game, else the defaults.
  - `getGame` is unchanged.
- `choice.test.ts` (real pool and data, skipped if absent): the cases listed in plan 27''s "Checks". In short:
  - each group: a game played to `won` with every joker used once
  - `colombia` off
  - normalization of `[]` and `["colombia"]`
  - unknown values → 409 with the save unchanged
  - a state without the new keys draws exactly like the explicit default (same seed)
  - the `choice` route
- Plans:
  - `plans/21-age-groups.md`, AG-7: note "engine: group ranges and choice per game, plan 27". It stays `[ ]` until plan 30.
  - `plans/22-bundles.md`, BN-6: the same note, and update the "Later" sentence on Cambiazo.
  - `plans/12-client-engine.md`, if it lists engine functions.

Done when: `npm test`, `npm run check`, `npm run build` and `qgen validate` pass. Plans 18–20''s fixture replays pass byte for byte with no choice in any request. The screens are untouched.', '2026-10-12T00:29:45Z', NULL, 119);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (126, 28, 'Measure the draft level ranges, propose tuned windows, raise the approval decision', 'work', 'open', NULL, NULL, 'Part 1 of plan 28 (AG-7): measure what plan 27''s draft `levels` can play on the real pool, write a proposal, and ask the gamemaster. Needs plan 27 done: `levels` in `app/data/age-groups.json`, `parseAgeGroups`, `available(…, bundles)`, `supply(questions, ranges)`, `draw(level, questions, {ranges, …})`. If they are missing, stop and leave the task open.

- Throw-away `node` script (run like the engine tests, not committed, deleted afterwards) over `app/data/pool.json` + `app/data/age-groups.json`, per group × `{base}`, `{base, colombia}`; everything listed in plan 28''s "Measure":
  - per level: range, candidates, missing slots;
  - games until dry for one player: median over ~20 seeds, the level that runs out first;
  - per difficulty 1–15: approved count, expected cards per game;
  - plan 21''s demand table vs. the pool''s share per difficulty; each window vs. the scale anchors.
- Proposal for `kids`, `young_adults`, `adults` per plan 28''s "Adjust" (`young_teens` stays D-22, D-22''s shape, ≥ 20 candidates per level where the pool allows, widen thin top levels downward, overlap kept). Windows may move.
- `level_weights` for draft and proposal by plan 28''s formula; the script asserts `young_teens` equals `qgen.LEVEL_WEIGHTS` (sum 144).
- `plans/21-age-groups.md`: new section "Measured windows (AG-7)": date, pool size, one table per bundle set (draft vs. proposal: window, 12 ranges, thinnest level, games until dry), the thin top for milestone 1, and the demand table recomputed for the proposed windows. Don''t change `age-groups.json` or the "(draft)" wording yet.
- Decision: `pm decision add "Approve the age-group windows"` with the table and the thin top in the body; options in this order: "approve the proposal", "keep the draft windows", "adjust (name the change)".
- Make the task "Apply the approved age-group windows and level weights" (plan 28) wait on it: `pm task-pending-decision <that task> <decision>`.

Done when: plan 21 has the measured section, the decision is pending, the apply task waits on it, and no script is left in the repo.', '2026-10-12T00:30:14Z', NULL, 120);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (127, 28, 'Apply the approved age-group windows and level weights', 'work', 'open', NULL, NULL, 'Part 2 of plan 28 (AG-7). Needs the answer to the decision "Approve the age-group windows" (raised by the task "Measure the draft level ranges…"); read it in `pm show`. If the gamemaster asked for an adjustment, apply it as named, keeping D-22''s shape and the window bounds.

- `app/data/age-groups.json`: approved `window` and `levels` for `kids`, `young_adults`, `adults`; `young_teens` unchanged (D-22). New key `level_weights` for all four groups: `{"<difficulty>": n}` over the window, `n = round(12 × Σ 1/(hi − lo + 1))` over the levels containing the difficulty; `young_teens` equals `qgen.LEVEL_WEIGHTS`. `about` without "draft" ("levels: … tuned 2026-…, AG-7").
- Checks that `level_weights` has exactly the window''s keys and the values `levels` derive:
  - `parseAgeGroups` in `pool.ts`, plus a bad-file case in `pool.test.ts`;
  - the `levels` check of `qgen validate` in `authoring/tools/`.
- `plans/21-age-groups.md`: header "Window on the scale" without "(draft)"; remove "The windows of the other groups are a first draft…"; demand table recomputed if windows changed. AG-7 stays `[ ]`.
- `plans/decisions.md`: new entry (next D number): approved windows and ranges, `level_weights` derivation, `young_teens` = D-22. Related: D-22, D-31, D-38, D-53, plan 27''s entry.
- `plans/backlog.md`: `qgen` should read `young_teens.level_weights` instead of `LEVEL_WEIGHTS` once AG-8 starts.
- `directory.md`: mention `level_weights` under `age-groups.json`.

Done when: `npm test` (including `choice.test.ts` and `invariants.test.ts`), `npm run check` and `qgen validate` pass.', '2026-10-12T00:30:14Z', NULL, 120);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (128, 29, 'Choice screen: group and bundle choice between Player and Level', 'work', 'open', NULL, NULL, 'Build the Choice screen of plan 29 (AG-7, BN-6, IN-1). Everything in plan 29''s "Decisions taken here" applies; this task covers all of it except the overlay line.

## Before you start
- Plan 27 must be done: `engine/pool.ts` `AgeGroup` / `Bundle` / parsers, `engineData.ageGroups` / `.bundles`, `gameChoice`, the `choice` route, `newGame({player, age_group, bundles})`, `Game.settings` in `lib/types.ts`.
- M2 PORT-7 (screens on the engine, `plans/12-client-engine.md`) must have landed: `lib/api.ts` calls the in-client engine. If not, stop: log it in `plans/open-questions.md` and leave the task open. No Python route is added for this.
- `app/client/src/lib/i18n.ts` exists → every new string via `t()` with `choice.*` keys, `check:literals` passes. Else Spanish literals marked `// LUI-1` and the file listed in `plans/15a-ui-translation.md`.

## Changes
- `app/client/src/game/Choice.svelte` (new): props `player`, `busy`, `refused`; callbacks `onstart(choice)`, `onback()`; exported `key(e)` like `Player.svelte`. Arrive animations and glass tiles as on Player.
  - Title «¿Cómo juega {name}?».
  - Four group tiles in file order: `name` + ages («6–10 años», «23+ años» for `[23, null]`); window not shown; selected one highlighted like the name buttons'' focus.
  - Bundle toggles in file order: `name`, `description`, on/off; `always_on` shown on, locked, no key, `title` «Siempre activo».
  - Keys with `<kbd>` on every control: `1`–`4`, `←`/`→` group; bundle letter from one helper (first letter of `name`, case-insensitive, accents stripped, not taken by an earlier switchable bundle, else next letter; never `M`, `N`, `R`, `S`; today `C` = Colombia); `Enter`/`Space` «¡A jugar!»; `Backspace`/«Atrás» back to Player. `Esc` still opens the overlay.
  - Preset: `choice({player})` on entering (newest game of the player, else defaults).
  - Supply: on entering and on every change, `choice` for the current choice and once per group with the current bundles (5 calls). Group that can''t fill 12 levels: dimmed, «Faltan preguntas», still selectable. Selected choice fails: «¡A jugar!» disabled, report below. A `409` from `new` shows the report here.
- `app/client/src/game/SupplyReport.svelte` (new): today''s wording and style («No hay suficientes preguntas para una partida completa (N disponibles): Nivel L (dificultad lo–hi): faltan k»); replaces the copies in `Game.svelte` (Start) and `Player.svelte`. `Player.svelte` loses `refused` and its report.
- `Game.svelte`: `Screen` gains `"choice"`; `choosePlayer(name)` → `go("choice", "whoosh")`; `startGame(choice)` does today''s `act("new", …)` + greeting + Level; key routing for `"choice"`; Backspace/«Atrás» → `go("player", …)`.
- `lib/api.ts`: `fetchChoice({player?, age_group?, bundles?})`, `gameAction("new", {player, age_group, bundles})`, unless PORT-7 already typed them.
- `plans/04-ui-tv-display.md`: state diagram, table row, a "Choice" section, keys in "Input". `directory.md`: the two new files.

## Done when
- `npm run check`, `npm run build`, `npm test` (and `check:literals` if it exists) pass.
- Throw-away browser walk on the real pool (not committed): existing player, Enter, Enter plays as today (`young_teens`, every bundle); each group by key and by click; `C` and a click toggle Colombia, Básico doesn''t; the started game''s `settings` match the screen; a choice that can''t fill a game (test player with most questions burned, or a hand-edited `pool.json` copy in dev) dims the tile, shows the report, disables «¡A jugar!»; Backspace and «Atrás» return to Player; Esc opens the overlay; mouse only, then keyboard only, every action reachable.', '2026-10-12T00:30:51Z', NULL, 121);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (129, 29, 'Choice line in the overlay; preset after undo and abandon; AG-7/BN-6 notes', 'work', 'open', NULL, NULL, 'Close out plan 29 after the Choice screen task: show the running game''s choice to the gamemaster and check the preset survives undo and abandon.

## Changes
- `app/client/src/game/Overlay.svelte`: one read-only line under the joker budget, e.g. «Adolescentes · Básico, Colombia»: group `name` and active bundle `name`s in file order, from `game.settings` through `gameChoice`''s defaults (games without the keys show the defaults), names from `engineData.ageGroups` / `.bundles`. Not in the HUD. No way to change it mid-game.
- Strings: `t()` with `choice.*` keys if `app/client/src/lib/i18n.ts` exists, else Spanish literals marked `// LUI-1` and the file listed in `plans/15a-ui-translation.md`.
- `plans/21-age-groups.md` AG-7 and `plans/22-bundles.md` BN-6: note "start screen: plan 29"; both stay `[ ]` (closed by plan 30).
- `plans/04-ui-tv-display.md`: the overlay line in the overlay section. `directory.md` only if a file was added.

## Done when
- `npm run check`, `npm run build`, `npm test` (and `check:literals` if it exists) pass.
- Throw-away browser walk (not committed): Enter, Enter → overlay shows «Adolescentes · Básico, Colombia»; a game with Colombia off and another group shows that; after undo the choice is unchanged; after «Reiniciar partida» the next Choice screen presets the abandoned game''s choice.', '2026-10-12T00:30:51Z', NULL, 121);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (130, 30, 'Authoring readers check after age groups and bundles', 'work', 'open', NULL, NULL, 'Plan 30, task 1 ("Authoring readers" section). Independent of the play-test.

The authoring side still reads levels 1–10 from one range table; after plans 27–29 the game plays a window per age group and a bundle set. Check every reader:

- Known: `qgen report` supply (`authoring/tools/qgen.py`: `selection.LEVEL_RANGES`, `selection.supply`), authoring start page supply table (`authoring/server/overview.py` `supply_for`, `authoring/ui/src/home/Home.svelte`), `/stats/difficulty` (`authoring/ui/src/stats/DifficultyChart.svelte`, `PLAYED_GROUP = "young_teens"` shading).
- Grep for others: `LEVEL_RANGES`, `young_teens`, `1–10`, `range(1, 11)`.
- Run `qgen report`, `trivia-authoring` start page and `/stats/difficulty`.
- Broken (crash, wrong numbers for what it claims, text now false like "the window the game plays"): fix minimally (wording, or read `young_teens` `levels` from `app/data/age-groups.json`).
- Not broken but young-teens-only (supply per group/bundle set, shading every window): one line each in `plans/backlog.md`; link pm decision 5 (where the supply check lives) where it depends on it. Work on whatever decision 5 left in place.

Done when: readers run without errors, no false text; the rest logged in `plans/backlog.md`; `npm run check`, `qgen validate` pass.', '2026-10-12T00:31:20Z', NULL, 122);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (131, 30, 'Pre-check and play-test decision for age groups and bundles', 'work', 'open', NULL, NULL, 'Plan 30, task 2 ("Play-test" section). Needs plans 27, 28, 29 done.

1. Throw-away `node` script on the engine API over the real `app/data/pool.json`, a fresh player per run:
   - each of the 4 age groups with every bundle, and `young_teens` with `{base}` only;
   - `newGame` with the choice, play 12 levels to the end (answer right, use each joker once where allowed);
   - check every drawn question is in the group''s level range and an active bundle; Cambiazo offers no `colombia` category when it''s off.
2. `npm run build`, `npm run check`, `qgen validate`.
3. Failures → one fix task each in the owning plan (27 engine, 29 screen) with `pm task add`, not a fix here.
4. Raise the decision "Play-test of age groups and bundles" (`pm decision add`). Body: the pre-check''s result table (run × result) and the checklist: `trivia`; one session per age group (choice screen by mouse and by keyboard at least once, IN-1); one session with `colombia` off; defaults straight through with Enter look as before; overlay shows group and bundles; undo/abandon keep the choice. Options: "all sessions played fine" (recommended), "problems (listed in the answer)".
5. `pm task-pending-decision <close-out task of plan 30> <decision id>` (the "Close out AG-7 and BN-6" task).
6. Delete the script.

Done when: the decision exists with the table and checklist, the close-out task waits on it, script deleted.', '2026-10-12T00:31:20Z', NULL, 122);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (132, 30, 'Close out AG-7 and BN-6', 'work', 'open', NULL, NULL, 'Plan 30, task 3 ("Close-out docs" section). Waits on the play-test decision raised by the pre-check task.

If the answer is "problems": add one fix task per problem to plan 27 (engine) or 29 (screen), raise the play-test decision again (same body, updated), make this task pending on the new one, stage, stop.

If "all sessions played fine":
- `plans/21-age-groups.md`: AG-7 `[x]` with date and plans 27/28/29; remove "The game plays young teens (levels 1–10) until AG-7, whatever the focus" and other "until AG-7" wording.
- `plans/22-bundles.md`: BN-6 `[x]`; "Later" section: drop the BN-6 bullet (section too if empty); Cambiazo sentence ("all of them until BN-6") in the present tense.
- `plans/project.md`: AG-7, BN-6 `[x]`.
- `directory.md`: `age-groups.json` / `bundles.json` rows say the game reads them (group ranges, choice); check files new in plans 27–29 are listed.
- `app/data/age-groups.json` `about`: no "The game plays young teens until AG-7", no "draft". `app/data/bundles.json` `about`: "players switch on or off" and `base` always on still true.
- `plans/decisions.md`: new D entry (play-test confirmed, date, milestone 5 done-when met; related D-38, D-39, plans 27/28 entries) only if the answer adds something beyond "fine".

Done when: AG-7, BN-6 `[x]` in plans 21, 22, `project.md`; `grep -rn "until AG-7\|until BN-6" plans directory.md app/data/*.json` finds nothing; `qgen validate` passes.', '2026-10-12T00:31:20Z', NULL, 122);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (133, 6, 'create tasks for plan 6', 'split', 'dropped', 1000, 'tasks 134-136 added with the masterplan (task 6)', 'Split plan 6 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:32:21Z', '2026-10-12T00:32:24Z', 6);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (134, 6, 'write plan: Preload the next screen''s media (UI-7)', 'plan', 'done', 1000, '2026-10-11, plan 31 (tasks.sql)', 'Write the plan for part 1 of the masterplan (plan 6): `pm plan add 6 "…" --priority …` with the priority given there, and the plan''s scope, files and done-when as described in part 1.', '2026-10-12T00:32:21Z', '2026-10-12T00:33:14Z', 6);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (135, 6, 'write plan: Recorded sound effects (UI-10)', 'plan', 'done', 1000, '2026-10-11, plan 32 (tasks.sql)', 'Write the plan for part 2 of the masterplan (plan 6): `pm plan add 6 "…" --priority …` with the priority given there, and the plan''s scope, files and done-when as described in part 2.', '2026-10-12T00:32:21Z', '2026-10-12T00:34:31Z', 6);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (136, 6, 'write plan: Recorded music loops (UI-10)', 'plan', 'done', 1000, '2026-10-11, plan 33 (tasks.sql)', 'Write the plan for part 3 of the masterplan (plan 6): `pm plan add 6 "…" --priority …` with the priority given there, and the plan''s scope, files and done-when as described in part 3.', '2026-10-12T00:32:21Z', '2026-10-12T00:35:06Z', 6);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (137, 31, 'create tasks for plan 31', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 140, 141; no decisions needed)', 'Split plan 31 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:33:12Z', '2026-10-12T00:35:32Z', 134);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (138, 32, 'create tasks for plan 32', 'split', 'done', 1000, '2026-10-11, tasks 142-146; no upfront decisions (task 146 raises the gamemaster check)', 'Split plan 32 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:34:28Z', '2026-10-12T00:36:04Z', 135);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (139, 33, 'create tasks for plan 33', 'split', 'done', 1000, '2026-10-11, tasks.sql (tasks 147–150; no upfront decision: matched-set and gamemaster-check decisions are raised by tasks 147 and 149)', 'Split plan 33 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:35:05Z', '2026-10-12T00:36:39Z', 136);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (140, 31, 'UI-7: preload Question media before the fade-in', 'work', 'open', NULL, NULL, '`go()` in `app/client/src/game/Game.svelte` waits for the next Question''s media before fading in, at most 2 s; video/audio no longer play behind the black. Shape: plan 31, "Shape (decided here)".

- `Question.svelte`: export `ready(): Promise<void>`; resolves on picture decoded (`onload` / `img.decode()`), video/audio `canplaythrough`, or any failure (`onerror`, `mediaFailed`); text question → resolves at once.
- Drop `autoplay` on `<video>`/`<audio>` (~lines 367, 386); export `start()` (or a `shown` prop, your pick) that `go()` calls when `black = false`.
- Paths not through `go()` (page reload on a running game, `{#key game.question.id}` swaps by Bájale/Cambiazo): media still starts by itself, no waiting.
- `pausedMedia` (overlay pause) and `replay()` keep working with the deferred start.
- `go()`: after `screen = next`, `await tick()`, then `Promise.race([questionRef?.ready() ?? Promise.resolve(), sleep(PRELOAD_MAX_MS)])`, then fade in as today. Other screens: no wait.
- `timing.ts`: `PRELOAD_MAX_MS = 2000`, one-line comment.
- Remove the `PLACEHOLDER(UI-7)` comment (Game.svelte ~117).
- No new dependencies.

Done when:
- `npm run check`, `npm run build` pass.
- Dev browser, DevTools "Slow 4G", large video/image: fade waits for the media, never > 2 s; video/audio start with the fade-in.
- `/media` 404: fade in after ≤ 2 s, «medio no disponible» notice shows.
- Text questions and media-free screens fade in as fast as today.', '2026-10-12T00:35:30Z', NULL, 137);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (141, 31, 'Inline missing-media notice, delete Placeholder.svelte, docs', 'work', 'open', NULL, NULL, 'The last `PLACEHOLDER` hits go; the «medio no disponible» chip is a runtime fallback, not unfinished work (plan 31, "Missing media notice").

- `Question.svelte` (~line 420): replace `<Placeholder task="IMG" … chip />` with a plain inline notice, same text, same chip look, no `PLACEHOLDER · …` tag; delete `app/client/src/game/Placeholder.svelte`.
- Task 95 (LUI-1) overlap: if it ran first, keep the catalog key but rename `placeholder.*` → `question.mediaMissing` (or similar); if not, leave the literal, 95 catalogs it.
- Docs: AGENTS.md "Placeholders" line, `plans/04-ui-tv-display.md` "Implementation notes" (Placeholders bullet), `plans/project.md` ("One placeholder left", M3 row, UI-7 follow-up line): none left; D-25 stays as history.
- 04: UI-7 note (preload done; Question only; reload and Bájale/Cambiazo swaps don''t wait).

Done when:
- `grep -rn PLACEHOLDER app/client/src` is empty; `npm run check`, `npm run build` pass.
- Missing media file still shows the notice in the dev browser.', '2026-10-12T00:35:30Z', NULL, 137);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (142, 32, 'Audition aid /?efectos with recorded/synth toggle', 'work', 'open', NULL, NULL, 'First task of plan 32, so every later pick can be compared on the TV.

- `app/client/src/game/sound.svelte.ts`: a way to force the synth path, e.g. an optional flag on `sfx(name, { synth: true })` or an exported helper; default behaviour unchanged.
- `app/client/src/game/Game.svelte`: `/?efectos` on the Start screen, next to the `?fuegos` preview: a small list of every effect name (the names `RECIPES` / `SAMPLE_FOR` match, incl. the 13 existing recordings), each with «grabado» and «sintetizado» buttons.
- Minimal, plain styling; dev/check only, not in the admin overlay (B-3 «Demo de efectos» stays backlog).
- Keep the effect list in one place so later tasks (and plan 33''s music loops) just add entries.

Done when: `/?efectos` plays every effect both ways (recorded where a file exists); `npm run check` and `npm run build` pass.', '2026-10-12T00:36:02Z', NULL, 138);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (143, 32, 'Recorded whooshes, pops, menu blips, desbloqueado, hola', 'work', 'open', NULL, NULL, 'Replace the synthesized UI effects with CC0 recordings (plan 32 "Sources", "Pipeline", "Wiring").

- Effects: `whoosh`, «swoosh que sube», `swoosh|escoba` («escoba: fuuush»), `pop|carta`, `menú abierto` / `menú cerrado`, `desbloqueado`, `listo|hola`.
- Sources: Kenney.nl CC0 first (Interface Sounds, UI Audio, Impact Sounds, Digital Audio, Sci-fi Sounds), then Freesound/OpenGameArt CC0; D-45 allowlist only. Download outside the repo; don''t commit zips.
- Convert with `nix shell nixpkgs#ffmpeg-headless`: trim silence, short fade-out, `loudnorm` at the same target as the existing files, mono, AAC `.m4a`, ≤ 40 kB per file → `app/client/public/audio/<spanish-name>.m4a`.
- Wire: `SAMPLE_NAMES` + `SAMPLE_FOR` in `sound.svelte.ts`; `rate` callback for pops; variants only if repetition is audible. Recipes stay as fallback.
- `app/client/public/audio/CREDITS.md`: one row per file (source URL, pack, author, licence).
- If no recording beats the synth, keep the recipe; note which in the task''s done note (task 5 collects them for UI-10).

Done when: compared via `/?efectos`; credits complete; `npm run check` and `npm run build` pass.', '2026-10-12T00:36:02Z', NULL, 138);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (144, 32, 'Recorded joker sounds, Soplo rustle and token pop-back', 'work', 'open', NULL, NULL, 'Replace the synthesized joker sounds and give the two silent ones a sound (plan 32; JK-9 in `plans/09-jokers.md`).

- Effects: `comodín` shimmer, `comodín: preparado`, `comodín: abrir`, `silbato`, `trituradora`, `latido`, `rebobinar`, `mira: tic`, `disparo|corcho`, `rasgado` (envelope tear).
- Still silent: Soplo''s note paper rustle, token pop-back. Add an `sfx("…")` call with a new name at their call sites, a recording, and a tiny synth recipe as fallback; add both to the `/?efectos` list.
- Sources, pipeline, wiring, budget and `CREDITS.md` as in the previous task (Kenney Casino Audio / Impact Sounds / Sci-fi Sounds are likely candidates).
- Keep the recipe where no recording is better; record which in the done note.
- Update JK-9''s note in `plans/09-jokers.md` (rustle and pop-back now audible).

Done when: compared via `/?efectos`; both new sounds audible in a game; `npm run check` and `npm run build` pass.', '2026-10-12T00:36:02Z', NULL, 138);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (145, 32, 'Recorded firework sounds', 'work', 'open', NULL, NULL, 'Replace the synthesized firework sounds (plan 32; fireworks preview `/?fuegos`, UI-9).

- Effects: `cohete`, `cañón de confeti`, `bengalas`, `estrellas`.
- `rate` callback for stars and cannon so repeats vary in pitch.
- Sources, pipeline, wiring, `CREDITS.md` as in the earlier tasks; check the total budget: new effects ≤ 400 kB, ≤ 40 kB per file.
- Keep the recipe where no recording is better; record which in the done note.

Done when: compared via `/?efectos` and `/?fuegos=finale`; `npm run check` and `npm run build` pass.', '2026-10-12T00:36:02Z', NULL, 138);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (146, 32, 'Gamemaster check of the recorded effects on the TV', 'work', 'open', NULL, NULL, 'Close-out of plan 32.

1. Collect from the earlier tasks'' notes what was replaced and what stayed synthesized.
2. `pm decision add` asking the gamemaster to check the effects on the TV via `/?efectos` and a real game; body: the list (replaced / kept synthesized); options e.g. «approve» / «changes: …». Make this task pending on it (`pm task-pending-decision`), stage, stop.
3. Once answered: apply the feedback (swap or drop files, adjust rates/levels).
4. Update UI-10''s note in `plans/04-ui-tv-display.md` (what is recorded now, what stays synthesized and why) and `plans/project.md`. UI-10 stays `[~]` until plan 33 (music loops) is done.

Done when: the gamemaster approved; audio folder within budget; `CREDITS.md` complete; `npm run check` and `npm run build` pass.', '2026-10-12T00:36:02Z', NULL, 138);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (147, 33, 'Source and convert a matched set of CC0 music loops', 'work', 'open', NULL, NULL, 'First task of plan 33: find one matched set of recordings for `normal`, `question`, `submitted` and put the converted files in place (plan 33 "Sources and licences", "Pipeline"). Conversion is here, not in the wiring task: downloads live outside the repo and don''t survive between runs.

- Sources: Kenney.nl CC0 first (music loops / jingles packs), then OpenGameArt CC0, Freesound CC0; D-45 allowlist only (CC0 preferred; CC BY ok with credit; no NC/ND/unknown). Download outside the repo; don''t commit zips.
- Need: one theme at three intensities (calm / tense / most tense; variants or stems), or loops close enough in key and tempo that ~80 ms cuts `question` ↔ `submitted` don''t clash.
- Convert with `nix shell nixpkgs#ffmpeg-headless`: whole number of bars, loop length 20–40 s, `loudnorm` to the same target as `redoble.m4a`, stereo ok, AAC `.m4a` ~96–128 kbit/s → `app/client/public/audio/musica-normal.m4a`, `musica-pregunta.m4a`, `musica-enviada.m4a`.
- Check the seam (AAC encoder padding); note the loop points in seconds per file in the done note if the file length isn''t clean.
- `app/client/public/audio/CREDITS.md`: one row per file (source URL, pack, author, licence), CC0 too.
- Budget: the three ≤ 900 kB together; whole folder ≤ 3.5 MB.
- No matched set found: don''t guess. `pm decision add` for the gamemaster with the candidates you found and the options from plan 33 (1. one CC0 loop for all three, varied by rate / low-pass / synth layer on top; 2. recordings for some tracks, synth for the rest; 3. keep the synthesized loops), your recommendation first; make this task and the wiring task pending on it, stage, stop. After the answer: convert what the chosen option needs.

Done when: the three files (or what the decision asks for) are in place, within budget, with credit rows; the done note lists source, key, tempo, loop points.', '2026-10-12T00:36:37Z', NULL, 139);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (148, 33, 'Wire the music loops into startTrack() with synth fallback; extend /?efectos', 'work', 'open', NULL, NULL, 'Play the recorded loops from the previous task (plan 33 "Wiring", "Audition aid").

- `app/client/src/game/sound.svelte.ts`: `SAMPLE_NAMES` gets `musica-normal`, `musica-pregunta`, `musica-enviada`; `startTrack()` plays the decoded buffer via `AudioBufferSourceNode` with `loop = true` (+ `loopStart`/`loopEnd` per track if the previous task''s note gives loop points) into the track''s gain, like the `redoble` branch. The lookahead scheduler (`CHORDS`, `TEMPO`) stays as the fallback when a file is missing or fails to decode.
- Behaviour unchanged (04 "Music"): 600/800 ms fades, ~80 ms cuts `question` ↔ `submitted`, cut to `roll` on submit, ducking for jokers.
- Cuts: if the loops share tempo, start the new one at the old one''s position modulo its length so the beat continues; else at 0. Decide by ear.
- A per-track level constant if they don''t sit right against the music bus (as `redoble` uses 2.2).
- `/?efectos` (plan 32''s list in `Game.svelte`): the three tracks with «grabado» / «sintetizado», a «corte» button toggling `question` ↔ `submitted`, tracks keep looping so the seam can be heard.
- Header comment of `sound.svelte.ts`: what is still synthesized.
- If the decision from the previous task chose another option, implement that instead (e.g. one loop varied by rate / low-pass / synth layer).

Done when: `npm run check`, `npm run build` pass; dev browser: the three loops play gapless, cuts and fades work; with the files removed the synth loops play.', '2026-10-12T00:36:37Z', NULL, 139);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (149, 33, 'Gamemaster check of the music loops on the TV', 'work', 'open', NULL, NULL, 'Plan 33 task 3, same pattern as plan 32''s gamemaster check.

1. `pm decision add` asking the gamemaster to check the music on the TV via `/?efectos` and a real game: clicks at the seam, the `question` ↔ `submitted` cuts, level against effects and question media. Body: what is recorded, what stayed synthesized, sources. Options e.g. «approve» / «changes: …». Make this task pending on it (`pm task-pending-decision`), stage, stop.
2. Once answered: apply the feedback (loop points, levels, cut behaviour, swap files; keep `CREDITS.md` and budget in line).

Done when: the gamemaster approved; `npm run check`, `npm run build` pass.', '2026-10-12T00:36:37Z', NULL, 139);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (150, 33, 'Close UI-10 in the plans', 'work', 'open', NULL, NULL, 'Last task of plan 33; runs after the gamemaster approved the music (and plan 32''s effects check, task 146).

- `plans/04-ui-tv-display.md`: UI-10 `[x]` with a note (what is recorded now, what stayed synthesized and why, effects and music); "Sound assets": flat `app/client/public/audio/` folder (the `music/`, `sfx/` subfolders were never used), `CREDITS.md`, budget.
- `plans/project.md`: M6 / UI-10 line.
- Check: whole audio folder ≤ 3.5 MB; `CREDITS.md` has a row per recorded file.

Done when: 04 and `plans/project.md` updated; `grep -rn PLACEHOLDER app/client/src` result noted for the milestone.', '2026-10-12T00:36:37Z', NULL, 139);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (151, 7, 'create tasks for plan 7', 'split', 'done', 1000, '2026-10-11, tasks 162-171 (tasks.sql)', 'Split plan 7 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:37:56Z', '2026-10-12T00:38:54Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (152, 7, 'write plan: Desktop shell (OQ-29)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 1 of masterplan 7 ("Desktop shell (OQ-29)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Desktop shell (OQ-29)" --priority 700`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:01Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (153, 7, 'write plan: Default mode (OQ-30)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 2 of masterplan 7 ("Default mode (OQ-30)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Default mode (OQ-30)" --priority 600`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:01Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (154, 7, 'write plan: Reportar pregunta and settings screen (MD-6, MD-7)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 3 of masterplan 7 ("Reportar pregunta and settings screen (MD-6, MD-7)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Reportar pregunta and settings screen (MD-6, MD-7)" --priority 500`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (155, 7, 'write plan: Launch languages and Spanish variety (OQ-31)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 4 of masterplan 7 ("Launch languages and Spanish variety (OQ-31)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Launch languages and Spanish variety (OQ-31)" --priority 500`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (156, 7, 'write plan: Content target per player and language (OQ-32)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 5 of masterplan 7 ("Content target per player and language (OQ-32)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Content target per player and language (OQ-32)" --priority 590`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (157, 7, 'write plan: Price model and Steamworks account (OQ-33)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 6 of masterplan 7 ("Price model and Steamworks account (OQ-33)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Price model and Steamworks account (OQ-33)" --priority 300`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (158, 7, 'write plan: Code and content licence (OQ-35)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 7 of masterplan 7 ("Code and content licence (OQ-35)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Code and content licence (OQ-35)" --priority 290`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (159, 7, 'write plan: Competitive and couch co-op format (OQ-37)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 8 of masterplan 7 ("Competitive and couch co-op format (OQ-37)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Competitive and couch co-op format (OQ-37)" --priority 580`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (160, 7, 'write plan: Freesound API for a commercial release (OQ-45)', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 9 of masterplan 7 ("Freesound API for a commercial release (OQ-45)"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "Freesound API for a commercial release (OQ-45)" --priority 200`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (161, 7, 'write plan: S2 close-out', 'plan', 'dropped', 1000, 'created too early by task 7; task 151 (create tasks for plan 7) adds the part tasks', 'Write the plan for part 10 of masterplan 7 ("S2 close-out"): read the part in `pm show` of this task''s plan and the owning plan file, then `pm plan add 7 "S2 close-out" --priority 150`. Follow "How a decision part works" in the masterplan.', '2026-10-12T00:38:02Z', '2026-10-12T00:38:10Z', 7);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (162, 7, 'write plan: Desktop shell (OQ-29)', 'plan', 'done', 1000, '2026-10-11, plan 34 (Desktop shell, OQ-29) in tasks.sql', 'Write the plan for part 1 of the masterplan (plan 7): `pm plan add 7 "Desktop shell (OQ-29)" --priority 700`.
- Owner: `plans/18-steam-integration.md` ("Desktop shell"), SW-1.
- Tasks: prep (refresh facts: steamworks.js status, Electron support, install size, Deck/Proton, overlay; `pm decision add`, `pm task-pending-decision` on the follow-up), follow-up (D-entry, OQ-29 resolved, SW-1 `[x]`, plan 18 table decided, SW-2..SW-6 checked).
- Note OQ-37 (part 8) as a dependency (phones as buzzers → LAN server in the shell), not a blocker.', '2026-10-12T00:38:51Z', '2026-10-12T00:39:19Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (163, 7, 'write plan: Default mode (OQ-30)', 'plan', 'done', 1000, '2026-10-11, plan 35 (Default mode, OQ-30) in tasks.sql', 'Write the plan for part 2 of the masterplan (plan 7): `pm plan add 7 "Default mode (OQ-30)" --priority 600`.
- Owner: `plans/13-game-modes.md` ("Default mode"), MD-5.
- Tasks: prep (joker presets per difficulty, checkpoints, won levels, remaining admin actions; fit D-38 / `plans/21-age-groups.md` and the windows of plans 27, 28; may split into two decisions), follow-up (D-entry, OQ-30 resolved, MD-5 `[x]`, plan 13''s section a spec for MD-6/MD-7).', '2026-10-12T00:38:51Z', '2026-10-12T00:39:49Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (164, 7, 'write plan: Reportar pregunta and settings screen (MD-6, MD-7)', 'plan', 'done', 1000, '2026-10-11, plan 36 (Reportar pregunta and settings screen, MD-6/MD-7) in tasks.sql', 'Write the plan for part 3 of the masterplan (plan 7): `pm plan add 7 "Reportar pregunta and settings screen (MD-6, MD-7)" --priority 500`.
- Implementation after part 2''s decision; tasks wait for it (`pm task-pending-decision` on part 2''s decision if still pending).
- Builds on plan 20 "Engine game state machine (PORT-3)" and `SaveData`; strings via plan 21 "t() helper and the es catalog (LUI-1)". No second implementation in `app/server/game.py`.
- Done when as in part 3.', '2026-10-12T00:38:51Z', '2026-10-12T00:41:06Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (165, 7, 'write plan: Launch languages and Spanish variety (OQ-31)', 'plan', 'done', 1000, '2026-10-11, plan 37 (Launch languages and Spanish variety, OQ-31) in tasks.sql', 'Write the plan for part 4 of the masterplan (plan 7): `pm plan add 7 "Launch languages and Spanish variety (OQ-31)" --priority 500`.
- Owner: `plans/15-i18n.md` (+15a/15b/15c), I18N-1.
- Tasks: prep (Steam survey language shares, translation cost per question from `costs.log`, `colombia` vs `base` share, D-39, D-49, D-50; decision), follow-up (D-entry, OQ-31 resolved, I18N-1 `[x]`, 15/15a/15b updated, plan 24 "Draft en catalog (LUI-3)" checked against the answer).', '2026-10-12T00:38:52Z', '2026-10-12T00:41:50Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (166, 7, 'write plan: Content target per player and language (OQ-32)', 'plan', 'done', 1000, '2026-10-11, plan 38 (Content target per player and language, OQ-32) in tasks.sql', 'Write the plan for part 5 of the masterplan (plan 7): `pm plan add 7 "Content target per player and language (OQ-32)" --priority 590`.
- Owner: `plans/16-content-target.md`, CT-1. Needs parts 2 and 4 (their decisions): the follow-up waits on them; part 8''s burn multiplier too, if known.
- Tasks: prep (estimate from approved counts per level and window, D-52, D-53, burns per game; quality bar: point to D-56 / pm decision 2 instead of duplicating), follow-up (D-entry, OQ-32 resolved, CT-1 `[x]` noting CT-2 in S4 confirms it).', '2026-10-12T00:38:52Z', '2026-10-12T00:42:35Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (167, 7, 'write plan: Price model and Steamworks account (OQ-33)', 'plan', 'done', 1000, '2026-10-11, plan 39 (tasks.sql)', 'Write the plan for part 6 of the masterplan (plan 7): `pm plan add 7 "Price model and Steamworks account (OQ-33)" --priority 300`.
- Owner: `plans/17-publishing.md` ("Steamworks and store").
- Tasks: prep (Steam fees and payout, comparable prices, paid / free / free + DLC bundles (D-39), person vs company account; consequences for parts 7 and 8; flag where a professional must check), follow-up (D-entry, OQ-33 resolved, PUB-6 and PUB-11 rewritten, still S5).', '2026-10-12T00:38:52Z', '2026-10-12T00:43:15Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (168, 7, 'write plan: Code and content licence (OQ-35)', 'plan', 'done', 1000, '2026-10-11, plan 40 (tasks.sql)', 'Write the plan for part 7 of the masterplan (plan 7): `pm plan add 7 "Code and content licence (OQ-35)" --priority 290`.
- Owner: `plans/17-publishing.md` ("Code and content license"), PUB-4. Needs part 6''s decision.
- Tasks: prep (code × questions × repo options; media licences stay per file, plan 26 "Licence data in the pool"), follow-up (D-entry, OQ-35 resolved, PUB-4 `[x]`), then `LICENSE` (+ content licence file) and mentions in `README.md`, `directory.md`.', '2026-10-12T00:38:52Z', '2026-10-12T00:43:53Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (169, 7, 'write plan: Competitive and couch co-op format (OQ-37)', 'plan', 'done', 1000, '2026-10-11, plan 41 (tasks.sql)', 'Write the plan for part 8 of the masterplan (plan 7): `pm plan add 7 "Competitive and couch co-op format (OQ-37)" --priority 580`.
- Owners: `plans/13-game-modes.md` ("Competitive mode", "Couch co-op"), `plans/14-input.md` (section 3, IN-7).
- Tasks: prep (formats: relay, parallel ladders, buzzer; input: hot-seat, controllers, phones; decision notes burn multiplier for part 5 and shell needs for part 1), follow-up (D-entry, OQ-37 resolved, plans 13 and 14 name the format; MD-8, MD-9, IN-6 stay "Later").', '2026-10-12T00:38:52Z', '2026-10-12T00:44:29Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (170, 7, 'write plan: Freesound API for a commercial release (OQ-45)', 'plan', 'done', 1000, '2026-10-11, tasks.sql (plan 42)', 'Write the plan for part 9 of the masterplan (plan 7): `pm plan add 7 "Freesound API for a commercial release (OQ-45)" --priority 200`.
- Owner: `plans/23-media-providers.md` (Freesound row, MP-6).
- Tasks: housekeeping (OQ-45 used twice in `open-questions.md`: give the Freesound one a free number, update references), prep (ask Freesound/UPF with drafted email the gamemaster sends; replace picks via allowlisted sources (D-45); family-only and excluded from SW-9), follow-up (D-entry, plan 23 and provider order updated; if replacing, a task that re-picks via the review tool, D-36).', '2026-10-12T00:38:52Z', '2026-10-12T00:45:20Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (171, 7, 'write plan: S2 close-out', 'plan', 'done', 1000, '2026-10-11, pm plan 43 (S2 close-out)', 'Write the plan for part 10 of the masterplan (plan 7): `pm plan add 7 "S2 close-out" --priority 150`.
- Last; its tasks wait for the decisions of parts 1, 2, 4–9.
- `plans/11-steam.md`: open-questions table with D-numbers, S3–S6 and track table updated, ST-1 `[x]`; `plans/project.md`, `plans/README.md` statuses; notes in masterplans of milestones 8–11 (plans 8–11) if their scope changed.
- Done when the milestone''s "Done when" holds.', '2026-10-12T00:38:52Z', '2026-10-12T00:46:13Z', 151);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (172, 34, 'create tasks for plan 34', 'split', 'done', 1000, '2026-10-11, tasks 182 (prep + decision), 183 (record answer; made pending by 182)', 'Split plan 34 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:39:17Z', '2026-10-12T00:46:35Z', 162);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (173, 35, 'create tasks for plan 35', 'split', 'done', 1000, '2026-10-11, tasks 184 (prep + decisions), 185 (record answer; made pending by 184)', 'Split plan 35 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:39:47Z', '2026-10-12T00:46:59Z', 163);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (174, 36, 'create tasks for plan 36', 'split', 'done', 1000, '2026-10-11, tasks 186 (engine), 187 (MD-6 UI), 188 (MD-7, prio 380); no new decisions: OQ-30 decisions come from task 184, tasks guard on them', 'Split plan 36 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:41:03Z', '2026-10-12T00:47:37Z', 164);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (175, 37, 'create tasks for plan 37', 'split', 'done', 1000, '2026-10-11, tasks 189 (facts + decisions), 190 (record answer); no new decisions here: OQ-31 decisions come from task 189, which makes 190 wait on them', 'Split plan 37 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:41:48Z', '2026-10-12T00:48:07Z', 165);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (176, 38, 'create tasks for plan 38', 'split', 'done', 1000, '2026-10-11, tasks 191 (estimate + decision), 192 (record answer); no new decisions here: the OQ-32 decision comes from task 191, which makes 192 wait on it', 'Split plan 38 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:42:23Z', '2026-10-12T00:48:30Z', 166);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (177, 39, 'create tasks for plan 39', 'split', 'done', 1000, '2026-10-11, tasks 193 (facts + decision(s)), 194 (record answer); no new decisions here: the OQ-33 decision(s) come from task 193, which makes 194 wait on them', 'Split plan 39 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:43:13Z', '2026-10-12T00:48:51Z', 167);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (178, 40, 'create tasks for plan 40', 'split', 'done', 1000, '2026-10-11, tasks 198 (facts + decision(s), pends on OQ-33 if unanswered), 199 (record answer), 200 (licence files, PUB-4); 195–197 dropped (re-added in order); no new decisions here: task 198 writes the OQ-35 decision(s) and makes 199/200 wait', 'Split plan 40 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:43:52Z', '2026-10-12T00:49:43Z', 168);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (179, 41, 'create tasks for plan 41', 'split', 'done', 1000, '2026-10-11, tasks 201 (facts + OQ-37 decision(s), makes 202 wait), 202 (record answer in decisions/open-questions/plans 11, 13, 14, 16, project); no decisions here: task 201 writes them', 'Split plan 41 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:44:27Z', '2026-10-12T00:50:08Z', 169);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (180, 42, 'create tasks for plan 42', 'split', 'done', 1000, '2026-10-11, tasks 203 (renumber Freesound OQ-45), 204 (facts + decision, makes 205 wait), 205 (record answer in decisions/open-questions/plans 11, 23, project); no decisions here: task 204 writes it', 'Split plan 42 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:45:18Z', '2026-10-12T00:50:37Z', 170);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (181, 43, 'create tasks for plan 43', 'split', 'done', 1000, '2026-10-11, tasks 206, 207 (tasks.sql); no new decisions: S2 decisions come from plans 34–42', 'Split plan 43 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:46:09Z', '2026-10-12T00:51:08Z', 171);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (182, 34, 'Desktop shell: refresh facts, write the decision (OQ-29)', 'work', 'done', NULL, '2026-10-11, decision 12, plans/18-steam-integration.md; task 183 pending on decision 12', 'Part 1 of plan 34. Prepare the OQ-29 decision; no shell code.

- Facts, each with source and date:
  - steamworks.js: last release, open issues, supported Electron versions; alternatives (steamworks-ffi, Steamworks SDK via a native module).
  - Electron install size today.
  - Tauri v2: Windows (WebView2); Linux/Deck (WebKitGTK: media playback, `backdrop-filter`).
  - Steam overlay: Electron (known workarounds) vs. a system webview.
  - Deck/Proton: native Linux build vs. Windows build via Proton.
- OQ-37 (plan 41) as a dependency, not a blocker: phones as buzzers need a LAN server inside the shell. Say how each option handles it (Electron: Node `http` in main; Tauri: Rust side; browser + local server: has one).
- `pm decision add "Desktop shell (OQ-29)?"`: recommended option first; body = facts + trade-offs, ultra-short.
- `pm task-pending-decision <follow-up task> <decision id>` on the follow-up task of plan 34 ("record the answer").
- `plans/18-steam-integration.md`: update the "For/Against" cells of the "Desktop shell" table if facts changed; keep it marked draft.

Done when: the decision exists with sourced facts, the follow-up task waits on it, plan 18''s table is current.', '2026-10-12T00:46:31Z', '2026-10-12T02:11:02Z', 172);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (183, 34, 'Desktop shell: record the answer (OQ-29, SW-1)', 'work', 'open', NULL, NULL, 'Part 2 of plan 34. Waits for the decision "Desktop shell (OQ-29)?" (made pending by the prep task); the answer is in `pm show`.

- `plans/decisions.md`: D-entry with the next free D-number.
- `plans/open-questions.md`: OQ-29 moved to "Resolved" with the D-number.
- `plans/18-steam-integration.md`: "Desktop shell" table marked decided (D-number); SW-1 `[x]` with a note; SW-2..SW-6 checked against the choice and reworded if needed (e.g. electron-builder → Tauri bundler; preload bridge → Tauri commands).
- `plans/11-steam.md` open-questions row and `plans/project.md` in sync. The full S3–S6 rewrite stays with plan 43 (S2 close-out).

Done when: D-entry exists; OQ-29 resolved; SW-1 `[x]`; plan 18''s table says decided; SW-2..SW-6 match the choice.', '2026-10-12T00:46:31Z', NULL, 172);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (184, 35, 'Default mode: gather facts, write the decisions (OQ-30)', 'work', 'open', NULL, NULL, 'Part 1 of plan 35. Prepare the OQ-30 decision(s); no code.

- Facts (from `plans/13-game-modes.md`, D-28 in `plans/decisions.md`, `plans/21-age-groups.md`, plans 27/28 via `pm show`):
  - what each joker burns or saves (Soplo, Paso, Bájale, Cambiazo, Francotirador)
  - how a checkpoint interacts with burning and "12 to victory"
  - what `age-groups.json` holds per group (`levels`), so a preset can or can''t shift it
  - cards burned per game under each preset (rough; input for OQ-32, plan 38)
- Questions: (a) joker counts per preset, number of presets, default preset; (b) presets shift difficulty or only jokers; (c) checkpoints: none / Fácil only (level 6) / per preset; (d) won levels: only 12, or a reached checkpoint as partial win; (e) admin actions: no undo, no «Saltar y quemar para todos», «Reportar pregunta» (burn locally, report list, replacement), «Abandonar partida»; sound, pause.
- `pm decision add`, recommended option first, body = context + trade-offs, ultra-short. Two decisions if one is too big: "Presets, checkpoints and won levels (OQ-30)" and "Admin actions in the default mode (OQ-30)".
- `pm task-pending-decision <record task> <decision id>` for each decision (the record task is the next one in plan 35).

Done when: decision(s) exist, the record task waits on them.', '2026-10-12T00:46:59Z', NULL, 173);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (185, 35, 'Default mode: record the answer (OQ-30, MD-5)', 'work', 'open', NULL, NULL, 'Part 2 of plan 35. Waits for the OQ-30 decision(s) (made pending by the prep task); the answers are in `pm show`.

- D-entry (or two) in `plans/decisions.md`, next free D-number.
- OQ-30 → "Resolved" in `plans/open-questions.md` with the D-number(s).
- `plans/13-game-modes.md` "Default mode": draft table → decided; checkpoints, won levels, admin actions as a spec MD-6/MD-7 can build; settings fields in "Implementation notes" (e.g. `settings.preset`, `settings.checkpoint`); MD-5 `[x]` with a note.
- If presets shift difficulty: note it in plan 21''s age-group section and as input for plan 28 (`pm show`); no change to `age-groups.json`.
- Sync the open-questions row in `plans/11-steam.md` and `plans/project.md`.

Done when: D-entry exists, OQ-30 resolved, MD-5 `[x]`, plan 13''s default-mode section is implementable.', '2026-10-12T00:46:59Z', NULL, 173);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (186, 36, 'Engine: mode, preset, report (MD-6 engine part)', 'work', 'open', NULL, NULL, 'Part 1 of plan 36. Engine rules for the default mode; no UI.

Guards (stop without staging anything):
- `pm show` of plan 35: a pending OQ-30 decision → `pm task-pending-decision <this task> <decision id>`, stop. No decision yet, or record task (MD-5) still open → stop, note why; the spec is plan 13''s default-mode section.
- `engine/game.ts`, `engine/api.ts`, `engine/state.ts` (plan 20, PORT-3) or part 4''s store with `version` + migration (PORT-4/5) missing → stop, leave open, say which.

Work:
- `engine/state.ts`: `settings.mode: "gamemaster" | "default"` (missing = `"gamemaster"` in `withDefaults`), `settings.preset`, checkpoint fields per plan 13; `ReportRow {question_id, game_id, player_id, level, reported_on, note?}`; `SaveData.reports`; version bump + migration step (`reports: []`, games untouched).
- Preset table: one engine constant, plan 13''s decided table.
- `engine/game.ts` / `api.ts`: `newGame` takes `mode` / `preset`, fills `settings.jokers`; `report` action = skip-for-everyone path (`BurnRow` `player_id: null`, replacement at the same level, same supply check) + `ReportRow`; no undo of a report.
- Refusals (`409` + reason): default mode → `undo`, skip for everyone, `setJokers`; gamemaster mode → `report`.
- Checkpoint and won-level rules if plan 13 specifies them.
- `view` exposes `settings.mode` / `preset`; `lib/types.ts` to match.

Check: `npm test` (fixture replay unchanged), `npm run check`; throw-away script: default-mode game, report burns for everyone, replacement at the same level, row in `reports`, undo / skip-everyone / setJokers refused, report in gamemaster mode refused, empty supply → `409`.

Done when: checks pass; gamemaster-mode games behave exactly as before.', '2026-10-12T00:47:35Z', NULL, 174);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (187, 36, '«Reportar pregunta» and the report list (MD-6 UI)', 'work', 'open', NULL, NULL, 'Part 2 of plan 36. Overlay by mode, confirm step, report list screen.

Guards: part 1 of plan 36 still open → stop, leave open. Screens not on the engine yet (M2 part 5, PORT-7) → stop, leave open, say so.

Work:
- `Overlay.svelte`: gamemaster mode exactly as today; default mode: sound, «Reportar pregunta», «Preguntas reportadas», «Abandonar partida», read-only preset line; no undo, skip/burn, budget editor.
- Confirm step: «¿Reportar esta pregunta? Se quema para todos.», Enter/Esc.
- `Reports.svelte` (new): newest first; date, question id, question text, answer, player; «Copiar» → plain text (one block per report) via `navigator.clipboard`, selectable `<pre>` fallback. Offline; no server route.
- `Game.svelte`: `Screen` gains `"reports"`, back with Backspace/Esc; `lib/api.ts` `report`.
- Strings via `t()` (`report.*`); without `lib/i18n.ts`, Spanish literals marked `// LUI-1`.

Check: browser walk in both modes (gamemaster overlay unchanged; default: report → confirm → new question at the same level, list shows it, copy works); keyboard only and mouse only (IN-1); `npm run check`.

Done when: checks pass; plan 13 MD-6 `[x]` with a note.', '2026-10-12T00:47:35Z', NULL, 174);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (188, 36, 'Mode and settings screen (MD-7)', 'work', 'open', 380, NULL, 'Part 3 of plan 36. Mode toggle and preset row on plan 29''s Choice screen; no second screen. Priority 380: after plans 29 and 30.

Guards: part 2 of plan 36 or plan 29''s Choice screen still open → stop, leave open, say which.

Work:
- `Choice.svelte`: toggle «Con presentador / Sin presentador» (key `M`) in both modes; preset row only in the default mode (tile per preset: name, joker counts as badges; keys per plan 13, else `F`/`N`/`D`/`E` if free; default preset as decided); `newGame({…, mode, preset})`.
- Preselect mode/preset from the player''s newest game (like the age group); new player / fresh save → `gamemaster`.
- Launch option `?mode=default|gamemaster` presets the toggle.
- Strings via `t()` (`mode.*`) or `// LUI-1` literals.
- Docs: plan 13 MD-7 `[x]` and "Implementation notes" (mode/settings fields as built); `plans/04-ui-tv-display.md` (Choice section, Reports screen, overlay by mode, keys); `directory.md` (new files); `plans/project.md` if MD-6/MD-7 are listed.

Check: Enter straight through on an existing family save plays today''s game; each preset starts with its joker budget; `?mode=default` presets the toggle; keyboard only and mouse only; `npm run check`.

Done when: checks pass, docs updated.', '2026-10-12T00:47:35Z', NULL, 174);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (189, 37, 'Launch languages: gather facts, write the decisions (OQ-31)', 'work', 'open', NULL, NULL, 'Part 1 of plan 37. Prepare the OQ-31 decision(s); no code, no translation.

- Facts (numbers in the decision body, one-line source each):
  - Steam language shares: latest Steam Hardware & Software Survey; "Spanish – Spain" and "Spanish – Latin America" are separate store languages
  - translation cost per language: cost per approved question from `work/*/costs.log` (proxy for translate + re-rate + fact-check + review, 15b) × plan 16 draft (2,000–3,000 per language)
  - pool flavour: approved/total per bundle (`base`, `colombia`) from `authoring/data/questions.json` (`qgen report` or throw-away script); rough count of Colombian vocabulary in a `base` sample ("bombillo", "crispetas", "carro", "celular" …) to size a neutral-Spanish rewrite
  - UI: size of the `es` catalog (plan 21) if it exists; LUI work per language (15a)
- Questions: (a) launch languages: Spanish only (recommended unless facts say otherwise) / Spanish + English / more; (b) Spanish variety: Colombian usage as is under "Spanish – Latin America" / neutral LatAm in `base`, Colombian in `colombia` / neutral + per-variety variants; store languages to tick (LatAm only or Spain too); (c) first post-launch language, if any (decides whether plan 24''s `en` is launch or later work).
- Each option: what it means for OQ-32 (plan 38, content per language) and D-50 (localized names).
- `pm decision add`, recommended option first, body = context + facts + trade-offs, ultra-short. Two decisions if one is too big: "Launch languages (OQ-31)" and "Spanish variety (OQ-31)".
- `pm task-pending-decision <record task> <decision id>` for each decision (the record task is the next one in plan 37).
- Delete throw-away scripts.

Done when: decision(s) exist, the record task waits on them.', '2026-10-12T00:48:02Z', NULL, 175);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (190, 37, 'Launch languages: record the answer (OQ-31, I18N-1)', 'work', 'open', NULL, NULL, 'Part 2 of plan 37. Waits for the OQ-31 decision(s) from the previous task.

- D-entry in `plans/decisions.md` (next free D-number).
- OQ-31 → "Resolved" in `plans/open-questions.md` with the D-number.
- `plans/15-i18n.md`: "Spanish varieties" decided, launch languages stated, I18N-1 `[x]` with a note; drop "stub" status if the model is settled.
- `15a`: LUI-5 names the launch languages (or "none beyond es"); `15b`: QT-6 and intro name the target languages (or "after launch"); `15c`: RG-5 checked against the answer.
- Neutral-Spanish answer: backlog row in `plans/backlog.md` for the `base` rewrite (S4 content work, via pipeline, D-36); no pool edits.
- Plan 24 "Draft en catalog (LUI-3)": English at launch or first later language → keep, one-line note via `pm plan edit 24 --body` if scope changes; no English planned → say so in plan 24, leave dropping it to the gamemaster (mention in done note).
- `plans/11-steam.md` open-questions row and `plans/project.md` in sync (S4 exit wording stays with plan 43).

Done when: D-entry exists; OQ-31 resolved; I18N-1 `[x]`; 15/15a/15b name the launch languages; plan 24 checked.', '2026-10-12T00:48:02Z', NULL, 175);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (191, 38, 'Content target: estimate games per player, write the decision (OQ-32)', 'work', 'open', NULL, NULL, 'Part 1 of plan 38. Prepare the OQ-32 decision; estimate only, no simulation (CT-2, `qgen report --simulate`, is S4). Can start now: use drafts where answers are missing and say so in the body.

- Facts (numbers in the decision body, one-line source each):
  - approved per level (1–15) and per age-group window (D-38, `app/data/age-groups.json`) for `base` today (`qgen report`)
  - D-52''s 5000; D-53''s per-level targets from `authoring/data/targets.json` if present (pm decision 1 answer if given, else draft)
  - per-level draw of a game: 4 shown, ≥ 1 burned per ladder level (D-22, D-27, D-28, D-31)
  - burns per game from the default joker preset: plan 35''s decision if answered, else its draft (12 + Paso + Bájale + Cambiazo + Snipe hits); whether a preset shifts the age-group window
  - launch languages: plan 37''s decision if answered, else "Spanish only" draft; whether a translation counts as a full pool
  - extra-player burn multiplier: plan 41 (OQ-37) if answered, else named as open (target stated for solo play)
- Estimate: games per new player = min over ladder levels of (approved in that level''s window ÷ burns per game at that level), today and at 5000. Throw-away script, deleted after. Name the bottleneck level.
- Options, recommended first: ≥ 30 games per new player in every launch language, ≥ 50 in the primary (16''s draft); a lower bar met by 5000 `base`; a target per age group. State that CT-2 (S4) verifies it.
- Quality bar: point to D-56 and pm decision 2 (spot-check size, agreement rate); no new numbers.
- `pm decision add`, body = context + facts + estimate + trade-offs, ultra-short.
- `pm task-pending-decision <record task> <decision id>` (the record task is the next one in plan 38).

Done when: the decision exists with the estimate; the record task waits on it; no throw-away script left.', '2026-10-12T00:48:28Z', NULL, 176);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (192, 38, 'Content target: record the answer (OQ-32, CT-1)', 'work', 'open', NULL, NULL, 'Part 2 of plan 38. Waits for the OQ-32 decision from the previous task.

- D-entry in `plans/decisions.md` (next free D-number): target per language, the estimate behind it, CT-2 (S4) confirms it.
- OQ-32 → "Resolved" in `plans/open-questions.md` with the D-number.
- `plans/16-content-target.md`: "Target" decided (numbers, per language); "Quality bar" points to D-56; "Where we stand" refreshed; CT-1 `[x]` with a note that CT-2 (S4) confirms it; status no longer stub.
- `plans/project.md` in sync; `plans/11-steam.md` S4 exit names the target if it mentions one.

Done when: D-entry exists; OQ-32 resolved; CT-1 `[x]`; 16''s target section decided.', '2026-10-12T00:48:28Z', NULL, 176);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (193, 39, 'Price model and account holder: facts, options, write the decision(s) (OQ-33)', 'work', 'open', NULL, NULL, 'Part 1 of plan 39. Prepare the OQ-33 decision(s); no code, no contact with Valve or an advisor. Not legal or tax advice: name where a professional must check.

- Facts (numbers in the decision body, one-line source each; Valve''s Steamworks docs first):
  - fees and payout: revenue share 30 % → 25 % above $10 M → 20 % above $50 M; $100 app credit per app (recouped after $1,000 gross); DLC: no app credit; monthly payout threshold and timing; refunds (2 h / 14 days); VAT/sales tax handled by Valve
  - regional pricing: Valve''s recommended price matrix; a USD band in COP/MXN/ARS/EUR (Spanish-speaking markets, plan 37)
  - 5–8 comparable trivia/party games on Steam with price and review count (Jackbox packs incl. Trivia Murder Party, smaller solo trivia titles); which sell DLC question packs
  - free on Steam: wishlists, visibility, refund-free reviews; free + paid DLC (bundles as DLC per D-39/D-49: `colombia`, later bundles) vs paid base + paid DLC
  - account holder: person (individual tax interview, W-8BEN, personal tax return, real name/address to Valve; store Developer/Publisher can be a label) vs company (W-8BEN-E, formation and bookkeeping cost, liability); app transfer between partner accounts (check the doc)
  - advisor questions as text for the gamemaster: country of residence, US withholding under the treaty, VAT/small-business thresholds, whether hobby income needs registration
- Options, recommended first; one decision or two if too big ("Price model (OQ-33)", "Steamworks account holder (OQ-33)"):
  - price: paid, low band ($4.99–$7.99) with regional pricing (recommended unless the facts say otherwise); free; free base + paid DLC bundles; paid base + paid DLC bundles later
  - account: person (recommended for a hobby launch) vs company; what would trigger switching later
- Each option names its consequence for plan 40 (OQ-35: paid + public pool → anyone can copy the content; free → public pool costs nothing) and plan 42 (OQ-45: paid or DLC → "commercial" under Freesound/CC NC; free still counts as distribution).
- `pm decision add`, body = context + facts + trade-offs, ultra-short.
- `pm task-pending-decision <record task> <decision id>` for each decision (the record task is the next one in plan 39).

Done when: the decision(s) exist with facts and sources; the record task waits on each.', '2026-10-12T00:48:50Z', NULL, 177);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (194, 39, 'Price model and account holder: record the answer (OQ-33, PUB-6, PUB-11)', 'work', 'open', NULL, NULL, 'Part 2 of plan 39. Waits for the OQ-33 decision(s) from the previous task.

- D-entry in `plans/decisions.md` (next free D-number): price model and account holder, consequences for OQ-35 (plan 40) and OQ-45 (plan 42), professional checks still owed.
- OQ-33 → "Resolved" in `plans/open-questions.md` with the D-number; `plans/11-steam.md` open-questions row and `plans/project.md` in sync (S5 wording stays with plan 43).
- `plans/17-publishing.md` "Steamworks and store": account bullet decided; PUB-6 rewritten to the holder (person/company, tax form, app credit, advisor check before signup); PUB-11 rewritten to the price model (band, regional pricing, launch discount, DLC pricing if bundles become DLC). Both stay S5, unchecked.
- If bundles become DLC: one row in `plans/backlog.md` (DLC depots/app IDs for bundles, S5, plan 18 SW tasks); no code.

Done when: D-entry exists; OQ-33 resolved; PUB-6 and PUB-11 match the answer and stay unchecked.', '2026-10-12T00:48:50Z', NULL, 177);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (195, 40, 'Licence: facts, options, write the decision(s) (OQ-35)', 'work', 'dropped', NULL, 're-added by task 178 with a corrected body (ordering)', 'Part 1 of plan 40. Prepare the OQ-35 decision(s); no code, no licence files, never contact a lawyer. Not legal advice: name where a professional must check.

- First: OQ-33 (plan 39, task 193 writes its decision(s)). If OQ-33 is not answered yet: gather the facts, then `pm task-pending-decision <this task> <OQ-33 decision id>`, stage nothing permanent and stop; the decision is written once OQ-33 is answered and recorded (D-entry from plan 39).
- Facts (one line each, with source):
  - no licence on GitHub: GitHub ToS lets others view and fork, nothing else
  - code: MIT vs GPL-3.0 vs AGPL vs all rights reserved for a paid Steam game (GPL: anyone may rebuild and redistribute the game; MIT: anyone may ship a closed fork)
  - questions: CC BY-SA 4.0 vs CC BY-NC(-SA) 4.0 vs reserved (SA/BY allow reselling the pool; NC blocks commercial reuse, not copying; short factual questions: thin copyright, the curated set and hints/explanations are the protectable part)
  - AI-drafted text, reviewed by a person: protection uncertain, flag for a professional (link PUB-10)
  - pool size today: approved per bundle (`qgen report`), so the decision says what is at stake
- Options, recommended first; one decision or two if too big ("Licence (OQ-35)", "Is release content public (OQ-35)"):
  - code: MIT (recommended if paid), GPL-3.0, all rights reserved
  - questions: reserved (recommended if paid), CC BY-NC-SA 4.0, CC BY-SA 4.0
  - repo: public code + current pool public, release content (new batches, translations, paid bundles) private (repo or submodule); whole repo public; whole repo private before release
  - each option: effect on the build (`nix build .#app`, packaging step reading a private pool), on D-17 ("pool is public"), on existing forks (already-public content stays copyable as implied)
- Media (plan 26) and fonts (OFL) are never covered by the repo licence; say so in the body.
- Lawyer questions as text for the gamemaster in the body.
- `pm decision add`, body = context + facts + trade-offs, ultra-short.
- `pm task-pending-decision` on the next two tasks of plan 40 (record the answer; licence files) for each decision.

Done when: the decision(s) exist with facts and sources; both follow-up tasks wait on them.', '2026-10-12T00:49:21Z', '2026-10-12T00:49:31Z', 178);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (196, 40, 'Licence: record the answer (OQ-35)', 'work', 'dropped', NULL, 're-added by task 178 with a corrected body (ordering)', 'Part 2 of plan 40. Waits for the OQ-35 decision(s) from the previous task.

- D-entry in `plans/decisions.md` (next free D-number): code licence, question licence, what stays public; professional checks still owed. Amends D-17 if the pool or release content goes private.
- OQ-35 → "Resolved" in `plans/open-questions.md` with the D-number; `plans/11-steam.md` open-questions row and `plans/project.md` in sync.
- `plans/17-publishing.md` "Code and content license": decided. PUB-4 stays open; the next task checks it.
- If release content goes private: one row in `plans/backlog.md` (private content repo/submodule, how `qgen export` and the build find it, S4/S5); no restructuring.

Done when: D-entry exists; OQ-35 resolved; plan files match the answer.', '2026-10-12T00:49:21Z', '2026-10-12T00:49:31Z', 178);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (197, 40, 'Licence files and mentions (PUB-4)', 'work', 'dropped', NULL, 're-added by task 178 with a corrected body (ordering)', 'Part 3 of plan 40. Runs after the previous task (record the answer); waits for the OQ-35 decision(s) too.

- `LICENSE` at the repo root: the code licence''s full text (or an "all rights reserved" notice).
- If the questions differ from the code: separate content licence file (e.g. `LICENSE-content.md`): paths it covers (`authoring/data/`, `app/data/`); media and fonts keep their own licences per file (plan 26, `app/client/public/fonts/OFL-*.txt`).
- `README.md`: short "License" section. `directory.md`: the new file(s).
- `nix build .#app` still builds; `result/` includes the licence file(s) if the licence requires it (check `flake.nix` install step).
- `plans/17-publishing.md`: PUB-4 `[x]` with a note.

Done when: licence file(s) exist, linked from `README.md` and `directory.md`; `nix build .#app` passes; PUB-4 `[x]`.', '2026-10-12T00:49:21Z', '2026-10-12T00:49:31Z', 178);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (198, 40, 'Licence: facts, options, write the decision(s) (OQ-35)', 'work', 'open', NULL, NULL, 'Part 1 of plan 40. Prepare the OQ-35 decision(s); no code, no licence files, never contact a lawyer. Not legal advice: name where a professional must check.

- First: OQ-33 (plan 39, task 193 writes its decision(s)). If OQ-33 is not answered yet: gather the facts, then `pm task-pending-decision` this task and the next two tasks of plan 40 on the OQ-33 decision, stage nothing permanent and stop. The OQ-35 decision is written only once OQ-33 is answered and recorded (D-entry from plan 39).
- Facts (one line each, with source):
  - no licence on GitHub: GitHub ToS lets others view and fork, nothing else
  - code: MIT vs GPL-3.0 vs AGPL vs all rights reserved for a paid Steam game (GPL: anyone may rebuild and redistribute the game; MIT: anyone may ship a closed fork)
  - questions: CC BY-SA 4.0 vs CC BY-NC(-SA) 4.0 vs reserved (SA/BY allow reselling the pool; NC blocks commercial reuse, not copying; short factual questions: thin copyright, the curated set and hints/explanations are the protectable part)
  - AI-drafted text, reviewed by a person: protection uncertain, flag for a professional (link PUB-10)
  - pool size today: approved per bundle (`qgen report`), so the decision says what is at stake
- Options, recommended first; one decision or two if too big ("Licence (OQ-35)", "Is release content public (OQ-35)"):
  - code: MIT (recommended if paid), GPL-3.0, all rights reserved
  - questions: reserved (recommended if paid), CC BY-NC-SA 4.0, CC BY-SA 4.0
  - repo: public code + current pool public, release content (new batches, translations, paid bundles) private (repo or submodule); whole repo public; whole repo private before release
  - each option: effect on the build (`nix build .#app`, packaging step reading a private pool), on D-17 ("pool is public"), on existing forks (already-public content stays copyable as implied)
- Media (plan 26) and fonts (OFL) are never covered by the repo licence; say so in the body.
- Lawyer questions as text for the gamemaster in the body.
- `pm decision add`, body = context + facts + trade-offs, ultra-short.
- `pm task-pending-decision` on the next two tasks of plan 40 (record the answer; licence files) for each decision.

Done when: the decision(s) exist with facts and sources; both follow-up tasks wait on them.', '2026-10-12T00:49:40Z', NULL, 178);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (199, 40, 'Licence: record the answer (OQ-35)', 'work', 'open', NULL, NULL, 'Part 2 of plan 40. Waits for the OQ-35 decision(s) from the previous task.

- D-entry in `plans/decisions.md` (next free D-number): code licence, question licence, what stays public; professional checks still owed. Amends D-17 if the pool or release content goes private.
- OQ-35 → "Resolved" in `plans/open-questions.md` with the D-number; `plans/11-steam.md` open-questions row and `plans/project.md` in sync.
- `plans/17-publishing.md` "Code and content license": decided. PUB-4 stays open; the next task checks it.
- If release content goes private: one row in `plans/backlog.md` (private content repo/submodule, how `qgen export` and the build find it, S4/S5); no restructuring.

Done when: D-entry exists; OQ-35 resolved; plan files match the answer.', '2026-10-12T00:49:40Z', NULL, 178);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (200, 40, 'Licence files and mentions (PUB-4)', 'work', 'open', NULL, NULL, 'Part 3 of plan 40. Runs after the previous task (record the answer); waits for the OQ-35 decision(s) too.

- `LICENSE` at the repo root: the code licence''s full text (or an "all rights reserved" notice).
- If the questions differ from the code: separate content licence file (e.g. `LICENSE-content.md`): paths it covers (`authoring/data/`, `app/data/`); media and fonts keep their own licences per file (plan 26, `app/client/public/fonts/OFL-*.txt`).
- `README.md`: short "License" section. `directory.md`: the new file(s).
- `nix build .#app` still builds; `result/` includes the licence file(s) if the licence requires it (check `flake.nix` install step).
- `plans/17-publishing.md`: PUB-4 `[x]` with a note.

Done when: licence file(s) exist, linked from `README.md` and `directory.md`; `nix build .#app` passes; PUB-4 `[x]`.', '2026-10-12T00:49:40Z', NULL, 178);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (201, 41, 'Multiplayer: facts, options, write the decision(s) (OQ-37)', 'work', 'open', NULL, NULL, 'Part 1 of plan 41. Prepare the OQ-37 decision(s); no code.

- Facts (one line each, with source):
  - Gamepad API pad limit in Chromium/Electron (4 on most platforms); Steam Input / Steam Deck behaviour
  - Remote Play Together: remote input arrives as extra pads, so any per-pad format works online for free (plan 18, SW-13)
  - phones as buzzers: LAN HTTP/WebSocket server in the shell, QR join, Windows firewall prompt, weakens "no network"; Jackbox as reference
  - how comparable party trivia games on Steam handle 2–8 players
- Burn multiplier per format vs. single player (relay ~1×, parallel ladders ~N×, buzzer ~1× per round but more rounds); from today''s approved counts per level (`qgen report`): how many games of N players each format lasts.
- Options, recommended first; one decision, or two if too big ("Competitive format (OQ-37)", "Multiplayer input (OQ-37)"):
  - format: relay ladder on one shared tower (recommended unless the facts say otherwise), parallel ladders, buzzer round; per-player joker budgets (from the plan 35 default preset); "attack" jokers yes/no
  - couch co-op: default mode with several pads + team confirm (majority / any player / captain) vs. no separate co-op (hot-seat the default mode)
  - input: hot-seat with one pad or mouse (recommended baseline), one pad per player up to 4 (+ Remote Play Together), phones as buzzers (LAN server, own later task)
  - mixed age groups (D-38): one window per game (youngest player''s) vs. per-player windows
  - each option: burn multiplier (for plan 38) and shell needs (for plan 34)
- `pm decision add`, body = context + facts + trade-offs, ultra-short.
- `pm task-pending-decision` on the next task of plan 41 (record the answer) for each decision.

Done when: the decision(s) exist with facts and sources; the follow-up task waits on them.', '2026-10-12T00:50:05Z', NULL, 179);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (202, 41, 'Multiplayer: record the answer (OQ-37)', 'work', 'open', NULL, NULL, 'Part 2 of plan 41. Waits for the OQ-37 decision(s) from the previous task.

- D-entry in `plans/decisions.md` (next free D-number): format, co-op rule, input, mixed age groups, burn multiplier, shell needs.
- OQ-37 → "Resolved" in `plans/open-questions.md` with the D-number; `plans/11-steam.md` open-questions row and `plans/project.md` in sync ("Later" phase wording stays with plan 43).
- `plans/13-game-modes.md`: "Competitive mode" stub → the chosen format (players, turn order, win rule, jokers per player, burning and supply rules); "Couch co-op" → the chosen rule. MD-8 and MD-9 rewritten to build exactly that; unchecked, "Later".
- `plans/14-input.md` section 3: the chosen input; IN-7 `[x]` with a note; IN-6 rewritten to match (join screen or hot-seat only), stays "Later". If phones are chosen: one row in `plans/backlog.md` (LAN buzzer page, Later).
- `plans/16-content-target.md`: the burn multiplier line points to the D-entry (plan 38 uses it).

Done when: D-entry exists; OQ-37 resolved; plans 13, 14, 16 match the answer.', '2026-10-12T00:50:05Z', NULL, 179);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (203, 42, 'Renumber the Freesound open question (OQ-45 → next free OQ)', 'work', 'open', NULL, NULL, 'Part 1 of plan 42. Housekeeping only; no code.

- `plans/open-questions.md` uses OQ-45 twice: the open Freesound one (line ~8) and the resolved one belonging to D-42 (line ~25). Give the Freesound one the next free number (OQ-47 as of 2026-10-11; check with `grep -rhoE ''OQ-[0-9]+'' plans | sort -V | uniq | tail`).
- Update every Freesound reference: `plans/open-questions.md`, `plans/23-media-providers.md` (Freesound row), `plans/project.md` (open-questions table), `plans/11-steam.md` if it lists it, milestone 7''s body (`pm milestone set 7 --body -`; outcome line and "Done when"), plan 7''s body and plan 42''s subject/body (`pm plan edit`), any other hit of `grep -rn ''OQ-45'' plans`.
- Leave references meaning D-42''s OQ-45 as they are (e.g. D-42''s context in `plans/decisions.md`).
- Note: editing plan 42''s subject/body queues a new "create tasks for plan 42"; that run only has to confirm the tasks still match.

Done when: each OQ number is used once; every Freesound reference uses the new number.', '2026-10-12T00:50:35Z', NULL, 180);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (204, 42, 'Freesound: facts, options, write the decision', 'work', 'open', NULL, NULL, 'Part 2 of plan 42. Prepare the Freesound decision; no code, no picks, never contact Freesound/UPF.

- Facts (ultra-short, one source line each):
  - Freesound API terms of use and the commercial-licence page: what counts as "commercial use of the API"; whether an internal authoring tool for a paid product counts. CC0/CC BY sound licences themselves allow commercial use (CC BY with credit).
  - Count today: questions with a Freesound pick (`freesound.org` in media URLs, or `provider` once plan 26 lands) in `authoring/data/questions.json` and `app/data/pool.json`, by status (2026-10-11: 2 approved, q-0752, q-1016; masterplan''s 9/6 needs a recount). Share of Freesound among audio picks in the last batches → expected future slots.
  - Per Freesound question: what Commons and the other allowlisted sources (D-45) offer, via a quick review-tool search (`trivia-authoring`, search modal). No picks (D-36).
- Options, recommended first (recommendation from the facts, e.g. replace if the count stays small); each notes its consequence for plan 39 (free vs paid release):
  - (a) Replace the Freesound picks with allowlisted sources before release; drop Freesound from the audio order (`providers.ORDER`) or from release batches.
  - (b) Ask Freesound/UPF: draft a short English email (what the tool does, only CC0/CC BY files ship, no API in the game, expected volume, the question) in the decision body; the gamemaster sends it.
  - (c) Keep Freesound for the family only: tag its picks and exclude them from the Steam media bundle (SW-9, `plans/18-steam-integration.md`); those questions don''t ship or need another pick.
- `pm decision add` (subject names the OQ number from the previous task), body = context + facts + trade-offs, ultra-short; names plan 39 as a dependency.
- `pm task-pending-decision` on the next task of plan 42 (record the answer).

Done when: the decision exists with facts, sources and the email draft; the follow-up task waits on it.', '2026-10-12T00:50:35Z', NULL, 180);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (205, 42, 'Freesound: record the answer', 'work', 'open', NULL, NULL, 'Part 3 of plan 42. Waits for the Freesound decision from the previous task.

- D-entry in `plans/decisions.md` (next free D-number).
- The Freesound OQ → "Resolved" in `plans/open-questions.md` with the D-number; `plans/project.md` and `plans/11-steam.md`''s open-questions row in sync.
- `plans/23-media-providers.md`: Freesound row and the "Which provider for which slot" table match the answer; MP-6 note updated.
- If (a): `pm task add 42` a task that re-picks each Freesound slot through the review tool (search modal, D-36; the gamemaster or `qgen` picks, never by hand in the pool), then removes Freesound from `providers.ORDER`; `qgen validate` passes.
- If (b): `pm task add 42` "send the Freesound email and record the reply", pending on a decision for the gamemaster (`pm task-pending-decision`); the provider stays until the reply.
- If (c): add the exclusion rule to SW-9 in `plans/18-steam-integration.md`.

Done when: D-entry exists; OQ resolved; plan 23 (and the provider order, if (a)) reflect the answer; any follow-up is a task in plan 42.', '2026-10-12T00:50:35Z', NULL, 180);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (206, 43, 'S2 close-out: plans/11-steam.md to the answers (ST-1)', 'work', 'open', NULL, NULL, 'Plan 43 task 1. Brings `plans/11-steam.md` in line with the S2 answers in `plans/decisions.md`. Docs only.

**Guard first:** `pm show` a follow-up task of each of plans 34, 35, 37–42 (e.g. 183, 185, 190, 192, 194, 199, 202, 205). If a decision is still pending: `pm task-pending-decision <this task> <decision id>` and stop. If answered but its record-the-answer task is still open: stop without changes, don''t drop; the queue brings it back. Plan 36 (MD-6, MD-7) is not waited for.

- Freesound question: use the new OQ number from plan 42 (task 203), not OQ-45.
- "Open questions (blocking)" table: each row → answer + D-number (OQ-34, OQ-36 already done); add the Freesound row.
- "Tracks" table: "Steam part starts" / "What it covers" match the answers (shell in 18''s row, languages in 15''s, competitive/co-op format in 13/14''s).
- "Phases": S3 names the chosen shell; S4''s exit names launch languages and the CT-1 target (CT-2 verifies); S5 names price model, account holder, licence files, Freesound outcome; "Later" names the co-op/competitive format.
- Risks: media licensing → Freesound outcome; scope creep → co-op format; others only if an answer changed them.
- ST-1 `[x]` with date and D-numbers; file status `draft` → `agreed`.

Done when: no "open"/"recommended" wording left in `11-steam.md` for OQ-29..OQ-37 or the Freesound question.', '2026-10-12T00:51:05Z', NULL, 181);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (207, 43, 'S2 close-out: indexes and milestones 8–11', 'work', 'open', NULL, NULL, 'Plan 43 task 2, after task 1. Indexes and later milestones in line with the S2 answers. Docs and pm only.

**Guard first:** same as task 1 (`pm show` the record-the-answer tasks of plans 34, 35, 37–42; pending decision → `pm task-pending-decision` and stop; open follow-up → stop without changes). Also stop if task 1 (`11-steam.md`) is still open.

- `plans/project.md`: drop resolved rows from "Open questions"; "Steam track" paragraph: S2 done (D-numbers); tick SW-1, MD-5, I18N-1, CT-1, PUB-4 where ticked in their plan files.
- `plans/README.md`: status column for 13, 15, 15a/15b/15c, 16, 17, 18 (and 23 if changed) to what the files say.
- `plans/open-questions.md`: OQ-29..OQ-37 and the Freesound question (new number) under "Resolved"; nothing left open for S2.
- Milestones 8–11: `pm show` their masterplans (plans 8–11) and bodies. Masterplan "tbd." → nothing. Written and scope changed (shell ≠ Electron, languages, licence files, Freesound replacement) → short dated note via `pm plan edit <id> --body -`. Change a milestone body (`pm milestone set <id> --body -`) only if it names something the answers ruled out; list such changes in the task note.
- Note the state of plan 36 (MD-6, MD-7) in `project.md`; don''t wait for it.

Done when: milestone 7''s "Done when" holds (OQ-29..OQ-37 and the Freesound question resolved in `decisions.md`, later phases in `11-steam.md` match); `qgen validate` unaffected (no data touched).', '2026-10-12T00:51:05Z', NULL, 181);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (208, 8, 'create tasks for plan 8', 'split', 'done', 1000, '2026-10-11, tasks 209–216 (plan tasks for parts 1–8; 209–211 at 690/680/670 to run after OQ-29 prep task 182); no new decisions: OQ-29 comes from task 182, the rest are raised by the part plans', 'Split plan 8 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:52:42Z', '2026-10-12T00:53:44Z', 8);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (209, 8, 'write plan: Desktop shell skeleton (SW-2)', 'plan', 'open', 690, NULL, 'Write the plan for part 1 of the masterplan (plan 8): `pm plan add 8 "Desktop shell skeleton (SW-2)" --priority 480`.

- Needs OQ-29 (plan 34): task 182 adds the decision "Desktop shell (OQ-29)?". If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop. Task priority 690 puts this after task 182 (700).
- Needs PORT-7''s plan (task 59, "Screens on the engine"): the shell loads the client without Python. If that plan doesn''t exist yet, write against the masterplan''s assumption and name the dependency.
- Content: window (fullscreen default, F11 toggle), loads `app/client/dist/` without a server, minimal preload bridge; shell-side resolver for data files and `/media?url=…` (today `app/server/main.py`, `media_cache.py`; see decision 4 on which routes Python keeps); NixOS dev runtime from the flake + `trivia-desktop`.
- Code under `app/` (D-35, e.g. `app/desktop/`); `directory.md`, `plans/19-repo-layout.md`; owner `plans/18-steam-integration.md`.
- Done when (for the plan): tasks fit one worker run each; "whole game with media and sound, no Python process" is the last task''s check.', '2026-10-12T00:53:42Z', NULL, 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (210, 8, 'write plan: File saves (SW-3)', 'plan', 'open', 680, NULL, 'Write the plan for part 2 of the masterplan (plan 8): `pm plan add 8 "File saves (SW-3)" --priority 470`.

- Needs OQ-29 (plan 34, decision "Desktop shell (OQ-29)?"): if pending, make this task pending on it and stop.
- Needs the Store interface + `SaveData` (task 58, plan "Save document, stores and migration", PORT-4/5): `FileStore` implements that interface; read the plan or, if missing, `plans/12-client-engine.md`.
- Content: one JSON file in the shell''s user data folder via the bridge; atomic write (temp + rename) + retry for Windows locks; corrupt/newer-version file → backup, fresh start, message through the catalog (plan 21). Save import of `state/game.json` only if cheap, else `plans/backlog.md`.
- Owner `plans/18-steam-integration.md`.
- Done-when check: throw-away script kills the shell mid-write; save survives.', '2026-10-12T00:53:42Z', NULL, 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (211, 8, 'write plan: Local builds for Windows and Linux (SW-5, SW-6)', 'plan', 'open', 670, NULL, 'Write the plan for part 3 of the masterplan (plan 8): `pm plan add 8 "Local builds for Windows and Linux (SW-5, SW-6)" --priority 460`.

- Needs OQ-29 (plan 34, decision "Desktop shell (OQ-29)?"): builder follows the answer; if pending, make this task pending on it and stop.
- Content: Windows x64 and Linux x64 artefacts (Deck runs Linux); build steps: client build, `qgen validate`, media bundled from the approved cache (~720 MB, no resizing: SW-9 is S5).
- Decisions the plan raises if it can''t settle them from `plans/18-steam-integration.md` (recommended option first): CI with or without media (D-17: media is gitignored); keep SW-6 (GitHub Actions) in S3 or move it to S5.
- Offline start test on clean Windows and non-Nix Linux: a written checklist for the gamemaster, not a worker task that pretends to run it.
- Owner `plans/18-steam-integration.md` ("Builds and depots").', '2026-10-12T00:53:42Z', NULL, 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (212, 8, 'write plan: Action layer and focus navigation (IN-2, IN-3)', 'plan', 'done', 1000, '2026-10-11, pm plan 44, plans/14-input.md', 'Write the plan for part 4 of the masterplan (plan 8): `pm plan add 8 "Action layer and focus navigation (IN-2, IN-3)" --priority 500`.

- Client only; no engine or shell dependency. Read `plans/14-input.md` (IN-1 audit of `keydown` branches in `Game.svelte` and dialogs).
- Content: actions `confirm`, `back`, `menu`, `answer(1..4)`, `joker(name)`, `navigate(dir)` in `app/client/src/lib/` (e.g. `input.ts`); keyboard/mouse → actions; screens listen only to actions. Spatial focus, sky-blue ring (D-29), focus memory per screen, never on the ☰ button by accident.
- Screens from plans 29 and 36 (milestones 5, 7): convert those that exist, note the rule for those that land later.
- Coordinate with PORT-7 (task 59): both touch `Game.svelte`; order the tasks so one doesn''t undo the other.
- No new dependency without a `pm decision`. Family keys unchanged.', '2026-10-12T00:53:42Z', '2026-10-12T00:56:05Z', 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (213, 8, 'write plan: Gamepad input and button glyphs (IN-4, IN-5)', 'plan', 'done', 1000, '2026-10-12, plan 45 (tasks.sql), pm decision 9 (IN-4 design), plans/14-input.md', 'Write the plan for part 5 of the masterplan (plan 8): `pm plan add 8 "Gamepad input and button glyphs (IN-4, IN-5)" --priority 490`.

- Builds on part 4 (action layer). Owner `plans/14-input.md`.
- Content: Gamepad API polling (rAF while connected), standard mapping; D-pad/stick → `navigate`, A/B/Start → `confirm`/`back`/`menu`.
- IN-4 design: answer buttons (A/B/X/Y on the Question screen?) and joker access (bumpers, wheel or focus row). If `plans/14-input.md` doesn''t settle it, add a `pm decision` with a recommendation and make the plan''s implementation tasks pending on it.
- Glyphs follow the last-used device (keyboard, Xbox, PlayStation via `Gamepad.id`); art original or a free set with a clear licence (D-45 style); list sources for the credits (part 7). A glyph pack with code needs a decision.', '2026-10-12T00:53:42Z', '2026-10-12T00:58:28Z', 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (214, 8, 'write plan: Deck layout and controller-only text entry (SW-4)', 'plan', 'done', 1000, '2026-10-11, pm plan 46, plans/14-input.md, plans/18-steam-integration.md', 'Write the plan for part 6 of the masterplan (plan 8): `pm plan add 8 "Deck layout and controller-only text entry (SW-4)" --priority 380`.

- After parts 4–5 and the screen changes of milestones 5–6 (plans 29, 30, 31; check `pm plan list`).
- Content: every screen at 1280×800, 1280×720, 4K sanity; text ≥ 9 px at 800p; fixes in the `--u` system (D-29). Screenshot tool: follow decision 6''s answer (Playwright vs. by hand) if given, else the shell at a fixed window size.
- Player name without a keyboard (on-screen keyboard is S5, SW-8): propose letter picker / preset names / pick existing; `pm decision` if the Player screen changes visibly for the family.
- Owners: `plans/18-steam-integration.md`, `plans/14-input.md`, `plans/04-ui-tv-display.md`.', '2026-10-12T00:53:42Z', '2026-10-12T01:00:26Z', 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (215, 8, 'write plan: Credits screen and generated CREDITS.md (PUB-5)', 'plan', 'done', 1000, '2026-10-11, pm plan 47, plans/17-publishing.md', 'Write the plan for part 7 of the masterplan (plan 8): `pm plan add 8 "Credits screen and generated CREDITS.md (PUB-5)" --priority 400`.

- Needs plan 26 "Licence data in the pool" (fields per media file) and part 5''s glyph sources; its screen uses part 4''s actions. Implementation tasks wait for those; the plan names them.
- Content: generator at build time (in `app/` or the build step, not `authoring/`) from pool licence data + fixed lists (audio `app/client/public/audio/CREDITS.md` incl. Elgar note, fonts, glyphs, Svelte, the shell); code/content licence from plan 40 (OQ-35) if decided. Screen from start screen or ☰ overlay, scrollable with a pad; `CREDITS.md` in the shipped files.
- Owner `plans/17-publishing.md` ("Credits in the game").', '2026-10-12T00:53:42Z', '2026-10-12T01:02:36Z', 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (216, 8, 'write plan: S3 close-out and platform test', 'plan', 'done', 1000, '2026-10-11, pm plan 48 (S3 close-out and platform test), plans/11-steam.md', 'Write the plan for part 8 of the masterplan (plan 8): `pm plan add 8 "S3 close-out and platform test" --priority 140`.

- Last; below plan 43 "S2 close-out" (150).
- Content: gamemaster test checklist (Windows, Linux, Deck; controller only; offline; full game to level 12 or a loss; restart keeps the save); a `pm decision` "S3 test passed?" with the checklist in the body, a task that records the result.
- Docs: `plans/11-steam.md` S3 row; 14, 17, 18 statuses; `plans/project.md`; `plans/README.md`; notes in masterplans 9–11 if S3 changed their scope (SW-6 moved, media bundle).', '2026-10-12T00:53:42Z', '2026-10-12T01:04:03Z', 208);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (217, 44, 'create tasks for plan 44', 'split', 'done', 1000, '2026-10-11, tasks 222–225 for plan 44; no decisions needed', 'Split plan 44 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:56:02Z', '2026-10-12T01:04:38Z', 212);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (218, 45, 'create tasks for plan 45', 'split', 'done', 1000, '2026-10-12, tasks 226–229; 227–229 wait for decision 9', 'Split plan 45 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T00:58:22Z', '2026-10-12T01:05:15Z', 213);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (219, 46, 'create tasks for plan 46', 'split', 'done', 1000, '2026-10-12, tasks 230–231; both wait for decision 9 (via task 228)', 'Split plan 46 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:00:20Z', '2026-10-12T01:05:46Z', 214);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (220, 47, 'create tasks for plan 47', 'split', 'done', 1000, '2026-10-11, tasks.sql: tasks 232-234 for plan 47; no decisions needed', 'Split plan 47 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:02:33Z', '2026-10-12T01:06:23Z', 215);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (221, 48, 'create tasks for plan 48', 'split', 'done', 1000, '2026-10-11, tasks 238 (checklist + decision, prio 150), 236 (record result), 237 (docs close-out); 235 dropped (wrong guard command); no decisions up front: task 238 raises ''S3 test passed?'' once the checklist and build exist', 'Split plan 48 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:03:55Z', '2026-10-12T01:07:19Z', 216);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (222, 44, 'Action layer core; Game, Overlay and Player on actions (IN-2)', 'work', 'open', NULL, NULL, 'Plan 44, task 1; design in the plan body ("Design" → `lib/input.ts`). Client only; never edit `lib/api.ts` or the data flow (PORT-7 coordination).

- New `app/client/src/lib/input.ts`, no dependency: `Action` type (confirm, back, menu, pick n 1–9, joker, navigate dir, replay, flag, new) with `device`; `lastDevice` `$state` (pointerdown = mouse); keymap with per-scope extras (`question`: A–D, joker letters read from `TOKENS`/catalog, never copied, R; `start`: N); scope stack `pushScope({ name, keys, handle, root?, modal? })` → pop; `text` handling (input focused: only Enter/Esc/↑↓ become actions; a letter outside the Player field focuses it); `e.repeat` ignored, first key/click unlocks audio, `busy` drops all but menu/flag, `preventDefault` when handled; `dispatch(action)` export for part 5.
- The single `svelte:window` key listener moves from `Game.svelte` into `input.ts` (or Game calls its handler).
- `Game.svelte`: one scope per screen (start, level, select, correct, wrong, victory) plus global menu/flag; replaces the `overlayOpen`/`dialogOpen()` chain.
- `Overlay.svelte` (menu = close, modal) and `Player.svelte` incl. delete dialog (modal, menu = back) push their own scopes; their `key(e)` exports go.
- Question and Cambiazo keep the raw event via a temporary passthrough scope (removed in task 2).
- Mouse: `onclick` stays; click and action call the same function.

Check: `npm run check`, `npm run build`; throw-away script for key + scope → action; in the browser (`trivia` + `npm run dev -w app/client`) every key of `plans/04-ui-tv-display.md` "Input" on Start, Player, Level, Select, Correct, Wrong, Victory and the overlay does what it did.', '2026-10-12T01:04:36Z', NULL, 217);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (223, 44, 'Question, jokers and Cambiazo on actions (IN-2)', 'work', 'open', NULL, NULL, 'Plan 44, task 2; needs task 1 (`lib/input.ts`).

- `Question.svelte` pushes scopes for answering, armed joker, Paso dialog (modal, pick 1/2), Francotirador (handles navigate itself via `moveTarget`, letters aim), Cambiazo (`CategoryPicker.svelte`: Esc cancel, Backspace back a level, arrows still move over tiles).
- Remove the `key(e)` exports of Question and CategoryPicker and task 1''s passthrough scope.

Check: `npm run check`, `npm run build`; `grep -rn "keydown\|KeyboardEvent" app/client/src` lists only `lib/input.ts`; in the browser every joker (incl. unavailable ones), Paso 1/2, aim with letters and arrows, unlock, replay, submit, flag, undo/skip from the overlay work as before. Mark `IN-2` `[x]` in `plans/14-input.md`.', '2026-10-12T01:04:36Z', NULL, 217);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (224, 44, 'Spatial focus, ring and memory (IN-3)', 'work', 'open', NULL, NULL, 'Plan 44, task 3; design in the plan body ("Focus navigation"). Needs tasks 1–2.

- New `app/client/src/lib/focus.ts`: pure rect function (primary distance + 2 × cross offset, no wrap) plus `navigate(dir)` over candidates in the top scope''s `root` (enabled `button`, `input`, `a[href]`, `[data-focusable]`; never `tabindex="-1"`/`[data-nofocus]`).
- `data-nofocus` on ☰ and flag (stay `tabindex="-1"`); `data-focus-default` on «¡Jugar!»/«Continuar», «Seguir», first card, first answer, «Cancelar» in the delete dialog; `data-focus-id` where index isn''t stable.
- First navigate with nothing focused focuses the default; `confirm` clicks the focused control only if focus came from navigate/Tab, else the screen''s default (Enter as today).
- Ring: sky outline from `theme.css` on every candidate; find out whether `focus({ focusVisible: true })` or a `.nav-focus` class shows it in Chromium and Firefox, use what works.
- Focus memory per scope name, restored when the scope is on top again, cleared on new content; dialogs return focus to their opener.
- Cambiazo: `CategoryPicker.move` uses the helper if it gives the same result. Overlay and Francotirador keep handling navigate themselves.

Check: throw-away script for the rect logic (2×2 answers, 4 cards, Cambiazo grid with disabled tiles); in the browser every screen and dialog plays with arrows + Enter + Esc/Backspace, the ring is visible wherever focus is, Enter without arrows behaves as today.', '2026-10-12T01:04:36Z', NULL, 217);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (225, 44, 'Audit, docs and later screens (IN-3)', 'work', 'open', NULL, NULL, 'Plan 44, task 4; needs tasks 1–3.

- Walk a full game with arrows + Enter + Esc/Backspace only: start → player (new name, delete) → levels → every joker → wrong and victory → overlay (undo, skip, restart, volumes, jokers). Fix what''s missing.
- Plans 29 (Choice screen) and 36 (Reportar pregunta, settings): any of these screens that exists goes on actions and focus; for each that doesn''t, `pm task add <plan> "<screen> on the action layer (IN-2, IN-3)"` with a body pointing to plan 44 and a priority 10 below the task that builds the screen.
- Docs: `plans/04-ui-tv-display.md` "Input" gets the rule (screens listen to actions from `lib/input.ts` and declare a focus default; no `keydown` elsewhere); `plans/14-input.md` IN-3 `[x]`; `directory.md` lists `lib/input.ts` and `lib/focus.ts`; `plans/project.md` in sync.

Done when: every screen and dialog plays with arrow keys + Enter + Esc/Backspace only; the task note lists what the gamemaster should try on the TV at the next game night (family keys unchanged).', '2026-10-12T01:04:36Z', NULL, 217);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (226, 45, 'Gamepad source (IN-4)', 'work', 'open', NULL, NULL, 'Part of plan 45, task 1. Needs plan 44''s tasks 222–225 done (`dispatch`, `Action.device`, `lastDevice`, scopes, `navigate` + focus); if one is open, stop and say so.

- `app/client/src/lib/gamepad.ts` (new, no dependency), per plan 45 "Design":
  - `gamepadconnected`/`gamepaddisconnected` start/stop a `requestAnimationFrame` loop; only `mapping === "standard"` pads (others: one `console.warn`); any pad drives the game.
  - Pure `step(prev, pad) → { next, actions }`; the loop `dispatch`es with `device: "gamepad"`.
  - Mapping: D-pad 12–15 and left stick → `navigate` (dead zone 0.5, release below 0.3, dominant axis); 0 A → `confirm`, 1 B → `back`, 9 Start → `menu`, 3 Y → `replay`, 8 View → `flag`. LB/RB, X, triggers, right stick: not yet (task 2, decision 9).
  - Edges only, no auto-repeat; ignored while `document.hidden` or no window focus; on focus return held buttons don''t fire.
  - `padStyle: "xbox" | "playstation"` (`$state`) from the `id` of the pad that last acted: `/054c|playstation|dualshock|dualsense|wireless controller/i` → playstation, else xbox.
- Start it once from `Game.svelte` (or `main.ts`).
- Audio unlock: check in Chromium whether a pad press counts as user activation. If not: browser keeps today''s hint; add to `plans/18-steam-integration.md` "Desktop shell": the shell sets `autoplayPolicy: "no-user-gesture-required"`.
- Keyboard and mouse unchanged.

Done when: `npm run check`, `npm run build` pass; a throw-away script feeds fake pads to `step` (edges, stick dead zone and hysteresis, no repeat, two buttons at once); tried in Chromium with a pad if available, else the task note lists what the gamemaster should try.', '2026-10-12T01:05:13Z', NULL, 218);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (227, 45, 'Question screen and jokers with the pad (IN-4)', 'work', 'open', NULL, NULL, 'Part of plan 45, task 2. Needs task 1 of this plan and decision 9 (Question screen with a pad).

- Implement decision 9''s answer on the Question screen. Option 1 (recommended): A on a focused answer locks it (`tap`), focus jumps to «Respuesta final» once it is enabled (A, A = lock, submit); B unlocks; LB/RB (4/5) → new action `joker-focus` prev/next (added to plan 44''s `Action` in `input.ts`) moves focus into the joker tray; A arms, A again plays (two-tap arming); B disarms.
- Other options: follow the answer; update plan 45 "Design" first if it changes the mapping, new actions or components.
- Francotirador: `navigate` moves the crosshair, A fires, B cancels. Cambiazo: works with `navigate`/A/B.
- Files: `lib/gamepad.ts`, `lib/input.ts`, `game/Question.svelte`, `game/JokerTray.svelte`, the Cambiazo/Francotirador components as needed. Keyboard and mouse unchanged.

Done when: `npm run check` passes; a throw-away script or Chromium run shows lock → submit, unlock, every joker armed and played, aiming and Cambiazo with pad actions only.', '2026-10-12T01:05:13Z', NULL, 218);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (228, 45, 'Glyphs and prompts (IN-5)', 'work', 'open', NULL, NULL, 'Part of plan 45, task 3. Needs task 1 of this plan and decision 9 (decides whether joker tokens and answer tiles show pad glyphs).

- `app/client/src/game/Glyph.svelte` (new): inline SVG drawn in-house, `Icon.svelte` style (VD-8: rounded, `currentColor`, 24×24). Sets: xbox (A, B, X, Y discs, LB, RB, View, Menu, D-pad), playstation (✕ ○ □ △, L1, R1, Create, Options, D-pad). No console art, no glyph pack; if drawing is clearly worse than a CC0 set (e.g. Kenney "Input Prompts"), stop and add a pm decision instead of switching.
- `app/client/src/game/Prompt.svelte` (new): `<Prompt action="confirm" />`; keyboard/mouse → today''s `<kbd>` text from `input.ts`''s keymap (one copy), gamepad → `<Glyph>` of `padStyle`; actions without a pad binding render nothing with a pad. Device = `lastDevice`; mouse counts as keyboard. Same size as today''s `kbd` chips, instant switch.
- Replace every `<kbd>` in `app/client/src/game/*.svelte` (Game, Question, Player, CategoryPicker, JokerTray, Overlay) and the joker tokens'' `.key` letter (hidden with a pad unless decision 9 binds jokers to buttons). Answer tiles keep A–D unless decision 9 picks option 2.
- `plans/17-publishing.md` "Controller glyphs": "original, drawn for the game (`Glyph.svelte`)".

Done when: `npm run check` passes; screenshots of Start, Question (armed joker, Paso, aiming) and Cambiazo with `lastDevice` forced to keyboard, xbox and playstation (throw-away flag or devtools) show no layout shift.', '2026-10-12T01:05:13Z', NULL, 218);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (229, 45, 'Pad audit and docs (IN-4, IN-5)', 'work', 'open', NULL, NULL, 'Part of plan 45, task 4. Runs after tasks 1–3 of this plan.

- Walk a full game with a pad only: start → existing player → levels → every joker incl. unavailable ones → wrong and victory → overlay incl. undo, skip, volumes; fix what''s missing. New player names are plan 46 (SW-4), not here.
- Screens from plans 29/36 (Choice, settings, report), if they exist: `<Prompt>` instead of `<kbd>`.
- Docs: `plans/14-input.md` IN-4/IN-5 `[x]`; `plans/04-ui-tv-display.md` "Input": prompts through `<Prompt>`, no raw `<kbd>`; `directory.md`: `lib/gamepad.ts`, `Glyph.svelte`, `Prompt.svelte`; `plans/project.md`.
- Task note: steps for the gamemaster''s check in Chromium on Linux and Windows with an Xbox-style pad.

Done when: `npm run check`, `npm run build` pass; the walk-through finds no screen a pad can''t operate; keyboard and mouse behave as before.', '2026-10-12T01:05:13Z', NULL, 218);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (230, 46, 'Letter picker for player names with a pad (SW-4, IN-4)', 'work', 'open', NULL, NULL, 'Task 1 of plan 46 ("Letter picker" in Design). A new player name can be typed with a pad only; keyboard and mouse see today''s Player screen unchanged.

- Needs plan 44 (actions, focus, dialog scope) and plan 45 (`lib/gamepad.ts`, `<Prompt>`, `lastDevice`; task 228). If missing: stop, say so in the note, leave open. Waits for decision 9 because task 228 does.
- `app/client/src/game/LetterPicker.svelte` (new): modal dialog, glass panel like the delete dialog; name as typed above the grid; 9 columns `A`–`Z`, `Ñ`, `Á É Í Ó Ú Ü`, `-`, row «Espacio», «⌫ Borrar», «Listo». Plan 44''s spatial focus, default «A».
- Hook in `Player.svelte`: opens on gamepad `confirm` with the name field focused, or via the field''s pad prompt «Ⓐ Escribir» (`<Prompt action="confirm">`, only when `lastDevice` is the pad).
- Auto-capital helper (pure function): first letter and the one after space or `-` upper case, rest lower case; same `typed` cleanup, `maxlength` 30.
- Pad: A types; B deletes last letter, closes on empty name; Start closes; «Listo» = `onchoose(typed)`, disabled while empty; closing keeps the text. Mouse clicks on keys; physical letters/`Backspace`/`Enter`/`Esc` while open.
- Strings «Escribir», «Espacio», «Borrar», «Listo», «Escribe tu nombre»: `t()` (`picker.*`) if `lib/i18n.ts` exists, else literals marked `// LUI-1`.
- No new dependency.

Check: `npm run check`, `npm run build`; throw-away script for the helper («ana sofía» → «Ana Sofía», «-», «ñ», 30-char limit); in Chromium with a pad (or forced `device: "gamepad"`): new player created pad-only, B deletes, Start closes and keeps text, mouse clicks work; keyboard: no picker, no new prompt.

Docs: `plans/04-ui-tv-display.md` "Player", `directory.md` (`LetterPicker.svelte`), `plans/14-input.md` Steam Deck paragraph ("in-game letter picker, plan 46"), one line in `plans/18-steam-integration.md` "Steamworks" (SW-8 `ShowFloatingGamepadTextInput` may replace the picker under Steam; picker stays the fallback).', '2026-10-12T01:05:44Z', NULL, 219);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (231, 46, 'Screen check at 1280×800, 1280×720 and 4K, fixes (SW-4)', 'work', 'open', 370, NULL, 'Task 2 of plan 46 ("Size rule", "Check sizes", "What to look for", "Screens and states", "Screenshots" in Design). Runs after the letter picker task so the picker is checked.

- Needs: letter picker (task 1 of plan 46), plan 45 glyphs (task 228), and the final screen set: plans 29, 30, 31 (`Placeholder.svelte` gone), 36. Screenshots: Playwright (throw-away, temp dir) if pm decision 6 says so, else a throw-away Electron main script on the desktop shell (plan 34). If something is missing: stop, say so in the note, leave open.
- Every screen and state from the plan at 1280×800, 1280×720, 1920×1080, 3840×2160, with keyboard prompts and with Xbox glyphs; long content picked from `app/data/pool.json` by script, 9 names of 30 chars, long supply report, error box. Script prints every element with computed `font-size` < 9 px. PNGs in a temp dir, not the repo.
- Fixes only in `--u` multiples (at least `.credit` in `Question.svelte` 0.8 → 0.9); no media query, no Deck layout; no `px`/`rem` font sizes in `app/client/src/game/`. Repeat until the small-text report is empty and nothing clips or leaves the safe area at 720p.

Check: 1080p screenshots before/after differ only at intended fixes (ImageMagick `compare`); 4K sane.

Docs: size rule in `plans/10-visual-design.md` (type scale) and `plans/04-ui-tv-display.md` "Implementation notes"; `plans/18-steam-integration.md` SW-4 `[x]` with note (sizes, tool, fixes); `plans/14-input.md` Deck paragraph; `plans/project.md` in sync. Task note lists what to check on a real Deck (Linux build, Game Mode, built-in controls only) for part 8''s checklist (plan 48).', '2026-10-12T01:05:44Z', NULL, 219);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (232, 47, 'Licence fields in the export and the credits generator (PUB-5)', 'work', 'open', NULL, NULL, 'Part 1 of plan 47 ("Data for the generator", "Generator: a Vite plugin"). Build-time credits from `app/data/pool.json` plus fixed lists; no screen yet.

**Precondition:** plan 26''s task 113 (licence migration, validate errors) is done (`pm show 113`). If not, stop and say so in the run output; don''t work around it.

- `authoring/tools/pool_export.py`: add `provider`, `license`, `license_url`, `author`, `author_url` to `MEDIA_PLAY_FIELDS` and `BACKGROUND_PLAY_FIELDS` (not `restrictions`, `pd_reasons`). `qgen export`, `qgen validate` green.
- `app/client/credits.ts` (new, TypeScript, no dependency), used in `app/client/vite.config.ts`:
  - build: emits `credits.json` and `CREDITS.md` at the root of `dist/`; dev: `configureServer` middleware serves `/credits.json` from the same function.
  - Media: one entry per distinct `file_url` across `media` and `background` of all questions; fields kind, title (Commons `File:` name without extension, URL-decoded; else last path segment of `source_url`), author (`author` → `credit`''s author part → «Autor desconocido»), `author_url`, `license`, `license_url`, `source_url`, provider. Sorted by kind, then title.
  - Build fails (ids listed) when a slot lacks `license` or `source_url`; warns for GFDL.
  - Sounds: parsed from `app/client/public/audio/CREDITS.md`; fail if a row doesn''t parse or an `.m4a` in `public/audio/` has no row; Elgar note line (composition PD, Elgar † 1934; recording US Marine Band, US government work).
  - Fonts: Baloo 2, Nunito, SIL OFL 1.1, linking `fonts/OFL-*.txt`.
  - Controller glyphs: «original, dibujados para el juego» only if `src/game/Glyph.svelte` exists.
  - Libraries: Svelte, version/licence from `node_modules/svelte/package.json`, full `LICENSE.md` text into `CREDITS.md`. No build tools.
  - Game: `LICENSE` / content licence file from the repo root only if present (plan 40); else no section.
  - `CREDITS.md` in English: intro (licences per file; CC BY-SA adaptations such as blurred backgrounds (D-15) and crops under the same licence), sections Game, Media in the questions (table), Sounds, Fonts, Controller glyphs, Libraries.
- `plans/18-steam-integration.md` "Desktop shell": one line — whoever adds the shell adds its entry (e.g. Electron MIT + Chromium licence file) to the generator.
- Docs: `directory.md` (`credits.ts`, generated `credits.json`/`CREDITS.md`); `plans/19-repo-layout.md` if it lists client build files.

Check: `npm run build` → `dist/credits.json`, `dist/CREDITS.md`; throw-away script: every distinct `file_url` in pool.json appears once with author, licence, source link; every `.m4a` listed; a temp pool copy with one `license` removed fails the build. `nix build .#app` contains `CREDITS.md`. `npm run check`.', '2026-10-12T01:06:21Z', NULL, 220);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (233, 47, 'Credits screen (PUB-5)', 'work', 'open', NULL, NULL, 'Part 2 of plan 47 ("Credits screen"). After this plan''s task 1 and plan 44''s tasks (222–225); priority order puts it there. If `credits.json` isn''t generated yet or plan 44''s action layer (`navigate`, `back`, scopes) is missing, stop and say so.

- `app/client/src/game/Credits.svelte` (new); overlay item «Créditos» in `Overlay.svelte` `items`, left column, below «Pantalla completa». No change to the start screen.
- Fetches `credits.json` with a relative URL on first open, keeps it in memory; error line on failure.
- Full-screen glass panel over the current screen; section headings with counts; one row per entry: title, author, licence, provider; source URL as small text, not a link.
- Input via plan 44: own scope; `navigate` up/down scrolls ~70 % of the panel, left/right jump to previous/next section; `back` (Esc, Backspace, pad B) and `menu` close it back to the overlay; wheel and scrollbar work. No focusable rows.
- Text ≥ 9 px at 1280×800 in the `--u` system (D-29); rows `content-visibility: auto`.
- Strings via `t()` if `app/client/src/lib/i18n.ts` exists (plan 21), else Spanish literals marked `// LUI-1`.

Check: `npm run check`; screenshots at 1920×1080 and 1280×800 (top, middle of media list, sounds); keyboard (arrows, Esc) and mouse (wheel, close button) in Chromium; a pad (D-pad, B) if plan 45''s task 226 is done, else list the pad steps for the gamemaster in the done note. Family keys and other overlay items behave as before.', '2026-10-12T01:06:21Z', NULL, 220);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (234, 47, 'Credits docs and close-out (PUB-5)', 'work', 'open', NULL, NULL, 'Part 3 of plan 47. After this plan''s task 2.

- `plans/17-publishing.md` "Credits in the game": how it works (generator `app/client/credits.ts`, Credits screen, `CREDITS.md` in `dist/`); PUB-5 `[x]` with a note.
- `plans/04-ui-tv-display.md`: overlay item «Créditos», Credits screen. `plans/05-gamemaster-controls.md` if it lists the overlay items.
- `plans/18-steam-integration.md` "Builds and depots": part 3 also copies `CREDITS.md` to the artefact root.
- `plans/project.md` in sync.

Done when: the plan files describe the shipped state; plan 47''s "Done when" holds (check `dist/CREDITS.md`, `nix build .#app`).', '2026-10-12T01:06:21Z', NULL, 220);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (235, 48, 'S3 platform test: checklist and the test decision', 'work', 'dropped', NULL, 'guard named a wrong command (pm show 48); replaced by the next task', 'Plan 48 task 1. Writes the S3 platform test checklist and hands it to the gamemaster as a pm decision. Docs and pm only; no code. Workers own no Windows machine or Deck: never fill a result yourself.

**Guard first:** `pm show 48`''s milestone lists its plans; `pm plans list`. If any other milestone-8 plan still has open tasks (plans 8, 44–47, and the plans written by tasks 209 desktop shell SW-2, 210 file saves SW-3, 211 local builds SW-5/SW-6): if one of them waits for a pending decision, `pm task-pending-decision <this task> <that decision>` and stop; otherwise stop without changes and say so (the queue brings the task back). Never drop tasks of other plans.

- `plans/18-steam-integration.md`: new section "S3 platform test" after "Steam Deck Verified". Intro (build commit, date, artefact names), then one table per platform (check | result | note), results empty:
  - Windows x64 (clean machine, no Node/Python); Linux x64 without Nix; Steam Deck in Game Mode (Linux build as a non-Steam game, built-in controls only); optional row "Windows build on the Deck via Proton (if cheap)".
  - Rows per platform as in plan 48 "The checklist": offline; start/fullscreen toggle; controller only (new player via letter picker, existing player, play to 12 or a loss); every joker incl. Paso, Francotirador, Cambiazo both levels, ☰ via Start, B closes every dialog; glyphs (Xbox, PlayStation if at hand, keyboard switch and back); media (image, video, audio, music, sounds); credits opens and scrolls with the pad; save after quit and after force-quit; Deck only: 800p readability, nothing cut off, suspend/resume mid-question.
  - One "Family check" table: `trivia` + browser on the TV with keyboard plays a round; `state/` intact.
  - Reuse, don''t copy: link or merge the offline start checklist of the local-builds plan (task 211); turn the "what the gamemaster should try" items from the task notes of plans 45 and 46 (`pm show` their tasks; plan 46 task 3: real Deck in Game Mode) into rows.
- Run what a worker can and note it in the intro: artefacts from one commit (the local-builds plan''s build command), `qgen validate` clean, `trivia-media sync --status approved` before the build, `CREDITS.md` in the artefact. A failure here: note it, `pm task add` in the owning plan, stop without the decision.
- `did=$(pm decision add "S3 test passed?" --body - --option "passed" --option "passed with minor issues (list them; they go to the backlog)" --option "failed (list the failing rows)")`, body: the whole checklist (tables as Markdown, build commit, artefact names) and how to report (copy the tables, fill result and note; "skipped" needs a reason).
- `pm task-pending-decision` for plan 48''s tasks 2 and 3 on `did`.

Done when: the section exists, the decision is pending, tasks 2 and 3 wait for it.', '2026-10-12T01:07:02Z', '2026-10-12T01:07:16Z', 221);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (236, 48, 'S3 platform test: record the result', 'work', 'open', NULL, NULL, 'Plan 48 task 2, after task 1; waits for the decision "S3 test passed?" (or a later "S3 re-test passed?"). Docs and pm only; no code.

**Guard first:** as in task 1 (other milestone-8 plans with open tasks → pending decision or stop without changes). If the decision isn''t answered yet, `pm task-pending-decision <this task> <its id>` and stop.

- Copy the reported results into the tables of "S3 platform test" in `plans/18-steam-integration.md` (date, build commit). Never fill a row the gamemaster didn''t report.
- D-entry in `plans/decisions.md` only if the answer settles something (e.g. Proton row dropped for good).
- `passed`: done.
- `passed with minor issues`: each issue into `plans/backlog.md` with the owning plan file''s task ID prefix (SW-, IN-, PUB-); done.
- `failed`: per failing row `pm task add <owning plan>` (shell/saves/builds plans from tasks 209–211, or 44–47) with the row, the note and how to reproduce, at that plan''s priority (no `--priority`). Then `did=$(pm decision add "S3 re-test passed?" …)` with only the failed rows plus the full-game row, same options; `pm task-pending-decision` for this task and task 3 on it; stage and stop without closing. Repeat until passed.

Done when: the section shows a passing result for every non-optional row.', '2026-10-12T01:07:02Z', NULL, 221);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (237, 48, 'S3 close-out: plan files, indexes and later masterplans', 'work', 'open', NULL, NULL, 'Plan 48 task 3, after task 2 (waits for the same decision). Docs and pm only; no code.

**Guard first:** stop without changes if task 2 is still open; pending decision → `pm task-pending-decision <this task> <its id>` and stop.

- `plans/11-steam.md`: S3 row done (date, link to "S3 platform test"); ST-4 (release checklist) notes it starts from the S3 checklist.
- `plans/14-input.md`, `17-publishing.md`, `18-steam-integration.md`: IN-2..IN-5, PUB-5, SW-2..SW-6 ticked with notes (check, don''t redo, the parts'' own ticks); status lines up to date (`stub` → `draft`, or `agreed` where everything for S3 is decided); `plans/README.md` status column to match.
- `plans/project.md`: "Steam track" paragraph says S3 done (date); tasks ticked in their plan files ticked here too; open-questions rows S3 resolved removed.
- Masterplans 9–11 (S4–S6, `pm show` a task of each): "tbd." → nothing. Written and S3 changed their scope (SW-6 CI moved to S5, media bundle size or depot layout, Proton/Deck findings for SW-12, letter picker vs. on-screen keyboard for SW-8) → short dated note via `pm plan edit <id> --body -`. Milestone bodies (`pm milestone set <id> --body -`) only if they name something S3 ruled out; list such changes in the task note.
- Don''t set milestone 8''s status (pm''s post-milestone cleanup does).

Done when: milestone 8''s "Done when" holds and is cited in the task note (decision id, date); `qgen validate` unaffected.', '2026-10-12T01:07:02Z', NULL, 221);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (238, 48, 'S3 platform test: checklist and the test decision', 'work', 'open', 150, NULL, 'Plan 48 task 1 (priority 150: before tasks 2 and 3 of the plan). Writes the S3 platform test checklist and hands it to the gamemaster as a pm decision. Docs and pm only; no code. Workers own no Windows machine or Deck: never fill a result yourself.

**Guard first:** `pm show <this task>` (lists milestone 8''s plans) and `pm plans list`. If any other milestone-8 plan still has open tasks (plans 8, 44–47, and the plans written by tasks 209 desktop shell SW-2, 210 file saves SW-3, 211 local builds SW-5/SW-6): if one of them waits for a pending decision, `pm task-pending-decision <this task> <that decision>` and stop; otherwise stop without changes and say so (the queue brings the task back). Never drop tasks of other plans.

- `plans/18-steam-integration.md`: new section "S3 platform test" after "Steam Deck Verified". Intro (build commit, date, artefact names), then one table per platform (check | result | note), results empty:
  - Windows x64 (clean machine, no Node/Python); Linux x64 without Nix; Steam Deck in Game Mode (Linux build as a non-Steam game, built-in controls only); optional row "Windows build on the Deck via Proton (if cheap)".
  - Rows per platform as in plan 48 "The checklist": offline; start/fullscreen toggle; controller only (new player via letter picker, existing player, play to 12 or a loss); every joker incl. Paso, Francotirador, Cambiazo both levels, ☰ via Start, B closes every dialog; glyphs (Xbox, PlayStation if at hand, keyboard switch and back); media (image, video, audio, music, sounds); credits opens and scrolls with the pad; save after quit and after force-quit; Deck only: 800p readability, nothing cut off, suspend/resume mid-question.
  - One "Family check" table: `trivia` + browser on the TV with keyboard plays a round; `state/` intact.
  - Reuse, don''t copy: link or merge the offline start checklist of the local-builds plan (task 211); turn the "what the gamemaster should try" items from the task notes of plans 45 and 46 (`pm show` their tasks; plan 46 task 3: real Deck in Game Mode) into rows.
- Run what a worker can and note it in the intro: artefacts from one commit (the local-builds plan''s build command), `qgen validate` clean, `trivia-media sync --status approved` before the build, `CREDITS.md` in the artefact. A failure here: note it, `pm task add` in the owning plan, stop without the decision.
- `did=$(pm decision add "S3 test passed?" --body - --option "passed" --option "passed with minor issues (list them; they go to the backlog)" --option "failed (list the failing rows)")`, body: the whole checklist (tables as Markdown, build commit, artefact names) and how to report (copy the tables, fill result and note; "skipped" needs a reason).
- `pm task-pending-decision` for tasks 236 (record the result) and 237 (close-out) on `did`.

Done when: the section exists, the decision is pending, tasks 236 and 237 wait for it.', '2026-10-12T01:07:16Z', NULL, 221);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (239, 9, 'create tasks for plan 9', 'split', 'done', 1000, '2026-10-11, tasks 240–251 (plan-writing for parts 1–12); task 241 waits on decision 2', 'Split plan 9 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:09:32Z', '2026-10-12T01:10:59Z', 9);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (240, 9, 'write plan: Simulation: games per new player (CT-2)', 'plan', 'open', 490, NULL, 'Write the plan for part 1 of the masterplan (plan 9): `pm plan add 9 "Simulation: games per new player (CT-2)" --priority 570`.

- Needs the answers to OQ-32 (plan 38, tasks 191/192), OQ-30 (plan 35, tasks 184/185), OQ-37 (plan 41, tasks 201/202) and OQ-31 (plan 37, tasks 189/190). Any of those decisions still pending: `pm task-pending-decision <this task> <its id>` for each, stage nothing, stop. Task priority 490 puts this after all four decision tasks.
- Needs the TS engine (plans 19, 20) and group windows + bundle filter (plan 27): if their code isn''t done, write against their plans and name the dependency; no second referee in Python; the plan decides the small Node adapter if needed.
- Content: `qgen report --simulate [--locale] [--bundles] [--age-group] [--preset] [--players] [--seeds]`; median, 10th percentile, strong-player bound, bottleneck level/subcategory; pass/fail per launch language, default bundle set, every age group; exit 1 on fail.
- Owner `plans/16-content-target.md` ("Metric"); feeds parts 9 and 12.', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (241, 9, 'write plan: Release quality bar and back-audit (CT-5)', 'plan', 'open', 610, NULL, 'Write the plan for part 2 of the masterplan (plan 9): `pm plan add 9 "Release quality bar and back-audit (CT-5)" --priority 640`.

- Waits for decision 2 (D-56''s spot-check size and agreement rate); linked by task 239. Task priority 610 puts this after plan 16''s tasks (46, 47, 49), which build `qgen audit` and the spot-check tooling.
- Content: release bar = D-56''s numbers, or stricter (then a pm decision with a recommendation); error limit and what happens to a batch above it; back-audit of the pre-D-56 approved pool in slices through `qgen` (gamemaster asks, like `qgen rework`), findings → `/review?audit=flagged`; cost estimate from `costs.log` first, as a pm decision before the full run.
- Owner `plans/16-content-target.md` ("Quality bar").', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (242, 9, 'write plan: Translation layout and schema (QT-1, I18N-3)', 'plan', 'open', 490, NULL, 'Write the plan for part 3 of the masterplan (plan 9): `pm plan add 9 "Translation layout and schema (QT-1, I18N-3)" --priority 890`.

- Needs OQ-31 (plan 37): task 189 writes the decision "launch languages", task 190 records it (D-entry, I18N-1). If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- OQ-31 = Spanish only: `pm task drop <this task> "OQ-31: Spanish only"`.
- Content: draft preference A (`authoring/data/questions.<locale>.json`, same ids, translated fields + own `difficulty`, `status`, `review`, `source_hash` → `stale`); `translatable: false` on sources; translated category/subcategory/bundle names; `qgen export` → `app/data/pool.<locale>.json` + names (D-35); `qgen validate` checks; D-entry for the layout.
- After plan 26 (licence fields, priority 900), which also changes pool fields.
- Owner `plans/15b-question-translation.md` ("Storage"), `plans/15-i18n.md` (I18N-3).', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (243, 9, 'write plan: Spanish variety (neutral Spanish)', 'plan', 'open', 490, NULL, 'Write the plan for part 8 of the masterplan (plan 9): `pm plan add 9 "Spanish variety (neutral Spanish)" --priority 690`.

- Needs OQ-31 (plan 37): task 189 writes the decision "launch languages", task 190 records it (D-entry, I18N-1). If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- OQ-31 keeps Colombian Spanish: `pm task drop <this task> "OQ-31: Colombian Spanish stays"`.
- Content: a `qgen batch` mode (e.g. `--neutralize`) that rewrites Colombian wording in `base` to neutral Latin American Spanish, through review and D-56''s QC; `colombia` keeps its wording; prompt drafted, approved by the gamemaster (pm decision); RUNBOOK + D-36 amended. The runs go to part 11.
- Owner `plans/15-i18n.md` ("Spanish varieties").', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (244, 9, 'write plan: Translation pipeline (QT-2, QT-3)', 'plan', 'open', 480, NULL, 'Write the plan for part 4 of the masterplan (plan 9): `pm plan add 9 "Translation pipeline (QT-2, QT-3)" --priority 700`.

- Needs OQ-31 (plan 37): task 189 writes the decision "launch languages", task 190 records it (D-entry, I18N-1). If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- OQ-31 = Spanish only: `pm task drop <this task> "OQ-31: Spanish only"`.
- Needs part 3''s plan ("Translation layout and schema"): build on its layout; if it was dropped or isn''t written, stop the same way on its task.
- Content: `translate --to L` → `rate --locale L` → `factcheck --locale L` → review (D-32/D-33) → audit (D-56) → merge; only approved, translatable sources; `costs.log`; entry point `qgen batch --translate L`; RUNBOOK + D-36 amended; new prompts drafted, approved by pm decision.
- Owner `plans/15b-question-translation.md` ("Pipeline").', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (245, 9, 'write plan: Review tool for translations (QT-4)', 'plan', 'open', 470, NULL, 'Write the plan for part 5 of the masterplan (plan 9): `pm plan add 9 "Review tool for translations (QT-4)" --priority 400`.

- Needs OQ-31 (plan 37): task 189 writes the decision "launch languages", task 190 records it (D-entry, I18N-1). If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- OQ-31 = Spanish only: `pm task drop <this task> "OQ-31: Spanish only"`.
- Content: `/review?batch=…&locale=L` with source and translation side by side; same verdicts; media with visible text flagged per locale; blind spot-check sample mode per locale (reuse plan 16''s, task 47); stats pages filter by locale. `authoring/ui`, `authoring/server`.
- Owner `plans/15b-question-translation.md` ("Review tool").', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (246, 9, 'write plan: Language setting and per-locale pool (I18N-2)', 'plan', 'open', 470, NULL, 'Write the plan for part 6 of the masterplan (plan 9): `pm plan add 9 "Language setting and per-locale pool (I18N-2)" --priority 480`.

- Needs OQ-31 (plan 37): task 189 writes the decision "launch languages", task 190 records it (D-entry, I18N-1). If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- OQ-31 = Spanish only: `pm task drop <this task> "OQ-31: Spanish only"`.
- Builds on plan 36 (settings screen, task 188) and part 3''s export (`pool.<locale>.json` + names).
- Content: UI and question language in `SaveData`, default from `navigator.language`; on the settings screen; engine loads the locale''s pool; burns by id; names from the locale; supply check per locale. Family: `es` fixed, gamemaster mode unchanged.
- Owner `plans/15-i18n.md` ("Model").', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (247, 9, 'write plan: UI catalogs for the launch languages (LUI-4, LUI-5)', 'plan', 'open', 470, NULL, 'Write the plan for part 7 of the masterplan (plan 9): `pm plan add 9 "UI catalogs for the launch languages (LUI-4, LUI-5)" --priority 390`.

- Needs OQ-31 (plan 37): task 189 writes the decision "launch languages", task 190 records it (D-entry, I18N-1). If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- OQ-31 = Spanish only: `pm task drop <this task> "OQ-31: Spanish only"`.
- Builds on plans 21, 23, 24 (`t()`, `xx`, draft `en`) and plan 45 (gamepad glyphs).
- Content: LUI-4 joker keys per language or neutral (pm decision with a recommendation); LUI-5 catalog per launch language, joker names per language (pm decision per joker, like plan 24), fonts, `xx` length check, `/comodines` per language, native-speaker playtest (checklist + pm decision "playtest passed?"). LUI-6 is S5: note it in 15a, don''t plan it.
- Owner `plans/15a-ui-translation.md`.', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (248, 9, 'write plan: Cost, budget and generation plan by gap (CT-3, CT-4)', 'plan', 'open', 470, NULL, 'Write the plan for part 9 of the masterplan (plan 9): `pm plan add 9 "Cost, budget and generation plan by gap (CT-3, CT-4)" --priority 560`.

- Needs part 1''s plan (simulation, its bottleneck output): if its task is pending or open, stop the same way on it. Reuse plans 12 (`targets.json`, D-53) and 13 (gap-aimed drafting, D-54); no new mechanism if theirs covers it.
- Content: cost per approved and per translated question from `costs.log` (translated: from part 11''s pilot); release budget per language as a pm decision before full runs; simulation bottlenecks → targets per language/age group in `authoring/data/targets.json`, read by `draft` and `--translate`.
- Owner `plans/16-content-target.md` ("Cost").', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (249, 9, 'write plan: Regional packs (RG-3..RG-5)', 'plan', 'open', 280, NULL, 'Write the plan for part 10 of the masterplan (plan 9): `pm plan add 9 "Regional packs (RG-3..RG-5)" --priority 300`.

- Needs OQ-31 (plan 37): task 189 writes the decision "launch languages", task 190 records it (D-entry, I18N-1). If it is still pending, `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- Needs OQ-33 (plan 39: task 193 writes the decision, 194 records it; DLC or free). Still pending: link it the same way and stop. Task priority 280 puts this after task 194 (300).
- OQ-46 (`colombia` subcategories, `plans/open-questions.md`): answered first or folded into RG-5''s decision.
- Content: mark RG-3 (= BN-6, plan 27, + part 1''s `--bundles`) and RG-4 (= BN-11, done); RG-5 pm decision with a recommendation (which packs launch, default on per language, is `colombia` translated); new bundles via `qgen bundle new`, taxonomy approved by the gamemaster; batches go to part 11.
- Owner `plans/15c-regional-questions.md`, `plans/22-bundles.md`.', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (250, 9, 'write plan: Release content runs', 'plan', 'open', 270, NULL, 'Write the plan for part 11 of the masterplan (plan 9): `pm plan add 9 "Release content runs" --priority -110`.

- Needs the plans of parts 4, 8 and 10 (their `qgen batch` modes) and part 9''s plan (budget, targets): write against those that exist; a dropped part means no runs for it.
- Content: translation pilot per language (QT-5: 50 questions, reject rate and cost, go/no-go pm decision; task priority -90), full translation per language (QT-6), neutral Spanish runs, regional pack batches, `base` top-ups where the simulation fails after milestone 1''s 5000; each batch followed by D-56''s QC (`authoring/QC.md`), native-speaker spot checks for translations (sample + pm decision "spot check done?"). Full runs after plan 17''s batch runs.
- Workers only run `qgen batch` (D-36).', '2026-10-12T01:10:56Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (251, 9, 'write plan: S4 close-out', 'plan', 'open', 260, NULL, 'Write the plan for part 12 of the masterplan (plan 9): `pm plan add 9 "S4 close-out" --priority -130`.

- Last part; write it after the other parts'' plans exist (or were dropped).
- Content: `qgen report --simulate` passes for every launch language, result recorded in `plans/16-content-target.md`; `plans/11-steam.md` S4 row done; statuses and tasks in 15, 15a, 15b, 15c, 16; `plans/project.md`, `plans/README.md`; notes in the masterplans of milestones 10–11 (plans 10, 11) if S4 changed their scope (store languages, DLC packs, install size).', '2026-10-12T01:10:57Z', NULL, 239);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (252, 10, 'create tasks for plan 10', 'split', 'done', 1000, '2026-10-11, tasks 253–263 (plan-writing for parts 1–11); priorities put each after its decision tasks; no new decisions (parts raise their own)', 'Split plan 10 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:12:46Z', '2026-10-12T01:13:58Z', 10);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (253, 10, 'write plan: Partner account, name check and AI terms (PUB-6, PUB-7, PUB-10)', 'plan', 'open', 250, NULL, 'Write the plan for part 1 of the masterplan (plan 10): `pm plan add 10 "Partner account, name check and AI terms (PUB-6, PUB-7, PUB-10)" --priority 720`.

- Needs OQ-33 (plan 39: task 193 writes the decision "price model and account holder", task 194 records it). Still pending: `pm task-pending-decision <this task> <its id>`, stage nothing, stop. Task priority 250 puts this after task 194 (300).
- Read the current `plans/17-publishing.md` (plan 43, S2 close-out, may have rewritten PUB-*).
- Content: PUB-6 signup checklist for the holder (tax interview, bank, $100 app credit), result via pm decision "Steamworks app created? App ID?"; PUB-7 name/trademark check for D-50''s names (Steam search, EUIPO/USPTO/WIPO, domains), findings in a pm decision, fail → OQ-34 reopens; PUB-10 Anthropic commercial-use terms for `claude -p` outputs, one line + source in plan 17, unclear → decision body for a professional.
- Gamemaster does signup and payments; workers never enter credentials or contact anyone.
- Owner `plans/17-publishing.md` ("Steamworks and store", "AI disclosure").', '2026-10-12T01:13:55Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (254, 10, 'write plan: Steamworks app configuration (SW-7)', 'plan', 'open', 240, NULL, 'Write the plan for part 2 of the masterplan (plan 10): `pm plan add 10 "Steamworks app configuration (SW-7)" --priority 700`.

- Needs OQ-31 (plan 37, tasks 189/190), OQ-29 (plan 34, tasks 182/183) and OQ-33 (plan 39, tasks 193/194). Any still pending: `pm task-pending-decision <this task> <its id>` for each, stage nothing, stop.
- Needs part 1''s plan (App ID decision) and the file-saves plan of milestone 8 (task 210, `FileStore` path); write against them.
- Content: checklist with exact values in plan 18: App ID, localized names (D-50), depots (Windows, Linux, shared content; language/bundle depots only if milestone 9 or OQ-33 call for them), launch options per OS (incl. plan 36''s mode flag), languages, branches `default` + password-protected `beta`, controller flags, Steam Input default config, Deck settings; Auto-Cloud root/pattern per OS for the `FileStore` file, quota, conflict behaviour; `steam_appid.txt` for dev.
- Done when (of the plan): gamemaster confirms the values are entered (pm decision).
- Owner `plans/18-steam-integration.md` ("Builds and depots", "Steam features").', '2026-10-12T01:13:55Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (255, 10, 'write plan: Steamworks binding in the shell (SW-8)', 'plan', 'open', 240, NULL, 'Write the plan for part 3 of the masterplan (plan 10): `pm plan add 10 "Steamworks binding in the shell (SW-8)" --priority 690`.

- Needs OQ-29 (plan 34, tasks 182/183: shell and binding). Still pending: `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- Builds on milestone 8''s plans: shell skeleton (task 209), gamepad + glyphs (plan 45), letter picker (plan 46), and I18N-2 (milestone 9, task 246). Add to the shell, don''t rebuild it.
- Content: binding in the main process, one optional `steam` object through the preload bridge (`steam?.available`), silent fallback without Steam, no `restartAppIfNecessary`; overlay in Electron (Windows, Deck); `ShowFloatingGamepadTextInput` for the player name; glyphs via `GetInputTypeForHandle` where better than `Gamepad.id`; default language from Steam (I18N-2''s setting wins once set); rich presence optional via `t()`; dev on NixOS with Spacewar (480) or the real App ID, native lib from the flake in dev.
- Owner `plans/18-steam-integration.md` ("Steam features"); touches `14-input.md`, `15-i18n.md`.', '2026-10-12T01:13:55Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (256, 10, 'write plan: Steam Cloud saves', 'plan', 'open', 230, NULL, 'Write the plan for part 4 of the masterplan (plan 10): `pm plan add 10 "Steam Cloud saves" --priority 680`.

- Builds on part 2''s Auto-Cloud values, part 3''s binding and milestone 8''s `FileStore` (task 210''s plan); write against them.
- Content: Auto-Cloud only unless the test shows a need; check that `FileStore`''s temp + rename leaves only the real file in the synced pattern (temp/backup excluded); one save per OS user vs. per Steam user (pm decision if it changes behaviour for two Steam accounts on one PC); test checklist for the gamemaster (machine A → B, Windows ↔ Linux/Deck; offline on both then online → conflict dialog), result via pm decision.
- Owner `plans/18-steam-integration.md` ("Steam features"); save format `plans/12-client-engine.md`.', '2026-10-12T01:13:55Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (257, 10, 'write plan: Achievements (SW-11)', 'plan', 'open', 230, NULL, 'Write the plan for part 5 of the masterplan (plan 10): `pm plan add 10 "Achievements (SW-11)" --priority 590`.

- Needs OQ-30 (plan 35, tasks 184/185: preset names). Still pending: `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- Unlocks go through part 3''s bridge; write against its plan.
- Content: few achievements, no grind (plan 18''s draft), exact trigger per engine event, gamemaster mode counts or not; names/descriptions per launch language; the list as a pm decision before icons; 64×64 achieved + unachieved icons, original art, in the credits (plan 47); Steamworks setup values in plan 18; optional retroactive unlock from the save; nothing in the save depends on Steam.
- Owner `plans/18-steam-integration.md` ("Steam features").', '2026-10-12T01:13:55Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (258, 10, 'write plan: Store page and AI disclosure (PUB-8, LUI-6)', 'plan', 'open', 220, NULL, 'Write the plan for part 8 of the masterplan (plan 10): `pm plan add 10 "Store page and AI disclosure (PUB-8, LUI-6)" --priority 300`.

- Needs OQ-31 (plan 37, tasks 189/190: launch languages). Still pending: `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- Uses part 1''s PUB-10 finding and name check; part 7''s builds for system requirements; write against their plans.
- Content: texts per launch language (short/long description, features, system requirements, controller support, privacy line, AI disclosure per D-32/D-33/D-56, no live AI), drafts in a file under `plans/` or `docs/`, approved via pm decision; capsule sizes per Valve''s current list, scripted screenshots at 1920×1080, trailer only if cheap (else backlog); who makes capsule art: pm decision (AI-made art needs disclosing).
- Owner `plans/17-publishing.md` ("Steamworks and store", "AI disclosure"), `plans/15a-ui-translation.md` (LUI-6).', '2026-10-12T01:13:55Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (259, 10, 'write plan: Content survey, rating and price (PUB-9, PUB-11)', 'plan', 'open', 210, NULL, 'Write the plan for part 9 of the masterplan (plan 10): `pm plan add 10 "Content survey, rating and price (PUB-9, PUB-11)" --priority 290`.

- Needs OQ-33 (plan 39, tasks 193/194: price, DLC). Still pending: `pm task-pending-decision <this task> <its id>`, stage nothing, stop.
- After part 8''s plan.
- Content: content survey answers drafted from the game (no violence, gambling, user content; topics that may need a note); IARC per Valve''s current rules; price + regional prices from OQ-33''s D-entry (Valve''s matrix), DLC entries if bundles are paid DLC; gamemaster enters both, result via pm decision.
- Owner `plans/17-publishing.md`.', '2026-10-12T01:13:56Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (260, 10, 'write plan: Media bundle for shipping (SW-9)', 'plan', 'open', 190, NULL, 'Write the plan for part 6 of the masterplan (plan 10): `pm plan add 10 "Media bundle for shipping (SW-9)" --priority 640`.

- Needs the Freesound answer (plan 42, tasks 204/205; OQ number per task 203). Still pending: `pm task-pending-decision <this task> <its id>`, stage nothing, stop. Task priority 190 puts this after task 205 (200).
- Needs licence data (plan 26) and the shell''s media resolver (task 209''s plan); write against them.
- Content: `trivia-media` (`app/`, no `authoring/` imports) gains a bundle command: images ≤ 3840 px wide (D-48), WebP/AVIF, < 1 MB target; audio → Opus; video re-encoded; same lookup keys as the cache (D-17) or one adapter; size budget per depot and a check that fails over budget or on a missing file; Freesound rule applied; `CREDITS.md` lists exactly the shipped files.
- Owner `plans/18-steam-integration.md` ("Platforms and display"), `plans/23-media-providers.md`.', '2026-10-12T01:13:56Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (261, 10, 'write plan: Builds, depots and upload (SW-10)', 'plan', 'open', 180, NULL, 'Write the plan for part 7 of the masterplan (plan 10): `pm plan add 10 "Builds, depots and upload (SW-10)" --priority 620`.

- Builds on milestone 8''s local builds (task 211''s plan) and part 6''s media bundle; write against them. If milestone 8 moved SW-6 (CI) to S5 (plan 48''s note, `plans/18-steam-integration.md`), this plan takes it over.
- Content: SteamCMD app/depot VDFs in the repo (no secrets); one upload command (e.g. `trivia-steam upload --branch beta`) from a clean tagged commit: `qgen validate`, `npm run check`, both platform builds + media bundle, `run_app_build`; SteamCMD from nixpkgs (unfree) or Valve''s SDK (the plan decides); runs on the author''s machine, CI upload only with a pm decision; build account and beta password stay with the gamemaster; gitignore what SteamCMD writes; `default` branch empty until S6.
- Owner `plans/18-steam-integration.md` ("Builds and depots").', '2026-10-12T01:13:56Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (262, 10, 'write plan: Steam Deck test and Deck Verified (SW-12)', 'plan', 'open', 175, NULL, 'Write the plan for part 10 of the masterplan (plan 10): `pm plan add 10 "Steam Deck test and Deck Verified (SW-12)" --priority 370`.

- Builds on plan 48''s S3 Deck rows (no copy), part 3 (keyboard, glyphs), part 4 (Cloud) and part 7 (beta upload).
- Content: checklist for a real Deck with the Steam-installed beta: Valve''s current Verified criteria, Cloud sync with a PC, suspend/resume; result via pm decision; when to request the review (check Valve''s docs: before or after release; if after, note it for S6 in plan 11).
- Owner `plans/18-steam-integration.md` ("Steam Deck Verified"), `plans/14-input.md`.', '2026-10-12T01:13:56Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (263, 10, 'write plan: Beta test and S5 close-out', 'plan', 'open', 170, NULL, 'Write the plan for part 11 of the masterplan (plan 10): `pm plan add 10 "Beta test and S5 close-out" --priority 130`.

- Last part; write it after the other parts'' plans exist (or were dropped).
- Content: beta checklist in plan 18 (install `beta` from Steam on a second machine, offline start, a full family game, Cloud to another machine), result via pm decision "S5 beta test passed?", failures → tasks in the owning parts; `plans/11-steam.md` S5 row done; SW-13, SW-14 marked deferred with a note; statuses in 17, 18, 15a, 14; `plans/project.md`, `plans/README.md`; note in plan 11 (masterplan of milestone 11) if S5 changed S6''s scope.', '2026-10-12T01:13:56Z', NULL, 252);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (264, 11, 'create tasks for plan 11', 'split', 'done', 1000, '2026-10-11, tasks 265–271 (plan-writing for parts 2, 3, 5, 1, 4, 6, 7); priorities 165–130 put them after milestone 10''s plan tasks; no new decisions (parts raise their own: coming-soon date, report channel, cadence, released)', 'Split plan 11 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:15:13Z', '2026-10-12T01:16:15Z', 11);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (265, 11, 'write plan: Version numbers and patch-safe saves', 'plan', 'open', 165, NULL, 'Write the plan for part 2 of the masterplan (plan 11): `pm plan add 11 "Version numbers and patch-safe saves" --priority 600`.

- Read first: `pm plan list`; plan 18 "Builds and depots" (masterplan 10 part 7, task 261, may have written the upload plan); `plans/12-client-engine.md` (save format); the engine plans 19/20 (PORT-2/3) for how burns and history are keyed today.
- Content: one semver source of truth (today `0.1.0` in `flake.nix`), stamped into the build, shown on credits/settings and in the report text (part 5); pool version (export hash or tag) next to it; git tag per release (`v1.0.0`), Steam build description = tag.
- Saves across patches: unknown question ids ignored, dropped questions never come back as "new", save format version + migration only if the shape changes. Add only what the engine lacks; verify with a throw-away script (old save vs. new pool).
- Owner `plans/18-steam-integration.md` ("Builds and depots"), save format in `plans/12-client-engine.md`.
- Task priority 165 puts this after the plan-writing tasks of milestone 10 (170–250); first of plan 11 because part 3 checks it.', '2026-10-12T01:16:13Z', NULL, 264);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (266, 11, 'write plan: Release checklist (ST-4)', 'plan', 'open', 160, NULL, 'Write the plan for part 3 of the masterplan (plan 11): `pm plan add 11 "Release checklist (ST-4)" --priority 700`.

- Needs: part 2''s plan (version + tag); masterplan 10 part 7''s plan (upload command, task 261) and part 10''s Deck rows (task 262). If those plans don''t exist yet, refer to them by part and write the check list against the upload command''s interface as planned.
- Credits check reads plan 47 (PUB-5, `CREDITS.md`/`credits.json`) and plan 26 (licence data).
- Content: automated `release-check` (extend the upload command, no new tool): clean tree on a tagged commit matching the version; `qgen validate`; `npm run check`; pool export fresh; credits complete both ways (every shipped file/font/sound/glyph/library listed, nothing extra); media bundle within budget; both platform builds succeed; loud failure, prints the manual steps left.
- Manual checklist in `plans/11-steam.md` (ST-4), result via one pm decision per release candidate: offline test (network and Steam off, full game to level 12 or a won checkpoint), Deck test, Windows test, Cloud sync, family sign-off on the `beta` branch. Optional "patch" variant only with a reason in the plan.
- Gamemaster does the manual tests; workers write the checklist and record the result.', '2026-10-12T01:16:13Z', NULL, 264);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (267, 11, 'write plan: Question reports by hand (ST-5)', 'plan', 'open', 160, NULL, 'Write the plan for part 5 of the masterplan (plan 11): `pm plan add 11 "Question reports by hand (ST-5)" --priority 550`.

- Needs: plan 36 (MD-6 «Reportar pregunta», the local report list) and part 2''s plan (version + pool version in the report text). Read their current state; build on the report list, don''t rebuild it.
- Content: channel decision for the gamemaster (pinned Steam discussions thread recommended, and/or an email address in the game; an address is the gamemaster''s personal data): the plan''s first task writes it as a pm decision.
- Client: per report and for all, a "copy" text (question id, language, version + pool version, the player''s reason) plus where to send it; no automatic network request, `mailto:`/Steam overlay URL only on a click (overlay only under Steam); strings via `t()` for every launch language. Owner in-game: `plans/13-game-modes.md` (MD-6).
- Authoring: turn a pasted report into a `needs_work` flag with the report as review note (a `qgen` command or the review tool''s form), fix via `qgen rework`; no new storage beyond `authoring/data/questions.json`.
- Never phones home. Owner `plans/11-steam.md` (ST-5).', '2026-10-12T01:16:13Z', NULL, 264);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (268, 11, 'write plan: Coming soon page (ST-3)', 'plan', 'open', 155, NULL, 'Write the plan for part 1 of the masterplan (plan 11): `pm plan add 11 "Coming soon page (ST-3)" --priority 450`.

- Needs masterplan 10 part 8 (store page, PUB-8, task 258), part 1 (App ID, names, task 253), part 9 (survey, task 259). Read their plans if they exist; the plan''s tasks wait on the gamemaster''s approval of the store page, not this task.
- Content: checklist for the gamemaster (store page complete → Valve''s store review → fixes → "Coming soon" with a date or "to be announced"); result via pm decision "Coming soon page live? date?".
- Timing: Valve''s current minimum between "Coming soon" and release (two weeks in the masterplan; check the Steamworks docs, cite the source in `plans/11-steam.md`); aim for longer; part 4''s release date counts from the live date.
- Wishlists: only Steam''s own wishlist/follow; no mailing list, own website or marketing.
- Gamemaster does the Steamworks steps; workers never enter credentials or contact Valve. Owner `plans/11-steam.md` (ST-3), store texts in `plans/17-publishing.md` (PUB-8).', '2026-10-12T01:16:13Z', NULL, 264);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (269, 11, 'write plan: Launch', 'plan', 'open', 150, NULL, 'Write the plan for part 4 of the masterplan (plan 11): `pm plan add 11 "Launch" --priority 160`.

- Needs: the plans of parts 1, 2, 3, 5 (write after them, refer to their tasks); OQ-33 price (plan 39, task 194 records it); milestone 9''s content target met for every launch language (plan 38, `qgen report --simulate`): the release task waits for it.
- Content: release candidate (tag, upload to `beta`, part 3''s check, family sign-off) → Valve''s build review (current lead time from the Steamworks docs, cited) → gamemaster sets the build live on `default` and presses Release on part 1''s date.
- Launch-day checklist: price/discounts from OQ-33 live; store languages match the build; discussions open with part 5''s report thread pinned; launch announcement drafted per launch language (gamemaster posts it).
- First week: gamemaster watches discussions/reviews; bugs → `plans/backlog.md`; hotfix through part 3. Result via pm decision "Released? date, build id".
- Owner `plans/11-steam.md` (S6 row). Workers never contact Valve or players.', '2026-10-12T01:16:13Z', NULL, 264);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (270, 11, 'write plan: Content updates as patches (ST-5)', 'plan', 'open', 145, NULL, 'Write the plan for part 6 of the masterplan (plan 11): `pm plan add 11 "Content updates as patches (ST-5)" --priority 250`.

- Needs: parts 2, 3, 4, 5 (plans); OQ-35 (plan 40, task 199): if the pool isn''t public, patch notes must not leak unreleased questions; read the answer.
- Content: cadence as a pm decision for the gamemaster (e.g. monthly or every N new approved questions per launch language; hotfixes for wrong answers any time); the plan records the answer.
- Patch = new version (part 2) + part 3 + upload; new approved questions via `qgen batch`, fixes from part 5, dropped questions; never changes rules or saves silently.
- Patch notes: a `qgen` command that diffs the pool between two tags (added/fixed/dropped per language and category) and drafts the note; gamemaster posts it as a Steam event.
- Done when: the first content patch after launch went out this way (pm decision with version and date). Owner `plans/11-steam.md` (ST-5), `plans/16-content-target.md`.', '2026-10-12T01:16:13Z', NULL, 264);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (271, 11, 'write plan: S6 close-out', 'plan', 'open', 130, NULL, 'Write the plan for part 7 of the masterplan (plan 11): `pm plan add 11 "S6 close-out" --priority 120`.

- Last part; write it after the other parts'' plans exist (or were dropped).
- Content: `plans/11-steam.md` ST-3..ST-5 `[x]`, S6 row done, status; leftovers in `plans/17-publishing.md` and `plans/18-steam-integration.md` done or deferred with a note; `plans/project.md`, `plans/README.md`; `README.md`: how to cut a release and send a patch (commands for humans).
- Leftovers to `plans/backlog.md`: competitive mode, couch co-op, more regions/languages, SW-13, SW-14.
- Done when: the milestone''s "Done when" holds (released, first content patch out).', '2026-10-12T01:16:13Z', NULL, 264);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (272, 13, 'create tasks for plan 13', 'split', 'dropped', 1000, 'queued by task 29''s baseline edit to plan 13; plan 13 is already split (task 20), the tasks are unchanged', 'Split plan 13 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:28:12Z', '2026-10-12T01:28:17Z', 29);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (273, 15, 'create tasks for plan 15', 'split', 'done', 1000, '2026-10-11, tasks.sql: task 41 re-added as 274 (batch-8 guard per plan, overlap_candidates(), priority 710); 42, 44, 45 match the plan; threshold decision stays with task 45 (needs the baseline), task 44 waits on decision 1', 'Split plan 15 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T01:30:57Z', '2026-10-12T01:31:54Z', 40);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (274, 15, 'no_overlap criterion in rate; drop overlaps at merge', 'work', 'done', 710, '2026-10-11, authoring/tools/qgen.py (rate_candidates, overlap_candidates in the rate payload, no_overlap hard criterion + overlap_with in RATE_SCHEMA, merge drops ''overlap like q-…'', overlaps skip revise), authoring/tools/prompts/rate.md. Check on 20 batch-7 questions (4 known overlaps + 12 with candidates + 4 without): without candidates all no_overlap 5; with candidates q-0646→q-0217 1, q-0957→q-0644 2, q-0689→q-0279 2, q-1210→q-0315 2, the 16 others 4-5 (final prompt; an earlier wording without the ''same moment from another side'' rule passed q-1210). batch-8 drafts: 788, candidates mean 2.5, max 8, 600 with any, 14 s. 4 Opus calls ~$1.24. Plan 15 body not edited (it would re-queue its split). qgen validate: only the pre-existing q-0021 licence error (decision 10).', 'Part "Judge in rate" of plan 15. Builds on task 40''s `overlap_candidates()` in `authoring/tools/qgen.py`.

- Batch-8 guard: change `rate`/`merge` only before or after a batch''s rate step, not during it. Check `work/batch-8` (and any newer batch): `ratings/` present but no `merged.json` = mid-rate → stop, note it, leave it for plan 17''s batch-run task. Drafts only (no `ratings/`) is fine: that batch then rates with `no_overlap`.
- Grouped `rate` call (PE-1): each draft''s candidates from `overlap_candidates()` (pool of every bundle, status ≠ `rejected`, plus earlier drafts of the same batch; id, question, answer, concept) in the payload; new hard criterion `no_overlap` in the rating schema and `authoring/tools/prompts/rate.md` (5 = asks a different fact; ≤ 3 = knowing one answer gives the other away, or the same fact again). Within-batch pairs: the later draft fails.
- `merge`: a `no_overlap` hard fail is dropped with reason `overlap like q-…` in `dropped.json`; the concept isn''t retired. `duplicates()` stays.
- Prompts are changed here as an implementation task, never inside a batch run (RUNBOOK).
- Check (throw-away script, two LLM calls): rate ~20 batch-7 drafts incl. the four known overlaps (plan 15 baseline), once without and once with candidates; the four fail `no_overlap`, the others don''t. Result in the task note and plan 15''s baseline.

Done when: check passes; `qgen validate` clean; no batch run.', '2026-10-12T01:31:50Z', '2026-10-12T01:39:49Z', 273);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (275, 18, 'create tasks for plan 18', 'split', 'dropped', 1000, 'plan 18 body edit by task 70 only notes the soak db/step-count format; tasks 70/71 already cover it, nothing new to split', 'Split plan 18 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-12T02:07:41Z', '2026-10-12T02:08:03Z', 70);

INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (1, 'Target count per difficulty (1–15) for 5000 approved base questions?', 'answered', '["1: 250 · 2: 350 · 3–8: 450 each · 9–11: 330 each · 12–13: 230 each · 14–15: 125 each (sum 5000)", "masterplan draft: 1–2: 490 each · 3–8: 420 each · 9–11: 300 each · 12–13: 200 each · 14–15: 100 each (sum 5000)", "flat: 333 per level (5 extra at 6–10)"]', 'Milestone 1, part 1 (D-52). Today (2026-10-11) approved base by difficulty: 1: 36 · 2: 67 · 3: 96 · 4: 104 · 5: 112 · 6: 147 · 7: 101 · 8: 67 · 9: 74 · 10: 57 · 11: 61 · 12: 38 · 13: 48 · 14: 19 · 15: 8.
The targets steer `draft` (part 2: aim at the gaps) and are the milestone''s exit check.
Recommended curve tapers at both ends; the masterplan draft puts more at 1–2 than at the middle levels, which is likely more easy questions than game nights need.', '1: 250 · 2: 350 · 3–8: 450 each · 9–11: 330 each · 12–13: 230 each · 14–15: 125 each (sum 5000)', NULL, '2026-10-11T23:16:33Z', '2026-10-12T02:09:52Z', 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (2, 'When is batch quality "fine": human spot-check size and agreement rate with the LLM review?', 'answered', '["30 random questions per batch; ≥ 90% agreement in each of the last two batches", "50 per batch; ≥ 95% agreement", "20 per batch; ≥ 85% agreement"]', 'Milestone 1, parts 1 and 5. After every batch the gamemaster checks a random sample in the review tool and records agree/disagree with the LLM verdict. This rate is the main "quality is fine" signal and part of the milestone''s exit check (last two batches).
30 questions take roughly 10–15 minutes; 50 gives a tighter rate but costs more of the human''s time per batch (~8 batches left).', '30 random questions per batch; ≥ 90% agreement in each of the last two batches', NULL, '2026-10-11T23:16:33Z', '2026-10-12T02:10:59Z', 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (3, 'How are needs_work questions (33 now, more per batch) resolved?', 'answered', '["qgen rework once after each batch''s QC, then the gamemaster decides what is still needs_work in the review tool", "the gamemaster decides all of them in the review tool; no qgen rework", "leave them; only approved questions count toward 5000"]', 'Milestone 1, part 6. RUNBOOK: `qgen rework` runs only on the gamemaster''s word; this answer is that word for the batch tasks of this milestone. batch-7 needs_work reasons: mostly giveaway hints, overlap with a pool question, or no usable media.
Rework costs LLM calls but saves the gamemaster''s time; overlaps (once part 4 drops them before merge) and media misses don''t benefit from rework.', 'qgen rework once after each batch''s QC, then the gamemaster decides what is still needs_work in the review tool', NULL, '2026-10-11T23:16:33Z', '2026-10-12T02:11:18Z', 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (4, 'After the engine port, which routes does the Python game server keep besides static files and /api/save?', 'pending', '["Keep /media (download on cache miss, D-17), /api/flags (state/flags.json, D-47) and /api/categories; amend the milestone''s ''static files plus /api/save only'' accordingly", "Move flags into SaveData (drop /api/flags, trivia-authoring reads game.json); keep /media and /api/categories", "Strictly static + /api/save: flags into SaveData, categories served as static files, media served only from the synced cache (no download on miss; trivia-media sync required before play)"]', 'Milestone 2 "Done when" says `trivia` serves static files plus `/api/save` only. Today `app/server/main.py` also has `/media` (cache + download on miss, D-17), `/api/flags` (game flags questions, `trivia-authoring` turns them into reviews, D-47) and `/api/categories` (all bundles, D-43). Python stays in family mode anyway (plan 12, D-3); the desktop shell (plan 18) is out of scope. Affects parts 4, 5, 6 of the masterplan.', NULL, NULL, '2026-10-11T23:56:57Z', NULL, 54, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (5, 'Where does the supply check for qgen report and the authoring start page live once app/server/selection.py has no game to serve?', 'pending', '["Move selection.py to authoring/tools/ unchanged (reads game.json), parity with engine/selection.ts guarded by the PORT-1 selection fixtures", "Authoring calls the TS engine via node (type stripping), no Python copy", "Keep app/server/selection.py where it is"]', '`qgen report` and `authoring/server/overview.py` use `selection.py` (levels, `LEVEL_RANGES`, `available`, `supply`, `burned_ids`). After PORT-8 the game no longer needs it. A Python copy duplicates the rules in two languages; calling Node from Python tooling adds a runtime hop. Plan 12 (PORT-8) left it open. Affects part 6 (and part 4''s switch of the authoring readers).', NULL, NULL, '2026-10-11T23:56:58Z', NULL, 54, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (6, 'Plan 21 (LUI-1): how to check the screens show no visible change?', 'answered', '["Throw-away Playwright outside the project (nix shell / temp dir, nothing in package.json): scripted run before and after, pixel diff with ImageMagick compare", "Gamemaster clicks through by hand with a checklist the worker writes", "No screenshots: the per-task literal checks are enough"]', 'Plan 21 asks for before/after screenshots of every screen, but the flake has no headless browser and the client has no test deps. Each task already checks that every moved literal reappears verbatim in es.ts.', 'Throw-away Playwright outside the project (nix shell / temp dir, nothing in package.json): scripted run before and after, pixel diff with ImageMagick compare', NULL, '2026-10-12T00:14:30Z', '2026-10-12T02:15:40Z', 86, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (7, 'Have you checked the colombia proposals at /review?bundle=colombia?', 'answered', '["checked, all moves done in the review tool", "checked, the ids to move are listed in the answer"]', 'BN-3 (qgen bundles, 2026-10-07) moved 84 existing questions to the colombia bundle; their reasons are in work/bundles/proposals.json. Rule (D-39): a question belongs in colombia only if answering needs a connection to Colombia that players outside Colombia mostly wouldn''t know. Run trivia-authoring and open http://127.0.0.1:8001/review?bundle=colombia (109 questions: the 84 proposals plus later colombia questions; checking all is fine). Key n moves a question to the next bundle (colombia → base). A question moved to base needs a base subcategory (D-49); qgen validate will report it and the agent logs it for you.', 'checked, all moves done in the review tool', NULL, '2026-10-12T00:16:29Z', '2026-10-12T02:26:16Z', 90, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (8, 'Media with Commons restriction flags (personality rights, trademark, …): replace all, or let the gamemaster keep a file after checking it?', 'pending', '["Gamemaster checks each flagged file in the review tool and either keeps it (stored mark) or replaces it", "Replace every flagged file"]', 'Milestone 4 lists flagged files among those to replace; plans/17-publishing.md says the flags don''t stop editorial use in a quiz and suggests checking each file. Replacing all is simpler (no extra state) but drops usable photos of people and logos; per-file checking needs a stored ''checked, keep'' mark per slot that the audit (part 2) honours and the review tool (part 3) sets.', NULL, NULL, '2026-10-12T00:17:48Z', NULL, 106, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (9, 'Gamepad on the Question screen: how do players pick answers and play jokers (IN-4)?', 'answered', '["Focus only: D-pad moves over the 2×2 answers and the joker tray, A locks the focused answer and focus jumps to «Respuesta final» (A again submits), B unlocks/cancels, Start = menu; LB/RB move focus into the tray (prev/next token), A arms and A again plays (today''s two-tap arming); Y = replay media; tiles keep A–D, no pad glyph on them", "Direct face buttons: Y/X/B/A pick answers by position (top-left, bottom-left, top-right, bottom-right; tiles show the pad glyph next to A–D); RT submits, LT unlocks, Start = menu; jokers by focus as in option 1", "Focus as in option 1, plus a joker wheel: holding LB opens a radial picker of the five jokers (new component), the stick picks, release plays"]', 'Plan "Gamepad input and button glyphs (IN-4, IN-5)" (masterplan 8, part 5). `plans/14-input.md` leaves this open ("To decide when designing (IN-4)").

- Recommended: option 1. Same model on every screen (navigate + A/B), no new UI, the 2×2 grid fits the D-pad, and the tray is already a column next to the answers.
- Against direct face buttons: the tiles are labelled A–D, and Xbox A/B/X/Y sit in a diamond (A bottom, B right, X left, Y top), so tile «B» would be a different pad button than B, and B would no longer mean "back" on this one screen. Speed doesn''t matter (no timer; the family discusses first).
- The wheel is the most work (new component, analog input, art) for five jokers that fit a focus column.
- Keyboard and mouse stay as today in every option.', 'Direct face buttons: Y/X/B/A pick answers by position (top-left, bottom-left, top-right, bottom-right; tiles show the pad glyph next to A–D); RT submits, LT unlocks, Start = menu; jokers by focus as in option 1', NULL, '2026-10-12T00:57:48Z', '2026-10-12T02:30:23Z', 213, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (10, 'q-0021: GFDL-only photo blocks qgen validate', 'answered', '["Gamemaster repicks q-0021''s image in the review tool (/review/q-0021); then task 113 closes", "Set q-0021 to needs_work until plan 26 part 3 replaces it", "Allowlist failures stay a validate warning until part 3; only a missing record is an error"]', 'After the licence migration (task 113), validate errors on q-0021 (approved): its media https://commons.wikimedia.org/wiki/File:Container_Ship.jpg is GFDL 1.2 only, not on the allowlist (D-45). Until fixed, qgen validate and the last step of qgen batch fail. Replacements are picked by the gamemaster, not an LLM. Everything else in task 113 is done and staged.', 'Set q-0021 to needs_work until plan 26 part 3 replaces it', NULL, '2026-10-12T01:26:01Z', '2026-10-12T02:30:52Z', 113, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (11, 'Difficulty anchors 9–15: are these levels right?', 'answered', '["levels as proposed", "corrections in the answer"]', 'Proposed anchors for the house style''s calibration section (task 32 writes them in). Approved base questions, spread over 9–15 and broad categories; level = stored difficulty. Scale: 10 = 16-year-old, 12 = most adults, 14 = well-read adult / graduate in the field, 15 = trivia specialists.

- 9 · q-0023 (geografía mundo): ¿Cuál es la capital de Australia? → Canberra
- 10 · q-0833 (historia): Busto de piedra pintada hallado en 1912 en Amarna, Egipto: ¿a qué reina representa? → Nefertiti
- 11 · q-0812 (ciencia y matemáticas): Filósofo francés del siglo XVII que popularizó x, y, z para las incógnitas → René Descartes
- 12 · q-0849 (fútbol): Centrocampista española, campeona del mundo 2023, mejor jugadora del Mundial y Balón de Oro → Aitana Bonmatí
- 13 · q-1171 (inventos y tecnología): ¿Quién creó la World Wide Web y el HTML? → Tim Berners-Lee
- 13 · q-0624 (arte y literatura): Estilo de las entradas del metro de París, los carteles de Mucha y las casas de Horta → Art nouveau
- 14 · q-0814 (ciencia y matemáticas): Los siete puentes de Königsberg, imposible demostrado en 1736 → Leonhard Euler
- 14 · q-0669 (fiestas y tradiciones): ¿En cuál de estos años febrero NO tuvo día 29? → 1900
- 15 · q-0604 (Amazonas): Mariposa inofensiva que copia los colores de otra de mal sabor; el truco lleva el apellido de un naturalista inglés → Mimetismo batesiano
- 15 · q-0221 (comida y bebida): El tempura llegó a Japón hace unos 450 años desde un país europeo. ¿Cuál? → Portugal

Answer "levels as proposed", or list corrections as "q-XXXX: <level>" (and any question to drop or swap).', 'yes', NULL, '2026-10-12T01:47:40Z', '2026-10-12T02:02:22Z', 34, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (12, 'Desktop shell (OQ-29)?', 'pending', '["Electron; Steam binding: steamworks-ffi-node or steamworks.js, picked in SW-2", "Tauri v2", "Browser + local server (PyInstaller)"]', 'Shell only shows `app/client/dist/` + one save file (after milestone 2). Details: `plans/18-steam-integration.md`. Facts checked 2026-10-11.

**Facts**
- Electron: v44.7.0 (2026-10-07); zip 158 MB Win, 123 MB Linux (GitHub release assets). Same Chromium everywhere.
- steamworks.js: last npm release 0.4.0 (2024-08-06), last commit 2025-09-07, 66 open issues (GitHub API). Node-API (napi6) → not tied to an Electron version. Overlay: `electronEnableSteamOverlay()`; open issues #116 (white overlay), #160, #195 (no overlay on Linux Electron, 2025-07). → stale.
- steamworks-ffi-node: active, 0.11.3 (2026-09-24), SDK 1.64, Koffi FFI (no C++ build), experimental Electron overlay incl. Linux/SteamOS (OpenGL). Young (2025-10), 83 stars.
- Steam overlay over a system webview: no hook (tauri#6196, Construct blog "Trying to show the Steam overlay" 2023); community Win-only workaround tauri-steam-overlay-surface (2026-07).
- Tauri v2.12.3 (2026-10-10). Linux/Deck = WebKitGTK: `backdrop-filter` broken on some setups (tauri#14811, open 2026-01, NVIDIA), media via GStreamer (tauri#8579 open, #10665 AVIF), AppImage breaks on Mesa 25+ (#15665, 2026-07).
- Deck: Electron overlay is shaky on native Linux; Windows build via Proton is the common fallback. Electron bundles its engine, so either works; Tauri depends on the system WebKitGTK/WebView2.

**Phones as buzzers (OQ-37, not a blocker)**
- Electron: Node `http`/`ws`-free server in main; same TS as the client.
- Tauri: server in Rust (new language).
- Browser + local server: has one already (Python), but plans 19/20 remove Python.

**Trade-offs**
- Electron: + one engine on every target, overlay works on Win, TS only. − ~150 MB, Steam binding needs care (stale vs. young).
- Tauri: + ~10 MB. − two engines to test, our blur/video effects at risk on Deck, no overlay.
- Browser + server: + closest to today. − no game window, no overlay, two runtimes, PyInstaller AV false positives.

**Recommendation:** Electron. Wrap the Steam calls in one small bridge, so the binding can be swapped.', NULL, NULL, '2026-10-12T02:10:48Z', NULL, 182, NULL);

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
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (22, 64, '2026-10-12T00:04:57Z', '2026-10-12T00:05:48Z', 'done', NULL, 0, '5f99490ece8b9fc658cd0904b7e0972c85bcc220', 'claude-opus-5-5[1m]', '5ac41bca-defc-4ca4-8f63-883913dd2cfb', 6, 12, 4108, 201341, 32981, 0.3863242, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (23, 3, '2026-10-12T00:05:48Z', '2026-10-12T00:07:07Z', 'done', NULL, 0, 'fcdcd77201876c5380225f69e11e9fa7bb432cb1', 'claude-opus-5-5[1m]', 'ef8ffbe1-f90a-4cea-88fa-c7b6ea5eef0a', 11, 22, 6650, 405513, 36517, 0.5063266, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (24, 80, '2026-10-12T00:07:07Z', '2026-10-12T00:07:39Z', 'done', NULL, 0, '48351dca931872c2e0d97ea68840497acdbe0079', 'claude-opus-5-5[1m]', '86f247c9-de89-48c0-b89e-4eab17be46c8', 5, 10, 3444, 142563, 25794, 0.30378459999999996, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (25, 81, '2026-10-12T00:07:39Z', '2026-10-12T00:08:48Z', 'done', NULL, 0, 'bb2bbacdcd890c63fd12bf134ff61752f8ecc3da', 'claude-opus-5-5[1m]', '8c09aac5-faf4-405d-85f1-f867bf40e85f', 9, 18, 6702, 323744, 36877, 0.49387680000000006, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (26, 82, '2026-10-12T00:08:48Z', '2026-10-12T00:10:34Z', 'done', NULL, 0, '0afe9e36a55dba56a8b37abac7560c1741f690f4', 'claude-opus-5-5[1m]', '16b2f7c6-80c1-4091-a429-3a349ad84ed3', 13, 24, 10223, 517440, 50171, 0.709412, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (27, 83, '2026-10-12T00:10:34Z', '2026-10-12T00:12:00Z', 'done', NULL, 0, '62310d83ab7781dbff32a1d512609266e4bb6ab7', 'claude-opus-5-5[1m]', 'a5b33a77-0531-4f70-82c4-1cbe29ef63c4', 13, 26, 6035, 437204, 30161, 0.4495327999999999, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (28, 84, '2026-10-12T00:12:00Z', '2026-10-12T00:12:54Z', 'done', NULL, 0, '9c3900a593498d93bb40d5a20294b62923a3602b', 'claude-opus-5-5[1m]', 'e30aea65-7e96-4968-a3e2-64d42d6ff437', 10, 18, 5205, 312693, 37502, 0.4667266, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (29, 85, '2026-10-12T00:12:54Z', '2026-10-12T00:13:27Z', 'done', NULL, 0, '6856afb17ae063cec511c4c58a5781abf9c7d68f', 'claude-opus-5-5[1m]', '93cd3ef1-c029-4b57-9c4f-00bd4d822acc', 7, 14, 3359, 211757, 25913, 0.3168914, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (30, 86, '2026-10-12T00:13:27Z', '2026-10-12T00:14:39Z', 'done', NULL, 0, 'aa7ecfaa70763739bb83ca58d6a2a71501c20529', 'claude-opus-5-5[1m]', 'e1b89153-9203-488e-b78b-997064cb0dda', 10, 18, 7121, 317028, 34422, 0.4812736, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (31, 87, '2026-10-12T00:14:39Z', '2026-10-12T00:15:06Z', 'done', NULL, 0, '9ccb7d365cf7d4d255d2c43c15e99293022b4e36', 'claude-opus-5-5[1m]', '7cb5e5a9-9ce6-473d-b48f-cd241af9f2a6', 5, 10, 2682, 146953, 26760, 0.2971506, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (32, 88, '2026-10-12T00:15:06Z', '2026-10-12T00:15:35Z', 'done', NULL, 0, '3e7e03adfb6af77955939451e0026d067c70fde1', 'claude-opus-5-5[1m]', '1747bc29-143e-4f9a-9a8b-be63ea5afaba', 5, 10, 2467, 137300, 23503, 0.264864, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (33, 89, '2026-10-12T00:15:35Z', '2026-10-12T00:16:14Z', 'done', NULL, 0, '86798ec730c5965c0171a44dffdd17cce42832d5', 'claude-opus-5-5[1m]', 'eec8adb3-21b3-4c29-bb95-618aa0e20397', 6, 12, 3768, 176209, 26896, 0.32581780000000005, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (34, 90, '2026-10-12T00:16:14Z', '2026-10-12T00:16:37Z', 'done', NULL, 0, '0c48ce95e69c76fec549fc431cf3b18a5c20168b', 'claude-opus-5-5[1m]', '2be3d996-3971-49ce-a259-f2d197b10153', 5, 10, 2231, 131828, 22146, 0.24819360000000001, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (35, 4, '2026-10-12T00:16:37Z', '2026-10-12T00:17:24Z', 'done', NULL, 0, 'edc4316c5a2e73de7f630abaf1310d52470f514c', 'claude-opus-5-5[1m]', '6fe83abf-1d85-4871-988d-07ebe9593fe4', 7, 14, 4380, 216089, 29610, 0.36775380000000008, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (36, 106, '2026-10-12T00:17:24Z', '2026-10-12T00:17:54Z', 'done', NULL, 0, 'ab328d8bc1ca4095eb732f71ce01a1db755e3e4c', 'claude-opus-5-5[1m]', '70538cb7-2b9c-42ca-8de3-f2e7cd8f5cdd', 6, 12, 2848, 180214, 27498, 0.3130348, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (37, 107, '2026-10-12T00:17:54Z', '2026-10-12T00:19:38Z', 'done', NULL, 0, '108450cbd1f0af835247f1eedc5df687b5d252eb', 'claude-opus-5-5[1m]', '669603f9-cc8f-4b7e-850e-ef062460877f', 14, 26, 8949, 598914, 52311, 0.71735480000000007, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (38, 110, '2026-10-12T00:19:38Z', '2026-10-12T00:20:15Z', 'done', NULL, 0, 'b993c3ffdf9ae3482c11803a85ddc846b228d1bb', 'claude-opus-5-5[1m]', '2336a44f-548a-470c-91a9-f146233b05e1', 5, 10, 3099, 140041, 25137, 0.2911242, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (39, 5, '2026-10-12T00:20:15Z', '2026-10-12T00:22:02Z', 'done', NULL, 0, '9313e076630c764cc0b719af2fec5dff644ff162', 'claude-opus-5-5[1m]', '96a0dac8-5fbc-4034-a0a7-8f9cadd00d9d', 13, 26, 8473, 609137, 54430, 0.7268314, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (40, 114, '2026-10-12T00:22:02Z', '2026-10-12T00:22:38Z', 'done', NULL, 0, '6bef0c6b41c88617d91a3c2300bf198d3d8c9e69', 'claude-opus-5-5[1m]', '0ef5388e-bfb0-46f0-98f8-efdebb02c834', 6, 12, 3514, 193939, 31037, 0.3574118, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (41, 115, '2026-10-12T00:22:38Z', '2026-10-12T00:25:21Z', 'done', NULL, 0, '3dbac1bfbda4c3236635e8bd72a4e6aeed57251c', 'claude-opus-5-5[1m]', '43edd34a-8d41-4e04-af39-47aa4eccc1a5', 14, 28, 15778, 656573, 64141, 0.96011459999999993, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (42, 116, '2026-10-12T00:25:21Z', '2026-10-12T00:26:36Z', 'done', NULL, 0, 'cda27beb9246172310caa7bb7cd4a868e5d79f82', 'claude-opus-5-5[1m]', 'fe9f7c1e-bdbc-427b-8e1d-67278e2035b3', 11, 18, 7187, 346515, 40259, 0.53518699999999986, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (43, 117, '2026-10-12T00:26:36Z', '2026-10-12T00:28:16Z', 'done', NULL, 0, '325e9ec5e7e0e9d41c839a5d19ae33b41852dfed', 'claude-opus-5-5[1m]', '533ef7fa-60d4-43ae-bb40-739aa5bd6b49', 18, 34, 9375, 748325, 60023, 0.81748499999999991, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (44, 118, '2026-10-12T00:28:16Z', '2026-10-12T00:29:14Z', 'done', NULL, 0, '90470e86f71063c6482a8ecc69aa8c3267eb3359', 'claude-opus-5-5[1m]', 'd61f7c67-ffff-4679-935f-bbadac936d13', 12, 24, 5497, 442591, 37152, 0.49577020000000011, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (45, 119, '2026-10-12T00:29:14Z', '2026-10-12T00:29:52Z', 'done', NULL, 0, 'dac58c0bb0d926a5fc64595af85fd13c47dbaa80', 'claude-opus-5-5[1m]', 'fb29fc0e-6e81-4377-b2d7-efed779b85af', 5, 10, 4127, 157782, 30617, 0.3590724, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (46, 120, '2026-10-12T00:29:52Z', '2026-10-12T00:30:25Z', 'done', NULL, 0, '09f60000c745552efba38285927baffb9c3b8fcb', 'claude-opus-5-5[1m]', '7b4d0951-2e8b-4e4f-a024-f83a9d4700ce', 5, 10, 3249, 145386, 26691, 0.30762520000000004, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (47, 121, '2026-10-12T00:30:25Z', '2026-10-12T00:30:59Z', 'done', NULL, 0, '887b9814d53bf360f2ace8a3143af319e2ad429a', 'claude-opus-5-5[1m]', '8223788e-58c1-4687-9634-096338d24717', 5, 10, 3611, 145377, 27128, 0.3183594, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (48, 122, '2026-10-12T00:30:59Z', '2026-10-12T00:31:32Z', 'done', NULL, 0, '49790417acaf56c24ff59d7d9cd4bccce2480485', 'claude-opus-5-5[1m]', '8717ddc2-17d5-488e-bfc0-ef0657b9e2c2', 6, 12, 3416, 174242, 25147, 0.3043924, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (49, 6, '2026-10-12T00:31:32Z', '2026-10-12T00:32:33Z', 'done', NULL, 0, '6262f5802b6c5b1fade0950c0366b229ce836a38', 'claude-opus-5-5[1m]', '5d235fd1-3ff2-4e75-9bb3-105a9731f335', 10, 18, 5732, 342880, 38435, 0.49076800000000004, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (50, 134, '2026-10-12T00:32:33Z', '2026-10-12T00:33:22Z', 'done', NULL, 0, '628ee8aaabbc958ab2a40c538f11137dd40e8052', 'claude-opus-5-5[1m]', '9919c7ba-6fc1-4735-8ae7-37bd209d7d2c', 8, 16, 4710, 268736, 34111, 0.42089920000000003, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (51, 135, '2026-10-12T00:33:22Z', '2026-10-12T00:34:38Z', 'done', NULL, 0, '1e4f9f203abdfae13d97b609611a03b9c191305d', 'claude-opus-5-5[1m]', '7a27c0ff-b031-444f-b3ca-6d79e93d587a', 10, 20, 4511, 360873, 37034, 0.45874660000000006, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (52, 136, '2026-10-12T00:34:38Z', '2026-10-12T00:35:14Z', 'done', NULL, 0, 'f66b83b0826fd7a28c82b17ed22d01f12937ec3a', 'claude-opus-5-5[1m]', 'dcf5fdea-cb31-4515-aef0-b7edee5e07ec', 6, 12, 3488, 193246, 33780, 0.3786972, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (53, 137, '2026-10-12T00:35:14Z', '2026-10-12T00:35:36Z', 'done', NULL, 0, '29ad06258100c9e7d1dbca21944e0f1793d19d46', 'claude-opus-5-5[1m]', '1db34157-9dcd-4e8e-9c21-d63ae7bd3015', 5, 10, 2341, 133851, 22683, 0.2550942, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (54, 138, '2026-10-12T00:35:36Z', '2026-10-12T00:36:10Z', 'done', NULL, 0, 'dd574936c557333b110868a421b4966cec0dccef', 'claude-opus-5-5[1m]', '802f81ce-9f22-4c8e-a143-c711d4fea11a', 5, 10, 3372, 145058, 26526, 0.3086996, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (55, 139, '2026-10-12T00:36:10Z', '2026-10-12T00:36:45Z', 'done', NULL, 0, 'c3f802cfe9a5ebaaeaedf53feedc54da1d1092e9', 'claude-opus-5-5[1m]', '5e48d658-4a13-49c6-9fd8-a4d0bb43b592', 5, 10, 3531, 146738, 28783, 0.3302716, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (56, 7, '2026-10-12T00:36:45Z', '2026-10-12T00:38:19Z', 'done', NULL, 0, 'aa323f30031742363fdc041797c03f838aec1ef2', 'claude-opus-5-5[1m]', '3c482457-76a4-49f9-82b6-20bc1945a04f', 13, 26, 9065, 617366, 56610, 0.75775719999999991, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (57, 151, '2026-10-12T00:38:19Z', '2026-10-12T00:39:00Z', 'done', NULL, 0, '3b6f901730b7596320d7e4f88e6894ae668e18f9', 'claude-opus-5-5[1m]', '329bbc6f-7271-4c54-817f-3d503a782533', 6, 12, 4484, 181096, 27251, 0.34395519999999996, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (58, 162, '2026-10-12T00:39:00Z', '2026-10-12T00:39:26Z', 'done', NULL, 0, '28f62b5f898ca2e2d7be301b184e7f28ffde696f', 'claude-opus-5-5[1m]', 'fe939d73-121d-4575-be7e-cc929bbb2a34', 5, 10, 1932, 145256, 25438, 0.27123520000000007, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (59, 163, '2026-10-12T00:39:27Z', '2026-10-12T00:39:55Z', 'done', NULL, 0, '350427cee4811a071ebc75c14379dfab6776ed4c', 'claude-opus-5-5[1m]', 'dbecc7b6-b72e-4872-8e78-0c159e940683', 6, 12, 2664, 197763, 32552, 0.35329659999999996, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (60, 164, '2026-10-12T00:39:55Z', '2026-10-12T00:41:14Z', 'done', NULL, 0, '2074a341a37cd2db64a11bd2f97bcb978ec40e04', 'claude-opus-5-5[1m]', '23aed49f-002b-4f2d-8c28-2b5f14fe6986', 11, 20, 7664, 421197, 52399, 0.6567914, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (61, 165, '2026-10-12T00:41:14Z', '2026-10-12T00:41:58Z', 'done', NULL, 0, '0968f233ac9f95da94c965e1198e22eb10328c78', 'claude-opus-5-5[1m]', '3776f64b-3400-4590-8b1f-1a64005b7825', 10, 20, 4209, 383866, 40750, 0.4870332, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (62, 166, '2026-10-12T00:41:58Z', '2026-10-12T00:42:42Z', 'done', NULL, 0, '1148a7244df7b708b5885735889dbbf4119466fc', 'claude-opus-5-5[1m]', '24a16517-618d-48d3-94d5-c5555b1574f0', 8, 16, 4372, 270184, 31270, 0.39170080000000007, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (63, 167, '2026-10-12T00:42:42Z', '2026-10-12T00:43:22Z', 'done', NULL, 0, 'b0f94409082aa93100f6d9b990f8eb6bade01d83', 'claude-opus-5-5[1m]', 'f179348f-5bc9-4e25-bcae-ce50834388bc', 7, 14, 3366, 220746, 29459, 0.3471972, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (64, 168, '2026-10-12T00:43:22Z', '2026-10-12T00:43:59Z', 'done', NULL, 0, '123481c9aa12a9972eb7256347b740036df3f14d', 'claude-opus-5-5[1m]', 'f97dc7c0-d112-4eba-9593-40bb2c3d7d8e', 8, 16, 3366, 266623, 31133, 0.3697726, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (65, 169, '2026-10-12T00:43:59Z', '2026-10-12T00:44:36Z', 'done', NULL, 0, 'b4d3dc057fe20d2212a82c534ede04f613c031ff', 'claude-opus-5-5[1m]', '165572df-89d6-422f-82a3-a944c06ed173', 9, 16, 3649, 270690, 34444, 0.40273399999999993, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (66, 170, '2026-10-12T00:44:36Z', '2026-10-12T00:45:27Z', 'done', NULL, 0, '9cc27ddbbeefc6bcb52aafe5e57a4caff6712153', 'claude-opus-5-5[1m]', 'e4559d6a-8747-4728-92c3-d92d59184920', 14, 26, 4802, 523554, 37390, 0.49997479999999989, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (67, 171, '2026-10-12T00:45:27Z', '2026-10-12T00:46:19Z', 'done', NULL, 0, '44d7a52342e579c657bff3bd1d203bc638928ad8', 'claude-opus-5-5[1m]', 'f6187c6f-9141-4726-a762-fb90889bfe99', 8, 16, 4298, 287612, 37657, 0.4448024, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (68, 172, '2026-10-12T00:46:19Z', '2026-10-12T00:46:40Z', 'done', NULL, 0, 'a0d5a742e3005af028fda69825c387fae521af1c', 'claude-opus-5-5[1m]', '339ea660-fce4-4f46-90f8-5813f68d7d3a', 5, 10, 2010, 131867, 21311, 0.23710140000000002, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (69, 173, '2026-10-12T00:46:40Z', '2026-10-12T00:47:06Z', 'done', NULL, 0, '5f66200134b9f9436ea6e9dbf2bcd90fb6e0b138', 'claude-opus-5-5[1m]', 'a02e603c-8c95-4185-b093-0277c73f4ee6', 4, 8, 1896, 101830, 22211, 0.236006, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (70, 174, '2026-10-12T00:47:06Z', '2026-10-12T00:47:44Z', 'done', NULL, 0, 'ec676d8f4e5438ff656c70a49dbfcc3df48fdb3a', 'claude-opus-5-5[1m]', 'e0933653-8490-4dc1-89ec-6bca68304c7d', 6, 12, 3878, 190531, 30447, 0.35929019999999995, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (71, 175, '2026-10-12T00:47:44Z', '2026-10-12T00:48:13Z', 'done', NULL, 0, '178a84015e665cb1c30f105255077ef004d84334', 'claude-opus-5-5[1m]', '3d7df2a2-5c87-439e-a6ea-99f7bd641a99', 5, 10, 2484, 125504, 20183, 0.2362848, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (72, 176, '2026-10-12T00:48:13Z', '2026-10-12T00:48:35Z', 'done', NULL, 0, '2124038a57b5015f3a4e91c6c4a4053af523351b', 'claude-opus-5-5[1m]', 'ff6789bf-3a31-4d6a-bc38-185e10e9f4c1', 5, 10, 2289, 138957, 25582, 0.2782674, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (73, 177, '2026-10-12T00:48:35Z', '2026-10-12T00:48:59Z', 'done', NULL, 0, 'd8e8fa860302c2d2177f4cd1204c046b7f869acc', 'claude-opus-5-5[1m]', 'b24a26e5-2123-48e0-b3ab-aba19167f3ab', 4, 6, 2542, 72584, 24787, 0.2636768, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (74, 178, '2026-10-12T00:48:59Z', '2026-10-12T00:49:49Z', 'done', NULL, 0, 'db9d01b516784d649f6d93369eff0398eb9978d0', 'claude-opus-5-5[1m]', '022cd1ad-3de4-4fc2-b9c0-3341920b6041', 8, 16, 5232, 265681, 30190, 0.39936019999999994, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (75, 179, '2026-10-12T00:49:49Z', '2026-10-12T00:50:14Z', 'done', NULL, 0, '36ce9f055935129958cb26493cbf7027edf758e4', 'claude-opus-5-5[1m]', '66e85f33-14fd-4787-979a-4aa66167404b', 5, 10, 2615, 135545, 22992, 0.263385, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (76, 180, '2026-10-12T00:50:14Z', '2026-10-12T00:50:43Z', 'done', NULL, 0, '5025c8633aee3f5aa586222a9097788e437866c1', 'claude-opus-5-5[1m]', 'b23eb71a-4dc8-4043-a734-6c197147b7a2', 5, 10, 2973, 143617, 26259, 0.2982954, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (77, 181, '2026-10-12T00:50:43Z', '2026-10-12T00:51:13Z', 'done', NULL, 0, 'daf6bd27f2f0c08c14863a72ecfdc257d3ecb10c', 'claude-opus-5-5[1m]', '9265f951-bbab-4d3b-bd84-b3674781b041', 5, 10, 2624, 147857, 27724, 0.3038834, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (78, 8, '2026-10-12T00:51:14Z', '2026-10-12T00:52:54Z', 'done', NULL, 0, 'c915c05219cdd9fbbaffbdc70d9ccd3109280dfd', 'claude-opus-5-5[1m]', 'd93901ef-0cc7-4e68-be21-e1ea094eed89', 12, 22, 9677, 451848, 51253, 0.6940216, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (79, 208, '2026-10-12T00:52:54Z', '2026-10-12T00:53:53Z', 'done', NULL, 0, 'a8ef981539569ec3963c70ea33813b1730c84051', 'claude-opus-5-5[1m]', '2bc8338c-bf13-4a99-8841-075799a52112', 8, 16, 6150, 327810, 46217, 0.558362, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (80, 212, '2026-10-12T00:53:53Z', '2026-10-12T00:56:14Z', 'done', NULL, 0, 'b5df7182db45f421334edaebbface98b604f85a7', 'claude-opus-5-5[1m]', 'c0d62dab-72a4-45e4-b06b-1f36198be63f', 14, 20, 13767, 494026, 63071, 0.87879319999999994, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (81, 213, '2026-10-12T00:56:14Z', '2026-10-12T00:58:37Z', 'done', NULL, 0, '7386a4b72c6454f65f50d548f69def20196acdae', 'claude-opus-5-5[1m]', '67171dce-a404-4450-a752-d8228b7685a2', 13, 26, 13902, 606088, 57745, 0.86132159999999991, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (82, 214, '2026-10-12T00:58:37Z', '2026-10-12T01:00:37Z', 'done', NULL, 0, '8cab26d6dce119a55f167c1adbeb1a51eaa53089', 'claude-opus-5-5[1m]', '64c3dc00-b4c6-42ed-9808-48e3e6f4f2b2', 18, 34, 11314, 887842, 66537, 0.9362803999999999, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (83, 215, '2026-10-12T01:00:37Z', '2026-10-12T01:02:45Z', 'done', NULL, 0, 'b70a9336f95a293c8673592a06fa411a9d01ed1b', 'claude-opus-5-5[1m]', '179066a4-08b8-48a4-82ee-8821eab60359', 15, 30, 12372, 688261, 58275, 0.85141220000000006, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (84, 216, '2026-10-12T01:02:45Z', '2026-10-12T01:04:11Z', 'done', NULL, 0, '2a00239b3a701c7a4957c1debfb8beaf7e62766a', 'claude-opus-5-5[1m]', '8a00b665-f8d3-47e8-9619-c262df80cb25', 13, 22, 8318, 447245, 46264, 0.62600900000000015, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (85, 217, '2026-10-12T01:04:11Z', '2026-10-12T01:04:43Z', 'done', NULL, 0, 'b99006b5b5b4674068fb4724c51ce840ce989bcb', 'claude-opus-5-5[1m]', 'd156c9ef-d0b7-404d-a27d-c5c1403bef3a', 5, 10, 3281, 156802, 29071, 0.3295884, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (86, 218, '2026-10-12T01:04:43Z', '2026-10-12T01:05:20Z', 'done', NULL, 0, '592fc7fdbb0b3e7715e2c76486f3460cae1f9e24', 'claude-opus-5-5[1m]', 'b8d1cd04-72b3-49a6-9ea5-810fa620663e', 7, 14, 4029, 215953, 28191, 0.3493546, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (87, 219, '2026-10-12T01:05:21Z', '2026-10-12T01:05:52Z', 'done', NULL, 0, 'f08803b3cbe6028a60146ddd82e40a230a4e5316', 'claude-opus-5-5[1m]', 'abb5b477-9f26-4530-8121-353a38d45891', 5, 10, 3070, 161592, 32421, 0.35312640000000006, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (88, 220, '2026-10-12T01:05:52Z', '2026-10-12T01:06:28Z', 'done', NULL, 0, '708739fdb6ab6142131fd60fd5a244fbc0368e10', 'claude-opus-5-5[1m]', 'd9401651-6429-4bd8-aa1e-804203465ead', 6, 12, 3824, 189406, 29308, 0.3488732, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (89, 221, '2026-10-12T01:06:28Z', '2026-10-12T01:07:25Z', 'done', NULL, 0, 'f7a29de95ea702b1946f47f6b8d5b37b80b8b4a6', 'claude-opus-5-5[1m]', 'd1ee0391-da39-4384-8cfb-dbffd1cbd0af', 9, 18, 6106, 310040, 32612, 0.44509600000000005, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (90, 9, '2026-10-12T01:07:26Z', '2026-10-12T01:09:45Z', 'done', NULL, 0, '42689dd2e13e74beb576671ac9192ac088dadcfd', 'claude-opus-5-5[1m]', 'e9d0eccc-e33a-4e2e-854d-2c1e902a4082', 12, 24, 11849, 647075, 84247, 1.040467, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (91, 239, '2026-10-12T01:09:45Z', '2026-10-12T01:11:08Z', 'done', NULL, 0, '821c4a922e93ba26c68b49ae89c16c1f301d350d', 'claude-opus-5-5[1m]', '93e6fa81-9603-473b-aeb3-b23f830af4ae', 9, 18, 8915, 372158, 44673, 0.6101876, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (92, 10, '2026-10-12T01:11:08Z', '2026-10-12T01:12:55Z', 'done', NULL, 0, '268cd0a317a19089a143e6b39ecf3b96921991f6', 'claude-opus-5-5[1m]', 'b997afa5-855d-45ce-af5c-78efa6623016', 11, 22, 10472, 578005, 76797, 0.93950500000000015, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (93, 252, '2026-10-12T01:12:55Z', '2026-10-12T01:14:05Z', 'done', NULL, 0, 'a81f4f061f84625c548d35857d777496fcd21c36', 'claude-opus-5-5[1m]', '37c1b395-402a-4d41-8086-62e23401ca49', 7, 14, 7648, 307258, 52507, 0.6345236, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (94, 11, '2026-10-12T01:14:05Z', '2026-10-12T01:15:22Z', 'done', NULL, 0, '3dbc8d6dd51952e9a18895c48e52e946655f1b5a', 'claude-opus-5-5[1m]', '39d45d05-1317-4b13-8ea2-41214bfe7f2f', 8, 16, 7126, 293706, 42144, 0.5384772, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (95, 264, '2026-10-12T01:15:22Z', '2026-10-12T01:16:22Z', 'done', NULL, 0, '443f2660c596b68d2f06273c50e0e1066f669701', 'claude-opus-5-5[1m]', '25f5fa09-d0cc-40c7-9b40-1e928ccfb717', 8, 16, 6109, 302524, 38039, 0.4870608, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (96, 111, '2026-10-12T01:16:22Z', '2026-10-12T01:17:39Z', 'done', NULL, 0, 'fc06477fae30d3e7b96c077ff88e59e3d6ef46b9', 'claude-opus-5-5[1m]', 'c4eb59b7-b2db-4e19-9163-73d939642fa0', 10, 20, 6073, 349739, 30974, 0.43927979999999994, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (97, 112, '2026-10-12T01:17:39Z', '2026-10-12T01:19:30Z', 'done', NULL, 0, '45622b612c8c3ad4ae198d64f07eab44cc18700a', 'claude-opus-5-5[1m]', '27f2bb00-c52d-49c2-9dda-e696f75cf000', 28, 46, 10671, 1125475, 50504, 0.84273100000000012, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (98, 113, '2026-10-12T01:19:30Z', '2026-10-12T01:26:11Z', 'blocked', NULL, 0, '4b81cdd472403d6cb17c61cf9fd1542c7b7cf8ca', 'claude-opus-5-5[1m]', '2f30ec08-45d4-4159-9527-fa6006c00d7e', 20, 40, 11314, 883678, 46584, 0.7758476, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (99, 29, '2026-10-12T01:26:11Z', '2026-10-12T01:28:28Z', 'done', NULL, 0, 'ef824b4742e8dac6436b132f47f8ae79b36c3a65', 'claude-opus-5-5[1m]', '4b54a0e4-f6d7-4d3a-b668-f50d8fcfeaa5', 29, 48, 14654, 1388065, 61137, 1.0599810000000003, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (100, 40, '2026-10-12T01:28:28Z', '2026-10-12T01:31:18Z', 'done', NULL, 0, '6d3039b1ebffb3d039d3843d05f8bf04edbe2f45', 'claude-opus-5-5[1m]', '6bf25820-4627-45d9-88ef-f2a90e9119eb', 32, 50, 14516, 1250925, 51211, 0.950393, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (101, 273, '2026-10-12T01:31:18Z', '2026-10-12T01:32:00Z', 'done', NULL, 0, 'd1c6c85e8941782cf678ae98da860c2269b66b93', 'claude-opus-5-5[1m]', 'aa9e3408-90ab-4404-a02e-85715f29a60b', 9, 18, 3903, 296965, 29304, 0.371957, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (102, 274, '2026-10-12T01:32:00Z', '2026-10-12T01:40:04Z', 'done', NULL, 0, '22e3c606c10eaa85934bda165e2f23ebd000f320', 'claude-opus-5-5[1m]', '57fa7b83-e1a9-4c43-b7d8-f26de972c29f', 48, 78, 20869, 2723785, 87667, 1.6637850000000003, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (103, 98, '2026-10-12T01:40:04Z', '2026-10-12T01:43:52Z', 'done', NULL, 0, 'eda6cf1f3297345e9c9a5799746adedcf86b886d', 'claude-opus-5-5[1m]', 'ded98f99-0eb8-4d46-8ebe-28f69ddcbfa0', 31, 60, 21359, 1705718, 65605, 1.2934036, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (104, 30, '2026-10-12T01:43:52Z', '2026-10-12T01:45:52Z', 'done', NULL, 0, '65dfb685bdafae2d15e62823e834c1280e734cf2', 'claude-opus-5-5[1m]', 'df5fc368-5507-46a6-8436-3202d31b88be', 14, 28, 4501, 472774, 29225, 0.4184868, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (105, 31, '2026-10-12T01:45:52Z', '2026-10-12T01:46:58Z', 'done', NULL, 0, '60dda716d22441137dc4a22602ad4026053b31db', 'claude-opus-5-5[1m]', 'c8081eaf-7d31-4630-969a-fe5be9bd4bc7', 14, 26, 5601, 447069, 30854, 0.4483698, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (106, 34, '2026-10-12T01:46:58Z', '2026-10-12T01:48:01Z', 'done', NULL, 0, '00d812eea32fe2a2577c7851f4eeac7fdef122f8', 'claude-opus-5-5[1m]', 'e20a3efe-c22e-4d41-aaff-61e6033b3606', 15, 28, 5983, 719147, 57040, 0.71992140000000016, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (107, 42, '2026-10-12T01:48:01Z', '2026-10-12T01:49:46Z', 'done', NULL, 0, '3dafa7fa2b5ad9fb64562c030f2e40cef22b7e7b', 'claude-opus-5-5[1m]', '314cc15b-e1f0-431b-b09e-a5dafe8dbb4e', 27, 44, 10852, 992751, 44938, 0.77527020000000013, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (108, 65, '2026-10-12T01:49:46Z', '2026-10-12T01:51:39Z', 'done', NULL, 0, 'abb1444f04641fba0b4cb65fc0fc26a70fa9c3af', 'claude-opus-5-5[1m]', 'f360a04e-0bb9-4576-b3e1-743918d7866b', 11, 22, 12296, 511964, 52662, 0.76969679999999985, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (109, 66, '2026-10-12T01:51:39Z', '2026-10-12T01:53:09Z', 'done', NULL, 0, '91777b6494ac4722d52b03d9a3597403b0fd2ec3', 'claude-opus-5-5[1m]', 'f176786e-0625-4b9e-82e9-9f44d82648da', 15, 26, 8328, 618126, 49058, 0.68275320000000006, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (110, 67, '2026-10-12T01:53:09Z', '2026-10-12T01:55:59Z', 'done', NULL, 0, 'a16cc236fb6635c2d6cc24894f1afc13f62821d4', 'claude-opus-5-5[1m]', '01eddb41-34fe-4ac4-a075-7a23d77b0445', 17, 30, 9072, 629079, 41587, 0.64007180000000008, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (111, 68, '2026-10-12T01:55:59Z', '2026-10-12T01:58:51Z', 'done', NULL, 0, 'c60b0f3bf366641e8f08b0fef33f6fa3ba1a5de8', 'claude-opus-5-5[1m]', '2ba942bb-8d15-4f71-89f6-c33f82760071', 16, 24, 17388, 635948, 60496, 0.9590136, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (112, 69, '2026-10-12T01:58:51Z', '2026-10-12T02:00:38Z', 'failed', 'the worker left changes that are not staged:
 M flake.lock', 0, '2b43282a9aa9fb29b08d22617c8916e06ac07604', 'claude-opus-5-5[1m]', '51ba72b0-a037-4d1f-9559-928930986143', 12, 20, 9289, 503466, 57556, 0.74700120000000014, 80113);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (113, 70, '2026-10-12T02:04:49Z', '2026-10-12T02:08:14Z', 'done', NULL, 0, '6ea9c260adfe15a281659a9367171dcda2d38d3c', 'claude-opus-5-5[1m]', 'ad225721-f683-483c-bbd5-84769812b162', 19, 38, 13264, 1032553, 61438, 0.96344660000000026, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (114, 71, '2026-10-12T02:08:14Z', '2026-10-12T02:09:47Z', 'done', NULL, 0, '592295ae0134ec9973121e4882a6d709ea9cbd20', 'claude-opus-5-5[1m]', 'ea1ea066-39bb-45e9-89d4-81bf17aa7c8e', 13, 24, 6941, 481561, 40993, 0.5631722, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (115, 182, '2026-10-12T02:09:47Z', '2026-10-12T02:11:11Z', 'done', NULL, 0, 'edffe68621ae6a27c0fa04a15c87623b0a4a25d7', 'claude-opus-5-5[1m]', '309f2e2f-cd40-4a02-aef1-926d94ee7c9e', 18, 32, 7208, 593681, 36153, 0.55224820000000008, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (116, 25, '2026-10-12T02:11:11Z', '2026-10-12T02:12:10Z', 'done', NULL, 0, '1b10c1f0a8953f816da344934b258f64d2e9a4d0', 'claude-opus-5-5[1m]', 'eeffabf8-b4a2-40b3-8fdf-32b23fa570ef', 16, 30, 5990, 615555, 40131, 0.564079, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (117, 26, '2026-10-12T02:12:10Z', '2026-10-12T02:12:53Z', 'done', NULL, 0, '8bc8f45edf0937356cbc706f3d52873b7e626a70', 'claude-opus-5-5[1m]', '2757d6a2-a896-4943-9fb1-5e0bcb49403c', 16, 28, 4161, 470158, 29830, 0.41600360000000003, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (118, 35, '2026-10-12T02:12:53Z', '2026-10-12T02:13:45Z', 'done', NULL, 0, '5a6ec0987edf91428e4feba45d902e91b5863094', 'claude-opus-5-5[1m]', 'a774a763-043e-4d06-9e7d-19003044e627', 19, 30, 5228, 553300, 32769, 0.477492, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (119, 32, '2026-10-12T02:13:45Z', '2026-10-12T02:14:07Z', 'done', NULL, 0, '77c0c3b4618a419f26f5fe4da11ee87271471fd8', 'claude-opus-5-5[1m]', '03978830-a008-4fc4-b8f8-4151c132a874', 9, 18, 1773, 296708, 27680, 0.3163136, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (120, 36, '2026-10-12T02:14:07Z', '2026-10-12T02:17:21Z', 'done', NULL, 0, '08ee712be02e3a256dea5791671aa1f1f691f5c7', 'claude-opus-5-5[1m]', '116aa6b4-22ae-4696-af49-8b80917434d1', 30, 54, 16924, 1429487, 58455, 1.0922334000000002, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (121, 44, '2026-10-12T02:17:21Z', '2026-10-12T02:17:43Z', 'failed', 'still open and not blocked', 0, '21d6534a8bf026cd138e58e23acb043d2bc414f2', 'claude-opus-5-5[1m]', '17e748ae-1eb0-46ea-86b0-9a47cffae6ab', 6, 12, 1782, 173875, 25733, 0.276327, 159754);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (122, 113, '2026-10-12T02:35:53Z', '2026-10-12T02:36:23Z', 'done', NULL, 0, '016e5df3377c9006f2053d819260db6dbe2ca89a', 'claude-opus-5-5[1m]', '42ec4817-94cf-4f2b-a10c-cd51ce960a76', 8, 16, 2827, 228644, 23558, 0.2907968, 175567);

INSERT INTO task_decision (task_id, decision_id) VALUES (25, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (26, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (27, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (28, 1);
INSERT INTO task_decision (task_id, decision_id) VALUES (28, 2);
INSERT INTO task_decision (task_id, decision_id) VALUES (32, 11);
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
INSERT INTO task_decision (task_id, decision_id) VALUES (97, 6);
INSERT INTO task_decision (task_id, decision_id) VALUES (101, 6);
INSERT INTO task_decision (task_id, decision_id) VALUES (105, 7);
INSERT INTO task_decision (task_id, decision_id) VALUES (108, 8);
INSERT INTO task_decision (task_id, decision_id) VALUES (109, 8);
INSERT INTO task_decision (task_id, decision_id) VALUES (113, 10);
INSERT INTO task_decision (task_id, decision_id) VALUES (183, 12);
INSERT INTO task_decision (task_id, decision_id) VALUES (227, 9);
INSERT INTO task_decision (task_id, decision_id) VALUES (228, 9);
INSERT INTO task_decision (task_id, decision_id) VALUES (229, 9);
INSERT INTO task_decision (task_id, decision_id) VALUES (230, 9);
INSERT INTO task_decision (task_id, decision_id) VALUES (231, 9);
INSERT INTO task_decision (task_id, decision_id) VALUES (241, 2);
