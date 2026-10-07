# 10 — Visual Design

**Status:** confirmed (VD-1)

How the game looks: colours, type, panels over images, component styles, motion. `04-ui-tv-display.md` owns the screens and what happens on them; this file owns how they look (UI-1). The gamemaster set the direction (D-29): **much smaller text**, **every element over the image a bit transparent**, a **gray and dark-blue** colour scheme with a few contrasting highlights, green and red for right and wrong. The rest below is a proposal, and the gamemaster has the final say.

## Concept: "Noche de concurso"

A late-night TV game show on a midnight-blue stage. The picture is the star; the interface floats over it as frosted glass. Amber stage lights mark what matters: the current level, the locked answer, the big button. Everything is a little chunky, a little tilted and a little bouncy, like a board game, not a school test.

A wink for the family: amber, navy and coral are the colours of the Colombian flag.

## Colour

All colours are CSS custom properties in one theme file (VD-2). Components use tokens only, never raw hex values.

### Base: night blue and slate gray
| Token | Value | Use |
|---|---|---|
| `--night-900` | `#0b1120` | Deepest background, behind media, letterbox |
| `--night-800` | `#111a2e` | Screen background (Start, Level, Select, results) |
| `--night-700` | `#1a2540` | Solid panels (admin overlay, dialogs) |
| `--slate-600` | `#2b3650` | Borders, inactive buttons, empty tower slots |
| `--slate-400` | `#6b7894` | Muted text, key hints, dotted outlines |
| `--slate-200` | `#c3cad8` | Secondary text (fun fact, labels) |
| `--paper` | `#eef1f6` | Primary text; never pure white |

### Glass (everything that covers the image)
| Token | Value | Use |
|---|---|---|
| `--glass` | `rgba(17, 26, 46, 0.62)` + `backdrop-filter: blur(10px) saturate(1.2)` | Answer tiles, hint notes, small panels |
| `--glass-strong` | `rgba(17, 26, 46, 0.74)` + same blur | The question card (most text) |
| `--glass-light` | `rgba(17, 26, 46, 0.45)` + `blur(6px)` | HUD chips, credit line |
| `--glass-line` | `rgba(195, 202, 216, 0.18)` | 1px border on glass, so edges read over bright images |

### Highlights
| Token | Value | Meaning |
|---|---|---|
| `--amber` | `#ffb81c` | **Commitment and stakes:** primary buttons, the locked answer, the current level, «Respuesta final» |
| `--sky` | `#4cc9f0` | **Focus and hover:** keyboard focus ring, the card or answer under the cursor, joker arming |
| `--mint` | `#2fe39a` | **Right:** the correct answer, ¡Correcto!, earned blocks glow |
| `--coral` | `#ff5470` | **Wrong:** the wrong pick, ¡Oh no!, the Snipe's struck-out answers |
| `--placeholder` | `#ff7ad9` | Reserved for `PLACEHOLDER` boxes (D-25), so unfinished parts never look finished |

- Two highlights never mean the same thing: amber says "this counts", sky says "you are here".
- Dark text (`--night-900`) on amber, mint and coral fills; light text (`--paper`) on everything else.
- Red and green never carry meaning alone: the wrong pick also shakes and gets a ✗ badge, the right one pops and gets a ✓ badge (colour-blind players, glare on the TV).

## Type

### Fonts
- **Display: Baloo 2** (rounded, chunky, playful): titles, numbers, buttons, letter badges, the tower.
- **Text: Nunito** (rounded, very legible): question, answers, card descriptions, fun facts.
- Both are under the SIL Open Font License and cover Spanish (¿ ¡ ñ á é í ó ú ü). They ship as `woff2` in `app/client/public/fonts/` with their licence; no CDN (04, AGENTS.md). Fallback: `system-ui`.
- Numbers use tabular figures, so «Nivel 10» doesn't jump.

### Scale: much smaller than the skeleton (D-29)
One unit, `--u = 100vw / 120` (16 px at 1920 px wide; it scales with the screen, 4K included), capped at `100vh / 67.5` so a window that isn't 16:9 still fits. Sizes are multiples of `--u`, never `vw` directly.

