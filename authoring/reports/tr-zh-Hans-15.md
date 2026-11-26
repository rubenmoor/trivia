# tr-zh-Hans-15

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 604, about $29.79 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-15&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-13 | tr-zh-Hans-14 | tr-zh-Hans-15 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 293 | 292 | 292 |
| needs_work |  | 7 | 8 | 8 |
| needs_work rate | ≤ 20.0 % | 2.3 % ✓ | 2.7 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.3 % ✓ | 2.3 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 1.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 98.3 % ✓ | 93.3 % ✓ |
| cost $ |  | $25.47 | $25.91 | $27.32 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 58 (3 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), overlap 2 (2 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.47

Major findings on approved questions:

- **q-26225**: overlap — Related q-27415 asks what Sun Wukong's tail became when he turned into a temple to hide from 二郎神 (answer: 旗杆). This question's fun fact states that answer, and q-27415's text names 二郎神 as the one hunting him in the transformation contest, so each question gives the other away. The translation itself is faithful and reads naturally, and the facts check out: he is the Jade Emperor's nephew, he wields a 三尖两刃枪, he has a third eye, and his dog helps capture Wukong. (http://127.0.0.1:8001/review/q-26225)
- **q-26595**: overlap — The translation is faithful and accurate: 三彩 counts the main glazes (yellow, green, white or brown), and most pieces were made as tomb goods. The problem is related question q-26980 in the same bundle and subcategory. It writes “唐三彩” out in full in its question text, so any player who has seen it already knows this answer. That overlap is in the source too. Smaller point: the media file title “Tang Sancai Horse” spells out sancai (三彩), but players only see the picture, not the title. (http://127.0.0.1:8001/review/q-26595)

## Needs work

- **q-25811** (chinese-cartoons) 我们的恒星和绕着它转的一切，比如八大行星、它们的卫星和彗星，合在一起叫什么？ → 太阳系: The description «太阳是唯一的一盏路灯» names 太阳 (Sun), and with only the options in view that points straight to 太阳系. Unlike the English, where "Sun" and "Solar System" don't share a word, this gives the answer away in Chinese. Rewrite the description to play on the cosmic-neighbourhood theme without 太阳 or 恒星. Optionally, also drop 太阳 from hint 3 («海王星是其中最远的行星»).
- **q-26079** (dialects) 台湾很多人说这种话，他们的祖先来自泉州和漳州，名曲《爱拼才会赢》也用它演唱。是哪种语言？ → 闽南语: Fact check: wrong. The answer 闽南语 and the hints and fun fact are correct. The wrong answer 潮州话 is a problem. Teochew is a Southern Min (闽南语) variety, so it is arguably also correct. This makes the question ambiguous.
- **q-26325** (mythical-creatures) 我侍奉西王母，替她传递消息。李商隐曾托我去探望心上人。我是谁？ → 青鸟: source: this asks the same thing as approved q-26171 (青鸟 as 西王母's messenger, and 李商隐 sending it to visit a loved one), with the same answer, so one of the two should be dropped. The translation itself is faithful and reads naturally.
- **q-26469** (chinese-tech-brands) 在中国城市里，有些车牌是绿色的，比蓝牌多一个字符，还常常不受限行限制。哪种车用这种车牌？ → 新能源汽车: Fact check: uncertain. The answer and fun fact are correct. Green plates are for new energy vehicles (NEVs), and they have 8 characters against 7 on blue plates. NEVs are often exempt from driving restrictions. The weak point is the distractor 出租车 (taxi). Electric taxis are NEVs, and in many Chinese cities they carry green plates. A player could fairly argue that taxis also use this plate. Police cars and military trucks use white plates, so those two distractors are fine. I did not run web searches. This check comes from my own knowledge.
- **q-26585** (martial-arts) 一个圆分成黑白两半，每一半里都有一个另一种颜色的小圆点，代表阴和阳。它叫什么？ → 太极图: Source problem: this asks the same thing as approved q-27366 (a circle split into black and white halves, each with a dot of the other colour → 太极图), so one of the two should be dropped. The translation itself reads naturally. One small point: hint 3 says the name is the same as (相同) the martial art's, but 太极图 and 太极拳 only share the first two characters (太极). If this item is kept, change it to something like «它的名字前两个字和……拳法一样».
- **q-26831** (spring-festival) 有些厨师只用多少根面条，就能做成一整碗长寿面？ → 1根: The fun fact doesn't match the source. The source says the single noodle "can be several metres long". The translation instead says it is usually just over 1 m and at most about 2 m. The fact check says the 2 m figure comes from Yangling dipping noodles (蘸水面), not from 一根面, so these new numbers are unconfirmed and probably wrong. Follow the source, e.g. «陕西有名的“一根面”，一碗只有一根面条，能有好几米长。» The question, options and hints are fine. Fact check: uncertain. Answer 1 is fine. The fun fact is shaky. The 'two metres' claim comes from Yangling dipping noodles (裤带面), not the 一根面 dish. Some sources also place 一根面 in Shanxi, not Shaanxi.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: Source-level problem: q-27533 asks the same fact as the already approved q-26256 (how heavy 东方红一号 was, answer about 173千克). Seeing one gives the other away. One of the two should be dropped or turned into a different question. The translation itself is faithful and reads naturally.
- **q-27665** (board-and-tile-games) 我曾是世界排名第一的围棋棋手。2017年5月，我在乌镇围棋峰会上三局全败给AlphaGo。我是谁？ → 柯洁: Fact check: uncertain. The answer (柯洁) and the question text are correct. Ke Jie was world No.1, born 2 Aug 1997, so he was 19 in May 2017. He lost 0-3 to AlphaGo at the Wuzhen Future of Go Summit. Lee Sedol (Korean, lost 1-4 in 2016), Gu Li and Nie Weiping are all valid wrong answers. The hints are true, and 柯 is pinyin Kē. The fun fact is true: DeepMind announced that Wuzhen was AlphaGo's last competitive match. The one problem is the description, '这场峰会的贵宾,宴席上的菜一口都没吃'. It is a riddle that seems to point to AlphaGo, an AI guest that can't eat. It doesn't describe Ke Jie, and I couldn't verify it as a fact about him. I did this from memory without running searches.

## Not travelling

None.

## Stale re-translated

None.
