# batch-91

Made by `qgen batch --media-first` on 2026-11-18 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 1 (q-21209…q-21209)
- Approved: 1
- Needs work: 0
- Dropped by the pipeline: 1
- Reviewed by: claude-opus-5-5
- Claude calls: 63, about $4.81 at list price; $4.81 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-89, batch-90; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-89 | batch-90 | batch-91 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 1 | 1 | 2 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 0 | 0 | 1 |
| drop rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 50.0 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 0 | 0 | 0 |
| dropped: overlap |  | 0 | 0 | 1 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 1 | 1 | 1 |
| approved |  | 1 | 1 | 1 |
| needs_work |  | 0 | 0 | 0 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| media: no pick in review 1 |  | no | no | no |
| media: recovered by research |  | no | no | no |
| media: no pick at record |  | yes | yes | yes |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | n/a | n/a | n/a |
| overlap rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 50.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 1 | 1 | 1 |
| top move | ≤ 25.0 % | n/a | n/a | n/a |
| values move |  | n/a | n/a | n/a |
| top stimulus |  | n/a | n/a | n/a |
| values stimulus |  | n/a | n/a | n/a |
| top clue | ≤ 60.0 % | n/a | n/a | n/a |
| values clue |  | n/a | n/a | n/a |
| top answer_kind | ≤ 40.0 % | n/a | n/a | n/a |
| values answer_kind |  | n/a | n/a | n/a |
| top lens | ≤ 25.0 % | n/a | n/a | n/a |
| values lens |  | n/a | n/a | n/a |
| giveaway-step drop rate |  | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| mechanical-check rate |  | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 4.00 ✓ | 3.00 ✗ | 3.50 ✓ |
| cost $ |  | $7.54 | $5.56 | $4.74 |
| $ per approved | ≤ $0.35 | $7.54 ✗ | $5.56 ✗ | $4.74 ✗ |
| calls |  | 98 | 74 | 62 |
| calls per approved |  | 98.00 | 74.00 | 62.00 |
| wall time h |  | 0.45 | 0.24 | 0.24 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 1 (100 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 1 (1 major), media 1 (1 major)
- Mean |audit − final difficulty|: 2.0; ≥ 3 on 0 of 1 (0 %)
- Audit/review agreement (both accept or both not): 0 of 1 (0 %)
- Sample: 1 audited of 1; 1 Claude calls, about $0.07

Major findings on approved questions:

- **q-21209**: giveaway, media — The text answers the question without the clip. "Lander" rules out the rovers Curiosity and Perseverance. "Two round solar panels" rules out Viking 1, which ran on nuclear power (RTGs). The description's "dig a little hole" points to InSight's mole. Also, the 25–55 s window of this HP3 overview animation gives only texture-like OCR noise, which suggests close-ups of the mole hammering into the soil rather than a clear shot of the lander, its round panels and the white dome. I couldn't open the frame sheet to confirm that, so the clip may not support the question or hints 1 and 2. The facts (landing in November 2018, end in 2022, mole stopped at about 40 cm) are correct. (http://127.0.0.1:8001/review/q-21209)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Videos of nature | 30 | 2 | 2 | 2 | 1 | 1 |
| q:video:volcano eruption video | 24 | 0 | 0 | 0 | 0 | 0 |
| total | 54 | 2 | 2 | 2 | 1 | 1 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 54 | 2 | 2 | 2 | 1 | 1 |
| total | 54 | 2 | 2 | 2 | 1 | 1 |

- $ per approved: $4.81

## Needs work

None.

## Question axes

- move: None 1
- stimulus: None 1
- clue: None 1
- answer_kind: None 1
- lens: None 1

## Dropped by the pipeline

- mf-2740413e17: overlap like q-20521: In 2003, Britain sent a small lander called Beagle 2 to the planet in this photo. Which planet is it? → Mars: Watch: a robot lander has hammered a probe deep into the ground to measure the heat inside a world. Which world is it? → Mars
