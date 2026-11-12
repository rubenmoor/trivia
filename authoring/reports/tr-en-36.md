# tr-en-36

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `mexico` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 511, about $31.46 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-36&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-34 | tr-en-35 | tr-en-36 |
|---|---|---:|---:|---:|
| sources |  | 300 | 256 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 296 | 255 | 300 |
| not travelling |  | 4 | 1 | 0 |
| not travelling confirmed |  | 3 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 1.0 % ✓ | 0.4 % ✓ | 0.0 % ✓ |
| approved |  | 289 | 249 | 292 |
| needs_work |  | 7 | 6 | 8 |
| needs_work rate | ≤ 20.0 % | 2.4 % ✓ | 2.4 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 2.0 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.4 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 95.0 % ✓ |
| cost $ |  | $26.06 | $24.49 | $28.15 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: fact 1 (0 major), overlap 1 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.30

Major findings on approved questions:

- **q-11528**: overlap — Same fact as the approved q-2491: the move described (back to goal, body in the air, ball kicked over the head) has the answer "bicycle kick". The question is answerable from that description alone, and the Raúl Jiménez detail is optional context, so seeing one question gives the other away. The rest checks out: Jiménez scored a late bicycle kick against Panama at the Azteca on October 11, 2013 (2–1), the fun fact is true, the wrong answers are really wrong, and the English hint 3 (named after the people of Chile) is a sound adaptation of "chilena". (http://127.0.0.1:8001/review/q-11528)

## Needs work

- **q-11592** (contemporary-cinema) In the comedy “Tod@s caen” (2019), two seduction experts compete against each other. Which actor stars in it alongside Martha Higareda? → Omar Chaparro: Hint 3 is false: Omar Chaparro did not voice Pikachu. He played Sebastian, the Charizard trainer, in “Detective Pikachu” and dubbed his own role in the Latin American version. The translation turned the source's vague wording into a specific claim that is wrong. Use: “He's from Chihuahua and played Sebastian, the Charizard trainer, in “Detective Pikachu”.” The source's own wording (“le puso la voz en español a «Detective Pikachu»”) is also misleading; source: it should be clarified the same way. Separately, related q-17307 pairs Omar Chaparro with Martha Higareda in its question text, and q-15670 is built on the same clues as hints 2 and 3, so the overlap is worth checking. Fact check: wrong. Hint 3 is false. Omar Chaparro is from Chihuahua, but he did not voice Pikachu in the Spanish dub. He played Sebastian in the film and dubbed himself in Latin America. Reynolds voiced Pikachu in the original. The answer is right and the film was a big box-office hit.
- **q-12506** (civic-holidays) On May 5, 1862, at the forts of Loreto and Guadalupe, General Ignacio Zaragoza won a battle. Who lost it? → The French: The translation itself is faithful and natural, but it asks the same fact as related q-12493: the Battle of Puebla, May 5, 1862, and whom Mexico defeated, with the answer "The French army". The two questions shouldn't sit together in the English mexico pool, so keep only one of them.
- **q-12641** (golden-age-cinema) It starred Jorge Negrete, Fernando de Fuentes directed it in 1942, and it was the first Mexican film with this new feature. What was it? → Color: Fact check: uncertain. Cast and director are right (Negrete, Fernando de Fuentes, 1942, ¡Así se quiere en Jalisco!). The 'first Mexican color feature' claim is widely repeated, but English Wikipedia only says it 'was commented' to be the first. The Cinecolor detail in the fun fact is not stated in any source I found. The only support is a Wikipedia category tag. Color shorts such as Novillero and Extravaganza mexicana existed, so the hint 'all Mexican films were black and white' is slightly overstated. Sound and 3D are clearly wrong, and widescreen is almost certainly wrong too.
- **q-13495** (childrens-songs) In the song «Mi pollito amarillito», what does the little chick do when it wants to eat bugs? → Scratches the ground with its little feet: Fact check: uncertain. I could not open the lyrics text. Search summaries confirm the song is about a yellow chick that fits in the palm of a hand, eats bugs and fears a hawk. I could not verify the line about what it does to get the bugs. From memory, the answer (scratching the ground with its feet) is plausible, and the wrong answers look wrong. The fun fact about hens scratching for seeds and bugs is generally true. The title is also ambiguous because several versions exist (Gallina Pintadita, El Reino Infantil, Lunacreciente).
- **q-13554** (landmarks) Look at this sign from one of the longest avenues in Mexico City. Who does its name honor? → Those who fought for Independence: Source: the essential image is titled “Nomenclatura urbana Anillo Periférico.jpg”, so it apparently shows a Periférico street sign, not one that reads “Av. Insurgentes”. If so, players can't work out the answer from the sign (Periférico sections carry other names, such as Ávila Camacho), and the question breaks in every language. Someone needs to check the file, and replace it with an actual Insurgentes sign if it doesn't show one. The English text itself is fine.
- **q-13580** (other-sports) Born in Mexicali, she won vault bronze at a 2018 World Championships: Mexican gymnastics' first world medal. Who is she? → Alexa Moreno: Source: the claim "Mexican gymnastics' first world medal" is wrong. Daniel Corral won pommel-horse silver at the 2013 World Championships, so Moreno's 2018 vault bronze was the first world medal for a Mexican woman (female gymnast). The source needs this correction ("first world medal for a Mexican woman gymnast"), and the translation should then follow it.
- **q-15458** (boxing) I was born in Sonora, grew up in Culiacán, went almost 90 fights without losing and filled Estadio Azteca with over 130,000 people. Who am I? → Julio César Chávez: source: Hint 3 says Julio César Chávez is named after a "Roman emperor". Julius Caesar was a Roman dictator, never an emperor; the empire began with Augustus after his death. Fix the source hint (e.g. "a famous Roman dictator" or "a famous Roman leader") first. The translation will then follow it. Fact check: wrong. The third hint says he is named after a Roman emperor. Julius Caesar was never an emperor. He was a Roman dictator, and the empire began after his death with Augustus. The rest checks out from memory: Chávez was born in Ciudad Obregón, Sonora, and grew up in Culiacán. He was unbeaten for his first 89 fights, losing the 91st to Frankie Randall. The 1993 Haugen fight at Estadio Azteca drew about 132,000. His son Julio César Chávez Jr. is a boxer. The wrong answers are other Mexican boxers.
- **q-17728** (20th-century) It was made for the 1968 Olympics and runs about 17 km (10.5 mi) across the south of the capital. What is the Ruta de la Amistad? → A corridor of giant sculptures: Fact check: uncertain. Answer (sculpture corridor, ~17 km, Goeritz, 1968, south Periférico) is right and the wrong answers are wrong. But the fun fact says '19 sculptures by artists from five continents'. Sources say 19 stations on the route, plus 3 guest sculptures at Olympic venues (22 total), by 22 sculptors from 17 countries. So '19' is defensible for the route itself, but the 'five continents' claim and the artist count are loosely sourced. The hint 'over 10 m tall' is unverified, and some works are smaller.

## Not travelling

None.

## Stale re-translated

None.
