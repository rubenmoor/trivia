// The audio engine (plans/04-ui-tv-display.md, "Audio", UI-8, D-21/D-22): one AudioContext,
// three channels (music, effects, question media) under a master gain, fades and crossfades.
// Recorded sounds live in app/client/public/audio/ (free licences, CREDITS.md, UI-10) and replace the
// synthesized ones they cover; everything else is synthesized: the music loops are generated
// (same key and tempo family, rising intensity) and each effect name maps to a recipe below.

/** normal: Start/Level/Select; question: a question on screen; submitted: an answer locked in;
 * roll: the drum roll from «Respuesta final» until the reveal; victory: «Pomp and Circumstance»
 * on the Victory screen, once (04, "Music"). */
export type Track = "normal" | "question" | "submitted" | "roll" | "victory";

export type Volumes = { music: number; effects: number; media: number; muted: boolean };

const STORE = "trivia.volumes";
const DEFAULTS: Volumes = { music: 0.3, effects: 0.7, media: 1, muted: false };

function loadVolumes(): Volumes {
  try {
    return { ...DEFAULTS, ...JSON.parse(localStorage.getItem(STORE) ?? "{}") };
  } catch {
    return { ...DEFAULTS };
  }
}

/** Reactive settings (the admin overlay edits them) and what is playing. */
export const sound = $state({
  volumes: loadVolumes(),
  music: null as Track | null,
  unlocked: false,
});

let ctx: AudioContext | null = null;
let master: GainNode, musicBus: GainNode, fxBus: GainNode, duckGain: GainNode;
let noiseBuffer: AudioBuffer;

/** Recorded sounds (UI-10), decoded once after the unlock; a missing one falls back to synthesis. */
const SAMPLE_NAMES = [
  "aplausos", "aplausos-gran", "redoble", "fanfarria", "trombon-triste", "candado-cierra", "candado-abre",
  "papel", "vidrio", "sello", "golpe", "estallido", "victoria",
] as const;
type Sample = (typeof SAMPLE_NAMES)[number];
const samples: Partial<Record<Sample, AudioBuffer>> = {};
/** Effect names played from a recording, first match wins; `rate` changes the pitch. */
const SAMPLE_FOR: [RegExp, Sample, ((name: string) => number)?][] = [
  [/gran aplausos/, "aplausos-gran"],
  [/aplausos/, "aplausos"],
  [/fanfarria/, "fanfarria"],
  [/trombón|Ups/, "trombon-triste"],
  [/candado: clunk|candado se cierra/, "candado-cierra"],
  [/candado se abre/, "candado-abre"],
  [/^papel$/, "papel"],
  [/vidrio/, "vidrio"],
  [/sello/, "sello"],
  // The block landing: the higher the tower, the higher the thud (04, "Block arrival").
  [/bloque (\d+)/, "golpe", (n) => 0.75 + Number(/bloque (\d+)/.exec(n)?.[1] ?? 1) * 0.06],
  [/estallido/, "estallido", () => 0.85 + Math.random() * 0.3],
];

async function loadSamples(c: AudioContext) {
  await Promise.all(
    SAMPLE_NAMES.map(async (key) => {
      try {
        samples[key] = await c.decodeAudioData(await (await fetch(`/audio/${key}.m4a`)).arrayBuffer());
      } catch {
        /* offline or not supported: the synthesized version plays instead */
      }
    }),
  );
}

/** The first click or key press unlocks audio in the browser (04, "Start"). */
export function unlock() {
  if (ctx) return void ctx.resume();
  ctx = new AudioContext();
  master = ctx.createGain();
  master.connect(ctx.destination);
  musicBus = ctx.createGain();
  duckGain = ctx.createGain();
  musicBus.connect(duckGain).connect(master);
  fxBus = ctx.createGain();
  fxBus.connect(master);
  noiseBuffer = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
  const data = noiseBuffer.getChannelData(0);
  for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
  sound.unlocked = true;
  loadSamples(ctx);
  applyVolumes();
  if (sound.music) startTrack(sound.music, 0.8);
}

export function setVolumes(v: Partial<Volumes>) {
  sound.volumes = { ...sound.volumes, ...v };
  try {
    localStorage.setItem(STORE, JSON.stringify(sound.volumes));
  } catch {
    /* private window: settings last for this session only */
  }
  applyVolumes();
}

