# batch-42

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: spain
- Language: Spanish (Spain)
- Subcategories (27): legends-and-superstitions, radio-and-internet, sayings, rivers-and-mountains, brands-and-shops, bourbons-and-19th-century, co-official-languages, ancient-hispania, sportspeople, coasts-and-islands, famous-figures, current-music, empire, footballers-and-national-team, national-symbols, wildlife, christmas-and-holidays, spanish-cinema, modern-literature, slang, ham-cheese-and-produce, folk-music-and-dance, pop-and-rock, sweets-and-desserts, regional-symbols, scientists-and-explorers, comics-and-childrens-books
- Merged: 264 (q-13212…q-13475)
- Approved: 238
- Needs work: 26
- Dropped by the pipeline: 78
- Reviewed by: claude-opus-5-5
- Claude calls: 573, about $78.25 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-40, batch-41; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-40 | batch-41 | batch-42 |
|---|---|---:|---:|---:|
| source locale |  | en | de | es-ES |
| drafts |  | 310 | 336 | 342 |
| skipped slots |  | 140 | 150 | 144 |
| dropped |  | 82 | 77 | 78 |
| drop rate | ≤ 20.0 % | 26.5 % ✗ | 22.9 % ✗ | 22.8 % ✗ |
| dropped: hard fail correct |  | 2 | 0 | 5 |
| dropped: hard fail unambiguous |  | 1 | 2 | 0 |
| dropped: hard fail no_giveaway |  | 26 | 21 | 17 |
| dropped: overlap |  | 53 | 51 | 54 |
| dropped: duplicate |  | 1 | 2 | 2 |
| dropped: fact-check wrong |  | 1 | 1 | 1 |
| merged |  | 228 | 259 | 264 |
| approved |  | 214 | 243 | 238 |
| needs_work |  | 14 | 16 | 26 |
| needs_work rate | ≤ 20.0 % | 6.1 % ✓ | 6.2 % ✓ | 9.8 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.2 % ✓ | 1.5 % ✓ | 3.8 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.4 % ✓ | 0.4 % ✓ | 0.8 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.4 % ✓ | 0.8 % ✓ | 1.5 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.5 % ✓ | 3.9 % ✓ | 4.5 % ✓ |
| media: no pick in review 1 |  | 27 | 49 | 34 |
| media: recovered by research |  | 22 | 40 | 23 |
| media: no pick at record |  | 6 | 9 | 11 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 17.7 % ✓ | 16.4 % ✓ | 17.5 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 58.0 % ✓ | 63.3 % ✓ | 58.3 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.75 ✗ | 1.29 ✓ | 1.00 ✓ |
| approved 11–15 |  | 47 | 60 | 54 |
| top move | ≤ 25.0 % | 20.2 % ✓ | 13.9 % ✓ | 18.9 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 72.4 % | 78.4 % | 72.7 % |
| values stimulus |  | 5 | 5 | 6 |
| top clue | ≤ 60.0 % | 47.8 % ✓ | 46.7 % ✓ | 50.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 23.7 % ✓ | 26.3 % ✓ | 20.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 17.5 % ✓ | 25.1 % ✗ | 19.3 % ✓ |
| values lens |  | 11 | 10 | 11 |
| media share | 15.0 %–50.0 % | 27.6 % ✓ | 21.6 % ✓ | 27.3 % ✓ |
| mean fun | ≥ 3.40 | 3.56 ✓ | 3.40 ✗ | 3.45 ✓ |
| cost $ |  | $64.05 | $73.68 | $74.70 |
| $ per approved | ≤ $0.35 | $0.30 ✓ | $0.30 ✓ | $0.31 ✓ |
| calls |  | 470 | 498 | 513 |
| calls per approved |  | 2.20 | 2.05 | 2.16 |
| wall time h |  | 1.84 | 2.15 | 2.05 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 54 (0 %)
- Major among review needs work: 0 of 6 (0 %)
- Problems by kind: giveaway 6 (0 major), fact 1 (0 major), overlap 2 (0 major), media 2 (0 major), difficulty 1 (0 major), style 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.55

Major findings on approved questions:

None.

## Needs work

