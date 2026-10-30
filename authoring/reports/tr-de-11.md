# tr-de-11

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 293
- Needs work: 6
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 841, about $41.89 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-11&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-9 | tr-de-10 | tr-de-11 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 292 | 295 | 293 |
| needs_work |  | 8 | 5 | 6 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | 1.7 % ✓ | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.0 % ✓ | 1.3 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 100.0 % ✓ |
| cost $ |  | $37.42 | $38.73 | $38.30 |
| $ per approved |  | $0.13 | $0.13 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: giveaway 7 (0 major), fact 2 (0 major), overlap 1 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.59

Major findings on approved questions:

None.

## Needs work

- **q-0077** (disney-films) Welche Gabe hat Luisa im Film „Encanto“? → Übermenschlich stark sein: source: the fun fact is wrong in the Spanish source, and the translation repeats it. Not every Madrigal has a magic door: Mirabel gets no gift or door at her ceremony, and those who married in (Agustín, Félix) have none. The source needs correcting, e.g. "Jedes Madrigal-Kind mit einer Gabe bekommt eine magische Tür mit eigenem Zimmer."
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Same fact as approved q-0369 ("Aus welchem Land stammt der Zauberwürfel…?", answer Ungarn): both ask for the Rubik's Cube's country of origin. One of the two should be dropped; rewording can't solve this without making it a different question.
- **q-0660** (cartoons) Was haben die Erfindungen Zoetrop, Thaumatrop und Praxinoskop aus dem 19. Jahrhundert gemeinsam? → Täuschen Bewegung vor: source: the fact itself is flawed, and the German translation carries it over faithfully. The classic thaumatrope blends two images into one static picture (bird in cage), so "Täuschen Bewegung vor" doesn't properly hold for all three devices. Hint 2 (drawings changing slightly from frame to frame) and hint 3 also don't fit it. The source should be corrected, e.g. by swapping the thaumatrope for another true animation device such as the phenakistiscope, or by asking about persistence of vision. Fact check: wrong. The thaumatrope (1824) does not fake motion. It has one image on each side of a disc, and spinning it blends the two into one picture, such as a bird in a cage. So "Täuschen Bewegung vor" is wrong for it. Hint 2 (drawings that change slightly from frame to frame) and hint 3 (drawings seem to come alive) only fit the zoetrope and praxinoscope. What all three share is persistence of vision.
- **q-1529** (harry-potter) Harry schenkt seinem geerbten Hauselfen ein falsches Medaillon, und der Griesgram wird freundlich. Von wem, dem der Elf am liebsten diente, stammte es? → Regulus Black: The second sentence, "Von wem, dem der Elf am liebsten diente, stammte es?", is translationese: a relative clause hung on an interrogative is stilted and hard to follow when read aloud. The masculine "dem" also leans towards a male person and so against Walburga and Bellatrix, which the translator's note meant to avoid. Suggested rewording: "Harry schenkt dem griesgrämigen Hauselfen, den er geerbt hat, ein falsches Medaillon, und der Elf wird freundlich. Wem gehörte es?", possibly with a neutral phrase for the elf's favourite such as "seiner liebsten Bezugsperson aus der Familie".
- **q-2912** (world-cuisines) Ich bin ein süßer Klassiker aus Schichten von Schokobiskuit, Schlagsahne und kleinen roten Früchten. Was bin ich? → Schwarzwälder Kirschtorte: The kept image, a sharp photo of a bowl of cherries, is a giveaway in German. The answer is the only option with "Kirsch" in its name, and the translation deliberately hides the cherries as "kleine rote Früchte". The German version needs a different file or a blurred decorative one, such as a generic cake or bakery scene without cherries. The text itself is fine.
- **q-3968** (space-race-and-astronauts) Wie heißt die Geschwindigkeit, die ein Objekt braucht, um die Erde zu umkreisen und um sie herumzufallen, ohne je aufzuschlagen? → Orbitalgeschwindigkeit: Fact check: uncertain. Answer, wrong answers and hints are correct (orbital speed; the ISS flies about 27,600 km/h, so 'rund 28 000' is fine). The fun fact is imprecise. At about 7.66 km/s, a typical crossing (New York–London or Lisbon, about 5,500 km) takes roughly 12 minutes, not 15. 15 minutes would need about 6,900 km, which is more than most routes. This check is from my own calculation and general knowledge. I ran no searches.

## Not travelling

- **q-0381** other, confirmed: Si en Alemania alguien te dice 'Danke', ¿qué te está diciendo? → Gracias (The question asks what the German word 'Danke' means. For German-speaking players this is trivial and pointless; no fair equivalent keeps the same fact and answer.)

## Stale re-translated

None.
