# Open Questions

Answer each question here, then record the resulting decision in `decisions.md` and mark the question as resolved.

## Open

### Game rules
- **OQ-1** Must the family answer 12 in a row, or reach 12 correct answers before some limit (lives or wrong answers)?
- **OQ-2** What happens on a wrong answer: game over, lose a life, or a point for the gamemaster?
- **OQ-3** Does difficulty increase along the 12 steps (Millionaire-style ladder)?
- **OQ-4** Jokers or lifelines? A timer per question?

### Content
- **OQ-8** Which categories? Are family-specific questions (e.g. "Where did we go on holiday in 2015?") wanted? *The first draft proposes 10 categories in `data/questions.json`.* **Answered 2026-10-06:** 24 broad categories with 140 subcategories in `data/categories.json` (D-19). Family-specific questions: still open.

### Added 2026-10-06
- **OQ-15** How are hints used in play? Free, limited per game, or do they cost something?
- **OQ-17** Target total pool size? It decides how many questions to generate and how strict the quality filter is (see `07-question-generation.md`).

### Tech & setup
- **OQ-11** Which device drives the TV (laptop via HDMI, smart-TV browser, Raspberry Pi, Chromecast)?
- **OQ-12** Is internet available during play? (Affects the image strategy.)
- **OQ-13** Does the gamemaster want a separate device that shows the answers?

## Resolved
- **OQ-16** Media sources → Wikimedia Commons only; no songs or film clips (D-13).
- **OQ-18** Feedback is its own decision: salvageable but needs changes → `needs_work` (D-11).
- **OQ-19** Reject asks for no reason: it means unsalvageable (D-11).
- **OQ-5** Formats → multiple choice only: 1 correct + 3 wrong, 3 hints, one media item (D-7).
- **OQ-6** Language → Spanish, Colombian usage (D-6).
- **OQ-7** Players → two Colombian kids, 11 and 12; difficulty 1–10 = age 6 to 16 (D-6).
- **OQ-9** Pool size → ~120 questions, 10 games (D-6).
- **OQ-10** Authoring → AI drafts, gamemaster reviews (D-7).
- **OQ-14** Tech stack preference → server Python (D-4), client Svelte 5 + Vite + TypeScript (D-5).
