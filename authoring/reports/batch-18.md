# batch-18

Made by `qgen batch` on 2026-10-23 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): olympic-medallists, hosts-actors-and-comedians, home-school-and-paperwork, pop-rock-and-urban-music, transport, languages, national-symbols, mountains-and-landscapes, plants-and-flowers, national-team, pioneers-and-popular-figures, pre-columbian-cultures, 20th-century, poetry-and-childrens-stories, cinema, scientists-and-inventors, salsa-and-tropical-music, popular-and-andean-music, christmas-and-special-dates, crafts-and-traditional-dress, cities-and-towns, brands-and-products, painters-sculptors-and-museums, sayings-and-expressions, vallenato, club-football, conquest-and-colonial-era
- Merged: 216 (q-7209…q-7424)
- Approved: 198
- Needs work: 18
- Dropped by the pipeline: 70
- Reviewed by: claude-opus-5-5
- Claude calls: 515, about $67.88 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-16, batch-17; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-16 | batch-17 | batch-18 |
|---|---|---:|---:|---:|
| source locale |  | es | es | es |
| drafts |  | 271 | 269 | 286 |
| skipped slots |  | 215 | 217 | 200 |
| dropped |  | 65 | 54 | 70 |
| drop rate | ≤ 20.0 % | 24.0 % ✗ | 20.1 % ✗ | 24.5 % ✗ |
| dropped: hard fail correct |  | 4 | 2 | 1 |
| dropped: hard fail unambiguous |  | 0 | 0 | 1 |
| dropped: hard fail no_giveaway |  | 25 | 14 | 16 |
| dropped: overlap |  | 37 | 38 | 51 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 1 | 1 |
| merged |  | 206 | 215 | 216 |
| approved |  | 186 | 194 | 198 |
| needs_work |  | 20 | 21 | 18 |
| needs_work rate | ≤ 20.0 % | 9.7 % ✓ | 9.8 % ✓ | 8.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.9 % ✓ | 3.3 % ✓ | 1.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.5 % ✓ | 0.9 % ✓ | 0.5 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.9 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.5 % ✓ | 1.9 % ✗ | 0.9 % ✓ |
| needs_work: media | ≤ 10.0 % | 6.3 % ✓ | 4.2 % ✓ | 5.1 % ✓ |
| media: no pick in review 1 |  | 36 | 41 | 43 |
| media: recovered by research |  | 24 | 34 | 33 |
| media: no pick at record |  | 13 | 7 | 10 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.5 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.5 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 14.0 % ✓ | 15.6 % ✓ | 18.5 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 29.2 % ✗ | 45.9 % ✗ | 43.4 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.75 ✗ | 0.83 ✓ |
| approved 11–15 |  | 25 | 40 | 42 |
| top move | ≤ 25.0 % | 14.6 % ✓ | 14.4 % ✓ | 14.8 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 76.7 % | 84.2 % | 86.1 % |
| values stimulus |  | 5 | 5 | 4 |
| top clue | ≤ 60.0 % | 37.4 % ✓ | 38.1 % ✓ | 40.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 28.6 % ✓ | 27.4 % ✓ | 25.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.9 % ✓ | 20.9 % ✓ | 25.0 % ✓ |
| values lens |  | 11 | 11 | 11 |
| media share | 15.0 %–50.0 % | 23.3 % ✓ | 15.8 % ✓ | 13.9 % ✗ |
| mean fun | ≥ 3.40 | 3.32 ✗ | 3.38 ✗ | 3.35 ✗ |
| cost $ |  | $54.66 | $59.96 | $64.49 |
| $ per approved | ≤ $0.35 | $0.29 ✓ | $0.31 ✓ | $0.33 ✓ |
| calls |  | 415 | 443 | 455 |
| calls per approved |  | 2.23 | 2.28 | 2.30 |
| wall time h |  | 2.04 | 1.91 | 1.89 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 3 of 5 (60 %)
- Problems by kind: giveaway 6 (1 major), fact 2 (1 major), ambiguity 1 (1 major), overlap 2 (0 major), media 5 (2 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.38

Major findings on approved questions:

None.

## Needs work

- **q-7220** (christmas-and-special-dates) En el bautizo cargo al bebé junto a la pila de agua y prometo ayudar a cuidarlo toda la vida. ¿Quién soy? → El padrino: The description gives the answer away. "El cargo más bonito de la familia… te dan un bebé y una promesa, pero no sueldo" calls the answer a family role that holds the baby and is unpaid. With the four options alone, that rules out the monaguillo, the sacristán and the notario, which are all church or legal jobs. Rewrite it so it plays on baptism day without calling the role a family one, without the baby and promise, and without the unpaid contrast.
- **q-7229** (cinema) 'La cara oculta' (2011), el thriller de Andrés Baiz sobre una mujer atrapada en un cuarto secreto, tuvo una nueva versión. ¿Cuál? → Una película de Bollywood: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-7258** (crafts-and-traditional-dress) Mira de cerca: en esta vasija grande de barro se guardaba el agua fresca en las casas de antes. ¿Cómo se llama? → Tinaja: No candidate is an adequate essential image. #1 is a black-and-white book scan with a crowd, and #2–#6 are ancient Greek hydriae from the MET (painted figures, handles, narrow necks), not the wide-mouthed, big-bellied clay water tinaja the question and hints describe. A new search isn't allowed here. The media needs a real tinaja photo, for example from a search like "tinaja barro agua" or "clay water tinaja Colombia". No se encontró una imagen adecuada para esta pregunta.
- **q-7259** (crafts-and-traditional-dress) En este desfile del martes de Carnaval en Barranquilla, unas «viudas» lloran a un personaje que «murió» de tanto parrandear. ¿Quién es? → Joselito Carnaval: The media slot has no candidates and can't be searched again, so the question has no image. The text answers the question on its own, so the slot should also be illustrative, not essential. A new search should look for the Barranquilla Carnival or its 'viudas' costumes, and the picture must not show a sign naming Joselito. No se encontró una imagen adecuada para esta pregunta.
- **q-7321** (popular-and-andean-music) Jorge Velosa bautizó su música como "carranga". En el campo, ¿a qué se refería originalmente esa palabra? → A la carne de reses muertas: The text is fine: the carranga etymology (meat from cattle that died in the field, from Velosa's 'El carranguero') is confirmed and nothing gives it away. But no image candidate shows the Boyacá countryside: they are snowy Chilean/Argentine Andes, ISS desert views and South Dakota wetlands. A new search is needed, for example "Boyaca countryside farm" or "Colombian Andes pasture cows". No se encontró una imagen adecuada para esta pregunta.
- **q-7330** (pre-columbian-cultures) Viene de una lengua indígena caribe, la anotaron los cronistas y en la Independencia se usó en los campamentos. ¿Qué significaba «guaricha»? → Muchacha o mujer joven: Verificación de datos: uncertain. I didn't verify this one online. The Caribe origin and the meaning 'muchacha/mujer' look plausible. The claim that the Independence-era 'guarichas' were camp followers who marched with Bolívar's armies is unverified.
- **q-7331** (pre-columbian-cultures) Mira esta figura tallada en piedra. ¿Qué es? → Una estatua de San Agustín: Hint 2 gives the answer away: 'en las montañas del sur de Colombia' rules out all three wrong answers outright (Easter Island/Chile, Mexico, Peru), so hint 2 solves the question by itself. Hint 2 should be about something like the fangs or the guardian figures, with no country or region. Media pick 6 is fine.
- **q-7346** (club-football) Completa el nombre del gran torneo de clubes de Sudamérica que ganaron Atlético Nacional y Once Caldas: «Copa…» → Libertadores: This question overlaps with pool questions that give its answer away. The approved q-7028 says "Copa Libertadores 2004" in its text, and draft q-7244 says "ganó la Libertadores de 2004". A family that saw either of them is handed this answer. You could keep this one only if the other questions stop naming the trophy. Otherwise drop it.
- **q-7348** (conquest-and-colonial-era) El conquistador navarro Pedro de Ursúa fundó la ciudad de Pamplona, en el actual Norte de Santander. ¿En qué año? → 1549: None of the image candidates shows Pamplona in Norte de Santander. They show Plaza Colombia in Buenos Aires (1, 2), Botero sculptures in Medellín (3, 4), Plaza de Bolívar in Bogotá (5) and Cartagena (6), and no new search is allowed. The slot needs a photo of Pamplona's main square or cathedral, for example from the search 'Pamplona Norte de Santander'. No se encontró una imagen adecuada para esta pregunta.
- **q-7349** (conquest-and-colonial-era) Este recipiente de madera se usa en el mazamorreo, en los ríos de Antioquia y Chocó. ¿Qué se busca con él? → Oro: The essential image must show a wooden batea, but none of the candidates does: two are municipal coats of arms (Nechí, Bagadó) and one is a river swimming spot. Another search isn't allowed, so the slot needs a real batea photo (e.g. 'wooden gold pan batea'), or the question should be reworded so it doesn't depend on the image ("Este recipiente…"). No se encontró una imagen adecuada para esta pregunta.
- **q-7361** (hosts-actors-and-comedians) «La Liendra» es el apodo de un influencer colombiano muy famoso. Pero, ¿qué es de verdad una liendra? → El huevo del piojo: The text is fine, but none of the candidates fits a question about nits and human hair. Candidates 1 and 6 are plants. Candidates 2, 3 and 5 are cats, which suggest pets and fleas (close to the wrong option «pulga de perro»). Candidate 4 is a body-focused gym photo, not suitable for families. A new search such as "child hair comb" or "hair brushing" is needed. No se encontró una imagen adecuada para esta pregunta.
- **q-7366** (national-symbols) Este escudo, con dos cuernos de la abundancia y un haz de lanzas, era el de un país creado en 1819. ¿Qué países de hoy lo formaban? → Colombia, Venezuela, Ecuador y Panamá: None of the candidates shows the Gran Colombia coat of arms, but the question needs it because it says "Este escudo". #1 is Venezuela's 2006 coat of arms, which is a different emblem. #2, #3 and #5 are maps of Gran Colombia that show which countries it covered, so they give the answer away. #4 is Panama's 1821 independence act, which points to Panama. #6 is a handwritten letter. No new search is allowed, so the media needs a manual fix: for example, Commons' Gran Colombia coat of arms file, cropped so the name doesn't show. No se encontró una imagen adecuada para esta pregunta.
- **q-7377** (pioneers-and-popular-figures) ¿En qué año se estrenó «Yo soy Betty, la fea», la novela donde Nicolás Mora es el mejor amigo de Betty? → 1999: This asks the same fact as approved q-7179, the year "Yo soy Betty, la fea" premiered in Colombia (1999), just in other words. It's a duplicate and should be dropped. Hint 2 ("en los años noventa") also rules out two of the three wrong answers.
- **q-7382** (pop-rock-and-urban-music) Esta cantante colombiana le pone la voz a la estrella pop de Zootopia. ¿Qué animal es ese personaje? → Una gacela: Hint 2 gives the answer away: "savanna, thin, horns, very fast" leaves gazelle as the only possible option out of the four (rabbit, sheep and fox all fail), so hint 2 effectively solves the question. It should give a vaguer clue (e.g. that she has a herbivore's diet or a long neck and legs), and the third hint can then point to savanna and horns. Separately, "Una zorra" works as a crude insult for a woman in Colombia and much of Latin America, so a family game shouldn't use it as an option. Replace it with another animal from the film (e.g. "Una cebra" or "Una leona").
- **q-7392** (sayings-and-expressions) Es muy informal y viene de juntar «qué» y «hubo». ¿Qué quiere decir «¿quiubo?»? → Hola, ¿qué más?: No candidate works as an illustrative image, and another search isn't allowed. #2 (two cats touching noses) shows a greeting, which is the answer itself. #1 is a climate protest with a 'KILLER' sign, #3 is a captioned 1847 Māori engraving, #5 is a diplomatic meeting, and #4 and #6 have nothing to do with the question. The question needs a neutral Colombian image instead, such as a neighbourhood street or a corner shop in Bogotá or Medellín. Also check overlap with q-5198: if its options list «quiubo» as a greeting, it gives this answer away. No se encontró una imagen adecuada para esta pregunta.
- **q-7403** (salsa-and-tropical-music) Estás en una salsoteca de Cali y un melómano dice que la orquesta «se cruzó de clave». En la salsa, ¿qué es la clave? → Un patrón de cinco golpes que guía el ritmo: The description gives away the answer: saying that even the best orchestra is lost without it is the clave's defining trait (the pattern that guides the rhythm). It also rules out the sung high note, the dancers' step and the closing piano solo, since no orchestra gets lost without those. Rewrite the description so it plays on Cali or salsoteca nights without hinting that the thing keeps the band together.
- **q-7416** (scientists-and-inventors) El billete de 20 000 pesos lleva la cara de Julio Garavito y un dibujo de la Luna, y un cráter lunar tiene su nombre. ¿Por qué? → Porque estudió el movimiento de la Luna: All four media candidates show the Chilean 20 000 peso banknote (Andrés Bello portrait and the reverse with a landscape), not the Colombian note with Julio Garavito and the Moon. A new search isn't allowed, so the slot needs media from somewhere else, e.g. a Commons file of the Colombian 20 000 COP note (2016 series) or a generic Moon photo as the illustrative image. No se encontró una imagen adecuada para esta pregunta.
- **q-7424** (vallenato) En 1982 García Márquez llevó músicos vallenatos a Estocolmo y recibió el Nobel vestido con esta prenda blanca. ¿Cómo se llama? → El liqui liqui: None of the six candidates shows a liqui liqui: they are Ifugao, Tibetan, Andean, Seto, Russian and Uzbek costumes, and #3 even shows a poncho (a wrong option). No new search is allowed. The slot needs a real liqui liqui photo, or a change to an illustrative or decorative role (e.g. Stockholm Concert Hall or a vallenato accordion). No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 5, cause_effect 5, count 6, estimate 3, identify 28, made_of 8, name_concept 17, odd_one_out 21, origin 25, purpose 12, record 6, sequence 9, when 19, who 20, word_meaning 32
- stimulus: detail 8, map_outline 1, none 186, photo 21
- clue: completion 8, direct 88, riddle 23, scenario 29, three_facts 68
- answer_kind: group 22, number 10, person 38, place 20, thing 55, time 19, word 52
- lens: body_senses 6, colombia 54, educational_media 15, everyday 21, history 33, language 36, nature 8, pop_culture 23, school 10, science_news 1, university 9

## Dropped by the pipeline

- 20th-century-5: overlap like q-0405: ¿Qué noche se celebra en Colombia el Día de las Velitas, cuando las familias prenden velas y faroles en ventanas y andenes? → La noche del 7 de diciembre: El 7 de diciembre las familias colombianas prenden velitas y faroles. ¿En honor a quién? → La Virgen María
- 20th-century-14: overlap like q-5162: Completa la Constitución de 1991: «Las lenguas y dialectos de los grupos étnicos son también oficiales en…» → sus territorios: La Constitución de 1991 reconoce la «diversidad étnica y cultural» de Colombia. Por eso, ¿qué son lenguas como el wayuunaiki o el palenquero? → Oficiales en sus territorios
- brands-and-products-1: overlap like q-7138: En una tienda de barrio en Colombia pides una Jumbo. ¿Qué te entregan? → Una chocolatina con maní: ¿De qué país es la chocolatina Jumbo, la famosa que viene con maní? → Colombia
- brands-and-products-5: overlap like 20th-century-9: La Chocolatina Jet trae adentro una lámina de animales, del espacio o de la naturaleza. ¿Para qué la guardan los niños? → Para pegarla en un álbum: Además del chocolate, ¿qué trae cada chocolatina Jet que los niños colombianos coleccionan desde hace décadas? → Una lámina
- christmas-and-special-dates-4: overlap like q-6985: La guacharaca del conjunto vallenato lleva el nombre de un ave de la costa. ¿A qué familia de instrumentos pertenece? → De percusión: En el villancico del «ropopompom», un niño pobre no tiene regalo y le toca su instrumento al Niño Dios. ¿Qué tipo de instrumento es? → De percusión
- christmas-and-special-dates-6: overlap like q-4232: A baby bird sleeps in a nest. In the Christmas story, baby Jesus sleeps in a…? → Manger: En el pesebre, el buey y la mula le dan calor al Niño Dios con su aliento. Según la historia, ¿dónde pasó eso? → En un establo de Belén
- christmas-and-special-dates-8: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: En los juegos de aguinaldos, ¿cómo se llama el juego en el que debes tener algo como esto en la boca todo el tiempo? → Pajita en boca
- christmas-and-special-dates-10: overlap like q-1017: En España, el juego de sacar papelitos y dar un regalo sin revelar a quién te tocó no se llama 'amigo secreto'. ¿Cómo lo llaman allá? → Amigo invisible: En Colombia, en Amor y Amistad, sacas un papelito con un nombre: te tocó de «amigo secreto». ¿Qué significa? → Que le das detalles sin que sepa quién eres
- christmas-and-special-dates-12: overlap like q-5178: El 7 de diciembre por la noche, las familias colombianas prenden lucecitas en andenes, ventanas y balcones para arrancar la Navidad. ¿Cómo se llama esa noche? → Noche de velitas: Son de cera, tienen una mecha y el 7 de diciembre las familias colombianas las prenden en ventanas y andenes. ¿Qué son? → Las velitas
- cinema-4: overlap like q-3374: I'm a golden statue. In 2022, minutes after Will Smith slapped Chris Rock on stage, he took me home for Best Actor. What am I called? → An Oscar: Es una estatuilla dorada de un caballero con espada, 'Encanto' lo ganó como mejor película animada y Sebastián Yatra cantó en su ceremonia. ¿Qué premio es? → El Óscar
- cinema-7: overlap like q-0794: Completa: García Márquez es a 'Cien años de soledad' como Héctor Abad Faciolince es a… → El olvido que seremos: Soy escritor de Medellín. Escribí un libro sobre mi padre, un médico salubrista, y mi hija Daniela lo llevó al documental 'Carta a una sombra'. ¿Quién soy? → Héctor Abad Faciolince
- cities-and-towns-1: overlap like q-6904: Vivo en cables larguísimos, me prendo y me apago de colores y en diciembre me cuelgan en balcones y en el alumbrado de Medellín. ¿Qué soy? → Los bombillos navideños: Mira la foto: en diciembre, Medellín llena el río y los parques de figuras de luces como estas. ¿Cómo las llaman? → Los alumbrados
- cities-and-towns-4: overlap like q-6964: ¿Cada cuánto y en qué mes se celebra el Carnaval de Riosucio, en Caldas? → En enero, cada dos años: En Riosucio, Caldas, el carnaval es cada dos años, en enero, y su gran figura es el Diablo. Allá, ¿quiénes son los «matachines»? → Los poetas que escriben y recitan los versos burlones del carnaval
- cities-and-towns-7: overlap like q-0130: Mira la foto: ¿en qué ciudad colombiana está esta famosa torre del reloj? → Cartagena: Por la Torre del Reloj se entra a un centro histórico del Caribe rodeado de murallas. ¿Con qué apodo se conoce esa ciudad? → El Corralito de Piedra
- conquest-and-colonial-era-7: overlap like q-5008: Estás viendo las miles de láminas de flores pintadas a mano por la Real Expedición Botánica. ¿Quién dirigió esa expedición? → José Celestino Mutis: Pedro Messía de la Cerda llegó como virrey en 1761 con un médico gaditano amante de las plantas, que se quedó para siempre. ¿Qué gran empresa dirigió luego ese médico? → La Expedición Botánica
- crafts-and-traditional-dress-15: overlap like q-3902: For thousands of years, people have cut riverside plants like these. What have they mostly made from them? → Baskets and mats: Esta estera se teje con una planta que crece en las lagunas, como la de Fúquene. ¿Cuál es? → El junco
- home-school-and-paperwork-10: overlap like q-0003: ¿Con qué se hacen tradicionalmente las arepas? → Maíz: Es redonda y hecha de maíz, se asa en la mañana y se come con mantequilla, queso o huevo. ¿Qué es? → La arepa
- languages-1: overlap like q-0583: En la isla de San Andrés, el pueblo raizal habla creole. ¿De qué idioma viene la mayoría de las palabras de esa lengua? → Inglés: Viven en San Andrés, Providencia y Santa Catalina, hablan creole e inglés, y casi todos son protestantes. ¿Cómo se llama este pueblo? → Los raizales
- languages-4: overlap like q-7059: Boyacomán hace reír como un campesino de Boyacá, y como buen boyacense trata a todos con mucho cariño. ¿Qué palabra usa en vez de «usted»? → Sumercé: En Boyacá, para hablarle a alguien con cariño y respeto, dicen: «¿Cómo amaneció, …?». Completa la frase. → Sumercé
- mountains-and-landscapes-6: overlap like q-0132: ¿Cuál de estas ciudades colombianas está a mayor altura sobre el nivel del mar? → Tunja: ¿Cuál de estas ciudades colombianas NO está a más de 2000 metros sobre el nivel del mar? → Cartagena
- mountains-and-landscapes-15: overlap like q-5913: What is this rushing, foamy stretch of a river, full of rocks, called? → Rapids: En el río Orinoco, en el Vichada, el agua baja rugiendo entre rocas gigantes, y Humboldt la llamó «la octava maravilla del mundo». ¿Cómo se llama ese tramo de rápidos? → Raudal
- national-symbols-1: overlap like q-7000: ¿Qué día se recuerda en Colombia la Batalla de Boyacá? → 7 de agosto: En Colombia, muchas casas cuelgan así la bandera el 20 de julio y el 7 de agosto. ¿Qué batalla se recuerda el 7 de agosto? → La batalla de Boyacá
- national-symbols-10: overlap like q-0469: ¿Cómo se llama el famoso caficultor de bigote, sombrero y poncho que, junto con su mula, es el símbolo del café de Colombia? → Juan Valdez: Lleva sombrero, poncho y una mula llamada Conchita, y representa el café de Colombia en el mundo. ¿Cómo se llama? → Juan Valdez
- national-symbols-14: overlap like q-0272: Mira la foto: ¿cómo se llama esta palma? → Palma de cera: Es el árbol nacional de Colombia, puede pasar de 50 metros de altura y su nombre completo incluye un departamento cafetero. ¿Cuál? → Quindío
- national-symbols-16: overlap like q-5165: Estás en la Plaza de Bolívar de Bogotá, frente a la estatua de bronce del Libertador hecha por el italiano Pietro Tenerani. ¿En qué año se instaló? → 1846: En el centro de esta plaza de Bogotá, llena de palomas, hay una estatua de bronce. ¿De quién es? → Simón Bolívar
- national-team-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Completa: a la Selección Colombia le dicen «la Tricolor» porque… → lleva los tres colores de la bandera
- olympic-medallists-3: overlap like q-5167: Óscar Figueroa ganó oro olímpico en pesas y, como despedida, dejó sus zapatos sobre la tarima. ¿En qué ciudad fue? → Río de Janeiro: ¿Qué pesista colombiano ganó oro en Río 2016 y, al terminar, se quitó los zapatos y los dejó en la tarima como despedida? → Óscar Figueroa
- olympic-medallists-6: overlap like q-7075: En este deporte, ¿qué colombiana ganó bronce olímpico en Londres 2012 y plata en Río 2016? → Yuri Alvear: ¿Cuántas medallas olímpicas ganó la judoca colombiana Yuri Alvear? → 2
- painters-sculptors-and-museums-9: overlap like q-5075: ¿Cuántas esculturas de Fernando Botero hay en la Plaza Botero de Medellín? → 23: Mira la foto: estas figuras voluminosas son el estilo llamado boterismo. ¿En qué ciudad colombiana nació su creador? → Medellín
- painters-sculptors-and-museums-15: overlap like q-5093: Este grupo del Pacífico colombiano ganó un Latin Grammy en 2010 con «De dónde vengo yo». ¿Cómo se llama? → ChocQuibTown: ¿Quién es la cantante de ChocQuibTown, el grupo chocoano que mezcla hip hop con ritmos del Pacífico y cantó «De dónde vengo yo»? → Goyo
- plants-and-flowers-6: overlap like q-0008: ¿Cuál es la flor nacional de Colombia? → La orquídea: Mira la flor nacional de Colombia, la Cattleya trianae. ¿A qué grupo de plantas pertenece? → Las orquídeas
- plants-and-flowers-13: overlap like national-symbols-14: Es el árbol nacional de Colombia, puede pasar de 50 metros de altura y su nombre completo incluye un departamento cafetero. ¿Cuál? → Quindío: Mira este tronco altísimo, liso y con anillos: es del árbol nacional de Colombia. ¿Qué tipo de planta es? → Una palma
- poetry-and-childrens-stories-13: overlap like q-5171: «Pablito clavó un clavito: ¿qué clavito clavó Pablito?». ¿Qué tipo de frase es esta? → Un trabalenguas: Soy redonda, lisa y brillante, no tengo ni un pelo, y Pablito clavó en mí un clavito. ¿Qué soy? → La calva de un calvito
- poetry-and-childrens-stories-15: overlap like poetry-and-childrens-stories-16: Me dicen «la gata candonga» y, en un cuento en verso de Rafael Pombo, voy a dar una fiesta jugando a la ronda. ¿Quién soy? → Mirringa Mirronga: Rin Rin, el renacuajo paseador, sale con su amigo Ratón. ¿Cuál de estos personajes NO aparece en ese cuento de Pombo? → Mirringa Mirronga
- poetry-and-childrens-stories-16: overlap like q-5090: ¿En qué siglo publicó Rafael Pombo «El convite de Mirringa Mirronga», la fiesta de la gata candonga? → Siglo XIX: Me dicen «la gata candonga» y, en un cuento en verso de Rafael Pombo, voy a dar una fiesta jugando a la ronda. ¿Quién soy? → Mirringa Mirronga
- poetry-and-childrens-stories-17: overlap like q-5173: Tío Conejo engaña a animales más grandes y feroces, y Pedro Rimales se burla del rey, aunque ninguno es fuerte. ¿Qué cualidad los hace ganar? → La astucia: Soy un pícaro de los cuentos del campo y los Llanos, engaño a ricos y bobos con mi ingenio, y en España me llamaban Pedro de Urdemalas. ¿Quién soy? → Pedro Rimales
- pop-rock-and-urban-music-11: overlap like q-6792: En los mariposarios de Colombia cuelgan muchas cápsulas como esta. ¿Para qué sirven? → Para que la oruga se convierta en mariposa: En Encanto suena «Dos oruguitas». Si las oruguitas esperan su tiempo, ¿en qué se convierten? → En mariposas
- popular-and-andean-music-3: overlap like cities-and-towns-1: Mira la foto: en diciembre, Medellín llena el río y los parques de figuras de luces como estas. ¿Cómo las llaman? → Los alumbrados: Estás caminando junto al río Medellín, entre millones de bombillos de colores que forman figuras gigantes. ¿En qué mes del año estás? → Diciembre
- popular-and-andean-music-16: overlap like q-5082: Es capital del Huila, queda junto al río Magdalena y en sus fiestas de San Pedro corona a la Reina Nacional del Bambuco. ¿Qué ciudad es? → Neiva: Soy una capital del sur de Colombia; cada junio, en las fiestas de San Pedro, celebro el Reinado Nacional del Bambuco. ¿Quién soy? → Neiva
- popular-and-andean-music-17: overlap like q-0062: Escucha: ¿qué instrumento está sonando? → El violín: Tengo cuatro cuerdas, me apoyan bajo la barbilla y me tocan frotándome con un arco. ¿Qué soy? → El violín
- pre-columbian-cultures-6: overlap like q-0406: El sombrero vueltiao, símbolo cultural de Colombia, se teje con trenzas de una fibra vegetal. ¿Cuál es? → Caña flecha: Para el sombrero vueltiao, los zenúes raspan unas hojas largas, tiñen las tiras de negro con barro y las trenzan. ¿De qué planta son? → Caña flecha
- 20th-century-4: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: La fundaron en 1950 miembros del Grupo de Barranquilla, con Alfonso Fuenmayor de director y Gabo de jefe de redacción. ¿Qué era «Crónica»? → Un semanario de cuentos y fútbol
- 20th-century-9: overlap like brands-and-products-5: Además del chocolate, ¿qué trae cada chocolatina Jet que los niños colombianos coleccionan desde hace décadas? → Una lámina: La Chocolatina Jet trae adentro una lámina de animales, del espacio o de la naturaleza. ¿Para qué la guardan los niños? → Para pegarla en un álbum
- brands-and-products-11: overlap like scientists-and-inventors-12: Es un ponquecito rectangular, forrado en chocolate, se vende en todas las tiendas de Colombia y es el clásico de las onces. ¿Cuál es? → Chocoramo: Es rectangular, viene en paquete individual y lo hace la marca Ramo. ¿Qué es un Chocoramo? → Un ponqué cubierto de chocolate
- cinema-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Qué actor protagonizó 'La pena máxima' (2001) como Mariano Concha, un hincha capaz de todo por la Selección Colombia? → Enrique Carriazo
- cities-and-towns-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Mira la foto: este puente de hierro sobre el Magdalena es símbolo de un pueblo de tierra caliente. Su nombre es el apellido de un prócer: ¿cuál? → Atanasio Girardot
- club-football-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Cómo se llama la barra del Junior que alienta en la tribuna sur del Metropolitano de Barranquilla? → Frente Rojiblanco Sur
- club-football-9: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Soy el apodo del Millonarios de comienzos de los años 50, el de Pedernera y Di Stéfano, que jugaba como si bailara. ¿Cómo me llamaban? → El Ballet Azul
- conquest-and-colonial-era-1: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Lo bautizó Gonzalo Jiménez de Quesada en 1538 y en 1717 se volvió virreinato. ¿Qué fue el Nuevo Reino de Granada? → La colonia española del territorio colombiano
- conquest-and-colonial-era-10: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Vestían hábito café con cordón de nudos y en el siglo XVI levantaron en la avenida Jiménez de Bogotá una iglesia de altar dorado. ¿Qué orden era? → Los franciscanos
- crafts-and-traditional-dress-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En el Carnaval de Pasto, el 6 de enero todo el mundo termina lleno de talco. ¿Cómo se llama ese día? → Día de los Blancos
- home-school-and-paperwork-12: overlap like q-6843: El trapero tiene un palo largo, se moja en el balde y se exprime antes de usarlo. ¿Para qué sirve? → Para limpiar el piso: Barrer es a la escoba como trapear es a… → El trapeador
- hosts-actors-and-comedians-1: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Antonio Bolívar fue el viejo chamán Karamakate en «El abrazo de la serpiente». ¿De dónde salió la historia de esa película? → De diarios de exploradores reales
- languages-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En la tienda saludamos a «don Pedro». ¿Qué palabra usamos, igual de respetuosa, para la señora Carmen? → Doña
- mountains-and-landscapes-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Son la muralla verde que se ve desde casi toda Bogotá, y en ellos están Monserrate y Guadalupe. ¿Cómo se llaman? → Los cerros Orientales
- national-symbols-9: overlap like q-1963: En el Capitolio Nacional de Bogotá se reúnen… → Los senadores y representantes: Estas columnas son de un famoso edificio de piedra en la Plaza de Bolívar de Bogotá. ¿Cuál es? → El Capitolio Nacional
- olympic-medallists-11: hard fail: correct 4, unambiguous 2, no_giveaway 4, no_overlap 5: ¿En qué año fueron los Juegos Olímpicos en los que el colombiano Anthony Zambrano ganó plata en los 400 metros? → 2021
- poetry-and-childrens-stories-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Somos tres, andamos muy tristes y tragamos trigo en un trigal. ¿Quiénes somos? → Los tres tristes tigres
- salsa-and-tropical-music-15: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Los bailarines caleños de Swing Latino cuentan la salsa en dos mitades de cuatro tiempos. ¿En qué tiempo de la primera mitad no pisan? → 4
- sayings-and-expressions-1: fact-check wrong: The fun fact says «bacán» is 'siempre' used for something very good in Chile, Peru and Cuba. In Cuba it can also mean a man kept by his wife or lover, and in Argentina and Uruguay it means a rich man. Also, the usual Colombian form is «bacano».: En la Costa la dicen en fiestas y en canciones de champeta. ¿Para qué se usa «bacán»? → Para decir que algo es muy bueno
- sayings-and-expressions-10: overlap like q-5057: ¿Cómo se le dice al acento de Medellín y Antioquia, famoso por el «pues» y el «¡ave María!»? → Paisa: Se pone al final de casi todo («¡hágale, pues!») y sale en muchas comedias. ¿De qué región es más típico ese «pues»? → Antioquia
- transport-3: overlap like q-5076: Este parque nacional queda en el departamento resaltado, a orillas del río Amazonas y cerca de Leticia. ¿Cómo se llama? → Amacayacu: En Leticia, el bus es a la carretera como el bote es a… → el río Amazonas
- transport-6: hard fail: correct 2, unambiguous 5, no_giveaway 5, no_overlap 5: Completa: «En Bogotá, Medellín y Cali, casi todos los taxis son de color…» → amarillo
- vallenato-4: overlap like q-0702: Protege lugares como Machu Picchu y Cartagena; también protege tradiciones vivas; y en 2010 incluyó la cocina tradicional mexicana en su lista. ¿Qué organización es? → UNESCO: El vallenato es Patrimonio Cultural Inmaterial de la UNESCO. ¿Qué significa aquí «inmaterial»? → Que es una tradición viva, no un objeto
- vallenato-16: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: «El cantor de Fonseca» habla de su propio autor, nacido en ese pueblo guajiro. ¿Quién la compuso? → Carlos Huertas
- salsa-and-tropical-music-7: overlap like q-6948: Una cumbia famosísima cuenta la historia de una embarcación como esta: la de Guillermo Cubillos. ¿Quién la compuso? → José Barros: Nací en 1915 en El Banco, Magdalena. Compuse «El gallo tuerto» y «Momposina», y allá hacen cada año un festival de cumbia con mi nombre. ¿Quién soy? → José Barros
- scientists-and-inventors-3: overlap like q-0051: ¿Qué planeta es conocido como el planeta rojo? → Marte: Tiene dos lunas chiquitas, por su suelo ruedan robots de la NASA y la caleña Diana Trujillo trabajó en misiones para explorarlo. ¿Qué planeta es? → Marte
- scientists-and-inventors-12: overlap like brands-and-products-11: Es rectangular, viene en paquete individual y lo hace la marca Ramo. ¿Qué es un Chocoramo? → Un ponqué cubierto de chocolate: Es un ponquecito rectangular, forrado en chocolate, se vende en todas las tiendas de Colombia y es el clásico de las onces. ¿Cuál es? → Chocoramo
- scientists-and-inventors-17: overlap like q-5203: En el método madre canguro, creado en Bogotá: la bolsa es a la cría de canguro como ¿qué es al bebé prematuro? → El pecho de la mamá: El método madre canguro, creado en Bogotá, ayuda a los bebés que nacen antes de tiempo. ¿Cómo se les dice? → Prematuros
- transport-0: overlap like q-7096: Si el 6 de enero cae un miércoles, ¿qué día descansan en Colombia por el festivo de Reyes? → El lunes siguiente: En Colombia, en un puente festivo, ¿qué día de la semana suele caer el festivo? → El lunes
