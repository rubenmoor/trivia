# tr-de-21

Made by `qgen batch --translate de` on 2026-10-31 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 277
- Needs work: 23
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 691, about $43.83 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-21&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-19 | tr-de-20 | tr-de-21 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 275 | 273 | 277 |
| needs_work |  | 24 | 27 | 23 |
| needs_work rate | ≤ 20.0 % | 8.0 % ✓ | 9.0 % ✓ | 7.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 5.7 % ✓ | 6.7 % ✓ | 5.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.0 % ✗ | 2.3 % ✗ | 1.7 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 91.7 % ✓ | 91.7 % ✓ | 93.3 % ✓ |
| cost $ |  | $39.41 | $39.98 | $39.43 |
| $ per approved |  | $0.14 | $0.15 | $0.14 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 1 of 5 (20 %)
- Problems by kind: giveaway 3 (0 major), fact 6 (0 major), overlap 1 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.40

Major findings on approved questions:

None.

## Needs work

- **q-0228** (deserts) Wie heißt die größte heiße Wüste der Welt? → Sahara: Duplicate, and it comes from the source: q-0731 (approved, same answer) asks the same fact, 'largest hot desert in the world → Sahara', only as a 'Wer bin ich?' riddle. One of the two should be dropped. The translation itself is otherwise fine.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicate: this asks the same fact as approved q-0369 ("Aus welchem Land stammt der Zauberwürfel…?", answer Ungarn), as the rater also noted. The translation itself is faithful, but only one of the two should be played; the overlap comes from the source pool, so it can't be fixed by rewording.
- **q-0548** (countries) Wie heißen diese riesigen Steinstatuen auf der Osterinsel? → Moai: source: hint 2 says almost all moai are giant heads ("Casi todas son cabezas gigantes"), but moai are full figures with torsos; they only look like heads where they are buried up to the shoulders. The hint also contradicts the fun fact. The translation copies this faithfully, so the source needs correcting, e.g. "Sie haben riesige Köpfe mit langen Nasen…".
- **q-0954** (greek-heroes) Rate mal: „Eine Göttin ließ mich nur die letzten Worte anderer wiederholen, und ich liebte einen Jüngling, der nur sich im Wasser ansah.“ Wer bin ich? → Echo: source: the fun fact reverses the etymology, and the translation carries this over. The Greek common noun ēchō ("sound") came first and the nymph personifies it, so the word "Echo" does not come from her. The source fun fact needs correcting, e.g. "Die Nymphe ist nach dem griechischen Wort für Schall benannt, und vom jungen Narziss stammt das Wort „Narzisst“."
- **q-1544** (fashion-history) Welches europäische Volk verbindet man traditionell mit dieser flachen Wollmütze? → Basken: In German this question collapses: the object's everyday name, "Baskenmütze", contains the answer, and q-6565 ("Wie heißt diese Kopfbedeckung?") has exactly that as its answer, so seeing q-6565 gives this one away. Rewording can't avoid this, so the question should not be played in German.
- **q-1952** (winter-olympics) Wann finden die Winter-Paralympics statt, verglichen mit den Olympischen Winterspielen? → Kurz danach, am selben Ort: source: Hint 2 ("Nunca se celebran antes que los Juegos Olímpicos" / "Sie finden nie vor den Olympischen Spielen statt") is historically false. The Winter Paralympics of 1980 (Geilo), 1984 and 1988 (both Innsbruck) took place before that year's Winter Olympics, and in different places. The translation faithfully copies the error, so the source needs correcting, for example hint 2 limited to the modern era ("Heute kommen sie immer nach den Olympischen Spielen") and the question given a "heute".
- **q-2257** (basketball) Dieser Spieler verbrachte seine gesamte 20-jährige NBA-Karriere bei den Los Angeles Lakers. Wer ist er? → Kobe Bryant: source: the fun fact is out of date. Bam Adebayo scored 83 points in March 2026, so Kobe Bryant's 81 is now the third-highest NBA total, not the second-highest. The fact check's 'confirmed' misses this, as the translator and rater both noted. The source needs correcting, for example by dropping the ranking and keeping only the 81 points in 2006; the German then follows.
- **q-2307** (capital-cities) Hunde wie dieser sind die Stars eines Disney-Films, der in London spielt, mit 101 gefleckten Welpen. Welche Rasse ist das? → Dalmatiner: source: "101 spotted puppies" is wrong, in the English source as well as the German. The film has 99 puppies, and the 101 Dalmatians include the two parents, Pongo and Perdita. The source needs correcting (e.g. "with 101 spotted dogs"), and the translation should then follow it with „mit 101 gefleckten Hunden“.
- **q-2502** (french-revolution) Ich wurde im heutigen Belgien geboren, trug im revolutionären Paris Reitkleidung und forderte 1792 Waffen für Frauen. Wer bin ich? → Théroigne de Méricourt: source: hint 3 says "My chosen name", and the German faithfully renders this as "selbst gewählter Name". The fun fact says the name was invented in Paris, and "de Méricourt" is generally credited to the royalist press, so the hint is doubtful and contradicts the fun fact. The source hint should be corrected (e.g. "The name I am known by comes from my home village of Marcourt"), then the translation updated.
- **q-2669** (poetry) Welcher Römer steckt hinter dem meistzitierten Beispiel für ein Asyndeton, also eine Aufzählung ohne „und“? → Julius Caesar: source: the fun fact says Caesar won the Battle of Zela in about five days, but the battle itself took only hours. Suetonius gives the fifth day after his arrival, and within four hours of sighting the enemy. The source's fun fact needs correcting, e.g. "defeated Pharnaces only five days after arriving"; the translation then follows it. The translator flagged the same issue.
- **q-3136** (wonders-of-the-world) Die berühmte Christusstatue steht auf dem Gipfel des Corcovado in Rio de Janeiro. Wie hoch ist der Berg ungefähr? → Etwa 700 m: Fact check: wrong. The facts are right (Corcovado is about 710 m, the statue is 30 m tall with a 28 m arm span). The image query 'Rio de Janeiro Sugarloaf Mountain' shows a different mountain (Pão de Açúcar, about 396 m), not Corcovado.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wofür war sein Hauptteil gedacht? → Zum Essen: source: hint 2 is false, and the translation carries the error over. In Toy Story 4, Woody, not Bonnie, takes the spork out of the trash and puts it on her table; Bonnie only builds Forky from it. Change it in the source (e.g. "Woody fished his main part out of a kindergarten trash can"), then update the German hint.
- **q-3870** (crime-fiction) Ich habe weder Kopf noch Beine, kann nicht sprechen und helfe Wednesday Addams, Rätsel zu lösen. Wie heiße ich? → Eiskaltes Händchen: The description gives the answer away. „alles fest im Griff, und zwar wortwörtlich“ points to a literal hand, and the only option containing a hand is „Eiskaltes Händchen“. The question text deliberately avoids saying „Hand“, so the joke undoes that. Rewrite the description to play on the school or supervision theme without any hand or grip wording (for example, a school supervisor nobody ever hears coming).
- **q-3930** (science-fiction) In „Ich – Einfach unverbesserlich“ stiehlt Gru den Mond. Welches Gerät benutzt er dafür? → Schrumpfstrahler: source: hint 2 is wrong in the English source and the German copies it. Vector did not steal the shrink ray from the secret lab: Gru and the Minions stole it there, then Vector took it from them. The fun fact's "slowly" is also wrong, because the film says larger objects revert faster and the Moon snaps back fairly quickly. Correct the source first. The translation itself is faithful.
- **q-4292** (fairy-tales) Was wird in „Die Schöne und das Biest“ wieder aus dem Biest, wenn der Zauber gebrochen ist? → Ein Prinz: source: the fun fact is wrong. Leprince de Beaumont wrote and published her 1756 version in London, where she was living, not in France. The translation faithfully repeats the error, so the source must be corrected first, e.g. "The best-known version of the story was published in 1756 by the French author Jeanne-Marie Leprince de Beaumont." Fact check: wrong. The answer (a prince) and the wrong answers are fine. The fun fact is inaccurate: Beaumont's 1756 version was written and published in London (in her Magasin des enfants), where she had lived since about 1745, not in France. Villeneuve's longer original dates from 1740 in France. I did not run searches; this comes from memory.
- **q-4546** (prehistory) In Fantasyfilmen und -spielen erhitzt dieser Handwerker Eisen im Feuer, hämmert es auf dem Amboss und fertigt Schwerter und Hufeisen. Wie heißt er? → Schmied: Duplicate of approved q-9199: both describe a craftsman hammering horseshoes on an anvil and have the answer "Schmied", so seeing one gives away the other. The rater's note says "No overlap" but then describes the same fact. Either q-4546 or q-9199 should be dropped. This cannot be fixed by rewording.
- **q-4940** (trains) Was ist das? → Fahrkarte: Fact check: wrong. The clue is ambiguous. "A small piece of paper adults lose exactly when they need it" fits the distractor "Einkaufszettel" at least as well as "Fahrkarte". Lost or forgotten shopping lists are the classic example, and a banknote is also a small paper item. Only the hints point to the ticket. The hints and the fun fact are true, but the main clue doesn't single out the answer. I didn't search the web for this; it rests on common knowledge.
- **q-5458** (famous-philosophers) Dieser bärtige deutsche Denker sah die Geschichte als Kampf zwischen sozialen Klassen, und eine ganze Bewegung ist nach ihm benannt. Wer ist er? → Karl Marx: source: the fun fact is wrong. The huge head on Marx's Highgate tomb is bronze, not stone, and the German 'Steinkopf' faithfully repeats this error. The source fun fact should say 'huge bronze head'; the translation can then follow. Fact check: wrong. The answer, wrong answers and hints are correct. Darwin was English, Tolstoy Russian and Freud Austrian, and Marx did spend his later life in London. The fun fact is slightly wrong: the huge head on Marx's tomb at Highgate Cemetery is a bronze bust (1956, by Laurence Bradshaw) on a granite plinth, not a 'Steinkopf'. This is from memory; I did not run any searches.
- **q-5561** (james-bond) Sean Connery gehört zu „James Bond jagt Dr. No“ wie Barry Nelson zu … → Casino Royale: source: the fun fact is wrong. In the 1954 "Climax!" version of Casino Royale, the British ally was called Clarence Leiter, not Felix Leiter. The source's fun fact needs correcting, e.g. "...und sein Verbündeter hieß Clarence Leiter und war Brite"; the translator and the rater both flagged this.
- **q-5622** (natures-records) Das Rote Riesenkänguru ist das größte Känguru überhaupt. Wie weit kommt es ungefähr mit einem einzigen Sprung? → Etwa 8 Meter: source: two hints are factually wrong in the English source, and the German copies them faithfully. Hint 1 says 8 m is much farther than a person can jump, but the human long-jump record is 8.95 m. Hint 2 says 8 m is about a bus length, but a standard bus is about 12 m, which also clashes with hint 3 (two cars, about 9 m). Correct the source first, e.g. hint 1 'more than the length of a room' and hint 2 'about as long as a minibus'. While retranslating, change the German to 'Wie weit kann es … springen', because 'kommt es' drops the source's 'can' and reads as a typical hop, not the maximum. Fact check: wrong. The answer (about 8 m) is fine, since red kangaroo leaps reach roughly 8–9 m. Hint 2 ('about as long as a bus') is inaccurate: a standard bus is about 12 m, so 8 m is not bus length. It also conflicts with hint 3 (two cars, about 9 m). Speed: red kangaroos reach about 56 km/h in short bursts, so 'more than 50 km/h' is acceptable but could be worded more carefully. I checked this from memory, not with a live search.
- **q-5934** (roman-empire) Ovid schrieb die „Metamorphosen“, die später Shakespeare inspirierten. Kaiser Augustus verbannte ihn in eine Stadt am Schwarzen Meer. In welchem heutigen Land liegt sie? → Rumänien: The German question text is 169 characters, over the translation limit of 160, and reads long aloud. Cutting the padding clause „die später Shakespeare inspirierten“ brings it well under the limit without losing the clue.
- **q-6098** (world-war-ii) Japan, eine der Achsenmächte, griff im Dezember 1941 einen US-Marinestützpunkt auf Hawaii an. Wozu führte das? → Die USA traten in den Krieg ein: source: this asks the same fact as the approved q-5553, with effectively the same answer: the Pearl Harbor attack led to the US entering the war. Seeing one gives away the other, so one of the two should be dropped. The German translation itself is faithful and natural.
- **q-6644** (famous-quotes) Welches dieser Länder gehört NICHT zu der Staatengemeinschaft mit dem Motto „In Vielfalt geeint“? → Norwegen: source: the fun fact says Norwegians voted twice against joining the European Union, in 1972 and 1994, but the EU did not exist in 1972. That referendum was about the European Communities (EC). The German text copies this error, as the translator's notes point out. The source fun fact should be corrected, for example: "Norwegians voted against joining twice: the European Community in 1972 and the European Union in 1994". The translation can then follow.

## Not travelling

None.

## Stale re-translated

None.
