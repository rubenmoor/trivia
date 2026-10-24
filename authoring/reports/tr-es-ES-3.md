# tr-es-ES-3

Made by `qgen batch --translate es-ES` on 2026-10-24 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 296
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 845, about $28.37 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-3&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-1 | tr-es-ES-2 | tr-es-ES-3 |
|---|---|---:|---:|---:|
| sources |  | 50 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 50 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 49 | 297 | 296 |
| needs_work |  | 1 | 3 | 4 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 1.0 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.0 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 74.0 % ✗ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $5.20 | $26.36 | $26.25 |
| $ per approved |  | $0.11 | $0.09 | $0.09 |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: media 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.12

Major findings on approved questions:

None.

## Needs work

- **q-1254** (childrens-songs) Se hace con las dos manos, hace ruido y la canción «Si estás feliz y lo sabes» te pide hacerlo. ¿Qué es? → Aplaudir: source: the fun fact says the song is "originally in English", but its origin is disputed. The melody is often linked to the Soviet song «Molodezhnaya» (1938) or to Latvian folk music, so the claim can't be confirmed. The source's fun fact should say something like "it is best known in English as «If You're Happy and You Know It», and its exact origin is disputed". The translation itself is faithful and natural for Spain. Fact check: uncertain. The answer "Aplaudir" is right, and the wrong answers and hints are fine. The fun fact is shaky. The song's origin is disputed. Some sources link the melody to the Soviet song "Molodezhnaya" (1938), others to Latvian folk music. The first recorded English version dates from 1957. Saying it is "originally in English" can't be verified.
- **q-2407** (disney-films) EVA es una robot blanca que viene del espacio para buscar una planta en la Tierra. En inglés se llama EVE, unas siglas. ¿Qué significan? → Evaluadora de Vegetación Extraterrestre: The answer and two of the wrong answers are Spanish phrases with the initials E-V-E. «Ingeniera de Aldeas Terrestres» has the initials I-A-T, so it doesn't match the acronym and players can rule it out straight away. Replace it with a feminine E-V-E phrase in the same style, for example «Exploradora de Valles Escondidos».
- **q-3299** (earthquakes) Soy una ciudad de colinas junto a una bahía, con famosos tranvías de cable. En 1906 un terremoto rompió mis tuberías de gas y hubo incendios durante días. ¿Qué ciudad soy? → San Francisco: source: the description («una semana de 1906 en la que hizo muchísimo calor» / "one very hot week in 1906") is a joke about the deadly 1906 fires, which breaks the tone rule. Read literally it also states a false heat wave, and the fact check marked it wrong. The source description should be rewritten, for example «Una ciudad famosa por sus cuestas, su niebla y un susto enorme en 1906», and the translation then follows it. The translation is otherwise faithful and natural es-ES. Fact check: wrong. The description says 1906 had a week of very high heat. That is false: the April 18, 1906 earthquake and fires happened in spring, and there was no notable heat wave. The rest (San Francisco, gas-main fires, water mains broken, Golden Gate built in the 1930s) is correct. The bridge is 'International Orange', so 'rojo' is loose.
- **q-4658** (architectural-styles) El Salón de Embajadores de la Alhambra guarda una famosa obra de arte hecha con más de 8000 piezas de madera de cedro. ¿En qué parte de la sala está? → Arriba, en el techo: Source: the media file 'Toit salle Abencerrages Alhambra Espagne.jpg' is a photo of an Alhambra ceiling (the muqarnas dome of the Sala de los Abencerrajes). It is shown sharp as an illustrative image and points straight to the answer 'Arriba, en el techo'. Replace it in the source with an Alhambra exterior or courtyard view that shows no ceiling. The Spanish text itself is faithful and natural.

## Not travelling

None.

## Stale re-translated

None.
