# chinese-base research: school curricula and shared family culture

This is the reading list for the taxonomy of `chinese-base`, the second base bundle, which centres on Chinese culture, history and everyday knowledge. It sums up what mainland children learn at school under the 2022 compulsory-education standards (with the senior-high standards where the 高考 makes them family knowledge) and what Chinese families share beyond school: festivals, food, legends, sport, pop culture. For each topic it gives the career subject, a rough age at which families know it and whether the sensitivity rule allows it. Taiwan's curriculum is only a cross-check for what both sides learn. Input to `plan 231: chinese-base taxonomy from Chinese school curricula`, written by `task 2380: chinese-base research: Chinese school curricula and shared family culture` (2026-11-20).

## How to read the tags

Every topic bullet ends in a tag `[subject · kn N · status · TW]`, which the taxonomy prompt reads.
- **subject:** one of the 7 career subjects (`app/data/subjects.json`, `plans/24-career.md`): history (also myths, languages, religion, philosophy), geography (also customs, food, money), nature, science (also maths, inventions, transport), arts, media, sport (also games, curiosities); same mapping as `base`'s categories.
- **kn N:** `known_at` (1–15, the scale of `authoring/tools/prompts/concepts-list.md`): the lowest level at which mainland families know the topic's easiest concepts, a range for the spread: 1 = a 6-year-old, 5 = an 11-year-old, 10 = a 16-year-old with good school knowledge, 12 = most adults, 15 = specialists.
  - Judged for Chinese families, not outsiders; an English player of `chinese-base` will find most items 2–4 points harder (a voice / drafting matter, part 7).
- **status**, per `decision 757: Sensitivity rule for Chinese content: how do drafting, the fit pass and zh translation treat contested political topics?` (neutral facts only; contested topics allowed when the question states an undisputed fact without judgement or status wording; maps and flags case by case):
  - `in`: no political charge.
  - `facts`: judgement-prone; only bare undisputed facts (a date, a name, a place); no "great", "liberation", "province of", "country" wording; no death tolls or assessments.
  - `out`: no family-party question about it avoids judgement or status; leave the area out of the taxonomy.
- **TW:** also taught in Taiwan's 108課綱 or shared by Taiwanese families: safe ground for `zh-Hant` (`plans/26-china.md` "Taiwan vs. mainland framing"); no TW = mainland-specific (fine in `zh-Hant` only if the wording names the mainland as such).

