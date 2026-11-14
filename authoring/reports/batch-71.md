# batch-71

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, landmarks-and-castles, early-britain, middle-ages, twentieth-century, regional-specialities, customs-and-ceremonies, legendary-heroes, pop-and-rock, traditional-music-and-dance, soaps-and-dramas, game-shows-and-presenters, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, team-gb-and-olympians, sporting-events, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, transport, crown-and-state, london, counties-and-regions, hills-moors-and-national-parks, wildlife
- Merged: 122 (q-19969…q-20090)
- Approved: 113
- Needs work: 9
- Dropped by the pipeline: 53
- Reviewed by: claude-opus-5-5
- Claude calls: 343, about $42.31 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-69, batch-70; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-69 | batch-70 | batch-71 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 264 | 191 | 175 |
| skipped slots |  | 240 | 313 | 329 |
| dropped |  | 77 | 68 | 53 |
| drop rate | ≤ 20.0 % | 29.2 % ✗ | 35.6 % ✗ | 30.3 % ✗ |
| dropped: hard fail correct |  | 1 | 2 | 1 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 8 | 12 | 11 |
| dropped: overlap |  | 64 | 50 | 40 |
| dropped: duplicate |  | 2 | 3 | 0 |
| dropped: fact-check wrong |  | 2 | 1 | 1 |
| merged |  | 187 | 123 | 122 |
| approved |  | 175 | 111 | 113 |
| needs_work |  | 12 | 12 | 9 |
| needs_work rate | ≤ 20.0 % | 6.4 % ✓ | 9.8 % ✓ | 7.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.1 % ✓ | 4.1 % ✓ | 4.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.1 % ✓ | 1.6 % ✓ | 0.8 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.6 % ✗ | 1.6 % ✗ | 1.6 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.7 % ✓ | 3.3 % ✓ | 3.3 % ✓ |
| media: no pick in review 1 |  | 19 | 12 | 15 |
| media: recovered by research |  | 15 | 10 | 12 |
| media: no pick at record |  | 5 | 2 | 3 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 26.1 % ✗ | 28.8 % ✗ | 24.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 64.1 % ✓ | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | 1.80 ✗ | n/a | n/a |
| approved 11–15 |  | 35 | 7 | 8 |
| top move | ≤ 25.0 % | 17.1 % ✓ | 14.6 % ✓ | 17.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 80.2 % | 82.9 % | 80.3 % |
| values stimulus |  | 5 | 5 | 3 |
| top clue | ≤ 60.0 % | 40.1 % ✓ | 41.5 % ✓ | 43.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.1 % ✓ | 26.0 % ✓ | 26.2 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 21.9 % ✓ | 18.7 % ✓ | 18.9 % ✓ |
| values lens |  | 10 | 9 | 8 |
| media share | 15.0 %–50.0 % | 19.8 % ✓ | 17.1 % ✓ | 19.7 % ✓ |
| mean fun | ≥ 3.40 | 3.48 ✓ | 3.43 ✓ | 3.44 ✓ |
| cost $ |  | $53.36 | $40.51 | $39.18 |
| $ per approved | ≤ $0.35 | $0.30 ✓ | $0.36 ✗ | $0.35 ✓ |
| calls |  | 381 | 287 | 283 |
| calls per approved |  | 2.18 | 2.59 | 2.50 |
| wall time h |  | 1.81 | 1.22 | 1.15 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 8 (0 major), ambiguity 1 (1 major), overlap 2 (0 major), media 6 (2 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.13

Major findings on approved questions:

None.

## Needs work

- **q-19977** (crown-and-state) In 2017, this 12-sided coin replaced an old round one in the UK. How much is it worth? → One pound: None of the candidates shows the heads side of the 12-sided £1 coin. #5 is the old round 1983 pound, which is the coin the question says was replaced. #6 is a close-up of the 12-sided coin, but its micro-lettering reads "ONE POUND", which gives the answer away. A new search is not allowed, so the slot needs a hand-picked image of the 12-sided coin's obverse with no "ONE POUND" text. No suitable picture found for this question.
- **q-19978** (crown-and-state) This is the King's flag, the Royal Standard. One of its lions, standing on its back legs, is Scotland's. How many lions are there in total? → 7: None of the candidates shows the current Royal Standard, so the essential image can't be filled, and no new search is allowed. The slot needs a clear image of the Royal Standard as flown in England (three gold lions in two quarters, Scotland's red lion, Irish harp), e.g. "Royal Standard of the United Kingdom". Separately, the fun fact repeats the answer of q-19916 (the flag flies only when the King is in residence), so seeing this question gives that one away. Consider a different fun fact. No suitable picture found for this question.
- **q-19980** (customs-and-ceremonies) Tennis fans join the famous Queue at Wimbledon to get tickets on the day. When do many of them arrive? → The night before: Hint 2 ("Some of them bring tents.") gives the answer away. Of the four options, only "The night before" would ever need a tent, so the hint solves the question one step early. Hint 2 needs replacing with something weaker, such as how long the line can get or that fans come from all over the world. The rest checks out, and candidate 1 is a good illustrative picture.
- **q-20017** (london) Chelsea FC play at Stamford Bridge, their fans sing “Blue is the Colour”, and Arsenal are local rivals. Which city are they from? → London: This overlaps with q-9636 (London subcategory, approved). Its question text says Chelsea is a "London district" that gives its name to a Premier League club, so seeing either question gives away the other. Separately, hint 2 ("It's the capital of the UK") gives the answer away outright, and only hint 3 is allowed to come that close.
- **q-20049** (rugby-and-cricket) In 2000, one country joined rugby's Five Nations, turning it into the Six Nations. Which country? → Italy: Approved question q-18619 (same subcategory) begins “Apart from Italy, which Six Nations team…”. That tells players Italy is a Six Nations team, and since none of Argentina, Georgia or Spain is, it gives this answer away. Separately, hint 2 (“Its home matches are played in Rome”) as good as names Italy. If the overlap is accepted, hint 2 should be made vaguer, for example a hint about the team's blue shirts or that it often finished bottom in its early years.
- **q-20061** (sayings-and-idioms) Brits stuck on a hard question say “I'm stumped!” Cricket has three stumps at each end. And in a wood, what is a stump? → What's left of a chopped-down tree: Hint 2 (“It's often what's left after someone uses an axe or a saw”) basically repeats the answer (“What's left of a chopped-down tree”), so hint 2 gives it away. Rewrite hint 2 so it stays vaguer, for example: “Woodpeckers and mushrooms love them.” Media is fine: candidate 1 (three cricket stumps, no tree stump in shot).
- **q-20065** (sayings-and-idioms) When someone looks lost in a daydream, Brits ask “A … for your thoughts?” Which coin is offered in this very old saying? → A penny: The fun fact says the saying is "nearly 500 years old". It was first recorded in 1522, so it is now just over 500 years old. Change it to "about 500 years old" or "more than 500 years old". Hint 2 ("the British coin worth the least") also gives the answer away, and it repeats the main clue of q-18802 almost word for word. Swap it for a vaguer hint, for example that the coin is copper-coloured.
- **q-20081** (transport) London's transport map splits the city into numbered rings like these. What are they for? → Working out your ticket price: The question says "numbered rings like these", so the image is essential and must show a London fare-zone map, but none of the candidates does. No new search is possible. Search Commons for something like "London fare zones map" or "Tube zone map" and check that no prices are shown. No suitable picture found for this question.
- **q-20082** (twentieth-century) Scottish inventor John Logie Baird showed off the first working television in London. When was that? → About 100 years ago: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).

