# batch-32

Made by `qgen batch` on 2026-11-05 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): cryptids-and-ufos, ghosts-and-superstitions, country-and-folk, roots-and-soul, traditional-songs, american-literature, childrens-books, comics-and-art, tv-shows, kids-tv, hosts-and-game-shows, movie-favorites, american-football, baseball, college-sports, more-sports, words-and-slang, sayings-and-idioms, place-names, money-and-shopping, school-life, household-brands, getting-around, national-symbols, state-symbols
- Merged: 307 (q-10491…q-10797)
- Approved: 281
- Needs work: 26
- Dropped by the pipeline: 60
- Reviewed by: claude-opus-5-5
- Claude calls: 640, about $75.92 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-30, batch-31; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-30 | batch-31 | batch-32 |
|---|---|---:|---:|---:|
| source locale |  | es-ES (first es-ES batch) | es | en |
| drafts |  | 375 | 427 | 367 |
| skipped slots |  | 111 | 95 | 83 |
| dropped |  | 63 | 85 | 60 |
| drop rate | ≤ 20.0 % | 16.8 % ✓ | 19.9 % ✓ | 16.3 % ✓ |
| dropped: hard fail correct |  | 1 | 2 | 1 |
| dropped: hard fail unambiguous |  | 0 | 3 | 0 |
| dropped: hard fail no_giveaway |  | 22 | 23 | 17 |
| dropped: overlap |  | 40 | 55 | 41 |
| dropped: duplicate |  | 0 | 1 | 0 |
| dropped: fact-check wrong |  | 0 | 1 | 1 |
| merged |  | 312 | 342 | 307 |
| approved |  | 290 | 318 | 281 |
| needs_work |  | 22 | 24 | 26 |
| needs_work rate | ≤ 20.0 % | 7.1 % ✓ | 7.0 % ✓ | 8.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.8 % ✓ | 2.0 % ✓ | 2.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.6 % ✓ | 0.9 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 2.6 % ✓ | 4.1 % ✓ | 5.5 % ✓ |
| media: no pick in review 1 |  | 64 | 63 | 38 |
| media: recovered by research |  | 57 | 53 | 25 |
| media: no pick at record |  | 8 | 11 | 14 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 11.5 % ✓ | 13.1 % ✓ | 11.4 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 64.0 % ✓ | 69.4 % ✓ | 71.3 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.12 ✓ | 1.56 ✗ | 2.29 ✗ |
| approved 11–15 |  | 54 | 61 | 59 |
| top move | ≤ 25.0 % | 21.2 % ✓ | 16.7 % ✓ | 19.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 77.6 % | 80.4 % | 84.4 % |
| values stimulus |  | 5 | 4 | 6 |
| top clue | ≤ 60.0 % | 47.1 % ✓ | 43.0 % ✓ | 45.0 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 27.6 % ✓ | 27.8 % ✓ | 24.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 22.1 % ✓ | 17.0 % ✓ | 21.8 % ✓ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 22.4 % ✓ | 19.6 % ✓ | 15.6 % ✓ |
| mean fun | ≥ 3.40 | 3.54 ✓ | 3.50 ✓ | 3.56 ✓ |
| cost $ |  | $79.45 | $86.59 | $73.13 |
| $ per approved | ≤ $0.35 | $0.27 ✓ | $0.27 ✓ | $0.26 ✓ |
| calls |  | 592 | 642 | 580 |
| calls per approved |  | 2.04 | 2.02 | 2.06 |
| wall time h |  | 2.43 | 2.98 | 2.60 |
| days |  | 8 | 1 | n/a |
| **health** | | ✓ pass | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 3 of 5 (60 %)
- Problems by kind: giveaway 6 (0 major), overlap 1 (1 major), media 3 (2 major), difficulty 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.78

Major findings on approved questions:

None.

## Needs work

