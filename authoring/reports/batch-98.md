# batch-98

Made by `qgen batch` on 2026-11-27 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (75): chinese-rivers-and-lakes, chinese-birds-and-water-life, chinese-kitchen, farming-and-silk, china-at-the-olympics, swimming, world-cups, fast-food, mythical-creatures, chinese-video-games, mega-projects, popular-chinese-fiction, chinese-fables, guinness-world-records, dream-of-the-red-chamber, climate-and-regions, idiom-stories, chinese-opera, modern-tv-dramas, late-qing-and-republic, song-ci, customs-and-etiquette, provinces, childrens-games, toys, science-fiction, song-and-yuan, giant-panda, qin-and-han, lunar-and-planetary-missions, spring-festival, hong-kong-cinema, diving-and-gymnastics, world-heritage-sites, city-snacks, ethnic-groups, folktales, nursery-rhymes, chinese-cartoons, three-kingdoms-to-sui, calendar-and-solar-terms, chinese-mountains, c-pop, qing-dynasty, chinese-cinema, silk-road-and-voyages, ancient-chinese-maths, early-china, cartoons, school-and-daily-life, modern-chinese-literature, space-race-and-astronauts, water-margin, team-sports-in-china, chinese-characters, bronzes-and-porcelain, ming-dynasty, crewed-spaceflight, traditional-architecture, confucianism, capital-cities, hundred-schools, chinese-medicine-history, chinese-sports-stars, calligraphy, board-and-tile-games, chinese-painting, tang-dynasty, daoism, dialects, chinese-buddhism, chinese-scientists, solar-system, stars-and-galaxies, famous-scientists
- Merged: 40 (q-28249…q-28288)
- Approved: 31
- Needs work: 9
- Dropped by the pipeline: 36
- Reviewed by: claude-opus-5-5
- Claude calls: 251, about $22.66 at list price; $0.73 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-96, batch-97; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-96 | batch-97 | batch-98 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | batch |
| drafts |  | 172 | 116 | 76 |
| skipped slots |  | 53 | 35 | 29 |
| dropped |  | 46 | 40 | 36 |
| drop rate | ≤ 20.0 % | 26.7 % ✗ | 34.5 % ✗ | 47.4 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 1 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 8 | 11 | 9 |
| dropped: overlap |  | 37 | 29 | 24 |
| dropped: duplicate |  | 0 | 0 | 1 |
| dropped: fact-check wrong |  | 1 | 0 | 1 |
| merged |  | 126 | 76 | 40 |
| approved |  | 109 | 68 | 31 |
| needs_work |  | 17 | 8 | 9 |
| needs_work rate | ≤ 20.0 % | 13.5 % ✓ | 10.5 % ✓ | 22.5 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 6.3 % ✓ | 0.0 % ✓ | 12.5 % ✗ |
| needs_work: fact | ≤ 10.0 % | 1.6 % ✓ | 3.9 % ✓ | 2.5 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 1.3 % ✗ | 2.5 % ✗ |
| needs_work: media | ≤ 10.0 % | 3.2 % ✓ | 5.3 % ✓ | 2.5 % ✓ |
| media: no pick in review 1 |  | 19 | 18 | 4 |
| media: recovered by research |  | 15 | 14 | 3 |
| media: no pick at record |  | 4 | 4 | 1 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 4.0 % ✓ | 0.0 % ✓ | 7.5 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 2.5 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 21.5 % ✗ | 25.9 % ✗ | 34.2 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 61.6 % ✓ | 53.6 % ✗ | 41.2 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.18 ✓ | 0.82 ✓ | 1.00 ✓ |
| approved 11–15 |  | 46 | 30 | 19 |
| top move | ≤ 25.0 % | 11.9 % ✓ | 17.1 % ✓ | 15.0 % ✓ |
| values move |  | 15 | 15 | 14 |
| top stimulus |  | 85.7 % | 76.3 % | 97.5 % |
| values stimulus |  | 4 | 4 | 2 |
| top clue | ≤ 60.0 % | 42.1 % ✓ | 52.6 % ✓ | 32.5 % ✓ |
| values clue |  | 4 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 23.0 % ✓ | 25.0 % ✓ | 27.5 % ✓ |
| values answer_kind |  | 7 | 7 | 6 |
| top lens | ≤ 25.0 % | 17.5 % ✓ | 25.0 % ✓ | 17.5 % ✓ |
| values lens |  | 11 | 11 | 11 |
| giveaway-step drop rate |  | n/a | n/a | n/a |
| mechanical-check rate |  | n/a | n/a | n/a |
| media share | 15.0 %–50.0 % | 14.3 % ✗ | 23.7 % ✓ | 2.5 % ✗ |
| mean fun | ≥ 3.40 | 3.37 ✗ | 3.32 ✗ | 3.41 ✓ |
| cost $ |  | $50.80 | $33.79 | $20.41 |
| $ per approved | ≤ $0.35 | $0.47 ✗ | $0.50 ✗ | $0.66 ✗ |
| calls |  | 458 | 327 | 211 |
| calls per approved |  | 4.20 | 4.81 | 6.81 |
| wall time h |  | 1.47 | 1.02 | 0.63 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 3 of 31 (10 %)
- Major among review needs work: 0 of 9 (0 %)
- Problems by kind: giveaway 9 (2 major), overlap 4 (2 major), media 1 (0 major), difficulty 5 (1 major), style 2 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 1.4; ≥ 3 on 5 of 40 (12 %)
- Audit/review agreement (both accept or both not): 28 of 40 (70 %)
- Sample: 40 audited of 40; 40 Claude calls, about $2.25

