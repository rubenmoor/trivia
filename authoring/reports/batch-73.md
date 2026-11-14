# batch-73

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, early-britain, middle-ages, twentieth-century, customs-and-ceremonies, legendary-heroes, traditional-music-and-dance, soaps-and-dramas, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, team-gb-and-olympians, sporting-events, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, transport, hills-moors-and-national-parks, landmarks-and-castles, birds, plants-and-gardens, tudors-and-stuarts, georgians-and-victorians, parliament-and-prime-ministers, scientists-and-inventors, pioneers-and-heroes
- Merged: 98 (q-20188…q-20285)
- Approved: 91
- Needs work: 7
- Dropped by the pipeline: 60
- Reviewed by: claude-opus-5-5
- Claude calls: 297, about $36.70 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-71, batch-72; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-71 | batch-72 | batch-73 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 175 | 163 | 158 |
| skipped slots |  | 329 | 341 | 346 |
| dropped |  | 53 | 66 | 60 |
| drop rate | ≤ 20.0 % | 30.3 % ✗ | 40.5 % ✗ | 38.0 % ✗ |
| dropped: hard fail correct |  | 1 | 2 | 0 |
| dropped: hard fail unambiguous |  | 0 | 1 | 3 |
| dropped: hard fail no_giveaway |  | 11 | 16 | 10 |
| dropped: overlap |  | 40 | 46 | 46 |
| dropped: duplicate |  | 0 | 1 | 1 |
| dropped: fact-check wrong |  | 1 | 0 | 0 |
| merged |  | 122 | 97 | 98 |
| approved |  | 113 | 90 | 91 |
| needs_work |  | 9 | 7 | 7 |
| needs_work rate | ≤ 20.0 % | 7.4 % ✓ | 7.2 % ✓ | 7.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 4.1 % ✓ | 3.1 % ✓ | 2.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.8 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.6 % ✗ | 1.0 % ✗ | 1.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.3 % ✓ | 3.1 % ✓ | 4.1 % ✓ |
| media: no pick in review 1 |  | 15 | 16 | 10 |
| media: recovered by research |  | 12 | 13 | 6 |
| media: no pick at record |  | 3 | 3 | 4 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 24.0 % ✗ | 29.4 % ✗ | 30.4 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 8 | 0 | 14 |
| top move | ≤ 25.0 % | 17.2 % ✓ | 15.5 % ✓ | 17.3 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 80.3 % | 77.3 % | 84.7 % |
| values stimulus |  | 3 | 3 | 4 |
| top clue | ≤ 60.0 % | 43.4 % ✓ | 43.3 % ✓ | 45.9 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 26.2 % ✓ | 34.0 % ✓ | 30.6 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.9 % ✓ | 18.6 % ✓ | 20.4 % ✓ |
| values lens |  | 8 | 10 | 11 |
| media share | 15.0 %–50.0 % | 19.7 % ✓ | 22.7 % ✓ | 15.3 % ✓ |
| mean fun | ≥ 3.40 | 3.44 ✓ | 3.44 ✓ | 3.50 ✓ |
| cost $ |  | $39.18 | $33.82 | $33.49 |
| $ per approved | ≤ $0.35 | $0.35 ✓ | $0.38 ✗ | $0.37 ✗ |
| calls |  | 283 | 246 | 237 |
| calls per approved |  | 2.50 | 2.73 | 2.60 |
| wall time h |  | 1.15 | 1.10 | 1.20 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 11 (0 major), fact 1 (0 major), media 4 (2 major), difficulty 2 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.20

Major findings on approved questions:

None.

## Needs work

