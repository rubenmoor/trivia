# tr-zh-Hans-8

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 496, about $29.99 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-8&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-6 | tr-zh-Hans-7 | tr-zh-Hans-8 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 293 | 295 | 295 |
| needs_work |  | 7 | 5 | 5 |
| needs_work rate | ≤ 20.0 % | 2.3 % ✓ | 1.7 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 1.0 % ✓ | 1.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.0 % ✓ | 1.0 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 86.7 % ✗ | 85.0 % ✗ | 88.3 % ✗ |
| cost $ |  | $25.96 | $25.56 | $27.17 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 7 of 59 (12 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: giveaway 3 (1 major), fact 1 (0 major), media 13 (7 major), difficulty 1 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 53 of 60 (88 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.82

Major findings on approved questions:

- **q-21247**: media — The media is marked essential, but no file was picked (title is null). The question says "看照片", and without a photo the clue "皱巴巴的狗" also fits the pug and the English bulldog. The translation itself is faithful and reads naturally, and the facts check out: the Shar Pei comes from Guangdong and has a blue-black tongue, like the Chow Chow. (http://127.0.0.1:8001/review/q-21247)
- **q-21391**: media — The question needs its essential image ("这样的食物" means the food shown in it), but media.title is null, so no image has been picked and the question can't be played as written. The rest of the translation checks out: 《天降美食》 is the mainland title, the names are standard transliterations, Swallow Falls is an island town, the FLDSMDFR fun fact is true, and the difficulty is about right (my estimate is 8, the given one is 10). (http://127.0.0.1:8001/review/q-21391)
- **q-21851**: media — The media is marked essential, and the question depends on it ("长着这种叶子的树"), but no file was picked (title is null), so players would get no leaf to look at. Everything else checks out: the translation matches the source, 枫树 is the correct answer, the hints and the 40:1 sap-to-syrup fun fact are accurate, and the wording reads naturally (松饼 is the usual mainland word for pancakes). (http://127.0.0.1:8001/review/q-21851)
- **q-22428**: media — The media role is essential, but no file is attached (title null), and the question starts with "这些晒干的豆荚", which points at a picture of vanilla pods that isn't there. Without it the question reads oddly on the TV. The translation itself is faithful and reads naturally, the facts check out (vanilla comes from an orchid, it is among the priciest spices by weight, and the Totonac people grew it in Mexico), and the options fit the same frame. (http://127.0.0.1:8001/review/q-22428)
- **q-23008**: media — The media is marked essential, but no file was picked (title null). The question says "这种棋" and expects a chess picture to show which game it means. Without it, players see no game, and Chinese families may think of 象棋 first, which also has 马 and 兵. The translation itself is faithful and natural, and the facts check out: the king loses by checkmate, it moves one square, and the shah mat etymology is right. (http://127.0.0.1:8001/review/q-23008)
- **q-23303**: media — The media is essential, but no file was picked (title is null). The question begins "这幅古代马赛克画上", so without the Alexander Mosaic it points at a picture that isn't there. The translation itself is fine: 大帝 is the standard Chinese epithet, the distractors 圣君/贤王/雄主 are the same kind of title and plausible, and hint 3 (彼得大帝, 叶卡捷琳娜大帝) gives a hint that works in Chinese without spelling out 大帝. The facts in the hints and the fun fact are correct. (http://127.0.0.1:8001/review/q-23303)
- **q-23466**: media — The media is essential but no file was picked (title null). Without the magnifying-glass picture, the question's "这个工具" refers to nothing, so the question can't be played. The translation itself is faithful and natural. The fun fact is true: Holmes takes out a magnifying glass in A Study in Scarlet (1887). The options, hints and description are fine. (http://127.0.0.1:8001/review/q-23466)

## Needs work

- **q-22352** (history) 你正在巴黎看烟花，这天法国纪念攻占巴士底狱。今天是几月几日？ → 7月14日: Hint 2 («它和美国独立日在同一个月») gives the answer away: it names the US Independence Day, which is the wrong option 7月4日, and implies that the answer is a different day in the same month. Together with hint 1, only 7月14日 is left. Use a hint that points to July without ruling out 7月4日 (for example «这一天在一年中的第七个月»), or keep a vague hint about the summer holidays.
- **q-22454** (strange-creatures) 它生活在美洲，成群结队活动，走路时把带环纹的尾巴高高竖起，还会用灵活的鼻子拱土找虫子。它是什么动物？ → 长鼻浣熊: The kept image is a common raccoon (File:Raccoon_by_water…), not a coati. The translation added 食蟹浣熊 (crab-eating raccoon) as a wrong answer, and the photo looks almost exactly like one, so it misleads players towards a wrong option. Either replace the media with a coati photo (e.g. "white-nosed coati tail") or swap 食蟹浣熊 for a distractor that doesn't look like a raccoon, such as 黑足鼬, which the translator's notes had planned. Fact check: wrong. The text is accurate. The image is a raccoon (query 'raccoon in forest'), not a coati. It could mislead players, because 食蟹浣熊 and the raccoon are distractors.
- **q-23051** (football) 足球的点球是在球门前的一个点上罚的。这个点离球门线大约多远？ → 11米: This asks the same fact as approved q-23860 ("点球大战中你站在点球点上，球门离你大约多远？", answer 11米): both ask how far the penalty spot is from the goal. One of the two should be dropped from the zh-Hans pool.
- **q-23666** (reptiles) 蛇嘴里那两根尖尖的“毒针”，有的像吸管一样是空心的，还能向后折起，毒液从中流出。它们其实是一种特殊的什么？ → 牙齿: Hint 3 «牙医会帮你照顾它们。» contains the character 牙, which is part of the answer 牙齿. The zh-Hans house rule says hint 3 must not contain a character that gives the answer away. Rephrase it without 牙, e.g. «你每天早晚都要刷它们。». Also, «那两根……有的……» is slightly awkward (two fangs, "some of them"). Something like «有些蛇嘴里的两根“毒针”像吸管一样是空心的……» would read better.
- **q-23789** (natural-phenomena) 微风之于飓风，好比轻微颤动之于……？ → 地震: Hint 3 «大号版能把房子震塌» uses 震, one of the two characters of the answer 地震. The zh-Hans rules say hint 3 must not contain a character that gives the answer away, and the translator avoided 微震 for this very reason. Reword it, for example as «大号版能把房子晃塌。» or «大号版能让房子倒塌。».

## Not travelling

None.

## Stale re-translated

None.
