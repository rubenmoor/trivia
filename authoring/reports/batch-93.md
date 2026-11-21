# batch-93

Made by `qgen batch` on 2026-11-20 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (27): spring-festival, eight-cuisines, provinces, world-heritage-sites, renminbi-and-old-coins, dynasties-overview, creation-myths, confucianism, chinese-characters, giant-panda, ancient-chinese-maths, tang-poems, chinese-fables, chinese-folk-music, calligraphy, chinese-cartoons, chinese-video-games, chinese-tech-brands, china-at-the-olympics, board-and-tile-games, mid-autumn-festival, city-snacks, chinese-cities, scenic-areas, early-china, folktales, daoism
- Merged: 55 (q-22226…q-22280)
- Approved: 50
- Needs work: 5
- Dropped by the pipeline: 13
- Reviewed by: claude-opus-5-5
- Claude calls: 213, about $19.34 at list price; $0.39 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-91, batch-92; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-91 | batch-92 | batch-93 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | batch |
| drafts |  | 2 | 0 | 68 |
| skipped slots |  | 0 | 0 | 13 |
| dropped |  | 1 | 0 | 13 |
| drop rate | ≤ 20.0 % | 50.0 % ✗ | n/a | 19.1 % ✓ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 0 | 0 | 6 |
| dropped: overlap |  | 1 | 0 | 6 |
| dropped: duplicate |  | 0 | 0 | 1 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 1 | 0 | 55 |
| approved |  | 1 | 0 | 50 |
| needs_work |  | 0 | 0 | 5 |
| needs_work rate | ≤ 20.0 % | 0.0 % ✓ | n/a | 9.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | n/a | 3.6 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | n/a | 3.6 % ✓ |
| media: no pick in review 1 |  | no | n/a | 10 |
| media: recovered by research |  | no | n/a | 8 |
| media: no pick at record |  | yes | n/a | 2 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | n/a | 1.8 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | n/a | 0.0 % ✓ |
| problems guessed |  | n/a | n/a | no |
| overlap rate | ≤ 20.0 % | 50.0 % ✗ | n/a | 10.3 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | 61.1 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | 0.80 ✓ |
| approved 11–15 |  | 1 | 0 | 9 |
| top move | ≤ 25.0 % | n/a | n/a | 18.2 % ✓ |
| values move |  | n/a | n/a | 14 |
| top stimulus |  | n/a | n/a | 85.5 % |
| values stimulus |  | n/a | n/a | 4 |
| top clue | ≤ 60.0 % | n/a | n/a | 43.6 % ✓ |
| values clue |  | n/a | n/a | 5 |
| top answer_kind | ≤ 40.0 % | n/a | n/a | 23.6 % ✓ |
| values answer_kind |  | n/a | n/a | 7 |
| top lens | ≤ 25.0 % | n/a | n/a | 18.2 % ✓ |
| values lens |  | n/a | n/a | 10 |
| giveaway-step drop rate |  | 0.0 % ✓ | n/a | n/a |
| mechanical-check rate |  | 0.0 % ✓ | n/a | n/a |
| media share | 15.0 %–50.0 % | n/a | n/a | 14.5 % ✗ |
| mean fun | ≥ 3.40 | 3.50 ✓ | n/a | 3.50 ✓ |
| cost $ |  | $4.74 | $0.42 | $16.87 |
| $ per approved | ≤ $0.35 | $4.74 ✗ | n/a | $0.34 ✓ |
| calls |  | 62 | 5 | 158 |
| calls per approved |  | 62.00 | n/a | 3.16 |
| wall time h |  | 0.24 | 0.04 | 0.98 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✓ pass | ✗ fail |

Deficit to the targets (chinese-base, approved now): 1: 233, 2: 326, 3: 415, 4: 401, 5: 400, 6: 376, 7: 378, 8: 401, 9: 296, 10: 261, 11: 307, 12: 207, 13: 224, 14: 136, 15: 137

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 50 (0 %)
- Major among review needs work: 2 of 5 (40 %)
- Problems by kind: giveaway 7 (1 major), media 2 (2 major), style 5 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 55 (0 %)
- Audit/review agreement (both accept or both not): 52 of 55 (95 %)
- Sample: 55 audited of 55; 55 Claude calls, about $2.47

Major findings on approved questions:

None.

## Needs work

