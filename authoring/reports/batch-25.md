# batch-25

Made by `qgen batch` on 2026-10-24 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): hosts-actors-and-comedians, telenovelas, salsa-and-tropical-music, rivers-seas-and-islands, vallenato, popular-and-andean-music, cities-and-towns, olympic-medallists, symbols-of-departments-and-cities, places-and-monuments, regions-and-departments, brands-and-products, sayings-and-expressions, tv-shows-and-series, national-team, ghosts-and-creatures, scientists-and-inventors, independence, club-football, plants-and-flowers, painters-sculptors-and-museums, regional-speech, natural-parks-and-ecosystems, mountains-and-landscapes, national-symbols, pioneers-and-popular-figures, crafts-and-traditional-dress
- Merged: 122 (q-8384…q-8505)
- Approved: 114
- Needs work: 8
- Dropped by the pipeline: 84
- Reviewed by: claude-opus-5-5
- Claude calls: 341, about $46.98 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-23, batch-24; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-23 | batch-24 | batch-25 |
|---|---|---:|---:|---:|
| source locale |  | es | es | es |
| drafts |  | 234 | 217 | 206 |
| skipped slots |  | 252 | 269 | 280 |
| dropped |  | 84 | 90 | 84 |
| drop rate | ≤ 20.0 % | 35.9 % ✗ | 41.5 % ✗ | 40.8 % ✗ |
| dropped: hard fail correct |  | 2 | 2 | 2 |
| dropped: hard fail unambiguous |  | 2 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 7 | 9 | 12 |
| dropped: overlap |  | 73 | 77 | 68 |
| dropped: duplicate |  | 0 | 0 | 2 |
| dropped: fact-check wrong |  | 1 | 3 | 1 |
| merged |  | 150 | 127 | 122 |
| approved |  | 136 | 117 | 114 |
| needs_work |  | 14 | 10 | 8 |
| needs_work rate | ≤ 20.0 % | 9.3 % ✓ | 7.9 % ✓ | 6.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.0 % ✓ | 2.4 % ✓ | 2.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.6 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.0 % ✗ | 1.6 % ✗ | 2.5 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.7 % ✓ | 3.1 % ✓ | 3.3 % ✓ |
| media: no pick in review 1 |  | 26 | 15 | 19 |
| media: recovered by research |  | 20 | 13 | 15 |
| media: no pick at record |  | 7 | 3 | 4 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.8 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 32.5 % ✗ | 36.4 % ✗ | 35.4 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 32.8 % ✗ | 23.1 % ✗ | 21.6 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 3.50 ✗ | 2.17 ✗ | 1.78 ✗ |
| approved 11–15 |  | 31 | 24 | 28 |
| top move | ≤ 25.0 % | 16.0 % ✓ | 14.2 % ✓ | 15.6 % ✓ |
| values move |  | 15 | 15 | 14 |
| top stimulus |  | 88.7 % | 89.0 % | 83.6 % |
| values stimulus |  | 3 | 5 | 4 |
| top clue | ≤ 60.0 % | 38.7 % ✓ | 38.6 % ✓ | 39.3 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 34.7 % ✓ | 24.4 % ✓ | 25.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 24.7 % ✓ | 22.0 % ✓ | 27.0 % ✗ |
| values lens |  | 10 | 11 | 11 |
| media share | 15.0 %–50.0 % | 11.3 % ✗ | 11.0 % ✗ | 16.4 % ✓ |
| mean fun | ≥ 3.40 | 3.32 ✗ | 3.29 ✗ | 3.32 ✗ |
| cost $ |  | $51.94 | $44.36 | $42.86 |
| $ per approved | ≤ $0.35 | $0.38 ✗ | $0.38 ✗ | $0.38 ✗ |
| calls |  | 347 | 287 | 281 |
| calls per approved |  | 2.55 | 2.45 | 2.46 |
| wall time h |  | 1.48 | 1.36 | 1.32 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 56 (2 %)
- Major among review needs work: 0 of 4 (0 %)
- Problems by kind: giveaway 10 (0 major), fact 5 (1 major), overlap 3 (0 major), media 1 (0 major), difficulty 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.9; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 55 of 60 (92 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.12

Major findings on approved questions:

- **q-8414**: fact — Hint 2 and the fun fact say Ospina has the most caps for Colombia. In July 2026, James Rodríguez made his 131st appearance in the round of 16 of the World Cup and either passed or tied Ospina's record (Infobae, El Tiempo, Telemundo, 7 July 2026), so both lines are now outdated or false. The answer, the other clues (Medellín 1988, Arsenal, Napoli, starter in 2014 and 2018) and the wrong answers are fine. (http://127.0.0.1:8001/review/q-8414)

## Needs work

- **q-8390** (club-football) Llevo el 10 en la espalda, juego detrás de los delanteros y me toca inventar los pases de gol; en Colombia el Pibe fue mi rey. ¿Cómo se llama mi posición? → Volante creativo: None of the media candidates works: #1 is a Free the Nipple rally (not family-friendly and off topic), and #2–#6 are close-ups of antique museum shirts, not a football shirt with the number 10. No new search is allowed. The text has a problem too: the first-person riddle speaks as the player but asks for his position instead of who he is, so it is really a plain question in disguise. It should be rewritten as a direct question, e.g. "¿Cómo se llama en Colombia la posición del 10 que juega detrás de los delanteros y arma los pases de gol, como el Pibe Valderrama?" No se encontró una imagen adecuada para esta pregunta.
- **q-8397** (crafts-and-traditional-dress) En la laguna de Fúquene cortan junco, lo secan al sol y lo tejen para hacer esteras. ¿Qué es una estera? → Un tejido plano para tender en el piso: Hint 2 ("Se teje en forma de rectángulo plano, como un individual gigante") gives the answer away: only the correct option is flat, and it even repeats the answer's key word "plano". It's also stronger than hint 3. Replace hint 2 with a vaguer clue, e.g. about where or how it's used, without "plano" or "piso", and keep the flat/floor clue for hint 3 at the latest.
- **q-8407** (mountains-and-landscapes) Mira la foto del Nevado de Santa Isabel. ¿De qué está hecha la capa blanca de su cumbre? → De hielo y nieve: The question text gives the answer away: the mountain's name, "Nevado", literally means "snow-covered" in Spanish. It also overlaps q-7276, which already states that Colombia's nevados have perpetual snow on their summits. Seeing either question answers this one, and there is no way to fix that without asking about a different fact.
- **q-8425** (places-and-monuments) Mira la foto: acordeón, caja y guacharaca. ¿En qué ciudad se hace el festival más famoso de esta música? → Valledupar: The essential image must show a vallenato group or the three instruments (accordion, caja, guacharaca), but every candidate shows only European or US accordion players, and no new search is allowed. The slot needs a real photo of a vallenato ensemble, for example from a search like "vallenato caja guacharaca" or "conjunto vallenato". No se encontró una imagen adecuada para esta pregunta.
- **q-8461** (plants-and-flowers) ¿En qué ciudad colombiana desfilan cada agosto los silleteros, que cargan enormes arreglos de flores en la espalda? → Medellín: Overlaps approved q-6935 ("En el Desfile de Silleteros de Medellín, ¿cuánto puede llegar a pesar…?"), which names Medellín as the home of the silleteros, so seeing it gives this question away. Also no candidate shows silleteros: all are Dutch, English or French flower parades. No new search is allowed. No se encontró una imagen adecuada para esta pregunta.
- **q-8468** (regional-speech) Viene del quechua y se oye mucho en Pasto y en Ecuador. ¿Qué es un «guambra»? → Un muchacho joven: Hint 2 ("Las mamás nariñenses lo usan para llamar a sus hijos") gives the answer away. Of the four options, only "un muchacho joven" fits a word mothers use for their children, so it rules out all three wrong answers before hint 3. Replace it with something vaguer, for example that the word is used for both boys and girls, or that it's common in Ecuador's highlands too, without implying "child".
- **q-8471** (sayings-and-expressions) Según un dicho, el dinero no da la felicidad. ¿Cómo le dicen al dinero en Colombia? → La plata: Overlaps the approved q-7393 ("estar pelado" → "Estar sin plata"): that question's answer uses "plata" as the Colombian word for money, so anyone who has seen it already knows this answer. The two ask nearly the same piece of slang knowledge, so drop this question or replace it with a different Colombian expression.
- **q-8497** (symbols-of-departments-and-cities) En 1848, colonos de Neira y Salamina hicieron la «Expedición de los Veinte» para escoger el sitio de una ciudad nueva. ¿Cuál se fundó allí en 1849? → Manizales: None of the image candidates fits the topic (the 1848 Antioquian colonization and the founding of Manizales), and a new search is not allowed. A suitable image would be the colonial architecture of Salamina or Neira, mule trains (arrieros) or Andean coffee-region mountains, without anything showing Manizales. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 1, cause_effect 4, estimate 3, identify 18, made_of 4, name_concept 18, odd_one_out 7, origin 10, purpose 11, record 1, sequence 2, when 6, who 19, word_meaning 18
- stimulus: map_outline 2, none 102, photo 17, sound 1
- clue: completion 5, direct 48, riddle 18, scenario 14, three_facts 37
- answer_kind: group 8, number 3, person 28, place 14, thing 31, time 7, word 31
- lens: body_senses 4, colombia 33, educational_media 10, everyday 19, history 12, language 15, nature 6, pop_culture 12, popular_science 1, school 9, science_news 1

## Dropped by the pipeline

- brands-and-products-13: overlap like q-7689: Lo venden en carritos por la calle y viene de muchos colores. ¿Qué es un Bon Ice? → Un hielo de sabor en tubito: Los vendedores de Bon Ice recorren calles y parques con su nevera. ¿Qué es un Bon Ice? → Hielo de sabores
- brands-and-products-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Estás viendo un partido de la Selección Colombia y gritas el nombre de una chocolatina. ¿Cuál? → Gol
- cities-and-towns-17: overlap like q-0557: Completa: Grupo Niche es a «Cali pachanguero» como Fruko y sus Tesos es a… → El preso: Soy una salsa del Grupo Niche y en mi coro llamo a mi ciudad «luz de un nuevo cielo». ¿Qué canción soy? → «Cali pachanguero»
- club-football-3: overlap like q-6690: I'm small enough to hold in your hand. When a boat is in trouble, I'm lit and I shoot a bright red light into the sky so rescuers can find it. What am I? → A flare: Me sostienen en la mano cuando sale el equipo, suelto humo y una luz roja que quema, y en los estadios colombianos estoy prohibida. ¿Qué soy? → Una bengala
- club-football-9: overlap like q-7086: Esta estatua gigante de bronce homenajea al Pibe Valderrama, junto al estadio de su ciudad natal. ¿Dónde está? → Santa Marta: Al «Pibe» Valderrama lo vieron debutar en el Unión Magdalena en 1981 y tiene una estatua gigante junto al estadio Eduardo Santos. ¿En qué ciudad nació? → Santa Marta
- club-football-11: overlap like q-7337: En 1995, en el estadio de Wembley, René Higuita hizo su famoso «escorpión». ¿Qué fue esa jugada? → Un despeje con los talones, lanzado hacia adelante: Fui arquero de Nacional y de la Selección, con melena crespa, y en Wembley atajé un balón con los talones haciendo «el escorpión». ¿Quién soy? → René Higuita
- crafts-and-traditional-dress-1: overlap like q-7954: En diciembre se arma con musgo y figuritas, y a la medianoche del 24 se pone al Niño Dios. ¿Qué dos animales lo acompañan en el pesebre? → La mula y el buey: Soy una figurita de barro muy chiquita. En la novena mi puesto en el pesebre está vacío, y me ponen ahí a la medianoche del 24 de diciembre. ¿Quién soy? → El Niño Dios
- crafts-and-traditional-dress-3: overlap like q-5120: Es la prenda insignia de los boyacenses, se teje en telar en Nobsa y abriga en el frío del altiplano. ¿De qué está hecha la ruana tradicional? → De lana de oveja: El campesino boyacense lleva sombrero, alpargatas y una prenda de lana gruesa, abierta por delante, que se pone por la cabeza. ¿Cómo se llama? → La ruana
- crafts-and-traditional-dress-4: overlap like q-0420: Mira la foto: ¿cómo se llaman estos campesinos que desfilan en Medellín cargando enormes arreglos de flores en la espalda? → Silleteros: Mira de cerca: esta estructura de madera llena de flores se carga en la espalda en un desfile de Antioquia. ¿Cómo se llama quien la lleva? → Un silletero
- crafts-and-traditional-dress-10: overlap like q-7755: Gracias a la herencia zenú de tejer en telar vertical, este pueblo de los Montes de María, en Bolívar, es famoso por sus hamacas. ¿Cuál es? → San Jacinto: Las hamacas tejidas en telar en San Jacinto, Bolívar, vienen de una tradición indígena muy antigua. ¿De qué pueblo? → Los zenúes
- ghosts-and-creatures-5: overlap like q-7622: 'Soñar no cuesta nada' cuenta la historia real de unos soldados que encuentran una guaca de millones de dólares de la guerrilla en la selva. ¿En qué año ocurrió el hallazgo? → 2003: En el campo colombiano hay gente que cava en cerros y tumbas indígenas antiguas, soñando con ollas llenas de oro. ¿Cómo se llama ese tesoro enterrado? → Una guaca
- ghosts-and-creatures-6: overlap like q-7838: «Se va el caimán» cuenta de un hombre que se volvió mitad caimán, y su pueblo celebra cada año el Festival del Hombre Caimán. ¿Qué pueblo es? → Plato: Me tomé una pócima para nadar en el río sin que me vieran, y como la otra no me cayó completa, quedé con cabeza de hombre y cuerpo de reptil. ¿Quién soy? → El Hombre Caimán
- ghosts-and-creatures-7: overlap like q-8260: Estudia los restos de pueblos antiguos, excava la tierra con cuidado y en San Agustín, Huila, ha sacado a la luz cientos de estatuas de piedra. ¿Qué ciencia es? → La arqueología: En el sur del Huila hay cientos de estatuas de piedra muy antiguas, y algunas muestran al Hombre Jaguar con colmillos de felino. ¿En qué parque arqueológico están? → San Agustín
- ghosts-and-creatures-11: overlap like q-6995: ¿Cómo se llama el hombre que, como este, lleva carga en mulas por los caminos de montaña? → Arriero: El rezandero cura con oraciones. ¿Cuál de estos NO es alguien que cura a la gente en el campo colombiano? → El arriero
- ghosts-and-creatures-17: hard fail: correct 3, unambiguous 4, no_giveaway 2, no_overlap 5: Ando de noche por el monte, nadie me ve y solo me oyen pegar alaridos que hielan la sangre; dicen que es mejor no contestarme. ¿Quién soy? → El Gritón
- independence-0: overlap like q-7245: Era vendedora en la plaza del Socorro. Un día arranqué el edicto con los nuevos impuestos y empezó la Revolución de los Comuneros. ¿Quién soy? → Manuela Beltrán: Pasó en El Socorro, Santander, en 1781: Manuela Beltrán rompió el edicto de los nuevos impuestos y miles de personas se levantaron. ¿Cómo se llamó esa rebelión? → La Revolución de los Comuneros
- independence-2: overlap like q-5112: Me fueron a pedir prestado para adornar una cena en honor a Villavicencio, mi dueño se negó y la pelea terminó en revuelta. ¿Qué soy? → El florero de Llorente: Antonio Morales fue a pedir prestado un florero el 20 de julio de 1810. Por eso, en Colombia, «ser el florero de Llorente» quiere decir… → Ser la excusa para armar un problema grande
- independence-5: overlap like q-7414: A finales del siglo XVIII, Antonio Nariño tradujo e imprimió en secreto en Santafé un texto prohibido. ¿Cuál era? → La Declaración de los Derechos del Hombre y del Ciudadano: En su Imprenta Patriótica de Santafé, Antonio Nariño imprimió en 1793 un texto traducido del francés que lo llevó a prisión. ¿Cuál era? → Los Derechos del Hombre y del Ciudadano
- independence-9: overlap like q-7630: Fui un joven coronel antioqueño de la Independencia y luché junto a Bolívar. Hoy una ciudad de tierra caliente, a orillas del Magdalena, lleva mi apellido. ¿Quién soy? → Atanasio Girardot: Nací en Medellín, crucé a Venezuela con Bolívar en 1813 y caí en la batalla de Bárbula al clavar la bandera en la cima. ¿Quién soy? → Atanasio Girardot
- independence-13: overlap like q-8270: En diciembre de 1814, ¿quién tomó Santafé al mando de las tropas del Congreso y obligó a Cundinamarca a unirse a las Provincias Unidas? → Simón Bolívar: ¿Cuál de estas provincias NO firmó el Acta de Federación de las Provincias Unidas de la Nueva Granada en noviembre de 1811? → Cundinamarca
- independence-16: overlap like q-7142: Cartagena se ganó el apodo de «La Heroica» por resistir un largo sitio en 1815. ¿Contra quiénes? → Las tropas españolas de Pablo Morillo: Completa: por resistir el sitio de 1815, a Cartagena la llaman «la Ciudad…». → Heroica
- mountains-and-landscapes-1: overlap like q-5119: ¿Qué departamento de Colombia está resaltado en este mapa? → Antioquia: Mira el mapa: en el departamento marcado está el Cerro Tusa, un cerro con forma de pirámide. ¿Cuál es? → Antioquia
- mountains-and-landscapes-6: overlap like q-7017: Subes al cerro de la Popa, en Cartagena, para la fiesta de la Virgen de la Candelaria. ¿Qué fecha es? → 2 de febrero: ¿Cuál de estos cerros NO está en Bogotá? → La Popa
- mountains-and-landscapes-8: overlap like q-0032: ¿Cuál es el roedor más grande del mundo? → El chigüiro: En las sabanas inundables de los Llanos vive en manada, nada muy bien y come pasto. Es el roedor más grande del mundo. ¿Cuál es? → El chigüiro
- mountains-and-landscapes-10: overlap like q-5141: Este paisaje con frailejones sale en el billete de 5000. ¿Por qué es tan importante para ciudades como Bogotá? → Porque guarda y da el agua que toman: En el páramo, el musgo y los frailejones atrapan el agua de la niebla y la lluvia y la sueltan poco a poco a los ríos. ¿A qué objeto se parecen? → A una esponja
- national-symbols-4: overlap like q-7865: Estás en la Casa del Florero, en Bogotá, donde se recuerda el 20 de julio de 1810. ¿Cuál de estas cosas NO pasó ese día? → La batalla de Boyacá: Mira este florero: el 20 de julio, una pelea por pedirlo prestado encendió el grito de independencia. ¿En qué ciudad pasó? → Bogotá
- national-symbols-9: overlap like q-7426: Estás en el valle de Cocora, frente a la palma de cera, el árbol nacional de Colombia. ¿Hasta qué altura puede llegar? → Unos 60 metros: Mira la foto: estas palmas de cera son famosas en un valle del Quindío que visitan miles de turistas. ¿Cuál es? → El valle de Cocora
- national-symbols-10: overlap like q-0587: ¿Para qué sirve este edificio del centro de Bogotá? → Es la sede y residencia oficial del presidente: Mira la foto: ¿cómo se llama este edificio de Bogotá? → La Casa de Nariño
- national-team-0: overlap like q-7337: En 1995, en el estadio de Wembley, René Higuita hizo su famoso «escorpión». ¿Qué fue esa jugada? → Un despeje con los talones, lanzado hacia adelante: En 1995, en Wembley, René Higuita despejó el balón con los talones, arqueando la espalda por encima de la cabeza. ¿Qué animal le dio nombre a esa jugada? → El escorpión
- natural-parks-and-ecosystems-3: overlap like q-0202: Escucha: ¿qué animal de la selva amazónica hace este sonido? → El mono aullador: Escucha: aves, insectos y monos aulladores. ¿En qué lugar de Colombia se grabó este sonido? → En la selva del Amazonas
- olympic-medallists-5: overlap like q-7376: ¿En qué puesto llegó Rigoberto Urán, el ciclista de Urrao, en la prueba de ruta de los Juegos Olímpicos de Londres 2012? → Segundo: Estás viendo en la tele a Rigoberto Urán, plata olímpica en ciclismo de ruta en Londres 2012. ¿Cuántas ruedas tiene su bicicleta? → 2
- olympic-medallists-9: overlap like q-8007: Nací en Maicao, La Guajira. En Tokio 2020 di una vuelta completa a la pista a toda velocidad y solo un corredor llegó antes que yo. ¿Quién soy? → Anthony Zambrano: Steven Gardiner fue campeón mundial de 400 metros en 2019 y ganó el oro olímpico en Tokio 2020, por delante del colombiano Anthony Zambrano. ¿De qué país es? → Bahamas
- painters-sculptors-and-museums-4: overlap like q-6926: Se saca de minas como Muzo y Chivor, en Boyacá, y las colombianas son famosas en todo el mundo. ¿Qué piedra preciosa es? → La esmeralda: Esta joya de oro de la iglesia de San Ignacio, en Bogotá, tiene apodo de verdura. ¿De qué piedras verdes está cubierta? → Esmeraldas
- painters-sculptors-and-museums-15: overlap like q-8172: Fui un filántropo antioqueño, viví en un castillo de Medellín que hoy es museo y le regalé a Itagüí su primera biblioteca. ¿Quién soy? → Diego Echavarría Misas: Este museo de El Poblado, en Medellín, parece un castillo medieval europeo y se construyó en los años 30. ¿Qué fue antes de ser museo? → Una casa de familia
- pioneers-and-popular-figures-4: overlap like q-7103: Es hija de colombianos, actuó en «Jane the Virgin» y en «Encanto» puso la voz en inglés de una Madrigal. ¿Qué don tiene ese personaje? → Hacer brotar flores y plantas: Isabela es la hermana mayor de Mirabel, el pueblo la cree perfecta y casi se compromete con Mariano. ¿Qué hace brotar con su don? → Flores
- pioneers-and-popular-figures-12: overlap like q-7625: La compuso Lin-Manuel Miranda, la canta Sebastián Yatra y fue nominada al Óscar a mejor canción. ¿De qué película viene 'Dos oruguitas'? → Encanto: La canta Sebastián Yatra, habla de dos orugas enamoradas y fue nominada al Óscar. ¿De qué película es «Dos oruguitas»? → Encanto
- places-and-monuments-2: overlap like q-5042: La marimonda del carnaval, con su trompa larga, orejas grandes y corbata, nació con una intención. ¿Cuál? → Burlarse de los ricos y los políticos: Tengo nariz larga como una trompa, orejas enormes, saco y corbata, y me burlo de los ricos y los políticos en el carnaval. ¿Quién soy? → La Marimonda
- places-and-monuments-3: overlap like q-7413: ¿Para qué se construyó el Metrocable de Medellín? → Para llevar a la gente a los barrios de las montañas: Mira la foto: estas cabinas pasan por encima de los barrios de las montañas de Medellín. ¿Para qué las usa la gente? → Para moverse por la ciudad, como en un bus o el metro
- places-and-monuments-8: overlap like q-7874: Subes los escalones de piedra de Ciudad Perdida, en la Sierra Nevada. ¿Más o menos cuándo empezaron los taironas a construirla? → Hacia el año 800 d. C.: Para llegar a las terrazas de Ciudad Perdida, en la Sierra Nevada de Santa Marta, hay que subir una escalera de piedra. ¿Más o menos cuántos escalones tiene? → Unos 1200
- places-and-monuments-10: overlap like q-6855: Para ver desde arriba el embalse de Guatapé se sube la Piedra del Peñol. ¿Más o menos cuántos escalones tiene su escalera? → Unos 700: Mira la foto: esta roca gigante se alza junto a un embalse en Antioquia. ¿Cómo se llama? → La Piedra del Peñol
- places-and-monuments-11: duplicate like q-8316: Esta capilla colonial está en lo alto de una colina y le da nombre a uno de los barrios más tradicionales de su ciudad. ¿En qué ciudad está? → Cali: Mira la foto: esta estatua de Cristo con los brazos abiertos vigila la ciudad desde el cerro Los Cristales. ¿En qué ciudad está? → Cali
- places-and-monuments-15: overlap like q-7630: Fui un joven coronel antioqueño de la Independencia y luché junto a Bolívar. Hoy una ciudad de tierra caliente, a orillas del Magdalena, lleva mi apellido. ¿Quién soy? → Atanasio Girardot: Mira la foto: este estadio de Medellín lleva el nombre de un prócer de la Independencia. ¿De cuál? → Atanasio Girardot
- plants-and-flowers-2: overlap like q-5141: Este paisaje con frailejones sale en el billete de 5000. ¿Por qué es tan importante para ciudades como Bogotá? → Porque guarda y da el agua que toman: Los páramos de Colombia son fríos, tienen frailejones y musgos que funcionan como esponjas. ¿Qué les dan a ciudades como Bogotá? → Agua
- plants-and-flowers-9: overlap like q-0272: Mira la foto: ¿cómo se llama esta palma? → Palma de cera: Es el árbol nacional de Colombia, crece en el Valle de Cocora y puede pasar los 50 metros de alto. ¿Cómo se llama? → La palma de cera
- plants-and-flowers-11: overlap like q-1158: Me llaman 'el río de los cinco colores' y algunos meses del año mi fondo se pone rojo intenso. ¿Qué me pinta de ese color? → Una planta acuática: Mira la foto: este río de la sierra de la Macarena se pone rojo varios meses al año. ¿Qué es lo rojo que ves en el agua? → Una planta acuática
- popular-and-andean-music-3: fact-check wrong: The first Festival Nacional de la Guabina y el Tiple was held in 1962, so it started in the 1960s, not the 1940s. The hint about the Bogotá 400th anniversary (1938) is also misleading.: El Festival Nacional de la Guabina y el Tiple se celebra en Vélez, Santander. ¿En qué década nació? → En los años cuarenta
- popular-and-andean-music-6: overlap like q-7978: Cada fin de año, los alumbrados navideños llenan de luces el río Medellín. ¿En qué mes se apagan? → Enero: ¿En qué época del año se prenden los famosos alumbrados de Medellín? → En diciembre, por Navidad
- regional-speech-0: overlap like q-6939: «Tú vienes» es a «¡Ven!» como «vos venís» es a… → «¡Vení!»: En una telenovela paisa, la mamá le da órdenes al hijo. ¿Cuál de estas NO está en voseo? → «Ven»
- regional-speech-8: overlap like q-6967: La chirimía con clarinete, bombardino, redoblante, bombo y platillos es la banda típica de un departamento del Pacífico. ¿Cuál? → Chocó: Con clarinete, bombardino, tambora y platillos, la chirimía alegra las fiestas de San Pacho. ¿De qué departamento es típica? → Chocó
- regions-and-departments-0: duplicate like q-6861: Mira el mapa: ¿en qué departamento está el cañón del Combeima, que sube hacia un nevado? → Tolima: Mira el mapa: ¿qué departamento de Colombia está resaltado? → Tolima
- regions-and-departments-5: overlap like q-7112: Esta isla rocosa del Pacífico colombiano es Patrimonio de la Humanidad. ¿Por qué animales es famosa? → Tiburones: Las islas Galápagos son a las tortugas gigantes como la isla Malpelo es a los… → Tiburones martillo
- regions-and-departments-9: overlap like mountains-and-landscapes-13: Estás en una islita del archipiélago de San Bernardo tan llena de casas que casi no queda espacio libre; la llaman «la isla más poblada del mundo». ¿Cuál es? → Santa Cruz del Islote: Llegas a Santa Cruz del Islote, en San Bernardo, una isla más pequeña que dos canchas de fútbol. ¿Cuántas personas viven allí, más o menos? → Unas 1000
- regions-and-departments-15: overlap like q-6985: La guacharaca del conjunto vallenato lleva el nombre de un ave de la costa. ¿A qué familia de instrumentos pertenece? → De percusión: La marimba de chonta tiene tablillas de palma, tubos de guadua y suena en el currulao. ¿A qué familia de instrumentos pertenece? → Los de percusión
- cities-and-towns-14: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: Mira la foto: ¿de qué región de Colombia es típico este plato? → La costa Caribe
- ghosts-and-creatures-3: overlap like q-7463: A muchos bebés colombianos les ponen una pulserita con un azabache contra el mal de ojo. ¿Qué es el azabache? → Una piedra negra: A muchos bebés en Colombia les ponen una manilla roja en la muñeca. Según la tradición, ¿contra qué los protege? → El mal de ojo
- mountains-and-landscapes-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Completa: en el Eje Cafetero, un chapolero o una chapolera es una persona que… → …recoge café
- mountains-and-landscapes-13: overlap like regions-and-departments-9: Llegas a Santa Cruz del Islote, en San Bernardo, una isla más pequeña que dos canchas de fútbol. ¿Cuántas personas viven allí, más o menos? → Unas 1000: Estás en una islita del archipiélago de San Bernardo tan llena de casas que casi no queda espacio libre; la llaman «la isla más poblada del mundo». ¿Cuál es? → Santa Cruz del Islote
- national-symbols-14: overlap like q-7646: Completa: en los colegios de Colombia, el acto cívico en que se honra la patria y se premia a los mejores estudiantes se llama «izada de…». → bandera: En los colegios de Colombia, a los mejores estudiantes los llaman al frente en un acto cívico para un honor especial. ¿Cuál? → Izar la bandera
- national-team-5: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: En los Mundiales de 32 selecciones, después de la fase de grupos quedan 16. ¿Cómo se llama esa ronda, a la que Colombia llegó en 1990, 2014 y 2018? → Los octavos de final
- natural-parks-and-ecosystems-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Mira la foto de Sumapaz, cerca de Bogotá, el más grande del mundo de su tipo. ¿Qué tipo de ecosistema es? → Un páramo
- natural-parks-and-ecosystems-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En las Islas del Rosario, muchos turistas hacen «careteo». ¿Qué es? → Nadar con careta y tubo
- natural-parks-and-ecosystems-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Mira esta foto tomada en el Tequendama, cerca de Bogotá. ¿Qué es lo que ves? → Una cascada
- painters-sculptors-and-museums-1: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Marco Ospina, pintor bogotano nacido en 1912, es considerado el primer artista colombiano de un estilo de pintura. ¿Cuál? → El arte abstracto
- places-and-monuments-4: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: La famosa balsa muisca muestra la ceremonia de la laguna de Guatavita que inspiró una leyenda. ¿De qué está hecha? → De oro
- salsa-and-tropical-music-0: overlap like q-7018: En la Feria de Cali todo el mundo sale a bailar salsa. ¿Cuál de estas cosas NO es un baile? → La arepa: Cali es famosa en el mundo por su salsa, pero no la de la cocina. ¿Qué es esa salsa? → Un baile
- scientists-and-inventors-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En 1821, José Félix de Restrepo defendió en el Congreso de Cúcuta la ley de libertad de vientres. ¿Quiénes nacerían libres gracias a ella? → Los hijos de las mujeres esclavizadas
- symbols-of-departments-and-cities-12: overlap like q-7316: Los reguetoneros le dicen «Medallo» a Medellín. ¿Cuál de estos apodos NO es de Medellín? → La Arenosa: ¿Con qué apodo cariñoso se conoce a Barranquilla, la ciudad del Carnaval? → La Arenosa
- vallenato-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Consuelo Araújo Noguera fundó el Festival de la Leyenda Vallenata con Rafael Escalona y Alfonso López Michelsen. ¿En qué año fue el primero? → 1968
- rivers-seas-and-islands-4: overlap like q-7158: La quebrada Las Gachas, con huecos redondos como jacuzzis en un lecho de roca rojiza, está en el departamento resaltado. ¿Cuál es? → Santander: Mira el mapa: en este departamento, la represa Hidrosogamoso embalsa las aguas del río Sogamoso. ¿Cuál es? → Santander
- rivers-seas-and-islands-5: overlap like q-5058: Quien dice «¡achichay!» cuando hace frío, con acento pastuso, viene del departamento resaltado. ¿Cuál es? → Nariño: Mira el mapa: en la isla del Gallo, frente a este departamento, Pizarro trazó una raya en la arena y solo 13 hombres la cruzaron. ¿Qué departamento es? → Nariño
- rivers-seas-and-islands-17: overlap like q-8292: Mira el contorno: es una isla colombiana del Caribe, la segunda más grande del archipiélago después de San Andrés. ¿Cuál es? → Providencia: Mira el mapa: en esta isla del Caribe colombiano está El Peak, un cerro de unos 360 metros. ¿Qué isla es? → Providencia
- sayings-and-expressions-3: overlap like q-6992: Le preguntas a alguien: «¿Vamos por un tinto?», y te responde: «¡Hágale!». ¿Qué te está diciendo? → Que sí, que vamos: Completa: cuando un paisa te dice «¡hágale, pues!», te está diciendo que… → …sí, que lo hagas ya
- sayings-and-expressions-5: overlap like q-1317: Aparezco como bultitos en tus brazos cuando tienes frío, y los pelitos se paran. ¿Para qué les servía a nuestros ancestros peludos? → Para atrapar aire caliente en el pelo: Cuando hace frío o una canción te emociona, se te paran los pelitos y te salen bultitos. ¿Cómo se dice? → Piel de gallina
- scientists-and-inventors-3: overlap like q-5008: Estás viendo las miles de láminas de flores pintadas a mano por la Real Expedición Botánica. ¿Quién dirigió esa expedición? → José Celestino Mutis: Estás en el Real Jardín Botánico de Madrid y ves miles de láminas de plantas de la Nueva Granada pintadas hace más de 200 años. ¿Quién dirigió la expedición que las hizo? → José Celestino Mutis
- symbols-of-departments-and-cities-0: overlap like q-7466: Mira este cuatro, el instrumento del joropo llanero. ¿A qué grupo de instrumentos pertenece? → De cuerda: Tiene una caja grande de madera, suena en el joropo junto al cuatro y las maracas, y es símbolo de los Llanos. ¿A qué familia de instrumentos pertenece el arpa llanera? → Instrumentos de cuerda
- symbols-of-departments-and-cities-3: overlap like q-0986: Mira de cerca este animal acuático. ¿A qué grupo de animales pertenece? → Mamíferos: En las ciénagas del Caribe colombiano vive el manatí: come plantas, sube a respirar y le dicen «vaca marina». ¿Qué es un manatí? → Un mamífero acuático
- symbols-of-departments-and-cities-6: overlap like q-8434: Mira el mapa: en el departamento resaltado está el volcán del Totumo, donde la gente flota en lodo. ¿Cuál es? → Bolívar: Los momposinos son de una ciudad famosa por su filigrana de plata y su Semana Santa, en el departamento resaltado. ¿Cuál es? → Bolívar
- symbols-of-departments-and-cities-16: overlap like q-8290: Mira la foto: este santuario blanco está en la cima de un cerro de Bogotá. ¿Para qué suben miles de personas hasta allá? → Para rezar en la iglesia y ver la ciudad desde arriba: Mira este detalle: esta iglesia blanca está en la cima de un cerro de Bogotá. ¿Qué cerro es? → Monserrate
- telenovelas-1: overlap like q-6844: Juanpis González es un gomelo, le dice «mi papi» a su papá y tiene su programa, «Juanpis Live Show». ¿De qué ciudad es? → Bogotá: En las telenovelas siempre aparece: viene de familia rica, viste solo ropa de marca y habla con un acento muy pispo. ¿Qué palabra colombiana lo describe? → Gomelo
- telenovelas-2: overlap like symbols-of-departments-and-cities-0: Tiene una caja grande de madera, suena en el joropo junto al cuatro y las maracas, y es símbolo de los Llanos. ¿A qué familia de instrumentos pertenece el arpa llanera? → Instrumentos de cuerda: Nació en los Llanos Orientales, se toca con arpa, cuatro y maracas, y se baila zapateando. ¿Qué música es? → El joropo
- telenovelas-10: overlap like q-5125: En la bionovela «Rigo», el pequeño Rigoberto Urán vende chance en las calles de Urrao para ayudar a su familia. ¿Qué es el «chance»? → Un juego de apuestas con números: «Diomedes, el cacique de La Junta», «Rafael Orozco, el ídolo» y «Rigo» contaron la vida real de artistas y deportistas. ¿Cómo se llama ese tipo de telenovela? → Bionovela
- telenovelas-17: overlap like q-7144: En «Café con aroma de mujer» (1994), Guy Ecker fue Sebastián, el galán que se enamora de Gaviota. ¿De qué familia era? → Los Vallejo: Soy recolectora de café y me enamoro del hijo de los dueños de la hacienda. En 1994 me interpretó Margarita Rosa de Francisco. ¿Qué apodo tengo? → Gaviota
- tv-shows-and-series-10: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: ¿En qué año empezaron en Colombia las primeras transmisiones de Televisión Digital Terrestre (TDT)? → 2010
- vallenato-0: overlap like q-5019: Este cantante de Santa Marta mezcló el vallenato con rock y pop en los años 90. ¿Quién es? → Carlos Vives: Este cantante de Santa Marta grabó «La tierra del olvido» en 1995. ¿Quién es? → Carlos Vives
