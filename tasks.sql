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
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (2, 2, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:55Z', NULL);
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

INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (1, 1, 'write the masterplan', 'masterplan', 'done', NULL, '2026-10-11, plan 1 body; plans/decisions.md (D-52), plans/open-questions.md, plans/project.md (OQ-17 resolved)', 'Write plan 1, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T20:08:18Z', '2026-10-11T23:15:56Z', NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (2, 2, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 2, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', NULL, NULL);
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
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (14, 1, 'write plan: aim batches at difficulty gaps', 'plan', 'open', 1000, NULL, 'Write the plan for part 2 of the masterplan (plan 1, B-6): `pm plan add 1 "Aim batches at difficulty gaps" --priority 700`.

- `draft` draws target difficulties weighted by the gap to part 1''s targets (decision 1), not evenly (D-40); subcategory choice should consider difficulty gaps too.
- Measure first: target vs. rated vs. reviewed difficulty for batch-7 and batch-8; where do 11–15 targets land?
- Fix prompts or concept `known_at` choice where hard drafts come out at 7–9. These are implementation tasks on `qgen.py`/prompts, never workarounds inside a batch run (RUNBOOK).
- Depends on part 1''s target storage; refer to that plan once it exists (`pm plan list`).', '2026-10-11T23:16:50Z', NULL, 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (15, 1, 'write plan: more subcategories', 'plan', 'open', 1000, NULL, 'Write the plan for part 3 of the masterplan (plan 1): `pm plan add 1 "More subcategories" --priority 600`.

- Find saturated `base` subcategories: approved count, concept-list use, duplicate rate, avoid-list length.
- Propose new subcategories, especially ones that carry hard (11–15) questions, with draft concept lists.
- Which ones to add is the gamemaster''s call (RUNBOOK): the plan''s analysis task raises a decision with the proposals as options; the task that adds them to `app/data/categories.json` waits for it.', '2026-10-11T23:16:50Z', NULL, 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (16, 1, 'write plan: duplicate and drift detection', 'plan', 'open', 1000, NULL, 'Write the plan for part 4 of the masterplan (plan 1, B-5; absorbs PE-6, PE-13, MP-11): `pm plan add 1 "Duplicate and drift detection" --priority 700`.

- Pre-merge overlap check of drafts against the whole approved pool by answer, concept and topic, not only question text (`dedupe`), so overlaps get dropped instead of ending up `needs_work` (cf. q-0644/q-0957, q-0646/q-0217, q-0689/q-0279).
- Per-batch health metrics in `authoring/reports/<batch>.md` and a cross-batch comparison: drop rate, needs_work rate by reason, duplicate rate, difficulty spread vs. targets, axis/style variety, cost per approved question.
- Thresholds that say "stop and look before the next batch"; they feed the milestone''s exit check.
- Close or update PE-6, PE-13, MP-11, B-5 in `plans/backlog.md` as the plan covers them.', '2026-10-11T23:16:50Z', NULL, 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (17, 1, 'write plan: quality control after every batch', 'plan', 'open', 1000, NULL, 'Write the plan for part 5 of the masterplan (plan 1): `pm plan add 1 "Quality control after every batch" --priority 650`.

- (a) LLM audit with its own prompt (not `review.md`) on a sample of a batch: facts, ambiguity, giveaways, difficulty, house style; results into the batch report.
- (b) Human spot check: random sample in the review tool (e.g. a sample filter on `/review?batch=…`), recording agree/disagree with the LLM verdict. Sample size and agreement rate: decision 2.
- (c) Procedure that turns findings into prompt or house-style changes before the next batch; documented in `authoring/RUNBOOK.md` or a plan file.
- Trend over batches of the human/LLM disagreement rate.
- Only the tooling and procedure; the QC runs themselves are tasks of part 6.', '2026-10-11T23:16:50Z', NULL, 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (18, 1, 'write plan: batch runs', 'plan', 'open', 1000, NULL, 'Write the plan for part 6 of the masterplan (plan 1): `pm plan add 1 "Batch runs" --priority -100`.

- Plan priority -100: every task that runs `qgen batch` must run only after all implementation work (milestone 1).
- First tasks: finish batch-8 (`work/batch-8`, commit d7fb13f) per `authoring/RUNBOOK.md`, then its QC (part 5''s procedure, once that exists), then the next batch. Add batch tasks one or two at a time, not all ~8 up front; the plan says that each batch task adds the next one while targets (part 1) are unmet.
- needs_work handling per decision 3 (RUNBOOK: `qgen rework` only on the gamemaster''s word).
- Watch media yield; if missing media limits throughput, propose a new plan with `plans/06-images.md`, `plans/23-media-providers.md`, IMG-16/17.
- Last task: the exit check from part 1, plus `qgen validate` and `trivia-media sync --status approved`.', '2026-10-11T23:16:50Z', NULL, 12);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (19, 12, 'create tasks for plan 12', 'split', 'open', 1000, NULL, 'Split plan 12 into tasks and identify all decisions that need to be made. If the plan already has tasks,
bring them in line with the plan. A task that writes a plan gets `--kind plan`.', '2026-10-11T23:39:28Z', NULL, 13);

INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (1, 'Target count per difficulty (1–15) for 5000 approved base questions?', 'pending', '["1: 250 · 2: 350 · 3–8: 450 each · 9–11: 330 each · 12–13: 230 each · 14–15: 125 each (sum 5000)", "masterplan draft: 1–2: 490 each · 3–8: 420 each · 9–11: 300 each · 12–13: 200 each · 14–15: 100 each (sum 5000)", "flat: 333 per level (5 extra at 6–10)"]', 'Milestone 1, part 1 (D-52). Today (2026-10-11) approved base by difficulty: 1: 36 · 2: 67 · 3: 96 · 4: 104 · 5: 112 · 6: 147 · 7: 101 · 8: 67 · 9: 74 · 10: 57 · 11: 61 · 12: 38 · 13: 48 · 14: 19 · 15: 8.
The targets steer `draft` (part 2: aim at the gaps) and are the milestone''s exit check.
Recommended curve tapers at both ends; the masterplan draft puts more at 1–2 than at the middle levels, which is likely more easy questions than game nights need.', NULL, NULL, '2026-10-11T23:16:33Z', NULL, 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (2, 'When is batch quality "fine": human spot-check size and agreement rate with the LLM review?', 'pending', '["30 random questions per batch; ≥ 90% agreement in each of the last two batches", "50 per batch; ≥ 95% agreement", "20 per batch; ≥ 85% agreement"]', 'Milestone 1, parts 1 and 5. After every batch the gamemaster checks a random sample in the review tool and records agree/disagree with the LLM verdict. This rate is the main "quality is fine" signal and part of the milestone''s exit check (last two batches).
30 questions take roughly 10–15 minutes; 50 gives a tighter rate but costs more of the human''s time per batch (~8 batches left).', NULL, NULL, '2026-10-11T23:16:33Z', NULL, 12, NULL);
INSERT INTO decision (id, subject, status, options, body, answer, reason, created_at, closed_at, created_by_task, signoff) VALUES (3, 'How are needs_work questions (33 now, more per batch) resolved?', 'pending', '["qgen rework once after each batch''s QC, then the gamemaster decides what is still needs_work in the review tool", "the gamemaster decides all of them in the review tool; no qgen rework", "leave them; only approved questions count toward 5000"]', 'Milestone 1, part 6. RUNBOOK: `qgen rework` runs only on the gamemaster''s word; this answer is that word for the batch tasks of this milestone. batch-7 needs_work reasons: mostly giveaway hints, overlap with a pool question, or no usable media.
Rework costs LLM calls but saves the gamemaster''s time; overlaps (once part 4 drops them before merge) and media misses don''t benefit from rework.', NULL, NULL, '2026-10-11T23:16:33Z', NULL, 12, NULL);

INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (1, 1, '2026-10-11T23:14:36Z', '2026-10-11T23:16:05Z', 'done', NULL, 0, 'd7fb13f0580397cd7e3cb79641c26f1f67ace8b0', 'claude-opus-5-5[1m]', '102a6d61-be2f-483e-83e1-57951f33bbef', 14, 28, 8375, 677422, 59914, 0.78240839999999989, 73367);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (2, 12, '2026-10-11T23:16:05Z', '2026-10-11T23:17:00Z', 'done', NULL, 0, 'c4bab21ed411ec2cadb1435ebb3fa8c838bbca71', 'claude-opus-5-5[1m]', 'e075f121-119b-411e-af9c-9034110e6417', 6, 12, 5681, 191036, 29983, 0.3917392, 73367);
INSERT INTO run (id, task_id, started_at, ended_at, result, reason, exit_code, base_commit, model, session_id, turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, pid) VALUES (3, 13, '2026-10-11T23:38:39Z', '2026-10-11T23:39:37Z', 'done', NULL, 0, '695c887e9c67db86f9ee0d3940dbc6cdd1f21c7c', 'claude-opus-5-5[1m]', 'cdb8babf-965b-40c1-b805-81625b28c7ff', 10, 20, 5455, 395561, 43117, 0.5332282, 80113);
