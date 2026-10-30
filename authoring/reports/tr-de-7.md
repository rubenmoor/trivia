# tr-de-7

Made by `qgen batch --translate de` on 2026-10-29 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 293
- Needs work: 6
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 840, about $32.20 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-7&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-5 | tr-de-6 | tr-de-7 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 299 |
| not travelling |  | 0 | 1 | 1 |
| not travelling confirmed |  | 0 | 1 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| approved |  | 297 | 297 | 293 |
| needs_work |  | 3 | 2 | 6 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 0.7 % ✓ | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.0 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 100.0 % ✓ | 100.0 % ✓ |
| cost $ |  | $28.08 | $29.79 | $29.76 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: giveaway 2 (0 major), fact 2 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.44

Major findings on approved questions:

None.

## Needs work

- **q-2278** (birds) Der Zwergpinguin aus Australien und Neuseeland ist der kleinste Pinguin der Welt. Wie groß ist er ungefähr? → Etwa 30 cm: source: hint 2 ("It's still bigger than a pigeon" / „Er ist trotzdem größer als eine Taube.“) is doubtful. A feral pigeon is about 29–36 cm long and the little penguin about 30–33 cm tall, so they are about the same size, not clearly different. Fix the source hint first, e.g. "It weighs only about 1 kg" or "It's about the size of a pigeon", then carry the change into the translation. Fact check: wrong. Answer (about 30 cm; the little penguin is about 30–33 cm tall) and the wrong answers are fine, and so is the fun fact. Hint 2 ('größer als eine Taube') is doubtful. A feral pigeon is about 29–36 cm long, so the penguin is about the same size, not clearly bigger.
- **q-2677** (reality-tv) Es passiert kurz vor Ende einer Folge, die Moderation verkündet es, und jemand muss die Show verlassen. Wie nennt man das? → Rauswurf: Fact check: wrong. The question is vague, and the description doesn't match it. The description talks about someone remembering the stove is still on at home, which has nothing to do with an elimination. "Rauswurf" is a plausible answer but not the standard term. Elimination shows use "Eliminierung" or "Ausscheiden". "Rauswurf" is also informal. Hint 3 says the person is "rausgewählt", which is an odd phrasing. The fun fact is true only for some shows, such as Big Brother or Dschungelcamp, and is stated loosely. It also lacks a clear link to the answer.
- **q-3640** (proverbs-of-the-world) Ein „Wolf im Schafspelz“ versteckt böse Pläne hinter einem freundlichen Gesicht. Welche Figur ist KEIN Wolf im Schafspelz? → Olaf aus „Die Eiskönigin“: Fact check: wrong. The question is flawed: the wrong-answer list includes the Wolf from Rotkäppchen, who is not a 'wolf in sheep's clothing' in the idiomatic sense (he is a real wolf who disguises himself as the grandmother). Still, he does deceive by disguise, so it's ambiguous. More importantly, the hint 'Drei von ihnen tun freundlich' fits Hans and Gothel, but the Wolf is openly predatory toward Rotkäppchen until the reveal. Also, the 'Wolf im Schafspelz' fable is from Aesop/Bible (Matthew 7:15), which is true. The core answer (Olaf is not a deceiver) is right, but the question is ambiguous because the Wolf is literally a wolf, and so arguably also not a 'Wolf im Schafspelz' figure.
- **q-3900** (rivers) Strand verhält sich zum Karibischen Meer wie ___ zum Fluss Magdalena. Was gehört in die Lücke? → Ufer: Fact check: wrong. The answer 'Ufer' is correct. The wrong answers (Mündung, Quelle, Flussbett) are really wrong. The fun fact is fine: the Magdalena is about 1,528 km long, flows into the Caribbean Sea and is Colombia's main river. But the description says 'im Haus', which makes no sense for a riverbank. I did not run searches. This rests on general knowledge.
- **q-4079** (world-war-ii) Weil im Krieg kein Coca-Cola-Sirup mehr nach Deutschland kam, wurde dort eine neue Orangenlimonade erfunden: Fanta. In welchem Jahrzehnt? → 1940er-Jahre: Source: the question calls Fanta "a new orange soda", but the original German Fanta from 1940/41 was a fruit soda made from whey and apple pomace. Orange Fanta only came in 1955, in Italy. The source and the translation need to drop "orange" (e.g. "ein neues Erfrischungsgetränk"/"a new soft drink"). The rest of the translation is faithful and reads naturally.
- **q-4940** (trains) Was ist das? → Fahrkarte: Fact check: wrong. The description is ambiguous: 'Einkaufszettel' is also a small piece of paper that adults often lose or forget just when they need it (in the shop). So a wrong answer could fairly count as correct. Hints and fun fact are fine (many train tickets are now digital, e.g. the Deutschlandticket). No web search was needed.

## Not travelling

- **q-2049** needs_local_knowledge, confirmed: Según el refrán, cuando la barriga está llena, ¿qué parte del cuerpo queda contenta? → El corazón (The question relies on the Spanish proverb 'Barriga llena, corazón contento'. German has no matching saying that names a body part, so German players would be guessing, not drawing on something they know.)

## Stale re-translated

None.
