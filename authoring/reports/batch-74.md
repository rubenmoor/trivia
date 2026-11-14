# batch-74

Made by `qgen batch` on 2026-11-14 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: uk
- Language: English
- Subcategories (28): cities-and-towns, early-britain, middle-ages, twentieth-century, customs-and-ceremonies, legendary-heroes, traditional-music-and-dance, soaps-and-dramas, sitcoms, comedians-and-panel-shows, football, rugby-and-cricket, team-gb-and-olympians, sayings-and-idioms, accents-and-dialects, languages-of-britain, money-and-shopping, transport, hills-moors-and-national-parks, landmarks-and-castles, birds, plants-and-gardens, tudors-and-stuarts, georgians-and-victorians, parliament-and-prime-ministers, scientists-and-inventors, pioneers-and-heroes, cakes-puddings-and-biscuits
- Merged: 101 (q-20286…q-20386)
- Approved: 94
- Needs work: 7
- Dropped by the pipeline: 43
- Reviewed by: claude-opus-5-5
- Claude calls: 303, about $36.59 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-72, batch-73; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-72 | batch-73 | batch-74 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| drafts |  | 163 | 158 | 144 |
| skipped slots |  | 341 | 346 | 360 |
| dropped |  | 66 | 60 | 43 |
| drop rate | ≤ 20.0 % | 40.5 % ✗ | 38.0 % ✗ | 29.9 % ✗ |
| dropped: hard fail correct |  | 2 | 0 | 0 |
| dropped: hard fail unambiguous |  | 1 | 3 | 0 |
| dropped: hard fail no_giveaway |  | 16 | 10 | 9 |
| dropped: overlap |  | 46 | 46 | 34 |
| dropped: duplicate |  | 1 | 1 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 97 | 98 | 101 |
| approved |  | 90 | 91 | 94 |
| needs_work |  | 7 | 7 | 7 |
| needs_work rate | ≤ 20.0 % | 7.2 % ✓ | 7.1 % ✓ | 6.9 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.1 % ✓ | 2.0 % ✓ | 4.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✗ | 1.0 % ✗ | 2.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.1 % ✓ | 4.1 % ✓ | 5.0 % ✓ |
| media: no pick in review 1 |  | 16 | 10 | 6 |
| media: recovered by research |  | 13 | 6 | 3 |
| media: no pick at record |  | 3 | 4 | 5 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 29.4 % ✗ | 30.4 % ✗ | 25.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 0 | 14 | 11 |
| top move | ≤ 25.0 % | 15.5 % ✓ | 17.3 % ✓ | 16.8 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 77.3 % | 84.7 % | 85.1 % |
| values stimulus |  | 3 | 4 | 4 |
| top clue | ≤ 60.0 % | 43.3 % ✓ | 45.9 % ✓ | 33.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 34.0 % ✓ | 30.6 % ✓ | 30.7 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.6 % ✓ | 20.4 % ✓ | 22.8 % ✓ |
| values lens |  | 10 | 11 | 11 |
| media share | 15.0 %–50.0 % | 22.7 % ✓ | 15.3 % ✓ | 14.9 % ✗ |
| mean fun | ≥ 3.40 | 3.44 ✓ | 3.50 ✓ | 3.47 ✓ |
| cost $ |  | $33.82 | $33.49 | $33.45 |
| $ per approved | ≤ $0.35 | $0.38 ✗ | $0.37 ✗ | $0.36 ✗ |
| calls |  | 246 | 237 | 243 |
| calls per approved |  | 2.73 | 2.60 | 2.59 |
| wall time h |  | 1.10 | 1.20 | 1.21 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 1 of 4 (25 %)
- Problems by kind: giveaway 10 (0 major), fact 3 (0 major), ambiguity 1 (1 major), overlap 1 (0 major), media 3 (1 major), difficulty 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.14

Major findings on approved questions:

None.

## Needs work

