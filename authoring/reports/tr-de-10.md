# tr-de-10

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 295
- Needs work: 5
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 885, about $42.06 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-10&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-8 | tr-de-9 | tr-de-10 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 297 | 292 | 295 |
| needs_work |  | 3 | 8 | 5 |
| needs_work rate | ≤ 20.0 % | 1.0 % ✓ | 2.7 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.3 % ✓ | 2.0 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $31.09 | $37.42 | $38.73 |
| $ per approved |  | $0.10 | $0.13 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 8 (0 major), fact 1 (0 major), media 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.33

Major findings on approved questions:

None.

## Needs work

- **q-0077** (disney-films) Welche Gabe hat Luisa im Film „Encanto“? → Übermenschliche Kraft: source: the fun fact is wrong and the translation carries it over faithfully. Not every Madrigal has a magic door: Mirabel famously has none until the end, which is the film's central plot, and those who married into the family have none either. Correct it in the source, e.g. "Every gifted Madrigal gets a magic door to a room that matches their gift", then re-translate.
- **q-0660** (cartoons) Was haben Zoetrop, Thaumatrop und Praxinoskop gemeinsam, alles Erfindungen des 19. Jahrhunderts? → Sie täuschen Bewegung vor: source: the thaumatrope normally merges two images into one (bird in a cage), so "Sie täuschen Bewegung vor" doesn't hold for all three devices, and hint 2 (drawings changing slightly from frame to frame) doesn't fit it at all. The translation is faithful, so the source needs correcting, e.g. by replacing the thaumatrope with the phenakistiscope, or by changing the answer to the afterimage/persistence-of-vision effect. Fact check: wrong. The Thaumatrop (1824) doesn't fake movement. It is a disc with two different images, one on each side. When spun, they blend into one image, such as a bird in a cage. So "Sie täuschen Bewegung vor" is false for it, and hint 2 (drawings that change slightly from frame to frame) doesn't fit it either. What all three share is that they use persistence of vision. The Zoetrop and Praxinoskop do show motion. The other wrong answers (sound, electricity, 3D) are correctly wrong. The fun fact is roughly right: Greek zoe = life and tropos = turning, usually rendered "Rad des Lebens".
- **q-0841** (world-cups) Ich bin ein italienischer Torwart, wurde 2006 mit meinem Land Weltmeister und spielte noch mit über 45 Jahren als Profi. Wer bin ich? → Gianluigi Buffon: source: hint 1 overstates the fact in both languages. Buffon spent about 19 of his roughly 28 professional years at Juventus, with about eight more at Parma and a season at PSG, so "Fast meine ganze Karriere" / "casi toda mi carrera" is wrong. Both should say "most of my career" ("Den größten Teil meiner Karriere verbrachte ich bei Juventus Turin."). The rest of the translation is faithful.
- **q-2494** (formula-1-and-motorsport) Ein Rennwagen überholt das Auto auf dem zweiten Platz, wie auf dem Foto. Auf welchem Platz liegt er jetzt? → Platz 2: Fact check: wrong. The question is ambiguous. "Das Auto auf dem zweiten Platz" is overtaken by the racer, but the question doesn't say which place the racer was in. The answer "Platz 2" only holds if the racer was in 3rd place before. The classic riddle reads "Du überholst den Zweiten". The photo is also not essential and gives no position info. The hints ("Der Führende ist immer noch vor ihm") and the fun fact ("Platz 1" is the common wrong answer) fit the classic riddle. The wrong answers are fine. But "Platz 3" could be defended if a leader were not assumed.
- **q-2912** (world-cuisines) Ich bestehe aus Schichten von Schokobiskuit, Schlagsahne und roten Früchten. Was bin ich? → Schwarzwälder Kirschtorte: The kept image, 'Bowl of cherries with colours enhanced', gives the answer away in German: the question hides the cherries as 'roten Früchten', but the picture shows them, and 'Schwarzwälder Kirschtorte' is the only option with cherries in its name. The media needs swapping for a picture without cherries (for example a Black Forest landscape would also give it away, so use a neutral image such as a generic cake or baking scene) or making decorative/blurred. The text itself is fine.

## Not travelling

None.

## Stale re-translated

None.
