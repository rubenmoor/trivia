# tr-en-3

Made by `qgen batch --translate en` on 2026-10-28 (plan 66, D-81): `base` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 295
- Approved: 292
- Needs work: 3
- Not travelling: 5 (4 confirmed → `translatable: false`, 1 translated again next run)
- Claude calls: 679, about $30.65 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-3&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-1 | tr-en-2 | tr-en-3 |
|---|---|---:|---:|---:|
| sources |  | 50 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 49 | 291 | 295 |
| not travelling |  | 1 | 9 | 5 |
| not travelling confirmed |  | 1 | 9 | 4 |
| rejected rate | ≤ 20.0 % | 2.0 % ✓ | 3.0 % ✓ | 1.3 % ✓ |
| approved |  | 49 | 282 | 292 |
| needs_work |  | 0 | 9 | 3 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 3.1 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 2.1 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 49 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 83.7 % ✗ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $5.55 | $27.69 | $27.75 |
| $ per approved |  | $0.11 | $0.10 | $0.10 |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 5 (0 major), overlap 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.90

Major findings on approved questions:

None.

## Needs work

- **q-0317** (knights) Look at the photo: what is this piece of a knight’s armor called? → Helm: Fact check: wrong. The answer (Helm) and the wrong answers (breastplate, gauntlet, greave) are right, and the hints are fine. The fun fact overstates the weight. Surviving 13th-century great helms weigh about 1.5–3 kg: examples are 2.26 kg, 2.7 kg and a Templar-style helm at 3.0 kg. 4 kg (9 lb) is above that range.
- **q-0878** (pirates) My name is course. Pirates set me before they sail, the helmsman keeps me all voyage, and the captain shouts to change me. What do I show? → Which way the ship is sailing: Fact check: uncertain. The answer and wrong answers are fine: a ship's course is its heading, not speed, cargo or depth. The fun fact is shaky. "Course" comes from Latin cursus ('a running, path') through Old French cours, so the word was not born at sea. Only the phrase "off course" is plausibly nautical in origin. I did not run searches, so this rests on my own knowledge of the etymology.
- **q-2145** (rock) In what year did the Beatles release their famous album “Sgt. Pepper's”? → 1967: Fact check: wrong. The answer (1967), the wrong answers, the hints and the fun fact are all correct. I checked this from memory and ran no searches. The media query is the problem: "Abbey Road zebra crossing" is the cover of a different album (1969), not Sgt. Pepper's. It would show the wrong album next to the question.

## Not travelling

- **q-0788** about_language, confirmed: Soy la palabra 'retahíla'. ¿Qué significo? → Una serie larga de cosas dichas una tras otra (Asks what the Spanish word “retahíla” means. The hints and description also depend on its Spanish spelling (the accent) and on Spanish children's counting-out rhymes. No English word works the same way.)
- **q-1017** about_language, confirmed: En España, el juego de sacar papelitos y dar un regalo sin revelar a quién te tocó no se llama 'amigo secreto'. ¿Cómo lo llaman allá? → Amigo invisible (Asks which Spanish adjective Spain uses for the gift-swap game (amigo invisible vs. amigo secreto), and the hints play on Spanish words. It doesn't work in English.)
- **q-1710** about_language, translate again: Soy un refrán: «Muerto el perro, se acabó la rabia». ¿Qué enseño? → Si quitas la causa, se acaba el problema (Asks the meaning of a Spanish proverb with no English dog-based equivalent; the hints and a wrong answer rely on Spanish “rabia” meaning both rabies and anger.)
- **q-1605** about_language, confirmed: Adivina: me llamo Dairy Queen, vendo helados y mi nombre en inglés significa 'la reina de los…'. ¿De qué soy reina? → De los lácteos (The question asks what the English word 'Dairy' in 'Dairy Queen' means. In English the answer is in the brand name itself, so there is nothing left to guess.)
- **q-1201** about_language, confirmed: Es un tubérculo dulce y anaranjado por dentro; en México le dicen 'camote' y en España 'boniato'. ¿Qué es? → La batata (The clue is the Spanish regional names (camote, boniato, batata). Hints 1 and 3 work on Spanish words: “papa dulce” translates to the English answer, and “sounds like patata” only works in Spanish. Also, in the US sweet potatoes are often called “yams”, so the yam distractor could count as correct.)

## Stale re-translated

None.
