# tr-es-ES-31

Made by `qgen batch --translate es-ES` on 2026-11-18 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 102 (0 stale re-translated)
- Translated: 102
- Approved: 101
- Needs work: 1
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 230, about $13.66 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-31&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-29 | tr-es-ES-30 | tr-es-ES-31 |
|---|---|---:|---:|---:|
| sources |  | 57 | 53 | 102 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 57 | 53 | 102 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 56 | 52 | 101 |
| needs_work |  | 1 | 1 | 1 |
| needs_work rate | ≤ 20.0 % | 1.8 % ✓ | 1.9 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.8 % ✓ | 1.9 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 57 | 53 | 60 |
| audit/review agreement | ≥ 90.0 % | 35.1 % ✗ | 34.0 % ✗ | 51.7 % ✗ |
| cost $ |  | $6.61 | $5.60 | $10.32 |
| $ per approved |  | $0.12 | $0.11 | $0.10 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 28 of 59 (47 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 1 (0 major), overlap 1 (1 major), media 46 (28 major), style 1 (1 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 31 of 60 (52 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.34

Major findings on approved questions:

- **q-21086**: media, style — The media is essential video, but its title is null, so no file was picked. The question says «Mira: este plato…» and has nothing to show. Smaller issue in the description: «barquito» is a literal rendering of "gravy boat". In Spain that's a «salsera», so the joke barely works; something like «hasta le da su propia salsera con forma de barco» would land better. I checked the answer (pie, chips, mushy peas and gravy is a classic British meal), the wrong options, the hints, the fun fact (marrowfat peas soaked overnight) and the difficulty; all are fine. (http://127.0.0.1:8001/review/q-21086)
- **q-21087**: media — The essential audio is missing (media.title is null). Without the alarm call, the «Escucha:» question can't be played. Translation checked: zarapito real, avefría, ostrero and archibebe común are the correct Spanish names; the facts about Europe's largest wader and the longer female bill are true; hint 3 rightly drops the name-sounds-like-song link. (http://127.0.0.1:8001/review/q-21087)
- **q-21088**: media — The question needs a recording of the anthem ("Escucha: …"), but the essential audio has no file picked (media title is null), so it can't be played as it is. Apart from that, the translation is faithful and reads naturally in Spain's Spanish ("Fiyi" is the standard spelling). The hints and fun fact are correct: the first verse is usually sung in Māori and then in English, and the country has two anthems with equal status. The difficulty of 11 is reasonable. (http://127.0.0.1:8001/review/q-21088)
- **q-21089**: media — The essential video has no picked file (media.title is null). This question only works if players see the bird, so it can't be played as it is. The translation itself is faithful and natural es-ES, and the option articles agree. The facts hold up: the emu is the second-tallest living bird, the father sits on the eggs for about 8 weeks while barely eating, and the emu and kangaroo share Australia's coat of arms. (http://127.0.0.1:8001/review/q-21089)
- **q-21095**: media — The translation is faithful and natural es-ES. Gambia without the article and Sierra Leona are both fine. The facts hold: the anthem's tune comes from the traditional Mandinka song «Foday Kaba Dumbuya», and Gambia is the smallest country on mainland Africa, almost surrounded by Senegal. The related Ghana anthem question asks a different fact. The one problem is the essential audio: its title is null, so no anthem recording is attached, and the question can't be played until one is. (http://127.0.0.1:8001/review/q-21095)
- **q-21098**: media — The essential video is missing (media title is null, so no file was picked). The question says «Mira» and asks about «esta isla», so it can't be played without the video. This comes from the source, not the translation. The translation itself is faithful and natural es-ES, with no article or gender giveaway among the options. The facts are correct (tube-shaped nostrils, Coleridge's Ancient Mariner, royal albatrosses pairing for life), and q-5550 asks a different albatross fact. (http://127.0.0.1:8001/review/q-21098)
- **q-21100**: media — Media is an essential video but media.title is null: no file was picked, so the question ("Mira este vídeo…") can't be played without its time-lapse (source: same media gap). The translation itself is faithful and natural es-ES; the hints, the fun fact (lentil sabzeh for Nowruz) and the options' grammar check out. (http://127.0.0.1:8001/review/q-21100)
- **q-21101**: media — The media is an essential video, but its title is null, so no file was picked. The question says «Mira este vídeo acelerado…», so it can't be played without that video. The Spanish translation is faithful and reads naturally. The facts hold: Liesegang described the rings in 1896 using silver nitrate on gelatin with dichromate, and similar banding shows up in agates. The wrong options (Newton's rings, Chladni figures, Widmanstätten patterns) are all clearly different phenomena, and none of the related questions overlap. (http://127.0.0.1:8001/review/q-21101)
- **q-21111**: media — The Spanish text is accurate and reads naturally. The facts check out: Dagomba lunsi drummers are hereditary historians, and talking drums are squeezed under the arm. The options agree in grammar, and «Bongó» is accepted by the RAE. The problem is the media: it is an essential video, but no file was picked (title is null). The question opens with «Mira a los tamborileros…», so it can't be played without the footage. (http://127.0.0.1:8001/review/q-21111)
- **q-21114**: media — The media is an essential video, but no file was picked (title null). The question opens with «Mira:» and relies on footage of astronauts suiting up, so it can't be played as it is. The translation itself matches the source and reads as natural Spain Spanish. The facts hold: the orange is for visibility at sea, and the Shuttle's ACES suits really were nicknamed "pumpkin suits". Hint 2 only fits if the footage shows a crew that splashes down, such as Orion's orange suits; it doesn't fit the Shuttle, which landed on a runway. (http://127.0.0.1:8001/review/q-21114)
- **q-21116**: media — The question needs an essential sped-up video ("Mira este vídeo acelerado"), but media.title is null, so no file was picked and the question can't be played as it is. The translation itself is faithful and natural for Spain. "Drosera" and its Greek root droserós ("dewy") are correct. Droseras grow on every continent except Antarctica, and Darwin's "Insectivorous Plants" came out in 1875. The options agree in grammar, and there is no overlap with q-0490 (Venus atrapamoscas). (http://127.0.0.1:8001/review/q-21116)
- **q-21118**: media — The media is an essential video, but its title is null, so no file was picked. Without the footage, the question «¿qué suelta el cohete?» is ambiguous, because rockets also release crew capsules, landers and station modules. The translation itself is faithful and reads naturally in Spain's Spanish. The options agree in gender and article. The fun fact is correct: the Landsat satellites have photographed Earth since 1972. (http://127.0.0.1:8001/review/q-21118)
- **q-21127**: media — The translation is faithful and reads naturally in Spain's Spanish. The facts check out: Beethoven's Sonata Op. 14 No. 1 in E major dates from 1798–99, and he arranged it himself for string quartet in F major. The problem is the media: this "Escucha" question needs its essential audio, but media.title is null, so no recording was picked. Without it the question can't be played (source: the issue comes from the source's media slot, not from the translation). (http://127.0.0.1:8001/review/q-21127)
- **q-21131**: media — The question depends on the anthem audio ("Escucha"), but no audio file has been picked (media.title is null), so it can't be played as it stands. That comes from the source, not the translation. The translation itself is fine: it is faithful and reads naturally in Spain's Spanish, with the number written correctly as «17 000». The facts check out: Indonesia has more than 17 000 islands and the fourth-largest population in the world, and Supratman first played «Indonesia Raya» on the violin at the 1928 Youth Congress, 17 years before independence in 1945. (http://127.0.0.1:8001/review/q-21131)
- **q-21134**: media — The essential audio has no file (media title is null), so the question «Escucha: ¿de qué país es este himno nacional?» can't be played without the anthem recording. Everything else checks out: the translation matches the source, the options agree in gender and are correct (Germany uses Haydn's tune, Switzerland the Schweizerpsalm, Liechtenstein the God Save the King melody), the hints and the Mozart/Holzer fun fact are accurate, and the Spanish reads naturally. (http://127.0.0.1:8001/review/q-21134)
- **q-21135**: media — The media is marked as essential video, but its title is null, so no file was picked. The question ("Mira: … ¿Qué símbolo musical dibuja?") can't be played without seeing the saltpeter line burn. The translation itself checks out: it is faithful to the source, the terms are correct castellano music vocabulary (corcheas, redondas, clave de sol, sostenido, plicas, negra), the options don't give each other away by grammar, and the fun fact about potassium nitrate making the paper smoulder only where it was painted is accurate. (http://127.0.0.1:8001/review/q-21135)
- **q-21139**: media — The essential video has no file (media title is null). The question opens with «Mira y escucha», so it can't be played without it. The translation itself is faithful and natural castellano: «zoco», «Esauira», «castañuelas de metal», and all four options take the masculine «el». Facts I checked are all correct: the guembri and qraqeb as instruments, the lila ceremony, the Gnaoua festival in Essaouira, the 2019 UNESCO listing, and Robert Plant playing with Gnawa musicians (Page & Plant, «No Quarter»). (http://127.0.0.1:8001/review/q-21139)
- **q-21154**: media — The essential video is missing (media title is null), and the question can't be played without it: «Mira lo que pasa…» relies on players watching the screaming gummy bear experiment. The translation itself is faithful and reads as natural Spanish from Spain («gominola», «sal fundida», «hoguera»). The facts hold up: potassium chlorate releases oxygen and the gummy's sugar burns, which is combustion. (http://127.0.0.1:8001/review/q-21154)
- **q-21157**: media — The translation is faithful and natural es-ES ("a cámara rápida", "polo sur", "desierto del Sahara"). The options agree in grammar, and the hints and fun fact match the source and are true (northern Sweden in January; polar night beyond the Arctic Circle). The one problem is the media: it is an essential video and its title is null, so no file has been picked. The question «Mira: este vídeo…» can't be played without it. If a file does exist and only the title is missing from the input, nothing is wrong with the translation itself. (http://127.0.0.1:8001/review/q-21157)
- **q-21159**: media — The question needs its essential audio (the Swedish anthem), but media.title is null, so no file is attached and it can't be played as it stands. The translation itself is faithful and natural es-ES. The facts hold: Stockholm sits on 14 islands where Lake Mälaren meets the Baltic, and «Du gamla, Du fria» uses a folk melody and has never been made official by law. (http://127.0.0.1:8001/review/q-21159)
- **q-21167**: media — The question needs an essential video ("Mira: ¿qué tipo de pingüino camina por esta playa?"), but no file is picked (media title is null), so it can't be played as it stands. The translation itself is faithful and reads naturally in Spain's Spanish: the species names are right (pingüino rey, emperador, papúa, de Adelia), and the hints and the brood-pouch fun fact are true and match the source. (http://127.0.0.1:8001/review/q-21167)
- **q-21169**: media — The essential video has no file (title null). The question depends entirely on seeing Sydney Harbour and the Opera House, so it can't be played as it is. The translation itself is faithful and reads naturally in Spain's Spanish ("ferris", «concurrido puerto»). I checked the facts: Sydney is on Australia's east coast, Port Jackson opens onto the Tasman Sea, which is part of the Pacific, and the Opera House sails have about 1,05 million glossy and matte tiles. (http://127.0.0.1:8001/review/q-21169)
- **q-21175**: media — The question needs an essential video ("Mira: esta escena…", "el hombre de la alta corona dorada", hint 1 "fíjate en sus manos"), but no file was picked (media title is null). Without the clip, players can't play it. The translation itself is faithful and natural es-ES ("Visnú", «mantequilla», "Mira:"). The facts check out: Bhaona is from Assam, created by Sankardev in the early 1500s, and Krishna is an avatar of Vishnu. (http://127.0.0.1:8001/review/q-21175)
- **q-21181**: media — The question needs an essential sped-up video of a ship being built, but no media file was picked (media.title is null), so it can't be played as it is. This may just be the pipeline not passing the source's file through. The translation itself reads well: it keeps the source's facts, the options agree in gender with «Un», the hints and «dique seco» are correct, and the Spanish is natural es-ES. (http://127.0.0.1:8001/review/q-21181)
- **q-21182**: media — The media is listed as an essential video, but its title is null, so no file seems to be attached. The question starts with «Mira:» and needs the sugar-and-acid (sulfuric acid dehydration) footage to be playable. This may only be a gap in the input data rather than a missing file. Everything else checks out: the translation is faithful and in natural es-ES. Carbon is correct and the three wrong answers are clearly wrong. The hints and fun fact are accurate (sugar is made of C, H and O; the reaction gives off heat and steam). The diamond and pencil-lead questions in related ask different facts, so there is no overlap. (http://127.0.0.1:8001/review/q-21182)
- **q-21185**: media — The translation is faithful and reads naturally in Spain's Spanish ("Mira", "Fíjate", «Amazonia» is a valid RAE spelling). The options agree in form and the facts hold: Brazil covers almost half of South America and most of the Amazon fires are started by people. The real problem is the essential video: its title is null, so no file is attached. The question ("cada punto rojo de este globo") can't be played without the satellite fire animation. (http://127.0.0.1:8001/review/q-21185)
- **q-21186**: media, overlap — The essential video is missing (media title is null). The question ("Mira cómo pasa este tren…") and hints 1 and 2 ("Mira encima del tren", "Escucha el rugido") only work if the footage plays, so it can't be played as it is. There is also a minor overlap with q-1181, which already teaches that today's locomotives usually run on diesel. The translation itself is faithful and natural es-ES ("catenaria", "camiones", «» quotes), and the facts are right, including the diesel-electric fun fact. (http://127.0.0.1:8001/review/q-21186)
- **q-21189**: media — The essential video has no file (title null), so «Mira bien el matraz» can't be played. This is a source/pipeline gap, not a translation error. The translation itself is faithful and natural es-ES; the four options agree in gender and number; the facts hold (in the blue bottle experiment, shaking brings in O2, which re-oxidises methylene blue; glucose then reduces it again until the glucose runs out). It doesn't repeat the fact in q-20991, which is about foam bubbles. (http://127.0.0.1:8001/review/q-21189)

## Needs work

- **q-21051** (birds) Fíjate en el primer plano del pato con llamativas rayas blancas en la cabeza oscura. ¿Qué tipo de pato es? → Pato carolino: Fact check: uncertain. The biology is correct: the wood duck is North American and bred worldwide as an ornamental. The male has a green crest, red eye and red-and-white bill. It nests in tree cavities. Ducklings leave the day after hatching and can drop about 15 m unharmed. The wrong answers (mallard, common eider, common shelduck) are different species. The 1937 Avicorni poultry show newsreel is real (Polygoon, December 1937). The Commons page only says a prize duck appears at the end and doesn't name its species. I couldn't confirm that the close-up at about 47 s shows a wood duck. The 'plumas, jaulas y un juez con bata blanca' description also isn't supported by the page text.

## Not travelling

None.

## Stale re-translated

None.
