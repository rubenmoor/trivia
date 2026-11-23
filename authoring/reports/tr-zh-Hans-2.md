# tr-zh-Hans-2

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 635, about $26.06 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-2&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-1 | tr-zh-Hans-2 |
|---|---|---:|---:|
| sources |  | 50 | 300 |
| stale re-translated |  | 0 | 0 |
| translated |  | 50 | 300 |
| not travelling |  | 0 | 0 |
| not travelling confirmed |  | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 50 | 296 |
| needs_work |  | 0 | 4 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 |
| audit/review agreement | ≥ 90.0 % | 88.0 % ✗ | 88.3 % ✗ |
| cost $ |  | $5.22 | $24.13 |
| $ per approved |  | $0.10 | $0.08 |
| **health** | | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 6 of 59 (10 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 1 (1 major), fact 1 (1 major), media 9 (4 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 53 of 60 (88 %)
- Sample: 60 audited of 60; 60 Claude calls, about $1.93

Major findings on approved questions:

- **q-21246**: media — The translation itself is fine: it keeps the source's meaning, the options 公鸡/小狗/奶牛/小猫 match in form, the hints and fun fact are correct, the wording is natural Chinese, and it doesn't overlap with the related donkey question. The problem is the media: the essential audio has title null, so no rooster crow has been picked (the background image is missing too). The question can't be played without the sound, unless null here just means the pipeline didn't pass the file along. (http://127.0.0.1:8001/review/q-21246)
- **q-21607**: giveaway — The question text calls it «另一种染成绿色的辣味根», which almost spells the answer «辣根». No wrong option has 辣 or 根 in it, so players can match the words without knowing the fact. Reword it to avoid both characters, e.g. «其实是另一种植物的根磨成、再染成绿色的。是哪一种？». The facts check out: imitation wasabi is mostly horseradish with green colouring, horseradish sauce is served with meat in Europe, and the root is white. Hints, fun fact and wording are fine otherwise. (http://127.0.0.1:8001/review/q-21607)
- **q-22035**: media — The media is marked essential but no file was picked (title null). The question depends on "照片里的材料" and never names glass, so it can't be played without a picture of glass. The translation itself is faithful and reads naturally: 天然碱 for natron is correct, the options all have the same form, and the Pliny legend and the hints about the Phoenicians are accurate. (http://127.0.0.1:8001/review/q-22035)
- **q-23057**: media — The question needs a photo: it opens with "看看照片" and only calls the object "这个". But the media is essential and no file was picked (title null), so players can't tell what goes in the ear. Everything else is fine: the translation matches the source, the answer 水 and the three wrong options are right, the hints don't give it away, and the fun fact (swimmer's ear is otitis externa) is true. (http://127.0.0.1:8001/review/q-23057)
- **q-23059**: media — The media is marked essential, but no file was picked (title is null). The question asks about "图中这位运动员", so without a high-jump photo it can't be played. The translation itself is faithful and natural. Answer 田径 is correct, all three wrong answers are clearly wrong, and the fun fact checks out (Sotomayor's 2.45 m from 1993 still stands). (http://127.0.0.1:8001/review/q-23059)
- **q-23878**: fact — The answer «大内元» gets the given name wrong. Kitaoka Akiyoshi's Ouchi-illusion page writes Hajime Ouchi as 大内朔 (おおうち はじめ), so the answer should be «大内朔». Everything else matches the source: the wrong options (北冈明佳, 草间弥生, 布里奇特·赖利) are still wrong, the hints work, and the fun fact only names the answer after it is revealed. (http://127.0.0.1:8001/review/q-23878)

## Needs work

- **q-21475** (brand-origins) 便利贴是在哪个年代第一次在商店里开卖的？ → 20世纪80年代: Fact check: uncertain. The answer 1980s matches the national Post-it launch (1980, after the 1978 Boise test). But the product was test-marketed in stores as 'Press 'n Peel' in four US cities in 1977, so 'first sold in stores' could be read as the 1970s. The hints and fun fact (Silver's weak adhesive, Fry's hymnal bookmarks) are fine. This is from memory, not from a fresh search.
- **q-21604** (famous-logos) 有些电影开场时，一盏蹦蹦跳跳的小台灯会把标志里的一个字母压扁。哪部电影的开场不是这样？ → 《怪物史莱克》: Hint 3 says '绿色怪物', which literally repeats '怪物' from the answer title 《怪物史莱克》. The house rule says hint 3 must contain no character that gives the answer away, and only one option contains these characters. Reword it without '怪物', e.g. '正确答案的主角是另一家工作室出品的绿皮肤大个子。' (roughly 'the hero of the right answer is a big green-skinned guy from another studio').
- **q-21699** (video-games) 在宝可梦游戏里，给皮卡丘用雷之石，它会进化成什么？ → 雷丘: Wrong answer '雷伊布' is the Taiwan/Hong Kong name for Jolteon. The official mainland Simplified Chinese name is '雷精灵', and the translator's own notes use '雷精灵'. Replace '雷伊布' with '雷精灵'. Everything else is faithful and correct: 雷丘, 皮丘, 电击兽 and 雷之石 are the right names.
- **q-22055** (legends-and-superstitions) 新娘在婚礼上一直拿着它，最后背对大家往后一抛，谁接到谁就是下一个结婚的人。它是什么？ → 捧花: Fact check: uncertain. The answer 捧花 (bouquet) is right. The three wrong answers (头纱, 戒指, 婚礼蛋糕) are not tossed and caught for the next-to-marry tradition. The hints are fine, and the fun fact matches the commonly told origin: guests tore off pieces of the bride's dress for luck, and the bouquet was thrown to distract them. That origin is folklore, not documented history. The description, "世界上唯一一项穿着礼服比赛的投掷运动", is an unverifiable superlative. The bouquet toss isn't a recognised sport, and I found no source for the claim. I did not run any searches, so this rests on general knowledge.

## Not travelling

None.

## Stale re-translated

None.