- **q-20189** (birds) Listen: Norwich City football club, who play in yellow and green, are nicknamed after this singing bird. Which bird is it? → Canary: None of the audio candidates is a canary singing. All six are spoken pronunciation files ("Canary Wharf", "canary fit", "canary in a coal mine", "Canary Islands", Dutch "Canariërs"), and some of them would say the answer out loud. No new search is allowed, so the essential audio slot can't be filled. Search for an actual canary song recording (for example "canary bird song" on Freesound). No suitable picture found for this question.
- **q-20194** (comedians-and-panel-shows) On Give Us a Clue, players acted out film and book titles without speaking. A player holds up this hand first. How many words are in the title? → 3: No candidate shows a single hand clearly holding up exactly three fingers, which this essential image needs. Candidate 1 is a Weimar coin with German text and an oath gesture. Candidate 2 shows soldiers swearing an oath to Hitler, which is unacceptable. 3 is a singer with an open hand, 4 is a sketch of a pointing hand, 5 contains nudity and 6 is a ring. No new search is allowed, so the media slot can't be filled. A search like "hand three fingers up" against a plain background would be needed. No suitable picture found for this question.
- **q-20207** (hills-moors-and-national-parks) In Scotland's pine woods, a shy pine marten is climbing a tree trunk. What is a pine marten? → A furry mammal: Hint 2 (“It's about the size of a pet cat”) gives the answer away: a small owl, a woodpecker and a beetle are all far smaller than a cat, so it rules out all three wrong answers at once. Hint 2 should narrow things down without settling it, for example something about its long bushy tail or its liking for berries and eggs, or the wrong answers should include something cat-sized.
- **q-20212** (money-and-shopping) Britons have a name for a lunch like this, when a sandwich, a snack and a drink come together for one price. What is it? → A meal deal: None of the media candidates works for the essential slot, and no new search is allowed. The question says "a lunch like this", so the image must clearly show a packaged sandwich, a bag of crisps and a drink together. Find such a photo (e.g. "UK meal deal sandwich"), or reword the question so it doesn't point at a picture and use an illustrative image. No suitable picture found for this question.
- **q-20213** (money-and-shopping) This is the Bank of England in London. Which of these is one of its jobs? → Issuing England's banknotes: This overlaps with q-17937 (approved), which asks “What are today's Bank of England £20 notes made of?”. That wording states outright that the Bank of England issues the £20 note, which is the answer here. A player who has seen either question gets the other one handed to them. If you want to keep a Bank of England question, it needs to ask about a different job, such as setting interest rates, and that would be a new question.
- **q-20243** (team-gb-and-olympians) Look at the photo: this building was built for London 2012. Who competes inside it? → Swimmers: Hint 2 (“finish their races dripping wet, and not from sweat”) leaves only Swimmers among the four options, so it gives the answer away before hint 3. It should be vaguer, for example about what the wave-shaped roof is meant to suggest without mentioning water or wetness. The facts check out: Zaha Hadid designed the building, Adlington won two bronzes there in 2012, and it opened to the public after the Games. The media is fine.
- **q-20254** (sayings-and-idioms) Teams run around on me. If I slope, one team gets to play downhill, which isn't fair. So a fair contest is called a “level” me. What am I? → A playing field: None of the six candidates is usable as an illustrative image, and no new search is allowed. None of them shows a referee's whistle or anything to do with football. The slot needs a new search, such as "referee whistle" or "football boots grass", that doesn't show a whole pitch. No suitable picture found for this question.

## Question axes

- move: analogy 3, cause_effect 2, count 5, estimate 3, identify 9, made_of 1, name_concept 11, odd_one_out 4, origin 14, purpose 7, record 1, sequence 2, when 8, who 11, word_meaning 17
- stimulus: detail 4, none 83, photo 10, sound 1
- clue: completion 5, direct 45, riddle 8, scenario 12, three_facts 28
- answer_kind: group 5, number 8, person 22, place 10, thing 30, time 8, word 15
- lens: body_senses 9, educational_media 7, everyday 19, history 11, language 16, nature 5, pop_culture 20, popular_science 4, school 4, science_news 2, university 1

## Dropped by the pipeline

