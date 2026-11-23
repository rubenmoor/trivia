# tr-zh-Hans-5

Made by `qgen batch --translate zh-Hans` on 2026-11-23 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 299
- Approved: 294
- Needs work: 5
- Not travelling: 1 (1 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 594, about $26.76 at list price; $0.08 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-5&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-3 | tr-zh-Hans-4 | tr-zh-Hans-5 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 297 | 300 | 299 |
| not travelling |  | 3 | 0 | 1 |
| not travelling confirmed |  | 3 | 0 | 1 |
| rejected rate | ≤ 20.0 % | 1.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| approved |  | 295 | 294 | 294 |
| needs_work |  | 2 | 6 | 5 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 2.0 % ✓ | 1.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 1.0 % ✓ | 0.3 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 1.0 % ✓ | 1.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.3 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 78.3 % ✗ | 83.3 % ✗ | 83.3 % ✗ |
| cost $ |  | $22.51 | $24.58 | $24.61 |
| $ per approved |  | $0.08 | $0.08 | $0.08 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 10 of 59 (17 %)
- Major among review needs work: 1 of 1 (100 %)
- Problems by kind: giveaway 3 (2 major), media 16 (11 major), style 3 (1 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 50 of 60 (83 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.15

Major findings on approved questions:

- **q-21507**: media, giveaway — The essential audio has no file (media title is null), so "听一听" can't be played as it is. In Chinese, hint 2 "用嘴敲打树木" practically spells out the name 啄木鸟 ("the bird that pecks wood"), which makes it a minor giveaway. Rewording it, for example to "这声音像有人在快速敲门", would fix that. The facts check out (drumming isn't made with the throat; the tongue wraps around the skull), and the wording reads naturally. (http://127.0.0.1:8001/review/q-21507)
- **q-21510**: media — The media is marked essential, but no file was picked (title null). The question opens with “这个充满气体的器官取自一条鱼”, which points at a picture of a swim bladder, so it doesn't work on the TV without that image. The translation itself is faithful and reads naturally. I checked the facts: bony fish have swim bladders, while sharks, rays, lampreys and hagfish don't. Sharks rely on an oily liver, and the swim bladder shares an evolutionary origin with lungs. (http://127.0.0.1:8001/review/q-21510)
- **q-21774**: media — The question says “看照片” and marks the media as essential, but no file was picked (title null). Without the photo it can't be played, and the text alone also fits a record player, which has a disc and a tonearm too. The translation itself is accurate and natural: «磁头» in the fun fact is even more precise than the source's “arm”, hint 3 points to 硬 without writing it, and it doesn't overlap with the 软盘 question. (http://127.0.0.1:8001/review/q-21774)
- **q-22084**: media — The media is marked essential, but no file is attached (title null). The question opens with "看这幅名画的局部", so players would be asked to look at a detail that isn't on screen; it needs a sfumato detail, such as the Mona Lisa's face. I found no problems with the translation itself: 晕涂法, 点彩法, 厚涂法 and 灰调画法 are the standard Chinese terms and match the source, and the hints and fun fact are accurate (Leonardo's glaze layers measure only a few micrometres). (http://127.0.0.1:8001/review/q-22084)
- **q-22133**: media — The media is essential but no file was picked (title is null), and the question says "穿上这样的防护服", so it needs a photo of an aluminized proximity or volcanologist suit. The translation itself is faithful and natural. The facts hold: these suits have an aluminized outer layer that reflects about 90% of radiant heat, and silver, steel and titanium are clearly wrong. Hint 3's “锡纸” clue is accurate and works well in Chinese, and it doesn't contain the character 铝. (http://127.0.0.1:8001/review/q-22133)
- **q-22657**: media — No media file is attached (the title is null), but the media role is essential and the question opens with "看这片沙地", so the players have nothing to look at. A long jump pit with its take-off board needs to be picked before this is played. Otherwise the translation is faithful and reads naturally: all four options are noun phrases of similar length, the hints and the fun fact are correct (the jump is measured to the nearest mark), and no related question asks the same thing. (http://127.0.0.1:8001/review/q-22657)
- **q-22926**: media — The media is marked essential and the question says “看看这盘摆好的国际象棋”, but no file was picked (title null), so there is no chess set to look at. The question is still answerable from knowledge, though. The translation itself is faithful and reads naturally, and the facts check out: there are 4 rooks, the hints are true, and castling is the only move where two pieces move at once. (http://127.0.0.1:8001/review/q-22926)
- **q-22968**: media — The media is marked essential but no file was picked (title null). The question opens with "这幅画里是雷神托尔和他的锤子", so on the TV it points at a painting that isn't there. The translation itself is faithful and natural: 北欧 = Scandinavia, and the options, hints and the Thursday fun fact are correct. (http://127.0.0.1:8001/review/q-22968)
- **q-23495**: media — The media is marked essential, but no file was picked (title null). The question opens with "看看这种蔬菜" and never names the pumpkin, so without the picture it points at nothing; a pumpkin photo needs to be attached. Everything else checks out: the translation is faithful and natural, the answer and fun fact match Perrault (mice into horses, a rat into the coachman), all four options have the same form, and the hints don't give the answer away. (http://127.0.0.1:8001/review/q-23495)
- **q-23511**: media — The media is marked essential but no file was picked (title null). The question opens with "看看这艘船", so it can't be played without a submarine photo. The translation itself is faithful and natural, the options and hints fit, and the fun fact about ballast tanks is correct. (http://127.0.0.1:8001/review/q-23511)

## Needs work

- **q-22745** (space) 人们把这样的一道光叫作“流星”。它其实是什么？ → 在大气中燃烧的太空小石块: Fact check: uncertain. The answer and wrong answers are fine. The third hint and the fun fact say meteors are usually smaller than a grain of sand. Sources more often say visible meteors come from particles about the size of a sand grain to a pea or pebble (roughly 1 mm to 1 cm). Only the faintest ones come from finer dust. This is an overstatement, and I did not run a search to check it.
- **q-23311** (world-war-ii) 战争让可口可乐糖浆运不进德国，于是德国人发明了一种新的橙味汽水——芬达。这是在哪个年代？ → 20世纪40年代: Source: the question calls the original wartime Fanta "a new orange soda", but the 1940 German Fanta was made from by-products like whey and apple pomace and wasn't orange-flavoured. Orange Fanta came in the 1950s in Italy. The source should drop "orange" (in zh: 橙味), e.g. "a new soda, Fanta". Then the translation can follow.
- **q-23514** (volcanoes) 金星上最高的火山以一位埃及真理女神命名。2023年，旧雷达图像显示它的一个火山口变了形。它叫什么？ → 玛阿特山: source: Hint 2 is factually wrong in the English source, and the translation repeats it faithfully. Maat Mons is about 8 km above Venus's mean planetary radius but only about 5 km above the surrounding plains. Fix the source hint to "It rises about 8 km above Venus's mean surface" (or "about 5 km above the surrounding plains"), then hint 2 in zh-Hans should follow it, e.g. «它高出金星平均表面约8公里。» Fact check: wrong. The answer (玛阿特山, Maat Mons) is right. The Magellan images and the 2023 vent change (Herrick & Hensley, Science) also check out, and the three wrong answers are other Venus volcanoes. Hint 2 is inaccurate: Maat Mons is about 8 km above Venus's mean surface radius, but only about 5 km above the surrounding plains.
- **q-23830** (planes) 看看这张照片。这个人是做什么工作的？ → 飞行员: The Chinese translation is faithful and reads naturally. The problem is in the source. The kept essential image (File:Cockpit_of_P-8A_Poseidon_of_VP-16_in_March_2014.JPG) shows naval aviators flying a US Navy P-8A patrol plane, not an airline pilot in uniform as the media note asks. That makes hint 1 ("vehicle full of passengers", 坐满乘客的交通工具) untrue for the person in the photo. Source: replace the photo with a clear one of an airline pilot in a passenger-jet cockpit, or reword hint 1 so it fits any pilot. Fact check: wrong. The image doesn't match the text. It shows the cockpit of a US Navy P-8A Poseidon, a military patrol aircraft. Its two crew are naval aviators on an MH370 search mission. The media note asks for an airline pilot in uniform. The hint says the person drives a vehicle full of passengers, which doesn't fit a military aircraft. The image is marked essential, so a viewer can't be sure it shows a pilot.
- **q-23884** (wonders-of-the-world) 古斯塔夫·埃菲尔的公司为1889年巴黎世界博览会建造了这座塔。它是用什么材料建成的？ → 铁: In Chinese the tower is universally called 埃菲尔铁塔, so its own name gives away the answer 铁. The essential photo makes every player think of that name. On top of that, the description literally says "铁娘子". Rewording can't fix this, because the answer is built into the tower's Chinese name. Mark it travels: no (reason other / about_language: the answer is part of the landmark's Chinese name).

## Not travelling

- **q-23545** other, confirmed: Dyslexia is common, often runs in families, and has nothing to do with intelligence. What does it mainly make harder? → Reading and spelling (The Chinese name of dyslexia (阅读障碍/读写障碍/诵读困难) literally contains 读/阅读, so naming the condition in the question gives the answer (reading and spelling) away; without the name the question has no clue.)

## Stale re-translated

None.
