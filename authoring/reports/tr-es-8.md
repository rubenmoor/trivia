# tr-es-8

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 686, about $33.38 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-8&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-6 | tr-es-7 | tr-es-8 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 297 | 296 | 297 |
| needs_work |  | 3 | 4 | 3 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 1.3 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $28.43 | $30.10 | $30.42 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), overlap 2 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.96

Major findings on approved questions:

- **q-4654**: overlap — The translation itself is faithful and natural es-419: the options agree in form, the hints and fun fact are true, and the essential scarab image fits a "this animal" question. The problem is overlap with related q-0834, which asks which animal an Egyptian stone amulet had the shape of (the heart scarab), with the same answer, "escarabajo". Seeing either question gives the other away. (http://127.0.0.1:8001/review/q-4654)

## Needs work

- **q-3293** (earthquakes) Los bomberos les enseñan a los niños a usar este objeto rojo. ¿Para qué sirve? → Para apagar incendios pequeños: Source: hint 1 ("Firefighters carry much bigger ones on their trucks") is doubtful. Fire engines carry extinguishers about the same size as the ones in buildings, and their firefighting power comes from hoses and water tanks. The fact check is 'uncertain' and I can't confirm the hint either. Fix the source first, for example: "Los bomberos usan mangueras mucho más grandes para incendios grandes." The Spanish translation is otherwise faithful and natural. Fact check: uncertain. The answer (to put out small fires) is right, and the wrong answers are clearly wrong. Hints 2 and 3 are true, and the fun fact is true (early fire engines were pulled by hand, then by horses). Hint 1 is doubtful. Fire trucks mostly carry hoses and water tanks, and the extinguishers they carry are usually the same size or smaller, not 'much bigger'. I did not run any searches; this is from general knowledge.
- **q-4570** (advertising-slogans) En el siglo XIX, los carteles de circo se pegaban en estos enormes tableros junto a los caminos. ¿Cómo se llama este gran anuncio al aire libre? → Valla publicitaria: The description's feminine adjective ("nunca se queda afónica") agrees only with feminine options (valla, pancarta), so it rules out "Letrero de neón" and "Globo dirigible" before any hint. Make it gender-neutral, e.g. "Les grita a los conductores todo el día y nunca pierde la voz."
- **q-5666** (pirates) Mira esta parte llena de tallados de un antiguo barco de guerra de madera. ¿Qué parte del barco es? → La popa: Fact check: uncertain. Answer (popa/stern) and wrong answers (proa, quilla, bodega) are correct; hints and fun fact (rudder below stern, captain's cabin aft with big windows) are accurate. But the description's claim that the carvers were paid by the hour could not be verified (Vasa museum sources don't state pay basis). Also the Vasa's bow was carved too, and 'seguro' in the description is odd/unclear.

## Not travelling

None.

## Stale re-translated

None.
