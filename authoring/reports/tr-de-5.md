# tr-de-5

Made by `qgen batch --translate de` on 2026-10-29 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 297
- Needs work: 3
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 840, about $30.23 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-5&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-3 | tr-de-4 | tr-de-5 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 298 | 294 | 300 |
| not travelling |  | 2 | 6 | 0 |
| not travelling confirmed |  | 2 | 6 | 0 |
| rejected rate | ≤ 20.0 % | 0.7 % ✓ | 2.0 % ✓ | 0.0 % ✓ |
| approved |  | 294 | 288 | 297 |
| needs_work |  | 4 | 6 | 3 |
| needs_work rate | ≤ 20.0 % | 1.3 % ✓ | 2.0 % ✓ | 1.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 1.4 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $29.28 | $28.41 | $28.08 |
| $ per approved |  | $0.10 | $0.10 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.15

Major findings on approved questions:

None.

## Needs work

- **q-1360** (product-design) Thomas Jefferson soll einen der ersten Drehstühle besessen haben. In welchem Jahrhundert hat er ihn benutzt? → 18. Jahrhundert: Fact check: uncertain. I did not run a search, so this rests on prior knowledge. The 18th-century answer is the intended one: Jefferson's swivel Windsor chair dates to about 1775–76, and tradition says he used it for the Declaration. The Darwin fun fact (wheels on his chair at Down House) is also right. But Jefferson lived until 1826 and kept using swivel chairs in the 19th century, so '19. Jahrhundert' is arguably not clearly wrong.
- **q-3456** (international-football) In Italiens Serie A trägt ein Team eine ganze Saison lang einen kleinen grün-weiß-roten Schild auf dem Trikot. Wofür steht er? → Amtierender Meister: The hints don't match the gender of the noun: the question uses "der Schild", but hints 1–3 refer to it as "es" ("darf es nur ein einziges Team tragen", "hat es sich verdient", "Es bekommt das Team"). They should use "ihn" ("darf ihn nur ein einziges Team tragen", "hat ihn sich … verdient", "Ihn bekommt das Team, …"). Everything else matches the source.
- **q-6120** (architectural-styles) Er war wie Victor Horta ein belgischer Jugendstil-Pionier, baute das Haus Bloemenwerf bei Brüssel und gründete eine Designschule in Weimar. Wer war er? → Henry van de Velde: Fact check: uncertain. The answer and hints check out. The fun fact says the Hôtel Tassel was finished in 1893. Sources I remember give construction as 1893–94, so the year may be off by one. I checked this from memory and ran no searches.

## Not travelling

None.

## Stale re-translated

None.
