// The few Node APIs credits.ts, devserver.ts and vite.config.ts use; no @types/node (minimal dependencies).
declare module "node:fs" {
  export function existsSync(path: string): boolean;
  export function readdirSync(path: string): string[];
  export function readFileSync(path: string, encoding: "utf8"): string;
}
declare module "node:url" {
  export function fileURLToPath(url: URL): string;
}
declare module "node:fs" {
  export function mkdtempSync(prefix: string): string;
  export function globSync(pattern: string, options: { cwd: string; exclude: string[] }): string[];
}
declare module "node:os" {
  export function tmpdir(): string;
}
declare module "node:path" {
  export function join(...parts: string[]): string;
}
interface NodeProcess {
  env: Record<string, string | undefined>;
}
declare const process: NodeProcess;
declare const Buffer: { concat(chunks: Uint8Array[]): { toString(encoding: "utf8"): string } };
