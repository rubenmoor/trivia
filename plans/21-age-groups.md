# 21 — Four Age Groups on One Difficulty Scale

**Status:** active

The project was built for one audience: two Colombian kids aged 11 and 12 (D-6). The house style, the prompts and the difficulty scale all say so. From now on the game has **four age groups**, and the current focus is one of them, young teens. Nothing in the authoring pipeline names a fixed audience any more; it names the focus group, which is set in one file (D-38).

## Age groups
In `app/data/age-groups.json` (it ships: the game offers the choice, AG-7):

| id | Name | Ages | Window on the scale |
|---|---|---|---|
| `kids` | Niños | 6–10 | 1–6 |
| `young_teens` | Adolescentes | 11–14 | 1–10 (D-22's levels) |
| `young_adults` | Jóvenes | 15–22 | 4–13 |
| `adults` | Adultos | 23+ | 5–15 |

`"focus": "young_teens"` in the same file is the group the pipeline writes for. `"focus": null` means no focus: the pipeline writes across the whole scale 1–15, with even targets, and each question is written for the groups whose window contains its difficulty (D-40). Windows, `levels` and `level_weights` tuned 2026-10-12 (AG-7, D-76).

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
- **Targets:** `draft` draws target difficulties from the focus group's window; `LEVEL_WEIGHTS` are the young-teen weights (D-31) and must cover exactly that window. Without a focus, every level of the scale gets the same weight (D-40).
- **Checks:** difficulty may be 1–15 (`check_question_shape`, `validate`).
- **Prompts:** no prompt names kids or a fixed age; they say "players of the focus group" where the audience matters. `age_fit` (rate) keeps its name and means: fits its difficulty and suits the focus group.
- **The game** (AG-7): players choose an age group before a session; selection uses its `levels` on the shared scale; the pool's difficulties unchanged.

## Tasks
- [x] AG-1 Decision D-38 and this plan; OQ-36 answered (four age groups, adults included)
- [x] AG-2 `app/data/age-groups.json`: four groups, ages, windows, `focus`. *Also `scale`; path in `app/server/paths.py`.*
- [x] AG-3 House style: audience and the shared scale 1–15 instead of "two kids aged 11 and 12". *`{age_groups}` and `{focus_group}` (now `{players}`, AG-10) are filled from the age-groups file by `prompt()`; calibration kept, labelled as observed with young teens.*
- [x] AG-4 Prompts (draft, rate, revise, concepts) without a fixed age; `known_at` replaces `familiarity`
- [x] AG-5 `qgen`: difficulty 1–15; targets from the focus window; `known_at` in drawing, lists and validation. *`draft` stops if `LEVEL_WEIGHTS` don't cover the focus window; a concept added for an existing question takes the question's difficulty as `known_at`.*
- [x] AG-6 Espacio's concept list again, with `known_at`. *255 concepts (225 + a 30-concept fill), `known_at` 1–14; 146 in the young-teen window, 86 in the kids', 232 in each adult window.*
- [x] AG-7 The game: choose an age group; levels map to the group's window; tune the windows and per-group level weights. *2026-10-15: engine plan 27 (`gameChoice`, `resolveChoice`; `levels` in `age-groups.json`), tuning plan 28 (D-76), Choice screen plan 29, play-test fixes plan 125; play-tested (pm decisions 50, 155, 206).*
- [ ] AG-8 Batches for other age groups: `LEVEL_WEIGHTS` per group, and how a batch picks its group
- [x] AG-10 No focus (D-40): `"focus": null` writes across the whole scale with even targets; house style, rate prompt and bundle rules say "the players" instead of "the focus group". *`target_weights()` in `qgen.py`; the house style's `{focus_group}` became `{players}`, which names the focus group or, without one, every group's window. `focus` is set to null for now.*
- [x] AG-9 Review tool: set difficulties 11–15 (the server accepts 1–15; the digit keys only reach 1–10). *`d`, then type the number and press Enter; Backspace corrects, Esc cancels. The header shows the difficulty without "/10".*

## Long-term difficulty distribution (proposal, for AG-7/AG-8)
Even targets are a stopgap: they catch up on 11–15, which the pool doesn't have yet. In the long run the pool should match what games use. A difficulty is played by every group whose window contains it, so the middle of the scale is needed most. With equal play per group and a flat spread within each window, the demand per level is the sum of 1 / window width over the groups that play it:

| Levels | Played by | Share per level |
|---|---|---|
| 1–3 | kids, young teens | 7 % |
| 4 | + young adults | 9 % |
| 5–6 | all four | 11 % |
| 7–10 | young teens, young adults, adults | 7 % |
| 11–13 | young adults, adults | 5 % |
| 14–15 | adults | 2 % |

Recomputed 2026-10-12 for the approved windows (D-76); with per-group weights: "Demand vs. pool" under "Measured windows".

The proposal: derive the targets from `age-groups.json` (windows, per-group level weights from AG-7, a play share per group), with a floor per level so every group can play several games without repeats, and draw each batch's targets by **deficit** (target share minus the pool's share) so batches fill gaps instead of repeating a fixed shape.

