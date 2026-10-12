# Backlog — Additional Tasks

Tasks that came up during planning but aren't yet assigned to a plan file. Move an item into the right plan file (with a task ID) once it's accepted.

The family game is living-room ready without any of these (2026-10-07); they are improvements, not blockers.

| # | Item | Origin | Status |
|---|------|--------|--------|
| B-1 | Session log: which questions were asked, the result, and the date. Would calibrate difficulty from real games (07) and could colour the tower blocks by category (04). With the TS engine (M7) it belongs in the save document (`SaveData`, 12). | planning | new |
| B-2 | Backup of the game save (`state/game.sqlite`, later `state/game.json` after PORT-5). The pool is already in git. | planning | new |
| B-3 | "Practice/preview" mode for the gamemaster to check questions and images on the TV; includes the overlay's «Demo de efectos» (04) | planning | new |
| B-4 | First-120: replace decorative images with images that show something related to the question, where that doesn't give the answer away | first-120 review | moved to IMG-14 |
| B-5 | `dedupe` misses duplicates with different wording: q-0369 repeats q-0341 (Rubik → Hungría), q-0420 overlaps q-0328 (silleteros). Both were caught only by the review. Compare answers and topics, not just question text. | batch-4 review | moved to pm plan 15 |
| B-6 | Top-up for difficulties 9–10: 24 approved (only 2 at 10), while level 12 draws only from 9–10 and level 11 from 8–10. The drafter writes high targets too easy (batch-3: target 10 → mostly 7–9). Needs a way to aim `qgen batch` at difficulties instead of subcategories (D-36 fixes the subcategory choice). | pool stats, 2026-10-07 | moved to pm plan 13 |
| B-7 | Picture effects for essential images: blur or pixelate that sharpens over time, a silhouette from a photo, a zoom that starts close and widens. Would bring back a "blurred" stimulus (dropped from the axes in PE-7) and make `detail`/`silhouette` independent of what Commons has. | plan 20, PE-7 | new |
| B-8 | Review tool: key `n` moves a question to another bundle but keeps its subcategory, so moving a `colombia` question to `base` can break D-49 (`validate` then fails). Moving to `base` should ask for a `base` subcategory, or the tool should let the gamemaster change the subcategory. | D-49 | new |
| B-9 | `providers.US_ONLY_PD` matches `PD-USGS` (a US government agency template) as US-only; harmless today (its one file has another reason), but a file with only `PD-USGS` would be listed for replacement. Exclude it like `PD-USGov*` (D-62). | task 307 | new |
| B-10 | `qgen batch-report` on a batch without `work/<b>/recorded.json` (batch-7 and older) rewrites the "Needs work" list from the current pool, and `llm_decisions` reads record's decisions from that list: the audit's numbers shift (batch-7: 49 → 57 LLM-approved in the sample). Write `recorded.json` for old batches once from their committed reports, or never regenerate them. | task 48 | new |
| B-11 | Desktop build: `Trivia.exe` keeps Electron's icon and file metadata and is unsigned (`win.signAndEditExecutable: false`, no wine on Linux, D-73). In S5: icon + metadata (SW-6 CI on Windows or a Windows machine), signing if Steam needs it. | task 329 | new |
| B-12 | `qgen` reads `young_teens.level_weights` from `app/data/age-groups.json` instead of its `LEVEL_WEIGHTS` constant (identical today, D-76), once AG-8 starts. | task 127 | new |
| B-13 | Rewrite `base` into neutral Latin American Spanish (es-419): the ~40 Colombianisms ("bombillo", "crispetas", …) via the pipeline (D-36), house style and prompts say es-419 for `base`; `colombia` keeps its voice. S4 content work (D-78). Plan: pm plan 64 (tools, prompts); runs in plan 9 part 11. | task 381 | new |
