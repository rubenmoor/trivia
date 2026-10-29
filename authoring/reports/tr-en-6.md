# tr-en-6

Made by `qgen batch --translate en` on 2026-10-29 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 519, about $25.90 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-6&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-4 | tr-en-5 | tr-en-6 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 298 | 289 | 300 |
| not travelling |  | 2 | 11 | 0 |
| not travelling confirmed |  | 2 | 11 | 0 |
| rejected rate | ≤ 20.0 % | 0.7 % ✓ | 3.7 % ✓ | 0.0 % ✓ |
| approved |  | 292 | 288 | 295 |
| needs_work |  | 6 | 1 | 5 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 0.3 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 0.3 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 96.7 % ✓ | 96.7 % ✓ | 98.3 % ✓ |
| cost $ |  | $23.62 | $26.46 | $23.46 |
| $ per approved |  | $0.08 | $0.09 | $0.08 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 59 (2 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: fact 1 (1 major), overlap 1 (1 major), other 1 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.44

Major findings on approved questions:

- **q-6793**: fact, other — The translation changes the answer: the source asks for the Spanish sound «quiquiriquí», but the English version asks for "cock-a-doodle-doo". That also removes the question's only link to Colombia, so it no longer fits the colombia bundle. Under "regional words travel", it should ask about the original word, e.g. "In Colombia a dog says “guau”. What does a rooster say?" with "Quiquiriquí" as the answer, Spanish sounds like "Cuac", "Oinc" and "Muuu" as the wrong answers, and the original hints adapted. The fun fact, the 1 rating and the junglefowl image are fine. (http://127.0.0.1:8001/review/q-6793)

## Needs work

- **q-6930** (olympic-medallists) Which of these colors does NOT appear in the Olympic rings? → Purple: The translation itself is faithful and natural. The problem is in the source: this asks the same fact as approved q-6258 ("Which color is NOT one of the colors of the Olympic rings?" → Purple), so English players would get the same question twice. The Colombian link is only in hint 2. The source should be retired or replaced with a different Colombia-related Olympic question.
- **q-7267** (languages) In which of these cities do people NOT speak with a costeño accent? → Bucaramanga: Fact check: wrong. The answer and the options are right. The description is the problem. It says people talk fast, chop their words and never get upset, which fits costeños (the wrong answers). It doesn't fit Bucaramanga, whose people are known as 'bravos', as q-7901 says. I checked this from general knowledge, not by searching.
- **q-7365** (mountains-and-landscapes) It falls from the clouds during afternoon downpours, sounds really loud on tin roofs and can turn streets white. What falls in a hailstorm? → Balls of ice: Source: the fun fact says the ice piled up "almost a meter" deep on some Bogotá streets on November 3, 2007. The fact check could not confirm that figure (the only source found says 1.5 m of water and ice at one intersection), and I can't confirm it either. Fix the source's fun fact first, for example: "On November 3, 2007, Bogotá's heaviest hailstorm in decades left ice piled up on some streets and trapped dozens of cars." Then carry the change into this translation. The translation itself is faithful and reads naturally. Fact check: uncertain. The 3 Nov 2007 Bogotá hailstorm is real. But the ice depth in the fun fact (almost 1 m on some streets) isn't confirmed. The only figure I found is 1.5 m (59 in) of water and ice at one intersection, from a forum quoting the BBC. Reports of how many cars were trapped also differ (30 vs 70).
- **q-7434** (cycling) In Colombia, a bicycle is called a “cicla.” If a park has 4 ciclas and 2 tricycles, how many wheels are there in total? → 14: Fact check: uncertain. The maths is right: 4×2 + 2×3 = 14, and the wrong answers are wrong. The fun fact is shaky. In Colombia "llanta" mainly means the tire, and "rueda" is the usual word for the whole wheel. Using "llanta" for the whole wheel is only loose colloquial usage, and I couldn't verify it.
- **q-8414** (national-team) I'm a goalkeeper, I played for Arsenal in England and Napoli in Italy, and I was Colombia's starting keeper at the 2014 and 2018 World Cups. Who am I? → David Ospina: source: Hint 2 and the fun fact say Ospina has the most caps in Colombia's history. That record changes over time, and by late 2026, after the 2026 World Cup, James Rodríguez has probably passed Ospina's 128 caps. Both the source and the translation should drop the record claim: hint 2 could become another clue (for example Atlético Nacional or Copa América 2021), and the fun fact a stable fact. The rest of the translation matches the source and reads naturally.

## Not travelling

None.

## Stale re-translated

None.
