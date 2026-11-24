# fit-9

Made by `qgen batch --bundle chinese-base --from base` on 2026-11-23 (plan 230): approved `base` questions judged for `chinese-base` (`prompts/fit.md`); kept and adapted ones copied. Verdicts: `authoring/data/bundles/chinese-base/fit.json`. Generated file: don't edit by hand.

- Judged by the fit pass: 188: kept 138, adapted 31, dropped 19
- Dropped by rule (no call): 0
- Developer flips copied: 0
- Not copyable yet (no approved, current English text): 406
- Left for later runs: 0
- Copies: 169, 164 approved, 5 needs work; adapted 31, 26 approved after revision
- Claude calls: 75, about $8.09 at list price

## Drop reasons

- too_hard_here (fit): 8
- latam_centric (fit): 6
- euro_centric (fit): 5

## Per base category and subcategory

| Category | Subcategory | Judged | Keep | Adapt | Drop | By rule |
|---|---|---|---|---|---|---|
| World geography | Countries | 29 | 22 | 2 | 5 | 0 |
| Animals | Birds | 35 | 21 | 8 | 6 | 0 |
| Science and maths | Nobel Prizes | 4 | 4 | 0 | 0 | 0 |
| Space | Solar system | 4 | 4 | 0 | 0 | 0 |
| Space | Stars and galaxies | 11 | 9 | 2 | 0 | 0 |
| History | World War II | 5 | 4 | 0 | 1 | 0 |
| History | Cold War | 1 | 1 | 0 | 0 | 0 |
| Myths and legends | Greek gods | 1 | 0 | 1 | 0 | 0 |
| Music | Classical music | 71 | 61 | 8 | 2 | 0 |
| Fashion and design | Traditional dress | 5 | 3 | 1 | 1 | 0 |
| Architecture and landmarks | Famous landmarks | 2 | 1 | 1 | 0 | 0 |
| Religion and philosophy | Sacred places | 2 | 1 | 1 | 0 | 0 |
| Religion and philosophy | Famous philosophers | 13 | 5 | 5 | 3 | 0 |
| Religion and philosophy | Big questions | 5 | 2 | 2 | 1 | 0 |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 3 of 26 (12 %)
- Major among review needs work: 1 of 5 (20 %)
- Problems by kind: giveaway 7 (3 major), overlap 1 (1 major), media 5 (3 major), difficulty 1 (0 major), style 1 (0 major), other 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 1 of 31 (3 %)
- Audit/review agreement (both accept or both not): 24 of 31 (77 %)
- Sample: 31 audited of 31; 31 Claude calls, about $1.85

Major findings on approved questions:

