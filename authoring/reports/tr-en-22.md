# tr-en-22

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `germany` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 289
- Needs work: 8
- Not travelling: 3 (3 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 522, about $28.25 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-22&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-20 | tr-en-21 | tr-en-22 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 298 | 300 | 297 |
| not travelling |  | 2 | 0 | 3 |
| not travelling confirmed |  | 1 | 0 | 3 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 1.0 % ✓ |
| approved |  | 296 | 298 | 289 |
| needs_work |  | 2 | 2 | 8 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 0.7 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 100.0 % ✓ | 95.0 % ✓ |
| cost $ |  | $25.27 | $22.40 | $25.46 |
| $ per approved |  | $0.09 | $0.08 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), overlap 2 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.79

Major findings on approved questions:

- **q-12193**: overlap — The question asks the same fact as approved q-8464 ("almost as tall as a person, played standing up, lowest sound in the string orchestra" → double bass), so seeing one gives the other away. Source issue: the topic also has no German connection, so it fits `base` rather than the `germany` bundle. The translation itself is accurate and natural. The facts, hints, fun fact and decorative concert-hall image all check out. (http://127.0.0.1:8001/review/q-12193)

## Needs work

- **q-13003** (drinks) In Germany, what is “Leitungswasser”? → Tap water: Now that the translation asks what “Leitungswasser” means, two things give the answer away that didn't in the source, where the question itself already said the water comes from the tap. First, the description ("waiting inside the wall") states the answer's defining trait: of the four options, only tap water waits inside the wall. Rewrite it to joke about water or drinks in general without saying where it comes from. Second, the kept illustrative image (a glass being filled at a kitchen tap) is shown sharp and shows the answer. Replace it with a decorative image, or with a neutral one such as a glass of water on a restaurant table.
- **q-13208** (winter-sports) When is the Biathlon auf Schalke in Gelsenkirchen's stadium traditionally held? → Between Christmas and New Year's Eve: source: the fun fact says "hundreds of metric tons" of snow, but sources give about 3,000–4,000 cubic metres, which is well over 1,000 tonnes. The fact check is uncertain and I can't confirm the tonnage either. Correct the fun fact in the German source, for example to "thousands of cubic metres of snow (from the Neuss ski hall)", and then translate it again. Fact check: uncertain. The date is right (late December, e.g. 28–30 Dec). The fun fact gives snow in 'hundreds of metric tons', but sources give about 3,000–4,000 cubic metres, which weighs far more than that. I found no figure in tonnes. The snow comes from the Neuss ski hall.
- **q-15182** (sausages-and-cheese) In some parts of Germany, the “Brotdose” (lunch box) is called a “Brotbüchse”. Where do kids usually pack it in the morning? → In their school bag: Fact check: uncertain. The answer is plausible and the wrong answers are clearly wrong. I did not verify the fun fact that 'Knifte' and 'Kniftendose' are used in the Ruhr area.
- **q-16042** (national-team) In July 2014, fans welcomed the world champions on Berlin's Fanmeile (fan mile) at the Brandenburg Gate. Roughly how many people were there? → Several hundred thousand: Fact check: uncertain. The answer is right: reports put the crowd at the 15 July 2014 welcome at roughly 400,000–500,000, and the other options are far too small. Two things are shaky. The hint 'almost 2 km' is loose, because sources give 1.2–1.5 km for the 2014 Fanmeile (about 2 km only in a 2006 taz article). 'Suddenly the living room is as long as an entire street' is odd for a description. The fun fact that the Straße des 17. Juni is fully closed to cars for big matches is plausible but I did not verify it.
- **q-16159** (slang-and-everyday-words) Eyes wide, often followed by an “ey”, say in front of the park's tallest roller coaster. What does “Boah!” express here? → Amazement: The question text reads as translationese and is hard to follow when read aloud. “Eyes wide, often followed by an ‘ey’” is a dangling phrase: it sounds as if the eyes are followed by “ey”. And “say in front of…” sounds like an instruction to say something rather than “for example”. Suggested rewording: “You stand in front of the park's tallest roller coaster, eyes wide, and shout “Boah, ey!”. What does “Boah!” express here?”
- **q-16910** (childrens-tv-and-audio-dramas) You don't watch it, you only listen. A voice reads a whole book out loud, often on long car trips. What is it? → Audiobook: This duplicates q-3506, which is already approved in the English pool. Both ask players to name an audiobook from the clue "a book someone reads aloud for you to listen to", so English players would get the same fact twice. The translation itself is faithful and reads naturally, and the reworked hint 3 is fine.
- **q-16921** (empire-weimar-and-nazi-era) I pushed for the founding of the German Empire in 1871, became its first chancellor, and a pickled herring is named after me. Who am I? → Otto von Bismarck: Source: the fun fact is wrong. About 170 Bismarck towers survive worldwide, and many of them are now in Poland, Czechia, Russia and other countries, so fewer than 170 stand in Germany. The source should say something like “About 170 Bismarck towers still stand today, most of them in Germany.” The translation should then follow it.
- **q-16931** (federal-republic-and-reunification) Complete the sentence: “The Bundestag in Berlin is …” → Germany's parliament: source: The fun fact gets the etymology backwards, in the German source and so in this translation. The “Tag” in Bundestag/Reichstag/Landtag literally means “day”: it came to mean an assembly because meetings were held on set days, and “tagen” comes from “Tag”, not the other way round. Correct the source fun fact (for example: “The “Tag” in Bundestag really means “day”: assemblies were held on fixed days, and the verb “tagen”, to meet, comes from it.”), then translate it again. Fact check: wrong. The answer, wrong answers and hints are fine (Bundestag = federal parliament, elected every 4 years). The fun fact has the etymology backwards. "Tag" in Bundestag/Reichstag/Landtag is literally "day", and it came to mean "assembly" because meetings were held on set days. "Tagen" (to meet) and "Tagung" derive from "Tag", not the other way round. So "nothing to do with the day" is false.

## Not travelling

- **q-10825** other, confirmed: Tom Tailor wurde 1962 in Hamburg gegründet, verkauft Jeans und Hemden und trägt ein englisches Wort im Namen. Was bedeutet „Tailor“? → Schneider (The question asks what the English word “Tailor” means; for English speakers the word is its own answer.)
- **q-17009** wordplay, confirmed: Welche Stadt im Ruhrgebiet heißt genauso wie etwas, das du jeden Tag tust? → Essen (Lives on the pun Essen = 'to eat' in German; in English the question would just ask for a German word and give the answer away.)
- **q-12180** other, confirmed: „Bro“ ist kurz für ein Familienwort und heute auf jedem Schulhof zu hören. Aus welchem Land kam es zu uns? → USA (Asks which country the German slang word “Bro” came from. For English speakers “bro” is a word of their own language, and the USA is the only English-speaking option, so the question becomes a giveaway.)

## Stale re-translated

None.
