# tr-en-4

Made by `qgen batch --translate en` on 2026-10-28 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 298
- Approved: 292
- Needs work: 6
- Not travelling: 2 (2 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 529, about $25.85 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-4&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-2 | tr-en-3 | tr-en-4 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 291 | 295 | 298 |
| not travelling |  | 9 | 5 | 2 |
| not travelling confirmed |  | 9 | 4 | 2 |
| rejected rate | ≤ 20.0 % | 3.0 % ✓ | 1.3 % ✓ | 0.7 % ✓ |
| approved |  | 282 | 292 | 292 |
| needs_work |  | 9 | 3 | 6 |
| needs_work rate | ≤ 20.0 % | 3.1 % ✓ | 1.0 % ✓ | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.0 % ✓ | 1.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 2.1 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $27.69 | $27.75 | $23.62 |
| $ per approved |  | $0.10 | $0.10 | $0.08 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 1 (0 major), fact 1 (0 major), overlap 1 (1 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.23

Major findings on approved questions:

- **q-0438**: overlap — The translation itself is accurate and reads naturally. The facts hold up: Bernal won in 2019 at age 22, he was born in Bogotá and grew up in Zipaquirá, and he started as a mountain biker. The rhyme with “canal” works in English, and the three wrong answers are really wrong. The problem is overlap with the approved q-7438 (“In what year did Egan Bernal win the Tour de France?”): seeing that question tells you Bernal won the Tour, and he is the only Colombian who has, so it gives this answer away. Hint 1 also states the 2019 answer to q-7438. (http://127.0.0.1:8001/review/q-0438)

## Needs work

- **q-0519** (independence) I'm a university in Bogotá, named after the first president of the State of Cundinamarca in 1811. Which one am I? → Universidad Jorge Tadeo Lozano: Source: the fun fact says the university was founded "almost 140 years" after Lozano's 1811 presidency, but 1954 − 1811 = 143 years, so it should say "more than 140 years". The error is in the Spanish source ("casi 140 años"), so the source needs the fix first. The translation itself is faithful and reads naturally.
- **q-7434** (cycling) In Colombia, a bicycle is called a “cicla.” If a park has 4 ciclas and 2 tricycles, how many wheels are there in total? → 14: Source: the fun fact says that in Colombia "llanta" means both the tire and the whole wheel. That can't be confirmed. In Colombian usage "llanta" mainly means the tire, "rin" is the rim and "rueda" is the wheel. The fact check rates it wrong. The source's fun fact needs to be replaced with a fact that can be checked, for example about "cicla" being everyday Colombian slang or about the Sunday ciclovía. Then this translation should be redone from the new source. Fact check: wrong. The math is right (4×2 + 2×3 = 14) and the wrong answers are wrong. The fun fact is not accurate. In Colombia "llanta" mainly means the rubber tire, and "rin" is the metal rim. It is not the standard word for the whole wheel (that is "rueda"). Some sources say "llanta" can mean the rim on a bicycle, and shops sometimes use it loosely for the whole assembly.
- **q-7676** (popular-and-andean-music) Carranga singers perform in a ruana and a light, hand-woven hat that keeps the sun off. What is that hat made of? → Straw: Fact check: uncertain. I couldn't confirm the hat is straw. Sources confirm the ruana and hat are the carranga look and that Jorge Velosa wears both. Some sources mention a straw campesino hat (e.g. the jipa). Boyacá campesino hats are also often felt (wool). Velosa's own hat is usually a dark felt one, which would make 'Wool' arguably correct. No source I found says what the carranga hat is made of. The question's 'light, hand-woven' wording favours straw. The fun fact is broadly true.
- **q-7902** (languages) In Colombian Sign Language, I’m used for spelling out names that have no sign: each letter is a hand shape. What am I? → The dactylological alphabet: The answer "the dactylological alphabet" copies the Spanish "alfabeto dactilológico" word for word. English speakers call it the "manual alphabet" or the "fingerspelling alphabet", so the correct option reads as translationese, and the question becomes a test of Greek roots. A natural version would use "The manual (fingerspelling) alphabet" as the answer. The options and hint 3 would then need new wording, because "manual" comes from the Latin for "hand" and the question already mentions hand shapes.
- **q-8141** (ghosts-and-creatures) I'm not a prayer or a charm, and I cost nothing. If a spirit gets you lost in the hills, I break the spell and you find your way. What am I? → Wearing your clothes inside out: Fact check: uncertain. Turning clothes inside out is the well-known remedy against the duende and Madremonte when lost. The duende is said to like children and long-haired girls, which is plausible. I did not run a search, so I couldn't confirm that every wrong answer is absent from the folklore (e.g. shoes on the wrong feet).
- **q-8414** (national-team) I'm a goalkeeper. I played for Arsenal in England and Napoli in Italy, and I started in goal for Colombia at the 2014 and 2018 World Cups. Who am I? → David Ospina: Source: hint 2 and the fun fact say Ospina has played more matches for Colombia than anyone else. That record can change, and by late 2026 James Rodríguez may have passed his roughly 128 caps, so I can't confirm it is still true. Rephrase it in the source (for example "one of the most-capped players in Colombia's history" or "more than 120 matches"), then translate it again. Apart from that, the translation is faithful and reads naturally.

## Not travelling

- **q-7705** about_language, confirmed: ¿Cuál de estas palabras NO es otra forma de decir «espanto»? → Guayabo (Asks which Spanish word is not a synonym of «espanto». Three options are general Spanish words (fantasma, espectro, aparición). In English, either they become “ghost/specter/apparition” and «guayabo» is the only Spanish word left, or the question stays a Spanish vocabulary test.)
- **q-6889** about_language, confirmed: Soy la palabra con que le hablas al profesor, a la abuela y al señor de la tienda cuando quieres ser respetuoso. ¿Qué palabra soy? → «Usted» (Asks which Spanish pronoun (usted vs tú/vos) is the formal one: general Spanish grammar, not a Colombian regional word.)

## Stale re-translated

None.
