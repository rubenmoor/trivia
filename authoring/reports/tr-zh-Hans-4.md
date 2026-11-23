# tr-zh-Hans-4

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 294
- Needs work: 6
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 609, about $26.58 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-4&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-2 | tr-zh-Hans-3 | tr-zh-Hans-4 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 297 | 300 |
| not travelling |  | 0 | 3 | 0 |
| not travelling confirmed |  | 0 | 3 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 1.0 % ✓ | 0.0 % ✓ |
| approved |  | 296 | 295 | 294 |
| needs_work |  | 4 | 2 | 6 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 0.7 % ✓ | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 1.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 88.3 % ✗ | 78.3 % ✗ | 83.3 % ✗ |
| cost $ |  | $24.13 | $22.51 | $24.58 |
| $ per approved |  | $0.08 | $0.08 | $0.08 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 9 of 59 (15 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 1 (1 major), media 11 (8 major), difficulty 2 (2 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 50 of 60 (83 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.00

Major findings on approved questions:

- **q-21671**: media, difficulty — The media is marked essential, but no file was picked (title null), and the question says “这个……头骨”, so the skull it points to is missing on screen. The facts are right (Meyer et al. 2016: nuclear DNA puts the Sima de los Huesos fossils, about 430 000 years old, on the Neanderthal lineage; at least 28 individuals), and the translation keeps the source's meaning. The difficulty is overrated: it is the only European option among the four, so adults can reason their way to it, which makes it about an 11, not a 14. (http://127.0.0.1:8001/review/q-21671)
- **q-21907**: giveaway, difficulty — In Chinese the answer gives itself away. 丹尼索瓦人, 尼安德特人 and 弗洛勒斯人 are all sound transliterations of foreign place names, while 能人 is a meaning translation that literally says "able person", which is the exact trait the question asks about. Anyone can spot the odd one out without knowing anything, so difficulty 7 is far too high (more like 3), and hint 1 (本领) only confirms it. I checked the facts (Denisova Cave in Siberia, Neander Valley in Germany, Flores in Indonesia, habilis = "handy") and they are correct. The fun fact's 几乎全部 is slightly loose, since there are also teeth and the Xiahe jaw, but that is acceptable. (http://127.0.0.1:8001/review/q-21907)
- **q-21936**: media — The media is marked essential, but no file was picked (title null), and the question text tells players to «看看球门前画出的这块长方形区域». Without a picture of the penalty area, the gamemaster asks players to look at something that isn't on the screen. The translation itself is faithful and natural: 点球 is the right answer, the other options and hints are fine (the 11-metre spot is correct), and the description doesn't give the answer away. (http://127.0.0.1:8001/review/q-21936)
- **q-21986**: media — The essential image is missing (media title is null), but the question says “照片里的节日”, so on the TV it points to a photo that isn't there. Everything else holds up: there are 12 zodiac animals, the hints and the rat-on-the-ox race legend are true, the translation keeps the source's meaning, and the 12 Western star signs question (q-21265) asks a different fact. (http://127.0.0.1:8001/review/q-21986)
- **q-22830**: media — The media is marked essential and the question says “像图中这样的洞穴”, but no file was picked (title null). On the TV the question would point to a picture that isn't there, so it needs a lava tube photo before it plays. The translation itself matches the source and reads naturally. The facts check out: Kazumura Cave is about 65 km long, and lunar pits are thought to lead into lava tubes. The options and hints have no giveaway issues. (http://127.0.0.1:8001/review/q-22830)
- **q-23020**: media — The media role is essential, but no file was picked (title is null), and the question points at a picture ("阿布辛贝的这张巨脸"). On the TV it would refer to an image that isn't there. The facts check out: the Egyptian–Hittite treaty after Kadesh (c. 1274 BC), the empire centred in Anatolia, the capital Hattusa, and the copy at the UN. The translation is faithful and reads naturally, and the options are parallel. (http://127.0.0.1:8001/review/q-23020)
- **q-23022**: media — The media is marked essential, but no file was picked (title is null). The question says "这种恐龙" and needs a picture of the Pachycephalosaurus skull to make sense, so it can't be played without one. The translation itself is faithful and natural: the 25 cm dome fact, the head-butting answer, the hints and the fun fact are all correct, and the four options have similar length and the same form. (http://127.0.0.1:8001/review/q-23022)
- **q-23360**: media — The media is essential and the question points to it ("图中这种河边植物"), but no file was picked (title null), so the players have no picture of the plant. The translation itself is faithful and reads naturally. The facts check out: Egyptian papyrus boats (hint 2) and the Uros totora-reed islands (fun fact) are both true, and the options are sound. (http://127.0.0.1:8001/review/q-23360)
- **q-23574**: media — The question needs essential audio ("听一听"), but the media title is null. No bass recording is attached, so it can't be played as it stands. The translation itself matches the source and reads naturally, the options are parallel, and the fun fact is correct (standard tuning E-A-D-G is one octave below the guitar's four lowest strings). (http://127.0.0.1:8001/review/q-23574)

## Needs work

- **q-21568** (world-cups) 我是一名意大利门将，随国家队赢得2006年世界杯，45岁之后仍在踢职业比赛。我是谁？ → 布冯: Source: hint 1 ("almost his whole career at Juventus") overstates the fact. Buffon played at Parma from 1995 to 2001 and again from 2021 to 2023, and at PSG in 2018–19, so only about 19 of roughly 28 seasons were at Juventus. The source hint should be corrected first, for example to "I played for Juventus for almost twenty years." Also, when this is re-translated, hint 3 should use the pinyin initial of the Chinese name instead of the Latin spelling, e.g. "我的中文译名拼音首字母是 B。" This still works because none of the wrong answers starts with B (卡西利亚斯 K, 诺伊尔 N, 卡恩 K). Fact check: wrong. Hint 1 is inaccurate. Buffon did not spend almost his whole career at Juventus. He played for Parma from 1995 to 2001 and again from 2021 to 2023, and for PSG in 2018–19. That leaves about 19 of roughly 28 seasons at Juventus. The question stem is also loose. He retired in 2023 at age 45, so "45岁之后仍在踢" (still playing after 45) isn't accurate. The answer 布冯, the wrong answers, the "吉吉" (Gigi) nickname, the B hint and the fun fact are otherwise fine. This is from memory, not a fresh search.
- **q-21643** (cats) 按照FCI（世界犬业联盟）规则的正式敏捷赛中，狗要绕着绕杆走“之”字形。绕杆一共有几根？ → 12根: Fact check: uncertain. I couldn't read the FCI agility regulations text. The FCI PDFs came back as unreadable compressed streams, and the KUSA copy returned a 404. So I did not confirm the FCI pole count. From memory, the FCI standard weave set is 12 poles, which fits the answer. But Wikipedia says weave poles come in sets of 5 to 12, and the UK Kennel Club allows 6 or 12. A set of 8 or 10 might therefore be valid in some rules, which would weaken the wrong answers. The fun fact is basically true: agility began at Crufts in the UK in the late 1970s (1978) and was modelled on horse show jumping. The hints are consistent with 12.
- **q-22092** (board-games) 马力欧是任天堂的吉祥物；那位留白胡子、戴高礼帽、拄手杖的老先生，是哪款游戏的吉祥物？ → 大富翁: The description still gives the answer away in Chinese. «钱多得数不清» calls the man extremely rich, and 大富翁 literally means "great rich man", so with only the four options shown it points straight to 大富翁. The 富 is gone, but the meaning is the same. Rewrite the description around his top hat, cane or moustache with no wealth at all, for example «这位老先生出门从不忘戴高礼帽，连睡觉都舍不得摘。». Hint 1 («赚好多钱») also leans on the name; consider making it vaguer (e.g. dice and walking around a board). Minor: «这位大富翁小人» in the fun fact reads awkwardly; «这位大富翁老先生» or «这个大富翁形象» would read better.
- **q-22454** (strange-creatures) 它的鼻子又长又灵活，走路时总把带环纹的尾巴高高翘起。它是什么动物？ → 南美浣熊: Fact: 南美浣熊 is one species (Nasua nasua, Colombia to northern Argentina), but hint 1 gives the range of coatis as a group (Mexico to Argentina). The answer should be the general 长鼻浣熊, or hint 1 should say Colombia to Argentina. Giveaway: in Chinese the answer is the only option containing 浣熊, so the kept raccoon photo all but points to it. This photo needs to be swapped for a neutral image (e.g. a rainforest floor) for the zh version. Fact check: uncertain. The answer 南美浣熊 names one species (Nasua nasua, Colombia to northern Argentina/Uruguay), but hint 1 says the range runs from Mexico to Argentina. That range fits coatis as a group, not this species. The ring-tailed lemur also holds a ringed tail upright when it walks, though its nose is not flexible.
- **q-23228** (famous-logos) 索尼克会像现实中的同类动物一样蜷成球去攻击。这种动物的背上长满了什么？ → 尖刺: The translation drops "hedgehog" from the question («现实中的同类动物»), so players must know which animal Sonic is. Chinese children don't know Sonic well, and two other animals that curl into a ball fit wrong options: the pangolin (穿山甲) has scales and the armadillo has a hard shell. Restore 刺猬 in the question, as the source has it. The 刺 it contains is an acceptable giveaway at difficulty 1, and it is what the translator's notes describe anyway.
- **q-23884** (wonders-of-the-world) 埃菲尔的公司为1889年巴黎世界博览会建造了这座塔。它是用什么材料建成的？ → 铁: In Chinese the tower is universally called 埃菲尔铁塔 ("Eiffel Iron Tower"), and players see it in the essential photo, so its everyday name gives away the answer 铁. The question also falls under the clue-translation case: it collapses in Chinese. It should be marked travels: no (reason: other, the answer is in the landmark's Chinese name) rather than translated.

## Not travelling

None.

## Stale re-translated

None.
