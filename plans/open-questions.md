# Open Questions

Answer each question here, then record the resulting decision in `decisions.md` and mark the question as resolved.

## Open

### Game rules
- **OQ-4** ~~Jokers or lifelines?~~ Five jokers (D-26). A timer per question?

### Content
- **OQ-8** Which categories? Are family-specific questions (e.g. "Where did we go on holiday in 2015?") wanted? *The first draft proposes 10 categories in `data/questions.json`.* **Answered 2026-10-06:** 24 broad categories with 140 subcategories in `data/categories.json` (D-19). Family-specific questions: still open.

### Added 2026-10-06
- **OQ-17** Target total pool size? It decides how many questions to generate and how strict the quality filter is (see `07-question-generation.md`). *Input from D-22: every level offers 4 questions from its difficulty range, so a game needs 48 unburned questions to show and burns 12 (`03-game-flow.md`). Unlimited jokers burn extra questions (D-27), but burning is per player (D-28).*

### Tech & setup
- **OQ-11** Which device drives the TV (laptop via HDMI, smart-TV browser, Raspberry Pi, Chromecast)?
- **OQ-12** Is internet available during play? (Affects the image strategy.)
- **OQ-13** Does the gamemaster want a separate device that shows the answers?

## Resolved
- **OQ-28** What is the game called? The Start screen needs a wordmark (`10-visual-design.md`). *Suggestions, playing on the tower: «¡La Torre!», «Torre de Preguntas», «Doce Pisos».*
- **OQ-15** Hints are shown only through the Pista joker, one hint per use, until the question's three are shown (D-26, D-27). **OQ-25** Jokers are unlimited; **OQ-26** one hint per Pista; **OQ-27** a Snipe hit costs nothing beyond repeating the level (D-27).
- **OQ-20** UI audio (music and effects) is committed; **OQ-21** players can unlock a locked answer, and then nothing is locked; **OQ-22** the correct answer is shown after a wrong one; **OQ-23** level → difficulty ranges; **OQ-24** tower of blocks, narrower towards the top (D-22).
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
