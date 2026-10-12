import { mount } from "svelte";
import "./app.css";
import { language } from "./lib/engine";
import { initDocument, initLang } from "./lib/i18n";

// The save's UI language before any game module runs `t()` (plan 68); a failed load shows up in the game.
const ui = await language().then((l) => l.language.ui, () => undefined);
await initLang(ui);
initDocument();
const { default: App } = await import("./App.svelte");
mount(App, { target: document.getElementById("app")! });
