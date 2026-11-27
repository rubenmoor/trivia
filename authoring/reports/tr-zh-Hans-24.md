# tr-zh-Hans-24

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 28 (0 stale re-translated)
- Translated: 28
- Approved: 22
- Needs work: 6
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 82, about $4.66 at list price; $0.15 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-24&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-22 | tr-zh-Hans-23 | tr-zh-Hans-24 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 28 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 28 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 290 | 290 | 22 |
| needs_work |  | 10 | 9 | 6 |
| needs_work rate | ≤ 20.0 % | 3.3 % ✓ | 3.0 % ✓ | 21.4 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 7.1 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.0 % ✓ | 10.7 % ✗ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.3 % ✗ | 1.3 % ✗ | 10.7 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 3.6 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 28 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 98.3 % ✓ | 78.6 % ✗ |
| cost $ |  | $29.13 | $29.09 | $3.27 |
| $ per approved |  | $0.10 | $0.10 | $0.15 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 3 of 22 (14 %)
- Major among review needs work: 3 of 6 (50 %)
- Problems by kind: giveaway 2 (1 major), fact 1 (1 major), overlap 5 (5 major), difficulty 2 (2 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 1 of 28 (4 %)
- Audit/review agreement (both accept or both not): 22 of 28 (79 %)
- Sample: 28 audited of 28; 28 Claude calls, about $1.39

Major findings on approved questions:

- **q-23987**: overlap — The related approved question q-24812 asks the same fact in almost the same words: after "各就各位" and "预备", the next thing is the starting gun. The two questions duplicate each other. The translation itself is accurate and natural: "各就位/预备" are the standard Chinese commands, the options match in form and the fun fact is true. One small nit: hint 2 calls the official 裁判 and hint 3 calls him 发令员. (http://127.0.0.1:8001/review/q-23987)
- **q-25148**: fact, difficulty, overlap — The translation replaced the source's three male distractors (Tenor, Baritone, Bass) with 男高音, 女中音 and 女低音. That changes what the question tests: telling a soprano from a mezzo or alto by ear on a scratchy 1913 recording is much harder than telling a female voice from male ones, so a difficulty of 5 no longer fits. The wrong answers should go back to 男高音, 男中音, 男低音. Also, the related q-24878 ("这首女高音咏叹调出自哪位意大利歌剧作曲家？" → 普契尼) probably uses the same recording, and each question's text answers the other. The answer itself (Alda as Butterfly, a soprano) and the fun fact (born in New Zealand, married to Gatti-Casazza of the Met) are correct. (http://127.0.0.1:8001/review/q-25148)
- **q-25564**: giveaway, difficulty — In Chinese the answer's name, 拟啄木鸟 ("woodpecker-like bird"), gives itself away: the question says the bird is chiselling a nest hole in a tree trunk, and only this option names a woodpecker. Players can pick it without knowing the bird, so the question plays far easier than 5. The facts are right (barbets live in Asia, Africa and the Americas, are close relatives of toucans and have bristles at the bill, and the video shows a blue-throated barbet), but the question text needs reworking, e.g. drop the woodpecker-like action from the clue or ask about the bird another way. (http://127.0.0.1:8001/review/q-25564)

## Needs work

- **q-22454** (strange-creatures) 它的鼻子又长又灵活，走路时总把带环纹的尾巴高高翘起。它是什么动物？ → 南美浣熊: Fact: the answer 南美浣熊 names one species, the South American coati (Nasua nasua). That species does not live in Mexico, so hint 1 ("从墨西哥一直分布到阿根廷") and hint 3 ("在墨西哥常被游客围着投喂") are wrong for it. The source means coatis in general, so the answer should be the genus name 长鼻浣熊 (or the Mexico references should go). Media: the kept image is a raccoon photo (Raccoon_by_water). Both answer names contain 浣熊, so a raccoon picture points straight at the answer in Chinese. The image also shows a different animal from the one asked about. The file needs replacing with a coati photo or a decorative forest image. Fact check: wrong. The image shows a raccoon (query 'raccoon in forest'), not a coati, so it points to the wrong animal. The hint says the range runs 'from Mexico to Argentina'. That is the range of the coati genus. The South American coati (Nasua nasua) does not live in Mexico, and the Mexican coati is the white-nosed coati. The text facts (long snout, ringed tail held upright, rotating hind ankles) are correct.
- **q-22786** (video-games) 在《超级马力欧》游戏里，长得很像图中这种蘑菇的道具会让马力欧怎样？ → 让他变大: This duplicates approved q-21801 in the same bundle. That question also asks what happens when Mario eats a red-and-white spotted mushroom like the one in the picture, and its answer is "他会变大". This is a pool-level duplicate that comes from the source, not from the translation, so one of the two questions should be dropped. The translation itself reads naturally and matches the source.
- **q-23051** (football) 足球比赛的点球要在球门前的罚球点上踢。罚球点离球门线大约多远？ → 11米: This duplicates related q-23860 (approved, 世界杯): "点球大战中你站在点球点上，球门离你大约多远？" with the answer 11米. Both ask how far the penalty spot is from the goal, so one of the two should be dropped from the zh-Hans pool. The translation itself is accurate and natural.
- **q-24811** (athletics) 1986年，哪个田径投掷项目改了器材设计，让它飞得更近，因为顶尖成绩快投出场地了？ → 标枪: Source: the fun fact says 104.80 m is "longer than a soccer field", but a standard international pitch is about 105 m (100–110 m), so the comparison is wrong or at best doubtful. The fact check rated it wrong. Source: hint 2 also gives the answer away, because "its tip sticks in the grass" points to the javelin, the only option with a tip. Both need fixing in the English source first. In the translation, «让它飞得更近» is awkward; «让它飞不了那么远» would read more naturally. Fact check: wrong. The answer (标枪) is right. The 1986 redesign moved the men's javelin's centre of gravity forward, so it lands nose-down and travels less far. Uwe Hohn's 104.80 m on 20 July 1984 is the only throw over 100 m with the old design. The fun fact is shaky, though: a standard international pitch is about 105 m (100–110 m), so 104.80 m is not 'longer than a football pitch'. It is about the same length. I did this from memory and ran no searches.
- **q-25999** (classic-tv-series) 《武林外传》里，白展堂在同福客栈当跑堂，那李大嘴当什么？ → 厨子: Fact check: uncertain. The answer is right: 李大嘴 is the cook (厨子) at 同福客栈. 吕秀才 is the accountant, and the 捕快 is 燕小六, not 李大嘴. The three wrong answers are really wrong, and the hints are fine. I could not verify the fun fact that “大嘴” is a pun on his gluttony and his loose tongue. It reads like an invented explanation. I did not run any searches, so this check rests on my own knowledge of the show.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: The translation itself is accurate and reads naturally. The problem is in the source: q-26256, already approved, asks the same fact (Dong Fang Hong 1 weighs about 173 kg) in other words. Only one of the two questions should stay in the pool. Retiring this one or q-26256, or giving the source a different angle, has to be done at source level.

## Not travelling

None.

## Stale re-translated

None.
