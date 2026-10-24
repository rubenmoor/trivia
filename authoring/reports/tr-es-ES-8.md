# tr-es-ES-8

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 826, about $31.05 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-8&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-6 | tr-es-ES-7 | tr-es-ES-8 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 300 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 297 | 298 |
| needs_work |  | 2 | 2 | 2 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 100.0 % ✓ | 100.0 % ✓ |
| cost $ |  | $27.00 | $27.87 | $28.53 |
| $ per approved |  | $0.09 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.52

Major findings on approved questions:

None.

## Needs work

- **q-1904** (cold-war) Suiza construyó refugios antinucleares desde la Guerra Fría. ¿Para qué parte de su población alcanzan hoy? → Cerca del 110 %: Source: the 110 % figure is outdated. It goes back to around 2006, when it was about 114 %. Current Swiss figures give roughly 8.6–9 million places for about 9 million residents, so coverage is about 96–100 %. That makes hint 3 («sobrarían plazas») doubtful too. The source needs rewording first: either make the answer «Cerca del 100 %» and drop hint 3, or date the fact explicitly (e.g. «a principios de este siglo»). The es-ES translation itself is faithful and idiomatic. Fact check: wrong. The "110 %" answer is outdated. The 114 % figure comes from 2006. Current Swiss figures are more than 8.6 million places for about 8.9 million residents, or about 96 %. So the hint "sobrarían plazas" is also false today, and "Cerca del 75 %" is not the nearest option either.
- **q-3121** (weather-and-climate) El explorador Douglas Mawson lo llamó «el hogar de la ventisca». Además, tiene el récord de la temperatura más baja jamás medida. ¿Dónde está? → La Antártida: Fact check: wrong. The answer (Antarctica) and the wrong answers are fine. Mawson's "The Home of the Blizzard" and the record low (-89.2 °C at Vostok) are true. The fun fact's figure is off: the mean wind at Cape Denison during Mawson's expedition was about 71 km/h (19.3 m/s, about 44 mph), not about 80 km/h.

## Not travelling

None.

## Stale re-translated

None.
