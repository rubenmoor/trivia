# batch-66

Made by `qgen batch` on 2026-11-13 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): comedians-and-panel-shows, landmarks-and-castles, brands-and-adverts, pop-and-rock, sitcoms, tudors-and-stuarts, legendary-heroes, art-and-architecture, transport, creatures-ghosts-and-superstitions, rivers-coasts-and-islands, rugby-and-cricket, hills-moors-and-national-parks, regional-specialities, sweets-and-crisps, accents-and-dialects, pub-and-playground-games, twentieth-century, georgians-and-victorians, sporting-events, languages-of-britain, middle-ages, cities-and-towns, birds, christmas-in-britain, traditional-music-and-dance, early-britain, soaps-and-dramas
- Merged: 241 (q-18971…q-19211)
- Approved: 226
- Needs work: 15
- Dropped by the pipeline: 105
- Reviewed by: claude-opus-5-5
- Claude calls: 544, about $73.18 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-64, batch-65; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-64 | batch-65 | batch-66 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 363 | 347 | 346 |
| skipped slots |  | 141 | 157 | 158 |
| dropped |  | 82 | 78 | 105 |
| drop rate | ≤ 20.0 % | 22.6 % ✗ | 22.5 % ✗ | 30.3 % ✗ |
| dropped: hard fail correct |  | 1 | 1 | 3 |
| dropped: hard fail unambiguous |  | 2 | 1 | 0 |
| dropped: hard fail no_giveaway |  | 17 | 19 | 18 |
| dropped: overlap |  | 60 | 56 | 81 |
| dropped: duplicate |  | 3 | 1 | 1 |
| dropped: fact-check wrong |  | 0 | 1 | 2 |
| merged |  | 281 | 269 | 241 |
| approved |  | 268 | 254 | 226 |
| needs_work |  | 13 | 15 | 15 |
| needs_work rate | ≤ 20.0 % | 4.6 % ✓ | 5.6 % ✓ | 6.2 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.5 % ✓ | 1.5 % ✓ | 3.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.4 % ✓ | 0.4 % ✓ | 0.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.2 % ✗ |
| needs_work: media | ≤ 10.0 % | 1.8 % ✓ | 3.3 % ✓ | 2.5 % ✓ |
| media: no pick in review 1 |  | 30 | 37 | 29 |
| media: recovered by research |  | 26 | 28 | 25 |
| media: no pick at record |  | 4 | 9 | 5 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 17.9 % ✓ | 17.0 % ✓ | 24.6 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 68.0 % ✓ | 69.2 % ✓ | 65.4 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.10 ✓ | 1.37 ✓ | 1.06 ✓ |
| approved 11–15 |  | 57 | 61 | 48 |
| top move | ≤ 25.0 % | 14.6 % ✓ | 14.5 % ✓ | 18.7 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 81.9 % | 76.2 % | 74.3 % |
| values stimulus |  | 4 | 5 | 4 |
| top clue | ≤ 60.0 % | 42.0 % ✓ | 46.8 % ✓ | 49.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 26.3 % ✓ | 23.4 % ✓ | 23.2 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 16.7 % ✓ | 21.2 % ✓ | 19.9 % ✓ |
| values lens |  | 11 | 10 | 11 |
| media share | 15.0 %–50.0 % | 18.1 % ✓ | 23.8 % ✓ | 25.7 % ✓ |
| mean fun | ≥ 3.40 | 3.62 ✓ | 3.63 ✓ | 3.67 ✓ |
| cost $ |  | $76.96 | $73.36 | $69.81 |
| $ per approved | ≤ $0.35 | $0.29 ✓ | $0.29 ✓ | $0.31 ✓ |
| calls |  | 548 | 525 | 484 |
| calls per approved |  | 2.04 | 2.07 | 2.14 |
| wall time h |  | 2.34 | 2.35 | 2.10 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 56 (4 %)
- Major among review needs work: 1 of 4 (25 %)
- Problems by kind: giveaway 5 (1 major), fact 2 (0 major), overlap 1 (0 major), media 6 (3 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 55 of 60 (92 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.37

Major findings on approved questions:

- **q-19072**: media — The media is the main problem. It is set as "essential", but the question doesn't ask about a photo. The file "Shirley Bassey Wembley 2006.jpg" shows the answer herself, sharp on screen, and its title names her. It should be an illustrative or decorative image that doesn't show her, such as Cardiff Bay or gold bars. I checked the facts and they hold: Bassey sang "Goldfinger", "Diamonds Are Forever" and "Moonraker", and the fun fact is right that she is the only singer with more than one Bond theme. The three wrong answers never sang a Bond theme, so none of them is also defensible. (http://127.0.0.1:8001/review/q-19072)
- **q-19076**: media, giveaway — The media is marked essential, but it is a sharp photo of Dua Lipa herself (the file title even names her). The question is a text clue, not "who is in this photo", so the picture shows the answer to anyone who knows her face. It needs an illustrative or decorative image instead, such as a pop concert stage. The facts are correct: she was born in London to Kosovo-Albanian parents, had hits with “New Rules” and “Levitating”, sang “Dance the Night” for the Barbie film, and “Dua” means love in Albanian. The wrong answers are fine and the difficulty fits. (http://127.0.0.1:8001/review/q-19076)

## Needs work

- **q-18993** (brands-and-adverts) It began in a lock-up garage in Uttoxeter in 1945, and Brits now call almost any yellow digger by its three letters. Where does the name JCB come from? → Its founder's initials: Hint 2 (“Lots of family firms, from cars to biscuits, are named after a person”) gives the answer away: it rules out the motto, customers and army code options and leaves only the founder's initials. Replace it with a hint that doesn't point at naming after a person, such as one about the founder's first products (tipping trailers made from war-surplus parts).
- **q-18998** (christmas-in-britain) Long before sugar was cheap in Britain, what were roots like these used for? → Sweetening cakes and jams: None of the candidates gives the essential slot what it needs: a clear photo of whole raw parsnips with no text. Candidates 1 and 2 are tall, grainy scans of a single odd-shaped root with a caption. Candidate 4 is a labelled catalogue drawing that looks like carrots. Candidates 3 and 5 are full catalogue pages of dense text, with parsley and okra pictured too. A new search isn't allowed, so the slot needs a modern parsnip photo, for example from the search "parsnips Pastinaca sativa". No suitable picture found for this question.
- **q-19002** (christmas-in-britain) Look at these: a paper crown, a tiny toy and a joke. At British Christmas dinner, what do they burst out of? → A Christmas cracker: None of the six candidates shows cracker contents: they're a coconut plate from a 1907 book and five 18th-century satirical prints (two titled "Murder"). This essential image needs a close-up of a paper crown, a small toy and a joke slip, but no new search is allowed. Search again with something like "Christmas cracker contents", or change the media role so the question no longer starts with "Look at these". No suitable picture found for this question.
- **q-19018** (georgians-and-victorians) Which of these stories is NOT a classic Christmas pantomime? → Hamlet: The picked picture has an unsuitable licence (pd-us-only: PD-1923, PD-US-expired).
- **q-19031** (hills-moors-and-national-parks) You twist your ankle high on a fell in the Lake District. Which number do you call to get mountain rescue? → 999: This repeats the fact in approved q-9674 (the UK emergency number is 999, used for police, fire and ambulance). Asking it again for mountain rescue doesn't make it a new fact, and seeing one question gives away the other. Hint 1 also gives the answer away for UK players, because it says the number is the same one you call for fire or an ambulance.
- **q-19039** (landmarks-and-castles) King Charles's gardens at Highgrove in Gloucestershire are famous worldwide. Which of these will you NOT find there? → Chemical weed killers: No candidate shows King Charles's Highgrove gardens in Gloucestershire. Candidates 1, 2 and 6 are a different Highgrove House in Eastcote, London. Candidate 3 is a plain field near a hotel of the same name. Candidates 4 and 5 are photos of visitors at Highgrove, with only a stone outbuilding behind them. The image needs a new search, for example "Highgrove Garden Gloucestershire" or "Highgrove wildflower meadow" (if the meadow is used, it must not stand out as the obvious answer). The text itself is fine. No suitable picture found for this question.
- **q-19069** (middle-ages) After MPs vote a new bill through the House of Commons, where does it usually go next? → The House of Lords: Hint 1 (“It's in the same building as the House of Commons”) gives the answer away. Of the four options, only the House of Lords sits in the Palace of Westminster. The Supreme Court is in Middlesex Guildhall, the Cabinet meets at Downing Street, and the Privy Council usually meets at Buckingham Palace. Hint 1 should be a vague hint instead, for example about the second stage of law-making.
- **q-19079** (pop-and-rock) On this TV show, any kind of act can perform for judges, and the winner gets a spot at the Royal Variety Performance. Which show? → Britain's Got Talent: The fun fact misspells the 2012 winner's name: she is Ashleigh Butler, not "Ashley". Correct it to "Ashleigh Butler and her dancing dog, Pudsey". Everything else is fine: the clue (any kind of act, Royal Variety spot) fits only Britain's Got Talent.
- **q-19080** (pub-and-playground-games) Look at this windmill with turning sails. On a British seafront, which game would you find it in? → Crazy golf: None of the candidates gives a clear view of a crazy golf windmill, which is what the question ("Look at this windmill…") and the note ask for. Candidate 1 shows a whole mini golf course at dusk with only a tiny windmill far in the background. Candidates 2 and 3 show a statue and a lighthouse, and 4 and 5 are off-topic. The slot needs a new search such as "crazy golf windmill" or "miniature golf windmill hole". No suitable picture found for this question.
- **q-19092** (accents-and-dialects) Liam Gallagher calls his brother Noel “our …”, the Mancunian way to say brother. Complete the phrase. → Kid: Hint 2 (“The same word also means a young child”) gives the answer away: of Kid, Pal, Chum and Bud, only “kid” means a young child, so the second hint already settles it. Replace hint 2 with a vaguer clue, for example that the phrase is common across northern England, and keep the young-child or baby-goat meaning for hint 3 only.
- **q-19123** (regional-specialities) In an Ulster fry, triangles of “fadge” sit next to the soda farls. What is fadge? → Potato bread: The description says the plate has “more bread on it than a bakery window”. Read with only the four options, that tells players fadge is a bread, which rules out Black pudding (and arguably Oatcake). Rewrite it to joke about the Ulster fry or Belfast breakfasts without saying what kind of food fadge is.
- **q-19148** (tudors-and-stuarts) You're searching the cellar under Parliament on 4 November 1605 and find 36 barrels hidden under firewood. What's inside? → Gunpowder: This overlaps approved q-9800 (“Remember, remember…”: a plot to blow up what? → The Houses of Parliament). This question puts barrels of gunpowder in the cellar under Parliament in 1605, so anyone who sees it already knows q-9800's answer, and the reverse is nearly true too. Both are level-2 Gunpowder Plot basics. Drop one of them, or move this one to a Gunpowder Plot fact that doesn't name Parliament as the target.
- **q-19161** (rivers-coasts-and-islands) Children have ridden these animals on British beaches for more than 100 years. What are they? → Donkeys: The media slot is set to essential with the note "donkeys giving rides on a British beach", but the question doesn't ask about the picture. Any matching photo shows the answer outright (candidates 1–4 all show donkeys). Change the slot to illustrative with a donkey-free British seaside image, e.g. candidate 5 (an empty Blackpool beach) or a search like "Blackpool beach promenade". The text itself is fine. No suitable picture found for this question.
- **q-19165** (rugby-and-cricket) The Ireland rugby union team has players from the Republic of Ireland and from which part of the UK? → Northern Ireland: Hint 2 (“Belfast is its biggest city.”) gives the answer away: naming Belfast identifies Northern Ireland outright, and it is a stronger clue than hint 3 (the Giant's Causeway). Hint 2 should be vaguer, for example that the part shares a land border with the Republic, and the Belfast clue could become hint 3. Also, “its” in hint 2 reads as if it refers to the team.
- **q-19209** (twentieth-century) Fearing poison gas bombs, the British government handed out gas masks in 1939. Who got one? → Everyone, even babies: Hint 2 (“Children had to carry theirs to school”) rules out all three “Only…” options, so it gives the answer away before hint 3. Hint 1 already points the same way. The answer “Everyone, even babies” also stands out in form from the three “Only…” options. Approved q-9808 shows 1939 children carrying gas mask boxes, which also gives this answer away. Hint 2 needs replacing with a vaguer clue, e.g. about how many millions of masks were made. Ideally the options would also have the same form, e.g. all “Every…/Only…” with similar length.

## Question axes

- move: analogy 6, cause_effect 14, count 7, estimate 7, identify 45, made_of 15, name_concept 15, odd_one_out 14, origin 23, purpose 13, record 8, sequence 14, when 18, who 27, word_meaning 15
- stimulus: detail 18, none 179, photo 41, sound 3
- clue: completion 5, direct 120, riddle 26, scenario 30, three_facts 60
- answer_kind: group 39, number 15, person 40, place 30, thing 56, time 22, word 39
- lens: body_senses 8, educational_media 32, everyday 27, history 48, language 34, nature 9, pop_culture 45, popular_science 2, school 29, science_news 1, university 6

## Dropped by the pipeline

- accents-and-dialects-2: overlap like q-9518: A Geordie comes from the city with this famous bridge. Which city is it? → Newcastle: It means “yes, of course!”, it's often followed by “man”, and Ant and Dec grew up saying it. Where does “Why aye” come from? → Newcastle
- accents-and-dialects-3: overlap like q-18072: If a British footballer says they're “gutted” after a match, how do they feel? → Very disappointed: You've just won tickets to see your favourite band. Three of these words could describe how you feel. Which one couldn't? → Gutted
- accents-and-dialects-10: overlap like q-18067: You're watching Smithy and Nessa in Gavin & Stacey. Which actor plays Smithy and co-wrote the show with Ruth Jones? → James Corden: It's Nessa's catchphrase in Gavin and Stacey, she says it all over Barry Island, and it's a laid-back Welsh greeting. What does “What's occurring?” mean? → What's going on?
- accents-and-dialects-15: overlap like q-18176: It's yellow, it travels underwater, and Liverpool's most famous band sang about living in one. What is it? → A submarine: Which world-famous band all grew up speaking with a Scouse accent? → The Beatles
- art-and-architecture-4: overlap like q-9637: You're in Trafalgar Square, counting the giant bronze lions around the base of Nelson's Column. How many are there? → 4: You're in Trafalgar Square looking at Nelson's Column. In 1867, years after the column went up, what was added around its base? → Four bronze lions
- birds-3: overlap like q-9553: Which birds do people in Britain count with the rhyme “One for sorrow, two for joy”? → Magpies: An old British rhyme about these birds starts “One for sorrow, two for…”. Two for what? → Joy
- birds-10: overlap like q-10142: Escucha: ¿qué pájaro canta así en los bosques de España en primavera? → El cuco: Listen: Britons used to write to The Times newspaper to say they'd heard this bird's first call of spring. Which bird is it? → Cuckoo
- brands-and-adverts-10: overlap like q-9525: I'm a sticky dark brown spread for toast. I'm made from yeast left over from brewing beer. Britons even use my name to mean something you either love or hate. What am I? → Marmite: It's dark brown and sticky, it comes in a squat jar, and its adverts say “Love it or hate it”. What do most Brits do with it? → Spread it thinly on toast
- brands-and-adverts-13: overlap like q-11396: En España lleva una lucecita verde en el techo cuando está libre y un aparato que va marcando lo que tienes que pagar. ¿Qué es? → Un taxi: It's tall and boxy, you can wave one down in the street, and its driver must learn every London street by heart. What is a London “black cab”? → A taxi
- christmas-in-britain-1: overlap like q-18856: On Christmas Jumper Day, British pupils wear festive jumpers to school and bring a small donation. Who does the money help? → Children who need help: Complete the name: on Christmas ___ Day, British pupils swap their uniform for a festive knitted top and give a small donation. → Jumper
- christmas-in-britain-9: overlap like q-7221: Son tres, viajan en camellos y en el pesebre llegan el 6 de enero. ¿Qué regalos le llevan al Niño Dios? → Oro, incienso y mirra: In the nativity story, these three kings bring gifts to baby Jesus. One is gold. What are the other two? → Frankincense and myrrh
- christmas-in-britain-12: overlap like q-18774: Look at this close-up. In Britain, what do people often call this jolly man, besides Santa Claus? → Father Christmas: Every December I sit in a cosy grotto inside a big shop. Children queue to whisper their wishes to me, and an elf hands out presents. Who am I? → Father Christmas
- christmas-in-britain-13: overlap like q-3278: In the old tale of Aladdin, who comes out when you rub a magic lamp like this one? → A genie: In the panto “Aladdin”, what pops out when someone rubs an old lamp like this one? → A genie
- christmas-in-britain-14: overlap like q-2399: You're riding to the royal ball in a coach made from a pumpkin. At what time does the magic end? → At midnight: You're watching the panto “Cinderella” and the palace clock begins to strike. At what time must she run from the ball? → Midnight
- christmas-in-britain-16: overlap like q-9507: Every winter I fill British theatres. My dame is a man in a dress, and when the villain says “Oh yes it is!”, the crowd shouts “Oh no it isn't!”. What am I? → A pantomime: Every winter, where do British families shout “He's behind you!” at the top of their voices? → At a pantomime
- cities-and-towns-2: overlap like birds-2: These ravens live at the Tower of London. An old legend says that as long as they stay, they keep something safe. What? → The kingdom: An old legend says something terrible will happen if the ravens ever leave the Tower of London. What? → The kingdom will fall
- cities-and-towns-3: overlap like q-9585: I sailed from Plymouth on the Endeavour, mapped the coast of New Zealand and in 1770 landed in Australia. Who am I? → Captain James Cook: This explorer learned to sail on coal ships out of Whitby, and his statue stands on the town's West Cliff. Who is he? → Captain James Cook
- cities-and-towns-7: overlap like q-9727: This bronze archer stands below the walls of an English castle, not far from a famous forest. Who is he? → Robin Hood: This statue of a legendary outlaw stands beside Nottingham Castle. Who is he? → Robin Hood
- cities-and-towns-13: duplicate like q-2239: This glass skyscraper is nicknamed “the Gherkin”. In which city is it? → London: This close-up shows part of a famous clock tower. In which city is it? → London
- comedians-and-panel-shows-9: overlap like q-0337: ¿Cómo se llaman los correos electrónicos basura que llegan por montones sin que nadie los haya pedido, como anuncios y promociones raras? → Spam: In a Monty Python sketch, Vikings sing about it and a café puts it in almost every dish. Today, junk email is named after it. What is it? → Spam
- creatures-ghosts-and-superstitions-2: overlap like q-3768: I'm a green ghost pirate who sails a ghost ship and loves to scare SpongeBob. My name comes from an old sailors' legend. Who am I? → The Flying Dutchman: I'm a ghost ship, doomed to sail the oceans forever and never reach port. In 1881, a young prince who later became King George V wrote that he saw me. What am I? → The Flying Dutchman
- creatures-ghosts-and-superstitions-4: overlap like q-18470: Look at this circle of mushrooms in the grass. In old British stories, who danced in circles like this at night? → Fairies: You're walking in a British wood and spot a tiny painted door at the foot of a tree. Who is it said to be for? → Fairies
- creatures-ghosts-and-superstitions-9: overlap like q-6539: Look: this winged boy is Cupid. What happens to someone hit by one of his arrows? → They fall in love: Puck is a cheeky English sprite, also called Robin Goodfellow. In a Shakespeare play, he squeezes a magic flower's juice onto sleeping eyes. What happens when they wake? → They fall in love with the first creature they see
- creatures-ghosts-and-superstitions-10: overlap like q-4394: Which Hogwarts teacher teaches Harry's class the spell “Riddikulus”, using a wardrobe with a Boggart inside? → Remus Lupin: In Harry Potter, you open an old wardrobe and a boggart jumps out. What does it turn into? → Whatever scares you most
- early-britain-0: overlap like q-4678: Look at this stone tool. What did Stone Age people use it for? → Cutting and chopping: Look at this sharp, chipped stone found buried in Britain. Who made tools like this? → Stone Age people
- early-britain-3: overlap like q-9619: On the longest day of the year, crowds gather here to watch what rise in line with the stones? → The sun: Around 21 June, crowds gather at Stonehenge before dawn and cheer as the Sun rises over the stones. What makes the day special? → It's the longest day of the year
- early-britain-4: overlap like q-5889: Medieval castles had thick, tall walls that were very hard to break. What were most of them made of? → Stone: You're visiting the Tower of London, where William the Conqueror built the big White Tower. What is it built from? → Stone
- early-britain-9: overlap like q-1440: ¿Qué pueblo navegaba en drakares, barcos largos con una cabeza de dragón en la proa? → Los vikingos: In 793, raiders in longships attacked the monastery on this island, Lindisfarne. Who were they? → The Vikings
- early-britain-11: overlap like q-18483: In 1066, near Hastings, English foot soldiers stood behind a wall of shields. Which army charged them with knights on horses and archers? → The Normans: This abbey stands in the French region that William the Conqueror ruled as duke before 1066. Which region? → Normandy
- early-britain-12: overlap like q-0263: La Edad del Bronce se llama así por el bronce, que se hace mezclando cobre con otro metal. ¿Con cuál? → Estaño: Bronze Age Britons made bronze by mixing copper with another metal, which they mined in Cornwall. Which metal? → Tin
- georgians-and-victorians-0: overlap like q-9637: You're in Trafalgar Square, counting the giant bronze lions around the base of Nelson's Column. How many are there? → 4: Admiral Nelson stands on top of this column in Trafalgar Square. How many bronze lions guard its base? → 4
- georgians-and-victorians-2: overlap like q-16071: Sie krochen durch enge Stollen, knüpften Fäden an laufenden Spinnmaschinen und bekamen nur ein paar Pfennige. Wer arbeitete so im 19. Jahrhundert? → Kinder: Georgian and Victorian chimneys were narrow and twisty, and long brushes were rare. So who did master sweeps send up inside them? → Small children
- georgians-and-victorians-7: overlap like q-0932: J. M. Barrie es a 'Peter Pan' como Lewis Carroll es a… → Alicia en el país de las maravillas: This character hosts a very strange tea party. Who wrote the book he comes from? → Lewis Carroll
- georgians-and-victorians-8: overlap like q-18731: In Britain, scones with jam and clotted cream are a treat traditionally served with a pot of tea. At what time of day? → In the afternoon: This classic British treat comes on a tiered stand with scones and tiny sandwiches. What is it called? → Afternoon tea
- georgians-and-victorians-14: overlap like q-9556: This giant arch towers over the stadium where the FA Cup Final is played. Which stadium is it? → Wembley Stadium: After all the earlier rounds, the FA Cup ends with the final. At which stadium is it usually played? → Wembley Stadium
- hills-moors-and-national-parks-5: overlap like q-4347: Look at this Border Collie. What kind of working dog is it on a farm? → A herding dog: This clever black-and-white dog works on hill farms, runs in wide circles and herds sheep with just a stare. Which breed is it? → Border collie
- hills-moors-and-national-parks-7: overlap like q-4261: Ratatouille is also a real dish from France. Which of these does NOT go in it? → Banana: Peter Rabbit sneaks into Mr McGregor's garden. Which of these does he NOT find growing there? → Bananas
- hills-moors-and-national-parks-9: overlap like q-18356: In April 1802, Dorothy Wordsworth saw wild flowers by Ullswater that inspired her brother's most famous poem. Which flowers? → Daffodils: A poet saw a crowd of these flowers by a lake in the Lake District and wrote “I Wandered Lonely as a Cloud”. Who was he? → William Wordsworth
- hills-moors-and-national-parks-17: overlap like q-6604: In 2023, Prince Philip's old title “Duke of Edinburgh” went to his youngest son. Who became Duchess of Edinburgh? → Sophie: Teenagers like these go on hikes for the Duke of Edinburgh's Award. Which royal is it named after? → Prince Philip
- landmarks-and-castles-9: overlap like q-3914: The Western Wall holds up the side of Jerusalem's Temple Mount. What kind of rock is it built from? → Limestone: York Minster, one of the largest Gothic cathedrals in northern Europe, glows a pale cream. What stone is it built from? → Limestone
- landmarks-and-castles-13: overlap like q-18600: You're watching a coronation in Westminster Abbey. Who traditionally places the crown on the new monarch's head? → The Archbishop of Canterbury: I wear a tall pointed hat, I place the crown on new kings and queens, and my special chair is in Canterbury Cathedral. What is my title? → Archbishop
- languages-of-britain-5: overlap like q-17861: On CBeebies, Mr Tumble talks with his voice and also with what? → Hand signs: You're watching CBeebies and a character signs in Makaton as he talks, then dresses up as lots of funny relatives. Who is he? → Mr Tumble
- languages-of-britain-17: overlap like q-9540: What is the highest mountain in the United Kingdom? → Ben Nevis: “Ben” comes from the Gaelic for mountain. You're standing on top of Ben Nevis, Britain's highest. About how high are you? → About 1,345 m
- legendary-heroes-0: overlap like creatures-ghosts-and-superstitions-13: These giant steel horse heads stand by a canal in Scotland. They are named after which Scottish water spirit? → Kelpies: I live in Scottish lochs and rivers. I look like a lovely horse, but if you climb on my back, I gallop straight into the deep water. What am I? → A kelpie
- legendary-heroes-9: overlap like q-5886: In Disney's 1973 film “Robin Hood”, the hero is a fox. Which animal plays the greedy Prince John? → A lion: In Disney's “Robin Hood”, Prince John is a thumb-sucking lion. What does he send the Sheriff of Nottingham out to do? → Collect taxes
- middle-ages-0: overlap like q-6606: A legend says Edward I showed his newborn son to the Welsh at Caernarfon Castle as their new prince. Which king did that baby become? → Edward II: You're at Caernarfon Castle, where King Edward I's son was born. In which year did that son become the first English Prince of Wales? → 1301
- middle-ages-2: overlap like q-5578: This huge round table hangs in Winchester, England. In legend, why did King Arthur's knights sit at a round table? → So no knight sat above the others: King Arthur's knights met at Camelot, at a huge table with no corners. Why was it round, according to legend? → So no knight sat at the head
- middle-ages-8: overlap like q-1440: ¿Qué pueblo navegaba en drakares, barcos largos con una cabeza de dragón en la proa? → Los vikingos: Vikings raided Britain in this long, narrow wooden boat, with oars, one square sail and often a dragon head at the front. What is it called? → A longship
- middle-ages-9: overlap like q-19015: This famous artwork, almost 70 m long, tells the story of the Norman Conquest of England. What is it called? → The Bayeux Tapestry: This close-up comes from a famous medieval artwork, almost 70 metres (230 ft) long, that tells the story of 1066. What is it called? → The Bayeux Tapestry
- middle-ages-11: overlap like q-9646: Robin Hood wants to marry Maid Marian in Sherwood Forest. Which member of his band can perform the wedding? → Friar Tuck: I'm a noblewoman in an old English legend. I can ride and shoot a bow, and I love an outlaw who robs the rich in Sherwood Forest. Who am I? → Maid Marian
- pop-and-rock-5: overlap like q-18337: Put together on The X Factor in 2010, this five-piece was the first British group whose debut album went straight to No. 1 in the US. Who? → One Direction: Before solo hits like “As It Was”, Harry Styles sang in which boy band? → One Direction
- pop-and-rock-12: overlap like q-1419: Kalush Orchestra ganó Eurovisión 2022 con «Stefania». ¿Qué país, mostrado en el mapa, representaba? → Ucrania: Liverpool hosted Eurovision 2023 for another country. It had won in 2022 with Kalush Orchestra but couldn't host safely. Which country? → Ukraine
- pop-and-rock-15: overlap like q-0072: ¿Qué banda británica cantaba 'Hey Jude' y 'Yellow Submarine'? → The Beatles: Paul McCartney played bass, wrote “Yesterday” and later formed Wings. Which famous band was he in first? → The Beatles
- pub-and-playground-games-13: overlap like q-18335: Every autumn, British children drill a hole in these shiny brown seeds. What do they do with them next? → Play conkers with them: Every autumn, British children hunt for spiky green cases like this one under trees. What's inside? → A conker
- regional-specialities-10: overlap like q-19065: Richard III died at the Battle of Bosworth in 1485. In 2012, his skeleton was found under a car park in which city? → Leicester: This hard cheese is dyed deep orange with annatto and named after the city where Richard III was found under a car park. Which cheese? → Red Leicester
- accents-and-dialects-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It's on the big signs as you drive into Wales. What does the Welsh word “croeso” mean? → Welcome
- birds-2: overlap like cities-and-towns-2: An old legend says something terrible will happen if the ravens ever leave the Tower of London. What? → The kingdom will fall: These ravens live at the Tower of London. An old legend says that as long as they stay, they keep something safe. What? → The kingdom
- twentieth-century-15: overlap like q-6605: Queen Elizabeth II died in 2022. Who became king after her? → Charles: Which monarch reigned just before King Charles III? → Queen Elizabeth II
- twentieth-century-16: overlap like q-18701: Flowers like these bloomed on First World War battlefields and inspired the poppies Britons wear in November. In which region were those fields? → Flanders: The guns of the First World War fell silent at 11 o'clock on the 11th day of which month? → November
- twentieth-century-17: fact-check wrong: Answer 1996 is right, but hint 3 says Euro 96 was held in the 'late 1990s'. 1996 is the mid-1990s.: You're in a pub where everyone is singing “It's coming home”. That song, “Three Lions”, was written for a tournament England hosted in which year? → 1996
- brands-and-adverts-2: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: A Cadbury Flake comes in a yellow wrapper. What is it made of? → Folded milk chocolate
- cities-and-towns-10: overlap like q-3898: The middle of this London bridge can open upward. Why was it built to do that? → To let tall ships pass: Its road lifts up in the middle to let tall ships through, and tourists often mix it up with London Bridge. Which bridge is it? → Tower Bridge
- comedians-and-panel-shows-0: hard fail: correct 2, unambiguous 5, no_giveaway 4, no_overlap 5: This BBC telethon happens every November and its mascot is a yellow bear with a spotty bandage over one eye. What is it called? → Children in Need
- comedians-and-panel-shows-14: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Before he became a comedian and the Taskmaster, what was Greg Davies's job? → Teacher
- creatures-ghosts-and-superstitions-13: overlap like legendary-heroes-0: I live in Scottish lochs and rivers. I look like a lovely horse, but if you climb on my back, I gallop straight into the deep water. What am I? → A kelpie: These giant steel horse heads stand by a canal in Scotland. They are named after which Scottish water spirit? → Kelpies
- creatures-ghosts-and-superstitions-17: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In Britain, a silver coin is often stirred into this Christmas dessert. Who is said to get good luck for the year? → The person who finds the coin
- early-britain-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Chedworth and Lullingstone are famous Roman villas in England, with mosaic floors and their own baths. What was a villa? → A rich family's country house
- hills-moors-and-national-parks-0: overlap like q-17270: Vivo en los montes de España, en otoño grito muy fuerte para buscar pareja y cada año se me caen las cuernas y me salen otras. ¿Qué animal soy? → El ciervo: In autumn on the Scottish hills, stags roar loudly to show off to each other. What is a stag? → A male deer
- hills-moors-and-national-parks-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Look at the photo. What kind of event is this? → A sheepdog trial
- landmarks-and-castles-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Penrhyn Castle near Bangor looks like a Norman fortress. In which century was it built? → 19th century
- landmarks-and-castles-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: I'm about 350 million years old, and Edinburgh Castle sits on top of me. What am I? → An extinct volcano
- languages-of-britain-11: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: In British Sign Language, Deaf people give one to friends, it often shows a trait like curly hair or glasses, and it saves spelling a name letter by letter. What is it? → A sign name
- pop-and-rock-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In 2005, which cartoon character's version of “Axel F”, first a mobile ringtone, kept Coldplay off UK No. 1? → Crazy Frog
- pub-and-playground-games-12: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In darts, what does it mean to play a game of 501? → Players start on 501 and count down to zero
- regional-specialities-17: overlap like q-18853: On I'm a Celebrity, famous faces take on Bushtucker Trials in the Australian jungle. In Australian slang, what is “tucker”? → Food: Royal Navy sailors, Scousers and Geordies all use the word “scran”. If someone asks “Fancy some scran?”, what are they offering? → Food
- rugby-and-cricket-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In rugby union I'm worth five points. You score me by pressing the ball down over the other team's line. What am I? → A try
- sitcoms-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Del Boy from Only Fools and Horses loves to say “Lovely jubbly”. What does he mean by it? → Brilliant, wonderful
- soaps-and-dramas-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Danny Dyer was born in Canning Town and ran EastEnders' Queen Vic as Mick Carter. Which accent is he famous for? → Cockney
- soaps-and-dramas-14: hard fail: correct 2, unambiguous 5, no_giveaway 4, no_overlap 5: If you'd watched every episode of BBC One's daytime soap Doctors, from 2000 to 2024, about how many would you have seen? → About 5,000
- sporting-events-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Old Tom Morris won The Open four times in the 1860s. Back then, the winner's prize was made of red leather and silver. What was it? → A belt
- sweets-and-crisps-6: fact-check wrong: The fun fact has the colours the wrong way round. Walkers salt & vinegar is in a blue packet and cheese & onion is in a green one. Some other brands use the opposite scheme. The answer, vinegar, is right.: It's sour and sharp, it's splashed on chips at the chip shop, and it pairs with salt in a famous crisp flavour. What is it? → Vinegar
- sweets-and-crisps-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: A Cadbury Creme Egg has a gooey white and yellow filling. What is the filling made to look like? → A real egg's white and yolk
- traditional-music-and-dance-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: You're watching morris dancers, and one prances about in a hooped frame with a little wooden head and a tail. What's he called? → The Hobby Horse
- twentieth-century-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I came down your street before sunrise, leaving glass bottles with foil tops on your doorstep, and I drove a quiet electric float. Who am I? → The milkman
- rivers-coasts-and-islands-7: overlap like q-17060: In vielen Ostseebädern führt so eine lange Brücke ins Meer hinaus. Wofür wurde sie ursprünglich gebaut? → Damit Schiffe anlegen konnten: Southend Pier, shown here, stretches far out into the Thames Estuary. Why was it first built? → To let boats land at low tide
- rugby-and-cricket-10: overlap like q-18640: Starting in 1988, Wigan won rugby league's Challenge Cup how many years in a row? → 8: I'm a rugby league trophy first won by Batley in 1897, I'm open to amateur clubs too, and my final is usually at Wembley. What am I? → The Challenge Cup
- rugby-and-cricket-17: overlap like q-18638: Rugby referees whistle for it all the time on wet days, and the other team gets a scrum. What is a “knock-on”? → Losing the ball forwards off your hand or arm: Rugby players pack down together like this in a scrum. What is a scrum for? → To restart play after a small mistake
- sitcoms-5: overlap like accents-and-dialects-10: It's Nessa's catchphrase in Gavin and Stacey, she says it all over Barry Island, and it's a laid-back Welsh greeting. What does “What's occurring?” mean? → What's going on?: In Gavin & Stacey, which character greets everyone with “What's occurring?” → Nessa
- soaps-and-dramas-1: hard fail: correct 3, unambiguous 4, no_giveaway 5, no_overlap 5: AC-12 hunts bent coppers in BBC's Line of Duty. Which of these groups does NOT appear in Line of Duty? → UCOS
- soaps-and-dramas-16: overlap like q-18089: You're in the Rovers Return snug in the 1960s, next to a stern woman in a hairnet sipping milk stout. Who is she? → Ena Sharples: Ena Sharples's hairnet became Coronation Street's most famous hat. Which actress wore it from 1960? → Violet Carson
- soaps-and-dramas-17: overlap like q-18414: Jacqueline Wilson's Tracy Beaker calls her home “the Dumping Ground” and waits for her mum to come back. What kind of place is it? → A children's care home: You're watching Heartstopper on Netflix. Which of these characters will you NOT meet? → Tracy Beaker
- sporting-events-1: overlap like q-18777: Scottish men wear a kilt to weddings, on Burns Night and at Highland games, often with a sporran. What is a kilt? → A knee-length tartan skirt: This Highland dancer's kilt is made from a woollen cloth with crossing coloured stripes. What is that cloth called? → Tartan
- sporting-events-15: overlap like q-4749: In 2013, this player became the first British man in 77 years to win the Wimbledon singles title. Who is he? → Andy Murray: In 2013, who became the first British man in 77 years to win the Wimbledon singles title on this court? → Andy Murray
- sporting-events-17: overlap like q-19086: This orange cheese has “Double” in its name, and a wheel of it is chased down Cooper's Hill every year. Which place is it named after? → Gloucester: You're at the bottom of Cooper's Hill, watching people tumble down after a rolling cheese. In which English county are you? → Gloucestershire
- sweets-and-crisps-10: overlap like q-9696: Which high-street shop had a famous pick and mix counter, began in the United States, and closed its UK shops in 2009? → Woolworths: At a British sweet shop or cinema, you take a scoop and a paper bag and fill it with any sweets you like. What is this called? → Pick 'n' mix
- sweets-and-crisps-13: overlap like q-2635: The 1971 musical film “Willy Wonka & the Chocolate Factory”, with the song “Pure Imagination”, is based on a book by which author? → Roald Dahl: As a boy in Wales, I hid a mouse in a grumpy shopkeeper's jar of gobstoppers. I later wrote “Matilda” and “The BFG”. Who am I? → Roald Dahl
- traditional-music-and-dance-0: overlap like q-4061: You're watching the Eurovision Song Contest when Irish dancers with still arms and flying feet start Riverdance. Which decade is it? → The 1990s: Riverdance began in 1994 as a seven-minute interval act at Eurovision. What did it grow into the next year? → A full-length stage show
- traditional-music-and-dance-14: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: On which festival do English villagers traditionally dance round a pole like this? → May Day
- tudors-and-stuarts-2: overlap like q-5358: Henry VIII had six wives. Which of these names did NONE of them have? → Mary: Which English king had more wives than any other, with six in all? → Henry VIII
- tudors-and-stuarts-7: overlap like q-18208: On Bonfire Night, a stuffed dummy like this one is put on top of the bonfire. Who is it named after? → Guy Fawkes: I was born in York, fought for Spain and called myself Guido. On 5 November 1605, I was caught under Parliament. Who am I? → Guy Fawkes
- tudors-and-stuarts-13: overlap like q-18140: Black wooden beams on white walls, like in this close-up: which style of building is this? → Tudor: Houses with black wooden beams and white walls, like this one, are often named after which royal family? → The Tudors
- tudors-and-stuarts-16: overlap like q-18146: What do you call a roof like this one, made from straw or reeds? → Thatch: Look at the roof of this old English cottage. What is it made of? → Straw or reeds
- twentieth-century-3: overlap like q-18266: Ringo Starr was born in the Dingle in 1940, joined a famous band in 1962 and later narrated Thomas the Tank Engine. Which city is he from? → Liverpool: I was one of the four Beatles during Beatlemania. I played the drums, sang “Yellow Submarine” and later narrated “Thomas the Tank Engine” on TV. Who am I? → Ringo Starr
- twentieth-century-5: overlap like q-18265: The Spice Girls turned “Girl Power” into a famous slogan with their first hit, “Wannabe”. In which decade? → The 1990s: The Spice Girls' first single, “Wannabe”, went to number one around the world. In which decade did it come out? → The 1990s
- twentieth-century-13: overlap like q-4773: During World War II, a wailing siren in a city sent people running to shelters. What was it warning them about? → Enemy planes: I sat on rooftops and poles in wartime Britain. When enemy planes were coming, I wailed up and down so people ran to the shelters. What am I? → An air raid siren
