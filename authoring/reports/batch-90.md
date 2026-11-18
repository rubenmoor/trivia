# batch-90

Made by `qgen batch --media-first` on 2026-11-18 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 1 (q-21208…q-21208)
- Approved: 1
- Needs work: 0
- Dropped by the pipeline: 0
- Reviewed by: claude-opus-5-5
- Claude calls: 75, about $5.61 at list price; $5.61 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-88, batch-89; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-88 | batch-89 | batch-90 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 3 | 1 | 1 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 0 | 0 | 0 |
| drop rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 0 | 0 | 0 |
| dropped: overlap |  | 0 | 0 | 0 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 3 | 1 | 1 |
| approved |  | 2 | 1 | 1 |
| needs_work |  | 1 | 0 | 0 |
| needs_work rate | ≤ 20.0 % | 33.3 % ✗ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 33.3 % ✗ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| media: no pick in review 1 |  | 1 | no | no |
| media: recovered by research |  | 0 | no | no |
| media: no pick at record |  | 3 | yes | yes |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | n/a | n/a |
| overlap rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 2 | 1 | 1 |
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
| mean fun | ≥ 3.40 | 3.67 ✓ | 4.00 ✓ | 3.00 ✗ |
| cost $ |  | $9.58 | $7.54 | $5.56 |
| $ per approved | ≤ $0.35 | $4.79 ✗ | $7.54 ✗ | $5.56 ✗ |
| calls |  | 122 | 98 | 74 |
| calls per approved |  | 61.00 | 98.00 | 74.00 |
| wall time h |  | 0.39 | 0.45 | 0.24 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 1 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: none
- Mean |audit − final difficulty|: 0.0; ≥ 3 on 0 of 1 (0 %)
- Audit/review agreement (both accept or both not): 1 of 1 (100 %)
- Sample: 1 audited of 1; 1 Claude calls, about $0.05

Major findings on approved questions:

None.

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Videos of nature | 30 | 1 | 1 | 1 | 1 | 1 |
| q:video:experiment science video | 5 | 1 | 1 | 0 | 0 | 0 |
| q:video:volcano eruption video | 30 | 0 | 0 | 0 | 0 | 0 |
| total | 65 | 2 | 2 | 1 | 1 | 1 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 65 | 2 | 2 | 1 | 1 | 1 |
| total | 65 | 2 | 2 | 1 | 1 | 1 |

- $ per approved: $5.61

## Needs work

None.

## Question axes

- move: None 1
- stimulus: None 1
- clue: None 1
- answer_kind: None 1
- lens: None 1

## Dropped by the pipeline

None.
