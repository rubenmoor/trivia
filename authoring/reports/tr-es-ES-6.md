# tr-es-ES-6

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 829, about $29.30 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-6&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-4 | tr-es-ES-5 | tr-es-ES-6 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 295 | 299 | 298 |
| needs_work |  | 4 | 1 | 2 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 100.0 % ✓ | 100.0 % ✓ |
| cost $ |  | $26.83 | $27.11 | $27.00 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 1 (0 major), overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.30

Major findings on approved questions:

None.

## Needs work

- **q-1952** (winter-olympics) ¿Cuándo se celebran los Juegos Paralímpicos de invierno, comparados con los Juegos Olímpicos de invierno? → Poco después, en la misma sede: source: hint 2 («Nunca se celebran antes que los Juegos Olímpicos») is historically wrong. The 1980 Winter Paralympics in Geilo (1–7 February) came before the Lake Placid Olympics (13–24 February). The source should say «Hoy en día nunca se celebran antes…» or something similar, and the translation should then follow it. The translation is otherwise identical to the source and reads naturally in Spain's Spanish.
- **q-3910** (roman-empire) ¿Qué famoso líder romano dio su nombre al mes de julio? → Julio César: In Spanish the answer «Julio César» starts with the very word «julio» that the question asks about, so the question text gives the answer away even to a small child. The English source only works because «Julius» and «July» are less alike. The same fact can't be asked in Spanish without this giveaway, so this item should be marked as not travelling (about_language) and not played in es-ES, or replaced with a different question.

## Not travelling

None.

## Stale re-translated

None.
