# tr-en-32

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `spain` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 292
- Needs work: 5
- Not travelling: 3 (3 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 495, about $31.89 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-32&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-30 | tr-en-31 | tr-en-32 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 300 | 297 |
| not travelling |  | 3 | 0 | 3 |
| not travelling confirmed |  | 3 | 0 | 3 |
| rejected rate | ≤ 20.0 % | 1.0 % ✓ | 0.0 % ✓ | 1.0 % ✓ |
| approved |  | 289 | 295 | 292 |
| needs_work |  | 8 | 5 | 5 |
| needs_work rate | ≤ 20.0 % | 2.7 % ✓ | 1.7 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 0.7 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.0 % ✗ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $27.57 | $27.55 | $28.62 |
| $ per approved |  | $0.10 | $0.09 | $0.10 |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: giveaway 1 (0 major), overlap 1 (1 major), media 1 (1 major), style 6 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.28

Major findings on approved questions:

- **q-13295**: overlap — The translation is faithful and the facts check out: Law 4 requires the goalkeeper to wear colors different from the other players and the referee. The problem is that related q-6292 ("In soccer, which player must wear a shirt of a different color from all the teammates?" → The goalkeeper) asks the same fact, with only the Spain red-shirt setting added, so seeing one gives the other away. The media (an SC Internacional red shirt) is harmless and the difficulty of 2 fits. (http://127.0.0.1:8001/review/q-13295)

## Needs work

- **q-11126** (childrens-tv) In the gesture song “Mi barba tiene tres pelos”, the words go: “My beard has three hairs, three hairs has my beard; if it didn't have three hairs…”. How does it go on? → …it wouldn't be a beard: Source: the fun fact ("almost nothing is sung on the last round: you just point to your chin and hold up three fingers") can't be confirmed and seems overstated. In the usual game, only "barba", "pelos" and "tres" turn into gestures, so words like "tiene", "si no tuviera" and "pues no sería" are still sung. The fact check also found a source saying the last round is sung in full, just faster. Fix the source's fun fact, for example: "In the gesture game, a word is swapped for a gesture each round (beard, hairs, three) until the song is half mime." Then carry the change into the translation. The rest of the translation is faithful and natural. Fact check: uncertain. The song's ending is right: sin los tres pelos, it would no longer be a beard. The wrong answers (mustache, shave it off, four hairs) are clearly wrong. Two things are shaky. (1) Versions differ on the wording: "no sería mi barba" vs "no sería una barba". (2) The fun fact is not supported. The only source I could open (Guiainfantil) says the last round is sung in full, just faster, and does not describe pointing to the chin with three fingers. In the usual game, words are replaced by gestures round by round. It is not verified that nothing is sung at the end.
- **q-12350** (money-and-services) Look at this 1-cent euro coin. It's copper-colored on the outside, but what metal is it made of inside? → Steel: The media file is wrong. The essential image is "File:Didymograptus artos.1 - Ordovicico medio.JPG", which is a fossil, but the question says "Look at this 1-cent euro coin". The source question needs a real photo of a 1-cent euro coin, ideally the Spanish side. The English translation itself is faithful and reads naturally, so it needs no text changes.
- **q-15299** (modern-literature) I wrote “Fariña,” about smuggling in the Galician rías; a judge pulled it from bookstores in 2018 and it later became a TV series. Who am I? → Nacho Carretero: Source: the timeline is wrong in both versions. The Antena 3 series “Fariña” premiered in late February 2018, and the judge ordered the book pulled from stores in early March 2018, so “a judge pulled it… and it later became a TV series” gets the order backwards. The source should say something like “it became a TV series, and a judge pulled it from bookstores in 2018”, and then the translation should follow it. Apart from that, the translation is faithful and reads naturally.
- **q-15435** (tv-series) On TVE, this actor played a police officer solving crimes in late 19th-century Madrid. Which character was he? → Víctor Ros: Source: the essential image is the wrong man. "File:Carles Francino i Navarro (2005).jpg" shows Carles Francino Navarro, the radio journalist born in 1958. He is the father. The question shows "this actor", and the actor is his son, Carles Francino Murgades. Replace the image in the source with a photo of the actor, for example one from the 2010s when Víctor Ros aired. The English translation itself is faithful and reads naturally.
- **q-16384** (scientists-and-explorers) This huge antenna in Robledo de Chavela (Madrid) is run by INTA, Spain's aerospace agency. What is it for? → To talk to faraway spacecraft: source: the fun fact says Robledo tracks "the Voyager probes", but Voyager 2 is too far south in the sky to be seen from Madrid. Only Canberra can reach it, so only Voyager 1 is tracked from Robledo. The source fun fact should say "Voyager 1" (e.g. "Robledo still talks to Voyager 1, which has already left the solar system."), and then the translation should follow it.

## Not travelling

- **q-11136** wordplay, confirmed: Adivina: «Blanco por dentro, verde por fuera; si quieres que te lo diga, espera». ¿Qué fruta es? → La pera (The answer “pera” is hidden inside the Spanish word “espera”, and that can't be rebuilt in English.)
- **q-12294** about_language, confirmed: Llevo un gorrito ondulado encima y salgo en «niño», «España» y «mañana». ¿Qué letra soy? → La eñe (The question asks about a letter of the Spanish alphabet and its spelling in Spanish words, and English has no equivalent.)
- **q-11322** about_language, confirmed: Para decir «clickbait» en español, la Fundéu propone una palabra que empieza por «ciber-». ¿Cómo termina? → Anzuelo (Asks how a Spanish word coined by Fundéu (ciberanzuelo) is built. In English, players would have to complete a Spanish word, so the question is about the Spanish language itself.)

## Stale re-translated

None.