- **q-22233** (chinese-cities) Li Bai's poem 蜀道难 (Shǔ dào nán, “The Road to Shu Is Hard”) is about the road into the region highlighted on this map. Which province is it today? → Sichuan: None of the candidates is the essential image the question needs: an unlabelled map of China with only Sichuan highlighted. No new search is allowed. Candidate 6 prints 四川 / Sichuan, 4 shows a big 四川 SICHUAN sign, 3 labels Chengdu and highlights nothing, and 1, 2 and 5 aren't maps. Try a fresh search such as "Sichuan locator map China" or "China Sichuan location map". No suitable picture found for this question.
- **q-22235** (chinese-fables) In the song 小兔子乖乖 (“Little Rabbits, Be Good”), the big bad wolf sings Mother Rabbit's song at the door. Why won't the little rabbits open it? → Mum hasn't come back yet: The answer uses "Mum", a UK-only word. The chinese-base voice doesn't set a spelling, so the general en rule applies: use the US word or reword around it. Change the answer to "Their mom hasn't come back yet", or better, to a neutral "Their mother isn't back yet". Everything else is fine: the song's reply line 妈妈没回来 confirms the answer, and the description doesn't give it away.
- **q-22257** (folktales) In the Chinese children's story, a little horse carries a sack of wheat to the mill. What does he have to cross on the way? → A river: Hint 2 ("very deep" vs. "very shallow") gives the answer away: of the four options, only a river can be deep or shallow, so it settles the question before hint 3. Hint 2 should hint at the advice without the words deep and shallow, for example by saying that the two animals give opposite advice because they are such different sizes. The mountain, desert and forest options all stay possible that way.
- **q-22261** (provinces) Car number plates from the province highlighted on this map begin with which character? → 川 (chuān): The essential map is missing. The question depends on a blank map of China with only Sichuan highlighted, but none of the six candidates shows one, and no new search is allowed. The text is fine; the slot needs an unlabelled Sichuan locator map, for example "Sichuan locator map China" on Commons. No suitable picture found for this question.
- **q-22264** (ancient-chinese-maths) Suzhou numerals (苏州码子), also called “grass numerals” (草码), grew out of the old counting rods. What were they mainly used for? → Writing prices and accounts in shops: Hint 2 gives the answer away. It says you can still see these numerals on handwritten signs in Hong Kong wet markets and medicine shops, and only one option mentions shops. Rewrite hint 2 so it stays vaguer, for example by saying the numerals were written by ordinary working people rather than by scholars or officials, without naming markets, shops, signs or prices.

## Question axes

- move: cause_effect 4, count 3, estimate 2, identify 10, made_of 3, name_concept 4, odd_one_out 3, origin 2, purpose 2, record 1, sequence 5, when 6, who 7, word_meaning 3
- stimulus: detail 1, map_outline 3, none 47, photo 4
- clue: completion 1, direct 24, riddle 9, scenario 9, three_facts 12
- answer_kind: group 4, number 6, person 9, place 6, thing 10, time 7, word 13
- lens: body_senses 1, educational_media 7, everyday 10, history 6, language 4, nature 3, pop_culture 6, school 9, science_news 3, university 6

## Dropped by the pipeline

- china-at-the-olympics-1: overlap like q-0857: ¿En qué año fueron los Juegos Olímpicos de Sídney, donde se hizo famoso el nadador Eric Moussambani? → 2000: In 1993 I beat Beijing by just two votes to host the 2000 Summer Olympics. Which city am I? → Sydney
- chinese-cartoons-2: overlap like q-2362: I hang above the street next to red and yellow lights. When I glow green, what do cars do? → Go: Complete: “A red traffic light is to ‘stop’ as a green traffic light is to…” → Go
- chinese-fables-2: overlap like q-5380: The fable of the town mouse and the country mouse is said to come from Aesop, who also told “The Tortoise and the Hare”. Where did Aesop live? → Ancient Greece: A dog carrying meat sees its reflection in the water, snaps at the “other” piece and loses its own. Where does this fable come from? → Ancient Greece
- city-snacks-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I come alive after dark. Under my strings of lights, people eat skewers, crayfish and stinky tofu as a 夜宵 (yèxiāo, late-night snack). Where am I? → A night market (夜市)
- eight-cuisines-1: overlap like q-2723: Legend says I was born when a leaf fell into a Chinese emperor's cup of hot water. Which drink am I? → Tea: Legend says Shennong (神农) tasted hundreds of wild plants, and one day leaves fell into his pot of boiling water. Which drink did he discover? → Tea
- folktales-1: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: In Disney's 1998 film Mulan, she grabs the last rocket in a mountain pass. She fires it at the snowy mountainside, not at Shan Yu, and the Hun army is stopped. What did the rocket set off? → An avalanche
- giant-panda-1: overlap like q-9361: In diesem Zoo wurde Eisbär Knut weltberühmt, und er ist Deutschlands ältester Zoo. In welcher Stadt steht er? → Berlin: Meng Meng and Jiao Qing (梦梦 and 娇庆) arrived at this zoo in 2017. In 2019 they had twins, the first pandas ever born in Germany. Which city is the zoo in? → Berlin
- calligraphy-2: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Tang Emperor Muzong asked calligrapher Liu Gongquan how to use a brush well. Liu answered, “If the heart is upright, the brush is upright.” What did he mean? → A warning to the emperor to rule honestly
- city-snacks-0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: This street stall opens before sunrise, smells of hot frying oil and sells youtiao (油条) with warm soy milk. What is it? → A breakfast stall (早点摊)
- early-china-1: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: This Shang dynasty turtle shell is covered in cracks and carved characters. What was it used for? → Asking the ancestors about the future
- scenic-areas-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Plaques line Hong Kong's Avenue of Stars on the Victoria Harbour waterfront. What kind of people do they honour? → Film stars and filmmakers
- world-heritage-sites-2: duplicate like q-4311: This statue in India was the world's tallest when it opened in 2018. What covers its outside? → Bronze: This mask with eyes that stick far out was found at Sanxingdui (三星堆) in Sichuan. What is it made of? → Bronze
- scenic-areas-2: overlap like q-19992: Glencoe in the Scottish Highlands is a deep, steep-sided valley shaped like a U. What carved it out long ago? → Glaciers: Kanas Lake (喀纳斯湖), shown here in Xinjiang's Altai Mountains, lies in a valley that was shaped by what? → Glaciers
