# batch-64

Made by `qgen batch` on 2026-11-13 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): hills-moors-and-national-parks, sporting-events, wildlife, christmas-in-britain, twentieth-century, rugby-and-cricket, weather-and-seasons, game-shows-and-presenters, sayings-and-idioms, pub-and-playground-games, creatures-ghosts-and-superstitions, traditional-music-and-dance, counties-and-regions, school-and-childhood, transport, childrens-books-and-comics, nursery-rhymes-and-singalongs, football, childrens-tv, london, drinks, accents-and-dialects, tudors-and-stuarts, pioneers-and-heroes, early-britain, cakes-puddings-and-biscuits, flags-and-emblems, georgians-and-victorians
- Merged: 281 (q-18421…q-18701)
- Approved: 268
- Needs work: 13
- Dropped by the pipeline: 82
- Reviewed by: claude-opus-5-5
- Claude calls: 608, about $80.08 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-62, batch-63; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-62 | batch-63 | batch-64 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 402 | 370 | 363 |
| skipped slots |  | 102 | 134 | 141 |
| dropped |  | 72 | 89 | 82 |
| drop rate | ≤ 20.0 % | 17.9 % ✓ | 24.1 % ✗ | 22.6 % ✗ |
| dropped: hard fail correct |  | 4 | 1 | 1 |
| dropped: hard fail unambiguous |  | 0 | 0 | 2 |
| dropped: hard fail no_giveaway |  | 16 | 21 | 17 |
| dropped: overlap |  | 49 | 65 | 60 |
| dropped: duplicate |  | 3 | 3 | 3 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 330 | 281 | 281 |
| approved |  | 311 | 268 | 268 |
| needs_work |  | 19 | 13 | 13 |
| needs_work rate | ≤ 20.0 % | 5.8 % ✓ | 4.6 % ✓ | 4.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.0 % ✓ | 1.8 % ✓ | 2.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.6 % ✓ | 1.4 % ✓ | 0.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 1.1 % ✗ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 2.4 % ✓ | 1.1 % ✓ | 1.8 % ✓ |
| media: no pick in review 1 |  | 40 | 25 | 30 |
| media: recovered by research |  | 36 | 22 | 26 |
| media: no pick at record |  | 4 | 3 | 4 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.4 % ✓ | 0.4 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 13.2 % ✓ | 19.2 % ✓ | 17.9 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 74.8 % ✓ | 69.7 % ✓ | 68.0 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.10 ✓ | 1.10 ✓ |
| approved 11–15 |  | 77 | 62 | 57 |
| top move | ≤ 25.0 % | 14.5 % ✓ | 19.2 % ✓ | 14.6 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 89.7 % | 73.3 % | 81.9 % |
| values stimulus |  | 3 | 4 | 4 |
| top clue | ≤ 60.0 % | 42.7 % ✓ | 49.8 % ✓ | 42.0 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 24.5 % ✓ | 20.3 % ✓ | 26.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 24.8 % ✓ | 21.7 % ✓ | 16.7 % ✓ |
| values lens |  | 9 | 11 | 11 |
| media share | 15.0 %–50.0 % | 10.3 % ✗ | 26.7 % ✓ | 18.1 % ✓ |
| mean fun | ≥ 3.40 | 3.64 ✓ | 3.66 ✓ | 3.62 ✓ |
| cost $ |  | $81.87 | $75.29 | $76.96 |
| $ per approved | ≤ $0.35 | $0.26 ✓ | $0.28 ✓ | $0.29 ✓ |
| calls |  | 637 | 534 | 548 |
| calls per approved |  | 2.05 | 1.99 | 2.04 |
| wall time h |  | 2.77 | 2.29 | 2.33 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 57 (4 %)
- Major among review needs work: 2 of 3 (67 %)
- Problems by kind: giveaway 3 (1 major), media 5 (3 major), difficulty 2 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.11

Major findings on approved questions:

