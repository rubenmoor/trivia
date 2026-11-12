# batch-56

Made by `qgen batch` on 2026-11-11 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): place-names, folk-heroes-and-tall-tales, hosts-and-game-shows, money-and-shopping, household-brands, national-parks, more-sports, sayings-and-idioms, nineteenth-century, roads-and-landmarks, fairs-and-festivals, winter-holidays, states-and-capitals, roots-and-soul, weather-and-seasons, words-and-slang, family-and-school-traditions, restaurant-chains, cryptids-and-ufos, traditional-songs, trailblazers, school-life, childrens-books, native-nations, american-football
- Merged: 239 (q-16620…q-16858)
- Approved: 208
- Needs work: 31
- Dropped by the pipeline: 70
- Reviewed by: claude-opus-5-5
- Claude calls: 522, about $67.84 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-54, batch-55; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-54 | batch-55 | batch-56 |
|---|---|---:|---:|---:|
| source locale |  | es-ES | es | en |
| drafts |  | 331 | 312 | 309 |
| skipped slots |  | 155 | 210 | 141 |
| dropped |  | 87 | 104 | 70 |
| drop rate | ≤ 20.0 % | 26.3 % ✗ | 33.3 % ✗ | 22.7 % ✗ |
| dropped: hard fail correct |  | 1 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 2 | 0 |
| dropped: hard fail no_giveaway |  | 15 | 23 | 20 |
| dropped: overlap |  | 69 | 78 | 49 |
| dropped: duplicate |  | 2 | 1 | 1 |
| dropped: fact-check wrong |  | 0 | 1 | 0 |
| merged |  | 244 | 208 | 239 |
| approved |  | 228 | 189 | 208 |
| needs_work |  | 16 | 19 | 31 |
| needs_work rate | ≤ 20.0 % | 6.6 % ✓ | 9.1 % ✓ | 13.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.6 % ✓ | 1.9 % ✓ | 1.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.8 % ✓ | 1.4 % ✓ | 0.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.4 % ✓ | 3.8 % ✗ | 2.5 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.1 % ✓ | 2.9 % ✓ | 8.4 % ✓ |
| media: no pick in review 1 |  | 43 | 28 | 33 |
| media: recovered by research |  | 36 | 24 | 22 |
| media: no pick at record |  | 9 | 5 | 11 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.5 % ✓ | 0.4 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 21.8 % ✗ | 27.9 % ✗ | 18.1 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 59.2 % ✓ | 55.7 % ✓ | 79.4 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.50 ✓ | 1.00 ✓ | 1.56 ✗ |
| approved 11–15 |  | 44 | 46 | 38 |
| top move | ≤ 25.0 % | 15.2 % ✓ | 16.8 % ✓ | 13.8 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 79.9 % | 86.5 % | 81.6 % |
| values stimulus |  | 4 | 4 | 6 |
| top clue | ≤ 60.0 % | 43.9 % ✓ | 37.0 % ✓ | 36.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 20.5 % ✓ | 21.6 % ✓ | 22.6 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 17.6 % ✓ | 18.3 % ✓ | 21.3 % ✓ |
| values lens |  | 9 | 10 | 11 |
| media share | 15.0 %–50.0 % | 20.1 % ✓ | 13.5 % ✗ | 18.4 % ✓ |
| mean fun | ≥ 3.40 | 3.47 ✓ | 3.37 ✗ | 3.51 ✓ |
| cost $ |  | $76.96 | $67.44 | $64.59 |
| $ per approved | ≤ $0.35 | $0.34 ✓ | $0.36 ✗ | $0.31 ✓ |
| calls |  | 505 | 424 | 462 |
| calls per approved |  | 2.21 | 2.24 | 2.22 |
| wall time h |  | 1.89 | 1.96 | 1.90 |
| days |  | 2 | 4 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 52 (4 %)
- Major among review needs work: 4 of 8 (50 %)
- Problems by kind: giveaway 9 (1 major), fact 2 (0 major), ambiguity 2 (1 major), overlap 1 (1 major), media 6 (6 major), difficulty 2 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 54 of 60 (90 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.24

Major findings on approved questions:

- **q-16684**: media — The image is essential, since the question says "Look at this stick with a net pocket", but the file picked is "File:Peter Profile Picture.jpg". That is almost certainly someone's profile photo, not a lacrosse stick, so the question doesn't work on screen without it. The facts hold up: lacrosse came from Native nations of the Northeast and Great Lakes, French Jesuits named it in the 1630s, the Haudenosaunee call it "the Creator's Game", and early games had hundreds of players on very long fields. The difficulty of 7 seems right. (http://127.0.0.1:8001/review/q-16684)
- **q-16788**: media, giveaway — The illustrative image's title is "US Route 1 Sign Florida Keys". It points straight at the Keys, which rules out Miami, Jacksonville and Fort Lauderdale, and the picture itself probably shows the Keys' bridges and water, so it gives away Key West. The facts check out: Route 1 runs from Fort Kent, Maine, to Mile 0 in Key West, and it is about 2,370 mi (3,810 km) long. Hint 2 (the chain of bridges and islands) already narrows the options to Key West, but that is only a minor issue, and the question doesn't overlap with the I-95/Miami question. (http://127.0.0.1:8001/review/q-16788)

## Needs work

- **q-16623** (american-football) Look at the white laces on this football. What do they mostly help with? → Gripping and throwing the ball: No candidate shows what this essential image needs: a clear photo of an American football with its white laces. 1 and 2 are scans of players lining up from a 1902 book, and 3 is a silver matchsafe shaped like a ball with no clear laces. No new search is allowed, so the media slot needs a proper photo of the laces (for example from "football laces close up"). No suitable picture found for this question.
- **q-16640** (fairs-and-festivals) At the Minnesota State Fair, big stars play concerts in front of huge rows of tiered seats facing the stage. What are those seats called? → The grandstand: Overlap with approved q-12779, whose question text reads "American fairgrounds usually have barns for animals, a grandstand for shows, and a 'midway.'" It names this answer and one of its wrong options, so seeing one question gives the other away. Drop this question or replace it with a different fair fact.
- **q-16641** (fairs-and-festivals) In rodeo barrel racing, a rider and horse race around barrels against the clock. Which of these is NOT part of the event? → A lasso for roping: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-16650** (folk-heroes-and-tall-tales) This old print shows young George Washington and the cherry tree. Which writer made up that story and added it to his book about Washington in 1806? → Parson Weems: None of the candidates shows the old print of young Washington and the cherry tree that the question names ("This old print shows…"). They are all Washington, D.C. cherry blossom photos plus a Childe Hassam sketch. A new search isn't allowed. Source a public-domain print by hand (e.g. the Currier & Ives "Father, I cannot tell a lie" lithograph or John C. McRae's 1867 engraving), or reword the question so it doesn't name the print and use an illustrative image. No suitable picture found for this question.
- **q-16651** (folk-heroes-and-tall-tales) The pirate Blackbeard got his nickname from his big, bushy black beard. About how long ago did he sail the seas? → About 300 years ago: This asks the same fact as approved q-5969 ("Real pirates flew the skull-and-crossbones flag in the Caribbean about how long ago?" → About 300 years ago). Blackbeard is the best-known pirate of that same golden age, with the same answer and the same options, so whichever one players see first gives away the other.
- **q-16661** (hosts-and-game-shows) This is “Boston Rob” Mariano. How many different seasons of Survivor did he play as a contestant? → 5: None of the image candidates shows Boston Rob Mariano, and no new search is allowed. The question says "This is “Boston Rob” Mariano," so it needs a real photo of him. Find a usable portrait (for example on Commons under "Rob Mariano"), or reword the question so it doesn't point at a photo and use an illustrative image such as a Survivor-style beach camp. No suitable picture found for this question.
- **q-16664** (household-brands) Around 2013, millions of kids had this plastic board with rows of pegs. What did they make on it? → Rubber band bracelets: The essential image slot has no candidates, and no new search is allowed. The question needs a clear photo of an empty Rainbow Loom pegboard. Either find one by hand, or change the media to an illustrative image that doesn't show bracelets, for example "plastic pegboard toy". No suitable picture found for this question.
- **q-16667** (household-brands) In this classic game, you call out spots like “B-4” to find hidden ships. What does a white peg mean? → A miss: None of the six candidates shows Battleship. They are other Milton Bradley products (Blitz, the Milton talking game, Hands Down, Comp IV) and two baseball photos of a player named Milton Bradley. I can't search again, so the essential slot can't be filled. The question doesn't really need an essential image. Switching the slot to illustrative or decorative, with a query like "battleship game pegs" or "naval grid map", would likely solve it. No suitable picture found for this question.
- **q-16678** (native-nations) The Lakota “winter count” was painted on an animal hide, gained one picture every year, and its keeper could explain each one. What was it for? → Remembering each year's big event: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-16681** (native-nations) Three of these Disney heroines are made up. Which one was a real person? → Pocahontas: This overlaps approved q-12813. That question opens with "Disney's “Pocahontas” is loosely based on history", which is exactly the fact this question asks. A player who has seen q-12813 already knows that Pocahontas is the real person. The rest checks out: the facts are correct, the three wrong answers are clearly made up, and there's no giveaway.
- **q-16689** (nineteenth-century) You're on a Texas ranch, watching a man in boots and a wide hat round up cattle on horseback. What is he called? → A cowboy: This overlaps too much with approved q-4934 (“This hat has a very wide brim, ranchers in the Wild West wore it, and Woody from Toy Story has one” → A cowboy hat). Once a player has seen that answer, this question is already solved, and both use the same Woody hint. Drop this question or swap in a different Wild West topic.
- **q-16694** (place-names) Puyallup, Washington, said “pew-AL-up,” is named after a Native people. What is the name said to mean? → Generous people: Hint 2 ("describes how the tribe treated visitors who came to their land") gives the answer away: only "Generous people" describes how people behave, while the three wrong options are all landscape features. Hint 2 needs to be vaguer, for example a hint that the name is about the people rather than the land, or about the river bend in its literal sense.
- **q-16715** (trailblazers) Rebecca Lee Crumpler became the first Black woman doctor in the US in 1864. After the Civil War she moved to Richmond, Virginia. Whom did she go there to care for? → Formerly enslaved people: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-16717** (weather-and-seasons) Many Great Plains towns have a loud siren on a tall pole and test it at noon once a month. What does it mainly warn about? → Tornadoes: This overlaps approved q-9098 in the same subcategory. Its text says “a twister has been spotted… so sirens wail and you take cover,” which already tells players that the sirens warn about tornadoes, the exact fact this question asks. Drop this question, or replace it with a different fact about tornado sirens or the Great Plains.
- **q-16718** (weather-and-seasons) On the Great Plains, doors like these in the yard lead to a small underground room. What is it called? → A storm cellar: No candidate shows the slanted double doors of an underground storm cellar, and the question depends on that photo ("doors like these"). A new search can't be run here. A query like "storm cellar doors" or "root cellar doors farm" should find a usable Commons photo. No suitable picture found for this question.
- **q-16726** (childrens-books) I was born on March 2, 1904, in Springfield, Massachusetts. For years, US schools held Read Across America Day on my birthday. Who am I? → Dr. Seuss: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-16742** (hosts-and-game-shows) In Wheel of Fortune's bonus round, the player is given R, S, T, L, N and E for free. What do these letters have in common? → They are among the most common letters in English: This new draft asks "What do these letters have in common?", and the 2026-10-21 rule bans that style for new drafts. None of the media candidates fit the question either: they are scans of old Bodleian game booklets and a newspaper column, and a new search isn't allowed. No suitable picture found for this question.
- **q-16743** (household-brands) In 1859, a young chemist saw workers rubbing a waxy goo on their cuts, and Vaseline was born. What is Vaseline made from? → Crude oil: None of the media candidates fits. Two are scans of handwritten 1840 letters, and one is an X-ray of a hand from a 1916 remedies book. A new search isn't allowed, so the slot needs a manual media choice. One idea is an 1860s Pennsylvania oil derrick (Titusville): it shows the setting but doesn't name the answer, and crude oil is already the answer, so it may need to be decorative and blurred. Another is a plain jar of petroleum jelly with no label. No suitable picture found for this question.
- **q-16748** (money-and-shopping) Starting in 1999, the US Mint made one quarter design for each of the 50 states. How many years did that take? → 10: The picked picture has an unsuitable licence (pd-no-reason: public domain without a template).
- **q-16762** (place-names) Prague, Oklahoma, said “PRAYG,” was founded by Czech settlers and holds a yearly Kolache Festival. What is a kolache? → A fruit-filled sweet bun: No candidate shows Prague, Oklahoma. They show Oklahoma City (1, 2, 4), Enid (3, 5) and Yukon (6, with "Yukon Mills" signs). The question names the town, so the picture has to be of it, and there are no searches left. The text itself is fine. No suitable picture found for this question.
- **q-16763** (place-names) Sequim, said “SKWIM,” is on the same peninsula as Forks, the rainy “Twilight” town, yet gets only about 16 inches (410 mm) of rain a year. Why? → A rain shadow from mountains: Hint 1 gives the answer away. It names the Olympic Mountains standing between Sequim and the Pacific, and "A rain shadow from mountains" is the only option that mentions mountains. Hint 1 is also stronger than hint 2, so the hints run in the wrong order. Hint 1 should become a vague hint (for example about the weather or the wind, without mountains), and the mountains should move to a later hint.
- **q-16765** (roads-and-landmarks) In Washington, D.C., 19 steel soldiers in ponchos walk through bushes. Reflected in a polished granite wall, they become 38. What does 38 stand for? → The line that divided Korea: No candidate shows the Washington, D.C. Korean War Veterans Memorial soldiers and wall the question names. Most are of the UN Memorial Cemetery in Busan or the museum in Seoul. #3 shows the D.C. site with the soldiers edited out, and its "1950 • KOREA • 1953" inscription rules out the "weeks" option. No new search is allowed, so the media slot needs a manual fix, for example a photo of the steel soldiers reflected in the granite wall. No suitable picture found for this question.
- **q-16768** (roads-and-landmarks) New York's Park Avenue is famous for fancy apartments. Its flower-filled middle strip was built to cover what? → Train tracks: Fact check: uncertain. The 1888 renaming detail isn't verified. Park Avenue's naming was done in stages, with some sections renamed earlier. The railroad-cover answer is correct.
- **q-16770** (sayings-and-idioms) Americans “stake a claim” when they grab something first. Gold miners and settlers did it for real with wooden posts. In which century? → The 1800s: This overlaps too much with approved q-10581, which asks in which century the California Gold Rush happened (the 1800s). Here the clue "gold miners" and hint 3 ("The California Gold Rush started in 1848") make it the same fact asked again, so each question gives away the other. Rewording can't fix this because the phrase's origin is tied to the gold rush era.
- **q-16772** (sayings-and-idioms) “Top banana,” meaning the boss, began as a name for the lead comic in American stage comedy. In which century did it appear? → The 1900s: The picked picture has an unsuitable licence (pd-us-only: PD-US-architecture).
- **q-16776** (school-life) In US high schools, the homecoming dance usually comes right after a big home game. Where is that game played? → On the football field: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-16778** (school-life) What do American kids call a classmate who runs to tell the teacher what another kid did? → A tattletale: Hint 2 ("the second half of the word is another word for a story") gives the answer away: none of the wrong options ends in a word for a story, so it points only to "tattletale". Hint 2 should be a vaguer clue, for example about how other kids feel about this classmate, and leave the word-shape clue to hint 3.
- **q-16794** (roots-and-soul) Listen: a hip-hop DJ makes this sound with a vinyl record. What is the trick called? → Scratching: None of the audio candidates is clearly a DJ scratching a vinyl record. #2–#5 are a head being scratched, brushes and a metal door. #6 is someone saying the word "scratch" in French, which would give the answer away. #1 ("Where it All Started djsamp") is an unclear DJ sample that may contain music. A new search isn't allowed, so the clip has to be found by hand (for example on Freesound: "vinyl scratch DJ" or "turntablism scratch"). No suitable picture found for this question.
- **q-16800** (sayings-and-idioms) In cowboy movies, when it's time to ride out, the boss yells “Saddle…!” Which word finishes it? → Up: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-16844** (weather-and-seasons) You're decorating your porch for Halloween on October 31. Which of these does NOT belong? → A snowman: Hint 2 ("One of them would melt long before October 31 in most places") gives the answer away: only the snowman can melt, so it names the answer's defining trait as plainly as hint 3 does. Replace it with a hint about the season, e.g. that one option belongs to a different time of year, without mentioning melting, snow or cold.
- **q-16851** (winter-holidays) This singer recorded “Rockin' Around the Christmas Tree” in 1958 when she was just 13. Who is she? → Brenda Lee: The picked picture has an unsuitable licence (pd-us-only: PD-US-no notice).

## Question axes

- move: analogy 1, cause_effect 15, count 14, estimate 5, identify 33, made_of 9, name_concept 20, odd_one_out 14, origin 24, purpose 19, record 11, sequence 13, when 12, who 21, word_meaning 28
- stimulus: detail 3, map_outline 2, none 195, photo 35, sound 1, video 3
- clue: completion 9, direct 88, riddle 31, scenario 35, three_facts 76
- answer_kind: group 23, number 21, person 37, place 35, thing 54, time 17, word 52
- lens: body_senses 10, educational_media 15, everyday 33, history 51, language 29, nature 11, pop_culture 51, popular_science 5, school 23, science_news 6, university 5

## Dropped by the pipeline

- american-football-8: overlap like q-12731: Almost every football play starts with the move shown here: the ball passed back between a player's legs. What is it called? → The snap: At the line, the quarterback yells “Blue 42… set… hut!” What happens right after the “hut”? → The center snaps the ball
- childrens-books-13: overlap like q-4020: The cartoon where Ms. Frizzle's class rides a bus that shrinks and flies, even into the human body, started out as what? → A series of children's books: Who is the teacher who drives the Magic School Bus and takes her class on wild science trips? → Ms. Frizzle
- childrens-books-17: overlap like q-9004: In “How the Grinch Stole Christmas!,” the Grinch dresses up as Santa and ties one horn to his dog's head. What should the dog look like? → A reindeer: In “How the Grinch Stole Christmas!”, the Grinch has no reindeer to pull his sleigh. Who pulls it instead? → Max, his dog
- fairs-and-festivals-0: overlap like q-13951: In 1890, a Pasadena club started a New Year's Day parade of carriages covered in flowers. What was it meant to show the rest of the country? → California's warm winter weather: Look at this Rose Parade float from Pasadena, California. By the rules, what must its whole outside be covered in? → Flowers, seeds and other plant parts
- family-and-school-traditions-7: overlap like q-9606: You've got the day off for Easter Monday, a bank holiday. Which season is it? → Spring: You're hunting for colorful eggs the Easter Bunny hid in an American backyard. What season is it? → Spring
- family-and-school-traditions-17: overlap like q-15805: Which big US holiday is celebrated every year on July 4? → Independence Day: Americans watch fireworks, grill hot dogs and wave flags on July 4. What is this holiday officially called? → Independence Day
- folk-heroes-and-tall-tales-0: overlap like q-8866: Whose signature is the largest on the Declaration of Independence? → John Hancock: Complete the American saying: when someone says “Put your John Hancock right here,” they want you to write your… → Signature
- folk-heroes-and-tall-tales-1: duplicate like q-12725: This stadium is the home field of the New York Giants. In which state is it? → New Jersey: This six-story building shaped like an animal was built in 1881, and you can climb inside it. In which state does it stand? → New Jersey
- folk-heroes-and-tall-tales-10: overlap like q-11800: This metal rod on a roof protects the building from lightning. Which American invented it? → Benjamin Franklin: I flew a kite with a metal key on its string during a storm, to show that lightning is electricity. Who am I? → Benjamin Franklin
- hosts-and-game-shows-8: overlap like q-10786: You're playing Family Feud and have just given your answer. What famous phrase does the host shout to reveal whether it's on the board? → “Survey says!”: When the host of Family Feud shouts “Survey says!”, the board reveals the top answers. Who gave those answers? → 100 ordinary people in a survey
- hosts-and-game-shows-16: overlap like q-2826: In the blind auditions of The Voice, coaches sit with their backs to the singer. How many coaches are there in most versions? → 4: On NBC's The Voice, coaches sit with their backs to the singer and spin around if they like the voice. How many coaches' chairs are there? → 4
- household-brands-6: overlap like q-3832: In this game, sold since 1974, you drop red and yellow discs into an upright grid. What is it called? → Connect Four: Players take turns dropping colored discs into this upright grid. How do you win? → Get four in a row
- money-and-shopping-13: overlap like q-2892: Whose portrait is on the front of the US one-dollar bill? → George Washington: You find a $1 bill in your jeans pocket. Whose face is printed on it? → George Washington
- more-sports-2: overlap like q-0423: En la patineta, ¿cómo se llama el salto básico en el que la tabla sube pegada a los pies, sin usar las manos? → Ollie: You're skating and you pop a perfect ollie. At the top of the jump, how many of your skateboard's wheels are in the air? → 4
- more-sports-8: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: I'm a rodeo bull who threw 309 riders in a row. In 1988, world champion Lane Frost finally stayed on me for 8 seconds. What is my name? → Red Rock
- national-parks-12: overlap like q-8927: You stand at the rim of Bryce Canyon in Utah, looking at thousands of orange rock spires called hoodoos. What mainly carved them? → Ice freezing and melting in cracks: I'm a tall, skinny tower of rock, often with a harder stone cap like a hat. Thousands of me crowd Bryce Canyon, and my name sounds like magic. What am I? → A hoodoo
- national-parks-15: overlap like q-14939: You're visiting a US national park, and a worker in a flat, wide-brimmed hat tells you not to feed the bears. What is this job called? → Park ranger: Park rangers, drill sergeants and Smokey Bear all wear a “campaign hat.” What is it? → A wide, flat-brimmed hat with a pinched top
- native-nations-0: overlap like q-11775: I was a Lakota holy man and leader. In 1876, I had a vision of soldiers falling into our camp like grasshoppers. Soon after, we beat Custer at Little Bighorn. Who am I? → Sitting Bull: I was a Hunkpapa Lakota leader. Later I toured with Buffalo Bill's Wild West show and nicknamed sharpshooter Annie Oakley “Little Sure Shot.” Who am I? → Sitting Bull
- native-nations-7: overlap like q-12860: Every April in Albuquerque, New Mexico, the Gathering of Nations brings together dancers from hundreds of tribes. It's called the largest what in North America? → Powwow: I'm a big gathering of Native American nations. Dancers in bright regalia move around a big drum, and visitors are welcome to watch. What am I? → A powwow
- nineteenth-century-1: overlap like q-10227: Es un pañuelo de algodón, casi siempre rojo o azul con dibujos como gotitas, y los charros y campesinos lo usan al cuello. ¿Cómo se llama? → Paliacate: I'm a square of cotton, often red with swirly patterns. Cowboys tied me around their necks and pulled me over their noses when dust blew. What am I? → A bandana
- nineteenth-century-8: overlap like q-14913: In 1860, Pony Express riders carried mail about 1,900 miles (3,000 km) from Missouri to California. About how many days did the trip take? → 10 days: In 1858, Butterfield Overland Mail stagecoaches began carrying mail and riders from Missouri to San Francisco. About how long did the trip take? → About 3 weeks
- nineteenth-century-9: overlap like q-1604: Adivina: nací en 1873 para los mineros de California, tengo remaches de cobre y en mi etiqueta dos caballos intentan romperme. ¿Qué soy? → Los jeans: Levi Strauss and the tailor Jacob Davis got a patent for work pants with metal rivets: the first blue jeans. In which year? → 1873
- place-names-8: overlap like q-9368: Auf wen geht der Name der Stadt „München“ zurück? → Mönche: Iowa's capital Des Moines is said “duh-MOYN,” with both S's silent. Its name is French and came from a river. What does it mean? → Of the monks
- restaurant-chains-0: overlap like q-1394: Soy una cadena de cafés con una sirena en el logo y mi nombre viene de un marinero de 'Moby Dick'. ¿En qué ciudad nací? → Seattle: The Starbucks siren honors the sea-trading past of the port city where the first store opened in 1971. Which city? → Seattle
- restaurant-chains-10: overlap like q-3400: Harland Sanders wore a white suit, sold fried chicken with a secret recipe and was never an army officer. So why was he called “Colonel”? → An honorary title from his state: You open a bucket of KFC chicken. The smiling man with white hair and a bow tie on it created the recipe. Who is he? → Colonel Sanders
- american-football-16: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Fans wear it on one hand, it often comes in the team's colors, and it usually says “#1.” What is it? → A foam finger
- weather-and-seasons-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which storm reporter has been a face of The Weather Channel for decades, famous for standing out in hurricanes? → Jim Cantore
- weather-and-seasons-17: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: In the movie “Twister,” storm chasers watch a spinning funnel cloud. Complete the rule: it only counts as a tornado once it touches the… → ground
- words-and-slang-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Americans pump it at a station and pay for it by the gallon. What is this “gas”? → Fuel for the car
- childrens-books-16: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Teachers assign it after you read a book: you retell the story, describe the characters and say what you thought. What is it? → A book report
- folk-heroes-and-tall-tales-2: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Kemp Morgan was a tall-tale giant who could smell it deep under the rock and drilled wells in Oklahoma and Texas. What was he hunting for? → Oil
- hosts-and-game-shows-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: You're on Survivor and you find a hidden immunity idol. Which of these does it NOT do for you? → Give you an extra vote
- household-brands-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This American brand came out in 1964, and celebrities often use it to sign autographs. What is a Sharpie? → A permanent marker
- household-brands-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: An out-of-work architect invented Scrabble in the 1930s, during the Great Depression. In which American city did he live? → New York City
- place-names-16: overlap like q-15832: A US state and a big river in it share the name Alabama. Who was the name first used for? → A Native American people: You're driving across Iowa past endless cornfields. Who is the state named after? → A Native American people
- restaurant-chains-17: overlap like q-8967: This burger chain has square patties, a red-haired girl with pigtails on its logo, and a thick chocolate shake called the Frosty. Which chain is it? → Wendy's: The Golden Arches are to McDonald's as a smiling red-haired girl with pigtails is to… → Wendy's
- roads-and-landmarks-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This old-fashioned street, called Main Street, U.S.A., is the first thing you see at which company's theme parks? → Disney
- roots-and-soul-7: overlap like q-10732: Barack Obama is to Michelle Obama as Jay-Z is to… → Beyoncé: I sang in Destiny's Child, and my hit “Single Ladies” has a famous hand-wave dance. Who am I? → Beyoncé
- roots-and-soul-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Teenage bassist Bootsy Collins and his guitarist brother Catfish backed James Brown in 1970. What was that band called? → The J.B.'s
- sayings-and-idioms-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Which of these American sayings does NOT describe someone staying calm? → Flying off the handle
- sayings-and-idioms-7: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: I hold the reins and shout “Hold your horses!” when my team goes too fast. Who am I? → A wagon driver
- sayings-and-idioms-15: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: In old Westerns, a cowboy points and says the ranch is “over yonder.” Where is the ranch? → Over there, some way off
- sayings-and-idioms-16: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: Americans call someone an “eager beaver,” often with a smile. What kind of person is that? → Someone extra keen to work hard
- school-life-0: overlap like q-6145: Cheerleaders shake pom-poms like these at games. What are they usually made of today? → Thin plastic strips: At an American high school, where would you most likely see students waving these? → At a football game
- school-life-8: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Birds Eye launched this frozen food in the US in 1953, and it became a classic Friday school lunch. What is it? → Fish sticks
- states-and-capitals-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: What color is San Francisco's Golden Gate Bridge painted? → Orange-red
- traditional-songs-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: “My Country, 'Tis of Thee” was first sung in Boston on July 4, 1831. Its tune first belonged to which country's national anthem? → The United Kingdom
- traditional-songs-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: “This Little Light of Mine” asks “Hide it under a bushel? No!” That idea of a lamp hidden under a basket comes from which book? → The Bible
- trailblazers-4: overlap like q-14932: The state on this map has Annapolis as its capital. What is its largest city? → Baltimore: “I'm a port city in Maryland. Edgar Allan Poe died here in 1849 and is buried here, and my NFL team is named after his most famous poem. Which city am I?” → Baltimore
- roads-and-landmarks-2: overlap like q-14750: Buildings like the one in this close-up line Ocean Drive in Miami's South Beach. Which style are they? → Art Deco: These pastel hotels with neon signs line Ocean Drive in Miami Beach. What style of architecture is the street famous for? → Art Deco
- roads-and-landmarks-8: overlap like q-12873: It could take months, it moved thousands of longhorns from Texas to railroad towns in Kansas, and the Chisholm Trail was its most famous route. What is it called? → A cattle drive: After cowboys drove longhorns from Texas up the Chisholm Trail to towns like Abilene, Kansas, what happened to the cattle next? → They were put on trains to the East
- roads-and-landmarks-17: overlap like q-2001: Monks Mound, cerca de San Luis (Estados Unidos), es una gran pirámide de tierra de la antigua Cahokia. ¿Quién la construyó? → Pueblos nativos de Norteamérica: Near St. Louis, Native Americans built Cahokia, a city of giant earth mounds that's now a World Heritage Site. When was it at its largest? → Around the year 1100
- roots-and-soul-0: overlap like q-9021: People escaping slavery called this group of stars the “Drinking Gourd.” What did it help them do? → Find north: “Follow the Drinking Gourd” is said to have guided people escaping slavery to the North. What is the “drinking gourd”? → The Big Dipper
- roots-and-soul-2: overlap like q-5621: Hip hop was born at New York block parties, where DJs like Kool Herc stretched a song's drum beat by switching between two of these. What? → Record players: Hip-hop DJs play music on two of these. What are they? → Turntables
- roots-and-soul-4: overlap like q-3932: The famous “Thriller” music video has a zombie dance. Who sang “Thriller”? → Michael Jackson: The 1983 hit “Thriller,” with its famous zombie dance video, came from this singer. Who is he? → Michael Jackson
- roots-and-soul-5: overlap like q-15723: Listen: cowboys and blues players carried this little instrument in their pockets. Which one is it? → A harmonica: Blues players nickname it a “harp,” and you play it by breathing in and out through small holes. What instrument is it? → The harmonica
- roots-and-soul-10: overlap like q-12728: New Orleans' NFL team is named after a famous jazz song. Finish its title: “When the Saints Go…” → Marching In: Louis Armstrong turned this old hymn into a jazz hit in 1938, and New Orleans parades still play it. Which song is it? → “When the Saints Go Marching In”
- sayings-and-idioms-11: overlap like q-5553: After the attack on Pearl Harbor on December 7, 1941, what happened the very next day? → The US entered World War II: “Remember Pearl Harbor!” was a famous American rallying cry during which war? → World War II
- school-life-9: overlap like childrens-books-13: Who is the teacher who drives the Magic School Bus and takes her class on wild science trips? → Ms. Frizzle: Which cartoon teacher's famous motto is “Take chances, make mistakes, get messy!”? → Ms. Frizzle
- states-and-capitals-3: overlap like q-2308: Buckingham Palace is to the British king as what is to the president of the United States? → The White House: Who lives and works in this famous house? → The US president
- states-and-capitals-6: overlap like q-10719: Washington State grows more of this fruit than any other US state. Which fruit is it? → Apple: Which fruit does Washington state grow more of than any other US state? → Apples
- states-and-capitals-7: overlap like q-12813: Disney's “Pocahontas” is loosely based on history. Which real English captain is the hero she befriends in the film? → John Smith: An English explorer mapped this region's coast in 1614 and named it “New England.” He's also in Disney's “Pocahontas.” Who was he? → John Smith
- states-and-capitals-10: overlap like q-9097: You can meet Mickey Mouse at the park with this castle. Which US state is it in? → Florida: Walt Disney World is in the state shown on this map. Which state is it? → Florida
- weather-and-seasons-0: overlap like q-14898: This orange pie, spiced with cinnamon and nutmeg, is America's classic Thanksgiving dessert. What is it made from? → Pumpkin: It came from the Americas, it grows on a vine along the ground, and Americans bake it into a pie for Thanksgiving. What is it? → Pumpkin
- weather-and-seasons-6: overlap like q-13890: In The Wizard of Oz, a twister carries Dorothy and her little dog from a Kansas farm to Oz. What is her last name? → Gale: It lies in the middle of Tornado Alley, it's covered in wheat fields, and in “The Wizard of Oz” a twister carries Dorothy's house away from it. Which state? → Kansas
- winter-holidays-3: overlap like q-12950: Kids spin a top like this one in a game played during which holiday? → Hanukkah: I spin on a point, I have a Hebrew letter on each of my four sides, and kids play with me for chocolate coins during Hanukkah. What am I? → A dreidel
- winter-holidays-5: overlap like q-16806: I wear a tall black hat and a white collar. Each November, American kids play me in school plays about the first Thanksgiving. Who am I? → A Pilgrim: Kids wear hats like this in school Thanksgiving plays. Which group, who founded Plymouth Colony in 1620, are they dressed as? → The Pilgrims
- winter-holidays-7: overlap like q-4888: I wear the same red as Coca-Cola, have a big white beard and come down chimneys once a year. Who am I? → Santa Claus: In American Christmas stories, Santa gets into the house through this on Christmas Eve. What is it? → A chimney
- winter-holidays-10: overlap like q-2334: I'm a party balloon, and if you let go of my string, I float up to the sky. What gas am I filled with? → Helium: The Snoopy balloon has flown in the Macy's Thanksgiving Day Parade more times than any other character. What gas makes it float? → Helium
- words-and-slang-10: overlap like q-3683: Which 1960s movement does this photo show? → Hippies: This painted van is a symbol of the young Americans who made “far out” and “groovy” famous in the 1960s. What were they called? → Hippies
