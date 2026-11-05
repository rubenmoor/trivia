# tr-es-ES-24

Made by `qgen batch --translate es-ES` on 2026-11-04 (plan 66, D-81): `stem` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 299
- Needs work: 1
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 468, about $25.89 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-24&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-22 | tr-es-ES-23 | tr-es-ES-24 |
|---|---|---:|---:|---:|
| sources |  | 300 | 193 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 193 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 291 | 186 | 299 |
| needs_work |  | 9 | 7 | 1 |
| needs_work rate | ≤ 20.0 % | 3.0 % ✓ | 3.6 % ✓ | 0.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.0 % ✓ | 3.6 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 98.3 % ✓ | 100.0 % ✓ |
| cost $ |  | $37.33 | $23.93 | $23.42 |
| $ per approved |  | $0.13 | $0.13 | $0.08 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 3 (0 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.46

Major findings on approved questions:

None.

## Needs work

- **q-8561** (chemical-reactions) ¿Qué tipo de compuesto químico es la herrumbre que sale en el hierro? → Un óxido: The question doesn't work in Spanish. The everyday word for rust is «óxido», and everyone says «el hierro se oxida», so even with «herrumbre» Spanish players hear the answer «Un óxido» as the plain word for rust. It also overlaps heavily with q-8751, whose answer is «Óxido» for what forms on an iron nail: seeing one gives the other away. Best to mark this item as not travelling (about_language) for es-ES rather than reword it. A minor point: «que sale en el hierro» reads awkwardly; «que se forma en el hierro» would be more natural.

## Not travelling

None.

## Stale re-translated

None.