- **q-20290** (cakes-puddings-and-biscuits) Look at this close-up. Which plain British biscuit, a favourite for dunking in a cuppa, is it? → Rich Tea: No candidate works for the essential close-up. #1 is a clear Rich Tea, but the words "RICH TEA BISCUITS" are pressed into its surface, which gives the answer away. #2 is from a file titled as digestives (one of the wrong options), and #3–#6 show generic tea-time biscuits from South Asia, not a Rich Tea. Another search isn't possible. A close-up of an unbranded Rich Tea (or one where the stamped text is cropped out or can't be read) would fix this. No suitable picture found for this question.
- **q-20298** (customs-and-ceremonies) In Britain, on which date do families most famously gather round a bonfire and wave sparklers? → 5 November: This repeats approved question q-9795, which already asks for the date of the British bonfire night (the guy burnt on a bonfire → 5 November). Seeing one question gives away the other, and q-18775 asks for the same thing as a month. It can't be fixed without becoming a different question.
- **q-20315** (landmarks-and-castles) Deep inside Wookey Hole Caves in Somerset, the air stays cool and damp all year. Which food is stored there for months to ripen? → Cheese: Hint 2 (“Mice in cartoons love it”) gives the answer away before hint 3. The description (“smells … like a sandwich”) rules out ice cream and chocolate, so only cheese and bread are left. None of the media candidates shows Wookey Hole: they are a cave in the Bahamas (1, 2), Ash Hole Cavern (3) and a portrait shot of a person in Iganteva Cave (4). A new search isn't allowed in this run. No suitable picture found for this question.
- **q-20319** (money-and-shopping) You order something online, the shop gets it ready, and you pick it up yourself in store. What do Britons call this? → Click and collect: The text is fine, but none of the image candidates fits a modern click-and-collect topic. All six are old prints or drawings: a 1913 florist shopfront, an 18th-century satire, a dark table of flowers, a 1940 chemist-shop watercolour and two wallpaper trade cards. No new search is allowed, so the slot needs a manual image, such as a modern "click and collect" sign-free parcel locker or a store collection point photo with no text naming the service. No suitable picture found for this question.
- **q-20324** (parliament-and-prime-ministers) An MP resigns halfway through a Parliament. What normally happens in their constituency? → A by-election is held: The ballot box image gives the answer away: "A by-election is held" is the only option that involves voting. Hint 1 ("The local voters get their say") and hint 2 ("goes to the polls") also rule out all three wrong answers on their own. Use a neutral illustrative image instead, such as the empty Commons green benches or the Palace of Westminster. Rewrite hints 1 and 2 so they stay vague, for example about how rarely this happens or about the Chiltern Hundreds custom. No suitable picture found for this question.
- **q-20352** (sayings-and-idioms) In old slang, something excellent is called “the cat's…” what? → Pyjamas: Hint 2 (“They usually come as a top and bottoms”) gives the answer away: only pyjamas fit it among the four options, since slippers, a dressing gown and a nightcap are all single items. Replace hint 2 with a vaguer clue, for example one about the saying's 1920s American origins. Hint 3 is also very close, because its phonetic spelling is really the answer itself.
- **q-20377** (traditional-music-and-dance) Which kind of dancers often wear a curly wig full of bouncy ringlets like this one? → Irish dancers: This repeats approved q-18946 ("These dancers keep their arms straight by their sides… often wear curly wigs. Which country does this dancing come from?" → Ireland). Both questions use the same clues (curly wigs, stiff arms) to get the same answer, so seeing one gives the other away. None of the candidates shows a ringlet wig either. No suitable picture found for this question.

## Question axes

