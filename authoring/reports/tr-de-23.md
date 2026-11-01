# tr-de-23

Made by `qgen batch --translate de` on 2026-10-31 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 43 (0 stale re-translated)
- Translated: 43
- Approved: 28
- Needs work: 15
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 149, about $10.03 at list price; $0.23 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-23&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-21 | tr-de-22 | tr-de-23 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 43 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 43 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 277 | 274 | 28 |
| needs_work |  | 23 | 26 | 15 |
| needs_work rate | ≤ 20.0 % | 7.7 % ✓ | 8.7 % ✓ | 34.9 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.3 % ✓ | 4.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 5.3 % ✓ | 6.3 % ✓ | 25.6 % ✗ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 2.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.7 % ✗ | 2.0 % ✗ | 9.3 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 43 |
| audit/review agreement | ≥ 90.0 % | 93.3 % ✓ | 95.0 % ✓ | 74.4 % ✗ |
| cost $ |  | $39.43 | $39.67 | $6.39 |
| $ per approved |  | $0.14 | $0.14 | $0.23 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 28 (4 %)
- Major among review needs work: 5 of 15 (33 %)
- Problems by kind: giveaway 8 (0 major), fact 11 (1 major), ambiguity 1 (0 major), overlap 5 (4 major), media 1 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 43 (0 %)
- Audit/review agreement (both accept or both not): 32 of 43 (74 %)
- Sample: 43 audited of 43; 43 Claude calls, about $3.64

Major findings on approved questions:

