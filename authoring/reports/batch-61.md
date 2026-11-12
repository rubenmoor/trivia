# batch-61

Made by `qgen batch` on 2026-11-12 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: mexico
- Language: Spanish (Latin America)
- Subcategories (29): indigenous-words, pop-and-rock, contemporary-cinema, revolution, other-sports, telenovelas, pre-hispanic-gods, other-cultures, tv-shows-and-hosts, traditional-dances, writers-and-poets, indigenous-peoples, liga-mx, states-and-capitals, regional-mexican, 20th-century, landscapes, legends, painters-and-muralists, animals, mexica, maya, cities-and-towns, landmarks, transport, mariachi-and-ranchera, conquest-and-colony, golden-age-cinema, national-team
- Merged: 170 (q-17640…q-17809)
- Approved: 160
- Needs work: 10
- Dropped by the pipeline: 102
- Reviewed by: claude-opus-5-5
- Claude calls: 407, about $59.59 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-59, batch-60; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-59 | batch-60 | batch-61 |
|---|---|---:|---:|---:|
| source locale |  | es | en | es |
| drafts |  | 321 | 255 | 272 |
| skipped slots |  | 201 | 195 | 250 |
| dropped |  | 123 | 86 | 102 |
| drop rate | ≤ 20.0 % | 38.3 % ✗ | 33.7 % ✗ | 37.5 % ✗ |
| dropped: hard fail correct |  | 1 | 0 | 3 |
| dropped: hard fail unambiguous |  | 0 | 1 | 2 |
| dropped: hard fail no_giveaway |  | 12 | 20 | 17 |
| dropped: overlap |  | 108 | 64 | 78 |
| dropped: duplicate |  | 2 | 1 | 4 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 198 | 169 | 170 |
| approved |  | 177 | 152 | 160 |
| needs_work |  | 21 | 17 | 10 |
| needs_work rate | ≤ 20.0 % | 10.6 % ✓ | 10.1 % ✓ | 5.9 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.5 % ✓ | 2.4 % ✓ | 2.4 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 1.2 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 3.5 % ✗ | 1.2 % ✗ | 2.9 % ✗ |
| needs_work: media | ≤ 10.0 % | 5.6 % ✓ | 5.9 % ✓ | 1.2 % ✓ |
| media: no pick in review 1 |  | 39 | 25 | 16 |
| media: recovered by research |  | 31 | 18 | 15 |
| media: no pick at record |  | 8 | 8 | 1 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.5 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 36.4 % ✗ | 26.3 % ✗ | 32.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 40.9 % ✗ | 60.7 % ✓ | 41.3 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.43 ✓ | 1.97 ✗ | 1.44 ✓ |
| approved 11–15 |  | 30 | 24 | 28 |
| top move | ≤ 25.0 % | 16.7 % ✓ | 14.8 % ✓ | 14.7 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 77.8 % | 79.9 % | 85.3 % |
| values stimulus |  | 4 | 4 | 4 |
| top clue | ≤ 60.0 % | 44.9 % ✓ | 40.2 % ✓ | 32.9 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 23.2 % ✓ | 24.3 % ✓ | 25.9 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.2 % ✓ | 18.9 % ✓ | 18.2 % ✓ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 22.2 % ✓ | 20.1 % ✓ | 14.7 % ✗ |
| mean fun | ≥ 3.40 | 3.38 ✗ | 3.51 ✓ | 3.33 ✗ |
| cost $ |  | $65.86 | $51.84 | $55.68 |
| $ per approved | ≤ $0.35 | $0.37 ✗ | $0.34 ✓ | $0.35 ✓ |
| calls |  | 422 | 362 | 347 |
| calls per approved |  | 2.38 | 2.38 | 2.17 |
| wall time h |  | 1.95 | 1.90 | 1.76 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 1 of 4 (25 %)
- Problems by kind: giveaway 8 (1 major), fact 3 (0 major), ambiguity 1 (0 major), overlap 3 (0 major), media 6 (1 major), difficulty 3 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.9; ≥ 3 on 3 of 60 (5 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.91

Major findings on approved questions:

None.

## Needs work

- **q-17645** (20th-century) Nací en 1990, organizaba las elecciones federales y muchos todavía le dicen a su credencial para votar con mi nombre. ¿Quién soy? → El IFE: The description ("la tarjetita de plástico que todos sacan de la cartera en el banco y en la tiendita") describes the IFE voter card, the answer's defining trait. Read with just the four options, it rules out the SAT, INEGI and SEP before the question is even heard. Rewrite it to joke about elections or bureaucracy without mentioning the ID card.
- **q-17655** (conquest-and-colony) En la Nueva España, la gente se clasificaba en castas según el origen de sus padres. ¿Cuál de estos nombres NO era una casta? → Tlatoani: Hint 2 gives the answer away: "es un cargo" is true only of Tlatoani, so anyone who knows Mestizo and Mulato are mixes of parents can solve it from hint 2 alone. Rewrite hint 2 to be vaguer, for example saying the odd word comes from before the Spanish arrived, without saying it is a title or office.
- **q-17657** (conquest-and-colony) El penacho de Moctezuma, que hoy está en un museo de Viena, es enorme. ¿Cuánto mide aproximadamente de ancho? → Casi 2 metros: The facts are right: the penacho is about 1.75 m wide, and it has hundreds of quetzal feathers and is too fragile to travel. The problem is the question text. It says the penacho 'hoy está en un museo de Viena', and that is exactly the answer to q-16476, which asks for its city. Anyone who sees this question gets q-16476 for free. Dropping the Vienna clause (e.g. 'El penacho de Moctezuma es enorme. ¿Cuánto mide aproximadamente de ancho?') removes the overlap.
- **q-17665** (contemporary-cinema) Escribí mis novelas en El Cairo y gané el Nobel de Literatura en 1988. En 1993, Arturo Ripstein llevó mi «Principio y fin» a la Ciudad de México. ¿Quién soy? → Naguib Mahfouz: This overlaps too much with approved q-12526, which asks about «El callejón de los milagros» and names "el egipcio Naguib Mahfouz" as the novelist that Mexican cinema adapted. A player who has seen q-12526 gets this "Who am I?" right away, since this one asks for the Egyptian Nobel winner adapted by a Mexican director. The facts check out, and candidate 4 would be a fine image.
- **q-17671** (indigenous-peoples) Los kikapúes llegaron desde los Grandes Lagos y viven en El Nacimiento, Coahuila. ¿Para qué les dio tierras México en el siglo XIX? → Para defender la frontera de ataques apaches: La imagen elegida tiene una licencia no adecuada (pd-no-reason: public domain without a template).
- **q-17705** (other-cultures) Son de barro, tienen unos 2000 años y muestran casas con techos altos, fiestas y juegos de pelota. ¿Para qué se hacían las maquetas de Nayarit? → Como ofrenda en tumbas de tiro: This overlaps too much with approved q-10310 ("perros de Colima: ¿para qué se hacían?" → "Para acompañar a los muertos en sus tumbas"). Both ask what West Mexican shaft-tomb ceramics were made for, the answer is the same, and hint 2 even brings up the little dogs. Anyone who has seen one question can answer the other.
- **q-17709** (other-cultures) Completa: el nombre de Huémac, el último gran rey de Tula según las leyendas, significa en náhuatl «…». → Mano grande: Hint 1 gives the answer away. It says the name "is not a god's name but describes his body", and all three wrong answers are god names (Espejo humeante = Tezcatlipoca, Serpiente de nubes = Mixcóatl, Colibrí zurdo = Huitzilopochtli). "Mano grande" is the only option about a body, so hint 1 settles it. Hint 1 should become a vague hint that doesn't rule out any option, for example one about the Toltec era or the legend of Tula's fall. The distractors could also include a non-divine, body-related name.
- **q-17717** (pop-and-rock) Maite Perroni fue Lupita en «Rebelde» y cantó en RBD. ¿Cómo estaba formado ese grupo? → Tres chicas y tres chicos: Hint 2 ("Uno de los chicos era Poncho, que en la telenovela hacía de Miguel") gives away approved q-11622, which asks for the nickname of Alfonso Herrera, who played Miguel in «Rebelde» (answer: Poncho). Replace hint 2 with one that doesn't name Poncho/Miguel, e.g. one that names one of the girls, Anahí or Dulce María, without giving the count.
- **q-17743** (landscapes) Mira el estado marcado en el mapa. ¿Qué estado es? → Baja California Sur: The essential image must be a map of Mexico with Baja California Sur highlighted, but every candidate is a fish, a moth or a beach photo, and no new search is allowed. Use a Wikimedia locator map such as "Baja California Sur in Mexico (location map scheme).svg" and check that it has no state names on it. The description's "al final… ya no hay carretera" also points to the tip of the peninsula, which rules out Baja California, Sonora and Sinaloa. No se encontró una imagen adecuada para esta pregunta.
- **q-17749** (maya) Eran blancos, de piedra cubierta de cal y elevados sobre el suelo de la selva. ¿Qué eran los sacbés mayas? → Caminos: This overlaps approved q-10291, in the same "Los mayas" subcategory. Its answer is that "sak be" means "camino blanco", so a player who has seen it already knows that sacbés were roads. Both questions hinge on the meaning of the same word, so one gives the other away.

## Question axes

- move: analogy 2, cause_effect 7, count 1, estimate 9, identify 25, made_of 7, name_concept 22, odd_one_out 14, origin 14, purpose 18, record 5, sequence 3, when 6, who 22, word_meaning 15
- stimulus: detail 7, map_outline 2, none 145, photo 16
- clue: completion 7, direct 56, riddle 30, scenario 22, three_facts 55
- answer_kind: group 24, number 10, person 30, place 23, thing 44, time 9, word 30
- lens: body_senses 4, educational_media 16, everyday 29, history 22, language 31, nature 11, pop_culture 31, school 13, science_news 5, university 8

## Dropped by the pipeline

- 20th-century-4: overlap like q-12716: Siendo secretario de Educación, el poeta Jaime Torres Bodet impulsó los libros de texto gratuitos. ¿En qué año se creó la comisión que los hace? → 1959: En las escuelas de México, la SEP reparte cada año unos libros muy famosos. Completa su nombre: «Libros de Texto…» → Gratuitos
- animals-3: overlap like q-11526: Al echar un volado gritas «¡águila o sol!». ¿De dónde viene el nombre del lado «águila» de la moneda? → Del escudo nacional: Me ves en la bandera, en las monedas y en los libros de la escuela. Tengo un águila parada sobre un nopal. ¿Qué soy? → El Escudo Nacional
- cities-and-towns-5: overlap like q-0488: ¿Cuál es la pirámide más grande del mundo si se mide por su volumen (todo lo que ocupa)? → La pirámide de Cholula: En Cholula, sobre lo que parece un cerro cubierto de pasto, hay una iglesia amarilla. ¿Qué está escondido debajo del «cerro»? → Una pirámide
- cities-and-towns-6: overlap like q-12493: El fin de semana del Cinco de Mayo hay grandes peleas de box mexicanas. La fecha recuerda la Batalla de Puebla de 1862. ¿A quién venció México? → Al ejército francés: En 1862 el ejército mexicano venció a los franceses en Puebla. Por eso miles de calles y escuelas llevan el nombre de esa fecha. ¿Cuál es? → Cinco de Mayo
- cities-and-towns-8: overlap like q-11682: La ciudad donde se celebra la Guelaguetza lleva oficialmente el apellido de un presidente de México. ¿De cuál? → Benito Juárez: El nombre completo de la ciudad de Oaxaca lleva el apellido de un presidente nacido en ese estado. ¿De quién? → Benito Juárez
- cities-and-towns-9: overlap like q-13588: ¿Quién es esta pintora mexicana, famosa por su uniceja y las flores en el cabello? → Frida Kahlo: Tuve monos araña, loros y un venado en mi casa azul, y me pinté a mí misma con flores en el pelo y las cejas juntas. ¿Quién soy? → Frida Kahlo
- cities-and-towns-16: overlap like q-16451: La muñeca Lele nació en Amealco, Querétaro, lleva trenzas con listones de colores y la hacen artesanas otomíes. ¿De qué está hecha? → De tela: Esta muñeca otomí de Amealco, Querétaro, lleva trenzas con listones de colores y su nombre significa «bebé». ¿De qué está hecha? → De tela
- conquest-and-colony-7: overlap like q-10361: Mira esta verdura. Su nombre viene de la lengua de un pueblo mesoamericano. ¿De cuál? → Los mexicas: La palabra «tamal» la heredamos del idioma de un pueblo antiguo de México. ¿De qué pueblo? → De los mexicas
- contemporary-cinema-8: overlap like q-14676: En México, ¿a quién se le dice «regio»? → A alguien de Monterrey: Mira la foto: Cindy, de la película «Cindy la Regia» (2020), es de la ciudad de este cerro. ¿Cómo se le dice a la gente de ahí? → Regiomontanos
- contemporary-cinema-16: overlap like q-12524: Emmanuel «El Chivo» Lubezki ganó el Óscar a mejor fotografía por «Gravedad». ¿Cuántos ganó seguidos empezando con esa película? → 3: Guillermo Navarro, que filmó «Cronos» y «Hellboy», fue el primer mexicano en ganar el Óscar en esta categoría, por «El laberinto del fauno». ¿Cuál? → Mejor fotografía
- golden-age-cinema-9: overlap like q-13478: Nací en Álamos, Sonora, y fui estrella del cine de oro. Me apodaron «La Doña» por mi papel en «Doña Bárbara». ¿Quién soy? → María Félix: Soy la temida dueña de una hacienda en los llanos de Venezuela y nací en una novela de Rómulo Gallegos. En 1943, María Félix me dio vida en el cine. ¿Quién soy? → Doña Bárbara
- indigenous-peoples-1: overlap like q-7430: La gaita colombiana es un tubo de cactus cardón, con cabeza de cera de abejas y una pluma de pato; hay gaita macho y hembra. ¿Qué tipo de instrumento es? → De viento: Mira de cerca esta flauta de carrizo, una caña hueca con agujeritos. ¿A qué familia de instrumentos pertenece? → Instrumentos de viento
- indigenous-peoples-10: overlap like q-0280: El mole poblano, una salsa espesa y oscura de México, lleva chiles, especias y un ingrediente que sorprende a muchos. ¿Cuál es? → Chocolate: Mira este mole negro de Oaxaca. ¿Qué ingrediente dulce lleva, además de muchos chiles? → Chocolate
- indigenous-peoples-12: overlap like q-10327: Este arte de chaquira es de los wixárikas, también llamados huicholes. ¿En qué estados viven principalmente? → Jalisco y Nayarit: Mira esta pieza cubierta de chaquira, hecha por artesanos wixárikas (huicholes). ¿En qué estados viven sobre todo? → Jalisco y Nayarit
- indigenous-peoples-17: overlap like q-5051: Te pasan un huevo por todo el cuerpo, lo rompen en un vaso de agua y miran la clara. Según la creencia, ¿para qué es? → Para sacar el mal de ojo: En una limpia, el curandero pasa por tu cuerpo ramas de hierbas y luego algo crudo que después rompe en un vaso de agua. ¿Qué es? → Un huevo
- landmarks-1: overlap like q-12514: Mira esta enorme escultura mexica del Museo Nacional de Antropología. ¿Cómo se llama? → La Piedra del Sol: Estás en el Museo Nacional de Antropología y alguien señala el famoso «Calendario Azteca». ¿Qué objeto es en realidad? → Una enorme piedra redonda tallada
- landmarks-4: overlap like q-12687: Mira el mapa: en este estado está la isla de Janitzio, famosa por su Noche de Muertos con velas y canoas. ¿Qué estado es? → Michoacán: Justo después del 31 de octubre, la gente de la isla de Janitzio pasa la noche en el panteón con velas y cempasúchil. ¿Qué fiesta es? → Día de Muertos
- landmarks-9: overlap like q-15613: Abro entre abril y mayo, y mis fechas coinciden con el aniversario de la victoria de 1862 sobre el ejército francés. ¿Qué feria soy? → La Feria de Puebla: Mira este fuerte: junto a él se peleó la famosa batalla del 5 de mayo de 1862 contra los franceses. ¿En qué ciudad está? → Puebla
- landmarks-10: overlap like q-11666: En Teotihuacán, la noche es a la Pirámide de la Luna como el día es a la Pirámide del… → Sol: Estás en lo alto de la Pirámide del Sol, en Teotihuacán. Al final de la gran avenida ves otra pirámide, su compañera. ¿Cómo se llama? → La Pirámide de la Luna
- landmarks-11: overlap like q-12570: Mira la foto: en el equinoccio de primavera, por la escalinata de esta pirámide maya parece bajar una serpiente. ¿De qué está hecho su cuerpo? → De luz y sombra: En Chichén Itzá, una serpiente de luz y sombra parece bajar por la escalera de El Castillo. ¿Cuándo se ve mejor? → En marzo, al empezar la primavera
- landmarks-12: overlap like q-10184: Según la tradición, ¿a quién se le apareció la Virgen que se venera en este templo? → Juan Diego: A sus pies está el santuario mariano más visitado del mundo, y según la tradición ahí se le apareció la Virgen a Juan Diego. ¿Qué cerro es? → El Cerro del Tepeyac
- landmarks-15: overlap like q-10192: En este castillo pelearon los Niños Héroes en 1847. ¿En qué bosque de la Ciudad de México está? → El Bosque de Chapultepec: Mira este monumento de seis columnas a la entrada del Bosque de Chapultepec. ¿A quiénes honra? → A los Niños Héroes
- landscapes-3: overlap like q-11601: Mira la foto: este animal también sale en Minecraft. En la vida real, ¿dónde vive en libertad? → En los canales de Xochimilco: Mira este animal. En libertad casi solo vive en los canales de una zona al sur de la Ciudad de México. ¿Cuál? → Xochimilco
- landscapes-4: overlap like q-13487: Las redes de enmalle para pescar totoaba atrapan a la vaquita marina en el golfo de California. ¿Cuántas vaquitas se calculaba que quedaban en 2024? → Menos de 10: La vaquita marina es la marsopa más pequeña del mundo, tiene manchas negras alrededor de los ojos y quedan poquísimas. ¿Por qué está por desaparecer? → Queda atrapada en redes de pesca
- landscapes-7: overlap like q-10274: El Popocatépetl es un volcán activo, está cerca de Puebla y a veces echa humo y ceniza. ¿De qué parte del volcán salen? → Del cráter, en la cima: El Nevado de Toluca está en el Estado de México, mide unos 4680 metros y en el hueco de su cima guarda dos lagos. ¿Cómo se llama ese hueco? → El cráter
- landscapes-8: overlap like q-7612: Mira este pelícano de las playas de Santa Marta. ¿Para qué usa la bolsa que tiene debajo del pico? → Para atrapar peces: Mira este pelícano café, muy común en las playas de México. ¿Para qué usa la bolsa de piel debajo de su pico? → Para atrapar peces
- landscapes-9: overlap like q-4188: The eagle on a cactus eating a snake on this flag recalls the founding legend of which ancient city? → Tenochtitlan: Los mexicas buscaban una señal: un águila sobre un nopal devorando una serpiente. La vieron en un islote del lago de Texcoco. ¿Qué fundaron ahí? → Tenochtitlan
- landscapes-16: overlap like q-17285: Mira esta roca con forma de arco, en la punta de una península donde se juntan dos mares. ¿Dónde está? → En Cabo San Lucas: En el Arco de Cabo San Lucas se juntan el océano Pacífico y otro mar. ¿Cuál? → El mar de Cortés
- legends-1: overlap like q-10427: Este volcán nevado, vecino del Popocatépetl, es famoso por la figura que forma su silueta. ¿Qué figura parece? → Una mujer dormida: Según una leyenda mexica, una princesa se quedó dormida para siempre y su guerrero la cuida con una antorcha que todavía echa humo. ¿En qué se convirtieron? → En volcanes
- legends-10: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: En México, «el pingo» es otro nombre del diablo. Entonces, ¿qué clase de niño es uno al que le dicen «¡eres un pingo!»? → Uno muy travieso
- legends-15: overlap like q-0483: Según la leyenda, ¿a quién busca la Llorona cuando anda de noche, llorando cerca de los ríos? → A sus hijos: Viste de blanco, sale de noche y grita «¡Ay, mis hijos!». Según la leyenda, ¿de dónde sale para asustar a la gente? → De un río
- legends-16: overlap like q-7054: En el campo colombiano dicen que donde de noche sale una llamita del suelo hay un «entierro». ¿Qué es ese entierro? → Un tesoro escondido: Soy un montón de monedas que alguien escondió bajo tierra hace mucho, y de noche una lumbrecita marca mi lugar. ¿Cómo me dicen en México? → Un entierro
- liga-mx-3: duplicate like q-6902: Este animal es plato de Navidad en muchas casas colombianas. ¿De qué continente es originario? → América: Mira la foto: en las gradas del estadio te los venden en bolsitas. ¿De qué continente es originaria esta planta? → América
- liga-mx-12: overlap like q-11668: Es de la Ciudad de México, viste de amarillo con azul y juega el Clásico Joven contra el Cruz Azul. ¿Qué ave es el apodo del América? → Las Águilas: Lo juegan América y Cruz Azul, los dos de la Ciudad de México, y es más reciente que el duelo América contra Chivas. ¿Cómo se llama? → Clásico Joven
- mariachi-and-ranchera-0: overlap like q-5100: Llevan traje de charro con botones plateados y sombrero gigante, tocan trompetas, violines y guitarras, y en Colombia los contratan para dar serenatas. ¿Cómo se llama ese grupo? → Mariachi: «Ella» es de José Alfredo Jiménez, empieza con «Me cansé de rogarle» y es infaltable en las cantinas. ¿Qué grupo suele tocarla? → Un mariachi
- mariachi-and-ranchera-5: overlap like q-10224: El vestido de Jalisco tiene falda amplia y listones de colores, y con él se baila el jarabe tapatío. ¿Qué quiere decir 'tapatío'? → Originario de Guadalajara: Estás en una fiesta y el mariachi canta «¡Guadalajara, Guadalajara!». ¿Cómo se les dice a quienes nacieron en esa ciudad? → Tapatíos
- maya-2: overlap like q-10284: En Yucatán, algunos campesinos construyen una casita de piedra en medio de su milpa. Según la tradición maya, ¿para qué? → Para que viva ahí un alux y cuide la milpa: En Yucatán dicen que miden lo que una rodilla, cuidan las milpas y hacen travesuras si no les dejas comida. ¿Qué son los aluxes? → Duendes mayas
- maya-11: overlap like legends-7: Estás frente a la pirámide del Adivino, en Uxmal: según la leyenda maya, un enano la levantó en una sola noche. ¿Para qué? → Para ganar un reto del rey: Cuenta una leyenda de Uxmal que la Pirámide del Adivino la levantó un enano mágico. ¿En cuánto tiempo la construyó? → En una noche
- maya-16: overlap like q-14572: Estas piezas negras y brillantes se hacen en San Bartolo Coyotepec, Oaxaca. ¿De qué material están hechas? → De barro: Se moldeaba con las manos, se secaba al sol y se cocía en el fuego: así hacían los mayas sus ollas y vasos. ¿Con qué material? → Barro
- mexica-2: overlap like q-10298: Mira estos tamales. ¿De qué está hecha su masa? → De maíz: Se vende en vasito con mayonesa, limón y chile en polvo, y su nombre viene del náhuatl «izquitl». ¿De qué se hace el esquite? → De granos de maíz
- mexica-3: overlap like q-12529: Estás en el puesto de tamales y pides un atole de fresa. Desde tiempos de los mexicas, ¿de qué grano se hace el atole? → De maíz: Con la masa de este grano se hace una bebida caliente y espesa que en México se toma con tamales. ¿Cómo se llama? → Atole
- mexica-11: overlap like q-10231: Para los mexicas, quien moría de forma natural viajaba cuatro años, cruzando nueve niveles y guiado por un perro. ¿A dónde llegaba? → Al Mictlán: Estoy bajo la tierra, me gobiernan un dios con cara de calavera y su esposa, y en Día de Muertos las almas salen de mí a visitar a su familia. ¿Qué lugar soy? → El Mictlán
- mexica-15: overlap like landscapes-9: Los mexicas buscaban una señal: un águila sobre un nopal devorando una serpiente. La vieron en un islote del lago de Texcoco. ¿Qué fundaron ahí? → Tenochtitlan: Si caminaras con los mexicas desde Aztlán, buscarías la señal de su dios para fundar su ciudad. ¿Cuál de estas cosas NO formaba parte de esa señal? → Un jaguar
- national-team-2: overlap like q-12553: Soy portero mexicano y debuté con el América. En el Mundial de Brasil 2014 le paré todo a Neymar y me volví meme. ¿Quién soy? → Memo Ochoa: En el Mundial de Brasil 2014, Memo Ochoa atajó todo contra Brasil. ¿Cuántos goles hubo en total en ese partido? → 0
- national-team-15: overlap like q-12575: Short blanco, medias rojas y un águila en el pecho: así es el uniforme clásico de local de la Selección Mexicana. ¿De qué color es la camiseta? → Verde: Completa el uniforme clásico del Tri: jersey verde, short blanco y medias… → rojas
- other-cultures-5: overlap like q-10265: Estas estatuas gigantes de guerreros están en Tula, Hidalgo. ¿Qué pueblo las talló? → Los toltecas: Mira estas estatuas gigantes de piedra que están en Tula, Hidalgo. ¿A quiénes representan? → A guerreros
- other-cultures-12: overlap like q-16476: Mira este detalle del penacho de plumas de quetzal que se atribuye a Moctezuma. ¿En qué ciudad está guardado hoy? → Viena: Este códice mixteco se llama Vindobonensis por el nombre en latín de la ciudad europea donde se guarda. ¿Cuál es? → Viena
- other-sports-6: overlap like q-10272: Está en la colonia Doctores, abrió en 1956 y es sede de la empresa más antigua del mundo de su deporte. ¿De qué deporte es «la Catedral» la Arena México? → La lucha libre: Estás en la Arena México viendo una función. La organiza la empresa de lucha libre más antigua del mundo, fundada en 1933. ¿Cuál es? → CMLL
- other-sports-7: overlap like q-9841: En la inauguración de los Juegos Olímpicos de Barcelona 92, un arquero disparó una flecha en llamas. ¿Para qué? → Para encender el pebetero olímpico: La antorcha de México 68 salió de Grecia, cruzó el mar siguiendo la ruta de Colón y llegó al estadio en manos de Enriqueta Basilio. ¿Para qué servía? → Para encender el pebetero olímpico
- other-sports-14: overlap like q-11504: En la lucha libre mexicana, ¿qué es un «técnico»? → El luchador limpio que respeta las reglas: Le jalo la máscara a mi rival, hago trampa cuando el réferi no ve y el público me abuchea. En la lucha libre, ¿qué soy? → Un rudo
- painters-and-muralists-6: overlap like indigenous-peoples-12: Mira esta pieza cubierta de chaquira, hecha por artesanos wixárikas (huicholes). ¿En qué estados viven sobre todo? → Jalisco y Nayarit: Los jaguares y venados del arte huichol, de Jalisco y Nayarit, van cubiertos de bolitas diminutas de colores pegadas con cera. ¿Qué son? → Chaquiras
- painters-and-muralists-14: overlap like q-10192: En este castillo pelearon los Niños Héroes en 1847. ¿En qué bosque de la Ciudad de México está? → El Bosque de Chapultepec: El Museo de Arte Moderno de la CDMX guarda «Las dos Fridas» y está en el mismo bosque que un castillo y un zoológico. ¿Qué bosque es? → Chapultepec
- pop-and-rock-2: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: «En los ochenta encabecé Rock 101, la estación de radio que llevó el rock en inglés y en español a toda la capital.» ¿Quién soy? → Luis Gerardo Salas
- pop-and-rock-7: overlap like q-11550: ¿En qué década se formó Caifanes, la banda de Saúl Hernández que puso a todos a bailar con «La negra Tomasa»? → En los ochenta: Peace and Love fue una de las estrellas del festival de Avándaro. ¿Cuál de estas bandas NO tocó ahí? → Caifanes
- pop-and-rock-13: overlap like q-11552: «Canté “Pelo suelto” con la melena alborotada y años después también “Todos me miran”.» ¿Quién soy? → Gloria Trevi: ¿Qué cantante de Monterrey es famosa por «Doctor Psiquiatra» y «Con los ojos cerrados»? → Gloria Trevi
- pre-hispanic-gods-0: duplicate like q-1472: Este dibujo de manchas es el caparazón de un animal africano. ¿A qué grupo pertenece? → Reptiles: Mira de cerca: en el equinoccio, en Chichén Itzá, una sombra baja por la escalera hasta esta cabeza de piedra. ¿A qué grupo de animales pertenece? → Reptiles
- pre-hispanic-gods-15: overlap like q-13485: Mira estas plumas de quetzal. Entre los mexicas, ¿quiénes podían lucirlas en sus penachos? → Los gobernantes y nobles: Esta ave vive en los bosques de niebla de Chiapas, el macho tiene una cola verde larguísima y da nombre a un dios. ¿Quiénes usaban sus plumas? → Los gobernantes y nobles
- regional-mexican-1: overlap like q-7200: Escucha: con este instrumento, y no con acordeón, Guillermo Buitrago grabó canciones costeñas en los años 40. ¿Cuál es? → La guitarra: Escucha: con este instrumento de cuerdas acompaña sus corridos tumbados Natanael Cano. ¿Cuál es? → La guitarra
- regional-mexican-5: duplicate like q-17345: En el mariachi, ¿cuál de estos instrumentos NO tiene caja de resonancia de madera? → La trompeta: ¿Cuál de estos instrumentos NO toca en un trío huasteco? → La trompeta
- regional-mexican-6: overlap like q-11448: La polka, que sigue viva en la música norteña, llegó al norte de México en el siglo XIX. ¿Quiénes la trajeron? → Inmigrantes alemanes y checos: Llegué a México con inmigrantes europeos en el siglo XIX, en el norte me toca el acordeón y me bailan en pareja dando brinquitos. ¿Qué baile soy? → La polka
- regional-mexican-12: overlap like q-7596: Escucha: ¿qué instrumento es este? → El acordeón: Escucha: este instrumento es el alma de Los Invasores de Nuevo León y de casi todo grupo norteño. ¿Cuál es? → El acordeón
- regional-mexican-17: overlap like q-1986: Soy de Jalisco, México, canto corridos tumbados y en 2023 'Ella baila sola' me hizo famoso en todo el mundo. ¿Quién soy? → Peso Pluma: Mi apodo es una categoría del boxeo, grabé una sesión con Bizarrap y en 2024 gané un Grammy con mi disco «Génesis». ¿Quién soy? → Peso Pluma
- 20th-century-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Qué hicieron millones de personas en México unas dos horas ANTES del sismo del 19 de septiembre de 2017? → Un simulacro nacional
- 20th-century-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Antes de que llegara la televisión a color a México, ¿cómo se veían los programas? → En blanco y negro
- cities-and-towns-3: overlap like q-13662: El Mercado de Coyoacán está a unas cuadras de la Casa Azul de Frida Kahlo, y sus puestos más famosos tienen fila. ¿Qué venden? → Tostadas y antojitos: ¿En qué barrio de la Ciudad de México está la Casa Azul, donde vivió Frida Kahlo? → Coyoacán
- cities-and-towns-11: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: ¿Qué construyó la ciudad de Campeche alrededor de su centro para defenderse de los piratas? → Una muralla
- conquest-and-colony-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En México hay magueyes desde mucho antes de los mexicas. ¿Qué es un maguey? → Una planta
- landscapes-6: overlap like q-17286: Venecia es a las góndolas como Xochimilco es a las… → Trajineras: Mira estas lanchas de colores, llamadas trajineras. ¿En qué lugar de la Ciudad de México navegan? → Xochimilco
- legends-7: overlap like maya-11: Cuenta una leyenda de Uxmal que la Pirámide del Adivino la levantó un enano mágico. ¿En cuánto tiempo la construyó? → En una noche: Estás frente a la pirámide del Adivino, en Uxmal: según la leyenda maya, un enano la levantó en una sola noche. ¿Para qué? → Para ganar un reto del rey
- liga-mx-7: overlap like q-16589: Los Guerreros de Santos Laguna juegan en Torreón y visten de verde y blanco. ¿A qué se refiere el «Laguna» de su nombre? → A la Comarca Lagunera: Santos Laguna representa a la Comarca Lagunera, donde están Torreón y Gómez Palacio. ¿Entre cuántos estados se reparte esa región? → 2
- liga-mx-14: overlap like q-12648: Ronaldinho, campeón del mundo con Brasil, llegó a jugar con los Gallos Blancos de Querétaro. ¿En qué año llegó? → 2014: ¿Cómo se apoda el equipo de futbol de Querétaro, que juega en el Estadio Corregidora? → Los Gallos Blancos
- mariachi-and-ranchera-14: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 4: Mira este traje de charro, con botonadura de plata y bordados. ¿Para qué se usa? → Para fiestas y ceremonias importantes
- maya-6: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: El Castillo de Tulum está en un acantilado frente al Caribe, justo ante un hueco del arrecife. ¿Para qué se cree que servía? → De faro para las canoas
- maya-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En Ocosingo y otros pueblos de Chiapas, más de medio millón de personas lo usan todos los días. ¿Qué es el tseltal? → Una lengua
- mexica-0: hard fail: correct 2, unambiguous 5, no_giveaway 5, no_overlap 5: Su nombre viene del náhuatl «pétatl» y se teje con hojas de palma. ¿Qué es un petate? → Una estera para acostarse
- national-team-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Completa la frase: «En las eliminatorias, las selecciones juegan para ganarse un boleto a…». → el Mundial
- other-cultures-10: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Los antiguos mexicanos sacaban de un árbol un líquido blanco y pegajoso que, al secarse, se volvía hule. ¿Para qué lo usaban? → Para hacer pelotas
- other-sports-9: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Nací en México a principios del siglo XX. Me juegan contra una pared alta, sin red, con raquetas de cuerda y una pelota de goma. ¿Qué soy? → El frontenis
- pre-hispanic-gods-7: overlap like q-13622: En el Popol Vuh maya, Huracán, el Corazón del Cielo, mandó un gran diluvio para acabar con unos primeros humanos fallidos. ¿Cuáles? → Los hombres de madera: Según el Popol Vuh, los hombres de madera que Huracán inundó dejaron descendientes en la selva. ¿Qué animales son? → Los monos
- pre-hispanic-gods-11: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Según el orden de la Piedra del Sol, ¿qué número de sol fue el Sol de Lluvia de Fuego? → El tercero
- regional-mexican-15: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Escribo mis propias canciones y luego yo mismo las canto, como Espinoza Paz, al que llaman «el … del pueblo». ¿Qué soy? → Un cantautor
- revolution-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Los Dorados de Pancho Villa eran famosos por sus cargas a toda velocidad. ¿A qué parte del ejército pertenecían? → La caballería
- telenovelas-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En muchas telenovelas, una misma actriz interpreta a dos hermanas que nacieron el mismo día: una buena y otra muy malvada. ¿Qué son? → Gemelas
- transport-7: hard fail: correct 5, unambiguous 3, no_giveaway 3, no_overlap 5: Es un camión largo que se dobla como acordeón, va por su propio carril sin cables arriba y tiene estaciones con tarjeta. ¿Cómo se llama? → Metrobús
- transport-13: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Mira la foto: en México a este le dicen pesero. ¿Qué tipo de transporte es? → Transporte público de pasajeros
- writers-and-poets-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Soy el lugar de la casa donde nació Tita de la Garza, entre olor a cebolla, y donde la cocinera Nacha le enseñó sus recetas. ¿Qué soy? → La cocina
- writers-and-poets-9: overlap like q-16613: Este escritor creó al detective Héctor Belascoarán Shayne y escribió una enorme biografía del revolucionario de la foto. ¿Quién es? → Paco Ignacio Taibo II: Nací en los años 70, Paco Ignacio Taibo II me puso nombre y mi héroe más famoso es Héctor Belascoarán Shayne. ¿Qué soy? → El neopolicial
- revolution-0: overlap like q-13653: En el Porfiriato, los peones compraban a crédito en la tienda de raya y quedaban endeudados. ¿Quién era el dueño de esa tienda? → El hacendado: En el Porfiriato era muy rico, mandaba sobre cientos de trabajadores del campo y en la Revolución los campesinos querían quitarme mis tierras. ¿Cómo me llamaban? → El hacendado
- revolution-3: overlap like q-7352: Tenían casa grande con capilla, eran de familias poderosas de Popayán o Santafé y empleaban a muchos trabajadores. ¿Para qué servían las haciendas coloniales? → Para cultivar y criar ganado: Tenía casa grande, capilla, establos y campos de caña, henequén o maíz, y en el Porfiriato muchas medían miles de hectáreas. ¿Qué era una hacienda? → Una finca enorme en el campo
- revolution-10: overlap like q-10374: En febrero de 1913, combates en el centro de la Ciudad de México terminaron con la caída de Madero y el ascenso de Victoriano Huerta. ¿Cómo se conoce ese episodio? → La Decena Trágica: Mira la foto: este general traicionó a Madero en 1913 y se quedó con la presidencia, por eso le dicen «el Usurpador». ¿Quién es? → Victoriano Huerta
- revolution-11: overlap like q-11524: En febrero, primero se celebra el Día de la Constitución, el 5. ¿Qué día llega después el Día de la Bandera? → El 24 de febrero: Es en febrero, muchas escuelas descansan el primer lunes del mes por él y recuerda la ley que se firmó en Querétaro en 1917. ¿Qué día es? → El Día de la Constitución
- revolution-17: overlap like q-10448: Fui soldadera en la Revolución, una canción lleva mi nombre y hoy así se les dice a todas las mujeres que lucharon. ¿Quién soy? → La Adelita: Si en el festival del 20 de noviembre te vistes como las mujeres que cocinaban, curaban heridos y a veces peleaban en la Revolución, ¿de qué vas vestida? → De soldadera
- states-and-capitals-0: overlap like mariachi-and-ranchera-5: Estás en una fiesta y el mariachi canta «¡Guadalajara, Guadalajara!». ¿Cómo se les dice a quienes nacieron en esa ciudad? → Tapatíos: Veracruz es a «jarocho» como Guadalajara es a… → Tapatío
- states-and-capitals-1: overlap like q-10176: Se cuecen por horas en un gran cazo de cobre, en su propia manteca, hasta quedar doraditas y suaves. ¿De qué animal son las carnitas? → Del cerdo: Esta carne de cerdo se cuece en su propia manteca en un cazo de cobre, como en Michoacán. ¿Cómo se llama? → Carnitas
- states-and-capitals-4: overlap like contemporary-cinema-8: Mira la foto: Cindy, de la película «Cindy la Regia» (2020), es de la ciudad de este cerro. ¿Cómo se le dice a la gente de ahí? → Regiomontanos: Querétaro es a «queretano» como Monterrey es a… → Regiomontano
- states-and-capitals-5: duplicate like q-12673: Mira el mapa: en la capital de este estado nació la torta ahogada, bañada en salsa de chile. ¿Qué estado es? → Jalisco: Mira el estado resaltado en el mapa: ahí está el pueblo de Tequila, rodeado de campos de agave azul. ¿Qué estado es? → Jalisco
- states-and-capitals-6: overlap like q-14586: Un chile poblano relleno, bañado en salsa de nuez y adornado con granada y perejil, es un chile en… → Nogada: Estás adornando chiles en nogada con los colores de la bandera. Si el verde es al perejil, el rojo es a… → La granada
- states-and-capitals-13: overlap like q-13660: La cebolla morada curtida acompaña este guiso yucateco de cerdo con achiote, cocido envuelto en hoja de plátano. ¿Cuál es? → La cochinita pibil: Estás en un mercado de Oaxaca. ¿Cuál de estas cosas NO es típica de ahí? → La cochinita pibil
- states-and-capitals-14: overlap like q-12626: Es una tortilla enorme y crujiente, se unta con asiento y frijoles y lleva queso encima. ¿De qué estado es típica la tlayuda? → Oaxaca: Esta tortilla enorme y tostada, untada con asiento y frijoles y cubierta de queso y carne, es típica de un estado. ¿Cuál? → Oaxaca
- traditional-dances-7: overlap like q-13656: ¿Cómo se llaman los danzantes de penacho que tocan una mandolina hecha con el caparazón de un armadillo? → Concheros: Los concheros bailan en el Zócalo, llevan penachos de plumas y le deben su nombre a «la concha». ¿Qué es esa concha? → Una mandolina hecha con caparazón de armadillo
- writers-and-poets-8: overlap like q-14687: ¿Quién dirigió la película «¡Vámonos con Pancho Villa!», clásico del cine mexicano de los años treinta? → Fernando de Fuentes: Rafael F. Muñoz escribió esta novela de 1931 sobre los Leones de San Pablo, que se unen a la División del Norte. ¿Cuál es? → «¡Vámonos con Pancho Villa!»
- writers-and-poets-17: overlap like q-14613: Martín Luis Guzmán es a «La sombra del Caudillo» como Vicente Leñero es a… → «Los albañiles»: ¿Cuál de estas obras NO es de Gregorio López y Fuentes? → «La sombra del Caudillo»
