# tr-es-ES-11

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 819, about $32.43 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-11&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-9 | tr-es-ES-10 | tr-es-ES-11 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 297 | 298 | 297 |
| needs_work |  | 3 | 2 | 3 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $29.07 | $28.80 | $29.50 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: style 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.93

Major findings on approved questions:

None.

## Needs work

- **q-4345** (farm-animals) En el cuento de 1936 sobre el toro Ferdinando, al pacífico toro le encanta sentarse bajo un árbol con una corteza como esta. ¿Qué árbol? → Alcornoque: The fun fact uses the Latin American title «Ferdinand». In Spain the 2017 film came out as «Olé, el viaje de Ferdinand», so the fun fact should use that title. The rater's note has the two titles the wrong way round, and the translator's note had them right. The rest of the translation is faithful and the kept cork-oak bark image fits.
- **q-4539** (prehistory) Una cerilla es a una cocina de gas lo que frotar dos palos secos es a… → Una hoguera: Fact check: wrong. The analogy is logically weak. A match lights a gas stove, so the match is the fire-starting tool and the stove is what gets lit. Rubbing two sticks is the fire-starting tool and a campfire is what gets lit, so "hoguera" does fit. But the question wording says a match is to a stove as sticks are to the answer, which makes it ambiguous. The fun fact is also misleading: the bow drill spins a spindle with a bow string, which makes an ember (hot dust) faster than a hand drill. "Con las manos" is loosely right, but the fact doesn't say it is the "taladro de mano". Hint 2 says the sticks "se calientan muchísimo", which is fine. Hint 3 gives away the answer and describes a campfire's effects, not the tool. The wrong answers (lanza, vasija, hacha) are clearly wrong.
- **q-5458** (famous-philosophers) Este pensador alemán barbudo dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact calls the head on Marx's Highgate tomb a stone head ("stone head" / "cabeza de piedra"), but it is a bronze bust by Laurence Bradshaw (1956) on a granite base. Correct the source to "bronze bust" (Spanish: "busto de bronce"), then re-translate. Fact check: wrong. The answer (Karl Marx) and the wrong answers are fine, and so are the hints. The fun fact is inaccurate. The big head on Marx's tomb in Highgate Cemetery is a bronze bust by Laurence Bradshaw (1956) on a granite plinth. It is not a 'cabeza de piedra'. This is from memory and was not checked with a search.

## Not travelling

None.

## Stale re-translated

None.
