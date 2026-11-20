# 26 — China: Chinese variants and the Chinese audience

**Status:** evaluation (`plan 228: Chinese variants and the Chinese audience (evaluation)`, task 2337, 2026-11-19); decisions 756–759 answered 2026-11-19 (section "Decisions"; applied by task 2338)

This document decides nothing by itself: it compares which written Chinese the game could ship, what each costs, and what selling a family trivia game to Chinese speakers means beyond translation. Spoken "dialects" are not separate written languages for a text game, so the real choice is between the two scripts (Simplified, Traditional) and the regional vocabulary that goes with them. The audience sections list the legal, political and technical facts a developer from Europe would not expect, each with what it means for us and the decision it raises. Bound by decisions 217, 220, 222, 236, 752, 753 (copies, volunteers, picker gate, English-first `base`, one base per session, content depot); "the zh locale(s)" in every later part = the answer to the variant decision below.

## Comparison

| | zh-Hans (mainland, SG, MY) | zh-Hant Taiwan (`zh-TW`) | Hong Kong / Macau | Spoken varieties |
|---|---|---|---|---|
| Steam language | `schinese`; 21.98 % of the survey, Oct 2026 (Sep ≈ 31.4 %) | `tchinese`; 1.30 %, Oct 2026 | none of its own: `tchinese` | none |
| Font (CJK set) | GB 2312 L1 3755 / 通用规范汉字表 8105; Noto Sans SC variable woff2: 1.6 MB (3755), 2.9 MB (6763), 13.2 MB full | Big5 常用字 4808; Noto Sans TC, similar sizes | Noto Sans HK (glyph forms differ slightly from TC) | — |
| Translation path | own `--translate zh-Hans` run | own run, or zh-Hans + OpenCC `s2twp` + vocabulary pass | `s2hk` or the TW text; written standard Chinese | — |
| Reviewer need | 1 volunteer (decision 220, decision 754) | 1 more volunteer, also for a converted text | read by the TW volunteer | — |
| Cost / approved (est.) | ≈ $0.12–0.20; 6000 → ≈ $830–1380 | own run as zh-Hans; conversion ≈ $0 + vocab pass ≈ $150–300 | ≈ $0 on top of TW | — |
| Content framing | PRC curriculum (部编 textbooks), PRC history framing | Taiwan 108 curriculum, own history framing | between both; British colonial past | — |

## Simplified Chinese (`zh-Hans`)

Written standard Chinese in simplified characters: the mainland, Singapore and Malaysia. By far the largest Chinese audience on Steam.

