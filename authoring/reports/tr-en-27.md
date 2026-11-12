# tr-en-27

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `mexico` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 290
- Needs work: 9
- Not travelling: 1 (0 confirmed → `translatable: false`, 1 translated again next run)
- Claude calls: 520, about $28.10 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-27&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-25 | tr-en-26 | tr-en-27 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 299 | 299 |
| not travelling |  | 1 | 1 | 1 |
| not travelling confirmed |  | 1 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 294 | 289 | 290 |
| needs_work |  | 5 | 10 | 9 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 3.3 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 2.3 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 96.7 % ✓ | 96.7 % ✓ |
| cost $ |  | $27.06 | $27.73 | $25.38 |
| $ per approved |  | $0.09 | $0.10 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 1 (0 major), fact 1 (0 major), overlap 2 (0 major), media 1 (0 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.71

Major findings on approved questions:

None.

## Needs work

- **q-10354** (reserves-and-climate) The drill alarm goes off at school, and the teacher says “No corro, no grito, no empujo” (I don't run, I don't shout, I don't push). What is that phrase for? → To leave calmly and safely: Fact check: uncertain. The core claim is confirmed: "No corro, no grito, no empujo" is the standard evacuation-drill rule, so the answer is right. I could not find a source for the fun fact that some schools add a fourth rule, "no regreso".
- **q-10380** (states-and-capitals) Which of these states is NOT part of the Bajío region? → Veracruz: Fact check: uncertain. Veracruz is correctly not in the Bajío. But Aguascalientes is included in broader definitions of the Bajío (and in auto-industry usage), so it's a shaky wrong answer. The 1,800 m figure is approximate (about 1,700–2,000 m).
- **q-10427** (landscapes) This snowy volcano, the Popocatépetl's neighbor, is famous for the figure its outline makes. What does it look like? → A sleeping woman: source: hint 1 says the Nahuatl name "describes exactly that figure". That is false: Iztaccíhuatl means "white woman", not "sleeping woman", so the source hint needs correcting first, e.g. "Its Nahuatl name means “white woman.”". On the translation side, "the Popocatépetl's neighbor" is awkward English and should be "Popocatépetl's neighbor", with no article. Fact check: wrong. Hint 1 is false. The Nahuatl name Iztaccíhuatl means 'white woman', not 'sleeping woman'. The sleeping-woman figure comes from the outline and the legend. The answer and the fun fact are correct: El Pecho is the highest summit, at about 5,230 m.
- **q-11648** (school-and-services) Complete the name: CONALEP is the Colegio Nacional de Educación… → Profesional Técnica: source: Hint 3 is false in the source and in the translation. CONALEP stands for COlegio NAcionaL de Educación Profesional, so the acronym ends in P and has no T. The source hint needs fixing first, e.g. "The P at the end of the acronym is the clue." or "The last word describes the kind of skills taught." Then the English hint should follow it. Fact check: wrong. Hint 3 is false: the acronym CONALEP has no T. It stands for Colegio Nacional de Educación Profesional (only P). The 'T' for Técnica is not in the acronym.
- **q-11697** (tv-shows-and-hosts) Who won the first season of “La Casa de los Famosos México” in 2023? → Wendy Guevara: Hint 2 says "Her videos", but the source's "Sus videos" doesn't mark gender. Wendy Guevara is the only woman among the options, so the pronoun gives the answer away before hint 3. Make hint 2 gender-neutral, e.g. "This contestant's videos went viral on social media."
- **q-13708** (sweets-and-bread) Take a close look at this pastry. What is it called in Mexico? → Dona: source: the fun fact says that in other Spanish-speaking countries a donut is called a “rosquilla”. The fact check marked this wrong: in Spain a rosquilla is a different traditional ring pastry, and donuts there are usually called “donut”/“dónut”. It also clashes with Rosquilla being a wrong answer. Fix the source fun fact, for example by dropping the rosquilla claim or saying it's written “donut”/“dónut” in Spain, then translate again. The rest of the translation is faithful and natural. Fact check: wrong. The fun fact says other Spanish-speaking countries call it a 'rosquilla'. That is misleading. In Spain a rosquilla is a different, traditional ring pastry, and donuts there are usually called 'donut' or 'dónut'. Rosquilla is also used as a wrong answer, so the fact undermines the question.
- **q-14621** (chespirito) In which decade were the famous El Chavo episodes filmed where the neighbors go on vacation to Acapulco? → The 1970s: Source: the description is false, and it is the same in the source. It says Señor Barriga didn't come to collect the rent, but in the Acapulco episodes he does come for it, finds the vecindad empty and takes El Chavo to Acapulco himself. Fix the source description, for example: “The whole vecindad went to the beach, and Señor Barriga ended up there too.” Then translate it again. Fact check: wrong. Answer (1970s) is right (aired May–June 1977), and the fun fact is right. But the description is false: Señor Barriga does come to collect rent. He finds the vecindad empty and takes El Chavo to his favorite hotel in Acapulco, so he is in the episodes.
- **q-14674** (slang) In Mexico, “hacer un bisne” means doing a little business deal. Which language does the word “bisne” come from? → English: The translation glosses “bisne” as “a little business deal”, so the English word “business” sits right next to “bisne” in the question and gives the answer away. The source's “negocito” gave nothing away. Gloss it without the word “business”, for example “making a little deal on the side” or “a small money-making deal”.
- **q-16597** (telenovelas) Angélica Aragón plays María Inés, a woman who falls for a much younger journalist in “Mirada de mujer”. What year did it premiere? → 1997: Fact check: wrong. Alejandro Salas (Ari Telch) is a writer, not a journalist. The 1997 premiere year is correct (June 9, 1997, Azteca Trece).

## Not travelling

- **q-14712** about_language, translate again: Por fin la protagonista le da su cachetada a la villana. ¿Cuál de estas palabras NO significa lo mismo? → Zancadilla (Asks which Spanish word is not a synonym of «cachetada»; an English set of slap synonyms would be a different, forced vocabulary question.)

## Stale re-translated

None.
