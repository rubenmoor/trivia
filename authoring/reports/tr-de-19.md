# tr-de-19

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 275
- Needs work: 24
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 785, about $43.54 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-19&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-17 | tr-de-18 | tr-de-19 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 282 | 275 | 275 |
| needs_work |  | 18 | 25 | 24 |
| needs_work rate | ≤ 20.0 % | 6.0 % ✓ | 8.3 % ✓ | 8.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 5.0 % ✓ | 6.3 % ✓ | 5.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 2.0 % ✗ | 2.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 93.3 % ✓ | 91.7 % ✓ |
| cost $ |  | $39.28 | $40.38 | $39.41 |
| $ per approved |  | $0.14 | $0.15 | $0.14 |
| **health** | | ✓ pass | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 0 of 5 (0 %)
- Problems by kind: giveaway 4 (0 major), fact 3 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 55 of 60 (92 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.12

Major findings on approved questions:

None.

## Needs work

- **q-0077** (disney-films) Welche Gabe hat Luisa im Film „Encanto“? → Übermenschliche Kraft: source: the fun fact is wrong in the Spanish source and the German translation repeats it faithfully. Not every Madrigal has a magic door with a gift: Mirabel has no gift and no door of her own, which is the film's premise. Correct the source (e.g. "Fast jedes Mitglied…" / "Jedes Madrigal-Kind mit Gabe bekommt eine magische Tür"), then carry it into the translation.
- **q-0228** (deserts) Wie heißt die größte heiße Wüste der Welt? → Sahara: Duplicate: approved q-0731 asks the same fact (largest hot desert in the world, answer Sahara), only as a "Wer bin ich?" riddle. The translation itself is fine; one of the two should be dropped from the pool.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicate: approved q-0369 asks the same fact (country of origin of the Zauberwürfel, answer Ungarn). This also holds for the source, so one of the two should be dropped from the pool; rewording the translation can't resolve it.
- **q-0343** (magic) Welche Enkelin von Abuela Alma bekam in „Encanto“ keine Gabe, weil ihre magische Tür nie aufleuchtete? → Mirabel: source: the clue that her magic door "never lit up" looks wrong. As I recall the film, Mirabel touches the doorknob at her ceremony, the door glows and then vanishes, so she gets no gift. Both the rater and the fact check flagged this wording. The source should say the door disappeared, e.g. "porque su puerta mágica desapareció", and the German can then follow ("weil ihre magische Tür verschwand").
- **q-0548** (countries) Wie heißen diese riesigen Steinstatuen auf der Osterinsel? → Moai: source: hint 2 ("Casi todas son cabezas gigantes" / "Fast alle sind riesige Köpfe") is factually wrong. Moai are full figures with torsos and oversized heads, not just heads, and the hint contradicts the fun fact about bodies under the heads. The German is faithful, so the source needs correcting first, e.g. "Sie haben übergroße Köpfe mit langen Nasen und ernsten Augenbrauen."
- **q-0834** (mummies) Ich bin ein Steinamulett auf der Brust von Mumien. Mein Zauberspruch verbot ihrem Herzen, beim Totengericht gegen sie auszusagen. Welches Tier bin ich? → Käfer: Overlaps approved q-4654 (Egyptian charms in the shape of a small animal, answer Käfer). Both ask which animal an Egyptian amulet represents and have the same answer, so a player who has seen one can answer the other at once. The developer should drop one of the two. The overlap comes from the pool, not from the translation.
- **q-0870** (video-game-characters) Aus welchem Land stammt Metal Gear, die 1987 gestartete Spielereihe um den Spion Solid Snake? → Japan: source: the fun fact calls the MSX a console, but it was a home computer standard (Metal Gear ran on the MSX2). The German "Konsole MSX" repeats this error, so the source needs correcting, e.g. to "Heimcomputer MSX2" in the German; the rest of the translation is fine.
- **q-1147** (fast-food) Mein Gesicht mit weißem Anzug und Spitzbart prangt auf Eimern voller Brathähnchen. Welcher US-Bundesstaat steckt im Namen meiner Kette? → Kentucky: source: the fun fact is wrong in both the Spanish source and the German. Harland Sanders did serve in the US Army (enlisted around 1906, in Cuba), so "war gar kein Soldat" / "no era militar" is false; only the Colonel title was honorary. It should say he was never an actual colonel, e.g. „Sanders war nie Oberst in der Armee: „Colonel“ war ein Ehrentitel des Bundesstaats Kentucky.“ Also, the first-person riddle asks for a fact other than the speaker's identity (reason 6); it should become a direct question, e.g. „Ein Mann im weißen Anzug mit Spitzbart prangt auf Eimern voller Brathähnchen. Welcher US-Bundesstaat steckt im Namen seiner Kette?“
- **q-1544** (fashion-history) Diese flache Wollmütze wird traditionell mit einem europäischen Volk verbunden. Mit welchem? → Basken: Overlaps q-6565 ("Wie heißt diese Kopfbedeckung?" → "Baskenmütze"): in German that answer contains this one, so seeing either question gives the other away. It is a side effect of the German word, which does not occur in Spanish ("boina"), and anyone who can name the hat already says the answer here. Consider not playing q-1544 in German.
- **q-1952** (winter-olympics) Wann finden die Winter-Paralympics statt, verglichen mit den Olympischen Winterspielen? → Kurz danach am selben Ort: source: hint 2 ("Nunca se celebran antes que los Juegos Olímpicos" / "Sie finden nie vor den Olympischen Spielen statt") is false. The Winter Paralympics in Geilo 1980 and Innsbruck 1984 and 1988 took place before those years' Winter Olympics, and at different venues. The question also has no time frame, so the answer only holds for the modern Games (same host since 1992). The source needs correcting: rewrite hint 2 without "never" and add "heute" or similar to the question. The German translation is faithful and natural.
- **q-2257** (basketball) Dieser Spieler verbrachte seine gesamte 20-jährige NBA-Karriere bei den Los Angeles Lakers. Wer ist er? → Kobe Bryant: source: the fun fact looks outdated. As far as I recall, Bam Adebayo scored 83 points for Miami against Washington in March 2026, which would drop Kobe's 81 to third-highest, so "second-highest" would be false in both the English and the German. The fact check confirmed the old record, so please verify this; dropping the ranking and keeping only "81 points in one game in 2006" would make the fact stable in both languages.
- **q-2502** (french-revolution) Ich wurde im heutigen Belgien geboren, trug im revolutionären Paris Reitkleidung und forderte 1792 Waffen für Frauen. Wer bin ich? → Théroigne de Méricourt: source: hint 3 says 'chosen name' ("Mein gewählter Name"), but she did not choose 'de Méricourt': the name was largely coined by the royalist press, as the fun fact's 'invented in Paris' implies. The hint is inaccurate and contradicts the fun fact. The source should say something neutral like 'The name I am known by comes from my home village of Marcourt'; the translation then follows. The German is otherwise faithful and natural.
- **q-2677** (reality-tv) Es passiert gegen Ende einer Folge, die Moderation verkündet es, und jemand muss die Show verlassen. Wie heißt das? → Rauswurf: Fact check: uncertain. I did no web searches. The answer "Rauswurf" fits, and the wrong answers (Casting, Immunität, Feier) are clearly wrong. The fun fact is generally true, since shows like Survivor and Big Brother have brought back eliminated contestants. But the question is vague: "Eliminierung", "Ausscheiden" and "Nominierung" fit about as well. The description ("Herd noch an") doesn't match the question. Hint 3's "rausgewählt" is awkward, and the hints don't single out "Rauswurf".
- **q-3089** (the-lord-of-the-rings) Das Wort wird in Gondor benutzt, kommt in Boromirs Traum vor und bezieht sich auf die Körpergröße. Wer sind die „Halblinge“? → Hobbits: Fact check: wrong. The text is correct. Gondor uses 'Halfling' for hobbits, and the word appears in Boromir's dream verse ('Halfling'). Hobbits are described as 2–4 feet tall (about 60–120 cm), and the barefoot and second-breakfast hints fit. Dwarves, half-elves and goblins are not called Halflings. The problem is the media: the image query 'Mont Saint-Michel abbey' has nothing to do with hobbits or Middle-earth.
- **q-3464** (international-football) Welcher Verein hat Europas wichtigsten Klubpokal, den Europapokal der Landesmeister oder die Champions League, am häufigsten gewonnen? → Real Madrid: source: the media file is titled "Real Madrid celebration after winning the 2018 UEFA Champions League Final". It is shown sharp on an illustrative slot, so it very likely shows the answer (the team celebrating with this trophy). The file was inherited from the source and can't be changed in this run, so the source question's media needs replacing, e.g. with a trophy-only photo or a decorative stadium image. The German text itself is fine.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wofür war sein Hauptteil gemacht? → Zum Essen: source: hint 2 is factually wrong, and the translation repeats it. In the film, Bonnie doesn't find the spork in a kindergarten trash can: Woody fishes the materials out of the trash and puts them on her table. The source hint needs correcting, for example to "Woody fished his main part out of a kindergarten trash can for Bonnie", and the German should then follow.
- **q-4546** (prehistory) In Fantasy-Filmen und -Spielen erhitzt diese Person Eisen im Feuer, hämmert es auf dem Amboss und fertigt Schwerter und Hufeisen. Wie heißt der Beruf? → Schmied: Duplicates approved q-9199: both describe hammering (glowing) horseshoes on an anvil and ask for the job, answer "Schmied". Only one of the two should be played in German; the translation itself is otherwise faithful.
- **q-4940** (trains) Was ist das? → Fahrkarte: Fact check: wrong. The description is ambiguous. Adults also often lose or misplace a Einkaufszettel (shopping list) or a Geldschein, and both are small pieces of paper. The description doesn't single out Fahrkarte, so the wrong answers aren't clearly wrong. The hints and fun fact are fine: digital tickets on phones are common, e.g. the Deutschlandticket. The only thing that points to Fahrkarte is the hints.
- **q-5458** (famous-philosophers) Dieser bärtige deutsche Denker sah die Geschichte als Kampf zwischen Gesellschaftsklassen, und eine ganze Bewegung trägt seinen Namen. Wer ist er? → Karl Marx: source: the fun fact is wrong in the English source as well as the translation. Marx's Highgate monument is a large bronze bust on a stone plinth (Laurence Bradshaw, 1956), not a stone head. Correct the source to "huge bronze head", then carry that into the German as "Bronzekopf". Fact check: wrong. The answer (Karl Marx) and the wrong answers are fine. The hints hold up too: he lived in London from 1849, and "Marx" has four letters. The fun fact is wrong: the Highgate monument is a large bronze bust on a granite plinth (Laurence Bradshaw, 1956), not a stone head.
- **q-5561** (james-bond) Sean Connery verhält sich zu „James Bond jagt Dr. No“ wie Barry Nelson zu … → Casino Royale: source: the fun fact is wrong in both languages. In the 1954 TV version the British ally was called Clarence Leiter, not Felix Leiter (the rater and translator both flagged this). The source needs correcting, e.g. "his friend, renamed Clarence Leiter, was British", and the German should then follow.
- **q-6098** (world-war-ii) Japan, eine der Achsenmächte, griff im Dezember 1941 einen US-Marinestützpunkt auf Hawaii an. Was war die Folge? → Die USA traten in den Krieg ein: Duplicates approved q-5553: both ask what followed the Pearl Harbor attack, and both answer that the USA entered the war. Seeing one gives the other away, and rewording can't fix this; drop one of the two from the German pool. The translation itself is faithful and natural.
- **q-6473** (languages-of-the-world) „In Leningrad, fern vom Dschungel, zeigte ich in den 1950ern, dass Maya-Glyphen auch für Laute stehen. Guatemala sah ich erst mit 68.“ Wer bin ich? → Juri Knorosow: source: the fact check is uncertain on "Guatemala sah ich erst mit 68". The visit is dated 1990 in most sources and 1991 in some. With his birthday on 19 Nov 1922, he could have been 67, 68 or 69, and I can't confirm the age from my own knowledge. The English source has the same claim, so the fix belongs there: drop the age or use a safe wording such as "erst kurz vor meinem Tod" or "erst Jahrzehnte später". The rest of the translation is faithful and natural. Fact check: uncertain. The Guatemala visit is dated 1990 in most sources and 1991 in some. Knorozov was born 19 Nov 1922, so he was 67 or 68 in 1990 and 68 or 69 in 1991. No source gives the exact date, so 'mit 68' can't be confirmed. The rest checks out: Leningrad, the phonetic reading, Thompson as the opponent, and Yuri Gagarin's first name. I did not look up the Asya cat fact. It is a known anecdote.
- **q-6492** (nobel-prizes) Karl Landsteiner entdeckte 1901 die Blutgruppen A, B und O und erhielt 1930 den Nobelpreis. In welcher Stadt gelang ihm die Entdeckung? → Wien: source: Hint 1 is wrong in both languages. Landsteiner was born on 14 June 1868, after the 1867 Compromise had turned the Austrian Empire into Austria-Hungary, so „Kaisertum Österreich“ / "Austrian Empire" is the wrong state. The source hint should say he was born in 1868 in Austria-Hungary or near the later Austrian capital without naming it, for example "in Österreich-Ungarn", and the translation should then follow. Everything else in the translation is faithful and natural.
- **q-6644** (famous-quotes) Welches dieser Länder gehört NICHT zu der Staatengemeinschaft mit dem Motto „In Vielfalt geeint“? → Norwegen: source: the fun fact says Norwegians voted against joining the European Union in both 1972 and 1994, but the EU did not exist until 1993. The 1972 referendum concerned the European Communities (EEC), as the translator noted. Correct the source fun fact, e.g. "voted against joining twice: the EEC in 1972 and the EU in 1994", then carry the change into the German.

## Not travelling

- **q-6523** about_language, confirmed: Many frogs are “nocturnal”. What does that mean? → They are active at night (The question asks what the fancy word 'nocturnal' means, but the German word 'nachtaktiv' states its own meaning (nachts aktiv), so the answer is given away. 'Nokturn' is not a usable everyday alternative. Reversing it to ask for the word would change the question and stay trivial.)

## Stale re-translated

None.
