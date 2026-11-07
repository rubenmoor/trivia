# batch-48

Made by `qgen batch` on 2026-11-07 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): roads-and-landmarks, fairs-and-festivals, states-and-capitals, household-brands, candy-and-snacks, cities-and-towns, movie-favorites, national-symbols, family-and-school-traditions, regional-dishes, more-sports, roots-and-soul, school-life, restaurant-chains, wildlife, college-sports, twentieth-century, money-and-shopping, american-literature, inventors-and-founders, holidays, nineteenth-century, kids-tv, place-names, cryptids-and-ufos
- Merged: 221 (q-14725…q-14945)
- Approved: 196
- Needs work: 25
- Dropped by the pipeline: 102
- Reviewed by: claude-opus-5-5
- Claude calls: 515, about $67.94 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-46, batch-47; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-46 | batch-47 | batch-48 |
|---|---|---:|---:|---:|
| source locale |  | es-ES | es | en |
| drafts |  | 333 | 320 | 323 |
| skipped slots |  | 153 | 202 | 127 |
| dropped |  | 62 | 85 | 102 |
| drop rate | ≤ 20.0 % | 18.6 % ✓ | 26.6 % ✗ | 31.6 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 0 |
| dropped: hard fail unambiguous |  | 2 | 0 | 1 |
| dropped: hard fail no_giveaway |  | 13 | 13 | 23 |
| dropped: overlap |  | 43 | 71 | 74 |
| dropped: duplicate |  | 3 | 0 | 2 |
| dropped: fact-check wrong |  | 1 | 0 | 2 |
| merged |  | 271 | 235 | 221 |
| approved |  | 255 | 213 | 196 |
| needs_work |  | 16 | 22 | 25 |
| needs_work rate | ≤ 20.0 % | 5.9 % ✓ | 9.4 % ✓ | 11.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.1 % ✓ | 2.6 % ✓ | 4.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.1 % ✓ | 0.9 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.5 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.1 % ✗ | 2.1 % ✗ | 1.4 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.0 % ✓ | 3.8 % ✓ | 6.3 % ✓ |
| media: no pick in review 1 |  | 32 | 40 | 27 |
| media: recovered by research |  | 25 | 34 | 20 |
| media: no pick at record |  | 7 | 6 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 14.7 % ✓ | 23.8 % ✗ | 24.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 67.4 % ✓ | 50.9 % ✗ | 71.1 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.31 ✓ | 1.11 ✓ | 1.27 ✓ |
| approved 11–15 |  | 58 | 47 | 54 |
| top move | ≤ 25.0 % | 18.1 % ✓ | 13.6 % ✓ | 17.6 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 79.0 % | 88.1 % | 81.9 % |
| values stimulus |  | 4 | 4 | 5 |
| top clue | ≤ 60.0 % | 50.2 % ✓ | 43.0 % ✓ | 38.0 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 18.8 % ✓ | 25.1 % ✓ | 25.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 22.9 % ✓ | 17.0 % ✓ | 24.4 % ✓ |
| values lens |  | 9 | 11 | 11 |
| media share | 15.0 %–50.0 % | 21.0 % ✓ | 11.9 % ✗ | 18.1 % ✓ |
| mean fun | ≥ 3.40 | 3.43 ✓ | 3.40 ✓ | 3.49 ✓ |
| cost $ |  | $76.48 | $72.25 | $64.67 |
| $ per approved | ≤ $0.35 | $0.30 ✓ | $0.34 ✓ | $0.33 ✓ |
| calls |  | 523 | 485 | 455 |
| calls per approved |  | 2.05 | 2.28 | 2.32 |
| wall time h |  | 2.07 | 2.04 | 1.73 |
| days |  | 1 | 2 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 53 (0 %)
- Major among review needs work: 5 of 7 (71 %)
- Problems by kind: giveaway 5 (1 major), fact 1 (1 major), ambiguity 1 (1 major), overlap 3 (2 major), media 6 (3 major), difficulty 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.27

Major findings on approved questions:

None.

## Needs work