Major findings on approved questions:

- **q-28260**: overlap — I checked the facts and they hold. On May 25, 1960, Wang Fuzhou, Gonpo and Qu Yinhua reached the top before dawn. Qu took off his boots at the Second Step and stood on Liu Lianman's shoulders, and Shi Zhanchun led the expedition, so he is a fair wrong answer. The problem is that related q-27585 (needs_work) asks which mountain Gonpo's three-man team climbed from its north side on May 25, 1960. This question says Everest's north side and 1960 in its text, and its fun fact names Gonpo, so playing one gives the other away. The difficulty is a little high: I'd rate it 13–14, because the barefoot Second Step story is well known in China. (http://127.0.0.1:8001/review/q-28260)
- **q-28264**: giveaway, difficulty — The question text gives the answer away. It says “My name comes from an effect found in 1879”, and “Hall-effect thruster” is the only option whose name contains an effect at all, so players can pick it without knowing anything about thrusters. That makes it far easier than the rated 15. The facts check out: Tianhe has four LHT-100 Hall thrusters running on xenon, Edwin Hall found the effect in 1879, the thrust of about 80 mN is roughly the weight of a coin, and none of the three wrong answers is used this way on Tianhe. (http://127.0.0.1:8001/review/q-28264)
- **q-28282**: overlap, giveaway — The fact checks out: the quote is Shen Dao's, and Han Feizi quotes it in the chapter “Nan Shi” (难势), along with the line about Yao as a commoner. The fun fact is also standard. The problem is overlap: the fun fact states “Shen Buhai's 术 (shù, methods)”, which is the exact answer to related question q-27381 (“Shang Yang is to 法 as Shen Buhai is to…”), so playing this one gives that one away. Also minor: hint 2 (势, power that comes from rank) points almost straight to the ruler answer. (http://127.0.0.1:8001/review/q-28282)

## Needs work

- **q-28255** (childrens-games) In 骑马打仗 (qí mǎ dǎ zhàng, “riding horses to fight”), riders try to pull each other down, and whoever falls first loses. What is each “horse”? → A child carrying the rider on their back: Hint 1 (“The game needs no toys or equipment at all.”) rules out all three wrong options at once: a toy stick horse, a bench and a rope swing are all equipment. That gives the answer away before hint 3. Hint 1 needs to be vaguer, for example a hint about the noisy playground or the shouting, and must not rule out any option.
- **q-28256** (chinese-birds-and-water-life) This duck has pure white feathers and an orange beak, reached America in 1873, and is now farmed worldwide. Which famous dish was it first bred for? → Peking roast duck (北京烤鸭): The fun fact can't be confirmed. The 1873 import was James Palmer's shipment to New York/Stonington, Connecticut, and only later to Long Island farms. The claim that most white farm ducks in the world descend from that one shipment also overstates it, because Pekins reached Britain separately the same year. The fact check is 'uncertain'. Reword the fun fact to something safe, like 'Pekin ducks reached the US in 1873, and Long Island became famous for farming them', or drop the descent claim. Fact check: uncertain. Answer fine. Fun fact says ducks were first shipped to Long Island in 1873. From memory, James Palmer first landed them at Stonington, Connecticut, and they reached Long Island shortly after. I did not check this with a search.
- **q-28268** (famous-scientists) This Greek doctor treated gladiators, served Emperor Marcus Aurelius, and his books guided Western medicine for about 1,400 years. What did he teach makes people ill? → An imbalance of four body fluids: This question doesn't belong in chinese-base. Galen and the four humours are pure Greco-Roman medical history, not something a Chinese family learns at school. The bundle rule puts well-known facts about other countries in `base`, and the hint linking it to traditional Chinese medicine doesn't make it China-centred. Move it to `base` or drop it. Also, the fun fact's “windows into the body” quote is a loosely sourced paraphrase, so it's better to replace it with a fact that has a firm source.
- **q-28270** (hundred-schools) Sunzi said that if you know the enemy and know yourself, you won't be in danger in how many battles? → 100: The text is fine, but none of the media candidates is usable. They show a Mazu temple stairway, a playground, Laozi statues in Quanzhou (a different thinker, so it would mislead) and a Canadian yacht plaque. None shows Sunzi or anything to do with The Art of War, and no new search is allowed. A new search for something like "Sun Tzu statue Huimin" or "Art of War bamboo slips" should find a usable image. No suitable picture found for this question.
- **q-28273** (modern-tv-dramas) You're watching Yang Mi in Palace (宫锁心玉, 2011), where her modern girl Luo Qingchuan travels back in time. To which dynasty? → Qing dynasty: Hint 1 ("the most recent of these four dynasties") gives the answer away. Chinese children learn the order Tang, Song, Yuan, Ming, Qing early in school, so the first hint alone picks out Qing. Replace it with a vague hint, for example about the palace setting or the era of the drama's emperor, without saying where Qing sits in time.
- **q-28276** (chinese-kitchen) Families hang strips of 腊肉 (là ròu) out to dry before Spring Festival. Which lunar month is this meat named after? → The twelfth lunar month: The question asks what the character 腊 in 腊肉 means (the twelfth lunar month, 腊月), which breaks the bundle rule against asking what a Chinese word states. In zh-Hans/zh-Hant the right option becomes 腊月/臘月 and shares its character with 腊肉 in the question, so it gives itself away. Hint 2 (腊八) also points straight at it.
- **q-28279** (chinese-video-games) You're on the bus, flinging birds at green pigs on a touchscreen phone. In which decade did Angry Birds first come out? → The 2000s: Angry Birds is a Finnish game that families everywhere know, so it isn't China-centred. It belongs in `base`, not in `chinese-base` under "Chinese video games". Rewording can't fix this. Move the question to base (after checking it against q-6753), or drop it. If it is kept, also cut the filler opening "You're on the bus".
- **q-28281** (dream-of-the-red-chamber) I was born with a piece of jade in my mouth. I hate studying for the imperial exams, and my cousin Lin Daiyu often cries because of me. Who am I? → Jia Baoyu (贾宝玉): The description gives the answer away. Tasting girls' rouge is one of Jia Baoyu's best-known traits (q-27302 is built on it). Calling him a "boy" with cousins also rules out Jia Zheng and the married Jia Lian before any hint is shown. Rewrite the description so it plays on the theme of the novel or the riddle without naming a trait of Baoyu.
- **q-28285** (team-sports-in-china) On 7 October 2001 in Shenyang, China beat Oman 1–0 to reach its first World Cup. In which country did China play its World Cup games? → South Korea: Hint 2 gives the answer away: "the host that is not an island nation" leaves only South Korea once a player knows Japan is a co-host. The question also overlaps approved q-26885 (year of China's first World Cup match → 2002). Saying China qualified for its first World Cup in October 2001, with the tournament "the very next summer", gives that answer away. To fix it, rewrite hint 2 so it doesn't decide between the co-hosts, and drop the qualification date or the "next summer" wording that answers q-26885.

## Question axes

- move: cause_effect 4, count 1, estimate 1, identify 5, made_of 3, name_concept 2, odd_one_out 2, origin 6, purpose 2, record 1, sequence 3, when 5, who 2, word_meaning 3
- stimulus: none 39, photo 1
- clue: completion 1, direct 13, riddle 6, scenario 7, three_facts 13
- answer_kind: group 4, number 2, person 8, thing 11, time 5, word 10
- lens: body_senses 2, educational_media 5, everyday 6, history 6, language 7, nature 1, pop_culture 7, popular_science 1, school 1, science_news 1, university 3

## Dropped by the pipeline

- bronzes-and-porcelain-0: overlap like q-6377: I'm a shiny thing you eat cereal with. Look into my curved bowl and you see your face upside down! What am I? → A spoon: I'm white and shiny, made of porcelain, with a short handle and a flat bottom so I stand on the table. You scoop wonton soup with me. What am I? → A porcelain spoon (汤匙)
- bronzes-and-porcelain-1: overlap like q-28006: In 1974, farmers digging a well near Xi'an found thousands of life-size soldiers guarding Qin Shi Huang's tomb, each with its own face. What are they made of? → Fired clay: Farmers digging a well near Xi'an in 1974 found them: thousands of life-size soldiers guarding Qin Shi Huang's tomb. What are they made of? → Fired clay
- calligraphy-0: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: This is a Chengni inkstone (澄泥砚), one of China’s Four Famous Inkstones. What is it made from? → Fine river silt, fired in a kiln
- china-at-the-olympics-0: overlap like q-26879: China's women's volleyball team won Olympic silver in 1996, losing the final to Cuba. Which city hosted those Games? → Atlanta: It won Olympic gold in Los Angeles in 1984, and its star Lang Ping was called the “Iron Hammer” (铁榔头). What is 女排 (nǚpái)? → The women's volleyball team
- chinese-medicine-history-1: duplicate like q-15428: Mira estas aceitunas negras. ¿Qué son en realidad? → Frutas: Look at these dried red goji berries (枸杞). Which part of the plant are they? → Fruits
- chinese-painting-1: overlap like q-4157: Look at this shadow. Which bird is it? → Peacock: This close-up shows part of one feather. Which bird does it come from? → Peacock
- chinese-rivers-and-lakes-0: overlap like q-26326: A landslide fills a narrow valley, blocks the river completely, and the water keeps flowing in. What forms behind the pile of rock? → A lake: The Three Gorges Dam blocks the Yangtze. Behind it the water rises, spreads back for about 600 km and floats big ships. What has formed? → A huge lake
- chinese-sports-stars-3: overlap like q-17961: At the start of a frame of snooker, all the balls are on the table, the white included. How many balls is that? → 22: Ding Junhui plays snooker. About how many balls are on the table at the start of a game, the white ball included? → About 20
- confucianism-0: overlap like q-26497: Which classic contains the famous line 学而不思则罔，思而不学则殆? → The Analects (论语): This book was put together by Confucius's students after he died. It records his talks with them, and many lines start with 子曰 (“The Master said”). Which book is it? → 论语 (Lúnyǔ, The Analects)
- early-china-0: overlap like q-26150: Yu the Great was so busy taming the great flood that he passed his home three times without going in. How did he beat the flood? → Digging channels to lead the water away: Yu's father Gun tried to block the floodwaters with walls of earth and failed. Yu worked for 13 years and led the water out to the sea. What did Yu dig? → Channels
- famous-scientists-0: overlap like q-21763: Guess: I'm a giant black hole, and Andrea Ghez won the Nobel Prize for proving I exist. Where do I live? → At the center of the Milky Way: I work at UCLA and spent decades tracking stars with the Keck telescopes in Hawaii. In 2020, I became the fourth woman to win the Nobel Prize in Physics. Who am I? → Andrea Ghez
- folktales-0: overlap like q-28163: Families hang red couplets and red lanterns at New Year. In the old legend, who was scared of the color red? → The Nian beast (年兽): In the old legend, 年 (Nián) lives deep in the sea, comes ashore every New Year's Eve and runs from loud bangs and the color red. What is Nian? → A fierce beast
- hong-kong-cinema-1: overlap like q-3265: This Wii add-on is named after a martial arts weapon. Which film star made that weapon world-famous? → Bruce Lee: I'm two short sticks joined by a chain or a rope. Bruce Lee spun me so fast in his films that I became world-famous. What am I? → Nunchaku
- idiom-stories-0: overlap like q-27929: I sat at my loom, then rode to war in my father's place. My ballad ends with two rabbits running side by side, so no one can tell which is the girl. Who am I? → Hua Mulan: My old father was called to war, so I put on armor and rode off in his place. For years, my comrades never knew I was a girl. Who am I? → Hua Mulan (花木兰)
- late-qing-and-republic-0: overlap like q-28106: In a Lu Xun story, which boy wears a silver necklace and guards the watermelon field from the zha (猹) by moonlight? → Runtu (闰土): “I studied medicine in Japan but chose to write instead. I wrote “The True Story of Ah Q” and about my childhood friend Runtu (闰土) guarding watermelons by moonlight. Who am I?” → Lu Xun (鲁迅)
- popular-chinese-fiction-0: overlap like q-26368: I was born in Sichuan in 1938 and grew up in Taiwan. My first novel was Outside the Window (窗外), and I later wrote My Fair Princess (还珠格格). Who am I? → Qiong Yao (琼瑶): My heroine, a high school girl in Taiwan, falls in love with her Chinese teacher, as my author once did. In 1973 Brigitte Lin (林青霞) made her film debut in my film. What am I? → 窗外 (Chuāng Wài, “Outside the Window”)
- qin-and-han-0: overlap like q-28206: Qin Shi Huang's eldest son was sent north to serve with general Meng Tian. Then a forged will gave the throne to his younger brother. Who was this son? → Fusu (扶苏): In 210 BC, Qin Shi Huang died on a tour at Shaqiu. Zhao Gao and Li Si kept it secret and faked one thing, so Huhai became emperor instead of Fusu. What was it? → The emperor's last edict (遗诏)
- qing-dynasty-0: overlap like q-27347: Look at this painted opera face (脸谱). The opera it belongs to is named after which city? → Beijing: The stage art in this photo is named after a Chinese city. Which city? → Beijing
- china-at-the-olympics-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In the right order, the first syllables of the five Fuwa (福娃) names spell a famous Olympic greeting. Where does Beibei stand? → 1st
- chinese-medicine-history-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Li Yanwen (李言闻) was a Ming doctor. He wrote a book on ginseng, and his son was Li Shizhen. Where was their home? → Qichun, Hubei
- chinese-scientists-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In the 1970s, Wu Wenjun (吴文俊) turned problems into polynomial equations and simplified them step by step with “characteristic sets”. What did his method let computers do? → Prove geometry theorems automatically
- chinese-scientists-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: I stretch about 55 km across the sea and dive into an undersea tunnel in the middle. What am I? → The Hong Kong–Zhuhai–Macao Bridge (港珠澳大桥)
- guinness-world-records-0: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 4: It is the fattest organ in your body, about 60% fat, and it keeps working even while you sleep. Which organ is it? → The brain
- modern-tv-dramas-1: overlap like q-26484: In Home with Kids (家有儿女), Yang Zi played the eldest child, a clever, bossy top student. Which character? → Xia Xue: I played the grape spirit Jinmi in Ashes of Love (香蜜沉沉烬如霜) and Tong Nian in Go Go Squid (亲爱的，热爱的). Who am I? → Yang Zi (杨紫)
- mythical-creatures-0: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: This sea beast from Indian myth is the makara (摩羯), which gave Capricorn its Chinese name 摩羯座. Its body is mainly which animal? → A crocodile
- nursery-rhymes-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Children's songs cheer on the little pine tree (小松树), and poems praise it in snowy winters. What kind of tree is a pine? → An evergreen tree
- space-race-and-astronauts-3: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In 2003, his rocket shook hard for about 26 seconds on the way up, and then he became China's first person in space. Who is he? → Yang Liwei (杨利伟)
- world-heritage-sites-0: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 5: Portuguese sailors are said to have named Macau after this temple by the harbor. Which goddess does it honor? → Mazu (妈祖)
- school-and-daily-life-0: overlap like q-22165: Sunlight splits into colors like these, but it also has invisible rays. Which invisible rays can give you sunburn? → Ultraviolet rays: Sunscreen (防晒霜) protects your skin from which kind of rays from the sun? → Ultraviolet (UV) rays
- science-fiction-0: overlap like q-10631: Minions are small, wear goggles and work for Gru. Which fruit makes them shout with joy? → Banana: In Despicable Me (神偷奶爸), Gru's Minions wear goggles, speak a funny made-up language and love one fruit. Which fruit makes them cheer? → Banana
- silk-road-and-voyages-0: overlap like q-26041: In the 1986 TV series “Journey to the West”, Tang Seng heads west with a monkey, a pig and a river ogre. Who else is in the team? → A white dragon horse: You're watching the 1986 TV series “Journey to the West”. Three of these pilgrims walk the whole way. Which one does Tang Sanzang ride? → The White Dragon Horse
- solar-system-0: overlap like q-27445: In Li Bai's 静夜思, what comes next: “床前明月光，疑是地上___”? → 霜 (shuāng, “frost”): “I loved wine and the Moon. One night, moonlight on the floor by my bed looked like frost and made me miss home, so I wrote 静夜思. Who am I?” → Li Bai (李白)
- song-ci-0: overlap like q-27520: At which festival do Chinese families eat zongzi (粽子), pyramid-shaped parcels wrapped in bamboo leaves? → Dragon Boat Festival: I'm sticky rice wrapped in bamboo leaves and tied with string. People eat me at the Dragon Boat Festival to remember the poet Qu Yuan. What am I? → Zongzi (粽子)
- stars-and-galaxies-0: overlap like q-26705: In the old Chinese legend, ten suns burned the earth until a hero shot some down with his bow and arrows. How many did he shoot down? → 9: Today you see just one Sun in the sky. In the legend of Hou Yi (后羿), how many suns were there before he picked up his bow? → 10
- tang-dynasty-0: fact-check wrong: Answer (Xinghua Ward) is right and the wrong answers are wrong. But hint 2 says Li Shouli, Prince of Bin, was a nephew of Emperor Xuanzong. He was Xuanzong's first cousin. His father was Li Xian (Crown Prince Zhanghuai), the brother of Xuanzong's father Ruizong. This is from memory; I ran no searches.: The Hejiacun hoard of Tang gold and silver was dug up south of Xi'an in 1970. In Tang Chang'an, which ward (坊) was this spot part of? → Xinghua Ward (兴化坊)
- three-kingdoms-to-sui-1: overlap like q-27626: Liu Xie wrote it around 500 CE in 50 chapters, covering every genre. It is China's first systematic book of literary theory. Which? → 文心雕龙 (Wénxīn Diāolóng, “The Literary Mind and the Carving of Dragons”): I was written around 500 AD in 50 chapters of parallel prose. My author grew up in a Buddhist temple and later became a monk. Shen Yue kept me on his desk. What am I? → 文心雕龙 (Wénxīn Diāolóng, “The Literary Mind and the Carving of Dragons”)