- move: analogy 1, cause_effect 4, count 4, estimate 2, identify 14, made_of 2, name_concept 17, odd_one_out 3, origin 10, purpose 8, record 1, sequence 1, when 10, who 9, word_meaning 15
- stimulus: detail 7, none 86, photo 7, sound 1
- clue: completion 4, direct 34, riddle 17, scenario 12, three_facts 34
- answer_kind: group 14, number 6, person 11, place 9, thing 31, time 10, word 20
- lens: body_senses 6, educational_media 7, everyday 9, history 23, language 20, nature 8, pop_culture 15, popular_science 1, school 9, science_news 1, university 2

## Dropped by the pipeline

- accents-and-dialects-12: overlap like q-19733: In which country do people say “Bore da” to mean “good morning”? → Wales: People say it as they clink glasses, it means “good health”, and it sounds like “YEH-chid dah”. Where are you most likely to hear “Iechyd da”? → Wales
- birds-8: overlap like q-13244: Montas el belén y pones la mula y el buey junto al pesebre. Según la tradición, ¿a quién dan calor con su aliento? → Al Niño Jesús: You're looking at a robin's orange-red breast. An old British legend says it got scorched fanning a fire in a stable to keep someone warm. Who? → Baby Jesus
- cakes-puddings-and-biscuits-10: overlap like q-13761: Jelly beans have filled American Easter baskets for nearly 100 years. What are they mostly made of? → Sugar: Hundreds and thousands are tiny, rainbow-coloured, and Brits shake them over trifles and birthday cakes. What are they mostly made of? → Sugar
- customs-and-ceremonies-1: overlap like q-18777: Scottish men wear a kilt to weddings, on Burns Night and at Highland games, often with a sporran. What is a kilt? → A knee-length tartan skirt: This criss-cross cloth is used to make Scottish kilts. What is the pattern called? → Tartan
- customs-and-ceremonies-15: overlap like q-3223: It's an honor from the British monarch, the ceremony uses a sword, and men who get it are called “Sir”. What is a woman called who gets it herself? → Dame: The man kneeling here is being knighted with a tap of a sword on each shoulder. What word goes before his name from now on? → Sir
- georgians-and-victorians-2: overlap like q-1226: Llevo un sombrero enorme, tomo té con una liebre y celebro el 'feliz no-cumpleaños' con Alicia. ¿Quién soy? → El Sombrerero Loco: In “Alice's Adventures in Wonderland”, time has stopped for the Mad Hatter. What time of day is it for him forever? → Tea-time
- hills-moors-and-national-parks-7: overlap like q-20108: You're walking along Offa's Dyke, the great border King Offa of Mercia built between England and Wales. What is it made of? → An earth bank and a ditch: Look at the photo: about 1,200 years ago, King Offa had this long earth bank and ditch built. What was it mainly for? → Marking the edge of his kingdom
- languages-of-britain-14: overlap like q-17861: On CBeebies, Mr Tumble talks with his voice and also with what? → Hand signs: On CBeebies' “Something Special”, which character uses Makaton signs to talk to children? → Mr Tumble
- legendary-heroes-8: overlap like q-5886: In Disney's 1973 film “Robin Hood”, the hero is a fox. Which animal plays the greedy Prince John? → A lion: In Disney's cartoon “Robin Hood”, greedy Prince John sucks his thumb and wears a crown that's too big for him. What animal is he? → A lion
- money-and-shopping-0: overlap like q-18883: In Britain, what is a “fiver”? → A £5 note: Britons call this note a “fiver”. How many of them do you need to make £20? → 4
- money-and-shopping-4: overlap like q-18248: You hand over a Tesco Clubcard at the till. It collects points and unlocks special lower prices. What kind of card is it? → A loyalty card: Which British supermarket has a red and blue logo, the Clubcard and the slogan “Every little helps”? → Tesco
- money-and-shopping-13: overlap like q-18744: This 50p coin shows a famous rabbit. Who wrote the books he comes from? → Beatrix Potter: This 50p coin shows a famous rabbit in a blue jacket. Which author created him? → Beatrix Potter
- parliament-and-prime-ministers-2: overlap like q-20144: Scotland's Parliament meets in a modern building, opened in 2004 next to a royal palace. Which city is it in? → Edinburgh: This is Scotland's parliament building, nicknamed Holyrood. In which city is it? → Edinburgh
- parliament-and-prime-ministers-8: overlap like q-1857: Las fiestas en la oficina del primer ministro británico Boris Johnson se volvieron un escándalo. ¿En qué época fueron? → La pandemia de covid-19: Police looked into gatherings held at Downing Street during the COVID lockdowns. What first did Boris Johnson become in 2022? → First serving PM fined for breaking the law
- parliament-and-prime-ministers-12: overlap like q-9658: I have four paws and live at 10 Downing Street. Since 2011 I've seen many prime ministers come and go. My title is Chief Mouser. Who am I? → Larry: What is the job of the “Chief Mouser to the Cabinet Office” at Downing Street? → Catching mice
- parliament-and-prime-ministers-17: overlap like q-19310: I'm one of the most powerful ministers in the government. I live at Number 11 Downing Street, and on Budget Day I hold up a red box for the cameras. Who am I? → The Chancellor of the Exchequer: Tony Blair's family lived in the flat above this house, next door to Number 10, because it was bigger. What is its address? → 11 Downing Street
- plants-and-gardens-12: overlap like q-9711: At English May Day fairs, children dance round a tall pole, each holding something that weaves a pattern down it. What do they hold? → Ribbons: On May Day, children in English villages dance round a tall maypole. What does each dancer hold? → A ribbon
- cakes-puddings-and-biscuits-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Raspberry ripple is a classic British ice cream. It's vanilla, it's sold at ice-cream vans, and it has a “ripple”. What is the ripple? → Raspberry sauce swirls
- cakes-puddings-and-biscuits-8: overlap like q-9787: Cadbury's famous Dairy Milk slogan promises how many glasses of full cream milk in every half pound of chocolate? → A glass and a half: Cadbury Dairy Milk famously promises how much full cream milk in its chocolate? → A glass and a half
- cakes-puddings-and-biscuits-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ginger nuts are hard, spicy British biscuits, made for dunking in tea. What kind of nut is inside them? → None at all
- cities-and-towns-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: I began in 1884 as a market stall in Leeds where everything cost a penny. Today I'm a big British shop famous for my food. What am I? → Marks & Spencer
- comedians-and-panel-shows-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In a Harry Enfield sketch, sweet little Kevin changes overnight on his birthday. What does he become? → A teenager
- georgians-and-victorians-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Victorian gentlemen wore this eyeglass. How many lenses does it have? → 1
- hills-moors-and-national-parks-3: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: In the Lake District, fell runners race over rough, muddy ground, often with no path at all. What is a “fell”? → A hill
- landmarks-and-castles-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This is the Senedd, the Welsh Parliament in Cardiff Bay. What are most of its outside walls made of? → Glass
- plants-and-gardens-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: At a British village produce show, which of these would NOT usually win a prize? → Fastest bicycle
- sayings-and-idioms-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In 1940, Winston Churchill gave a famous speech promising Britain would fight on. Its best-known line is “We shall fight on the…” what? → Beaches
- team-gb-and-olympians-6: overlap like q-19624: This boxer won super-heavyweight gold at London 2012 and later became world heavyweight champion. Who is he? → Anthony Joshua: I'm the Olympic boxing class with no top weight limit. Audley Harrison won gold in me for Britain in 2000. What am I? → Super-heavyweight
- twentieth-century-17: overlap like sitcoms-12: René's café in the sitcom 'Allo 'Allo! is full of soldiers. During which war is the show set? → The Second World War: You're watching “Dad's Army”, the comedy about older men in the Home Guard defending a seaside town. Which war is it set in? → The Second World War
- sayings-and-idioms-5: overlap like q-19329: In Cockney rhyming slang, “apples and pears” means stairs. What does “pork pies” mean? → Lies: It's short for “pork pies”, it comes from Cockney rhyming slang, and you get told off for telling them. What are porkies? → Lies
- sayings-and-idioms-11: overlap like q-18217: Look at this close-up of a tall, domed helmet. Which British workers are famous for wearing it? → Police officers: He walks the streets, wears a tall rounded helmet and keeps people safe. Brits nickname him a “bobby”. What is his job? → Police officer
- scientists-and-inventors-5: overlap like q-4101: In 1960 in Tanzania, these apes were seen stripping twigs to fish for termites: the first wild animals seen making tools. Which apes? → Chimpanzees: In an African forest, Jane Goodall from London saw wild animals use sticks to fish termites out of their nests. Which animal? → Chimpanzees
- sitcoms-6: overlap like q-19664: In “Gavin & Stacey”, Nessa often asks, “What's occurring?” What does she mean? → What's going on?: In Gavin & Stacey, which character greets people with “What's occurring?” → Nessa
- sitcoms-8: overlap like q-20068: Basil Fawlty runs a hotel in Fawlty Towers. What else is “basil”, apart from his first name? → A cooking herb: In Fawlty Towers, when Sybil catches her husband up to no good, which word does she shriek? → “Basil!”
- soaps-and-dramas-13: overlap like q-17909: We're a Geordie duo who met on Byker Grove, and each winter we send celebrities into the Australian jungle. Who are we? → Ant and Dec: I'm a Newcastle youth club on CBBC, first opened in 1989. PJ and Duncan hung around here before the two boys who played them got very famous. What am I? → Byker Grove
- team-gb-and-olympians-5: overlap like q-13803: ABC's Dancing with the Stars, which began in 2005, is based on a British TV show. What is that show called? → Strictly Come Dancing: After London 2012, track cycling champion Victoria Pendleton joined the TV show “Strictly Come …”. How does the title end? → Dancing
- tudors-and-stuarts-17: overlap like q-17880: The guards who wear this red-and-gold uniform have a famous nickname. What is it? → Beefeaters: Look at this guard at the Tower of London. What is the famous nickname for guards like him? → Beefeaters
- twentieth-century-1: overlap like q-5494: In 1953, two climbers became the first to stand on top of this mountain and wave flags there. Who were they? → Edmund Hillary and Tenzing Norgay: Edmund Hillary and Tenzing Norgay were the first to reach the top of Everest. The news reached London on the Queen's coronation day. Which year? → 1953
- twentieth-century-4: overlap like q-18314: It's the royal family's summer home, Queen Victoria loved it, and it stands in the UK's largest national park. Which UK country is Balmoral Castle in? → Scotland: You're on a road trip around the King's homes. Which of these is NOT in England? → Balmoral Castle
- twentieth-century-8: overlap like q-19724: In 1997, before any member had left, how many Spice Girls were there? → 5: When Geri Halliwell, known as Ginger Spice, left the Spice Girls in 1998, how many members were left? → 4
- twentieth-century-10: overlap like q-5661: In 1969, a famous band walked across this London street crossing for an album cover. Which band was it? → The Beatles: You're on a zebra crossing in north London where tourists copy a famous Beatles album cover. What's the road called? → Abbey Road
- twentieth-century-15: overlap like q-1171: ¿Quién creó la World Wide Web y el HTML, el lenguaje con el que se escriben las páginas web? → Tim Berners-Lee: In 1989, while working at CERN in Switzerland, which British scientist invented the World Wide Web? → Tim Berners-Lee
- twentieth-century-16: overlap like q-0163: En 1928, Alexander Fleming vio un moho creciendo en un plato de laboratorio. ¿Qué medicina descubrió? → La penicilina: In 1928, Scottish scientist Alexander Fleming saw mould killing germs on a dish he had left out in his London lab. What is the medicine from that mould used for? → Fighting infections caused by bacteria
