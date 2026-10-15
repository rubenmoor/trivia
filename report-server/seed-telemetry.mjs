// Dev only (plan 105 "Dev mode"): posts N synthetic telemetry sessions to the local report server.
// Usage: node seed-telemetry.mjs [N] [URL]; URL default http://127.0.0.1:8787, localhost only.
import { randomUUID } from "node:crypto";
import { readFileSync } from "node:fs";

const n = Number(process.argv[2] ?? 20);
const base = new URL(process.argv[3] ?? process.env.TRIVIA_REPORT_URL ?? "http://127.0.0.1:8787");
if (!Number.isInteger(n) || n < 1 || n > 2000) fail("N: integer 1–2000");
if (!["localhost", "127.0.0.1"].includes(base.hostname)) fail(`refusing ${base.origin}: localhost only`);

const data = (f) => JSON.parse(readFileSync(new URL(`../app/data/${f}`, import.meta.url), "utf8"));
const pool = data("pool.json");
const groups = data("age-groups.json").groups;
const version = JSON.parse(readFileSync(new URL("../app/desktop/package.json", import.meta.url), "utf8")).version;
const rated = new Map(), byDiff = new Map();
for (const q of pool.questions) {
  if (!/^q-\d{4,6}$/.test(q.id) || !Number.isInteger(q.difficulty)) continue;
  rated.set(q.id, q.difficulty);
  byDiff.set(q.difficulty, [...(byDiff.get(q.difficulty) ?? []), q.id]);
}
// Played = rated, except ~8 % outliers (±3–5) so the report has something to find.
const played = new Map([...rated.keys()].map((id) => [id, Math.random() < 0.08 ? (Math.random() < 0.5 ? -1 : 1) * (3 + rnd(3)) : 0]));

const MODES = ["solo", "solo", "gamemaster", "gamemaster", "rr-coop", "rr-competitive", "timed"];
const JOKERS = ["hint", "skip", "easier", "category", "snipe"];
const run = randomUUID().slice(0, 8);

let stored = 0, dup = 0, failed = 0;
for (let i = 0; i < n; i++) {
  const body = { ...session(), ticket: `dev-${run}-${Math.floor(i / 5)}` };  // 5 sessions per fake user (limit 10)
  const res = await fetch(new URL("/telemetry", base), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }).catch((e) => fail(`${base.origin}: ${e.cause?.code ?? e.message} (is \`trivia-report-server dev\` running?)`));
  if (res.status === 201) stored++;
  else if (res.status === 200) dup++;
  else {
    failed++;
    console.error(`session ${i + 1}: ${res.status} ${await res.text()}`);
    if (failed >= 3) break;
  }
}
console.log(`seed-telemetry: ${stored} stored, ${dup} duplicate, ${failed} failed`);
process.exit(failed ? 1 : 0);

function session() {
  const games = Array.from({ length: rnd(4) }, game);  // 0–3 games
  return { session: randomUUID(), install: randomUUID(), version, length_s: 300 + rnd(7200), games };
}

function game() {
  const mode = pick(MODES);
  const custom = Math.random() < 0.1;
  const g = custom ? null : pick(groups);
  const start = 1 + rnd(8), end = start + rnd(16 - start);
  const levels = g ? g.levels : Array.from({ length: 12 }, (_, l) => { const d = Math.round(start + ((end - start) * l) / 11); return [d, d]; });
  const skill = (g ? g.window[1] : end) + 1;
  const jokers = Object.fromEntries((mode === "timed" ? [] : JOKERS).map((j) => [j, 0]));
  const answers = [];
  let reached = 0, result = "won";
  for (let l = 1; l <= levels.length; l++) {
    reached = l;
    if (Math.random() < 0.02) { result = Math.random() < 0.5 ? "abandoned" : "open"; break; }
    const [lo, hi] = levels[l - 1];
    const id = question(lo, hi);
    if (!id) continue;
    const used = {};
    if (mode !== "timed" && Math.random() < 0.08) jokers.skip++;  // replaced question: no row
    for (const j of mode === "timed" ? [] : ["hint", "easier", "category", "snipe"])
      if (Math.random() < (j === "hint" ? 0.2 : 0.04)) { used[j] = j === "hint" ? 1 + rnd(3) : 1; jokers[j] += used[j]; }
    const bonus = (used.hint ?? 0) * 0.7 + (used.easier ? 1.5 : 0) + (used.category ? 0.5 : 0) + (used.snipe ? 1 : 0);
    const p = 1 / (1 + Math.exp((rated.get(id) + played.get(id) - skill - bonus) / 1.5));
    const correct = Math.random() < p;
    answers.push({ question: id, level: l, correct, jokers: used });
    if (!correct) { result = "lost"; break; }
  }
  return {
    mode, locale: "es", pool: pool.hash ?? null,
    age_group: g ? g.id : null, difficulty: g ? null : { start, end },
    levels: levels.length, reached, result,
    customized: custom || Math.random() < 0.1, mods: Math.random() < 0.05,
    jokers, answers,
  };
}

function question(lo, hi) {
  const ids = [];
  for (let d = lo; d <= hi; d++) ids.push(...(byDiff.get(d) ?? []));
  return ids.length ? pick(ids) : null;
}

function rnd(k) { return Math.floor(Math.random() * k); }
function pick(xs) { return xs[rnd(xs.length)]; }
function fail(msg) { console.error(`seed-telemetry: ${msg}`); process.exit(2); }
