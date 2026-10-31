# tr-de-17

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 282
- Needs work: 18
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 841, about $43.24 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-17&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-15 | tr-de-16 | tr-de-17 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 288 | 284 | 282 |
| needs_work |  | 12 | 16 | 18 |
| needs_work rate | ≤ 20.0 % | 4.0 % ✓ | 5.3 % ✓ | 6.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.0 % ✓ | 4.3 % ✓ | 5.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 95.0 % ✓ | 96.7 % ✓ |
| cost $ |  | $40.83 | $39.74 | $39.28 |
| $ per approved |  | $0.14 | $0.14 | $0.14 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 3 (0 major), fact 3 (0 major), overlap 2 (2 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.96

Major findings on approved questions:

None.

## Needs work

- **q-0077** (disney-films) Welche Gabe hat Luisa im Film „Encanto“? → Übermenschliche Kraft: source: the fun fact is wrong in both the source and the translation. Not every Madrigal has a magic door: Mirabel gets hers only at the end, and Abuela and the in-laws have none. The fix must start from the source, e.g. "Jedes Madrigal-Kind mit einer Gabe bekommt eine magische Tür, die dazu passt." Also worth changing: "Übermenschliche Kraft" is the only noun phrase among three infinitive phrases, so it stands out ("Übermenschlich stark sein" would match). Hint 3's "Brücken" is unconfirmed (she does move houses and a church), and the description's "jeder" ignores Mirabel, who has no gift.
- **q-0228** (deserts) Wie heißt die größte heiße Wüste der Welt? → Sahara: Duplicates approved q-0731, which asks the same fact (largest hot desert in the world → Sahara) as a riddle. q-0228 should be dropped from the German pool, or one of the two retired. The translation itself is fine.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicate of approved q-0369 ("Aus welchem Land stammt der Zauberwürfel…?", answer Ungarn): both ask the same fact with the same answer. Keep only one in the German pool. The translation itself is faithful and natural.
- **q-0343** (magic) Welche Enkelin von Abuela Alma blieb in „Encanto“ ohne Gabe, weil ihre magische Tür nie aufleuchtete? → Mirabel: source: the clue "her door never lit up" (Spanish "nunca se iluminó") misdescribes the film. As I recall it, young Mirabel's door appears and glows at her ceremony, then vanishes when she touches the knob, and at the end of the film she does get a glowing door. The German is faithful, so the source needs correcting first, e.g. "weil ihre magische Tür bei der Zeremonie verschwand" ("porque su puerta mágica desapareció").
- **q-0354** (museums) Sieh dir dieses berühmte Gemälde an: „Las Meninas“ hängt im Prado in Madrid. Wer hat es gemalt? → Diego Velázquez: source: the fun fact is inaccurate. Picasso's 1957 series has 58 works, but only about 45 are versions of Las Meninas; the rest are mostly pigeons and landscapes. The source's fun fact needs correcting (e.g. "more than 40 versions" or "about 45 versions"), then the German can follow. The translation itself is otherwise faithful and natural.
- **q-0548** (countries) Wie heißen diese riesigen Steinstatuen auf der Osterinsel? → Moai: source: hint 2 ("Fast alle sind riesige Köpfe", from "Casi todas son cabezas gigantes") is false, because moai are carved as full figures with torsos, and only the buried ones look like heads alone. It also contradicts the fun fact about bodies. The source needs correcting too, e.g. "Sie haben übergroße Köpfe mit langen Nasen und ernsten Augenbrauen."
- **q-0870** (video-game-characters) Aus welchem Land stammt Metal Gear, die 1987 gestartete Spielereihe um den Spion Solid Snake? → Japan: source: the fun fact calls the MSX a console ("consola MSX", translated as "Konsole MSX"), but the MSX was a home computer standard and the 1987 game ran on the MSX2. Correct the source, for example to "Heimcomputer MSX2" / "computadora MSX2", then carry the change into the translation.
- **q-1544** (fashion-history) Diese flache Wollmütze wird traditionell mit einem Volk Europas verbunden. Mit welchem? → Basken: In German this hat is called 'Baskenmütze', so the essential photo gives away the answer 'Basken' to anyone who can name it; only the Spanish source word 'boina' hides it. It also overlaps approved q-6565 ('Wie heißt diese Kopfbedeckung?' → 'Baskenmütze'): seeing that question gives this one away. This doesn't travel to German and should not be played here.
- **q-1952** (winter-olympics) Wann finden die Winter-Paralympics im Vergleich zu den Olympischen Winterspielen statt? → Kurz danach, am selben Austragungsort: source: hint 2 ("Nunca se celebran antes que los Juegos Olímpicos" / "Sie finden nie vor den Olympischen Spielen statt") is historically false. The Winter Paralympics of 1980 (Geilo), 1984 and 1988 (both Innsbruck) took place before that year's Winter Olympics. The translation is faithful, so the source needs correcting, for example to "Heute finden sie nicht mehr vor den Olympischen Spielen statt" or a hint about the current order.
- **q-2257** (basketball) Dieser Spieler verbrachte seine gesamte 20-jährige NBA-Karriere bei den Los Angeles Lakers. Wer ist das? → Kobe Bryant: source: the fun fact is outdated. Bam Adebayo scored 83 points in March 2026, so Kobe Bryant's 81 is now the third-highest NBA total, not the second-highest. The fact check missed this; the claim is also a changeable record. Correct the source's fun fact, e.g. to drop the ranking ("81 points in a single game in 2006"), then re-translate it.
- **q-2677** (reality-tv) Es passiert kurz vor Ende der Folge, die Moderation verkündet es, und jemand muss die Show verlassen. Wie nennt man das? → Rauswurf: Fact check: wrong. The question is vague and doesn't fit its own answer. "Rauswurf" is a loose term. The usual word for this in TV shows is "Eliminierung" or "Ausscheiden". The question could also fit "Elimination". The description ("Herd an") is unrelated to the content. Hint 3 quotes "abgewählt", but many shows have no vote, so it doesn't hold for all of them. The fun fact is only true for some shows (e.g. Wildcard or comeback twists), not "manche Shows" in general. Wrong answers are fine, but "Immunität" could count as related. The question is also tagged lens=history and three_facts, which doesn't match. Overall the item is ambiguous and not cleanly verifiable.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wofür war sein Hauptteil gedacht? → Zum Essen: source: hint 2 is false, and the translation reproduces it faithfully. In the film, Woody fishes the spork and craft supplies out of the kindergarten trash and puts them on Bonnie's table; Bonnie doesn't retrieve the spork herself. The source hint should become something like "Its main part came out of a kindergarten trash can", then the German can follow.
- **q-4395** (harry-potter) Du trittst wie Harry als Champion beim Trimagischen Turnier an. Welche Aufgabe musst du NICHT bestehen? → Den Goldenen Schnatz im Spiel fangen: Fact check: wrong. The fun fact calls the plant 'Dianthuskraut'. In the German edition of Goblet of Fire, Harry eats 'Kiemenkraut' (Gillyweed). A quiz and a LEGO set page I found both use 'Kiemenkraut'. 'Dianthuskraut' does not appear in my searches. I did not check the German book text directly.
- **q-4940** (trains) Was ist das? → Fahrkarte: Fact check: wrong. The description is ambiguous. "A small piece of paper adults lose exactly when they need it" fits the wrong answer "Einkaufszettel" at least as well, because shopping lists are often lost or forgotten. It also loosely fits "Geldschein". Only the hints point to Fahrkarte. The fun fact is true, since many tickets are now digital. I did not run a web search; this rests on reading the question.
- **q-5458** (famous-philosophers) Dieser bärtige deutsche Denker sagte, die Geschichte sei ein Kampf zwischen Klassen. Eine ganze Bewegung trägt seinen Namen. Wer ist er? → Karl Marx: source: the fun fact is wrong in the English source too, and the translation keeps the error. The head on Marx's Highgate tomb is bronze (Laurence Bradshaw, 1956) on a granite plinth, so neither "stone head" nor "Steinkopf" is correct. The translator's notes and the fact check both flag this. The source needs correcting first, e.g. "huge bronze head"; the German can then read "riesiger Bronzekopf". Fact check: wrong. The answer, wrong answers and hints are fine. The fun fact is wrong: the large head on Marx's tomb at Highgate Cemetery is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth, not a stone head. This is from memory; I ran no searches.
- **q-5561** (james-bond) Sean Connery verhält sich zu „James Bond jagt Dr. No“ wie Barry Nelson zu … → Casino Royale: source: the fun fact is wrong, and the translation carries the error over. In the 1954 TV version, the British ally was called Clarence Leiter, not Felix Leiter. The source needs correcting, for example: "…and his friend, renamed Clarence Leiter, was British." Fact check: wrong. Fun fact: in the 1954 TV version Felix Leiter was renamed Clarence Leiter, so calling him 'Felix Leiter' is inaccurate. Bond as the American 'Jimmy Bond' and Leiter as British is correct. The answer Casino Royale is right.
- **q-6549** (strange-creatures) Das Tiefseetier Bathynomus lebt am Meeresboden, hat 14 Beine und wird bis zu 50 cm lang. Es ist der größte Verwandte welcher kleinen Gartentiere? → Rollasseln: Fact check: uncertain. I did not run any searches, so this rests on my own knowledge. Bathynomus (giant isopod) is about 50 cm long, has 7 pairs of legs and lives on the deep sea floor. The Toba Aquarium isopod that went about five years without food is also accurate. The weak point is the answer. Bathynomus belongs to the Cirolanidae (suborder Cymothoida), not the Oniscidea (land isopods). Rollasseln (Armadillidiidae) are therefore only distant relatives. Popular sources usually call it a relative of woodlice (Asseln, e.g. Kellerassel) or pill bugs. Many woodlice cannot roll up, so the 'Kugel' hint fits only Rollasseln.
- **q-6644** (famous-quotes) Welches dieser Länder gehört NICHT zur Staatengemeinschaft mit dem Motto „In Vielfalt geeint“? → Norwegen: source: the fun fact says Norwegians voted against joining the European Union in 1972, but the EU only came into being in 1993. The 1972 referendum was about the European Communities (EEC), as the translator's notes also say. The German repeats the error faithfully, so the source needs correcting, e.g. "voted against joining the EU and its predecessor, in 1972 and 1994".

## Not travelling

None.

## Stale re-translated

None.