function applyVolumes() {
  if (!ctx) return;
  const v = sound.volumes;
  const t = ctx.currentTime;
  master.gain.setTargetAtTime(v.muted ? 0 : 1, t, 0.05);
  musicBus.gain.setTargetAtTime(v.music * 0.5, t, 0.05);
  fxBus.gain.setTargetAtTime(v.effects, t, 0.05);
}

/** Volume for the question's <audio>/<video> (they play outside the AudioContext). */
export function mediaVolume() {
  return sound.volumes.muted ? 0 : sound.volumes.media;
}

/** Jokers duck the music to about half while they play (09, "Common play animation"). */
export function duck(on: boolean) {
  if (ctx) duckGain.gain.setTargetAtTime(on ? 0.5 : 1, ctx.currentTime, 0.12);
}

// Music ------------------------------------------------------------------------------------------

type Loop = { gain: GainNode; stop: () => void };
let current: Loop | null = null;

/** Switch the music loop; null = silence. Screen changes fade out and in (04, "Transitions");
 * on the Question screen the changes are sharp cuts: locking in, unlocking, the drum roll, the
 * reveal (gamemaster feedback: the music has to jump when an answer is clicked). */
export function music(track: Track | null) {
  if (track === sound.music) return;
  const from = sound.music;
  sound.music = track;
  if (!ctx) return;
  const inQuestion = (t: Track | null) => t === "question" || t === "submitted" || t === "roll";
  const sharp = inQuestion(from) && (inQuestion(track) || track === null);
  fadeOut(sharp ? (from === "roll" ? 0.15 : 0.08) : 0.6);
  if (track) startTrack(track, sharp ? 0.05 : 0.8);
}

function fadeOut(seconds: number) {
  if (!current || !ctx) return;
  const loop = current;
  current = null;
  const t = ctx.currentTime;
  loop.gain.gain.cancelScheduledValues(t);
  loop.gain.gain.setValueAtTime(loop.gain.gain.value, t);
  loop.gain.gain.linearRampToValueAtTime(0, t + seconds);
  setTimeout(loop.stop, seconds * 1000 + 100);
}

/** The theme: A minor, i – VI – III – V (Am F C E), one chord per bar. */
const CHORDS = [
  [57, 60, 64],
  [53, 57, 60],
  [55, 60, 64],
  [52, 56, 59],
];
const TEMPO: Record<Track, number> = { normal: 76, question: 96, submitted: 120, roll: 120, victory: 120 };
/** The drum roll: hits per second, and how long it takes to build to full strength. */
const ROLL_HZ = 22;
const ROLL_BUILD_S = 6;
const hz = (midi: number) => 440 * 2 ** ((midi - 69) / 12);