- **q-13213** (ancient-hispania) Estás en la cueva de Altamira, mirando los bisontes pintados en el techo. ¿Cuándo se pintaron? → Hace más de 10 000 años: This overlaps with approved q-9864 («¿Quiénes pintaron estos bisontes en la cueva de Altamira?» → Cazadores del Paleolítico). Both ask about the age and makers of the same Altamira bison, and seeing «Paleolítico» in that answer settles this one, because «Hace más de 10 000 años» is the only option left that fits it. The media is fine (candidate 4).
- **q-13224** (bourbons-and-19th-century) La Diada de Cataluña, cada 11 de septiembre, recuerda la caída de Barcelona ante las tropas de Felipe V. ¿En qué año fue? → En 1714: This overlaps approved q-9873. That question says Barcelona "resistió un largo asedio hasta 1714", which is the exact fact this question asks for (the year Barcelona fell to Felipe V). Anyone who has seen q-9873 knows the answer here. Drop this question or ask about a different Diada fact.
- **q-13225** (bourbons-and-19th-century) Reino en el siglo XVIII: el rey manda en todo, pero quiere escuelas, ciencia y progreso. Mi lema: «Todo para el pueblo, pero sin el pueblo». ¿Qué soy? → El despotismo ilustrado: The description gives the answer away. «Muchas ganas de cambiar el mundo… desde el trono» states the defining trait of enlightened despotism: reform imposed by an absolute monarch. Read with only the four options, it rules out parlamentarismo and liberalismo (not from the throne) and feudalismo (no reforming zeal). Rewrite it to play on the 18th-century court theme, for example wigs and palaces, without the idea of reform from above.
- **q-13243** (christmas-and-holidays) En la cabalgata ves a Melchor, con su barba blanca, y a Baltasar. ¿Cómo se llama el tercer Rey Mago? → Gaspar: The approved question q-9881 says «Melchor, Gaspar y Baltasar» in its text, so a player who has seen it already has the answer here. The two questions overlap too much to keep both. Drop this one or rework it so that q-9881 doesn't give it away.
- **q-13247** (co-official-languages) En sus comunidades, el catalán, el gallego y el euskera tienen el mismo rango que el castellano, como permite la Constitución de 1978. ¿Cómo se llaman? → Lenguas cooficiales: Hint 2 gives the answer away. «El nombre indica que son oficiales "junto con" otra lengua» puts the word «oficiales» in the hint, and only «Lenguas cooficiales» contains it, so the hint settles the question at step 2. Hint 2 should point to the shared status without using the answer's own word, for example by saying both languages can be used with the authorities and in schools.
- **q-13251** (coasts-and-islands) Mira el mapa: ¿qué océano está marcado, el que baña las costas de Galicia y Portugal? → El océano Atlántico: No candidate is the essential map the question needs: a blank map of the Iberian Peninsula with the ocean west of Galicia and Portugal highlighted or marked. #1 and #4 are old world maps with printed ocean names (#4 clearly says «Atlantic»). #2 and #3 are diagrams of map projections with nothing marked. No new search is allowed, so the media has to be sourced by hand (for example a blank Iberia map with the Atlantic shaded), or the question reworded so it doesn't depend on a marked map. No se encontró una imagen adecuada para esta pregunta.
- **q-13258** (coasts-and-islands) Mira el mapa de España: ¿qué costa está marcada? → La Costa del Sol: No candidate works as the essential map. #1 is the only relevant one, but it is a labelled map of Andalusia, not a blank map of Spain. Its German labels name Málaga and the comarcas, and the highlighted strip appears to be labelled with the comarca name "Costa del Sol Occidental", which gives the answer away. A new search isn't allowed, so the question needs a hand-picked or custom blank locator map of Spain with the Málaga coast highlighted, or it should be dropped. No se encontró una imagen adecuada para esta pregunta.
- **q-13262** (coasts-and-islands) Mira el mapa de España: ¿qué costa está marcada? → La Costa Brava: None of the candidates shows a blank map of Spain with the Girona coast highlighted. They are maps of Brava in Cape Verde, Punta Brava in Havana, an Álava municipality and Ribeira Brava in Madeira. No new search is allowed, so the essential map has to be found by hand, for example a Costa Brava locator map on Commons or a Spain map with the Girona coast marked. No se encontró una imagen adecuada para esta pregunta.
- **q-13272** (current-music) El cantante de «Quédate», el gran éxito de 2022 con Bizarrap, se crio en la isla de esta foto. ¿En cuál? → Gran Canaria: The question text calls «Quédate» with Bizarrap 'el gran éxito de 2022', which is exactly the answer to the approved q-11166 (the year of the Quevedo/Bizarrap «Quédate» session), so seeing this question gives that one away. Dropping 'de 2022' from the question text would remove the overlap. The facts are fine: Quevedo was born in Madrid and raised in Gran Canaria, which is the third-largest island and roughly round.
- **q-13322** (national-symbols) Mira esta moneda española de 50 céntimos. ¿Qué escritor aparece en ella? → Miguel de Cervantes: The real Spanish 10/20/50-cent coins have Cervantes' name engraved in script beside the portrait, as candidate 1 clearly shows ('Cervantes' next to a quill). So any essential photo of the coin gives the answer away, and the rater's note that the name isn't on the coin is wrong. The question needs a different approach, for example a decorative or illustrative image with no coin, and asking 'which writer appears on Spain's 10, 20 and 50 cent coins?'. Candidate 1 is also the 10-cent coin, not the 50-cent coin the text names. No se encontró una imagen adecuada para esta pregunta.
- **q-13336** (regional-symbols) Esta bandera de triángulos blancos y negros es casi igual que la de Lisboa. ¿De qué ciudad española es? → Ceuta: No candidate shows the flag of Ceuta, and the question needs it as essential media ("Esta bandera…"). Candidates 1, 3 and 4 are maps labelled "Ceuta", candidate 2 is a «Ceuta Ya» logo, and all of them give the answer away. 5 and 6 are unrelated maps or satellite views. A new search isn't allowed, so the file needs to be set by hand, for example File:Flag of Ceuta.svg from Commons. No se encontró una imagen adecuada para esta pregunta.
- **q-13355** (comics-and-childrens-books) El botones Sacarino, de Francisco Ibáñez, siempre está liándola en su trabajo. ¿Dónde trabaja? → En la redacción de un periódico: La imagen elegida tiene una licencia no adecuada (pd-us-only: PD-US-expired).
- **q-13360** (comics-and-childrens-books) ¿Cuál de estos personajes NO es compañero de aventuras del Capitán Trueno? → Robin: Hints 1 and 2 give the answer away: in a «which is NOT a Trueno companion» question, hint 1 («de un tebeo estadounidense») already picks out the one non-Spanish character. Hint 2 («joven ayudante de un superhéroe con antifaz y capa») is simply Robin's definition. Hint 1 should be a vague hint (e.g. about the era or the kind of story), and hint 2 should not describe Robin outright; only hint 3 may come that close.
- **q-13366** (famous-figures) Si el Goya es al cine, la estrella Michelin es a… → Los restaurantes: The text is fine, but no candidate shows a Goya statuette (or anything Michelin-related). They are unrelated awards: a Polish atheist award, a porcelain Figaro figure, nativity figurines, two 1930 Oscar photos and a Russian Wiki-award. Another search isn't allowed, so the media slot needs a new search such as "Premios Goya statuette" or a "fine dining plate" image. No se encontró una imagen adecuada para esta pregunta.
- **q-13380** (ham-cheese-and-produce) Mira este chorizo hecho a la manera tradicional. ¿De qué está hecha su piel? → De tripa: The question says «Mira este chorizo», but none of the six candidates shows a chorizo. They show twine spools, baptism amulets, chili ristras, a garlic braid and a kitchen. No new search is allowed, so the slot needs a real chorizo photo (e.g. "chorizo sausage" or "chorizo sarta") from a new media run. No se encontró una imagen adecuada para esta pregunta.
- **q-13400** (rivers-and-mountains) La Cueva de Nerja, en Málaga, se descubrió en 1959. ¿Quién la encontró? → Cinco chicos del pueblo: Hint 1 («No eran científicos ni trabajaban allí») rules out the archaeologists and the coal miners outright, and arguably the shepherd too, who works in that countryside. That leaves only the five local boys at the first hint. Hint 1 should be vague, for example about the season or the year's mood, and shouldn't knock out options.
- **q-13401** (sayings) Según la explicación más popular, ¿qué era el «ocho» de la expresión «más chulo que un ocho»? → Un tranvía: Hint 2 («Circulaba por raíles») settles it: only the tram among the four options runs on rails, so hint 2 gives the answer away (hint 1 already narrows it to horse or tram). Hint 2 should be weaker, for example about the 8 being a number or a line, without naming rails. The media is fine: candidate 1.
- **q-13403** (scientists-and-explorers) «Soy de Alcaraz y en 1587 se publicó con mi nombre un libro que decía que las penas y las alegrías afectan a la salud.» ¿Quién soy? → Oliva Sabuco: Verificación de datos: uncertain. Oliva Sabuco (Alcaraz, 'Nueva filosofía de la naturaleza del hombre', 1587) is correct. Hint 3 is loose: the olive tree is 'olivo', and 'oliva' is the fruit.
- **q-13409** (sportspeople) El donostiarra Lucas Eguibar fue campeón del mundo de snowboard en 2017, en Sierra Nevada. ¿En qué modalidad? → Snowboard cross: The fun fact is wrong: it says Eguibar finished fourth at the 2018 Olympics, but he went out in the 1/8 finals at Pyeongchang (Regino Hernández won the Spanish bronze). Correct the fun fact or drop the Olympic claim, e.g. «Eguibar ganó aquel título mundial en casa, en Sierra Nevada (Granada).» Verificación de datos: wrong. The fun fact says Eguibar was fourth at the 2018 Olympics. He crashed out in the 1/8 final at Pyeongchang 2018 and finished about 33rd. The Spanish rider who medalled there was Regino Hernández (bronze).
- **q-13413** (sweets-and-desserts) Mira la foto: son palitos secos de la raíz de una planta. Hace décadas, ¿para qué los compraban los niños en España? → Para masticarlos como golosina: No candidate shows what the essential image needs: dried liquorice root sticks (paloduz). #1 shows small chopped chips of root, not sticks. #2 is a botanical drawing of the whole plant, and #3 is an unrelated engraving of fruit. No new search is allowed. Hint 2 («Tenían un sabor dulce y un poco anisado») also gives the answer away: the sweet taste rules out chalk, whistles and bait. It should become a vaguer hint, for example about where the root grows or what it looks like. No se encontró una imagen adecuada para esta pregunta.
- **q-13425** (sayings) Oyes un trueno enorme en mitad de la noche y se te ponen los… de punta. ¿Qué completa la frase? → Pelos: Hint 2 («Se cortan en la peluquería») gives the answer away: «peluquería» even contains «pelo», and against the four options it points straight to «Pelos». Replace it with a hint that doesn't name or suggest the hairdresser, e.g. «Los gatos los erizan cuando se asustan».
- **q-13427** (sayings) «Estar como una cabra» es estar un poco loco. ¿Con cuál de estas comparaciones NO se dice lo mismo? → «Como un roble»: The text is fine, but none of the image candidates shows a goat. No new search is allowed, so the media slot can't be filled. It needs a clear photo of a goat on rocks, for example from the search "mountain goat rocks" or "domestic goat cliff". No se encontró una imagen adecuada para esta pregunta.
- **q-13435** (scientists-and-explorers) De estos cuatro grandes poetas españoles del siglo XX, ¿cuál ganó el Premio Nobel de Literatura? → Juan Ramón Jiménez: The clue also fits Vicente Aleixandre, a 20th-century Spanish poet who won the Nobel Prize in Literature in 1977. The question only works through «de estos cuatro», which the house style rules out. Use a clue only Juan Ramón Jiménez has, for example «¿Qué poeta español ganó el Premio Nobel de Literatura en 1956?», and move or replace hint 1, which gives that year.
- **q-13438** (slang) Cuando alguien exclama «¡Caramba!», ¿qué está mostrando normalmente? → Sorpresa: The question text is fine, but none of the image candidates works, and no new search is allowed. #1 is a nude body (not family-friendly), #2 shows a sleeping woman, which points to the wrong option «Sueño». #3 is a church statue, #4 a caricaturist drawing a calm boy, #5 a medical photo of a baby with chickenpox, and #6 an old Sunday-school group photo. A new search such as "surprised face reaction" or "cartoon surprise expression" is needed. No se encontró una imagen adecuada para esta pregunta.
- **q-13459** (sweets-and-desserts) Estás preparando manzanas asadas y les quitas el corazón antes de meterlas al horno. ¿Para qué es ese hueco? → Para rellenarlo de azúcar y mantequilla: Hint 2 ("Al salir del horno, ese hueco está lleno de un almíbar delicioso") basically states the answer, since almíbar is melted sugar syrup and the hollow is said to end up full of it. Replace it with a vaguer hint, for example about the hollow being there to hold something that melts and adds flavour, without naming sugar or syrup.
- **q-13468** (wildlife) Esta piel con puntos rojos es de un animal de los ríos de montaña de España. ¿A qué grupo pertenece? → A los peces: No candidate shows the skin close-up the question needs. #2 and #4 show the whole trout, head and fins included, so the answer (a fish) is obvious. #1 is a plate of several fish drawings and #3 is a range map. No new search is allowed, so the image slot can't be filled. The question may need a different image approach, such as a cropped trout-skin photo, or a rewrite that doesn't depend on a close-up. No se encontró una imagen adecuada para esta pregunta.

