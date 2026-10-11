# Task: find long-winded questions

You get question texts from the pool of the trivia game described above, with their id and clue form. Find every one that breaks house style "Keep it short":
- it is long-winded: more than one or two short sentences, or context that isn't needed to answer;
- it is wrapped in an invented story: a relative, friend, guide or influencer telling or asking you something ("Tu tío…", "Tu prima te reta…"), "Imagina que…", a backstory, or a situation that isn't part of the clue.

A short setting that is the clue itself is fine ("Estás en la cocina y el agua hierve…"). Don't flag a question only because it is a bit dry or could be worded better.

For each one you flag, give `issue`: an English instruction for the reviser, naming what to cut or shorten and what must stay (the clue that makes the answer unique). Leave every other question out.
