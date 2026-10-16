# tr-es-ES-1

Made by `qgen batch --translate es-ES` on 2026-10-16 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 50 (0 stale re-translated)
- Translated: 50
- Approved: 49
- Needs work: 1
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 169, about $7.12 at list price; $0.11 per approved translation (without the audit)
- Spot check by a native speaker: http://127.0.0.1:8001/review?batch=tr-es-ES-1&locale=es-ES&sample=1

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. The pilot (`-1`) and a ✗ stop the next `qgen batch --translate` until `qgen health ack` (D-55).

| metric | threshold | tr-es-ES-1 |
|---|---|---:|
| sources |  | 50 |
| stale re-translated |  | 0 |
| translated |  | 50 |
| not travelling |  | 0 |
| not travelling confirmed |  | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ |
| approved |  | 49 |
| needs_work |  | 1 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ |
| audited |  | 50 |
| audit/review agreement | ≥ 90.0 % | 74.0 % ✗ |
| cost $ |  | $5.20 |
| $ per approved |  | $0.11 |
| **health** | | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 12 of 49 (24 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 4 (2 major), ambiguity 1 (1 major), media 12 (12 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 50 (0 %)
- Audit/review agreement (both accept or both not): 37 of 50 (74 %)
- Sample: 50 audited of 50; 50 Claude calls, about $1.92

Major findings on approved questions:

- **q-0126**: media, giveaway — The image is marked essential, but no file was picked (title null). The question asks about "este trocito" of a flag, so it can't be played without a picture of part of the Mexican flag. The translation itself is faithful and natural for Spain ("trocito", "comida"), and the facts are right. Minor issue: hint 2 (verde, blanco y rojo) rules out all three wrong answers, and the description's eagle-on-a-cactus joke points strongly to Mexico's coat of arms. (http://127.0.0.1:8001/review/q-0126)
- **q-0186**: media — The question needs its essential image ("Mira este primer plano"), but the media title is null, so no picture was picked. Without the photo the question can't be answered, and a fried, golden dish fits the buñuelo too. Apart from that the translation is faithful and reads as natural Spain Spanish ("primer plano", "patata", "dentro", «» quotes), and the hints and fun fact are correct. (http://127.0.0.1:8001/review/q-0186)
- **q-0466**: media — The media is essential, but no file was picked (title is null). Without the close-up photo, «Mira esta imagen» can't be answered. The translation itself is faithful and reads naturally in Spain's Spanish («tejado», «polvillo», angle quotes), the facts are right (butterfly wing scales come off as coloured dust) and the difficulty of 5 fits. (http://127.0.0.1:8001/review/q-0466)
- **q-0490**: media — The media is marked essential, but no file was picked (title is null). Without the photo, «Mira la foto» can't be played. The translation itself is fine: the facts are right (the plant grows wild only in the Carolinas' wetlands, and the trap needs two touches to close), the Spain wording reads naturally («Rocío del sol» and «pelos» are fine), and no option stands out by grammar. (http://127.0.0.1:8001/review/q-0490)
- **q-0514**: media — The media role is "essential", but no file was picked (title null), so the question opens with "Este animal…" and nothing is shown on screen. The rest checks out: the translation matches the source word for word and reads naturally in Spain's Spanish. The facts hold up: peccaries (Tayassuidae) live only in the Americas, from the southern US to Argentina, they are a separate family from pigs, and they have a dorsal scent gland that the herd uses to recognise its members. All three wrong answers are clearly wrong. (http://127.0.0.1:8001/review/q-0514)
- **q-0693**: media — The essential image has no file picked (title null), but the question starts with «Mira la foto» and only works if players see a dorayaki. As it stands it can't be played; it needs a clear dorayaki photo (this is in the source's media, not the translation). The translation itself is fine: it keeps the same fact and answer, «tortitas» and «judía roja» are natural Spanish from Spain, it uses «» quotes, the hints don't name Doraemon, and the facts are right (dorayaki is Doraemon's favourite food, and anko is red bean paste). (http://127.0.0.1:8001/review/q-0693)
- **q-0725**: media — The media is marked essential, but no file was picked (title null), so the TV would show «Mira la foto» with no photo; the source has the same problem. The translation is otherwise fine: «desmontar» is natural Spain Spanish, the description reads well with «escapar de las visitas», «Jaima» is the usual Spain term, and the facts check out (ger, the wooden frame with felt, taking it down in 1–2 hours). Hint 2 rules out two options, which only counts as a minor hint-level narrowing. (http://127.0.0.1:8001/review/q-0725)
- **q-0738**: media — The media is marked essential, but no file was picked (title null), and the question opens with «Mira esta planta». On the TV, players would be told to look at a plant that isn't there. The facts check out: catnip (Nepeta cataria) belongs to the mint family (Lamiaceae), and the rose, sunflower and grass families are clearly wrong. The toothed leaves, the culinary relatives and the fun fact (roughly a third of cats don't react, and the trait is inherited) are also accurate. The es-ES wording is fine: changing «pasto» to «césped» is acceptable, though «gramíneas» would be more precise. (http://127.0.0.1:8001/review/q-0738)
- **q-0751**: media — The media is marked essential, but no file was picked (title null), and the question text says «como esta», which points at a fruit-fly picture that won't be on screen. The text is the same as the approved source and reads naturally in Spain's Spanish. The facts check out: on 20 February 1947 the US launched fruit flies on a captured V-2 from White Sands, New Mexico, and they were recovered alive in a capsule under a parachute. The wrong answers are really wrong, and hint 1 only narrows the options. (http://127.0.0.1:8001/review/q-0751)
- **q-1697**: media, ambiguity — The media is essential, but no file was picked (title null), so the question "Mira este diente fósil…" has nothing to show. And without the picture, "enorme y con bordes de sierra" also fits big theropod dinosaurs like T. rex and Carcharodontosaurus, which had serrated teeth too, so "De un dinosaurio" can't be ruled out. The translation itself matches the source and reads naturally in Spain's Spanish ("cinta transportadora" is just a clearer word), and the hints and fun fact are correct. (http://127.0.0.1:8001/review/q-1697)
- **q-1834**: media, giveaway — The question is "Mira de cerca esta cola", but its essential image has title null, so no file was picked. Without a photo of a rattlesnake's rattle the question can't be played. Separately, the description («Una cola que viene con su propia banda sonora») points straight at the only snake with a tail that makes a sound. This comes from the source and is minor, since the photo shows the rattle anyway. The translation itself is identical to the source and reads naturally in Spain. The facts are right: the rattle is made of keratin, and a new segment is added at each shed. (http://127.0.0.1:8001/review/q-1834)
- **q-2123**: media — The media is essential, but no file was picked (title null). The text never names the chocolate («Este bombón»), so without a picture of a chocolate truffle the question can't be answered. The translation itself is fine for Spain and matches the source. The facts check out: truffles are mycorrhizal fungi that grow with oaks and spread by spores, and the chocolate truffle is traditionally credited to France. (http://127.0.0.1:8001/review/q-2123)

## Needs work

- **q-0708** (fast-food) Completa: «Las patatas fritas se hacen con patata, y el coleslaw, esa ensalada rallada con mayonesa, se hace con…» → Col: The translation changed the answer from 'Repollo' to 'Col'. Now 'coleslaw' in the question already sounds like the answer, and hint 2 («"Cole" viene de una palabra neerlandesa para esta verdura») points straight at 'Col'. 'Coliflor' also starts with 'col', so that is the only thing left to rule out. 'Repollo' is a common word in Spain. Go back to answer 'Repollo', and make hint 3 say «también se le llama col», as in the source.

## Not travelling

None.

## Stale re-translated

None.
