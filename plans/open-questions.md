# Open Questions

Frozen on 2026-10-12: this file is history. New questions for the developer are `pm` decisions (`pm decision add`, see `pm instructions`); answers that set a lasting rule still go to `decisions.md`. Old OQ ids stay valid where they are cited. The questions below were still open when the file was frozen; the `pm` plan or task named with each one raises it as a `pm` decision.

## Open when frozen
None.

## Resolved
- **OQ-45** (Freesound) Freesound's API needs a UPF licence for commercial use: no asking; Freesound leaves the audio order; its 2 picks dropped, no Commons replacement (D-103, pm decision 184).
- **OQ-35** Code MIT; questions all rights reserved (personal, non-commercial play allowed); the whole repo stays public, release content included (D-102).
- **OQ-46** Yes: every bundle has its own categories and subcategories (names may repeat across bundles); the 19 `colombia` questions on `base` subcategories move to `colombia`'s own (D-99, pm decision 110, plan 98).
- **OQ-33** Paid one-time purchase, $9.99 (final check PUB-11), regional pricing, launch discount; packs as free DLC, never paid; the developer holds the Steamworks account as a person after an advisor check, company later via app transfer (D-98).
- **OQ-31** Launch languages es, en, de (zh-Hans, ru, pt-BR later, milestone 12); `base` in neutral Latin American Spanish (es-419) plus an es-ES variant where wording differs; `colombia` keeps its Colombian voice; store: Spanish – Latin America, Spanish – Spain, English, German (D-78). Amended by D-107: `base` drafted in English from batch-9, `es` idiomatic Latin American by translation, `es-ES` its own question pool.
- **OQ-37** Multiplayer: round-robin co-op, round-robin competitive, competitive (timed); one gamepad per player, keyboard, mouse, shared keyboard; no phones (D-77; timed revised D-80).
- **OQ-32** Content target: 5000 approved per launch language (es, en, de) with D-53's mix; no games-per-player number, CT-2 reports it for information (D-75).
- **OQ-30** No default mode: five game modes; no presets, no checkpoint, no skip outside gamemaster mode; «Reportar pregunta» only logs (D-74).
- **OQ-29** Desktop shell: Electron; Steam binding (steamworks-ffi-node or steamworks.js) picked in SW-2 (D-63).
- **OQ-17** Target pool size: 5000 approved `base` questions, tapering at high difficulties (D-52).
- **OQ-34** Store name: «Living Room Trivia», in Spanish «Trivia en Familia», in German «Wohnzimmer-Quiz» (Steam localized names); final, PUB-7 passed 2026-10-15 (D-50, pm decisions 78, 176).
- **OQ-45** LLM-approved questions no human has seen are an option to review, not a to-do; `needs_work` and the other open queues come first (D-42).
- **OQ-44** No per-bundle house style: a session mixes questions from every active bundle, so they all follow one house style (D-44).
- **OQ-41** A non-base bundle's categories are in `app/data/bundles/<id>/` (they ship), and its concepts and axes in `authoring/data/bundles/<id>/`. Subcategory names and category slugs are unique across bundles; question ids are global. **OQ-42** The Colombian subcategories leave `base` for `colombia`'s own list, and their questions keep their bundle. **OQ-43** Prompt only; the developer moves the rest in the review tool (D-43).
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
- **OQ-10** Authoring → AI drafts, developer reviews (D-7).
- **OQ-14** Tech stack preference → server Python (D-4), client Svelte 5 + Vite + TypeScript (D-5).
