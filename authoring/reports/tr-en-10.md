# tr-en-10

Made by `qgen batch --translate en` on 2026-10-29 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 298
- Approved: 290
- Needs work: 8
- Not travelling: 2 (1 confirmed → `translatable: false`, 1 translated again next run)
- Claude calls: 516, about $29.80 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-10&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-8 | tr-en-9 | tr-en-10 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 297 | 298 |
| not travelling |  | 3 | 3 | 2 |
| not travelling confirmed |  | 3 | 3 | 1 |
| rejected rate | ≤ 20.0 % | 1.0 % ✓ | 1.0 % ✓ | 0.3 % ✓ |
| approved |  | 288 | 293 | 290 |
| needs_work |  | 9 | 4 | 8 |
| needs_work rate | ≤ 20.0 % | 3.0 % ✓ | 1.3 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.0 % ✓ | 1.3 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 1.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 93.3 % ✓ |
| cost $ |  | $25.68 | $27.46 | $26.76 |
| $ per approved |  | $0.09 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 58 (3 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 3 (2 major), overlap 5 (0 major), media 1 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 56 of 60 (93 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.04

Major findings on approved questions:

- **q-5212**: giveaway — The description, "Grandma's favorite wrapping…", gives the answer away: "To wrap tamales" is the only option about wrapping, so the other three are ruled out before any hint. This comes from the source ("La envoltura favorita de la abuela"), and the translation keeps it word for word. Apart from that, the translation is faithful and reads naturally in US English, the facts are right (leaves are used to wrap tamales in Tolima, and you don't eat them), and the banana-leaf image fits the question. (http://127.0.0.1:8001/review/q-5212)
- **q-5236**: giveaway, media — The translation matches the source, and "A penalty" is a fair English word for "penitencia". The problem is the description, which says "nobody wants to be left holding anything". That tells players the outcome is bad, which rules out all three wrong answers (candy, prize, applause), since they are all rewards. The source has the same flaw ("nadie quiere quedarse con nada en las manos"). The media is also weak: it is marked essential, but "Playing a Maths Game" is a generic classroom photo, not tingo tingo tango. (http://127.0.0.1:8001/review/q-5236)

## Needs work

- **q-5211** (scientists-and-inventors) I was born in Cali, arrived in the US with 300 dollars, and narrated the Perseverance rover's Mars landing in Spanish. Who am I? → Diana Trujillo: Overlap in the pool: approved q-7947 ("Diana Trujillo, from Cali, led the team behind this Mars rover's robotic arm…") and q-8478 ("The Perseverance rover, which Colombian Diana Trujillo worked on…") both name the answer with the same clues (Cali, Mars rover, Perseverance), so seeing either one gives this question away. The translation itself is accurate and reads naturally. To fix this, take Trujillo's name out of q-7947 and q-8478 (e.g. "a Colombian engineer from Cali"), or retire this question. The same applies to the source pool.
- **q-6930** (olympic-medallists) Which of these colors does NOT appear in the Olympic rings? → Purple: Source: this asks the same fact as approved q-6258 ("Which color is NOT one of the colors of the Olympic rings?" → Purple), so English players would meet the same question twice. It also has no real Colombian link beyond hint 2, which breaks the bundle rule. The translation itself is faithful and natural, but the source question should be dropped or replaced with one about a Colombian Olympic medallist.
- **q-7079** (other-sports) The sack race is to the sack as the egg race is to the… → Spoon: Fact check: uncertain. The answer 'Spoon' is right: the egg-and-spoon race is a real, well-known race. The wrong answers (Basket, Plate, Hen) are not the standard implement. I did not run web searches, so this rests on general knowledge. The description ('only sport where climbing into a bag is part of the training') is inaccurate, because the sack race is a game and not training. Hint 3 ('mouth or hand') fits the spoon but is vague. The fun fact about Colombian school fairs and paseos de olla is plausible, and paseo de olla is a real custom, but I could not verify the sack-race link.
- **q-7365** (mountains-and-landscapes) It falls from the clouds on stormy afternoons, pounds on tin roofs and can turn streets white. What falls in a hailstorm? → Little balls of ice: Fact check: uncertain. The fun fact says hail piled up almost 1 m high on some streets on Nov 3, 2007. The storm and date are real, and it was the strongest in about 40 years. I found no source for the 1 m depth. A 50 cm figure I saw was for a different storm.
- **q-7633** (drinks) Smelling fritanga, seeing mango biche with salt or hearing chicharrón frying makes your mouth water. Which part of the body makes that “water”? → The salivary glands: Source: this asks the same fact as approved q-4549 (mouth watering comes from the salivary glands, same answer), and the Colombian foods are only decoration. Seeing one question gives the other away. The translation itself is faithful and natural, but the question should be dropped or replaced with a different fact in the source.
- **q-7681** (popular-and-andean-music) If you go out with a couple and you're the extra person, in Colombia they say you're “tocando…”. Which instrument finishes the phrase? → Violin: The fun fact doesn't say what the source says. The source calls «tocar violín» very Colombian and says other countries use «hacer mal tercio» or «ser el chaperón». The translation instead says the phrase is also used in Chile and Peru, and that Spain uses «hacer de carabina» or «hacer mal tercio». The Chile and Peru claim is plausible, so the source's "very Colombian" may be overstated (source: worth checking). But the claim that Spain says «hacer mal tercio» can't be confirmed, since Spain typically says «hacer de carabina» or «sujetar la vela». Bring the fun fact back in line with the source, or keep only claims that can be confirmed (for example the Colombian saying plus the English "third wheel").
- **q-7914** (places-and-monuments) At Medellín's most famous fair, the silleteros parade with silletas on their backs. What are the silletas made of? → Flowers: Fact check: wrong. Facts are right (silletas are made of flowers at the Feria de las Flores, and a large one can weigh 60 kg or more). But the image query 'Medellin metrocable' would show a cable car, not silleteros or silletas. It doesn't fit the question.
- **q-8172** (pioneers-and-popular-figures) I was a philanthropist from Antioquia. I lived in a castle in Medellín that is a museum today, and I gave Itagüí its first library. Who am I? → Diego Echavarría Misas: Fact check: wrong. Answer is right (Diego Echavarría Misas, Coltejer family, Itagüí library bears his name). But hint 2 is false: he did not buy the castle in the 1940s. He had it built (c. 1930–1932) as a home with his wife Benedikta Zur Nieden, and filled it with European art.

## Not travelling

- **q-0256** about_language, translate again: Completa el coro de los gozos de la novena: 'Dulce Jesús mío, mi niño adorado, ¡ven a nuestras almas! ¡Ven, no tardes…!' → tanto (Asks for a missing Spanish word in a Spanish lyric; options, rhyme/syllable hint and “te quiero ___” hint only work in Spanish.)
- **q-7683** about_language, confirmed: «Tú eres» es a «vos sos» como «tú tienes» es a… → «Vos tenés» (Asks for the Spanish voseo verb form; it tests Spanish grammar, so it doesn't work in English.)

## Stale re-translated

None.
