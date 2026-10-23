# tr-es-ES-2

Made by `qgen batch --translate es-ES` on 2026-10-23 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 821, about $28.52 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-2&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-1 | tr-es-ES-2 |
|---|---|---:|---:|
| sources |  | 50 | 300 |
| stale re-translated |  | 0 | 0 |
| translated |  | 50 | 300 |
| not travelling |  | 0 | 0 |
| not travelling confirmed |  | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 49 | 297 |
| needs_work |  | 1 | 3 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 |
| audit/review agreement | ≥ 90.0 % | 74.0 % ✗ | 98.3 % ✓ |
| cost $ |  | $5.20 | $26.36 |
| $ per approved |  | $0.11 | $0.09 |
| **health** | | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), style 4 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.16

Major findings on approved questions:

None.

## Needs work

- **q-2923** (brain-and-mind) En la película «Origen», cinco minutos de sueño en el mundo real equivalen a cuánto tiempo, más o menos, en el primer nivel del sueño? → 1 hora: The translation's fun fact says Nolan "rodó" (shot) Inception in 2010, but it was shot in 2009 and released in 2010. The source's "making the film in 2010" is loose, but "rodar" makes it plainly wrong. Use "estrenar" or "antes de que la película se estrenara en 2010" instead. Fact check: wrong. The answer is right (5 minutes is about 1 hour in the first level). The fun fact is wrong: Inception was filmed in 2009, not 2010. It was released in 2010.

## Not travelling

None.

## Stale re-translated

None.
