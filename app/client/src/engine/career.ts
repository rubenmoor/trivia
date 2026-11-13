// The career (plan 195, plans/24-career.md): pure counters, badges, rank and the catch-up step over the save. No UI.
import { DEFAULT_AGE_GROUP } from "./choice.ts";
import { qualifies, towerWin } from "./achievements.ts";
import { cleanName, gameMode, playerId } from "./game.ts";
import { subOf } from "./pool.ts";
import type { EngineData, GameRow, GameState, PlayerRow, SaveData } from "./state.ts";
import { GameError, gameLocale, transact } from "./state.ts";

/** Ids of app/data/subjects.json, same order (career.test.ts checks). @internal used by tests and the UI parts */
export const SUBJECTS = ["history", "geography", "nature", "science", "arts", "media", "sport"] as const;

/** Ids of app/data/age-groups.json, kids first (career.test.ts checks). @internal used by tests and the UI parts */
export const YEAR_GROUPS = ["kids", "young_teens", "young_adults", "adults"] as const;

/** Difficulty floors of the grades elementary, middle, high, college: a right answer counts for every grade with floor ≤ d. */
const BAND_FLOORS = [1, 5, 9, 13] as const;
const GRADES = ["elementary", "middle", "high"] as const;
/** Right answers per subject for the grades elementary, middle, high. */
const GRADE_NEED = [15, 25, 15] as const;
const COLLEGE_NEED = 15;
const YEAR_NEED = 20;
const SCORE_MILESTONES = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000] as const;
const RANKS_KEPT = 10;
const RANK_NAMES = 15;

export interface PlayerCareer {
  off?: true;
  score: number;
  /** Subject id → right answers at difficulty 1+, 5+, 9+, 13+. */
  right: Record<string, [number, number, number, number]>;
  /** Age group id → finished games (won or lost). */
  years: Record<string, number>;
  /** Last 10 rank values, newest last. */
  ranks: number[];
  /** API name → local ISO date earned; `shown` once celebrated. */
  badges: Record<string, { on: string; shown?: true }>;
}

export interface GameCareer {
  /** History entries counted: `row.state` first, then each seat's own state. */
  cursor: number[];
  /** The game end is counted. */
  ended?: true;
}

/** @internal used by tests and the UI parts */
export const emptyCareer = (): PlayerCareer => ({ score: 0, right: {}, years: {}, ranks: [], badges: {} });

const up = (s: string) => s.toUpperCase();

interface Badge { name: string; met: (c: PlayerCareer) => boolean }

const rightAt = (c: PlayerCareer, subject: string, grade: number) => c.right[subject]?.[grade] ?? 0;

/** Every badge in live order (Steam): grade-major subject × grade, diplomas, college, school years, score. New ones are appended, never inserted. @internal used by tests and the UI parts */
export const BADGES: readonly Badge[] = [
  ...GRADES.flatMap((g, gi) => SUBJECTS.map((s) => ({
    name: `CAREER_${up(s)}_${up(g)}`, met: (c: PlayerCareer) => rightAt(c, s, gi) >= GRADE_NEED[gi],
  }))),
  ...GRADES.map((g, gi) => ({
    name: `CAREER_DIPLOMA_${up(g)}`, met: (c: PlayerCareer) => SUBJECTS.every((s) => rightAt(c, s, gi) >= GRADE_NEED[gi]),
  })),
  { name: "CAREER_COLLEGE", met: (c) => SUBJECTS.reduce((n, s) => n + rightAt(c, s, 3), 0) >= COLLEGE_NEED },
  ...YEAR_GROUPS.map((g) => ({ name: `CAREER_YEAR_${up(g)}`, met: (c: PlayerCareer) => (c.years[g] ?? 0) >= YEAR_NEED })),
  ...SCORE_MILESTONES.map((n) => ({ name: `CAREER_SCORE_${n}`, met: (c: PlayerCareer) => c.score >= n })),
];

export const BADGE_NAMES: readonly string[] = BADGES.map((b) => b.name);

/** A right answer of difficulty `d` (+d²), counted for `subject` (none: score only). @internal used by tests and the UI parts */
export function countRight(c: PlayerCareer, subject: string | undefined, d: number): PlayerCareer {
  const next = { ...c, score: c.score + d * d };
  if (subject !== undefined && (SUBJECTS as readonly string[]).includes(subject)) {
    const row = [...(c.right[subject] ?? [0, 0, 0, 0])] as [number, number, number, number];
    BAND_FLOORS.forEach((floor, i) => { if (d >= floor) row[i]++; });
    next.right = { ...c.right, [subject]: row };
  }
  return next;
}

