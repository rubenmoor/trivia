# tr-en-23

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `spain` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 294
- Needs work: 5
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 537, about $29.86 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-23&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-21 | tr-en-22 | tr-en-23 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 297 | 299 |
| not travelling |  | 0 | 3 | 1 |
| not travelling confirmed |  | 0 | 3 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 1.0 % ✓ | 0.3 % ✓ |
| approved |  | 298 | 289 | 294 |
| needs_work |  | 2 | 8 | 5 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 2.7 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 95.0 % ✓ | 100.0 % ✓ |
| cost $ |  | $22.40 | $25.46 | $27.11 |
| $ per approved |  | $0.08 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: media 1 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.75

Major findings on approved questions:

None.

## Needs work

- **q-12310** (dress-crafts-and-games) Belén figures are sold at the Christmas market in Madrid's Plaza Mayor, and the classic ones are hand-painted. What are they usually made of? → Clay: Fact check: wrong. The description (teaser) says 'the smallest town in all of Spain', which has nothing to do with the question about belén figures and is not true of anything in it. The answer (clay) and the other content are fine.
- **q-12484** (team-and-traditional-sports) Look at the photo: in padel you don't play with a strung racket, but with this. What is it called in Spain? → Pala: Hint 2 adds "also used for a shovel", which isn't in the source. For players with a link to Spain, "shovel" translates straight to "pala", so the answer is given away at hint 2. Keep only the four-letter clue from the source ("In Spanish it's a four-letter word."). Note: the translator's notes (Paddle, Club, six letters) describe an older version and no longer match the text.
- **q-14291** (painting-and-architecture) This carving of the Sacrifice of Isaac, now in Valladolid's National Museum of Sculpture, is by a sculptor who trained in Italy studying Michelangelo. Who? → Alonso Berruguete: Fact check: uncertain. Answer, distractors and hints are right. The fun fact says Berruguete was in Italy when the Laocoön was dug up in 1506, but sources date his Italian stay differently (c. 1504/08, or leaving in 1506). None confirms he was there at the discovery. Britannica does link his work to the Laocoön.
- **q-15435** (tv-series) On TVE, this actor played a policeman solving crimes in late 19th-century Madrid. Which character was it? → Víctor Ros: source: the essential image is "File:Carles Francino i Navarro (2005).jpg". Carles Francino i Navarro (born 1958) is most likely the radio journalist, the father, not the actor (born 1978) who played Víctor Ros. The fun fact itself makes this mix-up likely. Please check the file and replace it with a photo of the actor if it shows the father. The English translation is faithful and natural, with nothing to fix.
- **q-17179** (regional-symbols) This is the coat of arms of Barcelona. How many red crosses can you see on it? → 2: source: The essential image is "File:IV Trobada oficial de Biquipedia.jpg". Going by the title, it is a photo of a Catalan Wikipedia meetup, not the Barcelona coat of arms the question asks players to count crosses on. The source's media slot needs a new file, for example the Commons SVG "Escut de Barcelona.svg". The translated text itself is faithful and fine.

## Not travelling

- **q-13407** other, confirmed: En España, si alguien deja de contestarte de golpe y sin explicación, se dice que te ha «ghosteado». ¿De qué ser viene la palabra? → Un fantasma (In English «ghosteado» visibly contains the word “ghost”, so the question would give its own answer away (and hint 1, “the word comes from English”, is pointless for English speakers).)

## Stale re-translated

None.
