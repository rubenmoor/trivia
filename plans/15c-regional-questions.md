# 15c — Regional Questions

**Status:** stub

Sub-plan of [15](15-i18n.md). The pool was written for two Colombian kids (D-6), so some questions are about Colombia (Valle de Cocora, Colombian food, history, music) and are easy for them but hard or unfair elsewhere. Regions make those questions an opt-in pack instead of a problem, and they open the door to more regional packs later.

## Model
- `region` on every question: `null` = universal, or an ISO 3166 code (`"co"`). Maybe a list later, e.g. a question about the Andes for `co`, `pe`, `ec`.
- The player picks regions in the settings (15): "universal" is always on, and the default is the region of the UI language's main market (to decide: probably no regions by default outside Spanish).
- **Difficulty is rated for players of that region** (a Colombian kid for `co`). Outside the region the question isn't shown, so it never needs a second rating.
- **The family keeps everything:** the gamemaster mode defaults to "universal + Colombia", so nothing changes for them.
- **Packs:** a region is a set of questions with a name and a flag («Colombia»). It could later be a free DLC or update; Steam handles DLC as extra depots (18).
- **Supply per region:** `qgen.py report --region co` shows how many games a pack adds; a pack on its own doesn't need to fill a whole game, because it mixes into the universal pool.

## Tasks
- [ ] RG-1 Add `region` to the schema (`null` default) and `validate`.
- [ ] RG-2 Tag the existing pool: an LLM pass proposes `co` or `null` per question, and the gamemaster checks the proposals in the review tool (filter by proposed region). Can start now.
- [ ] RG-3 Region filter in the selection (engine, 12) and in `qgen.py report`.
- [ ] RG-4 `qgen.py draft --region co`: generate regional questions on purpose.
- [ ] RG-5 Decide which regional packs come next (by launch language, OQ-31).
