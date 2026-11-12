# tr-en-18

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `spain` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 292
- Needs work: 7
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 530, about $25.61 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-18&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-16 | tr-en-17 | tr-en-18 |
|---|---|---:|---:|---:|
| sources |  | 5 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 5 | 299 | 299 |
| not travelling |  | 0 | 1 | 1 |
| not travelling confirmed |  | 0 | 1 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| approved |  | 0 | 294 | 292 |
| needs_work |  | 5 | 5 | 7 |
| needs_work rate | ≤ 20.0 % | 100.0 % ✗ | 1.7 % ✓ | 2.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 100.0 % ✗ | 1.3 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 5 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 20.0 % ✗ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $1.46 | $23.22 | $23.21 |
| $ per approved |  | n/a | $0.08 | $0.08 |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), fact 1 (0 major), media 3 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.40

Major findings on approved questions:

None.

## Needs work

- **q-13339** (regional-symbols) I'm shaped like an X and I fly white on blue on the flag of Tenerife. What am I? → The Cross of Saint Andrew: This overlaps heavily with q-9607 ("Scotland's flag, the Saltire, is a white diagonal cross on a blue background. Whose cross is it?" → Saint Andrew). Both ask which cross is a white X on blue, so seeing one gives away the other. In English, hint 1 also gives it away: "saltire" is the everyday English name for Scotland's flag, which points straight to Saint Andrew. Dropping Scotland from the question text helps, but the core fact is still the same. Either keep this item out of the English pool or move the question to a Tenerife-only fact, and in hint 1 use a neutral word such as "diagonal cross" instead of "saltire".
- **q-14306** (protected-areas) In a lagoon in Doñana you see a black bird with a white plate on its forehead and, above it, two small red bumps in breeding season. What bird is it? → The crested coot: Source: the fun fact is wrong. The crested (red-knobbed) coot lives mainly in eastern and southern Africa. Morocco and southern Spain are only the northern edge of its range. The translation copies this error faithfully, so the source needs correcting first. Apart from that, the translation is faithful and reads naturally.
- **q-14431** (spanish-cinema) I directed «El otro lado de la cama» in 2002, and in 2014 I had a huge hit about a man from Seville pretending to be Basque. Who am I? → Emilio Martínez-Lázaro: source: The fun fact is probably wrong in both the source and the translation. The fact check says Los Secretos are not on the soundtrack of «El otro lado de la cama», but Tequila is, along with Los Rodríguez, Coz and Kiko Veneno. Correct the source fun fact to name, for example, Tequila, Los Rodríguez and Coz, then translate it again. The rest of the translation is faithful and reads naturally. Fact check: wrong. The answer is right (Emilio Martínez-Lázaro directed both films; the wrong answers are different directors). The fun fact is inaccurate: Los Secretos is not in the film's soundtrack. Tequila is, along with Los Rodríguez, Coz and Kiko Veneno. I did not check the hints beyond this.
- **q-16384** (scientists-and-explorers) This huge antenna in Robledo de Chavela (Madrid) is run by INTA. What is it for? → Talking to faraway spacecraft: source: the fun fact says Robledo tracks “the Voyager probes” (present tense), but today only Voyager 1 can be reached from Madrid. Voyager 2 is too far south and is tracked only from Canberra. The source fun fact should say Voyager 1, and the translation should follow. Otherwise the translation is faithful and reads naturally.
- **q-17230** (rivers-and-mountains) Rain falls on Sierra Nevada, runs down the Genil, crosses Granada and keeps going. Which river basin does it belong to? → The Guadalquivir: Fact check: uncertain. The answer (Guadalquivir) is correct. The Segura, Tagus and Guadiana are not the Genil's basin. The fun fact is loose: sources place the Genil's headwaters near Mulhacén or the Veleta area, and I found no source giving 'almost 3,000 m'. One source gives 2,850 m for the Guarnón headwater near Corral del Veleta.
- **q-9950** (ham-cheese-and-produce) Look closely at this photo: it's a very typical dish in Spanish bars. What is it? → Calamares en su tinta: Source: hint 2 (“Su salsa no es de tomate ni de pimentón”) can't be relied on. Many classic recipes for calamares en su tinta (and chipirones en su tinta) start from a sofrito with tomato, and some add paprika. The fact check is "uncertain" and I can't confirm the hint either. The source's hint should be replaced with something safe, such as "The sauce gets its dark color from an ink, not from a spice." After that, re-translate it. Fact check: uncertain. The answer and the wrong answers hold up. Pulpo a la gallega, calamares a la romana and callos a la madrileña are all clearly different dishes. Hint 3 and the sepia fun fact are true. Hint 2 is shaky: many classic recipes for calamares en su tinta use a sofrito with tomato, and some add paprika, so 'isn't made with tomato or paprika' is not reliably true. This check was done from general knowledge, without web searches.
- **q-9958** (ham-cheese-and-produce) This is mojama, a salt-cured specialty of Cádiz and Huelva. Which fish is it made from? → Tuna: source: the fun fact's etymology is wrong. The RAE traces mojama to Hispano-Arabic mušámma‘, from Classical Arabic mušamma‘, meaning “waxed”, not “dried thing”. The Spanish source needs this fix first, and then the translation should follow it (e.g. “The word mojama comes from Arabic and means something like “waxed,” for its shiny look.”).

## Not travelling

- **q-14393** about_language, confirmed: «Pequeñín» significa «muy pequeño». ¿Cuál de estas palabras acabadas en -ín NO quiere decir «algo más pequeño»? → Jardín (Asks about the Spanish diminutive suffix -ín; cannot be rebuilt in English.)

## Stale re-translated

None.
