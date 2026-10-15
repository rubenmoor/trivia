# batch-8

Made by `qgen batch` on 2026-10-15 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Subcategories (92): Quesos, Dulces y chocolate, Fauna africana, Química, Física, Científicos famosos, Premios Nobel, Imperio romano, Revolución francesa, Exploradores y descubrimientos, Segunda Guerra Mundial, Guerra Fría, Presidentes de Estados Unidos, Monarquía británica, Crímenes famosos, Escándalos famosos, Rock, Música pop, Hip hop y rap, Eurovisión, Musicales, Canciones infantiles, Premios Óscar, Ciencia ficción, Fantasía, Cine de terror, Reality shows, Telenovelas, James Bond, Harry Potter, El Señor de los Anillos, Fórmula 1 y automovilismo, Rugby, Críquet, Shakespeare, Poesía, Novela policiaca, Fotografía, Frases célebres, Refranes y dichos, Circo, Dúos famosos, Historia de la moda, Diseñadores de moda, Trajes típicos del mundo, Zapatos y accesorios, Diseño de objetos, Maravillas del mundo, Monumentos famosos, Rascacielos, Puentes famosos, Templos y catedrales, Estilos arquitectónicos, Monedas del mundo, Billetes del mundo, Historia del dinero, Ahorro y bancos, Religiones del mundo, Historias de la Biblia, Lugares sagrados, Filósofos famosos, Preguntas filosóficas, Logotipos famosos, Eslóganes publicitarios, Mascotas de marcas, Origen de las marcas, Empresas famosas, Productos del supermercado, Leyendas y supersticiones, Juegos Olímpicos de invierno, Bebidas, Terremotos, Reptiles, Peces, Bichos raros, Perros, Mascotas raras, Números, Formas, Cosas raras del cuerpo humano, Inventos por accidente, Redes sociales, Carros, Aviones, Prehistoria, Dinosaurios, Faraones, Pirámides, Castillos, Dioses griegos, Mitología romana, Música del mundo
- Merged: 992 (q-1212…q-2203)
- Approved: 947
- Needs work: 45
- Dropped by the pipeline: 144
- Reviewed by: claude-opus-5-5
- Claude calls: 1921, about $218.00 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it, ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ stops the next `qgen batch` until `qgen health ack` (D-55). Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-6 | batch-7 | batch-8 |
|---|---|---:|---:|---:|
| drafts |  | 91 | 712 | 1136 |
| skipped slots |  | 29 | 313 | 519 |
| dropped |  | 9 | 96 | 144 |
| drop rate | ≤ 20.0 % | 9.9 % ✓ | 13.5 % ✓ | 12.7 % ✓ |
| dropped: hard fail correct |  | 0 | 3 | 1 |
| dropped: hard fail unambiguous |  | 0 | 2 | 6 |
| dropped: hard fail no_giveaway |  | 9 | 90 | 77 |
| dropped: overlap |  | 0 | 0 | 57 |
| dropped: duplicate |  | 0 | 1 | 2 |
| dropped: fact-check wrong |  | 0 | 2 | 2 |
| merged |  | 82 | 616 | 992 |
| approved |  | 66 | 504 | 947 |
| needs_work |  | 16 | 112 | 45 |
| needs_work rate | ≤ 20.0 % | 19.5 % ✓ | 18.2 % ✓ | 4.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 9.8 % ✓ | 8.9 % ✓ | 1.4 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.2 % ✓ | 2.9 % ✓ | 0.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.2 % ✗ | 2.9 % ✗ | 0.4 % ✓ |
| needs_work: media | ≤ 10.0 % | 7.3 % ✓ | 7.0 % ✓ | 2.1 % ✓ |
| media: no pick in review 1 |  | 6 | 69 | 101 |
| media: recovered by research |  | 0 | 26 | 92 |
| media: no pick at record |  | 6 | 43 | 9 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 2.4 % ✓ | 0.6 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 1.2 % ✓ | 0.5 % ✓ | 0.0 % ✓ |
| problems guessed |  | yes | yes | no |
| overlap rate | ≤ 3.0 % | 1.1 % ✓ | 2.7 % ✓ | 5.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 52.5 % ✗ | 60.0 % ✓ | 63.8 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 2.00 ✗ | 2.95 ✗ | 2.52 ✗ |
| approved 11–15 |  | 17 | 136 | 339 |
| top move | ≤ 25.0 % | 14.6 % ✓ | 13.0 % ✓ | 12.3 % ✓ |
| values move |  | 14 | 16 | 15 |
| top stimulus |  | 74.4 % | 86.2 % | 87.8 % |
| values stimulus |  | 7 | 6 | 6 |
| top clue | ≤ 50.0 % | 42.7 % ✓ | 45.3 % ✓ | 45.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 43.9 % ✗ | 28.4 % ✓ | 23.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.7 % ✓ | 18.5 % ✓ | 18.6 % ✓ |
| values lens |  | 12 | 12 | 12 |
| media share | 15.0 %–50.0 % | 25.6 % ✓ | 13.8 % ✗ | 12.2 % ✗ |
| mean fun | ≥ 3.40 | 3.56 ✓ | 3.67 ✓ | 3.60 ✓ |
| cost $ |  | $19.53 | $120.74 | $215.25 |
| $ per approved | ≤ $0.35 | $0.30 ✓ | $0.24 ✓ | $0.23 ✓ |
| calls |  | 174 | 964 | 1861 |
| calls per approved |  | 2.64 | 1.91 | 1.97 |
| wall time h |  | n/a | n/a | 4.81 |
| days |  | 2 | 3 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets (base, approved now): 1: 205, 2: 242, 3: 311, 4: 297, 5: 280, 6: 237, 7: 278, 8: 290, 9: 175, 10: 178, 11: 176, 12: 91, 13: 94, 14: 59, 15: 108

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 7 of 115 (6 %)
- Major among review needs work: 1 of 5 (20 %)
- Problems by kind: giveaway 13 (6 major), overlap 2 (2 major), media 2 (1 major), difficulty 8 (0 major), style 3 (1 major), other 4 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 9 of 120 (8 %)
- Audit/review agreement (both accept or both not): 109 of 120 (91 %)
- Sample: 120 audited of 120; 120 Claude calls, about $5.41

Major findings on approved questions:

