# tr-es-7

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 692, about $33.05 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-7&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-5 | tr-es-6 | tr-es-7 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 293 | 297 | 296 |
| needs_work |  | 7 | 3 | 4 |
| needs_work rate | ≤ 20.0 % | 2.3 % ✓ | 1.0 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 1.0 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $29.52 | $28.43 | $30.10 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), overlap 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.95

Major findings on approved questions:

None.

## Needs work

- **q-2776** (marvel-superheroes) Bestia apareció por primera vez en X-Men #1, junto al equipo original. ¿En qué década salió ese cómic? → Los años 60: source: the fun fact says Beast turned blue in 1975, but his fur was grey in Amazing Adventures #11 (1972) and was recoloured blue within about a year (1972–73). He was already blue before he joined the Avengers in 1975. The rater flagged this as well. Fix the date in the English source, or drop it ("got his fur in 1972, grey at first, and soon turned blue"), then translate again. The Spanish translation itself is faithful and natural.
- **q-4929** (the-sea) Mira esta sombra. ¿Qué animal marino es? → Una tortuga marina: Source: the description "A sea traveler that brings its house on every trip" (faithfully rendered as "se lleva la casa a cada viaje") names the shell, the sea turtle's defining trait. Against crab, stingray and octopus, it gives the answer away before any hint and repeats hint 2. The source description should play on the sea or travel theme without the carried house. The Spanish translation itself is faithful and natural.
- **q-6217** (countries) Una pizza italiana clásica tiene masa suave, queso derretido y una salsa roja. ¿De qué está hecha la salsa roja? → Tomates: Fact check: wrong. The fun fact is misleading: Italy had no tomato sauce before the 16th century is true, but the first Italian tomato sauce recipe dates to 1692 (Scappi, 1570s mention of tomatoes), so tomato sauce appeared well after the 16th century, not in it. Also the description says 'regalo redondo... para todas las fiestas de cumpleaños' which is vague, and the image query (Bay of Naples Vesuvius) doesn't match the question. Answer (tomatoes) and wrong answers are fine.
- **q-6258** (famous-logos) ¿Qué color NO es uno de los colores de los aros olímpicos? → Morado: The translation itself is faithful and reads naturally, but it asks the same fact as the approved q-6930 ("¿Cuál de estos colores NO aparece en los aros olímpicos?" → Morado). That is a duplicate in the Spanish pool, so you should drop one of the two, or decide that the two bundles are kept apart on purpose.

## Not travelling

None.

## Stale re-translated

None.