- **q-25543**: media, giveaway — The media is marked essential, but it is Mayall's well-known 1875 portrait of Karl Marx, shown sharp next to the question. The question text never refers to the photo, so the picture just shows the answer's face. Chinese families see this face everywhere, so the clues stop mattering. Use an illustrative image that doesn't show Marx (for example the British Museum Reading Room or a 19th-century factory). The facts check out: London, Engels, the Manifesto and the Highgate bust. Hint 3 ties Marx to “The Communist Manifesto”, which comes close to q-23762's answer but isn't the same fact. (http://127.0.0.1:8001/review/q-25543)
- **q-25574**: giveaway, media — This is a media-first question, and the clip isn't needed: "What is the star closest to the Sun?" is a famous fact that players answer from the text alone. The played window (2.5–9.5 s) only shows the "Sun" label and the www.eso.org watermark (going by the OCR; I had no tool to open the frame sheet or spectrogram), so the "Watch:" framing is empty because nothing in the window decides the answer. The facts are correct: Proxima at about 4.2 light-years, its name from the Latin for "nearest", and it is visible only from the far south of China. The silent audio doesn't matter for a video, and the title-word flag is false. (http://127.0.0.1:8001/review/q-25574)
- **q-25672**: giveaway, media — The text alone gives the answer, and the clip doesn't decide it. For Chinese families, "the famous piano concerto named after a great river" is simply the Yellow River Piano Concerto. The 60–90 s window (the opening "Boatmen" part) only shows Chinese performers in an orchestra hall, and nothing in it tells the Yellow River from the Yangtze. So the media-first check 1 fails. A fix would ask about something you can see or hear in the clip, such as the solo instrument or the era. I couldn't open the frame sheet or the spectrogram here, so this judgment rests on the aids text: OCR picks up only noise, the transcript has no words, and the loudness is fine. The licence basis is also shaky. This is a 1970 newsreel, not a film from before 1930 or a government work, and the concerto is a new 1969 arrangement whose co-arranger Yin Chengzong is still alive. The facts themselves check out: the 1939 cantata, written in about six days, and the May 1, 1970 premiere conducted by Li Delun. (http://127.0.0.1:8001/review/q-25672)

## Needs work

- **q-25521** (from q-21163) Watch: these famous sea cliffs, with a small round stone tower on top, rise over 200 m (650 ft) above the Atlantic. In which country are they? → Ireland: This question doesn't belong in chinese-base. It's about an Irish landmark, and hint 1 relies on the Western nickname “Emerald Isle”. The bundle is for China-centred knowledge and says facts about other countries belong in base. Move the question to base, where the clip and the question work as they are, or drop it from chinese-base. (http://127.0.0.1:8001/review/q-25521)
- **q-25523** (from q-5456) This movement began in 19th-century France, said only knowledge tested by science counts, and inspired the motto “Order and Progress” on Brazil's flag. What is it? → Positivism: The bundle is wrong. This question is about a French movement and Brazil's flag, with no Chinese connection, so under the bundle rule it belongs in `base`, not `chinese-base`. Hint 3 is also English wordplay ("positive" vs "negative") that doesn't work in Chinese (实证主义), and wordplay that fails in any of the bundle's languages has to go. Move the question to base, or replace it, and rewrite hint 3 without the pun. (http://127.0.0.1:8001/review/q-25523)
- **q-25535** (from q-6160) Socrates' mother was a midwife, and he said his questions helped minds give birth to ideas. What name did his method get from this? → Maieutics: This chinese-base question is also played in zh-Hans and zh-Hant, where the method is called 产婆术/產婆術, which literally means "midwife art". Since the question's clue is the midwife, the Chinese versions give the answer away: it is the only option that mentions midwives. A fixed version would have to drop the midwife clue, which is the heart of the question. Rhetoric, hermeneutics and heuristics are all Greek-derived terms too, so the clue also adds nothing beyond a translation. I can't confirm the fact from the review alone. The kept image (Vincent's Socrates teaching Alcibiades) fits. (http://127.0.0.1:8001/review/q-25535)
- **q-25569** (from q-21037) Watch: which bird is putting on this courtship show, with its white puffed-up chest and spiky fanned tail? → Sage grouse: This repeats related q-21036 almost exactly: a "Watch: which bird is this…" question about a sage grouse puffing out its white chest on frosty ground, very likely using the same BLM lek clip. It also doesn't fit chinese-base. The sage grouse lives only in western North America, and the hints point to US plains and sagebrush, so a Chinese family has no way in. The bundle asks for questions that need no link to Europe or the Americas. Drop it, or move one sage-grouse video question to base and keep only one. (http://127.0.0.1:8001/review/q-25569)
- **q-25604** (from q-21071) Listen: this is the national anthem of which country? → China: Hint 2 gives the answer away: for a Chinese family, 义勇军进行曲 (“March of the Volunteers”) is simply the name of China's national anthem, so naming it answers the question at hint 2, not hint 3. Hint 2 should give a vaguer clue instead, such as the 1935 composer's age or the anthem's march style, and leave out the title. (http://127.0.0.1:8001/review/q-25604)
