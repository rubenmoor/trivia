# tr-es-ES-15

Made by `qgen batch --translate es-ES` on 2026-10-29 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 797, about $32.31 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-15&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-13 | tr-es-ES-14 | tr-es-ES-15 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 296 | 298 | 296 |
| needs_work |  | 3 | 2 | 4 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 0.7 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.7 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $29.05 | $30.02 | $29.61 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), fact 1 (0 major), overlap 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.70

Major findings on approved questions:

None.

## Needs work

- **q-0137** (dinosaurs) Mira este esqueleto: ¿qué dinosaurio es? → Estegosaurio: source: the description gives the stegosaurus 'a club on its tail' («garrote»/«porra en la cola»), but stegosaurus had tail spikes. A tail club is the ankylosaurus's trait, and ankylosaurus is one of the wrong options, so the description is factually wrong and points players to a distractor. The source's description should say something like 'pinchos en la cola' or play on the theme without the trait. The rest of the es-ES translation is faithful and idiomatic.
- **q-1952** (winter-olympics) ¿Cuándo se celebran los Juegos Paralímpicos de invierno, comparados con los Juegos Olímpicos de invierno? → Poco después, en la misma sede: source: Hint 2 («Nunca se celebran antes que los Juegos Olímpicos») is false. The 1980 Geilo and 1984 Innsbruck Winter Paralympics took place before that year's Winter Olympics, and at a different venue. The question also doesn't say it means today's rule (in place since 1992), so the source needs fixing. It should add «Hoy en día» or «Desde 1992» to the question and rewrite hint 2 so it no longer says «never», for example «Hoy en día, siempre empiezan cuando los Olímpicos ya han terminado».
- **q-4811** (extreme-sports) Vas en un telesilla subiendo la montaña. ¿A qué velocidad aproximada te lleva? → Unos 15 km/h: Fact check: uncertain. The answer depends on the lift type. I did not run searches. This is from general knowledge of lift specs. Fixed-grip chairlifts, which are still common, run about 1–2.5 m/s (4–9 km/h). Modern detachable chairlifts run about 4–6 m/s (15–22 km/h), so 15 km/h is only right for those. The question does not say which type. The wrong answers 60 and 150 km/h are clearly wrong. 2 km/h is too slow for almost any lift. The fun fact and hints 2 and 3 are broadly fine for detachable lifts. Hint 1 and the 'banco' description fit any type.
- **q-5561** (james-bond) Sean Connery es a «Agente 007 contra el Dr. No» lo que Barry Nelson es a… → Casino Royale: source: the fun fact says Bond's friend "Felix Leiter" was British in the 1954 Climax! episode. In that episode the British agent was renamed Clarence Leiter. The source fun fact should say the character became a British agent called Clarence Leiter, and then the translation should follow. Apart from this, the Spanish translation is faithful and natural, and it uses Spain's release titles.

## Not travelling

None.

## Stale re-translated

None.
