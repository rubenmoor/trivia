# tr-en-30

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `mexico` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 289
- Needs work: 8
- Not travelling: 3 (3 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 532, about $30.53 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-30&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-28 | tr-en-29 | tr-en-30 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 298 | 297 |
| not travelling |  | 3 | 2 | 3 |
| not travelling confirmed |  | 2 | 1 | 3 |
| rejected rate | ≤ 20.0 % | 0.7 % ✓ | 0.3 % ✓ | 1.0 % ✓ |
| approved |  | 290 | 293 | 289 |
| needs_work |  | 7 | 5 | 8 |
| needs_work rate | ≤ 20.0 % | 2.4 % ✓ | 1.7 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 1.3 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.3 % ✓ | 1.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.78 | $28.25 | $27.57 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 2 (0 major), overlap 1 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.97

Major findings on approved questions:

None.

## Needs work

- **q-10178** (christmas-season) Look at this close-up: which Mexican plant is the queen of the December holidays? → The poinsettia: This duplicates q-0254, which is already approved: both ask the player to name the poinsettia from a photo of the December plant, and in English both have the answer "poinsettia". The rater flagged this too. Rewording can't fix it, so drop this question or replace it with a different poinsettia fact (for example its Nahuatl name cuetlaxóchitl).
- **q-11638** (slang) In Mexican memes and chats, when someone loses a game or gets left on read, people write “¡pipipipí!”. What does it imitate? → A fake cry: Fact check: uncertain. The one source I found says 'pipipi' comes from El Chavo del 8, where Chavo whines after Don Ramón hits him. It is used to mock a loss. No source describes it as a fake cry, though that reading is plausible.
- **q-11648** (school-and-services) Complete it: CONALEP stands for Colegio Nacional de Educación… → Profesional Técnica: source: hint 3 is false in the source and in the translation. The acronym CONALEP ends in E-P (Educación Profesional) and has no T, so "the P and the T at the end of the acronym" doesn't match the letters and misleads players. The source needs a corrected hint 3, for example "The acronym stops at the P of Profesional; the full name adds one more word." The translation should then follow it. Fact check: wrong. The answer (Profesional Técnica) and the 1978 founding date are right, and the wrong answers are wrong. But hint 3 is false. The acronym CONALEP ends in E-P (Educación Profesional). It has no T, so 'Técnica' isn't represented in it. The 'P and T at the end' clue doesn't match the letters. I checked this from my own knowledge of the name, not with a search.
- **q-12506** (civic-holidays) On May 5, 1862, at the forts of Loreto and Guadalupe, General Ignacio Zaragoza won a battle. Who lost it? → The French: This repeats approved q-12493 ("The date honors the 1862 Battle of Puebla. Whom did Mexico defeat?" → The French army): it asks the same fact with the same answer. Seeing one gives the other away. The translation itself is faithful and reads naturally.
- **q-13554** (landmarks) Look at this sign from one of the longest avenues in Mexico City. Who does its name honor? → The fighters for Independence: source: the essential image is "Nomenclatura urbana Anillo Periférico.jpg". From its title it shows a Periférico street sign, not an "Av. Insurgentes" sign, so players would be asked who a name honors without seeing that name. The source question's media needs replacing with a real Insurgentes sign, or a decorative image and a question that names Avenida Insurgentes. The translated text itself is faithful and reads naturally.
- **q-13708** (sweets-and-bread) Take a close look at this bread. What is it called in Mexico? → Dona: Source: the fun fact says that other Spanish-speaking countries call a donut a “rosquilla”. That is doubtful. In Spain a rosquilla is a different ring pastry, and Spain and much of Latin America just say “donut” or “dona”. The fact check marked it uncertain. Fix the fun fact in the source (for example, keep only “dona comes from the English donut”) and then re-translate. The fact check also flagged “Rosquilla” as a weak distractor, because Mexico has its own ring-shaped rosquillas. Fact check: uncertain. The answer "Dona" is right for Mexico (from English "donut"), and Concha and Rol are clearly different breads. The fun fact is shaky. "Rosquilla" is not a general name for a donut in other Spanish-speaking countries. In Spain it is a different ring-shaped pastry, and Spain mostly says "donut" or "donuts". Mexico also has its own rosquillas (ring-shaped sweet breads or cookies), so it is a weak distractor. I did not run searches; this is from background knowledge.
- **q-15573** (regional-fiestas) It's huge and round, turns slowly and lifts you up high in little cabins to see the whole fair. Which ride is it? → The Ferris wheel: This asks the same fact as approved q-9381 (“What is this ride called?” → Ferris wheel), so it duplicates a question already in the English pool. Source: it also has no link to Mexico, so it doesn't belong in the mexico bundle. The rater flagged both problems.
- **q-15613** (regional-fiestas) I open between April and May, and my dates match the anniversary of the 1862 victory over the French army. Which fair am I? → The Feria de Puebla: source: the clue ("opens between April and May, dates match the anniversary of the 1862 victory") also fits the Feria de San Marcos, one of the wrong answers. It also runs from late April to early May and spans May 5, as the fact check notes. The source needs a Puebla-only clue (e.g. "held beside the forts where the May 5, 1862 victory over the French was won") or a distractor that isn't held in April–May. The English text is a faithful, natural translation. Fact check: wrong. The answer (Feria de Puebla) and the hints and fun fact are true. The Zaragoza and Loreto/Guadalupe facts check out, and the fair is held at the Centro Expositor next to the forts (24 Apr–11 May 2025). The problem is the distractor "Feria de San Marcos". It also opens in April and runs through early May (19 Apr–11 May 2025), so it also spans 5 May. The riddle's clue ("opens between April and May, dates match the anniversary") therefore doesn't clearly rule it out.

## Not travelling

- **q-16485** about_language, confirmed: Al terminar el día o la ceremonia, la bandera se baja con cuidado, como en la foto. ¿Qué verbo se usa para eso? → Arriar (Asks for the Spanish verb «arriar» (to lower a flag); in English the question itself would say the answer ("lower"), and hint 3 plays on the sound of «arriba».)
- **q-17781** wordplay, confirmed: Trabajábamos de sol a sol en las tierras de la hacienda por un pago muy pequeño, y nos llamamos igual que las piezas más pequeñas del ajedrez. ¿Quiénes somos? → Los peones (The clue depends on «peón» meaning both hacienda laborer and chess pawn in Spanish. In English the words are "peon" and "pawn", so the double meaning is lost, and a version explaining it would be strained for a difficulty-3 kids' question.)
- **q-14712** about_language, confirmed: Por fin la protagonista le da su cachetada a la villana. ¿Cuál de estas palabras NO significa lo mismo? → Zancadilla (Asks which Spanish word is not a synonym of “cachetada”; it is a Spanish vocabulary question.)

## Stale re-translated

None.
