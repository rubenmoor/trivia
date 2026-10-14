// Report server client (plans 93, 107): `/reports` on the player's click, `/telemetry` at quit and next start; pure Node, no Electron.
import { randomBytes } from "node:crypto";
import http from "node:http";
import https from "node:https";

/** Plan 103's ticket identity; the server's `TICKET_IDENTITY`. */
export const IDENTITY = "trivia-reports";
/** Plan 105's; the server's `TELEMETRY_IDENTITY`. */
export const TELEMETRY_IDENTITY = "trivia-telemetry";

const CONNECT_MS = 5000;
const TOTAL_MS = 10000;
const MAX_BODY = 16 * 1024;
export const MAX_TELEMETRY_BODY = 64 * 1024;
const MAX_RESPONSE = 64 * 1024;

/** `{ url, dev }`: `<base>/<route>`; base `TRIVIA_REPORT_URL` only with the dev switch (then dev tickets), else `configured`; null when empty or not http(s). */
export function reportTarget(configured, env, route = "reports") {
  const dev = env.TRIVIA_DEV_STEAM_USER === "1" && !!env.TRIVIA_REPORT_URL;
  const raw = dev ? env.TRIVIA_REPORT_URL : configured;
  if (typeof raw !== "string" || !raw) return null;
  let url;
  try {
    url = new URL(route, raw.endsWith("/") ? raw : `${raw}/`);
  } catch {
    return null;
  }
  return url.protocol === "https:" || url.protocol === "http:" ? { url, dev } : null;
}

/** Plan 103's dev check takes any `dev-*` ticket. */
export const devTicket = () => `dev-${randomBytes(16).toString("hex")}`;

// Plan 103's field rules; control characters but \n, \t stripped as the server does.
const CONTROL = /[\u0000-\u0008\u000b-\u001f\u007f]/g;
const RULES = {
  question: (v) => typeof v === "string" && /^[A-Za-z0-9._:-]{1,64}$/.test(v),
  lang: (v) => typeof v === "string" && v.length <= 16 && /^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$/.test(v),
  text: (v) => typeof v === "string" && v.trim().length >= 1 && v.trim().length <= 4000,
  note: (v) => v === undefined || v === null || (typeof v === "string" && v.length <= 1000),
  version: (v) => typeof v === "string" && v.length <= 32 && /^\d+\.\d+\.\d+([-+][0-9A-Za-z.-]+)?$/.test(v),
  pool: (v) => v === null || (typeof v === "string" && /^[0-9a-f]{8}$/.test(v)),
};

/** The page's `{ question, lang, text, note?, version, pool }`; throws `bad_report` (`.field`). */
export function reportFields(arg) {
  const plain = arg !== null && typeof arg === "object" && Object.getPrototypeOf(arg) === Object.prototype;
  for (const [field, ok] of Object.entries(RULES))
    if (!plain || !ok(arg[field])) throw Object.assign(new Error("bad_report"), { field: plain ? field : null });
  return {
    question: arg.question,
    lang: arg.lang,
    text: arg.text.replace(CONTROL, ""),
    note: (arg.note ?? "").replace(CONTROL, ""),
    version: arg.version,
    pool: arg.pool,
  };
}

/** POST `{ ...fields, ticket }`; `{ ok, id }` or `{ ok: false, status, error, retryAfter? }`, `status: 0` without a response. No retry. */
export async function postReport(url, fields, ticket, opts) {
  const r = await postJson(url, { ...fields, ticket }, { maxBody: MAX_BODY, ...opts });
  return r.res ? result(r.res, r.text) : r;
}

/** One JSON POST: `{ res, text }`, or `{ ok: false, status: 0, error }` without a response (`too_large`: not sent). */
export function postJson(url, payload, { maxBody, connectMs = CONNECT_MS, totalMs = TOTAL_MS }) {
  const body = Buffer.from(JSON.stringify(payload), "utf8");
  if (body.length > maxBody) return Promise.resolve({ ok: false, status: 0, error: "too_large" });
  const mod = url.protocol === "https:" ? https : http;
  return new Promise((resolve) => {
    let done = false;
    const finish = (result) => {
      if (done) return;
      done = true;
      clearTimeout(connectTimer);
      clearTimeout(totalTimer);
      req.destroy();
      resolve(result);
    };
    const req = mod.request(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Content-Length": body.length, Accept: "application/json" },
      agent: false,
    });
    const connectTimer = setTimeout(() => finish({ ok: false, status: 0, error: "timeout" }), connectMs);
    const totalTimer = setTimeout(() => finish({ ok: false, status: 0, error: "timeout" }), totalMs);
    req.on("socket", (socket) =>
      socket.once(url.protocol === "https:" ? "secureConnect" : "connect", () => clearTimeout(connectTimer)),
    );
    req.on("error", () => finish({ ok: false, status: 0, error: "no_connection" }));
    req.on("response", (res) => {
      const chunks = [];
      let size = 0;
      res.on("data", (chunk) => {
        size += chunk.length;
        if (size <= MAX_RESPONSE) chunks.push(chunk);
      });
      res.on("error", () => finish({ ok: false, status: res.statusCode ?? 0, error: "no_connection" }));
      res.on("end", () => finish({ res, text: Buffer.concat(chunks).toString("utf8") }));
    });
    req.end(body);
  });
}

function result(res, text) {
  const status = res.statusCode ?? 0;
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {}
  if (status === 201 && Number.isInteger(json?.id)) return { ok: true, id: json.id };
  const out = { ok: false, status, error: typeof json?.error === "string" ? json.error : `http_${status}` };
  if (status === 429) {
    const after = Number(json?.retry_after ?? res.headers["retry-after"]);
    if (Number.isFinite(after) && after >= 0) out.retryAfter = Math.round(after);
  }
  return out;
}
