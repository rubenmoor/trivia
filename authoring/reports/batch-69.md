# batch-69

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, london, counties-and-regions, wildlife, early-britain, middle-ages, tudors-and-stuarts, twentieth-century, customs-and-ceremonies, pop-and-rock, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, pub-and-playground-games, sayings-and-idioms, money-and-shopping, transport, plants-and-gardens, regional-specialities, art-and-architecture, game-shows-and-presenters, team-gb-and-olympians, scientists-and-inventors, sporting-events, accents-and-dialects, traditional-music-and-dance, soaps-and-dramas
- Merged: 187 (q-19659…q-19845)
- Approved: 175
- Needs work: 12
- Dropped by the pipeline: 77
- Reviewed by: claude-opus-5-5
- Claude calls: 441, about $56.76 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-67, batch-68; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-67 | batch-68 | batch-69 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 351 | 304 | 264 |
| skipped slots |  | 153 | 200 | 240 |
| dropped |  | 110 | 98 | 77 |
| drop rate | ≤ 20.0 % | 31.3 % ✗ | 32.2 % ✗ | 29.2 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 1 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 22 | 22 | 8 |
| dropped: overlap |  | 84 | 70 | 64 |
| dropped: duplicate |  | 4 | 4 | 2 |
| dropped: fact-check wrong |  | 0 | 1 | 2 |
| merged |  | 241 | 206 | 187 |
| approved |  | 214 | 186 | 175 |
| needs_work |  | 27 | 20 | 12 |
| needs_work rate | ≤ 20.0 % | 11.2 % ✓ | 9.7 % ✓ | 6.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.7 % ✓ | 2.9 % ✓ | 1.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.1 % ✓ | 1.5 % ✓ | 1.1 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.2 % ✗ | 1.0 % ✓ | 1.6 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.1 % ✓ | 4.9 % ✓ | 3.7 % ✓ |
| media: no pick in review 1 |  | 28 | 25 | 19 |
| media: recovered by research |  | 20 | 18 | 15 |
| media: no pick at record |  | 8 | 7 | 5 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 25.9 % ✗ | 25.0 % ✗ | 26.1 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 64.9 % ✓ | 64.3 % ✓ | 64.1 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.17 ✓ | 2.00 ✗ | 1.80 ✗ |
| approved 11–15 |  | 42 | 37 | 35 |
| top move | ≤ 25.0 % | 14.1 % ✓ | 18.9 % ✓ | 17.1 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 78.8 % | 79.1 % | 80.2 % |
| values stimulus |  | 4 | 3 | 5 |
| top clue | ≤ 60.0 % | 42.7 % ✓ | 40.3 % ✓ | 40.1 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 23.2 % ✓ | 21.8 % ✓ | 25.1 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 19.9 % ✓ | 22.8 % ✓ | 21.9 % ✓ |
| values lens |  | 11 | 9 | 10 |
| media share | 15.0 %–50.0 % | 21.2 % ✓ | 20.9 % ✓ | 19.8 % ✓ |
| mean fun | ≥ 3.40 | 3.56 ✓ | 3.55 ✓ | 3.48 ✓ |
| cost $ |  | $69.70 | $62.57 | $53.36 |
| $ per approved | ≤ $0.35 | $0.33 ✓ | $0.34 ✓ | $0.30 ✓ |
| calls |  | 481 | 426 | 381 |
| calls per approved |  | 2.25 | 2.29 | 2.18 |
| wall time h |  | 2.05 | 1.85 | 1.81 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 56 (2 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 9 (1 major), fact 2 (1 major), overlap 1 (0 major), media 2 (1 major), difficulty 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.40

Major findings on approved questions:

- **q-19756**: fact — The question calls it a "London pop awards night", but that is no longer true: the 2026 BRITs were held at Manchester's Co-op Live on 28 February 2026, the first time the show left London, and the 2027 show is going there too (Official Charts, Music Week). The question needs rewording, e.g. "Which British pop awards night…". The rest checks out: annual since 1982, the 1977 Silver Jubilee first show, the BPI hint and all three wrong answers. (http://127.0.0.1:8001/review/q-19756)

## Needs work

- **q-19689** (football) Leah Williamson's club won the Women's Champions League in 2007 and 2025 and holds the record for Women's FA Cup wins. Which club? → Arsenal: Hints 1 and 2 each give the answer away against these options: "north London" rules out Chelsea (west London) and both Manchester clubs, and "red with white sleeves" is Arsenal's well-known kit. Both should be vague (e.g. the club's founding era or the women's team's Champions League final opponent) and only hint 3 should come close. The facts check out: Arsenal won the 2007 UEFA Women's Cup, which UEFA counts as the Champions League, and the 2025 final, and they hold the FA Cup record.
- **q-19692** (game-shows-and-presenters) You're watching the very first MasterChef on BBC One, with Loyd Grossman tasting the food. Which decade is it? → The 1990s: The question says the first MasterChef was on BBC One, but the original 1990 series with Loyd Grossman was shown on BBC Two (the fact check marked this wrong). Change "BBC One" to "BBC Two" in the question text. The rest is correct: the answer, the 1990s, is right, and the Mandela clue in hint 3 matches 1990. Fact check: wrong. The original MasterChef (1990, Loyd Grossman) was first shown on BBC Two, not BBC One. The decade (1990s) is right.
- **q-19702** (london) London's double-decker buses are famously red. Which of these London things is NOT usually red? → Taxis: This overlaps approved q-18533 in the same London subcategory. That question's answer is “A black cab”, so anyone who has seen it already knows London taxis are black and not red, which gives this question away. Seeing this one also helps with q-18533. Drop this question, or rebuild it around a different London thing that isn't red.
- **q-19709** (money-and-shopping) Britons call a £10 note a “tenner”. How many tenners make £50? → 5: None of the candidates shows a Bank of England £10 note, which is what the question names. 1–2 are Samsung Galaxy Note phones, 3, 4 and 6 are Canadian $10 notes, and 5 is an old engraving of the Bank of England building. No new search is allowed, so the slot needs a real £10 note photo (for example the Jane Austen £10 polymer note). No suitable picture found for this question.
- **q-19732** (accents-and-dialects) Complete the sentence: elocution lessons teach you how to… → Speak clearly and properly: All six candidates are vintage microphones. Even blurred, a microphone points straight to speaking, which gives the answer away against options about writing, dancing and laying a table. A new search can't be run, so the slot needs a neutral decorative image, for example "old classroom" or "vintage parlour room". Separately, hint 1's mention of newsreaders also leans hard towards speaking. No suitable picture found for this question.
- **q-19797** (sayings-and-idioms) I'm how sandpaper feels, and I'm how a Brit says they feel after a bad night with a cold. Which word am I? → Rough: None of the media candidates fit: all five are old scans (a printing manual, a portrait of Dr Maurice Raynaud, a Fritz Kahn book advert, two garden-tool catalogue pages), with no tissue box or cold. No new search is allowed. The question text itself is fine; it needs a new image search, something like "box of tissues" or "person with cold blanket". No suitable picture found for this question.
- **q-19799** (sayings-and-idioms) On an old sailing ship in a storm, the captain shouts “All hands on deck!”. What are the “hands”? → The sailors: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-19805** (sayings-and-idioms) Complete the old-fashioned British cry of surprise: “Golly…!” → Gosh: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-19810** (sporting-events) This is one of the famous Grand National fences at Aintree. What is it covered with? → Spruce branches: Neither candidate works as an essential photo. #1 is a distant view of the course where you can barely see the fence. #2 is an old sepia photo of Becher's Brook: it has no colour, so hint 1 doesn't work, and the old hedge may not be the modern spruce dressing. A new search isn't allowed here. The description is also out of date: since 2024 the Grand National field is capped at 34 runners, not 40, so "Forty horses" should become e.g. "Thirty-four horses" or drop the number. No suitable picture found for this question.
- **q-19829** (tudors-and-stuarts) You're at Hampton Court Palace, where Jane Seymour gave Henry VIII the son he longed for. In which century was the baby born? → The 16th century: This repeats approved q-3222 ("Anne Boleyn, one of Henry VIII's six wives… was queen of England in which century?" → 16th century). Both ask which century Henry VIII's reign falls in, through one of his wives, so seeing either one gives away the other. Hint 2 (Henry VIII became king in 1509) also almost settles it by itself.
- **q-19837** (twentieth-century) Who were the suffragettes in early 20th-century Britain? → Women fighting for the right to vote: This overlaps approved q-9810 in the same subcategory. Its question text says “To make people notice their fight for votes for women, Emmeline Pankhurst's suffragettes…”, which states this question's answer outright. Seeing one gives the other away, and the definition can't be reworded without becoming a different question.
- **q-19842** (wildlife) Look closely at this creature from a British rock pool. What is it? → A starfish: None of the candidates shows a starfish: 1 and 2 are fossil crinoids, and 3 and 4 are a Japanese woodblock print of a woman with a lantern. A new search isn't allowed this round. The slot needs a close-up of one common starfish (Asterias rubens) arm that hides the star shape. A search like "Asterias rubens close-up" might find one, or the question could be reworked so it doesn't need that image. No suitable picture found for this question.

## Question axes

- move: analogy 3, cause_effect 6, count 11, estimate 9, identify 32, made_of 5, name_concept 23, odd_one_out 10, origin 14, purpose 13, record 5, sequence 2, when 17, who 15, word_meaning 22
- stimulus: detail 7, none 150, photo 27, silhouette 1, sound 2
- clue: completion 7, direct 75, riddle 17, scenario 32, three_facts 56
- answer_kind: group 21, number 20, person 22, place 15, thing 44, time 18, word 47
- lens: body_senses 13, educational_media 17, everyday 35, history 35, language 20, nature 8, pop_culture 41, school 14, science_news 2, university 2

## Dropped by the pipeline

- accents-and-dialects-8: overlap like q-9542: This pastry with a crimped edge is named after which English county? → Cornwall: I say “Proper job!” when you've done well, I love pasties and cream teas, and my flag is a white cross on black. Who am I? → A Cornish person
- cities-and-towns-3: overlap like q-19460: People who speak with a Scouse accent come from which city? → Liverpool: Scousers have a famous accent, all four Beatles were Scousers, and many cheer for the Reds or the Blues. What is a Scouser? → Someone from Liverpool
- cities-and-towns-5: overlap like q-18871: I'm a hard, sugary stick sold at the seaside, and the town's name runs right through me. What am I? → Rock: It's long and often pink, the town's name runs right through the middle, and it's very hard on your teeth. What is Brighton rock? → A stick-shaped sweet
- comedians-and-panel-shows-0: overlap like q-17913: On QI, which panellist, the only one to appear in every episode, is famous for setting off the klaxon? → Alan Davies: On QI, first hosted by Stephen Fry, an obvious but wrong answer sets off a loud alarm and costs points. What is that alarm called? → The klaxon
- customs-and-ceremonies-2: overlap like q-18177: In Cambridge, people glide along the River Cam in these flat boats, pushed with a long pole. What are they called? → Punts: In Oxford and Cambridge, people glide along the river in flat boats like this. What does the person at the back use to push it along? → A long pole
- customs-and-ceremonies-7: overlap like q-15737: Look at this coin. An American rhyme says if you find one and pick it up, all day long you'll have… what? → Good luck: You spot a coin on the pavement. The rhyme says “Find a penny, pick it up…”. How long will your good luck last? → All day long
- customs-and-ceremonies-8: overlap like q-11512: En mi gran fiesta llevo vestido blanco y velo, me casé hace un ratito y el mariachi me canta mientras bailo con mi esposo. ¿Quién soy? → La novia: I've just got married. I step out of the church holding hands, and everyone throws confetti over me and my partner. Who am I? → The bride
- customs-and-ceremonies-17: duplicate like q-2461: Look at this shaggy cow with long horns and a fringe over its eyes. Which country does this breed come from? → Scotland: Look at this patterned cloth. Which country is it most famous from? → Scotland
- early-britain-1: overlap like q-9619: On the longest day of the year, crowds gather here to watch what rise in line with the stones? → The sun: Every year, thousands of people gather at this place to watch the Sun rise on the longest day. Where is it? → Stonehenge
- early-britain-2: overlap like q-19532: Viking raiders came to Britain over 1,000 years ago with a carved head like this one at the front. What was it fixed to? → A ship: In Lerwick, Shetland, people dressed as Vikings march with torches every January and set fire to one of these. What is it? → A Viking longship
- early-britain-8: overlap like q-18242: He was the son of Sir Lancelot, the purest of the Knights of the Round Table, and the one who found the Holy Grail. What was his name? → Galahad: King Arthur's knights searched for it, and Sir Galahad finally found it. Legends say Jesus drank from it at the Last Supper. What is it? → The Holy Grail
- early-britain-9: overlap like q-18357: Twice a day, I pull the sea far back from the shore. I uncover rock pools and let cars drive across the causeway to Lindisfarne. What am I? → Low tide: Twice a day I creep up the beach and slide back again. A Viking king of England once sat on the shore and told me to stop. I didn't! What am I? → The tide
- early-britain-12: overlap like q-6127: I'm a picture made of thousands of tiny colored stones or glass tiles pressed into cement. The Romans put me on their floors. What am I? → A mosaic: This floor in a Roman villa in Britain is a picture made of thousands of tiny coloured stones. What is this kind of picture called? → A mosaic
- football-9: overlap like q-2546: In 2023, Manchester City won the English league, the FA Cup and the Champions League in one season. What is this feat called? → Treble: In which season did Pep Guardiola's Manchester City win the Premier League, the FA Cup and the Champions League? → 2022–23
- game-shows-and-presenters-3: overlap like q-18406: Which British pair won Olympic gold in this sport in 1984, dancing to Ravel's “Boléro”? → Torvill and Dean: Dancing on Ice stars Torvill and Dean won 1984 Olympic gold skating to Boléro. How many perfect 6.0 marks did they get? → 12
- game-shows-and-presenters-7: overlap like q-18302: Complete the rule: on Pointless Celebrities, a “pointless” answer is a correct answer that… → Nobody in the survey gave: On Pointless, teams want the lowest score they can get. How many points does a pointless answer score? → 0
- game-shows-and-presenters-11: overlap like q-18770: On ITV's Catchphrase, a little golden robot pops up in the animated clues. What is his name? → Mr Chips: Catchphrase hosts tell players “Say what you see”. What are the players looking at? → A cartoon hiding a well-known phrase
- game-shows-and-presenters-12: overlap like q-19100: In each series of Taskmaster, how many comedians compete against each other? → 5: You've done the best job of anyone on a Taskmaster task. How many points does Greg Davies usually give you? → 5
- game-shows-and-presenters-17: overlap like q-18737: I come at the very end of Countdown: nine jumbled letters that always make one word, and 30 seconds to buzz in. What am I? → The Conundrum: Rachel Riley works the numbers board on Countdown. Which round always ends each show? → The Conundrum
- london-3: overlap like q-2307: Dogs like this one star in a Disney film set in London, with 101 spotted puppies. What breed is it? → Dalmatian: We were born in a house in London, and Cruella de Vil wanted to turn our coats into a fur coat. What kind of dogs are we? → Dalmatians
- london-6: overlap like q-17860: Which famous bear came all the way to London from Peru? → Paddington: I was found sitting on my suitcase at a London railway station, wearing a label: “Please look after this bear.” I was named after the station. Who am I? → Paddington Bear
- london-13: overlap like q-17883: It's black, furry and about 45 cm tall, worn by the King's Guard outside Buckingham Palace. Why was the bearskin hat made so tall? → To make soldiers look taller: The guards at Buckingham Palace wear red coats, shiny boots and a “bearskin”. What is a bearskin? → A tall furry hat
- middle-ages-0: overlap like q-1440: ¿Qué pueblo navegaba en drakares, barcos largos con una cabeza de dragón en la proa? → Los vikingos: I sailed to Britain from Denmark and Norway in a longship. I carved spiky letters called runes into stone and wood. Who am I? → A Viking
- middle-ages-1: overlap like q-18114: Folk dancers tie bells like these to their legs and jingle through village streets every May. Which country's tradition is this? → England: Look at these dancers in white with bells on their legs. What is this old English folk dance called? → Morris dancing
- middle-ages-6: overlap like q-19063: My people fought long wars against England in the Middle Ages. My hero William Wallace won a battle at a bridge in 1297, and the film “Braveheart” tells his story. Which country am I? → Scotland: This tower near Stirling honours the Scottish hero who won the Battle of Stirling Bridge in 1297. Who was he? → William Wallace
- middle-ages-8: overlap like q-18236: Angles, Saxons and Jutes began settling in Britain after the Romans left. Roughly how long ago was that? → About 1,600 years ago: Along with the Angles and the Saxons, which people crossed from what is now Denmark and settled in Kent and the Isle of Wight? → The Jutes
- middle-ages-9: overlap like q-18232: Each year a poet wins a carved chair like this one at a big festival of music and poetry that moves to a new town every summer. Which country holds it? → Wales: It's a Welsh word, the first recorded one was held at Cardigan Castle in 1176, and a national one is held every summer. What is an eisteddfod? → A festival of music and poetry
- middle-ages-10: overlap like q-19061: Robert the Bruce hid in a cave after losing battles. He watched a spider keep trying to spin its web until it worked. Which enemy did he then fight again and beat? → The English: The tale of Robert the Bruce and the spider is often told with the saying “If at first you don't succeed…”. How does it end? → “…try, try again.”
- middle-ages-12: overlap like q-9580: Westminster Abbey, January 1066: Harold Godwinson is crowned king. Who was crowned there next, on Christmas Day that same year? → William the Conqueror: This scene comes from the Bayeux Tapestry, which tells the story of 1066. Who won the Battle of Hastings that year? → William the Conqueror
- middle-ages-14: overlap like q-6606: A legend says Edward I showed his newborn son to the Welsh at Caernarfon Castle as their new prince. Which king did that baby become? → Edward II: Legend says Edward I promised the Welsh a prince born in Wales who spoke no English, then showed them his baby son. Where was the baby born? → Caernarfon Castle
- money-and-shopping-0: overlap like q-18883: In Britain, what is a “fiver”? → A £5 note: It's blue-green, has Winston Churchill on the back, and Britons call it a “fiver”. What is a fiver? → A £5 note
- plants-and-gardens-13: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: I stand tall on the village green. Every spring, children dance round me holding long coloured ribbons and weave them around me. What am I? → A maypole
- pop-and-rock-0: overlap like q-19380: You're watching Take That in the early 1990s, with Gary Barlow and Robbie Williams. How many singers are on stage? → 5: Before going solo with hits like “Angels”, Robbie Williams sang in which boy band? → Take That
- pop-and-rock-11: duplicate like q-16155: In welchem Jahrzehnt startete „Bauer sucht Frau“ bei RTL? → 2000er-Jahre: In which decade did Ant and Dec's Saturday Night Takeaway first air on ITV? → The 2000s
- pop-and-rock-12: overlap like q-18574: Who has been the lead singer of the Rolling Stones since the band began in 1962? → Mick Jagger: I grew up in Dartford in Kent, I studied at the London School of Economics, and a Maroon 5 hit is named after the way I dance. Who am I? → Mick Jagger
- pop-and-rock-17: overlap like q-8921: In 1849, New York inventor Walter Hunt bent a piece of wire into a pin with a little cap that covers its sharp point. What is it for? → Holding pieces of cloth together: Punks in 1970s London used these to hold their ripped clothes together, and even wore them as earrings. What are they? → Safety pins
- pub-and-playground-games-5: overlap like q-19266: You're at the World Conker Championships, swinging a nut on a string at your rival's. Which tree did your nut fall from? → Horse chestnut: Conkers fall in autumn, grow inside spiky green cases and get threaded on strings by British children. Which tree do they come from? → Horse chestnut
- regional-specialities-1: overlap like q-19246: It's eaten on Burns Night, it's served with mashed turnip and potatoes, and a bagpiper may lead it to the table. Where is haggis from? → Scotland: On Burns Night, a famous poem is read out loud to this Scottish food before it's cut open. What is it? → Haggis
- regional-specialities-5: overlap like q-12757: New Yorkers love this bread, which is boiled before it's baked and often eaten with cream cheese. What is it called? → A bagel: Shops on London's Brick Lane, open all night, sell salt beef in this ring of bread, boiled before it's baked. Their signs spell it “beigel”. What is it? → A bagel
- accents-and-dialects-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: It's a Scots word, and it hides in place names like Falkirk and Selkirk. What is a “kirk”? → A church
- art-and-architecture-2: overlap like q-19226: David Hockney painted sunny California swimming pools and drew on an iPad. In which northern English city was he born? → Bradford: David Hockney's famous 1967 painting “A Bigger Splash” shows a burst of white water. What is the splash in? → A swimming pool
- customs-and-ceremonies-13: fact-check wrong: Hint 1 ('They're real animals, not monsters') doesn't rule out the wrong answer 'crocodiles', which are also real animals. The answer, 'bears', is correct.: In A. A. Milne's poem “Lines and Squares”, a child walks on pavement like this. Who waits to eat anyone who steps on the lines? → The bears
- game-shows-and-presenters-8: fact-check wrong: Hint 3 is false: Tipping Point still starts with four players today, not one fewer. The answer of 4 is correct.: When Ben Shephard's Tipping Point began in 2012, how many players started each show? → 4
- money-and-shopping-4: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: In Asda's TV adverts, shoppers tap their back pocket. Complete the famous slogan: “That's Asda …” → Price
- pub-and-playground-games-13: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: In which playground chasing game are you safe from the chaser whenever your feet are off the floor? → Off ground tig
- regional-specialities-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This crumbly white cheese shares its name with a town that has a huge castle, and miners took it down the pits for lunch. Which cheese? → Caerphilly
- regional-specialities-16: overlap like q-9523: It's thick with a golden crust, and Devon and Cornwall argue about whether it goes on a scone before or after the jam. Clotted cream is made by gently heating what? → Full-fat cow's milk: Cornish ice cream is often extra rich and slightly yellow, because it's made with lots of which thick dairy product? → Clotted cream
- rugby-and-cricket-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In rugby union, the ball goes out over the side of the pitch. The hooker throws it back in and teammates lift the jumpers. What is this restart called? → A lineout
- rugby-and-cricket-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Rugby teams playing New Zealand face this dance before kick-off. Which people does it come from? → The Māori
- sayings-and-idioms-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: When a Brit says “Aww, bless!” about a toddler's wobbly first steps, what do they mean? → That's so sweet
- scientists-and-inventors-12: overlap like q-4305: Food in tin cans was patented in 1810. About how many years later was the can opener invented? → Nearly 50 years: Food tins were patented in London in 1810, long before the tin opener. How did people open the earliest tins? → With a hammer and chisel
- sporting-events-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Phil Taylor from Stoke-on-Trent won 16 world darts titles. What was his famous nickname? → “The Power”
- traditional-music-and-dance-3: overlap like q-18632: At an Irish dancing competition, a dancer in clicking hard shoes does a dance named like an old sailors' dance. Which dance is it? → The hornpipe: The Hornpipe gets faster and faster at the Last Night of the Proms, and its dancers mime pulling on ropes. Where was it famously danced? → On ships at sea
- traditional-music-and-dance-5: overlap like q-19141: Clog dancers in northern England wear traditional clogs. What are the soles of these shoes made of? → Wood: Clog dancers in northern England wear shoes with wooden soles, and their feet become part of the music. Which family of instruments are they joining? → Percussion
- tudors-and-stuarts-6: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: This water gate at the Tower of London opens onto the Thames, and many famous prisoners arrived through it by boat. What is it called? → Traitors' Gate
- twentieth-century-3: overlap like q-18701: Flowers like these bloomed on First World War battlefields and inspired the poppies Britons wear in November. In which region were those fields? → Flanders: Armistice Day marks the moment the fighting of the First World War stopped. In which month is it? → November
- twentieth-century-9: overlap like q-18265: The Spice Girls turned “Girl Power” into a famous slogan with their first hit, “Wannabe”. In which decade? → The 1990s: In 1996 we were five British girls singing about what we “really, really want”. Who are we? → The Spice Girls
- rugby-and-cricket-2: overlap like q-19184: This tiny urn is what England and Australia play the Ashes for. Where does it stay, even when Australia win? → Lord's: This little urn was given to an England cricket captain during the 1882–83 tour of Australia. Who was he? → Ivo Bligh
- rugby-and-cricket-12: overlap like q-5943: In 2003, this fly-half won the Rugby World Cup final with a drop goal in the last minute of extra time. Who is he? → Jonny Wilkinson: In which year did Jonny Wilkinson's last-minute drop goal in Sydney win England the Rugby World Cup? → 2003
- rugby-and-cricket-16: overlap like q-6673: I was a Welsh scrum-half, captain of Wales at 20, and I scored “that try” for the Barbarians against New Zealand in 1973. Who am I? → Gareth Edwards: The scrum-half is often the smallest player in a rugby union team and is always near the forwards. What is their main job? → Putting the ball into scrums and passing it out
- scientists-and-inventors-7: overlap like q-19466: I was born near Edinburgh in 1996, I was the first mammal cloned from an adult cell, and now I stand stuffed in the National Museum of Scotland. What animal am I? → A sheep: Ian Wilmut's team at the Roslin Institute near Edinburgh made the first mammal cloned from an adult cell. In which year was she born? → 1996
- scientists-and-inventors-14: overlap like q-2321: Drivers see me on dark roads, and I'm named after the way a cat's eyes look at night. People call me a “cat's eye”. What am I? → A road reflector: In 1934, Percy Shaw from Halifax patented these little reflectors set in the middle of the road. They shine in headlights at night. What are they called? → Cat's eyes
- sporting-events-3: overlap like q-18107: Wenlock, the London 2012 mascot, was said to be made from the last drops of steel used to build the stadium. How many eyes did he have? → 1: Wenlock and Mandeville each had one big eye and were said to be made from drops of steel. What were they at London 2012? → The official mascots
- sporting-events-8: overlap like q-18116: I have a soft sack you squeeze under your arm and long tubes that rest on your shoulder. I'm often played by people in kilts. What am I? → Bagpipes: Highland dancers at Scottish Highland Games wear kilts, dance on the balls of their feet and leap to the music of which instrument? → Bagpipes
- team-gb-and-olympians-4: overlap like q-9809: Eddie the Eagle became a hero at the 1988 Calgary Olympics despite finishing last in ski jumping. What did the “Eddie the Eagle rule” then require? → Minimum qualifying results to compete: Look at the photo: this British ski jumper became a hero at the 1988 Winter Olympics in Calgary. Who is he? → Eddie the Eagle
- team-gb-and-olympians-6: overlap like q-18555: On “Super Saturday”, Jessica Ennis-Hill won Olympic heptathlon gold in this stadium. Which one is it? → The London Olympic Stadium: I'm from Sheffield. I was the poster girl of London 2012, and on Super Saturday I won gold after seven events over two days. Who am I? → Jessica Ennis-Hill
- team-gb-and-olympians-10: overlap like sporting-events-3: Wenlock and Mandeville each had one big eye and were said to be made from drops of steel. What were they at London 2012? → The official mascots: It was a mascot of London 2012, it had one big eye, and it was named after the village where the Paralympics began. What was it called? → Mandeville
- team-gb-and-olympians-11: overlap like q-3542: This object slides across the ice in a Winter Olympics sport. What is it mostly made of? → Granite: It's a very hard rock, it comes from a tiny Scottish island called Ailsa Craig, and most Olympic curling stones are made of it. What is it? → Granite
- traditional-music-and-dance-1: overlap like q-6771: Before a World Cup match, the players line up, often put a hand on their heart and sing their country's special song. What is that song called? → The national anthem: Welsh fans sing “Land of My Fathers” before every big rugby match, like here. What kind of song is it? → Their national anthem
- traditional-music-and-dance-14: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: On May Day, many English villages put up a tall pole like this one. What is it for? → Dancing round with ribbons
- transport-12: overlap like q-18780: I walk the streets checking parking meters and yellow lines. Stay parked too long, and I'll stick a ticket on your car. Who am I? → A traffic warden: In Britain, you mustn't park on lines like these. Who might put a ticket on your car if you do? → A traffic warden
- tudors-and-stuarts-1: overlap like q-17880: The guards who wear this red-and-gold uniform have a famous nickname. What is it? → Beefeaters: These guards in red and gold look after the Tower of London. What is their famous nickname? → Beefeaters
- tudors-and-stuarts-14: overlap like q-2072: En la escena más famosa de Hamlet, en un cementerio, ¿qué sostiene el príncipe en la mano mientras habla? → Una calavera: In a famous Shakespeare scene, the hero holds a skull like this and talks to it. Which character is he? → Hamlet
- twentieth-century-1: overlap like q-5003: It lasted from 1914 to 1918, soldiers fought from muddy trenches, and people at the time called it “the Great War”. What do we call it today? → The First World War: In Michael Morpurgo's “War Horse”, Joey the farm horse is sent to France in 1914. Which war is he caught up in? → The First World War
- twentieth-century-13: overlap like q-4991: My face was on coins in Canada, Australia and Britain for decades. On Canada's gold-colored dollar coin, I shared the coin with a loon. Who am I? → Queen Elizabeth II: I was Queen for 70 years, I loved my corgis, and I told Paddington Bear I kept a marmalade sandwich in my handbag. Who am I? → Queen Elizabeth II
- twentieth-century-16: overlap like q-18902: Penicillin was found at St Mary's Hospital in London in 1928. Which family of medicines does it belong to? → Antibiotics: Alexander Fleming spotted it in London in 1928, it came from a mould on a dish, and it's called penicillin. What is it used for? → Killing germs that make you ill
- wildlife-5: overlap like q-9828: In which season are British garden ponds full of frogspawn and wriggling tadpoles? → Spring: Listen to this animal in a British garden pond. What are the clumps of jelly-covered eggs it lays called? → Frogspawn
