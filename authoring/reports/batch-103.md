# batch-103

Made by `qgen batch` on 2026-11-27 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: chinese-base
- Language: English
- Subcategories (30): climate-and-regions, early-china, qing-dynasty, late-qing-and-republic, mythical-creatures, idiom-stories, mega-projects, song-ci, modern-tv-dramas, world-cups, swimming, guinness-world-records, silk-road-and-voyages, giant-panda, space-race-and-astronauts, hong-kong-cinema, capital-cities, hundred-schools, calligraphy, chinese-cinema, ming-dynasty, chinese-medicine-history, crewed-spaceflight, chinese-painting, chinese-scientists, chinese-sports-stars, board-and-tile-games, solar-system, stars-and-galaxies, famous-scientists
- Merged: 7 (q-28386…q-28392)
- Approved: 5
- Needs work: 2
- Dropped by the pipeline: 14
- Reviewed by: claude-opus-5-5
- Claude calls: 73, about $5.30 at list price; $1.06 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-101, batch-102; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-101 | batch-102 | batch-103 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | batch |
| drafts |  | 39 | 29 | 21 |
| skipped slots |  | 13 | 10 | 12 |
| dropped |  | 16 | 16 | 14 |
| drop rate | ≤ 20.0 % | 41.0 % ✗ | 55.2 % ✗ | 66.7 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 1 |
| dropped: hard fail no_giveaway |  | 1 | 4 | 1 |
| dropped: overlap |  | 14 | 12 | 11 |
| dropped: duplicate |  | 1 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 1 |
| merged |  | 23 | 13 | 7 |
| approved |  | 19 | 11 | 5 |
| needs_work |  | 4 | 2 | 2 |
| needs_work rate | ≤ 20.0 % | 17.4 % ✓ | 15.4 % ✓ | 28.6 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 4.3 % ✓ | 7.7 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| media: no pick in review 1 |  | 6 | 2 | 0 |
| media: recovered by research |  | 5 | 2 | 0 |
| media: no pick at record |  | 1 | 0 | 0 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 8.7 % ✓ | 7.7 % ✓ | 28.6 % ✗ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 38.5 % ✗ | 41.4 % ✗ | 52.4 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | 57.1 % ✓ | 45.0 % ✗ | 33.3 % ✗ |
| max final−target gap 11–15 | ≤ 1.50 | 1.07 ✓ | 0.78 ✓ | 0.83 ✓ |
| approved 11–15 |  | 12 | 7 | 4 |
| top move | ≤ 25.0 % | 17.4 % ✓ | 38.5 % ✗ | 28.6 % ✗ |
| values move |  | 11 | 8 | 6 |
| top stimulus |  | 91.3 % | 84.6 % | 100.0 % |
| values stimulus |  | 3 | 2 | 1 |
| top clue | ≤ 60.0 % | 43.5 % ✓ | 53.8 % ✓ | 57.1 % ✓ |
| values clue |  | 3 | 3 | 3 |
| top answer_kind | ≤ 40.0 % | 21.7 % ✓ | 38.5 % ✓ | 28.6 % ✓ |
| values answer_kind |  | 7 | 6 | 5 |
| top lens | ≤ 25.0 % | 17.4 % ✓ | 15.4 % ✓ | 28.6 % ✗ |
| values lens |  | 9 | 9 | 6 |
| giveaway-step drop rate |  | n/a | n/a | n/a |
| mechanical-check rate |  | n/a | n/a | n/a |
| media share | 15.0 %–50.0 % | 8.7 % ✗ | 15.4 % ✓ | 0.0 % ✗ |
| mean fun | ≥ 3.40 | 3.18 ✗ | 3.17 ✗ | 3.10 ✗ |
| cost $ |  | $12.35 | $7.20 | $4.90 |
| $ per approved | ≤ $0.35 | $0.65 ✗ | $0.65 ✗ | $0.98 ✗ |
| calls |  | 127 | 89 | 66 |
| calls per approved |  | 6.68 | 8.09 | 13.20 |
| wall time h |  | 0.40 | 0.28 | 0.20 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 5 (0 %)
- Major among review needs work: 0 of 2 (0 %)
- Problems by kind: giveaway 1 (0 major), fact 1 (0 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 1.4; ≥ 3 on 1 of 7 (14 %)
- Audit/review agreement (both accept or both not): 5 of 7 (71 %)
- Sample: 7 audited of 7; 7 Claude calls, about $0.40

Major findings on approved questions:

None.

## Needs work

- **q-28391** (space-race-and-astronauts) You're watching a Space Shuttle deliver NASA's Destiny lab to the International Space Station. In which year is this happening? → 2001: This is a NASA/US fact (a Space Shuttle delivering the US Destiny lab) with no Chinese connection, so it breaks the chinese-base rule that questions must be answerable without any link to Europe or the Americas. It is also a minor date that no one can reason towards. If anywhere, it belongs in base, but a Chinese space topic (Shenzhou, Tiangong) would fit this bundle better.
- **q-28392** (space-race-and-astronauts) On Christmas Eve 1968, the first humans to orbit the Moon read from the Book of Genesis on live TV. Which crew was it? → The Apollo 8 crew: This is a US Apollo fact with no Chinese angle, so it doesn't fit the China-centred chinese-base bundle. Move it to base, or drop it from this bundle. A minor point if it's moved: the fun fact says all three astronauts ended the reading, but only Frank Borman spoke the closing words.

## Question axes

- move: identify 1, origin 1, record 1, sequence 1, when 2, who 1
- stimulus: none 7
- clue: direct 1, scenario 4, three_facts 2
- answer_kind: group 1, person 1, place 2, time 2, word 1
- lens: history 1, pop_culture 1, popular_science 1, school 2, science_news 1, university 1

## Dropped by the pipeline

- early-china-0: overlap like q-27520: At which festival do Chinese families eat zongzi (粽子), pyramid-shaped parcels wrapped in bamboo leaves? → Dragon Boat Festival: It is sticky rice wrapped in bamboo leaves and tied with string. Legend says people threw it into the Miluo River for Qu Yuan. What is it? → Zongzi (粽子)
- famous-scientists-0: fact-check wrong: The fun fact is misleading. Galois' letter to Auguste Chevalier, written the night before the duel, was published in the Revue Encyclopédique in September 1832, a few months after his death. What Liouville published in 1846 was Galois' collected manuscripts, not that letter. The answer and the wrong answers are fine. The claim that he 'founded group theory' is a slight overstatement, since Lagrange, Ruffini, Abel and Cauchy came earlier.: Évariste Galois was French, died at 20 after a duel in 1832, and founded group theory. Why did he show some degree-5 equations can't be solved with roots? → Their group of root symmetries is not solvable
- giant-panda-0: overlap like q-28335: You're looking at a skull of Ailuropoda microta, the oldest known species in the panda's own genus, found in a Guangxi cave. About how old is it? → About 2 million years: My skull turned up in a cave in Guangxi (广西). I was about half the size of today's pandas, but my worn teeth show I already chewed bamboo. What is my scientific name? → Ailuropoda microta
- guinness-world-records-0: overlap like q-2266: Ancient Egyptians threw it away when making mummies. It uses about a fifth of your body's energy. Your awareness comes from it. What is it? → The brain: It looks like a big wrinkly walnut, it sits inside your skull, and it has more nerve cells than any other part of your body. What is it? → The brain
- hundred-schools-0: overlap like q-26420: I conquered six states. I made everyone use the same writing, the same coins and the same weights and measures. Who am I? → Qin Shi Huang: After Shang Yang's reforms made my state of Qin strong, I conquered all the other states. I called myself the First Emperor, and clay soldiers guard my tomb. Who am I? → Qin Shi Huang (秦始皇)
- idiom-stories-0: overlap like q-27929: I sat at my loom, then rode to war in my father's place. My ballad ends with two rabbits running side by side, so no one can tell which is the girl. Who am I? → Hua Mulan: I stopped weaving when the army list named my old father. So I bought a horse, dressed as a man and fought for twelve years. Who am I? → Hua Mulan (花木兰)
- idiom-stories-1: overlap like q-26273: You're reciting 床前明月光 (chuáng qián míng yuè guāng) at bedtime, like millions of Chinese children. In which dynasty was this poem written? → Tang dynasty: Legend says a boy who skipped school met an old woman grinding an iron rod into a needle, and he grew up to be the poet Li Bai. In which dynasty did he live? → The Tang dynasty
- late-qing-and-republic-0: overlap like q-27428: British merchants brought it from India, it made many people sick, and Lin Zexu destroyed huge piles of it at Humen in 1839. What was it? → Opium: In June 1839, on a Guangdong beach, Lin Zexu had tonnes of a harmful drug mixed with salt and lime in pools, then washed out to sea. What is this event called? → 虎门销烟 (Hǔmén xiāo yān, “destroying opium at Humen”)
- qing-dynasty-0: overlap like q-27347: Look at this painted opera face (脸谱). The opera it belongs to is named after which city? → Beijing: The stage art in this photo is China's best-known opera. Which city is it named after? → Beijing
- hong-kong-cinema-0: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Before he directed Rouge (胭脂扣) and Center Stage (阮玲玉), Stanley Kwan (关锦鹏) worked as assistant director to which filmmaker? → Ann Hui (许鞍华)
- mythical-creatures-0: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: This Indian sea beast, the makara, came to China with Buddhism as 摩羯 (mójié). Its body mostly mixes which two animals? → A crocodile and a fish
- solar-system-0: overlap like q-27445: In Li Bai's 静夜思, what comes next: “床前明月光，疑是地上___”? → 霜 (shuāng, “frost”): “I loved wine and travelling. One night, moonlight before my bed looked like frost, and gazing up at the Moon made me miss home.” Who am I? → Li Bai (李白)
- song-ci-0: overlap like early-china-0: It is sticky rice wrapped in bamboo leaves and tied with string. Legend says people threw it into the Miluo River for Qu Yuan. What is it? → Zongzi (粽子): I'm sticky rice wrapped in leaves and tied with string. People eat me at the Dragon Boat Festival (端午节) to remember the poet Qu Yuan. What am I? → Zongzi (粽子)
- stars-and-galaxies-0: overlap like q-26705: In the old Chinese legend, ten suns burned the earth until a hero shot some down with his bow and arrows. How many did he shoot down? → 9: On a hot summer day, you see just one sun in the sky. In the legend, how many suns did Hou Yi (后羿) shoot down? → 9
