# batch-27

Made by `qgen batch` on 2026-10-29 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): states-and-capitals, cities-and-towns, rivers-lakes-and-mountains, roads-and-landmarks, wildlife, plants-and-trees, national-parks, weather-and-seasons, native-nations, colonies-and-founding, nineteenth-century, twentieth-century, civics, inventors-and-founders, trailblazers, regional-dishes, home-cooking, desserts-and-baking, candy-and-snacks, restaurant-chains, holidays, winter-holidays, fairs-and-festivals, family-and-school-traditions, folk-heroes-and-tall-tales
- Merged: 287 (q-8833…q-9119)
- Approved: 261
- Needs work: 26
- Dropped by the pipeline: 50
- Reviewed by: claude-opus-5-5
- Claude calls: 609, about $71.67 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-25, batch-26; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-25 | batch-26 | batch-27 |
|---|---|---:|---:|---:|
| source locale |  | es | en | en |
| drafts |  | 206 | 412 | 337 |
| skipped slots |  | 280 | 92 | 113 |
| dropped |  | 84 | 85 | 50 |
| drop rate | ≤ 20.0 % | 40.8 % ✗ | 20.6 % ✗ | 14.8 % ✓ |
| dropped: hard fail correct |  | 2 | 0 | 3 |
| dropped: hard fail unambiguous |  | 0 | 0 | 2 |
| dropped: hard fail no_giveaway |  | 12 | 19 | 14 |
| dropped: overlap |  | 68 | 65 | 30 |
| dropped: duplicate |  | 2 | 1 | 1 |
| dropped: fact-check wrong |  | 1 | 0 | 0 |
| merged |  | 122 | 327 | 287 |
| approved |  | 114 | 302 | 261 |
| needs_work |  | 8 | 25 | 26 |
| needs_work rate | ≤ 20.0 % | 6.6 % ✓ | 7.6 % ✓ | 9.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.5 % ✓ | 2.1 % ✓ | 3.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.6 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.5 % ✗ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 3.3 % ✓ | 4.3 % ✓ | 5.6 % ✓ |
| media: no pick in review 1 |  | 19 | 50 | 34 |
| media: recovered by research |  | 15 | 36 | 27 |
| media: no pick at record |  | 4 | 14 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.8 % ✓ | 0.9 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 35.4 % ✗ | 16.3 % ✓ | 9.5 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 21.6 % ✗ | 74.3 % ✓ | 68.1 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.78 ✗ | 1.00 ✓ | 1.71 ✗ |
| approved 11–15 |  | 28 | 62 | 49 |
| top move | ≤ 25.0 % | 15.6 % ✓ | 16.2 % ✓ | 17.1 % ✓ |
| values move |  | 14 | 15 | 15 |
| top stimulus |  | 83.6 % | 76.1 % | 77.7 % |
| values stimulus |  | 4 | 5 | 5 |
| top clue | ≤ 60.0 % | 39.3 % ✓ | 44.6 % ✓ | 48.1 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.4 % ✓ | 31.5 % ✓ | 30.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 27.0 % ✗ | 15.3 % ✓ | 15.7 % ✓ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 16.4 % ✓ | 23.9 % ✓ | 22.3 % ✓ |
| mean fun | ≥ 3.40 | 3.32 ✗ | 3.61 ✓ | 3.65 ✓ |
| cost $ |  | $42.86 | $78.80 | $69.16 |
| $ per approved | ≤ $0.35 | $0.38 ✗ | $0.26 ✓ | $0.26 ✓ |
| calls |  | 281 | 627 | 549 |
| calls per approved |  | 2.46 | 2.08 | 2.10 |
| wall time h |  | 1.32 | 2.56 | 2.25 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 55 (2 %)
- Major among review needs work: 0 of 5 (0 %)
- Problems by kind: giveaway 11 (0 major), media 6 (1 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.51

Major findings on approved questions:

- **q-9026**: media — The facts check out: the plate lunch (two scoops of rice, macaroni salad, a main dish) is a Hawaiian classic that came from multi-ethnic plantation workers, and Louisiana, California and Texas are clearly wrong. The problem is the media file, "L&L Hawaiian BBQ beef curry meal.JPG". Its title names the answer, and L&L packaging or branding in the photo could show "Hawaiian" on screen. The photo also isn't essential to the question, so an illustrative plate-lunch image with no branding, or a decorative image, would be better. Difficulty 9 is within range (I'd put it at about 8). The loco moco question (q-9028) is related but doesn't give this one away. (http://127.0.0.1:8001/review/q-9026)

