# batch-34

Made by `qgen batch` on 2026-11-05 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): pop-and-rock, current-music, classic-literature, modern-literature, painting-and-architecture, comics-and-childrens-books, spanish-cinema, tv-series, tv-shows-and-presenters, radio-and-internet, football-clubs, footballers-and-national-team, sportspeople, team-and-traditional-sports, regional-speech, co-official-languages, brands-and-shops, transport, school-and-home, money-and-services, national-symbols, regional-symbols, folk-music-and-dance, slang, sayings, childrens-tv, flamenco-and-copla
- Merged: 307 (q-11119…q-11425)
- Approved: 282
- Needs work: 25
- Dropped by the pipeline: 61
- Reviewed by: claude-opus-5-5
- Claude calls: 630, about $81.24 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-32, batch-33; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-32 | batch-33 | batch-34 |
|---|---|---:|---:|---:|
| source locale |  | en | de | es-ES |
| drafts |  | 367 | 375 | 368 |
| skipped slots |  | 83 | 111 | 118 |
| dropped |  | 60 | 54 | 61 |
| drop rate | ≤ 20.0 % | 16.3 % ✓ | 14.4 % ✓ | 16.6 % ✓ |
| dropped: hard fail correct |  | 1 | 8 | 3 |
| dropped: hard fail unambiguous |  | 0 | 3 | 0 |
| dropped: hard fail no_giveaway |  | 17 | 28 | 15 |
| dropped: overlap |  | 41 | 19 | 42 |
| dropped: duplicate |  | 0 | 0 | 1 |
| dropped: fact-check wrong |  | 1 | 1 | 1 |
| merged |  | 307 | 321 | 307 |
| approved |  | 281 | 295 | 282 |
| needs_work |  | 26 | 26 | 25 |
| needs_work rate | ≤ 20.0 % | 8.5 % ✓ | 8.1 % ✓ | 8.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.9 % ✓ | 1.9 % ✓ | 2.6 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.6 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 1.6 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 5.5 % ✓ | 3.7 % ✓ | 4.9 % ✓ |
| media: no pick in review 1 |  | 38 | 45 | 51 |
| media: recovered by research |  | 25 | 39 | 39 |
| media: no pick at record |  | 14 | 6 | 12 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 11.4 % ✓ | 6.4 % ✓ | 11.7 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 71.3 % ✓ | 72.8 % ✓ | 70.6 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 2.29 ✗ | 1.55 ✗ | 1.00 ✓ |
| approved 11–15 |  | 59 | 67 | 63 |
| top move | ≤ 25.0 % | 19.5 % ✓ | 17.4 % ✓ | 17.6 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 84.4 % | 92.5 % | 89.6 % |
| values stimulus |  | 6 | 3 | 5 |
| top clue | ≤ 60.0 % | 45.0 % ✓ | 37.7 % ✓ | 42.0 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 24.4 % ✓ | 27.4 % ✓ | 23.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 21.8 % ✓ | 20.9 % ✓ | 19.9 % ✓ |
| values lens |  | 10 | 9 | 9 |
| media share | 15.0 %–50.0 % | 15.6 % ✓ | 7.5 % ✗ | 10.4 % ✗ |
| mean fun | ≥ 3.40 | 3.56 ✓ | 3.53 ✓ | 3.43 ✓ |
| cost $ |  | $73.13 | $80.73 | $78.33 |
| $ per approved | ≤ $0.35 | $0.26 ✓ | $0.27 ✓ | $0.28 ✓ |
| calls |  | 580 | 591 | 570 |
| calls per approved |  | 2.06 | 2.00 | 2.02 |
| wall time h |  | 2.60 | 3.07 | 2.96 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 55 (2 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 6 (2 major), fact 2 (0 major), overlap 1 (1 major), media 2 (2 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.92

Major findings on approved questions:

- **q-11134**: giveaway — Hint 1 ("novela anónima del siglo XVI") rules out all three wrong answers at once: 1499 is in the 15th century, and 1605 and 1626 are in the 17th. That leaves 1554 as the only option, so the first hint solves the question instead of just narrowing it. The facts check out: Lazarillo was published in 1554, the squire's toothpick scene and Lázaro begging to feed him are both in the third chapter (tratado III), and the wrong answers are the years of La Celestina, the Quijote and El Buscón. The media and the description are fine. (http://127.0.0.1:8001/review/q-11134)

## Needs work

- **q-11145** (co-official-languages) La lengua oficial en toda España tiene dos nombres: «español» y… ¿cuál más? → Castellano: Hints 1 and 2 give the answer away. Hint 1 («Es la lengua de esta pregunta») tells players the answer is the language they're reading, and that rules out Catalán, Gallego and Euskera at once. Hint 2 (the language of the Quijote) does the same. Hint 1 should be vague (for example, that most people in Latin America speak it too, or how old the name is), and hint 2 should not point straight to Spanish.
- **q-11147** (co-official-languages) Completa el nombre oficial en valenciano de esta capital de provincia: «Castelló de la …». → Plana: Hint 2 ("La palabra describe un terreno sin montañas") gives the answer away: any Spanish speaker hearing it picks «Plana» straight away and rules out «Serra». It should be a vaguer hint, such as one about the Magdalena festival or the province's location on the coast, and the flat-land clue should only come in hint 3. The facts are fine (Castelló de la Plana, the move down from the hill in 1251, the Magdalena festival).
- **q-11148** (co-official-languages) En la comunidad de este mapa, para dar las gracias se dice «grazas». ¿Cuál es? → Galicia: The essential slot needs a map of Spain with Galicia highlighted, but none of the candidates is a map: they are a dragonfly, a Braille sign, a playground, the Torre de Hércules, the Miño river and a street tree in Santiago. A new search isn't allowed, so the slot needs a locator map (e.g. "Galicia in Spain locator map" on Commons) chosen by hand, or the question should drop «de este mapa» and use an illustrative image. No se encontró una imagen adecuada para esta pregunta.
- **q-11156** (comics-and-childrens-books) Soy una agencia de espías llena de desastres. Mi jefe es el Súper y mis agentes más famosos son Mortadelo y Filemón. ¿Quién soy? → La T.I.A.: Verificación de datos: wrong. Hint 1 is false: Mortadelo y Filemón (and the T.I.A.) first appeared in 1958 in Pulgarcito, not in the late 1960s.
- **q-11172** (flamenco-and-copla) Mira este detalle. ¿Quién suele llevar esto? → Una bailaora de flamenco: None of the candidates is the close-up of a big flower in pinned-up hair that this essential slot needs. Candidates 1, 2, 5 and 6 are old drawings or paintings of hairstyles, 3 is a girl in a white communion or wedding dress with a flower crown, and 4 is a full-body dancer in a red dress with no flower visible. A new search is not allowed here. No se encontró una imagen adecuada para esta pregunta.
- **q-11174** (flamenco-and-copla) Escucha: ¿qué sonido flamenco es este? → Un zapateado: None of the audio candidates is a solo zapateado recording. #1 and #3 are pronunciation clips ('footwork', 'Flamenco'), #2 is a guitar piece, #4 is palmas (one of the wrong answers), and #5 and #6 are MIDI files of the flamenco mode. No new search is allowed, so this essential audio slot needs a real zapateado recording (for example from Freesound, 'zapateado flamenco'). No se encontró una imagen adecuada para esta pregunta.
- **q-11175** (folk-music-and-dance) Es Navidad y en casa cantas «Los peces en el río». Según la canción, ¿qué hacen los peces una y otra vez? → Beben: Hint 2 («Es algo que haces cuando tienes sed») gives the answer away: of the four options, only «Beben» is what you do when you're thirsty. It's also stronger than hint 3, so the hints don't go from vague to strong. Hint 2 should be vaguer, for example about the carol's tune or chorus, and hint 3 can stay as it is.
- **q-11188** (football-clubs) En 2005, el Bernabéu entero aplaudió a este brasileño del Barça tras marcar dos golazos. ¿Quién es? → Ronaldinho: The media slot is 'essential' and its note asks for a clear photo of Ronaldinho's face, but every candidate is a photo of the Bernabéu stadium, and no new search is allowed. The question doesn't need his photo. Changing the role to 'illustrative' would fix it, and candidate 1 (empty Bernabéu, no names on show) would then be a good pick. The text, facts and options are fine. No se encontró una imagen adecuada para esta pregunta.
- **q-11205** (modern-literature) ¿Cómo se llama el niño que narra «Los Futbolísimos» y juega en el Soto Alto? → Pakete: Hint 2 ("Su apodo suena a algo que trae el cartero") gives the answer away. Against Manolito, Teo and Pepito, only Pakete sounds like «paquete», so hint 2 already solves the question and hint 3 just repeats it. Hint 2 should give a vaguer clue, for example his role in the team (he usually sits on the bench and isn't the star) or his real name Francisco, and leave the parcel wordplay to hint 3 only.
- **q-11210** (modern-literature) ¿En qué década empezó Elena Fortún a publicar en la revista «Gente Menuda» las historias de su famosa niña protagonista? → En la década de 1920: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-1923, PD-US-expired).
- **q-11220** (national-symbols) Es dorada, va encima del escudo en la camiseta de la selección masculina de fútbol y solo hay una. ¿Qué recuerda? → El Mundial de Sudáfrica 2010: The fact check is 'wrong': it reports that Spain won the 2026 World Cup, so the shirt now has, or will soon have, a second star. That makes 'solo hay una' and the description's 'vive sola' outdated. I can't confirm the result myself (it is after my knowledge cutoff), and either way the premise depends on a fact that changes. Rewrite it so it doesn't depend on how many stars there are (for example, ask where the 2010 World Cup that the first star recalls was played), or drop it. Verificación de datos: wrong. Outdated. Spain won the 2026 World Cup (1-0 over Argentina after extra time, 19 July 2026). The shirt now has or will have a second star, so 'solo hay una' and the premise are no longer true.
- **q-11221** (national-symbols) Mira la bandera de España. Comparada con cada franja roja, ¿cómo es la franja amarilla del centro? → El doble de ancha: None of the candidates shows the current flag of Spain, flat and from the front, so the essential image can't be filled. A new search isn't allowed this round. The slot needs a file like "File:Flag of Spain.svg" from Commons. No se encontró una imagen adecuada para esta pregunta.
- **q-11223** (national-symbols) Mira esta moneda española de 1 euro. ¿Cuántas estrellas rodean la cara del rey? → 12: None of the candidates shows the Spanish 1-euro coin with the king's portrait, and no new search is possible. The question says «Mira esta moneda española de 1 euro», so the essential image has to be that exact coin. The text itself is fine. Options: find a Commons photo of the Spanish 1-euro coin (for example the Felipe VI or Juan Carlos I national side) and attach it by hand, or reword the question to fit candidate 3, a Spanish 2-euro coin from 1999 with Juan Carlos I. No se encontró una imagen adecuada para esta pregunta.
- **q-11229** (painting-and-architecture) Estás viendo pasar un paso de Semana Santa por la calle. ¿Quién de estos NO forma parte de la procesión? → El picador: Hint 2 ("con capotes y trajes de luces cerca") points straight at bullfighting, and the picador is the only bullfighting option, so the answer is given away at hint 2. Replace it with a vaguer hint, for example one saying the odd one out belongs to a different kind of show, without naming bullfighting gear. Also, an odd-one-out about Semana Santa roles doesn't fit the subcategory "Pintores, escultores y arquitectos".
- **q-11234** (painting-and-architecture) Este techo con estalactitas de colores cubre la Sala de los Derechos Humanos de la ONU en Ginebra. ¿Qué artista español lo creó? → Miquel Barceló: No candidate clearly shows Barceló's stalactite ceiling in Room XX, and this essential slot needs it. Candidate 1 is Room XX, but the photo is mostly seats, with only a thin strip of the ceiling at the top. Candidates 4 and 5 show the metal-panel ceiling of Room XIX, a different room. A new search isn't allowed, so the media needs a manual pick, for example a Commons photo looking up at the Room XX ceiling. No se encontró una imagen adecuada para esta pregunta.
- **q-11274** (co-official-languages) En una tienda de Bilbao oyes «eskerrik asko». ¿Qué significa en castellano? → «Gracias»: Hint 2 («Asko» significa «mucho») gives the answer away: of the four options, only «gracias» goes with «mucho» («muchas gracias»), so the hint solves the question before hint 3. The rater flagged this too. Hint 2 needs a vaguer clue, for example that it's the word you say after paying or receiving something, without the «mucho» link.
- **q-11290** (folk-music-and-dance) Escucha: este instrumento de percusión llegó de Perú y Paco de Lucía lo metió en el flamenco. ¿Cuál es? → El cajón: None of the audio candidates is a cajón recording. They are drum-kit MIDI grooves and a Kevin MacLeod song, which the rules forbid. No new search is allowed, so the essential audio can't be filled. A solo cajón recording has to come from Freesound (e.g. "cajon solo"), or the question should switch to an essential photo of a cajón. No se encontró una imagen adecuada para esta pregunta.
- **q-11292** (football-clubs) David Villa nació en un pueblo minero y le llaman «el Guaje», que significa «chaval». ¿De qué lengua viene su apodo? → Del asturiano: None of the media candidates fits the question: they show work or hiking boots, a chainsaw scene, grass-ski boots, an Icelandic mountain and a Puss in Boots print. There are no football boots and nothing connected to Villa or football, and no new search is allowed. The slot needs a new search, e.g. "football boots close-up" or "soccer ball on pitch". No se encontró una imagen adecuada para esta pregunta.
- **q-11317** (pop-and-rock) ¿Qué dúo barcelonés de Quimi Portet cantó «Insurrección» y se separó en 1998? → El Último de la Fila: No candidate fits. 1 and 2 are early-1900s US political cartoons (the Democratic Party donkey with English captions), 3 is an 1856 satirical map of Europe and 4 is a Bible engraving of a coastal town. None of them relates to a Spanish pop-rock duo, and no new search is allowed. A better slot would be an illustrative image such as a concert stage or an electric guitar, or a clear photo of a tethered donkey. No se encontró una imagen adecuada para esta pregunta.
- **q-11321** (pop-and-rock) Lo cantaba el grupo Zapato Veloz y fue canción del verano en 1992. ¿Qué canción es? → «El tractor amarillo»: The text is fine: the song, the 1992 summer hit and the chorus «es lo que se lleva ahora» are all correct, and nothing gives the answer away. The problem is the picture. Candidate 1 is a 1902 book photo of a peasant woman from the Don region of Russia. Candidates 2–6 are night shots of a modern education centre in Kirchdorf in Tirol, Austria. None of them shows a Spanish village fiesta, and no new search is allowed. A search like "verbena pueblo orquesta" or "Spanish village festival stage" should find something that fits. No se encontró una imagen adecuada para esta pregunta.
- **q-11332** (regional-speech) En el castellano de una comunidad mediterránea con tres provincias y lengua propia se oye mucho «poquete» y «chiquete». ¿Cuál es? → Comunidad Valenciana: Hint 2 («Allí se celebran las Fallas») gives the answer away: the Fallas are known all over Spain as Valencian, so a second hint that names them ends the question. Hint 2 should point towards the answer less directly, for example the bilingual sound of the region's Spanish, without naming Valencia's signature festival. Everything else checks out: the clue (Mediterranean, three provinces, its own language) fits only the Comunidad Valenciana, and the fun fact is correct.
- **q-11371** (spanish-cinema) En «El hoyo», una plataforma con comida baja de nivel en nivel por una prisión vertical. ¿Cuántos presos hay en cada nivel? → 2: «El hoyo» is a gory, adult-rated horror film with cannibalism and violence. That breaks the house rule "nothing scary, gory or adult-only, in any age group", and at difficulty 10 young teens would get this question too. The topic doesn't fit a family game; replace it with a question about a family-friendly Spanish film.
- **q-11379** (sportspeople) Si sumas las chaquetas verdes que ganó José María Olazábal como campeón del Masters de Augusta, ¿cuántas te salen? → 2: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-no notice).
- **q-11408** (tv-series) Este actor fue Pepe, el dueño del chiringuito de Peñíscola en «Chiringuito de Pepe». ¿Quién es? → Jesús Bonilla: No candidate shows the actor Jesús Bonilla. #1 is a different man with the same name (a meditation teacher, «Tanumanasi»), and the rest are religious images and Spanish politicians. No new search is allowed, so the essential portrait slot can't be filled. Either find a proper Commons portrait of the actor (e.g. "Jesús Bonilla actor") or change the role to illustrative/decorative with a Peñíscola beach-bar image. No se encontró una imagen adecuada para esta pregunta.
- **q-11421** (tv-shows-and-presenters) TVE emite cada año el especial de humor de José Mota. ¿Qué noche suele ser? → Nochevieja: Hint 2 («toca prepararse para algo con uvas») gives the answer away: in Spain, grapes mean the twelve chimes on Nochevieja and nothing else, so it is no weaker than hint 3. Rewrite hint 2 as a middle-strength clue, for example that the special airs shortly before a big live broadcast on La 1 that the whole country watches, without mentioning the grapes, the chimes or the end of the year. La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).

