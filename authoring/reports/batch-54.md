# batch-54

Made by `qgen batch` on 2026-11-08 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): current-music, scientists-and-explorers, regional-symbols, pop-and-rock, tv-series, 20th-century, comics-and-childrens-books, spanish-cinema, painting-and-architecture, flamenco-and-copla, radio-and-internet, fiestas, al-andalus-and-reconquista, legends-and-superstitions, team-and-traditional-sports, modern-literature, empire, monuments, sportspeople, classic-literature, cities-and-towns, protected-areas, regions-and-provinces, coasts-and-islands, money-and-services, bourbons-and-19th-century, rivers-and-mountains
- Merged: 244 (q-16168…q-16411)
- Approved: 228
- Needs work: 16
- Dropped by the pipeline: 87
- Reviewed by: claude-opus-5-5
- Claude calls: 565, about $80.57 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-52, batch-53; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-52 | batch-53 | batch-54 |
|---|---|---:|---:|---:|
| source locale |  | en | de | es-ES |
| drafts |  | 316 | 337 | 331 |
| skipped slots |  | 134 | 149 | 155 |
| dropped |  | 86 | 73 | 87 |
| drop rate | ≤ 20.0 % | 27.2 % ✗ | 21.7 % ✗ | 26.3 % ✗ |
| dropped: hard fail correct |  | 1 | 0 | 1 |
| dropped: hard fail unambiguous |  | 1 | 1 | 0 |
| dropped: hard fail no_giveaway |  | 12 | 19 | 15 |
| dropped: overlap |  | 70 | 51 | 69 |
| dropped: duplicate |  | 2 | 2 | 2 |
| dropped: fact-check wrong |  | 0 | 1 | 0 |
| merged |  | 230 | 264 | 244 |
| approved |  | 212 | 243 | 228 |
| needs_work |  | 18 | 21 | 16 |
| needs_work rate | ≤ 20.0 % | 7.8 % ✓ | 8.0 % ✓ | 6.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.6 % ✓ | 1.1 % ✓ | 1.6 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.9 % ✓ | 1.1 % ✓ | 0.8 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.4 % ✓ | 1.5 % ✗ | 0.4 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.8 % ✓ | 4.2 % ✓ | 4.1 % ✓ |
| media: no pick in review 1 |  | 21 | 29 | 43 |
| media: recovered by research |  | 15 | 21 | 36 |
| media: no pick at record |  | 7 | 8 | 9 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.8 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 23.1 % ✗ | 16.9 % ✓ | 21.8 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 68.6 % ✓ | 67.1 % ✓ | 59.2 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 2.12 ✗ | 1.35 ✓ | 1.50 ✓ |
| approved 11–15 |  | 35 | 50 | 44 |
| top move | ≤ 25.0 % | 14.8 % ✓ | 12.5 % ✓ | 15.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 77.4 % | 87.9 % | 79.9 % |
| values stimulus |  | 6 | 5 | 4 |
| top clue | ≤ 60.0 % | 47.4 % ✓ | 42.4 % ✓ | 43.9 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.7 % ✓ | 25.0 % ✓ | 20.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.4 % ✓ | 22.3 % ✓ | 17.6 % ✓ |
| values lens |  | 10 | 11 | 9 |
| media share | 15.0 %–50.0 % | 22.6 % ✓ | 12.1 % ✗ | 20.1 % ✓ |
| mean fun | ≥ 3.40 | 3.44 ✓ | 3.38 ✗ | 3.47 ✓ |
| cost $ |  | $65.05 | $76.22 | $76.96 |
| $ per approved | ≤ $0.35 | $0.31 ✓ | $0.31 ✓ | $0.34 ✓ |
| calls |  | 463 | 488 | 505 |
| calls per approved |  | 2.18 | 2.01 | 2.21 |
| wall time h |  | 2.00 | 2.35 | 1.89 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 56 (2 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 7 (1 major), fact 2 (0 major), overlap 2 (0 major), media 5 (2 major), difficulty 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.60

Major findings on approved questions:

- **q-16324**: giveaway — The facts hold up: Vázquez's Anacleto is a well-known James Bond parody, and he also created Las hermanas Gilda and La familia Cebolleta. The problem is that the question text ("agente secreto", "aires de espía") and the description ("Un espía") rule out every wrong option. Sherlock Holmes is a detective, Indiana Jones an archaeologist and the Zorro a masked swordsman, so Bond is the only spy among the four. The wrong answers should be other spy franchises, for example Superagente 86, OSS 117 or Misión Imposible. (http://127.0.0.1:8001/review/q-16324)

## Needs work

- **q-16176** (al-andalus-and-reconquista) Mira este detalle de un laúd, el instrumento que los árabes llamaban «al-ʿūd». ¿A qué familia de instrumentos pertenece? → Cuerda pulsada: None of the media candidates shows a lute or oud. They are a guitar cable, NASA instruments, a telescope instrument and a car dashboard, and no new search is allowed. The slot needs a close-up of an oud. It should also be illustrative, not essential, because the question already names the lute. Minor point for the reviser: hints 1 and 2 together already rule out every option except «Cuerda pulsada», so hint 2 should be softer. No se encontró una imagen adecuada para esta pregunta.
- **q-16182** (bourbons-and-19th-century) En la Guerra de la Independencia (1808-1814), grupos pequeños de campesinos atacaban por sorpresa y se escondían en los montes. ¿Contra quién luchaban? → Contra los soldados franceses: The question's real content is "the 1808–1814 War of Independence was fought against the French". Approved pool questions already state this in their own text: q-9868 says Zaragoza resisted «contra los franceses» in that war, and q-14229 says that in 1808 Spaniards were urged to rise up «contra los franceses». q-14295 (Goya's 3 de mayo, answer "Soldados franceses") also overlaps. Seeing any of them gives this answer away. Either drop the question, or rework it so it asks about something those questions don't reveal, such as the guerrilla tactic itself.
- **q-16186** (bourbons-and-19th-century) El nombre «Generación del 98» lo inventó en 1913 uno de sus propios escritores. ¿Quién fue? → Azorín: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-16205** (classic-literature) Este poeta granadino publicó en 1928 el «Romancero gitano», con versos como «Verde que te quiero verde». ¿Quién es? → Federico García Lorca: The media slot is set as essential, and its note asks for a portrait of Lorca. No candidate is a portrait, and a portrait would give the answer away anyway, because the question is answered from the text. Change the slot to illustrative. Candidate 1 or 2 (Albaicín rooftops seen from the Alhambra) would then work fine. No se encontró una imagen adecuada para esta pregunta.
- **q-16211** (classic-literature) Cada primavera, cientos de casetas como estas llenan de libros un famoso parque de Madrid. ¿Cuál? → El Retiro: None of the candidates shows the Madrid Book Fair stalls. They are from book fairs in Hyderabad, Juliaca, Assam and Kolkata, and several show food stalls, Telugu signs or a Penguin Random House sign. The question says «casetas como estas», so the essential image has to show the Feria del Libro's own white stalls, and no new search is allowed. The fix is to find a Commons photo of the Feria del Libro de Madrid stalls without signs naming the park, or to switch the role to illustrative or decorative and reword the question. No se encontró una imagen adecuada para esta pregunta.
- **q-16224** (comics-and-childrens-books) En la película «Superlópez» (2018), con Dani Rovira, el héroe llega de bebé desde otro planeta. ¿Desde cuál? → Chitón: Hint 2 ("its name is also a word you say to ask for silence") gives the answer away: of Krypton, Namek, Melmac and Chitón, only Chitón is a Spanish word, so anyone who speaks Spanish gets it from hint 2. Hint 2 should be vaguer, for example about how the planet appears in Jan's comics, and the silence wordplay should be kept for hint 3 only.
- **q-16232** (empire) Viendo «La ruta hacia El Dorado» parece que El Dorado es una ciudad, pero al principio el nombre se refería a otra cosa. ¿A quién? → Un jefe indígena cubierto de polvo de oro: Hint 1 gives the answer away. «Era una persona que vivía en América antes de que llegaran los españoles» rules out all three wrong answers: the Spanish king and the English pirate didn't live in pre-conquest America, and an Inca god isn't a person. Hint 1 should be vague, for example about the era or the conquistadors' expeditions, and should leave the options open.
- **q-16242** (fiestas) El 6 de julio a mediodía, el chupinazo abre los Sanfermines de Pamplona. ¿Qué es el chupinazo? → Un cohete: The text is fine, but none of the image candidates shows Pamplona or the Sanfermines. They are crowds in Prague's Old Town Square, the Queen in Grimsby, a First World War parade in Adelaide and an open-air cinema in Tartu. A new search could try "San Fermin Pamplona" or "Pamplona Plaza Consistorial". No se encontró una imagen adecuada para esta pregunta.
- **q-16244** (flamenco-and-copla) ¿En qué década salió la canción «Mi carro», de Manolo Escobar? → En los años 60: None of the media candidates works and no new search is allowed. Candidates 2–6 are night shots of a modern civic centre in Tirol, Austria, and 1 is a portrait scan from a 1902 book. Neither fits a Spanish 1960s song or a verbena. The text itself is acceptable: as far as I know, «Mi carro» came out in 1969, so the Moon-landing hint holds. No se encontró una imagen adecuada para esta pregunta. Verificación de datos: uncertain. The answer (1960s) is right. Secondary sources date 'Mi carro' to 1969, which fits the moon-landing hint. I found no original release record, and some sources may say 1968, so the 'same year as the Moon landing' hint is unverified.
- **q-16303** (regions-and-provinces) Mira a este deportista cortando un tronco con un hacha, subido encima. ¿De qué comunidad es típico este deporte rural? → Del País Vasco: No candidate shows an aizkolari: the essential image needs a photo of a Basque wood chopper standing on a log and cutting it with an axe, and no new search is allowed. Try a search such as "aizkolari" or "Basque wood chopping" and pick a clear photo with no place names visible. No se encontró una imagen adecuada para esta pregunta.
- **q-16325** (comics-and-childrens-books) ¿Qué héroe de tebeo, creado por Manuel Gago en 1944, vive sus aventuras en la España de los Reyes Católicos? → El Guerrero del Antifaz: The fun fact says Gago was "solo 19 años" when he started El Guerrero del Antifaz. He was born in 1925 with no confirmed exact date, so in 1944 he was 18 or 19. Change it to "tenía solo 18 o 19 años" or "era un chaval de apenas 19 años como mucho". The rest checks out: answer, creator, 1944 and the Reyes Católicos setting. Verificación de datos: uncertain. Answer, creator, year and setting are right. The fun fact says Gago was 19, but he was born in 1925 with no exact date, so he was 18 or 19 in 1944. Lambiek puts the launch in October 1944.
- **q-16346** (monuments) Mira este palacio, el de la Zarzuela, en el monte de El Pardo, cerca de Madrid. ¿Quién tiene en él su residencia oficial? → El rey de España: None of the candidates shows the Palacio de la Zarzuela. All three are photos of the Palacio Real de Madrid, a different building, and new searches are not allowed. The slot needs a real exterior photo of Zarzuela; a search like "Palacio de la Zarzuela" on Commons should find one. The rater also suggests making the role illustrative, since the text already names the palace. No se encontró una imagen adecuada para esta pregunta.
- **q-16379** (rivers-and-mountains) Si recorres el Parque Natural de las Lagunas de Ruidera, ¿cuántas lagunas encadenadas, unidas por cascadas, puedes ver? → Unas 15: Hint 2 («Se cuentan con los dedos de las manos y algún pie», i.e. a bit over 10) already picks «Unas 15» out of 3/15/60/200, so it gives the answer away before hint 3, which then says the same thing again. Hint 2 should stay vague, e.g. about the lagoons being lined up along the upper Guadiana valley, with no number range in it.
- **q-16386** (spanish-cinema) ¿En qué año se estrenó «Los otros», la película de fantasmas de Alejandro Amenábar con Nicole Kidman? → 2001: Hint 1 («Se estrenó en el cambio de siglo») gives the answer away: 2001 is the only option anywhere near the year 2000, so the first hint already rules out 1985, 1991 and 2011. Replace it with a vague hint that doesn't point to the turn of the century, for example one about Amenábar's career stage or the film's Goya awards without a date.
- **q-16387** (spanish-cinema) ¿Cuál de estos actores NUNCA ha ganado el Goya al mejor actor protagonista? → Dani Rovira: None of the media candidates fit: two show an F-117 stealth fighter and four show a French colonial campaign medal. Nothing relates to the Goya Awards or Spanish cinema, and no new search is allowed. The slot needs a Goya bust or a Spanish cinema or film-set image, for example the query "Goya Award statuette". No se encontró una imagen adecuada para esta pregunta.
- **q-16401** (team-and-traditional-sports) En balonmano, ¿cuántos jugadores tiene cada equipo en la pista, contando al portero? → 7: None of the media candidates shows handball. They show ice-hockey nets and games (2, 4, 5, 6), a football pitch (3) and a toy goal in a park (1). No new search is allowed, so the image slot needs a handball picture, for example from the search "handball match indoor" or "handball goalkeeper". The question text itself is fine. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 1, cause_effect 9, count 8, estimate 6, identify 37, made_of 11, name_concept 22, odd_one_out 17, origin 22, purpose 15, record 3, sequence 13, when 24, who 35, word_meaning 21
- stimulus: detail 7, map_outline 3, none 195, photo 39
- clue: completion 10, direct 107, riddle 29, scenario 39, three_facts 59
- answer_kind: group 33, number 17, person 50, place 29, thing 44, time 25, word 46
- lens: body_senses 5, educational_media 27, everyday 25, history 32, language 43, nature 18, pop_culture 43, school 34, university 17

