# tr-en-11

Made by `qgen batch --translate en` on 2026-10-29 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 281
- Needs work: 18
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 516, about $30.80 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-11&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-9 | tr-en-10 | tr-en-11 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 298 | 299 |
| not travelling |  | 3 | 2 | 1 |
| not travelling confirmed |  | 3 | 1 | 1 |
| rejected rate | ≤ 20.0 % | 1.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| approved |  | 293 | 290 | 281 |
| needs_work |  | 4 | 8 | 18 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 2.7 % ✓ | 6.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.7 % ✓ | 5.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 1.0 % ✗ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 93.3 % ✓ | 91.7 % ✓ |
| cost $ |  | $27.46 | $26.76 | $27.60 |
| $ per approved |  | $0.09 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 56 (2 %)
- Major among review needs work: 0 of 4 (0 %)
- Problems by kind: giveaway 3 (0 major), fact 1 (0 major), overlap 5 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 55 of 60 (92 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.20

Major findings on approved questions:

- **q-7633**: overlap — Related q-4549 is already approved and asks the same thing: where the "water" comes from when your mouth waters. Its answer is also "The salivary glands", so the only change here is Colombian food in the setup. Apart from that, the translation is faithful and natural, the wrong answers really are wrong, and the fun fact is accurate (1–1.5 L is about 2–3 US pints). (http://127.0.0.1:8001/review/q-7633)

## Needs work

- **q-0232** (sweets-and-desserts) What fruit is bocadillo veleño made from? → Guava: The English text of approved q-7574 says “Bocadillo veleño (guava paste)”, so anyone who has seen q-7574 already knows the answer here. The better fix is in q-7574: drop the “(guava paste)” gloss. Its question doesn't need it, because it asks about the bijao leaf. After that, this translation can be approved as it is.
- **q-0519** (independence) I'm a university in Bogotá, named after the first president of the State of Cundinamarca, in 1811. Which one am I? → Universidad Jorge Tadeo Lozano: source: the fun fact says the university was founded in 1954, "almost 140 years" after the 1811 presidency, but that gap is 143 years, so it should say "more than 140 years". The translation copies this faithfully, so the source needs correcting. Also from the source: the question says the university is named after a person, and only the answer is a person's full name, so the options give it away (hint 1 says so outright). Consider replacing a wrong answer with a university named after a person (e.g. Universidad Sergio Arboleda).
- **q-5235** (traditional-games) In the circle game “el gato y el ratón,” the children hold hands in a ring. What do they do when the cat tries to get in? → They lower their arms to block the way: Fact check: uncertain. The game mechanic is supported: one source says the children in the ring are the mouse's allies and lower their arms to keep the cat out. I could not find the exact rhyme "Ratón, ratón / ¿Qué quieres, gato ladrón?" in any source. The Colombian version may differ. The difficulty rating of 4 also looks high for such a simple question.
- **q-6878** (plants-and-flowers) Every February, Colombia ships flowers abroad for Valentine's Day. About how many stems does it send? → 600 million: Source: the 600 million figure is out of date. Recent seasons were about 700 million stems in 2024 and more than 900 million in 2025, nearing 1 billion, so the answer should become about 900 million or 1 billion, with wrong answers rebuilt around it. The English translation itself is faithful and natural ("6 billion" is the correct US rendering of 6000 millones), so it only needs updating once the source changes. Fact check: wrong. The 600 million figure is outdated. A 2023-era Portafolio piece cited a 600 million stem target. Reports for 2024 cite about 700 million stems, and Forbes and Portafolio coverage of 2025 cites more than 900 million (over 60,000 tonnes). La República's 2026 projection converts to about 980 million.
- **q-6930** (olympic-medallists) Which of these colors does NOT appear in the Olympic rings? → Purple: Source: this question asks the same fact as approved q-6258 ("Which color is NOT one of the colors of the Olympic rings?", answer Purple), so English players would get the same question twice. Its only link to Colombia is hint 2. The translation is faithful and reads naturally, so the problem is the duplicate, not the wording. Drop it, or replace it in the source with a question that really needs Colombian knowledge.
- **q-7019** (carnivals-and-fairs) On January 5 in Pasto, people smear your face with black paint. According to tradition, who asked for that day off in colonial times? → Enslaved Africans: Fact check: uncertain. Answer (enslaved Africans) and the Jan 5 'Día de los Negros' tradition are correct. The 1607 date is documented only in Wikipedia, which says the revolt was in Remedios, Antioquia, not Pasto, and flags the history as needing citations. Other sources call the carnival's origins '17th century' without a specific revolt. The hint 'They didn't have a single day of rest' is awkward but acceptable.
- **q-7190** (traditional-games) You're making your kite's tail out of things from around the house. Which of these will NOT work for the tail? → Iron hex nuts: Fact check: uncertain. Iron hex nuts are plausible as the heavy wrong item, but I did not search for this one. Kite tails are normally light, so heavy nuts would not work. Some kite makers tie small weights to a tail, so the answer could be argued. August as Colombia's kite month is well known.
- **q-7267** (languages) In which of these cities do people NOT speak with a costeño (Caribbean coast) accent? → Bucaramanga: Fact check: wrong. The answer and distractors are correct. Bucaramanga is inland, it's the capital of Santander, and it's nicknamed "Ciudad Bonita". Barranquilla, Cartagena and Santa Marta are Caribbean cities with costeño accents. The fun fact about dropping the final s is accurate. The problem is the description: "talk fast, chop their words short" describes the costeño accent, which is the distractors' accent and not the answer's. It points players to the wrong cities. I did not run searches. This verdict rests on my own knowledge.
- **q-7365** (mountains-and-landscapes) It falls from the clouds on stormy afternoons, rattles loudly on tin roofs and can turn the streets white. What falls in a granizada? → Balls of ice: Fact check: uncertain. The answer and wrong answers are fine, since hail is balls of ice. The Nov 3, 2007 Bogotá hailstorm is well documented, but I found no source for the "almost 1 m (3 ft) deep" figure. One Blu Radio piece mentions up to 1 m, but it seems to be about a different storm. Pulzo gives no depth.
- **q-7453** (fruits) Which of these fruits do you NOT need to peel before eating it? → Guava: Fact check: uncertain. Guava is correct (edible skin, bocadillo veleño is guava paste). But granadilla is a weak wrong answer: you don't peel it either. You crack the hard shell open and eat the pulp, so a player could argue it also needs no peeling.
- **q-7696** (cinema) In which decade was the Cinemateca Distrital de Bogotá founded? Today it’s called the Cinemateca de Bogotá. → The 1970s: source: the fun fact says the new Cinemateca de Bogotá building opened in 2019, but I recall it opening in December 2018, and the rater had the same doubt. Please verify. If December 2018 is right, the source should say 2018 or drop the year.
- **q-7783** (words) In Colombia, what do you call a group of friends who go out together to have a good time? → El parche: source: The fun fact's “parchesazo” is doubtful. The common Colombian augmentative is “parchazo”, the translator flagged this too, and the fact check only went from memory. The source's fun fact should be corrected to “parchazo” (or reworded), and then the translation should follow it. Apart from that, the translation is faithful and reads naturally.
- **q-7821** (home-school-and-paperwork) It stays at the bottom of the rice pot, comes out toasted and crunchy, and many families fight over it. What is it called in Colombia? → Pegao: Fact check: uncertain. Pegao is the standard Colombian term. But "cuncho" is also reported as a regional word for the rice crust or dregs in Colombia, Ecuador and Peru, so it may not be clearly wrong. My search did not confirm or rule this out. Other regional names are cucayo (Caribbean coast) and pega.
- **q-7914** (places-and-monuments) At Medellín's most famous fair, the silleteros parade with silletas on their backs. What are the silletas made of? → Flowers: Fact check: wrong. The answer (flowers) and the fun fact are fine. The image query is "Medellin metrocable", which doesn't show silleteros or silletas, so the illustration doesn't fit the question.
- **q-8083** (salsa-and-tropical-music) Boogaloo was born in New York in the 1960s and drove Cali's dancers wild. It mixed Latin rhythms with which African American music? → Soul and R&B: Fact check: uncertain. The answer is right: boogaloo (Latin boogaloo) blended Latin rhythms with soul and R&B. The wrong answers are wrong, and the hints are true. The fun fact is unverified: Cali DJs are widely said to have sped up records, but usually salsa records played at 45 rpm instead of 33. Tying this specifically to boogaloo is not well sourced. The question also says "which African American music" (singular) but the answer names two genres. I did not run a search.
- **q-8302** (regional-speech) In Barranquilla, if someone says “¡Qué pava!”, what are they complaining about? → Bad luck: Fact check: uncertain. I couldn't find a source for 'pava' meaning bad luck in Barranquilla. I also couldn't verify 'pavoso' or 'echar la pava'. My recollection is that this sense exists on the Colombian coast, but 'echar pava' may carry another meaning.
- **q-8406** (mountains-and-landscapes) Cerro de Guadalupe, with its big statue of the Virgin, watches over Bogotá from the eastern hills. Roughly how high is its summit? → About 3,300 meters: source: The fun fact calls the summit statue "the statue of the Virgin of Guadalupe". The fact check says the 15 m statue by Gustavo Arcila Uribe (1946) shows the Immaculate Conception, and only the chapel is dedicated to Guadalupe. The Spanish source has the same error, so it needs fixing there first. Change the fun fact to something like "The statue of the Immaculate Conception on the summit is about 15 m (49 ft) tall…", then translate it again. Otherwise the translation is faithful and reads naturally. Fact check: wrong. Answer (~3,300 m; sources say 3,317 m) and the 15 m statue height are right. But the fun fact calls it the statue of the Virgin of Guadalupe. The statue shows the Virgin of the Immaculate Conception. Only the small chapel is dedicated to Guadalupe.
- **q-8428** (popular-and-andean-music) I was born in Ginebra, Valle del Cauca, played the tiple all my life, and my town's big Colombian Andean music festival bears my nickname. Who am I? → Benigno Núñez: Fact check: uncertain. The person and the festival are right: Benigno "Mono" Núñez was born in Ginebra, Valle, and the festival bears his name. But "played the tiple all my life" is shaky. Sources say he began on the accordion, then played tiple, guitar and bandola, and he is mostly known as a bandola player. The hint that the nickname refers to his light hair is plausible ("mono" means blond) but I couldn't verify it. The festival start year of 1974/75 fits "since the 1970s". The description about a "corner store" nickname is also unverified.

## Not travelling

- **q-6914** about_language, confirmed: En la obra lleva arena y cemento, y en la finca carga abono o leña. ¿Qué es una carretilla? → Un carrito de mano de una rueda (Asks what the everyday Spanish word “carretilla” (wheelbarrow) means; it isn't a Colombian regional word, so in English it would just be a Spanish vocabulary test.)

## Stale re-translated

None.