- **q-14734** (american-literature) Langston Hughes's poem that begins “I, too, sing America” answers “I Hear America Singing.” Who wrote that one? → Walt Whitman: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-14751** (cities-and-towns) You're at a Super Bowl party, and there's a pile of Buffalo wings on the table. About how many chicken wings do Americans eat that weekend? → 1 billion: This asks the same fact as the approved question q-11788 ("On Super Bowl Sunday, Americans eat a mountain of chicken wings. About how many?", answer 1.4 billion). Drop it or replace it with a different fact about a US city.
- **q-14752** (college-sports) The Crimson Tide plays football in Tuscaloosa, its mascot is an elephant named Big Al, and fans shout “Roll Tide!” Which state is its university in? → Alabama: Overlap: approved q-10670 (Nick Saban) says “Alabama's Crimson Tide” in its question text, so a player who has seen it gets this one for free. Hint 2 also gives the answer away. It names Georgia and Mississippi as neighbors, which rules out two options, and it names Montgomery as the capital, which solves the question. Hint 2 should only narrow things down, not hand over the answer.
- **q-14755** (college-sports) I'm the games students play against other students from their own school, not other schools. My name comes from Latin for “within the walls.” What am I? → Intramural sports: The picked picture is broken at the source (truncated (Premature end of JPEG file)).
- **q-14757** (college-sports) Every spring, 68 college basketball teams play in March Madness, and everyone talks about the “Final Four.” What is the Final Four? → The last four teams left: Hint 2 ("more than 60 of the 68 teams have gone home") lets players work out that only about four teams remain. Next to the four options, that gives away "The last four teams left". Replace hint 2 with something vaguer, for example that every team still in it has won all its games so far.
- **q-14762** (cryptids-and-ufos) Zeta Reticuli is a pair of Sun-like stars about 39 light-years away. UFO fans call it the home of the gray aliens. What made them link it to aliens? → A star map from the Betty and Barney Hill story: Hints 1 and 2 give the answer away. Only one option is about a couple, so hint 1 ("a story a couple told under hypnosis in the 1960s") settles it at once. Hint 2 ("shown a drawing aboard the ship") also points straight to the star-map option. Hint 3 names Betty Hill, so it contains part of the answer. Rewrite hints 1–2 so they stay vague (for example, the 1970s debate among astronomers, or a model built from beads), and keep the Hill name out of the hints.
- **q-14775** (holidays) It's a plastic card from a store, someone puts money on it for you, and you use it to buy whatever you like there. What is it? → A gift card: The media slot searches for wrapped presents. With the options gift card, credit card, library card and report card, a picture of gift-wrapping points straight at "gift card", even blurred. All four candidates are gift-wrapping or toy-drive scenes, and no new search is allowed. Re-search with a neutral store setting, such as "store checkout counter" or "shopping mall interior". The text itself is fine. No suitable picture found for this question.
- **q-14782** (household-brands) I'm a big plastic mat with rows of red, blue, yellow and green circles. A spinner calls out “right hand, red!” until everyone falls over. What game am I? → Twister: The text is fine, but no media candidate fits. All three are scans of an old Japanese handscroll painting with colour calibration bars. They don't show the world of an American party game played on a floor mat, and no new search is allowed. A decorative image needs a new search, for example "kids playing living room" or "family game night". No suitable picture found for this question.
- **q-14783** (household-brands) You're setting up the classic board game The Game of Life. Which of these is NOT in the box? → Dice: Hint 2 ("The thing that decides your move sits on the board itself, not loose in your hand") gives the answer away. Of the four options, only dice are held loose in the hand, and it also says that the spinner is in the box. Replace it with a mid-strength hint that doesn't rule options in or out, for example one about the game's career or salary paths.
- **q-14797** (kids-tv) I'm a glamorous star with blond hair, I do karate chops when I'm angry, and I'm madly in love with a green frog named Kermit. Who am I? → Miss Piggy: The description's “the star was always her” tells players the answer is female. Before any hint, that rules out Porky Pig and Fozzie Bear and leaves only Miss Piggy and Peppa Pig. Rewrite it to play on the diva or star theme without a gendered pronoun, for example: “Every show needs a star, and this one never lets anyone forget who it is.”
- **q-14803** (money-and-shopping) This building is printed on the back of the US $100 bill. In which city is it? → Philadelphia: Hint 2 ("It's in Pennsylvania") gives the answer away. Philadelphia is the only option in Pennsylvania, so hint 2 rules out all three wrong answers at once. Replace it with a medium-strength hint that doesn't name the state, for example that the US Constitution was written in this city. Media: every real $100 bill image still shows the small “INDEPENDENCE HALL” caption under the building. Candidate 5 is the cleanest choice, but the caption needs to be cropped out before the question is used.
- **q-14820** (nineteenth-century) Clara Barton brought bandages and food to Civil War field hospitals. Soldiers called her the “Angel of the…” → Battlefield: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-14821** (nineteenth-century) In 1864, Union General William T. Sherman led his “March to the Sea” across the state on this map. Which state is it? → Georgia: No candidate shows the outline map of Georgia that this essential slot needs. The sheet has tree silhouettes, a portrait silhouette, an Atlanta airport skyline, a beach, a nativity scene and a zoo sign. No new search is allowed, so the slot can't be filled. A search like "Georgia state outline map" or "Georgia blank map" on Commons should find one. The question text itself is fine. No suitable picture found for this question.
- **q-14823** (nineteenth-century) Cowboys worked outside all day, rode for hours across open land, and often had no roof nearby. Why did their hats have such wide brims? → To keep off sun and rain: The picked picture has an unsuitable licence (pd-us-only: PD-1923, PD-US-expired).
- **q-14832** (place-names) Leominster, Massachusetts, is said “LEM-in-ster,” was the birthplace of Johnny Appleseed, and was a plastics capital. Which lawn decoration was born there in 1957? → The pink flamingo: Hint 1 ("stuck in the grass on metal legs") gives the answer away: of the four options, only the pink flamingo stands on two metal-rod legs. Gnomes sit or stand on their own base, a gazing ball sits on a pedestal, and a pinwheel turns on one stick. Hint 1 should stay vague, for example by saying it was made by a local plastics company, without naming legs or a bird.
- **q-14841** (american-literature) Curious George, the little troublemaker who lives with the Man in the Yellow Hat, is this kind of animal. What is it? → A monkey: None of the media candidates shows a yellow wide-brim hat. They show natural straw hats at Thai markets, a historical rodeo photo, cotton harvest machines and an old cowboy portrait. The slot can't search again, so it needs a new search such as "yellow felt hat" or "yellow brimmed hat". No suitable picture found for this question.
- **q-14845** (cities-and-towns) Superman's home city, Metropolis, has a name from Greek that once meant “mother city.” What does “metropolis” mean today? → A very large, busy city: Hint 2 ("The word is about how big and important a city is, not where it is or what it's built from") almost states the answer and rules out the water and stone-walls options, which leaves only the king option. It should be replaced with a vaguer hint, for example one about the word's use in news or geography for places like Tokyo, but without saying "big".
- **q-14873** (kids-tv) Three of these shows come from Cartoon Network. Which one does NOT? → PAW Patrol: This overlaps draft q-14795, which names “PAW Patrol” as a Nick Jr. show. Anyone who has seen that question already knows PAW Patrol isn't on Cartoon Network, so it gives this answer away. Keep only one of the two, or change q-14795's list of example shows so it leaves out PAW Patrol.
- **q-14879** (money-and-shopping) At an American estate sale, often held after a family moves away, shoppers walk through the home and buy what? → The things inside the home: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-14891** (nineteenth-century) This woman escaped slavery in 1849 and went back many times to guide others to freedom. What was the secret escape network called? → The Underground Railroad: The wrong answer “The Liberty Line” is arguably also correct. Abolitionists used it as a nickname for the Underground Railroad, most famously in the 1844 “Liberty Line” cartoon ad in Chicago's Western Citizen. Replace it with a made-up name that was never linked to the network, for example “The Midnight Road”.
- **q-14912** (roads-and-landmarks) This glass crown with lights inside tops a skyscraper that opened in 2018, now the tallest in its city. Which city? → San Francisco: None of the candidates shows Salesforce Tower's crown, and the question needs that photo because it is essential media. 1 and 2 are Crown Tower in Warsaw, 3 and 5 are Iris Tower in Brussels, 4 is the Sydney skyline and 6 is a royal crown. No new search is allowed. Use a close-up of the Salesforce Tower crown with no skyline or landmarks in view. No suitable picture found for this question.
- **q-14930** (states-and-capitals) The capital of the US territory shown on this map is named after a saint. Which city is it? → San Juan: None of the candidates is a plain, unlabeled outline map of Puerto Rico, which this essential slot needs. Maps 3, 5 and 6 have inset maps labeled "San Juan", and map 4 is captioned "Island of Puerto Rico" and has town names. Photos 1 and 2 are not maps. A new search can't be run here, so the slot needs an unlabeled outline map, such as "Puerto Rico blank map" or a locator map. No suitable picture found for this question.
- **q-14931** (states-and-capitals) Which US state is shown on this map? → Michigan: None of the six candidates works. They are all 1890s–1910s county maps (Montmorency, Antrim, Clare, Gladwin), not an outline of the state, and each has "Michigan" printed in its title cartouche. No new search is allowed, so the essential image slot needs a plain, unlabeled outline map of Michigan from somewhere else, for example a blank Commons locator map of Michigan. No suitable picture found for this question.
- **q-14932** (states-and-capitals) The state on this map has Annapolis as its capital. What is its largest city? → Baltimore: No candidate works as the essential map. Candidates 1–3 are Maryland county maps with English labels that print "BALTIMORE" (and "Baltimore City" on 2), which gives the answer away. They also show "FREDERICK" and Annapolis. Candidates 4–6 are covered in Chinese county labels, not the plain unlabeled outline the note asks for. Since another search isn't allowed, the slot needs a plain Maryland outline or locator map without labels, or a change of role. No suitable picture found for this question.
- **q-14934** (states-and-capitals) You stand at the foot of Mount Rushmore and look up. About how tall is each president's face? → About 60 feet: The picked picture has an unsuitable licence (pd-us-only: PD-US).

