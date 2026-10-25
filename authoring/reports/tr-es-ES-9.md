# tr-es-ES-9

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 814, about $31.66 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-9&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-7 | tr-es-ES-8 | tr-es-ES-9 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 297 | 298 | 297 |
| needs_work |  | 2 | 2 | 3 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.87 | $28.53 | $29.07 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: none
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.59

Major findings on approved questions:

None.

## Needs work

- **q-0558** (celebrations-around-the-world) Adivina: cuando llegan las fiestas me pinto la cara, me pongo un disfraz de colores y bailo en el desfile hasta que se acaba la fiesta. ¿Qué soy? → Un carnavalero: Fact check: uncertain. The answer "carnavalero" is a real Spanish word and the wrong answers (bombero, panadero, marinero) are clearly wrong. But I did not search, so I could not verify the fun fact about Barranquilla. The Carnaval de Barranquilla does have thousands of participants who prepare costumes for months, but "miles de carnavaleros" is vague. The riddle says "fiestas" while the hint says the name comes from the festival, which fits. The "trabajo favorito" hint is odd but harmless.
- **q-1858** (advertising-slogans) En 1910 se presentó en París un letrero que brilla en rojo gracias a un gas y anuncia tiendas de noche. ¿Qué inventor lo presentó? → Georges Claude: source: in 1910 Georges Claude showed neon lamps (tubes) at the Paris Motor Show, not a sign that advertised shops at night. The first neon sign was sold in 1912, as the fun fact itself says. The source and this translation both get this wrong. The question should say a red-glowing neon tube lamp was presented in 1910, which later became the basis of illuminated signs. Fact check: wrong. In 1910 Georges Claude presented neon lamps/tubes (Paris Motor Show, December 1910), not a sign. The first neon sign was sold in 1912 (as the fun fact says), so the question text contradicts the fun fact.
- **q-5355** (brand-origins) La fórmica cubrió infinidad de mesas y encimeras de cocina en los años 50. Es brillante, puede tener cualquier color o estampado y se limpia con un trapo. ¿Qué es? → Un laminado plástico: In Spain the word is «formica» (stressed on «mi», no accent mark); «fórmica» is the Latin American form (the DLE lists «fórmica» as used in America). Write «La formica» in the question text.

## Not travelling

None.

## Stale re-translated

None.
