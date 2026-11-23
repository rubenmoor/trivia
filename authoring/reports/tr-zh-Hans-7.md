# tr-zh-Hans-7

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 563, about $27.98 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-7&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-5 | tr-zh-Hans-6 | tr-zh-Hans-7 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 294 | 293 | 295 |
| needs_work |  | 5 | 7 | 5 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 2.3 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 1.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 2.0 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 83.3 % ✗ | 86.7 % ✗ | 85.0 % ✗ |
| cost $ |  | $24.61 | $25.96 | $25.56 |
| $ per approved |  | $0.08 | $0.09 | $0.09 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 8 of 59 (14 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), media 14 (8 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 51 of 60 (85 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.43

Major findings on approved questions:

- **q-21783**: media — The media is marked essential, but no file was picked (title null). The question says “这座金字塔” and never names the Great Pyramid, so without the picture players can't tell which pyramid it means until hint 1. The facts check out: the King's and Queen's Chambers have two shafts each, four in total, and in 1993 Gantenbrink's Upuaut-2 robot found a small stone door with two copper handles. The translation is faithful and reads naturally. (http://127.0.0.1:8001/review/q-21783)
- **q-22417**: media — The media is marked essential but its title is null, so no file was picked. The question says “图中这样的道岔拉杆”, so it refers to a picture that isn't there. The translation itself checks out: it matches the source, the Chinese reads naturally, 电车难题 is the standard mainland term, and the hints don't give the answer away. The fun fact is correct: Philippa Foot proposed the dilemma in 1967. (http://127.0.0.1:8001/review/q-22417)
- **q-22806**: media — The media is set to essential, but no file was picked (title null), and the question says “像图中这样” (like the one in the picture), so it refers to an image that isn't there. The translation itself is faithful and natural, and the facts hold up: Christie's step-grandmother "expected the worst" is from her autobiography. No overlap with q-21582: hint 3 names Christie, but that question asks for the author of a different novel. (http://127.0.0.1:8001/review/q-22806)
- **q-22916**: media — The media is marked essential but no file was picked (title null). The question says “这种船” and only works if a kayak is shown, so without the picture players can't tell which boat it means. The translation itself matches the source: the answer, options, hints and fun fact (kayak from qajaq) are correct, and the wording is natural mainland Chinese. (http://127.0.0.1:8001/review/q-22916)
- **q-23110**: media — The question needs an essential silhouette image (“这张剪影图”), but media.title is null, so no file was picked and the question can't be played. The translation itself is faithful and reads naturally, the hints and fun fact are correct, and difficulty 2 fits. (http://127.0.0.1:8001/review/q-23110)
- **q-23297**: media — The media is marked essential, but no file was picked (title is null). The question says «照片里这样的计算机», so without a photo of a server rack it can't be played as written. The translation itself is faithful and reads naturally: 服务器 is correct, the three wrong answers are clearly wrong, the hints and fun fact are true, and hint 3 swapping the English etymology for the English word "server" is acceptable for a hint 3. (http://127.0.0.1:8001/review/q-23297)
- **q-23651**: media — The question needs an essential video ("看：海水一点点退去", the draining-oceans animation), but no file was picked (media title is null). Without it, the 看 prompt points at nothing on the TV. Apart from that the translation is faithful and natural. I checked the facts: the Bering Strait is about 50 m deep, sea level in the last Ice Age was about 120 m lower, and Beringia (白令陆桥) is correct. The wrong options are really wrong: Gibraltar is about 300 m deep, and Asia and Australia were never joined because of the Wallace Line. The hints don't give the answer away. (http://127.0.0.1:8001/review/q-23651)
- **q-23825**: media — The media is marked essential and the question opens with "看图片：这块磁铁…", but no file was picked (title null), so players get no picture. The translation itself reads naturally and matches the source. The options are parallel and the hints and fun fact are correct; the compass fun fact was rendered fine as "指向南北". (http://127.0.0.1:8001/review/q-23825)

## Needs work

- **q-21568** (world-cups) 我是意大利门将，随国家队夺得2006年世界杯，过了45岁还在踢职业比赛。我是谁？ → 布冯: Source: hint 1 ("I spent almost my whole career at Juventus") is inaccurate. Buffon spent about 19 of his roughly 28 professional seasons at Juventus (2001–2018 and 2019–2021). He also played for Parma (1995–2001 and 2021–2023) and PSG (2018–19). The translation copies this faithfully as 我几乎整个职业生涯都效力于尤文图斯. The source hint should say something like "I played for Juventus for almost 20 years", and the translation can then follow. Minor point once that is fixed: hint 3 still relies on the Latin letter B. A hint that works in Chinese, such as the number of characters in the Chinese name, would suit zh-Hans better. Fact check: wrong. The answer 布冯 is right. The wrong answers are really wrong, and 2006 World Cup, nickname Gigi, retiring in 2023 at 45 and the B spelling are all correct. Hint 1 is misleading. Buffon spent only about 19 of his ~28 seasons at Juventus (2001–2018, 2019–2021). He also played for Parma (1995–2001, 2021–23) and PSG (2018–19). 'Almost his whole career' overstates it. The clue 过了45岁 is also slightly loose, since he retired aged 45.
- **q-21696** (harry-potter) 哪种魔法游戏有点像弹珠，玩家每丢一分，棋子就会朝他喷出一股臭液？ → 高布石: Hint 3 says the name starts with "高". That is the answer's first character, which the zh-Hans rules forbid in hint 3, and it singles out 高布石 among the options. Rewrite hint 3 without it, for example: "它的棋子通常用石头做成，是一颗颗小圆球。" Separately, the fact check couldn't confirm hint 1 (Harry seeing students play it). Both the source and the translation could use a verifiable hint instead, such as "霍格沃茨有这项游戏的俱乐部。" Fact check: uncertain. The answer, the wrong answers, the Eileen Prince hint and the fun fact check out. Gobstones squirt foul liquid at the player who loses a point, and the stones are usually stone but can be precious metal. I couldn't verify hint 1, that Harry sees other students playing it. The sources only show a Gobstones Club sign-up sheet in Order of the Phoenix.
- **q-22044** (prehistory) 石器时代对应石头，那么金属时代的第一个阶段对应的是…… → 铜: Source problem: "the first stage of the Metal Age" is a European/Spanish school periodisation (Copper, Bronze, Iron). Chinese school teaching uses the three-age system, where 青铜时代 follows the Stone Age directly, so 青铜 is a defensible answer for Chinese players. 金属时代 is also not a common Chinese term, and 铜 versus 青铜 blurs even more in Chinese (铜器 is often used for bronze ware). The source needs a clue that only copper fits, e.g. 'the first metal humans learned to smelt' or 'the metal of the Copper Age / 铜石并用时代'. The translation alone can't fix this.
- **q-22454** (strange-creatures) 它的鼻子又长又灵活，走路时总把带环纹的尾巴高高翘起。这是什么动物？ → 南美浣熊: Fact: the answer 南美浣熊 (South American coati, Nasua nasua) does not live in Mexico, so hint 1's range "从墨西哥一直到阿根廷" is wrong for it. The source's "Coati" means the whole genus, so the answer should be 长鼻浣熊 or the range should be narrowed to South America. Giveaway: the kept media is a raccoon photo ('Raccoon by water'). In Chinese, the answer is the only option with 浣熊 in its name, so the picture points straight to it. The image should be replaced with a coati, or with a decorative picture of the forest it lives in. Fact check: wrong. The image shows a North American raccoon, not a coati. It would mislead players on a coati question. Also, the hint's range (Mexico to Argentina) fits coatis as a group. The South American coati lives only in South America.
- **q-23265** (reptiles) 下面哪只宝可梦，和另外三只不属于同一个进化家族？ → 蚊香蝌蚪: In Chinese the odd one out gives itself away: the official names 呱呱泡蛙, 呱头蛙 and 甲贺忍蛙 all contain 蛙, and 蚊香蝌蚪 is the only one without it, so anyone can solve it without knowing Pokémon. The official names can't be changed, so the translation can't fix this. Either change the source's options (for example, use a wrong family whose mainland names don't share a character) or don't play this item in zh-Hans.

## Not travelling

None.

## Stale re-translated

None.
