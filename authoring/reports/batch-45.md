# batch-45

Made by `qgen batch` on 2026-11-06 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: germany
- Language: German
- Subcategories (27): films-and-actors, pop-and-rock, sayings-and-idioms, inventors-and-scientists, shows-and-presenters, native-animals, art-architecture-and-museums, gdr-history, superstitions-and-folk-beliefs, brands-and-products, state-and-city-emblems, gdr-everyday-life, drinks, home-and-public-life, carnival-and-fairs, childrens-tv-and-audio-dramas, rap-and-electronic, athletes-and-other-sports, winter-sports, slang-and-everyday-words, cakes-and-sweets, empire-weimar-and-nazi-era, national-team, states-and-capitals, rivers-lakes-and-coasts, mountains-and-landscapes, dialects-and-regional-words
- Merged: 256 (q-13963…q-14218)
- Approved: 223
- Needs work: 33
- Dropped by the pipeline: 52
- Reviewed by: claude-opus-5-5
- Claude calls: 556, about $79.28 at list price
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-43, batch-44; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-43 | batch-44 | batch-45 |
|---|---|---:|---:|---:|
| source locale |  | es | en | de |
| drafts |  | 343 | 305 | 308 |
| skipped slots |  | 179 | 145 | 178 |
| dropped |  | 100 | 61 | 52 |
| drop rate | ≤ 20.0 % | 29.2 % ✗ | 20.0 % ✓ | 16.9 % ✓ |
| dropped: hard fail correct |  | 0 | 1 | 0 |
| dropped: hard fail unambiguous |  | 2 | 2 | 0 |
| dropped: hard fail no_giveaway |  | 25 | 17 | 11 |
| dropped: overlap |  | 73 | 43 | 40 |
| dropped: duplicate |  | 1 | 0 | 1 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 243 | 244 | 256 |
| approved |  | 224 | 221 | 223 |
| needs_work |  | 19 | 23 | 33 |
| needs_work rate | ≤ 20.0 % | 7.8 % ✓ | 9.4 % ✓ | 12.9 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.5 % ✓ | 0.4 % ✓ | 3.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.8 % ✓ | 0.8 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.4 % ✓ | 0.4 % ✓ | 0.4 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.5 % ✓ | 7.4 % ✓ | 9.0 % ✓ |
| media: no pick in review 1 |  | 43 | 26 | 44 |
| media: recovered by research |  | 34 | 17 | 28 |
| media: no pick at record |  | 9 | 9 | 16 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.4 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 21.9 % ✗ | 14.4 % ✓ | 13.6 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | 53.0 % ✗ | 59.8 % ✓ | 57.6 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 2.67 ✗ | 1.15 ✓ |
| approved 11–15 |  | 52 | 44 | 47 |
| top move | ≤ 25.0 % | 19.8 % ✓ | 13.5 % ✓ | 14.5 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 68.7 % | 85.2 % | 78.1 % |
| values stimulus |  | 6 | 5 | 6 |
| top clue | ≤ 60.0 % | 49.4 % ✓ | 39.3 % ✓ | 43.0 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 22.6 % ✓ | 26.6 % ✓ | 26.6 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 19.3 % ✓ | 20.9 % ✓ | 18.8 % ✓ |
| values lens |  | 11 | 11 | 11 |
| media share | 15.0 %–50.0 % | 31.3 % ✓ | 14.8 % ✗ | 21.9 % ✓ |
| mean fun | ≥ 3.40 | 3.50 ✓ | 3.54 ✓ | 3.46 ✓ |
| cost $ |  | $71.96 | $65.01 | $75.76 |
| $ per approved | ≤ $0.35 | $0.32 ✓ | $0.29 ✓ | $0.34 ✓ |
| calls |  | 489 | 480 | 496 |
| calls per approved |  | 2.18 | 2.17 | 2.22 |
| wall time h |  | 2.10 | 1.79 | 1.92 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✓ pass |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 52 (0 %)
- Major among review needs work: 5 of 8 (62 %)
- Problems by kind: giveaway 6 (1 major), fact 2 (0 major), ambiguity 1 (0 major), overlap 1 (0 major), media 8 (5 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.52

Major findings on approved questions:

None.

## Needs work

- **q-13976** (athletes-and-other-sports) Isabell Werth holte 2024 in Paris noch Olympia-Gold im Dressurreiten. In welchem Jahrzehnt gewann sie ihr erstes? → 1990er-Jahre: Fact check: wrong. The premise is false. In Paris 2024 Werth won silver (team and individual), not gold. Her first gold, Barcelona 1992 team, is correct.
- **q-13985** (athletes-and-other-sports) Ich kam aus Niedersachsen, gewann 1934 und 1936 in Paris und stand dreimal in Folge im Wimbledon-Finale. Wer bin ich? → Gottfried von Cramm: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-13994** (cakes-and-sweets) Diese gelbe Plastikkapsel mit einem kleinen Spielzeug drin steckt in welcher Süßigkeit? → Überraschungsei: No candidate works for the essential image. #1 shows the capsule inside a broken chocolate egg, which shows the answer, and the capsule there is clear rather than yellow. #2 and #3 show Japanese gashapon capsules and vending machines, and #4 is an engraving of a shotgun. No new search is possible. Separately, hint 2 ("Ihre Form passt besonders gut zu Ostern") points straight to the only egg among the options, so it gives the answer away too early; it should be swapped with a vaguer hint. No suitable picture found for this question.
- **q-14002** (carnival-and-fairs) Diese Kölner Band gibt es seit 1972, sie sang „Viva Colonia“, und ihr Name ist Kölsch. Was bedeutet er auf Hochdeutsch? → Hühner: The description says the Höhner sing "nur auf Kölsch". That's false: many of their songs are in standard German, including "Wenn nicht jetzt, wann dann?", the song the fun fact itself names. Hint 2 also gives the answer away, because the breakfast-table "what they deliver" points straight to eggs, so only Hühner fits among the four options. The description should play on Cologne or carnival without the false claim, and hint 2 should be vaguer, for example a hint about the band's mascot or the sound of the name.
- **q-14006** (dialects-and-regional-words) Ich begrüße dich mit „Ei gude wie?“ und trinke am liebsten Apfelwein aus dem gerippten Glas. Wer bin ich? → Ein Hesse: The picked picture has an unsuitable licence (pd-no-reason: public domain without a template).
- **q-14007** (dialects-and-regional-words) Ich komme jedes Jahr wieder, und wenn ich gehe, singen Kinder mir nach: „… ade, Scheiden tut weh“. Wer bin ich? → Der Winter: Fact check: uncertain. The line 'Sommer ade, Scheiden tut weh' is, as far as I know, also a real children's song. I could not confirm that with a search. If it exists, the question stem alone fits both winter and summer, so 'Der Sommer' may not be clearly wrong. Only the hint about Schneeglöckchen and Krokusse settles it.
- **q-14019** (empire-weimar-and-nazi-era) Diese Frau sprach am 19. Februar 1919 als erste Frau in der Weimarer Nationalversammlung und gründete die Arbeiterwohlfahrt. Wer ist sie? → Marie Juchacz: None of the essential-image candidates works: every one carries the name „Marie Juchacz“ (medal inscription, monument lettering, street sign, plaque), and none is the plain portrait the note asks for. No new search is allowed. Switch the slot to an illustrative or decorative image without her name, for example the Weimar Nationaltheater, where the Nationalversammlung met. Also consider rewriting the description: it quotes her famous opening line, which identifies her to anyone who knows it. No suitable picture found for this question.
- **q-14025** (films-and-actors) Dieser Lehmriese stammt aus dem Stummfilm „Der Golem, wie er in die Welt kam“ von 1920. Wer spielte ihn und führte zugleich Regie? → Paul Wegener: None of the candidates is usable for the essential slot. The question says „Dieser Lehmriese“, so it needs a still of Wegener in his Golem costume. Candidate 1 is the film poster, and it prints „Paul Wegener“ in large letters, which gives the answer away. Candidate 2 is a film still, but it shows Rabbi Löw and Miriam, not the Golem. Candidates 3–6 are modern figurines, a stage play and a computer labelled GOLEM. No new search is allowed, so either source a clean film still showing only the Golem, or change the role to illustrative/decorative and reword the question so it no longer refers to a picture. No suitable picture found for this question.
- **q-14030** (films-and-actors) Dieser Literaturkritiker sollte 2008 den Deutschen Fernsehpreis fürs Lebenswerk bekommen und lehnte ihn auf der Bühne ab. Wer ist er? → Marcel Reich-Ranicki: No candidate is usable for this slot, and a new search isn't allowed. Candidates 1 and 4 are plaques that print his name and give the answer away. 2 is a sculpture of his face, which also gives it away. 3 and 5 show a school building that has nothing to do with the question. 6 is a Stolperstein for his mother that mentions deportation and murder, which is not family-friendly. The slot is also set up wrong: the question doesn't ask about a picture, so an 'essential' portrait would only reveal the answer. Change the slot to illustrative or decorative with a query like 'television award stage' or 'stack of books'. No suitable picture found for this question.
- **q-14033** (gdr-everyday-life) Dieses knusprige Gebäck aus Eiweiß, Zucker und Kakao hat die Form von Buchstaben und wurde in der DDR in Dresden gebacken. Wie heißt es? → Russisch Brot: The fun fact names the wrong baker. The Russisch Brot legend credits the Dresden baker Ferdinand Wilhelm Hanke (around 1844/45), not "Ferdinand Wendler" (Wendler is the name linked to the Dominostein). Fix: replace the fun fact with the fact check's correction, which credits Hanke and says around 1845. Fact check: wrong. The fun fact names the wrong baker. Sources attribute the St. Petersburg recipe to the Dresden baker Ferdinand Wilhelm Hanke (about 1845). Herbert Wendler is linked to the Dominostein, not to Russisch Brot.
- **q-14045** (gdr-history) Die US-Bürgerrechtlerin auf dem Foto wurde 1973 bei den Weltfestspielen der Jugend in Ost-Berlin wie ein Star gefeiert. Wer ist sie? → Angela Davis: The picked picture has an unsuitable licence (pd-us-only: PD-US-no notice).
- **q-14050** (gdr-history) Dieses blaue Halstuch auf dem Foto trugen viele Schulkinder in der DDR. Zu welcher Organisation gehörte es? → Junge Pioniere: No adequate essential image: the question needs a photo of schoolchildren wearing the blue Pioneer neckerchief, but the candidates are an adult (Grotewohl) at a 1951 camp, a cyclist in 1955 and a 1944 Atlantic Wall bunker, all black-and-white, so the blue can't be seen. A colour photo of Jungpioniere with blue neckerchiefs is needed, without text that names the organisation. No suitable picture found for this question.
- **q-14053** (gdr-history) Die Frau auf dem Foto war von 1963 bis 1989 Ministerin für Volksbildung der DDR. Wer ist sie? → Margot Honecker: No candidate is a clear portrait of Margot Honecker: they're all crowded Bundesarchiv group scenes, and in several it isn't clear which woman "die Frau auf dem Foto" is. Candidate 4 even centres on Lotte Ulbricht, who is one of the wrong answers. A new search isn't allowed, so this needs a usable portrait (e.g. Bundesarchiv Bild 183-1986-0421-030 or a similar head shot). No suitable picture found for this question.
- **q-14056** (home-and-public-life) Beim Stoßlüften reißt man die Fenster für einige Minuten weit auf, statt sie lange zu kippen. Wozu? → Damit feuchte Luft rausgeht, aber die Wände warm bleiben: No candidate shows an open window or a room being aired. 1 is a rusty padlock on a window sill, 2–4 and 6 are black-and-white US building surveys with closed windows, and 5 is a bunker interior. No new search is allowed, so the media slot can't be filled. A note on the text too: the distractor „Damit beschlagene Fensterscheiben schnell trocknen“ is close to defensible, because airing does remove the moisture that fogs the panes. It would be better replaced with a reason clearly unrelated to moisture. No suitable picture found for this question.
- **q-14063** (inventors-and-scientists) Ein ausgewanderter Mechaniker soll in New York schon vor Edison Glühlampen wie diese gebaut haben. Aus welcher Stadt bei Hannover stammte er? → Springe: The picked picture has an unsuitable licence (pd-us-only: PD-US).
- **q-14078** (native-animals) Hör zu: Das ist ein männliches Tier aus dem deutschen Wald. Wie nennt man es in der Jägersprache? → Keiler: No usable audio: candidates 1–3 are domestic pig grunts under one second long (the note rules out domestic pigs), 4 and 6 are spoken words, and 5 ('En-uk-wild boar.ogg') is someone saying 'wild boar', which gives the answer away. The background candidates are book scans (a leaf drawing and a magazine page), not a forest floor. No new search is allowed, so this needs a real wild boar recording, such as one from Freesound, and a forest background photo, or else a switch to an illustrative wild boar image with the wording changed. No suitable picture found for this question. No suitable background picture found.
- **q-14082** (native-animals) Hör zu: Welcher Vogel singt hier im Garten? → Amsel: The question text and the audio are fine, but none of the background candidates shows a garden. 1 and 2 are the ESO Paranal desert at dusk, 3 is a California rooftop park with palm trees and skyscrapers, and 4 is a street of skyscrapers. The background needs a new search for something like "German garden lawn" or "suburban garden morning". No suitable background picture found.
- **q-14090** (pop-and-rock) Wer saß bei „Deutschland sucht den Superstar“ seit 2002 in den meisten Staffeln in der Jury? → Dieter Bohlen: The description says „dieser Mann“, which rules out Heidi Klum before any hint is shown. It also comes close to naming the answer's defining trait: being the juror candidates feared. Rewrite it so it plays on the casting-show theme without mentioning gender or the harsh judging. One option is to replace Heidi Klum with a male distractor, but the description should still avoid the „gefürchtet“ trait.
- **q-14099** (athletes-and-other-sports) Welche Deutsche wurde 2021 in Tokio in dieser Disziplin Olympiasiegerin? → Malaika Mihambo: The picked picture is broken at the source (truncated (Premature end of JPEG file)).
- **q-14103** (cakes-and-sweets) Die Waffel mit Nuss-Nougat-Creme gibt es seit 1959, und ihr Name „Hanuta“ ist eine Abkürzung. Wofür? → Haselnusstafel: Hint 2 ("Das zweite Wort hängt auch in fast jedem Klassenzimmer an der Wand") points to "Tafel" and is the only fit among Taler/Torte/Tüte/Tafel, so it gives the answer away. Hint 2 should be vaguer, e.g. about the shape of the product (flat, rectangular) without naming the school blackboard.
- **q-14106** (carnival-and-fairs) An der Losbude rollst du dein Los auf und liest „Niete“. Was bedeutet das? → Du hast nichts gewonnen: No candidate shows a fairground lottery booth (Losbude). The candidates are US state-lottery counters, Korean school signage, a classroom and a Thai night-market vendor selling printed lottery tickets. Another search isn't allowed. The question text itself is fine. A new search such as "Losbude Kirmes" or "Lostrommel Jahrmarkt" should find a usable picture. No suitable picture found for this question.
- **q-14124** (gdr-everyday-life) Du liest eine alte DDR-Speisekarte: „Broiler“ ist zu Brathähnchen wie „Sättigungsbeilage“ zu …? → Kartoffeln, Reis oder Nudeln: No candidate shows what the question names, an old GDR menu. They are modern menus: an Italian dessert menu (1, 2), an English fine-dining menu (3), a Kenyan menu (4), a Chinese wedding menu (5) and an English chalkboard (6). Candidate 1 also shows puddings and ice cream, which points to a wrong option. No new search is allowed, so the media slot needs a GDR menu (e.g. "DDR Speisekarte HO Gaststätte") or a different illustrative subject such as a GDR canteen meal. No suitable picture found for this question.
- **q-14143** (rap-and-electronic) Vor Berliner Techno-Clubs wie dem Berghain entscheidet diese Person, wer rein darf. Wer ist das? → Türsteher: The text is fine, but no image candidate shows the Berghain, which the question names. #1 (Ostgut.jpg) is an empty old freight yard, and #2–6 show the Reichstag and Berlin-Mitte. No new search is allowed, so the slot needs a real Berghain exterior photo (e.g. query "Berghain club exterior") or a switch to a decorative image. No suitable picture found for this question.
- **q-14155** (state-and-city-emblems) Die Landesflagge von Baden-Württemberg ist schwarz-gold. Aus dem Wappen welches alten Herzogtums stammen diese Farben? → Schwaben: Fact check: uncertain. The black-gold colours are tied to the Staufer/Swabia arms (three lions), but I found no source that explicitly says the flag colours derive from the Duchy of Swabia's arms. The state constitution just prescribes black-gold. Difficulty 10 also looks too high.
- **q-14157** (state-and-city-emblems) Das ist das Wappen von Berlin. Was sitzt oben auf dem Schild, über dem Bären? → Krone: No candidate shows the current Berlin coat of arms (black bear on a silver shield under the gold crown with wall and gate). Since no new search is allowed, the slot needs the Commons file of the official Landeswappen (e.g. "Coat of arms of Berlin.svg") added by hand. No suitable picture found for this question.
- **q-14166** (rivers-lakes-and-coasts) In Gruben wie dieser wird Kies abgebaut. Wofür wird er vor allem gebraucht? → Für Beton und Straßen: The question says „In Gruben wie dieser“, so the image has to clearly show a gravel pit. No candidate does: 1 and 3 show a green screening conveyor on grass with a little bare soil, 2 is a close-up of a machine, 4 is a rusty processing plant, 5 is an old conveyor in the bushes and 6 is a long covered conveyor across fields. No new search is allowed. A clear photo of a German gravel pit (Kiesgrube) with heaps and an excavator is needed, for example from the search "Kiesgrube Bagger" or "gravel pit excavator Germany". No suitable picture found for this question.
- **q-14182** (shows-and-presenters) Bei ProSieben forderte ich bis 2015 Kandidaten in bis zu 15 Spielen heraus. Die Promi-Version meiner Show heißt „Schlag den Star“. Wer bin ich? → Stefan Raab: No media candidate fits: the sheet shows an old hearing photo, a cathedral painting, office buildings, an 80s band, a mantis and a circuit board, none of which is a TV studio. A new search like "TV studio cameras" is needed, and can_search_again is false. No suitable picture found for this question.
- **q-14188** (slang-and-everyday-words) Wer immer wieder schikaniert wird, erlebt „Mobbing“. Das klingt englisch. Welches Wort sagt man dafür in England meist? → Bullying: The picked picture has an unsuitable licence (pd-us-only: PD-USNWR).
- **q-14194** (states-and-capitals) Aus dem Bundesland auf dieser Karte stammt eine berühmte Rostbratwurst. Welches Bundesland ist es? → Thüringen: No candidate shows the essential image: a German map with state borders and Thuringia highlighted, without labels. #1 prints „THÜRINGEN“ and Erfurt on the map, #2 has no highlight, and #3–#6 are maps of Europe or the world. A new search isn't allowed here, so the slot needs a hand-picked file such as „Thuringia in Germany.svg“. Also, hint 2 names the capital, Erfurt, which nearly gives the answer away at hint 2. Hint 2 should be vaguer, for example the neighbouring states or the Thuringian Forest. No suitable picture found for this question.
- **q-14198** (states-and-capitals) Dieses blau-weiße Rautenmuster ist das Erkennungszeichen von wem? → die Bayern: No candidate shows the essential image (a close-up of the blue-white Bavarian lozenge pattern): the candidates are army vehicles with German flags, a Kamala Harris photo, a warning sign, a US Veterans Day parade, and a portrait-format town sign where the lozenge flag is small and comes with text. No new search is allowed, so the image needs a different source, e.g. "Bavarian lozenge flag" or "Flag of Bavaria (lozengy)" on Commons. No suitable picture found for this question.
- **q-14203** (superstitions-and-folk-beliefs) Nach der Mathearbeit seufzt jemand: „Da mache ich drei Kreuze!“ Was meint er damit? → Er ist froh, dass es vorbei ist: Hint 1 („Es geht um ein Gefühl nach etwas Anstrengendem“) gives the answer away: the correct option is the only one that describes a feeling, so this hint alone solves the question. Hint 1 needs to become vague (e.g. about where the idiom comes from), and hint 2 should stop ruling out options so directly. Fact check: uncertain. The answer is right. The fun fact is not supported. The usual explanation is the Catholic habit of crossing oneself in thanks. I found no source linking the phrase to illiterate people signing with three crosses.
- **q-14208** (superstitions-and-folk-beliefs) Um Mitternacht beginnt die Geisterstunde. Wie oft schlägt eine Turmuhr wie diese dann? → 12: This asks the same fact as the approved q-5648 ("An old church clock rings once at 1 o'clock… How many times does it ring at midnight?" → 12). The ghost-hour framing doesn't change what's being asked. To keep the Geisterstunde topic, ask a different folklore fact, for example when the Geisterstunde ends (1 Uhr).
- **q-14216** (winter-sports) Bei der Vierschanzentournee hörst du „Schanze HS 142“. Welches Maß hat dort den alten K-Punkt als Größenangabe abgelöst? → Hillsize: Hint 1 („Der Begriff kommt aus dem Englischen.“) gives the answer away: „Hillsize“ is the only English option, the other three are German words. Hint 1 needs to be vaguer, for example about the hill as a whole and not just the landing point. The wrong answers could also include an English-sounding term so the answer doesn't stand out. Also consider the official spelling „Hill Size“.

## Question axes

- move: analogy 8, cause_effect 8, count 8, estimate 15, identify 36, made_of 7, name_concept 37, odd_one_out 12, origin 16, purpose 18, record 9, sequence 11, when 15, who 33, word_meaning 23
- stimulus: detail 3, map_outline 3, none 200, photo 45, sound 3, video 2
- clue: completion 11, direct 110, riddle 33, scenario 36, three_facts 66
- answer_kind: group 26, number 25, person 42, place 25, thing 52, time 18, word 68
- lens: body_senses 4, educational_media 16, everyday 44, history 46, language 48, nature 21, pop_culture 40, popular_science 2, school 21, science_news 2, university 12

## Dropped by the pipeline

- cakes-and-sweets-1: overlap like q-13111: Bei mir drehen sich Karussells und ein Riesenrad, und überall duftet es nach gebrannten Mandeln. Was bin ich? → Jahrmarkt: Seit Generationen werden sie auf jeder Kirmes in Kupferkesseln geröstet und warm verkauft. Welche Nascherei zeigt die Nahaufnahme? → Gebrannte Mandeln
- cakes-and-sweets-17: overlap like q-11021: Du stehst im Wald und eine Stimme ruft: „Knusper, knusper, Knäuschen, wer knuspert an meinem Häuschen?“ In welchem Märchen bist du? → Hänsel und Gretel: Ein süßes Häuschen wie dieses steht im Märchen „Hänsel und Gretel“. Wo steht es dort? → Tief im Wald
- carnival-and-fairs-2: overlap like q-12969: Beim Rosenmontagszug ruft man am Straßenrand laut „Kamelle!“. Wer wirft daraufhin Süßigkeiten? → Die Leute auf den Festwagen: Ich werde wochenlang geschmückt, trage riesige Pappfiguren und winkende Narren und rolle im Rosenmontagszug durch die Stadt. Was bin ich? → Festwagen
- carnival-and-fairs-9: overlap like q-10921: Wie heißt der Laden, in dem es frische Brötchen, Brezeln und Kuchen gibt? → Bäckerei: Auf der Wiesn gibt es dieses Gebäck riesengroß. Wer backt es? → Bäcker
- carnival-and-fairs-17: overlap like q-1822: Según la tradición de Pascua en muchos países, ¿qué personaje esconde estos huevos de colores? → El conejo de Pascua: Er hat lange Ohren, kommt im Frühling und versteckt bunte Eier im Garten. Wer bringt an Ostern die Eier? → Osterhase
- childrens-tv-and-audio-dramas-3: overlap like q-10859: Welche Farbe hat KEINE der drei Figuren Maus, Elefant und Ente aus der „Sendung mit der Maus“? → Grün: Orange Maus, gelbe Ente und kleiner blauer …: Welches Tier macht das Trio aus der „Sendung mit der Maus“ komplett? → Elefant
- childrens-tv-and-audio-dramas-6: overlap like q-10851: Ein Mädchen namens George, das lieber ein Junge wäre, ihr Hund Timmy und die Felseninsel Kirrin: Zu welcher Bande gehören sie? → Fünf Freunde: Du hörst eine Folge „Fünf Freunde“ und zählst nur die Kinder. Auf wie viele kommst du? → 4
- childrens-tv-and-audio-dramas-16: overlap like q-12134: Ich bin eine Fernsehsendung mit vielen Puppen, in Deutschland seit 1973. In meinem Lied heißt es: „Wer nicht fragt, bleibt dumm!“ Wer bin ich? → Sesamstraße: Einer liebt sein Quietscheentchen, der andere Büroklammern und Tauben. In welcher Straße wohnen Ernie und Bert? → Sesamstraße
- dialects-and-regional-words-4: overlap like q-13162: In der Pfalz kocht man daraus „Grumbeersupp“, im Saarland „Dibbelabbes“. Was ist eine „Grumbeere“? → Kartoffel: Im Süden heißt sie oft „Erdapfel“, sie kam aus Südamerika nach Europa, und der Alte Fritz ließ sie in Preußen anbauen. Was ist gemeint? → Kartoffel
- dialects-and-regional-words-11: overlap like q-9414: Im Märchen besiegt ein Igel den Hasen beim Wettlauf. Wer hat das Märchen in eine berühmte Sammlung aufgenommen? → Brüder Grimm: Im Märchen gewinnt dieses Tier mit dem Ruf „Ick bün all hier!“ ein Rennen. Wer nahm das Märchen in seine berühmte Sammlung auf? → Brüder Grimm
- dialects-and-regional-words-13: overlap like q-9328: Tiefe Zechen voller Steinkohle, Stahl von Krupp und Bergleute, die sich „Kumpel“ nennen: Welche Region ist gemeint? → Ruhrgebiet: Früher fuhr ich im Ruhrgebiet unter Tage in die Zeche ein. Heute nennt man auch einen guten Freund so. Wer bin ich? → Kumpel
- drinks-1: duplicate like q-12210: In welcher Stadt steht dieser Turm? → München: Aus welcher Stadt stammt die Brauerei Paulaner? → München
- drinks-3: overlap like q-12128: Holzbuden, Lebkuchenherzen, gebrannte Mandeln und warmer Kinderpunsch: Welcher Markt ist gemeint? → Weihnachtsmarkt: Du kaufst an einem Marktstand einen dampfenden Kinderpunsch. Zu welcher Zeit im Jahr gibt es den in Deutschland vor allem? → In der Adventszeit
- drinks-4: overlap like q-9392: „Ich komme aus dem Automaten, nachdem du leere Flaschen hineingesteckt hast, und an der Kasse werde ich zu Geld.“ Was bin ich? → Pfandbon: Er steht meist am Eingang vom Supermarkt. Man schiebt leere Flaschen in sein Loch, und ein Band fährt sie weg. Wie heißt dieses Gerät? → Pfandautomat
- drinks-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Welches Wasser kribbelt NICHT auf der Zunge? → Stilles Wasser
- drinks-14: overlap like q-13996: Auf der Wiesn bestellt man Bier in der Maß. Wie viel passt in einen vollen Maßkrug? → 1 Liter: Wie viel Bier passt in einen vollen Maßkrug? → 1 Liter
- empire-weimar-and-nazi-era-9: overlap like q-4078: Locked in a prison cell after a failed coup in Munich, Adolf Hitler began writing “Mein Kampf”. In which year? → 1924: Im November 1923 zog eine Partei vom Münchner Bürgerbräukeller zur Feldherrnhalle, um die Reichsregierung zu stürzen. Welche? → NSDAP
- empire-weimar-and-nazi-era-15: overlap like q-10940: Die SRP wurde 1952 verboten, die KPD 1956, zwei Anläufe gegen die NPD scheiterten. Welches Gericht entscheidet über ein Parteiverbot? → Bundesverfassungsgericht: In welchem Jahr verbot das Bundesverfassungsgericht die KPD in der Bundesrepublik? → 1956
- films-and-actors-1: overlap like q-12046: Ich bin Apachenhäuptling, mein Blutsbruder heißt Ranger, und mein Zwillingsbruder führt die Puder-Rosa-Ranch. Wer bin ich? → Abahachi: Michael Bully Herbigs Komödie von 2001 ist mit über 11 Millionen Zuschauern der erfolgreichste deutsche Kinofilm. Was nimmt sie auf die Schippe? → Karl-May-Western
- films-and-actors-2: overlap like q-12045: Du schaltest sonntags die ARD ein und siehst Mutter Beimer in der „Lindenstraße“. In welchem Jahr lief die erste Folge? → 1985: Til Schweiger wurde Anfang der 1990er sonntags im Ersten bekannt, als Bewohner einer Fernsehstraße. Wie hieß sie? → Lindenstraße
- films-and-actors-16: overlap like q-10889: Ich war Synchronsprecher in München und lieh über 20 Jahre lang einem gelben, Donut-liebenden Familienvater die deutsche Stimme. Wer bin ich? → Norbert Gastell: Sie sitzen im Tonstudio, schauen auf einen Bildschirm und sprechen Hollywoodstars Satz für Satz auf Deutsch nach. Wie heißt ihr Beruf? → Synchronsprecher
- home-and-public-life-11: overlap like q-9462: Dieses Ampelmännchen mit Hut ist heute Kult in Berlin. Aus welchem Staat stammt es ursprünglich? → DDR: Seit Jahrzehnten zeigt die Fußgängerampel in Deutschland, wann man gehen darf. Wie viele Farben hat sie? → 2
- inventors-and-scientists-1: overlap like q-4080: Frank Whittle in Britain and Hans von Ohain in Germany invented it separately in the 1930s, and Germany's Me 262 used it in battle in 1944. What is it? → The jet engine: Hans von Ohain entwickelte ihn bei Heinkel, und 1939 flog die He 178 als erstes Flugzeug der Welt damit. Welcher Antrieb war das? → Turbinen-Strahltriebwerk
- inventors-and-scientists-3: overlap like q-0104: ¿Quién inventó la imprenta de tipos móviles en Europa, hacia 1450? → Johannes Gutenberg: Johannes Gutenberg druckte in Mainz seine berühmte Bibel mit beweglichen Buchstaben. Wann war sie fertig? → Um 1455
- inventors-and-scientists-8: overlap like q-5688: I lived in Germany and hated bitter coffee grounds in my cup. In 1908, I poked holes in a brass pot and lined it with paper from my son's school notebook. Who am I? → Melitta Bentz: Edison ist zur Glühbirne wie Melitta Bentz zu …? → Kaffeefilter
- mountains-and-landscapes-15: overlap like q-9439: Sie staut einen Fluss im Sauerland, heißt „Westfälisches Meer“, und ihre Mauer brach im Mai 1943 durch Rollbomben. Welche Talsperre ist das? → Möhnetalsperre: Der Möhnesee im Sauerland wurde 1913 fertig, hält Wasser für die Ruhr bereit und war 1943 Ziel britischer „Rollbomben“. Was für ein See ist er? → Stausee
- national-team-8: overlap like q-2486: Germany won the 2014 World Cup final at the famous Maracanã stadium. In which city is it? → Rio de Janeiro: Rund 200 000 Zuschauer sahen hier 1950 ein WM-Spiel – Weltrekord. 2014 wurde Deutschland hier Weltmeister. Welches Stadion ist das? → Maracanã
- pop-and-rock-4: overlap like q-12107: Campino singt seit 1982 in einer Düsseldorfer Punkband, deren Name eine Redewendung ist. Was bedeutet „tote Hose“? → Es ist nichts los: Ich bin Frontmann einer Punkband und heiße eigentlich Andreas Frege. 2012 sang ich „An Tagen wie diesen“. Wer bin ich? → Campino
- pop-and-rock-9: overlap like q-11683: ¿Qué músico cubano, apodado «el Rey del Mambo», hizo famoso ese ritmo desde la Ciudad de México con «Qué rico el mambo» y «Mambo No. 5»? → Dámaso Pérez Prado: Ein Münchner landete 1999 einen Welthit, in dem er Frauennamen von Angela bis Rita aufzählt. Welcher Tanz steht im Titel? → Mambo
- pop-and-rock-14: overlap like q-13198: Ich bin ein Fernsehsender, bei mir laufen „Die Simpsons“ und „Germany's Next Topmodel“. Wer bin ich? → ProSieben: „Deutschland sucht den Superstar“ ist zu RTL wie „Germany's Next Topmodel“ zu …? → ProSieben
- rap-and-electronic-5: overlap like q-11100: Auf dem Schulhof hört man viele Wörter aus anderen Sprachen. Welches davon stammt NICHT aus dem Arabischen? → Digga: Es kommt aus Hamburg, ist aus dem Wort „Dicker“ entstanden, und Jugendliche sagen es zu ihren Kumpels. Welches Wort ist gemeint? → Digga
- rap-and-electronic-12: overlap like q-0643: El bushido, 'el camino del guerrero', fue un código de honor que también valoraba la ceremonia del té. ¿De qué país viene? → Japón: Dieser Berliner Rapper nannte sich nach dem Ehrenkodex der japanischen Samurai. Wie heißt er? → Bushido
- brands-and-products-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Aus welchem Land stammt der Korrekturhelfer Tipp-Ex ursprünglich? → Deutschland
- dialects-and-regional-words-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Ich klettere auf Bäume, stibitze Nachbars Äpfel und habe nur Unfug im Kopf. Wie nennt man mich im Süden? → Lausbub
- dialects-and-regional-words-3: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Auf Schwäbisch wird aus „Häuschen“ ein „Häusle“. Was wird auf dieselbe Weise aus „Mädchen“? → Mädle
- dialects-and-regional-words-7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Im Ruhrpott grüßt man gern mit „Tach auch!“. Wofür ist „Tach“ die Kurzform? → Guten Tag
- drinks-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: In vielen deutschen Kurorten steht eine prächtige Trinkhalle. Wofür ist sie dort gedacht? → Heilwasser aus Quellen trinken
- gdr-history-10: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Das Gefängnis Bautzen I in Sachsen war erst Speziallager der Sowjets, dann Haftort für politische Gefangene der DDR. Wie hieß es im Volksmund? → „Gelbes Elend“
- mountains-and-landscapes-11: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Die Barbarine ist ein Wahrzeichen der Sächsischen Schweiz, steht am Pfaffenstein und soll laut Sage ein versteinertes Mädchen sein. Was ist sie? → Eine Felsnadel aus Sandstein
- rap-and-electronic-17: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Tangerine Dream nutzte ihn in den 1970ern, Giorgio Moroder 1977 in München für „I Feel Love“. Wozu dient ein Sequenzer? → Tonfolgen automatisch abspielen
- slang-and-everyday-words-5: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: „Das ist ja bodenlos!“, schimpfen Erwachsene gern. Was meint jemand, wenn ein Witz „bodenlos“ war? → Er war richtig schlecht
- winter-sports-12: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Dieser Eishockeyklub kommt aus der Karnevalsstadt am Rhein und spielt in Deutschlands größter Eishockeyhalle. Welches Tier steckt in seinem Namen? → Haie
- rivers-lakes-and-coasts-3: overlap like q-13176: Auf diesem Brötchen liegen „Nordseekrabben“. Zu welcher Tiergruppe gehören sie in Wahrheit? → Garnelen: An der Nordseeküste nennt man diese Tiere „Krabben“. Zu welcher Tiergruppe gehören sie eigentlich? → Garnelen
- sayings-and-idioms-3: overlap like q-13039: Wer tanzt im Märchen ums Feuer und singt: „Ach, wie gut, dass niemand weiß …“? → Rumpelstilzchen: Im Märchen hüpft ein Männchen auf einem Bein, singt „Ach, wie gut, dass niemand weiß …“ und wird dabei belauscht. Wo tanzt es? → Um ein Feuer vor seinem Haus
- sayings-and-idioms-14: overlap like q-9222: Eine schwarze Katze läuft dir über den Weg. Was bringt das nach altem Aberglauben? → Pech: An Silvester verschenkt man in Deutschland gern kleine Glücksbringer, oft zusammen mit einem Schornsteinfeger. Welcher gehört NICHT dazu? → Schwarze Katze
- slang-and-everyday-words-11: overlap like q-11086: Welcher deutsche YouTuber heißt mit bürgerlichem Namen Erik Range und gilt als Pionier der Let’s-Play-Videos? → Gronkh: Du schaust zu, wie jemand Minecraft spielt und dabei kommentiert. Wer gilt als bekanntester Let's Player Deutschlands? → Gronkh
- slang-and-everyday-words-14: overlap like q-10822: Du hörst in der Werbung eines Elektronikmarkts den Spruch „Geiz ist geil!“. In welchem Jahrzehnt bist du wohl? → 2000er: Der Werbespruch „Geiz ist geil“ machte eine Elektronikmarktkette berühmt. In welchem Jahrzehnt lief er? → In den 2000er-Jahren
- state-and-city-emblems-17: overlap like q-12034: „Etwas im Schilde führen“ kommt von den Wappen, die Ritter auf ihre Schilde malten. Seit wann taten sie das? → 12. Jahrhundert: Schilde mit Wappen wie diesem gab es zuerst im Mittelalter. Wer trug sie, damit man ihn unter seinem Helm erkannte? → Ritter
- states-and-capitals-3: overlap like q-14158: Ich springe weiß auf rotem Grund im Wappen von Niedersachsen. Welches Tier bin ich? → Pferd: Stuttgarts Name kommt von einem „Stutengarten“, einem alten Gestüt. Welches Tier steht deshalb im Stadtwappen und im Porsche-Logo? → Pferd
- superstitions-and-folk-beliefs-5: overlap like q-14013: Zu Hause bekommst du eine heiße Zitrone mit Honig gemacht. Wogegen gilt sie als Hausmittel? → Gegen Erkältung: Sie ist heiß, hat Nudeln und Gemüse, und Oma schwört auf sie. Wogegen soll Hühnersuppe helfen? → Erkältung
- superstitions-and-folk-beliefs-12: overlap like cakes-and-sweets-17: Ein süßes Häuschen wie dieses steht im Märchen „Hänsel und Gretel“. Wo steht es dort? → Tief im Wald: In welchem Märchen der Brüder Grimm finden zwei Kinder im Wald ein Häuschen wie dieses? → Hänsel und Gretel
- winter-sports-17: overlap like q-12248: Im Winter liegt dort Schnee. Kinder ziehen ihren Schlitten hinauf und sausen dann hinunter. Wo sind sie? → Rodelberg: Er hat Kufen, man zieht ihn den Rodelberg hinauf, und dann saust man darauf hinunter. Wie heißt er? → Schlitten
