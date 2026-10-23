# tr-es-2

Made by `qgen batch --translate es` on 2026-10-23 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 688, about $28.63 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-2&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-1 | tr-es-2 |
|---|---|---:|---:|
| sources |  | 50 | 300 |
| stale re-translated |  | 0 | 0 |
| translated |  | 50 | 300 |
| not travelling |  | 0 | 0 |
| not travelling confirmed |  | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 50 | 296 |
| needs_work |  | 0 | 4 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $5.62 | $26.22 |
| $ per approved |  | $0.11 | $0.09 |
| **health** | | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: style 3 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.40

Major findings on approved questions:

None.

## Needs work

- **q-2313** (cars) Cuelgo en la parte de arriba del parabrisas y le muestro al conductor lo que hay detrás del vehículo, sin girar la cabeza. ¿Qué soy? → El espejo retrovisor: Fact check: wrong. The first hint, 'Puedes ver tu propia cara en mí', is ambiguous and not wrong, but the riddle says the mirror is 'en la parte de arriba del parabrisas' and shows what's behind. That is correct. The real problem is the hint 'Mi nombre dice que sirvo para mirar hacia atrás', which gives away the answer ('retro-visor'). Also the description says 'la única parte del vehículo que vive mirando al pasado', which is a loose claim, since side mirrors and the backup camera also look back. The fun fact is true: ambulance fronts are lettered in mirror image. The answer and the wrong answers (parasol, limpiaparabrisas, tablero) are correct.
- **q-2745** (inventions) En este juego, ¿qué pieza debes proteger? Si queda atrapada, pierdes. → Rey: Fact check: wrong. The third hint says the king "is married to the queen" and "governs the board", which is a loose, misleading description. In chess the queen is the most powerful piece, and the king is not a ruler. The wording also fits the queen too well, so it points to the wrong answer. The "checkmate" fun fact is correct: it comes from Persian "shah mat", usually read as "the king is helpless/dead". The answer Rey is correct. The one-square movement hint is true (apart from castling). The wrong answers are valid.
- **q-4345** (farm-animals) En el libro de 1936 «El cuento de Ferdinando», al toro tranquilo le encanta sentarse bajo un árbol con una corteza como esta. ¿Qué árbol es? → Alcornoque: The fun fact uses Spain's release title «Olé, el viaje de Ferdinand». In Latin America the 2017 film came out as «Ferdinand», and the translator's own notes say that title was meant to be kept. Change the fun fact to «Ferdinand».
- **q-5824** (skyscrapers) En las películas, un pequeño incendio activa todos los rociadores de un edificio. En un rascacielos real, ¿qué rociadores echan agua? → Solo los que calienta el fuego: Fact check: wrong. The facts are right: sprinklers fire individually when their own heat-sensitive element is heated, smoke alone doesn't trigger them, and 68 °C (155 °F) is a common glass-bulb rating. But the wrong answer 'Solo los del piso en llamas' is close to being correct. In a real fire only heads near the fire open, and those are usually on the burning floor. This makes the question ambiguous.

## Not travelling

None.

## Stale re-translated

None.
