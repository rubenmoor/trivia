# Task: draft questions

Write questions for one subcategory of the trivia game described above. You get the subcategory, its broad category, and a list of slots. Each slot has a question style, a target difficulty, and an idea from planning (you may use or replace the idea).

For each slot, write one question of that style at that difficulty (±1 is acceptable if it makes a clearly better question; report the difficulty you actually think it is).

Rules:
- Follow the house style exactly.
- **Skipping is allowed and encouraged** when a slot would produce a forced, boring, ambiguous or uncertain question. No question is better than a filler question. Put skipped slots in `skipped` with a short reason.
- Avoid the answers and topics listed under "Already in the pool".
- Questions in one batch must not overlap each other.
- Set `needs_fact_check` to true if the question, answer, hints or fun fact contain a number, date, record, superlative ("el más grande") or any fact that could be wrong.
- Set `needs_media` to true if the style requires a specific picture, sound or video (then `media.role` is "essential" and `media.note` says exactly what is needed).
