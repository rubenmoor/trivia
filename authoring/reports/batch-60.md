# batch-60

Made by `qgen batch` on 2026-11-12 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): family-and-school-traditions, more-sports, nineteenth-century, hosts-and-game-shows, roads-and-landmarks, place-names, cities-and-towns, american-literature, folk-heroes-and-tall-tales, country-and-folk, college-sports, national-parks, trailblazers, roots-and-soul, ghosts-and-superstitions, colonies-and-founding, sayings-and-idioms, states-and-capitals, desserts-and-baking, plants-and-trees, money-and-shopping, candy-and-snacks, rivers-lakes-and-mountains, state-symbols, tv-shows
- Merged: 169 (q-17471…q-17639)
- Approved: 152
- Needs work: 17
- Dropped by the pipeline: 86
- Reviewed by: claude-opus-5-5
- Claude calls: 422, about $55.11 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-58, batch-59; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-58 | batch-59 | batch-60 |
|---|---|---:|---:|---:|
| source locale |  | es-ES | es | en |
| drafts |  | 256 | 321 | 255 |
| skipped slots |  | 230 | 201 | 195 |
| dropped |  | 74 | 123 | 86 |
| drop rate | ≤ 20.0 % | 28.9 % ✗ | 38.3 % ✗ | 33.7 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 1 |
| dropped: hard fail no_giveaway |  | 16 | 12 | 20 |
| dropped: overlap |  | 52 | 108 | 64 |
| dropped: duplicate |  | 6 | 2 | 1 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 182 | 198 | 169 |
| approved |  | 172 | 177 | 152 |
| needs_work |  | 10 | 21 | 17 |
| needs_work rate | ≤ 20.0 % | 5.5 % ✓ | 10.6 % ✓ | 10.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.6 % ✓ | 2.5 % ✓ | 2.4 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.6 % ✓ | 0.0 % ✓ | 1.2 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.5 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.2 % ✗ | 3.5 % ✗ | 1.2 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.5 % ✓ | 5.6 % ✓ | 5.9 % ✓ |
| media: no pick in review 1 |  | 20 | 39 | 25 |
| media: recovered by research |  | 20 | 31 | 18 |
| media: no pick at record |  | 0 | 8 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.5 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 24.2 % ✗ | 36.4 % ✗ | 26.3 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 53.7 % ✗ | 40.9 % ✗ | 60.7 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.06 ✓ | 1.43 ✓ | 1.97 ✗ |
| approved 11–15 |  | 33 | 30 | 24 |
| top move | ≤ 25.0 % | 12.1 % ✓ | 16.7 % ✓ | 14.8 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 82.4 % | 77.8 % | 79.9 % |
| values stimulus |  | 4 | 4 | 4 |
| top clue | ≤ 60.0 % | 42.9 % ✓ | 44.9 % ✓ | 40.2 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 22.5 % ✓ | 23.2 % ✓ | 24.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.3 % ✓ | 20.2 % ✓ | 18.9 % ✓ |
| values lens |  | 10 | 11 | 11 |
| media share | 15.0 %–50.0 % | 17.6 % ✓ | 22.2 % ✓ | 20.1 % ✓ |
| mean fun | ≥ 3.40 | 3.36 ✗ | 3.38 ✗ | 3.51 ✓ |
| cost $ |  | $56.74 | $65.86 | $51.84 |
| $ per approved | ≤ $0.35 | $0.33 ✓ | $0.37 ✗ | $0.34 ✓ |
| calls |  | 363 | 422 | 362 |
| calls per approved |  | 2.11 | 2.38 | 2.38 |
| wall time h |  | 1.66 | 1.95 | 1.89 |
| days |  | 1 | 2 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 54 (2 %)
- Major among review needs work: 3 of 6 (50 %)
- Problems by kind: giveaway 10 (2 major), fact 1 (0 major), overlap 1 (1 major), media 3 (2 major), difficulty 5 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 1.0; ≥ 3 on 5 of 60 (8 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.27

Major findings on approved questions:

- **q-17482**: giveaway — The question gives itself away. It says Mickey Mouse, Bugs Bunny and Kermit the Frog have stars, and those three are exactly the wrong answers, so George Washington is the only option left before anyone has to know anything. The facts are correct: Mickey got his star in 1978, Bugs in 1985 and Kermit in 2002, Washington has none, and the fun fact's "more than 2,700 stars" holds. The Stan Freberg star picture is a fine choice. (http://127.0.0.1:8001/review/q-17482)

## Needs work

- **q-17486** (college-sports) I dance with the band at Stanford University's games. My team is named after a color, not after me. I'm green and shaggy. Who am I? → A tree: Hint 2 ("I don't have legs, I have roots") gives the answer away: among the four options only a tree has roots, so the question is solved by the second hint. Hint 1 ("Stanford's campus is full of me") also points strongly at a tree. Hint 2 should go vaguer (for example, about the Stanford Band or the costume being homemade), and the root/leaf clue should move to hint 3.
- **q-17489** (colonies-and-founding) This secret colonial group included Samuel Adams and Paul Revere, fought the Stamp Act and planned the Boston Tea Party. What was it called? → The Sons of Liberty: Hint 3 is factually wrong: "Liberty Bell" ends with "Bell", so "The Sons of Liberty" doesn't end with the same word as the bell's name. Change it to something like "Their name shares a word with the famous cracked bell in Philadelphia". The wrong answer "The Liberty Bell Club" also contains both words, so hint 3 points more toward it than toward the answer. Replace that wrong answer with one that doesn't use "Liberty" (for example "The Minutemen Society"), or rewrite hint 3 so it doesn't rely on the bell. Fact check: wrong. Answer is right, but hint 3 is misleading: the Liberty Bell's name ends in 'Bell', not 'Liberty'. 'Liberty' is the bell's first word.
- **q-17491** (colonies-and-founding) In which year did the signers put their names on the Declaration of Independence? → 1776: This asks for the same fact as draft q-17598, the year the 13 colonies declared independence (1776), and it also overlaps a lot with approved q-11834 (the Statue of Liberty tablet date, 1776). Keep only one of the two drafts. Separately, hint 2 ("the year celebrated every Fourth of July") gives the answer away.
- **q-17517** (hosts-and-game-shows) Simon Cowell has judged several US talent shows. Which of these has he NEVER judged? → The Voice: None of the media candidates shows a TV studio or a talent-show stage. They are a 1922 hearing photo, a cathedral painting, a campus building, a 1980s band portrait, a praying mantis and a circuit board, and no new search is allowed. The text itself is fine: the facts check out (Cowell judged Idol, AGT and the US X Factor, never The Voice) and the earlier invented scenario is gone. It needs a new image search, for example "talent show stage" or "TV studio audience". No suitable picture found for this question.
- **q-17523** (more-sports) Every NHL team has retired the jersey number in this close-up, all for one player. Who wore it? → Wayne Gretzky: None of the candidates shows the number 99 on a jersey. 1 and 2 are a MoDo jersey with the number 29, and 3 is an old black-and-white Leafs vs. Black Hawks game photo. Since the image is essential and the question points to "this close-up," it needs a close-up of a 99 jersey with no name on it. Another search isn't allowed, so this needs a manual media fix or a new search, for example "number 99 hockey jersey". No suitable picture found for this question.
- **q-17524** (more-sports) At the 1968 Olympics in Mexico City, Bob Beamon smashed the long jump world record. By about how much? → About 22 inches: The picked picture is broken at the source (truncated (Premature end of JPEG file)).
- **q-17529** (national-parks) You're hiking in a US national park and find ancient pictures of animals pecked into a rock wall. Which word does NOT describe them? → Fossils: The text is fine, but the image slot needs a photo of the rock art itself (e.g. "petroglyphs rock panel" or "Newspaper Rock petroglyphs"). Every candidate shows only bare canyon walls or hoodoos, and no new search is allowed this round. No suitable picture found for this question.
- **q-17541** (place-names) In the film “Field of Dreams,” a farmer builds a baseball field in his cornfield. Which state, shown here, is his farm in? → Iowa: The essential slot needs a blank outline map of Iowa, and no candidate is one. The only map (5, a 1928 Iowa road map) has "IOWA" printed in its title and its caption, which gives the answer away. Another search isn't allowed, so the slot needs a label-free Iowa outline (for example "Iowa blank outline map" or "Iowa locator map"). No suitable picture found for this question.
- **q-17542** (place-names) Madrid, an old coal-mining town on the Turquoise Trail, is said “MAD-rid,” not like Spain's capital. Which state, shown here, is it in? → New Mexico: None of the candidates is a blank New Mexico outline, and every map has text naming the answer. #4 has the outline but is titled "Köppen climate types of New Mexico". #2, #3 and #6 are old survey maps labeled "New Mexico" or "Mexico". #1 and #5 are photos, not maps. A new search isn't allowed, so the slot needs a clean, unlabeled outline map, for example from the query "New Mexico blank map". No suitable picture found for this question.
- **q-17551** (plants-and-trees) It's the national flower of the United States, a big New Year's Day parade in Pasadena is named after it, and people give red ones on Valentine's Day. What is it? → Rose: The description gives the answer away. Read with only the four options, “Valentine's Day's most overworked flower, with its own parade and football game” points straight to the rose (the Rose Parade and the Rose Bowl) and rules out tulip, daisy and lily. Rewrite it so it plays on the flower or holiday theme without naming Valentine's Day or the parade and football game.
- **q-17570** (ghosts-and-superstitions) Many Americans believe a New Year's Eve kiss brings a year full of love and luck. When exactly are you supposed to kiss? → At the stroke of midnight: Hint 2 ("right as the old year ends") is the definition of midnight on New Year's Eve, so it gives the answer away before hint 3. It also rules out all three wrong answers. Hint 2 should only narrow things down, for example by mentioning the countdown crowd, without naming the moment the year changes.
- **q-17588** (sayings-and-idioms) To say someone was very small long ago, Americans say they were “knee-high to a…” what? → A grasshopper: None of the image candidates fits the question, and a new search isn't allowed. The slot needs a photo of a child's height marks on a wall or door frame, or of a grasshopper-free meadow or small child scene, sourced by hand. No suitable picture found for this question.
- **q-17598** (states-and-capitals) You're watching Fourth of July fireworks, which celebrate the day the 13 colonies declared independence. What year was that? → 1776: This asks for the same fact as q-17491 (draft: the year the Declaration of Independence was signed, 1776). It also overlaps heavily with the approved q-11834 (the Statue of Liberty tablet date, 1776, which is the date of the Declaration). In both cases the question is the year of American independence. Drop it, or turn it into a different Fourth of July fact that isn't the year.
- **q-17602** (trailblazers) Madam C.J. Walker, daughter of formerly enslaved parents, became one of America's first self-made female millionaires with her own line of what? → Hair care products: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-17612** (roads-and-landmarks) When this San Francisco bridge opened in 1936, its lower deck carried trucks and what else? → Electric trains: The question's premise is wrong. When the Bay Bridge opened in November 1936, its lower deck carried trucks and cars. The electric interurban trains only started in January 1939 and ran until 1958. Reword it to something like "Its lower deck carried trucks and, from 1939 to 1958, what else?" Fact check: wrong. The Bay Bridge opened in Nov 1936 with the lower deck carrying trucks and cars. The electric interurban trains only began running in January 1939, so 'when it opened in 1936' is inaccurate. The 1958 end date is correct.
- **q-17620** (state-symbols) The state on this map has the Latin motto “Montani semper liberi.” Which state is it? → West Virginia: None of the six candidates shows a blank outline map of West Virginia, and the question needs one because it says "The state on this map". A new search is not allowed this run. The media needs a manual source, for example a blank West Virginia locator or outline map from Commons with no labels. No suitable picture found for this question.
- **q-17624** (state-symbols) This 1999 Delaware quarter shows Caesar Rodney riding through a stormy night in 1776 to vote for independence in Philadelphia. About how far did he ride? → About 80 miles: None of the media candidates shows the 1999 Delaware quarter the question names. They are beach and marina photos of Rodney Bay in St Lucia, a police station there, and a portrait of Admiral George Rodney. A new search isn't allowed, so the slot needs the reverse of the Delaware state quarter, for example from a search like "Delaware state quarter reverse" on Commons. No suitable picture found for this question.

## Question axes

- move: analogy 2, cause_effect 12, count 4, estimate 6, identify 25, made_of 9, name_concept 24, odd_one_out 16, origin 20, purpose 11, record 2, sequence 5, when 6, who 16, word_meaning 11
- stimulus: detail 8, map_outline 3, none 135, photo 23
- clue: completion 7, direct 68, riddle 16, scenario 20, three_facts 58
- answer_kind: group 18, number 12, person 24, place 27, thing 41, time 6, word 41
- lens: body_senses 4, educational_media 12, everyday 32, history 32, language 21, nature 10, pop_culture 30, popular_science 4, school 19, science_news 2, university 3

## Dropped by the pipeline

- american-literature-10: overlap like q-2585: Who are these people, throwing their caps in the air? → Students finishing their studies: The rhyming book “Oh, the Places You'll Go!” is a top gift for which big day, when students finish school and toss their caps? → Graduation
- american-literature-12: overlap like q-13890: In The Wizard of Oz, a twister carries Dorothy and her little dog from a Kansas farm to Oz. What is her last name? → Gale: Dorothy and her dog Toto are carried off by a tornado. At the end, she clicks her heels, says “There's no place like home,” and wakes up in which state? → Kansas
- american-literature-17: overlap like q-4522: Look at this huge skull with teeth as big as bananas. Which dinosaur did it belong to? → Tyrannosaurus rex: In “Jurassic Park,” this dinosaur rules the island and roars in the very last scene. Which dinosaur's skeleton is this? → Tyrannosaurus rex
- candy-and-snacks-1: overlap like q-7216: ¿Cuál de estos NO es un sabor de las Papas Margarita? → Chocolate: You open a bag of Airheads taffy bars. Which of these flavors will you NOT find inside? → Chocolate
- candy-and-snacks-5: overlap like q-4172: Tony the Tiger sells sugar-frosted flakes like these. What grain are the flakes made from? → Corn: Tony the Tiger says this sugar-coated corn flake cereal is “Grrreat!” What is it called? → Frosted Flakes
- cities-and-towns-0: overlap like q-9009: Which Pennsylvania town has a Chocolate Avenue, air that can smell like cocoa, and streetlights shaped like foil-wrapped chocolate drops? → Hershey: The town of Hershey, Pennsylvania, got its name because one man built a chocolate factory there. Who was he? → Milton Hershey
- cities-and-towns-7: overlap like q-16673: The Boston Bruins took their name from “Bruin,” an old folk-tale nickname for an animal. Which animal? → Bear: A baby of this animal gave the Chicago Cubs baseball team its name and its mascot. What animal is it? → A bear
- cities-and-towns-14: overlap like q-12748: I played for the Braves in Milwaukee and Atlanta, and in 1974 I hit my 715th home run to pass Babe Ruth. Who am I? → Hank Aaron: This New York Yankees slugger hit 714 home runs and was nicknamed “the Bambino.” Who is he? → Babe Ruth
- college-sports-2: overlap like q-16649: Many American schools pick an animal like a tiger or an eagle, give its name to their teams, and have someone dress up as it at games. What is this mascot for? → Cheering for the school's teams: It's often a costumed animal, it dances at games, and its picture is on the team's shirts. What is a school mascot for? → To cheer on the team and stand for the school
- college-sports-3: overlap like q-6145: Cheerleaders shake pom-poms like these at games. What are they usually made of today? → Thin plastic strips: I shake pom-poms, lead the crowd in chants, and get tossed into the air in stunts on the sidelines. Who am I? → A cheerleader
- college-sports-4: overlap like q-4746: A poor, kind girl falls in love with a rich man, and after many troubles they marry at the end. What kind of story is this often called? → A Cinderella story: I'm a low-seeded March Madness team nobody picked, yet I keep beating the giants until my magic runs out. Which fairy-tale girl am I named after? → Cinderella
- college-sports-11: overlap like q-12786: There's a parade, a big football game and a dance, and a king and queen are crowned. Who is an American homecoming meant to welcome back? → Former students: At a US high school homecoming, who wears a crown and sash like the one in this photo? → The homecoming queen
- colonies-and-founding-7: overlap like q-8859: Paul Revere started his famous midnight ride in 1775 in the city where this church stands. Which city is it? → Boston: I was a silversmith in Boston. One April night in 1775, I rode a horse to warn that British soldiers were coming. Who am I? → Paul Revere
- colonies-and-founding-12: overlap like q-11838: You visit the National Archives in Washington, D.C. Which document there is often called the oldest national rulebook still in use? → The Constitution: What is the main job of the US Constitution? → Setting the rules for how the government works
- country-and-folk-0: overlap like q-7200: Escucha: con este instrumento, y no con acordeón, Guillermo Buitrago grabó canciones costeñas en los años 40. ¿Cuál es? → La guitarra: Listen: Willie Nelson has played the same instrument, nicknamed “Trigger,” for over 50 years. What kind of instrument is it? → A guitar
- country-and-folk-4: overlap like q-5611: Musicians move a bow back and forth to play some instruments. Which instrument family is usually played with a bow? → String instruments: A fiddle like this one is the star of American barn dances. What do fiddlers usually play it with? → A bow
- country-and-folk-5: overlap like q-3375: I was accepting my first MTV video award in 2009 when a rapper grabbed my microphone to say Beyoncé deserved it. Who am I? → Taylor Swift: I started out as a teenager singing country songs with my guitar. Now I'm a pop superstar, and my Eras Tour became the biggest concert tour ever. Who am I? → Taylor Swift
- desserts-and-baking-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: You hear a jingly tune coming down your street. In which season does the ice cream truck come around the most? → Summer
- desserts-and-baking-9: overlap like q-6017: Many white hard candies and candy canes get their cool, fresh taste from the plant shown up close. Which plant is it? → Mint: A lemon is to sour as a classic red and white candy cane is to… → Minty
- desserts-and-baking-12: overlap like q-3253: We have antlers, and on Christmas Eve we fly across the sky pulling something heavy. What do we pull? → Santa's sleigh: On Christmas Eve, kids leave milk and cookies for my boss and carrots for me. I fly through the night pulling his sleigh. Who am I? → A reindeer
- family-and-school-traditions-2: overlap like q-15779: I happen in backyards every July 4th: burgers and hot dogs sizzle on a grill, and later fireworks light up the sky. What am I? → A cookout: It's the Fourth of July in the US. The barbecue is over and the sun goes down. What do families watch next? → Fireworks
- family-and-school-traditions-4: overlap like q-13916: US report cards grade from A at the top down to F for failing. How many different letters are used? → 5: An American kid brings home a report card, and the school wants it signed and sent back. Who signs it? → A parent
- family-and-school-traditions-14: overlap like college-sports-6: I paint my face in school colors, stand in the bleachers with my classmates, and cheer the whole game. Who am I? → A student fan: They're on the team jerseys, the cheerleaders' pom-poms and the gym banners, and fans wear them to every game. What are they called? → School colors
- family-and-school-traditions-16: overlap like q-10580: Kids at sleepovers dare each other to call me. Turn off the bathroom light, look into the mirror and say my name three times, and I'm said to appear. Who am I? → Bloody Mary: What do Americans call it when kids spend the night at a friend's house with sleeping bags, snacks and movies? → A sleepover
- folk-heroes-and-tall-tales-6: overlap like q-8866: Whose signature is the largest on the Declaration of Independence? → John Hancock: John Hancock led the Continental Congress and signed the Declaration of Independence in big letters in 1776, in today's Independence Hall. In which city? → Philadelphia
- folk-heroes-and-tall-tales-7: overlap like q-8894: I hissed and puffed while I pounded holes in rock. A man with a hammer raced me through a mountain tunnel, and he won. What am I? → A steam drill: Legend says John Henry swung his hammer and beat a steam drill while digging a railroad tunnel. In which century is the race set? → The 1800s
- hosts-and-game-shows-2: overlap like q-2825: In “Got Talent” shows, the golden buzzer sends an act straight to the live shows. How many times can each judge usually press it in a season? → 1: During America's Got Talent auditions, how many times per season can each judge hit the Golden Buzzer? → 1
- hosts-and-game-shows-4: overlap like q-11795: This singing contest began on TV in 2002. Simon Cowell judged, viewers voted by phone, and Kelly Clarkson won the first season. Which show is it? → American Idol: Kelly Clarkson won the very first American Idol in 2002, years before her own talk show. Who picked her as the winner? → Viewers voting from home
- hosts-and-game-shows-16: overlap like q-2826: In the blind auditions of The Voice, coaches sit with their backs to the singer. How many coaches are there in most versions? → 4: On the US show The Voice, coaches sit with their backs to the singer in big spinning chairs. Usually, how many coaches are there? → 4
- hosts-and-game-shows-17: overlap like q-10783: You're in the audience as The Price Is Right begins. How many people are called with “Come on down!” to fill Contestants' Row? → 4: Ed McMahon is to “Heeere's Johnny!” as game show announcer Johnny Olson is to… → “Come on down!”
- money-and-shopping-1: overlap like q-8848: Every July 4, Americans light up the night sky like this. Whose birthday are they celebrating? → The United States: Lots of US stores hold big sales on the summer holiday when the sky fills with fireworks like these. Which holiday is it? → Fourth of July
- money-and-shopping-13: overlap like q-2892: Whose portrait is on the front of the US one-dollar bill? → George Washington: You pull a $1 bill out of your piggy bank. Whose face is on the front? → George Washington
- more-sports-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In the backyard game of horseshoes, players toss U-shaped shoes at a metal stake. What is a “ringer”? → A shoe that lands around the stake
- more-sports-15: overlap like q-1891: En las 500 Millas de Indianápolis, el ganador no celebra con champaña. ¿Qué se toma? → Leche: Instead of spraying champagne, the Indianapolis 500 winner celebrates in Victory Lane with a cold bottle of… → Milk
- national-parks-1: overlap like q-11881: This flat-topped hill in the American Southwest is much wider than it is tall. What is it called? → A mesa: Out West, a lone rock hill like this one, with steep sides and a flat top, is narrower than it is tall. What is it called? → A butte
- national-parks-3: overlap like q-8927: You stand at the rim of Bryce Canyon in Utah, looking at thousands of orange rock spires called hoodoos. What mainly carved them? → Ice freezing and melting in cracks: Bryce Canyon in Utah is packed with thousands of tall, thin rock towers like these. What are they called? → Hoodoos
- national-parks-9: overlap like q-13891: I'm a bear in a ranger's hat and jeans. Since the 1940s I've told Americans, “Only you can prevent forest fires.” Who am I? → Smokey Bear: Park rangers wear hats like this one, with a flat brim and four dents on top. Which famous US character also wears one? → Smokey Bear
- nineteenth-century-0: overlap like q-3356: Almost every Wild West town had a building like this one. What was it mainly used for? → Drinking, card games and meeting people: In Wild West towns, this place had swinging half-doors, a long wooden bar and often a piano player. What was it called? → A saloon
- nineteenth-century-2: overlap like q-9058: In 1804, sent by Thomas Jefferson, Lewis and Clark headed up the Missouri River to explore land the US had just bought. From which country? → France: In 1803, Napoleon, the ruler of this country, sold the huge Louisiana Territory to the United States. Which country is it? → France
- nineteenth-century-3: overlap like q-2432: “I'm a code of dots and dashes, and I carry my American inventor's name.” Who was he? → Samuel Morse: With a key like this one, telegraph operators tapped out messages in a code of dots and dashes. Who is that code named after? → Samuel Morse
- nineteenth-century-5: overlap like q-8941: Lincoln gave his Gettysburg Address in 1863, opening with “Four score and seven years ago.” A score is 20. Which event was he pointing back to? → The Declaration of Independence: This is the battlefield of Gettysburg, in Pennsylvania. Which president gave a famous short speech here in November 1863? → Abraham Lincoln
- nineteenth-century-11: overlap like q-3107: You find a US penny with Abraham Lincoln's face on it. In which century was he president? → The 19th century (1800s): Look at this one-cent coin. Whose face is on it? → Abraham Lincoln
- nineteenth-century-17: overlap like q-4403: Long before rappers wore it, cowboys tied a cloth like this one over their nose and mouth. Why? → To keep dust out: On long cattle drives, the herds kicked up clouds of dust. Which riders pulled a cloth like this over their nose and mouth? → Cowboys
- plants-and-trees-15: overlap like q-2482: The sweet syrup often poured on pancakes comes from the tree with this leaf. Which tree is it? → Maple: Every spring in Vermont, farmers drill small holes in trees, hang buckets to catch the sap, and boil it for hours. What sweet treat do they make? → Maple syrup
- american-literature-4: overlap like q-11843: In Shel Silverstein's book “The Giving Tree,” the tree gives a boy its fruit to sell, its branches for a house and its trunk for a boat. What kind of tree is it? → An apple tree: In Shel Silverstein's “The Giving Tree,” the grown-up boy wants a boat so he can sail far away. What does the tree give him? → Her trunk
- college-sports-6: hard fail: correct 5, unambiguous 3, no_giveaway 5, no_overlap 4: I paint my face in school colors, stand in the bleachers with my classmates, and cheer the whole game. Who am I? → A student fan
- colonies-and-founding-8: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: I was a farmer in colonial Massachusetts who kept my musket close, ready to fight almost the moment an alarm rang. Who am I? → A minuteman
- desserts-and-baking-10: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: This frosted pastry is a Pop-Tart. Which kitchen appliance was it made to be warmed up in? → A toaster
- family-and-school-traditions-17: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: I visit American schools a few times a year. I fill the library with books, posters and pens with fluffy tops for kids to buy. What am I? → The book fair
- folk-heroes-and-tall-tales-12: overlap like q-16653: Engineer Casey Jones stayed aboard the speeding Cannonball Express to slow it before it hit a stalled train in 1900, saving his passengers. In which state did it happen? → Mississippi: In the 1890s, people along one railroad knew who was driving by his train whistle, which sounded like a whippoorwill bird. Who was he? → Casey Jones
- ghosts-and-superstitions-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: La Llorona, “the weeping woman,” wears a white dress and wails by rivers at night. Which country does her legend come from? → Mexico
- ghosts-and-superstitions-10: overlap like q-15737: Look at this coin. An American rhyme says if you find one and pick it up, all day long you'll have… what? → Good luck: When their car drives over these, many American kids lift their feet off the floor. Why? → For good luck
- money-and-shopping-7: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: In the US, when you order a pizza like this one to your home, who do you usually give a tip to? → The delivery driver
- more-sports-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: The Golden Gloves is a yearly US tournament that newspapers started in the 1920s. Who competes in it? → Amateur boxers
- more-sports-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: The Pittsburgh Penguins' first home was the first big sports arena with a roof that could open. What did fans call it? → The Igloo
- national-parks-5: overlap like q-13153: Hör zu: Mit diesem schrillen Pfiff warnt ein Tier im Nationalpark Berchtesgaden seine Familie vor Adlern. Welches Tier ist das? → Murmeltier: They are the heaviest members of the squirrel family, they sleep all winter in burrows, and Punxsutawney Phil is one. What are they? → Marmots
- national-parks-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Kids earn me at US national parks by filling in an activity book and promising to protect the park. What am I? → A Junior Ranger badge
- nineteenth-century-4: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Davy Crockett, the “King of the Wild Frontier,” fought at the Alamo in 1836. In which state is the Alamo? → Texas
- roads-and-landmarks-0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: This US building went up during World War II, in only about 16 months. What is it mostly made of? → Concrete
- roads-and-landmarks-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This close-up shows part of an old-style bridge seen on country roads in New England and Pennsylvania. What kind of bridge is it? → A covered bridge
- roads-and-landmarks-7: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: The elevators of One World Trade Center whisk visitors up to the observation deck near the top. About how long does the ride take? → Under 1 minute
- roads-and-landmarks-10: overlap like q-12916: When it opened in 1940, the Pennsylvania Turnpike was called “America's first superhighway.” Its mountain tunnels had first been dug decades earlier for what? → A railroad: Long ago, some roads were blocked by a spiked bar that was moved aside once a traveler paid. Which word for a toll road comes from this? → Turnpike
- roots-and-soul-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Alicia Keys picked her stage name because of the instrument she has played since she was 7. Which instrument is it? → The piano
- sayings-and-idioms-2: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Before every game, football coaches draw one up for the whole game. Americans now use the same two words for tackling any big task at work or school. What are they? → Game plan
- sayings-and-idioms-11: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: You're jumping up and down to open your presents, and someone says “Hold your horses!” Who is this old saying usually linked to? → Wagon drivers
- sayings-and-idioms-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Beavers work hard, building dams all night. So what kind of person do Americans call an “eager beaver”? → Someone who is extra keen to work
- state-symbols-2: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Abraham Lincoln once used this word in a speech. What is a “Michigander”? → Someone from Michigan
- trailblazers-7: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Annie Jump Cannon sorted about 350,000 stars by hand and shaped the O, B, A, F, G, K, M star classes. Which group of women was she part of? → The Harvard Computers
- rivers-lakes-and-mountains-8: overlap like q-14933: You drift down the Mississippi on a raft like Huck Finn. Just north of St. Louis, which big river pours in from the west? → The Missouri River: Huck Finn floats on a raft down the river shown on this map. Which river is it? → Mississippi River
- rivers-lakes-and-mountains-10: overlap like q-11762: Paul Bunyan, the giant of American tall tales, swings his huge axe all day. What is his job? → Lumberjack: This giant statue shows Paul Bunyan, hero of American tall tales. The stories about him were first told by which workers? → Lumberjacks
- roads-and-landmarks-2: overlap like q-11820: You're the night guard in “Night at the Museum,” and a US president on horseback comes to life to help you. Which president is he? → Theodore Roosevelt: My father helped found New York's natural history museum, and I loved exploring the wild. In “Night at the Museum,” I ride a horse through its halls. Who am I? → Theodore Roosevelt
- roads-and-landmarks-3: overlap like q-9058: In 1804, sent by Thomas Jefferson, Lewis and Clark headed up the Missouri River to explore land the US had just bought. From which country? → France: It starts in Montana's Rocky Mountains, it's the longest river in the US, and Lewis and Clark paddled up it in 1804. Which river is it? → The Missouri
- roads-and-landmarks-8: overlap like q-17480: This California theme park opened in 1955, has Sleeping Beauty Castle and is the only Disney park Walt Disney saw finished. What is it? → Disneyland: I opened a park in California in 1955. Its first street, Main Street, U.S.A., looks like the little town where I grew up. Who am I? → Walt Disney
- roads-and-landmarks-14: overlap like q-17084: Welcher dieser Schätze gehört NICHT zu den Museen auf der Berliner Museumsinsel? → Mona Lisa: During World War II, Fort Knox in Kentucky kept some famous treasures safe. Which of these was NOT kept there? → The Mona Lisa
- roots-and-soul-4: overlap like q-5621: Hip hop was born at New York block parties, where DJs like Kool Herc stretched a song's drum beat by switching between two of these. What? → Record players: “I spin round and round, a DJ puts a vinyl record on me, and hip-hop was born on two of me side by side.” What am I? → A turntable
- sayings-and-idioms-8: overlap like q-11800: This metal rod on a roof protects the building from lightning. Which American invented it? → Benjamin Franklin: I flew a kite in a thunderstorm, my face is on the $100 bill, and I told young workers “Remember that time is money.” Who am I? → Benjamin Franklin
- state-symbols-8: duplicate like q-2895: This snowy volcano, Mount Rainier, is in the only US state named after a president. Which state is it? → Washington: Woody Guthrie's “Roll On, Columbia” is the official folk song of the state on this map. Which state is it? → Washington
- state-symbols-17: overlap like q-14826: Larry Bird played college basketball in this Indiana city on the Wabash River, said “TERR-uh HOHT.” What does its French name mean? → High ground: Complete the title of Indiana's state song: “On the Banks of the ___, Far Away.” → Wabash
- states-and-capitals-3: overlap like q-4764: What is this famous room in the White House called? → Oval Office: The president works in a White House room shaped like a stretched circle. Complete its name: the Oval… → Office
- states-and-capitals-12: overlap like q-9097: You can meet Mickey Mouse at the park with this castle. Which US state is it in? → Florida: You're at the most-visited theme park in the world, home of Cinderella Castle, at Walt Disney World. Which state are you in? → Florida
- states-and-capitals-16: overlap like q-2482: The sweet syrup often poured on pancakes comes from the tree with this leaf. Which tree is it? → Maple: In New England, people collect sap in buckets like these each spring and boil it into sweet syrup. Which tree is the sap from? → Maple
- trailblazers-11: overlap like q-17600: Carl Sagan's team packed it with music, sounds and greetings in 55 languages. It flew on both Voyager probes in 1977 as a message for aliens. What is it? → A gold-plated record: You're watching “Back to the Future,” and Marty McFly plays “Johnny B. Goode” at the 1955 school dance. Which rock 'n' roll pioneer wrote it? → Chuck Berry
- trailblazers-12: overlap like q-7950: Es la rueda gigante con canastas de las ferias. George Ferris construyó la primera en 1893, y en Colombia le decimos el nombre de la ciudad donde se estrenó. ¿Qué ciudad? → Chicago: Engineer George Ferris built the first giant wheel like this one for the 1893 World's Fair. In which city was it? → Chicago
- tv-shows-0: overlap like q-4198: In the Minions' language, “Bello!” is to hello as “Poopaye!” is to… → Goodbye: Watching Dora the Explorer, you learn that “hola” is to hello as “adiós” is to… → Goodbye
- tv-shows-1: overlap like q-3842: You're watching the longest-running cartoon series in US TV history, and the dad yells “D'oh!”. Which show is it? → The Simpsons: I'm one short word. A bald, yellow TV dad shouts me every time he does something dumb. What am I? → “D'oh!”
- tv-shows-11: overlap like q-12755: In “Stranger Things,” the kids of Hawkins, Indiana, ride their bikes into trouble in which decade? → The 1980s: In which decade is Stranger Things set? → The 1980s
