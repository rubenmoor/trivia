# Task: concept list

You write the concept list of one subcategory of the trivia game described above. Questions are later written from these concepts, one concept per question. You get the subcategory, its facets, the question axes, and the questions already in the pool for this subcategory.

## 1. Concepts
For every facet, list 15–25 **concepts**:
- A concept is a bare name in the language of the content (house style, "Language"): a thing, animal, plant, person, character, place, event, object, custom or term (in English: "Saturn", "Solar eclipse", "Neil Armstrong", "Telescope"). **No facts, descriptions or question ideas.**
- Concrete and specific: "Saturno", not "Planetas grandes".
- Something players of some age group, from kids to adults, could be asked about in a family-friendly game. Cover the whole range: what every child knows, what teens and students know, and what well-read adults know. Nothing only a specialist knows.
- Follows the bundle (under "Bundle"). For `base`, the house style's "International angle": spread the concepts of every facet across the world's regions (Africa, Asia, Europe, the Americas, Oceania) as far as the facet allows; no Spanish-speaking-world focus, no Anglo/US default; a concept known only to one country's players belongs to that country's regional bundle, not here.
- Fame comes first: a concept families know beats a balanced map; never add an obscure concept only to cover a region.
- No duplicates or near-duplicates in the list: no synonyms, nicknames, singular/plural pairs or a concept and a part of it under another name.
- Each concept belongs to exactly one facet, spelled exactly as given.

`known_at` (1–15): the lowest point on the shared difficulty scale (house style) at which people know the concept: 1 = a 6-year-old knows it (the Sun), 5 = an 11-year-old, 10 = a 16-year-old with good school knowledge, 12 = most adults, 15 = trivia specialists. For `base`, judge families anywhere, not one country's: a national hero known at 3 at home may be 13 abroad. Use the calibration in the house style: people know more from everyday life, films and games, and less from school theory, than expected.

## 2. Existing questions
For every existing question, give:
- `concept`: the main thing the question is about (usually its answer, or the subject it asks about). Use a concept from your list; if none fits, add one to the list in the best facet.
- `axes`: one value for each axis that describes the question best, from the values given. Pick the closest value even if none fits perfectly. `stimulus` is `none` unless the question needs its media (a photo, sound or video that is part of the question).

Return every existing question, by its `id`.
