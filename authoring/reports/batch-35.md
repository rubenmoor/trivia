# batch-35

Made by `qgen batch` on 2026-11-05 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: mexico
- Language: Spanish (Latin America)
- Subcategories (29): folk-beliefs, mariachi-and-ranchera, regional-mexican, pop-and-rock, traditional-dances, painters-and-muralists, writers-and-poets, comics, golden-age-cinema, contemporary-cinema, telenovelas, chespirito, liga-mx, national-team, lucha-libre, boxing, other-sports, slang, indigenous-words, money, brands-and-snacks, transport, school-and-services, home-and-street, national-symbols, state-symbols, tv-shows-and-hosts, childrens-songs, sayings
- Merged: 286 (q-11426…q-11711)
- Approved: 263
- Needs work: 23
- Dropped by the pipeline: 63
- Reviewed by: claude-opus-5-5
- Claude calls: 625, about $78.04 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-33, batch-34; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-33 | batch-34 | batch-35 |
|---|---|---:|---:|---:|
| source locale |  | de | es-ES | es |
| drafts |  | 375 | 368 | 349 |
| skipped slots |  | 111 | 118 | 173 |
| dropped |  | 54 | 61 | 63 |
| drop rate | ≤ 20.0 % | 14.4 % ✓ | 16.6 % ✓ | 18.1 % ✓ |
| dropped: hard fail correct |  | 8 | 3 | 0 |
| dropped: hard fail unambiguous |  | 3 | 0 | 2 |
| dropped: hard fail no_giveaway |  | 28 | 15 | 21 |
| dropped: overlap |  | 19 | 42 | 41 |
| dropped: duplicate |  | 0 | 1 | 0 |
| dropped: fact-check wrong |  | 1 | 1 | 0 |
| merged |  | 321 | 307 | 286 |
| approved |  | 295 | 282 | 263 |
| needs_work |  | 26 | 25 | 23 |
| needs_work rate | ≤ 20.0 % | 8.1 % ✓ | 8.1 % ✓ | 8.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.9 % ✓ | 2.6 % ✓ | 2.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.6 % ✓ | 0.7 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.6 % ✗ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 3.7 % ✓ | 4.9 % ✓ | 3.8 % ✓ |
| media: no pick in review 1 |  | 45 | 51 | 45 |
| media: recovered by research |  | 39 | 39 | 38 |
| media: no pick at record |  | 6 | 12 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 6.4 % ✓ | 11.7 % ✓ | 12.3 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 72.8 % ✓ | 70.6 % ✓ | 45.9 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.55 ✗ | 1.00 ✓ | 0.82 ✓ |
| approved 11–15 |  | 67 | 63 | 45 |
| top move | ≤ 25.0 % | 17.4 % ✓ | 17.6 % ✓ | 19.9 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 92.5 % | 89.6 % | 95.1 % |
| values stimulus |  | 3 | 5 | 3 |
| top clue | ≤ 60.0 % | 37.7 % ✓ | 42.0 % ✓ | 36.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 27.4 % ✓ | 23.5 % ✓ | 25.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.9 % ✓ | 19.9 % ✓ | 23.4 % ✓ |
| values lens |  | 9 | 9 | 9 |
| media share | 15.0 %–50.0 % | 7.5 % ✗ | 10.4 % ✗ | 4.9 % ✗ |
| mean fun | ≥ 3.40 | 3.53 ✓ | 3.43 ✓ | 3.44 ✓ |
| cost $ |  | $80.73 | $78.33 | $75.28 |
| $ per approved | ≤ $0.35 | $0.27 ✓ | $0.28 ✓ | $0.29 ✓ |
| calls |  | 591 | 570 | 565 |
| calls per approved |  | 2.00 | 2.02 | 2.15 |
| wall time h |  | 3.07 | 2.96 | 2.80 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 4 (1 major), overlap 1 (0 major), media 3 (1 major), difficulty 1 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.76

Major findings on approved questions:

None.

## Needs work

