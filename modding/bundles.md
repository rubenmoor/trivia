# Make your own question bundle

A question bundle is a set of questions the family can switch on before a game, next to the game's own. You make one as a mod: a folder with a few JSON files and, if you like, pictures. Start from `template-bundle/` beside this file (15 questions about the solar system, Spanish and English) or let an AI write the files with `bundle-prompt.md`. The game checks your folder with `living-room-trivia --check-mod <folder>`. No stability promise: a game update may change this format.

## Folder layout
- `mod.json`: who the mod is (below)
- `data/bundles.json`: your bundles, one row each
- `data/bundles/<bundle>/`: one folder per bundle, named by its `id`
  - `categories.json`: categories and subcategories
  - `pool.json`: Spanish questions; `pool.en.json`, `pool.de.json`: English, German
  - `names.en.json`, `names.de.json`: translated names (optional)
  - pictures, sounds, videos: anywhere inside the bundle folder, e.g. `img/owl.png`
- All files UTF-8 JSON; copy the template and change what you need.

## `mod.json`
- `id`: lowercase letters, digits and `-`, 2–64 characters; the key of your mod everywhere (settings, question ids, the Workshop)
  - Change `template-bundle` to your own id before you publish: two mods with the same id can't both load.
- `name` (up to 80 characters), `description` (up to 2000)
- `version`: your own, e.g. `1.0.0`
- `game`: the game version you made it for, e.g. `0.1.0` (shown on the mods screen if it differs)
- `languages`: e.g. `["es", "en"]`
- `kind`: `["bundle"]` (optional, the game works it out)
- `workshopId`: written by `--publish-mod` on the first upload; leave it out, keep it once there

## `data/bundles.json`
- `{ "bundles": [ … ] }`, one row per bundle:
  - `id`: lowercase letters, digits and `-`; the folder name under `data/bundles/`
  - `kind`: `base` or anything else (e.g. `topic`)
    - anything else: an add-on next to our questions; off by default, the players switch it on before the game
    - `base`: a full replacement for our base bundle, offered as a second choice beside ours; only for a large, all-round set (a few hundred questions over the whole difficulty range); pick add-on when in doubt
  - `languages`: question languages, from `es`, `es-ES`, `en`, `de`; a language without its pool file isn't offered
  - `name`, `description`: plain text in your main language, shown in the bundle selector; translations in `names.<locale>.json`
- In the game your ids become `<mod id>:<id>`, e.g. `template-bundle:solar-system`; your bundle is marked player-made.

## `categories.json`
- `{ "categories": [ { "slug", "name", "subcategories": [ … ] } ] }`
- `slug`: lowercase id of the category; `name`: shown in the game; `subcategories`: names, at least one
- Every question's `subcategory` is one of these names, in every language's pool file: the names in `categories.json` are the keys, `names.<locale>.json` translates them.
- Slugs and subcategory names only need to be unique within the bundle; they may repeat the game's or other mods' names («Historia»): each bundle keeps its own.

## `names.<locale>.json`
- Optional, one per extra language; anything missing shows in the original.
- `bundles`: `{ "<bundle id>": { "name", "description" } }` (the id from `bundles.json`, without your mod id)
- `categories`: `{ "<slug>": "<name>" }`
- `subcategories`: `{ "<name in categories.json>": "<translated name>" }`

## Pool files
- `{ "version": 1, "questions": [ … ] }`; one file per language; the same `id` in two files = the same question translated.
- Question fields:
  - `id`: lowercase letters, digits and `-`, up to 64 characters, unique in your mod, e.g. `dino-001`
  - `difficulty`: whole number 1–15 (below)
  - `subcategory`: a name from `categories.json`
  - `description`: one funny sentence shown before the question; must not give the answer away
  - `question`, `answer`
  - `wrong_answers`: exactly 3
  - `hints`: exactly 3, vague → strong; the third may nearly give it away, without containing the answer
  - `fun_fact`: one short true sentence shown after the answer
  - `media`: optional (below); no media: leave it out
  - `background`: only for a sound: `{ "file_url", "credit" }`, a picture shown while it plays
  - `status`: optional, only `approved`
- The game shuffles the four options.

