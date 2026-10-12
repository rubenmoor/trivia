#!/usr/bin/env node
// Flags on-screen literals outside the catalog (plans/15a-ui-translation.md, LUI-1).
// Usage: node scripts/check-literals.mjs [path…]  (default src/game; relative to app/client)
import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SPANISH = /[áéíóúñÁÉÍÓÚÑ¡¿]/;
const LETTER = /\p{L}/u;
const ATTRS = /\b(aria-label|title|placeholder)\s*=\s*("[^"]*"|'[^']*')/g;

/** Same length, newlines kept, so offsets and line numbers stay. */
const blank = (s) => s.replace(/[^\n]/g, " ");

function files(path) {
  if (statSync(path).isFile()) return [path];
  return readdirSync(path)
    .sort()
    .flatMap((f) => files(join(path, f)))
    .filter((f) => /\.(svelte|ts|js|mjs)$/.test(f) && !/\.test\.ts$/.test(f));
}

/** Blanks `//` and `/* *\/` comments in JS/TS; strings and template literals stay. */
function stripJs(src) {
  let out = "";
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === "/" && src[i + 1] === "/") {
      const end = src.indexOf("\n", i);
      const j = end < 0 ? src.length : end;
      out += blank(src.slice(i, j));
      i = j;
    } else if (c === "/" && src[i + 1] === "*") {
      const end = src.indexOf("*/", i + 2);
      const j = end < 0 ? src.length : end + 2;
      out += blank(src.slice(i, j));
      i = j;
    } else if (c === '"' || c === "'" || c === "`") {
      let j = i + 1;
      while (j < src.length && src[j] !== c && !(c !== "`" && src[j] === "\n")) j += src[j] === "\\" ? 2 : 1;
      out += src.slice(i, j + 1);
      i = j + 1;
    } else {
      out += c;
      i++;
    }
  }
  return out;
}

/** Blanks balanced `{…}` expressions (string-aware); returns the markup without them. */
function stripExpressions(src) {
  let out = "";
  let depth = 0;
  let quote = null;
  for (let i = 0; i < src.length; i++) {
    const c = src[i];
    if (depth === 0) {
      if (c === "{") depth = 1, (out += " ");
      else out += c;
      continue;
    }
    if (quote) {
      if (c === "\\") (out += blank(src.slice(i, i + 2))), i++;
      else {
        if (c === quote) quote = null;
        out += blank(c);
      }
      continue;
    }
    if (c === '"' || c === "'" || c === "`") quote = c;
    else if (c === "{") depth++;
    else if (c === "}") depth--;
    out += blank(c);
  }
  return out;
}

function lineAt(src, offset) {
  return src.slice(0, offset).split("\n").length;
}

function check(path) {
  const raw = readFileSync(path, "utf8");
  const hits = [];
  let code;
  if (path.endsWith(".svelte")) {
    // <style> is not text; <script> is JS; the rest is markup.
    const SCRIPT = /(<script[^>]*>)([\s\S]*?)(<\/script>)/g;
    const base = raw.replace(/<style[\s\S]*?<\/style>/g, blank);
    code = base
      .replace(SCRIPT, (_, a, body, b) => blank(a) + stripJs(body) + blank(b))
      .replace(/<!--[\s\S]*?-->/g, blank);
    const markup = stripExpressions(base.replace(SCRIPT, blank).replace(/<!--[\s\S]*?-->/g, blank));
    for (const m of markup.matchAll(/<[a-zA-Z/!][^>]*>/g)) {
      for (const a of m[0].matchAll(ATTRS))
        if (LETTER.test(a[2])) hits.push([m.index + a.index, `${a[1]}=${a[2].replace(/\s+/g, " ")}`]);
    }
    // <kbd> holds key names (Enter, Esc), not text (LUI-4).
    const text = markup.replace(/<kbd>[^<]*<\/kbd>/g, blank).replace(/<[a-zA-Z/!][^>]*>/g, blank);
    for (const m of text.matchAll(/[^\s]+(?:[ \t]+[^\s]+)*/g))
      if (LETTER.test(m[0])) hits.push([m.index, `text "${m[0].replace(/\s+/g, " ")}"`]);
  } else code = stripJs(raw);
  for (const m of code.matchAll(new RegExp("[^\\n]*" + SPANISH.source + "[^\\n]*", "g")))
    hits.push([m.index, `Spanish "${m[0].trim().slice(0, 80)}"`]);
  return hits.map(([offset, what]) => ({ line: lineAt(raw, offset), what }));
}

const args = process.argv.slice(2);
const paths = (args.length ? args : ["src/game"]).map((p) => resolve(root, p));
let failed = 0;
for (const file of paths.flatMap(files)) {
  const seen = new Set();
  for (const { line, what } of check(file).sort((a, b) => a.line - b.line)) {
    if (seen.has(line + what)) continue;
    seen.add(line + what);
    console.log(`${relative(process.cwd(), file)}:${line}: ${what}`);
    failed++;
  }
}
if (failed) {
  console.error(`${failed} literal(s) outside the catalog (src/locales/es.ts).`);
  process.exit(1);
}
