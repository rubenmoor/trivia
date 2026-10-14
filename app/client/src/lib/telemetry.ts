// Opt-in telemetry recording (plan 106, decisions 119, 121): after each action the page rebuilds this run's
// games from the save and hands them to the shell. Nothing runs without a bridge and a stored yes; errors stay in the console.
import { buildTelemetry, sessionRows, telemetryStart, type Telemetry, type TelemetryGame, type TelemetryStart } from "../engine/telemetry.ts";
import { gameLocale, type EngineData, type SaveData } from "../engine/state.ts";
import { loadEngineData } from "./data.ts";
import { telemetry, type TelemetryState } from "./desktop.ts";
import { modsOn } from "./mods.ts";

const OFF: TelemetryState = { available: false, consent: null };

let state: Promise<TelemetryState> | null = null;
let start: TelemetryStart | null = null;
let buffer: Telemetry | null = null;
let latest: SaveData | null = null;
let chain: Promise<void> = Promise.resolve();

const warn = (e: unknown) => console.warn("telemetry:", e);

/** One step at a time, in order; never rejects. */
function queued(fn: () => Promise<void>): void {
  chain = chain.then(fn).catch(warn);
}

/** Consent and availability, read once per page load (plan 108 asks when `available && consent === null`). */
export function telemetryState(): Promise<TelemetryState> {
  state ??= telemetry
    ? telemetry.state().catch((e) => {
        warn(e);
        return OFF;
      })
    : Promise.resolve(OFF);
  return state;
}

/** Plan 108's setter; a yes mid-run starts the session at the current save. Rejects on a failed call. */
export async function setTelemetryConsent(yes: boolean): Promise<TelemetryState> {
  if (!telemetry) return OFF;
  const next = await telemetry.setConsent(yes);
  state = Promise.resolve(next);
  queued(async () => {
    buffer = null;
    if (next.consent && latest) {
      start = telemetryStart(latest);
      await record(latest);
    }
  });
  return next;
}

/** The engine's save at page load: this run's starting point. */
export function telemetryLoad(save: SaveData): void {
  start ??= telemetryStart(save);
  telemetryCheckpoint(save);
}

/** After an adopted save; fire-and-forget. */
export function telemetryCheckpoint(save: SaveData): void {
  latest = save;
  if (telemetry) queued(() => record(save));
}

async function record(save: SaveData): Promise<void> {
  const { consent } = await telemetryState();
  if (consent !== true || !start || !telemetry) return;
  if (!buffer) {
    const stored = await telemetry.load();
    buffer = stored ? { games: stored.games as TelemetryGame[], index: stored.index } : { games: [], index: [] };
  }
  const locales = new Set(sessionRows(save, buffer, start).flatMap(({ row }) => (row ? [gameLocale(row)] : [])));
  const data = new Map<string, EngineData>(await Promise.all([...locales].map(async (l) => [l, await loadEngineData(l)] as const)));
  const next = buildTelemetry(save, buffer, start, data, modsOn());
  await telemetry.record(next);
  buffer = next;
}
