// Body checks of `POST /reports` (plan 103 "API contract"); pure, no Worker APIs.

export const MAX_BODY = 16 * 1024;

export interface Report {
  question: string;
  lang: string;
  text: string;
  note: string;
  version: string;
  pool: string | null;
  ticket: string;
}

export type Rejected = { ok: false; status: 400 | 413 | 415; field?: string };
export type Checked = { ok: true; report: Report } | Rejected;

export const LANG = /^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$/;
export const VERSION = /^\d+\.\d+\.\d+([-+][0-9A-Za-z.-]+)?$/;

const CONTROL = /[\u0000-\u0008\u000b-\u001f\u007f]/g;

export const isObj = (v: unknown): v is Record<string, unknown> => typeof v === "object" && v !== null && !Array.isArray(v);

/** Strict UTF-8 JSON; undefined when not. */
export function parseJson(body: Uint8Array): unknown {
  try {
    return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(body));
  } catch {
    return undefined;
  }
}

/** Hex Steam ticket; `dev` also takes `dev-*` (fake check). */
export const validTicket = (v: unknown, dev: boolean): v is string =>
  typeof v === "string" && (/^[0-9A-Fa-f]{2,4096}$/.test(v) || (dev && /^dev-[0-9A-Za-z-]{1,64}$/.test(v)));

const RULES: Record<Exclude<keyof Report, "ticket">, (v: unknown) => boolean> = {
  question: (v) => typeof v === "string" && /^[A-Za-z0-9._:-]{1,64}$/.test(v),
  lang: (v) => typeof v === "string" && v.length <= 16 && LANG.test(v),
  text: (v) => typeof v === "string" && v.replace(CONTROL, "").trim().length >= 1 && v.replace(CONTROL, "").trim().length <= 4000,
  note: (v) => v === undefined || v === null || (typeof v === "string" && v.replace(CONTROL, "").length <= 1000),
  version: (v) => typeof v === "string" && v.length <= 32 && VERSION.test(v),
  pool: (v) => v === null || (typeof v === "string" && /^[0-9a-f]{8}$/.test(v)),
};

/** Content type, size, JSON, fields; unknown fields dropped. `dev` also takes `dev-*` tickets (fake check). */
export function checkReport(contentType: string | null, body: Uint8Array, dev = false): Checked {
  if (!/^application\/json\s*(;|$)/i.test(contentType ?? "")) return { ok: false, status: 415 };
  if (body.byteLength > MAX_BODY) return { ok: false, status: 413 };
  const o = parseJson(body);
  if (!isObj(o)) return { ok: false, status: 400 };
  for (const [field, ok] of Object.entries(RULES)) if (!ok(o[field])) return { ok: false, status: 400, field };
  if (!validTicket(o.ticket, dev)) return { ok: false, status: 400, field: "ticket" };
  return {
    ok: true,
    report: {
      question: o.question as string,
      lang: o.lang as string,
      text: (o.text as string).replace(CONTROL, "").trim(),
      note: ((o.note as string | null | undefined) ?? "").replace(CONTROL, "").trim(),
      version: o.version as string,
      pool: o.pool as string | null,
      ticket: o.ticket,
    },
  };
}

/** `POST /reports/ack` body: 1–500 integer ids, else null. */
export function checkAck(body: Uint8Array): number[] | null {
  const data = parseJson(body);
  const ids = isObj(data) ? data["ids"] : undefined;
  if (!Array.isArray(ids) || ids.length < 1 || ids.length > 500 || !ids.every((i) => Number.isSafeInteger(i))) return null;
  return ids as number[];
}

/** `?limit=`: default 100, at most 500; null when not a positive integer. */
export function checkLimit(raw: string | null): number | null {
  if (raw === null) return 100;
  if (!/^\d{1,6}$/.test(raw) || Number(raw) < 1) return null;
  return Math.min(Number(raw), 500);
}
