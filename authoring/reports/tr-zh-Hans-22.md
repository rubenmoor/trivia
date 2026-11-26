# tr-zh-Hans-22

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 290
- Needs work: 10
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 493, about $32.07 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-22&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-20 | tr-zh-Hans-21 | tr-zh-Hans-22 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 288 | 288 | 290 |
| needs_work |  | 11 | 12 | 10 |
| needs_work rate | ≤ 20.0 % | 3.7 % ✓ | 4.0 % ✓ | 3.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.0 % ✓ | 3.0 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.3 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 95.0 % ✓ |
| cost $ |  | $29.28 | $30.28 | $29.13 |
| $ per approved |  | $0.10 | $0.11 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 2 (1 major), fact 1 (1 major), difficulty 1 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.94

Major findings on approved questions:

- **q-21907**: giveaway, difficulty, fact — In Chinese, the answer gives itself away. «能人» is a plain two-character word meaning "capable person". The three wrong options are long phonetic transliterations of place names (丹尼索瓦, 尼安德特, 弗洛勒斯), so any reader spots the one name that isn't a place without knowing anything about early humans. It also stands out by its form and length, and hint 1's «本领» points straight at «能». That drops the real difficulty from 10 to about 4. Fun fact (minor, also true of the English source): the Xiahe jawbone (2019) and the Harbin skull (identified as Denisovan in 2025) mean that "almost everything from one finger bone" is now overstated. (http://127.0.0.1:8001/review/q-21907)

## Needs work

- **q-22786** (video-games) 在超级马力欧游戏里，一个长得很像图中这种的蘑菇，会对马力欧起什么作用？ → 让他变大: This asks the same fact as approved q-21801 in the same pool ("在超级马力欧游戏里，马力欧吃到一个像图中这样的红底白点蘑菇，会发生什么？" → 他会变大). It is the same question with the same picture idea and the same answer, so one of the two should be dropped from the zh-Hans pool.
- **q-23051** (football) 足球比赛的点球是从球门前的一个点上踢的。这个点离球门线大约多远？ → 11米: This duplicates the approved related question q-23860 ("点球大战中你站在点球点上，球门离你大约多远？" → 11米), which asks the same fact: the penalty spot is 11 m from the goal. Only one of the two should stay in the pool. The translation itself is fine.
- **q-23888** (celebrations-around-the-world) 某城市举办一个双年艺术节，上一届在2023年。下一届在哪一年？ → 2025年: The source is a vocabulary question about what the English word "biennial" means. In Chinese, 双年 literally says "two years", so the question answers itself, and hint 2 (not twice a year) is a leftover from the English biennial/biannual confusion that means nothing in Chinese. Any Chinese wording (双年展, 每两年) states the answer, so this item should be marked travels: no (about_language) for zh-Hans.
- **q-23987** (athletics) 你蹲在短跑起跑线上。发令员先喊“各就位”，再喊“预备”。你什么时候起跑？ → 发令枪响时: This asks the same fact as the approved q-24812: a sprint start, the starter says “各就各位” then “预备”, and the answer is the starting gun. One gives the other away. This comes from the source, not the translation; the translation itself is accurate and natural. Drop one of the two questions.
- **q-24811** (athletics) 1986年，顶尖选手快要扔到场地尽头了，于是哪个田径投掷项目换上了飞不那么远的新器材？ → 标枪: source: the fun fact says Hohn's 104.80 m was longer than a football pitch, but the standard international pitch is 105 m, so the claim is shaky or wrong. The source fun fact should say "almost as long as a standard football pitch" (e.g. 几乎相当于一个标准足球场的长度), and the translation should then follow it. Otherwise the translation is faithful and reads naturally. Fact check: wrong. The answer (javelin) and the 1986 redesign are correct. Uwe Hohn's 104.80 m throw on 20 July 1984 is also correct. But the fun fact says it was longer than a football pitch, and 104.80 m is slightly shorter than the standard 105 m international pitch. I did not run searches, so this comes from memory.
- **q-25156** (tennis) 这是一项运动要用的东西。它是什么？ → 羽毛球: Fact check: wrong. The wrong answer "羽箭" is not clearly wrong. Archery arrows are sports equipment, and their fletching is often made of real bird feathers. The stem and description ("运动要用的东西", "曾经长在鸟身上") fit an arrow as well as a shuttlecock. Only the hints separate them. The other facts hold from memory (I ran no searches): a shuttlecock has 16 goose feathers on a cork base, and Lin Dan and Lee Chong Wei are badminton stars. The 400+ km/h smash is also true, since the record is far higher (over 500 km/h).
- **q-25564** (birds) 看视频：这只正在树干上凿洞做窝的鸟，是哪种鸟？ → 拟啄木鸟: The Chinese name 拟啄木鸟 contains 啄木鸟 ("woodpecker-like bird"). With a video of the bird chiselling a nest hole and a description about a "carpenter", it is the only option whose name says it drills wood, so the answer is given away. The translator also quietly swapped the source's wrong answers (parakeet, bee-eater, kingfisher) for nuthatch, treecreeper and wryneck. The notes don't mention this, and the options no longer match the source. One way out: keep the source's options and point the question at something other than drilling (for example, the bird's family or diet). Otherwise mark it travels: no.
- **q-25999** (classic-tv-series) 在《武林外传》里，白展堂是跑堂的，那李大嘴是干什么的？ → 厨子: Fact check: uncertain. The answer 厨子 is correct: 李大嘴 is the cook at 同福客栈. 白展堂 is the 跑堂, and 吕秀才 is the 账房. Two things couldn't be verified. First, the fun fact that 大嘴 is a pun on gluttony and talkativeness, which I found no source for. Second, the distractor 捕快. One search summary says 李大嘴 once served as 捕头 before becoming the cook, and that claim looks muddled. If it's true, 捕快 isn't clearly wrong. The description (everyone works but no one is especially good) is also vague.
- **q-26831** (spring-festival) 有些厨师做的一整碗长寿面，是用几根面条做成的？ → 1根: source: the fun fact says Shaanxi's 一根面 is a single noodle "several metres long" (好几米). The fact check rates this wrong: reliable sources put it at about 1–1.5 m, sometimes a little over 2 m. I can't confirm "several metres" either. The source's fun fact should be corrected, for example to "usually over a metre long, sometimes more than two metres", and then the translation updated to match. Apart from that, the translation is faithful and natural. Fact check: wrong. The answer (1 noodle) is plausible, but the fun fact is shaky. Shaanxi's "一根面" (biangbiang/裤带面) is usually about 1–1.5 m, and some blogs say 2 m or a bit more. It is not "好几米" (several metres). Only unreliable posts claim 7 m. Also, the question says "有些厨师" and the hints/description are vague; the claim that you "won't touch a second noodle" is fine.
- **q-27533** (peoples-republic) 1970年发射的东方红一号，比另外四个国家的第一颗卫星加起来还重。它大约有多重？ → 173千克: Overlap: related q-26256 (approved, 探月与探火) already asks about the mass of 东方红一号 and has the same answer (约173千克). Players would get the same fact twice. One of the two should be dropped or rewritten to ask about a different fact (e.g. which song it played, or its launch year). This is a pool-level duplicate, not a translation problem.

## Not travelling

None.

## Stale re-translated

None.
