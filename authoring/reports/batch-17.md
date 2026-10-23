# batch-17

Made by `qgen batch` on 2026-10-23 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: colombia
- Language: Spanish (Latin America)
- Subcategories (27): hosts-actors-and-comedians, sweets-and-desserts, natural-parks-and-ecosystems, club-football, banknotes-and-coins, national-team, olympic-medallists, popular-and-andean-music, carnivals-and-fairs, painters-sculptors-and-museums, salsa-and-tropical-music, cycling, symbols-of-departments-and-cities, vallenato, brands-and-products, ghosts-and-creatures, cinema, writers-and-books, other-sports, rhythms-dances-and-instruments, telenovelas, indigenous-myths-and-folk-beliefs, traditional-games, tv-shows-and-series, 19th-century, rivers-seas-and-islands, drinks
- Merged: 215 (q-6994…q-7208)
- Approved: 194
- Needs work: 21
- Dropped by the pipeline: 54
- Reviewed by: claude-opus-5-5
- Claude calls: 503, about $63.29 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-15, batch-16; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-15 | batch-16 | batch-17 |
|---|---|---:|---:|---:|
| source locale |  | en | es | es |
| drafts |  | 955 | 271 | 269 |
| skipped slots |  | 827 | 215 | 217 |
| dropped |  | 273 | 65 | 54 |
| drop rate | ≤ 20.0 % | 28.6 % ✗ | 24.0 % ✗ | 20.1 % ✗ |
| dropped: hard fail correct |  | 0 | 4 | 2 |
| dropped: hard fail unambiguous |  | 2 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 52 | 25 | 14 |
| dropped: overlap |  | 210 | 37 | 38 |
| dropped: duplicate |  | 8 | 0 | 0 |
| dropped: fact-check wrong |  | 1 | 0 | 1 |
| merged |  | 682 | 206 | 215 |
| approved |  | 618 | 186 | 194 |
| needs_work |  | 64 | 20 | 21 |
| needs_work rate | ≤ 20.0 % | 9.4 % ✓ | 9.7 % ✓ | 9.8 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.4 % ✓ | 1.9 % ✓ | 3.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.4 % ✓ | 1.5 % ✓ | 0.9 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.9 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.3 % ✗ | 0.5 % ✓ | 1.9 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.4 % ✓ | 6.3 % ✓ | 4.2 % ✓ |
| media: no pick in review 1 |  | 82 | 36 | 41 |
| media: recovered by research |  | 57 | 24 | 34 |
| media: no pick at record |  | 26 | 13 | 7 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.9 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.5 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 23.8 % ✗ | 14.0 % ✓ | 15.6 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 55.7 % ✓ | 29.2 % ✗ | 45.9 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.52 ✗ | 1.00 ✓ | 1.75 ✗ |
| approved 11–15 |  | 215 | 25 | 40 |
| top move | ≤ 25.0 % | 16.3 % ✓ | 14.6 % ✓ | 14.4 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 76.2 % | 76.7 % | 84.2 % |
| values stimulus |  | 7 | 5 | 5 |
| top clue | ≤ 60.0 % | 45.6 % ✓ | 37.4 % ✓ | 38.1 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 23.6 % ✓ | 28.6 % ✓ | 27.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 19.4 % ✓ | 20.9 % ✓ | 20.9 % ✓ |
| values lens |  | 12 | 11 | 11 |
| media share | 15.0 %–50.0 % | 23.8 % ✓ | 23.3 % ✓ | 15.8 % ✓ |
| mean fun | ≥ 3.40 | 3.35 ✗ | 3.32 ✗ | 3.38 ✗ |
| cost $ |  | $182.45 | $54.66 | $59.96 |
| $ per approved | ≤ $0.35 | $0.30 ✓ | $0.29 ✓ | $0.31 ✓ |
| calls |  | 1417 | 415 | 443 |
| calls per approved |  | 2.29 | 2.23 | 2.28 |
| wall time h |  | 3.37 | 2.04 | 1.90 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 54 (0 %)
- Major among review needs work: 5 of 6 (83 %)
- Problems by kind: giveaway 11 (3 major), fact 3 (2 major), ambiguity 2 (0 major), overlap 2 (2 major), media 4 (2 major), difficulty 1 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.33

