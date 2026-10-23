# batch-16

Made by `qgen batch` on 2026-10-23 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): plants-and-flowers, salsa-and-tropical-music, conquest-and-colonial-era, regional-speech, natural-parks-and-ecosystems, rhythms-dances-and-instruments, mountains-and-landscapes, home-school-and-paperwork, typical-dishes, club-football, independence, hosts-actors-and-comedians, olympic-medallists, other-sports, fruits, vallenato, popular-and-andean-music, christmas-and-special-dates, ghosts-and-creatures, cycling, drinks, rivers-seas-and-islands, regions-and-departments, animals, national-symbols, words, cities-and-towns
- Merged: 206 (q-6788…q-6993)
- Approved: 186
- Needs work: 20
- Dropped by the pipeline: 65
- Reviewed by: claude-opus-5-5
- Claude calls: 475, about $57.51 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-14, batch-15; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-14 | batch-15 | batch-16 |
|---|---|---:|---:|---:|
| source locale |  | en | en | es |
| drafts |  | 1137 | 955 | 271 |
| skipped slots |  | 645 | 827 | 215 |
| dropped |  | 292 | 273 | 65 |
| drop rate | ≤ 20.0 % | 25.7 % ✗ | 28.6 % ✗ | 24.0 % ✗ |
| dropped: hard fail correct |  | 8 | 0 | 4 |
| dropped: hard fail unambiguous |  | 4 | 2 | 0 |
| dropped: hard fail no_giveaway |  | 51 | 52 | 25 |
| dropped: overlap |  | 220 | 210 | 37 |
| dropped: duplicate |  | 9 | 8 | 0 |
| dropped: fact-check wrong |  | 2 | 1 | 0 |
| merged |  | 845 | 682 | 206 |
| approved |  | 791 | 618 | 186 |
| needs_work |  | 54 | 64 | 20 |
| needs_work rate | ≤ 20.0 % | 6.4 % ✓ | 9.4 % ✓ | 9.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.3 % ✓ | 3.4 % ✓ | 1.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.2 % ✓ | 0.4 % ✓ | 1.5 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.4 % ✗ | 1.3 % ✗ | 0.5 % ✓ |
| needs_work: media | ≤ 10.0 % | 3.0 % ✓ | 4.4 % ✓ | 6.3 % ✓ |
| media: no pick in review 1 |  | 109 | 82 | 36 |
| media: recovered by research |  | 87 | 57 | 24 |
| media: no pick at record |  | 23 | 26 | 13 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.7 % ✓ | 0.9 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.5 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 21.2 % ✗ | 23.8 % ✗ | 14.0 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 57.0 % ✓ | 55.7 % ✓ | 29.2 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 0.99 ✓ | 1.52 ✗ | 1.00 ✓ |
| approved 11–15 |  | 193 | 215 | 25 |
| top move | ≤ 25.0 % | 15.1 % ✓ | 16.3 % ✓ | 14.6 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 76.1 % | 76.2 % | 76.7 % |
| values stimulus |  | 7 | 7 | 5 |
| top clue | ≤ 60.0 % | 45.7 % ✓ | 45.6 % ✓ | 37.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.3 % ✓ | 23.6 % ✓ | 28.6 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 15.4 % ✓ | 19.4 % ✓ | 20.9 % ✓ |
| values lens |  | 12 | 12 | 11 |
| media share | 15.0 %–50.0 % | 23.9 % ✓ | 23.8 % ✓ | 23.3 % ✓ |
| mean fun | ≥ 3.40 | 3.49 ✓ | 3.35 ✗ | 3.32 ✗ |
| cost $ |  | $218.11 | $182.45 | $54.66 |
| $ per approved | ≤ $0.35 | $0.28 ✓ | $0.30 ✓ | $0.29 ✓ |
| calls |  | 1696 | 1417 | 415 |
| calls per approved |  | 2.14 | 2.29 | 2.23 |
| wall time h |  | 4.88 | 3.37 | 2.03 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 54 (2 %)
- Major among review needs work: 5 of 6 (83 %)
- Problems by kind: giveaway 8 (1 major), fact 3 (1 major), media 7 (4 major), difficulty 2 (1 major), style 1 (0 major), other 1 (1 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.86

Major findings on approved questions:

- **q-6878**: fact, difficulty — The answer, "600 millones", is out of date. Asocolflores reported more than 900 million stems for Valentine's 2025 and projected about 980 million for 2026 (Portafolio, Contexto Ganadero, La República). It is still the closest of the four options, but players would learn a figure about 35–40% too low, and the number keeps growing every year. Asking a 6–10-year-old to estimate export volumes in the hundreds of millions is closer to a 9 than a 6. The fun fact (Amor y Amistad in September) and the media are fine. (http://127.0.0.1:8001/review/q-6878)

## Needs work

- **q-6809** (cities-and-towns) ¿En qué década se terminó el Cristo Rey que vigila a Cali desde el cerro Los Cristales? → La década de 1950: No candidate shows Cali's Cristo Rey: 1, 2, 4, 5 and 6 show the Christ the King statue in Świebodzin, Poland, and 3 shows Cristo Rei in Lisbon. No new search is allowed, so the slot can't be filled. Also, hint 2 ("a few years after the Second World War") gives the answer away: with these options, only the 1950s fits. Make it vaguer, e.g. a hint about the 20th century or the city's growth. No se encontró una imagen adecuada para esta pregunta.
- **q-6811** (club-football) Este delantero nacido en el Tolima es el máximo goleador en la historia de la liga colombiana. ¿Quién es? → Dayro Moreno: The media slot is 'essential' with a face photo of Dayro Moreno, but the question text never refers to a photo: a sharp face shot of the answer would just give it away to anyone who recognises him. None of the candidates shows a clear face anyway (1: two Steaua players seen from afar; 2: face cut off; 3: titled Juan Carlos Bedoya; 4–5: distant Xolos action shots). Make the media illustrative instead, with a picture that doesn't show the player, e.g. 'Estadio Palogrande Manizales' or 'Colombian football stadium crowd'. No se encontró una imagen adecuada para esta pregunta.
- **q-6823** (cycling) Mira la foto: en esta subida, el Alpe d'Huez, un colombiano ganó en 1984 la primera etapa del Tour para su país. ¿Quién fue? → Lucho Herrera: No candidate shows the Alpe d'Huez hairpins that the question points to ("Mira la foto: en esta subida"). 1 and 2 show the Col de Sarenne pastoral road with signs, and 3 is a portrait of Pierre Rolland on a podium. A new search can't be run, so this needs a proper hairpin photo (e.g. 'Alpe d'Huez hairpins'). The text itself is fine. No se encontró una imagen adecuada para esta pregunta.
- **q-6824** (cycling) Mira la foto: con una bicicleta como esta, Mariana Pajón ganó dos oros olímpicos. ¿Para qué se usa? → Carreras cortas con saltos y curvas: The essential image must show a BMX race bike, but all six candidates are other bikes: an 1890s safety bicycle, old roadsters, a road racer, a public bike-share station and Dutch city bikes. A new search isn't allowed, so the slot needs a real BMX photo (e.g. 'BMX race bike' or 'BMX bicycle'). No se encontró una imagen adecuada para esta pregunta.
- **q-6827** (drinks) Mira de cerca: ¿cómo se le dice en Colombia a esta bebida dulce llena de burbujas? → Gaseosa: Every image candidate is a branded Coca-Cola bottle or pack with big logos (and #1 has skulls). The note asks for an unbranded close-up of a glass of dark soda with visible bubbles, and none of them shows bubbles. No new search is allowed, so the media slot can't be filled. Try a search like "soda glass bubbles closeup" or "carbonated drink glass". No se encontró una imagen adecuada para esta pregunta.
- **q-6844** (hosts-actors-and-comedians) Juanpis González es un gomelo, le dice «mi papi» a su papá y tiene su programa, «Juanpis Live Show». ¿De qué ciudad es? → Bogotá: Hint 2 gives the answer away: 'la más grande del país' points only to Bogotá, so any Colombian player has the answer before hint 3, which then just repeats it ('la capital'). Hint 2 should hint at the upper-class northern neighbourhoods without naming a fact that only Bogotá has (e.g. drop 'que es la más grande del país').
- **q-6852** (independence) James Rooke, jefe de la Legión Británica, fue herido en el Pantano de Vargas en 1819. ¿Qué tuvieron que amputarle? → Un brazo: The question is about an injury: which body part was cut off a wounded officer. Hint 2 shows him raising the cut-off limb, and the fun fact jokes about his burial. That breaks the Tone rule (never ask about suffering or deaths, nothing gory). Hint 3 ('Lo que le quedó libre fue una mano') is also confusing. The question should be dropped or replaced with a non-injury question about Rooke or the British Legion at Pantano de Vargas, such as which foreign unit he led.
- **q-6853** (independence) El 20 de julio de 1810, este hombre animó a la multitud de Santafé a exigir un cabildo abierto. ¿Quién es? → José Acevedo y Gómez: None of the six candidates is a portrait of Acevedo y Gómez, and most of them print his full name. 1 and 2 are handwritten or typed documents, 3 is a school logo, 4 is a school bus, 5 is a UNAD building and 6 is a Bucaramanga cityscape. Another search isn't allowed. The slot should become illustrative or decorative, for example a colonial Bogotá plaza or the Casa del Florero, as the rater suggested, since few players would recognise his face anyway. No se encontró una imagen adecuada para esta pregunta.
- **q-6860** (mountains-and-landscapes) Completa: por su clima frío, mucha gente de tierra caliente le dice a Bogotá «la…» → Nevera: None of the media candidates shows Bogotá. They are cloudy skylines of Dhaka, Calgary, Kaohsiung (two), London and Atlanta, and no new search is allowed. The slot needs a real Bogotá image, such as a cloudy Bogotá skyline from Monserrate or people in ruanas in Bogotá. No se encontró una imagen adecuada para esta pregunta.
- **q-6864** (national-symbols) Esta es la bandera de un departamento de Colombia. ¿De cuál? → Bolívar: No candidate shows the Bolívar department flag, and the question needs it as essential media. The candidates are Plaza Bolívar scenes, a protest, Palestinian flags and a Cúcuta statue with national flags. No new search is allowed. Supply the Commons SVG 'Flag of Bolívar (Colombia).svg' directly. Also note: hint 2 (walled capital, i.e. Cartagena) already gives the answer away almost as clearly as hint 3. No se encontró una imagen adecuada para esta pregunta.
- **q-6868** (natural-parks-and-ecosystems) ¿A cuántos metros sobre el nivel del mar está, más o menos, el mirador del cerro de Monserrate en Bogotá? → Unos 3150 metros: This repeats approved q-5240, which asks for Monserrate's altitude above sea level with the same answer, "Unos 3150 metros". Drop it or replace it with a different Monserrate fact.
- **q-6877** (plants-and-flowers) Es el segundo domingo de mayo en Colombia y todo el mundo sale a comprar flores. ¿A quién se las regalan? → A las mamás: The date is wrong: Colombia celebrates Mother's Day on the last Sunday of May (law from 1925), not the second Sunday like the USA and Mexico's neighbours. The rater's note confirming the second Sunday is mistaken.
- **q-6879** (plants-and-flowers) Mira esta mota blanca que sale de una planta sembrada en Córdoba y el Tolima. ¿Qué es? → Algodón: The question needs an essential photo of an open white cotton boll, and none of the candidates shows one. The candidates are a boll weevil monument (1, 2), old book illustrations (3, 4), a chart (5) and a textile fragment (6). The slot needs a new search such as "Gossypium open boll" or "cotton boll field". No se encontró una imagen adecuada para esta pregunta.
- **q-6916** (fruits) Mira la foto: en Colombia estas semillas se le echan al tamal y al arroz. ¿Para qué se usan? → Como colorante: None of the candidates shows achiote (Bixa orellana). The sheet has pepper seeds, mustard seeds, pomegranate arils and a milkweed pod. The image is essential ("Mira la foto"), and no new search is allowed. The slot needs a photo of an open achiote pod with its red seeds, for example from a search like "Bixa orellana fruit". No se encontró una imagen adecuada para esta pregunta.
- **q-6931** (olympic-medallists) Ingrit Valencia ganó bronce en Río 2016, fue la primera boxeadora colombiana con medalla olímpica y peleaba en la categoría femenina más liviana de esos Juegos. ¿Cuál era? → Peso mosca: Verificación de datos: wrong. Ingrit Valencia won bronze in Rio 2016 in the women's lightweight (60 kg) category, not flyweight. The 51 kg flyweight hint and the 'lightest category' framing are therefore wrong for her. Peso ligero is listed as a wrong answer but is the true one. The question premise 'más liviana' is also false.
- **q-6936** (plants-and-flowers) Colombia es uno de los mayores exportadores del mundo de esta flor. Mira el detalle: ¿cuál es? → Clavel: No candidate gives the clear photo of a single carnation that this essential slot needs. All three are 19th-century seed-catalogue engravings. #1 and #2 show other flowers, and #3 shows a small drawn carnation crowded in with three other plants under a catalogue banner. Since the text alone also fits roses, the question needs a real close-up photo of a carnation, for example from a search for 'Dianthus caryophyllus flower'. No se encontró una imagen adecuada para esta pregunta.
- **q-6937** (plants-and-flowers) En el Desfile de Silleteros, ¿qué categoría de silleta lleva solo flores en ramilletes, sin figuras ni letreros? → Tradicional: None of the media candidates fits. All six are churches of St Margaret of Antioch in Slovakia and England. The search for 'Santa Elena Antioquia' matched 'Antioch' instead of the Colombian village. No new search is allowed, so the slot needs a new query by hand, for example 'Silleteros parade Medellín' or 'Feria de las Flores Medellín'. Make sure the picture doesn't clearly show a traditional silleta that gives the answer away. No se encontró una imagen adecuada para esta pregunta.
- **q-6945** (rhythms-dances-and-instruments) La flauta de millo se toca de lado y su lengüeta se corta en la misma caña. ¿Qué es el millo? → Una planta parecida al sorgo: The fact check is 'uncertain', and I can't confirm from my own knowledge which plant 'millo' is. Sources disagree: some describe a grass like corn, others sorghum or millet. That makes the answer 'Una planta parecida al sorgo' and hint 3's 'su pariente el mijo' unconfirmable. Also, the question's clues only describe the flute, not the plant, so they don't help players work out the answer. The correct option is longer and more specific than the wrong ones and stands out. Verificación de datos: uncertain. In Colombia 'millo' is often described as a plant similar to corn (maíz) or as sorghum/millet. 'Parecida al sorgo' and the hint about 'su pariente el mijo' are shaky and could not be verified.
- **q-6981** (typical-dishes) Compras maíz peto en la plaza. ¿Cuál de estas preparaciones NO se hace con maíz? → Mote de queso: Hint 1 gives the answer away: it calls the odd one out "a soup", and mote de queso is the only soup among the options (mazamorra, chicha and arepa are not). Hint 2 then names its base, a tuber, which leaves nothing to guess. Hint 1 should say something vaguer, for example about the Caribbean region or its cheese, without naming the dish type. Hint 2 shouldn't name the tuber base. The "suero" pairing in hint 2 is also shaky (it is usually served with white rice) and should be dropped.
- **q-6985** (vallenato) Este instrumento del conjunto vallenato lleva el nombre de un ave de la costa. ¿A qué familia de instrumentos pertenece? → De percusión: None of the candidates shows the guacharaca instrument. They are all Espeletia guacharaca plants (1, 4) or chachalaca birds (2, 3, 5, 6), and no new search is allowed. The question ("Este instrumento…") only works with an essential photo of the instrument. Either find a real photo of a guacharaca with its trinche, or rework the question to name the instrument in the text and use an illustrative image (for example a vallenato ensemble or a caja vallenata). No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 8, cause_effect 8, count 6, estimate 11, identify 30, made_of 6, name_concept 29, odd_one_out 19, origin 25, purpose 15, record 6, sequence 5, when 9, who 11, word_meaning 18
- stimulus: detail 12, map_outline 4, none 158, photo 31, sound 1
- clue: completion 7, direct 77, riddle 14, scenario 42, three_facts 66
- answer_kind: group 41, number 18, person 22, place 21, thing 34, time 11, word 59
- lens: body_senses 11, colombia 33, educational_media 12, everyday 43, history 11, language 25, nature 24, pop_culture 24, school 17, science_news 3, university 3

## Dropped by the pipeline

- christmas-and-special-dates-7: overlap like q-1017: En España, el juego de sacar papelitos y dar un regalo sin revelar a quién te tocó no se llama 'amigo secreto'. ¿Cómo lo llaman allá? → Amigo invisible: En septiembre, para Amor y Amistad, en colegios y oficinas de Colombia juegan al 'amigo secreto'. ¿En qué consiste? → Sortear a quién darle un regalo sin que sepa de quién es
- cities-and-towns-12: overlap like christmas-and-special-dates-4: Vivo en cables larguísimos, me prendo y me apago de colores y en diciembre me cuelgan en balcones y en el alumbrado de Medellín. ¿Qué soy? → Los bombillos navideños: Cada diciembre, Medellín ilumina el río y sus parques como en esta foto. ¿Cómo le dicen los paisas a esta tradición? → Los alumbrados
- cities-and-towns-13: overlap like q-5109: Mira esta estatua de San Agustín. ¿Qué etnólogo alemán hizo las primeras excavaciones científicas allí, en 1913 y 1914? → Konrad Theodor Preuss: Esta figura tallada en piedra, con colmillos de felino, está en un famoso parque arqueológico del Huila. ¿Qué es? → Una estatua de San Agustín
- conquest-and-colonial-era-3: overlap like q-6803: ¿En qué municipio de Cundinamarca está esta catedral, construida dentro de una mina de sal? → Zipaquirá: Mira la foto: esta famosa catedral está excavada dentro de una mina en Zipaquirá. ¿Qué se sacaba de esa mina? → Sal
- conquest-and-colonial-era-17: overlap like q-5015: ¿Qué día celebramos el Grito de Independencia de Colombia? → 20 de julio: Hay desfiles y banderas por todo el país porque celebramos el Grito de Independencia. ¿Qué día es? → El 20 de julio
- cycling-3: overlap like q-5021: Esta carrera ciclística por etapas se corrió por primera vez en 1951 y la ganó Efraín Forero, 'el Indomable Zipa'. ¿Cuál es? → La Vuelta a Colombia: Mira la foto: de esta ciudad era Efraín Forero, ganador de la primera Vuelta a Colombia en 1951. ¿Cuál es? → Zipaquirá
- cycling-12: overlap like q-5021: Esta carrera ciclística por etapas se corrió por primera vez en 1951 y la ganó Efraín Forero, 'el Indomable Zipa'. ¿Cuál es? → La Vuelta a Colombia: Soy la carrera por etapas más antigua del país, y Rafael Antonio Niño me ganó seis veces, más que nadie. ¿Qué soy? → La Vuelta a Colombia
- cycling-17: overlap like q-5188: Cada domingo y festivo, en Bogotá pasa lo que ves en esta foto. ¿Cómo se llama? → La Ciclovía: Para un ciclopaseo en familia por la Ciclovía de Bogotá, con las calles cerradas a los carros, ¿cuándo tienes que salir? → Los domingos y festivos
- drinks-3: overlap like q-0320: En Año Nuevo, ¿cuántas uvas se comen a las doce de la noche? → 12: Es 31 de diciembre, suenan las 12 campanadas y en Colombia todos se comen 12 uvas. ¿Qué empieza en ese momento? → El Año Nuevo
- fruits-1: overlap like q-5213: Estos son patacones, como los que se comen en toda Colombia. ¿De qué están hechos? → Plátano verde: Es aguacate machacado con tomate, cebolla y cilantro, y en Colombia se unta sobre este frito de plátano verde aplastado. ¿Cuál es? → El patacón
- ghosts-and-creatures-1: overlap like q-0483: Según la leyenda, ¿a quién busca la Llorona cuando anda de noche, llorando cerca de los ríos? → A sus hijos: Soy un alma en pena. Vago de noche por las orillas de ríos y quebradas, y mi lamento se oye a lo lejos mientras busco a mis hijos. ¿Quién soy? → La Llorona
- ghosts-and-creatures-6: overlap like q-0281: ¿Cómo se llama eso que le da al cuerpo sin querer, una y otra vez, y que según la gente se quita con un susto o tomando agua? → El hipo: Un buen susto por sorpresa, aguantar la respiración o tomar agua al revés: según las abuelas, son remedios para quitar… → El hipo
- ghosts-and-creatures-17: overlap like q-6801: Ves calabazas con caras talladas y niños disfrazados gritando '¡Triqui triqui!' para pedir dulces. ¿Qué fecha es? → 31 de octubre: Es 31 de octubre en Colombia y los niños disfrazados van de casa en casa gritando “¡Triqui, triqui!”. ¿Qué están pidiendo? → Dulces
- home-school-and-paperwork-1: overlap like q-6828: «Popote» es a México como ¿qué palabra es a Colombia? → Pitillo: Completa la frase de la lonchera: «Para tomarse el jugo en cajita, hay que chuzarla con el…». → Pitillo
- home-school-and-paperwork-2: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: En muchos colegios colombianos hay unos días sin clases normales, con bailes folclóricos, obras de teatro y comidas típicas de las regiones. ¿Cómo se llaman? → La semana cultural
- home-school-and-paperwork-3: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Completa la analogía: «La olla arrocera es al arroz como la sanduchera es al…». → Sánduche
- home-school-and-paperwork-4: overlap like q-4665: Look at this close-up. You show this little booklet at the airport when you travel to another country. What is it? → Passport: En Colombia lo expide la Cancillería, no la Registraduría, y es una libreta vinotinto con páginas para sellos. ¿Qué documento es? → El pasaporte
- home-school-and-paperwork-6: overlap like home-school-and-paperwork-1: Completa la frase de la lonchera: «Para tomarse el jugo en cajita, hay que chuzarla con el…». → Pitillo: Tengo manija, voy al colegio con el jugo, la fruta y el sánduche, y vuelvo a la casa casi vacía. ¿Qué soy? → La lonchera
- independence-10: overlap like q-5011: El país Bolivia lleva el nombre de un prócer de la Independencia. ¿De cuál? → Simón Bolívar: El departamento cuya capital es Cartagena lleva el nombre de este prócer. ¿Quién es? → Simón Bolívar
- mountains-and-landscapes-11: overlap like q-5240: Subes en el teleférico hasta la cima de Monserrate, en Bogotá. ¿Más o menos a qué altura sobre el nivel del mar llegas? → Unos 3150 metros: Se sube en teleférico o en funicular, arriba tiene una iglesia blanca y desde allí se ve todo Bogotá. ¿Qué cerro es? → Monserrate
- mountains-and-landscapes-13: overlap like q-0229: Las dunas de Taroa, donde la arena del desierto cae directamente al mar Caribe, ¿en qué departamento de Colombia están? → La Guajira: Mira el mapa: en el departamento resaltado están las salinas de Manaure. ¿Cuál es? → La Guajira
- national-symbols-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Estás formado en el patio del colegio para un acto cívico. ¿Cuál de estas cosas NO se hace normalmente ahí? → Partir una torta de cumpleaños
- national-symbols-16: overlap like q-0011: ¿Qué batalla de 1819 selló la independencia de Colombia? → La Batalla de Boyacá: Primero vino el Grito de Independencia, en 1810. ¿En qué año llegó la victoria en la Batalla de Boyacá? → 1819
- national-symbols-17: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: Lees que la palma de cera está «en peligro» en la lista roja de especies. Si siguiera disminuyendo, ¿a qué categoría pasaría? → En peligro crítico
- natural-parks-and-ecosystems-0: overlap like q-1626: Escucha: este animal es de los que más se rescatan del tráfico ilegal en Latinoamérica. ¿Cuál es? → Guacamaya: Estas plumas rojas, azules y amarillas son de un ave que vuela en las selvas de los parques de Colombia. ¿Cuál es? → Guacamaya
- natural-parks-and-ecosystems-1: overlap like q-6835: La casona al borde del Salto del Tequendama, famosa por sus historias de fantasmas, fue hotel durante años. ¿Qué funciona allí hoy? → Un museo: Cerca de Bogotá está el Salto del Tequendama, donde el río cae desde muy alto por un precipicio. En un río, ¿qué es un «salto»? → Una cascada
- natural-parks-and-ecosystems-5: overlap like q-3017: Sunlight splits into colors like these, but it also has invisible rays. Which invisible rays can give you sunburn? → Ultraviolet rays: Antes de pasar el día en la playa en Tayrona, te echas este bloqueador. ¿De qué te protege? → De los rayos del sol
- natural-parks-and-ecosystems-16: overlap like q-1034: El humo de chimeneas como esta lleva el gas que más contribuye al cambio climático causado por los humanos. ¿Cuál es? → Dióxido de carbono: Por él, Colombia ya perdió la mayoría de sus glaciares; lo causan gases de quemar petróleo y carbón, y calienta todo el planeta. ¿Cómo se llama? → Cambio climático
- plants-and-flowers-7: overlap like q-5141: Este paisaje con frailejones sale en el billete de 5000. ¿Por qué es tan importante para ciudades como Bogotá? → Porque guarda y da el agua que toman: El musgo del páramo es verde, suave y cubre rocas y suelos. ¿Qué hace con el agua que luego llega a las ciudades? → La guarda como una esponja
- plants-and-flowers-17: overlap like q-0010: ¿Qué río del Meta es conocido como 'el río de los cinco colores'? → Caño Cristales: Este río se pone rojo por una planta acuática que solo crece ahí. ¿En qué sierra colombiana queda? → Sierra de la Macarena
- popular-and-andean-music-8: overlap like q-5092: En Colombia es ese dolor con rabia que deja un amor que se acabó, se cura con rancheras y hasta tiene su propia música. ¿Cómo se llama? → Despecho: Darío Gómez nació en San Jerónimo, Antioquia, compuso 'Nadie es eterno' y lo coronaron rey de un género. ¿De cuál? → El despecho
- popular-and-andean-music-9: overlap like q-5017: Este boyacense de ruana y sombrero es considerado el padre de la carranga. ¿Quién es? → Jorge Velosa: Estudié para curar animales, pero terminé cantándole con humor a la vida del campo, y mi canción 'La cucharita' se sabe en todo el país. ¿Quién soy? → Jorge Velosa
- popular-and-andean-music-11: overlap like cities-and-towns-12: Cada diciembre, Medellín ilumina el río y sus parques como en esta foto. ¿Cómo le dicen los paisas a esta tradición? → Los alumbrados: En diciembre, millones de bombillos y figuras gigantes de luces adornan el río de esta ciudad, y miles de familias salen a verlos. ¿Qué ciudad es? → Medellín
- regional-speech-15: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Soy caleña de pura cepa. Si te digo «¿Qué más, …?» es porque eres mi amigo del alma. ¿Qué palabra soy? → «Mompa»
- regions-and-departments-7: overlap like q-0329: ¿En qué mes del año se celebra la Feria de las Flores de Medellín? → Agosto: Estás en Medellín viendo el Desfile de Silleteros de la Feria de las Flores. ¿En qué mes del año estás? → En agosto
- cycling-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En los años 80, lo financiaban los cafeteros y en 1987 llevó a Lucho Herrera al título de la Vuelta a España. ¿Qué era «Café de Colombia»? → Un equipo profesional de ciclismo
- drinks-2: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Si en Colombia alguien dice que fulano «se cree la última Coca-Cola del desierto», ¿qué clase de persona es fulano? → Un creído
- drinks-6: overlap like q-1372: ¿Cómo se llama el jarabe espeso y oscuro que sobra al refinar el azúcar de caña y del que se hace casi todo el ron? → Melaza: Se destila de la caña de azúcar o de su melaza y se añeja en barriles de roble. ¿Qué licor es? → El ron
- home-school-and-paperwork-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Después de lavar, la ropa se cuelga en el alambre del patio con ganchos para que se seque al sol. ¿Cómo se dice esto? → Tender la ropa
- hosts-actors-and-comedians-6: hard fail: correct 2, unambiguous 4, no_giveaway 3, no_overlap 5: ¿Qué creadora de contenido de Medellín es la mamá de los dos hijos del cantante Pipe Bueno? → Luisa Fernanda W
- hosts-actors-and-comedians-15: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: La bogotana Pautips se hizo famosa en YouTube con videos de maquillaje y belleza. ¿De dónde sale su nombre? → Pau, por Paula, y «tips», consejos
- mountains-and-landscapes-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Son las montañas pegadas a Bogotá, y en ellas están los cerros de Monserrate y Guadalupe. ¿Cómo se llaman? → Cerros Orientales
- national-symbols-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En el colegio todos cantan el himno y premian a los mejores estudiantes frente a la bandera. ¿Cómo se llama esta ceremonia? → Izada de bandera
- national-symbols-10: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Estás en clase dibujando la bandera de Colombia. ¿Qué representa la franja azul? → Los mares
- national-symbols-11: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Recorres el Museo Nacional en Bogotá, que funciona en el antiguo Panóptico. ¿Qué era un panóptico? → Una cárcel
- natural-parks-and-ecosystems-7: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: En Colombia, una finca puede volverse «Reserva Natural de la Sociedad Civil», registrada ante Parques Nacionales para cuidar el bosque. ¿Quiénes son sus dueños? → Particulares, como familias u ONG
- natural-parks-and-ecosystems-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Vivo en lo alto del Parque Nacional Natural El Cocuy, entre Boyacá y Arauca. Soy blanco, duro y frío, y me deslizo montaña abajo despacito. ¿Qué soy? → Un glaciar
- olympic-medallists-2: hard fail: correct 3, unambiguous 5, no_giveaway 5, no_overlap 5: Nelson Crispín es de Bucaramanga, ganó oro paralímpico en Tokio 2020, medallas de plata en París 2024 y ha batido récords mundiales. ¿En qué deporte? → Natación
- olympic-medallists-7: hard fail: correct 2, unambiguous 5, no_giveaway 4, no_overlap 5: Ángel Barajas ganó en la barra fija la primera medalla olímpica de Colombia en gimnasia. ¿En qué Juegos fue? → París 2024
- olympic-medallists-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Antes de 2019, ¿cómo se llamaba la entidad que hoy es el Ministerio del Deporte de Colombia? → Coldeportes
- popular-and-andean-music-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: ¿Cómo se llamaba el grupo que Jorge Velosa fundó a finales de los años 70 con música campesina de Boyacá? → Los Carrangueros de Ráquira
- regional-speech-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: ¿Cuál de estas personas NO diría «ustedes» para hablarles a sus amigos, sino «vosotros»? → Un madrileño
- regions-and-departments-6: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Soy un departamento pequeño del Caribe, me limita el río Magdalena y en mi capital se celebra un carnaval famosísimo. ¿Quién soy? → Atlántico
- regions-and-departments-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Entre 1863 y 1886, Antioquia tenía su propia constitución y su propio presidente. ¿Qué era Antioquia entonces? → Un estado soberano
- typical-dishes-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Este tamal, que se come con chocolate caliente, lleva en su nombre el antiguo nombre colonial de Bogotá. ¿Cuál es? → Tamal santafereño
- typical-dishes-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Estás en un piquete y te sirven papitas enteras, cocinadas con cáscara en agua, sin freír y sin salsa encima. ¿Cómo se llaman? → Papas saladas
- typical-dishes-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El arroz de lisa es típico de Barranquilla y la Ciénaga, y se hace con lisa salada. ¿Qué es la lisa? → Un pescado
- vallenato-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: ¿En qué película animada de 2021 canta Carlos Vives una canción con acordeón? → Encanto
- words-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Cuando un colombiano dice «¡pailas!», ¿qué quiere decir? → Que ya no hay nada que hacer
- rhythms-dances-and-instruments-7: overlap like q-5135: Cada abril, en Valledupar, los mejores acordeoneros se pelean mi corona tocando paseo, merengue, son y puya. ¿Quién soy? → El Rey Vallenato: Es uno de los cuatro aires del vallenato, el más grabado, de ritmo cadencioso, y se llama igual que una salida de vacaciones. ¿Cuál es? → Paseo
- rhythms-dances-and-instruments-17: overlap like q-0158: Escucha: ¿qué instrumento suena? → La trompeta: Es dorada, tiene tres pistones y suena fuertísimo en las orquestas de salsa de Cali y en las bandas de desfile. ¿Qué instrumento es? → Trompeta
- typical-dishes-6: overlap like q-0465: La aguapanela se hace con panela. Pero, ¿de qué se hace la panela? → Del jugo de la caña de azúcar: La panela de la aguapanela viene en bloques cafés, es muy dulce y se parte con cuchillo o se raspa. ¿Qué es la panela? → Azúcar de caña sin refinar
- typical-dishes-15: overlap like q-5221: En Colombia, el chócolo se asa en la calle con mantequilla y sal, se usa para arepas dulces y no falta en el ajiaco. ¿Qué es? → La mazorca de maíz tierno: La arepa de chócolo es amarilla, dulce y se come con un quesito encima. ¿De qué se hace? → Maíz tierno
- words-5: overlap like q-5221: En Colombia, el chócolo se asa en la calle con mantequilla y sal, se usa para arepas dulces y no falta en el ajiaco. ¿Qué es? → La mazorca de maíz tierno: Crece en una planta alta como una persona, viene envuelta en hojas y tiene pelitos en la punta. ¿De qué planta es la mazorca? → Del maíz
- words-15: overlap like q-5120: Es la prenda insignia de los boyacenses, se teje en telar en Nobsa y abriga en el frío del altiplano. ¿De qué está hecha la ruana tradicional? → De lana de oveja: Las cobijas de lana de Boyacá se hacen con el pelo de un animal que dice «beee». ¿Cuál es? → La oveja
