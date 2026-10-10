# Backlog — Additional Tasks

Tasks that came up during planning but aren't yet assigned to a plan file. Move an item into the right plan file (with a task ID) once it's accepted.

The family game is living-room ready without any of these (2026-10-07); they are improvements, not blockers.

| # | Item | Origin | Status |
|---|------|--------|--------|
| B-1 | Session log: which questions were asked, the result, and the date. Would calibrate difficulty from real games (07) and could colour the tower blocks by category (04). With the TS engine (M7) it belongs in the save document (`SaveData`, 12). | planning | new |
| B-2 | Backup of the game save (`state/game.sqlite`, later `state/game.json` after PORT-5). The pool is already in git. | planning | new |
| B-3 | "Practice/preview" mode for the gamemaster to check questions and images on the TV; includes the overlay's «Demo de efectos» (04) | planning | new |
| B-4 | First-120: replace decorative images with images that show something related to the question, where that doesn't give the answer away | first-120 review | moved to IMG-14 |
| B-5 | `dedupe` misses duplicates with different wording: q-0369 repeats q-0341 (Rubik → Hungría), q-0420 overlaps q-0328 (silleteros). Both were caught only by the review. Compare answers and topics, not just question text. | batch-4 review | new |
| B-6 | Top-up for difficulties 9–10: 24 approved (only 2 at 10), while level 12 draws only from 9–10 and level 11 from 8–10. The drafter writes high targets too easy (batch-3: target 10 → mostly 7–9). Needs a way to aim `qgen batch` at difficulties instead of subcategories (D-36 fixes the subcategory choice). | pool stats, 2026-10-07 | new |
| B-7 | Picture effects for essential images: blur or pixelate that sharpens over time, a silhouette from a photo, a zoom that starts close and widens. Would bring back a "blurred" stimulus (dropped from the axes in PE-7) and make `detail`/`silhouette` independent of what Commons has. | plan 20, PE-7 | new |
| B-8 | Review tool: key `n` moves a question to another bundle but keeps its subcategory, so moving a `colombia` question to `base` can break D-49 (`validate` then fails). Moving to `base` should ask for a `base` subcategory, or the tool should let the gamemaster change the subcategory. | D-49 | new |
