# Style guide: `es-ES` (Spain)

`es-ES.ts` is an override of `es`: only the leaves that differ, merged over `es` at boot (D-78). Everything in [`es.md`](es.md) holds unless this guide says otherwise. Read both before changing a string in `es-ES.ts` or a string in `es.ts` that addresses the players.

## Glossary
Differences from `es` only.
- «vídeo» (not «video»), «Teclado y ratón» (not «mouse»), «iconos» (not «íconos»), «hoja A4» (not «hoja carta»)
- «Pulsa» (`es` «Presiona», decision 59), «¡Qué pasada!» (`es` «¡Qué maravilla!»)
- Jokers, modes, Esc rows, Steam terms: as in `es` («Modo anfitrión», «Volver al menú principal», «Salir del juego», «logros de Steam»)

## Address
- «vosotros» wherever `es` addresses the group with «ustedes»: «Elegid una respuesta», «¡Habéis ganado!», «ya no os quedan Soplos»
- Peninsular perfect for just-finished events: «ha llegado», «no se ha podido enviar»
- «tú» strings of `es` (language screen, consent) stay «tú» unless `es` uses «ustedes» there; consent asks the group («¿Nos ayudáis…?») as today
- Impersonal strings: no override

## Buttons and prompts
- As in `es`; imperative plural «-d» forms («Escribid», «Disparad»), never the infinitive used as an imperative («Elegir una pregunta» as a prompt)

## Bad patterns
Seen in review; guidance, not a lint. Wrong → right.
- «ustedes» leaking in because a new `es` string got no override: every new `es` string that addresses the players gets its `es-ES` leaf in the same change
  - fixed in task 800: `outlook.none` «… que ya vieron» → «… que ya habéis visto»; `outlook.exhausted` «Ya vieron todas …» → «Ya habéis visto todas …»
- Overriding a leaf that reads the same in Spain: leave it to `es`
