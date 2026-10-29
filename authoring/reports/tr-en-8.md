# tr-en-8

Made by `qgen batch --translate en` on 2026-10-29 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 288
- Needs work: 9
- Not travelling: 3 (3 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 522, about $28.56 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-8&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-6 | tr-en-7 | tr-en-8 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 295 | 297 |
| not travelling |  | 0 | 5 | 3 |
| not travelling confirmed |  | 0 | 5 | 3 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 1.7 % ✓ | 1.0 % ✓ |
| approved |  | 295 | 293 | 288 |
| needs_work |  | 5 | 2 | 9 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 0.7 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 0.7 % ✓ | 3.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 100.0 % ✓ | 96.7 % ✓ |
| cost $ |  | $23.46 | $28.15 | $25.68 |
| $ per approved |  | $0.08 | $0.10 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 3 (1 major), fact 3 (1 major), ambiguity 1 (0 major), overlap 2 (1 major), media 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.88

Major findings on approved questions:

- **q-0484**: overlap, giveaway — The facts hold up: Ibargüen won triple jump gold at Rio 2016 and silver at London 2012, and the Christ the Redeemer image only sets the scene in Rio. The problem is overlap with related q-7855 ("In the triple jump, Caterine Ibargüen landed in a place like this one…"), whose question text gives this answer away. On top of that, hint 2's "hop, step and jump" is the event's old English name, so in English it all but names the answer before hint 3. This is a minor hint giveaway. (http://127.0.0.1:8001/review/q-0484)

## Needs work

- **q-0107** (20th-century) Which country split off from Colombia in 1903? → Panama: Source: the fun fact overstates the period. Panama was part of Colombia from 1821 to 1903, so about 80 years of the 19th century, not "almost the whole" century. The source should say "most of the 19th century, from 1821 until 1903", and the translation should then follow it. The rest of the translation is faithful and natural. Fact check: wrong. The fun fact overstates it. Panama joined Gran Colombia in 1821 and left in 1903, so it was part of Colombia for about 80 of the 19th century's 100 years, not 'almost the whole' century. The answer, wrong answers and hints are fine.
- **q-6820** (conquest-and-colonial-era) Dominican archbishop Fray Cristóbal de Torres founded it in 1653, many independence heroes studied there, and today it's a university in central Bogotá. Which one? → Universidad del Rosario: Fact check: uncertain. The answer is right: Colegio Mayor de Nuestra Señora del Rosario, founded in 1653 by Fray Cristóbal de Torres, with Camilo Torres and Caldas among its alumni. The hints hold up. The only unverified part is the description's claim that former students appear on banknotes. A search found no Rosario alumnus on a Colombian banknote, and most notable banknote figures (Santander, García Márquez, Lleras Restrepo) studied elsewhere.
- **q-6975** (salsa-and-tropical-music) Englishman Quantic and Mario Galeano formed Ondatrópica in 2012 and recorded their first album at the legendary Discos Fuentes studios. In which city? → Medellín: source: the fact check says Ondatrópica began in late 2011, and only the album was recorded in early 2012 at Discos Fuentes in Medellín. The source repeats "created Ondatrópica in 2012", so the error comes from the source and not from the translation. The source should be reworded first, for example "Quantic and Mario Galeano recorded Ondatrópica's first album in 2012 at the legendary Discos Fuentes studios. In which city?", and then translated again. Fact check: wrong. The question says Ondatrópica was formed in 2012. Sources say the project began at the end of 2011, and the album was recorded in January 2012 at Discos Fuentes in Medellín. The answer, Medellín, is right.
- **q-7243** (club-football) You're at the Pascual Guerrero stadium: Nacional vs. Medellín is the clásico paisa, just as América vs. Deportivo Cali is the clásico… → Vallecaucano: Source: the fun fact says América and Deportivo Cali have played each other "since the 1940s", but the fact check found they first met in 1931; only the professional-era clásico began in 1948. The source needs correcting (e.g. "first met in 1931; their professional-era clásico began in 1948"), and the translation should then follow it. Fact check: wrong. The answer (clásico vallecaucano) and wrong answers are fine. The fun fact is inaccurate: América and Deportivo Cali first met in 1931 (departmental tournament, Galilea stadium). The 1940s is only when the professional-era clásico began (1948, Cali won 4-3).
- **q-7365** (mountains-and-landscapes) It falls from the clouds during afternoon downpours, hammers on tin roofs and can turn the streets white. What falls in a hailstorm? → Balls of ice: Fact check: uncertain. The answer (balls of ice) is correct and the 3 Nov 2007 Bogotá hailstorm is real. But the 'almost 1 m of ice on some streets' figure is only loosely supported. A BBC report cited 1.5 m of water and ice at one intersection, and I found no primary source for ice piled up on streets in general.
- **q-7434** (cycling) In Colombia, a bicycle is called a “cicla.” If a park has 4 ciclas and 2 tricycles, how many wheels are there in total? → 14: Fact check: uncertain. The math is right: 4×2 + 2×3 = 14, and 12, 10 and 16 are wrong. "Cicla" is a real Colombian word for bicycle. The fun fact is shaky. In Colombian Spanish "llanta" mainly means the tire. It can mean the whole wheel only loosely in everyday speech, and the standard word for wheel is "rueda". I did not search to check this, so I could not confirm the claim.
- **q-7807** (christmas-and-special-dates) It hangs from the ceiling at birthday parties, is shaped like a character, and kids hit it with a stick until it breaks. What is it usually made of? → Paper and cardboard: Fact check: uncertain. The answer (paper and cardboard) is right. Glass, metal and stone are clearly wrong, and the hints are fine. The fun fact, that in Colombia a whole children's birthday party is also called "la piñata", could not be verified. The sources I found only say piñatas are common at Colombian birthdays. I found nothing on the party itself being called "la piñata". The "hang from the ceiling" detail is also loose, since piñatas are usually hung from a tree or a rope. The image query "children birthday party balloons" doesn't show a piñata.
- **q-8141** (ghosts-and-creatures) I'm not a prayer or a charm, and I cost nothing: if a spirit gets you lost in the hills, I break the spell and you find your way. What am I? → Your clothes worn inside out: Fact check: uncertain. The folk remedy of wearing clothes inside out against the duende and the Madremonte is plausible and widely reported in Colombian and Latin American folklore, but I did not run a search to confirm it. The fun fact (the duende likes long-haired girls and small children) also matches general folklore and was not verified. The wrong answers are not real remedies.
- **q-8414** (national-team) I'm a goalkeeper, I played for Arsenal in England and Napoli in Italy, and I was Colombia's starter at the 2014 and 2018 World Cups. Who am I? → David Ospina: source: Hint 2 and the fun fact say Ospina has more caps than anyone in Colombia's history. That record can change, and after the 2026 World Cup cycle I can't confirm it still holds: James Rodríguez was close to Ospina's total and may have passed it. Rephrase both in the source as a fact that can't go out of date (e.g. "one of the most-capped players" or "more than 120 matches"). The translation itself is faithful and natural.

## Not travelling

- **q-7381** wordplay, confirmed: Recitas «El renacuajo paseador»: Rin Rin sale «con pantalón corto, corbata a la moda, sombrero encintado y chupa de…». ¿Qué palabra sigue? → Boda (Completing a Spanish verse whose key clue is the rhyme with “moda”. The answer and options are Spanish words, and in English the rhyme is lost.)
- **q-5172** wordplay, confirmed: Dice la adivinanza: «Agua pasa por mi casa, cate de mi corazón; el que no me lo adivine es un burro cabezón». ¿Qué es? → El aguacate (The riddle hides the answer in Spanish sounds (agua + cate = aguacate), and that can't be rebuilt in English.)
- **q-5174** wordplay, confirmed: Dice la adivinanza: «Oro parece, plata no es; el que no lo adivine, bien bobito es». ¿Qué es? → El plátano (The riddle hides the answer in Spanish words (“plata no” = plátano), and that can't be rebuilt in English.)

## Stale re-translated

None.
