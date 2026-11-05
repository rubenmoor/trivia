# batch-30

Made by `qgen batch` on 2026-11-05 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): regions-and-provinces, cities-and-towns, rivers-and-mountains, coasts-and-islands, monuments, wildlife, plants-and-climate, protected-areas, ancient-hispania, al-andalus-and-reconquista, empire, bourbons-and-19th-century, 20th-century, transition-and-democracy, scientists-and-explorers, famous-figures, regional-dishes, tapas, sweets-and-desserts, ham-cheese-and-produce, drinks, fiestas, christmas-and-holidays, dress-crafts-and-games, creatures, legends-and-superstitions, flamenco-and-copla
- Merged: 312 (q-9837…q-10148)
- Approved: 290
- Needs work: 22
- Dropped by the pipeline: 63
- Reviewed by: claude-opus-5-5
- Claude calls: 652, about $82.24 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-28, batch-29; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-28 | batch-29 | batch-30 |
|---|---|---:|---:|---:|
| source locale |  | de (first de batch) | en | es-ES (first es-ES batch) |
| drafts |  | 406 | 413 | 375 |
| skipped slots |  | 80 | 91 | 111 |
| dropped |  | 39 | 63 | 63 |
| drop rate | ≤ 20.0 % | 9.6 % ✓ | 15.3 % ✓ | 16.8 % ✓ |
| dropped: hard fail correct |  | 0 | 2 | 1 |
| dropped: hard fail unambiguous |  | 0 | 1 | 0 |
| dropped: hard fail no_giveaway |  | 20 | 19 | 22 |
| dropped: overlap |  | 17 | 41 | 40 |
| dropped: duplicate |  | 0 | 1 | 0 |
| dropped: fact-check wrong |  | 2 | 0 | 0 |
| merged |  | 367 | 350 | 312 |
| approved |  | 343 | 331 | 290 |
| needs_work |  | 24 | 19 | 22 |
| needs_work rate | ≤ 20.0 % | 6.5 % ✓ | 5.4 % ✓ | 7.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.8 % ✓ | 2.3 % ✓ | 3.8 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.1 % ✓ | 0.9 % ✓ | 0.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.5 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.5 % ✓ | 0.3 % ✓ | 1.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.4 % ✓ | 2.6 % ✓ | 2.6 % ✓ |
| media: no pick in review 1 |  | 52 | 46 | 64 |
| media: recovered by research |  | 40 | 38 | 57 |
| media: no pick at record |  | 12 | 8 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 4.7 % ✓ | 10.4 % ✓ | 11.5 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 74.0 % ✓ | 76.2 % ✓ | 64.0 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 2.14 ✗ | 1.00 ✓ | 1.12 ✓ |
| approved 11–15 |  | 64 | 69 | 54 |
| top move | ≤ 25.0 % | 16.1 % ✓ | 18.0 % ✓ | 21.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 79.0 % | 81.4 % | 77.6 % |
| values stimulus |  | 6 | 5 | 5 |
| top clue | ≤ 60.0 % | 51.5 % ✓ | 47.4 % ✓ | 47.1 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.9 % ✓ | 23.4 % ✓ | 27.6 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 24.0 % ✓ | 16.0 % ✓ | 22.1 % ✓ |
| values lens |  | 11 | 11 | 11 |
| media share | 15.0 %–50.0 % | 21.0 % ✓ | 18.6 % ✓ | 22.4 % ✓ |
| mean fun | ≥ 3.40 | 3.55 ✓ | 3.70 ✓ | 3.54 ✓ |
| cost $ |  | $87.70 | $81.75 | $79.45 |
| $ per approved | ≤ $0.35 | $0.26 ✓ | $0.25 ✓ | $0.27 ✓ |
| calls |  | 663 | 643 | 592 |
| calls per approved |  | 1.93 | 1.94 | 2.04 |
| wall time h |  | 3.58 | 3.19 | 2.42 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 0 of 4 (0 %)
- Problems by kind: giveaway 9 (0 major), media 2 (0 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.80

Major findings on approved questions:

None.

## Needs work

- **q-9844** (20th-century) ¿Cuál de estos grupos NO participó en el «pistolerismo» que sacudió Barcelona entre 1917 y 1923? → Falange Española: Hint 2 gives the answer away. It says the groups that took part were workers' unions and employers' organisations, and three options are named that way: «Sindicatos Libres», «Federación Patronal» and the CNT (Confederación Nacional del Trabajo). So anyone can pick Falange from the names alone. Hint 2 should be replaced with a vaguer clue, such as the 1917–1923 period being the last years before Primo de Rivera's dictatorship, without describing what kind of groups took part.
- **q-9877** (bourbons-and-19th-century) Este presidente de la Primera República dimitió en 1873 para no firmar unas penas de muerte. ¿Quién es? → Nicolás Salmerón: The text and facts are fine, but no candidate works as the essential portrait without showing his name. #1 has a caption under it that names Salmerón, #5 is a newspaper page that names him, #2–4 are buildings with his name on them, and #6 (the Madrazo portrait) has his name painted at the top of the canvas. I can't search again, so the image needs a portrait without the name, or a cropped #6. The rater also suggests switching the role to illustrative. No se encontró una imagen adecuada para esta pregunta.
- **q-9883** (christmas-and-holidays) Es Nochevieja y empiezan las campanadas. Si sigues la tradición, ¿cuántas uvas te comes? → 12: This asks the same fact as approved q-0320 («En Año Nuevo, ¿cuántas uvas se comen a las doce de la noche?» → 12): the number of New Year's Eve grapes. Drop it or swap it for a different Nochevieja fact.
- **q-9900** (coasts-and-islands) Por el Tratado de Utrecht, España cedió Gibraltar a Gran Bretaña. ¿En qué año se firmó? → 1713: This asks the same fact as the approved q-8030: the year the Treaty of Utrecht was signed (1713). That question only reaches it through the asiento de negros instead of Gibraltar. Seeing one question gives away the other. If the bundles are never played together, this could be approved instead.
- **q-9908** (creatures) Según la leyenda de Redondela, en Galicia, ¿de dónde salía la Coca, la dragona que se llevaba a las doncellas? → Del mar: Hint 2 («Los marineros la temían») gives the answer away: sailors point straight to the sea and rule out the mountain lagoon and the forest cave, leaving only the Miño as a weak rival. Hint 2 should say something vaguer that doesn't involve water, such as the Coca's link to the Corpus festival or how the townspeople felt about her.
- **q-9910** (creatures) Medio Pollito, con una pata y un ala, fue a ver al rey y acabó subido para siempre en lo alto de un campanario. ¿En qué se convirtió? → En una veleta: Hint 1 («Fue el viento quien lo subió allí») gives the answer away: with these four options, mentioning the wind points straight to the weathervane, so hints 2 and 3 add nothing. Hint 1 should be vague, e.g. about how Medio Pollito treated the creatures he met on the way, and only hint 3 should bring in the wind.
- **q-9917** (drinks) En España se puso de moda servirlo en copa de balón con mucho hielo; lleva tónica y un licor aromatizado con enebro. ¿Qué licor es? → Ginebra: None of the media candidates fits. They are an 1875 hotel engraving, two railway truss photos, two 18th-century balloon apparatus plates and a glass ball in a cobbler's workshop. No new search is allowed, so the slot needs another search by hand, for example "gin tonic copa" or "copa balón hielo". No se encontró una imagen adecuada para esta pregunta.
- **q-9941** (fiestas) Vas vestido de blanco y, cuando suena el chupinazo a mediodía del 6 de julio, te atas al cuello un pañuelo rojo. ¿Dónde estás? → En Pamplona: Hint 1 («Es una ciudad del norte de España») gives the answer away: Valencia, Sevilla and Buñol are all in the east or south, so it rules out all three wrong options at once. A vaguer first hint would work, for example one about the summer date. None of the media candidates fits either. They show a Native American camp, a WWII factory worker, Hajduk Split graffiti, a Thai band, a US-flag bandana and a hunter, and no new search is allowed. The slot needs a picture of a red neckerchief on white festival clothes, or a Pamplona street scene that shows no city name. No se encontró una imagen adecuada para esta pregunta.
- **q-9948** (fiestas) ¿Cuál de estos vehículos NO es tirado por caballos? → El patinete: The question «¿Cuál de estos vehículos NO es tirado por caballos?» only works inside the four options: countless real vehicles aren't horse-drawn, so the clue doesn't point to the answer in the real world, and the patinete stands out at once as the only modern option. The question needs a different clue that only the answer fits, or a replacement question. Also, every candidate image shows a Seville horse carriage, which is a wrong option (calesa/carruaje), so none fits the illustrative rules. No se encontró una imagen adecuada para esta pregunta.
- **q-9957** (ham-cheese-and-produce) Soy pequeña y plateada y viajo muy apretada con mis hermanas en una lata plana. Cuando el metro va lleno, se dice que la gente va como yo. ¿Qué soy? → La sardina: The description opens with «Un pez», which rules out the wrong answer «El mejillón» (a mussel, not a fish) before any hint. It also points at swimming in groups, which is close to the "packed together" clue. Rewrite the description so it plays on the topic (the sea, cans, crowds) without saying it is a fish.
- **q-9993** (regional-dishes) Mira esta imagen de cerca. ¿Cómo se llama este recipiente? → Paellera: No candidate shows a paella pan: five are freight trains (the query 'empty steel' matched railway photos) and #5 is a small one-handled stainless frying pan, which would point to the wrong object. The essential image needs a fresh search such as 'paella pan' or 'paellera'. Also, the description ('dos asas, cero tapas, mucha fama los domingos') rules out the olla, which has a lid, and points at Sunday paella. It should be reworded to play on the theme without the pan's traits. No se encontró una imagen adecuada para esta pregunta.
- **q-10002** (regions-and-provinces) ¿De qué comunidad autónoma es esta bandera? → Comunidad de Madrid: None of the six candidates shows the flag of the Community of Madrid (crimson with seven white stars). All are municipal flags or coats of arms (Coslada, Los Molinos, Tielmes, Cenicientos, Serranillos del Valle, Rascafría), so the essential image can't be filled, and no new search is allowed. Use a new search, e.g. "Flag of the Community of Madrid", or upload the Commons file "Flag of the Community of Madrid.svg" directly. No se encontró una imagen adecuada para esta pregunta.
- **q-10024** (tapas) Un mesón tiene jamones colgados, vigas de madera y cocina casera. ¿De dónde viene su nombre? → Del latín «mansio», la parada para pasar la noche: Hint 1 («Piensa más en dormir que en comer») gives the answer away: only the mansio option is about sleeping, so the first hint rules out all three wrong answers. Hint 1 should be vague, for example about the word coming from Roman times, without pointing to lodging. The etymology (RAE: from Latin mansio, -ōnis) checks out, and so do the description and the media.
- **q-10038** (cities-and-towns) Lleva anillas de calamar rebozadas en una barra de pan, se pide en los bares junto a su Plaza Mayor y su ciudad está lejos del mar. ¿Qué ciudad es? → Madrid: Hint 2 («es la más poblada del país») gives the answer away: in Spain everyone knows that is Madrid, so it is as strong as hint 3 («Es la capital de España»). Hint 2 should be a middle-strength clue instead, e.g. something about the city's bars or a famous square, without naming the city or its population rank.
- **q-10066** (fiestas) Mira la foto. ¿En qué país se inventó esto? → China: This overlaps the approved q-8750 ("Gunpowder… Where was it first invented?" → China). Fireworks are gunpowder, and the photo's «esto» could mean either one, so it asks the same fact again and either question gives away the other. Drop it, or swap it for a different Fallas or fireworks fact that isn't where they were invented.
- **q-10074** (legends-and-superstitions) «Nos recogen el día de la noche más corta del año, dormimos en agua al sereno y por la mañana te lavas la cara con nosotras». ¿Qué somos? → Las hierbas de San Juan: None of the six candidates shows anything to do with herbs soaking in water. They are LA aqueduct reservoirs, a Versailles garden print, a river barge drawing, olive pickers and an 1807 bathroom drawing, and no new search is allowed. The slot needs a new search such as "herbas de San Xoán" or "bunch of herbs in water bowl". No se encontró una imagen adecuada para esta pregunta.
- **q-10079** (protected-areas) La Alhambra, la catedral de Burgos y el parque nacional del Teide comparten este título internacional. ¿Cuál es? → Patrimonio de la Humanidad: This is a new draft that asks what three given places have in common («La Alhambra, la catedral de Burgos y el parque nacional del Teide comparten este título… ¿Cuál es?»). That is the "what do they have in common" style, which is not allowed for new drafts (developer rule, 2026-10-21).
- **q-10087** (regional-dishes) Completa el nombre de esta tapa de anillas de calamar rebozadas y fritas: calamares a la… → Romana: Hint 2 ("un pueblo antiguo que gobernó Hispania y construyó acueductos") points straight to the Romans, so it gives the answer away before hint 3. It also states as fact that the name comes from the Romans, but where "a la romana" comes from is disputed. Hint 2 should be a vaguer clue (for example about the batter or the lemon), and the claim about the name's origin should be dropped. Hint 3 ("Allí está el Coliseo") would then need its own place reference rather than "allí".
- **q-10103** (rivers-and-mountains) Hacia 2002 quedaban menos de 100 en libertad, vive en Doñana y Sierra Morena y come sobre todo conejos. ¿Qué felino llegó a ser el más amenazado del mundo? → El lince ibérico: Hint 1 («Solo vive en la península ibérica») gives the answer away: only one option is named after that peninsula, so the hint does the work meant for hint 3. The description also nearly settles it before any hint. «Gato de campo» with a rabbit diet rules out the Sumatran tiger and the snow leopard, and «remontada de película» names the comeback from near-extinction that the question asks about. Hint 1 should be vague, for example about the lynx's habitat of scrub and woodland. The description should play on the theme without the diet or the recovery.
- **q-10119** (sweets-and-desserts) Tengo color amarillo, me comes con cuchara y a menudo llevo una galleta flotando encima con canela. ¿Qué postre soy? → Natillas: None of the media candidates fits: they show euphorbia plants, a snowy spruce branch, ice hockey players and a drum kit, none of them cinnamon or a dessert. A new search isn't allowed. The slot needs a new search such as "cinnamon sticks" or "custard dessert bowl". No se encontró una imagen adecuada para esta pregunta.
- **q-10126** (tapas) Estas tiras de calamar rebozadas se llaman «rabas», y son el aperitivo estrella de una comunidad. ¿Cuál? → Cantabria: The fun fact's etymology can't be confirmed and is likely wrong: the RAE dictionary traces «raba» to French «rabes» (cod-roe bait), not to «rabo». The rater flagged it too. Replace the fun fact with a safe one, for example that rabas are usually served with lemon in Santander's bars, or that they are cut in strips instead of the rings of calamares a la romana.
- **q-10134** (transition-and-democracy) La expresión «café para todos» nació en la Transición, se atribuye al ministro Manuel Clavero Arévalo y aún sale en los debates. ¿Qué se daba a todos? → Autonomía a todas las regiones: Hint 2 gives the answer away: it says the phrase comes back whenever Catalonia or the Basque Country ask for «más autogobierno», which is just a synonym for autonomy, so the hint answers the question before hint 3. Hint 2 should keep the Suárez link but drop the self-government clue, for example by pointing to the Ministry for the Regions or to the Transition's political deals more vaguely.

## Question axes

- move: analogy 3, cause_effect 26, count 7, estimate 10, identify 66, made_of 21, name_concept 35, odd_one_out 13, origin 33, purpose 21, record 8, sequence 15, when 14, who 18, word_meaning 22
- stimulus: detail 13, map_outline 6, none 242, photo 49, sound 2
- clue: completion 9, direct 147, riddle 26, scenario 29, three_facts 101
- answer_kind: group 29, number 21, person 36, place 53, thing 86, time 15, word 72
- lens: body_senses 2, educational_media 44, everyday 69, history 43, language 43, nature 27, pop_culture 28, popular_science 1, school 41, science_news 5, university 9

## Dropped by the pipeline

- 20th-century-17: overlap like q-3150: Before the euro, the franc was to France what which currency was to Spain? → Peseta: Nació en 1868, su nombre viene de «pieza pequeña» y hacían falta 166,386 de ellas para tener un euro. ¿Qué era? → La peseta
- al-andalus-and-reconquista-0: overlap like q-0333: Muchas palabras del español que empiezan por 'al-', como 'almohada', 'alfombra' y 'algodón', vienen de un mismo idioma. ¿De cuál? → Árabe: Estás rallando zanahorias para la ensalada. ¿De qué lengua llegó al castellano la palabra «zanahoria»? → Del árabe andalusí
- ancient-hispania-0: overlap like q-1928: Soy de Cartago y, por mi culpa, los romanos vieron elefantes bajando por los Alpes. ¿Quién soy? → Aníbal: ¿Qué general asedió Sagunto en el año 219 a. C. y así desató la Segunda Guerra Púnica? → Aníbal
- ancient-hispania-4: overlap like q-2617: Who uses a small brush like this to free old objects from the ground? → Archaeologist: En Atapuerca se hacen trabajos como este, con pinceles y cuadrículas. ¿Quiénes los hacen? → Los arqueólogos
- ancient-hispania-7: overlap like q-3787: I'm a long piece of white wool, wrapped around the body and over the left shoulder. Who wore me with pride? → A Roman citizen: Muchas estatuas del Museo Romano de Mérida llevan esta prenda. ¿Cómo se llama? → Toga
- ancient-hispania-9: overlap like q-1738: Este cráneo de unos 430 000 años salió de la Sima de los Huesos, en España. ¿A qué linaje humano pertenecía? → Al de los neandertales: En la Sima de los Huesos de Atapuerca apareció «Excalibur», un hacha de piedra de cuarcita roja. ¿Qué antigüedad tiene, más o menos? → Unos 430 000 años
- ancient-hispania-14: overlap like q-1566: Estás frente a la famosa estatua de Augusto de Prima Porta. ¿En la villa de qué mujer la encontraron? → Livia: Esta estatua es del emperador que terminó la conquista de Hispania venciendo a cántabros y astures. ¿Quién es? → Augusto
- christmas-and-holidays-1: overlap like q-5151: Mira de cerca: con este material los artesanos de Ráquira, Boyacá, hacen ollas y figuras. ¿Qué es? → Barro: Las figuritas de pastores como estas se hacen tradicionalmente con un material que se moldea a mano y se cuece en el horno. ¿Cuál? → Barro
- christmas-and-holidays-2: overlap like q-7954: En diciembre se arma con musgo y figuritas, y a la medianoche del 24 se pone al Niño Dios. ¿Qué dos animales lo acompañan en el pesebre? → La mula y el buey: Montas el belén y llegas al pesebre. ¿Cuántos animales pone la tradición junto al Niño para darle calor? → 2
- cities-and-towns-4: overlap like q-9875: El edificio de la Puerta del Sol cuyo reloj da las campanadas de Nochevieja se construyó con Carlos III. ¿Para qué? → Para ser la casa de correos: Con las campanadas de este reloj se comen las uvas en toda España cada Nochevieja. ¿En qué plaza de Madrid está? → Puerta del Sol
- cities-and-towns-5: overlap like q-1987: Es una avenida de Madrid, se empezó a construir en 1910 y la llaman 'el Broadway madrileño' por sus teatros. ¿Cuál es? → La Gran Vía: Mira esta calle de Madrid, llena de cines, teatros y tiendas. ¿Cómo se llama? → Gran Vía
- cities-and-towns-16: overlap like q-2238: Who designed this colorful park in Barcelona? → Antoni Gaudí: ¿En qué lugar de Barcelona está este famoso dragón de mosaico? → Park Güell
- coasts-and-islands-17: overlap like q-9735: Horatio Nelson stands on top of Nelson's Column. He was an admiral: what did he command? → Warships: Esta columna de Londres recuerda la victoria en la batalla de Trafalgar, frente a Cádiz, en 1805. ¿Qué almirante está en lo alto? → Horatio Nelson
- creatures-2: overlap like q-6337: In a famous Spanish novel, a knight charges at tall machines with huge spinning arms, sure they are giants. What are they? → Windmills: Tienen grandes aspas, están en lo alto de los cerros y un caballero los atacó creyendo que eran gigantes. ¿De qué región española son esos molinos? → La Mancha
- creatures-13: overlap like q-7463: A muchos bebés colombianos les ponen una pulserita con un azabache contra el mal de ojo. ¿Qué es el azabache? → Una piedra negra: A un bebé le ponen una pulserita con una piedrecita negra de azabache. Según la tradición, ¿para qué sirve? → Para protegerlo del mal de ojo
- dress-crafts-and-games-10: overlap like al-andalus-and-reconquista-0: Estás rallando zanahorias para la ensalada. ¿De qué lengua llegó al castellano la palabra «zanahoria»? → Del árabe andalusí: Esta prenda se llama también mandil. ¿De qué lengua llegó la palabra «mandil» al español? → Del árabe
- dress-crafts-and-games-16: overlap like q-7147: Un bando persigue y el otro huye; a los atrapados los llevan a la 'cárcel' y un compañero libre los salva tocándolos. ¿Cómo se llama el juego? → Policías y ladrones: En polis y cacos, un equipo persigue y el otro huye, y los pillados van a la cárcel. ¿Qué son los cacos? → Los ladrones
- empire-11: overlap like q-0099: ¿Quién llegó a América en 1492 con tres barcos? → Cristóbal Colón: Los Reyes Católicos me ayudaron, mis barcos eran la Pinta, la Niña y la Santa María, y creí haber llegado a las Indias. ¿Quién soy? → Cristóbal Colón
- empire-14: overlap like q-0354: Mira este cuadro famoso, 'Las Meninas', que está en el Museo del Prado de Madrid: ¿quién lo pintó? → Diego Velázquez: En este detalle de uno de los cuadros más famosos del Museo del Prado, el pintor se retrató a sí mismo con el pincel. ¿Quién es? → Diego Velázquez
- fiestas-5: overlap like empire-4: La patata llegó a Europa en barcos españoles en el siglo XVI. ¿De dónde procede? → De Sudamérica: En los mercados medievales de hoy se venden muchos alimentos, pero uno no existía en la Europa de la Edad Media porque llegó de América. ¿Cuál? → La patata
- fiestas-12: overlap like dress-crafts-and-games-5: Camisa del color de su grupo, pantalón blanco y faja negra. ¿Cómo se llama a quienes visten así en la foto? → Castellers: Los castellers se enrollan en la cintura una larga tela, casi siempre negra, que les sujeta la espalda y sirve de agarre para trepar. ¿Cómo se llama? → Faixa
- fiestas-16: overlap like q-9943: La Feria de Abril de Sevilla nació en 1847, con casetas pero sin tanto baile. ¿Para qué se creó? → Para comprar y vender ganado: Estás en la Feria de Abril y entras en una carpa de lona a rayas donde un grupo de amigos baila sevillanas y comparte tapas. ¿Cómo se llama? → Caseta
- flamenco-and-copla-11: overlap like q-7200: Escucha: con este instrumento, y no con acordeón, Guillermo Buitrago grabó canciones costeñas en los años 40. ¿Cuál es? → La guitarra: Escucha: este instrumento acompaña desde hace siglos al cante y al baile flamenco. ¿Cuál es? → La guitarra
- ham-cheese-and-produce-15: overlap like q-5045: Soy una hojita verde que huele fresquito, como los chicles de menta. En Colombia me hacen aromática para el dolor de barriga. ¿Qué soy? → La yerbabuena: Una ramita adorna el caldo del puchero andaluz, también se usa en el té moruno y en el mojito. ¿Qué hierba es? → Hierbabuena
- legends-and-superstitions-1: overlap like q-1600: Según la tradición, ¿por qué se cuelga este objeto con las puntas hacia arriba? → Para que la suerte no se derrame: Se clava sobre la puerta para atraer la suerte, la llevan los caballos en los cascos y da nombre a un arco de la Mezquita de Córdoba. ¿Qué es? → La herradura
- legends-and-superstitions-2: overlap like q-0534: Pasar debajo de una escalera, que se te cruce un gato negro y abrir un paraguas dentro de la casa: ¿qué tienen en común? → Según las supersticiones, traen mala suerte: Según una superstición muy conocida, ¿qué te trae pasar por debajo de una escalera de mano apoyada en la pared? → Mala suerte
- monuments-16: overlap like q-1861: Se hace con pedazos de baldosa o cerámica rota, se pega como mosaico y Gaudí lo usó mucho. ¿Cómo se llama esta técnica? → Trencadís: Mira este dragón de Gaudí en el Parque Güell de Barcelona. ¿Con qué está cubierto? → Con trozos de cerámica rota
- plants-and-climate-4: overlap like q-7999: En Boyacá y la sabana de Bogotá, los campesinos les tienen miedo a las «heladas». ¿Qué es una helada? → Un frío de madrugada que congela los cultivos: Llego en las noches despejadas de invierno, cuando el termómetro baja de cero, congelo los charcos y estropeo los cultivos. ¿Qué soy? → La helada
- regions-and-provinces-5: overlap like q-9962: Según la tradición, la Virgen se apareció sobre un pilar en Zaragoza para animar a un apóstol que predicaba en Hispania. ¿A cuál? → Santiago: Se alza a orillas del Ebro, Goya pintó una de sus cúpulas y su gran fiesta es el 12 de octubre. ¿Qué templo es? → La basílica del Pilar
- regions-and-provinces-12: overlap like q-9894: Soy un mar del norte de España, frío y con mucho oleaje. Baño Gijón, Santander y Bilbao. ¿Quién soy? → El mar Cantábrico: Llevo el nombre de un pueblo antiguo que plantó cara a Roma, y baño las playas de Santander, Gijón y San Sebastián. ¿Quién soy? → El mar Cantábrico
- regions-and-provinces-16: overlap like q-9890: Mira este acueducto de Segovia. ¿Qué pueblo lo construyó? → Los romanos: Esta torre de A Coruña es uno de los faros más antiguos del mundo que aún funcionan. ¿Quiénes la construyeron? → Los romanos
- 20th-century-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: «Naranjito» llevaba la camiseta de la selección española y era famosísimo en el verano de 1982. ¿Qué era? → La mascota del Mundial de fútbol
- al-andalus-and-reconquista-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El algodón llegó a la península en la Edad Media y necesita mucho calor. ¿En qué comunidad se cultiva hoy casi todo el de España? → Andalucía
- al-andalus-and-reconquista-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Lo trajeron los andalusíes, su nombre viene del árabe y hoy se cultiva en el delta del Ebro. ¿Qué es? → El arroz
- al-andalus-and-reconquista-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Soy blanca y en granitos, y los andalusíes me sacaban de la caña en la costa de Granada. ¿Qué soy? → Azúcar
- ancient-hispania-5: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: «Fuego», «hogar» y «foco» vienen del latín «focus». ¿Qué significaba esa palabra para los romanos? → El fogón de la casa
- tapas-5: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Una bodega guarda vino en barricas, y su nombre viene del griego «apothéke», que también dio «botica». ¿Qué significaba? → Almacén
- tapas-11: overlap like q-9940: En una churrería, ¿cuál de estas cosas NO se suele mojar en el chocolate a la taza? → Una croqueta: Tiene una gran sartén de aceite, sirve chocolate caliente y los domingos por la mañana se forma cola. ¿Qué se vende sobre todo allí? → Churros y porras
- tapas-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En un bar pides «un bocata de chorizo». ¿Qué te traen? → Un bocadillo de chorizo
- wildlife-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Fíjate en el dibujo del lomo de esta culebra joven: le da nombre a su especie. ¿Qué culebra es? → La culebra de escalera
- bourbons-and-19th-century-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Qué tiene de especial la Marcha Real, el himno nacional de España? → No tiene letra oficial
- christmas-and-holidays-8: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Sale el Domingo de Ramos, muestra la entrada de Jesús en Jerusalén y la acompañan niños con palmas. ¿Cómo se llama popularmente este paso? → La Borriquita
- christmas-and-holidays-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: En Navidad, carteros, barrenderos y serenos llamaban a las casas a pedirlo, a menudo con una tarjeta de felicitación. ¿Qué era el aguinaldo? → Un regalo de dinero navideño
- christmas-and-holidays-10: overlap like q-0497: ¿Qué día se celebra en Colombia el Día de los Inocentes, cuando la gente se hace bromas? → 28 de diciembre: El 28 de diciembre, cuando alguien cae en una broma, ¿qué le gritan en España? → ¡Inocente, inocente!
- dress-crafts-and-games-5: overlap like fiestas-12: Los castellers se enrollan en la cintura una larga tela, casi siempre negra, que les sujeta la espalda y sirve de agarre para trepar. ¿Cómo se llama? → Faixa: Camisa del color de su grupo, pantalón blanco y faja negra. ¿Cómo se llama a quienes visten así en la foto? → Castellers
- famous-figures-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La marca de zapatos Camper nació en Mallorca. ¿Qué significa su nombre en mallorquín? → Campesino
- fiestas-14: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: En el Carnaval de Santa Cruz de Tenerife, los trajes de las candidatas a reina pueden pesar más de 100 kilos. ¿Qué llevan escondido para moverlos? → Ruedas
- ham-cheese-and-produce-3: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Cuando algo no te interesa nada, dices que te importa un comino. ¿Por qué se usa el comino en esta expresión? → Porque su semilla es diminuta
- monuments-1: overlap like rivers-and-mountains-9: Está en una montaña de rocas puntiagudas cerca de Barcelona, es de madera oscura y la gente hace cola para tocar la esfera que sostiene. ¿Qué es La Moreneta? → Una imagen de la Virgen: ¿Cómo llaman con cariño a la Virgen de Montserrat, patrona de Cataluña? → La Moreneta
- plants-and-climate-5: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Soy un paraje de roca caliza en Castilla-La Mancha. El agua y el viento me tallaron piedras con forma de seta, barco o tobogán. ¿Qué soy? → La Ciudad Encantada
- plants-and-climate-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El tomillo es una mata del monte de hojitas diminutas y flores rosadas. ¿Qué notas si frotas una ramita entre los dedos? → Un olor fuerte y agradable
- protected-areas-8: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 4: ¿Cómo se llama la lista oficial española en la que el lince ibérico figura «en peligro de extinción»? → El Catálogo Español de Especies Amenazadas
- protected-areas-10: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: España tiene reservas marinas como la de Cabo de Palos, en Murcia. ¿Para qué sirven sobre todo? → Para que los peces se recuperen
- regional-dishes-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El jamón serrano debe su nombre al lugar donde se curaba tradicionalmente. ¿Dónde? → En la sierra
- regional-dishes-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El socarrat es crujiente, se rasca con la cuchara y muchos valencianos lo consideran lo mejor del plato. ¿De qué está hecho? → De arroz tostado
- rivers-and-mountains-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Soy una enorme roca volcánica que se alza de pie en las cumbres de Gran Canaria y soy el símbolo más famoso de la isla. ¿Quién soy? → El Roque Nublo
- scientists-and-explorers-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: «Nací en Moguer, escribí un libro sobre un burro y en Puerto Rico supe que había ganado el Nobel de 1956.» ¿Quién soy? → Juan Ramón Jiménez
- scientists-and-explorers-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es de vidrio, tiene un pitorro largo y fino y es típico de Cataluña y Aragón. ¿Para qué se usa el porrón? → Para beber vino a chorro sin tocarlo con la boca
- rivers-and-mountains-5: overlap like q-1331: Está pintado sobre roca, tiene miles de años y lo hay en Chiribiquete y en Altamira. ¿Cómo se llama este arte? → Arte rupestre: Los bisontes de la cueva de Altamira, en Cantabria, se pintaron sobre la roca hace más de 14 000 años. ¿Cómo se llama este arte prehistórico? → El arte rupestre
- rivers-and-mountains-9: overlap like monuments-1: ¿Cómo llaman con cariño a la Virgen de Montserrat, patrona de Cataluña? → La Moreneta: Está en una montaña de rocas puntiagudas cerca de Barcelona, es de madera oscura y la gente hace cola para tocar la esfera que sostiene. ¿Qué es La Moreneta? → Una imagen de la Virgen
- rivers-and-mountains-13: overlap like q-0563: ¿Cómo se llama la desembocadura de un río que se abre en muchos brazos formando un triángulo, como la del Nilo? → Delta: Estás donde el Ebro llega al mar: una enorme llanura con forma de punta, hecha con la tierra que arrastra el río. ¿Cómo se llama? → Un delta
- scientists-and-explorers-8: overlap like q-2021: Estás viendo los dibujos de neuronas más famosos de la historia, hechos a mano por un Nobel de Medicina. ¿Quién los hizo? → Santiago Ramón y Cajal: Al aprender, se refuerzan tus sinapsis, las uniones entre neuronas. ¿Qué científico español demostró que las neuronas están separadas? → Santiago Ramón y Cajal
- wildlife-9: overlap like q-9957: Soy pequeña y plateada y viajo muy apretada con mis hermanas en una lata plana. Cuando el metro va lleno, dicen que vais como yo. ¿Qué soy? → La sardina: Soy pequeña y plateada; en las playas de Málaga me asan ensartada en una caña junto al fuego, y al acabar el carnaval me entierran. ¿Quién soy? → La sardina
