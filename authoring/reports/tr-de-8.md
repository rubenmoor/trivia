# tr-de-8

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 848, about $33.66 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-8&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-6 | tr-de-7 | tr-de-8 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 299 | 300 |
| not travelling |  | 1 | 1 | 0 |
| not travelling confirmed |  | 1 | 1 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| approved |  | 297 | 293 | 297 |
| needs_work |  | 2 | 6 | 3 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 2.0 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 2.0 % ✓ | 0.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 100.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $29.79 | $29.76 | $31.09 |
| $ per approved |  | $0.10 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), overlap 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.57

Major findings on approved questions:

None.

## Needs work

- **q-2912** (world-cuisines) Ich bin ein Dessert aus Schokobiskuit-Schichten, Sahne und roten Steinfrüchten. Was bin ich? → Schwarzwälder Kirschtorte: In German the answer gives itself away. „Schwarzwälder Kirschtorte“ is the only option with a fruit in its name, and the question's „roten Steinfrüchten“ is just a clumsy way of saying cherries. On top of that, the source's illustrative image is a sharp bowl of cherries, and hint 1 (Kuckucksuhren) points German players straight to the Schwarzwald. The question needs a German version that doesn't hint at cherries (in the text, hint 1 or the image), or it should be marked as not travelling. The image needs a decorative or neutral replacement, for example a generic cake shop, which this run can't search for.
- **q-4546** (prehistory) In Fantasy-Filmen und -Spielen erhitzt dieser Handwerker Eisen im Feuer, hämmert es auf dem Amboss und macht Schwerter und Hufeisen. Wie heißt er? → Schmied: This duplicates q-9199, which is already approved in the German pool. Both ask for the craft that hammers horseshoes on an anvil, and the answer to both is „Schmied“. Seeing one gives the other away. Retranslating can't fix this: either drop this question in German, or retire one of the pair (check whether the English source pool has the same overlap).
- **q-4940** (trains) Was ist das? → Fahrkarte: Fact check: wrong. The facts are true (paper tickets exist, and many tickets are now digital, e.g. the Deutschlandticket). The riddle itself is ambiguous. Adults often lose a shopping list (Einkaufszettel) just when they need it, and a Geldschein is also a small piece of paper. The distractor Einkaufszettel therefore fits the description at least as well as Fahrkarte. Only the hints point to the answer.

## Not travelling

None.

## Stale re-translated

None.