## Measured windows (AG-7)
Measured 2026-10-11 with a throw-away script on the engine (`supply`, `draw`, `seededRng`; plan 28), pool of 1136 approved questions (`base` 1034, `colombia` 102). Draft = `levels` from plan 27; proposal = tuned `kids`, `young_adults`, `adults`; `young_teens` stays D-22. Raised as the decision "Approve the age-group windows"; the developer approved the proposal, applied 2026-10-12 (D-76).

- Thinnest: level with the fewest candidates (`supply`). Until dry: games one player can play, burning every card shown, until a level can't be filled; median of 20 seeds, and the level that ran dry most often.
- Ranges: level 1 first; `×n` = the same range n levels in a row.

### `{base}`
| Group | | Window | Ranges | Thinnest | Until dry |
|---|---|---|---|---|---|
| `kids` | draft | 1–7 | 1, 2, 2–4, 3–4 ×3, 4–5, 4–6 ×2, 5–7, 6–7 ×2 | L1 (1): 36 | 9, L1 |
| | proposal | 1–6 | 1, 2, 2–3, 2–4, 3–4 ×2, 3–5, 4–5 ×2, 4–6, 5–6 ×2 | L1 (1): 36 | 9, L1 |
| `young_teens` | D-22 | 1–10 | 1, 2–3, 3–5, 4–6 ×3, 5–7, 6–8, 6–9, 7–10, 8–10, 9–10 | L1 (1): 36 | 9, L1 |
| `young_adults` | draft | 3–13 | 3, 4–5, 5–7, 6–9 ×3, 7–10, 9–11, 9–12, 10–13, 11–13, 12–13 | L12 (12–13): 86 | 10, L12 |
| | proposal | 4–13 | 4, 5–6, 6–8, 7–9 ×3, 8–10, 9–11, 9–12, 10–13, 11–13 ×2 | L1 (4): 103 | 10, L12 |
| `adults` | draft | 4–15 | 4, 5–6, 6–9, 8–10 ×3, 9–11, 10–13, 10–14, 11–15, 13–15, 14–15 | L12 (14–15): 27 | 4.5, L12 |
| | proposal | 5–15 | 5, 6–7, 7–9, 8–10 ×2, 8–11, 9–11, 10–12, 10–13, 11–14, 12–15, 13–15 | L12 (13–15): 75 | 8, L12 |

### `{base, colombia}`
| Group | | Thinnest | Until dry |
|---|---|---|---|
| `kids` | draft | L1 (1): 36 | 9, L1 |
| | proposal | L1 (1): 36 | 9, L1 |
| `young_teens` | D-22 | L1 (1): 36 | 9, L1 |
| `young_adults` | draft | L12 (12–13): 90 | 11, L12 |
| | proposal | L1 (4): 117 | 11, L12 |
| `adults` | draft | L12 (14–15): 27 | 5, L12 |
| | proposal | L12 (13–15): 77 | 9, L12 |

- Every level of every group has ≥ 36 candidates (target ≥ 20); no missing slots.
- Level 1 = difficulty 1 (36 approved) limits `kids` and `young_teens` to 9 games; kept, D-22 fixes it for young teens.
- `colombia` adds 102 questions, almost all at 2–9; it barely moves the top.

