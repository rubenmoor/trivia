# batch-76

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, early-britain, middle-ages, twentieth-century, customs-and-ceremonies, legendary-heroes, soaps-and-dramas, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, hills-moors-and-national-parks, birds, tudors-and-stuarts, georgians-and-victorians, parliament-and-prime-ministers, scientists-and-inventors, pioneers-and-heroes, drinks, creatures-ghosts-and-superstitions, pop-and-rock, traditional-music-and-dance, childrens-books-and-comics, art-and-architecture
- Merged: 76 (q-20490…q-20565)
- Approved: 72
- Needs work: 4
- Dropped by the pipeline: 55
- Reviewed by: claude-opus-5-5
- Claude calls: 265, about $32.22 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-74, batch-75; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-74 | batch-75 | batch-76 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 144 | 148 | 131 |
| skipped slots |  | 360 | 356 | 373 |
| dropped |  | 43 | 45 | 55 |
| drop rate | ≤ 20.0 % | 29.9 % ✗ | 30.4 % ✗ | 42.0 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 9 | 11 | 6 |
| dropped: overlap |  | 34 | 33 | 48 |
| dropped: duplicate |  | 0 | 1 | 1 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 101 | 103 | 76 |
| approved |  | 94 | 90 | 72 |
| needs_work |  | 7 | 13 | 4 |
| needs_work rate | ≤ 20.0 % | 6.9 % ✓ | 12.6 % ✓ | 5.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 4.0 % ✓ | 4.9 % ✓ | 2.6 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 1.0 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.0 % ✗ | 2.9 % ✗ | 1.3 % ✗ |
| needs_work: media | ≤ 10.0 % | 5.0 % ✓ | 6.8 % ✓ | 0.0 % ✓ |
| media: no pick in review 1 |  | 6 | 17 | 4 |
| media: recovered by research |  | 3 | 11 | 4 |
| media: no pick at record |  | 5 | 7 | 0 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 25.0 % ✗ | 25.0 % ✗ | 38.2 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 11 | 1 | 0 |
| top move | ≤ 25.0 % | 16.8 % ✓ | 15.5 % ✓ | 18.4 % ✓ |
| values move |  | 15 | 15 | 14 |
| top stimulus |  | 85.1 % | 78.6 % | 81.6 % |
| values stimulus |  | 4 | 4 | 3 |
| top clue | ≤ 60.0 % | 33.7 % ✓ | 39.8 % ✓ | 34.2 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 30.7 % ✓ | 34.0 % ✓ | 27.6 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 22.8 % ✓ | 24.3 % ✓ | 18.4 % ✓ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 14.9 % ✗ | 21.4 % ✓ | 18.4 % ✓ |
| mean fun | ≥ 3.40 | 3.47 ✓ | 3.63 ✓ | 3.50 ✓ |
| cost $ |  | $33.45 | $35.70 | $28.92 |
| $ per approved | ≤ $0.35 | $0.36 ✗ | $0.40 ✗ | $0.40 ✗ |
| calls |  | 243 | 252 | 205 |
| calls per approved |  | 2.59 | 2.80 | 2.85 |
| wall time h |  | 1.21 | 1.23 | 0.96 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 57 (2 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 9 (0 major), fact 1 (0 major), overlap 1 (1 major), media 3 (0 major), difficulty 2 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.30

Major findings on approved questions:

- **q-20561**: overlap — The facts are right: eight English fireships were sent in at night off Calais in 1588 (before Gravelines), they burned no Spanish ship but broke the crescent formation, and the hints and media (French coast near Boulogne) are fine. The problem is overlap. Related q-9805 (also 1588, also "what enemy?", answer The Spanish Armada) tests the same link between 1588 and the Armada, and q-18681 even names "the Armada" in its question text, so seeing either one gives this answer away. (http://127.0.0.1:8001/review/q-20561)

## Needs work

- **q-20544** (money-and-shopping) My signs shout “Everything must go!” and even the shelves, rails and tills have price tags. What sale am I? → A closing-down sale: Hint 1 (“I don't come round on any calendar date.”) already rules out all three wrong answers, because Boxing Day, January and summer sales are all tied to the calendar. Hint 2 (“only once in a shop's whole life”) also gives the answer away. Hint 1 should be a vague hint about the shop or the signs, and hint 2 should not say that the sale only happens once.
- **q-20554** (sayings-and-idioms) Brits praise the “Dunkirk spirit” when people pull together. Dunkirk, where a famous rescue happened in 1940, is in which country? → France: Hint 2 gives the answer away: of the four options, only France has a Mediterranean coast, so it rules out Belgium, the Netherlands and Germany at once. Hint 1 ("just across the Channel from Kent") also points straight to France. Replace hint 2 with something vaguer, such as one about the 1940 evacuation or the town's North Sea beaches, and soften hint 1 so it doesn't name Kent.
- **q-20558** (sayings-and-idioms) A Yorkshire builder says “Where there's muck there's brass”, with brass meaning money. Which of these is NOT British slang for money? → Nosh: This question overlaps with approved q-18919, which asks for the British slang word for money (answer: Dosh). Here Dosh is one of the three money-slang options, so seeing either question gives the other away. Swap Dosh for another money word (e.g. "Quid" isn't usable, but "Readies" or "Spondulicks" would work), or drop this question. Smaller point: the "Yorkshire builder says" setup is close to an invented story. A plain "In Yorkshire they say…" would be cleaner.
- **q-20564** (tudors-and-stuarts) The Groom of the Stool was one of Henry VIII's closest servants, chatted with the king in private and often got very rich. What did he help the king with? → Going to the toilet: Hint 1 says only noblemen got the Groom of the Stool job. That's wrong: under Henry VIII it went to trusted gentlemen of the privy chamber, and many of them were gentry, not nobles (Henry Norris, Anthony Denny). Hint 1 should say instead that the job went to the king's closest companions. Fact check: wrong. Hint 1 says only noblemen got the Groom of the Stool job. It was held by trusted gentlemen of the privy chamber, many of them gentry rather than nobles (e.g. Henry Norris, Anthony Denny).

## Question axes

- move: cause_effect 4, count 2, estimate 2, identify 6, made_of 5, name_concept 14, odd_one_out 6, origin 6, purpose 12, record 1, sequence 4, when 3, who 3, word_meaning 8
- stimulus: detail 1, none 62, photo 13
- clue: completion 6, direct 26, riddle 3, scenario 18, three_facts 23
- answer_kind: group 13, number 5, person 6, place 11, thing 21, time 3, word 17
- lens: body_senses 6, educational_media 10, everyday 12, history 13, language 10, nature 2, pop_culture 14, popular_science 2, school 6, university 1

## Dropped by the pipeline

- accents-and-dialects-4: overlap like q-20220: In Scotland, if a baby is “greetin'”, what is it doing? → Crying: Complete the meaning: in Northern Ireland, a child who's “gurnin'” is… → Crying and moaning
- accents-and-dialects-7: overlap like q-19908: Someone says “wee” for small, “aye” for yes and “loch” for lake. Which country are they most likely from? → Scotland: You look a bit pale and poorly, and someone says you're “peely-wally”. Where are you most likely to be? → Scotland
- accents-and-dialects-8: overlap like q-5628: Irish writer George Bernard Shaw won the 1925 Nobel Prize in Literature. His play “Pygmalion” then made him the first person to also win which award? → An Oscar: I'm an Irish playwright, I won the Nobel Prize, and my play “Pygmalion” turned a Cockney flower girl into a lady. Who am I? → George Bernard Shaw
- accents-and-dialects-11: overlap like q-19455: In “My Fair Lady”, Eliza Doolittle sells flowers in Covent Garden until Professor Higgins teaches her to speak “properly”. Which accent does she start with? → Cockney: In “My Fair Lady”, which professor of phonetics bets he can make Eliza Doolittle speak like a duchess? → Henry Higgins
- accents-and-dialects-16: overlap like q-9683: In the East Midlands, a bread roll is called a “cob”. Which of these is NOT another British word for a bread roll? → Pikelet: Drivers here call a roundabout an “island”, a bread roll is a “cob”, and Spaghetti Junction tangles its motorways. Which region is it? → The Midlands
- birds-6: overlap like q-6702: White storks build huge nests on rooftops in Europe. Each autumn they fly far to the south, and they come back in spring. Where do they spend the winter? → Africa: This little bird sings in British woods all summer. Where does it fly to spend the winter? → Africa
- birds-16: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: An old British legend says a little brown bird fanned a fire to keep a baby warm, and the flames scorched it. Which part of the robin turned red? → Its breast
- childrens-books-and-comics-8: overlap like q-1906: En el quidditch, ¿cuántos aros defiende el guardián de cada equipo? → 3: In Quidditch, each team guards goal hoops like these. How many hoops does each team have? → 3
- childrens-books-and-comics-15: overlap like q-18961: You're reading “Alice's Adventures in Wonderland” at bedtime. Which place will you NOT find in it? → Neverland: Christopher Robin plays with Winnie-the-Pooh and his friends. Which of these places is NOT in their stories? → Neverland
- cities-and-towns-1: overlap like q-5151: Mira de cerca: con este material los artesanos de Ráquira, Boyacá, hacen ollas y figuras. ¿Qué es? → Barro: Stoke-on-Trent, nicknamed “The Potteries”, has made millions of things like this. What are they made from? → Clay
- cities-and-towns-6: overlap like q-19508: Many British seaside towns have one of these, stretching out over the waves with arcades and rides along it. What is it? → A pier: In Southend-on-Sea, it stretches 2.1 km (1.3 miles) into the sea and has its own train. It's the world's longest pleasure… what? → Pier
- cities-and-towns-10: overlap like q-19972: This is an Aberdeen Angus, first bred in Aberdeenshire in Scotland. What kind of animal is it? → A cow: This is an Aberdeen Angus, a famous breed from north-east Scotland. Which animal is it? → Cows
- cities-and-towns-11: overlap like q-19161: Children have ridden these animals on British beaches for more than 100 years. What are they? → Donkeys: For more than 100 years, children at Weston-super-Mare have ridden these long-eared animals along the beach. What are they? → Donkeys
- creatures-ghosts-and-superstitions-5: overlap like q-18624: When old British sailors said something had gone to “Davy Jones's locker”, where was it? → The bottom of the sea: You're on a pirate ship and the captain groans that the treasure has gone to “Davy Jones' Locker”. Where is it? → The bottom of the sea
- customs-and-ceremonies-1: duplicate like q-2461: Look at this shaggy cow with long horns and a fringe over its eyes. Which country does this breed come from? → Scotland: This criss-cross cloth pattern is famous all over the world. Which part of the UK is it most linked to? → Scotland
- customs-and-ceremonies-4: overlap like q-20444: You're at Wimbledon, and every tennis player on court is dressed all in white. Which season is it? → Summer: You're on the pier at Bognor Regis, watching people in homemade wings leap into the sea at the Birdman contest. What season is it? → Summer
- customs-and-ceremonies-5: overlap like q-19310: I'm one of the most powerful ministers in the government. I live at Number 11 Downing Street, and on Budget Day I hold up a red box for the cameras. Who am I? → The Chancellor of the Exchequer: It's red, a bit battered and full of papers. On Budget day, the Chancellor holds it up outside 11 Downing Street. What is it? → A briefcase
- customs-and-ceremonies-9: overlap like q-18208: On Bonfire Night, a stuffed dummy like this one is put on top of the bonfire. Who is it named after? → Guy Fawkes: On Bonfire Night, the town of Lewes holds famous torch parades like this one. Whose failed plot does Bonfire Night remember? → Guy Fawkes
- drinks-8: overlap like cities-and-towns-1: Stoke-on-Trent, nicknamed “The Potteries”, has made millions of things like this. What are they made from? → Clay: Look at the photo: this is a Brown Betty, a classic British teapot. What is it made from? → Clay
- early-britain-9: overlap like q-3509: In an old legend, the boy who pulled a sword like this one out of a stone became king. Who was he? → King Arthur: Legend says the boy who pulled the sword from the stone was born at Tintagel Castle in Cornwall. Who was he? → King Arthur
- football-6: overlap like q-19483: This ship set off on its first and only voyage in April 1912. From which English port did it leave? → Southampton: This south-coast port's club is nicknamed the Saints and plays at St Mary's Stadium, and the Titanic sailed from here. Which city is it? → Southampton
- football-10: overlap like q-19579: Who is this Lioness, who scored the winning goal against Germany in the Euro 2022 final at Wembley? → Chloe Kelly: I came off the bench in the Euro 2025 final, set up England's goal and scored the winning penalty against Spain in the shootout. Who am I? → Chloe Kelly
- football-12: overlap like q-10830: Eine Bundesliga-Dauerkarte gilt für alle Heimspiele der Saison. Wie viele Bundesliga-Heimspiele sind das? → 17: A Premier League season ticket gets you into every home league game. With 20 clubs, how many home league games is that? → 19
- football-16: overlap like q-19485: You're cheering in Celtic Park, home of Celtic and Scotland's biggest club football ground. About how many fans fit inside? → 60,000: It's in Glasgow's East End, holds about 60,000 fans and is Scotland's biggest club ground. What do Celtic fans nickname Celtic Park? → Paradise
- georgians-and-victorians-0: overlap like q-5898: At the start of “Alice's Adventures in Wonderland”, Alice follows a White Rabbit with a pocket watch. Where does she follow him? → Down a rabbit hole: In Lewis Carroll's story, Alice runs after the White Rabbit. What does she fall down next, on her way to Wonderland? → A rabbit hole
- georgians-and-victorians-3: overlap like q-9735: Horatio Nelson stands on top of Nelson's Column. He was an admiral: what did he command? → Warships: You're in Trafalgar Square, looking up at Horatio Nelson on his tall column. He was an admiral. What does an admiral do? → Commands a fleet of warships
- hills-moors-and-national-parks-0: overlap like q-19032: The Uffington White Horse is a giant chalk figure cut into a hillside in Oxfordshire. About how old is it? → About 3,000 years: Salisbury Plain, home of Stonehenge, sits on a soft white rock. White horse figures are cut into it, and teachers once wrote with it. What is it? → Chalk
- hills-moors-and-national-parks-7: overlap like q-2699: This curved concrete bridge in Scotland was built for one kind of traffic. Which one? → Trains: Look at the photo: this long stone bridge, the Ribblehead Viaduct, crosses a valley in the Yorkshire Dales. What was it built to carry? → Trains
- hills-moors-and-national-parks-10: overlap like q-19908: Someone says “wee” for small, “aye” for yes and “loch” for lake. Which country are they most likely from? → Scotland: A brae is a steep hillside, a loch is a lake and a glen is a narrow valley. Which part of the UK do these words come from? → Scotland
- languages-of-britain-8: overlap like q-2569: Many deaf people talk in a language like this one. What is it made of? → Hand signs and facial expressions: You're choosing GCSEs in England, and a new option is a language with no sounds, used with your hands and face. What is it? → British Sign Language
- languages-of-britain-12: overlap like q-18425: Complete the meaning: when someone in Belfast says “Bout ye?”, they're asking… → How are you?: In Scottish Gaelic you might hear “Ciamar a tha thu?” when you meet someone. A happy reply is “Tha gu math”, “I'm well”. What's the question? → How are you?
- languages-of-britain-16: overlap like q-17861: On CBeebies, Mr Tumble talks with his voice and also with what? → Hand signs: This CBeebies star uses Makaton, a way of talking with signs and symbols, as which spotty-faced character? → Mr Tumble
- legendary-heroes-9: overlap like q-6322: In medieval Europe, riders in armor charged at each other with long lances in contests like this. Who were they? → Knights: Sir Bedivere wore armour, rode into battle on horseback and served King Arthur. What was he? → A knight
- middle-ages-6: overlap like q-9580: Westminster Abbey, January 1066: Harold Godwinson is crowned king. Who was crowned there next, on Christmas Day that same year? → William the Conqueror: King William Rufus built this great hall in London. His father was the king who conquered England in 1066. Who was he? → William the Conqueror
- middle-ages-9: overlap like q-18483: In 1066, near Hastings, English foot soldiers stood behind a wall of shields. Which army charged them with knights on horses and archers? → The Normans: In 1066, a duke from Normandy sailed to England and beat its king in a battle near the south coast. Which battle? → The Battle of Hastings
- middle-ages-10: overlap like q-18232: Each year a poet wins a carved chair like this one at a big festival of music and poetry that moves to a new town every summer. Which country holds it? → Wales: The first famous Eisteddfod was held at Cardigan Castle in 1176, and Welsh children still compete in one every year. What is it? → A festival of music and poetry
- middle-ages-11: overlap like q-9616: In 1917 the royal family took its surname from this castle. What is it called? → Windsor Castle: King Edward III was born in this castle in 1312 and later rebuilt it as a grand palace. Which castle is it? → Windsor Castle
- money-and-shopping-13: overlap like q-18495: It's on every British coin, on Royal Mail stamps and on Bank of England notes. Whose head is it? → The king or queen's: You buy a stamp at the Post Office. Whose head is always shown on Royal Mail stamps? → The King or Queen
- parliament-and-prime-ministers-11: overlap like q-19310: I'm one of the most powerful ministers in the government. I live at Number 11 Downing Street, and on Budget Day I hold up a red box for the cameras. Who am I? → The Chancellor of the Exchequer: The Prime Minister lives at number 10 Downing Street. The Chancellor lives right next door. At what number? → Number 11
- parliament-and-prime-ministers-17: overlap like q-18688: Britain's NHS began in 1948, it's paid for out of taxes, and it's free when you use it. What does it give people? → Free doctors and hospitals: A law created me in 1946, and I opened my doors in 1948. My doctors and hospitals are free for everyone in the UK. What am I? → The NHS
- pioneers-and-heroes-16: overlap like q-0019: ¿Cuál es la montaña más alta del mundo? → El monte Everest: In the 1920s, George Mallory tried to be the first person to climb the highest mountain in the world. Which mountain was it? → Mount Everest
- art-and-architecture-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: William Morris's famous wallpapers of flowers and birds were printed by hand, one colour at a time, using carved blocks of what? → Wood
- art-and-architecture-11: overlap like q-18281: Tracey Emin's “My Bed” was shortlisted for the Turner Prize in 1999 and later sold for over £2 million. What is it? → Her own unmade bed and the mess around it: The Turner Prize started in 1984 and is handed out every year. Who can win it? → British artists
- languages-of-britain-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: The BBC programme “See Hear” has been on TV since 1981. Who is it mainly made for? → Deaf people
- parliament-and-prime-ministers-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In the House of Commons, ordinary MPs with no job as a minister sit on the seats behind their leaders. What are they called? → Backbenchers
- traditional-music-and-dance-3: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Many morris teams have a “fool” who runs around among the dancers. What is the fool's main job? → Making the crowd laugh
- tudors-and-stuarts-8: overlap like q-19065: Richard III died at the Battle of Bosworth in 1485. In 2012, his skeleton was found under a car park in which city? → Leicester: In 2012, the lost bones of King Richard III were dug up in Leicester. What were they found under? → A car park
- sayings-and-idioms-1: overlap like q-19329: In Cockney rhyming slang, “apples and pears” means stairs. What does “pork pies” mean? → Lies: Cockney rhyming slang turned me from a meaty snack into a word for fibs. If a parent says you're telling me, they think you're lying. What am I? → Porkies
- sayings-and-idioms-5: overlap like q-12771: Ben Franklin printed the saying “Early to bed and early to rise makes a man healthy, wealthy, and…” How does it end? → Wise: Complete the old saying: “Early to bed and early to rise makes a man healthy, wealthy and…” → Wise
- sayings-and-idioms-15: overlap like q-19020: As Home Secretary, I set up London's Metropolitan Police in 1829. Officers are still called “bobbies” after my first name. Who am I? → Robert Peel: You ask a British bobby for directions. That nickname comes from which man, who set up London's police in 1829? → Robert Peel
- scientists-and-inventors-14: overlap like q-2321: Drivers see me on dark roads, and I'm named after the way a cat's eyes look at night. People call me a “cat's eye”. What am I? → A road reflector: Percy Shaw from Halifax invented these little road studs in 1934. Who are they there to help? → Drivers at night
- traditional-music-and-dance-16: overlap like q-7596: Escucha: ¿qué instrumento es este? → El acordeón: Listen: this is the instrument Scottish dance-band star Jimmy Shand played. What is it? → An accordion
- tudors-and-stuarts-5: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: On the freezing morning of 30 January 1649, Charles I wore extra shirts so the crowd wouldn't see him shiver and think he was scared. How many shirts did he wear? → 2
- tudors-and-stuarts-7: overlap like q-17880: The guards who wear this red-and-gold uniform have a famous nickname. What is it? → Beefeaters: Guards at the Tower of London wear this famous uniform. What are they nicknamed? → Beefeaters
- twentieth-century-11: overlap like q-5661: In 1969, a famous band walked across this London street crossing for an album cover. Which band was it? → The Beatles: These black-and-white stripes on Abbey Road in London are on a 1969 Beatles album cover, and fans come from all over the world to copy the photo. What are they really for? → Helping people cross the road
