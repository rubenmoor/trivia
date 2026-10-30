# tr-es-ES-23

Made by `qgen batch --translate es-ES` on 2026-10-30 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 193 (0 stale re-translated)
- Translated: 193
- Approved: 186
- Needs work: 7
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 408, about $27.96 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-23&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-21 | tr-es-ES-22 | tr-es-ES-23 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 193 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 193 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 288 | 291 | 186 |
| needs_work |  | 11 | 9 | 7 |
| needs_work rate | ≤ 20.0 % | 3.7 % ✓ | 3.0 % ✓ | 3.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.3 % ✓ | 3.0 % ✓ | 3.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 95.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $38.60 | $37.33 | $23.93 |
| $ per approved |  | $0.13 | $0.13 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 2 (0 major), fact 6 (1 major), media 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.02

Major findings on approved questions:

None.

## Needs work

- **q-0748** (greek-heroes) En la mitología romana: Zeus es a Júpiter como Hades es a… → Plutón: source: hint 1 says «Los romanos también llamaban así a un planeta… o casi planeta», which is false: Pluto was only discovered in 1930 and named then, so the Romans never used the name for any planet. The translator noted this but kept it. The source needs correcting, for example to say the far-off world discovered in the 20th century bears this god's name. The translation copies it word for word, so it should follow once the source is fixed.
- **q-3136** (wonders-of-the-world) El Cristo Redentor se alza en la cima del Corcovado, en Río de Janeiro. ¿Qué altura tiene más o menos esa montaña? → Unos 700 m: Fact check: wrong. The text facts hold. Corcovado is about 710 m high. The statue is 30 m tall, not counting its 8 m pedestal, and its arms span 28 m. Eiffel tower is about 330 m, so 'double' is fair. The wrong answers are clearly wrong. The problem is the media: the image query is 'Rio de Janeiro Sugarloaf Mountain'. That is a different mountain (about 396 m), so the image doesn't match a question about Corcovado.
- **q-3930** (science-fiction) En «Gru, mi villano favorito», Gru roba la Luna. ¿Qué artilugio usa para hacerlo? → Rayo reductor: source: hint 2 is factually wrong, and the Spanish translation repeats it. In the film, Gru and the Minions steal the shrink ray from the secret lab, then Vector takes it from Gru, so Vector did not steal it from the lab. The source hint needs correcting, for example to "Vector se lo había quitado a Gru justo después de que este lo robara de un laboratorio secreto".
- **q-4078** (world-war-ii) Encerrado en una celda tras un golpe fallido en Múnich, Adolf Hitler empezó a escribir «Mi lucha». ¿En qué año? → 1924: source: the fun fact that Hitler dictated much of the book to Rudolf Hess is a popular legend. Recent historians (e.g. Plöckinger) conclude that he typed most of it himself, so the English source's fun fact should be replaced or corrected first (for example, by saying that Hess was imprisoned with him and helped edit the book). The Spanish translation is otherwise faithful.
- **q-4079** (world-war-ii) Cuando la guerra dejó a Alemania sin jarabe de Coca-Cola, allí se inventó un nuevo refresco de naranja, la Fanta. ¿En qué década? → Los años 40: source: the fact is wrong. Wartime German Fanta (1940) was not an orange soda; it was made from whey, apple pomace and other leftovers, and orange Fanta only appeared in Italy in 1955. The English source should drop "orange" (e.g. "a new soda, Fanta"), and the translation should then follow it. The fact_check's 'confirmed' overlooks this, though the rater and translator both flagged it.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact is wrong in the English source as well as in the translation. The head on Marx's Highgate tomb is a bronze bust (Laurence Bradshaw, 1956) on a granite plinth, not stone. Correct the source to 'huge bronze bust', then the Spanish can follow: 'su enorme busto de bronce'. Fact check: wrong. The fun fact says Marx's huge head at Highgate is made of stone. The monument is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth. Everything else checks out.
- **q-5784** (norse-mythology) En God of War, Kratos es un espartano calvo que deja Grecia por las tierras nórdicas con su hijo Atreus. ¿Qué significa su nombre en griego? → Fuerza: source: the question says Kratos leaves Greece for the Norse lands with his son Atreus, which is wrong. In the games he leaves Greece alone and Atreus is born later in Midgard, so the premise needs correcting in the source (e.g. "who leaves Greece for the Norse lands, where he raises his son Atreus"). The translator flagged this too; the fact check missed it.

## Not travelling

None.

## Stale re-translated

None.
