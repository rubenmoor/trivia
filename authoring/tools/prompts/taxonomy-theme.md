# Task: propose a topic bundle's taxonomy

A topic bundle is a pack of trivia questions for families who love one topic (the bundle's rule below): they want more of it, and deeper, than the main pool, `base`, gives them. `base` stays as it is and keeps its own questions on the topic; its subcategories are listed below with their approved question counts. The bundle adds questions, it never repeats base's: a family playing both gets new concepts, not the famous ones again.

You propose the bundle's broad categories and their subcategories. Drafting later picks concepts per subcategory (150–250 each) and writes questions about them, at every difficulty from 1 to 15, in English first, then translated for players in other languages and countries.

## Keys and names
Every category and every subcategory has:
- `slug`: its key in code and files, never shown to players: English, lowercase ASCII words joined by dashes (`olympic-history`, `bridges-and-tunnels`); unique within the bundle among categories and among subcategories (a category and a subcategory may share one). No bundle name in it: `football-tactics`, not `sports-football-tactics`. It may equal a base slug only for the same topic seen deeper; prefer a slug of its own.
- `en`: the English name players see, short, sentence case, as on a game's category screen ("Football tactics", "Bridges and tunnels").
- `name`: the same as `en`.

Names in the game's other languages are made from `en` later.

## Steps
1. **Base on the topic.** Find base's subcategories on the bundle's topic. Each is a starting point: the bundle goes beyond it (lesser-known concepts, a narrower angle, a part base only touches) without asking base's concepts again.
2. **Categories.** Group the bundle's topic into broad categories, as a fan of the topic sees it. `origin`: `base_extends` when the category mainly goes deeper into topics base already has, `new` when base has next to nothing of it. Each with a `scope` and a `reason`.
3. **Subcategories.** For every category, its subcategories. Size them for the target: about {per_sub} approved questions per subcategory, so about {subs} subcategories in total; more where a category has more to ask, at least 2 per category. A subcategory must hold 150 concepts that families who follow the topic know at some level; narrower topics go into a wider neighbour.

## Each subcategory
- `slug`, `en`, `name`: as above; `en` unique within the bundle and different from every base name (a base name only if the bundle's angle is clear from it: "Football tactics", not "Football").
- `scope`: one English line: what belongs in it, so two neighbours don't overlap, and how it differs from base's related subcategories.
- `reason`: one English sentence: why the bundle needs it, what it adds next to base and its neighbours.
- `base_related`: the slugs of base's subcategories it goes beyond (the drafter keeps away from their questions), from the list below; empty when base has nothing close.
- `samples`: about 10 concepts from easy to hard, each with `known_at`, named in English; none that base's related subcategories already ask about.

`known_at` (1–15): the lowest point on the difficulty scale at which families who follow the topic know the concept: 1 = a 6-year-old fan knows it, 5 = an 11-year-old, 10 = a 16-year-old with good school knowledge, 12 = most adult fans, 15 = trivia specialists. Spread the samples: a subcategory with only hard concepts or only easy ones is a bad split.

## Rules
- The bundle's rule decides: every subcategory is on its topic.
- Deeper, not beside: no subcategory that merely renames one of base's; where base has a subcategory, the bundle's go into what base leaves out.
- Neighbours don't overlap: a concept belongs to exactly one subcategory. Say in the scope where a borderline topic goes.
- Players are families in many countries: no subcategory only one country's families know; a country's league, team or history only where fans worldwide follow it.
- Mix across the families' ages: something for children as well as for adults.
- No current party politics, no armed conflict as entertainment, no crime figures as celebrities.
- `scope` and `reason`: English.
