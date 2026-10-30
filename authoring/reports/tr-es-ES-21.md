# tr-es-ES-21

Made by `qgen batch --translate es-ES` on 2026-10-30 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 288
- Needs work: 11
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 725, about $42.60 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-21&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-19 | tr-es-ES-20 | tr-es-ES-21 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 295 | 291 | 288 |
| needs_work |  | 5 | 9 | 11 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 3.0 % ✓ | 3.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 2.7 % ✓ | 3.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 95.0 % ✓ |
| cost $ |  | $38.30 | $36.31 | $38.60 |
| $ per approved |  | $0.13 | $0.12 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 2 (0 major), fact 2 (1 major), overlap 1 (0 major), media 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.01

Major findings on approved questions:

- **q-0410**: fact — The quoted line looks like the Latin American dub, or a literal rendering of the English, not Spain's: Spongepedia lists separate Spain lyrics, and the three Spanish lyric pages I could read (enparranda's «en castellano», olopoio, musica.com) contain neither «poroso» nor «absorbente y amarillo». So es-ES players are probably told to complete a line they never heard. This isn't conclusive: those pages are user-submitted, only the enparranda page is labelled castellano, and Spongepedia's and the Fandom wiki's lyrics wouldn't load, so check against the Spain intro (FormulaTV hosts it) and rewrite if it differs. If the source's line is simply Latin American, the source is fine and this is a translation issue. Hillenburg teaching marine biology checks out (Orange County Marine Institute); options, hints, description and coral image are fine. (http://127.0.0.1:8001/review/q-0410)

## Needs work

