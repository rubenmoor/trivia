import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { fileURLToPath } from "node:url";
import { relative, resolve } from "node:path";

const src = fileURLToPath(new URL("src/", import.meta.url));

export default {
  preprocess: vitePreprocess(),
  compilerOptions: {
    // Scoped class names per component path, stable across CSS edits (decision 124): game/Hud.svelte → svelte-game-hud.
    cssHash: ({ filename }) =>
      `svelte-${relative(src, resolve(filename)).replace(/\.svelte$/, "").replace(/[^A-Za-z0-9]+/g, "-").toLowerCase()}`,
  },
};
