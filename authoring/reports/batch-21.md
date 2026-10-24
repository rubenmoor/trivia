# batch-21

Made by `qgen batch` on 2026-10-23 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): hosts-actors-and-comedians, 19th-century, languages, olympic-medallists, places-and-monuments, salsa-and-tropical-music, traditional-games, natural-parks-and-ecosystems, rivers-seas-and-islands, club-football, home-school-and-paperwork, indigenous-myths-and-folk-beliefs, independence, writers-and-books, plants-and-flowers, national-team, tv-shows-and-series, christmas-and-special-dates, carnivals-and-fairs, scientists-and-inventors, banknotes-and-coins, brands-and-products, pre-columbian-cultures, other-sports, fruits, painters-sculptors-and-museums, rhythms-dances-and-instruments
- Merged: 177 (q-7789…q-7965)
- Approved: 169
- Needs work: 8
- Dropped by the pipeline: 89
- Reviewed by: claude-opus-5-5
- Claude calls: 435, about $60.22 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-19, batch-20; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-19 | batch-20 | batch-21 |
|---|---|---:|---:|---:|
| source locale |  | es | es | es |
| drafts |  | 261 | 266 | 266 |
| skipped slots |  | 225 | 220 | 220 |
| dropped |  | 84 | 79 | 89 |
| drop rate | ≤ 20.0 % | 32.2 % ✗ | 29.7 % ✗ | 33.5 % ✗ |
| dropped: hard fail correct |  | 2 | 3 | 0 |
| dropped: hard fail unambiguous |  | 1 | 2 | 1 |
| dropped: hard fail no_giveaway |  | 15 | 13 | 20 |
| dropped: overlap |  | 66 | 63 | 67 |
| dropped: duplicate |  | 0 | 0 | 2 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 177 | 187 | 177 |
| approved |  | 157 | 170 | 169 |
| needs_work |  | 20 | 17 | 8 |
| needs_work rate | ≤ 20.0 % | 11.3 % ✓ | 9.1 % ✓ | 4.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 4.0 % ✓ | 2.7 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.1 % ✓ | 0.0 % ✓ | 0.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.7 % ✗ | 1.6 % ✗ | 0.6 % ✓ |
| needs_work: media | ≤ 10.0 % | 5.1 % ✓ | 5.3 % ✓ | 3.4 % ✓ |
| media: no pick in review 1 |  | 31 | 33 | 26 |
| media: recovered by research |  | 23 | 23 | 22 |
| media: no pick at record |  | 8 | 10 | 4 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 26.4 % ✗ | 24.8 % ✗ | 26.3 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 32.8 % ✗ | 48.0 % ✗ | 34.7 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.13 ✓ | 1.50 ✓ | 1.43 ✓ |
| approved 11–15 |  | 27 | 51 | 28 |
| top move | ≤ 25.0 % | 16.4 % ✓ | 13.4 % ✓ | 13.0 % ✓ |
| values move |  | 15 | 15 | 14 |
| top stimulus |  | 80.2 % | 88.8 % | 84.7 % |
| values stimulus |  | 5 | 4 | 4 |
| top clue | ≤ 60.0 % | 44.1 % ✓ | 41.7 % ✓ | 39.0 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 24.9 % ✓ | 25.7 % ✓ | 20.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 27.7 % ✗ | 23.5 % ✓ | 23.7 % ✓ |
| values lens |  | 12 | 11 | 12 |
| media share | 15.0 %–50.0 % | 19.8 % ✓ | 11.2 % ✗ | 15.3 % ✓ |
| mean fun | ≥ 3.40 | 3.33 ✗ | 3.38 ✗ | 3.38 ✗ |
| cost $ |  | $53.84 | $58.01 | $56.01 |
| $ per approved | ≤ $0.35 | $0.34 ✓ | $0.34 ✓ | $0.33 ✓ |
| calls |  | 382 | 395 | 375 |
| calls per approved |  | 2.43 | 2.32 | 2.22 |
| wall time h |  | 1.49 | 1.71 | 1.65 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 57 (2 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 4 (0 major), fact 3 (1 major), media 2 (0 major), difficulty 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.21

Major findings on approved questions:

- **q-7916**: fact — The answer (2010s) is right. Hint 3 is wrong, though: it says the tower reached its top height two years after the 2014 World Cup, so 2016. Wikipedia says the south tower topped out at 216 m on 24 July 2015 and passed Colpatria on 2 June 2015, one year after Brasil 2014; only the structural work ended in February 2016. The crowdfunding fun fact checks out (more than 3800 investors, billed as the first crowdfunded skyscraper), and there's no overlap with the related decade questions. (http://127.0.0.1:8001/review/q-7916)

## Needs work

- **q-7789** (19th-century) Hacia 1850 el Partido Liberal se dividió entre jóvenes librecambistas y militares aliados de los artesanos. ¿Cómo se llamaron los dos bandos? → Gólgotas y draconianos: Verificación de datos: uncertain. Answer (Gólgotas and draconianos) and the split are right. I could not verify the fun fact that draconianos got the name for defending harsh punishments like the death penalty. The origin of the nickname is usually explained differently, so check it.
- **q-7791** (19th-century) Con la Constitución de Rionegro de 1863, cada estado tenía su propio presidente, sus propias leyes y hasta su ejército. ¿Cómo se llama ese sistema? → El federalismo: Overlaps approved q-7090 ("Con la Constitución de 1886, el país dejó de ser federal. ¿Qué nombre oficial adoptó entonces?"). That question says outright that the country was federal before 1886, which is this question's answer. This question's hint 3 is the same 1886 fact from the other side. Anyone who has seen q-7090 knows the answer here, so keep only one of the two.
- **q-7835** (indigenous-myths-and-folk-beliefs) Es un agüero: se golpea una mesa o una puerta con los nudillos y se dice «toco madera». ¿Para qué se hace? → Para no salarse: None of the image candidates fits the question, and no new search is allowed. The slot needs a photo of a hand knocking on a wooden table or door; a search like "knuckles knocking wood table" might find one. No se encontró una imagen adecuada para esta pregunta.
- **q-7880** (19th-century) Según la tradición, ¿desde qué época se juega el tejo en Colombia? → Desde antes de la llegada de los españoles: All six media candidates show the Vasco da Gama Bridge in Lisbon. The search for "tejo" matched the Portuguese name of the Tagus River instead of the Colombian game. None fits, and no new search is allowed. The slot needs a new search such as "tejo Colombia cancha" or "tejo mecha Boyacá". No se encontró una imagen adecuada para esta pregunta.
- **q-7890** (fruits) Mira la foto: así se cultivan el maracuyá y la granadilla, sobre alambres. ¿Qué tipo de planta son? → Enredaderas: No candidate clearly shows a passion-fruit or granadilla vine growing on a wire trellis, and the question says "Mira la foto: así se cultivan… sobre alambres". A new search can't be run, so the media slot needs a clear photo of a maracuyá/granadilla emparrado (e.g. "passion fruit vine trellis wires"). No se encontró una imagen adecuada para esta pregunta.
- **q-7932** (tv-shows-and-series) En «100 colombianos dicen», dos familias adivinan las respuestas más comunes de una encuesta a cien personas. ¿De qué país viene ese formato? → Estados Unidos: None of the media candidates works. The piezo and electromagnetic buzzers (2–6) are electronic components and have nothing to do with a TV game show. Candidate 1 is a Japanese bus stop button with Japanese text, which points players towards the wrong option 'Japón'. The question text itself is fine; it only needs a new image, such as a TV game show studio set. No se encontró una imagen adecuada para esta pregunta.
- **q-7935** (writers-and-books) Lo escribió el boyacense Jairo Aníbal Niño en los años ochenta y se lee muchísimo en los colegios colombianos. ¿Qué es «La alegría de querer»? → Un libro de poemas de amor para niños: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-7938** (writers-and-books) El bogotano Ivar Da Coll escribe e ilustra libros álbum para los más chiquitos, casi sin palabras. ¿Qué animal protagoniza su serie más famosa? → Un chigüiro: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).