- **q-1316**: overlap — Hint 1 ("Mi color viene del hierro que llevo dentro") gives away the answer to related q-1314, which asks which metal in haemoglobin makes blood red (answer: Hierro). If both questions are played, one spoils the other, so hint 1 should be reworded. Everything else checks out: the answer is right (blood is red, and venous blood is dark red, never blue), the hints and fun fact are true, the vein photo is a fair illustration that doesn't show the answer, and difficulty 2 fits. (http://127.0.0.1:8001/review/q-1316)
- **q-1378**: giveaway — Hint 1 ("Es un líquido.") rules out all three wrong answers (huevo, harina, azúcar), so the first hint gives the answer away. A vaguer hint 1 would fix it, for example "Viene de un animal", though that still leaves huevo in play. Everything else checks out: the answer and fun fact are correct (hard cheeses take about 10 L of milk per kg), the media shows an arepa with fish rather than milk, and difficulty 2 fits. (http://127.0.0.1:8001/review/q-1378)
- **q-1531**: giveaway — Hint 1 ("Esto pasa en 'Animales fantásticos', décadas antes de Harry") rules out all three wrong answers, since Voldemort, Bellatrix and Barty Crouch Jr. are all villains from Harry's time, so only Grindelwald is left. Hint 2 ("la segunda película") also points to a film titled 'Los crímenes de Grindelwald'. The facts check out: Queenie is Tina's sister and a legilimens, she joins Grindelwald in Paris in film 2 because of the US ban on marrying no-majs, and she marries Jacob at the end of 'Los secretos de Dumbledore'. Q-1908 about Tina is a different fact, and the decorative Paris image is fine. (http://127.0.0.1:8001/review/q-1531)
- **q-1774**: giveaway, style — Hint 2 ("Lo bebían lejos, muy lejos de la Tierra") gives the answer away: of the four options, only astronauts leave Earth, so it rules out all three wrong answers. It should be moved to hint 3 or made vaguer. Minor style issues: in a base question, "neveras" (hint 1) is regional ("refrigeradores" is closer to neutral), and "refresco" usually means a soda in many countries. The facts are correct: Tang was created by William A. Mitchell at General Foods in 1957, he also invented Pop Rocks, and Tang flew on Gemini missions. (http://127.0.0.1:8001/review/q-1774)
- **q-1868**: giveaway — Hint 2 ("joven de un pueblo nómada del desierto") is basically the definition of a Bedouin. It rules out all three wrong answers at once, and it gives more away than hint 3 (the goat), so the hints go from stronger to weaker. Swapping hints 2 and 3, or rewording hint 2, would fix it. The facts check out: Muhammed edh-Dhib was a Bedouin shepherd looking for a lost goat near Qumran in 1946/47 who threw a stone into a cave and heard a jar break. The Qumran caves image doesn't show the answer, and no related question overlaps. (http://127.0.0.1:8001/review/q-1868)
- **q-2033**: giveaway — The facts hold up: pernicious anemia comes from B12 deficiency, liver therapy began with Minot and Murphy in 1926, and Whipple, Minot and Murphy won the 1934 Nobel. The problem is the hints. Only one option is an anemia, so hint 1 ("Afecta la sangre") already points straight at it, and hint 2 ("faltan glóbulos rojos sanos") is the textbook definition of anemia; both rule out every wrong answer long before hint 3. (http://127.0.0.1:8001/review/q-2033)
- **q-2199**: media — The essential image is "Weisse boutonniere.jpg", which shows a flower worn in a buttonhole, not an ascot. The question says "una pañoleta como esta", so the image has to show an ascot tie. The facts check out: the ascot is named after Ascot Racecourse, and Royal Ascot's dress code does set rules for hats and headpieces, such as a minimum base size in the Royal Enclosure. The distractors are clearly wrong and none of the related questions asks the same fact. (http://127.0.0.1:8001/review/q-2199)

## Quality control

The developer's blind spot check (`/review?batch=…&sample=1`) against the LLM review and the audit (plan 16, `qgen report --qc`). Agree = both accept or both don't.

- Spot check: 120 decided of 120
- Agreement with the LLM review: 108 of 120 (90 %) ✓ (bar: ≥ 30 questions, ≥ 90 %)
- Release bar (D-79): ✓ release-ready
- False approve (LLM approved, human not): 9 of 120 (8 %); the audit flagged 1
- False needs work (LLM not approved, human approved): 3 of 120 (2 %)
- Difficulty |Δ| ≥ 2: 6 of 120 (5 %)
- Media changed: 1 of 120 (1 %)
- Audit/human agreement: 105 of 120 (88 %)

Disagreements with the LLM review, by the human's problems:

### media (1)

- **q-1897** LLM approved → human needs_work, audit ok: needs photo of earth from space (http://127.0.0.1:8001/review/q-1897)

### style (1)

- **q-1581** LLM approved → human needs_work, audit ok: the "three hints" style should be purged. this one has two hints (http://127.0.0.1:8001/review/q-1581)

### no problem given (10)

- **q-1691** LLM approved → human needs_work, audit ok: the question is fine per se, but "cinta scotch" is only used in Spain. This has to go into a regional bundle "Spain". it can't go into a base bundle (http://127.0.0.1:8001/review/q-1691)
- **q-1868** LLM approved → human needs_work, audit problem (http://127.0.0.1:8001/review/q-1868)
- **q-1733** LLM approved → human needs_work, audit ok (http://127.0.0.1:8001/review/q-1733)
- **q-1646** LLM approved → human needs_work, audit ok: i don't think the bills of every currency have that. and for regional it's not specific enough (http://127.0.0.1:8001/review/q-1646)
- **q-1950** LLM approved → human needs_work, audit ok: this might work ... not sure how this question translates to english. (http://127.0.0.1:8001/review/q-1950)
- **q-1246** LLM approved → human needs_work, audit ok: the original image didn't actually show a peso bill (http://127.0.0.1:8001/review/q-1246)
- **q-1973** LLM approved → human rejected, audit ok (http://127.0.0.1:8001/review/q-1973)
- **q-1854** LLM needs_work → human approved, audit ok (http://127.0.0.1:8001/review/q-1854)
- **q-1452** LLM needs_work → human approved, audit ok (http://127.0.0.1:8001/review/q-1452)
- **q-2043** LLM needs_work → human approved, audit ok (http://127.0.0.1:8001/review/q-2043)

Changes from this QC: 1182, 1183

## Needs work

- **q-1229** (Bebidas) Hierves flores secas de Jamaica en agua para hacer una bebida. ¿De qué color queda el agua? → Roja: La pista 2 ("un color cálido y profundo, más oscuro que el naranja") resuelve la pregunta: descarta verde y azul por no ser cálidos, y amarilla por ser más clara que el naranja. Además, la pista 1 ya apunta al color de la flor seca, así que las pistas 1 y 2 deberían ser mucho más vagas (por ejemplo, sobre el sabor ácido o sobre dónde se bebe).
- **q-1291** (Científicos famosos) Oppenheimer dirigió el laboratorio que probó la primera bomba atómica en el desierto de Nuevo México. ¿En qué año? → 1945: La pista 2 ("Fue el mismo año en que terminó esa guerra") delata la respuesta: el año en que terminó la Segunda Guerra Mundial (1945) es muy conocido y ya está en el pool (q-0105). Hay que cambiarla por una pista más vaga, por ejemplo una sobre el contexto del Proyecto Manhattan que no fije el año.
- **q-1301** (Cine de terror) Soy la letra del cine barato de monstruos y platillos voladores, y nací en el Hollywood de los años 30. ¿Qué significaba yo al principio? → La película secundaria de una función doble: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-no notice, PD-US-pre1978).
- **q-1313** (Cosas raras del cuerpo humano) Soy una burbujita en la piel que sale cuando un zapato nuevo te roza mucho. ¿De qué estoy llena? → De líquido: La pista 1 ("me muevo como un globo de agua") ya revela que la ampolla está llena de líquido; debería ser una pista vaga (por ejemplo, sobre dónde suele salir o por qué aparece) y no sobre su contenido.
- **q-1323** (Crímenes famosos) Desde el puerto de Marsella ves una islita con una fortaleza: el Castillo de If. ¿Para qué se usó durante siglos? → Como cárcel: La pista 2 ('Alejandro Dumas encerró ahí a Edmundo Dantès') delata la respuesta: 'encerró' equivale a decir que era una cárcel, aunque uno no conozca la novela. Además, la pista 3 dice 'Es la prisión de…', que es casi un sinónimo literal de 'cárcel'; habría que hacer la pista 2 más vaga (p. ej. que un escritor francés famoso ambientó ahí una novela de aventuras) y en la pista 3 evitar la palabra 'prisión'.
- **q-1331** (Dinosaurios) Está pintado sobre roca, tiene miles de años y lo hay en Chiribiquete y en Altamira. ¿Cómo se llama este arte? → Arte rupestre: La búsqueda de imagen ('Chiribiquete tepuis aerial') no devolvió candidatos y no se puede buscar de nuevo, así que no hay media. El texto está bien. Para la imagen ilustrativa, prueben con un paisaje de los tepuyes sin pinturas, por ejemplo 'Serranía de Chiribiquete' o 'Caquetá rainforest tepui'. Aparte: la subcategoría 'Dinosaurios' no corresponde al arte rupestre; convendría pasarla a Historia o Arte. No se encontró una imagen adecuada para esta pregunta.
- **q-1334** (Dinosaurios) Encuentras en una roca un fósil en forma de espiral: es una amonita. ¿Cuándo se extinguieron las amonitas? → Hace unos 66 millones de años: Repite el mismo dato que q-1035 (aprobada): cuándo se extinguieron las amonitas, con la misma respuesta «Hace unos 66 millones de años». Hay que descartarla o reemplazarla por otra pregunta. Además, la descripción llama a la amonita «caracol de mar», pero era un cefalópodo.
- **q-1352** (Diseñadores de moda) Coco Chanel es al vestido negro como Levi Strauss es a… → Jeans: Se solapa demasiado con q-1604 (también es sobre los jeans): la pista 2 (ropa de trabajo para mineros) y el dato curioso (remaches patentados en 1873) son justo las pistas de esa adivinanza, así que ver una pregunta resuelve la otra. Hay que quedarse solo con una de las dos.
- **q-1423** (Eurovisión) Sandie Shaw ganó Eurovisión 1967 cantando descalza «Puppet on a String». ¿Qué país del mapa representaba? → Reino Unido: Ningún candidato sirve como mapa esencial: el único mapa del Reino Unido (n.º 2) lleva los rótulos «UNITED KINGDOM», «ENGLAND» y «London», y los demás son otro mapa, otro país o fotos de Perth. Hace falta una nueva búsqueda, p. ej. «United Kingdom blank map», de una silueta sin nombres. No se encontró una imagen adecuada para esta pregunta.
- **q-1450** (Fantasía) Lo apodan Trancos, es heredero de un reino perdido y se enamora de la elfa Arwen. ¿A qué pueblo pertenece Aragorn? → Humanos: La imagen elegida tiene una licencia no adecuada (pd-no-reason: public domain without a template).
- **q-1452** (Fantasía) Gobierno Gondor mientras no hay rey y soy el padre de Boromir y Faramir. ¿Quién soy? → Denethor: El texto está bien, pero ninguna imagen sirve: son un relieve budista maurya, animales de piedra de las tumbas Ming, grabados del siglo XIX y caricaturas políticas, y nada evoca Gondor ni Minas Tirith. Hace falta una búsqueda nueva, por ejemplo "white stone citadel" o "medieval throne room". No se encontró una imagen adecuada para esta pregunta.
- **q-1463** (Fauna africana) La Gran Migración de ñus da una vuelta completa cada año. ¿Por cuántos países pasa? → 2: La pista 2 delata la respuesta: si un recorrido de ida y vuelta cruza «una frontera», pasa exactamente por 2 países. Hay que cambiarla por una pista sobre el río Mara o la estación seca que no hable de fronteras.
- **q-1485** (Física) Sueltas al mismo tiempo una piedra y una hoja de papel extendida: la piedra llega primero. ¿Qué frena más a la hoja? → La resistencia del aire: Ninguna imagen sirve: los candidatos son una pintura de aves, un ángel, la tripulación de un hidroavión, una locomotora colgando y unos querubines, y nada de eso tiene que ver con objetos que caen o con la resistencia del aire. El texto está bien. Hace falta otra búsqueda, por ejemplo «falling paper sheet» o «crumpled paper ball», o bien una imagen decorativa. No se encontró una imagen adecuada para esta pregunta.
- **q-1519** (Guerra Fría) Este yate llevó en 1956 a Fidel Castro y al Che de México a Cuba, y hoy nombra al periódico oficial cubano. ¿Cómo se llamaba? → Granma: La pista 2 ("Su nombre no viene de ningún lugar de Cuba") descarta de golpe las tres opciones incorrectas (Moncada, Sierra Maestra y Playa Girón son lugares cubanos) y así revela la respuesta. Hay que cambiarla por una pista vaga que no excluya opciones, por ejemplo sobre el tamaño del yate o el número de tripulantes.
- **q-1522** (Guerra Fría) ¿Quién es este cantante, al que todavía llaman 'el Rey'? → Elvis Presley: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-not renewed).
- **q-1528** (Harry Potter) Fui capitán y guardián de quidditch, y lloré de emoción al ganar la copa en mi último año. ¿En qué casa de Hogwarts estuve? → Gryffindor: La pista 2 ("entrené a Harry como buscador") regala la respuesta: Wood era capitán del equipo de Harry, y saber la casa de Harry (q-0079, muy fácil) basta para responder. Debe sustituirse por una pista vaga que no lo ligue al equipo de Harry (p. ej. sobre su obsesión con las tácticas o su puesto de guardián).
- **q-1547** (Historia de la moda) En los años veinte, los vestidos de fiesta eran rectos, cortos y se movían al bailar charlestón. ¿De qué solían ir adornados? → Flecos y cuentas brillantes: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-1554** (Historia del dinero) Soy de papel y sirvo para pagar. Me inventaron hace más de mil años en un país de Asia. ¿En cuál? → China: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-1556** (Historia del dinero) El siclo, que hoy da nombre a la moneda de Israel, empezó como un peso de plata en Mesopotamia. ¿Hace cuánto? → Hace unos 4500 años: Verificación de datos: uncertain. Sources date the shekel differently. One has the word first used around 2150 BC (about 4200 years ago). The weight system is Sumerian, from the 3rd or 4th millennium BC (4500 to 5000+ years ago). 'About 4500 years' is plausible but not exact. Also, 'Ya aparece en el Código de Hammurabi' is true but vague.
- **q-1563** (Historias de la Biblia) Mateo era uno de los apóstoles de Jesús. ¿Cuántos apóstoles tenía Jesús? → 12: La pista 2 («más de 10 y menos de 15») deja solo una opción posible (12), porque 7, 10 y 40 quedan fuera, así que regala la respuesta. Hay que cambiarla por una pista más vaga, por ejemplo una que no excluya todas las opciones incorrectas.
- **q-1566** (Imperio romano) Estás frente a la famosa estatua de Augusto de Prima Porta. ¿En la villa de qué mujer la encontraron? → Livia: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-1923, PD-US-expired).
- **q-1583** (Inventos por accidente) La warfarina, medicamento contra los coágulos, se descubrió estudiando esta planta enmohecida que comía el ganado. ¿Cuál es? → Trébol dulce: El medio está marcado como 'essential' con nota de mostrar el trébol dulce en flor, pero todos los candidatos son vacas comiendo heno. La pregunta no necesita ver la planta (y mostrarla delataría la respuesta), así que conviene cambiar el rol a 'illustrative' y usar el candidato 1 (vacas comiendo heno), que encaja sin delatar nada. No se encontró una imagen adecuada para esta pregunta.
- **q-1604** (Logotipos famosos) Adivina: nací en 1873 para los mineros de California, tengo remaches de cobre y en mi etiqueta dos caballos intentan romperme. ¿Qué soy? → Los jeans: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-1657** (Música del mundo) Me llamaban 'La Voz' y canté 'New York, New York'. Nací en Estados Unidos, pero mis padres venían de otro país. ¿De cuál? → Italia: Las pistas 1 y 2 regalan la respuesta: Italia es la única de las cuatro opciones junto al Mediterráneo y la única con un idioma que viene del latín. La pista 1 debería ser vaga (por ejemplo, sobre la época o la emigración a Estados Unidos) y la pista 2 no debería descartar las tres opciones falsas.
- **q-1666** (Musicales) Soy animadora en Seabrook, escondo mi pelo blanco bajo una peluca y me enamoré de Zed, un zombi. ¿Quién soy? → Addison: Verificación de datos: wrong. Hint 2 is false: in Zombies, Addison's cousin Bucky Buchanan is the captain of the football team, not of the cheerleaders. I answered from memory and did not run a web search.
- **q-1670** (Novela policiaca) Soy la razón por la que alguien comete un crimen: dinero, celos o venganza. Los detectives siempre me buscan. ¿Qué soy? → El móvil: La pista 2 («En España, así también se le llama al teléfono») delata la respuesta: ninguna otra opción es un nombre del teléfono, así que cualquiera que conozca la palabra «móvil» la acierta de inmediato. Hay que cambiarla por una pista más vaga, por ejemplo sobre la tríada móvil, medio y oportunidad, pero sin nombrarla, porque esa tríada está en el dato curioso.
- **q-1709** (Perros) En 1925, perros de trineo como Balto llevaron una medicina por relevos hasta Nome, Alaska. ¿Cuántos kilómetros recorrieron en total? → Unos 1000 km: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-1757** (Premios Óscar) Este premio se entregó por primera vez en 1929. ¿En qué ciudad fue esa primera ceremonia? → Los Ángeles: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-1779** (Puentes famosos) En «Shrek», Shrek y Burro cruzan un puente de tablas que se balancea sobre lava. ¿Cómo se llama ese tipo de puente? → Puente colgante: El dato curioso no está confirmado. Dice que Shrek «empuja de espaldas» a Burro mientras lo distrae, pero en la película Shrek sacude el puente y avanza hacia él, y Burro, discutiendo, retrocede hasta cruzar. Hay que corregir el dato curioso (por ejemplo: «Cuando Burro se congela, Shrek lo distrae y lo hace retroceder sin que se dé cuenta hasta llegar al otro lado») o cambiarlo por otro dato seguro. Verificación de datos: uncertain. Answer (puente colgante) is right. The fun fact doesn't match the scene as described: a source says Shrek shakes the bridge and scares Donkey until he backs across. I found nothing saying Shrek pushes him while distracting him.
- **q-1811** (Redes sociales) ¿Quién creó la red social de este logo? → Mark Zuckerberg: Ningún candidato muestra el logo de Facebook (la «f» blanca sobre fondo azul). Los resultados son material de oficina, una torre de madera, una furgoneta, un ciclón, un logo de un coro y un cartel de campaña. La imagen es esencial y no se puede buscar de nuevo. Hay que conseguir a mano un archivo del logo, por ejemplo «Facebook f logo (2019).svg» de Commons. No se encontró una imagen adecuada para esta pregunta.
- **q-1838** (Reptiles) Medía unos 11 metros, es uno de los cocodrilos más grandes que han existido y lo llamaron «SuperCroc». ¿Dónde se hallaron sus fósiles más famosos? → En el desierto del Sahara: La pista 2 dice que los fósiles «salieron de África», y el Sahara es la única opción africana, así que la pista 2 ya resuelve la pregunta. Debería dar una pista más vaga (por ejemplo, el clima actual del lugar) y dejar África/Níger para la pista 3. Detalle menor: la descripción llama a Sarcosuchus «abuelo de los cocodrilos», pero no es antepasado de los cocodrilos actuales.
- **q-1840** (Reptiles) ¿Para qué cava esta tortuga marina un hoyo en la arena de la playa? → Para poner sus huevos: Ninguna imagen muestra con claridad una tortuga marina cavando en la playa: la 1 es un escaneo en blanco y negro, borroso y tapado por hierba; la 2 y la 3 muestran personas excavando un nido; la 4 es una pintura de un perro; y la 5 es solo un hoyo. Hace falta una foto clara de una tortuga marina cavando su nido (por ejemplo, buscando «sea turtle nesting beach»), o cambiar la pregunta a una imagen ilustrativa sin «esta». No se encontró una imagen adecuada para esta pregunta.
- **q-1854** (Escándalos famosos) ¿En qué país estalló en 2009 un escándalo porque diputados pasaron al Estado gastos como una casita para patos o limpiar el foso de su mansión? → Reino Unido: Verificación de datos: wrong. Hint 2 ('Allí se maneja por la izquierda') also fits the wrong answer Australia, so it is ambiguous. The answer (UK, 2009 expenses scandal, duck house £1,645, moat) is correct.
- **q-1858** (Eslóganes publicitarios) Soy un letrero que brilla en rojo gracias a un gas y anuncio tiendas de noche. ¿Qué inventor me presentó en París en 1910? → Georges Claude: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-architecture).
- **q-1880** (Fauna africana) El springbok, que da nombre a la selección sudafricana de rugby, salta de forma espectacular. ¿Hasta qué altura puede llegar? → Unos 3,5 metros: La altura del salto no está confirmada: fuentes de referencia como Wikipedia dan unos 2 m para el salto del springbok (pronking), y los 3,5 m solo aparecen en fuentes populares. La pista 3 (un aro de baloncesto y un poco más) depende de esa cifra. Conviene usar como respuesta un rango bien documentado (p. ej. «Unos 2 metros» o «Más de 2 metros»), ajustar la pista 3 y mantener los distractores bien alejados. Verificación de datos: uncertain. Sources disagree on springbok jump height: Wikipedia-type sources say up to about 2 m, and popular sources say 3 m or more. 3.5 m is at the high end, and the hint compares it to a hoop (3.05 m).
- **q-1943** (Inventos por accidente) El celofán, que envuelve flores y canastas de regalo, nació sin querer en 1908. ¿Qué intentaba crear su inventor? → Un mantel a prueba de manchas: La pista 1 ("un químico suizo que trabajaba con telas") y la pista 2 ("cubrir tela con una capa fina") delatan la respuesta: el mantel es la única opción de tela, así que las otras tres quedan descartadas enseguida. La pista 1 debería ser vaga (por ejemplo, sobre la época o el país sin mencionar telas) y la pista 2 no debería nombrar la tela.
- **q-1974** (Monedas del mundo) ¿Cómo se llama la moneda que se usa en Japón? → El yen: Se solapa con q-1648 ("Soy la moneda de 1 yen de Japón…"), que dice directamente que la moneda de Japón es el yen: quien vea esa pregunta ya sabe esta respuesta. Hay que quedarse con una de las dos o reformular q-1648 para que no diga "yen de Japón" (por ejemplo, "la moneda japonesa más pequeña").
- **q-1990** (Novela policiaca) La aconsejó el poeta Horacio y la usan la «Odisea» y muchas novelas policiacas. ¿Qué significa «in medias res»? → Empezar en mitad de la acción: El dato curioso es falso: cuando empieza la «Odisea», Ulises lleva casi veinte años lejos de casa (diez de guerra en Troya y casi diez de regreso), no «casi diez años». Hay que corregirlo, por ejemplo a «casi veinte años lejos de casa (casi diez desde la caída de Troya)». Verificación de datos: wrong. El dato curioso es falso: cuando empieza la Odisea, Ulises lleva casi veinte años fuera de Ítaca (diez de guerra en Troya y casi diez de viaje de regreso), no «casi diez años».
- **q-1991** (Novela policiaca) Este escritor puso a su personaje Tom Sawyer a resolver un misterio en «Tom Sawyer, detective». ¿Quién es? → Mark Twain: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-2035** (Quesos) Científicos descubrieron que un famoso queso con huecos los estaba perdiendo porque la leche ya no traía polvo de heno. ¿De qué país es? → Suiza: Se solapa con q-1783, que dice textualmente «queso suizo Emmental» y además pregunta de dónde salen sus huecos, el mismo tema que esta pregunta. Si alguien ve q-1783, ya sabe que la respuesta aquí es Suiza. Habría que descartar una de las dos o cambiar el enfoque de esta por completo.
- **q-2043** (Reality shows) En televisión, ¿qué es el 'prime time'? → El horario con más audiencia: La descripción da la respuesta: «La hora en que el control remoto es el objeto más peleado de la casa» describe justo el horario de más audiencia y descarta la pausa comercial y el estreno de temporada. La pista 1 («Tiene que ver con la hora del día») también descarta esas dos opciones; conviene cambiar la descripción por una broma sobre la televisión que no hable de horarios ni de audiencia.
- **q-2053** (Religiones del mundo) Este es el rostro de una estatua de mármol de Miguel Ángel. ¿Qué personaje del Antiguo Testamento es? → David: Ningún candidato muestra un primer plano del rostro del David de Miguel Ángel: los 1–3 muestran la estatua entera (desnudo completo, y no es el rostro que anuncia la pregunta), el 4 y el 6 son el David de Caravaggio y el 5 es el David de Verrocchio. Hay que buscar una imagen de la cabeza del David (p. ej. "Michelangelo David head"). No se encontró una imagen adecuada para esta pregunta.
- **q-2162** (Shakespeare) En una tragedia de Shakespeare, el protagonista dice al morir: «El resto es silencio». ¿Qué personaje es? → Hamlet: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-1923, PD-US-expired).
- **q-2187** (Terremotos) Suena la alerta sísmica en tu ciudad. ¿Cuál de estas cosas NO puede hacer ese sistema? → Avisar días antes del terremoto: Ninguna imagen sirve: la 1 es un collage militar de operaciones psicológicas, la 2 es un parlante de fiesta con batería de carro en una trajinera y la 3 es una rueda de prensa. Ninguna muestra una alerta sísmica, y la 2 además muestra un altavoz, que es una de las opciones incorrectas. Hay que buscar otra imagen, por ejemplo con «seismograph station» o «earthquake early warning siren»; el texto está bien. No se encontró una imagen adecuada para esta pregunta.
- **q-2202** (Zapatos y accesorios) ¿Cuál de estos personajes NO lleva gafas? → Elsa, de Frozen: La pista 2 ('tiene poderes de hielo') revela la respuesta: entre las cuatro opciones solo Elsa tiene poderes de hielo, así que la pista 2 resuelve la pregunta. Hay que cambiarla por una pista más vaga, por ejemplo que el personaje es de una película de animación reciente o que es de la realeza, pero sin mencionar el hielo.

## Question axes

- move: analogy 55, cause_effect 49, count 22, estimate 42, identify 114, made_of 56, name_concept 111, odd_one_out 51, origin 102, purpose 68, record 16, sequence 34, when 79, who 122, word_meaning 71
- stimulus: detail 34, map_outline 4, none 871, photo 78, sound 3, video 2
- clue: completion 20, direct 453, riddle 232, scenario 117, three_facts 170
- answer_kind: group 80, number 71, person 207, place 98, thing 231, time 84, word 221
- lens: body_senses 43, colombia 32, educational_media 83, everyday 77, history 176, language 147, nature 38, pop_culture 185, popular_science 58, school 62, science_news 20, university 71

## Dropped by the pipeline

- ahorro-y-bancos-7: overlap like q-0427: En Colombia, ¿cómo le dicen a una persona muy tacaña, que no presta ni un lápiz? → Codo: Completa: generoso es a 'mano abierta' como tacaño es a… → Codo
- bebidas-7: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Soy una taza alta y recta, con asa y sin platito, y a menudo traigo una frase impresa. Mi nombre viene del inglés. ¿Qué soy? → Mug
- bichos-raros-5: overlap like q-0386: ¿Qué hace un erizo cuando se asusta? → Se enrolla como una bola: Soy gris, tengo catorce patas y vivo bajo las macetas húmedas. Si me tocas, ¿qué hago? → Me enrollo como una bola
- billetes-del-mundo-16: overlap like q-1158: Me llaman 'el río de los cinco colores' y algunos meses del año mi fondo se pone rojo intenso. ¿Qué me pinta de ese color? → Una planta acuática: Soy el 'río de los cinco colores' y salgo en un billete colombiano. ¿Qué me pinta de rojo? → Una planta acuática
- ciencia-ficcion-17: overlap like q-0939: ¿Qué tiene de especial el cielo de Tatooine, el planeta desértico donde creció Luke Skywalker? → Dos soles: Eres Obi-Wan y acabas de dejar al bebé Luke con sus tíos. ¿En qué planeta te quedas viviendo escondido? → Tatooine
- circo-7: duplicate like q-0648: Este es el río Tíber. ¿Qué capital europea atraviesa? → Roma: En este enorme estadio corrían las carreras de cuadrigas hace 2.000 años. ¿En qué ciudad está? → Roma
- cosas-raras-del-cuerpo-humano-3: overlap like q-0163: En 1928, Alexander Fleming vio un moho creciendo en un plato de laboratorio. ¿Qué medicina descubrió? → La penicilina: Alexander Fleming volvió de vacaciones y vio que un moho mataba bacterias en un plato olvidado: así nació la penicilina. ¿En qué año? → 1928
- dinosaurios-11: overlap like q-1333: Hatzegopteryx, un reptil volador enorme, cazaba pequeños dinosaurios en una isla de la actual Rumania. ¿En qué periodo vivió? → Cretácico: En el Sahara se hallaron restos del carcarodontosaurio, un carnívoro gigante que convivió con el espinosaurio. ¿En qué periodo vivió? → Cretácico
- disenadores-de-moda-11: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Es un perfume de Giorgio Armani, salió en los años 90 y lo inspiró el mar de la isla italiana de Pantelleria. ¿Cómo se llama? → Acqua di Giò
- duos-famosos-16: overlap like q-0414: En el torneo de tenis de Wimbledon, en Londres, ¿de qué color tiene que ser casi toda la ropa de los jugadores? → Blanco: Se juega sobre césped, queda en Londres y Roger Federer lo ganó 8 veces. ¿Qué torneo es? → Wimbledon
- empresas-famosas-11: overlap like q-0213: Mira este escudo en un carro: ¿de qué marca es? → Ferrari: El toro dorado es a Lamborghini como el caballito negro de los autos rojos de carreras es a… → Ferrari
- empresas-famosas-12: overlap like q-0020: ¿Cuál es el río más caudaloso (con más agua) del mundo? → El Amazonas: Es el río con más agua del mundo, cruza Brasil y le da nombre a la tienda de Prime Video. ¿Cuál es? → Amazonas
- estilos-arquitectonicos-14: overlap like q-0624: ¿Qué estilo comparten las entradas del metro de París con tallos de hierro, los carteles de Alfons Mucha y las casas curvas de Victor Horta? → Art nouveau: Son de hierro verde, parecen tallos y flores, y Hector Guimard las diseñó para París hacia 1900. ¿Para qué sirven? → Para entrar al metro
- exploradores-y-descubrimientos-8: overlap like q-0722: El pueblo de Tenzing Norgay, que subió al Everest con Hillary, dio su nombre a los guías del Himalaya. ¿Cuál es? → Sherpa: Son guías de montaña, cargan las expediciones y uno de ellos, Tenzing Norgay, coronó el Everest en 1953. ¿Dónde viven los sherpas? → En el Himalaya
- fantasia-5: overlap like q-1389: Ando descalzo con pies grandes y peludos, y vivo en un agujero redondo bajo una colina. ¿De qué tierra soy? → La Comarca: Son bajitos, andan descalzos y les encanta el segundo desayuno. ¿Qué pueblo vive en La Comarca? → Hobbits
- faraones-0: overlap like q-0833: Este famoso busto de piedra pintada fue hallado en 1912 en Amarna, Egipto. ¿A qué reina representa? → Nefertiti: Soy la ciudad que un faraón construyó desde cero para adorar solo al dios sol Atón, y me abandonaron cuando él murió. ¿Qué soy? → Amarna
- fauna-africana-14: overlap like q-0080: En 'El rey león', ¿cómo se llama el papá de Simba? → Mufasa: En El Rey León, ¿quién es el papá de Simba? → Mufasa
- fisica-5: overlap like q-0850: Una bola pesadísima cuelga de un cable larguísimo; con las horas, su vaivén cambia de dirección y tumba palitos puestos en círculo. ¿Qué demuestra? → Que la Tierra gira sobre sí misma: Colgué un péndulo gigante bajo la cúpula del Panteón de París y demostré que la Tierra gira. ¿Quién soy? → Léon Foucault
- fisica-6: overlap like q-0720: Saltas de un avión y, después de unos segundos boca abajo, ya no caes más rápido porque el aire te frena. ¿A qué velocidad vas más o menos? → 200 km/h: Soy la velocidad máxima de un paracaidista en caída libre, cuando el aire frena tanto como tira la gravedad. ¿Cómo me llamo? → Velocidad terminal
- fisica-11: overlap like q-0060: Un 'año luz' es una medida de... → Distancia: Los kilómetros por hora miden velocidad. ¿Cuál de estas NO es una medida de velocidad? → El año luz
- formas-2: overlap like q-1489: Son segmentos rectos, forman el borde de un polígono y un triángulo tiene tres. ¿Qué son? → Los lados: El prefijo «poli» aparece en «polígono», en «Polinesia» y en «polideportivo». ¿Qué significa? → Muchos
- formula-1-y-automovilismo-2: overlap like q-1395: Fui una niña; mi papá vendía autos y le puso mi nombre a la marca de la estrella de tres puntas. ¿Cómo me llamo? → Mercedes: Su logo es una estrella de tres puntas, sus carros de carreras se apodan 'Flechas Plateadas' y con ella Hamilton ganó seis títulos. ¿Qué marca es? → Mercedes
- frases-celebres-0: overlap like q-0055: ¿Quién fue la primera persona en caminar sobre la Luna? → Neil Armstrong: ¿Quién dijo «Es un pequeño paso para el hombre, pero un gran salto para la humanidad» al pisar la Luna? → Neil Armstrong
- frases-celebres-2: overlap like q-0007: ¿Qué escritor colombiano ganó el Premio Nobel de Literatura en 1982? → Gabriel García Márquez: ¿En qué año dio Gabriel García Márquez su discurso «La soledad de América Latina» al recibir el Nobel? → 1982
- guerra-fria-8: overlap like q-1352: Coco Chanel es al vestidito negro como Levi Strauss es al… → Bluyín: Soy el pantalón azul que los jóvenes soviéticos compraban de contrabando. Mi marca más famosa lleva el nombre de mi creador. ¿Quién es? → Levi Strauss
- hip-hop-y-rap-17: overlap like q-1541: "Lose Yourself", de Eminem, fue la primera canción de rap en ganar un Óscar. ¿En qué década salió? → Los años 2000: Esta avenida de Detroit le dio nombre a una película de 2002 sobre batallas de rap. ¿Qué rapero la protagonizó? → Eminem
- inventos-por-accidente-14: overlap like q-1259: Este parabrisas se rajó, pero no se deshizo en pedazos. ¿De qué está hecho? → Vidrio laminado: Tres pistas: está en el parabrisas de los vehículos, al golpearse se agrieta como telaraña sin desarmarse y nació cuando a un químico se le cayó un frasco. ¿De qué está hecho? → Dos vidrios con plástico en medio
- juegos-olimpicos-de-invierno-16: overlap like q-0073: ¿Cuál es el ratón de dibujos animados más famoso del mundo? → Mickey Mouse: Mira la foto de este espectáculo sobre hielo: ¿qué personaje famoso está patinando? → Mickey Mouse
- leyendas-y-supersticiones-3: overlap like q-0854: En una casa museo de Aracataca, Magdalena, hay mariposas amarillas en las paredes y un letrero que dice 'Macondo'. ¿Qué une todo eso? → La vida de García Márquez: Se dice que anuncia buenas noticias o dinero; en «Cien años de soledad» siguen a Mauricio Babilonia, y despidieron a García Márquez. ¿Qué es? → La mariposa amarilla
- logotipos-famosos-3: hard fail: correct 3, unambiguous 4, no_giveaway 1, no_overlap 5: En el logo de esta carrera famosa se esconde una persona dibujada con las letras. ¿Quién es? → Un ciclista
- lugares-sagrados-12: overlap like q-1024: ¿Qué creyentes celebran sobre todo la fiesta de las luces de esta foto, con lamparitas de barro y dibujos de colores en el suelo? → Los hindúes: Este templo del sur de la India está cubierto de miles de figuras de dioses. ¿Los fieles de qué religión rezan aquí? → Hindúes
- maravillas-del-mundo-8: overlap like q-0431: Mira la foto: ¿cómo se llama este bote largo y delgado que un remero maneja de pie con un solo remo? → Góndola: Llevo turistas por el Gran Canal de Venecia en una barca negra y alargada, remando de pie. ¿Quién soy? → El gondolero
- mascotas-de-marcas-9: overlap like empresas-famosas-11: El toro dorado es a Lamborghini como el caballito negro de los autos rojos de carreras es a… → Ferrari: El caballo es a Porsche como ¿qué animal es a Lamborghini? → Toro
- mascotas-de-marcas-16: overlap like logotipos-famosos-5: Antes de la manzana mordida, el primer logo de Apple, de 1976, mostraba a un científico sentado bajo un árbol. ¿Quién era? → Isaac Newton: El panda es a WWF como la manzana mordida es a… → Apple
- mitologia-romana-2: overlap like q-0051: ¿Qué planeta es conocido como el planeta rojo? → Marte: Es rojizo, tiene dos lunas pequeñas y lleva el nombre del dios romano de la guerra. ¿Qué planeta es? → Marte
- mitologia-romana-9: overlap like q-0056: ¿Cuál es el planeta más caliente del sistema solar? → Venus: Este planeta, cubierto de nubes espesas, lleva el nombre de la diosa romana del amor. ¿Cuál es? → Venus
- monarquia-britanica-3: overlap like q-0218: Según una vieja leyenda, si cierto tipo de ave abandona la Torre de Londres, caerá el reino. ¿Qué aves viven por eso siempre en la Torre? → Cuervos: Según la tradición, ¿cuántos de estos pájaros debe haber como mínimo en la Torre de Londres para que el reino no caiga? → 6
- monedas-del-mundo-11: overlap like q-0235: Mira esta famosa máscara de oro: ¿de qué faraón es? → Tutankamón: Esta moneda de una libra egipcia muestra la máscara de un famoso faraón. ¿Cuál? → Tutankamón
- monumentos-famosos-2: overlap like q-0587: ¿Para qué sirve este edificio del centro de Bogotá? → Es la sede y residencia oficial del presidente: Soy una casa en el centro de Bogotá y llevo el nombre del prócer Antonio Nariño. ¿Para qué sirvo? → Casa y oficina del presidente
- monumentos-famosos-7: overlap like q-0953: Tres pistas: lo diseñó Dédalo, estaba en Creta y Teseo salió de él siguiendo el hilo de Ariadna. ¿Qué construcción es? → El laberinto: Estas son las ruinas del palacio de Cnosos, en la isla de Creta. Según el mito, ¿qué monstruo vivía en su laberinto? → El Minotauro
- musica-pop-11: overlap like q-0051: ¿Qué planeta es conocido como el planeta rojo? → Marte: Es rojo, es el cuarto planeta desde el Sol y en inglés le presta su nombre al cantante Bruno Mars. ¿Qué planeta es? → Marte
- origen-de-las-marcas-12: overlap like q-1193: Esta mezcla de maicena y agua se pone dura si la golpeas o la aprietas, pero escurre como líquido si la dejas quieta. ¿Qué tipo de sustancia es? → Un fluido no newtoniano: Mezclas maicena con poca agua y golpeas la mezcla con el puño. ¿Qué pasa? → Se pone dura como un sólido
- peces-2: overlap like q-0298: Mira la foto: ¿cómo se llama este pez? → Pez payaso: Noche de películas: 'Mickey' es a 'ratón' como 'Nemo' es a… → pez payaso
- piramides-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Soy una colina junto a Visoko, en Bosnia. En 2005 alguien anunció que era la pirámide más grande del mundo. ¿Quién? → Semir Osmanagić
- prehistoria-16: overlap like q-1743: La Edad de Piedra es a la piedra como la primera etapa de la Edad de los Metales es al… → Cobre: Ves a un herrero martillando hierro al rojo vivo. La época en que se empezó a trabajar ese metal llegó justo después de… → La Edad del Bronce
- premios-oscar-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Cuántas veces ha presentado el comediante Steve Martin la gala de los Óscar? → 3
- productos-del-supermercado-4: overlap like logotipos-famosos-12: El señor del logo de la avena Quaker viste como un cuáquero. ¿Qué colonia inglesa fundó un cuáquero como refugio para su grupo? → Pensilvania: El señor de sombrero y pelo largo del empaque de avena Quaker representa a un miembro de un grupo. ¿Cuál? → Un cuáquero
- quesos-8: overlap like q-1378: Estás desayunando arepa con queso. La arepa se hace con maíz, como el queso se hace con… → Leche: Viene de Italia, es durísimo y lo rallan encima de los espaguetis. ¿De qué está hecho el queso parmesano? → De leche de vaca
- quimica-0: overlap like q-1194: Vinagre, jugo de limón y gaseosa de cola: ¿qué tienen en común, que si dejas un huevo crudo en ellos varios días le van deshaciendo la cáscara? → Son ácidos: ¿Cuál de estos NO es un ácido, sino una base? → Bicarbonato de sodio
- refranes-y-dichos-4: overlap like q-0284: Escucha: ¿qué fenómeno natural produce este sonido? → Un rayo: Soy una luz que baja del cielo en las tormentas y dicen que alguien muy veloz es 'rápido como un…'. ¿Qué soy? → rayo
- religiones-del-mundo-3: overlap like q-1674: Tenía claustro, iglesia y biblioteca, y allí se copiaban libros a mano. ¿Quiénes vivían en una abadía medieval? → Monjes: Esta montaña sagrada de Grecia está llena de monasterios. ¿Quiénes viven en ella? → Monjes
- reptiles-14: overlap like q-1240: Su cabeza plana parece una hoja muerta, respira por una nariz en forma de tubo y caza peces sorbiéndolos. ¿Dónde vive esta tortuga? → En ríos de Sudamérica: La matamata vive en ríos de Sudamérica, parece hojarasca y no mastica. ¿Para qué abre de golpe su enorme boca? → Para aspirar peces con el agua
- ahorro-y-bancos-10: hard fail: correct 5, unambiguous 3, no_giveaway 5, no_overlap 5: Es un papel con el que tú mismo te comprometes a pagarle una suma a alguien, casi siempre por un préstamo. ¿Qué es? → Un pagaré
- bebidas-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En las películas de Navidad, los niños dejan un vaso de leche para Papá Noel. ¿Qué le ponen al lado? → Galletas
- estilos-arquitectonicos-16: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Soy una puerta corrediza japonesa con marco de madera y dejo pasar la luz suavemente. ¿De qué está hecha mi parte clara? → Papel
- eurovision-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Somos un grupo alemán de música disco: cantamos en Eurovisión 1979 y luego triunfamos con «Moskau». ¿Quiénes somos? → Dschinghis Khan
- exploradores-y-descubrimientos-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En 1507, un mapa alemán escribió por primera vez un nombre para el Nuevo Mundo. ¿Qué nombre? → América
- faraones-3: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Mira la cabeza de esta estatua de una noble egipcia. ¿Qué lleva puesto sobre la cabeza? → Una peluca
- faraones-14: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: En Guiza hay tres grandes pirámides. ¿Qué faraón mandó construir la más pequeña de las tres? → Micerinos
- fauna-africana-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Los elefantes se comunican con infrasonidos. ¿Por debajo de cuántos hercios ya no los oye el oído humano? → 20
- fisica-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Mide 30,48 cm y los pilotos dicen la altura del avión con ella. ¿Qué unidad es? → El pie
- fisica-15: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: La ley de Hooke, formulada por Robert Hooke en el siglo XVII, se estudia en física escolar. ¿Qué objeto describe? → Un resorte
- fotografia-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Cómo se llama el género de fotos espontáneas de gente desconocida en plena vida de la ciudad? → Fotografía callejera
- guerra-fria-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En Berlín Oriental, un hombrecito con sombrero se hizo famosísimo en las calles. 'Ampelmännchen' significa 'hombrecito del…' → Semáforo
- guerra-fria-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Qué tratado de 1968 reconoce solo a cinco países como potencias nucleares y pide al resto no fabricar bombas atómicas? → Tratado de No Proliferación Nuclear
- harry-potter-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Fred y George inventaron los caramelos longuilinguos, y Dudley se comió uno. ¿Qué hacen esos caramelos? → Hacen crecer la lengua
- harry-potter-9: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Soy el jugo naranja que toman en el Gran Comedor de Hogwarts, hecho de la misma hortaliza de Halloween. ¿De qué estoy hecho? → Calabaza
- harry-potter-14: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Completa el nombre del juego de cartas que Harry y Ron juegan en Hogwarts: 'Snap…' → explosivo
- hip-hop-y-rap-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es un líquido, huele fuerte y Daddy Yankee pedía "dame más" de él en su gran éxito. ¿Para qué sirve en la vida real? → Para mover los motores de los vehículos
- historia-de-la-moda-12: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: ¿Qué cambió en la moda cuando llegó el prêt-à-porter? → Se compraba la ropa ya hecha, por tallas
- historias-de-la-biblia-17: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Viene del hebreo y le da nombre a un día de la semana en español. ¿Qué significa «shabbat»? → Descanso
- imperio-romano-7: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: El garum se hacía dejando pescado fermentar al sol, se guardaba en ánforas y costaba caro. ¿Para qué se usaba? → Para condimentar la comida
- imperio-romano-9: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: En la película «Espartaco», muchos esclavos gritan «¡Yo soy Espartaco!». ¿Qué significa ese grito? → Que todos protegen a su líder
- canciones-infantiles-2: overlap like q-0864: Esta canción nació en la España del siglo XV y su nombre viene de 'villano'. En su forma clásica, ¿de qué partes se compone? → Estribillo y coplas: Se canta en diciembre con panderetas y maracas. ¿Qué tipo de canción es 'Antón tiruriruriru'? → Un villancico
- james-bond-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Estas cuevas excavadas en la roca de Matera, Italia, salen en una persecución de 007. ¿Para qué se usaron durante siglos? → Como viviendas
- james-bond-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En «El mañana nunca muere», la agente Wai Lin ayuda a Bond. ¿Para qué país espía? → China
- leyendas-y-supersticiones-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La mano de Fátima es una mano abierta, a veces con un ojo en la palma, que protege del mal de ojo. ¿De qué región viene? → Oriente Medio y norte de África
- logotipos-famosos-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Completa: en los videojuegos, cuando 'nerfean' a un personaje, significa que… → lo hacen más débil
- logotipos-famosos-12: overlap like productos-del-supermercado-4: El señor de sombrero y pelo largo del empaque de avena Quaker representa a un miembro de un grupo. ¿Cuál? → Un cuáquero: El señor del logo de la avena Quaker viste como un cuáquero. ¿Qué colonia inglesa fundó un cuáquero como refugio para su grupo? → Pensilvania
- maravillas-del-mundo-17: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Soy la torre más alta del mundo: mido 634 metros y me inauguraron en 2012. ¿En qué país estoy? → Japón
- mascotas-raras-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En el ciclo del nitrógeno de un acuario, ¿cuál de estas sustancias NO forma parte del ciclo? → Cloro
- mascotas-raras-8: fact-check wrong: Hint 1 is inaccurate: Darwin was born in Feb 1809 and saw maras in Patagonia in 1833–34, so he was about 24–25, not 23.: ¿Qué famoso naturalista escribió sobre las maras durante su viaje por la Patagonia en la década de 1830? → Charles Darwin
- mitologia-romana-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En el arte medieval, una diosa romana con los ojos vendados gira una rueda que sube y baja a reyes y mendigos. ¿Quién es? → Fortuna
- monarquia-britanica-17: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: Brilla con diamantes, era de la familia Spencer y Diana la llevó el día de su boda. ¿Qué joya es? → Una tiara
- monedas-del-mundo-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Completa: la moneda de Honduras se llama lempira en honor a Lempira, que fue un… → Cacique indígena
- monedas-del-mundo-6: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 4: ¿Qué moneda famosa debe su nombre al tálero, una antigua moneda de plata alemana? → Dólar
- monumentos-famosos-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Este edificio con cúpula está en La Habana, Cuba. ¿Para qué se construyó? → Para el Congreso
- musica-del-mundo-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El arpa es el símbolo nacional de un país europeo y aparece hasta en sus monedas. ¿Cuál? → Irlanda
- musicales-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En la mitología griega, Talía es a la comedia como Melpómene es a… → la tragedia
- numeros-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es de día y las dos agujas del reloj apuntan justo hacia arriba. ¿Qué hora es? → Las 12 del día
- numeros-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En el calendario de pagos, «semana» es a 7 días como «quincena» es a… → 15 días
- numeros-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: «Cuarentena» viene de Venecia: era el tiempo que los barcos esperaban antes de desembarcar. ¿Cuántos días? → 40
- origen-de-las-marcas-6: overlap like q-1772: Es un polvo blanco y suave, se pone en la piel del bebé tras el baño y Johnson's lo vende hace más de cien años. ¿Qué es? → Talco: Soy el champú amarillo de Johnson's y mi lema es 'No más lágrimas'. ¿Para quién me hicieron? → Para los bebés
- origen-de-las-marcas-7: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Soy una bañera con chorros de agua y burbujas, y llevo el apellido de unos hermanos italianos. ¿Quiénes eran? → Los hermanos Jacuzzi
- origen-de-las-marcas-13: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: Soy un cubito que le da sabor a la sopa y llevo el apellido del suizo que me creó. ¿Quién era? → Julius Maggi
- perros-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Escucha: este ruido asusta muchísimo a muchos perros. ¿Qué es? → Fuegos artificiales
- piramides-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Camino de piedra, techado en algunos casos; unía el templo junto al Nilo con el de la pirámide; por él pasaba el cortejo del faraón. ¿Cómo se llama? → Calzada
- piramides-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: Estás en Chichén Itzá en el equinoccio y ves bajar la serpiente de sombra por la escalera. ¿Cuántos triángulos de luz forman su cuerpo? → 7
- poesia-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿De qué país son las 'calaveritas literarias', versos burlones que 'entierran' en broma a alguien que está vivo? → México
- castillos-17: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Mira este detalle de una pieza de ajedrez. ¿Cuál es? → La torre
- circo-0: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Mezclo acróbatas, teatro, música y luces, y el Cirque du Soleil es mi ejemplo más famoso. ¿Qué tipo de circo soy? → El circo contemporáneo
- premios-oscar-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En 1999, Roberto Benigni fue el primer hombre en ganar el Óscar a Mejor actor con un papel que no era en inglés. ¿En qué idioma? → Italiano
- productos-del-supermercado-5: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Es un nombre inventado, aparece en los empaques de Halls y promete refrescar. ¿Qué une «Mentho-Lyptus»? → Mentol y eucalipto
- productos-del-supermercado-16: hard fail: correct 5, unambiguous 5, no_giveaway 1, no_overlap 5: La marca de champú Pantene tomó su nombre de un ingrediente para el cabello. ¿Cuál? → Pantenol
- puentes-famosos-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Este viaducto de tren sale en varias películas. ¿Qué personaje lo cruza en tren? → Harry Potter
- puentes-famosos-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Completa: «Pilar» es a puente de piedra como «___» es a puente de pontones. → Barca flotante
- puentes-famosos-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Paseas por París y cruzas el Pont Neuf, que significa «Puente Nuevo». ¿Cuándo se terminó? → Hace unos 400 años
- quesos-6: fact-check wrong: The answer (a fungus, Penicillium roqueforti) is right, but the hint 'de la misma familia que los champiñones' is inaccurate. Penicillium is a mold (Ascomycota), mushrooms are Basidiomycota. They share only the kingdom.: Pinta de azul las vetas del queso Roquefort mientras este madura en cuevas del sur de Francia. ¿Qué es? → Un hongo
- rascacielos-7: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: En rascacielos como el Burj Khalifa, algunos ascensores paran en dos pisos seguidos al mismo tiempo. ¿Cómo se llaman? → Ascensor de doble cabina
- reality-shows-10: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Son gemelos: uno es constructor y el otro vende casas. ¿Qué les hacen a las casas en su famoso programa de televisión? → Remodelación
- reality-shows-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Estás viendo un concurso en la tele. ¿Cuál de estas palabras NO sirve para llamar a quienes compiten? → Presentadores
- rock-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Los Ramones arrancaban casi cada canción gritando una cuenta rápida en inglés. ¿Hasta qué número contaban? → 4
- segunda-guerra-mundial-7: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Soy Gueorgui Zhúkov: defendí Moscú, gané en Stalingrado y me llamaron el mariscal de la victoria. ¿Qué ejército comandaba? → El Ejército Rojo
- shakespeare-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es una palabra inglesa, significa 'solitario' y su primer uso escrito conocido está en 'Coriolano' de Shakespeare. ¿Cuál es? → Lonely
- telenovelas-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Es una telenovela argentina de 2006, la protagoniza Pablo Echarri y se inspira en una novela clásica del siglo XIX. ¿Cuál es? → Montecristo
- templos-y-catedrales-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿En qué siglo se terminó la gigantesca Mezquita Hassan II de Casablanca, en Marruecos? → Siglo XX
- zapatos-y-accesorios-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Las encontraron en los pies de la momia de Tutankamón, imitan sandalias de fibra y nunca se usaron para caminar. ¿De qué eran? → Oro
- zapatos-y-accesorios-15: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: ¿Para qué sirve este bolsito tan pequeño? → Para guardar monedas
- circo-9: hard fail: correct 4, unambiguous 3, no_giveaway 5, no_overlap 4: ¿En qué siglo se empezó a llamar «circo» al espectáculo de acróbatas, payasos y caballos? → Siglo XVIII
- circo-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Mi compañera se queda quieta frente a una tabla de madera y yo, desde lejos, clavo objetos afilados justo a su alrededor. ¿Quién soy? → El lanzador de cuchillos
- cosas-raras-del-cuerpo-humano-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Soy un saquito diminuto escondido en tu piel. De mí crece algo que te cortan en la peluquería. ¿Qué crece de mí? → El pelo
- cosas-raras-del-cuerpo-humano-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Somos cientos de millones de bolsitas diminutas, como racimos de uvas, y por nosotras el oxígeno pasa a tu sangre. ¿Dónde vivimos? → En los pulmones
- cosas-raras-del-cuerpo-humano-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Soy la molécula con la que tu cuerpo se libra del nitrógeno que le sobra, y me fabrica el hígado. ¿Cómo me llamo? → Urea
- criquet-4: overlap like q-1594: Tengo cinco casitas, una para cada dedo, y en la nieve te protejo del frío. ¿Qué soy? → Unos guantes: Es de cuero, se pone en una sola mano y sirve para atrapar la bola en béisbol. En críquet, casi todos atrapan sin él. ¿Qué es? → El guante
- criquet-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En 2021 nació en Inglaterra un torneo de críquet en el que cada equipo lanza 100 bolas por turno. ¿Cómo se llama? → The Hundred
- criquet-10: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: En el 'stoolball', un antiguo juego inglés de granja emparentado con el críquet, ¿qué se usaba como blanco? → Un taburete
- dioses-griegos-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La palabra «tridente», el arma de tres puntas del dios del mar, significa literalmente «tres…» → dientes
- dioses-griegos-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Este dios griego era mitad cabra, tocaba una flauta de cañas y su grito causaba un miedo repentino. ¿Qué palabra nació de su nombre? → Pánico
- dioses-griegos-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: La diosa Ceres dio origen a la palabra «cereal» y bautizó a un planeta enano. ¿Qué civilización la adoraba con ese nombre? → Roma antigua
- disenadores-de-moda-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Con él se hacen los tutús de ballet, los velos de novia y los mosquiteros. ¿Qué es el tul? → Una tela fina tipo malla
- disenadores-de-moda-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El 'wrap dress' hizo famosa a la diseñadora Diane von Fürstenberg en 1974. ¿Qué tipo de vestido es? → Uno que se cruza y se amarra
- diseno-de-objetos-6: hard fail: correct 4, unambiguous 2, no_giveaway 4, no_overlap 4: Derrito granitos de plástico y los inyecto a presión en un molde de acero. ¿Qué fabrico así? → Fichas de LEGO
- diseno-de-objetos-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Estás en la barra de la cocina, en un asiento alto sin respaldo ni brazos: un taburete. ¿De qué idioma viene esa palabra? → Francés
- duos-famosos-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En la serie animada «Ren y Stimpy», Ren es un perro y Stimpy es un… → Gato
- el-senor-de-los-anillos-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Soy la escritura élfica que inventó Fëanor y me llamo tengwar. ¿Qué significa mi nombre en quenya? → Letras
- el-senor-de-los-anillos-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Somos los descendientes de Númenor, Aragorn es uno de nosotros y nos llaman Dúnedain. ¿Qué significa nuestro nombre? → Hombres del Oeste
- revolucion-francesa-11: overlap like q-0108: ¿Qué revolución comenzó en 1789 con la toma de la Bastilla? → La Revolución francesa: ¿En qué año empezó la Revolución francesa con la toma de la Bastilla? → 1789
- segunda-guerra-mundial-11: overlap like q-0084: ¿Quién dirigió las películas 'E.T.' y 'Jurassic Park'? → Steven Spielberg: Este director ganó su primer Óscar a mejor director con 'La lista de Schindler'. ¿Quién es? → Steven Spielberg
- segunda-guerra-mundial-13: duplicate like q-1423: Sandie Shaw ganó Eurovisión 1967 cantando descalza «Puppet on a String». ¿Qué país del mapa representaba? → Reino Unido: Este cartel de 1939 casi no se usó en la guerra; hoy aparece en tazas y camisetas. ¿Qué país lo imprimió? → Reino Unido
- telenovelas-6: overlap like q-0067: ¿Qué ritmo colombiano se toca tradicionalmente con acordeón, caja y guacharaca? → Vallenato: En la fiesta suena 'La gota fría' de Carlos Vives y todos cantan '¡Acordate, Moralito!'. ¿Qué género musical es? → Vallenato
- templos-y-catedrales-7: overlap like q-0526: Estás en Popayán en Semana Santa y ves pasar, cargados en hombros, el del Señor del Huerto, el de la Dolorosa y el del Santo Sepulcro. ¿Con qué palabra se nombran los tres? → Pasos: Las procesiones de Popayán, con siglos de historia, son famosas en todo el mundo. ¿En qué época del año salen? → Semana Santa
- templos-y-catedrales-8: overlap like lugares-sagrados-12: Este templo del sur de la India está cubierto de miles de figuras de dioses. ¿Los fieles de qué religión rezan aquí? → Hindúes: Nazco en el Himalaya, y en mis orillas, en la ciudad de Benarés, millones se bañan para purificarse. ¿Quiénes son? → Los hindúes
- trajes-tipicos-del-mundo-13: overlap like q-1660: Soy la fiesta más famosa de Brasil, con plumas, lentejuelas y carrozas gigantes. ¿Quiénes compiten desfilando en mí? → Escuelas de samba: Se baila con trajes de plumas y lentejuelas, nació en Brasil y es la reina del Carnaval de Río. ¿Qué baile es? → Samba
- zapatos-y-accesorios-16: overlap like q-0312: Es millonario, no tiene ningún superpoder, sale de noche a vigilar su ciudad y tiene su guarida secreta en una cueva. ¿Qué superhéroe es? → Batman: No tengo superpoderes, pero mi cinturón amarillo está lleno de aparatos y bumeranes. ¿Quién soy? → Batman