function startTrack(track: Track, fadeIn: number) {
  if (!ctx) return;
  const c = ctx;
  const gain = c.createGain();
  gain.gain.setValueAtTime(0, c.currentTime);
  gain.gain.linearRampToValueAtTime(1, c.currentTime + fadeIn);
  gain.connect(musicBus);
  const beat = 60 / TEMPO[track];
  let next = c.currentTime + 0.05;
  let step = 0; // eighth notes
  const voices = new Set<AudioScheduledSourceNode>();
  const keep = (n: AudioScheduledSourceNode) => {
    voices.add(n);
    n.onended = () => voices.delete(n);
  };
  // A lookahead scheduler: notes are placed slightly ahead of time, so the loop never stutters.
  if (track === "victory") {
    // Elgar's finale (US Marine Band, public domain), once and loud: it is the moment, not a
    // background loop. Without the file the Victory screen keeps its cheers only.
    if (samples.victoria) {
      const src = c.createBufferSource();
      src.buffer = samples.victoria;
      const level = c.createGain();
      level.gain.value = 3;
      src.connect(level).connect(gain);
      src.start(c.currentTime + 0.05);
      keep(src);
    }
    current = {
      gain,
      stop: () => {
        voices.forEach((v) => v.stop());
        gain.disconnect();
      },
    };
    return;
  }
  if (track === "roll") {
    // Crescendo from soft to full over ROLL_BUILD_S, then keep rolling at full strength.
    const swell = c.createGain();
    swell.gain.setValueAtTime(0.3, c.currentTime);
    swell.gain.linearRampToValueAtTime(1, c.currentTime + ROLL_BUILD_S);
    swell.connect(gain);
    if (samples.redoble) {
      // The recorded roll (US Air Force Band, public domain), looped if the wait is longer.
      const src = c.createBufferSource();
      src.buffer = samples.redoble;
      src.loop = true;
      const level = c.createGain();
      level.gain.value = 2.2; // the music bus is set for soft loops; the roll is the music here
      src.connect(level).connect(swell);
      src.start();
      keep(src);
      current = {
        gain,
        stop: () => {
          voices.forEach((v) => v.stop());
          gain.disconnect();
        },
      };
      return;
    }
    const rumble = c.createOscillator();
    rumble.frequency.value = hz(33);
    const rg = c.createGain();
    rg.gain.value = 0.12;
    rumble.connect(rg).connect(swell);
    rumble.start();
    keep(rumble);
    let i = 0;
    const timer = setInterval(() => {
      while (next < c.currentTime + 0.2) {
        snare(c, swell, next, 0.5 + (i++ % 2) * 0.12 + Math.random() * 0.1, keep);
        next += 1 / ROLL_HZ;
      }
    }, 40);
    current = {
      gain,
      stop: () => {
        clearInterval(timer);
        voices.forEach((v) => v.stop());
        gain.disconnect();
      },
    };
    return;
  }
  const timer = setInterval(() => {
    while (next < c.currentTime + 0.2) {
      const bar = Math.floor(step / 8) % 4;
      const chord = CHORDS[bar];
      if (step % 8 === 0) pad(c, gain, chord, next, beat * 4, track, keep);
      if (track === "normal" && step % 2 === 0) pluck(c, gain, chord[0] - 12, next, 0.18, keep);
      if (track === "question") {
        pluck(c, gain, chord[0] - 12, next, 0.22, keep);
        tick(c, gain, next, step % 2 ? 0.05 : 0.09, keep);
      }
      if (track === "submitted") {
        if (step % 4 === 0) thump(c, gain, next, 0.9, keep);
        if (step % 4 === 1) thump(c, gain, next + beat * 0.1, 0.6, keep);
        tick(c, gain, next, 0.06, keep);
        if (step % 8 === 6) roll(c, gain, next, beat, keep);
      }
      next += beat / 2;
      step++;
    }
  }, 50);
  current = {
    gain,
    stop: () => {
      clearInterval(timer);
      voices.forEach((v) => v.stop());
      gain.disconnect();
    },
  };
}

type Keep = (n: AudioScheduledSourceNode) => void;

function pad(c: AudioContext, out: AudioNode, chord: number[], t: number, len: number, track: Track, keep: Keep) {
  const filter = c.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.value = track === "normal" ? 700 : track === "question" ? 1100 : 1600;
  const g = c.createGain();
  g.gain.setValueAtTime(0, t);
  g.gain.linearRampToValueAtTime(0.06, t + len * 0.25);
  g.gain.linearRampToValueAtTime(0, t + len);
  filter.connect(g).connect(out);
  for (const note of chord) {
    for (const detune of [-7, 7]) {
      const o = c.createOscillator();
      o.type = "sawtooth";
      o.frequency.value = hz(note);
      o.detune.value = detune;
      // Submitted: the pad creeps upwards, so the tension rises towards the reveal.
      if (track === "submitted") o.detune.linearRampToValueAtTime(detune + 60, t + len);
      o.connect(filter);
      o.start(t);
      o.stop(t + len + 0.05);
      keep(o);
    }
  }
}

