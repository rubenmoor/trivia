// Spain's override of `es` (plans/15a-ui-translation.md, LUI-5, D-78): only the leaves that differ,
// merged over `es` at boot. «vosotros» for the players, «vídeo», Peninsular wording.
import type { Override } from "./es";

export const esES = {
  overlay: {
    /** `es`: «Presiona» (decision 59). */
    confirm: "¿Seguro? Pulsa otra vez",
    media: "Audio y vídeo de las preguntas",
  },
  flag: {
    pickerTitle: "Escribid una nota",
    copyFailed: "No se ha podido copiar: seleccionad el texto y copiadlo.",
  },
  credits: {
    media: "Imágenes, audio y vídeo de las preguntas",
    video: "Vídeo",
  },
  joker: {
    category: { title: "Cambiazo: ¿qué tema queréis?" },
    snipe: {
      aim: "Elegid la respuesta que creéis que es",
      hit: "¡Habéis dado a la correcta! Este nivel se repite.",
    },
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
      skip: "ya no os quedan Pasos",
      easier: "ya no os quedan Bájales",
      category: "ya no os quedan Cambiazos",
      snipe: "ya no os quedan Francotiradores",
    },
  },
} satisfies Override;
