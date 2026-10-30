# tr-es-ES-19

Made by `qgen batch --translate es-ES` on 2026-10-30 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 820, about $41.81 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-19&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-17 | tr-es-ES-18 | tr-es-ES-19 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 296 | 294 | 295 |
| needs_work |  | 4 | 6 | 5 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 2.0 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 2.0 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $30.07 | $31.81 | $38.30 |
| $ per approved |  | $0.10 | $0.11 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 4 (0 major), fact 1 (0 major), style 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.52

Major findings on approved questions:

None.

## Needs work

- **q-0226** (body-oddities) Más o menos, ¿cuánta sangre tiene el cuerpo de una persona adulta? → Unos 5 litros: source: the fun fact states as true that a person's blood vessels would circle the Earth more than twice. That rests on the old 100 000 km figure, which is disputed: recent re-estimates are far lower, around 9000–19 000 km, or less than half a lap. The fact check confirmed it from memory only. The source fun fact needs replacing with a safe fact, for example that red blood cells cross the body in about a minute or live about four months, and the translation then follows.
- **q-1398** (famous-companies) La Guía Michelin, la de las estrellas para restaurantes, la creó una fábrica de neumáticos. ¿De qué país? → Francia: source: hint 3 says the founding brothers «eran de Clermont-Ferrand», but André and Édouard Michelin were both born in Paris. Clermont-Ferrand is where the company and its factory are based, so the hint should read e.g. «La fábrica estaba en Clermont-Ferrand». The source and the translation share this error, so the source needs correcting.
- **q-1530** (harry-potter) ¿Cómo se llama el juego mágico parecido a las canicas en el que las piedras le escupen un líquido apestoso al que pierde un punto? → Gobstones: source: both hints come from the source, not the translation. Hint 1 ("Harry ve a otros alumnos jugarlo en Hogwarts") is unconfirmed by the fact check and I can't confirm it either. Hint 2 says Eileen Prince captained the "club", but in the book she was captain of the Hogwarts Gobstones team. Correct the source, e.g. hint 1 about Percy Weasley's Gobstones set and "equipo" in hint 2, then carry that into the es-ES text. Fact check: uncertain. The answer (Gobstones), the wrong answers, the marble-like squirting-stones description, the Eileen Prince detail and the stone/gold fun fact all check out. I couldn't verify hint 1, that Harry sees other students playing it at Hogwarts. The sources only mention a Gobstones Club (OotP) and Percy's set in Gryffindor (PA). Eileen Prince was captain of the Gobstones team (HBP), not a 'club'.
- **q-3464** (international-football) ¿Qué club ha ganado más veces que ningún otro la máxima competición europea, la Copa de Europa o Champions League? → Real Madrid: source: the media file is "Real Madrid celebration after winning the 2018 UEFA Champions League Final", an illustrative image shown sharp. Going by the title, it shows the answer's team with the trophy and gives the answer away in every language. The source slot needs a new file, for example the trophy alone or a neutral European stadium. The Spanish text itself is fine.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact is wrong in both the English source and this translation. The monument at Highgate is a bronze bust by Laurence Bradshaw (1956) on a granite plinth, not a 'stone head'. Correct the source to 'huge bronze bust' and the Spanish to 'enorme busto de bronce'. Fact check: wrong. The fun fact says the monument at Highgate is a huge 'stone head'. It is a bronze bust (by Laurence Bradshaw, 1956) on a large granite plinth. The rest of the question checks out.

## Not travelling

None.

## Stale re-translated

None.
