// Spanish copy for milestones and consolation (plans/04-ui-tv-display.md, UI-14). The players are
// addressed as «ustedes» (Colombian usage, D-6). {n} is the level.

/** A line on the Level screen at some levels; null at the others. */
const MILESTONES: Record<number, string[]> = {
  4: ["¡Cada vez más alto!", "¡La torre ya tiene forma!"],
  6: ["¡Ya van por la mitad!", "¡Mitad de la torre!"],
  8: ["¡Esto ya es un rascacielos!", "¡Desde aquí se ve todo el barrio!"],
  10: ["¡Ya se ve la cima!", "¡Solo quedan tres!"],
  12: ["¡Última pregunta! La corona los espera.", "¡Una más y son leyenda!"],
};

/** After a wrong answer, by how far the players got. */
const CONSOLATION: [maxLevel: number, lines: string[]][] = [
  [
    3,
    [
      "¡Llegaron al nivel {n}! Toda torre empieza con un primer bloque.",
      "Nivel {n}: el calentamiento ya está. ¡La próxima va más alto!",
      "¡Uy! Nivel {n}. Hasta los mejores se tropiezan al principio.",
    ],
  ],
  [
    6,
    [
      "¡Llegaron al nivel {n}! La torre ya se veía desde la ventana.",
      "Nivel {n}: ¡nada mal! Ya iban por la mitad del camino.",
      "¡Nivel {n}! Eso ya es para sacar pecho.",
    ],
  ],
  [
    9,
    [
      "¡Nivel {n}! Eso es más alto que la mayoría de las torres.",
      "¡Qué berraquera! Llegaron al nivel {n}.",
      "Nivel {n}: desde allá arriba ya se veían las nubes.",
    ],
  ],
  [
    12,
    [
      "¡Nivel {n}! Estuvieron a un pelo de la corona.",
      "¡Tan cerquita! El nivel {n} es casi la cima.",
      "Nivel {n}: ¡la corona ya los estaba esperando!",
    ],
  ],
];

/** The same game and level always get the same line, so a re-render doesn't change it. */
const choose = (lines: string[], seed: number) => lines[Math.abs(seed) % lines.length];

export function milestone(level: number, seed: number): string | null {
  const lines = MILESTONES[level];
  return lines ? choose(lines, seed) : null;
}

export function consolation(level: number, seed: number): string {
  const lines = CONSOLATION.find(([max]) => level <= max)?.[1] ?? CONSOLATION[CONSOLATION.length - 1][1];
  return choose(lines, seed).replace("{n}", String(level));
}
