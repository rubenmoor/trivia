# tr-de-15

Made by `qgen batch --translate de` on 2026-10-30 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 288
- Needs work: 12
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 886, about $44.86 at list price; $0.14 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-15&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-13 | tr-de-14 | tr-de-15 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 291 | 291 | 288 |
| needs_work |  | 9 | 9 | 12 |
| needs_work rate | ≤ 20.0 % | 3.0 % ✓ | 3.0 % ✓ | 4.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 2.3 % ✓ | 3.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.7 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 1.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 95.0 % ✓ | 96.7 % ✓ |
| cost $ |  | $40.85 | $39.80 | $40.83 |
| $ per approved |  | $0.14 | $0.14 | $0.14 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 58 (2 %)
- Major among review needs work: 1 of 2 (50 %)
- Problems by kind: giveaway 9 (0 major), fact 3 (1 major), overlap 2 (1 major), difficulty 1 (0 major), style 2 (1 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.02

Major findings on approved questions:

- **q-2170**: fact, style — The answer "Bruder Johannes" is a literal rendering of Friar John, but the classic Schlegel translation, the German text beside the "Bruder Lorenzo" the question uses, calls him "Bruder Markus" (cast lists: "Bruder Markus, von demselben Orden"; https://projekt-gutenberg.org/authors/william-shakespeare/books/william-shakespeare-romeo-und-julia), so it breaks "names as German speakers know them" and the very players who could answer a 15 would look for a name that isn't an option. The story, hints and fun fact match the play (the zeno.org scene text failed to load, so the Markus name rests on search results); a fix should use "Bruder Markus" or state that the name follows the English original, and hint 3 needs adjusting either way. (http://127.0.0.1:8001/review/q-2170)

## Needs work

- **q-0077** (disney-films) Welche Gabe hat Luisa in „Encanto“? → Übermenschliche Kraft haben: source: the fun fact is wrong in the Spanish source and the German copies it. Not every Madrigal has a magic door showing a gift: Mirabel has no gift or door of her own for most of the film, which is its central plot point, and those who married in have none either. It should read 'every gifted member of the Madrigal family', in the source first and then in the translation.
- **q-0341** (toys) In welchem Land wurde der Zauberwürfel erfunden? → Ungarn: Duplicate: approved q-0369 asks the same fact (country of origin of the Zauberwürfel, answer Ungarn) with only a different wording. One of the two should be dropped. The overlap exists in the source pool too, so the translation itself is not at fault.
- **q-0354** (museums) Schau dir dieses berühmte Gemälde an: „Las Meninas“ aus dem Prado in Madrid. Wer hat es gemalt? → Diego Velázquez: source: the fun fact is imprecise in both the Spanish source and the German translation. Picasso's 1957 series has 58 works, but only about 45 are versions of Las Meninas; the rest are pigeons, landscapes and a portrait. Correct the source, for example to "more than 40 versions" or "a series of 58 works", then carry the change into the translation.
- **q-0989** (maths) Ergänze beim Dreieck: „Gleichseitig“ bedeutet drei gleiche Seiten, „ungleichseitig“ bedeutet … → Keine gleichen Seiten: The German term „ungleichseitig“ literally says the answer „Keine gleichen Seiten“. Unlike the opaque „escaleno“, it also rules out both angle options, so the question nearly answers itself, the giveaway the translator's notes warned about. Hint 1 about the English word „scalene“ is also odd for German players. A possible rework: ask „Wie heißt ein Dreieck mit drei verschieden langen Seiten?“ with the terms as options, though the options then need checking, or mark the item as not travelling.
- **q-1544** (fashion-history) Welches europäische Volk verbindet man traditionell mit dieser flachen Wollmütze? → Basken: Overlap in German: approved q-6565 ("Wie heißt diese Kopfbedeckung?") has the answer "Baskenmütze", which contains this question's answer "Basken". Seeing one gives the other away, and the same headgear would be shown in both. The Spanish "boina" has no such link, so the problem arises only in German. Consider not playing this question in German.
- **q-1551** (fashion-history) Ich trage eine Uniform mit blauen, gelben und roten Streifen, einen Helm mit Feder und eine Lanze und beschütze den Papst. Wer bin ich? → Schweizergarde: source: the Swiss Guard's traditional weapon is a halberd, not a lance, so the Spanish "una lanza" is wrong and the German "eine Lanze" carries the error over. The fact check also returned `wrong`. Correct the source to "alabarda"; the translation can then use "eine Hellebarde". Fact check: wrong. The Swiss Guard carries a halberd (Hellebarde), not a lance (Lanze). The rest (blue/yellow/red uniform, plumed helmet, 1914 uniform, Michelangelo myth) is correct.
- **q-1671** (crime-fiction) Ich war Detektiv Sam Spade in „Die Spur des Falken“ und Philip Marlowe in „Tote schlafen fest“, Klassikern des Film noir. Wer bin ich? → Humphrey Bogart: source: the fun fact is inaccurate, and the translation reproduces it faithfully. Gallimard's Série noire is known for its black-and-yellow look, and its name did not come from black covers. Correct the source fun fact, for example: "Den Namen „Film noir“ verdankt das Genre französischen Kritikern (u. a. Nino Frank, 1946), die sich unter anderem von der französischen Krimireihe „Série noire“ inspirieren ließen." Then carry the correction into the German text. Fact check: wrong. The answer, wrong answers and hints are correct. Bogart played Spade (1941) and Marlowe (1946), and the Casablanca line matches the German dub. The fun fact is inaccurate: Gallimard's Série noire was known for its yellow covers with a black band, not black covers. The series name wasn't about the covers.
- **q-1952** (winter-olympics) Wann finden die Paralympischen Winterspiele statt, verglichen mit den Olympischen Winterspielen? → Kurz danach, am selben Ort: source: hint 2 ("Nunca se celebran antes que los Juegos Olímpicos" / "Sie finden nie vor den Olympischen Spielen statt") is historically false. The Winter Paralympics of 1980 (Geilo), 1984 and 1988 (both Innsbruck) took place before the Winter Olympics of those years. The fix belongs in the source: reword hint 2 to the present day, and add a time frame to the question ("heute"/"hoy"), because the answer only holds since 1992. The German translation itself is faithful and natural.
- **q-2246** (athletics) Diese Latte liegt lose auf zwei Halterungen und fällt bei der kleinsten Berührung. Bei welchen Leichtathletik-Wettbewerben kommt sie zum Einsatz? → Sprungdisziplinen: source: the fact check is 'wrong', and I agree. 'Jumping events' is too broad because long jump and triple jump are jumping events without a bar; only high jump and pole vault use one. The source also says the bar drops at the slightest touch, which contradicts its own fun fact that a brushed bar can stay up. The English source needs correcting (e.g. a narrower answer or 'jumping events with a bar', and a softer claim); the German then follows it. Fact check: wrong. The answer 'Sprungdisziplinen' is too broad. Long jump and triple jump are also jumping events, but they have no bar. Only the vertical jumps (high jump and pole vault) use a loose bar on two supports. The wrong answers (throws, relays, race walking) are correctly wrong. The hints and fun fact are accurate: the bar is raised after each round, and a touch doesn't count as a failure if the bar stays on the pegs.
- **q-2677** (reality-tv) Es passiert gegen Ende einer Folge, die Moderation verkündet es, und jemand muss die Show verlassen. Wie nennt man das? → Rauswurf: Fact check: wrong. The question is flawed. The description ("someone suddenly remembers the stove is still on at home") doesn't match the question, which asks for the elimination. "Rauswurf" is not the standard term for a TV-show elimination; "Eliminierung" or "Ausscheiden" is more common. The hint "Niemand möchte, dass es ihn selbst trifft" is vague. The wrong answer "Immunität" fits poorly as a distractor. The fun fact is only true for some shows (e.g. Big Brother, Survivor).
- **q-3089** (the-lord-of-the-rings) Das Wort ist in Gondor gebräuchlich, taucht in Boromirs Traum auf und spielt auf die Körpergröße an. Wer sind die „Halblinge“? → Hobbits: Fact check: wrong. The text facts are right: 'Halfling' is the Gondorian name for hobbits, it appears in Boromir's dream verse, and the Prologue gives hobbit height as roughly 2–4 feet (60–120 cm). The wrong answers and hints hold up. I checked this from memory of the books, not by searching. The media query 'Mont Saint-Michel abbey' has nothing to do with hobbits or Middle-earth.
- **q-3840** (toys) In „A Toy Story: Alles hört auf kein Kommando“ bastelt Bonnie ein Spielzeug mit Wackelaugen und Pfeifenputzer-Armen. Wozu diente sein Hauptteil ursprünglich? → Zum Essen: source: hint 2 is factually wrong, and the German repeats it. In Toy Story 4 Woody fishes the spork out of the trash and puts it on Bonnie's table; Bonnie doesn't take it from the bin herself. The source hint should become e.g. "Woody fished his main part out of a kindergarten trash can for Bonnie", then the German should follow.

## Not travelling

None.

## Stale re-translated

None.
