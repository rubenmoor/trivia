# tr-en-7

Made by `qgen batch --translate en` on 2026-10-29 (plan 66, D-81): `base` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 295
- Approved: 293
- Needs work: 2
- Not travelling: 5 (5 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 652, about $31.05 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-7&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-5 | tr-en-6 | tr-en-7 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 289 | 300 | 295 |
| not travelling |  | 11 | 0 | 5 |
| not travelling confirmed |  | 11 | 0 | 5 |
| rejected rate | ≤ 20.0 % | 3.7 % ✓ | 0.0 % ✓ | 1.7 % ✓ |
| approved |  | 288 | 295 | 293 |
| needs_work |  | 1 | 5 | 2 |
| needs_work rate | ≤ 20.0 % | 0.3 % ✓ | 1.7 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 1.3 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 100.0 % ✓ |
| cost $ |  | $26.46 | $23.46 | $28.15 |
| $ per approved |  | $0.09 | $0.08 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 4 (0 major), fact 1 (0 major), ambiguity 1 (0 major), overlap 1 (0 major), media 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.90

Major findings on approved questions:

None.

## Needs work

- **q-0792** (literature) Content, cheerful, joyful, sad, furious: how many of these words are synonyms of “happy”? → 3: Fact check: wrong. Content, cheerful and joyful are all synonyms of happy, so 3 is right. But the description says 'Twin words that look nothing alike but mean the same thing', which is off for this question. The fun fact (car/auto/automobile/motorcar) is true but only loosely related. The third hint, 'Furious doesn't work either', is fine. The main problem is the description, which doesn't match the question. 'Content' is also a slightly weaker synonym (it means satisfied), so the answer is arguable.
- **q-1530** (harry-potter) What is the magic game, a bit like marbles, where the pieces squirt a smelly liquid at a player who loses a point? → Gobstones: Fact check: uncertain. The answer is right. The smelly squirt, the marbles comparison and Eileen Prince as club captain are confirmed. Two claims are not supported. Rowling's site says the stones may be made of 'precious metals', not specifically 'solid gold'. I also found no source for 'Harry sees other students playing it at Hogwarts'. The Gobstones Club first appears in Order of the Phoenix.

## Not travelling

- **q-0952** about_language, confirmed: Es una palabra del diccionario que empieza con 'gat', pero no tiene nada que ver con animales. ¿Qué significa 'gatuperio'? → Un enredo o mezcla turbia (Asks what the Spanish dictionary word “gatuperio” means and plays on its “gat-” (cat) start; there is no English word that works the same way.)
- **q-0113** about_language, confirmed: ¿Cuál es el plural de 'lápiz'? → Lápices (Asks how a Spanish word is spelled in the plural (lápiz → lápices). The z-to-c rule has no English equivalent, so the question can't be asked fairly in English.)
- **q-1983** about_language, confirmed: Soy la parte de la canción que se repite y todos corean. Mi nombre viene de un objeto. ¿De cuál? → Del estribo (The question depends on the Spanish word “estribillo” (chorus) coming from “estribo” (stirrup). English “chorus” has no such link to an object, so there is no clean equivalent.)
- **q-1095** about_language, confirmed: ¿Qué significa decir que alguien es 'el perejil de todas las salsas'? → Que se mete en todo (Asks what a Spanish idiom (“el perejil de todas las salsas”) means; English has no parsley idiom, so a literal version would be a question about Spanish.)
- **q-1028** about_language, confirmed: El diamante de los Sims se llama 'plumbob', como la pesa colgada de un hilo con la que el albañil revisa si una pared está derecha. ¿Cómo se llama en español? → Plomada (Asks for the Spanish word for the tool (plomada). In English the tool is the “plumb bob”, which the question already names, so nothing is left to ask.)

## Stale re-translated

None.
