import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { credits } from "./credits.ts";

// In development, /api, /data and cached media go to the Python server (app/server/main.py).
const backend = "http://127.0.0.1:8000";

// The game version's single source (D-91).
const version = (JSON.parse(readFileSync(fileURLToPath(new URL("../desktop/package.json", import.meta.url)), "utf8")) as { version: string }).version;

export default defineConfig({
  define: { __APP_VERSION__: JSON.stringify(version) },
  plugins: [svelte(), credits()],
  server: {
    proxy: { "/api": backend, "/data": backend, "/media": backend },
  },
});
