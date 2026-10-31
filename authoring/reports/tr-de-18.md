# tr-de-18

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 275
- Needs work: 25
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 816, about $44.76 at list price; $0.15 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-18&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-16 | tr-de-17 | tr-de-18 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 284 | 282 | 275 |
| needs_work |  | 16 | 18 | 25 |
| needs_work rate | ≤ 20.0 % | 5.3 % ✓ | 6.0 % ✓ | 8.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 4.3 % ✓ | 5.0 % ✓ | 6.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 1.0 % ✓ | 2.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 96.7 % ✓ | 93.3 % ✓ |
| cost $ |  | $39.74 | $39.28 | $40.38 |
| $ per approved |  | $0.14 | $0.14 | $0.15 |
| **health** | | ✓ pass | ✓ pass | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 1 of 5 (20 %)
- Problems by kind: giveaway 4 (0 major), fact 5 (0 major), overlap 1 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.39

Major findings on approved questions:

None.

## Needs work

- **q-0228** (deserts) Wie heißt die größte heiße Wüste der Welt? → Sahara: q-0228 duplicates approved q-0731: both ask for the world's largest hot desert, with the answer Sahara. Only one of them should stay in the pool. The same duplicate exists in the source, and the translation itself is otherwise fine.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicate: q-0369 (approved) already asks for the Rubik's cube's country of origin, with the same answer, Ungarn. Only one of the two should stay in the German pool; the rater's no_overlap note flags the same thing.
- **q-0343** (magic) Welche Enkelin von Abuela Alma bekam in „Encanto“ keine Gabe, weil ihre magische Tür nie aufleuchtete? → Mirabel: source: the clue that the door never lit up ("nunca se iluminó" / "nie aufleuchtete") looks wrong. In the film, Mirabel's door glows when she touches it at her ceremony, then fades and vanishes, as the rater also noted. The translation is faithful, so the source needs correcting, e.g. "because her magic door vanished at her ceremony"; the translation can then follow.
- **q-0548** (countries) Wie heißen diese riesigen Steinstatuen auf der Osterinsel? → Moai: source: hint 2 ("Casi todas son cabezas gigantes…", translated as "Fast alle sind riesige Köpfe…") repeats a misconception. Moai are full figures with torsos, and the question's own fun fact says bodies lie below the heads. The source hint should say something like "huge heads on stone bodies, with long noses and stern brows", and the translation should follow it.
- **q-0870** (video-game-characters) Aus welchem Land stammt Metal Gear, die 1987 gestartete Spielereihe um den Spion Solid Snake? → Japan: source: the fun fact calls the MSX a console ("consola"), but it was a home computer standard, not a console. The German "die Konsole MSX" repeats this error, so the source fun fact needs correcting to "Heimcomputer"/"computadora doméstica"; the translation should then follow.
- **q-1147** (fast-food) Ein Mann mit weißem Anzug und Spitzbart prangt auf Eimern voller Brathähnchen. Welcher US-Bundesstaat steckt im Namen seiner Kette? → Kentucky: source: the fun fact says Sanders was not a military man ("Sanders no era militar" / "Sanders war kein Militär"), but he served briefly as a US Army private in 1906, in Cuba. Only the colonel rank was honorary. The source's fun fact needs correcting, e.g. "kein echter Oberst", and should then be carried into the German. It could also say who Sanders is, since he is named nowhere else.
- **q-1544** (fashion-history) Diese flache Wollmütze wird traditionell mit einem europäischen Volk verbunden. Mit welchem? → Basken: In German the pictured object is called "Baskenmütze", so its everyday name contains the answer. This also overlaps approved q-6565 ("Wie heißt diese Kopfbedeckung?" → Baskenmütze): seeing either one gives away the other. The question doesn't travel to German and should be dropped for this locale.
- **q-1952** (winter-olympics) Wann finden die Winter-Paralympics im Vergleich zu den Olympischen Winterspielen statt? → Kurz danach, am selben Austragungsort: source: hint 2 ("Nunca se celebran antes que los Juegos Olímpicos"), translated as "Sie finden nie vor den Olympischen Spielen statt", is historically false. The 1984 and 1988 Winter Paralympics in Innsbruck took place in January, before the Games in Sarajevo and Calgary. The source hint needs correcting (for example, "Seit Jahrzehnten kommen sie nicht mehr zuerst dran"), and the question text could use a modern time frame, since the same-host rule dates from 1992.
- **q-2257** (basketball) Dieser Spieler verbrachte seine gesamte 20-jährige NBA-Karriere bei den Los Angeles Lakers. Wer ist er? → Kobe Bryant: source: the fun fact calls Bryant's 81 points the second-highest total in NBA history, but Bam Adebayo scored 83 on 10 March 2026, so 81 is now third behind Wilt Chamberlain's 100 and Adebayo's 83. Correct the English source, for example by dropping the ranking ("Kobe Bryant once scored 81 points in a single game in 2006"), then carry the change into the translation.
- **q-2677** (reality-tv) Es passiert gegen Ende einer Folge, die Moderation verkündet es, und jemand muss die Show verlassen. Wie heißt das? → Rauswurf: Fact check: wrong. The description ('someone suddenly remembers the stove is still on at home') doesn't match the question text (elimination at the end of an episode). The 'Immunität' wrong answer is fine, but the question is vague: 'Rauswurf' is not the only valid term, since 'Eliminierung', 'Ausscheiden' and 'Abwahl' also fit. The hint 'abgewählt/nach Hause geschickt' nearly gives the answer away, and the 'three_facts' clue style is not followed. The fun fact is true for some shows, but it is generic and unsourced. I did no web search, so this rests on reasoning alone.
- **q-2905** (volcanoes) Dieses orange glühende Zeug fließt aus Vulkanen. Was ist es wirklich? → Geschmolzenes Gestein: Overlap, inherited from source: approved q-6063 says "dieses glühende, geschmolzene Gestein" comes out of a volcano as lava, which states this question's answer outright. Hint 2 here also names "Magma", the answer to q-6063. The German translation itself is fine. The developer should reword q-6063's text or drop one of the two questions.
- **q-3293** (earthquakes) Die Feuerwehr zeigt Kindern diesen roten Gegenstand. Wofür ist er da? → Kleine Brände löschen: source: hint 1 ("Firefighters carry much bigger ones on their trucks") is inaccurate. Fire engines rely on water tanks, pumps and hoses, and the extinguishers they carry are mostly ordinary portable ones, with only the occasional larger wheeled unit. The fact check is 'uncertain' on this point and I can't confirm it. The German mirrors the source faithfully, so the source hint needs correcting first, for example to say firefighters use hoses for big fires and this object is only for small ones. Fact check: uncertain. The answer and wrong answers are fine. I did not run any searches, so this rests on general knowledge. Hint 1 is shaky. Fire engines mostly carry water tanks, pumps and hoses. They do carry extinguishers, but mostly ordinary portable ones, plus the odd larger wheeled unit. So 'noch viel größere davon' is misleading. The fun fact is roughly true (hand-drawn, then horse-drawn fire engines) but has nothing to do with extinguishers.
- **q-3313** (environment) Du verlässt das Bad: Der Hahn tropft, das Licht ist an. Der tropfende Hahn verschwendet Wasser, das Licht verschwendet … → Strom: Fact check: uncertain. Answer 'Strom' is right; the wrong answers (Papier, Seife, Luft) and hints are fine. Only the fun fact is shaky. The EPA says a faucet dripping once a second can waste more than 3,000 gallons (about 11,000 L) a year, so '>10 000 Liter' matches that source. But this is from memory and I did not open any source this session. By my own arithmetic, a typical drop of about 0.05 mL gives only about 1,500–2,000 L a year. Drop-size assumptions differ, so the figure is disputed.
- **q-3395** (flags) Wer bemalt sich meistens das Gesicht mit der Flagge seines Landes, so wie auf diesem Foto? → Fans bei einem großen Sportspiel: Fact check: wrong. The description says 'ganz ohne ein einziges T-Shirt', which is odd and unclear. The question says 'meistens' (mostly), which is a stretch: most people who paint their faces are fans, but the word is vague. The answer 'Fans bei einem großen Sportspiel' is right and the wrong answers (cooks, pilots, doctors) are clearly wrong. Hint 1 'rufen gern ganz laut' is fine. The fun fact is vague but plausible: face and body painting for rituals and festivals is ancient. I did not run web searches, so this rests on general knowledge. The question itself is also hard to judge without the photo.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wozu war sein Hauptteil gedacht? → Zum Essen: source: Hint 2 is factually wrong in both the English source and the German. In the film Woody fishes the spork out of the kindergarten bin and puts it on Bonnie's table; Bonnie doesn't find it in the trash. The source needs a corrected hint 2 (e.g. "His main part came out of a kindergarten trash can"), then the German should follow.
- **q-4292** (fairy-tales) Was wird in „Die Schöne und das Biest“ aus dem Biest, sobald der Zauber gebrochen ist? → Ein Prinz: source: the fun fact is wrong. Leprince de Beaumont was French, but she lived in England and published her 1756 version in London (Magasin des enfants), so 'written in France' / 'in Frankreich' does not hold. Correct the source, e.g. 'written by the Frenchwoman Jeanne-Marie Leprince de Beaumont in 1756', then re-translate.
- **q-4395** (harry-potter) Du trittst wie Harry beim Trimagischen Turnier an. Welche dieser Aufgaben musst du NICHT bestehen? → Den Goldenen Schnatz in einem Spiel fangen: Fact check: uncertain. The answer and wrong answers are correct. The fun fact names the plant 'Dianthuskraut'. I recall the German edition calling Gillyweed 'Kiemenkraut' and 'Dianthuskraut' being Dittany, but I couldn't verify either term online.
- **q-4546** (prehistory) In Fantasyfilmen und -spielen erhitzt dieser Handwerker Eisen im Feuer, hämmert es auf dem Amboss und fertigt Schwerter und Hufeisen. Wie heißt er? → Schmied: Duplicates approved q-9199, which also describes hammering horseshoes on an anvil and asks for the trade, with the same answer, Schmied. Keep only one of the two in the German pool. This comes from the pool itself, so the source may carry the same overlap.
- **q-4940** (trains) Was ist das? → Zugfahrkarte: Fact check: wrong. The description is not unique. "A small piece of paper adults lose exactly when they need it" fits the wrong answer "Einkaufszettel" at least as well as a train ticket, since a shopping list is a small paper note that people famously lose or forget in the shop. A banknote could also fit. The hints and the fun fact are true: digital tickets and the Deutschlandticket on a phone exist, and the conductor checks tickets. But the riddle text points to no single answer.
- **q-5286** (amazon-history-and-exploration) In Werner Herzogs Film „Fitzcarraldo“ wurde ein riesiges Flussschiff wie dieses wirklich über einen Hügel gezogen. In welchem Land wurde das gedreht? → Peru: source: hint 1 is wrong and misleading in both languages. The film opens at the Manaus opera house in Brazil, and Manaus has a road link. The road-less rubber city is Iquitos, the protagonist's home, so the hint can steer players towards the wrong option, Brasilien. It should say something like "The film's hero lives in a rubber-boom city you can't reach by road". The German translation itself is faithful and natural.
- **q-5458** (famous-philosophers) Dieser bärtige deutsche Denker sagte, die Geschichte sei ein Kampf zwischen sozialen Klassen. Eine ganze Bewegung ist nach ihm benannt. Wer ist er? → Karl Marx: source: the fun fact is wrong in the English source, and the translation repeats it. The head on Marx's Highgate tomb is a bronze bust on a stone plinth, not a stone head. Correct the source (e.g. "huge bronze head"), then carry the change into the German ("riesiger Bronzekopf"). Fact check: wrong. Fun fact is inaccurate: the Highgate monument is a large bronze bust on a granite plinth, not a stone head. The rest checks out (Marx, 4 letters, London, Darwin/Tolstoy/Freud didn't say this).
- **q-5561** (james-bond) Sean Connery ist zu „James Bond – 007 jagt Dr. No“ wie Barry Nelson zu … → Casino Royale: source: the fun fact is wrong. In the 1954 TV "Casino Royale" the British ally was called Clarence Leiter, not Felix Leiter. The English source needs correcting (e.g. "and his ally Leiter, renamed Clarence, was British"); the German should then follow it. The translation itself is faithful.
- **q-6098** (world-war-ii) Die Achsenmacht Japan griff im Dezember 1941 einen US-Marinestützpunkt auf Hawaii an. Welche Folge hatte das? → Die USA traten in den Krieg ein: Duplicate of approved q-5553: both ask what followed the attack on Pearl Harbor in December 1941, and both answer that the USA entered the war. Seeing one gives the other away. The translation itself is faithful, so keep only one of the two in the German pool; source: the same overlap may exist in English.
- **q-6473** (languages-of-the-world) „In Leningrad, fern von jedem Dschungel, zeigte ich in den 1950ern, dass Maya-Glyphen auch für Laute stehen. Guatemala sah ich erst mit 68.“ Wer bin ich? → Juri Knorosow: source: the fact check is 'uncertain' on "Guatemala sah ich erst mit 68". Knorosow was born on 19 Nov 1922 and visited in 1990, so he was 67 or 68 depending on the month, which I can't confirm. Both the source and the translation should change to "erst 1990" or similar. The rest of the translation is faithful and natural. Fact check: uncertain. The answer and hints are right. The riddle says Knorozov first saw Guatemala at 68. He was born 19 Nov 1922 and went in 1990, so he was 67 or 68 depending on the month. I found no source for the month.
- **q-6644** (famous-quotes) Welches dieser Länder gehört NICHT zu der Staatengemeinschaft mit dem Motto „In Vielfalt geeint“? → Norwegen: source: the fun fact says Norwegians voted against joining the European Union in 1972, but the EU did not exist until 1993. The 1972 referendum was on joining the European Community (EC), and only the 1994 vote was on the EU. The translator flagged this and kept it. The source needs correcting first, e.g. "Norwegians voted against joining twice: the European Community in 1972 and the EU in 1994."

## Not travelling

None.

## Stale re-translated

None.
