# tr-zh-Hans-17

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 290
- Needs work: 9
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 618, about $31.12 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-17&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-15 | tr-zh-Hans-16 | tr-zh-Hans-17 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 292 | 290 | 290 |
| needs_work |  | 8 | 10 | 9 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | 3.3 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 2.3 % ✓ | 2.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 1.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 93.3 % ✓ | 95.0 % ✓ | 96.7 % ✓ |
| cost $ |  | $27.32 | $27.73 | $28.52 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: fact 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.59

Major findings on approved questions:

None.

## Needs work

- **q-24113** (video-game-characters) 在《我的世界》里，有个大鼻子角色会“嗯”一声，还能用绿宝石跟你换东西。它是谁？ → 村民: Fact check: wrong. The third hint is wrong. 村民 has pinyin initials C and M? No: 村民 is cūn mín, so the initials are C and M. That part is fine. The real problem is that the hint says the name has two characters with initials C and M, which makes the answer easy to guess. The bigger problem is that the wrong answer 苦力怕 (kǔ lì pà) and the others are fine. But the hint 'never attacks you' is only roughly true: villagers are passive, yes. Still, the clue 'big nose' and the '嗯' sound (the villager 'hmm' sound) are true. The 'well' hint is true for villages. The fun fact is true: a villager with a lectern becomes a librarian. Overall the question is factually correct. The only flaw is that the hint makes 村民 a giveaway, which is not a factual error.
- **q-24389** (history-of-money) 用银行卡付款时，你要在这样的键盘上输入什么？ → 支付密码: Fact check: wrong. The answer (PIN / 支付密码) is right. The wrong answers don't fit a payment keypad. The hints are fine. The fun fact matches the widely reported story: Shepherd-Barron wanted 6 digits, but his wife could only remember 4. The problem is the description. It says this is the "only" keyboard adults type on with one finger. That is false, because many adults type on phone keypads and touchscreens with one finger. It is also an unverifiable overclaim.
- **q-25558** (world-war-ii) 《血战钢锯岭》中，医护兵戴斯蒙德·道斯在冲绳把伤员一个个从悬崖上放下去。真实的道斯大约救了多少人？ → 约75人: source: Hint 1's timeline is wrong. Accounts put the cliff rescue at about 12 hours on 5 May 1945, not "a night and a day", and the translation makes it stronger still (忙了一整夜又一整天). Hint 3 is loosely supported: the Medal of Honor citation mentions about 75 casualties in the unit, not 75 men Doss saved. The fact check was 'wrong'. Fix the source hints first (e.g. hint 1: "about 12 hours, alone, with a rope"; hint 3: "estimates range from 50 to 100; the usual figure is 75"), then re-translate. The translation itself is otherwise faithful and natural. Fact check: wrong. The answer (about 75) is fine. Hint 3 is not supported. The Medal of Honor citation gives no number of men saved. The 75 and 50–100 figures come from later estimates.
- **q-25999** (classic-tv-series) 在《武林外传》里，白展堂是跑堂的，那李大嘴是干什么的？ → 厨子: Fact check: uncertain. I did not run any searches. The answer and distractors match what I remember of the show. 李大嘴 is the cook (厨子). 吕秀才 is the 账房, so that distractor is wrong as it should be. 白展堂 is the 跑堂. 捕快 (燕小六/邱莫言's role) and 门房 are not his job. The fun fact is the problem. I know of no source saying the name 李大嘴 is a deliberate pun on 爱吃 and 嘴碎. The nickname most plausibly just means 'big mouth'. The description 'nobody does anything especially well' is also loose.
- **q-26469** (chinese-tech-brands) 中国城市里有些车牌是绿色的，比蓝牌多一位字符，还常常不受限行。这是哪种车？ → 新能源车: Fact check: wrong. The answer and the facts are right. New energy vehicles have green plates with 8 characters, and blue plates have 7. Many cities exempt them from driving restrictions. The wrong answer "出租车" is a problem. Many cities, such as Shenzhen, have electric taxis with green plates, so a taxi can also be a green-plate car. That makes it arguably correct.
- **q-26585** (martial-arts) 一个圆分成黑白两半，每半各有一个另一种颜色的圆点，象征阴阳。它叫什么？ → 太极图: Source problem: q-26585 asks the same fact as the approved q-27366. Both describe a black-and-white circle with a dot of the opposite colour in each half, and both have the answer 太极图. Players in zh-Hans would get the same question twice. One of the two source questions should be retired or replaced. The translation itself is fine.
- **q-26831** (spring-festival) 有的厨师做一整碗长寿面，只用几根面条？ → 1根: source: the fun fact credits Shaanxi with the famous "一根面", but the fact check traces the well-known single-noodle dish to Weishan, Dali (云南大理巍山). I can't confirm a famous Shaanxi version, so the source fun fact needs correcting first. Separately, in the translation «只用几根» hints at a small number; «用几根面条» would match the source's neutral "from how many noodles". Fact check: wrong. The answer (1 noodle) is fine, and the wrong answers 2, 9 and 100 are wrong. The fun fact is wrong about the place. The well-known "一根面" (one-noodle) dish is from Weishan, Dali, Yunnan, not Shaanxi. I found no sources for a Shaanxi "一根面".
- **q-26995** (c-pop) 下面哪首歌不是“情歌王子”张信哲的代表作？ → 《童话》: source: Hint 2 is wrong. In Guang Liang's 《童话》 (2005) the singer wants to become the angel (天使) that she loves in the fairy tale, not her prince. The translation copies this error. Correct the source's hint 2 (for example "It came out in 2005, and its singer wants to become the angel his love dreams of."), then translate it again.
- **q-27022** (cartoons) 高飞用两条腿走路，戴着帽子，是米奇最好的朋友。他是什么动物？ → 狗: Fact check: wrong. The answer (狗) is correct. Goofy is an anthropomorphic dog, Pluto is Mickey's non-speaking pet dog, and the Goofy/Pluto confusion is well known. The description's claim that his hat "从来没掉过" is unsupported. Goofy's hat is often knocked off or lost in cartoon gags. I answered from memory and ran no searches.

## Not travelling

- **q-25449** other, confirmed: Kanzashi can be made of lacquered wood or folded silk flowers, and apprentice geisha change theirs with the seasons. What are kanzashi used for? → Decorating the hair (Kanzashi is written 簪 in Japanese, and its standard Chinese form is 簪/簪子 (hairpin), so naming the term gives the answer away; dropping the name would change the question.)

## Stale re-translated

None.
