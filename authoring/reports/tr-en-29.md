# tr-en-29

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `spain` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 298
- Approved: 293
- Needs work: 5
- Not travelling: 2 (1 confirmed → `translatable: false`, 1 translated again next run)
- Claude calls: 522, about $31.57 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-29&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-27 | tr-en-28 | tr-en-29 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 297 | 298 |
| not travelling |  | 1 | 3 | 2 |
| not travelling confirmed |  | 0 | 2 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.3 % ✓ |
| approved |  | 290 | 290 | 293 |
| needs_work |  | 9 | 7 | 5 |
| needs_work rate | ≤ 20.0 % | 3.0 % ✓ | 2.4 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.3 % ✓ | 1.7 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $25.38 | $27.78 | $28.25 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), fact 3 (0 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.32

Major findings on approved questions:

None.

## Needs work

- **q-11126** (childrens-tv) In the gesture song «Mi barba tiene tres pelos», words get swapped for actions: “My beard has three hairs, three hairs has my beard; if it didn't have three hairs…”. How does it go on? → …then it wouldn't be a beard: Fact check: uncertain. The answer fits the song: without the three hairs, it wouldn't be a beard. The usual line is "no sería mi barba" ("wouldn't be my beard"), a minor difference. The wrong answers are wrong. The fun fact is shaky. In the standard game, each word (barba, pelos, tres, tiene and so on) is replaced by its own gesture, not just a chin point and three fingers. One source summary said the final round is the full song sung fast, which conflicts with the fun fact. I couldn't see the exact lyrics or the last-round rules.
- **q-12489** (tv-series) Who is this host of the «Grand Prix del verano»? → Ramón García: Source: hint 3 is false. Santiago Ramón y Cajal's first name is Santiago, and "Ramón" is his first surname, so the hint says something untrue in both languages. Source hint 1 ("presenta el programa desde los años 90") also suggests he hosted without a break, when he hosted 1995–2005 and again from 2023. Fix the source (e.g. "Comparte su nombre con el primer apellido de Ramón y Cajal" and "Lo presentó en los 90 y volvió a hacerlo en 2023"), then translate it again. Fact check: wrong. Hint 3 is false: Santiago Ramón y Cajal's first name is Santiago; 'Ramón' is part of his surname. The answer is otherwise right.
- **q-12491** (tv-shows-and-presenters) I'm Basque, an actor and stand-up comic, and in 1999 I started asking questions on Telecinco to people who wanted to be millionaires. Who am I? → Carlos Sobera: Source: the fact check rates calling Carlos Sobera a "stand-up comic" (Spanish "monologuista") as wrong, and I can't confirm it either. He is known as an actor and TV presenter, and earlier was a lawyer and lecturer. The source should say "actor and TV presenter", and then the translation should follow. Also, hint 3 names "First Dates", and the draft q-11425 calls it "Carlos Sobera's blind-date show", so the two overlap if both get approved. Fact check: wrong. The riddle calls Carlos Sobera a 'stand-up comic', but no source describes him that way. He is an actor and TV presenter, and a former lawyer and lecturer. The rest checks out: born in Barakaldo, hosted ¿Quién quiere ser millonario? on Telecinco from 1999, and hosts First Dates on Cuatro.
- **q-13295** (footballers-and-national-team) You're watching Spain's national team play in red. Which Spanish player does NOT wear the red shirt? → The goalkeeper: The translation is accurate, but it asks the same fact as the approved base question q-6292 ("which player must wear a shirt of a different color from all the teammates?" → the goalkeeper). English players of the spain bundle also get base questions, so they could meet both, and one gives the other away. The only Spanish touch is the red shirt. Consider dropping this item, or replacing the source with a question that really needs Spain.
- **q-16197** (cities-and-towns) In Seville's Semana Santa, I walk slowly behind the pasos in a robe, with my face covered and a tall pointed capirote on my head. Who am I? → The nazareno: Source error: the riddle says the nazareno walks "behind the pasos" (source: "tras los pasos"), but in Seville's processions the nazarenos' rows walk in front of each paso, and the paso closes its section. Fix the Spanish source first (e.g. "delante de los pasos" or "acompaño a los pasos"), then re-translate. Otherwise the translation is faithful and natural. Fact check: wrong. The riddle says the nazareno walks 'behind the pasos'. In Seville's processions, nazarenos walk in front of each paso (the paso comes at the end of its section, followed by the band). Answer, wrong answers, hints and fun fact are otherwise fine.

## Not travelling

- **q-17184** about_language, translate again: En los libros de historia se habla a menudo de militares que se «sublevaron». ¿Qué significa «sublevarse»? → Rebelarse contra el gobierno (Asks the meaning of an ordinary Spanish verb (“sublevarse”), not a Spain-specific term; in English it becomes either a Spanish vocabulary test or a trivial question about “rise up”.)
- **q-16307** about_language, confirmed: Esta es la catedral de Murcia. ¿Cómo se llama a una persona nacida en esa ciudad? → Murciano (Asks how a Spanish demonym is formed (-ano vs -ense/-ino, plus a murciélago joke option); in English it would just be “Murcian” with no fair invented alternatives.)

## Stale re-translated

None.
