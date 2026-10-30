# tr-en-9

Made by `qgen batch --translate en` on 2026-10-29 (plan 66, D-81): `base` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 293
- Needs work: 4
- Not travelling: 3 (3 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 623, about $30.48 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-9&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-7 | tr-en-8 | tr-en-9 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 295 | 297 | 297 |
| not travelling |  | 5 | 3 | 3 |
| not travelling confirmed |  | 5 | 3 | 3 |
| rejected rate | ≤ 20.0 % | 1.7 % ✓ | 1.0 % ✓ | 1.0 % ✓ |
| approved |  | 293 | 288 | 293 |
| needs_work |  | 2 | 9 | 4 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 3.0 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 3.0 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $28.15 | $25.68 | $27.46 |
| $ per approved |  | $0.10 | $0.09 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), overlap 1 (0 major), media 2 (0 major), difficulty 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.01

Major findings on approved questions:

None.

## Needs work

- **q-0017** (capital-cities) What is the capital of France? → Paris: Fact check: wrong. The answer, wrong answers, hints and fun fact are correct. But the media query is 'Mont Saint-Michel', which is not in Paris and doesn't illustrate the answer.
- **q-0137** (dinosaurs) Look at this skeleton: which dinosaur is it? → Stegosaurus: source: the description says the animal has “a club on its tail”, but Stegosaurus had tail spikes (a thagomizer). The tail club belongs to Ankylosaurus, which is one of the wrong options, so the description is false and points players to a wrong answer. The source needs fixing first, for example “...still wearing the roof, with spikes on its tail” or with no tail detail at all. After that the translation can follow it.
- **q-0716** (extreme-sports) In a tandem skydive, roughly how high up do you jump out of the plane? → 4,000 meters: source: Hint 3 says 4,000 m is "about the height of a very tall mountain in the Andes". That is misleading, because the very tall Andean peaks are 6,000–7,000 m (Aconcagua is about 6,960 m), and many Andean cities sit near 4,000 m. The translation copies this faithfully, so the source hint needs correcting first, for example: "It's about the height of the highest cities in the Andes" or "a bit lower than Mont Blanc". Everything else in the translation is faithful and reads naturally. Fact check: wrong. Hint 3 is misleading. 4,000 m is not 'a very tall mountain in the Andes'. Many Andean peaks and cities are at or above that height (Aconcagua is about 6,960 m). The answer itself is fine: tandem jumps go from about 3,000 to 4,200 m (10,000 to 14,000 ft), and freefall lasts about 50 to 60 seconds. This is from memory; I ran no searches.
- **q-1661** (pop-music) There are seven of them, they're from South Korea, and in 2020 “Dynamite” made them the first South Korean group to hit No. 1 on Billboard. Who are they? → BTS: Source: the claim is wrong as stated, in both the source and the translation. BTS already reached No. 1 on the Billboard 200 album chart in 2018 with "Love Yourself: Tear". "Dynamite" was their first No. 1 on the Billboard Hot 100, the singles chart. The source should say "Hot 100" (for example "the first all-South Korean act to top the Billboard Hot 100"), and the translation should then follow it.

## Not travelling

- **q-1560** about_language, confirmed: Si de alguien dicen que «es el benjamín de la casa», ¿qué quiere decir? → Que es el hijo menor (Asks what a Spanish idiom means (“es el benjamín de la casa” = the youngest child). English has no common equivalent: calling the youngest child “the Benjamin” is rare and old-fashioned, so the question would no longer be about an everyday expression.)
- **q-1818** about_language, confirmed: Para decir que alguien espera algo imposible, se dice que 'pide peras' a un árbol. ¿A cuál? → Al olmo (Asks for the wording of the Spanish idiom “pedir peras al olmo”. English has no equivalent, so English players couldn't know or work out the tree. The willow also has no edible fruit, so you can't reason your way to the elm either. Hint 3 is also built on the Spanish word “olmo”.)
- **q-1807** wordplay, confirmed: Completa: «calcomanía» es a «cuaderno» como «…» es a «chat de WhatsApp». → Sticker (The analogy depends on Spanish using two words (“calcomanía” for the paper one, “sticker” for the chat one). In English both are “sticker”, so the first half of the analogy already gives the answer, and hint 3 (“its English name means…”) doesn't work.)

## Stale re-translated

None.
