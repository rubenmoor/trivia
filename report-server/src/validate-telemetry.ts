// Body checks of `POST /telemetry` (plan 105 "API contract"); pure, no Worker APIs.
// The result holds known fields only: unknown fields never reach the stored body.
import { isObj, LANG, parseJson, validTicket, VERSION, type Rejected } from "./validate";

export const MAX_TELEMETRY_BODY = 64 * 1024;
/** `GET /telemetry` page and ack maximum. */
export const TELEMETRY_PAGE = 200;

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

type Jokers = Record<string, number>;

export interface Answer {
  question: string;
  level: number;
  correct: boolean;
  jokers: Jokers;
}

export interface Game {
  mode: string;
  locale: string;
  pool: string | null;
  age_group: string | null;
  difficulty: { start: number; end: number } | null;
  levels: number;
  reached: number;
  result: string;
  customized: boolean;
  mods: boolean;
  /** Seats in the session (milestone 16); missing = 1. */
  players: number;
  jokers: Jokers;
  answers: Answer[];
}

/** The stored body: everything but the ticket. */
export interface Session {
  session: string;
  install: string;
  version: string;
  length_s: number;
  games: Game[];
}

export type CheckedTelemetry = { ok: true; session: Session; ticket: string } | Rejected;

class Bad extends Error {
  readonly field: string;
  constructor(field: string) {
    super(field);
    this.field = field;
  }
}

type Obj = Record<string, unknown>;

function obj(v: unknown, path: string): Obj {
  if (!isObj(v)) throw new Bad(path);
  return v;
}

function str(v: unknown, re: RegExp, path: string, max = 64): string {
  if (typeof v !== "string" || v.length > max || !re.test(v)) throw new Bad(path);
  return v;
}

function int(v: unknown, min: number, max: number, path: string): number {
  if (!Number.isInteger(v) || (v as number) < min || (v as number) > max) throw new Bad(path);
  return v as number;
}

function bool(v: unknown, path: string): boolean {
  if (typeof v !== "boolean") throw new Bad(path);
  return v;
}

function arr(v: unknown, max: number, path: string): unknown[] {
  if (!Array.isArray(v) || v.length > max) throw new Bad(path);
  return v;
}

function jokers(v: unknown, path: string): Jokers {
  const o = obj(v, path);
  const keys = Object.keys(o);
  if (keys.length > 8) throw new Bad(path);
  const out: Jokers = {};
  for (const k of keys) out[str(k, /^[a-z]{1,16}$/, path)] = int(o[k], 0, 99, `${path}.${k}`);
  return out;
}

function game(v: unknown, path: string): Game {
  const g = obj(v, path);
  const levels = int(g["levels"], 1, 20, `${path}.levels`);
  const ageGroup = g["age_group"] ?? null;
  const diff = g["difficulty"] ?? null;
  if ((ageGroup === null) === (diff === null)) throw new Bad(`${path}.age_group`);
  let difficulty: Game["difficulty"] = null;
  if (diff !== null) {
    const d = obj(diff, `${path}.difficulty`);
    const start = int(d["start"], 1, 15, `${path}.difficulty.start`);
    difficulty = { start, end: int(d["end"], start, 15, `${path}.difficulty.end`) };
  }
  return {
    mode: str(g["mode"], /^[a-z][a-z-]{0,23}$/, `${path}.mode`),
    locale: str(g["locale"], LANG, `${path}.locale`, 16),
    pool: g["pool"] === null ? null : str(g["pool"], /^[0-9a-f]{8}$/, `${path}.pool`),
    age_group: ageGroup === null ? null : str(ageGroup, /^[a-z_]{1,24}$/, `${path}.age_group`),
    difficulty,
    levels,
    reached: int(g["reached"], 0, levels, `${path}.reached`),
    result: str(g["result"], /^(won|lost|completed|abandoned|open)$/, `${path}.result`),
    customized: bool(g["customized"], `${path}.customized`),
    mods: bool(g["mods"], `${path}.mods`),
    players: g["players"] === undefined ? 1 : int(g["players"], 1, 64, `${path}.players`),
    jokers: jokers(g["jokers"], `${path}.jokers`),
    answers: arr(g["answers"], 100, `${path}.answers`).map((a, i) => {
      const p = `${path}.answers[${i}]`;
      const o = obj(a, p);
      return {
        question: str(o["question"], /^q-\d{4,6}$/, `${p}.question`),
        level: int(o["level"], 1, levels, `${p}.level`),
        correct: bool(o["correct"], `${p}.correct`),
        jokers: jokers(o["jokers"], `${p}.jokers`),
      };
    }),
  };
}

/** Content type, size, JSON, fields. `dev` also takes `dev-*` tickets (fake check). */
export function checkTelemetry(contentType: string | null, body: Uint8Array, dev = false): CheckedTelemetry {
  if (!/^application\/json\s*(;|$)/i.test(contentType ?? "")) return { ok: false, status: 415 };
  if (body.byteLength > MAX_TELEMETRY_BODY) return { ok: false, status: 413 };
  const data = parseJson(body);
  if (data === undefined) return { ok: false, status: 400 };
  try {
    const o = obj(data, "");
    const session: Session = {
      session: str(o["session"], UUID, "session"),
      install: str(o["install"], UUID, "install"),
      version: str(o["version"], VERSION, "version", 32),
      length_s: int(o["length_s"], 0, 86_400, "length_s"),
      games: arr(o["games"], 30, "games").map((g, i) => game(g, `games[${i}]`)),
    };
    if (session.games.reduce((n, g) => n + g.answers.length, 0) > 500) throw new Bad("games");
    const ticket = o["ticket"];
    if (!validTicket(ticket, dev)) throw new Bad("ticket");
    return { ok: true, session, ticket };
  } catch (e) {
    if (e instanceof Bad) return e.field ? { ok: false, status: 400, field: e.field } : { ok: false, status: 400 };
    throw e;
  }
}

/** `POST /telemetry/ack` body: 1–`TELEMETRY_PAGE` session UUIDs, else null. */
export function checkTelemetryAck(body: Uint8Array): string[] | null {
  const data = parseJson(body);
  const ids = isObj(data) ? data["sessions"] : undefined;
  if (!Array.isArray(ids) || ids.length < 1 || ids.length > TELEMETRY_PAGE || !ids.every((i) => typeof i === "string" && UUID.test(i))) return null;
  return ids as string[];
}
