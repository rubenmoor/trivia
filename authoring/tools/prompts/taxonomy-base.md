# Task: propose the taxonomy of a further base bundle

`base` is the main pool of a family trivia game: general knowledge as a Latin American or European family knows it. A further base bundle is a second main pool for families of another culture (the bundle's rule and voice below). It is a full pool of its own, the same size as `base`, with broad categories and subcategories. It is built in two steps: (1) the questions of `base` that fit the culture are copied into it, each onto one of its subcategories; (2) new questions about the culture, which `base` never asks, fill the rest up to the target. Your taxonomy serves both steps.

You propose the bundle's categories and subcategories, a map from every `base` subcategory to one of them (or to none), and say where the gap is. Drafting later picks concepts per subcategory and writes questions at every difficulty from 1 to 15, in English first, then translated into the bundle's other languages.

## Keys and names
Every category and every subcategory has:
- `slug`: its key in code and files, never shown to players: English, lowercase ASCII words joined by dashes (`tang-poems`, `solar-terms`); unique within the bundle among categories and among subcategories (a category and a subcategory may share one). A subcategory that is `reused` has exactly a `base` slug.
- `en`: the English name players see, short, sentence case ("Tang poems", "Solar terms").
- `name`: the same as `en` (the bundle's names in its other languages are made from `en` later).

## Subject
Every category belongs to exactly one school-style subject of the career (a fixed list, never extended): `subject` is its id, `subject_reason` one English sentence why. Pick by what the category is about, as a school would file it:
{subjects}

## Steps
1. **Read the research notes** (if given): what the culture's children learn at school and what its families share beyond it. Notes mark each topic with its subject, `known_at` range and a status: `in` is free, `facts` only as bare undisputed facts, `out` is left out of the taxonomy entirely. The bundle's rule rules over the notes.
2. **Reuse.** Go through `base`'s subcategories. A subcategory whose questions are mostly on topic for this culture (animals, the human body, space, mathematics, world food seen from this side) becomes a `reused` subcategory: same slug as in `base`, own `scope` and own `en`/`name`. A reused subcategory's scope says what its copies hold, and where new questions go beside them.
3. **New.** Add what a family of this culture knows and `base` doesn't ask: school subjects and their canon, language, literature, history, festivals, food, places, legends, sport, media, daily life. Group the whole into broad categories as a family sees them, each with `origin` (`reused` when mostly made of reused subcategories, else `new`), `scope` and `reason`.
4. **Size.** About {per_sub} approved questions per subcategory, so about {subs} subcategories in total. A subcategory must hold 150 concepts that families of the culture know at some level; narrower topics go into a wider neighbour.
5. **Map.** `from_base`: every `base` subcategory exactly once: `to` the slug of the subcategory its fitting questions go to (usually the same slug when `reused`, else a `new` or other one), or `null` when its questions mostly don't fit, with a `reason`: `euro_centric` (European or Western history, places, figures, culture), `latam_centric` (Latin American topics), `wordplay` (questions that live on the source language's wording), `sensitivity` (against the bundle's rule). For a mapped one `reason` is empty. `expected_keep` is your estimate (0 to 1) of the share of `base`'s approved questions the copy step keeps in all.

## Each subcategory
- `slug`, `en`, `name`, `origin` (`reused` or `new`), as above.
- `scope`: one English line: what belongs in it, so neighbours don't overlap; for a `reused` one, also where copies end and new questions start.
- `reason`: one English sentence: why the bundle needs it.
- `related`: slugs of the bundle's own subcategories that border it (new drafting keeps away from their questions); empty when none.
- `language`: true for a language topic: idioms, characters, poems, sayings, wordplay. Such questions are drafted in English and translated, and a question that is fair in English may give its answer away in the other language. Its scope says: ask the origin, the author, the place or season, never what the words themselves state.
- `samples`: for a `new` subcategory about 10 concepts from easy to hard, each with `known_at`, named in English; empty for a `reused` one.

`known_at` (1–15): the lowest point on the difficulty scale at which families of the culture know the concept: 1 = a 6-year-old knows it, 5 = an 11-year-old, 10 = a 16-year-old with good school knowledge, 12 = most adults, 15 = specialists. Spread the samples and the subcategories: something for children (rhymes, cartoons, fairy tales, school texts) as well as for adults.

## Rules
- The bundle's rule decides what is on topic and how contested subjects are handled; a topic against it is not proposed, however well known.
- A concept belongs to exactly one subcategory; the scopes say where a borderline topic goes. A `new` subcategory keeps off what copies of `base` already cover (its `reused` neighbours and `related`).
- Every category has a subject; spread subjects roughly as `base` does (its shares are listed below), or say in a `reason` why not.
- Well-known facts about any country belong in `base`, not here.
- `scope` and `reason`: English.