## Question axes

- move: analogy 9, cause_effect 5, count 3, estimate 4, identify 50, made_of 14, name_concept 22, odd_one_out 24, origin 41, purpose 11, record 6, sequence 15, when 16, who 27, word_meaning 17
- stimulus: detail 12, map_outline 5, none 192, photo 53, sound 1, video 1
- clue: completion 5, direct 133, riddle 28, scenario 38, three_facts 60
- answer_kind: group 35, number 8, person 54, place 46, thing 50, time 18, word 53
- lens: body_senses 9, educational_media 12, everyday 44, history 51, language 50, nature 16, pop_culture 39, popular_science 1, school 26, science_news 5, university 11

## Dropped by the pipeline

- ancient-hispania-2: overlap like q-0303: Mira este esqueleto de museo: ¿de qué animal prehistórico es? → Mamut: En Padul (Granada) aparecieron restos de un gigante peludo de la Edad de Hielo, con colmillos enormes y curvados. ¿Qué animal era? → El mamut lanudo
- bourbons-and-19th-century-7: overlap like q-8029: En 1808 mis tropas entraron en España y dejé al rey Fernando VII sin trono. Sin rey, en la Nueva Granada nacieron juntas de gobierno. ¿Quién soy? → Napoleón Bonaparte: Este emperador puso a su hermano José como rey de España, y los españoles lo apodaron «Pepe Botella». ¿Quién era el emperador? → Napoleón Bonaparte
- bourbons-and-19th-century-14: overlap like q-11263: Esta comunidad celebra su día cada 2 de mayo, en recuerdo del levantamiento de 1808 contra las tropas francesas. ¿Cuál es? → Comunidad de Madrid: Tras el levantamiento de los madrileños el 2 de mayo de 1808 empezó la Guerra de la Independencia. ¿Contra quiénes? → Contra los franceses
- bourbons-and-19th-century-15: overlap like q-11219: Cuando suena el himno de España en el estadio, la gente canta «lo, lo, lo». ¿Por qué? → Porque no tiene letra oficial: Suena antes de cada partido de la selección española, viene de una marcha militar del siglo XVIII y no tiene letra oficial. ¿Cómo se llama? → La Marcha Real
- bourbons-and-19th-century-16: overlap like q-9900: Por el Tratado de Utrecht, España cedió a Gran Bretaña Gibraltar y también una isla. ¿Cuál? → Menorca: Gibraltar fue español hasta el Tratado de Utrecht de 1713. ¿A qué país pertenece desde entonces? → Al Reino Unido
- brands-and-shops-13: overlap like q-9952: Soy un pez grande y rápido, pero en el súper me venden a trocitos, en latas redondas con aceite. Me echan en la ensalada. ¿Qué soy? → El atún: Viene en lata, se echa en ensaladas y en pizzas, y Calvo es una de sus marcas más famosas. ¿Qué es? → Atún
- christmas-and-holidays-0: overlap like q-0320: En Año Nuevo, ¿cuántas uvas se comen a las doce de la noche? → 12: En Nochevieja, ¿cuántas uvas se comen, una con cada campanada? → 12
- christmas-and-holidays-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Cruzan el desierto, beben el agua que les dejan los niños y cargan los regalos de Melchor, Gaspar y Baltasar. ¿De dónde vienen estos camellos? → De Oriente
- christmas-and-holidays-8: overlap like q-0665: Nochebuena es a Navidad como Halloween (31 de octubre) es a… → Día de Todos los Santos: Es 1 de noviembre, festivo en toda España, y las pastelerías se llenan de buñuelos y panellets. ¿Qué día se celebra? → Todos los Santos
- christmas-and-holidays-13: overlap like q-0667: ¿Qué semana empieza con el Domingo de Ramos y termina con el Domingo de Resurrección? → La Semana Santa: Abre la Semana Santa, la gente lleva palmas y olivo a la iglesia y es costumbre estrenar ropa. ¿Qué día es? → Domingo de Ramos
- co-official-languages-10: overlap like q-9889: Estás preparando pulpo a la gallega: ya está cocido y cortado en rodajas. ¿Qué especia se le espolvorea encima, con sal gorda y aceite? → Pimentón: Se cuece en olla de cobre, se corta con tijeras y se sirve en plato de madera con pimentón y sal gorda. ¿Qué plato gallego es? → El pulpo á feira
- co-official-languages-13: overlap like q-11273: En gallego, ¿qué es una «rúa»? → Una calle: Va antes del nombre en las placas de Barcelona, tiene aceras y por él pasan coches. ¿Qué es un «carrer»? → Una calle
- comics-and-childrens-books-2: overlap like q-11157: Zipi y Zape nacieron en 1948 en la revista Pulgarcito, de la editorial Bruguera, dibujados por Josep Escobar. ¿En qué ciudad estaba esa editorial? → Barcelona: La revista Pulgarcito nació en 1921 en la editorial barcelonesa El Gato Negro. ¿Cómo pasó a llamarse esa editorial más tarde? → Bruguera
- comics-and-childrens-books-8: overlap like q-12409: ¿Qué poeta madrileña, famosa por sus versos para niños, escribió el libro «La oca loca»? → Gloria Fuertes: Lees en clase el libro «La pata mete la pata». ¿Quién lo escribió? → Gloria Fuertes
- current-music-16: overlap like q-10042: Benidorm es a la Costa Blanca como Marbella es a la… → Costa del Sol: El festival Cala Mijas se celebra cerca del pueblo de esta foto. ¿En qué costa española está? → La Costa del Sol
- empire-0: overlap like q-0354: Mira este cuadro famoso, 'Las Meninas', que está en el Museo del Prado de Madrid: ¿quién lo pintó? → Diego Velázquez: ¿Cómo se llama este famoso cuadro del Museo del Prado? → Las meninas
- empire-6: overlap like q-13260: Cristóbal Colón es a la Santa María como Juan Sebastián Elcano es a la… → Nao Victoria: Esta es una réplica del barco más grande de Colón en su viaje de 1492, donde iba él mismo. ¿Cómo se llamaba? → La Santa María
- empire-9: duplicate like q-9991: Esta sopa de fideos se hace con el caldo del cocido. ¿De qué ciudad toma su nombre el cocido más famoso de España? → Madrid: ¿En qué ciudad está este famoso museo de pintura? → Madrid
- empire-11: overlap like q-12377: Estás en la Alhambra, el palacio del antiguo Reino nazarí de Granada. ¿En qué año lo conquistaron los Reyes Católicos? → 1492: Este detalle es de un palacio de la ciudad que Isabel la Católica y Fernando conquistaron en 1492. ¿Qué ciudad es? → Granada
- empire-12: overlap like q-2016: ¿Qué rey de España, nieto de los Reyes Católicos, fue también emperador del Sacro Imperio Romano Germánico? → Carlos V: En la serie «Carlos, rey emperador» el protagonista es Carlos I de España. ¿Qué número llevaba como emperador alemán? → Carlos V
- empire-13: overlap like q-12371: En la fachada de la Universidad de Salamanca hay una ranita de piedra que todos buscan. ¿Sobre qué está sentada? → Sobre una calavera: Este detalle es de la fachada plateresca de una universidad, donde los estudiantes lo buscan para tener suerte. ¿En qué ciudad está? → Salamanca
- famous-figures-8: overlap like q-11324: TheGrefg presentó su propia skin de Fortnite ante casi 2,5 millones de personas a la vez, récord de Twitch entonces. ¿En qué año? → 2021: ¿Qué streamer español batió en enero de 2021 el récord de espectadores en directo en Twitch al presentar su skin de Fortnite? → TheGrefg
- famous-figures-9: overlap like q-11425: ¿En qué año empezó en Cuatro «First Dates», el programa de citas a ciegas de Carlos Sobera? → 2016: Completa el nombre del programa de Cuatro en el que Carlos Sobera recibe a solteros en un restaurante: «First…» → Dates
- famous-figures-12: overlap like q-9931: Es la cadena de supermercados que más vende en España, nació en Valencia y su marca propia es Hacendado. ¿Cuál es? → Mercadona: Los productos de la marca Hacendado, ¿en qué supermercado se compran? → Mercadona
- famous-figures-13: overlap like q-9939: Empecé de dependiente en una camisería de A Coruña y en 1975 abrí allí la primera tienda Zara. ¿Quién soy? → Amancio Ortega: En 2022, Marta Ortega sustituyó a Pablo Isla como presidenta de un gran grupo de moda. ¿Cuál? → Inditex
- folk-music-and-dance-6: overlap like q-11450: En el villancico «Campana sobre campana», ¿para qué te asomas a la ventana? → Para ver al Niño en la cuna: Es muy antigua, suena con zambombas y panderetas y habla de campanas que tocan. ¿Cuándo se canta «Campana sobre campana»? → En Navidad
- folk-music-and-dance-10: overlap like q-9923: El 12 de octubre, Fiesta Nacional de España, también se celebra a la patrona de Zaragoza. ¿Qué Virgen es? → La Virgen del Pilar: Las Fiestas del Pilar se celebran en octubre, con jotas y conciertos junto al río Ebro. ¿En qué ciudad? → Zaragoza
- folk-music-and-dance-15: overlap like q-11139: En el patio, los niños se dan la mano formando un círculo y giran mientras cantan. ¿Qué tipo de canción es? → Una canción de corro: En «Al corro de la patata», los niños se cogen de las manos, dan vueltas y al final se sientan. ¿Qué es un «corro»? → Un círculo de personas
- footballers-and-national-team-14: overlap like q-2548: This coach won the Champions League with both Barcelona and Manchester City. Who is he? → Pep Guardiola: Este entrenador español ha ganado muchas veces la liga inglesa con el Manchester City. ¿Quién es? → Pep Guardiola
- ham-cheese-and-produce-6: overlap like q-9975: En Jaén forma un auténtico «mar» y España es la primera productora mundial de su fruto. ¿Qué árbol es el más cultivado en España? → El olivo: Mira este árbol, muy común en el campo de Andalucía. ¿Qué fruto da? → Aceitunas
- ham-cheese-and-produce-12: overlap like q-10041: ¿En qué ciudad se celebran las Fallas, en las que se queman enormes figuras cada mes de marzo? → Valencia: Las naranjas más famosas de España llevan el nombre de una tierra con la Albufera, las Fallas y la paella. ¿Cuál? → Valencia
- legends-and-superstitions-5: overlap like q-10035: Estás ante la tele en Nochevieja y, antes de las doce campanadas, suenan los cuartos. ¿Cuántos son? → 4: Antes de las campanadas de Nochevieja, este reloj toca los «cuartos». ¿Cuántos cuartos suenan? → 4
- legends-and-superstitions-10: overlap like empire-13: Este detalle es de la fachada plateresca de una universidad, donde los estudiantes lo buscan para tener suerte. ¿En qué ciudad está? → Salamanca: Sobre una calavera de la fachada de una universidad hay una rana tallada, y dicen que quien la encuentra sin ayuda aprueba los exámenes. ¿En qué ciudad está? → Salamanca
- national-symbols-9: overlap like q-11296: Iniesta marcó en la prórroga el gol que dio a España su primer Mundial. ¿En qué minuto? → 116: En la final del Mundial de 2010 contra Países Bajos, ¿en qué momento marcó Iniesta el gol de la victoria? → En la prórroga
- national-symbols-11: overlap like q-9884: En el sorteo de Navidad, un niño de San Ildefonso canta el número que ha salido. ¿Qué canta justo después su compañero? → El premio en euros: ¿Quién canta los números y los premios en el Sorteo de Navidad? → Los niños de San Ildefonso
- pop-and-rock-2: overlap like q-1428: Antes de cantar fui portero juvenil del Real Madrid; en 1970 canté «Gwendolyne» en Eurovisión. ¿Quién soy? → Julio Iglesias: En 1970, un exportero de las categorías inferiores del Real Madrid cantó «Gwendolyne» en Eurovisión y quedó cuarto. ¿En qué ciudad se celebró ese festival? → Ámsterdam
- regional-symbols-3: overlap like q-9922: Fue el lema de Carlos I, aparece en el escudo de España entre las columnas de Hércules y dio nombre a un hidroavión que cruzó el Atlántico en 1926. ¿Cuál es? → «Plus Ultra»: Estas columnas con el lema «Plus Ultra», «más allá», están en el escudo de España. ¿Qué rey adoptó ese lema? → Carlos V
- ancient-hispania-3: overlap like q-1743: La Edad de Piedra es a la piedra como la primera etapa de la Edad de los Metales es al… → Cobre: Los arqueólogos me llaman también Calcolítico. En mí se levantó Los Millares, en Almería, y se pusieron de moda unos vasos con forma de campana. ¿Qué época soy? → La Edad del Cobre
- ancient-hispania-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Augusto fundó Emerita Augusta en el 25 a. C. junto al Guadiana y la hizo capital de Lusitania. ¿Para quiénes la fundó? → Para soldados veteranos de sus legiones
- ancient-hispania-11: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Los cartagineses fundaron una ciudad hacia el 227 a. C. en la costa de Murcia, con un gran puerto. Los romanos la llamaron Carthago Nova. ¿Qué significa? → Nueva Cartago
- bourbons-and-19th-century-8: hard fail: correct 2, unambiguous 5, no_giveaway 3, no_overlap 5: Moratín y Meléndez Valdés fueron «afrancesados»: ilustrados que querían reformas y acabaron exiliados. ¿Qué hicieron para ganarse ese nombre? → Apoyaron al rey José Bonaparte
- sweets-and-desserts-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Son granitos de colores que vienen en un sobre pequeño. ¿Qué pasa cuando te pones Peta Zetas en la lengua? → Chisporrotean y estallan
- sweets-and-desserts-17: overlap like christmas-and-holidays-8: Es 1 de noviembre, festivo en toda España, y las pastelerías se llenan de buñuelos y panellets. ¿Qué día se celebra? → Todos los Santos: Los dulces de mazapán cubiertos de piñones son típicos de Todos los Santos en Cataluña. ¿Cómo se llaman estos dulces? → Panellets
- co-official-languages-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En catalán, ¿qué es una «plaça»? → Una plaza
- co-official-languages-7: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: En Barcelona o en Valencia, ¿qué es el «Ajuntament»? → El ayuntamiento
- co-official-languages-14: fact-check wrong: The fun fact says only one ninot is saved each year. Two are pardoned: one from the adult falla and one from the children's (infantil) falla.: ¿Cuál de estas cosas NO forma parte de las Fallas de Valencia? → La batalla de tomates
- comics-and-childrens-books-4: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Soy dibujante gallega y estudié arquitectura. Para la editorial Image dibujé el wéstern fantástico «Pretty Deadly», con Kelly Sue DeConnick. ¿Quién soy? → Emma Ríos
- comics-and-childrens-books-7: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Son personajes de Ibáñez nacidos en los años 80: jóvenes en paro que en cada historieta buscan trabajo. ¿Quiénes son? → Chicha, Tato y Clodoveo
- comics-and-childrens-books-14: overlap like q-11176: La nana «Duérmete, niño» avisa de que, si no duermes, vendrá alguien que te comerá. ¿Quién? → El coco: ¿Qué es una nana? → Una canción para dormir
- current-music-2: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: La cantó Quevedo y fue la canción más escuchada en Spotify en España en el verano de 2023. ¿Cuál es? → «Columbia»
- folk-music-and-dance-0: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: En la gaita asturiana, ¿qué parte del instrumento se llama «fol»? → La bolsa que guarda el aire
- folk-music-and-dance-16: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: En la canción de comba «El cocherito, leré», ¿a qué se dedicaba un cochero? → Conducía coches de caballos
- ham-cheese-and-produce-7: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Tiene un pitorro fino y sirve para echar un chorrito en la tostada del desayuno o en la ensalada. ¿Cómo se llama? → Aceitera
- national-symbols-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Soy morado, llevo corona, estoy en el escudo de España y represento a un antiguo reino con mi mismo nombre. ¿Qué animal soy? → Un león
- pop-and-rock-1: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Este grupo de San Sebastián debutó en 1998 con «Dile al sol» y se llama como una parte del cuerpo de un pintor holandés. ¿Cuál? → La oreja
- pop-and-rock-3: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: En la España de los 80, el vinilo es a la tienda de discos como la casete barata de rumbas es a… → Gasolinera
- slang-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: En el cole se usan muchas palabras cortas: «profe», «finde», «mates». ¿Qué asignatura es «mates»? → Matemáticas
- slang-12: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: En los bares del norte se toman de pie en la barra y antes se cobraban contando los palillos del plato. ¿Qué es un pincho? → Una tapa pequeña sobre pan
- slang-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Llegan al final de cada trimestre y tus padres las tienen que ver. ¿Qué son «las notas» del cole? → Tus calificaciones
- sportspeople-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: En París 2024, la nadadora Teresa Perales igualó el total de medallas olímpicas de Michael Phelps. ¿Cuántas medallas paralímpicas sumó? → 28
- rivers-and-mountains-10: overlap like q-0264: ¿Cómo se llaman las pinturas que hacían los primeros humanos en las paredes de roca de las cuevas? → Pinturas rupestres: Los bisontes que pintaron los hombres prehistóricos en el techo de la cueva de Altamira, ¿cómo se llaman? → Pinturas rupestres
- rivers-and-mountains-12: overlap like q-10043: Es un bosque húmedo de árboles de hoja perenne y brillante, vive envuelto en niebla y sobrevive en el parque de Garajonay, en La Gomera. ¿Cómo se llama? → La laurisilva: Este bosque de laurisilva, envuelto en niebla, es el Parque Nacional de Garajonay. ¿En qué isla está? → La Gomera
- rivers-and-mountains-15: overlap like folk-music-and-dance-10: Las Fiestas del Pilar se celebran en octubre, con jotas y conciertos junto al río Ebro. ¿En qué ciudad? → Zaragoza: En la foto se ve la basílica del Pilar, en Zaragoza. ¿Qué río pasa por delante? → El Ebro
- scientists-and-explorers-2: overlap like q-2021: Estás viendo los dibujos de neuronas más famosos de la historia, hechos a mano por un Nobel de Medicina. ¿Quién los hizo? → Santiago Ramón y Cajal: Este dibujo de una neurona lo hizo a mano un científico español que ganó el Nobel. ¿Quién fue? → Santiago Ramón y Cajal
- scientists-and-explorers-3: overlap like q-1179: Te subes en Madrid a un tren llamado AVE, sigla de 'Alta Velocidad Española'. ¿Más o menos a qué velocidad máxima puede llevar pasajeros? → Unos 300 km/h: ¿Para qué se usa este tren tan rápido de España? → Para llevar viajeros rápido entre ciudades lejanas
- scientists-and-explorers-4: overlap like q-4708: In ancient mines, workers heated the blood-red mineral cinnabar. Which metal came out of it? → Mercury: Bajas a las minas de Almadén y lees que de allí se sacaba el «azogue». ¿Cómo se llama hoy ese metal? → Mercurio
- scientists-and-explorers-10: overlap like q-11308: Cada año, en la gala de los Premios Princesa de Asturias en Oviedo, la heredera del trono da un discurso. ¿Quién es? → Leonor de Borbón: En este teatro se entregan cada otoño los Premios Princesa de Asturias. ¿En qué ciudad está? → Oviedo
- slang-6: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Se dice que el primer bar de playa llamado «chiringuito» abrió en un pueblo costero cerca de Barcelona, famoso por su festival de cine fantástico. ¿Cuál? → Sitges
- slang-9: overlap like q-11284: ¿En qué década nacieron Pepe Gotera y Otilio, los «chapuzas a domicilio» de Ibáñez? → En los años 60: Es un arreglo hecho deprisa y mal, que se rompe al día siguiente, y sale en el lema de Pepe Gotera y Otilio. ¿Qué palabra es? → Chapuza
- spanish-cinema-7: overlap like q-13354: Si haces un maratón de películas de Dani Rovira, ¿cuál de estas NO podrás ver con él de protagonista? → El Capitán Trueno y el Santo Grial: En «Ocho apellidos vascos», ¿qué actor interpreta a Rafa, el sevillano que se hace pasar por vasco para conquistar a Amaia? → Dani Rovira
- spanish-cinema-13: duplicate like q-12374: Mira el mapa: en esta comunidad, en otoño se celebra el magosto, una fiesta con castañas asadas. ¿Cuál es? → Galicia: Este actor fue Malamadre en «Celda 211». ¿De qué comunidad autónoma es? → Galicia
- sportspeople-4: overlap like q-12480: Completa: Pau Gasol fue campeón de la NBA con Los Angeles… → Lakers: ¿En qué equipo de la NBA ganó Pau Gasol sus dos anillos de campeón, junto a Kobe Bryant? → Los Angeles Lakers
- sportspeople-13: overlap like q-3688: In 2005, at age 24, I became the youngest Formula 1 champion up to then and ended Michael Schumacher's run of five titles. Who am I? → Fernando Alonso: ¿Qué piloto de Fórmula 1, nacido en Oviedo, fue dos veces campeón del mundo? → Fernando Alonso
- sportspeople-16: overlap like q-11389: Estás viendo a Rafa Nadal tumbarse sobre la tierra batida tras ganar el Grand Slam que conquistó 14 veces. ¿Qué torneo es? → Roland Garros: Toni Nadal entrenó a su sobrino Rafa desde niño hasta 2017. ¿En qué torneo tiene Rafa el récord mundial de títulos? → Roland Garros
- sweets-and-desserts-6: overlap like q-9940: En una churrería, ¿cuál de estas cosas NO se suele mojar en el chocolate a la taza? → Una croqueta: Estás en el quiosco con una bolsa para llenar de chuches. ¿Cuál de estas cosas NO es una chuche? → Las croquetas
- wildlife-6: overlap like q-0986: Mira de cerca este animal acuático. ¿A qué grupo de animales pertenece? → Mamíferos: Me ven en el estrecho de Gibraltar y en Canarias. Bajo a más de 1000 metros a cazar calamares y subo a respirar aire. ¿Qué tipo de animal soy? → Un mamífero
- wildlife-9: overlap like q-0155: ¿Cómo se llama este insecto? → Mantis religiosa: Mira este insecto. ¿A quién se parece por cómo pone las patas delanteras? → A una persona rezando
- wildlife-11: overlap like q-6702: White storks build huge nests on rooftops in Europe. Each autumn they fly far to the south, and they come back in spring. Where do they spend the winter? → Africa: El ruiseñor llega a los sotos de España en abril, canta de día y de noche, y en otoño se marcha. ¿De dónde viene? → Del África tropical
