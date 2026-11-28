# batch-99

Made by `qgen batch` on 2026-11-27 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (66): chinese-rivers-and-lakes, chinese-birds-and-water-life, farming-and-silk, china-at-the-olympics, swimming, world-cups, fast-food, mythical-creatures, chinese-video-games, chinese-fables, guinness-world-records, mega-projects, popular-chinese-fiction, climate-and-regions, modern-tv-dramas, dream-of-the-red-chamber, toys, late-qing-and-republic, song-ci, song-and-yuan, giant-panda, chinese-opera, science-fiction, idiom-stories, hong-kong-cinema, qin-and-han, lunar-and-planetary-missions, city-snacks, provinces, folktales, nursery-rhymes, world-heritage-sites, three-kingdoms-to-sui, spring-festival, qing-dynasty, early-china, school-and-daily-life, silk-road-and-voyages, cartoons, modern-chinese-literature, space-race-and-astronauts, water-margin, team-sports-in-china, chinese-mountains, bronzes-and-porcelain, traditional-architecture, ming-dynasty, chinese-cinema, ancient-chinese-maths, confucianism, capital-cities, hundred-schools, chinese-medicine-history, board-and-tile-games, calligraphy, chinese-characters, chinese-painting, tang-dynasty, daoism, crewed-spaceflight, chinese-sports-stars, chinese-buddhism, chinese-scientists, solar-system, stars-and-galaxies, famous-scientists
- Merged: 36 (q-28289…q-28324)
- Approved: 32
- Needs work: 4
- Dropped by the pipeline: 26
- Reviewed by: claude-opus-5-5
- Claude calls: 229, about $19.67 at list price; $0.61 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-97, batch-98; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-97 | batch-98 | batch-99 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | batch |
| drafts |  | 116 | 76 | 62 |
| skipped slots |  | 35 | 29 | 23 |
| dropped |  | 40 | 36 | 26 |
| drop rate | ≤ 20.0 % | 34.5 % ✗ | 47.4 % ✗ | 41.9 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 1 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 11 | 9 | 4 |
| dropped: overlap |  | 29 | 24 | 21 |
| dropped: duplicate |  | 0 | 1 | 0 |
| dropped: fact-check wrong |  | 0 | 1 | 1 |
| merged |  | 76 | 40 | 36 |
| approved |  | 68 | 31 | 32 |
| needs_work |  | 8 | 9 | 4 |
| needs_work rate | ≤ 20.0 % | 10.5 % ✓ | 22.5 % ✗ | 11.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 12.5 % ✗ | 2.8 % ✓ |
| needs_work: fact | ≤ 10.0 % | 3.9 % ✓ | 2.5 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.3 % ✗ | 2.5 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 5.3 % ✓ | 2.5 % ✓ | 5.6 % ✓ |
| media: no pick in review 1 |  | 18 | 4 | 7 |
| media: recovered by research |  | 14 | 3 | 5 |
| media: no pick at record |  | 4 | 1 | 2 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 7.5 % ✓ | 2.8 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 2.5 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 25.9 % ✗ | 34.2 % ✗ | 33.9 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 53.6 % ✗ | 41.2 % ✗ | 45.2 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 0.82 ✓ | 1.00 ✓ | 1.00 ✓ |
| approved 11–15 |  | 30 | 19 | 14 |
| top move | ≤ 25.0 % | 17.1 % ✓ | 15.0 % ✓ | 16.7 % ✓ |
| values move |  | 15 | 14 | 12 |
| top stimulus |  | 76.3 % | 97.5 % | 91.7 % |
| values stimulus |  | 4 | 2 | 2 |
| top clue | ≤ 60.0 % | 52.6 % ✓ | 32.5 % ✓ | 41.7 % ✓ |
| values clue |  | 5 | 5 | 5 |
| top answer_kind | ≤ 40.0 % | 25.0 % ✓ | 27.5 % ✓ | 19.4 % ✓ |
| values answer_kind |  | 7 | 6 | 7 |
| top lens | ≤ 25.0 % | 25.0 % ✓ | 17.5 % ✓ | 16.7 % ✓ |
| values lens |  | 11 | 11 | 10 |
| giveaway-step drop rate |  | n/a | n/a | n/a |
| mechanical-check rate |  | n/a | n/a | n/a |
| media share | 15.0 %–50.0 % | 23.7 % ✓ | 2.5 % ✗ | 8.3 % ✗ |
| mean fun | ≥ 3.40 | 3.32 ✗ | 3.41 ✓ | 3.32 ✗ |
| cost $ |  | $33.79 | $20.41 | $17.70 |
| $ per approved | ≤ $0.35 | $0.50 ✗ | $0.66 ✗ | $0.55 ✗ |
| calls |  | 327 | 211 | 193 |
| calls per approved |  | 4.81 | 6.81 | 6.03 |
| wall time h |  | 1.02 | 0.64 | 0.58 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 32 (0 %)
- Major among review needs work: 1 of 4 (25 %)
- Problems by kind: giveaway 4 (1 major), ambiguity 1 (0 major), difficulty 1 (0 major), style 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 1.0; ≥ 3 on 1 of 36 (3 %)
- Audit/review agreement (both accept or both not): 33 of 36 (92 %)
- Sample: 36 audited of 36; 36 Claude calls, about $1.97

