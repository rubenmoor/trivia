// Helpers shared by the report and telemetry routes.
import type { Env } from "../env";

export const json = (status: number, body: unknown, headers: Record<string, string> = {}): Response =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json; charset=utf-8", ...headers } });

export const error = (status: number, code: string, extra: Record<string, unknown> = {}): Response =>
  json(status, { error: code, ...extra });

export const day = (now: Date): string => now.toISOString().slice(0, 10);

/** 429 until the next UTC day. */
export function rateLimited(now: Date): Response {
  const wait = Math.ceil((Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1) - now.getTime()) / 1000);
  return json(429, { error: "rate_limited", retry_after: wait }, { "Retry-After": String(wait) });
}

/** Body up to `max + 1` bytes, so oversize is seen without reading it all. */
export async function readBody(req: Request, max: number): Promise<Uint8Array> {
  if (Number(req.headers.get("Content-Length") ?? 0) > max) return new Uint8Array(max + 1);
  const buf = new Uint8Array(await req.arrayBuffer());
  return buf.byteLength > max ? buf.subarray(0, max + 1) : buf;
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
