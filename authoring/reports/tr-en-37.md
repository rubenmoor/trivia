# tr-en-37

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `mexico` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 485, about $30.37 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-37&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-35 | tr-en-36 | tr-en-37 |
|---|---|---:|---:|---:|
| sources |  | 256 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 255 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.4 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 249 | 292 | 292 |
| needs_work |  | 6 | 8 | 8 |
| needs_work rate | ≤ 20.0 % | 2.4 % ✓ | 2.7 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.0 % ✓ | 2.0 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.4 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 95.0 % ✓ | 95.0 % ✓ |
| cost $ |  | $24.49 | $28.15 | $27.16 |
| $ per approved |  | $0.10 | $0.10 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: fact 1 (1 major), overlap 2 (0 major), style 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.21

Major findings on approved questions:

- **q-12607**: fact — Source: hint 1 is false. Lupillo Rivera was born on January 30, 1972 in La Barca, Jalisco, and moved to Long Beach, California as a child (IMDb, Wikipedia). Jenni was the one born in California. The translation copies the error faithfully, so the fix belongs in the source, e.g. "I was born in Jalisco and grew up in California…". The rest checks out: "El Toro del Corrido", Jenni as "La Diva de la Banda", the wrong answers and the fun fact. (http://127.0.0.1:8001/review/q-12607)

## Needs work

- **q-10157** (20th-century) This mural is made of colored stones and covers all four walls of a famous building. Which building is it? → The UNAM Central Library: source: Hint 2 says the library opened in the early 1950s "along with the rest of the campus", but the UNAM Central Library opened on April 5, 1956. It was built from 1950 to 1952, and the campus was inaugurated in 1952. The translation copies this error from the source. Fix the source hint first, for example to "It was built in the early 1950s, along with the rest of the campus.", and then translate it again. Fact check: wrong. Hint 2 is inaccurate: the Central Library opened on April 5, 1956 (construction began 1950). The main campus was inaugurated in 1952, but the library wasn't open then.
- **q-12506** (civic-holidays) On May 5, 1862, at the forts of Loreto and Guadalupe, General Ignacio Zaragoza won a battle. Who lost it? → The French: This duplicates related q-12493 (“Cinco de Mayo weekend… The date honors the 1862 Battle of Puebla. Whom did Mexico defeat?” → The French army). Both ask who Mexico beat at Puebla on May 5, 1862, so whichever one players see first gives away the other. Keep only one of them in the English pool. The translation itself is faithful and reads naturally.
- **q-13554** (landmarks) Look at this street sign from one of the longest avenues in Mexico City. Who is it named after? → Those who fought for independence: source: the essential image is 'File:Nomenclatura urbana Anillo Periférico.jpg', which most likely shows a Periférico street sign, not 'Av. Insurgentes'. The question asks about the name on the sign, so it fails if the image is wrong. The source's media needs to be replaced with a real Avenida Insurgentes street sign. The English translation itself is faithful and natural. Fact check: wrong. The text is correct (Insurgentes is named for the independence insurgents; Metrobús Line 1 opened in 2005). But the essential image is file 'Nomenclatura urbana Anillo Periférico', so it likely shows a Periférico sign, not 'Av. Insurgentes'. The question depends on the image.
- **q-14598** (regional-mexican) Listen: a Sinaloan banda is never without this instrument. Which one is it? → The cymbals: Fact check: wrong. The snare drum (tarola) is a standard part of the banda sinaloense, so it is arguably also a correct answer. The 'never without' claim fits the tambora, with cymbals mounted on it, better than the cymbals alone. Cymbals are usually mounted on the tambora and are not always a separate instrument.
- **q-15458** (boxing) I was born in Sonora, grew up in Culiacán, went almost 90 fights without losing and filled Estadio Azteca with over 130,000 people. Who am I? → Julio César Chávez: Source: hint 3 says Chávez shares his name with a Roman emperor, but Julius Caesar was a general and dictator, never an emperor. The translation copies this faithfully, so the source hint needs correcting first (e.g. “a famous Roman general and dictator”), then the English should follow it. Fact check: wrong. Hint 3 says the name is shared with a Roman emperor. Julius Caesar was a dictator and never an emperor. The rest checks out: born in Ciudad Obregón, Sonora; raised in Culiacán; unbeaten in his first 89 fights; the 1993 Haugen fight at Estadio Azteca drew about 132,000.
- **q-16537** (indigenous-peoples) Look at this woven palm mat, the petate. What was it mainly used for in homes in the old days? → To sleep on: source: the fun fact gives the Nahuatl word as «pétatl», but the Nahuatl word for mat is «petlatl». The source needs correcting first. The English fun fact also uses «» guillemets where house style wants “…”. Fix both in the translation once the source is fixed.
- **q-17328** (indigenous-peoples) Look at these dancers from Oaxaca with huge round headdresses and mirrors. Which dance are they performing? → Danza de la Pluma: source: The fun fact says the headdresses can be more than 1 meter (3 ft) across. The fact check couldn't confirm this: sources give about 1 m tall and roughly 80 cm wide, or a 60 cm crown. The source's fun fact should be corrected, for example to “The dancers jump and spin nonstop wearing feathered headdresses about 1 meter (3 ft) tall that can weigh over 25 kg (55 lb).” Then the translation should follow it. One small style point while revising: “hairdo” in the description is a literal rendering of “peinado”; “headgear” reads more naturally. Fact check: uncertain. The answer (Danza de la Pluma) is right. The wrong answers are wrong: Venado is Yaqui/Sonora, Viejitos is Michoacán, Voladores is Totonac/Veracruz. The hints are consistent with sources: Guelaguetza, Moctezuma and the conquest, a headdress of feathers and mirrors. The fun fact is not verified. No source gave a headdress diameter of more than 1 m. One travel guide gives about 1 m tall and 80 cm wide, weighing over 25 kg. An artisan catalog lists a 60 cm crown.
- **q-17428** (revolution) It puffed black smoke, had a very loud whistle and carried Villa's troops across the north. What was the “iron horse”? → A steam locomotive: The translation itself is fine, but in English it asks the same fact as approved q-8899: that the "iron horse" is the steam locomotive. Anyone who has seen one question already knows the answer to the other. Either keep only one of them in the English pool, or rework this one around a Mexico-specific fact about Villa's trains, which would make it a different question.

## Not travelling

None.

## Stale re-translated

None.
