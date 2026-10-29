# batch-29

Made by `qgen batch` on 2026-10-29 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, london, counties-and-regions, rivers-coasts-and-islands, hills-moors-and-national-parks, landmarks-and-castles, wildlife, birds, plants-and-gardens, weather-and-seasons, early-britain, middle-ages, tudors-and-stuarts, georgians-and-victorians, twentieth-century, parliament-and-prime-ministers, scientists-and-inventors, pioneers-and-heroes, classic-dishes, regional-specialities, cakes-puddings-and-biscuits, sweets-and-crisps, drinks, holidays-and-celebrations, christmas-in-britain, customs-and-ceremonies, legendary-heroes, creatures-ghosts-and-superstitions
- Merged: 350 (q-9487…q-9836)
- Approved: 331
- Needs work: 19
- Dropped by the pipeline: 63
- Reviewed by: claude-opus-5-5
- Claude calls: 703, about $84.36 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-27, batch-28; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-27 | batch-28 | batch-29 |
|---|---|---:|---:|---:|
| source locale |  | en | de (first de batch) | en |
| drafts |  | 337 | 406 | 413 |
| skipped slots |  | 113 | 80 | 91 |
| dropped |  | 50 | 39 | 63 |
| drop rate | ≤ 20.0 % | 14.8 % ✓ | 9.6 % ✓ | 15.3 % ✓ |
| dropped: hard fail correct |  | 3 | 0 | 2 |
| dropped: hard fail unambiguous |  | 2 | 0 | 1 |
| dropped: hard fail no_giveaway |  | 14 | 20 | 19 |
| dropped: overlap |  | 30 | 17 | 41 |
| dropped: duplicate |  | 1 | 0 | 1 |
| dropped: fact-check wrong |  | 0 | 2 | 0 |
| merged |  | 287 | 367 | 350 |
| approved |  | 261 | 343 | 331 |
| needs_work |  | 26 | 24 | 19 |
| needs_work rate | ≤ 20.0 % | 9.1 % ✓ | 6.5 % ✓ | 5.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.5 % ✓ | 0.8 % ✓ | 2.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 1.1 % ✓ | 0.9 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.5 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.5 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 5.6 % ✓ | 4.4 % ✓ | 2.6 % ✓ |
| media: no pick in review 1 |  | 34 | 52 | 46 |
| media: recovered by research |  | 27 | 40 | 38 |
| media: no pick at record |  | 8 | 12 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 9.5 % ✓ | 4.7 % ✓ | 10.4 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 68.1 % ✓ | 74.0 % ✓ | 76.2 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.71 ✗ | 2.14 ✗ | 1.00 ✓ |
| approved 11–15 |  | 49 | 64 | 69 |
| top move | ≤ 25.0 % | 17.1 % ✓ | 16.1 % ✓ | 18.0 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 77.7 % | 79.0 % | 81.4 % |
| values stimulus |  | 5 | 6 | 5 |
| top clue | ≤ 60.0 % | 48.1 % ✓ | 51.5 % ✓ | 47.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 30.3 % ✓ | 25.9 % ✓ | 23.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 15.7 % ✓ | 24.0 % ✓ | 16.0 % ✓ |
| values lens |  | 10 | 11 | 11 |
| media share | 15.0 %–50.0 % | 22.3 % ✓ | 21.0 % ✓ | 18.6 % ✓ |
| mean fun | ≥ 3.40 | 3.65 ✓ | 3.55 ✓ | 3.70 ✓ |
| cost $ |  | $69.16 | $87.70 | $81.75 |
| $ per approved | ≤ $0.35 | $0.26 ✓ | $0.26 ✓ | $0.25 ✓ |
| calls |  | 549 | 663 | 643 |
| calls per approved |  | 2.10 | 1.93 | 1.94 |
| wall time h |  | 2.25 | 3.58 | 3.19 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✓ pass |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 57 (4 %)
- Major among review needs work: 1 of 3 (33 %)
- Problems by kind: giveaway 4 (1 major), fact 1 (0 major), overlap 1 (0 major), media 4 (3 major), difficulty 3 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 3 of 60 (5 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.61

Major findings on approved questions:

- **q-9591**: media, giveaway — The facts check out: the statue was unveiled in 2018 and is the first of a woman in the square, the hints about her sister and the NUWSS are right, and the banner quote is hers. None of the three wrong options has a statue in the square. The essential image may give the answer away. London Remembers says "MILLICENT GARRETT FAWCETT" is carved on the front of the plinth, and the picked Geograph photo is a full-height portrait shot taken facing west, so it probably shows that front with her name. Someone should look at the photo and crop it or swap it for a figure-only close-up if the name shows. (http://127.0.0.1:8001/review/q-9591)
- **q-9730**: media — The facts check out: the Central line is red, runs from Epping to West Ruislip, is the longest line at about 74 km, and that ride is the longest Tube journey without changing trains. The media is the problem. The illustrative image is a 1938 Tube diagram (LT Museum) shown sharp, and Beck's maps from that time have a colour key listing the Central line in red. Together with the “red” clue in the question, the picture can give the answer away, so it needs a neutral picture (e.g. a Tube train or a platform roundel without a line name). (http://127.0.0.1:8001/review/q-9730)

## Needs work

- **q-9540** (counties-and-regions) What is the highest mountain in the United Kingdom? → Ben Nevis: Hint 2 ("It's in Scotland, near the town of Fort William") gives the answer away: each option is in a different UK nation (Snowdon is in Wales, Scafell Pike in England, Slieve Donard in Northern Ireland), so naming Scotland rules out all three wrong answers. Hint 2 should be vaguer, for example about its height or the cloud on its summit, and Scotland can go in hint 3 instead.
- **q-9549** (creatures-ghosts-and-superstitions) This photo, taken by two young cousins in Yorkshire in 1917, fooled many people. By what name is this famous fairy hoax known? → The Cottingley Fairies: The essential slot needs the 1917 Cottingley Fairies photo (Frances Griffiths with the paper fairies), but none of the candidates show it, and no new search is allowed. Fetch the Commons file directly (e.g. "File:Cottingley Fairies 1.jpg") or change the media role. No suitable picture found for this question.
- **q-9557** (customs-and-ceremonies) For a wedding at a register office in England, how many witnesses are legally needed? → 2: No candidate fits. Candidates 1 and 2 show robed clergy signing a register in a church. That contradicts the register-office setting (the description even says "no church"). Candidate 1 also shows exactly two people signing, which hints at the answer "2". Candidates 3–6 are an old French newspaper and 17th-century ship paintings, which have nothing to do with the question. The text itself is fine. It needs a neutral register-office image, for example "register office wedding room" or "marriage certificate pen", with no visible count of signers. No suitable picture found for this question.
- **q-9561** (customs-and-ceremonies) It happens near the end of the summer term. There's a sack race and a parents' race, and the school houses compete for a cup. What is this called? → Sports day: Overlaps q-9560 (draft, same subcategory), whose question text reads "You're running an egg-and-spoon race at school sports day": anyone who sees that one first is handed this answer. Keep only one of them, or reword q-9560 so it doesn't say "sports day".
- **q-9563** (drinks) Ribena's name comes from the Latin “Ribes nigrum”, and in the Second World War it was given to children for vitamin C. Which fruit is it made from? → Blackcurrant: The text is fine, but none of the image candidates fit a question about a British fruit drink, and a new search isn't allowed. The slot needs a new search, for example "blackcurrant cordial glass" or "fruit squash jug". A bush or bunch of blackcurrants would also work, since the image is shown blurred. No suitable picture found for this question.
- **q-9568** (drinks) Talisker, a smoky, peppery single malt whisky, has been made since 1830 on which Scottish island? → Skye: The text is fine, but no media candidate fits. None of them shows whisky or a whisky glass: there is a melon still life, antique engraved beakers with German text, a Victorian pink tumbler and a red wine splash. A new search (e.g. "Talisker distillery" or "whisky glass dram") is needed, but no further search is allowed here. No suitable picture found for this question.
- **q-9590** (georgians-and-victorians) Britain brought in secret voting with the Ballot Act of 1872. The secret ballot is still nicknamed after which country, where its modern form began? → Australia: No candidate shows a ballot paper: the sheet has two painted decorative crosses, a pencil sketch of Dante, a wayside cross landscape, a Civil War sutler-cart sketch and a medieval lead pencil. A new search isn't allowed. The slot also shouldn't be essential. An illustrative image would do, for example a ballot box or a polling station, or a ballot paper with no country text on it. No suitable picture found for this question.
- **q-9601** (hills-moors-and-national-parks) For centuries, island families in Scotland have cut peat from the moors to burn. Roughly how much does a peat bog grow each year? → About 1 mm: The description gives the answer away. “Grow so slowly that even a snail would get bored” states the answer's defining trait (extreme slowness), and when all four options are growth rates, that points straight to the smallest one, About 1 mm. Rewrite it to play on peat, moors or island fires without saying how fast peat grows.
- **q-9624** (legendary-heroes) The Scottish outlaw Rob Roy MacGregor, played by Liam Neeson in a 1995 film, lived around which time? → Around 1700: The picked picture has an unsuitable licence (pd-us-only: PD-1923, PD-US-expired).
- **q-9633** (london) How many yellow towers poke out of the roof of this huge London dome? → 12: Hint 1 gives the answer away: with the options 8, 10, 12 and 16, "chosen on purpose to match something about time" points straight to 12 (hours, months), so hint 2 and hint 3 add nothing. Hint 1 should be vague, for example about the dome's tent-like build or the masts holding up the roof, and the time link should move to hint 2 or 3. The facts are confirmed (12 masts of about 100 m, a 365 m dome that is 52 m high).
- **q-9669** (pioneers-and-heroes) In 2020, aged 99, Captain Tom Moore walked 100 laps of his garden and raised more than £30 million. Who was the money for? → NHS charities: None of the candidates works. #1 (a patient in a hospital gown with a walking frame beside a hospital bed) is shown sharp, and the hospital setting points straight at the NHS and rules out the three charity distractors. #2–6 (a stone house, an old general store, two moths and a US politician) have nothing to do with the topic. A neutral image is needed, such as an English back garden lawn or a walking frame on a garden path with no hospital in view. No suitable picture found for this question.
- **q-9675** (plants-and-gardens) Garden owners in Britain have planted this upright bluebell since the 1600s, and now it crosses with the native kind. Where did it first come from? → The Iberian Peninsula: Hint 2 (“Its home is in south-western Europe”) gives the answer away: of the four options, only the Iberian Peninsula is in south-western Europe (the Netherlands is north-west, the Balkans south-east, Scandinavia north). Replace it with a hint that still leaves at least two options open, for example one about its long flowering season or its tough, sturdy growth.
- **q-9713** (drinks) In a British pub, regulars often chat with “the landlord”. Who is that? → The person who runs the pub: Hint 2 is misleading. It says the title "has nothing to do with owning fields or farmland", but "landlord" does come from owning or letting out land and property. The fact check marked it wrong. Rewrite hint 2 to be accurate, for example: the title dates from when innkeepers let out rooms to lodgers. Fact check: wrong. Answer is right, but hint 2 is misleading. 'Landlord' literally means lord of land, from owning or letting property. It is not unrelated to land ownership.
- **q-9745** (plants-and-gardens) The tails side of the 12-sided £1 coin shows a rose, a leek, a thistle and a shamrock. What do the four plants stand for? → The four nations of the UK: None of the candidates shows the 12-sided £1 coin that the question names. Five are George III gold guineas and half-guineas (1778–1803), and one is a Korean War bomb photo. No new search is allowed, so this needs a manual media pick, for example the Wikimedia Commons file of the 2017 £1 coin, with either side shown (search "2017 one pound coin"). No suitable picture found for this question.
- **q-9779** (scientists-and-inventors) Around 1770, William Addis made one of the first modern toothbrushes in a London prison. What did he use for the handle? → A bone from his dinner: Fact check: uncertain. The bone-handle story is traditional, but sources differ on the date. Some say about 1770, while Wikipedia and others give 1780. The prison origin is also partly legend.
- **q-9809** (twentieth-century) Eddie the Eagle became a hero at the 1988 Calgary Olympics despite finishing last in ski jumping. What did the “Eddie the Eagle rule” then require? → Minimum qualifying results to compete: The fun fact says Eddie was short-sighted, but the usual sources (Wikipedia, BBC) say he was far-sighted (long-sighted) and wore thick glasses that fogged up, so the fact as written is likely wrong. Hint 1 ("Britain's only ski jumper, so he got in easily") also comes close to giving the answer away. It points straight at entry requirements, so the only qualifying-results option stands out before the stronger hints.
- **q-9813** (twentieth-century) Every Commonwealth Day, on the second Monday in March, the King and Commonwealth guests attend a big service in a London church. Which one? → Westminster Abbey: Hints 1 and 2 each give the answer away to UK players: "right next to the Houses of Parliament" and "Kings and queens are crowned there" both point straight to Westminster Abbey. Hint 1 should be vague (e.g. its age or its Gothic style, without the location), and hint 2 should be more indirect. The coronation fact or Poets' Corner could serve as hint 3.
- **q-9818** (weather-and-seasons) When snow falls in Britain, children grab a sledge, wrap up warm and head off to go sledging. Where do they go? → A steep hill: None of the candidates works: the results show a rocket sled, a rocket test track, a sea shell, a butterfly wing and sled dogs in Alaska. None shows a child's sledge or snowy British hills, and #6 shows a flat snowy field, which hints at a wrong option. Also, hint 2 (“slides down, then you walk back up”) gives the answer away almost as much as hint 3. It should be made vaguer, and the padding in the question (“wrap up warm and head off”) could be cut. No suitable picture found for this question.
- **q-9819** (weather-and-seasons) You wake up on a winter morning, the grass is white and crunchy, and someone says “Jack Frost has been!”. When did he come? → During the night: Hint 1 (“You were asleep when it happened.”) solves the question: of the four options, only “During the night” is a time when you'd be asleep. Hint 2 (“when the sun is gone”) also points straight to night. Hint 1 needs to become vague (for example about frost needing very cold air or a clear sky), and the night clues should only come in hints 2 and 3.

## Question axes

- move: analogy 3, cause_effect 23, count 7, estimate 10, identify 63, made_of 29, name_concept 33, odd_one_out 16, origin 27, purpose 26, record 13, sequence 15, when 26, who 37, word_meaning 22
- stimulus: detail 12, none 285, photo 48, sound 4, video 1
- clue: completion 8, direct 166, riddle 35, scenario 42, three_facts 99
- answer_kind: group 48, number 18, person 56, place 40, thing 82, time 32, word 74
- lens: body_senses 1, educational_media 50, everyday 56, history 55, language 48, nature 31, pop_culture 42, popular_science 9, school 42, science_news 10, university 6

## Dropped by the pipeline

- christmas-in-britain-3: overlap like q-3148: This big bird comes from the Americas, and many families roast it for big holiday feasts. What is it? → Turkey: It's cold, it's left over from the Christmas roast, and on Boxing Day it goes between two slices of bread. Which meat is it usually? → Turkey
- christmas-in-britain-8: overlap like q-9355: Wer verkündet in der Weihnachtsgeschichte den Hirten auf dem Feld die Geburt Jesu? → Engel: In a nativity play, the child who tells Mary she'll have baby Jesus wears this. Which kind of character are they? → An angel
- christmas-in-britain-16: overlap like q-6636: Jack is to the magic beans as the Evil Queen in “Snow White” is to the… → Magic mirror: In “Jack and the Beanstalk”, Jack swaps this animal for something. What does he get for it? → Magic beans
- cities-and-towns-1: overlap like q-0493: Mira la foto: ¿cómo se llama el río que pasa por debajo de este famoso puente? → El Támesis: A bend of this river, seen from the air, appears in the opening titles of EastEnders. Which river is it? → The Thames
- cities-and-towns-3: overlap like q-3412: Which London club is nicknamed after things like this one? → Arsenal: It's a word for a place where weapons are made or stored. It was a huge factory in Woolwich. Today it's a north London football club. What's the word? → Arsenal
- cities-and-towns-6: overlap like q-2792: London's Great Exhibition, the first world's fair, showed off inventions in a giant glass hall, the Crystal Palace. In which decade? → 1850s: This giant glass hall was built for the Great Exhibition of 1851. It later gave its name to a south London area and football club. What was it called? → Crystal Palace
- classic-dishes-2: overlap like q-8897: You're at an American diner and order a tall stack of flapjacks. What arrives? → Pancakes: It's a chewy British tray bake cut into squares, held together with butter and golden syrup. What is a flapjack mainly made of? → Oats
- classic-dishes-12: overlap like q-0398: Mira este acercamiento: ¿qué postre es? → Arroz con leche: It's baked slowly in milk with sugar, often topped with jam, and its small grains are the same food that goes into sushi. What is this pudding? → Rice pudding
- classic-dishes-13: overlap like q-4392: You're Harry at Hogwarts, and a parcel arrives with a hand-knitted sweater from Molly Weasley. Which day is it? → Christmas: You're pulling crackers and wearing a paper crown while someone carves a big roast turkey. Which day is it most likely? → Christmas Day
- counties-and-regions-8: duplicate like q-6211: Which of these countries is NOT in South America? → Spain: Which of these countries does NOT play in rugby's Six Nations Championship? → Spain
- creatures-ghosts-and-superstitions-15: overlap like q-8908: When bobbing for apples at a Halloween party, how many hands may you use to grab an apple? → 0: When you go apple bobbing at Halloween, what are you trying to do? → Grab a floating apple with your teeth
- early-britain-9: overlap like q-5578: This huge round table hangs in Winchester, England. In legend, why did King Arthur's knights sit at a round table? → So no knight sat above the others: The legendary Round Table had no head, so no knight could claim the best seat. Whose knights sat around it? → King Arthur
- georgians-and-victorians-9: overlap like q-2792: London's Great Exhibition, the first world's fair, showed off inventions in a giant glass hall, the Crystal Palace. In which decade? → 1850s: William IV reigned from 1830 to 1837. Which of these did NOT happen while he was king? → The Great Exhibition
- hills-moors-and-national-parks-2: overlap like cities-and-towns-8: You're eating a pastry with jam, almond sponge and white icing, maybe topped with a cherry. Which town is it named after? → Bakewell: Legend says a cook in Bakewell, Derbyshire, got a jam tart recipe wrong and created the Bakewell pudding. In which century? → The 19th century
- hills-moors-and-national-parks-3: overlap like q-4347: Look at this Border Collie. What kind of working dog is it on a farm? → A herding dog: Hill farmers use this clever dog to round up their sheep. What breed is it? → Border collie
- hills-moors-and-national-parks-9: overlap like q-2461: Look at this shaggy cow with long horns and a fringe over its eyes. Which country does this breed come from? → Scotland: This hairy cow comes from the Scottish Highlands. What does its long, shaggy coat help it do? → Stay warm in cold weather
- hills-moors-and-national-parks-13: overlap like counties-and-regions-9: Which famous children's writer lived in this Lake District farmhouse? → Beatrix Potter: Beatrix Potter bought Hill Top, her Lake District farmhouse, with money from her first books. In which decade? → The 1900s
- holidays-and-celebrations-1: overlap like q-5885: In a 2022 sketch, Elizabeth II told Paddington Bear what she kept in a handbag like this one. What was inside? → A marmalade sandwich: In 2022, I became the first British monarch to reach 70 years on the throne, and I had tea with Paddington Bear on TV. Who am I? → Queen Elizabeth II
- landmarks-and-castles-8: overlap like q-3914: The Western Wall holds up the side of Jerusalem's Temple Mount. What kind of rock is it built from? → Limestone: Norman builders shipped pale stone from Caen, in France, to build this Kent cathedral. What kind of rock is it? → Limestone
- landmarks-and-castles-12: overlap like q-9556: This giant arch towers over the stadium where the FA Cup Final is played. Which stadium is it? → Wembley Stadium: This giant white arch towers over which London stadium? → Wembley Stadium
- legendary-heroes-8: overlap like q-1083: En un poema medieval inglés, un caballero gigante y todo verde entra a una fiesta de Navidad y reta a la corte del rey. ¿A qué grupo de leyendas pertenece? → Las leyendas del rey Arturo: In a famous medieval poem, a giant knight rides into Camelot at Christmas to challenge Sir Gawain. His skin, hair and horse are all one colour. Which? → Green
- legendary-heroes-12: overlap like q-3509: In an old legend, the boy who pulled a sword like this one out of a stone became king. Who was he? → King Arthur: In the old British legend, a boy pulls a sword out of a stone and becomes king. What is his name? → Arthur
- london-4: overlap like q-5359: Who wears this tall black fur hat while on guard in London? → The guards at Buckingham Palace: Soldiers in red tunics and tall black bearskin hats march with a band to swap guards outside the King's official London home. Which palace is it? → Buckingham Palace
- london-12: overlap like q-1326: Brillo con diamantes, vivo guardada en la Torre de Londres y solo salgo en ocasiones muy especiales. ¿Quién me usa en la cabeza? → Un rey o una reina: This crown is one of the Crown Jewels. Who wears it at big ceremonies? → The King
- parliament-and-prime-ministers-9: overlap like q-6172: This seaside palace in Brighton, England, looks like it came from India. Which royal had it built? → George IV: I'm a seaside city with a famous pier and a royal palace with onion domes. In 2010 I elected Britain's first Green Party MP. Where am I? → Brighton
- parliament-and-prime-ministers-12: overlap like q-1024: ¿Qué creyentes celebran sobre todo la fiesta de las luces de esta foto, con lamparitas de barro y dibujos de colores en el suelo? → Los hindúes: Rishi Sunak was the UK's first prime minister of Asian heritage, and he lit Diwali lamps at Downing Street. He was also the first PM of which faith? → Hinduism
- pioneers-and-heroes-4: overlap like q-6389: Look at this aircraft. What does it usually carry? → Sick or injured people: I fly fast, land in fields and even on motorways, and bring doctors and paramedics to people who need help. In the UK, charity pays for most of me. What am I? → An air ambulance
- pioneers-and-heroes-15: overlap like q-6633: It sits on ice almost 3 km (2 miles) thick, it's colder than almost anywhere else, and explorers first reached it in 1911. What is it? → The South Pole: Captain Scott's Terra Nova Expedition reached the South Pole, only to find that Roald Amundsen had got there first. In which year? → 1912
- regional-specialities-16: overlap like q-6016: This fluffy pink treat in the photo is made almost entirely of one thing. What is it? → Sugar: You're at the British seaside and buy a stick of rock with the town's name inside. What is it mostly made of? → Sugar
- birds-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Swallows fly back to Britain from Africa every spring. Finish the old saying: “One swallow doesn't make a…” → Summer
- cakes-puddings-and-biscuits-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Many British children get a flat cardboard selection box at Christmas, often opened before breakfast. What's inside it? → Chocolate bars and sweets
- wildlife-17: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: This glossy black garden bird has a bright orange-yellow beak and a ring around its eye. What is it? → Blackbird
- christmas-in-britain-15: hard fail: correct 2, unambiguous 1, no_giveaway 5, no_overlap 5: The UK's first Christmas stamps, in 1966, were designed by the winners of a competition. About how old were the winners? → 6
- cities-and-towns-8: overlap like hills-moors-and-national-parks-2: Legend says a cook in Bakewell, Derbyshire, got a jam tart recipe wrong and created the Bakewell pudding. In which century? → The 19th century: You're eating a pastry with jam, almond sponge and white icing, maybe topped with a cherry. Which town is it named after? → Bakewell
- cities-and-towns-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which famous company performs at this riverside theatre? → The Royal Shakespeare Company
- counties-and-regions-9: overlap like hills-moors-and-national-parks-13: Beatrix Potter bought Hill Top, her Lake District farmhouse, with money from her first books. In which decade? → The 1900s: Which famous children's writer lived in this Lake District farmhouse? → Beatrix Potter
- customs-and-ceremonies-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In A. A. Milne's poem “Lines and Squares”, a child in London avoids treading on the lines in the pavement. Which animals will eat him if he does? → Bears
- customs-and-ceremonies-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: The Eton wall game is played along a brick wall at Eton College. In its big St Andrew's Day match, what hasn't happened since 1909? → A goal
- drinks-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Orange squash comes in a big bottle, it's thick and very sweet, and you only pour a little into your glass. What kind of drink is it? → A drink you mix with water
- drinks-16: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: I'm a brown powder you stir into hot milk. Long ago, Quaker families like the Cadburys sold me as a cosy drink instead of beer. What am I? → Cocoa
- early-britain-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: The famous “Cupid on a dolphin” mosaic floor at Fishbourne Palace in West Sussex was laid in which century? → The 2nd century AD
- georgians-and-victorians-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: In the 1840s, the Duchess of Bedford got hungry long before her late dinner, so she called for a hot drink, bread and butter and cake. What did this start? → Afternoon tea
- hills-moors-and-national-parks-0: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In “The Hound of the Baskervilles”, Dartmoor hides the Great Grimpen Mire. What is a mire? → A deep, wet bog
- holidays-and-celebrations-13: overlap like q-3228: I'm a London church. In 2011, Prince William and Catherine Middleton got married under my roof. Where am I? → Westminster Abbey: In April 2011, Prince William married Catherine Middleton at Westminster Abbey. That morning, they were made Duke and Duchess of where? → Cambridge
- holidays-and-celebrations-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: On Bonfire Night, a “guy” is made by hand, named after a man from 1605, and placed on top of the fire. What is it? → A stuffed dummy of a man
- holidays-and-celebrations-16: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: It's knitted, often has reindeer or snowflakes on it, and there's a charity day each December when people wear it to school. What is it? → A Christmas jumper
- middle-ages-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Robin Hood's friend Little John got his nickname because he was really… → Very tall
- parliament-and-prime-ministers-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In the House of Commons, when does an MP give their “maiden speech”? → Soon after first being elected
- pioneers-and-heroes-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Sir Chris Hoy, from Edinburgh, won six Olympic gold medals for Great Britain. In which sport? → Track cycling
- plants-and-gardens-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: The word “courgette” comes from French and means “little gourd”. What is a courgette? → A young marrow
- sweets-and-crisps-6: overlap like twentieth-century-12: In Britain, blue tits famously learned to peck through the foil tops of bottles left on doorsteps. Who left the bottles there? → The milkman: These chewy sweets copy the glass bottles once left on British doorsteps every morning. Who delivered the real ones? → The milkman
- weather-and-seasons-2: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In Scotland, some winter road vehicles have names like “Sir Andy Flurry” and “Gritney Spears”. What do they do? → Spread salt on icy roads
- weather-and-seasons-7: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: In Raymond Briggs's “The Snowman”, a boy creeps downstairs and finds his snowman has come to life. What time is it? → Midnight
- rivers-coasts-and-islands-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: At the British seaside, families queue at the “chippy”. The food comes wrapped in paper, with salt and vinegar. What does a chippy sell? → Fish and chips
- rivers-coasts-and-islands-17: overlap like counties-and-regions-9: Which famous children's writer lived in this Lake District farmhouse? → Beatrix Potter: In a famous children's story, red squirrels cross this lake on little rafts to visit an owl on an island. Who wrote it? → Beatrix Potter
- scientists-and-inventors-10: overlap like q-2321: Drivers see me on dark roads, and I'm named after the way a cat's eyes look at night. People call me a “cat's eye”. What am I? → A road reflector: Percy Shaw of Halifax invented cat's eyes in 1934. They sit in the road and light up in headlights. What are they for? → Showing drivers the lanes at night
- sweets-and-crisps-1: overlap like regional-specialities-16: You're at the British seaside and buy a stick of rock with the town's name inside. What is it mostly made of? → Sugar: Classic seaside rock is hard boiled sugar, pink on the outside, with letters running all the way through. What flavour is it traditionally? → Peppermint
- tudors-and-stuarts-5: overlap like q-3226: The Tudor dynasty ended in 1603 because Elizabeth I had no children. Who became king of England next? → James I: Queen Elizabeth I ruled England a long time ago. In which times did she live? → Tudor times
- tudors-and-stuarts-16: overlap like q-3934: Tourists crowd into this courtyard in Verona to see “Juliet's house”. Which family from the play was said to live here? → The Capulets: In “Romeo and Juliet”, two families in Verona hate each other, and Romeo is a Montague. Which family does Juliet belong to? → The Capulets
- twentieth-century-3: overlap like q-5707: In 1936 he gave up the British throne to marry Wallis Simpson, and his brother became the king of “The King's Speech”. What title did he get then? → Duke of Windsor: In which year did King Edward VIII give up the throne so he could marry the American Wallis Simpson? → 1936
- twentieth-century-7: overlap like q-5003: It lasted from 1914 to 1918, soldiers fought from muddy trenches, and people at the time called it “the Great War”. What do we call it today? → The First World War: In the First World War, soldiers lived for months in long ditches dug into the ground like this. What are they called? → Trenches
- twentieth-century-12: overlap like sweets-and-crisps-6: These chewy sweets copy the glass bottles once left on British doorsteps every morning. Who delivered the real ones? → The milkman: In Britain, blue tits famously learned to peck through the foil tops of bottles left on doorsteps. Who left the bottles there? → The milkman
- twentieth-century-15: overlap like q-4798: Who first called British Prime Minister Margaret Thatcher “the Iron Lady”? → A Soviet army journalist: Who became Britain's first woman Prime Minister, in 1979? → Margaret Thatcher