- **q-18445**: giveaway — The question text says "I'm a little fairy princess", and "Princess Holly" is the only option with "Princess" in it, so that word alone rules out Nanny Plum, Queen Thistle and Lucy Big. To fix it, write the answer as "Holly" or drop "princess" from the question. The facts are correct: Holly's twin sisters are Daisy and Poppy, her best friend is Ben Elf, her spells go wrong, and the show comes from Astley Baker Davies, who also made Peppa Pig. The image and the related questions are fine. (http://127.0.0.1:8001/review/q-18445)
- **q-18589**: media — The essential image is "Korbel Champagne Cellars", a photo of a winery. The question says "sandwiches like this", so it needs a picture of a leftover turkey sandwich, and players would see the wrong subject. The rest checks out: the answer is right, the wrong answers are clearly wrong (Boxing Day is also St Stephen's Day, but nobody eats sandwiches to honour him), the hints and fun fact are true, and no related question asks the same fact. (http://127.0.0.1:8001/review/q-18589)

## Needs work

- **q-18430** (accents-and-dialects) You'll hear “Wind your neck in!” in Belfast and across the UK. What does it mean? → Calm down and back off: The description (“sounds like advice from a chiropractor, but isn't”) tells players the meaning is not posture advice, which rules out the wrong answer “Sit up straight” before any hint. Rewrite the description so it plays on Belfast or put-downs in general without saying the phrase isn't about the body.
- **q-18432** (cakes-puddings-and-biscuits) At a traditional afternoon tea on a three-tier cake stand, what goes on the bottom tier, to be eaten first? → Sandwiches: Hint 2 ("start with the savoury things and save the sweetest for the top") gives the answer away. Sandwiches are the only savoury option, so this hint rules out scones, cakes and biscuits all at once. Hint 2 should be vaguer, for example about the order being a matter of etiquette or about what you might find on the other tiers, without saying "savoury".
- **q-18434** (cakes-puddings-and-biscuits) Look inside this Mars bar cut in half. What is the gooey golden layer on top of the soft nougat? → Caramel: No candidate shows a Mars bar cut open. The question says “this Mars bar cut in half”, so the essential image must show exactly that, and no new search is allowed. The slot needs a real Mars bar cross-section showing the nougat and caramel layers, with no wrapper. If none can be found, make the image illustrative or decorative instead. No suitable picture found for this question.
- **q-18473** (drinks) Costa Coffee was started in 1971 by two Italian brothers. In which city did they found it? → London: Hint 2 ("already home to the world's first underground railway") names a famous fact that only London has, so it gives the answer away at hint 2. The pool even asks that exact fact in q-0314. Hint 1 already cuts the options to London and Seattle, so hint 2 should be a vague clue, for example about the era or the type of business, and must not identify the city.
- **q-18485** (early-britain) They crowned hilltops across Iron Age Britain and sheltered whole villages. What were hill forts' defences mostly made of? → Earth banks, ditches and wooden fences: This overlaps too much with the approved q-9577 (Maiden Castle hill fort: “huge grassy ramparts… in which age was it mostly built?” → Iron Age). This question names “Iron Age Britain”, which gives away q-9577's answer, and q-9577's “grassy ramparts” gives away this answer (earth banks). Hint 1 (“grassy rings on a hill”) also nearly gives away the answer. Rewording this question won't fix it, because the earth ramparts are already the clue in q-9577. Drop it or ask about something else.
- **q-18505** (football) You buy an England replica football shirt. How many lions are on the badge? → 3: This repeats an approved question: q-5357 asks how many lions are on England's old royal coat of arms (3), and the England badge's lions come straight from those arms, as this question's own fun fact says. It's the same fact in other words, so one question gives the other away. Hint 2 is also a near-giveaway for UK players, since “England's team is often nicknamed after them” points straight to the “Three Lions” nickname.
- **q-18523** (hills-moors-and-national-parks) Which of these does NOT belong in the legends of King Arthur? → A glass slipper: Hint 2 gives the answer away. It describes all three wrong options in turn (the knights sat at the Round Table, searched for the Grail, and the king carried Excalibur), so the glass slipper is the only option left. Hint 2 should instead point vaguely at another story world without matching each Arthurian item. Also, this odd-one-out question doesn't fit the "Hills, moors and national parks" subcategory.
- **q-18560** (pioneers-and-heroes) This Victorian traveller rode through the Rocky Mountains, Japan and Persia, and in 1892 was among the first women made Fellows of the Royal Geographical Society. Who is she? → Isabella Bird: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-18599** (early-britain) My bones lay in a cave in Cheddar Gorge for about 10,000 years. How did I live? → As a hunter-gatherer: The question is a first-person riddle ("My bones lay… How did I live?") that asks about the speaker's way of life, not who the speaker is. House style says a riddle like this should be a direct question. Rewrite it as one, e.g. "A man's skeleton lay in a cave in Cheddar Gorge for about 10,000 years. How did he live?", and change the hints to the third person to match.
- **q-18642** (rugby-and-cricket) In cricket, one umpire stands at square leg, level with the batter. Which decisions is that umpire best placed to judge? → Run-outs and stumpings: The fun fact is misleading and the fact check marks it wrong. Each umpire stays at the same end, but at the end of every over they do move: one goes from behind the stumps to square leg, and the other goes from square leg to behind the stumps. Saying they “don't swap places” is false as most people will read it. Rewrite the fun fact, for example: “At the end of every over, the two umpires swap jobs: one walks out to square leg while the other takes his place behind the stumps.” Fact check: wrong. The answer is fine, but the fun fact is false. Umpires do change places between overs. The bowler's-end umpire moves to square leg, and the square-leg umpire goes to the new bowler's end. The roles swap and so do the positions.
- **q-18654** (school-and-childhood) Many British primary school girls wear a checked dress like this one in the summer term. What is this pattern called? → Gingham: None of the candidates gives the essential image the question needs: a clear photo of a gingham dress or fabric. #1 is a black-and-white archive scan whose typed caption says "blue gingham dress", which gives the answer away. In #2 the gingham dress is a tiny background detail among children in blue jumpers. #3–#6 show no gingham. A new search, such as "blue gingham dress" or "gingham fabric", is needed, but no more searches are allowed. No suitable picture found for this question.
- **q-18676** (tudors-and-stuarts) Before every State Opening of Parliament, these royal bodyguards search the cellars of Westminster with lanterns. Who are they? → The Yeomen of the Guard: The media slot doesn't fit. It is marked essential and its note asks for Yeomen of the Guard in uniform, which would show the answer. The search was for "Houses of Parliament night", so the candidates are buildings. The question doesn't need an image to be answered. Change the role to illustrative and use candidate 3 (Westminster Palace and Bridge at night). It fits the question and doesn't show any guard unit. No suitable picture found for this question.
- **q-18693** (weather-and-seasons) Which of these is NOT something the English scientist Lewis Fry Richardson is known for? → Naming the cloud types cumulus and stratus: None of the media candidates shows Lewis Fry Richardson or anything to do with weather forecasting, and no new search is allowed. There is a second problem: the description ("tried to out-think the British weather with a pencil") states the trait behind the option "Working out a weather forecast by hand with maths", so it rules that option out before any hint. It should play on the weather theme without the hand-calculation detail. No suitable picture found for this question.