## Question axes

- move: analogy 4, cause_effect 8, count 4, estimate 8, identify 21, made_of 5, name_concept 14, odd_one_out 4, origin 9, purpose 7, record 3, sequence 2, when 12, who 5, word_meaning 16
- stimulus: detail 5, none 98, photo 19
- clue: completion 8, direct 53, riddle 9, scenario 13, three_facts 39
- answer_kind: group 16, number 12, person 9, place 13, thing 27, time 13, word 32
- lens: body_senses 8, educational_media 17, everyday 18, history 18, language 23, nature 8, pop_culture 15, school 15

## Dropped by the pipeline

- cities-and-towns-6: overlap like q-19508: Many British seaside towns have one of these, stretching out over the waves with arcades and rides along it. What is it? → A pier: This is Brighton's most famous seaside sight, with rides and arcades on top. What is it called? → A pier
- cities-and-towns-11: overlap like q-18531: These guards, nicknamed Beefeaters, live and work at which famous London landmark? → The Tower of London: What is the name of this famous castle in London? → The Tower of London
- cities-and-towns-13: overlap like q-9824: Wellies, the rubber boots for wet British days, are named after which famous person? → The Duke of Wellington: Glastonbury Festival is famous for its mud, so lots of fans wear these. What are they called? → Wellies
- counties-and-regions-5: overlap like q-9751: The Manx cat comes from the Isle of Man. Because of a natural gene change, many Manx cats are born without what? → A tail: Manx cats come from the Isle of Man. A “stumpy” Manx has a short one, and a “rumpy” has none at all. None of what? → A tail
- crown-and-state-3: overlap like q-18220: Look at this red box on a British street. What do people put in it? → Letters and cards: For about 150 years, red boxes like this have stood on streets all over the UK. What do people put in them? → Letters and cards
- customs-and-ceremonies-3: overlap like q-18777: Scottish men wear a kilt to weddings, on Burns Night and at Highland games, often with a sporran. What is a kilt? → A knee-length tartan skirt: I'm a pattern of coloured stripes crossing each other in squares. Each Scottish clan has its own version of me. Bagpipers and shortbread tins love me. What am I? → Tartan
- customs-and-ceremonies-9: overlap like q-9737: In the UK, who has the power to make someone a knight? → The King: In this British ceremony, the King taps a kneeling person on each shoulder with a sword. What does that person become? → A knight
- football-0: overlap like q-2488: A match ends in a draw and goes to a penalty shootout. How many kicks does each team take at first? → 5: Look at the photo of a penalty kick. In a penalty shootout, how many kicks does each team take before it goes to sudden death? → 5
- hills-moors-and-national-parks-11: overlap like q-19565: This is Prince Philip, who started the Duke of Edinburgh's Award in 1956. Who is the award meant for? → Young people: The Duke of Edinburgh's Award is named after the royal who started it in 1956. Who was he? → Prince Philip
- landmarks-and-castles-4: overlap like q-19452: This king won the Battle of Bosworth in 1485 and began the Tudor family's rule. Who is he? → Henry VII: I was born in Pembroke Castle in Wales in 1457. In 1485 I beat Richard III at the Battle of Bosworth and took the crown. Who am I? → Henry VII
- landmarks-and-castles-13: overlap like q-18709: Round arches, thick walls and zigzag carving mark Norman architecture, like Durham Cathedral. After which year did it spread across England? → 1066: You're standing among the huge zigzag-carved stone columns of Durham Cathedral. In which period of history was it begun? → Norman times
- languages-of-britain-6: overlap like q-13177: Von welchem Tier stammt dieser Speck meistens? → Schwein: This bacon butty is a British café favourite. Which animal does the bacon come from? → Pigs
- legendary-heroes-2: overlap like q-18477: Some say this hill in Somerset was the real Camelot. In the legends, who was the queen there? → Guinevere: In 1191, monks at this abbey in Glastonbury said they had dug up King Arthur's grave. Which queen did they say lay beside him? → Guinevere
- legendary-heroes-11: overlap like q-19115: In June 1215, at Runnymede, a meadow by the River Thames, King John put his seal on a famous charter. What is it called? → Magna Carta: You're at Runnymede, where Robin Hood's old enemy Prince John, by then king, sealed Magna Carta. In which century was that? → The 13th century
- london-0: overlap like q-19653: Which of these is NOT a Bonfire Night tradition in Britain? → Hunting for chocolate eggs: Bonfire Night on 5 November remembers the Gunpowder Plot of 1605. Which of these is NOT part of a usual Bonfire Night? → Chocolate eggs
- london-4: overlap like q-18317: I'm a Yeoman Warder at the Tower of London. Each day I feed my feathered charges raw meat and tuck them into their night pens. Who am I? → The Ravenmaster: He is a Yeoman Warder at the Tower of London, he feeds the big black birds every day, and he knows each one by name. What is his job called? → Ravenmaster
- london-7: overlap like q-2307: Dogs like this one star in a Disney film set in London, with 101 spotted puppies. What breed is it? → Dalmatian: This spotty coat belongs to the puppies in a famous London story with Pongo and Cruella de Vil. Which kind of dog is it? → Dalmatians
- london-9: overlap like q-19845: Listen: which British animal is making this scream at night in towns and gardens? → A fox: This bushy orange tail belongs to an animal often seen trotting through London gardens at night. Which animal is it? → A fox
- london-11: overlap like q-6221: This was found in an ancient Egyptian tomb. What is it? → A mummy: Crowds come to see these in the British Museum's Ancient Egypt rooms. What are they? → Mummies
- middle-ages-0: overlap like q-19063: My people fought long wars against England in the Middle Ages. My hero William Wallace won a battle at a bridge in 1297, and the film “Braveheart” tells his story. Which country am I? → Scotland: I fought for Scotland's freedom over 700 years ago. A tall tower near Stirling is named after me, and in the film “Braveheart” Mel Gibson played me. Who am I? → William Wallace
- middle-ages-6: overlap like q-18117: These dancers wave white hankies as they skip and jump outside village pubs. Who are they? → Morris dancers: These dancers wear bells strapped to their legs. Which English folk dance are they doing? → Morris dancing
- middle-ages-8: overlap like q-18483: In 1066, near Hastings, English foot soldiers stood behind a wall of shields. Which army charged them with knights on horses and archers? → The Normans: In 1066, William of Normandy's knights beat King Harold's army in Sussex, and the Bayeux Tapestry tells the story. Which battle was it? → The Battle of Hastings
- money-and-shopping-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This British supermarket started in Shropshire in 1970, and its old TV slogan was “That's why mums go to Iceland”. What is it best known for selling? → Frozen food
- money-and-shopping-5: overlap like q-18883: In Britain, what is a “fiver”? → A £5 note: Complete the British nickname: a £5 note is a “…”. → Fiver
- pop-and-rock-12: overlap like q-17909: We're a Geordie duo who met on Byker Grove, and each winter we send celebrities into the Australian jungle. Who are we? → Ant and Dec: We're best mates from Newcastle, we always stand the same way round on telly, and we present Britain's Got Talent. Who are we? → Ant and Dec
- regional-specialities-2: overlap like q-19972: This is an Aberdeen Angus, first bred in Aberdeenshire in Scotland. What kind of animal is it? → A cow: Welsh Blacks are a famous farm animal from Wales. Which animal is shown in this close-up? → A cow
- regional-specialities-10: overlap like q-19122: In Lancashire, “Creamy”, “Tasty” and “Crumbly” are the three types of a local food, often eaten with an Eccles cake. What food? → Cheese: It's white and crumbly, it's named after a Welsh town with a huge castle, and miners once took it down the pits for lunch. What is it? → Cheese
- regional-specialities-16: overlap like q-18853: On I'm a Celebrity, famous faces take on Bushtucker Trials in the Australian jungle. In Australian slang, what is “tucker”? → Food: In British slang, “I'm starving, let's grab some scran!” means you want some… → Food
- regional-specialities-17: overlap like q-13177: Von welchem Tier stammt dieser Speck meistens? → Schwein: Wiltshire is famous for ham like this. Which animal does ham come from? → A pig
- accents-and-dialects-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In the North of England, what is “chuddy”? → Chewing gum
- customs-and-ceremonies-4: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: At British universities, when does Freshers' Week happen? → Just before the first term's lessons start
- football-11: fact-check wrong: The grounds are usually cited as about 200 yards (~183 m) apart, not 300 m. The fun fact's 'neighbouring streets' is loose (they are on or near the same street, Tannadice Street).: Dundee and Dundee United play the Dundee derby. About how far apart are their two home grounds? → About 300 metres
- legendary-heroes-15: overlap like q-19999: In which year was the famous Sycamore Gap tree beside Hadrian's Wall cut down overnight? → 2023: A lone sycamore in a dip of an ancient wall became the “Robin Hood Tree” after a 1991 film was shot there. Which wall? → Hadrian's Wall
- middle-ages-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Complete the old British weather saying: “St Swithin's Day, if thou dost ___, for forty days it will remain.” → rain
- money-and-shopping-9: hard fail: correct 3, unambiguous 5, no_giveaway 5, no_overlap 5: You're grabbing a supermarket meal deal for lunch. How many items do you pick for the one price? → 3
- rugby-and-cricket-6: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: I push at the very back of the rugby scrum, and my position is simply named after my shirt number. Who am I? → The number eight
- sayings-and-idioms-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: When a Brit chatters on and on, people say they're “…ing on”. Which animal fills the gap? → A rabbit
- sayings-and-idioms-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: What does the saying “Too many cooks spoil the broth” warn you about? → Too many helpers can ruin a job
- sayings-and-idioms-10: overlap like q-0286: En 'Alicia en el país de las maravillas', ¿qué gato desaparece poco a poco hasta que solo queda su sonrisa? → El Gato de Cheshire: In which famous story does a Cheshire Cat fade away until only its grin is left? → Alice's Adventures in Wonderland
- sayings-and-idioms-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Football pundits love the cliché “It's a game of two…”. What's the missing word? → Halves
- team-gb-and-olympians-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: After retiring as an Olympic track cycling champion, Victoria Pendleton took up racing on what? → Racehorses
- traditional-music-and-dance-12: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: What kind of shoe is this close-up from? → Clogs
- twentieth-century-11: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In prison, some suffragettes went on hunger strike to fight for votes for women. What did they refuse? → Food
- sayings-and-idioms-5: overlap like q-12771: Ben Franklin printed the saying “Early to bed and early to rise makes a man healthy, wealthy, and…” How does it end? → Wise: Complete the old saying: “Early to bed and early to rise makes a man healthy, wealthy and…” → Wise
- sporting-events-17: overlap like q-3029: Runners often get shiny foil blankets like these after a marathon. Where were these blankets first meant to be used? → In space: At the end of the London Marathon, tired runners get wrapped in shiny, crinkly sheets like this one. What are they? → Foil blankets
- team-gb-and-olympians-1: overlap like q-9809: Eddie the Eagle became a hero at the 1988 Calgary Olympics despite finishing last in ski jumping. What did the “Eddie the Eagle rule” then require? → Minimum qualifying results to compete: Look at the photo: in this sport, a British plasterer came last at the 1988 Winter Olympics and became a hero. Who is he? → Eddie the Eagle
- team-gb-and-olympians-6: overlap like q-16374: Completa: Ander Mirambell fue el primer español en tirarse en los Juegos de Invierno, de cabeza y boca abajo, en la prueba de… → skeleton: I'm a Winter Olympic sport on ice. Amy Williams won gold in me for Britain in 2010, and Lizzy Yarnold won me twice. You ride me on a tiny sled, lying on your tummy. What am I? → Skeleton
- team-gb-and-olympians-12: overlap like q-18935: Which British runner made this celebration famous when he won gold at London 2012? → Mo Farah: I came to London from Somalia as a child. On Super Saturday in 2012, I won the 10,000 m soon after two teammates won gold. Who am I? → Mo Farah
- traditional-music-and-dance-14: overlap like q-4061: You're watching the Eurovision Song Contest when Irish dancers with still arms and flying feet start Riverdance. Which decade is it? → The 1990s: Riverdance began as the seven-minute interval act at the Eurovision Song Contest in Dublin. In which year? → 1994
- transport-12: overlap like q-12250: Bajo varias ciudades españolas quedan túneles como este, excavados durante la Guerra Civil (1936-1939). ¿Para qué servían? → Para protegerse de los bombardeos aéreos: During the Second World War, London families carried blankets down to Tube platforms every evening, and some stations even got bunk beds. Why? → To shelter from air raids
- twentieth-century-7: overlap like q-17826: You've seen “Keep Calm and Carry On” on mugs and tea towels. Roughly how many copies of the original poster were printed in 1939? → About 2.5 million: A British poster from 1939, now found on mugs everywhere, says “Keep calm and…”. How does it end? → Carry on
- twentieth-century-8: overlap like q-1636: Nunca iba a ser rey, pero mi hermano renunció a la corona por amor y me tocó a mí. Además, tartamudeaba. ¿Quién soy? → Jorge VI: You're reading the royal family tree: King George V, then his son Edward VIII, then Edward's brother George. Which George was he? → George the Sixth
- twentieth-century-16: overlap like q-0163: En 1928, Alexander Fleming vio un moho creciendo en un plato de laboratorio. ¿Qué medicina descubrió? → La penicilina: In 1928, Alexander Fleming came back from holiday and found something fuzzy on a dish, killing the germs around it. What was it? → A mould
