# tr-en-20

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `spain` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 298
- Approved: 296
- Needs work: 2
- Not travelling: 2 (1 confirmed → `translatable: false`, 1 translated again next run)
- Claude calls: 535, about $27.75 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-20&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-18 | tr-en-19 | tr-en-20 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 297 | 298 |
| not travelling |  | 1 | 3 | 2 |
| not travelling confirmed |  | 1 | 1 | 1 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| approved |  | 292 | 295 | 296 |
| needs_work |  | 7 | 2 | 2 |
| needs_work rate | ≤ 20.0 % | 2.3 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.0 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 100.0 % ✓ |
| cost $ |  | $23.21 | $24.30 | $25.27 |
| $ per approved |  | $0.08 | $0.08 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 3 (0 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.47

Major findings on approved questions:

None.

## Needs work

- **q-12390** (al-andalus-and-reconquista) Ibn Hazm of Córdoba wrote it in the 11th century, about the signs of falling in love and of jealousy. What is its title? → The Ring of the Dove: Fact check: wrong. Answer is right, but hint 2 says the title names jewelry worn around the neck. In the English title, a ring is worn on the finger. The Arabic 'tawq' means a neck-collar, so the hint is confusing and mismatched with 'Ring'.
- **q-14426** (school-and-home) They watch you while you eat at school, help you peel your fruit and keep an eye on the playground afterward, but they're not your teachers. Who are they? → The lunchtime monitors: Fact check: uncertain. The fun fact (more than two hours a day with monitors) is not verified. Lunch breaks vary, and many schools with a continuous day have only about 1–2 hours. The rest of the question looks fine.

## Not travelling

- **q-11322** about_language, translate again: Para decir «clickbait» en español, la Fundéu propone una palabra que empieza por «ciber-». ¿Cómo termina? → Anzuelo (Asks how the Fundéu's Spanish coinage “ciberanzuelo” ends; the answer is a Spanish word fragment, so it is about the Spanish language itself.)
- **q-11260** about_language, confirmed: En el castellano de Galicia se dice «¿Ya comiste?» aunque fuera hace cinco minutos, en vez de «¿Ya has comido?». ¿Qué tiempo verbal se prefiere? → Pretérito perfecto simple (Asks about Spanish verb tense names (pretérito perfecto simple vs. compuesto): a question on Spanish grammar.)

## Stale re-translated

None.
