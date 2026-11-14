# batch-77

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, early-britain, middle-ages, twentieth-century, legendary-heroes, soaps-and-dramas, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, hills-moors-and-national-parks, birds, tudors-and-stuarts, georgians-and-victorians, parliament-and-prime-ministers, scientists-and-inventors, pioneers-and-heroes, drinks, creatures-ghosts-and-superstitions, pop-and-rock, traditional-music-and-dance, childrens-books-and-comics, art-and-architecture, childrens-tv
- Merged: 68 (q-20566…q-20633)
- Approved: 65
- Needs work: 3
- Dropped by the pipeline: 57
- Reviewed by: claude-opus-5-5
- Claude calls: 238, about $28.16 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-75, batch-76; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-75 | batch-76 | batch-77 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 148 | 131 | 125 |
| skipped slots |  | 356 | 373 | 379 |
| dropped |  | 45 | 55 | 57 |
| drop rate | ≤ 20.0 % | 30.4 % ✗ | 42.0 % ✗ | 45.6 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 11 | 6 | 11 |
| dropped: overlap |  | 33 | 48 | 46 |
| dropped: duplicate |  | 1 | 1 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 103 | 76 | 68 |
| approved |  | 90 | 72 | 65 |
| needs_work |  | 13 | 4 | 3 |
| needs_work rate | ≤ 20.0 % | 12.6 % ✓ | 5.3 % ✓ | 4.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 4.9 % ✓ | 2.6 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 1.3 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.9 % ✗ | 1.3 % ✗ | 2.9 % ✗ |
| needs_work: media | ≤ 10.0 % | 6.8 % ✓ | 0.0 % ✓ | 1.5 % ✓ |
| media: no pick in review 1 |  | 17 | 4 | 7 |
| media: recovered by research |  | 11 | 4 | 6 |
| media: no pick at record |  | 7 | 0 | 1 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 25.0 % ✗ | 38.2 % ✗ | 38.4 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 1 | 0 | 2 |
| top move | ≤ 25.0 % | 15.5 % ✓ | 18.4 % ✓ | 13.2 % ✓ |
| values move |  | 15 | 14 | 13 |
| top stimulus |  | 78.6 % | 81.6 % | 88.2 % |
| values stimulus |  | 4 | 3 | 3 |
| top clue | ≤ 60.0 % | 39.8 % ✓ | 34.2 % ✓ | 36.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 34.0 % ✓ | 27.6 % ✓ | 23.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 24.3 % ✓ | 18.4 % ✓ | 22.1 % ✓ |
| values lens |  | 11 | 10 | 11 |
| media share | 15.0 %–50.0 % | 21.4 % ✓ | 18.4 % ✓ | 11.8 % ✗ |
| mean fun | ≥ 3.40 | 3.63 ✓ | 3.50 ✓ | 3.47 ✓ |
| cost $ |  | $35.70 | $28.92 | $25.19 |
| $ per approved | ≤ $0.35 | $0.40 ✗ | $0.40 ✗ | $0.39 ✗ |
| calls |  | 252 | 205 | 178 |
| calls per approved |  | 2.80 | 2.85 | 2.74 |
| wall time h |  | 1.23 | 0.96 | 0.86 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 57 (0 %)
- Major among review needs work: 3 of 3 (100 %)
- Problems by kind: giveaway 7 (1 major), fact 4 (0 major), overlap 5 (2 major), media 2 (1 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.97

Major findings on approved questions:

None.

## Needs work

- **q-20573** (childrens-books-and-comics) Which picture-book elephant has skin made of bright squares, just like this patchwork? → Elmer: No candidate shows a bright patchwork of plain coloured squares like Elmer's skin, which the question points to with "just like this patchwork". The candidates are a muted drawing with a signature (1), a duck appliqué (2), a two-colour quilt (3), star-block or hexagon quilts (4, 5) and a mostly cream quilt (6). A new search isn't allowed, so a better picture has to be found by hand (for example "colorful square patchwork quilt"). The text itself is fine. No suitable picture found for this question.
- **q-20580** (drinks) When someone has a cold, Brits often make them a mug of hot Ribena. What good thing in blackcurrants is it known for? → Vitamin C: This overlaps q-9563 (approved, British drinks), whose question text says Ribena "was given to children for vitamin C". Anyone who has seen that question already knows this answer, and this fun fact repeats the same wartime vitamin C story. Drop it, or replace it with a different Ribena or blackcurrant fact.
- **q-20615** (tudors-and-stuarts) The Yeoman Warders who guard the Tower of London have a famous nickname. Finish it: “Beef…” → …eaters: This asks the same fact as q-17880 (in the pool, status needs_work): "The guards who wear this red-and-gold uniform have a famous nickname. What is it?" → Beefeaters. Keep only one of the two. If this one stays, also replace hint 2 (the gin brand), since it doesn't suit a kids' question at difficulty 3.

## Question axes

- move: cause_effect 7, count 4, identify 8, made_of 3, name_concept 6, odd_one_out 8, origin 3, purpose 5, record 2, sequence 3, when 4, who 9, word_meaning 6
- stimulus: detail 2, none 60, photo 6
- clue: completion 3, direct 25, riddle 9, scenario 9, three_facts 22
- answer_kind: group 14, number 4, person 11, place 10, thing 16, time 4, word 9
- lens: body_senses 1, educational_media 13, everyday 7, history 8, language 15, nature 1, pop_culture 13, popular_science 2, school 5, science_news 1, university 2

## Dropped by the pipeline

- art-and-architecture-5: overlap like q-17824: John Everett Millais's painting of a curly-haired boy gazing up at a soap bubble became a famous Pears soap advert. When did he paint it? → In the 1880s: John Everett Millais painted a curly-haired boy blowing bubbles. In 1886 a company bought it and turned it into a famous advert. What did it sell? → Soap
- childrens-books-and-comics-0: overlap like q-18171: Ron Weasley is Harry Potter's best friend at which school for witches and wizards? → Hogwarts: Pupils play Quidditch on flying broomsticks there, its four houses battle for the cup, and Harry becomes their youngest player in a century. Which school is it? → Hogwarts
- childrens-books-and-comics-7: overlap like q-5898: At the start of “Alice's Adventures in Wonderland”, Alice follows a White Rabbit with a pocket watch. Where does she follow him? → Down a rabbit hole: Alice sees a White Rabbit with a pocket watch hurry past, and she runs after him. What does she fall down next? → A rabbit hole
- childrens-books-and-comics-13: overlap like q-19216: Hagrid tells Harry, “Yer a wizard, Harry.” Complete the meaning: in his accent, “yer” stands for… → You're: I'm a half-giant with a bushy beard. I brought baby Harry to his aunt and uncle on a flying motorbike, and later told him “You're a wizard, Harry.” Who am I? → Hagrid
- childrens-tv-0: overlap like q-9509: Wallace loves Wensleydale cheese, his dog Gromit never says a word, and their films are often a Christmas treat on the BBC. What are the two made of? → Modelling clay: Gromit never speaks, loves reading the newspaper and is Wallace's best friend. What is he made of? → Modelling clay
- childrens-tv-11: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: CBeebies presenter Andy Day works at a museum and jumps back in time to meet which animals? → Dinosaurs
- childrens-tv-15: overlap like q-1489: Son segmentos rectos, forman el borde de un polígono y un triángulo tiene tres. ¿Qué son? → Los lados: Tinky Winky, the purple Teletubby, has an antenna on his head shaped like a triangle. How many sides does a triangle have? → 3
- cities-and-towns-15: overlap like q-20188: Many people here ask for a “bo'le o' wa'er”, dropping the “t”, and the TV soap “EastEnders” is set here. Which city is it? → London: The soap EastEnders is set in a made-up part of the city in this photo. Which city is it? → London
- drinks-2: overlap like q-18745: Red Lion is one of Britain's most common pub names. Legend says which king ordered his Scottish red lion to be shown in public places? → James I: In Britain, you're more likely to see a building called The Red Lion than anything else of its kind. What kind of place is it? → A pub
- drinks-12: overlap like q-18760: Horlicks and Ovaltine are malty powders that many Brits stir into a mug of something hot at bedtime. What do they stir them into? → Milk: Horlicks is a malty powder, you stir it into warm milk, and Brits have made it in Slough for over 100 years. When do people usually drink it? → At bedtime
- early-britain-4: overlap like q-9720: You’ve climbed Glastonbury Tor and are looking over the Somerset Levels. Which king do old legends link with this hill? → King Arthur: This statue stands at Tintagel in Cornwall, where legend says a famous king was born. Who is he meant to be? → King Arthur
- early-britain-5: overlap like q-6127: I'm a picture made of thousands of tiny colored stones or glass tiles pressed into cement. The Romans put me on their floors. What am I? → A mosaic: Rich Romans in Verulamium, the Roman town at St Albans, had mosaic floors. What is a mosaic made of? → Tiny coloured tiles
- early-britain-8: overlap like q-19199: You're catching a train at London Waterloo. Where does the station's name come from in the end? → A famous battle: Battle Abbey stands in East Sussex, and the town around it is simply called Battle. Why did it get that name? → A famous battle was fought there
- early-britain-11: overlap like q-18224: At Vindolanda, a Roman fort near Hadrian's Wall, thin wooden letters survived for nearly 2,000 years, including a birthday invitation. Why? → They lay in wet ground with no air: The Vindolanda tablets are thin wooden letters written by Romans. They were found at a fort in Northumberland, next to a wall built across northern England. Which wall? → Hadrian's Wall
- football-15: overlap like q-18539: In “Hey Diddle Diddle”, the cat plays the fiddle, the little dog laughs and the dish runs away with the spoon. Who jumps over the moon? → The cow: In an old nursery rhyme, I jumped over the moon. Footballers who win a big match say they're “over the moon”, just like me. Who am I? → The cow
- football-17: overlap like q-18204: Look at this close-up of a flag. Which part of the UK does it belong to? → Wales: Midfielder Aaron Ramsey captained the football team of the country with this flag. Which country is it? → Wales
- georgians-and-victorians-11: overlap like q-19416: Brits say “I'll put the kettle on” after bad news, when guests arrive, or after a long day. What are they about to make? → A cup of tea: In Britain, these dried leaves called Earl Grey are sold in boxes in every supermarket. What are they used to make? → A cup of tea
- georgians-and-victorians-12: overlap like q-7340: En las novenas de diciembre en Colombia, nunca falta «Los peces en el río». ¿Qué es? → Un villancico: “Good King Wenceslas” was written in Victorian times, its king trudges through deep snow, and people sing it door to door in December. What kind of song is it? → A Christmas carol
- hills-moors-and-national-parks-5: overlap like q-4705: Sticks of chalk crumble easily and leave a dusty white line. What did teachers use them for? → Writing on blackboards: The North Downs are hills in south-east England. Their soft white rock also makes the White Cliffs of Dover, and teachers once wrote with it. What rock is it? → Chalk
- hills-moors-and-national-parks-17: overlap like q-20108: You're walking along Offa's Dyke, the great border King Offa of Mercia built between England and Wales. What is it made of? → An earth bank and a ditch: Look at the photo: the Offa's Dyke Path follows this long bank, built over 1,200 years ago along the border of England and Wales. What is it made of? → Earth
- languages-of-britain-12: overlap like q-18388: Coronation Street is to ITV as the Welsh-language soap Pobol y Cwm is to… → S4C: S4C started in 1982, it's all in Welsh, and it shows the long-running soap “Pobol y Cwm”. What is S4C? → A TV channel
- legendary-heroes-3: overlap like q-0218: Según una vieja leyenda, si cierto tipo de ave abandona la Torre de Londres, caerá el reino. ¿Qué aves viven por eso siempre en la Torre? → Cuervos: The Welsh giant Bran's name means a big black bird. Legend links him to the Tower of London, where these birds live and must never leave. Which birds? → Ravens
- middle-ages-17: overlap like q-19015: This famous artwork, almost 70 m long, tells the story of the Norman Conquest of England. What is it called? → The Bayeux Tapestry: This very long picture tells the story of 1066, when the Normans took over England. What is it made of? → Cloth stitched with wool
- money-and-shopping-9: overlap like q-9602: Postman Pat drives his red van around the valley of Greendale with his black-and-white cat. What is the cat called? → Jess: You're in Greendale's post office, where Mrs Goggins works, and in comes a postman with his black-and-white cat. Who is he? → Postman Pat
- parliament-and-prime-ministers-2: overlap like q-9658: I have four paws and live at 10 Downing Street. Since 2011 I've seen many prime ministers come and go. My title is Chief Mouser. Who am I? → Larry: This is Palmerston, the cat who caught mice at the Foreign Office. Which famous Downing Street cat did he often have stand-offs with? → Larry
- parliament-and-prime-ministers-3: overlap like q-19535: Who works behind this famous black door in London? → The Prime Minister and their team: This is King Charles III. In the UK, who actually leads the government? → The Prime Minister
- parliament-and-prime-ministers-9: overlap like q-18310: A crowned portcullis with chains is a famous British badge. Whose badge is it? → The Houses of Parliament: It's a heavy metal grid gate that drops down to shut a castle entrance. With a crown on top, it's the symbol of the UK Parliament. What is it? → A portcullis
- parliament-and-prime-ministers-17: overlap like q-18688: Britain's NHS began in 1948, it's paid for out of taxes, and it's free when you use it. What does it give people? → Free doctors and hospitals: An Act of Parliament in 1946 created me. Since 1948, Britons have seen doctors and gone to hospital without paying at the door. In 2020, people clapped for me on their doorsteps. What am I? → The NHS
- pioneers-and-heroes-17: overlap like q-18940: Sports games held at Stoke Mandeville Hospital in Buckinghamshire from 1948 grew into which world event? → The Paralympic Games: In 1948, Doctor Ludwig Guttmann held wheelchair sports games for injured soldiers at Stoke Mandeville Hospital. Which big sports event grew out of them? → The Paralympic Games
- accents-and-dialects-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In the North East of England, someone might say “I've got a spelk in my finger!” What is a spelk? → A splinter
- accents-and-dialects-12: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Very proper, correct English is called “the Queen's English” or “the King's English”. Who is it named after? → Britain's king or queen
- childrens-books-and-comics-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I'm round and yellow, my hair is in two bunches, and I'm always cheerful. I'm one of the Little Misses. Who am I? → Little Miss Sunshine
- early-britain-7: overlap like q-6608: St Edward's Crown is named after Edward the Confessor, who built Westminster Abbey. When does a British monarch wear it? → Only at their coronation: King Edward the Confessor had the first great abbey built on this spot in London. What is it called? → Westminster Abbey
- early-britain-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Sweyn Forkbeard was the Viking who became king of England in 1013. What did his nickname describe? → A beard split into two points
- football-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Fans jump up and cheer me, strikers dream of me and goalkeepers try to stop me. What am I? → A goal
- georgians-and-victorians-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: I'm small, and the very first one of me, from 1840, was black and showed young Queen Victoria. What am I? → A postage stamp
- hills-moors-and-national-parks-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In the Lake District, fell runners race up and down the “fells”. What is a fell? → A hill
- pioneers-and-heroes-0: overlap like q-20424: Donald Campbell's boat Bluebird K7 broke the same world record seven times. Which record was it? → Fastest boat on water: In the 1920s, Sir Malcolm Campbell drove his car Bluebird on Pendine Sands in Wales. What was Bluebird built to do? → Go faster than any car before
- soaps-and-dramas-2: overlap like q-19639: Ken Barlow has lived on me since my very first episode. I'm in Weatherfield and I'm covered in cobbles. What am I? → Coronation Street: Ken's wife is Deirdre, his son is Peter and his adopted daughter is Tracy. Which Coronation Street family is this? → The Barlows
- traditional-music-and-dance-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Around 1903, music teacher Cecil Sharp went from village to village in Somerset, collecting from old farm workers. What did he collect? → Folk songs
- traditional-music-and-dance-3: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Many morris dancing teams have a “fool” in a patchwork costume. What is his job? → Making the crowd laugh
- tudors-and-stuarts-9: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: A Tudor whipping boy was often a noble's son, shared lessons with a young prince, and was the prince's friend. What was his job? → Taking the prince's punishments
- sayings-and-idioms-10: overlap like q-19329: In Cockney rhyming slang, “apples and pears” means stairs. What does “pork pies” mean? → Lies: A British mum says “Stop telling porkies!” It's short for “pork pies”, which rhymes with the real word. What are porkies? → Lies
- scientists-and-inventors-3: overlap like q-4101: In 1960 in Tanzania, these apes were seen stripping twigs to fish for termites: the first wild animals seen making tools. Which apes? → Chimpanzees: British scientist Jane Goodall spent decades studying these animals in the forests of Tanzania. What are they? → Chimpanzees
- sitcoms-13: overlap like q-18185: In The Two Ronnies' hardware-shop sketch, the shopkeeper brings these. What had the customer actually asked for? → Fork handles: In a famous 1976 Two Ronnies sketch, Ronnie Barker walks into a hardware shop and asks for “four candles”. What does he really want? → Fork handles
- soaps-and-dramas-13: overlap like q-18924: Producer Julia Smith and writer Tony Holland based me on a Victorian square in Dalston. I was built at Elstree, in Borehamwood. What am I? → Albert Square: I'm a London square where, in 2001, teenage Zoe screamed “You ain't my mother!” and Kat shouted back “Yes I am!”. What am I? → Albert Square
- traditional-music-and-dance-9: overlap like q-18308: Every January, people in Somerset sing to the trees in places like this to wake them up for a good cider crop. What is this kind of place called? → An orchard: In January, people in Somerset and Herefordshire sing to trees, pour cider on their roots and hang toast in their branches. Where does this happen? → In an orchard
- traditional-music-and-dance-8: overlap like q-18232: Each year a poet wins a carved chair like this one at a big festival of music and poetry that moves to a new town every summer. Which country holds it? → Wales: At Wales's National Eisteddfod, a festival of words and music, one winner gets a carved chair like this. What must they do best? → Write a poem
- traditional-music-and-dance-16: overlap like q-7596: Escucha: ¿qué instrumento es este? → El acordeón: Listen: Scotland's Jimmy Shand became famous playing this instrument at dances and ceilidhs. What is it? → An accordion
- tudors-and-stuarts-6: overlap like q-9795: British children make a “guy” from old clothes stuffed with newspaper. On which date is it burnt on a bonfire? → 5 November: He was born in York, called himself “Guido” while abroad, and was caught under Parliament in 1605. Which everyday word for a man comes from his name? → Guy
- tudors-and-stuarts-10: overlap like q-19065: Richard III died at the Battle of Bosworth in 1485. In 2012, his skeleton was found under a car park in which city? → Leicester: The film “The Lost King” tells how a fan helped find Richard III's bones under a car park in Leicester. In which decade were they found? → The 2010s
- twentieth-century-4: overlap like q-20269: Which Dad's Army character runs around yelling “Don't panic!” whenever trouble starts? → Lance Corporal Jones: In the BBC comedy “Dad's Army”, old butcher Corporal Jones gets in a flap whenever things go wrong. What does he shout? → “Don't panic!”
- twentieth-century-7: overlap like q-0163: En 1928, Alexander Fleming vio un moho creciendo en un plato de laboratorio. ¿Qué medicina descubrió? → La penicilina: I'm a Scottish scientist. In 1928, in my London lab, I found a mould killing the germs in a dish, and I named its juice penicillin. Who am I? → Alexander Fleming
- twentieth-century-8: overlap like q-20385: In 1903 I started a group in Manchester to win votes for women. Our motto was “Deeds not words”, and my daughters joined me. Who am I? → Emmeline Pankhurst: I was founded in Manchester in 1903, my motto was “Deeds, not words”, and a newspaper nicknamed my members suffragettes. What am I? → The Women's Social and Political Union
- twentieth-century-9: overlap like q-5494: In 1953, two climbers became the first to stand on top of this mountain and wave flags there. Who were they? → Edmund Hillary and Tenzing Norgay: I kept bees in New Zealand. In 1953, on a British expedition, I reached the top of Everest with Tenzing Norgay, and the news reached London on Coronation Day. Who am I? → Edmund Hillary
- twentieth-century-10: overlap like q-1636: Nunca iba a ser rey, pero mi hermano renunció a la corona por amor y me tocó a mí. Además, tartamudeaba. ¿Quién soy? → Jorge VI: It's December 1936, and King Edward VIII has just given up the throne to marry Wallis Simpson. Who becomes king next? → George VI
- twentieth-century-13: overlap like q-1171: ¿Quién creó la World Wide Web y el HTML, el lenguaje con el que se escriben las páginas web? → Tim Berners-Lee: I'm a scientist from London. In 1989, working in Switzerland, I came up with a way to link pages across the internet, and I built the first website. Who am I? → Tim Berners-Lee
