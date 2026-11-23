# tr-zh-Hans-10

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 114 (0 stale re-translated)
- Translated: 114
- Approved: 111
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 220, about $12.85 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-10&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-8 | tr-zh-Hans-9 | tr-zh-Hans-10 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 114 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 114 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 295 | 297 | 111 |
| needs_work |  | 5 | 3 | 3 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 1.0 % ✓ | 2.6 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 1.0 % ✓ | 0.7 % ✓ | 0.9 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.9 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.3 % ✓ | 1.8 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.9 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 88.3 % ✗ | 86.7 % ✗ | 85.0 % ✗ |
| cost $ |  | $27.17 | $28.15 | $9.96 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 8 of 58 (14 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 1 (0 major), ambiguity 1 (1 major), overlap 1 (1 major), media 12 (9 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 51 of 60 (85 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.89

Major findings on approved questions:

- **q-21415**: media — The media is marked essential, but no file was picked (title is null). The question starts with «看照片», and without the photo of El Castillo, Tikal, Palenque and Copán all fit "a famous site with a Maya pyramid", so the question can't be played as it is. The translation itself is faithful and natural. The hints and fun fact are correct: Chichén Itzá is one of the New Seven Wonders and is on the Yucatán Peninsula, and the equinox serpent shadow is real. (http://127.0.0.1:8001/review/q-21415)
- **q-21727**: media — The essential image is missing (media title is null). "这些是用什么做的？" only works if a photo of French fries is shown, so the question can't be played as it is. The translation itself is faithful and natural: it uses 土豆 (the standard mainland word), the hints are true, the description doesn't give the answer away, and the fun fact about Belgium and France both claiming fries is accurate. (http://127.0.0.1:8001/review/q-21727)
- **q-22751**: media — The media is marked essential, but no file was picked (title is null). "这是用来干什么的？" can't be answered without a picture of swim fins. Everything else checks out: the translation is faithful and natural, the options and hints are fine, and the Franklin fun fact is true (he made wooden hand fins at about age 11). (http://127.0.0.1:8001/review/q-22751)
- **q-22847**: media, ambiguity — The media is marked essential, but no file was picked (title null). The question «这种甲虫» depends on a photo of the Goliath beetle. Without it, "one of the heaviest insects" also fits the titan beetle and Hercules beetle (South America) and the Atlas beetle (Southeast Asia), so wrong options become defensible. The facts (Goliath beetle in Africa, larvae weighing about 100 g) and the Chinese wording are fine. (http://127.0.0.1:8001/review/q-22847)
- **q-23522**: media — The media is marked essential but no file was picked (title is null). The question says «这种蛙» and only makes sense with a photo of a poison dart frog, so it can't be played as it is. The translation itself is faithful and natural. The facts hold: Emberá hunters do put Phyllobates frog poison on blowgun darts, and zoo-raised dart frogs aren't toxic because they don't eat the wild ants and mites. The options and hints are fine. (http://127.0.0.1:8001/review/q-23522)
- **q-23537**: media — The media is essential, but no file was picked (title null). The question asks about "这个符号", so without an image of ∞ it can't be played. Everything else holds up. The translation stays true to the source. The Wallis 1655 fun fact is correct. None of the wrong options can be argued as correct. The Buzz Lightyear hint doesn't contain 无穷, and the difficulty of 5 is reasonable. (http://127.0.0.1:8001/review/q-23537)
- **q-23771**: media — The media is marked essential, but no file was picked (title is null), so the "看照片" question would play with no photo of udon. The translation itself is faithful and natural. The facts check out: udon is made from wheat flour, water and salt, and dough is traditionally kneaded by foot. 通心粉 in hint 3 is fine as a stand-in for spaghetti, and 乌冬 in the question is no more of a giveaway than "udon" in the source. (http://127.0.0.1:8001/review/q-23771)
- **q-23880**: media — The media role is essential and the question says "像这样的杂耍球" ("juggling balls like these"), but no file was picked (title null), so the TV would refer to a picture that isn't there. The translation itself is faithful and natural. The answer is correct (bean bags and thud balls hold pellets, seeds or rice). The Beni Hasan fun fact holds up: it's the tomb of Baqet III, about 4000 years old. (http://127.0.0.1:8001/review/q-23880)

## Needs work

- **q-22454** (strange-creatures) 它有又长又灵活的鼻子，走路时把带环纹的尾巴高高翘起。这是什么动物？ → 南美浣熊: The kept image is a raccoon ('Raccoon_by_water'). The answer 南美浣熊 is the only option containing 浣熊, so the raccoon photo points straight at it. It also shows the wrong animal, so it needs to be replaced with a coati photo or a neutral decorative image. Hint 1 says the animal lives from Mexico to Argentina, which describes coatis as a group. 南美浣熊 (Nasua nasua) lives only in South America. Either use the genus-level name (长鼻浣熊) as the answer or limit hint 1 to South America. Fact check: wrong. The image is a raccoon (query 'raccoon in forest'), not a coati. It shows the wrong animal for this question. Also 'Mexico to Argentina' fits coatis in general, not only 南美浣熊 (Nasua nasua).
- **q-22786** (video-games) 在《超级马力欧》游戏里，一个长得很像图中这种的蘑菇会让马力欧怎样？ → 让他变大: This duplicates approved q-21801 («马力欧吃到一个像图中这样的红底白点蘑菇，会发生什么？» → «他会变大»). Both ask the same fact with the same answer and the same kind of image, so one of them should go. The translation itself is accurate, but «一个长得很像图中这种的蘑菇» reads awkwardly. If this question is kept, «像图中这样的蘑菇» would read better.
- **q-23051** (football) 足球点球要在球门前的点球点上踢。这个点离球门线大约多远？ → 11米: This duplicates approved q-23860 ("点球大战中你站在点球点上，球门离你大约多远？" → 11米). Both ask how far the penalty spot is from the goal, with the same answer, so one of them should be dropped from the zh-Hans pool. The translation itself is faithful and natural.

## Not travelling

None.

## Stale re-translated

None.
