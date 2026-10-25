# tr-es-9

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 677, about $33.98 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-9&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-7 | tr-es-8 | tr-es-9 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 296 | 297 | 295 |
| needs_work |  | 4 | 3 | 5 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 1.0 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $30.10 | $30.42 | $30.69 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: overlap 1 (0 major), style 4 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.29

Major findings on approved questions:

None.

## Needs work

- **q-2313** (cars) Cuelgo en la parte de arriba del parabrisas y le muestro al conductor lo que hay detrás, sin que gire la cabeza. ¿Qué soy? → El espejo retrovisor: Fact check: wrong. The riddle says the object hangs at the top of the windshield, but the hints and fun fact are weak. The first hint, 'you can see your own face', also fits the sun visor's vanity mirror. The fun fact is loosely worded: the word 'AMBULANCE' is printed mirror-reversed on the front, not 'their name'. The wrong answer 'El parasol' is also questionable, because the sun visor sits at the top of the windshield and often has a mirror.
- **q-2622** (musical-instruments) Los guitarristas rasguean con esta pequeña pieza. ¿De qué material suele estar hecha hoy? → Plástico: Fact check: wrong. Guitar picks (púas) are not described accurately as the question says 'rasguean con esta pequeña pieza' fine, but the answer 'Plástico' is right; the problem is the hint 'Muchos juguetes y botellas están hechos del mismo material' is fine. The weak point is the fun fact: tortoiseshell picks were used, but 'plástico las reemplazó' is generally accepted (celluloid). Also the description says 'triangulito' which is fine. No clear error found.
- **q-2677** (reality-tv) Pasa cerca del final del episodio: el presentador lo anuncia y un participante tiene que dejar el programa. ¿Cómo se llama? → Eliminación: Fact check: wrong. The description (a moment when someone suddenly remembers they left the stove on at home) doesn't match the question or answer (elimination). The question is also vague: 'Inmunidad' and others are not clearly wrong, and the description doesn't fit any of the answers. The hint 'Nadie quiere que le toque' is fine, but the description belongs to a different question. Also the axes say 'three_facts' and 'history' but the content is generic.
- **q-4005** (temples-and-cathedrals) ¿Cuál de estas cosas NO forma parte del bautizo de un bebé en la iglesia? → Un anillo de bodas: Fact check: wrong. The odd-one-out question is flawed in two ways. Hint 1 says the priest pours something on the head, which fits water, but the wrong answers are also baptism items: water, a candle and a white garment are all part of the rite. The ring is correctly the odd one out. However, the description says the baby 'will sleep through the whole party', which is not an issue. The main flaw is hint 3: 'Los novios se lo intercambian' is true. The fun fact is misleading: some fonts are large enough for an adult to enter, which is true for immersion baptisteries, but it is not a general claim about fonts.
- **q-5458** (famous-philosophers) Este pensador alemán barbudo dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: Source error: the fun fact calls the head on Marx's Highgate tomb a stone head ("enorme cabeza de piedra"). It is a bronze bust by Laurence Bradshaw, standing on a granite plinth. The source fun fact needs correcting ("huge bronze head"), and the Spanish should then say "enorme cabeza de bronce".

## Not travelling

None.

## Stale re-translated

None.