## Dropped by the pipeline

- 20th-century-3: overlap like q-12276: Miliki saludaba a los niños con «¿Cómo están ustedes?» en «El gran circo de TVE». ¿En qué década empezó ese programa? → En los años 70: Gaby, Fofó y Miliki empezaban su programa gritando «¿Cómo están ustedes?». ¿Qué les contestaban los niños? → «¡Bieeen!»
- 20th-century-5: overlap like q-13331: Es hijo de Julio Iglesias, se crió en Miami y debutó en 1995 con «Si tú te vas». ¿En qué ciudad nació Enrique Iglesias? → Madrid: El cantante de «Bailando» y «Hero» es hijo de otro cantante español famosísimo. ¿De quién? → Julio Iglesias
- 20th-century-6: overlap like q-1987: Es una avenida de Madrid, se empezó a construir en 1910 y la llaman 'el Broadway madrileño' por sus teatros. ¿Cuál es? → La Gran Vía: Empieza en la calle de Alcalá junto al edificio Metrópolis, pasa por Callao con su letrero luminoso de Schweppes y acaba en la plaza de España. ¿Qué calle es? → La Gran Vía
- 20th-century-12: overlap like q-11156: Soy una agencia de espías llena de desastres. Mi jefe es el Súper y mis agentes más famosos son Mortadelo y Filemón. ¿Quién soy? → La T.I.A.: En los tebeos de Francisco Ibáñez, la T.I.A. tiene un jefe llamado el Súper, un inventor llamado Bacterio y dos empleados muy torpes. ¿Qué es? → Una agencia secreta de espías
- 20th-century-17: overlap like q-10020: Es transparente, tiene burbujas y un toque dulce. Mezclada con vino tinto da el tinto de verano. ¿Qué es? → La gaseosa: Es española, su anuncio decía «Si no hay Casera, nos vamos» y se mezcla con vino para hacer tinto de verano. ¿Qué tipo de bebida es La Casera? → Una gaseosa
- al-andalus-and-reconquista-13: overlap like al-andalus-and-reconquista-4: La plaza de Zocodover, en Toledo, debe su nombre a un antiguo mercado donde se compraban y vendían animales. ¿De qué época viene ese nombre? → De la época de al-Ándalus: Estás en la Albufera de Valencia, rodeado de arrozales. ¿En qué época se extendió el cultivo del arroz por esta zona? → En la época de al-Ándalus
- bourbons-and-19th-century-5: overlap like q-15235: «La maja desnuda» le costó a Goya una citación de la Inquisición. ¿Cuál de estos cuadros NO pintó él? → «La Venus del espejo»: Mira el cuadro: es «La maja vestida», que está en el Museo del Prado. ¿Quién lo pintó? → Francisco de Goya
- bourbons-and-19th-century-7: overlap like q-14286: Goya pintó este perro directamente sobre la pared de una casa a las afueras de Madrid. ¿Cómo se llamaba esa casa? → La Quinta del Sordo: Mira este detalle de «El perro», una de las Pinturas negras de Goya. ¿Dónde pintó Goya estas obras? → En las paredes de su casa
- cities-and-towns-2: overlap like q-14349: Ana Belén y Víctor Manuel le cantaron a un monumento de Madrid: «Ahí está, ahí está…». ¿Qué rey lo mandó construir? → Carlos III: Completa la canción de Ana Belén y Víctor Manuel: «Mírala, mírala, mírala, mírala, la Puerta de…» → Alcalá
- cities-and-towns-5: overlap like q-9923: El 12 de octubre, Fiesta Nacional de España, también se celebra a la patrona de Zaragoza. ¿Qué Virgen es? → La Virgen del Pilar: Sevilla es a la Giralda como Zaragoza es a… → La basílica del Pilar
- cities-and-towns-7: overlap like q-1267: Es una palabra francesa, aparece en muchas etiquetas de vino y hay cientos junto al río Loira. ¿Qué significa 'château'? → Castillo: En fiestas catalanas, la gente se sube a los hombros de otros y un niño corona la cima. Lo llaman «castell». ¿Qué significa? → Castillo
- cities-and-towns-12: overlap like q-0320: En Año Nuevo, ¿cuántas uvas se comen a las doce de la noche? → 12: Estás en la Puerta del Sol en Nochevieja y empiezan las campanadas. ¿Cuántas uvas tienes que comerte? → 12
- cities-and-towns-13: overlap like q-12293: En 1936, en la Universidad de Salamanca, su rector le plantó cara al general Millán Astray con la frase «Venceréis, pero no convenceréis». ¿Quién era? → Miguel de Unamuno: Soy bilbaíno, nací en 1864, fui rector de la Universidad de Salamanca y escribí «Niebla». ¿Quién soy? → Miguel de Unamuno
- cities-and-towns-14: overlap like q-9996: Mira esta crema fría con huevo y jamón por encima. ¿De qué comunidad es típica? → Andalucía: Es una crema fría de tomate, pan, ajo y aceite, más espesa que el gazpacho, que se sirve con huevo duro y jamón. ¿De qué ciudad es? → Córdoba
- cities-and-towns-16: overlap like q-13449: San Sebastián es a la Concha de Oro como el Festival de Cine de Huesca es al… → Danzante: El gran premio del Festival de Cine de San Sebastián es la… de Oro. ¿Qué palabra falta? → Concha
- classic-literature-6: overlap like q-0116: ¿Quién escribió 'Don Quijote de la Mancha'? → Miguel de Cervantes: El Día del Libro, el 23 de abril, recuerda a este escritor, que murió por esas fechas de 1616 y escribió el Quijote. ¿Quién es? → Miguel de Cervantes
- classic-literature-16: overlap like q-5583: This statue shows a famous knight from La Mancha on his skinny horse. Who is the round man on the donkey beside him? → Sancho Panza: En este monumento de la plaza de España de Madrid, uno de los personajes no para de soltar refranes. ¿Cuál? → Sancho Panza
- coasts-and-islands-0: overlap like q-13473: Mira estos espetos de sardinas asados en la arena. ¿De qué ciudad son típicos? → Málaga: Se ensartan sardinas en una caña y se asan junto a una hoguera en la arena de las playas de Málaga. ¿Cómo se llama esto? → El espeto
- coasts-and-islands-13: overlap like q-9995: En Galicia se pagan muy caros los percebes. ¿Qué es un percebe? → Un crustáceo pegado a las rocas: Vivo pegado a las rocas donde rompen las olas, parezco un dedito con una uña y en Galicia se juegan la vida para cogerme. ¿Qué soy? → El percebe
- coasts-and-islands-17: overlap like q-14404: En «Juego de tronos», el islote de San Juan de Gaztelugatxe, en Bizkaia, se convirtió en otro lugar. ¿En cuál? → Rocadragón: Para llegar a la ermita de San Juan de Gaztelugatxe, sobre un islote de Bizkaia, hay que subir una escalera. ¿Cuántos escalones tiene, más o menos? → Unos 240
- current-music-6: overlap like q-14269: Estás en una boda y suena «Despechá», de Rosalía. ¿En qué década salió esa canción? → En los años 2020: «Despechá» fue una de las canciones del verano de 2022 en España. ¿Quién la canta? → Rosalía
- current-music-10: overlap like q-13269: ¿Quién es este cantante, que salió de Operación Triunfo 2017 y fue a Eurovisión 2018 junto a Amaia? → Alfred García: Se conocieron en Operación Triunfo, eran pareja y cantaron «Tu canción» en Eurovisión 2018. ¿Quiénes eran? → Amaia y Alfred
- current-music-13: duplicate like q-15226: Mira el cuadro: Goya pintó a la gente luchando contra los soldados de Napoleón el 2 de mayo de 1808. ¿En qué ciudad pasó? → Madrid: Este cantante de la foto, Omar Montes, presume siempre de su barrio. ¿En qué ciudad está? → Madrid
- current-music-16: overlap like q-16229: En Eurovisión 2023 fue Blanca Paloma, y en 2025, Melody. ¿Quién representó a España en 2024? → Nebulossa: De niña cantó «El baile del gorila» y en 2025 representó a España en Eurovisión. ¿Quién es esta cantante? → Melody
- empire-5: overlap like q-14234: Mira el retrato: un archipiélago de Asia, español hasta 1898, lleva el nombre de este rey. ¿Quién es? → Felipe II: Tengo más de 7000 islas en Asia, fui española durante más de tres siglos y llevo el nombre de un rey de España. ¿Quién soy? → Filipinas
- empire-10: overlap like q-12387: Me casé en secreto con mi primo Fernando, conquistamos juntos Granada y le pagué el viaje a Cristóbal Colón. ¿Quién soy? → Isabel la Católica: Isabel la Católica fue reina de Castilla, se casó con Fernando de Aragón y, según la leyenda, ofreció sus joyas para pagar algo. ¿Qué? → El viaje de Colón
- empire-13: overlap like q-12371: En la fachada de la Universidad de Salamanca hay una ranita de piedra que todos buscan. ¿Sobre qué está sentada? → Sobre una calavera: Esta fachada de piedra labrada es la de la universidad más antigua de España que sigue abierta. ¿En qué ciudad está? → Salamanca
- fiestas-4: overlap like q-9945: ¿Cuánto dura más o menos un encierro de San Fermín, desde que salen los toros hasta que entran en la plaza? → Unos 3 minutos: Cada mañana de Sanfermines, los toros salen de unos corrales y corren con los mozos unos 850 metros por Pamplona. ¿Adónde llegan al final? → A la plaza de toros
- legends-and-superstitions-1: overlap like q-10289: En los mercados de México venden el «ojo de venado» para colgárselo a los bebés. ¿Para qué sirve, según la tradición? → Para protegerlos del mal de ojo: En muchas tiendas de España venden el «ojo turco», un colgante de cristal azul. Según la tradición, ¿para qué sirve? → Para protegerte del mal de ojo
- legends-and-superstitions-4: overlap like fiestas-3: La noche de San Juan, con hogueras en la playa, es la víspera del día de San Juan. ¿Qué día es San Juan? → El 24 de junio: Estás en la playa, escribes tus deseos en un papel y lo quemas en una hoguera. ¿Qué noche es? → La noche de San Juan
- legends-and-superstitions-9: overlap like q-12371: En la fachada de la Universidad de Salamanca hay una ranita de piedra que todos buscan. ¿Sobre qué está sentada? → Sobre una calavera: En la fachada de la Universidad de Salamanca se esconde una rana tallada sobre una calavera. Según la tradición, ¿qué le pasa a quien la encuentra? → Que aprobará los exámenes
- modern-literature-13: overlap like q-15295: «La catedral del mar», de Ildefonso Falcones, se ambienta mientras se construye la iglesia de Santa María del Mar en Barcelona. ¿En qué siglo? → En el siglo XIV: La novela «La catedral del mar», de Ildefonso Falcones, cuenta cómo se construyó esta iglesia de Barcelona. ¿Cuál es? → Santa María del Mar
- modern-literature-15: overlap like q-11153: ¿Quién recopiló los «Cuentos al amor de la lumbre», una gran colección de cuentos populares españoles? → Antonio Rodríguez Almodóvar: Antonio Rodríguez Almodóvar reunió en «Cuentos al amor de la lumbre» cuentos populares de toda España. ¿De dónde los sacó, sobre todo? → De la gente que los contaba de memoria
- money-and-services-3: overlap like q-15633: Mira a este trabajador. ¿Qué reparte en las casas? → Cartas y paquetes: Echas una carta en un buzón amarillo de Correos. ¿Quién acaba llevándola a la casa de destino? → El cartero
- money-and-services-12: overlap like q-14275: En España, si un inquilino deja de pagar el alquiler y un juez le obliga a dejar el piso, ¿cómo se llama eso? → Un desahucio: En un piso de alquiler, «casero» es al dueño como «…» es a quien vive en él y paga cada mes. → Inquilino
- money-and-services-14: overlap like q-11348: En un bloque de pisos en España, ¿qué es el «portero automático»? → El aparato para abrir el portal desde casa: ¿Cuál de estos nombres NO se usa en España para el aparato del portal con el que abres a quien llama? → Buzón
- monuments-2: overlap like q-2238: Who designed this colorful park in Barcelona? → Antoni Gaudí: Mira esta casa de Barcelona, la Casa Batlló, con un tejado que parece el lomo de un dragón. ¿Quién la diseñó? → Antoni Gaudí
- monuments-6: overlap like q-15315: Mira la foto de la Terminal 4 del aeropuerto de Madrid-Barajas. ¿Qué arquitecto británico la diseñó con el Estudio Lamela? → Richard Rogers: Mira este enorme edificio de Madrid, con techo ondulado de madera y columnas de colores. ¿Para qué sirve? → Para coger aviones
- monuments-8: overlap like q-15399: Esta virgen negra, «la Moreneta», es la patrona de Cataluña. ¿En qué montaña está su monasterio? → Montserrat: Mira estas rocas con forma de dientes de sierra, al noroeste de Barcelona. ¿Qué montaña es? → Montserrat
- monuments-13: overlap like q-16193: Mira la foto: es una de las fuentes del Paseo del Prado de Madrid. ¿Qué se celebra en ella? → Los títulos del Atlético de Madrid: Mira esta fuente de Madrid, la de Neptuno. ¿Qué aficionados se reúnen aquí para celebrar sus títulos? → Los del Atlético de Madrid
- painting-and-architecture-2: overlap like q-10090: Estás de visita en la Ciudad de las Artes y las Ciencias de Valencia. ¿Cuál de estos edificios NO forma parte de ella? → El Museo Guggenheim: Paseas por el Paseo del Prado de Madrid, el llamado «Triángulo del Arte». ¿Cuál de estos museos NO forma parte de él? → El Museo Guggenheim
- painting-and-architecture-14: overlap like q-5349: The daisy-shaped Chupa Chups lollipop logo was designed in 1969 by a famous Spanish painter. Who? → Salvador Dalí: Salvador Dalí dibujó el logotipo de Chupa Chups en 1969, en menos de una hora, con forma de margarita. ¿De qué colores es? → Amarillo y rojo
- painting-and-architecture-15: overlap like q-1331: Está pintado sobre roca, tiene miles de años y lo hay en Chiribiquete y en Altamira. ¿Cómo se llama este arte? → Arte rupestre: Los bisontes de Altamira son el ejemplo más famoso de un tipo de arte. ¿Cómo se llama el arte pintado en cuevas y rocas? → Arte rupestre
- pop-and-rock-7: overlap like q-12259: Este cantante de Linares representó a España en Eurovisión en 1966 y 1967 y triunfó con «Mi gran noche». ¿Quién es? → Raphael: Me cantó Raphael en 1967 y en las fiestas todo el mundo grita conmigo «¿Qué pasará? ¿Qué misterio habrá?». ¿Qué canción soy? → «Mi gran noche»
- protected-areas-13: overlap like q-13397: Cada otoño, pastores y miles de ovejas cruzan el centro de una ciudad por una antigua cañada. ¿Qué ciudad es? → Madrid: Las protegía el Concejo de la Mesta desde la Edad Media, y aún hoy, cada otoño, un rebaño de ovejas cruza por una de ellas el centro de Madrid. ¿Qué son? → Las cañadas reales
- radio-and-internet-0: overlap like q-15268: ¿Qué streamer organiza La Velada del Año, el evento de boxeo entre creadores de contenido? → Ibai Llanos: Cada Nochevieja, muchos jóvenes no ven las campanadas en la tele, sino en un directo de Twitch. ¿Qué streamer las presenta? → Ibai Llanos
- regional-symbols-5: overlap like q-11265: El Estatuto de autonomía del País Vasco de 1979 lleva el nombre de la villa donde está este árbol. ¿Qué villa es? → Gernika: Es un roble, junto a él los señores de Vizcaya juraban respetar los fueros y hoy jura su cargo el lehendakari. ¿En qué localidad está? → Gernika
- regions-and-provinces-1: overlap like q-10004: La montaña más alta de España está en la isla de Tenerife. ¿Cómo se llama? → Teide: Mira este volcán nevado que asoma sobre las nubes de una isla española. ¿Cómo se llama? → El Teide
- regions-and-provinces-4: overlap like q-12264: Estás en el Patio de los Leones de la Alhambra. ¿En qué siglo se construyó? → En el siglo XIV: Esta fuente está rodeada de leones de piedra. ¿En qué monumento español se encuentra? → En la Alhambra
- regions-and-provinces-10: overlap like q-10041: ¿En qué ciudad se celebran las Fallas, en las que se queman enormes figuras cada mes de marzo? → Valencia: Se levantan enormes figuras de cartón y madera, retumban las mascletás y todo arde la noche del 19 de marzo. ¿En qué ciudad? → Valencia
- regions-and-provinces-16: overlap like q-9945: ¿Cuánto dura más o menos un encierro de San Fermín, desde que salen los toros hasta que entran en la plaza? → Unos 3 minutos: El encierro de San Fermín va desde los corrales hasta la plaza de toros. ¿Cuánto mide su recorrido, más o menos? → Unos 850 metros
- classic-literature-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En este cortijo de Almería, en 1928, una novia se fugó con su primo la víspera de su boda. ¿Qué obra de teatro inspiró aquella noticia? → Bodas de sangre
- classic-literature-15: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Ni como ni dejo comer, y Lope de Vega me usó como título de una comedia. ¿De quién soy perro? → Del hortelano
- empire-9: overlap like q-16174: En la serie «Isabel» de TVE, la boda de la protagonista con Fernando en 1469 acaba uniendo dos grandes coronas. ¿Cuáles? → Castilla y Aragón: Nací en un pueblo de Zaragoza que hoy lleva mi apodo, fui rey de Aragón y con mi esposa conquisté Granada en 1492. ¿Quién soy? → Fernando el Católico
- empire-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En 1529, los príncipes alemanes que seguían a Lutero se opusieron por escrito a una decisión tomada en nombre de Carlos I. ¿Qué nombre les quedó? → Protestantes
- fiestas-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Los nazarenos de Semana Santa, con túnica y capirote, toman su nombre de una persona. ¿De quién? → De Jesús de Nazaret
- fiestas-16: overlap like q-16237: Estás en la verbena de tu pueblo, bailando con la orquesta en la plaza. ¿Cuándo suele ser una verbena? → De noche: Llega a la plaza del pueblo en un camión que se convierte en escenario y toca éxitos para bailar hasta la madrugada. ¿Qué es? → La orquesta de verbena
- modern-literature-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: La escribió Alejandro Casona en el exilio, transcurre en una aldea de Asturias y en ella una misteriosa peregrina resulta ser la Muerte. ¿Qué es «La dama del alba»? → Una obra de teatro
- money-and-services-8: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: ¿Qué día es fiesta en toda España por el Día del Trabajador? → El 1 de mayo
- painting-and-architecture-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Este perro gigante cubierto de flores vigila la entrada de un famoso museo. ¿En qué ciudad está? → Bilbao
- painting-and-architecture-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿En qué año pintó Juan Genovés «El abrazo», el cuadro que se convirtió en símbolo de la Transición española? → En 1976
- pop-and-rock-4: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: ¿Cómo se llama el grupo de San Sebastián que, con Amaia Montero de cantante, sacó «Dile al sol» en 1998? → La Oreja de Van Gogh
- protected-areas-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Nací en Jauja, en Córdoba, a comienzos del siglo XIX. Fui bandolero en Sierra Morena y decía que en la sierra mandaba yo. Al final el rey Fernando VII me indultó. ¿Quién soy? → El Tempranillo
- radio-and-internet-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Qué cadena de radio española pertenece sobre todo a la Iglesia católica, a través de sus obispos? → COPE
- scientists-and-explorers-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Completa: en 2022, la investigadora leonesa Sara García Alonso se convirtió en la primera mujer española en la reserva de… → astronautas de Europa
- spanish-cinema-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: «Spanish Movie» (2009) recrea escenas de «El orfanato» y «Los otros», pero cambia los sustos por chistes. ¿Qué tipo de película es? → Parodia
- sportspeople-0: overlap like q-14446: Antes se llamaba natación sincronizada, se compite con una pinza en la nariz y Gemma Mengual ganó medallas en ella. ¿Qué mezcla con la natación? → Danza y gimnasia: La barcelonesa Ona Carbonell ganó en Londres 2012 una plata en dúo y un bronce por equipos, y entrenaba oyendo música bajo el agua. ¿Cuál es su deporte? → Natación artística
- sportspeople-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: La gallega Ana Peleteiro ganó el bronce en Tokio 2020 y además batió el récord de España. ¿En qué prueba? → Triple salto
- sportspeople-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Este equipo español ganó el Mundial sub-19 de baloncesto de 1999 en Lisboa, con Pau Gasol y Juan Carlos Navarro. ¿Qué apodo tiene? → Los Juniors de Oro
- team-and-traditional-sports-4: overlap like q-11381: Soy piloto de motos, nací en Cervera y me llaman «la Hormiga». En las curvas me tumbo tanto que rozo el asfalto con el codo. ¿Quién soy? → Marc Márquez: ¿Qué piloto de MotoGP, varias veces campeón del mundo, es conocido como «la Hormiga de Cervera»? → Marc Márquez
- team-and-traditional-sports-15: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: El equipo de Memphis donde jugaron Pau y Marc Gasol lleva el nombre de un animal. ¿Cuál? → El oso pardo
- rivers-and-mountains-4: overlap like q-14366: En el techo de la cueva de Altamira, en Cantabria, hay bisontes rojos y negros pintados hace unos 14 000 años. ¿Con qué se hicieron esos colores? → Con tierra rojiza y carbón: Estás en la cueva de Altamira, en Cantabria, mirando bisontes pintados en el techo. ¿Cuándo se pintaron? → Hace unos 15 000 años
- rivers-and-mountains-5: overlap like q-9986: El oso pardo de la cordillera Cantábrica come muchísimas bellotas y castañas en otoño, engorda y busca una cueva. ¿Para qué? → Para dormir buena parte del invierno: Mira la foto: ¿en qué cordillera de España vive la mayoría de estos animales? → La Cordillera Cantábrica
- rivers-and-mountains-7: overlap like q-0945: Estás explorando una cueva: una estalactita crece desde el techo y una estalagmita desde el suelo. Cuando por fin se tocan, ¿qué forman? → Una columna: Mira la foto: estas puntas de piedra cuelgan del techo de una cueva, como en las Cuevas del Drach de Mallorca. ¿Cómo se llaman? → Estalactitas
- rivers-and-mountains-12: overlap like q-7509: En una vuelta ciclista, ¿qué clasificación da puntos al primero que pasa por la cima de los puertos? → Gran Premio de la Montaña: Navacerrada, Somosierra y Pajares son pasos de carretera entre montañas que la Vuelta ciclista sube a menudo. ¿Qué nombre reciben? → Puertos
- rivers-and-mountains-13: overlap like q-10006: Separan España de Francia, en medio está Andorra y su pico más alto es el Aneto. ¿Qué cordillera es? → Los Pirineos: Es la montaña más alta de los Pirineos, está en Huesca y, para llegar a su cima, hay que cruzar el estrecho «Puente de Mahoma». ¿Cuál es? → El Aneto
- rivers-and-mountains-17: duplicate like q-13268: Este cantante, Manuel Carrasco, salió de Operación Triunfo y es de Isla Cristina. ¿En qué provincia está su pueblo? → Huelva: Mira la foto: este río de aguas rojas por los minerales es famoso por sus minas. ¿En qué provincia está? → Huelva
- scientists-and-explorers-15: overlap like q-2021: Estás viendo los dibujos de neuronas más famosos de la historia, hechos a mano por un Nobel de Medicina. ¿Quién los hizo? → Santiago Ramón y Cajal: Estos dibujos a tinta mostraron que las neuronas no están pegadas, sino que se comunican por contactos, las sinapsis. ¿Quién los hizo? → Santiago Ramón y Cajal
- scientists-and-explorers-17: overlap like q-1435: Están en Indonesia, Magallanes buscaba llegar a ellas y los holandeses las controlaron por siglos. ¿Qué buscaban allí los europeos? → Clavo y nuez moscada: En 1522, la Nao Victoria volvió a Sanlúcar tras la primera vuelta al mundo, cargada de un tesoro de las islas Molucas. ¿Cuál? → Clavo y otras especias
- spanish-cinema-1: overlap like q-1087: En 1307, el rey de Francia mandó arrestar a una orden de caballeros creada para proteger a los peregrinos que iban a Jerusalén. ¿Qué orden era? → Los templarios: Fuimos monjes guerreros medievales condenados por brujería. En «La noche del terror ciego» (1972) salimos de la tumba, ciegos, y cazamos guiándonos por el oído. ¿Quiénes somos? → Los caballeros templarios
- spanish-cinema-3: overlap like q-4362: At a big film awards night like the Oscars, when do the stars walk the red carpet? → Before the ceremony: Me extienden ante la entrada de los Goya o del Festival de San Sebastián, y los famosos posan sobre mí ante los fotógrafos. ¿Qué soy? → La alfombra roja
- spanish-cinema-15: overlap like q-14432: En «Lo imposible», de J. A. Bayona, una familia pasa la Navidad de 2004 en Tailandia. ¿Cuántos hijos tiene la pareja protagonista? → 3: Este director barcelonés rodó «Lo imposible» y «Jurassic World: El reino caído». ¿Quién es? → J. A. Bayona
- sportspeople-10: overlap like q-12479: Mira la foto: Marc Gasol y Serge Ibaka ganaron en 2019 el anillo de la NBA con el equipo de esta ciudad. ¿Cuál es? → Toronto: Mira la foto: este pívot ganó en 2019 el anillo de la NBA con los Toronto Raptors y el Mundial con España. ¿Quién es? → Marc Gasol
- sportspeople-16: overlap like q-9841: En la inauguración de los Juegos Olímpicos de Barcelona 92, un arquero disparó una flecha en llamas. ¿Para qué? → Para encender el pebetero olímpico: En la inauguración de Barcelona 92, Epi entró con la antorcha olímpica y encendió algo con ella. ¿Con qué se prendió después el pebetero? → Una flecha
- tv-series-6: overlap like q-0102: ¿Qué civilización construyó Machu Picchu? → Los incas: Machupichu sirve en el bar de Mauricio en «Aída». Su apodo es el de una ciudad de piedra en los Andes de Perú. ¿Qué pueblo la construyó? → Los incas
- tv-series-8: overlap like q-11410: Vivo en Mirador de Montepinar, vendo marisco al por mayor y siempre aclaro: «Soy mayorista, no limpio pescado». ¿Quién soy? → Antonio Recio: En «La que se avecina», Antonio Recio grita «¡Soy mayorista, no limpio pescado!». ¿Qué es un mayorista? → Quien vende en grandes cantidades a otras tiendas
- tv-series-16: overlap like q-9892: ¿En qué década se estrenó «Verano azul», la serie rodada en Nerja? → Los años 80: ¿En qué año empezó a emitir TVE «Verano azul», la serie en la que Piraña veraneaba con su pandilla? → 1981
