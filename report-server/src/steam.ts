// Steam Web API ticket check (plan 103 "Steam ticket check"); fake `dev-*` tickets behind the dev switch.
// Never logs the key, the ticket or the SteamID.
import type { Env } from "../env";

const AUTH_URL = "https://partner.steam-api.com/ISteamUserAuth/AuthenticateUserTicket/v1/";
const TIMEOUT_MS = 5000;

export type TicketResult = { ok: true; steamid: string } | { ok: false; status: 401 | 502 };

/** Fake check only with `DEV_FAKE_TICKETS == "1"` on localhost/127.0.0.1. */
export function devTickets(env: Env, url: URL): boolean {
  return env.DEV_FAKE_TICKETS === "1" && (url.hostname === "localhost" || url.hostname === "127.0.0.1");
}

/** The ticket's SteamID64, held in memory only for the rate-limit hash. */
export async function checkTicket(ticket: string, env: Env, dev: boolean): Promise<TicketResult> {
  if (dev && ticket.startsWith("dev-")) {
    if (ticket === "dev-invalid") return { ok: false, status: 401 };
    if (ticket === "dev-steamdown") return { ok: false, status: 502 };
    return { ok: true, steamid: `dev:${ticket}` };
  }
  // Half set up: fail safe as 502, not 500.
  if (!env.STEAM_WEB_API_KEY || !env.STEAM_APP_ID) return { ok: false, status: 502 };
  const q = new URLSearchParams({ key: env.STEAM_WEB_API_KEY, appid: env.STEAM_APP_ID, ticket, identity: env.TICKET_IDENTITY });
  let body: unknown;
  try {
    const res = await fetch(`${AUTH_URL}?${q}`, { signal: AbortSignal.timeout(TIMEOUT_MS) });
    if (!res.ok) return { ok: false, status: 502 };
    body = await res.json();
  } catch {
    return { ok: false, status: 502 };
  }
  return ticketResult(body);
}

/** `{response: {params: {result, steamid, publisherbanned, …}}}` or `{response: {error: {…}}}`. */
export function ticketResult(body: unknown): TicketResult {
  const response = isObject(body) ? body["response"] : undefined;
  if (!isObject(response)) return { ok: false, status: 502 };
  if (response["error"] !== undefined) return { ok: false, status: 401 };
  const params = response["params"];
  if (!isObject(params)) return { ok: false, status: 502 };
  if (params["result"] !== "OK" || params["publisherbanned"] === true) return { ok: false, status: 401 };
  const steamid = params["steamid"];
  return typeof steamid === "string" && /^\d{1,20}$/.test(steamid) ? { ok: true, steamid } : { ok: false, status: 502 };
}

const isObject = (v: unknown): v is Record<string, unknown> => typeof v === "object" && v !== null && !Array.isArray(v);

/** HMAC-SHA256(HASH_SALT, SteamID64), hex. */
export async function userHash(salt: string, steamid: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", enc.encode(salt), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(steamid)));
  return Array.from(mac, (b) => b.toString(16).padStart(2, "0")).join("");
}
