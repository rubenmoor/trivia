# batch-53

Made by `qgen batch` on 2026-11-07 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): athletes-and-other-sports, empire-weimar-and-nazi-era, art-architecture-and-museums, mountains-and-landscapes, gdr-history, rap-and-electronic, gdr-everyday-life, childrens-tv-and-audio-dramas, pop-and-rock, reformation-to-empire, films-and-actors, brands-and-products, federal-republic-and-reunification, chancellors-and-presidents, shows-and-presenters, national-symbols-and-state, national-team, state-and-city-emblems, dialects-and-regional-words, parks-weather-and-climate, sayings-and-idioms, inventors-and-scientists, family-customs-and-dress, cities-and-towns, holidays-through-the-year, drinks, slang-and-everyday-words
- Merged: 264 (q-15904…q-16167)
- Approved: 243
- Needs work: 21
- Dropped by the pipeline: 73
- Reviewed by: claude-opus-5-5
- Claude calls: 548, about $79.91 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-51, batch-52; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-51 | batch-52 | batch-53 |
|---|---|---:|---:|---:|
| source locale |  | es | en | de |
| drafts |  | 328 | 316 | 337 |
| skipped slots |  | 194 | 134 | 149 |
| dropped |  | 101 | 86 | 73 |
| drop rate | ≤ 20.0 % | 30.8 % ✗ | 27.2 % ✗ | 21.7 % ✗ |
| dropped: hard fail correct |  | 3 | 1 | 0 |
| dropped: hard fail unambiguous |  | 2 | 1 | 1 |
| dropped: hard fail no_giveaway |  | 14 | 12 | 19 |
| dropped: overlap |  | 76 | 70 | 51 |
| dropped: duplicate |  | 4 | 2 | 2 |
| dropped: fact-check wrong |  | 2 | 0 | 1 |
| merged |  | 227 | 230 | 264 |
| approved |  | 207 | 212 | 243 |
| needs_work |  | 20 | 18 | 21 |
| needs_work rate | ≤ 20.0 % | 8.8 % ✓ | 7.8 % ✓ | 8.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.2 % ✓ | 2.6 % ✓ | 1.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.4 % ✓ | 0.9 % ✓ | 1.1 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.8 % ✗ | 0.4 % ✓ | 1.5 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.4 % ✓ | 4.8 % ✓ | 4.2 % ✓ |
| media: no pick in review 1 |  | 39 | 21 | 29 |
| media: recovered by research |  | 32 | 15 | 21 |
| media: no pick at record |  | 7 | 7 | 8 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.8 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 25.6 % ✗ | 23.1 % ✗ | 16.9 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 50.5 % ✗ | 68.6 % ✓ | 67.1 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 2.12 ✗ | 1.35 ✓ |
| approved 11–15 |  | 48 | 35 | 50 |
| top move | ≤ 25.0 % | 13.2 % ✓ | 14.8 % ✓ | 12.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 85.0 % | 77.4 % | 87.9 % |
| values stimulus |  | 4 | 6 | 5 |
| top clue | ≤ 60.0 % | 37.4 % ✓ | 47.4 % ✓ | 42.4 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 22.0 % ✓ | 25.7 % ✓ | 25.0 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 18.1 % ✓ | 20.4 % ✓ | 22.3 % ✓ |
| values lens |  | 10 | 10 | 11 |
| media share | 15.0 %–50.0 % | 15.0 % ✗ | 22.6 % ✓ | 12.1 % ✗ |
| mean fun | ≥ 3.40 | 3.41 ✓ | 3.44 ✓ | 3.38 ✗ |
| cost $ |  | $68.24 | $65.05 | $76.22 |
| $ per approved | ≤ $0.35 | $0.33 ✓ | $0.31 ✓ | $0.31 ✓ |
| calls |  | 452 | 463 | 488 |
| calls per approved |  | 2.18 | 2.18 | 2.01 |
| wall time h |  | 2.13 | 2.00 | 2.34 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 55 (2 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 8 (1 major), fact 3 (0 major), overlap 3 (1 major), media 1 (1 major), difficulty 2 (0 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.69

Major findings on approved questions:

- **q-16007**: giveaway — The question text gives the answer away. It asks for the name of this "Kurskorrektur", and "Neuer Kurs" is the only option with "Kurs" in it, so a player with no DDR knowledge can still pick it. A neutral word like "Wende" or "Kursänderung des Politbüros" would avoid this, but the "Kurs" stem must go. The facts check out: the Politbüro decided it on 9 June and Neues Deutschland printed it on 11 June 1953, the price increases were taken back but the higher work norms were not, and the Stalinallee strike followed on 16 June. The wrong answers are all clearly wrong (NÖS 1963, Aufbau des Sozialismus 1952, Hauptaufgabe 1971). Without the giveaway I'd rate it about 13, not 15. (http://127.0.0.1:8001/review/q-16007)

## Needs work

- **q-15921** (athletes-and-other-sports) Carl-Uwe „Charly“ Steeb schlug 1988 im Finale in Göteborg Mats Wilander. So holte Deutschland erstmals welchen Titel? → Davis Cup: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-15931** (chancellors-and-presidents) 2015 kamen sehr viele Geflüchtete über die Balkanroute nach Deutschland, oft am Münchner Hauptbahnhof an. Aus welchem Land kamen die meisten? → Syrien: The question overlaps too much with approved q-9159 (Merkel's "Wir schaffen das", 31 August 2015 → "Aufnahme vieler Geflüchteter"). This text says outright that very many refugees came to Germany in 2015, so a player who sees it first gets q-9159's answer handed to them. Both questions cover the same 2015 refugee event in the same subcategory.
- **q-15932** (childrens-tv-and-audio-dramas) Der kleine blaue Elefant bekam eine eigene Sendung für Vorschulkinder. In wessen Sendung spielte er vorher eine Nebenrolle? → Maus: Overlaps approved q-10859 ("Welche Farbe hat KEINE der drei Figuren Maus, Elefant und Ente aus der „Sendung mit der Maus“?"). That question states outright that the elephant belongs to the Maus show, which is the whole fact asked here, so seeing one gives the other away. The facts themselves check out (elephant added 1975, own show 2007), and candidate 1 would be a fine illustrative image.
- **q-15950** (dialects-and-regional-words) Zu wem sagt man normalerweise NICHT „Schatzi“? → zum Schulleiter: Hint 2 has a grammar error that players will see: "Man sagt ihn zu jemandem …" uses "ihn", but hint 1 calls it "das Wort", which is neuter. It should be "Man sagt es zu jemandem, den man sehr lieb hat." Everything else works: the facts are fine, there's no giveaway, and it doesn't repeat q-10882 (that one asks for the term "Kosename").
- **q-15962** (drinks) Er steht im Supermarkt, hat ein rundes Loch und brummt beim Arbeiten. Seit 2003 hat er noch mehr zu tun. Wofür ist er da? → Leere Flaschen zurückgeben: This overlaps approved q-9392 (Pfandbon riddle). Its text says „Ich komme aus dem Automaten, nachdem du leere Flaschen hineingesteckt hast“, which directly answers what the Pfandautomat is for, so seeing one question gives the other away. The pool also already covers deposits through q-9391 (25 Cent) and q-14015 (Mehrweg).
- **q-15970** (empire-weimar-and-nazi-era) In welchem Jahr stellte Märklin auf der Leipziger Messe seine erste Spielzeugeisenbahn mit Schienen vor? → 1891: Hints 1 and 2 each give the answer away. 'Damals regierte noch ein Kaiser' rules out 1925, 1955 and 1972, since the German monarchy ended in 1918. 'Echte Eisenbahnen erst seit gut 50 Jahren' (from 1835) points straight to about 1890. Hint 1 should be vague, for example about the company's Swabian workshop origins, and hint 2 should not let anyone work out the decade. Another option is to move the wrong answers closer to 1891 (for example 1871, 1902, 1912) so the Kaiser hint is no longer decisive.
- **q-15989** (federal-republic-and-reunification) „Die Würde des Menschen ist unantastbar“ steht im ersten Artikel des Grundgesetzes. Seit welchem Jahr gilt er? → 1949: The only media candidate is an 1891 American streetcar scan, which has nothing to do with the Grundgesetz, and no new search is allowed. The slot needs a photo of the Grundgesetz glass panels on the Spree in Berlin (Jakob-Kaiser-Haus), or a Bundestag/Reichstag photo with no year visible. No suitable picture found for this question.
- **q-16003** (gdr-everyday-life) Dieses Gericht heißt im Osten scherzhaft „Tote Oma“. Woraus besteht die dunkle Masse auf dem Teller hauptsächlich? → Gebratene Grützwurst: None of the candidates shows Tote Oma: they are Botswanan samp and beans (1, 2), a yellow Nigerian mash (3, 4) and raw Moroccan tripe (5, 6). No new search is allowed. Also, the wrong answer „Zerdrücktes Bratkartoffeln“ is ungrammatical and must be „Zerdrückte Bratkartoffeln“. The image could become a decorative or illustrative one (for example „sauerkraut boiled potatoes“), since Commons may not have a clean Tote Oma photo. No suitable picture found for this question. Fact check: wrong. The wrong answer "Zerdrücktes Bratkartoffeln" is ungrammatical, because Bratkartoffeln is plural. The facts are fine: Tote Oma is fried Grützwurst or Blutwurst with potatoes and sauerkraut.
- **q-16017** (holidays-through-the-year) Am zweiten Sonntag im Mai basteln Kinder Karten, pflücken Blumen und machen Frühstück ans Bett. Für wen? → Für die Mama: Hint 2 („Sie hat dich auf die Welt gebracht.“) gives the answer away: only the mother fits it. Hint 1 („Der Tag heißt nach dieser Person.“) also comes very close, because it points straight to Muttertag. Hint 2 should be replaced with a vaguer clue, for example that it's someone from the family. The near-giveaway could then move to hint 3.
- **q-16018** (holidays-through-the-year) Kinder singen „Ich geh mit meiner Laterne und meine Laterne mit mir“. Zu welcher Art Lieder gehört es? → Martinslieder: None of the image candidates fits: #1 is a Hong Kong Mid-Autumn bunny lantern display (wrong culture and setting), #2 is an Indian classical singer on a Diwali stage, #3 is Ramadan calligraphy. The text itself is fine; the slot needs a new search such as "Sankt Martin Laternenumzug" or "children lantern procession". No suitable picture found for this question.
- **q-16043** (national-team) Das Wort steckt im Autokorso nach Deutschlandsiegen und im Blumenkorso, es stammt aus dem Italienischen. Was bedeutet „Korso“? → Festlicher Umzug: None of the pictures fits a question about a car parade or the word „Korso“: they show a Rangers flag in a house window, an old army football match, the Danish team bus and England flags at a school. Another search isn't allowed. A new search like „Autokorso Deutschland“ or „flower parade float“ should find something usable. No suitable picture found for this question.
- **q-16054** (pop-and-rock) Die Leipziger Band Die Prinzen sang „Ich wär so gerne Millionär“. In welchem Jahrzehnt wurde das Lied ein Hit? → 1990er: Hint 2 says the first „Bravo Hits“ CD came out in the same decade. That gives away the answer to approved question q-12163 (same subcategory), so whichever of the two is played first spoils the other. Replace hint 2 with a decade clue that doesn't depend on another pool question, for example one about German reunification shortly before the song came out.
- **q-16059** (pop-and-rock) Welcher dieser Hits ist NICHT von Wincent Weiss? → „Lieblingsmensch“: Hint 2 („Liebeslied über den Menschen, der einem am meisten bedeutet“) just paraphrases the title „Lieblingsmensch“, so it gives the answer away before hint 3. It should become a vague hint that doesn't describe the title, for example the release year (2015) or that it was a debut hit. The facts are correct: „Musik sein“, „Feuerwerk“ and „Frische Luft“ are Wincent Weiss songs, „Lieblingsmensch“ is by Namika, and Weiss was on DSDS in 2013.
- **q-16086** (athletes-and-other-sports) Zehnkämpfer Leo Neugebauer stellte 2024 einen deutschen Rekord auf. Wie viele Punkte waren das ungefähr? → Rund 9000: The fun fact is wrong: Neugebauer set the German record of 8961 points in June 2024 at the NCAA Championships in Eugene, not at the Paris Olympics. In Paris he won silver with about 8748 points, which was not a record. Correct the fun fact, e.g. „Im Juni 2024 steigerte Neugebauer in Eugene (USA) seinen eigenen deutschen Rekord auf 8961 Punkte; bei Olympia in Paris gewann er Silber.“ Fact check: wrong. The fun fact is false. Neugebauer's German record of 8961 points came in June 2024 at the NCAA Championships in Eugene, not at the Paris Olympics. In Paris he won silver with about 8748 points, which was not a German record.
- **q-16104** (empire-weimar-and-nazi-era) Hinter welchem Plan der deutschen Wehrmacht von 1940 verbarg sich der Deckname „Unternehmen Seelöwe“? → Eine Landung in England: The picked picture has an unsuitable licence (pd-us-only: PD-US-not renewed).
- **q-16111** (federal-republic-and-reunification) Dieser Umriss zeigt das Bundesland, in dem Franz Beckenbauer geboren wurde. Welches Bundesland ist das? → Bayern: No media candidates were found for the essential outline of Bavaria, and another search isn't allowed. The question can't be played without an unlabelled outline map of Bayern. Source one by hand (for example a blank locator or outline map from Commons) or turn the question into one that doesn't need essential media. No suitable picture found for this question.
- **q-16147** (shows-and-presenters) In welchem Jahr lief die erste Staffel von „Let's Dance“ bei RTL? → 2006: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-16152** (shows-and-presenters) Ich komme aus Düsseldorf, habe polnische Wurzeln und wurde Anfang der 2010er mit Beauty- und Lifestylevideos auf YouTube berühmt. Wer bin ich? → Dagi Bee: The fact check is 'uncertain', and I can't confirm the fun fact's claim that Dagi Bee had fans join her 2018 wedding to Eugen by video either. Replace the fun fact with a verified one. Also confirm the Polish roots in the question text; I'm fairly sure she has them, but the fact check couldn't verify it. Fact check: uncertain. Düsseldorf, 2012 channel start and 2018 wedding to Eugen check out. I could not confirm the Polish roots (only the maiden name Ochmanczyk hints at it). I also could not confirm that fans joined the wedding by video.
- **q-16157** (shows-and-presenters) Bei „Schlag den Raab“ bringt Spiel 1 einen Punkt, Spiel 2 zwei, Spiel 3 drei und so weiter. Wie viele Punkte gibt es bei 15 Spielen insgesamt? → 120: The text is fine (1 + … + 15 = 120 is correct, and the escalating points rule of Schlag den Raab is right), but none of the decorative candidates shows a TV studio or game-show setting. No new search is allowed, so the slot needs a TV studio or game-show stage image found by hand (e.g. 'game show studio set'). No suitable picture found for this question.
- **q-16164** (state-and-city-emblems) Dieses Abzeichen mit einem Landeswappen in der Mitte sitzt auf Uniformmützen in Deutschland. Wie heißt es? → Polizeistern: None of the media candidates works. All six show Nazi-era or Norwegian NS police and party eagles, several with swastikas. That is the wrong subject and not family-friendly, and no new search is allowed. The essential image needs a photo of a modern German Polizeistern on a cap, with no „Polizei“ lettering visible. A search like "Polizeistern Mütze" on Commons might find one. No suitable picture found for this question.
- **q-16167** (state-and-city-emblems) Das ist das kleine Landeswappen von Baden-Württemberg. Wie viele Löwen siehst du darauf? → 3: No candidate shows the lesser coat of arms of Baden-Württemberg on its own, and the question can't work without that picture. Candidate 1 is a map of Germany with all the state arms as tiny icons, and 2–6 are arms of other countries. A new search is not allowed, so the slot needs a file such as "Coat of arms of Baden-Württemberg (lesser).svg" from Commons. No suitable picture found for this question.

## Question axes

- move: analogy 3, cause_effect 14, count 6, estimate 11, identify 28, made_of 11, name_concept 33, odd_one_out 20, origin 13, purpose 21, record 7, sequence 17, when 29, who 26, word_meaning 25
- stimulus: detail 6, map_outline 1, none 232, photo 24, video 1
- clue: completion 5, direct 112, riddle 31, scenario 38, three_facts 78
- answer_kind: group 31, number 21, person 38, place 22, thing 56, time 30, word 66
- lens: body_senses 3, educational_media 37, everyday 44, history 59, language 43, nature 4, pop_culture 29, popular_science 2, school 26, science_news 2, university 15

## Dropped by the pipeline

- art-architecture-and-museums-6: overlap like q-9474: Der Rheinturm ist rund 240 Meter hoch, steht neben dem Landtag und zeigt mit Lichtern die Uhrzeit an. In welcher Stadt steht er? → Düsseldorf: Wozu wurde dieser Turm am Düsseldorfer Rheinufer ursprünglich gebaut? → Für Funk und Fernsehen
- athletes-and-other-sports-2: overlap like q-10973: Rudolf Caracciola fuhr in den 1930ern Silberpfeile für Mercedes. Welchen Spitznamen trug er, weil er bei bestimmtem Wetter fast unschlagbar war? → Regenmeister: Wie nannte man solche deutschen Rennwagen aus den 1930er-Jahren? → Silberpfeile
- athletes-and-other-sports-13: overlap like q-9169: Garmisch-Partenkirchen an der Zugspitze hat jedes Jahr an Neujahr ein Skispringen. Zu welcher Serie gehört es? → Vierschanzentournee: Hier waren 1936 Olympische Winterspiele, an Neujahr springen hier Skispringer, und Slalomstar Felix Neureuther wuchs hier auf. Welcher Ort? → Garmisch-Partenkirchen
- brands-and-products-3: overlap like q-9264: Viele sagen „Tesa“ statt Klebefilm – eine Marke wurde zum Alltagswort. Welches dieser Wörter ist dagegen KEIN Markenname? → Pflaster: Die Marke stammt von Beiersdorf aus Hamburg, und ihr Name kommt von der Büroangestellten Elsa Tesmer. Was ist Tesa? → Klebeband
- brands-and-products-4: overlap like q-13014: Diese Frau fuhr 1888 mit dem Motorwagen ihres Mannes von Mannheim nach Pforzheim, die erste lange Autofahrt. Wer ist sie? → Bertha Benz: Carl Benz meldete dieses Gefährt 1886 zum Patent an. Was war es? → Ein Auto
- brands-and-products-10: overlap like q-6256: Milka chocolate comes in purple wrappers with a purple cow. Its name joins the German words for milk and which other ingredient? → Cocoa: Ich stehe auf einer Alpenwiese, trage eine Glocke und habe ein Fell in einer ganz besonderen Farbe. Wer bin ich? → Die Milka-Kuh
- chancellors-and-presidents-0: overlap like q-13060: In welchem Jahr wurde mit Angela Merkel zum ersten Mal eine Frau deutsche Bundeskanzlerin? → 2005: Ihr Spitzname war „Mutti“: Wer regierte als erste Frau Deutschland als Bundeskanzlerin? → Angela Merkel
- chancellors-and-presidents-1: overlap like q-10945: Du siehst eine Wiederholung: Deutschland schlägt im WM-Halbfinale Gastgeber Brasilien mit 7:1. In welchem Jahr war das? → 2014: WM 2014: Deutschland gewann im Halbfinale 7:1, so hoch wie noch nie ein Team in einem WM-Halbfinale. Gegen wen? → Brasilien
- chancellors-and-presidents-6: overlap like q-11999: 2021 begann die Ampel-Koalition aus SPD, Grünen und FDP. In welchem Jahr zerbrach sie, als Kanzler Scholz FDP-Finanzminister Lindner entließ? → 2024: SPD, FDP und Grüne regierten ab 2021 zusammen. Warum nannte man das Bündnis „Ampel“? → Wegen der Parteifarben Rot, Gelb und Grün
- childrens-tv-and-audio-dramas-4: overlap like q-10851: Ein Mädchen namens George, das lieber ein Junge wäre, ihr Hund Timmy und die Felseninsel Kirrin: Zu welcher Bande gehören sie? → Fünf Freunde: Ich belle bei Gefahr, buddele gern und begleite George, Julian, Dick und Anne bei jedem Abenteuer. Wer bin ich? → Timmy
- cities-and-towns-17: duplicate like q-12210: In welcher Stadt steht dieser Turm? → München: Diese Wurst isst man mit süßem Senf und Brezel. Aus welcher Stadt stammt sie? → München
- dialects-and-regional-words-10: overlap like q-9338: Das Gericht auf dem Foto heißt fast überall anders. Wo sagt man vor allem „Reibekuchen“ dazu? → Rheinland: An einer Imbissbude im Rheinland: Welches dieser Wörter meint KEINE frittierten Kartoffelstäbchen? → Reibekuchen
- dialects-and-regional-words-16: overlap like q-13162: In der Pfalz kocht man daraus „Grumbeersupp“, im Saarland „Dibbelabbes“. Was ist eine „Grumbeere“? → Kartoffel: In Teilen Süddeutschlands heißt es „Erdapfel“. Es wächst unter der Erde, hat „Augen“, und Franzosen sagen ähnlich „pomme de terre“. Was ist es? → Kartoffel
- drinks-1: duplicate like q-9280: Dieses Fossil ist ein Archaeopteryx. In welchem Bundesland wurden alle bekannten Exemplare gefunden? → Bayern: Dieses trübe Bier im hohen, schlanken Glas ist ein Weißbier. Aus welchem Bundesland stammt es traditionell? → Bayern
- empire-weimar-and-nazi-era-1: overlap like q-5530: In June 1914, the heir to Austria-Hungary's throne was shot while riding through a city in an open car. A month later, World War I began. Which city? → Sarajevo: Dieser Mann war Thronfolger von Österreich-Ungarn. Seine Ermordung am 28. Juni 1914 in Sarajevo löste den Ersten Weltkrieg aus. Wer war er? → Franz Ferdinand
- empire-weimar-and-nazi-era-4: overlap like q-14976: Deutschlands erste Demokratie begann 1918, hatte Friedrich Ebert als ersten Präsidenten und endete 1933. Wie nennt man sie? → Weimarer Republik: Dieser Sozialdemokrat war von 1919 bis 1925 der erste Reichspräsident der Weimarer Republik. Wer war er? → Friedrich Ebert
- empire-weimar-and-nazi-era-14: overlap like q-1266: Mira este detalle de un castillo alemán de cuento. ¿Qué rey, apodado 'el Rey Cisne', lo mandó construir? → Luis II de Baviera: Du stehst vor Schloss Neuschwanstein. Welcher König ließ es bauen? → Ludwig II.
- family-customs-and-dress-1: overlap like q-14865: In musical chairs, players circle the chairs while the music plays. What changes after each round? → One chair is taken away: Auf dem Kindergeburtstag heißt es: „Wir spielen Reise nach Jerusalem!“ Was braucht man dafür? → Stühle und Musik
- family-customs-and-dress-11: overlap like q-12089: Was gehört in Deutschland in die braune Tonne? → Obst- und Gemüsereste: In mich kommen Bananenschalen, Eierschalen und Kaffeesatz, und im Sommer rieche ich ganz schön streng. Welche Tonne bin ich? → Biotonne
- federal-republic-and-reunification-4: overlap like q-14125: Trabant ist zu Pkw wie Barkas B 1000 zu …? → Kleintransporter: In der DDR wartete man oft über zehn Jahre darauf, er knatterte laut und hatte eine Hülle aus Kunststoff. Wofür war der Trabant da? → Zum Autofahren
- federal-republic-and-reunification-9: overlap like q-10939: Nach wie vielen Jahren wird der Bundestag regulär neu gewählt? → 4: Alle wie viele Jahre wird normalerweise der Bundestag gewählt? → 4
- federal-republic-and-reunification-15: overlap like q-13165: Ich sende seit 1963, und zwischen meinen Werbespots zeigen sich kleine Männchen mit Zipfelmützen. Wer bin ich? → ZDF: Du schaust am frühen Abend ZDF. Wann tauchen dort die Mainzelmännchen auf? → Zwischen den Werbespots
- films-and-actors-8: overlap like q-10885: Dieser Mann drehte „(T)Raumschiff Surprise – Periode 1“ und spielte darin selbst mit. Wer ist es? → Michael Herbig: Dieser Mann auf dem Foto drehte „Der Schuh des Manitu“ und „Wickie und die starken Männer“. Wer ist es? → Michael „Bully“ Herbig
- films-and-actors-14: overlap like q-12044: Er zeichnete Männchen mit Knollennasen, erfand die Steinlaus und ließ Opa Hoppenstedt „Früher war mehr Lametta“ sagen. Wie lautet sein Künstlername? → Loriot: Bei Loriot meckert Opa Hoppenstedt über das Weihnachtsfest von heute. Wie endet sein Satz „Früher war mehr …“? → Lametta
- gdr-everyday-life-7: overlap like q-15039: Du lebst 1985 in Dresden und deine Antenne empfängt kein Westfernsehen. Wie nannte man die Gegend deshalb im Spott? → Tal der Ahnungslosen: Weil sie sehr weit von den Westsendern entfernt lag, bekam neben dem Raum Dresden noch eine Gegend der DDR kaum Westfernsehen. Welche? → Die Gegend um Greifswald
- gdr-everyday-life-16: overlap like q-12066: „Ich hatte zehn Klassen, fast alle Kinder der DDR gingen zu mir, und ab Klasse 7 schickte ich sie regelmäßig in echte Betriebe.“ Wer bin ich? → Die Polytechnische Oberschule: Ab der 7. Klasse stand bei DDR-Schülern einmal pro Woche „UTP“ im Stundenplan. Was machten sie da? → In einem Betrieb mitarbeiten
- holidays-through-the-year-1: overlap like q-9129: Am 6. Dezember kommt der Nikolaus. Wie viele Türchen am Adventskalender sind dann schon offen? → 6: Ich trage einen roten Bischofsmantel, eine hohe Mütze und einen goldenen Stab. Mein Festtag ist der 6. Dezember. Wer bin ich? → Nikolaus
- holidays-through-the-year-16: overlap like q-9256: Ich wollte nicht Bischof werden und versteckte mich in einem Stall, doch schnatternde Gänse verrieten mich. Wer bin ich? → Sankt Martin: Im Herbst brennt in vielen Orten so ein großes Feuer, und Kinder kommen mit Laternen. Zu Ehren welches Heiligen? → Sankt Martin
- inventors-and-scientists-0: overlap like q-4910: Ulm Minster in Germany has a church tower 161.5 m (530 ft) tall with 768 steps. Which famous scientist was born in the same city? → Albert Einstein: Ich kam 1879 in Ulm zur Welt, schrieb die Formel E = mc² auf und streckte auf einem berühmten Foto die Zunge heraus. Wer bin ich? → Albert Einstein
- inventors-and-scientists-14: overlap like q-2863: At a concert, loudness is to decibel as pitch is to… → Hertz: Die Einheit Hertz ist nach einem Hamburger Physiker benannt und steht auf Radiosendern (MHz) und Bildschirmen (Hz). Was gibt sie an? → Wie oft etwas pro Sekunde schwingt
- inventors-and-scientists-16: overlap like q-5836: In 1922, Hans Riegel of Haribo in Germany made one of the first gummy candies, shaped like an animal that danced at fairs back then. Which animal? → Bear: Hans Riegel erfand 1922 eine Fruchtgummi-Figur. Vorbild waren Tiere, die damals auf Jahrmärkten tanzten. Welche Süßigkeit ist das? → Gummibärchen
- mountains-and-landscapes-5: overlap like q-9295: Diese Gänge unter der Rinde einer Fichte hat ein Tier gefressen. Welches? → Borkenkäfer: Er ist nur Millimeter groß, frisst unter der Rinde von Fichten und ließ im Nationalpark Bayerischer Wald ganze Hänge absterben. Wer ist es? → Borkenkäfer
- mountains-and-landscapes-12: overlap like q-6479: The föhn is a warm, dry wind that rushes down mountain slopes. In which mountain range did it get its name? → The Alps: Dieser warme, trockene Fallwind weht von den Alpen nach Bayern, bringt klare Fernsicht und manchen Kopfweh. Wie heißt er? → Föhn
- national-symbols-and-state-9: overlap like q-13047: Diese Blätter sind auf den deutschen 1-, 2- und 5-Cent-Münzen zu sehen. Von welchem Baum stammen sie? → Eiche: Auf dem alten Pfennig war ein junger Baum zu sehen. Auf den deutschen 1-, 2- und 5-Cent-Münzen ist heute ein Zweig. Von welchem Baum? → Eiche
- national-symbols-and-state-11: overlap like q-15013: Diese gläserne Kuppel sitzt seit 1999 auf dem Reichstagsgebäude in Berlin. Welcher Architekt hat sie entworfen? → Norman Foster: Ich bin ein britischer Architekt. In den 1990ern baute ich im Berliner Regierungsviertel den Reichstag um und gab ihm eine begehbare Glaskuppel. Wer bin ich? → Norman Foster
- national-symbols-and-state-17: overlap like q-9401: Bis 2011 leisteten viele junge Männer Zivildienst, oft im Krankenhaus oder Altenheim. Was war das? → Ersatz für den Wehrdienst: Bis 2011 bekamen sie mit 18 Post, mussten zur Musterung und danach zur Bundeswehr oder zum Zivildienst. Wer? → Junge Männer
- national-team-4: overlap like q-15281: Mira la foto: ¿quién lleva en el brazo una cinta como esta durante un partido de fútbol? → El capitán: Ich trage eine Binde am Oberarm, lose vor dem Anpfiff mit dem Schiri die Seiten aus und hob 2014 in Rio als Erster den WM-Pokal hoch. Wer bin ich? → Der Kapitän
- parks-weather-and-climate-4: overlap like q-9485: Was sagt die alte Bauernregel „Grüne Weihnachten, weiße Ostern“ voraus? → Kein Schnee an Weihnachten, dafür Schnee zu Ostern: Alte, oft gereimte Sprüche vom Land sagen das Wetter voraus, etwa: „Kräht der Hahn auf dem Mist …“ Wie heißen solche Sprüche? → Bauernregeln
- parks-weather-and-climate-11: overlap like q-9300: Das Tier, das diesen Baum so angenagt hat, war in Deutschland fast ausgerottet. Zu welcher Tiergruppe gehört es? → Nagetiere: Wer hat diesen Baumstamm am Flussufer so spitz angenagt? → Biber
- pop-and-rock-0: overlap like q-14090: Wer saß bei „Deutschland sucht den Superstar“ seit 2002 in den meisten Staffeln in der Jury? → Dieter Bohlen: Wir sangen 1984 „You're My Heart, You're My Soul“. Einer von uns trug eine „Nora“-Kette, der andere saß später bei DSDS. Wer sind wir? → Modern Talking
- reformation-to-empire-3: overlap like q-9363: Ich kam 1770 in einem Haus in der Bonngasse in Bonn zur Welt. Heute ist es ein Museum über mich. Wer bin ich? → Ludwig van Beethoven: Ich wurde am Rhein geboren und zog später nach Wien. Meine Fünfte Sinfonie beginnt mit vier Tönen: „Ta-ta-ta-taaa“. Wer bin ich? → Ludwig van Beethoven
- reformation-to-empire-8: overlap like q-9260: Du kommst am ersten Schultag mit deiner Schultüte. Was steckt traditionell darin? → Süßigkeiten und Schulsachen: Sie ist spitz, oft selbst gebastelt und voller Süßigkeiten und Stifte. Kinder in Deutschland tragen sie an einem großen Tag stolz im Arm. Was ist das? → Schultüte
- reformation-to-empire-14: overlap like q-14001: Früher trug mich der Spaßmacher am Königshof. Ich habe bunte Zipfel, und an jedem klingelt ein Glöckchen. Was bin ich? → Narrenkappe: Er trug eine Kappe mit Glöckchen, machte Späße und durfte dem Fürsten sogar frech die Wahrheit sagen. Wozu hielt man einen Hofnarren? → Zur Unterhaltung des Hofes
- reformation-to-empire-16: overlap like q-12186: Ich wurde in England gebaut und dampfte am 7. Dezember 1835 von Nürnberg nach Fürth, als erste Lok Deutschlands. Wie heiße ich? → Adler: Du sitzt im ICE. Was zog 1835 den allerersten deutschen Zug von Nürnberg nach Fürth? → Eine Dampflokomotive
- athletes-and-other-sports-7: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: In welchem Jahrzehnt wurde der Nürburgring in der Eifel mit seiner kurvigen Nordschleife eröffnet? → 1920er
- brands-and-products-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Wie viele Ringe hat das Logo des Autoherstellers Audi? → 4
- chancellors-and-presidents-12: fact-check wrong: The question is ambiguous. The AfD (and the BSW, which has never been in the Bundestag) has also never provided a Vizekanzler. Hint 2 ('always in opposition in the Bundestag') fits the AfD too. Linke is the only correct choice among the options.: Welche Partei stellte bisher noch NIE den deutschen Vizekanzler? → Linke
- dialects-and-regional-words-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ich bin ein Wort aus dem Süden, lobe Menschen in Dirndl und Lederhose und stamme vom englischen „fashionable“ ab. Welches Wort bin ich? → fesch
- drinks-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Viele Läufer trinken es gern nach dem Marathon. Woraus wird alkoholfreies Bier gemacht? → Malz, Hopfen, Wasser und Hefe
- family-customs-and-dress-2: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 4: Was ist in Spanien die „Siesta“? → Ein Mittagsschlaf
- federal-republic-and-reunification-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Bayern, Bremen und Sachsen sind Bundesländer. Was bedeutet das Wort „Bundesland“? → Ein Teil Deutschlands mit eigener Regierung
- federal-republic-and-reunification-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: „Ich bin rund, mein Motor sitzt hinten, und ich war das Auto des Wirtschaftswunders.“ Wer bin ich? → VW Käfer
- federal-republic-and-reunification-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Der Grüne Punkt steht seit 1991 auf vielen Verpackungen. Wie viele Pfeile hat dieses Zeichen? → 2
- films-and-actors-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Welcher deutsche Medienpreis wird schon seit 1948 verliehen und ist damit einer der ältesten des Landes? → Bambi
- films-and-actors-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Der Kölner Udo Kier spielte in von Andy Warhol produzierten Filmen Frankenstein und Dracula. In welchem Jahrzehnt? → 1970er
- gdr-everyday-life-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Der DDR-Jugendsender DT64 begann als Sonderprogramm für ein großes Jugendtreffen im Jahr 1964. In welcher Stadt fand dieses Treffen statt? → Ost-Berlin
- gdr-everyday-life-12: hard fail: correct 4, unambiguous 3, no_giveaway 3, no_overlap 5: „Ich bin hart und abwaschbar, oft bunt oder in Holzoptik. Aus Papier und Harz gepresst, decke ich in der DDR Küchentische und Möbel ab.“ Was bin ich? → Sprelacart
- gdr-history-6: overlap like q-12084: Er leitete über 30 Jahre die HVA, die Auslandsspionage der Stasi, und galt im Westen lange als „Mann ohne Gesicht“. Wer ist er? → Markus Wolf: Sie wurden in den Westen geschickt, lebten unter falschem Namen und arbeiteten für Markus Wolfs HVA. Was waren die „Romeos“? → Agenten, die Sekretärinnen in Bonn umwarben
- mountains-and-landscapes-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Das Sauerland in Nordrhein-Westfalen ist ein beliebtes Wandergebiet. Welchen Beinamen trägt es? → „Land der tausend Berge“
- mountains-and-landscapes-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: Laut einer Sage entstand das Felsenmeer im Odenwald, weil sich zwei Gestalten mit Felsbrocken bewarfen. Wer waren sie? → Zwei Riesen
- national-symbols-and-state-4: overlap like q-9474: Der Rheinturm ist rund 240 Meter hoch, steht neben dem Landtag und zeigt mit Lichtern die Uhrzeit an. In welcher Stadt steht er? → Düsseldorf: Alle fünf Jahre wählt Nordrhein-Westfalen seinen Landtag. Das Gebäude steht direkt am Rhein – in welcher Stadt? → Düsseldorf
- national-symbols-and-state-8: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 4: Studenten schwenkten mich 1832 auf dem Hambacher Fest, heute wehe ich auf dem Reichstag in Berlin. Was bin ich? → Bundesflagge
- parks-weather-and-climate-8: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Wie heißt die milde Wetterphase Ende Dezember, die in Deutschland oft den Schnee schmelzen lässt? → Weihnachtstauwetter
- shows-and-presenters-16: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In der ZDF-Musikshow „Disco“ rief Ilja Richter vor den Stargästen einen Kultspruch. Wie lautete er? → „Licht aus – Spot an!“
- slang-and-everyday-words-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Das Wort klingt englisch, doch in England sagt man zu dem Gerät „mobile phone“. Wie heißt es bei uns? → Handy
- sayings-and-idioms-10: overlap like q-10992: Ich stickte „Sieben auf einen Streich“ auf meinen Gürtel – dabei hatte ich nur Fliegen erschlagen. Wer bin ich? → Tapferes Schneiderlein: „Zwei Fliegen mit einer Klappe“ ist nichts gegen diesen Märchenhelden: Er erschlägt sieben auf einen Streich. Wer ist es? → Das tapfere Schneiderlein
- sayings-and-idioms-13: overlap like q-13039: Wer tanzt im Märchen ums Feuer und singt: „Ach, wie gut, dass niemand weiß …“? → Rumpelstilzchen: Ich spinne Stroh zu Gold, tanze nachts ums Feuer und singe: „Ach, wie gut, dass niemand weiß …“ Wer bin ich? → Rumpelstilzchen
- sayings-and-idioms-16: overlap like q-9222: Eine schwarze Katze läuft dir über den Weg. Was bringt das nach altem Aberglauben? → Pech: Zu Silvester verschenkt man in Deutschland gern Glücksbringer wie den Schornsteinfeger. Was gehört NICHT dazu? → Schwarze Katze
- slang-and-everyday-words-11: overlap like q-1172: Mira la foto: en inglés a este aparato le dicen 'laptop'. Según ese nombre, ¿dónde se pensó para usarlo? → Sobre las piernas: Das Gerät lässt sich zuklappen, läuft mit Akku, und sein englischer Name verrät, wo es liegen soll. Wo? → Auf dem Schoß
- state-and-city-emblems-0: overlap like q-12184: Frankreich ist zu Blau-Weiß-Rot wie Deutschland zu …? → Schwarz-Rot-Gold: Dieser Streifen gehört zur deutschen Flagge. Wie heißt seine Farbe offiziell? → Gold
- state-and-city-emblems-4: overlap like q-9157: In diesem Gebäude wählen die Abgeordneten den Bundeskanzler. Welches ist es? → Reichstagsgebäude: Unter dieser gläsernen Kuppel liegt der Plenarsaal, in dem der Bundestag tagt. In welchem Gebäude ist das? → Reichstagsgebäude
- state-and-city-emblems-11: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Das ist das Wappen der Stadt Rosenheim. Welche Blume ist darauf zu sehen? → Rose
- state-and-city-emblems-17: overlap like q-12034: „Etwas im Schilde führen“ kommt von den Wappen, die Ritter auf ihre Schilde malten. Seit wann taten sie das? → 12. Jahrhundert: Solche bemalten Schilde mit Wappen trug man im Mittelalter in den Kampf. Wer trug sie? → Ritter
