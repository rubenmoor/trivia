# batch-75

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, early-britain, middle-ages, twentieth-century, customs-and-ceremonies, legendary-heroes, traditional-music-and-dance, soaps-and-dramas, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, transport, hills-moors-and-national-parks, birds, tudors-and-stuarts, georgians-and-victorians, parliament-and-prime-ministers, scientists-and-inventors, pioneers-and-heroes, cakes-puddings-and-biscuits, drinks, creatures-ghosts-and-superstitions, pop-and-rock
- Merged: 103 (q-20387…q-20489)
- Approved: 90
- Needs work: 13
- Dropped by the pipeline: 45
- Reviewed by: claude-opus-5-5
- Claude calls: 312, about $38.92 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-73, batch-74; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-73 | batch-74 | batch-75 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 158 | 144 | 148 |
| skipped slots |  | 346 | 360 | 356 |
| dropped |  | 60 | 43 | 45 |
| drop rate | ≤ 20.0 % | 38.0 % ✗ | 29.9 % ✗ | 30.4 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 3 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 10 | 9 | 11 |
| dropped: overlap |  | 46 | 34 | 33 |
| dropped: duplicate |  | 1 | 0 | 1 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 98 | 101 | 103 |
| approved |  | 91 | 94 | 90 |
| needs_work |  | 7 | 7 | 13 |
| needs_work rate | ≤ 20.0 % | 7.1 % ✓ | 6.9 % ✓ | 12.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.0 % ✓ | 4.0 % ✓ | 4.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✗ | 2.0 % ✗ | 2.9 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.1 % ✓ | 5.0 % ✓ | 6.8 % ✓ |
| media: no pick in review 1 |  | 10 | 6 | 17 |
| media: recovered by research |  | 6 | 3 | 11 |
| media: no pick at record |  | 4 | 5 | 7 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 30.4 % ✗ | 25.0 % ✗ | 25.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 14 | 11 | 1 |
| top move | ≤ 25.0 % | 17.3 % ✓ | 16.8 % ✓ | 15.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 84.7 % | 85.1 % | 78.6 % |
| values stimulus |  | 4 | 4 | 4 |
| top clue | ≤ 60.0 % | 45.9 % ✓ | 33.7 % ✓ | 39.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 30.6 % ✓ | 30.7 % ✓ | 34.0 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.4 % ✓ | 22.8 % ✓ | 24.3 % ✓ |
| values lens |  | 11 | 11 | 11 |
| media share | 15.0 %–50.0 % | 15.3 % ✓ | 14.9 % ✗ | 21.4 % ✓ |
| mean fun | ≥ 3.40 | 3.50 ✓ | 3.47 ✓ | 3.63 ✓ |
| cost $ |  | $33.49 | $33.45 | $35.70 |
| $ per approved | ≤ $0.35 | $0.37 ✗ | $0.36 ✗ | $0.40 ✗ |
| calls |  | 237 | 243 | 252 |
| calls per approved |  | 2.60 | 2.59 | 2.80 |
| wall time h |  | 1.20 | 1.21 | 1.23 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 52 (0 %)
- Major among review needs work: 2 of 8 (25 %)
- Problems by kind: giveaway 18 (2 major), fact 2 (0 major), overlap 2 (1 major), media 4 (1 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.22

Major findings on approved questions:

None.

## Needs work

- **q-20395** (cakes-puddings-and-biscuits) This twisty, ladder-shaped bar is a Curly Wurly. What is under its chocolate coating? → Chewy caramel: No candidate is adequate for the essential image. Candidate 1 is the only Curly Wurly, but it is snapped in two, so the broken ends show the golden caramel inside (the answer). It is also shot from the side, so the ladder shape barely shows. Candidates 2–6 are a sculpture, seating, a footbridge, wooden stepping stones and a tree vine, not the chocolate bar. A whole, unwrapped Curly Wurly seen from above is needed, but no new search is allowed. No suitable picture found for this question.
- **q-20399** (cakes-puddings-and-biscuits) At Hogwarts, the gamekeeper offers Harry rock cakes so hard they nearly break his teeth. Who is the gamekeeper? → Hagrid: None of the media candidates shows rock cakes. They show a 1916 florist journal scan with flowers and two photos of a woman standing on rocks by the sea. A new search isn't allowed, so the image slot needs a real photo of rock cakes or rock buns. The question text itself is fine. No suitable picture found for this question.
- **q-20407** (drinks) It was invented in 1927 to help poorly people get their energy back, it came wrapped in yellow cellophane, and now there's a “Sport” version. Which drink is it? → Lucozade: The description (“A sick day at home… something fizzy by the bed”) states Lucozade's defining trait, the drink given to poorly people. With only the four options shown, it already points to Lucozade over Irn-Bru, Vimto and Tango. Rewrite it so it plays on British fizzy drinks or Newcastle in general, without mentioning illness or recovery.
- **q-20419** (money-and-shopping) How many of these notes do you need to make £20? → 4: No candidate shows the current turquoise polymer £5 note with a clear "5" that the essential slot needs. Candidates 1 and 3 are Victorian and 1930s white fivers whose value is written only in old copperplate script, which kids can't read. The other candidates show a book cover, harbour scans and an Australian note. A new search for a polymer Bank of England £5 note (for example "Bank of England £5 polymer") is needed. No suitable picture found for this question.
- **q-20420** (money-and-shopping) You're checking your change for special 50p coins. Which of these characters has never been on a British 50p? → SpongeBob SquarePants: Hint 1 (“The Royal Mint loves characters from British children's books.”) gives the answer away: SpongeBob is the only option that isn't a character from a British children's book, so the first hint alone solves it. Replace hint 1 with a vague hint, for example about 50p coins being collected or about the Royal Mint making special designs, and keep the British-books clue for hint 2 or 3.
- **q-20423** (parliament-and-prime-ministers) In which part of Parliament would you sit on these red leather benches? → The House of Lords: The fun fact says the monarch's golden throne stands in the Lords chamber, which is exactly the answer to the approved q-18808, so seeing this question gives that one away. The fun fact should get a different fact, for example about the red colour or the benches. The description's "if you can get an invitation" also hints that members are appointed, not elected. That is the trait that separates the answer from the House of Commons, the only serious distractor, so it should play on the theme without that hint.
- **q-20450** (drinks) The famous pub in EastEnders is named after a real queen. Which one? → Queen Victoria: This overlaps too much with approved q-18086 ("Which pub did EastEnders' Kat Slater run with her husband Alfie Moon?" → “The Queen Vic”). Whichever of the two is seen first gives away the other, since the pub's name contains the queen's name. Also, all the image candidates show grand Regency terraces in Regent's Park (York Terrace East), not an East End street. No suitable picture found for this question.
- **q-20454** (football) In football, what is a derby? → A match between two local rivals: No candidate fits: all six pictures are US college American football stadiums (gridiron lines, marching bands, Notre Dame, Neyland, Hawaii) or a NASA mascot event, which is the wrong sport for a British football question. A new search can't be run, so the media slot needs a fresh query such as "Premier League crowd" or "football terrace fans". A smaller point: hint 1's same-city examples (Liverpool v Everton, Celtic v Rangers) nearly give the answer away; consider a vaguer first hint. No suitable picture found for this question.
- **q-20459** (parliament-and-prime-ministers) This cat lives at 10 Downing Street and has an official job there. Which animals is he meant to catch? → Mice: This overlaps with approved q-9658 in the same subcategory. That question is about Larry at 10 Downing Street and says outright “My title is Chief Mouser”, which gives away this question's answer (mice). Seeing either question also gives away most of the other.
- **q-20474** (twentieth-century) In 2017, Britain's round pound coin was replaced by a new one with 12 sides and two colours. What was the main reason? → To stop fake coins: None of the candidates shows a British round pound coin, which the question names. They show a Malaysian 20 sen next to an egg, a corroded jetton, a triangular weight, 1830s gold £5 pieces and a 1937 Palestine coin. I can't search again. Also, hint 2 ("one of the most secure coins in the world") nearly gives the answer away; it should be a vaguer hint, for example about how the coin was made or its design. No suitable picture found for this question.
- **q-20479** (sitcoms) Tim works at an office in Slough, Gareth sits opposite him, and one day Tim sets Gareth's stapler in jelly. Why can Gareth spot it at once? → Jelly is see-through: Fact check: uncertain. The prank is real (UK Office: Tim sets Gareth's stapler in jelly; US pilot copied it). But the reasoning is weak: Gareth would notice a jelly-encased stapler anyway, and 'see-through' is only a loose explanation. The 'history' lens also doesn't fit. I did not verify this by search.
- **q-20485** (twentieth-century) In old British homes, Friday was often “bath night”: the whole family took turns in one tin bath in front of the fire. When was that common? → About 100 years ago: None of the candidates shows a tin bath, a bath by the fire or an old British home. They are a Devon map, metal-detector finds (spoons, a scabbard chape, a Roman object) and a seascape, and a new search isn't allowed. The slot needs a new search for something like “zinc tin bath” or “Victorian tin bath”. No suitable picture found for this question.
- **q-20489** (twentieth-century) Every year the royal family spends several weeks at Balmoral Castle in Scotland. When do they usually go? → In the summer holidays: Hint 2 (“The days are long and the heather is purple”) says summer outright and rules out all three wrong options (Christmas, Easter, New Year), so it gives the answer away before hint 3. Hint 1's picnicking also leans hard towards summer; hint 2 should point to something vaguer, such as Highland activities or who joins the family, without naming the season.

