# batch-102

Made by `qgen batch` on 2026-11-27 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (36): chinese-rivers-and-lakes, climate-and-regions, early-china, qing-dynasty, late-qing-and-republic, mythical-creatures, idiom-stories, mega-projects, song-ci, modern-tv-dramas, hong-kong-cinema, world-cups, swimming, guinness-world-records, traditional-architecture, silk-road-and-voyages, giant-panda, space-race-and-astronauts, water-margin, bronzes-and-porcelain, capital-cities, hundred-schools, calligraphy, chinese-cinema, ming-dynasty, confucianism, chinese-medicine-history, crewed-spaceflight, chinese-painting, chinese-scientists, chinese-sports-stars, ancient-chinese-maths, board-and-tile-games, solar-system, stars-and-galaxies, famous-scientists
- Merged: 13 (q-28373…q-28385)
- Approved: 11
- Needs work: 2
- Dropped by the pipeline: 16
- Reviewed by: claude-opus-5-5
- Claude calls: 102, about $7.93 at list price; $0.72 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-100, batch-101; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-100 | batch-101 | batch-102 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | batch |
| drafts |  | 46 | 39 | 29 |
| skipped slots |  | 16 | 13 | 10 |
| dropped |  | 21 | 16 | 16 |
| drop rate | ≤ 20.0 % | 45.7 % ✗ | 41.0 % ✗ | 55.2 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 4 | 1 | 4 |
| dropped: overlap |  | 16 | 14 | 12 |
| dropped: duplicate |  | 1 | 1 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 25 | 23 | 13 |
| approved |  | 19 | 19 | 11 |
| needs_work |  | 6 | 4 | 2 |
| needs_work rate | ≤ 20.0 % | 24.0 % ✗ | 17.4 % ✓ | 15.4 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 8.0 % ✓ | 4.3 % ✓ | 7.7 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.0 % ✓ | 4.3 % ✓ | 0.0 % ✓ |
| media: no pick in review 1 |  | 3 | 6 | 2 |
| media: recovered by research |  | 2 | 5 | 2 |
| media: no pick at record |  | 1 | 1 | 0 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 16.0 % ✗ | 8.7 % ✓ | 7.7 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 37.0 % ✗ | 38.5 % ✗ | 41.4 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 48.5 % ✗ | 57.1 % ✓ | 45.0 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.00 ✓ | 1.07 ✓ | 0.78 ✓ |
| approved 11–15 |  | 11 | 12 | 7 |
| top move | ≤ 25.0 % | 16.0 % ✓ | 17.4 % ✓ | 38.5 % ✗ |
| values move |  | 11 | 11 | 8 |
| top stimulus |  | 88.0 % | 91.3 % | 84.6 % |
| values stimulus |  | 3 | 3 | 2 |
| top clue | ≤ 60.0 % | 44.0 % ✓ | 43.5 % ✓ | 53.8 % ✓ |
| values clue |  | 4 | 3 | 3 |
| top answer_kind | ≤ 40.0 % | 20.0 % ✓ | 21.7 % ✓ | 38.5 % ✓ |
| values answer_kind |  | 7 | 7 | 6 |
| top lens | ≤ 25.0 % | 16.0 % ✓ | 17.4 % ✓ | 15.4 % ✓ |
| values lens |  | 9 | 9 | 9 |
| giveaway-step drop rate |  | n/a | n/a | n/a |
| mechanical-check rate |  | n/a | n/a | n/a |
| media share | 15.0 %–50.0 % | 12.0 % ✗ | 8.7 % ✗ | 15.4 % ✓ |
| mean fun | ≥ 3.40 | 3.26 ✗ | 3.18 ✗ | 3.17 ✗ |
| cost $ |  | $12.36 | $12.35 | $7.20 |
| $ per approved | ≤ $0.35 | $0.65 ✗ | $0.65 ✗ | $0.65 ✗ |
| calls |  | 136 | 127 | 89 |
| calls per approved |  | 7.16 | 6.68 | 8.09 |
| wall time h |  | 0.45 | 0.40 | 0.27 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 11 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: overlap 1 (0 major), difficulty 1 (0 major), style 2 (0 major)
- Mean |audit − final difficulty|: 1.1; ≥ 3 on 1 of 13 (8 %)
- Audit/review agreement (both accept or both not): 11 of 13 (85 %)
- Sample: 13 audited of 13; 13 Claude calls, about $0.73

Major findings on approved questions:

None.

## Needs work

- **q-28375** (chinese-cinema) Song of the Fishermen (渔光曲) ran for a record 84 days in Shanghai in 1934. In which city did it win an honor the next year? → Moscow: Hint 2 gives the answer away: "far to the north-west of China, in a country that shared a long border with it" fits only Moscow among the options, so it leaves only one choice before hint 3. Hint 2 should only narrow things down. For example, it could say the prize came from a festival that was new in 1935. That leaves Venice (1932) as a fair rival after hint 1. The fact itself is correct: the film won an honorary prize at the 1935 Moscow festival.
- **q-28383** (space-race-and-astronauts) Vladimír Remek of Czechoslovakia flew in 1978, Pham Tuan of Vietnam became the first Asian in space in 1980, and India's Rakesh Sharma flew in 1984. Which Soviet programme flew them? → Interkosmos: The question doesn't fit the chinese-base bundle. It asks about a Soviet programme for cosmonauts from Czechoslovakia, Vietnam and India, which Chinese school and everyday knowledge doesn't cover, and only the fun fact mentions China. It belongs in `base`, or should be dropped from this bundle.

