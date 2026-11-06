# batch-37

Made by `qgen batch` on 2026-11-05 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): winter-sports, gdr-everyday-life, national-team, brands-and-products, films-and-actors, transport, pop-and-rock, inventors-and-scientists, state-and-city-emblems, cakes-and-sweets, shows-and-presenters, gdr-history, founders-and-entrepreneurs, home-and-public-life, schlager-and-folk-music, sights-and-landmarks, rap-and-electronic, bundesliga-and-clubs, art-architecture-and-museums, early-history, states-and-capitals, chancellors-and-presidents, federal-republic-and-reunification, athletes-and-other-sports, slang-and-everyday-words, childrens-books-and-comics, childrens-and-folk-songs
- Merged: 295 (q-11954…q-12248)
- Approved: 265
- Needs work: 30
- Dropped by the pipeline: 52
- Reviewed by: claude-opus-5-5
- Claude calls: 622, about $85.02 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-35, batch-36; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-35 | batch-36 | batch-37 |
|---|---|---:|---:|---:|
| source locale |  | es | en | de |
| drafts |  | 349 | 332 | 347 |
| skipped slots |  | 173 | 118 | 139 |
| dropped |  | 63 | 90 | 52 |
| drop rate | ≤ 20.0 % | 18.1 % ✓ | 27.1 % ✗ | 15.0 % ✓ |
| dropped: hard fail correct |  | 0 | 0 | 1 |
| dropped: hard fail unambiguous |  | 2 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 21 | 17 | 25 |
| dropped: overlap |  | 41 | 64 | 27 |
| dropped: duplicate |  | 0 | 7 | 0 |
| dropped: fact-check wrong |  | 0 | 2 | 0 |
| merged |  | 286 | 242 | 295 |
| approved |  | 263 | 216 | 265 |
| needs_work |  | 23 | 26 | 30 |
| needs_work rate | ≤ 20.0 % | 8.0 % ✓ | 10.7 % ✓ | 10.2 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.1 % ✓ | 3.3 % ✓ | 2.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.4 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.8 % ✓ | 1.7 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.8 % ✓ | 7.0 % ✓ | 5.1 % ✓ |
| media: no pick in review 1 |  | 45 | 34 | 33 |
| media: recovered by research |  | 38 | 25 | 22 |
| media: no pick at record |  | 8 | 10 | 12 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 12.3 % ✓ | 22.0 % ✗ | 9.2 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 45.9 % ✗ | 68.1 % ✓ | 65.3 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 0.82 ✓ | 2.00 ✗ | 1.25 ✓ |
| approved 11–15 |  | 45 | 54 | 62 |
| top move | ≤ 25.0 % | 19.9 % ✓ | 14.5 % ✓ | 14.9 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 95.1 % | 82.2 % | 79.3 % |
| values stimulus |  | 3 | 5 | 4 |
| top clue | ≤ 60.0 % | 36.4 % ✓ | 38.4 % ✓ | 44.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.5 % ✓ | 21.1 % ✓ | 20.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 23.4 % ✓ | 19.4 % ✓ | 18.3 % ✓ |
| values lens |  | 9 | 11 | 11 |
| media share | 15.0 %–50.0 % | 4.9 % ✗ | 17.8 % ✓ | 20.7 % ✓ |
| mean fun | ≥ 3.40 | 3.44 ✓ | 3.55 ✓ | 3.47 ✓ |
| cost $ |  | $75.28 | $64.45 | $81.47 |
| $ per approved | ≤ $0.35 | $0.29 ✓ | $0.30 ✓ | $0.31 ✓ |
| calls |  | 565 | 470 | 562 |
| calls per approved |  | 2.15 | 2.18 | 2.12 |
| wall time h |  | 2.80 | 1.99 | 2.31 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 54 (0 %)
- Major among review needs work: 4 of 6 (67 %)
- Problems by kind: giveaway 7 (2 major), fact 3 (0 major), overlap 3 (3 major), media 2 (1 major), difficulty 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.55

Major findings on approved questions:

None.

## Needs work

