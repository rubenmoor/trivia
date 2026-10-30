# tr-de-9

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 292
- Needs work: 8
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 844, about $41.16 at list price; $0.13 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-9&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-7 | tr-de-8 | tr-de-9 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 300 | 300 |
| not travelling |  | 1 | 0 | 0 |
| not travelling confirmed |  | 1 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 293 | 297 | 292 |
| needs_work |  | 6 | 3 | 8 |
| needs_work rate | ≤ 20.0 % | 2.0 % ✓ | 1.0 % ✓ | 2.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.0 % ✓ | 0.3 % ✓ | 2.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $29.76 | $31.09 | $37.42 |
| $ per approved |  | $0.10 | $0.10 | $0.13 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 10 (1 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.74

Major findings on approved questions:

None.

## Needs work

- **q-0295** (mountains) Wie viele Berge auf der Welt sind höher als 8000 Meter? → 14: source: the fun fact says without qualification that Messner was the first to climb all 14 eight-thousanders, in 1986. After Eberhard Jurgalski's summit research, Guinness World Records revised this in 2023 and now lists Ed Viesturs, so the claim is contested. Correct the source (e.g. drop the 'first' claim or say 'gilt traditionell als Erster'); the translation can then follow. For that retranslation, 'der Südtiroler' reads better than 'der Italiener' for German speakers.
- **q-0841** (world-cups) Ich bin ein italienischer Torwart, wurde 2006 Weltmeister und spielte noch mit über 45 Jahren als Profi. Wer bin ich? → Gianluigi Buffon: source: Hint 1 overstates the fact, in the source ('casi toda mi carrera') and so in the translation. Buffon spent about 19 of his 28 professional years at Juventus; he also played for Parma (1995–2001, 2021–2023) and PSG (2018–19). The hint should say 'most of my career' ('Die meiste Zeit meiner Karriere verbrachte ich bei Juventus Turin.') in both the source and the translation.
- **q-1551** (fashion-history) Ich trage eine Uniform mit blauen, gelben und roten Streifen, einen Helm mit Feder und eine Lanze und beschütze den Papst. Wer bin ich? → Schweizergarde: source: the question says the Swiss Guard carries a lance ("lanza"/"Lanze"), but its traditional weapon is the halberd. The error comes from the Spanish source, so correct it there too ("alabarda"/"Hellebarde"); the German translation is otherwise faithful and natural. Fact check: wrong. The Swiss Guard carries a halberd (Hellebarde), not a lance (Lanze). The rest checks out: the current uniform dates from 1914 (Jules Repond), and the Michelangelo story is a myth.
- **q-2912** (world-cuisines) Ich bin eine Torte aus Schokobiskuit-Schichten, Schlagsahne und Kirschen. Was bin ich? → Schwarzwälder Kirschtorte: Giveaway in the German wording: the question says "Ich bin eine Torte" and "Schwarzwälder Kirschtorte" is the only option that is a Torte (the others are Streuselkuchen, Clafoutis and Strudel), so the text alone gives the answer. It would help to make the wrong answers cherry Torten as well, or to replace "Torte" with a neutral word such as "Ich bin ein Dessert" in the question.
- **q-3121** (weather-and-climate) Der Forscher Douglas Mawson sprach von der „Heimat des Schneesturms“. Dort wurde auch die tiefste Temperatur aller Zeiten gemessen. Wie heißt diese Gegend? → Antarktis: source: the fun fact's "about 80 km/h" annual mean wind at Cape Denison is unconfirmed. The fact check is 'uncertain': 1912–13 measurements give about 19.3–19.4 m/s, or roughly 70 km/h, and I can't settle it from my own knowledge. Correct or drop the figure in the source first, then carry it into the translation. Minor, same pass: 'Gegend' is odd for a continent-sized place; 'Wie heißt diese Region?' reads better. Fact check: uncertain. The answer (Antarktis), the wrong answers and the hints are fine. Mawson's "Home of the Blizzard" is Cape Denison, and Antarctica holds the record low (−89.2 °C at Vostok). The fun fact's wind figure is shaky. Measurements from 1912–13 give an annual mean of about 19.3–19.4 m/s, or roughly 70–71 km/h. The "80 km/h" figure is a popular, rounded number that appears on Wikipedia-derived pages.
- **q-3301** (earthquakes) Die San-Andreas-Verwerfung zieht sich durch Kalifornien. Wie lang ist sie ungefähr? → Etwa 1200 km: source: hint 3 is inaccurate in both the English source and the translation. London–Rome is about 1430 km in a straight line, about 20% more than the fault's roughly 1200 km, and the fact check's verdict is "wrong". Correct the source, for example with London–Vienna (about 1240 km), then carry the change into the translation. Fact check: wrong. The answer (about 1200 km, roughly 800 miles) is right and the wrong answers are clearly wrong. The fun fact about offset streams is true. Hint 3 is off: London to Rome is about 1,430 km in a straight line, which is about 20% more than 1,200 km.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wofür war sein Körper ursprünglich gemacht? → Zum Essen: source: Hint 2 is factually wrong, and the translation faithfully copies it. In Toy Story 4, Woody climbs into the kindergarten bin and puts the spork and other scraps on Bonnie's table; Bonnie doesn't find it in the trash herself. The source hint needs correcting, for example to "The spork came out of a kindergarten trash can", and then the German should follow. The fact check's "trash she took from the bin" repeats the same error.
- **q-4546** (prehistory) In Fantasy-Filmen und -Spielen erhitzt dieser Handwerker Eisen im Feuer, hämmert es auf dem Amboss und macht Schwerter und Hufeisen. Wie nennt man ihn? → Schmied: Duplicate of approved q-9199: both describe a craftsman hammering horseshoes on an anvil and ask for the job, with the answer "Schmied". Keep only one of them in the German pool. The difference in setting (fantasy vs. medieval workshop) doesn't make this a different fact.

## Not travelling

None.

## Stale re-translated

None.
