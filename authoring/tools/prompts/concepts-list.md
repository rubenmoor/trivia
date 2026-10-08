# Task: concept list

You write the concept list of one subcategory of the trivia game described above. Questions are later written from these concepts, one concept per question. You get the subcategory, its facets, the question axes, and the questions already in the pool for this subcategory.

## 1. Concepts
For every facet, list 15–25 **concepts**:
- A concept is a bare Spanish name: a thing, animal, plant, person, character, place, event, object, custom or term ("Saturno", "Eclipse solar", "Neil Armstrong", "Telescopio"). **No facts, descriptions or question ideas.**
- Concrete and specific: "Saturno", not "Planetas grandes".
- Something a Colombian family with kids aged 6–16 could be asked about. Include both well-known and less-known concepts, but nothing only an expert knows.
- No duplicates or near-duplicates in the list: no synonyms, nicknames, singular/plural pairs or a concept and a part of it under another name.
- Each concept belongs to exactly one facet, spelled exactly as given.

`familiarity` (1–5): how well kids aged 11–12 in a Colombian family know the concept. 5 = every kid knows it; 3 = kids have heard of it; 1 = only a keen 16-year-old knows it. Use the calibration in the house style: kids know more from everyday life, films and games, and less from school theory, than adults expect.

## 2. Existing questions
For every existing question, give:
- `concept`: the main thing the question is about (usually its answer, or the subject it asks about). Use a concept from your list; if none fits, add one to the list in the best facet.
- `axes`: one value for each axis that describes the question best, from the values given. Pick the closest value even if none fits perfectly. `stimulus` is `none` unless the question needs its media (a photo, sound or video that is part of the question).

Return every existing question, by its `id`.
