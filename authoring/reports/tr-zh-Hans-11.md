# tr-zh-Hans-11

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 571, about $25.75 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-11&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-9 | tr-zh-Hans-10 | tr-zh-Hans-11 |
|---|---|---:|---:|---:|
| sources |  | 300 | 114 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 114 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 297 | 111 | 298 |
| needs_work |  | 3 | 3 | 2 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 2.6 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.7 % ✓ | 0.9 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.9 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 1.8 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.9 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 86.7 % ✗ | 85.0 % ✗ | 100.0 % ✓ |
| cost $ |  | $28.15 | $9.96 | $23.69 |
| $ per approved |  | $0.09 | $0.09 | $0.08 |
| **health** | | ✗ fail | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: overlap 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.06

Major findings on approved questions:

None.

## Needs work

- **q-25990** (city-snacks) 西安的肉夹馍是把剁碎的炖肉夹进又圆又酥的馍里。因此它常被叫作什么？ → 中式汉堡: Fact check: uncertain. The answer 中式汉堡 is right. Roujiamo is widely called the "Chinese hamburger", and the three wrong answers aren't its usual nickname. The fun fact (肉夹于馍 abbreviation) is a common explanation. The description says "好几千年" (several thousand years), which overstates the usual claim of about 2,000+ years (Qin/Warring States origin). I did not run web searches, so this is from memory.
- **q-27199** (chinese-video-games) 在红白机游戏《坦克大战》里，下面哪种东西在战场地图上找不到？ → 岩浆: source: the fun fact says the map editor is *why* Battle City was popular with Chinese kids in the 1990s («所以»). The fact check found no support for that link, since the game's popularity in China came mainly from Famicom clone consoles. The English source has the same claim, so the source fun fact needs rewriting without the causal link, for example: "Battle City had a built-in map editor, and it was hugely popular with Chinese kids in the 1990s on Famicom clone consoles." The zh-Hans translation should then follow it. The rest of the translation is faithful and natural. Fact check: wrong. The answer is right. Battle City has brick walls, steel walls, water, trees and ice, and it has no lava. The hints are accurate: tanks can't cross water, but shells can fly over it, and trees hide tanks. The fun fact is the problem. The game does have a map editor (construction mode). But the "所以" (so) claims that this made it popular with Chinese kids in the 1990s, and I found no source for that. Its popularity in China came mainly from Famicom clone consoles and cartridges.

## Not travelling

None.

## Stale re-translated

None.
