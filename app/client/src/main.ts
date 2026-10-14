import { mount } from "svelte";
import "./app.css";
import { language } from "./lib/engine.ts";
import { mods } from "./lib/desktop.ts";
import { initDocument, initLang } from "./lib/i18n.ts";
import { emit, loadMods } from "./lib/mods.ts";

// Mods first: their setup registers hooks before data and language load (decision 131).
await loadMods();
// The save's UI language before any game module runs `t()` (plan 68); a failed load shows up in the game.
const ui = await language().then((l) => l.language, () => undefined);
await initLang(ui);
initDocument();
const { default: App } = await import("./App.svelte");
mount(App, { target: document.getElementById("app")! });
emit("ready", {});
// Start confirmed: the shell's crash marker goes (plan 118).
void mods?.ready();
