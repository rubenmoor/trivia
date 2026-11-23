# tr-zh-Hans-6

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 293
- Needs work: 7
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 584, about $28.26 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-6&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-4 | tr-zh-Hans-5 | tr-zh-Hans-6 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 300 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 294 | 294 | 293 |
| needs_work |  | 6 | 5 | 7 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 1.7 % ✓ | 2.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 1.3 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 83.3 % ✗ | 83.3 % ✗ | 86.7 % ✗ |
| cost $ |  | $24.58 | $24.61 | $25.96 |
| $ per approved |  | $0.08 | $0.08 | $0.09 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 7 of 59 (12 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (1 major), fact 1 (0 major), media 8 (7 major), style 3 (1 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 52 of 60 (87 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.29

Major findings on approved questions:

- **q-21619**: media, giveaway — The media is essential and the question starts with "看照片", but no file was picked (title null), so there is no photo to show. Hint 3 also breaks the zh rule that hint 3 contains no character that gives the answer away: «名字里有一个“包”字» points straight at 蒙古包, the only option with that character. A pinyin initial or character count would work better. The translation is otherwise faithful, the options are parallel, and the facts check out. (http://127.0.0.1:8001/review/q-21619)
- **q-22366**: media — The media is marked essential, but no file was picked (title null). The question text says "就录在这样一盘磁带上", so it points at a cassette picture the players won't see. The translation itself is faithful and reads naturally: 垃圾摇滚 is the standard term for grunge. The facts hold: Awesome Mix Vol. 1 is 1960s–70s pop and rock, and its soundtrack reached No. 1 on the Billboard 200 with only previously released songs. (http://127.0.0.1:8001/review/q-22366)
- **q-22852**: media — The media is marked essential and the question opens with "看看这只动物", but no file was picked (title null), so the TV would show nothing. The translation itself is faithful and natural: 宝嘉康蒂, 花木兰, 莫阿娜 and 乐佩 are the standard mainland names. Meeko is a raccoon in Pocahontas, the hints are true, and dropping Flit's name from hint 2 doesn't hurt the clue. (http://127.0.0.1:8001/review/q-22852)
- **q-23017**: media — The media is marked essential, but no file was picked (title null). The question opens with «看看这张特写», so on the TV it points to a close-up that isn't there. The translation itself is faithful and natural, and the options and hints are fine. The fun fact about the British king needing no passport is true. (http://127.0.0.1:8001/review/q-23017)
- **q-23640**: media, style — The question needs its essential image ("这是哪种厨房用品？"), but media.title is null, so no picture was picked and the question can't be played. There is also a smaller wording issue: in mainland usage «水壶» usually means a kettle (烧水壶) or a water bottle, so for a pitcher «水罐» or «凉水壶» would be clearer. Otherwise the text is faithful to the source, and the hints and fun fact are fine. (http://127.0.0.1:8001/review/q-23640)
- **q-23830**: media — The media is essential ("看看这张照片") but no file was picked (title null), so as it stands the question can't be played: there's no photo of a pilot to look at. The translation is faithful and reads naturally. Hint 2's mention of the control tower (塔台) points straight to pilot, but hints come only through a joker, so that's acceptable. The fun fact about English being the standard radio language on international flights (an ICAO rule) is correct. (http://127.0.0.1:8001/review/q-23830)
- **q-23882**: media — The media is essential, and the question starts with "这张特写", but no file was picked (title null). Without the close-up, the question can't be played. Everything else checks out: the translation matches the source, the nationality prefixes on all four options keep them parallel, the new hint 3 (the brim) doesn't name the answer, and the fun fact about sombra/shade is true. (http://127.0.0.1:8001/review/q-23882)

## Needs work

- **q-21310** (tennis) 在网球里，发球好到对手连球都碰不到，这种球叫什么？ → Ace球: Fact check: uncertain. The answer (Ace) and the hints are right. The fun fact's 'official record about 250 km/h' is shaky. Guinness lists Sam Groth's 263.4 km/h (2012) as the fastest serve. The ATP doesn't recognize it because the radar was uncalibrated. The fastest serve ATP-recognized is about 253 km/h (John Isner, Davis Cup 2016). I did not run a search to check this.
- **q-21739** (volcanoes) 1816年，印度尼西亚坦博拉火山的火山灰让欧洲6月下了雪。这座火山离欧洲大约多远？ → 约1.2万公里: source: the claim that Tambora's ash brought June snow to Europe in 1816 is not solid. The documented June 1816 snow fell in New England and eastern Canada, and Europe had a cold, rainy summer. The cooling also came mainly from sulfate aerosols, not ash. The source needs rewording, e.g. "In 1816, sulfur from Indonesia's Tambora volcano brought a cold, rainy summer to Europe and June snow to North America. About how far is the volcano from Europe?" Then re-translate. The zh-Hans translation itself is faithful and in good style. Fact check: wrong. The question says Tambora's ash brought snow to Europe in June 1816. The documented June 1816 snow was in New England and eastern Canada (e.g. Albany, NY and Maine). Europe had cold, rain and gloom that summer. I found no solid record of June snow there. The cold also came mainly from stratospheric sulfate aerosols, not ash. The distance (~12,000 km), the hints and the Frankenstein fun fact are fine.
- **q-22062** (cartoons) 在电影《海洋奇缘》里，莫阿娜要去哪里归还被偷走的心？ → 特菲提: Overlap: approved q-22898 asks "是谁偷走了特菲提之心？". That puts the answer 特菲提 right in its question text, and it names the stolen heart this question asks about. A player who has seen one of the two questions gets this one for free. The translation itself is accurate and natural. The way out is to reword q-22898 so it doesn't name Te Fiti, or to keep only one of the two questions.
- **q-22431** (flags) 誓言是什么？比如有些人对着国旗立下的那种。 → 庄严的承诺: source: the fun fact says one athlete takes the oath for all athletes at every Olympic Games. That has not been true since Tokyo 2020, when a male and a female athlete took it together, alongside judges and coaches. The source fun fact should say something like "athletes' representatives take an oath to play fair". The translation itself is faithful and natural.
- **q-22677** (famous-landmarks) 克罗地亚杜布罗夫尼克老城的石头城墙，大部分建于哪个时代？ → 中世纪: Fact check: uncertain. The answer 中世纪 is broadly right. The walls date from the 13th–17th centuries, with the main outline set in the 14th–15th centuries. Greek, Roman and Napoleonic dates are clearly wrong, and the ~2 km length (1,940 m) and the walkable circuit are correct. Hint 2, 'most work was finished before Columbus reached the Americas (1492)', is shaky. Sources say the major reinforcements came in the 15th century, and some work (Revelin 1539, Bokar 1570, work up to 1660) came later. The period is also partly Renaissance, so 'medieval' is not clean-cut.
- **q-22697** (world-cuisines) 古埃及墓里发现的一罐蜂蜜，打开后可能还能吃。它大约有多少年历史？ → 3000年: Fact check: wrong. The description says the honey might outlast the pyramids. The tomb honey is about 3000 years old, but the Giza pyramids are about 4500 years old. So the honey is younger, not longer-lived. The answer (about 3000 years), the wrong answers and the fun fact are fine.
- **q-23548** (space-race-and-astronauts) “我是一条长长的旋转臂，转得你觉得自己比平时重好几倍。”航天员用我来适应什么？ → 火箭发射时的强大推力: Fact check: uncertain. The answer and the wrong answers hold up. Centrifuges simulate the g-forces of launch and re-entry, and weightlessness, Moon walking and sleeping standing up are not what they train. The hints are fine. The fun fact's "最多8倍" is not backed by one source. Facilities differ: ESA sessions reach about 6 g, the AFRL centrifuge reaches 9 g, and Apollo launches were about 4 g. So "8倍" is not a fixed maximum.

## Not travelling

None.

## Stale re-translated

None.
