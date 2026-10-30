# tr-es-ES-22

Made by `qgen batch --translate es-ES` on 2026-10-30 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 291
- Needs work: 9
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 639, about $41.51 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-22&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-20 | tr-es-ES-21 | tr-es-ES-22 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 300 |
| not travelling |  | 0 | 1 | 0 |
| not travelling confirmed |  | 0 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 291 | 288 | 291 |
| needs_work |  | 9 | 11 | 9 |
| needs_work rate | ≤ 20.0 % | 3.0 % ✓ | 3.7 % ✓ | 3.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.7 % ✓ | 3.3 % ✓ | 3.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 95.0 % ✓ | 95.0 % ✓ |
| cost $ |  | $36.31 | $38.60 | $37.33 |
| $ per approved |  | $0.12 | $0.13 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 1 (0 major), fact 2 (1 major), media 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.18

Major findings on approved questions:

- **q-6367**: fact — source: the fun fact is false as worded and the translation keeps it. Marie Curie won the 1911 Chemistry Nobel alone (as hint 1 nearly reminds players), and Hodgkin (1964) and McClintock (1983) also won science Nobels alone. The true claim is that it was the first science Nobel shared by a team made up only of women. The answer 5 is right (Curie, Joliot-Curie, Hodgkin, Yonath, Arnold), and the translation is faithful and natural in es-ES. (http://127.0.0.1:8001/review/q-6367)

## Needs work

- **q-0748** (greek-heroes) En la mitología romana: Zeus es a Júpiter como Hades es a… → Plutón: source: hint 1 is false. It says the Romans called a planet by this name, but Pluto was discovered in 1930 and only then named after the god. The Spanish translation copies this faithfully, so the source needs correcting, e.g. "Un astro descubierto en 1930 lleva el nombre de este dios romano." Hint 2 ("planeta enano") may also be too strong next to the options, so check it in the same pass. Fact check: wrong. The answer (Plutón) and the wrong answers (Neptuno, Marte, Vulcano) are correct. The fun fact is correct: Venetia Burney was 11 and proposed the name in 1930. The Mickey Mouse dog hint is fine. Hint 1 is false: the Romans did not call a planet Plutón. They didn't know of it, and it was discovered in 1930 and named after the god.
- **q-2307** (capital-cities) Los perros como este protagonizan una película de Disney ambientada en Londres, con 101 cachorros con manchas. ¿De qué raza son? → Dálmata: source: "101 spotted puppies" is factually wrong, and the translation repeats it as «101 cachorros con manchas». In the Disney film there are 99 puppies; the 101 Dalmatians include the parents, Pongo and Perdita. The source should say something like "101 spotted dogs", and the translation should then follow it («101 perros con manchas»).
- **q-3019** (solar-system) ¿En qué año se lanzó al espacio el telescopio espacial James Webb? → 2021: source: hint 2 is inaccurate in the English source and faithfully translated. "Not long after the COVID-19 pandemic began" doesn't fit, as the pandemic began in early 2020 and Webb launched on 25 December 2021, almost two years later. Correct the source hint, e.g. "It launched when the COVID-19 pandemic had been going on for almost two years", then retranslate it. Fact check: wrong. La respuesta (2021; lanzamiento el 25 de diciembre de 2021) y las respuestas incorrectas son correctas. El espejo de 6,5 m, con baño de oro y plegable, también es cierto. Pero la pista 2 es engañosa: la pandemia empezó en marzo de 2020 y el lanzamiento fue casi 2 años después, así que no fue 'poco después'. Es de memoria, sin búsqueda web.
- **q-3136** (wonders-of-the-world) El Cristo Redentor se alza en lo alto del Corcovado, una montaña de Río de Janeiro. ¿Cuánto mide aproximadamente la montaña? → Unos 700 m: Fact check: wrong. Text facts are right (Corcovado ~710 m, statue 30 m, arms 28 m), but the media query 'Rio de Janeiro Sugarloaf Mountain' shows a different mountain (Pão de Açúcar), not Corcovado/Cristo Redentor.
- **q-3930** (science-fiction) En «Gru, mi villano favorito», Gru roba la Luna. ¿Qué artilugio usa para hacerlo? → Rayo reductor: source: hint 2 is factually wrong in the English source, and the translation repeats it faithfully. In the film, Gru's team steals the shrink ray from the secret lab, and Vector then takes it from Gru; Vector did not steal it from the lab first. Correct the source hint (e.g. "Gru's team first took it from a secret lab, but Vector snatched it from them"), then carry that change over to the translation.
- **q-5286** (amazon-history-and-exploration) En «Fitzcarraldo», de Werner Herzog, un enorme barco fluvial como este fue arrastrado de verdad por una colina. ¿En qué país se rodó esa escena? → Perú: source: hint 1 says the story starts in a rubber-boom city with no road access, which means Iquitos, but the film opens at the Manaus opera house in Brazil, so the hint is inaccurate and points towards a wrong option. Change it in the source (e.g. the hero lives in a rubber-boom city with no road access), then carry it into the translation. The translation itself is faithful and natural.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: source: the fun fact is wrong. The head on Marx's Highgate tomb is bronze on a stone (marble) plinth, not stone. The translation copies this faithfully as «enorme cabeza de piedra». Correct the source (e.g. "huge bronze head"), then carry the change into the translation («enorme cabeza de bronce»).
- **q-6457** (harry-potter) En el Expreso de Hogwarts, en su sexto curso, alguien dice «Episkeyo» y Harry nota la nariz muy caliente y luego muy fría. ¿Qué hace el hechizo? → Cura heridas pequeñas: Fact check: wrong. The spell is spelled "Episkey" in the books, not "Episkeyo". The rest of the facts are correct.
- **q-6618** (cold-war) Una invasión de Estados Unidos en diciembre de 1989 sacó del poder a Manuel Noriega en el país que ves aquí. ¿Qué país es? → Panamá: source: the fun fact says US troops blasted rock music until Noriega gave up, but the music stopped after the Vatican complained, days before his surrender on 3 January 1990. The source should change to something like "blasted loud rock music outside for days", and the Spanish should then follow it.

## Not travelling

None.

## Stale re-translated

None.
