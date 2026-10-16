// Example code add-on (MIT): one more hint joker per game.
// The game imports this file and calls setup() once, before the game shows.

const RULE = {
  es: "Con este mod: un Soplo más por partida.",
  "es-ES": "Con este mod: un Soplo más por partida.",
  en: "With this mod: one extra Hint per game.",
  de: "Mit diesem Mod: ein Wink mehr pro Spiel.",
};

export default async function setup(trivia) {
  // Before every action: on "new", raise the hint budget by one.
  // No budget sent: 3 in solo, unlimited (null) in gamemaster mode. The engine still checks the body.
  trivia.actions.before((action, body) => {
    if (action !== "new") return;
    const jokers = body.jokers ?? {};
    const hint = "hint" in jokers ? jokers.hint : body.mode === "solo" ? 3 : null;
    if (hint === null) return;
    body.jokers = { ...jokers, hint: Math.min(hint + 1, 99) };
  });

  // The hint card's rule line, per UI language; other keys stay ours.
  for (const [locale, rule] of Object.entries(RULE)) {
    trivia.i18n.add(locale, { joker: { hint: { rule } } });
  }

  // Events get copies: read them, changing them does nothing.
  trivia.on("game:end", ({ game, result }) => {
    console.log(`[${trivia.mod.id}] game ${result} at level ${game.level}`);
  });
}
