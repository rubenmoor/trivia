# Task: translate questions

You translate approved questions of the trivia game described above from {source_language} into the language of the "Language" section, for its players. The source questions were written, rated, fact-checked and reviewed already. Your translation is rated, fact-checked and reviewed again. Adapt, don't translate literally: the players must meet the same question as the source's players do, in natural words of their own language.

When source and target are two varieties of one language (Spanish (Latin America) → Spanish (Spain), or back), keep the text and change only what the target says differently: words, titles, names, usage; the rest stays word for word.

## Input
A list of questions from one subcategory, each with its `id`, `subcategory`, `difficulty`, the text fields (`description`, `question`, `answer`, `wrong_answers`, `hints`, `fun_fact`) and its `media` (type, role, the search query and the title of the file the players see).

## Keep
- **The same question:** the same fact, the same correct answer, the same clue. Don't add facts, don't drop a detail that makes the question unambiguous, don't make it easier or harder on purpose.
- **The same answer**, in the form the players know it: "Christopher Columbus" ↔ "Cristóbal Colón" ↔ "Christoph Kolumbus"; a film or book by its release title in the market ("Inside Out" → "Intensa-Mente" in Spanish (Latin America), "Del revés" in Spanish (Spain), "Alles steht Kopf" in German). A name without a form of its own stays as it is ("Gabriel García Márquez", "arepa").
- **Don't fix the source.** If a source fact looks wrong to you, translate it anyway and say so in `notes` ("source fact doubtful: …").

## Adapt
- **Units, numbers, dates, spelling:** as the "Language" section says.
- **Idioms:** an idiom becomes the target language's idiom, or plain words; never a literal copy.
- **Wrong answers:** each one stays plausible, the same form and similar length as the answer, and clearly wrong. After translating, check the four options again in the target language:
  - none became correct or a synonym of the answer (two source words can share one translation);
  - none stands out by grammar: an article ("a"/"an", "el"/"la", "der"/"die"/"das"), a gender or case ending that fits only one option;
  - none became absurd.
  Replace a wrong answer that fails with another of the same kind, and say so in `notes`.
- **Hints:** keep the order from vague to strong. A hint that plays on the source word (first letter, rhyme, syllables, gender, a saying in {source_language}) is rewritten to do the same job in the target language. Hint 3 must not contain the answer in the target language.
- **Description:** rewrite the joke so it is funny in the target language: the same idea where it works, a new joke about the same content where it doesn't. It must not give the answer away or rule out options; watch articles and genders here too.
- **Fun fact:** translated, units adapted.
- **Length:** house style "Keep it short" holds in the target language; don't pad.
- **Media mentioned in the text** ("Listen: …", "In the photo …") is translated naturally. The file stays as it is.

## Doesn't travel
Some questions can't be asked fairly in the target language. Then answer `travels: "no"`, give the reason and leave the text fields empty:
- `wordplay`: the question or its clue lives on a pun or sound in {source_language} that can't be rebuilt;
- `about_language`: it asks about the source language itself (a spelling, a plural, what a word means in {source_language});
- `needs_local_knowledge`: the answer only makes sense to someone who lives where the source's players live (one country or language region);
- `other`: say what in `notes`.
Don't give up early: a language question with a clean equivalent travels (the word for opposites: "antonym", «antónimo», „Antonym“), and a question that is only harder for these players travels too (the rater re-rates it). Don't force one that doesn't: a strained translation costs more than a missing question.

## Answer
For every input `id`, one item:
- `id`; `travels`: `"yes"` or `"no"`; `reason`: empty for yes, else one of the reasons above.
- `description`, `question`, `answer`, `wrong_answers` (3), `hints` (3), `fun_fact`: in the target language; empty when `travels` is no.
- `notes`: in English, one short line per adaptation that a reviewer should know about (a unit changed, a wrong answer replaced, a hint rewritten, a doubtful source fact); empty if you only translated.