Major findings on approved questions:

None.

## Needs work

- **q-28294** (chinese-cinema) Wang Xiaoshuai's Shanghai Dreams (青红) won the Cannes Jury Prize in 2005. Shanghai families sent to work in Guizhou long to go home. In which decade is it set? → The 1980s: None of the candidates shows Guizhou or anywhere in China. 1 and 2 are karst in Vang Vieng, Laos; 3 is Spain, 4 is Crimea and 5 is the Caucasus. No new search is allowed, so the slot needs a real Guizhou karst photo (for example "Guizhou karst landscape" or "Wanfenglin Xingyi"). The text is also borderline long: three sentences, about 158 characters. Cutting the Cannes sentence down would help. No suitable picture found for this question.
- **q-28313** (hundred-schools) Mozi (墨子) sat in a dark room with a tiny hole in one wall. A person stood outside in the sun. How did the person look on the far wall? → Upside down: The media slot has no candidates, and no new search is allowed, so no image can be picked. The text itself is fine: the pinhole fact is correct and the options are clear. It needs a new image search from outside this step, for example "pinhole camera obscura diagram" or a Mozi statue. No suitable picture found for this question.
- **q-28315** (ming-dynasty) Zhu Yuanzhang's Ming weisuo (卫所) garrisons farmed their own land to feed themselves. Who filled their ranks? → Families registered as soldiers for good: Hint 2 gives the answer away: 军户 (jūnhù) reads directly as “military households”, and only the correct option mentions households or families, so a Chinese family solves it at hint 2. Replace hint 2 with a clue that doesn't name or translate the category, for example that the household's status was written into the state registers and could not easily be changed.
- **q-28322** (space-race-and-astronauts) This is Expedition 1, the first crew to live on the International Space Station, in 2000. Who was its American commander? → William Shepherd: This question doesn't belong in chinese-base. It's about an American commander of a US-Russian ISS crew, has no Chinese connection, and a Chinese family can't reason towards it. It's also pure name recall at difficulty 15. It would fit `base` better, or be replaced by a Chinese space question (for example Shenzhou or Tiangong crews).

## Question axes

- move: cause_effect 6, count 2, identify 3, made_of 2, name_concept 3, odd_one_out 1, origin 5, purpose 1, sequence 2, when 5, who 4, word_meaning 2
- stimulus: none 33, photo 3
- clue: completion 1, direct 12, riddle 4, scenario 4, three_facts 15
- answer_kind: group 5, number 3, person 6, place 3, thing 7, time 5, word 7
- lens: body_senses 2, educational_media 5, everyday 6, history 6, language 6, nature 1, pop_culture 3, school 3, science_news 1, university 3

## Dropped by the pipeline