## Question axes

- move: analogy 6, cause_effect 15, count 5, estimate 11, identify 39, made_of 14, name_concept 23, odd_one_out 11, origin 21, purpose 13, record 7, sequence 10, when 7, who 18, word_meaning 21
- stimulus: detail 9, map_outline 4, none 181, photo 26, video 1
- clue: completion 5, direct 84, riddle 28, scenario 27, three_facts 77
- answer_kind: group 25, number 19, person 30, place 34, thing 56, time 8, word 49
- lens: body_senses 5, educational_media 16, everyday 37, history 41, language 28, nature 14, pop_culture 54, popular_science 2, school 15, science_news 3, university 6

## Dropped by the pipeline

- american-literature-3: overlap like q-13940: In “The Wizard of Oz,” Dorothy clicks the heels of her ruby slippers and says: “There's no place like…” what? → Home: You want to get back to Kansas like Dorothy in “The Wizard of Oz.” How many times must you tap your heels together? → 3
- american-literature-10: overlap like q-9115: It's the biggest songbird in North America, and in an Edgar Allan Poe poem it only says “Nevermore.” Which bird is it? → Raven: You're flipping through a book of Henry Wadsworth Longfellow's poems. Which of these will you NOT find in it? → The Raven
- american-literature-15: overlap like q-11843: In Shel Silverstein's book “The Giving Tree,” the tree gives a boy its fruit to sell, its branches for a house and its trunk for a boat. What kind of tree is it? → An apple tree: In Shel Silverstein's book, I give a boy my apples, my branches and finally my trunk, and I'm still happy. Who am I? → The Giving Tree
- candy-and-snacks-0: overlap like q-1606: Adivina: tengo rayas, llevo un pañuelo rojo al cuello y en la caja de cereal digo '¡Son grrrandiosas!'. ¿Quién soy? → Tony el Tigre: I'm a big striped cat with a red bandana, and I've been selling sugar-frosted corn flakes since the 1950s. Who am I? → Tony the Tiger
- candy-and-snacks-3: overlap like q-12754: I'm a cool cat in sunglasses, my snack leaves orange dust on your fingers, and I like to say “It ain't easy being cheesy.” Who am I? → Chester Cheetah: This snack is made by pushing cornmeal through a hot machine so it puffs up, then coating it in bright orange cheese powder. What is it? → Cheetos
- candy-and-snacks-12: overlap like q-2925: He's the round, cheerful yellow M&M's character. What is inside him? → A peanut: In M&M's ads, Red is the bossy one, and Yellow is the sweet, goofy one who's bigger and lumpier. What's inside Yellow? → A peanut
- cities-and-towns-2: overlap like q-9091: In 1992 I won Olympic gold in Barcelona with the “Dream Team.” I won six NBA titles and was named Finals MVP every time. Who am I? → Michael Jordan: You're watching “The Last Dance”: the Chicago Bulls' star left to play baseball, then came back and won three more titles. Who was he? → Michael Jordan
- cities-and-towns-6: overlap like q-5031: Fundé el estudio que hizo 'Encanto', la película de la familia Madrigal, y mi nombre sale al comienzo con un castillo. ¿Quién soy? → Walt Disney: You're walking into Disneyland in California, the very first Disney park. Who dreamed it up and opened it? → Walt Disney
- college-sports-2: overlap like q-7115: Estás jugando ponchados en el recreo y tienes el balón en la mano. ¿Para qué lo lanzas? → Para sacar a un rival: In this gym-class game, what are you trying to do with the ball? → Hit a player on the other team
- college-sports-6: overlap like q-10540: Texas A&M quarterback Johnny Manziel was the first freshman ever to win the Heisman Trophy. In which year? → 2012: Tim Tebow played quarterback at Florida and made kneeling in prayer famous. In 2007, he became the first sophomore to win which award? → The Heisman Trophy
- college-sports-14: overlap like q-1174: Adivinanza: soy un valle de California donde nacieron empresas como Apple y Google, y en inglés me llaman 'Silicon Valley'. ¿Qué material esconde mi nombre? → Silicio: This tech region south of San Francisco grew up around Stanford University, and Stanford students started Google there. What is the region called? → Silicon Valley
- cryptids-and-ufos-4: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: When aliens in old American sci-fi movies talk about “Earthlings,” who do they mean? → People from Earth
- cryptids-and-ufos-17: overlap like q-5961: I'm round and flat like a dinner plate, I spin and zoom through the sky, and cartoon aliens fly me. What am I? → A flying saucer: In 1947, an American pilot saw nine shiny objects zooming across the sky. Newspapers gave these mystery objects a famous name. What was it? → Flying saucers
- fairs-and-festivals-1: overlap like q-12761: A marching band like this one performs on the field during a break in the middle of a football game. What is that break called? → Halftime: At an American high school football game, when does the marching band put on its big show on the field? → At halftime
- fairs-and-festivals-12: overlap like q-9381: Wie heißt dieses Fahrgeschäft? → Riesenrad: I'm a giant wheel at the fair. You sit in my little cars, I turn slowly, and from my top you can see far away. What am I? → A Ferris wheel
- family-and-school-traditions-1: overlap like q-3404: I'm a sour yellow fruit. Squeeze me, add water and sugar, and you get a cool summer drink. What fruit am I? → Lemon: On hot summer days, American kids sell cups of this drink at little stands on the sidewalk. What is it? → Lemonade
- family-and-school-traditions-4: overlap like q-12920: In 2019, the Scripps National Spelling Bee ran out of words hard enough and crowned several co-champions. How many? → 8: You're on stage at an American spelling bee. You may ask the judges about your word, but what are you NOT allowed to ask? → How to spell it
- holidays-2: overlap like q-10037: En Pascua, muchos padrinos regalan una mona con huevos encima. ¿De qué suelen ser hoy esos huevos? → De chocolate: Kids find bunnies like this one in their Easter basket. What is this bunny made of? → Chocolate
- holidays-4: overlap like q-5372: Which country do decorated sugar skulls like this one come from? → Mexico: Many families in the US decorate with sugar skulls like these for the Day of the Dead. Which country does this holiday come from? → Mexico
- holidays-11: overlap like q-8853: Every Thanksgiving, the US president “pardons” a turkey at the White House. Where does the bird usually go next? → To a farm to live out its life: You watch the President pardon a turkey before Thanksgiving. Where does that turkey go next? → To a farm
- holidays-15: overlap like q-2334: I'm a party balloon, and if you let go of my string, I float up to the sky. What gas am I filled with? → Helium: Giant balloons like this one float through New York in the Thanksgiving parade. What gas keeps them up? → Helium
- holidays-17: overlap like q-8848: Every July 4, Americans light up the night sky like this. Whose birthday are they celebrating? → The United States: Americans watch big summer shows like this one to celebrate their country's birthday. Which day is it? → The Fourth of July
- household-brands-16: overlap like q-4181: Johnson's golden baby shampoo is made for babies and gentle on their eyes. Its famous promise is “No more…” what? → Tears: Johnson's Baby Shampoo famously promised that if it got in a baby's eyes, there would be “no more…” what? → Tears
- inventors-and-founders-3: overlap like q-10613: For about 70 years, a bottle of Coca-Cola cost exactly one of these coins. In which US city was the drink invented, in 1886? → Atlanta: I'm a big Southern city. In 1886, a pharmacist named John Pemberton mixed up a famous cola syrup here, and I later hosted the Olympics. Which city am I? → Atlanta
- inventors-and-founders-16: overlap like q-2650: A filter like this cuts glare from water and windows. The man who invented cheap polarizing plastic sheets later founded a famous instant-camera company. Who? → Edwin Land: In 1943, Edwin Land's 3-year-old daughter asked why she couldn't see a photo right away. Her question led him to invent what? → The instant camera
- kids-tv-1: overlap like q-13889: You're watching an old Looney Tunes cartoon and it's ending. Who bursts out of a drum to stutter “That's all, folks!”? → Porky Pig: At the end of many Looney Tunes cartoons, Porky Pig stutters a famous goodbye. Complete it: “That's all, ___!” → Folks
- kids-tv-2: overlap like q-5763: In Disney's “Descendants”, the heroes are the children of famous villains. Which villain is the mother of the main heroine? → Maleficent: In Disney Channel's “Descendants” movies, Mal is the purple-haired daughter of which famous villain? → Maleficent
- kids-tv-8: overlap like q-3366: In “Dora the Explorer”, what kind of animal is Swiper, the sneaky thief? → A fox: I'm a sneaky animal with a blue mask. I try to steal things from Dora, but she stops me by saying “Swiper, no swiping!” three times. What animal am I? → A fox
- kids-tv-11: overlap like q-2719: “I live in a pineapple under the sea, and I work at the Krusty Krab.” What is my job called? → Fry cook: SpongeBob jumps out of bed shouting “I'm ready! I'm ready!” before rushing to work. At which restaurant does he work? → The Krusty Krab
- money-and-shopping-1: overlap like holidays-17: Americans watch big summer shows like this one to celebrate their country's birthday. Which day is it? → The Fourth of July: US stores hold huge summer sales, towns light up the sky, and families have cookouts to mark the year 1776. Which holiday is it? → The Fourth of July
- money-and-shopping-10: overlap like q-2892: Whose portrait is on the front of the US one-dollar bill? → George Washington: I led an army, I became the first president of the United States, and my face is on the one-dollar bill. Who am I? → George Washington
- movie-favorites-6: overlap like q-0075: En 'Toy Story', ¿cómo se llama el vaquero? → Woody: I'm a toy cowboy with a pull string in my back, and I belong to a boy named Andy. When people leave the room, I come to life. Who am I? → Woody
- movie-favorites-7: overlap like q-4932: In Lilo's home, Hawaii, visitors get a gift made of flowers, worn around the neck, as a welcome. What is it called? → A lei: In “Lilo & Stitch,” Stitch escapes from space in a stolen ship. Where does he crash-land on Earth? → Hawaii
- movie-favorites-8: overlap like q-6399: In the movie Frozen, who sings “Let It Go”? → Elsa: In the movie “Frozen,” who is the older of the two royal sisters? → Elsa
- movie-favorites-13: overlap like q-1060: ¿Cómo se llama el anciano de la película de Pixar que amarra miles de globos a su casa? → Carl Fredricksen: I'm a grumpy old man. I tied thousands of balloons to my house and flew it to South America, with a young scout stuck on my porch. Who am I? → Carl Fredricksen
- movie-favorites-14: overlap like q-2779: Spider-Man shoots webs, as Captain America throws his… → Shield: In “The Avengers,” Thor is to his hammer as Captain America is to his… → Shield
- movie-favorites-15: overlap like q-3615: Which kind of animal does NOT appear in “Finding Nemo”? → Penguin: Which of these animals is NOT a character in Disney's “The Lion King”? → A penguin
- national-symbols-2: overlap like q-2363: Besides stripes, which shape appears 50 times on this flag? → Stars: This close-up shows part of a famous flag. Which flag is it? → The US flag
- national-symbols-7: overlap like q-2893: This man is Alexander Hamilton, the first US Treasury Secretary. He was never president, yet his face is on a US banknote. What is its value? → $10: Alexander Hamilton, the face on the $10 bill, was the first person in this job. He set up a national bank, and his department still makes US money. What job? → Secretary of the Treasury
- nineteenth-century-4: overlap like q-2432: “I'm a code of dots and dashes, and I carry my American inventor's name.” Who was he? → Samuel Morse: This American painter and inventor created a code of dots and dashes for sending messages by telegraph. Who is he? → Samuel Morse
- nineteenth-century-14: overlap like q-3356: Almost every Wild West town had a building like this one. What was it mainly used for? → Drinking, card games and meeting people: My swinging half-doors flap open when a cowboy walks in. Inside, someone plays the piano and people play cards. What am I? → A saloon
- nineteenth-century-17: overlap like q-10700: Look at this coin. How many cents is it worth? → 1: Abraham Lincoln's face is on the US penny. How many pennies make one dollar? → 100
- place-names-2: overlap like q-8863: The Continental Army spent the freezing winter of 1777–78 in huts like these at Valley Forge. Who was its commander? → George Washington: Dozens of US towns are named Lafayette to honor a young French noble. Under which commander did he fight in the American Revolution? → George Washington
- place-names-13: overlap like q-3621: Which Pixar character moves with her family to the city with the bridge in this photo? → Riley: In Pixar's “Inside Out,” Riley moves from Minnesota to the “Bay Area.” Which bay gives the area its name? → San Francisco Bay
- regional-dishes-1: overlap like q-8848: Every July 4, Americans light up the night sky like this. Whose birthday are they celebrating? → The United States: Families grill hot dogs and watch fireworks like these on the Fourth of July. Whose birthday does the holiday celebrate? → The United States
- regional-dishes-2: overlap like q-8993: Breaux Bridge, a Cajun town in Louisiana, calls itself the world capital of which food? → Crawfish: Cajun seasoning like this, a spicy mix of paprika, cayenne and garlic, comes from the cooking of which state? → Louisiana
- regional-dishes-4: overlap like q-8972: Tostitos get their name from the Spanish word for “toasted.” What kind of chips are they? → Tortilla chips: What do you call the crunchy, triangle-shaped chips that people dip in salsa? → Tortilla chips
- regional-dishes-8: overlap like q-7776: Estás almorzando un corrientazo y al lado del arroz viene ensalada de repollo rallado. ¿Qué verdura naranja suele ir revuelta con el repollo? → La zanahoria: Coleslaw came to America with Dutch settlers, it's a cool side at barbecues, and it's mostly cabbage. Which orange vegetable is often shredded in? → Carrot
- regional-dishes-13: fact-check wrong: Fun fact is wrong: Juvencio Maldonado was a Mexican-born restaurateur in Los Angeles, not New York. The 1947 patent filing is correct. I did not run a search, so this comes from memory.: It's shaped like a U, it's fried until it's hard and crunchy, and you fill it with meat and cheese. What is a hard taco shell made from? → Corn
- regional-dishes-14: overlap like q-4776: This V-shaped bone in a bird's chest forms when two collarbones join, and it bends like a spring as the bird flaps. What is it called? → The wishbone: I'm a Y-shaped bone from the Thanksgiving turkey. After dinner, two people pull on me, and whoever gets the bigger piece gets good luck. What am I? → The wishbone
- regional-dishes-16: overlap like q-10339: Estas empanadas de las costas de Sinaloa y Nayarit van rellenas de camarón. ¿A qué grupo de animales pertenece el camarón? → Crustáceos: Crawfish, the stars of a Louisiana crawfish boil like this one, belong to which group of animals? → Crustaceans
- regional-dishes-17: overlap like q-13832: Look at the photo: this hot, creamy corn dish is a breakfast classic in which part of the US? → The South: Unripe tomatoes, sliced, coated in cornmeal and fried like these, are best known as a dish from which part of the US? → The South
- restaurant-chains-2: overlap like q-3670: You're looking at a Domino's pizza box. How many dots are on the domino in its logo? → 3: Look at the photo. Which pizza chain is named after this game piece? → Domino's
- restaurant-chains-16: overlap like q-1147: Mi cara, con traje blanco y barbita de chivo, sale en baldes de pollo frito. ¿Qué estado de EE. UU. lleva mi cadena en su nombre? → Kentucky: I have a white suit, a black bow tie, glasses and a white beard. My face is on buckets of fried chicken. Who am I? → Colonel Sanders
- college-sports-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: US high school football has no official national champion. What is usually the top title a team can win? → A state championship
- twentieth-century-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: I'm a piece of paper Americans bought in World War II to lend money to the government, which paid them back later with interest. What am I? → A war bond
- wildlife-8: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 5: Winter, a bottlenose dolphin in Florida, was badly hurt in a crab trap as a baby and later starred in a 2011 movie. What did people build to help her swim? → An artificial tail
- fairs-and-festivals-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In the Macy's Thanksgiving Day Parade in New York, who rides on the very last float? → Santa Claus
- holidays-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: I'm a tiny, chalky candy in pastel colors, with short words like “BE MINE” printed on me. What am I? → Conversation hearts
- household-brands-14: fact-check wrong: The answer (1980s) is right, but the third hint is shaky. Wikipedia and Retro Network date the first Energizer Bunny ad to Oct 30, 1988, which is well before the Berlin Wall fell in Nov 1989. Other sources say 1989.: The drum-banging Energizer Bunny, who “keeps going and going,” first appeared on US TV in which decade? → The 1980s
- inventors-and-founders-4: overlap like q-8020: Es una empresa nacida en Medellín en 1949 y su logo es amarillo. ¿Qué es el Éxito? → Una cadena de almacenes: Walmart has blue signs with a yellow spark and thousands of locations across America. What kind of business is it? → Store chain
- inventors-and-founders-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Heinz comes from Pittsburgh, puts a “57” on its glass bottles, and sells more of one sauce than any other brand in America. Which sauce? → Ketchup
- kids-tv-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In “Adventure Time,” he has a long white beard, a magic crown that gives him powers, a penguin named Gunter, and keeps kidnapping princesses. Who is he? → The Ice King
- money-and-shopping-5: overlap like q-13812: The Salvation Army sells donated clothes and furniture in its thrift stores. What does the money mainly pay for? → Programs helping people beat addiction: Goodwill runs thousands of these stores in the US, and the British call them charity shops. What do they mostly sell? → Used things people gave away
- more-sports-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In 2021, Bubba Wallace became the first Black driver since 1963 to win a race at the top level of which kind of racing? → NASCAR
- more-sports-12: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Its NHL team, nicknamed the “Broad Street Bullies,” won the Stanley Cup in 1974, the first team from the 1967 expansion to do so. Which city? → Philadelphia
- movie-favorites-10: overlap like q-0315: ¿Qué villano le dice a Luke Skywalker la famosa frase: 'Yo soy tu padre'? → Darth Vader: I breathe loudly through my black mask and fight with a red lightsaber. Who am I? → Darth Vader
- movie-favorites-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In 1993, Disney started a real NHL team named after its movie “The Mighty Ducks.” Which Southern California city became its home? → Anaheim
- place-names-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I'm the southern tip of Illinois. My town of Cairo, said “KAY-roh,” sits where the Ohio meets the Mississippi, and I also have a Thebes. What's my nickname? → Little Egypt
- place-names-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Many US states are named after Native American peoples. Which of these peoples does NOT have a state named after it? → The Cherokee
- regional-dishes-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In New Mexico, if you order your enchiladas with both red and green chile sauce, like this, what one word do you say? → Christmas
- regional-dishes-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Red-eye gravy is a Southern breakfast sauce made from country ham drippings and which drink? → Black coffee
- regional-dishes-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It was created in Baltimore in 1939 and comes in a yellow and blue can. What is Old Bay? → A spice blend
- restaurant-chains-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Pizza Hut's logo shows one red part of a building, and its classic restaurants had a huge one. Which part? → The roof
- roads-and-landmarks-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I'm a long avenue in Washington, D.C. Presidents parade along me after taking office, and the White House's address is on me. What am I? → Pennsylvania Avenue
- roots-and-soul-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Breakdancers in 1980s New York carried boomboxes, big stereos with handles, on their shoulders. Why did dancers love them? → They played music anywhere outside
- roots-and-soul-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: What makes a rap “freestyle” different from a normal rap song? → The words are made up on the spot
- school-life-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: You're in an American classroom and a wad of chewed paper flies out of a straw and hits your neck. What is it called? → A spitball
- school-life-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In an American school, a teacher says “Go to the principal's office!” What does it usually mean? → You're in trouble
- states-and-capitals-7: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: You're landing in Los Angeles. What does the city's Spanish name mean in English? → The Angels
- states-and-capitals-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In Yosemite National Park, climbers scale a giant granite wall called El Capitan. What does its Spanish name mean? → The Captain
- roads-and-landmarks-11: overlap like cities-and-towns-6: You're walking into Disneyland in California, the very first Disney park. Who dreamed it up and opened it? → Walt Disney: This old-time street greets visitors at the entrance of a famous theme park. Whose childhood hometown inspired it? → Walt Disney
- roads-and-landmarks-16: overlap like q-11762: Paul Bunyan, the giant of American tall tales, swings his huge axe all day. What is his job? → Lumberjack: This giant roadside statue in Minnesota shows a hero from American tall tales. What kind of worker was he? → A lumberjack
- roots-and-soul-4: overlap like q-4402: At a breaking battle: headspin is to the head as windmill is to the…? → Upper back and shoulders: I'm a breakdance move. Dancers wear a cap and turn me round and round while upside down, balancing on the top of the head. What am I? → Headspin
- roots-and-soul-15: overlap like q-8843: The record label Motown is named after its city's nickname “Motor Town,” thanks to its car factories. Which city? → Detroit: This Detroit house was the first home of Motown Records. Which two words blend to make the name “Motown”? → Motor and Town
- roots-and-soul-17: overlap like q-5607: Listen: which instrument is playing? → Bass guitar: Listen: Bootsy Collins played this instrument for James Brown and George Clinton. What is it? → Bass guitar
- school-life-4: overlap like q-1575: Cuando se halló grafito en Inglaterra en el siglo XVI, se creyó que era un metal. ¿Cuál, que todavía da nombre al lápiz en inglés? → Plomo: For decades, American tests told students to bring a “No. 2 pencil.” Which of these is NOT true about it? → Its core is made of real lead
- school-life-12: duplicate like q-5975: This hat is a famous symbol of which country? → United States: These crunchy chicken bites are a school lunch favorite. In which country were they invented? → The United States
- states-and-capitals-4: overlap like q-10720: This state's flag has one white star on a blue stripe next to white and red stripes. It was once its own country. Which state is it? → Texas: This state's flag is called the Lone Star Flag. Which state is shown on this map? → Texas
- states-and-capitals-8: overlap like q-2363: Besides stripes, which shape appears 50 times on this flag? → Stars: Each star on this flag stands for one US state. How many stars are there? → 50
- states-and-capitals-10: overlap like q-9060: Which river carved the canyon in this photo? → Colorado River: A chisel is to a statue as what is to the Grand Canyon? → A river
- twentieth-century-0: overlap like q-3102: I'm a giant marble statue of a seated man in Washington, D.C. Martin Luther King Jr. gave his “I Have a Dream” speech on my steps. Who do I show? → Abraham Lincoln: In 1963, Martin Luther King Jr. gave his “I Have a Dream” speech on the steps of which monument? → The Lincoln Memorial
- twentieth-century-1: overlap like q-1382: ¿En qué década inventaron los hermanos Kellogg las hojuelas de cereal que hoy llamamos corn flakes? → Los años 1890: Brothers John Harvey and Will Keith Kellogg first made their famous corn flakes in Battle Creek, Michigan. When? → Around 1900
- twentieth-century-5: overlap like q-2639: When Martin Luther King Jr. won the 1964 Nobel Peace Prize, he was the youngest winner of that prize so far. How old was he? → 35: I helped lead the bus boycott in Montgomery, Alabama, and in 1964 I won the Nobel Peace Prize at age 35. Who am I? → Martin Luther King Jr.
- twentieth-century-10: overlap like q-12788: Before World War II, the cream filling inside Twinkies tasted of which fruit? → Banana: Twinkies were invented in 1930 with a different filling. A shortage during World War II made the company switch to vanilla cream. What was the first filling? → Banana cream
- twentieth-century-12: overlap like q-6287: Peter Pan lives in Neverland, and the name says it all: children there never do one thing. What is it? → Grow up: Michael Jackson's California ranch had a zoo, a train and fair rides. It was named after the island where Peter Pan lives. What was it called? → Neverland
- twentieth-century-14: overlap like q-13721: In which year did Jackie Robinson first play for the Brooklyn Dodgers, breaking Major League Baseball's color line? → 1947: In 1947, I became the first Black player in modern Major League Baseball, for the Brooklyn Dodgers. Who am I? → Jackie Robinson
- twentieth-century-17: overlap like q-9139: Sie ist rosa oder weiß, wird auf dem Jahrmarkt um ein Holzstäbchen gewickelt und schmilzt im Mund. Wie heißt sie? → Zuckerwatte: Where do kids in America usually buy this fluffy treat? → At a fair
- wildlife-1: overlap like q-5345: The Ford Mustang's badge shows a mustang, a wild horse of North America. Where did today's mustangs come from? → Horses brought by Spanish explorers: Wild horses like these still run free in the American West. Who brought their ancestors to the Americas about 500 years ago? → Spanish explorers
- wildlife-4: overlap like q-3148: This big bird comes from the Americas, and many families roast it for big holiday feasts. What is it? → Turkey: This close-up shows the wrinkly red head of a big wild bird from North America. Which bird is it? → Turkey
- wildlife-11: overlap like q-0457: Escucha: ¿qué animal hace este sonido grave? → Una rana toro: It's the biggest frog in North America. Its deep call sounds like a farm animal, and that animal is in its name. Which frog is it? → Bullfrog
- wildlife-13: duplicate like q-2380: Which continent is shown in this satellite photo? → North America: This is an eastern chipmunk. On which continent does it live in the wild? → North America
