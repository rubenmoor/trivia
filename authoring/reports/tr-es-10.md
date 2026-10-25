# tr-es-10

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 666, about $33.78 at list price; $0.11 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-10&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-8 | tr-es-9 | tr-es-10 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 297 | 295 | 292 |
| needs_work |  | 3 | 5 | 8 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 1.7 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.7 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $30.42 | $30.69 | $30.70 |
| $ per approved |  | $0.10 | $0.10 | $0.11 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: overlap 1 (0 major), media 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.08

Major findings on approved questions:

None.

## Needs work

- **q-2313** (cars) Cuelgo arriba del parabrisas y le muestro al conductor lo que hay detrás del vehículo, sin que gire la cabeza. ¿Qué soy? → El espejo retrovisor: Fact check: wrong. The hint 'Puedes ver tu propia cara en mí' is fine, but the question is ambiguous/flawed: the rear-view mirror shows what is behind through the rear window, which is accurate; however the description 'se pasa la vida mirando al pasado' is fine. Main issue: the fun fact is imprecise — ambulances print 'AMBULANCE' mirrored on the front so drivers read it correctly in their rear-view mirror (true), but the Spanish text says 'su nombre' (the ambulance's name), which is loosely worded. Also the wrong answer 'La visera para el sol' hangs in the same place (top of windshield), but does not show what's behind, so it is wrong as intended. Overall the answer is correct; only the fun fact wording needs tightening.
- **q-2465** (fashion-designers) Los diseñadores de moda lo hojean para elegir telas y colores. ¿Cómo se llama? → Un muestrario de telas: Fact check: wrong. The description says the book can't be read but can be "caressed", which is odd. The hint "Su nombre viene de la palabra «muestra»" is trivially true but gives away the answer. The fun fact claims about paint stores and the car industry are plausible. The bigger issue is that the question is ambiguous: designers also leaf through swatch books (cartas de colores, e.g. Pantone) for colors. The wrong answers (molde, tablero de inspiración, cuaderno de bocetos) are not things made of real fabric pieces, so they are wrong. The answer "muestrario de telas" is correct. Only minor wording issues. Not searched online.
- **q-2677** (reality-tv) Pasa casi al final del episodio, el presentador la anuncia y un concursante debe dejar el programa. ¿Cómo se llama? → La eliminación: Fact check: wrong. The description (remembering the oven left on at home) doesn't match the question about elimination. The answer 'La eliminación' fits, but the description is irrelevant/inconsistent. Also, hint 2 ('queda un jugador menos') nearly restates the answer, and the 'inmunidad' distractor is plausible only weakly. The fun fact is true in general (e.g., Survivor, Big Brother, Drag Race return twists).
- **q-3271** (deserts) Los lagartos como este se quedan horas al sol cada mañana. ¿Por qué lo hacen? → Para calentar su cuerpo: Fact check: wrong. The hint says 'En el desierto, las mañanas pueden ser frías', but iguanas are mostly tropical (rainforest/scrub), though desert iguanas exist; the fun fact says an iguana 'se esconde bajo tierra', which is true only of some species. The main issue: the wrong answer 'Para secarse las plumas' is silly but harmless. The answer (thermoregulation) is correct. The 'description' is not a clue. Minor: 'la luz del sol' options are fine.
- **q-4772** (world-currencies) Es una fábrica con prensas enormes que produce el dinero metálico de un país, y la de la antigua Roma estaba junto al templo de Juno Moneta. ¿Cómo se llama? → Una casa de moneda: In Spanish the clue "Juno Moneta" sounds almost the same as "moneda". The answer "Una casa de moneda" is also the only option that contains that word, so it gives itself away. Fix it in one of two ways: drop the Juno Moneta clue from the question and keep it for the fun fact, or rebuild the options in parallel form (e.g. "Una casa de moneda", "Una casa de cambio", "Una casa de empeño", "Una bolsa de valores") so the shared word doesn't single out the answer.
- **q-5433** (economy-and-stock-market) Se fundó en Bagdad en 1960, tiene su sede en Viena y una docena de países miembros. ¿Qué significa la sigla OPEP? → Organización de Países Exportadores de Petróleo: The fact check reports that the UAE left OPEC on 1 May 2026, so OPEC now has 11 members. The source hedges with "about a dozen", but the translation says "una docena" outright, which is now wrong. Restore the hedge ("unos doce países miembros" or "más de diez países miembros"). Everything else (the O-P-E-P distractors, the hints, the description and the fun fact) is fine. Fact check: wrong. The UAE left OPEC effective May 1, 2026, so OPEC now has 11 members, not 'una docena'. The acronym answer is right, but the clue is outdated.
- **q-5458** (famous-philosophers) Este pensador alemán barbudo dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: Source: the fun fact calls Marx's Highgate monument a "huge stone head", but the bust by Laurence Bradshaw is bronze; only the pedestal is stone. Correct the source to "bronze head" (or just "huge head"), then carry it over to the Spanish ("enorme cabeza de bronce").
- **q-6665** (roman-empire) El rey Pirro venció a los romanos en batallas tan costosas que nos dejaron la expresión «victoria pírrica». ¿En qué siglo fue? → Siglo III a. C.: Fact check: wrong. The answer (3rd century BC) is right. Pyrrhus won at Heraclea in 280 BC and Asculum in 279 BC, and the other centuries are wrong. The hints and fun fact match Plutarch's account. But the description says the winner asked for his money back, and no source says that. It is invented, and it also contradicts the fun fact, where Pirro says another such victory would ruin him.

## Not travelling

None.

## Stale re-translated

None.
