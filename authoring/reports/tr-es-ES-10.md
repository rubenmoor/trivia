# tr-es-ES-10

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 793, about $31.55 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-10&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-8 | tr-es-ES-9 | tr-es-ES-10 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 297 | 298 |
| needs_work |  | 2 | 3 | 2 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 1.0 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 100.0 % ✓ |
| cost $ |  | $28.53 | $29.07 | $28.80 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 2 (0 major), overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.75

Major findings on approved questions:

None.

## Needs work

- **q-1305** (circus) Viste un traje de rombos de colores, lleva máscara negra y nació en la comedia italiana. ¿Quién es? → Arlequín: Fact check: wrong. The question text says he "viste un traje de rombos... lleva máscara negra" (fine), but the fun fact is shaky: the usual Spanish term is "arlequinado"/"diseño de arlequín", and "todavía se le llama «diseño arlequinado»" is not a standard phrase. Also the description says "hace cuatro siglos" while Arlequín's diamond patchwork costume became standardized in the 17th century, so that is acceptable. The hint "Su nombre empieza por «Arle-»" nearly gives away the answer, and the question grammar "Viste" (no subject) is ambiguous. Answer Arlequín is correct; Pierrot (white, no mask), Polichinela and bufón are wrong answers.
- **q-4079** (world-war-ii) Cuando la guerra impidió que el jarabe de Coca-Cola llegara a Alemania, allí se inventó un nuevo refresco de naranja: la Fanta. ¿En qué década? → Los años 40: source: the question calls the original German Fanta (1940) "a new orange soda", but it wasn't orange-flavoured. It was made from leftovers such as whey and apple pomace, and orange Fanta first came out in Italy in 1955. The source should drop "orange" (for example "a new soda" or "a new fruit soda"), and the translation should then follow it. Apart from this, the Spanish translation is faithful and reads naturally.

## Not travelling

None.

## Stale re-translated

None.
