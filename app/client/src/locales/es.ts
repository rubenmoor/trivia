// The Spanish catalog (plans/15a-ui-translation.md, LUI-1, D-70). Players are addressed as
// «ustedes» (Colombian usage, D-6). Leaves: a string, a plural map ({ one, other, … }) or a
// string[] of variants. The `error` namespace is reserved for plan 22.

const es = {
  app: {
    title: "Trivia",
  },
  action: {
    back: "Atrás",
    cancel: "Cancelar",
  },
  /** `key`: the keyboard shortcut (case-insensitive). */
  joker: {
    hint: { name: "Soplo", key: "S" },
    skip: { name: "Paso", key: "P", stamp: "ELIMINADO" },
    easier: { name: "Bájale", key: "F", dial: "Dificultad" },
    category: { name: "Cambiazo", key: "T", title: "Cambiazo: ¿qué tema quieren?" },
    snipe: { name: "Francotirador", key: "X" },
    /** The armed token's bubble. */
    arm: "¿Usar {name}?",
    aria: "{name} ({key})",
  },
  copy: {
    /** A line on the Level screen at some levels (UI-14). */
    milestone: {
      4: ["¡Cada vez más alto!", "¡La torre ya tiene forma!"],
      6: ["¡Ya van por la mitad!", "¡Mitad de la torre!"],
      8: ["¡Esto ya es un rascacielos!", "¡Desde aquí se ve todo el barrio!"],
      10: ["¡Ya se ve la cima!", "¡Solo quedan tres!"],
      12: ["¡Última pregunta! La corona los espera.", "¡Una más y son leyenda!"],
    },
    /** After a wrong answer, by the highest level of the bracket; {n} is the level. */
    consolation: {
      3: [
        "¡Llegaron al nivel {n}! Toda torre empieza con un primer bloque.",
        "Nivel {n}: el calentamiento ya está. ¡La próxima va más alto!",
        "¡Uy! Nivel {n}. Hasta los mejores se tropiezan al principio.",
      ],
      6: [
        "¡Llegaron al nivel {n}! La torre ya se veía desde la ventana.",
        "Nivel {n}: ¡nada mal! Ya iban por la mitad del camino.",
        "¡Nivel {n}! Eso ya es para sacar pecho.",
      ],
      9: [
        "¡Nivel {n}! Eso es más alto que la mayoría de las torres.",
        "¡Qué berraquera! Llegaron al nivel {n}.",
        "Nivel {n}: desde allá arriba ya se veían las nubes.",
      ],
      12: [
        "¡Nivel {n}! Estuvieron a un pelo de la corona.",
        "¡Tan cerquita! El nivel {n} es casi la cima.",
        "Nivel {n}: ¡la corona ya los estaba esperando!",
      ],
    },
  },
} as const;

export type Plural = { other: string } & Partial<Record<Intl.LDMLPluralRule, string>>;

type Widen<T> = T extends string
  ? string
  : T extends readonly string[]
    ? readonly string[]
    : T extends { other: string }
      ? Plural
      : { [K in keyof T]: Widen<T[K]> };

/** Shape every catalog has; wording and variant counts may differ. */
export type Catalog = Widen<typeof es>;

type Paths<T, Leaf> = {
  [K in keyof T & (string | number)]: T[K] extends Leaf
    ? `${K}`
    : T[K] extends string | readonly string[] | { other: string }
      ? never
      : `${K}.${Paths<T[K], Leaf>}`;
}[keyof T & (string | number)];

/** Keys `t()` reads: strings and plural maps. */
export type TextKey = Paths<Catalog, string | Plural>;
/** Keys `variants()` reads. */
export type VariantsKey = Paths<Catalog, readonly string[]>;
export type Key = TextKey | VariantsKey;

export default es satisfies Catalog;
