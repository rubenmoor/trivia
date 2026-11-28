# batch-100

Made by `qgen batch` on 2026-11-27 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (51): chinese-rivers-and-lakes, chinese-birds-and-water-life, china-at-the-olympics, swimming, mythical-creatures, world-cups, guinness-world-records, climate-and-regions, mega-projects, popular-chinese-fiction, toys, provinces, late-qing-and-republic, idiom-stories, song-ci, dream-of-the-red-chamber, nursery-rhymes, modern-tv-dramas, hong-kong-cinema, lunar-and-planetary-missions, school-and-daily-life, three-kingdoms-to-sui, qing-dynasty, early-china, silk-road-and-voyages, modern-chinese-literature, giant-panda, space-race-and-astronauts, water-margin, traditional-architecture, team-sports-in-china, bronzes-and-porcelain, chinese-cinema, capital-cities, confucianism, chinese-medicine-history, hundred-schools, calligraphy, chinese-painting, tang-dynasty, daoism, ming-dynasty, ancient-chinese-maths, crewed-spaceflight, board-and-tile-games, chinese-characters, chinese-sports-stars, chinese-scientists, solar-system, stars-and-galaxies, famous-scientists
- Merged: 25 (q-28325…q-28349)
- Approved: 19
- Needs work: 6
- Dropped by the pipeline: 21
- Reviewed by: claude-opus-5-5
- Claude calls: 170, about $14.54 at list price; $0.77 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-98, batch-99; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-98 | batch-99 | batch-100 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | batch |
| drafts |  | 76 | 62 | 46 |
| skipped slots |  | 29 | 23 | 16 |
| dropped |  | 36 | 26 | 21 |
| drop rate | ≤ 20.0 % | 47.4 % ✗ | 41.9 % ✗ | 45.7 % ✗ |
| dropped: hard fail correct |  | 1 | 1 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 9 | 4 | 4 |
| dropped: overlap |  | 24 | 21 | 16 |
| dropped: duplicate |  | 1 | 0 | 1 |
| dropped: fact-check wrong |  | 1 | 1 | 0 |
| merged |  | 40 | 36 | 25 |
| approved |  | 31 | 32 | 19 |
| needs_work |  | 9 | 4 | 6 |
| needs_work rate | ≤ 20.0 % | 22.5 % ✗ | 11.1 % ✓ | 24.0 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 12.5 % ✗ | 2.8 % ✓ | 8.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 2.5 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.5 % ✗ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 2.5 % ✓ | 5.6 % ✓ | 4.0 % ✓ |
| media: no pick in review 1 |  | 4 | 7 | 3 |
| media: recovered by research |  | 3 | 5 | 2 |
| media: no pick at record |  | 1 | 2 | 1 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 7.5 % ✓ | 2.8 % ✓ | 16.0 % ✗ |
| needs_work: other | ≤ 10.0 % | 2.5 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 34.2 % ✗ | 33.9 % ✗ | 37.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 41.2 % ✗ | 45.2 % ✗ | 48.5 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.00 ✓ | 1.00 ✓ |
| approved 11–15 |  | 19 | 14 | 11 |
| top move | ≤ 25.0 % | 15.0 % ✓ | 16.7 % ✓ | 16.0 % ✓ |
| values move |  | 14 | 12 | 11 |
| top stimulus |  | 97.5 % | 91.7 % | 88.0 % |
| values stimulus |  | 2 | 2 | 3 |
| top clue | ≤ 60.0 % | 32.5 % ✓ | 41.7 % ✓ | 44.0 % ✓ |
| values clue |  | 5 | 5 | 4 |
| top answer_kind | ≤ 40.0 % | 27.5 % ✓ | 19.4 % ✓ | 20.0 % ✓ |
| values answer_kind |  | 6 | 7 | 7 |
| top lens | ≤ 25.0 % | 17.5 % ✓ | 16.7 % ✓ | 16.0 % ✓ |
| values lens |  | 11 | 10 | 9 |
| giveaway-step drop rate |  | n/a | n/a | n/a |
| mechanical-check rate |  | n/a | n/a | n/a |
| media share | 15.0 %–50.0 % | 2.5 % ✗ | 8.3 % ✗ | 12.0 % ✗ |
| mean fun | ≥ 3.40 | 3.41 ✓ | 3.32 ✗ | 3.26 ✗ |
| cost $ |  | $20.41 | $17.70 | $12.36 |
| $ per approved | ≤ $0.35 | $0.66 ✗ | $0.55 ✗ | $0.65 ✗ |
| calls |  | 211 | 193 | 136 |
| calls per approved |  | 6.81 | 6.03 | 7.16 |
| wall time h |  | 0.64 | 0.59 | 0.44 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 19 (0 %)
- Major among review needs work: 0 of 6 (0 %)
- Problems by kind: giveaway 4 (0 major), media 3 (0 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 1.2; ≥ 3 on 1 of 25 (4 %)
- Audit/review agreement (both accept or both not): 19 of 25 (76 %)
- Sample: 25 audited of 25; 34 Claude calls, about $2.18

Major findings on approved questions:

None.

## Needs work

- **q-28329** (chinese-scientists) Rice blast (稻瘟病) is one of the worst diseases of rice in China. What kind of organism causes it? → Fungi: Hint 1 ("spreads by tiny spores carried on wind and dew") gives the answer away. Wind-borne spores are the textbook trait of fungi, and none of the wrong options (bacteria, viruses, insects) spread that way, so an adult can answer from hint 1 alone. Hint 1 should be rewritten as a vague clue, for example about the disease striking in warm, humid weather or about the crop losses it causes.
- **q-28333** (famous-scientists) You're in Hawaii, looking up at the twin Keck telescopes Andrea Ghez used for her Nobel Prize work. Which mountain are you on? → Mauna Kea: The question doesn't fit the chinese-base bundle. It's about a US observatory on a Hawaiian volcano and an American Nobel laureate, and it needs Hawaii knowledge that a Chinese family doesn't learn at school or in daily life. Per the bundle rule ("well-known facts about any country still belong in base"), move it to the base bundle or drop it here. Moving it means the bundle changes, not the text.
- **q-28334** (famous-scientists) Around 400 AD, the mathematician and philosopher Hypatia taught in the city in this photo. Which city is it? → Alexandria: Wrong bundle: Hypatia and Alexandria are Mediterranean history with no link to China. Chinese families don't learn this at school, and under the bundle rule it belongs in `base`, not `chinese-base`. If it moves to base, hints 1 and 2 also need softening: the Pharos lighthouse and "coast of Egypt" each pick out Alexandria from the four options right away.
- **q-28337** (late-qing-and-republic) Once I was late for school, so I carved 早 (“early”) into my desk. Later I wrote The True Story of Ah Q (阿Q正传). Who am I? → Lu Xun (鲁迅): The text is fine, but no media candidate is adequate: none shows Shaoxing. 1 and 6 are Western towns, 3 and 4 show the Grand Canal at Guazhou, and 2 and 5 show Lijiang, a place unrelated to Lu Xun. No new search is allowed. A better search would be "Lu Xun Native Place Shaoxing" or "Sanwei Study Shaoxing". No suitable picture found for this question.
- **q-28347** (space-race-and-astronauts) In December 1957, the US rocket Vanguard TV3 tried to launch its first satellite. About how high did it rise before it fell back and exploded? → About 1 m: This is a US space-history fact with no Chinese angle. The chinese-base bundle needs content centred on China that a Chinese family meets at school or in daily life, so this question belongs in base, not chinese-base. Move it to base (where it would need US-style dates) or drop it from this bundle.
- **q-28349** (toys) Toy Stirling engines spin on the warmth of a cup of hot tea. In which year did Robert Stirling patent this engine? → 1816: This question doesn't belong in chinese-base. Robert Stirling's 1816 patent is a European invention date with nothing Chinese at its core, and the Jiaqing hint only adds a Chinese angle on top. It also gets its difficulty of 15 from a minor patent year that players have to remember, not from knowledge they can reason towards. If you want to keep it, move it to base, ideally as a question about Stirling himself or how the engine works rather than the year.

## Question axes

- move: cause_effect 2, count 1, estimate 2, identify 4, origin 3, purpose 1, record 1, sequence 3, when 3, who 4, word_meaning 1
- stimulus: detail 1, none 22, photo 2
- clue: direct 11, riddle 2, scenario 4, three_facts 8
- answer_kind: group 3, number 3, person 5, place 4, thing 3, time 3, word 4
- lens: body_senses 1, educational_media 2, everyday 4, history 4, language 2, pop_culture 4, popular_science 1, school 3, university 4

## Dropped by the pipeline

- chinese-medicine-history-0: overlap like q-15428: Mira estas aceitunas negras. ¿Qué son en realidad? → Frutas: These little red dried things are often dropped into Chinese soups and tea. What kind of food are they? → Fruits
- chinese-rivers-and-lakes-0: overlap like q-26326: A landslide fills a narrow valley, blocks the river completely, and the water keeps flowing in. What forms behind the pile of rock? → A lake: The Three Gorges Dam is a giant concrete wall across the Yangtze. It holds the river back, so the water rises behind it. What forms there? → A long lake
- daoism-0: overlap like q-26099: Who is China's most famous flood tamer, said to have passed his own home three times without going in? → Yu the Great (大禹): My legs were half-lame, so I walked with a dragging step. Daoist priests copy it when they tread the stars of the Big Dipper (北斗). Who am I? → Yu the Great (大禹)
- dream-of-the-red-chamber-0: overlap like q-26090: I lost my husband young and quietly raise my son, Jia Lan. My home in the garden is Paddy-Sweet Cottage (稻香村), built to look like a farm. Who am I? → Li Wan: My father Jia Zhu died young. In my mother's picture in the Jinling register, a pot of orchids blooms. In the end, I pass the imperial exam with my uncle. Who am I? → 贾兰 (Jiǎ Lán)
- early-china-0: overlap like q-27520: At which festival do Chinese families eat zongzi (粽子), pyramid-shaped parcels wrapped in bamboo leaves? → Dragon Boat Festival: Legend says people threw this into the Miluo River so the fish would eat it and leave Qu Yuan alone. Today it comes wrapped in leaves. What is it? → Zongzi (粽子)
- guinness-world-records-0: overlap like q-2266: Ancient Egyptians threw it away when making mummies. It uses about a fifth of your body's energy. Your awareness comes from it. What is it? → The brain: It has about 86 billion nerve cells, more than any other part of your body. It weighs about 1.4 kg and sits inside your skull. What is it? → The brain
- hundred-schools-0: overlap like q-26420: I conquered six states. I made everyone use the same writing, the same coins and the same weights and measures. Who am I? → Qin Shi Huang: I was king of the State of Qin (秦国). I made all the warring states into one China, and thousands of clay soldiers guard my tomb. Who am I? → Qin Shi Huang (秦始皇)
- idiom-stories-0: overlap like q-27929: I sat at my loom, then rode to war in my father's place. My ballad ends with two rabbits running side by side, so no one can tell which is the girl. Who am I? → Hua Mulan: I was weaving at home when the army called for my old father. I dressed as a boy and went in his place for twelve years. Who am I? → Hua Mulan (花木兰)
- idiom-stories-1: overlap like q-26273: You're reciting 床前明月光 (chuáng qián míng yuè guāng) at bedtime, like millions of Chinese children. In which dynasty was this poem written? → Tang dynasty: The saying 铁杵磨成针 (tiě chǔ mó chéng zhēn) comes from a story about young Li Bai meeting an old woman grinding an iron rod. In which dynasty did Li Bai live? → The Tang dynasty
- lunar-and-planetary-missions-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It launched in August 2022, looped far beyond the Moon to save fuel, and in December 2022 became South Korea's first lunar orbiter. What is it? → Danuri
- popular-chinese-fiction-0: overlap like q-26368: I was born in Sichuan in 1938 and grew up in Taiwan. My first novel was Outside the Window (窗外), and I later wrote My Fair Princess (还珠格格). Who am I? → Qiong Yao (琼瑶): I came out in Crown magazine (皇冠) in 1963. My heroine, schoolgirl Jiang Yanrong (江雁容), falls in love with her teacher. In 1973 I became Lin Qingxia's (林青霞) first film. What am I? → 窗外 (Chuāng Wài, “Outside the Window”)
- qing-dynasty-0: overlap like q-27347: Look at this painted opera face (脸谱). The opera it belongs to is named after which city? → Beijing: The stage art in this photo grew up in Qing times and is named after a Chinese city. Which city? → Beijing
- climate-and-regions-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Rows of giant white towers with three long blades stand on the Inner Mongolia grassland. China has more of them than any other country. What are they? → Wind turbines (风力发电机)
- provinces-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Legend says five immortals riding rams brought rice to this city, so it is called 羊城 (Yángchéng, “City of Rams”). Which city is it? → Guangzhou
- school-and-daily-life-0: overlap like q-22165: Sunlight splits into colors like these, but it also has invisible rays. Which invisible rays can give you sunburn? → Ultraviolet rays: On a sunny day, sunscreen (防晒霜) protects your skin from which kind of rays in sunlight? → Ultraviolet rays (紫外线)
- silk-road-and-voyages-0: overlap like q-25815: I'm a kind monk who rides a white horse west to bring back holy books. A monkey, a pig and a quiet giant protect me. Who am I? → Tang Sanzang (唐三藏): You're watching “Journey to the West” on TV. Three of these pilgrims walk all the way west. Who rides the White Dragon Horse? → Tang Sanzang (唐三藏)
- solar-system-0: overlap like q-27445: In Li Bai's 静夜思, what comes next: “床前明月光，疑是地上___”? → 霜 (shuāng, “frost”): “I loved wine and travel. One night, far from home, I saw moonlight like frost by my bed and wrote 床前明月光.” Who am I? → Li Bai (李白)
- song-ci-0: overlap like early-china-0: Legend says people threw this into the Miluo River so the fish would eat it and leave Qu Yuan alone. Today it comes wrapped in leaves. What is it? → Zongzi (粽子): I'm sticky rice wrapped in bamboo leaves and tied with string. Families eat me at the Dragon Boat Festival (端午节) to remember the poet Qu Yuan. What am I? → Zongzi (粽子)
- space-race-and-astronauts-2: hard fail: correct 5, unambiguous 5, no_giveaway 2, no_overlap 5: This photo shows a US Space Shuttle docked to the Russian space station Mir in 1995. How many times did a Shuttle dock with Mir in total? → 9
- stars-and-galaxies-0: overlap like q-26705: In the old Chinese legend, ten suns burned the earth until a hero shot some down with his bow and arrows. How many did he shoot down? → 9: On a sunny day you see just one sun in the sky. In the legend, how many suns did Hou Yi (后羿) shoot down? → 9
- traditional-architecture-0: duplicate like q-27566: Whose portrait is on the front of this 100-yuan note? → Mao Zedong: This close-up shows the big portrait hanging on the gate tower of Tiananmen (天安门). Who is in the portrait? → Mao Zedong
