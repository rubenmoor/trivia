# Style guide: `zh-Hans` (Simplified Chinese)

How the UI talks in `zh-Hans.ts`: plain, friendly mainland Chinese for a family at the TV; playful in cheers and joker names, flat in menus and notices. Drafted by Claude from `en.ts` (`es.ts` for meaning), no native check yet (plan 141's volunteer, decision 220); the joker names are final (decision 775: Joker names for the Chinese UI (zh-Hans, zh-Hant)?). Read this before changing a string in `zh-Hans.ts`; new bad patterns found in review go into the last section. `zh-Hant.md` derives from this guide (decision 762).

## Glossary
Fixed terms; use them as written, never a synonym. Steam terms as Steam writes them in `schinese`.
- Modes: «主持人模式» (`mode.gamemaster`), «单人或团队» (`mode.solo`); the role: «主持人» («主持人作弊»)
- Jokers (the concept): «锦囊» («锦囊卡» for the print sheet); names «提示» (H), «跳过清除» (P), «仙女教母» (F), «挑剔小姐» (K), «神来一枪» (T); plain skip «只跳过»; keys stay the Latin letters of `en`
- Level: «关» («第{n}关»); the tower, the top, the crown: «塔», «塔顶», «皇冠»
- Question, answer, topic: «题目» (a question), «答案», «题材» (category on screen); a question card: «题卡»
- Question bundle: «题包»; base bundle «基础题包»; bundle names from `app/data/names.zh-Hans.json`
- Age group: «年龄段»; difficulty groups 简单 / 普通 / 困难 / 专家 (`names.zh-Hans.json`); «难度», «从» / «到», «自定义»
- Flag: «举报» / «提交审核», «举报这道题», «已举报的题目»; never «标记»
- Esc menu: «暂停»; «返回主菜单» (`overlay.restart`); «退出游戏» (`overlay.quit`); «游戏设置» (`overlay.settings`); «全屏» / «窗口模式»
- Steam terms: «Steam 成就» (never bare «成就»), «Steam 云存档», «Steam 创意工坊», «Steam Deck»
- Devices: «手柄» (pad), «键盘和鼠标»
- Career: «生涯», badges «徽章»; grades «小学», «初中», «高中», «大学»; diplomas «小学毕业», «初中毕业», «高中毕业»; «积分», «等级» (`career.rank`); rank names 1–15 in `career.ranks`
- Credits: «制作人员»

## Address
- «你们» for the family at the TV, never «您们», never «您»; where one person fits, «你»
- Prompts and buttons: bare verb phrases without a subject («选择题目», «输入名字»)
- Cheers: playful, 口语 («加油！», «离皇冠只差一步！»)

## Numbers, punctuation, spacing
- Full-width punctuation `，。？！：；（）`; quotes “…” (mainland); book titles 《》; ellipsis «……» for text, «…» only on waiting states («加载中…»)
- No space between Chinese and digits or `{param}` («第{n}关», «{n}道题»); one space around a Latin word or the key chip text («Steam 成就», «Steam Deck»)
- Counting: «道» for questions, «局» for games, «位» for players, «个» otherwise; plural forms only `other`
- Scores stay digits; thousands grouping via `Intl` (`1,840`); no 万 below 10 000
- Dates by `Intl` («2026年11月19日»); never typed into a leaf

## Buttons and prompts
- Short: buttons 2–6 characters, prompts one line at 1280 × 800
- No letter-spacing, no hyphenation; line breaks are the browser's (`line-break: strict`)
- «！» for cheers only, not menu rows; «…» for waiting states only
- Dialog titles that state the action: no «？» («举报这道题»)
- Keys and pad glyphs: shown by the `Prompt` chip, never typed into the text; exception `{key}` in `flag.on` / `flag.off`
- Shortcut letters stay Latin (QWERTY keyboards), unique per screen, not A–D where answers show (decision 53, `check:literals`)
- Sensitivity (plan 228, `plans/26-china.md`): no flags, maps or place-name wording that takes a side; no contested politics in any string

## Bad patterns
Seen in review; guidance, not a lint. Wrong → right.
- Plain machine translation: calques of English phrasing («你有多少题目要玩？») → short natural wording («要玩多少题？»)
- «您们» / «您»: too stiff for a family game → «你们» / «你»
- Half-width punctuation in Chinese text (`, . ? !`) → `，。？！`
- Space between Chinese and digits («第 3 关») → «第3关»
- «标记» for flagging a question → «举报»
- Bare «成就» for Steam achievements → «Steam 成就»
