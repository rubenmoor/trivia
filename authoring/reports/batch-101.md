# batch-101

Made by `qgen batch` on 2026-11-27 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (47): swimming, chinese-rivers-and-lakes, china-at-the-olympics, guinness-world-records, mythical-creatures, world-cups, toys, climate-and-regions, provinces, idiom-stories, modern-tv-dramas, hong-kong-cinema, mega-projects, popular-chinese-fiction, late-qing-and-republic, song-ci, school-and-daily-life, dream-of-the-red-chamber, lunar-and-planetary-missions, qing-dynasty, early-china, silk-road-and-voyages, modern-chinese-literature, giant-panda, traditional-architecture, water-margin, space-race-and-astronauts, team-sports-in-china, three-kingdoms-to-sui, bronzes-and-porcelain, chinese-cinema, capital-cities, confucianism, hundred-schools, chinese-medicine-history, calligraphy, chinese-painting, tang-dynasty, ming-dynasty, crewed-spaceflight, ancient-chinese-maths, board-and-tile-games, chinese-scientists, chinese-sports-stars, solar-system, stars-and-galaxies, famous-scientists
- Merged: 23 (q-28350…q-28372)
- Approved: 19
- Needs work: 4
- Dropped by the pipeline: 16
- Reviewed by: claude-opus-5-5
- Claude calls: 150, about $13.67 at list price; $0.72 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-99, batch-100; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-99 | batch-100 | batch-101 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | batch |
| drafts |  | 62 | 46 | 39 |
| skipped slots |  | 23 | 16 | 13 |
| dropped |  | 26 | 21 | 16 |
| drop rate | ≤ 20.0 % | 41.9 % ✗ | 45.7 % ✗ | 41.0 % ✗ |
| dropped: hard fail correct |  | 1 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 4 | 4 | 1 |
| dropped: overlap |  | 21 | 16 | 14 |
| dropped: duplicate |  | 0 | 1 | 1 |
| dropped: fact-check wrong |  | 1 | 0 | 0 |
| merged |  | 36 | 25 | 23 |
| approved |  | 32 | 19 | 19 |
| needs_work |  | 4 | 6 | 4 |
| needs_work rate | ≤ 20.0 % | 11.1 % ✓ | 24.0 % ✗ | 17.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.8 % ✓ | 8.0 % ✓ | 4.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 5.6 % ✓ | 4.0 % ✓ | 4.3 % ✓ |
| media: no pick in review 1 |  | 7 | 3 | 6 |
| media: recovered by research |  | 5 | 2 | 5 |
| media: no pick at record |  | 2 | 1 | 1 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 2.8 % ✓ | 16.0 % ✗ | 8.7 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 33.9 % ✗ | 37.0 % ✗ | 38.5 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 45.2 % ✗ | 48.5 % ✗ | 57.1 % ✓ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.00 ✓ | 1.07 ✓ |
| approved 11–15 |  | 14 | 11 | 12 |
| top move | ≤ 25.0 % | 16.7 % ✓ | 16.0 % ✓ | 17.4 % ✓ |
| values move |  | 12 | 11 | 11 |
| top stimulus |  | 91.7 % | 88.0 % | 91.3 % |
| values stimulus |  | 2 | 3 | 3 |
| top clue | ≤ 60.0 % | 41.7 % ✓ | 44.0 % ✓ | 43.5 % ✓ |
| values clue |  | 5 | 4 | 3 |
| top answer_kind | ≤ 40.0 % | 19.4 % ✓ | 20.0 % ✓ | 21.7 % ✓ |
| values answer_kind |  | 7 | 7 | 7 |
| top lens | ≤ 25.0 % | 16.7 % ✓ | 16.0 % ✓ | 17.4 % ✓ |
| values lens |  | 10 | 9 | 9 |
| giveaway-step drop rate |  | n/a | n/a | n/a |
| mechanical-check rate |  | n/a | n/a | n/a |
| media share | 15.0 %–50.0 % | 8.3 % ✗ | 12.0 % ✗ | 8.7 % ✗ |
| mean fun | ≥ 3.40 | 3.32 ✗ | 3.26 ✗ | 3.18 ✗ |
| cost $ |  | $17.70 | $12.36 | $12.35 |
| $ per approved | ≤ $0.35 | $0.55 ✗ | $0.65 ✗ | $0.65 ✗ |
| calls |  | 193 | 136 | 127 |
| calls per approved |  | 6.03 | 7.16 | 6.68 |
| wall time h |  | 0.59 | 0.45 | 0.40 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 19 (0 %)
- Major among review needs work: 2 of 4 (50 %)
- Problems by kind: giveaway 3 (1 major), ambiguity 1 (1 major), overlap 1 (0 major), media 1 (1 major), difficulty 2 (1 major)
- Mean |audit − final difficulty|: 1.2; ≥ 3 on 2 of 23 (9 %)
- Audit/review agreement (both accept or both not): 21 of 23 (91 %)
- Sample: 23 audited of 23; 23 Claude calls, about $1.32

