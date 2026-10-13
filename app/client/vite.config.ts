import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { credits } from "./credits.ts";

// In development, /api, /data and cached media go to the Python server (app/server/main.py).
const backend = "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [svelte(), credits()],
  server: {
    proxy: { "/api": backend, "/data": backend, "/media": backend },
  },
});