| Role | Size | px at 1080p | Skeleton had |
|---|---|---|---|
| Screen title («Nivel 3 de 12», «¡Correcto!») | 4 u | 64 | 96–115 |
| Question | 2.4 u | 38 | 65 |
| Answer | 1.9 u | 30 | 46 |
| Card description | 1.6 u | 26 | 36 |
| Body (fun fact, consolation) | 1.5 u | 24 | 36 |
| Labels, key hints, HUD | 1.1 u | 18 | 18–30 |
| Credit line, debug ID | 0.8 u | 13 | 15 |

- Nothing goes below 0.8 u. Whether this reads well from the couch is checked on the TV (VD-9, UI-6); change the unit, not the individual sizes.
- The question is at most ~55 characters per line, with `text-wrap: balance`. Long questions shrink one step (2.1 u) instead of growing to three lines.
- Text on glass gets a soft shadow (`0 1px 2px rgba(0, 0, 0, 0.5)`).

## Glass over the image

The picture should fill the screen and stay visible; the interface floats over it.

- **No full-width bands or gradients.** Every element over the image is a separate glass panel with rounded corners (1.2 u) and a `--glass-line` border, inside a **safe area** of 4 % per side (TV overscan, UI-6).
- On the Question screen, at least **half of the picture** stays uncovered: the question card sits top-centre (max 70 % wide), the answer grid bottom-centre (70 % wide), and the sides stay free.
- While the players wait for the reveal, the **picture** darkens and loses colour (brightness 40 %, saturation 30 %); the panels stay as they are, so the question and answers remain sharp.
- Decorative images stay blurred with the big «?» (D-15); the «?» becomes Baloo 2 in `--paper` at 12 % opacity.
- `backdrop-filter` may stutter on a weak TV machine (OQ-11). Fallback: a setting that drops the blur and raises the alpha to 0.85 (VD-9).

## Layout of the Question screen

```
┌─────────────────────────────────────────────────────────────────┐
│ [Nivel 5 · ▮▮▮▮▯▯▯▯▯▯▯▯]  [Ana]                                    │  HUD chips (glass-light)
│        ┌───────────────────────────────────────────────┐        │
│  (S)   │      ¿Qué instrumento se toca golpeándolo      │        │  question card (glass-strong)
│  (P)   │            con las manos o con palos?          │        │
│  (F)   └───────────────────────────────────────────────┘        │
│  (T)                 [Soplo 1: Tiene cuero]                      │  hint notes (09)
│  (X)                                                             │
│ joker            . . . . . the picture . . . . .                 │
│ tray (09)                                                        │
│        ┌──────────────────────┐  ┌──────────────────────┐       │
│        │ (A) El tambor        │  │ (B) El violín         │       │  answer tiles (glass)
│        └──────────────────────┘  └──────────────────────┘       │
│        ┌──────────────────────┐  ┌──────────────────────┐       │
│        │ (C) La flauta        │  │ (D) La trompeta       │       │
│        └──────────────────────┘  └──────────────────────┘       │
│                     [ 🔒  Respuesta final ]                       │  candy button
│                                    Foto: Jane Doe · CC BY-SA 4.0 │  credit (glass-light)
└─────────────────────────────────────────────────────────────────┘
```

- **HUD (new):** a small level chip top-left, «Nivel 5» with a 12-tick mini tower, plus the player's name (D-28). Shown on Select and Question, so the family always knows what's at stake.
- The joker tray (09) runs down the left edge inside the safe area; nothing else uses that strip.

## Components

- **Candy buttons** (primary actions: «¡Jugar!», «Respuesta final», «Volver al inicio»): solid amber fill, dark text, radius 1 u, a hard 0.35 u bottom shadow in a darker amber. On press the button moves down and the shadow collapses, like an arcade button. The primary button on a waiting screen "breathes" (scale 1 → 1.03, 2 s loop).
- **Secondary buttons:** glass with a slate border; sky ring on focus.
- **Answer tiles:** glass, a round letter badge (A–D, Baloo 2, amber on night) and the key hint.
  | State | Look |
  |---|---|
  | Idle | Glass, slate border |
  | Focus / hover | Sky ring, lift by 0.3 u |
  | Locked | Amber border 0.25 u, soft amber glow, padlock badge, scale 1.02 |
  | Dimmed (another is locked) | Opacity 0.45, desaturated |
  | Right (reveal) | Mint fill, dark text, ✓ badge, pop to 1.06 and back |
  | Wrong pick (reveal) | Coral fill, ✗ badge, shake ×3 |
