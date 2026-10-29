# tr-es-ES-13

Made by `qgen batch --translate es-ES` on 2026-10-28 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 296
- Needs work: 3
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 811, about $31.78 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-13&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-11 | tr-es-ES-12 | tr-es-ES-13 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 297 | 295 | 296 |
| needs_work |  | 3 | 5 | 3 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 1.7 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.3 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $29.50 | $30.69 | $29.05 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 4 (1 major)
- Mean |audit − final difficulty|: 1.0; ≥ 3 on 0 of 1 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.73

Major findings on approved questions:

- **q-1308**: giveaway — The source says «se lo estampan» and every option is masculine. The translation changed it to «se la estampan», and «Una tarta» is the only feminine option, so the pronoun in the question rules out all three wrong answers (hint 3 repeats «se la»). Fix: make the wording neutral, e.g. «…y los payasos lo estampan en la cara», or make the wrong answers feminine too. The answer, the wording for Spain (nata, pastelería, cubo, tartazo) and the fun fact are fine: «La batalla del siglo» (1927) used about 3000 pies. (http://127.0.0.1:8001/review/q-1308)

## Needs work

None.

## Not travelling

- **q-0397** needs_local_knowledge, confirmed: Mira la foto: ¿cómo se llama este dulce típico de la costa colombiana? → Cocadas (Asks for a Colombian coastal sweet; options (panelitas, alfandoques, bocadillos) are Colombian sweets unknown in Spain, and «bocadillos» means sandwiches there. Hints rely on Cartagena/Santa Marta beach culture.)

## Stale re-translated

None.
