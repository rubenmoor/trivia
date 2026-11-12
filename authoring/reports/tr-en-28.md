# tr-en-28

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `germany` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 290
- Needs work: 7
- Not travelling: 3 (2 confirmed → `translatable: false`, 1 translated again next run)
- Claude calls: 522, about $30.91 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-28&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-26 | tr-en-27 | tr-en-28 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 299 | 297 |
| not travelling |  | 1 | 1 | 3 |
| not travelling confirmed |  | 1 | 0 | 2 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| approved |  | 289 | 290 | 290 |
| needs_work |  | 10 | 9 | 7 |
| needs_work rate | ≤ 20.0 % | 3.3 % ✓ | 3.0 % ✓ | 2.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.3 % ✓ | 2.3 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.73 | $25.38 | $27.78 |
| $ per approved |  | $0.10 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), overlap 1 (0 major), style 4 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.13

Major findings on approved questions:

None.

## Needs work

- **q-12126** (winter-sports) What is this machine at the edge of the ski slope? → Snow cannon: This duplicates the approved q-4990 (“Look closely at this machine on a ski slope. What is it?” → A snow cannon). English players would get the same photo question with the same answer twice. Drop one of the two from the English pool. The translation itself is faithful and reads naturally.
- **q-13091** (plants-and-forests) Which vegetable is this typical German dish made from? → White cabbage: The translation is faithful and natural. The problem is the essential image kept from the source, titled "Bramborak - close-up - Koliba AUD5.90". That title points to a Czech potato pancake, not a bowl of sauerkraut. The question depends on the picture ("this typical German dish"), so the source's media needs to be swapped for a clear sauerkraut photo.
- **q-13168** (series-and-crime) I've been solving cases on “Tatort” in Cologne since 1997, my partner is Freddy Schenk, and after a case we often eat currywurst by the Rhine. Who am I? → Max Ballauf: Source: hint 2 is wrong in the German source and the translation repeats it. Before Cologne, Max Ballauf was Horst Schimanski's assistant in Duisburg, not Düsseldorf. The source hint should say Duisburg (or be replaced), and then the translation should follow it.
- **q-15042** (gdr-everyday-life) East German apartment ads often said “Zweiraumwohnung,” typical for Plattenbau blocks and still common in the East. What does it mean? → Two rooms plus kitchen and bathroom: Fact check: wrong. The answer is correct: a Zweiraumwohnung has two living or sleeping rooms plus a separate kitchen and bathroom, the same as a Zweizimmerwohnung. The wrong answers are wrong and the fun fact is fine. The problems are in the hints and description. Hint 2 ('the two counts something every apartment has') is misleading, because the 'two' does not count the kitchen and bathroom that every apartment has. Hint 1 is vague. Hint 3 almost gives the answer away. The description says Westerners 'have to do the math', but the term is simply equivalent to Zweizimmerwohnung, so no calculation is needed.
- **q-16931** (federal-republic-and-reunification) Complete the sentence: “The Bundestag in Berlin is …” → Germany's parliament: source: the German fun fact is wrong. It says the "Tag" in Bundestag comes from "tagen" and has nothing to do with the day. In fact "tagen" comes from "Tag" (the fixed day of the assembly). The English translation already gives the correct version, so only the German source fun fact needs changing.
- **q-9211** (empire-weimar-and-nazi-era) You're watching “Babylon Berlin,” set in 1929. Which object really shouldn't show up in it yet? → Ballpoint pen: Source: hint 2 says the ballpoint pen "wasn't patented until the late 1930s," which is false. John J. Loud patented a ballpoint pen in 1888; what came in 1938 was Bíró's practical pen. Reword the source hint, e.g. "The first one that wrote well was patented in 1938," then re-translate. The rest of the translation is faithful and natural.
- **q-9230** (federal-republic-and-reunification) Which little black goblin from East German children's TV loves to cry “Ach du meine Güte!” (Oh my goodness!)? → Pittiplatsch: Fact check: wrong. Pittiplatsch's catchphrase is "Ach du meine Nase!", not "Ach du meine Güte!". The rest (answer, wrong answers, hints, fun fact) appears correct. This is from memory and I did not search.

## Not travelling

- **q-13003** about_language, translate again: Ergänze: Wasser, das zu Hause direkt aus dem Wasserhahn kommt, nennt man … → Leitungswasser (Asks for the everyday German word for tap water (hint plays on “Leitung” = pipe); in English it becomes a vocabulary test or trivially “tap water”.)
- **q-11059** other, confirmed: Wer früh aufsteht, hat einen Vorsprung, sagt das Sprichwort: „Der frühe Vogel fängt den …“ → Wurm (The German proverb is word for word the English “The early bird catches the worm”. In English it's a base fact with no German link left, and the fun fact (it exists in English too) falls apart.)
- **q-14154** other, confirmed: In Berlin stehen viele bunt bemalte Buddy Bären mit erhobenen Armen. Was bedeutet das englische Wort „Buddy“? → Kumpel (The question asks German speakers what the English word “buddy” means; for English-speaking players it asks about their own everyday word, so it is trivial.)

## Stale re-translated

None.
