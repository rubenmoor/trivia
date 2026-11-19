# Native review of the Chinese translation

This is the brief for volunteer native speakers who check the Chinese version of our family trivia game. The game runs on a TV: the family plays against the gamemaster, and 12 questions to victory. Questions are written in English and translated; you tell us where the Chinese is wrong, unnatural or unfair. Volunteers are unpaid and credited (with consent); a free Steam key comes with the playtest.

Locale reviewed: `zh-Hans` (Simplified Chinese). Change this one line if a second variant is added.

## For the volunteer

### Jobs and time
- Read the locale prompt `authoring/tools/prompts/locale-zh-Hans.md` (~1 h)
  - it holds the translation rules we gave the machine; it is also your yardstick
  - findings as comments only; nothing is edited silently
- Pilot sheet: 30 questions (~45 min)
- Chinese-language sheet: all questions about characters, idioms 成语 and poems (size varies)
- Release sample: 30 questions across all runs, before the release (~45 min)
- More sheets only if you offer
- UI: look at the screens in the gallery, then playtest via a Steam key on the `beta` branch (3–4 h)
- Store text drafts: read and correct (1–2 h)
- Total ≈ 8–10 h over months; ~1 week per sheet is fine

### What you check
- Faithful to the English source (always shown beside the Chinese)
- Natural Chinese, as a native would say it
- Hints and wrong answers that still work in Chinese (the wrong options must stay plausible, never give the answer away)
- Difficulty for Chinese players (difficulty 1–15 is shown; say if it is far off)
- Sensitivity rule: PLACEHOLDER(plan 228 apply task) names the rule of `plans/26-china.md`
- Text inside images, audio or video is never a problem; ignore it

### Verdicts
- Per question: approve / needs_work / reject / doesn't travel (fine in English, makes no sense for Chinese players)
- Problem kinds: giveaway, fact, ambiguity, overlap, media, difficulty, style, other (`authoring/tools/qgen.py` `PROBLEMS`)
- Feedback in English; optionally the corrected text in Chinese
- General comments at the end of the sheet

### Returning work
- The sheet is one HTML file; open it in a browser, no internet needed
- Progress stays in your browser; close and return any time
- When done: «Download verdicts» → `<sheet>.verdicts.json`, send it back by e-mail
- Gallery and store drafts: reply by e-mail with your notes

## For the developer

- Names and contacts stay outside the repo
- Per job, what to send:
  - prompt: `authoring/tools/prompts/locale-zh-Hans.md`
  - sheets: the file from `qgen spotcheck export` (`work/<run>/spotcheck-<run>.html`, or `work/spotcheck/<name>.html` for `--release` and `--subcategory`)
  - UI: gallery zip from `trivia-gallery --set task-<id> --only <shots>`, then a Steam key for `beta`
  - store: the draft texts
- Per reply:
  - verdicts: `qgen spotcheck import <file>` in `../trivia-review` (AGENTS.md: spot checks are human review work), merge into `main`, then `qgen report --qc`
  - prompt comments: proposals for `locale-zh-Hans.md`, `translate.md`, `translate-review.md` (QC.md step 4), never silent edits
  - playtest: answer the playtest decision of the UI plan; store: answer the store decisions
- No fit job: the `chinese-base` fit pass is reviewed by the developer in English
- Nothing waits for a reviewer (decision 414)
