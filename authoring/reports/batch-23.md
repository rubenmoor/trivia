# batch-23

Made by `qgen batch` on 2026-10-24 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): hosts-actors-and-comedians, salsa-and-tropical-music, plants-and-flowers, vallenato, olympic-medallists, crafts-and-traditional-dress, telenovelas, pop-rock-and-urban-music, scientists-and-inventors, popular-and-andean-music, indigenous-myths-and-folk-beliefs, painters-sculptors-and-museums, poetry-and-childrens-stories, regions-and-departments, regional-speech, natural-parks-and-ecosystems, club-football, national-symbols, rhythms-dances-and-instruments, pioneers-and-popular-figures, banknotes-and-coins, ghosts-and-creatures, national-team, 19th-century, brands-and-products, other-sports, fruits
- Merged: 150 (q-8107…q-8256)
- Approved: 136
- Needs work: 14
- Dropped by the pipeline: 84
- Reviewed by: claude-opus-5-5
- Claude calls: 407, about $55.86 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-21, batch-22; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-21 | batch-22 | batch-23 |
|---|---|---:|---:|---:|
| source locale |  | es | es | es |
| drafts |  | 266 | 237 | 234 |
| skipped slots |  | 220 | 249 | 252 |
| dropped |  | 89 | 96 | 84 |
| drop rate | ≤ 20.0 % | 33.5 % ✗ | 40.5 % ✗ | 35.9 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 2 |
| dropped: hard fail unambiguous |  | 1 | 2 | 2 |
| dropped: hard fail no_giveaway |  | 20 | 10 | 7 |
| dropped: overlap |  | 67 | 85 | 73 |
| dropped: duplicate |  | 2 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 1 |
| merged |  | 177 | 141 | 150 |
| approved |  | 169 | 126 | 136 |
| needs_work |  | 8 | 15 | 14 |
| needs_work rate | ≤ 20.0 % | 4.5 % ✓ | 10.6 % ✓ | 9.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 2.1 % ✓ | 2.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.6 % ✓ | 1.4 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.6 % ✓ | 2.1 % ✗ | 2.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.4 % ✓ | 5.0 % ✓ | 4.7 % ✓ |
| media: no pick in review 1 |  | 26 | 29 | 26 |
| media: recovered by research |  | 22 | 22 | 20 |
| media: no pick at record |  | 4 | 7 | 7 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 26.3 % ✗ | 37.1 % ✗ | 32.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 34.7 % ✗ | 34.6 % ✗ | 32.8 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.43 ✓ | 1.33 ✓ | 3.50 ✗ |
| approved 11–15 |  | 28 | 33 | 31 |
| top move | ≤ 25.0 % | 13.0 % ✓ | 13.5 % ✓ | 16.0 % ✓ |
| values move |  | 14 | 15 | 15 |
| top stimulus |  | 84.7 % | 85.1 % | 88.7 % |
| values stimulus |  | 4 | 4 | 3 |
| top clue | ≤ 60.0 % | 39.0 % ✓ | 41.1 % ✓ | 38.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 20.3 % ✓ | 30.5 % ✓ | 34.7 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 23.7 % ✓ | 27.0 % ✗ | 24.7 % ✓ |
| values lens |  | 12 | 10 | 10 |
| media share | 15.0 %–50.0 % | 15.3 % ✓ | 14.9 % ✗ | 11.3 % ✗ |
| mean fun | ≥ 3.40 | 3.38 ✗ | 3.27 ✗ | 3.32 ✗ |
| cost $ |  | $56.01 | $49.86 | $51.94 |
| $ per approved | ≤ $0.35 | $0.33 ✓ | $0.40 ✗ | $0.38 ✗ |
| calls |  | 375 | 332 | 347 |
| calls per approved |  | 2.22 | 2.63 | 2.55 |
| wall time h |  | 1.65 | 1.43 | 1.48 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 54 (4 %)
- Major among review needs work: 2 of 6 (33 %)
- Problems by kind: giveaway 6 (0 major), fact 2 (1 major), ambiguity 1 (1 major), overlap 6 (3 major), media 6 (1 major), style 1 (0 major), other 2 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.92

Major findings on approved questions:

