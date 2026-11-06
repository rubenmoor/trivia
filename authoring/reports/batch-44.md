# batch-44

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): roots-and-soul, school-life, national-parks, hosts-and-game-shows, money-and-shopping, winter-holidays, folk-heroes-and-tall-tales, cryptids-and-ufos, home-cooking, country-and-folk, words-and-slang, inventors-and-founders, sayings-and-idioms, childrens-books, comics-and-art, getting-around, place-names, ghosts-and-superstitions, trailblazers, tv-shows, desserts-and-baking, baseball, plants-and-trees, weather-and-seasons, state-symbols
- Merged: 244 (q-13719…q-13962)
- Approved: 221
- Needs work: 23
- Dropped by the pipeline: 61
- Reviewed by: claude-opus-5-5
- Claude calls: 540, about $68.28 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-42, batch-43; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-42 | batch-43 | batch-44 |
|---|---|---:|---:|---:|
| source locale |  | es-ES | es | en |
| drafts |  | 342 | 343 | 305 |
| skipped slots |  | 144 | 179 | 145 |
| dropped |  | 78 | 100 | 61 |
| drop rate | ≤ 20.0 % | 22.8 % ✗ | 29.2 % ✗ | 20.0 % ✓ |
| dropped: hard fail correct |  | 5 | 0 | 1 |
| dropped: hard fail unambiguous |  | 0 | 2 | 2 |
| dropped: hard fail no_giveaway |  | 17 | 25 | 17 |
| dropped: overlap |  | 54 | 73 | 43 |
| dropped: duplicate |  | 2 | 1 | 0 |
| dropped: fact-check wrong |  | 1 | 0 | 0 |
| merged |  | 264 | 243 | 244 |
| approved |  | 238 | 224 | 221 |
| needs_work |  | 26 | 19 | 23 |
| needs_work rate | ≤ 20.0 % | 9.8 % ✓ | 7.8 % ✓ | 9.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.8 % ✓ | 2.5 % ✓ | 0.4 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.8 % ✓ | 0.8 % ✓ | 0.8 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.5 % ✗ | 0.4 % ✓ | 0.4 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.5 % ✓ | 4.5 % ✓ | 7.4 % ✓ |
| media: no pick in review 1 |  | 34 | 43 | 26 |
| media: recovered by research |  | 23 | 34 | 17 |
| media: no pick at record |  | 11 | 9 | 9 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 17.5 % ✓ | 21.9 % ✗ | 14.4 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 58.3 % ✓ | 53.0 % ✗ | 59.8 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.00 ✓ | 2.67 ✗ |
| approved 11–15 |  | 54 | 52 | 44 |
| top move | ≤ 25.0 % | 18.9 % ✓ | 19.8 % ✓ | 13.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 72.7 % | 68.7 % | 85.2 % |
| values stimulus |  | 6 | 6 | 5 |
| top clue | ≤ 60.0 % | 50.4 % ✓ | 49.4 % ✓ | 39.3 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 20.5 % ✓ | 22.6 % ✓ | 26.6 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 19.3 % ✓ | 19.3 % ✓ | 20.9 % ✓ |
| values lens |  | 11 | 11 | 11 |
| media share | 15.0 %–50.0 % | 27.3 % ✓ | 31.3 % ✓ | 14.8 % ✗ |
| mean fun | ≥ 3.40 | 3.45 ✓ | 3.50 ✓ | 3.54 ✓ |
| cost $ |  | $74.70 | $71.96 | $65.01 |
| $ per approved | ≤ $0.35 | $0.31 ✓ | $0.32 ✓ | $0.29 ✓ |
| calls |  | 513 | 489 | 480 |
| calls per approved |  | 2.16 | 2.18 | 2.17 |
| wall time h |  | 2.05 | 2.10 | 1.79 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 54 (4 %)
- Major among review needs work: 3 of 6 (50 %)
- Problems by kind: giveaway 7 (1 major), fact 2 (1 major), ambiguity 1 (1 major), media 6 (4 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 55 of 60 (92 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.27

Major findings on approved questions:

- **q-13743**: media — The facts check out: Flatt & Scruggs played “The Ballad of Jed Clampett” (Jerry Scoggins sang it), both men were in Monroe's Blue Grass Boys, and “Foggy Mountain Breakdown” was used in “Bonnie and Clyde.” The problem is the media. It is set as essential, but the question doesn't need a picture, and the file chosen, “Earl Scruggs and Lester Flatt.jpg”, is a photo of the answer itself. Its title names the answer outright, so it should be an illustrative image that doesn't show them, such as a banjo or a Beverly Hills scene. (http://127.0.0.1:8001/review/q-13743)
- **q-13866**: fact, ambiguity, giveaway — The question says game shows like The Price Is Right "compete" for the Daytime Emmy, but in August 2022 the two TV academies moved the game show categories to the Primetime Emmys, starting in 2023 (Deadline, CBS News, Wikipedia's "Primetime Emmy Award for Outstanding Game Show"). So in the present tense, the distractor "The Primetime Emmy Award" is the correct answer for the game-show half of the question. Smaller issue: hint 2 (the Emmy statuette) rules out the Peabody and the Golden Globe, leaving only the two Emmys, which is a minor narrowing. The fun fact (Bob Barker's 19 Daytime Emmys) is fine. (http://127.0.0.1:8001/review/q-13866)

## Needs work

- **q-13731** (childrens-books) In Cynthia Rylant's easy readers, lonely old Mr. Putter goes to adopt a pet. What does he bring home? → An old cat: The description (“the best friends come with a teapot and very little noise”) rules out options before any hint: “very little noise” excludes the talking parrot and the young puppy, and it states the answer's defining trait (a quiet, calm companion). Rewrite it to play on the theme, for example tea or Mr. Putter's routines, without saying the pet is quiet or calm.
- **q-13744** (country-and-folk) Listen: this tall instrument thumps out the beat in bluegrass bands and old rockabilly songs. Which one is it? → The upright bass: None of the audio candidates is a solo upright bass: #1 is a tango MIDI file, #2 is a Kevin MacLeod march, #3 is a song draft. The question's essential audio needs a clear recording of a plucked double bass, and no new search is allowed here. The text itself is fine. No suitable picture found for this question.
- **q-13745** (country-and-folk) Fringed suede jackets, like the ones American frontiersmen wore, became a big hippie fashion favorite in which decade? → The 1960s: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-13751** (country-and-folk) This Canadian singer wrote “Big Yellow Taxi” and “Both Sides, Now” and became a folk star in 1960s America. Who is she? → Joni Mitchell: None of the six candidates shows Joni Mitchell, and a new search isn't allowed. Also, the question asks only about her songs, so a photo isn't really needed to answer it. Switch the slot to an illustrative image, like an acoustic guitar or a 1960s folk club scene, or to a decorative one, and search again. No suitable picture found for this question.
- **q-13753** (country-and-folk) Which of these US states has NOT made the bolo tie its official state neckwear? → California: Fact check: wrong. The fun fact is wrong about New Mexico. New Mexico named the bolo tie its official state tie in 1987, not 2007. Arizona (1971) and Texas (2007) are right. I checked this from memory, not with a search.
- **q-13775** (folk-heroes-and-tall-tales) Old lumber camps like this one, where the first Paul Bunyan tales were told, filled the forests of which states? → Michigan, Wisconsin and Minnesota: No candidate shows the lumber camp the question names ("like this one"). Candidate 2 is a "Lumbering in Minnesota" sign that names part of the answer, candidate 1 is a "Canada Lumberman" masthead, and 3 and 4 are engravings of Columbia River rock formations. A new search can't run, so the slot needs a real 19th-century lumber camp photo, for example "lumber camp loggers 1890s" or "logging camp bunkhouse historic", with no state named in a caption. No suitable picture found for this question.
- **q-13776** (folk-heroes-and-tall-tales) This actor starred in the Westerns “Stagecoach” (1939) and “True Grit” (1969) and became America's ultimate cowboy hero. Who is he? → John Wayne: The picked picture has an unsuitable licence (pd-us-only: PD-US-no notice).
- **q-13777** (getting-around) Listen to this New York sound. Where are you? → On the subway: None of the audio candidates is a New York subway recording. They are train horns (#1–3), trains in Rome (#4–5) and a Sydney CityRail announcement (#6). The question needs the NYC subway door chime and the “Stand clear of the closing doors” announcement, and no new search is allowed. Find a real NYC subway recording (Freesound is the likeliest source), or drop the question. No suitable picture found for this question.
- **q-13783** (ghosts-and-superstitions) It's February 1692 in Salem Village, and the first three women are accused of witchcraft. Which one, enslaved in Reverend Parris's home, confessed? → Tituba: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-13794** (home-cooking) Which food is a round, flat patty that people flip on the grill with this tool and then put in a bun? → A burger: No candidate shows a grill spatula. The search for "turner" returned ducks of the genus Spatula, Ike & Tina Turner and J. M. W. Turner paintings. The only utensil is an 1814 silver fish slice, which doesn't look like a grill tool. The question says "this tool", so the essential image needs a clear photo of a metal grill spatula or turner. Searching again isn't allowed, so the developer needs to supply one by hand (for example from "barbecue spatula" or "metal kitchen turner"). No suitable picture found for this question.
- **q-13799** (hosts-and-game-shows) On The Tonight Show, I wore a giant turban, held a sealed envelope to my forehead, said the answer, then opened it to read the question. Who am I? → Carnac the Magnificent: The picked picture has an unsuitable licence (pd-no-reason: public domain without a template).
- **q-13820** (national-parks) This card gets a carload into every US national park for a year. Which kids can get one for free? → Fourth graders: None of the media candidates shows the America the Beautiful pass card. All six are scanned pages from old "American Annual of Photography" volumes, and no new search is allowed. The slot also doesn't need to be essential: an illustrative national-park scene, such as a family car at a park entrance sign or Old Faithful erupting, would work and is easy to find. No suitable picture found for this question.
- **q-13822** (place-names) Greenwich, a town founded in 1640 that locals say “GREN-itch,” lies in the state outlined here. Which state is it? → Connecticut: No candidate is a clean, unlabeled outline of Connecticut: #1 shows three states covered in place names, #4 and #6 print "Connecticut" in large text, and #2, #3 and #5 show other subjects. The essential map needs a new source, for example a blank outline file of Connecticut from Commons ("Connecticut blank map" or a US Census outline). No suitable picture found for this question.
- **q-13829** (place-names) In 1881, this state's lawmakers passed an official ruling on how to say the state's name. Which state is outlined here? → Arkansas: None of the six candidates shows an outline of Arkansas, and no new search is allowed, so the essential media slot can't be filled. It needs a blank Arkansas outline map, for example a Commons file of the state's outline with no labels. No suitable picture found for this question.
- **q-13833** (plants-and-trees) I grow along trails all over America. My tiny hairs make your skin burn and itch, but Native Americans twisted my stems into fishing line. What am I? → Stinging nettle: The picked picture has an unsuitable licence (pd-no-reason: public domain without a template).
- **q-13850** (folk-heroes-and-tall-tales) Old Mississippi steamboats were pushed by a big spinning part with flat boards, at the back or side. What is it called? → A paddle wheel: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-13853** (folk-heroes-and-tall-tales) An angler says the one that got away was as long as a canoe, and it gets longer each time he tells it. What do Americans call such a bragging story? → A fish story: This overlaps with draft q-13774 (“Which of these is NOT a name for a wildly exaggerated story?”, answer Cliffhanger). That question almost certainly lists “fish story” as a real name for a bragging story, and this one uses “A cliffhanger” as a wrong answer, so seeing either one gives the other away. Keep only one of the two, or change q-13774's options so they leave out “fish story”.
- **q-13890** (weather-and-seasons) I'm a farm girl from Kansas, and a twister carried me and my little dog to Oz. What is my last name? → Gale: The question is a first-person riddle (“I'm a farm girl from Kansas…”) that asks for a fact other than the speaker's identity (her last name), which house style rule 6 rules out. Rewrite it as a direct question, e.g. “In The Wizard of Oz, a twister carries Dorothy and her dog from a Kansas farm to Oz. What is her last name?”, and turn the hints from “My…” into third person (“Her Aunt Em and Uncle Henry…”).
- **q-13918** (state-symbols) The state shown on this map is nicknamed “the Bay State.” Which state is it? → Massachusetts: None of the candidates is a locator map of Massachusetts. They show the Denver skyline, a ferry off Hyannis, a geological map of the northwest US, Denver's Mile High steps and a New Bedford road. A new search isn't allowed, so this essential slot can't be filled. It needs an unlabeled locator map of Massachusetts, for example a Commons search for "Massachusetts locator map", checked for state-name labels. No suitable picture found for this question.
- **q-13924** (trailblazers) Linus Pauling won the 1954 Nobel Prize in Chemistry and the 1962 Nobel Peace Prize. What did he campaign against? → Nuclear weapons tests: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-13935** (tv-shows) In the opening credits of Laverne & Shirley, the two skip down the street chanting “Schlemiel! Schlimazel! ___ Incorporated!” What's the missing word? → Hasenpfeffer: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-13943** (winter-holidays) You're hanging one stocking for each reindeer on Santa's team, Rudolph included. How many stockings do you need? → 9: The fun fact is wrong: Rudolph was created in 1939 for a free illustrated storybook from Montgomery Ward, not a coloring booklet. The store wrote the story so it could stop buying coloring books to give away. Change the fun fact to: “Rudolph was created in 1939 for a free storybook given out by the Montgomery Ward department store.” Fact check: wrong. Fun fact is inaccurate. The 1939 Rudolph booklet was an illustrated storybook, not a coloring booklet. Montgomery Ward wrote it to replace the coloring books it used to buy and give away.
- **q-13951** (winter-holidays) In 1890, a Pasadena club started a New Year's Day parade of carriages covered in flowers. What was it meant to show the rest of the country? → California's warm winter weather: The picked picture has an unsuitable licence (pd-us-only: PD-US).

## Question axes

- move: analogy 8, cause_effect 11, count 7, estimate 4, identify 29, made_of 14, name_concept 22, odd_one_out 24, origin 21, purpose 13, record 6, sequence 5, when 18, who 29, word_meaning 33
- stimulus: detail 3, map_outline 4, none 208, photo 26, sound 3
- clue: completion 14, direct 96, riddle 22, scenario 38, three_facts 74
- answer_kind: group 20, number 11, person 42, place 29, thing 65, time 18, word 59
- lens: body_senses 2, educational_media 26, everyday 37, history 43, language 51, nature 8, pop_culture 48, popular_science 2, school 22, science_news 2, university 3

## Dropped by the pipeline

- baseball-0: overlap like q-11940: In 1941, Joe DiMaggio of the New York Yankees got a hit in game after game. How many games in a row did his streak last? → 56: I played center field for the Bronx Bombers, was nicknamed the “Yankee Clipper,” and in 1941 got a hit in 56 games in a row. Who am I? → Joe DiMaggio
- baseball-10: overlap like q-2387: Bat is to hitting as baseball glove is to… → Catching: What do baseball players use this big leather glove for? → Catching the ball
- baseball-11: overlap like q-10519: In baseball, the pitcher stands on a small hill in the middle of the field and faces the batter. What is the pitcher's job? → Throwing the ball to the batter: This player crouches behind home plate. Who throws the ball into his mitt on almost every play? → The pitcher
- childrens-books-11: overlap like q-10510: Little Ramona Quimby couldn't say her sister's name, Beatrice, so she called her “Beezus.” Which author created them? → Beverly Cleary: Who wrote the books about Ramona Quimby and her big sister, Beezus? → Beverly Cleary
- childrens-books-13: overlap like q-6039: In the film “The Polar Express”, a boy rides a magic train to the North Pole and gets the first gift of Christmas. Only true believers can hear it. What is it? → A sleigh bell: In which year did Chris Van Allsburg publish “The Polar Express”, about a night train to the North Pole? → 1985
- comics-and-art-2: overlap like q-0307: ¿Qué le pasa a quien queda atrapado en el lazo dorado de la Mujer Maravilla? → Dice la verdad: You're dressing up as superheroes: Thor brings his hammer, so Wonder Woman brings her… → Golden lasso
- comics-and-art-4: overlap like q-2599: I raised a boy from Queens and told him: “With great power comes great responsibility.” Who am I? → Uncle Ben: In the Spider-Man films, Uncle Ben tells Peter Parker: “With great power comes great…” what? → Responsibility
- comics-and-art-13: overlap like q-2597: Because Peter Parker's parents are gone, he grows up with his Aunt May. In which city do they live? → New York: Spider-Man swings between the skyscrapers of this city, his hometown. Which city is it? → New York City
- cryptids-and-ufos-17: overlap like q-5961: I'm round and flat like a dinner plate, I spin and zoom through the sky, and cartoon aliens fly me. What am I? → A flying saucer: In 1947, a US pilot named Kenneth Arnold saw shiny objects that moved like a plate skipping on water. Newspapers gave them a famous name. What was it? → Flying saucer
- desserts-and-baking-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: They came out in 1964, you warm them in a toaster, and many have frosting and sprinkles on top. What are they called? → Pop-Tarts
- desserts-and-baking-6: overlap like q-12948: On Christmas Eve, many American kids leave a snack like this one by the fireplace. Who is it meant for? → Santa Claus: On Christmas Eve, carrots are to the reindeer as cookies and milk are to… → Santa Claus
- desserts-and-baking-8: overlap like q-11866: In the first “Ghostbusters” movie, a giant marshmallow man stomps through New York. In which decade did it come out? → The 1980s: I'm soft, white and puffy. Toast me over a campfire and I go in a s'more. In “Ghostbusters,” a giant man made of me stomps through New York. What am I? → A marshmallow
- folk-heroes-and-tall-tales-5: overlap like q-9036: Babe the Blue Ox was huge, hauled logs for Paul Bunyan, and left giant footprints that filled with rain. Tall tales say they became what? → Minnesota's 10,000 lakes: I'm a giant from the North Woods. I carry a huge ax, and legend says my footprints filled with water and became Minnesota's 10,000 lakes. Who am I? → Paul Bunyan
- getting-around-8: overlap like q-5956: You give it on top of the bill, often to waiters, taxi drivers or hairdressers, to say thanks for good service. What is this money called? → A tip: In the US, it's not part of the taxi fare, it's often 15 to 20 percent of it, and in a ride app you add it after the trip. What is it? → A tip
- ghosts-and-superstitions-5: overlap like q-3107: You find a US penny with Abraham Lincoln's face on it. In which century was he president? → The 19th century (1800s): You find a lucky penny on the sidewalk, heads up. Whose face is on it? → Abraham Lincoln
- hosts-and-game-shows-0: overlap like q-2826: In the blind auditions of The Voice, coaches sit with their backs to the singer. How many coaches are there in most versions? → 4: You're watching the Blind Auditions on NBC's The Voice, and every coach's chair spins around. How many chairs is that? → 4
- inventors-and-founders-8: overlap like q-1382: ¿En qué década inventaron los hermanos Kellogg las hojuelas de cereal que hoy llamamos corn flakes? → Los años 1890: We were brothers at a health spa in Michigan. In 1894, cooked wheat left sitting too long gave us the idea for breakfast flakes. Who are we? → The Kellogg brothers
- inventors-and-founders-11: overlap like q-10613: For about 70 years, a bottle of Coca-Cola cost exactly one of these coins. In which US city was the drink invented, in 1886? → Atlanta: Pharmacist John Pemberton created Coca-Cola here in 1886. It later hosted the Olympics, and its airport is most years the busiest in the world. Which city? → Atlanta
- inventors-and-founders-16: overlap like q-0443: Una bombilla de larga duración, el fonógrafo y una de las primeras cámaras de cine: ¿qué inventor los desarrolló? → Thomas Edison: Thomas Edison invented this machine in 1877. What is it called? → Phonograph
- money-and-shopping-13: overlap like q-13806: Sam Walton founded Walmart. Which of these men did NOT also start a big American store chain? → Henry Ford: This warehouse store is named after the man who founded it in 1983. Who was he? → Sam Walton
- money-and-shopping-14: overlap like q-12947: Look at the eagle on the Great Seal of the United States. One claw holds arrows, the other an olive branch. What does the branch stand for? → Peace: This bird is printed on the back of every US one-dollar bill. What kind of bird is it? → A bald eagle
- national-parks-0: overlap like q-9060: Which river carved the canyon in this photo? → Colorado River: This close-up shows the Grand Canyon's layered walls. What did most of the work carving them out? → A river
- national-parks-8: overlap like q-9013: I'm thin blades of calcite sticking out of cave walls and ceilings in a honeycomb pattern. Wind Cave in South Dakota holds most of the world's examples of me. What am I called? → Boxwork: In 1903, it became the world's first cave national park. It lies under South Dakota's Black Hills, and its maze of passages is one of the longest on Earth. Which cave is it? → Wind Cave
- national-parks-10: overlap like q-3560: Look at this stalagmite growing up from a cave floor. What built it, layer by layer? → Minerals left by dripping water: They hang like icicles from the ceiling in caves like Carlsbad Caverns, grow slower than your fingernails, and can take thousands of years to form. What builds stalactites? → Dripping water full of minerals
- national-parks-12: overlap like q-6162: You're getting ready for game night. Which of these games do you NOT need a board for? → Hide-and-seek: You're on a long family road trip across the US. Which of these is NOT a classic car game? → Hide-and-seek
- national-parks-13: overlap like q-11891: Monument Valley's red rock towers sit on the border between Arizona and the state shown on this map. Which state is it? → Utah: This video shows giant red sandstone towers that have starred in many cowboy movies. Where is it? → Monument Valley
- plants-and-trees-1: overlap like q-10719: Washington State grows more of this fruit than any other US state. Which fruit is it? → Apple: Washington is America's top apple state. About what share of all apples grown in the US come from there? → About 60%
- plants-and-trees-13: overlap like q-11833: I was a US senator from Illinois who pushed for years to make the marigold the national flower. Long after my death, the rose won instead. Who am I? → Everett Dirksen: Look at this close-up: since 1986, this flower has been the official national flower of the United States. Which flower is it? → Rose
- comics-and-art-14: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Shepard Fairey's famous 2008 poster shows Barack Obama's face in red, beige and blue above a single word. Which word? → HOPE
- country-and-folk-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In 1963, folk singer Odetta sang before about 250,000 people who had come for jobs and civil rights. What was this event? → The March on Washington
- desserts-and-baking-1: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Look at this sweet, crunchy snack. Mixed with peanuts, it's the Cracker Jack from “Take Me Out to the Ball Game.” What is it? → Caramel corn
- desserts-and-baking-11: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Look at this scoop of cookies and cream ice cream. Which famous cookie gives it the dark bits? → Oreo
- ghosts-and-superstitions-11: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Real Voodoo in New Orleans rarely uses dolls stuck with pins. Where do most people know these dolls from? → Movies and cartoons
- ghosts-and-superstitions-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Scooby-Doo's friends often get him to be brave by offering him a treat. What is the treat called? → Scooby Snacks
- home-cooking-9: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Where are Americans most likely to eat a big bowl of this creamy dish? → At a backyard barbecue
- money-and-shopping-6: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: In 1950, a New York businessman started a card that let diners eat now and pay the bill later. What kind of card was it? → A credit card
- national-parks-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: This horseshoe-shaped walkway with a glass floor sticks out over the Grand Canyon on Hualapai land. What is it called? → The Skywalk
- place-names-3: hard fail: correct 3, unambiguous 2, no_giveaway 3, no_overlap 5: Three of these US towns put the stress on the same syllable as the European city they're named after. Which one doesn't? → New Berlin, Wisconsin
- place-names-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This Wisconsin city is said “oh-CLAIR,” sits where two rivers meet, and has a French name. What does its name mean? → Clear water
- place-names-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Michigan's name comes from a word in the Ojibwe language. What does it mean? → Big lake
- roots-and-soul-1: overlap like q-6397: Which singer made the moonwalk famous, gliding backward while seeming to walk forward? → Michael Jackson: He was the youngest of the five brothers in a famous Motown family band, then went solo and became the “King of Pop.” Who is he? → Michael Jackson
- school-life-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: They have rounded tips and short, blunt blades, and kindergarten kids use them to cut paper without getting hurt. What are they? → Safety scissors
- state-symbols-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Wisconsin calls itself “America's Dairyland.” What is its official state drink? → Milk
- state-symbols-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: The scissor-tailed flycatcher catches insects in midair and is the state bird of a state whose name comes from Choctaw words for “red people.” Which state? → Oklahoma
- trailblazers-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In 1984, Geraldine Ferraro, a congresswoman from Queens, New York, became the first woman to do what for a major US party? → Run for vice president
- weather-and-seasons-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: A young inventor's machine makes burgers and spaghetti rain down on his town. The film's title, “Cloudy with a Chance of Meatballs,” jokes about what? → A weather forecast
- roots-and-soul-9: overlap like q-5621: Hip hop was born at New York block parties, where DJs like Kool Herc stretched a song's drum beat by switching between two of these. What? → Record players: I spin vinyl records, and hip-hop DJs push me back and forth with their hands to make a scratching sound. What am I? → A turntable
- sayings-and-idioms-15: overlap like q-6458: It's made of wood, it's sharp at one end, and in old stories hunters use it against vampires. What is it? → A stake: Prospectors pounded me into the ground at the corners of their patch of land, so everyone knew it was taken. What am I? → A wooden stake
- school-life-3: overlap like q-10788: You're making a PB&J sandwich in an American kitchen. What kind of food is the “J”, the jelly? → A sweet fruit spread: In American lunchboxes, “PB&J” stands for peanut butter and… what? → Jelly
- school-life-13: overlap like q-6145: Cheerleaders shake pom-poms like these at games. What are they usually made of today? → Thin plastic strips: At US pep rallies they come in school colors, rustle loudly, and cheerleaders hold one in each hand. What are pom-poms? → Fluffy bunches of shiny strips
- state-symbols-16: overlap like q-0208: ¿Cómo se llamaban los hermanos que hicieron el primer vuelo en un avión con motor, en 1903? → Los hermanos Wright: North Carolina license plates say “First in Flight.” It honors something that lasted 12 seconds near Kitty Hawk in 1903. What was it? → The first powered airplane flight
- trailblazers-10: overlap like q-9095: Which Harlem nightclub's radio broadcasts in the late 1920s made Duke Ellington famous across America? → The Cotton Club: I was born in Washington, D.C., led my big band at Harlem's Cotton Club, and wrote “It Don't Mean a Thing (If It Ain't Got That Swing).” Who am I? → Duke Ellington
- trailblazers-12: overlap like q-9058: In 1804, sent by Thomas Jefferson, Lewis and Clark headed up the Missouri River to explore land the US had just bought. From which country? → France: From 1804 to 1806, we led a team across the West to the Pacific, guided in part by Sacagawea. Who are we? → Lewis and Clark
- trailblazers-14: overlap like q-5899: Louisa May Alcott's novel “Little Women” follows the March sisters. How many sisters are there? → 4: Jo March, the bold sister who wants to be a writer in “Little Women,” was based on which real person? → Louisa May Alcott
- trailblazers-16: overlap like q-9115: It's the biggest songbird in North America, and in an Edgar Allan Poe poem it only says “Nevermore.” Which bird is it? → Raven: This black bird gave its name to Baltimore's NFL team, after a famous poem where it says “Nevermore.” Who wrote the poem? → Edgar Allan Poe
- tv-shows-0: overlap like q-13801: You're on The Price Is Right playing Plinko, and your chip bounces down into the middle slot. About how much does that one chip win today? → $10,000: Its current version began in 1972, it has a game called Plinko, and it tells contestants to “come on down!” What is the longest-running daytime game show on US TV? → The Price Is Right
- tv-shows-4: overlap like q-10584: On Wheel of Fortune, a player with $5,000 in round money spins and lands on Bankrupt. How much round money do they have now? → $0: You're playing Wheel of Fortune, and the wheel stops on a black wedge that wipes out all your money for the round. What is that wedge called? → Bankrupt
- tv-shows-8: overlap like q-3842: You're watching the longest-running cartoon series in US TV history, and the dad yells “D'oh!”. Which show is it? → The Simpsons: I work at a nuclear power plant, I love donuts, and when something goes wrong I yell “D'oh!” Who am I? → Homer Simpson
- winter-holidays-7: overlap like q-8840: You're watching New Year's Eve in Times Square on TV. What slides down a pole as the clock counts down to midnight? → A glittering ball: You're watching the ball drop in Times Square, a tradition started by New York Times owner Adolph Ochs. In what year did the first ball drop? → 1907
- winter-holidays-8: overlap like q-4888: I wear the same red as Coca-Cola, have a big white beard and come down chimneys once a year. Who am I? → Santa Claus: In American Christmas stories, Santa slides down one of these to bring presents. What is it? → A chimney
- words-and-slang-14: overlap like q-8893: Many American kids “graduate” from kindergarten in tiny caps and gowns. The word “kindergarten” comes from German: what does it mean? → Children's garden: German immigrants opened the first kindergartens in America in the 1850s. What does the German word “kindergarten” literally mean? → Children's garden
