// The Spanish catalog (plans/15a-ui-translation.md, LUI-1, D-70): neutral Latin American (es-419, D-78).
// Players are addressed as «ustedes» (D-6). Leaves: a string, a plural map ({ one, other, … }) or a
// string[] of variants. `error` holds the engine's refusals by code (plan 22).

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
  /** Flag for review (GM-5, decision 60): its dialog and «Preguntas marcadas»; `key` is the shortcut (case-insensitive). */
  flag: {
    key: "M",
    on: "Marcada para revisar ({key})",
    off: "Marcar para revisar ({key})",
    title: "¿Marcar esta pregunta?",
    titleOn: "Pregunta marcada",
    body: "Queda anotada para revisarla; la pregunta sigue.",
    notePlaceholder: "Nota opcional: ¿qué tiene de malo?",
    pickerTitle: "Escriban una nota",
    confirm: "Marcar",
    save: "Guardar nota",
    unflag: "Quitar marca",
    list: "Preguntas marcadas",
    empty: "Todavía no hay preguntas marcadas.",
    copy: "Copiar",
    copied: "Copiado",
    copyFailed: "No se pudo copiar: seleccionen el texto y cópienlo.",
    copyAll: "Copiar todo",
    send: "Enviar",
    sendAll: "Enviar todas",
    sending: "Enviando…",
    sent: "Enviada {date}",
    sendOffline: "Sin conexión: no se pudo enviar.",
    sendTomorrow: "Demasiados envíos: prueben mañana.",
    sendClosed: "Los reportes están cerrados por ahora.",
    sendFailed: "No se pudo enviar.",
    sendTitle: "¿Enviar el reporte?",
    privacy1: "Se envían la pregunta tal como se vio, la nota, el idioma y la versión del juego, con un ticket de Steam de un solo uso.",
    privacy2: "No se guarda la cuenta de Steam ni la IP; se borra al descargarse, a más tardar en 90 días.",
    question: "Pregunta",
    answer: "Respuesta",
    player: "Jugador",
    note: "Nota",
    level: "nivel {n}",
    /** The answer of the question still on screen stays hidden. */
    hidden: "(en juego)",
  },
  a11y: {
    menu: "Menú (Esc)",
  },
  /** The admin overlay (Esc). */
  overlay: {
    title: "Pausa",
    continue: "Continuar",
    skip: "Saltar pregunta",
    skipAll: "Bloquear pregunta",
    undo: "Deshacer última respuesta",
    fullscreen: "Pantalla completa",
    restart: "Volver al menú principal",
    quit: "Salir del juego",
    confirm: "¿Seguro? Presiona otra vez",
    sound: "Sonido",
    music: "Música",
    effects: "Efectos",
    media: "Audio y video de las preguntas",
    muted: "Sonido: apagado",
    unmuted: "Sonido: encendido",
    /** Opt-in telemetry (plan 108); only with a valid Steam user. */
    telemetryOn: "Datos anónimos: activados",
    telemetryOff: "Datos anónimos: desactivados",
    telemetryInfo: "Al cerrar: respuestas, niveles y comodines; sin nombres ni cuenta de Steam.",
    budget: "Comodines de esta partida",
    less: "menos",
    more: "más",
    /** Followed by the ←/→ keys. */
    keys: "Cambiar valor o columna:",
    /** Without the budget editor (outside gamemaster mode). */
    keysVolume: "Volumen:",
    /** What the overlay acts on, shown with its id. */
    question: "pregunta",
    lastQuestion: "última pregunta",
    stats: "Estadísticas:",
    statsCategories: "categorías",
    statsDifficulty: "dificultad",
    /** The gamemaster cheats, apart from the general part (MD-12, D-88). */
    cheats: "Trucos del anfitrión",
    /** Rows that code mods add (plan 117). */
    mods: "Mods",
    /** «Cambiar pregunta»: ‹ › toggles whether the old one counts as seen. */
    replace: "Cambiar pregunta",
    seen: "vista",
    unseen: "no vista",
    /** «Saltar a nivel»: ‹ › picks the level. */
    level: "Saltar a nivel",
    settings: "Ajustes de la partida",
    /** Dev mode only (plan 85): a question by id replaces the one on screen. */
    goTo: "Ir a pregunta…",
    goToBody: "Id de la pregunta (q-0007 o 7); sustituye a la que está en pantalla, en este nivel.",
    goToOpen: "Abrir",
    settingsNote: "Cartas nuevas en la mesa; el nivel y lo jugado se quedan.",
    apply: "Aplicar",
    /** Joker uses so far; the row's number is the uses left. */
    used: "{n} usados",
  },
  /** First-start language picker and the Start screen's language button (plan 126); language names are endonyms in lib/i18n.ts. */
  language: {
    /** First-start screen (fresh save): heading and confirm prompt. */
    choose: "Elige el idioma",
    confirm: "Aceptar",
  },
  /** First-start telemetry question (plan 108; PRIVACY.md has the long version). */
  consent: {
    title: "¿Nos ayudas a mejorar el juego?",
    body: "Si aceptas, al cerrarse el juego envía datos anónimos de las partidas: qué preguntas se respondieron, si bien o mal, nivel, grupo de edad y comodines.",
    noNames: "Sin nombres, sin cuenta de Steam, sin dirección IP.",
    change: "Lo puedes cambiar en el menú.",
    no: "No",
    yes: "Sí, enviar datos",
  },
  /** The Credits screen (PUB-5, plan 47); its data is credits.json from the build. */
  credits: {
    open: "Créditos",
    title: "Créditos",
    /** Header line (plan 91): game version, pool export hash. */
    version: "Versión {version}",
    pool: "preguntas {pool}",
    loading: "Cargando…",
    failed: "No se pudieron cargar los créditos.",
    scroll: "Desplazar",
    jump: "Sección",
    game: "Juego",
    media: "Imágenes, audio y video de las preguntas",
    sounds: "Sonidos",
    /** Victory march (task 745). */
    elgar: "Marcha de la victoria: Pompa y circunstancia n.º 1, compuesta por Edward Elgar († 1934, dominio público); grabación de la Banda de la Infantería de Marina de los Estados Unidos, obra del gobierno de EE. UU. (dominio público).",
    horizon: "Imágenes de la pantalla de inicio",
    fonts: "Fuentes",
    glyphs: "Botones del control",
    glyphsText: "Originales, dibujados para el juego",
    achievements: "Íconos de logros de Steam",
    libraries: "Bibliotecas",
    unknownAuthor: "Autor desconocido",
    image: "Imagen",
    audio: "Audio",
    video: "Video",
    background: "Fondo",
    /** A mod bundle's media section (decision 129). */
    playerMade: "Hecho por jugadores · {mod}",
  },
  /** The Mods screen (plan 118); codes from the shell (plan 112, 114) and lib/mods.ts (plan 117). */
  mods: {
    open: "Mods",
    title: "Mods",
    /** Start screen, while the notice isn't accepted. */
    held: { one: "1 mod encontrado, apagado hasta que lo permitan", other: "{n} mods encontrados, apagados hasta que los permitan" },
    loading: "Cargando…",
    order: "El de arriba gana cuando dos cambian el mismo archivo.",
    move: "Mover",
    up: "Subir",
    down: "Bajar",
    turnOn: "Encender",
    turnOff: "Apagar",
    refresh: "Actualizar",
    allOff: "Apagar todos",
    restart: "Reiniciar para aplicar",
    local: "Carpeta local",
    workshop: "Workshop de Steam · {id}",
    allLanguages: "Todos los idiomas",
    folder: "Carpeta: {dir}",
    crashed: "El último inicio con mods no terminó. Se inició sin mods. Activos entonces: {mods}.",
    crashedUnknown: "El último inicio con mods no terminó. Se inició sin mods.",
    flag: "Iniciado sin mods (--no-mods).",
    noUser: "Los mods necesitan Steam con un usuario conectado. Se pueden encender y apagar igual.",
    empty: "No hay mods. Suscríbanse a mods en el Workshop de Steam o pongan carpetas de mods en la carpeta local de mods; la guía de modding explica dónde.",
    failed: "No se pudo guardar la lista de mods.",
    kind: {
      bundle: "Preguntas",
      theme: "Tema visual",
      code: "Código",
      conversion: "Conversión total",
    },
    state: {
      loaded: "Cargado",
      off: "Apagado",
      onNext: "Se enciende al reiniciar",
      offNext: "Se apaga al reiniciar",
      invalid: "No válido: {reason}",
      downloading: "Descargando en Steam",
      disabled: "Desactivado en Steam",
      no_user: "Necesita un usuario de Steam",
    },
    error: {
      not_a_folder: "no es una carpeta",
      no_manifest: "falta mod.json",
      bad_json: "mod.json no se puede leer",
      bad_field: "campo «{field}» incorrecto en mod.json",
      entry_missing: "falta el script de entrada",
      duplicate_id: "otro mod tiene el mismo id",
    },
    warning: {
      game_version: "Hecho para la versión {version}",
      needs_update: "Actualización pendiente en Steam",
      workshop_id_mismatch: "mod.json nombra otro ítem del Workshop",
      unknown_key: "mod.json tiene un campo desconocido",
      unknown_language: "mod.json nombra un idioma desconocido",
      bundle_json: "data/bundles.json no se puede leer",
      bundle_row: "Un paquete de data/bundles.json se ignora",
      load_failed: "El script no cargó",
      setup_failed: "Falló al iniciar",
      timeout: "Tardó demasiado en iniciar",
      hook_failed: "Un cambio del mod falló",
    },
    /** Per mod bundle, from lib/data.ts modIssues(); {bundle}: its name. */
    issue: {
      bad_question: { one: "{bundle}: 1 pregunta omitida", other: "{bundle}: {n} preguntas omitidas" },
      bad_media: { one: "{bundle}: 1 archivo multimedia omitido", other: "{bundle}: {n} archivos multimedia omitidos" },
      bad_categories: "{bundle}: categories.json no se puede leer",
      no_pool: "{bundle}: no hay preguntas para este idioma",
      bundle_language: { one: "{bundle}: 1 idioma sin preguntas se ignora", other: "{bundle}: {n} idiomas sin preguntas se ignoran" },
    },
    /** One-time notice before the first mod runs. */
    notice: {
      title: "¿Permitir mods?",
      body: "Los mods los hacen otros jugadores y corren código con el mismo acceso que el juego: partida guardada, logros y funciones de Steam. Enciendan solo mods de confianza.",
      crash: "Si un inicio con mods falla, el siguiente arranca sin mods.",
      allow: "Permitir mods",
    },
  },
  /** `key`: the keyboard shortcut (case-insensitive). */
  joker: {
    /** `rule`: the one line on the printed card (JK-11). */
    hint: { name: "Soplo", key: "S", rule: "Muestra una pista de la pregunta. Hasta tres por pregunta." },
    skip: { name: "Paso y fuera", key: "P", pass: "Solo paso", stamp: "ELIMINADO", purge: "Quitar todas las preguntas del tema «{name}»",
      rule: "Cambia la pregunta por otra carta. Si quieren, ese tema sale del juego.",
    },
    easier: { name: "Hada madrina", key: "H", dial: "Dificultad", rule: "Cambia la pregunta por una más fácil del mismo tema." },
    category: { name: "Doña Exigente", key: "E", title: "Doña Exigente: ¿qué tema quieren?",
      rule: "Ustedes eligen otro tema; la dificultad sigue parecida.",
    },
    snipe: {
      name: "Tiro mágico",
      key: "T",
      /** Aim hint: «{aim} <b>{false}</b> · Enter {shoot}». */
      aim: "Elijan la respuesta que creen que es",
      false: "falsa",
      shoot: "dispara",
      hit: "¡Le dieron a la correcta! Este nivel se repite.",
      rule: "Disparen a una respuesta falsa y queda tachada. Si le dan a la correcta, el nivel se repite.",
    },
    /** The armed token's bubble. */
    arm: "¿Usar {name}?",
    aria: "{name} ({key})",
  },
  /** The printable joker cards (`/comodines`, JK-11); `{scale}` is «100 %» in bold. */
  cards: {
    title: "Comodines para imprimir",
    intro: "Una hoja carta: 4 × {hint} y 2 × cada otro comodín. Imprimir al {scale} (sin «ajustar a la página»), luego recortar por las líneas.",
    print: "Imprimir",
  },
  bundles: {
    /** The Bundles screen (plan 151): «¿Qué preguntas juega <name>?» with the name highlighted. */
    titleOpen: "¿Qué preguntas juega ",
    titleClose: "?",
    /** Heading of the base bundles' column: exactly one. */
    baseHeading: "Elijan uno",
    /** Heading of the optional bundles' column: any number. */
    extraHeading: "Sumen los que quieran",
    /** A mod's bundle (decision 128); `mod`: the mod's name. */
    playerMade: "Hecho por jugadores · {mod}",
  },
  /** The Choice screen (plan 29): mode, age group and the like before a game. */
  choice: {
    /** «¿Cómo juega <name>?» with the name highlighted. */
    titleOpen: "¿Cómo juega ",
    titleClose: "?",
    groups: "Edad",
    ages: "{lo}–{hi} años",
    agesFrom: "{lo}+ años",
    on: "activado",
    off: "desactivado",
    start: "¡A jugar!",
    /** The running game's choice in the overlay, two rows. */
    lineGroup: "Edad: {group}",
    lineBundles: "Paquetes de preguntas: {bundles}",
    /** A custom difficulty in place of the group (D-88). */
    difficulty: "Dificultad {start}–{end}",
  },
  /** The mode row on the Choice screen (MD-7); names English first in code, Spanish per 15a. */
  mode: {
    heading: "Modo",
    gamemaster: "Modo anfitrión",
    gamemasterAbout: "El anfitrión lo maneja todo",
    gamemasterKey: "A",
    solo: "Solo o en grupo",
    soloAbout: "Sin trucos, comodines estándar",
    soloKey: "G",
  },
  /** «Personalizar partida» in «Solo o en grupo» (MD-7): the joker counts. */
  customize: {
    open: "Personalizar partida",
    openKey: "P",
    title: "Personalizar partida",
    body: "Una partida personalizada no gana logros de Steam.",
    standard: "Comodines estándar",
    custom: "Comodines personalizados",
    done: "Listo",
  },
  /** The configure game screen (MD-11, D-88): gamemaster mode's fields on the Choice screen. */
  configure: {
    game: "Partida",
    difficulty: "Dificultad",
    /** The difficulty row's value after the age groups: start and end set by hand. */
    custom: "A medida",
    start: "Desde",
    end: "Hasta",
    levels: "Niveles",
    cards: "Cartas por nivel",
    /** 0 cards: the question shows at once. */
    noCards: "pregunta directa",
    video: "Preguntas con video",
    audio: "Preguntas con audio",
    /** Switch (D-105): off = the padlock reveals the correct answer, every question advances one level. */
    answers: "Responder para avanzar",
    jokers: "Comodines",
    /** The jokers preset row (decision 99): picking one fills the counts; edited counts show `custom`. */
    preset: "Conjunto",
    presets: { standard: "Estándar", unlimited: "Sin límite", custom: "Personalizado" },
  },
  /** The supply notice before level 1 (plan 65, decision 31): informational, «¡A jugar!» stays. */
  outlook: {
    title: "Antes de empezar",
    /** {ranges}: difficulty ranges, «7» or «13–15», joined with ", ". */
    tight: "Casi no quedan preguntas nuevas de dificultad {ranges}; después se repetirán algunas.",
    none: "En esta partida pueden salir preguntas que ya vieron.",
    bundle: "Con el paquete {bundle} activado habría más.",
    /** {list}: subcategory names joined with ", ". */
    exhausted: { one: "A este paquete le quedan pocas preguntas: {list}", other: "A estos paquetes les quedan pocas preguntas: {list}" },
  },
  /** The letter picker: a new name with a pad only (plan 46). */
  /** A seat's controller is gone (decision 289). */
  seat: {
    lostTitle: "Mando de {name} desconectado",
    lostBody: "Reconéctenlo o usen otro mando libre.",
    take: "Tomar su lugar",
  },
  picker: {
    /** The keys, in order; `marks`: extra keys for a note. */
    letters: "ABCDEFGHIJKLMNOPQRSTUVWXYZÑÁÉÍÓÚÜ-",
    marks: "0123456789.,?¿!¡",
    title: "Escriban su nombre",
    write: "Escribir",
    space: "Espacio",
    erase: "Borrar",
    done: "Listo",
  },
  screen: {
    loading: "Cargando…",
    noData: "Esta pantalla no tiene datos.",
    start: {
      /** The wordmark «¡Trivia!»; the marks bob on their own. */
      open: "¡",
      name: "Trivia",
      close: "!",
      subtitle: { one: "1 pregunta para llegar a la cima", other: "{n} preguntas seguidas para llegar a la cima" },
      resume: "Continuar, nivel {level}",
      resumePlayer: "Continuar: {name}, nivel {level}",
      new: "Nueva partida",
      /** Shortcut for `new` (case-insensitive). */
      newKey: "N",
      /** Language button top right (plan 126): aria label; the button shows the endonym. */
      language: "Idioma: {name}",
      /** Shortcut for `language` (case-insensitive). */
      languageKey: "I",
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
      confirmBody: "Se borran el nombre y {lose}. Las preguntas que ya vio siguen contando como vistas. No se puede deshacer.",
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
      /** Answers off (D-105): after a reveal, and after the last level. */
      next: "Siguiente ronda",
      completed: "Cuestionario completado",
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
      peek: "Ver imagen",
      /** Hold to show only the picture (plan 113); case-insensitive. */
      peekKey: "V",
      hint: "Soplo {n}",
      mediaMissing: "medio no disponible (¿falta `trivia-media sync`?)",
      sendFailed: "No se pudo enviar la respuesta: {error}",
      final: "Respuesta final",
      finalWaiting: "Respuesta final…",
      prompt: "Elijan una respuesta",
      /** The padlock with answers off (D-105). */
      reveal: "Mostrar respuesta",
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
        "¡Qué maravilla! Llegaron al nivel {n}.",
        "Nivel {n}: desde allá arriba ya se veían las nubes.",
      ],
      12: [
        "¡Nivel {n}! Estuvieron a un pelo de la corona.",
        "¡Tan cerquita! El nivel {n} es casi la cima.",
        "Nivel {n}: ¡la corona ya los estaba esperando!",
      ],
    },
  },
  /** The save file couldn't be used (plan 55, decision 98); {path}: the backup. */
  save: {
    corrupt: "El archivo de la partida guardada está dañado. Se guardó como copia de seguridad en {path} y empieza una partida nueva.",
    newer: "El archivo de la partida guardada es de una versión más nueva del juego. Se guardó como copia de seguridad en {path} y empieza una partida nueva.",
    /** No valid Steam user (decision 111): memory-only save. */
    unsaved: "Sin Steam no se guarda el progreso.",
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
      skip: "ya no les queda ningún Paso y fuera",
      easier: "ya no les quedan Hadas madrinas",
      category: "ya no les queda ninguna Doña Exigente",
      snipe: "ya no les quedan Tiros mágicos",
    },
    age_group_unknown: "grupo de edad desconocido: '{group}'",
    bundle_unknown: "paquete desconocido: '{bundle}'",
    bundles_not_list: "los paquetes deben ser una lista",
    bundle_not_offered: "el paquete '{bundle}' no está disponible en este idioma",
    base_bundle_count: "elige exactamente un paquete básico",
    difficulty_invalid: "dificultad a medida: de 1 a 15, el final no menor que el inicio",
    levels_invalid: "número de niveles: de {min} a {max}",
    cards_invalid: "cartas por nivel: de {min} a {max}",
    switch_invalid: "valor no válido para {field}",
    mode_unknown: "modo desconocido: '{mode}'",
    mode_not_built: "ese modo todavía no se puede jugar",
    mode_single: "ese modo es para un solo jugador",
    seat_missing: "no se sabe qué jugador es",
    seat_unknown: "ese jugador no está en la partida",
    seat_out: "ese jugador ya está fuera de la partida",
    not_your_turn: "no es tu turno",
    player_twice: "«{name}» solo puede jugar una vez",
    players_too_few: "hacen falta al menos {min} jugadores",
    gamemaster_only: "en este modo no se puede",
    replace_empty: "no hay otra pregunta para este nivel",
    question_unknown: "no hay ninguna pregunta «{id}» cargada (otro idioma o paquete no instalado)",
    level_invalid: "nivel: de {min} a {max}",
    answers_on: "aquí hay que elegir una respuesta",
    answers_off: "sin elegir respuesta: el candado muestra la correcta",
    snipe_answers_off: "sin elegir respuesta no hay a qué apuntar",
    cheat_not_select: "solo se puede con las cartas en la mesa",
    save_locked: "No se pudo guardar. Se intenta de nuevo con la próxima jugada.",
    bad_save: "No se pudo guardar la partida. El juego sigue.",
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

type Partial_<T> = T extends string | readonly string[] | Plural ? T : { [K in keyof T]?: Partial_<T[K]> };
/** A regional override (`es-ES`): only the differing leaves; plural maps and variant arrays whole. */
export type Override = Partial_<Catalog>;

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

export default es satisfies Catalog;
