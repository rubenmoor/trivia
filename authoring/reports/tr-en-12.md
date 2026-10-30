# tr-en-12

Made by `qgen batch --translate en` on 2026-10-30 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 286
- Needs work: 13
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 509, about $31.96 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-12&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-10 | tr-en-11 | tr-en-12 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 298 | 299 | 299 |
| not travelling |  | 2 | 1 | 1 |
| not travelling confirmed |  | 1 | 1 | 1 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| approved |  | 290 | 281 | 286 |
| needs_work |  | 8 | 18 | 13 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | 6.0 % ✓ | 4.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 5.4 % ✓ | 3.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✗ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 93.3 % ✓ | 91.7 % ✓ | 96.7 % ✓ |
| cost $ |  | $26.76 | $27.60 | $28.57 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 57 (0 %)
- Major among review needs work: 1 of 3 (33 %)
- Problems by kind: giveaway 3 (0 major), overlap 2 (1 major), media 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.39

Major findings on approved questions:

None.

## Needs work

- **q-0232** (sweets-and-desserts) What fruit is bocadillo veleño made from? → Guava: Overlap: the approved q-7574 opens with “Bocadillo veleño (guava paste)”, which gives away this question's answer to anyone who has seen it. The cleanest fix is in q-7574: drop the “(guava paste)” gloss (or say “a fruit paste”). That question doesn't need the gloss to ask about the bijao leaf. Once that's done, this translation can be approved as it is.
- **q-7019** (carnivals-and-fairs) On January 5 in Pasto, people paint your face black. According to tradition, who asked for that day off in colonial times? → Enslaved Africans: Fact check: uncertain. The answer (enslaved Africans) is consistent across sources. The fun fact is shaky: sources disagree on the origin. One says a 1607 uprising in Remedios, Antioquia, led to the day off. Others say the enslaved people asked for it in Popayán. Others date it to 1854. The question says 'colonial times', but 1854 is after independence. 'Spanish Crown granted it after an uprising in 1607 (in Pasto)' is not well supported. The hint 'It happened in the 17th century' is also not firmly established.
- **q-7128** (rhythms-dances-and-instruments) In Colombia, someone invites you to «echar un pie». What are they suggesting? → Go dancing: Fact check: uncertain. "Echar un pie" does mean to dance, but sources place it in the Caribbean, Venezuela and Cuba/salsa contexts. I found no source calling it Colombian. The fun fact says "In Colombia", and I couldn't verify that. "Tirar paso" is Colombian, and "mover el esqueleto" is general Spanish.
- **q-7365** (mountains-and-landscapes) It falls from the clouds on stormy afternoons, sounds super loud on tin roofs and can turn streets white. What falls in a granizada? → Little balls of ice: Fact check: uncertain. The Nov 3, 2007 Bogotá hailstorm is real (strongest in ~40 years). I found no source for the "almost 1 meter (3 ft) high" depth. Sources say only that cars were buried and streets flooded.
- **q-7399** (transport) In Colombia, an autopista is to asphalt as a trocha is to… → packed dirt: The English version of related q-5243 says "a muddy trocha (dirt track)". That gloss gives away this question's answer, "packed dirt". The fix belongs in q-5243: drop the "(dirt track)" gloss there or reword it so it doesn't define trocha. This translation itself is faithful and reads naturally.
- **q-7783** (words) In Colombia, what do you call a group of friends who go out together to have a good time? → El parche: Source: the fun fact's "parchesazo" can't be confirmed. The fact check is uncertain, the translator flagged it, and the usual Colombian augmentative is "parchazo". The source's fun fact should be corrected to "parchazo" or replaced with a fact that can be checked, for example that "parchar" means to hang out. The translation itself is faithful. Fact check: uncertain. "El parche" is right for a group of friends and for a plan, and the wrong answers don't fit Colombia. I could not verify the fun fact's "parchesazo" as a real Colombian term. One search found no usage of it.
- **q-7803** (carnivals-and-fairs) At town fiestas, people light buscapiés. Going by its name, what does a buscapiés do once lit? → It runs along the ground through the crowd: Fact check: uncertain. Answer, wrong answers and hints fit the name (buscapiés = ground-running firework that 'chases feet'). But I found no source saying the buscapiés was used at Spanish fiestas centuries ago. Sources only show similar ground-running devices (ratas de tierra) in older Spanish pyrotechnics.
- **q-7821** (home-school-and-paperwork) It's left at the bottom of the rice pot, comes out toasty and crunchy, and families fight over it. What do Colombians call it? → Pegao: Fact check: uncertain. 'Pegao' (or 'pega') is a valid Colombian name for the rice crust, mainly in Antioquia, Bogotá and the Andean region. The Caribbean coast says 'cucayo', so the answer is region-dependent. 'Cuncho' is listed as a wrong answer, but it is a documented Latin American word for dregs or residue at the bottom of a pot. My searches did not confirm or rule out its use for rice crust in Colombia, so it may be a valid alternative. The question also says 'What do Colombians call it?', which implies a single name. The 'Cuncho' distractor is risky, and 'Calentado' (reheated leftovers) is fine.
- **q-7870** (places-and-monuments) The Torre Colpatria in downtown Bogotá has 50 floors, stands 196 m (643 ft) tall, and at night its facade lights up in colors. What is it mainly used for? → Offices: source: the description calls Colpatria "Bogotá's tallest" (Christmas tree), but Torre BD Bacatá (about 216 m, finished 2016) is now taller than Colpatria (196 m), so the claim is out of date. Fix the source description first (e.g. "One of Bogotá's tallest Christmas trees, lit up all year round") and then translate it again. The rest of the translation is faithful and reads naturally. Fact check: wrong. The fun fact says 'almost one thousand steps'. That is fine, since sources give about 980 steps and an annual climb race. But the description calls it 'Bogotá's tallest' tower. Torre BD Bacatá (216 m, completed 2016) is taller than Colpatria (196 m), so that claim is outdated.
- **q-7914** (places-and-monuments) At Medellín's most famous fair, the silleteros parade carrying silletas on their backs. What are those silletas made of? → Flowers: Fact check: wrong. Text content is right (silletas are made of flowers, Feria de las Flores, some weigh 60+ kg). But the media query 'Medellin metrocable' does not match the question; the image would show a cable car, not silleteros.
- **q-8225** (popular-and-andean-music) I'm a pasillo from Antioquia, heard at every wedding, graduation and birthday, and I make dads cry. Which song am I? → “El camino de la vida”: source: the riddle calls “El camino de la vida” a pasillo, but the fact check says sources describe it as a vals (waltz) or bambuco, and I can't confirm it is a pasillo. The source should say something like “I'm a song from Antioquia” instead. The fun fact could also add that the vote was in 1999. Once the source is fixed, the translation needs the same change. Fact check: wrong. The answer song and composer are right (Héctor Ochoa; 1999 chosen as Colombian song of the 20th century). But the riddle calls it a "pasillo", and no source supports that. Radio Nacional describes it as a nostalgic vals (waltz), and other sources say bambuco or vals.
- **q-8265** (cycling) In the Vuelta a Colombia, a car from each team follows the riders, with bikes on the roof and the director inside. What is it for? → To hand out spare parts, water and instructions: source: the fun fact says commentators call it “el bidón pegado”. The fact check found no sign of that term in use (Spanish sources say “bidón pegajoso”), and I can't confirm it. The source's fun fact needs correcting first, and then the translation should follow it. Apart from that, the translation is faithful and natural US English. Fact check: wrong. The fun fact gives "el bidón pegado" as a Spanish commentators' term. It looks invented. Spanish sources use "bidón pegajoso" for the sticky bottle. Nothing found shows "bidón pegado" in use. The rest of the question (answer, wrong answers, hints) is fine.
- **q-8288** (painters-sculptors-and-museums) I'm a painter from Bogotá: I studied art in Japan in the 1930s and painted the savanna and misty páramos in the style of Japanese prints. Who am I? → Gonzalo Ariza: Source: the fact check is uncertain, and I can't confirm two claims from my own knowledge. One is the fun fact that Ariza was "one of the first Latin American artists to study in Japan" and that it "shaped all his work". The other is the question's "in the style of Japanese prints"; sources describe a looser Japanese influence. The source should soften both, for example "with a Japanese-influenced eye" and "Ariza was the first Colombian to exhibit in Japan". The translation follows the source faithfully and reads naturally. Fact check: uncertain. Ariza (Bogotá, 1912–1995) did live in Japan and was the first Colombian to exhibit there. Sources disagree on the dates: one says he returned in 1938, another says he stayed until 1958. A Banco de la República article says Japanese influence on his work is faint and more philosophical than stylistic, so "in the style of Japanese prints" is doubtful. I found no source for the fun fact that he was one of the first Latin American artists to study in Japan, or that the experience "shaped all his work".

## Not travelling

- **q-6885** about_language, confirmed: En Cali dicen «vos sabés», «mirá, ve» y «¿vos qué querés?». ¿Cómo se llama esta manera de tratar a alguien? → El voseo (Asks for the Spanish grammar term for a form of address (voseo vs tuteo/ustedeo/seseo); the hints rely on Spanish verb forms.)

## Stale re-translated

None.
