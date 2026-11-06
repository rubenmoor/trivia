# batch-38

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): sayings, scientists-and-explorers, spanish-cinema, regional-symbols, drinks, team-and-traditional-sports, brands-and-shops, flamenco-and-copla, monuments, childrens-tv, creatures, radio-and-internet, tv-series, legends-and-superstitions, painting-and-architecture, cities-and-towns, tv-shows-and-presenters, money-and-services, al-andalus-and-reconquista, 20th-century, tapas, fiestas, football-clubs, plants-and-climate, comics-and-childrens-books, dress-crafts-and-games, classic-literature
- Merged: 244 (q-12249…q-12492)
- Approved: 230
- Needs work: 14
- Dropped by the pipeline: 60
- Reviewed by: claude-opus-5-5
- Claude calls: 553, about $74.21 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-36, batch-37; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-36 | batch-37 | batch-38 |
|---|---|---:|---:|---:|
| source locale |  | en | de | es-ES |
| drafts |  | 332 | 347 | 304 |
| skipped slots |  | 118 | 139 | 182 |
| dropped |  | 90 | 52 | 60 |
| drop rate | ≤ 20.0 % | 27.1 % ✗ | 15.0 % ✓ | 19.7 % ✓ |
| dropped: hard fail correct |  | 0 | 1 | 3 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 17 | 25 | 22 |
| dropped: overlap |  | 64 | 27 | 31 |
| dropped: duplicate |  | 7 | 0 | 1 |
| dropped: fact-check wrong |  | 2 | 0 | 3 |
| merged |  | 242 | 295 | 244 |
| approved |  | 216 | 265 | 230 |
| needs_work |  | 26 | 30 | 14 |
| needs_work rate | ≤ 20.0 % | 10.7 % ✓ | 10.2 % ✓ | 5.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.3 % ✓ | 2.7 % ✓ | 2.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 1.2 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.4 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.8 % ✓ | 1.7 % ✗ | 2.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 7.0 % ✓ | 5.1 % ✓ | 1.2 % ✓ |
| media: no pick in review 1 |  | 34 | 33 | 37 |
| media: recovered by research |  | 25 | 22 | 35 |
| media: no pick at record |  | 10 | 12 | 3 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 22.0 % ✗ | 9.2 % ✓ | 12.2 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 68.1 % ✓ | 65.3 % ✓ | 63.4 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 2.00 ✗ | 1.25 ✓ | 1.22 ✓ |
| approved 11–15 |  | 54 | 62 | 59 |
| top move | ≤ 25.0 % | 14.5 % ✓ | 14.9 % ✓ | 14.8 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 82.2 % | 79.3 % | 80.3 % |
| values stimulus |  | 5 | 4 | 4 |
| top clue | ≤ 60.0 % | 38.4 % ✓ | 44.7 % ✓ | 45.5 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 21.1 % ✓ | 20.3 % ✓ | 22.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 19.4 % ✓ | 18.3 % ✓ | 24.2 % ✓ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 17.8 % ✓ | 20.7 % ✓ | 19.7 % ✓ |
| mean fun | ≥ 3.40 | 3.55 ✓ | 3.47 ✓ | 3.51 ✓ |
| cost $ |  | $64.45 | $81.47 | $70.75 |
| $ per approved | ≤ $0.35 | $0.30 ✓ | $0.31 ✓ | $0.31 ✓ |
| calls |  | 470 | 562 | 493 |
| calls per approved |  | 2.18 | 2.12 | 2.14 |
| wall time h |  | 1.99 | 2.31 | 1.95 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 57 (0 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 8 (0 major), fact 2 (0 major), media 3 (0 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.46

Major findings on approved questions:

None.

## Needs work

- **q-12254** (20th-century) En julio de 1909 Barcelona ardió así durante la llamada Semana Trágica. ¿Qué desató la revuelta? → El envío de reservistas a la guerra de Marruecos: The question text says «Barcelona ardió así», so the image must show Barcelona burning in 1909. Neither candidate does: #2 shows police arresting people in a street with no fire, and #1 is an unrelated 1885 drawing. Search for a photo of the 1909 fires (for example «Barcelona 1909 burning convent»), or reword the question so it doesn't point at the image with «así». Then #2 could serve as an illustrative image. No se encontró una imagen adecuada para esta pregunta.
- **q-12257** (20th-century) Nació en 1958 en Cataluña, tiene forma de bola y su inventor, Enric Bernat, le puso un palo. ¿Para qué? → Para que los niños no se mancharan las manos: Hints 1 and 2 give the answer away. Hint 1 ("quiénes comen más caramelos") points to children, and the answer is the only option that mentions children. Hint 2 ("los niños podían sujetar el caramelo fácilmente") practically states the answer. Rewrite the hints so they escalate and the first two don't single out the answer, e.g. hint 1 about Bernat watching how people ate sweets and hint 2 about a practical everyday problem.
- **q-12279** (cities-and-towns) Esta gran escultura de Chillida, el «Elogio del Horizonte», corona un cerro junto al mar. ¿En qué ciudad está? → Gijón: Hint 2 («La ciudad es de Asturias, pero no es su capital») solves the question: Gijón is the only Asturian city among the options (San Sebastián is in Gipuzkoa, Santander in Cantabria, A Coruña in Galicia). Hint 2 should be vaguer, for example about Chillida's other seaside work or the city's industrial and port past, without naming the region.
- **q-12298** (comics-and-childrens-books) Es un texto breve, a menudo con rima, que describe algo sin decir su nombre para que lo aciertes. Gloria Fuertes escribió muchas. ¿Cómo se llama? → Una adivinanza: This question gives away the draft q-12409. Its description says «Gloria Fuertes escribió tantos versos para niños…» and its text names her again, while q-12409 asks which Madrid poet, famous for verses for children, wrote «La oca loca». The answer there is Gloria Fuertes, so one question reveals the other. To fix it, drop Gloria Fuertes from this question's description and text, for example by playing on the school or car-trip riddle theme instead. The question is otherwise correct and unambiguous.
- **q-12308** (creatures) La Virgen de Covadonga es a Asturias como la Virgen de la Candelaria es a… → Canarias: This overlaps approved q-9901 in the same subcategory. That question's text says the Tenerife Guanches identified their goddess with the Virgen de Candelaria, which gives this answer (Canarias) away straight off. Separately, hint 2 («pastores guanches») gives the answer away, because the Guanches are known only as the native people of the Canary Islands.
- **q-12331** (fiestas) Mira la foto: en los Sanfermines de Pamplona, cada mañana, mucha gente corre así por las calles. ¿Delante de qué animales corren? → Toros: No candidate can serve as the essential photo: every picture shows the bulls, which is the answer. #1 is the encierro with a bull in the street, #2 is a blurred bull, and #3–#6 are the bronze encierro monument full of bulls. No new search is allowed. Also, related q-9945 asks about the encierro and says «desde que salen los toros», which gives this answer away if both are played. No se encontró una imagen adecuada para esta pregunta.
- **q-12386** (al-andalus-and-reconquista) Mira este palacio de una taifa andalusí. Alfonso I el Batallador conquistó en 1118 la ciudad donde está. ¿Cuál es? → Zaragoza: No candidate shows the Aljafería palace itself. Candidates 2–5 show the Convento de Santa Isabel de los Reyes in Toledo, which is one of the wrong options, and 6 is an unrelated church courtyard. Candidate 1 is an Aljafería arch, but it stands in a room of the Museo Arqueológico Nacional, not the palace the question asks you to look at. A new search such as "Aljafería palace Zaragoza" is needed. No se encontró una imagen adecuada para esta pregunta.
- **q-12411** (dress-crafts-and-games) Estás en el patio echando a suertes quién se la queda con «Pito, pito, gorgorito». ¿Cuál de estas NO es otra retahíla para echar a suertes? → «Al pasar la barca»: Verificación de datos: uncertain. 'Zapatito blanco, zapatito azul' is mostly known as a skipping-rope rhyme, though some versions are used for choosing. So the 'wrong answer' may not be clearly a counting-out rhyme, and the answer is ambiguous with 'Al pasar la barca'.
- **q-12420** (flamenco-and-copla) Estás en un tablao y el guitarrista empieza a tocar. ¿Cuántas cuerdas tiene su guitarra flamenca? → 6: This asks the same fact as approved q-0065 («¿Cuántas cuerdas tiene una guitarra normal?» → 6). Hint 2 even says the flamenco guitar has the same number as a normal Spanish guitar, so the tablao setting doesn't make it a different question. Drop it or replace it with a different flamenco fact.
- **q-12427** (monuments) El monasterio de Leyre, en Navarra, fue muy importante para los primeros reyes de Pamplona. ¿Para qué les sirvió? → Como panteón real: Hint 2 gives the answer away. It says the kings didn't live there, didn't hold the Cortes there and didn't imprison anyone there, which rules out all three wrong answers and leaves only «Como panteón real». It should be replaced with a vague hint that rules out nothing, for example one about the monastery's age or its role in the early kingdom.
- **q-12446** (scientists-and-explorers) En 1999, la gallega Chus Lago subió al Everest sin oxígeno embotellado. ¿Qué puesto ocupó entre las mujeres del mundo que lo habían logrado? → La tercera: Verificación de datos: uncertain. Chus Lago's 1999 Everest summit (26 May, north side) is documented, but only a Galician teaching sheet says she was the third woman without oxygen. The Himalayan Database doesn't mention oxygen, and I found no independent source for the ranking. Her 1998 attempt failed.
- **q-12449** (scientists-and-explorers) Karlos Arguiñano es a la cocina como Jesús Calleja es a… → la aventura: Verificación de datos: uncertain. Calleja was born in Madrid (1967) and raised in León, so 'es de León' is loose. I did not check this by search. The answer is fine.
- **q-12455** (tapas) Mira la pezuña de este jamón. ¿De qué animal suele ser el jamón que la tiene así? → Del cerdo ibérico: Overlap: the fun fact (black seal only for 100 % ibérico de bellota) gives away the answer of q-10070 (the seal colour), and hint 2 names the dehesa, the answer of q-10124. Change the fun fact to a different fact (e.g. about the hoof or curing time) and make hint 2 point to acorns/oak woods without the word «dehesa».
- **q-12475** (tapas) Entras en una bodega de La Rioja y huele a barricas de roble. ¿Qué se hace allí? → Vino: Hint 2 («Suele servirse en copa y puede ser tinto, blanco o rosado») gives the answer away: tinto/blanco/rosado names wine outright. It is also stronger than hint 3 («Se hace con uvas»), so the hints don't go from vague to strong. Replace hint 2 with something vaguer (for example about the harvest season or ageing for years), and keep the grapes for hint 3.

## Question axes

- move: analogy 11, cause_effect 11, count 4, estimate 6, identify 36, made_of 20, name_concept 21, odd_one_out 12, origin 27, purpose 15, record 11, sequence 10, when 15, who 30, word_meaning 15
- stimulus: detail 7, map_outline 3, none 196, photo 38
- clue: completion 9, direct 111, riddle 23, scenario 27, three_facts 74
- answer_kind: group 25, number 12, person 44, place 41, thing 50, time 17, word 55
- lens: body_senses 6, educational_media 37, everyday 28, history 59, language 39, nature 12, pop_culture 25, popular_science 4, school 23, university 11

## Dropped by the pipeline

- 20th-century-7: overlap like q-11237: El pintor Salvador Dalí era famoso por llevar algo muy largo y fino, con las puntas retorcidas hacia arriba. ¿Qué era? → El bigote: Mi bigote apunta al cielo como dos agujas, pinté relojes blandos que se derriten y fui la gran estrella del surrealismo. ¿Quién soy? → Salvador Dalí
- al-andalus-and-reconquista-8: overlap like q-0333: Muchas palabras del español que empiezan por 'al-', como 'almohada', 'alfombra' y 'algodón', vienen de un mismo idioma. ¿De cuál? → Árabe: Echas una cucharada de azúcar a la leche. ¿Quiénes nos dejaron la palabra «azúcar»? → Los árabes
- al-andalus-and-reconquista-10: overlap like q-9858: ¿Qué pueblo germánico convirtió Toledo en la capital de su reino en Hispania? → Los visigodos: Tenían su capital en Toledo, su rey Recaredo se hizo católico en el año 589 y su reino cayó con don Rodrigo en 711. ¿Qué pueblo era? → Los visigodos
- al-andalus-and-reconquista-15: overlap like q-1674: Tenía claustro, iglesia y biblioteca, y allí se copiaban libros a mano. ¿Quiénes vivían en una abadía medieval? → Monjes: Vivo en un monasterio y paso horas a la luz de una vela, con pluma y tinta, copiando e ilustrando libros a mano letra a letra. ¿Quién soy? → Un monje copista
- brands-and-shops-5: overlap like q-9994: La morcilla de Burgos es negra y lleva cebolla, especias y sangre. ¿De qué animal es esa sangre? → Del cerdo: Casa Tarradellas empezó en un pueblo cerca de Vic haciendo fuet, un embutido fino y curado. ¿De qué animal es su carne? → Del cerdo
- brands-and-shops-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Soy un muñeco con cara de bebé: me das el biberón, me cambias el pañal y me llamo igual que una colonia infantil famosa. ¿Quién soy? → Nenuco
- childrens-tv-9: overlap like q-11156: Soy una agencia de espías llena de desastres. Mi jefe es el Súper y mis agentes más famosos son Mortadelo y Filemón. ¿Quién soy? → La T.I.A.: Mortadelo se disfraza, Filemón se lleva los golpes y el profesor Bacterio les da inventos que fallan. ¿Para qué agencia trabajan? → La T.I.A.
- classic-literature-14: overlap like q-9942: El 23 de abril, día de San Jorge, las calles se llenan de puestos y la gente se regala rosas y libros. ¿Dónde es típica esta costumbre? → En Cataluña: Estás en Barcelona un 23 de abril y las calles se llenan de puestos de libros y rosas. ¿Qué santo se celebra ese día? → San Jorge
- comics-and-childrens-books-17: overlap like q-8219: Se dice bajito y se repite una y otra vez en una canción muy conocida de Colombia. ¿Para qué se usa «arrurrú»? → Para dormir a un bebé: ¿Cuándo se suele cantar una nana a un bebé? → A la hora de dormir
- creatures-1: overlap like q-8398: Cuentan en los pueblos que a medianoche pasa por la calle una fila silenciosa de figuras con velas, rezando. ¿Quiénes son? → Almas de difuntos: En Galicia también me llaman Estadea. Salgo de noche por los caminos y nadie quiere cruzarse conmigo. ¿Qué soy? → Una procesión de almas de difuntos
- creatures-3: overlap like q-9903: El trasno es un duende travieso que esconde cosas, cambia los muebles de sitio y no deja dormir. ¿De qué comunidad es su leyenda? → Galicia: Son brujas, se las espanta con el conjuro de la queimada y, según el dicho, «haberlas, haylas». ¿De dónde son las meigas? → Galicia
- dress-crafts-and-games-5: overlap like q-11173: Mira este traje de lunares y volantes. ¿Para qué se lo pone la gente en Andalucía? → Para ir a la feria: ¿De qué región de España es típico el traje que lleva esta muñeca? → De Andalucía
- dress-crafts-and-games-6: overlap like q-9941: Vas vestido de blanco y, cuando suena el chupinazo a mediodía del 6 de julio, te atas al cuello un pañuelo rojo. ¿Dónde estás? → En Pamplona: Miles de personas vestidas así, de blanco y con pañuelo rojo al cuello. ¿En qué fiesta están? → En San Fermín
- drinks-10: overlap like q-5044: Se le echa agua y café molido, se pone a hervir o se enchufa, y de ella sale el tinto de la mañana. ¿Qué es? → La cafetera: Mira de cerca: ¿qué objeto de cocina es este, que se pone al fuego en muchas casas de España cada mañana? → La cafetera italiana
- drinks-11: duplicate like q-6902: Este animal es plato de Navidad en muchas casas colombianas. ¿De qué continente es originario? → América: Mira el fruto de la foto: de sus semillas sale el chocolate. ¿De qué continente lo trajeron a España? → De América
- fiestas-1: overlap like q-7428: Estás en la Batalla de Flores del Carnaval de Barranquilla y pasa la carroza más grande y adornada. ¿Quién va encima saludando? → La reina del carnaval: Me eligen cada año en el pueblo, llevo banda y a veces corona, y desfilo en la carroza principal con mis damas. ¿Quién soy? → La reina de las fiestas
- fiestas-13: overlap like q-10073: Es la noche de San Juan y estás en la playa. ¿Cuál de estas cosas NO es una tradición de esa noche? → Comer doce uvas: Mira la foto: la noche del 23 de junio se encienden hogueras así en playas y plazas. ¿A qué santo está dedicada? → San Juan
- legends-and-superstitions-3: overlap like q-0859: Somos doce, pequeñitas y redondas, y nos comen una por cada campanada de la medianoche del 31 de diciembre. Según la tradición, ¿qué representa cada una de nosotras? → Un mes del año: Son doce, se comen en Nochevieja al ritmo del reloj y prometen un buen año. ¿Con qué nombre se conocen? → Las uvas de la suerte
- legends-and-superstitions-5: overlap like fiestas-13: Mira la foto: la noche del 23 de junio se encienden hogueras así en playas y plazas. ¿A qué santo está dedicada? → San Juan: La noche del 23 de junio, en muchos lugares de España se saltan hogueras como esta. ¿Qué santo da nombre a esa noche? → San Juan
- legends-and-superstitions-7: overlap like q-9883: En Nochevieja, la tele da las campanadas desde el reloj más famoso de España. ¿En qué plaza de Madrid está? → La Puerta del Sol: Son doce, suenan a medianoche del 31 de diciembre y la tele las emite desde un reloj de Madrid. ¿Cómo se llaman? → Las campanadas
- money-and-services-6: overlap like q-11223: Mira esta moneda española de 2 euros. ¿Cuántas estrellas rodean la cara del rey? → 12: Mira la cara española de esta moneda de 1 euro. ¿Quién sale en ella? → Felipe VI
- monuments-3: overlap like q-3791: I'm a ribbed seashell. Hikers walking the Way of Saint James to Santiago de Compostela hang me on their backpacks. What am I? → Scallop shell: Si ves este símbolo en un mojón o en el suelo de un pueblo, ¿a quiénes está guiando? → A los peregrinos
- monuments-5: overlap like q-6291: This is the home stadium of FC Barcelona. Which superstar scored more goals for the club than anyone else? → Lionel Messi: Mira este estadio de Barcelona. ¿Qué futbolista ha marcado aquí más goles que nadie? → Lionel Messi
- monuments-13: overlap like q-9864: ¿Quiénes pintaron estos bisontes en la cueva de Altamira? → Cazadores del Paleolítico: Mira esta pintura de hace más de 14 000 años, en una famosa cueva de Cantabria. ¿Qué animal es? → Un bisonte
- radio-and-internet-6: overlap like q-11250: Un streamer dice: «¡Hoy hago directo!». ¿Qué significa? → Que lo ves mientras pasa: Ibai, TheGrefg y AuronPlay la usan, tiene un chat para el público y su logo es morado. ¿Para qué sirve Twitch? → Para emitir vídeos en directo
- regional-symbols-9: overlap like q-9922: Fue el lema de Carlos I, aparece en el escudo de España entre las columnas de Hércules y dio nombre a un hidroavión que cruzó el Atlántico en 1926. ¿Cuál es? → «Plus Ultra»: Carlos V eligió como emblema dos columnas con una cinta y un lema en latín, que siguen en el escudo de España. ¿Qué dice la cinta? → Plus Ultra
- 20th-century-11: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Si le preguntabas a Ángel Nieto cuántos mundiales de motociclismo había ganado, ¿cómo respondía siempre? → «12+1»
- brands-and-shops-17: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: ¿En qué parte de la casa se usa el limpiador Pato WC? → El cuarto de baño
- tv-series-4: hard fail: correct 3, unambiguous 5, no_giveaway 5, no_overlap 5: ¿Qué negocio tiene Paco en los bajos del edificio de «Aquí no hay quien viva»? → Un videoclub
- tv-series-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En «Amar es para siempre», el tiempo avanza con las temporadas. ¿En qué década empieza la serie? → En los años 60
- childrens-tv-17: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En el doblaje de España de «Los Simpson», ¿cuál de estos nombres NO se usa para nadie de la familia? → Homero
- cities-and-towns-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En Cádiz, cada febrero, grupos llamados chirigotas cantan coplas graciosas por la calle. ¿Qué fiesta es? → El Carnaval
- cities-and-towns-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es la ciudad más poblada de Canarias, tiene la playa de Las Canteras y comparte la capitalidad con Santa Cruz de Tenerife. ¿Cuál es? → Las Palmas de Gran Canaria
- classic-literature-11: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: En esta tragicomedia de Lope de Vega, don Alonso se enamora de doña Inés en la feria de Medina del Campo. ¿Cuál es? → «El caballero de Olmedo»
- comics-and-childrens-books-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Esta editorial barcelonesa del Grupo Zeta nació en 1986, se quedó con los personajes de Bruguera y siguió publicando Mortadelo y Filemón. ¿Cuál es? → Ediciones B
- comics-and-childrens-books-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El botones Sacarino es un chico con flequillo, creado por Ibáñez, que lo pone todo patas arriba en su trabajo. ¿Dónde trabaja? → En la redacción de una revista
- comics-and-childrens-books-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es un edificio dibujado sin fachada, donde ves a la vez a todos sus vecinos, de la azotea a la alcantarilla. Ibáñez lo creó en 1961. ¿Cómo se llama? → 13, Rue del Percebe
- drinks-0: fact-check wrong: Kas was founded in Vitoria in 1956 (some sources say 1954), not the 1950s only loosely; Bitter Kas came in 1966. Fun fact is roughly OK, but 'San Bitter' is also a red, bitter, non-alcoholic aperitif from the maker of a famous orange soda (Sanpellegrino Aranciata), so that wrong answer is arguably valid.: En una terraza pides un aperitivo rojo intenso, amargo y sin alcohol, de la marca de una famosa naranjada. ¿Qué te traen? → Un Bitter Kas
- drinks-5: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Estás en el súper leyendo la etiqueta de una botella de agua mineral natural española. ¿De dónde sale esa agua? → De un manantial
- fiestas-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Corren detrás de la manada, impiden que los toros se den la vuelta y no dejan que nadie los cite por detrás. ¿Qué llevan en la mano los pastores del encierro? → Una vara larga de madera
- flamenco-and-copla-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Nació en 1980, sus premios se llaman Giraldillos y reúne a las grandes figuras del flamenco. ¿Qué festival es? → La Bienal de Flamenco de Sevilla
- football-clubs-0: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Está en Madrid, es la casa del Atlético desde 2017 y acogió la final de la Champions de 2019. ¿Qué estadio es? → El Metropolitano
- football-clubs-4: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 4: Llevé el 10 del Barça y con él levanté cuatro veces la Liga de Campeones. ¿Quién soy? → Lionel Messi
- football-clubs-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Mira este detalle: ¿qué llevan al cuello muchos aficionados cuando van al estadio? → Una bufanda
- monuments-9: fact-check wrong: The answer (1960s; Beatles at Las Ventas on 2 July 1965) is right. But the third hint is wrong. It says «Sonrisas y lágrimas» premiered in Spain in 1970, the year the Beatles split. Sources give a Spanish release of 20 December 1965.: Estás en la plaza de Las Ventas de Madrid, donde una vez tocaron los Beatles. ¿En qué década fue? → En los años 60
- painting-and-architecture-4: overlap like q-1861: Se hace con pedazos de baldosa o cerámica rota, se pega como mosaico y Gaudí lo usó mucho. ¿Cómo se llama esta técnica? → Trencadís: Gaudí cubrió el banco ondulado del Park Güell con trencadís, una técnica del modernismo catalán. ¿De qué está hecho? → De trozos de cerámica rota
- painting-and-architecture-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿En qué año pintó Picasso «Ciencia y caridad», un gran cuadro realista de un médico junto a una enferma? → 1897
- radio-and-internet-7: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: ¿Quiénes son Las Ratitas, el famoso canal infantil de YouTube? → Dos hermanas
- regional-symbols-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La bandera de Ceuta tiene ocho triángulos blancos y negros y, en el centro, el escudo de otro país que gobernó la ciudad. ¿Qué escudo es? → El escudo de Portugal
- sayings-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Según el refrán «A quien madruga, Dios le ayuda», ¿quiénes reciben la ayuda? → Los que se levantan temprano
- scientists-and-explorers-3: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: ¿Qué tipo de tren es este de la foto? → Un tren de alta velocidad
- scientists-and-explorers-4: fact-check wrong: The name change was approved in October 2014, but the 2014 edition was still awarded as 'Príncipe de Asturias'. The first 'Princesa' edition was 2015, so 'antes de 2014' is imprecise.: Ves en la tele la entrega de los Premios Princesa de Asturias en Oviedo. ¿Cómo se llamaban estos premios antes de 2014? → Premios Príncipe de Asturias
- scientists-and-explorers-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Isabel Zendal, primera enfermera de una misión sanitaria internacional según la OMS, zarpó en 1803 hacia América. ¿Quiénes llevaban en su cuerpo la vacuna de la viruela? → Niños huérfanos
- spanish-cinema-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En 2015, la argentina «Relatos salvajes» ganó este Goya, en el que las películas españolas no compiten. ¿Cómo se llama? → Mejor película iberoamericana
- scientists-and-explorers-7: overlap like q-7985: Estás en el mercado de Ráquira y ves cazuelas de barro recién horneadas. ¿Quién las hizo? → Un alfarero: ¿Qué artesano fabrica objetos como este de la foto? → El alfarero
- spanish-cinema-14: overlap like cities-and-towns-16: Es la ciudad más poblada de Canarias, tiene la playa de Las Canteras y comparte la capitalidad con Santa Cruz de Tenerife. ¿Cuál es? → Las Palmas de Gran Canaria: Javier Bardem nació en 1969 en la ciudad de esta foto. ¿Cuál es? → Las Palmas de Gran Canaria
- tv-series-8: overlap like q-11375: Fernando Tejero por «Días de fútbol», Alberto Ammann por «Celda 211» y Miguel Herrán por «A cambio de nada» ganaron este Goya. ¿Cuál? → Mejor actor revelación: Este actor fue Emilio Delgado, el portero de «Aquí no hay quien viva». ¿Cómo se llama? → Fernando Tejero
- tv-shows-and-presenters-4: overlap like legends-and-superstitions-7: Son doce, suenan a medianoche del 31 de diciembre y la tele las emite desde un reloj de Madrid. ¿Cómo se llaman? → Las campanadas: En Nochevieja suenan doce, con cada una te comes una uva y la tele las retransmite en directo. ¿Cómo se llaman? → Las campanadas
- tv-shows-and-presenters-6: overlap like q-9933: Soy periodista y presenté en Telecinco el primer «Gran Hermano» español, en el año 2000, y muchas ediciones más durante unos quince años. ¿Quién soy? → Mercedes Milá: Es una cadena privada que nació en 1990, pertenece a Mediaset y en ella empezó «Gran Hermano» en España en el año 2000. ¿Cuál es? → Telecinco
- tv-shows-and-presenters-10: overlap like q-10035: Estás ante la tele en Nochevieja y, antes de las doce campanadas, suenan los cuartos. ¿Cuántos son? → 4: Suenan justo antes de la primera uva, son cuatro toques dobles del reloj de la Puerta del Sol y despistan a muchos. ¿Cómo se llaman? → Los cuartos
