# tr-es-ES-18

Made by `qgen batch --translate es-ES` on 2026-10-30 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 294
- Needs work: 6
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 812, about $35.49 at list price; $0.11 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-18&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-16 | tr-es-ES-17 | tr-es-ES-18 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 296 | 296 | 294 |
| needs_work |  | 4 | 4 | 6 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 1.3 % ✓ | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 1.0 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $29.97 | $30.07 | $31.81 |
| $ per approved |  | $0.10 | $0.10 | $0.11 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.68

Major findings on approved questions:

None.

## Needs work

- **q-0001** (drinks) ¿Qué bebida caliente, hecha con granos tostados, hace famosa a Colombia en todo el mundo? → El café: Fact check: wrong. The question asks which 'bebida caliente' Colombia is famous for, but the wrong answers include cold or non-hot drinks, so they are clearly wrong and fine. The real issue is the description: 'Los padres no funcionan...' is fine. However, 'Se cultiva en el Eje Cafetero' is true. The media query 'Valle de Cocora' is a valley known for wax palms, in the Eje Cafetero, so it is acceptable. Fun fact: Colombia is among the top coffee producers (3rd–4th largest) and is known for mild coffee, which is true. Leche can be served hot, so 'La leche' is arguably also a hot drink, but it is not made from roasted beans, so it stays wrong. I found no factual error; this is from background knowledge and I did no web search.
- **q-1530** (harry-potter) ¿Cómo se llama el juego mágico parecido a las canicas en el que las piedras le escupen un líquido apestoso al que pierde un punto? → Gobstones: Source: hint 1 ("Harry ve a otros alumnos jugarlo en Hogwarts") can't be confirmed from the books. Hint 2 says Eileen Prince was captain of the Gobstones "club", but HBP ch. 25 says she was captain of the Hogwarts Gobstones team. Both problems come from the source, so the source needs correcting first, e.g. hint 1 → Percy's old Gobstones set in PA, hint 2 → «capitana del equipo». The translation itself is faithful and reads naturally in Spain's Spanish. Fact check: uncertain. The answer (Gobstones) is right. The wrong answers (Ajedrez mágico, Snap explosivo, Quodpot) are different games, so they are really wrong. The fun fact is true: the stones are usually stone but can be precious metals, and a solid gold set is sold in Diagon Alley. I couldn't confirm hint 1: no source says Harry sees other students playing Gobstones. They only mention a Hogwarts Gobstones Club (OP) and Percy's old set (PA). Hint 2 is imprecise: Eileen Prince was captain of the Hogwarts Gobstones Team (HBP ch. 25), and president of the Gobstones Club.
- **q-2677** (reality-tv) Pasa casi al final del programa, el presentador lo anuncia y un concursante tiene que abandonar el concurso. ¿Cómo se llama? → Eliminación: Fact check: wrong. The description doesn't match the question. It says it is the moment someone remembers they left the oven on at home, but the question asks for the elimination of a contestant. The hints are also loose. The 'Nadie quiere que le toque' hint is vague. The fun fact is true in general (e.g. Survivor Redemption Island, Big Brother returnees). The answer 'Eliminación' and the wrong answers fit the question itself.
- **q-3271** (deserts) Los lagartos como este pasan horas al sol cada mañana. ¿Por qué lo hacen? → Para calentar su cuerpo: Fact check: wrong. Hint 1 says desert mornings are cool, but the iguana in the photo is only described as being on a sunny rock, so the desert claim is not shown. The fun fact is also loose. Iguanas do move to shade or burrows to avoid overheating, which is true. The wrong answers are fine and 'secarse las plumas' is clearly wrong because lizards have no feathers. The main answer is correct, since basking is thermoregulation. The question does not say 'iguana', so the 'como este' framing relies on the photo. The group answer_kind and 'purpose' framing are okay. The 'sin hacer nada' description is fine.
- **q-4205** (castles) Fíjate en esta parte de un castillo. ¿Cómo se llama? → Torreta: Fact check: wrong. The description says "despacho de la esquina... las peores escaleras" and the hint says "torre pequeña y redonda", but a turret is not necessarily round. More importantly, the fun fact is questionable: 19th-century revival castles' turrets were decorative, but "nunca protegieron a nadie" is an unverified generalisation. Also, the hint "Sobresale por encima del resto del castillo" is ambiguous (fits a tower/torre del homenaje). Wrong answers are fine (foso, puente levadizo, mazmorra are not turrets). Answer "Torreta" is acceptable, but the hints/fun fact are loose.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact says Marx's tomb in Highgate has a huge stone head, but the head is a bronze bust (Laurence Bradshaw, 1956) on a granite plinth. The translation copies the error faithfully («cabeza de piedra»). Fix the source to say bronze, then the translation to «cabeza de bronce». Fact check: wrong. The answer and hints are correct. Marx's tomb in Highgate Cemetery has a large bronze bust (by Laurence Bradshaw, 1956) on a granite plinth, so the fun fact's "cabeza de piedra" is inaccurate.

## Not travelling

None.

## Stale re-translated

None.
