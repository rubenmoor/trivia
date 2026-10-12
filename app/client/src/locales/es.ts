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
    next: "Seguir",
    home: "Volver al inicio",
  },
  placeholder: {
    tag: "PLACEHOLDER · {task}",
  },
  /** The pool can't fill a game (GF-5). */
  supply: {
    short: "No hay suficientes preguntas para una partida completa ({n} disponibles):",
    level: "Nivel {level} (dificultad {lo}–{hi}): faltan {missing}",
  },
  hud: {
    level: "Nivel {n}",
  },
  /** Flag for review (GM-5); `key` is the shortcut (case-insensitive). */
  flag: {
    key: "M",
    on: "Marcada para revisar ({key})",
    off: "Marcar para revisar ({key})",
  },
  a11y: {
    menu: "Menú (Esc)",
  },
  /** What the admin overlay acts on. */
  overlay: {
    question: "pregunta",
    lastQuestion: "última pregunta",
  },
  /** `key`: the keyboard shortcut (case-insensitive). */
  joker: {
    hint: { name: "Soplo", key: "S" },
    skip: { name: "Paso", key: "P", stamp: "ELIMINADO", purge: "Paso, y fuera el tema «{name}»" },
    easier: { name: "Bájale", key: "F", dial: "Dificultad" },
    category: { name: "Cambiazo", key: "T", title: "Cambiazo: ¿qué tema quieren?" },
    snipe: {
      name: "Francotirador",
      key: "X",
      /** Aim hint: «{aim} <b>{false}</b> · Enter {shoot}». */
      aim: "Elijan la respuesta que creen que es",
      false: "falsa",
      shoot: "dispara",
      hit: "¡Le dieron a la correcta! Este nivel se repite.",
    },
    /** The armed token's bubble. */
    arm: "¿Usar {name}?",
    aria: "{name} ({key})",
  },
  screen: {
    loading: "Cargando…",
    noData: "Esta pantalla no tiene datos.",
    start: {
      /** The wordmark «¡Trivia!»; the marks bob on their own. */
      open: "¡",
      name: "Trivia",
      close: "!",
      subtitle: "12 preguntas seguidas para llegar a la cima",
      resume: "Continuar, nivel {level}",
      resumePlayer: "Continuar: {name}, nivel {level}",
      new: "Nueva partida",
      /** Shortcut for `new` (case-insensitive). */
      newKey: "N",
      play: "¡Jugar!",
    },
    player: {
      title: "¿Quién juega?",
      /** «¡Hola, <name>!» with the name highlighted. */
      helloOpen: "¡Hola, ",
      helloClose: "!",
      gamesNone: "sin partidas",
      games: { one: "1 partida", other: "{n} partidas" },
      won: { one: "1 ganada", other: "{n} ganadas" },
      gamesWon: "{games} · {won}",
      delete: "Borrar a {name}",
      newLabel: "¿Alguien nuevo?",
      firstLabel: "Escriban su nombre",
      placeholder: "Nombre",
      submit: "¡A jugar!",
      /** «¿Borrar a <name>?» with the name highlighted. */
      confirmOpen: "¿Borrar a ",
      confirmClose: "?",
      loseNone: "sus datos",
      lose: { one: "su partida", other: "sus {n} partidas" },
      confirmBody: "Se borran {lose} y todo su progreso: las preguntas que ya vio vuelven a salir. No se puede deshacer.",
      confirm: "Sí, borrar",
    },
    level: {
      kicker: "Nivel",
      of: "de {n}",
      again: "¡Otra vez! Le dieron a la correcta.",
    },
    select: {
      title: "Elijan una pregunta",
      empty: "No quedan preguntas para este nivel.",
      fresh: "¡Nueva!",
    },
    result: {
      correct: "¡Correcto!",
      wrong: "¡Oh no!",
      answerWas: "La respuesta correcta era",
    },
    victory: {
      title: "¡Ganaron!",
      top: "¡{name} llegó a la cima!",
    },
    question: {
      topic: "Tema: {name}",
      replay: "repetir",
      /** Shortcut for `replay` (case-insensitive). */
      replayKey: "R",
      hint: "Soplo {n}",
      mediaMissing: "medio no disponible (¿falta `trivia-media sync`?)",
      sendFailed: "No se pudo enviar la respuesta: {error}",
      final: "Respuesta final",
      finalWaiting: "Respuesta final…",
      prompt: "Elijan una respuesta",
    },
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