## Question axes

- move: cause_effect 1, identify 5, odd_one_out 1, origin 1, record 1, sequence 1, when 2, word_meaning 1
- stimulus: detail 2, none 11
- clue: direct 3, scenario 3, three_facts 7
- answer_kind: group 5, person 1, place 1, thing 3, time 2, word 1
- lens: body_senses 1, educational_media 1, everyday 2, history 1, nature 1, pop_culture 2, school 2, science_news 2, university 1

## Dropped by the pipeline

- early-china-0: overlap like q-27520: At which festival do Chinese families eat zongzi (粽子), pyramid-shaped parcels wrapped in bamboo leaves? → Dragon Boat Festival: Legend says people dropped this food into the Miluo River (汨罗江) for Qu Yuan. It is made of sticky rice and wrapped in leaves. What is it? → Zongzi (粽子)
- famous-scientists-0: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Évariste Galois died at 20 in 1832, and his theory shows why no root formula exists for every fifth-degree equation. What is the reason? → Its symmetry group is not solvable
- giant-panda-0: overlap like q-28335: You're looking at a skull of Ailuropoda microta, the oldest known species in the panda's own genus, found in a Guangxi cave. About how old is it? → About 2 million years: You're in a museum looking at a skull of Ailuropoda microta, an early panda found in a Guangxi cave. About how long was its body? → About 1 m
- guinness-world-records-0: overlap like q-2266: Ancient Egyptians threw it away when making mummies. It uses about a fifth of your body's energy. Your awareness comes from it. What is it? → The brain: It has more nerve cells than any other part of your body, about 86 billion. It weighs about 1.4 kg and is wrinkly like a walnut. What is it? → The brain
- hundred-schools-0: overlap like q-26420: I conquered six states. I made everyone use the same writing, the same coins and the same weights and measures. Who am I? → Qin Shi Huang: I started as king of the State of Qin. I joined the warring states into one China and made everyone use one script and one coin. An army of clay soldiers guards my tomb. Who am I? → Qin Shi Huang (秦始皇)
- idiom-stories-0: overlap like q-25976: In the Great Race legend, Rat is to Ox as Snake is to… → Horse: Nezha is to his wind-fire wheels (风火轮) as Mulan, going to war in her father's place, is to her… → Horse
- idiom-stories-1: overlap like q-26273: You're reciting 床前明月光 (chuáng qián míng yuè guāng) at bedtime, like millions of Chinese children. In which dynasty was this poem written? → Tang dynasty: The boy who watched an old woman grind an iron rod into a needle (铁杵磨成针) grew up to be the poet Li Bai. In which dynasty did he live? → The Tang dynasty
- late-qing-and-republic-0: overlap like q-27428: British merchants brought it from India, it made many people sick, and Lin Zexu destroyed huge piles of it at Humen in 1839. What was it? → Opium: In June 1839, Lin Zexu's men mixed seized drugs with salt and lime in big pits on a Guangdong beach, then let the sea wash them away. What is this event called? → 虎门销烟 (Hǔmén Xiāo Yān, Destruction of Opium at Humen)
- qing-dynasty-0: overlap like q-27347: Look at this painted opera face (脸谱). The opera it belongs to is named after which city? → Beijing: This photo shows a performer from China's best-known opera, the 国粹 (guócuì) of the stage. Which city is it named after? → Beijing
- board-and-tile-games-0: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Modern mahjong is said to have taken shape in the 1800s in a port city where the Qing official Chen Yumen fixed its rules. Which city? → Ningbo
- modern-tv-dramas-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: You're watching Empresses in the Palace (甄嬛传) when a woman cries “皇上，臣妾做不到啊！” to the emperor. Who is she? → Empress Yixiu (宜修)
- silk-road-and-voyages-0: overlap like q-26041: In the 1986 TV series “Journey to the West”, Tang Seng heads west with a monkey, a pig and a river ogre. Who else is in the team? → A white dragon horse: You're watching the 1986 TV series “Journey to the West” as a demon attacks. Which team member does NOT fight it with a weapon? → The White Dragon Horse
- solar-system-0: overlap like q-27445: In Li Bai's 静夜思, what comes next: “床前明月光，疑是地上___”? → 霜 (shuāng, “frost”): “I loved wine and travelling across China. One night, moonlight on my floor looked like frost and made me miss home, so I wrote 静夜思. Who am I?” → Li Bai (李白)
- song-ci-0: overlap like early-china-0: Legend says people dropped this food into the Miluo River (汨罗江) for Qu Yuan. It is made of sticky rice and wrapped in leaves. What is it? → Zongzi (粽子): I'm sticky rice wrapped in leaves and tied up tight. People say I was thrown into the river for the poet Qu Yuan. What am I? → Zongzi (粽子)
- space-race-and-astronauts-0: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: You're watching astronauts float through Destiny, the main US science lab on the International Space Station. In which year was it attached? → 2001
- stars-and-galaxies-0: overlap like q-26705: In the old Chinese legend, ten suns burned the earth until a hero shot some down with his bow and arrows. How many did he shoot down? → 9: This archer is Hou Yi (后羿), the hero of a famous Chinese legend. How many suns did he shoot down? → 9
