// Question report server (plan 103, decision 93): the game posts, `qgen flag --pull` pulls and acks.
// Never logs bodies, tickets, SteamIDs or hashes.
import type { Env, ExecutionContext, ScheduledController } from "../env";
import { authorized, day, error, json, rateLimited, readBody } from "./http";
import { checkTicket, devTickets, userHash } from "./steam";
import { ackTelemetry, postTelemetry, pullTelemetry, telemetryRetention } from "./telemetry";
import { checkAck, checkLimit, checkReport, MAX_BODY } from "./validate";

const KEEP_DAYS = 90;

/** Today's count of `user` after this one. */
async function bump(env: Env, user: string, today: string): Promise<number> {
  const row = await env.DB.prepare(
    "INSERT INTO rate (user_hash, day, count) VALUES (?, ?, 1) ON CONFLICT (user_hash, day) DO UPDATE SET count = count + 1 RETURNING count",
  )
    .bind(user, today)
    .first<{ count: number }>();
  return row?.count ?? 0;
}

async function postReport(req: Request, env: Env, url: URL): Promise<Response> {
  if (env.REPORTS_OPEN === "0") return error(503, "closed");
  const dev = devTickets(env, url);
  const checked = checkReport(req.headers.get("Content-Type"), await readBody(req, MAX_BODY), dev);
  if (!checked.ok) {
    if (checked.status === 413) return error(413, "too_large");
    if (checked.status === 415) return error(415, "unsupported_media_type");
    return error(400, "bad_request", checked.field ? { field: checked.field } : {});
  }
  const r = checked.report;
  const ticket = await checkTicket(r.ticket, env.TICKET_IDENTITY, env, dev);
  if (!ticket.ok) return ticket.status === 401 ? error(401, "invalid_ticket") : error(502, "steam_unavailable");
  if (!env.HASH_SALT) throw new Error("HASH_SALT not set");

  const now = new Date();
  const today = day(now);
  if ((await bump(env, await userHash(env.HASH_SALT, ticket.steamid), today)) > Number(env.RATE_USER)) return rateLimited(now);
  if ((await bump(env, "*", today)) > Number(env.RATE_TOTAL)) return rateLimited(now);

  const row = await env.DB.prepare(
    "INSERT INTO reports (received_at, question_id, lang, text, note, version, pool) VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id",
  )
    .bind(now.toISOString().slice(0, 19) + "Z", r.question, r.lang, r.text, r.note, r.version, r.pool)
    .first<{ id: number }>();
  return json(201, { id: row?.id });
}

async function listReports(env: Env, url: URL): Promise<Response> {
  const limit = checkLimit(url.searchParams.get("limit"));
  if (limit === null) return error(400, "bad_request", { field: "limit" });
  const { results } = await env.DB.prepare(
    "SELECT id, received_at, question_id AS question, lang, text, note, version, pool FROM reports ORDER BY id LIMIT ?",
  )
    .bind(limit + 1)
    .all<Record<string, unknown>>();
  return json(200, {
    reports: results.slice(0, limit),
    more: results.length > limit,
  });
}

async function ack(req: Request, env: Env): Promise<Response> {
  const ids = checkAck(await readBody(req, MAX_BODY));
  if (!ids) return error(400, "bad_request", { field: "ids" });
  const res = await env.DB.prepare("DELETE FROM reports WHERE id IN (SELECT value FROM json_each(?))")
    .bind(JSON.stringify(ids))
    .run();
  return json(200, { acked: res.meta.changes });
}

async function route(req: Request, env: Env): Promise<Response> {
  const url = new URL(req.url);
  const methods: Record<string, string[]> = {
    "/reports": ["GET", "POST"],
    "/reports/ack": ["POST"],
    "/telemetry": ["GET", "POST"],
    "/telemetry/ack": ["POST"],
    "/health": ["GET"],
  };
  const allowed = methods[url.pathname];
  if (!allowed) return error(404, "not_found");
  if (!allowed.includes(req.method)) return error(405, "method_not_allowed");
  if (url.pathname === "/health") return json(200, { ok: true, api: 1 });
  if (url.pathname === "/reports" && req.method === "POST") return postReport(req, env, url);
  if (url.pathname === "/telemetry" && req.method === "POST") return postTelemetry(req, env, url);
  if (!(await authorized(req, env))) return error(401, "unauthorized");
  if (url.pathname === "/telemetry") return pullTelemetry(env, url);
  if (url.pathname === "/telemetry/ack") return ackTelemetry(req, env);
  return url.pathname === "/reports" ? listReports(env, url) : ack(req, env);
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    try {
      return await route(req, env);
    } catch (e) {
      console.error("internal", e instanceof Error ? e.name : "error");
      return error(500, "internal");
    }
  },

  /** Daily 03:00 UTC: rate rows of past days, reports older than 90 days, telemetry (plan 105 "Retention"). */
  async scheduled(controller: ScheduledController, env: Env, ctx: ExecutionContext): Promise<void> {
    const now = new Date(controller.scheduledTime);
    const cutoff = new Date(now.getTime() - KEEP_DAYS * 86_400_000).toISOString().slice(0, 19) + "Z";
    ctx.waitUntil(
      Promise.all([
        env.DB.prepare("DELETE FROM rate WHERE day < ?").bind(day(now)).run(),
        env.DB.prepare("DELETE FROM reports WHERE received_at < ?").bind(cutoff).run(),
        telemetryRetention(env, now),
      ]),
    );
  },
};
