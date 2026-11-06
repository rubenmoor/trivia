# batch-40

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): winter-holidays, american-literature, fairs-and-festivals, nineteenth-century, place-names, household-brands, restaurant-chains, school-life, more-sports, family-and-school-traditions, baseball, wildlife, american-football, weather-and-seasons, cities-and-towns, colonies-and-founding, state-symbols, home-cooking, native-nations, regional-dishes, rivers-lakes-and-mountains, candy-and-snacks, college-sports, traditional-songs, roads-and-landmarks
- Merged: 228 (q-12725…q-12952)
- Approved: 214
- Needs work: 14
- Dropped by the pipeline: 82
- Reviewed by: claude-opus-5-5
- Claude calls: 530, about $67.32 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-38, batch-39; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-38 | batch-39 | batch-40 |
|---|---|---:|---:|---:|
| source locale |  | es-ES | es | en |
| drafts |  | 304 | 305 | 310 |
| skipped slots |  | 182 | 217 | 140 |
| dropped |  | 60 | 73 | 82 |
| drop rate | ≤ 20.0 % | 19.7 % ✓ | 23.9 % ✗ | 26.5 % ✗ |
| dropped: hard fail correct |  | 3 | 3 | 2 |
| dropped: hard fail unambiguous |  | 0 | 2 | 1 |
| dropped: hard fail no_giveaway |  | 22 | 19 | 26 |
| dropped: overlap |  | 31 | 48 | 53 |
| dropped: duplicate |  | 1 | 1 | 1 |
| dropped: fact-check wrong |  | 3 | 2 | 1 |
| merged |  | 244 | 232 | 228 |
| approved |  | 230 | 212 | 214 |
| needs_work |  | 14 | 20 | 14 |
| needs_work rate | ≤ 20.0 % | 5.7 % ✓ | 8.6 % ✓ | 6.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.5 % ✓ | 1.3 % ✓ | 2.2 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.2 % ✓ | 0.9 % ✓ | 0.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.0 % ✗ | 2.2 % ✗ | 0.4 % ✓ |
| needs_work: media | ≤ 10.0 % | 1.2 % ✓ | 4.3 % ✓ | 3.5 % ✓ |
| media: no pick in review 1 |  | 37 | 37 | 27 |
| media: recovered by research |  | 35 | 28 | 22 |
| media: no pick at record |  | 3 | 9 | 6 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 12.2 % ✓ | 17.7 % ✓ | 17.7 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 63.4 % ✓ | 48.2 % ✗ | 58.0 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.11 ✓ | 0.71 ✓ | 1.75 ✗ |
| approved 11–15 |  | 59 | 47 | 47 |
| top move | ≤ 25.0 % | 14.8 % ✓ | 14.2 % ✓ | 20.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 80.3 % | 79.3 % | 72.4 % |
| values stimulus |  | 4 | 5 | 5 |
| top clue | ≤ 60.0 % | 45.5 % ✓ | 44.8 % ✓ | 47.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 22.5 % ✓ | 22.4 % ✓ | 23.7 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 24.2 % ✓ | 20.3 % ✓ | 17.5 % ✓ |
| values lens |  | 10 | 11 | 11 |
| media share | 15.0 %–50.0 % | 19.7 % ✓ | 20.7 % ✓ | 27.6 % ✓ |
| mean fun | ≥ 3.40 | 3.51 ✓ | 3.47 ✓ | 3.56 ✓ |
| cost $ |  | $70.75 | $67.46 | $64.05 |
| $ per approved | ≤ $0.35 | $0.31 ✓ | $0.32 ✓ | $0.30 ✓ |
| calls |  | 493 | 471 | 470 |
| calls per approved |  | 2.14 | 2.22 | 2.20 |
| wall time h |  | 1.96 | 1.89 | 1.84 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 1 of 4 (25 %)
- Problems by kind: giveaway 8 (0 major), fact 1 (0 major), overlap 1 (0 major), media 2 (1 major), difficulty 1 (0 major), style 1 (0 major), other 3 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.28