/** A wrong answer: −1, the score may go negative. @internal used by tests and the UI parts */
export const countWrong = (c: PlayerCareer): PlayerCareer => ({ ...c, score: c.score - 1 });

/** A finished game (won or lost) in `ageGroup`; `rank`: its rank value (hardest right answer, 0 if none). @internal used by tests and the UI parts */
export const countEnd = (c: PlayerCareer, ageGroup: string, rank: number): PlayerCareer => ({
  ...c, years: { ...c.years, [ageGroup]: (c.years[ageGroup] ?? 0) + 1 }, ranks: [...c.ranks, rank].slice(-RANKS_KEPT),
});

/** The badges reached and not yet held, in live order. @internal used by tests and the UI parts */
export const newBadges = (c: PlayerCareer): string[] => BADGES.filter((b) => !c.badges[b.name] && b.met(c)).map((b) => b.name);

/** The career with its new badges held from `on`; a badge is never removed. @internal used by tests and the UI parts */
export function award(c: PlayerCareer, on: string): PlayerCareer {
  const names = newBadges(c);
  return names.length ? { ...c, badges: { ...c.badges, ...Object.fromEntries(names.map((n) => [n, { on }])) } } : c;
}

/** Rank value: weighted mean of the ranks (newest last; weights 10..1 newest first), half up, at least 1; null without games. @internal used by tests and the UI parts */
export function rankOf(ranks: readonly number[]): number | null {
  if (!ranks.length) return null;
  const last = ranks.slice(-RANKS_KEPT);
  let sum = 0, weights = 0;
  last.forEach((v, i) => {
    const w = RANKS_KEPT - (last.length - 1 - i);
    sum += w * v;
    weights += w;
  });
  return Math.max(1, Math.floor((2 * sum + weights) / (2 * weights)));
}

/** Index into the 15 rank names (0-based), null without games. @internal used by tests and the UI parts */
export const rankIndex = (ranks: readonly number[]): number | null => {
  const r = rankOf(ranks);
  return r === null ? null : Math.min(r, RANK_NAMES) - 1;
};

// The catch-up step (decision 589): after every game action and at load (backfill).

/** The states a row's cursor counts: `row.state`, then (rr-competitive) each seat's own. */
const cursorStates = (row: GameRow): (GameState | undefined)[] =>
  [row.state, ...(gameMode(row.state) === "rr-competitive" ? (row.seats ?? []).map((s) => s.state) : [])];

const finished = (row: GameRow) => row.result === "won" || row.result === "lost";

/** History entries or a game end the career hasn't counted yet. */
export function behind(row: GameRow): boolean {
  const cursor = row.career?.cursor ?? [];
  return cursorStates(row).some((s, i) => (s?.history?.length ?? 0) > (cursor[i] ?? 0)) || (finished(row) && !row.career?.ended);
}

/** Count what `save`'s rows of `data`'s locale haven't counted (decisions 589, 590, 515, 516); the same save if nothing.
 * `now`: the action's time for new badges; null (backfill): the game's `finished_on`, else `started_on`. Demo build: nothing. */
export function catchUp(save: SaveData, data: EngineData, now: string | null = null): SaveData {
  if (data.demo || !save.games.some((g) => gameLocale(g) === data.locale && behind(g))) return save;
  const players = save.players.map((p) => ({ ...p }));
  const byId = new Map(players.map((p) => [p.id, p]));
  const games = save.games.map((row) => (gameLocale(row) === data.locale && behind(row) ? countRow(row, byId, data, now) : row));
  return { ...save, players, games };
}

