# batch-28

Made by `qgen batch` on 2026-10-29 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): states-and-capitals, cities-and-towns, rivers-lakes-and-coasts, mountains-and-landscapes, sights-and-landmarks, native-animals, plants-and-forests, parks-weather-and-climate, early-history, reformation-to-empire, empire-weimar-and-nazi-era, federal-republic-and-reunification, chancellors-and-presidents, inventors-and-scientists, founders-and-entrepreneurs, regional-dishes, sausages-and-cheese, bread-and-baked-goods, cakes-and-sweets, drinks, advent-and-christmas, carnival-and-fairs, holidays-through-the-year, family-customs-and-dress, legends-and-figures, superstitions-and-folk-beliefs, schlager-and-folk-music
- Merged: 367 (q-9120…q-9486)
- Approved: 343
- Needs work: 24
- Dropped by the pipeline: 39
- Reviewed by: claude-opus-5-5
- Claude calls: 723, about $90.42 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-26, batch-27; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-26 | batch-27 | batch-28 |
|---|---|---:|---:|---:|
| source locale |  | en | en | de (first de batch) |
| drafts |  | 412 | 337 | 406 |
| skipped slots |  | 92 | 113 | 80 |
| dropped |  | 85 | 50 | 39 |
| drop rate | ≤ 20.0 % | 20.6 % ✗ | 14.8 % ✓ | 9.6 % ✓ |
| dropped: hard fail correct |  | 0 | 3 | 0 |
| dropped: hard fail unambiguous |  | 0 | 2 | 0 |
| dropped: hard fail no_giveaway |  | 19 | 14 | 20 |
| dropped: overlap |  | 65 | 30 | 17 |
| dropped: duplicate |  | 1 | 1 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 2 |
| merged |  | 327 | 287 | 367 |
| approved |  | 302 | 261 | 343 |
| needs_work |  | 25 | 26 | 24 |
| needs_work rate | ≤ 20.0 % | 7.6 % ✓ | 9.1 % ✓ | 6.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.1 % ✓ | 3.5 % ✓ | 0.8 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.6 % ✓ | 0.0 % ✓ | 1.1 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.5 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.5 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.3 % ✓ | 5.6 % ✓ | 4.4 % ✓ |
| media: no pick in review 1 |  | 50 | 34 | 52 |
| media: recovered by research |  | 36 | 27 | 40 |
| media: no pick at record |  | 14 | 8 | 12 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.9 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 16.3 % ✓ | 9.5 % ✓ | 4.7 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 74.3 % ✓ | 68.1 % ✓ | 74.0 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.71 ✗ | 2.14 ✗ |
| approved 11–15 |  | 62 | 49 | 64 |
| top move | ≤ 25.0 % | 16.2 % ✓ | 17.1 % ✓ | 16.1 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 76.1 % | 77.7 % | 79.0 % |
| values stimulus |  | 5 | 5 | 6 |
| top clue | ≤ 60.0 % | 44.6 % ✓ | 48.1 % ✓ | 51.5 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 31.5 % ✓ | 30.3 % ✓ | 25.9 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 15.3 % ✓ | 15.7 % ✓ | 24.0 % ✓ |
| values lens |  | 11 | 10 | 11 |
| media share | 15.0 %–50.0 % | 23.9 % ✓ | 22.3 % ✓ | 21.0 % ✓ |
| mean fun | ≥ 3.40 | 3.61 ✓ | 3.65 ✓ | 3.55 ✓ |
| cost $ |  | $78.80 | $69.16 | $87.70 |
| $ per approved | ≤ $0.35 | $0.26 ✓ | $0.26 ✓ | $0.26 ✓ |
| calls |  | 627 | 549 | 663 |
| calls per approved |  | 2.08 | 2.10 | 1.93 |
| wall time h |  | 2.56 | 2.25 | 3.58 |
| days |  | 1 | 2 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 56 (0 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 8 (1 major), fact 1 (0 major), ambiguity 1 (0 major), overlap 1 (1 major), media 1 (1 major), difficulty 3 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 3 of 60 (5 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.72

Major findings on approved questions:

None.

## Needs work

- **q-9130** (bread-and-baked-goods) Wenn jemand dauernd stört, sagt man: „Du gehst mir auf den …“ Wie geht der Satz weiter? → Keks: No candidate fits: 1 is a US congressional press conference, 2 is explicit adult content (a chastity device, which must never be used), 3 and 4 are a roadside memorial and statues at a California lodge, and 5 is an Indian clean-water poster covered in text. A new search isn't allowed, so the media slot needs a new decorative query, for example "cookies on plate" or "biscuit crumbs". No suitable picture found for this question.
- **q-9132** (bread-and-baked-goods) Ich bin ein Mehl und mache Brot dunkel und kräftig. Ohne Sauerteig klappt es mit mir kaum, und aus mir wird Pumpernickel. Welches Mehl bin ich? → Roggenmehl: This asks the same fact as related draft q-9451 ("dark, strong bread with sourdough: which grain?" → Roggen). Seeing one gives the other away, so only one of the two should stay in the pool.
- **q-9136** (bread-and-baked-goods) Kokosmakronen backt man oft auf einer dünnen weißen Scheibe wie hier. Wofür ist sie da? → Damit sie nicht am Blech kleben: No candidate shows coconut macaroons on Oblaten wafers, and the question depends on that picture ("wie hier"). Candidate 1 shows French macarons on gelato cones. Candidates 2–6 are old book scans: a soap ad, a nutrition chart, a kitchen exhibit, a camp scene and a market painting. No new search is allowed, so the slot needs a sourced photo of Kokosmakronen on Oblaten, or the question needs to drop the essential image. No suitable picture found for this question.
- **q-9140** (cakes-and-sweets) Welches Gebäck backt man in diesem Gerät? → Waffeln: The question needs an essential photo of an open, empty heart-shaped waffle iron, but none of the candidates shows one: two are archaeological thimbles and one is an old book illustration of a dragon. A new search isn't allowed, so the image has to be found another way, for example by searching Commons for "Waffeleisen" or "heart waffle iron". No suitable picture found for this question.
- **q-9143** (cakes-and-sweets) Kinder putzen diese Stiefel am 5. Dezember und stellen sie vor die Tür. Wofür? → Damit der Nikolaus sie füllt: The picked picture has an unsuitable licence (pd-us-only: PD-1923, PD-US-expired).
- **q-9176** (cities-and-towns) Dieses weiße Gebäude steht am Hafen von Stralsund. Was gibt es darin? → Große Aquarien mit Meerestieren: None of the essential-image candidates shows the Ozeaneum in Stralsund. They are harbours in Heimaey, Lindau, Hong Kong, a US Navy ship, Chicago and Reykjavík. No new search is allowed, so the slot needs a new search such as "Ozeaneum Stralsund exterior", using a shot where the lettering is hidden or can't be read. No suitable picture found for this question.
- **q-9181** (cities-and-towns) Norderney liegt in Ostfriesland und ist seit 1797 Seebad. Was bedeutet die Endung „-ney“ im Namen der Insel? → Neu: The etymology is disputed. The common explanation is „Norder neye Oog“ („Norders neue Insel“), so the ending „-ney“ mixes „neu“ (new) and „ey/oog“ (island). That makes both „Neu“ and an answer like „Insel“ defensible, and the fact check rated it wrong. Hint 3 („Gegenteil von alt“) gives the answer away. The question also opens with unneeded padding (Ostfriesland, Seebad since 1797). A niche place-name fact like this is likely above difficulty 9. Either drop the question or rebuild it around a clearly settled fact. Fact check: wrong. "-ney" (Norder-ey, ostfriesisch 'oog/ey') means 'Insel' (Aue/Eiland), not 'Neu'. Norderney is simply 'nördliche Insel'. The hints ('Gegenteil von alt') are wrong too.
- **q-9197** (early-history) Dieses Denkmal erinnert an den Sieg der Germanen über den Römer Varus. In welchem Gebirge steht es? → Teutoburger Wald: The fun fact says the Hermannsdenkmal was the tallest statue in the world until 1886. That is false: the Leshan Giant Buddha (about 71 m, 8th century) and the Bamiyan Buddhas were taller. The record only holds for the "western world". Also, the 53 m is the total height including the pedestal, not "with the sword" alone (the figure with its sword is about 26,6 m). Rewrite the fun fact, for example: total height about 53 m with the pedestal, tallest statue in the western world until the Statue of Liberty in 1886.
- **q-9208** (empire-weimar-and-nazi-era) In den Zwanzigern trugen viele junge Frauen einen „Bubikopf“. Was war das? → eine kurze Frisur: The picked picture has an unsuitable licence (pd-us-only: PD-US-expired).
- **q-9225** (family-customs-and-dress) Zu welchem Anlass klappern solche Dosen hinten am Auto? → Hochzeit: None of the candidates shows cans tied behind a car: they are a bike carriage on Caltrain and old street-railway journal scans of trams. The question says "solche Dosen", so it needs an essential image of that exact thing, and no new search is allowed. It needs a hand-picked photo of tin cans on strings behind a car, with no "Just Married" sign. The alternative is to reword it so it doesn't point at a picture. No suitable picture found for this question.
- **q-9322** (plants-and-forests) Im Harz und im Schwarzwald stehen riesige Fichtenwälder. Was für ein Baum ist die Fichte? → Nadelbaum: Hint 1 is out of date. It says the spruce is the most common tree in German forests, but the fourth Bundeswaldinventur (2022 data, published 2024) found the Kiefer at about 22 % and the Fichte at about 21 %, so the pine now ranks first. Change hint 1, for example to "Sie ist einer der häufigsten Bäume in deutschen Wäldern." or a vague hint about forestry or timber. The rest of the question and the media pick are fine.
- **q-9336** (reformation-to-empire) Im Unterricht liest du die Ballade vom „Zauberlehrling“, der einen Besen Wasser holen lässt. Wer hat sie geschrieben? → Johann Wolfgang von Goethe: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-9367** (states-and-capitals) Welches Bundesland zeigt diese Karte? → Baden-Württemberg: None of the candidates is an unlabelled outline of today's Baden-Württemberg. Candidates 1, 2, 3 and 6 are historical atlas maps with titles naming Württemberg and Baden, which give the answer away. Candidate 5 shows the 1442 county of Württemberg, and candidate 4 highlights the Black Forest on a map of Germany. A new search isn't allowed, so the slot needs a hand-picked file, such as a blank locator map of Baden-Württemberg from Commons. No suitable picture found for this question.
- **q-9390** (drinks) Dieses schlichte Bierglas wurde in den 1950ern entworfen und steht bis heute in fast jeder deutschen Kneipe. Wie heißt es? → Willi-Becher: Fact check: wrong. The answer is fine, but hint 3 is misleading. The glass is said to be named after its designer Willy Steinmeier (Ruhrglas, 1954), not as a generic short form of Wilhelm. That origin comes from a single blog source and I couldn't cross-check it. The 'designed in the 1950s' claim is also only loosely supported: museum items are dated 1940–1980.
- **q-9397** (family-customs-and-dress) Ein Tischler baut Schränke, Tische und Türen. Mit welchem Material arbeitet er vor allem? → Holz: No candidate fits as the decorative image. #1 is a wrought-iron 'Schlossermeister' sign, which points to the wrong option Metall. #2–4 are leather sailmaker's palm guards (wrong option Leder). #5 is a metal thimble and #6 is a drawing of a Roman figurine. A new search for a carpenter's workshop (e.g. 'woodworking workbench tools') is needed. The question text itself is fine. No suitable picture found for this question.
- **q-9400** (family-customs-and-dress) Beim feierlichen Baustart eines Hauses kommen Tageszeitung, Münzen und Baupläne in eine Metallkapsel. Wohin kommt sie? → In den Grundstein: The picked picture has an unsuitable licence (pd-us-only: PD-US-no notice).
- **q-9412** (mountains-and-landscapes) Welcher deutsche Wintersportort liegt NICHT in Bayern? → Winterberg: The clue „deutscher Wintersportort, der NICHT in Bayern liegt“ fits many real places besides Winterberg: Oberhof, Willingen, Altenberg, Feldberg, Braunlage. So the answer only works within the four options, which the house style rules out ("the clue must point to the answer in the real world"). Rework it as a direct question with a clue only Winterberg has, e.g. the winter sports centre of the Sauerland with a bobsleigh track.
- **q-9432** (rivers-lakes-and-coasts) Was ist auf diesem Foto zu sehen? → Schleuse: No candidate shows a lock clearly. 1 and 2 are scratched, faded black-and-white scans of the Miami and Erie Canal where you can't make out the lock chamber or gates, and 3 and 4 are photos of a WWII seaplane. A fresh search for a modern colour photo of a lock chamber with its gates and a ship inside is needed (e.g. "Schleuse Kiel-Holtenau" or "canal lock gates ship"). No suitable picture found for this question.
- **q-9435** (sausages-and-cheese) Quark steht in Deutschland in fast jedem Kühlschrank. Zu welcher Käsegruppe zählt er? → Frischkäse: The text is fine, but the media slot has no candidates and another search isn't allowed. The question needs an illustrative image of quark in a bowl (e.g. try "quark cheese bowl" or "Speisequark") from a manual or later search. No suitable picture found for this question.
- **q-9451** (sausages-and-cheese) Beim Bäcker kaufst du ein dunkles, kräftiges Brot mit Sauerteig. Aus welchem Getreide ist es meistens? → Roggen: This repeats draft q-9132, which asks the same thing: dark, strong sourdough bread is made from rye, and Pumpernickel comes from it. Both questions even use the same Pumpernickel clue, so seeing one gives away the other. Keep only one of the two.
- **q-9454** (schlager-and-folk-music) Im Kinderlied „Grün, grün, grün sind alle meine Kleider“ trägt man Grün wegen des Berufs vom Schatz. Was ist der Schatz? → Jäger: The text is fine, but none of the media candidates work. The slot needs green clothes, for example on a washing line, with no person in the picture. No candidate shows that, and no new search is possible. The role should also be illustrative rather than essential, since the question works without the image. No suitable picture found for this question.
- **q-9467** (states-and-capitals) Welcher Fluss fließt mitten durch Berlin? → Spree: None of the media candidates shows Berlin or a river. They are US riverbank buildings, shop fronts (Staples, Burlington), black-and-white interiors and an old sketch, and no new search is allowed. The slot needs a new search such as "Reichstag Berlin river" or "Berlin Museum Island boat". The question text itself is fine. No suitable picture found for this question.
- **q-9468** (states-and-capitals) Ich staune mit „Ei verbibbsch!“, sage „nu“, wenn ich ja meine, und aus Kaffee wird bei mir „Gaffee“. Welcher Dialekt bin ich? → Sächsisch: Hint 1 („im Osten Deutschlands“) gives the answer away: Bairisch, Schwäbisch and Kölsch are all clearly southern or western, so the first hint alone picks out Sächsisch. Hint 2 (Elbsandsteingebirge) is almost as strong. Hint 1 should stay vague, e.g. about how the dialect is often teased or ranked in dialect polls, without giving the region.
- **q-9469** (states-and-capitals) Welches Bundesland zeigt diese Karte? Das Loch in der Mitte ist kein Druckfehler. → Brandenburg: No candidate is the unlabelled outline map of Brandenburg with Berlin as a hole that the essential slot needs: all six are 19th-century atlas pages or wider maps, and several have „Brandenburg“ printed on them. Another search isn't allowed, so the slot needs a blank modern locator or outline map (e.g. a Commons 'Brandenburg location map' or blank map). Also, hint 2 („Das Loch ist die Hauptstadt Deutschlands“) does almost the whole reasoning step for the player, so it is close to a giveaway. Consider making it vaguer, for example: „Das Loch ist ein eigenes Bundesland.“ No suitable picture found for this question.

## Question axes

- move: analogy 7, cause_effect 30, count 7, estimate 4, identify 59, made_of 36, name_concept 36, odd_one_out 15, origin 31, purpose 35, record 5, sequence 14, when 25, who 29, word_meaning 34
- stimulus: detail 12, map_outline 3, none 290, photo 60, sound 1, video 1
- clue: completion 10, direct 189, riddle 24, scenario 37, three_facts 107
- answer_kind: group 49, number 11, person 51, place 48, thing 95, time 27, word 86
- lens: body_senses 3, educational_media 38, everyday 88, history 56, language 71, nature 25, pop_culture 30, popular_science 2, school 36, science_news 10, university 8

## Dropped by the pipeline

- carnival-and-fairs-16: overlap like q-0882: En las caricaturas, obligo a mis prisioneros a caminar por una tabla sobre el mar hasta que caen al agua. Tengo parche en el ojo y un loro en el hombro. ¿Quién soy? → Un pirata: Zu welchem Kostüm gehört diese Augenklappe? → Pirat
- early-history-4: overlap like q-3583: In the old poem Hávamál, Odin hangs from the world tree Yggdrasil for nine nights as a sacrifice. What does he win? → The runes: Im Museum siehst du einen Stein mit Runen. Welcher Gott hat diese Schrift laut germanischer Sage gefunden? → Odin
- empire-weimar-and-nazi-era-13: overlap like q-1076: Esta robot es María, de la película muda «Metrópolis» (1927). Su diseño inspiró a un robot muy famoso de otra saga del cine. ¿Cuál? → C-3PO: Ich bin ein Stummfilm von Fritz Lang aus dem Jahr 1927 und zeige eine Stadt voller Hochhäuser und eine Roboterfrau namens Maria. Wer bin ich? → Metropolis
- federal-republic-and-reunification-2: overlap like q-9161: Mich wählt eine eigene Versammlung: alle Bundestagsabgeordneten und genauso viele Gesandte der Länder, oft auch Promis. Wer bin ich? → Bundespräsident: Ich wohne im Schloss Bellevue, unterschreibe Gesetze und werde alle fünf Jahre von der Bundesversammlung gewählt. Wer bin ich? → Bundespräsident
- federal-republic-and-reunification-4: overlap like federal-republic-and-reunification-2: Ich wohne im Schloss Bellevue, unterschreibe Gesetze und werde alle fünf Jahre von der Bundesversammlung gewählt. Wer bin ich? → Bundespräsident: Theodor Heuss war der erste Bundespräsident. Wie viele Jahre blieb er im Amt? → 10
- holidays-through-the-year-1: overlap like q-9143: Kinder putzen diese Stiefel am 5. Dezember und stellen sie vor die Tür. Wofür? → Damit der Nikolaus sie füllt: Ich komme in der Nacht zum 6. Dezember und fülle geputzte Stiefel mit Süßigkeiten. Wer bin ich? → Nikolaus
- inventors-and-scientists-1: overlap like q-3347: The company Thermos, which made vacuum flasks famous, was founded in Germany in which year? → 1904: Sie hält Tee stundenlang heiß oder Saft kalt, hat eine doppelte Wand mit Vakuum dazwischen und kam 1904 aus Berlin. Was ist es? → Thermoskanne
- inventors-and-scientists-16: overlap like q-4474: Robert Koch won the 1905 Nobel Prize for finding the germ behind it. It mainly attacks the lungs, and the BCG vaccine protects against it. What disease is it? → Tuberculosis: Welcher Arzt entdeckte 1882 in Berlin das Bakterium, das Tuberkulose auslöst? → Robert Koch
- mountains-and-landscapes-11: overlap like q-9169: Garmisch-Partenkirchen liegt an der Zugspitze, war 1936 Olympiaort und hat jedes Jahr an Neujahr ein Skispringen. Zu welcher Serie gehört es? → Vierschanzentournee: Es beginnt Ende Dezember in Oberstdorf, am Neujahrstag wird in Garmisch-Partenkirchen gesprungen, und der Gesamtsieger bekommt einen goldenen Adler. Wie heißt es? → Vierschanzentournee
- mountains-and-landscapes-12: overlap like q-9282: Die Vulkaneifel hat Maare, erloschene Vulkankegel und Quellen, aus denen Mineralwasser von selbst sprudelt. Welches Gas bringt es zum Sprudeln? → Kohlendioxid: Ich bin ein runder See in der Eifel. Kein Fluss schuf mich, sondern eine Dampfexplosion aus der Tiefe. Man nennt mich „Auge der Eifel“. Was für ein See bin ich? → Maar
- plants-and-forests-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Diese Wiesenblume hat blaue, nickende Blüten wie kleine Kelche. Ihr Name lautet „…blume“. Was fehlt? → Glocken
- reformation-to-empire-15: overlap like q-1822: Según la tradición de Pascua en muchos países, ¿qué personaje esconde estos huevos de colores? → El conejo de Pascua: Ein Heidelberger Arzt erwähnte mich 1682 zum ersten Mal, Auswanderer nahmen mich mit nach Amerika, und ich verstecke Dinge im Garten. Wer bin ich? → Osterhase
- advent-and-christmas-2: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: Heiligabend: Ein Glöckchen klingelt, und die Tür zum Weihnachtszimmer geht auf. Was kommt jetzt? → die Bescherung
- advent-and-christmas-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welche Holzfigur aus dem Erzgebirge hat am Rücken einen Hebel, der ihren großen Mund bewegt? → Nussknacker
- schlager-and-folk-music-13: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Auf jeder Hochzeit singt die Tanzfläche mit: „Atemlos durch die Nacht, bis ein neuer … erwacht.“ Was erwacht? → Tag
- sights-and-landmarks-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Was darf man im Serengeti-Park Hodenhagen machen, was in einem normalen Zoo nicht geht? → Mit dem Auto durch Tiergehege fahren
- sights-and-landmarks-11: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Du läufst im Europa-Park von Land zu Land. Welches Land passt NICHT zu den anderen? → Brasilien
- states-and-capitals-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welches Bundesland zeigt diese Karte? → Bayern
- cakes-and-sweets-9: fact-check wrong: The distractor 'Blumen und Sträußchen' is not clearly wrong. At the Cologne Rosenmontagszug, 'Strüßjer' (small flower bunches) are thrown along with Kamelle. The question says 'Was fliegt dann von den Wagen?', so two answers could fit.: Beim Rosenmontagszug im Rheinland rufen alle „Kamelle!“. Was fliegt dann von den Wagen? → Bonbons und Süßigkeiten
- cakes-and-sweets-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: „Wir suchen uns ein schattiges Plätzchen.“ Was bedeutet Plätzchen in diesem Satz? → Ein kleiner Ort
- carnival-and-fairs-8: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Woraus ist diese Maske der schwäbisch-alemannischen Fasnet gemacht? → Holz
- chancellors-and-presidents-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welche Partei bildet im Bundestag mit einer Schwesterpartei die „Union“, tritt aber nur in einem einzigen Bundesland zur Wahl an? → CSU
- cities-and-towns-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Diese Uhr auf dem Berliner Alexanderplatz ist ein beliebter Treffpunkt. Wie heißt sie? → Weltzeituhr
- early-history-3: hard fail: correct 4, unambiguous 5, no_giveaway 2, no_overlap 5: Es stand oft in alten Bauernstuben, man trat es mit dem Fuß an, und im Märchen macht Rumpelstilzchen daran Stroh zu Gold. Was ist das? → Spinnrad
- early-history-9: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Nürnberg, Frankfurt und Lübeck regierten sich im Mittelalter mit eigenem Rat und Gericht selbst. Wem unterstanden sie direkt? → Dem Kaiser
- family-customs-and-dress-10: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Wie heißt der Handwerker, der diesen Hutschmuck aus Bayern und Österreich aus Tierhaaren bindet? → Gamsbartbinder
- federal-republic-and-reunification-13: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Dieser US-Präsident sprach 1963 in West-Berlin. Welchen berühmten Satz sagte er dort auf Deutsch? → „Ich bin ein Berliner“
- holidays-through-the-year-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Die Fernsehsitzung „Mainz bleibt Mainz, wie es singt und lacht“ läuft seit 1955. Woraus besteht sie vor allem? → Büttenreden, Liedern und Gardetänzen
- holidays-through-the-year-7: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Brunnen wie diesen schmückt man in der Fränkischen Schweiz zu Ostern mit Tausenden bemalten Eiern. Was wird damit geehrt? → Das Wasser
- inventors-and-scientists-0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Er trägt den Namen eines Heidelberger Chemikers und steht in vielen Chemieräumen. Was ist ein Bunsenbrenner? → Ein Gasbrenner
- reformation-to-empire-12: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Um 1835 arbeiteten in vielen Fabriken auch Kinder. Welchen Kindern verbot Preußen 1839 die Fabrikarbeit ganz? → Kindern unter 9 Jahren
- regional-dishes-3: fact-check wrong: The fun fact is inaccurate. The Donauwelle's wave pattern comes from the dark and light dough layers with the sour cherries pressed in. It doesn't come from dragging a fork through the chocolate glaze. (Checked from memory, not by search.): Sie versteckt Sauerkirschen und trägt obendrauf ein Muster aus Schokolade. Was ist eine „Donauwelle“? → Blechkuchen
- rivers-lakes-and-coasts-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ich entspringe in der Senne, fließe durchs Münsterland nach Norden und trage riesige Kreuzfahrtschiffe aus Papenburg zur Nordsee. Welcher Fluss bin ich? → Ems
- sausages-and-cheese-9: overlap like sausages-and-cheese-13: Du kehrst im Schwarzwald zum „Vesper“ ein. Was kommt typischerweise auf den Tisch? → Brot, Speck, Wurst und Käse: Im Osten Deutschlands sagen viele „Brotbüchse“ zur Brotdose. Wie heißt sie oft in Schwaben? → Vesperdose
- rivers-lakes-and-coasts-11: overlap like q-9285: Auf den Halligen stehen die Häuser auf solchen Hügeln, damit sie bei „Land unter“ trocken bleiben. Wie heißt so ein Hügel? → Warft: Der Leuchtturm Westerhever steht auf einem künstlich aufgeschütteten Hügel, der vor Sturmfluten schützt. Wie heißt so ein Hügel? → Warft
- rivers-lakes-and-coasts-12: overlap like q-9281: Ich bin ein riesiger Stein auf einem Acker in Norddeutschland, stamme aber aus Skandinavien. Gletscher brachten mich her. Was bin ich? → Findling: Wer oder was hat vor langer Zeit die vielen Seen im Norden Deutschlands geformt? → Gletscher
- schlager-and-folk-music-1: overlap like q-3891: Nicole was 17 when she won Eurovision 1982 for Germany. It's still the last winner sung in German. Which song was it? → “Ein bisschen Frieden”: Mit so einer weißen Gitarre gewann 1982 erstmals jemand für Deutschland den Eurovision Song Contest. Wer? → Nicole
- sights-and-landmarks-5: overlap like q-9176: Dieses weiße Gebäude steht am Hafen von Stralsund. Was gibt es darin? → Große Aquarien mit Meerestieren: Was gibt es im Ozeaneum in Stralsund NICHT zu sehen? → Eisbären
- superstitions-and-folk-beliefs-16: overlap like q-9345: In Berlin bestellst du einen „Pfannkuchen“. Er ist in Fett gebacken, mit Marmelade gefüllt und gezuckert. Was bekommst du? → Einen Berliner: In Berlin heißt er Pfannkuchen, anderswo Berliner oder Krapfen. An Silvester ist einer oft heimlich fies gefüllt. Womit? → Senf
