# batch-49

Made by `qgen batch` on 2026-11-07 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): reformation-to-empire, chancellors-and-presidents, pop-and-rock, films-and-actors, federal-republic-and-reunification, founders-and-entrepreneurs, inventors-and-scientists, sights-and-landmarks, classic-literature, bundesliga-and-clubs, bread-and-baked-goods, sausages-and-cheese, early-history, cities-and-towns, regional-dishes, childrens-tv-and-audio-dramas, shows-and-presenters, series-and-crime, art-architecture-and-museums, national-symbols-and-state, legends-and-figures, childrens-books-and-comics, schlager-and-folk-music, plants-and-forests, gdr-everyday-life, gdr-history, transport
- Merged: 269 (q-14946…q-15214)
- Approved: 251
- Needs work: 18
- Dropped by the pipeline: 80
- Reviewed by: claude-opus-5-5
- Claude calls: 593, about $86.85 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-47, batch-48; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-47 | batch-48 | batch-49 |
|---|---|---:|---:|---:|
| source locale |  | es | en | de |
| drafts |  | 320 | 323 | 349 |
| skipped slots |  | 202 | 127 | 137 |
| dropped |  | 85 | 102 | 80 |
| drop rate | ≤ 20.0 % | 26.6 % ✗ | 31.6 % ✗ | 22.9 % ✗ |
| dropped: hard fail correct |  | 1 | 0 | 1 |
| dropped: hard fail unambiguous |  | 0 | 1 | 1 |
| dropped: hard fail no_giveaway |  | 13 | 23 | 21 |
| dropped: overlap |  | 71 | 74 | 55 |
| dropped: duplicate |  | 0 | 2 | 2 |
| dropped: fact-check wrong |  | 0 | 2 | 1 |
| merged |  | 235 | 221 | 269 |
| approved |  | 213 | 196 | 251 |
| needs_work |  | 22 | 25 | 18 |
| needs_work rate | ≤ 20.0 % | 9.4 % ✓ | 11.3 % ✓ | 6.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.6 % ✓ | 4.5 % ✓ | 1.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.9 % ✓ | 0.0 % ✓ | 2.2 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.5 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.1 % ✗ | 1.4 % ✗ | 1.5 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.8 % ✓ | 6.3 % ✓ | 1.9 % ✓ |
| media: no pick in review 1 |  | 40 | 27 | 41 |
| media: recovered by research |  | 34 | 20 | 37 |
| media: no pick at record |  | 6 | 8 | 4 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 23.8 % ✗ | 24.5 % ✗ | 17.5 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 50.9 % ✗ | 71.1 % ✓ | 74.1 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.11 ✓ | 1.27 ✓ | 1.76 ✗ |
| approved 11–15 |  | 47 | 54 | 55 |
| top move | ≤ 25.0 % | 13.6 % ✓ | 17.6 % ✓ | 14.1 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 88.1 % | 81.9 % | 82.2 % |
| values stimulus |  | 4 | 5 | 4 |
| top clue | ≤ 60.0 % | 43.0 % ✓ | 38.0 % ✓ | 42.8 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.1 % ✓ | 25.3 % ✓ | 30.9 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 17.0 % ✓ | 24.4 % ✓ | 20.4 % ✓ |
| values lens |  | 11 | 11 | 11 |
| media share | 15.0 %–50.0 % | 11.9 % ✗ | 18.1 % ✓ | 17.8 % ✓ |
| mean fun | ≥ 3.40 | 3.40 ✓ | 3.49 ✓ | 3.50 ✓ |
| cost $ |  | $72.25 | $64.67 | $83.13 |
| $ per approved | ≤ $0.35 | $0.34 ✓ | $0.33 ✓ | $0.33 ✓ |
| calls |  | 485 | 455 | 533 |
| calls per approved |  | 2.28 | 2.32 | 2.12 |
| wall time h |  | 2.04 | 1.74 | 2.37 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 11 (1 major), fact 1 (1 major), media 2 (2 major), style 1 (1 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.72

Major findings on approved questions:

None.

## Needs work

- **q-14947** (art-architecture-and-museums) Kostbare Stücke wie dieses aus dem Quedlinburger Domschatz verschwanden 1945 und tauchten 1990 wieder auf. Wer hatte sie mitgenommen? → Ein amerikanischer Offizier: None of the media candidates is usable. The search for "Quedlinburg Samuel Gospels" returned only Sam Cooke pictures: portraits, his grave, his camera, his outfit and a Billboard ad. The essential slot needs a photo of a piece from the Quedlinburg cathedral treasure, and no new search is allowed. A new search such as "Quedlinburg Domschatz reliquary" or "Samuhel-Evangeliar Quedlinburg" should be run manually. No suitable picture found for this question.
- **q-14975** (chancellors-and-presidents) Kurz nach dem russischen Angriff auf die Ukraine 2022 kündigte Olaf Scholz 100 Milliarden Euro extra an. Wer bekam das Geld? → Die Bundeswehr: Overlap with approved q-9164 ("In welchem Jahr sprach Olaf Scholz im Bundestag von einer „Zeitenwende“?" → 2022): this question says the announcement came in 2022, and hint 1 says it was made in the „Zeitenwende“ speech in the Bundestag. Anyone who sees this question gets q-9164's answer. Hint 1 should drop the „Zeitenwende“ reference and use a vague hint instead, for example that the announcement came in a special Bundestag session.
- **q-14977** (chancellors-and-presidents) Wer hat diese Handhaltung als Markenzeichen berühmt gemacht? → Angela Merkel: Fact check: uncertain. Answer and hints are fine. The 2013 giant CDU poster of the Raute near Berlin Hauptbahnhof is confirmed, and it was a mosaic of small pictures. I could not verify the 'over 2000 photos' number.
- **q-14978** (childrens-books-and-comics) Der kleine Bär und der kleine Tiger suchen das Land ihrer Träume. Ergänze den Buchtitel von Janosch: „Oh, wie schön ist …“ → Panama: The text is fine (the facts about Janosch's book, the hints and the fun fact all check out), but none of the image candidates shows the Tigerente or anything else from the book. They are a boomerang, toy trains, train tracks and a wooden castle. The slot needs a real Tigerente pull-along toy, or something from the book's world such as a teddy bear and a toy tiger, or a banana crate. No suitable picture found for this question.
- **q-15020** (federal-republic-and-reunification) Abends im Fernsehen: Wie lange dauert eine Sendung „Unser Sandmännchen“ ungefähr? → Etwa 10 Minuten: Fact check: uncertain. The usual length of 'Unser Sandmännchen' is reported as about 5–7 minutes (rbb: about 7). Only special Advent episodes ran 10–12 minutes. 'Etwa 10 Minuten' is therefore not accurate for a normal episode, though it is the closest of the options. The 22 Nov 1959 first broadcast is correct.
- **q-15038** (gdr-everyday-life) Die Simson S51 wurde ab 1980 in Suhl gebaut, hat 50 Kubikzentimeter und ist heute Kult bei Jugendlichen. Warum gerade bei ihnen? → Man darf sie mit Mopedführerschein 60 statt 45 km/h fahren: This asks the same fact as the approved q-12149: thanks to a rule from the reunification period, Simson mopeds may go 60 km/h. Seeing one question gives away the other. Also, the correct answer is noticeably longer and more specific than the distractors.
- **q-15043** (gdr-history) Die Hennecke-Bewegung von 1948 kopierte einen sowjetischen Rekord-Bergmann. Wann hatte dieser Vorbild-Rekord stattgefunden? → in den 1930er-Jahren: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-15065** (national-symbols-and-state) Das Grundgesetz sollte 1949 nur ein Provisorium bis zur deutschen Einheit sein. In welchem Jahr wurde es zur Verfassung ganz Deutschlands? → 1990: This asks the same fact as approved q-12230 (the year of German reunification, 1990). The year the Grundgesetz became the constitution of all Germany is just the reunification year in other words, and hints 2 and 3 (the Berlin Wall, 3 October) make that obvious. Drop it, or turn it into a different question about the Grundgesetz (for example the year 1949 or the city where it was adopted, Bonn).
- **q-15117** (sights-and-landmarks) Im Hamburger Hafen stehen riesige Kräne, so hoch wie Hochhäuser. Wozu dienen sie vor allem? → Container be- und entladen: Fact check: uncertain. The facts are fine (container cranes, Hamburg is Germany's largest seaport). But the image query 'Hamburg Speicherstadt canal' does not show cranes and does not match the question (the question says 'photo' stimulus).
- **q-15144** (gdr-everyday-life) Ab 1962 galt in der DDR die Wehrpflicht. Junge Männer bekamen um 18 Post und mussten 18 Monate in steingrauer Uniform dienen. Wohin? → Zur Nationalen Volksarmee: Hint 1 („Es war die eigene Armee der DDR.“) gives the answer away: of the four options, only the Nationale Volksarmee is the GDR's own army, so the first, supposedly vague hint already settles the question. Hint 1 should give vaguer context instead, e.g. the barracks life or that conscripts swore an oath, without saying it was the GDR's own army.
- **q-15145** (gdr-history) Willi Stoph leitete es lange, Hans Modrow 1989/90. Welches Gremium war die Regierung der DDR? → Ministerrat: The question text says Willi Stoph led the GDR government for a long time, which gives away approved q-12080 ("Brandt meets the DDR Ministerpräsident in Erfurt 1970 – who was it?" → Willi Stoph). q-12080 in turn ties Stoph to the head-of-government role and so hints at this answer. A reworded version could drop Stoph and keep only Modrow, or use another clue such as the seat or role of the body.
- **q-15159** (national-symbols-and-state) Sie ist aus Stoff, schwarz-rot-gold und wird über die Außenspiegel von Autos gezogen. Wen feuert man damit an? → Die Fußball-Nationalmannschaft: The text is fine, but none of the image candidates works. 1 and 2 are side views of 1980s AMC cars with a US flag hanging between fire-truck ladders, not a flag on a car mirror. 3 and 4 are Soviet savings cheques, 5 is an 1891 tram and 6 is a florist's display. Search again with something like 'Germany car mirror flag' or 'Autospiegel Fahne' for a picture of black-red-gold mirror covers on a car. No suitable picture found for this question.
- **q-15165** (reformation-to-empire) Welches dieser Märchen steht NICHT in den „Kinder- und Hausmärchen“ der Brüder Grimm? → Die kleine Meerjungfrau: The description ("fast jede Großmutter bekommt Ärger mit einem Wolf") points straight at Rotkäppchen. It tells players Rotkäppchen is in the collection, so that option is ruled out before any hint. Rewrite it to play on fairy tales or the Grimm brothers without hinting at any of the four tales, for example a joke about two brothers collecting stories instead of stamps.
- **q-15169** (sausages-and-cheese) Mett ist gewürztes Schweinehackfleisch, das man aufs Brötchen streicht. Warum muss man es noch am selben Tag essen? → Weil das Fleisch roh ist: Hint 3 ("Mett kommt nie in eine Pfanne") is factually wrong: Mett is often fried, e.g. in Käse-Lauch-Suppe, Mettbällchen or Mettsoße. Reword it so it is true, e.g. "Auf dem Brötchen wird Mett nicht gebraten oder gekocht."
- **q-15172** (schlager-and-folk-music) „Ich stehe ganz still und stumm auf einem Bein, trage ein purpurrotes Mäntlein und ein schwarzes Käppchen.“ Wer bin ich? → Das Männlein im Walde: Fact check: uncertain. The song's riddle solution is the Hagebutte (rose hip), as the hint and fun fact say. The answer "Das Männlein im Walde" is only the song's title figure. The question's paraphrase also differs from the original lyrics ("ein Männlein steht im Walde…"). Facts about Hoffmann von Fallersleben and the Hagebutte are correct.
- **q-15176** (schlager-and-folk-music) Im Titellied der „Biene Maja“ wird Maja mit drei Eigenschaften beschrieben. Welche gehört NICHT dazu? → fleißig: Fact check: uncertain. I couldn't retrieve the German lyrics. The words klein, frech and schlau match the well-known 'kleine, freche, schlaue Biene Maja' as I remember it, and 'fleißig' is not one of them. I couldn't verify that hint 2 is right about where these words sit relative to the line 'Und diese Biene, die ich meine, nennt sich Maja'.
- **q-15183** (sausages-and-cheese) An der Wursttheke fragt die Verkäuferin beim Aufschnitt: „Darf's ein bisschen mehr sein?“ Was meint sie damit? → Ob es etwas mehr als bestellt sein darf: The question text gives the answer away. The quoted phrase „Darf's ein bisschen mehr sein?“ means literally what the answer says („Ob es etwas mehr als bestellt sein darf“), so anyone who understands the words can just match it. Unlike an idiom such as „Das ist mir Wurst“, there is nothing to work out. A real question would need a non-literal angle, for example what really happens on the scale, or why sellers like to ask it.
- **q-15187** (schlager-and-folk-music) Hör zu: Welches Instrument aus dem Spielmannszug ist das? → Glockenspiel: No audio candidate is a plain glockenspiel recording. Candidates 1 and 4 are Lingua Libre/Commons recordings of someone saying the word „Glockenspiel“, which would give the answer away. Candidate 2 mixes clock chimes, tubular bells, handbells and vibraphone, and candidate 3 is the carillon on the Kiel town hall tower, not the hand-played instrument. Find a Freesound recording of a lyra or glockenspiel played alone, or drop the question. No suitable picture found for this question.

## Question axes

- move: analogy 7, cause_effect 20, count 6, estimate 16, identify 38, made_of 15, name_concept 28, odd_one_out 19, origin 13, purpose 22, record 4, sequence 18, when 12, who 28, word_meaning 23
- stimulus: detail 11, none 221, photo 33, sound 4
- clue: completion 7, direct 115, riddle 29, scenario 36, three_facts 82
- answer_kind: group 29, number 23, person 45, place 24, thing 83, time 18, word 47
- lens: body_senses 7, educational_media 24, everyday 51, history 55, language 37, nature 6, pop_culture 36, popular_science 1, school 35, science_news 1, university 16

## Dropped by the pipeline

- art-architecture-and-museums-11: overlap like q-9280: Dieses Fossil ist ein Archaeopteryx. In welchem Bundesland wurden alle bekannten Exemplare gefunden? → Bayern: Dieses Fossil ist einer der Stars im Berliner Museum für Naturkunde. Welches Tier ist es? → Archaeopteryx
- bread-and-baked-goods-3: overlap like q-9436: Vollkornmehl ist dunkel, Weißmehl hell. Welcher Teil des Getreidekorns fehlt im Weißmehl? → Schale: „Für mich wird das ganze Korn gemahlen, mit Schale und Keim. Früher aß man mein dunkles Brot auf dem Land, heute gilt es als gesund.“ Was bin ich? → Vollkornmehl
- bread-and-baked-goods-5: overlap like q-12134: Ich bin eine Fernsehsendung mit vielen Puppen, in Deutschland seit 1973. In meinem Lied heißt es: „Wer nicht fragt, bleibt dumm!“ Wer bin ich? → Sesamstraße: Du schaust Kinderfernsehen und siehst das blaue Krümelmonster Kekse futtern. In welcher Straße wohnt es? → Sesamstraße
- bundesliga-and-clubs-5: overlap like q-0735: La hace todo el estadio a la vez: la gente se pone de pie y se vuelve a sentar por turnos. Se volvió famosa en el mundo gracias al Mundial de México 1986. ¿Qué es? → La ola: Die Fans auf dem Bild machen „La Ola“. Woher hat die Bewegung ihren Namen? → Vom spanischen Wort für „Welle“
- chancellors-and-presidents-2: overlap like q-9236: Man braucht die Mehrheit im Bundestag und muss zugleich einen Nachfolger wählen. Wen stürzt ein konstruktives Misstrauensvotum? → Bundeskanzler: 1972 wollte die Union Willy Brandt stürzen und Rainer Barzel zum Kanzler wählen. Es fehlten zwei Stimmen. Wie heißt dieses Verfahren? → Konstruktives Misstrauensvotum
- chancellors-and-presidents-10: overlap like q-10933: Wie viele Kreuze darf man bei einer Bundestagswahl auf dem Stimmzettel machen? → 2: Bei der Bundestagswahl kreuzt du links auf dem Stimmzettel eine Person an. Was wählst du mit der Zweitstimme rechts? → Eine Partei
- chancellors-and-presidents-15: overlap like q-12143: Diese Politikerin war 16 Jahre lang Bundeskanzlerin. Welcher Partei gehört sie an? → CDU: Wie viele Jahre war Angela Merkel, genannt „Mutti“, Bundeskanzlerin? → 16
- chancellors-and-presidents-16: overlap like q-10939: Nach wie vielen Jahren wird der Bundestag regulär neu gewählt? → 4: Welche dieser Amts- oder Wahlperioden dauert regulär NICHT fünf Jahre? → Bundestag
- childrens-tv-and-audio-dramas-0: overlap like q-9231: Welches Wort fehlt bei der „Sendung mit der Maus“: „Lach- und …geschichten“? → Sach: Nach der Titelmelodie der „Sendung mit der Maus“ verrät eine Stimme, was gleich kommt. Wie nennt sie die Geschichten? → Lach- und Sachgeschichten
- childrens-tv-and-audio-dramas-8: overlap like q-10862: „Ich bin jung, kann zaubern und wohne in Neustadt. Ich fliege auf Kartoffelbrei, und meine Sprüche enden mit „Hex-hex!“. Wer bin ich?“ → Bibi Blocksberg: „Ich bin aus Holz und Reisig, fliege eine kleine Hexe durch Neustadt und lande oft ziemlich wackelig.“ Wie heißt der Hexenbesen? → Kartoffelbrei
- childrens-tv-and-audio-dramas-15: overlap like q-12972: Toggo, Toggolino für die Kleinen und das Toggo Radio: Zu welchem Fernsehsender gehört diese Kindermarke? → Super RTL: Privatsender aus Köln, gestartet 1995, tagsüber Kinderprogramm, abends Filme für Erwachsene: Wie heißt er? → Super RTL
- childrens-tv-and-audio-dramas-16: overlap like q-10859: Welche Farbe hat KEINE der drei Figuren Maus, Elefant und Ente aus der „Sendung mit der Maus“? → Grün: „Ich bin klein und blau, habe einen Rüssel und tröte gern. Ich bin der Freund der orangen Maus.“ Wer bin ich? → Elefant
- cities-and-towns-9: overlap like q-12175: In Wolfsburg stehen zwei gläserne Türme, die fast bis oben gefüllt sind. Womit? → Neuwagen: In Wolfsburg steht das große Werk von Volkswagen. Was bedeutet der Name „Volkswagen“? → Ein Auto für alle Leute
- cities-and-towns-11: overlap like q-12226: Bis zu welcher Uhrzeit isst man Weißwürste traditionell? → Bis 12 Uhr mittags: Wann isst man in München traditionell Weißwurst mit süßem Senf und Brezn? → Vor 12 Uhr mittags
- cities-and-towns-15: overlap like q-12208: Ich kam 1875 in Lübeck zur Welt und schrieb über eine Kaufmannsfamilie meiner Heimatstadt. 1929 bekam ich den Literaturnobelpreis. Wer bin ich? → Thomas Mann: Thomas Mann ließ hier seinen Roman „Buddenbrooks“ spielen, Willy Brandt kam hier zur Welt, und ein Stadttor war auf dem 50-Mark-Schein. Welche Stadt? → Lübeck
- cities-and-towns-16: overlap like q-11039: Sie ist Deutschlands größtes Raubtier, bekommt ihre weißen Babys im Winter und liegt gern auf der Helgoländer Düne. Welches Tier ist gemeint? → Kegelrobbe: Am Strand der Helgoländer Düne liegen sie oft zu Hunderten: die größten Raubtiere Deutschlands. Welche Tiere sind es? → Kegelrobben
- classic-literature-1: overlap like q-14978: Der kleine Bär und der kleine Tiger suchen das Land ihrer Träume. Ergänze den Buchtitel von Janosch: „Oh, wie schön ist …“ → Panama: Du liest Janoschs „Oh, wie schön ist Panama“ vor. Wie viele Freunde machen sich darin auf die Suche nach Panama? → 2
- classic-literature-15: overlap like q-14118: Bei Erich Kästner merken Luise und Lotte im Ferienheim, dass sie Zwillinge sind. Was müssen sie ändern, um heimlich die Rollen zu tauschen? → Frisur: In Erich Kästners „Das doppelte Lottchen“ treffen sich im Ferienheim Mädchen, die gleich aussehen. Wie viele sind es? → 2
- early-history-0: overlap like q-9172: Ich dufte nach Zimt und Nelken, Nürnberg ist seit Jahrhunderten für mich berühmt, und auf dem Christkindlesmarkt bin ich überall. Was bin ich? → Lebkuchen: Es duftet nach Honig und Gewürzen, man backt es im Advent, und daraus baut man oft das Hexenhaus von Hänsel und Gretel. Was ist es? → Lebkuchen
- early-history-7: overlap like q-9220: Zimmerleute auf der Walz tragen schwarze Kluft und großen Hut und sind mindestens drei Jahre und einen Tag unterwegs. Welcher Ort ist für sie dann tabu? → Der eigene Heimatort: Junge Handwerker in schwarzer Kluft mit Hut sind drei Jahre und einen Tag unterwegs und dürfen nicht nach Hause. Warum gehen sie auf die Walz? → Um bei fremden Meistern zu lernen
- early-history-10: duplicate like q-9348: Den Döner im Brot wie auf dem Foto gibt es so vermutlich erst seit den 1970ern. In welcher deutschen Stadt kam er auf? → Berlin: Dieses Wappen gehört zu einer deutschen Stadt. Zu welcher? → Berlin
- early-history-11: overlap like q-9581: Roman soldiers invading Britain could lock their shields together in a formation called the “testudo”. What was it for? → Blocking arrows and stones: Römische Legionäre am Rhein stellten sich im Kampf so mit ihren Schilden auf. Wozu diente diese „Schildkröte“? → Schutz vor Pfeilen und Steinen
- federal-republic-and-reunification-2: overlap like q-12042: Solche Flugzeuge brachten 1948/49 Lebensmittel und Kohle nach West-Berlin. Welchen Spitznamen gaben ihnen die Berliner? → Rosinenbomber: Du feierst in der Nacht des 9. November 1989 an der Berliner Mauer. Welches Wort stammt NICHT aus dieser Wendezeit? → Rosinenbomber
- federal-republic-and-reunification-13: overlap like q-12067: In der DDR fuhr man am Wochenende auf die „Datsche“: Laube, Beete und Obstbäume, oft am Stadtrand. Aus welchem Land stammt dieses Wort? → Russland: In der DDR fuhren viele am Wochenende in ihr kleines Häuschen mit Garten, oft am See. Das Wort dafür kommt aus dem Russischen. Wie heißt es? → Datsche
- federal-republic-and-reunification-14: overlap like q-10846: In welchem Jahrzehnt erschienen die ersten Hörspielkassetten von „Benjamin Blümchen“ und „Die drei ???“? → 1970er: In welchem Jahrzehnt erschien die erste Hörspielfolge von „Die drei ???“ in Deutschland? → In den 1970er-Jahren
- films-and-actors-8: overlap like q-10885: Dieser Mann drehte „(T)Raumschiff Surprise – Periode 1“ und spielte darin selbst mit. Wer ist es? → Michael Herbig: Dieser Münchner Komiker trägt einen Spitznamen, der auf Englisch „Rüpel“ bedeutet. Wer ist er? → Michael „Bully“ Herbig
- founders-and-entrepreneurs-7: overlap like q-1859: Soy una marca alemana de ropa deportiva y mi lema es 'Imposible no es nada'. ¿Quién me fundó? → Adi Dassler: Was stellte Adi Dassler in den 1920er-Jahren in der Waschküche seiner Mutter in Herzogenaurach her? → Sportschuhe
- founders-and-entrepreneurs-12: overlap like q-13990: Wie geht der Haribo-Spruch weiter: „Haribo macht Kinder froh und … ebenso“? → Erwachsene: Wie geht der Werbespruch weiter: „Haribo macht Kinder froh und …“? → Erwachsene ebenso
- founders-and-entrepreneurs-17: overlap like q-14116: Um 1902 brachte die Spielzeugfirma Steiff aus Giengen ein Plüschtier heraus, das bis heute weltberühmt ist. Welches? → Teddybär: Märklin ist zu Modelleisenbahn wie Steiff zu …? → Teddybär
- gdr-everyday-life-9: overlap like q-12066: „Ich hatte zehn Klassen, fast alle Kinder der DDR gingen zu mir, und ab Klasse 7 schickte ich sie regelmäßig in echte Betriebe.“ Wer bin ich? → Die Polytechnische Oberschule: Du gehst in der DDR zur POS und hast einmal pro Woche Unterrichtstag in der Produktion, also im Betrieb. Ab welcher Klasse gab es das? → 7
- gdr-everyday-life-11: overlap like q-11075: Ich moderierte ab 1960 im DDR-Fernsehen „Der schwarze Kanal“ und kommentierte dort Ausschnitte aus dem Westfernsehen. Wer bin ich? → Karl-Eduard von Schnitzler: Ich zeigte im DDR-Fernsehen ab 1960 montags zerschnittene Westsendungen und erklärte sie. Man nannte mich spöttisch „Sudel-Ede“. Wer bin ich? → Karl-Eduard von Schnitzler
- inventors-and-scientists-4: overlap like q-2749: “I was a German engineer. In the 1890s I built an engine that lights its fuel just by squeezing air, with no spark.” Who am I? → Rudolf Diesel: Der Kraftstoff an dieser Zapfsäule ist nach einem deutschen Erfinder benannt. Wie hieß er? → Rudolf Diesel
- inventors-and-scientists-10: overlap like q-5688: I lived in Germany and hated bitter coffee grounds in my cup. In 1908, I poked holes in a brass pot and lined it with paper from my son's school notebook. Who am I? → Melitta Bentz: Eine Dresdner Hausfrau bastelte mich 1908 aus dem Löschpapier ihres Sohnes. Ich halte gemahlene Bohnen zurück. Was bin ich? → Kaffeefilter
- inventors-and-scientists-16: overlap like q-4910: Ulm Minster in Germany has a church tower 161.5 m (530 ft) tall with 768 steps. Which famous scientist was born in the same city? → Albert Einstein: Die Formel „E = mc²“ veröffentlichte 1905 ein in Ulm geborener Physiker. Wer war es? → Albert Einstein
- legends-and-figures-6: overlap like q-3580: I bathed in a dragon's blood, so no weapon could hurt me, except where a leaf stuck to my back. Who am I, hero of the Song of the Nibelungs? → Siegfried: Der Held Siegfried besiegt einen Drachen, badet in dessen Blut und bekommt eine Haut wie aus Horn. Was ist er danach? → unverwundbar
- legends-and-figures-9: overlap like q-9368: Auf wen geht der Name der Stadt „München“ zurück? → Mönche: Dieses Kind im Mönchsgewand ist das Wappenzeichen welcher Stadt? → München
- legends-and-figures-17: overlap like childrens-tv-and-audio-dramas-8: „Ich bin aus Holz und Reisig, fliege eine kleine Hexe durch Neustadt und lande oft ziemlich wackelig.“ Wie heißt der Hexenbesen? → Kartoffelbrei: Bibi Blocksberg fliegt auf ihm, er ist ein echter Hexenbesen und heißt wie ein Essen. Wie lautet sein Name? → Kartoffelbrei
- plants-and-forests-10: overlap like early-history-0: Es duftet nach Honig und Gewürzen, man backt es im Advent, und daraus baut man oft das Hexenhaus von Hänsel und Gretel. Was ist es? → Lebkuchen: Zur Adventszeit bauen viele Familien das Haus der Hexe aus „Hänsel und Gretel“ nach. Wie heißt es? → Lebkuchenhaus
- pop-and-rock-7: overlap like q-14090: Wer saß bei „Deutschland sucht den Superstar“ seit 2002 in den meisten Staffeln in der Jury? → Dieter Bohlen: Ich bin eine Castingshow bei RTL, seit 2002 im Programm. Mein allererster Sieger war Alexander Klaws. Was bin ich? → „Deutschland sucht den Superstar“
- reformation-to-empire-2: overlap like q-11024: Erstklässler bekommen eine riesige Tüte, die Zweitklässler führen ein Stück auf, und alle Eltern filmen. Welche Feier ist das? → Einschulungsfeier: Wer bekommt in Deutschland traditionell so eine große, bunte Tüte voller Überraschungen geschenkt? → Kinder am ersten Schultag
- reformation-to-empire-15: overlap like q-8893: Many American kids “graduate” from kindergarten in tiny caps and gowns. The word “kindergarten” comes from German: what does it mean? → Children's garden: Friedrich Fröbel eröffnete 1840 in Thüringen den ersten Kindergarten. Wie sollten die Kinder dort nach seiner Idee wachsen? → Wie Pflanzen in einem Garten
- regional-dishes-9: overlap like q-13176: Auf diesem Brötchen liegen „Nordseekrabben“. Zu welcher Tiergruppe gehören sie in Wahrheit? → Garnelen: Nordseekrabben wie auf dem Foto heißen zwar Krabben. Zu welcher Tiergruppe gehören sie aber wirklich? → Garnelen
- regional-dishes-14: overlap like cities-and-towns-2: Du willst auf den berühmten Hamburger Fischmarkt an der Elbe zwischen St. Pauli und Altona. Wann musst du hin? → Sonntag ganz früh am Morgen: Ich öffne sonntags im Morgengrauen, Marktschreier preisen bei mir Aale an, und Fischbrötchen gibt's schon zum Sonnenaufgang. Wer bin ich? → Hamburger Fischmarkt
- art-architecture-and-museums-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Der Düsseldorfer Rheinturm wurde 1981 eröffnet und hat oben ein Drehrestaurant. Wofür wurde er vor allem gebaut? → Für Funk und Fernsehen
- bread-and-baked-goods-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Das Fladenbrot hat seinen Namen vom Wort „Fladen“. Was ist ein Fladen? → Etwas Flaches und Rundes
- bread-and-baked-goods-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Es wird auf Empfängen in Schalen gereicht, ist außen braun und knusprig und wird mit den Fingern gegessen. Woraus besteht Laugenkonfekt? → Kleine Stücke Brezelteig
- shows-and-presenters-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ich bin ein E-Sport-Team, spiele „League of Legends“ und wurde vom Streamer HandOfBlood gegründet. Wer bin ich? → Eintracht Spandau
- shows-and-presenters-14: fact-check wrong: The fun fact is overstated. The video was among the most disliked on YouTube (about 3.3M dislikes, around 6th place in 2017, later 15th to 34th). It is not clearly 'one of the most disliked worldwide' today, and dislike counts are now hidden. The rest checks out.: Sie verkauft den Duschschaum „Bilou“, sang 2017 „How It Is (Wap Bap …)“ und war mit Julienco verheiratet. Unter welchem Namen wurde sie bekannt? → BibisBeautyPalace
- sights-and-landmarks-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Günzburg in Bayern gibt es einen Freizeitpark mit ganzen Städten im Kleinformat aus Millionen bunter Steine. Nach welchem Spielzeug heißt er? → Lego
- transport-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ich habe Streifen wie ein Tier aus Afrika, liege quer über der Straße, und Autos müssen halten, wenn du über mich gehen willst. Was bin ich? → Zebrastreifen
- transport-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Du fährst seit Stunden auf der Autobahn und fährst ab auf einen Parkplatz ohne Tankstelle. Wofür ist er vor allem da? → Um Pause zu machen und auszuruhen
- bundesliga-and-clubs-3: overlap like q-2548: This coach won the Champions League with both Barcelona and Manchester City. Who is he? → Pep Guardiola: Ich trage an der Seitenlinie gern Rollkragenpullover und wurde zwischen 2013 und 2016 dreimal in Folge Meister mit Bayern. Wer bin ich? → Pep Guardiola
- childrens-books-and-comics-15: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Seit 1976 erleben die Abrafaxe im DDR-Comicheft „Mosaik“ ihre Abenteuer. Welche Figuren waren vorher die Helden des Hefts? → Die Digedags
- cities-and-towns-2: overlap like regional-dishes-14: Ich öffne sonntags im Morgengrauen, Marktschreier preisen bei mir Aale an, und Fischbrötchen gibt's schon zum Sonnenaufgang. Wer bin ich? → Hamburger Fischmarkt: Du willst auf den berühmten Hamburger Fischmarkt an der Elbe zwischen St. Pauli und Altona. Wann musst du hin? → Sonntag ganz früh am Morgen
- early-history-16: overlap like q-12979: Der Speyerer Dom wurde ab 1030 von den Saliern gebaut und birgt Gräber von acht Kaisern und Königen. Er ist die größte erhaltene Kirche welchen Stils? → Romanik: Die Abtei Maria Laach hat dicke Mauern, kleine Fenster und viele Rundbögen. Zu welchem Baustil gehört sie? → Romanik
- films-and-actors-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: „Ich bin ein deutscher Medienpreis, ein Verlag verleiht mich, und das schon seit 1948.“ Wer bin ich? → Bambi
- founders-and-entrepreneurs-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Es kommt von Henkel aus Düsseldorf, gibt es seit 1907 und als Pulver, Gel oder Kapsel. Was ist Persil? → Waschmittel
- founders-and-entrepreneurs-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Welche Farbe gibt es bei den klassischen Haribo-Goldbären nicht? → Blau
- founders-and-entrepreneurs-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Händler gründeten mich 1898 in Berlin als „Einkaufsgenossenschaft der Kolonialwarenhändler“. Was bin ich heute? → Edeka
- founders-and-entrepreneurs-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Der Otto-Versand schickte bis 2018 jedes Jahr dicke Hefte an Millionen Haushalte. Was war das? → Versandkatalog
- gdr-everyday-life-5: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: Die SED bekämpfte sie 1953 heftig, und Schüler flogen ihretwegen sogar von der Oberschule. Was war die Junge Gemeinde? → Evangelische Jugendgruppen
- gdr-everyday-life-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In vielen DDR-Küchen, Kantinen und Wohnzimmern gab es Sprelacart. Wofür nutzte man es? → Als abwaschbare Oberfläche für Möbel
- gdr-history-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ab 1991 standen in Berlin frühere DDR-Grenzsoldaten und später auch DDR-Politiker vor Gericht. Wie nennt man diese Verfahren? → Mauerschützenprozesse
- inventors-and-scientists-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Die Thermoskanne hat ihren Namen aus dem Griechischen. Was bedeutet das Wort „thermos“? → warm
- legends-and-figures-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In Norddeutschland liegen tonnenschwere Steinblöcke aus der Steinzeit. Wer hat sie der Sage nach dorthin geschleppt? → Riesen
- plants-and-forests-5: duplicate like q-13047: Diese Blätter sind auf den deutschen 1-, 2- und 5-Cent-Münzen zu sehen. Von welchem Baum stammen sie? → Eiche: Früher trieb man im Herbst Schweine in den Wald, damit sie solche Früchte fressen. Von welchem Baum stammen sie? → Eiche
- plants-and-forests-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Auf einer Bergwiese hängen blauviolette Blüten wie kleine umgedrehte Becher an dünnen Stielen. Welche Blume ist das? → Glockenblume
- plants-and-forests-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Du zählst an einem Baumstumpf 60 Jahresringe. Wie alt war der Baum ungefähr, als er gefällt wurde? → 60 Jahre
- reformation-to-empire-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Friedrich der Große ließ dieses Sommerschloss auf Weinbergterrassen bauen, und auf seinem Grab dort liegen oft Kartoffeln. Welches Schloss? → Sanssouci
- sausages-and-cheese-1: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Er ist aus Hefeteig, aus drei Strängen geflochten und oft mit Hagelzucker bestreut. Zu welchem Fest backen ihn viele Familien besonders gern? → Ostern
- sausages-and-cheese-6: overlap like q-9366: Dieser Käse wird von Hand geformt, ist eine hessische Spezialität und kommt mit Zwiebeln und Essig „mit Musik“ auf den Tisch. Woraus macht man ihn? → Sauermilchquark: Handkäse aus Hessen wird aus Sauermilchquark gemacht. Wie viel Fett steckt ungefähr in 100 Gramm davon? → Weniger als 1 Gramm
- sausages-and-cheese-17: overlap like q-13091: Aus welchem Gemüse wird dieses typisch deutsche Gericht gemacht? → Weißkohl: Sauerkraut ist sauer und liegt oft neben der Bratwurst auf dem Teller. Aus welchem Gemüse wird es gemacht? → Weißkohl
- schlager-and-folk-music-0: overlap like q-15083: Du sitzt im Mai vor dem Fernseher: Deutschland hat diesen Wettbewerb 1982 mit Nicole und 2010 mit Lena gewonnen. Wie heißt er? → Eurovision Song Contest: Mit „Satellite“ gewann Lena den Eurovision Song Contest für Deutschland. In welchem Jahr war das? → 2010
- schlager-and-folk-music-14: overlap like q-14113: Ergänze: Gewürznelken stecken im Glühwein. Ihr Name „Nelke“ kommt von einem alten Wort für kleine … → Nägel: Im Wiegenlied „Guten Abend, gut' Nacht“ ist das Kind „mit Rosen bedacht, mit Näglein besteckt“. Was sind Näglein? → Nelken
- series-and-crime-2: overlap like q-10875: In Janoschs Geschichten zieht der kleine Tiger sie an einer Schnur hinter sich her. Wie heißt das gelb-schwarz gestreifte Holztier auf Rädern? → Tigerente: Der „Tigerenten Club“ ist nach einem gestreiften Holzspielzeug benannt. Aus wessen Büchern stammt die Tigerente? → Janosch
- series-and-crime-3: overlap like q-10890: Wer spielt im Münsteraner „Tatort“ den eitlen Rechtsmediziner Professor Karl-Friedrich Boerne? → Jan Josef Liefers: Ich bin Rechtsmediziner im Tatort aus Münster, ziemlich eitel und nenne meine kleine Assistentin „Alberich“. Wer bin ich? → Karl-Friedrich Boerne
- shows-and-presenters-0: overlap like q-2823: On The Bachelor, what does the bachelor give to each woman he wants to keep on the show? → A rose: Ich bin Junggeselle, suche bei RTL unter vielen Frauen die große Liebe und verteile in jeder Nacht Rosen. Wer bin ich? → Der Bachelor
- shows-and-presenters-16: overlap like q-12173: Ich bin Modedesigner und bewerte bei VOX, wie Kandidatinnen mit 500 Euro in vier Stunden ein Outfit zu einem Motto kaufen. Wer bin ich? → Guido Maria Kretschmer: Bei „Shopping Queen“ gilt es die ganze Woche für alle Kandidatinnen, und jedes Outfit wird danach bewertet. Wie heißt diese Vorgabe in der Show? → Motto
- sights-and-landmarks-7: overlap like q-11987: Dieser Verein spielt in Schwarz-Gelb, hat eine Biene namens Emma als Maskottchen und im Stadion die riesige „Gelbe Wand“. Welcher ist es? → Borussia Dortmund: Welcher Verein trägt in diesem Stadion seine Heimspiele aus? → Borussia Dortmund
- sights-and-landmarks-12: overlap like q-15007: Hier ließ Karl der Große seine Pfalzkapelle bauen, hier liegt er begraben, und hier vermaßen Forscher 2014 seine Knochen. Welche Stadt ist das? → Aachen: Karl der Große ließ ihn bauen, rund 30 Könige wurden dort gekrönt, und 1978 wurde er als erstes deutsches Bauwerk Welterbe. Welcher Dom? → Aachener Dom