- **Steam:** language `schinese`; Steam survey Oct 2026: 21.98 % (−9.41 pts from Sep), English 39.04 % ([survey](https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam)). The share swings ±10 pts month to month with Chinese internet-café sampling ([GamingOnLinux, Feb 2026 swing](https://www.gamingonlinux.com/2026/03/steam-survey-for-february-2026-shows-a-big-swing-to-simplified-chinese), [Sep 2026](https://www.gamingonlinux.com/2026/10/steam-survey-for-september-2026-shows-a-drop-in-linux-with-simplified-chinese-rising/)); read it as "a fifth to a third of Steam", not as buyers of a family quiz. `guessTag()` already maps `schinese` (`plans/15-i18n.md`).
- **Fonts:**
  - coverage: GB 2312 level 1 = 3755 common characters; 通用规范汉字表 (2013) = 8105, level 1 = 3500. A trivia pool with names and places goes beyond level 1; the build subsets to the characters the pool and catalogs use ∪ a common set (plan 142's script).
  - measured 2026-11-19 (pyftsubset, Noto Sans CJK SC 2.004 variable, all weights, + ASCII and CJK punctuation): GB 2312 level 1 → 1.63 MB; all of GB 2312 (6763) → 2.92 MB; full SC face → 13.2 MB. A static single weight is roughly half.
  - today: `app/client/public/fonts` 96 KB (Baloo 2 33 KB, Nunito 39 KB, OFL texts); `app/desktop/media-budget.json` has no `fonts` key (audio 7, file 5, video 32 MB; content 950 MB, decisions.md D-row): a 2–3 MB CJK subset is small against the content depot, large against today's fonts.
  - OFL candidates: Noto Sans SC / Source Han Sans SC (same design, many weights, [OFL](https://github.com/notofonts/noto-cjk)); Resource Han Rounded (rounded, derived from Source Han Sans, OFL, CN/TW/HK subsets: [repo](https://github.com/CyanoHao/Resource-Han-Rounded), [AUR](https://aur.archlinux.org/pkgbase/ttf-resource-han-rounded)), the closest match to Baloo / Nunito; LXGW WenKai (kai style, OFL, [CTAN](https://www.ctan.org/pkg/lxgw-fonts)): friendly but handwriting-like, display only.
  - system fallback: Windows ships Microsoft YaHei (SC) / JhengHei (TC); Linux and the Steam Deck have Noto CJK only if installed (SteamOS ships it for the Steam client, not guaranteed to the game's Chromium): zero bytes, uneven look, no guarantee. Recommended: ship a subset, system fonts last in the chain. The choice is plan 142's font decision.
- **Translation path:** own `qgen batch --translate zh-Hans` run from English sources (decision 236: zh never steers `base` drafting); the locale prompt (part 8) carries the sensitivity rule and the format rules below.
- **Reviewer need:** one native volunteer (decision 220); pilot sheet, one release sample of 30, a full sheet of Chinese-language questions (decision 754). No volunteer reachable = a risk to the release, not a cost.
- **Cost per question:**
  - baseline `qgen report --cost` (2026-11-19): translation en $0.09, de $0.12, es-ES $0.11 per approved; recent de runs `tr-de-9`…`tr-de-22` $0.13–0.15; overhead outside batches ×1.15.
  - CJK tokens: Claude takes ≈ 1 token per Chinese character, ≈ 1.17× English per meaning ([measurement](https://dev.to/synthorai/which-llm-is-cheapest-for-your-language-tokenizer-costs-measured-1k5m)); other write-ups 1.5–2.4× ([aihola](https://aihola.com/article/claude-tokenizer-language-tax), [hackernoon](https://hackernoon.com/the-hidden-language-tax-making-ai-more-expensive-for-non-english-users)). Only output and the fact-check context grow; the English source and prompts stay.
  - estimate: $0.12–0.20 per approved; 6000 × ($0.12–0.20) × 1.15 ≈ $830–1380 per zh locale. The pilot run (`task 2303: Pilot translation run zh-Hans of chinese-base: run, native spot check, budget decision`) replaces this with a measured figure.
- **Content framing:** mainland compulsory curriculum 义务教育课程方案 (2022 edition, from autumn 2022): 道德与法治, 语文, 数学, 外语, 历史, 地理, 科学/物理/化学/生物学, 信息科技, 体育与健康, 艺术, 劳动 ([chinanews](https://www.chinanews.com.cn/gn/2022/04-21/9734982.shtml), [Hunan implementation](https://m.voc.com.cn/xhn/news/202210/14691629.html)); 语文 is heavy on classical poems and idioms (古诗词, 成语); history follows the PRC's official periodisation. Part 6's taxonomy draws from it.

## Traditional Chinese for Taiwan (`zh-Hant` / `zh-TW`)

Traditional characters with Taiwan's own vocabulary (軟體 not 软件, 計程車 not 出租车, 影片 not 视频); Bopomofo (注音) is a phonetic aid for children and IME input, not needed in a text game.

- **Steam:** `tchinese`, 1.30 % (+0.03), Oct 2026 ([survey](https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam)); steady, unlike `schinese`. About 1/17 of the Simplified share, but a market with no licence barrier and a strong PC culture.
- **Fonts:** Big5 has 5401 common characters, MOE 常用字 4808; Noto Sans TC / Source Han Sans TC; Resource Han Rounded has a TW subset. Glyph shapes differ by region (same code point, other form), so TC needs its own face, not the SC one; subset size about as for SC.
- **Translation path:**
  - option A, own run `--translate zh-Hant`: same cost as zh-Hans, independent text, Taiwan framing in the prompt.
  - option B, conversion: zh-Hans → OpenCC `s2twp` (characters + Taiwan phrases, [OpenCC](https://github.com/BYVoid/OpenCC)) → an LLM vocabulary and framing pass → native read. OpenCC picks the first candidate on one-to-many mappings (≈ 12 % of Simplified characters map to several Traditional ones, e.g. 发 → 發/髮, 后 → 後/后, 干 → 乾/幹/干); sentence accuracy of converters 55–85 % in a 2020 study ([arXiv 2005.03375](https://arxiv.org/pdf/2005.03375), [opencc-python](https://raw.githubusercontent.com/yichen0831/opencc-python/master/README.md)); `--ambiguities` can mark the risky spans. Transliterated foreign names differ between Taiwan and the mainland (e.g. 悉尼 / 雪梨, 奥巴马 / 歐巴馬) and OpenCC knows only a few: the vocabulary pass is not optional.
  - pipeline code: B needs a conversion step (`opencc-js` or the Python binding, a new `qgen` subcommand writing `questions.zh-Hant.json` from `questions.zh-Hans.json`, then the existing review); A needs nothing but the locale entry. B also inherits every zh-Hans fix only by re-running.
- **Reviewer need:** a second volunteer; a converted text needs a native read as much as a translated one (decision 754's pilot, release sample and Chinese-language sheet per zh locale).
- **Cost:** A ≈ as zh-Hans (≈ $830–1380 for 6000); B ≈ $0 conversion + a vocabulary pass at ≈ $0.02–0.05 per question ≈ $150–300.
- **Content framing:** the 108 curriculum (十二年國教課綱, from 2019) teaches history as Taiwan → China and East Asia → world ([Taipei Times 2018](https://www.taipeitimes.com/News/taiwan/archives/2018/08/11/2003698324), [TIMSS encyclopedia](https://timss.bc.edu/timss2019/encyclopedia/pdf/Chinese%20Taipei.pdf)); fewer classical texts than before; history and civics framing differ from the mainland on 1911–1949, the ROC and the present. Shared with the mainland: classical poetry, idioms, festivals, cuisine, geography of the land, science, pre-1911 dynastic history, world knowledge.

## Hong Kong and Macau

Written standard Chinese in Traditional characters; Cantonese only in speech and informal writing (written Cantonese with 嘅, 咗, 冇 appears in ads and chat, not in schoolbooks).

- **Steam:** no language of its own; Hong Kong players pick `tchinese` (or English). No separate share in the survey.
- **Fonts:** Noto Sans HK / Source Han Sans HC (HK glyph forms; TC is acceptable to readers).
- **Translation path:** OpenCC `s2hk` or the Taiwan text as is; HK vocabulary differs from Taiwan's (e.g. 的士 / 計程車), but a `zh-HK` locale for a sub-1 % slice isn't worth a reviewer.
- **Content framing:** HK schools follow their own curriculum (中國歷史 as a separate subject, citizenship and national security education since 2021); post-2019 politics are as sensitive as on the mainland.
- **Result:** no own locale; HK and Macau players play `zh-Hant` (if shipped) or `zh-Hans`.

## Spoken varieties: why no "dialect" locales

The milestone mentions "two or three main dialects of mainland China". Mandarin (普通话), Cantonese (粤语), Wu (吴语, Shanghai), Min (闽语, incl. Hokkien / Taiwanese), Hakka (客家话) are spoken languages, often mutually unintelligible, but they share one written standard: every literate speaker reads and writes standard written Chinese (Mandarin-based), in Simplified or Traditional characters.

- **A text game:** all text is read, never heard; a Cantonese or Shanghainese family reads the same written Chinese as a Beijing family. Writing a question in "written Shanghainese" would be odd to them, like writing a German quiz in Swiss German dialect spelling.
- **Written Cantonese** exists but is informal; no Steam language, no school standard.
- **What remains a real choice:** the script (Simplified vs. Traditional) and the regional vocabulary (mainland vs. Taiwan vs. HK). So: one or two written locales, not three dialects.
- **Spoken varieties as content:** they make good `chinese-base` questions ("In which city is Wu Chinese spoken?") — part 6's taxonomy, not a locale.
- **Taxonomy research:** curricula, family culture, per-topic subject, `known_at` and sensitivity status: `authoring/data/bundles/chinese-base/research.md`.
- **Taxonomy applied:** `app/data/bundles/chinese-base/categories.json` (33 categories, 201 subcategories), `names.{en,zh-Hans,zh-Hant}.json`, `authoring/data/bundles/chinese-base/related.json` (`decision 786: chinese-base taxonomy: categories, subcategories and the map from base`).

## The Chinese audience

What selling to Chinese speakers means beyond the words. Each implication: what it means for us, and the decision it raises or why it doesn't.

### Mainland sales: NPPA licence and Steam China
- **Facts:**
  - every game sold or operated in mainland China needs an NPPA publication number (版号); imported games need a Chinese publisher and operator to apply; no formal appeal or deadline ([MFAT report](https://www.mfat.govt.nz/assets/Trade-General/Trade-Market-reports/Chinas-Gaming-Market-Scale-Growth-and-a-Distinct-Regulatory-Environment.pdf)). 2026 imports: 3–12 a month (Sep 3, Oct 12: [Digital Policy Alert Oct 2026](https://digitalpolicyalert.org/event/45200-national-press-and-publication-administration-issued-october-2026-list-of-approved-imported-online-video-games), [Sep 2026](https://digitalpolicyalert.org/event/44203-national-press-and-publication-administration-issued-september-2026-list-of-approved-imported-online-video-games)), a few percent of all approvals.
  - Steam China (蒸汽平台, Perfect World, open beta 2021-02-09) is a separate store with only licensed games: ≈ 536 products in 2026 ([AppInChina guide](https://appinchina.co/blog/the-complete-guide-to-steam-china/), [PC Gamer launch](https://pcgamer.com/steam-china-launch)).
  - global Steam is reachable from the mainland in practice but unlicensed; the community pages were blocked in 2017 and store access had outages (Christmas 2021); it can be blocked any time ([PC Gamer 2017](https://www.pcgamer.com/steam-community-access-has-been-blocked-in-china), [Fortune 2021](https://fortune.com/2021/12/28/global-pc-game-superstore-steam-has-basically-gone-dark-in-china-and-no-one-knows-why/), [SCMP 2021](https://amp.scmp.com/tech/policy/article/3161180/chinas-gaming-crackdown-concerns-about-steam-ban-heightened-after)).
- **What it means for us:** a licence needs a domestic publisher, a content review of every question (thousands of trivia facts, many about history and politics), real-name and anti-addiction wiring, months to years; a solo developer with no Chinese entity can't apply. Mainland families buy on global Steam (most PC players there already do) at Valve's regional price, at the risk of a block that would hit every Western game alike.
- **Decision raised:** store targets (recommended: global Steam only).

### Content sensitivity
- **Topics:** Taiwan's status and the ROC (flag, "country", president); Tibet and the Dalai Lama; Xinjiang and the Uyghurs; Hong Kong 2019–2020; 4 June 1989; the Cultural Revolution and the Great Leap Forward (judgements, death tolls); Mao and present leaders (jokes, caricatures, Winnie-the-Pooh); disputed borders on maps (Arunachal Pradesh / 藏南, Aksai Chin, Kashmir, South China Sea nine-dash line, Senkaku / 钓鱼岛); Falun Gong; Japan's wartime history (Nanjing) as a political flashpoint; LGBT content is filtered on mainland Steam ([Outlook Respawn](https://respawn.outlookindia.com/gaming/gaming-news/steam-reportedly-restricts-lgbtq-tag-access-in-china)). Taiwanese players are just as sensitive the other way: a "Taiwan, province of China" wording would be resented.
- **Scan of `base` (2026-11-19, 6746 approved `base` questions, English text and media metadata):**
  - 159 mention China or Chinese; most are culture, science, geography (Forbidden City, pandas, tea) and fit.
  - touching the list: `q-4242` (Mao, Long March, Little Red Book), `q-2944` (Bamboo Curtain around "Mao's China"), `q-2638` (Potala as "the winter home" of the 1989 Nobel Peace laureate, i.e. the Dalai Lama), `q-0969` (Hong Kong, Singapore, Jamaica: British colonies), `q-2183` (Taipei 101: neutral, but places Taiwan), `q-2989` and `q-3548` (Mount Kailash "in Tibet": neutral wording), `q-1645` (Ho Chi Minh on Vietnamese notes), `q-6366` (Le Duc Tho refusing the Nobel); none about Tiananmen 1989, Xinjiang, Falun Gong; "1989" hits are the Berlin Wall and films.
  - media: 58 map and 70 flag media in `base`; none shows the ROC flag; world and region locator maps (`q-2377` LocationIndianOcean.png, `q-0417` Circum-Pacific belt, `q-3050` and `q-3863` a 1794 world map, `q-0653` a 1939 air-route map) may draw Taiwan in its own colour or India's claimed borders; Commons locator maps follow de-facto borders. Any map with East or South Asia on it needs a look in part 5's fit pass.
- **Steam (global):** Valve's rules ask for no illegal content but don't impose Chinese law; the global store shows a game to every region unless the developer restricts it. The risk isn't Valve but players' reviews (review-bombing over a map or a "country" label) and a Chinese family meeting a question they find offensive.
- **What it means for us:** one rule for `chinese-base` drafting, part 5's fit pass, every zh translation, the zh catalogs (plan 142) and the store texts (plan 144). The game's tone (family party, no gotchas) argues for leaving contested politics out altogether rather than stating "neutral facts" that each side reads as taking sides; `base` for other locales is not affected unless the developer says so.
- **Decision raised:** sensitivity rule (recommended: avoid contested political topics entirely).

### Taiwan vs. mainland framing
- **Facts:** one `chinese-base` can't frame modern history and politics for both (1949, the ROC, "our country", national holidays: 国庆节 1 Oct vs. 國慶日 10 Oct); both share dynastic history, poetry, idioms, festivals, food, nature, science and world knowledge.
- **What it means for us:** with the recommended sensitivity rule, one shared `chinese-base` with shared content works for both scripts; anything only one side would ask ("our national anthem", "our capital") is left out. Variant-specific content (a Taiwan-only or mainland-only set) is out of scope.
- **No decision:** follows from the sensitivity rule; a Taiwan-specific content line would be a new milestone, and nobody has asked for one.

### Reachability from the mainland
- **Media:** ship with the game (decision 753, D-17); Commons being blocked in China doesn't matter.
- **Report server and telemetry:** both on Cloudflare Workers at `https://trivia-reports.trivia-question-reports.workers.dev` (`app/desktop/package.json` `reportUrl`, plan 103, plan 106). `*.workers.dev` has been reported SNI-blocked in China, and Cloudflare's own `pages.dev` isn't served there ([GDIndex issue](https://www.github.com/maple3142/GDIndex/issues/206), [Cloudflare China FAQ](https://developers.cloudflare.com/china-network/faq/)); a custom domain on Cloudflare often works but isn't guaranteed; Cloudflare's China Network needs an ICP licence via JD Cloud ([Cloudflare China Network](https://www.cloudflare.com/china-network/)). Not measured from inside China (no vantage point); expect "sometimes or never".
- **Code paths checked (2026-11-19):**
  - reports: `report:available` only checks a valid Steam user and a configured URL (`app/desktop/main.mjs` `reportAvailable`), no network probe; `report:send` posts on the player's «Enviar» with a 2 s ticket wait, 5 s connect, 10 s total (`report.mjs` `CONNECT_MS`, `TOTAL_MS`), then the UI offers «Copiar» (plan 93): at most ≈ 12 s of a spinner, never a blocked game.
  - telemetry: opt-in; sent at quit with the window hidden, a 4 s budget (`QUIT_BUDGET_MS`), and one leftover try 30 s after the next start in the background (`LEFTOVERS_MS`), then deleted either way: never blocks play.
  - everything else is offline (`trivia` serves `/data/` and media locally; the game never downloads media).
- **What it means for us:** the game works fully offline in China; a mainland player's report may fail to send and fall back to «Copiar» (they can paste it in Steam Discussions, itself flaky there), and their telemetry may be lost. That skews played-difficulty data (decision 122) away from mainland players, which is acceptable.
- **Decision raised:** reports and telemetry for zh players (recommended: keep as is, failure falls back silently; alternatives a custom domain, or off for zh).

### Personal data: PIPL vs. our GDPR line
- **Facts:** PIPL applies to processing abroad of data of people in China when the purpose is offering them products or services (art. 3); such processors must name a representative in China (art. 53); cross-border transfers need consent and a mechanism; personal information of children under 14 is sensitive ([Winston & Strawn](https://www.winston.com/en/insights-news/online-videogame-cos-must-prepare-for-china-data-law), [IBA](https://www.ibanet.org/chinas-restrictions-on-cross-border-transfer-of-personal-information), [Deloitte guide](https://www2.deloitte.com/content/dam/Deloitte/cn/Documents/risk/deloitte-cn-ra-cbdt-compliance-guide-en-240606.pdf), [Morgan Lewis on the 2024 Guangzhou case](https://www.morganlewis.com/ru/pubs/2024/11/chinese-court-concluded-landmark-case-on-cross-border-transfer-of-personal-information)).
- **Our data (`PRIVACY.md`):** reports send question id, language, the question as shown, the player's note, versions and a one-time ticket; kept without account id, IP or name, ≤ 90 days. Telemetry (opt-in, off by default) sends a random install id and session id, per-game mode, language, age group, levels, result, per-question right/wrong; ≤ 30 days; a salted hash of the SteamID for a daily rate counter, dropped at day's end. Player names stay on the device and in Steam Cloud.
- **What it means for us:** the only plausibly personal items are the free-text note (a player could type a name) and the transient SteamID / IP at Cloudflare and Valve; telemetry's random ids are pseudonymous at most. Both features are already consent-based (click to send, opt-in), which is what PIPL's consent rule asks; a zh `PRIVACY.md` section and a zh consent text (plan 142 catalog, plan 144 store text) are needed anyway. The art. 53 representative is the open point; for a tiny volume of pseudonymous, consented data enforcement against a foreign solo developer is unlikely, but not zero. Turning reports and telemetry off for zh removes it entirely.
- **Decision:** folded into the reports-and-telemetry decision above (its option "off for zh" is the PIPL-safe one).

### Language and format
- **Numbers:** Chinese counts in 万 (10⁴) and 亿 (10⁸): 1 400 000 000 = 14亿, 38 万 km²; numbers in questions and answers follow it (the locale prompt), `Intl.NumberFormat('zh')` groups by thousands, fine for scores.
- **Dates:** 2026年11月19日, 公元前221年 for BC; century as 19世纪.
- **Names:** Chinese names family-first (毛泽东, not "Zedong Mao"); foreign names in their established Chinese form (爱因斯坦, 莎士比亚), mainland vs. Taiwan forms differ (see Taiwan section); one transliteration per person across the pool: a glossary the translator keeps (part 8).
- **Pinyin in the English pool:** `chinese-base`'s English text writes Chinese terms in pinyin with tone marks only where needed and the characters in brackets for Chinese-language questions (e.g. "the idiom 画蛇添足 (huà shé tiān zú)"); Wade-Giles only in fixed names (Kuomintang, Tao Te Ching vs. Dao De Jing: one choice per term).
- **Punctuation:** full-width 。，？！：；“”《》 (book titles in 《》), no spaces between Chinese and digits or Latin by mainland convention (Taiwan often adds them); the `?` of the question becomes `？`.
- **Line breaking:** no spaces; CSS `line-break: strict` and `word-break: normal` work for CJK, `overflow-wrap: anywhere` must not break inside Latin words; plan 142's layout walk. A question of 60 characters is ≈ 30 English words: shorter on screen.
- **Key chips:** Chinese keyboards are QWERTY; letter shortcuts stay Latin (decision 53, `decision 671: Key chips are labels, not predictions`); but with a Chinese IME active `keydown` gives `e.key === "Process"` (`app/client/src/lib/intent.ts` reads `e.key`), so letter keys don't reach the game: plan 142's wiring task already plans an `e.code` fallback.
- **Answer letters A–D:** standard in Chinese exams (选择题 A/B/C/D); keep. 甲乙丙丁 would be old-fashioned.
- **No decision:** these are rules for part 8's locale prompt, plan 142's style guide and the drafting voice (part 7).

### Unexpected implications
- **Age rating, Taiwan:** Taiwan's Game Software Rating Regulations (遊戲軟體分級管理辦法) require a rating (普遍級 G … 限制級 R) displayed on the download page for games offered in Taiwan ([Wikipedia](https://en.wikipedia.org/wiki/Game_Software_Rating_Regulations)); Steam handles regional ratings through its content survey and IARC, but whether a Taiwanese rating label is required for a global Steam game isn't documented: plan 144 checks the Steamworks rating fields for Taiwan; a trivia game would be 普遍級.
- **Anti-addiction (mainland):** the 2021 NPPA rules (minors: 1 hour, 20–21 h, Fri–Sun and holidays, real-name check) bind licensed online games operated in China ([WEF](https://weforum.org/stories/2021/08/new-rules-in-china-restrict-video-gaming-to-3-hours-per-week-for-under-18s), [PC Gamer](https://www.pcgamer.com/china-really-doesnt-want-young-people-to-play-online-games)); an offline game on global Steam isn't in that system. No action under "global Steam only"; a Steam China or NPPA answer would bring it in.
- **Game name and trademark:** China is first-to-file; squatters register Chinese names of foreign brands, and a foreign mark doesn't protect its Chinese name (Clicker Heroes lost its name this way) ([Harris Sliwoski](https://harris-sliwoski.com/chinalawblog/china-trademark-registration-how-to-stop-squatters-from-stealing-your-brand/), [China Briefing](https://www.china-briefing.com/news/register-trademarks-in-china-before-market-entry/)). A foreign applicant must file through a Chinese agency. The Chinese store name ("客厅问答" or similar, plan 144's PUB-7 check) is a generic description, hard to squat; a CNIPA filing costs agency fees and isn't needed for selling on global Steam. No decision now; plan 144's name check notes it.
- **VPN use is an offence:** fines for unauthorised VPN use were reported in March 2026 ([AppInChina](https://appinchina.co/blog/the-complete-guide-to-steam-china/)): the store page and Discussions must not tell mainland players to use a VPN (e.g. to send a report).
- **Steam regional pricing:** Valve's recommended CNY price is far below the EUR price; key resellers move keys across regions. No decision: plan 144 / PUB pricing.
- **Volunteer reviewers in the mainland** may not reach GitHub or Google reliably; review sheets go as files (decision 754's sheets are files already).
- **Fonts on a Steam Deck in Chinese:** the Deck has CJK fonts for its own UI, but the game's Chromium may not see them: shipping a font is the safe path (plan 142).

## Recommendation
Research-time recommendations; the developer's answers are under "Decisions" below and win where they differ (variant: both; sensitivity: neutral facts; domain).
- Ship `zh-Hans` only now; `zh-Hant` later as its own decision, by conversion (OpenCC `s2twp` + vocabulary pass + native read) once zh-Hans and a Taiwanese volunteer exist.
- No dialect locales; Hong Kong and Macau read `zh-Hant` (later) or `zh-Hans`.
- Sensitivity: leave contested political topics out of `chinese-base`, every zh translation, the zh catalogs and the store texts; check every map with East or South Asia and every flag question in part 5's fit pass; `base` for es/en/de stays as is.
- Store: global Steam only; no NPPA licence, no Steam China.
- Reports and telemetry: keep as is for zh; failures fall back silently (already the case); add a zh section to `PRIVACY.md`.
- Font: ship a subset CJK font (Noto Sans SC or Resource Han Rounded; plan 142's font decision), ≈ 1.5–3 MB.
- Budget: ≈ $830–1380 per 6000 zh translations, measured by the pilot run.

## Decisions raised
- Variant(s): `zh-Hans` only now (recommended) / both at once / `zh-Hant` only → decision 756; "Comparison", "Simplified Chinese", "Traditional Chinese for Taiwan".
- Sensitivity rule for drafting, fit pass and translation → decision 757; "Content sensitivity", "Taiwan vs. mainland framing".
- Store targets → decision 758; "Mainland sales: NPPA licence and Steam China".
- Reports and telemetry for zh players → decision 759; "Reachability from the mainland", "Personal data: PIPL vs. our GDPR line".
- Ids: decision 756 (variant), decision 757 (sensitivity), decision 758 (store targets), decision 759 (reports and telemetry); answers written in by `task 2338: Apply the Chinese variant, sensitivity and store answers to the docs`.

## Decisions
Answered 2026-11-19; they override the recommendations above where they differ.
- `decision 756: Chinese variant(s): which written Chinese does the game ship in milestone 12?` → `zh-Hans` and `zh-Hant` both in milestone 12, a player choice like any language.
  - "The zh locale(s)" in every later part = `zh-Hans` + `zh-Hant`; each is its own locale in the picker, own pool, own catalog, own native reviewer (decision 220), own gate (decision 222).
  - Steam languages `schinese` + `tchinese`; fonts SC + TC; Hong Kong and Macau read `zh-Hant`.
  - How `zh-Hant` is translated: `decision 762: zh-Hant translation path: its own translation run, or conversion from zh-Hans?` → OpenCC `s2twp` conversion of approved zh-Hans (`authoring/tools/hant.py`, exceptions `authoring/data/zh-hant-exceptions.json`) + vocabulary pass + native read; no own run.
- `decision 757: Sensitivity rule for Chinese content: how do drafting, the fit pass and zh translation treat contested political topics?` → neutral facts only.
  - Rule text (verbatim into the fit prompt, the `chinese-base` voice, the zh locale prompts and store texts): contested topics are allowed when the question states an undisputed fact (a date, a name) without judgement or status wording; maps and flags are checked case by case.
  - Replaces the research recommendation "leave contested topics out entirely": no blanket ban on maps, flags or politics in shots, trailer or pool; each map or flag is judged on its own.
  - Same rule for `zh-Hans` and `zh-Hant`; `base` for es/en/de stays as is.
- `decision 758: Store targets for Chinese players: global Steam only, Steam China later, or an NPPA licence?` → global Steam now; Steam China later (needs a licence through a Chinese publisher).
  - No NPPA work, no anti-addiction work now; Steam China is a backlog item (`plans/backlog.md` B-23).
- `decision 759: Question reports and telemetry for Chinese players: keep as is, own domain, or off for zh?` → move the report/telemetry server to a custom domain on Cloudflare (needs a domain of our own) to improve reachability; otherwise as before (kept for zh, silent fallback, `PRIVACY.md` zh section).
  - Needs the developer to pick and register the domain; follow-up work: domain decision, then server and client URL change.
