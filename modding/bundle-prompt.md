# Let an AI write your question bundle

This prompt lets an AI chat assistant (ChatGPT, Claude, Gemini, …) write a question bundle for the game with you. It asks you a few questions first, then writes every file of a mod folder. The format is explained in `bundles.md` beside this file; you don't need it to use the prompt.

## How to use it
- Copy everything inside the box below and paste it into a new chat with your AI.
- Answer its questions, in your own language.
- For each file it writes, save the JSON block under the path shown above it, inside a new folder named like your mod's id, e.g. `dinosaurs/mod.json`, `dinosaurs/data/bundles.json`.
- Long sets come in parts: say «next» until it says it's done; add each part's questions to the same pool file.
- Check the folder: `living-room-trivia --check-mod <folder>` (see «Check it» in `bundles.md`); paste errors back to the AI to fix them.
- Read the questions yourself: AIs make mistakes, and your family will notice.
- Pictures: add them by hand afterwards, see «Media» in `bundles.md`.
- Try it: copy the folder into the mods folder and restart the game (see «Try it» in `bundles.md`).

## The prompt

````text
You help me write a question bundle for "¡Trivia!", a family trivia party game played on a TV. You write the bundle's files in the game's JSON format. Talk with me in the language I write in; these instructions are for you, don't repeat them to me.

STEP 1: ASK FIRST
Before writing anything, ask me all of this in ONE message, with your suggestion for each:
1. Topic: what the questions are about.
2. Audience: which age group plays it:
   - Kids, 6–10 years: difficulty 1–6
   - Teens, 11–14: difficulty 1–10
   - Young adults, 15–22: difficulty 4–13
   - Adults, 23+: difficulty 5–15
   - Everyone: difficulty 1–15
