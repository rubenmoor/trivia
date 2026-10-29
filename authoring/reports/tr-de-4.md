# tr-de-4

Made by `qgen batch --translate de` on 2026-10-29 (plan 66, D-81): `base` questions translated into German. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 294
- Approved: 288
- Needs work: 6
- Not travelling: 6 (6 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 855, about $30.67 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-de-4&locale=de

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-de-2 | tr-de-3 | tr-de-4 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 298 | 294 |
| not travelling |  | 2 | 2 | 6 |
| not travelling confirmed |  | 2 | 2 | 6 |
| rejected rate | ≤ 20.0 % | 0.7 % ✓ | 0.7 % ✓ | 2.0 % ✓ |
| approved |  | 290 | 294 | 288 |
| needs_work |  | 7 | 4 | 6 |
| needs_work rate | ≤ 20.0 % | 2.4 % ✓ | 1.3 % ✓ | 2.0 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.3 % ✓ | 1.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 1.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 95.0 % ✓ | 98.3 % ✓ | 98.3 % ✓ |
| cost $ |  | $26.97 | $29.28 | $28.41 |
| $ per approved |  | $0.09 | $0.10 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 59 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 2 (0 major), ambiguity 1 (0 major), media 1 (0 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 59 of 60 (98 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.26

Major findings on approved questions:

None.

## Needs work

- **q-0660** (cartoons) Was haben Zoetrop, Thaumatrop und Praxinoskop gemeinsam, drei Erfindungen aus dem 19. Jahrhundert? → Sie täuschen Bewegung vor: Source: the classic thaumatrope doesn't show a sequence of slightly changing drawings. It merges two pictures (bird and cage) into one, so hint 2 is wrong for it, and "täuschen Bewegung vor" fits it only loosely. The fact check rates this "wrong". Fix the source first: replace the thaumatrope with the phenakistiscope, or reword the answer and hint 2 around persistence of vision. Then re-translate. The German translation itself is faithful and natural. Fact check: wrong. Das Thaumatrop zeigt keine Bewegung. Es hat zwei verschiedene Bilder auf Vorder- und Rückseite einer Scheibe (z. B. Vogel und Käfig), die beim Drehen im Auge zu einem Bild verschmelzen. Die Antwort „täuschen Bewegung vor“ und Hinweis 2 („Zeichnungen, die sich von Bild zu Bild nur ein bisschen verändern“) stimmen daher nur für Zoetrop und Praxinoskop. Gemeinsam ist allen dreien die Nutzung der Nachbildwirkung (Trägheit des Auges). Die übrigen Aussagen sind richtig: Alle drei stammen aus dem 19. Jahrhundert, und „Zoetrop“ wird üblicherweise als „Rad des Lebens“ übersetzt.
- **q-0917** (natures-records) Was haben der Mount Everest, der Aconcagua und der Mount Vinson gemeinsam? → Sie sind die höchsten Berge ihres Kontinents: Fact check: wrong. Hint 3 is imprecise: Aconcagua is the highest peak of South America, not of 'Amerika' as a whole (Denali is North America's highest).
- **q-1549** (fashion-history) Mein Mann krönte sich zum Kaiser, ich brachte Kleider mit hoher Taille unter der Brust in Mode und liebte die Rosen meines Gartens. Wer bin ich? → Joséphine Bonaparte: source: hint 3 („Mein Mann wurde bei Waterloo besiegt und auf eine Insel verbannt“) is wrong in Joséphine's voice. Napoleon divorced her in 1809/1810, and she died in May 1814, a year before Waterloo, so he wasn't her husband then and she never saw that defeat or the exile to St Helena. The Spanish source has the same error, so it should be fixed there first (e.g. „Ich ließ mich 1809 von dem Mann scheiden, der später bei Waterloo besiegt wurde.“). Then the German version can follow. Fact check: wrong. The answer is right. Napoleon crowned himself, and Joséphine popularized Empire-style dresses and grew roses at Malmaison. The wrong answers don't fit. But hint 3 is anachronistic in her voice: Napoleon divorced her in 1809, and she died in May 1814, a year before Waterloo (1815). She was no longer his wife, and she never saw his final defeat or his exile to St Helena. The fun fact about hundreds of cashmere shawls is commonly reported.
- **q-2021** (famous-scientists) Zu sehen sind die berühmtesten Nervenzellen-Zeichnungen der Geschichte, von Hand gemacht von einem Medizin-Nobelpreisträger. Wer hat sie gezeichnet? → Santiago Ramón y Cajal: Source issue (media): the question says „Zu sehen sind …“ (source: „Estás viendo …“), meaning the image should be one of Cajal's hand drawings, but the kept file 'Simple Myelinated Neuron of the PNS.jpg' is a modern schematic diagram. The question doesn't match what players see. The source media should be replaced with an actual Cajal drawing that has no signature or label, and the role should be essential. The German translation itself is faithful and fine.
- **q-4079** (world-war-ii) Der Krieg stoppte den Coca-Cola-Sirup für Deutschland, also wurde dort eine neue Orangenlimo erfunden: Fanta. In welchem Jahrzehnt? → 1940er-Jahre: source: The question calls wartime Fanta a "new orange soda", which is wrong. The first Fanta (1940/41) was made from whey and apple pomace, and orange Fanta only came in 1955 in Italy. The source should say "a new soft drink" instead, and then the translation should be redone with "eine neue Limonade". The translation itself is faithful and reads naturally.
- **q-4287** (extreme-sports) Ein Kitesurfer steht auf einem kleinen Brett und wird von einem riesigen Drachen gezogen. Was hält er in den Händen, um den Drachen zu steuern? → Lenkstange: Hint 1 starts with the feminine pronoun „Sie ist …“. „Lenkstange“ is the only feminine option (Gabelbaum and Schleppgriff are masculine, Paddel is neuter), so hint 1 gives the answer away by grammar alone. Hint 3 („Man hält sie …“) does the same. Both hints need rewording without a gendered pronoun, e.g. „Das gesuchte Teil ist über lange Leinen mit dem Drachen verbunden.“ and „Man hält das Teil mit beiden Händen, ähnlich wie einen Fahrradlenker.“

## Not travelling

- **q-1250** needs_local_knowledge, confirmed: En la ronda se canta: 'Cucú, cantaba la rana… cucú, pasó un marinero, cucú, vendiendo…'. ¿Qué vendía? → Romero ('Cucú, cantaba la rana' is a Spanish-language nursery rhyme unknown in Germany; hint 3 also relies on a Spanish rhyme (romero/marinero).)
- **q-1255** needs_local_knowledge, confirmed: 'Los pollitos dicen' es a 'hambre y frío' como 'Señora Santa Ana' es a… → Una manzana perdida ('Los pollitos dicen' and 'Señora Santa Ana' are Spanish-language children's songs that German-speaking players don't know.)
- **q-0428** about_language, confirmed: Completa el refrán: «Camarón que se duerme…» → …se lo lleva la corriente (The question asks players to complete a Spanish proverb („Camarón que se duerme, se lo lleva la corriente“). German has no such saying. The nearest German proverbs („Wer zu spät kommt, den bestraft das Leben“, „Den Letzten beißen die Hunde“) would make it a different question with a different answer.)
- **q-2087** about_language, confirmed: Perdiste el partido y andas desanimado. Según el dicho, ¿qué prenda tienes caída? → La capa (Asks about the Spanish idiom 'andar de capa caída'. German has no matching clothing idiom for being downcast, so the question can't be rebuilt fairly.)
- **q-4082** about_language, confirmed: U-boats were German, hunted ships crossing the Atlantic and attacked in groups called “wolf packs”. What was a U-boat? → A submarine (The question asks what the foreign word 'U-boat' means. In German, 'U-Boot' is simply the everyday word for submarine, so the question would answer itself. The fun fact about 'Unterseeboot' would also be trivial.)
- **q-0592** needs_local_knowledge, confirmed: Soy el profe del canal «Unicoos», donde subo clases gratis de matemáticas, física y química. ¿Quién soy? → David Calle (Unicoos and all four options are Spanish-language YouTube science communicators. They are known only in the Spanish-speaking world, and German players would have no exposure to them, so the question would be pure guessing.)

## Stale re-translated

None.