- **q-11429** (boxing) Completa la frase que viene del box y usamos cuando alguien se rinde: "Ya no puedo más, voy a tirar la…" → Toalla: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-11436** (brands-and-snacks) El Lucas Gusano es un dulce en una botellita que aprietas para que salga. ¿Qué trae adentro? → Chamoy enchilado: The fact check marks the fun fact as wrong: it says Mars has owned Lucas since 2004, while the check's sources put the purchase in 2001 (2004 is the year of the lead-contamination case). I can't settle the year myself. Correct the year after checking it, or drop the year from the fun fact. Verificación de datos: wrong. The fun fact says Lucas has belonged to Mars since 2004. Sources date the purchase to 2001. 2004 is the year of the lead-contamination issue.
- **q-11440** (brands-and-snacks) Mira la foto: chiles en vinagre, como los que vienen en lata. ¿Qué tipo de chile es el más usado para hacerlos? → El jalapeño: None of the candidates shows pickled jalapeño slices, and the question says "Mira la foto: chiles en vinagre". #1 is roast chicken with carrots and onion, #2 is jars of pink pickled onions or radish, #3 is a jar of pickled onion on a restaurant table. A new search isn't allowed here, so the slot needs a real photo of jalapeños en escabeche (e.g. "pickled jalapeño slices"). Another option is to drop "Mira la foto" and make the image illustrative. No se encontró una imagen adecuada para esta pregunta.
- **q-11445** (chespirito) Lo grita el Profesor Jirafales y cada vez sube más la voz hasta el último «¡taaa!». ¿Qué siente cuando dice «¡Ta ta ta ta!»? → Enojo: Verificación de datos: uncertain. The answer (enojo) fits. I couldn't verify the fun fact that he often ended the "ta ta ta" with a foot stomp.
- **q-11446** (chespirito) Sale después de un golpe, se levanta en la cabeza y el Chapulín Colorado le puso su nombre a su martillo. ¿Qué es un «chipote»? → Un chichón: All six candidates are ice-hockey photos (players, rinks, the Stanley Cup). None has anything to do with a bump on the head, an ice pack or the Chapulín's world, so even a blurred decorative image doesn't fit. A new search isn't allowed, so the slot needs a new search by hand, for example "ice pack on forehead" or "toy squeaky hammer". No se encontró una imagen adecuada para esta pregunta.
- **q-11464** (comics) Muchos luchadores mexicanos, como El Santo, pasaron casi toda su carrera sin quitarse la máscara. ¿Para qué la usaban? → Para mantener en secreto quiénes eran: Hint 2 ("Como los superhéroes que no quieren que sepan su nombre") restates the answer, so it gives it away before hint 3. Hint 3 ("Nadie debía ver su verdadero rostro") is actually weaker than hint 2, so the hints don't build from vague to strong. Fix: make hint 2 vaguer (for example about a luchador's life outside the ring) and keep the near-answer for hint 3.
- **q-11473** (folk-beliefs) En muchas casas y negocios de México hay una figurita de elefante con la trompa hacia arriba. Según la creencia, ¿qué atrae? → El dinero y la abundancia: The fun fact contradicts itself: an elephant "de espaldas a la puerta" can't be "como si «recibiera» lo que entra". Sources disagree on which way it should face, and the fact check is uncertain. Rewrite the fun fact without the door direction, or have it face the door to "receive" good luck. Keep only the trunk-up detail if you're unsure. Verificación de datos: uncertain. The answer (money and abundance) is fine, but the fun fact contradicts itself. An elephant with its back to the door can't 'receive' what comes in. Folk tradition usually says it should face the door, and sources disagree. The 'history' lens also looks odd for this question.
- **q-11494** (liga-mx) Terminó el Apertura en diciembre y en enero arranca el otro torneo de la temporada de la Liga MX. ¿Cómo se llama? → Clausura: Related draft q-11495 (Matías Almeyda) literally says "la final del Clausura", so a player who sees it first gets this question's answer for free. Reword q-11495 (e.g. "la final del torneo de 2017" or "la final de liga de 2017") and this question can go in as it is.
- **q-11507** (mariachi-and-ranchera) ¿Qué cantante, conocido como «El Lujo de México», fue la primera voz de Los Tres Ases? → Marco Antonio Muñiz: The question says Marco Antonio Muñiz was the "primera voz" of Los Tres Ases. The fact check marks this wrong: Juan Neri was the trio's first voice, requinto player and director, and Muñiz sang third and lead voice until 1960. Reword it to say he was a member of Los Tres Ases before going solo, for example "¿Qué cantante, conocido como «El Lujo de México», integró el trío Los Tres Ases antes de su carrera solista?". Verificación de datos: wrong. The question says Muñiz was the first voice (primera voz) of Los Tres Ases. Juan Neri was the first voice, requinto player and director. Muñiz joined in the 1950s, sang third and lead voice, and left in 1960 to go solo.
- **q-11531** (national-team) Jorge Campos fue portero y también delantero, medía cerca de 1,68 metros y diseñaba sus uniformes fosforescentes inspirado en el surf. ¿De qué ciudad es? → Acapulco: Hint 1 ("Es una ciudad de playa") gives the answer away: Acapulco is the only coastal city among the options, since Guadalajara, Monterrey and Mérida are all inland. The surf clue in the question already points the same way. Hint 1 needs a clue that doesn't tell the coastal city apart, and ideally one wrong answer should be a beach city (e.g. Mazatlán or Cancún) so the surf clue doesn't rule out the other three.
- **q-11571** (traditional-dances) ¿Qué danza de la Sierra Norte de Puebla es famosa por terminar con cuatro danzantes girando en una gran cruz de madera vertical, como rueda de la fortuna? → La danza de los Huahuas: Verificación de datos: uncertain. I did not search for this one. From memory, the Huahuas dance of Cuetzalan ends on a rotating cross, but I could not verify that detail or the hints.
- **q-11574** (transport) ¿Cómo se llama esta parte de la estación del Metro? → El andén: None of the four image candidates shows a metro platform. 1 and 2 are animated railway maps of French departments, and 3 and 4 are ESA satellite views of New Orleans and the Mississippi delta. The essential image has to be a clear photo of an empty CDMX Metro platform, with no train and no 'andén' sign. Another search isn't allowed here, so the image needs to be found by hand (try something like 'Metro CDMX andén' or 'Mexico City Metro station platform' on Commons). No se encontró una imagen adecuada para esta pregunta.
- **q-11583** (comics) Completa: en México, a quien dibuja historietas y caricaturas en el periódico se le llama «___». → monero: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-11590** (contemporary-cinema) Estás viendo «El laberinto del fauno»: ¿cuántas pruebas le pide el fauno a Ofelia antes de la luna llena? → 3: The text is fine (three tasks: the toad, the Pale Man's key and the brother's blood; the Doug Jones fact is correct), but none of the media candidates shows a stone labyrinth or anything from the film's world, and no new search is allowed. The slot needs a new search, for example "stone hedge labyrinth" or "old stone maze garden". No se encontró una imagen adecuada para esta pregunta.
- **q-11593** (folk-beliefs) En muchos negocios de México cuelgan una herradura de la suerte con la imagen de un santo para que lleguen clientes. ¿Qué santo es? → San Martín Caballero: The text is fine, but none of the image candidates works. 1–4 show a French château, a heron and English weirs. 6 is a Moscow garage plaque. 5 does show a horseshoe, but it's on the Route 91 shooting memorial in Las Vegas, with a US flag and a Chicago fire badge, which doesn't fit the topic or the tone. No new search is allowed, so this needs a manual media search, e.g. "San Martín Caballero herradura" or "Mexican shop horseshoe amulet". No se encontró una imagen adecuada para esta pregunta.
- **q-11616** (other-sports) Ernesto Canto fue campeón mundial en 1983, rompió el récord mundial en 1984 y ese año ganó oro en Los Ángeles. ¿En qué prueba? → Marcha de 20 km: Hint 2 gives the answer away. It says another Mexican won gold in "a longer distance of the same event", and among the options only the walk comes in two distances. So hint 2 rules out the marathon and the 10 000 m, and it also tells players Canto's race was the shorter one: the 20 km. Hint 2 should be replaced with a vaguer clue, for example about the 1983 Helsinki world title or Mexico's walking tradition, and should not mention a longer version of his event.
- **q-11621** (pop-and-rock) ¿Con qué apodo conocen a la cantante Lucero desde hace décadas? → La Novia de América: Hint 1 says outright that «La Chica Dorada» is Paulina Rubio, which is the fact draft q-11546 asks for ("…me dicen “La Chica Dorada”. ¿Quién soy?" → Paulina Rubio). So this question gives away that one. Replace hint 1 with a vague hint that doesn't name any other singer's nickname, for example one about how long Lucero has carried the nickname or her career as a child star.
- **q-11636** (slang) Sus chistes se cuentan en todo México, pasan de abuelos a nietos y casi siempre lo meten en problemas. ¿Quién es Pepito? → Un niño travieso de la escuela: Every candidate is a school classroom with a chalkboard, which points straight at the answer "Un niño travieso de la escuela", even blurred. None of the other options (dog, grandpa, clown) has anything to do with a classroom. The slot needs a neutral decorative image, such as a family get-together or people laughing, and no new search was allowed this round. No se encontró una imagen adecuada para esta pregunta.
- **q-11650** (school-and-services) Los graduados me eligen, casi siempre entre sus maestros. Salgo en la invitación, en la foto del grupo y en la ceremonia. ¿Quién soy? → El padrino de generación: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-11652** (school-and-services) ¿Qué producto vende Liconsa a bajo precio a millones de familias mexicanas? → Leche: Hint 2 ("Es buena para los huesos de los niños") gives the answer away among tortillas, frijol and huevo, because calcium for bones is milk's defining trait. Replace it with a vaguer clue, for example about the government programme or who can sign up for it. Also worth checking: in 2025 Liconsa was rebranded as "Leche para el Bienestar". Consider mentioning that, or wording the question so it doesn't depend on the current brand name.
- **q-11670** (state-symbols) Mira el contorno de este estado: su equipo de béisbol son los Pericos. ¿Qué estado es? → Puebla: The essential image must be a plain outline of the state of Puebla, but no candidate shows one, and I can't search again. The candidates are city photos (cathedral, fountain, bus, park), an old city map labelled 'PUEBLA', and a black satellite tile. Either find a plain outline of the state of Puebla (e.g. 'Puebla state outline blank'), or drop the outline from the wording and use an illustrative image, since the Pericos clue already carries the question. No se encontró una imagen adecuada para esta pregunta.
- **q-11696** (tv-shows-and-hosts) La Chilindrina, de «El Chavo del 8», es hija de don Ramón, tiene pecas y se peina con dos coletas. ¿Qué lleva siempre en la cara? → Unos lentes: Hint 1 ("Es algo que se usa para ver mejor") gives the answer away: of the four options only the glasses help you see. Hint 2 ("tienen armazón") does too. Hint 1 should be vague, for example about her look or her character, and hint 2 should not describe glasses directly.
- **q-11701** (tv-shows-and-hosts) En «En Familia con Chabelo», el concursante podía cambiar su premio por otro escondido sin saber si era mejor o peor. ¿Cómo se llamaba ese juego? → La catafixia: No image candidate is adequate: 1–2 are 1917 archival scans of soldiers' Christmas packets with typed catalogue labels, 3–5 are historical cartoons/prints/text pages, 6 is a Comic-Con panel. A new search (e.g. "wrapped gift boxes") is needed; the question text itself is fine. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 5, cause_effect 11, count 11, estimate 1, identify 40, made_of 11, name_concept 31, odd_one_out 15, origin 19, purpose 23, record 8, sequence 9, when 12, who 57, word_meaning 33
- stimulus: map_outline 2, none 272, photo 12
- clue: completion 10, direct 104, riddle 43, scenario 40, three_facts 89
- answer_kind: group 20, number 15, person 72, place 28, thing 73, time 14, word 64
- lens: body_senses 20, educational_media 4, everyday 66, history 40, language 61, nature 4, pop_culture 67, school 17, university 7

