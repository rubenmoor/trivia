# Task: draft questions

Write questions for one subcategory of the trivia game described above. You get the subcategory, its broad category, the question axes, and a list of slots. Each slot has:
- a `concept` (and its facet): what the question is about;
- a `target_difficulty`;
- up to three numbered `options`: combinations of the question axes (move, stimulus, clue, answer_kind, lens);
- `already_asked`: every question the pool already has about this concept.

For each slot, choose the option that makes the best question about the concept, and write one question with exactly that option's move, stimulus, clue form, answer kind and lens. Put the option's number in `option`. Aim for the target difficulty (±1 is acceptable if it makes a clearly better question; report the difficulty you actually think it is).

Rules:
- Follow the house style exactly.
- The concept is central to the question: it is the answer, or the thing the question asks about.
- **Ask a different fact than every question in `already_asked`.** The new question must not be answerable from an earlier one, and must not give one away. The answer may be the same concept, if the fact asked is clearly different.
- Don't repeat any fact listed under "Already in the pool"; it covers the whole subcategory.
- Questions in one batch must not overlap each other.
- **Skipping is allowed and encouraged** when a slot would produce a forced, boring, ambiguous or uncertain question. No question is better than a filler question. Put skipped slots in `skipped` with a short reason and `retire`:
  - `"used_up"`: every good question about this concept for these players has already been asked;
  - `"unaskable"`: this concept can't give a good question for this family (too obscure, too adult, not something to ask as multiple choice);
  - `"no"`: anything else (e.g. none of the three options fits the concept).
- `stimulus` other than `none` means the media is part of the question: `media.role` is "essential", `needs_media` is true, and `media.note` says exactly what must be shown or played. `photo`, `detail`, `silhouette` and `map_outline` are images, `sound` is audio, `video` is video. With `stimulus` `none`, the media is illustrative or decorative and `needs_media` is false.
- Set `needs_fact_check` to true if the question, answer, hints or fun fact contain a number, date, record, superlative ("el más grande") or any fact that could be wrong.
- `bundle`: the one bundle whose rule fits the question (listed under "Bundles"). Judge by what a player needs to know to answer, not by the topic; when in doubt, `base`.
- `background_query`: only for audio questions: an English Commons search term for a generic, decorative background image shown while the sound plays (e.g. "misty forest" for a bird call). It must not show the answer. Empty string for all other questions.
