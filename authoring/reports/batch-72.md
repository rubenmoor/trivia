# batch-72

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, landmarks-and-castles, early-britain, middle-ages, twentieth-century, customs-and-ceremonies, legendary-heroes, pop-and-rock, traditional-music-and-dance, soaps-and-dramas, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, team-gb-and-olympians, sporting-events, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, transport, crown-and-state, hills-moors-and-national-parks, birds, plants-and-gardens, weather-and-seasons, tudors-and-stuarts, georgians-and-victorians
- Merged: 97 (q-20091…q-20187)
- Approved: 90
- Needs work: 7
- Dropped by the pipeline: 66
- Reviewed by: claude-opus-5-5
- Claude calls: 306, about $37.20 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-70, batch-71; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-70 | batch-71 | batch-72 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 191 | 175 | 163 |
| skipped slots |  | 313 | 329 | 341 |
| dropped |  | 68 | 53 | 66 |
| drop rate | ≤ 20.0 % | 35.6 % ✗ | 30.3 % ✗ | 40.5 % ✗ |
| dropped: hard fail correct |  | 2 | 1 | 2 |
| dropped: hard fail unambiguous |  | 0 | 0 | 1 |
| dropped: hard fail no_giveaway |  | 12 | 11 | 16 |
| dropped: overlap |  | 50 | 40 | 46 |
| dropped: duplicate |  | 3 | 0 | 1 |
| dropped: fact-check wrong |  | 1 | 1 | 0 |
| merged |  | 123 | 122 | 97 |
| approved |  | 111 | 113 | 90 |
| needs_work |  | 12 | 9 | 7 |
| needs_work rate | ≤ 20.0 % | 9.8 % ✓ | 7.4 % ✓ | 7.2 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 4.1 % ✓ | 4.1 % ✓ | 3.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.6 % ✓ | 0.8 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.6 % ✗ | 1.6 % ✗ | 1.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.3 % ✓ | 3.3 % ✓ | 3.1 % ✓ |
| media: no pick in review 1 |  | 12 | 15 | 16 |
| media: recovered by research |  | 10 | 12 | 13 |
| media: no pick at record |  | 2 | 3 | 3 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 28.8 % ✗ | 24.0 % ✗ | 29.4 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 7 | 8 | 0 |
| top move | ≤ 25.0 % | 14.6 % ✓ | 17.2 % ✓ | 15.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 82.9 % | 80.3 % | 77.3 % |
| values stimulus |  | 5 | 3 | 3 |
| top clue | ≤ 60.0 % | 41.5 % ✓ | 43.4 % ✓ | 43.3 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 26.0 % ✓ | 26.2 % ✓ | 34.0 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.7 % ✓ | 18.9 % ✓ | 18.6 % ✓ |
| values lens |  | 9 | 8 | 10 |
| media share | 15.0 %–50.0 % | 17.1 % ✓ | 19.7 % ✓ | 22.7 % ✓ |
| mean fun | ≥ 3.40 | 3.43 ✓ | 3.44 ✓ | 3.44 ✓ |
| cost $ |  | $40.51 | $39.18 | $33.82 |
| $ per approved | ≤ $0.35 | $0.36 ✗ | $0.35 ✓ | $0.38 ✗ |
| calls |  | 287 | 283 | 246 |
| calls per approved |  | 2.59 | 2.50 | 2.73 |
| wall time h |  | 1.22 | 1.15 | 1.10 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 56 (4 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 10 (2 major), fact 1 (1 major), overlap 4 (0 major), media 3 (2 major), difficulty 2 (2 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.37

Major findings on approved questions:

- **q-20100**: giveaway, difficulty — The facts are right: the Turing £50 is red and is the Bank of England's highest-value note, its ticker tape shows 23061912 in binary, and the £20 is purple. But the question text says "highest-value note" and the four options are £50, £20, £10 and £5, so the biggest number wins and players need nothing about red or Turing. This is the "which of these is biggest" pattern the house style bans, so a young child can get it and the difficulty is about 2, not 4. Rewrite it so that red or Turing is the real clue, without "highest-value". (http://127.0.0.1:8001/review/q-20100)
- **q-20134**: giveaway, difficulty — The facts are right: Æthelred II ruled around 1000, "Unræd" means "no counsel" and puns on his name, and his son was Edward the Confessor. The problem is that the description ("a royal nickname so bad…") and the question's "badly advised" both tell players the nickname is an insult, and The Unready is the only insulting option (The Confessor, The Great and The Bold are all flattering), so they can rule out every wrong answer before any hint and the question plays well below 9. Fix it with negative or neutral wrong answers (for example "The Simple", "Lackland", "The Fat") and a description that doesn't say whether the nickname is good or bad. (http://127.0.0.1:8001/review/q-20134)

## Needs work

- **q-20092** (birds) This bird of British farms and moors has the old nickname “peewit”. Where does that nickname come from? → The sound of its call: Hint 2 gives the answer away. Hint 1 already rules out "The shape of its crest", and hint 2 says names don't come "from places or old words", which rules out "A village in Yorkshire" and "An old word for green". After hint 2, only the correct answer is left. Hint 2 should instead point vaguely to the bird's behaviour in spring (for example, that you are more likely to notice it with your ears than your eyes) without ruling out the wrong answers by name.
- **q-20111** (football) Look at the photo: these fans of the visiting team are packed in together behind one goal. What do British fans call this part of the ground? → The away end: No candidate shows what the essential photo needs: a British football ground with visiting fans packed behind a goal. Candidates 1 and 5 are empty rugby league stands, 2 is a stadium exterior, and 3, 4 and 6 are Korean grounds. We can't search again. The text could also work with an illustrative image, since the question itself says the fans are visiting, so dropping "Look at the photo" would allow a looser image. No suitable picture found for this question.
- **q-20126** (plants-and-gardens) An old British carol is named after these two plants. What do people traditionally use them for at home? → Christmas decorations: The essential image must show both plants (“these two plants”), but no candidate shows holly together with ivy: 1 is a bird illustration, and 2 and 3 show holly only. A new search isn't allowed this round. The slot needs a holly-and-ivy photo, for example from a search like “holly and ivy”. Another option is to reword the question so it doesn't depend on the picture. No suitable picture found for this question.
- **q-20132** (crown-and-state) This special dark red train was built to carry which people? → The royal family: No candidate fits the essential slot. The question says “this special dark red train”, but every candidate is a black-and-white photo. Candidate 1 also shows a royal crest on the side, which gives the answer away. Candidates 3–6 are New Zealand royal carriages from 1901 and 1927, not the British Royal Train, and 3–4 show interiors. A new search isn't allowed, so the slot needs a colour photo of the claret Royal Train with no crests visible, found manually or by a later search. No suitable picture found for this question.
- **q-20149** (middle-ages) What kind of traditional dancing is shown in this close-up? → Morris dancing: This repeats approved q-18117, which already asks players to recognise morris dancers from their white hankies and from dancing outside village pubs. Hints 1 and 2 here are almost exactly that question's clue, so whichever of the two is played first gives away the other. Drop this question, or turn it into a different morris fact (for example the bell pads, the Will Kemp dance or Whitsun traditions) that doesn't depend on recognising the dance.
- **q-20165** (tudors-and-stuarts) In Tudor times, people played “mob football” through the streets, often on Shrove Tuesday. What does “mob” mean here? → A huge, wild crowd: Hint 2 ("The word describes the players, not the ball, the pitch or the kicking") rules out all three wrong answers by name, so it gives the answer away before hint 3. Replace it with a hint that doesn't eliminate options directly, e.g. one about how many people could join in (whole villages or parishes).
- **q-20170** (weather-and-seasons) Britons say it's “pelting down” outside. What's pelting down? → Heavy rain: The description ("The sky's throwing things again, and it's got a very good aim") rules out options before any hint. Autumn leaves come from trees, not the sky, and fog isn't thrown, so only rain and drizzle are left. Rewrite it to play on British weather or soggy days without saying that something falls from the sky.

## Question axes

- move: analogy 2, cause_effect 8, count 2, estimate 7, identify 13, made_of 3, name_concept 15, odd_one_out 3, origin 8, purpose 15, record 3, sequence 1, when 3, who 2, word_meaning 12
- stimulus: detail 2, none 75, photo 20
- clue: completion 3, direct 42, riddle 13, scenario 10, three_facts 29
- answer_kind: group 14, number 9, person 7, place 9, thing 22, time 3, word 33
- lens: body_senses 2, educational_media 14, everyday 10, history 18, language 18, nature 8, pop_culture 11, school 13, science_news 2, university 1

## Dropped by the pipeline

- accents-and-dialects-7: overlap like q-19733: In which country do people say “Bore da” to mean “good morning”? → Wales: “Iechyd da!” is said as glasses clink, it means “good health”, and it comes from the country with a red dragon on its flag. Which country? → Wales
- cities-and-towns-11: overlap like q-0218: Según una vieja leyenda, si cierto tipo de ave abandona la Torre de Londres, caerá el reino. ¿Qué aves viven por eso siempre en la Torre? → Cuervos: These big black birds live at the Tower of London. Legend says the kingdom will fall if they ever leave. What are they? → Ravens
- comedians-and-panel-shows-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In their TV show, The Goodies rode around on a bike like this one. How many people can ride it at once? → 3
- crown-and-state-3: duplicate like q-9707: The fruity tea loaf bara brith is a traditional bake from which part of the UK? → Wales: Look at this vegetable. It's a national symbol of which part of the UK? → Wales
- crown-and-state-6: overlap like q-19304: Crowns like this one belong to the Crown Jewels. In which London building are they kept under guard? → The Tower of London: In 1671, Colonel Blood dressed as a priest and tried to steal me from the Tower of London. He even flattened a crown to hide it! What am I? → The Crown Jewels
- crown-and-state-11: overlap like q-18488: I'm a soldier saint on a white horse. My red cross flies over England, and in old tales I beat a fire-breathing beast. Who am I? → St George: The upright red cross in the middle of this flag belongs to which saint? → Saint George
- customs-and-ceremonies-2: overlap like q-18465: You're trying to grab apples floating in a tub of water using only your teeth. On which night is this game most often played in Britain? → Halloween: In Scotland, children go “guising”: they dress up, knock on doors and tell a joke or sing for sweets. On which night? → Halloween
- customs-and-ceremonies-4: overlap like q-20089: At a yearly contest in a Cheshire village, digging is banned, so people wiggle garden forks in the lawn and even play music to it. Which creatures come up? → Earthworms: At British “charming” contests, people wiggle garden forks in the lawn to make this creature come up. What is it? → An earthworm
- customs-and-ceremonies-5: overlap like q-9515: I'm made from flour, eggs and milk. I puff up tall in a very hot oven. I sit beside roast beef with gravy. What am I? → Yorkshire puddings: In Ramsbottom, people throw black puddings to knock these off a high ledge. They're puffy, made of batter and served with a Sunday roast. What are they? → Yorkshire puddings
- customs-and-ceremonies-17: overlap like q-19305: Soldiers march through gates like these for the Changing of the Guard. Which royal palace is it? → Buckingham Palace: Most ceremonies where new knights get a sword tap on the shoulder are held in this London building. What is it? → Buckingham Palace
- early-britain-8: overlap like q-19581: I share my name with a Yorkshire battle from 1066, fought weeks before Hastings. Chelsea play their home games here. What am I? → Stamford Bridge: You're in King Harold's army in 1066: you win at Stamford Bridge in Yorkshire, then march south to fight at Hastings. About how long between the two battles? → About 3 weeks
- early-britain-10: overlap like cities-and-towns-11: These big black birds live at the Tower of London. Legend says the kingdom will fall if they ever leave. What are they? → Ravens: This is the White Tower, the oldest part of the Tower of London. Which birds live here, because legend says the kingdom will fall if they leave? → Ravens
- football-16: overlap like q-9593: Boxing Day comes how many days after Christmas Day? → 1 day: Britons eat leftover turkey on me, and football fans flock to big matches. I'm the day after Christmas Day. Which day am I? → Boxing Day
- georgians-and-victorians-1: overlap like q-18432: At a traditional afternoon tea on a three-tier cake stand, what goes on the bottom tier, to be eaten first? → Sandwiches: A traditional afternoon tea stand has one level for sandwiches, one for scones and one for cakes. How many levels does it have? → 3
- georgians-and-victorians-8: overlap like q-2522: Steam trains, Sherlock Holmes's London and Charles Dickens's novels all belong to a period named after a British queen. What is it called? → The Victorian era: Ladies carried lacy parasols to keep their skin pale, while families took the new steam trains to the seaside. Which era was this? → The Victorian era
- georgians-and-victorians-15: overlap like q-9637: You're in Trafalgar Square, counting the giant bronze lions around the base of Nelson's Column. How many are there? → 4: You're in London's Trafalgar Square, looking up at Nelson's Column. How many big bronze lions guard its base? → 4
- georgians-and-victorians-16: overlap like q-19305: Soldiers march through gates like these for the Changing of the Guard. Which royal palace is it? → Buckingham Palace: Queen Victoria was the first monarch to live in this London palace. What is it called? → Buckingham Palace
- landmarks-and-castles-11: overlap like q-9580: Westminster Abbey, January 1066: Harold Godwinson is crowned king. Who was crowned there next, on Christmas Day that same year? → William the Conqueror: I sailed from Normandy and won a famous battle in 1066. Two years later, I ordered a castle built on a hill in Lincoln. Who am I? → William the Conqueror
- languages-of-britain-12: overlap like q-19519: This primary school opened in 2001, teaches its lessons in a revived Celtic language, and is in St John's. Where is Bunscoill Ghaelgagh? → The Isle of Man: An old Celtic language is still learned and spoken on the island whose flag is shown here. Which island? → The Isle of Man
- middle-ages-10: overlap like q-18483: In 1066, near Hastings, English foot soldiers stood behind a wall of shields. Which army charged them with knights on horses and archers? → The Normans: In 1066, King Harold beat a Viking army in the north, then raced south when Duke William of Normandy landed. Near which town was the great battle fought? → Hastings
- money-and-shopping-1: overlap like q-17833: It's Christmas 2015, and John Lewis's advert shows a girl sending a gift to a lonely old man on the Moon. Which animal starred in the year before? → A penguin: Every November, Britons wait for John Lewis's Christmas advert. In 2014, it starred a toy one of these, called Monty. What animal is it? → Penguin
- money-and-shopping-5: overlap like q-18883: In Britain, what is a “fiver”? → A £5 note: Britons call a £10 note a “tenner”. Complete the pattern: a £5 note is a … → Fiver
- plants-and-gardens-7: overlap like q-18330: At election counts, British candidates often pin one of these to their chest in their party's colour. What is it called? → A rosette: I'm made of pleated ribbon, I look a bit like a flower, and I'm pinned beside the best marrow at a village show. What am I? → A rosette
- pop-and-rock-11: overlap like q-6239: These drinking straws can be washed and used again. What are they made of? → Metal: Punks in 1970s London wore pins like these on their clothes. What are they made of? → Metal
- accents-and-dialects-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Scotland, who leads the service in the kirk every Sunday? → A minister
- comedians-and-panel-shows-2: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: On ITV's Give Us a Clue, celebrities acted out film and book titles for their team. Which of these were they NOT allowed to do? → Speak out loud
- customs-and-ceremonies-7: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Since the 1970s, a Staffordshire pub has hosted a world championship in an odd kind of wrestling. What do the players wrestle with? → Their toes
- football-5: overlap like q-4372: At the 2018 World Cup, Colombia and England were tied 1–1 when the 90 minutes ended. When did the penalty shootout begin? → After 30 minutes of extra time: England lost these at the 1990 and 1998 World Cups, then finally won one against Colombia in 2018. What are they? → Penalty shootouts
- football-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Commentators shout me when a shot beats the goalkeeper, and comedy character Alan Partridge made me his catchphrase. What am I? → “Back of the net!”
- georgians-and-victorians-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Victorian “trappers” sat alone in dark coal mines, opening doors for the coal carts. How old were most trappers? → Between 5 and 10 years old
- languages-of-britain-11: overlap like q-18791: It's on road signs at a national border, on the shirts of a national football team, and it's a country's name in its own Celtic language. Which place is Cymru? → Wales: It started in 1982, it was the first TV channel mostly in Welsh, and its name is short for “Sianel Pedwar Cymru”. What does that mean? → Channel Four Wales
- money-and-shopping-10: hard fail: correct 3, unambiguous 5, no_giveaway 5, no_overlap 5: A British meal deal gets you a main, a snack and a drink for one price. You and your mum buy one each. How many items is that? → 6
- sayings-and-idioms-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: When surprising news “hits you for six”, Brits are borrowing a phrase from which sports players? → Cricketers
- sayings-and-idioms-8: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 5: It's a sudden fit of bad temper. Toddlers often have one in shops, and in Britain you “throw” one. What is it called? → A wobbly
- sayings-and-idioms-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Someone who chatters on and on is “rabbiting on”. It comes from Cockney rhyming slang “rabbit and…” what, rhyming with “talk”? → Pork
- sayings-and-idioms-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Brits refusing something might say “Not for all the tea in…” where? → China
- sitcoms-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In an old CBBC show, which magic object lets the schoolboy Bernard freeze time? → Pocket watch
- sporting-events-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Snooker referees wear gloves when they pick up the balls to clean them. What colour are the gloves? → White
- sporting-events-5: overlap like q-19181: What is the giant arch over Wembley Stadium, seen here, actually for? → Holding up the roof: When the old Wembley Stadium and its famous Twin Towers were knocked down, what became the new stadium's landmark? → A giant arch
- sporting-events-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It's held every March at Cheltenham, and the racers leap over big fences. Who races in the Cheltenham Gold Cup? → Horses
- sporting-events-15: overlap like q-19086: This orange cheese has “Double” in its name, and a wheel of it is chased down Cooper's Hill every year. Which place is it named after? → Gloucester: At Cooper's Hill in Gloucestershire, people chase a big round cheese down a very steep hill. Which cheese is it? → Double Gloucester
- team-gb-and-olympians-0: overlap like q-19624: This boxer won super-heavyweight gold at London 2012 and later became world heavyweight champion. Who is he? → Anthony Joshua: Audley Harrison, Anthony Joshua and Frazer Clarke all won Olympic boxing medals for Britain. In which weight class? → Super-heavyweight
- team-gb-and-olympians-5: overlap like q-18935: Which British runner made this celebration famous when he won gold at London 2012? → Mo Farah: Mo Farah had a famous victory pose, with his arms curved over the top of his head. What is it called? → The Mobot
- transport-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Britain, a minicab is usually an ordinary car, you have to book it in advance, and you can't wave one down in the street. What is it for? → Giving people a paid ride
- transport-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: At many British railway stations, you have to get through gates like these. Who do they let through? → People with a ticket
- transport-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This giant tangle of roads near Birmingham has a famous food nickname. What is it? → Spaghetti Junction
- twentieth-century-3: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Complete the sentence: a semi-detached house shares one wall with… → one other house
- twentieth-century-4: overlap like q-18252: Britain's top government ministers usually meet around this table every week. In which building is this room? → 10 Downing Street: Who lives and works behind this famous black door in London? → Prime Ministers
- twentieth-century-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Some suffragettes in prison refused to eat anything at all, to protest and win votes for women. What is this called? → A hunger strike
- rugby-and-cricket-1: overlap like q-6541: New Zealand's famous rugby team has a nickname. Complete it: the “All …” → Blacks: Before kick-off, these rugby players perform the haka. Which team are they? → The All Blacks
- rugby-and-cricket-9: overlap like q-2065: En rugby, llevan los números del 1 al 8, forman el scrum y entre ellos están los pilares y el talonador. ¿Cómo se llama este grupo? → Delanteros: You're watching a rugby union scrum. The player wearing number 8 is at the very back. How many players from one team are in the scrum? → 8
- soaps-and-dramas-3: overlap like q-17909: We're a Geordie duo who met on Byker Grove, and each winter we send celebrities into the Australian jungle. Who are we? → Ant and Dec: These two TV presenters first became famous as PJ and Duncan in the children's drama Byker Grove. Who are they? → Ant and Dec
- sporting-events-13: overlap like q-3029: Runners often get shiny foil blankets like these after a marathon. Where were these blankets first meant to be used? → In space: At the end of a marathon, runners are handed shiny sheets like these. What are they for? → To keep them warm
- team-gb-and-olympians-15: overlap like q-9809: Eddie the Eagle became a hero at the 1988 Calgary Olympics despite finishing last in ski jumping. What did the “Eddie the Eagle rule” then require? → Minimum qualifying results to compete: Eddie “the Eagle” Edwards from Cheltenham came last at the 1988 Winter Olympics, became a hero, and got a film about him. What was his sport? → Ski jumping
- traditional-music-and-dance-13: overlap like q-0487: Escucha: ¿qué instrumento suena? → La gaita escocesa: Listen: hundreds of musicians play these together at the Royal Edinburgh Military Tattoo. Which instrument is it? → Bagpipes
- tudors-and-stuarts-0: overlap like q-17123: Nací porque un rey inglés quería divorciarse de una hija de los Reyes Católicos y el Papa no le dejó. Ese rey se hizo mi jefe. ¿Qué soy? → La Iglesia anglicana: This king asked the Pope to annul his first marriage, declaring it had never counted. When the Pope said no, he did it anyway. Who is he? → Henry VIII
- tudors-and-stuarts-4: overlap like q-17880: The guards who wear this red-and-gold uniform have a famous nickname. What is it? → Beefeaters: Look at this uniform worn by the guards at the Tower of London. What is their famous nickname? → Beefeaters
- tudors-and-stuarts-6: overlap like q-16235: Los soldados de los tercios llevaban esta lanza de unos cinco metros, la pica. ¿Para qué servía sobre todo? → Para frenar a la caballería enemiga: It was a wooden pole up to 5 m (16 ft) long with a steel point. Civil War soldiers held it to stop charging horses. What was it called? → A pike
- twentieth-century-0: overlap like q-20006: The Palace of Holyroodhouse in Edinburgh is the official home in Scotland of which person? → The King: Who uses this huge castle west of London as a weekend home? → The King
- twentieth-century-7: overlap like q-17826: You've seen “Keep Calm and Carry On” on mugs and tea towels. Roughly how many copies of the original poster were printed in 1939? → About 2.5 million: Complete this British wartime slogan from 1939: “Keep Calm and…” → Carry On
- twentieth-century-8: overlap like q-18266: Ringo Starr was born in the Dingle in 1940, joined a famous band in 1962 and later narrated Thomas the Tank Engine. Which city is he from? → Liverpool: This statue shows the four Beatles. Three are John, Paul and George. Who is the drummer? → Ringo Starr
- twentieth-century-9: overlap like q-19073: The Spice Girls' first single, “Wannabe”, went to No. 1 in about how many countries? → 37: In which decade did the Spice Girls have their first number one, “Wannabe”? → The 1990s
- twentieth-century-13: overlap like q-5661: In 1969, a famous band walked across this London street crossing for an album cover. Which band was it? → The Beatles: Fans copy the Beatles walking over the zebra crossing on Abbey Road. In which decade was that album photo taken? → The 1960s
- twentieth-century-15: overlap like q-0163: En 1928, Alexander Fleming vio un moho creciendo en un plato de laboratorio. ¿Qué medicina descubrió? → La penicilina: Mould like this, growing in a dish, led to penicillin, a medicine that kills germs. Which Scottish scientist noticed it in 1928? → Alexander Fleming
- weather-and-seasons-10: overlap like q-16842: Trucks like this one clear snow off US roads. What do they often spread behind them to melt the ice? → Salt: On icy nights, lorries like this one drive along British roads. What do they spread to stop the roads freezing? → Salt
- weather-and-seasons-17: overlap like q-9783: Buy a “99” from an ice cream van and you get soft whippy ice cream in a cone. What is pushed into the top? → A Flake: In Britain, a “99” is a cone of soft, whippy white ice cream with something stuck in the top. What is it? → A chocolate flake
