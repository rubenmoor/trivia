# batch-65

Made by `qgen batch` on 2026-11-13 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): comedians-and-panel-shows, art-and-architecture, pub-and-playground-games, sporting-events, middle-ages, languages-of-britain, birds, customs-and-ceremonies, slang-and-words, wildlife, team-gb-and-olympians, holidays-and-celebrations, classic-dishes, traditional-music-and-dance, money-and-shopping, home-and-public-services, crown-and-state, drinks, writers-and-poets, regional-specialities, weather-and-seasons, parliament-and-prime-ministers, soaps-and-dramas, scientists-and-inventors, sitcoms, game-shows-and-presenters, plants-and-gardens, british-films
- Merged: 269 (q-18702…q-18970)
- Approved: 254
- Needs work: 15
- Dropped by the pipeline: 78
- Reviewed by: claude-opus-5-5
- Claude calls: 585, about $76.81 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-63, batch-64; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-63 | batch-64 | batch-65 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 370 | 363 | 347 |
| skipped slots |  | 134 | 141 | 157 |
| dropped |  | 89 | 82 | 78 |
| drop rate | ≤ 20.0 % | 24.1 % ✗ | 22.6 % ✗ | 22.5 % ✗ |
| dropped: hard fail correct |  | 1 | 1 | 1 |
| dropped: hard fail unambiguous |  | 0 | 2 | 1 |
| dropped: hard fail no_giveaway |  | 21 | 17 | 19 |
| dropped: overlap |  | 65 | 60 | 56 |
| dropped: duplicate |  | 3 | 3 | 1 |
| dropped: fact-check wrong |  | 0 | 0 | 1 |
| merged |  | 281 | 281 | 269 |
| approved |  | 268 | 268 | 254 |
| needs_work |  | 13 | 13 | 15 |
| needs_work rate | ≤ 20.0 % | 4.6 % ✓ | 4.6 % ✓ | 5.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.8 % ✓ | 2.5 % ✓ | 1.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.4 % ✓ | 0.4 % ✓ | 0.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.1 % ✗ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 1.1 % ✓ | 1.8 % ✓ | 3.3 % ✓ |
| media: no pick in review 1 |  | 25 | 30 | 37 |
| media: recovered by research |  | 22 | 26 | 28 |
| media: no pick at record |  | 3 | 4 | 9 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.4 % ✓ | 0.4 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 19.2 % ✓ | 17.9 % ✓ | 17.0 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 69.7 % ✓ | 68.0 % ✓ | 69.2 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.10 ✓ | 1.10 ✓ | 1.37 ✓ |
| approved 11–15 |  | 62 | 57 | 61 |
| top move | ≤ 25.0 % | 19.2 % ✓ | 14.6 % ✓ | 14.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 73.3 % | 81.9 % | 76.2 % |
| values stimulus |  | 4 | 4 | 5 |
| top clue | ≤ 60.0 % | 49.8 % ✓ | 42.0 % ✓ | 46.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 20.3 % ✓ | 26.3 % ✓ | 23.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 21.7 % ✓ | 16.7 % ✓ | 21.2 % ✓ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 26.7 % ✓ | 18.1 % ✓ | 23.8 % ✓ |
| mean fun | ≥ 3.40 | 3.66 ✓ | 3.62 ✓ | 3.63 ✓ |
| cost $ |  | $75.29 | $76.96 | $73.36 |
| $ per approved | ≤ $0.35 | $0.28 ✓ | $0.29 ✓ | $0.29 ✓ |
| calls |  | 534 | 548 | 525 |
| calls per approved |  | 1.99 | 2.04 | 2.07 |
| wall time h |  | 2.29 | 2.34 | 2.34 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 3 of 57 (5 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 10 (3 major), fact 2 (0 major), overlap 1 (0 major), media 3 (1 major), difficulty 2 (2 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.44

Major findings on approved questions:

- **q-18834**: giveaway, difficulty — The question says the nests are under the eaves "of British houses", and the answer is "House martin". That word match gives the answer away to anyone who doesn't know birds, and it does the same job as hint 3 ("Its name tells you where it likes to live"). Rewording to "under the eaves" alone would fix it. As written it plays at about 4, not 7. The rest checks out: the Commons file shows house martin chicks in a nest under the eaves at Sea Mills station, so the essential image is correct. The fun fact (about 1,000 beakfuls of mud) matches common sources. Swift, starling and wren don't build mud nests, so they are clearly wrong, and no related question overlaps (the swift and swallow questions ask different things). (http://127.0.0.1:8001/review/q-18834)
- **q-18924**: giveaway, difficulty — The facts check out: Julia Smith and Tony Holland based the set on Fassett Square in Dalston, and it was built at BBC Elstree in Borehamwood. The problem is that the question says "based me on a Victorian square", and Albert Square is the only option that is a square. The others are a Close, a Street and a Street, so the wording gives the answer away without any soap knowledge, and the difficulty should be about 6, not 12. Rewording the setting as "a Victorian street layout" or similar would fix it. (http://127.0.0.1:8001/review/q-18924)
- **q-18935**: media, giveaway — The essential image ("Mo Farah doing the Mobot at the Olympic Victory Parade") shows Farah himself, and its title names him. A question about who made the celebration famous is then answered by his face. The image should show the Mobot done by someone else, such as a fan or a child. Hint 2 ("the first letter of his first name", M) also rules out all three wrong options, which is a minor giveaway. The facts check out: the Mobot became famous at London 2012, Farah and Bolt swapped celebrations there, and Mo is short for Mohamed. (http://127.0.0.1:8001/review/q-18935)

## Needs work

- **q-18703** (art-and-architecture) This bronze statue in Parliament Square, London, faces the Houses of Parliament. Who does it show? → Winston Churchill: None of the six candidates shows the Churchill statue in Parliament Square. They show a Buddha head, the Statue of Liberty, an Egyptian head, a Roman woman, the Matija Gubec bust and a wooden saint. The question needs that statue as essential media, and no new search is allowed. A side note for the rework: Lloyd George, Peel and Disraeli also have statues in Parliament Square, so the image has to do the identifying work. Check that the clue "faces the Houses of Parliament" really fits only Churchill. No suitable picture found for this question.
- **q-18752** (customs-and-ceremonies) In the playground, when do children secretly cross their fingers behind their back? → When telling a fib: Hint 1 ("It's a secret they keep from the person they're talking to") already describes deceiving the listener. It rules out sneezing and the bell, and points straight to the fib, so it gives the answer away. Replace it with a vague hint, for example one about it being an old playground custom or a gesture that "cancels" something.
- **q-18766** (game-shows-and-presenters) Victoria Coren Mitchell's BBC quiz Only Connect ends with a fast buzzer round. It's called “Missing …” what? → Vowels: The text is fine, but none of the image candidates fits. They show a wasp on a flower, a Japanese bus stop-request button and bare electronic buzzer parts, not a quiz-show buzzer or studio. A new search (e.g. "quiz show buzzer" or "game show podium") is needed, but this run can't search again. No suitable picture found for this question.
- **q-18774** (holidays-and-celebrations) Look at this close-up. In Britain, what do people often call this jolly man, besides Santa Claus? → Father Christmas: Overlaps approved q-18207 (mince pie and sherry left out for Father Christmas) and q-18575 (The Snowman meets Father Christmas). Both reveal “Father Christmas” as the British Christmas gift-bringer, which is all this question asks. Seeing either one gives this one away, and the close-up adds nothing because the question already names Santa Claus. I'd drop it or replace it with a different British Christmas fact.
- **q-18775** (holidays-and-celebrations) You're in a British park, watching rockets whoosh into the sky over a huge bonfire with a guy on top. Which month is it? → November: This repeats the fact in approved q-9795 (a guy burnt on a bonfire → 5 November). Here the clue is again the bonfire with a guy on top, and the answer is November. It also overlaps heavily with q-18208 (the Bonfire Night guy → Guy Fawkes) and q-18569 (parkin → 5 November). Whichever of these a player sees first gives away the others.
- **q-18777** (holidays-and-celebrations) Scottish men wear a kilt to weddings, on Burns Night and at Highland games, often with a sporran. What is a kilt? → A knee-length tartan skirt: Hint 1 (“You wear it around your waist.”) already gives the answer away: of the four options, only the skirt is worn around the waist. Hint 1 should be vague, for example about Scotland or the occasions, and the waist or skirt shape should come in hint 2 or 3 at the earliest.
- **q-18812** (parliament-and-prime-ministers) At a UK election count, a candidate pins on a badge like this one. Which party do they most likely stand for? → The Conservatives: No candidate shows a plain blue rosette, and a new search isn't possible. The question depends on that picture, so it needs a plain blue election-style rosette with no text, for example from the search "blue rosette award". No suitable picture found for this question.
- **q-18825** (pub-and-playground-games) The crowd waves cards for it, the caller roars it out, and it's the top score with three throws. Which game's maximum is “One hundred and eightyyy!”? → Darts: No candidate fits the decorative slot. The candidates are Sinterklaas, a Zwarte Piet figure on a fire engine (unsuitable for a family game), Victorian paintings of dockside and royal crowds, a WWI-era carriage photo and a satirical print. None of them shows the world of darts, and no new search is allowed. The text itself is fine. A new search such as "darts match crowd" or "darts oche" would probably work. No suitable picture found for this question.
- **q-18851** (drinks) Look at the photo: what is this traditional game, played in pub alleys in the West Country, called? → Skittles: None of the candidates works as the essential photo of a British pub skittle alley. Candidates 1 and 2 are drawings of German Kegeln, 3 and 4 are technical diagrams with German labels, 5 is a CGI render of red pins on a chessboard (not a photo, and not a pub), and 6 is an Eva Braun photo, which is unsuitable. Another search isn't allowed, so the slot needs a real photo of a pub skittle alley with its pins (for example "pub skittle alley"). No suitable picture found for this question.
- **q-18855** (holidays-and-celebrations) Carol singers go from door to door, often holding lanterns and collecting money for charity. What do they sing? → Christmas songs: No candidate shows carol singers: 1–2 are pencil sketches of Japanese lanterns, 3–4 are old photos of a crowd singing on a ship's deck, 5 is a carved pumpkin and 6 is an Indian concert stage. A new search isn't allowed. Separately, the question text more or less gives the answer away: “carol” already means a Christmas song, so the question names its own answer. It could ask about something else to do with carolling, or describe the singers without the word “carol”. No suitable picture found for this question.
- **q-18858** (home-and-public-services) Look at this British stamp marked “2nd”. What do you get with a second-class stamp instead of a first-class one? → Cheaper, slower delivery: No candidate shows the essential British stamp marked “2nd”, and a new search isn't allowed. Consider making the media illustrative (e.g. a British postbox or letters on a doormat), as the rater suggested, and rewording the question so it doesn't refer to "this stamp". No suitable picture found for this question.
- **q-18911** (slang-and-words) Which friendly British greeting is thought to come from squashing “how are you” into one quick word? → Hiya: Fact check: uncertain. The 'how are you' origin is only one theory (dictionaries often give 'hi' + 'you'). The fun fact about it being especially popular in northern England and Wales, and used dozens of times a day, can't be verified.
- **q-18925** (soaps-and-dramas) You're chatting with Dot Cotton in the Walford launderette. Which of these is she NOT known for? → Running the Queen Vic: Hint 2 ("The odd one out is a job Dot never had on the Square") gives away the answer: "Running the Queen Vic" is the only option that is a job, so the other three are ruled out. Hint 2 needs to be vaguer, e.g. about Dot's real launderette job or her long run on the show, without pointing at the job/habit/person difference between the options.
- **q-18926** (soaps-and-dramas) Huge, bright earrings like these were the trademark of which EastEnders character? → Pat Butcher: None of the media candidates shows earrings: #1 is a scan of a painted book plate from an 1895 ethnology report, and #2 and #3 are the same full-body bikini photo of a woman with a skateboard. The question says “earrings like these”, so it needs a clear close-up of big, bright costume earrings, and no new search is allowed. The slot could also be illustrative rather than essential, since the photo doesn't show Pat's own earrings. No suitable picture found for this question.
- **q-18927** (sporting-events) A darts caller roars “One hundred and eighty!” It's the top score you can get with three darts. What has the player hit? → Three treble 20s: None of the media candidates has anything to do with darts: an award ceremony, an archival photo of a woman holding sticks, and Marines grappling. A new search isn't allowed, so the slot needs a darts image, for example "darts player throwing" or "dartboard pub wall". The image must not show a dart landing in the treble 20. No suitable picture found for this question.

## Question axes

- move: analogy 3, cause_effect 11, count 8, estimate 8, identify 39, made_of 8, name_concept 33, odd_one_out 14, origin 24, purpose 21, record 8, sequence 10, when 24, who 32, word_meaning 26
- stimulus: detail 14, none 205, photo 48, sound 1, video 1
- clue: completion 11, direct 126, riddle 30, scenario 29, three_facts 73
- answer_kind: group 26, number 17, person 49, place 24, thing 63, time 27, word 63
- lens: body_senses 11, educational_media 30, everyday 26, history 55, language 57, nature 4, pop_culture 48, school 21, science_news 3, university 14

## Dropped by the pipeline

- birds-7: overlap like q-9553: Which birds do people in Britain count with the rhyme “One for sorrow, two for joy”? → Magpies: You spot magpies in the garden. In the old rhyme that starts “One for sorrow”, how many magpies are “for joy”? → Two
- birds-14: overlap like q-9553: Which birds do people in Britain count with the rhyme “One for sorrow, two for joy”? → Magpies: In parts of Britain, some people salute when they see a single bird like this one. Why do they do it? → To keep away bad luck
- british-films-0: overlap like q-0079: En Harry Potter, ¿a qué casa de Hogwarts pertenece Harry? → Gryffindor: Daniel Radcliffe played Harry Potter in all eight films. Which of these groups was Harry NEVER part of? → Slytherin house
- british-films-17: overlap like q-9752: Brunel designed it, Bristol launched it in 1843, and it was then the largest ship in the world, made of iron with a propeller. Which ship? → SS Great Britain: This English city has a famous suspension bridge, Brunel's ship SS Great Britain, and the studio that makes Wallace & Gromit's stop-motion films. Which city? → Bristol
- classic-dishes-1: overlap like q-9747: I'm a small green ball of leaves. I'm served with Christmas dinner in Britain, and many children push me to the side of their plate. What am I? → A Brussels sprout: Look at these vegetables growing on their stalk. Which city are they named after? → Brussels
- classic-dishes-12: overlap like q-9528: Which hot brown sauce is poured over a Sunday roast? → Gravy: Proper gravy like this is made from the juices left in the tin after cooking what? → Roast meat
- crown-and-state-3: overlap like q-5577: This country's national animal is the unicorn, its flag is a diagonal white cross on blue, and it's famous for bagpipes. Which country? → Scotland: On the royal coat of arms, the lion stands for England. Which part of the UK does this unicorn stand for? → Scotland
- crown-and-state-10: overlap like q-3228: I'm a London church. In 2011, Prince William and Catherine Middleton got married under my roof. Where am I? → Westminster Abbey: Prince William and Catherine married in this famous church in 2011. What is it called? → Westminster Abbey
- customs-and-ceremonies-1: overlap like q-14867: At many American weddings, a little girl walks down the aisle just before the bride, scattering something from a basket. What is it? → Flower petals: Guests throw it over newlyweds outside the church. Many British churches ban the paper kind. What natural kind do they often allow instead? → Dried flower petals
- customs-and-ceremonies-2: overlap like q-12332: Soy una caseta de feria llena de premios: compras un boleto, lo abres y, si te toca, te llevas un peluche o un jamón. ¿Qué soy? → La tómbola: You'll find a spinning drum like this one at British school fairs and village fetes. What is it for? → Mixing tickets for a prize draw
- customs-and-ceremonies-3: overlap like q-17923: You're at a Highland games as the MacDonalds march past in their own tartan. What do you call a big Scottish family group like theirs? → A clan: I'm a pattern of criss-crossing coloured stripes woven into wool. Scottish clans each have their own version of me, and you see me on kilts. What am I? → Tartan
- customs-and-ceremonies-4: overlap like q-7220: En el bautizo cargo al bebé junto a la pila de agua y prometo ayudar a cuidarlo toda la vida. ¿Quién soy? → El padrino: At a christening I stand by the font and make promises for the baby. Prince George has seven of me. Who am I? → A godparent
- drinks-15: overlap like q-4354: The Happy Meal comes in a small box with a toy inside. Who is it made for? → Children: It comes in a small bottle with a sports cap, it's fruity, and it's a lunchbox favourite. Who is Fruit Shoot made for? → Children
- game-shows-and-presenters-8: overlap like q-2678: In Big Brother, housemates go alone into a special room and sit in a big chair. What do they do there? → Talk to the cameras in private: On the UK's Big Brother, when Big Brother called a housemate in to talk alone, which room did they go to? → The Diary Room
- holidays-and-celebrations-9: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: On the early May bank holiday, children in some English villages dance around a pole like this. What do they weave as they dance? → Ribbons
- holidays-and-celebrations-11: overlap like q-5577: This country's national animal is the unicorn, its flag is a diagonal white cross on blue, and it's famous for bagpipes. Which country? → Scotland: Pipers play them at Highland games, at Hogmanay and to lead in the haggis on Burns Night. Which part of the UK are these bagpipes from? → Scotland
- holidays-and-celebrations-16: overlap like q-10037: En Pascua, muchos padrinos regalan una mona con huevos encima. ¿De qué suelen ser hoy esos huevos? → De chocolate: They're hidden around the garden on Easter Sunday, wrapped in shiny foil, and children race to find them. What are these little eggs made of? → Chocolate
- languages-of-britain-0: overlap like q-17890: Look at the dragon on this flag. How many legs does it have? → 4: Welsh rugby fans wave it, it stands on a green and white background, and in Welsh it's called “Y Ddraig Goch”. What is it? → A red dragon
- languages-of-britain-5: overlap like q-9540: What is the highest mountain in the United Kingdom? → Ben Nevis: Its name starts with the Gaelic word for mountain, it rises to 1,345 m (4,413 ft), and it's the highest peak in the UK. What is it? → Ben Nevis
- middle-ages-6: overlap like q-1440: ¿Qué pueblo navegaba en drakares, barcos largos con una cabeza de dragón en la proa? → Los vikingos: In 793, raiders sailed boats like this to attack the island monastery of Lindisfarne. Who were they? → The Vikings
- middle-ages-10: overlap like q-1118: Soy un santo muy famoso de Irlanda. Cuenta la leyenda que usaba un trébol de tres hojas para enseñar, y en mi día, el 17 de marzo, medio mundo se viste de verde. ¿Quién soy? → San Patricio: You're pinning a shamrock to your coat on 17 March. Legend says Saint Patrick used its three leaves to explain what? → The Holy Trinity
- middle-ages-13: overlap like q-18483: In 1066, near Hastings, English foot soldiers stood behind a wall of shields. Which army charged them with knights on horses and archers? → The Normans: In 1066, William the Conqueror crossed the Channel and took the English crown. Which region of France did he rule? → Normandy
- middle-ages-17: overlap like q-9570: On 1 March, many people pin a daffodil or a leek to their coat, and children may dress up in tall black hats. Which day is it? → St David's Day: On which date does Wales celebrate Saint David's Day? → 1 March
- money-and-shopping-1: overlap like q-3883: In a famous children's book, a mother rabbit gives her naughty son chamomile tea at bedtime. Who is he? → Peter Rabbit: I wear a blue jacket, I sneak into Mr McGregor's garden, and in 2016 I hopped onto British 50p coins. Who am I? → Peter Rabbit
- money-and-shopping-15: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: When Poundland opened in 1990, how much did everything in the shop cost? → £1
- parliament-and-prime-ministers-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This famous black door has no keyhole on the outside. Whose official home is behind it? → The Prime Minister
- parliament-and-prime-ministers-8: overlap like q-18674: You're walking past the Houses of Parliament and see a bronze Oliver Cromwell holding a sword and a Bible. When was this statue put up? → The 19th century: I stand in bronze outside Westminster Hall, with a sword, a Bible and a lion at my feet. In life, I fought a king and threw MPs out of the Commons. Who am I? → Oliver Cromwell
- plants-and-gardens-4: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: At village May Day fairs, children dance around this, weaving the ribbons together. What is it called? → A maypole
- plants-and-gardens-8: overlap like q-18701: Flowers like these bloomed on First World War battlefields and inspired the poppies Britons wear in November. In which region were those fields? → Flanders: Britons wear paper poppies like this every November. Poppies became a symbol after blooming on the battlefields of which war? → The First World War
- plants-and-gardens-12: overlap like q-9570: On 1 March, many people pin a daffodil or a leek to their coat, and children may dress up in tall black hats. Which day is it? → St David's Day: On 1 March, Welsh children pin this flower to their clothes. Whose saint's day is it? → Saint David
- regional-specialities-4: overlap like q-13186: Früher bekamen Kinder auf dem Land im Herbst schulfrei, um bei dieser Ernte zu helfen. Was wird hier geerntet? → Kartoffeln: In Scotland, tatties are dug up in autumn, boiled, and often mashed. Children once got “tattie holidays” to help pick them. What are tatties? → Potatoes
- regional-specialities-5: overlap like game-shows-and-presenters-12: I'm a Celebrity is filmed in the Australian jungle, and stars do Bushtucker Trials to win stars for camp. In Australian slang, what is “tucker”? → Food: You're in Liverpool and a café sign says “Best scran in town”. What is it selling? → Food
- regional-specialities-6: overlap like q-16856: In much of the US it's called “soda,” in the Midwest it's “pop,” and in parts of the South even “coke.” What do these words mean? → A sweet, fizzy drink: In Yorkshire it's called “pop”, and in Glasgow the same thing is called “ginger”, even when it's cola. What is it? → A fizzy drink
- regional-specialities-11: overlap like q-17899: Which English city's football club is nicknamed after this animal? → Leicester: This orange cheese from the East Midlands is a sandwich favourite. Its name is “Red …” what? → Leicester
- regional-specialities-15: overlap like q-2950: Ancient royal purple dye was made from the animal whose shell you see here. What kind of animal is it? → Sea snail: Whelks like these are sold in pots with vinegar at British seaside stalls. What kind of animal is a whelk? → A sea snail
- birds-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which small black-and-white bird dashes across car parks chasing flies, pumping its long tail up and down? → Pied wagtail
- crown-and-state-0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: It was made for William IV in 1831 and has a large sapphire topped with a cross of rubies. The monarch wears it at the coronation. What is it? → The Sovereign's Ring
- crown-and-state-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: At the Changing of the Guard, one Foot Guards regiment has a leek as its cap badge. Which one? → The Welsh Guards
- game-shows-and-presenters-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: On Who Wants to Be a Millionaire?, which lifeline makes the computer take away two wrong answers? → 50:50
- game-shows-and-presenters-4: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: The questions on Lee Mack's ITV quiz The 1% Club aren't about knowing facts. What do they test instead? → Logic and common sense
- home-and-public-services-11: fact-check wrong: The text is correct, but the image query (red double-decker bus London) does not show a bollard.: On British streets you'll often see bollards. What is a bollard? → A short, thick post
- money-and-shopping-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Britain's £2 coin is made of two different metals that look different. What does it look like? → Silver middle, gold ring
- pub-and-playground-games-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I'm a funfair stall. Little yellow plastic birds float round and round in my water, and you fish one out with a pole to win a prize. What am I? → Hook-a-duck
- regional-specialities-12: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Teisen lap means “moist cake” in Welsh. Coal miners carried it to work because it didn't crumble. Which area is it most linked to? → The South Wales Valleys
- regional-specialities-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It's green, poured over pie and mash in London's East End, and made with parsley and the water eels were stewed in. What's it called? → Liquor
- soaps-and-dramas-5: hard fail: correct 3, unambiguous 5, no_giveaway 5, no_overlap 5: You pop into Rita Tanner's newsagent on Coronation Street for a paper and some sweets. What is the shop called? → The Kabin
- sporting-events-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: What is the name of the most famous court at Wimbledon, where the singles finals are played? → Centre Court
- weather-and-seasons-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: At the end of Raymond Briggs's “The Snowman”, the boy runs outside in the morning. What has happened to his snowman? → It has melted
- weather-and-seasons-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: You rub it on before a day at the beach and put more on after a swim. What is it for? → Stopping sunburn
- weather-and-seasons-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: What do Britons call this little pool that children splash about in on hot days? → A paddling pool
- weather-and-seasons-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This painter loved London's thick fog and painted the Houses of Parliament in it again and again. Who was he? → Claude Monet
- weather-and-seasons-14: overlap like q-18695: Who was Prime Minister when the Great Smog covered London in December 1952? → Winston Churchill: What thick, dirty fog brought London to a standstill for five days in December 1952? → The Great Smog
- wildlife-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In “The Gruffalo”, which animal invites the mouse to tea in its treetop house? → Owl
- wildlife-3: hard fail: correct 5, unambiguous 3, no_giveaway 3, no_overlap 5: Listen: which insect is buzzing round the flowers in this British garden? → Bumblebee
- wildlife-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: How many arms does the common starfish, found in British rock pools, usually have? → 5
- scientists-and-inventors-4: overlap like q-2321: Drivers see me on dark roads, and I'm named after the way a cat's eyes look at night. People call me a “cat's eye”. What am I? → A road reflector: I sit in the middle of the road. At night I shine back when headlights hit me. A man from Halifax invented me in 1934. What am I? → Cat's eyes
- scientists-and-inventors-5: overlap like q-18250: Barclays opened the world's first cash machine in 1967, and the comedy actor Reg Varney was the first to use it. In which city was it? → London: The world's first one opened in 1967 outside a Barclays bank in Enfield, London. A comedy actor used it first, and it gave out £10 at a time. What is it? → A cash machine
- scientists-and-inventors-9: overlap like q-4101: In 1960 in Tanzania, these apes were seen stripping twigs to fish for termites: the first wild animals seen making tools. Which apes? → Chimpanzees: In Gombe, Tanzania, Jane Goodall saw chimpanzees poking grass stems into mounds. What were they doing? → Fishing for termites
- scientists-and-inventors-12: overlap like q-1957: Antes de la manzana mordida, el primer logo de Apple, de 1976, mostraba a un científico sentado bajo un árbol. ¿Quién era? → Isaac Newton: Which scientist is said to have thought up his idea of gravity after seeing an apple like this fall from a tree? → Isaac Newton
- sitcoms-6: overlap like q-6741: He hardly says a word, drives a little green car and carries a teddy bear everywhere. Which country does Mr. Bean come from? → United Kingdom: Which TV character has a scruffy little brown teddy bear called Teddy as his best friend? → Mr Bean
- slang-and-words-4: overlap like q-13914: I wear a hairnet and gloves, and every day at noon I scoop food onto trays in the school cafeteria. Who am I? → The lunch lady: A “dinner lady” works in a British school. She isn't a teacher, and her busiest time is the middle of the day. What does she do? → Serves the school lunches
- slang-and-words-5: overlap like q-18347: Many British towns have a shop that smells of vinegar, gets busy on Friday nights and wraps food in paper. What is its most famous meal? → Fish and chips: Brits queue there on a Friday night, it smells of vinegar, and it wraps your supper in paper. What do they call it? → The chippy
- sporting-events-2: overlap like q-18098: Flicking through tennis record books: Rafael Nadal is to the French Open as Martina Navratilova is to which tournament? → Wimbledon: The Venus Rosewater Dish goes to Wimbledon's women's singles champion. Who has won it the most times? → Martina Navratilova
- sporting-events-8: overlap like q-0666: Soy redondo y pesado, y cada año me lanzan colina abajo en Cooper's Hill, Inglaterra, mientras decenas de valientes ruedan detrás de mí para atraparme. ¿De qué estoy hecho? → Queso: I take place on a very steep hill in Gloucestershire every spring. People tumble downhill after a big round prize and the winner keeps it. What am I? → Cheese rolling
- team-gb-and-olympians-6: overlap like q-9809: Eddie the Eagle became a hero at the 1988 Calgary Olympics despite finishing last in ski jumping. What did the “Eddie the Eagle rule” then require? → Minimum qualifying results to compete: I'm from Cheltenham, I wore thick glasses, and I was Britain's only ski jumper at the 1988 Winter Olympics in Calgary. Who am I? → Eddie “the Eagle” Edwards
- team-gb-and-olympians-14: overlap like q-3542: This object slides across the ice in a Winter Olympics sport. What is it mostly made of? → Granite: Team GB's curlers slide stones made from Scottish granite. Roughly how heavy is one stone? → 20 kg
- traditional-music-and-dance-2: overlap like q-4061: You're watching the Eurovision Song Contest when Irish dancers with still arms and flying feet start Riverdance. Which decade is it? → The 1990s: This dance show began as a seven-minute interval act at Eurovision in 1994. In which city was it first performed? → Dublin
- traditional-music-and-dance-5: overlap like q-5610: This big metal disc is struck with a soft mallet. Which instrument family does it belong to? → Percussion instruments: In a folk session in a pub, a player holds two spoons back to back and taps them on their knee and hand. What kind of instrument does that make them? → Percussion
- traditional-music-and-dance-6: overlap like plants-and-gardens-4: At village May Day fairs, children dance around this, weaving the ribbons together. What is it called? → A maypole: Children dance round a tall pole with ribbons, a girl is crowned queen, and there's a bank holiday that week. Which celebration is it? → May Day
- traditional-music-and-dance-10: duplicate like q-11979: In diesem Stadion spielten 2013 Bayern und Dortmund das Champions-League-Finale gegeneinander. In welcher Stadt steht es? → London: Folk-rock band Mumford & Sons, pictured here, formed in 2007. In which city? → London
- traditional-music-and-dance-11: overlap like q-18488: I'm a soldier saint on a white horse. My red cross flies over England, and in old tales I beat a fire-breathing beast. Who am I? → St George: Every Good Friday in Heptonstall, I lead an old Easter folk play. I boast loudly, take on Bold Slasher and the Black Prince of Paradine, and win. Who am I? → Saint George
- weather-and-seasons-3: overlap like q-9552: An old British saying starts “Red sky at night…”, about a sunset like this one. Whose delight is it? → Shepherds': According to the old British saying, a red sky like this at night is the delight of whom? → A shepherd
- weather-and-seasons-9: overlap like q-9783: Buy a “99” from an ice cream van and you get soft whippy ice cream in a cone. What is pushed into the top? → A Flake: Britons buy a cone with a chocolate Flake stuck in it from the ice cream van. Which number is in its name? → 99
- wildlife-13: overlap like q-9828: In which season are British garden ponds full of frogspawn and wriggling tadpoles? → Spring: I float in a pond in spring as a big clump of jelly, with a black dot in every little ball. Soon tadpoles wriggle out of me. What am I? → Frogspawn
- writers-and-poets-1: overlap like q-4340: Narnia is to a wardrobe as the Land of Oz is to a… → Tornado: You want to reach Narnia just like Lucy does. Which piece of furniture do you climb into? → A wardrobe
- writers-and-poets-5: overlap like q-1389: Ando descalzo con pies grandes y peludos, y vivo en un agujero redondo bajo una colina. ¿De qué tierra soy? → La Comarca: It's green and peaceful, its hobbit homes have round doors, and Frodo and Sam set off from it in “The Lord of the Rings”. What is it called? → The Shire
- writers-and-poets-11: overlap like q-18582: At which London station does Harry Potter find Platform Nine and Three-Quarters? → King's Cross: I'm a busy London railway station. J.K. Rowling's parents met on a train leaving me, and she hid a magic platform between my platforms 9 and 10. What am I? → King's Cross
- writers-and-poets-14: overlap like q-2515: What did English speakers, pirates included, call this Spanish silver coin? → Piece of eight: In “Treasure Island”, Long John Silver's parrot Captain Flint keeps screeching “Pieces of…!” What? → Eight
