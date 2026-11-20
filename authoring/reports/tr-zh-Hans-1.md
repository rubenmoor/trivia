# tr-zh-Hans-1

Made by `qgen batch --translate zh-Hans` on 2026-11-20 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 50 (0 stale re-translated)
- Translated: 50
- Approved: 50
- Needs work: 0
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 184, about $6.81 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-1&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-1 |
|---|---|---:|
| sources |  | 50 |
| stale re-translated |  | 0 |
| translated |  | 50 |
| not travelling |  | 0 |
| not travelling confirmed |  | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ |
| approved |  | 50 |
| needs_work |  | 0 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ |
| audited |  | 50 |
| audit/review agreement | ≥ 90.0 % | 88.0 % ✗ |
| cost $ |  | $5.22 |
| $ per approved |  | $0.10 |
| **health** | | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 6 of 50 (12 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), media 8 (6 major), style 2 (2 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 50 (0 %)
- Audit/review agreement (both accept or both not): 44 of 50 (88 %)
- Sample: 50 audited of 50; 50 Claude calls, about $1.59

Major findings on approved questions:

- **q-21226**: media — The media is marked essential, but no file was picked (title null). Without the photo, “看看这张照片：这种天气现象叫什么？” can't be answered. Everything else holds up: the translation matches the source, the wording is natural mainland Chinese, the options are parallel, the hints are fine (the Wizard of Oz tornado is real), and the fun fact is accurate (the US has about 1200 tornadoes a year). (http://127.0.0.1:8001/review/q-21226)
- **q-21376**: media — The media role is essential and the question opens with "看照片", but no file was picked (title is null). Without a photo of a glass frog showing its see-through belly, the question can't be played. The translation itself is faithful and natural: the answer, the options and the hints match the source, and the fun fact about hiding red blood cells in the liver while asleep is true (Science, 2022). (http://127.0.0.1:8001/review/q-21376)
- **q-21377**: media — The media is marked essential, but no file was picked (title null). The question says “看看这条带条纹的小观赏鱼” and never names the fish, so without a zebrafish photo players can't play it. The translation itself is faithful and reads naturally, with full-width punctuation and options of the same form. The hints and fun fact are correct: zebrafish embryos are transparent, the fish can regrow heart tissue, it is a widely used lab model, and GloFish began as zebrafish given a jellyfish or coral gene. (http://127.0.0.1:8001/review/q-21377)
- **q-21482**: media, style — The media is marked essential ("看看这张特写"), but no file was picked (title null). Without the close-up photo the question can't be played. The translation itself is faithful and the options are consistent. One minor style point: the fun fact leaves "kheer" in Latin script; a Chinese rendering such as «印度的甜奶米粥（kheer）» would read more naturally. (http://127.0.0.1:8001/review/q-21482)
- **q-21595**: media — The media is marked essential but no file was picked (title is null). The question only says "这座建筑" (this building), so without a photo of Hagia Sophia it can't be played. Everything else is fine: the answer, the hints (hint 3 doesn't use the characters 君士坦丁), the fun fact, the fidelity to the source and the Chinese wording. (http://127.0.0.1:8001/review/q-21595)
- **q-21682**: media, style — The media is marked essential, but no file was picked (title null), yet the question points to "图中这样的纸折作品". Without the picture of a paper crane, the question refers to an image that isn't on screen. Two smaller points: "纸折作品" reads like translationese, and "折纸" or "纸鹤" would be more natural. The facts (senbazuru/千羽鹤, Japan, the hints) are correct and match the source. (http://127.0.0.1:8001/review/q-21682)

## Needs work

None.

## Not travelling

None.

## Stale re-translated

None.