- **q-11974** (brands-and-products) Haba sitzt in Bad Rodach in Oberfranken, wurde 1938 gegründet und heißt nach der Familie Habermaaß. Was für eine Firma ist das? → Spielzeughersteller: Hint 1 ("macht sehr vieles aus Holz") rules out all three wrong answers at once: porcelain, baby food and bicycles aren't made of wood, so the first hint gives the answer away. Hint 2 (products in kindergartens) does the same. Hint 1 should be vague (e.g. about the family business or the region), and hint 2 should narrow the options without settling it.
- **q-11981** (bundesliga-and-clubs) Du jubelst beim Public Viewing der Heim-EM in Deutschland, Bundestrainer ist Julian Nagelsmann. Welches Jahr ist es? → 2024: This asks the same thing as related q-10943 (in what year Germany hosted a men's Euro, answer 2024), just with different clues (Nagelsmann here, the Berlin final there). Only one of the two should stay in the pool.
- **q-11982** (bundesliga-and-clubs) Fans des FC Bayern rufen gern „Mia san …“. Was bedeutet der ganze Spruch auf Hochdeutsch? → Wir sind wir: Hint 2 („Wir bleiben, wie wir sind“) paraphrases the answer „Wir sind wir“ almost word for word, so it gives the answer away before hint 3. It should instead describe the spirit of the motto (e.g. Bavarian pride, the club's identity) without the "we stay who we are" wording.
- **q-11992** (cakes-and-sweets) Am Sonntag ist der Tisch für Kaffee und Kuchen gedeckt. Welche Tageszeit ist es dann meistens? → Nachmittag: This repeats approved q-9351 ("Du bist zum Adventskaffee eingeladen. Wann gibt es den traditionell?" → Sonntagnachmittag). Both ask what time of day Sunday coffee and cake is held, and the answer is the afternoon. Seeing one gives away the other, so this draft should be dropped, not revised.
- **q-12001** (chancellors-and-presidents) Ich habe Knöpfe und einen immer gleichen Schnitt. Angela Merkel trug mich in fast allen Farben des Regenbogens. Was bin ich? → Blazer: The fact check marks the fun fact as wrong: Noortje van Eekelen's 'Pantone Merkel' chart dates from 2012, not 2013. Since I can't confirm 2013, change the year to 2012 or drop the year from the fun fact. Fact check: wrong. Fun fact date is off: the Dutch designer Noortje van Eekelen made the 'Pantone Merkel' colour chart in 2012, not 2013.
- **q-12016** (childrens-books-and-comics) Welches Merkmal passt NICHT zu einem typischen Wimmelbuch? → Lange Textkapitel: The picked picture has an unsuitable licence (pd-us-only: PD-1923, PD-US-expired).
- **q-12021** (childrens-books-and-comics) Was gehört NICHT zur Bande „Die Wilden Hühner“ von Cornelia Funke? → Baumhaus als Hauptquartier: "Hühner von Sprottes Oma" is a defensible second answer to "Was gehört NICHT zur Bande?": the hens are Oma Slättberg's, not members or property of the gang (the girls only want to save them), so a player could reasonably pick it as well as the treehouse. The question needs a frame where only the treehouse is wrong, e.g. asking which of these is the gang's headquarters, or replacing that option with an actual gang feature.
- **q-12046** (films-and-actors) Ich bin Apachenhäuptling, mein Blutsbruder heißt Ranger, und mein Zwillingsbruder führt die Puder-Rosa-Ranch. Wer bin ich? → Abahachi: The picked picture has an unsuitable licence (pd-us-only: PD-US-no notice).
- **q-12060** (founders-and-entrepreneurs) Wie heißt dieses rote Rutschauto für kleine Kinder? → Bobby-Car: No candidate shows a red Bobby-Car. The only real Bobby-Car (#1) is a blue THW special edition with a child on it, which contradicts the question's 'rote Rutschauto'. The other candidates show a toy car in sand, a pink ride-on, a white VW ride-on, a toy train and a street scene. A new search isn't allowed, so this needs a manual search for a plain red Bobby-Car photo. The other option is to drop 'rote' from the question and use #1. No suitable picture found for this question.
- **q-12068** (gdr-everyday-life) Was stimmt NICHT über den DEFA-Film „Spur der Steine“ von 1966? → Die Romanvorlage schrieb Christa Wolf: Hint 2 gives the answer away. It says the source novel was written "von einem Mann", which rules out Christa Wolf at once and so solves this "what is NOT true" question. Hint 2 needs to be rewritten so it says nothing about the author's gender or identity, for example a vague hint about the film's fate or its setting.
- **q-12071** (gdr-everyday-life) In den „Exquisit“-Läden der DDR zahlte man mit DDR-Mark statt mit Westgeld, aber zu sehr hohen Preisen. Was wurde dort vor allem verkauft? → Modische Kleidung und Schuhe: Hint 1 („Wer dort einkaufte, wollte vor allem gut aussehen.“) gives the answer away: of the four options, only clothing and shoes are about looking good, so it rules out all three wrong answers at once. It is as strong as hint 3. Replace it with a vague hint, e.g. about the shops' look, prices or when they opened, that doesn't point at what they sold.
- **q-12074** (gdr-everyday-life) Bei der Maidemonstration 1985 in Ost-Berlin zogen Tausende an der Ehrentribüne vorbei. Welcher SED-Chef winkte ihnen von dort zu? → Erich Honecker: None of the candidates shows a May Day parade in East Berlin. They show a 1987 city council meeting, a modern climate speaker, 1990 tenant and conscientious-objector protests, and a squatted house on Mainzer Straße. A new search isn't allowed. The slot should become illustrative and get a real 1. Mai DDR parade photo, for example 'Bundesarchiv 1. Mai Berlin Demonstration'. No suitable picture found for this question.
- **q-12075** (gdr-everyday-life) Wer trug in den 1980er-Jahren in der DDR dieses blaue Halstuch? → Jungpioniere der Klassen 1 bis 3: No candidate shows a blue DDR pioneer neckerchief, but the essential image has to show one. Another search isn't allowed, so the slot needs a suitable image, for example a Commons photo of a 'Pionierhalstuch blau'. The other option is to rework the question so it doesn't depend on 'dieses' Halstuch. No suitable picture found for this question.
- **q-12084** (gdr-history) Er leitete über 30 Jahre die HVA, die Auslandsspionage der Stasi, und galt im Westen lange als „Mann ohne Gesicht“. Wer ist er? → Markus Wolf: The media slot is marked essential and its note asks for a portrait of Markus Wolf, but the search ran for the Stasi headquarters, so no candidate matches. The question doesn't need his face, though. Setting the role to illustrative and using candidate 2 (the former Stasi headquarters in Lichtenberg, no visible text) would work. As it stands, no candidate fits the essential note, and no new search is allowed. No suitable picture found for this question.
- **q-12089** (home-and-public-life) Was gehört in Deutschland in diese braune Tonne? → Obst- und Gemüsereste: No candidate shows a German brown Biotonne without a giveaway: 4 is brown but labelled 'BIOJÄTE' next to bins labelled for metal and glass, 1–2 are black Spanish containers with brown lids (2 says 'ORGÁNICA'), and 3, 5 and 6 aren't brown bins. A new search, e.g. 'brown wheelie bin Germany', is needed but not allowed in this run. No suitable picture found for this question.
- **q-12096** (inventors-and-scientists) Beim WM-Finale in Bern regnet es, und Deutschlands Spieler schrauben längere Stollen von Adi Dassler unter die Schuhe. Welches Jahr ist es? → 1954: This asks the same fact as the approved q-9229: the year of the World Cup final in Bern that Germany won (1954). Only the clue changes (Dassler's studs here, the radio commentary there). Separately, hint 1 (Germany's first World Cup title) and hint 2 („Wunder von Bern“) each give the year away to most German players.
- **q-12104** (national-team) Dieser Mann war 15 Jahre lang Bundestrainer der Männer. Wer ist es? → Joachim Löw: None of the six media candidates shows Joachim Löw. They are all Library of Congress photos of early-1900s carriages that matched the surname "Loew", and no new search is allowed. The essential slot needs a clear portrait of Löw without any caption, for example from the search "Joachim Löw Bundestrainer" or "Joachim Löw 2018". No suitable picture found for this question.
- **q-12108** (pop-and-rock) Die Band hinter dem Hit „Applaus, Applaus“ (2013) stammt aus der Nähe welcher Großstadt? → München: Fact check: uncertain. The answer München is right: Sportfreunde Stiller come from Germering near Munich, and 'Applaus, Applaus' is from 2013. Sources disagree on the role of the namesake Hans Stiller. One calls him a former football manager at SV Germering, while the fun fact says youth coach.
- **q-12141** (federal-republic-and-reunification) Im August 1948 entwarfen Fachleute zwei Wochen lang auf einer Insel in einem bayerischen See die Grundlagen des Grundgesetzes. Welche Insel? → Herreninsel: None of the media candidates works: none shows the Grundgesetz. Most show Nazi-era material (police uniform plates, an Organisation Todt Dienstbuch, a völkisch pamphlet), which is wrong for this topic and the tone, and no new search is allowed. Use a new search, such as "Grundgesetz Parlamentarischer Rat" or "Grundgesetz book", for an illustrative image that doesn't show Chiemsee or its islands. No suitable picture found for this question.
- **q-12149** (gdr-everyday-life) Die Simson Schwalbe aus der DDR hat einen Zweitaktmotor. Welche Sonderregel aus der Zeit der Wiedervereinigung gilt für sie bis heute? → Bis zu 60 km/h fahren: The correct option stands out by its form. It is the only one not phrased as „Ohne …“, and it is longer, so players can pick it as the odd one out without knowing the fact. Rephrase all four options in one parallel form: either four permissions like „Bis zu 60 km/h fahren“ / „Ohne Helm fahren“ / … written the same way, or four speed limits such as „Bis zu 60 km/h“, „Bis zu 45 km/h“, „Bis zu 50 km/h“, „Bis zu 70 km/h“, adjusting hints 1 and 3 to match.
- **q-12162** (national-team) Wo schauen diese Fans gerade ein Spiel der Nationalmannschaft? → beim Public Viewing: None of the six candidates shows what the essential image needs: football fans with German flags in the open air, watching a giant screen. Without that photo the question can't be answered, and no new search is allowed. A Fanmeile or public-viewing photo needs to be found on Commons (e.g. "Fanmeile Berlin" or "Public Viewing Deutschland") and attached by hand. No suitable picture found for this question.
- **q-12189** (transport) In der Fahrstunde sitzt der Fahrlehrer neben dir. Was ist im Fahrschulauto extra für ihn ein zweites Mal eingebaut? → Bremspedal: None of the image candidates fits: they show a parking-payment sign, an Irish car-park sign, Wiesmann company signs, an old hotel postcard and a tram. None shows a driving-school car. Another search isn't allowed, so the slot needs a new search such as "Fahrschule car" or "driving school car exterior" (outside of the car only, so the dual pedals don't show). No suitable picture found for this question.
- **q-12197** (schlager-and-folk-music) „Ich habe drei Ecken, sitze auf dem Kopf, und in meinem Lied lässt man nach und nach Wörter weg und zeigt sie nur mit den Händen.“ Wer bin ich? → Hut: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-12198** (schlager-and-folk-music) Die Stimme springt schnell zwischen tief und hoch, oft ohne echte Wörter, und man hört es auf den Almen im Allgäu. Wie heißt dieser Gesang? → Jodeln: This asks the same thing as the approved base question q-4062 (a singing style that flips fast between low and high notes, heard in the Alps → yodeling). Base questions are also played in German, so German players would get the same question twice.
- **q-12201** (shows-and-presenters) Du sitzt bei „Wer wird Millionär?“ und nimmst den Publikumsjoker. Was passiert dann? → Die Leute im Studio stimmen ab: The description „Wenn du nicht weiterweißt, frag einfach alle“ states the answer's defining trait (asking everyone at once). With only the four options, that leaves just „Die Leute im Studio stimmen ab“ and rules out the moderator, the expert and the extra time. Rewrite it so it plays on the quiz-show theme without saying that many people are asked.
- **q-12215** (slang-and-everyday-words) „Yalla, komm jetzt!“ hört man in vielen deutschen Städten. Aus welcher Weltregion stammt das Wort „Yalla“? → Arabische Welt: This overlaps approved q-11100 („Welches Wort stammt NICHT aus dem Arabischen?“, answer Digga). Its Arabic-origin options are almost certainly schoolyard words like „Yalla“, so it tests the same fact, and seeing one question gives the other away. Drop this question, or pick a different loanword whose origin isn't covered in q-11100.
- **q-12223** (state-and-city-emblems) Was für ein Blick ist ein „Basiliskenblick“? → Einen bösen, stechenden Blick: None of the media candidates fits. The search term "empty classroom" has nothing to do with a basilisk or a medieval fable creature, and candidate 6 is an October 7 massacre memorial, which is unsuitable for a family game. The text itself is fine. The image needs a new search for a decorative picture of a medieval basilisk or bestiary, e.g. "medieval bestiary basilisk" or "basilisk woodcut". No suitable picture found for this question.
- **q-12231** (states-and-capitals) Welches Nachbarland Deutschlands hat diese Form? → Frankreich: None of the six candidates is a map or outline of France. They are all silhouettes of people, a statue or a museum building, so the essential image is missing, and no new search is allowed. Getting a usable image will take a search like "France outline map blank" or "France blank map" on Commons. No suitable picture found for this question.
- **q-12233** (transport) Auf der Straße ist ein Unfall passiert. Wer muss jetzt den Verbandskasten holen und Erste Hilfe leisten? → Jeder, der dazukommt: The answer is the only option that doesn't start with "Nur …", so it gives itself away by form alone. Every option needs the same form. One way is to make the answer specific, e.g. "Jeder Ersthelfer vor Ort", against wrong answers like "Ein Arzt", "Die Polizei" and "Der Pannendienst". Hint 2 (the first-aid course for the driving licence) also nearly gives the answer away at hint 2. Facts are fine (§ 323c StGB), and candidate 4 works as the image.
- **q-12244** (winter-sports) Linus Straßer gewann 2024 die Rennen in Kitzbühel und Schladming auf einer Strecke wie dieser. In welcher Disziplin ist er Spezialist? → Slalom: No candidate shows a slalom course. They are a Fra Angelico altarpiece, a photo of the Loggia dei Lanzi in Florence and two 1856 ILN ship engravings. The question says "auf einer Strecke wie dieser", so it needs an essential image of a slalom course with closely spaced gates, and no new search is allowed. Separately, the description ("um Stangen kurvt") already rules out Abfahrt; consider rewording it to play on the theme without the gates. No suitable picture found for this question.

## Question axes

- move: analogy 3, cause_effect 15, count 9, estimate 15, identify 44, made_of 16, name_concept 28, odd_one_out 23, origin 30, purpose 13, record 7, sequence 15, when 24, who 32, word_meaning 21
- stimulus: detail 7, map_outline 1, none 234, photo 53
- clue: completion 9, direct 132, riddle 32, scenario 49, three_facts 73
- answer_kind: group 41, number 26, person 45, place 39, thing 58, time 26, word 60
- lens: body_senses 6, educational_media 37, everyday 45, history 54, language 52, nature 8, pop_culture 49, popular_science 1, school 33, science_news 4, university 6

## Dropped by the pipeline

- art-architecture-and-museums-16: overlap like q-3132: “Legend says I built terraced gardens full of trees for my wife, who missed the green hills of her home.” Who am I? → Nebuchadnezzar II: Du stehst im Berliner Pergamonmuseum vor dem blauen Ischtar-Tor. Unter welchem König wurde es gebaut? → Nebukadnezar II.
- brands-and-products-7: overlap like q-6256: Milka chocolate comes in purple wrappers with a purple cow. Its name joins the German words for milk and which other ingredient? → Cocoa: Vervollständige: Die Kuh aus der Milka-Werbung ist ganz … → lila
- brands-and-products-12: overlap like q-9405: Der Name Haribo steht für Hans Riegel und seine Heimatstadt. In welcher Stadt wurden die Gummibärchen erfunden? → Bonn: Der Name hinter „Haribo macht Kinder froh“ steckt aus Gründer und Stadt zusammen: Ha-Ri-Bo. Wer war der Gründer? → Hans Riegel
- cakes-and-sweets-0: overlap like q-9135: Du schneidest einen dicken Stollen voller Rosinen und Puderzucker an. Wann im Jahr isst man ihn vor allem? → In der Weihnachtszeit: Welche Trockenfrucht steckt reichlich im klassischen Dresdner Christstollen? → Rosinen
- cakes-and-sweets-16: overlap like q-9356: Plätzchen, die man im Advent mit Förmchen aussticht und mit Zuckerguss verziert, tragen oft ein Fett im Namen. Welches? → Butter: Man sticht sie mit Förmchen aus und backt sie im Advent blechweise. Ihr Name heißt eigentlich „kleiner flacher Kuchen“. Was ist das? → Plätzchen
- chancellors-and-presidents-12: overlap like q-9166: Ich rauchte gern Zigarre und war als SPD-Kanzler so eng mit Konzernchefs, dass man mich „Genosse der Bosse“ nannte. Wer bin ich? → Gerhard Schröder: Dieser Kanzler beendete Streit in seiner Partei gern mit einem Machtwort und hieß darum „Basta-Kanzler“. Wer ist es? → Gerhard Schröder
- childrens-and-folk-songs-7: overlap like q-9267: Welche Gestalt tanzt im bekannten Kinderlied „in unserm Haus herum, dideldum“? → Butzemann: Der Butzemann tanzt im Haus herum, rüttelt sich und schüttelt sich. Was wirft er dann hinter sich? → Sein Säckchen
- early-history-2: overlap like q-9220: Zimmerleute auf der Walz tragen schwarze Kluft und großen Hut und sind mindestens drei Jahre und einen Tag unterwegs. Welcher Ort ist für sie dann tabu? → Der eigene Heimatort: Am Straßenrand steht ein Zimmermann in schwarzer Kluft: Er ist auf der Walz. Wie lange dauert sie traditionell mindestens? → 3 Jahre und 1 Tag
- early-history-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Der Name der Stadt Augsburg geht auf diesen römischen Kaiser zurück. Wer ist das? → Augustus
- federal-republic-and-reunification-0: overlap like q-9221: Meister Eder hobelt in seiner Münchner Werkstatt, als Pumuckl am Leimtopf kleben bleibt. Was bedeutet „Meister“ in seinem Namen? → Er hat die Meisterprüfung bestanden: Meister Eder und sein Pumuckl wohnen in der Landeshauptstadt dieses Bundeslandes. Welche Stadt ist das? → München
- federal-republic-and-reunification-5: overlap like q-11029: Das Sandmännchen kommt jeden Abend im Fernsehen. Was ist danach für viele Kinder dran? → Schlafenszeit: Nach welcher kleinen Figur im Abendfernsehen heißt es für viele Kinder seit 1959: Ab ins Bett? → Sandmännchen
- films-and-actors-7: overlap like q-12044: Er zeichnete Männchen mit Knollennasen, erfand die Steinlaus und ließ Opa Hoppenstedt „Früher war mehr Lametta“ sagen. Wie lautet sein Künstlername? → Loriot: Aus welchem Sketch von Loriot stammt der Satz „Früher war mehr Lametta“? → „Weihnachten bei Hoppenstedts“
- films-and-actors-8: overlap like q-2580: It's a baby deer, it often has white spots on its back, and Bambi is one. What is it called? → Fawn: Der Bambi wird seit 1948 verliehen und ist eine goldene Figur. Woher hat der Medienpreis seinen Namen? → Von einem Rehkitz aus einem Kinderbuch
- films-and-actors-12: overlap like q-1235: Soy un perezoso torpe y parlanchín, y viajo con un mamut y un tigre dientes de sable. ¿Cómo me llamo? → Sid: Ich bin tollpatschig, ziehe mit einem Mammut durch die Eiszeit und spreche auf Deutsch mit der Stimme von Otto Waalkes. Wer bin ich? → Sid
- home-and-public-life-4: overlap like q-9462: Dieses Ampelmännchen mit Hut ist heute Kult in Berlin. Aus welchem Staat stammt es ursprünglich? → DDR: Wie nennt man diese Figur auf der Fußgängerampel? → Ampelmännchen
- inventors-and-scientists-2: overlap like q-8988: In December 1965, the Gemini 6 astronauts surprised NASA by playing a tiny harmonica. Which song became the first one played in space? → Jingle Bells: Die Firma Hohner aus Trossingen baut seit 1857 Mundharmonikas. Darin sitzen dünne Metallzungen. Was bringt sie zum Klingen? → Die Luft aus dem Mund
- inventors-and-scientists-4: overlap like q-8766: Gustav Kirchhoff wrote his two famous laws in 1845, while still a student. Engineers use them to work out what? → Currents and voltages in circuits: „Ich kam 1824 in Königsberg zur Welt, fand als Student Regeln für verzweigte Stromkreise und las später in Heidelberg Lichtspektren.“ Wer bin ich? → Gustav Kirchhoff
- inventors-and-scientists-9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Im Wort „Kühlschrank“ steckt schon, was er macht: Er hält Milch, Butter und Joghurt … → kalt
- inventors-and-scientists-12: overlap like q-3018: “Kepler showed I'm the path of every planet around the Sun, and the Sun sits at one of my two focus points.” What shape am I? → An ellipse: Kepler stammte aus Weil der Stadt, arbeitete in Prag und Linz und fand 1609 heraus, welche Form Planetenbahnen haben. Welche? → Ellipse
- national-team-1: overlap like q-7368: ¿Qué selección ha ganado más Copas del Mundo en la historia? → Brasil: Das WM-Finale 2002 in Yokohama verlor Deutschland 0:2 gegen die Mannschaft, die bis heute Rekordweltmeister ist. Gegen wen? → Brasilien
- national-team-12: overlap like q-10984: Manuel Neuer wurde 2014 Weltmeister und gilt als einer der Besten auf seiner Position. Auf welcher Position wurde er berühmt? → Torwart: Mein Trikot hat eine andere Farbe als das meiner Mitspieler. Ich darf den Ball im Strafraum in die Hand nehmen. Oliver Kahn und Manuel Neuer waren wie ich. Wer bin ich? → Torwart
- pop-and-rock-11: overlap like q-10966: Mit welchem Album von 1974 gelang Kraftwerk der Durchbruch in den USA? → Autobahn: Kraftwerk landete 1974 mit „Autobahn“ einen Welterfolg. Welches Album stammt NICHT von Kraftwerk? → Phaedra
- rap-and-electronic-3: overlap like q-11100: Auf dem Schulhof hört man viele Wörter aus anderen Sprachen. Welches davon stammt NICHT aus dem Arabischen? → Digga: Das Wort stammt aus Hamburg, geht auf „Dicker“ zurück und ist heute eine beliebte Anrede unter Jugendlichen. Welches Wort ist es? → Digga
- art-architecture-and-museums-0: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Der Architekt Frei Otto wurde mit einem Dach in München weltberühmt. Für welche Bauweise steht er? → Seilnetzkonstruktion
- athletes-and-other-sports-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Kristina Vogel wurde 2012 und 2016 auf einer Bahn wie dieser Olympiasiegerin. Wie heißt so eine Anlage? → Velodrom
- brands-and-products-5: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Elmex gibt es als Paste, als Gelee für einmal pro Woche und als Spülung. Wofür ist es da? → Zahnpflege
- bundesliga-and-clubs-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Dieser Stürmer schoss bei der WM 2002 fünf Tore. Womit erzielte er alle fünf? → Kopf
- winter-sports-0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Was siehst du auf diesem Foto? → Skischule
- winter-sports-5: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Wie viele Skistöcke benutzt ein Skifahrer normalerweise? → 2
- winter-sports-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Im Biathlon-Sprint wird zweimal geschossen, beim ersten Mal liegend. In welcher Haltung schießt man beim zweiten Mal? → Stehend
- winter-sports-15: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Er ist schwarz, flach wie eine Scheibe und aus Hartgummi. Eishockeyspieler schießen ihn mit dem Schläger ins Tor. Was ist er? → Puck
- chancellors-and-presidents-16: overlap like q-9160: Du blätterst in alten Satireheften: „Mutti“ ist zu Angela Merkel wie welches Obst zu Helmut Kohl? → Birne: Welcher dieser Spitznamen gehörte NICHT zu Angela Merkel? → Birne
- childrens-books-and-comics-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Mit den Ohren der Toniebox stellt man ein, wie laut sie ist. Wie viele Ohren hat sie? → 2
- childrens-books-and-comics-9: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In „Die unendliche Geschichte“ gilt: Artax ist zu Pferd wie Fuchur zu …? → Glücksdrache
- childrens-books-and-comics-15: hard fail: correct 3, unambiguous 4, no_giveaway 3, no_overlap 5: Echte „Bücherwürmer“ gibt es wirklich: Sie fressen sich durch alte Bücher. Was sind sie meistens? → Käferlarven
- early-history-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Wer im Mittelalter abends zu spät heimkam, musste vor der Stadtmauer übernachten. Welches Wort für die Sorge, etwas zu verpassen, stammt daher? → Torschlusspanik
- early-history-10: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Ritter trugen unter ihrem Wappenrock oft ein Kettenhemd. Woraus bestand es? → Kleinen Eisenringen
- early-history-13: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: Dieser Ausschnitt zeigt etwas, das auf Jahrmärkten und dem Oktoberfest an Bändern hängt. Was ist es? → Lebkuchenherz
- federal-republic-and-reunification-16: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Dieses Auto baute die Firma Volkswagen. Für wen war es ursprünglich gedacht? → Normale Familien
- federal-republic-and-reunification-17: overlap like films-and-actors-12: Ich bin tollpatschig, ziehe mit einem Mammut durch die Eiszeit und spreche auf Deutsch mit der Stimme von Otto Waalkes. Wer bin ich? → Sid: Dieser Ostfriese wurde in den 1970ern mit Blödel-Shows berühmt und dreht seit 1985 eigene Kinofilme. Wer ist er? → Otto Waalkes
- founders-and-entrepreneurs-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welcher Hamburger Kaufmann gründete 1949 einen Versandhandel, der heute zu den größten Onlinehändlern Deutschlands gehört? → Werner Otto
- home-and-public-life-1: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Sie trennt oft Nachbargärten, Vögel brüten darin, und von März bis September darf man sie nicht radikal stutzen. Was ist gemeint? → Hecke
- inventors-and-scientists-5: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: „Mein Hauptsitz ist in Köln, und ich forsche an Flugzeugen, Satelliten, Raketenantrieben und Energie.“ Wer bin ich? → DLR
- slang-and-everyday-words-2: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Eine „Red Flag“ ist ein Warnzeichen. Welches Verhalten in einer neuen Freundschaft ist KEINE Red Flag? → Jemand hört dir zu und fragt nach
- slang-and-everyday-words-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: „Ja“ wird lässig zu „Jo“. Welches lässige „Nein“ klingt passend dazu, wenn du keine Lust aufs Aufräumen hast? → Nö
- slang-and-everyday-words-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welcher „Kopf“ redet ständig Unsinn? → Quatschkopf
- state-and-city-emblems-17: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Vervollständige den Satz aus der Wappenkunde: „Die Helmdecke ist …“ → das Tuch, das vom Helm zu beiden Seiten herabfällt
- states-and-capitals-6: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Weihnachten ist zum Christbaum wie der 1. Mai zum …? → Maibaum
- schlager-and-folk-music-2: overlap like q-3891: Nicole was 17 when she won Eurovision 1982 for Germany. It's still the last winner sung in German. Which song was it? → “Ein bisschen Frieden”: Wer im Radio „Ein bisschen Frieden“ hört, hört Deutschlands ersten ESC-Sieg. In welchem Jahr gewann Nicole damit? → 1982
- shows-and-presenters-9: overlap like q-2823: On The Bachelor, what does the bachelor give to each woman he wants to keep on the show? → A rose: Bei „Der Bachelor“ fällt immer wieder die Frage: „Möchtest du diese … annehmen?“ Welches Wort fehlt? → Rose
- state-and-city-emblems-8: overlap like q-9157: In diesem Gebäude wählen die Abgeordneten den Bundeskanzler. Welches ist es? → Reichstagsgebäude: Es steht in Berlin, wurde 1894 eröffnet und hat seit 1999 eine begehbare Glaskuppel über dem Plenarsaal des Bundestags. Welches Gebäude ist es? → Reichstagsgebäude
- states-and-capitals-16: overlap like q-9126: Du sitzt am Weihnachtstisch, es gibt Gänsebraten, Rotkohl und runde Klöße. Woraus sind die Klöße meistens gemacht? → Kartoffeln: Diese Klöße sind der Stolz Thüringens. Woraus werden sie hauptsächlich gemacht? → Kartoffeln
