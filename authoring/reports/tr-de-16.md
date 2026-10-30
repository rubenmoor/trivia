# tr-de-16

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 284
- Needs work: 16
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 815, about $43.64 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-16&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-14 | tr-de-15 | tr-de-16 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 291 | 288 | 284 |
| needs_work |  | 9 | 12 | 16 |
| needs_work rate | ≤ 20.0 % | 3.0 % ✓ | 4.0 % ✓ | 5.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.3 % ✓ | 3.0 % ✓ | 4.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 96.7 % ✓ | 95.0 % ✓ |
| cost $ |  | $39.80 | $40.83 | $39.74 |
| $ per approved |  | $0.14 | $0.14 | $0.14 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 57 (0 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 4 (0 major), fact 3 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.90

Major findings on approved questions:

None.

## Needs work

- **q-0077** (disney-films) In „Encanto“: Welche besondere Gabe hat Luisa? → Übermenschlich stark sein: source: the fun fact is wrong in the Spanish source and the German copies it. Not every Madrigal has a magic door showing a gift: Abuela Alma, Pepa, Julieta and the in-laws have none, and Mirabel's door shows no gift. Correct the source, for example to "Die Kinder und Enkel mit Gabe haben jeweils eine magische Tür", then re-translate. Fact check: wrong. The answer (superhuman strength) and the wrong answers are right: animals is Antonio, seeing the future is Bruno, flowers is Isabela. The hints fit Luisa. The fun fact is too broad. Only the Madrigal children and grandchildren have magic doors. Abuela Alma, Pepa, Julieta, Félix and Agustín have none. Mirabel's door shows no gift and vanishes. This is from memory, not checked against sources.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicate of the approved q-0369 ("Aus welchem Land stammt der Zauberwürfel…?", answer Ungarn): it asks the same fact with the same answer, so one of the two should be dropped from the German pool. The translation itself is faithful and natural.
- **q-0548** (countries) Wie heißen diese riesigen Steinstatuen auf der Osterinsel? → Moai: source: hint 2 ("Casi todas son cabezas gigantes…", translated faithfully as "Fast alle sind riesige Köpfe…") is factually wrong. Moai are full figures with oversized heads and torsos, and the question's own fun fact says many have a body buried below the head. The source needs correcting, for example to "Sie haben übergroße Köpfe mit langen Nasen und ernsten Augenbrauen"; the translation is otherwise fine.
- **q-0870** (video-game-characters) Aus welchem Land stammt Metal Gear, die 1987 gestartete Spielereihe um den Spion Solid Snake? → Japan: source: the fun fact calls the MSX a console, but it is a home computer standard, and Metal Gear ran on the MSX2. The German translation copies this faithfully. The source needs correcting, for example to „Heimcomputer MSX2“, and the translation should then follow. Fact check: wrong. The answer (Japan), Konami, the 1987 release and Kojima's birth in Tokyo are all correct. The fun fact calls the MSX a "Konsole", but the MSX (Metal Gear ran on the MSX2) is a home computer standard, not a console. This is from memory; I ran no searches.
- **q-0989** (maths) Ergänze: „Gleichseitig“ ist zu drei gleichen Seiten wie „skalen“ zu … → Keine gleichen Seiten: The stem's case doesn't fit the options. „… wie ‚skalen‘ zu …“ needs a dative ("zu keinen gleichen Seiten", "zu einem rechten Winkel"), but the options are accusative or nominative, and „zu Einen rechten Winkel“ is plainly ungrammatical when read aloud. Reword the stem so all four fit, e.g. „Ein gleichseitiges Dreieck hat drei gleiche Seiten. Und ein skalenes Dreieck?“. Also note that „skalen“ is rare in German, and the translator's notes are stale because they still describe „unregelmäßig“.
- **q-1147** (fast-food) Mein Gesicht mit weißem Anzug und Spitzbart prangt auf Eimern voller Brathähnchen. Welcher US-Bundesstaat steckt im Namen meiner Kette? → Kentucky: source: the fun fact is false in both the source and the translation. Harland Sanders did serve in the US Army (enlisted around 1906, stationed in Cuba), so "war nie beim Militär" is wrong despite the fact check's "confirmed". The source needs correcting, for example: "'Colonel' was not a military rank but an honorary title from the state of Kentucky." The translation can then follow.
- **q-1952** (winter-olympics) Wann finden die Paralympischen Winterspiele statt, verglichen mit den Olympischen Winterspielen? → Kurz danach, am selben Ort: source: hint 2 ("Nunca se celebran antes que los Juegos Olímpicos") is historically false, and the translation carries it over faithfully. The 1980 (Geilo), 1984 and 1988 (Innsbruck) Winter Paralympics took place before the Olympic Winter Games, and in other places. The source should drop "nunca" and limit the hint to today's pattern, and the question should say "heute"/"hoy", since the answer only holds for the modern era (same host since 1992).
- **q-2246** (athletics) Diese Latte liegt lose auf zwei Auflagen und fällt bei der kleinsten Berührung herunter. In welchen Leichtathletik-Disziplinen kommt sie vor? → Sprungdisziplinen: Fact check: wrong. The loose bar is only used in high jump and pole vault (vertical jumps). 'Sprungdisziplinen' also includes long jump and triple jump, which have no bar, so the answer is too broad.
- **q-2677** (reality-tv) Es passiert gegen Ende einer Folge, die Moderation verkündet es, und jemand muss die Show verlassen. Wie heißt das? → Rauswurf: Fact check: wrong. The description ("Teil der Show, in dem jemandem einfällt, dass zu Hause der Herd an ist") doesn't match the question or the answer. The question is vague: "Rauswurf" isn't the only fitting term. "Elimination" or "Ausscheiden" fit equally well. The hint "abgewählt" only applies to vote-based shows. "Immunität" and "Casting" are clearly wrong, but "Feier" is just filler. The fun fact (eliminated contestants returning for a second chance) is true for some shows, e.g. Survivor's Redemption Island and Big Brother, but it doesn't relate to the question. The question also says "three_facts" clue style but has no concrete facts. I checked this from general knowledge, without web sources.
- **q-3136** (wonders-of-the-world) Die Christusstatue von Rio de Janeiro steht auf dem Gipfel des Corcovado. Wie hoch ist dieser Berg ungefähr? → Etwa 700 m: Fact check: wrong. The facts hold. Corcovado is about 710 m. The statue is 30 m tall, not counting its 8 m pedestal, and its arm span is 28 m. The Eiffel Tower is about 330 m, so the 'about double' hint works. The wrong answers (70, 2000 and 7000 m) are clearly wrong. The problem is the media query, 'Rio de Janeiro Sugarloaf Mountain'. Sugarloaf (Zuckerhut) is a different mountain, about 396 m high, so the image doesn't show Corcovado or the statue. It could mislead players, especially in a question about the mountain's height. I did not run web searches. This check relies on well-known figures.
- **q-3393** (flags) Bei der Eröffnungsfeier der Olympischen Spiele: Wie nennt man die Person auf dem Foto, die vor ihrem Team herläuft? → Fahnenträger: source: the fun fact's 'Greece always marches first' is not strictly true, and the German 'immer als Erstes' copies it. At Athens 2004, Greece's flag led the parade but, as host, its team marched last. The source fun fact should say 'traditionally' or note the exception, and the translation should then follow it.
- **q-3681** (fashion-history) Ich trage einen weißen Anzug, dicke Handschuhe und einen Hut mit Netz vor dem Gesicht, dazu eine kleine Rauchdose. Wer bin ich? → Imker: Overlaps q-9291 (approved, German pool): both are identify-the-person questions with the answer "Imker", and both use the hat with veil or net as a clue, so seeing one gives away the other. The translation itself is faithful and natural; the conflict is at pool level, so one of the two should be dropped.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenreiniger-Armen. Wofür war sein Hauptteil ursprünglich gemacht? → Zum Essen: source: hint 2 is false and the translation carries it over. In Toy Story 4, Woody takes the spork and craft bits out of the kindergarten bin and puts them on Bonnie's table; Bonnie doesn't fish it out herself. The source hint should become e.g. "He came out of a kindergarten trash can, and Bonnie didn't take him out herself", then be retranslated. Also, the German question is about 165 characters, over the 160 limit; a retranslation could drop "ursprünglich" and shorten the wording.
- **q-4940** (trains) Was ist das? → Fahrkarte: Fact check: wrong. The description is ambiguous. "A small piece of paper adults always lose just when they need it" also fits the distractor "Einkaufszettel", which is a classic lost-or-forgotten slip. A Geldschein can also be lost. Only the hints point to Fahrkarte. The hints and the fun fact (many tickets are now digital codes on phones) are true.
- **q-5561** (james-bond) Sean Connery verhält sich zu „James Bond jagt Dr. No“ wie Barry Nelson zu … → Casino Royale: source: the fun fact is inaccurate. In the 1954 TV version the British friend was named Clarence Leiter, not Felix Leiter, so "sein Freund Felix Leiter war Brite" is wrong in both the source and the translation. Correct the source, e.g. "…and his friend Leiter was a Briton named Clarence", then carry the correction over to the German. The translation is otherwise fine.
- **q-6407** (pyramids) Du stehst im Dschungel Kambodschas vor Prasat Thom, der siebenstufigen Stufenpyramide von Koh Ker. In welchem Jahrhundert wurde sie gebaut? → 10. Jahrhundert n. Chr.: source: hint 3 says Jayavarman IV ruled from Koh Ker until 944, but his reign is usually dated about 928–941; 944 is the end of Koh Ker as capital, under his son Harshavarman II. The fact check also flags that the seven-tier pyramid is properly called Prasat Prang, with Prasat Thom naming the main temple group, and that its height is given as 30 or 36 m. These need correcting in the source first. The German faithfully repeats them, though 'siebenstufigen Stufenpyramide' is clumsy and should become 'siebenstufigen Pyramide' on retranslation. Fact check: uncertain. The answer (10th century) is correct. The wrong answers are wrong. Angkor Wat is 12th century, so that hint is fine. Three details are shaky. (1) Jayavarman IV's reign is usually given as 928–941. Koh Ker stayed capital until 944 under Harshavarman II, so hint 3 ('928 bis 944') is slightly off. (2) The height of the pyramid is given as 36 m by some sources and 30 m by others (Wikipedia's Jayavarman IV article says 30 m). (3) The seven-tiered pyramid is properly called Prasat Prang, and Prasat Thom is the name of the main temple group. The Maya comparison is common in travel writing.

## Not travelling

None.

## Stale re-translated

None.