## Sources
- Mainland compulsory education: 《义务教育课程方案和课程标准（2022年版）》, 教材〔2022〕2号, 16 subject standards, in force from autumn 2022 ([MOE](http://www.moe.gov.cn/srcsite/A26/s8001/202204/t20220420_619921.html), [中国新闻网 on the release](https://www.chinanews.com.cn/gn/2022/04-21/9735008.shtml), [中国新闻网 on the changes](https://www.chinanews.com.cn/gn/2022/04-21/9734982.shtml)); 劳动 a subject of its own from 2022, ≥ 1 period a week.
- Senior high: 《普通高中课程方案和语文等学科课程标准（2017年版2020年修订）》, 教材〔2020〕3号, 20 subject standards ([新华网](https://www.xinhuanet.com/politics/2020-06-04/c_1126071120.htm)); 语文 recitation list raised from 14 to 72 texts ([新高考过渡时期语文学科背诵篇目说明, Wikisource](https://zh.wikisource.org/wiki/%E6%96%B0%E9%AB%98%E8%80%83%E8%BF%87%E6%B8%A1%E6%97%B6%E6%9C%9F%E8%AF%AD%E6%96%87%E5%AD%A6%E7%A7%91%E8%83%8C%E8%AF%B5%E7%AF%87%E7%9B%AE%E8%AF%B4%E6%98%8E)).
- Textbooks: 统编版 (部编版, People's Education Press) 语文, 历史, 道德与法治, nationwide since 2019; e.g. 一年级上册: 天地人, 金木水火土, 对韵歌, 小兔子乖乖, 乌鸦喝水 ([课文朗读 index, bilibili](https://www.bilibili.com/video/av64662819)).
- Taiwan: 十二年國民基本教育課程綱要 總綱 (108課綱, issued 2014, in force from school year 2019) ([國家教育研究院 總綱](https://www.naer.edu.tw/upload/1/16/doc/1325/十二年國教課程綱要總綱.pdf)), 國語文 領域綱要 with 15 recommended classical texts for senior high ([國語文 綱要](https://www.naer.edu.tw/upload/1/16/doc/806/十二年國民基本教育課程綱要國民中小學暨普通型高級中等學校語文領域-國語文.odt), [NOWnews on the 15](https://www.nownews.com/news/6320416)).
- Culture: UNESCO intangible heritage, China 44 elements by Dec 2024, incl. [Twenty-Four Solar Terms (2016)](https://ich.unesco.org/en/RL/00647) and Spring Festival (2024) ([Henan gov](https://english.henan.gov.cn/2024/12-05/3095710.html)); 5A scenic areas: 358 (Dec 2024), 17 more proposed Nov 2026 ([新华网 2026-11-05](https://www.news.cn/politics/20261105/4fc71d4671cb4d4ea873c4ce3410df34/c.html), [China Daily 2025](https://cn.chinadaily.com.cn/a/202505/20/WS682bbceaa310205377033e52.html)).
- Topic overviews (Wikipedia): [Four Great Inventions](https://en.wikipedia.org/wiki/Four_Great_Inventions), [Four Great Classical Novels](https://en.wikipedia.org/wiki/Four_Great_Classical_Novels), [Four Great Folktales](https://en.wikipedia.org/wiki/Four_Great_Folktales), [Chinese zodiac](https://en.wikipedia.org/wiki/Chinese_zodiac), [Solar term](https://en.wikipedia.org/wiki/Solar_term), [Chinese cuisine: eight traditions](https://en.wikipedia.org/wiki/Chinese_cuisine#Eight_Great_Traditions), [Varieties of Chinese](https://en.wikipedia.org/wiki/Varieties_of_Chinese), [Chengyu](https://en.wikipedia.org/wiki/Chengyu), [Xiehouyu](https://en.wikipedia.org/wiki/Xiehouyu), [Three Hundred Tang Poems](https://en.wikipedia.org/wiki/Three_Hundred_Tang_Poems), [Table of General Standard Chinese Characters](https://en.wikipedia.org/wiki/Table_of_General_Standard_Chinese_Characters), [Gaokao](https://en.wikipedia.org/wiki/Gaokao), [CMG New Year's Gala](https://en.wikipedia.org/wiki/CMG_New_Year%27s_Gala), [Journey to the West (1986 TV series)](https://en.wikipedia.org/wiki/Journey_to_the_West_(1986_TV_series)), [Black Myth: Wukong](https://en.wikipedia.org/wiki/Black_Myth:_Wukong), [Chinese Lunar Exploration Program](https://en.wikipedia.org/wiki/Chinese_Lunar_Exploration_Program), [Tu Youyou](https://en.wikipedia.org/wiki/Tu_Youyou), [World Heritage Sites in China](https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_China), [AAAAA Tourist Attractions](https://en.wikipedia.org/wiki/AAAAA_Tourist_Attractions_of_China), [Calabash Brothers](https://en.wikipedia.org/wiki/Calabash_Brothers), [Pleasant Goat and Big Big Wolf](https://en.wikipedia.org/wiki/Pleasant_Goat_and_Big_Big_Wolf), [Ne Zha 2](https://en.wikipedia.org/wiki/Ne_Zha_2).
- Not confirmed online: the plan's recitation counts for compulsory education (小学 75, 初中 61) are the 2011 standard's figures, as far as secondary sources show kept in the 2022 appendix; character targets (≈ 1600 known after grade 2, ≈ 3000 known / 2500 written after grade 6) from the standard as commonly cited; both only matter as scale, not as question facts.

## School: 语文 (Chinese)

The largest subject (≈ 20–22 % of compulsory periods) and the richest source: every family recites the same poems, fables and texts. It is also where questions risk giving the answer away in Chinese (section "Language topics").
- **Ancient poems (古诗):** the first-grade canon every adult can recite: 骆宾王《咏鹅》, 李白《静夜思》, 孟浩然《春晓》, 李绅《悯农》, 王之涣《登鹳雀楼》, 贺知章《咏柳》; later 杜甫《春夜喜雨》, 王维《九月九日忆山东兄弟》 (重阳), 杜牧《清明》, 苏轼《题西林壁》, 王安石《元日》 (春节). Ask author, season, festival, place (黄鹤楼 → Wuhan, 庐山), the poet's nickname (诗仙 李白, 诗圣 杜甫, 诗佛 王维). [arts · kn 1–12 · in · TW]
- **Classical prose (文言文), junior and senior high:** 《论语》 sayings, 《桃花源记》 (陶渊明), 《出师表》 (诸葛亮), 《岳阳楼记》 (范仲淹, «先天下之忧而忧»), 《醉翁亭记》 (欧阳修), 《爱莲说》 (周敦颐), 《陋室铭》 (刘禹锡), 《师说》 (韩愈), 《赤壁赋》 (苏轼), 《劝学》 (荀子), 《离骚》 (屈原), 《逍遥游》 (庄子), 《滕王阁序》 (王勃), 《阿房宫赋》 (杜牧). Senior-high list: 72 texts for recitation. Taiwan's 15 recommended texts overlap: 桃花源記, 出師表, 師說, 赤壁賦, 鴻門宴 (司馬遷), 項脊軒志. [arts · kn 8–13 · in · TW for the overlap]
- **Song lyrics (宋词) and their poets:** 苏轼《水调歌头·明月几时有》 (中秋), 李清照 (only famous woman poet of the canon), 辛弃疾, 岳飞《满江红》 (facts: a national-hero text, neutral as literature). [arts · kn 9–13 · in · TW]
- **Four Classic Novels (四大名著):** 西游记, 三国演义, 水浒传, 红楼梦; characters (孙悟空, 猪八戒, 诸葛亮, 关羽, 武松打虎, 林黛玉), episodes (三打白骨精, 草船借箭, 桃园结义), number of 梁山 heroes (108), authors (吴承恩, 罗贯中, 施耐庵, 曹雪芹). 整本书阅读 is in the 2022 standard; families know them mostly from TV (section "Media"). [arts · kn 2–12 · in · TW]
- **Modern literature in textbooks:** 鲁迅 (《从百草园到三味书屋》, 《孔乙己》, 《故乡》 with 闰土, 《阿Q正传》; pen name, real name 周树人), 朱自清《背影》《春》, 老舍《骆驼祥子》《茶馆》, 冰心, 巴金《家》, 沈从文《边城》. [arts · kn 9–12 · in · TW for 朱自清, 鲁迅 partly]
- **Modern and popular authors outside textbooks:** 莫言 (Nobel 2012), 刘慈欣《三体》 (Hugo 2015), 金庸 (武侠: 射雕, 天龙八部, 笑傲江湖), 琼瑶 (TW), 三毛 (TW), 余华《活着》. [arts · kn 10–13 · in · TW]
- **Fables and textbook stories (寓言, 课文):** 乌鸦喝水, 小马过河, 守株待兔, 揠苗助长, 刻舟求剑, 画蛇添足, 狐假虎威, 井底之蛙, 亡羊补牢, 自相矛盾, 曹冲称象, 司马光砸缸, 孔融让梨, 铁杵磨成针 (李白), 凿壁偷光, 悬梁刺股, 神笔马良, 小蝌蚪找妈妈. Many are 成语 too. [arts or history · kn 1–6 · in · TW]
- **Idioms (成语) and sayings:** origin story and the person behind it (卧薪尝胆 → 勾践, 破釜沉舟 → 项羽, 纸上谈兵 → 赵括, 三顾茅庐 → 刘备 / 诸葛亮, 完璧归赵 → 蔺相如, 闻鸡起舞 → 祖逖, 负荆请罪 → 廉颇). [history · kn 5–13 · in · TW]
- **Characters (汉字):** pictographs (日, 月, 山, 水, 人, 木), radicals (氵 water, 扌 hand, 木 tree), oracle bones (甲骨文, 殷墟, 安阳), script history (篆 → 隶 → 楷), 仓颉 legend, 通用规范汉字表 8105 characters (2013), simplification 1956/1964 (facts), pinyin 1958 (mainland) vs. 注音 (Taiwan). [history · kn 3–13 · in · TW except pinyin / simplification as mainland facts]
- **Couplets (对联) and riddles (灯谜):** 春联 at the door, 元宵 lantern riddles; ask about the custom, not the riddle's solution (Chinese wordplay). [geography · kn 3–9 · in · TW]

## School: 数学 (maths)
- **Counting tools and tables:** 算盘 (abacus; beads 上二下五 or 上一下四; UNESCO 2013 珠算), 九九乘法表 (oldest found on 里耶秦简), counting rods. [science · kn 3–11 · in · TW]
- **Classic problems:** 鸡兔同笼 (《孙子算经》, primary grade 4–6 staple), 韩信点兵 (Chinese remainder theorem), 百鸡问题; the problem can be asked as a sum. [science · kn 6–12 · in · TW]
- **Ancient mathematics:** 《九章算术》, 勾股定理 (商高, 赵爽弦图: logo of the 2002 ICM Beijing), 祖冲之 π between 3.1415926 and 3.1415927 (密率 355/113), 刘徽 割圆术, 杨辉三角 (= Pascal's triangle, older; 贾宪). [science · kn 8–13 · in · TW]
- **Modern mathematicians:** 华罗庚 (self-taught, 优选法), 陈景润 (Goldbach "1+2"; 徐迟's report 1978), 丘成桐 (Fields 1982), 陈省身. [science · kn 11–14 · in · TW for 陈省身, 丘成桐]
- **School maths culture:** 奥数, 口算, the 高考 maths paper as the feared one. [science · kn 6–12 · in]

## School: 历史 (history)

Grades 7–9 cover Chinese history from prehistory to today, then world history; high school repeats it in depth (《中外历史纲要》). Taiwan's 108課綱 dropped Chinese history as its own block: senior-high history is Taiwan, then East Asia (with China inside), then the world; dynastic culture is still learned through 國語文 and family culture.
- **Prehistory and legends turned history:** 北京人 (周口店), 元谋人, 河姆渡 (rice), 半坡 (pottery), 炎帝 and 黄帝 (炎黄子孙), 尧舜禹, 大禹治水. [history · kn 4–11 · in · TW]
- **Dynasties:** order (朝代歌), founders, capitals; 夏商周, 春秋战国 (诸子百家), 秦 (秦始皇, 221 BC unification of script, coins, measures; 长城, 兵马俑 found 1974), 汉 (刘邦, 汉武帝, 张骞 and the 丝绸之路, 蔡伦's paper), 三国, 隋 (大运河, 科举 from 605), 唐 (长安, 李世民, 武则天 only empress, 玄奘, 鉴真 to Japan, 文成公主 → facts: a Tibet link), 宋 (活字印刷 毕昇, 清明上河图, 岳飞), 元 (忽必烈, 马可·波罗), 明 (朱元璋, 郑和 1405–1433, 紫禁城 1420, 戚继光), 清 (康熙, 乾隆, 圆明园). [history · kn 3–13 · in · TW]
- **Four Great Inventions (四大发明)** and other firsts: paper, printing, gunpowder, compass (司南); silk, porcelain, tea, 地动仪 (张衡, 132 AD). [science · kn 3–10 · in · TW]
- **Late Qing and Republic (1840–1949):** 鸦片战争 1840, 林则徐 虎门销烟, 南京条约 and Hong Kong 1842, 圆明园 burnt 1860, 戊戌变法, 辛亥革命 1911 and 孙中山 (honoured on both sides), 五四运动 1919, 抗日战争 1937–1945. [history · kn 8–12 · facts · TW for 孙中山, 辛亥]
  - Party history (1921 founding, 长征 1934–35, 遵义会议), civil war 1945–49, 南京大屠杀 (date and place yes; victim numbers out): facts; Taiwan reads these years differently, so wording names neither side as the rightful one.
- **After 1949:** 1949-10-01 founding of the PRC (facts, "the People's Republic of China was founded in"), 两弹一星, 1971 UN seat (out: status wording), 改革开放 1978 (facts), 深圳 special economic zone 1980, 香港回归 1997-07-01 and 澳门 1999-12-20 (facts: dates only), 2008 Beijing Olympics, 2003 first taikonaut. [history · kn 6–12 · facts]
  - Out: 大跃进, 文化大革命 beyond bare dates, 1989, Tibet and Xinjiang politics, Taiwan's status, present leaders and party bodies (decision 757 allows a bare date, but no family-party question about them avoids judgement; recommend leaving the areas out).
- **World history as taught in China:** ancient civilisations (Egypt, Babylon, India, Greece), Renaissance, industrial revolution, the world wars; overlaps `base` heavily: copies' ground, not new subcategories. [history · kn 8–12 · in]

## School: 地理 (geography)
- **Administrative China:** provincial-level divisions, their capitals, one-character abbreviations (简称: 京, 沪, 粤, 川, 湘, 鲁, 豫…), nicknames (天府之国 四川, 鱼米之乡 江南), the map as a rooster (雄鸡; map questions case by case). [geography · kn 6–12 · in for mainland provinces; counts "34" and Taiwan's listing out (status)]
- **Rivers and lakes:** 长江 (≈ 6300 km, longest in Asia), 黄河 (母亲河, 壶口瀑布), 珠江, 京杭大运河 (UNESCO 2014), 青海湖, 鄱阳湖, 洞庭湖, 西湖, 太湖. [geography · kn 3–11 · in · TW]
- **Mountains and landforms:** 珠穆朗玛峰 8848.86 m (2020 survey; "on the border with Nepal" fine), 五岳 (泰山 东岳…), 黄山, 峨眉山, 庐山, 张家界, 青藏高原 (roof of the world), 四大高原, 四大盆地 (四川盆地, 塔里木), 塔克拉玛干沙漠, 喀斯特 (桂林山水甲天下). [geography · kn 3–12 · in · TW]
- **Climate and the north–south line:** 秦岭–淮河 (north/south, 0 °C January line, 800 mm rain), monsoon, 胡焕庸线 (population), 东北 cold (哈尔滨 ice festival), 吐鲁番 heat (火焰山), 海南 tropical. [geography · kn 6–12 · in]
- **Regions and cities:** 北上广深, 重庆 (largest municipality by area), 西安 (former capital), 杭州, 苏州 (gardens), 成都, 哈尔滨, 三亚, 拉萨 (facts: places only), 乌鲁木齐 (farthest city from any sea), 香港 and 澳门 as cities. [geography · kn 3–11 · in; Lhasa, Urumqi facts]
- **Borders and seas:** 14 land neighbours (facts), 渤海 黄海 东海 南海 as seas; disputed lines (藏南, 阿克赛钦, South China Sea claims, 钓鱼岛 / Senkaku) out; any map with borders checked case by case. [geography · kn 6–12 · facts]
- **Ethnic groups:** 56 officially recognised groups (facts), festivals of groups (傣族 泼水节, 蒙古族 那达慕, 彝族 火把节, 壮族 三月三), houses (蒙古包, 土楼 of the Hakka, 窑洞), dress. Tibetan and Uyghur culture: facts (food, places), no politics. [geography · kn 5–12 · facts for minority framing]
- **World geography:** continents, countries, capitals: `base` ground (copies). [geography · kn 3–12 · in]

## School: 道德与法治 (morality and law)

Mostly out: much of it is political education (constitution, party, "core socialist values"), where no neutral family question exists.
- **In (daily life):** emergency numbers 110 police, 119 fire, 120 ambulance, 122 traffic; traffic rules (red light, zebra crossing), school safety, 垃圾分类 (four bins since 2019 in Shanghai). [geography · kn 1–6 · in]
- **Facts only:** 国旗 (五星红旗), 国徽, 国歌 《义勇军进行曲》 (聂耳, 田汉): facts naming the PRC; 宪法 1982. [history · kn 2–10 · facts, not TW]
- **Out:** ideology, party bodies, present policy, "our country" framing.

## School: 科学, 物理, 化学, 生物学 (science)

Primary 科学 from grade 1 (2017 onward), then physics (grade 8), chemistry (grade 9), biology (grades 7–8). The world-science content (Newton, cells, periodic table) is `base` ground; China-centric are the people, inventions and projects.
- **Ancient science:** 墨子 (pinhole camera 小孔成像, ≈ 400 BC; also the 2016 quantum satellite's name), 沈括《梦溪笔谈》 (magnetic declination), 张衡, 郭守敬 (授时历), 都江堰 (李冰, still working), 赵州桥 (李春, oldest open-spandrel stone arch), 鲁班 (saw legend), 黄道婆 (cotton). [science · kn 5–13 · in · TW]
- **Medicine (history only):** 华佗 (麻沸散), 张仲景, 李时珍《本草纲目》, 孙思邈; acupuncture (UNESCO 2010); questions about people and history, never on efficacy claims of TCM. [science · kn 8–12 · in · TW]
- **Modern scientists:** 钱学森 (rocketry), 邓稼先, 袁隆平 (hybrid rice), 屠呦呦 (artemisinin, Nobel 2015, first PRC woman scientist laureate), 杨振宁 and 李政道 (Nobel 1957), 钱三强, 侯德榜 (soda process), 茅以升 (钱塘江大桥), 詹天佑 (京张铁路 1909, zigzag 人字形), 钟南山 (facts: SARS 2003; COVID topics out). [science · kn 8–13 · in · TW for pre-1949 and Nobel laureates]
- **Space (2003–2026):** 神舟五号 杨利伟 2003, 天宫 station (complete 2022), 嫦娥 probes (嫦娥四号 first far-side landing 2019, 嫦娥五号 samples 2020, 嫦娥六号 far-side samples 2024), 玉兔 rovers, 天问一号 / 祝融 Mars 2021, 北斗 navigation, 长征 rockets, 王亚平 first Chinese woman spacewalker 2021, 天宫课堂 (lessons from space, every pupil saw them). [science · kn 4–12 · in]
- **Big engineering and records:** 三峡大坝 (facts; resettlement debate out), 港珠澳大桥 (2018), 青藏铁路 (2006, highest railway), FAST 天眼 500 m telescope (2016), 高铁 (复兴号, largest network), 天河 / 神威 supercomputers, C919 airliner (2023), 墨子号 quantum satellite. [science · kn 5–12 · in]
- **Chemistry and physics in families' memory:** gunpowder recipe (一硫二硝三木炭), 人工合成牛胰岛素 (1965, first synthetic protein), 克隆猴 中中、华华 (2018). [science · kn 9–13 · in]

## Nature (from 科学, 生物学, 地理 and family life)
- **Iconic animals:** 大熊猫 (国宝, 卧龙, eats bamboo, diplomacy facts), 金丝猴, 东北虎, 华南虎, 扬子鳄, 朱鹮 (from 7 birds in 1981), 丹顶鹤, 藏羚羊 (2008 mascot 迎迎), 中华鲟, 白鳍豚 (functionally extinct 2006), 亚洲象 (2021 northward wandering herd in Yunnan). [nature · kn 1–12 · in · TW]
- **Plants:** 银杏 (living fossil), 水杉, 竹, 牡丹 (洛阳), 梅 兰 竹 菊 (四君子, also arts), 荷花, 桂花, 茶树, 珙桐 (dove tree). [nature · kn 3–12 · in · TW]
- **Farm and home:** rice, wheat (north noodles, south rice), 桑蚕 silkworms (kids raise them in school), 鸬鹚 fishing, goldfish (bred in China), 鲤鱼跃龙门. [nature · kn 2–10 · in · TW]
- **Body and health:** 眼保健操 (every school day), 广播体操, 近视 rates; Chinese-specific twists on `base`'s human body. [nature · kn 2–8 · in]
- **Natural hazards and reserves:** 黄河 floods, 汶川地震 2008 (facts: date, magnitude 8.0), 九寨沟, 三江源, 卧龙 reserve, 西双版纳. [nature · kn 6–12 · facts for disasters, else in]

## School: 音乐, 美术, 体育与健康, 信息科技, 劳动
- **Music (音乐):** pentatonic scale 宫商角徵羽, instruments (二胡, 古筝, 琵琶, 笛子, 唢呐, 编钟 of 曾侯乙 433 BC), 民歌 (《茉莉花》, 《康定情歌》, 《小河淌水》), 《二泉映月》 (阿炳, blind), 《梁祝》 violin concerto (1959), 《黄河大合唱》 (冼星海, facts), 十面埋伏, 高山流水 (伯牙 子期 → 知音). [arts · kn 4–12 · in · TW]
- **Opera (戏曲):** 京剧 (国粹; face colours: red 关羽 loyal, white 曹操 cunning, black 包公 honest; 梅兰芳, 生旦净丑), 昆曲 (UNESCO 2001), 越剧, 黄梅戏, 豫剧, 川剧 变脸, 粤剧. [arts · kn 5–12 · in · TW]
- **Art (美术):** 书法 (王羲之 书圣, 《兰亭序》; 颜真卿; 文房四宝), 国画 (齐白石's shrimp, 徐悲鸿's horses, 张择端《清明上河图》, 王希孟《千里江山图》), 敦煌 murals (飞天), bronzes (后母戊鼎, 四羊方尊), 青花瓷 and 景德镇, 剪纸, 年画 (杨柳青), 皮影, 刺绣 (四大名绣: 苏 湘 蜀 粤). [arts · kn 4–13 · in · TW]
- **PE and health (体育与健康):** 广播体操, 跳绳, 踢毽子, 中考体育, 武术 and 太极 (UNESCO 2020), 乒乓球 and 羽毛球 in school. [sport · kn 2–9 · in]
- **IT (信息科技):** binary, coding basics, first full internet link 1994, 搜索 / 百度; mostly `base` ground, China-centric bits in "brands". [science · kn 8–12 · in]
- **Labour (劳动):** cooking (包饺子), farming calendar (节气), tools (犁, 水车), housework; feeds food and customs, no own subcategory. [geography · kn 3–9 · in]

## High school and the 高考
- **The exam itself:** 7–8 (9–10) June, 全国卷 vs. provincial papers, 状元, the essay topic (作文题) as yearly news, resumed 1977. Origin: 科举 from 605 (隋) to 1905, 状元 / 榜眼 / 探花, 八股文. [history · kn 8–12 · in; 科举 TW]
- **What high school adds that families know:** the 72 recitation texts (语文 above), 《中外历史纲要》 (history in depth: facts rule applies), 必修 physics/chemistry (`base` ground), 思想政治 (out, like 道德与法治).

## Festivals, calendar and customs
- **Festivals (传统节日):** 春节 (年兽, 春联, 福 upside down, 压岁钱 / 红包, 饺子 north, 年糕, 守岁, 鞭炮, 春运), 元宵 (汤圆 / 元宵, lantern riddles), 清明 (扫墓, 青团), 端午 (屈原, 粽子, 龙舟; UNESCO 2009), 七夕 (牛郎织女, 鹊桥), 中元, 中秋 (嫦娥, 月饼, 玉兔), 重阳 (登高, 菊花), 腊八 (粥), 小年 (灶王爷). [geography · kn 1–10 · in · TW]
- **Modern days:** 国庆 1 Oct (facts; Taiwan's 國慶日 is 10 Oct: not TW), 劳动节 golden week, 双十一 (shopping, since 2009), 520 (love, homophone of 我爱你), 教师节 10 Sep. [geography · kn 4–11 · in; 国庆 facts]
- **Calendar (二十四节气, 农历):** 24 terms (UNESCO 2016; 立春, 清明, 夏至, 冬至 with 饺子 / 汤圆, 惊蛰), lunar months, 闰月, 天干地支 and the 60-year cycle (甲子; 2026 = 丙午 year of the horse). [geography · kn 4–12 · in · TW]
- **Zodiac (生肖):** 12 animals in order, the race legend (cat left out, rat on the ox), 本命年 and red underwear, 2026 horse, 2027 goat. [geography · kn 1–8 · in · TW]
- **Numbers, colours, etiquette:** 8 lucky (2008-08-08 08:08 Olympic opening), 4 avoided (homophone of 死), red for luck and weddings, white for mourning, no clock as a gift (送钟 = 送终), chopsticks not upright in rice, toasting, 敬茶 at weddings. [geography · kn 3–10 · in · TW]

## Food and drink
- **Eight cuisines (八大菜系):** 鲁, 川, 粤, 苏, 闽, 浙, 湘, 徽; signature dishes per cuisine (麻婆豆腐, 宫保鸡丁, 回锅肉 川; 白切鸡, 早茶 dim sum 粤; 松鼠鳜鱼 苏; 佛跳墙 闽; 东坡肉, 西湖醋鱼 浙; 剁椒鱼头 湘; 臭鳜鱼 徽). [geography · kn 4–12 · in · TW]
- **Famous dishes and snacks by city:** 北京烤鸭, 兰州牛肉面, 西安肉夹馍 and 羊肉泡馍, 天津煎饼果子 and 狗不理包子, 武汉热干面, 上海小笼包, 柳州螺蛳粉, 重庆 / 成都火锅, 长沙臭豆腐, 新疆大盘鸡 and 烤羊肉串, 沙县小吃, 广州肠粉, 台湾 珍珠奶茶 (bubble tea, TW origin, shared). [geography · kn 2–11 · in · TW]
- **Tea:** six types (绿, 白, 黄, 青/乌龙, 红, 黑), 西湖龙井, 碧螺春, 铁观音, 大红袍, 普洱, 陆羽《茶经》 (茶圣), 功夫茶, 茶马古道; UNESCO 2022. [geography · kn 6–12 · in · TW]
- **Staples and debates:** 南甜北咸 豆腐脑, 粽子 sweet vs. savoury, 饺子 vs. 汤圆, 豆浆油条, chopsticks, 白酒 (茅台, 五粮液), 黄酒 (绍兴), 月饼 fillings. [geography · kn 2–9 · in · TW]

## Myths, legends and religion
- **Creation and heroes (神话):** 盘古开天, 女娲补天 / 造人, 后羿射日, 嫦娥奔月, 精卫填海, 夸父逐日, 大禹治水, 愚公移山, 仓颉造字, 神农尝百草. [history · kn 1–8 · in · TW]
- **Four folktales (四大民间传说):** 牛郎织女, 孟姜女哭长城, 梁山伯与祝英台 (butterflies), 白蛇传 (雷峰塔, 西湖); plus 八仙过海, 哪吒闹海, 宝莲灯 (沉香), 聊斋 ghosts (蒲松龄). [history · kn 3–10 · in · TW]
- **Creatures and gods:** 龙 (dragon king, nine sons), 凤凰, 麒麟, 貔貅, 年兽, 门神 (秦琼, 尉迟恭), 财神, 土地公, 灶王爷, 月老, 山海经 beasts, 玉皇大帝, 王母娘娘. [history · kn 2–11 · in · TW]
- **Philosophy and religion:** 孔子 (论语, 72 disciples, 曲阜, 教师节 link), 孟子 (孟母三迁), 老子 (道德经), 庄子 (庄周梦蝶), 孙子兵法, 墨子, 韩非子, 百家争鸣, Buddhism (白马寺, 少林寺, 玄奘, 观音), Daoism (武当山, 八卦, 太极图). Living religion today and present-day religious politics: facts or out. [history · kn 5–12 · in · TW]

## Places and sights
- **World heritage:** ≈ 60 UNESCO sites by 2025 (长城, 故宫, 兵马俑, 莫高窟, 布达拉宫 (facts: a place, not a status), 颐和园, 天坛, 苏州园林, 丽江, 平遥, 黄山, 九寨沟, 武陵源, 杭州西湖, 鼓浪屿, 泉州 2021, 普洱景迈山 2023, 北京中轴线 2024). [geography · kn 2–12 · in · TW]
- **5A scenic areas and family trips:** 358 (2024; 375 if Nov 2026's proposals pass); famous for school trips and holidays: 故宫, 八达岭, 外滩 and 东方明珠, 黄山, 张家界 (Avatar mountains), 桂林漓江 (20-yuan note scene), 乐山大佛, 少林寺, 西湖, 三亚. [geography · kn 3–11 · in]
- **On banknotes and in sayings:** 人民币 backs (100: 人民大会堂, 50: 布达拉宫, 20: 桂林山水, 10: 长江三峡, 5: 泰山, 1: 西湖) (facts), 不到长城非好汉, 上有天堂下有苏杭. [geography · kn 6–12 · facts for notes, else in]

## Sport and games
- **Olympics:** 许海峰 first gold 1984, 2008 Beijing (鸟巢, 水立方, 福娃 five mascots, 51 golds), 2022 Winter (冰墩墩, 谷爱凌 facts: her nationality choice is a debate, results only), 刘翔 110 m hurdles 2004, 苏炳添 9.83 (2021), 全红婵 diving 2021 (age 14). [sport · kn 4–12 · in]
- **Table tennis and badminton:** 国球, 容国团 (first world title 1959), 邓亚萍, 王楠, 张怡宁, 马龙 (grand slam), 樊振东, 孙颖莎; 林丹 vs. 李宗伟. [sport · kn 5–12 · in]
- **Volleyball, basketball, football, tennis:** 女排 (郎平, five titles in a row 1981–86, 女排精神), 姚明 (NBA #1 pick 2002), CBA, men's football (2002 World Cup only), 李娜 (French Open 2011), 丁俊晖 (snooker). [sport · kn 6–12 · in]
- **Martial arts and traditional sports:** 武术, 太极拳 (UNESCO 2020), 少林功夫, 李小龙, 成龙, 龙舟, 舞龙舞狮, 毽子, 空竹, 蹴鞠 (football origin, FIFA acknowledges). [sport · kn 3–11 · in · TW]
- **Board and party games:** 围棋 (19×19, AlphaGo vs. 柯洁 2017), 中国象棋 (楚河汉界), 麻将 (136/144 tiles), 斗地主, 跳棋, 七巧板 (tangram), 华容道, 九连环, 鲁班锁. [sport · kn 3–12 · in · TW]
- **Children's games:** 老鹰捉小鸡, 跳皮筋, 丢手绢, 石头剪刀布, 弹珠. [sport · kn 1–6 · in · TW]

## Media and pop culture
- **CMG New Year's Gala (春晚):** since 1983, sketches (小品: 赵本山, 宋丹丹), cross-talk (相声), the closing song 《难忘今宵》, 2025 robot dancers. [media · kn 4–12 · in]
- **Classic TV series:** 西游记 (1986, 六小龄童 as Monkey King, theme 《云宫迅音》), 红楼梦 (1987), 三国演义 (1994), 水浒传 (1998), 还珠格格 (1998, TW writer 琼瑶), 家有儿女 (sitcom), 甄嬛传 (2011), 武林外传 (2006), 庆余年, 繁花 (2023, Shanghai). [media · kn 5–12 · in · TW for 还珠格格, 西游记]
- **Film:** 张艺谋 (红高粱, 英雄, 2008 opening ceremony), 陈凯歌 (霸王别姬, Palme d'Or 1993 shared), 李安 (TW; 卧虎藏龙, Oscars), 周星驰 (大话西游, 功夫, 少林足球), 成龙, 李连杰, 甄子丹 (叶问), 流浪地球 (2019), 你好，李焕英 (2021), 哪吒之魔童降世 (2019), 哪吒之魔童闹海 (2025, highest-grossing animated film). War films (长津湖): facts. [media · kn 5–12 · in]
- **C-pop and songs everyone sings:** 邓丽君 (TW, 《月亮代表我的心》), 王菲, 四大天王 (张学友, 刘德华, 郭富城, 黎明), Beyond (《海阔天空》), 周杰伦 (TW, 《青花瓷》, 《稻香》), 五月天 (TW), 李宇春 (超级女声 2005), TFBOYS, 凤凰传奇 (广场舞), 《小苹果》, 《最炫民族风》. [arts · kn 6–12 · in · TW]
- **Games:** 仙剑奇侠传 (1995, TW-made, shared), 王者荣耀 (2015, Tencent), 和平精英, 原神 (2020, miHoYo, Shanghai), 阴阳师, 黑神话：悟空 (2024, Game Science, 西游记-based), 开心消消乐, 植物大战僵尸 (foreign, hugely popular). [media · kn 5–12 · in]
- **Internet life:** 微信 (2011, red packets 2014), 支付宝 (2004), QQ (1999, the penguin), 抖音 (2016; TikTok abroad), B站 bullet comments, 淘宝, 外卖 (美团), 共享单车, 二维码 everywhere; memes are out (fast-dated). [media · kn 6–12 · in]
- **Brands and products:** 华为, 小米, 联想, 比亚迪 (largest EV maker), 大疆 (drones), 海尔, 李宁, 大白兔 (candy), 老干妈, 茅台, 王老吉, 青岛啤酒 (German-founded 1903), 格力, 蜜雪冰城 (snowman). [media · kn 5–12 · in]

## Children's culture (kids level)

The kids-level spine: what a 6–10-year-old knows from home, kindergarten and the first textbooks. Lowest `known_at` in the bundle; every category should reach some of it.
- **Nursery rhymes and songs (儿歌):** 《小兔子乖乖》, 《两只老虎》, 《找朋友》, 《拔萝卜》, 《数鸭子》, 《世上只有妈妈好》, 《小燕子》, 《让我们荡起双桨》, 《一分钱》, 《卖报歌》. [arts · kn 1–5 · in · TW for most]
- **Cartoons (动画片):** 《大闹天宫》 (1961/64), 《小蝌蚪找妈妈》 (1960 ink-wash animation), 《葫芦兄弟》 (1986, seven brothers, colours and powers), 《黑猫警长》, 《哪吒闹海》 (1979), 《大头儿子和小头爸爸》, 《蓝猫淘气三千问》, 《喜羊羊与灰太狼》 (2005), 《熊出没》 (2012), 《猪猪侠》, 《汪汪队立大功》 and 《小猪佩奇》 (foreign, ubiquitous; Peppa: `base` ground). [media · kn 1–8 · in]
- **Fairy tales and fables (童话, 寓言):** 神笔马良, 小马过河, 小蝌蚪找妈妈, 孔融让梨, 司马光砸缸, 曹冲称象, 狼来了 (Aesop, told as Chinese), 郑渊洁 (皮皮鲁, 童话大王); foreign tales (安徒生, 格林) are `base` ground. [arts · kn 1–6 · in · TW]
- **Textbook figures (课本 figures):** 司马光, 孔融, 曹冲, 李白, 王二小 (wartime boy, facts), 雷锋 (学雷锋日 5 Mar, facts), 小英雄雨来 (facts), 詹天佑, 邓稼先; the textbook mascots (小明 as the eternal maths-problem boy). [history · kn 2–8 · in; war heroes facts]
- **School life:** red scarf (红领巾, facts), 眼保健操, 广播体操, 早读, 课间, 值日, 三好学生, 寒暑假作业, 小学 six years, 中考. [geography · kn 2–7 · in; 红领巾 facts]
- **Toys and snacks:** 大白兔, 跳跳糖, 辣条, 小浣熊 cards, 溜溜球, 四驱车, 魔方; 1980s–90s ones are parents' nostalgia (kn for adults). [sport or media · kn 2–9 · in]

## Spoken varieties and languages (as content)
- **Varieties (方言):** 普通话 (Beijing phonology, northern grammar, 1955 standard), 粤语 (广州, 香港; 9 tones in classic counts), 吴语 (上海, 苏州, 越剧), 闽语 (福建, 台湾 台語, 潮汕), 客家话, 湘语, 赣语, 晋语; questions ask where it's spoken, its city, a well-known word's region, not how to say it. [history · kn 6–12 · in · TW]
- **Writing systems:** 简体 vs. 繁体 (where each is used: facts, neutral), 注音 vs. 拼音, 女书 (women's script, Hunan), minority scripts (蒙古文, 藏文 facts). [history · kn 8–13 · in]
- **Chinese loanwords in English and vice versa:** ketchup (闽南 kê-tsiap), typhoon, kowtow, tea (te vs. cha routes), 沙发 sofa, 咖啡 coffee, 巧克力. [history · kn 8–12 · in]

## Language topics: what an English question can ask

Plan 231 "Language subcategories": 成语, 汉字, 唐诗 / 宋词, 歇后语 are drafted in English (`decision 750: New China-centric questions: drafted in English (milestone 12 as edited) instead of Chinese (decision 218)?`) and translated; the Chinese text may give the answer away, or lose the point. These are the Chinese-language questions of `decision 754: Native checks of Chinese translation runs: pilot and release sample, not every run` (full native sheet).
- **成语:** ask the person, dynasty or story behind an idiom ("Which king slept on brushwood and tasted gall to plan his revenge?" → 勾践), the source book, the animal in it; never the idiom's meaning or the idiom from its story when the story is its literal words (守株待兔 from "a farmer waited by a stump": in Chinese the question spells the answer). Works in English: yes, with characters + pinyin + gloss in the options.
- **汉字:** ask what a pictograph was drawn from (日 = the sun), the radical's meaning, stroke counts, which object oracle bones were (turtle shells, ox bones), the script's evolution order; never "which character means X" when the Chinese question shows it. Works in English: mostly; stroke questions are fine in both.
- **唐诗 / 宋词:** ask the author of a named poem, its festival or season, the place, the poet's nickname, the dynasty; never "which line follows" or a fill-in-the-blank (meaningless in English, trivial in Chinese). Works in English: yes, poem titles in characters + pinyin + English title.
- **歇后语:** the joke is the pun of the second half (猪八戒照镜子 — 里外不是人); in English it needs explaining, in Chinese the first half gives the punchline to anyone who knows it. Recommend: no subcategory, or a small one asking only the character (who looks in the mirror: 猪八戒) for kids; keep or cut in the taxonomy decision.
- **对联 / 灯谜:** custom yes, solutions no (wordplay).
- **General rule for the scope text:** "Ask about origin, author, person, place, time or custom; never what the Chinese words themselves state; in en, Chinese terms as characters + pinyin + English gloss" (`plans/26-china.md` "Language and format").

## Overlap with base (copies' ground)

What the base copies (part 5) already bring, so new subcategories keep off it or take only the China-specific slice.
- `base` holds ≈ 159 China-related questions (`plans/26-china.md` "Content sensitivity": Forbidden City, pandas, tea, Great Wall, Mao items); after part 5 they sit in reused subcategories unless the map moves a whole subcategory.
- World science, world geography, world history, foreign film, football, foreign music, Western art, fashion, superheroes: `base` ground; the China slice of each (Chinese scientists, Chinese film, CBA) is new ground.
- Pandas, Great Wall, terracotta army, chopsticks, dragon, zodiac, gunpowder already appear in `base`: new subcategories ask the next layer (卧龙, 八达岭 vs. 慕田峪, 兵马俑's discovery year) and leave the headline facts to the copies.

## Suggested areas for the taxonomy (non-binding)

Raw candidates for task 2382's proposal, grouped by subject, with the lowest `known_at` that keeps kids in reach.
- **history:** dynasties and emperors (3), ancient inventions (3; science possible), myths and creation (1), folktales (3), gods and creatures (2), philosophy and teachers (5), idioms and their stories (5), Chinese characters and scripts (3), spoken varieties (6), late Qing and Republic (8, facts), founding to present (6, facts), textbook figures (2).
- **geography:** provinces and cities (3), rivers and lakes (3), mountains and landforms (3), climate and regions (6), festivals (1), calendar and solar terms (4), zodiac (1), customs and etiquette (3), eight cuisines (4), snacks and street food (2), tea (6), places and heritage (2), ethnic customs (5, facts), school life and daily safety (1).
- **nature:** iconic animals (1), plants and flowers (3), farm, silkworms and fish (2), reserves and hazards (6).
- **science:** ancient maths and puzzles (3), ancient science and engineering (5), medicine history (8), modern scientists (8), space programme (4), big engineering (5), internet and tech (6; media possible).
- **arts:** ancient poems (1), classical prose (8), four classic novels (2), modern literature (9), nursery rhymes (1), fables (1), music and instruments (4), opera (5), calligraphy and painting (4), crafts (4), C-pop (6).
- **media:** cartoons (1), TV classics (5), film (5), Spring Festival Gala (4), games (5), brands and apps (5).
- **sport:** Olympics (4), table tennis and badminton (5), team sports (6), martial arts and traditional sports (3), board and tile games (3), children's games (1).
- Out of the taxonomy (decision 757 as read here): ideology and party, present leaders, Taiwan's status, disputed borders and seas, 1989, 文革 / 大跃进 beyond dates, Tibet and Xinjiang politics, COVID origins, LGBT topics (filtered on mainland Steam; `plans/26-china.md`).