function pluck(c: AudioContext, out: AudioNode, note: number, t: number, level: number, keep: Keep) {
  const o = c.createOscillator();
  o.type = "triangle";
  o.frequency.value = hz(note);
  const g = c.createGain();
  g.gain.setValueAtTime(level, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
  o.connect(g).connect(out);
  o.start(t);
  o.stop(t + 0.4);
  keep(o);
}

function tick(c: AudioContext, out: AudioNode, t: number, level: number, keep: Keep) {
  const n = c.createBufferSource();
  n.buffer = noiseBuffer;
  const f = c.createBiquadFilter();
  f.type = "highpass";
  f.frequency.value = 7000;
  const g = c.createGain();
  g.gain.setValueAtTime(level, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.04);
  n.connect(f).connect(g).connect(out);
  n.start(t, Math.random() * 0.5, 0.05);
  keep(n);
}

function snare(c: AudioContext, out: AudioNode, t: number, level: number, keep: Keep) {
  const n = c.createBufferSource();
  n.buffer = noiseBuffer;
  const f = c.createBiquadFilter();
  f.type = "bandpass";
  f.frequency.value = 2400 + Math.random() * 600;
  f.Q.value = 0.9;
  const g = c.createGain();
  g.gain.setValueAtTime(level * 0.35, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.07);
  n.connect(f).connect(g).connect(out);
  n.start(t, Math.random() * 0.8, 0.08);
  keep(n);
  const body = c.createOscillator();
  body.frequency.setValueAtTime(210, t);
  body.frequency.exponentialRampToValueAtTime(150, t + 0.04);
  const bg = c.createGain();
  bg.gain.setValueAtTime(level * 0.12, t);
  bg.gain.exponentialRampToValueAtTime(0.001, t + 0.05);
  body.connect(bg).connect(out);
  body.start(t);
  body.stop(t + 0.06);
  keep(body);
}

function thump(c: AudioContext, out: AudioNode, t: number, level: number, keep: Keep) {
  const o = c.createOscillator();
  o.frequency.setValueAtTime(110, t);
  o.frequency.exponentialRampToValueAtTime(42, t + 0.15);
  const g = c.createGain();
  g.gain.setValueAtTime(level * 0.5, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
  o.connect(g).connect(out);
  o.start(t);
  o.stop(t + 0.3);
  keep(o);
}

function roll(c: AudioContext, out: AudioNode, t: number, len: number, keep: Keep) {
  for (let i = 0; i < 8; i++) thump(c, out, t + (i * len) / 8, 0.15 + i * 0.05, keep);
}

// Effects ----------------------------------------------------------------------------------------

/** Play a short effect by name; the names describe the sound (04, "Sound assets"). */
export function sfx(name: string) {
  if (!ctx || ctx.state !== "running") return;
  const [, key, rate] = SAMPLE_FOR.find(([pattern]) => pattern.test(name)) ?? [];
  const buffer = key && samples[key];
  if (buffer) {
    const src = ctx.createBufferSource();
    src.buffer = buffer;
    if (rate) src.playbackRate.value = rate(name);
    src.connect(fxBus);
    src.start();
    return;
  }
  const recipe = RECIPES.find(([pattern]) => pattern.test(name));
  recipe?.[1](ctx, fxBus, ctx.currentTime + 0.01, name);
}

type Recipe = (c: AudioContext, out: AudioNode, t: number, name: string) => void;

function tone(c: AudioContext, out: AudioNode, t: number, opts: {
  type?: OscillatorType; from: number; to?: number; len: number; level?: number; attack?: number;
}) {
  const o = c.createOscillator();
  o.type = opts.type ?? "sine";
  o.frequency.setValueAtTime(opts.from, t);
  if (opts.to) o.frequency.exponentialRampToValueAtTime(opts.to, t + opts.len);
  const g = c.createGain();
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(opts.level ?? 0.3, t + (opts.attack ?? 0.005));
  g.gain.exponentialRampToValueAtTime(0.0001, t + opts.len);
  o.connect(g).connect(out);
  o.start(t);
  o.stop(t + opts.len + 0.05);
}

function noise(c: AudioContext, out: AudioNode, t: number, opts: {
  type?: BiquadFilterType; from: number; to?: number; len: number; level?: number; q?: number; attack?: number;
}) {
  const n = c.createBufferSource();
  n.buffer = noiseBuffer;
  n.loop = true;
  const f = c.createBiquadFilter();
  f.type = opts.type ?? "bandpass";
  f.Q.value = opts.q ?? 1;
  f.frequency.setValueAtTime(opts.from, t);
  if (opts.to) f.frequency.exponentialRampToValueAtTime(opts.to, t + opts.len);
  const g = c.createGain();
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(opts.level ?? 0.4, t + (opts.attack ?? 0.01));
  g.gain.exponentialRampToValueAtTime(0.0001, t + opts.len);
  n.connect(f).connect(g).connect(out);
  n.start(t);
  n.stop(t + opts.len + 0.05);
}

function notes(c: AudioContext, out: AudioNode, t: number, midis: number[], step: number, type: OscillatorType, len = 0.35) {
  midis.forEach((m, i) => tone(c, out, t + i * step, { type, from: hz(m), len, level: 0.22 }));
}

/** A crowd clapping: hundreds of short, band-passed noise bursts at random moments, swelling in
 * quickly and dying away, with a few louder claps near the front. */
function applause(c: AudioContext, out: AudioNode, t: number, seconds: number) {
  const claps = Math.round(seconds * 70);
  for (let i = 0; i < claps; i++) {
    const at = Math.random() ** 1.6 * seconds; // denser at the start
    const swell = Math.min(1, at / 0.35) * Math.max(0, 1 - at / seconds);
    const level = (0.08 + Math.random() * 0.12) * swell;
    if (level < 0.01) continue;
    const n = c.createBufferSource();
    n.buffer = noiseBuffer;
    const f = c.createBiquadFilter();
    f.type = "bandpass";
    f.frequency.value = 900 + Math.random() * 1800;
    f.Q.value = 1.2;
    const pan = c.createStereoPanner();
    pan.pan.value = Math.random() * 1.6 - 0.8;
    const g = c.createGain();
    const len = 0.015 + Math.random() * 0.025;
    g.gain.setValueAtTime(level, t + at);
    g.gain.exponentialRampToValueAtTime(0.0001, t + at + len);
    n.connect(f).connect(g).connect(pan).connect(out);
    n.start(t + at, Math.random() * 0.9, len + 0.01);
  }
}

/** First match wins; patterns follow the effect names used in the game's code. */
const RECIPES: [RegExp, Recipe][] = [
  [/silencio/, () => {}],
  // Fireworks (UI-9)
  [/cohete/, (c, o, t) => {
    tone(c, o, t, { from: 600, to: 2400, len: 0.9, level: 0.05, attack: 0.1 });
    noise(c, o, t, { type: "highpass", from: 3000, len: 0.9, level: 0.08, attack: 0.1 });
  }],
  [/estallido/, (c, o, t) => {
    tone(c, o, t, { from: 120, to: 40, len: 0.5, level: 0.5 });
    noise(c, o, t, { type: "lowpass", from: 2500, to: 300, len: 0.6, level: 0.45 });
    for (let i = 0; i < 10; i++) noise(c, o, t + 0.25 + Math.random() * 0.8, { type: "highpass", from: 4000, len: 0.025, level: 0.12 });
  }],
  [/cañón de confeti/, (c, o, t) => {
    tone(c, o, t, { from: 300, to: 80, len: 0.15, level: 0.6 });
    noise(c, o, t, { from: 1500, to: 400, len: 0.5, q: 0.8, level: 0.35 });
  }],
  [/bengalas/, (c, o, t) => {
    for (let i = 0; i < 60; i++) noise(c, o, t + Math.random() * 2.4, { type: "highpass", from: 5000, len: 0.02, level: 0.06 });
  }],
  [/estrellas/, (c, o, t) => {
    [88, 91, 95, 100, 96, 93].forEach((m, i) => tone(c, o, t + i * 0.28, { from: hz(m), len: 0.6, level: 0.06 }));
  }],
  [/aplausos/, (c, o, t, n) => applause(c, o, t, n.includes("gran") ? 5 : 3)],
  [/whoosh|swoosh que sube/, (c, o, t, n) =>
    noise(c, o, t, { from: n.includes("sube") ? 400 : 2400, to: n.includes("sube") ? 3000 : 300, len: 0.45, q: 2, attack: 0.15 })],
  [/swoosh|escoba/, (c, o, t) => noise(c, o, t, { from: 3000, to: 500, len: 0.5, q: 1.5, attack: 0.1, level: 0.5 })],
  // The chosen envelope tearing open (UI-11): a short run of crackles, rising.
  [/rasgado/, (c, o, t) => {
    for (let i = 0; i < 5; i++) noise(c, o, t + i * 0.035, { from: 2200 + i * 600, len: 0.06, q: 2, level: 0.32 });
  }],
  [/papel/, (c, o, t) => {
    noise(c, o, t, { from: 5000, len: 0.08, q: 3, level: 0.3 });
    noise(c, o, t + 0.07, { from: 3500, len: 0.12, q: 3, level: 0.25 });
  }],
  [/listo|hola/, (c, o, t) => notes(c, o, t, [72, 76, 79], 0.09, "triangle", 0.5)],
  [/boom|golpe/, (c, o, t) => {
    tone(c, o, t, { from: 140, to: 38, len: 0.6, level: 0.8 });
    noise(c, o, t, { type: "lowpass", from: 900, to: 120, len: 0.35, level: 0.5 });
  }],
  [/bloque (\d+)/, (c, o, t, n) => {
    const level = Number(/bloque (\d+)/.exec(n)?.[1] ?? 1);
    tone(c, o, t, { from: 90 + level * 12, to: 40 + level * 6, len: 0.35, level: 0.7 }); // higher thud, higher tower
    noise(c, o, t, { type: "lowpass", from: 600, len: 0.15, level: 0.3 });
  }],
  [/disparo|corcho/, (c, o, t) => {
    tone(c, o, t, { from: 700, to: 120, len: 0.08, level: 0.5 });
    noise(c, o, t + 0.03, { from: 2500, len: 0.08, q: 2, level: 0.4 });
  }],
  [/pop|carta/, (c, o, t) => tone(c, o, t, { from: 900, to: 300, len: 0.12, level: 0.4 })],
  [/candado: clunk|candado se cierra/, (c, o, t) => {
    tone(c, o, t, { type: "square", from: 180, to: 90, len: 0.12, level: 0.18 });
    noise(c, o, t, { from: 1800, len: 0.06, q: 4, level: 0.3 });
  }],
  [/candado se abre/, (c, o, t) => {
    noise(c, o, t, { from: 3000, len: 0.04, q: 6, level: 0.3 });
    noise(c, o, t + 0.09, { from: 4200, len: 0.05, q: 6, level: 0.35 });
    tone(c, o, t + 0.1, { from: 1320, len: 0.25, level: 0.12 });
  }],
  [/fanfarria/, (c, o, t) => {
    notes(c, o, t, [60, 64, 67], 0.11, "sawtooth", 0.3);
    [72, 76, 79].forEach((m) => tone(c, o, t + 0.36, { type: "triangle", from: hz(m), len: 1.1, level: 0.2 }));
  }],
  [/trombón|Ups/, (c, o, t) => {
    [58, 57, 56].forEach((m, i) => tone(c, o, t + i * 0.32, { type: "sawtooth", from: hz(m), len: 0.32, level: 0.16 }));
    tone(c, o, t + 0.96, { type: "sawtooth", from: hz(55), to: hz(53), len: 0.9, level: 0.16 });
  }],
  [/rebobinar/, (c, o, t) => {
    tone(c, o, t, { type: "sawtooth", from: 1200, to: 150, len: 0.5, level: 0.12 });
    noise(c, o, t, { from: 2000, to: 600, len: 0.5, q: 0.7, level: 0.25 });
  }],
  [/menú abierto/, (c, o, t) => tone(c, o, t, { from: 500, to: 900, len: 0.12, level: 0.2 })],
  [/menú cerrado/, (c, o, t) => tone(c, o, t, { from: 900, to: 500, len: 0.12, level: 0.2 })],
  [/desbloqueado/, (c, o, t) => tone(c, o, t, { from: 880, len: 0.15, level: 0.12 })],
  [/comodín: preparado/, (c, o, t) => notes(c, o, t, [84, 88], 0.06, "sine", 0.25)],
  [/comodín: abrir/, (c, o, t) => notes(c, o, t, [76, 81], 0.07, "triangle", 0.3)],
  [/comodín/, (c, o, t) => {
    // The activate shimmer: a quick rising sparkle.
    [79, 83, 86, 91, 95].forEach((m, i) => tone(c, o, t + i * 0.05, { from: hz(m), len: 0.3, level: 0.12 }));
  }],
  [/silbato/, (c, o, t) => tone(c, o, t, { from: 1800, to: 380, len: 0.8, level: 0.2, attack: 0.05 })],
  [/sello/, (c, o, t) => {
    tone(c, o, t, { from: 160, to: 50, len: 0.3, level: 0.8 });
    noise(c, o, t, { type: "lowpass", from: 1200, len: 0.12, level: 0.5 });
  }],
  [/trituradora/, (c, o, t) => {
    noise(c, o, t, { from: 700, len: 1.0, q: 0.8, level: 0.35, attack: 0.05 });
    tone(c, o, t, { type: "sawtooth", from: 55, len: 1.0, level: 0.08, attack: 0.05 });
  }],
  [/latido/, (c, o, t) => {
    tone(c, o, t, { from: 70, to: 45, len: 0.18, level: 0.7 });
    tone(c, o, t + 0.22, { from: 60, to: 40, len: 0.18, level: 0.5 });
  }],
  [/mira: tic/, (c, o, t) => noise(c, o, t, { type: "highpass", from: 6000, len: 0.03, level: 0.3 })],
  [/vidrio/, (c, o, t) => {
    for (let i = 0; i < 7; i++) {
      tone(c, o, t + i * 0.035, { from: 2200 + Math.random() * 3000, len: 0.18, level: 0.1 });
      noise(c, o, t + i * 0.03, { type: "highpass", from: 5000, len: 0.06, level: 0.2 });
    }
  }],
];
