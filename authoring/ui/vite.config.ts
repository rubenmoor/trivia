import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// The authoring pages (D-35). In development, /api and cached media go to the authoring
// server (authoring/server/main.py). `$app` is the game client's source: authoring may use
// the game's code, never the other way round. The game's public/ provides the fonts.
const backend = "http://127.0.0.1:8001";

export default defineConfig({
  plugins: [svelte()],
  resolve: { alias: { $app: fileURLToPath(new URL("../../app/client/src", import.meta.url)) } },
  publicDir: "../../app/client/public",
  server: {
    port: 5174,
    proxy: { "/api": backend, "/media": backend, "/reports": backend },
  },
});
