# tr-es-11

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 636, about $34.50 at list price; $0.11 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-11&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-9 | tr-es-10 | tr-es-11 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 295 | 292 | 292 |
| needs_work |  | 5 | 8 | 8 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 2.7 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 2.3 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 96.7 % ✓ |
| cost $ |  | $30.69 | $30.70 | $31.29 |
| $ per approved |  | $0.10 | $0.11 | $0.11 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 1 (0 major), overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.21

Major findings on approved questions:

None.

## Needs work

- **q-2313** (cars) Cuelgo arriba del parabrisas y le muestro al conductor lo que hay detrás del vehículo, sin que tenga que voltear. ¿Qué soy? → El espejo retrovisor: Fact check: wrong. The riddle says the mirror hangs at the top of the windshield and shows what's behind, which fits. But the hint 'Puedes ver tu propia cara en mí' is true of any mirror and weak. The bigger issue is the hint 'Mi nombre dice que sirvo para ver hacia atrás' is fine. The fun fact is the real problem: the reversed 'AMBULANCE' lettering is meant to be read in a rearview mirror by drivers AHEAD of the ambulance, which is true, but 'en el frente' and 'su nombre' are okay. The answer and wrong answers (parasol, limpiaparabrisas, tablero) are correct. The 'sin que tenga que voltear' wording is fine. Main flaw: the description 'La única parte del vehículo que vive mirando al pasado' is a loose claim, since side mirrors and rear cameras also show what's behind.
- **q-2504** (french-revolution) La Revolución francesa convirtió a Francia por primera vez en esto, y hoy Francia va por su quinta versión. ¿Qué es? → República: The description uses feminine pronouns ("la estrenaron, la rompieron y la volvieron a armar"), so before any hint it rules out the masculine options "Imperio" and "Reino" and leaves only "República" and "Federación". Rewrite it without gendered pronouns that refer to the answer, for example as a joke about France starting over several times. It must not hint at a crown or at its absence.
- **q-2677** (reality-tv) Pasa casi al final del episodio, el presentador la anuncia y un concursante debe dejar el programa. ¿Cómo se llama? → La eliminación: Fact check: wrong. The description ('the moment in the show when someone suddenly remembers they left the oven on') has nothing to do with the question or answer (elimination). It looks like a mismatched or leftover text. The 'history' lens and 'name_concept' axes also don't fit. The answer 'La eliminación' and the wrong answers (audición, inmunidad, celebración) are fine. Hint 3 ('sacan por votación') is not true of every show, since some eliminations are by judges or by challenge. Hint 2 is fine, and the fun fact is true (e.g. Survivor's Redemption Island, Big Brother returnees).
- **q-3183** (anime) Meteoro maneja un auto de carreras blanco con una gran “M” roja en la parte delantera: el Mach 5. ¿Qué significa “Mach 5”? → Cinco veces la velocidad del sonido: Source: the fact check says the car's '5' is a pun on Japanese 'go' (five), and in the show's lore it is also the fifth car Mifune Motors built. That makes the distractor 'El quinto modelo del auto' / 'The fifth model of the car' arguably correct, and I can't rule it out from my own knowledge. The source should ask what the 'Mach' in the name refers to (the speed of sound), or swap that distractor for one that is clearly wrong. The description ('suena a examen de física') also leaves only the two physics options. The translation itself is faithful and reads naturally. Fact check: uncertain. The car's name is a double meaning. 'Mach' comes from the Mach number, but the '5' means it was the fifth racecar built by Mifune Motors (and puns on Japanese 'go' = 5). The car does not go Mach 5. So the distractor 'El quinto modelo del auto' is arguably correct, and the answer 'Cinco veces la velocidad del sonido' is questionable.
- **q-3271** (deserts) Los lagartos como este toman el sol durante horas cada mañana. ¿Por qué lo hacen? → Para calentar su cuerpo: Fact check: wrong. One wrong answer, "Para secarse las plumas", is silly for a lizard but fine as a distractor. The real issue is the hint "Las mañanas en el desierto pueden ser frías": iguanas (the photo subject) mostly live in tropical forests, not deserts. The fun fact is also shaky: iguanas do move to shade or burrows to cool down, which is accurate. The question says "lagartos como este" and the photo is an iguana, so the desert hint is a mismatch.
- **q-5458** (famous-philosophers) Este pensador alemán barbudo dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: Source: the fun fact says Marx's tomb at Highgate has a huge "stone head", but the head is a bronze bust (Laurence Bradshaw, 1956) on a granite plinth. The Spanish text copies the error ("cabeza de piedra"). Fix the source first, then the translation can follow it, e.g. "su enorme busto de bronce". Fact check: wrong. The answer (Karl Marx) and the wrong answers are fine: Darwin was English, Tolstoy Russian, Freud Austrian. The hints are true, and "Marx" has four letters. The fun fact is inaccurate: the huge head on Marx's tomb at Highgate Cemetery is a bronze bust by Laurence Bradshaw (1956) on a granite plinth, not stone. I did not run a web search. This is from memory.
- **q-6258** (famous-logos) ¿Qué color NO es uno de los colores de los anillos olímpicos? → Morado: Overlap: q-6930 (approved, colombia bundle) already asks the same fact in Spanish, which colour does NOT appear in the Olympic rings, with the same answer, Morado. A family that plays both bundles would get the same question twice. Keep only one of the two. The translation itself is faithful and reads naturally in es-419.
- **q-6665** (roman-empire) El rey Pirro venció a los romanos en batallas tan costosas que nos dejaron la expresión «victoria pírrica». ¿En qué siglo fue? → Siglo III a. C.: Fact check: wrong. The answer (3rd century BC) is correct, and Heraclea 280 BC and Asculum 279 BC are right. The description is false: Pyrrhus never asked for his money back. The real saying is that another such victory would ruin him.

## Not travelling

None.

## Stale re-translated

None.
