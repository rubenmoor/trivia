# Plans — Index

This directory holds the plan for the family trivia party game. These files are the source of truth for **what** gets built and **why**. Code follows the plans. When the code and a plan disagree, update the plan first.

## Project in one paragraph

A trivia/Q&A party game that runs locally and offline; the code and question pool are public, media files are a local cache (D-17). It is shown on a living-room TV. The family plays as one team against the gamemaster (the author). They have to answer **12 questions to win**. Every question has a background image related to its content. A reusable question pool lets the game be played several times, and a question is marked **burned** for a player once that player has seen it (D-28).

## File hierarchy

| File | Purpose | Status |
|------|---------|--------|
| [`00-vision.md`](00-vision.md) | Goals, constraints, non-goals, success criteria | implemented |
| [`01-architecture.md`](01-architecture.md) | Tech stack, components, data flow | implemented |
| [`02-question-pool.md`](02-question-pool.md) | Question schema, pool storage, burned tracking | stub |
| [`03-game-flow.md`](03-game-flow.md) | Rules, 12-question progression, win/lose states | draft |
| [`04-ui-tv-display.md`](04-ui-tv-display.md) | Screen states, transitions, sound, animation for the TV | draft |
| [`05-gamemaster-controls.md`](05-gamemaster-controls.md) | How the gamemaster drives the game | decided |
| [`06-images.md`](06-images.md) | Media sourcing (Wikimedia Commons), caching, credits, picking in the review tool | draft |
| [`07-question-generation.md`](07-question-generation.md) | Drafting, rating, reviewing and accepting new questions; batch generation strategy | draft |
| [`08-review-tool.md`](08-review-tool.md) | Local web page to approve, reject or give feedback on questions | draft |
| [`09-jokers.md`](09-jokers.md) | Jokers (hint, skip/purge, easier, other subcategory, snipe): rules, server, UI, animations | draft |
| [`10-visual-design.md`](10-visual-design.md) | Look and feel: colours, type scale, glass panels over images, components, motion | draft |
| [`11-steam.md`](11-steam.md) | **Steam release master plan:** principles, tracks, phases, blocking questions (D-34) | draft |
| [`12-client-engine.md`](12-client-engine.md) | Move the game referee from Python to TypeScript; storage adapters; pool export (M7) | draft |
| [`13-game-modes.md`](13-game-modes.md) | Steam: gamemaster mode with joker budget, default mode with presets, competitive mode | stub |
| [`14-input.md`](14-input.md) | Steam: every button clickable, controller support, couch co-op input | draft |
| [`15-i18n.md`](15-i18n.md) | Steam: locale and region model; sub-plans 15a (UI), 15b (questions), 15c (regional) | stub |
| [`15a-ui-translation.md`](15a-ui-translation.md) | Steam: UI string catalogs, joker names and keys per language | stub |
| [`15b-question-translation.md`](15b-question-translation.md) | Steam: translating, re-rating and reviewing the pool per language | stub |
| [`15c-regional-questions.md`](15c-regional-questions.md) | Steam: `region` tags (Colombia today), regional packs | stub |
| [`16-content-target.md`](16-content-target.md) | Steam: pool size and quality bar for release, games-per-player simulation | stub |
| [`17-publishing.md`](17-publishing.md) | Steam: media and code licenses, credits, AI disclosure, store page, Steamworks account | stub |
| [`18-steam-integration.md`](18-steam-integration.md) | Steam: desktop shell, Steamworks features, builds and depots, Steam Deck | stub |
| [`19-repo-layout.md`](19-repo-layout.md) | Repo layout (`app/` ships, `authoring/` doesn't), flake packages, the one-command LLM batch (D-35, D-36) | active |
| [`20-pipeline-efficiency.md`](20-pipeline-efficiency.md) | Fewer Claude calls and tokens in `qgen batch`; stored concept lists and multi-axis question styles for more varied questions | active |
| [`project.md`](project.md) | Milestones; all open tasks and questions grouped by milestone | living |
| [`backlog.md`](backlog.md) | Additional tasks found along the way | living |
| [`open-questions.md`](open-questions.md) | Unresolved questions and their answers | living |
| [`decisions.md`](decisions.md) | Decision log (lightweight ADRs) | living |

Order of work: **02 (question pool) first, together with 07 (question generation)**, then 03 → 01 → 06 → 04 → 10 → 09 → 05.

The family game is done and living-room ready (2026-10-07). Open work is grouped in [`project.md`](project.md): content (M5) and groundwork that doesn't change how the family plays (M7–M10, from plans 12, 13, 14, 15a, 15c, 17). The Steam release (11–18) is a separate track with its own phases (S2–S6) in [`11-steam.md`](11-steam.md).

## Conventions

### Task status markers

Every plan file ends with a `## Tasks` section that uses these markers:

- `[ ]` — todo
- `[~]` — in progress
- `[x]` — **implemented** (add a short note: date, and file or commit reference)
- `[-]` — dropped (give the reason)

Task IDs are `<file-prefix>-<n>`, for example `QP-3` for question-pool task 3. IDs are never reused, so other files can cite them.

### File status (header line in each file)

`stub` → `draft` → `agreed` → `implemented`

### Rules for LLM-assisted work

1. Read [`../AGENTS.md`](../AGENTS.md) and this index before starting any task.
2. Work one task ID at a time. Keep changes small and reviewable.
3. When a new requirement comes up, add it to [`backlog.md`](backlog.md). Don't silently widen the scope.
4. When something is ambiguous, log it in [`open-questions.md`](open-questions.md) and don't guess. Once it's answered, record the outcome in [`decisions.md`](decisions.md).
5. After you implement something, tick the task and update the file status.
