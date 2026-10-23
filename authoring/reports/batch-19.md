# batch-19

Made by `qgen batch` on 2026-10-23 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): hosts-actors-and-comedians, olympic-medallists, typical-dishes, writers-and-books, fruits, drinks, regional-speech, places-and-monuments, brands-and-products, banknotes-and-coins, symbols-of-departments-and-cities, carnivals-and-fairs, mountains-and-landscapes, independence, indigenous-myths-and-folk-beliefs, natural-parks-and-ecosystems, tv-shows-and-series, street-food-and-bakery, animals, vallenato, cycling, rhythms-dances-and-instruments, sweets-and-desserts, salsa-and-tropical-music, plants-and-flowers, scientists-and-inventors, regions-and-departments
- Merged: 177 (q-7425…q-7601)
- Approved: 157
- Needs work: 20
- Dropped by the pipeline: 84
- Reviewed by: claude-opus-5-5
- Claude calls: 442, about $57.48 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-17, batch-18; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-17 | batch-18 | batch-19 |
|---|---|---:|---:|---:|
| source locale |  | es | es | es |
| drafts |  | 269 | 286 | 261 |
| skipped slots |  | 217 | 200 | 225 |
| dropped |  | 54 | 70 | 84 |
| drop rate | ≤ 20.0 % | 20.1 % ✗ | 24.5 % ✗ | 32.2 % ✗ |
| dropped: hard fail correct |  | 2 | 1 | 2 |
| dropped: hard fail unambiguous |  | 0 | 1 | 1 |
| dropped: hard fail no_giveaway |  | 14 | 16 | 15 |
| dropped: overlap |  | 38 | 51 | 66 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 1 | 1 | 0 |
| merged |  | 215 | 216 | 177 |
| approved |  | 194 | 198 | 157 |
| needs_work |  | 21 | 18 | 20 |
| needs_work rate | ≤ 20.0 % | 9.8 % ✓ | 8.3 % ✓ | 11.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.3 % ✓ | 1.9 % ✓ | 4.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.9 % ✓ | 0.5 % ✓ | 1.1 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.9 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.9 % ✗ | 0.9 % ✓ | 1.7 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.2 % ✓ | 5.1 % ✓ | 5.1 % ✓ |
| media: no pick in review 1 |  | 41 | 43 | 31 |
| media: recovered by research |  | 34 | 33 | 23 |
| media: no pick at record |  | 7 | 10 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.5 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 15.6 % ✓ | 18.5 % ✓ | 26.4 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 45.9 % ✗ | 43.4 % ✗ | 32.8 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.75 ✗ | 0.83 ✓ | 1.13 ✓ |
| approved 11–15 |  | 40 | 42 | 27 |
| top move | ≤ 25.0 % | 14.4 % ✓ | 14.8 % ✓ | 16.4 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 84.2 % | 86.1 % | 80.2 % |
| values stimulus |  | 5 | 4 | 5 |
| top clue | ≤ 60.0 % | 38.1 % ✓ | 40.7 % ✓ | 44.1 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 27.4 % ✓ | 25.5 % ✓ | 24.9 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.9 % ✓ | 25.0 % ✓ | 27.7 % ✗ |
| values lens |  | 11 | 11 | 12 |
| media share | 15.0 %–50.0 % | 15.8 % ✓ | 13.9 % ✗ | 19.8 % ✓ |
| mean fun | ≥ 3.40 | 3.38 ✗ | 3.35 ✗ | 3.33 ✗ |
| cost $ |  | $59.96 | $64.49 | $53.84 |
| $ per approved | ≤ $0.35 | $0.31 ✓ | $0.33 ✓ | $0.34 ✓ |
| calls |  | 443 | 455 | 382 |
| calls per approved |  | 2.28 | 2.30 | 2.43 |
| wall time h |  | 1.91 | 1.89 | 1.49 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 53 (0 %)
- Major among review needs work: 3 of 7 (43 %)
- Problems by kind: giveaway 5 (1 major), overlap 1 (1 major), media 4 (2 major), difficulty 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.64

Major findings on approved questions:

None.

## Needs work

