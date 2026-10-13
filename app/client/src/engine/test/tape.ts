import type { Rng } from "../rng.ts";

// Recorded Python shuffle (fixtures/README.md): perm[j] = old index now at j.
export interface TapeEntry {
  site: string;
  n: number;
  perm: number[];
}

interface TapeRng extends Rng {
  done(): void;
}

export function tapeRng(tape: TapeEntry[]): TapeRng {
  let pos = 0;
  return {
    shuffle<T>(xs: T[], site: string): void {
      const e = tape[pos];
      if (!e) throw new Error(`tape: missing entry ${pos} (site ${site}, n ${xs.length})`);
      if (e.site !== site) throw new Error(`tape: entry ${pos} site ${e.site}, got ${site}`);
      if (e.n !== xs.length) throw new Error(`tape: entry ${pos} n ${e.n}, got ${xs.length}`);
      pos++;
      const old = xs.slice();
      for (let j = 0; j < xs.length; j++) xs[j] = old[e.perm[j]];
    },
    done(): void {
      if (pos < tape.length) throw new Error(`tape: ${tape.length - pos} leftover entries from ${pos}`);
    },
  };
}
