# tr-zh-Hans-23

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 290
- Needs work: 9
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 485, about $32.31 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-23&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-21 | tr-zh-Hans-22 | tr-zh-Hans-23 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 288 | 290 | 290 |
| needs_work |  | 12 | 10 | 9 |
| needs_work rate | ≤ 20.0 % | 4.0 % ✓ | 3.3 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.0 % ✓ | 1.3 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 1.3 % ✗ | 1.3 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 95.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $30.28 | $29.13 | $29.09 |
| $ per approved |  | $0.11 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 2 of 2 (100 %)
- Problems by kind: giveaway 4 (1 major), ambiguity 1 (0 major), overlap 2 (2 major), difficulty 1 (1 major), style 2 (1 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.22

Major findings on approved questions:

- **q-25083**: overlap — The related question q-25245 says the Romans made a drink from crushed grapes (葡萄) and that Bacchus was its god. That is the same fact as this question, and seeing it gives this answer away. Apart from that, the translation is faithful and natural, the Turpan raisin hint and the Dionysus fun fact are true, the amphora picture is fine and the difficulty fits. (http://127.0.0.1:8001/review/q-25083)

## Needs work

- **q-22454** (strange-creatures) 它有一根又长又灵活的鼻子，走路时把带环纹的尾巴高高翘起。它是什么动物？ → 南美浣熊: The kept illustrative image (File:Raccoon_by_water…, from the query 'raccoon in forest') shows a raccoon (浣熊) sharp on screen. In Chinese, 南美浣熊 is the only option containing 浣熊, so the picture gives the answer away. The zh-Hans text itself is fine. The fix is to the media: the source needs a different illustrative image with no raccoon in it, e.g. 'Amazon rainforest' or 'Central American jungle', or a decorative one.
- **q-22786** (video-games) 在《超级马力欧》游戏里，长得很像图中这种的蘑菇，会让马力欧怎么样？ → 让他变大: This duplicates the approved q-21801 ("在超级马力欧游戏里，马力欧吃到一个像图中这样的红底白点蘑菇，会发生什么？" → 他会变大). Both ask the same fact, with the same fly agaric picture and the same answer. Keep only one of them in the zh-Hans pool.
- **q-23051** (football) 足球点球要在球门前的一个点上踢。这个点离球门线大约多远？ → 11米: This repeats an approved question. q-23860 ("点球大战中你站在点球点上，球门离你大约多远？", answer 11米) asks for the same thing: how far the penalty spot is from the goal. One of the two should be dropped. The translation itself is accurate and natural.
- **q-23987** (athletics) 短跑起跑时，你蹲在起跑线上。发令员先喊“各就位”，再喊“预备”。你什么时候开始跑？ → 发令枪响时: Source: this question asks the same fact as approved q-24812: the same scene (on your marks, then set) and the same answer (the starting gun fires). Players who see one already know the answer to the other. One of the two should be retired at source level. The translation itself is faithful and natural.
- **q-24811** (athletics) 1986年，因为顶尖选手快要投出场地了，哪个田径投掷项目换成了飞不那么远的新器材？ → 标枪: Source: the fun fact says Uwe Hohn's 104.80 m throw was longer than a football pitch, but a standard pitch is about 105 m (FIFA range 100–110 m), so the throw was about the same length, not longer. The translation copies this faithfully. Fix the source fun fact (for example "about the length of a standard football pitch") and then re-translate it. Fact check: wrong. The answer (javelin) is right. The men's javelin was redesigned in 1986 with the centre of gravity moved forward, so it lands tip-first sooner. Uwe Hohn threw 104.80 m in 1984. However, the fun fact says that is longer than a football pitch. The standard FIFA pitch is about 105 m long (100–110 m), so 104.80 m is about the same length, not longer.
- **q-25564** (birds) 看：这只鸟正在树干上凿洞筑巢。它是哪种鸟？ → 拟啄木鸟: Giveaway in Chinese: the answer 拟啄木鸟 literally means "woodpecker-like bird", and the question text and the essential clip both show the bird chiseling a nest hole like a woodpecker. So it is the only option that matches, and players can pick it with no bird knowledge, which undercuts difficulty 11. The clue amounts to a translation of the answer's own name. Also, the translator replaced all three source distractors (parakeet, bee-eater, kingfisher) with tree-trunk birds, and 䴓 is a rare character that may not render. To fix it, the text would have to drop the hole-chiseling and the distractors would need names that also sound woodpecker-like. The clip still shows the chiseling, though, so marking it as not travelling may be the cleaner option.
- **q-25659** (classical-music) 听一听：这段巴赫名曲在这里用扬琴演奏，它是哪部作品的开篇？ → 《第一无伴奏大提琴组曲》: The fun fact says Casals found «一份旧抄本», which means a handwritten manuscript copy. What he actually found in 1890 was a printed edition (Grützmacher's). The source says "an old copy", so this error comes from the translation. Change «旧抄本» to «旧乐谱» or «旧版乐谱», and the sentence also drops the doubled «旧».
- **q-25999** (classic-tv-series) 《武林外传》里，白展堂是跑堂，那李大嘴是干什么的？ → 厨子: Fact check: uncertain. The answer is right: 李大嘴 is the cook (厨子) at 同福客栈, 白展堂 is the waiter, and 吕秀才 is the bookkeeper. The wrong answers 账房, 捕快 and 门房 are all wrong for him. The hints are fine. I could not verify the fun fact that 大嘴 is a pun on both loving food and talking too much. The search found no source for where the nickname comes from. The description (nobody is especially good at their job) is also loose.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: source: this asks the same fact as the approved q-26256 (“东方红一号……它大约有多重？” → 约173千克), so the two questions duplicate each other in the zh-Hans pool. The translation itself is faithful and natural. The fix belongs at the source level: drop one of the two questions, or rework one to ask a different fact about Dong Fang Hong 1.

## Not travelling

- **q-25078** other, confirmed: Ancient Egyptians made millions of mummies of the ibis. What kind of animal is an ibis? → A bird (The Chinese name of the ibis (鹮/圣鹮) has the 鸟 (bird) radical, so the answer is given away. Leaving the animal unnamed doesn't work either: the baboon was also sacred to Thoth, so 猴子 would become arguably correct.)

## Stale re-translated

None.
