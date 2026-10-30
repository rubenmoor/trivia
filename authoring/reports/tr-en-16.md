# tr-en-16

Made by `qgen batch --translate en` on 2026-10-30 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 5 (0 stale re-translated)
- Translated: 5
- Approved: 0
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 21, about $2.52 at list price; – per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-16&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-14 | tr-en-15 | tr-en-16 |
|---|---|---:|---:|---:|
| sources |  | 12 | 5 | 5 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 12 | 5 | 5 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 7 | 0 | 0 |
| needs_work |  | 5 | 5 | 5 |
| needs_work rate | ≤ 20.0 % | 41.7 % ✗ | 100.0 % ✗ | 100.0 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 41.7 % ✗ | 100.0 % ✗ | 100.0 % ✗ |
| needs_work: ambiguity | ≤ 10.0 % | 8.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 12 | 5 | 5 |
| audit/review agreement | ≥ 90.0 % | 58.3 % ✗ | 0.0 % ✗ | 20.0 % ✗ |
| cost $ |  | $2.46 | $1.37 | $1.46 |
| $ per approved |  | $0.35 | n/a | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 0
- Major among review needs work: 1 of 5 (20 %)
- Problems by kind: fact 2 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 5 (0 %)
- Audit/review agreement (both accept or both not): 1 of 5 (20 %)
- Sample: 5 audited of 5; 5 Claude calls, about $1.06

Major findings on approved questions:

None.

## Needs work

- **q-7049** (ghosts-and-creatures) According to folk tradition, if you sprinkle holy water in the corners of your house, who runs away? → Witches: Fact check: uncertain. The answer 'witches' fits folk belief (holy water repels witches, evil spirits, the devil), and the wrong answers (thieves, neighbors, debt collectors) are clearly wrong. But I found no source that documents this specific belief for Colombia, only the general practice of sprinkling holy water in corners, doors and windows for protection. Another answer such as 'evil spirits' or 'the devil' is at least as common in the tradition. The hint 'they get around on a broom' is generic witch lore. The fun fact is generally true.
- **q-7365** (mountains-and-landscapes) It falls from the clouds on stormy afternoons, sounds very loud on tin roofs and can turn streets white. What falls in a hailstorm? → Balls of ice: source: the fun fact's claim that ice piled up to almost 1 m on some Bogotá streets is unconfirmed. The fact check verifies the November 3, 2007 hailstorm but found no source for the depth, and I can't confirm it from my own knowledge. The translation renders the source faithfully, so the source's fun fact needs correcting first, for example: "On November 3, 2007, a hailstorm in Bogotá, the strongest in almost 40 years, covered streets in ice and interrupted the Rock al Parque festival." Fact check: uncertain. The answer (balls of ice), the wrong answers and the hints are fine. The fun fact is only partly verified. A major Bogotá hailstorm on 3 Nov 2007 is well documented. It is described as the strongest in almost 40 years, and it interrupted Rock al Parque. I found no source saying the ice piled up to almost 1 m in some streets. Sources mention only streets covered in ice and flooded.
- **q-7416** (scientists-and-inventors) The 20,000-peso bill shows Julio Garavito's face and a drawing of the Moon, and a lunar crater bears his name. Why? → Because he studied the Moon's motion: source: the question says the 20,000-peso bill shows Julio Garavito in the present tense (“lleva”), but the current series, issued since 2016, has Alfonso López Michelsen on the 20,000. Garavito was on the earlier design, so both the source and this faithful translation are out of date and need rewording, e.g. “The old 20,000-peso bill showed…”.
- **q-7821** (home-school-and-paperwork) It stays at the bottom of the rice pot, comes out toasted and crunchy, and families fight over it. What do Colombians call it? → Pegao: Fact check: uncertain. The crispy rice at the bottom of the pot is usually called 'pega' (Andean region) or 'cucayo/cucallo' (Caribbean coast); 'pegao' is used informally and is the common name in the Caribbean/Puerto Rico, but it is not clearly THE Colombian term. 'Chicharras' is also a regional name. 'Cuncho' (which in Colombia often means dregs or sediment) was not confirmed as a name for this rice, but I can't fully rule it out as a regional variant. The hint 'stays stuck to the pot' gives it away. The fun fact about rice cookers is unverified.
- **q-8225** (popular-and-andean-music) I'm a paisa pasillo heard at every wedding, graduation and birthday, and I make parents cry. What song am I? → “El camino de la vida”: source: the fact check is 'wrong'. It says sources classify “El camino de la vida” as a bambuco, not a pasillo, and I can't confirm “pasillo” from my own knowledge. The source's “pasillo paisa” carries the same claim, so the source needs correcting first, for example to “paisa song” or “paisa bambuco”; then the translation can follow it. The translation itself is faithful. Fact check: wrong. The question calls the song a "paisa pasillo", but sources classify "El camino de la vida" as a bambuco, not a pasillo. The rest holds up: the author is Héctor Ochoa, the lyrics follow the stages of life, and in 1999 the Academia Colombiana de Música chose it as Colombian Song of the 20th century. The other options (Pueblito viejo, Los guaduales, Espumas) are different songs. I did not check whether they fit the "wrong answer" role beyond that. One source says the song is not clearly tied to pasillo, and I found none that calls it one.

## Not travelling

None.

## Stale re-translated

None.
