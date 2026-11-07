# batch-50

Made by `qgen batch` on 2026-11-07 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): current-music, rivers-and-mountains, scientists-and-explorers, modern-literature, legends-and-superstitions, tv-series, radio-and-internet, classic-literature, flamenco-and-copla, 20th-century, regional-symbols, spanish-cinema, monuments, creatures, plants-and-climate, tv-shows-and-presenters, comics-and-childrens-books, tapas, national-symbols, painting-and-architecture, bourbons-and-19th-century, football-clubs, brands-and-shops, footballers-and-national-team, famous-figures, sportspeople, ancient-hispania
- Merged: 232 (q-15215…q-15446)
- Approved: 214
- Needs work: 18
- Dropped by the pipeline: 88
- Reviewed by: claude-opus-5-5
- Claude calls: 528, about $75.63 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-48, batch-49; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-48 | batch-49 | batch-50 |
|---|---|---:|---:|---:|
| source locale |  | en | de | es-ES |
| drafts |  | 323 | 349 | 320 |
| skipped slots |  | 127 | 137 | 166 |
| dropped |  | 102 | 80 | 88 |
| drop rate | ≤ 20.0 % | 31.6 % ✗ | 22.9 % ✗ | 27.5 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 4 |
| dropped: hard fail unambiguous |  | 1 | 1 | 1 |
| dropped: hard fail no_giveaway |  | 23 | 21 | 17 |
| dropped: overlap |  | 74 | 55 | 66 |
| dropped: duplicate |  | 2 | 2 | 1 |
| dropped: fact-check wrong |  | 2 | 1 | 0 |
| merged |  | 221 | 269 | 232 |
| approved |  | 196 | 251 | 214 |
| needs_work |  | 25 | 18 | 18 |
| needs_work rate | ≤ 20.0 % | 11.3 % ✓ | 6.7 % ✓ | 7.8 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 4.5 % ✓ | 1.1 % ✓ | 0.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 2.2 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.5 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.4 % ✗ | 1.5 % ✗ | 1.3 % ✗ |
| needs_work: media | ≤ 10.0 % | 6.3 % ✓ | 1.9 % ✓ | 4.3 % ✓ |
| media: no pick in review 1 |  | 27 | 41 | 30 |
| media: recovered by research |  | 20 | 37 | 23 |
| media: no pick at record |  | 8 | 4 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 24.5 % ✗ | 17.5 % ✓ | 21.9 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 71.1 % ✓ | 74.1 % ✓ | 55.8 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.27 ✓ | 1.76 ✗ | 0.53 ✓ |
| approved 11–15 |  | 54 | 55 | 49 |
| top move | ≤ 25.0 % | 17.6 % ✓ | 14.1 % ✓ | 16.4 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 81.9 % | 82.2 % | 81.5 % |
| values stimulus |  | 5 | 4 | 3 |
| top clue | ≤ 60.0 % | 38.0 % ✓ | 42.8 % ✓ | 45.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.3 % ✓ | 30.9 % ✓ | 20.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 24.4 % ✓ | 20.4 % ✓ | 20.3 % ✓ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 18.1 % ✓ | 17.8 % ✓ | 18.5 % ✓ |
| mean fun | ≥ 3.40 | 3.49 ✓ | 3.50 ✓ | 3.46 ✓ |
| cost $ |  | $64.67 | $83.13 | $71.78 |
| $ per approved | ≤ $0.35 | $0.33 ✓ | $0.33 ✓ | $0.34 ✓ |
| calls |  | 455 | 533 | 468 |
| calls per approved |  | 2.32 | 2.12 | 2.19 |
| wall time h |  | 1.74 | 2.37 | 2.24 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 4 (0 major), fact 2 (0 major), media 3 (2 major), difficulty 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.84

Major findings on approved questions:

None.

## Needs work

