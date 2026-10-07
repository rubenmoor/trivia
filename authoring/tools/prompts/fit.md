# Task: fit table

You plan questions for the trivia game described above. You get a list of subcategories and a list of question styles (sorted from best to worst fit for this game in general).

For each subcategory:
1. Score how well each question style fits this subcategory, 1–5:
   - 5 = a great, fun multiple-choice question of this style is easy to imagine for this subcategory.
   - 3 = possible, but likely ordinary.
   - 1 = forced or impossible (e.g. "playing a sound" for Matemáticas).
   Prefer styles near the top of the list when fit is equal. Media styles (picture, sound, video) only fit if suitable media is likely to exist on Wikimedia Commons or be easy to find.
2. Return only styles with score 4 or 5, best first, at most {max_styles}. Give each a one-line idea (in Spanish) of the question you have in mind.

Return every subcategory, even if no style scores 4 or more (then `styles` is empty).
