# tr-zh-Hans-19

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 289
- Needs work: 11
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 591, about $33.11 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-19&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-17 | tr-zh-Hans-18 | tr-zh-Hans-19 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 290 | 290 | 289 |
| needs_work |  | 9 | 10 | 11 |
| needs_work rate | ≤ 20.0 % | 3.0 % ✓ | 3.3 % ✓ | 3.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.7 % ✓ | 1.7 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 1.0 % ✓ | 1.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 1.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $28.52 | $30.29 | $30.30 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 1 (0 major), overlap 1 (0 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.80

Major findings on approved questions:

None.

## Needs work

- **q-21907** (prehistory) 下面的古人类中，有三种是以化石发现地命名的。哪一种不是？ → 能人: In Chinese the answer 能人 literally means "capable person". It plainly describes an ability and not a place, while the three wrong options are visibly place-name transliterations (丹尼索瓦, 尼安德特, 弗洛勒斯). The question collapses in Chinese: anyone can solve it from the options alone, without knowing anything about the fossils. Every standard Chinese name for a Homo species not named after a place (能人, 直立人, 智人) is a translated meaning, so swapping the answer doesn't help. This translation should be marked travels: no (other: the answer's Chinese name translates its own clue).
- **q-23987** (athletics) 短跑起跑时你蹲在起跑线上，裁判先喊“各就位”，再喊“预备”。你什么时候起跑？ → 发令枪响时: Source problem: this question asks the same thing as approved q-24812 ("各就各位" → "预备" → the starting gun fires) in almost the same words, so the pool would have the same question twice. The translation can't fix that. Retire one of the two, or make one of them about a different fact.
- **q-24268** (famous-bridges) 我高高悬在丛林河流上方，是用“藤本植物”编成的。藤本植物是什么？ → 长长的木质茎蔓: The source asks what the English loanword "lianas" means. In Chinese the term 藤本植物 explains itself (藤 = vine, 植物 = plant), so the question names its own answer. It is also the only option that is a living plant, while the wrong answers are dead materials. The riddle's "我" is the bridge, but the question asks about the lianas, which reads oddly. Suggested rebuild: ask what the bridge is woven from, without naming the material ("我是用丛林里什么东西编成的？"), with the answer 藤蔓 against bamboo, palm leaves and bark strips. Otherwise mark it travels: no (about_language).
- **q-24409** (deserts) 绿洲是沙漠里有棕榈树和水的一片绿地。它的水是从哪里来的？ → 来自地下: Source: the wrong answer "From melting snow" is defensible for Chinese players. Chinese middle-school geography teaches that Xinjiang's oases (Turpan, Hotan and others) are fed by snowmelt from the high mountains, which seeps underground and resurfaces or is tapped through karez (坎儿井). The source should swap that distractor for one that is clearly wrong, such as water from rivers flowing in from the sea, or water brought by camels. The translation itself is faithful and natural.
- **q-24811** (athletics) 1986年，田径哪个投掷项目改了器材设计，让它飞得近一些，因为顶尖成绩快扔出场地了？ → 标枪: source: the fun fact says Hohn's 104.80 m throw was longer than a soccer field (比一个足球场还长). The standard international pitch is 105 m, so this comparison is doubtful, and Chinese players know 105 m as the standard length. Change the source to something like 'almost as long as a standard soccer field', then translate it again. Apart from that, the translation is faithful and natural. Fact check: uncertain. The answer (标枪) is right. The javelin was redesigned in 1986 for the men's event, with the center of gravity moved forward so it lands tip-down sooner. Uwe Hohn's 104.80 m in 1984 is correct. The claim that it is 'longer than a football field' is shaky. A standard international pitch is 105 m, which is slightly longer than 104.80 m. Pitch length varies, so the claim depends on which pitch you mean. This is from memory, and I ran no searches.
- **q-25170** (world-currencies) 钞票并非一枚枚单独印刷，而是几十个票面一起印在一大块平整的东西上，再裁开。它们是印在什么上的？ → 纸张: The translation uses the wrong measure word: «一枚枚» is for coins, not banknotes, so it reads as unnatural to mainland readers. The translator chose it to avoid 张, but «一张一张地»/«逐张» or «不是单独印出来的» would work without the odd 枚. It also changes the question from what the piece is called (sheet) to what material it is (paper). That makes it easier, but it still holds as a level-2 item.
- **q-25999** (classic-tv-series) 在《武林外传》里，白展堂是跑堂，那李大嘴是什么？ → 厨子: Fact check: uncertain. The answer 厨子 is right: 李大嘴 is the cook at 同福客栈, 吕秀才 is the accountant, and 白展堂 is the waiter (跑堂). The wrong answers 账房, 捕快 and 门房 don't fit. The 捕快 distractor is a little risky, because 李大嘴 was a 捕头 in the story before he became the inn's cook, but he isn't one at the inn. I found no source for the fun fact's claim that 大嘴 is a pun on both his appetite and his loose tongue. The hint '他在同福客栈的后面干活' is vague but acceptable.
- **q-26325** (mythical-creatures) 我替西王母传递消息，李商隐还托我去探望心上人。我是谁？ → 青鸟: Source: this question asks the same fact as approved q-26171: the bluebird (青鸟) that serves Xiwangmu and that Li Shangyin sends to visit his beloved, with almost the same clues. Both would be in the zh-Hans pool, so one of them should be dropped or this one rebuilt on a different fact. The translation itself is faithful and natural.
- **q-26469** (chinese-tech-brands) 在中国城市，有些车牌是绿色的，比蓝牌多一位，还常常不受限行限制。挂这种车牌的是什么车？ → 新能源汽车: Fact check: wrong. The answer 新能源汽车 and the fun fact are correct. Green NEV plates have 8 characters and blue plates have 7. NEVs are often exempt from purchase and driving restrictions. But the wrong answer 出租车 is not clearly wrong. Many Chinese cities, such as Shenzhen, run all-electric taxis, and those taxis carry green NEV plates. This makes the question ambiguous. I checked this from memory and ran no web searches.
- **q-26831** (spring-festival) 有些厨师做一整碗长寿面，一共用几根面条？ → 1根: source: the fun fact's claim that Shaanxi's famous "一根面" is a single noodle several metres long is not confirmed. The fact check ties the dish named "一根面" mainly to Sichuan (Huanglongxi) and Shanxi. Shaanxi's single-noodle bowl is Yangling 蘸水面 (裤带面), said to be only about 2+ metres long. Correct the source's fun fact (e.g. "陕西杨凌的蘸水面一碗只有一根面条，据说能长达两米多。"), then re-translate. The rest of the translation is faithful and natural. Fact check: wrong. The answer (1根) and the distractors are fine. The fun fact is shaky. "一根面" as a named dish is mainly tied to Sichuan (Huanglongxi) and Shanxi, not Shaanxi. Shaanxi's one-noodle-per-bowl dish is Yangling dipping noodles (杨凌蘸水面, 裤带面). Its longest noodles are said to reach only about 2+ metres, not "好几米".
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: This duplicates approved q-26256, which asks the same fact (how heavy Dong Fang Hong 1 was, answer about 173 kg). One of the two should be retired. The translation itself is accurate and natural.

## Not travelling

None.

## Stale re-translated

None.
