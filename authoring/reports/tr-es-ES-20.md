# tr-es-ES-20

Made by `qgen batch --translate es-ES` on 2026-10-30 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 291
- Needs work: 9
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 770, about $40.38 at list price; $0.12 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-20&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-18 | tr-es-ES-19 | tr-es-ES-20 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 294 | 295 | 291 |
| needs_work |  | 6 | 5 | 9 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 1.7 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.0 % ✓ | 1.3 % ✓ | 2.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $31.81 | $38.30 | $36.31 |
| $ per approved |  | $0.11 | $0.13 | $0.12 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 3 (0 major), fact 3 (0 major), media 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.07

Major findings on approved questions:

None.

## Needs work

- **q-1398** (famous-companies) La Guía Michelin, la de las estrellas para restaurantes, la creó una fábrica de neumáticos. ¿De qué país? → Francia: source: hint 3 says the founding brothers "eran de Clermont-Ferrand", but André and Édouard Michelin were both born in Paris; only the company is from Clermont-Ferrand. Correct the source hint, for example "La fábrica de los hermanos fundadores estaba en Clermont-Ferrand."
- **q-1525** (harry-potter) ¿Qué criaturas administran Gringotts, el banco de los magos? → Los gnomos: Fact check: wrong. In the Spanish editions of Harry Potter, Gringotts is run by 'duendes' (goblins), not 'gnomos'. In Spanish 'gnomos' are the garden pests, so the answer is a mistranslation of 'goblins'.
- **q-2307** (capital-cities) Perros como este protagonizan una película de Disney ambientada en Londres, con 101 cachorros manchados. ¿De qué raza es? → Dálmata: source: the question says the film has 101 spotted puppies, but it has 99 puppies, and the 101 Dalmatians include the parents, Pongo and Perdita. The source and the translation («101 cachorros manchados») both carry this error; rewording to '101 spotted dogs' (or similar) in the source would fix both.
- **q-2502** (french-revolution) Nací en la actual Bélgica, vestía traje de montar en el París revolucionario y en 1792 pedí que las mujeres pudieran llevar armas. ¿Quién soy? → Théroigne de Méricourt: source: hint 3 says her name was 'chosen' ('My chosen name'), but as far as I know 'Théroigne de Méricourt' was coined by the royalist press from Terwagne and Marcourt; she did not pick it. The rater flagged this too, and the source should say 'The name I am known by comes from Marcourt'. The Spanish faithfully repeats it, and 'mi nombre elegido' also sounds stiff, so it should become e.g. 'El nombre por el que me conocen viene de Marcourt, mi pueblo natal' once the source is corrected.
- **q-3136** (wonders-of-the-world) La estatua del Cristo Redentor se alza en lo alto del monte Corcovado, en Río de Janeiro. ¿Qué altura tiene el monte, aproximadamente? → Unos 700 m: Fact check: wrong. The facts check out from my own knowledge (no searches run). Corcovado is about 710 m. The statue is 30 m tall, not counting its 8 m pedestal, and its arms span 28 m. The Eiffel Tower is about 330 m, so the 'double' hint holds. The problem is the image. The query 'Rio de Janeiro Sugarloaf Mountain' would show Pão de Açúcar, a different mountain, in a question about Corcovado.
- **q-3464** (international-football) ¿Qué club ha ganado más veces que ningún otro la gran copa europea de clubes, la Copa de Europa o Champions League? → Real Madrid: source: the attached file is titled 'Real Madrid celebration after winning the 2018 UEFA Champions League Final', and this illustrative image is shown sharp, so it very likely reveals the answer in every language. I judged this from the title only because no picture was supplied. The file should be checked and replaced with a trophy-only or otherwise neutral image; the Spanish text itself is fine.
- **q-5286** (amazon-history-and-exploration) En la película «Fitzcarraldo», de Werner Herzog, un enorme barco fluvial como este se arrastró de verdad por una colina. ¿En qué país se rodó esa escena? → Perú: source: hint 1 is factually off. The film opens at the Manaus opera house in Brazil, a wrong option, and only then moves to Iquitos, so "the story starts" in the city with no road access is wrong and misleads anyone who knows the film. Change the source hint to something like "The film's hero lives in a rubber-boom city you can't reach by road", then carry that into the Spanish. The translation itself is faithful and natural.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact is wrong in the source and the translation copies it faithfully. The huge head on Marx's tomb at Highgate is bronze (Laurence Bradshaw's bust, 1956), not stone. Correct the source to "bronze bust" and carry the change over: «…donde su enorme busto de bronce sigue atrayendo a visitantes de todo el mundo». Fact check: wrong. The answer, wrong answers and hints are fine. The fun fact is slightly wrong: the huge head on Marx's tomb in Highgate Cemetery is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth, not stone. I did not run a web search. This comes from my own knowledge.
- **q-6281** (famous-villains) Su nombre significa «dragón» en latín, tiene el pelo rubio platino y es el rival de Harry Potter en el colegio. ¿En qué casa de Hogwarts está? → Slytherin: source: the fun fact calls Draco and Scorpius star names, but both are constellations, and the translation repeats this as «nombre de estrellas», so the fact check is 'wrong'. Correct the source fun fact to say constellation, for example «El hijo de Draco Malfoy también lleva nombre de constelación: Scorpius», then re-translate. Fact check: wrong. The answer (Slytherin), the wrong answers and the hints are correct. The fun fact is imprecise: Draco and Scorpius are constellations, not stars. Draco is also a constellation, so «también» only works if «constelaciones» is used.

## Not travelling

None.

## Stale re-translated

None.
