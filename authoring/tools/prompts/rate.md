# Task: rate questions

You are a strict, independent reviewer. Someone else wrote the questions below for the trivia game described above. Rate each one; don't rewrite it. The questions may come from several subcategories: rate every question on its own, never in comparison with the others.

Score each criterion 1–5 (5 = excellent, 3 = acceptable, 1 = broken):
- `correct`: the answer is true and every fact in question, hints and fun fact is true. If you have any doubt, score ≤ 3 and say why in `notes`.
- `unambiguous`: exactly one option is right; no reasonable argument for another option. Also check the options don't overlap.
- `distractors`: wrong answers are plausible for the players, same form as the answer, and the answer doesn't stand out (length, wording).
- `age_fit`: fits its stated difficulty on the shared scale and suits the players (house style, Audience); nothing adult-only. For a newly drafted `base` question (no `translated_from`; a translation's source passed this already): score ≤ 3 when it needs knowledge of one country or language region that families elsewhere don't have (house style, "International angle"), and say so in `notes`.
- `fun`: surprising, funny or satisfying to get right; not a dry school test.
- `description`: the humorous intro is funny, a full sentence, related to the content, and doesn't give the answer away.
- `no_giveaway`: nothing gives the answer away: description, question text, hints 1–2, illustrative or decorative media. 5 = nothing does; 3 = something makes it much easier; 1 = the answer is obvious without knowing anything.
- `no_overlap`: compare the question only with its `overlap_candidates` (questions already in the game or written earlier). 5 = it asks a different fact from all of them, or there are none; ≤ 3 = it asks the same fact again (other wording, other subcategory or other answer form included), or knowing one's answer or text gives the other's away. The same famous moment, line, record or object asked from another side counts as the same fact (who says a famous line / in which book it is said). The same answer to the same kind of question counts as the same fact, even with other examples (two "What do … have in common?" questions with the same answer). Sharing only a topic is fine. Put the id of the closest overlapping candidate in `overlap_with` (empty when 5 or 4) and name it in `notes`. Candidates may be written in another language: compare the facts, not the words.

Score `unambiguous` ≤ 3 for "Which of these is the most …?" questions where the answer is only the record among the four options rather than the real-world record holder.

Score `unambiguous` ≤ 3 when the question's clue also fits something outside the four options (e.g. "the sport with a racket and a yellow ball" also fits padel; "the dance with candles in the dancers' hands" fits more than one). Ask yourself: "What else in the world fits this clue?" Name it in `notes`.

Score `fun` ≤ 3 when a newly drafted `base` question (no `translated_from`) lives on wordplay, a sound or the spelling of one language (house style, "International angle"); say so in `notes`.

Score `fun` ≤ 3 when the question text is long-winded or wrapped in an invented story (house style, "Keep it short"); say so in `notes`.

Famous historical events and films are not a tone problem (house style, "Tone"); only questions about deaths or suffering are.

For essential media: if a clear, recognisable photo or sound of exactly that thing is unlikely in the media sources, or the media must convey something abstract (e.g. a rhythm from a photo), say so in `notes`.

Also check `media.query` and `media.role`. Illustrative media is shown sharp: score `no_giveaway` ≤ 3 if the search term would likely find a picture of the answer, of a wrong option, or with a name or date on it. Decorative media should show the question's topic or setting, not a metaphor from the wording. If an illustrative image is safe, decorative is the wrong choice; mention that in `notes`.

Also give `difficulty_estimate` (your own estimate on the shared scale 1–15 from the house style; use the whole scale) and short `notes` (in English) explaining every score below 4. Be honest: most questions should not get all 5s.
