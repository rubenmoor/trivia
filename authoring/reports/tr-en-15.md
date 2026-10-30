# tr-en-15

Made by `qgen batch --translate en` on 2026-10-30 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 5 (0 stale re-translated)
- Translated: 5
- Approved: 0
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 21, about $2.26 at list price; – per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-15&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-13 | tr-en-14 | tr-en-15 |
|---|---|---:|---:|---:|
| sources |  | 274 | 12 | 5 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 272 | 12 | 5 |
| not travelling |  | 2 | 0 | 0 |
| not travelling confirmed |  | 2 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 260 | 7 | 0 |
| needs_work |  | 12 | 5 | 5 |
| needs_work rate | ≤ 20.0 % | 4.4 % ✓ | 41.7 % ✗ | 100.0 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 4.4 % ✓ | 41.7 % ✗ | 100.0 % ✗ |
| needs_work: ambiguity | ≤ 10.0 % | 0.4 % ✓ | 8.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 12 | 5 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 58.3 % ✗ | 0.0 % ✗ |
| cost $ |  | $31.57 | $2.46 | $1.37 |
| $ per approved |  | $0.12 | $0.35 | n/a |
| **health** | | ✓ pass | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 0
- Major among review needs work: 0 of 5 (0 %)
- Problems by kind: fact 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 5 (0 %)
- Audit/review agreement (both accept or both not): 0 of 5 (0 %)
- Sample: 5 audited of 5; 5 Claude calls, about $0.89

Major findings on approved questions:

None.

## Needs work

- **q-7049** (ghosts-and-creatures) According to popular tradition, if you sprinkle holy water in the corners of the house, who runs away? → Witches: Fact check: uncertain. I found no source for the specific Colombian tradition that sprinkling holy water in house corners makes witches flee. Sources only show the Catholic and esoteric practice of sprinkling holy water in corners for protection against evil. Witches as the answer is plausible. The wrong answers (thieves, neighbors, debt collectors) are clearly not the folk-belief answer. The hints (flying at night, broomsticks) are generic folklore. The fun fact about fonts at church entrances and people taking holy water home is generally true. The first hint ('haven't come to borrow money') is odd and unhelpful.
- **q-7365** (mountains-and-landscapes) It falls from the clouds on stormy afternoons, pounds on tin roofs and can turn the streets white. What falls in a hailstorm? → Little balls of ice: source: the fun fact's depth claim, repeated faithfully from the Spanish, is unconfirmed. The fact check found no source for "almost 1 meter" of ice in the November 3, 2007 Bogotá hailstorm, and I can't confirm it either. The source needs correcting, for example by dropping the depth: "On November 3, 2007, the strongest hailstorm in almost 40 years hit Bogotá, flooding streets and burying cars under ice." Fact check: uncertain. The answer (little balls of ice) is right, and the wrong answers (snow, ash, sand) are wrong. The hints are fine. The storm date is real: a record hailstorm hit Bogotá on Nov 3, 2007. I found no source for the 'almost 1 meter (3 ft) deep' figure. The only depth I found was 24 inches (~60 cm), and that was for a March 2015 storm in southern Bogotá, not 2007. The fun fact's depth is probably exaggerated or invented.
- **q-7416** (scientists-and-inventors) The 20,000-peso banknote shows Julio Garavito and a drawing of the Moon, and a lunar crater bears his name. Why? → Because he studied the Moon's motion: source: the present tense “shows” is out of date. Since the 2016 series, the 20,000-peso note has shown Alfonso López Michelsen, and Garavito was on the previous series. The Spanish source (“lleva”) has the same error and should be corrected there, for example “The old 20,000-peso banknote showed…”. The translation is otherwise faithful.
- **q-7821** (home-school-and-paperwork) It stays at the bottom of the rice pot, comes out toasted and crispy, and many families fight over it. What is it called in Colombia? → Pegao: Fact check: uncertain. "Pegao" (pega/pegao) is a real Colombian name for the crispy rice crust, so the answer is plausible. However, the Caribbean coast's most common name is "cucayo", and "pegao" is mainly Andean/Antillean, so "Colombia" is somewhat ambiguous. I found no source showing "cuncho" means this in Colombia. Some dictionaries list "cuncho" as a Colombian word for dregs or residue, and I couldn't rule out regional use for rice. Hint 1 ("its Spanish name says where it stays") is vague. The rice-cooker fun fact is plausible but I couldn't verify it.
- **q-8225** (popular-and-andean-music) I'm a paisa pasillo heard at every wedding, graduation and birthday, and I make parents cry. What song am I? → “El camino de la vida”: source: the Spanish question calls “El camino de la vida” a “pasillo paisa”, and the translation repeats this. The fact check says sources classify it as a bambuco, and I can't confirm “pasillo” from my own knowledge. Correct the source first, using “bambuco paisa” or a genre-free “canción paisa”, then carry that into the English. Fact check: wrong. The question calls the song a 'paisa pasillo', but sources classify "El camino de la vida" as a bambuco, not a pasillo. The answer, the composer (Héctor Ochoa), the wrong answers, the lyric themes and the fun fact (chosen Colombian song of the 20th century, by a 1999 poll and the Academia Colombiana de Música) all check out.

## Not travelling

None.

## Stale re-translated

None.
