# batch-70

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, counties-and-regions, landmarks-and-castles, early-britain, middle-ages, twentieth-century, regional-specialities, customs-and-ceremonies, legendary-heroes, pop-and-rock, traditional-music-and-dance, soaps-and-dramas, game-shows-and-presenters, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, team-gb-and-olympians, sporting-events, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, transport, crown-and-state, london, rivers-coasts-and-islands, hills-moors-and-national-parks
- Merged: 123 (q-19846…q-19968)
- Approved: 111
- Needs work: 12
- Dropped by the pipeline: 68
- Reviewed by: claude-opus-5-5
- Claude calls: 347, about $43.77 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-68, batch-69; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-68 | batch-69 | batch-70 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 304 | 264 | 191 |
| skipped slots |  | 200 | 240 | 313 |
| dropped |  | 98 | 77 | 68 |
| drop rate | ≤ 20.0 % | 32.2 % ✗ | 29.2 % ✗ | 35.6 % ✗ |
| dropped: hard fail correct |  | 1 | 1 | 2 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 22 | 8 | 12 |
| dropped: overlap |  | 70 | 64 | 50 |
| dropped: duplicate |  | 4 | 2 | 3 |
| dropped: fact-check wrong |  | 1 | 2 | 1 |
| merged |  | 206 | 187 | 123 |
| approved |  | 186 | 175 | 111 |
| needs_work |  | 20 | 12 | 12 |
| needs_work rate | ≤ 20.0 % | 9.7 % ✓ | 6.4 % ✓ | 9.8 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.9 % ✓ | 1.1 % ✓ | 4.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.5 % ✓ | 1.1 % ✓ | 1.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 1.6 % ✗ | 1.6 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.9 % ✓ | 3.7 % ✓ | 3.3 % ✓ |
| media: no pick in review 1 |  | 25 | 19 | 12 |
| media: recovered by research |  | 18 | 15 | 10 |
| media: no pick at record |  | 7 | 5 | 2 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 25.0 % ✗ | 26.1 % ✗ | 28.8 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 64.3 % ✓ | 64.1 % ✓ | n/a |
| max final−target gap 11–15 | ≤ 1.50 | 2.00 ✗ | 1.80 ✗ | n/a |
| approved 11–15 |  | 37 | 35 | 7 |
| top move | ≤ 25.0 % | 18.9 % ✓ | 17.1 % ✓ | 14.6 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 79.1 % | 80.2 % | 82.9 % |
| values stimulus |  | 3 | 5 | 5 |
| top clue | ≤ 60.0 % | 40.3 % ✓ | 40.1 % ✓ | 41.5 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 21.8 % ✓ | 25.1 % ✓ | 26.0 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 22.8 % ✓ | 21.9 % ✓ | 18.7 % ✓ |
| values lens |  | 9 | 10 | 9 |
| media share | 15.0 %–50.0 % | 20.9 % ✓ | 19.8 % ✓ | 17.1 % ✓ |
| mean fun | ≥ 3.40 | 3.55 ✓ | 3.48 ✓ | 3.43 ✓ |
| cost $ |  | $62.57 | $53.36 | $40.51 |
| $ per approved | ≤ $0.35 | $0.34 ✓ | $0.30 ✓ | $0.36 ✗ |
| calls |  | 426 | 381 | 287 |
| calls per approved |  | 2.29 | 2.18 | 2.59 |
| wall time h |  | 1.85 | 1.81 | 1.22 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 54 (2 %)
- Major among review needs work: 0 of 6 (0 %)
- Problems by kind: giveaway 11 (1 major), fact 2 (0 major), media 5 (1 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 53 of 60 (88 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.26

Major findings on approved questions:

- **q-19886**: media, giveaway — The media is a portrait of the answer ("File:Wordsworth portrait.png"), set as essential, so the file title names Wordsworth and the picture shows the person being asked about. A Dove Cottage or Grasmere image would work instead. The facts are correct: Wordsworth moved to Dove Cottage in December 1799, the Lyrical Ballads hint is right, and so is Dorothy's Grasmere Journal. There's no overlap with the related questions (the Wainwright question asks about a different person). (http://127.0.0.1:8001/review/q-19886)

## Needs work

- **q-19846** (accents-and-dialects) Someone says “bath” and “grass” with a short “a”, like in “cat”. Where in England are they most likely from? → The North: Hint 2 ("Think of Manchester, Leeds and Newcastle") gives the answer away. Those are three of the best-known cities in the North, so anyone who knows where they are can pick "The North" straight away. Hint 2 is also stronger than hint 3. Replace it with a vaguer hint (for example, about the famous "barth"/"bath" argument between regions), and keep naming northern cities for hint 3 at most.
- **q-19847** (accents-and-dialects) Who is most likely to tell you to “haud yer wheesht” when you're being too noisy? → A Scottish granny: None of the four image candidates fits: they are old book engravings of Margate sands, a park gateway and Guards ships at Portsmouth, nothing to do with hushing a noisy room or Scotland. No new search is allowed, so the media slot needs a new search by hand (for example "Scottish tenement kitchen" or "Scottish living room"). No suitable picture found for this question.
- **q-19864** (customs-and-ceremonies) Look at this outfit with a tailcoat, waistcoat and top hat. In Britain, what kind of event is it mostly worn to? → Formal daytime weddings: The picked picture has an unsuitable licence (pd-us-only: PD-1923, PD-US-expired).
- **q-19889** (london) Piccadilly Circus has no tents, no clowns and no acrobats. Its “circus” comes from a Latin word for which shape? → A circle: Hint 2 ("Think of how the buildings were first built to curve around the junction") gives the answer away: a curve fits only a circle, so it rules out square, triangle and star at once. Replace it with a vaguer hint, for example about the Roman origin of the word or about Roman chariot-racing tracks, without saying anything about curves or roundness.
- **q-19893** (london) You're in Trafalgar Square and spot only a few pigeons, though photos from the 1990s show thousands. Why are there so few now? → Feeding them was banned: The description's "company at lunchtime" points straight at food, so with only the four options it signals "Feeding them was banned" before any hint. Rewrite it to play on Nelson, the square or the pigeons without mentioning eating or meals, e.g. "Nelson's fan club has shrunk a lot since the 1990s."
- **q-19899** (accents-and-dialects) Complete the meaning: in Belfast, if a dinner “gives you the boke”, it makes you feel… → Sick: The description says Belfast's way of "reviewing your cooking" "isn't always kind". With only the four options in view, that marks the meal as bad, which rules out Sleepy, Hungry and Full and leaves only Sick. Rewrite it to play on Belfast slang or dinner time without saying whether the verdict is good or bad. For example: "Belfast has a word for this, and it's not on the menu." The rest of the question is fine: the fact is confirmed, it doesn't overlap q-18425 ("Bout ye?"), and candidate 1 works as the image.
- **q-19903** (cities-and-towns) You're watching Balamory. Which of these characters would you NOT meet there? → Postman Pat: The fun fact says Balamory was filmed in Tobermory on Mull, which is the answer to q-19157 (rater notes), so seeing this question gives that one away. Replace the fun fact with a different true Balamory fact, for example that the show had a 2025 revival or that each character lived in a house of their own colour. Everything else checks out.
- **q-19911** (football) I never kick the ball, but I pick the team and plan the tactics. Sir Alex Ferguson did my job at Manchester United for 26 years. What am I? → The manager: This question overlaps with approved q-18503, which asks “This Scottish manager won 13 league titles with the same English club. Who is he?” (answer: Sir Alex Ferguson). Each one gives the other away. q-18503 says “manager” about Ferguson, which answers this riddle. This riddle's clue (Ferguson did the job at Manchester United for 26 years) plus the fun fact (he managed Aberdeen in Scotland) all but answers q-18503. To fix it, the clue would need a different famous manager who doesn't appear in another question, or the question should be dropped.
- **q-19918** (pop-and-rock) This singer from Newcastle got his stage name from a striped jumper. Which creature did his bandleader say he looked like? → A bee: Hint 1 ("His stage name hints at what this creature can do") gives the answer away: once you link the name Sting to stinging, tiger, zebra and skunk are all ruled out, so only the bee is left. The media is also a giveaway: candidates 1–5 all show Sting, and once players recognise him the name leads straight to "bee". Candidate 6 is an unrelated 1901 Adelaide street scene, and no new search is allowed. Hint 1 needs to become a vague one (for example about the jazz-band era in the north-east of England), and the image slot should be decorative (for example "jazz band stage") so it doesn't show Sting. No suitable picture found for this question.
- **q-19931** (sporting-events) This person sits in a racing rowing boat but never rows. They steer and shout orders to the crew. What is their job called? → The cox: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-19949** (sayings-and-idioms) Grandparents say it instead of a rude word when things go wrong. It's also an old name for the bow used to play a violin. What is it? → Fiddlesticks: Fact check: wrong. Fun fact is wrong: Shakespeare's 'fiddlestick' is in Romeo and Juliet (Mercutio, 'Here's my fiddlestick', used of his sword), not Henry IV, Part 1. Answer and wrong answers are fine. (Checked from memory, not by search.)
- **q-19953** (soaps-and-dramas) Coronation Street fans call its famous road “the cobbles”, because it is paved with rounded… → Stones: The fun fact is wrong: the street set that opened in 2014 is at Trafford Wharf in Trafford, across the Manchester Ship Canal from MediaCityUK. It is not at MediaCityUK and not in Salford. Change it to: "In 2014 the outdoor street set moved to a new site at Trafford Wharf, near MediaCityUK, and the cobbles were rebuilt there." Fact check: wrong. Fun fact is inaccurate. The 2014 outdoor set moved to Trafford Wharf, next to but not in MediaCityUK, and Trafford Wharf is in Trafford, not Salford. Answer is fine. (Checked from memory, not by search.)

## Question axes

- move: analogy 1, cause_effect 8, count 6, estimate 9, identify 18, made_of 5, name_concept 16, odd_one_out 5, origin 12, purpose 4, record 4, sequence 2, when 8, who 8, word_meaning 17
- stimulus: detail 1, none 102, photo 18, sound 1, video 1
- clue: completion 7, direct 51, riddle 10, scenario 17, three_facts 38
- answer_kind: group 8, number 15, person 20, place 11, thing 28, time 9, word 32
- lens: body_senses 6, educational_media 13, everyday 23, history 21, language 23, nature 4, pop_culture 20, school 10, university 3

## Dropped by the pipeline

- accents-and-dialects-5: overlap like q-19733: In which country do people say “Bore da” to mean “good morning”? → Wales: “Iechyd da” means “good health”, people say it when they clink glasses, and it comes from the land with a red dragon on its flag. Where is that? → Wales
- accents-and-dialects-11: overlap like q-9736: Westminster is named after the “minster” that stood west of the City of London. Complete it: a minster is a big… → Church: In Scotland, a “kirk” often has a tall steeple and bells, couples get married there, and people sing hymns inside. What is a kirk? → A church
- accents-and-dialects-13: overlap like q-9542: This pastry with a crimped edge is named after which English county? → Cornwall: I'm at the far south-west tip of England, my pasties are famous, and here “proper job!” means “great work!”. Where am I? → Cornwall
- cities-and-towns-2: overlap like q-18086: Which pub did EastEnders' Kat Slater run with her husband Alfie Moon? → The Queen Vic: Coronation Street is to the Rovers Return as EastEnders is to… → The Queen Vic
- cities-and-towns-3: overlap like q-18987: In “Mary Poppins”, an old woman sits on the steps of St Paul's Cathedral selling little bags of crumbs for tuppence. Who eats the crumbs? → Birds: I have one of the world's biggest domes. I stood tall through the Blitz. In “Mary Poppins”, the Bird Woman feeds pigeons on my steps. What am I? → St Paul's Cathedral
- cities-and-towns-7: overlap like q-0218: Según una vieja leyenda, si cierto tipo de ave abandona la Torre de Londres, caerá el reino. ¿Qué aves viven por eso siempre en la Torre? → Cuervos: Legend says the kingdom will fall if these birds ever leave the Tower of London. What are they? → Ravens
- cities-and-towns-16: overlap like q-6172: This seaside palace in Brighton, England, looks like it came from India. Which royal had it built? → George IV: This palace in Brighton was built for the man who gave the Regency era its name. Who was he? → George IV
- crown-and-state-3: overlap like q-19304: Crowns like this one belong to the Crown Jewels. In which London building are they kept under guard? → The Tower of London: This building at the Tower of London has huge steel doors and guards outside. What is kept inside? → The Crown Jewels
- crown-and-state-14: overlap like q-18600: You're watching a coronation in Westminster Abbey. Who traditionally places the crown on the new monarch's head? → The Archbishop of Canterbury: At a coronation, who uses this golden spoon to anoint the new monarch with holy oil? → The Archbishop of Canterbury
- customs-and-ceremonies-11: overlap like q-18177: In Cambridge, people glide along the River Cam in these flat boats, pushed with a long pole. What are they called? → Punts: In Cambridge and Oxford, people go punting on the river, standing on a flat boat with a very long pole. What is the pole for? → Pushing against the riverbed to move the boat
- customs-and-ceremonies-13: overlap like q-9737: In the UK, who has the power to make someone a knight? → The King: In Britain, a king or another royal still taps people on the shoulders with a sword like this. What does it make them? → A knight
- customs-and-ceremonies-17: duplicate like q-2461: Look at this shaggy cow with long horns and a fringe over its eyes. Which country does this breed come from? → Scotland: This criss-cross patterned cloth is called tartan. Which part of the UK is it most famous for? → Scotland
- early-britain-1: overlap like q-16548: En México, el solsticio de verano es el día más largo del año. ¿Qué fecha es, más o menos? → El 21 de junio: Every June, thousands of people gather at Stonehenge to watch the Sun rise on the longest day of the year. What is that day called? → The summer solstice
- early-britain-2: overlap like q-19532: Viking raiders came to Britain over 1,000 years ago with a carved head like this one at the front. What was it fixed to? → A ship: Raiders sailing to Britain carved heads like this one on the front of what? → A Viking longship
- early-britain-8: overlap like q-18865: He became King of England in 1016, was a Danish Viking, and legend says he ordered the tide to stop. Which kingdoms made up his empire? → England, Denmark and Norway: In the 1020s, King Cnut ruled England, Denmark and Norway at the same time. What do historians call his realm? → The North Sea Empire
- early-britain-10: overlap like q-6127: I'm a picture made of thousands of tiny colored stones or glass tiles pressed into cement. The Romans put me on their floors. What am I? → A mosaic: This is part of a floor at Chedworth Roman Villa in Gloucestershire. What do you call a picture made from tiny stones like this? → A mosaic
- game-shows-and-presenters-5: overlap like q-19694: On Alexander Armstrong's Pointless, how much money is added to the jackpot each time nobody wins it? → £1,000: It's a right answer that scores zero, every player hopes for one, and none of the 100 people surveyed thought of it. What is it called on Alexander Armstrong's BBC quiz? → A pointless answer
- hills-moors-and-national-parks-0: overlap like q-19300: Ben Nevis, Ben Lomond and Ben Macdui all start with the same word. What does “Ben” mean in Scottish Gaelic? → Mountain: Tor, fell and ben are all words used in Britain for a hill or mountain. Which of these words is NOT? → Loch
- hills-moors-and-national-parks-3: overlap like q-18839: Which of these was NOT written by Agatha Christie? → The Hound of the Baskervilles: On a misty moor like this, a famous story is set where a giant ghostly dog scares a family. Which detective solves the case? → Sherlock Holmes
- hills-moors-and-national-parks-17: overlap like q-19565: This is Prince Philip, who started the Duke of Edinburgh's Award in 1956. Who is the award meant for? → Young people: I was married to Queen Elizabeth II for over 70 years, and in 1956 I started an award for young people named after my title. Who am I? → Prince Philip
- languages-of-britain-6: overlap like q-13177: Von welchem Tier stammt dieser Speck meistens? → Schwein: The bacon and sausages in a full English breakfast like this one usually come from which animal? → Pigs
- legendary-heroes-1: overlap like q-18241: In which century did the highwayman Dick Turpin hold up travellers on the roads of England? → The 18th century: Old legends tell of a fast black horse called Black Bess. Which highwayman was said to ride her? → Dick Turpin
- legendary-heroes-10: overlap like q-19270: This huge round table hangs on a wall in Winchester. In the legends, who sat around a round table so nobody sat at the head? → King Arthur's knights: This huge painted round table has hung in Winchester's Great Hall for centuries. Which legendary king's table was it made to be? → King Arthur
- london-4: overlap like q-1643: ¿En qué año fue coronado Carlos III en la abadía de Westminster? → 2023: In May 2023, King Charles III sat in an ancient wooden chair at Westminster Abbey and a crown was placed on his head. What is this ceremony called? → A coronation
- london-6: overlap like q-18538: Its trains run through round tunnels under London, its sign is a red circle with a blue bar, and you'll hear “Mind the gap”. What do Londoners call it? → The Tube: When a Tube train stops, a voice warns you about the space between the train and the platform: “Please mind the…” → Gap
- london-9: overlap like q-19821: On Christmas Eve, a boy sang “God rest ye merry, gentlemen” through my keyhole, and I grabbed a ruler to chase him off. That night, ghosts came to visit me. Who am I? → Ebenezer Scrooge: This picture comes from the first book of a famous London Christmas story. Which mean old man is visited by ghosts on Christmas Eve? → Ebenezer Scrooge
- london-11: overlap like q-17883: It's black, furry and about 45 cm tall, worn by the King's Guard outside Buckingham Palace. Why was the bearskin hat made so tall? → To make soldiers look taller: Guards at Buckingham Palace wear tall, furry black hats like this one. What are these hats called? → Bearskins
- london-12: overlap like q-6227: My hair is half black and half white, I drive a fast car, and I dream of a coat made of black-and-white spotted puppy fur. Who am I? → Cruella de Vil: Spotty puppies like these star in a story set in London. Which villain wants to make a fur coat out of them? → Cruella de Vil
- middle-ages-2: overlap like q-9727: This bronze archer stands below the walls of an English castle, not far from a famous forest. Who is he? → Robin Hood: You're watching a Robin Hood film, and the Sheriff of Nottingham locks Maid Marian in his castle. Who comes to rescue her? → Robin Hood
- money-and-shopping-16: overlap like q-18858: In the UK, what do you get with a second-class stamp instead of a first-class one? → Cheaper, slower delivery: It's a Royal Mail stamp with the King's head on it, it costs more than second class, and letters with it should arrive the next working day. What's it called? → First class
- regional-specialities-6: overlap like q-13177: Von welchem Tier stammt dieser Speck meistens? → Schwein: Wiltshire ham, like this, is a famous meat from the West Country. Which animal does it come from? → Pig
- regional-specialities-7: overlap like q-4874: This spiral fossil is an ammonite. Where did these animals live? → In the sea: Cornish sardines are small silver fish. Where are they caught? → In the sea
- regional-specialities-14: overlap like q-19122: In Lancashire, “Creamy”, “Tasty” and “Crumbly” are the three types of a local food, often eaten with an Eccles cake. What food? → Cheese: Caerphilly, like this, is a famous food from Wales. What kind of food is it? → Cheese
- accents-and-dialects-6: fact-check wrong: Hint 2 is false: a glottal stop is made in the throat (the glottis), not by the tongue behind the top teeth. That describes a normal T.: Linguists call it a “glottal stop”: many Britons swallow one letter in “bottle” and “water”. Which letter? → T
- accents-and-dialects-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Birmingham, people often say “babby”. What do they mean? → A baby
- accents-and-dialects-10: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: In Yorkshire, a tasty pie is “reyt good”. What does “reyt” mean? → Right
- comedians-and-panel-shows-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In which decade did Ken Dodd's song “Tears” spend five weeks at number one in the UK? → The 1960s
- comedians-and-panel-shows-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Little Britain, bored desk worker Carol Beer turns down every customer request. What is her catchphrase? → “Computer says no”
- early-britain-0: overlap like q-6322: In medieval Europe, riders in armor charged at each other with long lances in contests like this. Who were they? → Knights: In the old legends, Lancelot wore armour, rode a horse and swore to protect King Arthur's kingdom. What was he? → A knight
- football-5: overlap like q-18179: Wolverhampton Wanderers play in black and a colour fans call “old…”. Complete the colour. → Gold: Which West Midlands football club plays in old gold and black at a ground called Molineux? → Wolverhampton Wanderers
- london-2: overlap like q-18992: British Airways, which flew Concorde until 2003, is the UK's flag carrier. Which airport is its main home? → Heathrow: What is the busiest airport in the UK? → Heathrow
- london-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Hamleys first opened in London in 1760, now fills seven floors on Regent Street, and has staff blowing bubbles at the door. What does it sell? → Toys
- money-and-shopping-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Britain, people talk about “a fifty pee”. Two of them make a pound, and some show Peter Rabbit. What is a fifty pee? → A coin
- money-and-shopping-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This blue-green Bank of England note has Winston Churchill on the back. Which note is it? → The £5 note
- money-and-shopping-12: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: A British supermarket meal deal starts with a sandwich and crisps, like in the photo. What is the third item? → A drink
- money-and-shopping-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This British supermarket chain opened its first shop in 1970 and shares its name with an island country. What food is it best known for? → Frozen food
- regional-specialities-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: These little black sweets, called Pontefract cakes, come from Yorkshire. What flavour are they? → Liquorice
- rivers-coasts-and-islands-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: This cow's breed comes from the island of Guernsey. What do farmers mainly keep it for? → Its creamy milk
- sayings-and-idioms-4: hard fail: correct 2, unambiguous 4, no_giveaway 4, no_overlap 4: When a hard question has Brits “stumped”, the word comes from which sport? → Cricket
- sayings-and-idioms-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: If a Brit says you're “rabbiting on”, what are you doing? → Talking on and on
- sporting-events-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Ronnie O'Sullivan is to snooker as Phil “The Power” Taylor is to… → Darts
- rivers-coasts-and-islands-1: duplicate like q-18114: Folk dancers tie bells like these to their legs and jingle through village streets every May. Which country's tradition is this? → England: Look at this long, thin boat painted with roses and castles. In which country were boats like this first built for canals? → England
- rivers-coasts-and-islands-4: overlap like q-3785: The Panama Canal has locks with huge gates at both ends. What are canal locks for? → Raising and lowering boats: Look at these canal locks at Caen Hill in Wiltshire. What are canal locks for? → Lifting boats up and down hills
- rugby-and-cricket-1: duplicate like q-18205: This flag has the Union Jack in its corner and red stars with white borders. Which country's flag is it? → New Zealand: This team performs this war dance, the haka, facing its opponents before matches at Twickenham. Which country is it from? → New Zealand
- rugby-and-cricket-8: overlap like q-1880: El springbok, que da nombre a la selección sudafricana de rugby, salta de forma espectacular. ¿Hasta qué altura puede llegar? → Unos 2 metros: When the British and Irish Lions tour South Africa, they face this team, named after a leaping antelope and first to win four Rugby World Cups. What is it called? → The Springboks
- rugby-and-cricket-17: overlap like q-5945: It's in southwest London, fans call it “HQ”, and it's the largest stadium in the world built for rugby union. What is it? → Twickenham: In 2025, England's Red Roses won the Women's Rugby World Cup final at this stadium. Which city is it in? → London
- sayings-and-idioms-1: overlap like q-5417: Look at this ball. Which sport is it made for? → Cricket: Brits who are amazed say they were “bowled over”, like stumps I've knocked flat. I'm hard, red and stitched. What am I? → A cricket ball
- sitcoms-12: overlap like q-18918: I sell dodgy goods in Peckham, drive a yellow three-wheeled van, and call my brother Rodney a “plonker”. Who am I? → Del Boy: You see a yellow three-wheeled van with “Trotters Independent Traders – New York, Paris, Peckham” on the side. Whose van is it? → Del Boy
- sporting-events-15: overlap like q-3029: Runners often get shiny foil blankets like these after a marathon. Where were these blankets first meant to be used? → In space: It's shiny and silver, crinkles when you move, and London Marathon runners get wrapped in one at the finish to stay warm. What is it? → A foil blanket
- traditional-music-and-dance-1: overlap like q-18941: Three of these ceilidh dances have names linked to soldiers. Which one doesn't? → Strip the Willow: The band at a Scottish wedding strikes up “Strip the Willow”. What are the guests meant to do? → Dance in long lines
- traditional-music-and-dance-9: overlap like accents-and-dialects-5: “Iechyd da” means “good health”, people say it when they clink glasses, and it comes from the land with a red dragon on its flag. Where is that? → Wales: Rugby fans sing “Land of My Fathers” before big matches while waving flags with a red dragon. Which country's national anthem is it? → Wales
- traditional-music-and-dance-17: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: On 1 May, children in English villages skip round a tall pole, each holding a long ribbon. What is the pole called? → A maypole
- transport-14: overlap like q-2704: The first Land Rover, from 1948, was mainly made for which group of people? → Farmers: The first Land Rover, the car that later became the Defender, came out in 1948. It was tough enough for muddy fields and could even power farm machines. Who was it mainly made for? → Farmers
- twentieth-century-0: overlap like q-6605: Queen Elizabeth II died in 2022. Who became king after her? → Charles: Queen Elizabeth II belonged to the House of Windsor. Which Windsor became the next monarch when she died in 2022? → King Charles III
- twentieth-century-4: overlap like q-5661: In 1969, a famous band walked across this London street crossing for an album cover. Which band was it? → The Beatles: It's a zebra crossing in north London, next to a recording studio, and tourists walk across it in a line. Why is it famous? → The Beatles crossed it on an album cover
- twentieth-century-11: overlap like q-18338: After the Spice Girls, Posh Spice, Victoria Beckham, became famous for a new career. What is it? → Fashion design: I was “Posh” in a 1990s girl band, and I married a famous England football captain. Who am I? → Victoria Beckham
- twentieth-century-14: overlap like q-0163: En 1928, Alexander Fleming vio un moho creciendo en un plato de laboratorio. ¿Qué medicina descubrió? → La penicilina: It came from mould, Alexander Fleming spotted it on a dish in London in 1928, and it kills germs. What is this medicine called? → Penicillin
- twentieth-century-17: overlap like q-19420: A judge chats by text with a hidden human and a hidden computer. If the judge can't tell which is the machine, what has the computer passed? → The Turing test: Alan Turing suggested it in 1950: a person chats by text without seeing who answers. What does the Turing test check? → Whether a computer can pass for a human
