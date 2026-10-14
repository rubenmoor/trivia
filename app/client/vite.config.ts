import { defineConfig, type Plugin } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { globSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { credits } from "./credits.ts";

// In development, /api, /data and cached media go to the Python server (app/server/main.py).
const backend = "http://127.0.0.1:8000";

// The game version's single source (D-91).
const version = (JSON.parse(readFileSync(fileURLToPath(new URL("../desktop/package.json", import.meta.url)), "utf8")) as { version: string }).version;

const client = fileURLToPath(new URL(".", import.meta.url));
const src = `${client}src/`;

/** Readable build (decision 124): output path = source path; `vendor/<pkg>/…` for packages; null: keep Rolldown's name. */
function outPath(id: string | null | undefined, ext: string): string | null {
  if (!id || id.includes("?") || id.startsWith("\0")) return null;
  const pkg = id.lastIndexOf("/node_modules/");
  const rel = pkg >= 0 ? `vendor/${id.slice(pkg + 14)}` : id.startsWith(src) ? id.slice(src.length) : null;
  return rel && `${rel.replace(/\.(ts|js|mjs)$/, "")}${ext}`;
}

/** Every shipped source module, so each keeps all its exports for mods' by-path imports (task 1005). */
const modules = Object.fromEntries(
  globSync("**/*.{ts,svelte}", { cwd: src, exclude: ["**/*.test.ts", "**/*.d.ts", "engine/test/**", "locales/xx.ts"] }).map((f) => [f, `${src}${f}`]),
);

/** Only `/main.js` as a module script: the browser follows its imports. */
function oneEntryScript(): Plugin {
  return {
    name: "trivia-one-entry-script",
    transformIndexHtml: {
      order: "post",
      handler: (html) => html.replace(/\s*<script type="module" crossorigin src="(?!\/main\.js")[^"]*"><\/script>/g, ""),
    },
  };
}

export default defineConfig({
  define: { __APP_VERSION__: JSON.stringify(version) },
  plugins: [svelte(), credits(), oneEntryScript()],
  build: {
    minify: false,
    sourcemap: true,
    cssCodeSplit: true,
    modulePreload: false,
    rolldownOptions: {
      // Our modules and Svelte's runtime with every export: mods import them by path (plan 117, decision 145).
      input: {
        index: `${client}index.html`,
        ...modules,
        "svelte-index": "svelte",
        "svelte-client": "svelte/internal/client",
        "svelte-version": "svelte/internal/disclose-version",
      },
      preserveEntrySignatures: "strict",
      output: {
        preserveModules: true,
        preserveModulesRoot: "src",
        entryFileNames: (c) => outPath(c.facadeModuleId, ".js") ?? "[name].js",
        chunkFileNames: (c) => outPath(c.facadeModuleId, ".js") ?? "[name].js",
        // Component CSS: `game/Game.svelte?svelte&type=style&lang.css` → `game/Game.svelte.css`.
        assetFileNames: (a) => {
          const from = a.originalFileNames[0]?.replace(/\?.*$/, "");
          const path = from && outPath(`${client}${from}`, "");
          const ext = a.names[0]?.match(/\.[^./]+$/)?.[0] ?? "";
          return path ? (path.endsWith(ext) ? path : path + ext) : "[name][extname]";
        },
      },
    },
  },
  server: {
    proxy: { "/api": backend, "/data": backend, "/media": backend },
  },
});
