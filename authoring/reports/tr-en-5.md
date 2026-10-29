# tr-en-5

Made by `qgen batch --translate en` on 2026-10-29 (plan 66, D-81): `base` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 289
- Approved: 288
- Needs work: 1
- Not travelling: 11 (11 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 673, about $29.27 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-5&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-3 | tr-en-4 | tr-en-5 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 295 | 298 | 289 |
| not travelling |  | 5 | 2 | 11 |
| not travelling confirmed |  | 4 | 2 | 11 |
| rejected rate | ≤ 20.0 % | 1.3 % ✓ | 0.7 % ✓ | 3.7 % ✓ |
| approved |  | 292 | 292 | 288 |
| needs_work |  | 3 | 6 | 1 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 2.0 % ✓ | 0.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 1.7 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 96.7 % ✓ |
| cost $ |  | $27.75 | $23.62 | $26.46 |
| $ per approved |  | $0.10 | $0.08 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 60 (3 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 5 (1 major), overlap 2 (1 major), difficulty 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.80

Major findings on approved questions:

- **q-0369**: overlap — Overlap (in the source too): related q-0341 ("In which country was the Rubik's Cube invented?" → Hungary) asks the same fact, so the two shouldn't both be played. Otherwise the translation is faithful and correct: Spanish "43 trillones" is 43 quintillion (10^18, about 4.3×10^19), the 1974 invention by Ernő Rubik, a Budapest professor, is right, the hints are true and the wording is natural US English. (http://127.0.0.1:8001/review/q-0369)
- **q-2113**: giveaway — The source says the Chanel jacket "lo lleva" ("has it"), which still fits a gold button, a collar or pearl embroidery. The translation says the jacket "is made of it", and a jacket can't be made of a button, a collar or embroidery, so the question text rules out all three wrong answers. A fix: "The classic Chanel jacket has it, it was born in Scotland, and it feels a little scratchy. What is tweed?" I also checked the facts: tweed is a wool fabric from Scotland, and the fun fact (the "tweel" misread as the River Tweed) is the usual story. The River Tweed picture is fine, and so are the hints and the difficulty. (http://127.0.0.1:8001/review/q-2113)

## Needs work

- **q-0317** (knights) Look at the photo: what is this piece of a knight's armor called? → Helm: Fact check: uncertain. The answer (Helm) and the wrong answers (Breastplate, Gauntlet, Greave) are right. The hints are fine: the helm protects the head, it has narrow eye slits, and "Helm" is four letters starting with H. The fun fact is shaky. The sources I found put great helms at about 1.5–3 kg, with a 1375 Pembridge-type helm at 2.4–2.6 kg. They don't support 3–4 kg (7–9 lb) as typical. Only a different helm type, a c. 1460 kettle hat, weighed more (5.66 kg).

## Not travelling

- **q-1993** about_language, confirmed: En inglés, ¿qué significa 'axe', el nombre del famoso desodorante? → Hacha (Asks what the English word “axe” means. English speakers already know the word, so the question becomes trivial.)
- **q-0526** about_language, confirmed: Estás en Popayán en Semana Santa y ves pasar, cargados en hombros, el del Señor del Huerto, el de la Dolorosa y el del Santo Sepulcro. ¿Con qué palabra se nombran los tres? → Pasos (Asks for the Spanish word “pasos”. In English these are usually called “floats”, which is also the translation of the wrong answer “carrozas”. Hint 3 is a pun on “paso” = step. The question is also about a Colombian local tradition.)
- **q-0789** needs_local_knowledge, confirmed: En nuestro mundo, dos y dos son cuatro. En 'El reino del revés', la canción de María Elena Walsh, dos y dos son… → Tres (Asks about the lyrics of María Elena Walsh's Argentine children's song “El reino del revés”, known only in the Spanish-speaking world; the answer (three) can't be reasoned out without knowing the song.)
- **q-1251** needs_local_knowledge, confirmed: Estoy sentadita en mi verde limón; con el pico recojo la rama y con la rama, la flor. ¿Quién soy? → La pájara pinta (“La pájara pinta” is a Spanish-language children's ring song with no English equivalent; the lyric riddle and all options (Spanish children's songs) are unknown to English-speaking players.)
- **q-0934** about_language, confirmed: En las competencias de 'Red Bull Cliff Diving', los clavadistas se lanzan al mar desde plataformas de unos 27 metros. 'Cliff diving' significa 'clavados desde…' → Acantilados (The question asks what the English phrase 'cliff diving' means. In English the name itself gives the answer (cliffs), and rewording it would make it a different question.)
- **q-0976** wordplay, confirmed: Adivina: soy un anagrama de 'ROMA' y los poetas me escriben miles de versos. ¿Qué palabra soy? → Amor (Anagram of the Spanish word ROMA = AMOR (love). In English, Rome/Roma doesn't rearrange into 'love' or into any word poets write about, and the hints and fun fact also depend on the Spanish letters.)
- **q-0794** needs_local_knowledge, confirmed: Completa: García Márquez es a 'Cien años de soledad' como Héctor Abad Faciolince es a… → El olvido que seremos (Héctor Abad Faciolince's memoir (published in English as 'Oblivion: A Memoir') and all three wrong answers (La vorágine, Rosario Tijeras, Delirio) are Colombian literature that is little known outside Colombia. In English the options would be unfamiliar or translated titles, and families couldn't reason their way to the answer.)
- **q-1806** about_language, confirmed: El reality 'The Great British Bake Off' lleva el verbo inglés 'bake'. ¿Qué tienen que hacer sus concursantes? → Hornear (The question asks what the English word “bake” in the show's title means. For English speakers the title states the answer, so no fair version is possible.)
- **q-2062** needs_local_knowledge, confirmed: ¿Cuál de estas canciones NO es de la banda mexicana Molotov? → Matador (Asks which song isn't by Mexican band Molotov (vs. Los Fabulosos Cadillacs). It needs Latin American rock knowledge most English-speaking players don't have, and they have nothing to reason from.)
- **q-2197** about_language, confirmed: Completa: 'La cajita donde guardas tus collares y la persona que los fabrica se llaman igual: el ___'. → Joyero (The question depends on the Spanish word “joyero” meaning both “jewelry box” and “jeweler”. English uses two different words, so the question can't be rebuilt.)
- **q-2175** needs_local_knowledge, confirmed: Fue la primera telenovela de Belinda, se estrenó en el año 2000 y era infantil, de Televisa. ¿Cuál es? → Amigos x siempre (Asks to identify a Mexican children's telenovela by its Spanish title (Belinda's debut). It has no English title and English-speaking families would almost never know it. Hint 3 also depends on Spanish (“x” standing for “por”).)

## Stale re-translated

None.
