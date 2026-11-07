# batch-51

Made by `qgen batch` on 2026-11-07 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: mexico
- Language: Spanish (Latin America)
- Subcategories (29): legends, states-and-capitals, contemporary-cinema, pop-and-rock, indigenous-words, regional-fiestas, boxing, indigenous-peoples, transport, crafts-and-dress, national-team, lucha-libre, golden-age-cinema, scientists-and-inventors, mexica, mariachi-and-ranchera, childrens-songs, traditional-dances, other-cultures, school-and-services, sweets-and-bread, traditional-games, ingredients, conquest-and-colony, animals, home-and-street, drinks, tv-shows-and-hosts, regional-dishes
- Merged: 227 (q-15447…q-15673)
- Approved: 207
- Needs work: 20
- Dropped by the pipeline: 101
- Reviewed by: claude-opus-5-5
- Claude calls: 512, about $72.09 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-49, batch-50; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-49 | batch-50 | batch-51 |
|---|---|---:|---:|---:|
| source locale |  | de | es-ES | es |
| drafts |  | 349 | 320 | 328 |
| skipped slots |  | 137 | 166 | 194 |
| dropped |  | 80 | 88 | 101 |
| drop rate | ≤ 20.0 % | 22.9 % ✗ | 27.5 % ✗ | 30.8 % ✗ |
| dropped: hard fail correct |  | 1 | 4 | 3 |
| dropped: hard fail unambiguous |  | 1 | 1 | 2 |
| dropped: hard fail no_giveaway |  | 21 | 17 | 14 |
| dropped: overlap |  | 55 | 66 | 76 |
| dropped: duplicate |  | 2 | 1 | 4 |
| dropped: fact-check wrong |  | 1 | 0 | 2 |
| merged |  | 269 | 232 | 227 |
| approved |  | 251 | 214 | 207 |
| needs_work |  | 18 | 18 | 20 |
| needs_work rate | ≤ 20.0 % | 6.7 % ✓ | 7.8 % ✓ | 8.8 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.1 % ✓ | 0.9 % ✓ | 2.2 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.2 % ✓ | 1.3 % ✓ | 0.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.5 % ✗ | 1.3 % ✗ | 1.8 % ✗ |
| needs_work: media | ≤ 10.0 % | 1.9 % ✓ | 4.3 % ✓ | 4.4 % ✓ |
| media: no pick in review 1 |  | 41 | 30 | 39 |
| media: recovered by research |  | 37 | 23 | 32 |
| media: no pick at record |  | 4 | 8 | 7 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 17.5 % ✓ | 21.9 % ✗ | 25.6 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 74.1 % ✓ | 55.8 % ✓ | 50.5 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.76 ✗ | 0.53 ✓ | 1.00 ✓ |
| approved 11–15 |  | 55 | 49 | 48 |
| top move | ≤ 25.0 % | 14.1 % ✓ | 16.4 % ✓ | 13.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 82.2 % | 81.5 % | 85.0 % |
| values stimulus |  | 4 | 3 | 4 |
| top clue | ≤ 60.0 % | 42.8 % ✓ | 45.7 % ✓ | 37.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 30.9 % ✓ | 20.3 % ✓ | 22.0 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.4 % ✓ | 20.3 % ✓ | 18.1 % ✓ |
| values lens |  | 11 | 10 | 10 |
| media share | 15.0 %–50.0 % | 17.8 % ✓ | 18.5 % ✓ | 15.0 % ✗ |
| mean fun | ≥ 3.40 | 3.50 ✓ | 3.46 ✓ | 3.41 ✓ |
| cost $ |  | $83.13 | $71.78 | $68.24 |
| $ per approved | ≤ $0.35 | $0.33 ✓ | $0.34 ✓ | $0.33 ✓ |
| calls |  | 533 | 468 | 452 |
| calls per approved |  | 2.12 | 2.19 | 2.18 |
| wall time h |  | 2.37 | 2.24 | 2.13 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 9 (0 major), fact 1 (0 major), overlap 1 (1 major), media 5 (1 major), difficulty 5 (0 major), other 2 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 5 of 60 (8 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.85

Major findings on approved questions:

None.

## Needs work

- **q-15455** (boxing) Suena la campana y los boxeadores profesionales se van a su esquina a descansar. ¿Cuánto dura ese descanso? → 1 minuto: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-15465** (childrens-songs) En este estado del sureste hace tanto calor que muchas familias duermen en hamaca, se habla mucho maya y está Chichén Itzá. ¿Cuál es? → Yucatán: None of the image candidates shows a hammock or anything from Yucatán: they show laundry, curtains, a selfie, airport workers, a seed catalogue and a crowd of children. No new search is allowed, so the media slot needs a new search, for example "Yucatan hammock" or "hammock Mexico house". The question text itself is acceptable. No se encontró una imagen adecuada para esta pregunta.
- **q-15482** (drinks) Viene en lata, su mascota es Pancho Pantera y se prepara en un vaso frío. Su nombre junta «choco» con una palabra en inglés. ¿Qué significa? → Leche: The description and hint 1 give the answer away: among Polvo, Fuerza, Dulce and Leche, only milk is something you have or drink for breakfast, so «El desayuno favorito…» and «Es algo que muchos niños toman en el desayuno» rule out every wrong option. Hint 2 («milkshake») also translates the word outright. The description should play on the brand or panther theme without mentioning breakfast. Hint 1 should be something vague, such as the brand's age or its can. Hint 2 must not contain the English word.
- **q-15492** (home-and-street) Por tu calle se escucha una grabación: «Se compran colchones, tambores, refrigeradores…». ¿Quién viene pasando? → El que compra fierro viejo: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-15506** (ingredients) Mira la foto de esta granada china. Al abrir su cáscara, ¿qué parte de la fruta se come? → Las semillas con su pulpa: No adequate essential image: candidate 1 is the right fruit but shows it cut open with the seeds and pulp visible, which gives the answer away; candidates 2–6 are unrelated (river boats, cider, a donut). A new search isn't allowed here, so this needs a closed, whole granada china photo (e.g. 'Passiflora ligularis fruit') or a crop of the left half of candidate 1. No se encontró una imagen adecuada para esta pregunta.
- **q-15507** (ingredients) Las entomatadas son tortillas dobladas con queso fresco y crema. ¿Con qué salsa se bañan? → Salsa de jitomate: The question text gives the answer away: the dish's name 'entomatadas' already contains 'tomate', so asking which salsa it is bathed in answers itself. The text also says the same thing twice: the name tells you the salsa, then the question asks for it. Rework it so the dish's name isn't the clue, for example by describing the dish and asking for its name, with enfrijoladas, enmoladas and enchiladas as the wrong options.
- **q-15521** (mariachi-and-ranchera) Mira la foto: así se visten muchas niñas el 20 de noviembre. ¿Cómo se llaman las cintas de balas que llevan cruzadas en el pecho? → Cananas: None of the candidates shows what the essential image needs: a girl or woman in an Adelita costume with crossed bandoliers. A new search isn't allowed, so the question needs a real Adelita or 20 de noviembre parade photo (e.g. "Adelita costume parade" or "soldadera costume Mexico"), or the wording must stop relying on "Mira la foto". No se encontró una imagen adecuada para esta pregunta.
- **q-15528** (mexica) Hablaba náhuatl y maya, aprendí español y fui la intérprete de Hernán Cortés. ¿Quién soy? → La Malinche: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-1923, PD-US-expired).
- **q-15532** (mexica) «Tlapalería» viene de la palabra náhuatl «tlapalli». ¿Qué significa «tlapalli»? → Color: Hint 2 gives the answer away: saying the Mexica used «tlapalli» for dyes made from plants and insects tells players the word means colour, and none of the wrong options (Fierro, Clavo, Madera) could fit. It is also stronger than hint 3. Make hint 2 vaguer, for example about how the Mexica used the thing the word names in codices or textiles without mentioning dyes, and keep the strongest hint for hint 3.
- **q-15536** (mexica) Con las plumas de esta ave se hizo el famoso penacho que hoy está en un museo de Viena. ¿A qué tlatoani se le atribuye? → Moctezuma: Overlaps approved q-10434, which shows a 500-year-old Mexica piece of green quetzal feathers and asks what kind of object it is (penacho). This question says outright that the famous penacho in Vienna is made of quetzal feathers, so whichever one a player sees first gives away the other. The two can't stay in the pool together unless this one asks about Moctezuma without the penacho.
- **q-15556** (pop-and-rock) Estás en el Tianguis del Chopo entre chamarras de cuero y discos de El Tri. ¿Cómo se llamaba a los jóvenes rockeros de barrio de los ochenta? → Chavos banda: Hint 2 gives the answer away: it rules out Pachucos and Jipitecas by decade, which leaves only Chavos banda and Fresas, and fresas are obviously not barrio rockers. Replace hint 2 with a vaguer clue, for example about the barrios or the sound of 1980s Mexico City rock, that doesn't rule out options.
- **q-15571** (regional-fiestas) En la feria lanzas unas piezas de plástico para que queden ensartadas en el cuello de una botella y ganar un premio. ¿Cómo se llama el juego? → Los aros: No adequate image: candidates 1 and 2 show carnival shooting galleries with toy rifles, which is the wrong option 'El tiro al blanco'. Candidates 3 and 4 are an old magazine masthead and a newspaper scan that have nothing to do with the question. A new search for the ring-toss game is needed (e.g. 'ring toss bottles'). No se encontró una imagen adecuada para esta pregunta.
- **q-15575** (regional-fiestas) Cada 28 de octubre, miles de personas visitan a San Judas Tadeo en el templo de San Hipólito. ¿Para qué casos le rezan? → Para las causas difíciles y desesperadas: Hint 2 ("Lo buscan cuando ya no saben a quién más pedirle") restates the answer: someone you turn to when nobody else can help is the patron of desperate causes, so it gives the answer away before hint 3. Hint 2 should be a vaguer clue, for example about the saint's green robe or the medallion he wears, and should not hint at desperation or last resorts.
- **q-15601** (national-team) En la Copa Oro W 2024, el Tri femenil le ganó 2-0 a Estados Unidos en California. ¿En qué año había sido su victoria anterior ante ellas? → 2010: The fun fact says the 2024 win was in San Diego, but the 2-0 group-stage match (26 February 2024) was played in Carson, California, at Dignity Health Sports Park. Change the fun fact to name Carson (or just say 'California'). Separately, the rater flagged the question as an obscure-date question (the year of the 2010 Cancún qualifier), which most players can't work out. The developer may want to rethink it. Verificación de datos: wrong. The answer 2010 is right, but the fun fact puts the 2024 match in San Diego. It was played in Carson, California (Dignity Health Sports Park) on Feb 26, 2024.
- **q-15627** (traditional-games) Se dice señalando a cada niño con el dedo, empieza con «De tin marín, de do pingüé» y sigue con «cúcara, mácara». ¿Qué son esas palabras? → Palabras inventadas sin significado: Overlaps q-7380, which asks what the «De tin marín» rhyme is for. Here the description ('decidir quién la trae') and hint 1 ('Se usan para escoger quién la trae') state that answer outright, so seeing this question gives q-7380 away. Either drop the purpose from the description and hint 1 or drop this question.
- **q-15629** (transport) El Tren Ligero de la CDMX, con su estación Estadio Azteca, empezó a funcionar el mismo año del segundo Mundial en México. ¿Qué año fue? → 1986: This duplicates approved q-12587 (same bundle). That question asks the year of the Argentina–West Germany final at the Estadio Azteca, which is 1986. This one is really the same question: the year of Mexico's second World Cup, with the Tren Ligero only as a wrapper. Hint 3 even uses the same clue, Argentina and Maradona. Drop it, or rewrite it around a Tren Ligero fact that doesn't depend on the World Cup year.
- **q-15647** (states-and-capitals) Mira el estado resaltado en el mapa: aquí se celebra el Festival Internacional del Globo, con cientos de globos aerostáticos. ¿Qué estado es? → Guanajuato: The essential map has no usable candidate. None of the six shows Mexico with Guanajuato highlighted: they are UK stewardship signs, plus maps of Serbia/Kosovo, Kenya, Bhutan and Russia. No new search is allowed, so the map has to be sourced another way, for example 'Guanajuato in Mexico (location map scheme).svg' from Commons. No se encontró una imagen adecuada para esta pregunta.
- **q-15650** (sweets-and-bread) Mira de cerca esta botana que venden en bolsitas en la tienda y en los puestos. ¿Cómo se llama? → Cacahuates enchilados: None of the candidates can serve as the essential image. The question asks players to identify cacahuates enchilados from a close-up, but no candidate shows a clean close-up of them. No new search is allowed, so the question needs a new image source, or it should become an illustrative-image question. No se encontró una imagen adecuada para esta pregunta.
- **q-15654** (traditional-dances) Llego a la fiesta vestida como princesa, cumplo una edad muy especial y abro el baile con un vals. ¿Quién soy? → La quinceañera: This question overlaps with approved q-11680 (chambelanes). Its fun fact says "otro con los chambelanes", which gives away q-11680's answer. q-11680's own text ("bailan el vals con la quinceañera") also hands this question its answer. To keep it, the fun fact must drop the chambelanes and use another XV años detail, for example the "última muñeca" or the change of shoes.
- **q-15662** (tv-shows-and-hosts) Nací en Tijuana, conduje «Atínale al precio» y en 2000 estrené en Televisa «¿Quién quiere ser millonario?». ¿Quién soy? → Marco Antonio Regil: The text is fine, but no media candidate fits. The sheet shows a 1960s hearing, a cathedral painting, an office building, a rock band, a praying mantis and a circuit board. None of them shows a TV studio or a game-show set, and no new search is allowed. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 3, cause_effect 12, count 5, estimate 7, identify 30, made_of 11, name_concept 25, odd_one_out 12, origin 24, purpose 20, record 4, sequence 7, when 15, who 26, word_meaning 26
- stimulus: detail 6, map_outline 2, none 193, photo 26
- clue: completion 10, direct 85, riddle 30, scenario 27, three_facts 75
- answer_kind: group 30, number 13, person 36, place 33, thing 50, time 17, word 48
- lens: body_senses 11, educational_media 24, everyday 35, history 38, language 41, nature 9, pop_culture 37, school 18, science_news 9, university 5

