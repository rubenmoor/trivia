# tr-de-13

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 291
- Needs work: 9
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 878, about $44.68 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-13&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-11 | tr-de-12 | tr-de-13 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 293 | 290 | 291 |
| needs_work |  | 6 | 10 | 9 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 3.3 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 2.7 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 1.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 96.7 % ✓ | 95.0 % ✓ |
| cost $ |  | $38.30 | $38.97 | $40.85 |
| $ per approved |  | $0.13 | $0.13 | $0.14 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 7 (0 major), fact 4 (0 major), ambiguity 1 (1 major), media 2 (0 major), style 2 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.82

Major findings on approved questions:

- **q-3873**: ambiguity, style — The description „In jedem Krimi das, worauf am Ende alle im Gerichtssaal warten.“ departs from the source (collecting evidence like stickers). What everyone waits for at the end of a trial is the verdict, so it describes the wrong option „Urteil“, says something untrue of the answer, and is a fragment rather than a full sentence; it should go back to the source joke. The rest holds: the answer and wrong options are fine, „Jeder Kontakt hinterlässt eine Spur“ is Locard's principle, there is no overlap with q-5424 or q-5694, and difficulty 5 fits. (http://127.0.0.1:8001/review/q-3873)

## Needs work

- **q-0870** (video-game-characters) Aus welchem Land stammt Metal Gear, die 1987 gestartete Spielereihe um den Spion Solid Snake? → Japan: source: the fun fact calls MSX a console, but MSX/MSX2 was a home computer standard. The translator, rater and fact check all flagged this. The source's fun fact should say "home computer"; the German should then read "MSX-Heimcomputer" instead of "MSX-Konsole".
- **q-1147** (fast-food) Mein Gesicht mit weißem Anzug und Spitzbart prangt auf Eimern voller Brathähnchen. Welcher US-Bundesstaat steckt im Namen meiner Kette? → Kentucky: source: the fun fact is false in both the source and the translation. Harland Sanders enlisted in the US Army in 1906 and served in Cuba, so "war gar kein Soldat" is wrong; only the "Colonel" title was honorary (a Kentucky colonel). The source needs correcting first, e.g. "'Colonel' war nie sein Dienstgrad, sondern ein Ehrentitel des Bundesstaats Kentucky", which should also name him as "Harland Sanders" because the name appears nowhere earlier. Secondary: the first-person riddle asks for a fact other than the speaker's identity, so it reads as a plain question in disguise; the source has the same form, and a direct question would be better, e.g. "Ein Mann mit weißem Anzug und Spitzbart prangt auf Eimern voller Brathähnchen. Welcher US-Bundesstaat steckt im Namen der Kette?".
- **q-1296** (horror-films) Ich bin das Monster aus einem Animationsfilm von 2006: Meine Tür ist mein Mund, mein Teppich meine Zunge, und ich verschlucke Bälle. Was bin ich? → Haus: source: hint 1 ("Ich laufe nicht: Aus meiner Straße komme ich nie weg" / "No camino: nunca me muevo de mi calle") is factually wrong for the film. In the climax of Monster House the house tears itself from its foundations and chases the children. The German is faithful, so the source hint needs correcting (e.g. a vague hint that it waits for visitors to come close), then the translation should follow.
- **q-1648** (world-currencies) Ich bin die Münze mit dem kleinsten Wert in Japan und wiege genau 1 Gramm. Aus welchem Metall bin ich? → Aluminium: The question is a first-person riddle that asks for another fact (the coin's metal) than the speaker's identity, so it is a plain question in disguise (reason 6). The same form is in the source. A direct wording would solve it: „Japans Münze mit dem kleinsten Wert wiegt genau 1 Gramm. Aus welchem Metall besteht sie?“
- **q-1952** (winter-olympics) Wann finden die Winter-Paralympics im Vergleich zu den Olympischen Winterspielen statt? → Kurz danach, am selben Ort: source: hint 2 („Sie finden nie vor den Olympischen Spielen statt“ / "Nunca se celebran antes…") is historically false. The 1980 Geilo and 1984 Innsbruck Winter Paralympics took place before the Winter Olympics of those years. The source hint should say "today" or "nowadays" (e.g. „Heute kommen sie nie zuerst dran“), and the translation should then follow it.
- **q-2369** (consoles-and-game-companies) „Fünfzig Spieler springen per Fallschirm über meiner Insel ab, nur der Letzte, der übrig bleibt, gewinnt. Free Fire ist eines meiner bekanntesten Spiele.“ Welche Spielart bin ich? → Battle Royale: The question text is 179 characters, over the 160-character limit for German (source: about 130), so it can't be read in one breath. It could be cut to e.g. „50 Spieler springen per Fallschirm auf meine Insel, nur einer bleibt übrig. Ein Beispiel: Free Fire.“ Welche Spielart bin ich?
- **q-3464** (international-football) Welcher Verein hat Europas wichtigsten Klubpokal, den Europapokal der Landesmeister oder die Champions League, am häufigsten gewonnen? → Real Madrid: source: the media file is a photo of Real Madrid celebrating the 2018 Champions League title, and it is shown sharp. Going by its title, it shows the answer's team with the trophy, so it gives the answer away. The slot needs a new file, such as the trophy alone or a neutral stadium. The German text itself is fine.
- **q-3681** (fashion-history) Ich trage einen weißen Anzug, dicke Handschuhe, einen Hut mit Netz vor dem Gesicht und habe eine kleine Rauchdose dabei. Wer bin ich? → Imker: Duplicate of approved q-9291: same answer (Imker) and the same core clue (a hat with veil or net, working with bees), so seeing one gives the other away. If this one is kept anyway, also replace the awkward 'Rauchdose' with a natural word such as 'Rauchgerät' or 'Smoker'.
- **q-5332** (birds) Ein Schwan kann nicht richtig tauchen, hat einen sehr langen Hals und kippt oft kopfüber, den Schwanz in der Luft. Wonach streckt er sich dabei meist? → Wasserpflanzen: source: hint 1 says swans feed only where the water is shallow enough for their neck to reach the bottom, but swans also graze on land (fields, meadows) and take food from the surface. The German copies this faithfully, so the source hint needs correcting, for example to "When they tip up, swans can only reach food where the water is shallow enough for their neck to reach the bottom." The German can then follow.

## Not travelling

None.

## Stale re-translated

None.