- **q-2021**: media — Media: the question says „Du siehst die berühmtesten Zeichnungen von Nervenzellen der Geschichte“, but the picked file is a 2024 modern drawing of a myelinated neuron by Biology with Risa (Wikimedia Commons), not a Cajal drawing, so the TV shows the wrong subject and the role would need to be essential with a real Cajal drawing (source: same file). Translation is faithful and natural; answer, wrong options (Ochoa, Fleming, Pawlow are all medicine Nobel laureates who did not make these drawings), hints and the Golgi fun fact checked out, and difficulty is within range. (http://127.0.0.1:8001/review/q-2021)

## Needs work

- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Direct duplicate of the approved q-0369 („Aus welchem Land stammt der Zauberwürfel…?“, answer Ungarn): both ask the same fact with the same answer, so only one should stay in the German pool. The translation itself is faithful and has no other defects; rewording it can't fix this without making it a different question.
- **q-0954** (greek-heroes) Rate: „Eine Göttin strafte mich: Ich wiederhole nur die letzten Worte anderer. Ich liebte einen Jüngling, der nur sich selbst im Wasser ansah.“ Wer bin ich? → Echo: source: the fun fact has the etymology backwards. Greek ēchō was the common word for this sound, and the nymph is its personification, so the word doesn't come from her; the Narziss/Narzisst half is fine. Both versions also share a description problem: 'always has the last word, never the first' states Echo's defining trait and singles her out among the four options, so it should play on the theme without that trait.
- **q-1544** (fashion-history) Welches europäische Volk verbindet man traditionell mit dieser flachen Wollmütze? → Basken: The German word for this cap is „Baskenmütze“, so anyone who recognises the beret in the photo has the answer: the language gives it away, even though the text avoids the word. It also overlaps approved q-6565 („Wie heißt diese Kopfbedeckung?“ → „Baskenmütze“), where seeing one question solves the other. This cannot be fixed in German without changing the question; it should be treated as not travelling and left out of the German pool.
- **q-2307** (capital-cities) Hunde wie dieser sind die Stars eines Disney-Films, der in London spielt, mit 101 gefleckten Welpen. Welche Rasse ist das? → Dalmatiner: source: the English source says "101 spotted puppies", and the translation repeats it, but this is wrong. In Disney's "101 Dalmatiner" there are 99 puppies plus the parents Pongo and Perdita, 101 Dalmatians in total. The source needs correcting first, for example to "with 101 spotted dogs" or "a film about 101 spotted dogs", and the German should then follow it.
- **q-3581** (norse-mythology) Die Serie „Vikings“ begleitete ab 2013 sechs Staffeln lang den legendären Ragnar Lothbrok. In welchem Land wurde sie größtenteils gedreht? → Irland: source: the question says the series followed Ragnar Lothbrok for six seasons, but Ragnar dies in season 4 and his sons carry the rest. The source should say the series began with Ragnar, or drop 'six seasons'. The German translation is faithful and repeats this error.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wozu war sein Hauptteil gedacht? → Zum Essen: source: hint 2 is factually wrong, and the German text carries the error over faithfully. In Toy Story 4, Bonnie doesn't find the spork in the kindergarten trash can; Woody fishes it out and puts it on her table. The source hint should say something like "His main part came out of a trash can at kindergarten", and the translation should then follow.
- **q-4078** (world-war-ii) In einer Gefängniszelle nach einem gescheiterten Putsch in München begann Adolf Hitler, „Mein Kampf“ zu schreiben. In welchem Jahr? → 1924: source: the fun fact says Hitler dictated much of the book to Rudolf Hess. This is a popular claim that modern research disputes (Plöckinger: he largely typed it himself, and Hess helped at most with editing). The source's fun fact needs correcting, e.g. to say that Hess was imprisoned with him in Landsberg. The German translation itself is faithful and natural.
- **q-4546** (prehistory) In Fantasyfilmen und -spielen erhitzt jemand Eisen im Feuer, hämmert es auf dem Amboss und macht daraus Schwerter und Hufeisen. Wie heißt dieser Beruf? → Schmied: Duplicates approved q-9199: both ask for the profession that hammers glowing horseshoes on an anvil, with the same answer, Schmied. Rewording cannot fix this, so one of the two should be dropped.
- **q-4940** (trains) Was ist das? → Zugfahrkarte: Fact check: wrong. The description is too vague to identify a train ticket. Adults lose many small papers just when they need them, such as a Geldschein, Einkaufszettel or Postkarte. An Einkaufszettel fits the description at least as well, because people often lose or forget it when shopping. The question is ambiguous and has more than one defensible answer. The hints and fun fact are fine, but the hints only partly narrow it down.
- **q-5458** (famous-philosophers) Dieser bärtige deutsche Denker sagte, Geschichte sei ein Kampf zwischen sozialen Klassen, und eine ganze Bewegung trägt seinen Namen. Wer ist er? → Karl Marx: source: the fun fact is wrong. The head on Marx's Highgate tomb is a bronze bust by Laurence Bradshaw (1956) on a granite plinth, not stone. The source's fun fact needs correcting ("huge bronze head"), and the German should then read „riesiger Bronzekopf“ („…wo sein riesiger Bronzekopf noch immer Besucher aus aller Welt anzieht“). Fact check: wrong. Fun fact: the huge head on Marx's Highgate Cemetery tomb is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth, not a stone head.
- **q-5561** (james-bond) Sean Connery verhält sich zu „James Bond jagt Dr. No“ wie Barry Nelson zu … → Casino Royale: source: the fun fact says Bond's friend "Felix Leiter" was British, but in the 1954 Climax! episode the British character was named Clarence Leiter, not Felix. The translator and rater both flagged this, and the fact check itself notes the name. The source needs correcting (e.g. "...and his friend, renamed Clarence Leiter, was British"), then the German can follow it.
- **q-5622** (natures-records) Das Rote Riesenkänguru ist das größte aller Kängurus. Wie weit kommt es ungefähr mit einem einzigen Sprung? → Etwa 8 Meter: source: two hints are factually wrong, and the German translation copies them faithfully. Hint 1 says the hop is much farther than a person can jump, but the long jump world record is 8.95 m. Hint 2 says it is about as long as a bus, but a standard bus is about 12 m, not 8 m. The source should fix these, e.g. hint 1 'farther than most people can jump' and hint 2 a comparison that fits 8 m or a different hint. Also, the translation's 'Wie weit kommt es' drops the source's 'can'; once the source is fixed, it should read 'Wie weit kann es ... kommen', since 8 m is a top-end leap, not a typical hop. Fact check: wrong. The answer (about 8 m, up to ~9 m) is fine. The wrong answers and the fun fact are also fine. Two hints are off. Hint 1 says it is 'much farther than a human can jump', but the long jump world record is 8.95 m, so it is about the same. Hint 2 says it is about as long as a bus, but a standard bus is about 12 m, so 8 m is shorter.
- **q-5784** (norse-mythology) In „God of War“ verlässt der kahle Spartaner Kratos mit seinem Sohn Atreus Griechenland Richtung Norden. Was bedeutet sein Name auf Griechisch? → Stärke: source: the premise is false. In the God of War games Kratos leaves Greece alone, and Atreus is born later in the Norse lands to Faye, so he can't leave Greece "with his son Atreus". The English source needs correcting first, e.g. "Kratos, a bald Spartan, left Greece for the Norse lands, where he raises his son Atreus". In the same pass, the German "sein Name" should say "der Name Kratos", because "sein" could also refer to Atreus.
- **q-6098** (world-war-ii) Japan, eine der Achsenmächte, griff im Dezember 1941 einen US-Marinestützpunkt auf Hawaii an. Wozu führte das? → Die USA traten in den Krieg ein: Same fact as the approved q-5553: the Pearl Harbor attack leads to the USA entering the war, and seeing one gives the other away. This duplicate comes from the source pair, not the translation; rewording can't fix it, so one of the two should be dropped.
- **q-6367** (nobel-prizes) Emmanuelle Charpentier und Jennifer Doudna erhielten 2020 den Chemie-Nobelpreis für CRISPR. Wie viele Frauen hatten ihn vor ihnen gewonnen? → 5: source: the fun fact is inaccurate, and the translation repeats it. Dorothy Hodgkin (Chemistry 1964) and Barbara McClintock (Medicine 1983) each won a science Nobel alone, so 2020 wasn't the first time one went only to women. It was the first science Nobel shared by a team made up only of women. Suggested source wording: "It was the first time a science Nobel was shared by two women with no male co-laureate." The German should then follow, e.g. „Zum ersten Mal teilten sich damit zwei Frauen einen naturwissenschaftlichen Nobelpreis ohne männlichen Mitpreisträger.“

## Not travelling

None.

## Stale re-translated

None.
