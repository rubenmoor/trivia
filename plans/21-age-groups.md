# 21 — Four Age Groups on One Difficulty Scale

**Status:** active

The project was built for one audience: two Colombian kids aged 11 and 12 (D-6). The house style, the prompts and the difficulty scale all say so. From now on the game has **four age groups**, and the current focus is one of them, young teens. Nothing in the authoring pipeline names a fixed audience any more; it names the focus group, which is set in one file (D-38).

## Age groups
In `app/data/age-groups.json` (it ships: the game will offer the choice, AG-7):

| id | Name | Ages | Window on the scale (draft) |
|---|---|---|---|
| `kids` | Niños | 6–10 | 1–7 |
| `young_teens` | Adolescentes | 11–14 | 1–10 (the game's levels today, D-22) |
| `young_adults` | Jóvenes | 15–22 | 3–13 |
| `adults` | Adultos | 23+ | 4–15 |

`"focus": "young_teens"` in the same file is the group the pipeline writes for and the game plays today. The windows of the other groups are a first draft; they are tuned when the game uses them (AG-7).

## One shared scale, 1–15
Difficulty stays "who can answer it", one number per question, on one scale for every group. Each group plays a window of it. The old scale 1–10 keeps its meaning, so the existing pool needs no migration; 11–15 extend it past school:

- 1 = a 6-year-old can answer it
- 3 = a 9-year-old
- 5 = an 11-year-old
- 7 = a 13-year-old
- 10 = a 16-year-old with good school knowledge
- 12 = most adults; a first-year university student
- 14 = a well-read adult, or a graduate in the field
- 15 = trivia specialists

Why one scale and not a difficulty per group: one number per question is simple to rate, review and select by, and the windows overlap, so most questions serve several groups. The cost: the scale assumes everyone learns in roughly the same order, which isn't quite true (teens know games and cartoons that adults don't). The house style's calibration says how to place such questions: by who can answer them, at their easiest.

## Concepts: `known_at` instead of `familiarity`
`familiarity` (1–5) said how well kids aged 11–12 know a concept, which ties every list to one group. It is replaced by **`known_at`** (1–15): the lowest point on the shared scale at which people know the concept (Sol 1, Saturno 2, Betelgeuse 12). `draft` prefers concepts whose `known_at` is close to the slot's target difficulty (`1 / (1 + |known_at − target| / 2)`). Lists serve every group; the focus only decides which targets are drawn.

## In the pipeline
- **House style:** "Players: two Colombian kids" becomes "Audience": four age groups, the focus group, and content that stays family-friendly in every group. The difficulty section describes the shared scale. The calibration examples stay: they were observed with young teens and are already on the shared scale.
- **Targets:** `draft` draws target difficulties from the focus group's window; `LEVEL_WEIGHTS` are the young-teen weights (D-31) and must cover exactly that window.
- **Checks:** difficulty may be 1–15 (`check_question_shape`, `validate`).
- **Prompts:** no prompt names kids or a fixed age; they say "players of the focus group" where the audience matters. `age_fit` (rate) keeps its name and means: fits its difficulty and suits the focus group.
- **Not changed now:** the game (it plays young teens, levels 1–10 as today), selection, and the pool's difficulties.

## Tasks
- [x] AG-1 Decision D-38 and this plan; OQ-36 answered (four age groups, adults included)
- [x] AG-2 `app/data/age-groups.json`: four groups, ages, windows, `focus`. *Also `scale`; path in `app/server/paths.py`.*
- [x] AG-3 House style: audience and the shared scale 1–15 instead of "two kids aged 11 and 12". *`{age_groups}` and `{focus_group}` are filled from the age-groups file by `prompt()`; calibration kept, labelled as observed with young teens.*
- [x] AG-4 Prompts (draft, rate, revise, concepts) without a fixed age; `known_at` replaces `familiarity`
- [x] AG-5 `qgen`: difficulty 1–15; targets from the focus window; `known_at` in drawing, lists and validation. *`draft` stops if `LEVEL_WEIGHTS` don't cover the focus window; a concept added for an existing question takes the question's difficulty as `known_at`.*
- [x] AG-6 Espacio's concept list again, with `known_at`. *255 concepts (225 + a 30-concept fill), `known_at` 1–14; 146 in the young-teen window, 86 in the kids', 232 in each adult window.*
- [ ] AG-7 The game: choose an age group; levels map to the group's window; tune the draft windows and per-group level weights
- [ ] AG-8 Batches for other age groups: `LEVEL_WEIGHTS` per group, and how a batch picks its group
- [ ] AG-9 Review tool: set difficulties 11–15 (the server accepts 1–15; the digit keys only reach 1–10)
