import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// In development, /api and cached media go to the Python server (server/main.py).
const backend = "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [svelte()],
  server: {
    proxy: { "/api": backend, "/media": backend },
  },
});
