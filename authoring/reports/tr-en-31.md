# tr-en-31

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `germany` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 495, about $30.74 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-31&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-29 | tr-en-30 | tr-en-31 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 298 | 297 | 300 |
| not travelling |  | 2 | 3 | 0 |
| not travelling confirmed |  | 1 | 3 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 1.0 % ✓ | 0.0 % ✓ |
| approved |  | 293 | 289 | 295 |
| needs_work |  | 5 | 8 | 5 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 2.7 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.3 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 1.0 % ✗ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 100.0 % ✓ |
| cost $ |  | $28.25 | $27.57 | $27.55 |
| $ per approved |  | $0.10 | $0.10 | $0.09 |
| **health** | | ✓ pass | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: giveaway 3 (1 major), overlap 2 (0 major), media 2 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.19

Major findings on approved questions:

None.

## Needs work

- **q-12126** (winter-sports) What is this machine at the edge of the ski slope? → Snow cannon: This duplicates approved q-4990 ("Look closely at this machine on a ski slope. What is it?" → snow cannon). It asks the same thing from a photo with the same answer, so players who meet both get the answer handed to them. The translation itself is accurate and reads naturally. Keep only one of the two questions, or turn this one into a different question about snowmaking with a real German link.
- **q-13024** (holidays-through-the-year) Saint Martin cut his cloak for a freezing beggar. Into how many pieces? → 2: This duplicates approved q-10835 ("In the song “Sankt Martin ritt durch Schnee und Wind”, Martin cuts his cloak with his sword. Into how many pieces?" → 2). Both ask the same fact with the same answer, so one of the two should be dropped from the English pool. Note that the duplicate is also in the German source pool.
- **q-16067** (rap-and-electronic) Which word became Germany's Jugendwort des Jahres (youth word of the year) in 2012? → YOLO: The translation dropped the source's spelled-out meaning (“You only live once”), so the description now carries the clue: calling the word “a life motto” picks out YOLO, because Swag, Babo and Smombie are not mottos. Rewrite the description to joke about youth slang or the yearly vote without saying the word is a motto or saying.
- **q-16931** (federal-republic-and-reunification) Complete the sentence: “The Bundestag in Berlin is …” → Germany's parliament: Source: the fun fact is wrong. The "Tag" in Bundestag/Reichstag comes from "Tag" (day), meaning a day set for an assembly, and "tagen" comes from it too. So it is false that it has nothing to do with "day". The English version makes the claim even stronger ("nothing to do with the German word for 'day'"). Fix the source fun fact first (for example: "The 'Tag' in Bundestag means an assembly; it comes from the old sense of 'Tag' as a day set for a meeting, which is also where 'tagen' comes from"), then translate it again. Fact check: wrong. The fun fact is misleading. "Tag" in Bundestag does mean an assembly or meeting, and "tagen" (to meet) is related. But both come from the ordinary word "Tag" (day), meaning a day appointed for a meeting. So it is not true that it has nothing to do with the word for "day". The answer and the wrong answers are fine.
- **q-9230** (federal-republic-and-reunification) Which little black goblin from East German children's TV loves to shout “Ach du meine Güte!”? → Pittiplatsch: source: the fact check says Pittiplatsch's catchphrase is “Ach du meine Nase!”, not “Ach du meine Güte!”. I can't confirm “Güte” myself. The fix belongs in the German source, which should switch to “Ach du meine Nase!”. The translation can then follow it. Apart from that, the translation is faithful and reads naturally. Fact check: wrong. Pittiplatsch's catchphrase is "Ach du meine Nase!", not "Ach du meine Güte!". The question's clue is therefore wrong. The answer, the wrong answers and the hints are fine.

## Not travelling

None.

## Stale re-translated

None.