## Difficulty
Difficulty means who can answer it, not how obscure the fact is.

| Difficulty | Who can answer it |
|---|---|
| 1 | a 6-year-old |
| 3 | a 9-year-old |
| 5 | an 11-year-old |
| 7 | a 13-year-old |
| 10 | a 16-year-old with good school knowledge |
| 12 | most adults |
| 14 | a well-read adult, or someone who studied the field |
| 15 | trivia specialists |

- Rate by who answers it most easily: things kids know from cartoons, films and games are easier than they look; school facts (prize names, years, theory) are harder.
- Hard means fewer people know it, never a fact nobody could know or work out.
- Each age group plays a window of the scale, 12 questions a game, easy to hard:

| Age group | Ages | Window |
|---|---|---|
| Kids | 6–10 | 1–6 |
| Teens | 11–14 | 1–10 |
| Young adults | 15–22 | 4–13 |
| Adults | 23+ | 5–15 |

- Cover the window of the audience you write for, every level, spread evenly; e.g. a kids bundle: 1–6, about the same number at each.
- `--check-mod` lists per age group how many questions are in its window and which levels have none.

## Media
- `media`: `{ "type", "role", "file_url", "credit", "source_url" }`
  - `type`: `image`, `audio` or `video`
  - `role`: `essential` (the question needs it: «Which planet is this?»), `illustrative` (shows the topic, never the answer), `decorative` (mood only, shown blurred)
  - `file_url`: path inside the bundle folder, e.g. `img/planet.png`; web addresses and paths outside the folder are dropped (an `essential` question with them too)
  - `credit`: required for every file you didn't make yourself: author · licence · source, e.g. `Jane Doe · CC BY 4.0 · Wikimedia Commons`; your own: e.g. `Jane Doe · CC0`
  - `source_url`: optional, the page you got it from
- Credits appear on the game's Credits screen; use only files you may share (your own, CC0, CC BY, public domain).
- Images: at most 1920 px wide, at most 500 KB each (PNG, JPG, WebP).
- No picture? Leave `media` out: the question shows as text only.

## Writing good questions
- One breath: the question read aloud in one go, ideally under 120 characters.
- Four options of the same form and length: all names, all numbers, all years.
- Wrong answers: believable, but clearly wrong once you know the answer.
- No giveaways: not in the description, the question, the first two hints or the picture.
- Superlatives about the real world: «What is the largest planet?», never «Which of these is the largest?»
- A clue only the answer fits: ask yourself what else in the world fits it.
- Family-friendly: no deaths, violence or mockery as the point of a question.
- Only facts you are sure of; drop a question rather than guess.

## Try it
- Copy your folder into the local mods folder:
  - Windows: `%APPDATA%\trivia\mods\`
  - Linux: `~/.config/trivia/mods/`
- Restart the game; «Mods» on the start screen lists it; the first time, «Allow mods», then keep it on.
- Choose your bundle before a game; it shows «Player-made · <mod name>».

## Check it
- From a terminal in the game's install folder: `living-room-trivia --check-mod <folder>` (Windows: `LivingRoomTrivia.exe --check-mod <folder>`; the result also goes to `<folder>-check.log` beside the folder)
- Output: per bundle and language, questions ok and dropped; per age group, questions in its window; last line «loads as is» or «fix the errors above»; exit code 0 = fine, 1 = errors.
- Why a question was dropped:
  - `bad_id`: id not lowercase letters, digits and `-`
  - `duplicate_id`: the same id twice in one language
  - `no_text`: `question` or `answer` empty
  - `wrong_answers`, `hints`: not exactly 3
  - `difficulty`: not a whole number 1–15
  - `subcategory`: not in `categories.json`
  - `status`: something other than `approved`
  - `bad_media`: `file_url` a web address or outside the folder; only the media is dropped, unless `essential`
- Other errors: `media_missing` (file not found), `bad_categories`, `bundle_row`, `bad_field` (in `mod.json`), `no_pool` (no pool file for any language).

## Share it
- `living-room-trivia --publish-mod <folder>` uploads it as a Steam Workshop item (Steam running; `--dry-run` to try without uploading); run it again to update.
