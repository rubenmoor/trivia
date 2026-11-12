# tr-en-33

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `mexico` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 298
- Approved: 292
- Needs work: 6
- Not travelling: 2 (2 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 535, about $31.08 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-33&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-31 | tr-en-32 | tr-en-33 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 297 | 298 |
| not travelling |  | 0 | 3 | 2 |
| not travelling confirmed |  | 0 | 3 | 2 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 1.0 % ✓ | 0.7 % ✓ |
| approved |  | 295 | 292 | 292 |
| needs_work |  | 5 | 5 | 6 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 1.7 % ✓ | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.3 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.55 | $28.62 | $27.99 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), fact 1 (0 major), overlap 2 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.08

Major findings on approved questions:

None.

## Needs work

- **q-12506** (civic-holidays) On May 5, 1862, at the forts of Loreto and Guadalupe, General Ignacio Zaragoza won a battle. Who lost it? → The French: This duplicates approved q-12493, which also asks whom Mexico defeated at the 1862 Battle of Puebla (answer: the French army). It asks the same fact with the same answer. The overlap comes from the source, so the fix is to keep only one of the two questions in the pool, not to change this translation.
- **q-13495** (childrens-songs) In the song “Mi pollito amarillito”, what does the little chick do when it wants to eat bugs? → It scratches the ground with its feet: Fact check: uncertain. Song summaries confirm the chick scratches the ground for bugs, but I couldn't see the exact lyrics. The wrong answers look plausible as wrong.
- **q-13554** (landmarks) Look at this street sign from one of the longest avenues in Mexico City. Who does its name honor? → Those who fought for Independence: Source: the essential image is "File:Nomenclatura urbana Anillo Periférico.jpg". Going by its title, it shows a Periférico street sign, not one saying "Av. Insurgentes". The question depends on players reading "Insurgentes" on the sign, so it can't be answered with this file. The source's media needs a new search for an Insurgentes sign. The English translation itself is faithful and reads naturally.
- **q-14618** (chespirito) You’re in the park on a hot day and hear the cicadas singing. Which of these is NOT true about them? → They sing by rubbing their legs: source: Hint 3 says crickets rub their legs to sing, which is wrong. Crickets rub their wings together; grasshoppers (chapulines) rub their hind legs against their wings. The Spanish source has the same error, and the translator and rater both flagged it. The source needs a corrected hint 3, for example: “Grasshoppers make their sound by rubbing their back legs against their wings.” Then the translation can be redone from it.
- **q-17428** (revolution) It puffed black smoke, had a very loud whistle and carried Villa’s troops across the north. What was the “iron horse”? → A steam locomotive: This asks the same fact as approved q-8899: that the "iron horse" is the steam locomotive. Anyone who has seen one question knows the answer to the other, and the Villa setting doesn't change the fact being asked. The translation itself is faithful and natural ("camiones" correctly became "buses"), so the only problem is the duplicate; drop this English version or have the Mexican question ask something other than the nickname.
- **q-17728** (20th-century) It was made for the 1968 Mexico City Olympics and runs about 17 km (11 mi) across the south of the capital. What is the Ruta de la Amistad? → A corridor of giant sculptures: Fact check: uncertain. Answer, 17 km, and Goeritz are right, and the wrong answers are wrong. The fun fact is shaky. Wikipedia says 22 sculptures (19 route stations plus 3 guest pieces at Olympic venues) from 17 countries. 'Five continents' appears only in Time Out. '19 sculptures' is accurate only for the route stations. I could not confirm the hint about works over 10 m.

## Not travelling

- **q-13519** about_language, confirmed: «Paleta» es a «paletero» como «globo» es a… → Globero (The question tests Spanish word formation (-ero suffix); the wrong answers are invented Spanish word forms, so it is about the Spanish language itself.)
- **q-17690** about_language, confirmed: La palabra «quinceañera» junta un número con otra palabra. ¿Cuál es esa otra palabra? → Años (Asks how the Spanish word “quinceañera” is built (quince + años): a question about Spanish word formation, and the options would have to be Spanish words.)

## Stale re-translated

None.
