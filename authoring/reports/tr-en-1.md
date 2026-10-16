# tr-en-1

Made by `qgen batch --translate en` on 2026-10-16 (plan 66, D-81): `base` questions translated into English. Generated file: don't edit by hand.

- Sources: 50 (0 stale re-translated)
- Translated: 49
- Approved: 49
- Needs work: 0
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 176, about $7.56 at list price; $0.11 per approved translation (without the audit)
- Spot check by a native speaker: http://127.0.0.1:8001/review?batch=tr-en-1&locale=en&sample=1

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. The pilot (`-1`) and a ✗ stop the next `qgen batch --translate` until `qgen health ack` (D-55).

| metric | threshold | tr-en-1 |
|---|---|---:|
| sources |  | 50 |
| stale re-translated |  | 0 |
| translated |  | 49 |
| not travelling |  | 1 |
| not travelling confirmed |  | 1 |
| rejected rate | ≤ 20.0 % | 2.0 % ✓ |
| approved |  | 49 |
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
| audited |  | 49 |
| audit/review agreement | ≥ 90.0 % | 83.7 % ✗ |
| cost $ |  | $5.55 |
| $ per approved |  | $0.11 |
| **health** | | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 8 of 49 (16 %)
- Major among review needs work: 0 of 0
- Problems by kind: giveaway 2 (1 major), ambiguity 1 (1 major), media 11 (8 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 49 (0 %)
- Audit/review agreement (both accept or both not): 41 of 49 (84 %)
- Sample: 49 audited of 49; 49 Claude calls, about $2.01

Major findings on approved questions:

- **q-0126**: media — The question needs essential media, but media.title is null. With no flag crop on screen, "This small piece comes from a flag" can't be answered. The translation itself is faithful and natural: the facts (eagle and snake on a cactus, Tenochtitlan, green/white/red), the options and the hints all match the source and are correct. (http://127.0.0.1:8001/review/q-0126)
- **q-0186**: media — The media is essential, but no file was picked (title is null). That leaves "Look at this close-up" with nothing to show, so the question can't be played as it is. The translation itself is faithful and natural: the facts, options and hints match the source, and explaining ají as "a spicy sauce" in hint 3 is a harmless addition. The empanada etymology in the fun fact is correct. (http://127.0.0.1:8001/review/q-0186)
- **q-0466**: media — The media is marked essential ("Look at this picture…"), but its title is null, so no file was picked. Without a close-up photo of butterfly-wing scales the question can't be answered, and the fix has to come from the source's media. The translation itself is faithful and natural US English: the "tiles"/"roof" description works, the hints and options match the source, and the fact is right (butterfly wings are covered in scales, dragonfly wings are not). One small risk to check: a close-up of moth scales would look the same, so the photo you pick must really be from a butterfly. (http://127.0.0.1:8001/review/q-0466)
- **q-0725**: media — The media is marked essential, and the question opens with “Look at the photo”, but no file was picked (title is null). As it stands the question can't be played: it needs a clear photo of a Mongolian ger/yurt. The translation itself is fine. Swapping the source's “Jaima” for “Wigwam” works, because the Mongolian/Gobi clue still points only to the yurt. Hint 2 and the fun fact are accurate. (http://127.0.0.1:8001/review/q-0725)
- **q-0738**: media — Media is marked essential, but no file was picked (title null). The question opens with "Look at this plant", so it can't be played without a catnip photo. This is a source-level issue, not a translation one. Everything else checks out: catnip (Nepeta cataria) is in the mint family (Lamiaceae), the hints are true (toothed leaves, minty smell, culinary herb relatives), and the fun fact matches the usual figure that about a third of cats don't react, a trait that is inherited. The translation is faithful and reads naturally. Small quibble in the description: "the only plant" isn't strictly true, since silvervine and valerian also affect cats, but it reads as a joke. (http://127.0.0.1:8001/review/q-0738)
- **q-1697**: media, ambiguity — The media is marked essential, but no file was picked (title is null). The question says “Look at this huge fossil tooth”, so it can't be played without the picture. Without the image, the text alone is ambiguous: big theropod dinosaurs like T. rex and Carcharodontosaurus also had large serrated fossil teeth, so “A dinosaur” is defensible. The source has the same dependency on the image. The translation itself is faithful, and its hints and fun fact are accurate. (http://127.0.0.1:8001/review/q-1697)
- **q-1834**: media, giveaway — The media is marked essential ("Take a close look at this tail"), but no file was picked (title null), so the question can't be played without a photo of a rattlesnake's rattle. Minor: the description ("its own soundtrack") all but names the only noisy tail among the options, though it copies the reviewed source. The translation is faithful and natural. The facts check out: the rattle is keratin and gains a segment at each shed. (http://127.0.0.1:8001/review/q-1834)
- **q-2123**: media — The media is marked essential but no file was picked (title null), yet the question opens with "This chocolate", which refers to a picture nobody sees. It needs a clear chocolate-truffle photo, or a decorative role and reworded text (this gap is inherited from the source). Translation fidelity, facts (truffles are fungi that grow on oak roots and reproduce with spores; chocolate truffle credited to Dufour, France, 1895), options and hints all check out. (http://127.0.0.1:8001/review/q-2123)

## Needs work

None.

## Not travelling

- **q-0905** about_language, confirmed: En una boda, la novia dice emocionada: '¡Por fin encontré a mi media naranja!'. ¿Qué quiere decir? → Su pareja ideal (The question asks what the Spanish idiom “media naranja” (literally “half orange”) means. English says “my other half” or “better half”, with no fruit in it. Translating it word for word would only make sense as a question about Spanish. Using the English idiom drops the orange, so the fruit wrong answer, the description and the image no longer fit, and the question becomes trivial.)

## Stale re-translated

None.
