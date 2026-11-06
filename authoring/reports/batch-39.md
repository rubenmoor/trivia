# batch-39

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: mexico
- Language: Spanish (Latin America)
- Subcategories (29): painters-and-muralists, folk-beliefs, indigenous-words, golden-age-cinema, maya, brands-and-snacks, drinks, other-sports, national-symbols, legends, boxing, mariachi-and-ranchera, traditional-games, liga-mx, civic-holidays, pre-hispanic-gods, writers-and-poets, telenovelas, traditional-dances, money, regional-mexican, states-and-capitals, tv-shows-and-hosts, national-team, sayings, lucha-libre, contemporary-cinema, christmas-season, conquest-and-colony
- Merged: 232 (q-12493…q-12724)
- Approved: 212
- Needs work: 20
- Dropped by the pipeline: 73
- Reviewed by: claude-opus-5-5
- Claude calls: 531, about $70.75 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-37, batch-38; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-37 | batch-38 | batch-39 |
|---|---|---:|---:|---:|
| source locale |  | de | es-ES | es |
| drafts |  | 347 | 304 | 305 |
| skipped slots |  | 139 | 182 | 217 |
| dropped |  | 52 | 60 | 73 |
| drop rate | ≤ 20.0 % | 15.0 % ✓ | 19.7 % ✓ | 23.9 % ✗ |
| dropped: hard fail correct |  | 1 | 3 | 3 |
| dropped: hard fail unambiguous |  | 0 | 0 | 2 |
| dropped: hard fail no_giveaway |  | 25 | 22 | 19 |
| dropped: overlap |  | 27 | 31 | 48 |
| dropped: duplicate |  | 0 | 1 | 1 |
| dropped: fact-check wrong |  | 0 | 3 | 2 |
| merged |  | 295 | 244 | 232 |
| approved |  | 265 | 230 | 212 |
| needs_work |  | 30 | 14 | 20 |
| needs_work rate | ≤ 20.0 % | 10.2 % ✓ | 5.7 % ✓ | 8.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.7 % ✓ | 2.5 % ✓ | 1.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.2 % ✓ | 0.9 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.7 % ✗ | 2.0 % ✗ | 2.2 % ✗ |
| needs_work: media | ≤ 10.0 % | 5.1 % ✓ | 1.2 % ✓ | 4.3 % ✓ |
| media: no pick in review 1 |  | 33 | 37 | 37 |
| media: recovered by research |  | 22 | 35 | 28 |
| media: no pick at record |  | 12 | 3 | 9 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 9.2 % ✓ | 12.2 % ✓ | 17.7 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 65.3 % ✓ | 63.4 % ✓ | 48.2 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.25 ✓ | 1.11 ✓ | 0.71 ✓ |
| approved 11–15 |  | 62 | 59 | 47 |
| top move | ≤ 25.0 % | 14.9 % ✓ | 14.8 % ✓ | 14.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 79.3 % | 80.3 % | 79.3 % |
| values stimulus |  | 4 | 4 | 5 |
| top clue | ≤ 60.0 % | 44.7 % ✓ | 45.5 % ✓ | 44.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 20.3 % ✓ | 22.5 % ✓ | 22.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.3 % ✓ | 24.2 % ✓ | 20.3 % ✓ |
| values lens |  | 11 | 10 | 11 |
| media share | 15.0 %–50.0 % | 20.7 % ✓ | 19.7 % ✓ | 20.7 % ✓ |
| mean fun | ≥ 3.40 | 3.47 ✓ | 3.51 ✓ | 3.47 ✓ |
| cost $ |  | $81.47 | $70.75 | $67.46 |
| $ per approved | ≤ $0.35 | $0.31 ✓ | $0.31 ✓ | $0.32 ✓ |
| calls |  | 562 | 493 | 471 |
| calls per approved |  | 2.12 | 2.14 | 2.22 |
| wall time h |  | 2.31 | 1.96 | 1.89 |
| days |  | 1 | 2 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 55 (4 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 8 (2 major), fact 2 (1 major), ambiguity 1 (1 major), overlap 5 (0 major), media 6 (3 major), difficulty 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 55 of 60 (92 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.29

Major findings on approved questions:

- **q-12584**: media, giveaway — The media is the problem. It is set as essential, so it shows sharp, and the file is "Santiago Giménez - 2023 (AI-generated version).jpg". That is a portrait of the answer, its title names him, and it is AI-generated, which shouldn't go on the TV. The question is a text question, so it needs an illustrative image that doesn't show him, such as a Feyenoord stadium. The facts check out: he was born in Buenos Aires, his father Christian "Chaco" Giménez played for Cruz Azul, his nickname is "Bebote" and he made his name at Feyenoord. None of the three wrong answers played for Feyenoord. I rate it a 6 against the given 4, which is within tolerance. (http://127.0.0.1:8001/review/q-12584)
- **q-12665**: fact — The question text says Siqueiros "la donó al público en 1969". He opened the Sala de Arte Público on 29 January 1969, but INBA and the CDMX government both date the donation (through a trust) to 12 December 1973, 25 days before he died. The fix is easy: "la abrió al público en 1969". The answer, the hints (revolutionary soldier, airbrush and Duco car paint, the Polyforum), the fun fact about Lecumberri, the media and the difficulty all check out, and nothing overlaps with the related questions. (http://127.0.0.1:8001/review/q-12665)

## Needs work

- **q-12550** (liga-mx) ¿Con qué apodo se conoce a este entrenador mexicano? → El Vasco: The description says he has coached in Spain and Japan. That is Aguirre's best-known trait among Mexican coaches, and it rules out Piojo, Tuca and Chepo before the photo or any hint. Rewrite the description so it jokes about coaching or the bench without naming countries or anything else only he has done.
- **q-12555** (lucha-libre) Mira: el réferi cuenta mientras el luchador está de espaldas sobre la lona. ¿Hasta qué número debe llegar para que se gane la caída? → 3: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-no notice).
- **q-12559** (mariachi-and-ranchera) ¿En qué mes se celebran las Fiestas Patrias de México, con el Grito, banderas y mariachis? → Septiembre: This repeats the fact in approved q-11631 ("En México, ¿qué día se celebra oficialmente la Independencia?" → 16 de septiembre). Both ask when Mexico celebrates Independence, so either one gives the other away. Drop it, or replace it with a different Fiestas Patrias fact (for example, where the president gives the Grito).
- **q-12560** (mariachi-and-ranchera) Escucha: este instrumento se toca en el mariachi tradicional y en el son jarocho. ¿Cuál es? → El arpa: The only audio candidate, "File:Arpeggio.ogg" (Mysid), doesn't say it's a harp. It's most likely the synthesized example from Wikipedia's "Arpeggio" article, so it may not sound like a harp at all. The essential audio needs a clearly labelled solo harp recording, for example from a search for "harp solo" or "arpa jarocha", but no new search is allowed in this run. The question text itself is fine. No se encontró una imagen adecuada para esta pregunta.
- **q-12589** (painters-and-muralists) Manuel Felguérez, Vicente Rojo y Fernando García Ponce le dieron la espalda al muralismo nacionalista y apostaron por lo abstracto. ¿Qué grupo formaban? → La Generación de la Ruptura: The answer overlaps approved questions: q-11542 names "Generación de la Ruptura" and Felguérez in its question text, and q-11618 says "los artistas de la Ruptura". Seeing either one gives this answer away. Hint 2 also points almost directly at "Ruptura", since the question already says they "turned their back" on muralism.
- **q-12593** (painters-and-muralists) La película «Frida» (2002), con Salma Hayek, ganó dos premios Óscar: uno a la mejor música original. ¿Cuál fue el otro? → Mejor maquillaje: Hint 2 ("una categoría técnica") gives the answer away: best actress, best picture and best director are not technical categories, so only makeup is left once hint 2 is read. Hint 1 had already ruled out best actress. Hint 2 should stay vague, for example about the night of the ceremony or the film's look, without saying the category is technical.
- **q-12613** (brands-and-snacks) Son botanas enrolladas, saben a chile con limón y la bolsa de los Fuego es morada. ¿De qué país son los Takis? → México: The text works, but no candidate fits. The slot needs a photo of Takis or rolled spicy tortilla chips. The candidates show two galaxies, two bowls of salsa and an old archaeological site plan. The salsa also points to Mexico. No new search is allowed, so the media slot can't be filled. No se encontró una imagen adecuada para esta pregunta.
- **q-12619** (tv-shows-and-hosts) En el programa de espectáculos «Ventaneando» de TV Azteca, ¿qué significa «ventanear» a un famoso? → Exhibir sus secretos en público: Verificación de datos: uncertain. I could not verify the exact meaning of «ventanear» from a source. The answer is plausible, and the wrong answers are clearly wrong.
- **q-12625** (christmas-season) Caminas de noche por la calle con una velita encendida, cantando para pedir posada. ¿En qué mes estás? → Diciembre: Overlap with approved q-10389, whose text states "En México las posadas empiezan justo el 16 de diciembre": seeing that question gives this one's answer away. Consider dropping this one or asking a different posadas fact.
- **q-12627** (civic-holidays) El 20 de noviembre hay desfiles deportivos en escuelas y ciudades de todo México. ¿Qué se conmemora? → La Revolución Mexicana: This question overlaps draft q-12629, whose text says "La Revolución que empezó el 20 de noviembre de 1910". Anyone who has seen that question already knows this answer. Keep only one of them, or reword q-12629 so it doesn't link 20 de noviembre to the Revolution. Also, hint 2 (Villa and Zapata) is close to giving the answer away for a hint that isn't the last one.
- **q-12631** (civic-holidays) Mira esta foto de cerca. ¿Cómo se llaman estas sorpresas de colores que se rompen en la cabeza durante las fiestas? → Cascarones: None of the candidates shows cascarones, the painted, confetti-filled eggs the essential image needs. They show hatching chicks and ducklings, a prickly-pear cactus, a craft panel and Filipino rice balls. No new search is allowed. You could add a Commons photo of Mexican confetti eggs by hand, or turn the question into a text-only one with an illustrative or decorative image. No se encontró una imagen adecuada para esta pregunta.
- **q-12636** (contemporary-cinema) ¿Qué película dirigió Alfonso Cuarón justo después de «Y tu mamá también» (2001)? → Harry Potter y el prisionero de Azkaban: The text is fine, but no media candidate works. 1, 5 and 6 are old maps, 2 is an 1883 village engraving and 3 is sheep in a corral, so none fits the road trip or Cuarón's films. 4 is the Mexican coast photographed from the ISS, which points to the wrong option «Gravedad». A new search such as "Oaxaca beach road" or "film clapperboard" is needed. No se encontró una imagen adecuada para esta pregunta.
- **q-12657** (national-symbols) Según la explicación más común en la escuela, ¿qué representa la franja verde de la bandera de México? → La esperanza: Hint 2 states that red is 'la sangre de los héroes', which is exactly the answer of draft q-12578 ('el rojo … representa «la sangre de los…»'), so seeing this question gives that one away. Replace hint 2 with a vaguer clue that doesn't reveal another colour's meaning (e.g. about the word in the saying or the feeling's link to the future).
- **q-12670** (regional-mexican) Completa el nombre del grupo que desde 1977 revivió los fandangos jarochos, fundado por Gilberto Gutiérrez: Mono… → Blanco: The fact check says 'wrong': hint 2 claims Mono Blanco was born in Tlacotalpan, but sources generally say Gilberto Gutiérrez founded it in Mexico City in 1977, and I can't confirm Tlacotalpan myself. Replace hint 2 with something verifiable, e.g. «El grupo se fundó en la Ciudad de México, pero su música es de raíz veracruzana.» Verificación de datos: wrong. Hint 2 says the group was born in Tlacotalpan, Veracruz. Mono Blanco was founded in 1977 in Mexico City by Gilberto Gutiérrez (Veracruz-born members, but not founded in Tlacotalpan). This is from memory; I did not search.
- **q-12696** (traditional-dances) Estás en Cuajinicuilapa, Guerrero, y por la calle bailan diablos con máscaras de crin al ritmo de una quijada de burro. ¿En qué fecha del año es? → En Día de Muertos: None of the media candidates fits: none shows a quijada de burro, the Danza de los Diablos or the Costa Chica, and no new search is allowed. The text itself is fine. It needs a new image search, e.g. "Danza de los Diablos Guerrero" or "donkey jawbone percussion". No se encontró una imagen adecuada para esta pregunta.
- **q-12701** (traditional-games) Juegas lotería y cantan «¡el gallo!», que está en tu tabla. ¿Qué pones tradicionalmente encima de la carta? → Un frijol: No candidate fits: all six are 19th-century stereograph cards of Santa Fe, New Mexico (a residence, pack burros), not a lotería game. A new search isn't allowed. The slot needs a picture of lotería cards or a lotería board ('loteria mexicana tabla'); since frijoles may appear on it, check that it doesn't show bean markers. No se encontró una imagen adecuada para esta pregunta.
- **q-12703** (traditional-games) Mira de cerca este juguete de Día de Muertos que mueve brazos y piernas. ¿Cómo se le dice en México? → Calaca: None of the candidates shows what the essential image must show: a close-up of an articulated Mexican skeleton toy that moves its arms and legs. #3 shows small clay skeleton figurines in a market, #4 and #5 are Catrina figures, #6 shows Coco merchandise, and #1 and #2 are unrelated. No new search is allowed. Either find a photo of a jointed calaca toy (a pull-string or jumping-jack skeleton) or reword the question so it doesn't refer to a moving toy shown in the photo. No se encontró una imagen adecuada para esta pregunta.
- **q-12704** (traditional-games) Es una carta de la Lotería mexicana: una mujer rema en una canoa llena de flores, como en Xochimilco. ¿Cómo se llama? → La Chalupa: Hint 2 gives the answer away. It says the card's name is a small boat, "not a person or an animal", which rules out La Dama, La Sirena and La Garza in one go. Replace it with a vaguer hint, for example about the card's usual verse or the trajineras of Xochimilco, without saying what kind of word the name is.
- **q-12720** (writers-and-poets) ¿En qué año publicó Octavio Paz la primera edición de su libro de poemas “Libertad bajo palabra”? → 1949: None of the six image candidates shows Octavio Paz. They're other people with "Paz" in their names (Elena Garro's family, Bolivian legislators, others), and no new search is allowed. The text itself is fine. A better search would be "Octavio Paz 1988" or "Octavio Paz writer", or an illustrative image such as "Palacio de Bellas Artes". No se encontró una imagen adecuada para esta pregunta.
- **q-12721** (writers-and-poets) Amado Nervo nació en 1870, fue diplomático y murió en Montevideo en 1919. ¿En qué estado actual está su ciudad natal? → Nayarit: No media candidate shows Amado Nervo or anything related to him: they are a botany plate, Luis Amado with the Obamas, and four portraits of the Brazilian writer Jorge Amado. A new search isn't allowed here. The slot needs a new search, for example "Amado Nervo" or "Tepic Nayarit cathedral". The text itself is fine. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 7, cause_effect 4, count 11, estimate 9, identify 33, made_of 21, name_concept 25, odd_one_out 9, origin 25, purpose 16, record 4, sequence 6, when 30, who 17, word_meaning 15
- stimulus: detail 6, map_outline 3, none 184, photo 37, sound 2
- clue: completion 7, direct 104, riddle 17, scenario 36, three_facts 68
- answer_kind: group 27, number 20, person 28, place 27, thing 52, time 32, word 46
- lens: body_senses 9, educational_media 19, everyday 47, history 47, language 43, nature 6, pop_culture 38, popular_science 2, school 15, science_news 2, university 4

## Dropped by the pipeline

- brands-and-snacks-17: overlap like brands-and-snacks-2: Son botanas enrolladas, saben a chile con limón y la bolsa de los Fuego es morada. ¿De qué país son los Takis? → México: Es blanco, usa gorro de cocinero y aparece en las bolsas de pan desde los años 40. ¿En qué país nació la marca del Osito Bimbo? → México
- christmas-season-0: overlap like q-0670: Cuelgo en las fiestas de cumpleaños y los niños me pegan con un palo con los ojos vendados. Cuando me rompo, ¿qué cae de mí? → Dulces y juguetes: Te tapan los ojos, te dan vueltas y todos cantan «Dale, dale, dale, no pierdas el tino». ¿Qué tienes en la mano? → Un palo
- christmas-season-13: overlap like q-12310: Se colocan en el belén, se venden en el mercado navideño de la Plaza Mayor de Madrid y las clásicas se pintan a mano. ¿De qué suelen ser? → De barro: En los nacimientos mexicanos tradicionales, como los de Tlaquepaque, ¿de qué material son las figuritas de la mula y el buey? → De barro
- christmas-season-15: overlap like q-6902: Este animal es plato de Navidad en muchas casas colombianas. ¿De qué continente es originario? → América: Te sirven pavo en la cena de Nochebuena; en México también le dicen guajolote. ¿Desde cuándo se cría en México? → Desde antes de que llegaran los españoles
- civic-holidays-12: overlap like q-4264: Look closely at Mexico's flag. How many animals can you find on it? → 2: En el centro de las banderitas tricolores está el escudo nacional. ¿Cuántos animales aparecen en él? → 2
- civic-holidays-14: overlap like q-4755: Mariachi bands wear the charro suit, with silver buttons and a huge hat. Who first wore this kind of outfit in Mexico? → Ranch horsemen: Mira la foto. ¿Cómo se llama este traje típico de México? → Traje de charro
- conquest-and-colony-1: overlap like q-10107: El tornaviaje lo descubrió Urdaneta en 1565: subía hasta la altura de Japón para coger vientos del oeste y llegaba a Acapulco. ¿Desde dónde salía? → Desde Filipinas: La Nao de China llegaba a Acapulco cargada de seda y porcelana, pero no zarpaba de China. ¿De qué ciudad salía? → Manila
- conquest-and-colony-6: overlap like q-10230: En muchas ofrendas se sirve la bebida favorita del difunto, como el pulque. ¿De qué planta sale el pulque? → Del maguey: En una pulquería de la Nueva España te servían una bebida blanca, espesa y fermentada. ¿De qué planta salía? → Del maguey
- conquest-and-colony-7: overlap like q-12500: Si te sale el muñequito de la rosca el 6 de enero, te toca invitar tamales el Día de la Candelaria. ¿Cuántos días después es? → 27: El 2 de febrero, Día de la Candelaria, a alguien le toca invitar los tamales. ¿A quién? → A quien le salió el muñequito en la rosca
- drinks-8: overlap like q-4532: This tropical fruit has a crown of spiky leaves, a rough, scaly skin and sweet yellow flesh. What is it? → Pineapple: Con esta fruta se prepara el agua fresca que mejor va con los tacos al pastor. ¿Qué fruta es? → La piña
- drinks-14: overlap like q-10011: La sidra es la bebida más famosa de Asturias y se sirve echándola desde muy alto. ¿De qué fruta se hace? → De la manzana: En muchas casas de México se destapa esta bebida burbujeante para brindar en Navidad y Año Nuevo. ¿De qué fruta se hace? → De manzana
- indigenous-words-1: overlap like q-10306: Teotenango, la ciudad amurallada del Estado de México, significa en náhuatl "en la muralla de los…". ¿De los qué? → Dioses: Los mexicas hallaron una ciudad abandonada con dos pirámides gigantes y la llamaron Teotihuacan. ¿Qué significa ese nombre? → Ciudad de los dioses
- indigenous-words-3: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 4: Mi nombre viene de los mexicas, mi capital se llama casi igual que yo y aquí se comen tacos y tamales. ¿Cómo me llamo? → México
- indigenous-words-17: overlap like q-0625: Estos dibujos hechos en roca se llaman petroglifos. 'Petro' significa piedra en griego. ¿Qué significa 'glifo'? → Grabado: Los mayas los tallaban en estelas de piedra, cada uno podía ser una sílaba o una palabra entera, y en Palenque hay cientos. ¿Qué es un glifo? → Un signo de escritura
- legends-8: overlap like q-10233: Aguascalientes celebra cada año el Festival de Calaveras en honor al autor de este grabado, nacido en esa ciudad. ¿Quién fue? → José Guadalupe Posada: Este grabado de una calavera con sombrero ilustraba calaveritas literarias a principios del siglo XX. ¿Quién lo hizo? → José Guadalupe Posada
- legends-10: overlap like q-12545: Estás viendo la película de la saga Leyendas donde Leo San Juan enfrenta momias que salen del panteón. ¿En qué ciudad sucede? → Guanajuato: Vivo en la Nueva España, ya vencí a la Nahuala, a la Llorona, a las momias y al Chupacabras, y en mi quinta aventura un jinete de negro quiere mi alma. ¿Quién soy? → Leo San Juan
- lucha-libre-0: overlap like q-10272: Está en la colonia Doctores, abrió en 1956 y es sede de la empresa más antigua del mundo de su deporte. ¿De qué deporte es «la Catedral» la Arena México? → La lucha libre: Mira estos puestos de máscaras. Son una tradición frente a la arena más famosa de la colonia Doctores, en la CDMX. ¿Cuál es? → La Arena México
- lucha-libre-11: overlap like q-11465: Su dueño se enfrentó a momias y vampiros en más de 50 películas y lo enterraron con ella en 1984. ¿Qué máscara de luchador salió en más películas que ninguna? → La de El Santo: ¿Qué legendario luchador mexicano hizo famosa una máscara plateada como esta? → El Santo
- mariachi-and-ranchera-12: overlap like q-11507: ¿Qué cantante, conocido como «El Lujo de México», integró el trío Los Tres Ases antes de su carrera solista? → Marco Antonio Muñiz: ¿Quién NO formó parte del trío de boleros Los Tres Ases? → Chucho Navarro
- mariachi-and-ranchera-15: overlap like q-11680: En unos XV años, son los muchachos que bailan el vals con la quinceañera, ensayan por semanas y van vestidos igualitos. ¿Cómo se llaman? → Los chambelanes: En una fiesta de XV años, ¿quiénes son los «chambelanes»? → Los muchachos que bailan el vals con la quinceañera
- maya-3: overlap like q-10436: En el juego de pelota que los mexicas llamaban tlachtli, las canchas tenían aros de piedra como este. ¿Para qué servían? → Para pasar la pelota por dentro: Tengo forma de I mayúscula, unos muros altísimos y dos aros de piedra en lo alto; si aplaudes en mí, el eco se repite. ¿Qué soy? → Un juego de pelota
- maya-10: overlap like conquest-and-colony-0: En Chichén Itzá hay un edificio redondo con una escalera de caracol por dentro y ventanitas en lo alto. ¿Para qué lo usaban los mayas? → Para observar el cielo: Mira esta torre redonda: desde sus ventanas, los mayas seguían los movimientos de Venus. ¿En qué zona arqueológica está? → Chichén Itzá
- money-5: overlap like q-10189: Taxco, en Guerrero, tiene calles empinadas, el templo de Santa Prisca y muchísimos talleres. ¿Qué artesanos lo hicieron famoso? → Los plateros: Mira estas joyas de plata. ¿Qué pueblo de Guerrero es famoso en todo México por hacer joyería así? → Taxco
- national-symbols-0: overlap like q-12559: ¿En qué mes se celebran las Fiestas Patrias de México, con el Grito, banderas y mariachis? → Septiembre: ¿En qué mes se llenan de papel picado verde, blanco y rojo las calles y escuelas de México? → Septiembre
- national-symbols-5: overlap like q-7283: Cuando el Gobierno declara duelo nacional, la bandera se iza así, sin llegar a lo más alto. ¿Cómo se dice? → A media asta: Soy alto, delgado y muy derecho, y cada lunes en la escuela suben la bandera por mí con una cuerda. ¿Qué soy? → El asta
- national-symbols-11: overlap like q-10322: Los mexicas salieron de Aztlán y caminaron años buscando un águila sobre un nopal devorando una serpiente. ¿Qué les indicaba esa señal? → Dónde fundar su ciudad: Este escudo va en la franja blanca de la bandera. ¿Sobre qué planta está parada el águila? → Un nopal
- national-symbols-17: overlap like q-10201: Al saludar a la bandera en los honores, ¿cómo se pone la mano sobre el pecho? → La derecha, con la palma hacia abajo: Mano derecha extendida sobre el pecho, palma hacia abajo, a la altura del corazón: así lo haces en los honores. ¿Cómo se llama ese gesto? → El saludo civil
- other-sports-10: overlap like q-11584: En la lucha libre mexicana, ¿qué es un luchador «rudo»? → El villano que hace trampa: En la lucha libre mexicana, desde los tiempos de El Santo, hay dos bandos: técnicos y rudos. ¿Quiénes son los rudos? → Los 'malos', que hacen trampa
- other-sports-11: overlap like q-3054: Which Olympic combat sport comes from Korea and is famous for high and spinning kicks? → Taekwondo: Se practica descalzo y con un peto que marca los puntos. Sus cintas van de la blanca a la negra, y Guillermo Pérez ganó en él un oro olímpico para México. ¿Qué deporte es? → El taekwondo
- painters-and-muralists-12: overlap like q-6129: Frida Kahlo, the Mexican painter with flowers in her hair and famous joined eyebrows, painted which kind of picture more than any other? → Self-portraits: Mira el rostro de esta pintora mexicana. ¿Qué rasgo suyo se volvió famoso en todo el mundo? → La uniceja
- painters-and-muralists-15: overlap like q-4659: Diego Rivera painted his huge murals as frescoes, just like Michelangelo. What is a fresco? → Paint on wet plaster: Orozco pintó al fresco murales como este, en el Hospicio Cabañas de Guadalajara. ¿Sobre qué se aplica la pintura en esa técnica? → Sobre cal todavía húmeda
- pre-hispanic-gods-4: overlap like q-10231: Para los mexicas, quien moría de forma natural viajaba cuatro años, cruzando nueve niveles y guiado por un perro. ¿A dónde llegaba? → Al Mictlán: Para llegar al Mictlán, el alma pasaba entre cerros que chocan, vientos de navajas y ríos. ¿Cuántos años duraba ese viaje? → 4
- pre-hispanic-gods-9: overlap like q-10427: Este volcán nevado, vecino del Popocatépetl, es famoso por la figura que forma su silueta. ¿Qué figura parece? → Una mujer dormida: Según la leyenda, la princesa Iztaccíhuatl se quedó dormida para siempre y el guerrero Popocatépetl se arrodilló a cuidarla. ¿En qué se convirtieron? → En volcanes
- regional-mexican-6: overlap like q-1986: Soy de Jalisco, México, canto corridos tumbados y en 2023 'Ella baila sola' me hizo famoso en todo el mundo. ¿Quién soy? → Peso Pluma: El cantante de «Ella baila sola» tomó su nombre artístico de una categoría del boxeo para peleadores ligeros. ¿Cuál? → Peso pluma
- regional-mexican-15: overlap like q-7596: Escucha: ¿qué instrumento es este? → El acordeón: Escucha: este instrumento no falta en las canciones de Grupo Firme y del norteño. ¿Cuál es? → El acordeón
- boxing-5: hard fail: correct 5, unambiguous 3, no_giveaway 3, no_overlap 5: Es verde con oro, trae las banderas de los países miembros y lo entrega un consejo con sede en la Ciudad de México. ¿Qué gana quien se lo lleva? → El título de campeón mundial
- boxing-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Su límite ronda los 72,6 kilos, Julio César Chávez Jr. fue campeón del CMB en ella y Canelo peleó ahí contra Golovkin. ¿Qué división es? → Peso medio
- boxing-12: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Estoy en Canastota, un pueblito de Nueva York. Cada junio recibo nuevos inquilinos y ya guardo a Julio César Chávez, Salvador Sánchez y Rubén Olivares. ¿Qué soy? → El Salón de la Fama del Boxeo
- boxing-15: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Saúl Álvarez nació en Jalisco, tiene muchas pecas y desde niño le dicen "Canelo". ¿De dónde viene ese apodo? → De su pelo rojizo
- writers-and-poets-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Federico Gamboa admiraba a Émile Zola y retrató el México porfiriano en su novela “Santa” (1903). ¿A qué corriente literaria pertenece? → Naturalismo
- brands-and-snacks-10: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: En muchas esquinas de México hay carritos que venden vasitos de pepino, jícama y mango. ¿Qué se les pone casi siempre encima? → Chile en polvo y limón
- brands-and-snacks-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: Chedraui empezó como una pequeña mercería y sus fundadores eran inmigrantes libaneses. ¿En qué estado del Golfo de México nació? → Veracruz
- conquest-and-colony-10: overlap like q-10212: Tras su encuentro con Cortés en 1519, Moctezuma acabó prisionero de los españoles. ¿Quién gobernó a los mexicas justo después de él? → Cuitláhuac: Usaba un gran penacho de plumas y gobernó cuando llegaron los españoles. ¿Qué pueblo gobernaba Moctezuma? → Los mexicas
- drinks-0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: En el mercado te sirven café de olla en un recipiente rojizo, con asa, que deja un saborcito a tierra. ¿Qué es? → Un jarrito de barro
- drinks-1: hard fail: correct 3, unambiguous 5, no_giveaway 3, no_overlap 5: ¿De dónde es originaria la papaya, la fruta del clásico licuado de mercado? → Del sur de México y Centroamérica
- folk-beliefs-1: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Según una creencia muy mexicana, ¿qué significa que te dé comezón en la palma de la mano? → Que te va a llegar dinero
- folk-beliefs-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Se vende en pomada o en alcohol y las abuelas la untan en golpes, moretones y torceduras. ¿De dónde sale el árnica? → De una planta de flores amarillas
- golden-age-cinema-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: ¿En qué década se estrenó «Río Escondido», la película en la que María Félix es una maestra rural? → En los años 40
- legends-11: fact-check wrong: Fun fact: the 'amarrar al diablito' custom could not be found. The known Mexican custom for lost objects is tying knots in a cloth/handkerchief to San Antonio or San Cucufato. Main answer (duendes) is plausible.: Se te pierden las cosas en la casa y nadie sabe dónde quedaron. En México, ¿a quiénes se les echa la culpa? → A los duendes
- liga-mx-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Este equipo de Monterrey nació en 1945 y también es conocido como «La Pandilla». ¿Cuál es? → Rayados
- lucha-libre-17: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Al terminar una lucha de máscara contra máscara, ¿quién se quita la máscara y dice su nombre real frente al público? → El luchador que perdió
- mariachi-and-ranchera-16: fact-check wrong: Fun fact is false: Vicente Fernández's 2016 farewell concert 'Un Azteca de Rey' at Estadio Azteca was a paid, ticketed show, not free.: Una gran arena de conciertos en Jalisco lleva las iniciales de un ídolo de la música ranchera. ¿De quién? → Vicente Fernández
- maya-7: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 4: En 1952, un arqueólogo halló bajo el piso de un templo de Palenque una escalera oculta hasta la tumba de Pakal. ¿En qué templo fue? → Templo de las Inscripciones
- money-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: La moneda de 20 pesos tiene 12 lados. ¿De qué está hecha? → De dos metales distintos
- money-15: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Muchas empresas en México dan a sus trabajadores «vales de despensa». ¿Qué son? → Saldo para el súper
- painters-and-muralists-3: hard fail: correct 2, unambiguous 5, no_giveaway 4, no_overlap 4: Diego Rivera, José Clemente Orozco y un tercer muralista son conocidos como «los tres grandes». ¿Quién completa el trío? → David Alfaro Siqueiros
- pre-hispanic-gods-7: overlap like q-10423: En Chichén Itzá, la gran pirámide de El Castillo tiene escaleras que suben hasta su templo. ¿Cuántas escaleras tiene? → 4: Estás en Chichén Itzá contando todos los escalones de El Castillo: los cuatro lados y la plataforma de arriba. ¿Cuántos son? → 365
- regional-mexican-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Requinto, guitarra de doce cuerdas, letras de desamor y tono melancólico: ¿qué estilo hizo famoso Junior H? → Sad sierreño
- states-and-capitals-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Sales en carro de la Ciudad de México hacia el poniente, subiendo por La Marquesa. ¿A qué capital estatal llegas primero? → Toluca
- traditional-dances-9: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 5: En el norte de México se bailan ritmos llegados de Europa. Completa: la polka es a Bohemia como ¿qué baile es a Polonia? → La mazurca
- states-and-capitals-4: overlap like q-11682: La ciudad donde se celebra la Guelaguetza lleva oficialmente el apellido de un presidente de México. ¿De cuál? → Benito Juárez: Mira el mapa: cada julio, la capital de este estado celebra la Guelaguetza con danzas de todas sus regiones. ¿Qué estado es? → Oaxaca
- states-and-capitals-12: duplicate like q-10334: Los huevos motuleños de la foto llevan el nombre del pueblo donde se inventaron. ¿En qué estado está? → Yucatán: Mira el mapa: en este estado el Día de Muertos se llama Hanal Pixán y se come mucbipollo. ¿Qué estado es? → Yucatán
- states-and-capitals-14: overlap like q-1612: Soy una ciudad maya sobre un acantilado frente al Caribe mexicano, y mi nombre dice lo que me rodea. ¿Qué significa «Tulum»? → Muralla: Esta ciudad amurallada se construyó en lo alto de un acantilado frente al mar Caribe. ¿Qué pueblo antiguo la levantó? → Los mayas
- telenovelas-5: overlap like q-11585: Antes de ser telenovela con Bárbara Mori en 2004, «Rubí», de Yolanda Vargas Dulché, nació en otro formato. ¿Cuál? → Una historieta: Soy bella y ambiciosa, nací pobre y en 2004 dejé al amor de mi vida para casarme con un millonario. ¿Quién soy? → Rubí
- traditional-dances-2: overlap like q-10320: Estos danzantes giran colgados de un poste altísimo. ¿De qué ciudad de México son los más famosos? → Papantla: Antes se cortaba un árbol entero en el monte para hacer este poste, desde el que bajan cuatro hombres girando de cabeza. ¿Qué ciudad veracruzana es famosa por esta tradición? → Papantla
- traditional-dances-4: overlap like q-10434: Esta pieza mexica de hace unos 500 años está hecha con plumas verdes de quetzal. ¿Qué tipo de objeto es? → Penacho: Voy en la cabeza de los danzantes aztecas, soy muy alto y de colores, y me muevo cada vez que giran. ¿Qué soy? → Un penacho
- traditional-dances-8: overlap like mariachi-and-ranchera-15: En una fiesta de XV años, ¿quiénes son los «chambelanes»? → Los muchachos que bailan el vals con la quinceañera: Completa el título de la canción de Chayanne que suena en muchísimos XV años: «Tiempo de…» → vals
- traditional-dances-11: overlap like q-11448: La polka, que sigue viva en la música norteña, llegó al norte de México en el siglo XIX. ¿Quiénes la trajeron? → Inmigrantes alemanes y checos: El vals norteño se baila en tres tiempos, con bajo sexto y acordeón. ¿Cómo llegó el acordeón al norte de México? → Con inmigrantes alemanes y checos
- traditional-games-2: overlap like q-7380: ¿Para qué sirve recitar el «Tin marín de do pingüé»? → Para escoger a alguien al azar: Se recita en el patio, el dedo salta de un niño a otro y dice «cúcara mácara títere fue». ¿Para qué sirve «De tin marín»? → Para escoger a alguien
- traditional-games-4: overlap like q-7191: En la canción 'Un elefante se balanceaba', cuando el elefante ve que la tela de araña resiste, ¿a quién va a llamar? → A otro elefante: Mira este animal. En una canción infantil muy famosa, se columpiaba sobre… ¿qué? → La tela de una araña
- traditional-games-11: overlap like q-6449: Kids do it in the playground, boxers train with it, and Guinness counts how many jumps you can do with it in 30 seconds. What is it? → Jump rope: Mira la foto. ¿A qué están jugando? → A brincar la cuerda
- traditional-games-17: overlap like q-10223: Se hace girar sobre la mesa, tiene seis caras y en ellas dice cosas como 'toma todo' o 'todos ponen'. ¿Cómo se llama? → Pirinola: Juegas pirinola con dulces: si cae en «Toma todo», te llevas el montón entero. ¿Cuántas caras tiene la pirinola? → 6
- writers-and-poets-3: overlap like q-10187: Soy dueño de la Media Luna y mando en Comala. Mi hijo llega a buscarme y solo encuentra murmullos. ¿Quién soy? → Pedro Páramo: Si llegas a Comala con Juan Preciado a buscar a su papá, ¿por quién tienes que preguntar? → Pedro Páramo