Major findings on approved questions:

None.

## Needs work

- **q-6996** (19th-century) En el siglo XIX, Colombia exportaba a Europa y Estados Unidos esta semilla, el 'marfil vegetal'. ¿Para qué se usaba sobre todo? → Para hacer botones: No candidate shows clean tagua seeds as the essential slot needs. #6 is tagua buttons, which shows the answer. #4 and #5 are carvings made from tagua. #2 and #3 are frog photos where the nut is only a perch. #1 shows the palm's spiky fruit clusters, not the seeds. A new search (e.g. 'tagua nut' or 'vegetable ivory seeds') is needed. No se encontró una imagen adecuada para esta pregunta.
- **q-7006** (banknotes-and-coins) Mira este billete colombiano. ¿Cuántas lucas vale? → 50: None of the candidates shows the 50 000 peso note: they are people at Fundación Gabo events and an FNPI logo. A search can't be run again here, so this essential-image question can't be finished. Either find a freely licensed photo of the García Márquez 50 000 note, or change the question so it doesn't need a photo of the note. No se encontró una imagen adecuada para esta pregunta.
- **q-7011** (brands-and-products) Crepes & Waffles nació en Bogotá en 1980, es famosa por sus helados y tiene una política especial al contratar. ¿A quiénes contrata principalmente? → Madres cabeza de familia: Hint 2 ('darle un trabajo estable a quien sostiene un hogar sin ayuda') is just the definition of 'madre cabeza de familia', so it gives the answer away and rules out all three wrong options at the second hint. Make hint 2 vaguer, for example about the policy aiming to support a particular group of women or families, and leave the strong clue for hint 3.
- **q-7013** (brands-and-products) Ego es una marca colombiana de champú y gel, de la misma empresa que hace Savital y Bon Ice. ¿Para quién se creó? → Para hombres: Hint 2 gives the answer away: "dark, sober packaging and stronger scents than Savital" is textbook men's-product marketing and, against babies, pets and swimmers, points straight to "Para hombres". Rewrite hint 2 so it stays vague, e.g. about when the brand launched or its gel's place in the shelf, without the masculine-styling cues.
- **q-7030** (club-football) Cuando una final de la Liga colombiana termina empatada, se patean penales como este. ¿Cuántos cobra cada equipo antes de la muerte súbita? → 5: This asks the same fact as approved q-2488: how many kicks each team takes at first in a penalty shootout (5). Putting it in the Colombian league doesn't change the fact. Separately, hint 2 ("la mitad de diez") already gives the number away.
- **q-7046** (drinks) Estás colando el tinto en un colador de tela. ¿Cómo se llama el café molido y mojado que queda adentro? → La borra: None of the image candidates fits: they show a fuel outlet, an industrial filter room, a beach, an airman, a 1943 warehouse and mussel shells, none of them a cloth coffee filter. A new search isn't allowed in this run. The text itself is fine. A good search would be "cloth coffee filter" or "colador de tela café". No se encontró una imagen adecuada para esta pregunta.
- **q-7053** (ghosts-and-creatures) El curandero del pueblo le pasa un huevo por todo el cuerpo a un bebé. Según la creencia, ¿para qué lo hace? → Para quitarle el mal de ojo: This repeats approved q-5051 ("Te pasan un huevo por todo el cuerpo… ¿para qué es?" → "Para sacar el mal de ojo"): same ritual, same question, same answer. Drop this draft or replace it with a different fact.
- **q-7065** (national-team) Diego Maradona y el Pibe Valderrama usaban el mismo número en la camiseta de sus selecciones. ¿Cuál era? → 10: This asks the same fact as approved q-3687 ("Pelé, Maradona and Messi all made one shirt number famous": 10). Both name Maradona, and this one's hint 2 even names Messi, so seeing one question gives the other away. To keep it in the Colombia bundle, it needs a different question about Valderrama.
- **q-7083** (painters-sculptors-and-museums) Un enorme gato de bronce de Botero llegó a esta ciudad en 1987, cambió de sitio varias veces y hoy vive en el barrio del Raval. ¿Qué ciudad es? → Barcelona: Hints 1 and 2 each give the answer away. Hint 1 ("European city on the Mediterranean shore") rules out Madrid, Paris and Rome (Rome isn't on the coast), and hint 2 ("not its country's capital") rules out all three wrong options at once. Replace them with vague hints that leave more than one option open, for example about Botero's rounded style or the 1980s. Optionally make hint 3 something other than the Sagrada Familia.
- **q-7087** (painters-sculptors-and-museums) Mira estas terrazas circulares de piedra que construyeron los taironas en Ciudad Perdida. ¿Para qué servían? → Bases para casas y templos: The essential image must show Ciudad Perdida's (Teyuna's) circular stone terraces, but none of the candidates does, and a new search isn't allowed this round. Find a Commons photo of the Teyuna terraces (try 'Ciudad Perdida terraces' or 'Teyuna Colombia') and attach it manually. No se encontró una imagen adecuada para esta pregunta.
- **q-7092** (banknotes-and-coins) El papel de los billetes colombianos tiene unas fibras de colores que a simple vista no se notan. ¿Cómo se pueden ver? → Con una lámpara de luz ultravioleta: The text is fine, but all three image candidates are Argentine 50 000-peso banknotes. A question about Colombian banknotes can't use them, and no new search is allowed. The slot needs a Colombian banknote (e.g. "Colombian peso banknote" or "billete colombiano") or a neutral UV lamp/counterfeit-detector image. A UV lamp would hint at the answer, so the banknote is better. No se encontró una imagen adecuada para esta pregunta.
- **q-7093** (banknotes-and-coins) Fui presidente de Colombia en los años 70, mi papá también fue presidente y hoy salgo en el billete naranja de 20 000. ¿Quién soy? → Alfonso López Michelsen: The premise is wrong. Colombia's orange 20 000-peso note (the 2016 series) shows the astronomer Julio Garavito Armero, not Alfonso López Michelsen, and I know of no Colombian banknote that shows López Michelsen. One of the wrong answers, Carlos Lleras Restrepo, is actually on the 100 000-peso note, so the banknote clue points away from the intended answer. The fact check's 'confirmed' verdict should be overruled.
- **q-7098** (cycling) Egan Bernal la conquistó en el Giro de Italia de 2021, y allá la llaman «maglia rosa». ¿Qué es? → La camiseta del líder de la carrera: The description calls it 'una prenda' and the question says 'la conquistó', so both the description and the feminine pronoun rule out the masculine 'El trofeo para el equipo ganador'. Replace that option with a fourth feminine garment-type option, e.g. 'La camiseta del mejor joven' (would need checking against Egan's 2021 classifications) or 'La camiseta del campeón nacional'. Also make the description play on the Giro or Italy without saying it's a garment.
- **q-7115** (other-sports) Estás jugando ponchados en el recreo y tienes el balón en la mano. ¿Para qué lo lanzas? → Para sacar a un rival: Hint 2 ("En este juego no hay red, ni aro, ni arco") rules out all three wrong answers, so it gives the answer away before hint 3. Replace it with a vague hint that rules out none of the options, e.g. about how the teams are set up or where they stand on the court.
- **q-7120** (popular-and-andean-music) El Bunde tolimense, de Alberto Castilla, se convirtió en el himno del Tolima. ¿Qué tres aires andinos mezcla su música? → Guabina, torbellino y bambuco: The fact check is 'uncertain' and I can't confirm it either: sources disagree on which aires the Bunde tolimense blends. Some say guabina, torbellino and bambuco. Spanish Wikipedia adds rajaleña, pasillo, vals, chotis and others. English Wikipedia names bambuco, vals, danza and pasillo. That means the distractors 'Pasillo, danza y vals' and 'Pasillo, chotis y bambuco' are partly defensible. Hint 3 also ties guabina to Boyacá and Santander, but it is just as much a Tolima/Huila rhythm. Either ask about a fact that isn't disputed (for example the composer or the song's status as the department's anthem), or replace the distractors with rhythms that no source links to the Bunde. Verificación de datos: uncertain. Sources disagree. Some give guabina, torbellino and bambuco. The Spanish Wikipedia lists rajaleña, pasillo, guabina, torbellino and bambuco, plus vals, mazurka, redova and chotis. The English Wikipedia lists bambuco, vals, danza and pasillo. So 'three aires' is ambiguous, and the distractors 'Pasillo, chotis y bambuco' and 'Pasillo, danza y vals' partly overlap with documented elements. Also, the Tolima anthem version has lyrics by Nicanor Velásquez, which the question doesn't mention.
- **q-7131** (rivers-seas-and-islands) Este es el río Cesar, que le da nombre a un departamento y desemboca en la ciénaga de Zapatosa. ¿Dónde nace? → En la Sierra Nevada de Santa Marta: The question text says "Este es el río Cesar", so the picture has to show the Cesar River. Candidates 1 and 2 show the Guatapurí, a different river (a tributary at Valledupar). Candidate 3 is an unidentified rocky gorge with nothing to place it. No new search is allowed, so the slot needs a real photo of the Cesar River, e.g. from a search for "Cesar River Colombia". Another option is to drop "Este es" and use a decorative Cesar-region image. No se encontró una imagen adecuada para esta pregunta.
- **q-7134** (salsa-and-tropical-music) Según la tradición, ¿qué llevan en la mano las bailarinas de cumbia mientras bailan en la rueda? → Un manojo de velas encendidas: None of the media candidates fits the question: the search "tambor alegre Colombia" matched place names containing "Alegre" (a river dolphin, a night hike, a couple by a chiva bus, village houses, a Brazilian signing ceremony). A new search is needed, e.g. "cumbia dancers pollera" or "tambor alegre drum". Avoid any picture that shows candles. The question text itself is fine. No se encontró una imagen adecuada para esta pregunta.
- **q-7166** (sweets-and-desserts) Viene en polvo en un sobrecito, se cuaja en la nevera, tiembla en el plato y hay roja, verde y amarilla. ¿Qué es? → Gelatina: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-7174** (symbols-of-departments-and-cities) Si naces en Palmira, Buga o Buenaventura, ¿cómo te dicen según tu departamento? → Vallecaucano: The description ('Salsa, pandebono y lulada') names Cali's best-known trademarks, so a Colombian family can pick 'Vallecaucano' from the description alone, before hearing the cities or any hint. The description needs to play on the theme without Valle-specific signatures. Also note the overlap with approved q-5227 (pandebono → 'De los vallunos'): it asks the same Valle demonym, and naming pandebono here makes the link even stronger.
- **q-7178** (telenovelas) En «Yo soy Betty, la fea», Lorna Cepeda interpretó a Patricia Fernández. ¿Qué cosa de ella inspiró su famoso apodo? → Su pelo teñido: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US).
- **q-7189** (traditional-games) La púa es la punta de metal del trompo: sobre ella baila y raya el piso. En los juegos de calle, ¿para qué más la usan los niños? → Para golpear el trompo del rival: The wrong answer 'Para enrollar la pita' can be defended: the usual way to wind a trompo is to start the cord at the púa, wrapping it around the tip first and then up the body. Replace it with a use the púa clearly never has (for example 'Para guardarlo colgado' or 'Para pintar figuras en el piso'). Hint 2 ('deja marcas o hasta raja la madera') also comes very close to giving the answer away, so consider making it vaguer.