## Question axes

- move: analogy 2, cause_effect 4, count 4, estimate 3, identify 11, made_of 8, name_concept 11, odd_one_out 5, origin 9, purpose 11, record 2, sequence 5, when 8, who 4, word_meaning 16
- stimulus: detail 2, none 81, photo 19, sound 1
- clue: completion 5, direct 41, riddle 7, scenario 15, three_facts 35
- answer_kind: group 11, number 8, person 9, place 9, thing 35, time 10, word 21
- lens: body_senses 1, educational_media 15, everyday 25, history 18, language 15, nature 3, pop_culture 14, popular_science 2, school 6, science_news 3, university 1

## Dropped by the pipeline

- accents-and-dialects-10: overlap like q-19852: It was designed by Isambard Kingdom Brunel, it hangs high over the Avon Gorge and it opened in 1864. What is it? → Clifton Suspension Bridge: Locals greet a friend as “my babber”, often add an “L” to words like “area”, and Brunel designed its famous suspension bridge. Which city? → Bristol
- accents-and-dialects-16: overlap like q-19455: In “My Fair Lady”, Eliza Doolittle sells flowers in Covent Garden until Professor Higgins teaches her to speak “properly”. Which accent does she start with? → Cockney: I'm a phonetics professor, I can place a person's home street by their accent, and I bet I can make a Cockney flower girl talk like a duchess. Who am I? → Henry Higgins
- cakes-puddings-and-biscuits-4: overlap like q-18994: McVitie's launched Hobnobs in 1985, and they're often half-coated in milk chocolate. Which grain makes them so rough and crunchy? → Oats: This brand started in Edinburgh and makes Digestives, Hobnobs and Jaffa Cakes. Which brand is it? → McVitie's
- cakes-puddings-and-biscuits-5: overlap like q-20186: On a hot day, a tune like “Greensleeves” plays in the street and children run out with coins. What has just arrived? → An ice cream van: It's a sunny day and you fancy a Mr Whippy ice cream. Where do you usually buy one? → From an ice-cream van
- creatures-ghosts-and-superstitions-3: overlap like q-18843: On which day do most British families sit down to a big roast turkey? → Christmas Day: You find a silver coin hidden in your slice of dark, fruity pudding that was set alight at the table. Which day is it most likely to be? → Christmas Day
- customs-and-ceremonies-1: duplicate like q-18551: Sir Chris Hoy, pictured here, won six Olympic gold medals in track cycling. Which part of the UK is he from? → Scotland: Cloth with this criss-cross pattern is most closely linked with which part of the UK? → Scotland
- customs-and-ceremonies-4: overlap like q-20089: At a yearly contest in a Cheshire village, digging is banned, so people wiggle garden forks in the lawn and even play music to it. Which creatures come up? → Earthworms: At a contest in Cheshire, people wiggle garden forks in the grass to charm these up from the soil. What are they? → Earthworms
- customs-and-ceremonies-7: overlap like q-19441: It's golf's oldest major, first played in 1860, and the winner lifts the Claret Jug. Which course has hosted The Open more times than any other? → St Andrews: The winner of the Open, Britain's oldest major championship, lifts this silver jug. Which sport is it? → Golf
- customs-and-ceremonies-8: overlap like q-18618: I wear white shirts, my fans sing “Swing Low, Sweet Chariot”, and my home ground is Twickenham. Which team am I? → England: It's an old African-American spiritual. England fans have sung it since 1988, and it booms round Twickenham. Fans of which sport? → Rugby fans
- customs-and-ceremonies-11: overlap like q-18989: In Britain, some people salute a lone magpie to avoid bad luck. They then say “Good morning, …” to whom? → Mr Magpie: You spot a single magpie, so you salute it and say “Good morning, Mr Magpie”. Why do Britons do this? → To avoid bad luck
- drinks-2: overlap like q-9917: En España se puso de moda servirlo en copa de balón con mucho hielo; lleva tónica y un licor aromatizado con enebro. ¿Qué licor es? → Ginebra: In a British pub, someone orders a “G and T”. It stands for gin and… what? → Tonic
- early-britain-5: overlap like q-18224: At Vindolanda, a Roman fort near Hadrian's Wall, thin wooden letters survived for nearly 2,000 years, including a birthday invitation. Why? → They lay in wet ground with no air: At Vindolanda, a Roman fort by Hadrian's Wall, people wrote in ink on thin slices of wood. What did they mostly use them for? → Letters and notes
- football-4: overlap like q-9666: In 2022 at Wembley, they became the first England football team since 1966 to win a major tournament, and in 2025 they won the Euros again. Who are they? → The Lionesses: We're England's women's football team. We won the Euros in 2022, then kept our title at Euro 2025 in Switzerland. What is our nickname? → The Lionesses
- georgians-and-victorians-12: overlap like q-19463: Four huge bronze animals guard the bottom of Nelson's Column in Trafalgar Square. Which animal are they? → Lions: Admiral Nelson stands on top of this column in London. How many bronze lions guard its base? → 4
- languages-of-britain-2: overlap like q-1440: ¿Qué pueblo navegaba en drakares, barcos largos con una cabeza de dragón en la proa? → Los vikingos: People who sailed in ships like this one gave English the everyday word “they”. Who were they? → The Vikings
- legendary-heroes-8: overlap like q-5886: In Disney's 1973 film “Robin Hood”, the hero is a fox. Which animal plays the greedy Prince John? → A lion: In Disney's cartoon “Robin Hood”, greedy Prince John wears a crown too big for him and sucks his thumb. Which animal is he? → A lion
- middle-ages-2: overlap like q-19273: The Anglo-Saxons brought runes to England, in an alphabet called the futhorc. The letters are almost all straight lines. Why? → They were easy to carve into wood or stone: Vikings in Britain carved runes into stone, wood and bone. They are made of straight lines that are easy to cut, and they spell out names. What were runes? → Letters for writing
- money-and-shopping-5: overlap like q-18744: This 50p coin shows a famous rabbit. Who wrote the books he comes from? → Beatrix Potter: Which author created the rabbit on this 50p coin? → Beatrix Potter
- parliament-and-prime-ministers-6: overlap like q-19310: I'm one of the most powerful ministers in the government. I live at Number 11 Downing Street, and on Budget Day I hold up a red box for the cameras. Who am I? → The Chancellor of the Exchequer: The Prime Minister's office is at number 10 Downing Street. Which number is the Chancellor of the Exchequer's official home? → 11
- parliament-and-prime-ministers-12: overlap like q-18688: Britain's NHS began in 1948, it's paid for out of taxes, and it's free when you use it. What does it give people? → Free doctors and hospitals: An Act of Parliament created me in 1946. I opened in 1948, and I let people see a doctor without paying on the spot. What am I? → The NHS
- parliament-and-prime-ministers-16: overlap like q-20144: Scotland's Parliament meets in a modern building, opened in 2004 next to a royal palace. Which city is it in? → Edinburgh: Scotland's Parliament building, shown here, is nicknamed “Holyrood” after the area it stands in. Which city is it in? → Edinburgh
- pioneers-and-heroes-1: overlap like q-18349: In 1823, a Glasgow chemist patented a waterproof cloth made by putting rubber between two layers of fabric. Who was he? → Charles Macintosh: Riddle: “I'm named after a Scottish chemist who made cloth waterproof with rubber. People often shorten my name to “mac”. What am I?” → A raincoat
- accents-and-dialects-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Complete the meaning: you fix a fence in Cornwall and a local says “Proper job!”. They mean… → Well done!
- birds-16: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: An old legend says this bird got its red colour fanning a fire to keep baby Jesus warm. What's its old name: Robin…? → Redbreast
- cakes-puddings-and-biscuits-1: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Love Hearts are small, fizzy sweets that come in a paper roll. Besides a heart, what is stamped on each one? → A short message
- cakes-puddings-and-biscuits-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Wine gums have words like “Port” and “Sherry” stamped on them. How much wine is in them? → None at all
- drinks-8: overlap like q-14572: Estas piezas negras y brillantes se hacen en San Bartolo Coyotepec, Oaxaca. ¿De qué material están hechas? → De barro: Look at the photo: this “Brown Betty” teapot has been made in England for about 300 years. What is it made of? → Clay
- georgians-and-victorians-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: In Alice in Wonderland, the Mad Hatter has a card in his hat that says “10/6”. What does it tell you? → The hat's price
- georgians-and-victorians-11: overlap like q-18985: L. S. Lowry filled his paintings with “matchstick” people walking to the mills of Salford. What were those mills for? → Making cotton thread and cloth: This is Quarry Bank, a big old mill near Manchester. What did its machines make? → Thread and cloth
- hills-moors-and-national-parks-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: What is Pen y Fan, in the Brecon Beacons in Wales? → A mountain
- hills-moors-and-national-parks-2: overlap like hills-moors-and-national-parks-1: What is Pen y Fan, in the Brecon Beacons in Wales? → A mountain: Scottish walkers try to “bag” all 282 Munros. What is a Munro? → A Scottish mountain
- money-and-shopping-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: John Lewis, Selfridges and Harrods are all famous British examples of which kind of shop? → A department store
- money-and-shopping-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Which Bank of England note shows the codebreaker Alan Turing? → The £50 note
- pioneers-and-heroes-3: overlap like q-18101: Captain Webb swam the English Channel in 1875 using a stroke where your legs kick like a frog's. Which stroke? → Breaststroke: In 1875, Captain Matthew Webb smeared himself in porpoise oil and made a famous first swim. What did he swim across? → The English Channel
- traditional-music-and-dance-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Llanelli rugby fans sing the Welsh song “Sosban Fach”. What is a “sosban”? → A saucepan
- transport-5: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: At many British stations, these gates open when you feed in your ticket or tap a card, then snap shut behind you. What are they? → Ticket barriers
- tudors-and-stuarts-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Which English writer wrote 154 sonnets, short love poems of 14 lines each? → William Shakespeare
- sayings-and-idioms-11: overlap like q-18217: Look at this close-up of a tall, domed helmet. Which British workers are famous for wearing it? → Police officers: In Britain, a “bobby” walks the streets, may wear a tall domed helmet and will help you if you're lost. Who is a bobby? → A police officer
- sayings-and-idioms-16: overlap like q-19329: In Cockney rhyming slang, “apples and pears” means stairs. What does “pork pies” mean? → Lies: I'm a cold, meaty snack in a crunchy crust, loved at picnics. In Cockney rhyming slang, I stand for “lies”. What am I? → A pork pie
- sitcoms-1: overlap like q-18918: I sell dodgy goods in Peckham, drive a yellow three-wheeled van, and call my brother Rodney a “plonker”. Who am I? → Del Boy: My van says “New York – Paris – Peckham”, I call my little brother a plonker, and I run Trotters Independent Traders. Who am I? → Del Boy
- traditional-music-and-dance-0: overlap like q-18308: Every January, people in Somerset sing to the trees in places like this to wake them up for a good cider crop. What is this kind of place called? → An orchard: In January, wassailers in Somerset sing and bang pots to wake up trees like this one. Where do these trees grow? → An orchard
- transport-16: overlap like q-20293: This is part of a railway station sign with a very, very long village name. Which language is the name in? → Welsh: Britain's longest station name, Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch, has 58 letters. Which language is it in? → Welsh
- tudors-and-stuarts-0: overlap like q-17880: The guards who wear this red-and-gold uniform have a famous nickname. What is it? → Beefeaters: I live with my family inside a famous castle by the River Thames, wear a dark blue and red uniform, and help look after the ravens. Who am I? → A Beefeater
- twentieth-century-10: overlap like q-0163: En 1928, Alexander Fleming vio un moho creciendo en un plato de laboratorio. ¿Qué medicina descubrió? → La penicilina: In 1928, Alexander Fleming came back from holiday to an untidy lab. Something fuzzy had grown on a dish and killed the germs around it. What was it? → Mould
- twentieth-century-13: overlap like q-18122: British road crossings are named after animals. What is this one called? → Zebra crossing: Tourists in London copy a famous Beatles album photo by walking across Abbey Road on black-and-white stripes. What is that kind of crossing called? → Zebra crossing