- **q-0748** (greek-heroes) En la mitología romana: Zeus es a Júpiter como Hades es a… → Plutón: source: hint 1 is false in both the source and the translation. It says the Romans also called a planet by this name, but Pluto was only discovered in 1930 and named after the god then. The source's hint needs correcting, for example to "Hoy un astro lejano lleva el nombre de este dios".
- **q-1060** (natures-records) ¿Cómo se llama el anciano de la película de Pixar que ata miles de globos a su casa? → Carl Fredricksen: Fact check: wrong. The answer (Carl Fredricksen), the wrong answers (Muntz is the villain, not the protagonist) and the hints are correct. But the description and fun fact are about Mount Roraima, and the image query is also Roraima. None of these mention Up or Carl. Roraima only loosely inspired the film's tepuis. The fun fact is true on its own terms (the rocks are about 1.7–2 billion years old), but it doesn't fit this question.
- **q-2307** (capital-cities) Los perros como este protagonizan una película de Disney ambientada en Londres, con 101 cachorros con manchas. ¿De qué raza son? → Dálmata: source: the question says the film has 101 spotted puppies, which is false. In the Disney film there are 99 puppies plus the parents Pongo and Perdita, 101 Dalmatians in all. The Spanish text faithfully repeats the error. Correct the source, for example to «101 perros con manchas», and then re-translate it.
- **q-2991** (sacred-places) Los peregrinos hacen el vía crucis por su ciudad vieja, sagrada para tres religiones, donde se dice que Jesús cargó con la cruz. ¿Qué ciudad es? → Jerusalén: Overlap with draft q-3918 (Vía Dolorosa): its text names Jerusalén and uses the same clue (pilgrims, the 14 stations, «por donde se dice que Jesús cargó con la cruz"), so seeing it gives this answer away. This comes from the source pair, not the translation. Resolve it by rewording q-3918 so it doesn't name the city, or by keeping only one of the two.
- **q-3136** (wonders-of-the-world) La estatua del Cristo Redentor se alza en la cima del monte Corcovado, en Río de Janeiro. ¿Qué altura tiene aproximadamente el monte? → Unos 700 m: Fact check: wrong. Text facts are right: Corcovado is about 710 m, the statue is 30 m tall with a 28 m arm span, and the Eiffel Tower is about 330 m. But the image query is 'Rio de Janeiro Sugarloaf Mountain'. That is a different mountain (Pão de Açúcar, about 396 m), so the illustration would show the wrong place.
- **q-3723** (legends-and-superstitions) Me escondo debajo de las camas y en los armarios oscuros, y los padres dicen que vengo a por los niños que no se duermen o no se portan bien. ¿Quién soy? → El Coco: Fact check: uncertain. The answer 'El Coco' is right, and the fun fact (Portuguese 'coco' = bogeyman, coconut named for its face-like three holes) is the standard etymology. Two weak spots. (1) The Sandman is a risky distractor: in Hoffmann's tale he takes the eyes of children who won't sleep, so he could fit the riddle. (2) The description 'monstruo al que los padres piden ayuda' is inaccurate, since parents invoke the Coco as a threat and don't ask it for help. The third hint ('saco') is more typical of 'el Hombre del Saco'. I did not run web searches, so this rests on my own knowledge.
- **q-3930** (science-fiction) En «Gru, mi villano favorito», Gru roba la Luna. ¿Qué artilugio usa para conseguirlo? → Rayo reductor: source: hint 2 is false in both the English source and the translation. In the film, Gru himself steals the shrink ray from the secret lab, and Vector then takes it from Gru. Vector did not steal it from the lab first. The source hint needs correcting, for example to "Vector le quita el aparato a Gru justo después de que Gru lo robe de un laboratorio secreto", and the translation should then follow it.
- **q-5286** (amazon-history-and-exploration) En «Fitzcarraldo», la película de Werner Herzog, un enorme barco fluvial como este se arrastró de verdad por una colina. ¿En qué país se rodó esa escena? → Perú: source: hint 1 is wrong, in the English source as well as the Spanish. The film's story opens at the opera house in Manaus, Brazil, not in road-less Iquitos, and Manaus is a wrong-option country, so the hint misleads. Reword the source hint, e.g. 'The film's hero lives in a rubber-boom city that you can't reach by road', then carry the change into the translation. The rater flagged this and it is still in the text.
- **q-5307** (art) Ocupo poco, pero me ves en zapatos, coches y móviles. Soy un dibujo o diseño que te dice al momento qué empresa ha hecho algo. ¿Qué soy? → Un logo: Fact check: wrong. The question says the logo is visible on 'zapatos, coches y móviles' and that it's a drawing/design identifying the company. That fits, but a mascot or other options could arguably also be identified as brand symbols; more importantly, hint 3 says 'una curva en forma de «visto»' (Nike swoosh) and 'manzana mordida' (Apple), both true logos. However, the description 'Tus zapatillas, tu móvil y tu caja de cereales' mentions cereal boxes, where mascots (e.g., Tony the Tiger) are common, making 'Una mascota' a partially plausible distractor. Also hint 1 'No soy una frase pegadiza que se dice en voz alta' is true for logo vs slogan.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact says Marx's head at Highgate is stone, but the monument's head is a bronze bust on a marble plinth. The English source needs correcting ("huge bronze head"), and the Spanish then follows («enorme cabeza de bronce»). The translation is otherwise faithful and natural.
- **q-6281** (famous-villains) Su nombre significa «dragón» en latín, tiene el pelo rubio casi blanco y es el rival de Harry Potter en el colegio. ¿A qué casa de Hogwarts pertenece? → Slytherin: source: the fun fact is inaccurate, and the translation repeats it. Draco and Scorpius are constellations, not stars, so «nombre de estrellas» and "star name" are wrong. The source fun fact needs correcting to "constellation name" (es: «nombre de constelación»); the fact check gives a correction. Fact check: wrong. The answer (Slytherin) and hints are right, but the fun fact is inaccurate. Draco and Scorpius are constellations, not stars. Draco is Latin for dragon.

## Not travelling

- **q-2574** other, confirmed: The greeting “Hola!” comes from the language of the country with this flag. Which language is it? → Spanish (Asks which language «¡Hola!» comes from, shown with Spain's flag. For players in Spain the answer is the language they are playing in and the flag is their own, so it is no longer a question.)

## Stale re-translated

None.
