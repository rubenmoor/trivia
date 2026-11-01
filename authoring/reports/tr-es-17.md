# tr-es-17

Made by `qgen batch --translate es` on 2026-10-31 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 281 (0 stale re-translated)
- Translated: 281
- Approved: 266
- Needs work: 15
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 497, about $36.36 at list price; $0.12 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-17&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-15 | tr-es-16 | tr-es-17 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 281 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 281 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 292 | 290 | 266 |
| needs_work |  | 8 | 10 | 15 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | 3.3 % ✓ | 5.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.7 % ✓ | 3.2 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✓ | 1.7 % ✗ | 1.8 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $33.43 | $33.73 | $32.13 |
| $ per approved |  | $0.11 | $0.12 | $0.12 |
| **health** | | ✓ pass | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 57 (0 %)
- Major among review needs work: 2 of 3 (67 %)
- Problems by kind: giveaway 3 (0 major), fact 1 (0 major), overlap 2 (2 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.23

Major findings on approved questions:

None.

## Needs work

- **q-2257** (basketball) Este jugador pasó sus 20 años de carrera en la NBA con los Lakers de Los Ángeles. ¿Quién es? → Kobe Bryant: source: the fun fact is outdated in both the source and the translation. Bam Adebayo scored 83 points in March 2026, so Kobe's 81 is now the third-highest total in NBA history, not the second. Change the source to something like 'the most in a game since 1962 until 2026', or drop the ranking, then retranslate.
- **q-2638** (nobel-prizes) Este palacio fue la residencia de invierno de alguien que ganó el Nobel de la Paz en 1989. ¿De quién? → El dalái lama: source: hint 1 ("The palace stands high in the Himalayas") is geographically wrong, and the translation faithfully repeats it. The Potala Palace is in Lhasa, on the Tibetan Plateau north of the Himalaya range. The source hint should say something like "stands high on a vast plateau in Asia", and the translation should follow.
- **q-2679** (retro-games) En los juegos de Super Mario, ¿qué pasa cuando Mario agarra un hongo rojo con puntos blancos como este? → Se hace más grande: Duplicate: q-2903 (draft, "¿qué le hace a Mario un hongo muy parecido a este?" → "Lo hace más grande") asks the same fact with the same mushroom photo idea. Only one of the two should stay in the pool; the translation itself is otherwise fine. Source: the overlap comes from the source questions, not from the translation.
- **q-2903** (video-games) En los juegos de Super Mario, ¿qué le hace a Mario un hongo muy parecido a este? → Lo hace más grande: Exact overlap with q-2679 (draft, es): both ask what the red spotted mushroom does to Mario, with the same answer and the same photo idea. The Spanish text itself is fine; keep only one of the two, so if q-2679 goes ahead, this one should be dropped.
- **q-3373** (famous-scandals) Somos una banda británica de rock. En 1982, unos predicadores dijeron que nuestra canción más famosa escondía mensajes secretos si se tocaba al revés. ¿Quiénes somos? → Led Zeppelin: source: the fun fact's claim that the band laughed it off is not accurate. Robert Plant publicly called the accusation "saddening", and only the label's "turntables play in one direction" line was a joke. The English source needs correcting (e.g. "Their record label joked that its turntables only played in one direction"), and the Spanish should then follow. The translation itself is faithful and natural.
- **q-4078** (world-war-ii) Encerrado en una celda tras un golpe fallido en Múnich, Adolf Hitler empezó a escribir “Mi lucha”. ¿En qué año? → 1924: source: the fun fact that Hitler dictated much of the book to Rudolf Hess is a tradition that research contradicts. Plöckinger and the 2016 critical edition by the Institut für Zeitgeschichte show that Hitler typed the drafts himself, and Hess was at most a helper. Correct the fun fact in the source (e.g. drop the dictation claim, or say that Hess was jailed in the same prison), then re-translate. The translation itself is faithful and natural.
- **q-4079** (world-war-ii) Cuando la guerra impidió que el jarabe de Coca-Cola llegara a Alemania, allí se inventó un nuevo refresco de naranja, Fanta. ¿En qué década? → La década de 1940: source: the question calls wartime German Fanta "a new orange soda", but the 1940 drink was made from whey, apple pomace and other leftovers. Orange Fanta came from Italy in 1955. The decade (1940s) is right, and the Spanish faithfully repeats the source's error, so the source needs correcting (for example, drop "orange").
- **q-4153** (birds) Mira el pico enorme de este pelícano, con una bolsa elástica debajo. ¿Para qué sirve esa bolsa? → Para atrapar peces: This duplicates approved q-7612 (Colombia bundle): same pelican, same question about what the pouch under the beak is for, and the same answer, "Para atrapar peces". Players with both bundles would get the same fact twice, so one should be dropped; the translation itself is fine.
- **q-5297** (animal-records) Soy verde o marrón y vivo en campos de hierba. Canto frotando las patas traseras contra las alas y salto unas 20 veces mi longitud. ¿Quién soy? → Saltamontes: Overlap: q-7608 (approved, 'Animales de Colombia') is the same riddle with the same answer: a green insect in the grass, long back legs, huge jumps, saltamontes. Spanish players could meet both, and one gives the other away. The developer should drop one of the two; q-7608, as the later question, is the natural one to drop. The translation itself is fine.
- **q-5997** (solar-system) La OSIRIS-REx de la NASA tocó el asteroide Bennu en 2020, su brazo se hundió más de lo esperado y en 2023 trajo polvo a casa. ¿Qué es Bennu? → Un montón suelto de escombros: source: the description says NASA travelled ("went") 300 million km, but that is only roughly Bennu's distance from Earth. OSIRIS-REx flew about 6200 million km in total, so the source's number is wrong as a travel distance. The translation copies it faithfully. Correct the English source, e.g. drop the number ("NASA crossed the solar system for a handful of dirt and was thrilled with it"), then re-translate that line.
- **q-6009** (stars-and-galaxies) Este número indica qué tan rápido se expande el universo, en kilómetros por segundo por megapársec. Distintos métodos dan valores distintos, un enigma llamado “tensión”. ¿Cómo se llama? → La constante de Hubble: source: the fun fact says the constant was first measured in 1929, but Lemaître had already derived a value in 1927 (about 600 km/s/Mpc), as the rater noted. The source should drop the 'first' or the date (e.g. 'Hubble's 1929 value came out about seven times too big'), then the translation should follow. The Spanish question also runs to about 185 characters, against about 165 in the source, so it should be tightened at the same time.
- **q-6030** (the-lord-of-the-rings) Mi padre se fue de aventura con Bilbo. Me hago el mejor amigo de un elfo, y la Dama del Bosque de Oro me regala tres cabellos suyos. ¿Quién soy? → Gimli: Regional/translationese wording: "Me hago el mejor amigo de un elfo" reads as "I pretend to be an elf's best friend", because "hacerse el + X" means "to pretend" in Spanish. It should read "Me vuelvo el mejor amigo de un elfo" or "Me hice el gran amigo…" is not an option; use "Me vuelvo".
- **q-6258** (famous-logos) ¿Qué color NO es uno de los colores de los anillos olímpicos? → Morado: Source: this asks the same fact with the same answer as approved q-6930 ("¿Cuál de estos colores NO aparece en los aros olímpicos?" → Morado), so one of the two should be dropped. The translation itself is fine; the duplicate comes from the source question, not the wording.
- **q-6535** (rock) ¿Qué estrella del gospel de los años 40, que tocaba fuerte la guitarra eléctrica e inspiró a Elvis y Chuck Berry, es llamada la “madrina del rock and roll”? → Sister Rosetta Tharpe: source: hint 1 says she grew up in Arkansas, but Tharpe was only born there (Cotton Plant, 1915) and moved to Chicago with her mother at about age six. The English source needs correcting (e.g. "She was born in Arkansas..."), and the Spanish "Se crio en Arkansas" should then follow as "Nació en Arkansas...".
- **q-6618** (cold-war) Una invasión de EE. UU. lanzada en diciembre de 1989 sacó del poder a Manuel Noriega en el país que se ve aquí. ¿Qué país es? → Panamá: source: the fun fact is wrong in the English source and the translation copies it. The US troops' loud rock music at the Vatican nunciature was stopped days before Noriega surrendered on 3 January 1990, after the Vatican complained, so "until he gave up" is false. Correct the source first, for example: "US troops blasted loud rock music outside the Vatican's embassy where Noriega hid, until the Vatican complained." Then carry the change into the translation.

## Not travelling

None.

## Stale re-translated

None.
