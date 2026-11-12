# tr-en-24

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `mexico` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 535, about $26.94 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-24&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-22 | tr-en-23 | tr-en-24 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 299 | 300 |
| not travelling |  | 3 | 1 | 0 |
| not travelling confirmed |  | 3 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 1.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 289 | 294 | 295 |
| needs_work |  | 8 | 5 | 5 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | 1.7 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $25.46 | $27.11 | $24.58 |
| $ per approved |  | $0.09 | $0.09 | $0.08 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 4 (0 major), overlap 1 (0 major), media 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.36

Major findings on approved questions:

None.

## Needs work

- **q-10406** (drinks) The torito, a party drink from Veracruz, has aguardiente and fruit or peanut. What other ingredient makes it creamy? → Condensed milk: Source: the fun fact says toritos are sold in Tlacotalpan and Alvarado. The fact check could only confirm Tlacotalpan, and I can't confirm Alvarado either. The source's fun fact should be fixed first (e.g. "sold in Tlacotalpan and across Veracruz"), then the translation re-run. Apart from that, the translation is faithful and reads naturally. Fact check: uncertain. Answer (condensed milk) is supported: torito is made with aguardiente, evaporated milk and condensed milk, plus fruit or peanut. Wrong answers (egg yolk, corn masa, pulque) are not standard ingredients. But the fun fact's claim that toritos are sold in Alvarado could not be verified; only Tlacotalpan was confirmed. Also, evaporated milk is also used, so 'condensed milk' is not the only creamy ingredient.
- **q-11569** (telenovelas) In many telenovelas, a poor, kind young woman falls in love with a rich man and marries him. Which fairy tale is that story like? → Cinderella: The translation itself is faithful and reads naturally, but it asks the same fact as approved q-4746: a poor, kind girl marries a rich man, so it's "a Cinderella story". Anyone who plays both gets a duplicate. Source: the Spanish original has the same overlap, so drop or replace the question at the source level.
- **q-12685** (sayings) You're invited out with a group that's always getting into trouble, and you'd rather stay home. Complete: “Más vale solo que…” → Mal acompañado: Hint 2 (“The ending is about who you're with.”) gives the answer away: “Mal acompañado” is the only option about company, so the hint points straight to it. The source's hint only narrowed it to the two “Mal…” options. Hint 2 needs a vaguer replacement that doesn't point to company, for example one that says the ending has two words and rhymes with nothing in particular, or one about the tone of the warning.
- **q-16598** (telenovelas) The whole family gathers in front of the TV to watch me, the streets go empty and the villain finally gets punished. What am I? → The final episode: Fact check: uncertain. The answer (the final episode) fits the riddle, and the wrong answers are clearly wrong. The empty-streets effect is documented: Cuna de lobos' finale on 5 June 1987 emptied Mexico City streets and reached about 73 rating points. I couldn't find a source for the fun fact's claim that people moved parties and weddings to catch finales. It's plausible but unverified.
- **q-17723** (pre-hispanic-gods) She was the Tlaxcaltec water goddess, her name means “the one with the blue skirt,” and it's the old name of a volcano in Tlaxcala. Who is she? → Matlalcueye: Fact check: uncertain. Matlalcueye ("owner of the blue skirt"), the Tlaxcalan water goddess and old name of La Malinche, checks out. But sources say she is a Tlaxcalan form of, or closely related to, Chalchiuhtlicue ("jade skirt"), which is one of the wrong answers. That makes the distractor arguable. Chalchiuhtlicue is also the deity usually called Tláloc's consort, so the hint "Tláloc's partner" fits both. I didn't check the volcano's height or the Puebla/Tlaxcala visibility; the Wikipedia figure I recall is about 4,461 m, which would fit "more than 4,400 m".

## Not travelling

None.

## Stale re-translated

None.
