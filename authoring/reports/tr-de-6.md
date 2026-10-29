# tr-de-6

Made by `qgen batch --translate de` on 2026-10-29 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 297
- Needs work: 2
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 841, about $32.06 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-6&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-4 | tr-de-5 | tr-de-6 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 294 | 300 | 299 |
| not travelling |  | 6 | 0 | 1 |
| not travelling confirmed |  | 6 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 2.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 288 | 297 | 297 |
| needs_work |  | 6 | 3 | 2 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 1.0 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.4 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 100.0 % ✓ |
| cost $ |  | $28.41 | $28.08 | $29.79 |
| $ per approved |  | $0.10 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.27

Major findings on approved questions:

None.

## Needs work

- **q-0913** (recycling) Dir fällt der Badezimmerspiegel herunter und zerspringt. Wie viele Jahre Pech drohen dir laut dem bekannten Aberglauben? → 7: Hint 1 („Diese Zahl gilt in vielen Kulturen als besondere Glückszahl“) gives the answer away: of 1, 20 and 100, only 7 is a well-known lucky number. Hint 1 should be vague, e.g. that the superstition goes back to ancient Rome, where people believed the body renews itself every few years. The lucky-number idea could become hint 2, and the current hint 2 (odd and less than ten) could go.
- **q-4507** (physics) Ein fallen gelassener Ball springt nie höher zurück, als man ihn losgelassen hat, und eine Achterbahn steigt nie höher als ihr erster Hügel. Welches Gesetz erklärt beides? → Energieerhaltungsgesetz: The question text is about 171 characters, above the 160-character limit for German. Its first clause is also clumsy: "springt nie höher zurück, als man ihn losgelassen hat" compares height with an action, not a place. Tighten it, for example: „Ein fallen gelassener Ball springt nie über seine Starthöhe, eine Achterbahn nie über ihren ersten Hügel. Welches Gesetz erklärt beides?“

## Not travelling

- **q-2047** about_language, confirmed: Cuando se arma un lío tremendo se dice: 'se armó la de…'. ¿Qué lugar completa la frase? → San Quintín (Asks players to complete a Spanish idiom ('se armó la de San Quintín'). German has no version that names San Quintín, and asking about the Spanish saying would make it a question about the Spanish language.)

## Stale re-translated

None.
