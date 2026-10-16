# Task: propose a regional bundle's taxonomy

A regional bundle is a pack of trivia questions for families with a connection to one region: they live there, come from there or have family there. Its questions need that connection to answer (the bundle's rule below). Everything families anywhere in the world answer without it, whatever their language, stays in `base`, the main pool (its subcategories are listed below).

You propose the bundle's broad categories and their subcategories. Drafting later picks concepts per subcategory (150–250 each) and writes questions about them, at every difficulty from 1 to 15, in the bundle's language, {language}, and its voice (under "Bundle").

## Keys and names
Every category and every subcategory has:
- `slug`: its key in code and files, never shown to players: English, lowercase ASCII words joined by dashes (`food-and-drink`, `rivers-and-lakes`); unique within the bundle among categories and among subcategories (a category and a subcategory may share one). No region in it, the bundle already says it: `history`, not `history-of-germany`. An existing category or subcategory (under "Existing taxonomy") whose topic stays the same keeps its slug.
- `en`: the English name players see, short, sentence case, as on a game's category screen ("Rivers of Colombia", "Colombian sweets"); for an English bundle in its voice ("Colours of …" for a British one).
- `name`: the name in {language} the region's players see, in the bundle's voice («Ríos de Colombia», „Flüsse Deutschlands“); for an English bundle the same as `en`.

Names in the game's other languages are made from `en` later. `region`: the region's name in English.

## Steps
1. **General list.** Start from the general category list for regional bundles. Take a general category's `slug` as it is and fill `{region}` in its English `name` with the region's English name, worded as English needs it ("Food and drink of Germany" or "German food and drink"); its `name` in {language} says the same. Keep a general category unless the region has too little to ask in it; a left-out one goes into `left_out` (its English name) with the reason.
2. **Region's own categories.** Add categories the region needs and the general list lacks: a topic its families talk about that no general category holds without crowding it out. Each with a `reason`. None is fine.
3. **Subcategories.** For every category, its subcategories. Size them for the target: about {per_sub} approved questions per subcategory, so about {subs} subcategories in total; more where a category has more to ask, at least 2 per category. A subcategory must hold 150 concepts the region's families know at some level; narrower topics go into a wider neighbour.

## Each subcategory
- `slug`, `en`, `name`: as above; `en` and `name` unique within the bundle (they may repeat a `base` name only if the region's angle is clear from the name: "Rivers of Colombia", not "Rivers").
- `scope`: one English line: what belongs in it, so two neighbours don't overlap.
- `reason`: one English sentence: why the region needs it, what it adds next to its neighbours.
- `samples`: about 10 concepts from easy to hard, each with `known_at`, named in {language} as the region's families say them.

`known_at` (1–15): the lowest point on the difficulty scale at which the region's families know the concept: 1 = a 6-year-old there knows it, 5 = an 11-year-old, 10 = a 16-year-old with good school knowledge, 12 = most adults there, 15 = trivia specialists. Judge people of the region, not outsiders. Spread the samples: a subcategory with only hard concepts or only easy ones is a bad split.

## Rules
- The bundle's rule decides: no subcategory whose questions players without the connection answer as well (world facts, the country's capital, its most famous names known worldwide).
- Neighbours don't overlap: a concept belongs to exactly one subcategory. Say in the scope where a borderline topic goes.
- Mix across the families' ages: something for children (animals, sweets, festivals, cartoons, games) as well as for adults (history, politics of the past, how people speak).
- No current party politics, no armed conflict as entertainment, no crime figures as celebrities.
- The existing taxonomy is shown for context only: reuse a slug and name where it fits, drop or split it where it doesn't; your proposal stands on its own.
- `scope` and `reason`: English.