## Question axes

- move: analogy 12, cause_effect 1, count 12, estimate 2, identify 54, made_of 8, name_concept 46, odd_one_out 16, origin 23, purpose 11, record 4, sequence 8, when 38, who 50, word_meaning 22
- stimulus: detail 3, map_outline 2, none 275, photo 25, sound 2
- clue: completion 9, direct 129, riddle 46, scenario 40, three_facts 83
- answer_kind: group 20, number 15, person 72, place 30, thing 71, time 39, word 60
- lens: body_senses 17, educational_media 21, everyday 59, history 55, language 51, nature 1, pop_culture 61, school 35, university 7

## Dropped by the pipeline

- brands-and-shops-14: overlap like q-1694: ¿De dónde viene el nombre de la marca japonesa Casio? → Del apellido de sus fundadores: Estás desayunando galletas Cuétara. ¿De dónde viene el nombre de la marca? → Del apellido de sus fundadores
- childrens-tv-0: overlap like q-1252: ¿Cuál de estos payasos NO formó parte de 'Los Payasos de la Tele' junto con Miliki? → Cepillín: Éramos tres hermanos, llevábamos narices rojas y cantábamos en la tele las aventuras de la gallina Turuleca. ¿Quiénes somos? → Los Payasos de la Tele
- childrens-tv-2: overlap like q-6399: In the movie Frozen, who sings “Let It Go”? → Elsa: Estás en el coche y suena «¡Suéltalo, suéltalo!», de Frozen. ¿Qué personaje la canta en la película? → Elsa
- childrens-tv-4: overlap like q-9935: Pablo Motos presenta en Antena 3 un programa con experimentos y dos marionetas, Trancas y Barrancas. ¿Cómo se llama? → El Hormiguero: Estás viendo a Pablo Motos y aparecen Trancas y Barrancas, que dan nombre a su programa. ¿Qué animales son? → Hormigas
- classic-literature-4: overlap like q-1507: ¿En qué siglo se publicó el libro que empieza «En un lugar de la Mancha, de cuyo nombre no quiero acordarme…»? → Siglo XVII: El hidalgo Alonso Quijano protagoniza una novela que se publicó por primera vez en… ¿qué siglo? → El siglo XVII
- classic-literature-13: overlap like q-9851: ¿Quién llevaba en la batalla la famosa espada Tizona? → El Cid: ¿Qué caballero castellano medieval conquistó Valencia y tenía una espada llamada Tizona? → El Cid Campeador
- classic-literature-17: overlap like q-10063: La expresión «noche oscura del alma», usada para hablar de una gran crisis interior, viene de un poema de un místico español. ¿De quién? → San Juan de la Cruz: Escribí «En una noche oscura, con ansias en amores inflamada»; fui fraile carmelita y me escapé de una prisión de Toledo. ¿Quién soy? → San Juan de la Cruz
- co-official-languages-13: overlap like q-10041: ¿En qué ciudad se celebran las Fallas, en las que se queman enormes figuras cada mes de marzo? → Valencia: Se celebra en marzo en Valencia, tiene mascletàs y sus figuras gigantes, los ninots, se queman al final. ¿Qué fiesta es? → Las Fallas
- comics-and-childrens-books-13: overlap like q-11155: Soy agente secreto, tengo solo dos pelos en la cabeza y mando sobre mi compañero, aunque él siempre me la lía. ¿Quién soy? → Filemón: Abres un tebeo de Ibáñez: Batman es a Robin como Filemón es a… → Mortadelo
- folk-music-and-dance-5: overlap like q-11173: Mira este traje de lunares y volantes. ¿Para qué se lo pone la gente en Andalucía? → Para ir a la feria: Mira este traje de flamenca: ¿cómo se llaman las tiras de tela fruncida que forman su falda? → Volantes
- folk-music-and-dance-7: overlap like folk-music-and-dance-5: Mira este traje de flamenca: ¿cómo se llaman las tiras de tela fruncida que forman su falda? → Volantes: Es el traje típico de la Feria de Abril de Sevilla, se lleva con una flor en el pelo y cambia de moda cada año. ¿Cuál es? → El traje de flamenca
- folk-music-and-dance-14: overlap like q-7200: Escucha: con este instrumento, y no con acordeón, Guillermo Buitrago grabó canciones costeñas en los años 40. ¿Cuál es? → La guitarra: Escucha: este instrumento de cuerda es el rey del flamenco. ¿Cuál es? → La guitarra
- football-clubs-6: overlap like q-0737: ¿Qué tienen en común Xavi, Iniesta y Busquets, del Barça? → Cerebros del tiki-taka: ¿Cómo se llama el estilo de juego de pases cortos y rápidos que hizo famoso al Barça de Guardiola? → Tiki-taka
- footballers-and-national-team-2: overlap like q-2548: This coach won the Champions League with both Barcelona and Manchester City. Who is he? → Pep Guardiola: Fui centrocampista del Barça, como entrenador gané con él un triplete y en Inglaterra conseguí cuatro Premier League seguidas con el Manchester City. ¿Quién soy? → Pep Guardiola
- national-symbols-12: overlap like q-9885: En España, cuando se dice que a alguien «le ha tocado el Gordo», ¿qué significa? → Ha ganado el primer premio de la lotería: ¿Cómo se llama el primer premio del Sorteo de Navidad del 22 de diciembre? → El Gordo
- painting-and-architecture-5: duplicate like q-0354: Mira este cuadro famoso, 'Las Meninas', que está en el Museo del Prado de Madrid: ¿quién lo pintó? → Diego Velázquez: Este retrato del papa Inocencio X, pintado en Roma hacia 1650, se guarda en la Galería Doria Pamphilj. ¿Quién lo pintó? → Diego Velázquez
- painting-and-architecture-9: overlap like q-0851: Según Salvador Dalí, ¿qué le inspiró los relojes blandos que se derriten en 'La persistencia de la memoria'? → Un queso camembert derretido: Estás en el MoMA de Nueva York ante un cuadro pequeño con relojes blandos que se derriten sobre un paisaje. ¿Quién lo pintó? → Salvador Dalí
- radio-and-internet-6: overlap like q-1809: ¿Qué tiene que lograr un canal de YouTube para recibir esta placa plateada? → Llegar a 100 000 suscriptores: Pulsas el botón rojo de un canal de YouTube para no perderte sus vídeos nuevos. ¿Qué pasas a ser? → Suscriptor
- regional-speech-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Viene de «chico», lleva el diminutivo dos veces y se dice mucho a los bebés. ¿Qué significa «chiquitito»? → Muy pequeño
- regional-symbols-10: overlap like q-10096: Según la leyenda, en el puerto del Suspiro del Moro el último rey nazarí de Granada suspiró al mirar por última vez su ciudad. ¿Quién era? → Boabdil: El Reino de Granada fue el último reino musulmán de la península y cayó en 1492. ¿Qué dinastía lo gobernaba? → Los nazaríes
- regional-symbols-17: overlap like q-9607: Scotland's flag, the Saltire, is a white diagonal cross on a blue background. Whose cross is it? → Saint Andrew: La bandera de Tenerife es azul con una cruz blanca en forma de aspa. ¿Qué santo da nombre a esa cruz? → San Andrés
- classic-literature-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Lleva encima una rayita ondulada, nació de abreviar dos enes en los manuscritos medievales y es símbolo del español. ¿Qué letra es? → La eñe
- classic-literature-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿En qué año se publicó «Los trabajos de Persiles y Sigismunda», la última novela de Cervantes? → 1617
- co-official-languages-3: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: En verano, en Barcelona, se oye mucho «Anem a la platja!» mientras la gente coge la toalla. ¿Adónde van? → A la playa
- co-official-languages-10: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: En Barcelona, el cartel de este edificio dice «Ajuntament». ¿Qué edificio es? → El ayuntamiento
- tv-series-8: fact-check wrong: Eduardo Gómez played Mariano Delgado in «Aquí no hay quien viva», not Mauricio Colmenero. Mauricio Colmenero is the bar owner in «Aída», played by Mariano Peña. The fun fact is also false: the videoclub in Desengaño 21 belonged to Paco, not Mauricio. Máximo Angulo is correct for La que se avecina.: Eduardo Gómez fue Mauricio Colmenero en «Aquí no hay quien viva». ¿Qué personaje interpretó después en «La que se avecina»? → Máximo Angulo
- tv-series-10: hard fail: correct 3, unambiguous 5, no_giveaway 3, no_overlap 5: Si ves en la tele dos equipos esquivando vaquillas en «El Gran Prix del verano», ¿qué representa cada equipo? → Un pueblo de España
- comics-and-childrens-books-7: overlap like q-11176: La nana «Duérmete, niño» es muy antigua, se canta para dormir a los bebés y avisa de que, si no duermes, vendrá alguien que te comerá. ¿Quién? → El coco: Se cantan bajito, sirven para dormir a los bebés y Lorca les dedicó una conferencia. ¿Cómo se llaman estas canciones? → Nanas
- current-music-4: overlap like q-0849: Soy centrocampista española: en 2023 fui campeona del mundo con mi selección, me eligieron la mejor jugadora de ese Mundial y luego gané el Balón de Oro. ¿Quién soy? → Aitana Bonmatí: Salí de Operación Triunfo, canté «Teléfono» y «Mon Amour», y me llamo igual que una futbolista Balón de Oro. ¿Quién soy? → Aitana
- flamenco-and-copla-0: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Las bailaoras lo llevan bajo, en la nuca, bien sujeto con horquillas. ¿Qué ventaja práctica tiene el moño al bailar? → Que el pelo no tapa la cara al girar
- flamenco-and-copla-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En bodegas como esta se cría el vino que medio mundo llama «sherry». ¿En qué ciudad, cuna de la bulería? → Jerez de la Frontera
- flamenco-and-copla-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Escucha: este sonido da título a una copla que cantaba el niño Joselito en los años 50. ¿Cuál es? → «Campanera»
- folk-music-and-dance-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es un adorno grande y curvo que se clava en el moño y sostiene la mantilla en Semana Santa o en las bodas. ¿Cómo se llama? → Peineta
- money-and-services-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Si domicilias el recibo de la luz, ¿desde dónde se paga cada mes? → Desde tu cuenta del banco
- radio-and-internet-3: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: «La Pija y la Quinqui» y «Estirando el chicle» son dos de los éxitos de Spotify y YouTube en España. ¿Qué formato son? → Videopódcast
- regional-symbols-12: overlap like q-11225: Según la tradición, las cadenas doradas del escudo de Navarra se ganaron en una batalla de 1212. ¿Cuál? → Las Navas de Tolosa: En el escudo de España aparecen unas cadenas doradas sobre fondo rojo. ¿Qué antiguo reino representan? → El Reino de Navarra
- school-and-home-16: overlap like q-11218: Completa: el 6 de enero, los niños de España abren los regalos que les han traído los Reyes… → Magos: Me escribes con tu mejor letra antes del 6 de enero, dices que te has portado bien y pides juguetes. ¿Qué soy? → La carta a los Reyes Magos
- slang-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: «Profe» es a «profesor» como «tele» es a… → Televisión
- spanish-cinema-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Torrente, el policía más cutre del cine, protagoniza la saga más taquillera del cine español. ¿Adónde viaja de misión en su segunda película? → Marbella
- sportspeople-10: overlap like team-and-traditional-sports-5: Crecí en Sant Boi de Llobregat, fui novato del año de la NBA en 2002 y gané dos anillos con los Lakers junto a Kobe Bryant. ¿Quién soy? → Pau Gasol: Fue el primer español campeón de la NBA y ganó dos anillos junto a Kobe Bryant. ¿En qué equipo jugaba Pau Gasol? → Los Angeles Lakers
- team-and-traditional-sports-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Cuántos Tours de Francia seguidos ganó el ciclista navarro Miguel Induráin? → 5
- transport-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Desde 1999, Pontevedra es famosa en medio mundo por lo que hizo con casi todo su centro. ¿Qué hizo? → Lo hizo peatonal
- sayings-4: overlap like q-0116: ¿Quién escribió 'Don Quijote de la Mancha'? → Miguel de Cervantes: En clase de Lengua lees: «En un lugar de la Mancha, de cuyo nombre no quiero acordarme…». ¿Quién escribió esa frase? → Miguel de Cervantes
- sayings-7: overlap like q-0033: ¿Cuántos corazones tiene un pulpo? → 3: El animal que está «más perdido que un ___ en un garaje» tiene un número sorprendente de corazones. ¿Cuántos tiene? → 3
- slang-2: overlap like q-7844: En Colombia a un amigo le puedes decir «socio». ¿Cuál de estas palabras NO se usa en Colombia para lo mismo? → Cuate: Estás en el patio de un colegio de España y llamas a tu amigo. ¿Qué palabra NO se suele usar aquí para eso? → Cuate
- slang-4: overlap like q-11360: «ESO» es a «instituto» como «Primaria» es a… → Colegio: Vas allí después de primaria, a partir de los 12 años, y es donde se estudia la ESO. ¿Cómo lo llaman los chavales? → El insti
- slang-6: overlap like q-7745: Va en la cartuchera y casi todos los estudiantes tienen uno. En Colombia, ¿qué es un esfero? → Un bolígrafo: En España, ¿qué es un «boli»? → Un bolígrafo
- slang-7: overlap like q-7670: En Colombia, si algo te gusta mucho dices que está «bacano». ¿Cuál de estas expresiones NO se usa allá con ese sentido? → Guay: Ya lo decían tus padres de jóvenes, hoy lo dicen los niños en el patio y significa que algo te encanta. ¿Qué exclamación es? → ¡Qué guay!
- spanish-cinema-1: hard fail: correct 3, unambiguous 5, no_giveaway 5, no_overlap 5: Fui Margarita en «Águila Roja», protagonicé «La novia» y en «Tres bodas de más» acudo a las bodas de mis tres ex. ¿Quién soy? → Inma Cuesta
- spanish-cinema-11: overlap like q-9878: Ves en las noticias que alguien ha ganado tres «Goyas». ¿Qué ha ganado? → Premios del cine español: Soy una cabeza de bronce y cada año me llevo a casa lo mejor del cine español. Tengo la cara de un pintor aragonés. ¿De quién es mi cara? → Francisco de Goya
- spanish-cinema-13: overlap like q-1122: En la saga de Shrek, Antonio Banderas y Salma Hayek ponen la voz a dos personajes que pelean con espadas y roban frijoles mágicos. ¿Qué animales son? → Gatos: ¿Qué actor malagueño puso voz al Gato con Botas en «Shrek 2» y en sus películas propias? → Antonio Banderas
- spanish-cinema-16: overlap like q-2066: «La sociedad de la nieve» cuenta la historia del equipo uruguayo de rugby Old Christians atrapado en los Andes. ¿Quién la dirigió? → J. A. Bayona: Estás viendo los Goya de 2024 y «La sociedad de la nieve» gana el premio a la mejor película. ¿Quién la dirigió? → J. A. Bayona
- sportspeople-0: overlap like q-10517: This MLB team is named after a blue bird, won the World Series in 1992 and 1993, and is the only team outside the US. Where does it play? → Toronto: Marc Gasol fue campeón de la NBA en 2019 con el único equipo actual de la liga que no es de Estados Unidos. ¿De qué ciudad es? → Toronto
- sportspeople-4: overlap like q-3688: In 2005, at age 24, I became the youngest Formula 1 champion up to then and ended Michael Schumacher's run of five titles. Who am I? → Fernando Alonso: ¿En qué deporte ha sido campeón del mundo Fernando Alonso? → Fórmula 1
- team-and-traditional-sports-5: overlap like sportspeople-10: Fue el primer español campeón de la NBA y ganó dos anillos junto a Kobe Bryant. ¿En qué equipo jugaba Pau Gasol? → Los Angeles Lakers: Crecí en Sant Boi de Llobregat, fui novato del año de la NBA en 2002 y gané dos anillos con los Lakers junto a Kobe Bryant. ¿Quién soy? → Pau Gasol
- team-and-traditional-sports-12: overlap like q-11196: Portero vasco del Dream Team que ganó la Copa de Europa de 1992 en Wembley y que jugó cuatro Mundiales con España. ¿Quién era? → Andoni Zubizarreta: Así se llamó al Barça de Johan Cruyff, que ganó cuatro Ligas seguidas y su primera Copa de Europa en Wembley en 1992. ¿Qué apodo es? → Dream Team
- team-and-traditional-sports-13: overlap like q-7098: Egan Bernal la conquistó en el Giro de Italia de 2021, y allá la llaman «maglia rosa». ¿Qué es? → La camiseta del líder de la carrera: El rojo es a la Vuelta a España como el rosa es al… → Giro de Italia
- tv-series-6: overlap like q-1673: ¿Cuál de estos NO es el nombre de un atracador de la banda de «La casa de papel»? → París: En «La casa de papel», los atracadores usan nombres de ciudades. ¿Cuál de estas NO es el nombre de ninguno? → París
- tv-shows-and-presenters-4: overlap like q-9883: En Nochevieja, la tele da las campanadas desde el reloj más famoso de España. ¿En qué plaza de Madrid está? → La Puerta del Sol: Suenan doce a medianoche del 31 de diciembre, la tele las da desde Madrid y con cada una te comes una uva. ¿Qué son? → Las campanadas
- tv-shows-and-presenters-6: overlap like q-11164: Me celebro cada invierno en la Costa Blanca, nací en 2022 y de mí salió Chanel con «SloMo» rumbo a Eurovisión. ¿Qué soy? → El Benidorm Fest: Empezó en 2022, se celebra en una ciudad de playa y su ganador representa a España en Eurovisión. ¿Cómo se llama? → Benidorm Fest
- tv-shows-and-presenters-9: overlap like q-9935: Pablo Motos presenta en Antena 3 un programa con experimentos y dos marionetas, Trancas y Barrancas. ¿Cómo se llama? → El Hormiguero: ¿Cuál de estos programas NO se ha emitido en Telecinco? → El hormiguero
