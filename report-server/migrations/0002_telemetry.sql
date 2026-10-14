-- Plan 105 "Storage": one row per session, body = validated known fields only.
CREATE TABLE telemetry (
  session_id TEXT PRIMARY KEY,
  received_day TEXT NOT NULL,
  body TEXT NOT NULL
);
CREATE INDEX telemetry_received_day ON telemetry (received_day);

-- Daily sessions per HMAC(HASH_SALT, SteamID64); user_hash '*' = daily total.
CREATE TABLE telemetry_rate (
  user_hash TEXT NOT NULL,
  day TEXT NOT NULL,
  count INTEGER NOT NULL,
  PRIMARY KEY (user_hash, day)
);

-- Acked session ids, so a late resend isn't stored twice.
CREATE TABLE telemetry_seen (
  session_id TEXT PRIMARY KEY,
  day TEXT NOT NULL
);
