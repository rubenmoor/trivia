# tr-es-ES-7

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 297
- Needs work: 2
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 823, about $30.28 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-7&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-5 | tr-es-ES-6 | tr-es-ES-7 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 299 | 298 | 297 |
| needs_work |  | 1 | 2 | 2 |
| needs_work rate | ≤ 20.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 100.0 % ✓ | 100.0 % ✓ |
| cost $ |  | $27.11 | $27.00 | $27.87 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 3 (0 major), fact 1 (0 major), media 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.41

Major findings on approved questions:

None.

## Needs work

- **q-0660** (cartoons) ¿Qué tienen en común el zoótropo, el taumatropo y el praxinoscopio, inventos del siglo XIX? → Crean ilusión de movimiento: Fact check: wrong. The answer is inaccurate for the thaumatrope. It shows two images on opposite sides of a spinning disc that blend into one image (bird in cage), so it creates no illusion of motion. Zoetrope and praxinoscope do animate. What all three share is persistence of vision. Hint 2 (drawings changing one after another) is also false for the thaumatrope. The 'wheel of life' fun fact is fine. I did not run searches. This is from established knowledge.
- **q-4371** (fish) Si el gato tiene bigotes, ¿qué tiene el pez gato? → Barbillones: The translation drops the analogy. «Si el gato tiene bigotes, ¿qué tiene el pez gato?» literally asks what a catfish has, and it really does have fins and gills, so «Aletas» and «Branquias» become defensible answers. Reword it so the analogy is explicit, e.g. «Lo que los bigotes son para el gato, ¿qué son para el pez gato?».

## Not travelling

- **q-1017** about_language, confirmed: En España, el juego de sacar papelitos y dar un regalo sin revelar a quién te tocó no se llama 'amigo secreto'. ¿Cómo lo llaman allá? → Amigo invisible (The question asks what Spain calls the Secret Santa game ('amigo invisible'). For players in Spain that's their own everyday word, so the question becomes trivial. Flipping it to ask for the Latin American name would change the answer.)

## Stale re-translated

None.
