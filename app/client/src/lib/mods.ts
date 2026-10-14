// Code add-ons (plan 117, decision 131): the shell's /mods.js, each mod's style and entry, `window.trivia`.
// No stability promise: members and module paths may change between versions.
import { flushSync, mount, unmount } from "svelte";
import * as game from "../engine/game.ts";
import { music, sfx } from "../game/sound.svelte.ts";
import * as api from "./api.ts";
import { buildInfo } from "./build.ts";
import { read, run } from "./engine.ts";
import { messageOf } from "./http.ts";
import { fill, lang, t } from "./i18n.ts";
import { lastDevice, pushScope } from "./input.svelte.ts";

export interface ModInfo {
  id: string;
  name: string;
  version: string;
}

/** A row of /mods.js (mods.mjs `modsScript`), in run order: bottom of the load order first. */
interface ModRow extends ModInfo {
  entry: string | null;
  style: string | null;
}

export type ModErrorCode = "load_failed" | "setup_failed" | "timeout" | "hook_failed";

export interface ModError {
  id: string;
  code: ModErrorCode;
  message: string;
}

/** Event payloads, `structuredClone`d per listener. */
export interface ModEvents {
  /** After the game is mounted. */
  ready: Record<string, never>;
}

/** Same instances as importing our modules by path (`/lib/api.js`); exports are read-only. */
export interface ModModules {
  api: typeof api;
  /** A mod's own route over save + data. */
  engine: { read: typeof read; run: typeof run };
  game: typeof game;
  i18n: { t: typeof t; readonly lang: string; fill: typeof fill };
  input: { pushScope: typeof pushScope; lastDevice: typeof lastDevice };
  sound: { sfx: typeof sfx; music: typeof music };
  /** Our Svelte runtime: compiled mod components import `/vendor/svelte/…`, not their own. */
  svelte: { mount: typeof mount; unmount: typeof unmount; flushSync: typeof flushSync };
}

/** `window.trivia`; `setup(trivia)` gets a view scoped to its mod (`mod` set, registrations tagged). */
export interface TriviaApi {
  version: string;
  mods: ModInfo[];
  mod?: ModInfo;
  modules: ModModules;
  on<E extends keyof ModEvents>(event: E, fn: (payload: ModEvents[E]) => void): () => void;
  /** A stylesheet after ours: `trivia.css(new URL("./x.css", import.meta.url))`. */
  css(href: string | URL): void;
}

declare global {
  interface Window {
    trivia?: TriviaApi;
  }
}

/** A mod's hook; removed when its mod fails or the hook throws. */
export interface Registration<F = unknown> {
  mod: string;
  kind: string;
  fn: F;
}

const TIMEOUT_MS = 5000;
/** Served by the shell only (resolve.mjs). */
const MODS_JS = "/mods.js";
const loaded: ModInfo[] = [];
const errors: ModError[] = [];
const failed = new Set<string>();
let regs: Registration[] = [];
/** The mod whose entry runs now: registrations through the global view are tagged with it. */
let current: string | null = null;

/** Mods whose entry (if any) set up fine, in run order (achievements, plan 118). */
export const loadedMods = (): readonly ModInfo[] => loaded;
/** Failures this run (mods screen, plan 118). */
export const modErrors = (): readonly ModError[] => errors;

function report(id: string, code: ModErrorCode, e: unknown): void {
  errors.push({ id, code, message: messageOf(e) });
  console.error(`mod ${id}: ${code}`, e);
}

/** Registrations of a kind, in run order (top mod last). */
export function registrations<F>(kind: string): Registration<F>[] {
  return regs.filter((r) => r.kind === kind) as Registration<F>[];
}

function register(mod: string, kind: string, fn: unknown): () => void {
  if (failed.has(mod)) return () => {};
  const reg: Registration = { mod, kind, fn };
  regs.push(reg);
  return () => {
    regs = regs.filter((r) => r !== reg);
  };
}

/** A hook threw: report it and drop that registration for the rest of the run. */
export function hookFailed(reg: Registration, e: unknown): void {
  report(reg.mod, "hook_failed", e);
  regs = regs.filter((r) => r !== reg);
}

/** Calls each listener with its own copy of the payload. */
export function emit<E extends keyof ModEvents>(event: E, payload: ModEvents[E]): void {
  for (const reg of registrations<(p: ModEvents[E]) => unknown>(`on:${event}`)) {
    try {
      const out = reg.fn(structuredClone(payload));
      if (out instanceof Promise) out.catch((e: unknown) => hookFailed(reg, e));
    } catch (e) {
      hookFailed(reg, e);
    }
  }
}

/** In `<body>`: after our `<head>` CSS, also the component CSS that loads with the game. */
function linkStyle(href: string | URL): void {
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = String(href);
  document.body.append(link);
}

const modules: ModModules = {
  api,
  engine: { read, run },
  game,
  i18n: {
    t,
    get lang() {
      return lang;
    },
    fill,
  },
  input: { pushScope, lastDevice },
  sound: { sfx, music },
  svelte: { mount, unmount, flushSync },
};

function view(mod: ModInfo | null): TriviaApi {
  const tag = () => mod?.id ?? current ?? "unknown";
  return {
    version: buildInfo().version,
    mods: loaded,
    ...(mod && { mod }),
    modules,
    on: (event, fn) => register(tag(), `on:${event}`, fn),
    css: linkStyle,
  };
}

async function fetchList(): Promise<ModRow[]> {
  try {
    const m = (await import(/* @vite-ignore */ MODS_JS)) as { default?: ModRow[] };
    return Array.isArray(m.default) ? m.default : [];
  } catch {
    return []; // outside the shell: no mods
  }
}

async function start(row: ModRow, mod: ModInfo): Promise<void> {
  if (!row.entry) return;
  let entry: { default?: unknown };
  try {
    entry = (await import(/* @vite-ignore */ row.entry)) as { default?: unknown };
  } catch (e) {
    throw Object.assign(new Error(messageOf(e)), { code: "load_failed" });
  }
  if (typeof entry.default !== "function") return;
  try {
    await (entry.default as (trivia: TriviaApi) => unknown)(view(mod));
  } catch (e) {
    throw Object.assign(new Error(messageOf(e)), { code: "setup_failed" });
  }
}

/** main.ts, before data and language load: each mod's style, then its entry's `setup(trivia)`. */
export async function loadMods(): Promise<void> {
  const rows = await fetchList();
  window.trivia = view(null);
  for (const row of rows) {
    const mod = { id: row.id, name: row.name, version: row.version };
    if (row.style) linkStyle(row.style);
    current = row.id;
    let timer = 0;
    const timeout = new Promise<never>((_, reject) => {
      timer = window.setTimeout(() => reject(Object.assign(new Error(`no setup after ${TIMEOUT_MS} ms`), { code: "timeout" })), TIMEOUT_MS);
    });
    try {
      await Promise.race([start(row, mod), timeout]);
      loaded.push(mod);
    } catch (e) {
      failed.add(row.id);
      regs = regs.filter((r) => r.mod !== row.id);
      report(row.id, (e as { code?: ModErrorCode }).code ?? "setup_failed", e);
    } finally {
      clearTimeout(timer);
    }
  }
  current = null;
}
