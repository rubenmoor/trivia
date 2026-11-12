# batch-58

Made by `qgen batch` on 2026-11-11 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): spanish-cinema, current-music, tv-series, pop-and-rock, flamenco-and-copla, sportspeople, regional-symbols, modern-literature, scientists-and-explorers, painting-and-architecture, rivers-and-mountains, classic-literature, team-and-traditional-sports, ancient-hispania, footballers-and-national-team, empire, 20th-century, tv-shows-and-presenters, bourbons-and-19th-century, comics-and-childrens-books, sayings, legends-and-superstitions, monuments, transition-and-democracy, protected-areas, radio-and-internet, wildlife
- Merged: 182 (q-17091…q-17272)
- Approved: 172
- Needs work: 10
- Dropped by the pipeline: 74
- Reviewed by: claude-opus-5-5
- Claude calls: 423, about $60.44 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-56, batch-57; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-56 | batch-57 | batch-58 |
|---|---|---:|---:|---:|
| source locale |  | en | de | es-ES |
| drafts |  | 309 | 299 | 256 |
| skipped slots |  | 141 | 187 | 230 |
| dropped |  | 70 | 67 | 74 |
| drop rate | ≤ 20.0 % | 22.7 % ✗ | 22.4 % ✗ | 28.9 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 20 | 14 | 16 |
| dropped: overlap |  | 49 | 51 | 52 |
| dropped: duplicate |  | 1 | 0 | 6 |
| dropped: fact-check wrong |  | 0 | 1 | 0 |
| merged |  | 239 | 232 | 182 |
| approved |  | 208 | 213 | 172 |
| needs_work |  | 31 | 19 | 10 |
| needs_work rate | ≤ 20.0 % | 13.0 % ✓ | 8.2 % ✓ | 5.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.7 % ✓ | 3.0 % ✓ | 1.6 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.4 % ✓ | 0.9 % ✓ | 1.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.5 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.5 % ✗ | 2.2 % ✗ | 2.2 % ✗ |
| needs_work: media | ≤ 10.0 % | 8.4 % ✓ | 4.3 % ✓ | 0.5 % ✓ |
| media: no pick in review 1 |  | 33 | 31 | 20 |
| media: recovered by research |  | 22 | 21 | 20 |
| media: no pick at record |  | 11 | 10 | 0 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 18.1 % ✓ | 18.7 % ✓ | 24.2 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 79.4 % ✓ | 65.0 % ✓ | 53.7 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.56 ✗ | 1.63 ✗ | 1.06 ✓ |
| approved 11–15 |  | 38 | 70 | 33 |
| top move | ≤ 25.0 % | 13.8 % ✓ | 17.2 % ✓ | 12.1 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 81.6 % | 83.6 % | 82.4 % |
| values stimulus |  | 6 | 3 | 4 |
| top clue | ≤ 60.0 % | 36.8 % ✓ | 40.9 % ✓ | 42.9 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 22.6 % ✓ | 22.4 % ✓ | 22.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 21.3 % ✓ | 18.5 % ✓ | 20.3 % ✓ |
| values lens |  | 11 | 9 | 10 |
| media share | 15.0 %–50.0 % | 18.4 % ✓ | 16.4 % ✓ | 17.6 % ✓ |
| mean fun | ≥ 3.40 | 3.51 ✓ | 3.37 ✗ | 3.36 ✗ |
| cost $ |  | $64.59 | $71.62 | $56.74 |
| $ per approved | ≤ $0.35 | $0.31 ✓ | $0.34 ✓ | $0.33 ✓ |
| calls |  | 462 | 467 | 363 |
| calls per approved |  | 2.22 | 2.19 | 2.11 |
| wall time h |  | 1.91 | 2.21 | 1.65 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 57 (0 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 5 (0 major), fact 4 (0 major), overlap 3 (0 major), media 3 (0 major), difficulty 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.70

Major findings on approved questions:

None.

## Needs work

- **q-17112** (comics-and-childrens-books) Gloria Fuertes, que adoraba las rimas, tituló un cuento «El dragón…». ¿Qué palabra viene después? → tragón: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-17114** (current-music) Amaia es de Pamplona, tocaba el piano sin parar y ganó en 2018 un concurso que volvía a la tele tras años sin emitirse. ¿Qué concurso? → Operación Triunfo: Overlaps q-13269, an approved question that says outright that Alfred "salió de Operación Triunfo 2017 y fue a Eurovisión 2018 junto a Amaia", so anyone who has seen it already knows this answer. The description has a second problem: «una casa llena de cámaras» describes the live-in format, and among the four options only Operación Triunfo has it, so the description rules out the other three before any hint.
- **q-17124** (empire) Don Quijote lo era, no pagaba ciertos impuestos y le parecía indigno trabajar con las manos. ¿Qué era un hidalgo? → Un noble de rango bajo: The description («veía gigantes donde solo había molinos») gives away the answer to the approved q-9924 («¿Qué creía que eran?» → Gigantes). Rewrite it to play on Don Quijote or nobility some other way, without the giants-and-windmills episode.
- **q-17125** (empire) Moctezuma gobernaba Tenochtitlan cuando llegó Hernán Cortés. ¿Qué ciudad se construyó después sobre sus ruinas? → Ciudad de México: Hint 2 («En ese país se habla español y se comen tacos») points straight to Mexico, and Ciudad de México is the only Mexican option, so hint 2 gives the answer away. Replace it with a vaguer hint, for example that the city is one of the biggest in the world or is very high above sea level, without naming the country or its food.
- **q-17139** (modern-literature) ¿Cuál de estas ciudades NO aparece en el título de ningún libro de Antonio Muñoz Molina? → París: Verificación de datos: uncertain. A search found no Muñoz Molina book titled with Paris. It did confirm 'Los misterios de Madrid' and 'Córdoba de los Omeyas'. 'El invierno en Lisboa' is well known. I did not check a full bibliography, so I can't rule out a Paris title.
- **q-17148** (monuments) Mira este edificio de Gaudí en Barcelona, que lleva más de 140 años en obras. ¿Para qué es? → Para ir a misa: Hint 2 («Sus torres terminan en cruces») is factually wrong: only the central Tower of Jesus Christ is topped by a cross. The other towers end in other finials (mitres, a star, fruit and symbol pinnacles). Replace it with an accurate hint, for example that the tallest tower, dedicated to Jesus, is crowned by a large cross. Verificación de datos: wrong. Hint 2 'Sus torres terminan en cruces' is inaccurate: only the central Tower of Jesus Christ (completed Feb 2026) ends in a cross. The other towers end in other finials (mitres, star, symbols).
- **q-17161** (pop-and-rock) Tenía una cinta enrollada dentro y dos caras, A y B; si la cinta se enredaba, la arreglabas con un boli. ¿Qué era? → El casete: The description gives the answer away. Read with only the four options, «rebobinado manual incluido» points to the cassette alone: of the four, only a tape gets rewound, and by hand with a pen. That rules out the vinyl, the CD and the floppy disk before any hint. Rewrite it to play on the retro-music theme without mentioning rewinding, tape or winding.
- **q-17163** (pop-and-rock) ¿En qué década nació en San Sebastián el grupo de heavy metal Ángeles del Infierno? → En los años 70: The answer can't be confirmed: sources disagree on when Ángeles del Infierno was founded. Some give 1978 in Lasarte-Oria, which is near San Sebastián rather than in it, and others such as English Wikipedia give 1980. The band also only took the name around 1982, so «los años 80» is defensible too. The question also rests on a minor date, which is only hard because it is obscure. Drop it or replace it with a fact about the band that sources agree on. Verificación de datos: uncertain. Sources differ on founding: 1978 (Lasarte-Oria, near San Sebastián) per some, 1980 per English Wikipedia/Apple Music; name Ángeles del Infierno adopted c. 1982. The 70s answer holds only if 1978 is used, and the hint 'finales de la década' depends on that.
- **q-17239** (sportspeople) Juan Carlos Navarro, «la Bomba», jugó toda su carrera en España en el mismo club. ¿En qué ciudad? → Barcelona: This repeats an approved question. q-11345 asks which city's basketball team won the Euroleague in 2003 and 2010 and names Juan Carlos Navarro, with the answer Barcelona. Seeing one of the two questions gives the other away. A rewrite can't fix this without turning it into a different question.
- **q-17242** (sportspeople) ¿Qué medalla ganó Blanca Fernández Ochoa, hermana de Paquito, en el eslalon de Albertville 1992? → La medalla de bronce: The fun fact says outright that Paquito won Spain's first Winter Olympic gold in Sapporo 1972, which is the whole answer to the approved q-11386 ('¿Quién ganó el primer oro olímpico de invierno de la historia de España?'). Replace the fun fact with another true fact about Blanca, for example that she competed in four Winter Olympics, and the question can pass.

## Question axes

- move: analogy 7, cause_effect 8, count 6, estimate 4, identify 18, made_of 10, name_concept 19, odd_one_out 9, origin 22, purpose 20, record 6, sequence 10, when 14, who 17, word_meaning 12
- stimulus: detail 2, none 150, photo 29, video 1
- clue: completion 2, direct 78, riddle 25, scenario 16, three_facts 61
- answer_kind: group 23, number 11, person 29, place 28, thing 41, time 15, word 35
- lens: body_senses 7, educational_media 22, everyday 13, history 37, language 27, nature 7, pop_culture 24, school 35, science_news 3, university 7

## Dropped by the pipeline

- 20th-century-3: overlap like q-1179: Te subes en Madrid a un tren llamado AVE, sigla de 'Alta Velocidad Española'. ¿Más o menos a qué velocidad máxima puede llevar pasajeros? → Unos 300 km/h: El AVE se estrenó en 1992 entre Madrid y Sevilla y corre a unos 300 km/h. ¿Qué tipo de transporte es? → Un tren
- 20th-century-14: overlap like q-14455: El famoso puente de diciembre empieza con el Día de la Constitución. ¿Qué día se celebra? → El 6 de diciembre: Estás de puente en diciembre y el primer festivo es el Día de la Constitución. ¿Qué día es? → El 6 de diciembre
- 20th-century-16: overlap like q-12426: «Me terminaron en 1929 en la Gran Vía de Madrid y con casi 90 metros fui el edificio más alto de España». ¿Qué soy? → El edificio Telefónica: Soy el edificio de Telefónica en la Gran Vía: en 1929, con 89 metros, fui el más alto de España y parezco rozar las nubes. ¿Qué tipo de edificio soy? → Un rascacielos
- ancient-hispania-0: overlap like q-2617: Who uses a small brush like this to free old objects from the ground? → Archaeologist: Excavamos con paletas y pinceles en Mérida, Itálica o Empúries para sacar a la luz casas romanas. ¿Quiénes somos? → Los arqueólogos
- ancient-hispania-5: overlap like q-0263: La Edad del Bronce se llama así por el bronce, que se hace mezclando cobre con otro metal. ¿Con cuál? → Estaño: Hace unos 4000 años, en la cultura de El Argar (Almería y Murcia), se mezclaba cobre con estaño para hacer hachas y puñales. ¿Qué época era? → La Edad del Bronce
- ancient-hispania-6: overlap like q-4540: You hunt wild animals and gather wild plants, and nobody on Earth has a farm yet. In which era are you living? → The Paleolithic: Vivo en cuevas como las de Atapuerca, no siembro nada ni tengo animales: cazo ciervos y busco frutos y raíces. ¿Quién soy? → Un cazador-recolector
- ancient-hispania-17: overlap like q-8627: Scientists give every species a two-part Latin name. What is the name of our own species, modern humans? → Homo sapiens: Llegó a la península hace unos 40 000 años, pintó los bisontes de Altamira y es la única especie humana que sigue viva. ¿Cuál es? → Homo sapiens
- bourbons-and-19th-century-15: overlap like q-14286: Goya pintó este perro directamente sobre la pared de una casa a las afueras de Madrid. ¿Cómo se llamaba esa casa? → La Quinta del Sordo: Goya pintó sus Pinturas negras entre 1819 y 1823, ya mayor y sordo, en su casa junto al Manzanares, y nunca las enseñó. ¿Sobre qué las pintó? → Sobre las paredes
- classic-literature-6: overlap like q-16223: Se cantan muy bajito, sirven para dormir a los bebés y una muy famosa empieza «Duérmete, niño». ¿Qué canciones son? → Nanas: Se canta bajito junto a la cuna, muchas empiezan con «Duérmete, niño» y Lorca recogió decenas por toda España. ¿Qué es una nana? → Una canción para dormir a un bebé
- classic-literature-11: overlap like q-9942: El 23 de abril, día de San Jorge, las calles se llenan de puestos y la gente se regala rosas y libros. ¿Dónde es típica esta costumbre? → En Cataluña: Ese día se regalan rosas y libros por Sant Jordi en Cataluña, hay cuentacuentos en los colegios y en Madrid se lee el Quijote en voz alta. ¿Qué día es? → El Día del Libro
- classic-literature-12: overlap like q-5186: Según un refrán muy conocido, Dios ayuda a alguien en especial. ¿A quién? → Al que madruga: Son frases cortas que pasan de abuelos a nietos, dan un consejo y a veces riman, como «A quien madruga, Dios le ayuda». ¿Cómo se llaman? → Los refranes
- current-music-4: overlap like q-14269: Estás en una boda y suena «Despechá», de Rosalía. ¿En qué década salió esa canción? → En los años 2020: ¿En qué verano sonaba por todas partes «Despechá», de Rosalía? → 2022
- empire-3: overlap like q-0354: Mira este cuadro famoso, 'Las Meninas', que está en el Museo del Prado de Madrid: ¿quién lo pintó? → Diego Velázquez: En este detalle de un famoso cuadro de Velázquez, el rey Felipe IV y su esposa aparecen reflejados en un espejo. ¿Qué cuadro es? → «Las meninas»
- empire-4: overlap like q-14422: Te pones «como un tomate» cuando te da vergüenza. Pero ¿de qué continente llegó el tomate a España? → De América: Mira este fruto. Los españoles lo trajeron a Europa en el siglo XVI. ¿De qué continente venía? → De América
- empire-17: overlap like q-12371: En la fachada de la Universidad de Salamanca hay una ranita de piedra que todos buscan. ¿Sobre qué está sentada? → Sobre una calavera: La fachada de la Universidad de Salamanca es del siglo XVI y esconde una rana sobre una calavera. Según la tradición, ¿qué le pasa al estudiante que la encuentra sin ayuda? → Aprobará sus exámenes
- flamenco-and-copla-1: overlap like q-7200: Escucha: con este instrumento, y no con acordeón, Guillermo Buitrago grabó canciones costeñas en los años 40. ¿Cuál es? → La guitarra: Escucha este instrumento: es el que toca Paco de Lucía en su rumba «Entre dos aguas». ¿Cuál es? → La guitarra
- footballers-and-national-team-7: overlap like q-5177: ¿Qué lleva siempre en la cara el cantante paisa Camilo como su sello personal? → El bigote: Es riojano, fue lateral del Athletic y ganó la Eurocopa 2024 como seleccionador. ¿Qué lleva siempre en la cara Luis de la Fuente? → Un bigote
- footballers-and-national-team-9: overlap like q-0849: Soy centrocampista española: en 2023 fui campeona del mundo con mi selección, me eligieron la mejor jugadora de ese Mundial y luego gané el Balón de Oro. ¿Quién soy? → Aitana Bonmatí: ¿Qué futbolista española ganó este trofeo tres años seguidos: 2023, 2024 y 2025? → Aitana Bonmatí
- footballers-and-national-team-14: duplicate like q-16476: Mira este detalle del penacho de plumas de quetzal que se atribuye a Moctezuma. ¿En qué ciudad está guardado hoy? → Viena: En este estadio España ganó la final de la Eurocopa 2008. ¿En qué ciudad está? → Viena
- legends-and-superstitions-2: overlap like empire-17: La fachada de la Universidad de Salamanca es del siglo XVI y esconde una rana sobre una calavera. Según la tradición, ¿qué le pasa al estudiante que la encuentra sin ayuda? → Aprobará sus exámenes: Está tallada sobre una calavera en la fachada de la Universidad de Salamanca y cuesta mucho verla. Según la tradición, ¿qué le pasa al estudiante que encuentra la rana? → Que aprobará los exámenes
- modern-literature-11: overlap like q-12288: El Marqués de Bradomín, «feo, católico y sentimental», protagoniza las cuatro «Sonatas». ¿Qué escritor lo creó? → Ramón María del Valle-Inclán: En las «Sonatas» de Valle-Inclán, el marqués de Bradomín se define como «feo, católico y sentimental». ¿Qué clase de personaje es? → Un donjuán
- monuments-5: overlap like q-1674: Tenía claustro, iglesia y biblioteca, y allí se copiaban libros a mano. ¿Quiénes vivían en una abadía medieval? → Monjes: Mira este edificio en la montaña de Montserrat, en Cataluña. ¿Quiénes viven y rezan en él desde hace siglos? → Monjes
- monuments-6: overlap like q-16185: El palacio de La Granja de San Ildefonso, cerca de Segovia, se construyó imitando a Versalles y tiene fuentes enormes. ¿Quién pasaba allí los veranos? → Los reyes y su corte: Mira este palacio de La Granja, en la sierra de Segovia, con sus jardines llenos de fuentes. ¿Para qué lo usaban sobre todo los reyes? → Para pasar el verano
- monuments-7: overlap like q-3791: I'm a ribbed seashell. Hikers walking the Way of Saint James to Santiago de Compostela hang me on their backpacks. What am I? → Scallop shell: Los peregrinos del Camino de Santiago la llevan colgada como símbolo, y en Galicia también se come. ¿Qué concha es? → La vieira
- monuments-8: duplicate like q-16334: Este detalle es de un cuadro enorme que muestra el entierro de un caballero ante muchos nobles. ¿Quién lo pintó? → El Greco: Este cuadro, «El Expolio», cuelga en la sacristía de la catedral de Toledo desde hace más de 400 años. ¿Quién lo pintó? → El Greco
- monuments-13: overlap like q-1861: Se hace con pedazos de baldosa o cerámica rota, se pega como mosaico y Gaudí lo usó mucho. ¿Cómo se llama esta técnica? → Trencadís: Mira esta figura de Gaudí en la escalinata del Park Güell. ¿Cómo se llama la técnica de trocitos de cerámica rota que la cubre? → Trencadís
- painting-and-architecture-0: overlap like q-11235: Dalí compró el castillo de Púbol para Gala en 1969. ¿Qué animales de patas larguísimas decoran su jardín? → Elefantes: ¿Cómo se llamaba la mujer rusa que fue esposa y musa de Salvador Dalí, y a la que él pintó una y otra vez? → Gala
- painting-and-architecture-7: overlap like q-1362: Soy la gran obra de Antoni Gaudí en Barcelona y empezaron a construirme en 1882. ¿Qué soy? → La Sagrada Familia: Mira esta fachada llena de figuras de piedra que cuentan el nacimiento de Jesús. ¿Qué arquitecto la diseñó? → Antoni Gaudí
- pop-and-rock-12: overlap like q-12259: Este cantante de Linares representó a España en Eurovisión en 1966 y 1967 y triunfó con «Mi gran noche». ¿Quién es? → Raphael: Me llaman «el Niño de Linares» y canto «Qué pasará, qué misterio habrá, puede ser mi gran noche». ¿Quién soy? → Raphael
- pop-and-rock-15: overlap like q-14349: Ana Belén y Víctor Manuel le cantaron a un monumento de Madrid: «Ahí está, ahí está…». ¿Qué rey lo mandó construir? → Carlos III: Soy madrileña, actriz y cantante, y con Víctor Manuel, mi marido, canté «La puerta de Alcalá». ¿Quién soy? → Ana Belén
- protected-areas-1: overlap like q-7851: Mira la foto: esta neblina cubre el páramo casi todos los días. ¿Qué les da a plantas como los frailejones? → Agua: En el macizo de Anaga, en Tenerife, llueve poco, pero los árboles del bosque gotean casi todo el día. ¿De dónde sacan el agua? → De la niebla
- radio-and-internet-7: overlap like q-1809: ¿Qué tiene que lograr un canal de YouTube para recibir esta placa plateada? → Llegar a 100 000 suscriptores: Tu canal llega a 100 000 suscriptores y YouTube te manda el botón de plata. ¿Con cuántos suscriptores llega el de oro? → 1 millón
- ancient-hispania-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Fue la etapa justo antes de la llegada de los romanos a la península: celtas e íberos forjaban armas con un metal más duro que el bronce. ¿Cómo se llama? → La Edad del Hierro
- ancient-hispania-15: overlap like q-15338: Pasas por la Sierra de Atapuerca (Burgos) y ves a decenas de arqueólogos excavando, como cada año. ¿En qué mes estás, casi seguro? → En julio: Está en Burgos, es Patrimonio de la Humanidad y allí se descubrió el «Homo antecessor». ¿Qué yacimiento es? → Atapuerca
- bourbons-and-19th-century-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En el Retiro de Madrid hay una gran estatua de Alfonso XII junto al estanque. ¿Qué reinado vino justo después del suyo? → El de Alfonso XIII
- comics-and-childrens-books-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Es una palabra muy española que nació del nombre de una antigua revista. ¿Qué es un tebeo? → Un cómic
- current-music-8: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En 2023, los Grammy Latino salieron por primera vez de Estados Unidos y se celebraron en una ciudad andaluza junto al Guadalquivir. ¿En cuál? → Sevilla
- empire-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Soy un dulce pequeño, redondo y amarillo, típico de Ávila, y se me vende en cajitas. ¿Qué soy? → Las yemas de Santa Teresa
- monuments-3: overlap like q-16193: Mira la foto: es una de las fuentes del Paseo del Prado de Madrid. ¿Qué se celebra en ella? → Los títulos del Atlético de Madrid: Mira la estatua de esta fuente de Madrid. ¿Qué dios romano va subido en el carro? → Neptuno
- pop-and-rock-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La medalla de oro es al deportista que gana como ¿qué es al cantante que vende muchísimos discos? → El disco de oro
- protected-areas-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Soy un trozo de mar en el sur de El Hierro, junto a La Restinga, y los buceadores me adoran. En 2011 nació un volcán bajo mis aguas. ¿Qué soy? → El Mar de las Calmas
- regional-symbols-15: hard fail: correct 5, unambiguous 5, no_giveaway 1, no_overlap 5: Mira esta bandera. ¿De qué tierra española es? → León
- rivers-and-mountains-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Mira la foto: estos campos inundados del delta del Ebro son famosos en toda España. ¿Qué alimento sale de ellos? → El arroz
- rivers-and-mountains-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: ¿Qué ave rapaz de hombros blancos caza conejos, anida en Doñana y solo vive en España y Portugal? → El águila imperial ibérica
- scientists-and-explorers-7: duplicate like q-15226: Mira el cuadro: Goya pintó a la gente luchando contra los soldados de Napoleón el 2 de mayo de 1808. ¿En qué ciudad pasó? → Madrid: Este es el edificio del Museo Nacional de Ciencias Naturales. ¿En qué ciudad está? → Madrid
- scientists-and-explorers-10: overlap like q-0295: ¿Cuántas montañas hay en el mundo que superan los 8000 metros de altura? → 14: En 2010, Edurne Pasaban completó la colección de las 14 montañas más altas del planeta. ¿Cómo las llaman los alpinistas? → Los ochomiles
- spanish-cinema-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Soy una casa donde viven niños que no tienen padres. En una película de J. A. Bayona, Belén Rueda vuelve a mí. ¿Qué soy? → Un orfanato
- sportspeople-13: overlap like sportspeople-16: Soy de El Puerto de Santa María, me apodan «el Lobo» y llegué a ser número 1 del ranking mundial de pádel. ¿Quién soy? → Juan Lebrón: ¿Qué jugador madrileño de pádel fue número 1 del mundo formando pareja con el gaditano Juan Lebrón? → Alejandro Galán
- team-and-traditional-sports-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Jugamos en pista cubierta con un balón que bota poco y porterías pequeñas, y fuimos campeones del mundo en 2000 y 2004. ¿Qué selección española somos? → La de fútbol sala
- team-and-traditional-sports-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Quiénes compiten por ganar la Copa Davis de tenis? → Equipos de países
- transition-and-democracy-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El partido Vox toma su nombre de una palabra latina, la de la expresión «vox populi». ¿Qué significa «vox»? → Voz
- tv-shows-and-presenters-2: hard fail: correct 5, unambiguous 5, no_giveaway 1, no_overlap 5: Soy el canal de la tele pública española que solo emite deporte, todo el día: Juegos Olímpicos, ciclismo, balonmano… ¿Cómo me llamo? → Teledeporte
- rivers-and-mountains-10: duplicate like q-9890: Mira este acueducto de Segovia. ¿Qué pueblo lo construyó? → Los romanos: Mira la foto: este puente de Córdoba cruza el Guadalquivir frente a la Mezquita. ¿Quiénes lo construyeron primero? → Los romanos
- rivers-and-mountains-12: overlap like q-14400: Son montañas de caliza entre Asturias, Cantabria y León, y en ellas se alza el Naranjo de Bulnes. ¿Cómo se llaman? → Picos de Europa: En asturiano es el Picu Urriellu; en castellano lleva el nombre de un árbol frutal por su color al atardecer. ¿Cuál? → Naranjo
- rivers-and-mountains-13: overlap like q-9986: El oso pardo de la cordillera Cantábrica come muchísimas bellotas y castañas en otoño, engorda y busca una cueva. ¿Para qué? → Para dormir buena parte del invierno: Vive en la cordillera Cantábrica, pasa el invierno dormido en su guarida y sale en el escudo de Madrid junto a un madroño. ¿Qué animal es? → El oso pardo
- scientists-and-explorers-9: overlap like q-12449: Karlos Arguiñano es a la cocina como Jesús Calleja es a… → la aventura: Pones «Desafío Extremo» en Cuatro y ves a un leonés escalando montañas y bajando a volcanes. ¿Quién es? → Jesús Calleja
- scientists-and-explorers-16: overlap like q-12257: Nació en 1958 en Cataluña, tiene forma de bola y su inventor, Enric Bernat, le puso un palo. ¿Para qué? → Para que los niños no se mancharan las manos: ¿Qué golosina creó en 1958 el barcelonés Enric Bernat, pensada para que los niños no se mancharan las manos? → El Chupa Chups
- scientists-and-explorers-17: overlap like q-2021: Estás viendo los dibujos de neuronas más famosos de la historia, hechos a mano por un Nobel de Medicina. ¿Quién los hizo? → Santiago Ramón y Cajal: «Nací en 1852 en Navarra, dibujé miles de neuronas y demostré que no están pegadas: entre ellas hay un hueco, la sinapsis. Gané el Nobel en 1906». ¿Quién soy? → Santiago Ramón y Cajal
- spanish-cinema-5: overlap like q-10730: Earth, Wind & Fire's famous dance hit starts with “Do you remember the 21st night of…” which month? → September: Suena varias veces en «Robot Dreams» (2023), de Pablo Berger: un éxito disco de Earth, Wind & Fire con el que el perro y el robot patinan en Central Park. ¿Qué canción es? → «September»
- spanish-cinema-17: overlap like q-2042: Son dos torres gemelas, se inclinan 15 grados una hacia la otra y las llaman 'Puerta de Europa'. ¿En qué ciudad están? → Madrid: Mira la foto: el final de «El día de la bestia» (1995), de Álex de la Iglesia, transcurre en lo alto de estas torres inclinadas. ¿En qué ciudad están? → Madrid
- sportspeople-11: overlap like q-12479: Mira la foto: Marc Gasol y Serge Ibaka ganaron en 2019 el anillo de la NBA con el equipo de esta ciudad. ¿Cuál es? → Toronto: Mira la foto: este pívot barcelonés fue Mejor Defensor de la NBA en 2013 y campeón con los Toronto Raptors en 2019. ¿Quién es? → Marc Gasol
- sportspeople-16: overlap like sportspeople-13: ¿Qué jugador madrileño de pádel fue número 1 del mundo formando pareja con el gaditano Juan Lebrón? → Alejandro Galán: Soy de El Puerto de Santa María, me apodan «el Lobo» y llegué a ser número 1 del ranking mundial de pádel. ¿Quién soy? → Juan Lebrón
- team-and-traditional-sports-7: duplicate like q-13473: Mira estos espetos de sardinas asados en la arena. ¿De qué ciudad son típicos? → Málaga: Mira la foto: el Unicaja de baloncesto juega en la ciudad de esta catedral. ¿Qué ciudad es? → Málaga
- transition-and-democracy-5: overlap like q-14457: Nació en 1989, su símbolo fue durante años una gaviota y lo presidieron Aznar y Rajoy. ¿Qué significan sus siglas PP? → Partido Popular: Mariano Rajoy fue presidente del Gobierno de España de 2011 a 2018. ¿De qué partido era? → El Partido Popular
- transition-and-democracy-7: overlap like q-10137: Estoy en Madrid, y dentro de mí 350 personas elegidas debaten y votan las leyes. Dos leones de bronce guardan mi puerta. ¿Qué soy? → El Congreso de los Diputados: En este edificio de Madrid juró la Constitución Felipe VI al ser proclamado rey en 2014. ¿Qué edificio es? → El Congreso de los Diputados
- transition-and-democracy-9: overlap like q-14303: ¿De qué ciudad es Hombres G, el grupo de «Devuélveme a mi chica»? → Madrid: Somos cuatro chicos de Madrid que triunfamos en los 80 con «Venecia» y «Devuélveme a mi chica», y nuestro cantante es David Summers. ¿Quiénes somos? → Hombres G
- transition-and-democracy-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: El tricornio, el sombrero de charol de la Guardia Civil, se llama así por un sombrero antiguo. ¿Cuántos picos tenía? → 3
- transition-and-democracy-17: overlap like q-12519: Las reformas borbónicas crearon las intendencias, subieron impuestos y expulsaron a los jesuitas en 1767. ¿De qué país venía la familia real que las impulsó? → Francia: La familia real de Felipe VI llegó al trono español en 1700 con Felipe V, nieto del Rey Sol. ¿De qué país venía? → Francia
- tv-shows-and-presenters-0: overlap like q-13281: Antes de «La Revuelta» en La 1, David Broncano presentaba un late night en Movistar Plus+. ¿Cómo se llamaba? → «La Resistencia»: Soy humorista, nací en un pueblo de Jaén y desde 2024 presento «La Revuelta» por las noches en La 1. ¿Quién soy? → David Broncano
- tv-shows-and-presenters-1: overlap like q-11419: ¿Qué humorista malagueño se hizo famoso en 1994 en «Genio y figura» con expresiones como «¡Jarl!» o «condemor»? → Chiquito de la Calzada: Me movía a saltitos, contaba chistes larguísimos y gritaba «¡Pecador de la pradera!» y «¡No puedorrr!». ¿Quién soy? → Chiquito de la Calzada
- tv-shows-and-presenters-9: overlap like q-10035: Estás ante la tele en Nochevieja y, antes de las doce campanadas, suenan los cuartos. ¿Cuántos son? → 4: Estás viendo las campanadas: baja la bola y, antes de la primera uva, suenan los cuartos. ¿Cuántos cuartos suenan? → 4
- wildlife-0: duplicate like q-13381: Mira la foto de esta tienda. ¿De dónde viene casi todo lo que se vende aquí? → Del mar: Mira estos boquerones en vinagre, una tapa de bar muy típica de España. ¿De dónde sale este pescado? → Del mar
- wildlife-10: overlap like q-0029: ¿Cómo se llama la cría de la rana? → Renacuajo: La gallina es al pollito como la rana es al… → Renacuajo
- wildlife-12: overlap like q-9941: Vas vestido de blanco y, cuando suena el chupinazo a mediodía del 6 de julio, te atas al cuello un pañuelo rojo. ¿Dónde estás? → En Pamplona: Sus corredores visten de blanco con pañuelo rojo, empieza el 6 de julio con el chupinazo y tiene el encierro de toros más famoso del mundo. ¿Qué fiesta es? → San Fermín
