# tr-de-24

Made by `qgen batch --translate de` on 2026-11-04 (plan 66, D-81): `stem` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 299
- Needs work: 1
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 481, about $28.80 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-24&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-22 | tr-de-23 | tr-de-24 |
|---|---|---:|---:|---:|
| sources |  | 300 | 43 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 43 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 274 | 28 | 299 |
| needs_work |  | 26 | 15 | 1 |
| needs_work rate | ≤ 20.0 % | 8.7 % ✓ | 34.9 % ✗ | 0.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 4.7 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 6.3 % ✓ | 25.6 % ✗ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 2.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.0 % ✗ | 9.3 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 43 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 74.4 % ✗ | 100.0 % ✓ |
| cost $ |  | $39.67 | $6.39 | $26.17 |
| $ per approved |  | $0.14 | $0.23 | $0.09 |
| **health** | | ✗ fail | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 5 (0 major), difficulty 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.63

Major findings on approved questions:

None.

## Needs work

- **q-8753** (conservation) Wem gehört dieses flauschige Gesicht? → Roter Panda: Fact check: uncertain. The answer is right. The fun fact 'about 50 years before' is loose. The name 'panda' was used for the red panda from 1825. For the giant panda, the date is 1869 (description) or 1901 (first English use). That gives about 44 to 76 years.

## Not travelling

None.

## Stale re-translated

None.
