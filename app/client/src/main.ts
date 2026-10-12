import { mount } from "svelte";
import "./app.css";
import App from "./App.svelte";
import { initDocument } from "./lib/i18n";

initDocument();
mount(App, { target: document.getElementById("app")! });
