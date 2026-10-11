-- pm database. Change it with pm; after a hand edit run `pm validate`.
PRAGMA user_version = 5;

CREATE TABLE milestone (
    id           INTEGER PRIMARY KEY,
    title        TEXT NOT NULL CHECK (trim(title) <> ''),
    status       TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'implemented')),
    description  TEXT NOT NULL DEFAULT '',                 -- Markdown
    created_date TEXT NOT NULL DEFAULT (date('now'))
) STRICT;

CREATE TABLE plan (
    id           INTEGER PRIMARY KEY,
    milestone_id INTEGER NOT NULL REFERENCES milestone (id),
    title        TEXT NOT NULL CHECK (trim(title) <> ''),
    priority     INTEGER,                                  -- NULL: 0
    description  TEXT NOT NULL CONSTRAINT "a plan needs a description" CHECK (trim(description) <> '')
) STRICT;

CREATE TABLE task (
    id           INTEGER PRIMARY KEY,
    plan_id      INTEGER NOT NULL REFERENCES plan (id),
    title        TEXT NOT NULL CHECK (trim(title) <> ''),
    status       TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'done', 'dropped')),
    priority     INTEGER,                                  -- NULL: the plan's
    note         TEXT,                                     -- done: date, files or commit; dropped: reason
    description  TEXT NOT NULL DEFAULT '',                 -- Markdown
    CONSTRAINT "an open task needs a description" CHECK (status <> 'open' OR trim(description) <> '')
) STRICT;

CREATE TABLE decision (
    id       INTEGER PRIMARY KEY,
    question TEXT NOT NULL CHECK (trim(question) <> ''),
    status   TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'answered', 'irrelevant')),
    options  TEXT NOT NULL DEFAULT '[]' CHECK (json_type(options) = 'array'),  -- recommended first
    context  TEXT NOT NULL DEFAULT '',
    answer   TEXT,
    reason   TEXT,
    closed   TEXT,
    CONSTRAINT "pending: no answer, reason or closed; answered: answer and closed; irrelevant: reason and closed"
    CHECK (status = 'pending' AND answer IS NULL AND reason IS NULL AND closed IS NULL
           OR status = 'answered' AND answer IS NOT NULL AND closed IS NOT NULL
           OR status = 'irrelevant' AND reason IS NOT NULL AND closed IS NOT NULL)
) STRICT;

CREATE TABLE task_decision (                               -- the task waits while the decision is pending
    task_id     INTEGER NOT NULL REFERENCES task (id),
    decision_id INTEGER NOT NULL REFERENCES decision (id),
    PRIMARY KEY (task_id, decision_id)
) STRICT;

CREATE INDEX plan_milestone ON plan (milestone_id);

CREATE INDEX task_plan ON task (plan_id);

CREATE INDEX task_decision_decision ON task_decision (decision_id);

CREATE VIEW queue AS
SELECT coalesce(t.priority, p.priority, 0) AS priority, t.id AS task_id, t.title
FROM task t
JOIN plan p ON p.id = t.plan_id
JOIN milestone m ON m.id = p.milestone_id
WHERE m.status = 'open' AND t.status = 'open'
  AND NOT EXISTS (SELECT 1 FROM task_decision td JOIN decision d ON d.id = td.decision_id
                  WHERE td.task_id = t.id AND d.status = 'pending')
ORDER BY priority DESC, m.id, p.id, t.id;