- accents-and-dialects-3: overlap like q-19733: In which country do people say “Bore da” to mean “good morning”? → Wales: People say “Iechyd da” when they clink glasses, it means “good health”, and it comes from the land of the red dragon. Where? → Wales
- birds-5: overlap like q-18411: Harry Potter's pet Hedwig is an animal like this one. What kind of animal is it? → An owl: Listen: this is the call of the bird Hagrid gives Harry Potter for his 11th birthday. What kind of bird is it? → Snowy owl
- cities-and-towns-6: overlap like q-19508: Many British seaside towns have one of these, stretching out over the waves with arcades and rides along it. What is it? → A pier: At Brighton, a long walkway with rides and arcades stands on iron legs out over the sea. What is it called? → A pier
- cities-and-towns-11: overlap like q-6393: Watch: soft clay is shaped on a spinning wheel. What does it turn into after baking in a very hot oven? → Hard pottery: I start as soft, wet clay, then I'm baked in a very hot oven called a kiln. Stoke-on-Trent made so much of me that it got a nickname from me. What am I? → Pottery
- cities-and-towns-14: overlap like q-20146: The village with the longest place name in Britain, 58 letters long, is on which island? → Anglesey: A village on Anglesey in Wales has Britain's longest place name. Its station sign is famous with tourists. About how many letters does the name have? → About 60
- comedians-and-panel-shows-3: overlap like q-5571: I'm full of words lined up from A to Z. Look one up, and I tell you what it means and how to spell it. What am I? → A dictionary: On the panel show Call My Bluff, teams gave three meanings for a strange word, but only one was true. Which book, shown here, holds the true meanings? → A dictionary
- customs-and-ceremonies-8: overlap like q-17923: You're at a Highland games as the MacDonalds march past in their own tartan. What do you call a big Scottish family group like theirs? → A clan: Tartan is a criss-cross pattern of coloured stripes, Scots wear it as kilts at weddings, and many Scottish surnames have their own. Why? → To show which clan you belong to
- customs-and-ceremonies-17: overlap like q-3223: It's an honor from the British monarch, the ceremony uses a sword, and men who get it are called “Sir”. What is a woman called who gets it herself? → Dame: In this ceremony, a kneeling man is touched on the shoulder with a sword. In Britain, what word does he then get to put before his name? → Sir
- early-britain-8: overlap like q-9720: You’ve climbed Glastonbury Tor and are looking over the Somerset Levels. Which king do old legends link with this hill? → King Arthur: You're standing on the cliffs at Tintagel Castle in Cornwall. Legend says which famous king was born here? → King Arthur
- georgians-and-victorians-3: duplicate like q-2239: This glass skyscraper is nicknamed “the Gherkin”. In which city is it? → London: This hard, round hat was first made in 1849 by a famous hat shop that is still open today. In which city is that shop? → London
- georgians-and-victorians-6: overlap like q-5422: In stories, who uses this tool to look for clues? → A detective: Arthur Conan Doyle's most famous hero is usually shown in a hat like this one. What is his job? → A detective
- georgians-and-victorians-8: overlap like q-2522: Steam trains, Sherlock Holmes's London and Charles Dickens's novels all belong to a period named after a British queen. What is it called? → The Victorian era: Queen Victoria ruled for 63 years, from 1837 to 1901, and gave her name to a whole age. What do we call the British people of her time? → The Victorians
- georgians-and-victorians-17: overlap like q-9637: You're in Trafalgar Square, counting the giant bronze lions around the base of Nelson's Column. How many are there? → 4: This is Nelson's Column in Trafalgar Square, London. How many big bronze lions sit around its base? → 4
- hills-moors-and-national-parks-14: overlap like q-9619: On the longest day of the year, crowds gather here to watch what rise in line with the stones? → The sun: On Salisbury Plain in Wiltshire stands a giant ring of standing stones, built about 4,500 years ago, that lines up with the midsummer sunrise. What is it called? → Stonehenge
- landmarks-and-castles-0: overlap like q-2241: What is the water around this castle for? → To keep attackers out: Beaumaris Castle in Wales, shown here, has a ditch full of water all the way round it. What was the water for? → To keep attackers out
- landmarks-and-castles-5: overlap like q-5889: Medieval castles had thick, tall walls that were very hard to break. What were most of them made of? → Stone: Look at Durham Cathedral, shown here. What is it mostly built from? → Stone
- legendary-heroes-9: overlap like q-1674: Tenía claustro, iglesia y biblioteca, y allí se copiaban libros a mano. ¿Quiénes vivían en una abadía medieval? → Monjes: It's a ruin in Somerset, legend says King Arthur was buried there, and Henry VIII shut it down in 1539. What was Glastonbury Abbey built for? → A home for monks
- middle-ages-3: overlap like q-18204: Look at this close-up of a flag. Which part of the UK does it belong to? → Wales: Around 1400, Owain Glyndŵr led a rebellion in me against the English king. My flag has a red dragon on it. What am I? → Wales
- middle-ages-17: overlap like q-1268: El tapiz de Bayeux cuenta con dibujos bordados la conquista normanda de Inglaterra en 1066. ¿Cuánto mide de largo, más o menos? → 70 metros: You're standing on the battlefield in the town of Battle, where Harold fought William the Conqueror. In which year was the battle? → 1066
- money-and-shopping-0: overlap like q-18883: In Britain, what is a “fiver”? → A £5 note: Britons have a nickname for this note. What is it? → A fiver
- pioneers-and-heroes-5: overlap like q-4859: You spot the International Space Station passing overhead as a bright moving dot. About how high above Earth is it? → About 400 km: In 2016, Tim Peake ran the London Marathon on a treadmill, strapped down so he wouldn't float away, 400 km (250 miles) above Earth. Where was he? → The International Space Station
- pioneers-and-heroes-10: overlap like q-0051: ¿Qué planeta es conocido como el planeta rojo? → Marte: Beagle 2 was a small British lander, named after Charles Darwin's ship and sent off in 2003 to the red planet. Where was it going? → Mars
- accents-and-dialects-6: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 4: In the South Wales Valleys, someone says “Alright, butt?” to you. Who are they most likely to be? → Your friend
- accents-and-dialects-12: overlap like q-19908: Someone says “wee” for small, “aye” for yes and “loch” for lake. Which country are they most likely from? → Scotland: It means “I don't know”, and grannies say it every day. Where do people say “I dinnae ken”? → Scotland
- accents-and-dialects-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Cornish locals call them “emmets”: they arrive every summer and leave again in autumn. What is an emmet? → A holidaymaker
- birds-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which speckled British bird can copy car alarms and ringing phones almost perfectly? → Starling
- comedians-and-panel-shows-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In 2004, Tim Vine set a world record by telling 499 of something in one hour. What? → Jokes
- comedians-and-panel-shows-13: hard fail: correct 5, unambiguous 5, no_giveaway 1, no_overlap 5: The Goodies rode a famous bike called the trandem. How many seats did it have? → 3
- comedians-and-panel-shows-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I judge the celebrities' bakes in the famous Bake Off tent for charity. I have bright blue eyes, and only a truly great bake earns my handshake. Who am I? → Paul Hollywood
- football-2: overlap like q-9593: Boxing Day comes how many days after Christmas Day? → 1 day: English football has a big day of matches every year, the day after Christmas. What is that day called? → Boxing Day
- georgians-and-victorians-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: I'm a huge brick building in Lancashire, full of noisy machines. Victorian children crawled under them, and I spin fluffy fibres from a plant. What am I? → A cotton mill
- languages-of-britain-11: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: In Wales you might hear the word “Cymraeg”, said “kum-RAIG”. What is it? → The Welsh language
- parliament-and-prime-ministers-11: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 4: This street is lined with government offices and leads to Parliament. In which city is it? → London
- pioneers-and-heroes-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In 1939, Londoner Nicholas Winton arranged eight trains from Prague for 669 children. What were the trains for? → Carrying children to safety
- scientists-and-inventors-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It ran from 1990 to 2003, and a lab near Cambridge did almost a third of the work. What did the Human Genome Project read? → All of the DNA in a human
- transport-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Many British bus lanes only work at the times shown on their sign. Outside those times, who may drive in them? → Ordinary cars too
- tudors-and-stuarts-12: overlap like q-1674: Tenía claustro, iglesia y biblioteca, y allí se copiaban libros a mano. ¿Quiénes vivían en una abadía medieval? → Monjes: After breaking with the Pope, Henry VIII closed hundreds of abbeys and priories and took their land, gold and lead roofs. Who lost their homes? → Monks and nuns
- tudors-and-stuarts-15: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: On a freezing day in 1649, Charles I wore extra shirts so nobody would think he shivered from fear. How many shirts? → 2
- twentieth-century-8: overlap like q-20006: The Palace of Holyroodhouse in Edinburgh is the official home in Scotland of which person? → The King: Who owns this castle in the Scottish Highlands? → King Charles III
- sayings-and-idioms-5: overlap like q-12771: Ben Franklin printed the saying “Early to bed and early to rise makes a man healthy, wealthy, and…” How does it end? → Wise: Complete the old English proverb: “Early to bed and early to rise makes a man healthy, wealthy and…” → Wise
- sayings-and-idioms-16: overlap like q-19020: As Home Secretary, I set up London's Metropolitan Police in 1829. Officers are still called “bobbies” after my first name. Who am I? → Robert Peel: They wear tall helmets, help lost tourists, and their nickname comes from a man called Robert. What do Brits call them? → Bobbies
- scientists-and-inventors-4: overlap like q-18174: This castle sits on the rock of an ancient volcano, high above a capital city. Which castle is it? → Edinburgh Castle: Physicist Peter Higgs, whose “God particle” was found in 2012, worked for decades at the university in this city. Which city is it? → Edinburgh
- scientists-and-inventors-6: overlap like q-4101: In 1960 in Tanzania, these apes were seen stripping twigs to fish for termites: the first wild animals seen making tools. Which apes? → Chimpanzees: I was born in London. In 1960 I went to Tanzania and saw chimpanzees using twigs as tools, which surprised scientists everywhere. Who am I? → Jane Goodall
- scientists-and-inventors-14: overlap like q-2321: Drivers see me on dark roads, and I'm named after the way a cat's eyes look at night. People call me a “cat's eye”. What am I? → A road reflector: Percy Shaw from Halifax invented them in 1934: little studs in the middle of the road that shine back at car headlights at night. What are they called? → Cat's eyes
- sitcoms-3: overlap like q-19392: In 2000, TV experts chose the greatest British TV programme ever for the BFI. The winner was a 1970s sitcom set in Torquay. Which? → Fawlty Towers: You're watching Sybil Fawlty shout “Basil!” across the hotel lobby. In which decade was this first on TV? → The 1970s
- sitcoms-7: overlap like q-19664: In “Gavin & Stacey”, Nessa often asks, “What's occurring?” What does she mean? → What's going on?: Which Gavin & Stacey character greets people with “What's occurring?” → Nessa
- sitcoms-11: overlap like q-20069: My name means the head of an old horse. Del Boy, Rodney and Trigger meet inside me in Peckham. What kind of place am I? → A pub: Del Boy's van says “Trotters Independent Traders: New York – Paris – …”. Which place comes next? → Peckham
- sporting-events-0: overlap like q-1594: Tengo cinco casitas, una para cada dedo, y en la nieve te protejo del frío. ¿Qué soy? → Unos guantes: We come in a pair and we're white. Snooker referees wear us to pick up the balls, so no fingerprints get on them. What are we? → Gloves
- sporting-events-13: overlap like q-3029: Runners often get shiny foil blankets like these after a marathon. Where were these blankets first meant to be used? → In space: At the end of the London Marathon, runners get wrapped in shiny blankets like these. What are they for? → Keeping runners warm
- traditional-music-and-dance-13: overlap like q-19051: It's a Gaelic word, it's said in Ireland and Scotland, and people say it as they clink glasses. What does “sláinte” literally mean? → Health: “Wassail” comes from Old English, carol singers took it from door to door at Christmas, and some villages still sing it to apple trees. What does it wish you? → Good health
- tudors-and-stuarts-0: overlap like q-3675: This king broke with the Pope in the 1530s so he could end his marriage. Which church did he make himself the head of? → The Church of England: I had six wives, I loved feasts and jousting, and I broke away from the Pope to start the Church of England. Who am I? → Henry VIII
- tudors-and-stuarts-5: overlap like q-16235: Los soldados de los tercios llevaban esta lanza de unos cinco metros, la pica. ¿Para qué servía sobre todo? → Para frenar a la caballería enemiga: In the English Civil War, pikemen stood in tight blocks to stop charging horsemen. What was the pike they carried? → A very long spear
- tudors-and-stuarts-7: overlap like q-9805: In 1588, fires were lit on hilltops across England, each one seen from the next. What were they warning of? → The Spanish Armada: In which year did English sailors set old ships on fire and send them drifting into the Spanish Armada at night? → 1588
- tudors-and-stuarts-8: overlap like q-14257: Esta hija de los Reyes Católicos se casó con Enrique VIII y fue reina de Inglaterra. ¿Quién es? → Catalina de Aragón: Henry VIII asked the Pope to cancel his marriage to this queen so he could marry Anne Boleyn. Who is she? → Catherine of Aragon
- tudors-and-stuarts-9: overlap like q-19832: This half-timbered house in Stratford-upon-Avon is where a famous writer was born in 1564. Who was he? → William Shakespeare: Historians think I learned Latin at the grammar school in my home town, Stratford-upon-Avon. Later I wrote plays for the Globe. Who am I? → William Shakespeare
- tudors-and-stuarts-11: overlap like q-18208: On Bonfire Night, a stuffed dummy like this one is put on top of the bonfire. Who is it named after? → Guy Fawkes: Children once pushed stuffed figures like this through the streets, asking for “a penny for the Guy”. Who is the Guy? → Guy Fawkes
- tudors-and-stuarts-17: overlap like q-17880: The guards who wear this red-and-gold uniform have a famous nickname. What is it? → Beefeaters: These guards in dark blue and red uniforms live and work at the Tower of London. What is their famous nickname? → Beefeaters
- twentieth-century-2: overlap like q-3230: Which of these royals was NOT part of the House of Windsor? → Queen Victoria: When the news talks about the “House of Windsor”, what does it mean? → The British royal family
- twentieth-century-10: overlap like q-5661: In 1969, a famous band walked across this London street crossing for an album cover. Which band was it? → The Beatles: Which band walked across a zebra crossing on Abbey Road, London, for the cover of a 1969 album? → The Beatles
- twentieth-century-14: overlap like q-4268: The India–Pakistan cricket rivalry exists because one land became two countries in 1947, when an empire's rule there ended. Which empire? → The British Empire: Mahatma Gandhi led peaceful protests until India won its freedom in 1947. Who had been ruling India? → The British
