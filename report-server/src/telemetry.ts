// Opt-in telemetry (plan 105, decision 118): the shell posts one session, authoring pulls and acks.
// Never logs bodies, tickets, SteamIDs, hashes, install or session ids.
import type { Env } from "../env";
import { day, error, json, rateLimited, readBody } from "./http";
import { checkTicket, devTickets, userHash } from "./steam";
import { checkLimit } from "./validate";
import { checkTelemetry, checkTelemetryAck, MAX_TELEMETRY_BODY } from "./validate-telemetry";

const BUMP = "INSERT INTO telemetry_rate (user_hash, day, count) VALUES (?, ?, 1) ON CONFLICT (user_hash, day) DO UPDATE SET count = count + 1";

async function count(env: Env, user: string, today: string): Promise<number> {
  const row = await env.DB.prepare("SELECT count FROM telemetry_rate WHERE user_hash = ? AND day = ?").bind(user, today).first<{ count: number }>();
  return row?.count ?? 0;
}

export async function postTelemetry(req: Request, env: Env, url: URL): Promise<Response> {
  if (env.TELEMETRY_OPEN === "0") return error(503, "closed");
  const dev = devTickets(env, url);
  const checked = checkTelemetry(req.headers.get("Content-Type"), await readBody(req, MAX_TELEMETRY_BODY), dev);
  if (!checked.ok) {
    if (checked.status === 413) return error(413, "too_large");
    if (checked.status === 415) return error(415, "unsupported_media_type");
    return error(400, "bad_request", checked.field ? { field: checked.field } : {});
  }
  const ticket = await checkTicket(checked.ticket, env.TELEMETRY_IDENTITY, env, dev);
  if (!ticket.ok) return ticket.status === 401 ? error(401, "invalid_ticket") : error(502, "steam_unavailable");
  if (!env.HASH_SALT) throw new Error("HASH_SALT not set");

  const s = checked.session;
  const seen = await env.DB.prepare(
    "SELECT 1 AS hit FROM telemetry WHERE session_id = ?1 UNION ALL SELECT 1 FROM telemetry_seen WHERE session_id = ?1",
  )
    .bind(s.session)
    .first<{ hit: number }>();
  if (seen) return json(200, { stored: false, duplicate: true });

  const now = new Date();
  const today = day(now);
  const user = await userHash(env.HASH_SALT, ticket.steamid);
  if ((await count(env, user, today)) >= Number(env.RATE_TELEMETRY_USER)) return rateLimited(now);
  if ((await count(env, "*", today)) >= Number(env.RATE_TELEMETRY_TOTAL)) return rateLimited(now);

  await env.DB.batch([
    env.DB.prepare("INSERT INTO telemetry (session_id, received_day, body) VALUES (?, ?, ?) ON CONFLICT (session_id) DO NOTHING").bind(
      s.session,
      today,
      JSON.stringify(s),
    ),
    env.DB.prepare(BUMP).bind(user, today),
    env.DB.prepare(BUMP).bind("*", today),
  ]);
  return json(201, { stored: true });
}

export async function pullTelemetry(env: Env, url: URL): Promise<Response> {
  const limit = checkLimit(url.searchParams.get("limit"));
  if (limit === null) return error(400, "bad_request", { field: "limit" });
  const n = Math.min(limit, 200);
  const { results } = await env.DB.prepare("SELECT received_day, body FROM telemetry ORDER BY received_day, session_id LIMIT ?")
    .bind(n + 1)
    .all<{ received_day: string; body: string }>();
  return json(200, {
    sessions: results.slice(0, n).map((r) => ({ received_day: r.received_day, ...(JSON.parse(r.body) as object) })),
    more: results.length > n,
  });
}

export async function ackTelemetry(req: Request, env: Env): Promise<Response> {
  const ids = checkTelemetryAck(await readBody(req, MAX_TELEMETRY_BODY));
  if (!ids) return error(400, "bad_request", { field: "sessions" });
  const list = JSON.stringify(ids);
  const [, deleted] = await env.DB.batch([
    env.DB.prepare(
      "INSERT INTO telemetry_seen (session_id, day) SELECT session_id, ? FROM telemetry WHERE session_id IN (SELECT value FROM json_each(?)) ON CONFLICT (session_id) DO NOTHING",
    ).bind(day(new Date()), list),
    env.DB.prepare("DELETE FROM telemetry WHERE session_id IN (SELECT value FROM json_each(?))").bind(list),
  ]);
  return json(200, { acked: deleted?.meta.changes ?? 0 });
}

/** Unacked sessions and tombstones after `TELEMETRY_KEEP_DAYS`, rate rows of past days. */
export async function telemetryRetention(env: Env, now: Date): Promise<void> {
  const cutoff = day(new Date(now.getTime() - Number(env.TELEMETRY_KEEP_DAYS) * 86_400_000));
  await env.DB.batch([
    env.DB.prepare("DELETE FROM telemetry WHERE received_day < ?").bind(cutoff),
    env.DB.prepare("DELETE FROM telemetry_seen WHERE day < ?").bind(cutoff),
    env.DB.prepare("DELETE FROM telemetry_rate WHERE day < ?").bind(day(now)),
  ]);
}