- **Cards (Select):** cream paper (`#f4ecd8`, ink `#2a2238`) envelopes on the night table, each tilted at a random angle within ±3°, a number in an amber wax seal. The only light surfaces in the game, so they feel like real objects (04, UI-11).
- **Hint notes (09):** small paper notes (same cream), tilted, with a sky pin.
- **Tower (UI-3):** materials by height. Levels 1–3 slate stone (`#5d6b86`), 4–6 terracotta brick (`#c8643b`), 7–9 marble (`#d9dce6` with sky veins), 10–11 sapphire (`#3a6df0`), 12 gold (amber gradient) with the crown. Empty slots: dotted `--slate-400` at 40 %. The foundation is `--night-700` with an amber top edge. The newest block glows mint for a moment.
- **Icons:** small inline SVGs (padlock, replay, speaker, joker tokens, ✓ ✗), drawn in the same rounded style. No emoji on the TV: they look different on every system.
- **Admin overlay:** solid `--night-700`, not glass, so it reads clearly as "outside the game".

## Backgrounds (screens without media)

- **Start:** the night stage: a radial gradient (`--night-800` → `--night-900`), a soft amber spotlight cone from the top, and faint «?» glyphs drifting slowly upwards (5 % opacity). The game's name, «¡Trivia!», as a wordmark in Baloo 2 (D-30).
- **Level and Select:** the same stage, with the spotlight on the tower or the table.
- **Correct:** the stage brightens for a moment, with a mint rim light on the edges.
- **Wrong:** colours drain to grayscale navy, and the spotlight dims (with UI-4).
- **Victory:** the spotlight turns gold, and the drifting «?» become stars.

## Motion

- **Personality:** bouncy. Arrivals use a spring (`cubic-bezier(0.34, 1.56, 0.64, 1)`), exits a quick ease-in. UI feedback 150–300 ms; only set pieces (block drop, reveal, fireworks) take longer.
- Small idle life on waiting screens (breathing button, drifting «?», card wobble), never on the Question screen while the players read.
- The "reduced motion" toggle (04) turns off idle motion, shakes and bounces; fades stay.

## Implementation notes

- `app/client/src/game/theme.css`: tokens, `--u`, `@font-face`, the glass classes. It is scoped to the game (`.game`), so the review tool and the stats pages keep their own plain tool look.
- Sizes as `calc(<n> * var(--u))`. Don't set the `html` font size, so the review tool isn't affected.
- The `PLACEHOLDER` style (D-25) keeps its magenta dashed look until its task is done.

## Tasks
- [x] VD-1 Gamemaster confirms the palette, fonts and type scale from the implementation (D-30). *2026-10-06: confirmed («visual design is great»).*
- [x] VD-2 Theme file: tokens, `--u`, glass classes; replace raw colours and `vw` sizes in `app/client/src/game/`. *2026-10-06: `app/client/src/game/theme.css`, scoped to `.game`.*
- [x] VD-3 Ship Baloo 2 and Nunito (`woff2` + OFL licence) in `app/client/public/fonts/`. *2026-10-06: variable fonts, Latin subset (from Fontsource), with `OFL-*.txt`.*
- [x] VD-4 Question screen layout: floating question card, 70 % answer grid, safe area, HUD chip, free strip for the joker tray (with UI-2, JK-4). *2026-10-06: `Question.svelte`, `Hud.svelte`.*
- [x] VD-5 Candy buttons and answer tile states, with ✓/✗ badges. *2026-10-06: also the envelope cards on Select.*
- [x] VD-6 Stage backgrounds: spotlight, drifting «?», Correct/Wrong/Victory variants. *2026-10-06: `Stage.svelte`.*
- [x] VD-7 Tower materials by height (with UI-3). *2026-10-06: `Tower.svelte`: materials, drop-and-settle, wobble, crown, crumble on Wrong.*
- [x] VD-8 SVG icon set (padlock, replay, speaker, ✓, ✗; joker tokens with JK-4). *2026-10-06: `Icon.svelte` (also film, crown, star); joker tokens come with JK-4.*
- [ ] VD-9 TV check: legibility of the smaller scale from the couch, glass contrast over bright images, `backdrop-filter` performance and the no-blur fallback (with UI-6).
