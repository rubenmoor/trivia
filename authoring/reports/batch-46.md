# batch-46

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): radio-and-internet, protected-areas, flamenco-and-copla, tv-shows-and-presenters, monuments, regions-and-provinces, tv-series, regional-speech, transition-and-democracy, bourbons-and-19th-century, regional-dishes, sportspeople, legends-and-superstitions, money-and-services, transport, spanish-cinema, painting-and-architecture, drinks, empire, childrens-tv, school-and-home, sayings, al-andalus-and-reconquista, regional-symbols, co-official-languages, pop-and-rock, team-and-traditional-sports
- Merged: 271 (q-14219…q-14489)
- Approved: 255
- Needs work: 16
- Dropped by the pipeline: 62
- Reviewed by: claude-opus-5-5
- Claude calls: 583, about $80.00 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-44, batch-45; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-44 | batch-45 | batch-46 |
|---|---|---:|---:|---:|
| source locale |  | en | de | es-ES |
| drafts |  | 305 | 308 | 333 |
| skipped slots |  | 145 | 178 | 153 |
| dropped |  | 61 | 52 | 62 |
| drop rate | ≤ 20.0 % | 20.0 % ✓ | 16.9 % ✓ | 18.6 % ✓ |
| dropped: hard fail correct |  | 1 | 0 | 0 |
| dropped: hard fail unambiguous |  | 2 | 0 | 2 |
| dropped: hard fail no_giveaway |  | 17 | 11 | 13 |
| dropped: overlap |  | 43 | 40 | 43 |
| dropped: duplicate |  | 0 | 1 | 3 |
| dropped: fact-check wrong |  | 0 | 0 | 1 |
| merged |  | 244 | 256 | 271 |
| approved |  | 221 | 223 | 255 |
| needs_work |  | 23 | 33 | 16 |
| needs_work rate | ≤ 20.0 % | 9.4 % ✓ | 12.9 % ✓ | 5.9 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.4 % ✓ | 3.1 % ✓ | 1.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.8 % ✓ | 2.3 % ✓ | 1.1 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.4 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.4 % ✓ | 0.4 % ✓ | 1.1 % ✗ |
| needs_work: media | ≤ 10.0 % | 7.4 % ✓ | 9.0 % ✓ | 3.0 % ✓ |
| media: no pick in review 1 |  | 26 | 44 | 32 |
| media: recovered by research |  | 17 | 28 | 25 |
| media: no pick at record |  | 9 | 16 | 7 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 14.4 % ✓ | 13.6 % ✓ | 14.7 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 59.8 % ✓ | 57.6 % ✓ | 67.4 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 2.67 ✗ | 1.15 ✓ | 1.31 ✓ |
| approved 11–15 |  | 44 | 47 | 58 |
| top move | ≤ 25.0 % | 13.5 % ✓ | 14.5 % ✓ | 18.1 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 85.2 % | 78.1 % | 79.0 % |
| values stimulus |  | 5 | 6 | 4 |
| top clue | ≤ 60.0 % | 39.3 % ✓ | 43.0 % ✓ | 50.2 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 26.6 % ✓ | 26.6 % ✓ | 18.8 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.9 % ✓ | 18.8 % ✓ | 22.9 % ✓ |
| values lens |  | 11 | 11 | 9 |
| media share | 15.0 %–50.0 % | 14.8 % ✗ | 21.9 % ✓ | 21.0 % ✓ |
| mean fun | ≥ 3.40 | 3.54 ✓ | 3.46 ✓ | 3.43 ✓ |
| cost $ |  | $65.01 | $75.76 | $76.48 |
| $ per approved | ≤ $0.35 | $0.29 ✓ | $0.34 ✓ | $0.30 ✓ |
| calls |  | 480 | 496 | 523 |
| calls per approved |  | 2.17 | 2.22 | 2.05 |
| wall time h |  | 1.79 | 1.92 | 2.06 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✓ pass | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 56 (2 %)
- Major among review needs work: 3 of 4 (75 %)
- Problems by kind: giveaway 8 (1 major), fact 1 (0 major), overlap 1 (1 major), media 4 (3 major), difficulty 1 (0 major), other 1 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.51