## Dropped by the pipeline

- boxing-4: overlap like q-6931: Ingrit Valencia ganó bronce en Río 2016, fue la primera boxeadora colombiana con medalla olímpica y peleaba en la categoría femenina más liviana de esos Juegos. ¿Cuál era? → Peso mosca: El yucateco Miguel Canto fue campeón mundial de peso mosca en los años setenta. ¿Qué significa "peso mosca" en el box? → Una de las categorías más ligeras
- brands-and-snacks-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Soy un cereal de hojuelas de maíz escarchadas con azúcar, y en mi caja sale un tigre llamado Toño. ¿Qué cereal soy? → Zucaritas
- brands-and-snacks-7: overlap like q-5210: Es redondo, tiene un palito y cuando te comes el dulce de afuera encuentras un chicle adentro. ¿Cuál es? → El Bon Bon Bum: Es una paleta de dulce, viene cubierta de chile en polvo y se llama Rockaleta. ¿Qué esconde en el centro? → Un chicle
- brands-and-snacks-15: overlap like q-1576: Soy un snack triangular, crujiente y anaranjado, y nací para no desperdiciar sobras en un restaurante de Disneyland. ¿De qué estoy hecho? → Maíz: Nacieron en México a finales de los noventa, vienen enrollados como taquito y saben a chile con limón. ¿De qué están hechos los Takis Fuego? → De maíz
- childrens-songs-2: overlap like q-1720: Estás cantando 'Yo tenía diez perritos' y uno se cayó en la nieve. ¿Cuántos perritos te quedan? → 9: En «Yo tenía diez perritos», en cada verso se va un perrito hasta que no queda ninguno. ¿Qué practican los niños al cantarla? → Las restas
- contemporary-cinema-13: overlap like q-10290: Película mexicana de terror de 1968, de Carlos Enrique Taboada: en un internado de señoritas, unas alumnas oyen voces en una torre prohibida. ¿Cuál es? → Hasta el viento tiene miedo: Soy cineasta mexicano. Dirigí «Hasta el viento tiene miedo», «El libro de piedra» y, en 1975, «Más negro que la noche», con un gato negro llamado Becker. ¿Quién soy? → Carlos Enrique Taboada
- folk-beliefs-3: overlap like q-10289: En los mercados de México venden el «ojo de venado» para colgárselo a los bebés. ¿Para qué sirve, según la tradición? → Para protegerlos del mal de ojo: En México, a muchos bebés les ponen una pulserita roja como esta. Según la creencia, ¿de qué los protege? → Del mal de ojo
- home-and-street-3: overlap like folk-beliefs-1: Las abuelas mexicanas mojan con saliva un pedacito de hilo rojo y se lo pegan en la frente al bebé. ¿Qué le quieren quitar? → El hipo: Es una bolita de hilo rojo, se moja con saliva y se pega en la frente de un bebé. ¿Qué le quieren quitar con eso en México? → El hipo
- home-and-street-4: overlap like q-7956: Uno cuenta contra la pared y los demás se esconden. Para salvarte gritas «¡un, dos, tres por mí!». ¿A dónde debes llegar? → Al sitio donde contó el que busca: Uno cuenta hasta diez con los ojos tapados, los demás se esconden, y al hallar a alguien grita «¡un, dos, tres por…!». ¿Qué juego es? → Las escondidillas
- home-and-street-11: overlap like q-10332: Este consomé acompaña a los tacos de barbacoa. ¿De qué animal es la barbacoa tradicional de Hidalgo y el centro de México? → Borrego: Muchas familias mexicanas comen estos tacos de barbacoa los domingos. En el centro del país, ¿de qué animal es la barbacoa tradicional? → De borrego
- indigenous-words-3: overlap like q-0520: Construyeron la gran pirámide de Chichén Itzá y sus idiomas aún se hablan en México y Guatemala. ¿Qué pueblo es? → Los mayas: Contábamos los días con calendarios de piedra, nuestra lengua aún se oye en Yucatán y en «Wakanda por siempre» la habla Namor bajo el mar. ¿Quiénes somos? → Los mayas
- indigenous-words-10: overlap like q-0589: ¿Qué significa en náhuatl, la lengua de los aztecas, el nombre del volcán Popocatépetl? → Cerro que humea: Aparece en Chapultepec, Ecatepec y Tehuantepec, y viene de la palabra náhuatl «tépetl». ¿Qué significa? → Cerro
- liga-mx-0: overlap like q-0735: La hace todo el estadio a la vez: la gente se pone de pie y se vuelve a sentar por turnos. Se volvió famosa en el mundo gracias al Mundial de México 1986. ¿Qué es? → La ola: Este movimiento del público se hizo famoso en todo el mundo en el Mundial de México 1986. ¿Cómo se llama? → La ola
- lucha-libre-7: overlap like q-11464: Muchos luchadores mexicanos, como El Santo, nunca se quitaban la máscara en público. ¿Para qué la usaban? → Para mantener en secreto quiénes eran: En sus películas, ¿cuándo se quitaba la máscara plateada El Santo? → Nunca
- mariachi-and-ranchera-4: overlap like q-0699: Es un estado de México en la costa del golfo; de allí viene la canción 'La Bamba'; y un famoso pescado con tomate, aceitunas y alcaparras lleva su nombre. ¿Cuál es? → Veracruz: Estás en una fiesta donde el mariachi toca rancheras. ¿Cuál de estas canciones NO es una ranchera? → «La Bamba»
- mariachi-and-ranchera-6: overlap like q-4755: Mariachi bands wear the charro suit, with silver buttons and a huge hat. Who first wore this kind of outfit in Mexico? → Ranch horsemen: Mira este pantalón de charro. ¿De qué material son tradicionalmente los botones que lo adornan a los lados? → De metal, como la plata
- mariachi-and-ranchera-9: overlap like q-0062: Escucha: ¿qué instrumento está sonando? → El violín: Se apoya entre el hombro y la barbilla, tiene cuatro cuerdas y en el mariachi suelen tocarlo varios a la vez. ¿Qué instrumento es? → El violín
- national-symbols-3: overlap like q-3393: At an Olympic opening ceremony, who is the athlete walking in front of their team in this photo? → The flag bearer: Llevo la bandera en los honores del lunes y marcho al frente con la escolta. Me escogen por mis buenas calificaciones. ¿Quién soy? → El abanderado
- national-symbols-8: overlap like national-symbols-0: En un partido México contra Italia, las dos banderas tienen los mismos colores en el mismo orden. ¿Qué color va pegado al asta en ambas? → Verde: Estás coloreando la bandera de México: ya pintaste la franja roja y dejaste la blanca con el escudo. ¿De qué color pintas la franja que falta? → Verde
- national-team-10: overlap like q-5877: Maple the moose, Zayu the jaguar and Clutch the bald eagle are the mascots of which men's soccer World Cup? → 2026: Soy un alce, en la cancha soy portero y me encantan la música y el arte urbano. Represento a Canadá en el Mundial 2026. ¿Quién soy? → Maple
- painters-and-muralists-2: overlap like comics-5: Antes de ser telenovela con Bárbara Mori en 2004, «Rubí», de Yolanda Vargas Dulché, nació en otro formato. ¿Cuál? → Una historieta: Estás en un puesto de periódicos en 1966 y pides el nuevo número de Los Supermachos. ¿Qué te dan? → Una historieta
- painters-and-muralists-10: overlap like q-10447: Nací en Guanajuato, pinté la historia de México en los muros del Palacio Nacional y me casé dos veces con la misma pintora. ¿Quién soy? → Diego Rivera: ¿Quién pintó el mural Epopeya del pueblo mexicano? → Diego Rivera
- painters-and-muralists-11: overlap like q-6129: Frida Kahlo, the Mexican painter with flowers in her hair and famous joined eyebrows, painted which kind of picture more than any other? → Self-portraits: Una foto de otra persona es a «retrato» como una selfie es a… ¿qué? Frida Kahlo pintó decenas de ellos. → Autorretrato
- painters-and-muralists-14: overlap like q-10157: Este mural está hecho con piedras de colores y cubre las cuatro paredes de un edificio famoso. ¿Cuál es? → La Biblioteca Central de la UNAM: Los murales que cubren esta biblioteca de la UNAM no están pintados. ¿De qué están hechos? → De piedras de colores
- painters-and-muralists-16: overlap like q-6129: Frida Kahlo, the Mexican painter with flowers in her hair and famous joined eyebrows, painted which kind of picture more than any other? → Self-portraits: Frida Kahlo la pintaba en sus autorretratos, parecía las alas de una golondrina y aparece cuando las cejas se juntan. ¿Cómo se llama? → La uniceja
- regional-mexican-12: overlap like q-10438: El traje de tehuana, como el que se luce en Juchitán, Oaxaca, se volvió famoso en el mundo gracias a una pintora que lo usaba a diario. ¿Quién? → Frida Kahlo: Mira la foto de este traje de Oaxaca. ¿Qué famosa pintora mexicana se vestía muchas veces así? → Frida Kahlo
- boxing-7: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: En un gimnasio de box mexicano hay un costal: es muy pesado, cuelga del techo y está relleno de arena o trapos. ¿Para qué sirve? → Para practicar golpes
- brands-and-snacks-2: overlap like brands-and-snacks-7: Es una paleta de dulce, viene cubierta de chile en polvo y se llama Rockaleta. ¿Qué esconde en el centro? → Un chicle: La paleta Vero Mango tiene forma y sabor de mango. ¿De qué viene cubierta por fuera? → De chile en polvo
- state-symbols-10: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: En la Colonia, el galeón de Acapulco cruzaba el Pacífico hasta unas islas bautizadas en honor del rey Felipe II. ¿Cuáles? → Las Filipinas
- telenovelas-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Nació en la telenovela juvenil 'Miss XV', y en ella cantaban Paulina Goto y Natasha Dupeyrón. ¿Qué grupo es? → Eme 15
- transport-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Desde Guadalajara sale un tren turístico que cruza campos de agave azul hasta un Pueblo Mágico de Jalisco. ¿Cuál es? → Tequila
- tv-shows-and-hosts-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿Qué televisora mexicana transmite el noticiero «Telediario»? → Multimedios
- folk-beliefs-1: overlap like home-and-street-3: Es una bolita de hilo rojo, se moja con saliva y se pega en la frente de un bebé. ¿Qué le quieren quitar con eso en México? → El hipo: Las abuelas mexicanas mojan con saliva un pedacito de hilo rojo y se lo pegan en la frente al bebé. ¿Qué le quieren quitar? → El hipo
- folk-beliefs-5: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: Las abuelas mexicanas usan el Vaporrú para casi todo. Según su caja, ¿en quién NO se debe usar sin preguntarle al médico? → En un bebé de un año
- golden-age-cinema-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Si ves «El peñón de las Ánimas» (1943), de Miguel Zacarías, ves el debut en cine de una actriz que luego se casó con su coprotagonista, Jorge Negrete. ¿Quién es? → María Félix
- golden-age-cinema-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Por su fama internacional, Pedro Armendáriz hizo en 1963 de Kerim Bey, aliado en Estambul de un espía famoso. ¿De qué saga es esa película? → James Bond
- home-and-street-8: hard fail: correct 4, unambiguous 3, no_giveaway 3, no_overlap 5: En muchas casas de México se cambia cuando pasa el camión con su tonadita, y si se acaba no hay agua caliente para bañarse. ¿Qué es? → El tanque de gas
- indigenous-words-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En náhuatl se decía tomatl, ahuacatl y cacahuatl. Al pasar al español, ¿en qué se convirtió casi siempre esa terminación «-tl»? → En «-te»
- indigenous-words-11: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Aparece en Tonantzin, en Cuauhtemotzin y en Nezahualcoyotzin. ¿Qué expresa la terminación náhuatl «-tzin»? → Respeto o cariño
- indigenous-words-17: overlap like state-symbols-14: Un mazatleco es de Mazatlán. ¿Qué significa «Mazatlán» en náhuatl? → Lugar de venados: Este puerto de Sinaloa junta en su nombre «mázatl», un animal, con «-tlan», «lugar donde abundan». ¿Qué animal es? → Venados
- liga-mx-4: overlap like state-symbols-13: Estás en un partido de las Chivas y oyes estos apodos. ¿Cuál NO es de las Chivas? → Los Cementeros: Este club de Guadalajara viste rayas rojas y blancas y solo alinea futbolistas mexicanos. ¿Cuál es su apodo más famoso? → El Rebaño Sagrado
- money-1: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: En las noticias hablan mucho de «Banxico». ¿Qué es Banxico? → El banco central que emite los billetes
- national-symbols-0: overlap like national-symbols-8: Estás coloreando la bandera de México: ya pintaste la franja roja y dejaste la blanca con el escudo. ¿De qué color pintas la franja que falta? → Verde: En un partido México contra Italia, las dos banderas tienen los mismos colores en el mismo orden. ¿Qué color va pegado al asta en ambas? → Verde
- national-symbols-2: overlap like national-symbols-3: Llevo la bandera en los honores del lunes y marcho al frente con la escolta. Me escogen por mis buenas calificaciones. ¿Quién soy? → El abanderado: En los honores escolares, unos alumnos con guantes blancos marchan en formación y acompañan a la bandera. ¿Cómo se llama ese grupo? → La escolta
- national-symbols-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: «Tenochtitlan» está hecho de palabras náhuatl: tetl, «piedra»; tlan, «lugar», y nochtli, el fruto rojo o verde del nopal. ¿Cómo lo llamamos hoy? → La tuna
- national-team-1: overlap like q-11530: En este estadio, en 2012, el Tri ganó la final del futbol olímpico. ¿A qué selección le ganó? → Brasil: ¿Cuál fue el mayor triunfo de Luis Fernando Tena como técnico de una selección mexicana? → El oro olímpico
- other-sports-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ana Gabriela Guevara, plata olímpica en 400 metros en Atenas 2004, se dedicó luego a la política. ¿Qué organismo dirigió desde 2018? → La Comisión Nacional de Cultura Física y Deporte
- other-sports-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Vas al béisbol de la Liga Mexicana: la Ciudad de México es a los Diablos Rojos como Monterrey es a los… → Sultanes
- pop-and-rock-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: «Somos tres mujeres de los ochenta que cantamos a tres voces baladas como “¿Cómo te va mi amor?”.» ¿Quiénes somos? → Pandora
- regional-mexican-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Somos un grupo norteño de la frontera y en las fiestas todos bailan nuestra «La Chona». ¿Quiénes somos? → Los Tucanes de Tijuana
- sayings-4: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Si te dicen «No dejes para mañana lo que puedes hacer hoy», ¿qué te están diciendo que eres? → Un flojo
- school-and-services-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Hoy usa la marca «Correos de México», pero ¿con qué siglas se conoce oficialmente al Servicio Postal Mexicano? → SEPOMEX
- slang-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: «Adiosito», «cafecito» y «ahorita» le agregan «-ito» a una palabra. ¿Cómo se llaman estas palabras? → Diminutivos
- state-symbols-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En México, si alguien te dice «capitalino», ¿de dónde cree que eres? → De la Ciudad de México
- slang-12: overlap like q-5197: En las telenovelas colombianas, la mamá siempre le dice a su hijo «venga, mijo». ¿De dónde viene esa palabra? → De «mi hijo»: Las mamás y abuelitas mexicanas se la dicen con cariño a las niñas, y se forma juntando dos palabras de familia. ¿Cuál es? → Mija
- state-symbols-9: overlap like q-0450: Mira la foto: ¿cómo se llama este famoso lugar con esta pirámide maya? → Chichén Itzá: Mira este pedacito de una pirámide muy famosa de México. ¿Dónde está? → Chichén Itzá
- state-symbols-14: overlap like indigenous-words-17: Este puerto de Sinaloa junta en su nombre «mázatl», un animal, con «-tlan», «lugar donde abundan». ¿Qué animal es? → Venados: Un mazatleco es de Mazatlán. ¿Qué significa «Mazatlán» en náhuatl? → Lugar de venados
- telenovelas-4: overlap like q-11620: «Empecé de niña en la tele, canto pop y también rancheras con mariachi, y estuve casada con el cantante Mijares.» ¿Quién soy? → Lucero: ¿Qué cantante protagonizó 'Soy tu dueña' (2010) como Valentina Villalba, la rica dueña de una hacienda? → Lucero
- telenovelas-6: overlap like q-5231: Soy mexicana, en 2006 me puse lentes y frenos para ser Lety en «La fea más bella», la versión mexicana de Betty. ¿Quién soy? → Angélica Vale: ¿Qué actriz interpretó a Lety Padilla en 'La fea más bella' (2006)? → Angélica Vale
- traditional-dances-4: overlap like q-11555: Toqué el violín en la Tierra Caliente de Guerrero y Michoacán, me apodaron «el Paganini de la Tierra Caliente» y recibí el Premio Nacional de Ciencias y Artes. ¿Quién soy? → Juan Reynoso: Nací en la cuenca del río Balsas, entre Guerrero y Michoacán; me tocan con violín, guitarra y tamborita, y Juan Reynoso fue mi gran violinista. ¿Qué soy? → El son calentano
- traditional-dances-8: overlap like q-10435: Tras vencer a Azcapotzalco, el tlatoani Itzcóatl mandó quemar algo que no le convenía a los mexicas. ¿Qué? → Los códices antiguos: Completa el título de Moctezuma, «huey…», la palabra náhuatl de la que viene el nombre de los tastoanes de Jalisco. → Tlatoani
- traditional-dances-11: overlap like q-10434: Esta pieza mexica de hace unos 500 años está hecha con plumas verdes de quetzal. ¿Qué tipo de objeto es? → Penacho: Esta foto muestra de cerca una parte del atuendo de un danzante azteca. ¿Qué es? → El penacho
- writers-and-poets-5: overlap like q-0117: ¿En qué pueblo imaginario transcurre 'Cien años de soledad'? → Macondo: ¿Cuál de estos pueblos NO aparece en la obra de Juan Rulfo? → Macondo
