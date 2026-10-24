# batch-20

Made by `qgen batch` on 2026-10-23 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): hosts-actors-and-comedians, brands-and-products, tv-shows-and-series, rivers-seas-and-islands, national-symbols, popular-and-andean-music, cities-and-towns, ghosts-and-creatures, pioneers-and-popular-figures, cinema, painters-sculptors-and-museums, regional-speech, animals, olympic-medallists, banknotes-and-coins, pop-rock-and-urban-music, writers-and-books, other-sports, symbols-of-departments-and-cities, words, drinks, transport, vallenato, poetry-and-childrens-stories, 20th-century, telenovelas, typical-dishes
- Merged: 187 (q-7602…q-7788)
- Approved: 170
- Needs work: 17
- Dropped by the pipeline: 79
- Reviewed by: claude-opus-5-5
- Claude calls: 455, about $62.07 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-18, batch-19; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-18 | batch-19 | batch-20 |
|---|---|---:|---:|---:|
| source locale |  | es | es | es |
| drafts |  | 286 | 261 | 266 |
| skipped slots |  | 200 | 225 | 220 |
| dropped |  | 70 | 84 | 79 |
| drop rate | ≤ 20.0 % | 24.5 % ✗ | 32.2 % ✗ | 29.7 % ✗ |
| dropped: hard fail correct |  | 1 | 2 | 3 |
| dropped: hard fail unambiguous |  | 1 | 1 | 2 |
| dropped: hard fail no_giveaway |  | 16 | 15 | 13 |
| dropped: overlap |  | 51 | 66 | 63 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 1 | 0 | 0 |
| merged |  | 216 | 177 | 187 |
| approved |  | 198 | 157 | 170 |
| needs_work |  | 18 | 20 | 17 |
| needs_work rate | ≤ 20.0 % | 8.3 % ✓ | 11.3 % ✓ | 9.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.9 % ✓ | 4.0 % ✓ | 2.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.5 % ✓ | 1.1 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.9 % ✓ | 1.7 % ✗ | 1.6 % ✗ |
| needs_work: media | ≤ 10.0 % | 5.1 % ✓ | 5.1 % ✓ | 5.3 % ✓ |
| media: no pick in review 1 |  | 43 | 31 | 33 |
| media: recovered by research |  | 33 | 23 | 23 |
| media: no pick at record |  | 10 | 8 | 10 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.5 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 18.5 % ✓ | 26.4 % ✗ | 24.8 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 43.4 % ✗ | 32.8 % ✗ | 48.0 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 0.83 ✓ | 1.13 ✓ | 1.50 ✓ |
| approved 11–15 |  | 42 | 27 | 51 |
| top move | ≤ 25.0 % | 14.8 % ✓ | 16.4 % ✓ | 13.4 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 86.1 % | 80.2 % | 88.8 % |
| values stimulus |  | 4 | 5 | 4 |
| top clue | ≤ 60.0 % | 40.7 % ✓ | 44.1 % ✓ | 41.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.5 % ✓ | 24.9 % ✓ | 25.7 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 25.0 % ✓ | 27.7 % ✗ | 23.5 % ✓ |
| values lens |  | 11 | 12 | 11 |
| media share | 15.0 %–50.0 % | 13.9 % ✗ | 19.8 % ✓ | 11.2 % ✗ |
| mean fun | ≥ 3.40 | 3.35 ✗ | 3.33 ✗ | 3.38 ✗ |
| cost $ |  | $64.49 | $53.84 | $58.01 |
| $ per approved | ≤ $0.35 | $0.33 ✓ | $0.34 ✓ | $0.34 ✓ |
| calls |  | 455 | 382 | 395 |
| calls per approved |  | 2.30 | 2.43 | 2.32 |
| wall time h |  | 1.89 | 1.49 | 1.71 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 55 (2 %)
- Major among review needs work: 0 of 5 (0 %)
- Problems by kind: giveaway 7 (0 major), fact 2 (0 major), overlap 2 (0 major), media 2 (1 major), difficulty 3 (0 major), style 1 (0 major), other 2 (0 major)
- Mean |audit − final difficulty|: 0.9; ≥ 3 on 3 of 60 (5 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.06

Major findings on approved questions:

- **q-7632**: media — The essential image is "File:A fabulous tree.jpg". That title points to a tree, not a close-up of corn kernels, yet the question says "Mira de cerca: … estos granos", so on the TV the picture won't show what the question asks about. Otherwise the facts hold: Colombian mazamorra and the usual chicha are made from maize, and the Muiscas made maize chicha before the Spanish arrived. The hints are correct (chócolo is tender corn), and with a proper photo of the kernels a difficulty of 1–2 fits. (http://127.0.0.1:8001/review/q-7632)

## Needs work

- **q-7602** (20th-century) En 1958, liberales y conservadores pactaron el Frente Nacional. ¿Para qué se creó? → Para turnarse la presidencia entre los dos partidos: The description gives the answer away. "Un presidente, dos partidos y un pacto" tells players that two parties share one presidency, which is the answer's defining trait. It also rules out the "replace both parties with a new one" option. The description should play on pacts or fine print without hinting that the parties shared power. A smaller point: the question says the pact was made "en 1958", but hint 2 places the agreement in Spain, and that happened in 1956–57 (Benidorm and Sitges). Wording like "El Frente Nacional, que empezó en 1958…" would be more accurate.
- **q-7603** (20th-century) Soy cantadora del Caribe colombiano. En 1982 canté en Estocolmo para el Nobel de Gabo, y en 2011 con Calle 13. ¿Quién soy? → Totó la Momposina: The text is fine, but none of the media candidates works. The sheet shows a Quebec hotel, a Western rock drum kit, a cluttered hall, and photos of Colombian politicians and officials. None of them shows Caribbean Colombian drums or bullerengue/cumbia music, and I can't search again. A new search such as "tambor alegre drum" or "cumbia drums Colombia" is needed. No se encontró una imagen adecuada para esta pregunta.
- **q-7606** (20th-century) El 5 de septiembre de 1993, Faustino Asprilla le marcó dos goles a Argentina en el Monumental. ¿Cuántos goles hizo Colombia ese día? → 5: This is a duplicate of approved q-7066, which asks the same fact: how many goals Colombia scored against Argentina on 5 September 1993, answer 5. Drop this question, or turn it into a different fact about that match that q-7066 doesn't give away.
- **q-7615** (banknotes-and-coins) Este político liberal salía en el viejo billete de 1000 pesos. ¿Quién es? → Jorge Eliécer Gaitán: None of the six candidates is Jorge Eliécer Gaitán. The essential image needs a portrait of Gaitán, and a new search isn't allowed. A query like "Jorge Eliécer Gaitán" would likely find one on Commons. The text itself has no problems. No se encontró una imagen adecuada para esta pregunta.
- **q-7636** (drinks) Mira de cerca esta olla de aluminio, ancha abajo y angosta arriba, que no falta en las cocinas colombianas. ¿Cómo se llama? → La chocolatera: The essential image slot has no candidates, and no new search is allowed. Without a clear photo of a Colombian aluminium chocolatera, a question that starts "Mira de cerca esta olla" can't be played. Either find a suitable photo by hand or reword the question so it doesn't depend on the picture. No se encontró una imagen adecuada para esta pregunta.
- **q-7666** (poetry-and-childrens-stories) Va al final de las fábulas, a veces en un par de versos, y Rafael Pombo la ponía en sus «Fábulas y verdades». ¿Qué es la moraleja? → La enseñanza que deja la historia: None of the image candidates fits the topic: they show a medieval sickroom, a portrait medal, an Alma-Tadema dance scene, an Art Nouveau ornament, an Ovid mythology engraving and a royal frontispiece. None of them shows a fable. A new search isn't allowed, so the slot needs a fable picture, e.g. "Aesop fable illustration" or "fox and crow fable". No se encontró una imagen adecuada para esta pregunta.
- **q-7691** (banknotes-and-coins) Aunque ya casi nadie los ve, el peso colombiano se divide en centavos. ¿Cuántos centavos tiene un peso? → 100: Hint 2 gives the answer away: tying «centavo» to «centímetro» tells players straight away that it's a hundredth (100 cm in a metre). That is hint-3 strength. Replace it with a vague hint, for example one about how other currencies such as the dollar or the euro are split up, that doesn't point to the hundred.
- **q-7703** (ghosts-and-creatures) En una casa vieja las puertas se abren solas, se oyen pasos en la noche y los bombillos titilan sin razón. ¿Qué dice la gente que está la casa? → Embrujada: The fun fact says the Salto del Tequendama casona 'hoy es un museo', which is exactly the answer of approved question q-6835, so a player who sees this question's fun fact already knows q-6835's answer. The fun fact needs another fact about haunted houses that doesn't reveal what the Tequendama house is used for today. The question itself, the description, hints and options are fine.
- **q-7710** (national-symbols) En Colombia, cuando suena el himno nacional en un evento, ¿quiénes deben ponerse de pie? → Todos los presentes: None of the image candidates works for a question about the Colombian national anthem. They show pride flags (1–3), US flags (4, 6) and a Panamanian flag at a Noriega rally (5), and a new search isn't allowed. The slot needs a decorative image such as "Colombia stadium crowd" or "Colombian flag ceremony". No se encontró una imagen adecuada para esta pregunta.
- **q-7715** (poetry-and-childrens-stories) En el trabalenguas «Pepe Pecas pica papas con un pico», ¿qué son las pecas que le dan su apodo a Pepe? → Manchitas cafés en la piel: None of the image candidates shows potatoes or anything else from the tongue-twister's world, and no new search is allowed. The slot needs a clear photo of raw potatoes (for example "potatoes in sack" or "pile of potatoes"). No se encontró una imagen adecuada para esta pregunta.
- **q-7724** (regional-speech) En las fiestas del Tolima y el Huila, ¿qué es un «insulso»? → Una masa dulce de maíz y panela: The text is fine, but none of the media candidates fits. All six are folk-music festivals in the US, Canada or Australia (Newport, Winnipeg, Kerrville, Woodford), not Tolima's San Pedro festivities or its food, and no new search is allowed. The slot needs a new search such as "lechona tolimense" or "San Pedro festival Neiva". No se encontró una imagen adecuada para esta pregunta.
- **q-7750** (symbols-of-departments-and-cities) Mira la foto: esta es la bandera de un departamento de Colombia. ¿De cuál? → San Andrés y Providencia: None of the candidates shows the flag of San Andrés, Providencia y Santa Catalina, so this essential image slot can't be filled, and no new search is allowed. The question needs the official flag file (e.g. the Commons SVG 'Flag of San Andrés y Providencia'), shown without its filename or caption. No se encontró una imagen adecuada para esta pregunta.
- **q-7753** (symbols-of-departments-and-cities) ¿En qué década abrió su primera etapa el Gran Malecón del Río, junto al Magdalena en Barranquilla? → En la década de 2010: Hint 2 gives the answer away: Shakira became a worldwide star around 2001, so with hint 1 ("bastante reciente") the 2010s is the only option left. Replace hint 2 with a vaguer clue, for example one about the city's riverfront being industrial before, without a time anchor that rules out the 1990s.
- **q-7770** (tv-shows-and-series) Las letras de «Noticias RCN» vienen de una cadena que nació en la radio. Completa: Radio Cadena… → Nacional: Hint 2 gives the answer away: with these four options, every Colombian player instantly links 'a famous football club from Medellín' to Atlético Nacional, so the question is solved at hint 2. That is hint-3 strength, and hint 3 ('lo contrario de regional') already plays that role. Replace hint 2 with a vaguer clue, for example one about the radio era or Medellín as the founding city, without pointing to the word itself.
- **q-7774** (typical-dishes) Mira estos fríjoles antioqueños. ¿Cómo se llama el guiso de tomate y cebolla que se les sirve encima? → Hogao: No candidate shows frijoles antioqueños: all six are foreign bean soups (US Senate bean soup, Moroccan bissara, Maltese kusksu, etc.). The question says "Mira estos fríjoles antioqueños", so the media must show that dish, and no new search is allowed. Either find a real photo of frijoles antioqueños (search "frijoles antioqueños" or "bandeja paisa beans"), or reword the question so it doesn't point at a photo and use illustrative media. No se encontró una imagen adecuada para esta pregunta.
- **q-7781** (words) ¿En qué región de Colombia es típico saludar a cualquier amigo con un «¿Qué más, primo?»? → La costa Caribe: No media candidate fits. 1 and 2 are a US graduation candle ceremony, and 3 to 6 are Gerald Ford Library contact sheets, none of which shows friends greeting each other. The slot needs a new search such as "friends greeting street" or "Colombian friends chatting". The question text itself is fine. No se encontró una imagen adecuada para esta pregunta.
- **q-7785** (writers-and-books) «En un lugar de la Mancha» es a «Don Quijote» como «Muchos años después, frente al pelotón de fusilamiento» es a… → «Cien años de soledad»: Hint 2 gives the answer away: it names Colonel Aureliano Buendía and the ice, which are known only from «Cien años de soledad». The question also overlaps approved q-5253, which already starts "Abres «Cien años de soledad» y en la primera frase Aureliano recuerda cuando conoció el hielo". Seeing that question tells players which novel opens with this line.

## Question axes

- move: analogy 5, cause_effect 5, count 4, estimate 6, identify 21, made_of 8, name_concept 17, odd_one_out 18, origin 18, purpose 13, record 3, sequence 5, when 15, who 24, word_meaning 25
- stimulus: detail 3, map_outline 2, none 166, photo 16
- clue: completion 7, direct 78, riddle 24, scenario 22, three_facts 56
- answer_kind: group 22, number 10, person 33, place 24, thing 48, time 15, word 35
- lens: body_senses 7, colombia 44, educational_media 7, everyday 37, history 19, language 22, nature 9, pop_culture 25, school 12, science_news 3, university 2

## Dropped by the pipeline

- 20th-century-0: overlap like q-7006: El billete colombiano de Gabriel García Márquez vale 50 000 pesos. ¿Cuántas lucas son? → 50: ¿Quién es este escritor colombiano que sale en el billete de 50 000 pesos? → Gabriel García Márquez
- 20th-century-9: overlap like q-7424: En 1982 García Márquez llevó músicos vallenatos a Estocolmo y recibió el Nobel vestido con una prenda blanca. ¿Cómo se llama? → El liqui liqui: En diciembre de 1982, en Estocolmo, Gabo rompió el protocolo del frac y recibió el Nobel vestido con un liqui liqui. ¿Qué es un liqui liqui? → Un traje de chaqueta y pantalón
- 20th-century-10: overlap like q-7161: Fui cantante en la orquesta de Pedro Salcedo y le puse letra a una cumbia de Juan Madera sobre una falda roja que hoy suena en todo el mundo. ¿Quién soy? → Wilson Choperena: La compusieron Juan Madera y Wilson Choperena, se grabó en 1960, y cuando suena «La pollera colorá» todo el mundo sale a bailar. ¿Qué ritmo es? → Cumbia
- animals-4: overlap like q-4930: Listen: which sea animal makes these clicks and whistles? → A dolphin: Escucha: estos silbidos y chasquidos se oyen bajo el mar Caribe colombiano. ¿Qué animal los hace? → El delfín nariz de botella
- animals-5: overlap like q-5543: Bees build it from wax, it hangs inside their hive, and it is full of tiny rooms. What do bees keep in it? → Honey and baby bees: Tengo muchas celdas de seis lados, guardo miel adentro y miles de abejas viven en mí. ¿Qué soy? → El panal
- animals-8: overlap like q-0428: Completa el refrán: «Camarón que se duerme…» → …se lo lleva la corriente: Cuando te dicen «camarón que se duerme se lo lleva la corriente», ¿qué te quieren decir? → Si te descuidas, pierdes la oportunidad
- animals-9: overlap like q-0005: ¿Cuál es el ave nacional de Colombia? → El cóndor de los Andes: Sus alas abiertas miden casi 3 metros, come animales muertos y en el escudo de Colombia lleva una corona de laurel en el pico. ¿Qué ave es? → El cóndor de los Andes
- brands-and-products-1: overlap like q-7138: En una tienda de barrio en Colombia pides una Jumbo. ¿Qué te entregan? → Una chocolatina con maní: La chocolatina Jumbo es famosa en Colombia porque, además de chocolate, trae mucho de este ingrediente. ¿Cuál es? → Maní
- brands-and-products-17: overlap like q-5213: Estos son patacones, como los que se comen en toda Colombia. ¿De qué están hechos? → Plátano verde: Los Natuchips son un mecato colombiano como el de la foto. ¿De qué están hechos? → Plátano verde
- cinema-8: overlap like q-0184: ¿Qué ciudad colombiana construyó grandes murallas de piedra para protegerse de los ataques piratas? → Cartagena: Will Smith filmó en esta ciudad colombiana una persecución en moto de 'Proyecto Géminis', entre murallas coloniales y casas de colores frente al mar Caribe. ¿Qué ciudad es? → Cartagena
- cinema-13: overlap like q-5080: Barichara tiene calles de piedra, casas de tapia pisada y un Camino Real que baja hasta Guane. ¿En qué departamento está? → Santander: Barichara es un pueblo de piedra famoso por sus casas blancas, el Camino Real a Guane y un festival de cine ambiental. ¿En qué departamento queda? → Santander
- cities-and-towns-1: overlap like q-5028: Nació en 1955, construyó Hidroituango y cada diciembre prende algunos de los alumbrados navideños más famosos de Colombia. ¿Qué empresa es? → EPM: Cada diciembre, Medellín llena el río y los parques de figuras de luces como estas. ¿Cómo les dicen los paisas? → Los alumbrados
- cities-and-towns-3: overlap like q-6840: En Colombia hay seis estratos y el 1 es el más bajo. ¿Qué pasa con los servicios públicos de una casa estrato 1? → Pagan menos por un subsidio: En Colombia, las viviendas se clasifican del 1 al 6, eso cambia lo que pagas de agua y luz, y existe desde el siglo pasado. ¿Cómo se llama? → El estrato
- cities-and-towns-11: overlap like q-7373: Mira la foto: este gato de bronce cuida la orilla de un río en Cali. ¿Qué artista lo hizo? → Hernando Tejada: En la Sucursal del Cielo, junto al río, hay una famosa escultura de bronce del maestro Hernando Tejada. ¿Qué animal es? → Un gato
- cities-and-towns-13: overlap like q-0557: Completa: Grupo Niche es a «Cali pachanguero» como Fruko y sus Tesos es a… → El preso: Nacimos en Bogotá en 1979, de la mano de músicos chocoanos, pero nos hicimos famosos en Cali. Una canción nuestra dice «Cali, luz de un nuevo cielo». ¿Quiénes somos? → El Grupo Niche
- ghosts-and-creatures-4: overlap like q-0172: ¿De qué región de Colombia es la famosa leyenda del Hombre Caimán? → La región Caribe: Estás leyendo leyendas de la costa: «Drácula es al murciélago como Saúl Montenegro es al…». ¿Qué animal completa la frase? → Caimán
- ghosts-and-creatures-15: overlap like q-7490: Durante años, en Colombia muchos ramos del Domingo de Ramos se hicieron con hojas de una palma que casi se extingue por eso; hoy está prohibido cortarla. ¿Cuál? → La palma de cera: En muchas casas colombianas se guarda detrás de la puerta y se quema un pedacito cuando hay tormenta. ¿Qué es el «ramo bendito»? → Palma bendecida el Domingo de Ramos
- ghosts-and-creatures-16: overlap like ghosts-and-creatures-13: En Colombia, mucha gente «se echa la bendición» antes de un viaje o de patear un penalti. ¿Qué gesto hace? → Hacer la señal de la cruz: ¿Qué parte del cuerpo NO se toca al hacer la señal de la cruz? → La rodilla
- national-symbols-7: overlap like q-7607: Antes de llegar a tu taza como un tinto, el café fue una cereza roja. ¿Dónde creció? → En un cafetal: En Colombia, esto se llama «un tinto». ¿De qué está hecho? → De café
- national-symbols-9: overlap like q-6771: Before a World Cup match, the players line up, often put a hand on their heart and sing their country's special song. What is that song called? → The national anthem: El saludo militar es a los soldados como ¿qué gesto es a los civiles cuando suena el himno nacional? → La mano derecha en el pecho
- national-symbols-10: overlap like q-7426: Estás en el valle de Cocora, frente a la palma de cera, el árbol nacional de Colombia. ¿Hasta qué altura puede llegar? → Unos 60 metros: Es el árbol nacional de Colombia, puede pasar de 60 metros de altura y llena el valle de Cocora, en el Quindío. ¿Cuál es? → La palma de cera
- olympic-medallists-5: overlap like q-3063: On the Olympic podium, first place is to gold as third place is to…? → Bronze: Estás viendo los Olímpicos y una colombiana gana la medalla de plata. ¿Qué medalla recibe quien llega justo detrás de ella? → Bronce
- olympic-medallists-8: overlap like q-0484: ¿En qué prueba de atletismo ganó Caterine Ibargüen la medalla de oro en los Juegos Olímpicos de Río 2016? → Salto triple: En los Olímpicos de 2016, en la ciudad de esta estatua, una colombiana ganó el oro tras quedar de plata en Londres 2012. ¿Quién es? → Caterine Ibargüen
- olympic-medallists-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Mariana Pajón ganó la medalla de oro en Londres 2012. ¿En qué puesto terminó la carrera? → 1
- painters-sculptors-and-museums-3: overlap like q-6924: El 20 de julio de 1810 en Santafé, un comerciante español no quiso prestar un florero y estalló la pelea. ¿Quién era? → José González Llorente: Estás en el Museo de la Independencia Casa del Florero, en Bogotá. ¿De quién era el florero que se volvió famoso el 20 de julio de 1810? → José González Llorente
- painters-sculptors-and-museums-9: overlap like q-0112: ¿Qué artista colombiano es famoso por pintar y esculpir figuras muy voluminosas, 'gorditas'? → Fernando Botero: Figuras redondas, volúmenes enormes, colores alegres y hasta frutas y gatos bien gorditos: ¿cómo se llama este estilo que nació en Medellín? → El boterismo
- painters-sculptors-and-museums-10: overlap like q-3430: I'm a metal can. Shake me until I rattle, press my top, and a colorful mist comes out. What am I for? → Painting: Hago «clac, clac» cuando me agitas y los grafiteros de Bogotá me usan para llenar de colores las paredes. ¿Qué soy? → Un aerosol
- pioneers-and-popular-figures-4: overlap like q-6803: ¿En qué municipio de Cundinamarca está esta catedral, construida dentro de una mina de sal? → Zipaquirá: Egan Bernal nació en Bogotá, pero creció en una ciudad de Cundinamarca a más de 2600 metros, famosa por su Catedral de Sal. ¿Cuál? → Zipaquirá
- pioneers-and-popular-figures-7: overlap like q-0541: ¿Cuántos años tenía Linda Caicedo cuando le hizo un golazo a Alemania en el Mundial femenino de 2023? → 18 años: ¿Quién es esta futbolista colombiana? → Linda Caicedo
- poetry-and-childrens-stories-7: overlap like q-7207: «Érase una viejecita sin nadita qué comer». ¿Cuál de estos personajes NO salió de un poema de Rafael Pombo? → El ratón Pérez: «Érase una viejecita sin nadita qué comer, sino carnes, frutas, dulces…». ¿Quién escribió este poema? → Rafael Pombo
- poetry-and-childrens-stories-11: overlap like q-5254: ¿Qué poema de Rafael Pombo cuenta cómo un niño llamó al pastelero para probar sus pasteles, pero no tenía con qué pagar? → Simón el bobito: Completa el verso de Rafael Pombo: «Simón el bobito llamó al…». → Pastelero
- pop-rock-and-urban-music-12: overlap like pioneers-and-popular-figures-2: ¿Quién es este cantante colombiano? → Juanes: Soy de Medellín, empecé en la banda de metal Ekhymosis y en 2002 medio mundo cantó mi «A Dios le pido». ¿Quién soy? → Juanes
- popular-and-andean-music-13: overlap like q-7061: El 31 de diciembre se rellena un muñeco con ropa vieja y aserrín, y a la medianoche se le prende fuego. ¿Qué se dice que se quema con él? → Lo malo del año que termina: El 31 de diciembre muchas familias colombianas arman un muñeco llamado «Año Viejo» para quemarlo a medianoche. ¿Con qué se hace? → Con ropa vieja rellena de papel
- popular-and-andean-music-14: overlap like cities-and-towns-1: Cada diciembre, Medellín llena el río y los parques de figuras de luces como estas. ¿Cómo les dicen los paisas? → Los alumbrados: Cada diciembre, Medellín llena el río y los parques de millones de luces de colores, una tradición de muchas décadas. ¿Cómo se llama? → Los alumbrados
- regional-speech-4: overlap like q-6887: En el departamento resaltado en este mapa tratan de «usted» hasta a los hijos y a la pareja, con un tono fuerte y directo. ¿Cuál es? → Santander: En Colombia, ¿de qué región tiene fama la gente de hablar fuerte y golpeado, y parecer «brava» aunque esté contenta? → Los santandereanos
- regional-speech-16: overlap like q-6967: La chirimía con clarinete, bombardino, redoblante, bombo y platillos es la banda típica de un departamento del Pacífico. ¿Cuál? → Chocó: En las fiestas de San Pacho, en Quibdó, ¿cómo se llama el grupo que toca con clarinete, bombardino, tambora y platillos? → Chirimía
- 20th-century-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Según el artículo 1 de la Constitución de 1991, ¿qué tipo de Estado es Colombia? → Estado social de derecho
- animals-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Completa el dicho: «Cada oveja…» → …con su pareja
- cinema-4: overlap like q-5029: Dirigí 'La gente de La Universal' en 1993 y, años después, la comedia negra 'El Colombian Dream'. ¿Quién soy? → Felipe Aljure: En 'La gente de La Universal', de Felipe Aljure, un expolicía maneja en el centro de Bogotá el negocio que da nombre a la película. ¿Qué negocio es? → Una agencia de detectives
- drinks-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: El calentado es un desayuno típico colombiano, con chocolate o tinto. ¿De dónde sale? → De lo que sobró de la comida del día anterior
- ghosts-and-creatures-1: hard fail: correct 3, unambiguous 3, no_giveaway 4, no_overlap 5: Es enorme, tiene ojos de candela y arrastra cadenas por los caminos de noche. Según la leyenda, ¿para qué se aparece el Perro Negro? → Para asustar a los borrachos de noche
- ghosts-and-creatures-6: overlap like q-0482: ¿Qué espanto de la leyenda llanera es altísimo y flaco, anda de noche por la sabana y carga en un costal los huesos de su propio papá? → El Silbón: Completa el agüero llanero: «No silbe de noche, porque…» → llega el Silbón
- national-symbols-3: overlap like q-7646: Completa: en los colegios de Colombia, el acto cívico en que se honra la patria y se premia a los mejores estudiantes se llama «izada de…». → bandera: En los desfiles de los colegios de Colombia, la escolta lleva la bandera. ¿A qué estudiantes suelen escoger para ella? → A los de mejor rendimiento y disciplina
- other-sports-2: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Suesca, en Cundinamarca, cerca de Bogotá, es famosa en toda Colombia por un deporte. ¿Para qué viajan allá muchos deportistas? → Para escalar en roca
- painters-sculptors-and-museums-2: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Soy de bronce, me hizo el pintor más famoso de Medellín y vivo en el Parque Berrío. La gente se cita diciendo «nos vemos en…». ¿Cómo me llaman? → La Gorda
- pioneers-and-popular-figures-2: overlap like pop-rock-and-urban-music-12: Soy de Medellín, empecé en la banda de metal Ekhymosis y en 2002 medio mundo cantó mi «A Dios le pido». ¿Quién soy? → Juanes: ¿Quién es este cantante colombiano? → Juanes
- popular-and-andean-music-3: hard fail: correct 3, unambiguous 3, no_giveaway 4, no_overlap 5: ¿En qué década salió el primer disco de «Los 50 de Joselito», infaltable en las fiestas decembrinas colombianas? → Década de 1990
- rivers-seas-and-islands-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Estos son los cerros de Mavecure, a orillas del río Inírida. ¿En qué departamento quedan? → Guainía
- telenovelas-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Carolina Ramírez fue Rosario Guerrero, una cantante bogotana que se enamora de un extranjero que huye de la justicia y se esconde en Bogotá. ¿Qué telenovela era? → La hija del mariachi
- transport-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Mira la foto: en Bogotá, este aparato no marca pesos sino 'unidades'. ¿Cómo se llama? → El taxímetro
- tv-shows-and-series-14: overlap like q-3066: Which telenovela about a brilliant secretary at a fashion company holds the Guinness record as the most successful telenovela ever? → Yo soy Betty, la fea: ¿Cuál de estos programas emitidos en Colombia es una creación colombiana y no la adaptación de un formato extranjero? → Yo soy Betty, la fea
- typical-dishes-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En los cumpleaños colombianos casi siempre sirven «arroz con pollo», con papitas de paquete al lado. ¿Qué es? → Arroz amarillo revuelto con pollo y verduras
- typical-dishes-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La trucha al ajillo es un clásico de los restaurantes de tierra fría: se fríe entera y se baña en salsa con mantequilla. ¿Qué ingrediente le da el nombre? → El ajo
- words-5: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Completa: si alguien en Colombia dice «A ese río helado no me meto ni por el chiras», quiere decir que no se mete… → Por nada del mundo
- words-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Lo dices cuando toca hacer tareas un domingo, cuando la fila es eterna o cuando llueve y no puedes salir. ¿Qué expresas con «¡Qué mamera!»? → Pereza o aburrimiento
- words-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Completa: en Colombia, si a alguien «se le prendió el bombillo», es que… → Se le ocurrió una idea
- rivers-seas-and-islands-8: overlap like q-0174: ¿En qué parque nacional, cerca de Santa Marta, está la famosa playa de Cabo San Juan? → Parque Tayrona: El Cabo San Juan del Guía tiene una caseta de hamacas sobre una roca, dos playas en media luna y se llega caminando desde Cañaveral. ¿En qué parque nacional queda? → Parque Tayrona
- rivers-seas-and-islands-11: overlap like cities-and-towns-1: Cada diciembre, Medellín llena el río y los parques de figuras de luces como estas. ¿Cómo les dicen los paisas? → Los alumbrados: Estás en Medellín en diciembre y te invitan a ver los alumbrados en el río. ¿Qué vas a ver? → Luces navideñas
- rivers-seas-and-islands-17: overlap like q-5119: ¿Qué departamento de Colombia está resaltado en este mapa? → Antioquia: Mira el mapa: en este departamento está el embalse del Peñol, con la gigantesca piedra a la que sube la gente por escaleras. ¿Qué departamento es? → Antioquia
- symbols-of-departments-and-cities-2: overlap like q-5081: Estás al pie de Monserrate, en Bogotá, y quieres subir. ¿Cuál de estos NO te sirve para llegar arriba? → El metro: Mira la foto: ¿cómo se llama este cerro de Bogotá con un santuario blanco en la cima? → Monserrate
- symbols-of-departments-and-cities-10: overlap like q-7499: Mira el mapa: ¿qué departamento del Eje Cafetero está resaltado? → Caldas: Si eres manizaleño, eres de la capital del departamento resaltado en el mapa. ¿Cuál es? → Caldas
- symbols-of-departments-and-cities-13: overlap like q-7496: Soy plana hasta donde alcanza la vista, mis vaqueros arrean ganado cantando y en mis fiestas suenan arpa, cuatro y maracas. ¿Qué región soy? → La Orinoquía: En el mapa está resaltada la región de donde son los llaneros. ¿Cómo se llama? → Orinoquía
- symbols-of-departments-and-cities-14: overlap like q-0069: ¿Qué ciudad colombiana es conocida como la 'Capital Mundial de la Salsa'? → Cali: Mira la foto: una ciudad colombiana es famosa como la capital mundial de este baile. ¿Cuál es? → Cali
- telenovelas-0: overlap like q-7552: La serie de Netflix «Cien años de soledad» (2024) se grabó toda en Colombia. ¿En qué departamento se construyó su Macondo? → Tolima: Abres Netflix y ves a Macondo, construido de verdad en Colombia para la serie de «Cien años de soledad». ¿En qué año se estrenó? → 2024
- telenovelas-7: overlap like q-7150: La primera transmisión de televisión en Colombia fue el 13 de junio de 1954. ¿Desde qué edificio de Bogotá se emitió? → La Biblioteca Nacional: ¿En qué año se hizo la primera transmisión de televisión en Colombia? → 1954
- telenovelas-12: overlap like q-3066: Which telenovela about a brilliant secretary at a fashion company holds the Guinness record as the most successful telenovela ever? → Yo soy Betty, la fea: Soy economista, uso lentes, frenos y un peinado pasado de moda, trabajo de secretaria en Ecomoda y vivo enamorada de mi jefe, don Armando. ¿Quién soy? → Beatriz Pinzón Solano
- transport-0: overlap like q-1183: Esta es la Big Boy, una de las locomotoras de vapor más grandes que se han construido. ¿Para qué la fabricaron? → Arrastrar trenes de carga por montañas: Mira la foto: hace más de 100 años, en Colombia, máquinas como esta recorrían Antioquia y la Sabana. ¿Para qué servían? → Para jalar vagones con gente y carga
- transport-13: overlap like q-5036: La película colombiana 'El abrazo de la serpiente' se filmó en una región de selva con delfines rosados, anacondas y la ciudad de Leticia. ¿Cuál es? → La Amazonía: Barranquilla es al río Magdalena como Leticia es al río… → Amazonas
- tv-shows-and-series-15: overlap like q-5168: Andrés Cepeda canta baladas, fue vocalista de Poligamia y ha sido jurado de 'La Voz'. ¿En qué ciudad nació? → Bogotá: ¿Qué cantante colombiano de baladas ha sido coach en muchas temporadas de «La Voz Colombia»? → Andrés Cepeda
- tv-shows-and-series-17: overlap like q-5023: Este programa de humor de la TV colombiana, al aire desde 1972, es famoso por sus cuentachistes y sketches. ¿Cómo se llama? → Sábados Felices: ¿Cuál de estos programas de la TV colombiana NO es un noticiero? → Sábados Felices
- typical-dishes-3: overlap like q-0465: La aguapanela se hace con panela. Pero, ¿de qué se hace la panela? → Del jugo de la caña de azúcar: La aguapanela se toma caliente con queso o fría con limón. ¿De qué planta sale la panela? → De la caña de azúcar
- typical-dishes-10: overlap like q-0003: ¿Con qué se hacen tradicionalmente las arepas? → Maíz: La arepa paisa tradicional es blanca, delgada y sin relleno, y se asa en la parrilla. ¿De qué se hace? → De maíz blanco cocido y molido
- vallenato-0: overlap like q-5019: Este cantante de Santa Marta mezcló el vallenato con rock y pop en los años 90. ¿Quién es? → Carlos Vives: Suena en la radio «La tierra del olvido», de Carlos Vives, con acordeón y gaita. ¿En qué década salió? → En los años 90
- vallenato-5: overlap like q-7386: Mira esta mochila de muchos colores. ¿Quiénes la tejen tradicionalmente? → Las mujeres wayuu: Mira la foto: estas mochilas de colores se tejen en La Guajira. ¿Qué pueblo indígena las hace? → Los wayuu
- vallenato-7: overlap like q-5135: Cada abril, en Valledupar, los mejores acordeoneros se pelean mi corona tocando paseo, merengue, son y puya. ¿Quién soy? → El Rey Vallenato: Lleva el nombre de un presidente, la rodean casas coloniales y en 1968 recibió el primer festival de acordeoneros. ¿En qué ciudad está la plaza Alfonso López? → Valledupar
- words-8: overlap like q-5057: ¿Cómo se le dice al acento de Medellín y Antioquia, famoso por el «pues» y el «¡ave María!»? → Paisa: Es típica de los paisas, se dice cuando algo te sorprende mucho y viene de una oración a la Virgen. ¿Qué expresión es? → ¡Avemaría!
- words-16: overlap like q-7534: En la Costa dicen que ese niño es muy «pechichón». ¿Cómo es? → Muy consentido: Es como le dicen a un niño muy consentido, viene del verbo «pechichar» y se oye mucho en tierra caliente frente al mar. ¿En qué región de Colombia se dice «pechiche»? → La costa Caribe
- writers-and-books-9: overlap like q-6791: En el poema de Rafael Pombo, Rin Rin Renacuajo «salió esta mañana muy tieso y muy majo». ¿Qué significa «majo» aquí? → Elegante y bien arreglado: Salí una mañana muy tieso y muy majo, con pantalón corto y corbata a la moda, aunque mi mamá me dijo que no saliera. ¿Quién soy? → Rinrín Renacuajo
- writers-and-books-17: overlap like q-0111: ¿Quién escribió el cuento en verso 'El renacuajo paseador'? → Rafael Pombo: El hombre de la foto escribió «Hora de tinieblas», un largo poema lleno de dudas sobre el sentido de la vida. ¿Quién es? → Rafael Pombo
