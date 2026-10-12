// The Spanish catalog (plans/15a-ui-translation.md, LUI-1, D-70). Players are addressed as
// «ustedes» (Colombian usage, D-6). Leaves: a string, a plural map ({ one, other, … }) or a
// string[] of variants. `error` holds the server's refusals by code (plan 22).

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
  /** The admin overlay (Esc). */
  overlay: {
    title: "Pausa",
    continue: "Continuar",
    skip: "Saltar pregunta",
    skipAll: "Saltar y quemar para todos",
    undo: "Deshacer última respuesta",
    fullscreen: "Pantalla completa",
    restart: "Volver al inicio (termina la partida)",
    quit: "Salir del juego",
    confirm: "¿Seguro? Pulsa otra vez",
    sound: "Sonido",
    music: "Música",
    effects: "Efectos",
    media: "Audio y video de las preguntas",
    muted: "Sonido: apagado",
    unmuted: "Sonido: encendido",
    jokers: "Comodines",
    budget: "Comodines de esta partida",
    /** «Comodines: <b>{preset}</b>». */
    preset: "Comodines:",
    unlimited: "Sin límite",
    cards: "Como las cartas",
    custom: "A medida",
    less: "menos",
    more: "más",
    left: "quedan {n}",
    /** Followed by the ←/→ keys. */
    keys: "Volumen y comodines:",
    /** What the overlay acts on, shown with its id. */
    question: "pregunta",
    lastQuestion: "última pregunta",
    stats: "Estadísticas:",
    statsCategories: "categorías",
    statsDifficulty: "dificultad",
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
  /** The desktop's save file couldn't be used (plan 55); {path}: the backup. */
  save: {
    corrupt: "No se pudo leer la partida guardada. Se guardó una copia en {path} y empieza una partida nueva.",
    newer: "La partida guardada es de una versión más nueva del juego. Se guardó una copia en {path} y empieza una partida nueva.",
  },
  /** Refusals by server error code (plan 22, D-57); codes without a key show the English message. */
  error: {
    name_missing: "falta el nombre del jugador",
    name_too_long: "el nombre es demasiado largo (máximo {max} letras)",
    player_unknown: "no hay ningún jugador «{name}»",
    level_empty: "no quedan preguntas para el nivel {level} (dificultad {lo}–{hi})",
    /** {levels}: `supply_level` items joined with ", ". */
    supply_short: "no hay suficientes preguntas: {levels}",
    supply_level: "nivel {level} (dificultad {lo}–{hi}): faltan {missing}",
    purge_short: "sin este tema no alcanzan las preguntas",
    refill_empty: "no hay otra pregunta para este nivel",
    hints_used_up: "no quedan pistas",
    easier_none: "no hay preguntas más fáciles de este tema",
    category_unknown: "ese tema no existe",
    category_same: "ya están en ese tema",
    category_empty: "no hay preguntas de ese tema para este nivel",
    category_none: "no hay preguntas de otros temas para este nivel",
    snipe_last: "solo queda una respuesta",
    snipe_invalid: "no se puede apuntar a esa respuesta",
    snipe_no_repeat: "si le dan a la correcta, no quedan preguntas para repetir el nivel",
    joker_not_question: "los comodines solo se juegan en una pregunta",
    /** By joker id. */
    joker_spent: {
      hint: "ya no les quedan Soplos",
      skip: "ya no les quedan Pasos",
      easier: "ya no les quedan Bájales",
      category: "ya no les quedan Cambiazos",
      snipe: "ya no les quedan Francotiradores",
    },
    age_group_unknown: "grupo de edad desconocido: '{group}'",
    bundle_unknown: "paquete desconocido: '{bundle}'",
    bundles_not_list: "los paquetes deben ser una lista",
    save_locked: "No se pudo guardar. Se intenta de nuevo con la próxima jugada.",
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