- **q-10505** (american-literature) In the famous Dr. Seuss book, who keeps asking someone to try a dish like this one, “here or there”? → Sam-I-Am: None of the four candidates shows a plate of green eggs and ham, and this picture is essential to the question. Candidate 1 also shows Cat in the Hat hats, which points to a wrong option. A new search is needed, for example "green scrambled eggs ham", but searching again isn't allowed in this run. No suitable picture found for this question.
- **q-10507** (american-literature) In “The Wonderful Wizard of Oz,” which girl follows a road like this one to find the Wizard? → Dorothy: No candidate shows a clear yellow brick road: 1 and 2 are a Tel Aviv hostage memorial installation (yellow plaques with Hebrew handwriting on gravel), which isn't a brick road and brings in a sad context; 3 and 4 are grass and dirt paths. The essential image needs a new search, for example "yellow brick road" or "yellow paved path". Another option is to make the image illustrative or remove the "like this one" wording. No suitable picture found for this question.
- **q-10514** (baseball) This is the 1919 Chicago White Sox. After the “Black Sox” scandal over a fixed World Series, how many of its players were banned for life? → 8: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-10545** (comics-and-art) This boy starred in a giant, colorful Sunday newspaper strip starting in 1905, and each week ended with him waking up in bed. Who is he? → Little Nemo: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-10559** (country-and-folk) Whitney Houston made “I Will Always Love You” a huge hit in 1992, but this country singer wrote and sang it first, in 1974. Who is she? → Dolly Parton: The media slot is set up wrong. It is marked essential, and its note asks for a portrait of Dolly Parton. The question never refers to a photo, so a sharp picture of her face would just show the answer. Change the slot to illustrative (for example a vintage stage microphone), and choose candidate 4 or 6, the plain microphone shots. As the slot stands, no candidate fits, and no new search is allowed. No suitable picture found for this question.
- **q-10561** (country-and-folk) Listen: which instrument is this? → Banjo: All six audio candidates are 3–4 second MIDI files of banjo roll patterns from Wikipedia, not recordings. How they sound depends on the synthesizer, so they may not sound like a real banjo, or may even sound like a guitar or harp. That doesn't work for an essential "Listen: which instrument is this?" question. A real solo banjo recording is needed, for example from Freesound with a search like "banjo solo". New searches are used up for this slot. The text itself is fine. No suitable picture found for this question.
- **q-10573** (getting-around) On US roads, the sign that says “YIELD” has how many corners? → 3: This repeats approved q-3811, which already asks how many sides the yield / give way sign has (answer 3). Asking about US roads and "corners" instead of "sides" is still the same fact, so this one should be dropped rather than reworded.
- **q-10591** (hosts-and-game-shows) You face the chasers on ABC's The Chase in 2021: Ken Jennings, James Holzhauer and Brad Rutter. What are they all famous for? → Jeopardy! champions: This is a new draft that asks what three named people have in common ("What are they all famous for?"). The developer rule of 2026-10-21 bans that style for new drafts. If the topic is kept, it needs a different question, for example one about a single chaser, or about which show the 2021 ABC chasers came from, asked about a fact rather than a shared trait.
- **q-10605** (kids-tv) A pirate captain shouts “Are you ready, kids?”, the kids answer “Aye aye, Captain!”, and the song begins. Which cartoon does it open? → SpongeBob SquarePants: The media gives the answer away. Every candidate is an underwater coral-reef scene, and SpongeBob is the only one of the four options set under the sea, so even a blurred reef image points to it. A new search can't be run, so the slot needs a neutral decorative image, such as a pirate ship, a pirate hat or an old TV set. No suitable picture found for this question.
- **q-10611** (money-and-shopping) At a supermarket counter, you take a number, ask for “half a pound, sliced thin,” and watch it go through a spinning blade. What do people mostly buy there? → Lunch meats and cheese: None of the media candidates fits. They show a sacrament dispenser, coffee-bean bins (2 and 3), a pharmacy pill bag, a 1901 greenhouse plate and a handwritten letter. None shows a take-a-number dispenser or a supermarket counter, and no new search is allowed. The slot needs a new search, for example "deli ticket dispenser" or "meat slicer" (but no deli sign in the picture), or a decorative "supermarket aisle" image. No suitable picture found for this question.
- **q-10615** (money-and-shopping) Every US paper bill carries these words. What kind of institution is the Federal Reserve? → The country's central bank: No candidate clearly shows the words “Federal Reserve Note”, which the essential image must show because the question says “these words”. Candidate 1 crops the text to “…DERAL RESE…”, and candidate 2 mixes the dollars with Belarusian notes, with the text too small to read. 3 and 4 are stacks of cash, and 5 and 6 are not family-friendly. No new search is allowed, so the question needs a properly chosen image, for example a full US $1 bill with “FEDERAL RESERVE NOTE” readable at the top. No suitable picture found for this question.
- **q-10636** (national-symbols) Lady Liberty's crown has seven rays. Finish the phrase: they stand for the seven seas and the seven… → continents: Hint 2 ("Each one is much bigger than any country") is false. Russia (about 17 million km²) is bigger than Australia and also bigger than Antarctica. Replace it with a true hint, for example "Africa and Europe are two of them." The answer, the other hints and the fun fact are fine. Fact check: wrong. Hint 2, 'Each one is much bigger than any country', is false. Russia (about 17M km²) is bigger than Australia (about 7.7M km²) and also bigger than Antarctica (about 14M km²). The answer and the 162 steps are fine.
- **q-10638** (national-symbols) The US flag is often folded into a triangle like this one. What is the shape said to recall? → A three-cornered hat: None of the candidates shows a US flag folded into a triangle, which this essential image needs ("like this one"), and no new search is allowed. The slot needs a photo of a folded US flag (for example "folded American flag" or "flag folding ceremony"). The question text itself is fine. No suitable picture found for this question.
- **q-10642** (national-symbols) Which famous American bell has this shape, crack and all? → The Liberty Bell: The question asks for a "famous American bell", but none of the three wrong answers is American (Big Ben is in London, the Tsar Bell in Moscow, the Pummerin in Vienna), so the word "American" gives the answer away. Hints 1 and 2 (Philadelphia, 1776) do the same. Either drop "American" and make the hints vaguer, or replace the wrong answers with other famous US bells.
- **q-10655** (american-football) These sideline poles, joined by a chain, show how far a team must go for a new first down. How many yards long is the chain? → 10: No candidate shows the first-down chain crew: the three are a Virginia historical marker, a 1906 nursery catalogue page of pruned trees and an old sketch of colonial explorers. The essential image needs a photo of the chain crew holding the two poles and chain on a football sideline, for example from a search for "football chain crew" or "down marker chain sideline". No suitable picture found for this question.
- **q-10664** (words-and-slang) It has a cab in front and an open bed in back, and the first factory-built one rolled out in 1925. In which country was the pickup truck born? → The United States: Hint 2 ("in the Americas, but not in South America") rules out Germany, Japan and Brazil at once, so it gives the answer away before hint 3. Replace it with a vaguer hint, e.g. about the carmaker being famous for its early assembly line, without naming the country or its continent.
- **q-10667** (childrens-books) In “The Story of Ferdinand”, Ferdinand is a bull who would rather sit under a cork tree smelling flowers than fight. In which country does he live? → Spain: The text is fine, but no media candidate works: 1–3 are pit bull dogs, 4 is an American bison, 5 is an elk skull and 6 is an old group photo of press people. No new search is allowed. The slot needs a photo of a domestic bull resting in a meadow, or of flowers under a cork oak (search "bull meadow flowers" or "Quercus suber"). No suitable picture found for this question.
- **q-10674** (country-and-folk) This close-up shows a shiny pearly snap on a shirt. What kind of shirt is it usually found on? → Western shirt: No candidate shows what the essential image needs: a pearly snap on a shirt. The sheet has a portrait (1), a medieval painting (2), plain metal snaps on leather or a nylon jacket (3, 5, 6) and snap jewelry (4). Another search isn't allowed, so the slot needs a hand-picked close-up of a pearl snap on a Western shirt (e.g. a search for "pearl snap button shirt"). No suitable picture found for this question.
- **q-10739** (sayings-and-idioms) I pushed the pistons of old trains and Mississippi riverboats. To go top speed, captains called for “full” me “ahead.” What am I? → Steam: Hint 2 (“Coal was burned to make me.”) gives the answer away: it rules out Coal, and neither wind nor diesel is made by burning coal, so only Steam is left. Replace it with a vaguer hint that doesn't eliminate options, for example one about what the captain's command meant.
- **q-10749** (school-life) In American schools, what is “construction paper”? → Thick colored paper for crafts: The description gives the answer away. With only the four options to go on, "safety scissors are strongly recommended" points straight to young kids cutting paper for crafts, which is the answer's defining trait. It also uses the same clue as hint 2. The description should play on the construction/school theme without hinting at cutting or kids' crafts.
- **q-10753** (school-life) This American girl could neither see nor hear. Her world opened up when her teacher spelled “water” into her hand. Who is she? → Helen Keller: The description, “A girl who learned the whole world through the palm of her hand”, gives away Helen Keller's defining trait (learning through words spelled into her hand). With only the four options showing, it rules out Earhart, Parks and Barton straight away. Rewrite it to play on school or learning without naming that trait.
- **q-10754** (school-life) In the US, stores fill with new backpacks, pencils and binders for “back-to-school” sales. When does this happen? → Late summer: No candidate shows school supplies or a back-to-school display; all are generic grocery or warehouse aisles (bread, oil, baking, desserts, a Tesco aisle with £ prices). A new search such as "school supplies display" or "backpacks pencils binders" is needed. No suitable picture found for this question.
- **q-10755** (state-symbols) This state's motto is “Sic semper tyrannis”. Which state is it? → Virginia: The media slot is set to essential, and its note asks for a blank outline of Virginia, but the search was for "Latin inscription carved stone". All six candidates are old Latin inscriptions from Europe and Libya, so none shows the outline, and a new search isn't allowed. The question doesn't refer to any picture, so the slot should become an illustrative or decorative image (for example a Latin inscription or a colonial courthouse). The question can't actually use an outline of the state either, since that would let players answer from the map shape without knowing the motto. No suitable picture found for this question.
- **q-10763** (state-symbols) People from this state are called Hoosiers. Which state is it? → Indiana: The media slot is set up wrong. It is marked essential and its note asks for a blank outline of Indiana, but the question never refers to a picture, and an outline of the state would give the answer away anyway. None of the candidates is an Indiana outline, and no new search is allowed, so the slot should become illustrative or decorative (a Midwest barn in a cornfield, like candidate 1, would fit). Separately, hint 3 (“Its capital is Indianapolis.”) contains the answer word “Indiana”. The rules don't allow that even in the third hint, so swap it for another strong clue, such as the state's rival-free basketball fame or its spot between Ohio and Illinois. No suitable picture found for this question.
- **q-10773** (traditional-songs) George M. Cohan wrote “Over There” in 1917. It tells Johnnie to get his gun, and warns that “the Yanks are coming.” Where was “over there”? → Europe: The picked picture has an unsuitable licence (pd-us-only: PD-US-not renewed).
- **q-10791** (words-and-slang) I'm the American region where “hella”, meaning “very”, became everyday talk decades ago. My rappers spread it nationwide. What am I? → The San Francisco Bay Area: Hint 1 (“I'm on the West Coast.”) rules out all three wrong answers at once: Boston, New Orleans and the Texas Hill Country are not on the West Coast. Hint 2 (“Oakland is one of my cities.”) also gives the answer away directly. Hint 1 should be a vague clue that leaves several options open (for example about the era or the music scene). Hint 2 should not name a Bay Area city. One option would be to name the rappers' style without naming a place.