- bronzes-and-porcelain-1: overlap like q-28006: In 1974, farmers digging a well near Xi'an found thousands of life-size soldiers guarding Qin Shi Huang's tomb, each with its own face. What are they made of? → Fired clay: In 1974, farmers digging a well near Xi'an found thousands of life-size soldiers. They guard the tomb of Qin Shi Huang. What are the soldiers made of? → Fired clay
- cartoons-0: overlap like q-6049: In the Japanese anime, Shin-chan goes to kindergarten. How old is he? → 5: In the Japanese cartoon Crayon Shin-chan (蜡笔小新), how old is Shin-chan? → 5
- chinese-birds-and-water-life-0: overlap like q-20330: In Britain, an unwanted newcomer who pushes everyone else out is called “a cuckoo in the…” what? → Nest: A mother cuckoo (布谷鸟) builds no nest, never sits on her eggs and never feeds her chicks. Where does a cuckoo chick hatch? → In another bird's nest
- chinese-fables-0: overlap like q-25813: I'm a little mouse who left home to fly. I pilot a toy plane, and my best friend drives a toy tank. Who am I? → Shuke (舒克): People called all mice thieves, and I was so ashamed that I left home to start an honest life. Later, my friend and I ran an airline. Who am I? → Shuke (舒克)
- chinese-medicine-history-0: overlap like q-27811: Many people drop small, thin, oval dried berries like the ones in the photo into hot water or tea. What are they? → Goji berries (枸杞): Which small, long, bright red dried berries do many Chinese adults drop into a thermos of hot water to “stay healthy”? → Goji berries (枸杞)
- chinese-painting-1: overlap like q-4157: Look at this shadow. Which bird is it? → Peacock: This close-up shows one feather, a favorite subject of Chinese bird-and-flower painters. Which bird does it come from? → Peacock
- chinese-rivers-and-lakes-0: overlap like q-26326: A landslide fills a narrow valley, blocks the river completely, and the water keeps flowing in. What forms behind the pile of rock? → A lake: The Three Gorges Dam (三峡大坝) blocks the Yangtze. The river keeps flowing in, but only some water gets out through its gates. What forms behind the dam? → A huge lake
- famous-scientists-0: overlap like q-21763: Guess: I'm a giant black hole, and Andrea Ghez won the Nobel Prize for proving I exist. Where do I live? → At the center of the Milky Way: I'm a UCLA astronomer. With the Keck telescopes in Hawaii, I tracked a star called S0-2 for decades. In 2020, I became the fourth woman to win the Nobel Prize in Physics. Who am I? → Andrea Ghez
- guinness-world-records-0: overlap like q-2266: Ancient Egyptians threw it away when making mummies. It uses about a fifth of your body's energy. Your awareness comes from it. What is it? → The brain: It is soft and wrinkly like a walnut, it sits inside your skull, and it is the fattiest organ in your body. What is it? → The brain
- idiom-stories-1: overlap like q-26273: You're reciting 床前明月光 (chuáng qián míng yuè guāng) at bedtime, like millions of Chinese children. In which dynasty was this poem written? → Tang dynasty: The saying 铁杵磨成针 (tiě chǔ mó chéng zhēn) comes from a story about the poet Li Bai as a boy. In which dynasty did he live? → The Tang dynasty
- late-qing-and-republic-0: overlap like q-27735: Zhou Shuren wrote as “Lu Xun” and Xie Wanying wrote as “Bing Xin”. What kind of name is “Lu Xun”? → A pen name: I was born Zhou Shuren (周树人) in Shaoxing. I gave up studying medicine to write, and in 1918 I published 狂人日记 (A Madman's Diary). Who am I? → Lu Xun (鲁迅)
- nursery-rhymes-0: hard fail: correct 3, unambiguous 4, no_giveaway 2, no_overlap 5: In the children's song 小松树 (“Little Pine Tree”), the tree has green leaves and new shoots, and it isn't afraid in winter. Afraid of what? → Snowflakes
- popular-chinese-fiction-0: overlap like q-26368: I was born in Sichuan in 1938 and grew up in Taiwan. My first novel was Outside the Window (窗外), and I later wrote My Fair Princess (还珠格格). Who am I? → Qiong Yao (琼瑶): I appeared in Crown magazine (皇冠) in 1963. In me, schoolgirl Jiang Yanrong (江雁容) falls for her teacher, and my 1973 film was Lin Qingxia's debut. What am I? → 窗外 (Chuāng Wài, “Outside the Window”)
- qing-dynasty-0: overlap like q-27347: Look at this painted opera face (脸谱). The opera it belongs to is named after which city? → Beijing: The stage art in this photo grew up in the Qing dynasty. Which city is it named after? → Beijing
- chinese-painting-0: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Yan Liben's “Emperor Taizong Receiving the Tibetan Envoy” (步辇图) is the classic example of which of the “eighteen line styles” (十八描)? → 铁线描 (tiě xiàn miáo, “iron-wire line”)
- chinese-sports-stars-2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: In which year did Qian Hong win the Olympic gold medal in the women's 100 m butterfly? → 1992
- daoism-0: fact-check wrong: The answer 9 is right, but hint 2 is inaccurate. In Ge Hong's Baopuzi the three steps are not identical. They alternate in mirror image: left forward, then right forward, then left forward again. This is from memory and I did not run a search to check it.: Ge Hong wrote that the Daoist Pace of Yu (禹步) is done in three steps. How many footprints should those three steps leave? → 9
- famous-scientists-1: overlap like q-3727: I was the most famous library of the ancient world, built under kings named Ptolemy, and my chief librarian Eratosthenes measured the Earth. What am I? → The Library of Alexandria: This modern library, opened in 2002, stands in the city where Hypatia taught mathematics and philosophy around 400 AD. Which city is it? → Alexandria
- idiom-stories-0: overlap like q-27067: How many teeth does Zhu Bajie's famous rake have? → 9: Sun Wukong is to his golden staff as Zhu Bajie (猪八戒) is to his… → Nine-toothed rake
- space-race-and-astronauts-1: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: At China's Jiuquan launch center (酒泉卫星发射中心), the team counts out loud just before a rocket lifts off. How do the numbers go? → Down to zero
- school-and-daily-life-0: overlap like q-3017: Sunlight splits into colors like these, but it also has invisible rays. Which invisible rays can give you sunburn? → Ultraviolet rays: Sunscreen protects your skin from which kind of rays from the sun? → Ultraviolet (UV) rays
- silk-road-and-voyages-0: overlap like q-26041: In the 1986 TV series “Journey to the West”, Tang Seng heads west with a monkey, a pig and a river ogre. Who else is in the team? → A white dragon horse: You're watching the 1986 TV series “Journey to the West”. Which of Tang Sanzang's disciples almost never says a word? → The White Dragon Horse (白龙马)
- solar-system-0: overlap like q-26867: Li Bai is to “Quiet Night Thoughts” (静夜思) as Bai Juyi is to… → 草 (cǎo, “Grass”): I loved the Moon and wine, I wandered across the Tang empire, and I wrote 静夜思 (Jìng Yè Sī, “Quiet Night Thought”) about missing home. Who am I? → Li Bai (李白)
- song-ci-0: overlap like q-27520: At which festival do Chinese families eat zongzi (粽子), pyramid-shaped parcels wrapped in bamboo leaves? → Dragon Boat Festival: I'm wrapped in leaves and tied with string, with sticky rice inside. Families eat me on the day of the dragon boat races. What am I? → Zongzi (粽子)
- stars-and-galaxies-0: overlap like q-26705: In the old Chinese legend, ten suns burned the earth until a hero shot some down with his bow and arrows. How many did he shoot down? → 9: This NASA photo shows our Sun. In the legend, Hou Yi (后羿) shot down suns until only this one was left. How many did he shoot down? → 9
- traditional-architecture-0: overlap like q-28229: This photo shows part of a famous gate in Beijing. Which gate is it? → Tiananmen (天安门): This photo shows part of Tiananmen (天安门) in Beijing. Whose big portrait hangs above its central arch all year round? → Mao Zedong
