# Task: sort questions into bundles

A bundle is a set of questions that players switch on or off before a session. Every question is in exactly one bundle. Bundles add questions; they don't own a topic: a sports question can be in `base`, and a well-known fact about a country stays in `base`.

You get the bundles with their rules and a list of questions. For every question, pick the one bundle whose rule fits it. When in doubt, choose `base`.

Judge by what a player needs to know to answer, not by the topic: "¿Cuál es la capital de Colombia?" is `base` (everyone knows it); a question about a Colombian dish, festival, river or saying that people outside Colombia mostly don't know is `colombia`. Take the question, its options and its hints together.

`reason`: one short English sentence, only needed when the bundle isn't `base` (empty string otherwise).
