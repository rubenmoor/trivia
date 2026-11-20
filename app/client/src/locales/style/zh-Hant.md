# Style guide: `zh-Hant` (Traditional Chinese, Taiwan)

How the UI talks in `zh-Hant.ts`: the `zh-Hans` guide (`style/zh-Hans.md`) in Traditional characters with Taiwan's vocabulary. The catalog is OpenCC `s2twp` of `zh-Hans.ts` plus a vocabulary pass, then a native read (decision 762; plan 141's volunteer). Read this before changing a string in `zh-Hant.ts`; new bad patterns found in review go into the last section. Everything not listed here is as in `zh-Hans.md` (address «你們», keys stay Latin, sensitivity rule).

## Glossary
Differences from `zh-Hans.md`; use them as written.
- Flag: «檢舉» («檢舉這道題», «已檢舉的題目»), «審核»; never «舉報», «稽核»
- Device: «控制器» (pad), «鍵盤和滑鼠»; «選單», «返回主選單»; «全螢幕» / «視窗模式»
- Software terms: «模組», «資料夾», «檔案», «影片», «音訊», «程式碼», «權限», «帳號», «傳送», «儲存», «預設», «匿名資料»
- Jokers: same names as `zh-Hans` converted: «提示», «跳過清除», «仙女教母», «挑剔小姐», «神來一槍»; they follow the joker-name decision for `zh-Hant`
- Steam terms as `tchinese`: «Steam 成就», «Steam 雲端存檔», «Steam 創意工坊»
- Career: grades «小學», «國中», «高中», «大學»; diplomas «小學畢業», «國中畢業», «高中畢業»
- Rank names: from `zh-Hans`, converted

## Punctuation and spacing
- Quotes 「…」 (Taiwan), 『…』 inside; full-width `，。？！：；（）`; book titles 《》
- Spacing around digits and Latin as in `zh-Hans.md` (none next to digits and `{param}`, one around Latin words)

## Bad patterns
Seen in review; guidance, not a lint. Wrong → right.
- Mainland vocabulary left by the converter or the draft: «手柄» → «控制器», «舉報» → «檢舉», «稽核» → «審核», «許可權» → «權限», «賬號» → «帳號», «制作» → «製作», «發送» → «傳送»
- Mainland quotes “…” → 「…」
- Mainland level term «初中» → «國中»
