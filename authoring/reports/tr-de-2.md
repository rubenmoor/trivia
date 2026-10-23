# tr-de-2

Made by `qgen batch --translate de` on 2026-10-23 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 290
- Needs work: 7
- Not travelling: 2 (2 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 1402, about $28.95 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-2&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-1 | tr-de-2 |
|---|---|---:|---:|
| sources |  | 50 | 300 |
| stale re-translated |  | 0 | 0 |
| translated |  | 50 | 297 |
| not travelling |  | 0 | 2 |
| not travelling confirmed |  | 0 | 2 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.7 % ✓ |
| approved |  | 50 | 290 |
| needs_work |  | 0 | 7 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 2.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 1.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 |
| audit/review agreement | ≥ 90.0 % | 80.0 % ✗ | 95.0 % ✓ |
| cost $ |  | $6.59 | $26.97 |
| $ per approved |  | $0.13 | $0.09 |
| **health** | | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 59 (3 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 6 (2 major), media 1 (1 major), style 7 (1 major), other 1 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $1.97

Major findings on approved questions:

- **q-0895**: style, giveaway, other — The source is a word riddle built on the many meanings of Spanish „claro“ (light colour, clear water, clear sky, „ok“). In German, „Lichtung“ has none of those meanings, so the three wrong answers (clear river, white trunk, cloudless day) lose their point and look random. What's left is just "what does the word Lichtung mean", which any German speaker answers from the word itself. The description's „ein Licht aufgeht“ also points at the light in the answer. This item should have been marked not-travelling (wordplay/about_language), or rebuilt as a plain question about rainforest gaps. (http://127.0.0.1:8001/review/q-0895)
- **q-1679**: media, giveaway — The essential image, "Portrait of Sherlock Holmes by Sidney Paget", appears with the question. It shows the answer, deerstalker and all, and its title names him. The image should be decorative (e.g. a Victorian London street) or illustrative without Holmes. The translation itself is accurate and natural ("Pater Brown", „die Frau“), and the facts about Irene Adler and the hints are correct. (http://127.0.0.1:8001/review/q-1679)

## Needs work

- **q-1822** (world-religions) Wer versteckt zu Ostern in vielen Ländern solche bunten Eier? → Osterhase: Hint 1 („Er kommt jedes Jahr im Frühling.“) gives the answer away. „Er“ rules out Zahnfee (sie) and Christkind (es) by grammar, and „Frühling“ rules out Weihnachtsmann. Hint 1 should use a gender-neutral wording (e.g. „Diese Figur …“) and a vague clue that doesn't point to the season. Hints 2 and 3 should also avoid „Er“ (e.g. „Lange Ohren gehören dazu.“).
- **q-2776** (marvel-superheroes) Beast trat zum ersten Mal in „X-Men #1“ auf, zusammen mit dem Originalteam. In welchem Jahrzehnt erschien dieses Heft? → 1960er-Jahre: source: the fun fact says Beast turned blue only in 1975. As far as I know he got grey fur in Amazing Adventures #11 (1972) and was coloured blue later in that same series (around 1972–73), well before his 1975 Avengers stint. The translator and the rater both doubted the date. The source's fun fact should drop or correct the blue year (e.g. "Sein Fell bekam er erst 1972, zuerst sogar grau."), and then the translation should follow it.
- **q-3568** (natures-records) Schau genau hin: Welches Tier hat das gebaut? → Honigbiene: Fact check: uncertain. The answer Honigbiene and the fun fact are right (about 2 million flowers per pound, or about 500 g, of honey is the commonly cited figure). However, the text clue only mentions hexagonal rooms, and paper wasps (Wespe) also build hexagonal cells. The distractor 'Wespe' is therefore only clearly wrong if the image shows wax comb filled with honey. I did not run searches. This is from general knowledge.

## Not travelling

- **q-1692** about_language, confirmed: Me pongo en las pestañas para que se vean largas y oscuras, y mi nombre viene de un perfumista del siglo XIX. ¿Qué soy? → El rímel (The clue relies on the Spanish word 'rímel', which comes from Eugène Rimmel. In German the product is called 'Wimperntusche' or 'Mascara', and neither word comes from Rimmel, so the clue would be false. Hint 3 also uses a Spanish rhyme ('nivel').)
- **q-1252** needs_local_knowledge, confirmed: ¿Cuál de estos payasos NO formó parte de 'Los Payasos de la Tele' junto con Miliki? → Cepillín (Los Payasos de la Tele (Gaby, Fofó, Miliki, Fofito) and Cepillín are known only in Spain and Latin America; German players can't tell them apart.)

## Stale re-translated

None.
