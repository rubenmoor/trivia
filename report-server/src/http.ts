// Helpers shared by the report and telemetry routes.
import type { Env } from "../env";
import type { Rejected } from "./validate";

export const json = (status: number, body: unknown, headers: Record<string, string> = {}): Response =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json; charset=utf-8", ...headers } });

export const error = (status: number, code: string, extra: Record<string, unknown> = {}): Response =>
  json(status, { error: code, ...extra });

export const day = (now: Date): string => now.toISOString().slice(0, 10);

/** A failed body check as its response. */
export function rejected(r: Rejected): Response {
  if (r.status === 413) return error(413, "too_large");
  if (r.status === 415) return error(415, "unsupported_media_type");
  return error(400, "bad_request", r.field ? { field: r.field } : {});
}

/** A failed ticket check as its response. */
export const ticketFailed = (status: 401 | 502): Response =>
  status === 401 ? error(401, "invalid_ticket") : error(502, "steam_unavailable");

/** 429 until the next UTC day. */
export function rateLimited(now: Date): Response {
  const wait = Math.ceil((Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1) - now.getTime()) / 1000);
  return json(429, { error: "rate_limited", retry_after: wait }, { "Retry-After": String(wait) });
}

/** Body up to `max + 1` bytes, so oversize is seen without reading it all (also without `Content-Length`). */
export async function readBody(req: Request, max: number): Promise<Uint8Array> {
  if (Number(req.headers.get("Content-Length") ?? 0) > max) return new Uint8Array(max + 1);
  const out = new Uint8Array(max + 1);
  const reader = req.body?.getReader();
  let n = 0;
  while (reader && n <= max) {
    const { done, value } = await reader.read();
    if (done) break;
    out.set(value.subarray(0, max + 1 - n), n);
    n += value.byteLength;
  }
  if (n > max) await reader?.cancel();
  return out.subarray(0, Math.min(n, max + 1));
}

async function digest(s: string): Promise<Uint8Array> {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)));
}

/** Bearer `PULL_TOKEN`, compared in constant time over digests. */
export async function authorized(req: Request, env: Env): Promise<boolean> {
  if (!env.PULL_TOKEN) return false;
  const given = /^Bearer (.+)$/.exec(req.headers.get("Authorization") ?? "")?.[1] ?? "";
  const [a, b] = await Promise.all([digest(given), digest(env.PULL_TOKEN)]);
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i]! ^ b[i]!;
  return diff === 0;
}

/** Today's count of `user` in rate `table` after this one, atomically. */
export async function bump(env: Env, table: "rate" | "telemetry_rate", user: string, today: string): Promise<number> {
  const row = await env.DB.prepare(
    `INSERT INTO ${table} (user_hash, day, count) VALUES (?, ?, 1) ON CONFLICT (user_hash, day) DO UPDATE SET count = count + 1 RETURNING count`,
  )
    .bind(user, today)
    .first<{ count: number }>();
  return row?.count ?? 0;
}
