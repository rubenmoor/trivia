# tr-es-3

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 697, about $31.11 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-3&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-1 | tr-es-2 | tr-es-3 |
|---|---|---:|---:|---:|
| sources |  | 50 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 50 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 50 | 296 | 298 |
| needs_work |  | 0 | 4 | 2 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 1.3 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 1.0 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.0 % ✓ | 98.3 % ✓ | 100.0 % ✓ |
| cost $ |  | $5.62 | $26.22 | $28.36 |
| $ per approved |  | $0.11 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 60 (0 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 1 (0 major), media 2 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.76

Major findings on approved questions:

None.

## Needs work

- **q-4568** (retro-games) Estás jugando un videojuego de carreras. ¿Qué de esto NO vas a encontrar en él? → Un portero de fútbol: Fact check: wrong. The question is ambiguous and the answer isn't reliably true. A goalkeeper does not appear in racing games, but the wrong answers include a 'volante' (steering wheel), which many racing games show in cockpit view. The hint 'Tres de ellas tienen que ver con autos que van muy rápido' is loose. The fun fact is true, since plastic wheels that clip onto controllers exist (e.g., Wii Wheel). Another issue is that the description says 'garaje' and the image query is 'go kart race'. The odd-one-out question is also not strictly checkable, because some racing games, such as soccer-car games like Rocket League, do have goalkeepers.
- **q-6044** (trees) ¿Cómo se llama un grupo pequeño de árboles como este, más pequeño que un bosque? → Arboleda: Hint 3 mixes number: it says 'Son más que unos pocos árboles' (plural) but then 'puedes rodearla' (feminine singular). That's ungrammatical, and the feminine 'la' also rules out 'Seto'. Suggested wording: 'Tiene más que unos pocos árboles, pero puedes darle la vuelta caminando en unos minutos.' Optionally, make hint 1 singular too: 'Se encuentra en parques y en granjas de todo el mundo.'

## Not travelling

None.

## Stale re-translated

None.
