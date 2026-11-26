# tr-zh-Hans-20

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 288
- Needs work: 11
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 527, about $32.17 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-20&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-18 | tr-zh-Hans-19 | tr-zh-Hans-20 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 290 | 289 | 288 |
| needs_work |  | 10 | 11 | 11 |
| needs_work rate | ≤ 20.0 % | 3.3 % ✓ | 3.7 % ✓ | 3.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 1.3 % ✓ | 3.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 1.0 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 1.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $30.29 | $30.30 | $29.28 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: fact 1 (0 major), overlap 1 (1 major), style 4 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.89

Major findings on approved questions:

None.

## Needs work

- **q-21907** (prehistory) 以下人类群体中，有三个是以化石发现地命名的。哪一个不是？ → 能人: source: the fun fact is overstated. It says almost everything we know about Denisovans comes from the DNA in one finger bone, but Denisovans are now also known from teeth, the Xiahe jaw (identified by protein in 2019) and the Harbin skull (identified as Denisovan in 2025). The source fun fact should be softened, for example to say that the first Denisovan genome was read from a single finger bone, and the translation then follows it. The rest of the translation is faithful and natural.
- **q-23987** (athletics) 你蹲在短跑起跑线上，裁判先喊“各就位”，再喊“预备”。你什么时候开始跑？ → 发令枪响的时候: Source: this asks the same fact as approved q-24812, almost word for word: a sprint start, “各就位/各就各位”, “预备”, then the starting gun. Players who see one already know the answer to the other. One of the two should be dropped. A translation fix can't solve this.
- **q-24265** (wonders-of-the-world) 救世基督像矗立在里约热内卢的科尔科瓦多山顶。这座山大约有多高？ → 约700米: Fact check: wrong. The text facts are right. Corcovado is about 710 m high. The statue is 30 m tall, not counting its 8 m pedestal, and its arm span is 28 m. The wrong answers are clearly wrong, and the hints hold: under 1 km, over 500 m, and about twice the Eiffel Tower (~330 m). The media query is the problem. It asks for "Rio de Janeiro Sugarloaf Mountain", which is a different peak (Pão de Açúcar, ~396 m). The image would not show Corcovado or the statue.
- **q-24811** (athletics) 1986年，哪个田径投掷项目改了器材设计让它飞得更近，因为顶尖选手快要扔出场地了？ → 标枪: source: the fun fact says Uwe Hohn's 104.80 m throw was "longer than a soccer field", but the standard international pitch is 105 m, so 104.80 m is a little shorter. The translation repeats the claim faithfully, so the source needs fixing first. Suggested replacement: say it was the first throw over 100 m, which led to the 1986 redesign. Don't call it the current world record. Small wording point: «让它飞得更近» reads awkwardly; «让它飞不了那么远» is more natural. Fact check: wrong. The answer (javelin) is right. The 1986 redesign moved the men's javelin's centre of gravity forward so it landed earlier and tip-first. Uwe Hohn threw 104.80 m on 20 July 1984, and the wrong answers are correct. The fun fact's "比一个足球场还长" is shaky. A standard international pitch is about 105 m, so 104.80 m is slightly shorter. Pitch lengths can be 100–110 m.
- **q-25156** (tennis) 这个东西是一项运动里用的。它是什么？ → 羽毛球: Fact check: wrong. The description and question stem fit the wrong answer "箭" too. Arrows used in archery have fletching, often made of feathers. So the stem doesn't pick out one answer. The hints do rule it out. The other facts hold: 16 goose feathers, a cork base, Lin Dan and Chen Long as champions, and smashes over 400 km/h.
- **q-25429** (famous-landmarks) 看视频：1984年到2018年的卫星图像展示了这片沙漠海岸的变化。这是哪座城市？ → 迪拜: source: Hint 2 says Dubai has built shaped islands since the 1990s, but land reclamation for Palm Jumeirah, the first shaped island, began in 2001. The only 1990s island is the small Burj Al Arab islet. The source hint should say "since the early 2000s" (zh: 从21世纪初起), and the translation should then follow it. Apart from that, the translation is faithful and natural. Fact check: uncertain. The answer (Dubai) and the fun fact (about 94 million m³ of sand) are right. Hint 2 says the islands began in the 1990s. The Palm Jumeirah started in 2001, and only the small Burj Al Arab island dates from 1999. I couldn't verify that the video file exists.
- **q-25436** (birds) 听一听：哪种鸟会发出这种低沉、沙哑的叫声？ → 鞭笞巨嘴鸟: Fact check: uncertain. The answer name '鞭笞巨嘴鸟' is a nonstandard form. The common Chinese name is 巨嘴鸟 (大嘴鸟). One source gives the alias '鞭笞鵎鵼', not '鞭笞巨嘴鸟'. The biology in the hints matches the toco toucan. A raven also croaks deeply, so the answer depends on the audio.
- **q-25999** (classic-tv-series) 《武林外传》里，白展堂是跑堂，那李大嘴在同福客栈干什么？ → 厨子: Fact check: uncertain. 答案“厨子”正确：李大嘴是同福客栈的厨师，吕秀才是账房，白展堂是跑堂。“账房”“捕快”“门房”都不是他的职务，提示也说得通。但我没能找到来源证实趣闻，即“大嘴”是一语双关，既指贪吃又指话多。搜索结果没有解释这个外号的由来。
- **q-26469** (chinese-tech-brands) 在中国城市，有些车牌是绿色的，比蓝牌多一位字符，还常常不受限行限制。哪种车挂这种车牌？ → 新能源汽车: Fact check: uncertain. I didn't run searches. This is from memory. The answer is right: new-energy vehicles get green plates with 8 characters, while blue plates have 7. Many cities also exempt them from driving restrictions. The fun fact is correct. The weak point is the wrong answer 出租汽车. Many taxis, such as Shenzhen's, are electric and carry green plates, so it isn't clearly wrong. Police and military vehicles use white plates, so those two are fine.
- **q-26831** (spring-festival) 有些厨师做一整碗长寿面，一共只用几根面条？ → 1根: source: the fun fact's claim that Shaanxi's famous 一根面 is a single noodle per bowl could not be confirmed. The fact check found that the well-known 一根面 comes from Weishan in Yunnan, where one very long noodle is cooked per pot. The source fun fact needs correcting, for example to the Weishan version or with the place left out, and then it can be re-translated. Fact check: wrong. The answer (1 根) and the hints fit the longevity noodle custom. The fun fact is the problem. Searches found no Shaanxi "一根面" with one noodle per bowl. The well-known "一根面" is from Weishan, Dali, Yunnan. There one long noodle is cooked per pot, and it can be broken when divided into bowls. A 2023 chinanews item on a "面食王国的一根面" could not be read. "面食王国" usually means Shanxi, not Shaanxi. The question wording also says one noodle per whole bowl, which is looser than the Weishan custom.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: This duplicates related question q-26256 (approved), which also asks how heavy Dong Fang Hong 1 was, with the answer 约173千克. Both would be played in the same zh-Hans pool. One of the two should be dropped, or this one should ask a different fact. That fix goes to the source, not the translation. The translation itself is faithful and natural.

## Not travelling

- **q-24268** about_language, confirmed: I swing high above a jungle river, and I'm woven from lianas. What are lianas? → Long woody vines (Asks what the English word 'liana' means. The Chinese term (木质藤本/藤本植物) contains 藤, so the word gives the answer away. Without the term, bamboo or bark would also fit, because real jungle bridges are made of them too.)

## Stale re-translated

None.
