# batch-62

Made by `qgen batch` on 2026-11-13 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): pop-and-rock, traditional-music-and-dance, nursery-rhymes-and-singalongs, writers-and-poets, childrens-books-and-comics, art-and-architecture, childrens-tv, soaps-and-dramas, game-shows-and-presenters, british-films, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, team-gb-and-olympians, sporting-events, pub-and-playground-games, slang-and-words, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, brands-and-adverts, transport, school-and-childhood, home-and-public-services, flags-and-emblems, crown-and-state
- Merged: 330 (q-17810…q-18139)
- Approved: 311
- Needs work: 19
- Dropped by the pipeline: 72
- Reviewed by: claude-opus-5-5
- Claude calls: 697, about $84.64 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-60, batch-61; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-60 | batch-61 | batch-62 |
|---|---|---:|---:|---:|
| source locale |  | en | es | en |
| drafts |  | 255 | 272 | 402 |
| skipped slots |  | 195 | 250 | 102 |
| dropped |  | 86 | 102 | 72 |
| drop rate | ≤ 20.0 % | 33.7 % ✗ | 37.5 % ✗ | 17.9 % ✓ |
| dropped: hard fail correct |  | 0 | 3 | 4 |
| dropped: hard fail unambiguous |  | 1 | 2 | 0 |
| dropped: hard fail no_giveaway |  | 20 | 17 | 16 |
| dropped: overlap |  | 64 | 78 | 49 |
| dropped: duplicate |  | 1 | 4 | 3 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 169 | 170 | 330 |
| approved |  | 152 | 160 | 311 |
| needs_work |  | 17 | 10 | 19 |
| needs_work rate | ≤ 20.0 % | 10.1 % ✓ | 5.9 % ✓ | 5.8 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.4 % ✓ | 2.4 % ✓ | 3.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.2 % ✓ | 0.0 % ✓ | 0.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.2 % ✗ | 2.9 % ✗ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 5.9 % ✓ | 1.2 % ✓ | 2.4 % ✓ |
| media: no pick in review 1 |  | 25 | 16 | 40 |
| media: recovered by research |  | 18 | 15 | 36 |
| media: no pick at record |  | 8 | 1 | 4 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 26.3 % ✗ | 32.0 % ✗ | 13.2 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 60.7 % ✓ | 41.3 % ✗ | 74.8 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.97 ✗ | 1.44 ✓ | 1.00 ✓ |
| approved 11–15 |  | 24 | 28 | 77 |
| top move | ≤ 25.0 % | 14.8 % ✓ | 14.7 % ✓ | 14.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 79.9 % | 85.3 % | 89.7 % |
| values stimulus |  | 4 | 4 | 3 |
| top clue | ≤ 60.0 % | 40.2 % ✓ | 32.9 % ✓ | 42.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 24.3 % ✓ | 25.9 % ✓ | 24.5 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.9 % ✓ | 18.2 % ✓ | 24.8 % ✓ |
| values lens |  | 11 | 10 | 9 |
| media share | 15.0 %–50.0 % | 20.1 % ✓ | 14.7 % ✗ | 10.3 % ✗ |
| mean fun | ≥ 3.40 | 3.51 ✓ | 3.33 ✗ | 3.64 ✓ |
| cost $ |  | $51.84 | $55.68 | $81.87 |
| $ per approved | ≤ $0.35 | $0.34 ✓ | $0.35 ✓ | $0.26 ✓ |
| calls |  | 362 | 347 | 637 |
| calls per approved |  | 2.38 | 2.17 | 2.05 |
| wall time h |  | 1.90 | 1.76 | 2.77 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 57 (2 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 9 (1 major), fact 1 (0 major), ambiguity 1 (1 major), media 2 (0 major), difficulty 2 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.77

Major findings on approved questions:

- **q-17849**: ambiguity, giveaway — Hammer is right for the book and the 2022 musical. But Wikipedia says the well-known 1996 film makes Trunchbull a shot putter, hammer thrower and javelin thrower at the 1972 Munich Olympics, so “Javelin” can also be defended. Also, the question text asks “in which event did she throw?”, which rules out Pole vault and High jump straight away, leaving a 50/50 between two throwing events, and hint 1 says the same thing again. (http://127.0.0.1:8001/review/q-17849)

## Needs work

- **q-17818** (accents-and-dialects) You'll hear it in Nottingham, Derby and Stoke, and the “duck” isn't a bird. What does “ay up me duck” mean? → Hello, my dear: The description calls the phrase "a greeting", which is the answer's defining trait. Among the four options only "Hello, my dear" is a greeting, so the answer is given away before any hint. Hint 1 ("It's said when you meet someone") gives it away the same way. The description should play on the duck/pond theme without saying what kind of phrase it is, and hint 1 needs to be vaguer, for example about the region.
- **q-17821** (accents-and-dialects) Complete the jokey Scottish phrase heard in countless films and cartoons: “Och aye the…” → noo: Hint 1 ("about time") gives the answer away: noo is the only time word among the options, since loch, toon and bairn mean a lake, a town and a child. Hint 2 ("right away") does the same. The description also gets a fact wrong: it says "Three words", but "Och aye the noo" has four. Hints 1 and 2 need to be vaguer (for example about where the phrase shows up or who says it), and the description should drop the word count.
- **q-17822** (accents-and-dialects) In old Yorkshire, “Don't thee-tha me!” warned someone who had called you “thee” or “tha”. What were they being? → Too familiar: Hint 2 gives the answer away. Saying that “thee” and “tha” were for close friends and family, while “you” was polite and distant, already spells out “too familiar”. It is also stronger than hint 3. Hint 2 should say something vaguer, for example that the saying was about manners or who has the right to speak to whom in a certain way, and the close-friends idea should move to hint 3. The fact, options, description and wording are otherwise fine.
- **q-17834** (brands-and-adverts) Which brand was famously sold with the line “Does exactly what it says on the tin”? → Ronseal: None of the image candidates fit. Candidates 1 and 2 are the same 1882 "Canada Lumberman" gazette header, and candidate 3 is an Indian miniature painting. Neither shows wood staining or a fence, and no new search is allowed. The question text itself is fine. It needs a new illustrative image, for example a "garden fence wood stain" photo with no brand names visible. No suitable picture found for this question.
- **q-17865** (childrens-tv) Sooty is a yellow bear with black ears who whispers in his presenter’s ear. What kind of puppet is he? → A glove puppet: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-17880** (crown-and-state) The guards who wear this red-and-gold uniform have a famous nickname. What is it? → Beefeaters: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-17907** (game-shows-and-presenters) On Strictly Come Dancing, what is the highest score one judge can give a couple for a dance? → 10: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-17921** (languages-of-britain) In British Sign Language's two-handed alphabet, pointing to your thumb is to A as pointing to your little finger is to… → U: Hint 2 gives the answer away. The question already says the thumb is A, so "the five fingertips are the five vowels, in order" leaves only U for the little finger. Hint 3 then adds nothing. Hint 2 should only point towards the vowel pattern, for example by saying that the fingertips stand for a special group of letters, without saying which group or that they go in order.
- **q-17937** (money-and-shopping) Look at this £20 note. What is it made of? → Polymer, a thin plastic: None of the six candidates shows a £20 note. They are all 19th-century book scans (a Civil War soldier, a beggars' tavern, Turner's house in Maiden Lane, a potato seed advert, a wheat field, cucumbers). The question says "Look at this £20 note", so the essential image has to show the polymer Turner £20, and no new search is allowed. Banknote copyright may mean Commons has no usable photo. If none can be found, rework the question so it doesn't depend on the picture, for example with an illustrative image of a wallet or till. Separately, the answer "Polymer, a thin plastic" is longer than the wrong options and stands out; shorten it to "Polymer (plastic)" or similar. No suitable picture found for this question.
- **q-17941** (nursery-rhymes-and-singalongs) In “Hey Duggee”, the Squirrels try a new activity in every episode. What do they earn at the end? → A badge: The fact check is uncertain, and I can't confirm from my own knowledge that Duggee wears lots of badges on his chest (hint 3). Duggee is mainly shown with his whistle. The fun fact's claims that Duggee has "a badge for nearly everything" and that the show won "Emmy awards" (plural) also need checking. Replace hint 3 with something safe, such as "Duggee gives them out at the end of each episode", and limit the fun fact to awards you can confirm. Fact check: uncertain. Answer (badge) and the BAFTA/Emmy claim are true. I could not verify hint 3, that Duggee wears lots of badges on his chest.
- **q-17959** (pub-and-playground-games) In a book from 1865, I hold croquet games where flamingos are the mallets, hedgehogs are the balls and soldiers bend over to be the hoops. Who am I? → The Queen of Hearts: The picked picture has an unsuitable licence (pd-no-reason: public domain without a template).
- **q-17972** (british-films) You're watching Michael Palin as a knight who shouts “Ni!” while others gallop to the sound of coconut halves. When did this Python film come out? → 1975: No adequate media candidate: all three pictures show sundot kulangot, a Filipino sweet sold in small red-painted shells tied with palm strips. They are not halved coconut shells and have nothing to do with the film or its coconut-clopping horse gag. No new search is allowed. A fresh search such as "coconut shell halves" or "medieval knight armour" would fit. No suitable picture found for this question.
- **q-17996** (pop-and-rock) In the blind auditions of The Voice UK, how many big spinning chairs face away from the singer? → 4: This repeats the fact in approved q-2826 (“In the blind auditions of The Voice, coaches sit with their backs to the singer. How many coaches are there in most versions?” → 4). The number of spinning chairs is the number of coaches, so it's the same question in other words. Drop it, or replace it with a different Voice UK fact.
- **q-18012** (school-and-childhood) In Year 6 in England, children take SATs and often go on a school trip away from home. What comes next for them? → Starting secondary school: Hint 1 ("they say goodbye to their primary teachers") tells players straight away that the children are leaving primary school, which points to secondary school and rules out Reception. Hint 2 ("a different teacher for each subject") nearly gives it away as well. Hint 1 should be vague, for example about the time of year or how they feel, and hint 2 should not describe secondary school.
- **q-18042** (sayings-and-idioms) Complete the rhyme for something really simple: “Easy peasy, lemon…” → Squeezy: Hint 2 (“about something you do with your hands”) gives the answer away: it applies only to “Squeezy”, not to Sneezy, Breezy or Cheesy, so it solves the question at the second hint. Replace it with a vaguer hint, e.g. one about the lemon or the kitchen that doesn't point to an action done by hand.
- **q-18048** (school-and-childhood) In England, many four-year-olds start “Reception” in September. Where is Reception class? → At primary school: None of the media candidates fits: the sheet shows a 19th-century Irish tavern engraving, two adobe house gates in Santa Fe and the Philippine coat of arms. None of them is a school cloakroom, and no new search is allowed. The description also gives the answer away: "No room service, no luggage trolley" rules out the hotel, and "glitter and glue" points to young children, which rules out secondary school and university. Rewrite it to play on the school theme without hinting at the children's age or ruling out the hotel. No suitable picture found for this question.
- **q-18055** (school-and-childhood) On a British school dinner menu, what is “sponge and custard”? → Cake with warm sweet sauce: Hint 2 gives the answer away. Hint 1 (“eaten after the main course”) already leaves only the cake and the jelly. Hint 2 (“sweet, and served warm”) then repeats the answer's own words “warm sweet” and rules out the cold jelly. Hint 2 should stay vaguer, for example about the texture or how it's cooked, and must not say “warm”.
- **q-18083** (soaps-and-dramas) ITV's long-running drama The Bill took its title from slang. Who are “the Old Bill”? → The police: Hint 2 gives the answer away: of the four options (police, judges, tax collectors, bailiffs), only the police work shifts at a “station”. Replace hint 2 with a vaguer clue that doesn't point to a police station, for example one about how long the show ran or which channel it was on.
- **q-18099** (sporting-events) In 2023, Wimbledon relaxed its all-white rule a little and allowed dark-coloured undershorts. Which players was this change for? → Women players: Hint 2 gives the answer away: naming Billie Jean King, a famous campaigner for women in tennis, as the one asking for the change points straight at "Women players" (the rater flagged this too). Hint 2 needs to be replaced with a vaguer clue, for example one about the tennis world or the timing, that doesn't point to women.

## Question axes

- move: analogy 6, cause_effect 13, count 25, estimate 10, identify 48, made_of 11, name_concept 27, odd_one_out 19, origin 23, purpose 18, record 7, sequence 10, when 27, who 46, word_meaning 40
- stimulus: detail 5, none 296, photo 29
- clue: completion 19, direct 141, riddle 37, scenario 42, three_facts 91
- answer_kind: group 32, number 38, person 64, place 33, thing 55, time 27, word 81
- lens: body_senses 21, educational_media 22, everyday 60, history 57, language 56, nature 1, pop_culture 82, school 26, university 5

## Dropped by the pipeline

- accents-and-dialects-10: overlap like q-2964: I was born in Liverpool, I wore small round glasses, and I wrote the song “Imagine”. Who am I? → John Lennon: Three of these famous people were born in Belfast and grew up with its accent. Which one was born in Liverpool? → John Lennon
- art-and-architecture-2: overlap like q-5536: I am made of hundreds of palm leaves tied onto poles. Rain runs off me, and I keep the house cool in the hot sun. What am I? → A thatched roof: This kind of roof is made from dried straw or reeds, keeps old country cottages cosy, and sometimes has a straw bird on top. What is it called? → A thatched roof
- art-and-architecture-7: overlap like q-4889: A soda can is light, shiny and can be recycled again and again without wearing out. Which metal is it usually made of? → Aluminum: Piccadilly Circus's winged archer, unveiled in 1893, was one of the first big statues cast in a light metal now used for fizzy drink cans. Which metal? → Aluminium
- art-and-architecture-13: overlap like q-6172: This seaside palace in Brighton, England, looks like it came from India. Which royal had it built? → George IV: You're strolling past the cream-white terraces on Brighton's seafront, built in the Regency style. Who is that style named after? → The future King George IV
- brands-and-adverts-12: duplicate like q-6612: Red buses with two floors like this one are a famous sight in which city? → London: Toy cars like this were first sold in boxes the size of a box of matches. In which city was the Matchbox brand born? → London
- brands-and-adverts-16: overlap like q-6255: When do most people eat a bowl of Kellogg's Corn Flakes with milk? → At breakfast: Look at these wheat biscuits. When do people in Britain usually eat them? → Breakfast
- brands-and-adverts-17: overlap like q-2441: Heinz ketchup is to tomatoes as Heinz's very first bottled product, from 1869, is to what? → Horseradish: “Beanz Meanz Heinz” was made up in London in 1967. Heinz itself was founded in 1869 by Henry J. Heinz, selling bottled horseradish. Where? → The USA
- british-films-4: overlap like q-1585: Soy británico, trabajo para el servicio secreto y pido mi vodka martini «agitado, no revuelto». ¿Quién soy? → James Bond: Look at this cocktail. Which author gave his spy the habit of ordering it “shaken, not stirred”? → Ian Fleming
- british-films-7: overlap like q-0083: ¿Qué película de 1997 sobre un barco que se hunde ganó 11 premios Óscar? → Titanic: Kate Winslet starred as Rose in a 1997 film set on board the ship in this photo. Which ship is it? → Titanic
- british-films-8: overlap like q-5005: I took over my country's government in 1940, gave rousing speeches on the radio, and raised two fingers in a V for victory. Who am I? → Winston Churchill: In May 1940 I become Prime Minister. In “Darkest Hour”, I ride the London Underground to ask ordinary people whether Britain should keep fighting. Who am I? → Winston Churchill
- british-films-11: overlap like q-1988: El título del musical 'Chitty Chitty Bang Bang' imita el sonido que hace… ¿qué? → El motor de un vehículo: This famous car flies in a 1968 British musical film with Dick Van Dyke. What is its name? → Chitty Chitty Bang Bang
- british-films-13: overlap like q-2635: The 1971 musical film “Willy Wonka & the Chocolate Factory”, with the song “Pure Imagination”, is based on a book by which author? → Roald Dahl: The film “Matilda the Musical”, with Emma Thompson as Miss Trunchbull, is based on a book by which author? → Roald Dahl
- childrens-books-and-comics-4: overlap like q-2635: The 1971 musical film “Willy Wonka & the Chocolate Factory”, with the song “Pure Imagination”, is based on a book by which author? → Roald Dahl: You unwrap a Wonka bar and find a Golden Ticket inside. Which author wrote the book where this happens? → Roald Dahl
- childrens-books-and-comics-7: overlap like q-9635: Which of these characters was NOT created by Charles Dickens? → Mary Poppins: Which of these characters is NOT in the story of Captain Hook? → Mary Poppins
- childrens-books-and-comics-9: overlap like q-6350: In J. K. Rowling's Harry Potter books, someone calls you a “Muggle”. What does that say about you? → You have no magic: In Harry Potter, it's what wizards call people with no magic. The Dursleys are this, and so are Hermione's parents. What's the word? → Muggle
- childrens-tv-6: overlap like q-9509: Wallace loves Wensleydale cheese, his dog Gromit never says a word, and their films are often a Christmas treat on the BBC. What are the two made of? → Modelling clay: I’m a dog who never speaks, I love knitting and reading, and my owner can’t get enough cheese. Who am I? → Gromit
- comedians-and-panel-shows-12: duplicate like q-11873: In which decade did “Mighty Morphin Power Rangers” first air on American TV? → The 1990s: In which decade did Reeves and Mortimer's surreal panel show Shooting Stars first air on BBC Two? → 1990s
- crown-and-state-4: overlap like q-11036: Wer rief bei einem Ritterturnier die Ritter auf und musste dafür alle ihre Wappen erkennen? → Herold: The College of Arms was founded in 1484 and grants coats of arms. Its officers have titles like Rouge Dragon and Bluemantle. What are they called? → Heralds
- crown-and-state-6: overlap like q-3228: I'm a London church. In 2011, Prince William and Catherine Middleton got married under my roof. Where am I? → Westminster Abbey: Prince William married Catherine Middleton in this church in 2011. Which church is it? → Westminster Abbey
- crown-and-state-11: overlap like q-6605: Queen Elizabeth II died in 2022. Who became king after her? → Charles: In 2022 the UK got a new monarch, so new 50p coins got a new head. Whose head is on them now? → King Charles III
- flags-and-emblems-1: overlap like q-9607: Scotland's flag, the Saltire, is a white diagonal cross on a blue background. Whose cross is it? → Saint Andrew: Legend says this white cross once appeared in a blue sky before a battle. Which saint's cross is it? → St Andrew
- flags-and-emblems-7: overlap like q-9585: I sailed from Plymouth on the Endeavour, mapped the coast of New Zealand and in 1770 landed in Australia. Who am I? → Captain James Cook: This is Australia's flag. Its Union Jack goes back to which explorer, who claimed Australia's east coast for Britain in 1770? → Captain James Cook
- flags-and-emblems-9: overlap like q-9580: Westminster Abbey, January 1066: Harold Godwinson is crowned king. Who was crowned there next, on Christmas Day that same year? → William the Conqueror: Almost every English and British coronation since 1066 has taken place in this church. Which one? → Westminster Abbey
- football-7: overlap like q-13070: Die deutschen Frauen verloren das EM-Finale 2022 mit 1:2 nach Verlängerung. Der Gegner war Gastgeber und holte seinen ersten großen Titel. Welches Land? → England: In which year did Leah Williamson lift the Women's Euros trophy as England captain at Wembley? → 2022
- home-and-public-services-6: overlap like crown-and-state-16: In 1509 I created a royal bodyguard, now called the Gentlemen at Arms. In 1520 I met the French king at the Field of the Cloth of Gold. Who am I? → Henry VIII: I was a Tudor king. In 1516 I appointed a “Master of the Posts”, the start of what became Royal Mail. I also had six wives. Who am I? → Henry VIII
- home-and-public-services-11: overlap like q-9661: I'm big and red, I carry long ladders and a hose, and Fireman Sam rides in me through Pontypandy. What am I? → A fire engine: Look closely at this part of a vehicle. What is the whole vehicle? → A fire engine
- languages-of-britain-9: overlap like q-9576: To the Romans, “Deva” was a big legionary fortress with Britain's largest stone amphitheatre. What is the city called today? → Chester: The Romans named a fortress after the goddess of the River Dee, and it later got Britain's biggest amphitheatre. What did they call it? → Deva Victrix
- money-and-shopping-2: overlap like crown-and-state-11: In 2022 the UK got a new monarch, so new 50p coins got a new head. Whose head is on them now? → King Charles III: Whose face is on the newest Bank of England banknotes, first used in 2024? → King Charles III
- nursery-rhymes-and-singalongs-4: overlap like q-5254: ¿Qué poema de Rafael Pombo cuenta cómo un niño llamó al pastelero para probar sus pasteles, pero no tenía con qué pagar? → Simón el bobito: In the nursery rhyme, Simple Simon was going to the fair. Who did he meet on the way? → A pieman
- pop-and-rock-10: overlap like q-17954: I was a Covent Garden club. From 1979, Steve Strange ran my Tuesday nights, and my dressed-up regulars were named after me, the “… Kids”. What was I? → The Blitz: Which singer, born George Alan O'Dowd in 1961, became famous in the 1980s for his hats, braids and bold make-up? → Boy George
- art-and-architecture-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: There are four of us, made of bronze, and children love to climb on our backs. Since 1867 we've guarded Nelson's Column in Trafalgar Square. What are we? → Lions
- british-films-2: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: “Zulu”, the film about the defence of Rorke's Drift that made Michael Caine a star, came out in which year? → 1964
- british-films-10: overlap like q-6452: Ron Weasley's favorite Quidditch team wears bright orange robes. Complete its name: the Chudley… → Cannons: Hermione is to Granger as Ron is to…? → Weasley
- writers-and-poets-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In “Alice's Adventures in Wonderland”, the Queen of Hearts' gardeners and soldiers are flat and paint white roses red. What are they? → Playing cards
- childrens-books-and-comics-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: You're shopping in Cheshire, the county the Cheshire Cat is named after. Which food is the county famous for? → Cheese
- childrens-tv-1: hard fail: correct 2, unambiguous 5, no_giveaway 4, no_overlap 5: I’m a lamb from Shaun’s farm. I go to nursery with other baby animals, and my teachers are an owl and a heron. Who am I? → Timmy
- childrens-tv-10: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: At the end of each CBeebies day, a famous guest such as Tom Hardy sits in a cosy chair and reads a book. What is this slot called? → Bedtime Story
- crown-and-state-16: overlap like home-and-public-services-6: I was a Tudor king. In 1516 I appointed a “Master of the Posts”, the start of what became Royal Mail. I also had six wives. Who am I? → Henry VIII: In 1509 I created a royal bodyguard, now called the Gentlemen at Arms. In 1520 I met the French king at the Field of the Cloth of Gold. Who am I? → Henry VIII
- flags-and-emblems-11: overlap like q-5942: Which national rugby team wears this flower on its shirt? → England: England's football badge has three blue lions and ten small flowers, with a star above it for 1966. Which flowers are they? → Tudor roses
- home-and-public-services-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Who drives this red van around British streets every day? → A postal worker
- home-and-public-services-14: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Big containers with round holes stand in many British supermarket car parks. What are they for? → Recycling glass
- languages-of-britain-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which actor's first name comes from the Irish word for “freedom”? → Saoirse Ronan
- money-and-shopping-5: overlap like slang-and-words-0: I led Britain through the Second World War, I made a famous V-for-victory sign, and I'm on the back of the plastic fiver. Who am I? → Winston Churchill: In Britain, what is the usual nickname for a five-pound note? → Fiver
- pop-and-rock-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This 1980s band topped the UK charts with “Do You Really Want to Hurt Me”. Its name nodded to its members' mixed backgrounds. Which band? → Culture Club
- pub-and-playground-games-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This close-up shows part of a course you might find at the seaside. What game is played on it? → Crazy golf
- sayings-and-idioms-7: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Henry and Frank Fowler wrote this guide to good English in 1906. Its title is now a phrase for “correct” English. What is it? → The King's English
- school-and-childhood-3: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: A child in England has just started Key Stage 1. How old are children in this stage? → 5 to 7
- slang-and-words-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which British nickname for a know-it-all names a kind of footwear? → Clever clogs
- slang-and-words-15: overlap like q-11876: In old American gangster films, characters talk about “dough,” “bread” and “clams.” What are all these words slang for? → Money: “Grub” is to food as “wonga” is to… → Money
- soaps-and-dramas-5: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: She's Emmerdale's ice-cold businesswoman, played by Claire King, and she loves her horses. Which grand house is Kim Tate's home? → Home Farm
- sporting-events-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I'm round and hard, and every spring I'm sent bouncing down Cooper's Hill in the Cotswolds while racers tumble after me. Which cheese am I? → Double Gloucester
- sporting-events-14: overlap like q-17224: Se juega cada primavera en la Caja Mágica, Nadal lo ganó cinco veces y en 2012 pintaron sus pistas de azul. ¿Sobre qué superficie se juega el Mutua Madrid Open? → Tierra batida: Wimbledon is to grass as the French Open is to… → Clay
- sporting-events-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Every day of Royal Ascot at 2 pm, the King and Queen travel up the course past the cheering crowds. What do they travel in? → Horse-drawn carriages
- team-gb-and-olympians-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: The Olympic team in red, white and blue is known as Team GB. What do the letters GB stand for? → Great Britain
- transport-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Britain, what is a “bendy bus”? → A long bus with a hinge in the middle
- rugby-and-cricket-1: overlap like q-5943: In 2003, this fly-half won the Rugby World Cup final with a drop goal in the last minute of extra time. Who is he? → Jonny Wilkinson: You're watching Jonny Wilkinson's last-minute drop goal in the 2003 Rugby World Cup final. How many points does that kick add? → 3
- rugby-and-cricket-3: overlap like q-2065: En rugby, llevan los números del 1 al 8, forman el scrum y entre ellos están los pilares y el talonador. ¿Cómo se llama este grupo? → Delanteros: This is a rugby union scrum. Which group of players from each team packs down in it? → The forwards
- sayings-and-idioms-6: overlap like q-13438: Cuando alguien exclama «¡Caramba!», ¿qué está mostrando normalmente? → Sorpresa: When a Brit says “Blimey!”, what are they usually showing? → Surprise
- sitcoms-13: overlap like q-10042: Benidorm es a la Costa Blanca como Marbella es a la… → Costa del Sol: I'm a sunny Costa Blanca resort, and from 2007 ITV filled me with British holidaymakers at the all-inclusive Solana hotel. Which place am I? → Benidorm
- slang-and-words-0: overlap like q-5005: I took over my country's government in 1940, gave rousing speeches on the radio, and raised two fingers in a V for victory. Who am I? → Winston Churchill: I led Britain through the Second World War, I made a famous V-for-victory sign, and I'm on the back of the plastic fiver. Who am I? → Winston Churchill
- slang-and-words-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: If someone calls you a “scaredy-cat”, what are they saying about you? → You get frightened easily
- soaps-and-dramas-7: overlap like q-5587: This is Agatha Christie, the “Queen of Crime”. Her famous detective Hercule Poirot comes from which country? → Belgium: This actor played Hercule Poirot on ITV from 1989 to 2013. Which country does Poirot come from? → Belgium
- sporting-events-15: overlap like q-0430: ¿Quién tiene el récord mundial de los 100 metros planos? → Usain Bolt: At the London 2012 Olympics, who won the men's 100 m race in this stadium? → Usain Bolt
- team-gb-and-olympians-2: overlap like q-1013: Las paredes del 'Cubo de Agua', la piscina olímpica de Pekín, están cubiertas de celdas irregulares. ¿En qué se inspiraron sus arquitectos? → En las burbujas de jabón: Rebecca Adlington won two Olympic swimming golds in this building. In which city is it? → Beijing
- team-gb-and-olympians-16: overlap like q-9668: At the Tokyo Olympics, cameras caught a British gold-medal diver knitting in the stands. He had been Britain's youngest athlete in Beijing, aged 14. Who is he? → Tom Daley: At the Tokyo 2020 Olympics, which British star was famously seen doing this hobby in the stands between events? → Tom Daley
- traditional-music-and-dance-10: duplicate like q-9626: Legend says Jack the Giant Killer beat his first giant, Cormoran, who lived on this island. In which English county is it? → Cornwall: The shanty-singing group Fisherman's Friends, who got their own film in 2019, come from this harbour village. Which county is it in? → Cornwall
- transport-6: overlap like q-6612: Red buses with two floors like this one are a famous sight in which city? → London: I'm red, I have an upstairs and a downstairs, and I carry people all over London. What am I? → A double-decker bus
- writers-and-poets-2: overlap like q-6643: In the novel where “All animals are equal, but some animals are more equal than others”, which of these animals is NOT a character? → A wolf: Which of these animals is NOT a character in George Orwell's “Animal Farm”? → Wilbur
- writers-and-poets-4: overlap like childrens-books-and-comics-9: In Harry Potter, it's what wizards call people with no magic. The Dursleys are this, and so are Hermione's parents. What's the word? → Muggle: In the Harry Potter books, what is the word for people with no magic at all, like Harry's aunt and uncle? → Muggles
- writers-and-poets-5: overlap like q-16100: Heiße Schokolade ist braun und wird mit warmer Milch getrunken. Aus welchen Bohnen macht man das Pulver dafür? → Kakaobohnen: Willy Wonka's factory makes bars like this one. What is chocolate made from? → Cocoa beans
- writers-and-poets-8: overlap like q-3087: In “The Lord of the Rings”, Frodo's journey begins in the Shire. Where must it end, so the One Ring can be destroyed? → Mount Doom: In “The Lord of the Rings”, which hobbit carries the One Ring to Mount Doom? → Frodo
- writers-and-poets-14: overlap like q-1377: ¿En qué siglo se publicó «Orgullo y prejuicio», la novela de Elizabeth Bennet y el señor Darcy? → Siglo XIX: I'm the second of five sisters, and my mother badly wants us all married. A rich, proud man says I'm not pretty enough to dance with. Who am I? → Elizabeth Bennet
