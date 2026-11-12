# batch-57

Made by `qgen batch` on 2026-11-11 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): athletes-and-other-sports, chancellors-and-presidents, federal-republic-and-reunification, gdr-everyday-life, empire-weimar-and-nazi-era, sights-and-landmarks, pop-and-rock, shows-and-presenters, mountains-and-landscapes, regional-dishes, gdr-history, national-symbols-and-state, films-and-actors, states-and-capitals, reformation-to-empire, rivers-lakes-and-coasts, childrens-books-and-comics, national-team, rap-and-electronic, cities-and-towns, brands-and-products, childrens-tv-and-audio-dramas, dialects-and-regional-words, art-architecture-and-museums, sayings-and-idioms, bundesliga-and-clubs, series-and-crime
- Merged: 232 (q-16859…q-17090)
- Approved: 213
- Needs work: 19
- Dropped by the pipeline: 67
- Reviewed by: claude-opus-5-5
- Claude calls: 527, about $75.43 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-55, batch-56; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-55 | batch-56 | batch-57 |
|---|---|---:|---:|---:|
| source locale |  | es | en | de |
| drafts |  | 312 | 309 | 299 |
| skipped slots |  | 210 | 141 | 187 |
| dropped |  | 104 | 70 | 67 |
| drop rate | ≤ 20.0 % | 33.3 % ✗ | 22.7 % ✗ | 22.4 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 1 |
| dropped: hard fail unambiguous |  | 2 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 23 | 20 | 14 |
| dropped: overlap |  | 78 | 49 | 51 |
| dropped: duplicate |  | 1 | 1 | 0 |
| dropped: fact-check wrong |  | 1 | 0 | 1 |
| merged |  | 208 | 239 | 232 |
| approved |  | 189 | 208 | 213 |
| needs_work |  | 19 | 31 | 19 |
| needs_work rate | ≤ 20.0 % | 9.1 % ✓ | 13.0 % ✓ | 8.2 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.9 % ✓ | 1.7 % ✓ | 3.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.4 % ✓ | 0.4 % ✓ | 0.9 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 3.8 % ✗ | 2.5 % ✗ | 2.2 % ✗ |
| needs_work: media | ≤ 10.0 % | 2.9 % ✓ | 8.4 % ✓ | 4.3 % ✓ |
| media: no pick in review 1 |  | 28 | 33 | 31 |
| media: recovered by research |  | 24 | 22 | 21 |
| media: no pick at record |  | 5 | 11 | 10 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.5 % ✓ | 0.4 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 27.9 % ✗ | 18.1 % ✓ | 18.7 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 55.7 % ✓ | 79.4 % ✓ | 65.0 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.56 ✗ | 1.63 ✗ |
| approved 11–15 |  | 46 | 38 | 70 |
| top move | ≤ 25.0 % | 16.8 % ✓ | 13.8 % ✓ | 17.2 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 86.5 % | 81.6 % | 83.6 % |
| values stimulus |  | 4 | 6 | 3 |
| top clue | ≤ 60.0 % | 37.0 % ✓ | 36.8 % ✓ | 40.9 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 21.6 % ✓ | 22.6 % ✓ | 22.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.3 % ✓ | 21.3 % ✓ | 18.5 % ✓ |
| values lens |  | 10 | 11 | 9 |
| media share | 15.0 %–50.0 % | 13.5 % ✗ | 18.4 % ✓ | 16.4 % ✓ |
| mean fun | ≥ 3.40 | 3.37 ✗ | 3.51 ✓ | 3.37 ✗ |
| cost $ |  | $67.44 | $64.59 | $71.62 |
| $ per approved | ≤ $0.35 | $0.36 ✗ | $0.31 ✓ | $0.34 ✓ |
| calls |  | 424 | 462 | 467 |
| calls per approved |  | 2.24 | 2.22 | 2.19 |
| wall time h |  | 1.96 | 1.91 | 2.21 |
| days |  | 4 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 1 of 5 (20 %)
- Problems by kind: giveaway 11 (1 major), fact 2 (1 major), overlap 4 (1 major), media 2 (1 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.9; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.81

Major findings on approved questions:

None.

## Needs work

- **q-16883** (brands-and-products) „Knorr Fix“ ist ein Pulver im Tütchen, das man mit Wasser und zum Beispiel Hackfleisch in die Pfanne gibt. Wofür ist es? → Für eine Soße: None of the candidates shows minced meat cooking in a pan: 1 is a whole beef tenderloin on a plate, 2 is a plated steak dinner and 3 is a 19th-century prison engraving. A new search isn't allowed, so the image needs a new query such as "minced meat frying pan" or "Hackfleisch Pfanne". No suitable picture found for this question.
- **q-16891** (bundesliga-and-clubs) Welcher Verein spielt von allen am längsten ohne Unterbrechung in der Bundesliga und ist nie abgestiegen? → FC Bayern München: Hint 2 ("Er kommt aus Süddeutschland") gives the answer away: Dortmund, Schalke and Köln are all in western Germany, so only Bayern is left. Hint 1 (a stadium facade that lights up in different colours) also points straight at the famous Allianz Arena. Replace hint 2 with a hint that doesn't rule out options by region (e.g. about the club's founding era or its record number of titles), and make hint 1 vaguer.
- **q-16892** (bundesliga-and-clubs) Wie viele Meter liegt dieser weiße Punkt von der Torlinie entfernt? → 11 Meter: The question asks the same fact as the approved base question q-4376, which is also played in German: the penalty spot is 11 metres from the goal line. None of the three image candidates shows a penalty spot (a village chief, baby birds, a pheasant engraving), and no new search is allowed. Separately, hint 2 ("as many players as a team has on the pitch") gives the answer away among these options. No suitable picture found for this question.
- **q-16901** (chancellors-and-presidents) Dieser Mann war Vizekanzler unter Angela Merkel. Wer ist auf dem Foto? → Olaf Scholz: Hint 3 is factually off: the Ampel coalition broke up in November 2024 when the FDP left. Scholz stayed chancellor until May 2025, but in a minority government with the Greens, not with the Ampel. Reword it, for example "Er wurde 2021 Bundeskanzler einer Ampel-Koalition."
- **q-16936** (federal-republic-and-reunification) Wie viele Bundesländer hat Deutschland? → 16: This duplicates approved q-13069 ("Aus wie vielen Bundesländern besteht Deutschland?", answer 16). It asks the same fact in almost the same words, so drop this question.
- **q-16953** (gdr-history) Auf diesem Foto von 1946 reicht Wilhelm Pieck (KPD) einem SPD-Mann die Hand: Die SED entsteht. Wer ist der SPD-Mann? → Otto Grotewohl: None of the candidates shows the famous Pieck–Grotewohl handshake that the question describes ("Auf diesem Foto … reicht … die Hand"), and no new search is allowed. The slot needs the April 1946 handshake photo (e.g. Bundesarchiv Bild 183-H26980 in a better crop, or another Commons copy of the handshake). Failing that, the question should drop "Auf diesem Foto" and use an illustrative or decorative image. No suitable picture found for this question.
- **q-16965** (national-team) Dieser Spieler trug in der Nationalmannschaft lange die Rückennummer 13, wie vor ihm Michael Ballack. Wer ist es? → Thomas Müller: The media slot is set up wrong. It is marked essential and asks for a clear photo of Thomas Müller, but showing his face in a "who is it?" question gives the answer away. No candidate fits the slot either: none shows Müller clearly, and another search isn't allowed. Make the slot illustrative (for example a plain Germany shirt with no number or name, like candidate 1 or 2) or decorative, and search again. No suitable picture found for this question.
- **q-16969** (national-team) Bei der Heim-EM 2024 pfiffen deutsche Fans Spaniens Marc Cucurella nach einem Handspiel im Viertelfinale aus. In welcher Stadt holte er danach den Titel? → Berlin: This question really asks where the Euro 2024 final was played. Related q-10943 (same subcategory, "Die Nationalmannschaft") says that outright: "das Finale steigt im Berliner Olympiastadion". So seeing that one gives this one away. Keep only one of the two, or rework q-10943 so it doesn't name the final's venue.
- **q-16970** (national-team) Gegen diesen Argentinier verlor Deutschland das WM-Finale 1986, vier Jahre später gewann es gegen ihn. Wer ist es? → Diego Maradona: The media slot is set to essential with a note asking for a photo of Maradona. That doesn't work: a photo of the answer would give it away, and the question doesn't need essential media anyway. All six candidates show the Stadio Olimpico in Rome, which doesn't match the essential note. Change the role to illustrative and use the Stadio Olimpico (venue of the 1990 final); candidate 1 would then be a good pick. No suitable picture found for this question.
- **q-16979** (reformation-to-empire) In vielen Dörfern schießen Vereinsmitglieder beim Sommerfest auf einen Holzvogel. Wie nennt man den, der das letzte Stück herunterholt? → Schützenkönig: None of the candidates shows a Vogelschießen or a wooden target bird. All six are real birds (pigeon, starlings) sitting on utility poles or posts, or a lake scene, so they miss the question's subject. No new search is allowed, so the slot needs a new image, e.g. "Vogelstange Schützenfest" or "Schützenfest Holzvogel". No suitable picture found for this question.
- **q-16994** (art-architecture-and-museums) Georg Baselitz, eigentlich Hans-Georg Kern, malt seit 1969 seine Motive kopfüber. Wozu? → Damit Farbe und Form mehr zählen als das Motiv: Hint 2 gives the answer away. It says the reason is "not technique, forgers or politics", which rules out all three wrong answers at once and leaves only the correct one. Replace it with a hint that points towards the viewer's perception without crossing off the other options.
- **q-17002** (chancellors-and-presidents) Mit wie viel Prozent der gültigen Stimmen wählte die SPD Martin Schulz im März 2017 zu ihrem Vorsitzenden? → 100 Prozent: None of the image candidates fits the question: 1–3 and 5 are Soviet CPSU congress postcards and stamps with Lenin, 6 is an old Soviet newspaper, and 4 is a crowd at a bus stop outside a Linke party congress. Another search isn't allowed. The slot needs a new search for a neutral SPD or generic party congress image, for example "SPD party convention hall" or "party congress ballot voting". No suitable picture found for this question.
- **q-17016** (empire-weimar-and-nazi-era) Dieses dreirädrige Gefährt von 1886 gilt als erstes Auto der Welt. Wie heißt es? → Benz Patent-Motorwagen: This overlaps too much with approved q-13014 (Bertha Benz drove her husband's Motorwagen from Mannheim to Pforzheim in 1888). Once someone has seen that question with its answer "Bertha Benz", "Benz" plus "Motorwagen" gives this answer away. Hint 3 here also repeats q-13014's fact word for word. Either drop this question or retire one of the two.
- **q-17039** (pop-and-rock) Bettina Wegner schrieb „Sind so kleine Hände“ und ging 1983 in den Westen. In welcher Stadt lebte und sang sie vorher? → Ost-Berlin: Hint 2 ("the seat of the DDR government") names East Berlin outright, so it gives the answer away at hint 2. It should be a vaguer clue, for example one about the city's size or its cultural scene. Also, "Ost-Berlin" stands out among the plain city names. Using "Berlin" as the answer, or giving every option the same form, would fix that.
- **q-17045** (rivers-lakes-and-coasts) Woher kommen solche Striche mit Jahreszahlen an alten Hauswänden am Fluss? → Von großen Hochwassern: None of the candidates clearly shows flood marks with years on a house wall, and this essential image is what "solche Striche" points to. No new search is allowed in this run. The slot needs a clear photo of flood marks, such as the Passau Rathaus or Hann. Münden marks, ideally without the word „Hochwasser“ in it. No suitable picture found for this question.
- **q-17054** (sights-and-landmarks) In Regensburgs Altstadt stehen hohe Wohntürme, die reiche Familien im Mittelalter bauten. Wozu vor allem? → Um Reichtum und Macht zu zeigen: No candidate shows Regensburg or its patrician towers: the sheet has an Italian hilltop castle, a Latin stone inscription, a Rembrandt etching, a Dutch castle painting, a Frankfurt double portrait and a handwritten letter. A new search is needed, e.g. "Goldener Turm Regensburg" or "Regensburg old town towers". No suitable picture found for this question.
- **q-17058** (rivers-lakes-and-coasts) Aus welcher Zeit stammt das Gestein der weißen Kreidefelsen auf Rügen? → Zeit der Dinosaurier: Hint 2 is factually wrong. It says Rügen chalk is made of shells of tiny sea animals, but it is mostly coccoliths, the calcite plates of single-celled marine algae (coccolithophores). Hint 2 should be replaced, for example with „Das Gestein besteht vor allem aus winzigen Kalkplättchen von Meeresalgen (Plankton).“ Fact check: wrong. Hint 2 says the chalk consists of shells of tiny sea animals. Rügen chalk is mostly coccoliths, the calcite plates of single-celled marine algae (coccolithophores), not animals. The answer (Cretaceous, dinosaur era) is correct.
- **q-17073** (series-and-crime) In welchem Jahr hatte Hauptkommissar Frank Thiel seinen ersten Fall im Münster-Tatort? → 2002: Hint 2 („in den ersten Jahren nach der Jahrtausendwende“) leaves only 2002 among the options (1992, 2012, 2018), so it gives the answer away before hint 3. Hint 2 should only narrow things down, for example by ruling out 1992 and one other year, or the wrong answers should be changed so hint 2 still leaves at least two options (e.g. 2004, 2006).
- **q-17090** (states-and-capitals) Schau genau hin: Welches Gebäck ist hier ganz nah zu sehen? → Brezel: The description („sich ordentlich verknotet hat“) states the Brezel's defining knot shape and rules out Croissant, Brötchen and Berliner before any hint, so it gives the answer away. The question also overlaps q-9475, which already shows a pretzel photo and calls it „Brezn“. No candidate is the close-up of a salted Laugenbrezel the note asks for, and a new search isn't allowed. No suitable picture found for this question.

## Question axes

- move: analogy 10, cause_effect 9, count 13, estimate 7, identify 40, made_of 10, name_concept 21, odd_one_out 12, origin 17, purpose 22, record 7, sequence 11, when 18, who 21, word_meaning 14
- stimulus: detail 6, none 194, photo 32
- clue: completion 5, direct 95, riddle 23, scenario 32, three_facts 77
- answer_kind: group 37, number 22, person 28, place 30, thing 52, time 21, word 42
- lens: body_senses 12, educational_media 31, everyday 38, history 43, language 27, nature 6, pop_culture 39, school 28, university 8

## Dropped by the pipeline

- brands-and-products-5: overlap like q-6257: You're snacking on Lay's chips. Which of these foods is NOT made from the same vegetable? → Popcorn: Kölln macht Haferflocken. Welches dieser Lebensmittel wird NICHT aus Hafer gemacht? → Popcorn
- brands-and-products-15: overlap like q-15034: Ich hatte 1932 die Idee zu einer Schokolade, die in jede Sakkotasche passt, ohne zu brechen. Wer bin ich? → Clara Ritter: „Quadratisch. Praktisch. Gut.“ – mit diesem Spruch wirbt eine Firma aus Waldenbuch. Was verkauft sie? → Schokolade
- chancellors-and-presidents-0: overlap like q-13060: In welchem Jahr wurde mit Angela Merkel zum ersten Mal eine Frau deutsche Bundeskanzlerin? → 2005: Sie wurde oft „Mutti“ genannt und war die erste Frau, die Deutschland als Bundeskanzlerin regierte. Wer ist sie? → Angela Merkel
- chancellors-and-presidents-1: overlap like q-10945: Du siehst eine Wiederholung: Deutschland schlägt im WM-Halbfinale Gastgeber Brasilien mit 7:1. In welchem Jahr war das? → 2014: Diese Mannschaft gewann 2014 das höchste WM-Halbfinale aller Zeiten, 7:1 gegen Brasilien, und feierte den Titel mit Kanzlerin Merkel. Welche? → Deutschland
- chancellors-and-presidents-6: overlap like q-10928: Auf die Große Koalition unter Angela Merkel folgte 2021 ein Bündnis aus SPD, Grünen und FDP. Wie wurde es genannt? → Ampelkoalition: In der Ampel-Koalition stand Rot für die SPD und Grün für die Grünen. Für welche Partei stand das Gelb? → FDP
- chancellors-and-presidents-11: overlap like q-4247: I grew up in East Germany, worked as a physicist in East Berlin, and later led a reunited Germany for 16 years. Who am I? → Angela Merkel: Ich stand 2013 neben Barack Obama in Berlin und sagte: „Das Internet ist für uns alle Neuland.“ Im Netz wurde viel gelacht. Wer bin ich? → Angela Merkel
- childrens-books-and-comics-3: overlap like q-0073: ¿Cuál es el ratón de dibujos animados más famoso del mundo? → Mickey Mouse: Ich habe große runde Ohren und trage eine rote Hose. Mein Hund heißt Pluto, und in Deutschland gibt es seit 1951 ein Heft mit meinem Namen. Wer bin ich? → Micky Maus
- childrens-books-and-comics-10: overlap like q-12015: Im Abzählreim „Eins, zwei, Polizei“ kommt bei „fünf, sechs“ jemand dazu. Wer? → Die alte Hex': Im Abzählreim „Eins, zwei, Polizei, drei, vier, Offizier …“: Nach welcher Zahl kommt „gute Nacht“? → 8
- childrens-books-and-comics-14: overlap like q-12052: Sie heißen Sabrina und Amadeus, wohnen auf dem Martinshof und tragen Bibi und Tina über Wiesen und Felder. Was für Tiere sind das? → Pferde: Tinas Pferd heißt Amadeus, Bibis Pferd Sabrina, und Tinas Familie hat einen Reiterhof. Zu welchem Hof fliegt Bibi deshalb so oft? → Martinshof
- childrens-tv-and-audio-dramas-16: overlap like q-12134: Ich bin eine Fernsehsendung mit vielen Puppen, in Deutschland seit 1973. In meinem Lied heißt es: „Wer nicht fragt, bleibt dumm!“ Wer bin ich? → Sesamstraße: Ernie badet mit seinem Quietscheentchen, Bert liebt Tauben und Büroklammern. In welcher Straße wohnen die beiden? → Sesamstraße
- cities-and-towns-3: overlap like q-11044: Die Wupper fließt durch Wuppertal, direkt unter der Schwebebahn hindurch. Was bedeutet die Redensart „über die Wupper gehen“? → Kaputtgehen oder pleitegehen: Die Stadt entstand 1929 aus Elberfeld, Barmen und anderen Orten. Ihr neuer Name lautete Wuppertal. Was ist die Wupper? → Ein Fluss
- cities-and-towns-4: overlap like q-11039: Sie ist Deutschlands größtes Raubtier, bekommt ihre weißen Babys im Winter und liegt gern auf der Helgoländer Düne. Welches Tier ist gemeint? → Kegelrobbe: Auf der Helgoländer Düne bekommen jeden Winter diese Tiere ihre Babys am Strand. Welche Tiere sind es? → Kegelrobben
- cities-and-towns-7: overlap like q-9414: Im Märchen besiegt ein Igel den Hasen beim Wettlauf. Wer hat das Märchen in eine berühmte Sammlung aufgenommen? → Brüder Grimm: Ich wohne bei Buxtehude auf dem Acker. Meine Beine sind kurz, doch mit meiner Frau habe ich den Hasen beim Wettrennen ausgetrickst. Wer bin ich? → Der Igel
- cities-and-towns-11: overlap like q-12226: Bis zu welcher Uhrzeit isst man Weißwürste traditionell? → Bis 12 Uhr mittags: Ich bin hell, schwimme in heißem Wasser, und in München isst man mich mit süßem Senf und Brezn, am besten vor zwölf Uhr mittags. Was bin ich? → Weißwurst
- cities-and-towns-15: overlap like q-13123: Walter Oehmichen eröffnete in Augsburg ein Marionettentheater, das später mit „Jim Knopf“ im Fernsehen berühmt wurde. In welchem Jahr? → 1948: Der Kasper verhält sich zur Handpuppe wie Jim Knopf aus der Augsburger Puppenkiste zur …? → Marionette
- cities-and-towns-17: overlap like q-14035: Du stehst in Berlin auf dem Alexanderplatz. Was ragt dort mit einer silbernen Kugel 368 Meter hoch in den Himmel? → Fernsehturm: Du stehst auf dem Alexanderplatz und schaust am Berliner Fernsehturm hoch. Wie hoch ist er ungefähr? → 368 Meter
- dialects-and-regional-words-15: overlap like q-9337: Am Imbisswagen bestellst du „Pommes rot-weiß“. Was kommt auf die Pommes? → Ketchup und Mayonnaise: Im Ruhrpott bestellt man an der Bude „Fritten“. Sie sind aus Kartoffeln, lang und dünn und kommen gern rot-weiß. Was ist das? → Pommes
- dialects-and-regional-words-17: overlap like q-12998: Plattdeutsch sagt „Water“, „Appel“ und „maken“, Hochdeutsch „Wasser“, „Apfel“ und „machen“. Woher kommt dieser Unterschied? → Zweite Lautverschiebung: Die Benrather Linie bei Düsseldorf trennt zwei Formen eines Wortes. Welches Paar ist es? → maken / machen
- empire-weimar-and-nazi-era-4: overlap like q-12062: Der „Knopf im Ohr“ ist das Markenzeichen der Kuscheltiere welcher Unternehmerin? → Margarete Steiff: Diese Frau saß im Rollstuhl und nähte 1880 einen kleinen Filzelefanten als Nadelkissen – der Anfang einer Firma. Wer ist sie? → Margarete Steiff
- empire-weimar-and-nazi-era-8: overlap like q-1266: Mira este detalle de un castillo alemán de cuento. ¿Qué rey, apodado 'el Rey Cisne', lo mandó construir? → Luis II de Baviera: Der „Märchenkönig“ Ludwig II. ließ es bei Füssen bauen, Disney nahm es sich zum Vorbild. Welches Schloss ist gemeint? → Neuschwanstein
- empire-weimar-and-nazi-era-17: overlap like q-14960: Du stemmst nach dem Finale in Berlin den DFB-Pokal in die Höhe. Wie schwer ist er ungefähr? → Etwa 6 Kilogramm: Seit 1985 wird in diesem Berliner Stadion jedes Jahr ein Finale gespielt. Welcher Wettbewerb ist das? → DFB-Pokal
- federal-republic-and-reunification-5: overlap like q-13072: Für jeden WM-Titel trägt Deutschland einen Stern, den vierten gab es 2014 in Brasilien. In welchem Land wurde der allererste gewonnen? → Schweiz: Mario Götze schoss 2014 das Siegtor im WM-Finale. In welchem Land, hier als Umriss gezeigt, fand diese WM statt? → Brasilien
- federal-republic-and-reunification-13: overlap like q-9170: Im Herbst 1989 zogen von dieser Kirche aus jeden Montag Tausende los und riefen „Wir sind das Volk“. In welcher Stadt steht sie? → Leipzig: Leipzig 1989: Nach dem Friedensgebet in der Nikolaikirche riefen Tausende „Wir sind das Volk“. Wie hießen diese Demos? → Montagsdemonstrationen
- films-and-actors-10: overlap like q-2580: It's a baby deer, it often has white spots on its back, and Bambi is one. What is it called? → Fawn: Den Medienpreis Bambi gibt es seit 1948. Er ist eine kleine goldene Figur. Welches Tier zeigt sie? → Reh
- gdr-everyday-life-2: overlap like q-12066: „Ich hatte zehn Klassen, fast alle Kinder der DDR gingen zu mir, und ab Klasse 7 schickte ich sie regelmäßig in echte Betriebe.“ Wer bin ich? → Die Polytechnische Oberschule: Ab der 7. Klasse kam ich jede Woche: Dann ging es nicht ins Klassenzimmer, sondern in einen Betrieb an Werkbank oder Maschine. Wie heiße ich? → Unterrichtstag in der Produktion
- gdr-everyday-life-7: overlap like q-6197: Opened in East Berlin in 1976, it housed the parliament and a bowling alley. People nicknamed it “Erich's lamp shop” after Erich Honecker. What was it? → The Palace of the Republic: In seinem Foyer hingen Hunderte Kugellampen, und Erich Honecker eröffnete es 1976. Welches Gebäude hieß deshalb „Erichs Lampenladen“? → Palast der Republik
- national-symbols-and-state-13: overlap like q-13047: Diese Blätter sind auf den deutschen 1-, 2- und 5-Cent-Münzen zu sehen. Von welchem Baum stammen sie? → Eiche: Ich bin ein Baum. Meine Früchte tragen kleine Hütchen, Wildschweine fressen sie gern, und meine Zweige sind auf kleinen Cent-Münzen. Welcher Baum bin ich? → Eiche
- national-team-3: overlap like q-8413: Estás viendo la Copa América 2024 con la camiseta amarilla puesta. ¿Cuál de estos jugadores NO era de la Selección Colombia? → Lionel Messi: Diese vier Stars standen im WM-Finale 2014 auf dem Platz. Wer spielte NICHT für Deutschland? → Lionel Messi
- national-team-10: overlap like federal-republic-and-reunification-5: Mario Götze schoss 2014 das Siegtor im WM-Finale. In welchem Land, hier als Umriss gezeigt, fand diese WM statt? → Brasilien: Über diesen Spieler rief der TV-Reporter im WM-Finale 2014: „Mach ihn! … Er macht ihn!“ Wer ist es? → Mario Götze
- national-team-14: overlap like q-2486: Germany won the 2014 World Cup final at the famous Maracanã stadium. In which city is it? → Rio de Janeiro: In diesem Stadion wurde Deutschland 2014 Weltmeister. In welcher Stadt steht es? → Rio de Janeiro
- pop-and-rock-11: overlap like q-10957: Tamara Danz war in den 1980ern die bekannteste Rocksängerin der DDR. Bei welcher Band sang sie? → Silly: Wer spielte NICHT in der Ostberliner Punkband Feeling B? → Tamara Danz
- rap-and-electronic-6: overlap like q-14095: Wir starteten 1994 mit „Hyper Hyper“ und ließen später Tausende „Maria (I Like It Loud)“ brüllen. Wer sind wir? → Scooter: Scooter landeten 2003 den Hit „Maria (I Like It …)“. Wie mag es die Band laut Songtitel, auf Deutsch übersetzt? → Laut
- rap-and-electronic-9: overlap like q-11087: Schon im DDR-Fernsehen stand ich vor der Kamera, seit 1999 lese ich die „Tagesschau“. 2021 machte mich das Jugendwort „cringe“ zum Internethit. Wer bin ich? → Susanne Daubner: Ich komme aus dem Englischen. Man sagt mich, wenn man sich fremdschämt, etwa wenn ein Lehrer cool reden will. 2021 war ich Jugendwort des Jahres. Welches Wort bin ich? → Cringe
- rap-and-electronic-13: overlap like q-16794: Listen: a hip-hop DJ makes this sound with a vinyl record. What is the trick called? → Scratching: Die DJ-Technik entstand in den 1970ern in New York: Die Hand schiebt die Schallplatte vor und zurück, es quietscht schrill. Was heißt „Scratching“ auf Deutsch? → Kratzen
- reformation-to-empire-0: overlap like q-12186: Ich wurde in England gebaut und dampfte am 7. Dezember 1835 von Nürnberg nach Fürth, als erste Lok Deutschlands. Wie heiße ich? → Adler: Ich fresse Kohle, trinke Wasser und zische laut. 1835 zog ich den ersten deutschen Zug von Nürnberg nach Fürth. Was bin ich? → Dampfmaschine
- reformation-to-empire-17: overlap like q-11024: Erstklässler bekommen eine riesige Tüte, die Zweitklässler führen ein Stück auf, und alle Eltern filmen. Welche Feier ist das? → Einschulungsfeier: Wer bekommt in Deutschland so eine bunte, gefüllte Tüte geschenkt? → Schulanfänger
- regional-dishes-4: overlap like q-16917: Hier plaudert man nicht, man „schnackt“. Dazu gibt es Fischbrötchen, Deiche und Wind vom Meer. Wo bist du? → In Norddeutschland: An Hafenbuden gibt es sie mit Hering oder Matjes und Zwiebeln, und Möwen klauen sie gern. Wo isst man Fischbrötchen am häufigsten? → An der Küste
- regional-dishes-5: overlap like q-12983: Diese dünnen Würstchen erwärmt man in heißem Wasser. Sie heißen nach der Stadt mit Deutschlands höchsten Wolkenkratzern. Welcher? → Frankfurt: In Österreich heißen diese dünnen Brühwürstchen „Frankfurter“. In Deutschland heißen sie „… Würstchen“. Wie lautet das fehlende Wort? → Wiener
- brands-and-products-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Der Mercedes Citaro ist rund zwölf Meter lang, hat mehrere breite Türen und fährt in vielen deutschen Städten. Was ist er? → Linienbus
- bundesliga-and-clubs-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Wie viele Länderspiele bestritt Bastian Schweinsteiger für Deutschland? → 121
- chancellors-and-presidents-5: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Angela Merkel nannte diese Suppe in Interviews als Lieblingsgericht, das sie selbst kocht. Welche Suppe ist auf dem Foto? → Kartoffelsuppe
- childrens-books-and-comics-0: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Welche Kinderbuchreihe von Ravensburger hat Klappen zum Aufklappen, unter denen sich Antworten verstecken? → Wieso? Weshalb? Warum?
- childrens-books-and-comics-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Ihr Platz heißt „Teufelstopf“, ihr Trainer Willi, ihr Motto „Alles ist gut, solange du wild bist!“. Mit welchem Ball spielen die Wilden Kerle? → Fußball
- cities-and-towns-6: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Gegenüber vom Dortmunder Hauptbahnhof steht ein großes Museum über eine Sportart. Über welche? → Fußball
- cities-and-towns-16: overlap like q-9424: An der Tür der Schlosskirche in Wittenberg soll Martin Luther 1517 seine Thesen angeschlagen haben. Wie viele waren es? → 95: In Wittenberg soll Martin Luther 1517 seine 95 Thesen an eine Kirchentür geschlagen haben. An welchem Tag? → 31. Oktober
- dialects-and-regional-words-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Ich sage „Griaß di“, trage zum Fest eine Lederhose und esse Weißwurst mit Brezn. Wer bin ich? → Ein Bayer
- gdr-everyday-life-14: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Ich bestellte aus dem Genex-Katalog Fernseher, Kühlschränke, sogar Autos für Leute in der DDR und zahlte in harter Währung. Wer war ich meist? → Ein Verwandter aus der Bundesrepublik
- gdr-history-15: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Was meinte der DDR-Auslandsgeheimdienst von Markus Wolf mit einem „Romeo“? → einen Agenten, der Sekretärinnen umwarb
- regional-dishes-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Wie heißt ein gebratenes Hackfleischbällchen in Berlin? → Bulette
- regional-dishes-10: fact-check wrong: The question text says "Was ist Glühwein?", which gives away the answer and makes the question ill-formed. The facts (spiced hot red wine, Striezelmarkt first mentioned 1434) are correct.: Man trinkt ihn auf dem Weihnachtsmarkt aus Tassen mit Pfand, Kinder bekommen stattdessen Punsch. Was ist Glühwein? → Heißer Rotwein mit Gewürzen
- sayings-and-idioms-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welcher „Preis“ ist im Sprichwort „Ohne Fleiß kein Preis“ gemeint? → Lohn für die Mühe
- sights-and-landmarks-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welches Berliner Bauwerk zeigt das Foto? → Berliner Dom
- sights-and-landmarks-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: In Dortmund steht Deutschlands größtes Stadion. Seine Tribüne heißt „Gelbe Wand“. Welcher Sport wird dort gespielt? → Fußball
- sights-and-landmarks-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Die Wilhelma in Stuttgart ist eine Seltenheit in Europa. Aus welchen zwei Teilen besteht sie? → Zoo und Botanischer Garten
- states-and-capitals-15: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Welches Münchner Fest zeigt das Foto? → Oktoberfest
- rivers-lakes-and-coasts-7: overlap like q-16987: Krabbenkutter laufen seit Generationen aus Husum, Büsum und Greetsiel aus, und die Krabben werden an Bord gekocht. In welchem Meer fischen sie? → Nordsee: Wer fährt mit solchen Booten an der Nordseeküste aufs Meer hinaus? → Krabbenfischer
- rivers-lakes-and-coasts-12: overlap like q-11051: Auf dem Foto liegen Boote im Schlick auf dem Trockenen. Was bringt das Wasser in ein paar Stunden zurück? → Die Flut: Zweimal am Tag ziehe ich das Wasser von der Nordseeküste weg. Dann liegen die Boote im Trockenen. Wer bin ich? → Ebbe
- sayings-and-idioms-0: overlap like q-13039: Wer tanzt im Märchen ums Feuer und singt: „Ach, wie gut, dass niemand weiß …“? → Rumpelstilzchen: Eine Märchenfigur hüpft auf einem Bein ums Feuer und singt: „Ach, wie gut, dass niemand weiß …“. Wer ist das? → Rumpelstilzchen
- sayings-and-idioms-15: overlap like q-9222: Eine schwarze Katze läuft dir über den Weg. Was bringt das nach altem Aberglauben? → Pech: An Silvester verschenkst du kleine Glücksbringer. Welcher davon bringt laut Aberglauben KEIN Glück? → Schwarze Katze
- series-and-crime-11: overlap like q-16930: Sonntagabend im Ersten läuft der Krimi „Tatort“. In welchem Jahrzehnt lief die allererste Folge? → 1970er: Erst um 20 Uhr die Tagesschau, dann sonntags um 20:15 Uhr im Ersten: Welche Art Sendung kommt da meistens? → Krimi
- sights-and-landmarks-1: overlap like chancellors-and-presidents-0: Sie wurde oft „Mutti“ genannt und war die erste Frau, die Deutschland als Bundeskanzlerin regierte. Wer ist sie? → Angela Merkel: Du stehst vor dem Bundeskanzleramt in Berlin. Wer regierte von hier aus als erste Frau Deutschland? → Angela Merkel
- sights-and-landmarks-13: overlap like q-15007: Hier ließ Karl der Große seine Pfalzkapelle bauen, hier liegt er begraben, und hier vermaßen Forscher 2014 seine Knochen. Welche Stadt ist das? → Aachen: Karl der Große ließ sie bauen, er liegt dort begraben, und 1978 kam sie als erste Stätte Deutschlands auf die Welterbeliste. Welche Kirche? → Aachener Dom
- states-and-capitals-6: overlap like q-14035: Du stehst in Berlin auf dem Alexanderplatz. Was ragt dort mit einer silbernen Kugel 368 Meter hoch in den Himmel? → Fernsehturm: Das höchste Bauwerk Deutschlands steht in Berlin. Was für ein Bauwerk ist es? → Fernsehturm
- states-and-capitals-9: overlap like q-9325: Wie heißt das Viergespann aus Pferden und Wagen mit der Siegesgöttin oben auf dem Brandenburger Tor? → Quadriga: Zähl nach: Wie viele Pferde ziehen den Wagen oben auf dem Brandenburger Tor? → 4
- states-and-capitals-10: overlap like q-11037: Ich stehe ganz oben auf Esel, Hund und Katze und mache Lärm, bis die Räuber fliehen. Wer bin ich? → Hahn: Bei den Bremer Stadtmusikanten steht der Hund auf dem Esel und die Katze auf dem Hund. Wer steht ganz oben? → Hahn
- states-and-capitals-12: overlap like q-5411: Which of these animals does NOT live in the wild around the Arctic Ocean? → Penguin: Du bist im Urlaub an der Nordsee. Welches Tier triffst du dort in freier Natur NICHT? → Pinguin
- states-and-capitals-13: overlap like q-15096: Du sitzt in München beim klassischen Weißwurstfrühstück. Was gehört traditionell NICHT auf den Tisch? → Sauerkraut: Am Imbiss gibt es eine klassische Currywurst. Was gehört NICHT darauf? → Sauerkraut
