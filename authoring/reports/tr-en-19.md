# tr-en-19

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `germany` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 297
- Approved: 295
- Needs work: 2
- Not travelling: 3 (1 confirmed → `translatable: false`, 2 translated again next run)
- Claude calls: 525, about $26.82 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-19&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-17 | tr-en-18 | tr-en-19 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 299 | 297 |
| not travelling |  | 1 | 1 | 3 |
| not travelling confirmed |  | 1 | 1 | 1 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| approved |  | 294 | 292 | 295 |
| needs_work |  | 5 | 7 | 2 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 2.3 % ✓ | 0.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 2.0 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 96.7 % ✓ |
| cost $ |  | $23.22 | $23.21 | $24.30 |
| $ per approved |  | $0.08 | $0.08 | $0.08 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 60 (3 %)
- Major among review needs work: 0 of 0
- Problems by kind: fact 1 (0 major), overlap 2 (2 major), style 1 (0 major), other 1 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.52

Major findings on approved questions:

- **q-12026**: overlap — This repeats related q-5889 ("Medieval castles had thick, tall walls… What were most of them made of?" → Stone). Naming Marksburg doesn't change the fact being asked, and seeing either question gives the other away. The translation itself is faithful and natural, the answer and fun fact are correct (Marksburg is often called the only Middle Rhine hilltop castle never destroyed), and the options and hints are fine. One small point: Marksburg is a hilltop castle without a water moat, so the description is only a general castle joke. (http://127.0.0.1:8001/review/q-12026)
- **q-12094**: overlap, other — The translation reads well and is accurate. Replacing hint 3 (“Geschirrspüler”) was a good call, and the Cochrane 1886 patent is correct. The problem is overlap: approved q-2709 (“dirty plates go in the…” → Dishwasher) asks the same thing, the machine you load with dirty plates. Seeing one gives the other away. Also, a dishwasher has no German link, so the source fits the germany bundle poorly. (http://127.0.0.1:8001/review/q-12094)

## Needs work

- **q-16116** (gdr-everyday-life) The “Pionierrepublik Wilhelm Pieck” lay on Lake Werbellin, also welcomed children from many other countries, and was named after East Germany's first president. What was it? → A large vacation camp for kids: Fact check: wrong. The fun fact gives the site's current name as 'European Youth Recreation and Meeting Center'. Sources call it the 'Europäische Jugenderholungs- und Begegnungsstätte' (EJB), meaning a meeting 'site', not a 'center'. It now runs as the 'seezeit-resort'. The question and answer are fine.
- **q-16910** (childrens-tv-and-audio-dramas) You don't watch it, you only listen. A voice reads a whole book out loud, great for long car trips. What is it? → Audiobook: This asks the same fact as the approved base question q-3506: a voice reads a book aloud, you listen to it, and the answer is audiobook. English players of the germany bundle also get base questions, so they would see the same question twice. This goes back to the source and also has no German connection. Rewording the translation can't fix that, so drop this item or replace the source.

## Not travelling

- **q-14018** other, confirmed: Wie nannte Wilhelm Conrad Röntgen die Strahlen selbst, die er 1895 entdeckte? → X-Strahlen (The question works because German calls them “Röntgenstrahlen”; in English the everyday name is “X-rays”, so asking what Röntgen called them gives the answer away (hint 3 even points to the English word).)
- **q-16161** about_language, translate again: „usw.“ steht für „und so weiter“. Welche dieser Abkürzungen bedeutet etwas ganz anderes? → d. h. (Asks which German written abbreviation (usw., usf., u. Ä., d. h.) differs in meaning; a German spelling/writing convention that doesn't carry into English.)
- **q-11099** about_language, translate again: Was bedeutet die Abkürzung „z. B.“? → zum Beispiel (Asks what the German abbreviation “z. B.” stands for; the wrong answers depend on German words starting with z/B, and the English answer “for example” would match the hint “e.g.”, so it can't be rebuilt fairly.)

## Stale re-translated

None.