/** One row counted to its end: a copy with the cursor at the end; `byId`'s players updated in place. */
function countRow(row: GameRow, byId: Map<number, PlayerRow>, data: EngineData, now: string | null): GameRow {
  const states = cursorStates(row);
  const cursor = states.map((s) => s?.history?.length ?? 0);
  const done = { ...row, career: { cursor, ...(finished(row) ? { ended: true as const } : {}) } };
  if (row.demo || !qualifies(row)) return done;
  const on = now ?? row.finished_on ?? row.started_on;
  const credit = (seat: number | undefined, fn: (c: PlayerCareer) => PlayerCareer) => {
    const pid = row.seats ? (seat === undefined ? null : row.seats[seat]?.player_id ?? null) : row.player_id;
    const p = pid === null ? undefined : byId.get(pid);
    if (p) p.career = award(fn(p.career ?? emptyCareer()), on);
  };
  const competitive = gameMode(row.state) === "rr-competitive";
  const hardest = new Map<number | undefined, number>();
  states.forEach((s, i) => {
    const seatOf = (h: { seat?: number }) => (competitive && i > 0 ? i - 1 : h.seat);
    const from = row.career?.cursor[i] ?? 0;
    (s?.history ?? []).forEach((h, j) => {
      const q = typeof h.correct === "boolean" && !h.revealed ? data.byId.get(h.question_id) : undefined;
      if (!q) return;
      if (h.correct) hardest.set(seatOf(h), Math.max(hardest.get(seatOf(h)) ?? 0, q.difficulty));
      if (j >= from) credit(seatOf(h), h.correct ? (c) => countRight(c, data.broad.get(subOf(q) ?? "")?.subject, q.difficulty) : countWrong);
    });
  });
  if (finished(row) && !row.career?.ended) {
    const win = towerWin(row);
    const seats = row.seats ? row.seats.map((_, i) => i) : [undefined];
    for (const seat of seats) {
      const state = (competitive && seat !== undefined ? row.seats![seat].state : undefined) ?? row.state;
      const group = state.settings.age_group ?? DEFAULT_AGE_GROUP;
      const top = win && (seat === undefined || (row.seats![seat].result ?? row.result) === "won") ? data.groupById.get(group)?.window[1] : undefined;
      credit(seat, (c) => countEnd(c, group, top ?? hardest.get(seat) ?? 0));
    }
  }
  return done;
}

// Ops and reads (plan 195): opt-out, shown marks, the player view, Steam's union.

/** What a player's career looks like to the UI (counted even when `off`; hiding is the UI's). */
export interface CareerView {
  off: boolean;
  score: number;
  /** Rank value (null before the first finished game), its 0-based name index, the 15 names' count is the UI's. */
  rank: number | null;
  rank_index: number | null;
  /** Subject id → right answers at difficulty 1+, 5+, 9+, 13+. */
  right: Record<string, [number, number, number, number]>;
  years: Record<string, number>;
  badges: { name: string; on: string; shown: boolean }[];
}

export function careerView(p: PlayerRow): CareerView {
  const c = p.career ?? emptyCareer();
  return {
    off: c.off === true, score: c.score, rank: rankOf(c.ranks), rank_index: rankIndex(c.ranks), right: c.right, years: c.years,
    badges: BADGE_NAMES.filter((n) => c.badges[n]).map((n) => ({ name: n, on: c.badges[n].on, shown: c.badges[n].shown === true })),
  };
}

/** `career` op: turn a player's career off (`off` true) or on; counting goes on either way, turning on shows nothing by itself (decision 515). */
export function setCareerOff(save: SaveData, name: unknown, off: unknown): SaveData {
  return transact(save, (work) => {
    const p = playerOf(work, name);
    const c = p.career ?? emptyCareer();
    const { off: _, ...rest } = c;
    p.career = off === true ? { ...rest, off: true } : rest;
  }).save;
}

/** `career_shown` op: mark held badges of a player shown; unknown or not-held names are ignored. */
export function markShown(save: SaveData, name: unknown, badges: unknown): SaveData {
  return transact(save, (work) => {
    const p = playerOf(work, name);
    const names = Array.isArray(badges) ? badges : [];
    for (const n of names) {
      const b = typeof n === "string" ? p.career?.badges[n] : undefined;
      if (b) b.shown = true;
    }
  }).save;
}

function playerOf(work: SaveData, name: unknown): PlayerRow {
  const pid = playerId(work, cleanName(name));
  const p = work.players.find((x) => x.id === pid);
  if (!p) throw new GameError("player_unknown", { name });
  return p;
}

/** Badges of every player with the career on, in live order: what Steam unlocks (decision 515). */
export function careerUnlocks(save: SaveData): string[] {
  const held = new Set(save.players.filter((p) => !p.career?.off).flatMap((p) => Object.keys(p.career?.badges ?? {})));
  return BADGE_NAMES.filter((n) => held.has(n));
}
