// The few Node APIs credits.ts and vite.config.ts use; no @types/node (minimal dependencies).
declare module "node:fs" {
  export function existsSync(path: string): boolean;
  export function readdirSync(path: string): string[];
  export function readFileSync(path: string, encoding: "utf8"): string;
}
declare module "node:url" {
  export function fileURLToPath(url: URL): string;
}