## Question axes

- move: analogy 5, cause_effect 15, count 12, estimate 5, identify 60, made_of 9, name_concept 31, odd_one_out 20, origin 31, purpose 9, record 4, sequence 15, when 18, who 47, word_meaning 26
- stimulus: detail 9, map_outline 3, none 259, photo 34, silhouette 1, sound 1
- clue: completion 10, direct 138, riddle 41, scenario 30, three_facts 88
- answer_kind: group 23, number 18, person 73, place 40, thing 60, time 18, word 75
- lens: body_senses 17, educational_media 17, everyday 48, history 64, language 49, nature 6, pop_culture 67, popular_science 4, school 32, university 3

## Dropped by the pipeline

- american-football-9: overlap like q-2871: It's round, it has a see-through front, and astronauts wear it on their heads. What is it? → A helmet: It's hard on the outside and padded inside, it often shows the team logo, and football players wear it on their heads. What is it? → A helmet
- american-football-14: overlap like q-3703: Kendrick Lamar, who headlined the 2025 Super Bowl halftime show, grew up in which city? → Compton: In the middle of the Super Bowl, a superstar sings and dances on the field while the teams rest. What is this show called? → The halftime show
- american-literature-2: overlap like q-4522: Look at this huge skull with teeth as big as bananas. Which dinosaur did it belong to? → Tyrannosaurus rex: In “Jurassic Park,” this huge dinosaur breaks free when the electric fences stop working. What is it called? → Tyrannosaurus rex
- american-literature-6: overlap like q-4614: Katniss Everdeen's home district in “The Hunger Games” digs this out of the ground. Which district is she from? → District 12: I'm the poorest part of Panem, known for coal mining, and both Katniss and Peeta come from me. Which am I? → District 12
- american-literature-11: overlap like q-4470: The writer in this photo created Macondo, inspired by an invented county in Mississippi. Which American Nobel winner invented that county? → William Faulkner: This American Nobel winner wrote “The Sound and the Fury” and “As I Lay Dying.” Who is he? → William Faulkner
- american-literature-12: overlap like q-3246: I'm a spider who writes words like “Some Pig” in my web to save my friend Wilbur. Who wrote my story? → E. B. White: In a famous American novel, the words “Some Pig” appear woven into a web like this one. Who wrote that book? → E. B. White
- baseball-6: overlap like q-2384: This player is batting in baseball. How many strikes put the batter out? → 3: The batter misses three times, the umpire yells “Strike three!” and the batter is out. It's how the poem “Casey at the Bat” ends. What is it called? → A strikeout
- baseball-8: overlap like q-5420: This baseball player crouches behind home plate in a mask and signals to the pitcher. Which position? → Catcher: This big, round, padded glove is called a mitt. Which baseball player wears it? → The catcher
- comics-and-art-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: I fly at night, sleep hanging upside down, and a famous superhero from Gotham City dresses up like me. What am I? → A bat
- comics-and-art-9: overlap like q-10129: «El Reina Sofía» está en Madrid, junto a la estación de Atocha, y lleva el nombre de la madre del rey Felipe VI. ¿Qué es? → Un museo de arte: In New York, “the Met” sits on Fifth Avenue next to Central Park, holds a real Egyptian temple, and hosts a famous yearly fashion gala. What is it? → An art museum
- comics-and-art-14: overlap like q-0437: En los dibujos animados, ¿qué come Popeye el marino para volverse superfuerte? → Espinacas: Finish Popeye's famous song: “I'm strong to the finish 'cause I eats me…” → Spinach
- comics-and-art-16: overlap like q-5860: Norman Rockwell painted the “Four Freedoms” from a speech by Franklin D. Roosevelt. In which year was that speech? → 1941: In 1941, President Franklin D. Roosevelt named four freedoms: freedom of speech, of worship, from want, and freedom from what? → Fear
- country-and-folk-9: overlap like q-4326: You're streaming a song marked “(Taylor's Version)”. Why did Taylor Swift record her old albums all over again? → To own the master recordings: Taylor Swift re-recorded old albums like “Fearless” and “Red” so she would own them. What did she add to their new titles? → Taylor's Version
- cryptids-and-ufos-0: overlap like q-8985: A substance found in the spit of this Arizona desert lizard led to a medicine. Which patients does it help? → People with diabetes: You're walking through a museum of American cryptids, creatures science has never proven. Which exhibit does NOT belong, because the animal is real? → The Gila monster
- cryptids-and-ufos-2: overlap like q-3364: In a film, a girl in Hawaii says “Ohana means family” about her blue pet Stitch. What kind of creature is Stitch? → An alien: I'm small, blue and fluffy, with big ears. I crash-landed in Hawaii, and a girl named Lilo adopted me as her dog. Who am I? → Stitch
- cryptids-and-ufos-4: overlap like q-1279: ¿En qué estado de Estados Unidos queda el Área 51? → Nevada: State Route 375 was officially named the “Extraterrestrial Highway” in 1996. It runs past the tiny town of Rachel and near a secret Air Force base. In which state is it? → Nevada
- cryptids-and-ufos-10: overlap like q-5961: I'm round and flat like a dinner plate, I spin and zoom through the sky, and cartoon aliens fly me. What am I? → A flying saucer: In 1947, a pilot saw shiny objects near Mount Rainier and said they moved like a plate skipping across water. Newspapers gave them a name. What was it? → Flying saucer
- cryptids-and-ufos-12: overlap like q-3668: Stories of the hairy forest giant Sasquatch, also known as Bigfoot, come from which part of the world? → North America: I'm huge, hairy and shy, I leave giant footprints in the forests of the Pacific Northwest, and this name of mine comes from a Native language there. Which name am I? → Sasquatch
- getting-around-8: overlap like q-4196: In most countries these road signs are triangles with a red edge, and they show things like a sharp bend, a deer or children ahead. What kind of signs are they? → Warning signs: Complete the rule US student drivers learn: a yellow, diamond-shaped road sign is a… → Warning sign
- getting-around-9: overlap like q-7760: Me paras con la mano en la calle, me dices la dirección y al llegar te cobro la carrera. Mi carro casi siempre es amarillo. ¿Quién soy? → El taxista: “I'm a bright yellow car, I drive people around New York City for money, and you wave your arm to stop me.” What am I? → A taxi
- ghosts-and-superstitions-7: overlap like q-1303: El «metraje encontrado» finge ser una grabación real hallada después. ¿Cuál de estas películas NO es de ese estilo? → El conjuro: “Paranormal Activity” looks like real home-video recordings left behind by its characters. What is this style of film called? → Found footage
- ghosts-and-superstitions-15: overlap like q-5963: I'm the brainy Ghostbuster with glasses and tall hair, and I designed the proton packs. Who am I? → Egon Spengler: They wear jumpsuits and proton packs, drive a car called Ecto-1 and catch spooky creatures in traps in New York. What are they called? → Ghostbusters
- household-brands-9: overlap like q-0781: La Super Soaker es la famosa pistola de agua que se bombea con la mano. ¿En qué década salió a la venta? → En los años 90: I'm a big plastic toy you pump full of air. Pull my trigger and I blast water clear across the yard in a summer fight. What am I called? → Super Soaker
- kids-tv-0: overlap like q-3160: “I'm Dora the Explorer's best friend, and I'm named after the red things I wear on my feet.” What kind of animal am I? → A monkey: On Nick Jr., who goes on adventures with a monkey named Boots and a talking Backpack? → Dora
- kids-tv-5: overlap like q-4338: I'm an evil scientist, my company's name ends in “Evil Incorporated”, and I always shout “Curse you, Perry the Platypus!”. Who am I? → Dr. Doofenshmirtz: Finish Dr. Doofenshmirtz's famous angry cry from Phineas and Ferb: “Curse you, ___ the Platypus!” → Perry
- kids-tv-6: overlap like q-5763: In Disney's “Descendants”, the heroes are the children of famous villains. Which villain is the mother of the main heroine? → Maleficent: In Disney's Descendants, Maleficent is to Mal as the Evil Queen is to… → Evie
- kids-tv-13: overlap like q-4203: SpongeBob shouts “I'm ready!” on his way to work. A painter is to a brush as SpongeBob is to a… → Spatula: SpongeBob jumps out of bed for work and shouts, over and over: “I'm …!” What's the missing word? → Ready
- kids-tv-15: overlap like q-2722: What super tall snack do Scooby-Doo and Shaggy love to make? → Sandwiches: I've been shouting “Zoinks!” since 1969, I'm always hungry, and my best buddy is a scared Great Dane. Who am I? → Shaggy
- movie-favorites-0: overlap like q-3618: In which year did “Toy Story”, the first feature film made fully with computer animation, first come out in cinemas? → 1995: You're watching the first full-length movie ever made entirely with computer animation. Which movie is it? → Toy Story
- movie-favorites-9: overlap like q-3617: When Elastigirl hides her powers and lives a normal family life, what is her everyday name? → Helen Parr: I'm a superhero mom. I can stretch my arms across a room and even turn myself into a parachute. My husband is Mr. Incredible. Who am I? → Elastigirl
- movie-favorites-10: overlap like q-8856: In the animated film Zootopia, why does a trip to the DMV take forever? → It's run by sloths: In “Zootopia,” Flash works at the DMV, where getting anything done takes forever. He's the world's slowest mammal. What animal is he? → Sloth
- movie-favorites-12: overlap like q-10562: In the 1982 movie “E.T. the Extra-Terrestrial”, the little alien famously says: “E.T. phone…” what? → Home: In which decade did the alien first say “E.T. phone home” in movie theaters? → 1980s
- movie-favorites-13: overlap like q-2261: In the 2021 film “Space Jam: A New Legacy”, a basketball star teams up with which cartoon gang? → The Looney Tunes: I'm an NBA star. In 2021, my son and I got pulled into a world of cartoons, and I played basketball with Bugs Bunny to get home. Who am I? → LeBron James
- movie-favorites-14: overlap like q-3159: In the film Up, Carl and Russell meet Kevin, the giant colorful bird, on their way to which waterfall? → Paradise Falls: In “Up,” Carl ties thousands of balloons to his house. Where is he trying to fly it? → Paradise Falls
- national-symbols-1: overlap like q-6243: Which big animal is this, seen roaming in Yellowstone National Park? → A bison: I can weigh about 2,000 pounds, my Yellowstone herd has lived there since prehistoric times, and since 2016 I'm the US national mammal. What am I? → The American bison
- national-symbols-11: overlap like q-10636: Lady Liberty's crown has seven rays. Finish the phrase: they stand for the seven seas and the seven… → continents: A famous lady holds this torch high in the sky. Who is she? → Lady Liberty
- childrens-books-15: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Cam Jansen remembers everything she sees. She blinks, says “Click!”, and the picture is saved. Her nickname is short for what? → Camera
- comics-and-art-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: From 1968, this building on New York's Union Square housed The Factory, a famous art studio. Which artist ran it? → Andy Warhol
- country-and-folk-11: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: In which country dance does everyone stand in rows and do the same steps at the same time, with no partner? → Line dance
- country-and-folk-15: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: Kenny Chesney's fans wear flip-flops to hear him sing about beaches. In which state did he grow up? → Tennessee
- cryptids-and-ufos-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Bigfoot hunters love the word, skeptics laugh at it, and it fills cryptid websites. What is a “blobsquatch”? → A blurry photo of a dark shape said to be Bigfoot
- getting-around-5: fact-check wrong: Hint 'one of them is a country' is inaccurate: 'America' is not a country's name (the country is the United States). The facts are otherwise right: Amtrak began in 1971, Acela runs Boston–Washington, and the Auto Train runs Lorton, VA to Sanford, FL.: “I was born in 1971 to run passenger trains across America, and my Acela trains zip from Boston to Washington, D.C.” What am I? → Amtrak
- getting-around-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Before it was renamed in 1949, what was Chicago's O'Hare airport called? → Orchard Field
- getting-around-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: At many US schools, older students wear a bright belt across the chest and a badge, and AAA trains them. What is their job? → Help kids cross and board buses safely
- getting-around-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which US stamp can mail a first-class letter any time later, no matter how much postage prices rise? → The Forever stamp
- ghosts-and-superstitions-3: overlap like q-10600: At the end of a Scooby-Doo mystery, the villain's mask comes off. Who does the villain usually blame? → Those meddling kids: In Scooby-Doo, the scary ghost is almost always a person in a mask. Why does the bad guy usually dress up like that? → To scare people away
- hosts-and-game-shows-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: On The Price Is Right, you shout out guesses for an item's exact price while the host only says “higher” or “lower.” Which game is it? → Clock Game
- more-sports-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Carli Lloyd scored three goals in the 2015 Women's World Cup final. Where on the field did she take her last shot from? → Near the halfway line
- more-sports-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Dick Fosbury was from Oregon, won Olympic gold in 1968, and went over the high-jump bar backwards. What change made landing on his back safe? → Raised foam landing mats
- national-symbols-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I'm a stern blue Muppet with a big frown, and I think the other Muppets' acts are far too silly. Who am I? → Sam the Eagle
- national-symbols-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: The date on the Statue of Liberty's tablet isn't written with everyday digits. What kind of numbers are used? → Roman numerals
- roots-and-soul-8: hard fail: correct 3, unambiguous 5, no_giveaway 5, no_overlap 5: Rapper and actress Queen Latifah, the voice of Ellie the mammoth in “Ice Age,” grew up in which US state? → New Jersey
- sayings-and-idioms-7: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: It sounds just like a greeting, and when you shout “Hey!”, a grown-up may say it's “for horses.” What is it? → Hay
- school-life-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: US high school sports teams, cheer squads and school plays all hold them, and a list is posted afterward. What are “tryouts”? → Tests to join a team or cast
- state-symbols-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ohio is to Ohioan as Alaska is to… → Alaskan
- roots-and-soul-4: overlap like q-10559: Whitney Houston made “I Will Always Love You” a huge hit in 1992, but this country singer wrote and sang it first, in 1974. Who is she? → Dolly Parton: You're at karaoke and someone tries the huge “And I will always love you” high note. Who made that version a giant hit in 1992? → Whitney Houston
- roots-and-soul-12: overlap like q-8215: Me agitan antes de usarme, suelto pintura de colores y los grafiteros me usan en los muros de Bogotá. ¿Qué soy? → Un aerosol: Listen: this sound is often heard where graffiti is being painted. What makes it? → A spray paint can
- school-life-6: overlap like q-6145: Cheerleaders shake pom-poms like these at games. What are they usually made of today? → Thin plastic strips: Riddle: “I wear my school's colors, stand by the field at football games and shake two fluffy bunches of shiny strips.” Who am I? → A cheerleader
- tv-shows-8: overlap like q-2978: Leonard Nimoy, who played Spock, based this Star Trek greeting on a blessing he saw as a boy. Who gives that blessing? → Jewish priests: You raise your hand in Mr. Spock's famous Vulcan salute. How many fingers do you keep pressed together on each side of the gap? → 2
- tv-shows-12: overlap like q-10526: Which author won five Newbery Honors for books about her own childhood, but never won the Newbery Medal itself? → Laura Ingalls Wilder: Little House on the Prairie, the 1970s TV series about a pioneer family, was based on books written by whom? → Laura Ingalls Wilder
