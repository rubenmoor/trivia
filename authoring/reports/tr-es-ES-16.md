# tr-es-ES-16

Made by `qgen batch --translate es-ES` on 2026-10-29 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 795, about $32.90 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-16&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-14 | tr-es-ES-15 | tr-es-ES-16 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 296 | 296 |
| needs_work |  | 2 | 4 | 4 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 1.3 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.3 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $30.02 | $29.61 | $29.97 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 1 (0 major), overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.93

Major findings on approved questions:

None.

## Needs work

- **q-3136** (wonders-of-the-world) El Cristo Redentor está en lo alto del monte Corcovado, en Río de Janeiro. ¿Qué altura tiene más o menos el monte? → Unos 700 m: Fact check: wrong. The facts are correct. Corcovado is about 704 m high, so 'Unos 700 m' is right and the wrong answers are clearly off. The hints hold up: it is under 1 km, over 500 m, and about twice the Eiffel Tower's 330 m. The statue is 30 m tall (without its 8 m pedestal) with a 28 m arm span. The one problem is the media query 'Rio de Janeiro Sugarloaf Mountain'. That is a different mountain (Pão de Açúcar, about 396 m), not Corcovado, so the image would mislead.
- **q-3968** (space-race-and-astronauts) ¿Cómo se llama la velocidad que necesita un objeto para dar vueltas a la Tierra, cayendo a su alrededor sin llegar nunca al suelo? → Velocidad orbital: Fact check: uncertain. The answer and the wrong answers are right. The ISS speed is about 27,600 km/h, so 'unos 28 000' is fine. The fun fact is loose, though. At about 7.66 km/s, a 5,500 km Atlantic crossing (New York–London) takes about 12 minutes, not 15. The narrowest crossing takes far less. I did not run a search; this comes from known figures.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: Source: the fun fact is wrong. Marx's tomb at Highgate has a large bronze bust (Laurence Bradshaw, 1956) on a granite plinth, not a stone head. The Spanish «enorme cabeza de piedra» repeats the source's mistake. Fix the source's fun fact (e.g. "huge bronze bust") and then re-translate it as «su enorme busto de bronce». Fact check: wrong. The answer (Karl Marx) and the wrong answers are fine. The hints are fine too: Marx is German, lived in London from 1849 and died there, and 'Marx' has four letters. The fun fact is inaccurate. The big head on Marx's tomb at Highgate is a bronze bust (by Laurence Bradshaw, 1956) on a granite plinth, not a stone head.
- **q-6627** (drinks) Además de leche, ¿qué se mezcla en la batidora para hacer un batido de heladería, el famoso «milkshake»? → Helado: The question text says «batido de heladería», and «heladería» contains the answer «Helado», so the question gives the answer away. Name the milkshake another way without that word, e.g. «el batido espeso tipo "milkshake"» or «un milkshake de cafetería».

## Not travelling

None.

## Stale re-translated

None.
