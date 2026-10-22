# batch-12

Made by `qgen batch` on 2026-10-21 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): 19th-century, scientists-and-inventors, pioneers-and-popular-figures, street-food-and-bakery, indigenous-myths-and-folk-beliefs, vallenato, popular-and-andean-music, telenovelas, tv-shows-and-series, hosts-actors-and-comedians, cinema, banknotes-and-coins, brands-and-products, drinks, crafts-and-traditional-dress, writers-and-books, places-and-monuments, 20th-century, traditional-games, painters-sculptors-and-museums, pre-columbian-cultures, symbols-of-departments-and-cities, pop-rock-and-urban-music, transport, languages, poetry-and-childrens-stories, sayings-and-expressions
- Merged: 253 (q-5008…q-5260)
- Approved: 239
- Needs work: 14
- Dropped by the pipeline: 85
- Reviewed by: claude-opus-5-5
- Claude calls: 559, about $69.26 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-10, batch-11; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ stops the next `qgen batch` until `qgen health ack` (D-55). Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-10 | batch-11 | batch-12 |
|---|---|---:|---:|---:|
| source locale |  | en | en | es |
| drafts |  | 1177 | 1157 | 338 |
| skipped slots |  | 604 | 625 | 148 |
| dropped |  | 237 | 244 | 85 |
| drop rate | ≤ 20.0 % | 20.1 % ✗ | 21.1 % ✗ | 25.1 % ✗ |
| dropped: hard fail correct |  | 1 | 2 | 6 |
| dropped: hard fail unambiguous |  | 5 | 0 | 6 |
| dropped: hard fail no_giveaway |  | 66 | 79 | 27 |
| dropped: overlap |  | 154 | 140 | 47 |
| dropped: duplicate |  | 14 | 22 | 0 |
| dropped: fact-check wrong |  | 2 | 1 | 4 |
| merged |  | 940 | 913 | 253 |
| approved |  | 866 | 836 | 239 |
| needs_work |  | 74 | 77 | 14 |
| needs_work rate | ≤ 20.0 % | 7.9 % ✓ | 8.4 % ✓ | 5.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.5 % ✓ | 1.3 % ✓ | 0.4 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.8 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.4 % ✓ | 0.1 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.8 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.3 % ✓ | 6.1 % ✓ | 3.6 % ✓ |
| media: no pick in review 1 |  | 114 | 142 | 43 |
| media: recovered by research |  | 84 | 98 | 36 |
| media: no pick at record |  | 32 | 45 | 7 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 1.4 % ✓ | 0.9 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 14.9 % ✓ | 14.5 % ✓ | 14.5 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 62.1 % ✓ | 59.0 % ✓ | 48.6 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.23 ✓ | 1.08 ✓ | 0.44 ✓ |
| approved 11–15 |  | 168 | 148 | 48 |
| top move | ≤ 25.0 % | 13.3 % ✓ | 14.0 % ✓ | 17.8 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 75.0 % | 76.6 % | 86.6 % |
| values stimulus |  | 7 | 7 | 4 |
| top clue | ≤ 60.0 % | 51.4 % ✓ | 47.1 % ✓ | 32.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.3 % ✓ | 23.8 % ✓ | 28.1 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 14.4 % ✓ | 15.4 % ✓ | 28.5 % ✗ |
| values lens |  | 12 | 12 | 11 |
| media share | 15.0 %–50.0 % | 25.0 % ✓ | 23.4 % ✓ | 13.4 % ✗ |
| mean fun | ≥ 3.40 | 3.56 ✓ | 3.50 ✓ | 3.40 ✗ |
| cost $ |  | $209.21 | $228.74 | $66.34 |
| $ per approved | ≤ $0.35 | $0.24 ✓ | $0.27 ✓ | $0.28 ✓ |
| calls |  | 1754 | 1832 | 499 |
| calls per approved |  | 2.03 | 2.19 | 2.09 |
| wall time h |  | 5.13 | 4.95 | 2.36 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail, acked | ✗ fail, acked | ✗ fail |

