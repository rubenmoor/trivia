# Open Questions

Answer each question here, then record the resulting decision in `decisions.md` and mark the question as resolved.

## Open

### Game rules
- **OQ-4** Jokers or lifelines? A timer per question?

### Content
- **OQ-8** Which categories? Are family-specific questions (e.g. "Where did we go on holiday in 2015?") wanted? *The first draft proposes 10 categories in `data/questions.json`.* **Answered 2026-10-06:** 24 broad categories with 140 subcategories in `data/categories.json` (D-19). Family-specific questions: still open.

### Added 2026-10-06
- **OQ-15** How are hints used in play? Free, limited per game, or do they cost something?
- **OQ-17** Target total pool size? It decides how many questions to generate and how strict the quality filter is (see `07-question-generation.md`).

### UI & sound (added 2026-10-06, `04-ui-tv-display.md`)
- **OQ-20** Are music and sound effects committed to the repo (small, CC0/CC BY, with `CREDITS.md`), unlike question media (D-17)? *Proposal: yes.*
- **OQ-21** Can the players change a locked-in answer before they press «Respuesta final»? *Proposal: yes; tapping another answer re-locks.*
- **OQ-22** After a wrong answer, is the correct answer (and `fun_fact`) shown before the consolation message? *Proposal: yes.*
- **OQ-23** Level → difficulty mapping: is `round(1 + (level − 1) × 9 / 11)` right, or should the curve be gentler early on? (`03-game-flow.md`)
- **OQ-24** Stack theme: tower of blocks, layer cake, pyramid, or something else? (UI-1)

### Tech & setup
- **OQ-11** Which device drives the TV (laptop via HDMI, smart-TV browser, Raspberry Pi, Chromecast)?
- **OQ-12** Is internet available during play? (Affects the image strategy.)
- **OQ-13** Does the gamemaster want a separate device that shows the answers?

## Resolved
- **OQ-1** 12 in a row; **OQ-2** a wrong answer ends the game; **OQ-3** difficulty rises from level 1 (easiest) to 12 (D-20).
- **OQ-16** Media sources → Wikimedia Commons only; no songs or film clips (D-13).
- **OQ-18** Feedback is its own decision: salvageable but needs changes → `needs_work` (D-11).
- **OQ-19** Reject asks for no reason: it means unsalvageable (D-11).
- **OQ-5** Formats → multiple choice only: 1 correct + 3 wrong, 3 hints, one media item (D-7).
- **OQ-6** Language → Spanish, Colombian usage (D-6).
- **OQ-7** Players → two Colombian kids, 11 and 12; difficulty 1–10 = age 6 to 16 (D-6).
- **OQ-9** Pool size → ~120 questions, 10 games (D-6).
- **OQ-10** Authoring → AI drafts, gamemaster reviews (D-7).
- **OQ-14** Tech stack preference → server Python (D-4), client Svelte 5 + Vite + TypeScript (D-5).
