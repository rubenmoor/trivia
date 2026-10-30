# tr-en-13

Made by `qgen batch --translate en` on 2026-10-30 (plan 66, D-81): `colombia` questions translated into English. Generated file: don't edit by hand.

- Sources: 274 (0 stale re-translated)
- Translated: 272
- Approved: 260
- Needs work: 12
- Not travelling: 2 (2 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 475, about $38.06 at list price; $0.12 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-13&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-11 | tr-en-12 | tr-en-13 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 274 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 299 | 299 | 272 |
| not travelling |  | 1 | 1 | 2 |
| not travelling confirmed |  | 1 | 1 | 2 |
| rejected rate | ≤ 20.0 % | 0.3 % ✓ | 0.3 % ✓ | 0.7 % ✓ |
| approved |  | 281 | 286 | 260 |
| needs_work |  | 18 | 13 | 12 |
| needs_work rate | ≤ 20.0 % | 6.0 % ✓ | 4.3 % ✓ | 4.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 5.4 % ✓ | 3.7 % ✓ | 4.4 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.4 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.7 % ✓ | 0.7 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 91.7 % ✓ | 96.7 % ✓ | 95.0 % ✓ |
| cost $ |  | $27.60 | $28.57 | $31.57 |
| $ per approved |  | $0.10 | $0.10 | $0.12 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 57 (0 %)
- Major among review needs work: 0 of 3 (0 %)
- Problems by kind: giveaway 7 (0 major), fact 5 (0 major), ambiguity 1 (0 major), media 1 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $6.49

Major findings on approved questions:

None.

## Needs work

- **q-7019** (carnivals-and-fairs) On January 5 in Pasto, people paint your face black. According to tradition, who asked for that day off in colonial times? → Enslaved Africans: Fact check: uncertain. The core is right: Jan 5 is Día de los Negros, and enslaved people are said to have been given a day off. But the 1607 revolt and the Spanish Crown granting it appear in only some popular sources (Radio Nacional, Sitio Andino). Academic and local sources don't back it up, and El Tiempo gives 1854. The hint 'It was in the 17th century' and the fun fact depend on that shaky date. Some accounts also place the origin in Popayán.
- **q-7049** (ghosts-and-creatures) According to popular tradition, if you sprinkle holy water in the corners of your house, who runs away? → Witches: Fact check: uncertain. In Colombian and Latin American tradition, holy water in the corners of a house usually drives away evil spirits, the devil or bad energies. Witches are not the standard answer. I did not verify this by search, so the claim that witches flee is shaky. The hints about broomsticks and night flight are generic witch lore, not Colombian tradition.
- **q-7180** (telenovelas) In “Pasión de gavilanes,” Norma, Jimena and Sara live at Hacienda Elizondo until the Reyes brothers arrive. What fictional town is it in? → San Marcos: source: the fun fact says “Pasión de gavilanes” was coproduced by Telemundo and Caracol. As far as I know, the producers were Telemundo and RTI Colombia, and Caracol was only the Colombian broadcaster. The translator flagged the same doubt, and the fact check covered only the town. Correct the source fun fact (e.g. “coproduced by Telemundo and RTI”) or drop the coproducer clause, then re-sync the translation.
- **q-7363** (languages) In Colombia, what short, affectionate word do you use for the man who runs the corner store? → Veci: Fact check: uncertain. 'Veci' as a Colombian term for the corner-store owner is plausible, but I found no source for it. 'Tendero' or 'don' are the standard terms.
- **q-7365** (mountains-and-landscapes) It falls from the clouds on stormy afternoons, pounds on zinc roofs and can turn the streets white. What falls in a hailstorm? → Balls of ice: source: the fun fact's claim that ice piled up to "almost a meter" in the November 3, 2007 Bogotá hailstorm is unconfirmed. The fact check found the storm but no source for the depth, and I can't confirm it either. The translation renders the source faithfully, so the source needs softening first, for example: "a hailstorm hit Bogotá so hard that ice buried streets and dozens of cars." Fact check: uncertain. The Nov 3, 2007 Bogotá hailstorm is real, but I found no source for 'almost a meter (3 ft)' of ice. Sources only say streets were buried and dozens of cars were covered. The answer and wrong answers are fine.
- **q-7416** (scientists-and-inventors) The 20,000-peso bill shows Julio Garavito and a drawing of the Moon, and a lunar crater bears his name. Why? → Because he studied the Moon's motion: source: the present tense is out of date in the source as well as the translation. The current 20,000-peso bill (2016 family) shows Alfonso López Michelsen, and Garavito was on the earlier design. The source should say "the old 20,000-peso bill showed" or similar, and the translation should then follow. The translation is otherwise faithful.
- **q-7821** (home-school-and-paperwork) It stays at the bottom of the rice pot, comes out toasted and crunchy, and families fight over it. What is it called in Colombia? → Pegao: source: the fun fact is unverified. Neither the fact check nor I can confirm that electric rice cookers leave almost no pegao, or that this is why many people still cook rice in a regular pot. The source should soften or replace it, for example with a fact about the regional names pega and cucayo. The answer itself is fine: pegao is a widely used Colombian word, and the regional variants pega and cucayo are not among the options. Fact check: wrong. The main weakness is that Colombia has several regional names for this, so the question has more than one defensible answer. Cucayo (Caribbean coast) and pega (Andean region) are the most common; pegao is also used on the coast. The wrong answers are fine: chicharrón and calentado are different foods, and I found no source that lists 'cuncho' in Colombia (it looks like a variant of the Panamanian 'concho' or of 'concón'). Hint 1 ('Its name tells you where it stays') is inaccurate, because 'pegao' means 'stuck', not 'at the bottom'. Hint 3 ('stuck to the pot') gives the answer away. I couldn't verify the fun fact about electric rice cookers.
- **q-7870** (places-and-monuments) Torre Colpatria in downtown Bogotá has 50 floors, stands 196 m (643 ft) tall and glows with colored lights at night. What is it mainly used for? → Offices: Fact check: wrong. The fun fact is off. The Torre Colpatria stair race is usually quoted as 980 steps over 48 floors, so 'nearly 1,000' is about right for that source. The race is also not clearly 'every year', and one source gives 943 steps for 50 floors. The step count is inconsistent across sources. Height (196 m), 50 floors and office use are right.
- **q-8104** (telenovelas) In 2001, which telenovela continued the story of Betty and Armando after the ending of “Yo soy Betty, la fea”? → Ecomoda: source: the fun fact is inaccurate, and the translation repeats it faithfully. Terramoda was a shell company set up by the Ecomoda executives (Armando and Mario) to absorb Ecomoda and keep it from the banks, with Betty only its figurehead manager; she did not use it herself to protect assets. Suggested text for the source: “Terramoda, one of the wrong options, was the shell company created to absorb Ecomoda and shield it from the banks, with Betty named as its general manager.” Fact check: uncertain. The answer (Ecomoda) is right. The fun fact is inaccurate: Terramoda was a shell company set up by the Ecomoda executives to absorb Ecomoda and stop the banks seizing it. Betty was only its figurehead general manager, and she did not use it to protect assets.
- **q-8225** (popular-and-andean-music) I'm a pasillo paisa heard at every wedding, graduation and birthday, and I make parents cry. What song am I? → “El camino de la vida”: source: the fact check says “El camino de la vida” is a bambuco, not a “pasillo paisa”, and I can't confirm the genre from my own knowledge. The error comes from the Spanish source, which the translation follows faithfully. Correct the source by dropping the genre (“canción paisa”), or use “bambuco” if verified, then retranslate. Fact check: wrong. The question calls the song a 'pasillo paisa', but sources describe 'El camino de la vida' as a bambuco, not a pasillo. The answer, author (Héctor Ochoa) and 'song of the 20th century' (1999 Academia Colombiana de Música poll) are correct. Wrong answers are other songs.
- **q-8302** (regional-speech) In Barranquilla, if someone says “¡qué pava!”, what are they complaining about? → Bad luck: source: the fact check is uncertain and I can't settle it. “Pava” as bad luck is solid, but Caribbean-coast “qué/cule pava” is reported to also mean something boring or annoying, so the wrong answer “Boredom” may be defensible. The fun fact's “echa la pava” (to bring bad luck) is also unconfirmed for the coast. The source needs checking with a Barranquilla speaker, then a replacement for “Boredom” (e.g. a concrete complaint such as noise) and a fun fact without “echa la pava” if unsupported; the English translation then follows. Fact check: uncertain. Sources say Colombian 'pava' = bad luck (tener pava, pavoso), but on the Caribbean coast 'pava' (e.g. 'cule pava') is also used for something boring or annoying, so the 'Boredom' distractor may be arguably right. The fun fact 'echa la pava' for bringing bad luck is unsupported; one dictionary gives 'echar la pava' as 'to vomit'.
- **q-8394** (crafts-and-traditional-dress) In the outfit of the paisa arriero (muleteer), what is the poncho? → A cloth worn over the shoulder: Fact check: uncertain. Sources agree that the poncho is worn on the shoulders. One says it is called a ruana in Antioquia. They do not clearly say it is a cloth. The wrong answers (carriel, hat, alpargatas) are correct as wrong answers.

## Not travelling

- **q-6939** about_language, confirmed: «Tú vienes» es a «¡Ven!» como «vos venís» es a… → «¡Vení!» (Asks how a Spanish imperative is conjugated in voseo; pure Spanish grammar.)
- **q-8227** about_language, confirmed: Así decían «yo traje» en tiempos de Cervantes, y en el campo de Boyacá todavía me oyes: «le ___ unas papitas, sumercé». ¿Qué palabra soy? → «Truje» (Asks for an old past-tense form of “traer”; the wrong options and vowel hints only work as Spanish conjugation.)

## Stale re-translated

None.
