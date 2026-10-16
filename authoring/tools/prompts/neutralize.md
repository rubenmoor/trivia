# Task: find wording that isn't neutral Spanish

You get Spanish questions from the `base` bundle of the trivia game described above, with their id: description, question, answer, wrong answers, hints and fun fact. `base` in `es` is played anywhere in Latin America, so its voice is idiomatic Latin American Spanish (house style "Language"); Spain has its own `es-ES` text. Find every question whose wording, in any of these fields, uses Colombian or other one-country usage where a word common across Latin America exists:
- one-country words: "crispetas" → "palomitas", "gripa" → "gripe", "tinto" → "café", "computador" → "computadora";
- Spain-only words: "ordenador" → "computadora", "zumo" → "jugo", "patata" → "papa";
- brands as generic words: "cinta Scotch" → "cinta adhesiva";
- regional diminutives and slang: "pelotica" → "pelota", "parcero";
- "vos" or "vosotros" forms → "tú";
- numbers with a dot as thousands separator: "2.640" → "2640", "42.195" → "42 195".

Don't flag:
- names, titles and references anyone knows (Encanto, García Márquez, "Cien años de soledad"), and a regional word that is itself the answer or the clue (a question about what "tinto" means in Colombia);
- Colombian content: a question that needs a connection to Colombia belongs in the `colombia` bundle (D-49), which is not this task;
- Latin American words that Spain says differently ("carro", "celular", "computadora", "jugo"): they are right for `es`;
- words with no form shared across Latin America ("carro"/"auto", "piscina"/"alberca"/"pileta") when no natural rewording exists; list them in `no_neutral_form` instead.

For each question you flag, give `issue`: an English instruction for the reviser naming every field, word and replacement ("description: 'bombillo' → 'bombilla'; hint 2: 'crispetas' → 'palomitas'"), keeping everything else as it is. Leave every other question out.
