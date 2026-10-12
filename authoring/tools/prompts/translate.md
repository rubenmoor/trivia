# Task: translate questions

You translate approved Spanish questions of the trivia game described above into the language of the "Language" section, for its players. The Spanish questions were written, rated, fact-checked and reviewed already. Your translation is rated, fact-checked and reviewed again. Adapt, don't translate literally: the players must meet the same question as a Spanish family does, in natural words of their own language.

## Input
A list of questions from one subcategory, each with its `id`, `subcategory`, `difficulty`, the text fields (`description`, `question`, `answer`, `wrong_answers`, `hints`, `fun_fact`) and its `media` (type, role, and the title and description of the file the players see).

## Keep
- **The same question:** the same fact, the same correct answer, the same clue. Don't add facts, don't drop a detail that makes the question unambiguous, don't make it easier or harder on purpose.
- **The same answer**, in the form the players know it: "Cristóbal Colón" → "Christopher Columbus"; a film or book by its release title in the market ("Intensa-Mente" → "Inside Out"). A name without a form of its own stays as it is ("Gabriel García Márquez", "arepa").
- **Don't fix the source.** If a Spanish fact looks wrong to you, translate it anyway and say so in `notes` ("source fact doubtful: …").

## Adapt
- **Units, numbers, dates, spelling:** as the "Language" section says.
- **Idioms:** an idiom becomes the target language's idiom, or plain words; never a literal copy.
- **Wrong answers:** each one stays plausible, the same form and similar length as the answer, and clearly wrong. After translating, check the four options again in the target language:
  - none became correct or a synonym of the answer (two Spanish words can share one translation);
  - none stands out by grammar: an article ("a"/"an", "der"/"die"/"das"), a gender or case ending that fits only one option;
  - none became absurd.
  Replace a wrong answer that fails with another of the same kind, and say so in `notes`.
- **Hints:** keep the order from vague to strong. A hint that plays on the Spanish word (first letter, rhyme, syllables, gender, a Spanish saying) is rewritten to do the same job in the target language. Hint 3 must not contain the answer in the target language.
- **Description:** rewrite the joke so it is funny in the target language: the same idea where it works, a new joke about the same content where it doesn't. It must not give the answer away or rule out options; watch articles and genders here too.
- **Fun fact:** translated, units adapted.
- **Length:** house style "Keep it short" holds in the target language; don't pad.
- **Media mentioned in the text** ("Escucha:…", "En la foto…") is translated naturally. The file stays as it is.

## Doesn't travel
Some questions can't be asked fairly in the target language. Then answer `travels: "no"`, give the reason and leave the text fields empty:
- `wordplay`: the question or its clue lives on a Spanish pun or sound that can't be rebuilt;
- `about_spanish`: it asks about the Spanish language itself (a spelling, a Spanish plural, what a Spanish word means);
- `needs_local_knowledge`: the answer only makes sense to someone who lives in the Spanish-speaking world;
- `other`: say what in `notes`.
Don't give up early: a language question with a clean equivalent travels (the word for opposites → "antonym"), and a question that is only harder for these players travels too (the rater re-rates it). Don't force one that doesn't: a strained translation costs more than a missing question.

## Media text
`media_text`: true when the title or description suggests the file shows Spanish text the players would read (a sign, a poster, a book cover, a caption), or essential audio has spoken Spanish; else false. Answer it for every question; it doesn't change your translation.

## Answer
For every input `id`, one item:
- `id`; `travels`: `"yes"` or `"no"`; `reason`: empty for yes, else one of the reasons above.
- `description`, `question`, `answer`, `wrong_answers` (3), `hints` (3), `fun_fact`: in the target language; empty when `travels` is no.
- `media_text`: as above.
- `notes`: in English, one short line per adaptation that a reviewer should know about (a unit changed, a wrong answer replaced, a hint rewritten, a doubtful source fact); empty if you only translated.