Major findings on approved questions:

None.

## Needs work

- **q-12725** (american-football) This stadium is the home field of the New York Giants. In which state is it? → New Jersey: Fact check: wrong. Hint 1 says the stadium is about 5 miles (8 km) from New York City. MetLife Stadium in East Rutherford is about 8 miles (13 km) from Midtown Manhattan. The answer, New Jersey, is correct.
- **q-12734** (american-literature) A famous Dr. Seuss character wears a tall striped hat like this one. What kind of animal is he? → A cat: None of the candidates shows what the question needs, a tall striped top hat on its own ("like this one"). They are 18th-century fashion prints with plain black top hats (1, 2, 4, 6), a traffic cone on a pavement (3) and a parade zombie in a striped shirt with a plain brown hat (5). No new search is allowed, so the media slot can't be filled. The text itself is fine. No suitable picture found for this question.
- **q-12780** (fairs-and-festivals) Look at this close-up from a fair. You pick one up and check the number underneath to see your prize. Which game is it? → Duck pond: No candidate shows a duck pond game. Candidate 1 is a shooting gallery with rubber ducks as targets, which is the wrong game and would mislead players. Candidates 2–6 are baseball players. Another search isn't allowed, so the essential image slot needs a close-up of rubber ducks floating in a carnival duck pond, for example from the query "hook a duck game". No suitable picture found for this question.
- **q-12791** (household-brands) The Super Soaker water gun, a huge hit in the 1990s, was invented by Lonnie Johnson. What was his job? → A NASA engineer: Hint 1 ("He studied engineering and holds dozens of patents") gives the answer away: only one option is an engineer, so the first and vaguest hint already solves it. Rewrite hint 1 as a vague hint that doesn't point to engineering, e.g. about his Alabama childhood of building robots and rockets, or that he had worked for the US Air Force.
- **q-12816** (native-nations) The Mayflower Pilgrims arrived in 1620, but they weren't the first lasting English colony in America. Which settlement, founded in 1607, was? → Jamestown: This question overlaps two drafts in the same subcategory. Hint 3 says the colony is in Virginia, which answers q-12808 ("first lasting English colony… which present-day state?" → Virginia). Hint 2 names John Smith, the answer to q-12813. Drop or rework one of the overlapping questions, or change hints 2 and 3 so they don't reveal those answers. One minor point: the description's "66 days" is the length of the Mayflower crossing, not the Jamestown one.
- **q-12818** (nineteenth-century) Whose portrait is on the front of the US five-dollar bill, like this one? → Abraham Lincoln: The only usable front image (candidate 2, the Series 2006 obverse) has the name “Lincoln” printed under the portrait. At this resolution it can be read on a TV, which gives the answer away, and the pipeline can't crop it. Every US $5 front has the name printed, so the slot needs a cropped version of candidate 2 that cuts off the name, or a hand-made crop of the portrait. No suitable picture found for this question.
- **q-12827** (place-names) Valdez, Alaska, which locals say “val-DEEZ,” was named in 1790 by a Spanish explorer. Whom did he name it after? → Spain's minister of the navy: Hint 1 ("a powerful man back in Europe") gives the answer away: among the four options, only Spain's navy minister was a powerful man in Europe. The Mexican general, the Russian fur trader and the gold rush miner all drop out at once. Hint 1 should stay vague, for example about the era or about Spanish naming customs. Separately, the distractors are weak: there was no Mexico and no gold rush in 1790. That alone isn't a reason to send it back, but it makes the question easy to solve by elimination.
- **q-12839** (restaurant-chains) White Castle's tiny square burgers have five holes and are steamed on onions. What word do Americans use for small burgers like these? → Sliders: Hint 1 ("close to a word for something kids ride down at the playground") points straight to "slide". None of the other options sounds like that, so the first hint already gives the answer away. Hint 2 gives it away too. Hint 1 should be vague, for example about where the nickname came from or about eating several at once, and the wordplay should only come in hint 3.
- **q-12846** (baseball) Which of these sports is NOT played with a bat? → Tennis: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-12857** (fairs-and-festivals) In mutton busting, young kids at a rodeo hang on to a running sheep as long as they can. Most contests set a top weight for riders. About how much? → About 60 pounds (27 kg): The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-12890** (rivers-lakes-and-mountains) Signs like this one appear in Pacific Northwest forests. Bigfoot's other name, “Sasquatch,” comes from which kind of language? → A First Nations language from Canada: The question says “Signs like this one”, so the picture has to show a Sasquatch/Bigfoot crossing sign. None of the candidates does, and no new search is allowed. Find a Bigfoot crossing sign photo by hand (for example search Commons for “Bigfoot crossing sign”), or reword the question so it doesn't point at a sign. No suitable picture found for this question.
- **q-12921** (state-symbols) The cactus wren, a loud desert bird that nests in cactus, is the state bird of the state on this map. Which state is it? → Arizona: No candidate works as the essential unlabeled outline of Arizona, and no new search is allowed. #2 and #6 print "Arizona" on the map, #1 is a labeled regional map, #3 is a faded military-division map, and #4 and #5 are Moon photos. The slot needs a plain, unlabeled Arizona outline (for example a blank Arizona locator or outline map from Commons). No suitable picture found for this question.
- **q-12925** (state-symbols) Which of these is NOT a real name for people from a US state? → New Yorkian: None of the media candidates fit the question. The search term "kids sports stadium" came from the sports-meet scene that was cut, and the results are stadiums in Australia, Mexico City and Ohio, plus a galaxy (#6). The decorative image should show the question's world, for example "US state flags" or "map of United States". A new search isn't allowed here, so the slot needs a manual search. No suitable picture found for this question.
- **q-12952** (winter-holidays) It hangs by the fireplace, it often has your name on it, and Santa fills it with small gifts. It looks like a giant what? → Sock: Hint 2 ("shaped like a long tube with a bend near one end") describes a sock so exactly that it gives the answer away: none of the other options (glove, hat, scarf) has that shape. Hint 2 should be a vaguer hint, for example about clothing in general, and not describe the sock's shape.

## Question axes

- move: analogy 6, cause_effect 9, count 6, estimate 12, identify 46, made_of 13, name_concept 26, odd_one_out 9, origin 28, purpose 12, record 6, sequence 9, when 11, who 18, word_meaning 17
- stimulus: detail 18, map_outline 5, none 165, photo 39, sound 1
- clue: completion 9, direct 109, riddle 19, scenario 30, three_facts 61
- answer_kind: group 32, number 20, person 32, place 32, thing 45, time 13, word 54
- lens: body_senses 10, educational_media 17, everyday 39, history 37, language 39, nature 10, pop_culture 40, popular_science 3, school 19, science_news 2, university 12

## Dropped by the pipeline

- american-literature-1: overlap like q-4627: This is the top of a famous skyscraper that was the tallest building in the world for about 40 years. Which building is it? → Empire State Building: In the Percy Jackson books, Mount Olympus, home of the Greek gods, sits on a secret 600th floor of this building. What is it? → The Empire State Building
- candy-and-snacks-8: overlap like q-5350: You finish a bag of Cheetos and your fingertips are bright orange. That orange dust is a seasoning made mostly from which food? → Cheese: These smiling, fish-shaped crackers are a classic orange color. What food gives them their flavor? → Cheese
- cities-and-towns-0: overlap like q-2694: I own the nuclear power plant in Springfield, so Homer Simpson's paycheck comes from me. Who am I? → Mr. Burns: I'm in Springfield, Mr. Burns owns me, and Homer Simpson is my safety inspector, who often falls asleep on the job. What am I? → A nuclear power plant
- cities-and-towns-5: overlap like q-0467: ¿Qué personaje de dibujos animados es? Vive en la Edad de Piedra, trabaja en una cantera manejando un dinosaurio como si fuera una grúa y es el papá de una bebé llamada Pebbles. → Pedro Picapiedra: I live in the Stone Age town of Bedrock, I work at a gravel quarry, my best friend Barney lives next door, and I power my car with my feet. Who am I? → Fred Flintstone
- cities-and-towns-7: overlap like q-9091: In 1992 I won Olympic gold in Barcelona with the “Dream Team.” I won six NBA titles and was named Finals MVP every time. Who am I? → Michael Jordan: I played for Chicago's NBA team, wore number 23, won six titles in the 1990s, and the sneakers named after me still sell today. Who am I? → Michael Jordan
- cities-and-towns-9: overlap like q-1655: Nació en Nueva Orleans, se improvisa mucho y Louis Armstrong la tocaba con su trompeta. ¿Qué género musical es? → Jazz: I grew up in New Orleans, played the trumpet, sang with a gravelly voice, and had a hit with “What a Wonderful World.” Who am I? → Louis Armstrong
- cities-and-towns-11: overlap like q-2001: Monks Mound, cerca de San Luis (Estados Unidos), es una gran pirámide de tierra de la antigua Cahokia. ¿Quién la construyó? → Pueblos nativos de Norteamérica: Around the year 1100, Cahokia, near today's St. Louis, was the biggest city north of Mexico, with huge earthen mounds. Which culture built it? → The Mississippian culture
- cities-and-towns-13: overlap like q-8717: This shark can grow longer than a car, is the biggest hunting fish in the sea, and stars in the film “Jaws.” Which shark is it? → Great white shark: In a 1975 movie, a shark with a fin like this terrorizes the beaches of Amity Island. Which kind of shark is it? → A great white shark
- cities-and-towns-14: overlap like q-2259: In 2023, I broke a record that had stood since 1984 and became the top scorer in NBA history. Who am I? → LeBron James: This player joined the Los Angeles Lakers in 2018, and in 2023 he became the NBA's all-time top scorer. Who is he? → LeBron James
- college-sports-2: overlap like q-7115: Estás jugando ponchados en el recreo y tienes el balón en la mano. ¿Para qué lo lanzas? → Para sacar a un rival: In this game from American gym class, what are the players trying to do with the ball? → Hit players on the other team with it
- college-sports-8: overlap like q-6145: Cheerleaders shake pom-poms like these at games. What are they usually made of today? → Thin plastic strips: I come in pairs, I’m made of lots of shiny plastic strips, and cheerleaders shake me at football games. What am I? → Pom-poms
- colonies-and-founding-13: overlap like q-8848: Every July 4, Americans light up the night sky like this. Whose birthday are they celebrating? → The United States: You're watching fireworks on Independence Day in the United States. What's the date? → July 4
- fairs-and-festivals-16: overlap like q-8848: Every July 4, Americans light up the night sky like this. Whose birthday are they celebrating? → The United States: Look at this close-up. American towns cover parade floats with it in the morning and watch fireworks that night. Which holiday is it? → Fourth of July
- family-and-school-traditions-2: overlap like q-8848: Every July 4, Americans light up the night sky like this. Whose birthday are they celebrating? → The United States: Fireworks like these light up the sky all over America every July 4. Whose birthday are they celebrating? → The United States
- family-and-school-traditions-9: overlap like q-6145: Cheerleaders shake pom-poms like these at games. What are they usually made of today? → Thin plastic strips: I shake pom-poms, shout “Go, team, go!” from the sidelines and do flips and jumps. Who am I? → A cheerleader
- household-brands-0: overlap like q-5686: In 1924, a company sold soft paper sheets for wiping off makeup, but buyers found a different use that became their main job. What were they? → Tissues: Kleenex first went on sale in 1924 to wipe off makeup. It pops out of a box one sheet at a time, and Americans use the name for any tissue. What do most people use one for? → Blowing your nose
- more-sports-12: overlap like q-11893: I'm big and grassy, with ponds and little flags. In 1997, Tiger Woods won the Masters on me at just 21. What am I? → A golf course: Which golfer won the 1997 Masters at age 21, the youngest champion ever, and by a record 12 strokes? → Tiger Woods
- native-nations-15: overlap like q-11775: I was a Lakota holy man and leader. In 1876, I had a vision of soldiers falling into our camp like grasshoppers. Soon after, we beat Custer at Little Bighorn. Who am I? → Sitting Bull: This Lakota leader toured with Buffalo Bill's Wild West show in 1885. Who is he? → Sitting Bull
- nineteenth-century-3: overlap like q-1604: Adivina: nací en 1873 para los mineros de California, tengo remaches de cobre y en mi etiqueta dos caballos intentan romperme. ¿Qué soy? → Los jeans: Work pants like these, with copper rivets at the pockets, were patented in 1873 for workers out West. Which San Francisco businessman's name became the famous brand? → Levi Strauss
- nineteenth-century-7: overlap like q-4934: This hat has a very wide brim, ranchers in the Wild West wore it, and Woody from Toy Story has one. What is it called? → A cowboy hat: Who would wear a hat like this one to work? → A cowboy
- nineteenth-century-12: overlap like q-11780: This stone bridge stands on the 1862 Antietam battlefield, a Civil War site many say is haunted. In which state is it? → Maryland: The Battle of Antietam was fought in 1862 in the state shown on this map. Which state is it? → Maryland
- place-names-6: overlap like q-2895: This snowy volcano, Mount Rainier, is in the only US state named after a president. Which state is it? → Washington: Tacoma, Washington, takes its name from a Native name for the mountain in this photo. What do most maps call it? → Mount Rainier
- place-names-10: overlap like q-12809: It starts in Minnesota, flows past St. Louis and New Orleans, and its name comes from an Ojibwe word for “great river.” What is it? → The Mississippi River: The state of Michigan is named after a great lake. That lake's name comes from a word meaning “great water” in which people's language? → The Ojibwe
- regional-dishes-4: overlap like q-8963: It's brushed on ribs, it's sweet and smoky, and the most common kind gets its red color mostly from which food? → Tomatoes: Red salsa for tortilla chips gets its color mostly from which fruit? → Tomato
- regional-dishes-5: overlap like q-10713: “All y'all” means every single one of you. In which part of the US is this phrase famous? → The South: Sweet tea is served iced, very sugary and by the pitcher, often next to fried chicken. Which part of the US is it famous in? → The South
- regional-dishes-10: overlap like q-8993: Breaux Bridge, a Cajun town in Louisiana, calls itself the world capital of which food? → Crawfish: In Louisiana, crawfish étouffée is crawfish in a thick sauce over rice. What does “étouffée” mean in French? → Smothered
- regional-dishes-14: overlap like q-1576: Soy un snack triangular, crujiente y anaranjado, y nací para no desperdiciar sobras en un restaurante de Disneyland. ¿De qué estoy hecho? → Maíz: The crunchy chips in nachos like these are made mostly from which plant? → Corn
- regional-dishes-15: overlap like q-11755: Despite the saying “as American as apple pie,” apples aren't native to America, and the oldest known apple pie recipe is from 1381. Which country is it from? → England: Complete the saying: “As American as…” → Apple pie
- restaurant-chains-2: overlap like q-1147: Mi cara, con traje blanco y barbita de chivo, sale en baldes de pollo frito. ¿Qué estado de EE. UU. lleva mi cadena en su nombre? → Kentucky: This chain sells fried chicken in buckets, keeps a secret recipe of 11 herbs and spices, and has an old colonel on its logo. Which chain is it? → KFC
- restaurant-chains-5: overlap like q-3662: When people talk about “the Golden Arches”, what are they talking about? → McDonald's: You open a red box with a toy inside. It's a Happy Meal from the world's biggest burger chain. Where are you eating? → McDonald's
- restaurant-chains-9: overlap like q-1411: Una cadena de comida rápida invitaba a 'pensar fuera del pan' porque vendía tacos y burritos. ¿De qué país es esa comida? → México: This US chain sells tacos, burritos and quesadillas, and its logo is a bell. Which country's food inspired its menu? → Mexico
- baseball-9: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: If a Major League Baseball game is still tied, after how many innings does it go into extra innings? → 9
- candy-and-snacks-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: You get it buttery in a big striped bucket, and you munch it while the lights go down. Where do you usually buy it? → At the movie theater
- winter-holidays-3: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Finish the line from the American song “Santa Claus Is Comin' to Town”: “He's making a list and checking it twice, gonna find out who's naughty or…” → Nice
- winter-holidays-10: overlap like q-4888: I wear the same red as Coca-Cola, have a big white beard and come down chimneys once a year. Who am I? → Santa Claus: It's on the roof, smoke goes up it, and on Christmas Eve Santa slides down it. What is it? → The chimney
- winter-holidays-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: This golden statue looks over a famous ice rink in New York. Every December, what huge thing stands right behind it? → A Christmas tree
- candy-and-snacks-11: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In 1949, a couple started this hard-candy company in Golden, a town in the Rocky Mountains, and named it after a friendly Western ranch owner. In which state? → Colorado
- fairs-and-festivals-0: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: At many American county fairs, piglets with funny names wear numbered vests while the crowd cheers for a favorite. What is this show called? → A pig race
- fairs-and-festivals-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Look at this close-up from a fair. Which carnival game is it? → Water gun race
- family-and-school-traditions-14: overlap like winter-holidays-16: I march at the front of a parade band in a tall hat, waving a long baton to keep everyone in step. Who am I? → The drum major: I march in front of the band in a tall hat, I blow a whistle and raise a mace, and the musicians follow my signals. Who am I? → The drum major
- home-cooking-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: You split a warm, sweet biscuit, then pile on sliced strawberries and whipped cream. What is this American dessert called? → Strawberry shortcake
- household-brands-3: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: You're rinsing your mouth with Listerine. Its name honors which British surgeon, famous for killing germs during operations? → Joseph Lister
- household-brands-12: fact-check wrong: Hint 3 is false. Aflac's full legal name is "American Family Life Assurance Company of Columbus", so it ends in "of Columbus", not "Life Assurance Company". The answer, wrong answers and fun fact are fine.: Since 2000, a white duck has starred in this American company's TV ads, loudly quacking its name, “Aflac!” What does Aflac sell? → Insurance
- household-brands-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In the board game Sorry!, you send rivals back to Start and slide along arrow spaces. What are the numbered cards for? → Telling you how far to move
- household-brands-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which of these is NOT part of the classic look of Mr. Clean, the mascot on the cleaning bottle? → A baseball cap
- household-brands-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: A Sharpie has a felt tip, and sports stars sign autographs with it. What is a Sharpie for? → Writing that won't rub off
- more-sports-1: overlap like q-11913: At this spot in Pittsburgh, rivers meet to form the Ohio River. How many rivers join here to start it? → 2: My hockey team is named after a bird that can't fly, and in my downtown two rivers meet to form a third. Which city am I? → Pittsburgh
- nineteenth-century-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: “As a girl in Ohio, I hunted to help pay off my family's farm. I beat a famous marksman in a match, then married him. I starred in Buffalo Bill's Wild West show.” Who am I? → Annie Oakley
- nineteenth-century-14: overlap like q-12730: Ohio is “the Buckeye State,” buckeye means “eye of a male deer,” and Ohio State players earn buckeye stickers for their helmets. What is a buckeye? → A tree: Andrew Jackson was so tough his soldiers nicknamed him “Old Hickory.” Hickory is a kind of… → Tree
- regional-dishes-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: This is goetta, a Cincinnati breakfast fried in slices. Besides meat, which grain holds it together? → Oats
- regional-dishes-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Portuguese workers brought it to Hawaii in the 1800s, it's rolled in sugar, and Hawaii eats piles of them on Fat Tuesday. What is a malasada? → A doughnut
- restaurant-chains-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Little Caesars started shouting “Pizza! Pizza!” in 1979, when the slogan stood for a special deal. What did it promise? → Two pizzas for the price of one
- restaurant-chains-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: You're eating Nashville-style chicken at Dave's Hot Chicken, which began in a Los Angeles parking lot in 2017. Which rapper invested in it? → Drake
- restaurant-chains-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Pizza Hut got its short name because the sign on its first restaurant only had room for a few letters. How many? → 8
- rivers-lakes-and-mountains-15: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: At Hawaii Volcanoes National Park, wind stretches flying lava drops into thin, golden threads of glass. Named after Hawaii's volcano goddess, what are they called? → Pele's hair
- roads-and-landmarks-6: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: The Studio Tour at Universal Studios Hollywood rolls through the famous “backlot.” What is a backlot? → An outdoor area of film sets
- roads-and-landmarks-13: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: You're driving alone on a US freeway. Who could ride along so you can legally use the lane marked with a white diamond? → Any passenger of any age
- state-symbols-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This is North Carolina's state vegetable. Which scientist, born into slavery, found more than 100 uses for it? → George Washington Carver
- state-symbols-14: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: The Baltimore oriole was named because its orange and black feathers matched the colors of the family that founded which colony? → Maryland
- traditional-songs-0: hard fail: correct 4, unambiguous 3, no_giveaway 2, no_overlap 5: In “Old MacDonald Had a Farm,” every verse brings a new farm animal. What do little kids learn from singing it? → Animal sounds
- traditional-songs-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In the Hokey Pokey, you put something in, take it out, and shake it all about. What does each verse name? → Body parts
- weather-and-seasons-15: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In the American South and West, people say “That was a real gully washer!” What are they talking about? → A sudden, very heavy rainstorm
- weather-and-seasons-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: During long droughts, Californians were asked not to water their lawns. What did some people do to their brown grass instead? → Painted it green
- rivers-lakes-and-mountains-3: overlap like q-11762: Paul Bunyan, the giant of American tall tales, swings his huge axe all day. What is his job? → Lumberjack: This giant statue stands in Bemidji, Minnesota, next to a big blue ox. Which tall-tale hero is it? → Paul Bunyan
- rivers-lakes-and-mountains-7: overlap like q-8927: You stand at the rim of Bryce Canyon in Utah, looking at thousands of orange rock spires called hoodoos. What mainly carved them? → Ice freezing and melting in cracks: I was a Scottish-born pioneer. In the 1870s, I grazed cattle below a maze of orange rock spires in Utah, and the park there carries my last name today. Who am I? → Ebenezer Bryce
- roads-and-landmarks-1: overlap like q-1302: Escribí la novela de un hotel embrujado y nevado que Stanley Kubrick llevó al cine en 1980, aunque su versión no me gustó. ¿Quién soy? → Stephen King: In 1974, Stephen King spent a night at the nearly empty Stanley Hotel in Colorado. Which of his novels grew out of that stay? → The Shining
- state-symbols-3: duplicate like q-11780: This stone bridge stands on the 1862 Antietam battlefield, a Civil War site many say is haunted. In which state is it? → Maryland: This black-and-gold pattern is part of a state flag that many people call the boldest in the US. Which state is it? → Maryland
- state-symbols-7: overlap like q-11916: Oklahoma's college teams are called the Sooners, after people in the 1889 Land Rush. Who were the first Sooners? → Settlers who sneaked in before the start: People from Oklahoma are called “Sooners.” Who were the first Sooners? → Settlers who sneaked in before a land race began
- state-symbols-8: overlap like q-8901: Texans say “Everything's bigger in Texas,” and for a long time it was the largest US state. Why did it slip to second place in 1959? → Alaska became a state: Texas's state song once called it “largest and grandest.” The words changed after the state on this map joined the US in 1959. Which state? → Alaska
- state-symbols-17: overlap like q-3055: Which people first built this kind of boat, for hunting in icy Arctic waters? → The Inuit: Native peoples of Alaska and the Arctic invented this boat long ago, with animal skin stretched over a frame. What is it? → Kayak
- traditional-songs-1: overlap like q-1254: Se hace con las dos manos, hace ruido y la canción 'Si estás feliz y lo sabes' te pide hacerlo. ¿Qué es? → Aplaudir: You're singing “If You're Happy and You Know It.” Which of these does the song NOT ask you to do? → Brush your teeth
- weather-and-seasons-0: overlap like q-7921: Su nombre viene del taíno, el de un dios de las tormentas, y en 2020 uno arrasó la isla de Providencia. ¿Qué es? → Huracán: I'm a giant spinning storm that grows over warm ocean water. I have a calm “eye” in my middle and I often hit Florida in late summer. What am I? → A hurricane
- weather-and-seasons-6: overlap like q-10507: In “The Wonderful Wizard of Oz,” which girl follows the yellow brick road to find the Wizard? → Dorothy: A Kansas twister carried me, my little dog and my whole house to a magical land. I followed a yellow brick road to get home. Who am I? → Dorothy
- wildlife-1: overlap like q-1837: Esta tortuga caimán pesca con un «gusanito» rosado en la lengua. ¿Dónde vive en libertad? → En el sureste de Estados Unidos: It lives in rivers of the southeastern US, has a spiky ridged shell and can weigh over 150 lb (68 kg). What is North America's heaviest freshwater turtle? → Alligator snapping turtle
- wildlife-3: overlap like q-9300: Das Tier, das diesen Baum so angenagt hat, war in Deutschland fast ausgerottet. Zu welcher Tiergruppe gehört es? → Nagetiere: Watch this beaver at work. Which animal group does it belong to? → Rodents
- wildlife-5: overlap like q-8716: This sea otter floats on its back and smashes its lunch against a stone on its chest. What is that lunch mostly? → Shellfish and sea urchins: Sea otters float on their backs, hold paws while they sleep, and crack shellfish with rocks. Along which US coast do they live in the wild? → The Pacific coast
- winter-holidays-4: overlap like q-11787: In 1621, Pilgrims who came on the Mayflower shared a three-day harvest feast with the Wampanoag people. In which colony? → Plymouth: This rock, carved with the year 1620, is said to be where the Mayflower Pilgrims stepped ashore. In which town is it? → Plymouth
- winter-holidays-6: overlap like q-9077: Georgia is called the Peach State. In which season are its peaches picked and sold at roadside stands? → Summer: Every winter, Atlanta hosts a big college football bowl game named after its state's nickname. Which nickname? → The Peach State
- winter-holidays-8: overlap like q-4229: It is the northernmost point on Earth, it lies on floating sea ice, and stories say Santa lives there. What is it? → The North Pole: This hat belongs to Santa Claus. In the stories, where does he live? → The North Pole
- winter-holidays-9: overlap like q-2719: “I live in a pineapple under the sea, and I work at the Krusty Krab.” What is my job called? → Fry cook: I'm a giant balloon in New York's Thanksgiving parade. I'm yellow and boxy, and in my cartoon I work as a fry cook. Who am I? → SpongeBob SquarePants
- winter-holidays-11: overlap like q-3757: I'm small, I have pointy ears and I live at the North Pole with Santa Claus. What is my job there? → Making toys: In the stories, who works all year in Santa's workshop making toys? → Elves
- winter-holidays-16: overlap like family-and-school-traditions-14: I march in front of the band in a tall hat, I blow a whistle and raise a mace, and the musicians follow my signals. Who am I? → The drum major: I march at the front of a parade band in a tall hat, waving a long baton to keep everyone in step. Who am I? → The drum major