3. Question language(s): one or more of Spanish (Latin America, es), Spanish (Spain, es-ES), English (en), German (de).
4. How many questions (suggest 30–60; at least 12, one game's worth).
5. Bundle name, and a one-sentence description for the bundle selector.
6. Add-on or base: "add-on" (default, recommended) adds the questions next to the game's own; "base" replaces the game's whole base set and only makes sense for several hundred all-round questions over the full range.
Then wait for my answers.

STEP 2: WRITE THE FILES
Pick ids from the topic: a mod id like "dinosaurs" (lowercase a-z, 0-9 and "-", 2–64 characters), a bundle id (same rule, e.g. "dinosaurs"), a short question id prefix (e.g. "dino").
The MAIN language is the first language I chose. Write each file as its own fenced ```json block, with its path on the line above it, in this order:

a) mod.json
{
  "id": "<mod id>",
  "name": "<bundle name>",
  "description": "<one or two sentences>",
  "version": "1.0.0",
  "game": "0.1.0",
  "languages": ["<lang>", …],
  "kind": ["bundle"]
}

b) data/bundles.json
{ "bundles": [ { "id": "<bundle id>", "kind": "topic" (or "base"), "languages": ["<lang>", …], "name": "<name in main language>", "description": "<description in main language>" } ] }

c) data/bundles/<bundle id>/categories.json
{ "categories": [ { "slug": "<category slug>", "subcategories": ["<subcategory slug>", "<subcategory slug>", …] } ] }
- One category (two at most), 2–4 subcategories.
- Slugs are short English ids: lowercase a-z, 0-9 and "-", e.g. "dinosaurs", "jurassic-dinosaurs", "dinosaur-fossils"; unique within the file.

d) data/bundles/<bundle id>/names.<file lang>.json, one per language, the main one too; <file lang> is es for both Spanish varieties (names.es.json), plus names.es-ES.json only if Spain's names differ:
{
  "bundles": { "<bundle id>": { "name": "<name>", "description": "<description>" } },
  "categories": { "<category slug>": "<category name>" },
  "subcategories": { "<subcategory slug>": "<subcategory name>" }
}
- Names must be specific to the topic, never generic like "Animals", "History" or "Science". Good: "Dinosaurs of the Jurassic", "Dinosaur fossils".

e) The pool file per language: Spanish (Latin America) → data/bundles/<bundle id>/pool.json, Spanish (Spain) → pool.es-ES.json, English → pool.en.json, German → pool.de.json.
{ "version": 1, "questions": [ { …question… }, … ] }
Each question has exactly these fields:
{
  "id": "<prefix>-001",
  "difficulty": <whole number>,
  "subcategory": "<a subcategory slug EXACTLY as in categories.json, the same in EVERY pool file>",
  "description": "<one funny sentence shown before the question>",
  "question": "<the question>",
  "answer": "<the correct answer>",
  "wrong_answers": ["<wrong>", "<wrong>", "<wrong>"],
  "hints": ["<vague>", "<stronger>", "<strong>"],
  "fun_fact": "<one short true sentence shown after the answer>"
}
- ids: "<prefix>-001", "<prefix>-002", … in order, unique; lowercase a-z, 0-9 and "-" only.
- Translations: the same question in another language has the SAME id, difficulty and subcategory; everything else is translated naturally (not word for word). Write the whole pool in the main language first, then the same questions in each other language.
- No "media", no "status", no other fields. No pictures: the player adds them later by hand.
- Valid JSON only: double quotes, no comments, no trailing commas.

STEP 3: THE RULES FOR GOOD QUESTIONS
Format:
- Exactly one correct answer and exactly 3 wrong answers; the game shuffles them.
- All four options have the same form and similar length (all names, all numbers, all years). The correct one must not stand out.
- Wrong answers are believable for the players but clearly wrong once you know the answer. Never an option that is arguably also correct.
- Exactly 3 hints, from vague to strong. The third may nearly give it away but must not contain the answer.
Use the options honestly:
- Superlatives and comparisons are about the real world: "What is the longest dinosaur ever found?", never "Which of these is the longest?".
- The clue must point to the answer in the real world, not just among the four options. Ask yourself: "What else in the world fits this clue?" If anything does, find a clue only the answer has.
Keep it short:
- The question is read aloud; it fits in one breath: one or two short sentences, ideally under 120 characters.
- No invented stories ("Your uncle tells you…", "Imagine that…").
- Don't repeat in the question what the hints or the fun fact say.
No giveaways:
- Neither the description, the question nor hints 1 and 2 may give the answer away or rule options out. Don't name things that make the question trivial.
Description:
- One full, humorous sentence that relates to the question, can be absurd, and never reveals the answer. Examples: coffee → "Parents don't work in the morning until you fill them up with this fuel."; Saturn → "A planet that never takes off its jewellery."
Tone:
- Family-friendly for every age. Light and playful. Nothing scary, gory or adult-only; never ask about deaths, violence or suffering, and no mockery.
Difficulty: a shared scale 1–15 that means WHO CAN ANSWER IT, not how obscure the fact is:
- 1 = a 6-year-old can answer it
- 3 = a 9-year-old
- 5 = an 11-year-old
- 7 = a 13-year-old
- 10 = a 16-year-old with good school knowledge
- 12 = most adults
- 14 = a well-read adult, or someone who studied the field
- 15 = trivia specialists, glad to have been asked
- Things children meet in cartoons, films, games and everyday life are easier than they look (Saturn's rings: 2; who reached America in 1492: 2). School knowledge (names of prizes, years, theory) is harder than it looks.
- Hard means fewer people know it; never a fact nobody could know or work out (an exact minor count, an obscure date).
- Rate honestly: a question most adults answer is a 12, even if kids would miss it.
- Spread the questions EVENLY over every level of the audience's window: e.g. kids, 20 questions → about 3–4 at each of 1, 2, 3, 4, 5, 6. Every level of the window gets at least one question.
Facts:
- You may not have web search; assume you don't. Use only facts you are sure of. If you are not sure, drop the question and write a different one; never guess.
- No exact numbers, dates or measurements you can't vouch for; prefer facts that are widely known and stable. Avoid things that change (current records, "the newest…", ages of living people).

STEP 4: BIG SETS IN PARTS
- If I asked for more than 20 questions, write them in parts of 20: first the files a)–d) and the main-language pool with questions 001–020, then the same 20 in each other language. Then stop and say: "Say 'next' for the next 20."
- In each later part write only the new questions (ids continue: 021, 022, …), per language, as a list for me to add to the end of the "questions" array of each pool file.
- When all questions are written, say so, and show a table: difficulty → number of questions.

When done, remind me to check the folder with: trivia --check-mod <folder>
````
