# tr-es-19

Made by `qgen batch --translate es` on 2026-11-16 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 74 (0 stale re-translated)
- Translated: 74
- Approved: 71
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 189, about $11.52 at list price; $0.12 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-19&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-17 | tr-es-18 | tr-es-19 |
|---|---|---:|---:|---:|
| sources |  | 281 | 168 | 74 |
| stale re-translated |  | 0 | 1 | 0 |
| translated |  | 281 | 168 | 74 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 266 | 161 | 71 |
| needs_work |  | 15 | 7 | 3 |
| needs_work rate | ≤ 20.0 % | 5.3 % ✓ | 4.2 % ✓ | 4.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.2 % ✓ | 3.0 % ✓ | 2.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.8 % ✗ | 1.2 % ✗ | 1.4 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.4 % ✓ | 0.6 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 75.0 % ✗ | 55.0 % ✗ |
| cost $ |  | $32.13 | $17.76 | $8.17 |
| $ per approved |  | $0.12 | $0.11 | $0.12 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 26 of 58 (45 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: fact 1 (0 major), overlap 2 (2 major), media 44 (25 major), style 3 (3 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 33 of 60 (55 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.35

Major findings on approved questions:

- **q-20729**: media, style — The question needs an essential video ("Mira: esto se grabó desde la EEI..."), but no file was picked (title is null), so it can't be played. Otherwise the translation is faithful, the options' articles all match, and the facts check out (green from oxygen; the ISS has passed through auroras). One small style point: "cortinilla" sounds Spanish. "cortina de la ventanilla" would be more natural in Latin America. (http://127.0.0.1:8001/review/q-20729)
- **q-20731**: media — The question needs essential media ("Mira: ¿qué plato… se está cocinando aquí?"), but no video file was picked (media title is null), so players get nothing to identify and the question can't be played as it stands. The translation is otherwise faithful and reads naturally in es-419. The facts hold up: idli and dosa use the same batter, and "kuzhi" is the dish's other name. "Huequitos" is a mild diminutive but understood across Latin America. (http://127.0.0.1:8001/review/q-20731)
- **q-20737**: media, style — The video is marked essential, but no file was picked (title null). The question opens with "Mira: esta cascada…" and the text alone could just as well describe Skógafoss, so it can't be played until a Seljalandsfoss video is attached. A minor wording issue: "regadera" in the description means "shower" mainly in Mexico and "watering can" elsewhere, so "ducha" would read more naturally across Latin America. The facts check out: the drop is about 60 m, the cliff is Iceland's former coastline, the river comes from near Eyjafjallajökull, and a path leads behind the falls. The translation is faithful to the source. (http://127.0.0.1:8001/review/q-20737)
- **q-20738**: media — The question needs a video ("Mira: ¿qué ave es esta…?") and the media role is essential, but media.title is null. No file was picked, so there is nothing to identify and the question can't be played. The translation itself looks right: the Spanish names match the species (reinita amarilla = Setophaga petechia, jilguero canario = Spinus tristis, oropéndola europea = Oriolus oriolus, escribano cerillo = Emberiza citrinella). The hints and the fun fact about multi-story nests built over cowbird eggs are true, and hint 3 was sensibly adapted to the Spanish name. (http://127.0.0.1:8001/review/q-20738)
- **q-20743**: media — The essential video has no picked file (title null). The question ("Mira: ¿qué animal anda por esta pecera?") can't be played without footage of a shrimp in a tank. The translation itself is faithful and reads naturally in es-419: "camarón", "cangrejo de río" and "renta" all work. The hints and the fun fact are true: shrimp have ten legs, and their heart sits in the cephalothorax behind the eyes. (http://127.0.0.1:8001/review/q-20743)
- **q-20744**: media — The essential video is missing (the media title is null). The question "Mira: ¿qué famoso avión está despegando aquí?" can't be played without footage of the SR-71 taking off. The translation itself is faithful and natural es-419, and the facts hold: spy plane from the 1960s, above 25 km and Mach 3, and fuel tanks that leaked on the ground. Hint 3 adds "el mirlo", which translates Blackbird, but hint 3 is allowed to come that close. (http://127.0.0.1:8001/review/q-20744)
- **q-20745**: media — The question has essential video media, but no file was picked (title is null). "Mira: ¿qué tipo de pez nada en este estanque?" can't be played without a koi pond clip. The translation itself is faithful and reads as natural es-419. The options are gender-neutral as bare nouns, the hints don't name the answer before hint 3, and the Hanako fun fact matches the source, which correctly says it was "said to be" over 200 years old. (http://127.0.0.1:8001/review/q-20745)
- **q-20746**: media — The question needs its audio clip ("Escucha: …"), but no file is attached (media.title is null), so it can't be played as it is. The text itself is fine. I checked the facts: "O Canada" was first performed in Quebec City in 1880, Weir wrote the English words in 1908, and it became the official anthem on 1 July 1980. The translation matches the source, the options agree grammatically, and the difficulty of 11 fits. (http://127.0.0.1:8001/review/q-20746)
- **q-20747**: media, style — The question needs an audio clip ("Escucha:") to be played, but the media title is null, so no clip of the Dance of the Sugar Plum Fairy has been picked and the question can't be played as it is. A smaller point: "de puntitas" is mainly Mexican, and "de puntillas" would suit a general Latin American audience better. The translation is faithful to the source, the article "El/La" works with all four options, and the facts in the hints and the celesta fun fact are correct. (http://127.0.0.1:8001/review/q-20747)
- **q-20750**: media — The essential audio is missing (media title is null). The question says "Escucha:" and depends on hearing the Toreador Song, so it can't be played without it; this gap comes from the source. The translation is faithful and idiomatic, and the facts are correct: Carmen is set in Seville, Escamillo is a bullfighter, and the 3 March 1875 premiere was three months before Bizet died on 3 June 1875. (http://127.0.0.1:8001/review/q-20750)
- **q-20755**: media — Media is essential video but title is null: no clip was picked, so the "Mira y escucha… este insecto" question can't be played. The translation is faithful and natural es-419, and the facts are correct: male cicadas buckle tymbals (drum-like membranes on the abdomen), the wrong options describe other insects (grasshoppers, crickets, mosquitoes), and the hints and fun fact are true. No overlap with the related cricket question (q-0749). (http://127.0.0.1:8001/review/q-20755)
- **q-20761**: media — The media is essential video, but no file was picked (title is null). The question asks players to identify the DC-8 from footage of it taking off, so it can't be played as it is. The translation itself is faithful and natural es-419. The facts check out: Douglas was a California maker of propeller airliners, the DC-8 was its first jet airliner, it first flew in 1958, the Super 70 series was re-engined with CFM56s in the 1980s, and the Il-62's engines are at the tail. (http://127.0.0.1:8001/review/q-20761)
- **q-20764**: media — The question needs an essential timelapse video ("Mira: este timelapse..."), but media.title is null, so no file was picked and the question can't be played as it stands. I found no other problems. The translation is faithful and natural es-419 ("Adís Abeba" is the standard Spanish form). The facts check out: Nairobi is at about 1.3°S and about 1795 m, the KICC is named after Kenyatta, and Nairobi National Park is on the city's edge. No hint names the answer early. (http://127.0.0.1:8001/review/q-20764)
- **q-20766**: media — The question needs an essential video ("Mira: … este insecto"), but no file was picked (media title is null), so it can't be played as it is. Everything else is fine: the translation matches the source, "Polinizándolas" and the three wrong answers share the same gerund form, the hints and description don't give it away before hint 3, and the fun fact about buzz pollination is true. (http://127.0.0.1:8001/review/q-20766)
- **q-20769**: media — The question needs an essential video ("Mira: … en estos primeros planos"), but media.title is null, so there is no clip and the question can't be played. The translation itself is accurate and reads naturally in es-419. The options agree in gender, the hints don't give the answer away early, and the fun fact is true: Meganeura-type griffinflies had wings about 70 cm across, around 300 million years ago. (http://127.0.0.1:8001/review/q-20769)
- **q-20771**: media — The media is an essential video but its title is null, so no file was picked. Without the Merlion footage the question "Mira: ¿en qué ciudad está esta estatua…?" can't be answered. The translation matches the source, reads naturally in es-419, and its facts are correct (Singapore ~1°N at the tip of the Malay Peninsula, busy port, name means "lion city", Merlion origin). (http://127.0.0.1:8001/review/q-20771)
- **q-20777**: media — The question needs an essential video ("Mira: … este timelapse"), but media.title is null, so no video was picked and the question can't be played without it. The translation itself is faithful and natural es-419. The facts check out: Home Insurance Building (1885), Lake Michigan, the nickname "Ciudad de los Vientos" and the 1900 reversal of the river's flow. (http://127.0.0.1:8001/review/q-20777)
- **q-20779**: media — The media is an essential video, but its title is null, so no file was picked. The question says "Mira… en este video acelerado" and can't be played without the time-lapse. The translation itself is faithful and reads naturally in es-419: the answer, options, hints (Amaryllis named after the shepherdess, Hippeastrum vs. the South African Amaryllis) and article agreement are all fine. (http://127.0.0.1:8001/review/q-20779)
- **q-20782**: media — The question asks players to watch a video, and the media role is essential, but no file was picked (title is null), so it can't be played as it is. The translation itself is faithful and reads naturally. "Atardecer" for "Evening" fits the sunset clip and the hints. One minor point: the orange-sky description already narrows the choice to "Mañana" or "Atardecer", which the source does too. (http://127.0.0.1:8001/review/q-20782)
- **q-20786**: media — The essential video has no file (title is null), but the question depends on it ("Mira despegar esta aeronave…"). Without the takeoff video it can't be played as written. The translation itself is faithful and reads naturally in es-419 ("pista", "aeronave"). The options agree in article and gender. The facts are right: helicopters take off without a runway and can hover and fly backward or sideways. No related question asks the same fact (q-6390 asks what a runway is). (http://127.0.0.1:8001/review/q-20786)
- **q-20792**: media — The essential video is missing (media title is null), but the question depends on it ("Mira: … cruza esta playa"), so it can't be played as it is. The translation itself is faithful and natural in es-419. The facts check out: soldier crabs (Mictyris) walk forwards, sift the sand for food, march in swarms and corkscrew down into the sand. The option forms match, and the difficulty is about right. (http://127.0.0.1:8001/review/q-20792)
- **q-20794**: media — The essential video has no file (title null). The question needs it ("Mira: … este palacio"), so it can't be played without one. This comes from the source's media slot, not from the translation. The translation itself is faithful and reads as natural es-419. I checked the facts for the Palacio de Bellas Artes: it was built 1904–1934 and slowed by the 1910 Revolution, it has Rivera murals, and its Tiffany glass curtain of about a million pieces shows Popocatépetl and Iztaccíhuatl. All are correct, and no related question asks the same fact. (http://127.0.0.1:8001/review/q-20794)
- **q-20803**: media — The question needs a sound clip ("Escucha"), and the fun fact refers to Mozart's concerto, but no audio file is picked (media title is null). Without the clip the question can't be played. The translation itself is faithful and natural es-419. Hint 3 rightly leaves out the word "fagotto", which would give away "Fagot", and the fun fact is correct: Mozart wrote K.191 in 1774, at 18. (http://127.0.0.1:8001/review/q-20803)
- **q-20807**: media — The audio is marked essential, but no audio file was picked (media.title is null). Without the Jupiter recording ("Escucha: …") the question can't be played, and Marte, Venus and Mercurio all fit the text, since they are also movements of the suite. Everything else checks out: the translation is faithful and natural es-419, "the Bringer of Jollity" (hint 2) is correct, and the fun fact about "I Vow to Thee, My Country" and "World in Union" is true. (http://127.0.0.1:8001/review/q-20807)
- **q-20811**: media — The question depends on essential audio, but no audio file was picked (media title is null), so it can't be played. Everything else checks out: the Spanish is natural es-419, and "un aria" is correct Spanish. The fun fact fits K. 330 in C major, which dates from about 1783. The hints are faithful to the source, and none of the related questions asks the same fact. (http://127.0.0.1:8001/review/q-20811)
- **q-4153**: overlap — Related q-7612 (approved, colombia bundle) asks the same fact: what the pelican's pouch under its beak is for, with the answer "Para atrapar peces". Colombian players could see both. Otherwise the translation is faithful and idiomatic, the facts are correct (pouch holds about 10 L), the essential pelican image fits and difficulty 3 is right. (http://127.0.0.1:8001/review/q-4153)

## Needs work

- **q-5869** (athletics) En 1986, ¿qué prueba de lanzamiento del atletismo estrenó un implemento rediseñado que vuela menos, porque los mejores tiros llegaban casi al final del campo? → Lanzamiento de jabalina: source: the fun fact says Hohn's 104.80 m was longer than a soccer field, but the standard international pitch is 105 m and pitches can be up to 120 m, so the claim is wrong (fact check: wrong). The source should say "almost the length of a soccer field (105 m)". The translation copies the source faithfully. Also worth fixing in the source: hint 2 ("its tip sticks in the grass") already points to the javelin, since it is the only implement with a tip. Fact check: wrong. The answer (javelin) is right. The new men's javelin was introduced in 1986 with its center of gravity moved forward, and Uwe Hohn threw 104.80 m on 20 July 1984. The fun fact is shaky. A standard international football pitch is 105 m long, so 104.80 m is slightly shorter. It is not 'more than' the pitch length.
- **q-6258** (famous-logos) ¿Qué color NO está entre los colores de los anillos olímpicos? → Morado: The translation itself is faithful and natural, but the Spanish pool already has the same question: q-6930 asks which colour is missing from the Olympic rings, and its answer is also Morado. Players who get both the base and colombia bundles would meet the same fact twice. Drop one of the two, or replace q-6930 in the colombia bundle.
- **q-6635** (explorers-and-discoveries) Esta tela suave y brillante se fabricó por primera vez en la antigua China. ¿Qué animal produce el hilo para hacerla? → Gusano de seda: Source: hint 2 ("so small it could sit on your fingertip") is wrong. A full-grown silkworm is about 7–8 cm long, and only a newly hatched larva is that small. The source needs a correct hint 2, for example "It is a caterpillar that eats only mulberry leaves", and then the translation should be redone to match. Minor point for the re-translation: "pijamas dignas" uses the feminine, but most of Latin America says "el pijama", so "pijamas dignos" reads more widely. Fact check: wrong. The answer (gusano de seda), the wrong answers (sheep, camel and goat give wool or hair) and the fun fact are fine. The fact is right because cocoon filaments run about 600–900 m, and some sources say up to 1,500 m. Hint 2 is misleading. A full-grown silkworm is about 7–8 cm long, so it doesn't fit on a fingertip. Only the newly hatched larva is that small. This is from general knowledge. I did not run a web search.

## Not travelling

None.

## Stale re-translated

None.
