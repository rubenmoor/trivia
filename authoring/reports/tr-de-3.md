# tr-de-3

Made by `qgen batch --translate de` on 2026-10-28 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 298
- Approved: 294
- Needs work: 4
- Not travelling: 2 (2 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 856, about $31.52 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-3&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-1 | tr-de-2 | tr-de-3 |
|---|---|---:|---:|---:|
| sources |  | 50 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 50 | 297 | 298 |
| not travelling |  | 0 | 2 | 2 |
| not travelling confirmed |  | 0 | 2 | 2 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| approved |  | 50 | 290 | 294 |
| needs_work |  | 0 | 7 | 4 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 2.4 % ✓ | 1.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 1.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 50 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 80.0 % ✗ | 95.0 % ✓ | 98.3 % ✓ |
| cost $ |  | $6.59 | $26.97 | $29.28 |
| $ per approved |  | $0.13 | $0.09 | $0.10 |
| **health** | | ✗ fail | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), difficulty 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.24

Major findings on approved questions:

None.

## Needs work

- **q-1254** (childrens-songs) Man macht es mit beiden Händen, es ist laut, und das Lied „Wenn du glücklich bist …“ fordert dazu auf. Was ist es? → Klatschen: Fact check: uncertain. The answer Klatschen is right, and Winken, Pfeifen and Hüpfen are wrong. The hints are fine. The fun fact is shaky. The English title is correct, but the claim that the song originally comes from English is disputed. Sources say the melody may derive from a Latvian folk song or from Dunayevsky's 1938 Soviet song "Molodezhnaya". The earliest English print is from 1957.
- **q-3293** (earthquakes) Die Feuerwehr zeigt Kindern diesen roten Gegenstand. Wofür ist er da? → Kleine Brände löschen: Fact check: uncertain. I did not search; this is from general knowledge. The answer 'Kleine Brände löschen' is right, and the three wrong answers are clearly wrong. Hints 2 and 3 are true, and the fun fact is broadly true (early fire engines were hand-drawn, later horse-drawn). Hint 1 is misleading. Fire engines carry portable extinguishers of similar size (for example 6 to 12 kg powder). What they have that is much bigger is the water tank and pump, not 'viel größere Feuerlöscher'. The fun fact is also unrelated to the extinguisher.
- **q-4811** (extreme-sports) Du sitzt im Sessellift und fährst den Berg hinauf. Wie schnell bringt er dich ungefähr nach oben? → Etwa 15 km/h: Fact check: uncertain. The answer depends on lift type. From memory (I did not run a search): fixed-grip chairlifts run about 2–2.5 m/s (7–9 km/h), and detachable ones about 4–6 m/s (15–21 km/h). So 'about 15 km/h' fits modern detachable lifts but is too high for fixed-grip lifts. The wrong answers (2, 60 and 150 km/h) are clearly wrong. The hints and fun fact are accurate for detachable lifts.
- **q-4908** (temples-and-cathedrals) Den Bau dieser weißen Basilika in Paris versprach man in einem Gelübde, nachdem Frankreich 1870/71 einen Krieg verloren hatte. Wer besiegte Frankreich? → Preußen: source: Hint 1 says the new united country was founded right after the war ('Gleich nach dem Krieg'), but the German Empire was proclaimed on 18 January 1871, during the war (armistice 28 January, Treaty of Frankfurt May 1871). Fix the source hint to say 'during the war' (e.g. 'Noch während des Krieges wurde ein neues, geeintes Land gegründet.'), then re-translate it. Fact check: wrong. Hint 1 is inaccurate: the German Empire was proclaimed on 18 Jan 1871 during the war, not right after it. The answer 'Preußen' is acceptable (Prussia led the German coalition), and the Sacré-Cœur vow and the calcite fun fact are true.

## Not travelling

- **q-1017** about_language, confirmed: En España, el juego de sacar papelitos y dar un regalo sin revelar a quién te tocó no se llama 'amigo secreto'. ¿Cómo lo llaman allá? → Amigo invisible (Asks which Spanish word Spain uses ('amigo invisible' vs 'amigo secreto'). This is a regional Spanish vocabulary difference with no German equivalent (in German it is simply 'Wichteln').)
- **q-0397** needs_local_knowledge, confirmed: Mira la foto: ¿cómo se llama este dulce típico de la costa colombiana? → Cocadas (Asks for the name of a Colombian coastal sweet; all four options (cocadas, panelitas, alfandoques, bocadillos) are Colombian sweets that German players don't know. The only way to guess it is that 'Cocada' sounds a bit like 'Kokos'. Swapping in German-known distractors would turn it into a different question.)

## Stale re-translated

None.
