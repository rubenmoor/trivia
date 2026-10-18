import type { EngineData } from "./state.ts";

// Referee randomness (D-58): every shuffle goes through an injected Rng.
export interface Rng {
  // In place; site: the caller's tape label (fixtures/README.md).
  shuffle<T>(xs: T[], site: string): void;
}

function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function fisherYates<T>(xs: T[], next: () => number): void {
  for (let i = xs.length - 1; i > 0; i--) {
    const j = Math.floor(next() * (i + 1));
    [xs[i], xs[j]] = [xs[j], xs[i]];
  }
}

// mulberry32 + Fisher–Yates.
export function seededRng(seed: number): Rng {
  const next = mulberry32(seed);
  return { shuffle: (xs) => fisherYates(xs, next) };
}

const DEMO_SALT = "trivia-demo-1";

/** FNV-1a, 32 bit. */
function fnv1a(s: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 0x01000193);
  return h >>> 0;
}

const keyOf = (x: unknown): string =>
  (x && typeof x === "object" && "id" in x ? String(x.id) : String(x));

/** Demo (decision 340): each shuffle seeded from the salt, its site and its items; no state. */
function demoRng(): Rng {
  return {
    shuffle: (xs, site) => fisherYates(xs, mulberry32(fnv1a([DEMO_SALT, site, ...xs.map(keyOf)].join("\u0000")))),
  };
}

/** An action's rng: fixed in the demo, fresh randomness otherwise. */
export function actionRng(data: Pick<EngineData, "demo">): Rng {
  return data.demo ? demoRng() : seededRng(randomSeed());
}

function randomSeed(): number {
  return crypto.getRandomValues(new Uint32Array(1))[0];
}
