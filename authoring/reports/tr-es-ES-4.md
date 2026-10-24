# tr-es-ES-4

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 295
- Needs work: 4
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 841, about $29.05 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-4&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-2 | tr-es-ES-3 | tr-es-ES-4 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 297 | 296 | 295 |
| needs_work |  | 3 | 4 | 4 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 1.3 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 0.7 % ✓ | 1.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $26.36 | $26.25 | $26.83 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), media 1 (0 major)
- Mean |audit − final difficulty|: 0.2; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.22

Major findings on approved questions:

None.

## Needs work

- **q-1089** (trains) ¿Qué tecnología usa el tren rapidísimo que une Shanghái con su aeropuerto? → Levitación magnética: source: the fun fact's «menos de 8 minutos» is out of date. That time held only at the old 431 km/h top speed. Since the top speed was cut to 300 km/h, the 30 km trip takes about 8 minutes or slightly more. Change the source to «en unos 8 minutos» (or «a más de 400 km/h llegaba a hacerlo en poco más de 7 minutos»), then translate again.
- **q-2533** (human-body) Los médicos y las enfermeras suelen llevar esto sobre la nariz y la boca. ¿Qué ayuda a frenar? → Gérmenes: Fact check: wrong. The question asks what a mask helps stop, but a surgical mask is mainly worn to block droplets and germs. The answer 'Gérmenes' is acceptable. The wrong answers are wrong. However, the description says it handles something 'muchísimo más pequeño', which fits. The fun fact (a sneeze launches thousands of droplets) is true. The problem is the axis 'lens: history' has no connection to the content, but that is not a factual error. I found no factual error, but I did not verify this by search.
- **q-3359** (famous-logos) Soy un círculo con líneas dentro, dibujado en Gran Bretaña en 1958. Mis líneas son la N y la D del semáforo de banderas. ¿Qué significan en inglés? → Desarme nuclear: The translated options don't fit the N-D clue. The question asks «¿Qué significan en inglés?» but all four options are in Spanish. The three wrong answers all start with N («Ninguna destrucción», «Nuevo amanecer», «Nunca desesperar»), while «Desarme nuclear» is the only option that reads D-N, so the correct answer stands out by its form. One fix is to give the options as the English phrases with a Spanish gloss, e.g. «Nuclear Disarmament (desarme nuclear)», with English N-D distractors. Another is to reword the question to ask which cause the letters stood for. Either way, all options should follow the same letter pattern.
- **q-4407** (human-body) Estos dientes puntiagudos están en las esquinas de la boca y tienen las raíces más largas de todos tus dientes. ¿Para qué sirven sobre todo? → Para sujetar y desgarrar la comida: Fact check: wrong. The fun fact is dubious. Canines are called 'eye teeth' in English, specifically the upper canines, because their roots sit below the eyes. The fun fact says their roots reach 'very close' to the area under the eyes, which is roughly acceptable. But the hint 'las esquinas de la boca' and 'cuatro' are fine. The wrong answer 'Para mantener los labios en su sitio' is arguably not clearly wrong, since canines do support the lip and facial contour at the corners of the mouth. Also, 'eye teeth' applies mainly to the upper canines, not all four. I did not verify this by search.

## Not travelling

- **q-1166** needs_local_knowledge, confirmed: ¿De qué personaje de televisión viene la frase «¡No contaban con mi astucia!»? → El Chapulín Colorado (Chespirito's El Chapulín Colorado and his catchphrase are Latin American pop culture. Few families in Spain know the show, and fewer still know the Chespirito side characters used as wrong options (Doctor Chapatín, Chómpiras).)

## Stale re-translated

None.
