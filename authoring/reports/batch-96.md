# batch-96

Made by `qgen batch` on 2026-11-27 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (111): ethnic-groups, chinese-rivers-and-lakes, china-at-the-olympics, dynasties-overview, chinese-cinema, chinese-birds-and-water-life, chinese-land-animals, chinese-kitchen, martial-arts, farming-and-silk, popular-chinese-fiction, provinces, classic-tv-series, chinese-video-games, table-tennis-and-badminton, peoples-republic, idiom-stories, chinese-consumer-brands, swimming, chinese-folk-music, world-cups, chinese-fables, mythical-creatures, team-sports-in-china, guinness-world-records, late-qing-and-republic, mega-projects, modern-tv-dramas, traditional-puzzles, customs-and-etiquette, spring-festival-gala, childrens-games, climate-and-regions, scenic-areas, dream-of-the-red-chamber, china-transport, hundred-schools, fast-food, diving-and-gymnastics, chinese-opera, chinese-cartoons, silk-road-and-voyages, ancient-chinese-maths, calendar-and-solar-terms, classical-prose, qin-and-han, song-and-yuan, chinese-cities, song-ci, apps-and-online-life, toys, giant-panda, chinese-plants-and-flowers, hong-kong-cinema, other-traditional-festivals, science-fiction, nursery-rhymes, four-great-inventions, city-snacks, folktales, noodles-and-dumplings, calligraphy, spring-festival, gods-and-immortals, three-kingdoms-to-sui, c-pop, chinese-animated-films, landforms-and-deserts, world-heritage-sites, chinese-mountains, chinese-tech-brands, chinese-zodiac, lunar-and-planetary-missions, folk-crafts, renminbi-and-old-coins, mid-autumn-festival, qing-dynasty, chinese-medicine-history, drinks, early-china, creation-myths, tang-poems, crewed-spaceflight, school-and-daily-life, water-margin, modern-chinese-literature, ming-dynasty, cartoons, chinese-sports-stars, nature-reserves-and-hazards, chinese-scientists, imperial-exams-and-gaokao, space-race-and-astronauts, tea-and-drinks, chinese-characters, daoism, confucianism, dialects, eight-cuisines, romance-of-the-three-kingdoms, traditional-architecture, journey-to-the-west, capital-cities, chinese-painting, bronzes-and-porcelain, board-and-tile-games, tang-dynasty, chinese-buddhism, solar-system, stars-and-galaxies, famous-scientists
- Merged: 126 (q-28047…q-28172)
- Approved: 109
- Needs work: 17
- Dropped by the pipeline: 46
- Reviewed by: claude-opus-5-5
- Claude calls: 518, about $54.32 at list price; $0.50 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-94, batch-95; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-94 | batch-95 | batch-96 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | batch |
| drafts |  | 1473 | 1346 | 172 |
| skipped slots |  | 345 | 472 | 53 |
| dropped |  | 201 | 253 | 46 |
| drop rate | ≤ 20.0 % | 13.6 % ✓ | 18.8 % ✓ | 26.7 % ✗ |
| dropped: hard fail correct |  | 7 | 5 | 0 |
| dropped: hard fail unambiguous |  | 4 | 2 | 0 |
| dropped: hard fail no_giveaway |  | 60 | 57 | 8 |
| dropped: overlap |  | 128 | 185 | 37 |
| dropped: duplicate |  | 4 | 2 | 0 |
| dropped: fact-check wrong |  | 3 | 4 | 1 |
| merged |  | 1272 | 1093 | 126 |
| approved |  | 1123 | 973 | 109 |
| needs_work |  | 149 | 120 | 17 |
| needs_work rate | ≤ 20.0 % | 11.7 % ✓ | 11.0 % ✓ | 13.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 3.8 % ✓ | 3.9 % ✓ | 6.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.1 % ✓ | 1.2 % ✓ | 1.6 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.2 % ✓ | 0.1 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.2 % ✗ | 1.1 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 5.9 % ✓ | 5.5 % ✓ | 3.2 % ✓ |
| media: no pick in review 1 |  | 204 | 227 | 19 |
| media: recovered by research |  | 138 | 173 | 15 |
| media: no pick at record |  | 69 | 54 | 4 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 1.2 % ✓ | 0.5 % ✓ | 4.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.2 % ✓ | 0.1 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 10.0 % ✓ | 14.8 % ✓ | 21.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 68.3 % ✓ | 57.4 % ✓ | 61.6 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 0.90 ✓ | 1.51 ✗ | 1.18 ✓ |
| approved 11–15 |  | 197 | 209 | 46 |
| top move | ≤ 25.0 % | 13.5 % ✓ | 16.1 % ✓ | 11.9 % ✓ |
| values move |  | 15 | 15 | 15 |
| top stimulus |  | 84.7 % | 82.0 % | 85.7 % |
| values stimulus |  | 6 | 6 | 4 |
| top clue | ≤ 60.0 % | 44.4 % ✓ | 46.1 % ✓ | 42.1 % ✓ |
| values clue |  | 5 | 5 | 4 |
| top answer_kind | ≤ 40.0 % | 22.2 % ✓ | 20.3 % ✓ | 23.0 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 17.1 % ✓ | 18.0 % ✓ | 17.5 % ✓ |
| values lens |  | 11 | 11 | 11 |
| giveaway-step drop rate |  | n/a | n/a | n/a |
| mechanical-check rate |  | n/a | n/a | n/a |
| media share | 15.0 %–50.0 % | 15.3 % ✓ | 18.0 % ✓ | 14.3 % ✗ |
| mean fun | ≥ 3.40 | 3.64 ✓ | 3.63 ✓ | 3.37 ✗ |
| cost $ |  | $335.43 | $320.81 | $50.80 |
| $ per approved | ≤ $0.35 | $0.30 ✓ | $0.33 ✓ | $0.47 ✗ |
| calls |  | 2440 | 2207 | 458 |
| calls per approved |  | 2.17 | 2.27 | 4.20 |
| wall time h |  | 5.46 | 4.80 | 1.46 |
| days |  | 2 | 2 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets (chinese-base, approved now): 1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 11

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 52 (0 %)
- Major among review needs work: 0 of 8 (0 %)
- Problems by kind: giveaway 6 (0 major), overlap 1 (0 major), media 2 (0 major), difficulty 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 60 (2 %)
- Audit/review agreement (both accept or both not): 52 of 60 (87 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.53

Major findings on approved questions:

None.

## Needs work

- **q-28057** (chinese-cinema) You wake up in 1981, like Jia Ling's character in Hi, Mom (你好，李焕英). Which of these would you NOT see there? → A smartphone: No candidate shows the question's world (China around 1981 / Hi, Mom), and no new search is allowed. #1 is a solar cooker on a Cornish beach, #2 is a cluttered Western-style antiques shop with mugs that could suggest a wrong option, and #3 is a staged still life of vintage cameras and books. The text is fine. The slot needs a new search such as "1980s China street bicycles". It would also work without bicycles, e.g. "Chinese vintage thermos flask" on Commons, or "1980s Chinese factory dormitory". No suitable picture found for this question.
- **q-28060** (chinese-fables) In Aesop's fable, a farmer cuts open his goose that lays golden eggs to get all the gold at once. Which fault does the story warn against? → Greed: This question doesn't fit the chinese-base bundle. It asks about Aesop's fable, a European story known worldwide, and the bundle requires questions answerable without any connection to Europe. World-famous facts belong in base. Either move it to base or rebuild it around a Chinese fable or idiom with the same lesson. The fun fact already points to 杀鸡取卵 (shā jī qǔ luǎn), which could be the starting point. If it moves to base, candidate 5 (white goose) fits as the illustrative image.
- **q-28067** (chinese-painting) Tang painter Zhang Zao (张璪) said to learn from nature and from the heart, and painted pines holding two brushes at once. What was each brush for? → One for a living branch, one for a dead branch: Hint 2 (“a pine that was both young and old at once”) gives away living vs. dead branches: of the four options, only the answer fits it. It is also a stronger hint than hint 3, which only names the idiom. Rewrite hint 2 as a vaguer clue, for example about the two brushes working at the same moment, and keep the young/old idea out of it.
- **q-28075** (creation-myths) China's solar observatory ASO-S went up from Jiuquan in October 2022 and studies solar flares and the Sun's magnetic field. Which mythical figure is it named after? → Kuafu (夸父): Fact check: wrong. ASO-S (Kuafu-1) was launched on 9 Oct 2022 from Taiyuan Satellite Launch Center, not Jiuquan. This is from memory; I did not run a search to confirm.
- **q-28078** (dialects) Dungan, a Mandarin dialect of Hui Muslims, is written in Cyrillic letters. It is spoken in neighboring Kazakhstan and in this country. Which country is it? → Kyrgyzstan: The media slot is set to "essential" and asks for an outline map of Kyrgyzstan. But the question text never mentions a map, so showing the answer country's shape sharp on the TV is a giveaway. The slot should be illustrative (for example "Dungan people" or "Tian Shan mountains", nothing that names the country), and a new search is needed. The text, the facts and the options are fine. No suitable picture found for this question.
- **q-28092** (giant-panda) Born at Chapultepec Zoo in Mexico City in 1981, this cub became a national star. It was the first giant panda born outside China that survived. What was its name? → Tohui: This breaks the chinese-base bundle rule. It asks for the name of a panda cub born at a Mexican zoo, and Chinese families don't learn that at school or in daily life. The question needs knowledge of Mexico (Chapultepec Zoo, a Rarámuri name), so it belongs in `base`, or it should be dropped.
- **q-28096** (hong-kong-cinema) Chang Cheh's The One-Armed Swordsman (独臂刀) was the first Hong Kong film to earn HK$1 million at the box office. In which year did it come out? → 1967: Hints 1 and 2 together give the answer away. Hint 1 ("before Bruce Lee's big films", 1971–73) rules out 1972 and 1978. Hint 2 ("same decade the Cultural Revolution began", the 1960s) then leaves only 1967 or 1962. Hint 3 names the 1967 riots, so it states the year outright. The hints need rewording so the first two don't narrow the options down this far. Also, a difficulty of 15 that rests only on a minor release year goes against the house style.
- **q-28097** (hong-kong-cinema) Under the CEPA trade deal (内地与香港关于建立更紧密经贸关系的安排), Hong Kong–mainland co-productions no longer count as imported films. In which year was CEPA signed? → 2003: Hint 2 gives the answer away. Hint 1 already rules out 1997, and hint 2 ("early in the 21st century, a few years before the Beijing Olympics") then rules out both 2008 and 2012, so 2003 is the only option left before hint 3. Hint 2 should be vaguer, for example one about the era of the Hong Kong film industry's slump in the early 2000s, but without anything that removes all the remaining wrong options.
- **q-28121** (capital-cities) This close-up shows part of a famous orange-and-white tower. In which city does it stand? → Tokyo: The question is about a world-famous landmark in Japan and needs nothing China-centred. The chinese-base bundle rule says well-known facts about any country belong in `base`, so move it there or drop it. Also, hint 3 points to 东 (east) in the Chinese name; in zh, 东京 is the answer itself, so that hint nearly spells it out.
- **q-28125** (chinese-consumer-brands) Pickles like these are the pride of Liubiju (六必居), a shop said to date back to the Ming dynasty. In which city is it? → Beijing: The question says “Pickles like these”, so the image must show Chinese sauce-pickled vegetables (jiangcai, 酱菜), but no candidate does. A new search isn't allowed, so the media slot has to be filled another way, for example by searching “Chinese jiangcai pickles” or “Beijing sauce pickles”. The other option is to reword the question so it doesn't point at a picture. No suitable picture found for this question.
- **q-28129** (chinese-mountains) The 珙桐 (gǒngtóng) grows wild in the misty mountains of Sichuan and Hubei. Chinese people call it the dove tree (鸽子树). Why? → Its white flower parts look like doves: Hints 1 and 2 together give the answer away. Hint 1 rules out the nesting and fruit options, and hint 2 ("when it blooms") points straight to the only option about flowers. Hint 2 should be reworded so it doesn't point to the flowers, for example a vague hint about the season or the tree's history, and hint 1 shouldn't rule out two options at once.
- **q-28130** (chinese-mountains) The red panda lives in the mountain forests of southwest China. Which of these is NOT true about it? → It is a close cousin of the giant panda: Hint 2 ("Three of these are about how it lives; one is about its family tree") gives the answer away: in a "which is NOT true" question, it singles out the only option that differs, so players can pick it without knowing anything. Replace hint 2 with one that doesn't separate the answer from the other options, e.g. a vague hint that its name is misleading or about where scientists place it among animals.
- **q-28136** (chinese-zodiac) Folk sayings call one zodiac animal 小龙 (xiǎolóng, “little dragon”). Which animal is it? → Snake: Hints 1 and 2 give the answer away: against Horse, Rabbit and Rooster, "It has no legs" (hint 1) and "sheds its skin and sleeps through winter" (hint 2) each point to the Snake right away. Hint 1 should be vague, for example the traits people link with this sign (wisdom, mystery), and hint 2 only a bit stronger. Hint 3 (comes after the Dragon) can stay.
- **q-28142** (hundred-schools) I'm a two-character word. Grandpa calls his son's son by me, and I'm also the name of a great general of the state of Wu. What word am I? → 孙子 (Sūnzǐ): The whole question rests on a pun in one Chinese word: 孙子 means both "grandson" and "Master Sun". The English clue "Grandpa calls his son's son by me" just translates the answer's own meaning, so English players are asked what the word says, which the chinese-base rule forbids. It also gives itself away: hint 2 names the surname Sun through Sun Wukong, which only one option has, and the description's "famous general" rules out the three other options, which are all philosophers.
- **q-28145** (martial-arts) Wang Ziping (王子平), the kung fu master from Cangzhou (沧州), belonged to three of these groups. Which one did he NOT belong to? → Shaolin monks: Fact check: uncertain. Wikipedia confirms he was Hui, vice chairman of the Chinese Wushu Association, a practitioner of traditional medicine, and head of the Shaolin division of the Martial Arts Institute (1928). That last point supports the 'Shaolin monks' answer, since he was not a monk. I could not verify bone-setting specifically. I also could not verify 'taught into his nineties', 'Central Guoshu Institute', or 'never shaved his head'. The wording 'Leaders of the Wushu Association' is loose for a vice chairman.
- **q-28149** (mythical-creatures) This close-up shows Haechi (해치), Korea's version of China's justice beast 獬豸 (xiezhi). Which city made Haechi its official symbol? → Seoul: This is about a Korean city's official symbol, not about China. The xiezhi (獬豸) link is only a hook, so the question doesn't fit chinese-base, whose rules send facts about other countries to base. Move it to base (dropping the Chinese-specific framing) or replace it with a question about the xiezhi itself, for example the judges' 獬豸冠 hat or the creature's role in Chinese law.
- **q-28156** (solar-system) “I live in the Moon Palace (广寒宫) with Chang'e, and I pound medicine with a pestle all night.” Who am I? → Jade Rabbit (玉兔): No candidate is adequate for the illustrative slot. Candidates 3–6 are shunga handscrolls (Japanese erotic art) and must never be used. Candidates 1 and 2 are daytime lake pavilions with no Moon or Mid-Autumn theme. A new search could try "Mid-Autumn full moon lantern" or "full moon over Chinese pavilion night", as long as it shows no rabbit. No suitable picture found for this question.

## Question axes

- move: analogy 3, cause_effect 13, count 2, estimate 3, identify 15, made_of 4, name_concept 7, odd_one_out 10, origin 15, purpose 11, record 5, sequence 7, when 10, who 15, word_meaning 6
- stimulus: detail 8, map_outline 2, none 108, photo 8
- clue: direct 53, riddle 13, scenario 22, three_facts 38
- answer_kind: group 14, number 7, person 29, place 15, thing 24, time 11, word 26
- lens: body_senses 6, educational_media 15, everyday 18, history 22, language 13, nature 7, pop_culture 7, popular_science 5, school 21, science_news 5, university 7

## Dropped by the pipeline

- bronzes-and-porcelain-1: overlap like q-28006: In 1974, farmers digging a well near Xi'an found thousands of life-size soldiers guarding Qin Shi Huang's tomb, each with its own face. What are they made of? → Fired clay: Farmers digging a well near Xi'an in 1974 found thousands of life-size soldiers and horses guarding the tomb of Qin Shi Huang. What are they made of? → Fired clay
- cartoons-0: overlap like q-12271: Doraemon saca de ahí el gorrocóptero y la puerta mágica. Es blanco, pequeño y lo lleva en la barriga. ¿Qué es? → Su bolsillo mágico: I'm sewn onto the belly of a blue robot cat from the 22nd century. I look tiny, but hundreds of gadgets come out of me. What am I called? → The 4D Pocket (四次元口袋)
- cartoons-1: overlap like q-0693: Mira la foto: este dulce japonés es la comida favorita de un famoso personaje de dibujos animados. ¿De quién? → Doraemon: Which cartoon character loves 铜锣烧 (tóngluóshāo, “gong cake”), two small pancakes filled with sweet red bean paste, more than anything? → Doraemon (哆啦A梦)
- childrens-games-1: overlap like q-5396: A trampoline has a frame and a stretchy mat. What pulls the mat tight around the edge so you can bounce? → Metal springs: Look at this close-up: a ring of metal springs holding a stretchy black mat. What is it part of? → A trampoline (蹦床)
- chinese-cities-1: overlap like bronzes-and-porcelain-1: Farmers digging a well near Xi'an in 1974 found thousands of life-size soldiers and horses guarding the tomb of Qin Shi Huang. What are they made of? → Fired clay: Farmers digging a well in 1974 found clay soldiers, and now tourists from all over the world come to this city, once called Chang'an. Which city is it? → Xi'an
- chinese-medicine-history-3: overlap like q-27811: Many people drop small, thin, oval dried berries like the ones in the photo into hot water or tea. What are they? → Goji berries (枸杞): I'm small, oval and bright red, and I grow on bushes in Ningxia. People dry me and drop me into tea and soup, often in a thermos flask. What am I? → Goji berry (枸杞)
- chinese-painting-2: overlap like q-4157: Look at this shadow. Which bird is it? → Peacock: Which bird, a favorite of Chinese bird-and-flower painters, opens its long tail like a giant fan full of shiny “eyes”? → Peacock (孔雀)
- chinese-plants-and-flowers-0: overlap like q-26356: Chrysanthemums bloom in late autumn, stand up to frost and stand for long life. So on Double Ninth Day (重阳节), whom do people especially honor? → The elderly: Three of these flowers bloom in spring, around Qingming (清明). Which one does NOT? → Chrysanthemum (菊花)
- chinese-tech-brands-1: overlap like q-25959: This tiny camera on a handle is the Osmo Pocket, made by the drone company DJI. Who founded DJI? → Wang Tao (汪滔): DJI (大疆) comes from Shenzhen, was started by a university student, and its products film weddings and landscapes from high above. DJI is the world's biggest maker of what? → Drones
- chinese-video-games-0: overlap like q-6753: You're playing Angry Birds and fling birds at round green creatures hiding in towers. What are those creatures? → Green pigs: The name Angry Birds (愤怒的小鸟) says the birds are angry. Which animals made them angry by stealing their eggs? → Pigs
- city-snacks-1: overlap like q-27326: Look at the photo: this fiery red dish is a summer favourite in Changsha. What is the animal in it called? → 小龙虾 (xiǎo lóngxiā, crayfish): Farmers raise me in rice paddies, and I turn red when I'm cooked with chilli. Xuyi in Jiangsu holds a festival for me, and Qianjiang in Hubei calls itself my hometown. Who am I? → 小龙虾 (xiǎo lóngxiā, crayfish)
- confucianism-1: overlap like q-26633: At age four, Kong Rong kept the smallest fruit for himself and left the bigger ones to his brothers. Which fruit? → Pears: Kong Rong is famous for giving away the bigger pears like these. He was a descendant of which great teacher? → Confucius
- dynasties-overview-0: overlap like q-25843: Anyang in Henan was the capital of the late Shang dynasty, where oracle bones were found. About how long ago was it the capital? → About 3,300 years ago: Because King Pan Geng moved the Shang capital to Yin (殷), oracle bones and Fu Hao's tomb were found there. Which modern city is it near? → Anyang
- early-china-0: overlap like q-27106: Da Yu tamed the great flood, and his son Qi started China's first dynasty. Which one? → Xia (夏): After Yu the Great (大禹), his son Qi took the throne, starting China's first dynasty. Which dynasty was it? → Xia (夏)
- guinness-world-records-0: overlap like q-2266: Ancient Egyptians threw it away when making mummies. It uses about a fifth of your body's energy. Your awareness comes from it. What is it? → The brain: It has more nerve cells than any other part of your body, the skull protects it, and it looks wrinkly like a walnut. What is it? → The brain
- idiom-stories-2: overlap like q-25793: Liu Bei said that having Zhuge Liang at his side made him feel like which idiom? → 如鱼得水 (rú yú dé shuǐ, “like a fish finding water”): Liu Bei said having Zhuge Liang was like a fish finding water, giving us 如鱼得水 (rú yú dé shuǐ). Who wrote the history 三国志 that records it? → Chen Shou (陈寿)
- journey-to-the-west-1: overlap like q-25815: I'm a kind monk who rides a white horse west to bring back holy books. A monkey, a pig and a quiet giant protect me. Who am I? → Tang Sanzang (唐三藏): “I'm a monk walking west to fetch scriptures. When my eldest disciple won't listen, I chant a spell and the gold band on his head squeezes tight. Who am I?” → Tang Sanzang (唐三藏)
- late-qing-and-republic-0: overlap like q-27428: British merchants brought it from India, it made many people sick, and Lin Zexu destroyed huge piles of it at Humen in 1839. What was it? → Opium: The emperor sent me to Guangzhou in 1839. At Humen beach I had over a thousand tonnes of opium destroyed with lime and seawater. Who am I? → Lin Zexu (林则徐)
- mega-projects-1: overlap like q-21899: Riddle: I'm the brain of the computer, I do billions of calculations per second and I live on a tiny chip. What am I made of inside? → Billions of transistors: Moore's law (摩尔定律) says the number of these tiny parts on a chip like this one doubles about every two years. What are they? → Transistors
- modern-tv-dramas-0: overlap like q-26408: You're watching Xiaoyanzi's adventures in My Fair Princess (还珠格格). In which dynasty is the story set? → Qing dynasty: You're watching Yang Mi in Palace (宫锁心玉). Her character falls back in time and meets Emperor Kangxi's sons. Which dynasty is she in? → Qing dynasty
- nursery-rhymes-0: overlap like q-18826: In “What's the time, Mr Wolf?”, the players creep up behind the wolf. What do they do when the wolf shouts “Dinner time!”? → Run back to the start: Children walk behind me asking the time, and I answer “one o'clock, two o'clock…”. When I shout “天黑了!” (“It's dark!”), I turn and chase them. Who am I? → The old wolf
- bronzes-and-porcelain-0: overlap like q-6377: I'm a shiny thing you eat cereal with. Look into my curved bowl and you see your face upside down! What am I? → A spoon: I'm made of smooth white porcelain, with a short, thick handle and a flat bottom so I can rest on the table. At dim sum, I wait beside your bowl. What am I? → A porcelain soup spoon
- china-at-the-olympics-0: overlap like q-26781: As the flag goes up at the Monday flag-raising ceremony (升旗仪式), which song do the students sing? → 义勇军进行曲 (Yìyǒngjūn Jìnxíngqǔ, “March of the Volunteers”): When a Chinese athlete wins Olympic gold, China's flag goes up the pole while a song plays. Which song is it? → 义勇军进行曲 (Yìyǒngjūn Jìnxíngqǔ, “March of the Volunteers”)
- chinese-cities-0: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: These Shanghai lane houses have stone gate frames and black wooden doors, and the CPC's First Congress met in one in 1921. What are they called? → Shikumen (石库门)
- chinese-kitchen-0: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Families hang strips of salted pork, 腊肉 (làròu), to dry before New Year. What does its 腊 refer to? → The twelfth month of the lunar year
- chinese-opera-0: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Mei Baojiu, son of Mei Lanfang, played the same kind of roles as his famous father all his life. What was he in Peking opera? → 男旦 (nándàn, “male dan”)
- chinese-scientists-1: overlap like q-27164: The Hong Kong–Zhuhai–Macao Bridge in this photo crosses the wide mouth of which river? → The Pearl River: “I cross the sea at the mouth of the Pearl River, and part of me dives into a tunnel under the sea. What am I?” → The Hong Kong–Zhuhai–Macao Bridge (港珠澳大桥)
- chinese-sports-stars-3: fact-check wrong: Fun fact is false. Le Jingyi's 1996 100 m freestyle gold was not a first for a Chinese swimmer in that event. Zhuang Yong won the Olympic 100 m freestyle at Barcelona 1992, and Le Jingyi finished 6th there. The answer (Freestyle) is correct.: In 1994 Le Jingyi set a 100 m world record, and in 1996 she won Olympic gold over the same distance. In which stroke? → Freestyle
- crewed-spaceflight-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: China cancelled its planned Tiangong-3 lab and gave its jobs to another craft, which was refueled by Tianzhou-1 in 2017 and brought down in 2019. Which craft? → Tiangong-2
- ming-dynasty-2: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: This is Tiananmen (天安门) in Beijing. In Ming and Qing times, what was it used for? → The palace's front gate
- qing-dynasty-1: overlap like song-and-yuan-0: Bao Zheng (包拯) judged cases in Kaifeng in the Northern Song. In Peking opera, his face is painted black with a white crescent moon. What does the black show? → He is honest and fair: On stage, what is the colorful face pattern (脸谱, liǎnpǔ) of this Peking opera actor usually made of? → Paint put straight on the face
- romance-of-the-three-kingdoms-0: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Zhuge Liang said the general Wei Yan had a 反骨 (fǎn gǔ) at the back of his skull. What did that mean? → He would one day turn against his lord
- school-and-daily-life-1: overlap like q-2484: In many Asian countries, what are these used for? → Eating food: Many families in China eat noodles with two thin sticks held in one hand. What are they called? → Chopsticks
- tea-and-drinks-0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: For Hakka lei cha (擂茶), tea leaves, sesame and peanuts are ground into a paste in a ridged bowl. What is poured on next to make the drink? → Hot water
- team-sports-in-china-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Coach Zhu Guanghu won the first Chinese Super League title in 2004 with a club called Jianlibao (健力宝), then became China's head coach. From which city was that club? → Shenzhen
- traditional-architecture-0: overlap like q-26100: Puyi (溥仪) became emperor at 2 and gave up the throne in 1912, but a deal with the new republic let him keep living at home until 1924. Where? → Forbidden City (故宫): In films and TV shows, Beijing's huge old imperial palace, the Palace Museum (故宫), is often called the “___ City”. Which word fills the gap? → Forbidden
- water-margin-0: overlap like q-26260: I was an army officer who became a monk on Mount Wutai, I pulled a willow tree out by its roots, and I'm often drawn carrying a heavy monk's spade. Who am I? → Lu Zhishen: In Water Margin (水浒传), idlers complain about a noisy crows' nest in a willow. Which hero pulls the whole tree out by its roots? → Lu Zhishen
- science-fiction-0: overlap like q-10631: Minions are small, wear goggles and work for Gru. Which fruit makes them shout with joy? → Banana: In “Despicable Me”, Gru's little helpers are yellow, wear goggles and talk funny. What food makes them drop everything and cheer? → Bananas
- silk-road-and-voyages-0: overlap like q-26041: In the 1986 TV series “Journey to the West”, Tang Seng heads west with a monkey, a pig and a river ogre. Who else is in the team? → A white dragon horse: In “Journey to the West”, this pilgrim gobbled up Tang Sanzang's first horse, hardly ever talks, and carries the monk all the way west. Who is it? → The White Dragon Horse (白龙马)
- song-and-yuan-0: overlap like q-28064: On the opera stage my face is painted black, with a white crescent moon on my forehead. I was a fair, honest judge in Kaifeng in the Song dynasty. Who am I? → Bao Zheng (包拯): Bao Zheng (包拯) judged cases in Kaifeng in the Northern Song. In Peking opera, his face is painted black with a white crescent moon. What does the black show? → He is honest and fair
- song-ci-0: overlap like q-28021: These paddlers race at the Dragon Boat Festival. Legend says people first paddled out on the river to save which poet? → Qu Yuan: Families eat zongzi (粽子) at the Dragon Boat Festival (端午节) to remember which ancient poet? → Qu Yuan
- song-ci-1: overlap like q-27450: The Double Ninth Festival (重阳节), when families climb hills and visit elders, falls in which season? → Autumn: You're at a park show where chrysanthemums, Tao Yuanming's favorite flower, are in full bloom. Which season is it? → Autumn
- space-race-and-astronauts-0: overlap like q-11785: You're in New York's Times Square on New Year's Eve, and the crowd shouts the countdown to midnight. Which number does it start from? → 10: You're watching a Shenzhou launch on TV. The final spoken countdown before “点火” (ignition) starts at which number? → 10
- stars-and-galaxies-0: overlap like q-26705: In the old Chinese legend, ten suns burned the earth until a hero shot some down with his bow and arrows. How many did he shoot down? → 9: This statue shows the archer Hou Yi (后羿). When ten suns rose together and burned the land, how many did he shoot down? → 9
- tang-poems-0: overlap like q-26273: You're reciting 床前明月光 (chuáng qián míng yuè guāng) at bedtime, like millions of Chinese children. In which dynasty was this poem written? → Tang dynasty: The poem that starts 两个黄鹂鸣翠柳 (liǎng gè huánglí míng cuì liǔ, “two yellow orioles sing in the green willows”) was written in which dynasty? → Tang dynasty
- tea-and-drinks-1: overlap like song-ci-1: You're at a park show where chrysanthemums, Tao Yuanming's favorite flower, are in full bloom. Which season is it? → Autumn: The pears are ripe, the air turns dry and your throat feels scratchy, so the family cooks rock sugar pear soup (冰糖雪梨). Which season is it? → Autumn
