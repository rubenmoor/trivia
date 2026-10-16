# tr-de-1

Made by `qgen batch --translate de` on 2026-10-16 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 50 (0 stale re-translated)
- Translated: 50
- Approved: 50
- Needs work: 0
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 181, about $8.56 at list price; $0.13 per approved translation (without the audit)
- Spot check by a native speaker: http://127.0.0.1:8001/review?batch=tr-de-1&locale=de&sample=1

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. The pilot (`-1`) and a ✗ stop the next `qgen batch --translate` until `qgen health ack` (D-55).

| metric | threshold | tr-de-1 |
|---|---|---:|
| sources |  | 50 |
| stale re-translated |  | 0 |
| translated |  | 50 |
| not travelling |  | 0 |
| not travelling confirmed |  | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ |
| approved |  | 50 |
| needs_work |  | 0 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ |
| audited |  | 50 |
| audit/review agreement | ≥ 90.0 % | 80.0 % ✗ |
| cost $ |  | $6.59 |
| $ per approved |  | $0.13 |
| **health** | | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 10 of 50 (20 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 4 (1 major), fact 1 (0 major), media 12 (10 major), style 2 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 50 (0 %)
- Audit/review agreement (both accept or both not): 40 of 50 (80 %)
- Sample: 50 audited of 50; 50 Claude calls, about $1.97

Major findings on approved questions:

- **q-0126**: media, giveaway — The media is essential, but no file was picked (title null). The question asks about "Dieser Ausschnitt", so it can't be played without the image. Minor: hint 2 ("grün, weiß und rot") already rules out all three wrong answers (Ecuador, Albania, Egypt), and the description's cactus points straight at the Mexican coat of arms. The German translation is faithful and natural, and the facts check out, including the Tenochtitlan legend. (http://127.0.0.1:8001/review/q-0126)
- **q-0186**: media — The question needs a close-up photo ("Sieh dir diese Nahaufnahme an"), but the essential media has no file (title null), so it can't be played as it is. The translation itself is faithful and reads naturally: the options keep their Spanish names without articles, the hints match the source and don't give the answer away early, and the etymology of "empanar" in the fun fact is correct. (http://127.0.0.1:8001/review/q-0186)
- **q-0466**: media — The media role is essential, but no file was picked (title null). The question only works with a close-up of a butterfly wing's scales, so it can't be played as it is. The translation itself is faithful and natural: "Schau dir … an" uses du, the options are article-free, and the hints, the fun fact (powder = wing scales) and the difficulty are all fine. (http://127.0.0.1:8001/review/q-0466)
- **q-0490**: media — The media is essential, but no file was picked (title null), so "Sieh dir das Foto an" points at a photo that isn't there and the question can't be answered. The translation itself is faithful and natural: the answer and distractors are correct, hint 3 still works in German (Venus + Fliege), the hints are true (native only to wetlands in North and South Carolina), and the fun fact is right (two touches within roughly 20 seconds). (http://127.0.0.1:8001/review/q-0490)
- **q-0693**: media — The question needs an essential photo ("Schau dir das Foto an: Diese japanische Süßigkeit…"), but no file was picked (media title is null). Without a dorayaki photo the question can't be played. The translation itself is faithful and natural German, and the facts are correct: dorayaki is Doraemon's favourite food, the filling is anko, and he is a blue robot cat without ears. (http://127.0.0.1:8001/review/q-0693)
- **q-0738**: media, style — The media is marked essential, but no file was picked (title null). The question opens with "Schau dir diese Pflanze an" and hint 1 asks players to look at the leaves, so the question can't be played as it stands. The facts are correct: catnip (Nepeta cataria) belongs to the Lamiaceae, and roughly a third of cats don't react to it, which is inherited. The family names are understandable but not the usual German terms ("Lippenblütler", "Korbblütler", "Süßgräser"/"Rosengewächse"). Also, the German name "Katzenminze" makes the answer easier for German players than in the source. (http://127.0.0.1:8001/review/q-0738)
- **q-0751**: media — The media is marked essential, but no file was picked (title is null). The question says „Fruchtfliegen wie diese“, so it points at a picture that won't be there. The facts check out: on 20 February 1947 the US launched a captured V-2 from White Sands, New Mexico, and the flies came back alive in a capsule on a parachute. The German wording is natural and stays faithful to the source. (http://127.0.0.1:8001/review/q-0751)
- **q-1697**: media — The image is marked essential, but no file was picked (title null). The question says „Sieh dir diesen … Zahn an“, so it can't be played without the photo, and the text alone (a huge, serrated fossil tooth) also fits theropod dinosaurs such as T. rex. The German translation itself is accurate and natural: the options carry no articles, none of the hints gives the answer away, the „steinreich“ description works, and the fact that sharks replace their teeth for life is correct. (http://127.0.0.1:8001/review/q-1697)
- **q-1834**: media — The media is essential (the question says "Schau dir diese Schwanzspitze genau an"), but no file was picked (title null), so the question can't be played without the rattle photo. The translation itself is faithful and natural: the hints, the fun fact (a new segment with each shed) and the description are correct, and hint 3 plays on "Klapperschlange" instead of the source's "cascabel", which is allowed for hint 3. (http://127.0.0.1:8001/review/q-1834)
- **q-2123**: media — The media is marked essential, but no file was picked (title null). The question says „Diese Praline“, so without a picture of a chocolate truffle on screen the question points at nothing. The translation itself matches the source: the answer Pilz and the wrong answers Knollenpflanze, Samen and Schnecke are correct and fit grammatically, the hints and the fun fact are true and the German reads naturally. (http://127.0.0.1:8001/review/q-2123)

## Needs work

None.

## Not travelling

None.

## Stale re-translated

None.
