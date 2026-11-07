# batch-52

Made by `qgen batch` on 2026-11-07 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: usa
- Language: English
- Subcategories (25): folk-heroes-and-tall-tales, national-parks, place-names, college-sports, trailblazers, hosts-and-game-shows, states-and-capitals, native-nations, state-symbols, regional-dishes, tv-shows, movie-favorites, american-football, civics, national-symbols, colonies-and-founding, roads-and-landmarks, comics-and-art, school-life, rivers-lakes-and-mountains, cities-and-towns, plants-and-trees, baseball, ghosts-and-superstitions, country-and-folk
- Merged: 230 (q-15674…q-15903)
- Approved: 212
- Needs work: 18
- Dropped by the pipeline: 86
- Reviewed by: claude-opus-5-5
- Claude calls: 523, about $68.28 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-50, batch-51; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-50 | batch-51 | batch-52 |
|---|---|---:|---:|---:|
| source locale |  | es-ES | es | en |
| drafts |  | 320 | 328 | 316 |
| skipped slots |  | 166 | 194 | 134 |
| dropped |  | 88 | 101 | 86 |
| drop rate | ≤ 20.0 % | 27.5 % ✗ | 30.8 % ✗ | 27.2 % ✗ |
| dropped: hard fail correct |  | 4 | 3 | 1 |
| dropped: hard fail unambiguous |  | 1 | 2 | 1 |
| dropped: hard fail no_giveaway |  | 17 | 14 | 12 |
| dropped: overlap |  | 66 | 76 | 70 |
| dropped: duplicate |  | 1 | 4 | 2 |
| dropped: fact-check wrong |  | 0 | 2 | 0 |
| merged |  | 232 | 227 | 230 |
| approved |  | 214 | 207 | 212 |
| needs_work |  | 18 | 20 | 18 |
| needs_work rate | ≤ 20.0 % | 7.8 % ✓ | 8.8 % ✓ | 7.8 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.9 % ✓ | 2.2 % ✓ | 2.6 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 0.4 % ✓ | 0.9 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.3 % ✗ | 1.8 % ✗ | 0.4 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.3 % ✓ | 4.4 % ✓ | 4.8 % ✓ |
| media: no pick in review 1 |  | 30 | 39 | 21 |
| media: recovered by research |  | 23 | 32 | 15 |
| media: no pick at record |  | 8 | 7 | 7 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 21.9 % ✗ | 25.6 % ✗ | 23.1 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 55.8 % ✓ | 50.5 % ✗ | 68.6 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 0.53 ✓ | 1.00 ✓ | 2.12 ✗ |
| approved 11–15 |  | 49 | 48 | 35 |
| top move | ≤ 25.0 % | 16.4 % ✓ | 13.2 % ✓ | 14.8 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 81.5 % | 85.0 % | 77.4 % |
| values stimulus |  | 3 | 4 | 6 |
| top clue | ≤ 60.0 % | 45.7 % ✓ | 37.4 % ✓ | 47.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 20.3 % ✓ | 22.0 % ✓ | 25.7 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.3 % ✓ | 18.1 % ✓ | 20.4 % ✓ |
| values lens |  | 10 | 10 | 10 |
| media share | 15.0 %–50.0 % | 18.5 % ✓ | 15.0 % ✗ | 22.6 % ✓ |
| mean fun | ≥ 3.40 | 3.46 ✓ | 3.41 ✓ | 3.44 ✓ |
| cost $ |  | $71.78 | $68.24 | $65.05 |
| $ per approved | ≤ $0.35 | $0.34 ✓ | $0.33 ✓ | $0.31 ✓ |
| calls |  | 468 | 452 | 463 |
| calls per approved |  | 2.19 | 2.18 | 2.18 |
| wall time h |  | 2.24 | 2.13 | 2.00 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 4 (1 major), fact 2 (0 major), ambiguity 1 (0 major), overlap 1 (0 major), media 4 (2 major), difficulty 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.23

Major findings on approved questions:

None.

## Needs work

