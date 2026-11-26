# tr-zh-Hans-14

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 591, about $28.17 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-14&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-12 | tr-zh-Hans-13 | tr-zh-Hans-14 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 293 | 292 |
| needs_work |  | 2 | 7 | 8 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 2.3 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 2.3 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 95.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $24.34 | $25.47 | $25.91 |
| $ per approved |  | $0.08 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 1 (0 major), overlap 1 (1 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.26

Major findings on approved questions:

None.

## Needs work

- **q-25999** (classic-tv-series) 《武林外传》里，白展堂是跑堂的，那李大嘴是干什么的？ → 厨师: Fact check: uncertain. The answer (厨师) and hints are right: 吕秀才 is the 账房, and 李大嘴 is the cook at 同福客栈. The fun fact is the problem. I found no source saying 李大嘴's nickname puns on being greedy and talkative. The wrong answers hold up, but 捕快 is a little risky because some sources say he once worked as a constable.
- **q-26159** (four-great-inventions) 黑龙江阿城出土的铜火铳是现存最古老的火器之一。它是由哪种更早的中国火药武器发展来的？ → 突火枪: The answer 突火枪 doesn't match the source's "fire lance" or the hints. 突火枪 (1259) was a wide bamboo barrel that fired a projectile (子窠). Hints 2 and 3, a tube on a long pole spraying flame from a bamboo or paper tube, describe the earlier fire lance (火枪). The fact check is uncertain, so as written the answer and hints contradict each other. To fix it: make the answer the fire lance, worded so it doesn't read as the modern word for a musket, e.g. «火枪（宋代喷火长矛）» or «长竹竿火枪». Or keep 突火枪 and rewrite hints 2 and 3 for a bamboo barrel that shoots a projectile. The second option drifts from the source's answer. Fact check: uncertain. The Acheng bronze gun is usually said to descend from the fire lance (火枪), a tube on a pole that sprayed flame. 突火枪 is a later bamboo-barrel gun that fired a projectile. Hints 2 and 3 describe the fire lance, not 突火枪, so they don't fit the answer. Some Chinese sources do name 突火枪 as the predecessor.
- **q-26272** (mega-projects) 青海塔拉滩光伏电站里，牧民让羊在光伏板下吃草。羊为电站干的是什么活？ → 防止草长高挡住光伏板: Fact check: wrong. The description says this is the "only power station in the world" with bleating employees. That is false. Sheep graze at many solar farms worldwide, including in the US, UK and Australia. The answer, hints and fun fact are fine: sheep keep grass from shading the panels, and locals call them "光伏羊". This is from memory, not searched.
- **q-26529** (dynasties-overview) 青铜器利簋上记载了这场战役：甲子日清晨，商朝士兵掉转了手中的戈。是哪场战役？ → 牧野之战: Source: the question says the Li gui (利簋) records the Shang soldiers turning their weapons, and the translation repeats that. The inscription only says that King Wu attacked Shang on the morning of a jiazi day and won (珷征商，唯甲子朝，岁鼎，克闻夙有商). The weapon-turning (前徒倒戈) comes from 《尚书·武成》 and other texts, not from the bronze. The source clue needs rewording, for example to "利簋铭文记载，武王在甲子日清晨征商取胜", with the 倒戈 detail credited to the texts in the fun fact. Then retranslate. Fact check: wrong. The answer (牧野之战) is right. But the question says the Li Gui records the Shang soldiers turning their weapons. The inscription only says 武王征商，唯甲子朝，岁鼎，克昏夙有商: King Wu attacked Shang on the morning of jiazi day and won. The 倒戈 detail comes from the 尚书·武成 and 诗经 texts, not from the vessel. I didn't run a web search; this is from memory of the inscription.
- **q-26585** (martial-arts) 一个圆被分成黑白两半，每一半里都有一个对方颜色的圆点，代表阴和阳。它叫什么？ → 太极图: This question is a duplicate of approved q-27366. Both ask about a circle split into black and white halves, each with a dot of the other colour, and both have the answer 太极图. The wording is almost the same. The source has the same problem, so it is not a translation error. One of the two should be retired or replaced with a question about a different fact.
- **q-26975** (board-and-tile-games) 打麻将时，一位玩家“听牌”了，说明他还差几张牌就能和牌？ → 1: source: Hint 2 ("The player can't improve the hand any more and can only wait" / “这手牌已经没法再改进，只能等。”) is false. A player who is 听牌 can still swap tiles to improve the hand or change the wait (换听/改听). The source needs a true hint 2, for example “只差最后一张牌就能和牌。” or “这时他在等一张特定的牌。”. Then the translation follows it. The rest of the translation is accurate and reads naturally. Fact check: wrong. The answer (1 tile) is right and the wrong answers are wrong. Hint 2, “这手牌已经没法再改进,只能等”, is false. A player in tenpai can still swap tiles to improve the hand or change the wait, for example 换听 or 改良听牌. The fun fact is fine: 聴牌/tenpai is a loanword from the Chinese 听牌.
- **q-26983** (bronzes-and-porcelain) 这种小口、丰肩、瘦底的瓶子从宋代起开始烧制。它最初是用来做什么的？ → 盛装酒水: Source: the claim that these vases were made "from the Song dynasty on" is loose. Chinese sources usually say the meiping first appeared in the Tang and that its classic shape was fixed and became popular in the Song. The translation's «从宋代起开始烧制» makes it a firmer "began in the Song". The source should say the shape became standard in the Song (e.g. «宋代定型并流行»), and the translation should then follow it. Apart from that, the translation is faithful and natural. Fact check: uncertain. The answer (wine) is right. But 'from the Song dynasty' is loose: the meiping is said to have first appeared in the Tang, and the typical shape was fixed in the Song. The Song name was 经瓶.
- **q-27997** (three-kingdoms-to-sui) “建安风骨”得名于“建安”这个年号。建安是哪个时期的年号？ → 东汉末年: source: the fun fact is inaccurate. The Jian'an era name was changed to Yankang (延康) in early 220, after Cao Cao died and Cao Pi became King of Wei. That was months before Cao Pi took the throne as emperor and founded Wei in late 220. The source fun fact should say the era ended in 220 after Cao Cao's death, when Cao Pi became King of Wei. The translation itself is faithful and natural.

## Not travelling

None.

## Stale re-translated

None.