- **q-8118**: overlap — The question text opens with "Al Envigado le dicen «la Naranja Mecánica»". That is exactly the answer to the approved related question q-7033 ("Al club apodado «la Naranja Mecánica»… ¿Cuál?" → Envigado), so playing one gives the other away. The facts hold: the Netherlands of 1974 reached the final unbeaten and lost it to West Germany, the host, and none of 1958, 1986 or 2002 fits. The hints, the description and the Envigado map image are fine. (http://127.0.0.1:8001/review/q-8118)
- **q-8238**: ambiguity, fact — The wrong answer "Los Hispanos" can also be defended. Wikipedia's pages on Gustavo Quintero and on Los Hispanos both say he was Los Hispanos' main singer in Medellín in the late 1960s, before he left to found Los Graduados, so the question "¿Con qué orquesta?" has two right answers. The fun fact also misleads: it presents Los Hispanos as a separate act from the same era, when Quintero sang in it himself. (http://127.0.0.1:8001/review/q-8238)

## Needs work

- **q-8113** (banknotes-and-coins) Quieres cambiar un billete de 50 000 pesos solo por billetes de 2000. ¿Cuántos te tienen que dar? → 25: The text is fine (25 is correct and the Ciudad Perdida fun fact checks out), but none of the image candidates works. The question names the current 50 000 and 2000 peso bills, and all four candidates are 1890s–1900 notes from private banks. No new search is allowed. Find a photo of the current 50 000 peso bill (García Márquez), or of 2000 peso bills, with no '25' visible. No se encontró una imagen adecuada para esta pregunta.
- **q-8128** (crafts-and-traditional-dress) Mira la foto: en Usiacurí, Atlántico, tejen artesanías como estas. ¿Con qué fibra? → Palma de iraca: The media slot has no candidates and can't be searched again. The question says "Mira la foto… artesanías como estas", so it needs a real photo of Usiacurí iraca crafts. Either find such an image by hand, or reword the question so it doesn't refer to a photo and use a decorative image instead. No se encontró una imagen adecuada para esta pregunta.
- **q-8145** (indigenous-myths-and-folk-beliefs) Según la leyenda antioqueña, el Sombrerón sale de noche en un caballo negro con dos perros encadenados. ¿A quiénes persigue? → A borrachos, apostadores y peleones: None of the six candidates fits the question, and no new search is allowed. They show a Sunoco gas station, an 1893 sketch of Princeton's Nassau Hall, an old greenhouse print, a brick street in Greenwich Village, New York, and two newspaper scans. The slot needs a new search for a night-time Antioquian village street, for example "Jardín Antioquia night" or "Santa Fe de Antioquia street". No se encontró una imagen adecuada para esta pregunta.
- **q-8152** (national-symbols) Mira esta bandera de la Gran Colombia. ¿Quién propuso sus tres colores, amarillo, azul y rojo? → Francisco de Miranda: This overlaps approved q-7279, which says Catherine the Great inspired "la bandera de Miranda". Anyone who has seen that question knows that Miranda proposed the yellow, blue and red, so one question gives the other away. Either drop this question or reword q-7279 so it no longer names Miranda as the creator of the flag.
- **q-8154** (national-symbols) Son en julio y agosto, se cuelgan banderas en las casas y hay desfiles por la independencia. ¿Cómo se llaman estas celebraciones? → Fiestas patrias: None of the candidates fits as an illustrative image. Candidates 2–4 show Ukrainian and Palestinian flags, 5 a Brazilian flag, 6 the US Star-Spangled Banner Flag House, and 1 is a plain wooden window in Riga with no link to Colombia. A new search is needed, for example "Colombian flag balcony" or "Colombia independence parade". Minor point for whoever revises next: hint 3 spells out "patria", which is very close to the answer's own wording. No se encontró una imagen adecuada para esta pregunta.
- **q-8166** (other-sports) En las fiestas de pueblo ponen un palo muy alto untado de grasa, con premios arriba, y la gente intenta trepar. ¿Cómo se llama? → Palo encebado: The text is fine, but none of the image candidates fits a Colombian town fiesta. 1 is a painted wardrobe in a museum. 2 and 3 are a 'Villaggio Latino' street event in Carpentras, France. 4 is a Belgian trade-union festival. 5 and 6 are 17th-century Flemish peasant paintings by Teniers. A new search, for example 'palo encebado Colombia' or 'greasy pole festival', would help, but no more searches are allowed for this slot. No se encontró una imagen adecuada para esta pregunta.
- **q-8172** (pioneers-and-popular-figures) Fui un filántropo antioqueño, viví en un castillo de Medellín que hoy es museo y le regalé a Itagüí su primera biblioteca. ¿Quién soy? → Diego Echavarría Misas: Verificación de datos: wrong. Hint 2 says he bought the castle in the 1940s and filled it with art. He did buy it, in about 1943. But he did not build it. Construction began in 1930 for José Tobón Uribe. The riddle and the answer are fine. The hint is true as written, so only the 'castle' phrasing needs checking. The riddle's 'viví en un castillo' is also correct.
- **q-8190** (regions-and-departments) ¿Cuál de estas maravillas naturales NO queda en el departamento del Guainía? → La serranía de Chiribiquete: Hint 3 says Chiribiquete is Colombia's largest national park. That is exactly what approved question q-0175 asks, so playing this question gives that one away. Replace hint 3 with another detail, such as its tepuis or its rock paintings, and leave out the "largest park" claim.
- **q-8213** (other-sports) En 2013, Cali organizó los Juegos Mundiales, con patinaje, squash y tiro de cuerda. ¿Qué tienen en común casi todos sus deportes? → No hacen parte de los Juegos Olímpicos: This is a new draft (existing is false) that asks "¿Qué tienen en común casi todos sus deportes?", a 'what do they have in common' question, and new drafts may not use that style (developer rule, 2026-10-21). The answer is also losing accuracy: squash joins the Olympics at LA 2028, and tug of war was an Olympic sport from 1900 to 1920. To keep the topic, ask a direct question about the 2013 World Games in Cali, without overlapping q-6932 or q-7114.
- **q-8223** (popular-and-andean-music) En la carranga de Jorge Velosa, el «merengue» no es el dulce de clara de huevo. ¿Qué es? → Un ritmo campesino: None of the candidates works: all four show string instruments (a tiple or guitar), and one wrong answer is literally "Un instrumento de cuerda", so the sharp illustrative image points to a wrong option. The slot needs a new search for something like "Boyacá countryside ruana" or "Colombian village fiesta". Also, hint 2 ("la gente lo baila en pareja") already gives the answer away, since only a rhythm gets danced. Hint 3 repeats it, so hint 2 should be vaguer. No se encontró una imagen adecuada para esta pregunta.
- **q-8232** (regions-and-departments) Mira la foto de los Llanos Orientales: ¿cómo se llama este tipo de paisaje? → Sabana: This asks the same thing as approved q-4571 ("What kind of landscape is shown here?" → Savanna): a photo of grassland, and you name the landscape type. Only the place changes (Llanos instead of Africa), and colombia-bundle players also get base questions, so seeing one gives the other away. Hint 3 even points back to the African savanna.
- **q-8235** (salsa-and-tropical-music) En las bandas de las sabanas de Córdoba, hay un ritmo en el que el bombero golpea el aro de madera del bombo y no el cuero. ¿Cuál es? → Porro palitiao: Hint 2 gives the answer away. "Es un porro" leaves only the two porro options, and "pero no el que apaga el cuero del bombo con la mano" then rules out porro tapao, so the answer is settled before hint 3. Hint 2 should instead give a vague clue, such as the San Pelayo festival or the Sinú region, that doesn't eliminate options.
- **q-8242** (telenovelas) En Bogotá, de recortar la palabra «compañero» salió «ñero». ¿Qué significa hoy esa palabra? → Una persona callejera y de modales bruscos: Hints 1 and 2 together give the answer away. Hint 2 ("Habla más de los modales que de la edad o del dinero") rules out the child and stingy options by naming them outright, and hint 1 ("No es precisamente un piropo") rules out "elegante". That leaves only the correct answer before hint 3. Hint 2 should be rewritten as a vague clue that doesn't name what the other options are about, for example something about where the word is heard.
- **q-8245** (rhythms-dances-and-instruments) ¿Qué distingue al paso caleño, el estilo de bailar salsa de Cali? → Pasos de pies muy rápidos: No candidate fits the salsa world: 1–5 are classical symphony orchestras, choirs and rehearsals, and 6 is a Balkan rock band (No Smoking Orchestra) on stage in St Petersburg. Re-search for something like "salsa dancers Cali" or "salsa band congas timbales", without footwork close-ups that hint at the answer. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 5, cause_effect 3, count 4, estimate 2, identify 15, made_of 13, name_concept 21, odd_one_out 7, origin 8, purpose 7, record 2, sequence 3, when 16, who 20, word_meaning 24
- stimulus: map_outline 1, none 133, photo 16
- clue: completion 7, direct 58, riddle 23, scenario 16, three_facts 46
- answer_kind: group 13, number 6, person 23, place 12, thing 27, time 17, word 52
- lens: body_senses 7, colombia 37, educational_media 10, everyday 24, history 16, language 15, nature 11, pop_culture 10, school 19, university 1

## Dropped by the pipeline

- 19th-century-4: overlap like q-7644: En el escudo de Colombia hay una granada abierta, con sus semillas rojas a la vista. ¿Qué recuerda? → El antiguo nombre del país, Nueva Granada: Antes de la Independencia, Colombia hacía parte de un virreinato con capital en Santafé y con nombre de ciudad andaluza. ¿Cuál? → El Virreinato de la Nueva Granada
- 19th-century-5: overlap like q-7349: En el mazamorreo, en los ríos de Antioquia y Chocó, se lava la arena en una batea de madera. ¿Qué se busca? → Oro: En los ríos del Chocó, los mineros mueven una batea con arena y agua: lo liviano se va y lo pesado queda al fondo. ¿Qué metal amarillo buscan? → Oro
- 19th-century-10: overlap like q-7962: Salí una mañana muy tieso y muy majo, con pantalón corto y sombrero encintado, aunque mi mamá me dijo que no saliera. ¿Quién soy? → Rinrín Renacuajo: Me puse sombrero, corbata y pantalón corto y salí sin permiso de mamá. Visité a mi amigo el ratón y a doña Ratona, y al final un pato me tragó. ¿Quién soy? → Rin Rin Renacuajo
- 19th-century-11: overlap like q-0119: ¿Cómo se llama la famosa novela romántica del colombiano Jorge Isaacs (1867)? → María: ¿En qué año publicó Jorge Isaacs «María», la historia de amor de Efraín y María en una hacienda del Valle del Cauca? → 1867
- 19th-century-14: overlap like q-5121: La telenovela «La Pola» contó la vida de Policarpa Salavarrieta. En el habla popular colombiana, ¿qué es una «pola»? → Una cerveza: Fue espía de los patriotas en Santafé y en 2010 una telenovela contó su vida con su apodo como título. ¿Cuál era el apodo de Policarpa Salavarrieta? → La Pola
- 19th-century-16: overlap like q-6928: ¿En qué símbolo patrio de Colombia aparece escrito el lema «Libertad y Orden»? → En el escudo: Completa el lema que aparece con el cóndor en el escudo de Colombia: «Libertad y…» → Orden
- banknotes-and-coins-1: overlap like q-7006: El billete colombiano de Gabriel García Márquez vale 50 000 pesos. ¿Cuántas lucas son? → 50: En Colombia, «una luca» son mil pesos. Si alguien te pide «diez lucas», ¿cuánta plata te está pidiendo? → 10 000 pesos
- banknotes-and-coins-7: overlap like q-1158: Me llaman 'el río de los cinco colores' y algunos meses del año mi fondo se pone rojo intenso. ¿Qué me pinta de ese color? → Una planta acuática: Estás en Caño Cristales, el río del billete azul de 2000, y ves el agua roja. ¿Qué le da ese color? → Plantas acuáticas
- banknotes-and-coins-12: overlap like q-5084: Esta pieza de oro es una de las más famosas del Museo del Oro de Bogotá. ¿Cómo se llama? → El Poporo Quimbaya: La vieja moneda de 200 pesos llevaba una figura del arte quimbaya. ¿En qué material son más famosas las piezas quimbayas, como su célebre poporo? → Oro
- banknotes-and-coins-13: overlap like q-7416: El billete de 20 000 pesos lleva la cara de Julio Garavito y un dibujo de la Luna, y un cráter lunar tiene su nombre. ¿Por qué? → Porque estudió el movimiento de la Luna: Fui matemático, ingeniero y astrónomo bogotano; un cráter de la Luna lleva mi nombre y salí en el viejo billete de 20 000. ¿Quién soy? → Julio Garavito
- brands-and-products-1: overlap like q-7689: Lo venden en carritos por la calle y viene de muchos colores. ¿Qué es un Bon Ice? → Un hielo de sabor en tubito: Empujo un carrito con congelador por calles y parques, voy uniformado y vendo tubitos de hielo de sabores que se chupan. ¿Quién soy? → Un vendedor de Bon Ice
- brands-and-products-8: overlap like q-5221: En Colombia, el chócolo se asa en la calle con mantequilla y sal, se usa para arepas dulces y no falta en el ajiaco. ¿Qué es? → La mazorca de maíz tierno: El nombre de los Choclitos viene de «choclo», que en Colombia es… → Una mazorca de maíz tierno
- brands-and-products-12: overlap like q-7138: En una tienda de barrio en Colombia pides una Jumbo. ¿Qué te entregan? → Una chocolatina con maní: La chocolatina Jet es a chocolate con leche como la chocolatina Jumbo es a chocolate con… → Maní
- club-football-0: overlap like q-6690: I'm small enough to hold in your hand. When a boat is in trouble, I'm lit and I shoot a bright red light into the sky so rescuers can find it. What am I? → A flare: En la tribuna, la barra las prende y las sostiene en la mano: echan una luz roja muy fuerte, mucho humo y en los estadios colombianos están prohibidas. ¿Qué son? → Bengalas
- club-football-10: overlap like q-0496: ¿Qué futbolista es? Era un volante colombiano con una enorme melena rubia y crespa, famoso por sus pases mágicos y por jugar casi sin correr. → Carlos Valderrama: ¿Qué futbolista colombiano, de melena rubia y crespa, hizo famoso el número 10 en Junior y en la Selección Colombia? → Carlos «el Pibe» Valderrama
- crafts-and-traditional-dress-11: overlap like q-7327: Las mujeres emberá chamí de Risaralda tejen collares anchos con figuras de colores, llamados okama. ¿De qué están hechos? → De chaquiras: Mira de cerca: estos collares anchos de chaquira los hace un pueblo indígena del Chocó, Antioquia y Risaralda. ¿Cuál? → Los emberá
- fruits-1: overlap like q-7213: La huelga de los trabajadores bananeros de 1928 terminó en una plaza junto a la estación del tren. ¿En qué población del Magdalena? → Ciénaga: La Zona Bananera queda entre la Ciénaga Grande y la Sierra Nevada, y sus plantaciones inspiraron las de Macondo. ¿En qué departamento está? → Magdalena
- fruits-13: overlap like q-0327: En Colombia, ¿qué te piden cuando te dicen «no dé papaya»? → Que no te descuides ni des ventaja: En Colombia te advierten: «No des papaya». ¿Qué te están aconsejando? → Que no dejes que otros se aprovechen de ti
- ghosts-and-creatures-2: overlap like q-7331: Mira esta figura tallada en piedra. ¿Qué es? → Una estatua de San Agustín: En un parque de Colombia hay cientos de estatuas de piedra con colmillos de jaguar, cerca de donde nace el río Magdalena. ¿Dónde están? → San Agustín
- ghosts-and-creatures-4: overlap like q-0117: ¿En qué pueblo imaginario transcurre 'Cien años de soledad'? → Macondo: En una novela colombiana, el fantasma de un hombre muerto de un lanzazo tras una pelea de gallos persigue a su asesino, que huye y funda un pueblo. ¿Cuál? → Macondo
- ghosts-and-creatures-6: overlap like q-7463: A muchos bebés colombianos les ponen una pulserita con un azabache contra el mal de ojo. ¿Qué es el azabache? → Una piedra negra: Muchas abuelas colombianas le ponen al bebé una manilla roja en la muñeca, a veces con una pepita negra de azabache. ¿Para qué? → Para protegerlo del mal de ojo
- ghosts-and-creatures-11: overlap like q-7049: Según la tradición popular, si rocías agua bendita en los rincones de la casa, ¿quiénes salen corriendo? → Las brujas: Se dejan abiertas en forma de cruz debajo de la almohada o detrás de la puerta: dicen que la cruz y el metal las espantan. ¿A quiénes ahuyentan las tijeras? → A las brujas
- ghosts-and-creatures-17: overlap like q-8090: En un refrán, todo lo que sé lo aprendí más por viejo que por malo. ¿Quién soy? → El diablo: Completa lo que dicen en Colombia de alguien con una suerte demasiado buena para ser verdad: «Ese tiene pacto con el…». → diablo
- hosts-actors-and-comedians-9: overlap like q-7759: ¿Qué actor fue Pedro Coral Tavera en «Pedro el escamoso»? → Miguel Varoni: Estás viendo una repetición de «Pedro el escamoso», con su famoso baile. ¿Qué actor hace de Pedro Coral? → Miguel Varoni
- indigenous-myths-and-folk-beliefs-0: overlap like q-0534: Pasar debajo de una escalera, que se te cruce un gato negro y abrir un paraguas dentro de la casa: ¿qué tienen en común? → Según las supersticiones, traen mala suerte: Es un agüero muy común en Colombia: mucha gente da la vuelta para no pasar debajo de una escalera recostada en la pared. ¿Qué dicen que trae pasar por debajo? → Mala suerte
- indigenous-myths-and-folk-beliefs-5: overlap like q-3204: This mural shows Jesus' last meal with his twelve apostles. Which apostle later betrayed him? → Judas: Se te riega la sal en la mesa y alguien dice «¡mala suerte!». Una explicación popular lo liga a «La última cena» de Leonardo, donde un apóstol tumba el salero. ¿Cuál? → Judas
- indigenous-myths-and-folk-beliefs-12: overlap like q-0483: Según la leyenda, ¿a quién busca la Llorona cuando anda de noche, llorando cerca de los ríos? → A sus hijos: En el campo cuentan que de noche, junto a las quebradas, se oye a una mujer vestida de blanco que gime sin parar. ¿Quién es? → La Llorona
- indigenous-myths-and-folk-beliefs-13: overlap like q-0534: Pasar debajo de una escalera, que se te cruce un gato negro y abrir un paraguas dentro de la casa: ¿qué tienen en común? → Según las supersticiones, traen mala suerte: Las abuelas dicen que trae mala suerte, aunque esté lloviendo a cántaros y quieras secarlo. ¿Dónde no se debe abrir un paraguas? → Dentro de la casa
- indigenous-myths-and-folk-beliefs-15: overlap like q-0913: Se te cae el espejo del baño y se rompe en pedazos. Según la famosa superstición, ¿cuántos años de mala suerte te esperan? → 7: Se te cae el espejo del baño y se rompe en mil pedazos. Según el agüero, ¿qué te espera? → Siete años de mala suerte
- national-symbols-7: overlap like q-7283: Cuando el Gobierno declara duelo nacional, la bandera se iza así, sin llegar a lo más alto. ¿Cómo se dice? → A media asta: Antes fui un árbol del bosque o un tubo de metal; soy largo y derecho, y en cada izada la bandera sube por mí con una cuerda. ¿Qué soy? → El asta
- national-symbols-8: overlap like q-7607: Antes de llegar a tu taza como un tinto, el café fue una cereza roja. ¿Dónde creció? → En un cafetal: Es caliente, se sirve en pocillo y los adultos lo piden en la panadería por la mañana: un tinto. ¿De qué está hecho? → De café
- national-symbols-9: overlap like q-5015: ¿Qué día celebramos el Grito de Independencia de Colombia? → 20 de julio: El 25 de diciembre es a la Navidad como el 20 de julio es al… → Grito de Independencia
- national-symbols-16: overlap like q-7235: Según la tradición, Santa Fe de Bogotá nació en el Chorro de Quevedo. ¿De dónde viene la palabra «Bogotá»? → De Bacatá, el nombre muisca de la región: Es una plazoleta de La Candelaria, hoy llena de cuenteros y artistas, y la tradición dice que allí se fundó Bogotá en 1538. ¿Cuál es? → El Chorro de Quevedo
- national-team-3: overlap like q-7659: Tengo páginas de animales, planetas y paisajes, y me llenan con láminas que salen dentro de una chocolatina. Los niños cambian las repetidas en el recreo. ¿Qué soy? → El álbum de Jet: Abres un sobre de monas del álbum del Mundial y sale una que ya pegaste. Para cambiarla, dices que es una mona… → repetida
- natural-parks-and-ecosystems-4: overlap like q-8078: La cascada La Chorrera, en Choachí (Cundinamarca), es considerada la más alta de Colombia. ¿Más o menos cuánto mide? → Unos 590 metros: Escucha: en La Chorrera, cerca de Bogotá, este sonido no para nunca. ¿Qué lo produce? → Una cascada
- natural-parks-and-ecosystems-5: overlap like q-2617: Who uses a small brush like this to free old objects from the ground? → Archaeologist: Estatuas de piedra como esta, de San Agustín en el Huila, tienen siglos de antigüedad. ¿Qué científicos las estudian? → Los arqueólogos
- other-sports-15: overlap like q-0378: ¿Qué municipio colombiano es famoso como la capital de los deportes de aventura? → San Gil: Se practica con arnés, casco y cuerdas, en Santander es famoso en Juan Curí y uno termina empapado. ¿Qué es el torrentismo? → Bajar por una cascada colgado de una cuerda
- painters-sculptors-and-museums-7: overlap like q-7485: Mira la foto: esta estatua de Bolívar, de 1846, es el monumento público más antiguo de Bogotá. ¿De qué material está hecha? → Bronce: Vive en el Parque Berrío de Medellín, todos le dicen «la Gorda Gertrudis» y es una escultura de Fernando Botero. ¿De qué material está hecha? → Bronce
- pioneers-and-popular-figures-2: overlap like q-5097: Soy de Medellín, me dicen «Pretty Boy», y en 2020 le canté a una ex que presumía su viaje a «Hawái». ¿Quién soy? → Maluma: ¿Quién es este cantante colombiano? → Maluma
- pioneers-and-popular-figures-3: overlap like q-7588: Si te ríes con 'La pelota de letras', de Andrés López, ¿la infancia de quiénes estás recordando? → De quienes crecieron en los años 70 y 80: ¿Qué humorista es considerado el pionero del stand-up comedy en Colombia, famoso por «La pelota de letras»? → Andrés López
- pioneers-and-popular-figures-5: overlap like 19th-century-11: ¿En qué año publicó Jorge Isaacs «María», la historia de amor de Efraín y María en una hacienda del Valle del Cauca? → 1867: La novela romántica más famosa de Colombia cuenta el amor de María y Efraín en una hacienda. ¿En qué región pasa la historia? → El Valle del Cauca
- plants-and-flowers-3: overlap like q-5141: Este paisaje con frailejones sale en el billete de 5000. ¿Por qué es tan importante para ciudades como Bogotá? → Porque guarda y da el agua que toman: Mira la foto: en este lugar frío de montaña nacen muchos ríos de Colombia y por eso le dicen «fábrica de agua». ¿Qué es? → Un páramo
- plants-and-flowers-4: overlap like q-7426: Estás en el valle de Cocora, frente a la palma de cera, el árbol nacional de Colombia. ¿Hasta qué altura puede llegar? → Unos 60 metros: Es el árbol nacional de Colombia, puede pasar los 50 metros de alto y abunda en el Valle de Cocora. ¿Cuál es? → La palma de cera
- plants-and-flowers-7: overlap like q-5013: ¿Cómo se llama la sopa bogotana de pollo, tres clases de papa, mazorca y guascas? → El ajiaco: Mira esta hierba: son guascas. ¿En qué sopa bogotana no pueden faltar? → El ajiaco
- poetry-and-childrens-stories-5: overlap like 19th-century-10: Me puse sombrero, corbata y pantalón corto y salí sin permiso de mamá. Visité a mi amigo el ratón y a doña Ratona, y al final un pato me tragó. ¿Quién soy? → Rin Rin Renacuajo: Vivo en la charca y mi hijo es el renacuajo más famoso de Colombia: salió de paseo muy elegante y el paseo le salió muy mal. ¿Quién soy? → Mamá Rana
- poetry-and-childrens-stories-12: overlap like q-7951: Completa la ronda: «Juguemos en el bosque mientras el … no está». → Lobo: Mientras ustedes juegan en el bosque, yo me pongo los pantalones, la camisa y el sombrero… y cuando estoy listo, ¡salgo a atraparlos! ¿Quién soy? → El lobo
- pop-rock-and-urban-music-12: overlap like pioneers-and-popular-figures-13: ¿Qué cantante colombiano canta «La camisa negra» y «A Dios le pido»? → Juanes: Este cantante paisa de guitarra eléctrica es famoso por «La camisa negra». ¿Quién es? → Juanes
- popular-and-andean-music-10: overlap like q-0420: Mira la foto: ¿cómo se llaman estos campesinos que desfilan en Medellín cargando enormes arreglos de flores en la espalda? → Silleteros: El Festival Folclórico y Reinado Nacional del Bambuco se celebra cada junio en Neiva. ¿Cuál de estas cosas NO hace parte de él? → El desfile de silleteros
- popular-and-andean-music-11: overlap like q-7405: Grupo Niche le cantó a Cali «pachanguero», pero la pachanga es un ritmo de finales de los años 50. ¿De qué país viene? → Cuba: Es un ritmo andino colombiano lento y romántico, se escribe en compás de 2/4 y desciende de la habanera. ¿De qué país viene su origen? → Cuba
- popular-and-andean-music-13: overlap like q-7061: El 31 de diciembre se rellena un muñeco con ropa vieja y aserrín, y a la medianoche se le prende fuego. ¿Qué se dice que se quema con él? → Lo malo del año que termina: El 31 de diciembre, en muchos barrios de Colombia se arma un muñeco con ropa vieja y careta para quemarlo. ¿Con qué se rellena tradicionalmente? → Aserrín, papel y trapos
- regional-speech-2: overlap like q-6887: En el departamento resaltado en este mapa tratan de «usted» hasta a los hijos y a la pareja, con un tono fuerte y directo. ¿Cuál es? → Santander: ¿De qué departamento colombiano es famoso el «hablado golpeado», que suena a regaño aunque la persona esté feliz? → Santander
- regional-speech-10: overlap like q-6967: La chirimía con clarinete, bombardino, redoblante, bombo y platillos es la banda típica de un departamento del Pacífico. ¿Cuál? → Chocó: Estás en las fiestas de San Pacho en Quibdó y llega la chirimía. ¿Qué es? → Un grupo de músicos con clarinetes y tambores
- regional-speech-16: overlap like q-7597: Oyes a alguien decir «¡ajá!» a cada rato, al estilo costeño. ¿En cuál de estas ciudades sería MENOS típico? → Pasto: En tres de estas ciudades, cuando algo sale mal, la gente dice «¡qué pava!». ¿En cuál NO es común? → Pasto
- regional-speech-17: overlap like q-5229: A Pedro Coral Tavera lo apodaban «el escamoso». En Colombia, ser escamoso es… → Presumir y aparentar más de lo que uno es: Completa: en Bogotá, «chicanear» es lo mismo que… → Presumir
- regions-and-departments-5: overlap like q-6805: ¿En qué mes se celebran tradicionalmente las famosas corralejas de Sincelejo, en Sucre? → Enero: Montería es a Córdoba como Sincelejo es a… → Sucre
- regions-and-departments-11: overlap like q-0583: En la isla de San Andrés, el pueblo raizal habla creole. ¿De qué idioma viene la mayoría de las palabras de esa lengua? → Inglés: Son el pueblo nativo de San Andrés, Providencia y Santa Catalina, hablan un creole de base inglesa y muchos son protestantes. ¿Cómo se llaman? → Los raizales
- brands-and-products-0: fact-check wrong: Hint 3 is false: Brisa belongs to Bavaria (AB InBev), not to the Coca-Cola bottler in Colombia (Coca-Cola FEMSA). The answer itself is right.: Agua Cristal es una marca de Postobón. ¿Cuál de estas bebidas NO es de Postobón? → Agua Brisa
- crafts-and-traditional-dress-2: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: En el traje del cumbiambero no falta una pañoleta roja. ¿Qué es esa pañoleta? → Un pañuelo anudado al cuello
- crafts-and-traditional-dress-14: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 4: El arriero paisa lleva un poncho de tela delgada doblado sobre el hombro. ¿Para qué lo usa? → Para secarse el sudor y cubrirse del sol
- indigenous-myths-and-folk-beliefs-7: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Dicen que al bebé le dio mal de ojo: llora sin parar, no quiere comer y está decaído. Según la creencia, ¿qué se lo causó? → Una mirada fuerte o envidiosa
- national-symbols-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La bandera del departamento de Caldas no tiene escudo ni estrellas. ¿Cuántas franjas horizontales tiene? → 2
- national-team-2: overlap like q-8004: Por sus colores, la bandera de Colombia tiene un apodo que también usa la Selección. ¿Cuál es? → La Tricolor: Los narradores le dicen «la Tricolor» a la Selección Colombia. ¿De dónde sale ese apodo? → De los colores de la bandera
- painters-sculptors-and-museums-13: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: El Museo de los Niños de Bogotá fue pensado para que los más pequeños aprendieran ciencia. ¿Qué podías hacer allí con casi todas las exhibiciones? → Tocarlas y jugar con ellas
- pioneers-and-popular-figures-0: overlap like q-8162: En 2018, Caterine Ibargüen se convirtió en la primera colombiana en recibir un gran premio internacional. ¿Cuál? → Atleta Mundial del Año: ¿Cuál de estos deportistas colombianos NO es ciclista? → Caterine Ibargüen
- pioneers-and-popular-figures-8: overlap like q-7438: ¿En qué año ganó Egan Bernal el Tour de Francia? → 2019: Egan Bernal, criado en Zipaquirá, ganó el Tour de Francia 2019 y llegó a París con la camiseta del líder. ¿Cómo se llama? → El maillot amarillo
- pioneers-and-popular-figures-13: overlap like pop-rock-and-urban-music-12: Este cantante paisa de guitarra eléctrica es famoso por «La camisa negra». ¿Quién es? → Juanes: ¿Qué cantante colombiano canta «La camisa negra» y «A Dios le pido»? → Juanes
- poetry-and-childrens-stories-0: hard fail: correct 5, unambiguous 4, no_giveaway 1, no_overlap 5: Recitas rapidito «El cielo está enladrillado, ¿quién lo desenladrillará?». En el trabalenguas, ¿de qué está cubierto el cielo? → De ladrillos
- pop-rock-and-urban-music-10: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: Gané un Grammy Latino en la primera ceremonia, en el año 2000, y en 2025 me llevé un Grammy por un álbum de desamor. ¿Quién soy? → Shakira
- rhythms-dances-and-instruments-15: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Es la fiesta popular de la Costa donde, de noche, las parejas bailan en rueda alrededor de los músicos. ¿Cómo se llama? → Cumbiamba
- salsa-and-tropical-music-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En Monterrey, unos jóvenes con peinados extravagantes y ropa ancha bailan cumbia rebajada; la película «Ya no estoy aquí» los retrata. ¿Cómo les dicen? → Los kolombianos
- telenovelas-0: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: En la serie «Celia» (2015), sobre la vida de Celia Cruz, ¿qué actriz y cantante colombiana hizo de Celia joven? → Jeimy Osorio
- rhythms-dances-and-instruments-8: overlap like q-8175: Soy mujer del Pacífico colombiano: en los arrullos llevo la voz principal y las demás me responden en coro, al son del cununo. ¿Qué soy? → Una cantaora: En el Pacífico colombiano, es la mujer que lleva la voz en el currulao, canta arrullos y alabaos y suele tocar el guasá. ¿Cómo se le llama? → Cantaora
- rhythms-dances-and-instruments-12: overlap like q-6953: Emiliano Zuleta la compuso, Carlos Vives la hizo famosa en 1993 y en ella se burla de Lorenzo Morales. ¿De qué nació 'La gota fría'? → De una piquería: Nací en La Guajira y, en una pelea musical con Lorenzo Morales, compuse «La gota fría», que Carlos Vives llevó al mundo. ¿Quién soy? → Emiliano Zuleta
- rhythms-dances-and-instruments-13: overlap like q-7466: Mira este cuatro, el instrumento del joropo llanero. ¿A qué grupo de instrumentos pertenece? → De cuerda: Mira este instrumento. ¿De qué región de Colombia es típico? → Los Llanos Orientales
- salsa-and-tropical-music-0: overlap like q-6945: La flauta de millo se toca de lado y su lengüeta se corta en la misma caña. ¿Qué es el millo? → Una planta parecida al sorgo: Tiene cuatro huecos, se toca de lado y es el pito que suena en las cumbias de Totó la Momposina. ¿De qué está hecho? → Del tallo de una planta delgada
- salsa-and-tropical-music-3: overlap like q-0479: ¿En qué mes se celebra la Feria de Cali, con su famoso desfile de bailarines de salsa? → Diciembre: La Feria de Cali arranca cada año con el desfile del Salsódromo. ¿Qué día festivo es ese? → El día de Navidad
- salsa-and-tropical-music-11: overlap like q-6947: En el Festival Nacional del Porro de San Pelayo, Córdoba, compiten bandas sabaneras. ¿Qué instrumentos las forman? → Clarinetes, trompetas, bombo y platillos: Tocan con clarinetes, trompetas y bombardinos, animan corralejas y fandangos, y su ritmo rey es el porro. ¿De qué región son estas bandas? → De las sabanas de Córdoba y Sucre
- scientists-and-inventors-3: overlap like q-5008: Estás viendo las miles de láminas de flores pintadas a mano por la Real Expedición Botánica. ¿Quién dirigió esa expedición? → José Celestino Mutis: Te sirven una aromática de té de Bogotá, la planta que en el siglo XVIII se quiso vender como reemplazo del té de China. ¿Qué sabio la promovió? → José Celestino Mutis
- scientists-and-inventors-9: overlap like q-4465: I have a round ceiling, and when my lights go out, a machine paints stars and planets across it, even at noon. What am I? → A planetarium: Tengo una cúpula donde aparecen estrellas y planetas aunque afuera sea de día, y en Medellín llevo el nombre de Jesús Emilio Ramírez. ¿Qué soy? → Un planetario
- scientists-and-inventors-11: overlap like q-2738: This striped mosquito spreads a disease also called “breakbone fever”. What is it? → Dengue: Este zancudo de patas rayadas de blanco pica de día y transmite el dengue en ciudades como Cali y Barranquilla. ¿Cuál es? → El Aedes aegypti
- telenovelas-17: overlap like q-8103: ¿En qué año estrenó Caracol «Escobar, el patrón del mal», con Andrés Parra como protagonista? → 2012: Soy actor colombiano. En 2017 interpreté a Hugo Chávez en la serie «El comandante», y antes protagonicé una famosa súper serie de Caracol. ¿Quién soy? → Andrés Parra
- vallenato-6: overlap like q-7131: El río Cesar le da nombre a un departamento y desemboca en la ciénaga de Zapatosa. ¿Dónde nace? → En la Sierra Nevada de Santa Marta: Me llamo igual que un río que baja de la Sierra Nevada y que un famoso gobernante romano, y mi capital es Valledupar. ¿Qué departamento soy? → Cesar
- vallenato-9: overlap like q-5019: Este cantante de Santa Marta mezcló el vallenato con rock y pop en los años 90. ¿Quién es? → Carlos Vives: Mira la foto: ¿quién es este cantante samario que grabó «La tierra del olvido» en 1995? → Carlos Vives
- vallenato-16: overlap like q-6957: Un pelado dice: «El domingo me toca almorzar con los cuchos». ¿Con quiénes va a almorzar? → Con sus papás: En la costa le dicen «pelao» a un muchacho, y se oye en muchos vallenatos. ¿De qué palabra viene «pelao»? → Pelado
