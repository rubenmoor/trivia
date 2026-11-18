# batch-88

Made by `qgen batch --media-first` on 2026-11-18 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 3 (q-21204…q-21206)
- Approved: 2
- Needs work: 1
- Dropped by the pipeline: 0
- Reviewed by: claude-opus-5-5
- Claude calls: 125, about $9.75 at list price; $4.88 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-86, batch-87; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-86 | batch-87 | batch-88 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 87 | 28 | 3 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 29 | 15 | 0 |
| drop rate | ≤ 20.0 % | 33.3 % ✗ | 53.6 % ✗ | 0.0 % ✓ |
| dropped: hard fail correct |  | 1 | 1 | 0 |
| dropped: hard fail unambiguous |  | 2 | 1 | 0 |
| dropped: hard fail no_giveaway |  | 0 | 2 | 0 |
| dropped: overlap |  | 24 | 10 | 0 |
| dropped: duplicate |  | 2 | 1 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 58 | 13 | 3 |
| approved |  | 49 | 12 | 2 |
| needs_work |  | 9 | 1 | 1 |
| needs_work rate | ≤ 20.0 % | 15.5 % ✓ | 7.7 % ✓ | 33.3 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 13.8 % ✗ | 0.0 % ✓ | 33.3 % ✗ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 8.6 % ✓ | 7.7 % ✓ | 0.0 % ✓ |
| media: no pick in review 1 |  | 1 | 0 | 1 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 58 | 13 | 3 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 7.7 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 29.9 % ✗ | 39.3 % ✗ | 0.0 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 26 | 6 | 2 |
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
| mean fun | ≥ 3.40 | 3.52 ✓ | 3.32 ✗ | 3.67 ✓ |
| cost $ |  | $67.05 | $27.75 | $9.58 |
| $ per approved | ≤ $0.35 | $1.37 ✗ | $2.31 ✗ | $4.79 ✗ |
| calls |  | 725 | 322 | 122 |
| calls per approved |  | 14.80 | 26.83 | 61.00 |
| wall time h |  | 1.89 | 1.27 | 0.39 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 2 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: none
- Mean |audit − final difficulty|: 1.0; ≥ 3 on 0 of 3 (0 %)
- Audit/review agreement (both accept or both not): 2 of 3 (67 %)
- Sample: 3 audited of 3; 3 Claude calls, about $0.17

Major findings on approved questions:

None.

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 5 | 3 | 3 | 3 | 3 | 2 |
| cat:Videos of nature | 30 | 0 | 0 | 0 | 0 | 0 |
| q:audio:piano recording | 3 | 0 | 0 | 0 | 0 | 0 |
| q:video:experiment science video | 30 | 4 | 4 | 0 | 0 | 0 |
| q:video:volcano eruption video | 30 | 0 | 0 | 0 | 0 | 0 |
| total | 98 | 7 | 7 | 3 | 3 | 2 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 98 | 7 | 7 | 3 | 3 | 2 |
| total | 98 | 7 | 7 | 3 | 3 | 2 |

- $ per approved: $4.88

## Needs work

- **q-21204** (birds) Listen: which bird is singing in this recording? → Nightingale: The description's opening, “Tonight's headliner”, points at night singing, which is the nightingale's defining trait and the root of its name (the same clue hint 3 uses). Read with only the four options, it picks the nightingale over the song thrush, skylark and blackbird. Rewrite it to play on the concert theme without mentioning night or evening, for example “The headliner has no band, no stage and no ticket booth, just a very big voice.”

## Question axes

- move: None 3
- stimulus: None 3
- clue: None 3
- answer_kind: None 3
- lens: None 3

## Dropped by the pipeline

None.
