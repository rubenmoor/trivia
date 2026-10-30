# tr-de-14

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 291
- Needs work: 9
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 859, about $43.88 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-14&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-12 | tr-de-13 | tr-de-14 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 290 | 291 | 291 |
| needs_work |  | 10 | 9 | 9 |
| needs_work rate | ≤ 20.0 % | 3.3 % ✓ | 3.0 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.7 % ✓ | 1.7 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 1.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 95.0 % ✓ | 95.0 % ✓ |
| cost $ |  | $38.97 | $40.85 | $39.80 |
| $ per approved |  | $0.13 | $0.14 | $0.14 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 58 (3 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 8 (2 major), fact 2 (0 major), overlap 1 (1 major), media 2 (1 major), difficulty 1 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.08

Major findings on approved questions:

- **q-1914**: giveaway, difficulty — Question text: German "beitreten" only collocates with organisations, so it rules out all three wrong answers (nobody "tritt" a tax, a workshop or a fair "bei"). This is stronger than the source's "entrar a", and players can reason to "Vereinigung" without knowing the word, so it plays nearer 6 than 9; a neutral wording such as "kam an der Zunft nicht vorbei" would fix it. Facts, the fun fact (Meisterstück), hints, option grammar, media and related questions are fine; no fact search was needed. (http://127.0.0.1:8001/review/q-1914)
- **q-4756**: media, giveaway — The source's illustrative file 'Sillustani flocks of sheeps in Péru(1).jpg' names the answer in its title and, shown sharp, presumably shows sheep, so the picture points straight at 'Schaf'; it needs a sheep-free Andean image (not viewed, judged from the title; this is a source media issue, not a translation fault). Otherwise the fact holds (llama, vicuña and camel are camelids, sheep is not), the German is natural and faithful, the options have no article issues, and the difficulty fits. (http://127.0.0.1:8001/review/q-4756)

## Needs work

- **q-0077** (disney-films) Was ist Luisas magische Gabe in „Encanto“? → Übermenschlich stark sein: source: the fun fact is wrong in the source, and the translation repeats it. Not every Madrigal has a magic door: Mirabel has none during the film, and Abuela Alma and the in-laws have none either. Correct the source to limit it to family members with a gift, e.g. "Jedes Familienmitglied mit einer Gabe hat eine magische Tür, die sie zeigt."
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicates approved q-0369 ("Aus welchem Land stammt der Zauberwürfel…?", answer Ungarn): it is the same fact with the same answer, in other words. One of the two should be dropped from the German pool; a rewrite would make it a different question.
- **q-0860** (christmas) Lappland ist die verschneite Region im äußersten Norden Europas, wo angeblich der Weihnachtsmann wohnt. Welches dieser Länder hat keinen Anteil daran? → Dänemark: source: hint 1 says Lapland lies within the Arctic Circle, but this is wrong for much of the region: Finnish Lapland extends south of the circle (Rovaniemi sits on it), and roughly half of Swedish Lappland lies south of it. The German hint faithfully copies this, so the source hint needs correcting, for example to "Ein großer Teil Lapplands liegt nördlich des Polarkreises."
- **q-0954** (greek-heroes) Rate mal: „Eine Göttin ließ mich nur noch das Letzte wiederholen, was andere sagen, und ich liebte einen Jungen, der nur sich im Wasser ansah.“ Wer bin ich? → Echo: source: the fun fact reverses the etymology. Greek "ēchō" (sound) is the ordinary word and the nymph is named after it, so the word "Echo" does not come from her. The German translation faithfully carries over this error from the source, which needs correcting first (e.g. "Die Nymphe Echo trägt das griechische Wort für Schall als Namen, und vom jungen Narziss kommt „Narzisst“.").
- **q-1952** (winter-olympics) Wann finden die Winter-Paralympics statt, verglichen mit den Olympischen Winterspielen? → Kurz danach, am selben Austragungsort: source: hint 2 ("Sie finden nie vor den Olympischen Spielen statt" / "Nunca se celebran antes que los Juegos Olímpicos") is historically false. The 1984 and 1988 Winter Paralympics in Innsbruck took place in January, before the Sarajevo and Calgary Winter Games in February. The source needs correcting (e.g. "Heute finden sie nie vor…"), and the German can then follow; the translation itself is faithful.
- **q-4282** (extreme-sports) Schau dir diese Nahaufnahme an. Wozu gehören diese Räder? → Inlineskates: Hint 3 is inaccurate: 'Rollhockey' in German normally means the sport played on quad roller skates, not inline skates, and the fact check flagged it as wrong. Reword it to something generic like 'Beim Hockey auf Rollen'; 'Inlinehockey', the fact check's correction, would echo the answer. Fact check: wrong. Minor: hint 3 names 'Rollhockey', which in German is normally played on quad roller skates, not inline skates.
- **q-4727** (space-race-and-astronauts) Bei Apollo 17 brach an diesem Mondauto ein Kotflügel ab, und es schleuderte überall Staub herum. Womit reparierten die Astronauten ihn? → Landkarten und Klebeband: source: hint 2 ("One of the items was made of paper") is factually wrong. The Apollo 17 replacement fender was made from four stiff, coated cronopaque map sheets (plastic film), held with duct tape and clamps, so the maps weren't paper. The source and translation should say something like "Eines der beiden Dinge diente sonst zur Orientierung".
- **q-5506** (french-revolution) „Links“ und „rechts“ in der Politik stammen aus einer Versammlung während einer Revolution: Die Anhänger des Königs saßen rechts vom Präsidenten. In welchem Land? → Frankreich: source: hint 3 is wrong in the English source, and the German copies it. The Assembly met in the Salle des Menus-Plaisirs in the town of Versailles, not in the Palace of Versailles. Correct the source hint to something like "The assembly first met in the town of Versailles", then carry that into the German ("Die Versammlung tagte zuerst in der Stadt Versailles.").
- **q-6098** (world-war-ii) Japan, eine der Achsenmächte, griff im Dezember 1941 einen US-Marinestützpunkt auf Hawaii an. Was war die Folge? → Die USA traten in den Krieg ein: Duplicates approved q-5553: both ask what the Pearl Harbor attack led to, and both answer that the USA entered the war, so seeing one gives the other away. The translation itself is faithful; the overlap comes from the source, so one of the two should be dropped.

## Not travelling

None.

## Stale re-translated

None.