## Question axes

- move: analogy 8, cause_effect 15, count 12, estimate 9, identify 31, made_of 20, name_concept 41, odd_one_out 10, origin 25, purpose 26, record 4, sequence 9, when 16, who 31, word_meaning 24
- stimulus: detail 6, map_outline 1, none 230, photo 44
- clue: completion 6, direct 118, riddle 35, scenario 38, three_facts 84
- answer_kind: group 38, number 25, person 56, place 21, thing 74, time 17, word 50
- lens: body_senses 20, educational_media 37, everyday 44, history 44, language 47, nature 7, pop_culture 41, popular_science 1, school 30, science_news 3, university 7

## Dropped by the pipeline

- accents-and-dialects-4: overlap like q-18067: You're watching Smithy and Nessa in Gavin & Stacey. Which actor plays Smithy and co-wrote the show with Ruth Jones? → James Corden: This BBC sitcom links Essex and Barry in South Wales, made “What's occurring?” a catchphrase, and was co-written by Ruth Jones. Which show? → Gavin & Stacey
- accents-and-dialects-7: overlap like q-9516: Cadbury's chocolate factory sits in a village built for its workers, in a city with more canals than Venice. Which city? → Birmingham: My people call everyone “bab”, my accent rings out in “Peaky Blinders”, and Cadbury World sits on my edge. Which city am I? → Birmingham
- cakes-puddings-and-biscuits-3: overlap like q-6032: You eat like a hobbit in the films: breakfast, second breakfast, elevenses and so on. How many meals a day is that? → 7: You're a hobbit who has just finished second breakfast. In “The Lord of the Rings”, which meal does Pippin say comes next? → Elevenses
- cakes-puddings-and-biscuits-9: overlap like q-8875: Rocky road ice cream was created in California in 1929. It's chocolate, its “rocks” are nuts, and its soft lumps are what? → Marshmallows: This British café traybake is chocolate set with broken biscuits and sweet lumps, and its bumpy top is named after a rough path. What is it? → Rocky road
- childrens-books-and-comics-4: overlap like q-4340: Narnia is to a wardrobe as the Land of Oz is to a… → Tornado: I stand in an old professor's house. Four children hide inside me, push past the fur coats and find a snowy land. What am I? → A wardrobe
- childrens-books-and-comics-10: overlap like q-18258: Which storybook girl is sitting on a riverbank, wondering whether to make one of these, when a White Rabbit runs past? → Alice: Who follows the White Rabbit down a rabbit hole and lands in Wonderland? → Alice
- childrens-books-and-comics-12: overlap like q-0079: En Harry Potter, ¿a qué casa de Hogwarts pertenece Harry? → Gryffindor: After a long think, which Hogwarts house does the Sorting Hat put Hermione Granger in? → Gryffindor
- childrens-tv-7: overlap like q-17866: On the CBBC show “Get Your Own Back”, who got covered in gunge? → A grown-up: I hosted a CBBC show where children got their own back on grown-ups by dunking them in the gunge tank. Who am I? → Dave Benson Phillips
- childrens-tv-17: overlap like q-9602: Postman Pat drives his red van around the valley of Greendale with his black-and-white cat. What is the cat called? → Jess: Which of these places is NOT home to an Aardman hero? → Greendale
- christmas-in-britain-8: overlap like q-18207: On Christmas Eve, you leave a mince pie and a small glass of sherry by the fireplace. Who are they for? → Father Christmas: You leave a carrot by the fireplace for Father Christmas's reindeer. On which night do you put it out? → Christmas Eve
- christmas-in-britain-10: overlap like q-6278: He lives in a castle above the clouds, he shouts “Fee-fi-fo-fum,” and he owns a hen that lays golden eggs. What is he? → A giant: Jack climbs the beanstalk and takes the hen that lays golden eggs. Who chases him back down? → A giant
- christmas-in-britain-11: overlap like q-18455: When the royal Christmas message was shown on television for the first time in 1957, whose face did viewers see? → Queen Elizabeth II: When the clock shows this time on Christmas Day, millions of Britons turn on the TV. What do they watch? → The royal Christmas message
- christmas-in-britain-16: overlap like q-6060: Look at this vegetable. In the story of Cinderella, what does the fairy godmother turn it into? → A carriage: She has a wand, she sparkles, and she appears when Cinderella is crying. What does she use a pumpkin to make? → A coach
- counties-and-regions-6: overlap like q-18004: This Six Nations team plays home games at Murrayfield, plays England every year for the Calcutta Cup and wears a thistle on its shirts. Which team is it? → Scotland: This trophy was made from melted-down silver rupees. Which two rugby teams play for it every year? → England and Scotland
- counties-and-regions-9: overlap like q-9751: The Manx cat comes from the Isle of Man. Because of a natural gene change, many Manx cats are born without what? → A tail: The Manx cat comes from the Isle of Man, has long back legs and often hops a bit like a rabbit. What is it famous for not having? → A tail
- counties-and-regions-10: overlap like q-18314: It's the royal family's summer home, Queen Victoria loved it, and it stands in the UK's largest national park. Which UK country is Balmoral Castle in? → Scotland: Prince Albert bought it for Queen Victoria in 1852, it stands by the River Dee in Aberdeenshire, and the royal family spends summers there. Which royal home is it? → Balmoral Castle
- counties-and-regions-12: overlap like q-17856: Flopsy, Mopsy and Cotton-tail first appeared in Beatrix Potter's “The Tale of Peter Rabbit”. In which decade was it first published? → The 1900s: This farmhouse in the Lake District belonged to the writer who created Peter Rabbit. Who was it? → Beatrix Potter
- creatures-ghosts-and-superstitions-11: hard fail: correct 3, unambiguous 3, no_giveaway 4, no_overlap 5: This old inn is often called the most haunted house in England. In which county is it? → Gloucestershire
- creatures-ghosts-and-superstitions-15: overlap like q-18470: Look at this circle of mushrooms in the grass. In old British stories, who danced in circles like this at night? → Fairies: Look at this tiny door at the bottom of a tree. Who is it meant for? → Fairies
- drinks-0: overlap like q-18393: Bet Lynch pulled pints here, and it's the pub of Britain's longest-running TV soap. Which pub is it? → The Rovers Return: It stands on the corner of a cobbled street in Weatherfield, and Ken Barlow and Jack Duckworth have drunk there. Which TV pub is it? → The Rovers Return
- drinks-6: overlap like q-18299: Crystal Palace FC are named after a giant hall built for the Great Exhibition of 1851. In which London park did it first stand? → Hyde Park: Schweppes won the right to sell soft drinks at the Great Exhibition in Hyde Park's Crystal Palace. In which year was it? → 1851
- drinks-14: overlap like q-18350: The world's first solid chocolate bar was made in 1847 by J. S. Fry & Sons, a Quaker family firm. In which English city? → Bristol: Fry's Cocoa was made by a Quaker family firm that also made the first moulded chocolate bar in 1847. In which city was it based? → Bristol
- early-britain-0: overlap like q-18242: He was the son of Sir Lancelot, the purest of the Knights of the Round Table, and the one who found the Holy Grail. What was his name? → Galahad: Lancelot was raised by the Lady of the Lake, fathered Sir Galahad and fell for his king's wife. Which legendary band did he serve in? → The Knights of the Round Table
- early-britain-7: overlap like q-1440: ¿Qué pueblo navegaba en drakares, barcos largos con una cabeza de dragón en la proa? → Los vikingos: Long ago, ships with a carved head like this one sailed to Britain. Which people built them? → The Vikings
- early-britain-16: overlap like q-3794: The Roman writer Pliny said druids climbed sacred oak trees to cut which plant with a golden sickle? → Mistletoe: I was a wise priest of the Celts. I met in oak groves and cut mistletoe with a golden sickle. Who am I? → A druid
- flags-and-emblems-3: overlap like q-9605: Neighbours set up long tables with bunting and food right in the middle of their road, like this. What is this called? → A street party: It hangs in the Great British Bake Off tent, across streets at royal street parties and over village fêtes. What are these strings of little triangle flags called? → Bunting
- game-shows-and-presenters-8: overlap like q-17915: Which veteran entertainer first ended each Strictly Come Dancing with “Keep dancing!”? → Bruce Forsyth: I hosted The Generation Game and Play Your Cards Right, and when I said “Nice to see you, to see you…”, audiences shouted “Nice!”. Who am I? → Bruce Forsyth
- game-shows-and-presenters-12: overlap like q-18406: Which British pair won Olympic gold in this sport in 1984, dancing to Ravel's “Boléro”? → Torvill and Dean: You're watching Dancing on Ice. Which famous Olympic pair, gold medallists skating to Boléro in 1984, helped launch it in 2006? → Torvill and Dean
- georgians-and-victorians-6: overlap like q-18007: England and Australia play cricket for a tiny urn, after a joke obituary for English cricket in 1882. What is the series called? → The Ashes: England and Australia play cricket for this tiny urn. How many Test matches does a series between them usually have? → 5
- georgians-and-victorians-7: overlap like q-9604: At Christmas dinner, two people pull this until it goes bang. What do you usually find inside to wear? → A paper crown: At Christmas dinner, two people pull one of these until it goes bang. What do you usually find inside? → A paper crown, a joke and a little toy
- georgians-and-victorians-9: overlap like q-18174: This castle sits on the rock of an ancient volcano, high above a capital city. Which castle is it? → Edinburgh Castle: Alexander Graham Bell, the inventor of the telephone, was born in 1847 in this city. Which city is it? → Edinburgh
- georgians-and-victorians-11: duplicate like q-4128: This painter often showed faces from the front and the side at the same time. In which country was he born? → Spain: This London square is named after Nelson's most famous sea battle, fought in 1805. Off which country's coast was the battle fought? → Spain
- georgians-and-victorians-12: duplicate like q-3651: Many reusable shopping bags like this one are made from which plant? → Cotton: Hundreds of mills like this one turned Manchester into a Victorian boom town. Which material did they spin and weave? → Cotton
- georgians-and-victorians-17: overlap like q-1289: Fui enfermera en la guerra de Crimea, recorría el hospital de noche con una lámpara y fundé la enfermería moderna. ¿Quién soy? → Florence Nightingale: This nurse was nicknamed “the Lady with the Lamp” for her night rounds in the Crimean War. Who did she look after? → Wounded soldiers
- london-6: overlap like q-18317: I'm a Yeoman Warder at the Tower of London. Each day I feed my feathered charges raw meat and tuck them into their night pens. Who am I? → The Ravenmaster: He's a Yeoman Warder, he feeds his birds raw meat, and he makes sure at least six of them always live at the Tower of London. What is his job title? → Ravenmaster
- london-11: overlap like q-18252: Britain's top government ministers usually meet around this table every week. In which building is this room? → 10 Downing Street: Who lives and works behind this famous black door in London? → The Prime Minister
- london-15: overlap like q-17932: I'm a London street full of jewellers and designer shops. On the British Monopoly board I'm green, with Oxford Street and Regent Street. What am I? → Bond Street: On a British Monopoly board, which property comes right after Oxford Street? → Bond Street
- london-16: overlap like q-18304: The tall black hats of the King's Guard are named after the animal whose fur they are made from. Which animal? → Bear: You're watching the Changing of the Guard at Buckingham Palace. The guards' tall furry hats are called bearskins. What are they made from? → Real bear fur
- nursery-rhymes-and-singalongs-14: overlap like q-5389: In the song “The Wheels on the Bus”, which of these is NOT part of the bus? → The sails go flap, flap, flap: On the bus, the wheels go round and round, the horn goes “beep, beep, beep” and the babies go “wah, wah, wah”. What do the wipers go? → Swish, swish, swish
- pioneers-and-heroes-2: overlap like q-5501: Seven-time F1 champion Lewis Hamilton started racing when he was 8. What did he race first? → Go-karts: Who is this British racing driver, a seven-time Formula One world champion? → Lewis Hamilton
- pioneers-and-heroes-10: overlap like q-9672: Which member of Captain Scott's South Pole expedition said “I am just going outside and may be some time”? → Lawrence Oates: Captain Scott's team dragged sledges for months, got there on 17 January 1912, and found a Norwegian tent already waiting. Where were they? → The South Pole
- pioneers-and-heroes-17: overlap like q-18024: After London 2012, Royal Mail painted a postbox gold in Dunblane, Scotland, to celebrate a local champion. Who was it? → Andy Murray: Who is the only tennis player ever to win two Olympic gold medals in singles? → Andy Murray
- accents-and-dialects-13: overlap like q-9736: Westminster is named after the “minster” that stood west of the City of London. Complete it: a minster is a big… → Church: On a walk in Scotland you pass a loch, then a kirk. Loch is to lake as kirk is to… → Church
- wildlife-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: These little white flowers pop up in British gardens early in the year. Their name says each one looks like a drop of what? → Snow
- cakes-puddings-and-biscuits-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: I'm a soft, fruity sweet in bright colours, shaped like a tiny chubby person, and Doctor Who offered me to everyone he met. What am I? → Jelly Babies
- cakes-puddings-and-biscuits-17: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: It's a Cadbury bar in a purple wrapper, made near Birmingham, and the wrapper shows a glass and a half of something pouring in. What is it? → Milk
- childrens-tv-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: How many Alphablocks are there in the TV show Alphablocks? → 26
- christmas-in-britain-7: overlap like georgians-and-victorians-7: At Christmas dinner, two people pull one of these until it goes bang. What do you usually find inside? → A paper crown, a joke and a little toy: You pull a Christmas cracker at the dinner table. Which of these do you NOT usually find inside? → A mince pie
- christmas-in-britain-17: overlap like q-9530: Mince pies are little pastry pies eaten at Christmas, and many children leave one out for Father Christmas. What's inside a mince pie today? → Sweet dried fruit and spices: It goes inside the pies left out for Father Christmas, it's made of dried fruit, spices and sugar, and it comes in a jar. What is it called? → Mincemeat
- counties-and-regions-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which English county is highlighted on this map? → Cumbria
- counties-and-regions-8: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: These white chalk cliffs on the Sussex coast are known as the “Sisters”. How many Sisters are in their name? → Seven
- counties-and-regions-14: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In Ashbourne's Shrovetide football, the goals are about 3 miles apart and hundreds play at once. Who are the “Up'ards” and the “Down'ards”? → The two teams of players
- drinks-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which old English phrase means “have a drink”, appears in Chaucer's “Canterbury Tales”, and uses an old jokey word for mouth or throat? → Wet your whistle
- drinks-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Thatchers has made cider in Sandford, Somerset, since 1904, and one of its ciders is called Katy. What is Katy? → A variety of apple
- flags-and-emblems-4: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: It's on Liverpool FC's crest and the city's coat of arms, and two giant copies sit on top of a famous building by the River Mersey. What kind of creature is it? → A bird
- flags-and-emblems-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: This club's badge shows a ship and a little figure holding a trident. It plays at Old Trafford, and Sir Alex Ferguson managed it. What's its nickname? → The Red Devils
- game-shows-and-presenters-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Anne Hegerty is one of the Chasers on The Chase. What is her nickname? → The Governess
- game-shows-and-presenters-17: hard fail: correct 4, unambiguous 3, no_giveaway 5, no_overlap 5: Who hosted ITV's Take Your Pick!, where players had to answer questions for a minute without saying “yes” or “no”? → Michael Miles
- pub-and-playground-games-7: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: These cards are from Happy Families. What are you trying to collect when you play it? → Every member of one family
- pub-and-playground-games-11: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: You and a friend stand on opposite pavements and take turns throwing a ball at the edge of the pavement across the road. What's the game called? → Kerby
- rugby-and-cricket-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In T20 cricket, Sussex is to the Sharks as Kent is to the… → Spitfires
- transport-6: overlap like q-6612: Red buses with two floors like this one are a famous sight in which city? → London: Horses pulled my great-great-grandparents. Now I'm red, I have stairs inside, and you can ride upstairs to see London. What am I? → A double-decker bus
- tudors-and-stuarts-17: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In London's Great Plague of 1665, a red cross painted on a door was a warning. Who was inside? → People with the plague
- twentieth-century-0: overlap like q-4084: You're a child putting on a gas mask made to look like Mickey Mouse's face. During which war are you? → World War II: In 1939, everyone in Britain, even children, was given a mask in a cardboard box to carry. What was it meant to protect them from? → Poison gas
- rugby-and-cricket-1: overlap like q-5943: In 2003, this fly-half won the Rugby World Cup final with a drop goal in the last minute of extra time. Who is he? → Jonny Wilkinson: You're watching Jonny Wilkinson's 2003 World Cup drop goal sail between the posts. How many points does it add to England's score? → 3
- rugby-and-cricket-3: overlap like q-2065: En rugby, llevan los números del 1 al 8, forman el scrum y entre ellos están los pilares y el talonador. ¿Cómo se llama este grupo? → Delanteros: Look at this rugby restart. Which group of players usually lines up and jumps for the ball? → The forwards
- rugby-and-cricket-17: overlap like q-6609: In Britain, people drink it hot, often with a splash of milk, at an afternoon time with little sandwiches and cakes. What drink is it? → Tea: In a Saturday village cricket match, players stop between innings, head to the pavilion and eat sandwiches and cake. What is this break called? → Tea
- school-and-childhood-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: I sing songs, read stories and help toddlers with their coats, before they're old enough for Reception. Who am I? → A nursery teacher
- school-and-childhood-7: overlap like q-18073: I come in a crinkly bag, I'm thin slices of fried potato, and Americans call me chips. What do Brits call me? → Crisps: A classic British packed lunch has a sandwich, an apple and a small bag of thin, salty, crunchy potato slices. What are they called? → Crisps
- sporting-events-0: overlap like q-18024: After London 2012, Royal Mail painted a postbox gold in Dunblane, Scotland, to celebrate a local champion. Who was it? → Andy Murray: I'm usually red and I stand on British pavements. In 2012, over 100 of me were painted gold to honour Olympic and Paralympic champions. What am I? → A postbox
- sporting-events-7: overlap like q-6559: Look at this tennis court. What is its surface made of? → Grass: Which Grand Slam tennis tournament is played on grass courts like this one? → Wimbledon
- sporting-events-13: overlap like q-4749: In 2013, this player became the first British man in 77 years to win the Wimbledon singles title. Who is he? → Andy Murray: This is Wimbledon's Centre Court. In 2013, who became the first British man in 77 years to win the singles title here? → Andy Murray
- traditional-music-and-dance-3: overlap like q-9518: A Geordie comes from the city with this famous bridge. Which city is it? → Newcastle: Football fans in this city sing the old folk song “Blaydon Races”. The photo shows part of its most famous bridge. Which city is it? → Newcastle upon Tyne
- transport-4: overlap like q-18119: Britain's red-and-white L plates came in at the same time as the first driving test. In which decade was that? → The 1930s: You see this on the back of a car in Britain. Who is driving? → Someone learning to drive
- tudors-and-stuarts-2: overlap like q-5358: Henry VIII had six wives. Which of these names did NONE of them have? → Mary: British children learn a rhyme about the wives of Henry VIII, seen here: “Divorced, beheaded, died…”. How many wives did he have? → 6
- tudors-and-stuarts-5: overlap like q-18208: On Bonfire Night, a stuffed dummy like this one is put on top of the bonfire. Who is it named after? → Guy Fawkes: In Britain, fireworks like these light up the sky every 5 November. Whose failed plot are people remembering? → Guy Fawkes
- tudors-and-stuarts-15: overlap like q-18146: What do you call a roof like this one, made from straw or reeds? → Thatch: Roofs of straw or reeds like this cover many old English cottages. What is the person who makes them called? → A thatcher
- twentieth-century-15: overlap like q-17881: Which award do UK teenagers earn at Bronze, Silver and Gold levels by volunteering, learning a skill and going on an expedition? → The Duke of Edinburgh's Award: Each year, British teenagers hike, camp and volunteer to earn an award first set up in 1956. Which royal founded it? → Prince Philip
- twentieth-century-16: overlap like q-9810: To make people notice their fight for votes for women, Emmeline Pankhurst's suffragettes famously chained themselves to what? → Railings: The suffragette group led by this woman had the motto “Deeds not words”. Who is she? → Emmeline Pankhurst
- twentieth-century-17: overlap like q-18498: England fans sing it at every big tournament. It comes from a 1996 song for the Euros in England, and means football is going back where it was invented. What is it? → “It's coming home”: At England matches, fans sing “It's coming home”. The song was written for a football tournament England hosted in which year? → 1996
- wildlife-4: overlap like q-14082: Hör zu: Welcher Vogel singt hier im Garten? → Amsel: Look at this bright orange beak and the yellow ring round the eye. Which British garden bird is this? → Blackbird
- wildlife-5: duplicate like q-6581: This fan painted a flag on their face. Which country are they cheering for? → Japan: This fast-growing plant can push up through concrete, and British homebuyers dread finding it in the garden. From which country was it first brought to Britain? → Japan