### Proposal vs. the anchors
- `kids` (6–10): oldest ≈ 4. Draft top 6–7 = a 12–13-year-old, too hard; proposal top 5–6 = one step above the oldest, as a final challenge.
- `young_adults` (15–22): youngest ≈ 9, oldest ≈ 12–13. Warm-up 3 → 4; top 11–13 ×2 reaches 13; the wider top lets it share 11–13 between levels 10–12.
- `adults` (23+): 12 = most adults, top reaches 15. Warm-up 4 → 5; top widened downward (14–15 → 13–15, 13–15 → 12–15) instead of shrinking the window.
- Overlap kept: 5–6 serve all four groups, 4–10 three, 11–13 two, 14–15 adults only.

### Level weights
`n = round(12 × Σ 1/(hi − lo + 1))` over the levels containing the difficulty (plan 28); `young_teens` equals `qgen.LEVEL_WEIGHTS` (sum 144, asserted). Rounding can make another group's sum differ slightly.

| Group | | Weights (difficulty: n) |
|---|---|---|
| `kids` | draft | 1:12 2:16 3:22 4:36 5:18 6:24 7:16 |
| | proposal | 1:12 2:22 3:26 4:36 5:32 6:16 |
| `young_teens` | D-22 | 1:12 2:6 3:10 4:16 5:20 6:23 7:14 8:14 9:16 10:13 |
| `young_adults` | draft | 3:12 4:6 5:10 6:13 7:16 8:12 9:19 10:13 11:14 12:16 13:13 |
| | proposal | 4:12 5:6 6:10 7:16 8:20 9:23 10:14 11:18 12:14 13:11 |
| `adults` | draft | 4:12 5:6 6:9 7:3 8:15 9:19 10:21 11:12 12:8 13:12 14:15 15:12 |
| | proposal | 5:12 6:6 7:10 8:15 9:19 10:22 11:17 12:13 13:13 14:10 15:7 |

### Thin top (milestone 1, not fixed here)
- 14: 19 approved, 15: 8 (`colombia`: none). Adults' top two levels share 12–15 (113) and 13–15 (75); they run dry first (8 games).
- `young_adults`' top 11–13 (147) runs dry after 10 games.
- 10 (57) and 15 are below their demand share; 3 and 6 above.

### Demand vs. pool, proposed windows
Equal play per group. Flat: plan 21's method (1 / window width per group). Weights: from the proposed `level_weights`. Pool: `base` share.

| Difficulty | Played by | Flat | Weights | Pool |
|---|---|---|---|---|
| 1–3 | kids, young teens | 7 % each | 4 / 5 / 6 % | 3.5 / 6.5 / 9.3 % |
| 4 | + young adults | 9 % | 11 % | 10.0 % |
| 5–6 | all four | 11 % each | 12 / 10 % | 10.8 / 14.2 % |
| 7–10 | young teens, young adults, adults | 7 % each | 7 / 9 / 10 / 9 % | 9.8 / 6.5 / 7.2 / 5.5 % |
| 11–13 | young adults, adults | 5 % each | 6 / 5 / 4 % | 5.9 / 3.7 / 4.6 % |
| 14–15 | adults | 2 % each | 2 / 1 % | 1.8 / 0.8 % |

- Against the draft table above: 3 is played by two groups instead of three, 4 and 7 by three instead of four; 5–6 rise to 11 %.

## Played vs. rated (plan 109)
Opt-in telemetry measures how the scale plays. `qgen report --played` (decision 122) compares it with the ratings per age group; it never changes a question or a window on its own.

- Per group a curve: right rate per rated difficulty, clean answers only (no Soplo, no Francotirador), made monotone.
- Per question and group: the difficulty where the curve meets its played right rate; |Δ| ≥ 2 with enough answers → review candidate in `/review?played=outliers`.
- Relative: finds questions mis-rated against their peers, not a group that is too hard as a whole.
- Per age group × level table: answers, right rate, mean rated difficulty, games ending there; input for window and level changes, which go through their own plan.
