# tr-en-2

Made by `qgen batch --translate en` on 2026-10-24 (plan 66, D-81): `base` questions translated into English. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 291
- Approved: 282
- Needs work: 9
- Not travelling: 9 (9 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 704, about $30.36 at list price; $0.10 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-en-2&locale=en

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-en-1 | tr-en-2 |
|---|---|---:|---:|
| sources |  | 50 | 300 |
| stale re-translated |  | 0 | 0 |
| translated |  | 49 | 291 |
| not travelling |  | 1 | 9 |
| not travelling confirmed |  | 1 | 9 |
| rejected rate | ≤ 20.0 % | 2.0 % ✓ | 3.0 % ✓ |
| approved |  | 49 | 282 |
| needs_work |  | 0 | 9 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | 3.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.7 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 2.1 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 49 | 60 |
| audit/review agreement | ≥ 90.0 % | 83.7 % ✗ | 96.7 % ✓ |
| cost $ |  | $5.55 | $27.69 |
| $ per approved |  | $0.11 | $0.10 |
| **health** | | ✗ fail | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 58 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 3 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 58 of 60 (97 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.67

Major findings on approved questions:

None.

## Needs work

- **q-0274** (basketball) When basketball was invented in 1891, what was hung on the gym walls for players to shoot the ball into? → Peach baskets: The translation replaced the source's wrong answers (apple crates, milk buckets, fishing nets) with laundry, bread and egg baskets, even though the notes say the source options were kept. Because Peach baskets is now the only fruit container among the options, hint 2 ("They were used to carry fruit") gives the answer away. Make one wrong answer another fruit container, e.g. "Apple baskets", or keep the source's "Apple crates". Alternatively, rewrite hint 2 so it doesn't single out fruit.
- **q-0743** (cats) My name is Muezza. The story goes that I fell asleep on my owner's sleeve, and he cut it off rather than wake me. Who was my owner? → Muhammad: Fact check: uncertain. The question says "The story goes", so the answer Muhammad matches the popular legend, and the wrong answers are wrong. But the story is not in any verified hadith. Scholars say it probably comes from a tale about the saint Ahmad al-Rifa'i (d. 578 AH), and the cat is not named Muezza there. The fun fact about cats being loved and allowed in mosques is broadly true. The hint "He is a very important religious figure" is vague but fine.
- **q-1538** (hip-hop-and-rap) I'm a street dance named after the “pop” the body makes. What move is my base? → Tensing and releasing muscles in a flash: Hint 1 ("When you watch me, the dancer can look like a robot.") keeps the first-person voice of the source riddle ("Soy un baile…"). The English question isn't in the first person, so "me" doesn't refer to anything. Reword it, e.g. "Watching it, the dancer can look like a robot."
- **q-2146** (rugby) Which team, captained by Martin Johnson, won in Sydney in 2003 to become the first Northern Hemisphere Rugby World Cup champion? → England: Fact check: wrong. The answer (England), wrong answers, hints and fun fact all check out. England beat Australia 20-17 after extra time in Sydney in 2003. Johnson captained them, and Wilkinson kicked the winning drop goal. England wear a white shirt with a red rose and play at Twickenham. Johnson is 6 ft 7 in (2.01 m) and coached England from 2008 to 2011. The problem is the description, 'so tall he had to bend down during matches just to see the ball'. It is an unsupported, implausible claim and not a real fact. Also, answer_kind is 'place' but the answer is a team.

## Not travelling

- **q-0975** needs_local_knowledge, confirmed: Soy una canción infantil de los años cuarenta. Hablo de una vaca que no es una vaca cualquiera, porque da leche merengada. ¿En qué país nací? → España (“La vaca lechera” is a Spanish-language children's song known only in the Spanish-speaking world; English-speaking players have never heard it, and the hints rely on that background, so it's unfair rather than just harder.)
- **q-1248** needs_local_knowledge, confirmed: Completa: 'Sana, sana, colita de rana, si no sana hoy, sanará…' → Mañana (This is a Spanish-language family rhyme that English speakers don't know, and finding the answer depends on the rhyme "rana"/"mañana", which is lost in translation.)
- **q-2091** about_language, confirmed: ¿Qué es un saltimbanqui? → Un acróbata que actúa en la calle (Asks what the Spanish word “saltimbanqui” means. The wrong answers and the description play on its Spanish parts (saltar = jump, banco = bench), which mean nothing in English. The English “saltimbanque” is rare and doesn't carry that wordplay.)
- **q-1998** about_language, confirmed: Soy una expresión: si alguien dice «hace un tiempo de perros», ¿de qué está hablando? → De un clima muy malo (The question asks what the Spanish idiom “hace un tiempo de perros” means, and hint 1 plays on “tiempo” meaning both time and weather. English has no common dog idiom for bad weather. “Raining cats and dogs” would change the fact and repeat the source's fun fact, and “dog days” means hot weather, so it would give the wrong answer.)
- **q-0711** needs_local_knowledge, confirmed: Adivina: soy una ronda infantil. Hablo de un patio que se moja cuando llueve, pongo a todos a agacharse y, al final, canto una lista. ¿De qué es esa lista? → Letras del abecedario (The question is about “El patio de mi casa”, a Spanish-language children's ring song. English-speaking families don't know it, and there's no English song to swap in, because the clues and hints quote its Spanish lyrics.)
- **q-1498** about_language, confirmed: El 'Lightning McQueen' de 'Cars' es 'Rayo McQueen' en español. Del mismo modo, 'Speed Racer' es… → Meteoro (Asks for the Latin American Spanish name of Speed Racer (“Meteoro”). In English the question is just the show's own title, so it only works as a question about Spanish dubbing.)
- **q-0958** about_language, confirmed: Si alguien dice que estás "matando moscas a cañonazos", ¿qué quiere decir? → Usar algo exagerado para un problema pequeño (The question asks what the Spanish saying “matar moscas a cañonazos” means. English has no saying about flies and cannons. The nearest one, “using a sledgehammer to crack a nut”, is mostly British, has no insect in it (the subcategory is Insects), and doesn't match the cannon image, the hints or the flyswatter fun fact.)
- **q-2196** about_language, confirmed: Las invitadas a las bodas reales británicas suelen llevar este sombrero femenino de ala muy ancha. ¿Cómo se llama? → Pamela (The question asks for the Spanish name of a wide-brimmed hat (“pamela”). English has no common equivalent: “Pamela hat” is an obscure Victorian bonnet term, and “picture hat” or “cartwheel hat” would break hint 3 and the fun fact about Richardson's novel. Hint 3 also plays on a Spanish word.)
- **q-1163** needs_local_knowledge, confirmed: Su protagonista es Plácido López, se estrenó en 2007 y trata de una familia numerosa apretada en un apartamento pequeño. ¿De qué país es la comedia «Una familia de diez»? → México (“Una familia de diez” is a Mexican Televisa sitcom that is well known only in Latin America; English-speaking families around the world wouldn't know it, so the question would just be a guess.)

## Stale re-translated

None.
