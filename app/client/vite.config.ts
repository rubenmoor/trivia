import { build, defineConfig, type Plugin } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { globSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { credits } from "./credits.ts";
import { devServer } from "./devserver.ts";

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

/** Svelte's runtime as one file, `/vendor/svelte.js` (decision 149): every `svelte`/`svelte/*` import points at it;
 * it re-exports all of `svelte`, `svelte/internal/client` and whatever else we import, one instance (decision 145). */
function svelteRuntime(): Plugin {
  const file = "vendor/svelte.js";
  const entry = "\0trivia-svelte-runtime";
  const used = new Set(["svelte", "svelte/internal/client", "svelte/internal/disclose-version"]);
  return {
    name: "trivia-svelte-runtime",
    enforce: "pre",
    resolveId(id) {
      if (id !== "svelte" && !id.startsWith("svelte/")) return null;
      used.add(id);
      return { id: `/${file}`, external: true };
    },
    async generateBundle() {
      const out = await build({
        configFile: false,
        envFile: false,
        root: client,
        logLevel: "warn",
        plugins: [{
          name: "trivia-svelte-runtime-entry",
          resolveId: (id) => (id === entry ? id : null),
          load: (id) => (id === entry ? [...used].sort().map((s) => `export * from "${s}";`).join("\n") : null),
        }],
        build: {
          write: false,
          minify: false,
          sourcemap: true,
          rolldownOptions: { input: entry, preserveEntrySignatures: "strict", output: { entryFileNames: file } },
        },
      });
      for (const o of (Array.isArray(out) ? out : [out]).flatMap((r) => ("output" in r ? r.output : []))) {
        this.emitFile({ type: "asset", fileName: o.fileName, source: o.type === "chunk" ? o.code : o.source });
      }
    },
  };
}

/** Readable build; `--mode optimized`: Vite's defaults (hashed, minified), to measure the readable build's cost (decision 143). */
export default defineConfig(({ mode }) => ({
  define: { __APP_VERSION__: JSON.stringify(version) },
  plugins: [
    ...(mode === "optimized" ? [] : [{ ...svelteRuntime(), apply: "build" as const }, oneEntryScript()]),
    svelte(),
    credits(),
    devServer(),
  ],
  build: mode === "optimized" ? {} : {
    minify: false,
    sourcemap: true,
    cssCodeSplit: true,
    modulePreload: false,
    rolldownOptions: {
      // Our modules with every export: mods import them by path (plan 117).
      input: { index: `${client}index.html`, ...modules },
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
  server: { port: 5173, strictPort: true },
  preview: { port: 4173, strictPort: true },
}));
