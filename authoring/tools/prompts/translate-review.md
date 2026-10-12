# Translation runs

The question above is a translation of an approved Spanish question. You see the Spanish one as `source`, and the translator's `notes`. The source was reviewed already: judge the translation, as the players will meet it. Everything above applies to the translation, with these changes.

## Changes
- **Voice:** "Language" means the section above for this locale, not Spanish. Report wording that isn't natural for its players (a literal idiom, translationese, the wrong spelling or unit convention) as `style`.
- **Media:** the media is the source's picked file; there are no candidates and no new search. Leave `pick`, `background_pick` and `new_query` null. Text in the media, in any language, is never a problem.
- **Language of your answer:** `feedback`, `fix` and `notes` in English.
- **The source stays as it is.** A `fix` changes only the translation. If the source itself is wrong, report `fact` and say "source:" in your feedback or notes; leave `fix` empty.

## Check on top
- **Fidelity:** the translation asks the same fact with the same answer as the source. A changed fact, number or answer is `fact`; a lost detail that made the clue unique, or an added one that gives it away, is `ambiguity` or `giveaway`.
- **Options:** a wrong answer that became correct or a synonym of the answer is `ambiguity`; one that stands out by grammar (an article, a gender, a case ending) or is absurd enough to rule itself out is `giveaway`.
- **Hints:** a hint that still plays on the Spanish word, or names the answer in the target language before hint 3, is `giveaway`.
- **Description:** a literal joke that makes no sense is `style`; one that gives the answer away is `giveaway`.

## Not travelling
An item without a translation comes with the translator's `reason` (`wordplay`, `about_spanish`, `needs_local_knowledge`, `other`). Decide in one line:
- `approved`: right, it doesn't travel; it stays in Spanish only.
- `needs_work`: it can be translated; `feedback` says how in one line. It is translated in the next run.
