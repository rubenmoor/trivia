# tr-en-25

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `germany` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 294
- Needs work: 5
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 528, about $29.97 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-25&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-23 | tr-en-24 | tr-en-25 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 299 |
| not travelling |  | 1 | 0 | 1 |
| not travelling confirmed |  | 1 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 294 | 295 | 294 |
| needs_work |  | 5 | 5 | 5 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 1.7 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.0 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $27.11 | $24.58 | $27.06 |
| $ per approved |  | $0.09 | $0.08 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), overlap 1 (1 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.90

Major findings on approved questions:

- **q-12032**: overlap — This asks the same fact as the approved q-6322: someone who rides with a lance in a tournament contest is a knight. Seeing one question gives the other away. Apart from that, the translation is faithful and the wording is natural. The options, hints, description and fun fact are fine (Kaltenberg is widely billed as the biggest knights' tournament in the world). The essential jousting image fits, and difficulty 1 is right. (http://127.0.0.1:8001/review/q-12032)

## Needs work

- **q-11077** (series-and-crime) “Club der roten Bänder” aired on VOX from 2015 and follows teenagers on a children's hospital ward. What was it based on? → a series from Spain: Source: the fun fact says Espinosa beat cancer “as a teenager” („als Jugendlicher überstand“). He was ill from about 14 to 24 and spent roughly ten years in hospitals, so he wasn't cured until his early twenties. The source fun fact should say something like “which he fought for ten years from the age of 14”, and then the translation should follow it. The rest of the translation is faithful and natural.
- **q-13091** (plants-and-forests) Which vegetable is this typical German dish made from? → White cabbage: Source: the essential image is titled "Bramborak - close-up", which is a Czech potato pancake, not sauerkraut. The question only names the dish through the picture, so with this file players would see the wrong dish and could reasonably answer "potato". The source's media needs a new sauerkraut photo with no label. The English text itself is a faithful, natural translation.
- **q-13168** (series-and-crime) I've been solving cases on Tatort in Cologne since 1997, my partner is Freddy Schenk, and after a case we often eat currywurst by the Rhine. Who am I? → Max Ballauf: source: Hint 2 is wrong in the source and in the translation. Before Cologne, Max Ballauf was Schimanski's assistant in the Duisburg Tatort (around 1989–1991), not in Düsseldorf. Correct the source to "Duisburg" (or "Schimanski's assistant in Duisburg"), then re-translate. The rest of the translation is faithful and reads naturally.
- **q-14057** (home-and-public-life) In an apartment building, it leads from the front door to the apartments. The mailboxes often hang here, and the light goes off after a few minutes. What is it? → Hallway: Fact check: wrong. The question is based on the German "Treppenhaus" (stairwell). "Hallway" is ambiguous. It could mean the flat's own entrance hall or a floor corridor. The fun fact also mistranslates: "Treppenlichtautomat" means a stairwell light timer, not a hallway one. I did not run a web search, so this rests on my own knowledge of German.
- **q-9230** (federal-republic-and-reunification) Which little black goblin from East German children's TV loves to shout “Ach du meine Güte!” (Oh my goodness!)? → Pittiplatsch: Fact check: wrong. Pittiplatsch's famous catchphrase is "Ach du meine Nase!", not "Ach du meine Güte!". The question text misquotes it. The answer (Pittiplatsch), the wrong answers and the hints are fine. His best friend is the duck Schnatterinchen, and Moppi is a dog.

## Not travelling

- **q-15947** about_language, confirmed: Im Schwäbischen wird aus einem kleinen Stück ein „Stückle“. Was wird dort aus einem Mädchen? → Mädle (Asks how a German word is formed in Swabian dialect (the -le diminutive): a question on German grammar/word forms, not on a regional word's meaning.)

## Stale re-translated

None.
