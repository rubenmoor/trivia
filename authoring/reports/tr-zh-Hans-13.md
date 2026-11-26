# tr-zh-Hans-13

Made by `qgen batch --translate zh-Hans` on 2026-11-26 (plan 66, D-81): `chinese-base` questions translated into Simplified Chinese. Generated file: don't edit by hand.

- Sources: 300 (0 stale re-translated)
- Translated: 300
- Approved: 293
- Needs work: 7
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 577, about $27.72 at list price; $0.09 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-zh-Hans-13&locale=zh-Hans

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-zh-Hans-11 | tr-zh-Hans-12 | tr-zh-Hans-13 |
|---|---|---:|---:|---:|
| sources |  | 300 | 300 | 300 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 300 | 300 | 300 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 298 | 298 | 293 |
| needs_work |  | 2 | 2 | 7 |
| needs_work rate | ≤ 20.0 % | 0.7 % ✓ | 0.7 % ✓ | 2.3 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.7 % ✓ | 0.3 % ✓ | 2.3 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.3 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.3 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 100.0 % ✓ | 100.0 % ✓ | 95.0 % ✓ |
| cost $ |  | $23.69 | $24.34 | $25.47 |
| $ per approved |  | $0.08 | $0.08 | $0.09 |
| **health** | | ✓ pass | ✓ pass | ✓ pass |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 59 (3 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 6 (2 major), fact 1 (0 major), overlap 1 (1 major), style 2 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 57 of 60 (95 %)
- Sample: 60 audited of 60; 60 Claude calls, about $2.26

Major findings on approved questions:

- **q-26513**: overlap, giveaway — Related q-26976 says "你的帅被将军，无处可躲……这叫什么？", which states the fact this question asks: the game ends when the 帅/将 is trapped. Seeing one gives the other away. Minor point: hint 2 ("必须待在九宫里") also fits 士（仕）, so it only narrows the options. The swap of distractors (车 → 兵) and the rewritten hint 3 are otherwise faithful and correct. (http://127.0.0.1:8001/review/q-26513)
- **q-26905**: giveaway — The source keeps "Chu Ci (楚辞)" for hint 2, but the translation puts 《楚辞·渔父》 into the question text. Most Chinese players link 楚辞 with 屈原, and the three wrong answers (Li Bai, Du Fu, Tao Yuanming) all lived centuries after the Chu Ci, so the question now answers itself. It should say just 《渔父》 and keep 楚辞 as hint 2 (the new hint 2 about an exiled man also narrows things a lot, but that only counts as minor). The facts check out: the fisherman sings the 沧浪 song as he leaves Qu Yuan, "颜色憔悴，形容枯槁" is a real quote from the text, and Canglang Pavilion, first built in the Northern Song, is usually called Suzhou's oldest surviving garden. (http://127.0.0.1:8001/review/q-26905)

## Needs work

- **q-26079** (dialects) 台湾很多人说它，祖先多来自泉州和漳州，热门歌曲《爱拼才会赢》就是用它唱的。这是哪种语言？ → 闽南语: Fact check: wrong. The distractor 潮州话 (Teochew) is usually classed as a variety of Southern Min (闽南语), so it isn't clearly wrong. Hint 1 (属于闽方言) also fits it. This was checked from memory, not with a search.
- **q-26104** (dynasties-overview) 《沁园春·雪》中“只识弯弓射大雕”的那位，建立了史上最大的陆上连片帝国。他是谁？ → 成吉思汗: Hint 1 is mistranslated. The source says "grasslands north of China", but «来自中国北方的大草原» means "grasslands in northern China". Genghis Khan was born on the Mongolian steppe, in today's Mongolia, so the hint is now factually misleading. It should read something like «他来自中国以北的蒙古大草原。» The rest of the translation is faithful and natural. Fact check: wrong. Hint 1 says Genghis Khan came from the northern grasslands 'of China'. He was born in the Mongolian steppe, which is outside China today, so the hint is misleading. The rest checks out.
- **q-26159** (four-great-inventions) 黑龙江铜火铳是现存最古老的枪炮之一。它是从中国更早的哪种火药武器发展来的？ → 火矛: The answer «火矛» is a literal calque of "fire lance". It is not the standard Chinese term: Chinese histories and textbooks call this weapon «火枪» (for example 陈规's 长竹竿火枪, 1132). The fun fact then says the weapon "was called 火枪", which contradicts the answer and confuses players. It also replaces the source's fun fact (34 cm long, about 3.5 kg) with a different claim. Use «火枪» or «火枪（长竹竿火枪）» as the answer and restore the source's fun fact. Fact check: wrong. The standard Chinese name for the precursor is 火枪 (fire lance), not 火矛. The question text and answer use a non-standard term. The fun fact then says Song records call 火矛 '火枪', which is confusing, and modern 火枪 can also mean a musket. The bamboo or paper tube and the spear-mounted tube do describe the fire lance.
- **q-26469** (chinese-tech-brands) 在中国城市里，有些车牌是绿色的，比蓝牌多一位，还常常不受限行限制。哪种车挂这种车牌？ → 电动汽车: Fact check: wrong. The answer (new energy vehicles get green 8-character plates, often exempt from driving restrictions) is right. But the wrong answer "出租车" is not reliably wrong. Many Chinese cities, such as Shenzhen, have fully electric taxis. These carry green new-energy plates, so a taxi can be a green-plate vehicle. Also, "电动汽车" is narrower than the real category: plug-in hybrids and fuel-cell vehicles get green plates too. I did not run searches for this. It rests on my own knowledge of the plate rules.
- **q-26967** (apps-and-online-life) 一位明星选手的视频下面，评论区刷满了“YYDS”（永远的神）。这个词大约在哪一年成为全国热门流行语？ → 2021年前后: source: hint 3 says the magazine listed YYDS "soon after the COVID-19 outbreak began", but 《咬文嚼字》's 2021 list came out about two years after the outbreak, so the fact check marked it wrong. The translation copies this faithfully. Fix the source hint, for example "a language magazine put it on its top-ten buzzwords list for 2021" or "while the pandemic was still going on". The translation should then follow, for example "一本语言文字杂志把它评为2021年度十大流行语之一。" or "疫情持续期间". Fact check: wrong. The answer (about 2021) and the wrong answers are fine. YYDS began with fans of the esports player Uzi in late 2020. 咬文嚼字 named it one of its 2021 top ten buzzwords. Hint 3 is inaccurate. 2021 was about two years after COVID broke out, so it was not "shortly after".
- **q-27326** (eight-cuisines) 看照片：这道火红的菜是长沙人夏天的最爱。菜里的这种动物叫什么？ → 小龙虾: source: the fun fact gives the 1930s, but red swamp crayfish were brought to China from Japan around 1929, near Nanjing (late 1920s), as the fact check says. Correct the date in the source, e.g. "around 1929" or "in the late 1920s", and then translate it again. The rest of the translation is faithful and natural. Fact check: wrong. The answer 小龙虾 and the wrong answers are fine. The fun fact has a date error. Crayfish reached China from Japan around 1928–1929, near Nanjing. That is the 1920s, not the 1930s. They were first brought as feed for bullfrogs. They spread along the coast in the 1930s. The rice-field farming along the Yangtze is true.
- **q-27378** (hundred-schools) 郑国有个人在家量好了脚，到了集市却发现忘带尺码。他接下来去了哪儿？ → 家里: Fact check: uncertain. The story is 《韩非子·外储说左上》郑人买履, and the answer 家里 is correct. The wrong answers (鞋匠铺, 城门口, 裁缝铺) are all wrong. Hint 3 calls the measure a 绳子 (rope). The original only says 度 (a measuring tool or measurement) and never says rope. Also, in the original he had already picked up the shoes when he realized he'd forgotten the 度, and the question says he found out on arrival. This is a minor difference. The fun fact (the market had closed, so he got no shoes) matches the text. 'The last pair' is a slight embellishment.

## Not travelling

None.

## Stale re-translated

None.
