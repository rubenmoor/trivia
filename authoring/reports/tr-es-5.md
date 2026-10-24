# tr-es-5

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 293
- Needs work: 7
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 702, about $32.29 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-5&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-3 | tr-es-4 | tr-es-5 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 298 | 293 |
| needs_work |  | 2 | 2 | 7 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 0.7 % ✓ | 2.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $28.36 | $27.96 | $29.52 |
| $ per approved |  | $0.10 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: overlap 2 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.77

Major findings on approved questions:

- **q-2488**: overlap — The related q-7030 (colombia bundle, needs_work) asks the same fact: how many penalties each team kicks before sudden death, answer 5. Colombian players get both bundles, so they would meet this fact twice. The translation itself is faithful and the facts hold (5 kicks, then sudden death; McCrum, Irish goalkeeper, 1891; about 11 m to the spot). "De a un tiro" is a little regional, but it's understandable and only minor. (http://127.0.0.1:8001/review/q-2488)

## Needs work

- **q-2568** (language) Los lobos hacen este sonido largo con el hocico hacia arriba, a menudo de noche, y los dibujos animados lo adoran bajo la luna llena. ¿Cómo se llama? → Un aullido: Fact check: wrong. The fun fact is not supported: wolves howl to communicate over long distances, and the claim that they don't howl at the moon is correct, but the range is usually given as up to about 10 km (6–10 miles) in open terrain, which is acceptable. The hint 'Canta un «uuuu»...' is fine. The real issue is that the question says 'sonido largo con el hocico hacia arriba', which is correct. Not checked against sources in detail.
- **q-2714** (famous-philosophers) Friedrich Nietzsche escribió: “Dios ha muerto… y nosotros lo hemos matado”. ¿Qué quiso decir? → La fe ya no guiaba la vida de la gente moderna: Fact check: wrong. The description says 'Cuatro palabras', but 'Dios ha muerto' is three words in Spanish ('Gott ist tot' is also three). The quote shown in the question is longer. The rest holds: La gaya ciencia (1882), the madman with a lantern in the market, and the answer.
- **q-4079** (world-war-ii) Cuando la guerra impidió que el jarabe de Coca-Cola llegara a Alemania, allí se inventó un nuevo refresco de naranja, la Fanta. ¿En qué década? → La década de 1940: source: the question calls the 1940 German Fanta "a new orange soda" ("un nuevo refresco de naranja"), but the wartime original was a fruit soda made from whey and apple pomace with changing fruit flavours. Orange Fanta first appeared in Italy in 1955. Fix the source by saying "a new fruit soda" or just "a new soda". The Spanish then follows it as "un nuevo refresco de frutas" or "un nuevo refresco".
- **q-4675** (prehistory) Una piedra grande y plana sobre la que se frota a mano otra más pequeña, de adelante hacia atrás. Los agricultores del Neolítico la usaban a diario. ¿Para qué? → Moler grano para hacer harina: Hint 3 says "Sin él, no habría pan", but the question calls the object "una piedra… la usaban", which is feminine, so the pronoun doesn't agree. It should be "Sin ella, no habría pan." Also consider "hacia adelante y hacia atrás" in place of "de adelante hacia atrás", which reads as a single direction.
- **q-5364** (castles) ¿Cuál de estas cosas NO podían usar en un castillo medieval para iluminar un cuarto oscuro? → Una linterna de pilas: Fact check: uncertain. Fun fact says almost all castle candles were tallow; nobles commonly used costly beeswax candles, so 'casi todas' is overstated. Answer is fine.
- **q-5571** (language) Estoy lleno de palabras ordenadas de la A a la Z. Si buscas una, te digo qué significa y cómo se escribe. ¿Qué soy? → Un diccionario: Fact check: wrong. The riddle is ambiguous: an encyclopedia or a telephone directory (alphabetical lists) could fit loosely, and a directory is also A–Z ordered, so 'Un directorio telefónico' is not clearly wrong. The hint 'Hoy en día también vivo dentro de celulares' is fine. The riddle itself (meaning and spelling) points to a dictionary, but a phone directory is also alphabetical, though it gives no meanings or spelling. The fun fact is true in general. Also the description says 'nobody reads it cover to cover', which is fine.
- **q-6258** (famous-logos) ¿Qué color NO es uno de los colores de los anillos olímpicos? → Morado: This duplicates q-6930, an approved question in the colombia bundle. It asks the same thing: which colour is not on the Olympic rings, answer 'Morado'. Spanish-speaking players with both bundles would get the same question twice. Keep one of the two, or replace this one with a different fact about the Olympic rings.

## Not travelling

None.

## Stale re-translated

None.