Major findings on approved questions:

None.

## Needs work

- **q-28357** (famous-scientists) Andrew Wiles proved Fermat's Last Theorem in 1994 by proving a key case of a conjecture linking elliptic curves to modular forms. Which conjecture? → The Taniyama–Shimura conjecture: Wrong bundle: this is a European/Western maths-history fact (Fermat, Andrew Wiles), with no connection to Chinese school knowledge or culture. The chinese-base rule wants China-centred questions and sends well-known facts about other countries to base, so this question should move to base or be dropped. Rewriting it for chinese-base would make it a different question.
- **q-28359** (ming-dynasty) The film “Noryang: Deadly Sea” (2023) shows the last sea battle of Wanli's Korea campaign. About how old was Ming general Deng Zilong (邓子龙) when he fought in it? → About 70: The description gives the answer away. "Some generals retire to grow orchids" tells players he was already at retirement age, which rules out "About 30" and makes "About 50" unlikely before any hint is shown. The description should play on the theme (the sea, the Ming, Korea) without hinting at his age. One more thing to consider: Deng Zilong died in this battle, so asking his age there comes close to a death topic.
- **q-28363** (bronzes-and-porcelain) This close-up shows part of something you use at almost every Chinese meal. What is it? → A rice bowl: No candidate fits the essential slot. The question says "This close-up shows part of" an everyday rice bowl, but #1 shows the underside of a museum bowl with a "K2988" label, #2 puts a vase (a wrong option) next to the bowl, and #3 shows a whole decorated museum bowl, not a close-up. No new search is allowed. The slot needs a close-up of a plain eating bowl's rim and side. Another option is to reword the question so it doesn't promise a close-up (for example "This is something you use at almost every Chinese meal") and use #3. No suitable picture found for this question.
- **q-28369** (space-race-and-astronauts) You're looking at a model of Salyut 7 in a space museum. In which year was this Soviet space station launched? → 1982: This doesn't fit the chinese-base bundle. Salyut 7 is a Soviet station, a fact about another country that has nothing to do with what a Chinese family learns or knows, so it belongs in base if anywhere. It's also only hard because it asks for a minor launch year (April 1982), which the house style rules out for a 15. Hint 3's reform-and-opening-up link is there just to make it look Chinese. Drop it from this bundle, or replace it with a China-centred space question (for example about Tiangong or Shenzhou).

## Question axes

- move: analogy 1, cause_effect 3, estimate 3, identify 4, odd_one_out 3, origin 1, purpose 1, sequence 1, when 2, who 1, word_meaning 3
- stimulus: detail 1, none 21, photo 1
- clue: direct 6, scenario 7, three_facts 10
- answer_kind: group 5, number 3, person 2, place 3, thing 3, time 2, word 5
- lens: body_senses 4, educational_media 2, history 3, language 3, pop_culture 2, popular_science 1, school 4, science_news 1, university 3

## Dropped by the pipeline

