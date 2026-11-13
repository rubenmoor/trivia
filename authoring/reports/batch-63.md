# batch-63

Made by `qgen batch` on 2026-11-13 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): home-and-public-services, british-films, drinks, art-and-architecture, customs-and-ceremonies, regional-specialities, writers-and-poets, crown-and-state, plants-and-gardens, flags-and-emblems, pub-and-playground-games, team-gb-and-olympians, birds, languages-of-britain, scientists-and-inventors, comedians-and-panel-shows, brands-and-adverts, parliament-and-prime-ministers, soaps-and-dramas, landmarks-and-castles, holidays-and-celebrations, sitcoms, money-and-shopping, sweets-and-crisps, pop-and-rock, rivers-coasts-and-islands, legendary-heroes, cities-and-towns
- Merged: 281 (q-18140…q-18420)
- Approved: 268
- Needs work: 13
- Dropped by the pipeline: 89
- Reviewed by: claude-opus-5-5
- Claude calls: 594, about $78.33 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-61, batch-62; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-61 | batch-62 | batch-63 |
|---|---|---:|---:|---:|
| source locale |  | es | en | en |
| drafts |  | 272 | 402 | 370 |
| skipped slots |  | 250 | 102 | 134 |
| dropped |  | 102 | 72 | 89 |
| drop rate | ≤ 20.0 % | 37.5 % ✗ | 17.9 % ✓ | 24.1 % ✗ |
| dropped: hard fail correct |  | 3 | 4 | 1 |
| dropped: hard fail unambiguous |  | 2 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 17 | 16 | 21 |
| dropped: overlap |  | 78 | 49 | 65 |
| dropped: duplicate |  | 4 | 3 | 3 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 170 | 330 | 281 |
| approved |  | 160 | 311 | 268 |
| needs_work |  | 10 | 19 | 13 |
| needs_work rate | ≤ 20.0 % | 5.9 % ✓ | 5.8 % ✓ | 4.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.4 % ✓ | 3.0 % ✓ | 1.8 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.6 % ✓ | 1.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.9 % ✗ | 0.3 % ✓ | 1.1 % ✗ |
| needs_work: media | ≤ 10.0 % | 1.2 % ✓ | 2.4 % ✓ | 1.1 % ✓ |
| media: no pick in review 1 |  | 16 | 40 | 25 |
| media: recovered by research |  | 15 | 36 | 22 |
| media: no pick at record |  | 1 | 4 | 3 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 32.0 % ✗ | 13.2 % ✓ | 19.2 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 41.3 % ✗ | 74.8 % ✓ | 69.7 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.44 ✓ | 1.00 ✓ | 1.10 ✓ |
| approved 11–15 |  | 28 | 77 | 62 |
| top move | ≤ 25.0 % | 14.7 % ✓ | 14.5 % ✓ | 19.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 85.3 % | 89.7 % | 73.3 % |
| values stimulus |  | 4 | 3 | 4 |
| top clue | ≤ 60.0 % | 32.9 % ✓ | 42.7 % ✓ | 49.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.9 % ✓ | 24.5 % ✓ | 20.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.2 % ✓ | 24.8 % ✓ | 21.7 % ✓ |
| values lens |  | 10 | 9 | 11 |
| media share | 15.0 %–50.0 % | 14.7 % ✗ | 10.3 % ✗ | 26.7 % ✓ |
| mean fun | ≥ 3.40 | 3.33 ✗ | 3.64 ✓ | 3.66 ✓ |
| cost $ |  | $55.68 | $81.87 | $75.29 |
| $ per approved | ≤ $0.35 | $0.35 ✓ | $0.26 ✓ | $0.28 ✓ |
| calls |  | 347 | 637 | 534 |
| calls per approved |  | 2.17 | 2.05 | 1.99 |
| wall time h |  | 1.76 | 2.77 | 2.29 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 57 (4 %)
- Major among review needs work: 1 of 3 (33 %)
- Problems by kind: giveaway 10 (1 major), fact 1 (0 major), overlap 2 (1 major), media 4 (1 major), difficulty 1 (1 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.04

Major findings on approved questions:

- **q-18258**: overlap — The facts are right. Alice sits on the bank wondering whether making a daisy chain is worth getting up for when the White Rabbit runs past. The 1862 boat trip near Oxford is also correct, and the daisy-chain image is a suitable essential picture. The problem is that related q-5579 (which girl drops in on the Mad Hatter's tea party → Alice) asks the same thing in other words: name the heroine of Alice in Wonderland. A family that sees both questions gets the same answer from the same piece of knowledge. (http://127.0.0.1:8001/review/q-18258)
- **q-18313**: giveaway, difficulty — The facts check out: the map was made around 1300 on one calfskin, it is the largest medieval world map still around, it has east at the top and Jerusalem in the centre, and there really was a plan to sell it in 1988. The trouble is that the question says "world map" and the description says "Satnav", while "Mappa" sounds just like "map" and none of the three wrong answers is a map, so anyone can pick the answer from its name. That makes it about a 5, not a 10. A fix would be to drop "world map" from the question, or to make the wrong answers other medieval maps. (http://127.0.0.1:8001/review/q-18313)

## Needs work

- **q-18140** (art-and-architecture) Black wooden beams on white walls, like in this close-up: which style of building is this? → Tudor: This overlaps with approved q-17832, which opens with “Black-and-white “Tudor-style” houses line many British suburbs”. Anyone who has seen that question knows that black beams on white walls means Tudor, so each question gives the other away. Also, the fun fact's claim that builders reused ship timbers is a popular but exaggerated myth. If this question is kept, limit the fun fact to reused barn and house timbers.
- **q-18157** (brands-and-adverts) Since 2007, trains like this one have left London from which station? → St Pancras: Fact check: uncertain. The answer is right (Eurostar moved to St Pancras in Nov 2007, from Waterloo). The claim that French visitors found the Waterloo station name 'rather cheeky' is a popular joke, but I found no source for it, and I didn't search for one.
- **q-18168** (british-films) Desmond Llewelyn played the gadget master Q in 17 Bond films. In which decade did he first play him? → The 1960s: Fact check: wrong. Hint 1 is false. Llewelyn's Q worked with four Bond actors (Connery, Moore, Dalton, Brosnan). Q doesn't appear in On Her Majesty's Secret Service, so Lazenby is not one. Also, in The World Is Not Enough, Cleese plays R, Q's assistant. 'Future replacement' is correct, since Cleese's character takes over as Q in Die Another Day.
- **q-18205** (flags-and-emblems) This close-up shows part of a flag with the Union Jack in its corner and red stars with white borders. Which country's flag is it? → New Zealand: None of the candidates is the essential close-up of New Zealand's flag. A new search isn't allowed, so the slot needs a hand-picked image: a clear close-up of the New Zealand flag showing the Union Jack and the red stars with white borders, with no text in it. No suitable picture found for this question.
- **q-18215** (home-and-public-services) On a UK phone, dialling 112 reaches the same emergency services as 999. Where is 112 the standard emergency number? → Europe: The media slot is 'essential' with a note asking for a sign showing 112, but no candidate shows 112, and no new search is allowed. The question already says 112, so the image isn't needed to answer it. Make the role illustrative; candidate 1 (a public payphone keypad) would then fit. Separately, hint 2 rules out two of the three wrong answers (North America and Australia), which leaves only Europe or South America. Consider making it vaguer. No suitable picture found for this question.
- **q-18231** (languages-of-britain) “Pal”, British slang for a friend, came into English in the 1600s from the Romani language. What did it originally mean in Romani? → Brother: Hint 1 ("It describes a family member") gives the answer away: Brother is the only family member among the four options (Neighbour, Horse, Traveller). Hint 1 should stay vague, for example about how close the people are, without saying they are related. Hint 2 should move to the family idea instead.
- **q-18235** (languages-of-britain) The Scots Gruffalo begins “a moose took a dauner through the deep mirk wid”. Three of these are Scots words. Which one is Welsh? → Cwtch: Hint 1 gives away too much: it gives the meanings of the three Scots options, so anyone who knows "wee" = small or "bairn" = child gets the answer by elimination from the first hint. Hint 1 should be vague, for example about where Welsh is spoken, without explaining the other options. Also, the Scots Gruffalo quote has nothing to do with what is asked (none of its words are options). It only makes the question longer, so cut it to something like "Three of these are Scots words. Which one is Welsh?"
- **q-18274** (pub-and-playground-games) You're playing rounders in PE. Which of these will you NOT find on a rounders pitch? → Home plate: The description (“Like baseball…”) and hint 1 (“Think of rounders' famous American cousin”) both point straight at baseball, and “Home plate” is the only baseball term among the options. Anyone who knows that can answer before any real hint. The description should play on rounders or PE without mentioning baseball. Hint 1 should be vague, for example about how rounders is laid out with posts, and the baseball link should wait until hint 2 or 3.
- **q-18310** (flags-and-emblems) This crowned portcullis with chains is a famous British badge. Whose badge is it? → The Houses of Parliament: None of the candidates shows the crowned portcullis badge. The question needs an essential close-up of the badge, and no new search is allowed. A new search such as "Parliament portcullis emblem" or "crowned portcullis Westminster" might find one. The question text itself is fine. No suitable picture found for this question.
- **q-18317** (landmarks-and-castles) I'm a Yeoman Warder at the Tower of London. Each day I feed my feathered charges raw meat and tuck them into their night pens. Who am I? → The Ravenmaster: This overlaps q-0218 (approved), which asks which birds always live at the Tower of London (ravens). The two answer each other: once you've seen “The Ravenmaster”, q-0218 is solved, and if you know about the Tower ravens, this one comes down to the only raven option. Hint 2 even repeats q-0218's “at least six must stay” legend.
- **q-18341** (regional-specialities) I'm a biscuit topped with a marshmallow dome, coated in milk chocolate and wrapped in red and silver foil. What am I? → A Tunnock's Teacake: The description ("Scotland's shiniest export") rules out options before any hint. Jaffa Cakes are made in Stockport and Wagon Wheels by Burton's in England and Wales, so only the Teacake and the Penguin are left. Hint 1 ("a family bakery near Glasgow") then picks out the answer on its own, since the Penguin is a big-brand McVitie's biscuit. The description should play on the theme without naming Scotland, and hint 1 should be vaguer, for example about how old the recipe is, not where it's made.
- **q-18362** (scientists-and-inventors) In which decade did James Dyson's first bagless vacuum cleaner, the DC01, go on sale in Britain? → The 1990s: Hint 2 says Dyson's first design, the G-Force, was sold in Japan "in the late 1980s". It went on sale there in about 1986, which is the mid-1980s. The fact check was only "uncertain", and I can't confirm "late". Change the hint to "in the mid-1980s" or just "in the 1980s". The rest is correct: DC01 in 1993, 5,127 prototypes, the sawmill cyclone idea, and Harry Potter in 1997. Fact check: uncertain. The DC01 (1993) and the 5,127 prototypes are right. The hint says his first design sold in Japan in the 'late 1980s', but the G-Force launched in Japan in about 1986, which is mid-1980s. I did not search this, so it comes from memory.
- **q-18392** (soaps-and-dramas) In February 2010, EastEnders broadcast its first-ever live episode to celebrate a birthday. Which one? → 25th: Overlaps draft q-18395 (“In which decade did EastEnders begin?” → the 1980s): the 2010 date plus a 1980s start leaves only the 25th, so each question gives the other away. Hint 1 (“started in the mid-1980s”) has the same problem: with 2010 in the question, it rules out every wrong option, so it hands over the answer at the first hint. Keep only one of the two questions. If this one stays, hint 1 needs to be vague and must not date the show's start.

## Question axes

- move: analogy 8, cause_effect 14, count 3, estimate 8, identify 54, made_of 11, name_concept 18, odd_one_out 9, origin 31, purpose 17, record 16, sequence 17, when 24, who 31, word_meaning 20
- stimulus: detail 14, map_outline 1, none 206, photo 60
- clue: completion 10, direct 140, riddle 20, scenario 30, three_facts 81
- answer_kind: group 36, number 11, person 49, place 44, thing 54, time 30, word 57
- lens: body_senses 7, educational_media 28, everyday 24, history 60, language 54, nature 7, pop_culture 61, popular_science 2, school 24, science_news 7, university 7

## Dropped by the pipeline

- art-and-architecture-2: overlap like q-0620: Haces galletas con un cortador en forma de estrella y todas salen iguales. El cortador es a la galleta como el ___ es al grafiti que se repite igual en muchas paredes. → Esténcil: Banksy hides his face, comes from England's South West and sprays rats on walls. What does he use to spray his pictures so fast? → Stencils
- art-and-architecture-3: duplicate like q-7485: Mira la foto: esta estatua de Bolívar, de 1846, es el monumento público más antiguo de Bogotá. ¿De qué material está hecha? → Bronce: Four giant lions like this one guard Nelson's Column in London. What are they made of? → Bronze
- art-and-architecture-6: overlap like q-3936: This famous painting by John Everett Millais shows a Shakespeare character floating in a stream among flowers. Who is she? → Ophelia: This detail is from John Everett Millais's “Ophelia”. Which group of Victorian artists did Millais help found? → The Pre-Raphaelite Brotherhood
- art-and-architecture-10: overlap like q-15013: Diese gläserne Kuppel sitzt seit 1999 auf dem Reichstagsgebäude in Berlin. Welcher Architekt hat sie entworfen? → Norman Foster: Which architect designed this glass tower in the City of London, nicknamed “the Gherkin”? → Norman Foster
- art-and-architecture-15: overlap like q-15315: Mira la foto de la Terminal 4 del aeropuerto de Madrid-Barajas. ¿Qué arquitecto británico la diseñó con el Estudio Lamela? → Richard Rogers: These steel pipes and glass lifts belong to the Lloyd's building in London. Which architect designed it? → Richard Rogers
- birds-3: overlap like q-9553: Which birds do people in Britain count with the rhyme “One for sorrow, two for joy”? → Magpies: An old British rhyme about magpies begins “One for sorrow, two for joy”. Some people salute a lone magpie to keep its bad luck away. What does “sorrow” mean? → Sadness
- birds-14: overlap like q-8593: Swallows fly south before winter, whales swim to warm seas to have babies, and salmon swim back to the river where they hatched. What is this called? → Migration: Every autumn, I send swallows and cuckoos from Britain all the way to Africa. Every spring, I bring them back again. What am I? → Migration
- birds-16: overlap like q-10142: Escucha: ¿qué pájaro canta así en los bosques de España en primavera? → El cuco: In Britain, hearing this bird's two-note call means spring has come. A clock is named after it, and its name sounds like its call. What bird is it? → Cuckoo
- brands-and-adverts-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: What is Weetabix mainly made from? → Wheat
- brands-and-adverts-17: overlap like q-9516: Cadbury's chocolate factory sits in a village built for its workers, in a city with more canals than Venice. Which city? → Birmingham: The Flake was invented in 1920 when a Cadbury worker saw leftover chocolate falling into thin folds. In which city was that factory? → Birmingham
- british-films-13: overlap like q-6741: He hardly says a word, drives a little green car and carries a teddy bear everywhere. Which country does Mr. Bean come from? → United Kingdom: You're watching Mr Bean. Which of these does he NOT have? → A pet dog
- cities-and-towns-0: overlap like q-18147: Glasgow's Duke of Wellington statue has worn a traffic cone on its head almost nonstop since which decade? → The 1980s: This statue of the Duke of Wellington nearly always wears a traffic cone on his head. In which city does it stand? → Glasgow
- cities-and-towns-8: overlap like q-18175: This seaside tower in Blackpool opened in 1894. Which famous landmark inspired it? → The Eiffel Tower: These colourful lights stretch along the seafront every autumn. Which seaside town's famous Illuminations are they? → Blackpool
- cities-and-towns-13: duplicate like q-2239: This glass skyscraper is nicknamed “the Gherkin”. In which city is it? → London: This famous clock tower is called Big Ben. In which city is it? → London
- cities-and-towns-16: duplicate like q-2461: Look at this shaggy cow with long horns and a fringe over its eyes. Which country does this breed come from? → Scotland: New Year's Eve parties like this one are called Hogmanay. In which country of the UK does this name come from? → Scotland
- comedians-and-panel-shows-4: overlap like q-9559: It was started in 1985 by Richard Curtis and Lenny Henry, and it runs Red Nose Day. Which charity is it? → Comic Relief: I first appeared in 1988. Every other spring, people across Britain stick me on their faces and cars to raise money for Comic Relief. What am I? → A red nose
- comedians-and-panel-shows-16: overlap like q-18069: Dawn French plays a chocolate-loving vicar in a village whose parish council is run by David Horton. Which county is that village in? → Oxfordshire: Who played the vicar Geraldine Granger in The Vicar of Dibley, and was half of a famous double act with Jennifer Saunders? → Dawn French
- crown-and-state-2: overlap like q-5577: This country's national animal is the unicorn, its flag is a diagonal white cross on blue, and it's famous for bagpipes. Which country? → Scotland: It is Scotland's national animal, it comes from old legends, and it is often shown wearing a golden chain. What is it? → Unicorn
- crown-and-state-11: overlap like q-5357: The old royal coat of arms of England shows golden lions on a red shield. How many lions? → 3: On the shield of the royal coat of arms, two quarters stand for England. How many golden lions are in each? → 3
- flags-and-emblems-2: overlap like q-9607: Scotland's flag, the Saltire, is a white diagonal cross on a blue background. Whose cross is it? → Saint Andrew: Look at this flag. What is the special word for the X-shaped cross on it? → Saltire
- flags-and-emblems-4: overlap like q-9735: Horatio Nelson stands on top of Nelson's Column. He was an admiral: what did he command? → Warships: I lost an arm and the sight of one eye, I won a great sea battle in 1805, and now I stand on a tall column in Trafalgar Square. Who am I? → Horatio Nelson
- flags-and-emblems-5: overlap like q-14066: Die Schwäbische Alb war vor rund 150 Millionen Jahren Meeresboden und ist heute voller Höhlen. Aus welchem Gestein besteht sie vor allem? → Kalkstein: The Rock of Gibraltar rises 426 m (1,398 ft) above the sea and is full of caves, like St Michael's Cave. What kind of rock is it made of? → Limestone
- flags-and-emblems-7: overlap like q-9605: Neighbours set up long tables with bunting and food right in the middle of their road, like this. What is this called? → A street party: Strings of little flags like these hang over streets at British parties and fêtes. What are they called? → Bunting
- flags-and-emblems-8: overlap like q-6605: Queen Elizabeth II died in 2022. Who became king after her? → Charles: You get your change in a shop and spot a new coin. Whose head replaced Queen Elizabeth II's on British coins? → King Charles III
- flags-and-emblems-10: overlap like q-2366: Which country's flag sits in the top corner of this flag of Australia? → United Kingdom: This small flag sits in the top corner of Australia's flag. What is it called? → Union Jack
- holidays-and-celebrations-4: overlap like flags-and-emblems-10: This small flag sits in the top corner of Australia's flag. What is it called? → Union Jack: Complete the nickname of the UK's red, white and blue flag: the Union … → Jack
- holidays-and-celebrations-5: overlap like q-3861: Who is this British queen? → Queen Victoria: This monarch was the first British ruler ever to celebrate a Diamond Jubilee, in 1897. Who is she? → Queen Victoria
- holidays-and-celebrations-8: overlap like q-5577: This country's national animal is the unicorn, its flag is a diagonal white cross on blue, and it's famous for bagpipes. Which country? → Scotland: Look at this close-up of an instrument heard at Burns Night suppers. Which part of the UK is it most famous from? → Scotland
- holidays-and-celebrations-9: overlap like flags-and-emblems-14: In an old legend, England's patron saint rides out with his lance to save a princess. What creature does St George fight? → A dragon: St George's Day parades in England on 23 April often have a huge model of which creature from his legend? → A dragon
- holidays-and-celebrations-10: overlap like q-1118: Soy un santo muy famoso de Irlanda. Cuenta la leyenda que usaba un trébol de tres hojas para enseñar, y en mi día, el 17 de marzo, medio mundo se viste de verde. ¿Quién soy? → San Patricio: On 17 March, a bank holiday in Northern Ireland, many people pin on a shamrock. What is a shamrock? → A small three-leafed plant
- holidays-and-celebrations-12: overlap like q-18117: These dancers wave white hankies as they skip and jump outside village pubs. Who are they? → Morris dancers: On the May Day bank holiday, you might see bells on shins and white hankies like these. Which dancers wear them? → Morris dancers
- languages-of-britain-0: overlap like q-17890: Look at the dragon on this flag. How many legs does it have? → 4: Welsh speakers call it “Y Ddraig Goch”, and it has stood on the green and white flag of Wales since 1959. What is it called in English? → The Red Dragon
- languages-of-britain-11: overlap like q-18109: Male voice choirs grew up in its coal-mining valleys, and its national anthem calls it a land of “poets and singers”. Which country is it? → Wales: “Cymru” is what its own people call this country. In their language its capital is Caerdydd, and it lies west of England. Which country? → Wales
- legendary-heroes-1: overlap like q-9805: In 1588, fires were lit on hilltops across England, each one seen from the next. What were they warning of? → The Spanish Armada: In 1588, Elizabeth I rode among her troops at Tilbury and said she had “the heart and stomach of a king”. What attack were they waiting for? → The Spanish Armada
- legendary-heroes-9: overlap like q-5886: In Disney's 1973 film “Robin Hood”, the hero is a fox. Which animal plays the greedy Prince John? → A lion: In Disney's 1973 cartoon, Robin Hood wears a green hat, is a superb archer and has orange fur and a bushy tail. What animal is he? → A fox
- money-and-shopping-0: overlap like q-3990: I’m at the end of the supermarket and I beep a lot, but there’s no cashier: you scan your items and pay all by yourself. What am I? → A self-checkout: This close-up shows part of a supermarket machine famous for saying “Unexpected item in the bagging area”. Where in the shop is it? → At the self-checkout
- money-and-shopping-1: overlap like flags-and-emblems-8: You get your change in a shop and spot a new coin. Whose head replaced Queen Elizabeth II's on British coins? → King Charles III: My face is on Britain's newest coins and banknotes. I was Prince of Wales for over 60 years, and I was crowned in 2023. Who am I? → King Charles III
- money-and-shopping-6: overlap like q-9238: Lidl hat ein gelb-blau-rotes Logo, den Spruch „Lidl lohnt sich“ und Filialen in fast jedem Ort. Was für ein Geschäft ist Lidl? → Supermarkt: Tesco started as Jack Cohen's market stall in London in 1919. Today it's the UK's biggest grocer, with thousands of stores. What is Tesco? → A supermarket
- money-and-shopping-13: overlap like q-4991: My face was on coins in Canada, Australia and Britain for decades. On Canada's gold-colored dollar coin, I shared the coin with a loon. Who am I? → Queen Elizabeth II: Look at this £2 coin. Whose face is on it? → Queen Elizabeth II
- parliament-and-prime-ministers-6: overlap like q-9659: In October 2022, a newspaper livestreamed a lettuce like this one next to a photo of Liz Truss. Why? → To see if it would outlast her as PM: In October 2022, the Daily Star began livestreaming a lettuce next to a photo of Liz Truss. Roughly how long had it been running when she resigned? → About a week
- parliament-and-prime-ministers-10: overlap like q-9639: On New Year's Eve, Londoners count down as Big Ben strikes midnight. What is Big Ben, strictly speaking? → The great bell: This tower's official name is the Elizabeth Tower. Its famous nickname, “Big Ben”, first belonged to what? → The great bell inside it
- plants-and-gardens-2: overlap like q-9314: Am Waldrand hängen im Sommer noch harte, rote Brombeeren. Welche Farbe haben sie, wenn sie reif und süß sind? → Schwarz: I grow on prickly brambles in the hedgerow. I start green, turn red, then go shiny black, and in September families pick me for crumble. What am I? → A blackberry
- plants-and-gardens-9: overlap like q-17964: It opened in Oxford in 1683, is often called Britain's first public museum, and began with the Tradescant family's collection of curiosities. What is it? → The Ashmolean Museum: In the Garden Museum in Lambeth, London, you stand by the tomb of a royal gardener whose “Ark” of curiosities became the start of Oxford's Ashmolean Museum. Who was he? → John Tradescant
- plants-and-gardens-10: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: In English villages, children dance around a pole like this, weaving its ribbons together. Which festival is it for? → May Day
- plants-and-gardens-11: overlap like q-9570: On 1 March, many people pin a daffodil or a leek to their coat, and children may dress up in tall black hats. Which day is it? → St David's Day: On 1 March, many people in Wales pin this flower to their clothes. Which day are they celebrating? → St David's Day
- pop-and-rock-3: overlap like q-0072: ¿Qué banda británica cantaba 'Hey Jude' y 'Yellow Submarine'? → The Beatles: Paul McCartney came from Liverpool, played bass left-handed and wrote “Hey Jude”. Which band was he in? → The Beatles
- pop-and-rock-7: overlap like q-4861: In 1967, a Cambridge PhD student spotted a radio signal from space that ticked every 1.3 seconds: the first pulsar. Who was she? → Jocelyn Bell Burnell: Its 1979 cover shows radio pulses from the first pulsar ever found, and its band's singer was Ian Curtis. Which city's music scene did it come out of? → Manchester
- pub-and-playground-games-13: overlap like q-9639: On New Year's Eve, Londoners count down as Big Ben strikes midnight. What is Big Ben, strictly speaking? → The great bell: I spy with my little eye something beginning with B! I'm a huge bell in a London clock tower, and I bong every hour. What am I? → Big Ben
- regional-specialities-0: overlap like q-9767: Sticks of seaside rock have a town's name printed all the way through them. Which of these towns is NOT at the seaside? → Birmingham: I'm a hard, sugary stick, pink on the outside, and a town's name runs all the way through me. Where do families usually buy me? → At the seaside
- regional-specialities-14: overlap like q-9542: This pastry with a crimped edge is named after which English county? → Cornwall: Ice cream like this, made with thick clotted cream and sold on the beaches of England's far south-west tip, is named after which county? → Cornwall
- birds-6: overlap like writers-and-poets-1: Harry Potter's pet Hedwig is an animal like this one. What kind of animal is it? → An owl: Ron Weasley is to a rat as Harry Potter is to… → A snowy owl
- brands-and-adverts-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This game is named after a falcon, Falco subbuteo. Its inventor wanted the falcon's English name, but couldn't register it. What was it? → The Hobby
- sweets-and-crisps-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In a famous story, the Everlasting Gobstopper is a sweet you can suck all year without it getting smaller. Where was it invented? → Willy Wonka's chocolate factory
- team-gb-and-olympians-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: David Weir won four Paralympic golds at London 2012. In which sport? → Wheelchair racing
- cities-and-towns-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Edinburgh's Hibernian, who play at this stadium, take their name from the Latin word for a country. Which people founded the club in 1875? → Irish immigrants
- customs-and-ceremonies-10: overlap like q-3223: It's an honor from the British monarch, the ceremony uses a sword, and men who get it are called “Sir”. What is a woman called who gets it herself? → Dame: At an investiture, the monarch touches a kneeling person on each shoulder with a sword. Complete the phrase: they have been “… a knight”. → Dubbed
- customs-and-ceremonies-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which of these does NOT happen during Freshers' Week at a British university? → Final exams
- drinks-2: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: It lives in loads of British lunchboxes and first went on sale in 2000. What is a Fruit Shoot? → A small fruit drink
- drinks-3: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: A hot toddy is an old cure for a cold. Besides hot water, honey and lemon, which drink goes into it? → Whisky
- drinks-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It's often knitted and sits over a teapot like a woolly hat. What is a tea cosy for? → Keeping the tea warm
- flags-and-emblems-14: overlap like holidays-and-celebrations-9: St George's Day parades in England on 23 April often have a huge model of which creature from his legend? → A dragon: In an old legend, England's patron saint rides out with his lance to save a princess. What creature does St George fight? → A dragon
- flags-and-emblems-15: hard fail: correct 3, unambiguous 5, no_giveaway 3, no_overlap 5: Sailors call it the “Red Duster”: a red flag with the Union Flag in its corner. Which ships fly it? → British merchant ships
- holidays-and-celebrations-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Each December, many schools hold a Save the Children charity day named after a festive item. Which one? → A Christmas jumper
- holidays-and-celebrations-7: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Hundreds of years ago, young servants in Britain got one Sunday off in spring. Where did they go? → Back to their home church and family
- home-and-public-services-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This close-up shows the badge on the cover of a passport. Which country issued it? → The United Kingdom
- languages-of-britain-15: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: I'm a small piece of wood on a string. In some 1800s Welsh schools, I was hung round the neck of any child heard speaking Welsh. What am I? → The Welsh Not
- parliament-and-prime-ministers-1: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Big black security gates have closed off Downing Street since 1989. Back in the 1970s, who could walk up to Number 10's front door? → Any member of the public
- parliament-and-prime-ministers-16: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Instead of clapping, what do MPs in the House of Commons traditionally call out when they agree with a speech? → “Hear, hear!”
- plants-and-gardens-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: British children pick this fluffy seed head and blow on it, counting each puff. What do they pretend to find out? → Tell the time
- regional-specialities-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In the North of England and in Wales, fizzy drinks have a short nickname that copies the sound of a bottle being opened. What is it? → Pop
- rivers-coasts-and-islands-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This model village on the Wirral peninsula was built from 1888 for the workers of a nearby factory. What did the factory make? → Soap
- rivers-coasts-and-islands-12: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: At St Michael's Mount in Cornwall, low tide is to walking across the causeway as high tide is to… → Taking a boat
- sitcoms-13: overlap like q-10781: You walk into the Dunder Mifflin office from The Office. Which of these characters would you NOT find working there? → Leslie Knope: You're in the Slough office of paper firm Wernham Hogg. Which of these does NOT work for David Brent? → Mark Corrigan
- rivers-coasts-and-islands-6: overlap like q-9518: A Geordie comes from the city with this famous bridge. Which city is it? → Newcastle: They come from the banks of the River Tyne, have a famous accent, and many cheer for Newcastle United. What are they called? → Geordies
- scientists-and-inventors-12: overlap like q-4510: Around 1666, in an English garden, something fell from a tree and got a young scientist thinking about why things fall. What fell? → An apple: This apple tree grows in Lincolnshire. Legend says a scientist got his idea about gravity watching an apple fall from it. Who was he? → Isaac Newton
- scientists-and-inventors-15: overlap like q-1181: Si la locomotora de vapor es al carbón, las locomotoras de carga de hoy suelen ser al… → Diésel: You're on the platform as Flying Scotsman, the famous steam engine, puffs in. Which of these does it NOT need to run? → Diesel
- sweets-and-crisps-1: overlap like q-14742: Pringles come stacked in a tall tube. What vegetable are they mostly made from? → Potatoes: Hula Hoops are crunchy little rings you can wear on your fingertips before you eat them. What are they mainly made from? → Potato
- sweets-and-crisps-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This crisp flavour tastes sharp and sour, makes your lips tingle, and is named after what you sprinkle on fish and chips. Which flavour is it? → Salt and vinegar
- sweets-and-crisps-16: overlap like q-18278: Tayto crisps like these are made in the grounds of a castle in Tandragee, County Armagh. Which flavour are they most famous for? → Cheese and onion: Finish the name of this classic British crisp flavour: cheese and…? → Onion
- team-gb-and-olympians-2: overlap like q-9809: Eddie the Eagle became a hero at the 1988 Calgary Olympics despite finishing last in ski jumping. What did the “Eddie the Eagle rule” then require? → Minimum qualifying results to compete: Eddie “the Eagle” Edwards became a British hero at the 1988 Winter Olympics by using one of these. What is it? → A ski jump
- team-gb-and-olympians-8: overlap like q-2249: “I'm lit by the sun's rays and a curved mirror, then runners carry me all the way to the Games.” In which country am I lit? → Greece: The flame for the London 2012 torch relay was lit at these ancient ruins, then flown to Cornwall. Which country are they in? → Greece
- team-gb-and-olympians-10: overlap like q-3718: At the London 2012 Olympics opening, James Bond picked up Queen Elizabeth II. From which royal home did they fly off? → Buckingham Palace: I usually save the world with clever gadgets. For the London 2012 opening ceremony, I collected the Queen from Buckingham Palace on film. Who am I? → James Bond
- team-gb-and-olympians-13: overlap like q-4801: Which of these colors is NOT on the flag of France? → Green: Team GB athletes often wrap themselves in the Union Flag after winning. Which colour is NOT on it? → Green
- writers-and-poets-2: overlap like q-6169: This German city is home to the carmaker whose slogan is “Vorsprung durch Technik”, and in Mary Shelley's novel, Victor Frankenstein builds his creature there. Which city? → Ingolstadt: This woman began writing “Frankenstein” when she was just 18. Who was she? → Mary Shelley
- writers-and-poets-8: overlap like q-3087: In “The Lord of the Rings”, Frodo's journey begins in the Shire. Where must it end, so the One Ring can be destroyed? → Mount Doom: In “The Lord of the Rings”, which hobbit is given the job of destroying a magic ring like this? → Frodo
- writers-and-poets-9: overlap like q-2168: ¿Qué personaje de Shakespeare dice '¡Fuera, maldita mancha!' mientras camina dormido? → Lady Macbeth: Which Shakespeare character tells her husband to “screw your courage to the sticking place”? → Lady Macbeth
- writers-and-poets-10: overlap like q-18134: With my friend William Wordsworth, I published “Lyrical Ballads” in 1798. Its longest poem tells of a sailor who shoots an albatross. Who am I? → Samuel Taylor Coleridge: I dreamed of a pleasure-dome in Xanadu, but a visitor “from Porlock” interrupted me as I wrote it down, so I never finished. Who am I? → Samuel Taylor Coleridge
- writers-and-poets-12: overlap like q-5587: This is Agatha Christie, the “Queen of Crime”. Her famous detective Hercule Poirot comes from which country? → Belgium: You're reading a mystery solved by a neat Belgian detective who relies on his “little grey cells”. Who created him? → Agatha Christie
- writers-and-poets-17: overlap like q-4340: Narnia is to a wardrobe as the Land of Oz is to a… → Tornado: You step through the back of an old wardrobe into a snowy land with a lamp-post and a talking faun. Where are you? → Narnia
