// Spain's override of `es` (plans/15a-ui-translation.md, LUI-5, D-78): only the leaves that differ,
// merged over `es` at boot. «vosotros» for the players, «vídeo», Peninsular wording.
import type { Override } from "./es.ts";

export const esES = {
  overlay: {
    /** `es`: «Presiona» (decision 59). */
    confirm: "¿Seguro? Pulsa otra vez",
    media: "Audio y vídeo de las preguntas",
  },
  consent: {
    title: "¿Nos ayudáis a mejorar el juego?",
    body: "Si aceptáis, al cerrarse el juego envía datos anónimos de las partidas: qué preguntas se respondieron, si bien o mal, nivel, grupo de edad y comodines.",
    change: "Lo podéis cambiar en el menú.",
  },
  flag: {
    pickerTitle: "Escribid una nota",
    copyFailed: "No se ha podido copiar: seleccionad el texto y copiadlo.",
    sendOffline: "Sin conexión: no se ha podido enviar.",
    sendTomorrow: "Demasiados envíos: probad mañana.",
    sendFailed: "No se ha podido enviar.",
  },
  credits: {
    media: "Imágenes, audio y vídeo de las preguntas",
    video: "Vídeo",
    achievements: "Iconos de logros de Steam",
  },
  mods: {
    held: { one: "1 mod encontrado, apagado hasta que lo permitáis", other: "{n} mods encontrados, apagados hasta que los permitáis" },
    empty: "No hay mods. Suscribíos a mods en el Workshop de Steam o poned carpetas de mods en la carpeta local de mods; la guía de modding explica dónde.",
    notice: {
      body: "Los mods los hacen otros jugadores y ejecutan código con el mismo acceso que el juego: partida guardada, logros y funciones de Steam. Encended solo mods de confianza.",
    },
  },
  joker: {
    skip: { rule: "Cambia la pregunta por otra carta. Si queréis, ese tema sale del juego." },
    category: { title: "Doña Exigente: ¿qué tema queréis?", rule: "Elegís otro tema; la dificultad sigue parecida." },
    snipe: {
      aim: "Elegid la respuesta que creéis que es",
      hit: "¡Habéis dado a la correcta! Este nivel se repite.",
      rule: "Disparad a una respuesta falsa y queda tachada. Si dais a la correcta, el nivel se repite.",
    },
  },
  bundles: {
    baseHeading: "Elegid uno",
    extraHeading: "Sumad los que queráis",
  },
  cards: {
    intro: "Una hoja A4: 4 × {hint} y 2 × cada otro comodín. Imprimir al {scale} (sin «ajustar a la página»), luego recortar por las líneas.",
  },
  outlook: {
    none: "En esta partida pueden salir preguntas que ya habéis visto.",
  },
  picker: {
    title: "Escribid vuestro nombre",
  },
  screen: {
    player: {
      firstLabel: "Escribid vuestro nombre",
    },
    level: {
      again: "¡Otra vez! Habéis dado a la correcta.",
    },
    select: {
      title: "Elegid una pregunta",
    },
    victory: {
      title: "¡Habéis ganado!",
      top: "¡{name} ha llegado a la cima!",
    },
    question: {
      prompt: "Elegid una respuesta",
    },
  },
  copy: {
    milestone: {
      6: ["¡Ya vais por la mitad!", "¡Mitad de la torre!"],
      12: ["¡Última pregunta! La corona os espera.", "¡Una más y sois leyenda!"],
    },
    consolation: {
      3: [
        "¡Habéis llegado al nivel {n}! Toda torre empieza con un primer bloque.",
        "Nivel {n}: el calentamiento ya está. ¡La próxima va más alto!",
        "¡Uy! Nivel {n}. Hasta los mejores tropiezan al principio.",
      ],
      6: [
        "¡Habéis llegado al nivel {n}! La torre ya se veía desde la ventana.",
        "Nivel {n}: ¡nada mal! Ya ibais por la mitad del camino.",
        "¡Nivel {n}! Eso ya es para sacar pecho.",
      ],
      9: [
        "¡Nivel {n}! Eso es más alto que la mayoría de las torres.",
        "¡Qué pasada! Habéis llegado al nivel {n}.",
        "Nivel {n}: desde ahí arriba ya se veían las nubes.",
      ],
      12: [
        "¡Nivel {n}! Os habéis quedado a un pelo de la corona.",
        "¡Por los pelos! El nivel {n} es casi la cima.",
        "Nivel {n}: ¡la corona ya os estaba esperando!",
      ],
    },
  },
  error: {
    category_same: "ya estáis en ese tema",
    snipe_no_repeat: "si dais a la correcta, no quedan preguntas para repetir el nivel",
    joker_spent: {
      hint: "ya no os quedan Soplos",
      skip: "ya no os queda ningún Paso y fuera",
      easier: "ya no os quedan Hadas madrinas",
      category: "ya no os queda ninguna Doña Exigente",
      snipe: "ya no os quedan Tiros mágicos",
    },
  },
} satisfies Override;
