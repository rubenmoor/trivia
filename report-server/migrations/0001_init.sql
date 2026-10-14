-- Plan 103 "Data": no SteamID, no IP, no headers.
CREATE TABLE reports (
  id INTEGER PRIMARY KEY,
  received_at TEXT NOT NULL,
  question_id TEXT NOT NULL,
  lang TEXT NOT NULL,
  text TEXT NOT NULL,
  note TEXT NOT NULL,
  version TEXT NOT NULL,
  pool TEXT
);
CREATE INDEX reports_received_at ON reports (received_at);

-- Daily counts per HMAC(HASH_SALT, SteamID64); user_hash '*' = daily total.
CREATE TABLE rate (
  user_hash TEXT NOT NULL,
  day TEXT NOT NULL,
  count INTEGER NOT NULL,
  PRIMARY KEY (user_hash, day)
);
