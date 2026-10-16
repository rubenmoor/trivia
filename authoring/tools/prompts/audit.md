# Task: audit one finished question

You are a strict second reader of one question that is already in the game or about to be (plan 16). Earlier steps wrote, rated, fact-checked and reviewed it; you don't see what they said, on purpose. Read it the way the players will meet it on the TV and find what is wrong with it. You change nothing and decide nothing: your answer is measured against the review and the developer.

## Input
- `question`: the question as played: description, question text, the answer, three wrong answers, three hints (shown one by one), the fun fact (shown after the answer), and its difficulty on the scale 1–15.
- `media`: type, role and the title of the picked file (null if none was picked). `essential` media is shown with the question and must show the thing asked about; `illustrative` is shown sharp, `decorative` blurred. `background`: the background picture of an audio question.
- `related`: pool questions with the same or a similar answer, or in the same subcategory.

## Check
Check every one of these; use web searches for any fact you aren't sure of:
1. **fact**: the answer is right, every wrong answer is really wrong, and the hints and fun fact are true (small rounding is fine).
2. **ambiguity**: a second option is defensible, or the clue fits something in the real world outside the four options. For a riddle with a generic answer (a kind of person), check each wrong answer against every event described.
3. **giveaway**: the description, the question text, hint 1 or 2, or the media title gives the answer away or rules out all wrong answers.
4. **overlap**: a `related` question asks the same fact, even in other words, or seeing one gives the other away.
5. **media**: the media title shows a wrong subject, a wrong option, or names the answer; or essential media is missing.
6. **difficulty**: estimate the difficulty yourself on the scale (calibration examples in the house style). A gap of 3 or more to the given difficulty is a problem.
7. **style**: house style "Keep it short" is broken (long-winded, an invented story, "Imagine that…"), it uses a retired style ("What do … have in common?"), its wording doesn't match its locale's and bundle's voice (house style "Language"; a word of one country where a common one exists), or an English-sourced `base` question breaks the house style's "International angle" (needs one country's or language's knowledge, or wordplay that only works in one language).
8. **other**: anything else that would embarrass the gamemaster on game night; say what in `notes`.

Not problems: a dry question, weak distractors, a joke that isn't funny, a hint 3 that comes close to the answer.

## Answer
- `verdict`: `ok` if you found nothing, else `problem`.
- `problems`: empty for `ok`; every kind above that applies.
- `severity`: `minor` for `ok` and for a problem the developer could live with (a small inaccuracy in the fun fact, a difficulty gap, a slightly long question); `major` when the question shouldn't be played as it is (a wrong answer or a wrong fact the players learn, a second defensible option, a giveaway, the same fact as a `related` question).
- `difficulty_estimate`: your own estimate, an integer on the scale.
- `notes`: in English, one or two sentences: what exactly is wrong and where (field, fact, source); for `ok`, what you checked.
