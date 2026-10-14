// Steam Web API ticket check (plan 103 "Steam ticket check"). Here only the dev fake check;
// the real call: task 866 (Report server: Steam ticket check).
import type { Env } from "../env";

export type TicketResult = { ok: true; steamid: string } | { ok: false; status: 401 | 502 };

/** Fake check only with `DEV_FAKE_TICKETS == "1"` on localhost/127.0.0.1. */
export function devTickets(env: Env, url: URL): boolean {
  return env.DEV_FAKE_TICKETS === "1" && (url.hostname === "localhost" || url.hostname === "127.0.0.1");
}

/** The ticket's SteamID64, held in memory only for the rate-limit hash. */
export async function checkTicket(ticket: string, _env: Env, dev: boolean): Promise<TicketResult> {
  if (dev && ticket.startsWith("dev-")) {
    if (ticket === "dev-invalid") return { ok: false, status: 401 };
    if (ticket === "dev-steamdown") return { ok: false, status: 502 };
    return { ok: true, steamid: `dev:${ticket}` };
  }
  return { ok: false, status: 502 };
}

/** HMAC-SHA256(HASH_SALT, SteamID64), hex. */
export async function userHash(salt: string, steamid: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", enc.encode(salt), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(steamid)));
  return Array.from(mac, (b) => b.toString(16).padStart(2, "0")).join("");
}