## Dropped by the pipeline

- animals-0: duplicate like q-10361: Mira esta verdura. Su nombre viene de la lengua de un pueblo mesoamericano. ¿De cuál? → Los mexicas: Mira el escudo de México: según la leyenda, ¿qué pueblo vio esta señal y ahí fundó su ciudad? → Los mexicas
- animals-1: overlap like q-11668: Es de la Ciudad de México, viste de amarillo con azul y juega el Clásico Joven contra el Cruz Azul. ¿Qué ave es el apodo del América? → Las Águilas: En el futbol mexicano, cuando el narrador grita «¡Gol de las Águilas!», ¿qué equipo anotó? → El América
- animals-3: overlap like q-13610: En la charrería, el deporte nacional de México, ¿qué animales participan en las suertes? → Caballos y reses: La charrería, deporte nacional de México, nació del trabajo diario de un grupo de la época colonial. ¿De cuál? → Los vaqueros de las haciendas
- animals-12: overlap like q-1933: Este pájaro de Australia imita cámaras y motosierras, y la cola del macho parece una lira. ¿Para qué imita sonidos el macho? → Para conquistar a las hembras: Mira la foto: en las costas de México, el macho de esta ave marina infla una bolsa roja en el cuello. ¿A quiénes quiere impresionar? → A las hembras
- childrens-songs-0: overlap like q-12711: Despiertas temprano y en la tele está Chabelo con «En Familia». ¿Qué día de la semana es? → Domingo: Chabelo despedía su programa «En Familia con Chabelo» hasta la semana siguiente. ¿Qué día de la semana volvía a salir en la tele? → El domingo
- childrens-songs-2: overlap like q-11453: En el tocadiscos de los abuelos suena un disco con «La patita» y «El ratón vaquero». ¿Quién los canta? → Cri-Cri: Empecé cantando en la radio mexicana en 1934 y luego llegué a los discos; canto «El ratón vaquero» y «Los cochinitos dormilones». ¿Quién soy? → Cri-Cri
- childrens-songs-6: overlap like q-10298: Mira estos tamales. ¿De qué está hecha su masa? → De maíz: «Tortillitas para mamá» se juega dando palmadas con las manitas del bebé, como se palmean las tortillas para el comal. ¿De qué se hace la masa de esas tortillas? → De maíz
- childrens-songs-17: overlap like q-12630: En México, ¿qué día de mayo se celebra el Día de las Madres? → 10: En México, el Día del Niño es el 30 de abril. ¿Qué festejo de la escuela llega apenas diez días después? → El Día de las Madres
- conquest-and-colony-1: overlap like q-12500: Si te sale el muñequito de la rosca el 6 de enero, te toca invitar tamales el Día de la Candelaria. ¿Cuántos días después es? → 27: Mira esta rosca de Reyes. El 2 de febrero, Día de la Candelaria, ¿quién tiene que invitar los tamales? → Quien encontró el muñequito
- conquest-and-colony-9: overlap like q-2177: Soy la catedral del Zócalo de Ciudad de México, levantada sobre las ruinas de Tenochtitlan. ¿Qué conquistador tomó esa ciudad? → Hernán Cortés: Mira esta catedral, una de las más grandes de América. ¿Sobre las ruinas de qué ciudad se construyó? → Tenochtitlan
- conquest-and-colony-10: overlap like q-10212: Tras su encuentro con Cortés en 1519, Moctezuma acabó prisionero de los españoles. ¿Quién gobernó a los mexicas justo después de él? → Cuitláhuac: Fui hermano de Moctezuma. Encabecé a los mexicas cuando sacaron a los españoles de Tenochtitlan en la Noche Triste, y goberné solo unos 80 días. ¿Quién soy? → Cuitláhuac
- conquest-and-colony-12: overlap like q-10283: Las mujeres purépechas de Ocumicho, Michoacán, moldean coloridos diablitos de barro. Según uno de los relatos del pueblo, ¿por qué empezaron a hacerlos? → Para que el diablo tuviera dónde vivir y dejara en paz al pueblo: Vivían en lo que hoy es Michoacán, su capital fue Tzintzuntzan y los mexicas nunca lograron conquistarlos. ¿Qué pueblo era? → Los purépechas
- conquest-and-colony-14: fact-check wrong: Sor Juana appears on the 200-peso bill, not the 100-peso bill (the 100-peso bill shows Nezahualcóyotl). The 17th-century answer is correct.: Sor Juana Inés de la Cruz, la poeta y monja novohispana que hoy sale en el billete de 100 pesos, ¿en qué siglo vivió? → El siglo XVII
- conquest-and-colony-16: overlap like q-5532: The Aztecs drank it bitter and frothy, often spiced with chili, and kings drank it from golden cups. What was it made from? → Cacao beans: Mira esta bebida espumosa: el tlatoani Moctezuma tomaba tazas y tazas de ella. ¿De qué semilla se hace? → Del cacao
- contemporary-cinema-11: overlap like q-14527: Soy un huevo valiente de una película animada mexicana y mi mejor amigo es un tocino llamado Willy. ¿Quién soy? → Toto: Mira la foto: en «Otra película de huevos y un pollo», el amigo que siempre acompaña a Toto es un pedazo de esto. ¿Qué es? → Tocino
- crafts-and-dress-2: overlap like q-10472: Esta cerámica vidriada, pintada a mano en azul sobre blanco, es típica de Puebla y Tlaxcala. ¿Cómo se llama? → Talavera: Esta cerámica de azul cobalto sobre fondo blanco tiene denominación de origen. ¿En qué ciudad mexicana nació? → Puebla
- crafts-and-dress-4: overlap like q-13588: ¿Quién es esta pintora mexicana, famosa por su uniceja y las flores en el cabello? → Frida Kahlo: Me peinaba con trenzas adornadas con listones y flores, mis cejas se juntaban y pinté muchísimos autorretratos. ¿Quién soy? → Frida Kahlo
- crafts-and-dress-6: overlap like q-11490: Estás frente a un cuadro huichol hecho con estambre de colores. ¿Sobre qué material pegaron los hilos? → Cera de abeja: Es un cuadro huichol de estambre pegado con cera sobre una tabla, y su nombre alude a un portal o espejo hacia los dioses. ¿Cómo se llama? → Nierika
- drinks-0: overlap like q-7444: Mira la foto: estas astillas se le echan a la aguapanela y al arroz con leche. ¿De qué parte de la planta salen? → De la corteza de un árbol: Para el té de canela se hierven rajitas en agua. ¿De qué parte de un árbol salen esas rajitas? → De la corteza
- drinks-9: overlap like q-10304: Es de piedra volcánica, tiene tres patas y se usa con una piedra alargada llamada metlapil o mano. ¿Para qué sirve el metate? → Para moler maíz: Es de piedra volcánica, plana e inclinada, sobre tres patas, y se muele tallando con un rodillo de piedra. Así se hace el chocolate tradicional. ¿Cómo se llama? → Metate
- golden-age-cinema-1: overlap like q-12690: En un mapa de México tapas con la mano Chihuahua, el estado más grande. ¿Qué parte del país tapaste, más o menos? → Una octava parte: Es una exclamación de sorpresa muy de película mexicana: «¡Ay, …!». Lleva el nombre del estado más grande de México, cuya capital se llama igual. ¿Cuál? → Chihuahua
- home-and-street-0: overlap like q-12535: ¿Cuál de estas cosas NO hace la abuela con el Vick VapoRub? → Dártelo a tomar con agua para la panza: En los memes, el Vaporub de la mamá mexicana lo cura todo. ¿Para cuál de estas cosas NO sirve de verdad? → Para endulzar el atole
- home-and-street-13: overlap like q-13698: Este es el Multifamiliar Miguel Alemán, de 1949, el primer gran conjunto de departamentos de México. ¿Qué arquitecto lo diseñó? → Mario Pani: El Multifamiliar Miguel Alemán, de 1949, fue de las primeras de México y Tlatelolco es de las más grandes. ¿Qué es una unidad habitacional? → Un conjunto de edificios de departamentos
- indigenous-peoples-0: overlap like q-10474: Este tocado se usa en la Danza del Venado de los yaquis. ¿De qué estado es esta danza? → Sonora: Este danzante lleva una cabeza de venado y sonajas de capullos de mariposa en las piernas. ¿De qué pueblo viene su danza? → Un yaqui
- indigenous-peoples-4: overlap like q-11490: Estás frente a un cuadro huichol hecho con estambre de colores. ¿Sobre qué material pegaron los hilos? → Cera de abeja: Vivo en la sierra entre Jalisco y Nayarit, hago cuadros de estambre pegado con cera y cada año camino hasta Wirikuta, en San Luis Potosí. ¿Quién soy? → Un huichol
- indigenous-peoples-7: overlap like q-13573: Los mixtecos pintaron códices como este. ¿En qué estado está la mayor parte de su tierra, la Mixteca? → Oaxaca: Los mixtecos pintaban la historia de sus reyes en largas tiras de piel de venado que se doblaban como acordeón. ¿Cómo se llaman esos libros? → Códices
- indigenous-peoples-17: duplicate like q-14630: Este bordado de flores de colores es de Zinacantán, en los Altos de Chiapas. ¿Qué pueblo indígena lo borda? → Los tsotsiles: Mira esta iglesia de San Juan Chamula, en Chiapas, donde no hay bancas y el piso se cubre de hojas de pino. ¿Qué pueblo indígena vive ahí? → Los tsotsiles
- indigenous-words-17: overlap like q-2600: In the film “Black Panther: Wakanda Forever”, Black Panther is to Wakanda as Namor is to… → Talokan: Gobierno un reino bajo el mar inspirado en los mayas, tengo alitas en los tobillos y mi pueblo me llama K'uk'ulkan. ¿Quién soy? → Namor
- ingredients-5: overlap like q-4039: Pico de gallo is a fresh salsa of chopped tomato, onion, chili and cilantro. Which country does it come from? → Mexico: Mira este jitomate. Si lo picas con cebolla, chile y cilantro, ¿qué salsa mexicana preparas? → El pico de gallo
- ingredients-16: overlap like q-10476: La parte mexicana de esta península se reparte entre tres estados. ¿Cuáles son? → Yucatán, Campeche y Quintana Roo: El chile habanero de la Península de Yucatán tiene denominación de origen. ¿Cuál de estos estados NO está dentro de esa zona? → Tabasco
- ingredients-17: overlap like q-10263: Son las semillas de la calabaza: se tuestan con sal y limón, se venden en bolsitas y se muelen para el pipián. ¿Cómo se llaman? → Pepitas: Soy una salsa espesa, verde o roja; me hacen sobre todo con pepitas de calabaza molidas y baño pollo o carne. ¿Qué soy? → El pipián
- legends-0: overlap like q-0483: Según la leyenda, ¿a quién busca la Llorona cuando anda de noche, llorando cerca de los ríos? → A sus hijos: ¿Qué espanto se oye por las noches cerca de los ríos gritando «¡Ay, mis hijos!»? → La Llorona
- legends-11: overlap like q-8034: Cuentan en el campo que hay brujas que de día son señoras del pueblo y de noche se vuelven un ave que chilla sobre los techos. ¿Qué ave? → Una lechuza: Al anochecer salgo volando por los cerros como una bola de fuego, y al amanecer vuelvo a ser una señora más del pueblo. ¿Qué soy? → Una bruja
- legends-13: overlap like q-0589: ¿Qué significa en náhuatl, la lengua de los aztecas, el nombre del volcán Popocatépetl? → Cerro que humea: Sobre los nombres de los volcanes de la leyenda del guerrero y la princesa, ¿cuál de estos datos NO es cierto? → Iztaccíhuatl significa «princesa enamorada»
- lucha-libre-4: overlap like q-11461: Estás viendo una vieja película en la que El Santo hace equipo con su rival más famoso, nacido en Nuevo León. ¿Quién es? → Blue Demon: Esta máscara azul con bordes plateados alrededor de los ojos la hizo famosa un luchador legendario. ¿Quién? → Blue Demon
- lucha-libre-8: overlap like q-11584: En la lucha libre mexicana, ¿qué es un luchador «rudo»? → El villano que hace trampa: Hace trampa, le jala la máscara al rival y se pelea con el réferi. Por eso el público lo cuenta entre… ¿cuáles? → Los rudos
- mariachi-and-ranchera-17: overlap like q-5100: Llevan traje de charro con botones plateados y sombrero gigante, tocan trompetas, violines y guitarras, y en Colombia los contratan para dar serenatas. ¿Cómo se llama ese grupo? → Mariachi: La canción ranchera habla del campo y de amores que duelen, y lleva gritos de «¡ay, ay, ay!». ¿Qué conjunto la acompaña tradicionalmente? → El mariachi
- mexica-1: overlap like q-10322: Los mexicas salieron de Aztlán y caminaron años buscando un águila sobre un nopal devorando una serpiente. ¿Qué les indicaba esa señal? → Dónde fundar su ciudad: Según la leyenda, los mexicas fundaron su ciudad donde vieron un águila parada sobre un nopal. ¿Qué animal tenía en el pico? → Una serpiente
- mexica-3: overlap like q-10419: Si comes de esta salsa y te arde la boca, ¿qué ingrediente tiene la culpa? → El chile: Mira la foto: los mexicas ya lo echaban en casi todas sus comidas. ¿Qué es? → El chile
- mexica-14: overlap like q-12514: Mira esta enorme escultura mexica del Museo Nacional de Antropología. ¿Cómo se llama? → La Piedra del Sol: Mira esta enorme piedra tallada del Museo Nacional de Antropología. ¿Qué pueblo la hizo? → Los aztecas
- mexica-15: overlap like q-10169: Se vende por las mañanas en las esquinas de la Ciudad de México, va con atole y su nombre recuerda a la hembra del guajolote. ¿De qué está hecha? → Bolillo con tamal adentro: En un desayuno de domingo, el pan va con el café como el tamal va con el… → Atole
- mexica-17: overlap like q-2477: People in Mexico have made this flat, round bread from the plant in the photo for thousands of years. What is it? → Tortillas: Los mexicas la llamaban tlaxcalli: es redonda y plana, se hace con masa de maíz y se calienta en el comal. ¿Qué es? → La tortilla
- national-team-14: overlap like q-5877: Maple the moose, Zayu the jaguar and Clutch the bald eagle are the mascots of which men's soccer World Cup? → 2026: Maple es una de las tres mascotas del Mundial 2026: representa a Canadá y cuida la portería. ¿Qué animal es? → Un alce
- national-team-15: overlap like q-1349: Adidas es a las tres rayas como Nike es a… → un trazo curvo: El jersey del Tri lo fabrica Adidas, famosa por las rayas en hombros y mangas. ¿Cuántas rayas son? → 3
- other-cultures-0: overlap like q-10249: ¿Quién fue la primera mujer indígena mexicana nominada al Óscar a Mejor Actriz, por la película «Roma»? → Yalitza Aparicio: Nací en Tlaxiaco, Oaxaca, y estudié para maestra de preescolar. En mi primera película hablé mixteco y me nominaron al Óscar. ¿Quién soy? → Yalitza Aparicio
- other-cultures-2: overlap like q-10230: En muchas ofrendas se sirve la bebida favorita del difunto, como el pulque. ¿De qué planta sale el pulque? → Del maguey: En lo alto de un cerro de Tepoztlán, Morelos, está el Tepozteco, templo de Tepoztécatl, dios del pulque. ¿De qué planta se saca esa bebida? → Del maguey
- other-cultures-13: overlap like q-13550: Mira esta cabeza olmeca: algunas pesan más de 20 toneladas. ¿De qué está hecha? → De roca volcánica: Las cabezas colosales olmecas pesan como varios elefantes, llevan casco y se movieron sin ruedas. ¿De dónde sacaron su piedra? → De un volcán
- pop-and-rock-0: overlap like q-11552: «Canté “Pelo suelto” con la melena alborotada y años después también “Todos me miran”.» ¿Quién soy? → Gloria Trevi: «Nací en Monterrey, mi primer gran éxito fue “Doctor Psiquiatra” y años después canté “El recuento de los daños”.» ¿Quién soy? → Gloria Trevi
- pop-and-rock-1: overlap like q-11551: «Formé parte de RBD y la balada “Sálvame” se volvió mi gran momento: la canto casi sola.» ¿Quién soy? → Anahí: «De niña actué en “Chiquilladas”, en “Rebelde” fui la fresa Mía Colucci y me casé con un gobernador de Chiapas.» ¿Quién soy? → Anahí
- pop-and-rock-14: overlap like q-14723: ¿Qué banda mexicana convirtió «Las batallas en el desierto» en la canción «Las batallas», de su disco «Re» (1994)? → Café Tacvba: Pones «Re», el disco de Café Tacvba con «La ingrata» y «El baile y el salón». ¿En qué año salió? → 1994
- regional-dishes-0: overlap like q-8060: La avena de las panaderías colombianas es espesa y fría. ¿Qué tipo de alimento es la avena? → Un cereal: Este pozole blanco se prepara desde tiempos prehispánicos con granos grandes y reventados. ¿A qué grupo de alimentos pertenece ese grano? → Cereales
- regional-dishes-1: duplicate like q-10361: Mira esta verdura. Su nombre viene de la lengua de un pueblo mesoamericano. ¿De cuál? → Los mexicas: Esta bebida espumosa de cacao se llamaba «xocolatl». ¿De qué pueblo viene esa palabra? → Los mexicas
- regional-dishes-4: overlap like q-10239: Se vende en rajitas enrolladas, huele dulce y nunca falta en el café de olla ni en el arroz con leche. ¿Qué es? → La canela: En esta olla de ponche flotan frutas, pero ¿qué especia en forma de palito le da su aroma? → Canela
- regional-dishes-16: overlap like q-10263: Son las semillas de la calabaza: se tuestan con sal y limón, se venden en bolsitas y se muelen para el pipián. ¿Cómo se llaman? → Pepitas: Soy chiquita y verde por dentro, me venden tostada con sal y chile en bolsitas, y molida soy la base del pipián. ¿Qué soy? → La pepita de calabaza
- regional-fiestas-11: overlap like q-12499: El 6 de enero es a los Reyes Magos como el 12 de diciembre es a… → La Virgen de Guadalupe: Las Mañanitas se cantan en los cumpleaños o el día del santo. Por eso, la noche del 11 al 12 de diciembre, millones se las cantan a… → La Virgen de Guadalupe
- regional-fiestas-13: overlap like q-7139: En Colombia muchos comen natas en el pan, y con azúcar se hace un dulce con ellas. ¿Qué son las natas? → La capa que se forma encima de la leche: Son gorditas dulces, se cuecen en comal y se venden en ferias y afuera de las iglesias. Llevan la capa que se forma al hervir la leche. ¿Cómo se llama? → Nata
- regional-fiestas-14: overlap like q-12605: Mira este teclado: en el pasito duranguense hace los bajos que en una banda sinaloense toca otro instrumento. ¿Cuál? → La tuba: La banda sinaloense nació en Sinaloa y toca con clarinetes, trompetas, trombones y tambora. ¿Qué enorme instrumento de metal lleva los bajos? → La tuba
- regional-fiestas-17: overlap like q-11553: Mira la foto: ¿cómo se llama este traje típico que se luce al bailar el jarabe tapatío? → China poblana: Al final del jarabe tapatío, el charro avienta su sombrero al piso. ¿Quién baila sobre el ala del sombrero? → La china poblana
- boxing-5: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Estás en la Arena México viendo box olímpico y Agustín Zaragoza gana para México el bronce en peso medio. ¿En qué año? → 1968
- boxing-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ves en la tele la «Pelea del Milenio»: el puertorriqueño Félix «Tito» Trinidad le gana por decisión a Óscar de la Hoya. ¿En qué año? → 1999
- boxing-17: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: La empresa mexicana Zanfer fue fundada por Fernando Beltrán y sus eventos salen en Box Azteca. ¿A qué se dedica? → A organizar y promover funciones de box
- childrens-songs-13: overlap like q-13604: Las enmoladas son tortillas rellenas de pollo y bañadas en mole. ¿Qué semillitas se les espolvorean encima tradicionalmente? → Ajonjolí: El programa infantil «Plaza Sésamo» lleva el nombre de una semilla. ¿Cómo le decimos en México al sésamo? → Ajonjolí
- contemporary-cinema-3: overlap like legends-0: ¿Qué espanto se oye por las noches cerca de los ríos gritando «¡Ay, mis hijos!»? → La Llorona: Soy un fantasma de una leyenda de la Colonia. Me visto de blanco, mi lamento se oye de noche y en «Kilómetro 31» (2006) me aparezco en una carretera. ¿Quién soy? → La Llorona
- contemporary-cinema-5: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Mira la foto: este actor fue «El Cochiloco» en «El infierno» y el general Medrano en la película de James Bond «Quantum of Solace». ¿Quién es? → Joaquín Cosío
- crafts-and-dress-11: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: ¿Cómo se juega con estas bolitas de vidrio? → Se lanzan con el dedo para pegarle a otras
- crafts-and-dress-14: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En San Miguel de Allende a estos muñecos gigantes de cartonería les dicen mojigangas. ¿Para qué se usan? → Para bailar en desfiles y fiestas del pueblo
- home-and-street-1: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Tiene dos palas que se aprietan como pinza, muchas veces es amarillo o verde y no falta en la cocina para los tacos. ¿Cómo se llama? → El exprimidor
- legends-9: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 4: Es un volcán activo vigilado por cámaras día y noche, y en sus videos mucha gente jura haber visto ovnis entrando al cráter. ¿Cuál es? → El Popocatépetl
- mariachi-and-ranchera-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Es de Pepe Guízar, la toca cualquier mariachi y dice «tienes el alma de provinciana, hueles a limpio, a rosa temprana». ¿Cómo se llama? → Guadalajara
- national-team-1: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Con la Copa Oro que ganó en 2025, ¿cuántas Copas Oro tiene México en total? → 10
- school-and-services-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Este aparato está afuera de muchas casas. ¿Para qué sirve? → Para medir la electricidad que gastas
- school-and-services-17: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En México, una boda de iglesia no cuenta ante la ley sin este trámite. ¿Dónde te casas para tener acta de matrimonio? → En el Registro Civil
- states-and-capitals-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El acueducto de Morelia, con sus 253 arcos de cantera, se terminó en 1788. ¿En qué época de la historia de México se construyó? → El virreinato de la Nueva España
- sweets-and-bread-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Es de la marca Lucas y trae una paleta que mojas en el polvito enchilado que viene en el mismo envase. ¿Cómo se llama? → Lucas Muecas
- traditional-games-1: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Estás en un mercado de Michoacán y ves trastecitos de barro: ollitas, cazuelitas y jarritos del tamaño de un dedo. ¿Qué son? → Juguetes para jugar a la comidita
- traditional-games-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Soy una carta de la Lotería: un hombre con sarape y un puñal. Cuando me cantan dicen «¿por qué le corres, cobarde?». ¿Quién soy? → El Valiente
- traditional-games-11: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Se grita justo antes de echar una carrera y se oye en patios de todo México. ¿Quién es el «huevo podrido»? → El que llega al último
- transport-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La estación Bellas Artes del Metro de la CDMX abrió en 1970. ¿Cuántas líneas del Metro pasan hoy por ella? → 2
- transport-12: fact-check wrong: The hint and fun fact say the airport's logo has a mammoth. The first mammoth logo (April 2021) was cancelled. The current logo is an AIFA wordmark with airplane wings, mammoth tusks and General Felipe Ángeles's mustache. The answer is right.: Al hacer una gran obra en Santa Lucía, Estado de México, aparecieron restos de cientos de mamuts. ¿Qué se estaba construyendo? → El Aeropuerto Felipe Ángeles
- school-and-services-3: overlap like q-7265: Suena el timbre a media mañana y todos salen corriendo al patio a jugar. ¿Qué momento de la jornada es? → El recreo: En la escuela, ¿en qué momento del día abres tu lonchera para comer? → En el recreo
- scientists-and-inventors-2: overlap like q-11438: Las Chokis son galletas redondas de la marca Gamesa. ¿Qué traen encima y adentro? → Chispas de chocolate: Gamesa es una marca mexicana que hace las Marías, las Emperador y las Arcoíris. ¿Qué tipo de producto vende? → Galletas
- scientists-and-inventors-11: overlap like q-12570: Mira la foto: en el equinoccio de primavera, por la escalinata de esta pirámide maya parece bajar una serpiente. ¿De qué está hecho su cuerpo? → De luz y sombra: En Chichén Itzá, la sombra de una serpiente de luz parece bajar por la pirámide de Kukulcán. ¿Cuándo se ve mejor? → En los equinoccios de primavera y otoño
- scientists-and-inventors-17: overlap like q-10461: En noviembre de 1985 subí a bordo del transbordador Atlantis y me convertí en el primer mexicano en viajar al espacio. ¿Quién soy? → Rodolfo Neri Vela: Si un astronauta se arma un taco en el espacio, se lo debe a un mexicano que llevó tortillas al transbordador en 1985. ¿Quién fue? → Rodolfo Neri Vela
- states-and-capitals-4: duplicate like q-10474: Este tocado se usa en la Danza del Venado de los yaquis. ¿De qué estado es esta danza? → Sonora: Mira el estado resaltado en el mapa: su capital tiene el apodo de «la Ciudad del Sol». ¿Qué estado es? → Sonora
- states-and-capitals-10: overlap like q-14586: Un chile poblano relleno, bañado en salsa de nuez y adornado con granada y perejil, es un chile en… → Nogada: Es verde oscuro, se rellena para hacer chiles en nogada y, ya seco, se llama chile ancho. ¿Qué chile es? → El chile poblano
- sweets-and-bread-1: overlap like q-14514: La noche del 5 de enero, los niños mexicanos dejan sus zapatos. Antes de dormir, ¿qué suelen meter dentro? → Su carta para los Reyes: La noche del 5 de enero, muchos niños en México escriben su carta a los Reyes Magos y dejan algo junto al árbol para que ahí les pongan los regalos. ¿Qué dejan? → Sus zapatos
- sweets-and-bread-2: overlap like q-10239: Se vende en rajitas enrolladas, huele dulce y nunca falta en el café de olla ni en el arroz con leche. ¿Qué es? → La canela: Mira este pan de panadería enrollado en espiral. ¿Qué especia lleva entre sus capas? → Canela
- sweets-and-bread-3: overlap like q-0665: Nochebuena es a Navidad como Halloween (31 de octubre) es a… → Día de Todos los Santos: Caigo el 1 de noviembre; en México me dedican a los niños que ya se fueron, y al día siguiente llegan los Fieles Difuntos. ¿Qué día soy? → Día de Todos los Santos
- sweets-and-bread-6: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Mira esta cajeta de Celaya. Su nombre viene de los recipientes en que se vendía antiguamente. ¿Cómo eran? → Cajitas de madera
- sweets-and-bread-10: overlap like conquest-and-colony-1: Mira esta rosca de Reyes. El 2 de febrero, Día de la Candelaria, ¿quién tiene que invitar los tamales? → Quien encontró el muñequito: Viene escondido dentro de la rosca de reyes, es chiquito y de plástico, y a quien le sale le toca invitar los tamales el 2 de febrero. ¿Qué es? → Un muñequito
- sweets-and-bread-13: overlap like q-13511: Las calaveritas literarias se escriben en noviembre, son chistosas y cuentan cómo la Muerte se lleva a alguien. ¿En qué forma se escriben? → Versos que riman: Las calaveritas literarias del Día de Muertos no son de azúcar. ¿De qué están hechas? → De versos que riman
- sweets-and-bread-15: overlap like q-10381: Esta es leche quemada, un dulce de leche de vaca cocida con azúcar. Su prima, la cajeta tradicional de Celaya, se hace con leche de… → Cabra: Estas son glorias, dulces de Linares, Nuevo León, envueltos en celofán rojo. ¿Con qué leche se hacen? → Leche de cabra
- sweets-and-bread-16: overlap like q-11485: Al salir de un bautizo en México, los niños le gritan al padrino «¡bolo, bolo!». ¿Qué avienta el padrino al aire? → Monedas: Al salir de la iglesia, el padrino avienta monedas y dulces, y los niños gritan «¡Bolo, padrino!». ¿Qué se acaba de celebrar? → Un bautizo
- traditional-dances-4: overlap like q-13656: ¿Cómo se llaman los danzantes de penacho que tocan una mandolina hecha con el caparazón de un armadillo? → Concheros: Los danzantes concheros tocan la concha, un instrumento de cuerdas parecido a la mandolina. Su caja de resonancia se hacía tradicionalmente con… ¿qué? → El caparazón de un armadillo
- traditional-dances-7: overlap like q-10474: Este tocado se usa en la Danza del Venado de los yaquis. ¿De qué estado es esta danza? → Sonora: Los tenabaris son capullos de mariposa nocturna rellenos de piedritas que se enrollan en las piernas y suenan en la danza del Venado. ¿De qué estado son típicos? → Sonora
- traditional-dances-16: overlap like q-10320: Estos danzantes giran colgados de un poste altísimo. ¿De qué ciudad de México son los más famosos? → Papantla: El trampolín es al clavadista como el palo altísimo de Papantla es al… → Volador
- traditional-games-5: overlap like q-7115: Estás jugando ponchados en el recreo y tienes el balón en la mano. ¿Para qué lo lanzas? → Para sacar a un rival: Completa la regla del patio: en los quemados, a un niño le gritan «¡quemado!» cuando… → La pelota le pega
- traditional-games-16: overlap like q-10223: Se hace girar sobre la mesa, tiene seis caras y en ellas dice cosas como 'toma todo' o 'todos ponen'. ¿Cómo se llama? → Pirinola: Se gira con dos dedos, tiene seis caras con órdenes como «pon uno» y «todos ponen», y la mejor dice «toma todo». ¿Qué es? → La pirinola
- traditional-games-17: overlap like q-7956: Uno cuenta contra la pared y los demás se esconden. Para salvarte gritas «¡un, dos, tres por mí!». ¿A dónde debes llegar? → Al sitio donde contó el que busca: Juegas escondidas, llegas a la base antes que el que busca y gritas «¡un, dos, tres por mí!». ¿A quién salvas? → Solo a ti
- transport-13: overlap like conquest-and-colony-9: Mira esta catedral, una de las más grandes de América. ¿Sobre las ruinas de qué ciudad se construyó? → Tenochtitlan: Desde 2021 la estación Zócalo del Metro tiene un segundo nombre, el de la ciudad mexica que estaba justo ahí. ¿Cuál? → Tenochtitlan
- tv-shows-and-hosts-11: overlap like q-11579: Ves un partido en TV Azteca y Christian Martinoli le dice «Doctor» a su compañero, exdelantero de México en el Mundial de 1994. ¿Quién es? → Luis García: ¿Qué narrador de futbol de TV Azteca es famoso por sus burlas, apodos ingeniosos y referencias a películas en cada partido? → Christian Martinoli
