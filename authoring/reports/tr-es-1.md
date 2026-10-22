# tr-es-1

Made by `qgen batch --translate es` on 2026-10-21 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 50 (0 stale re-translated)
- Translated: 50
- Approved: 50
- Needs work: 0
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 181, about $7.75 at list price; $0.11 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-1&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ stops the next `qgen batch --translate` until `qgen health ack` (D-55).

| metric | threshold | tr-es-1 |
|---|---|---:|
| sources |  | 50 |
| stale re-translated |  | 0 |
| translated |  | 50 |
| not travelling |  | 0 |
| not travelling confirmed |  | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ |
| approved |  | 50 |
| needs_work |  | 0 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ |
| audited |  | 50 |
| audit/review agreement | ≥ 90.0 % | 98.0 % ✓ |
| cost $ |  | $5.62 |
| $ per approved |  | $0.11 |
| **health** | | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 50 (2 %)
- Major among review needs work: 0 of 0
- Problems by kind: ambiguity 1 (1 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 50 (0 %)
- Audit/review agreement (both accept or both not): 49 of 50 (98 %)
- Sample: 50 audited of 50; 50 Claude calls, about $2.13

Major findings on approved questions:

- **q-3291**: ambiguity — Source issue: the riddle never says the thing holds water. A microwave or a toaster also sits in the kitchen, hums and switches itself off with a click when its timer runs out, so the wrong answer "Se acaba un temporizador de un minuto" can be defended until hint 1 mentions the water. The fix belongs in the source, for example by adding the water or the spout to the question text. The translation itself is faithful and natural es-419 ("hervidores", "pico", "100 °C"). The decorative kitchen image doesn't give the answer away, and the fun fact about the bimetallic disc is correct. (http://127.0.0.1:8001/review/q-3291)

## Needs work

None.

## Not travelling

None.

## Stale re-translated

None.
