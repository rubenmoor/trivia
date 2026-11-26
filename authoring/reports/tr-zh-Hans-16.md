# tr-zh-Hans-16

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 290
- Needs work: 10
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 612, about $30.25 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-16&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-14 | tr-zh-Hans-15 | tr-zh-Hans-16 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 292 | 292 | 290 |
| needs_work |  | 8 | 8 | 10 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | 2.7 % ✓ | 3.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.3 % ✓ | 1.3 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 1.0 % ✓ | 1.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 93.3 % ✓ | 95.0 % ✓ |
| cost $ |  | $25.91 | $27.32 | $27.73 |
| $ per approved |  | $0.09 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 1 (1 major), overlap 1 (0 major), difficulty 1 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.52

Major findings on approved questions:

- **q-25509**: giveaway, difficulty — The facts are right: the Anschluss was in March 1938, about 18 months before September 1939, Hitler was born in Braunau, and Austria became independent again in 1945/1955. The problem is the answer. In English, "Anschluss" is an opaque German word, but the Chinese name 德奥合并 just restates the question ("奥地利从此成了德国的一部分" = Germany and Austria merged). Only 德奥同盟 is in competition, and 同盟 (alliance) clearly isn't "becoming part of". So the question text alone answers it, and it plays far easier than 9. One way to fix it in the translation: drop the "成了德国的一部分" clause, or reword it so the text doesn't define 合并. (http://127.0.0.1:8001/review/q-25509)

## Needs work

- **q-24386** (skyscrapers) 很多高塔的顶上有专门让游客看风景的地方。那里常放着什么，能让你把远处的东西看得更清楚？ → 望远镜: Fact check: uncertain. The answer 望远镜 is right, and 潜望镜, 放大镜 and 万花筒 are all wrong. The hints are shakier. Hint 3 ("常有两根并排的镜筒") describes binoculars, not telescopes in general, and many tower viewers are single-tube coin-operated scopes. Hint 1 ("举到眼睛前面") doesn't fit fixed tower viewers either. The fun fact (80+ km from the tallest towers) is roughly plausible: the horizon from about 500 m is around 80 km. I didn't check it against a source, and "世界最高的几座塔" is vague.
- **q-25460** (space-race-and-astronauts) 看视频：这是从载人飞船舷窗拍下的发射画面，飞走的那座尖塔是什么？ → 发射逃逸系统: Fact check: uncertain. The answer (发射逃逸系统) and the wrong answers are fine. The hints are fine: the tower sits above the capsule, its abort motor goes unused on a normal flight, and it is jettisoned about 3 min 18 s after liftoff. I couldn't verify that the Commons file exists. The fun fact's 800 km/h is the top of NASA's range. NASA says 0 to "400–500 mph in two seconds", and 400 mph is the figure it quotes most (about 645 km/h). 800 km/h equals about 497 mph.
- **q-25870** (chinese-folk-music) 看这张二胡的特写。二胡、京剧的京胡和板胡，都属于哪一类中国乐器？ → 胡琴: Giveaway: in Chinese the question names 二胡, 京胡 and 板胡, and 胡琴 is the only option with 胡, so players can match the character without knowing anything. Hint 2 doesn't need to help and hint 3 says it outright. The source has the same flaw in a milder form (the "hu" in the pinyin). Overlap: approved q-27107 calls the jinghu a 胡琴 outright, so seeing that question gives this one away. A reworded translation can't fix this, because any Chinese wording has to name 二胡; the source question needs to be rethought or this item dropped.
- **q-26469** (chinese-tech-brands) 中国城市里有些车牌是绿色的，比蓝牌多一个字符，还常常不受限行限制。哪种车挂这种车牌？ → 电动汽车: Fact check: wrong. The answer (电动汽车/新能源汽车: green plate, 8 characters vs 7 for blue, often exempt from traffic restrictions) is right. But the distractor 出租车 is not clearly wrong. Many cities, such as Shenzhen, run mostly electric taxis, and these carry green new-energy plates. Police cars and military trucks use other plates (white), so they are fine. I checked this from memory, not with a search.
- **q-26585** (martial-arts) 一个圆分成黑白两半，每一半里有一个另一种颜色的点，代表阴和阳。它叫什么？ → 太极图: Overlap, inherited from the source: q-26585 asks the same fact as the approved q-27366 ("a circle split into black and white halves, each with a dot of the other colour" → 太极图), in nearly the same words. One of the two should be dropped from the pool. Small wording note if it is kept: in the description, «一比之下» should be the standard «相比之下».
- **q-26831** (spring-festival) 有些厨师做一整碗长寿面，用的是几根面条？ → 1根: Fact check: uncertain. Answer 1根 is plausible (longevity noodles are one unbroken strand, and Shaanxi has a "一根面" dish). I did not search for it. I could not confirm the "几米" length or the claim that some chefs make a whole bowl from one noodle. The description also says nothing specific about the answer.
- **q-27202** (chinese-video-games) 刘亦菲曾在电视剧《仙剑奇侠传》中饰演赵灵儿。她主演的迪士尼电影《花木兰》哪一年上映？ → 2020年: Fact check: wrong. The answer (2020) is right. The wrong answers 2009, 2015 and 2024 are wrong. But the fun fact is false: Liu Yifei was born in 1987 and played Zhao Linger in the 2009 series (filmed 2008) when she was about 21, not a teenager. Hint 1 is also misleading: she became famous earlier, through 《金粉世家》 and 《天龙八部》 in 2003. Both claims come from my own recall of her biography, and I did not run searches to confirm them.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: This asks the same fact as approved q-26256 (the weight of Dong Fang Hong 1, answer about 173 kg). Seeing one gives the other away, so one of the two should be dropped. The translation itself is faithful and natural.
- **q-27568** (renminbi-and-old-coins) 商店价签上写着¥2.50。这一共是多少角？ → 25: Fact check: wrong. ¥2.50 is 2元5角 = 25角 total (2元=20角 + 5角). Answer 25 is correct. But the question says '多少角' and the hint '小数点后面的数表示角' is fine; the problem is that distractor '250' is wrong, '52' wrong, '205' wrong, so those are okay. Issue: the description ('唯一一种拿零食当奖励的作业') is nonsensical and unrelated, and the fun fact '两块五毛' is acceptable colloquially (毛=角).
- **q-27572** (renminbi-and-old-coins) 春节包饺子时，人们说饺子的形状能招财，因为它像什么？ → 元宝: Fact check: uncertain. Dumplings are said to resemble 元宝 (gold/silver ingots), which is the standard folk explanation, so the answer is right. However, 铜钱 as a distractor is arguable, since some say dumplings resemble money generally. Hint 1 '旧时有钱人家藏在箱子里' and hint 3 'a boat with two ends upturned' fit 元宝. Coin-in-dumpling fun fact is true. Not verified via search.

## Not travelling

None.

## Stale re-translated

None.
