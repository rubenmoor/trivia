// Node APIs of the engine tests, supply.ts and sim/ (tsconfig.node.json); no @types/node (minimal dependencies).
declare module "node:test" {
  export function test(name: string, fn: () => void | Promise<void>): void;
}
declare module "node:assert/strict" {
  interface Assert {
    ok(value: unknown, message?: string): asserts value;
    equal(actual: unknown, expected: unknown, message?: string): void;
    notEqual(actual: unknown, expected: unknown, message?: string): void;
    deepEqual(actual: unknown, expected: unknown, message?: string): void;
    notDeepEqual(actual: unknown, expected: unknown, message?: string): void;
    throws(fn: () => unknown, expected?: RegExp | string): void;
  }
  const assert: Assert;
  export default assert;
}
declare module "node:fs" {
  export function readFileSync(fd: number, encoding: "utf8"): string;
}
interface ImportMeta {
  readonly dirname: string;
}
interface NodeProcess {
  stdout: { write(text: string): boolean };
}
