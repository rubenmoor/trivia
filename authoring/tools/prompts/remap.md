# Task: move a regional bundle's questions onto its new taxonomy

A regional bundle got a new list of categories and subcategories. Its existing questions still carry old subcategory names, some of them from `base`, the main pool. Every name below is in the bundle's language; answer with names in that language too. You give every question the subcategory of the new list it fits best, and say what happens to the old concept lists.

## Questions
- For every question, `subcategory`: one name from the new list, exactly as written. Judge by what the question asks about (question, answer and hints together), not by its old subcategory's name. Use the scopes: a borderline topic goes where the scope says.
- Only when no subcategory of the new list fits at all: a new one. `subcategory`: a new name in the style of the list (unique within the bundle, the region's angle clear from the name); `category`: the existing category it goes into, exactly as written in the list, or a new category name when none fits; `scope`: one English line, what belongs in it so it doesn't overlap its neighbours. A new subcategory must be able to hold 150 concepts the region's families know; a narrower topic goes into the closest existing subcategory instead. Several questions may share one new subcategory: write its name, category and scope the same way each time.
- For a subcategory of the new list: `category` and `scope` are empty strings.
- `reason`: one short English sentence, only when the question changes subcategory (empty string otherwise).

## Old concept lists
- A concept list belongs to an old subcategory that is no longer in the list. For each, `target`: the subcategory of the new list (or a new one you introduced above) whose topic is the same, so the list's concepts all belong there; else an empty string (the list is deleted). A list whose topic is only part of a wider new subcategory may still go there when every concept of it fits; a list that would scatter over several subcategories is deleted.
- `reason`: one short English sentence.
