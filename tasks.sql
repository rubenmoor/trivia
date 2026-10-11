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

INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (1, 1, 'masterplan', 1000, 'tbd.', '2026-10-11T20:08:18Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (2, 2, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (3, 3, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:55Z', NULL);
INSERT INTO plan (id, milestone_id, subject, priority, body, created_at, created_by_task) VALUES (4, 4, 'masterplan', 1000, 'tbd.', '2026-10-11T21:54:55Z', NULL);

INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (1, 1, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 1, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T20:08:18Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (2, 2, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 2, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (3, 3, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 3, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', NULL, NULL);
INSERT INTO task (id, plan_id, subject, kind, status, priority, note, body, created_at, retired_at, created_by_task) VALUES (4, 4, 'write the masterplan', 'masterplan', 'open', NULL, NULL, 'Write plan 4, the masterplan of this milestone: expand on everything that needs to be done to achieve it,
divided into parts. State in the masterplan that its own tasks are not implementation work: each of them writes the
plan for one part.', '2026-10-11T21:54:55Z', NULL, NULL);
