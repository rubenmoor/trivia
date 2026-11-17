# batch-81

Made by `qgen batch --media-first` on 2026-11-16 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 74 (q-20814…q-20887)
- Approved: 59
- Needs work: 15
- Dropped by the pipeline: 32
- Reviewed by: claude-opus-5-5
- Claude calls: 996, about $87.73 at list price; $1.49 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-79, batch-80; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-79 | batch-80 | batch-81 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 112 | 115 | 106 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 30 | 30 | 32 |
| drop rate | ≤ 20.0 % | 26.8 % ✗ | 26.1 % ✗ | 30.2 % ✗ |
| dropped: hard fail correct |  | 1 | 2 | 0 |
| dropped: hard fail unambiguous |  | 2 | 3 | 1 |
| dropped: hard fail no_giveaway |  | 5 | 0 | 4 |
| dropped: overlap |  | 23 | 25 | 27 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 1 | 0 |
| merged |  | 82 | 85 | 74 |
| approved |  | 64 | 63 | 59 |
| needs_work |  | 18 | 22 | 15 |
| needs_work rate | ≤ 20.0 % | 22.0 % ✗ | 25.9 % ✗ | 20.3 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 4.9 % ✓ | 8.2 % ✓ | 9.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.2 % ✓ | 0.0 % ✓ | 2.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 1.2 % ✓ | 1.2 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 2.4 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 17.1 % ✗ | 18.8 % ✗ | 13.5 % ✗ |
| media: no pick in review 1 |  | 2 | 3 | 1 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 82 | 85 | 74 |
| needs_work: difficulty | ≤ 10.0 % | 1.2 % ✓ | 4.7 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 1.4 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 20.5 % ✗ | 23.5 % ✗ | 25.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 39 | 36 | 39 |
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
| mechanical-check rate |  | 3.7 % ✓ | 2.4 % ✓ | 4.1 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.46 ✓ | 3.43 ✓ | 3.36 ✗ |
| cost $ |  | $80.81 | $68.75 | $83.50 |
| $ per approved | ≤ $0.35 | $1.26 ✗ | $1.09 ✗ | $1.42 ✗ |
| calls |  | 942 | 779 | 936 |
| calls per approved |  | 14.72 | 12.37 | 15.86 |
| wall time h |  | 2.76 | 1.99 | 2.65 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 48 (2 %)
- Major among review needs work: 7 of 12 (58 %)
- Problems by kind: giveaway 12 (3 major), fact 2 (2 major), ambiguity 2 (1 major), media 9 (6 major), difficulty 4 (4 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.24

Major findings on approved questions:

- **q-20845**: media, difficulty — I couldn't open the frame sheet or the spectrogram because no Read tool was available, so this verdict rests on the OCR text and the question's wording. The question itself calls the clip "busy street scenes", and the OCR only picks up TSUTAYA, a chain found all over Japan. Nothing points to an Osaka landmark (Glico sign, Tsutenkaku, Osaka Castle, Umeda Sky Building) in the 145–205 s window. Generic time-lapse streets look the same in Tokyo or Yokohama, so players can only answer from the hints, and the "from the window" check fails. If no landmark shows, it's a guess even at 14, not a 12. If a landmark is clearly in the frames, the question should name it as what to look for. Minor issues: hint 2 (takoyaki) repeats the main clue of related q-0690. The soundtrack is a Jamendo track whose licence is unverified, and Commons marks the file "License review needed". Hints 1 and 3 and the Glico fun fact (sign since 1935, replaced several times) are correct. (http://127.0.0.1:8001/review/q-20845)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 30 | 9 | 9 | 9 | 4 | 2 |
| cat:Audio files of national anthems | 30 | 9 | 9 | 9 | 7 | 1 |
| cat:Videos by NASA | 30 | 8 | 8 | 8 | 6 | 6 |
| cat:Videos of animals | 30 | 4 | 4 | 4 | 2 | 2 |
| q:audio:classical music recording symphony | 19 | 6 | 6 | 6 | 5 | 5 |
| q:audio:musical instrument sample | 30 | 6 | 6 | 6 | 6 | 5 |
| q:audio:national anthem instrumental | 30 | 13 | 13 | 13 | 8 | 5 |
| q:audio:piano recording | 30 | 9 | 9 | 5 | 3 | 3 |
| q:audio:piano sonata public domain | 30 | 13 | 13 | 5 | 4 | 4 |
| q:audio:violin cello recording | 17 | 6 | 6 | 6 | 3 | 3 |
| q:video:NASA video launch | 30 | 1 | 1 | 1 | 1 | 1 |
| q:video:aircraft takeoff video | 30 | 3 | 3 | 3 | 3 | 3 |
| q:video:animal video wildlife | 30 | 6 | 6 | 6 | 5 | 4 |
| q:video:city timelapse video | 22 | 3 | 3 | 3 | 2 | 2 |
| q:video:cooking video | 30 | 4 | 4 | 4 | 3 | 2 |
| q:video:newsreel | 30 | 2 | 2 | 1 | 1 | 0 |
| q:video:rover mars video | 30 | 3 | 3 | 2 | 1 | 1 |
| q:video:space station astronaut video | 5 | 1 | 1 | 1 | 1 | 1 |
| q:video:time-lapse video | 30 | 5 | 5 | 5 | 3 | 3 |
| q:video:traditional dance video | 30 | 7 | 7 | 7 | 4 | 4 |
| q:video:train video | 30 | 2 | 2 | 2 | 2 | 2 |
| total | 573 | 120 | 120 | 106 | 74 | 59 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 434 | 77 | 77 | 72 | 49 | 44 |
| pd-film | 30 | 2 | 2 | 1 | 1 | 0 |
| pd-music | 109 | 41 | 41 | 33 | 24 | 15 |
| total | 573 | 120 | 120 | 106 | 74 | 59 |

- $ per approved: $1.49

## Needs work

- **q-20818** (countries) Listen: this is the national anthem of which country? → Armenia: Almost no player outside Armenia can recognise “Mer Hayrenik” by ear or tell it apart from the anthems of Georgia, Azerbaijan and Moldova. The clip can't decide the answer, so the question comes down to the hints or a lucky guess. The recording itself is clean (−11.1 LUFS, no silence, no clipping on the spectrogram) and correctly public domain. But no other question about this instrumental window would be fair to its players, so the file doesn't work as an essential clip for a family game.
- **q-20822** (countries) Listen: this is the national anthem of a small island nation in the Pacific Ocean. Which country is it? → Nauru: Players can't recognise Nauru's anthem by ear or tell it apart from the anthems of Tuvalu, Palau or Kiribati. The clip is a generic brass-band anthem, so the hints and luck decide the question, not the window (media-first check 1). The licence basis is also shaky: composer Laurence Hicks died in 1997, so 'pd-music' only holds if the anthem counts as a government work. Commons tags the recording CC BY-SA 3.0 (nationalanthems.info). Drop this file or check the composition's copyright.
- **q-20823** (birds) Listen: which night bird of the American tropics sings this song? → Common potoo: The description's "never sleeps on the job, only on a branch" gives away the potoo's defining trait: by day it roosts on a branch, disguised as part of it, which hint 2 also uses as the clue. It also rules out the oilbird, which roosts in caves, and the pauraque, which rests on the ground. Rewrite the description to play on the night-shift theme without saying where the bird rests.
- **q-20830** (birds) Watch: which kind of duck is the adult swimming with these ducklings? → Mallard: The description uses "armbands", a British word for swimming aids. American English says "water wings" or "floaties", and the house style asks for wording all English speakers share. Reword it with neutral words (for example "no floaties, no whistle" or "no swim coach, no whistle"). Everything else passes: the clip clearly shows a mallard drake with ducklings.
- **q-20843** (countries) Listen: who composed the music of this national anthem? → Phra Chenduriyang: Licence: Phra Chenduriyang died in 1968, so the melody is not 70+ years past the composer's death. The basis given (Thai life+50) doesn't meet the house rule, and the hard mechanical flag work-basis is real. Also, the clip doesn't help answer: only people who know the Thai anthem by ear can place it, and the composer's name still has to be memorised, so this is an ear test plus a specialist fact. No text fix can save it. Drop it, or keep the file only if the developer accepts a Thai life+50 basis. Media.work basis “composer died 1968 (Thai copyright: life + 50 years); old gramophone recording” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-20844** (manners-and-customs) Watch: men train in a sunken, eight-sided pit at this traditional gym, with spectators all around. Which country does this tradition come from? → Iran: The question text is fine. The only problem is the media's `work.basis`, "Public-domain newsreel, as marked on Wikimedia Commons", which isn't one of the accepted bases, so the code check fails as a hard error. The file's Commons categories include "PD US USIA": News of Iran was made by the US Information Agency. Change the basis to government-work (US government work, USIA) and re-run. No text change is needed. Media.work basis “Public-domain newsreel, as marked on Wikimedia Commons” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-20849** (countries) Listen: this instrumental piece is the national anthem of a partially recognized state. Which one? → Sahrawi Arab Democratic Republic (Western Sahara): Check 1 fails: almost no player, even a trivia specialist, can recognise the SADR anthem by ear or tell it from the anthems of Somaliland, Kosovo or Transnistria. The clip adds nothing and the question can only be answered from the hints (hint 3 nearly names it), so it rests on a fact nobody could know. I can't see another question about this window that players could answer (it's just a band playing an anthem), so the file doesn't work as a media-first question.
- **q-20853** (countries) Listen: this is a former national anthem of an African country. Which country used it? → Ethiopia: Players can't answer from the clip. Almost nobody, trivia specialists included, can recognise the Derg-era Ethiopian anthem (1975–1992) or tell it apart from the equally obscure former anthems of Mozambique, Somalia or Congo. So the question is answered only from the hints, and hint 2 ("Horn of Africa", "never a colony for long") already points straight to Ethiopia. The window offers no other question that families could answer by listening, so this file doesn't work for a playable question.
- **q-20858** (world-music) Listen: this national anthem's title means what in English? → “Army March”: Players can't answer this from the window. Almost nobody can tell Vietnam's anthem by ear, so they would have to recognise the anthem by sound and then also know what its Vietnamese title means. Without the hints that is a guess even for anthem fans, and hint 2 (Hanoi) skips the recording altogether. The hard mechanical licence flag also stands: the recorded basis is "rights donated in 2016", which isn't an accepted basis. If the file stays, recode it as an anthem or government work (Commons category "PD Vietnam Government"). Media.work basis “rights donated to the Vietnamese state and people by the composer's family in 2016; Commons marks it public domain” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-20859** (birds) Listen: these loud screeches were recorded in a German city. Which bird is making them? → Rose-ringed parakeet: Hint 2 gives the answer away. A "strong, hooked red beak" means a parrot, and only one of the four options is a parrot, so players can answer without hearing the clip. Rewrite hint 2 so it narrows things down without naming parrot traits, for example by saying the bird is not originally from Europe, or that it lives in noisy flocks that sleep together in the same trees.
- **q-20861** (countries) Listen: this is the opening of a national anthem. Which country's anthem is it? → Argentina: The 45 s window isn't just an orchestral intro, as the note says. The spectrogram changes at about 10 s to what looks like singing, and the transcript ("A su dronno di Misi…") matches the line "Ya su trono dignísimo abrieron", which is sung near the end of the window. The next words are "las Provincias Unidas del Sud" (Argentina's old name) and then "Al gran pueblo argentino, ¡salud!". So the window ends right before, or inside, the lines that name the country. Someone needs to listen and set the excerpt end before "Ya su trono…" (roughly 35 s or earlier), or confirm by ear that nothing past "dignísimo" is heard.
- **q-20864** (countries) Listen: this march was the national anthem of a pro-Soviet government in the 1980s. Which country was it? → Afghanistan: You can't answer this from the clip. Mongolia, Ethiopia and Laos also had pro-Soviet governments in the 1980s, so the text doesn't separate the options, and almost no one can identify the 1978–1992 Afghan anthem by ear. Hint 2 also gives the answer away: Soviet troops were stationed in the 1980s only in Afghanistan, of these four. Any question about this window would either be a pure ear test or be answered by the text alone, so the file doesn't support a fair question.
- **q-20872** (countries) Listen: this is the national anthem of a kingdom. Which country is it? → Jordan: Players can't recognise Jordan's anthem by ear: a generic brass-band anthem sounds much like the anthems of Saudi Arabia, Morocco or Bahrain, so the clip never decides the answer and the hints do all the work. Hint 2 (Aqaba) gives the answer away on its own, and "a few kilometers" understates the coastline, which is about 26 km. No other question about this window would work, since the only thing a listener can tell from it is "a brass band playing an anthem".
- **q-20882** (classical-music) Listen: which piano piece by Franz Liszt is this? → Consolation No. 3: The description gives the answer away. “Soft music for when your soul needs a warm blanket” states the defining trait (soothing, comforting) and paraphrases the title “Consolation”. With only the four options, before any listening, that rules out the three famously showy pieces (Hungarian Rhapsody No. 2, La Campanella, Mephisto Waltz). Hint 1 (“wants to soothe you, not to show off”) does the same. The description should play on the piano or Liszt theme without naming the mood, and hint 1 should point to something other than “calm versus showy”.
- **q-20884** (world-cuisines) Watch: the cooks make big flames leap out of their pans. Which French cooking word names this fiery trick? → Flambé: The text answers the question without the clip: "big flames leap out of their pans" and "fiery trick", with Poach, Braise and Blanch as the other options, point straight to Flambé, so the video adds nothing. Rewrite it so the flames are only seen, not described. For example: "Watch these cooks at work: which French cooking word names what they're doing?" Make the description vaguer the same way. There's also a fact risk: the Commons file only says "Cooking Calimari", and the flames may be oil or wine flare-ups while tossing the pan, not a true flambé (alcohol added on purpose and lit). Either confirm the Gilroy cooks really light alcohol, or word the question so it doesn't claim the clip shows a textbook flambé.

## Question axes

- move: None 74
- stimulus: None 74
- clue: None 74
- answer_kind: None 74
- lens: None 74

## Dropped by the pipeline

- mf-04fd8dd449: overlap like q-2909: Typhoons are giant spinning storms. In which ocean do they form? → Pacific Ocean: Watch: this kind of storm has a different name in different oceans. What is it called where these are forming? → Hurricanes
- mf-0adfb4aff4: overlap like q-4931: Lederhosen are tough leather shorts from the Alps, now worn at Oktoberfest. Who mainly wore them at first? → Farmers and hunters: Watch: what are the short leather trousers with suspenders that these Alpine dancers are wearing called? → Lederhosen
- mf-0ebaef8909: overlap like q-0724: Mira la foto: ¿qué lugar famoso es este? → El Gran Cañón: Watch: a storm rolls over layered red rock walls in this time-lapse. Which famous natural wonder is this? → The Grand Canyon
- mf-1432427ff6: overlap like q-16815: I'm a diving bird with red eyes and a checkered black-and-white back. My wailing call echoes over Minnesota's lakes, where I'm the state bird. What am I? → The common loon: Listen: which bird makes this long, haunting call? → Common loon
- mf-14d0a3c658: overlap like q-20636: Listen to this fast, stormy symphony movement. Who composed it? → Ludwig van Beethoven: Listen: which composer wrote this famous melody? → Ludwig van Beethoven
- mf-4af413304a: overlap like q-20640: Listen: this lively symphony finale weaves several tunes together at the same time. Who composed it? → Wolfgang Amadeus Mozart: Listen: which composer wrote this stormy piano piece? → Wolfgang Amadeus Mozart
- mf-5b2419566c: overlap like q-20693: Watch: in which country is this festival dance performed? → India: Watch: in which country are these men dancing in white wraps and patterned shawls? → India
- mf-5c7f007a2a: overlap like q-17599: Scott Joplin, who wrote “The Entertainer,” is the most famous composer of which piano style, and was called its “King”? → Ragtime: Listen: which style of piano music is this? → Ragtime
- mf-6215db8193: overlap like q-0943: Pasa de noche, la Luna se pone rojiza durante un rato y no necesitas gafas especiales para verla. ¿Qué es una 'luna de sangre'? → Un eclipse total de Luna: Watch the Moon in this timelapse over a city at night. Which sky event is happening? → A lunar eclipse
- mf-67c26f2b5f: overlap like q-20829: Listen: this melody opened the old anthem of the Kingdom of Yugoslavia. Today it is the national anthem of which country? → Serbia: Listen: this is a Balkan country's national anthem. What is its title in English? → “God of Justice”
- mf-804e7fb98b: overlap like q-13483: Mira la foto: este crustáceo de antenas largas y espinosas se pesca en las costas de Quintana Roo. ¿Qué es? → La langosta: Watch: what kind of animal is walking across the sea floor here? → Spiny lobster
- mf-823fe66d88: overlap like q-14082: Hör zu: Welcher Vogel singt hier im Garten? → Amsel: Listen: which bird is singing this song? → Common blackbird
- mf-8c57082afd: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: Listen: this was the national anthem of a former country, now gone. Which one? → Netherlands Antilles
- mf-9445f10da6: overlap like q-20717: Listen: this is the national anthem of which country? → Ecuador: Listen: this is the national anthem of which country? → Ecuador
- mf-9cd85c8a53: overlap like q-6225: Bambi is a white-tailed deer. He starts the film as a spotted baby and ends it as the Great Prince of the Forest. What has grown on his head? → Antlers: Watch: the adult males of this animal grow something on their heads. What is it called? → Antlers
- mf-a98d266a68: overlap like q-8733: This fish spends hours out of the water on mangrove shores, hopping along on its fins. What is it called? → Mudskipper: Watch: what is the bug-eyed animal resting on the wet mud in this clip? → Mudskipper
- mf-aa7c112aa3: overlap like q-20834: Watch: what is the name of the big drum that the seated musician is beating for the dancers? → Tapan (davul): Watch: what is the big drum the seated musician is beating for the dancer? → Tapan
- mf-ac6d9642c9: overlap like q-2416: A giant steel arch bridge is nicknamed “the Coathanger”. In which city does it stand? → Sydney: Watch: in which city is this big steel arch bridge? → Sydney
- mf-b06501ca1c: overlap like q-20825: Listen: this slow, solemn theme gave the whole string quartet its nickname. What is the quartet called? → “Death and the Maiden”: Listen: which composer wrote this fast, stormy string quartet movement? → Franz Schubert
- mf-b2884330ab: overlap like q-9691: This bird shrieks over British seaside towns and loves to snatch chips. What kind of bird is it? → A gull: Listen: which bird makes these loud cries? → Gull
- mf-c1842a4c34: hard fail: correct 4, unambiguous 3, no_giveaway 5, no_overlap 5: Listen: which bird makes this rhythmic sound during its display flight over northern bogs? → Jack snipe
- mf-d23d6b0620: overlap like q-8782: Look at this little animal munching on a leaf. What is it called? → A caterpillar: Watch: what is this cook getting ready for lunch, one by one, from the big bowl? → Caterpillars
- mf-dd94fd9e63: overlap like q-20765: Listen: which composer wrote this stormy piano piece? → Frédéric Chopin: Listen: which composer wrote this stormy piano piece? → Frédéric Chopin
- mf-eb5282e942: overlap like q-20723: Listen: which composer wrote this string quartet? → Claude Debussy: Listen: this string quartet movement is by the composer most closely linked with which musical style? → Impressionism
- mf-f08164e59e: overlap like q-20723: Listen: which composer wrote this string quartet? → Claude Debussy: Listen: which composer wrote this lively movement for string quartet? → Claude Debussy
- mf-f2c89b6981: overlap like q-20829: Listen: this melody opened the old anthem of the Kingdom of Yugoslavia. Today it is the national anthem of which country? → Serbia: Listen: this was the national anthem of a European kingdom between the two world wars. Which kingdom? → Kingdom of Yugoslavia
- mf-ffd1a0cdf8: overlap like q-20858: Listen: this national anthem's title means what in English? → “Army March”: Listen: this march, sung by a chorus, is the national anthem of which country? → Vietnam
- mf-15a9b50a6c: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Listen: which Australian bird makes this ringing, bell-like call? → Grey currawong
- mf-2db8ca915d: overlap like q-20843: Listen: who composed the music of this national anthem? → Phra Chenduriyang: Listen: this is the national anthem of which country? → Thailand
- mf-4ca065149a: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Listen: this duet for two high voices and orchestra is one section of a larger work. What kind of work is it? → A Mass
- mf-6b3e011efd: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Watch: this NASA computer model colors the tiny particles that winds carry around the world. What do the blue swirls over the oceans show? → Sea salt
- mf-be62d0d2cd: overlap like q-20521: In 2003, Britain sent a small lander called Beagle 2 to the planet in this photo. Which planet is it? → Mars: Watch: engineers are test-driving this six-wheeled robot explorer. Which planet was it built to explore? → Mars
