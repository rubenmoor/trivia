# tr-zh-Hans-3

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 295
- Needs work: 2
- Not travelling: 3 (3 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 591, about $24.37 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-3&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-1 | tr-zh-Hans-2 | tr-zh-Hans-3 |
|---|---|---:|---:|---:|
| sources |  | 50 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 50 | 300 | 297 |
| not travelling |  | 0 | 0 | 3 |
| not travelling confirmed |  | 0 | 0 | 3 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 1.0 % ✓ |
| approved |  | 50 | 296 | 295 |
| needs_work |  | 0 | 4 | 2 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 1.3 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 88.0 % ✗ | 88.3 % ✗ | 78.3 % ✗ |
| cost $ |  | $5.22 | $24.13 | $22.51 |
| $ per approved |  | $0.10 | $0.08 | $0.08 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 13 of 60 (22 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 5 (3 major), media 15 (13 major), style 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 47 of 60 (78 %)
- Sample: 60 audited of 60; 60 Claude calls, about $1.86

Major findings on approved questions:

- **q-21369**: media — The essential image is missing (media title is null), but the question only asks about "this close-up" (看看这张特写), so it can't be played without a close-up photo of a pine cone. The translation itself is faithful and natural; at most, "真圣诞树" in hint 3 reads a little like translationese. The hints are true, the fun fact about cones opening when dry is true, and the difficulty of 3 fits. (http://127.0.0.1:8001/review/q-21369)
- **q-21788**: media — The media is marked essential, but no file was picked (title null), so the question opens with “看照片” and then shows no photo. The rest of the translation checks out: it is faithful to the source, the Chinese names follow standard forms (赫拉克勒斯, 阿喀琉斯, 珀耳修斯, 奥德修斯), and the hints and fun fact are correct (Nemean lion as the first labour, Disney's 1997 film). There's no real overlap with q-23031, which asks about the Disney film 《大力士》, and difficulty 7 fits. (http://127.0.0.1:8001/review/q-21788)
- **q-22113**: media, giveaway — The media is marked essential, but no file was picked (title null). The question «这个东西是用来做什么的？» can't be played without a photo of a digital clock. The translation itself is faithful and natural. The fun fact is true: the Hamilton Pulsar LED watch went on sale in 1972. One more point, which comes from the source and is minor: the description (no hands, no ticking, glowing numbers) already says it's a clock, so it rules out all three wrong options. (http://127.0.0.1:8001/review/q-22113)
- **q-22364**: media — The audio is essential, but no file has been picked (media title is null), so the question can't be played. The translation itself is faithful and reads naturally. I checked that the answer and wrong options use the standard mainland names (曼陀林/班卓琴/竖琴/尤克里里), that the hints and fun fact are true (8 strings in 4 pairs, pear-shaped body, Neapolitan mandolin), that the description gives nothing away, and that difficulty 10 is reasonable for picking out a mandolin by ear. (http://127.0.0.1:8001/review/q-22364)
- **q-22470**: media — The media is marked essential, but no file was picked (title null), and the question begins with "看看这个器官". Without a picture of a brain, that opening points at nothing on screen. The translation itself is faithful and natural, and the fact holds: motor pathways cross in the medulla, so the right hemisphere mainly controls the left side. The wrong option "都不管，只管思考" is noticeably longer than the other three, which is a minor issue. (http://127.0.0.1:8001/review/q-22470)
- **q-22497**: media, giveaway — Media is marked essential but no file was picked (title null), and hint 3 "数一数照片里的叶子" relies on that photo. Any essential photo of a four-leaf clover would also show the answer outright. The description "比兄弟们多长了一片叶子" states the answer's defining trait (one leaf more than the usual three) and points straight to 四叶草 before any hint. That problem comes from the source. The translation itself is faithful and reads naturally, and the facts check out (about 1 in 10 000 clovers has four leaves). (http://127.0.0.1:8001/review/q-22497)
- **q-22930**: media — The media is marked essential but no file was picked (title null), and the question text points to a picture ("像这样的巨型南瓜"), so on screen it refers to an image that isn't there. The translation itself is faithful and reads naturally. I checked the fun fact: Travis Gienger's 2023 pumpkin weighed 1247 kg (2749 lb), which matches. Swapping apple for watermelon in hint 3 is a harmless change. (http://127.0.0.1:8001/review/q-22930)
- **q-23006**: media — The media role is essential, but no file was picked (title null). The question opens with «这道亮线» ("this bright line"), so it needs a long-exposure photo of a space station's trail and doesn't make sense without one. The translation itself is faithful and natural, and I found no fact problems: the ISS crosses the sky in about 5 minutes, shines steadily and orbits in about 90 minutes, and a comet, meteor or plane doesn't match the clue. The hints and description don't give the answer away. (http://127.0.0.1:8001/review/q-23006)
- **q-23209**: media — The media is set to essential, but no file was picked (title null). The question text says "像这样寄给埃及法老的信件", so it refers to a picture that never appears on screen, and an Amarna letter tablet needs to be attached. The translation itself matches the source: the facts check out (Akkadian was the diplomatic lingua franca of the Amarna period, and the letters were found in 1887, with more than 350 surviving), the options and hints don't give the answer away, and the Chinese reads naturally. (http://127.0.0.1:8001/review/q-23209)
- **q-23512**: media — The media role is essential video, but no file was picked (title null). The question says "这段视频拍的是…", so on the TV it would point to a video that isn't there. The translation itself is faithful and reads naturally. 季风 is correct and the three wrong answers (台风, 海啸, 暴风雪) are clearly wrong. Hint 3 was reworked well around the character 季 and doesn't contain it. The fun fact holds up, and difficulty 6 fits. (http://127.0.0.1:8001/review/q-23512)
- **q-23554**: media — The media role is essential but no file was picked (title null), and the question points at a picture ("这件布满齿轮的青铜装置"). Without a photo of the Antikythera mechanism it doesn't work as written. Everything else checks out: the translation matches the source, the answer is right (the wreck lies off Antikythera, Greece), the options are clean, the hints and fun fact are accurate, and the Chinese reads naturally. (http://127.0.0.1:8001/review/q-23554)
- **q-23559**: media, giveaway — The media is essential, but no file was picked (title null). The question says «看看这架飞机», so it can't be played without a clear photo of an air ambulance. The translation itself is faithful and reads naturally. One smaller issue: the description «只查脉搏» (it only checks your pulse) points straight to the medical answer before any hint. (http://127.0.0.1:8001/review/q-23559)
- **q-23865**: media — The essential image is missing (media title is null), but the question asks players to "look closely at this machine" (仔细看看……这台机器), so it can't be played without the picture. The translation itself is faithful and reads naturally. The options are parallel and the hints are fine. The fun fact is true: Beijing 2022 used almost entirely artificial snow. (http://127.0.0.1:8001/review/q-23865)

## Needs work

- **q-21643** (cats) 在按世界犬业联盟（FCI）规则举办的正式敏捷赛中，狗要绕着绕杆穿行。绕杆一共有几根？ → 12: Fact check: uncertain. I could not read the FCI regulation text, because the PDFs would not parse. Other sources say a weave set is 5–12 poles (Wikipedia), 6 or 12 (UK Kennel Club) or 12 maximum (AKC). Competition sets are normally 12 poles, so 12 is very likely right. I did not find an explicit FCI sentence setting the count at 12. The fun fact is broadly true: agility began at Crufts in the late 1970s in the UK, with courses modelled on horse jumping.
- **q-23514** (volcanoes) 金星上最高的火山以一位古埃及真理女神命名。2023年，旧雷达图像显示它的一个火山口变了形状。它叫什么？ → 玛阿特山: source: Hint 2 is wrong in the English source and carried over into the translation. Maat Mons rises about 8–9 km above Venus's mean planetary radius, but only about 5 km above the surrounding plains. Correct the source's hint 2, for example to "about 8 km above Venus's average surface level", then re-translate it (e.g. 它比金星的平均地表高出约8公里). A smaller point: the description's «脾气最高的一个» is a literal rendering of "tallest grump" and reads awkwardly in Chinese. Fact check: wrong. The answer, distractors, Magellan hint, feather hint and fun fact all fit. Hint 2 is imprecise. Maat Mons is about 8 km above Venus's mean planetary radius (the datum). It stands only about 5 km above the surrounding plains. I did not run a search this session, so this rests on my recall of the Wikipedia and NASA figures.

## Not travelling

- **q-22779** about_language, confirmed: “Ukiyo-e” is to Japanese woodblock prints as which word is to four-panel comic strips? → Yonkoma (Asks for the Japanese word for four-panel comics; in Chinese the term is 四格漫画/四コマ, so the answer is the clue itself, and romaji options would mean nothing to Chinese players.)
- **q-22743** about_language, confirmed: A neurologist treats problems in which group of body parts? → Brain, spinal cord and nerves (The question relies on the opaque English word 'neurologist'; in Chinese the title is 神经科医生, which literally says 'nerves' and gives away the answer (and the 'tongue twister' joke is lost).)
- **q-22997** other, confirmed: Beams like these shoot across the sky at concerts. What is a laser beam made of? → Light (The Chinese word for laser, 激光 (literally 'excited light'), contains the answer 光. Any natural wording gives it away, and 镭射 is not standard mainland usage.)

## Stale re-translated

None.
