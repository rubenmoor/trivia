#!/usr/bin/env node
// Every action button shows how to reach it (plans/14-input.md, section 4; decision 671): a `candy`, `secondary` or
// `danger` button in the game's markup holds a <Prompt> with its one fixed shortcut, unless it's `data-ringed`: one of
// several alike (a list's rows), reached by the ring and Space/X. Icon-only controls (tiles, trash, steps) are exempt.
// A chip never names `press` (Space/X is no shortcut) and no prop may tie it to focus.
// Usage: node scripts/check-prompts.mjs [path…]  (default src/game; relative to app/client)
import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const ACTION = /\bclass="[^"]*\b(candy|secondary|danger)\b/;
const BAD_PROMPT = /<Prompt\b[^>]*\b(action="press"|fixed|focused|ringed)\b/;

function files(path) {
  if (statSync(path).isFile()) return [path];
  return readdirSync(path)
    .sort()
    .flatMap((f) => files(join(path, f)))
    .filter((f) => f.endsWith(".svelte"));
}

const args = process.argv.slice(2);
let failed = 0;
const line = (src, at) => src.slice(0, at).split("\n").length;
for (const file of (args.length ? args : ["src/game"]).map((p) => resolve(root, p)).flatMap(files)) {
  const src = readFileSync(file, "utf8");
  for (const m of src.matchAll(/<button\b[\s\S]*?<\/button>/g)) {
    if (!ACTION.test(m[0]) || /<Prompt\b/.test(m[0]) || /\bdata-ringed\b/.test(m[0])) continue;
    failed++;
    console.log(`${relative(root, file)}:${line(src, m.index)}: action button without a <Prompt>`);
  }
  for (const m of src.matchAll(/<Prompt\b[^>]*>/g)) {
    if (!BAD_PROMPT.test(m[0])) continue;
    failed++;
    console.log(`${relative(root, file)}:${line(src, m.index)}: a chip is a fixed shortcut, never Space or focus-bound: ${m[0]}`);
  }
}
if (failed) {
  console.log(`check-prompts: ${failed} problem(s)`);
  process.exit(1);
}
console.log("check-prompts: every action button shows its fixed key");
