# batch-80

Made by `qgen batch --media-first` on 2026-11-16 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 85 (q-20729…q-20813)
- Approved: 63
- Needs work: 22
- Dropped by the pipeline: 30
- Reviewed by: claude-opus-5-5
- Claude calls: 839, about $72.88 at list price; $1.16 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-78, batch-79; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-78 | batch-79 | batch-80 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 17 | 112 | 115 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 4 | 30 | 30 |
| drop rate | ≤ 20.0 % | 23.5 % ✗ | 26.8 % ✗ | 26.1 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 2 |
| dropped: hard fail unambiguous |  | 0 | 2 | 3 |
| dropped: hard fail no_giveaway |  | 1 | 5 | 0 |
| dropped: overlap |  | 3 | 23 | 25 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 1 |
| merged |  | 13 | 82 | 85 |
| approved |  | 8 | 64 | 63 |
| needs_work |  | 5 | 18 | 22 |
| needs_work rate | ≤ 20.0 % | 38.5 % ✗ | 22.0 % ✗ | 25.9 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 38.5 % ✗ | 4.9 % ✓ | 8.2 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 1.2 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 1.2 % ✓ | 1.2 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 2.4 % ✗ |
| needs_work: media | ≤ 10.0 % | 15.4 % ✗ | 17.1 % ✗ | 18.8 % ✗ |
| media: no pick in review 1 |  | 1 | 2 | 3 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 13 | 82 | 85 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 1.2 % ✓ | 4.7 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 17.6 % ✓ | 20.5 % ✗ | 23.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 6 | 39 | 36 |
| top move | ≤ 25.0 % | n/a | n/a | n/a |
| values move |  | n/a | n/a | n/a |
| top stimulus |  | n/a | n/a | n/a |
| values stimulus |  | n/a | n/a | n/a |
| top clue | ≤ 60.0 % | n/a | n/a | n/a |
| values clue |  | n/a | n/a | n/a |
| top answer_kind | ≤ 40.0 % | n/a | n/a | n/a |
| values answer_kind |  | n/a | n/a | n/a |
| top lens | ≤ 25.0 % | n/a | n/a | n/a |
| values lens |  | n/a | n/a | n/a |
| giveaway-step drop rate |  | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| mechanical-check rate |  | 0.0 % ✓ | 3.7 % ✓ | 2.4 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.47 ✓ | 3.46 ✓ | 3.43 ✓ |
| cost $ |  | $12.37 | $80.81 | $68.75 |
| $ per approved | ≤ $0.35 | $1.55 ✗ | $1.26 ✗ | $1.09 ✗ |
| calls |  | 130 | 942 | 779 |
| calls per approved |  | 16.25 | 14.72 | 12.37 |
| wall time h |  | 0.90 | 2.76 | 1.98 |
| days |  | 1 | 2 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 44 (5 %)
- Major among review needs work: 8 of 16 (50 %)
- Problems by kind: giveaway 14 (3 major), fact 1 (0 major), ambiguity 1 (0 major), overlap 3 (3 major), media 13 (6 major), difficulty 3 (3 major), other 2 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 50 of 60 (83 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.13

Major findings on approved questions:

- **q-20766**: overlap, giveaway — Overlap: approved q-5770 asks the same fact (bees moving grains from flower to flower is called pollination), so one question gives the other away. Giveaway: the question text alone ("visits one flower after another") plus the description's "striped worker" answers it without the clip, so the video isn't needed. The facts hold: the Commons file is a rusty patched bumble bee (USFWS) and buzz pollination of tomatoes is real. The −37 LUFS level is only motor noise and doesn't matter for a video. I had no Read tool, so I couldn't open the frame sheet or the spectrogram. (http://127.0.0.1:8001/review/q-20766)
- **q-20804**: giveaway — The window has spec text burned into the video. OCR of frame 5 (33.95 s) reads “FOUR D-27 ENGINES WITH SV-27 —” and the line is cut off. On Antonov's promo footage it very likely goes on with “contra-rotating propfans”, which would name the answer on screen. I couldn't open the frame sheet or spectrogram (no file-reading tool), so check that frame by eye, or trim the window to end before 33 s. The facts hold: the An-70's SV-27 propfans have 8 front and 6 rear blades turning in opposite directions. The wrong options are clearly wrong. Players can work it out by seeing two rows of blades, so I'd rate it about 11 rather than 13 (not a big enough gap to flag). The “title-words” flag is a false alarm: “military transport” doesn't narrow the options. (http://127.0.0.1:8001/review/q-20804)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of national anthems | 30 | 14 | 14 | 12 | 9 | 4 |
| cat:Videos of animals | 30 | 11 | 11 | 11 | 8 | 8 |
| q:audio:classical music recording symphony | 30 | 13 | 13 | 13 | 9 | 8 |
| q:audio:dog bark | 30 | 1 | 1 | 0 | 0 | 0 |
| q:audio:drum percussion recording | 1 | 0 | 0 | 0 | 0 | 0 |
| q:audio:flute clarinet saxophone trumpet | 15 | 4 | 4 | 3 | 2 | 2 |
| q:audio:musical instrument sample | 30 | 10 | 10 | 9 | 7 | 4 |
| q:audio:national anthem instrumental | 30 | 17 | 17 | 17 | 14 | 3 |
| q:audio:piano sonata public domain | 12 | 6 | 6 | 6 | 4 | 4 |
| q:audio:whale song | 30 | 0 | 0 | 0 | 0 | 0 |
| q:video:aircraft takeoff video | 30 | 11 | 11 | 10 | 8 | 8 |
| q:video:animal video wildlife | 30 | 11 | 11 | 11 | 7 | 7 |
| q:video:city timelapse video | 30 | 10 | 10 | 10 | 8 | 8 |
| q:video:cooking video | 30 | 5 | 5 | 5 | 3 | 1 |
| q:video:time-lapse video | 30 | 8 | 8 | 8 | 6 | 6 |
| total | 388 | 121 | 121 | 115 | 85 | 63 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 286 | 71 | 71 | 67 | 49 | 44 |
| pd-music | 102 | 50 | 50 | 48 | 36 | 19 |
| total | 388 | 121 | 121 | 115 | 85 | 63 |

- $ per approved: $1.16

## Needs work

- **q-20733** (countries) Listen: this is the national anthem of which African country? → Liberia: Almost no player can tell Liberia's anthem from Sierra Leone's, Ghana's or Nigeria's by the tune alone. Three similar brass-band anthems can't be told apart by ear, so the 50-second window doesn't decide the answer. Only the hints (1847, never colonized, Monroe) make it answerable, which the house style calls a bad 15. No other fair question about this window comes to mind (asking for the instrument or the kind of band would be trivial), so the file doesn't suit a question.
- **q-20735** (countries) Listen: this is the national anthem of which country? → Azerbaijan: You can't tell the answer from the clip. Hardly any player, adults included, could recognise Azerbaijan's anthem by ear or tell it apart from the anthems of Armenia, Georgia or Kazakhstan. It is a Western-style march with no clear sound clue, so the question only works through geography hints and the recording adds nothing. It rests on a fact nobody could work out, much like the sibling anthem questions q-20648 and q-20650. No other question about this 55-second band window would work for the players, so I'd drop the file or this question.
- **q-20739** (history) Listen: this march was the official imperial anthem of which empire? → The Ottoman Empire: The clip doesn't help answer the question. The Mahmudiye March is a European-style military march by an Italian composer, and listening to it you can't tell it apart from an Austrian or Russian imperial march. Players can only answer from hint 2 or 3, so the audio decides nothing. No other question about this 60-second window would work for players: "which kind of piece" (a march) is trivial, and "which composer" is a test only experts pass.
- **q-20752** (countries) Listen: this is the national anthem of which Southeast Asian country? → Laos: The question rests only on recognizing the Lao anthem by ear. Almost no player can tell this generic brass-band march apart from the anthems of Cambodia, Myanmar or Thailand, so the clip can't decide the answer. That makes it a bad question, not a fair 15. Hint 1 ("the only landlocked country in Southeast Asia") would also give the answer away to anyone who knows geography, so the question turns into a geography question and the clip isn't needed. No other question about this window seems workable, so the file doesn't fit a family question.
- **q-20754** (countries) Listen: which country has this national anthem? → Central African Republic: Nobody, trivia specialists included, can tell the Central African Republic's anthem from Gabon's, Cameroon's or Congo's by ear, so the clip doesn't decide the question. Only hint 3 (landlocked, name gives its location) makes it solvable, which makes it a 15 only because the fact is obscure. The recording is also poor: it is band-limited to about 4.5 kHz, has crackle all the way through, and is very hot (−5.7 LUFS, true peak +1.0 dBFS), so it is likely clipped. No other question about this window would be fair to players, so drop the file for this question.
- **q-20756** (world-cuisines) Watch: strips of dough are wound around wooden rollers and turned over hot charcoal. Which Central European treat is being baked? → Trdelník: The clip, and the question's clue ("Central European treat" baked on wooden rollers over charcoal), fit Hungary's kürtőskalács just as well as trdelník. The two look the same on the spit, so a Hungarian player would rightly name the other pastry. The text needs a clue that only trdelník has, for example that it is sold all over Prague's Old Town or that it is the Czech and Slovak version. Then the clip shows the baking and the text picks out which name is meant.
- **q-20767** (classical-music) Listen: which composer wrote this symphony? → Antonín Dvořák: The clip can't be relied on to identify Dvořák by ear. The file's title says it is the start of the 3rd-movement Scherzo, but its Commons description says it is the 3rd record of the Largo. Either way, the 60-second window is probably not the famous cor anglais “Going Home” theme. Telling Dvořák's style from Tchaikovsky, Brahms and Beethoven by ear in a lesser-known passage is a test only musicians pass, not a question most adults can answer. Use an excerpt that surely holds a widely known theme, such as the Largo's cor anglais melody or the finale's opening brass theme, and confirm which movement the file contains before reusing it.
- **q-20770** (countries) Listen: this is the national anthem of which country? → Bulgaria: Almost no player can tell “Mila Rodino” apart from the Romanian, Serbian or Greek anthems by ear, so the clip doesn't decide the answer. Players can only get there through hint 2 (Black Sea plus Cyrillic) or hint 3 (Sofia). That makes this a near-unknowable ear test, not a fair 15, and changing the wording can't fix it, because any question about an instrumental anthem in this window still comes down to recognizing the tune. Also, the work basis says the composer died in 1948; Radoslavov actually died in 1931. The public-domain status holds either way.
- **q-20774** (countries) Listen: this is the national anthem of which European country? → Montenegro: Almost nobody can tell Montenegro's anthem apart from Serbia's, Croatia's or North Macedonia's by ear, trivia specialists included. Players can only get the answer from the hints, so the clip doesn't help them answer. This file fails media-first check 1 (the listener can't tell it from the wrong options). No other question about this instrumental window works for the players either. Drop the question or pair the file with a different kind of question.
- **q-20775** (countries) Listen: this is a national anthem. In which region of the world is its country? → The Arabian Peninsula: The window is a Western-style brass/band arrangement with no regional musical colour, so nobody can hear which region the anthem comes from; only the hints decide it, and hint 3 nearly names Yemen. The clip doesn't do the work the question claims for it, and no other question about this anonymous anthem window would be answerable for the players.
- **q-20776** (countries) Listen: this is the anthem of a breakaway region on the Black Sea coast, recognized by Russia in 2008. Which region is it? → Abkhazia: The text alone gives the answer: "breakaway region on the Black Sea coast, recognized by Russia in 2008" points only to Abkhazia among the options (South Ossetia has no coast, and Russia doesn't recognize Transnistria or Northern Cyprus), so the clip adds nothing. If the clue moves into the audio, nobody can tell the Abkhaz anthem by ear from those of South Ossetia, Transnistria or Northern Cyprus. I can't see another fair question about this window, so the file doesn't work as an essential media-first clip.
- **q-20778** (musical-instruments) Listen: this is a country's national anthem. What kind of group is playing it? → A military wind band: Hint 2 ("Listen for the instruments you blow into, not ones with strings or keys") rules out all three wrong answers: the string quartet and pianist have strings or keys, and the organ is played from keys. So hint 2 gives the answer away. Make hint 2 vaguer, for example about how loud the group is or how many players it has, and keep the instrument families for hint 3.
- **q-20780** (classical-music) Listen: this famous tune paints a spooky scene at midnight. What is happening in it? → Skeletons dance in a graveyard: This question asks for the same fact as related draft q-20812, which is also a “Danse Macabre” listening question with the answer “Skeletons dancing in a graveyard at midnight”. Keep only one of the two in the pool. The audio and the background picture are fine.
- **q-20781** (countries) Listen: for more than 60 years, this was the national anthem of which African country? → Niger: Players can't tell Niger's former anthem from the anthems of Mali, Senegal or Burkina Faso by ear. All four are French-style military-band anthems from the 1960s, so the window doesn't decide the question, and it can only be solved from the hints (hint 3 names the river and the capital). No other question about this window would work for the players: only "which kind of piece is this" (a national anthem), which is trivial and dull. The file doesn't fit a media-first question.
- **q-20785** (classical-music) Listen to this brass march. At which kind of event would you most likely hear music like this? → A funeral: The description ("Trumpets and tubas that clearly woke up on the wrong side of the bed") tells players the music is in a bad, gloomy mood. That is the one trait the clip is meant to show, and it rules out the three happy options (wedding, birthday party, carnival) before anyone listens. Rewrite it so it plays on brass bands or marching without describing the mood, for example a joke about tubas being heavy to carry.
- **q-20787** (countries) Listen: this is the national anthem of which Pacific island country? → Tonga: The text is fine. The only problem is the media metadata, and code makes it needs_work. The work basis “composed in the 19th century; the composer died long ago” is not one of the allowed bases. Karl Gustavus Schmitt died around 1900, so the basis should be recorded as died-70-years. The recording itself is free (PD Mark / CC BY 3.0 from nationalanthems.info). Once the basis is corrected, this can be approved with background pick 4. Media.work basis “composed in the 19th century; the composer died long ago; public domain” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-20788** (countries) Listen: this is the national anthem of which place? → Palestine: Licence: the piece isn't in the public domain. Ali Ismael died in 1974, so the 70-year term hasn't run out, and leaving out the lyrics doesn't change that. The recording is also a YouTube re-upload tagged "License review needed (audio)". Players also couldn't tell this anthem from Lebanon's or Algeria's by ear. Drop the question or find a truly public-domain file. Media.work basis “composer died 1974; instrumental recording, so no lyrics are used” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-20797** (countries) Listen: this is the national anthem of which country? → Chad: Players can't tell Chad's anthem apart from those of Niger, Mali or the Central African Republic by listening; they all sound alike as brass-band anthems in a French-colonial style. So the clip can't decide the question, and only hint 3 (Lake Chad) does. The recording itself is fine (about −12 LUFS, clean, public domain), but every question about this window would be an ear test nobody passes, apart from the trivial "this is a national anthem". The file doesn't fit a question.
- **q-20806** (countries) Listen: this was the national anthem of a Southeast Asian republic from 1979 to 1989. Which country uses that land today? → Cambodia: You can't recognize this anthem by ear, so the clip plays no part in the answer. The question is solved entirely by its text: "Southeast Asian republic from 1979 to 1989" points straight to the People's Republic of Kampuchea, so the "Listen:" framing is empty. No other question about this 60-second instrumental march would work for players (no lyrics, no famous tune, nothing distinctive to listen for), so the file doesn't fit a media-first question. It should be dropped, or the fact reused as a plain text or image question.
- **q-20808** (world-cuisines) Watch: which flatbread is this cook making in her Kenyan home? → Chapati: The description (“the best kitchen gadget is still a rolling pin”) says the bread is made from rolled dough, so it rules out injera and crêpe, both poured batters, before the clip plays. Rewrite it so it plays on home cooking or flatbreads without naming rolling or any other way of shaping the bread.
- **q-20812** (classical-music) Listen: this is a modern arrangement of a famous orchestral piece that tells a story. What scene does the music describe? → Skeletons dancing in a graveyard at midnight: This asks the same thing as draft q-20780 (“this famous tune paints a spooky scene at midnight. What is happening in it?” → skeletons dance in a graveyard). Both are Danse Macabre and both have the same answer, so the pool should keep only one of them.
- **q-20813** (countries) Listen: this is the anthem of a Pacific nation made of one single coral island, in free association with New Zealand. Which one? → Niue: The clip does nothing here. The text alone gives the answer: of the four options, only Niue is a single coral island in free association with New Zealand. Almost nobody can recognise Niue's anthem by ear, so taking the text clues out would leave a question nobody can answer. No other question about this instrumental window would work for families. Also, the licence basis still says “verify”: the anthem was composed in 1974 by Sisilia Talagi, so its public-domain status needs confirming.

## Question axes

- move: None 85
- stimulus: None 85
- clue: None 85
- answer_kind: None 85
- lens: None 85

## Dropped by the pipeline

- mf-12dc950d93: overlap like q-0724: Mira la foto: ¿qué lugar famoso es este? → El Gran Cañón: Watch: clouds drift over this huge natural wonder. Which famous place is it? → The Grand Canyon
- mf-136a12ffee: overlap like q-20642: Listen: this famous opera tune is sung here in English. Which Italian composer wrote it? → Giuseppe Verdi: Listen: which composer wrote this famous opera chorus? → Giuseppe Verdi
- mf-1f5979fc41: overlap like q-19841: Listen: which animal is making this sound in a British garden? → A bumblebee: Watch: which insect is visiting these white flowers? → Bumblebee
- mf-320d4f0ac1: hard fail: correct 3, unambiguous 3, no_giveaway 4, no_overlap 5: Watch: what does the baker use to move and turn the bread inside this clay oven? → Two thin sticks
- mf-4ab550b67e: overlap like q-6243: Which big animal is this, seen roaming in Yellowstone National Park? → A bison: Watch: which animal is rolling around in the dust? → Bison
- mf-5372573854: overlap like q-14988: Dieses Foto zeigt einen Teil eines berühmten Bauwerks in Deutschland. Welches ist es? → Kölner Dom: Watch: in which city does this huge cathedral stand? → Cologne
- mf-607f1c25b9: overlap like q-20634: Listen: who composed this lively piece with its racing flute melody? → Johann Sebastian Bach: Listen: which composer wrote this piece? → Johann Sebastian Bach
- mf-68e3b906e3: overlap like q-20682: Watch: where is this man doing his workout? → On the International Space Station: Watch: where was this video of Earth filmed from? → The International Space Station
- mf-6ef7b0c1a9: overlap like q-9060: Which river carved the canyon in this photo? → Colorado River: Watch: which river carved the famous canyon shown in this time-lapse video? → The Colorado River
- mf-827179a0c0: overlap like mf-10a37719be: Listen: this old national anthem was retired, but part of its melody lives on in which country's anthem today? → South Africa: Listen: this old anthem melody is now joined with another song to form one national anthem. Which song? → Nkosi Sikelel' iAfrika
- mf-9ddef43dea: overlap like q-3859: The three letters in the name of the delivery company DHL stand for what? → Its three founders: Watch: this jet has no rows of passenger windows along its body. What does it carry? → Parcels and letters
- mf-a1381ecea5: overlap like q-14080: Dieses Tier läuft dir im Watt an der Nordsee über den Weg. Zu welcher Tiergruppe gehört es? → Krebstiere: Watch: which group of animals does this rock climber belong to? → Crustaceans
- mf-a29bf65484: overlap like q-0407: Mira la foto: ¿cómo se llama esta verdura? → Brócoli: Watch: which green vegetable is stirred into the pan with the chicken? → Broccoli
- mf-a540d30014: overlap like q-0122: Escucha: ¿qué ave hace este sonido? → El pájaro carpintero: Watch: what kind of bird is the black-and-white one clinging to the side of the feeder? → A woodpecker
- mf-b28c3a39a4: overlap like q-20640: Listen: this lively symphony finale weaves several tunes together at the same time. Who composed it? → Wolfgang Amadeus Mozart: Listen: which composer wrote this famous symphony? → Wolfgang Amadeus Mozart
- mf-c1302a0526: overlap like mf-58d5040fd0: Listen: this anthem's melody began as a church hymn in Spanish colonial times. Which country's national anthem is it? → Nicaragua: Listen: this melody is now a national anthem. What was it first written as, more than a century ago? → A church hymn
- mf-c18b71ce28: overlap like q-0538: Los arrecifes de coral están hechos por millones de pólipos diminutos como los de la foto. ¿A qué grupo de animales pertenecen? → Cnidarios: Watch: to which major group of animals do these creatures belong? → Cnidarians
- mf-c263aaa916: overlap like q-20757: Watch the tips of this jet’s wings, which bend upward. What is the main job of these upturned tips? → Cutting air drag to save fuel: Watch the very end of the wing: what is that upturned tip called? → Winglet
- mf-c34c9ae6a2: overlap like q-19154: It's black and white, a small group of them lives off the west coast of Scotland, and it's the biggest member of the dolphin family. What is it? → Orca: Watch: the animal swimming in this clip is the largest member of which animal family? → Dolphins
- mf-c402b47d1e: overlap like q-20703: Listen to this fast, sparkling finale of a piano concerto. Which composer wrote it? → Camille Saint-Saëns: Listen: which composer wrote this showpiece for violin and orchestra? → Camille Saint-Saëns
- mf-ca7982d38e: overlap like q-13324: El himno de este pequeño país no tiene letra oficial. Está rodeado por Italia y es una república antiquísima. ¿Cuál es? → San Marino: Listen: this solemn, hymn-like national anthem belongs to which tiny European country? → San Marino
- mf-d44dce0f0f: overlap like mf-cd6aca5da2: Listen: from which era of Western music does this slow orchestral piece come? → The Classical period: Listen to this orchestral piece. Which era of Western classical music does its style belong to? → Classical
- mf-e65ec9ed70: overlap like q-20750: Listen: the opera this famous song comes from is set in which country? → Spain: Listen: which opera does this famous aria come from? → Carmen
- mf-e95a699437: overlap like q-20775: Listen: this is a national anthem. In which region of the world is its country? → The Arabian Peninsula: Listen: this is the national anthem of which country? → Yemen
- mf-f511c9e724: overlap like q-20636: Listen to this fast, stormy symphony movement. Who composed it? → Ludwig van Beethoven: Listen: which composer wrote this piano sonata? → Ludwig van Beethoven
- mf-01de861fbc: fact-check wrong: Hint 2 is false. Mozart wrote K. 545 in 1788 when he was 32, not a teenager. Beethoven was about 17 then, and he did not write it.: Listen to this famous piano opening. What nickname does the sonata it comes from carry? → “Sonata facile”
- mf-2b70dd23f3: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Listen: this is the national anthem of which country? → Equatorial Guinea
- mf-69acdee5f0: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Listen: this anthem’s melody was first written for a Soviet republic and kept after independence, with new words. Which country’s anthem is it? → Tajikistan
- mf-7d08027719: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 5: Watch: these dark, dolphin-like animals travel in big groups in warm tropical seas. What are they? → Melon-headed whales
- mf-cd6aca5da2: overlap like mf-d44dce0f0f: Listen to this orchestral piece. Which era of Western classical music does its style belong to? → Classical: Listen: from which era of Western music does this slow orchestral piece come? → The Classical period
