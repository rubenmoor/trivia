# tr-zh-Hans-18

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 290
- Needs work: 10
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 634, about $32.94 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-18&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-16 | tr-zh-Hans-17 | tr-zh-Hans-18 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 300 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 290 | 290 | 290 |
| needs_work |  | 10 | 9 | 10 |
| needs_work rate | ≤ 20.0 % | 3.3 % ✓ | 3.0 % ✓ | 3.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.3 % ✓ | 2.7 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 0.3 % ✓ | 1.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.73 | $28.52 | $30.29 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 2 of 2 (100 %)
- Problems by kind: giveaway 2 (1 major), overlap 3 (2 major), media 1 (0 major), difficulty 1 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.65

Major findings on approved questions:

- **q-25334**: giveaway, difficulty — The question asks for the apprentice of an 艺伎, and 舞伎 is the only option that shares the character 伎. Players can pick it without knowing the term. That makes the question much easier than its rated 12. The English source has no such link between "geisha" and "Maiko". The facts check out: maiko are Kyoto apprentices who use their own hair, while geiko usually wear wigs. The mainland film title 《艺伎回忆录》 and the distractors 花魁, 女忍者 and 女将 are correct and clearly wrong. A fix could swap in distractors that also end in 伎 or 妓, such as 艺妓 variants or 游女/太夫-style terms rewritten to match, or reword the question to avoid 艺伎. (http://127.0.0.1:8001/review/q-25334)

## Needs work

- **q-21907** (prehistory) 下面有三种古人类是以发现化石的地点命名的。哪一种不是？ → 能人: In Chinese the answer's standard name 能人 is an everyday word meaning "a capable person". It is also the only option that isn't a transliterated place name, so it stands out by form and meaning and anyone can pick it without knowing anything (hint 1 then says so outright). The clue is in effect a translation of the answer's own name, so the question collapses in zh-Hans. Swapping options can't fix that, because 能 always reads as a skill. Recommend marking it travels: no (about_language / other) rather than revising it.
- **q-24268** (famous-bridges) 我高高悬在丛林的河流上方，是用“藤本植物”编成的。藤本植物是什么？ → 攀着大树长的木质长茎: In Chinese the term itself gives the answer away: 藤本植物 contains 藤 (vine) and 植物 (plant), so any reader, even a child, knows it means a vine plant. The answer is also the only option described as a living, climbing plant. The question falls apart in zh-Hans. Either rebuild it so the clue doesn't rest on what the word means (for example, ask what the bridge is woven from, using a description rather than the term), or mark it travels: no (about_language).
- **q-25468** (traditional-dress) 这件衣服就像一条中间开了个洞、能把头套进去的毯子。它叫什么？ → 斗篷: Fact check: uncertain. The item described is a poncho. 斗篷 is a generic word for cloak or cape, and a cloak usually has no head hole and opens at the front. 斗篷 is a common dictionary gloss for poncho, so the answer is not strictly wrong. It is imprecise, though, and a player could argue it fits a cloak too. The three wrong answers (和服, 苏格兰裙, 纱丽) are clearly wrong. The hints and fun fact are plausible: Andean ponchos are woven from llama and alpaca wool and are worn in Peru and Bolivia. I did not check these against sources, and I did no web searches.
- **q-25999** (classic-tv-series) 在《武林外传》里，白展堂是跑堂，那李大嘴是什么？ → 厨师: Fact check: uncertain. The answer 厨师 is correct. 白展堂 is the 跑堂 and 李大嘴 is the cook at 同福客栈. 吕秀才 is the 账房, so that distractor is wrong. 捕快 and 门房 don't describe 李大嘴 now. He was a 捕头 earlier, but he resigned to cook. The hints are consistent with the show. I couldn't verify the fun fact that 大嘴 is a pun on both 贪吃 and 话多/嘴上没把门. My search found no source for the name's origin, and 李大嘴 isn't clearly known for talking a lot. The description 'nobody is especially good at their job' is also loose, because he is a skilled cook.
- **q-26282** (ming-dynasty) 他和自己的侄子建文帝打了一场仗，1402年登上了皇位。他是谁？ → 永乐皇帝: Fact check: wrong. The answer, wrong answers, hints and fun fact are correct. The description ("这一家人过年团聚的时候，最好别背对着门坐") has nothing to do with the Yongle Emperor. It looks like a leftover from another question.
- **q-26325** (mythical-creatures) 我侍奉西王母，替她传递消息。李商隐曾托我去探望心上人。我是谁？ → 青鸟: source: this question duplicates q-26171 (already approved). Both are riddles about the bird that serves the Queen Mother of the West (西王母) and that Li Shangyin sends to visit his beloved, and both have the answer 青鸟. The translation itself is faithful and natural. The fix belongs in the source: drop one of the two questions, or rebuild one around a different fact.
- **q-26464** (chinese-scientists) 1965年，王应睐领导的上海团队在世界上首次人工合成了有生物活性的蛋白质——胰岛素。它是哪种动物的胰岛素？ → 牛: Overlap: the related approved question q-27602 (same subcategory) says in its text "1965年，中国科学家人工合成了结晶牛胰岛素", which gives away this question's answer (牛). One of the two should be dropped, or q-27602's wording should be changed so it no longer names the animal. The translation itself is faithful and natural.
- **q-26469** (chinese-tech-brands) 在中国城市里，有些车牌是绿色的，比蓝色车牌多一位，还常常不受限行限制。哪种车挂这种车牌？ → 新能源汽车: source: the wrong answer 'Taxis' (出租车) is defensible. In cities like Shenzhen almost all taxis are electric and carry the green NEV plate, and taxis are often exempt from driving limits too. Replace it in the source with a vehicle that never gets a green plate (e.g. motorcycle 摩托车 or tractor 拖拉机), then update the translation to match. Fact check: wrong. The answer (新能源汽车), the 8-character green plate vs 7-character blue plate, and the restriction exemption in many cities are all correct. But the distractor 出租车 is not clearly wrong. Many Chinese cities, such as Shenzhen, have mostly electric taxis, and these carry green NEV plates. A taxi can therefore legitimately have a green plate. This is from my own knowledge. I did not run any searches.
- **q-26831** (spring-festival) 有的厨师做一整碗长寿面，只用几根面条？ → 1根: source: the fact check marks the fun fact wrong. The best-known single-noodle bowl (一根面) is from Weishan in Yunnan, not Shaanxi, and I can't confirm a well-known Shaanxi dish of that name. The source fun fact needs correcting (for example to 云南巍山的“一根面”), and then the translation should follow it. Also, when the source is fixed, the question «有的厨师做一整碗长寿面，只用几根面条？» reads clumsily. «只用» hints at a small number. Something like «有的厨师做一整碗长寿面，一共用几根面条？» would be better. Fact check: wrong. The answer (1根) is fine, but the fun fact is wrong. The famous 'one-noodle' dish (一根面) is from Weishan, Yunnan, not Shaanxi. A Weishan noodle set a Guinness record of about 1,704 m. Shaanxi's best-known long noodles are biangbiang noodles. Yangling dipping noodles run only about a metre per strand and aren't a single-strand bowl.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: source: this asks the same fact as approved q-26256 (how heavy Dong Fang Hong 1 was, answer about 173 kg), so it duplicates a pool question. The translation itself is fine. One of the two questions should be dropped or turned into a different question at the source level.

## Not travelling

None.

## Stale re-translated

None.
