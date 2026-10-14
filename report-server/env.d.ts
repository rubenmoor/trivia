// The few Worker and D1 types used (decision 117: no @cloudflare/workers-types).

export interface D1Result<T> {
  results: T[];
  meta: { changes: number };
}

export interface D1PreparedStatement {
  bind(...values: unknown[]): D1PreparedStatement;
  first<T>(): Promise<T | null>;
  all<T>(): Promise<D1Result<T>>;
  run(): Promise<D1Result<never>>;
}

export interface D1Database {
  prepare(sql: string): D1PreparedStatement;
  batch(statements: D1PreparedStatement[]): Promise<D1Result<unknown>[]>;
}

export interface ScheduledController {
  scheduledTime: number;
  cron: string;
}

export interface ExecutionContext {
  waitUntil(promise: Promise<unknown>): void;
}

/** `wrangler.toml` vars, Worker secrets, `.dev.vars`. */
export interface Env {
  DB: D1Database;
  STEAM_APP_ID: string;
  TICKET_IDENTITY: string;
  REPORTS_OPEN: string;
  RATE_USER: string;
  RATE_TOTAL: string;
  TELEMETRY_IDENTITY: string;
  TELEMETRY_OPEN: string;
  RATE_TELEMETRY_USER: string;
  RATE_TELEMETRY_TOTAL: string;
  TELEMETRY_KEEP_DAYS: string;
  STEAM_WEB_API_KEY?: string;
  PULL_TOKEN?: string;
  HASH_SALT?: string;
  DEV_FAKE_TICKETS?: string;
}
