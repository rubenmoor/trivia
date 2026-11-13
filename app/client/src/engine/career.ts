// The career (plan 195, plans/24-career.md): pure counters, badges and rank. No UI, no save access.

/** Ids of app/data/subjects.json, same order (career.test.ts checks). @internal until task 1980 wires it */
export const SUBJECTS = ["history", "geography", "nature", "science", "arts", "media", "sport"] as const;

/** Ids of app/data/age-groups.json, kids first (career.test.ts checks). @internal until task 1980 wires it */
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

/** @internal until task 1980 wires it */
export const emptyCareer = (): PlayerCareer => ({ score: 0, right: {}, years: {}, ranks: [], badges: {} });

const up = (s: string) => s.toUpperCase();

interface Badge { name: string; met: (c: PlayerCareer) => boolean }

const rightAt = (c: PlayerCareer, subject: string, grade: number) => c.right[subject]?.[grade] ?? 0;

/** Every badge in live order (Steam): grade-major subject × grade, diplomas, college, school years, score. New ones are appended, never inserted. @internal until task 1980 wires it */
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

/** @internal until task 1980 wires it */
export const BADGE_NAMES: readonly string[] = BADGES.map((b) => b.name);

/** A right answer of difficulty `d` (+d²), counted for `subject` (none: score only). @internal until task 1980 wires it */
export function countRight(c: PlayerCareer, subject: string | undefined, d: number): PlayerCareer {
  const next = { ...c, score: c.score + d * d };
  if (subject !== undefined && (SUBJECTS as readonly string[]).includes(subject)) {
    const row = [...(c.right[subject] ?? [0, 0, 0, 0])] as [number, number, number, number];
    BAND_FLOORS.forEach((floor, i) => { if (d >= floor) row[i]++; });
    next.right = { ...c.right, [subject]: row };
  }
  return next;
}

/** A wrong answer: −1, the score may go negative. @internal until task 1980 wires it */
export const countWrong = (c: PlayerCareer): PlayerCareer => ({ ...c, score: c.score - 1 });

/** A finished game (won or lost) in `ageGroup`; `rank`: its rank value (hardest right answer, 0 if none). @internal until task 1980 wires it */
export const countEnd = (c: PlayerCareer, ageGroup: string, rank: number): PlayerCareer => ({
  ...c, years: { ...c.years, [ageGroup]: (c.years[ageGroup] ?? 0) + 1 }, ranks: [...c.ranks, rank].slice(-RANKS_KEPT),
});

/** The badges reached and not yet held, in live order. @internal until task 1980 wires it */
export const newBadges = (c: PlayerCareer): string[] => BADGES.filter((b) => !c.badges[b.name] && b.met(c)).map((b) => b.name);

/** The career with its new badges held from `on`; a badge is never removed. @internal until task 1980 wires it */
export function award(c: PlayerCareer, on: string): PlayerCareer {
  const names = newBadges(c);
  return names.length ? { ...c, badges: { ...c.badges, ...Object.fromEntries(names.map((n) => [n, { on }])) } } : c;
}

/** Rank value: weighted mean of the ranks (newest last; weights 10..1 newest first), half up, at least 1; null without games. @internal until task 1980 wires it */
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

/** Index into the 15 rank names (0-based), null without games. @internal until task 1980 wires it */
export const rankIndex = (ranks: readonly number[]): number | null => {
  const r = rankOf(ranks);
  return r === null ? null : Math.min(r, RANK_NAMES) - 1;
};
