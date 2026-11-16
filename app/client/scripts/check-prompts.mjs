#!/usr/bin/env node
// Every action button shows how to reach it by keyboard or pad (plans/14-input.md, IN-5; task 2119): a `candy`,
// `secondary` or `danger` button in the game's markup must hold a <Prompt>. Icon-only controls (tiles, trash, steps) are
// reached by arrows and Space, so they're exempt.
// Usage: node scripts/check-prompts.mjs [path…]  (default src/game; relative to app/client)
import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const ACTION = /\bclass="[^"]*\b(candy|secondary|danger)\b/;

function files(path) {
  if (statSync(path).isFile()) return [path];
  return readdirSync(path)
    .sort()
    .flatMap((f) => files(join(path, f)))
    .filter((f) => f.endsWith(".svelte"));
}

const args = process.argv.slice(2);
let failed = 0;
for (const file of (args.length ? args : ["src/game"]).map((p) => resolve(root, p)).flatMap(files)) {
  const src = readFileSync(file, "utf8");
  for (const m of src.matchAll(/<button\b[\s\S]*?<\/button>/g)) {
    if (!ACTION.test(m[0]) || /<Prompt\b/.test(m[0])) continue;
    failed++;
    console.log(`${relative(root, file)}:${src.slice(0, m.index).split("\n").length}: action button without a <Prompt>`);
  }
}
if (failed) {
  console.log(`check-prompts: ${failed} button(s) without a key prompt`);
  process.exit(1);
}
console.log("check-prompts: every action button shows its key");