## Question axes

- move: analogy 5, cause_effect 9, count 2, estimate 6, identify 23, made_of 11, name_concept 17, odd_one_out 11, origin 15, purpose 20, sequence 7, when 15, who 18, word_meaning 18
- stimulus: detail 1, map_outline 1, none 150, photo 25
- clue: completion 5, direct 69, riddle 17, scenario 27, three_facts 59
- answer_kind: group 28, number 10, person 27, place 25, thing 36, time 17, word 34
- lens: body_senses 7, colombia 42, educational_media 20, everyday 22, history 23, language 30, nature 6, pop_culture 11, popular_science 1, school 8, science_news 2, university 5

## Dropped by the pipeline

- 19th-century-2: overlap like q-0119: ¿Cómo se llama la famosa novela romántica del colombiano Jorge Isaacs (1867)? → María: En esta hacienda del Valle del Cauca ambientó Jorge Isaacs su novela más famosa. ¿Cuál es? → María
- 19th-century-5: overlap like q-6928: ¿En qué símbolo patrio de Colombia aparece escrito el lema «Libertad y Orden»? → En el escudo: Tiene un cóndor arriba, una granada, dos cuernos llenos de monedas y frutas, y una cinta que dice «Libertad y Orden». ¿Qué símbolo patrio es? → El escudo de Colombia
- 19th-century-6: overlap like q-0567: La mula es a la yegua y el burro como la atemoya es a la chirimoya y… ¿a qué otra fruta? → El anón: Es hija de un burro y una yegua, es muy terca y en el siglo XIX cargaba el café por las montañas de Colombia. ¿Qué animal es? → La mula
- 19th-century-7: overlap like q-7668: En «El renacuajo paseador», Rin Rin canta en la fiesta de doña Ratona. ¿Quiénes llegan de repente y acaban con la fiesta? → Unos gatos: Rin Rin Renacuajo salió muy elegante aunque su mamá le dijo que no saliera. ¿A dónde fue? → A la casa de doña Ratona
- 19th-century-12: overlap like q-7003: A sus seguidores les dicen 'godos', su color es el azul y lo fundaron en 1849 Mariano Ospina Rodríguez y José Eusebio Caro. ¿Qué partido es? → Partido Conservador: El Partido Liberal colombiano nació en 1848. ¿Qué partido nació un año después y se volvió su gran rival? → El Partido Conservador
- 19th-century-13: overlap like q-6865: El himno de Colombia empieza con una gloria «inmarcesible». Si una flor fuera inmarcesible, ¿qué le pasaría? → Nunca se marchitaría: El himno de Colombia empieza «¡Oh gloria inmarcesible!». ¿Qué significa «inmarcesible»? → Que nunca se marchita
- 19th-century-16: overlap like q-7280: Si visitas la Quinta de San Pedro Alejandrino, en Santa Marta, conoces el lugar donde Simón Bolívar pasó sus últimos días. ¿En qué año fue? → 1830: En esta hacienda Simón Bolívar firmó, en diciembre de 1830, su última proclama a los colombianos. ¿Qué lugar es? → La Quinta de San Pedro Alejandrino
- banknotes-and-coins-1: overlap like q-7006: El billete colombiano de Gabriel García Márquez vale 50 000 pesos. ¿Cuántas lucas son? → 50: En Colombia le dicen «diez lucas» y es un solo billete: el que trae la selva amazónica por detrás. ¿Cuál es? → El billete de 10 000
- banknotes-and-coins-5: overlap like q-0010: ¿Qué río del Meta es conocido como 'el río de los cinco colores'? → Caño Cristales: Soy un río de la sierra de La Macarena, en el Meta. Una planta bajo el agua me pinta de rojo y salgo en el billete de 2000. ¿Quién soy? → Caño Cristales
- banknotes-and-coins-8: overlap like q-0427: En Colombia, ¿cómo le dicen a una persona muy tacaña, que no presta ni un lápiz? → Codo: Nunca invita, siempre «se le olvidó» la billetera y cuenta hasta las monedas de 50. En Colombia le dicen «agarrado». ¿Qué quiere decir? → Tacaño
- brands-and-products-7: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Las galletas Festival son como estas: dos galletas redondas y algo en la mitad. ¿Qué tienen en la mitad? → Crema dulce
- brands-and-products-12: overlap like q-5213: Estos son patacones, como los que se comen en toda Colombia. ¿De qué están hechos? → Plátano verde: Estos son platanitos, el mecato crocante de paquete. ¿De qué están hechos? → Plátano verde
- carnivals-and-fairs-3: overlap like q-0186: Mira este acercamiento: ¿qué comida colombiana es? → Empanada: ¿Cómo se llama la comida frita de masa de maíz, en forma de media luna, rellena de papa y carne, que venden en todas las ferias? → Empanada
- carnivals-and-fairs-8: hard fail: correct 5, unambiguous 4, no_giveaway 1, no_overlap 4: Las cometas que se elevan cada agosto en el festival de Villa de Leyva tienen ese nombre porque se parecen a algo con cola larga que cruza el cielo. ¿A qué? → A un cometa del espacio
- carnivals-and-fairs-14: overlap like q-7259: En el desfile del martes de Carnaval en Barranquilla, unas «viudas» lloran a un personaje que «murió» de tanto parrandear. ¿Quién es? → Joselito Carnaval: Me paso cuatro días de parranda, el martes de carnaval «me muero» de cansancio y viudas de mentira lloran en mi entierro. ¿Quién soy? → Joselito Carnaval
- christmas-and-special-dates-6: overlap like q-6013: Maizena is a fine white powder made from corn, sold in many countries, and many people use its name for any cornstarch. What do cooks mainly use it for? → Thickening sauces and puddings: Es un polvo blanco y finito, muchos lo conocen como Maizena y en diciembre no puede faltar en la natilla. ¿Para qué se le echa? → Para espesarla
- christmas-and-special-dates-9: overlap like q-5120: Es la prenda insignia de los boyacenses, se teje en telar en Nobsa y abriga en el frío del altiplano. ¿De qué está hecha la ruana tradicional? → De lana de oveja: Las ruanas de Boyacá se tejen con algo que nos da este animal. ¿Qué es? → La lana
- club-football-1: overlap like q-7604: A comienzos de los años 50, la liga colombiana jugó por fuera de la FIFA y fichó estrellas como Alfredo Di Stéfano. ¿Cómo se llama esa época? → El Dorado: El argentino Adolfo Pedernera fue la primera gran estrella extranjera que fichó Millonarios, en 1949. ¿Cómo se llamó esa época de cracks en Colombia? → El Dorado
- club-football-17: overlap like q-7086: Esta estatua gigante de bronce homenajea al Pibe Valderrama, junto al estadio de su ciudad natal. ¿Dónde está? → Santa Marta: Nació en Santa Marta, brilló en Unión Magdalena, Millonarios y Junior, y en 1987 fue el primer colombiano elegido mejor futbolista de América. ¿Cuál es su apodo? → El Pibe
- fruits-4: overlap like q-7167: Mira la foto: ¿qué postre es este, que en Colombia se vende en vasito en la calle? → Fresas con crema: En los puestos de carretera de Sopó y La Calera venden fresas picadas en vasito con algo blanco y dulce encima. ¿Qué es? → Crema
- fruits-5: overlap like q-7774: En los fríjoles antioqueños, ¿cómo se llama el guiso de tomate y cebolla que se les sirve encima? → Hogao: Aguacate es a guacamole como tomate y cebolla picados y sofritos son a… → Hogao
- fruits-6: overlap like q-0327: En Colombia, ¿qué te piden cuando te dicen «no dé papaya»? → Que no te descuides ni des ventaja: En Colombia dicen 'no hay que dar papaya'. ¿Cuál de estas cosas NO es dar papaya? → Guardar la plata en un lugar seguro
- fruits-16: overlap like q-7046: Estás colando el tinto en un colador de tela. ¿Cómo se llama el café molido y mojado que queda adentro? → La borra: Mira la foto: en muchas casas colombianas el tinto se cuela en un colador como este. ¿De qué está hecho el filtro? → De tela
- home-school-and-paperwork-9: overlap like q-6828: «Popote» es a México como ¿qué palabra es a Colombia? → Pitillo: Viene pegado a la cajita de jugo, es delgado y hueco, y en Colombia le decimos pitillo. ¿Para qué sirve? → Para tomar el jugo
- home-school-and-paperwork-10: overlap like q-0265: En Colombia, ¿de qué color es la caneca para residuos aprovechables, como plástico y papel limpios? → Blanca: Tiene una bolsa adentro, a veces se abre con pedal, y cuando te toca sacar la basura la vacías. ¿Cómo se llama en Colombia? → La caneca
- hosts-actors-and-comedians-12: overlap like q-7759: ¿Qué actor fue Pedro Coral Tavera en «Pedro el escamoso»? → Miguel Varoni: Soy un pícaro presumido, medio país imitó mi baile y en 2001 Miguel Varoni me dio vida en la televisión. ¿Quién soy? → Pedro Coral
- independence-1: overlap like q-7142: Cartagena se ganó el apodo de «La Heroica» por resistir un largo sitio en 1815. ¿Contra quiénes? → Las tropas españolas de Pablo Morillo: Crucé el Atlántico al frente del mayor ejército que España mandó a América, rendí Cartagena tras un largo sitio y el rey me llamó «el Pacificador». ¿Quién soy? → Pablo Morillo
- independence-15: overlap like q-5112: Me fueron a pedir prestado para adornar una cena en honor a Villavicencio, mi dueño se negó y la pelea terminó en revuelta. ¿Qué soy? → El florero de Llorente: En Colombia, cuando alguien dice que un pequeño incidente fue «el florero de Llorente», ¿qué quiere decir? → Que fue la excusa que desató un problema mayor
- indigenous-myths-and-folk-beliefs-9: overlap like q-6798: Es ropa interior, es del color del sol y se estrena la noche del 31 de diciembre. ¿Para qué es este agüero colombiano? → Para atraer la buena suerte: En Colombia, ¿qué se pone mucha gente debajo de la ropa para recibir el Año Nuevo con buena suerte? → Calzones amarillos
- indigenous-myths-and-folk-beliefs-12: overlap like q-5040: Anaco, chumbe, ruana y poporo: ¿cuál de estos NO es una prenda de vestir tradicional? → El poporo: Los hombres koguis lo reciben al hacerse adultos, lo llevan siempre y lo frotan con un palito mientras piensan. ¿Qué es el poporo? → Un calabacito con cal
- languages-6: overlap like q-5085: San Andrés es famosa por su mar de los siete colores, en el Caribe. ¿Cuál de estas islas colombianas NO está en el mar Caribe? → Malpelo: ¿Cuál es esta isla del Caribe colombiano, famosa por su mar de siete colores? → San Andrés
- languages-9: overlap like q-7059: Boyacomán hace reír como un campesino de Boyacá, y como buen boyacense trata a todos con mucho cariño. ¿Qué palabra usa en vez de «usted»? → Sumercé: Le digo «sumercé» a todo el mundo, me abrigo con ruana y en mi tierra quedan Villa de Leyva y el lago de Tota. ¿Quién soy? → Un boyacense
- national-team-15: overlap like q-6580: Before every World Cup, teams from each part of the world play each other for about two years, home and away. What for? → Winning a place at the World Cup: En las Eliminatorias sudamericanas juegan las 10 selecciones de Sudamérica, todos contra todos y de ida y vuelta. ¿Qué se gana en ellas? → Un cupo al Mundial
- natural-parks-and-ecosystems-0: overlap like q-6629: Rangers protect wild animals, trees and trails. Where do most of them work? → In national parks: En el Tayrona, en Chingaza o en Amacayacu, ellos vigilan la fauna, cuidan los senderos y les explican las reglas a los visitantes. ¿Quiénes son? → Los guardaparques
- natural-parks-and-ecosystems-13: overlap like q-7159: La Ciénaga Grande de Santa Marta fue el primer humedal colombiano protegido por la Convención Ramsar. ¿En qué año se firmó ese tratado en Irán? → 1971: El río Bita, en Vichada, fue declarado en 2018 sitio Ramsar. ¿Qué tipo de ecosistemas busca proteger esa designación? → Los humedales
- olympic-medallists-0: overlap like q-7648: Recibí los Juegos Olímpicos de 1972, y allí Colombia ganó sus primeras medallas: una plata en tiro y dos bronces en boxeo. ¿Quién soy? → Múnich: Colombia ganó sus primeras medallas olímpicas en Múnich 1972. ¿Cuántas medallas ganó allí? → 3
- olympic-medallists-11: overlap like q-7650: ¿Cuál de estas ciudades colombianas NUNCA ha sido sede de los Juegos Centroamericanos y del Caribe? → Cali: ¿Cuántas veces ha sido Colombia sede de los Juegos Centroamericanos y del Caribe? → 4
- olympic-medallists-16: overlap like q-7376: ¿En qué puesto llegó Rigoberto Urán, el ciclista de Urrao, en la prueba de ruta de los Juegos Olímpicos de Londres 2012? → Segundo: Nací en Urrao, Antioquia, de niño vendí lotería y en Londres 2012 gané la plata olímpica en la carrera de ruta. ¿Quién soy? → Rigoberto Urán
- other-sports-14: overlap like q-7076: Mis carros tienen una sola silla y las ruedas por fuera, corro en las calles de Mónaco y un bogotano ganó allí en 2003. ¿Qué categoría de carreras soy? → La Fórmula 1: ¿Qué piloto colombiano ganó el Gran Premio de Mónaco de Fórmula 1 en 2003? → Juan Pablo Montoya
- painters-sculptors-and-museums-17: overlap like q-0112: ¿Qué artista colombiano es famoso por pintar y esculpir figuras muy voluminosas, 'gorditas'? → Fernando Botero: Mira la foto: ¿qué artista colombiano hizo esta escultura? → Fernando Botero
- places-and-monuments-4: overlap like q-7737: En el conjunto vallenato hay un objeto al que le dicen «trinche». ¿Qué es? → El raspador de la guacharaca: Mira la foto de cerca: este instrumento del vallenato se toca raspándolo con un trinche. ¿Cómo se llama? → Guacharaca
- places-and-monuments-6: overlap like q-5135: Cada abril, en Valledupar, los mejores acordeoneros se pelean mi corona tocando paseo, merengue, son y puya. ¿Quién soy? → El Rey Vallenato: Mira la foto: cada año, en el festival más famoso de Valledupar, acordeoneros como este compiten por un título. ¿Cuál? → Rey Vallenato
- places-and-monuments-8: overlap like q-7712: El hip hop tiene cuatro elementos: el rap, el DJ, el breakdance y otro que convirtió la Comuna 13 de Medellín en un museo al aire libre. ¿Cuál? → El grafiti: Mira este detalle: son escaleras eléctricas al aire libre en un barrio de Medellín que hoy recibe turistas de todo el mundo. ¿Qué arte cubre sus muros? → Grafitis
- places-and-monuments-9: overlap like q-0103: ¿Qué pueblo indígena de Colombia inspiró la leyenda de El Dorado, en la laguna de Guatavita? → Los muiscas: Mira la foto de esta laguna redonda de Cundinamarca. ¿Qué pueblo indígena hacía aquí la ceremonia en que un cacique cubierto de oro se bañaba? → Los muiscas
- places-and-monuments-15: duplicate like q-6829: Mira la foto: chocolate caliente con queso derretido adentro. ¿De qué ciudad colombiana es una costumbre famosa? → Bogotá: Mira la foto: es el aeropuerto El Dorado, que lleva el nombre de la famosa leyenda del oro. ¿En qué ciudad está? → Bogotá
- plants-and-flowers-9: overlap like q-5141: Este paisaje con frailejones sale en el billete de 5000. ¿Por qué es tan importante para ciudades como Bogotá? → Porque guarda y da el agua que toman: Están por encima de los 3000 metros, tienen frailejones que atrapan la neblina y un suelo que es como una esponja. ¿Para qué les sirven los páramos a ciudades como Bogotá? → Les dan el agua que toman
- plants-and-flowers-11: overlap like q-5013: ¿Cómo se llama la sopa bogotana de pollo, tres clases de papa, mazorca y guascas? → El ajiaco: Mira la foto: esta hierba se llama guasca. ¿Para qué se usa en Bogotá? → Para darle sabor al ajiaco
- plants-and-flowers-14: overlap like q-0008: ¿Cuál es la flor nacional de Colombia? → La orquídea: Colombia es el país del mundo con más especies de un tipo de flor, y una de ellas es la flor nacional. ¿De qué flor hablamos? → Orquídeas
- pre-columbian-cultures-14: overlap like q-7256: Mira de cerca: estas prendas azules se ven en el mercado de los martes de Silvia, Cauca. ¿Qué pueblo indígena las lleva? → Los misak: Viven en Silvia, Cauca, usan ruana azul y sombrero de ala corta, y se llaman a sí mismos misak. ¿Con qué otro nombre se les conoce? → Guambianos
- pre-columbian-cultures-16: overlap like q-7247: Estas estatuas de piedra de San Agustín, en el Huila, tienen hasta unos 2000 años. ¿Para qué las tallaron? → Para acompañar y custodiar tumbas: Mira de cerca esta estatua del Parque Arqueológico de San Agustín. ¿En qué departamento está ese parque? → Huila
- brands-and-products-13: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Abres un paquete de De Todito en el descanso. ¿Qué encuentras adentro? → Una mezcla de pasabocas
- carnivals-and-fairs-5: hard fail: correct 4, unambiguous 3, no_giveaway 3, no_overlap 4: En la Feria de Cali, ¿qué desfile revive los personajes, oficios y costumbres de la ciudad de antes? → El Cali Viejo
- christmas-and-special-dates-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Un festivo se pasa para el lunes, se junta con el sábado y el domingo, y la gente se va a pasear tres días. ¿Cómo le dicen en Colombia? → Un puente
- club-football-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En los años 80, el América de Cali ganó varias Ligas colombianas seguidas. ¿Cuántas? → 5
- fruits-7: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: El babaco viene de los Andes de Ecuador, se cultiva en el sur de Colombia y al cortarlo parece una estrella de cinco puntas. ¿Qué NO tiene por dentro? → Semillas
- fruits-17: overlap like q-7892: Estás comiendo guanábana y le sacas las pepas negras. ¿Para qué le sirven las pepas a la planta? → Para que nazcan plantas nuevas: En la costa se hace jugo de melón. ¿Qué hay que sacarle del centro antes de licuarlo? → Las pepas
- home-school-and-paperwork-16: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: En muchos apartamentos colombianos, ¿cómo se llama el espacio junto a la cocina donde está la lavadora? → La zona de ropas
- languages-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ya no le queda ningún hablante nativo y sobrevive en viejos documentos y palabras sueltas, como el muysccubun de los muiscas. ¿Cómo se llama una lengua así? → Lengua extinta
- national-team-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es vecino de Colombia, su selección también juega de amarillo y hace de local a más de 2800 metros de altura. ¿De qué país es esa selección? → Ecuador
- painters-sculptors-and-museums-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Está en el Parque Bicentenario de Medellín, guarda historias de víctimas del conflicto armado y promueve la paz. ¿Cómo se llama este museo? → Museo Casa de la Memoria
- painters-sculptors-and-museums-10: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: En Barranquilla hay un museo con salas sobre la gente, la naturaleza y la música de toda la costa norte. ¿Cómo se llama? → Museo del Caribe
- painters-sculptors-and-museums-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ignacio Gómez Jaramillo estudió en México y en 1938 pintó la historia de los Comuneros en el Capitolio Nacional. ¿De qué arte fue pionero en Colombia? → El muralismo
- plants-and-flowers-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: La Organización Internacional del Cacao pone casi todo el cacao de Colombia en una categoría especial por sus notas frutales y florales. ¿Cuál? → Cacao fino de aroma
- plants-and-flowers-3: overlap like q-5008: Estás viendo las miles de láminas de flores pintadas a mano por la Real Expedición Botánica. ¿Quién dirigió esa expedición? → José Celestino Mutis: Está en Bogotá, tiene un «Tropicario» con plantas de selva y una parte de páramo con frailejones. ¿Qué lugar es? → El Jardín Botánico José Celestino Mutis
- pre-columbian-cultures-3: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: Mira esta canoa tradicional de los ríos de Colombia. ¿Cómo se hace? → Con un solo tronco de árbol ahuecado
- pre-columbian-cultures-4: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: En San Agustín hay una estatua llamada «El Doble Yo»: una figura con otra encima. ¿Qué representa, según los arqueólogos? → Un chamán con su doble animal
- pre-columbian-cultures-6: overlap like q-7386: Mira esta mochila de muchos colores. ¿Quiénes la tejen tradicionalmente? → Las mujeres wayuu: Mira de cerca el tejido de esta mochila. ¿De qué departamento es típica? → La Guajira
- rhythms-dances-and-instruments-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Son baladas viejas de Sandro, Leo Dan o Camilo Sesto que sonaban en la radio de la casa. ¿Cómo se le dice en Colombia a esa música? → Música de plancha
- rhythms-dances-and-instruments-17: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: La parranda es al vallenato como … es a la cumbia. → La cumbiamba
- salsa-and-tropical-music-10: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: La salsa choke nació entre jóvenes de Cali y sus coreografías se volvieron virales en redes. ¿Qué mezcla este ritmo? → Salsa con ritmos urbanos y del Pacífico
- writers-and-books-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Cada 23 de abril, los colegios de Colombia hacen izadas de bandera, leen el Quijote y recuerdan a Cervantes. ¿Qué se celebra ese día? → El Día del Idioma
- writers-and-books-16: overlap like q-7152: Rafael Pombo lo publicó en Nueva York en 1867, por encargo de la editorial Appleton, con versiones de rimas infantiles inglesas. ¿Qué libro es? → «Cuentos pintados para niños»: Me publicaron en Nueva York poco después de los «Cuentos pintados», y mi título promete enseñar a portarse bien. ¿Qué libro soy? → «Cuentos morales para niños formales»
- rhythms-dances-and-instruments-2: overlap like q-7720: «Ay, mi llanura», la canción que le canta a paisajes como este, es hoy el himno del Meta. ¿Quién la compuso? → Arnulfo Briceño: Estás en un acto oficial en Villavicencio y suena «Ay mi llanura», considerada el himno del Meta. ¿Quién la compuso? → Arnulfo Briceño
- rhythms-dances-and-instruments-3: overlap like q-7428: Estás en la Batalla de Flores del Carnaval de Barranquilla y pasa la carroza más grande y adornada. ¿Quién va encima saludando? → La reina del carnaval: La Batalla de Flores es el gran desfile de carrozas y comparsas de una fiesta colombiana. ¿De cuál? → El Carnaval de Barranquilla
- rhythms-dances-and-instruments-11: overlap like q-7430: La gaita colombiana es un tubo de cactus cardón, con cabeza de cera de abejas y una pluma de pato; hay gaita macho y hembra. ¿Qué tipo de instrumento es? → De viento: En un conjunto tradicional de gaitas de la costa Caribe, ¿cuántas gaitas suenan? → 2
- rhythms-dances-and-instruments-12: overlap like q-7088: El tiple suena en muchos conjuntos colombianos. ¿Cuál de estos conjuntos NO lo lleva normalmente? → El conjunto vallenato: ¿Cuál de estas agrupaciones colombianas NO lleva clarinete? → Un conjunto vallenato
- rhythms-dances-and-instruments-15: overlap like q-7466: Mira este cuatro, el instrumento del joropo llanero. ¿A qué grupo de instrumentos pertenece? → De cuerda: Es como una guitarra pequeña, acompaña al arpa en el joropo y su nombre es un número. ¿Por qué se llama cuatro? → Porque tiene cuatro cuerdas
- rivers-seas-and-islands-6: overlap like pre-columbian-cultures-6: Mira de cerca el tejido de esta mochila. ¿De qué departamento es típica? → La Guajira: Completa: los arhuacos son a la Sierra Nevada como los wayuu son a… → La Guajira
- rivers-seas-and-islands-7: duplicate like q-7749: Mira esta ciénaga, también llamada de Tesca: el aeropuerto queda entre ella y el mar. ¿Junto a qué ciudad está? → Cartagena: Mira esta playa famosa, Playa Blanca, en la isla de Barú. ¿De qué ciudad sale la gente en lancha para llegar a ella? → Cartagena
- rivers-seas-and-islands-8: overlap like q-7112: Esta isla rocosa del Pacífico colombiano es Patrimonio de la Humanidad. ¿Por qué animales es famosa? → Tiburones: Buceas en Malpelo, famoso por sus manadas de tiburones martillo. ¿Cuál de estos animales que podrías ver NO es un pez? → El delfín
- rivers-seas-and-islands-9: overlap like q-5105: Santa Marta, la ciudad más antigua de Colombia, fue fundada en 1525. ¿Qué conquistador la fundó? → Rodrigo de Bastidas: Mira esta bahía. La ciudad que la rodea, fundada en 1525, es la más antigua de Colombia que sigue en pie. ¿Cuál es? → Santa Marta
- rivers-seas-and-islands-10: overlap like q-7089: Hoy casi todas las púas para puntear la bandola o el tiple son de plástico, pero antes se hacían con el caparazón de un animal. ¿Cuál? → La tortuga carey: Mira esta tortuga marina de los arrecifes del Caribe colombiano, con pico en punta como de halcón. ¿Cómo se llama? → La tortuga carey
- salsa-and-tropical-music-16: overlap like q-6975: El inglés Quantic y Mario Galeano crearon Ondatrópica en 2012 y grabaron el primer disco en los míticos estudios de Discos Fuentes. ¿En qué ciudad? → Medellín: En 1934, en Cartagena, Antonio Fuentes fundó una empresa que luego se instaló en Medellín. ¿A qué se dedicaba? → A grabar y vender discos
- scientists-and-inventors-6: overlap like q-5241: Hoy hay pico y placa en tu ciudad. ¿Qué parte de la placa del carro miras para saber si puede salir? → El último número: Mira la foto. En ciudades como Bogotá, Medellín y Cali hay pico y placa. ¿Para qué sirve? → Para que haya menos trancones
- scientists-and-inventors-13: overlap like q-7397: Rodolfo Llinás cuenta que la larva de la ascidia, un animal marino, se 'come' su propio cerebro. ¿Qué hace justo antes? → Se pega a una roca y deja de moverse: Nací en Bogotá, dediqué mi vida a estudiar el cerebelo, la parte del cerebro que nos ayuda con el equilibrio, y fui profesor en la Universidad de Nueva York. ¿Quién soy? → Rodolfo Llinás
- traditional-games-7: overlap like q-1020: ¿Quiénes fueron los primeros en llegar a adorar al niño Jesús, la misma noche en que nació? → Los pastores: En la novena, todos cantan «Tutaina, tuturumá». Según la letra, ¿quiénes vienen a adorar al Niño? → Los pastores de Belén
- tv-shows-and-series-15: overlap like q-7708: María Elvira Arango presenta «Los Informantes», el programa de crónicas de Caracol Televisión. ¿En qué año se estrenó? → 2013: ¿Qué periodista ha sido la cara de «Los informantes», el programa de crónicas de Caracol, desde su estreno en 2013? → María Elvira Arango
- tv-shows-and-series-16: overlap like q-2826: In the blind auditions of The Voice, coaches sit with their backs to the singer. How many coaches are there in most versions? → 4: En «La Voz Colombia», los entrenadores escuchan de espaldas y giran la silla si les gusta la voz. ¿Cómo se llama esa etapa? → Audiciones a ciegas
- writers-and-books-6: overlap like q-5138: Rafael Pombo hizo su propia versión en español de la rima infantil inglesa «Little Bo-Peep». ¿Cómo se llama su poema? → Pastorcita: Perdí mis ovejas y no sé por dónde andarán; me dicen que no me enoje, que ellas solitas volverán. ¿Quién soy? → Pastorcita
