# tr-es-ES-14

Made by `qgen batch --translate es-ES` on 2026-10-29 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 843, about $32.80 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-14&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-12 | tr-es-ES-13 | tr-es-ES-14 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 300 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 295 | 296 | 298 |
| needs_work |  | 5 | 3 | 2 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 1.0 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 100.0 % ✓ |
| cost $ |  | $30.69 | $29.05 | $30.02 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 3 (0 major), fact 4 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.79

Major findings on approved questions:

None.

## Needs work

- **q-0077** (disney-films) En «Encanto», ¿cuál es el don de Luisa? → Una fuerza sobrehumana: source: the fun fact says every member of the Madrigal family has a magic door with their gift. That isn't true: Mirabel only gets her door at the end, and Abuela Alma and the in-laws (Félix, Agustín) have no gift and no door. The source's fun fact needs rewording, for example «Cada nieto de la familia Madrigal recibe una puerta mágica con su don… salvo Mirabel, hasta el final». The translation itself is faithful and reads as natural Spanish from Spain.
- **q-4943** (trees) Esta persona vigila un bosque, está atenta a los incendios y protege sus animales y plantas. ¿Cómo se llama este oficio? → Guarda forestal: Fact check: wrong. The hint 'El nombre del oficio termina con la palabra «forestal»' is false: the answer 'Guarda forestal' ends in 'forestal', but it is a weak/ambiguous hint. More importantly, the question and hints mix roles. The question describes a forest ranger/guard (guarda forestal), but hint 2 and the fun fact describe fire lookouts (vigías de incendios), a different job. The answer 'Guarda forestal' is acceptable, but the fun fact and hint 2 describe another job.

## Not travelling

None.

## Stale re-translated

None.
