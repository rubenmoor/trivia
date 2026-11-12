# tr-en-17

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `germany` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 294
- Needs work: 5
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 528, about $25.48 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-17&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-15 | tr-en-16 | tr-en-17 |
|---|---|---:|---:|---:|
| sources |  | 5 | 5 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 5 | 5 | 299 |
| not travelling |  | 0 | 0 | 1 |
| not travelling confirmed |  | 0 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 0 | 0 | 294 |
| needs_work |  | 5 | 5 | 5 |
| needs_work rate | ≤ 20.0 % | 100.0 % ✗ | 100.0 % ✗ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 100.0 % ✗ | 100.0 % ✗ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 5 | 5 | 60 |
| audit/review agreement | ≥ 90.0 % | 0.0 % ✗ | 20.0 % ✗ | 100.0 % ✓ |
| cost $ |  | $1.37 | $1.46 | $23.22 |
| $ per approved |  | n/a | n/a | $0.08 |
| **health** | | ✗ fail | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: giveaway 1 (0 major), fact 3 (0 major), overlap 1 (1 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 60 of 60 (100 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.26

Major findings on approved questions:

None.

## Needs work

- **q-13089** (plants-and-forests) What is this cone from a conifer tree made of? → Many woody scales: source: the fun fact's claim that most cones on German forest floors come from spruces can't be confirmed. Pine covers about as much of Germany's forest as spruce, and pine cones also fall whole. The fact check is "uncertain". The source should use the safer wording: "Real fir cones almost never lie on the ground because they fall apart up in the tree; spruce and pine cones fall whole." The translation itself is faithful and reads naturally. Fact check: uncertain. The answer and hints are correct. Silver fir cones do disintegrate in the tree. The claim that most cones on German forest floors come from spruces is unverified, because pine cones are also very common on the ground and pine covers almost as much of Germany as spruce. I did not search to check this.
- **q-16068** (rap-and-electronic) This rapper became famous as a YouTuber, sat on the jury of “Deutschland sucht den Superstar” and had a number-one hit with “Bauch Beine Po”. Who is she? → Shirin David: Fact check: uncertain. Answer Shirin David is right: she is from Hamburg, was a YouTuber and DSDS juror, and "Bauch Beine Po" (2024) hit #1. Her debut album "Supersize" and the "David" stage-name hint are consistent with what I know. I couldn't confirm the fun fact as written. Sources describe the Hamburger Mädchenchor, the Jugendopernakademie, small acting roles at the Staatsoper, and piano, violin and oboe lessons. None named the Hamburg State Opera children's choir.
- **q-16910** (childrens-tv-and-audio-dramas) You don't watch it, you only listen. A voice reads a whole book out loud, great for long car trips. What is it? → Audiobook: This asks the same fact as the approved base question q-3506: identify an audiobook from "someone reads a book aloud to you and you listen through headphones". English players would get the same question twice. The translation itself is faithful and reads naturally. Separately, the source has no real link to Germany and probably belongs in base, if anywhere (source issue).
- **q-16917** (dialects-and-regional-words) Here people don't chat, they “schnacken”. There are also Fischbrötchen, dikes and wind off the sea. Where are you? → Northern Germany: Fact check: uncertain. Answer, wrong answers and hints are fine: 'schnacken' is northern German/Low German for chatting, and Hamburg and Bremen are in the north. I couldn't find 'Schnackbüdel' in any dictionary. The usual word is 'Schnacker', and 'Büdel' compounds are rare, so the fun fact may be invented.
- **q-9326** (reformation-to-empire) Who wrote the play “Die Räuber” (The Robbers), whose 1782 premiere in Mannheim drove the audience wild? → Friedrich Schiller: Source: hint 2 merges two trips. Schiller did travel to Mannheim in secret for the premiere in January 1782, but Duke Karl Eugen gave him the 14-day arrest for a second secret trip in May 1782. The source should say something like "He traveled secretly to Mannheim to see his play and was locked up for two weeks for it." The translation follows the source faithfully and has no other problems.

## Not travelling

- **q-14178** about_language, confirmed: Wer im Chat zustimmen will, schreibt oft nur „Isso“. Aus welchen Wörtern ist es zusammengezogen? → „ist so“ (Asks how a German slang contraction is built from German words („ist so“ vs „ich so“, „ist sowieso“); the options only work in German.)

## Stale re-translated

None.
