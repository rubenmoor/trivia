# batch-79

Made by `qgen batch --media-first` on 2026-11-16 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 82 (q-20647…q-20728)
- Approved: 64
- Needs work: 18
- Dropped by the pipeline: 30
- Reviewed by: claude-opus-5-5
- Claude calls: 1002, about $84.83 at list price; $1.33 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-77, batch-78; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-77 | batch-78 | batch-79 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | media-first | media-first |
| drafts |  | 125 | 17 | 112 |
| skipped slots |  | 379 | 0 | 0 |
| dropped |  | 57 | 4 | 30 |
| drop rate | ≤ 20.0 % | 45.6 % ✗ | 23.5 % ✗ | 26.8 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 1 |
| dropped: hard fail unambiguous |  | 0 | 0 | 2 |
| dropped: hard fail no_giveaway |  | 11 | 1 | 5 |
| dropped: overlap |  | 46 | 3 | 23 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 68 | 13 | 82 |
| approved |  | 65 | 8 | 64 |
| needs_work |  | 3 | 5 | 18 |
| needs_work rate | ≤ 20.0 % | 4.4 % ✓ | 38.5 % ✗ | 22.0 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 38.5 % ✗ | 4.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 1.2 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 1.2 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.9 % ✗ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 1.5 % ✓ | 15.4 % ✗ | 17.1 % ✗ |
| media: no pick in review 1 |  | 7 | 1 | 2 |
| media: recovered by research |  | 6 | 0 | 0 |
| media: no pick at record |  | 1 | 13 | 82 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 1.2 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 38.4 % ✗ | 17.6 % ✓ | 20.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 2 | 6 | 39 |
| top move | ≤ 25.0 % | 13.2 % ✓ | n/a | n/a |
| values move |  | 13 | n/a | n/a |
| top stimulus |  | 88.2 % | n/a | n/a |
| values stimulus |  | 3 | n/a | n/a |
| top clue | ≤ 60.0 % | 36.8 % ✓ | n/a | n/a |
| values clue |  | 5 | n/a | n/a |
| top answer_kind | ≤ 40.0 % | 23.5 % ✓ | n/a | n/a |
| values answer_kind |  | 7 | n/a | n/a |
| top lens | ≤ 25.0 % | 22.1 % ✓ | n/a | n/a |
| values lens |  | 11 | n/a | n/a |
| giveaway-step drop rate |  | n/a | 0.0 % ✓ | 0.0 % ✓ |
| mechanical-check rate |  | n/a | 0.0 % ✓ | 3.7 % ✓ |
| media share | 15.0 %–50.0 % | 11.8 % ✗ | n/a | n/a |
| mean fun | ≥ 3.40 | 3.47 ✓ | 3.47 ✓ | 3.46 ✓ |
| cost $ |  | $25.19 | $12.37 | $80.81 |
| $ per approved | ≤ $0.35 | $0.39 ✗ | $1.55 ✗ | $1.26 ✗ |
| calls |  | 178 | 130 | 942 |
| calls per approved |  | 2.74 | 16.25 | 14.72 |
| wall time h |  | 0.86 | 0.90 | 2.75 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 3 of 47 (6 %)
- Major among review needs work: 7 of 13 (54 %)
- Problems by kind: giveaway 10 (3 major), fact 3 (1 major), overlap 1 (0 major), media 11 (8 major), difficulty 8 (5 major), other 1 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 3 of 60 (5 %)
- Audit/review agreement (both accept or both not): 51 of 60 (85 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.02

Major findings on approved questions:

- **q-20647**: giveaway — The description gives the answer away. "A puzzle picture" plus "didn't even try to solve the cube" is a pun on Cubism, which points straight to Picasso. That leaves one of the four options without the clip. The facts check out: the 2016 Scientific Reports study (Simpson et al., "Coral reef fish perceive lightness illusions") used Picasso triggerfish (Rhinecanthus aculeatus), and the hints and fun fact are correct. The title-word flag ("fish", "reef") is false. Caveat: I had no tool to open the frame sheet or spectrogram, so I couldn't confirm the fish is clear enough on screen to identify. (http://127.0.0.1:8001/review/q-20647)
- **q-20674**: media, difficulty — Media-first check 1 fails. Almost no player can tell the instrumental Uzbek anthem by ear from those of Turkmenistan, Kyrgyzstan or Mongolia, so the clip doesn't decide the answer and the question becomes a pure guess until the hints come (house style: something nobody can know or work out is not a 15, it is a bad question). I couldn't open the spectrogram because no file-reading tool was available here. The loudness numbers (−16.1 LUFS, no silence) look fine. The facts I checked hold: Tashkent is Central Asia's largest city, and the melody is Burhanov's from 1947, with new words in 1992. The "anthem/national" title-word flag is a false alarm. (http://127.0.0.1:8001/review/q-20674)
- **q-20701**: fact, media — Nothing in the file's Commons text supports the answer. The description only says "Cloud time-lapse footage… 125x normal speed", and the only category is "Time-lapse videos of clouds", with no cumulus category and no place named (check 3). I also had no tool to open the frame sheet, so I couldn't confirm that the window shows clear, separate fair-weather cumulus rather than stratocumulus or mixed cloud. Someone needs to look at the frames before this is played. The fun fact (about 500 t ≈ 1.1 million lb ≈ 100 elephants), the hints and the wrong options are fine, and q-2907 (what "cirrus" means) and q-4977 (what clouds are made of) don't overlap with this question. The "cloud" title-word flag is false: the word doesn't give away the type. (http://127.0.0.1:8001/review/q-20701)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 20 | 3 | 3 | 3 | 0 | 0 |
| cat:Audio files of national anthems | 30 | 8 | 8 | 8 | 7 | 1 |
| cat:Birds calling | 6 | 0 | 0 | 0 | 0 | 0 |
| cat:Speeches by speaker | 9 | 1 | 1 | 1 | 1 | 0 |
| cat:Videos by NASA | 30 | 3 | 3 | 3 | 3 | 3 |
| cat:Videos of animals | 30 | 11 | 11 | 11 | 6 | 6 |
| q:audio:classical music recording symphony | 30 | 3 | 3 | 3 | 3 | 3 |
| q:audio:frog call | 24 | 2 | 2 | 2 | 0 | 0 |
| q:audio:national anthem instrumental | 30 | 17 | 17 | 17 | 16 | 10 |
| q:audio:opera aria recording | 16 | 12 | 12 | 12 | 9 | 8 |
| q:audio:piano recording | 30 | 6 | 6 | 6 | 4 | 3 |
| q:audio:ship horn | 2 | 1 | 1 | 1 | 1 | 1 |
| q:audio:violin cello recording | 30 | 6 | 6 | 6 | 4 | 4 |
| q:video:NASA video launch | 30 | 5 | 5 | 5 | 4 | 3 |
| q:video:animal video wildlife | 26 | 6 | 6 | 6 | 4 | 4 |
| q:video:city timelapse video | 30 | 9 | 9 | 5 | 4 | 4 |
| q:video:rover mars video | 30 | 5 | 5 | 3 | 2 | 2 |
| q:video:space station astronaut video | 30 | 3 | 3 | 2 | 2 | 2 |
| q:video:time-lapse video | 27 | 7 | 7 | 6 | 4 | 3 |
| q:video:traditional dance video | 30 | 6 | 6 | 5 | 4 | 4 |
| q:video:train video | 30 | 6 | 6 | 6 | 3 | 2 |
| q:video:volcano eruption video | 30 | 1 | 1 | 1 | 1 | 1 |
| total | 550 | 121 | 121 | 112 | 82 | 64 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 444 | 81 | 81 | 72 | 47 | 42 |
| pd-music | 106 | 40 | 40 | 40 | 35 | 22 |
| total | 550 | 121 | 121 | 112 | 82 | 64 |

- $ per approved: $1.33

## Needs work

- **q-20648** (countries) Listen: this is the national anthem of which Pacific island country? → Solomon Islands: Almost nobody can recognize the Solomon Islands anthem by ear or tell it apart from the anthems of Fiji, Vanuatu or Papua New Guinea, so the clip can't decide the answer. Without the hints the question is a pure guess, and hint 2 (“a wise and very rich king from the Bible”) is what actually gives the answer. No other question about this window would work for players, so the file doesn't fit a question.
- **q-20650** (countries) Listen: this instrumental piece was once the national anthem of which country? → Iran: The kept file fails the licence check. Its public-domain basis is only that Iran has no copyright treaties, which is none of the accepted bases (creator dead 70+ years, pre-1930 film, government work, traditional), and the 1980 anthem's composer may still be alive. The clip also doesn't fit as a question: almost no player can recognize a short-lived 1980–1990 instrumental anthem by ear, so only the hints answer it. Media.work basis “Iranian work; Iran has no copyright treaties with most countries, so Commons hosts it as public domain” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-20651** (countries) Listen: this tune was once the national anthem of which African country? → Rwanda: The clip doesn't help answer the question. Hardly anyone can recognise Rwanda's 1962–2001 instrumental anthem, or tell it apart from the anthems of Burundi, Uganda or Tanzania, so the question can only be answered from the hints (the rater said the same). The window has no other feature players could identify, so it can't be fixed by rewording: the file isn't usable for this question. Two smaller points: hint 1 also fits Burundi (Kirundi), and Uganda's Mgahinga park, part of the same Virunga volcanoes, also has mountain gorillas, so hint 2 isn't unique to Rwanda.
- **q-20653** (countries) Listen: this is the national anthem of a Caribbean island nation. Which country is it? → Grenada: Players can't tell Grenada's anthem from the other three options by ear. Barbados, Saint Lucia and Dominica all have similar brass-band anthems from the 1960s and 70s, so the clip does no work. The question is answered only by reading the hints (independence in 1974, nutmeg on the flag, "Island of Spice"), so it's hard because the anthem is obscure, not because it takes knowledge. No other question about this window would be both fair and worth asking, so the file doesn't fit this format.
- **q-20659** (countries) Listen: this is the national anthem of which Central American country? → El Salvador: Players can't tell El Salvador's anthem apart from the anthems of Honduras, Guatemala and Costa Rica by ear. All four are 19th-century band anthems in a similar style, so the clip doesn't decide the answer. Only hint 3 does, which makes this a bad "nobody could know" question rather than a fair 15. No other question about this window (an instrumental anthem played by a military band) would work for this file. Smaller issues, if it is ever reworked: hint 1 fits all four options because they all have Pacific coasts, and the fun fact's "about four and a half minutes" goes beyond the sources, which say "more than four minutes".
- **q-20663** (british-royals) Listen: a young woman gives a radio speech to millions of listeners around the world. Whose voice is this? → Queen Elizabeth II: The text answers the question without the clip. The description's "back when radios were the size of a cupboard" places the voice around the 1930s–50s, which rules out Princess Diana. Radio already rules out Queen Victoria. "A young woman gives a radio speech to millions of listeners around the world" then leaves only Elizabeth II, because Thatcher never gave a worldwide broadcast as a young woman. The description should play on the theme without dating the recording. The question should leave the decision to the voice, for example with distractors who were young women on air in the same era.
- **q-20671** (countries) Listen: this is the national anthem of which country? → Kyrgyzstan: Almost nobody can tell the Kyrgyz anthem apart from the anthems of Kazakhstan, Uzbekistan and Tajikistan by ear, so the clip doesn't help answer the question. The hints (the flag's 40-ray sun, Issyk-Kul) do all the work, which fails media-first check 1. No other question about this instrumental window would be fair for players, so the file doesn't fit. Separately, code raised a hard flag on the licence basis ("official state symbol"). That flag is a false alarm: national anthems are an accepted basis. Media.work basis “official state symbol, not protected by copyright under Kyrgyz law” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-20677** (world-music) Listen: this is the national anthem of which Gulf country? → Kuwait: Players can't tell Kuwait's anthem apart from the anthems of Qatar, Bahrain and Oman by ear. All four are brass-band marches from the same region, so the clip can't decide the question and players are left to guess or rely on the hints. No other question about this window would work for the players without becoming trivial (for example "is this a national anthem?"), so the file doesn't fit this slot.
- **q-20678** (trains) Watch: this bright green double-decker express was built to link a European capital’s center nonstop with its airport. Which city? → Vienna: Hint 2 (waltzes, coffee houses, grand palaces) clearly gives away Vienna, and hints 1 and 2 must not do that. Calling it a "European capital" also rules out two options from the text alone: Zurich is not a national capital, and Munich is only a state capital. Prague then stands as the only real alternative. Make hint 2 vaguer (for example, the country's language, or that the city lies on a big river without naming it). Either drop "capital" or swap Zurich and Munich for capitals such as Budapest and Warsaw.
- **q-20681** (countries) Listen: this is a country's national anthem. Which country is it? → Egypt: Players can't answer this from the clip. Egypt's anthem is an instrumental, Western-style march, and almost no one outside the Arab world can tell it apart by ear from the anthems of Morocco, Saudi Arabia or Iraq. The rater agrees: the question is only solved through hints 2 and 3, not by listening. I see no other question about this 52-second window that players could answer by listening, so the file doesn't fit an ear question at difficulty 12.
- **q-20688** (plants) Watch this time-lapse: what kind of plant is blooming here? → A cactus: A video file named .ogg ships as audio; the game can't play it.
- **q-20689** (classical-music) Listen: which American composer wrote this piece, which opens with a famous slide up on the clarinet? → George Gershwin: The picked picture has an unsuitable licence (pd-us-only: PD-US, PD-US-expired, PD-US-record-expired).
- **q-20702** (space) Watch: this NASA science balloon is lifting a telescope. Why does it look so baggy and half-empty at launch? → Its gas will expand as the air pressure drops higher up: The question text describes exactly what the clip shows ("baggy and half-empty"), so players can answer from the text alone and the video isn't needed. Move that clue into the clip: ask something like "Watch: this NASA science balloon is lifting a telescope. Why is it only partly filled at launch?" or "Why is it shaped like this at launch?", so that players have to look at the balloon's shape.
- **q-20708** (classical-music) Listen: this soprano aria, on a record from 1910, comes from which Italian opera? → Lucia di Lammermoor: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-20710** (countries) Listen: this is a former national anthem, no longer in use. Which country did it belong to? → Iraq: Players can't recognise a former anthem that was in use 1981–2003 from a 50-second instrumental band recording, so the clip can't tell Iraq from Libya, Iran or Egypt. Only the hints make it answerable, and hint 2 (“Land of the Two Rivers”, meaning Mesopotamia) nearly gives Iraq away. No other question about this window would work for the players (it is a generic brass-band march), so the file doesn't suit a question.
- **q-20712** (countries) Listen: this is the national anthem of a Caribbean island in the Kingdom of the Netherlands. Which island? → Curaçao: The clip can't decide the answer. Almost no player, even an expert, can tell Curaçao's instrumental anthem apart from those of Aruba, Bonaire or Sint Maarten, which are similar island anthems. So the answer comes only from the hints, and hint 3 (Willemstad, Blue Curaçao) gives it away. The window is an instrumental anthem with nothing else in it a player could identify, so no other question about it would work. Also, Sint Maarten is only part of an island, so it doesn't fit "Which island?" well.
- **q-20717** (world-music) Listen: this is the national anthem of which country? → Ecuador: Players can't answer from the window. Ecuador's anthem is a 19th-century Italian-opera-style march, like the anthems of Colombia, Peru and Venezuela, and almost nobody can tell them apart by ear, not even trivia specialists. So the clip doesn't decide the question and only the hints solve it. No other question about this instrumental window works and still asks about Ecuador, so the file doesn't fit as an essential clip for this question.
- **q-20718** (countries) Listen: this national anthem has no official lyrics. Which country’s anthem is it? → Kosovo: The only clue in the question, an anthem with no official lyrics, fits three of the four options: Bosnia and Herzegovina ("Intermezzo"), San Marino and Spain ("Marcha Real") also have no official words. The question therefore has four defensible answers, and only hint 3 points to Kosovo. Hardly any player could tell Kosovo's anthem from these three by ear, so the clip doesn't settle it. To fix it, swap the wrong answers for young European countries whose anthems have words (for example Montenegro, North Macedonia or Slovenia), or add a clue that only Kosovo has, such as the anthem's title “Europe” (that clue makes it much easier). Fact check: wrong. The question says the anthem has no official lyrics, but that is also true of three of the wrong answers: Bosnia and Herzegovina (Intermezzo), San Marino and Spain (Marcha Real). Several options are therefore correct, and only the hints point to Kosovo.

## Question axes

- move: None 82
- stimulus: None 82
- clue: None 82
- answer_kind: None 82
- lens: None 82

## Dropped by the pipeline

- mf-16abed143d: overlap like q-2309: This bridge, guarded by dragon statues, stands in which European capital? → Ljubljana: Watch: which European capital city is shown in this time-lapse? → Ljubljana
- mf-356bddb5d5: overlap like q-20634: Listen: who composed this lively piece with its racing flute melody? → Johann Sebastian Bach: Listen: which composer wrote this lively concerto for violin, two flutes and strings? → Johann Sebastian Bach
- mf-37f8c35dee: overlap like q-20186: On a hot day, a tune like “Greensleeves” plays in the street and children run out with coins. What has just arrived? → An ice cream van: Listen: which famous old folk tune is being played on the piano? → Greensleeves
- mf-413fafb29d: overlap like q-13884: Which city's name is part of the name of this orange-and-black songbird? → Baltimore: Watch: what is the name of the orange-and-black bird feeding in the pink blossoms? → Baltimore oriole
- mf-5816ffa213: overlap like q-0057: ¿Cómo se llama la galaxia en la que vivimos? → La Vía Láctea: Watch: what is the glowing band stretching across this night sky called? → The Milky Way
- mf-67fdd39501: overlap like q-20658: Watch: this small flying machine was filmed by a rover on Mars. What is its name? → Ingenuity: Watch: on which planet is this spacecraft landing? → Mars
- mf-6fa2eacb17: overlap like q-20672: Listen: which country's national anthem is this? → Russia: Listen: this was the national anthem of which country, which no longer exists? → Soviet Union
- mf-7d1b9cfcdb: overlap like q-17599: Scott Joplin, who wrote “The Entertainer,” is the most famous composer of which piano style, and was called its “King”? → Ragtime: Listen: which composer wrote this piano piece and recorded it himself on a piano roll? → Scott Joplin
- mf-8d71c18996: overlap like q-3311: What are these huge metal boxes stacked at the port called? → Shipping containers: Watch: what is this long freight train carrying, stacked two high? → Shipping containers
- mf-940b7c411e: overlap like q-2416: A giant steel arch bridge is nicknamed “the Coathanger”. In which city does it stand? → Sydney: Watch: in which city is this harbor with its big steel arch bridge? → Sydney
- mf-98cf9a6ac8: overlap like q-17599: Scott Joplin, who wrote “The Entertainer,” is the most famous composer of which piano style, and was called its “King”? → Ragtime: Listen: what style of piano music is this? → Ragtime
- mf-9bca227c20: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Listen: which animals is this children's counting song about? → Frogs
- mf-9c8b7877c6: overlap like q-20676: Listen: this famous aria, sung here in Ukrainian, comes from which Mozart opera? → The Marriage of Figaro: Listen: this soprano aria is sung here in a translation. Which composer wrote it? → Wolfgang Amadeus Mozart
- mf-9d1066d6e9: overlap like q-14077: Er ist lang und rosa, hat keine Beine, lockert die Gartenerde und kriecht nach einem Schauer aus dem Boden. Wie heißt er? → Regenwurm: Watch: which animal is crawling across this rock? → Earthworm
- mf-a5b373df0e: overlap like q-20090: You see birds like this on almost every park pond in Britain. What kind of bird is it? → A duck: Listen: which bird makes this sound? → Duck
- mf-a87f4e40bf: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Watch: this white high-speed train with a red stripe is pulling into a station. In which country is it mainly used? → Germany
- mf-aa43c3511d: overlap like q-20685: Listen: which composer wrote this stormy string quartet music? → Franz Schubert: Listen: this is the end of the first movement of a famous string quartet. Which nickname does this quartet have? → Death and the Maiden
- mf-b58c154cd1: overlap like q-20667: Listen: this soprano prayer comes from an opera by Giuseppe Verdi. Which opera? → La forza del destino: Listen: which composer wrote this dramatic opera scene for soprano and orchestra? → Giuseppe Verdi
- mf-bba08caeb6: overlap like q-13256: Mira la foto: ¿qué animal del mar es este, que a veces pica a los bañistas en verano? → Una medusa: Watch: which sea animal is floating around in this aquarium tank? → Jellyfish
- mf-bdab247276: overlap like q-12158: Sie war über 110 Meter hoch, schickte 1969 Apollo 11 zum Mond und entstand unter Wernher von Braun. Welche Rakete war es? → Saturn V: Watch: this slow-motion film was shot from the launch tower as a giant rocket’s engines lit up. Which rocket is it? → Saturn V
- mf-d3e96526cd: overlap like q-17592: When danger comes, I flop over, shut my eyes and pretend to be dead until it goes away. Americans say kids who fake being asleep are copying me. Who am I? → The opossum: Watch: which animal is searching for food among the fallen leaves? → Opossum
- mf-dcd37af350: overlap like q-14082: Hör zu: Welcher Vogel singt hier im Garten? → Amsel: Listen: which bird is singing in this recording? → Eurasian blackbird
- mf-f159d5eec1: overlap like q-6743: Look at this close-up of a pet bird. Which bird is it? → Budgerigar: Listen: which small pet bird, often kept in a cage at home, is making these chirps? → Budgerigar
- mf-f579b79826: overlap like q-5276: I grow up underground for years, then climb a tree and leave my empty skin behind. In summer, the males sing very loudly. What am I? → A cicada: Watch and listen: which insect is making this loud buzzing song on the branch? → Cicada
- mf-fff93637f0: overlap like q-20639: Listen: which Italian opera composer wrote this soprano aria? → Giacomo Puccini: Listen: which composer wrote this love duet from an opera? → Giacomo Puccini
- mf-0142cf709f: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Watch: which high-speed train is pulling into this station? → ICE
- mf-231e8d97df: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Watch: which insect is this, resting on a trash can lid and then on a garden rail? → Green bottle fly
- mf-95b6be540e: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Listen: this is the national anthem of which country? → Serbia
- mf-d27ce54701: hard fail: correct 3, unambiguous 3, no_giveaway 4, no_overlap 5: Watch: what is the name of this traditional dance? → Bakisimba
- mf-ec460003ac: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 4: Watch: which animal is this? → Crayfish