- **q-15224** (ancient-hispania) Este símbolo de tres espirales, el trisquel, se ve por toda Galicia y Asturias. ¿Con qué pueblo antiguo se relaciona? → Con los celtas: None of the candidates shows a triskele (three joined spirals), and the essential image has to show one. Search again with something like 'triskelion Celtic stone' or 'trisquel gallego'. The question text itself is fine. No se encontró una imagen adecuada para esta pregunta.
- **q-15234** (bourbons-and-19th-century) Mira este detalle: ¿de qué cuadro famoso es? → «El 3 de mayo en Madrid»: Hint 2 gets the scene backwards. It says French soldiers are being shot, but the painting shows French soldiers shooting the people of Madrid after the uprising of 2 May 1808. The fact check flagged this. It should read something like «Muestra los fusilamientos de madrileños por soldados franceses tras el levantamiento del 2 de mayo contra Napoleón». Verificación de datos: wrong. Hint 2 reverses the scene: the painting shows French soldiers executing Spanish civilians (the rebels), not French soldiers being shot.
- **q-15240** (brands-and-shops) Mira esta foto: en esta tienda venden tornillos, martillos, llaves inglesas y clavos. ¿Cómo se llama? → Ferretería: No candidate works for the essential image. All six are black-and-white archive shots of 1900–1940s shop interiors (mostly Finnish), and none clearly shows screws, hammers or spanners. Candidate 6 also has a caption reading 'Hardware Store'. Because the text already lists the tools, the media could be switched to illustrative (e.g. a close-up of screws and nails, or hand tools on a pegboard) rather than searching for an essential store interior again. No se encontró una imagen adecuada para esta pregunta.
- **q-15283** (football-clubs) ¿Cuántas estrellas tiene el escudo del Atlético de Madrid, el del oso y el madroño? → 7: This repeats a question already in the pool: approved q-14338 asks how many stars are in the border of the Madrid city coat of arms, around the bear and the strawberry tree (answer 7). The Atlético crest's seven stars are the same Madrid stars, and the question even points to them with "el del oso y el madroño". Seeing one question gives away the other. Also, hint 2 (same as the Comunidad de Madrid flag) nearly gives the answer away to players in Spain.
- **q-15298** (modern-literature) En «El tiempo entre costuras», Sira abre su taller en esta ciudad, capital del protectorado español en Marruecos. ¿Cuál es? → Tetuán: The media slot doesn't match itself. It is marked essential and its note asks for a clear view of Tetuán's medina, but the query was "vintage sewing machine", so every candidate is a sewing machine. The question text answers itself without a photo, so the slot should become illustrative with the sewing-machine query. Candidate 1 (a vintage sewing machine, no text) would then fit. Or keep the slot essential and search for the medina, but that would add little. No se encontró una imagen adecuada para esta pregunta.
- **q-15309** (national-symbols) Este bombo gira cada 22 de diciembre mientras unos niños cantan números y premios. ¿Qué sorteo es? → La Lotería de Navidad: None of the media candidates shows the Christmas lottery drum. 1 and 2 are engravings of the 1683 Thames Frost Fair, and 3 is a roundabout with sculptures. The question says «Este bombo», so the essential image has to show the bombo itself, and no new search is allowed. The text is fine. No se encontró una imagen adecuada para esta pregunta.
- **q-15318** (painting-and-architecture) Francisco Pacheco es a Velázquez lo que Velázquez es a Juan Bautista Martínez del Mazo. ¿Qué relación es? → Maestro y suegro: Hint 2 ("Velázquez se casó con Juana Pacheco") gives the answer away: it shows that Pacheco was Velázquez's father-in-law, and «Maestro y suegro» is the only option with that relationship. Hint 2 should give a vaguer clue, for example that the link was both professional and family, without naming the marriage. The marriage can move to hint 3, and the Mazo–Francisca detail can go in the fun fact.
- **q-15345** (creatures) De noche ves llamitas azules flotando sobre el campo: es el fuego fatuo. Según la tradición popular, ¿qué eran? → Almas de difuntos: No media candidate fits. The four candidates are two scanned handwritten letters from 1856 and two book scans of a stone elephant statue in Nepal, none of them a night meadow or anything to do with will-o'-the-wisps. A new search isn't allowed. A query like "foggy field night" or "marsh at dusk" should find a usable decorative image. No se encontró una imagen adecuada para esta pregunta.
- **q-15350** (current-music) En 2018, «Lo malo» quedó segunda en la gala para elegir la canción de España en Eurovisión. ¿Quiénes ganaron? → Amaia y Alfred: This overlaps with approved q-13269 ("¿Quién es este cantante, que salió de OT 2017 y fue a Eurovisión 2018 junto a Amaia?" → Alfred García). That text says Amaia and Alfred went to Eurovisión 2018, so it gives away who won the 2018 gala. Seeing either question gives away the other.
- **q-15360** (football-clubs) El Barça, el Levante y el Eibar visten de azulgrana. ¿Qué colores son? → Azul y granate: Verificación de datos: uncertain. Azulgrana is blue + 'grana' (RAE), not 'granate'. Grana and granate are related dark reds but not the same word. The answer, the hint 'nombre antiguo de un color' and the fun fact are inconsistent with each other.
- **q-15365** (modern-literature) ¿Quién escribió «El pirata Garrapata», el desastroso pirata de los libros infantiles? → Juan Muñoz Martín: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-15377** (rivers-and-mountains) Según la tradición, el Parque Nacional de Doñana debe su nombre a una mujer que vivió allí. ¿A quién? → A una duquesa llamada Ana: Hint 2 («No era de la realeza, pero sí de la alta nobleza») rules out all three wrong answers at once: the queen is royalty, and a shepherdess or a saint aren't high nobility. Only the duchess is left. Rewrite hint 2 so it points vaguely towards her era or family without naming her rank, for example that she was the daughter of a famous princess at Philip II's court.
- **q-15381** (spanish-cinema) Estás viendo «Planet 51» y los habitantes verdes del planeta huyen aterrados de un visitante recién llegado del espacio. ¿Quién es? → Un astronauta de la Tierra: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-15406** (scientists-and-explorers) El ingeniero vasco Alejandro Goicoechea, la «G» del Talgo, probó el primer prototipo de su tren articulado ligero. ¿En qué década? → En los años cuarenta: Hint 3 contains a factual error: the 1942 prototype was the Talgo 0 (the experimental train), not the Talgo I. The Talgo I was built by ACF in the USA and tested around 1949–50. Hint 3 should say «El primer prototipo, el Talgo 0, se probó en 1942.» The answer itself (the 1940s) is correct. Verificación de datos: wrong. Hint 3 is inaccurate. The 1942 prototype was the Talgo 0. The Talgo I was built by ACF in the USA and tested in Spain around 1949-50. The answer (1940s) is still correct.
- **q-15415** (spanish-cinema) La estatuilla de los Premios Goya es el busto del pintor que les da nombre. ¿En cuál de estas ciudades NO vivió él? → Lisboa: No candidate shows the Goya statuette, which the question names: the sheet has a glass atheist award, a porcelain Figaro figurine, museum figurines, two 1930 Oscar photos and a Russian wiki-award. A new search isn't allowed, so the slot needs a real photo of the Goya bust, for example "Premios Goya estatuilla" or "Goya Award bust bronze". No se encontró una imagen adecuada para esta pregunta.
- **q-15430** (tapas) En este local se piden cañas, tercios y jarras, y su nombre sale de la bebida que más se sirve. ¿Qué local es? → Una cervecería: Overlaps the approved q-9915 («de cañas» → cerveza). This question's main clue is that cañas are ordered there, so anyone who has seen q-9915 knows the answer is the place named after beer. Both questions rest on the same fact: a caña is beer.
- **q-15436** (tv-series) ¿A qué personaje de «La que se avecina» da vida este actor? → Amador Rivas: The question depends on recognising the actor's face, and no candidate gives a clear one. Candidate 1 is Pablo Chiapella, but it is a dim, distant stage shot in which his face is tiny. Candidates 2–6 are Swiss landscapes and buildings (Chapella) and a Michigan historical sign. A new search isn't allowed, so the slot needs a close, clear portrait of Pablo Chiapella, or the question must change. No se encontró una imagen adecuada para esta pregunta.
- **q-15440** (tv-series) Este actor fue Julio Olmedo, el camarero que busca a su hermana desaparecida en «Gran Hotel». ¿Quién es? → Yon González: The essential image slot has no candidates and no new search is allowed. The question needs a clear photo of Yon González's face with no caption naming him or the series. Find one manually, or turn the question into a text-only version with illustrative media, such as the Palacio de la Magdalena. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 9, cause_effect 8, count 9, estimate 4, identify 38, made_of 10, name_concept 26, odd_one_out 20, origin 24, purpose 11, record 2, sequence 9, when 21, who 30, word_meaning 11
- stimulus: detail 8, none 189, photo 35
- clue: completion 5, direct 106, riddle 23, scenario 44, three_facts 54
- answer_kind: group 34, number 14, person 47, place 30, thing 39, time 23, word 45
- lens: body_senses 9, educational_media 27, everyday 35, history 47, language 38, nature 2, pop_culture 39, popular_science 1, school 21, university 13

