# tr-zh-Hans-21

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 288
- Needs work: 12
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 520, about $33.23 at list price; $0.11 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-21&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-19 | tr-zh-Hans-20 | tr-zh-Hans-21 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 300 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 289 | 288 | 288 |
| needs_work |  | 11 | 11 | 12 |
| needs_work rate | ≤ 20.0 % | 3.7 % ✓ | 3.7 % ✓ | 4.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 3.0 % ✓ | 3.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: style | ≤ 10.0 % | 1.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $30.30 | $29.28 | $30.28 |
| $ per approved |  | $0.10 | $0.10 | $0.11 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 1 (0 major), fact 1 (0 major), overlap 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.95

Major findings on approved questions:

None.

## Needs work

- **q-21907** (prehistory) 下面四个古人类类群中，有三个是以发现化石的地点命名的。哪一个不是？ → 能人: In Chinese the answer 能人 is an everyday word that plainly means 'capable person'. The other three options are long phonetic transliterations that sound like place names. So the answer gives itself away by its form and its obvious meaning, with no knowledge needed, and hint 1 ('a skill, not a place') then settles it. 能人 is the standard mainland term and can't be swapped, so the text can't fix this. Either accept it as a much easier question (about 3) or rebuild it on a Chinese angle such as 北京人 (Peking Man), which makes it a different question.
- **q-23911** (plants) 看视频：这段延时视频里开放的是哪种花？它常在冬天用大鳞茎种在室内。 → 朱顶红: Fact check: wrong. The description says the bloom was compressed into a time "比打个喷嚏还短" (shorter than a sneeze). The media note says the video is 13 seconds long, which is much longer than a sneeze. The answer, wrong answers, hints and fun fact all check out. Hippeastrum is the amaryllis sold in winter, its name comes from the shepherdess in classical poetry, and true Amaryllis is native to South Africa.
- **q-23987** (athletics) 你蹲在短跑起跑线上，裁判先喊“各就位”，再喊“预备”。你什么时候起跑？ → 发令枪响的时候: source: this asks the same fact as approved q-24812 (on your marks, set, then the starting gun fires), so seeing one gives the other away. The translation itself is faithful and natural. The duplicate comes from the source pool, and the translation can't fix it: one of the two should be retired.
- **q-24265** (wonders-of-the-world) 救世基督像矗立在里约热内卢的科尔科瓦多山顶。这座山大约有多高？ → 约700米: Fact check: wrong. The text facts are correct. Corcovado is about 710 m high, so 约700米 is right and the wrong answers are clearly wrong. The Eiffel Tower is about 330 m, so 700 m is roughly twice its height. The statue is 30 m tall, and its arms span 28 m. The media query is wrong: it asks for 'Rio de Janeiro Sugarloaf Mountain'. Sugarloaf is a different peak, about 396 m high, so the image would show the wrong mountain.
- **q-24351** (disney-films) 补全小飞侠彼得·潘关于飞翔的名言：“只需要信念和信任，再加上一点点……” → 仙尘: Hint 3 («拼音首字母是 X、C») fits the distractor 星尘 (xīng chén) just as well as 仙尘 (xiān chén). The strongest hint can't tell the answer from the closest wrong option and could push players towards the wrong one. Replace it with a hint that only fits 仙尘, for example about the tiny fairy Tinker Bell without using the character 仙. A smaller point: the question calls the line Peter Pan's own «名言». The source more carefully calls it a famous Disney saying, because the exact line is more a Disney catchphrase than dialogue from the film. Wording such as «迪士尼关于和彼得·潘一起飞翔的名言» would stay true to the source.
- **q-24811** (athletics) 1986年，哪个田径投掷项目改了器材设计、让它飞得没那么远，因为顶尖选手快要扔出场地了？ → 标枪: source: the fun fact says Uwe Hohn's 104.80 m throw was "longer than a soccer field", but a standard international pitch is about 105 m, so the claim is shaky. The fact check marked it wrong. The source fun fact should be reworded, for example to "almost the length of a standard football pitch", and then the translation updated to match. The translation itself is faithful and natural. Fact check: wrong. The answer (javelin) is right. In 1986 the men's javelin was redesigned, with the centre of gravity moved forward, so it lands earlier and tip-first. Uwe Hohn threw 104.80 m in Berlin on 20 July 1984. The fun fact's claim that this is longer than a football pitch is shaky. A standard international pitch is about 105 m long, so 104.80 m is slightly shorter. I checked this from memory and ran no searches.
- **q-25156** (tennis) 这个东西用在一项体育运动里。它是什么？ → 羽毛球: Fact check: wrong. The wrong answer "弓箭" is not clearly wrong. Arrows are traditionally fletched with bird feathers, and archery is a sport. The question text ("身上至少有一部分曾经属于一只鸟", "用在一项体育运动里") therefore fits arrows too. Only the hints point to the shuttlecock. The other facts hold: a shuttlecock has 16 feathers, usually goose, on a cork base. Top smashes exceed 400 km/h, and the record is about 565 km/h. I did not run searches. This rests on my own knowledge.
- **q-25564** (birds) 看视频：这只绿身蓝脸、喙粗短的鸟正在树干上凿巢洞。它属于哪一类鸟？ → 拟啄木鸟: The translation swapped the source's wrong answer Bee-eater (蜂虎) for 啄木鸟 and dropped the source's "like a woodpecker, but it isn't one". A bird chiselling a tree in the video now has 啄木鸟 as a near-defensible option: barbets belong to the woodpecker order, and nothing in the text rules woodpeckers out. The swap also makes the answer 拟啄木鸟 stand out, because it is the only other option that echoes the drilling. Restore 蜂虎 as the distractor and add a clause saying it is not a woodpecker, worded so the name 拟啄木鸟 isn't echoed too directly.
- **q-25999** (classic-tv-series) 在《武林外传》里，白展堂在同福客栈当跑堂，那李大嘴是干什么的？ → 厨子: Fact check: uncertain. The answer 厨子 is right: 李大嘴 is the cook at 同福客栈. 吕秀才 is the accountant, so 账房 is wrong. 捕快 is also wrong as an answer, though 李大嘴 was once the town's 捕头 before he became the cook. 门房 is wrong. The hints are fine. The fun fact is the problem: I found no source saying 大嘴 is a pun on both loving to eat and being talkative. The 'nobody is especially good at their job' description is also a stretch, because 大嘴 really is the cook. The 捕快 distractor is a little risky, since he did hold the 捕头 job earlier in the series.
- **q-26469** (chinese-tech-brands) 在中国城市里，有些车牌是绿色的，比蓝牌多一位，还常常不受限行限制。哪种车会挂这种车牌？ → 新能源汽车: source: the wrong answer "Taxis" (出租车) can be defended. Many Chinese cities run electric taxis with green new-energy plates (Shenzhen's taxis are almost all electric), so Chinese players see green-plate taxis every day. The source should swap Taxis for a vehicle that never gets green plates, such as a school bus (校车, yellow plate) or a driving-school car (教练车). The zh-Hans translation itself is faithful and natural. Fact check: wrong. The answer (新能源汽车) and the fun fact (green plate 8 characters, blue 7) are correct. But the wrong answer 「出租车」 is not clearly wrong. Many Chinese cities, such as Shenzhen, use electric taxis, and these carry green new-energy plates. So a taxi can be correct. The third hint also fits plug-in hybrids and does not single out one answer.
- **q-26831** (spring-festival) 有的厨师做一整碗长寿面，只用几根面条？ → 1根: Source: the fun fact can't be confirmed. The well-known one-noodle-per-bowl dish «一根面» belongs to Taiyuan, Shanxi, not Shaanxi. Shaanxi's one-noodle dish is the Yangling 蘸水面, and the reported lengths are about 2 m, not clearly "several metres". The source's fun fact should be corrected, for example to the fact check's suggestion, and then re-translated. Also, «只用几根面条» reads a little awkwardly, and «只» hints at a small number; «用几根面条做成» would be more neutral. Fact check: uncertain. The answer (1 noodle) is right, and the other options are wrong. The longevity-noodle custom of not cutting the noodle is well supported. The fun fact is shaky. The dish named "一根面" (one noodle per bowl, also called longevity noodles) is mostly tied to Taiyuan, Shanxi. The Shaanxi version of one noodle per bowl is Yangling 蘸水面 (also called 裤带面). Reports give lengths of about 50 cm up to "2 m+", not clearly "several metres". I found no source for a famous Shaanxi dish called "一根面" that is several metres long.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: This duplicates approved q-26256, which asks the same thing: how heavy Dong Fang Hong 1 was, answer about 173 kg. The translation itself is faithful and natural. The duplicate comes from the source, so one of the two questions should be dropped or this one should ask a different fact.

## Not travelling

None.

## Stale re-translated

None.
