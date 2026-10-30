# tr-es-ES-17

Made by `qgen batch --translate es-ES` on 2026-10-29 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 793, about $33.04 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-17&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-15 | tr-es-ES-16 | tr-es-ES-17 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 296 | 296 | 296 |
| needs_work |  | 4 | 4 | 4 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 1.3 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.0 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $29.61 | $29.97 | $30.07 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), overlap 2 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.98

Major findings on approved questions:

- **q-6216**: overlap — The translation is faithful and natural for Spain: «Ratoncito Pérez» is a good local stand-in for the Tooth Fairy, and the hints and the fun fact are correct (in reindeer, both sexes grow antlers). The problem is the overlap with related q-3253, which asks what antlered animals pull on Christmas Eve and answers «El trineo de Papá Noel». It is the same reindeer → Santa's sleigh fact, so seeing one question gives the other away. This comes from the source, not the translation. (http://127.0.0.1:8001/review/q-6216)

## Needs work

- **q-0077** (disney-films) En «Encanto», ¿cuál es el don de Luisa? → Una fuerza sobrehumana: source: the fun fact says every member of the Madrigal family has a magic door with their gift. That's wrong: Abuela Alma has no door, nor do the in-laws Félix and Agustín, and Mirabel only gets hers at the end. Fix it in the source, for example to «Cada Madrigal con un don recibe una puerta mágica que lo muestra», and the translation will follow. The translation itself is faithful and reads as natural Spanish from Spain: «cada uno» and the «…» quotes are correct.
- **q-0662** (cartoons) ¿Qué tienen en común una lámpara mágica, una alfombra voladora y un loro llamado Iago? → Son de la película Aladdin: The translation correctly uses Spain's title «Aladdin», but the wrong answer «Mulán» keeps the Latin American spelling. In Spain the 1998 film was released as «Mulan», with no accent. Change it to «Son de la película Mulan».
- **q-2677** (reality-tv) Ocurre casi al final del programa, el presentador la anuncia y un concursante tiene que dejar el concurso. ¿Cómo se llama? → Eliminación: Fact check: wrong. The question is vague and the hints and description don't match it. 'Inmunidad' (immunity) and 'Celebración' could also fit a late-show segment, and 'Audición' is just a poor distractor. The description (someone remembering they left the oven on) has nothing to do with the question. The first hint ("no contestant wants to be picked") is fine. The third hint puts the answer's own concept in quotes ("expulsan por votación"), but not every show uses voting. Eliminations also don't always happen near the end of the show, and the host doesn't always announce them. The fun fact is true in general (e.g. Survivor, Big Brother and Drag Race have brought back eliminated contestants), but it isn't specific.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: Source: the fun fact calls the head on Marx's Highgate tomb a stone head, but it is a bronze bust (Laurence Bradshaw, 1956) on a granite plinth. The translation copies the error. Correct the source's fun fact to "bronze bust", then translate it again. Apart from that, the Spanish translation is faithful and reads naturally. Fact check: wrong. The answer and the hints are fine. The fun fact is wrong in one detail. The large head on Marx's tomb at Highgate is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth, not a stone head. I did not run a search; this is from memory.

## Not travelling

None.

## Stale re-translated

None.