Deficit to the targets (base, approved now): 1: 63, 2: 13, 3: 84, 4: 63, 5: 45, 6: 0, 7: 24, 8: 36, 9: 2, 10: 0, 11: 27, 12: 0, 13: 0, 14: 0, 15: 58

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 5 of 57 (9 %)
- Major among review needs work: 1 of 3 (33 %)
- Problems by kind: giveaway 9 (1 major), fact 3 (3 major), ambiguity 1 (1 major), overlap 1 (1 major), media 5 (3 major), difficulty 2 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 53 of 60 (88 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.92

Major findings on approved questions:

- **q-5029**: fact — Hint 1 says "Soy bogotano", but biographies (Wikipedia-derived profiles such as onesheet.org) say Felipe Aljure was born in Girardot, Cundinamarca. So the hint teaches players a wrong fact. The other facts check out: he directed La gente de La Universal (usually dated 1993, though Wikipedia gives 1991) and El Colombian Dream (2006), and the three wrong answers are other Colombian directors. (http://127.0.0.1:8001/review/q-5029)
- **q-5068**: fact, media — The question text says she was born in Palenquito, but Petrona Martínez was born in San Cayetano (San Juan Nepomuceno, Bolívar) and moved to Palenquito as a child (Wikipedia, Colombia Reports). Rewording to 'vivo/crecí en Palenquito' fixes it. Minor: the image shows San Basilio de Palenque, a different village, which may point towards Graciela Salgado; the nickname and Latin Grammy hints check out. (http://127.0.0.1:8001/review/q-5068)
- **q-5070**: fact, ambiguity, media — The question is factually wrong. Fernando González Pacheco hosted 'Animalandia' for about 15 years, and he is one of the wrong answers. Jota Mario only joked about trying to break his TV "pa' meterme a Animalandia con Pacheco" (El Universal; Pacheco's Wikipedia page). So the first clue points to a wrong option, and players who know the show would pick Pacheco. The 'Muy buenos días' part on RCN is correct. Smaller points: the media file is a Swedish singer on Chicago TV in 1959, which has nothing to do with the question. The difficulty is also low for a host from 1990s and 2000s TV, since young teens hardly know him. (http://127.0.0.1:8001/review/q-5070)
- **q-5079**: media — The illustrative image is "File:Guatapé 29.jpg". Its title names the answer, and the photo itself is shown sharp. If it shows Guatapé's famous colourful streets or El Peñol rock, Colombian families can recognise the place from the picture alone. The facts check out: the zócalos, the Peñol-Guatapé reservoir, the rock climbed by stairs and the roughly two-hour drive from Medellín are all correct. The three wrong options don't fit the clue, and none of the related questions overlap. (http://127.0.0.1:8001/review/q-5079)
- **q-5106**: giveaway, difficulty — The description ("Una cartera que piensa") already says the object is a bag. That rules out all three wrong answers (ruana, sombrero vueltiao, hamaca). Hint 1 ("Sirve para cargar cosas") narrows it the same way. The question text adds "cruzada al pecho", which also only fits a bag, so this is easier than 6 for Colombian players (about 4). The facts (Arhuaco women weave the mochila with sheep wool, men wear it crossed over the chest) are correct. (http://127.0.0.1:8001/review/q-5106)

## Needs work

- **q-5008** (19th-century) Estás viendo las miles de láminas de flores pintadas a mano por la Real Expedición Botánica. ¿Quién dirigió esa expedición? → José Celestino Mutis: None of the media candidates shows what the question names. All six are black-and-white lithographs from 19th-century US expedition reports (Bigelow/Torrey, Stansbury, Sitgreaves), not the hand-painted colour plates of the Real Expedición Botánica. A new search can't be run, so the slot needs a real Mutis expedition plate, for example a search for "Flora de la Real Expedición Botánica" or "Mutis lámina quina" on Commons. No se encontró una imagen adecuada para esta pregunta.
- **q-5020** (20th-century) Este teatro bogotano, fundado en 1966, fue el gran laboratorio de la creación colectiva. ¿Quién fue su fundador y director? → Santiago García: The text is fine and the facts check out (Santiago García co-founded La Candelaria in 1966, studied architecture, and led it with Patricia Ariza). But "Este teatro bogotano" points to the Teatro La Candelaria building, and none of the six candidates shows it. They show the Camarín del Carmen, the Iglesia/Templo de la Candelaria and ordinary houses in the La Candelaria neighbourhood. A new search isn't allowed. Find a photo of the theatre's facade (Calle 12 No. 2-59), or change the slot to decorative with a Bogotá colonial-street image. No se encontró una imagen adecuada para esta pregunta.
- **q-5041** (crafts-and-traditional-dress) Mira la foto: estas máscaras de madera tallada, de toritos y tigres, se usan en un carnaval famoso. ¿De qué ciudad? → Barranquilla: The essential image must show the carved torito/tiger masks of the Barranquilla Carnival, but every candidate shows Portuguese (Lazarim caretos, a Diabo mask) or German Fastnacht masks. A photo of Barranquilla's masks is needed, or the question must drop "Mira la foto" and use an illustrative image. No se encontró una imagen adecuada para esta pregunta.
- **q-5046** (drinks) Esta bebida cremosa es la estrella de las playas de Cartagena. Además de limón, ¿de qué fruta lleva? → Coco: No candidate shows a coconut lemonade: the sheet has Ter Borch paintings (1, 5, 6), empty engraved glasses from the MET (2, 3) and a gilded vase (4). No new search is allowed. As the rater suggested, switch the slot to an illustrative image, such as a Cartagena beach or a coastal fruit stand, because the question works without a photo of the drink. No se encontró una imagen adecuada para esta pregunta.
- **q-5098** (pop-rock-and-urban-music) Somos dos hermanos del Valle del Cauca: pegamos «Yo te esperaré» y luego «Por fin te encontré» con Juan Magán. ¿Quiénes somos? → Cali y El Dandee: The question says the duo is from Valle del Cauca, and the capital of Valle del Cauca is Cali, which is part of the answer's name ("Cali y El Dandee"). A Colombian family can get the answer from the geography without knowing the songs, and hint 3 then repeats the same clue. Replace "del Valle del Cauca" with something that doesn't point to the name, such as "colombianos", or drop it.
- **q-5113** (19th-century) Completa: 'En 1851, bajo el gobierno de José Hilario López, se aprobó la ley que abolió la…' → Esclavitud: No candidate works. #1 (López's tomb plaque) has 'Libertador de los esclavos' written on it, which gives the answer away. #2–#6 (a ceiba seedling, a market hall, a military group photo, a church tower, a singer mural) are only linked to López through their file titles. A new search is needed, e.g. a portrait of José Hilario López or the 1851 law document, and it must have no visible text naming slavery. No se encontró una imagen adecuada para esta pregunta.
- **q-5129** (traditional-games) En el parqués, ¿cuántas fichas tiene cada jugador al empezar? → 4: This asks the same fact as approved q-3205 ("This board is for Ludo, also called Parcheesi. How many tokens does each player get?" → 4). Parqués is the Colombian form of parchís/Parcheesi, so the token count is the same fact in other words. Drop it, or ask about something only parqués has, such as the 'seguros', capturing pieces or 'soplar'.
- **q-5158** (indigenous-myths-and-folk-beliefs) Es un espanto antioqueño, anda por minas abandonadas y deja un rastro que seca las matas. ¿Qué significa su nombre, Patetarro? → Que tiene un tarro en lugar de pierna: Verificación de datos: uncertain. I could not verify the details. A source confirms the Patetarro exists in Antioquian folklore, but it says he throws worms at crops out of revenge. I found nothing on the tarro-for-a-leg story, the abandoned mines, or the trail that dries plants.
- **q-5159** (indigenous-myths-and-folk-beliefs) Según la leyenda, ¿a quiénes castiga el Hojarasquín del Monte? → A los que dañan el bosque y sus animales: The fun fact (the Hojarasquín helps lost walkers find their way) is unverified by the fact check, and I can't confirm it either. Replace it with a supported fact, e.g. that peasants describe him as a tree-like man seen as the conscience of nature. Verificación de datos: uncertain. The answer is supported: the legend says he punishes those who harm the forest and its animals. I found nothing saying he helps lost walkers find their way, so the fun fact is unverified.
- **q-5175** (poetry-and-childrens-stories) En un cuento en verso de Rafael Pombo, un gatico se escapa de su casa para volverse bandido. ¿Cómo se llama? → Michín: None of the candidates shows Rafael Pombo or anything from his world. They are Solana's paintings of the Café de Pombo in Madrid, portraits of other people named Pombo (Carlos Amaya Pombo, Álvaro Pombo, Luis E. Pombo) and a pigeon. A new search isn't allowed, so the slot needs a different image, for example an engraving of Rafael Pombo, a Cuentos pintados illustration that doesn't show the cat, or a plain cat photo for a decorative slot. No se encontró una imagen adecuada para esta pregunta.
- **q-5188** (scientists-and-inventors) Cada domingo y festivo, en Bogotá pasa lo que ves en esta foto. ¿Cómo se llama? → La Ciclovía: None of the candidates shows Bogotá's Ciclovía. They are UK road-closure signs (1, 2, 3, 6) and a biscuit in resin (4, 5), and no new search is allowed. The question says "lo que ves en esta foto", so it needs an essential photo: a Bogotá street closed to cars and full of cyclists and skaters, with no "Ciclovía" signage (e.g. search "Ciclovia Bogota Sunday"). No se encontró una imagen adecuada para esta pregunta.
- **q-5192** (sayings-and-expressions) Te da pena, la cara se te calienta y todo el salón se ríe. En Colombia dicen que te pusiste como un… ¿qué? → Tomate: This asks the same fact as approved q-4547: an embarrassed person turns as red as a tomato. Calling it Colombian doesn't change it, because the expression is pan-Hispanic. Seeing one question gives away the other, so drop this draft or swap it for a different, genuinely Colombian expression.
- **q-5196** (sayings-and-expressions) En la fiesta, la pareja quiere bailar pegadito, cachete con cachete. ¿Cuál de estos ritmos NO se baila así? → Mapalé: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-5202** (scientists-and-inventors) ¿Cuál de estos nombres NO se le da al insecto que transmite el mal de Chagas? → Zancudo: La imagen elegida está dañada en la fuente (truncated (Premature end of JPEG file)).

## Question axes

- move: analogy 5, cause_effect 9, count 3, estimate 2, identify 35, made_of 8, name_concept 44, odd_one_out 10, origin 26, purpose 14, record 3, sequence 11, when 14, who 45, word_meaning 24
- stimulus: detail 7, map_outline 5, none 219, photo 22
- clue: completion 6, direct 82, riddle 47, scenario 35, three_facts 83
- answer_kind: group 16, number 8, person 68, place 22, thing 71, time 15, word 53
- lens: body_senses 4, colombia 72, educational_media 16, everyday 37, history 30, language 34, nature 13, pop_culture 18, popular_science 2, school 24, university 3

## Dropped by the pipeline

- 19th-century-12: overlap like q-2192: Me tejen a mano en Ecuador con paja toquilla, pero el mundo me conoce con un nombre que no es de Ecuador. ¿Cómo me llaman? → Sombrero panamá: Se teje con fibra fina de palma de iraca, Colombia lo exportaba por montones en el siglo XIX y en el mundo le dicen 'sombrero Panamá'. ¿Qué otro nombre tiene? → Jipijapa
- 19th-century-16: overlap like q-0111: ¿Quién escribió el cuento en verso 'El renacuajo paseador'? → Rafael Pombo: ¿Quién escribió 'El renacuajo paseador', el cuento en verso de Rin Rin Renacuajo? → Rafael Pombo
- 20th-century-8: overlap like q-0977: García Márquez es a 'Cien años de soledad' como Isabel Allende es a… → La casa de los espíritus: Estás leyendo una novela en la que la familia Buendía vive en Macondo y llueve durante años. ¿Quién la escribió? → Gabriel García Márquez
- 20th-century-12: overlap like q-0405: ¿Qué noche se celebra en Colombia el Día de las Velitas, cuando las familias prenden velas y faroles en ventanas y andenes? → La noche del 7 de diciembre: Soy una noche de diciembre: las familias prenden velas y faroles en andenes y ventanas, y conmigo empieza la Navidad. ¿Qué soy? → El Día de las Velitas
- cinema-6: overlap like q-1757: Los premios Óscar se entregaron por primera vez en 1929. ¿En qué ciudad fue esa primera ceremonia? → Los Ángeles: 'Encanto' ganó uno en 2022, la estatuilla es dorada y la ceremonia se hace en el Teatro Dolby. ¿En qué ciudad se entregan los premios Óscar? → Los Ángeles
- crafts-and-traditional-dress-4: overlap like crafts-and-traditional-dress-0: Mira de cerca: con este material los artesanos de Ráquira, Boyacá, hacen ollas y figuras. ¿Qué es? → Barro: Mira de cerca: en muchas cocinas colombianas el sancocho se cocina en esto. ¿Qué es? → Una olla de barro
- crafts-and-traditional-dress-6: overlap like q-0239: ¿En qué ciudad colombiana se celebra el Carnaval de Negros y Blancos? → Pasto: Mira la foto: en este carnaval, cada 6 de enero, todo el mundo termina blanco de talco. ¿En qué ciudad pasa? → Pasto
- drinks-9: overlap like drinks-0: Nació en 1904, embotella el agua Cristal y los jugos Hit, y su gaseosa de manzana es famosa en todo el país. ¿Qué empresa es? → Postobón: La gaseosa Colombiana, 'la nuestra', es hecha por Postobón. ¿En qué ciudad nació esa empresa? → Medellín
- indigenous-myths-and-folk-beliefs-10: overlap like q-0465: La aguapanela se hace con panela. Pero, ¿de qué se hace la panela? → Del jugo de la caña de azúcar: Tienes gripa y te dan agua de panela con limón. Miel es a abeja como panela es a… → La caña de azúcar
- indigenous-myths-and-folk-beliefs-11: overlap like q-0483: Según la leyenda, ¿a quién busca la Llorona cuando anda de noche, llorando cerca de los ríos? → A sus hijos: Salgo de noche por la orilla de ríos y quebradas, visto de blanco y mi lamento se oye a lo lejos. ¿Quién soy? → La Llorona
- indigenous-myths-and-folk-beliefs-13: overlap like q-1600: Según la tradición, ¿por qué se cuelga este objeto con las puntas hacia arriba? → Para que la suerte no se derrame: Soy de hierro, tengo forma de U, me clavan en la pata de un caballo y me cuelgan en la casa para la buena suerte. ¿Qué soy? → La herradura
- languages-7: overlap like crafts-and-traditional-dress-1: El pueblo kogui teje mochilas de colores tierra y se llama a sí mismo “hermano mayor”. ¿En qué zona montañosa vive? → Sierra Nevada de Santa Marta: Hablan damana, sus mamos son sus guías espirituales y cuidan la Línea Negra. ¿De dónde son los wiwa? → De la Sierra Nevada de Santa Marta
- painters-sculptors-and-museums-6: overlap like crafts-and-traditional-dress-1: El pueblo kogui teje mochilas de colores tierra y se llama a sí mismo “hermano mayor”. ¿En qué zona montañosa vive? → Sierra Nevada de Santa Marta: Los taironas hacían figuras de oro de hombres-murciélago, construyeron Ciudad Perdida y sus descendientes son los koguis y los arhuacos. ¿Dónde vivían? → Sierra Nevada de Santa Marta
- painters-sculptors-and-museums-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Pinto murales en Bogotá y en medio mundo, llenos de mujeres y naturaleza, y nadie conoce mi rostro. Mi nombre artístico es otra forma de decir «letra cursiva». ¿Quién soy? → Bastardilla
- painters-sculptors-and-museums-9: overlap like q-0103: ¿Qué pueblo indígena de Colombia inspiró la leyenda de El Dorado, en la laguna de Guatavita? → Los muiscas: Los muiscas hacían figuritas llamadas tunjos y su cacique se cubría el cuerpo con polvo de este metal en la laguna de Guatavita. ¿Qué metal era? → Oro
- painters-sculptors-and-museums-14: overlap like q-0496: ¿Qué futbolista es? Era un volante colombiano con una enorme melena rubia y crespa, famoso por sus pases mágicos y por jugar casi sin correr. → Carlos Valderrama: ¿A qué futbolista homenajea esta estatua gigante de bronce en Santa Marta? → Carlos «el Pibe» Valderrama
- pioneers-and-popular-figures-7: overlap like q-0484: ¿En qué prueba de atletismo ganó Caterine Ibargüen la medalla de oro en los Juegos Olímpicos de Río 2016? → Salto triple: ¿Qué atleta colombiana ganó la medalla de oro en salto triple en los Juegos Olímpicos de Río 2016? → Caterine Ibargüen
- pioneers-and-popular-figures-16: overlap like q-0343: En 'Encanto', ¿qué nieta de la abuela Alma se quedó sin don porque su puerta mágica nunca se iluminó? → Mirabel: Uso lentes redondos y una falda llena de bordados de colores. Fui la primera en ver las grietas de la Casita. ¿Quién soy? → Mirabel
- places-and-monuments-3: overlap like q-0128: Mira la foto: ¿cómo se llama este disfraz típico del Carnaval de Barranquilla? → La Marimonda: ¿En qué fiesta colombiana se usa este disfraz? → El Carnaval de Barranquilla
- places-and-monuments-14: overlap like q-0168: ¿Qué animales llegan cada año a las aguas de la isla Gorgona, en el Pacífico colombiano, para tener sus crías? → Las ballenas jorobadas: En 1527 me refugié en una isla del Pacífico llena de culebras y la llamé Gorgona, por el monstruo con serpientes en la cabeza. Luego conquisté el Imperio inca. ¿Quién soy? → Francisco Pizarro
- poetry-and-childrens-stories-13: overlap like q-0906: Adivinanza: 'Soy el manguaré, el gran tambor del pueblo bora; cuando me golpean, mi voz viaja kilómetros por la selva llevando mensajes'. ¿De qué estoy hecho? → De un tronco ahuecado: El maguaré es un gran tambor de tronco ahuecado que los uitotos tocan para comunicarse y en sus fiestas. ¿De qué región colombiana es? → La Amazonía
- pop-rock-and-urban-music-0: overlap like pioneers-and-popular-figures-1: ¿Cómo se llama esta cantante colombiana? → Karol G: A esta cantante paisa le dicen «La Bichota», y hasta llamó así a una de sus giras. ¿Quién es? → Karol G
- pop-rock-and-urban-music-6: overlap like q-0063: ¿Qué cantante colombiana cantó 'Waka Waka' para el Mundial de 2010? → Shakira: Estás en una fiesta y suena «Whenever, Wherever», con flautas andinas. ¿Qué cantante colombiana la canta? → Shakira
- pop-rock-and-urban-music-14: overlap like q-5019: Este cantante de Santa Marta mezcló el vallenato con rock y pop en los años 90. ¿Quién es? → Carlos Vives: Soy samario, revolví el vallenato con el pop y en 2016 canté «La Bicicleta» con Shakira. ¿Quién soy? → Carlos Vives
- pop-rock-and-urban-music-16: overlap like q-5071: Veo el futuro, vivo escondido entre las paredes de la Casita y mi familia prefiere no hablar de mí. ¿Quién soy? → Bruno: Es la canción de Encanto que canta toda la familia Madrigal, sobre un tío que veía el futuro y que nadie quiere nombrar. ¿Cuál es? → No se habla de Bruno
- popular-and-andean-music-13: overlap like q-5028: Nació en 1955, construyó Hidroituango y cada diciembre prende algunos de los alumbrados navideños más famosos de Colombia. ¿Qué empresa es? → EPM: Cada diciembre, millones de bombillos de colores llenan el río de esta ciudad y familias enteras salen a verlos de noche. ¿Qué ciudad colombiana es famosa por estos alumbrados? → Medellín
- pre-columbian-cultures-6: overlap like painters-sculptors-and-museums-9: Los muiscas hacían figuritas llamadas tunjos y su cacique se cubría el cuerpo con polvo de este metal en la laguna de Guatavita. ¿Qué metal era? → Oro: ¿De qué material estaban hechos casi siempre los tunjos, las figuritas de ofrenda de los muiscas? → De tumbaga, una mezcla de oro y cobre
- pre-columbian-cultures-10: overlap like q-5084: Esta pieza de oro es una de las más famosas del Museo del Oro de Bogotá. ¿Cómo se llama? → El Poporo Quimbaya: Mira de cerca esta pieza precolombina: es el símbolo de un famoso museo de Bogotá. ¿Cuál? → El Museo del Oro
- 19th-century-4: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Se hacía en salas o cafés, se repetía cada semana y en Bogotá fue famosa la del grupo El Mosaico. ¿Para qué servía una tertulia? → Para conversar de libros e ideas
- 20th-century-1: fact-check wrong: Hint 2 is false. Pacheco hosted 'Animalandia', but 'Concéntrese' was Julio E. Sánchez Vanegas's show, not his. Pacheco hosted 'Quiere cacao', which was a concentration-style game show.: Este presentador nació en España, llegó a Colombia de niño y se volvió el animador más querido de la TV. ¿Quién es? → Fernando González Pacheco
- banknotes-and-coins-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es de Bancolombia y su color es fucsia. ¿Qué es Nequi? → Una app para pagar y mandar plata
- symbols-of-departments-and-cities-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Este vaquero colombiano pasa el día a caballo arreando ganado y canta y baila joropo. ¿Cómo se le dice? → Llanero
- telenovelas-2: overlap like tv-shows-and-series-7: ¿En qué año empezó en Caracol el reality de competencias físicas 'Desafío'? → 2004: Este canal colombiano transmite «Sábados Felices» desde hace décadas, el reality «Desafío» y el programa matutino «Día a Día». ¿Cuál es? → Caracol Televisión
- traditional-games-7: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: En el parqués, cuando sacas pares, tu ficha pasa de la cárcel a una casilla de tu color. ¿Cómo se llama esa casilla? → La salida
- transport-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Bogotá lo hace desde el año 2000 un jueves de febrero, y ese día la ciudad se llena de bicis, buses y peatones. ¿Cómo se llama? → El Día sin carro
- transport-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Por su puerto en el río Magdalena llegaron inmigrantes y novedades, y allí nació la primera aerolínea del país. ¿Cómo apodan a Barranquilla? → La Puerta de Oro de Colombia
- transport-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Tengo dos ruedas y motor, y por unas monedas te llevo sentado detrás del conductor en muchos pueblos de Colombia. ¿Qué soy? → Un mototaxi
- transport-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En Colombia, ¿qué es Expreso Brasilia? → Una empresa de buses intermunicipales
- transport-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Vas muy rápido o te pasas el semáforo en rojo, y días después te llega un cobro sin que ningún agente te haya parado. ¿Cómo se llama? → Una fotomulta
- vallenato-14: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Es el estilo vallenato de los pueblos ribereños del Magdalena, como Plato y El Banco, y su gran figura es Pacho Rada. ¿Cómo se llama? → Bajero
- writers-and-books-9: overlap like q-0007: ¿Qué escritor colombiano ganó el Premio Nobel de Literatura en 1982? → Gabriel García Márquez: En esta ciudad amurallada empezó como periodista, en 1948, un famoso escritor colombiano. ¿Quién es? → Gabriel García Márquez
- banknotes-and-coins-6: fact-check wrong: "Toque, mire y gire" is the slogan of Peru's central bank (BCRP). Colombia's Banco de la República currently uses "Mire, toque, levante, gire y compruebe", so "gire" is not the third verb. An older Colombian campaign may have used a similar phrase, but I couldn't confirm it.: Para revisar si un billete es falso, el Banco de la República dice: «toque, mire y…». ¿Cuál es el tercer verbo? → Gire
- brands-and-products-1: hard fail: correct 4, unambiguous 2, no_giveaway 3, no_overlap 5: Soy un mecato crocante de maíz, de los de toda la vida en las tiendas colombianas, y muchos me piden con limón. ¿Qué soy? → Choclitos
- brands-and-products-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Colanta, la marca paisa famosa por su leche y su quesito, tiene un nombre armado con pedazos de palabras. ¿Qué significa? → Cooperativa Lechera de Antioquia
- brands-and-products-12: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Son masticables, vienen en un paquetico alargado de colores y se venden en toda tienda de barrio. ¿De qué son los sabores de las Frunas? → De frutas
- cinema-16: hard fail: correct 3, unambiguous 3, no_giveaway 4, no_overlap 5: La comedia 'Uno al año no hace daño', producida por Dago García, se estrenó como casi todas sus películas en la época que le da sentido al dicho. ¿Cuál? → Diciembre, en Navidad
- crafts-and-traditional-dress-1: overlap like painters-sculptors-and-museums-6: Los taironas hacían figuras de oro de hombres-murciélago, construyeron Ciudad Perdida y sus descendientes son los koguis y los arhuacos. ¿Dónde vivían? → Sierra Nevada de Santa Marta: El pueblo kogui teje mochilas de colores tierra y se llama a sí mismo “hermano mayor”. ¿En qué zona montañosa vive? → Sierra Nevada de Santa Marta
- drinks-0: overlap like drinks-9: La gaseosa Colombiana, 'la nuestra', es hecha por Postobón. ¿En qué ciudad nació esa empresa? → Medellín: Nació en 1904, embotella el agua Cristal y los jugos Hit, y su gaseosa de manzana es famosa en todo el país. ¿Qué empresa es? → Postobón
- drinks-7: overlap like q-5018: Es diciembre y acaba de terminar la novena de aguinaldos en la casa. ¿Qué se reparte tradicionalmente después? → Natilla y buñuelos: En Colombia, ¿para qué fiesta se reza una novena con natilla y buñuelos? → Para Navidad
- hosts-actors-and-comedians-2: fact-check wrong: Javier Fernández Franco is 'el Cantante del Gol', but he no longer works at Caracol. He left it in 2019, then worked at RCN and Win Sports, and left RCN in October 2025. The present-tense 'narrador de Caracol' and the hint that his voice is heard in Selección Colombia matches are outdated. He also had a dispute with Caracol over his catchphrases.: ¿Qué narrador de fútbol de Caracol es conocido como «el Cantante del Gol»? → Javier Fernández
- indigenous-myths-and-folk-beliefs-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Al recién nacido le amarran una faja con una moneda sobre la barriga. Según la creencia, ¿qué evita? → Que se le salga el ombligo
- indigenous-myths-and-folk-beliefs-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Según el agüero, para que el día te salga bien, ¿con qué pie te tienes que levantar de la cama? → Con el pie derecho
- indigenous-myths-and-folk-beliefs-16: fact-check wrong: Hint 1 ('Es un país donde no se habla español') doesn't point to the answer. Greece also isn't Spanish-speaking, and the US has tens of millions of Spanish speakers. The answer, wrong answers and fun fact are correct.: «Martes 13, ni te cases ni te embarques». ¿En cuál de estos países el día de mala suerte NO es el martes 13? → Estados Unidos
- languages-6: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Ves en el noticiero el recuadro del intérprete. ¿En qué década una ley reconoció la Lengua de Señas Colombiana como idioma de la comunidad sorda? → En los años 90
- languages-12: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Escuchas a alguien hablar fuerte y directo, tratar de «usted» hasta al perro y saludar «¡Quiubo, mano!». ¿De dónde es? → Un santandereano
- languages-14: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: El andoque, de las orillas del río Caquetá cerca de Araracuara, estuvo a punto de desaparecer. ¿Cómo lo clasifican los lingüistas? → Como una lengua aislada
- languages-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Soy la costumbre de decir «vos» en vez de «tú», y en Cali me oyes en frases como «vos sabés, ve». ¿Qué soy? → El voseo
- painters-sculptors-and-museums-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Botero la pintó en 1967 para burlarse del poder: un mandatario, los suyos, un general y un obispo. Hoy está en el MoMA de Nueva York. ¿Cómo se llama? → La familia presidencial
- pioneers-and-popular-figures-1: overlap like pop-rock-and-urban-music-0: A esta cantante paisa le dicen «La Bichota», y hasta llamó así a una de sus giras. ¿Quién es? → Karol G: ¿Cómo se llama esta cantante colombiana? → Karol G
- pioneers-and-popular-figures-12: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Gonzalo Mejía impulsó la Carretera al Mar y el Teatro Junín. ¿Qué fundó en Medellín en 1919, una de las pioneras de su tipo en Colombia? → Una empresa de aviación
- places-and-monuments-2: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: La estatua gigante de Shakira bailando en el Malecón de Barranquilla es de metal. ¿De cuáles metales está hecha? → Bronce y aluminio
- poetry-and-childrens-stories-11: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Los cuentos de Tío Conejo y Pedro Rimales no tienen autor conocido. ¿Cómo llegaron hasta nuestros días? → Por la tradición oral
- poetry-and-childrens-stories-12: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Una mamá le canta a su bebé «Arrurrú mi niño, arrurrú mi sol». ¿En qué momento del día suele cantarla? → A la hora de dormir
- pop-rock-and-urban-music-7: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Este grupo de Medellín canta «Me llamas» y «Te vi». ¿Cómo se llama? → Piso 21
- pop-rock-and-urban-music-15: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Escuchas a alguien decir «¡Qué bacano!» cuando algo le gusta mucho. ¿De dónde es, seguramente? → Un colombiano
- popular-and-andean-music-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Lo llamaban 'Chente' y su 'Volver, volver' se canta en fondas y serenatas de toda Colombia. ¿De qué país era Vicente Fernández? → México
- popular-and-andean-music-10: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: Luffy, de One Piece, nunca se quita su sombrero de paja. ¿Qué es la paja? → Tallos secos de plantas
- pre-columbian-cultures-0: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 4: Los indígenas del Caribe la tejían con fibras de plantas y dormían en ella. ¿Qué es? → Hamaca
- street-food-and-bakery-9: hard fail: correct 3, unambiguous 3, no_giveaway 3, no_overlap 5: En la panadería del barrio venden por bolsas un pancito dulce que no cruje como el pan francés. ¿Cómo se llama? → Pan blandito
- sayings-and-expressions-11: overlap like q-5057: ¿Cómo se le dice al acento de Medellín y Antioquia, famoso por el «pues» y el «¡ave María!»? → Paisa: ¿A qué gente de Colombia se le reconoce por despedirse con un «¡chao, pues!»? → Los paisas
- sayings-and-expressions-16: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 4: Al despedirte en Colombia, le mandas cariños a toda la familia del otro, con una «e» muy colombiana: «saludes a…». ¿A qué? → La casa
- scientists-and-inventors-15: overlap like q-1052: El 'toldillo' se cuelga del techo, se usa sobre todo de noche y está hecho de una tela llena de agujeritos muy finos. ¿Qué es un toldillo? → Un mosquitero: Vas a dormir en tierra caliente y quieres evitar que te dé chikunguña. ¿Qué te sirve? → Un toldillo
- street-food-and-bakery-13: overlap like q-5044: Se le echa agua y café molido, se pone a hervir o se enchufa, y de ella sale el tinto de la mañana. ¿Qué es? → La cafetera: En las calles de Colombia, un señor con varios termos te vende 'un tinto' en vasito por pocos pesos. ¿Qué es? → Café negro
- symbols-of-departments-and-cities-0: overlap like q-0498: ¿De qué departamento es típica la lechona, el famoso cerdo relleno? → Tolima: Mira el mapa: el departamento resaltado es la tierra de la lechona más famosa de Colombia. ¿Cuál es? → Tolima
- symbols-of-departments-and-cities-4: overlap like q-5105: Caminas por el centro histórico de Santa Marta, fundada en 1525. ¿Qué conquistador la fundó? → Rodrigo de Bastidas: Esta bahía es la de la ciudad apodada «la Perla de América», fundada en 1525. ¿Quién la fundó? → Rodrigo de Bastidas
- symbols-of-departments-and-cities-8: overlap like q-0069: ¿Qué ciudad colombiana es conocida como la 'Capital Mundial de la Salsa'? → Cali: Estás en la ciudad apodada «Capital Mundial de la Salsa», viendo bailarines zapatear a toda velocidad. ¿Dónde estás? → Cali
- symbols-of-departments-and-cities-14: overlap like q-5209: Antioquia es a antioqueño como Caldas es a… → Caldense: Mira este carriel, el bolso de los arrieros de Antioquia. ¿Cómo se le dice a quien nace en ese departamento? → Antioqueño
- symbols-of-departments-and-cities-16: overlap like q-1359: Técnica de joyería: hilos finísimos de oro o plata se tuercen y se sueldan formando un encaje calado. En Mompox es tradición. ¿Cuál es? → Filigrana: Su ciudad queda en una isla del río Magdalena y es famosa por la filigrana de oro y su Semana Santa. ¿Cuál es su gentilicio? → Momposino
- telenovelas-13: overlap like q-0557: Completa: Grupo Niche es a «Cali pachanguero» como Fruko y sus Tesos es a… → El preso: Estás en una fiesta y suena «Cali pachanguero», el himno de la salsa caleña. ¿Qué agrupación la canta? → Grupo Niche
- telenovelas-14: overlap like q-3066: Which telenovela about a brilliant secretary at a fashion company holds the Guinness record as the most successful telenovela ever? → Yo soy Betty, la fea: Uso lentes y frenos, soy economista muy inteligente y trabajo de secretaria en Ecomoda, enamorada de mi jefe Armando. ¿Quién soy? → Betty
- vallenato-4: overlap like q-0067: ¿Qué ritmo colombiano se toca tradicionalmente con acordeón, caja y guacharaca? → Vallenato: Con los años, el bajo eléctrico se sumó al conjunto vallenato tradicional. ¿Cuántos instrumentos tiene ese conjunto ya con el bajo? → 4
- vallenato-12: overlap like q-5135: Cada abril, en Valledupar, los mejores acordeoneros se pelean mi corona tocando paseo, merengue, son y puya. ¿Quién soy? → El Rey Vallenato: La Plaza Alfonso López lleva el nombre de un expresidente, la rodean casas coloniales y por décadas allí se coronaron los reyes del acordeón. ¿En qué ciudad está? → Valledupar
- vallenato-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: «¡Ay hombe!» es un grito que los cantantes vallenatos sueltan en medio de las canciones y que la gente también usa al hablar. ¿De qué región de Colombia es típico? → La región Caribe
- vallenato-16: overlap like q-5019: Este cantante de Santa Marta mezcló el vallenato con rock y pop en los años 90. ¿Quién es? → Carlos Vives: ¿Qué cantante samario grabó en 1995 la canción «La tierra del olvido», que mezcla vallenato con rock y pop? → Carlos Vives
- writers-and-books-1: overlap like q-0111: ¿Quién escribió el cuento en verso 'El renacuajo paseador'? → Rafael Pombo: Este escritor bogotano escribió el poema «Juan Chunguero». ¿Quién es? → Rafael Pombo