## Question axes

- move: analogy 3, cause_effect 6, count 14, estimate 2, identify 31, made_of 13, name_concept 18, odd_one_out 27, origin 16, purpose 19, record 3, sequence 8, when 16, who 21, word_meaning 18
- stimulus: detail 3, map_outline 2, none 181, photo 26, sound 3
- clue: completion 4, direct 82, riddle 25, scenario 38, three_facts 66
- answer_kind: group 37, number 16, person 29, place 22, thing 59, time 18, word 34
- lens: body_senses 8, colombia 43, educational_media 7, everyday 38, history 45, language 36, nature 6, pop_culture 18, school 11, science_news 2, university 1

## Dropped by the pipeline

- 19th-century-0: overlap like q-6803: ¿En qué municipio de Cundinamarca está esta catedral, construida dentro de una mina de sal? → Zipaquirá: Este tren de vapor lleva turistas desde Bogotá por rieles de más de cien años. ¿A qué pueblo famoso por su catedral dentro de una mina de sal llega? → Zipaquirá
- 19th-century-6: overlap like q-0111: ¿Quién escribió el cuento en verso 'El renacuajo paseador'? → Rafael Pombo: Este animalito es el protagonista de un famoso cuento en verso colombiano. ¿Cómo se llama el personaje? → Rinrín
- 19th-century-8: overlap like q-5082: Es capital del Huila, queda junto al río Magdalena y en sus fiestas de San Pedro corona a la Reina Nacional del Bambuco. ¿Qué ciudad es? → Neiva: Es un ritmo de la región andina, se toca con tiple y bandola, y en Neiva tiene su reinado nacional. ¿Cuál es? → El bambuco
- brands-and-products-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En Colombia, la marca Margarita es famosa por este mecato. ¿De qué está hecho? → De papa
- carnivals-and-fairs-3: overlap like q-6965: Las gaitas del Festival de Gaitas de Ovejas tienen cabeza de cera de abejas y boquilla de pluma de pato. ¿De qué planta es su cuerpo? → Cardón: Se hace con el tallo de un cactus, lleva una cabeza de cera de abejas y una pluma de pato. ¿Cómo se toca la gaita colombiana? → Soplándola, como una flauta
- carnivals-and-fairs-7: overlap like q-0171: Está cubierta de musgo y hojas, vive en la selva y castiga a quienes maltratan la naturaleza. ¿Quién es? → La Madremonte: Cada agosto desfilo por Medellín en el Desfile de Mitos y Leyendas. Vivo en el monte, me visto de musgo y hojas y castigo a quien daña el bosque. ¿Quién soy? → La Madremonte
- carnivals-and-fairs-10: overlap like q-5041: Las máscaras de madera tallada de toritos y tigres son típicas de un carnaval colombiano muy famoso. ¿De qué ciudad? → Barranquilla: Mira la foto: carrozas como esta abren el carnaval en el desfile de la Batalla de Flores. ¿De qué ciudad es ese carnaval? → Barranquilla
- cinema-2: overlap like q-6845: Catalina Sandino Moreno fue nominada al Óscar a mejor actriz por «María llena eres de gracia». ¿En qué año fue la ceremonia? → 2005: ¿Qué actriz colombiana fue nominada al Óscar a mejor actriz por la película 'María, llena eres de gracia' (2004)? → Catalina Sandino Moreno
- club-football-11: overlap like q-6087: They blow a whistle, show yellow and red cards, and make sure soccer players follow the rules. Who are they? → Referees: «Uso pito, corro por toda la cancha de El Campín y saco una tarjeta amarilla cuando hay falta». ¿Quién soy? → El árbitro
- drinks-12: overlap like q-0509: ¿Con qué se hace la natilla navideña colombiana? → Leche, panela y fécula de maíz: Se reza la novena, se comen buñuelos con natilla y se brinda con sabajón. ¿Para celebrar qué fiesta? → La Navidad
- hosts-actors-and-comedians-1: overlap like q-5229: A Pedro Coral Tavera lo apodaban «el escamoso». En Colombia, ser escamoso es… → Presumir y aparentar más de lo que uno es: A Pedro Coral, el personaje de Miguel Varoni, le decían «Pedro el escamoso». En Colombia, ¿qué es ser «escamoso»? → Ser presumido y creído
- hosts-actors-and-comedians-15: overlap like q-5023: Este programa de humor de la TV colombiana, al aire desde 1972, es famoso por sus cuentachistes y sketches. ¿Cómo se llama? → Sábados Felices: La Gorda Fabiola es esposa del humorista Polilla y por décadas ha contado chistes en el mismo elenco de humor de Caracol. ¿En cuál? → Sábados Felices
- indigenous-myths-and-folk-beliefs-2: overlap like q-7049: Según la tradición popular, si rocías agua bendita en los rincones de la casa, ¿quiénes salen corriendo? → Las brujas: En el campo colombiano dicen que vuelan de noche, entran a las casas convertidas en pájaro y caen si pones unas tijeras abiertas en cruz. ¿Quiénes son? → Las brujas
- indigenous-myths-and-folk-beliefs-12: overlap like q-6798: Es ropa interior, es del color del sol y se estrena la noche del 31 de diciembre. ¿Para qué es este agüero colombiano? → Para atraer la buena suerte: Se estrenan el 31 de diciembre, se ponen antes de la medianoche y son calzones amarillos. Según el agüero, ¿qué atraen? → La buena suerte
- indigenous-myths-and-folk-beliefs-17: overlap like q-7053: El curandero del pueblo le pasa un huevo por todo el cuerpo a un bebé. Según la creencia, ¿para qué lo hace? → Para quitarle el mal de ojo: Según la creencia popular colombiana, ¿a quiénes les cae más fácil el mal de ojo? → A los bebés
- natural-parks-and-ecosystems-5: overlap like q-0752: El médico Ronald Ross descubrió que la malaria la transmite el insecto que hace este sonido. Escucha: ¿cuál es? → El zancudo: Escucha: si oyes esto mientras caminas por la selva del Amazonas, ¿qué te conviene ponerte? → Repelente
- natural-parks-and-ecosystems-11: overlap like q-0937: Adivina: soy la capa de hielo que cubre casi toda la Antártida. ¿Qué tesoro del planeta guardo congelado? → La mayor parte del agua dulce: Mira este nevado colombiano. ¿Qué nos da su glaciar? → Agua dulce para ríos y pueblos
- olympic-medallists-0: overlap like q-5167: Óscar Figueroa ganó oro olímpico en pesas y, como despedida, dejó sus zapatos sobre la tarima. ¿En qué ciudad fue? → Río de Janeiro: Mariana Pajón ganó su primer oro olímpico en Londres 2012 y repitió en los Juegos siguientes. ¿En qué ciudad fueron? → Río de Janeiro
- olympic-medallists-1: overlap like q-0484: ¿En qué prueba de atletismo ganó Caterine Ibargüen la medalla de oro en los Juegos Olímpicos de Río 2016? → Salto triple: Nací en Apartadó, empecé en el salto alto y terminé cayendo en un foso de arena. Soy campeona mundial y olímpica. ¿Quién soy? → Caterine Ibargüen
- olympic-medallists-2: overlap like q-0485: ¿Quién fue la primera mujer colombiana en ganar una medalla de oro en unos Juegos Olímpicos? → María Isabel Urrutia: ¿En qué año ganó Colombia su primera medalla de oro olímpica? → 2000
- olympic-medallists-4: overlap like q-5167: Óscar Figueroa ganó oro olímpico en pesas y, como despedida, dejó sus zapatos sobre la tarima. ¿En qué ciudad fue? → Río de Janeiro: En este deporte, ¿qué colombiano ganó oro en Río 2016 y se despidió dejando sus zapatos sobre la tarima? → Óscar Figueroa
- olympic-medallists-5: overlap like q-3063: On the Olympic podium, first place is to gold as third place is to…? → Bronze: Un deportista colombiano llega de tercero en unos Juegos Olímpicos. ¿De qué es la medalla que le cuelgan? → Bronce
- popular-and-andean-music-8: overlap like q-6904: Vivo en cables larguísimos, me prendo y me apago de colores y en diciembre me cuelgan en balcones y en el alumbrado de Medellín. ¿Qué soy? → Los bombillos navideños: Cada diciembre en Medellín, las familias salen a ver 'los alumbrados' a orillas del río y en los parques. ¿Qué son? → Figuras y luces navideñas gigantes
- popular-and-andean-music-12: overlap like q-5017: Este boyacense de ruana y sombrero es considerado el padre de la carranga. ¿Quién es? → Jorge Velosa: Los Carrangueros de Ráquira, el grupo del que nació la carranga en los años 70, surgieron alrededor de un músico boyacense. ¿Quién? → Jorge Velosa
- 19th-century-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Tras la separación de Venezuela y Ecuador, el país volvió al nombre del antiguo virreinato. ¿Cómo se llamó desde 1832? → República de la Nueva Granada
- carnivals-and-fairs-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: Las figuras gigantes del Carnaval de Negros y Blancos se moldean sobre barro y se secan al sol. ¿De qué material se hacen? → Papel maché
- cinema-8: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: En 'La playa D.C.', estrenada en Cannes en 2012, Tomás es un joven afro que hace peinados y llega a Bogotá desplazado. ¿De qué región viene? → El Pacífico
- club-football-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Jhon Jairo Tréllez fue delantero del Atlético Nacional que ganó la Copa Libertadores en 1989. ¿Cuál era su apodo? → La Turbina
- club-football-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La liga profesional colombiana se jugó por primera vez en 1948. ¿Qué club fue su primer campeón? → Independiente Santa Fe
- club-football-7: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Músicos es a orquesta como hinchas es a… → Hinchada
- drinks-6: fact-check wrong: Hint 1 is false: masato, one of the wrong answers, is traditionally made from fermented rice, so bocadillo isn't the only option without rice. Arroz con leche contains both rice and milk, and natilla contains milk, so the hint doesn't separate the answer from the others.: ¿Cuál de estas preparaciones colombianas NO lleva canela normalmente? → El bocadillo
- hosts-actors-and-comedians-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: El influenciador paisa La Liendra lleva un apodo que en Colombia es el nombre de algo. ¿De qué? → El huevito del piojo
- natural-parks-and-ecosystems-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En un documental sobre Chiribiquete aparecen sus tepuyes. ¿Cuál de estas palabras NO los describe? → Volcánicos
- other-sports-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Es de Medellín, lo apodan 'Spider-Man' por agacharse casi tocando el césped para leer el terreno, y en 2008 fue el primer colombiano en ganar en este circuito. ¿Cuál? → El PGA Tour
- painters-sculptors-and-museums-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Este edificio de ladrillo, diseñado por Rogelio Salmona junto al Parque de la Independencia en Bogotá, es un museo. ¿Cuál? → Museo de Arte Moderno de Bogotá
- salsa-and-tropical-music-12: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Toco el trombón, soy de Barranquilla y fundé una orquesta de salsa con nombre de gigantes mitológicos. ¿Quién soy? → Alberto Barros
- sweets-and-desserts-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: La uchuva, la fruta del dulce de uchuva, en inglés se llama 'cape gooseberry'. ¿De dónde es originaria? → De los Andes de Sudamérica
- sweets-and-desserts-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En la panadería pides un roscón relleno de arequipe con tu chocolate. ¿Qué forma tiene un roscón? → De anillo
- vallenato-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: En Valledupar, cientos de niños aprenden acordeón en una academia famosa por sus «acordeoneritos». ¿Quién la fundó? → Andrés Gil
- rhythms-dances-and-instruments-17: overlap like carnivals-and-fairs-10: Mira la foto: carrozas como esta abren el carnaval en el desfile de la Batalla de Flores. ¿De qué ciudad es ese carnaval? → Barranquilla: Me eligen cada año, leo el bando y encabezo la Batalla de Flores en mi carroza. ¿Quién soy? → La reina del Carnaval de Barranquilla
- rivers-seas-and-islands-2: overlap like q-5105: Santa Marta, la ciudad más antigua de Colombia, fue fundada en 1525. ¿Qué conquistador la fundó? → Rodrigo de Bastidas: Mira esta bahía del Caribe colombiano. Alrededor de ella está la ciudad más antigua de Colombia, fundada en 1525. ¿Cuál es? → Santa Marta
- rivers-seas-and-islands-13: overlap like q-6925: El cardón crece en La Guajira y en la Tatacoa, mide varios metros y los wayuu usan su madera para hacer sus casas. ¿Qué es? → Un cactus: En la península de La Guajira vive el pueblo indígena más numeroso de Colombia, famoso por sus mochilas tejidas. ¿Cuál es? → Los wayuu
- salsa-and-tropical-music-4: overlap like q-6945: La flauta de millo se toca de lado y su lengüeta se corta en la misma caña. ¿Qué es el millo? → Una planta parecida al sorgo: Se hace con el tallo de una planta, tiene una lengüeta cortada en el mismo tubo y se toca de lado. ¿Qué es la caña de millo? → Una flauta de la cumbia
- symbols-of-departments-and-cities-2: overlap like q-5081: Estás al pie de Monserrate, en Bogotá, y quieres subir. ¿Cuál de estos NO te sirve para llegar arriba? → El metro: Mira esta iglesia blanca en lo alto de un cerro de Bogotá. ¿Cómo se llama ese cerro? → Monserrate
- symbols-of-departments-and-cities-8: overlap like q-5057: ¿Cómo se le dice al acento de Medellín y Antioquia, famoso por el «pues» y el «¡ave María!»? → Paisa: Completa: en Colombia, a un antioqueño también le dicen «___». → paisa
- symbols-of-departments-and-cities-9: overlap like q-7154: Vivo entre ganado y sabana, llevo sombrero y cotizas, y en las fiestas zapateo con mi pareja hasta el amanecer. ¿Quién soy? → El llanero: Vive en las grandes sabanas planas del oriente, arrea ganado a caballo y baila joropo. ¿Cómo le dicen en Colombia? → Llanero
- symbols-of-departments-and-cities-13: overlap like q-1359: Técnica de joyería: hilos finísimos de oro o plata se tuercen y se sueldan formando un encaje calado. En Mompox es tradición. ¿Cuál es? → Filigrana: Así se le dice a quien nace en la ciudad de la filigrana de oro, donde Bolívar dijo que le debía «la gloria». ¿Cuál es ese gentilicio? → Momposino
- symbols-of-departments-and-cities-14: overlap like q-0063: ¿Qué cantante colombiana cantó 'Waka Waka' para el Mundial de 2010? → Shakira: Mira la foto: esta estatua en Barranquilla homenajea a una cantante costeña famosa en todo el mundo. ¿Quién es? → Shakira
- symbols-of-departments-and-cities-17: overlap like q-5058: Quien dice «¡achichay!» cuando hace frío, con acento pastuso, viene del departamento resaltado. ¿Cuál es? → Nariño: Un pastuso vive al pie del volcán Galeras, come cuy asado y se abriga del frío andino. ¿De qué departamento es? → Nariño
- traditional-games-4: overlap like q-0297: ¿Qué día empieza la Novena de Aguinaldos? → 16 de diciembre: Estás en la novena de aguinaldos cantando 'Tutaina' y 'Los peces en el río'. ¿En qué fechas se reza la novena? → Del 16 al 24 de diciembre
- tv-shows-and-series-16: overlap like q-6844: Juanpis González es un gomelo, le dice «mi papi» a su papá y tiene su programa, «Juanpis Live Show». ¿De qué ciudad es? → Bogotá: Vivo en el norte de Bogotá, mi papi tiene mucha plata y Alejandro Riaño me dio vida en la televisión. ¿Qué clase de joven soy? → Un gomelo
- vallenato-10: overlap like q-6975: El inglés Quantic y Mario Galeano crearon Ondatrópica en 2012 y grabaron el primer disco en los míticos estudios de Discos Fuentes. ¿En qué ciudad? → Medellín: Antonio Fuentes fundó Discos Fuentes en Cartagena en 1934, pero en los años 50 se llevó la disquera a otra ciudad. ¿A cuál? → Medellín
- writers-and-books-3: overlap like 19th-century-6: Este animalito es el protagonista de un famoso cuento en verso colombiano. ¿Cómo se llama el personaje? → Rinrín: «El hijo de Rana, Rinrín Renacuajo, salió esta mañana muy tieso y muy majo». ¿Cuál de estos personajes NO aparece en ese poema de Rafael Pombo? → El conejo
- writers-and-books-7: overlap like q-0119: ¿Cómo se llama la famosa novela romántica del colombiano Jorge Isaacs (1867)? → María: «En un lugar de la Mancha» es a «Don Quijote» como «Era yo niño aún cuando me alejaron de la casa paterna» es a… → «María»
