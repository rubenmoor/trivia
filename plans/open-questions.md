# Open Questions

Answer each question here, then record the resulting decision in `decisions.md` and mark the question as resolved.

## Open

### Added 2026-10-06
- **OQ-17** Target total pool size? It decides how many questions to generate and how strict the quality filter is (see `07-question-generation.md`). *Input from D-22: every level offers 4 questions from its difficulty range, so a game needs 48 unburned questions to show and burns 12 (`03-game-flow.md`). Unlimited jokers burn extra questions (D-27), but burning is per player (D-28).*

### Added 2026-10-08 (media providers, D-45, [`23`](23-media-providers.md))
- **OQ-45** Freesound's API is free for non-commercial use, and commercial apps need a licence from UPF. Our pipeline uses the API only to find sounds; the game ships the CC0/CC BY files, never the API. Before a paid Steam release: ask Freesound whether that counts as commercial use of the API, or replace the Freesound picks.

### Added 2026-10-07 (Steam release, [`11-steam.md`](11-steam.md))
- **OQ-29** Desktop shell: Electron + steamworks.js (recommended), Tauri, or a browser + local server? See `18-steam-integration.md`.
- **OQ-30** Default mode: joker counts per difficulty preset (draft table in `13-game-modes.md`), checkpoints, which admin actions remain?
- **OQ-31** Launch languages (Spanish only? plus English? more?) and the Spanish variety: Colombian as today, or neutral Spanish with Colombian variants?
- **OQ-32** Content target for release: how many games per new player, per language (draft: ≥ 30, primary language ≥ 50; `16-content-target.md`)?
- **OQ-33** Price model (paid, free, free + paid packs), and who holds the Steamworks account (a person or a company; tax)?
- **OQ-35** Code and content license (the repo has no `LICENSE` today); does new release content stay public on GitHub?
- **OQ-37** Competitive mode and couch co-op: format (relay ladder, parallel ladders, buzzer), and input (hot-seat, one controller per player, phones as buzzers)?

## Resolved
- **OQ-34** Store name: «Living Room Trivia», in Spanish «Trivia en Familia» (Steam localized name), pending the name and trademark check PUB-7 (D-50).
- **OQ-45** LLM-approved questions no human has seen are an option to review, not a to-do; `needs_work` and the other open queues come first (D-42).
- **OQ-44** No per-bundle house style: a session mixes questions from every active bundle, so they all follow one house style (D-44).
- **OQ-41** A non-base bundle's categories are in `app/data/bundles/<id>/` (they ship), and its concepts and axes in `authoring/data/bundles/<id>/`. Subcategory names and category slugs are unique across bundles; question ids are global. **OQ-42** The Colombian subcategories leave `base` for `colombia`'s own list, and their questions keep their bundle. **OQ-43** Prompt only; the gamemaster moves the rest in the review tool (D-43).
- **OQ-36** Four age groups, adults included: kids, young teens, young adults, adults, on one shared difficulty scale 1–15 (D-38).
- **OQ-38** About 150–250 concepts per subcategory, with top-ups; **OQ-39** the axis values as drafted in plan 20, and existing questions get axes too; **OQ-40** concept names unique across subcategories by normalized name only, synonyms accepted (D-37).
- **OQ-4** No timer per question; **OQ-13** no separate gamemaster device and no GM-only view; **OQ-8** no family-specific questions; **OQ-11** a computer connected to the TV via HDMI; **OQ-12** internet is available during play; **OQ-28** the game is called «¡Trivia!» (D-30).
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