- chinese-medicine-history-0: overlap like q-27811: Many people drop small, thin, oval dried berries like the ones in the photo into hot water or tea. What are they? → Goji berries (枸杞): These tiny, bright red, oval dried berries are famous for floating in thermos flasks of hot water. What are they called? → Goji berries (枸杞)
- chinese-rivers-and-lakes-0: overlap like q-26326: A landslide fills a narrow valley, blocks the river completely, and the water keeps flowing in. What forms behind the pile of rock? → A lake: The Three Gorges Dam blocks the Yangtze with a giant wall. Behind it, the water rose over 100 m and spread back about 600 km. What did the river become there? → A long lake
- dream-of-the-red-chamber-0: overlap like q-26090: I lost my husband young and quietly raise my son, Jia Lan. My home in the garden is Paddy-Sweet Cottage (稻香村), built to look like a farm. Who am I? → Li Wan: In the register of the Twelve Beauties of Jinling, my mother’s picture shows a pot of orchids. Late in the novel, I pass the imperial exams with my uncle Baoyu. Who am I? → Jia Lan
- early-china-0: overlap like q-27520: At which festival do Chinese families eat zongzi (粽子), pyramid-shaped parcels wrapped in bamboo leaves? → Dragon Boat Festival: Families eat this at the Dragon Boat Festival in memory of the poet Qu Yuan (屈原). It's sticky rice wrapped in leaves. What is it? → Zongzi (粽子)
- giant-panda-0: overlap like q-28335: You're looking at a skull of Ailuropoda microta, the oldest known species in the panda's own genus, found in a Guangxi cave. About how old is it? → About 2 million years: I'm a panda only about half the size of today's giant panda. My fossil skull was found in a karst cave in Guangxi, and my worn teeth show I already chewed bamboo. What am I? → Ailuropoda microta
- guinness-world-records-0: overlap like q-2266: Ancient Egyptians threw it away when making mummies. It uses about a fifth of your body's energy. Your awareness comes from it. What is it? → The brain: It sits safe inside your skull, it holds about 86 billion nerve cells (more than any other organ) and it controls your body. What is it? → The brain
- hundred-schools-0: overlap like q-26420: I conquered six states. I made everyone use the same writing, the same coins and the same weights and measures. Who am I? → Qin Shi Huang: I became King of Qin at 13. Thanks to Shang Yang's old laws my state was strong, so I conquered the other six and called myself the first emperor. Who am I? → Qin Shi Huang (秦始皇)
- idiom-stories-1: overlap like q-26273: You're reciting 床前明月光 (chuáng qián míng yuè guāng) at bedtime, like millions of Chinese children. In which dynasty was this poem written? → Tang dynasty: Li Bai saw an old woman grinding an iron rod into a needle and decided to study harder. In which dynasty did he live? → The Tang dynasty
- late-qing-and-republic-0: overlap like q-27428: British merchants brought it from India, it made many people sick, and Lin Zexu destroyed huge piles of it at Humen in 1839. What was it? → Opium: This statue honours the official who had seized opium destroyed on the beach at Humen in 1839. Who is he? → Lin Zexu (林则徐)
- lunar-and-planetary-missions-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: It launched in August 2022 on a SpaceX rocket, reached the Moon in December and carries NASA's ShadowCam. What is South Korea's first Moon orbiter called? → Danuri
- qing-dynasty-0: overlap like q-27347: Look at this painted opera face (脸谱). The opera it belongs to is named after which city? → Beijing: The stage art in this photo is named after which Chinese city? → Beijing
- silk-road-and-voyages-0: overlap like q-26041: In the 1986 TV series “Journey to the West”, Tang Seng heads west with a monkey, a pig and a river ogre. Who else is in the team? → A white dragon horse: You're watching “Journey to the West” on TV. Which of these pilgrims does NOT walk west on two legs? → The White Dragon Horse
- solar-system-0: overlap like q-27445: In Li Bai's 静夜思, what comes next: “床前明月光，疑是地上___”? → 霜 (shuāng, “frost”): “I loved wine and the Moon. One night, far from home, moonlight on my floor looked like frost, so I wrote 静夜思. Who am I?” → Li Bai (李白)
- song-ci-0: overlap like early-china-0: Families eat this at the Dragon Boat Festival in memory of the poet Qu Yuan (屈原). It's sticky rice wrapped in leaves. What is it? → Zongzi (粽子): I'm sticky rice wrapped in bamboo leaves and tied with string. You eat me at the Dragon Boat Festival (端午节), the day that remembers the poet Qu Yuan. What am I? → Zongzi (粽子)
- stars-and-galaxies-0: overlap like q-26705: In the old Chinese legend, ten suns burned the earth until a hero shot some down with his bow and arrows. How many did he shoot down? → 9: You look up on a sunny day and see just one Sun. In the legend, how many suns did Hou Yi (后羿) shoot down? → 9
- traditional-architecture-0: duplicate like q-27566: Whose portrait is on the front of this 100-yuan note? → Mao Zedong: This giant portrait hangs above the central doorway of Tiananmen (天安门) in Beijing. Who is shown in it? → Mao Zedong
