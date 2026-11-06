# batch-41

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): winter-sports, empire-weimar-and-nazi-era, sausages-and-cheese, cities-and-towns, dialects-and-regional-words, reformation-to-empire, mountains-and-landscapes, plants-and-forests, national-symbols-and-state, sayings-and-idioms, school-and-education, carnival-and-fairs, classic-literature, money-and-shopping, childrens-tv-and-audio-dramas, national-team, series-and-crime, drinks, legends-and-figures, parks-weather-and-climate, holidays-through-the-year, bread-and-baked-goods, rap-and-electronic, family-customs-and-dress, brands-and-products, regional-dishes, advent-and-christmas
- Merged: 259 (q-12953…q-13211)
- Approved: 243
- Needs work: 16
- Dropped by the pipeline: 77
- Reviewed by: claude-opus-5-5
- Claude calls: 558, about $77.09 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-39, batch-40; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-39 | batch-40 | batch-41 |
|---|---|---:|---:|---:|
| source locale |  | es | en | de |
| drafts |  | 305 | 310 | 336 |
| skipped slots |  | 217 | 140 | 150 |
| dropped |  | 73 | 82 | 77 |
| drop rate | ≤ 20.0 % | 23.9 % ✗ | 26.5 % ✗ | 22.9 % ✗ |
| dropped: hard fail correct |  | 3 | 2 | 0 |
| dropped: hard fail unambiguous |  | 2 | 1 | 2 |
| dropped: hard fail no_giveaway |  | 19 | 26 | 21 |
| dropped: overlap |  | 48 | 53 | 51 |
| dropped: duplicate |  | 1 | 1 | 2 |
| dropped: fact-check wrong |  | 2 | 1 | 1 |
| merged |  | 232 | 228 | 259 |
| approved |  | 212 | 214 | 243 |
| needs_work |  | 20 | 14 | 16 |
| needs_work rate | ≤ 20.0 % | 8.6 % ✓ | 6.1 % ✓ | 6.2 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.3 % ✓ | 2.2 % ✓ | 1.5 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.9 % ✓ | 0.4 % ✓ | 0.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.2 % ✗ | 0.4 % ✓ | 0.8 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.3 % ✓ | 3.5 % ✓ | 3.9 % ✓ |
| media: no pick in review 1 |  | 37 | 27 | 49 |
| media: recovered by research |  | 28 | 22 | 40 |
| media: no pick at record |  | 9 | 6 | 9 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 17.7 % ✓ | 17.7 % ✓ | 16.4 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 48.2 % ✗ | 58.0 % ✓ | 63.3 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 0.71 ✓ | 1.75 ✗ | 1.29 ✓ |
| approved 11–15 |  | 47 | 47 | 60 |
| top move | ≤ 25.0 % | 14.2 % ✓ | 20.2 % ✓ | 13.9 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 79.3 % | 72.4 % | 78.4 % |
| values stimulus |  | 5 | 5 | 5 |
| top clue | ≤ 60.0 % | 44.8 % ✓ | 47.8 % ✓ | 46.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 22.4 % ✓ | 23.7 % ✓ | 26.3 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 20.3 % ✓ | 17.5 % ✓ | 25.1 % ✗ |
| values lens |  | 11 | 11 | 10 |
| media share | 15.0 %–50.0 % | 20.7 % ✓ | 27.6 % ✓ | 21.6 % ✓ |
| mean fun | ≥ 3.40 | 3.47 ✓ | 3.56 ✓ | 3.40 ✗ |
| cost $ |  | $67.46 | $64.05 | $73.68 |
| $ per approved | ≤ $0.35 | $0.32 ✓ | $0.30 ✓ | $0.30 ✓ |
| calls |  | 471 | 470 | 498 |
| calls per approved |  | 2.22 | 2.20 | 2.05 |
| wall time h |  | 1.89 | 1.84 | 2.14 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 56 (2 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 11 (2 major), overlap 2 (0 major), media 1 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.41

Major findings on approved questions:

- **q-13058**: giveaway — The facts hold up: under KErzG §5, at 14 a child decides on their own religion, and from 12 they can't be raised in a different faith against their will. The problem is the description. "mehr Mitspracherecht, als manchen Eltern lieb ist" gives away the answer's defining trait, the right to decide for yourself against the parents' wishes. That rules out the tax and baptism options, which are duties, and the church wedding, which has nothing to do with having a say over your parents, before any hint is shown. Hint 2 ("Vorher bestimmen darüber meist die Eltern") narrows the options in the same way, which is a minor giveaway on its own. (http://127.0.0.1:8001/review/q-13058)

## Needs work

- **q-12956** (advent-and-christmas) Wann ist in den meisten deutschen Familien die Bescherung? → am Abend des 24. Dezember: Overlaps the approved q-9122 („Wozu kommt das Christkind an Heiligabend?“ → um Geschenke zu bringen). That question already says presents arrive on Heiligabend, so seeing it answers this one: the 24th is the only option on that day. Hint 2 also repeats the fact from q-9123 (Heiligabend is the eve of the first Weihnachtsfeiertag).
- **q-12960** (advent-and-christmas) Bei einem bayerischen Brauch zieht man zwischen Weihnachten und Dreikönig von Haus zu Haus und lobt den Christbaum der Gastgeber. Was bekommt man dafür? → einen Schnaps: Hint 2 gives the answer away: the host "füllt nach" (tops it up), which only fits a drink, so among the four options only Schnaps is left, and hint 3 then adds nothing. Hint 2 should stay vague, e.g. about where the reward is kept or how the host shows his thanks, without suggesting pouring or refilling.
- **q-12969** (carnival-and-fairs) Beim Rosenmontagszug ruft man am Straßenrand laut „Kamelle!“. Wer wirft daraufhin Süßigkeiten? → Die Leute auf den Festwagen: No adequate image: candidate 1 shows a carnival float (the answer), the others show Italian/Maltese carnival pastries or a Russian Maslenitsa scene, none of which depicts Kamelle or a German Rosenmontag setting. A new search (e.g. "wrapped hard candies" or "carnival crowd Cologne", avoiding floats) is needed. No suitable picture found for this question.
- **q-12970** (carnival-and-fairs) Beim Dosenwerfen sollen die Wurfbälle weich sein, nicht weit abprallen und nichts kaputt machen. Woraus sind sie meistens? → Stoff: No candidate fits: the sheet shows bee-eaters, rose and ground-ivy flowers, a beetle in a magnolia and lobster traps, nothing from a can-throwing stall, and no new search is allowed. Also, the fun fact (hitting the bottom row knocks down the most) is unverified; drop it or swap in a confirmed fact, e.g. that the balls are sewn fabric filled with granules or sawdust. No suitable picture found for this question.
- **q-12971** (carnival-and-fairs) Bei einer Karnevalssitzung fordert der Präsident „eine Rakete“. Was soll das Publikum tun? → Besonders laut Beifall spenden: Hint 2 („Dabei wird getrommelt, gepfiffen und geklatscht.“) gives the answer away: clapping is the answer („Besonders laut Beifall spenden“), and none of the other options involves it. Hint 2 should stay vaguer, e.g. say that the whole hall joins in on a set signal without naming clapping. The tabletop drumming and whistling can stay for hint 3 or the fun fact.
- **q-12974** (childrens-tv-and-audio-dramas) Ein Mädchen liest in einem magischen Buch, wird zur Elfe mit Flügeln und reitet auf Einhörnern. Wie heißt die Welt in „Mia and Me“? → Centopia: The text is fine, but no media candidate fits. Candidates 1 and 6 show an ancient bronze 'unicorn carrying vases' that reads as an odd archaic animal rather than a unicorn, and candidates 2–5 are fragments of post-medieval lead toys. A new search is not allowed, so the slot needs a different image (e.g. 'unicorn fantasy illustration' or 'fairy wings costume'). No suitable picture found for this question.
- **q-13004** (drinks) Du bestellst eine „Weiße mit Schuss“ und bekommst sie rot mit Himbeersirup. In welcher Stadt ist das Tradition? → Berlin: No candidate shows anything to do with the question. They show maple syrup bottles, an ice-cream sundae, honey and maple syrup jars at a buffet, an old cherry syrup jug, a Rijksmuseum print and a vineyard. Another search isn't allowed. The image slot needs a new search such as "Berliner Weisse glass" or "red beer goblet straw". A red Berliner Weiße with a straw is fine as an illustrative image, as long as no glass, sign or label shows the word "Berliner". No suitable picture found for this question.
- **q-13018** (family-customs-and-dress) In vielen deutschen Wohnungen zieht man an der Haustür solche Schuhe an. Was bleibt dadurch sauber? → Fußboden: None of the candidates works as the essential image. Candidates 1 and 2 are museum photos of embroidered Chinese silk slippers, not the ordinary German felt Hausschuhe the question and note call for. Candidates 3–6 are manuscript pages, a book page and a hospital ward. The question needs a clear photo of ordinary felt or plush house slippers, for example with the query 'felt slippers pair' or 'house slippers'. No suitable picture found for this question.
- **q-13022** (family-customs-and-dress) Was ist die eigentliche Aufgabe eines Taufpaten? → Das Kind im Leben und Glauben begleiten: Hint 2 („Die Aufgabe geht weit über den Tag der Taufe hinaus“) gives the answer away. All three wrong answers are tasks for the baptism day, or at most one-off tasks (leading the service, choosing the name, filling the font). The hint rules out every one of them, so only the answer is left. Replace hint 2 with a vague hint that doesn't separate lifelong tasks from one-off ones, for example one about the Pate's promise during the ceremony.
- **q-13032** (legends-and-figures) Dieser Dichter machte die Sage vom Doktor Faust weltberühmt, der einen Pakt mit dem Teufel schließt. Wer ist er? → Johann Wolfgang von Goethe: The media slot doesn't fit together: its role is essential and its note asks for a Goethe portrait, but the search term and all four candidates show the Faust/Mephisto statues at Auerbachs Keller in Leipzig. No candidate matches the note, and a new search isn't allowed. A Goethe portrait would give the answer away anyway. Set the role to illustrative and use candidate 1 (the Faust and Mephisto statue). The question text itself is fine. No suitable picture found for this question.
- **q-13057** (national-symbols-and-state) Das markierte Bundesland ließ als erstes 16-Jährige das Landesparlament mitwählen. Welches ist es? → Bremen: No candidate shows a Germany map with only Bremen (both Bremen and Bremerhaven) marked. Candidates 1–4 mark Lower Saxony, northern Germany or the Bremen-Oldenburg region instead, and the stamp (5) prints "BREMEN". No new search is allowed, so the essential map needs to be supplied another way, e.g. a Commons locator map such as "Locator map Bremen in Germany.svg". No suitable picture found for this question.
- **q-13059** (national-symbols-and-state) Du bekommst einen Brief mit dem Bundesadler im Briefkopf. Von wem kann er NICHT stammen? → Vom Bürgermeister deiner Stadt: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-13069** (national-symbols-and-state) Zähl mal nach: Aus wie vielen Bundesländern besteht Deutschland auf dieser Karte? → 16: None of the candidates shows a map of Germany with its federal states. The question says "auf dieser Karte" and needs an essential blank map of the 16 Länder, and no new search is allowed. A suitable file is a blank Länder map from Commons, e.g. "Germany states blank map" or "Deutschland Bundesländer leer". No suitable picture found for this question.
- **q-13073** (national-team) An allen vier Seitenfenstern eines Autos steckt eine Deutschlandfahne. Wie viele Farbstreifen sind das zusammen? → 12: None of the image candidates shows car flags or German fan flags: they show a Scottish saltire in a house window, a historic army football crowd, English flags at Rugby School and a Danish team bus. A new search such as "Germany car flag" or "car flag Germany fan" is needed, but a new search isn't available for this slot. No suitable picture found for this question.
- **q-13140** (family-customs-and-dress) Heute nennt man etwas besonders Gelungenes „ein Meisterstück“. Was war ein Meisterstück ursprünglich? → Prüfungsarbeit zum Meister: This overlaps too much with approved q-9221 (Meister Eder: "Meister" means he passed the Meisterprüfung). Anyone who has seen that question can solve this one at once, because the Meisterstück is exactly the piece made for that exam. Both questions turn on the same fact, the master craftsman's exam.
- **q-13156** (plants-and-forests) Er steht zu Ostern in vielen deutschen Wohnungen. Was ist ein „Osterstrauß“? → Zweige, behängt mit bunten Eiern: Hint 2 („Man stellt ihn oft schon Wochen vor Ostern ins Wasser.“) gives the answer away: only the branches option can stand in water, so the other three are ruled out at the second hint. Hint 2 needs to be a vaguer clue, e.g. about the custom or the season, that leaves the chocolate flowers, the Hefezopf and the basket possible.

## Question axes

- move: analogy 5, cause_effect 11, count 10, estimate 11, identify 36, made_of 14, name_concept 33, odd_one_out 17, origin 21, purpose 20, record 4, sequence 10, when 19, who 23, word_meaning 25
- stimulus: detail 6, map_outline 1, none 203, photo 47, sound 2
- clue: completion 6, direct 121, riddle 29, scenario 36, three_facts 67
- answer_kind: group 35, number 22, person 37, place 28, thing 68, time 20, word 49
- lens: body_senses 7, educational_media 24, everyday 38, history 65, language 56, nature 6, pop_culture 31, school 13, science_news 1, university 18

## Dropped by the pipeline

- advent-and-christmas-13: overlap like q-12044: Er zeichnete Männchen mit Knollennasen, erfand die Steinlaus und ließ Opa Hoppenstedt „Früher war mehr Lametta“ sagen. Wie lautet sein Künstlername? → Loriot: Über diesen Baumschmuck schimpft Opa Hoppenstedt: „Früher war mehr …!“ Wer hat sich den berühmten Satz ausgedacht? → Loriot
- brands-and-products-9: overlap like q-6256: Milka chocolate comes in purple wrappers with a purple cow. Its name joins the German words for milk and which other ingredient? → Cocoa: In der Werbung ist eine Kuh wie diese lila. Für welche Schokolade wirbt sie? → Milka
- bread-and-baked-goods-14: overlap like q-9378: Welcher Zucker ist so fein gemahlen, dass er beim Pusten staubt und wie Schnee auf dem Christstollen liegt? → Puderzucker: Du willst Zuckerguss anrühren. Welchen Zucker verrührst du dafür mit etwas Wasser oder Zitronensaft? → Puderzucker
- carnival-and-fairs-17: overlap like q-5373: What are these tiny colorful pieces of paper that people throw at parties? → Confetti: Das Wort kommt aus Italien, wo man im Karneval Zuckerwerk warf. Heute sind es bunte Papierschnipsel. Wie heißt es? → Konfetti
- childrens-tv-and-audio-dramas-1: overlap like q-10853: Welcher Moderator der Sachgeschichten in der „Sendung mit der Maus“ trägt fast immer einen grünen Pullover? → Christoph Biemann: „Ich wurde 1952 in Mecklenburg geboren und drehe seit den 1970ern mit Armin Maiwald Filme für die Maus. Wer bin ich?“ → Christoph Biemann
- childrens-tv-and-audio-dramas-9: overlap like q-10859: Welche Farbe hat KEINE der drei Figuren Maus, Elefant und Ente aus der „Sendung mit der Maus“? → Grün: Der kleine blaue Elefant bekam 2007 eine eigene Sendung für Vorschulkinder. In welcher Sendung trat er schon vorher auf? → Die Sendung mit der Maus
- childrens-tv-and-audio-dramas-11: overlap like q-10862: „Ich bin jung, kann zaubern und wohne in Neustadt. Ich fliege auf Kartoffelbrei, und meine Sprüche enden mit „Hex-hex!“. Wer bin ich?“ → Bibi Blocksberg: „Ich habe einen langen Stiel und Borsten am Ende und fliege mit Bibi Blocksberg durch Neustadt. Wer bin ich?“ → Kartoffelbrei
- childrens-tv-and-audio-dramas-14: overlap like q-9231: Welches Wort fehlt bei der „Sendung mit der Maus“: „Lach- und …geschichten“? → Sach: Am Anfang der „Sendung mit der Maus“ heißt es: „Lach- und …“. Wie geht es weiter? → Sachgeschichten
- childrens-tv-and-audio-dramas-17: overlap like q-10856: In welchem Jahrzehnt startete „Löwenzahn“, die Sendung mit Peter Lustig im blauen Bauwagen? → 1980er: Wer „Löwenzahn“ mit Fritz Fuchs einschaltet, sieht ihn im früheren Zuhause von Peter Lustig wohnen. Worin? → Bauwagen
- cities-and-towns-0: overlap like q-12177: Eine berühmte Sage spielt in Hameln an der Weser. Wozu spielte der fremde Mann dort zuerst auf seiner Flöte? → Ratten weglocken: Ich spiele Flöte und trage bunte Kleider. Eine Stadt an der Weser zahlte mir meinen Lohn nicht, da führte ich ihre Kinder fort. Wer bin ich? → Rattenfänger von Hameln
- cities-and-towns-5: duplicate like q-12205: An diesem Schokoladenbrunnen in einem Museum dürfen Besucher naschen. In welcher Stadt steht er? → Köln: Schau dir diese riesige Kirche an. In welcher Stadt steht sie? → Köln
- cities-and-towns-13: overlap like q-2355: This famous crossing linked West Berlin and East Berlin. Who was allowed to use it? → Foreigners and Allied soldiers: Du stehst in Berlin am Checkpoint Charlie vor dem Schild „You are leaving the American sector“. In welchen Jahren war hier ein Grenzübergang? → 1961 bis 1990
- classic-literature-1: overlap like q-10839: Im Kreisspiel „Dornröschen war ein schönes Kind“ spricht die böse Fee einen Fluch. Wie viele Jahre soll Dornröschen schlafen? → 100: Du schläfst so lange wie Dornröschen. Wie viele Jahre wären das? → 100
- classic-literature-5: overlap like q-9334: Ein Frankfurter Arzt schuf ein Kinderbuch mit dem Suppenkaspar, dem Zappelphilipp und Hans Guck-in-die-Luft. Wie heißt es? → Der Struwwelpeter: Ich war Arzt in Frankfurt und zeichnete 1844 selbst ein Bilderbuch für meinen Sohn – mit einem Kaspar, der seine Suppe nicht essen will. Wer bin ich? → Heinrich Hoffmann
- classic-literature-10: overlap like q-10844: Ich bin ein dicker, schüchterner Junge. Aus Herrn Koreanders Antiquariat nahm ich ein Buch mit und las es auf dem Dachboden meiner Schule. Wer bin ich? → Bastian: Bastian klaut mich aus einem Buchladen, liest mich auf dem Dachboden der Schule und gerät schließlich selbst in mich hinein. Was bin ich? → Die unendliche Geschichte
- classic-literature-15: overlap like q-12208: Ich kam 1875 in Lübeck zur Welt und schrieb über eine Kaufmannsfamilie meiner Heimatstadt. 1929 bekam ich den Literaturnobelpreis. Wer bin ich? → Thomas Mann: Er schrieb „Der Untertan“ und „Professor Unrat“, die Vorlage für „Der blaue Engel“, und starb 1950 in Kalifornien. Aus welcher Stadt stammt er? → Lübeck
- dialects-and-regional-words-1: overlap like q-9475: Wer nennt dieses Gebäck typischerweise „Brezn“? → jemand aus Bayern: „Red koa so a Gschmarri!“ – In welchem Bundesland schimpft man so, wenn jemand Unsinn erzählt? → Bayern
- dialects-and-regional-words-5: overlap like dialects-and-regional-words-1: „Red koa so a Gschmarri!“ – In welchem Bundesland schimpft man so, wenn jemand Unsinn erzählt? → Bayern: „Oachkatzlschwoaf“ ist ein berühmter Zungenbrecher, der den buschigen Teil eines Waldtiers meint. Wer ihn nicht schafft, ist kein Einheimischer. Wo? → Bayern
- dialects-and-regional-words-9: overlap like q-10882: Man sagt sie zu Menschen, die man lieb hat, oft enden sie auf „-i“, und „Mausi“ ist einer davon. Was für ein Name ist das? → Kosename: „Schatz“ ist zu „Schatzi“ wie „Hase“ zu …? → Hasi
- dialects-and-regional-words-16: overlap like q-10985: Dortmund gegen Schalke: zwei Nachbarstädte, gelbe gegen blaue Fans, und das Spiel heißt „Revierderby“. Woher kommt das „Revier“? → Vom Ruhrgebiet mit seinen Kohlezechen: Dort standen früher viele Zechen, Schalke und der BVB spielen dort Fußball, und man sagt „Revier“. Woher kommt man, wenn man „ausm Pott“ ist? → Ruhrgebiet
- drinks-4: overlap like q-12100: Man hängt ihn am Faden in heißes Wasser, er ist aus dünnem Papier, und Teekanne erfand 1949 eine Form mit zwei Kammern. Was ist es? → Teebeutel: Die Düsseldorfer Firma Teekanne brachte den Doppelkammer-Teebeutel auf den Markt, den es bis heute gibt. In welchem Jahr? → 1949
- drinks-5: overlap like q-9420: Diese Blätter riechen frisch und kühl. Was macht man in Deutschland bei Bauchweh oft daraus? → Tee: Aus welcher Pflanze wird dieser Tee gemacht? → Minze
- drinks-8: overlap like q-12128: Holzbuden, Lebkuchenherzen, gebrannte Mandeln und warmer Kinderpunsch: Welcher Markt ist gemeint? → Weihnachtsmarkt: Wann trinkt man in Deutschland typischerweise Kinderpunsch? → In der Adventszeit
- drinks-10: overlap like q-3805: In how many Shakespeare plays does the fat, joking knight Sir John Falstaff appear on stage? → 3: Der Name „Sekt“ soll auf einen Berliner Schauspieler zurückgehen, der als Falstaff nach „Sack“ rief. Wer schrieb die Falstaff-Rolle? → William Shakespeare
- empire-weimar-and-nazi-era-7: overlap like classic-literature-15: Er schrieb „Der Untertan“ und „Professor Unrat“, die Vorlage für „Der blaue Engel“, und starb 1950 in Kalifornien. Aus welcher Stadt stammt er? → Lübeck: Der Film „Der blaue Engel“ von 1930 beruht auf dem Roman „Professor Unrat“. Wer hatte ihn geschrieben? → Heinrich Mann
- family-customs-and-dress-9: overlap like q-9392: „Ich komme aus dem Automaten, nachdem du leere Flaschen hineingesteckt hast, und an der Kasse werde ich zu Geld.“ Was bin ich? → Pfandbon: Solche Automaten stehen in fast jedem deutschen Supermarkt. Was steckt man dort hinein? → Leere Flaschen
- holidays-through-the-year-1: overlap like family-customs-and-dress-14: Für 25 Ehejahre steht Silber, für 50 Jahre Gold. Nach welchem Material ist das Jubiläum nach 60 Ehejahren benannt? → Diamant: Bei der Silberhochzeit hängt ein Kranz an der Tür, es gibt silberne Geschenke und manchmal ein zweites Jawort. Wie lange ist das Paar verheiratet? → 25 Jahre
- holidays-through-the-year-13: overlap like q-8750: Gunpowder reached Europe in the 1200s after traveling along trade routes. Where was it first invented? → China: Böller gibt es in Deutschland nur zum Jahresende zu kaufen. Die meisten kommen aus dem Land, wo das Schwarzpulver erfunden wurde. Welchem? → China
- legends-and-figures-13: overlap like q-9364: „Wir arbeiteten nachts für die faulen Kölner, bis eine neugierige Frau Erbsen streute. Seitdem sind wir fort.“ Wer sind wir? → Heinzelmännchen: Wie geht die berühmte Zeile von August Kopisch weiter: „Wie war zu Köln es doch vordem mit Heinzelmännchen so …“? → bequem
- money-and-shopping-5: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Der Verbraucherzentrale Bundesverband wurde im Jahr 2000 gegründet, sitzt in Berlin und ist ein Dachverband. Wer sind vor allem seine Mitglieder? → Die 16 Verbraucherzentralen der Länder
- mountains-and-landscapes-11: overlap like q-0319: ¿Cómo se llama la espada legendaria del rey Arturo? → Excalibur: Was gehört NICHT zur Sage von Siegfried dem Drachentöter? → Excalibur
- mountains-and-landscapes-14: overlap like q-9316: In den 1980ern fürchtete man in Deutschland das „Waldsterben“ durch sauren Regen. Welches Gas aus Kohlekraftwerken machte ihn vor allem sauer? → Schwefeldioxid: Solche Bilder vom Waldsterben gab es in den 1980er-Jahren zum Beispiel im Erzgebirge. Was machte damals den Regen so sauer? → Schwefel aus Kohlekraftwerken
- national-team-0: overlap like q-9232: In welchem Jahr wurde Lothar Matthäus als Kapitän mit Deutschland Fußball-Weltmeister? → 1990: Lothar Matthäus wurde als erster Spieler überhaupt von der FIFA zum Weltfußballer gewählt. In welchem Jahr war das? → 1991
- national-team-13: overlap like q-12583: En el Mundial de Qatar 2022, este jugador le metió un golazo de zurda a México. ¿Quién es? → Lionel Messi: Ich bin nur 1,70 Meter groß und schieße fast alles mit links. 2014 verlor ich das WM-Finale gegen Deutschland, 2022 wurde ich doch Weltmeister. Wer bin ich? → Lionel Messi
- parks-weather-and-climate-11: overlap like q-9310: Ich färbe den Himmel rot und orange, kurz bevor die Sonne aufgeht. Eine alte Bauernregel sagt, nach mir kommt oft schlechtes Wetter. Wer bin ich? → Morgenrot: Bauernregeln reimen sich oft, sind Hunderte Jahre alt und hängen an Tagen wie Siebenschläfer. Wofür nutzten die Bauern sie früher? → Um das Wetter vorherzusagen
- plants-and-forests-5: overlap like q-9352: „Advent, Advent, ein Lichtlein brennt“ – so beginnt ein Gedicht zu diesem Kranz. Woraus ist er meist gebunden? → Tannenzweigen: Er hat vier Kerzen, liegt im Advent auf dem Tisch, und jeden Sonntag brennt eine mehr. Woraus wird dieser Kranz meist gebunden? → Aus Tannenzweigen
- plants-and-forests-11: overlap like q-12042: Solche Flugzeuge brachten 1948/49 Lebensmittel und Kohle nach West-Berlin. Welchen Spitznamen gaben ihnen die Berliner? → Rosinenbomber: Nach ihnen hießen die Flugzeuge der Berliner Luftbrücke, sie stecken im Christstollen, und wer nur das Beste nimmt, pickt sie sich heraus. Was ist gemeint? → Rosinen
- rap-and-electronic-2: overlap like q-11100: Auf dem Schulhof hört man viele Wörter aus anderen Sprachen. Welches davon stammt NICHT aus dem Arabischen? → Digga: Dieses Wort kommt aus Hamburg, ist aus „Dicker“ entstanden und bedeutet heute so viel wie „Kumpel“. Welches ist es? → Digga
- reformation-to-empire-4: overlap like q-13039: Wer tanzt im Märchen ums Feuer und singt: „Ach, wie gut, dass niemand weiß …“? → Rumpelstilzchen: In einem Märchen der Brüder Grimm spinnt ein kleines Männchen Stroh zu Gold, und die Königin muss seinen Namen erraten. Welches Märchen ist es? → Rumpelstilzchen
- reformation-to-empire-6: overlap like q-2345: I'm “Für Elise”, a short piano piece that almost every piano student learns. Who wrote me? → Ludwig van Beethoven: Es steht in a-Moll, beginnt mit zwei Tönen im schnellen Wechsel, und Beethoven schrieb es um 1810. Für welches Instrument ist „Für Elise“? → Klavier
- reformation-to-empire-7: overlap like q-10801: Du gehst durch einen Museumssaal mit Bildern der deutschen Romantik. Welches Werk gehört NICHT dorthin? → „Großstadt“ von Otto Dix: Zu welcher Kunstepoche gehört dieses Gemälde von Caspar David Friedrich? → Romantik
- reformation-to-empire-12: overlap like q-9209: Hoffmann von Fallersleben dichtete es 1841 auf Helgoland, die Melodie stammt von Joseph Haydn. 1922 wurde es Nationalhymne. Welches Lied? → Deutschlandlied: Auf dieser Insel schrieb er 1841 das „Lied der Deutschen“, dessen dritte Strophe heute Nationalhymne ist. Wer war es? → Hoffmann von Fallersleben
- regional-dishes-2: overlap like q-9388: Welche Stadt gilt als Hauptstadt des Apfelweins, der dort im Winter auch heiß mit Zimt und Nelken getrunken wird? → Frankfurt am Main: In diesem Krug, dem „Bembel“, kommt Apfelwein auf den Tisch. Welche Stadt ist für ihren „Ebbelwoi“ berühmt? → Frankfurt am Main
- regional-dishes-6: overlap like q-4370: I swim in huge schools in the North Atlantic. The Dutch eat me raw with onions, smoked I'm a kipper, and Swedes ferment me in smelly cans. What am I? → Herring: Matjes, Bismarck und Rollmops im Fischbrötchen stammen vom selben Fisch, der in riesigen Schwärmen durch die Nordsee zieht. Welcher ist es? → Hering
- advent-and-christmas-2: overlap like q-9355: Wer verkündet in der Weihnachtsgeschichte den Hirten auf dem Feld die Geburt Jesu? → Engel: Ich bin oft golden und glitzernd, sitze ganz oben auf dem Weihnachtsbaum, und wenn ich fehle, sitzt dort oft ein Stern. Wer bin ich? → Engel
- brands-and-products-3: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Tipp-Ex kam 1959 aus Hessen: Man legte ein weißes Blättchen auf den Fehler und tippte den Buchstaben noch mal. Auf welchen Geräten? → Schreibmaschinen
- brands-and-products-17: overlap like q-3057: I was founded in Germany in 1838 by Carl Heinrich Knorr, and you'll find me in kitchen cupboards worldwide. What am I best known for? → Soups and stock cubes: Die Erbswurst gibt es seit 1889 von Knorr, Soldaten nahmen sie als Notration mit. Was macht man aus ihr? → Suppe
- bread-and-baked-goods-4: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Dieses Brot enthält mindestens drei Getreidearten, ist oft mit Körnern bestreut und muss trotzdem kein Vollkornbrot sein. Wie heißt es? → Mehrkornbrot
- bread-and-baked-goods-12: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Er hat die Lehre und die Gesellenprüfung hinter sich, eine weitere Prüfung bestanden und darf nun Lehrlinge ausbilden. Wie heißt sein Titel? → Bäckermeister
- carnival-and-fairs-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Manche Jecken laufen im Karnevalszug in gleichen Kostümen ohne Wagen mit. Wie nennt man so eine Gruppe? → Fußgruppe
- childrens-tv-and-audio-dramas-12: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: In der SWR-Serie „Tiere bis unters Dach“ zieht eine Familie aus Hamburg in ein Dorf voller Tiere. In welcher Gegend liegt es? → Schwarzwald
- dialects-and-regional-words-6: hard fail: correct 5, unambiguous 3, no_giveaway 5, no_overlap 5: In welcher Stadt sagt man zu einem Mädchen im Dialekt „Mädle“? → Stuttgart
- dialects-and-regional-words-13: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Statt „Depp“ sagt man im Norden auch „Döskopp“. Was ist damit gemeint? → Dummkopf
- drinks-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In diesem Glas Mineralwasser steigen keine Bläschen auf. Wie bestellt man so ein Wasser in Deutschland? → Stilles Wasser
- drinks-15: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Ein Wirt bei München soll 1922 sein Bier mit einem Getränk gestreckt haben, und so entstand das Radler. Mit welchem? → Zitronenlimonade
- drinks-16: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welches dieser deutschen Mischgetränke enthält KEINE Cola? → Alsterwasser
- empire-weimar-and-nazi-era-6: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Sie tagte ab Februar 1919 im Weimarer Nationaltheater, erstmals saßen Frauen darin, und sie beschloss die Verfassung. Wie hieß sie? → Nationalversammlung
- empire-weimar-and-nazi-era-8: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Marlene Dietrich lehnte Angebote der Nazis ab, wurde 1939 US-Bürgerin und reiste im Krieg an die Front. Für wen sang sie dort? → Für amerikanische Soldaten
- empire-weimar-and-nazi-era-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Gottlieb Daimler baute 1885 mit Wilhelm Maybach dieses Fahrzeug mit Holzrädern. Als was gilt es heute? → Als erstes Motorrad
- family-customs-and-dress-14: overlap like holidays-through-the-year-1: Bei der Silberhochzeit hängt ein Kranz an der Tür, es gibt silberne Geschenke und manchmal ein zweites Jawort. Wie lange ist das Paar verheiratet? → 25 Jahre: Für 25 Ehejahre steht Silber, für 50 Jahre Gold. Nach welchem Material ist das Jubiläum nach 60 Ehejahren benannt? → Diamant
- holidays-through-the-year-4: overlap like q-9143: Viele Kinder putzen am 5. Dezember ihre Stiefel und stellen sie vor die Tür. Wofür? → Damit der Nikolaus sie füllt: Wer ist dieser Mann, der im Dezember mit Bischofsstab und goldenem Buch zu den Kindern kommt? → Nikolaus
- holidays-through-the-year-8: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: Unter welchem Spitznamen ist Christi Himmelfahrt in Deutschland bekannt? → Vatertag
- legends-and-figures-7: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: „Der Sage nach rettete ich im Morgenland ein Tier vor einem Drachen. Es folgte mir treu bis nach Braunschweig.“ Wer bin ich? → Heinrich der Löwe
- national-symbols-and-state-15: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Ich bin fast 115 Meter hoch, war Bonns Abgeordnetenhochhaus und beherberge heute die UNO. Mein Spitzname nennt einen Bundestagspräsidenten. Wie heiße ich? → Langer Eugen
- parks-weather-and-climate-2: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Polarlichter waren im Mai 2024 sogar in Bayern zu sehen. In welchem Bundesland sieht man sie am häufigsten? → Schleswig-Holstein
- plants-and-forests-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Sie wächst am Wegrand, Raupen fressen sie gern, und anfassen sollte man sie lieber nicht. Was sitzt auf ihren Blättern? → Winzige Brennhaare
- reformation-to-empire-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Justus von Liebig lehrte in Gießen Chemie und empfahl ab 1840 Kali- und Phosphatsalze. Wozu dienten diese Salze? → Zum Düngen der Felder
- regional-dishes-1: overlap like sausages-and-cheese-17: Ein Metzger lernte in einer deutschen Stadt sein Handwerk, zog nach Wien und erfand dort das Wiener Würstchen. In welcher Stadt hatte er gelernt? → Frankfurt am Main: Nach der Hauptstadt des Landes auf der Karte sind beliebte Würstchen benannt. Welche Stadt ist es? → Wien
- regional-dishes-5: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Was bedeutet der lateinische Ursprung des Wortes „Karneval“ vermutlich? → Fleisch wegnehmen
- sausages-and-cheese-0: duplicate like q-9280: Dieses Fossil ist ein Archaeopteryx. In welchem Bundesland wurden alle bekannten Exemplare gefunden? → Bayern: Dieses warme Brötchen gibt es beim Metzger auf die Hand. In welchem Bundesland ist es ein echter Imbiss-Klassiker? → Bayern
- school-and-education-9: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Viele Grundschulkinder in Deutschland machen für dieses Ding einen eigenen „Führerschein“. Was dürfen sie danach? → mit dem Füller schreiben
- winter-sports-14: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Vervollständige: Ein Skipass ist eine Karte, mit der du im Skigebiet … → die Lifte benutzen darfst
- sausages-and-cheese-14: overlap like q-9451: Beim Bäcker kaufst du ein dunkles, kräftiges Brot mit Sauerteig. Aus welchem Getreide ist es meistens? → Roggen: Aus welchem Getreide wird klassisches Knäckebrot wie dieses gebacken? → Roggen
- sausages-and-cheese-17: overlap like q-12983: Diese dünnen Würstchen erwärmt man in heißem Wasser. Sie heißen nach der Stadt mit Deutschlands höchsten Wolkenkratzern. Welcher? → Frankfurt: Ein Metzger lernte in einer deutschen Stadt sein Handwerk, zog nach Wien und erfand dort das Wiener Würstchen. In welcher Stadt hatte er gelernt? → Frankfurt am Main
- series-and-crime-0: overlap like q-10875: In Janoschs Geschichten zieht der kleine Tiger sie an einer Schnur hinter sich her. Wie heißt das gelb-schwarz gestreifte Holztier auf Rädern? → Tigerente: Die Kindershow läuft seit 1996 im Ersten und im KiKA, Schulklassen spielen gegeneinander, das Maskottchen stammt von Janosch. Wie heißt sie? → Tigerenten Club
- series-and-crime-12: overlap like q-10890: Wer spielt im Münsteraner „Tatort“ den eitlen Rechtsmediziner Professor Karl-Friedrich Boerne? → Jan Josef Liefers: Wer den Münster-Tatort schaut, kennt Professor Boerne. In welchem Fach der Medizin arbeitet er? → Rechtsmedizin
- winter-sports-2: fact-check wrong: Hoppe won only the two-man gold in 1984. The four-man gold went to Bernhard Lehmann's GDR-I sled, and Hoppe took silver. The question's premise (both events) is false; Meinhard Nehmer did that in 1976.: Wer steuerte 1984 in Sarajevo die DDR-Bobs sowohl im Zweier als auch im Vierer zu Olympiagold? → Wolfgang Hoppe
