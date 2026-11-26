# tr-zh-Hans-12

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 576, about $26.50 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-12&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-10 | tr-zh-Hans-11 | tr-zh-Hans-12 |
|---|---|---:|---:|---:|
| sources |  | 114 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 114 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 111 | 298 | 298 |
| needs_work |  | 3 | 2 | 2 |
| needs_work rate | ≤ 20.0 % | 2.6 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.9 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.9 % ✓ | 0.7 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.8 % ✗ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.9 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 85.0 % ✗ | 100.0 % ✓ | 100.0 % ✓ |
| cost $ |  | $9.96 | $23.69 | $24.34 |
| $ per approved |  | $0.09 | $0.08 | $0.08 |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 1 (0 major), overlap 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.16

Major findings on approved questions:

None.

## Needs work

- **q-26325** (mythical-creatures) 我侍奉西王母，替她传递消息。李商隐曾请我去探望心上人。我是谁？ → 青鸟: source: this is nearly a duplicate of approved q-26171, the same riddle (the Queen Mother of the West's messenger, Li Shangyin's line about looking in on a loved one) with the same answer, 青鸟. Seeing one gives the other away. The translation itself is accurate and natural, so one of the two questions should be dropped or this one rebuilt around a different fact.
- **q-27176** (chinese-scientists) 我在福建一个贫困山村长大。我培育的杂交水稻“汕优63”，1986—2001年是全国种植面积最大的水稻品种。我是谁？ → 谢华安: Fact check: wrong. The fun fact says 明恢63 was bred by 'the same team'. Sources say Xie Huaan himself bred 明恢63, so the parent line is his own work, not a separate team's. The '1986–2001' span is only roughly supported: one Fujian Daily report says 16 consecutive years from 1986, while other sources say it stayed on top until about 2002. I did not verify the Sanming and poor-village hints.

## Not travelling

None.

## Stale re-translated

None.