Major findings on approved questions:

- **q-14353**: media, other — The image chosen, «2012 Catalan independence protest (105).JPG», is a political photo. It probably shows flags and banners, which is a bad fit for a light family question about vocabulary and could embarrass the gamemaster. It should be swapped for something neutral, such as a Catalan town square («Plaça Major Vic»). Everything else holds up: «plaça» means «plaza», «ce trencada» is the right Catalan name for «ç», and French and Portuguese do use the letter. The question also doesn't repeat any related one (the closest, «rúa», asks a different word), and a difficulty of 3 is fair. (http://127.0.0.1:8001/review/q-14353)

## Needs work

- **q-14246** (co-official-languages) En catalán, «porta» es a «puerta» como «carrer» es a… → calle: Hint 3 («En gallego se dice "rúa"») together with the revealed answer "calle" states exactly the fact asked by approved q-11273 ("En gallego, ¿qué es una «rúa»?" → una calle), so playing this question gives that one away. Replace hint 3 with a strong hint that doesn't use the Galician word (for example: «Avenida, plaza, paseo… es la más común de todas»).
- **q-14247** (co-official-languages) Mira el mapa: la sobrasada, ese embutido rojo que se unta en el pan, es típica de esta isla. ¿Cuál es? → Mallorca: The question says «Mira el mapa» and needs an essential map or silhouette of Mallorca, but none of the six candidates is a map; all are photos taken on the island. A new search isn't allowed. Search Commons for something like "Mallorca island silhouette map" (no labels), or drop the map framing. Also, without the map, Menorca would also be defensible, because it makes sobrasada too. No se encontró una imagen adecuada para esta pregunta.
- **q-14248** (co-official-languages) Mira el mapa: en esta comunidad, cada marzo, se plantan y se queman «les Falles». ¿Cuál es? → La Comunidad Valenciana: None of the six candidates shows the Valencian Community: they are Madrid district maps (1, 3, 6), a Telugu Wikipedia example (2), a Cardiff map (4) and a South Carolina map (5). The question says «Mira el mapa», so it needs an essential locator map of the Valencian Community with no labels, and no new search is allowed. Supply a suitable file by hand, for example a blank map of Spain with the Valencian Community highlighted. No se encontró una imagen adecuada para esta pregunta.
- **q-14252** (drinks) Completa la expresión de cuando estás hecho un lío: «Tengo un cacao…» → …mental: The fun fact's etymology («cacao mental» comes from comparing mixed-up ideas to cocoa powder stirred into milk) is unsourced, and the fact check says it is uncertain. I can't confirm it either. Replace it with a fact you can check, for example that in colloquial Spain Spanish «cacao» on its own means «lío, jaleo» (RAE, marked coloquial, España). Verificación de datos: uncertain. «Cacao mental» is a real expression, but the fun fact's etymology (ideas mixed like cocoa powder stirred in milk) is unsourced and likely invented. The wrong answers also weren't checked against any source.
- **q-14274** (legends-and-superstitions) Mira el cuadro «El aquelarre», de Goya: las brujas rodean a un macho cabrío. ¿Cuántos cuernos tiene? → 2: The essential image is Goya's 1798 «El aquelarre», which shows a witch offering an emaciated infant to the devil-goat and a dead baby's body in the lower left. Shown sharp to 6-year-olds at difficulty 1, that breaks the house rule "nothing scary, gory or adult-only". Hint 2 («los mismos que una vaca») also gives the answer away. A goat-horn counting question would need a different, child-friendly image, so this makes it a different question.
- **q-14295** (painting-and-architecture) Este hombre de camisa blanca con los brazos en alto es de un famoso cuadro de Goya. ¿Quiénes están frente a él? → Soldados franceses: No candidate fits the essential slot. The note asks for a crop of the man in the white shirt without the soldiers or blood. Candidates 1 and 3 are the whole «El 3 de mayo de 1808» painting, which shows the firing squad and bloody bodies in the foreground. The other candidates are different paintings, and no new search is allowed. A crop of the man needs to be uploaded or made by hand. Another option is to change the media to an illustrative image, such as the Puerta del Sol or the Príncipe Pío hill. No se encontró una imagen adecuada para esta pregunta.
- **q-14323** (regional-dishes) Mira este plato de cerca: arroz blanco, huevo frito, tomate frito y plátano frito. Su nombre en España hace referencia a un país. ¿Cuál? → Cuba: None of the candidates shows arroz a la cubana, and no new search is allowed. The essential image needs a clear photo of white rice with a fried egg, tomato sauce and fried plantain or banana. Possible search terms: "arroz a la cubana" or "Cuban-style rice". Also, hint 2 (Spanish colony until 1898) fits Filipinas too, so it doesn't narrow the options; a revision could change it. No se encontró una imagen adecuada para esta pregunta.
- **q-14325** (regional-speech) Soy elástica y redonda, espero en tu muñeca hasta que me necesitas y en los noventa me forraron de tela. Sujeto coletas. ¿Qué soy? → La goma del pelo: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-14369** (monuments) Mira la Alcazaba de Málaga: al levantarla en el siglo XI se usaron piedras y columnas de un edificio más antiguo que está a sus pies. ¿Cuál? → Un teatro romano: All four image candidates show the Alhambra in Granada, not the Alcazaba of Málaga, which the question names with «Mira la Alcazaba de Málaga». No new search is allowed. The slot needs a new search for the Alcazaba of Málaga, framed without the Roman theatre below it, for example 'Alcazaba Malaga courtyard' or 'Alcazaba Malaga gardens'. No se encontró una imagen adecuada para esta pregunta.
- **q-14373** (pop-and-rock) Joaquín Sabina, de Úbeda, casi siempre sale al escenario con un sombrero negro, duro y de copa baja y abombada. ¿Cuál es? → Un bombín: The question text describes the hat as «de copa baja y abombada»: «abombada» echoes «bombín» in sound and root, so players can match it to the answer by the word alone. Hint 3 makes the same link («bombo» pequeño), so the question text already gives away what was meant to be the strongest hint. Replace «abombada» with a word that doesn't echo the name, such as «redondeada». At the same time, soften «casi siempre» to «suele salir», as the fact check suggests. Verificación de datos: uncertain. The bombín is his most-cited hat, but he also wears panama and white hats. 'Casi siempre' is a slight overstatement.
- **q-14386** (radio-and-internet) Esta cadena de radio nació en 1990 de la mano de la ONCE, hoy es de Atresmedia y emite el programa «Más de uno». ¿Cuál es? → Onda Cero: Hint 2 gives the answer away. It describes "onda" (the form radio signals take through the air), and Onda Cero is the only option whose name starts with that word, so the answer is solved before hint 3. Hint 2 needs replacing with a clue that doesn't spell out part of the name, for example the station's founding in 1990 or its link to the ONCE told another way. Also, hint 1 (Carlos Alsina) only names the host of «Más de uno», which the question already mentions.
- **q-14422** (sayings) Te pones «como un tomate» cuando te da vergüenza. Pero ¿de qué continente llegó el tomate a España? → De América: This asks the same fact as the approved q-3479 ("tomatoes only reached Italy in the 1500s. Where did they come from?" → the Americas). Players in Spain get both, so one gives the other away. Changing Italy to Spain and adding the «como un tomate» saying doesn't make it a different question.
- **q-14427** (school-and-home) Mira este detalle de una casa española. ¿Dónde suele estar puesto? → En la ventana: No candidate shows the essential image, a Spanish roller shutter (persiana enrollable) with horizontal slats. Candidate 1 is a vertical slat blind, and 2–6 are roll-top desks. No new search is allowed, so the media slot can't be filled. A better query would be "roller shutter window Spain" or "persiana enrollable ventana". No se encontró una imagen adecuada para esta pregunta.
- **q-14459** (transition-and-democracy) La heredera al trono de España es princesa de una tierra con sidra, los Picos de Europa y Covadonga. ¿Cuál? → Asturias: Overlaps the approved q-10027 (same subcategory). Its text says the heir to the Spanish throne is called «princesa de Asturias», which is exactly what this question asks. Anyone who has seen q-10027 knows this answer straight away. Drop this draft, or reword q-10027 so it no longer names the title.
- **q-14471** (transport) Vas por la autovía y ves un cartel: «Tramo controlado por radar». ¿Qué mide ese radar? → La velocidad media entre dos puntos: On Spanish roads, the sign «Tramo controlado por radar» is the usual warning before ordinary fixed radars, which measure your speed at one point. It doesn't mean average-speed section control. Section-control signs say something like «Control de velocidad media» or «radar de tramo». So the answer, hint 2, hint 3 and the fun fact describe the wrong kind of radar for the sign that's quoted. Quote a real section-control sign (e.g. «Control de velocidad media») or ask directly about the «radar de tramo».
- **q-14476** (transport) ¿Qué significa esta señal de tráfico? → Ceda el paso: No usable essential image: candidate 1 is the R-1 sign but the 'CEDA EL PASO' variant with the answer written inside the triangle; candidates 2 and 3 are street scenes not showing the sign. Needs a new search for the plain Spanish R-1 sign without text (e.g. 'Spain traffic signal r1.svg' or 'yield sign triangle'). No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 5, cause_effect 11, count 9, estimate 5, identify 49, made_of 10, name_concept 21, odd_one_out 13, origin 27, purpose 16, record 9, sequence 16, when 32, who 25, word_meaning 23
- stimulus: detail 12, map_outline 3, none 214, photo 42
- clue: completion 6, direct 136, riddle 25, scenario 36, three_facts 68
- answer_kind: group 33, number 16, person 47, place 46, thing 46, time 32, word 51
- lens: body_senses 12, educational_media 27, everyday 27, history 62, language 42, nature 11, pop_culture 43, school 26, university 21

