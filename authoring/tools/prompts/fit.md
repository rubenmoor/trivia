# Task: judge which questions of `base` fit another audience

`base` is the main pool of a family trivia game, shown on a TV: general knowledge as a Latin American or European family knows it. The bundle `{bundle}` is a second main pool for another audience. Its rule and voice:

- Rule: {rule}
- Voice: {voice}

You read questions of `base` (in English) and decide for each whether it can be copied into `{bundle}` as it is, with a light fix, or not at all. You are not re-rating or fact-checking: earlier steps did that. You judge only whether a family of the `{bundle}` audience would find the question fair, familiar and fine to play. {players}

## Input
A list of items; per item: `id`, `subcategory` and its scope, `difficulty` (1–15), `description`, `question`, `answer`, three wrong answers, three hints, `fun_fact`, and `media` (type and the title and credit line of the picked file: what the picture or sound shows; you don't see the file). Text inside a picture or sound is never a problem (`decision 35`).

## Verdict per item
- `keep`: copy as it is. World knowledge this audience shares: science, nature, the human body, maths, world geography, global films and music, sport stars, inventions, world history taught in its schools, everyday life everywhere.
- `adapt`: fits after a light fix to the text: a unit or currency, a comparison, a Western reference in a hint or fun fact, a difficulty that moves (e.g. "6 → 8"). The fact and the answer stay, no new question is written. If the fix needs more than that, it is a `drop`.
- `drop`: does not fit. Doubt → `drop` with a note: the developer flips what is wrong.

## Drop reasons (`reason`, for `drop` only)
- `euro_centric`: needs Europe or the West: its TV, clubs, local customs, politics, national figures known only there.
- `latam_centric`: needs Latin America or Spain: its people, places, TV, football, food, customs.
- `wordplay`: lives on English or Spanish words (puns, spelling, letters, a name that only works in that language), even if it travelled.
- `sensitivity`: breaks the bundle's rule on contested topics. The rule in full: contested topics are allowed when the question states an undisputed fact (a date, a name) without judgement or status wording; maps and flags are checked case by case. This applies to the media too (a map with a disputed border, a flag): judge it from its title and credit line.
- `too_hard_here`: fair only for players raised in the West; far above its difficulty for this audience, and no difficulty change repairs it.
- `other`: anything else; say it in `note`.

## What to look at
- The whole question: description, question, every answer, hints, fun fact, media title. A single Western reference in any field makes it at least an `adapt`.
- Familiarity: would a typical family of this audience have met the thing asked about (at school, on TV, in daily life)? A famous Western person, brand or show is fine when it is famous worldwide; it is not when it is famous mainly in one Western country.
- Difficulty: keep it unless familiarity clearly moves it; then `adapt` with the new number.
- Wrong answers: they must still be plausible wrong answers for this audience; a Western-only distractor list is an `adapt` (name the replacement fields in `issue`, keep the answer).

## Answer
One JSON object per item: `id`, `verdict` (`keep`/`adapt`/`drop`), `reason` (a drop reason; `null` otherwise), `note` (one English line for the developer: why), `issue` (only for `adapt`: an instruction for the reviser naming every field and change, e.g. "hint 2: replace the Premier League club with a football club known worldwide; difficulty 6 → 8"; fact and answer stay; `null` otherwise).
