# tr-en-26

Made by `qgen batch --translate en` on 2026-11-12 (plan 66, D-81): `spain` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 289
- Needs work: 10
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 537, about $30.65 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-26&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-24 | tr-en-25 | tr-en-26 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 299 | 299 |
| not travelling |  | 0 | 1 | 1 |
| not travelling confirmed |  | 0 | 1 | 1 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| approved |  | 295 | 294 | 289 |
| needs_work |  | 5 | 5 | 10 |
| needs_work rate | ≤ 20.0 % | 1.7 % ✓ | 1.7 % ✓ | 3.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.0 % ✓ | 1.3 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 96.7 % ✓ | 96.7 % ✓ |
| cost $ |  | $24.58 | $27.06 | $27.73 |
| $ per approved |  | $0.08 | $0.09 | $0.10 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: fact 1 (0 major), media 1 (0 major), style 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.92

Major findings on approved questions:

None.

## Needs work

- **q-11126** (childrens-tv) In this Spanish song, words are swapped for gestures each time: “My beard has three hairs, three hairs has my beard; if it didn't have three hairs…” How does it go on? → …it wouldn't be a beard: Fact check: uncertain. The usual lyric ends "no sería mi barba" (it wouldn't be my beard), and some versions say "una barba". The answer fits only loosely. The fun fact is also doubtful: in the last round every word (my, beard, three, hairs) is replaced by its own gesture, so nothing is sung. It isn't just pointing to the chin and holding up three fingers. I checked this from memory, not from a source.
- **q-11349** (school-and-home) I have camping spots, shared showers, campers and tents, and in summer I fill up with families. What am I? → A campground: The translation adds the answer's root word to the question. “Camping spots” and “campers” both echo “campground”, which makes it the only option that matches by sound. The source's “parcelas” and “caravanas” don't contain “camping”. Reword these as “sites” (or “plots”) and “RVs” (or “trailers”), so no word in the question shares “camp” with the answer.
- **q-11356** (school-and-home) What free phone number works in Spain for any emergency: fire, ambulance or police? → 112: Source: the fun fact says the European Union chose 112 in 1991, but the EU didn't exist until 1993 (Maastricht). The 1991 decision (91/396/EEC) came from the Council of the European Communities. The Spanish source has the same error, so it should say "la Comunidad Europea" (or drop the year), and the English then follow it as "the European Community". The rest of the translation is faithful and natural.
- **q-12412** (dress-crafts-and-games) I fix soles and heels with a hammer, nails and glue. Who am I? → A cobbler: This asks the same fact as the approved q-9398 ("The sole is worn through and the heel has broken off. Which craftsman do you take the shoe to?" → Cobbler), so English players would get the same question twice. The translation itself is accurate and reads naturally. The only link to Spain is the saying in the fun fact, so this item can't be fixed in the text: drop it from the English pool, or rebuild it around something Spanish, such as the saying “Zapatero, a tus zapatos”.
- **q-13295** (footballers-and-national-team) You're watching Spain's national soccer team, which plays in red. Which Spain player does NOT wear the red shirt? → The goalkeeper: source: This asks the same fact as approved q-6292 (the goalkeeper is the player who must wear a different color from the teammates); only the Spain framing differs, so in the English pool one gives the other away. The translation itself is faithful and natural; the overlap comes from the source question, which should be dropped or replaced with a different Spain-specific fact.
- **q-13371** (famous-figures) AuronPlay was born in 1988 in a Catalan city right next to Barcelona. Which one? → Badalona: Source: hint 3 ("Hace frontera con Barcelona por el norte") looks wrong. Badalona borders Sant Adrià de Besòs, Santa Coloma de Gramenet, Montgat and Tiana, but not Barcelona itself, and it lies to the northeast across the Besòs. The source should change it to something like "It lies just northeast of Barcelona, across the Besòs river." Separately, in the translation, "right next to Barcelona" is stronger than the source's "muy cerca" and also fits L'Hospitalet, which really does border Barcelona; it should read "very close to Barcelona".
- **q-14283** (painting-and-architecture) I was born in Brussels, became the first professor of landscape painting at Madrid’s San Fernando Academy, and painted the Picos de Europa. Who am I? → Carlos de Haes: Source problem, carried over faithfully into the translation. First, hint 3 states something false: Haes's surname doesn't look Dutch "because" his family moved to Málaga; it is Flemish because he was born to a Belgian family. The hint should give the two facts separately, for example "My surname isn't Spanish: my family moved from Belgium to Málaga when I was a child." Second, check "first professor of landscape painting": Jenaro Pérez Villaamil is usually named as the first holder of the landscape chair at San Fernando. Haes won that chair in 1857, at the new Escuela Especial.
- **q-14291** (painting-and-architecture) This carving of the Sacrifice of Isaac, now in Valladolid’s National Museum of Sculpture, is by a sculptor who trained in Italy studying Michelangelo. Who? → Alonso Berruguete: source: the fun fact says Berruguete was in Italy when the Laocoön was unearthed in 1506. That is doubtful. He is first documented in Florence around 1507–08. Vasari tells of him making a wax copy of the Laocoön for Bramante's contest, but that came after the discovery. The source fun fact needs changing, for example to "Berruguete spent about a decade in Italy, and his twisting figures recall the Laocoön and Michelangelo." Then the translation should follow it. Fact check: wrong. The fun fact is doubtful. The Laocoön was unearthed in January 1506, but Berruguete (b. c.1488) is generally thought to have gone to Italy around 1507–08, so he was probably not there at the discovery. The answer, wrong answers and hints check out.
- **q-15243** (classic-literature) In which centuries were the ballads of the Romancero viejo, such as the one about Count Arnaldos, composed? → 14th and 15th centuries: Source: hints 1 and 3 are factually off, and the translation carries both over faithfully. Printing reached Spain around 1472, and many 15th-century ballads (the frontier ballads about the Granada war, for example) were composed after that. The Catholic Monarchs reigned from 1474, inside the 15th century, so the ballads did not all come "just before" them. Fix it in the source (for example, hint 1: "They were passed on by word of mouth and mostly written down in the 16th century"; hint 3: "It's the late Middle Ages"), then re-translate. Fact check: wrong. The answer (14th and 15th centuries) is fine, and so is the Cancionero de romances fun fact (Antwerp, c. 1547). But hint 1 is false: printing reached Spain in the 1470s, and many 15th-century ballads were composed after that. Hint 3 is also off, since the Catholic Monarchs reigned 1474–1516, within the 15th century, so the ballads were not 'just before' them.
- **q-15281** (football-clubs) Look at the photo: who wears an armband like this one during a soccer match? → The captain: The fun fact gets the toss rule wrong and doesn't match the source. Since the 2019 Laws of the Game, the team that wins the toss chooses either which goal to attack or to take the kickoff. Translate the source faithfully: “At the coin toss before the match, the captains are the ones who choose the end or the kickoff.”

## Not travelling

- **q-11222** wordplay, confirmed: Sostiene la bandera frente al ayuntamiento, las velas de un barco y las cuerdas de una guitarra. ¿Cómo se llama? → Mástil (Rests on «mástil» meaning flagpole, ship's mast and guitar neck at once; English uses three different words.)

## Stale re-translated

None.
