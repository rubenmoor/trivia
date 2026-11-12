# tr-en-21

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `mexico` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 514, about $24.81 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-21&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-19 | tr-en-20 | tr-en-21 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 298 | 300 |
| not travelling |  | 3 | 2 | 0 |
| not travelling confirmed |  | 1 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 295 | 296 | 298 |
| needs_work |  | 2 | 2 | 2 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 100.0 % ✓ | 100.0 % ✓ |
| cost $ |  | $24.30 | $25.27 | $22.40 |
| $ per approved |  | $0.08 | $0.09 | $0.08 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), style 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.41

Major findings on approved questions:

None.

## Needs work

- **q-16424** (contemporary-cinema) Diego Boneta played the singer in “Luis Miguel: The Series”. How many seasons did the show have? → 3: Fact check: wrong. The answer (3 seasons) is right. But hint 2 is false: season 2 aired in 2019 and season 3 in 2021, so the last two seasons did not come out in the same year. (Season 1 was 2018.)
- **q-16598** (telenovelas) The whole family gathers in front of the TV to watch me, the streets go empty, and the villain finally gets punished. What am I? → The final episode: source: the fact check couldn't confirm the fun fact's claim that people moved parties and weddings so they wouldn't miss telenovela finales, and I can't confirm it either. The documented effect is that streets emptied (for example, the 1987 finale of Cuna de lobos). The source's fun fact should be replaced with a documented one, such as the Cuna de lobos finale emptying Mexico's streets. Then the translation can follow it. Apart from that, the translation is faithful and natural. Fact check: uncertain. Answer (the final episode) and wrong answers are fine. Cuna de lobos (1987) finale did empty streets and halt daily life in Mexico. But no source supports the fun fact's claim that people moved parties and weddings. Only the streets and daily-life impact is documented.

## Not travelling

None.

## Stale re-translated

None.
