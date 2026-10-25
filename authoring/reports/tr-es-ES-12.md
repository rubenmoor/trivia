# tr-es-ES-12

Made by `qgen batch --translate es-ES` on 2026-10-25 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 828, about $33.59 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-12&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-10 | tr-es-ES-11 | tr-es-ES-12 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 297 | 295 |
| needs_work |  | 2 | 3 | 5 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 1.0 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $28.80 | $29.50 | $30.69 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.90

Major findings on approved questions:

None.

## Needs work

- **q-0086** (football) En el fútbol, ¿qué jugador puede tocar el balón con las manos? → El portero: Fact check: uncertain. The answer (the goalkeeper) is the intended one, and the Higuita fun fact is true: his scorpion kick was at Wembley in 1995. But the wording is loose. Under the Laws of the Game, any outfield player uses their hands for throw-ins, and the referee can touch the ball on a dropped ball. So the wrong answers (forward, defender, referee) are not strictly wrong. The description's 'única persona' is also inaccurate, and 'Usa guantes' is typical but not required.
- **q-0137** (dinosaurs) Mira este esqueleto: ¿qué dinosaurio es? → Estegosaurio: Source: the description says the animal has «un garrote en la cola» (a club on its tail). That is wrong for the stegosaurus, which had tail spikes, and it describes the ankylosaurus, one of the wrong options, so it points players to a wrong answer. The source description should swap the club for spikes or another tail joke, e.g. «…con el tejado puesto y la cola llena de pinchos». The translation itself (a cuatro patas, empieza por, tejado, «…») reads as natural peninsular Spanish.
- **q-0295** (mountains) ¿Cuántas montañas hay en el mundo que superan los 8000 metros de altura? → 14: Fact check: wrong. Fun fact says Reinhold Messner is Italian and the first to climb all 14 in 1986: Messner (South Tyrolean, Italian citizen) did complete them in 1986 and was first, so that part holds. But the hint 'Todas están en Asia, en el Himalaya y el Karakórum' is true. The answer 14 is correct. Minor issue: the hint 'Son más de 10 pero menos de 20' is fine. Wrong answers 9, 21, 30 are wrong. Only possible nit: Messner's completion was without supplemental oxygen, and some dispute exists over Messner's Italian nationality label; overall the question is accurate.
- **q-3490** (knights) ¿Quién llevaba un traje como este en la corte de un rey medieval? → Un bufón: The description is ungrammatical: «…en el que se rieran de ti era señal de que lo hacías bien» has no subject for «era». It needs «en el que que se rieran de ti era señal…» or a smoother rewording such as «El único oficio de la corte en el que, si se reían de ti, era buena señal».
- **q-4205** (castles) Fíjate en esta parte de un castillo. ¿Cómo se llama? → Una torrecilla: Fact check: wrong. The question asks for a 'part of a castle', but the 'answer_kind' is place and the description calls it a corner office. More importantly, 'torrecilla' is a valid term (turret/bartizan = garita/torrecilla), but the hint 'Sobresale por encima del resto del castillo' and 'redonda' conflict with the image (a corbelled corner turret overhangs the corner, not rises above everything). The hint 'los guardias podían meterse dentro' fits. The fun fact is vague/unsourced ('muchas torrecillas ... solo decorativas' is plausible for Victorian castles but not verified). I did not run searches, so this is from general knowledge.

## Not travelling

None.

## Stale re-translated

None.
