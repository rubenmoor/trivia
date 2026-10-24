# tr-es-4

Made by `qgen batch --translate es` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 298
- Needs work: 2
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 679, about $30.66 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-4&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-2 | tr-es-3 | tr-es-4 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 296 | 298 | 298 |
| needs_work |  | 4 | 2 | 2 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $26.22 | $28.36 | $27.96 |
| $ per approved |  | $0.09 | $0.10 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 60 (2 %)
- Major among review needs work: 0 of 0
- Problems by kind: media 1 (1 major), style 4 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.70

Major findings on approved questions:

- **q-4756**: media — The translation is accurate and natural, and the facts check out: llama, vicuña and camel are all camelids, sheep are bovids, camelids walk on two padded toes, and vicuña wool is among the most expensive. The problem is the illustrative image from the source, "File:Sillustani flocks of sheeps in Péru(1).jpg". It shows sheep, which is the answer, and that breaks the rule that illustrative media must not show the answer (source-level: it needs an Andean image without sheep, like Inca ruins or alpacas). (http://127.0.0.1:8001/review/q-4756)

## Needs work

- **q-4568** (retro-games) Estás jugando un videojuego de carreras. ¿Qué de esto NO vas a encontrar en él? → Un portero: Fact check: wrong. The answer 'Un portero' is arguably fine, but the wrong answers include 'Una línea de meta' and 'Una pista de carreras' which are fine; however 'meta' (goal) is also a football term, and 'portero' hint is ok. Main issue: the item is ambiguous because 'línea de meta' also exists in football/soccer, and some racing games (e.g. Rocket League-style car-soccer games) do have goalkeepers. The question also says 'garaje' in the description though options are not garage items.
- **q-6258** (famous-logos) ¿Qué color NO es uno de los colores de los anillos olímpicos? → Morado: This asks the same fact as the approved q-6930 (colombia bundle: "¿Cuál de estos colores NO aparece en los aros olímpicos?", answer "Morado"). Colombian families who play both base and colombia would get the same question twice. The translation is fine. Keep one of the two questions, or replace q-6930 in the colombia bundle with a different Olympic question.

## Not travelling

None.

## Stale re-translated

None.