## Dropped by the pipeline

- al-andalus-and-reconquista-0: overlap like q-0816: Nací en Pisa hacia 1170, en mi libro 'Liber Abaci' ayudé a que Europa usara los números arábigos y planteé un famoso problema sobre parejas de conejos. ¿Quién soy? → Fibonacci: Nacieron en la India, los mejoraron sabios musulmanes y entraron en Europa por al-Ándalus. ¿Cómo llamamos por eso a nuestros números? → Números arábigos
- al-andalus-and-reconquista-4: overlap like q-0333: Muchas palabras del español que empiezan por 'al-', como 'almohada', 'alfombra' y 'algodón', vienen de un mismo idioma. ¿De cuál? → Árabe: Apoyas la cabeza en la almohada para dormir. ¿Quiénes nos dejaron esa palabra? → Los árabes
- bourbons-and-19th-century-0: overlap like q-11263: Esta comunidad celebra su día cada 2 de mayo, en recuerdo del levantamiento de 1808 contra las tropas francesas. ¿Cuál es? → Comunidad de Madrid: Un festivo de la Comunidad de Madrid, una plaza de Malasaña y un cuadro de Goya recuerdan el mismo levantamiento contra los franceses. ¿Cuál? → El Dos de Mayo
- bourbons-and-19th-century-6: overlap like q-8029: En 1808 mis tropas entraron en España y dejé al rey Fernando VII sin trono. Sin rey, en la Nueva Granada nacieron juntas de gobierno. ¿Quién soy? → Napoleón Bonaparte: «Me coroné emperador de Francia, nombré rey de España a mi hermano José y perdí mi última batalla en Waterloo». ¿Quién soy? → Napoleón Bonaparte
- bourbons-and-19th-century-7: overlap like q-9850: Mira este detalle. Su nombre árabe era «el monte de Tariq», por el general que desembarcó aquí en el año 711. ¿Qué es? → El Peñón de Gibraltar: Es un peñón del sur de Andalucía, tiene monos en libertad y pertenece al Reino Unido desde el Tratado de Utrecht de 1713. ¿Qué es? → Gibraltar
- childrens-tv-1: overlap like q-1374: Soy un canario amarillo y vivo en una jaula. Siempre digo «me pareció ver un lindo gatito». ¿Qué gato me persigue? → Silvestre: Es un canario amarillo de Looney Tunes, con una cabeza enorme, y el gato Silvestre siempre intenta atraparlo. ¿Cómo se llama en España? → Piolín
- co-official-languages-1: overlap like q-9893: Mira este mapa de España. ¿Qué mar baña la costa del este, la de Barcelona, Valencia y las islas Baleares? → El mar Mediterráneo: Un cartel en la arena dice «platja», el socorrista te dice «bon dia» y en el chiringuito sirven «pa amb tomàquet». ¿Qué mar tienes delante? → El mar Mediterráneo
- drinks-4: overlap like q-10011: La sidra es la bebida más famosa de Asturias y se sirve echándola desde muy alto. ¿De qué fruta se hace? → De la manzana: De ruta por España: Sant Sadurní d'Anoia es al cava como Villaviciosa, en Asturias, es a… → La sidra
- drinks-13: overlap like q-5044: Se le echa agua y café molido, se pone a hervir o se enchufa, y de ella sale el tinto de la mañana. ¿Qué es? → La cafetera: En muchas casas se le llama «la italiana»: es de metal, se enrosca por la mitad, va al fuego y borbotea al terminar. ¿Qué es? → Una cafetera
- empire-11: overlap like q-13391: Mira este escudo de España. ¿Qué antiguo reino representa la pieza roja con hojas verdes que hay en la parte de abajo? → El Reino de Granada: Fernando el Católico añadió esta fruta a su escudo al conquistar una ciudad en 1492. ¿Qué ciudad? → Granada
- empire-17: overlap like q-0101: ¿Cómo se llamaban los tres barcos de Colón? → La Niña, la Pinta y la Santa María: Completa los nombres de los barcos de Colón: la Pinta, la Niña y la… → Santa María
- monuments-1: overlap like q-2238: Who designed this colorful park in Barcelona? → Antoni Gaudí: Mira este tejado con escamas de colores, como el lomo de un dragón, en el paseo de Gracia de Barcelona. ¿Quién lo diseñó? → Antoni Gaudí
- monuments-9: overlap like q-10039: Soy una diosa, voy en un carro tirado por dos leones y los aficionados del Real Madrid se suben a mi fuente a celebrar títulos. ¿Quién soy? → Cibeles: «Estoy en Madrid, en un carro con forma de concha tirado por caballos marinos, y los aficionados del Atlético vienen a celebrar sus títulos conmigo.» ¿Quién soy? → Neptuno
- monuments-13: overlap like q-0695: Mira la foto: este marisco, que en Japón se llama 'hotate' y se come en sushi, ¿cómo se llama en español? → Vieira: Muchos peregrinos del Camino de Santiago llevan esta concha colgada de la mochila. ¿De qué marisco es? → De vieira
- monuments-15: overlap like q-2489: Which of these famous players never played for AC Milan? → Lionel Messi: ¿Cuál de estos futbolistas NUNCA ha jugado en el Real Madrid, el equipo del estadio Santiago Bernabéu? → Lionel Messi
- monuments-17: overlap like q-6118: What is the name of the summer palace and gardens that the Nasrid sultans built on the hill beside the Alhambra? → Generalife: Este patio alargado, con una acequia, surtidores y jardines, está en Granada. ¿En qué conjunto se encuentra? → El Generalife
- painting-and-architecture-5: overlap like q-5349: The daisy-shaped Chupa Chups lollipop logo was designed in 1969 by a famous Spanish painter. Who? → Salvador Dalí: Fui pintor surrealista y en 1969 dibujé en menos de una hora una margarita amarilla para el envoltorio de un famoso caramelo catalán con palo. ¿Quién soy? → Salvador Dalí
- pop-and-rock-8: overlap like q-12259: Este cantante de Linares representó a España en Eurovisión en 1966 y 1967 y triunfó con «Mi gran noche». ¿Quién es? → Raphael: En las fiestas todos cantan «¿Qué pasará? ¿Qué misterio habrá? Puede ser mi gran noche». ¿Quién la cantó por primera vez, en 1967? → Raphael
- pop-and-rock-12: overlap like q-9843: En 1968, el cantante elegido quiso cantar en catalán, lo sustituyó a última hora Massiel y ella ganó en Londres. ¿Qué ganó? → El Festival de Eurovisión: Soy de Barcelona, en 1968 iba a ir a Eurovisión pero quise cantar en catalán y me cambiaron por Massiel, y en 1971 le canté al «Mediterráneo». ¿Quién soy? → Joan Manuel Serrat
- protected-areas-12: overlap like q-10103: Hacia 2002 quedaban menos de 100 en libertad, vive en Doñana y Sierra Morena y come sobre todo conejos. ¿Qué felino llegó a ser el más amenazado del mundo? → El lince ibérico: En 2002 quedaban menos de 100 linces ibéricos. Tras años de cría en cautividad y sueltas en el campo, ¿qué logró la especie en 2024? → Pasar de «en peligro» a «vulnerable»
- protected-areas-17: overlap like q-10105: Este es el Gran Telescopio Canarias, del Instituto de Astrofísica de Canarias. ¿En qué isla está? → La Palma: Estás en el Roque de los Muchachos, con uno de los mejores cielos del mundo para ver estrellas, protegido por la «Ley del Cielo» de 1988. ¿En qué isla? → La Palma
- radio-and-internet-5: overlap like q-11324: TheGrefg presentó su propia skin de Fortnite ante casi 2,5 millones de personas a la vez, récord de Twitch entonces. ¿En qué año? → 2021: Soy morada, en mí Ibai y TheGrefg hacen sus directos y miles de personas escriben a la vez en mi chat. ¿Qué soy? → Twitch
- regional-dishes-2: overlap like q-12455: Mira la pezuña de este jamón. ¿De qué animal suele ser el jamón que la tiene así? → Del cerdo ibérico: El jamón serrano es la pata curada de un animal. ¿De cuál? → Del cerdo
- regional-dishes-5: overlap like q-10339: Estas empanadas de las costas de Sinaloa y Nayarit van rellenas de camarón. ¿A qué grupo de animales pertenece el camarón? → Crustáceos: Se sirven chisporroteando en una cazuelita de barro, con aceite, mucho ajo y guindilla. ¿A qué grupo de animales pertenece su ingrediente principal? → Crustáceos
- regional-dishes-7: overlap like q-13302: Mira la foto: este fruto cae de las encinas en las dehesas. ¿Para qué es famoso en España? → Para engordar cerdos: Los mejores jamones ibéricos son de cerdos que engordan comiendo el fruto de la encina. Manzano es a manzana como encina es a… → Bellota
- regional-dishes-9: overlap like q-6059: Look at this bowl of soup. Which vegetable gives it its bright red color? → Tomato: Mira esta sopa fría típica del verano en España. ¿Qué hortaliza le da su color rojo? → El tomate
- regional-speech-15: overlap like q-11446: Sale después de un golpe, se levanta en la cabeza y el Chapulín Colorado le puso su nombre a su martillo. ¿Qué es un «chipote»? → Un chichón: En los tebeos de Mortadelo y Filemón, tras cada porrazo, a alguien le sale un «chichón». ¿Qué es? → Un bulto por el golpe
- regional-symbols-7: overlap like q-9890: Mira este acueducto de Segovia. ¿Qué pueblo lo construyó? → Los romanos: Lo hicieron los romanos para llevar agua, tiene más de 160 arcos de granito y es la figura del escudo de su ciudad. ¿Qué monumento es? → El acueducto de Segovia
- regional-symbols-10: overlap like q-14336: Las cuatro cabezas de moro del escudo de Aragón recuerdan la batalla de Alcoraz de 1096. Según la leyenda, ¿qué santo ayudó a los cristianos? → San Jorge: Este es el escudo de Barcelona. ¿De qué santo es la cruz roja sobre fondo blanco? → San Jorge
- regional-symbols-12: overlap like empire-11: Fernando el Católico añadió esta fruta a su escudo al conquistar una ciudad en 1492. ¿Qué ciudad? → Granada: Miras el escudo de España y, abajo del todo, ves una granada abierta. ¿Quiénes la añadieron tras conquistar Granada? → Los Reyes Católicos
- regions-and-provinces-1: duplicate like q-0329: ¿En qué mes del año se celebra la Feria de las Flores de Medellín? → Agosto: ¿En qué mes se celebra cada año la Tomatina de Buñol? → Agosto
- regions-and-provinces-4: overlap like q-14248: Mira el mapa: en esta comunidad, cada marzo, se plantan y se queman «les Falles». ¿Cuál es? → La Comunidad Valenciana: ¿Qué comunidad autónoma está marcada en este mapa? → Comunidad Valenciana
- regions-and-provinces-10: duplicate like q-10130: ¿De qué comunidad autónoma es esta bandera? → Andalucía: ¿Qué comunidad autónoma está marcada en este mapa? → Andalucía
- regions-and-provinces-13: duplicate like q-13414: Este volcán, con un lado cortado por una antigua cantera, entró en erupción hace más de 10 000 años. ¿En qué comunidad está? → Cataluña: Mira este templo, que lleva más de 140 años en obras. ¿En qué comunidad autónoma está? → Cataluña
- al-andalus-and-reconquista-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es una palabra árabe, da nombre a la plaza de Zocodover en Toledo y en Fez sigue habiendo muchos. ¿Qué es un zoco? → Un mercado
- flamenco-and-copla-7: overlap like q-11162: ¿En qué año publicó Rosalía su disco «Motomami»? → 2022: ¿Qué disco publicó Rosalía justo después de «El mal querer»? → Motomami
- flamenco-and-copla-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Los fontaneros la enrollan en las roscas de las tuberías y da nombre a un dúo de Cornellà. ¿Qué es la estopa? → Una fibra basta de lino o cáñamo
- money-and-services-0: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 5: Cada mes salgo de tu bolsillo, pero por mucho que me pagues, el piso nunca será tuyo. ¿Qué soy? → El alquiler
- monuments-7: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Es de ladrillo rojo y estilo neomudéjar, abrió en 1931 y es la plaza de toros con más aforo de España. ¿Cuál es? → Las Ventas
- protected-areas-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Cómo se llama la reserva marina junto a La Restinga, al sur de la isla más occidental de España? → Mar de las Calmas
- radio-and-internet-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En el chat de un directo de Twitch, esta persona lleva una espadita verde junto a su nombre. ¿Quién es? → El moderador
- radio-and-internet-7: fact-check wrong: The fun fact says 'la pareja de Perú' won. The 2021 tournament was individual (32 players). The winner was one Peruvian player, Francesco de la Cruz, who beat Jan Spieß of Germany 6-2 in the final.: Ibai Llanos y Gerard Piqué organizaron en 2021 el «Mundial de Globos», emitido en Twitch. ¿Cuál era el objetivo del juego? → Que el globo no tocara el suelo
- regional-dishes-17: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 4: Mira esta salsa. ¿Cuál es? → La mayonesa
- regional-speech-10: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En el Madrid castizo de los siglos XVIII y XIX se hablaba de «majos» y «manolas». ¿Qué era una manola? → Una moza castiza de barrio
- sayings-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En la Castilla medieval, ¿qué era la «blanca» de la expresión «estar sin blanca»? → Una moneda
- spanish-cinema-10: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: La novela de Moccia que en España llegó al cine como «Tengo ganas de ti» me puso de moda en un puente de Roma. Las parejas me cuelgan con sus nombres. ¿Qué soy? → Un candado
- sportspeople-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Garbiñe Muguruza ganó las finales de Roland Garros 2016 y Wimbledon 2017, y en cada una venció a una hermana de la misma familia. ¿Qué familia? → Las hermanas Williams
- sportspeople-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Samuel Sánchez ganó el oro olímpico en ciclismo en ruta el día después de la inauguración de los Juegos. ¿En qué año? → 2008
- team-and-traditional-sports-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Quiénes compiten en la Copa Davis de tenis? → Selecciones de países
- transition-and-democracy-14: overlap like q-11309: La Constitución española me fija en los 18 años. ¿Qué soy? → La mayoría de edad: En noviembre de 1978, poco antes de votar la Constitución, España bajó la mayoría de edad. ¿Quién pudo votar por primera vez? → Los jóvenes de 18 a 20 años
- transport-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Cómo se llama el billete de tren que sirve para ir a un sitio y volver después al punto de salida? → Billete de ida y vuelta
- tv-series-10: overlap like q-12485: Este actor fue Antonio Alcántara en «Cuéntame cómo pasó». ¿Cómo se llama? → Imanol Arias: Si en 1989 veías «Brigada Central» en TVE, ¿qué actor era el inspector gitano Manuel Flores? → Imanol Arias
- sayings-17: overlap like q-0120: ¿Cómo se llama la figura literaria que exagera, como en 'te lo he dicho un millón de veces'? → Hipérbole: Completa esta queja de toda la vida: «¡Te lo he dicho … veces!» → Mil
- school-and-home-3: overlap like q-6910: Sobresale del segundo piso de las casas coloniales, en Cartagena suele ser de madera y estar lleno de flores, y desde ahí se veían las procesiones. ¿Qué es? → El balcón: Mira este detalle de una fachada de un pueblo andaluz. ¿Qué parte de la casa es? → Un balcón
- school-and-home-12: overlap like q-12471: Preparas la merienda: sándwich es a pan de molde como bocadillo es a… → Barra de pan: En España, ¿cómo se llama la pieza de pan larga y crujiente que se compra cada día en la panadería? → La barra
- sportspeople-16: overlap like q-12479: Mira la foto: Marc Gasol y Serge Ibaka ganaron en 2019 el anillo de la NBA con el equipo de esta ciudad. ¿Cuál es? → Toronto: Nací en Barcelona en 1985, fui Mejor Defensor de la NBA en 2013 y en 2019 gané el anillo con los Toronto Raptors. Mi hermano mayor también fue campeón de la NBA. ¿Quién soy? → Marc Gasol
- team-and-traditional-sports-17: overlap like q-11381: Soy piloto de motos, nací en Cervera y me llaman «la Hormiga». En las curvas me tumbo tanto que rozo el asfalto con el codo. ¿Quién soy? → Marc Márquez: ¿Qué piloto español ha ganado más Mundiales en MotoGP, la categoría reina de las motos? → Marc Márquez
- transition-and-democracy-1: overlap like q-14303: Suena en una fiesta «Devuélveme a mi chica», de Hombres G, y todo el mundo la canta. ¿De qué ciudad era el grupo? → Madrid: Es un grupo madrileño nacido en los 80, su nombre viene de una película de gánsteres y cantó «Devuélveme a mi chica». ¿Cuál es? → Hombres G
- transport-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En esta calle solo se puede ir andando: los coches no pueden entrar. ¿Cómo se llama una calle así? → Calle peatonal
- tv-shows-and-presenters-4: overlap like q-10035: Estás ante la tele en Nochevieja y, antes de las doce campanadas, suenan los cuartos. ¿Cuántos son? → 4: En Nochevieja, en la tele, primero suenan los cuartos y después las campanadas. ¿Cuántas campanadas hay? → 12
- tv-shows-and-presenters-9: overlap like q-1426: Estás viendo Eurovisión y un país anuncia «douze points» para una canción. ¿Cuántos puntos le está dando? → 12: En las votaciones de Eurovisión, cada país reparte 1, 2, 3… hasta 8 y luego 10. ¿Cuántos puntos da a su favorita? → 12
- tv-shows-and-presenters-13: overlap like q-13281: Antes de «La Revuelta» en La 1, David Broncano presentaba un late night en Movistar Plus+. ¿Cómo se llamaba? → «La Resistencia»: Nací en La 1 en 2024; mi presentador llegó desde Movistar Plus+ con Grison y Ricardo Castella, y me hago en un teatro. ¿Qué programa soy? → «La Revuelta»
