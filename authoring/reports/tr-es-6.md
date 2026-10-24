# tr-es-6

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 672, about $31.24 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-6&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-4 | tr-es-5 | tr-es-6 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 293 | 297 |
| needs_work |  | 2 | 7 | 3 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 2.3 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 1.7 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.96 | $29.52 | $28.43 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 4 (0 major), overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.81

Major findings on approved questions:

None.

## Needs work

- **q-2654** (physics) Tres de estos inventos solo funcionan gracias a la física cuántica. ¿Cuál NO la necesita? → La máquina de vapor: Fact check: wrong. Hint 1 says quantum physics was 'recién descubierta' in the 20th century, which is loosely true (Planck 1900), but the main flaw is the fun fact/phrasing: 'solo funcionan gracias a la física cuántica' is fine for laser, LED, solar panel. Answer (steam engine) is correct. However the hint 'recién se descubrió en el siglo XX' is awkward but accurate. Minor: the fun fact says 'miles de millones' of transistors per chip, which is true for modern phone chips. Overall the question is essentially correct; only the hint wording is weak.
- **q-4079** (world-war-ii) Cuando la guerra impidió que el jarabe de Coca-Cola llegara a Alemania, allí se inventó un nuevo refresco de naranja: la Fanta. ¿En qué década? → La década de 1940: source: the question calls wartime German Fanta "a new orange soda", but the 1940 German Fanta was made from whatever was available (whey, apple pomace, fruit leftovers). Orange Fanta only appeared in 1955 in Italy. The source should drop "orange" (e.g. "a new soda, Fanta"), and then the translation should follow it. Apart from that, the Spanish translation is faithful and idiomatic.
- **q-5979** (shoes-and-accessories) ¿Para qué sirve esto? → Llevar ropa en un viaje: Source: the fun fact claims the wheeled suitcase "was only patented in 1972", and that's wrong. Earlier wheeled-luggage patents exist, for example Arthur Browning's in Canada in the late 1940s and several US ones from before that. Bernard Sadow's 1972 patent is just the famous one, the first to catch on commercially. The fix belongs in the source, something like "Bernard Sadow's 1972 rolling suitcase was the first to catch on". The Spanish translation is otherwise faithful and natural.

## Not travelling

None.

## Stale re-translated

None.
