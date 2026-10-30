# tr-en-14

Made by `qgen batch --translate en` on 2026-10-30 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 12 (0 stale re-translated)
- Translated: 12
- Approved: 7
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 46, about $4.69 at list price; $0.35 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-14&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-12 | tr-en-13 | tr-en-14 |
|---|---|---:|---:|---:|
| sources |  | 300 | 274 | 12 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 272 | 12 |
| not travelling |  | 1 | 2 | 0 |
| not travelling confirmed |  | 1 | 2 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| approved |  | 286 | 260 | 7 |
| needs_work |  | 13 | 12 | 5 |
| needs_work rate | ≤ 20.0 % | 4.3 % ✓ | 4.4 % ✓ | 41.7 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.7 % ✓ | 4.4 % ✓ | 41.7 % ✗ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.4 % ✓ | 8.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 12 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 95.0 % ✓ | 58.3 % ✗ |
| cost $ |  | $28.57 | $31.57 | $2.46 |
| $ per approved |  | $0.10 | $0.12 | $0.35 |
| **health** | | ✓ pass | ✓ pass | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 7 (14 %)
- Major among review needs work: 1 of 5 (20 %)
- Problems by kind: giveaway 3 (0 major), fact 6 (2 major), ambiguity 1 (1 major), media 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 12 (0 %)
- Audit/review agreement (both accept or both not): 7 of 12 (58 %)
- Sample: 12 audited of 12; 12 Claude calls, about $2.23

Major findings on approved questions:

- **q-8302**: fact, ambiguity — source: the wrong answer “Boredom” is defensible and may be the real meaning. AsiHablamos and Jergozo, both from a Barranquilla contributor, define Caribbean-coast “pava” / “cule pava” as boredom or annoyance (“esta fiesta es cule pava”, “estudiar me empava”). The bad-luck sense is tied by the RAE to Venezuela, and I found no source for it in Barranquilla (“pavoso” and “echar la pava” unconfirmed for Colombia; only a forum snippet and collaborative sources were available, the WordReference thread could not be opened). Replace the “Boredom” option at minimum and verify the Barranquilla bad-luck claim against a Colombian dictionary; the translation itself is faithful and natural. (http://127.0.0.1:8001/review/q-8302)

## Needs work

- **q-7049** (ghosts-and-creatures) According to folk tradition, if you sprinkle holy water in the corners of your house, who runs away? → Witches: Fact check: uncertain. I found no source for the Colombia-specific belief that holy water in the house corners makes witches run away. The common folk and Catholic accounts say it drives off the devil, evil spirits or bad energy. Witches are plausible, since the question's hints (broomstick, flying at night) point to them. The hints themselves are fine, and the wrong answers (thieves, neighbors, debt collectors) are clearly wrong. The fun fact is plausible but I didn't verify it. Hint 1 is vague. 'Evil spirits' or 'the devil' would be the better-documented answer.
- **q-7365** (mountains-and-landscapes) It falls from the clouds on rainy afternoons, pounds on zinc roofs and can turn the streets white. What falls in a hailstorm? → Balls of ice: source: the fun fact's claim that ice piled up nearly 1 meter deep in Bogotá on November 3, 2007 is unconfirmed. The fact check found no source for it and one summary suggested about 20 cm, and I can't confirm it either. Correct the Spanish source first, for example to "strongest hailstorm in almost 40 years; it covered streets in ice and buried dozens of cars", then carry the change over to the translation. Fact check: uncertain. The answer (balls of ice) is correct and the wrong answers (snow, ash, sand) are wrong. The hints are fine. The fun fact's date (Nov 3, 2007) and its status as Bogotá's strongest hailstorm in about 40 years are confirmed. I found no source for 'nearly 1 meter (3 ft) deep'. Reports only say streets turned white and dozens of cars were buried. One search summary gave about 20 cm, but I couldn't tell whether that figure belongs to the 2007 storm. The question's stem also says it 'falls from the clouds ... pounds on zinc roofs', which is a loose description and not a factual error.
- **q-7416** (scientists-and-inventors) The 20,000-peso banknote shows Julio Garavito and a drawing of the Moon, and a lunar crater bears his name. Why? → Because he studied the Moon's motion: source: "shows" (Spanish "lleva") is out of date. Since the 2016 series, the 20,000-peso note has shown Alfonso López Michelsen, and Garavito and the Moon appear only on the earlier series. The fact check missed this, and the rater flagged it. The source should change to the past tense ("showed" / "llevaba", or "the old 20,000-peso banknote"), and the translation should then follow it.
- **q-7821** (home-school-and-paperwork) It stays at the bottom of the rice pot, comes out toasted and crunchy, and families fight over it. What do Colombians call it? → Pegao: Source: the translation is faithful, but the fact check is uncertain on points I can't confirm either. "Cuncho" is Colombian for residue or dregs at the bottom of a pot, so it may be a defensible name for the same thing, and the claim that rice cookers leave almost no pegao, "which is why" people prefer pots, is unverified. The source needs a clearly wrong replacement for "Cuncho" and a softer or sourced fun fact; "pegao" itself is fine as a Colombian word, though "pega" and "cucayo" are also regional names. Fact check: uncertain. "Pegao" is used in Colombia, but sources mostly give cucayo/cucallo (Caribbean coast) and pega (Andean region) as the Colombian names. Pegao is the usual name in Puerto Rico. The wrong answer "Cuncho" could not be ruled out: the Spanish dictionary may list it in Colombia for the rice stuck to the pot, but I found no source for that. The fun fact about rice cookers was not verified. One source mentions a rice cooker designed to make pegao.
- **q-8225** (popular-and-andean-music) I’m a pasillo paisa heard at every wedding, graduation and birthday, and I make parents cry. What song am I? → “El camino de la vida”: source: the error is in the Spanish source and the translation copies it faithfully. It calls “El camino de la vida” a pasillo, but the fact check found sources calling it a bambuco (El Comercio) or a vals (Portafolio). The source should drop the genre (“a paisa song”), then the translation can follow. Fact check: wrong. The song is not a pasillo. Sources call "El camino de la vida" a bambuco (El Comercio); Portafolio calls it a vals. The composer (Héctor Ochoa), the theme and the "Colombian Song of the 20th century" title (1999 poll) check out. The wrong answers are fine: Pueblito viejo, Los guaduales and Espumas are different songs.

## Not travelling

None.

## Stale re-translated

None.
