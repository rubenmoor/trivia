# tr-es-13

Made by `qgen batch --translate es` on 2026-10-28 (plan 66, D-81): `stem` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 299
- Needs work: 1
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 481, about $27.23 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-13&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-11 | tr-es-12 | tr-es-13 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 0 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 292 | 0 | 299 |
| needs_work |  | 8 | 0 | 1 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | n/a | 0.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | n/a | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | n/a | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | n/a | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| audited |  | 60 | 0 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | n/a | 100.0 % ✓ |
| cost $ |  | $31.29 | $17.46 | $24.71 |
| $ per approved |  | $0.11 | n/a | $0.08 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 2 (0 major), overlap 1 (0 major), media 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.51

Major findings on approved questions:

None.

## Needs work

- **q-8561** (chemical-reactions) ¿Qué tipo de compuesto químico es la herrumbre que cubre el hierro viejo? → Un óxido: In Spanish, rust is usually just called 'óxido', so this question collapses into the same fact as q-8751 (answer 'Óxido'): seeing one gives the other away, and the answer is obvious from everyday words. Consider marking this item as not travelling for Spanish (about_language), or dropping one of the two.

## Not travelling

None.

## Stale re-translated

None.
