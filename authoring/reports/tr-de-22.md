# tr-de-22

Made by `qgen batch --translate de` on 2026-10-31 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 274
- Needs work: 26
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 625, about $44.24 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-22&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-20 | tr-de-21 | tr-de-22 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 273 | 277 | 274 |
| needs_work |  | 27 | 23 | 26 |
| needs_work rate | ≤ 20.0 % | 9.0 % ✓ | 7.7 % ✓ | 8.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 6.7 % ✓ | 5.3 % ✓ | 6.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.3 % ✗ | 1.7 % ✗ | 2.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 91.7 % ✓ | 93.3 % ✓ | 95.0 % ✓ |
| cost $ |  | $39.98 | $39.43 | $39.67 |
| $ per approved |  | $0.15 | $0.14 | $0.14 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 4 (0 major), fact 7 (2 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.58

Major findings on approved questions:

None.

## Needs work

- **q-0228** (deserts) Wie heißt die größte heiße Wüste der Welt? → Sahara: Overlap: q-0731, already approved, asks the same fact with the same answer (the largest hot desert in the world, Sahara), so this is a duplicate in the German pool. Rewording can't fix that; one of the two should be dropped. The translation itself is otherwise faithful and natural.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicate of approved q-0369, which asks the same fact in nearly the same way: the Rubik's Cube's country of origin, answer Ungarn. One of the two should be dropped; the translation itself is otherwise fine.
- **q-0548** (countries) Wie heißen diese riesigen Steinstatuen auf der Osterinsel? → Moai: source: hint 2 ("Casi todas son cabezas gigantes…", translated faithfully as "Fast alle sind riesige Köpfe…") repeats a misconception. Moai are full figures with torsos, and the hint contradicts the question's own fun fact about bodies below the head. Correct the source, for example to "Sie haben riesige Köpfe mit langen Nasen und ernsten Augenbrauen", then carry the change into the translation.
- **q-0954** (greek-heroes) Rätsel: „Eine Göttin ließ mich nur noch die letzten Worte anderer wiederholen, und ich liebte einen Jüngling, der nur sich im Wasser ansah.“ Wer bin ich? → Echo: source: the fun fact has the etymology backwards, in the source and the faithful translation. Greek "ēchō" was already the common word for sound, and the nymph personifies it, so the word does not stem from her. The fun fact should instead say that her name is the Greek word for sound or that the myth explains the phenomenon; the Narziss/Narzisst half is fine.
- **q-1413** (architectural-styles) Dieser Teil sitzt ganz oben auf der Säule und verbindet sie mit dem, was sie trägt. Die Griechen schmückten ihn mit Spiralen oder Blättern. Wie heißt er? → Kapitell: Overlap with approved q-4127: its text says "erst die Basis, dann der lange Mittelteil, dann das Kapitell", so it names this answer as the top of the column. Its own answer, Schaft, and Basis are also distractors here, so seeing either question gives the other away. Resolve it by dropping one of the two or rewording q-4127 so it no longer names Kapitell; the same overlap may exist between the sources (source: please check).
- **q-1544** (fashion-history) Diese flache Wollmütze wird traditionell mit einem europäischen Volk verbunden. Mit welchem? → Basken: In German this overlaps q-6565 ("Wie heißt diese Kopfbedeckung?" → „Baskenmütze“): that answer contains this question's answer, so seeing one gives the other away. The everyday German word also solves q-1544 outright, which doesn't happen with Spanish „boina“. Best treated as not travelling to German; rewording can't remove the link.
- **q-1952** (winter-olympics) Wann finden die Paralympischen Winterspiele im Vergleich zu den Olympischen Winterspielen statt? → Kurz danach, am selben Ort: source: hint 2 ("Nunca se celebran antes que los Juegos Olímpicos") is false, and the German "Sie finden nie vor den Olympischen Spielen statt." carries the error over. The 1984 and 1988 Winter Paralympics in Innsbruck took place in January, before the Sarajevo and Calgary Olympics in February. The source hint needs correcting, for example to "Seit Jahrzehnten kommen sie nicht mehr vor den Olympischen Spielen." or a present-day wording, and then the translation should follow it.
- **q-2021** (famous-scientists) Du siehst die berühmtesten Zeichnungen von Nervenzellen der Geschichte, von Hand gemacht von einem Medizin-Nobelpreisträger. Wer war es? → Santiago Ramón y Cajal: source: the text says the players are seeing Cajal's famous hand drawings, but the media file is titled "Simple Myelinated Neuron of the PNS", which reads like a generic neuron image, not a Cajal drawing. No picture was available to confirm this. Check the file and swap it for a real Cajal drawing (e.g. his Purkinje cell drawing, without a signature or caption naming him). Keep the current file only if it really is one. The German text itself is fine.
- **q-2307** (capital-cities) Hunde wie dieser sind die Stars in einem Disney-Film, der in London spielt, mit 101 gefleckten Welpen. Welche Rasse ist das? → Dalmatiner: source: the question says the film has 101 spotted puppies, but '101 Dalmatians' has 99 puppies plus the adults Pongo and Perdita, making 101 dogs. The German text faithfully repeats this error, so the source needs correcting (e.g. '101 gefleckten Hunden'). When it is, also consider the description and the 'gefleckt' wording, which both state the trait that rules out the wrong options, though the essential photo shows the spots anyway.
- **q-2502** (french-revolution) Ich wurde im heutigen Belgien geboren, trug im revolutionären Paris Reitkleidung und forderte 1792 das Recht auf Waffen für Frauen. Wer bin ich? → Théroigne de Méricourt: source: hint 3 says "my chosen name" ("Mein gewählter Name"), but she did not choose it. The Paris press, mainly royalist, coined "Théroigne de Méricourt", as the fun fact itself says ("wurde erst in Paris erfunden"), so the hint is wrong and contradicts the fun fact. The source should say something like "My later name comes from my home village of Marcourt"; the German can then follow.
- **q-3136** (wonders-of-the-world) Die Christusstatue von Rio de Janeiro steht auf dem Berg Corcovado. Wie hoch ist der Berg ungefähr? → Etwa 700 m: Fact check: wrong. The text facts are right: Corcovado is about 710 m, the statue is 30 m tall with a 28 m arm span, and the Eiffel Tower is about 330 m. But the image query is 'Rio de Janeiro Sugarloaf Mountain'. That shows a different mountain (Zuckerhut), which misleads for a question about Corcovado.
- **q-3581** (norse-mythology) Die Serie „Vikings“ begleitete ab 2013 sechs Staffeln lang den legendären Ragnar Lothbrok. In welchem Land wurde sie größtenteils gedreht? → Irland: source: the question says the series followed Ragnar Lothbrok for six seasons, but Ragnar dies in season 4 and the later seasons follow his sons. The English source needs rewording (e.g. "The TV series 'Vikings', which began with the legendary Ragnar Lothbrok, ran for six seasons from 2013"). The German is otherwise a faithful, natural translation of the source.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wofür war sein Hauptteil gedacht? → Zum Essen: source: hint 2 is false, and the translation carries the error over. In the film Woody, not Bonnie, fishes the spork out of the kindergarten bin and puts it on her table. The source needs correcting first, e.g. "Woody holt seinen Hauptteil im Kindergarten aus dem Mülleimer."
- **q-3930** (science-fiction) In „Ich – Einfach unverbesserlich“ stiehlt Gru den Mond. Welches Gerät benutzt er dafür? → Schrumpfstrahler: source: hint 2 is wrong, and the translation carries the error over. In the film, Gru's own team steals the shrink ray from the lab in East Asia and Vector then snatches it from Gru, so Vector did not take it from the lab first. The fun fact's "slowly" is also doubtful: the effect wears off, and faster on large objects. The source needs correcting first, then the translation should follow it.
- **q-4078** (world-war-ii) Nach einem gescheiterten Putsch in München saß Adolf Hitler in Haft und begann, „Mein Kampf“ zu schreiben. In welchem Jahr? → 1924: source: the fun fact says Hitler dictated much of the book to Rudolf Hess. This is a disputed popular claim: recent research, including Plöckinger and the IfZ critical edition, indicates Hitler typed much of it himself, with Hess helping mainly as a reader and editor. The source fun fact should be corrected or replaced, for example with a safe fact such as Hitler's imprisonment in Landsberg, and the translation then updated.
- **q-4546** (prehistory) In Fantasyfilmen und -spielen erhitzt dieser Handwerker Eisen im Feuer, hämmert es auf dem Amboss und macht daraus Schwerter und Hufeisen. Wie heißt er? → Schmied: Duplicates approved q-9199: both describe hammering horseshoes on an anvil and have the answer "Schmied". The same fact is asked again in other words, so one question gives the other away; the translation itself is otherwise sound.
- **q-4940** (trains) Was ist das? → Zugfahrkarte: Fact check: wrong. The clue is too vague to identify one answer. "A small piece of paper adults lose exactly when they need it" fits the wrong answer "Einkaufszettel" at least as well as "Zugfahrkarte". A shopping list is the classic small paper that gets lost or forgotten in the shop. A Geldschein is also small, made of paper, and easy to lose. The hints and fun fact are true. The hints point to a train ticket, but the question text itself does not.
- **q-5458** (famous-philosophers) Dieser bärtige deutsche Denker sah die Geschichte als Kampf zwischen sozialen Klassen, und eine ganze Bewegung trägt seinen Namen. Wer ist er? → Karl Marx: source: the fun fact is wrong in the English source too. The huge head on Marx's Highgate tomb is bronze (Laurence Bradshaw, 1956, on a granite plinth), not stone. Correct the source to "huge bronze head"; the German should then read: „Marx liegt auf dem Londoner Highgate Cemetery begraben, wo sein riesiger Bronzekopf noch immer Besucher aus aller Welt anzieht.“ Fact check: wrong. The fun fact calls the Marx monument at Highgate Cemetery a 'Steinkopf' (stone head). The giant head is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth. The answer, wrong answers and hints are fine. Marx was German, lived in London from 1849, and 'Marx' has four letters. Darwin, Tolstoy and Freud are not German thinkers and have no 'class struggle' movement named after them. The description's claim of a worldwide fan club is a joke and not a fact.
- **q-5561** (james-bond) Sean Connery ist zu „James Bond jagt Dr. No“ wie Barry Nelson zu … → Casino Royale: source: the fun fact is wrong, and the translation copies it. In the 1954 'Climax!' version the British ally was called Clarence Leiter (played by Michael Pate), not Felix Leiter. The source should be corrected first, e.g. "...and the American Felix Leiter became the British agent Clarence Leiter"; the German text can then follow it. Fact check: wrong. The answer, wrong answers and hints are correct. Barry Nelson played Bond in CBS's 'Climax!' episode 'Casino Royale' (1954), and Daniel Craig's first Bond film (2006) has the same title. The fun fact is inaccurate. In the TV version Bond was the American 'Jimmy Bond', but Felix Leiter was renamed Clarence Leiter (played by Michael Pate), a British agent. He was not called Felix Leiter. This is from memory; I did not run a search.
- **q-5622** (natures-records) Das Rote Riesenkänguru ist das größte aller Kängurus. Wie weit kommt es ungefähr mit einem einzigen Sprung? → Etwa 8 Meter: source: hint 1 is false as stated, because the human long-jump record is 8.95 m, more than the 8 m answer. Hint 2 is also inaccurate, because a standard bus is about 12 m long, not 8 m. The German faithfully carries both errors, so the source hints need correcting (e.g. "farther than most people can jump" and a comparison that really is about 8 m), and the translation should then follow.
- **q-5784** (norse-mythology) In God of War ist Kratos ein glatzköpfiger Spartaner, der mit seinem Sohn Atreus von Griechenland in den Norden zieht. Was bedeutet sein Name auf Griechisch? → Stärke: source: the question text says Kratos goes from Greece to the north with his son Atreus, which is false. Kratos went north alone, and Atreus was born and raised there. The German faithfully repeats this error, as the translator and rater both noted, although the fact check says confirmed. The source needs correcting, e.g. 'a bald Spartan who left Greece for Norse lands, where he raises his son Atreus'; the translation should then follow it.
- **q-6098** (world-war-ii) Japan, eine der Achsenmächte, griff im Dezember 1941 einen US-Marinestützpunkt auf Hawaii an. Was war die Folge? → Die USA traten in den Krieg ein: Duplicate: q-5553 (approved) asks the same fact, that the Pearl Harbor attack led to the US entering the Second World War, with essentially the same answer. The overlap comes from the source question, so one of the two should be dropped; the translation itself is fine.
- **q-6105** (world-war-ii) In „Hacksaw Ridge – Die Entscheidung“ seilt Sanitäter Desmond Doss auf Okinawa Verwundete einzeln eine Klippe hinab. Wie viele rettete der echte Doss etwa? → Etwa 75: source: hint 1 ('over one long night and day', in German 'in einer langen Nacht und an einem langen Tag') can't be confirmed; accounts of the rescue give about 12 hours under fire, and the citation covers 29 April to 21 May 1945. The fact check's claim about hint 3 looks wrong, since the citation does say 'approximately 75 casualties'. Even so, 'knapp unter 100' is a poor fit for 75 and goes beyond the source's 'fewer than 100'. Replace hint 1's timing and reword hint 3, e.g. 'In der Urkunde zu seiner Medal of Honor steht eine Zahl unter 100.' Fact check: wrong. Hint 3 is false. Doss's Medal of Honor citation gives no number of men saved; it only says he saved many. The figure of 75 comes from a compromise: the army suggested 100, Doss said 50, and they settled on 75. The answer 'Etwa 75' is correct.
- **q-6367** (nobel-prizes) Emmanuelle Charpentier und Jennifer Doudna erhielten 2020 den Chemie-Nobelpreis für CRISPR. Wie viele Frauen hatten ihn vor ihnen gewonnen? → 5: source: the fun fact is false in both versions. Women had already won science Nobels alone (Marie Curie 1911, Dorothy Hodgkin 1964, Barbara McClintock 1983), so 2020 wasn't the first science Nobel to go only to women. It should say the first science Nobel shared only by women, e.g. in German: „Zum ersten Mal teilten sich ausschließlich Frauen einen naturwissenschaftlichen Nobelpreis.“ Correct the source first, then the translation.
- **q-6618** (cold-war) Im Dezember 1989 entmachtete eine US-Invasion Manuel Noriega in dem hier gezeigten Land. Welches Land ist das? → Panama: source: the fun fact is inaccurate, and the translation repeats it faithfully. US troops did blast rock music at the Vatican nunciature, but it was stopped days earlier after the Vatican complained, so it did not go on "until he gave up" (he surrendered on 3 January 1990). The source should say something like "blasted loud rock music outside the embassy to pressure him", then the translation should follow.
- **q-6644** (famous-quotes) Welches dieser Länder gehört NICHT zu der Staatenunion mit dem Motto „In Vielfalt geeint“? → Norwegen: source: the fun fact says Norwegians voted against joining the European Union in both 1972 and 1994, but the EU did not exist until 1993; the 1972 vote was on joining the European Communities. The source needs correcting, for example to "voted against joining the EU's predecessor in 1972 and the EU itself in 1994", and the German should follow. Everything else in the translation is fine.

## Not travelling

None.

## Stale re-translated

None.
