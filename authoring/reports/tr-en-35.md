# tr-en-35

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `spain` questions translated into English. Generated file: don't edit by hand.

- Sources: 256 (0 stale re-translated)
- Translated: 255
- Approved: 249
- Needs work: 6
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 420, about $27.79 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-35&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-33 | tr-en-34 | tr-en-35 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 256 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 298 | 296 | 255 |
| not travelling |  | 2 | 4 | 1 |
| not travelling confirmed |  | 2 | 3 | 1 |
| rejected rate | ≤ 20.0 % | 0.7 % ✓ | 1.0 % ✓ | 0.4 % ✓ |
| approved |  | 292 | 289 | 249 |
| needs_work |  | 6 | 7 | 6 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 2.4 % ✓ | 2.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 1.7 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.99 | $26.06 | $24.49 |
| $ per approved |  | $0.10 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 1 (0 major), fact 3 (0 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.30

Major findings on approved questions:

None.

## Needs work

- **q-11126** (childrens-tv) This song is sung again and again, swapping words for gestures: “My beard has three hairs, three hairs has my beard; if it didn't have three hairs…”. How does it go on? → …it wouldn't be a beard: Fact check: uncertain. The song is a Spanish clowns' game, and the usual lyric ends "no sería mi barba" (my beard), not "una barba". The answer "it wouldn't be a beard" is close, and the wrong answers are clearly wrong. The fun fact is unsupported. The source describes the rounds as banning "barba", then "barba" and "pelos", and ending with a faster full sing-through. It does not describe a nearly silent last round with a chin point and three fingers. I could not find the lyric text itself.
- **q-11228** (painting-and-architecture) It's a bronze statue by Ricardo Bellver that shows Lucifer falling from heaven, and it sits on top of a fountain. Which park is it in? → Retiro Park in Madrid: source: hint 3 is wrong. The Fuente del Ángel Caído stands in the southern part of the Retiro, a few hundred meters from the Palacio de Cristal, so the Palacio is not "right next to it" ("junto a él"). The source hint needs rewording (for example "The Palacio de Cristal is in the same park"), and the translation should then follow it. Otherwise the English is faithful and natural.
- **q-12350** (money-and-services) Look at this 1-cent euro coin. It is copper-colored on the outside, but what metal is it on the inside? → Steel: The kept media file is "Didymograptus artos.1 - Ordovicico medio.JPG", a graptolite fossil, but this is an essential slot and the question says "Look at this 1-cent euro coin". The file has to be replaced with a clear photo of a 1-cent euro coin, ideally the Spanish side showing Santiago de Compostela cathedral. This is in the source item too. The English text is a faithful, natural translation and needs no changes.
- **q-12449** (scientists-and-explorers) Karlos Arguiñano is to cooking as Jesús Calleja is to… → adventure: Source: the fun fact says Jesús Calleja was born in Madrid. As far as I know he was born in León in 1965, as the rater also noted. The source's fun fact needs correcting first, for example to say he was born and raised in León, and then the translation should follow it. Otherwise the translation is faithful and reads naturally.
- **q-13455** (sportspeople) I'm from Mallorca, I won Roland Garros in 1998, I was the first Spanish world No. 1, and years later I coached Rafa Nadal. Who am I? → Carlos Moyá: Source: "the first Spanish world No. 1" is false as written. Arantxa Sánchez Vicario reached WTA No. 1 in February 1995, four years before Moyá. Moyá was the first Spanish man to be world No. 1. The source should say “first Spanish man to be world No. 1” (“primer español” reads as men only in Spanish, but the English loses that), and then the translation should follow it.
- **q-16384** (scientists-and-explorers) INTA runs this huge antenna in Robledo de Chavela, near Madrid. What is it for? → Talking to faraway spacecraft: Source: the fun fact says Robledo tracks "the Voyager probes", but only Voyager 1 is visible from Madrid. Voyager 2 is far south in the sky and can only be reached from Canberra. The source fun fact should name Voyager 1 only ("Robledo still tracks Voyager 1, which has already left the solar system"), and the translation should then follow. Otherwise the translation is faithful and natural.

## Not travelling

- **q-11130** about_language, confirmed: ¿Cuál de estas frases NO es un trabalenguas? → «Más vale pájaro en mano que ciento volando» (Spotting the tongue twisters depends on how the Spanish phrases sound; in English it can't be read aloud or judged fairly.)

## Stale re-translated

None.
