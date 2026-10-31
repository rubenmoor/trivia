# tr-es-14

Made by `qgen batch --translate es` on 2026-10-30 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 641, about $38.27 at list price; $0.12 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-14&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-12 | tr-es-13 | tr-es-14 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 0 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 0 | 299 | 296 |
| needs_work |  | 0 | 1 | 4 |
| needs_work rate | ≤ 20.0 % | n/a | 0.3 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | n/a | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | n/a | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | n/a | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | n/a | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | n/a | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | n/a | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | n/a | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | n/a | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 0 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | n/a | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $17.46 | $24.71 | $34.72 |
| $ per approved |  | n/a | $0.08 | $0.12 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), media 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.55

Major findings on approved questions:

None.

## Needs work

- **q-3136** (wonders-of-the-world) El Cristo Redentor está en la cima del cerro del Corcovado, en Río de Janeiro. ¿Qué altura tiene aproximadamente ese cerro? → Unos 700 m: Fact check: wrong. The text facts are right. Corcovado is about 710 m, which is under 1 km, over 500 m and about twice the Eiffel Tower's 330 m. The statue is 30 m tall (plus an 8 m pedestal) and its arms span 28 m. The problem is the media query, 'Rio de Janeiro Sugarloaf Mountain'. Sugarloaf (Pão de Açúcar) is a different hill, about 396 m high, so the image would show the wrong mountain. I did not run web searches. These figures are well-established and I checked them from memory.
- **q-4153** (birds) Mira el enorme pico de este pelícano, con una bolsa elástica debajo. ¿Para qué sirve esa bolsa? → Para recoger peces: source: q-4153 asks the same fact as approved q-7612 (what the pelican's pouch under its beak is for, answer: catching fish), and the rater flagged this too. The translation itself is fine, but a Spanish-speaking family, in Colombia especially, could get both, so the developer should decide which one stays.
- **q-5297** (animal-records) Soy verde o café y vivo en los pastizales. Canto frotando las patas traseras contra las alas y salto unas 20 veces mi largo. ¿Quién soy? → Saltamontes: Overlap with approved q-7608 (colombia bundle): it is the same riddle with the same answer (green insect in the grass, long hind legs, huge jumps → saltamontes), so a Spanish player meeting both gets the answer from the other. The translation itself is faithful and natural. The overlap comes from the source's content, so the developer must decide whether to keep both, for example if the bundles never play together, or drop one.
- **q-5622** (natures-records) El canguro rojo es el canguro más grande de todos. ¿Más o menos qué distancia puede recorrer de un solo salto? → Alrededor de 8 m: source: the English hints carry the errors and the translation reproduces them faithfully. Hint 2 ("about as long as a bus") is off because a standard bus is 10–12 m, not 8 m. Hint 1 ("much farther than a person can jump") is false as worded, because the long jump world record is 8,95 m. Correct the source hints (e.g. "a small bus", and "farther than most people can jump"), then re-translate. Fact check: wrong. The answer of about 8 m is right: the red kangaroo's longest leaps are cited at 8–9 m. But hint 2 says that is about the length of a bus. A standard bus is 10–12 m, so the comparison is off. It also sits awkwardly beside hint 3, which uses two parked cars.

## Not travelling

None.

## Stale re-translated

None.
