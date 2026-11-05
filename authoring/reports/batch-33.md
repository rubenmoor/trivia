# batch-33

Made by `qgen batch` on 2026-11-05 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): pop-and-rock, rap-and-electronic, childrens-and-folk-songs, classic-literature, childrens-books-and-comics, art-architecture-and-museums, series-and-crime, childrens-tv-and-audio-dramas, shows-and-presenters, films-and-actors, bundesliga-and-clubs, national-team, athletes-and-other-sports, winter-sports, dialects-and-regional-words, sayings-and-idioms, slang-and-everyday-words, brands-and-products, money-and-shopping, school-and-education, transport, home-and-public-life, national-symbols-and-state, state-and-city-emblems, gdr-history, gdr-everyday-life, rivers-lakes-and-coasts
- Merged: 321 (q-10798…q-11118)
- Approved: 295
- Needs work: 26
- Dropped by the pipeline: 54
- Reviewed by: claude-opus-5-5
- Claude calls: 651, about $83.74 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-31, batch-32; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-31 | batch-32 | batch-33 |
|---|---|---:|---:|---:|
| source locale |  | es | en | de |
| drafts |  | 427 | 367 | 375 |
| skipped slots |  | 95 | 83 | 111 |
| dropped |  | 85 | 60 | 54 |
| drop rate | ≤ 20.0 % | 19.9 % ✓ | 16.3 % ✓ | 14.4 % ✓ |
| dropped: hard fail correct |  | 2 | 1 | 8 |
| dropped: hard fail unambiguous |  | 3 | 0 | 3 |
| dropped: hard fail no_giveaway |  | 23 | 17 | 28 |
| dropped: overlap |  | 55 | 41 | 19 |
| dropped: duplicate |  | 1 | 0 | 0 |
| dropped: fact-check wrong |  | 1 | 1 | 1 |
| merged |  | 342 | 307 | 321 |
| approved |  | 318 | 281 | 295 |
| needs_work |  | 24 | 26 | 26 |
| needs_work rate | ≤ 20.0 % | 7.0 % ✓ | 8.5 % ✓ | 8.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.0 % ✓ | 2.9 % ✓ | 1.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.9 % ✓ | 0.3 % ✓ | 0.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 1.6 % ✗ |
| needs_work: media | ≤ 10.0 % | 4.1 % ✓ | 5.5 % ✓ | 3.7 % ✓ |
| media: no pick in review 1 |  | 63 | 38 | 45 |
| media: recovered by research |  | 53 | 25 | 39 |
| media: no pick at record |  | 11 | 14 | 6 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 13.1 % ✓ | 11.4 % ✓ | 6.4 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 69.4 % ✓ | 71.3 % ✓ | 72.8 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.56 ✗ | 2.29 ✗ | 1.55 ✗ |
| approved 11–15 |  | 61 | 59 | 67 |
| top move | ≤ 25.0 % | 16.7 % ✓ | 19.5 % ✓ | 17.4 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 80.4 % | 84.4 % | 92.5 % |
| values stimulus |  | 4 | 6 | 3 |
| top clue | ≤ 60.0 % | 43.0 % ✓ | 45.0 % ✓ | 37.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 27.8 % ✓ | 24.4 % ✓ | 27.4 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 17.0 % ✓ | 21.8 % ✓ | 20.9 % ✓ |
| values lens |  | 11 | 10 | 9 |
| media share | 15.0 %–50.0 % | 19.6 % ✓ | 15.6 % ✓ | 7.5 % ✗ |
| mean fun | ≥ 3.40 | 3.50 ✓ | 3.56 ✓ | 3.53 ✓ |
| cost $ |  | $86.59 | $73.13 | $80.73 |
| $ per approved | ≤ $0.35 | $0.27 ✓ | $0.26 ✓ | $0.27 ✓ |
| calls |  | 642 | 580 | 591 |
| calls per approved |  | 2.02 | 2.06 | 2.00 |
| wall time h |  | 2.98 | 2.60 | 3.06 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 55 (0 %)
- Major among review needs work: 0 of 5 (0 %)
- Problems by kind: giveaway 13 (0 major), fact 3 (0 major), ambiguity 1 (0 major), media 1 (0 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 55 of 60 (92 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.01

Major findings on approved questions:

None.

## Needs work

- **q-10813** (athletes-and-other-sports) Angelique Kerber gewann drei verschiedene Grand-Slam-Turniere. Welches fehlt ihr? → French Open: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-10842** (childrens-books-and-comics) Ich bin ein kleiner Stoffhase. Meine Freundin Sophie hat mich verloren, und nun schicke ich ihr Briefe aus aller Welt. Wer bin ich? → Felix: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-10873** (classic-literature) Du deckst bei Schneewittchens Zwergen den Tisch: Wie viele Tellerchen brauchst du für die Zwerge? → 7: This asks the same fact as approved q-1686 (how many dwarfs live with Snow White → 7), just reworded as a table-setting scene. Drop it, or replace it with a different Snow White or Grimm fact.
- **q-10884** (dialects-and-regional-words) Was ist das „Rheinische Grundgesetz“? → Humorvolle kölsche Lebensweisheiten: Overlaps q-10994: its question text says "Dieser Spruch steht im „Kölschen Grundgesetz“" and then asks about "Et kütt wie et kütt". Anyone who has seen it knows the Grundgesetz is a collection of Kölsch sayings, so this question is solved. Keep only one of them, or reword q-10994 so it doesn't name the Grundgesetz. Minor point: "Humorvolle" in the answer makes it stand out as the joke option.
- **q-10896** (gdr-everyday-life) „Ich nahm Altpapier, Flaschen und Gläser an, Pioniere brachten mir ganze Handwagen voll, und dafür gab es Pfennige.“ Wer bin ich? → SERO: Hint 2 ("Mein Name ist eine Abkürzung") gives the answer away. Of the four options, only SERO, written in capitals, looks like an abbreviation; Intershop, Konsum and Exquisit read as ordinary words. Replace hint 2 with a vague hint that doesn't rule out options, e.g. one about the people who brought the material (school classes, Pioneer collection drives).
- **q-10906** (gdr-history) Bauarbeiter an der Ost-Berliner Stalinallee streikten, bald protestierten Hunderttausende in der ganzen DDR. Was geschah dann? → Sowjetische Panzer rückten an: This overlaps q-10904, which asks for the year of the same uprising (17 June 1953). Hint 1 here says "Sommer 1953", which is q-10904's answer, and q-10904's wording about a popular uprising and a state of emergency points towards this question's answer. Keep one of the two, or make sure they never appear in the same game.
- **q-10926** (national-symbols-and-state) Es ist schwarz, hat rote Krallen und einen roten Schnabel und hängt groß im Bundestag. Welches Tier ist das deutsche Wappentier? → Adler: Related draft q-10935 says outright that the German national team's jersey shows "einem Adler", which gives away this question's answer (the Wappentier is the eagle). Either reword q-10935 so it doesn't name the eagle (e.g. "mit dem Bundeswappen und vier Sternen"), or drop one of the two. Otherwise this question is fine, and candidate 1 works as the image.
- **q-10931** (national-symbols-and-state) Welches Bauwerk ist auf dieser deutschen Cent-Münze zu sehen? → Brandenburger Tor: None of the candidates shows the German national side with the Brandenburger Tor. Candidates 1–5 all show the common European side (map of Europe with the value), and 6 is a 1-cent coin with a micro-origami boat. The essential image can't be filled, and no new search is allowed. A search like "German 50 cent coin Brandenburg Gate" or "Euro coin Germany national side" should find the right side. No suitable picture found for this question.
- **q-10943** (national-team) Du jubelst auf der Fanmeile: Deutschland ist Gastgeber einer Fußball-EM, das Finale steigt im Berliner Olympiastadion. Welches Jahr ist es? → 2024: This repeats an approved question. q-3459 (base, played in German too) opens with "The men's European soccer championship was played in Germany in 2024", which states this question's answer outright. A player who has seen q-3459 knows this one, so it can't be fixed without asking a different fact.
- **q-10970** (art-architecture-and-museums) Der Künstler hatte nie ein Nashorn gesehen, als er dieses 1515 nach einer Beschreibung als Holzschnitt schuf. Wer war es? → Albrecht Dürer: No candidate works for the essential image. Candidates 1 and 2 are Dürer's woodcut but show the 'AD' monogram and the '1515 RHINOCERVS' inscription, which give the answer away. Candidate 6 is Enea Vico's mirrored engraving copy with 'E.V.' initials, not the woodcut the question means. 3 and 4 are AI images and 5 is a bronze door in Pisa. The fix is a cropped version of 1 or 2 that leaves out the monogram and the top text. No suitable picture found for this question.
- **q-10975** (brands-and-products) Pattex gibt es seit Jahrzehnten, es gehört zu Henkel und liegt als Tube in vielen Werkzeugkästen. Wofür benutzt man es? → Zum Kleben: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-10980** (transport) Dieses Schild steht vor einer besonderen Stelle der Straße. Was kommt gleich? → Kreisverkehr: None of the media candidates fit. All five are pictures of St. Augustine (Botticelli's fresco, a feather mosaic, two Confessiones manuscript pages, Seghers' painting), not German traffic sign Zeichen 215. A new search isn't allowed, so the essential image has to be supplied by hand, e.g. Commons "File:Zeichen 215 - Kreisverkehr, StVO 2000.svg" or a photo of that sign. No suitable picture found for this question.
- **q-10984** (bundesliga-and-clubs) Manuel Neuer wurde 2014 Weltmeister und gilt als einer der Besten auf seiner Position. Auf welcher Position wurde er berühmt? → Torwart: Hint 2 ("Er trägt ein Trikot in einer anderen Farbe als seine Mitspieler") gives the answer away: only the goalkeeper wears a different-coloured shirt from his team, so it rules out all three wrong answers at once. Hint 2 needs a vaguer clue that doesn't point to only one position, for example something about his height or his gloves being part of the kit without saying why.
- **q-10994** (dialects-and-regional-words) Was bedeutet der kölsche Spruch „Et kütt wie et kütt“? → Es kommt, wie es kommt: Hint 2 gives the answer away: "kommen" is the only verb of movement among the four options (kühlen, klappen, kochen are not). The description ("Terminkalender dem Schicksal überlassen") also states the saying's actual meaning (fatalism), which rules out "kühlt" and "kocht" before any hint. Hint 2 needs to be vaguer, e.g. about the sound shift from Standard German. The description should joke about Cologne or the carnival without saying what the saying means.
- **q-10997** (dialects-and-regional-words) So isst man gern Keks oder Brötchen. In welchen Bundesländern sagt man dazu „ditschen“? → Sachsen und Thüringen: Hint 1 ("Die beiden Bundesländer liegen im Osten Deutschlands") gives the answer away: Sachsen und Thüringen is the only eastern pair among the options. Replace it with a vague hint that doesn't single out one option, for example one about the dialect region or something cultural.
- **q-11004** (gdr-everyday-life) Der Sänger und Schauspieler Dean Reed lebte ab den 1970er-Jahren in der DDR. Was stimmt über ihn NICHT? → Er gewann den Eurovision Song Contest.: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-11007** (gdr-history) In der DDR war für jedes Wohnviertel ein bestimmter Volkspolizist zuständig, der seine Leute genau kannte. Welchen Titel trug er? → Abschnittsbevollmächtigter: The fun fact overstates the Hausbuch rule. As far as I know, DDR citizens visiting a flat only had to be entered once they stayed longer than three days; visitors from abroad or West Germany had to be entered for any stay. "Jeder Übernachtungsgast" isn't accurate. The fun fact should say "Gäste, die länger als drei Tage blieben" or something equally careful. Everything else holds up.
- **q-11009** (home-and-public-life) Bis 2004 hieß die Agentur für Arbeit noch anders. Wie lautet der alte Name: „Arbeits…“? → Arbeitsamt: None of the media candidates fits. They show ferry ticket payment devices, Japanese railway ticket machines and Japanese shrine ticket booths, not a German job centre or the waiting-number dispenser of a government office. No new search is allowed, so the slot needs a different image, e.g. "Agentur für Arbeit building" or "office waiting number dispenser". No suitable picture found for this question.
- **q-11029** (series-and-crime) Das Sandmännchen kommt jeden Abend im Fernsehen. Was ist danach für viele Kinder dran? → Schlafenszeit: None of the media candidates shows anything related to the Sandmännchen or bedtime. They are an equestrian statue, a bishop statue, a pietà, a saint with a cross, Elisabeth of Hungary and a kneeling noblewoman. No new search is allowed. The slot needs a new image, for example the Sandmännchen figure (if there is a freely licensed photo) or a decorative bedtime scene such as "child bedroom night lamp". The question text itself is fine. No suitable picture found for this question.
- **q-11043** (rivers-lakes-and-coasts) Der badische Ingenieur Johann Gottfried Tulla ließ im 19. Jahrhundert den Oberrhein begradigen. Was war eine Folge? → Das Sumpffieber im Rheintal verschwand: Hint 2 („Den Menschen in den Dörfern am Fluss ging es danach gesundheitlich besser“) gives the answer away: only one of the four options is about health, so hint 2 already settles it. Hint 2 should point somewhere less direct, for example the drained wetlands or the new farmland, and leave the health angle to hint 3.
- **q-11061** (sayings-and-idioms) Wer nicht zur Sache kommt, schleicht laut Redewendung „wie die … um den heißen Brei“. Welches Tier? → Katze: The article "die" in the question („wie die … um den heißen Brei“) fits only the feminine options Katze and Maus, so Fuchs and Hund are ruled out by grammar alone. Either replace the two masculine distractors with feminine animals (e.g. Ziege, Ente) or rephrase so the article doesn't show, e.g. „Wer nicht zur Sache kommt, schleicht laut Redewendung wie welches Tier um den heißen Brei?“
- **q-11074** (series-and-crime) „Sturm der Liebe“ läuft seit 2005 fast jeden Werktag in der ARD. Wie viele Folgen gibt es inzwischen ungefähr? → über 4000: The picked picture has an unsuitable licence (pd-us-only: PD-1923, PD-US-expired).
- **q-11077** (series-and-crime) „Club der roten Bänder“ lief ab 2015 bei VOX und zeigt Jugendliche auf einer Kinderstation. Was war ihr Vorbild? → eine Serie aus Spanien: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-11089** (shows-and-presenters) Bruce Darnell, Laufstegtrainer und „Supertalent“-Juror, hat einen berühmten Spruch. Wie geht er weiter: „Drama, …!“? → Baby: The fun fact ("kam als US-Soldat nach Deutschland") is probably wrong: the fact check says he served as a US paratrooper and moved to Germany only after his service, where his stepfather was stationed. Change the fun fact to something safe, e.g. "Bruce Darnell diente als Fallschirmjäger in der US-Armee, bevor er in Deutschland als Model arbeitete." Fact check: uncertain. The saying "Drama, Baby!" is right. The fun fact is shaky. English Wikipedia says he served as a US paratrooper, then moved to Germany after his service, where his stepfather was stationed. So he did not clearly come to Germany as a soldier.
- **q-11110** (transport) Was zeigt dieses Schild an? → Haltestelle: No candidate works for the essential image. Candidate 1 is the right sign (Zeichen 224), but the panel above it says „Doppelhaltestelle“ and it lists bus lines, so it gives the answer away. Candidates 2–6 show the Parthian Empire (maps, reliefs, a necklace). A new search isn't possible, so the slot needs a clean Commons file of Zeichen 224 on its own, such as the StVO SVG. No suitable picture found for this question.
- **q-11115** (winter-sports) Welches dieser Geräte für den Schneehang hat KEINE Kufen? → Poporutscher: The question only works among the four options: "Which of these has NO runners?" also fits lots of real snow gear outside the set (skis, snowboard, snow tube, a plastic bag). That breaks the rule that the clue must point to the answer in the real world. Rework it so the clue belongs only to the Poporutscher, e.g. "What is the small, flat plastic disc you sit on to slide down a snowy hill called?" Then change hints 2 and 3 so they don't repeat the clue.

## Question axes

- move: analogy 8, cause_effect 15, count 17, estimate 7, identify 48, made_of 5, name_concept 40, odd_one_out 21, origin 16, purpose 9, record 2, sequence 11, when 18, who 56, word_meaning 48
- stimulus: detail 7, none 297, photo 17
- clue: completion 20, direct 121, riddle 51, scenario 42, three_facts 87
- answer_kind: group 18, number 26, person 79, place 20, thing 71, time 19, word 88
- lens: body_senses 14, educational_media 30, everyday 60, history 55, language 46, nature 5, pop_culture 67, school 27, university 17

## Dropped by the pipeline

- brands-and-products-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Corsa, Astra und Mokka stammen alle von einer Firma aus Rüsselsheim, die einen Blitz als Zeichen hat. Was sind sie? → Automodelle
- brands-and-products-4: overlap like q-1397: Traduciendo marcas: 'Volkswagen' es a 'auto del pueblo' como 'Samsung', en coreano, es a… → Tres estrellas: Diese Firma aus Wolfsburg baut den Golf und den Bulli. Ihr Name heißt so viel wie „Auto für alle Leute“. Welche ist es? → Volkswagen
- brands-and-products-9: overlap like q-6256: Milka chocolate comes in purple wrappers with a purple cow. Its name joins the German words for milk and which other ingredient? → Cocoa: Sie ist lila, steht in der Werbung auf Alpenwiesen und trägt eine Glocke. Für welche Süßigkeit macht sie Werbung? → Schokolade
- bundesliga-and-clubs-6: overlap like q-0735: La hace todo el estadio a la vez: la gente se pone de pie y se vuelve a sentar por turnos. Se volvió famosa en el mundo gracias al Mundial de México 1986. ¿Qué es? → La ola: Sie rollt durchs ganze Stadion, Fans springen auf und reißen die Arme hoch. Ihr Name ist spanisch: „La Ola“. Was bedeutet das? → Welle
- bundesliga-and-clubs-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Der FC Bayern ist deutscher Rekordmeister: Kein Verein hat öfter die Meisterschaft gewonnen. In welcher Stadt ist er zu Hause? → München
- childrens-and-folk-songs-3: overlap like q-9259: Im Kindergarten basteln Kinder im Herbst Laternen. Wofür? → Für den Martinsumzug: Im November ziehen Kinder durch die dunklen Straßen und singen von Sonne, Mond und Sternen. Was tragen sie dabei leuchtend in der Hand? → Laternen
- childrens-and-folk-songs-12: overlap like q-0577: Adivina: 'En mí la historia se cuenta cantando, y Mozart me usó para La flauta mágica'. ¿Qué soy? → Una ópera: Bald nach der Melodie zu „Komm, lieber Mai, und mache“ schrieb ihr Komponist die Oper „Die Zauberflöte“. Wer war es? → Wolfgang Amadeus Mozart
- childrens-books-and-comics-10: overlap like q-9334: Ein Frankfurter Arzt schuf ein Kinderbuch mit dem Suppenkaspar, dem Zappelphilipp und Hans Guck-in-die-Luft. Wie heißt es? → Der Struwwelpeter: In welchem Kinderbuch kippelt der Zappelphilipp so lange, bis er samt Tischdecke und Essen zu Boden stürzt? → Struwwelpeter
- classic-literature-6: overlap like q-1839: Adivina: «Soy Pascal, un camaleón que vive en una torre con mi mejor amiga». ¿Quién es ella? → Rapunzel: Welche Märchenfigur ist auf diesem Bild zu sehen? → Rapunzel
- dialects-and-regional-words-3: overlap like q-9475: Wer nennt dieses Gebäck typischerweise „Brezn“? → jemand aus Bayern: „Des war a rechte Gaudi!“ – in welchem Bundesland hört man diesen Ausruf für einen Riesenspaß am häufigsten? → Bayern
- dialects-and-regional-words-11: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 4: „Tach“ ist ein geschrumpftes „Guten Tag“. Man hört es an der Trinkhalle und hörte es früher unter Tage im Bergwerk. Wo ist es typisch? → Ruhrgebiet
- films-and-actors-3: overlap like q-3699: Riddle: “People called me the most beautiful woman in the world. When Paris took me from Sparta, a great war began.” Who am I? → Helen: Ergänze: In „Troja“ (2004) an der Seite von Brad Pitt spielte Diane Kruger die schöne … → Helena
- films-and-actors-16: overlap like q-1235: Soy un perezoso torpe y parlanchín, y viajo con un mamut y un tigre dientes de sable. ¿Cómo me llamo? → Sid: Ich lebe in der Eiszeit, ziehe mit einem Mammut und einem Säbelzahntiger herum und spreche auf Deutsch mit Ottos Stimme. Wer bin ich? → Sid
- gdr-everyday-life-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Du wohnst im DDR-Winter in einem Altbau und trägst jeden Morgen Briketts aus dem Keller nach oben. Was heizt du damit? → Kohleofen
- gdr-everyday-life-11: overlap like q-9227: Seit 1948 zahlte man in Westdeutschland mit der D-Mark. Wo wurde sie am 1. Juli 1990 ebenfalls offizielles Geld? → DDR: Du tauschst am Bankschalter deine Ostmark um, weil die D-Mark ab dem 1. Juli offizielles Geld in der DDR wird. In welchem Jahr? → 1990
- money-and-shopping-0: overlap like q-2346: What are these instruments made of? → Metal: Woraus sind diese Münzen gemacht? → Metall
- pop-and-rock-0: overlap like q-10929: Bei diesem Zeremoniell zum Abschied von Angela Merkel 2021 erklang „Du hast den Farbfilm vergessen“. Wer sang das Original? → Nina Hagen: Nina Hagen sang 1974 „Du hast den Farbfilm vergessen“, ging 1976 in den Westen und wurde „Godmother of Punk“ genannt. Wo wurde sie geboren? → Ost-Berlin
- art-architecture-and-museums-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: Der Künstler schneidet alles weg, was weiß bleiben soll; nur die erhabenen Linien drucken. So entstanden schon um 1450 Buchbilder. Woraus ist der Druckstock? → Holz
- brands-and-products-14: hard fail: correct 4, unambiguous 3, no_giveaway 2, no_overlap 5: Mit dem Tiptoi-Stift tippst du auf Bilder, und sie fangen an zu sprechen. Wofür gibt es KEINE Tiptoi-Ausgabe? → Fernsehserien
- transport-5: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Auf diesem deutschen Verkehrsschild steht ein englisches Wort. Welches Schild ist es? → Stoppschild
- transport-6: hard fail: correct 2, unambiguous 4, no_giveaway 4, no_overlap 5: Du liest das hintere Nummernschild eines deutschen Autos von links. Was kommt direkt nach dem Ortskürzel, etwa „M“ für München? → Zwei runde Plaketten
- transport-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ich fahre ein gelbes Auto und komme, wenn dein Reifen auf der Autobahn platt ist. Dann helfe ich dir am Straßenrand weiter. Wer bin ich? → ADAC-Pannenhelfer
- winter-sports-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: 1908 baute ein Müller im Schwarzwald einen Lift, angetrieben vom Wasserrad seiner Mühle. Wen zog er den Hang hinauf? → Skifahrer
- childrens-tv-and-audio-dramas-4: overlap like q-9231: Welches Wort fehlt bei der „Sendung mit der Maus“: „Lach- und …geschichten“? → Sach: In welchem Jahr lief die erste Folge der „Lach- und Sachgeschichten“, aus denen „Die Sendung mit der Maus“ wurde? → 1971
- childrens-tv-and-audio-dramas-5: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Unter welchem Namen bündelt das ZDF seine Kindersendungen wie „logo!“ und „Löwenzahn“? → ZDFtivi
- dialects-and-regional-words-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Das Wort kommt aus Schwaben und hat die typische Verkleinerung „-le“ wie „Häusle“. Was ist ein „Mädle“? → Mädchen
- films-and-actors-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Roland Emmerich ließ in „Independence Day“ Aliens das Weiße Haus sprengen. In welcher deutschen Stadt wurde er geboren? → Stuttgart
- gdr-everyday-life-5: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Das Wort kommt aus dem Russischen, und in der DDR besaßen Millionen Familien eine. Was ist eine Datsche? → ein Gartenhaus
- gdr-everyday-life-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In der DDR nannte man es „Feierabendheim“. Wie heißt so eine Einrichtung heute meist? → Seniorenheim
- gdr-history-1: hard fail: correct 3, unambiguous 5, no_giveaway 3, no_overlap 5: In der DDR gab es über 300 „Kombinate“. Was war ein Kombinat? → Verbund von Industriebetrieben
- gdr-history-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ein Brief aus dem Westen kommt in der DDR geöffnet und wieder zugeklebt an. Wie nennt man, was die Stasi damit gemacht hat? → Postkontrolle
- home-and-public-life-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Wer wird von den Bürgern gewählt, arbeitet im Rathaus und trägt bei Festen oft eine Amtskette? → Bürgermeister
- home-and-public-life-8: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Früher wurde im Frühling das ganze Haus gründlich geputzt. Was hatte sich im Winter vor allem in den Wohnungen abgesetzt? → Ruß und Asche
- money-and-shopping-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Auf dem Weihnachtsmarkt zahlt man für die Glühweintasse extra und bekommt das Geld bei der Rückgabe wieder. Wie heißt so ein Becher? → Pfandbecher
- money-and-shopping-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Auf dem Joghurt steht ein Datum, nach dem er oft noch gut essbar ist. Wie heißt dieses Datum? → Mindesthaltbarkeitsdatum
- national-team-16: hard fail: correct 2, unambiguous 5, no_giveaway 4, no_overlap 5: Welcher Nationalspieler ist auf diesem Foto zu sehen? → Toni Kroos
- pop-and-rock-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ich war 2013 bei „DSDS“, wurde durch den Remix „Unter meiner Haut“ bekannt und sang danach „Musik sein“ und „Feuerwerk“. Wer bin ich? → Wincent Weiss
- pop-and-rock-14: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Thomas Anders von Modern Talking trug in den 1980ern bei Auftritten oft ein Schmuckstück mit dem Namen seiner damaligen Frau Nora. Welches? → Halskette
- rap-and-electronic-14: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Welches große Festival für elektronische Tanzmusik findet jedes Jahr in Neustadt-Glewe in Mecklenburg-Vorpommern statt? → Airbeat One
- rivers-lakes-and-coasts-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: An der Nordsee machen viele Urlauber eine „Wattwanderung“, meist barfuß und mit Führer. Was macht man dabei? → Bei Ebbe über den Meeresboden laufen
- school-and-education-7: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Im Kunstunterricht tauchst du den Pinsel ins Wasser und dann in kleine, feste Farbtöpfchen. Wie heißt der Kasten dazu? → Wasserfarbkasten
- school-and-education-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In vielen Grundschulen gibt es ihn in der 2. oder 3. Klasse, samt Urkunde. Was ist der „Füllerführerschein“? → Erlaubnis, mit Tinte zu schreiben
- school-and-education-17: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Du stehst im Schulmuseum vor einem alten Rohrstock. Bis in welches Jahrzehnt durften Lehrer in vielen westdeutschen Ländern damit strafen? → 1970er-Jahre
- series-and-crime-10: fact-check wrong: Stockl's catchphrase is in the subjunctive: 'Es gabat a Leich!' (Bavarian for 'there'd be a corpse'), not 'Es gibt a Leich'!'. The answer's spelling is inaccurate. Her departure from the show is also reported, so the fun fact may need a past-tense update.: In den „Rosenheim-Cops“ spielt Marisa Burger die Sekretärin Miriam Stockl. Mit welchem Satz kündigt sie jeden neuen Fall an? → „Es gibt a Leich'!“
- shows-and-presenters-9: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: Im „Aktuellen Sportstudio“ des ZDF schießen Gäste seit Jahrzehnten sechsmal auf eine Holzplatte mit zwei Löchern. Wie heißt das? → Torwandschießen
- state-and-city-emblems-3: hard fail: correct 2, unambiguous 5, no_giveaway 2, no_overlap 5: König Ludwig II. benannte sein berühmtestes Schloss in Bayern nach einem Tier. Nach welchem? → Schwan
- state-and-city-emblems-8: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: Wie heißt in der Wappenkunde die Fläche, auf die das eigentliche Wappenbild gemalt wird? → Schild
- school-and-education-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Viele Grundschulkinder haben für jedes Schulheft einen Heftumschlag. Was ist das? → Farbige Schutzhülle fürs Heft
- shows-and-presenters-10: overlap like q-3842: You're watching the longest-running cartoon series in US TV history, and the dad yells “D'oh!”. Which show is it? → The Simpsons: Wir sind eine Zeichentrickfamilie. Seit 2006 spricht Comedienne Anke Engelke unsere Mutter auf Deutsch. Wer sind wir? → Die Simpsons
- state-and-city-emblems-10: overlap like q-10926: Es ist schwarz, hat rote Krallen und einen roten Schnabel und hängt groß im Bundestag. Welches Tier ist das deutsche Wappentier? → Adler: Welches Tier ist auf der deutschen 1-Euro-Münze zu sehen? → Adler
- state-and-city-emblems-11: overlap like state-and-city-emblems-14: Welche Stadt an der Ostsee trägt dieses Wappentier sogar in ihrem Namen? → Greifswald: Die Herzöge von Pommern waren nach ihrem roten Wappentier benannt, das noch heute im Wappen von Mecklenburg-Vorpommern steht. Welches Wesen? → Greif
- state-and-city-emblems-14: overlap like state-and-city-emblems-11: Die Herzöge von Pommern waren nach ihrem roten Wappentier benannt, das noch heute im Wappen von Mecklenburg-Vorpommern steht. Welches Wesen? → Greif: Welche Stadt an der Ostsee trägt dieses Wappentier sogar in ihrem Namen? → Greifswald
- state-and-city-emblems-17: overlap like q-10935: Du siehst im Fernsehen Fußballer mit einem Adler und vier Sternen auf dem Trikot. Für wen spielen sie? → Deutsche Nationalmannschaft: Du siehst ein Trikot der deutschen Männer-Nationalmannschaft. Was ist über dem Adler auf der Brust zu sehen? → Sterne
- transport-3: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Du gehst an einer Autobahn-Raststätte durchs Drehkreuz von Sanifair und bekommst einen Bon. Wie viel ist er beim Einkauf wert? → 50 Cent
