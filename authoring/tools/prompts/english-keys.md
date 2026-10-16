You translate the answers and concepts of trivia questions into English, for a duplicate check against English questions (decision 232). Nobody plays these strings; they only have to match how an English question would name the same thing.

For each item, return its `id`, `answer` and `concept` in English:

- The usual English name: «Saturno» → "Saturn", «Cien años de soledad» → "One Hundred Years of Solitude", «el ornitorrinco» → "platypus", «Revolución Francesa» → "French Revolution".
- Names of people, places and works as English sources write them; keep a name that has no English form as it is.
- Short: the name only, no articles, no explanations. Numbers, dates and codes unchanged.
- An empty `concept` stays empty.
- Every item once, the same `id`.