## Needs work

- **q-8833** (candy-and-snacks) In the film E.T., Elliott lays a trail of candy to lure the alien into the house. What's inside those crunchy candies? → Peanut butter: None of the media candidates fits the question. They are a watermelon seed-catalog print, a "Breeder and Sportsman" masthead and a 1943 newspaper front page about a glider crash. No new search is allowed, so this slot needs a new image, for example a suburban house at night or a forest at night. No suitable picture found for this question.
- **q-8841** (cities-and-towns) If you visit Roanoke Island, you can watch a play about colonists who vanished, leaving only the word “CROATOAN” carved on a post. When did they arrive? → 1580s: Hint 1 (“It was before Jamestown”) gives the answer away. Jamestown (1607) is standard US school knowledge, and all three wrong answers (1620s, 1690s, 1730s) come after it. Hint 2 (Elizabeth I, who ruled until 1603) does the same. Make hints 1 and 2 vaguer, or add a wrong answer from the 16th century (for example 1550s) so these hints don't settle the question.
- **q-8850** (civics) How many jurors decide the verdict in a US federal criminal trial? → 12: Hint 2 gives the answer away: hint 1 ("even number") leaves only 6 and 12, and hint 2 then says federal trials use the "full traditional size" as opposed to smaller juries, which rules out 6. Hint 2 should hint at something else (for example the Sixth Amendment's right to a jury trial) without pointing to the bigger number.
- **q-8852** (civics) In 2010, the Supreme Court decided Citizens United v. FEC, a case that began over a film criticizing Hillary Clinton. What did the ruling allow? → Unlimited corporate spending on independent political ads: The description gives away the answer's defining effect. "Annoys everyone holding a TV remote in election season" points straight at a flood of TV political ads. Read with only the four options, that matches the answer and rules out "A ban on political ads in the final month" and probably "Companies to run their own candidates". Rewrite it to play on the Supreme Court or legal theme without hinting at more ads or more spending. The facts are correct (2010, 5–4, “Hillary: The Movie”, independent expenditures), and media pick 1 is fine.
- **q-8862** (colonies-and-founding) Johnnycakes, like these, are cornmeal flatbreads that colonists learned to make from Native Americans. Which US region are they a classic of? → New England: Hint 2 (“in the far northeast of the country, by the Atlantic”) is simply the definition of New England, and no wrong option is in the northeast. It solves the question at the second hint. Hint 2 needs to be vaguer, for example about the colonial era or the cold, rocky farmland, without saying where the region is. The media is fine: candidate 2 is a clear photo of New England-style jonnycakes with no label.
- **q-8865** (colonies-and-founding) In which decade was “The Spirit of '76,” with its two drummers and a fifer marching under the flag, painted? → The 1870s: The question names a specific artwork, “The Spirit of '76,” but every candidate is a modern fife-and-drum corps (the Old Guard in red coats, Civil War reenactors), not the painting. A new search can't be run, so the slot needs the painting itself (e.g. "Spirit of '76 Willard"). The painting shows a 1776 scene with no date on it, so it wouldn't give away the decade. No suitable picture found for this question.
- **q-8873** (desserts-and-baking) At an American state fair, this ribbon is pinned next to a pie. Which place did the pie win? → First place: None of the candidates works as the essential image. #2 is the only blue ribbon, but its printed text ("FIRST PREMIUM … DELAWARE STATE FAIR") gives the answer away. #1 is a Japanese train award plate, #3 is a train, and #4–#6 are old book scans of horses and buildings. A new search isn't allowed, so the slot needs a blue rosette or ribbon with no text, for example a search for "blue rosette ribbon". No suitable picture found for this question.
- **q-8879** (fairs-and-festivals) The very first Ferris wheel, shown here, was built for the 1893 World's Fair in Chicago. Which famous structure was it meant to outdo? → The Eiffel Tower: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-8892** (family-and-school-traditions) What is this box used for? → Carrying your lunch: None of the candidates shows a lunch box, and this question can't work without one because the image is essential. A new search isn't allowed, so the slot needs a real photo of an open kids' lunch box with food inside (for example, search "lunchbox sandwich apple" or "school lunch box"). No suitable picture found for this question.
- **q-8898** (folk-heroes-and-tall-tales) This Georgia newspaperman collected Br'er Rabbit tales into a best-selling book in 1880. Who is he? → Joel Chandler Harris: The picked picture has an unsuitable licence (pd-us-only: PD-US-1923, PD-US-expired).
- **q-8910** (home-cooking) Before an American meatloaf goes into the oven, what is often spread on top as a shiny glaze? → Ketchup: Hint 1 ("It's red.") gives the answer away: mustard, mayonnaise and ranch are none of them red, so the first and vaguest hint rules out all three wrong answers. Replace it with a vague hint that doesn't single out ketchup by color, for example one about it being a sauce found on most diner tables, or one that is made from a fruit.
- **q-8922** (inventors-and-founders) In 1899 in Colorado Springs, Nikola Tesla built a giant coil that shot bolts of artificial lightning. What did he dream of using such machines for? → Sending power without wires: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-8951** (plants-and-trees) Native Americans of the Southwest crushed the roots of this plant and mixed them with water. What did they make? → Soap: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-8954** (plants-and-trees) Hikers in the US warn each other about poison ivy with a rhyme. How many leaflets does each poison ivy leaf have? → 3: The picked picture has an unsuitable licence (pd-no-reason: public domain without a template).
- **q-8961** (regional-dishes) In Philadelphia, what do you get if you order a hoagie? → A long sandwich on an Italian roll: Hint 2 says "corner shops", which is British usage. This is a usa-bundle question, and Americans (Philadelphians especially) say "corner stores". Change it to "Delis and corner stores all over the city sell it at lunchtime." Everything else checks out, and candidate 4 is a good illustrative image.
- **q-8994** (family-and-school-traditions) The American phrase “jumping the broom” comes from a custom that enslaved African Americans kept alive. What does it mean? → Getting married: The description says the broom's big moment has "nothing to do with the kitchen floor", which rules out the wrong answer "Cleaning up before a holiday" before any hint. Rewrite it to play on brooms or big days without hinting that the custom isn't about sweeping.
- **q-9024** (plants-and-trees) What sweet, tan crystals were a main sweetener of Native Americans in the Northeast long before stores sold white sugar? → Maple sugar: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-9033** (restaurant-chains) I'm a fast-food mascot with a big frozen smile, and my restaurants grill their burgers over flames. Who am I? → The Burger King: Hints 1 and 2 give the answer away: “My restaurants sell the Whopper” names Burger King's signature burger, and “I wear a golden crown” points straight to a “King” among the four options. Hint 1 should be vague, for example about the chain starting in Miami in the 1950s. Hint 2 should be a medium clue that doesn't name the Whopper or the crown. The crown or the Whopper can move to hint 3.
- **q-9041** (rivers-lakes-and-mountains) In 1912, an Alaskan volcano produced the largest eruption of the 20th century. Which volcano? → Novarupta: The description (“did the work while its neighbor took the credit”) gives away the answer's defining trait, the misattribution to Katmai, before any hint. Anyone who links Katmai with 1912 is told to rule it out, and that leaves Novarupta. Hint 1 says the same thing again. Rewrite the description so it plays on Alaska or volcanoes without the credit twist.
- **q-9044** (states-and-capitals) This state takes its name from the river on its southern border, from a Seneca word meaning “good river.” Which state is shown? → Ohio: None of the three candidates works as the essential map. Candidate 1 is an outline of Ohio, but it labels Lake Erie, Cleveland, Cincinnati, Dayton, Kentucky and Pennsylvania, and its caption reads "Outline map of Ohio", so it gives the answer away. Candidates 2 and 3 are township plats from a county atlas, not the state's shape. We can't search again, so an unlabeled Ohio outline (e.g. "Ohio blank map" or "Ohio locator map blank") has to be found by hand. No suitable picture found for this question.
- **q-9049** (twentieth-century) In which decade did the Etch A Sketch first go on sale in American toy stores? → The 1960s: This repeats q-5262, an approved question that already asks the decade the Etch A Sketch first went on sale (answer: 1960s). It only uses other words, so it is the same fact twice in the pool. Drop q-9049 or replace it with a different fact. The picked picture has an unsuitable licence (pd-us-only: PD-US-no notice, PD-US-pre1978).
- **q-9068** (states-and-capitals) What is the capital of the state shown on this map? → Phoenix: No candidate is a plain, unlabeled outline of Arizona. #1, #2 and #6 print "Arizona" (and #1 also prints "Phoenix") right on the map. #3 is a faded map of several western states, and #4 and #5 are Moon photos. No new search is allowed, so the essential map needs a clean Arizona silhouette from somewhere else, for example a blank US-states locator map. No suitable picture found for this question.
- **q-9070** (states-and-capitals) What is the capital of the state shown on this map? → Boise: No candidate shows a plain, unlabeled outline of Idaho. #3 (2020 population density map) has the right shape, but its legend says “Idaho Population Density”, which names the state, and its red cluster marks where Boise is. #4 is full of mine and town labels under an “Idaho Silver Mines” title. The text itself is fine. The slot needs a blank Idaho outline map, for example from a search like “Idaho blank outline map” or “Idaho locator map blank”. No suitable picture found for this question.
- **q-9088** (trailblazers) In 1985, NASA picked this New Hampshire social studies teacher as the first “Teacher in Space.” Who is she? → Christa McAuliffe: The media slot is set up wrongly. Its role is essential and the note asks for a NASA portrait of Christa McAuliffe, which would show the answer. But the search was "New Hampshire classroom chalkboard", so no candidate shows her. The text is fine. Switch the slot to illustrative and pick a plain classroom photo such as candidate 1 or 4 (no readable text). Or use a space shuttle or launch pad image, but not one showing the Challenger by name. No suitable picture found for this question.
- **q-9104** (weather-and-seasons) Southern California's Santa Ana winds are hot, fast, and so dry they fan wildfires every fall. Why are they so dry? → They blow in from inland deserts: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-9113** (wildlife) A huge, shaggy bison blocks a road in Yellowstone. Which group does it NOT belong to? → Hibernators: Hint 2 gives the answer away. "Keep grazing all year round" says outright that bison don't hibernate, so hint 3 adds nothing. Replace hint 2 with something that points toward the answer without stating it, for example their size or their herds, and leave the year-round activity to hint 3.

## Question axes

- move: analogy 3, cause_effect 34, count 5, estimate 15, identify 49, made_of 16, name_concept 28, odd_one_out 8, origin 22, purpose 32, record 11, sequence 8, when 21, who 22, word_meaning 13
- stimulus: detail 10, map_outline 3, none 223, photo 50, video 1
- clue: completion 1, direct 138, riddle 29, scenario 37, three_facts 82
- answer_kind: group 32, number 20, person 39, place 34, thing 87, time 21, word 54
- lens: educational_media 36, everyday 45, history 36, language 34, nature 30, pop_culture 41, popular_science 5, school 37, science_news 9, university 14

## Dropped by the pipeline

- cities-and-towns-2: overlap like q-4720: Batman's Gotham City shares its name with an old nickname of this real city. Which city is it? → New York City: You're reading an old book from 1807 that calls a real city “Gotham.” Long before Batman, which city had that nickname? → New York City
- colonies-and-founding-2: overlap like q-2497: This French thinker wrote “The Spirit of the Laws” and said power should be split into three branches. Who is he? → Montesquieu: You're on a field trip in Washington, D.C., learning about the separation of powers. Into how many branches is the US government split? → 3
- colonies-and-founding-14: overlap like q-8848: Every July 4, Americans light up the night sky like this. Whose birthday are they celebrating? → The United States: Americans celebrate Independence Day with fireworks and parades. On which date is it? → July 4
- fairs-and-festivals-2: overlap like q-8777: At the fair, small electric cars get their power from a metal net on the ceiling. What is this ride called? → Bumper cars: At the fair, you drive a little car with a big rubber ring around it, and banging into the other cars is the whole fun. What is this ride called? → Bumper cars
- folk-heroes-and-tall-tales-17: overlap like q-4934: This hat has a very wide brim, ranchers in the Wild West wore it, and Woody from Toy Story has one. What is it called? → A cowboy hat: In Westerns, the ten-gallon hat is a tall, wide-brimmed hat worn by which kind of person? → A cowboy
- holidays-3: overlap like q-0099: ¿Quién llegó a América en 1492 con tres barcos? → Cristóbal Colón: A US federal holiday on the second Monday in October honors the explorer on top of this column. Who is he? → Christopher Columbus
- home-cooking-12: overlap like q-8897: You're at an American diner and order a tall stack of flapjacks. What arrives? → Pancakes: They're flat and round, cooked on a hot griddle, and Americans stack them high with maple syrup on top. What are they? → Pancakes
- inventors-and-founders-7: overlap like q-1767: ¿Qué presidente aparece en esta moneda de diez centavos de EE. UU.? → Franklin D. Roosevelt: A charity started by a US president who had polio paid for the research behind the polio vaccine. Which president? → Franklin D. Roosevelt
- inventors-and-founders-10: overlap like q-5267: When you fry an egg in a non-stick pan, you can thank a chemist who found the coating by accident in 1938. Who was he? → Roy Plunkett: Roy Plunkett discovered Teflon by accident in 1938. Which of these inventors did NOT make their famous discovery by accident? → Orville Wright
- national-parks-0: overlap like q-4199: I live in the desert and run faster than anyone. A hungry coyote chases me with silly gadgets but never catches me. All I say is “Beep beep!” Who am I? → Road Runner: This bird lives in deserts like Death Valley and would rather run than fly. What is it? → Roadrunner
- national-parks-11: overlap like q-8925: Delicate Arch, the stone arch on Utah's license plates, stands all alone on a rock bowl. About how tall is it? → About 50 feet: Double Arch appears at the start of “Indiana Jones and the Last Crusade,” where young Indy explores a cave. In which state is it? → Utah
- nineteenth-century-2: overlap like q-1514: En 1844, ¿quién envió entre Washington y Baltimore el famoso mensaje «¿Qué ha hecho Dios?»? → Samuel Morse: In 1844 the first official telegraph message, taken from the Bible, read “What hath God wrought.” What does “wrought” mean? → Made or done
- nineteenth-century-11: overlap like q-3669: In which year did Wyatt Earp and Doc Holliday take part in the gunfight at the O.K. Corral in Tombstone, Arizona? → 1881: Wyatt Earp became a Wild West legend after a 30-second gunfight in 1881. In which Arizona town did it happen? → Tombstone
- nineteenth-century-16: overlap like q-3666: In cowboy films, a man pins a shiny metal star on his shirt and chases outlaws. Why does he wear the star? → To show he is the sheriff: In the Wild West, he was picked by the people of the county, gathered a posse to chase outlaws, and locked them up in jail. What was his job? → Sheriff
- plants-and-trees-11: overlap like q-0918: Soy el árbol más grande del mundo por volumen, una secuoya de California con nombre de general de la guerra civil de EE. UU. ¿Cómo me llamo? → General Sherman: This is the trunk of the General Sherman in California, the biggest living tree on Earth by volume. What kind of tree is it? → Giant sequoia
- plants-and-trees-13: overlap like q-2895: This snowy volcano, Mount Rainier, is in the only US state named after a president. Which state is it? → Washington: This mossy forest gets about 12 feet (3.7 m) of rain a year, one of the wettest places in the lower 48 states. In which state is it? → Washington
- plants-and-trees-16: overlap like q-8582: If you heat these hard little corn kernels in a pot, what do they turn into? → Popcorn: It's sold in big buckets at the movie theater, it's crunchy and fluffy, and people often put butter on it. What is it? → Popcorn
- regional-dishes-11: overlap like q-1576: Soy un snack triangular, crujiente y anaranjado, y nací para no desperdiciar sobras en un restaurante de Disneyland. ¿De qué estoy hecho? → Maíz: Look at this stadium snack. What are the crunchy chips under the melted cheese made from? → Corn
- cities-and-towns-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: The Kansas City Chiefs play at Arrowhead Stadium, where Taylor Swift famously cheered for Travis Kelce in 2023. In which state is it? → Missouri
- cities-and-towns-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: I'm a baseball team, and in 2016 I won my first World Series in 108 years. Who am I? → The Chicago Cubs
- wildlife-0: duplicate like q-1704: Esta trucha arcoíris es común en los ríos fríos de los Andes, pero no es nativa de allí. ¿De dónde es originaria? → De Norteamérica: This masked animal now also lives wild in Germany and Japan. Which continent did it originally come from? → North America
- wildlife-8: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: He wears a hat and tie, lives in Jellystone Park with his buddy Boo-Boo, and says he's “smarter than the average bear.” What is he always scheming to grab? → Picnic baskets
- winter-holidays-14: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 5: This close-up shows part of a favorite Christmas decoration. What is it? → A Christmas stocking
- civics-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: I'm small and round. Poll workers hand me out after you fill in your ballot, and people wear me proudly on their shirts. What am I? → An “I Voted” sticker
- civics-11: hard fail: correct 2, unambiguous 5, no_giveaway 4, no_overlap 4: If a vote in the US Senate ends in a tie, who casts the deciding vote? → The vice president
- civics-16: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: The 16th Amendment of 1913 allowed a federal income tax. Before that, what was the biggest source of federal money? → Tariffs on imported goods
- desserts-and-baking-3: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: This donut has no hole, it's dusted with powdered sugar, and a bite squirts out sweet strawberry or raspberry filling. What is it called? → A jelly donut
- family-and-school-traditions-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: At American summer camp, kids sing “Kumbaya,” “Boom Chicka Boom” and “The Ants Go Marching” together at night. What kind of songs are these? → Campfire songs
- folk-heroes-and-tall-tales-5: overlap like family-and-school-traditions-13: At American summer camp, kids sing “Kumbaya,” “Boom Chicka Boom” and “The Ants Go Marching” together at night. What kind of songs are these? → Campfire songs: On the Sea Islands of South Carolina and Georgia, descendants of enslaved West Africans kept their own creole language and folktales. What is this culture called? → Gullah
- folk-heroes-and-tall-tales-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Br'er Bear, Br'er Fox and Br'er Rabbit share a title from Southern folktales. “Br'er” is short for which word? → Brother
- home-cooking-9: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: It's cream cheese mixed with cheddar, shaped into a ball, and served with crackers at holiday parties. What is it usually rolled in? → Chopped nuts
- inventors-and-founders-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: A statue of Nikola Tesla stands near these falls, where his AC power system ran a giant power plant starting in 1895. Which falls are these? → Niagara Falls
- national-parks-15: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: I'm a cave chamber so huge that about six football fields could fit on my floor. I'm the star of Carlsbad Caverns in New Mexico. What am I called? → The Big Room
- native-nations-11: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: The state of Utah takes its name from which Native people? → The Ute
- nineteenth-century-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Buffalo Bill Cody toured the US and Europe with cowboys, sharpshooter Annie Oakley and trick riders. What was his famous show called? → Buffalo Bill's Wild West
- rivers-lakes-and-mountains-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I'm born near Leadville, Colorado, I carve the Royal Gorge, and I pass Wichita and Tulsa before joining the Mississippi. What river am I? → Arkansas River
- states-and-capitals-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This is Utah. What is the huge lake in the state's north? → Great Salt Lake
- twentieth-century-9: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: This basketball team plays for laughs and spins balls on its fingers to the tune “Sweet Georgia Brown.” What is it called? → The Harlem Globetrotters
- weather-and-seasons-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This 1942 song dreams of snow on December 25. Bing Crosby sang it, and Guinness calls it the best-selling single of all time. What is it? → “White Christmas”
- roads-and-landmarks-1: overlap like plants-and-trees-13: This mossy forest gets about 12 feet (3.7 m) of rain a year, one of the wettest places in the lower 48 states. In which state is it? → Washington: This mossy forest is close to Forks, Washington, the rainy little town where “Twilight” is set. Which national park is it in? → Olympic National Park
- states-and-capitals-3: overlap like q-8928: This giant stone face of Abraham Lincoln is carved into a mountain. Which famous place is it? → Mount Rushmore: The dot on this map of South Dakota marks a mountain with the giant faces of four presidents carved into it. What is it called? → Mount Rushmore
- states-and-capitals-6: overlap like q-0205: ¿Qué tipo de árbol es el más alto del mundo? → La secuoya roja: They grow on California's foggy coast, can live over 2,000 years, and some are over 360 feet (110 m) tall. What are these tallest living things on Earth? → Coast redwoods
- states-and-capitals-7: overlap like q-4764: What is this famous room in the White House called? → Oval Office: It's the most famous office in America. The US president works there, inside the White House, and it's named after its shape. What is it called? → The Oval Office
- trailblazers-1: overlap like q-0752: El médico Ronald Ross descubrió que la malaria la transmite el insecto que hace este sonido. Escucha: ¿cuál es? → El zancudo: In 1900, US Army doctor Walter Reed's team worked in Cuba, used volunteers, and tracked how yellow fever spread. What did they prove carries it? → Mosquitoes
- trailblazers-5: overlap like q-3245: In the Dr. Seuss story of how the Grinch stole Christmas, what is the name of the Grinch's dog? → Max: “I wrote about a cat in a tall red-and-white striped hat, and a grumpy green creature who stole Christmas.” Who am I? → Dr. Seuss
- trailblazers-17: overlap like q-6707: Pantene started in Switzerland in 1945. What kind of products is it known for? → Hair products: Madam C.J. Walker, whose story is told in the series “Self Made,” became one of America's first self-made female millionaires by selling what? → Hair care products
- twentieth-century-4: overlap like q-2357: For Communist China, ping-pong was to sports diplomacy as which animal was to animal diplomacy? → Giant panda: In 1972, Richard Nixon visited China. Soon after, China sent two animals as a gift to the National Zoo in Washington. Which animals? → Giant pandas
- twentieth-century-10: overlap like q-5848: Which world leader travels in the plane known as “Air Force One”? → The US president: “Air Force One” is a radio call sign, not one plane's name, and only Air Force planes use it. What turns one of them into “Air Force One”? → The US president being on board
- twentieth-century-12: overlap like q-5863: You ride the elevator to the top of One World Trade Center in New York. About how tall is the building? → About 540 m: It opened in Lower Manhattan in 2014, was nicknamed the “Freedom Tower,” and is 1,776 feet (541 m) tall to honor the year of US independence. What is it? → One World Trade Center
- weather-and-seasons-16: overlap like q-8739: Listen to this siren as the vehicle passes. What is this change in its sound called? → The Doppler effect: US TV weather loves radar like this. It's named after an Austrian scientist who explained why a passing siren changes pitch. Who? → Christian Doppler
