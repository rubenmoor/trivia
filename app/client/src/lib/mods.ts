// Code add-ons (plan 117, decision 131): the shell's /mods.js, each mod's style and entry, `window.trivia`.
// No stability promise: members and module paths may change between versions.
import { flushSync, mount, unmount } from "svelte";
import * as game from "../engine/game.ts";
import { music, sfx } from "../game/sound.svelte.ts";
import * as api from "./api.ts";
import type { AgeGroup, Bundle, PoolQuestion } from "../engine/pool.ts";
import { buildInfo } from "./build.ts";
import { read, run } from "./engine.ts";
import { messageOf } from "./http.ts";
import { addCatalog, fill, lang, t } from "./i18n.ts";
import { lastDevice, pushScope } from "./input.svelte.ts";
import type { Game } from "./types.ts";

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
  /** After a screen switch; `name` as in `game/screens/` (`Question`). */
  screen: { name: string };
  /** After a successful `new`. */
  "game:start": { game: Game };
  /** A game's `result` went from null to won/lost/abandoned (a `new` abandons the running game). */
  "game:end": { game: Game; result: NonNullable<Game["result"]> };
  /** The Question screen is shown, its media ready. */
  "question:shown": { id: string; level: number };
  /** After `answer`; `index` as chosen. */
  "question:answered": { id: string; level: number; index: number; correct: boolean };
}

/** What a data hook sees per locale load; mod questions have `<mod id>:<id>` ids (decision 128). */
export interface ModData {
  locale: string;
  questions: PoolQuestion[];
  bundles: Bundle[];
  ageGroups: AgeGroup[];
}

/** Gets a copy: change it in place or return a partial replacement (arrays filtered, mapped, extended). */
export type DataHook = (data: ModData) => Partial<Omit<ModData, "locale">> | void;
/** `action`: a `gameAction` name or `joker`; gets a copy of the body: change it in place or return a new one.
 * The engine still validates it. */
export type BeforeHook = (action: string, body: Record<string, unknown>) => Record<string, unknown> | void;
/** A copy of the game after the action; null after some actions. */
export type AfterHook = (action: string, game: Game | null) => void;

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
  /** Runs per locale load (lib/data.ts), in run order; a throw leaves the data as it was. */
  data(fn: DataHook): () => void;
  /** Around game actions and jokers (lib/api.ts). */
  actions: { before(fn: BeforeHook): () => void; after(fn: AfterHook): () => void };
  i18n: {
    /** A catalog over a UI language (deep merge; `es-ES` is its own), or a new UI language (`opts.endonym`)
     * on `opts.base` (default `en`); question languages stay ours. Call in `setup`: later calls apply after a reload. */
    add(locale: string, catalog: Record<string, unknown>, opts?: { endonym?: string; base?: string }): void;
  };
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
  if (typeof fn !== "function" && kind !== "i18n") throw new TypeError(`${kind}: not a function`);
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

/** A sync hook's result; a Promise counts as a failure. */
function sync(out: unknown): unknown {
  if (out instanceof Promise) throw new TypeError("hook must not be async");
  return out;
}

const isObject = (v: unknown): v is Record<string, unknown> => !!v && typeof v === "object" && !Array.isArray(v);

/** lib/data.ts, before engineData: each data hook on a copy, in run order. */
export function runDataHooks(data: ModData): ModData {
  let out = data;
  for (const reg of registrations<DataHook>("data")) {
    try {
      const copy = structuredClone(out);
      const r = sync(reg.fn(copy));
      const next = { ...copy, ...(isObject(r) ? r : {}), locale: out.locale };
      if (![next.questions, next.bundles, next.ageGroups].every(Array.isArray)) throw new TypeError("data hook: not arrays");
      out = next;
    } catch (e) {
      hookFailed(reg, e);
    }
  }
  return out;
}

/** lib/api.ts: the body after every `before` hook. */
export function runBefore<B extends object>(action: string, body: B): B {
  let out = body;
  for (const reg of registrations<BeforeHook>("actions:before")) {
    try {
      const copy = structuredClone(out) as Record<string, unknown>;
      const r = sync(reg.fn(action, copy));
      if (r !== undefined && !isObject(r)) throw new TypeError("before hook: not an object");
      out = (r ?? copy) as B;
    } catch (e) {
      hookFailed(reg, e);
    }
  }
  return out;
}

/** lib/api.ts: each `after` hook with its own copy of the game. */
export function runAfter(action: string, game: Game | null): void {
  for (const reg of registrations<AfterHook>("actions:after")) {
    try {
      const out: unknown = reg.fn(action, structuredClone(game));
      if (out instanceof Promise) out.catch((e: unknown) => hookFailed(reg, e));
    } catch (e) {
      hookFailed(reg, e);
    }
  }
}

type CatalogReg = { locale: string; catalog: Record<string, unknown>; opts?: { endonym?: string; base?: string } };
let catalogsApplied = false;

function applyCatalog(reg: Registration<CatalogReg>): void {
  try {
    addCatalog(reg.fn.locale, reg.fn.catalog, reg.fn.opts);
  } catch (e) {
    hookFailed(reg, e);
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
    data: (fn) => register(tag(), "data", fn),
    actions: {
      before: (fn) => register(tag(), "actions:before", fn),
      after: (fn) => register(tag(), "actions:after", fn),
    },
    i18n: {
      add(locale, catalog, opts) {
        Intl.getCanonicalLocales(locale);
        if (!isObject(catalog)) throw new TypeError("i18n.add: catalog not an object");
        if (catalogsApplied) addCatalog(locale, catalog, opts);
        else register(tag(), "i18n", { locale, catalog, opts });
      },
    },
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
  // Catalogs of mods that set up fine, before language() and initLang.
  for (const reg of registrations<CatalogReg>("i18n")) applyCatalog(reg);
  catalogsApplied = true;
}
