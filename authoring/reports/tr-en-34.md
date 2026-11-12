# tr-en-34

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `germany` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 296
- Approved: 289
- Needs work: 7
- Not travelling: 4 (3 confirmed → `translatable: false`, 1 translated again next run)
- Claude calls: 451, about $29.45 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-34&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-32 | tr-en-33 | tr-en-34 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 298 | 296 |
| not travelling |  | 3 | 2 | 4 |
| not travelling confirmed |  | 3 | 2 | 3 |
| rejected rate | ≤ 20.0 % | 1.0 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| approved |  | 292 | 292 | 289 |
| needs_work |  | 5 | 6 | 7 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 2.0 % ✓ | 2.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.0 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.7 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $28.62 | $27.99 | $26.06 |
| $ per approved |  | $0.10 | $0.10 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 1 (0 major), fact 2 (0 major), overlap 2 (1 major), media 1 (0 major), style 1 (1 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.39

Major findings on approved questions:

- **q-9324**: overlap, style — This repeats a question already in the pool. q-5648 asks how many times an old church clock rings at midnight, after saying it rings once per hour. Both questions test the same fact (a clock sounds the hour count, so 12 at 12) with the same answer, so playing one gives away the other. Smaller point: hint 3, “Noon is the biggest number on the clock face”, is a literal translation of the German and reads oddly, since noon isn't a number; “12 o'clock” or “Noon is shown by the biggest number” would read better. Everything else is a faithful, correct translation: the answer and wrong options, the hints and the fun fact about the bellows and pipes, and the essential cuckoo-clock image all check out. (http://127.0.0.1:8001/review/q-9324)

## Needs work

- **q-13024** (holidays-through-the-year) St. Martin cut his cloak with his sword to share it with a freezing beggar. Into how many pieces? → 2: This duplicates approved q-10835 ("In the song “Sankt Martin ritt durch Schnee und Wind”, Martin cuts his cloak with his sword. Into how many pieces?", answer 2). It asks the same fact with the same answer, and the added "with his sword" makes the wording even closer. The German source has the same overlap (source:). One of the two should be dropped, or this one should ask a different St. Martin fact.
- **q-15922** (athletes-and-other-sports) Markus Rehm long-jumps with a sports prosthesis like this one. What material is the spring blade made of? → Carbon fiber: Source: this asks the same fact as approved q-2558 (what running-blade prostheses are made of → carbon fiber). Only the Markus Rehm framing is different, so whichever one players see first gives away the other. The translation itself is accurate and reads naturally. The source question needs a different angle on Rehm, for example his 2014 German long jump title or his Paralympic event, or it should be dropped.
- **q-16042** (national-team) In July 2014, fans welcomed the world champions on Berlin's Fanmeile at the Brandenburg Gate. About how many people were there? → Several hundred thousand: Fact check: wrong. The answer is fine (reports say roughly 250,000 to almost 500,000). But hint 1 is off: the Fanmeile is about 1.2 km long (Brandenburg Gate to Siegessäule), not 'almost 2 km'. The '1.2 miles' also mixes up km and miles.
- **q-16145** (shows-and-presenters) In what year did YouTuber Bibi start her channel “BibisBeautyPalace”? → 2012: Source: hint 2 says Bibi was 19 when she started the channel. She was born on August 20, 1993, and the channel started in spring 2012, so she was 18. The source hint needs fixing (for example "Bibi was still a teenager at the time" or "Bibi was 18 at the time"), and then the translation should follow it. Otherwise the translation is faithful and reads naturally.
- **q-16917** (dialects-and-regional-words) Here people don't chat, they “schnack”. There are also fish sandwiches, dikes and wind off the sea. Where are you? → In northern Germany: Source: the fun fact's word “Schnackbüdel” can't be confirmed. The fact check is uncertain, and the attested Low German word is “Sabbelbüdel”. The source's fun fact needs a verifiable replacement (for example “Klönschnack” for a cozy chat, or “Sabbelbüdel” for a chatterbox), and then the translation should follow it. Apart from that, the translation is faithful and reads naturally. Fact check: uncertain. The fun fact's word "Schnackbüdel" could not be found in any dictionary or source. "schnacken" (to talk) and the northern German setting are correct, and the answer and hints are fine.
- **q-16931** (federal-republic-and-reunification) Complete the sentence: “The Bundestag in Berlin is …” → Germany's parliament: The fun fact gets the word history backwards. “Tagen” comes from “Tag” (day), meaning a set day for a meeting; “Tag” does not come from “tagen”. Bundestag, like Reichstag, uses “Tag” in the sense of an assembly held on a fixed day. The translation half-admits the link to “day” but still says “Tag comes from tagen”, which contradicts itself. Source: the German fun fact has the same reversed claim and should be fixed too (for example: “The ‘Tag’ in Bundestag means ‘day’: assemblies used to meet on a fixed day, which is where ‘tagen’ (to meet) comes from”).
- **q-9230** (federal-republic-and-reunification) Which little black goblin from East German children's TV loves to shout “Ach du meine Güte!” (Oh my goodness!)? → Pittiplatsch: Source issue: the fact check says Pittiplatsch's signature catchphrase is “Ach du meine Nase!”, not “Ach du meine Güte!”. I can't confirm “Güte” as his defining line. The German source should use “Ach du meine Nase!”, and the English then becomes “Ach du meine Nase!” (Oh my nose!). Apart from that, the translation is faithful and natural. Fact check: wrong. Pittiplatsch's catchphrase is "Ach du meine Nase!", not "Ach du meine Güte!".

## Not travelling

- **q-16098** other, confirmed: Das Ruhrgebiet heißt auch „Pott“, und Fußballer holen „den Pott“. Was bedeutet „Pott“ eigentlich? → Topf (The answer “Topf” translates as “pot”, which is the English cognate of “Pott”, so in English the word gives itself away.)
- **q-13003** about_language, translate again: Ergänze: Wasser, das zu Hause direkt aus dem Wasserhahn kommt, nennt man … → Leitungswasser (Pure German vocabulary question (the word Leitungswasser, hint 3 plays on 'Leitung' = pipe). In English it becomes the trivial 'tap water', and the German version has no cultural content beyond the word itself.)
- **q-15162** about_language, confirmed: Seit den 1950ern rockt sie die Bühnen. Wofür steht das „E“ in E-Gitarre? → Elektrisch (Asks what the E in the German word “E-Gitarre” stands for; in English the answer is the word “electric guitar” itself.)
- **q-15080** wordplay, confirmed: „An der Nordseeküste, am plattdeutschen Strand, sind die Fische im Wasser und selten …“ Wie geht die Zeile weiter? → an Land (Completing a German lyric whose answer depends on the German rhyme (Strand / an Land); options and hints only work in German.)

## Stale re-translated

None.
