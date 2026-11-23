# tr-zh-Hans-9

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 487, about $31.10 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-9&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-7 | tr-zh-Hans-8 | tr-zh-Hans-9 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 295 | 295 | 297 |
| needs_work |  | 5 | 5 | 3 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 1.7 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.0 % ✓ | 1.0 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 85.0 % ✗ | 88.3 % ✗ | 86.7 % ✗ |
| cost $ |  | $25.56 | $27.17 | $28.15 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 7 of 59 (12 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (1 major), overlap 1 (1 major), media 13 (6 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 52 of 60 (87 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.95

Major findings on approved questions:

- **q-21214**: media, giveaway — The question needs an essential image ("看图"), but no file was picked (title is null), so it can't be played as it stands. Hint 2 also describes layers stacked one by one ("一张张叠起来"), which in Chinese almost spells out the name 千层面; that is only a minor hint giveaway. The facts check out (Bolognese lasagne verde, Garfield), and the translation and wrong answers are fine. (http://127.0.0.1:8001/review/q-21214)
- **q-21420**: overlap — The translation is faithful and reads naturally: 朱庇特, 马尔斯, 尼普顿 and 墨丘利 are the standard forms, and the hints and fun fact are correct. The problem is that related q-21916 states the answer outright in its question text (“宙斯对应朱庇特，哈迪斯对应……”), so anyone who has seen it gets this one for free; q-21789 (Jupiter's temple on the Capitoline Hill) also repeats this fun fact. Both overlaps already exist in the source pool and are not caused by the translation. (http://127.0.0.1:8001/review/q-21420)
- **q-22706**: media — The media is marked essential, but no file was picked (title null), and the question begins «看这个巨大的头骨», so on the TV it points to a picture that isn't there. The translation itself is faithful and natural. I checked that 霸王龙 is correct, that 剑龙, 三角龙 and 腕龙 are clearly wrong, and that the hints and fun fact are true. The 王 in hint 3 («暴君蜥蜴之王») is acceptable, since hint 3 may come close. q-22965 (how many legs T. rex walks on) asks a different fact. (http://127.0.0.1:8001/review/q-22706)
- **q-22837**: media — The media role is essential and the question points at the picture ("这些是从院子里的树上落下来的"), but no file was picked (title null), so the TV would show nothing for «这些». Everything else checks out: the translation matches the source, «有机垃圾» is correct and clear even though mainland sorting categories differ, the wrong answers are clearly wrong, and the hints and fun fact are accurate. (http://127.0.0.1:8001/review/q-22837)
- **q-22870**: media — The question needs its essential image: "这台机器" only means something if a TV is shown. Media title is null, so no file was picked, and without one the question can't be played. The translation itself is accurate and natural, the options are parallel, and the hints and fun fact are true (Baird's 1926 demonstration). (http://127.0.0.1:8001/review/q-22870)
- **q-23024**: media — The media is marked essential, but its title is null, so no file was picked. The question says “这三座小金字塔”, which points at a picture, so it can't be played without a photo of the Giza queens' pyramids (G1-a/b/c). The translation itself is faithful and natural: the answer is right, the queens' pyramids are about 30 m tall as the fun fact says, the options have the same form, and nothing in the description, hints or wording is a problem. (http://127.0.0.1:8001/review/q-23024)
- **q-23127**: media — The media is marked essential, but no file was picked (title null). Without the photo of the red-eyed tree frog, “这种青蛙” and “这道红光” point at nothing. The translation itself is faithful and natural, and the facts check out: startle display against predators, and early hatching when the eggs feel a snake's vibrations (Warkentin's research). The options and hints are fine. (http://127.0.0.1:8001/review/q-23127)

## Needs work

- **q-22454** (strange-creatures) 它长着又长又灵活的鼻子，走路时高高翘起带环纹的尾巴。它是什么动物？ → 南美浣熊: Hint 1 says the animal lives in South America (南美洲), and 南美浣熊 is the only option that starts with 南美, so hint 1 gives the answer away. Hint 1 should go back to the source's broader range (the Americas, e.g. 美洲的森林和丛林) or describe the habitat without naming a continent. Also, the source's media is a raccoon photo (raccoon in forest). In Chinese it points straight at the one option with 浣熊 in its name, so the illustrative image should be replaced with something neutral, like a rainforest floor.
- **q-22786** (video-games) 在超级马力欧游戏里，一种长得很像图中这样的蘑菇会让马力欧怎样？ → 让他变大: This asks the same fact as related q-21801 (the red mushroom with white spots in the picture makes Mario bigger), with the same picture idea and the same kind of wrong answers. Only one of the two should stay in the pool, and since both are Chinese versions of the same source fact, this may need resolving at source level.
- **q-23208** (art) 它装在相机前面，转一转就能变焦或对焦，不用时还要盖上盖子。它里面主要是什么？ → 弯曲的玻璃片: Hint 3 says “这些玻璃片能让光线弯折……”. That literally contains 玻璃片, the core of the answer 弯曲的玻璃片, and no other option mentions glass. The source hint ("The pieces bend the light…") deliberately avoids the word glass. Hint 3 should say “这些部件能让光线弯折，就像你眼睛里的晶状体。” (or similar, without 玻璃). Minor polish: the wrong answer 一面平面镜子 reads more naturally as 一面平面镜.

## Not travelling

None.

## Stale re-translated

None.