## Dropped by the pipeline

- 20th-century-1: overlap like q-14457: Nació en 1989, su símbolo fue durante años una gaviota y lo presidieron Aznar y Rajoy. ¿Qué significan sus siglas PP? → Partido Popular: Lees en un libro de historia que Manuel Fraga fundó Alianza Popular en 1976. ¿En qué partido se convirtió en 1989? → Partido Popular
- 20th-century-5: overlap like q-12281: ¿Cuánto mide, más o menos, la Gran Vía de Madrid de punta a punta? → Algo más de 1 kilómetro: ¿Cuánto mide de largo la Gran Vía de Madrid, de la calle de Alcalá a la plaza de España? → Algo más de 1 kilómetro
- 20th-century-6: overlap like q-12407: La palabra «tebeo» viene del TBO, una revista de historietas de Barcelona. ¿En qué año salió su primer número? → En 1917: Tiene viñetas y bocadillos, su nombre viene de una revista infantil de 1917 y Mortadelo y Filemón salían en uno. ¿Cómo se llamaba en España? → Un tebeo
- 20th-century-9: overlap like q-6843: El trapero tiene un palo largo, se moja en el balde y se exprime antes de usarlo. ¿Para qué sirve? → Para limpiar el piso: Este invento español de los años 50 libró a millones de personas de una tarea muy dura. ¿Cuál? → Fregar el suelo de rodillas
- 20th-century-10: overlap like q-1764: En España, la derrota ante EE. UU. que les hizo perder Cuba y Puerto Rico se llama «el Desastre del…». ¿Qué número completa el nombre? → 98: Tras perder Cuba, Puerto Rico y Filipinas en 1898, España vivió una crisis que pasó a la historia con un nombre. ¿Cuál? → El Desastre
- 20th-century-13: overlap like q-1252: ¿Cuál de estos payasos NO formó parte de 'Los Payasos de la Tele' junto con Miliki? → Cepillín: Estás viendo a los Payasos de la Tele en los años 70. ¿Cuál de estos NO era uno de ellos? → Pompoff
- 20th-century-16: overlap like q-10020: Es transparente, tiene burbujas y un toque dulce. Mezclada con vino tinto da el tinto de verano. ¿Qué es? → La gaseosa: Su anuncio decía «Si no hay Casera, nos vamos» y se mezcla con vino para hacer tinto de verano. ¿Qué pides en un bar si dices «una casera»? → Una gaseosa
- ancient-hispania-3: overlap like q-0263: La Edad del Bronce se llama así por el bronce, que se hace mezclando cobre con otro metal. ¿Con cuál? → Estaño: Los argáricos de Almería y Murcia lo fundían en hornos, hacían con él puñales y hachas, y da nombre a su época. ¿Qué es el bronce? → Una mezcla de cobre y estaño
- ancient-hispania-6: overlap like q-4540: You hunt wild animals and gather wild plants, and nobody on Earth has a farm yet. In which era are you living? → The Paleolithic: No tengo campos ni rebaños: cazo ciervos con arco y en la Cueva de la Araña (Valencia) me pintaron cogiendo miel silvestre. ¿Quién soy? → Un cazador-recolector
- ancient-hispania-12: overlap like q-1433: Navegamos todo el Mediterráneo, fundamos Cartago y creamos un alfabeto que inspiró al griego. ¿Quiénes somos? → Los fenicios: Los fenicios fundaron Gadir (Cádiz), comerciaban por todo el Mediterráneo y usaban un alfabeto de 22 letras. ¿Qué escrituras salieron de él? → Los alfabetos griego y latino
- bourbons-and-19th-century-6: overlap like q-8029: En 1808 mis tropas entraron en España y dejé al rey Fernando VII sin trono. Sin rey, en la Nueva Granada nacieron juntas de gobierno. ¿Quién soy? → Napoleón Bonaparte: Fui emperador de los franceses, invadí España en 1808 y puse en su trono a mi hermano José, al que llamaban «Pepe Botella». ¿Quién soy? → Napoleón Bonaparte
- bourbons-and-19th-century-7: overlap like q-9850: Mira este detalle. Su nombre árabe era «el monte de Tariq», por el general que desembarcó aquí en el año 711. ¿Qué es? → El Peñón de Gibraltar: Es un gran peñón en el extremo sur de Andalucía, es británico desde 1704 y en él viven monos en libertad. ¿Qué es? → Gibraltar
- bourbons-and-19th-century-16: overlap like q-11312: Este es el escudo de España. ¿Qué antiguo reino representa el castillo dorado sobre fondo rojo? → Castilla: Mira este detalle del escudo de España: un castillo y un león. ¿Qué antiguos reinos representan? → Castilla y León
- brands-and-shops-13: overlap like q-9848: La ONCE nació en 1938 y su cupón se vende en quioscos por la calle y se sortea casi a diario. ¿A quiénes da trabajo sobre todo? → A personas ciegas: La ONCE, la de los cupones de lotería, nació en España en 1938. ¿Quiénes la formaron? → Personas ciegas
- classic-literature-1: overlap like q-5583: This statue shows a famous knight from La Mancha on his skinny horse. Who is the round man on the donkey beside him? → Sancho Panza: Este personaje viaja en burro y suelta refranes sin parar, como «Al buen entendedor, pocas palabras bastan». ¿Quién es? → Sancho Panza
- classic-literature-6: overlap like q-9942: El 23 de abril, día de San Jorge, las calles se llenan de puestos y la gente se regala rosas y libros. ¿Dónde es típica esta costumbre? → En Cataluña: El Día del Libro, en Cataluña se regalan libros y rosas por Sant Jordi. ¿Cómo se dice «Sant Jordi» en castellano? → San Jorge
- classic-literature-15: overlap like q-5583: This statue shows a famous knight from La Mancha on his skinny horse. Who is the round man on the donkey beside him? → Sancho Panza: Rucio, un burro como este, es uno de los animales más famosos de la literatura española. ¿Quién era su dueño? → Sancho Panza
- comics-and-childrens-books-3: overlap like q-11157: Zipi y Zape nacieron en 1948 en la revista Pulgarcito, de la editorial Bruguera, dibujados por Josep Escobar. ¿En qué ciudad estaba esa editorial? → Barcelona: ¿Qué dibujante creó a Zipi y Zape, los gemelos traviesos de la escuela Bruguera? → Josep Escobar
- comics-and-childrens-books-11: overlap like q-11176: La nana «Duérmete, niño» avisa de que, si no duermes, vendrá alguien que te comerá. ¿Quién? → El coco: Canciones como «Duérmete, niño, duérmete ya…» son nanas. ¿Qué es una nana? → Una canción para dormir a los bebés
- comics-and-childrens-books-14: overlap like 20th-century-6: Tiene viñetas y bocadillos, su nombre viene de una revista infantil de 1917 y Mortadelo y Filemón salían en uno. ¿Cómo se llamaba en España? → Un tebeo: Su nombre viene de una antigua revista española y hoy casi todos lo llaman con una palabra inglesa. ¿Qué es un tebeo? → Un cómic
- creatures-0: overlap like q-10047: ¿Cuál de estos seres NO pertenece a la mitología vasca, la de la diosa Mari? → El ojáncano: Las sorginak sirven a la diosa Mari, se reúnen de noche cerca de las cuevas y su nombre aún significa «brujas». ¿De qué mitología son? → De la mitología vasca
- creatures-6: overlap like q-10048: La Tragantía, mitad mujer y mitad serpiente, canta en un castillo la noche de San Juan y se traga a quien la oye. ¿De qué pueblo es la leyenda? → Cazorla: En muchas leyendas de España, la Encantada sale de su fuente o su castillo una sola noche al año. ¿Qué noche es? → La noche de San Juan
- creatures-16: overlap like q-14274: Mira el cuadro «El aquelarre», de Goya: las brujas rodean a un macho cabrío. ¿Cuántos cuernos tiene? → 2: Presido las reuniones nocturnas de brujas en los prados, tengo cuernos y barba, y Goya me pintó en su «El aquelarre». ¿Quién soy? → El macho cabrío
- current-music-11: overlap like q-11164: Me celebro cada invierno en la Costa Blanca, nací en 2022 y de mí salió Chanel con «SloMo» rumbo a Eurovisión. ¿Qué soy? → El Benidorm Fest: Nací en Cuba, crecí en Cataluña, bailé en el musical «El Rey León» y en 2022 di a España su mejor Eurovisión en décadas. ¿Quién soy? → Chanel
- famous-figures-0: overlap like q-11324: TheGrefg presentó su propia skin de Fortnite ante casi 2,5 millones de personas a la vez, récord de Twitch entonces. ¿En qué año? → 2021: En enero de 2021, TheGrefg batió el récord de espectadores en Twitch al presentar su propia skin. ¿De qué videojuego era? → Fortnite
- famous-figures-1: overlap like q-14485: Lo dice un cocinero vasco en la tele desde los años noventa, al probar sus platos y entre chiste y chiste. ¿Qué frase es? → «Rico, rico y con fundamento»: Soy la palabra con la que Karlos Arguiñano cierra su frase más famosa: «Rico, rico y con…». ¿Qué palabra soy? → Fundamento
- famous-figures-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Qué youtuber español de Minecraft tomó su nombre de un príncipe saiyan de «Dragon Ball», con una letra de más? → Vegetta777
- famous-figures-5: overlap like q-11259: En Andalucía es normal oír «¡Quillo, ven!». ¿De qué palabra es un acortamiento «quillo»? → Chiquillo: El streamer malagueño Illojuan lleva en su nombre «illo», una palabra andaluza para llamar a alguien. ¿De qué palabra viene? → Chiquillo
- football-clubs-9: overlap like q-3464: Which club has won Europe's top club cup, the European Cup or Champions League, more times than any other? → Real Madrid: Mira este trofeo: ¿qué club lo ha ganado más veces? → El Real Madrid
- football-clubs-13: overlap like q-2548: This coach won the Champions League with both Barcelona and Manchester City. Who is he? → Pep Guardiola: Mira la foto: ¿quién es este entrenador español? → Pep Guardiola
- footballers-and-national-team-5: overlap like q-15282: Inglaterra es a la Premier League como España es a… → LaLiga: Es la liga que más dinero ingresa del mundo y en ella han triunfado Rodri y Cucurella. ¿Cómo se llama la liga de Inglaterra? → Premier League
- footballers-and-national-team-8: overlap like q-2740: In 2024, Lamine Yamal became the youngest player ever to score at a European Championship. How old was he? → 16: Estás viendo la semifinal de la Eurocopa 2024 y Lamine Yamal marca un golazo a Francia. ¿Cuántos años tiene? → 16
- legends-and-superstitions-8: overlap like q-0913: Se te cae el espejo del baño y se rompe en pedazos. Según la famosa superstición, ¿cuántos años de mala suerte te esperan? → 7: Se te cae un espejo y se hace añicos. Según la superstición, ¿cuántos años de mala suerte te esperan? → 7
- legends-and-superstitions-10: overlap like q-0534: Pasar debajo de una escalera, que se te cruce un gato negro y abrir un paraguas dentro de la casa: ¿qué tienen en común? → Según las supersticiones, traen mala suerte: Te protege cuando llueve, se abre y se cierra y, según la superstición, nunca hay que abrirlo dentro de casa. ¿Qué es? → Un paraguas
- legends-and-superstitions-14: overlap like q-12371: En la fachada de la Universidad de Salamanca hay una ranita de piedra que todos buscan. ¿Sobre qué está sentada? → Sobre una calavera: Según la tradición, el estudiante que encuentra la rana de la fachada de la Universidad de Salamanca aprueba. ¿Sobre qué está la rana? → Sobre una calavera
- legends-and-superstitions-15: overlap like q-0534: Pasar debajo de una escalera, que se te cruce un gato negro y abrir un paraguas dentro de la casa: ¿qué tienen en común? → Según las supersticiones, traen mala suerte: La usan los pintores, tiene peldaños y, según la superstición, nunca hay que pasar por debajo. ¿Qué es? → Una escalera
- monuments-4: overlap like q-14344: Esta flecha amarilla aparece pintada en muros y piedras de muchos pueblos de España. ¿Para qué sirve? → Para guiar a los peregrinos: Mira la foto: esta concha aparece en mojones, paredes y mochilas por todo el norte de España. ¿A quiénes guía? → A los peregrinos
- monuments-5: overlap like q-2238: Who designed this colorful park in Barcelona? → Antoni Gaudí: Mira esta casa del paseo de Gracia de Barcelona, con un tejado que recuerda al lomo de un dragón. ¿Quién la diseñó? → Antoni Gaudí
- monuments-11: overlap like q-1861: Se hace con pedazos de baldosa o cerámica rota, se pega como mosaico y Gaudí lo usó mucho. ¿Cómo se llama esta técnica? → Trencadís: Mira este dragón de la escalinata del Park Güell, en Barcelona. ¿De qué está cubierto? → De trocitos de azulejo
- national-symbols-3: overlap like q-4665: Look at this close-up. You show this little booklet at the airport when you travel to another country. What is it? → Passport: Es granate, lleva el escudo de España en la tapa y te lo sellan al entrar en otros países. ¿Qué es? → El pasaporte
- national-symbols-7: overlap like q-0842: Mira las estrellas que hay encima del escudo de esta camiseta. ¿Qué cuentan? → Los Mundiales que ganó esa selección: Completa: la estrella dorada sobre el escudo de la camiseta de España significa que la selección ganó… → Un Mundial
- national-symbols-8: overlap like q-10137: Estoy en Madrid, y dentro de mí 350 personas elegidas debaten y votan las leyes. Dos leones de bronce guardan mi puerta. ¿Qué soy? → El Congreso de los Diputados: Estos leones de bronce guardan el edificio donde la princesa Leonor juró la Constitución al cumplir 18 años. ¿Cuál es? → El Congreso de los Diputados
- national-symbols-10: overlap like bourbons-and-19th-century-16: Mira este detalle del escudo de España: un castillo y un león. ¿Qué antiguos reinos representan? → Castilla y León: Mira esta bandera. ¿De qué comunidad autónoma es? → Castilla y León
- national-symbols-12: overlap like q-11296: Iniesta marcó en la prórroga el gol que dio a España su primer Mundial. ¿En qué minuto? → 116: ¿Quién marcó el gol con el que España ganó el Mundial de fútbol de 2010? → Andrés Iniesta
- painting-and-architecture-2: overlap like q-11314: Este cuadro, «La lechera de Burdeos», lo pintó hacia 1827 un pintor español exiliado en esa ciudad francesa. ¿Quién? → Francisco de Goya: Llegué a Burdeos de niña con mi madre, compañera de Goya, y él me enseñó a dibujar. Hay expertos que creen que «La lechera de Burdeos» es mía. ¿Quién soy? → Rosario Weiss
- painting-and-architecture-5: duplicate like q-13213: En 1879 alguien vio por primera vez los bisontes pintados en el techo de la cueva de Altamira. ¿Quién fue? → Una niña de 8 años: Mira la foto: ¿quién se fijó por primera vez en estos bisontes pintados en el techo de una cueva, en 1879? → Una niña de 8 años
- painting-and-architecture-10: overlap like q-5349: The daisy-shaped Chupa Chups lollipop logo was designed in 1969 by a famous Spanish painter. Who? → Salvador Dalí: Me dibujó en 1969 un pintor surrealista en menos de una hora. Tengo forma de margarita y salgo en golosinas de todo el mundo. ¿Qué soy? → El logotipo de Chupa Chups
- plants-and-climate-7: overlap like q-13302: Mira la foto: este fruto cae de las encinas en las dehesas. ¿Para qué es famoso en España? → Para engordar cerdos: Mira la foto: en otoño, las encinas de la dehesa sueltan estas bellotas. ¿Para qué se aprovechan sobre todo? → Para engordar a los cerdos ibéricos
- plants-and-climate-12: overlap like q-12475: Entras en una bodega de La Rioja y huele a barricas de roble. ¿Qué se hace allí? → Vino: Mira la foto: en las bodegas de La Rioja hay filas y filas de barricas de roble. ¿Para qué sirven? → Para envejecer el vino
- regional-symbols-3: overlap like q-13391: Mira este escudo de España. ¿Qué antiguo reino representa la pieza roja con hojas verdes que hay en la parte de abajo? → El Reino de Granada: Esta fruta aparece en la parte de abajo del escudo de España. ¿Qué antiguo reino representa? → El Reino de Granada
- regional-symbols-8: overlap like q-9890: Mira este acueducto de Segovia. ¿Qué pueblo lo construyó? → Los romanos: Aparece en el escudo de Segovia, es de granito, lo levantaron los romanos y sus piedras se sostienen sin argamasa. ¿Qué es? → El acueducto
- 20th-century-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Naranjito, una naranja vestida con la camiseta de la selección, fue la mascota del Mundial de fútbol de España. ¿En qué año? → 1982
- bourbons-and-19th-century-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Soy un paseo de Madrid que Carlos III adornó con fuentes como la de Neptuno y la de Apolo. ¿Quién soy? → El Paseo del Prado
- bourbons-and-19th-century-13: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Este es «el Empecinado», que atacaba por sorpresa con partidas pequeñas. ¿En qué guerra se hizo famosa la palabra «guerrilla»? → La Guerra de la Independencia
- brands-and-shops-5: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: La caja de Magia Borrás, con su varita y sus cubiletes, es un clásico de los Reyes. ¿Cuándo nació la juguetera Borrás? → A finales del siglo XIX
- brands-and-shops-6: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: ¿Qué marca inventó la botella de cuello curvo para limpiar bajo el borde del váter? → Pato WC
- comics-and-childrens-books-2: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: Anacleto, agente secreto, es un espía muy torpe que Manuel Vázquez dibujó en los años 60 para Bruguera. ¿Qué saga parodiaba? → Las películas de James Bond
- comics-and-childrens-books-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Carpanta, el personaje de Escobar que vive bajo un puente, se llama como una palabra del diccionario. ¿Qué significa «carpanta»? → Hambre muy grande
- creatures-4: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Al ver pasar un gato negro, alguien dice: «Yo no creo en las meigas, pero haberlas, haylas». ¿Qué quiere decir? → Que no se lo cree, pero por si acaso
- famous-figures-7: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Ibai Llanos nació en 1995 y es muy del Athletic, el club de su ciudad. ¿De qué ciudad es? → Bilbao
- flamenco-and-copla-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Nací entre los gitanos de Barcelona, Peret me hizo famoso con «Borriquito» y me llevó a los Juegos Olímpicos de 1992. ¿Qué soy? → La rumba catalana
- flamenco-and-copla-15: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Una lámpara como esta es el premio más codiciado de un gran festival flamenco. ¿Qué cantes premia? → Los cantes mineros
- footballers-and-national-team-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: En un partido de fútbol, todos los jugadores llevan tres de estas cosas. ¿Cuál lleva solo el portero? → Guantes acolchados
- monuments-2: overlap like bourbons-and-19th-century-9: Soy un paseo de Madrid que Carlos III adornó con fuentes como la de Neptuno y la de Apolo. ¿Quién soy? → El Paseo del Prado: «Vivo en una fuente de Madrid, voy en un carro tirado por caballos de mar y llevo un tridente. Los del Atleti vienen a celebrar conmigo.» ¿Quién soy? → Neptuno
- monuments-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Montserrat, en Cataluña, debe su nombre en catalán a la forma de sus picos. ¿A qué herramienta se parecen? → A una sierra
- monuments-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El Canal de Isabel II se fundó en 1851 y su primera gran obra fue una presa en el río Lozoya. ¿Qué empezó a llevar a Madrid? → Agua para beber
- monuments-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: «Llevo el nombre de un presidente del club, estoy en el paseo de la Castellana de Madrid y aquí juega el equipo blanco.» ¿Quién soy? → El Santiago Bernabéu
- plants-and-climate-10: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: El pinsapo solo crece de forma natural en unas pocas sierras de Cádiz y Málaga. Tiene hojas como agujas y forma de cono. ¿Qué es? → Un abeto
- radio-and-internet-10: hard fail: correct 1, unambiguous 2, no_giveaway 4, no_overlap 5: ¿En qué año se celebró el primer Mundial de Globos, el torneo de Ibai en el que no puede caer el globo al suelo? → 2021
- regional-symbols-7: overlap like q-3427: Riddle: “We are two great rocks, one in Europe and one in Africa. Ancient sailors said the known world ended past us.” What are we? → The Pillars of Hercules: Aparezco en el escudo de Andalucía entre dos columnas, domando a dos leones. La leyenda dice que yo puse esas columnas en el Estrecho. ¿Quién soy? → Hércules
- scientists-and-explorers-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es de la Armada, se botó en Cartagena en 1990 y casi cada año viaja a la Antártida. ¿Para qué sirve el buque Hespérides? → Para la investigación oceanográfica y polar
- scientists-and-explorers-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Lo inventó un poeta gallego, Alejandro Finisterre, tras ver en un hospital a niños que no podían jugar al fútbol, y lo patentó en 1937. ¿Qué es? → El futbolín
- tapas-10: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Mira de cerca este encurtido de bar. ¿Qué es? → Cebollitas en vinagre
- rivers-and-mountains-0: overlap like q-10004: La montaña más alta de España está en la isla de Tenerife. ¿Cómo se llama? → Teide: Los guanches lo llamaban Echeyde y creían que dentro vivía Guayota, un demonio. Es la montaña más alta de España. ¿Cuál es? → El Teide
- rivers-and-mountains-1: overlap like q-9864: ¿Quiénes pintaron estos bisontes en la cueva de Altamira? → Cazadores del Paleolítico: Estos bisontes están pintados en el techo de la cueva de Altamira, en Cantabria. ¿Quién los pintó? → Personas de la Prehistoria
- scientists-and-explorers-1: overlap like q-2021: Estás viendo los dibujos de neuronas más famosos de la historia, hechos a mano por un Nobel de Medicina. ¿Quién los hizo? → Santiago Ramón y Cajal: Este dibujo de neuronas lo hizo a mano un médico español que ganó el Premio Nobel en 1906. ¿Quién era? → Santiago Ramón y Cajal
- scientists-and-explorers-3: overlap like q-10138: En los partidos de la selección española, la afición se viste de rojo y se pinta la cara de rojo y amarillo. ¿Por qué esos colores? → Son los colores de la bandera de España: Los aviones de la Patrulla Águila hacen acrobacias juntos y dejan en el cielo humo rojo y amarillo. ¿De dónde salen esos colores? → De la bandera de España
- scientists-and-explorers-4: overlap like q-1179: Te subes en Madrid a un tren llamado AVE, sigla de 'Alta Velocidad Española'. ¿Más o menos a qué velocidad máxima puede llevar pasajeros? → Unos 300 km/h: ¿Qué tipo de tren es este, que une Madrid y Sevilla desde 1992? → Un AVE
- scientists-and-explorers-17: overlap like q-13260: Cristóbal Colón es a la Santa María como Juan Sebastián Elcano es a la… → Nao Victoria: Esta es una réplica del primer barco que dio la vuelta al mundo, en 1522. ¿Cómo se llamaba? → Victoria
- spanish-cinema-3: overlap like q-4362: At a big film awards night like the Oscars, when do the stars walk the red carpet? → Before the ceremony: Se extiende a la puerta de la gala de los Goya, los famosos desfilan por ella con esmoquin y tacones y posan ante los fotógrafos. ¿Cómo se llama? → La alfombra roja
- spanish-cinema-9: overlap like q-11589: En un estudio, actores hablan mirando la pantalla para que las caricaturas extranjeras se oigan en español. ¿Qué es? → El doblaje: Una orden de 1941 me hizo obligatorio en los cines de España. Gracias a mí, John Wayne y Marilyn Monroe hablaban castellano sin estudiarlo. ¿Qué soy? → El doblaje
- sportspeople-14: overlap like q-12479: Mira la foto: Marc Gasol y Serge Ibaka ganaron en 2019 el anillo de la NBA con el equipo de esta ciudad. ¿Cuál es? → Toronto: Si ves a Marc Gasol con su anillo de campeón de la NBA de los Toronto Raptors, ¿de qué año es ese título? → 2019
- tapas-5: overlap like q-14390: Es una salsa blanca y espesa, típica de Cataluña, Valencia y Baleares, y acompaña al arroz negro. ¿Qué significa su nombre, alioli? → Ajo y aceite: Soy patata cocida en trozos, bañada en una salsa blanca de ajo y aceite, y mi apellido viene del catalán. ¿Qué soy? → Patatas alioli
- tv-series-13: overlap like q-14481: ¿Cómo se llamaba el personaje de este actor en «Aquí no hay quien viva»? → Juan Cuesta: En dos comedias de vecinos fui el presidente de la comunidad, y en la segunda me llamaba Enrique Pastor. ¿Quién soy? → José Luis Gil
- tv-shows-and-presenters-0: overlap like q-15267: Empecé de reportero en «Caiga quien caiga», fui Julián en «Camera Café» y en «¡Ahora caigo!» los concursantes caen por una trampilla. ¿Quién soy? → Arturo Valls: Soy valenciano, fui Julián en «Camera Café» y desde 2011 presento en Antena 3 «Ahora caigo», donde el suelo se abre si fallas. ¿Quién soy? → Arturo Valls
- tv-shows-and-presenters-9: overlap like q-1426: Estás viendo Eurovisión y un país anuncia «douze points» para una canción. ¿Cuántos puntos le está dando? → 12: Estás viendo las votaciones de Eurovisión: tras los 8 y los 10 puntos, llega la nota máxima. ¿Cuántos puntos son? → 12
- tv-shows-and-presenters-10: overlap like q-10035: Estás ante la tele en Nochevieja y, antes de las doce campanadas, suenan los cuartos. ¿Cuántos son? → 4: Somos cuatro toques dobles que suenan en el reloj de la Puerta del Sol justo antes de las doce, y muchos empiezan a comer uvas con nosotros por error. ¿Qué somos? → Los cuartos
- tv-shows-and-presenters-14: overlap like q-13281: Antes de «La Revuelta» en La 1, David Broncano presentaba un late night en Movistar Plus+. ¿Cómo se llamaba? → «La Resistencia»: Me crié en un pueblo de Jaén, presenté «La Resistencia» y desde 2024 hago «La Revuelta» en La 1, donde pregunto cuánto dinero tienes en el banco. ¿Quién soy? → David Broncano