- **q-15697** (civics) On the US flag, each of the 50 states gets one of these. What is it? → A star: This asks the same thing as approved q-2363 (“Besides stripes, which shape appears 50 times on this flag?” → Stars). Both ask about the 50 stars on the US flag, one for each state. Drop it or swap it for a different flag fact.
- **q-15731** (folk-heroes-and-tall-tales) Which of these is NOT true about Captain Ahab in the novel “Moby-Dick”? → He narrates the story: Hint 2 (“One of these is about how the book is told, not what happens in it”) solves the question. Only one option is about narration, so the hint points straight at the answer. Replace it with a vague hint, for example one saying the book is told by a young sailor and not the captain, without singling out an option.
- **q-15732** (folk-heroes-and-tall-tales) Giant fiberglass men like this one began in 1962 with a Paul Bunyan made for a café on Route 66. In which state did that first one stand? → Arizona: Fact check: uncertain. The Flagstaff, Arizona Paul Bunyan (Bob Prewitt, 1962, Paul Bunyan Café on Route 66) is only 'widely cited' as the first Muffler Man. Sources hedge ('World's First?', 'legend has it'). The question states it as flat fact. The café was also renamed the Lumberjack Cafe.
- **q-15761** (national-symbols) This bell was first cast in England in 1752. Which foundry made it? → Whitechapel Bell Foundry: Hint 1 gives the answer away. Whitechapel is the only London foundry among the options: Meneely was in Troy, New York, Paul Revere & Sons in Boston and John Taylor & Co in Loughborough. The question text already says the bell was cast in England, which rules out the two American foundries, so “The foundry was in London” leaves only one option. Replace hint 1 with a vaguer one, such as the era or how the bell crossed the Atlantic. Also replace the two American foundries with English foundries outside London, or swap one for another London foundry, so the location clues don't remove options.
- **q-15762** (national-symbols) You flip over a $1 bill and look at the eagle's left claw. How many arrows is it holding? → 13: Hint 2 (“Many people think of this number as unlucky”) gives the answer away: of 3, 7, 50 and 13, only 13 is the famous unlucky number. Hint 1 already points strongly at the 13 colonies too. Replace hint 2 with something vaguer, like the number of arrows being bigger than a handful but smaller than the number of states, and leave the colonies link for hint 3.
- **q-15767** (place-names) Newark, which locals squeeze into “NOO-erk,” was founded by Puritans in 1666. It is the biggest city of the state on this map. Which state? → New Jersey: No candidate works as the essential plain outline map. #1, #5 and #6 print "New Jersey" in their titles, #4 is a Hudson County map labeled with Jersey City, and #2 and #3 aren't maps. I can't run a new search, so the question needs an unlabeled New Jersey outline (for example a blank state-shape SVG from Commons). No suitable picture found for this question.
- **q-15780** (regional-dishes) A hard-shell taco is crunchy, U-shaped, and falls apart at the first bite. What is its shell? → A fried corn tortilla: No candidate works as an illustrative image. Candidates 1 and 2 show soft tortillas topped with filling, so they point straight to the answer "tortilla". Candidates 3 to 6 show pho, Thai noodles, Thai desserts and Filipino rice bowls, which have nothing to do with tacos. Search again with something like "taco night table" or "salsa and guacamole bowls", without showing tortillas or shells. No suitable picture found for this question.
- **q-15796** (cities-and-towns) This statue stands outside the arena of the Chicago Bulls. Which basketball star does it honor? → Michael Jordan: The question says the statue "stands outside the arena," but it was moved into the United Center's new atrium in 2017, so the text is out of date. It should say something like "stands at the home arena of the Chicago Bulls." There is also no usable essential image. Candidate 3 is the only clear shot of the statue, and the plaque on its base reads "MICHAEL JORDAN," which gives the answer away. Candidate 4 is a small, dark view of the statue indoors among NHL Draft banners. Candidates 1 and 2 are stone plaques full of text, and in 5 and 6 the statue is a tiny speck in front of the arena. No suitable picture found for this question.
- **q-15811** (folk-heroes-and-tall-tales) In the old US, workers nicknamed “gandy dancers” sang to keep the rhythm as they swung heavy hammers onto iron spikes. Who were they? → Railroad track workers: The picked picture has an unsuitable licence (pd-us-only: PD-USCG).
- **q-15820** (national-parks) In a 1959 Hitchcock thriller, Cary Grant dodges a crop-duster and hangs off Mount Rushmore. What do the villains hide inside a small statue? → Microfilm: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-15830** (place-names) From 1963 to 1973, Florida's Cape Canaveral officially carried the name of a US president. Which one? → John F. Kennedy: The picked picture has an unsuitable licence (pd-us-only: PD-USCG).
- **q-15833** (place-names) Lima, Ohio, said “LYE-muh” like the bean, is the setting of the TV show “Glee.” What is the show's high school choir called? → New Directions: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-15837** (regional-dishes) On an American diner menu, what are “silver dollars,” served several to a plate hot off the griddle? → Small pancakes: The description calls the item "a breakfast," which rules out "Fried onion rings" before any hint. The description should play on the money theme without saying which meal it is, e.g. "Diners hope you'll leave some of these behind, but these ones you eat."
- **q-15849** (roads-and-landmarks) In which decade was the famous “Welcome to Fabulous Las Vegas” sign put up? → The 1950s: The question names a showable object, the “Welcome to Fabulous Las Vegas” sign, but none of the six candidates shows it. They are general Strip and Fremont Street night scenes. A search for the sign itself (e.g. "Welcome to Las Vegas sign") is needed, and no new search is allowed here. The text is fine: the 1959 date and the Betty Willis fun fact check out. No suitable picture found for this question.
- **q-15853** (state-symbols) License plates from the state on this map read “Birthplace of Aviation,” even though the first airplane flight happened in another state. Which state is it? → Ohio: None of the six candidates shows an outline map of Ohio. They are skyscrapers, a ballpark scoreboard, a park path and an OH-13 helicopter, so the essential "state on this map" image is missing. A new search isn't allowed, so the slot needs a blank Ohio outline map found by hand, for example by searching "Ohio blank outline map" or "Ohio locator map". No suitable picture found for this question.
- **q-15882** (state-symbols) This close-up shows part of a freestanding kitchen cabinet from the early 1900s, with a built-in flour bin and sifter. What was this kind of cabinet called? → Hoosier cabinet: The question says the photo is a close-up of part of the cabinet showing its flour bin and sifter, but no candidate is a close-up: 1, 2, 5 and 6 show the whole cabinet, and 3 and 4 are advertisements with “Hoosier” printed on them. Either reword the question to “This photo shows a freestanding kitchen cabinet from the early 1900s, with a built-in flour bin and sifter…” and use candidate 1 (the whole cabinet, open, with the sifter showing in the middle), or find a real close-up of the flour bin and sifter with no brand label. No suitable picture found for this question.
- **q-15883** (states-and-capitals) The Lincoln Memorial stands in the place outlined on this map. Which place is it? → Washington, D.C.: No candidate shows a blank outline map of the District of Columbia. #1 is a street map with a big "DISTRICT OF COLUMBIA" title box, which names the answer. #2 and #3 are dense, tall old city maps covered in text. #4 and #6 are building photos, and #5 is a map of British Columbia. The slot needs a clean, unlabeled DC outline, and no new search is allowed. No suitable picture found for this question.
- **q-15897** (tv-shows) The Teenage Mutant Ninja Turtles live in tunnels like this one. Under which city are they? → New York City: Hint 2 ("a huge city on the East Coast of the United States") gives the answer away, because New York City is the only East Coast US city among the options. Hint 2 should only narrow things down, for example by mentioning the city's famous skyscrapers or its many yellow taxis without naming a region that only New York fits. The media is fine: candidate 2, the brick sewer tunnel, works.

## Question axes

- move: analogy 5, cause_effect 19, count 11, estimate 7, identify 34, made_of 15, name_concept 20, odd_one_out 15, origin 18, purpose 16, record 9, sequence 10, when 13, who 16, word_meaning 22
- stimulus: detail 10, map_outline 4, none 178, photo 36, sound 1, video 1
- clue: completion 8, direct 109, riddle 15, scenario 27, three_facts 71
- answer_kind: group 32, number 21, person 28, place 27, thing 59, time 14, word 49
- lens: body_senses 7, educational_media 29, everyday 29, history 47, language 35, nature 13, pop_culture 35, popular_science 3, school 26, university 6

## Dropped by the pipeline

- american-football-3: overlap like q-12843: Quarterback Tom Brady played 23 NFL seasons. Fans call him by an animal's name as a huge compliment. Which animal? → Goat: On a football team, “QB” is the player who takes the snap, calls the plays and throws the passes. What does QB stand for? → Quarterback
- american-football-5: overlap like q-12761: A marching band like this one performs on the field during a break in the middle of a football game. What is that break called? → Halftime: At the Super Bowl, in the break after the second quarter, stars like Rihanna, Shakira and Usher take over the field. What do they do there? → Put on a big music concert
- american-football-9: overlap like q-1408: Su lema es 'Lo mejor para el hombre', su fundador se llamaba King y popularizó las hojas de afeitar desechables. ¿Qué marca es? → Gillette: The New England Patriots play at Gillette Stadium, shown here. The stadium is named after a brand famous for which product? → Razors
- american-football-10: overlap like q-10723: In the song “Clementine,” her father was a “miner, forty-niner.” In which state did the 1849 gold rush happen? → California: Who are the San Francisco 49ers named after? → Gold seekers who rushed to California
- baseball-0: overlap like q-5420: This baseball player crouches behind home plate in a mask and signals to the pitcher. Which position? → Catcher: This baseball glove is round, extra thick and padded, with no separate fingers, and it's built to catch fast pitches all game. Which players wear it? → Catchers
- cities-and-towns-3: overlap like q-9009: Which Pennsylvania town has a Chocolate Avenue, air that can smell like cocoa, and streetlights shaped like foil-wrapped chocolate drops? → Hershey: The man in this photo built a whole Pennsylvania town for the workers of his chocolate factory. Who is he? → Milton Hershey
- cities-and-towns-7: overlap like q-0312: Es millonario, no tiene ningún superpoder, sale de noche a vigilar su ciudad y tiene su guarida secreta en una cueva. ¿Qué superhéroe es? → Batman: I live in Gotham City in a huge mansion, and my butler is named Alfred. At night I put on a cape and fight crime. Who am I? → Batman
- cities-and-towns-9: overlap like q-1964: Parece un platillo volador, se construyó para una feria mundial en 1962 y se llama Space Needle. ¿En qué ciudad está? → Seattle: This tower stands in the US city nicknamed “the Emerald City.” What is the tower called? → The Space Needle
- civics-5: overlap like q-3103: This animal became the symbol of the US Democratic Party after opponents mocked an 1828 candidate by calling him one. Who was he? → Andrew Jackson: This animal has stood for one of the two big US political parties since the 1800s. Which party? → The Democratic Party
- civics-14: overlap like q-13927: Who became the first woman Speaker of the US House of Representatives, in 2007? → Nancy Pelosi: Who became the first woman to serve as Speaker of the US House of Representatives, in 2007? → Nancy Pelosi
- college-sports-5: overlap like q-12786: There's a parade, a big football game and a dance, and a king and queen are crowned. Who is an American homecoming meant to welcome back? → Former students: At halftime of a fall high school football game, students wearing crowns and sashes like these are announced. What is this group called? → The homecoming court
- colonies-and-founding-14: overlap like q-9211: Du schaust „Babylon Berlin“, das 1929 spielt. Welcher Gegenstand dürfte darin eigentlich noch gar nicht vorkommen? → Kugelschreiber: You're watching the signing of the Declaration of Independence in 1776. Which of these could NOT be on the table? → A ballpoint pen
- comics-and-art-1: overlap like q-0437: En los dibujos animados, ¿qué come Popeye el marino para volverse superfuerte? → Espinacas: Popeye the Sailor Man gulps down this vegetable, straight from the can, to get super strong. What is it? → Spinach
- comics-and-art-6: overlap like q-3672: The letters in DC Comics come from a comic magazine that started in 1937, where Batman first appeared in 1939. What do the letters stand for? → Detective Comics: Founded in New York in 1934, this company publishes Superman, Batman and Wonder Woman. Which comic book company is it? → DC Comics
- comics-and-art-8: overlap like q-0307: ¿Qué le pasa a quien queda atrapado en el lazo dorado de la Mujer Maravilla? → Dice la verdad: Which superhero uses a golden rope like this one, which makes anyone caught in it tell the truth? → Wonder Woman
- comics-and-art-15: duplicate like q-6380: Animals with stripes like these live in the wild on only one continent. Which one? → Africa: Marvel's hero named after this big cat is the king of Wakanda. On which continent is Wakanda? → Africa
- country-and-folk-5: overlap like q-3375: I was accepting my first MTV video award in 2009 when a rapper grabbed my microphone to say Beyoncé deserved it. Who am I? → Taylor Swift: I grew up on a Christmas tree farm, sang my first country hits as a teen in Nashville, and later went on the huge Eras Tour. Who am I? → Taylor Swift
- country-and-folk-7: overlap like q-15186: Scherzhaft nennt man es „Quetschkommode“: Man trägt es vor dem Bauch, zieht es auseinander und drückt es zusammen. Was ist gemeint? → Akkordeon: Zydeco bands in Louisiana love a “squeezebox.” You push and pull it, and it has buttons or keys. What is it? → An accordion
- country-and-folk-13: overlap like q-0062: Escucha: ¿qué instrumento está sonando? → El violín: Listen: square dances and bluegrass bands can't do without this instrument. Which one is it? → The fiddle
- folk-heroes-and-tall-tales-7: overlap like q-0947: Benjamin Franklin, el de la famosa cometa en la tormenta, inventó tres de estas cosas. ¿Cuál NO inventó? → La bombilla: In 1752 I flew a kite in a thunderstorm with a metal key tied to the string, to show that lightning is electricity. I was also a Philadelphia printer. Who am I? → Benjamin Franklin
- ghosts-and-superstitions-8: overlap like q-3441: In Tim Burton's “Beetlejuice”, how do you summon the mischievous ghost? You say his name… → Three times in a row: I'm a wild ghost in a black-and-white striped suit with messy green hair. I call myself a “bio-exorcist,” and Michael Keaton played me in 1988 and 2024. Who am I? → Beetlejuice
- ghosts-and-superstitions-10: overlap like q-11875: US supermarkets sell hot “rotisserie” chickens, roasted on a turning spit. The name comes from the language of which country? → France: In the 1800s, Americans held “séances,” sitting in the dark holding hands to call spirits. The word means “a sitting” in the language of which country? → France
- ghosts-and-superstitions-17: overlap like q-6058: This picture shows the White House after British troops set it on fire in 1814. Who was US president then? → James Madison: This house in Washington, D.C., is said to be haunted. Which president moved in after the British burned the White House in 1814? → James Madison
- hosts-and-game-shows-2: overlap like q-11936: Announcer Ed McMahon shouted “Here's Johnny!” every night for 30 years, from 1962 to 1992, to bring out the host. On which TV show? → The Tonight Show: For 30 years, Johnny Carson walked onto The Tonight Show after the famous call “Heeere's Johnny!” Who was the announcer saying it? → Ed McMahon
- hosts-and-game-shows-12: overlap like q-7057: Mis jurados son cantantes famosos que escuchan de espaldas y giran su silla si les gusta la voz. En mi escenario solo cantan niños. ¿Qué programa soy? → La Voz Kids: On NBC's The Voice, coaches can't see the singer at first. They just listen. If they like the voice, they hit a big button. What turns around? → Their chair
- hosts-and-game-shows-15: overlap like q-5569: You go through the alphabet from A to Z and count the vowels, not counting Y. How many do you find? → 5: On Wheel of Fortune, players can “buy a vowel.” How many different vowels can they buy? → 5
- movie-favorites-0: overlap like q-0504: ¿Qué personaje de Marvel es? Es un científico que, cuando se enoja, se vuelve un gigante verde y superfuerte. → Hulk: In the Avengers movies, Bruce Banner is a quiet scientist who must stay calm. What happens if he gets really angry? → He turns into the Hulk
- movie-favorites-4: overlap like q-5962: In Star Wars, they carry glowing lightsabers, use the Force for good, and Yoda trains them. What are they called? → Jedi: Darth Vader was once Anakin Skywalker, who trained with a lightsaber to use the good side of the Force. When he turned to the dark side, which group did he betray? → The Jedi
- movie-favorites-9: overlap like q-1668: Olaf, de Frozen: está hecho de nieve, ama los abrazos cálidos y canta que sueña con una estación. ¿Cuál? → El verano: I was made by magic, I have a carrot for a nose, and I dream about summer and warm hugs. Who am I? → Olaf
- movie-favorites-10: overlap like q-1060: ¿Cómo se llama el anciano de la película de Pixar que amarra miles de globos a su casa? → Carl Fredricksen: I'm a grumpy old man. I tied thousands of balloons to my house and floated off to South America, with a boy scout stuck on my porch. Who am I? → Carl Fredricksen
- movie-favorites-14: overlap like q-4362: At a big film awards night like the Oscars, when do the stars walk the red carpet? → Before the ceremony: At the Oscars in Hollywood, when do the movie stars walk the red carpet and pose for photos? → Before the show starts
- national-parks-0: overlap like q-0945: Estás explorando una cueva: una estalactita crece desde el techo y una estalagmita desde el suelo. Cuando por fin se tocan, ¿qué forman? → Una columna: Look at the stone spikes hanging from the ceiling of Carlsbad Caverns in New Mexico. What are they called? → Stalactites
- national-parks-6: overlap like q-13891: I'm a bear in a ranger's hat and jeans. Since the 1940s I've told Americans, “Only you can prevent forest fires.” Who am I? → Smokey Bear: I'm a black bear in a ranger hat and jeans, and a real cub saved from a wildfire once played me. I say, “Only you can prevent wildfires!” Who am I? → Smokey Bear
- national-parks-10: overlap like q-3345: The red stone arches of Arches National Park in Utah are made of sandstone from ancient sand dunes. In which time in Earth's history did those dunes form? → The Jurassic: Most of the stone arches in Utah's Arches National Park, like this one, are carved from which kind of rock? → Sandstone
- national-symbols-0: overlap like q-6751: This city is the capital of the USA, it is home to the White House, and it is named after the country's first president. Which city is it? → Washington, D.C.: This face is on the US $1 bill. Which US city is named after him? → Washington, D.C.
- national-symbols-3: overlap like q-15697: On the US flag, each of the 50 states gets one of these. What is it? → A star: The Pledge to this flag calls the US “one nation, indivisible.” Its 50 stars stand for 50 what? → States
- national-symbols-4: overlap like q-12818: Whose portrait is on the front of the US five-dollar bill? → Abraham Lincoln: Alexander Hamilton, star of a hit Broadway musical, is on the $10 bill. Who is on the next bill down, the $5? → Abraham Lincoln
- national-symbols-14: overlap like q-4077: He has a white goatee, a top hat with stars and points at you on army posters saying “I want you”. What does Uncle Sam stand for? → The United States: It's tall, with a flat top and a stiff brim, and Uncle Sam's has a band of stars around it. What kind of hat is it? → A top hat
- native-nations-7: overlap like q-6393: Watch: soft clay is shaped on a spinning wheel. What does it turn into after baking in a very hot oven? → Hard pottery: Pueblo women in New Mexico rolled me from wet earth into long coils, painted me with yucca-leaf brushes and baked me in a fire. What craft am I? → Pottery
- native-nations-9: overlap like q-15765: The Lakota and other Plains nations followed huge bison herds across the grasslands. Why? → For food, clothing and tools: The Lakota, part of the Sioux, lived on the Great Plains, moved camp often and followed bison herds. What were their tipi covers made of? → Bison hides
- place-names-5: overlap like q-15691: Which of these sports teams does NOT play in Dallas? → The Lakers: Which of these pro sports teams does NOT play for the city Texans call “Big D”? → Houston Astros
- plants-and-trees-0: overlap like q-2478: The fruit in this photo first grew wild in which part of the world? → South America: Pineapples made Hawaii famous, and James Dole canned them there from 1901. But on which continent did pineapples first grow? → South America
- plants-and-trees-1: overlap like q-11841: Texas's state flower, the bluebonnet, is a kind of lupine. The name “lupine” comes from the Latin word for which animal? → Wolf: Look at this close-up. Each spring, Texans pose for family photos in roadside fields of this state flower. What is it called? → Bluebonnet
- plants-and-trees-3: overlap like q-0927: Adivina: soy una raíz del manglar, pero en vez de hundirme, salgo del barro hacia arriba como un lápiz, y la marea me tapa y me destapa. ¿Para qué sirvo? → Para tomar oxígeno del aire: In Florida, black mangroves push hundreds of pencil-like roots straight up out of the mud. What are these roots for? → To take in air
- plants-and-trees-6: overlap like q-3276: In dry lands, plants like this one break off at the base and roll away in the wind. Why do they do it? → To spread their seeds: Look at the photo: balls like this roll across empty towns in Western movies. What are they made of? → A dried-out plant
- plants-and-trees-9: overlap like q-2482: The sweet syrup often poured on pancakes comes from the tree with this leaf. Which tree is it? → Maple: Look at this close-up of a classic American breakfast. What sweet, golden-brown thing is dripping down these pancakes? → Maple syrup
- plants-and-trees-17: overlap like q-12831: This giant cactus stars in many cartoon deserts. In the US, it grows wild almost only in one state. Which one? → Arizona: This giant cactus grows arms after many years, woodpeckers drill nest holes in it, and its white flower is Arizona's state flower. What is it called? → Saguaro
- cities-and-towns-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: This close-up shows a famous kind of pizza from Chicago, with the cheese under a thick layer of tomato sauce. What kind is it? → Deep-dish pizza
- trailblazers-11: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: In 1869, Wyoming Territory became the first place in the US to give women the vote, and in 1870 it seated the first women on a jury. What nickname did this earn the state? → The Equality State
- trailblazers-14: overlap like q-3133: Gustave Eiffel's company built this tower for the 1889 World's Fair in Paris. What is it made of? → Iron: George Ferris built his giant wheel for Chicago's 1893 World's Fair to outdo the star of the previous World's Fair. Whose tower was that? → Gustave Eiffel
- cities-and-towns-15: overlap like roads-and-landmarks-15: I grew up in a small Missouri town with a train depot. Later I built a street like it, with a train station at one end and a castle at the other. Who am I? → Walt Disney: This castle stands in a theme park in California that opened in 1955. Who built the park? → Walt Disney
- college-sports-4: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Until 2004, what were Syracuse University's men's sports teams called? → The Orangemen
- college-sports-14: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Stanford's teams are named after a color, and their band's mascot is a dancing tree. What is the teams' nickname? → The Cardinal
- ghosts-and-superstitions-0: overlap like q-14898: This orange pie, spiced with cinnamon and nutmeg, is America's classic Thanksgiving dessert. What is it made from? → Pumpkin: Pumpkin spice mixes cinnamon, nutmeg, ginger and cloves, and often has no pumpkin in it at all. What was it first made for? → Baking pumpkin pie
- movie-favorites-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: I stand at the door of the movie theater. I tear the slip you bought in two and hand you back the stub. Who am I? → The ticket taker
- national-parks-2: overlap like states-and-capitals-17: The southern edge of the state on this map follows a river that forms the border with Mexico. What is that river called in the US? → The Rio Grande: A river makes a huge U-turn in Texas that gives Big Bend National Park its name. Which river is it? → Rio Grande
- national-parks-9: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Yosemite campsites have big steel boxes, and food, coolers and even toothpaste must go inside, not in your car. Why? → Bears smell it and break into cars
- national-symbols-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: On the Great Seal, the eagle holds a branch in its right claw. Its head turns toward it, and it stands for peace. Which tree is the branch from? → Olive
- native-nations-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Plains nations like the Lakota and the Crow made tipis. What did families use a tipi for? → As a home
- native-nations-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Look at the photo. This animal's English name comes from an Algonquian word. What is it? → A skunk
- place-names-13: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: French explorers named the city of Eau Claire, Wisconsin. What does its name mean? → Clear water
- rivers-lakes-and-mountains-1: overlap like q-2609: You're watching geysers in Yellowstone, which sits on a supervolcano. When did it last have a giant eruption? → About 600,000 years ago: Deep under Yellowstone, hot rock heats water until it bursts out of the ground in a tall spout. What is this called? → Geyser
- rivers-lakes-and-mountains-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: These mountains between Tennessee and North Carolina are often wrapped in a bluish haze. What are they called? → Great Smoky Mountains
- school-life-13: hard fail: correct 4, unambiguous 3, no_giveaway 5, no_overlap 5: You walk into an American kindergarten classroom in the morning. Where does your backpack go first? → Into your cubby
- state-symbols-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: A US state's Latin motto is “Montani semper liberi.” It was adopted in 1863, the year the state broke off from its neighbor during the Civil War. Who does it say are always free? → Mountaineers
- trailblazers-2: overlap like q-15846: At 16, this frontiersman ran away from Missouri with a trade caravan on the Santa Fe Trail. He later lived in Taos, New Mexico. Who is he? → Kit Carson: Which frontier scout, a hero of old dime novels, guided John C. Frémont's expeditions to the American West in the 1840s? → Kit Carson
- rivers-lakes-and-mountains-0: overlap like q-11762: Paul Bunyan, the giant of American tall tales, swings his huge axe all day. What is his job? → Lumberjack: This giant statue in Bemidji, Minnesota, shows Paul Bunyan, a hero of American tall tales. Which workers first told his stories? → Lumberjacks
- rivers-lakes-and-mountains-11: overlap like q-6066: The Hawaiian Islands formed one after another as the Pacific Plate slid over a hot spot. Which main island is the youngest? → Hawaiʻi Island: Kilauea, one of the most active volcanoes on Earth, is on the island highlighted on this map. Which island is it? → Hawaii
- roads-and-landmarks-5: overlap like q-1590: La famosa pista de hielo del Rockefeller Center, en Nueva York, abrió por primera vez el día de Navidad de… ¿qué año? → 1936: Rockefeller Center in New York, home of a famous ice rink, was built during the Great Depression. In which decade? → The 1930s
- roads-and-landmarks-13: overlap like q-15830: From 1963 to 1973, Florida's Cape Canaveral officially carried the name of a US president. Which one? → John F. Kennedy: You're driving on I-90 through Chicago's northwest side. This stretch of expressway is named after which president? → John F. Kennedy
- roads-and-landmarks-15: overlap like cities-and-towns-15: This castle stands in a theme park in California that opened in 1955. Who built the park? → Walt Disney: I grew up in a small Missouri town with a train depot. Later I built a street like it, with a train station at one end and a castle at the other. Who am I? → Walt Disney
- school-life-2: overlap like q-5764: In “High School Musical”, Troy Bolton is to the basketball team as Sharpay Evans is to the… → Drama club: In Disney's “High School Musical,” East High's basketball star secretly tries out for the school musical. What is his name? → Troy Bolton
- state-symbols-4: overlap like q-9076: Nicknamed the Badger State after 1800s lead miners who lived in holes dug into hillsides, it also calls itself “America's Dairyland.” Which state? → Wisconsin: License plates from the state on this map say “America's Dairyland,” and its football fans wear foam cheese hats. Which state is it? → Wisconsin
- state-symbols-12: overlap like q-11916: Oklahoma's college teams are called the Sooners, after people in the 1889 Land Rush. Who were the first Sooners? → Settlers who sneaked in before the start: In 1889, thousands lined up for a signal gun to race in and claim free land in Oklahoma. Some got the name “Sooners.” What had they done? → Entered the land before the start
- state-symbols-14: overlap like q-15872: In the license plate game, you'd know Idaho plates by their slogan: “Famous…” what? → Potatoes: Complete the slogan on Idaho's license plates: “Famous…” → Potatoes
- states-and-capitals-0: overlap like q-15697: On the US flag, each of the 50 states gets one of these. What is it? → A star: This flag design has flown since July 4, 1960. How many stars does it have? → 50
- states-and-capitals-4: duplicate like q-10759: In 2024, a US state replaced its old flag with this new design. Which state is it? → Minnesota: This photo shows a lake in the state nicknamed the “Land of 10,000 Lakes.” Which state is it? → Minnesota
- states-and-capitals-7: overlap like q-8958: At a Maryland crab feast, steamed crabs are piled on newspaper and cracked open with wooden mallets. Which crab, caught in the Chesapeake Bay, is the star? → Blue crab: Steamed blue crabs like these, caught in Chesapeake Bay, are the most famous food of which state? → Maryland
- states-and-capitals-11: overlap like q-3277: Which US state is home to the Grand Canyon? → Arizona: The Grand Canyon is in the state shown on this map. Which state is it? → Arizona
- states-and-capitals-13: overlap like q-3134: This famous bridge hangs from two huge cables. In which city is it? → San Francisco: You're crossing the Golden Gate Bridge, the world's longest suspension bridge when it opened in 1937. Which city is at its south end? → San Francisco
- trailblazers-5: overlap like q-9095: Which Harlem nightclub's radio broadcasts in the late 1920s made Duke Ellington famous across America? → The Cotton Club: You're at Harlem's Cotton Club, where Duke Ellington's orchestra is the house band and the radio carries it nationwide. When is this? → The 1920s
- trailblazers-12: overlap like q-9115: It's the biggest songbird in North America, and in an Edgar Allan Poe poem it only says “Nevermore.” Which bird is it? → Raven: “I was born in Boston in 1809. I wrote a poem about a talking black bird, and Baltimore's football team is named after it. Who am I?” → Edgar Allan Poe
- trailblazers-16: overlap like q-4478: Ernest Hemingway's “The Old Man and the Sea” tells of a fisherman who sails out from this country. Which one is it? → Cuba: This bearded American writer lived in Key West and Cuba and wrote “The Old Man and the Sea.” Who is he? → Ernest Hemingway
- tv-shows-3: overlap like q-13895: Which Simpsons character loves to play this instrument, often sounding the blues on it? → Lisa Simpson: In The Simpsons, which Simpson kid is the smart one who plays the saxophone? → Lisa
- tv-shows-5: overlap like q-3870: I'm a hand with no body. I run around on my fingertips and help Wednesday Addams solve mysteries. What's my name? → Thing: In The Addams Family, a hand like this one walks around by itself. What is the hand's name? → Thing
- tv-shows-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Elmo's pet Dorothy is orange, lives in a round glass bowl and swims all day. What kind of animal is she? → A goldfish
