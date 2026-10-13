// What a build is (plan 91): game version (D-91) and the current pool's hash (D-92).
import { poolHash } from "./names.svelte.ts";

export interface BuildInfo {
  version: string;
  pool: string | null;
}

export function buildInfo(): BuildInfo {
  return { version: __APP_VERSION__, pool: poolHash() };
}
