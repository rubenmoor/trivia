# tr-de-12

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 290
- Needs work: 10
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 857, about $42.50 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-12&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-10 | tr-de-11 | tr-de-12 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 300 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 295 | 293 | 290 |
| needs_work |  | 5 | 6 | 10 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 2.0 % ✓ | 3.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.0 % ✓ | 2.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 100.0 % ✓ | 96.7 % ✓ |
| cost $ |  | $38.73 | $38.30 | $38.97 |
| $ per approved |  | $0.13 | $0.13 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), overlap 1 (1 major), media 1 (1 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.54

Major findings on approved questions:

- **q-0647**: media — Essential media is wrong: per its Commons page, the file is Figure 62 of Carter's 1906 book, "Tongs-across-a-wall seat, rear view", a rider's posture plate and not a picture of a stirrup, so "dieses Teil" isn't identifiable (I saw the page text, not the image). The German is faithful and natural, the stirrup facts hold, the wrong answers are really wrong, and no related question overlaps. (http://127.0.0.1:8001/review/q-0647)

## Needs work

- **q-0077** (disney-films) Welche Gabe hat Luisa in „Encanto“? → Übermenschliche Kraft: source: the fun fact is wrong, and the translation carries it over faithfully. Not every Madrigal has a magic door with a gift: Mirabel gets no gift and no door, which drives the plot, and Abuela and those who married in have none either. The source's fun fact should be corrected (e.g. "Each gifted Madrigal child receives a magic door at a ceremony; only Mirabel's never appears"), then the translation updated to match.
- **q-0226** (body-oddities) Wie viel Blut hat ein erwachsener Mensch ungefähr im Körper? → Etwa 5 Liter: source: the fun fact states as plain truth that an adult's blood vessels would circle the Earth more than twice. That rests on the popular figure of about 100 000 km, an old extrapolation; recalculations give only about 9000–19 000 km, which is less than once around. The source needs a safer fun fact, and the translation should then follow it.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: This asks the same fact as approved q-0369 (the country the Rubik's Cube comes from, answer Ungarn) in slightly different words, so one of the two should be dropped. If the Spanish pool holds the same pair, the duplicate is in source: too. The translation itself is otherwise fine.
- **q-0954** (greek-heroes) Rate mal: „Eine Göttin ließ mich nur noch wiederholen, was andere zuletzt sagten, und ich liebte einen Jungen, der sich nur im Wasser ansah.“ Wer bin ich? → Echo: source: the fun fact reverses the etymology. Greek "ēchō" was already the ordinary word for a sound, and the nymph is named after it or personifies it, so the word doesn't come from her. The source's fun fact has the same error, so correct it there, for example: "Die Nymphe trägt das griechische Wort für Schall als Namen, und vom jungen Narziss stammt das Wort „Narzisst“." The translation itself is faithful.
- **q-1296** (horror-films) Ich bin das Monster aus einem Animationsfilm von 2006: Meine Tür ist mein Mund, mein Teppich meine Zunge, und ich verschlucke Bälle. Was bin ich? → Haus: source: hint 1 is factually wrong, in the Spanish source and faithfully in the translation. In the climax of Monster House, the house tears itself from its foundations and chases the children, so "Ich laufe nicht: Ich rühre mich nie von meiner Straße weg" is untrue. The source's hint needs correcting, for example to a vague hint about the suburban neighbourhood or the fear of the kids next door; the German should then follow it.
- **q-3681** (fashion-history) Ich trage einen weißen Anzug, dicke Handschuhe und einen Hut mit Netz vor dem Gesicht und habe eine kleine Rauchdose dabei. Wer bin ich? → Imker: Overlaps q-9291 (approved, same answer "Imker"): both identify the beekeeper by description, and both use the veiled hat, so one of the two should go. Separately, "Rauchdose" is a literal translation of "smoke can" and isn't natural German; if this question is kept, use "Rauchgerät" or similar.
- **q-4866** (stars-and-galaxies) Welche Raumfahrtagentur schickte 2013 die Sonde Gaia ins All, um die Positionen von über einer Milliarde Sternen zu vermessen? → ESA: source: the fun fact says in the present tense that Gaia measures star positions ("measures" / "misst"), but Gaia ended science operations in January 2025 and was switched off in March 2025. Correct the source to the past tense ("measured"), then carry that into the German ("Gaia maß Sternpositionen so genau, ...").
- **q-5667** (pirates) Von solchen Barren träumten Piraten. Aus welchem Metall sind sie? → Gold: Fact check: wrong. The third hint is wrong: gold is a metal, but 'Seine Farbe hat denselben Namen wie das Metall' is fine for gold, but the second hint is wrong: Olympic winners get a gold medal, which is actually mostly silver plated with about 6 g of gold. The medal only 'looks like' gold, so this hint is OK. The fun fact is also misleading: gold doesn't rust, but 'Piraten' bars in wrecks are mostly unverified. Also the hint 'Olympiasieger bekommen eine Medaille, die so aussieht' gives away the answer too directly. Overall the answer 'Gold' is right and the wrong answers are wrong, but I could not verify every detail with a search.
- **q-6297** (formula-1-and-motorsport) Rennteams wechseln so mitten im Rennen die Reifen. In welchem Bereich der Strecke arbeiten sie dabei? → Boxengasse: Fact check: uncertain. I checked this from background knowledge and ran no searches. Answer Boxengasse is correct and the wrong answers are clearly wrong. The F1 pit lane limit is usually 80 km/h (60 km/h at some tracks), and speeding is penalised. Each team has its own garage there. Guido changes Lightning McQueen's tires in Cars. The description line 'schneller als ein Nieser' is doubtful: a pit stop takes about 2 s (record about 1.8 s), and a sneeze lasts about a second or more, so the claim is not clearly true.
- **q-6407** (pyramids) Du stehst im Dschungel Kambodschas vor Prasat Thom, der siebenstufigen Pyramide von Koh Ker. In welchem Jahrhundert wurde sie gebaut? → 10. Jahrhundert n. Chr.: Source: hint 3 is wrong. Jayavarman IV reigned until about 941; 944 is when Koh Ker stopped being the capital, under his successor Harshavarman II. Correct it in the source, e.g. "ruled from Koh Ker from about 928 to 941", then carry the change into the German hint 3.

## Not travelling

None.

## Stale re-translated

None.