- **q-7425** (animals) Soy verde, tengo una cresta de púas en la espalda y una papada, y me asoleo en los árboles de los parques de Cartagena y Santa Marta. ¿Quién soy? → La iguana: No adequate decorative image: candidates 1 and 2 are a nativity scene in Cartagena, Spain, and candidate 3 is an old photo of the Puerta de San José with a tram, which also appears to be in Cartagena, Spain. None shows the parks of Cartagena or Santa Marta in Colombia. A new search is needed, e.g. "Cartagena Colombia park trees" or "Santa Marta park". No se encontró una imagen adecuada para esta pregunta.
- **q-7431** (carnivals-and-fairs) El papel maché se hace con papel periódico y engrudo de harina y agua; después se seca y se pinta. ¿Para qué se usa en los carnavales? → Para hacer figuras y máscaras: The fact check is 'uncertain' about the fun fact's claim that the Carnaval de Negros y Blancos figures can be over 10 m tall: sources mostly give about 8 m high by 16 m long, and I can't confirm the 10 m figure myself. Replace it with the safer version: 'Las carrozas del Carnaval de Negros y Blancos pueden medir hasta 8 metros de alto y 16 de largo.' Verificación de datos: uncertain. The fun fact says the Carnaval de Negros y Blancos figures 'pueden medir más de 10 metros de alto'. Sources say the floats reach about 8 m high by 16 m long. One 14 m float was also reported. The answer and wrong answers are fine.
- **q-7439** (cycling) Nairo Quintana y Egan Bernal ganaron el Giro de Italia. ¿Más o menos cuántas etapas tiene esa carrera? → 21: The fun fact says the Giro leader wears a pink jersey, and that is the answer to q-7098 ("maglia rosa" → the race leader's jersey). Players who see this fun fact get q-7098 for free. Replace the fun fact with a different true Giro fact, for example that the winner's trophy is the spiral Trofeo Senza Fine, or that the race sometimes starts outside Italy.
- **q-7455** (independence) Pedro Romero era herrero, había nacido en Cuba y armó a los artesanos de su barrio. Con su presión, en 1811 su ciudad se declaró independiente de España del todo. ¿Qué ciudad? → Cartagena: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-1923, PD-US-expired).
- **q-7474** (natural-parks-and-ecosystems) Soy un parque nacional del Cauca, cerca de El Tambo. En mis bosques de niebla vive el zamarrito multicolor, un colibrí que casi no se encuentra en ningún otro lugar del mundo. ¿Qué parque soy? → Munchique: Hint 1 ("No soy un volcán ni estoy en el Valle del Cauca ni en Antioquia") rules out all three wrong answers at once: Puracé is a volcano, Farallones de Cali is in Valle del Cauca, and Las Orquídeas is in Antioquia. That gives the answer away before hint 3. Hint 1 should be replaced with a vague hint that doesn't eliminate any option, for example one about the Pacific-facing slope of the Western Cordillera or the rainy cloud forest.
- **q-7477** (olympic-medallists) Óscar Figueroa alza una barra de 20 kilos con un disco rojo de 25 kilos en cada lado. ¿Cuántos kilos levanta en total? → 70: The media slot has no candidates and no new search is allowed, so the question has no image. The text itself is fine: 20 + 2×25 = 70, and the plate colours in the fun fact are correct. It needs a manual image search, for example 'red bumper plate barbell' or 'weightlifting barbell plates'. No se encontró una imagen adecuada para esta pregunta.
- **q-7481** (places-and-monuments) El Estadio El Campín, casa de Millonarios y Santa Fe, está en la ciudad marcada en el mapa. ¿Cuál es? → Bogotá: Hints 1 and 2 already give the answer away for Colombian players: 'the largest city in the country' and 'where the president works' each mean Bogotá immediately, just like hint 3. Hint 1 should be vague, for example about the stadium's location or the city's cool highland climate without saying it's the biggest, and hint 2 should be only moderately strong. Media candidate 1 is usable but weak: the Colombia inset with the red mark is small, and most of the picture is the shape of the district.
- **q-7493** (regional-speech) En tres de estas ciudades es muy normal oír «¡decime la verdad!» y «decí algo». ¿En cuál NO? → Cartagena: This overlaps too much with approved q-6940 ("Paisa es a «vos» como costeño es a… «tú»") and q-6886 (which group does NOT use «vos»?). The fact that coastal speakers use «tú» instead of voseo is already in the pool, and seeing q-6940 makes this question trivial. Hint 2 ("En la Costa se prefiere el «tú»") also gives the answer away, because Cartagena is the only coastal city among the options.
- **q-7495** (regions-and-departments) Mira el mapa: ¿qué región natural de Colombia está resaltada? → La región Amazónica: None of the essential-image candidates is a map of Colombia with the Amazon region highlighted. #1 is a labelled map of South America, and #2–6 are bilateral locator maps of Colombia with another country. A new search isn't allowed (can_search_again is false), so the map has to be sourced by hand: an unlabelled Colombia map with the Amazon region highlighted, e.g. a 'Colombia natural regions' map edited down to that one region. No se encontró una imagen adecuada para esta pregunta.
- **q-7511** (cycling) Mira la foto: este aparatico va en el manubrio de la cicla. ¿Para qué sirve? → Para avisar que vas pasando: The only candidate showing a bike bell is #2. The bell there is small and in the background, and the brake lever is the most visible thing on the handlebar, so "Para frenar la cicla" would look like a fair answer. The other candidates show a gear hub, a mission bell, bell towers and a foxglove flower. The slot needs a clear close-up of a bicycle bell on a handlebar (e.g. a search for "bicycle bell handlebar"), but no new search is allowed here. No se encontró una imagen adecuada para esta pregunta.
- **q-7516** (fruits) Buena parte se exporta a Europa. ¿Qué departamento de Colombia tiene más hectáreas sembradas de aguacate Hass? → Antioquia: Hint 1 gives the answer away. "One of the largest and most populated departments" fits only Antioquia among the options, since Caldas, Risaralda and Tolima are all much smaller. Hint 2 (coffee plus flowers) also points straight at Antioquia. Hint 1 should be vague, for example about the Andean highlands where Hass grows. Hint 2 should not name a trait only Antioquia has among the options.
- **q-7532** (places-and-monuments) Mira la foto: este domo de Bogotá es Maloka. ¿Qué clase de lugar es? → Un museo interactivo de ciencia: No candidate shows the Maloka dome in Bogotá, and no new search is possible. Candidates 2–4 and 6 show ayahuasca malocas at Centro Takiwasi in Peru, 1 is a Florentino y el Diablo statue, and 5 is a portrait photo of a glass pyramid behind a 'Huerta Uaque Maloka' sign, not the dome the question names. Either find a real Commons photo of the Maloka dome, or make the image illustrative and drop 'Mira la foto: este domo'. No se encontró una imagen adecuada para esta pregunta.
- **q-7537** (regional-speech) En Boyacá y Cundinamarca es muy común pedir «cuchuco de trigo». ¿Qué es el cuchuco? → Una sopa: No candidate shows the question's setting, the Colombian Andean highlands. #1 is a South Dakota prairie with an English 'Waterfowl Production Area' sign, and #2 and #3 are NASA satellite views (a coastline and a river floodplain in Patagonia). No new search is allowed, so the slot needs a new search such as 'Boyacá countryside' or 'Colombian ruana'. No se encontró una imagen adecuada para esta pregunta.
- **q-7551** (vallenato) Escucha: este tambor alto, que se toca con las manos, se sumó al conjunto vallenato moderno. ¿Cuál es? → La conga: None of the audio candidates is a conga recording. They are a gated-reverb drum-kit demo, a reggae kit beat, a talking drum, an Indian street drummer, a brass band and an udu. A new search isn't allowed, so the essential audio slot can't be filled. It needs a solo conga recording (open hand strokes), for example from Freesound. No se encontró una imagen adecuada para esta pregunta.
- **q-7567** (scientists-and-inventors) Nací en Bogotá, estudié ingeniería en Cambridge y en 1958 hice un marcapasos tan grande que funcionaba con una batería de carro. ¿Quién soy? → Jorge Reynolds: Verificación de datos: uncertain. Answer Jorge Reynolds is right, and so are Bogotá, Cambridge, 1958, the car battery, the Ecuadorian priest and the 18 extra years. The weight is inconsistent across sources: 'unos 45 kilos' (hint) vs 'más de 50 kilos', 'casi 50' and 55 kg.
- **q-7570** (street-food-and-bakery) Con esta grasa blanca se fríen los chicharrones en muchas cocinas colombianas. ¿Qué es? → Manteca de cerdo: No candidate shows pork lard. #1 is jars of goose lard ('Gęsi smalec') with readable labels, and #2–#6 are unrelated (a lab apparatus drawing, ceramic jars, a sketchbook page and a drape illustration). A new search isn't allowed. Re-search with something like 'pork lard block' or 'rendered pork fat'. If nothing clear turns up, change the slot to decorative (for example 'chicharron frying pan') and drop 'esta' from the question. No se encontró una imagen adecuada para esta pregunta.
- **q-7582** (symbols-of-departments-and-cities) Jesús María Ocampo, fundador de Armenia en 1889, era conocido por todos como «el…». ¿Cómo termina su apodo? → Tigrero: Hint 2 gives the answer away. It says Ocampo was a hunter in the forest who neither carried goods nor looked for treasure, which rules out Arriero and Guaquero by name. Of the two options left, only Tigrero is about hunting, since a hachero cuts wood. Hint 2 should be rewritten to stay vague, for example about how dangerous and brave his work in the wild forest was, without saying "cazador" or ruling options out.
- **q-7588** (tv-shows-and-series) Si te ríes con 'La pelota de letras', de Andrés López, ¿la infancia de quiénes estás recordando? → De quienes crecieron en los años 70 y 80: Hint 1 gives the answer away. It says the generation was in its twenties and thirties in 2004, so you can work out that they were children in the 70s and 80s. Hint 1 should be vague, for example about the show's style or its success, without ages or dates that point to the decade. Hint 2 also nearly settles it (colour TV and the first video game consoles, but no internet) and could be the strong hint instead.
- **q-7594** (typical-dishes) Abres la nevera en la mañana y vas a hacer calentado paisa. ¿Qué dos sobras de ayer no pueden faltar? → Fríjoles y arroz: Hint 2 ("un grano blanco que va en casi todo almuerzo") clearly points to rice, and only the correct option has rice, so the second hint gives the answer away. Hint 2 should stay vague (e.g. about the meal they come from, like the previous day's lunch), and the rice/bean clues should move into hint 3.
- **q-7600** (writers-and-books) ¿En qué año se publicó la novela que empieza «Era yo niño aún cuando me alejaron de la casa paterna»? → 1867: Overlaps approved q-0119, whose question text reads "la famosa novela romántica del colombiano Jorge Isaacs (1867)". It states the exact fact this question asks (the year María was published), so seeing one gives away the other. Either drop this question, or remove "(1867)" from q-0119 and keep this one.

## Question axes

- move: analogy 3, cause_effect 6, count 6, estimate 5, identify 29, made_of 21, name_concept 22, odd_one_out 11, origin 16, purpose 12, record 4, sequence 4, when 10, who 9, word_meaning 19
- stimulus: detail 5, map_outline 6, none 142, photo 22, sound 2
- clue: completion 6, direct 78, riddle 13, scenario 19, three_facts 61
- answer_kind: group 25, number 13, person 19, place 26, thing 44, time 10, word 40
- lens: body_senses 14, colombia 49, educational_media 8, everyday 22, history 23, language 19, nature 20, pop_culture 2, popular_science 1, school 16, science_news 1, university 2

## Dropped by the pipeline

- banknotes-and-coins-2: overlap like q-7006: El billete colombiano de Gabriel García Márquez vale 50 000 pesos. ¿Cuántas lucas son? → 50: Salgo en el billete morado de Colombia, nací en Aracataca y me inventé un pueblo llamado Macondo. ¿Quién soy? → Gabriel García Márquez
- brands-and-products-1: overlap like q-1576: Soy un snack triangular, crujiente y anaranjado, y nací para no desperdiciar sobras en un restaurante de Disneyland. ¿De qué estoy hecho? → Maíz: Los Choclitos, ese mecato crocante que viene en paquete, ¿de qué están hechos principalmente? → Maíz
- carnivals-and-fairs-1: overlap like q-7259: En el desfile del martes de Carnaval en Barranquilla, unas «viudas» lloran a un personaje que «murió» de tanto parrandear. ¿Quién es? → Joselito Carnaval: En Barranquilla, una multitud llora a gritos alrededor de un muñeco acostado en un ataúd: es el entierro de Joselito. ¿Cuándo pasa? → El martes de carnaval
- carnivals-and-fairs-4: overlap like q-0192: ¿De qué región de Colombia es el currulao, ese ritmo que se toca con marimba y tambores? → La región Pacífica: Este ritmo del Pacífico colombiano se toca con marimba de chonta, cununos y guasá, y tiene su propio festival en Tumaco. ¿Cuál es? → El currulao
- carnivals-and-fairs-7: overlap like q-2050: Según los Evangelios, ¿en qué río bautizó Juan el Bautista a Jesús? → El río Jordán: Mi día es el 24 de junio. En el Huila y el Tolima celebran mi fiesta con bambuco, junto a la de San Pedro. Bauticé a Jesús en el río Jordán. ¿Quién soy? → San Juan
- carnivals-and-fairs-12: overlap like q-7325: En las fiestas campesinas de Colombia se improvisan coplas. ¿Cuántos versos tiene una copla tradicional? → 4: Estás en el Festival Nacional de la Trova, en Medellín: dos trovadores se lanzan estrofas improvisadas. ¿Cuántos versos tiene cada estrofa? → 4
- drinks-1: overlap like q-3996: Chocolate starts in pods like this one. In which rainforest did this tree first grow wild? → The Amazon: Mira de cerca: ¿de qué fruto partido es este interior blanco lleno de semillas? → Mazorca de cacao
- drinks-4: overlap like q-0863: Cena especial con toda la familia, abrazos a las doce y regalos debajo del árbol la noche del 24 de diciembre. ¿Cómo se llama la noche en la que pasa todo eso? → Nochebuena: En Colombia, la Nochebuena se celebra con natilla, buñuelos, chocolate y regalos del Niño Dios. ¿Qué es la Nochebuena? → La noche del 24 de diciembre
- drinks-8: overlap like q-7014: Viene en un vaso con dos compartimientos y tú lo mezclas antes de comer. Además del yogur, ¿qué trae el Bon Yurt? → Cereal: Mira de cerca: el Bon Yurt de Alpina trae cereal aparte para mezclarlo con esto. ¿Qué es? → Yogur
- fruits-1: overlap like q-0397: Mira la foto: ¿cómo se llama este dulce típico de la costa colombiana? → Cocadas: Es un dulce redondo que venden las palenqueras en Cartagena; lo hay blanco o tostado con panela. ¿Cuál es su ingrediente principal? → Coco rallado
- independence-0: overlap like q-6924: El 20 de julio de 1810 en Santafé, un comerciante español no quiso prestar un florero y estalló la pelea. ¿Quién era? → José González Llorente: La tienda de José González Llorente, la del famoso florero, quedaba en una esquina de la Plaza Mayor de Santafé. ¿Cómo se llama hoy esa plaza? → Plaza de Bolívar
- independence-14: overlap like q-7366: En 1819 nació un país cuyo escudo tenía dos cuernos de la abundancia y un haz de lanzas. ¿Qué países de hoy lo formaban? → Colombia, Venezuela, Ecuador y Panamá: El 28 de noviembre de 1821, Panamá se independizó de España. ¿A qué se unió enseguida por voluntad propia? → La Gran Colombia
- indigenous-myths-and-folk-beliefs-0: overlap like q-6918: Completa el dicho: “Yo no creo en brujas, pero…” → de que las hay, las hay: Completa el dicho que repiten las abuelas colombianas: «Yo no creo en…, pero de que las hay, las hay». → Brujas
- indigenous-myths-and-folk-beliefs-5: overlap like q-0465: La aguapanela se hace con panela. Pero, ¿de qué se hace la panela? → Del jugo de la caña de azúcar: Tienes gripa y la abuela te prepara aguapanela caliente con limón. ¿Qué es la panela? → Un bloque de dulce de caña
- mountains-and-landscapes-1: overlap like q-6804: Bajas de Bogotá a Melgar, la 'tierra caliente' favorita de los rolos. ¿Más o menos cuál es la temperatura promedio allá? → Unos 27 °C: Melgar, Girardot y Neiva están a menos de 1000 metros de altura y pasan de 24 °C. ¿En qué piso térmico están? → Cálido
- mountains-and-landscapes-5: overlap like q-0945: Estás explorando una cueva: una estalactita crece desde el techo y una estalagmita desde el suelo. Cuando por fin se tocan, ¿qué forman? → Una columna: En las cuevas de Santander hay formaciones que cuelgan del techo, hechas gota a gota por agua con caliza durante miles de años. ¿Cómo se llaman? → Estalactitas
- natural-parks-and-ecosystems-1: overlap like q-6629: Rangers protect wild animals, trees and trails. Where do most of them work? → In national parks: Patrullan los parques nacionales de Colombia, orientan a los visitantes y vigilan que nadie cace ni tale árboles. ¿Cómo se llama este oficio? → Guardaparques
- olympic-medallists-10: overlap like q-5167: Óscar Figueroa ganó oro olímpico en pesas y, como despedida, dejó sus zapatos sobre la tarima. ¿En qué ciudad fue? → Río de Janeiro: Allí Caterine Ibargüen, Óscar Figueroa y Mariana Pajón ganaron oro olímpico, y desde un cerro la vigila el Cristo Redentor. ¿Qué ciudad es? → Río de Janeiro
- olympic-medallists-13: overlap like q-7075: En este deporte, ¿qué colombiana ganó bronce olímpico en Londres 2012 y plata en Río 2016? → Yuri Alvear: Nací en Jamundí, Valle del Cauca. Me pongo el judogui y fui tres veces campeona mundial en la categoría de 70 kilos. ¿Quién soy? → Yuri Alvear
- places-and-monuments-3: overlap like q-0174: ¿En qué parque nacional, cerca de Santa Marta, está la famosa playa de Cabo San Juan? → Parque Tayrona: Vivieron en la Sierra Nevada de Santa Marta, construyeron la Ciudad Perdida y un famoso parque de playas lleva su nombre. ¿Qué pueblo indígena es? → Los tayronas
- places-and-monuments-4: overlap like q-6973: Si un preso escapaba de la antigua cárcel de la isla Gorgona, tenía que nadar hasta el continente. ¿A qué distancia aproximada queda la costa? → Unos 35 kilómetros: La isla Gorgona, en el Pacífico, hoy es parque nacional y allí llegan ballenas jorobadas. Hasta 1984, ¿qué funcionaba en ella? → Una cárcel
- plants-and-flowers-0: overlap like q-5013: ¿Cómo se llama la sopa bogotana de pollo, tres clases de papa, mazorca y guascas? → El ajiaco: Crecen como maleza, se venden secas en la plaza y sin ellas un bogotano dice que la sopa «no sabe a nada». ¿En qué plato no pueden faltar las guascas? → El ajiaco santafereño
- regional-speech-2: overlap like q-6887: En el departamento resaltado en este mapa tratan de «usted» hasta a los hijos y a la pareja, con un tono fuerte y directo. ¿Cuál es? → Santander: En chistes y telenovelas, ¿de qué departamento son los personajes que hablan «golpeado», tan fuerte que parece que regañaran? → Santander
- regional-speech-4: overlap like q-7255: Es un departamento frío de montaña, sus campesinos usan ruana y en pueblos como Nobsa tejen bufandas de lana. ¿Cuál es? → Boyacá: «Truje» por «traje» se decía en tiempos de Cervantes, hoy suena a abuelo campesino y se oye en tierra de ruana y papa. ¿En qué departamento? → Boyacá
- regional-speech-8: overlap like q-7010: En Colombia, ¿cuál de estas frases NO quiere decir que alguien está sin plata? → Estoy amañado: Estás en Colombia y te cuentan que tu papá está bravo. ¿Cuál de estas frases NO quiere decir lo mismo? → Está amañado
- regional-speech-14: overlap like q-5119: ¿Qué departamento de Colombia está resaltado en este mapa? → Antioquia: En el departamento resaltado en el mapa todo termina en «pues»: «¡Hágale, pues!», «¡Vamos, pues!». ¿Cuál es? → Antioquia
- regional-speech-16: overlap like q-0498: ¿De qué departamento es típica la lechona, el famoso cerdo relleno? → Tolima: Nací en Ibagué, me encanta la lechona y el tamal de mi tierra, y bailo bambuco en el Festival Folclórico. ¿Qué soy? → Tolimense
- regions-and-departments-1: overlap like q-0420: Mira la foto: ¿cómo se llaman estos campesinos que desfilan en Medellín cargando enormes arreglos de flores en la espalda? → Silleteros: Cada agosto en Medellín, los silleteros desfilan cargando en la espalda una silleta llena de… → Flores
- regions-and-departments-2: overlap like q-6979: El sancocho trifásico lleva yuca, papa y plátano, y se cocina en olla grande en los paseos de río. ¿Qué indica la palabra «trifásico»? → Que lleva tres carnes: Mira la foto: ¿cómo se llama esta sopa con trozos de yuca, plátano verde, mazorca y carne? → Sancocho
- regions-and-departments-8: overlap like q-5237: Un barco con contenedores sale de China y llega al puerto de Buenaventura. ¿Qué océano atravesó? → El océano Pacífico: Mira la foto: por este puerto del Pacífico sale buena parte del café colombiano rumbo a Asia. ¿Cuál es? → Buenaventura
- regions-and-departments-12: overlap like q-7091: En la batalla de Ayacucho, José María Córdova gritó: “¡División, armas a discreción, de frente, paso de…!”. ¿Cómo termina? → Vencedores: Nací en Antioquia, a los 25 años grité «¡Armas a discreción, paso de vencedores!» en Ayacucho y un departamento del Caribe lleva mi nombre. ¿Quién soy? → José María Córdova
- carnivals-and-fairs-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: El Carnaval de Barranquilla tiene un desfile aparte, con su propia reina y su propio rey coronados cada año. ¿Quiénes desfilan en él? → Los niños
- independence-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En 1819, en Las Queseras del Medio, José Antonio Páez les gritó a sus lanceros llaneros: «¡Vuelvan caras!». ¿Qué hicieron entonces? → Dejaron de huir y giraron para atacar
- independence-12: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: ¿Cuál de estas batallas NO fue parte de la Campaña Libertadora de 1819? → La batalla de San Mateo
- indigenous-myths-and-folk-beliefs-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: El agüero dice «martes 13, ni te cases ni te embarques». ¿Qué es «embarcarse»? → Subirse a un barco para viajar
- indigenous-myths-and-folk-beliefs-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Un bebé amanece llorando y con fiebre después de una visita. Según la creencia del mal de ojo, ¿quiénes le pudieron «echar el ojo»? → Quienes lo miraron con envidia o admiración
- indigenous-myths-and-folk-beliefs-7: overlap like q-7362: La lengua de los kogui, en la Sierra Nevada, es de la familia chibcha. ¿Qué pueblo le dio nombre a esa familia? → Los muiscas: En 1990, un documental de la BBC mostró a nuestros mamos de la Sierra Nevada de Santa Marta advirtiendo a los «hermanitos menores». ¿Qué pueblo somos? → Los kogui
- mountains-and-landscapes-6: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Las sabanas inundables de los Llanos son planas y se llenan de agua en invierno. ¿Qué plantas las cubren sobre todo? → Pastos y gramíneas
- natural-parks-and-ecosystems-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: ¿Cuál de estos parques nacionales de Colombia NO está en la costa del océano Pacífico? → Old Providence McBean Lagoon
- places-and-monuments-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Mira la foto: esta plaza con iglesia, fuente y balcones de colores es la réplica de un pueblo tradicional, en un cerro de Medellín. ¿Cómo se llama? → El Pueblito Paisa
- regional-speech-1: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En tres de estas ciudades, a un grupo de amigos se le dice «ustedes». ¿En cuál NO? → Madrid
- regional-speech-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: Es una de las expresiones más típicas de Medellín. ¿Qué expresa un paisa cuando dice «¡Ave María, pues!»? → Sorpresa o asombro
- regional-speech-6: overlap like q-7312: El maguaré, el gran tambor de tronco que le da nombre al portal infantil del Ministerio de Cultura, es tradicional de ¿qué pueblo indígena? → Los uitotos: El huitoto es la lengua de un pueblo indígena famoso por el maguaré, un gran tambor de tronco. ¿En qué región colombiana se habla? → La Amazonía
- regional-speech-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Si un paisa dice que está «tragado» de alguien, ¿qué le pasa? → Está enamorado
- regions-and-departments-11: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 4: Mira la foto: ¿a qué región natural de Colombia pertenece este lugar? → La región Insular
- rhythms-dances-and-instruments-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Antes masticaba pasto en un potrero; hoy me raspan y me golpean, y mis dientes flojos castañetean en la música costeña. ¿Qué soy? → La quijada de burro
- salsa-and-tropical-music-10: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: La salsa choke nació en Cali hacia 2010. ¿Qué mezcla? → Salsa, reguetón y ritmos del Pacífico
- street-food-and-bakery-0: overlap like q-7546: El Chocoramo es rectangular, viene en paquete individual y está cubierto de chocolate. ¿Qué tipo de mecato es? → Un ponqué: Completa: en Colombia, «comer mecato» es comer… → Paquetes y dulces entre comidas
- street-food-and-bakery-1: overlap like sweets-and-desserts-4: Mira la foto: es una paleta de agua, de esas que venden en la tienda. ¿Con qué se hace? → Agua, fruta y azúcar: En el parque suena la campanita del paletero. ¿De qué están hechas principalmente las paletas que vende? → Jugo o leche congelados
- street-food-and-bakery-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Hueles el pandebono recién salido del horno y dices «¡qué antojo!». Un antojo es… → Ganas de comer algo especial
- street-food-and-bakery-17: overlap like typical-dishes-1: Mira la foto: esta arepa delgada, blanca y sin sal acompaña casi todas las comidas en una región de Colombia. ¿Cuál? → Antioquia: Es una arepa antioqueña muy delgada, blanca y sin relleno, que acompaña el desayuno paisa. ¿Cómo se llama? → Arepa tela
- sweets-and-desserts-11: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: En algunas veredas de Colombia se oye: "Esta semana hay molienda". ¿Qué significa? → Que se va a moler caña para hacer panela
- symbols-of-departments-and-cities-9: overlap like q-7466: Mira este cuatro, el instrumento del joropo llanero. ¿A qué grupo de instrumentos pertenece? → De cuerda: En la música llanera, junto al arpa y las maracas, suena una guitarrita pequeña que lleva el ritmo. ¿Cuántas cuerdas tiene? → 4
- tv-shows-and-series-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En Caracol, al mediodía y a las 7 de la noche, unos presentadores cuentan lo que pasó en Colombia y el mundo. ¿Qué tipo de programa es? → Un noticiero
- vallenato-5: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Nací a orillas del río Magdalena, lejos de Valledupar, y soy más pausado y cumbiambero que el vallenato guajiro. ¿Qué estilo de vallenato soy? → El estilo bajero
- rhythms-dances-and-instruments-2: overlap like q-7428: Estás en la Batalla de Flores del Carnaval de Barranquilla y pasa la carroza más grande y adornada. ¿Quién va encima saludando? → La reina del carnaval: Este desfile de carrozas abre el Carnaval de Barranquilla. ¿Quién lo encabeza tradicionalmente? → La Reina del Carnaval
- rhythms-dances-and-instruments-13: overlap like q-0479: ¿En qué mes se celebra la Feria de Cali, con su famoso desfile de bailarines de salsa? → Diciembre: Soy un desfile de miles de bailarines con trajes brillantes y zapatos que echan chispas, y cada 25 de diciembre abro la Feria de Cali. ¿Qué soy? → El Salsódromo
- rhythms-dances-and-instruments-15: overlap like q-7325: En las fiestas campesinas de Colombia se improvisan coplas. ¿Cuántos versos tiene una copla tradicional? → 4: El cantador llanero la improvisa en el joropo, la usa para retar a otro en el contrapunteo y rima sus versos pares. ¿Cómo está formada una copla? → Cuatro versos de ocho sílabas
- salsa-and-tropical-music-3: overlap like q-6945: La flauta de millo se toca de lado y su lengüeta se corta en la misma caña. ¿Qué es el millo? → Una planta parecida al sorgo: La caña de millo de la cumbia se toca de lado y suena como un clarinete pequeño. ¿Qué parte, cortada en el mismo tubo, la hace sonar? → La lengüeta
- salsa-and-tropical-music-11: overlap like rhythms-dances-and-instruments-13: Soy un desfile de miles de bailarines con trajes brillantes y zapatos que echan chispas, y cada 25 de diciembre abro la Feria de Cali. ¿Qué soy? → El Salsódromo: La Feria de Cali termina el 30 de diciembre. ¿Qué día arranca con el desfile del Salsódromo? → El 25 de diciembre
- scientists-and-inventors-3: overlap like q-5211: Nací en Cali, llegué a Estados Unidos con 300 dólares y narré en español el aterrizaje del rover Perseverance en Marte. ¿Quién soy? → Diana Trujillo: Soy el vecino de la Tierra, tengo el volcán más grande del sistema solar y la caleña Diana Trujillo ayudó a mandarme un robot. ¿Qué soy? → Marte
- scientists-and-inventors-13: overlap like q-5241: Hoy hay pico y placa en tu ciudad. ¿Qué parte de la placa del carro miras para saber si puede salir? → El último número: Por el pico y placa, ciertos días tu carro no puede salir en las horas de más tráfico. ¿Qué decide cuáles son esos días? → El último número de la placa
- scientists-and-inventors-15: overlap like q-5008: Estás viendo las miles de láminas de flores pintadas a mano por la Real Expedición Botánica. ¿Quién dirigió esa expedición? → José Celestino Mutis: El Jardín Botánico de Bogotá lleva el nombre de quien dirigió la Real Expedición Botánica, desde 1783. ¿Quién fue? → José Celestino Mutis
- scientists-and-inventors-17: overlap like q-5203: En el método madre canguro, creado en Bogotá: la bolsa es a la cría de canguro como ¿qué es al bebé prematuro? → El pecho de la mamá: El método madre canguro, creado en Bogotá, ayuda a los bebés que nacen antes de tiempo. ¿Cómo se les dice a esos bebés? → Prematuros
- street-food-and-bakery-13: overlap like q-6016: This fluffy pink treat in the photo is made almost entirely of one thing. What is it? → Sugar: En los parques y ferias de Colombia venden este dulce en un palito. ¿Cómo se llama? → Algodón de azúcar
- street-food-and-bakery-14: overlap like q-0003: ¿Con qué se hacen tradicionalmente las arepas? → Maíz: La arepa paisa, blanca y sin sal, ¿con qué se hace? → Con maíz
- sweets-and-desserts-4: overlap like street-food-and-bakery-1: En el parque suena la campanita del paletero. ¿De qué están hechas principalmente las paletas que vende? → Jugo o leche congelados: Mira la foto: es una paleta de agua, de esas que venden en la tienda. ¿Con qué se hace? → Agua, fruta y azúcar
- sweets-and-desserts-9: overlap like q-3992: This treat's name comes from Arabic and reached South America with the Spanish. In which country is it a national favorite? → Argentina: Soy dos galletitas suaves pegadas con arequipe, a veces con coco rallado en el borde, y mi nombre viene del árabe. ¿Qué soy? → Un alfajor
- sweets-and-desserts-12: overlap like q-5144: La fundaron dos inmigrantes suizos en Sopó, Cundinamarca, en 1945, y es famosa por el Bon Yurt. ¿Qué marca es? → Alpina: Queda en Cundinamarca, cerca de Bogotá, allí nació Alpina en 1945 y la gente va a comprar arequipe y postres de leche. ¿Qué municipio es? → Sopó
- sweets-and-desserts-14: overlap like q-5227: Mira la foto: este pan de queso y almidón de yuca es típico de una región. ¿De quiénes es tradicional? → De los vallunos: Mira la foto: es un pandebono, que a veces viene relleno de bocadillo. Además de almidón de yuca, ¿qué lleva su masa? → Queso
- sweets-and-desserts-17: overlap like q-6833: Mira la foto: esta fruta de palma se come cocida, con sal y miel. ¿De qué región de Colombia es típica? → El Pacífico: Es el fruto anaranjado de una palma, se cocina con sal y en Cali se vende con miel en las esquinas. ¿De qué región de Colombia es típico? → Región Pacífica
- symbols-of-departments-and-cities-13: overlap like q-0517: En Colombia, ¿cómo les dicen a quienes hablan con 'ajá', 'eche' y '¡qué nota!'? → Costeños: Mira este detalle de un sombrero vueltiao. ¿Cómo les dicen en Colombia a los de la región donde se teje? → Costeños
- tv-shows-and-series-6: overlap like q-7178: En «Yo soy Betty, la fea», Lorna Cepeda interpretó a Patricia Fernández. ¿Qué cosa de ella inspiró su famoso apodo? → Su pelo teñido: Viendo 'Yo soy Betty, la fea': los frenillos son a Betty como ¿qué es a Patricia Fernández, su rival en la oficina? → El pelo teñido
- tv-shows-and-series-17: overlap like q-2826: In the blind auditions of The Voice, coaches sit with their backs to the singer. How many coaches are there in most versions? → 4: En 'La Voz Kids', ¿cómo se llama la primera etapa, en la que los jurados escuchan a los niños sin poder verlos? → Las audiciones a ciegas
- typical-dishes-0: overlap like q-7571: Es maíz blanco pelado y cocido, se sirve con leche y se acompaña con un pedacito de panela o bocadillo. ¿De dónde es típica esta mazamorra? → Antioquia: Se vende en bolsa en la plaza, se deja en remojo la noche anterior y con él se hace la mazamorra. ¿Qué es el maíz pilado? → Maíz sin cáscara, golpeado en pilón
- typical-dishes-1: overlap like street-food-and-bakery-17: Es una arepa antioqueña muy delgada, blanca y sin relleno, que acompaña el desayuno paisa. ¿Cómo se llama? → Arepa tela: Mira la foto: esta arepa delgada, blanca y sin sal acompaña casi todas las comidas en una región de Colombia. ¿Cuál? → Antioquia
- typical-dishes-5: overlap like q-1704: Esta trucha arcoíris es común en los ríos fríos de los Andes, pero no es nativa de allí. ¿De dónde es originaria? → De Norteamérica: Mira la foto: este pescado se cría en estanques de agua fría de montaña y se come mucho en el Oriente antioqueño. ¿Qué es? → Trucha
- typical-dishes-11: overlap like q-5218: El plátano maduro es amarillo con manchas negras y muy dulce. En Colombia se fríe en rodajas largas para el almuerzo. ¿Cómo se llaman? → Tajadas: Estás en un corrientazo y te sirven unas tajadas de maduro, doradas y dulcecitas. ¿De qué se hacen? → Plátano
- typical-dishes-13: overlap like q-0425: Las primeras zanahorias que cultivaron las personas, hace más de mil años en Asia, no eran naranjas. ¿De qué color eran casi siempre? → Moradas: La ensalada de repollo acompaña el corrientazo, lleva el repollo picado finito y una verdura anaranjada rallada. ¿Cuál? → Zanahoria
- typical-dishes-15: overlap like q-7448: En las heladerías colombianas lleva crema de leche, queso rallado y helado encima. ¿Qué va debajo, en trocitos? → Frutas picadas: ¿De qué está hecho el salpicón que venden en las heladerías y en la calle en Colombia? → Frutas picadas en jugo
- typical-dishes-16: overlap like q-5221: En Colombia, el chócolo se asa en la calle con mantequilla y sal, se usa para arepas dulces y no falta en el ajiaco. ¿Qué es? → La mazorca de maíz tierno: Es amarilla, gruesa y dulce, se hace con maíz tierno recién sacado de la mazorca y se sirve con mantequilla y queso. ¿Cómo se llama? → Arepa de chócolo
- vallenato-4: overlap like q-5135: Cada abril, en Valledupar, los mejores acordeoneros se pelean mi corona tocando paseo, merengue, son y puya. ¿Quién soy? → El Rey Vallenato: Completa la lista de los cuatro aires del vallenato: son, paseo, merengue y… → Puya
- writers-and-books-13: overlap like q-7348: El conquistador navarro Pedro de Ursúa fundó la ciudad de Pamplona, en el actual Norte de Santander. ¿En qué año? → 1549: Soy una novela de William Ospina de 2005. Cuento la vida de un conquistador navarro que fundó Pamplona y buscó El Dorado en el Amazonas. ¿Qué novela soy? → Ursúa
- writers-and-books-14: overlap like q-7151: Los primeros cuentos de García Márquez, que luego se reunieron en «Ojos de perro azul», salieron en El Espectador. ¿En qué década? → Los años cuarenta: El premio mundial de libertad de prensa de la UNESCO lleva el nombre de Guillermo Cano. ¿Qué periódico dirigió? → El Espectador
