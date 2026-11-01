# tr-es-15

Made by `qgen batch --translate es` on 2026-10-31 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 585, about $37.06 at list price; $0.11 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-15&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-13 | tr-es-14 | tr-es-15 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 299 | 296 | 292 |
| needs_work |  | 1 | 4 | 8 |
| needs_work rate | ≤ 20.0 % | 0.3 % ✓ | 1.3 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $24.71 | $34.72 | $33.43 |
| $ per approved |  | $0.08 | $0.12 | $0.11 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: fact 1 (0 major), overlap 1 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.64

Major findings on approved questions:

None.

## Needs work

- **q-2638** (nobel-prizes) ¿De qué ganador del Nobel de la Paz de 1989 fue residencia de invierno este palacio? → El Dalái Lama: source: hint 1 ("The palace stands high in the Himalayas") is geographically wrong. The Potala is in Lhasa, on the Tibetan Plateau, well north of the Himalaya range, and the translation carries this over faithfully. Fix the hint in the source (e.g. "The palace stands at over 3600 metres above sea level, in Asia"), then re-translate it.
- **q-3136** (wonders-of-the-world) La estatua del Cristo Redentor está en la cima del cerro del Corcovado, en Río de Janeiro. ¿Qué altura tiene aproximadamente el cerro? → Unos 700 m: Fact check: wrong. The text is correct: Corcovado is about 710 m, and the statue is 30 m tall with arms 28 m wide. But the media query is 'Rio de Janeiro Sugarloaf Mountain'. That is a different hill (Pão de Açúcar, about 396 m), so the image would show the wrong mountain for a question about Corcovado.
- **q-3464** (international-football) ¿Qué club ha ganado más veces la máxima copa de clubes de Europa, la Copa de Europa o Champions League? → Real Madrid: source: the media file is "Real Madrid celebration after winning the 2018 UEFA Champions League Final", so the picture, shown sharp, shows the answer club celebrating with the very trophy asked about. Replace it with a trophy-only image (the slot's query, "UEFA Champions League trophy closeup") or a decorative stadium image. The Spanish text itself is fine.
- **q-4138** (basketball) Al inicio de un partido de baloncesto, el árbitro lanza el balón hacia arriba entre dos jugadores en el círculo central. ¿Qué intentan hacer ellos? → Palmearlo hacia un compañero: Fact check: wrong. The description says the referee 'makes the first throw' and the question says the referee throws the ball upward between two players. That fits. But the hint 'No deben agarrar el balón mientras va subiendo' is fine. The wrong answer 'Dejarlo rebotar una vez' is also wrong. However, the answer is correct per the rules: jumpers must tap the ball, not catch it. The fun fact 'salto entre dos' is correct. The remaining issue is that the 'Tirarlo directo al aro' distractor is also a rules violation, so it is wrong. The jump ball is correctly described. Minor point: the center-circle toss is accurate for the opening tip.
- **q-4153** (birds) Mira el enorme pico de este pelícano, con una bolsa elástica debajo. ¿Para qué sirve esa bolsa? → Para atrapar peces: Overlap: q-7612 (approved, Colombian animals) asks the same fact with the identical answer 'Para atrapar peces' about the pelican's pouch, so a player who gets both sees the same question twice. The translation itself is faithful and natural. The duplication comes from the source and the pool, not the wording, so the developer must decide which question to keep or whether bundles keep them apart.
- **q-5297** (animal-records) Soy verde o marrón y vivo en campos de hierba. Canto frotando las patas traseras contra las alas y salto unas 20 veces mi longitud. ¿Quién soy? → Saltamontes: Overlap: q-7608 (approved, colombia bundle) is almost the same riddle in Spanish, with a green insect in grass, long hind legs, big jumps and the answer grasshopper. Seeing one gives the other away. The translation itself is fine, so the developer should decide which of the two stays in the Spanish pool.
- **q-5458** (famous-philosophers) Este pensador alemán barbudo dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact is wrong. The huge head on Marx's Highgate tomb is a bronze bust by Laurence Bradshaw (1956) on a stone plinth, not a "cabeza de piedra". The translation faithfully repeats the error, so the source's fun fact must be corrected (e.g. "enorme busto de bronce"), then the Spanish can follow. Fact check: wrong. The answer (Karl Marx) and the wrong answers are fine. The fun fact is inaccurate: the giant head on Marx's tomb at Highgate Cemetery is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth, not a stone head. I did not run searches; this is from memory.
- **q-6258** (famous-logos) ¿Qué color NO es uno de los colores de los aros olímpicos? → Morado: Duplicate: approved q-6930 ("¿Cuál de estos colores NO aparece en los aros olímpicos?", answer Morado) asks the same fact with the same answer, as the rater noted. Source: this is a pool-level duplicate, not a translation fault, so one of the two should be dropped.

## Not travelling

None.

## Stale re-translated

None.
