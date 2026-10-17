// The demo's question list (plan 174, decision 339): the engine's supply check over every demo configuration and the
// picker that sizes and fills the list; rules from game.ts and selection.ts (D-60), nothing re-implemented.
// stdin: {cmd: "sizes" | "propose" | "check", candidates, locales, shares, seats?, ids?}; stdout: JSON per cmd (`main`).
// Deterministic: no time, no random; ties by question id. Empty save: seen counts 0, nothing blocked.
//
// Joker reserve R: fresh questions one game can pull at one level on top of its cards (game.ts):
//   «Paso» (playSkip → backToSelect) 1, «Bájale» (playEasier) 1, «Cambiazo» (playCategory) 1,
//   «Francotirador» hit (playSnipe: the level again) a new table = cards, Gamemaster «Cambiar pregunta» (replaceCurrent) 1;
//   «Soplo» draws nothing → R = cards + 4 = 8 at 4 cards. «Bájale»'s pick may lie below the range: counted at the level.
//   Timed has no jokers (timed_no_jokers): R = 0; its sudden death (decision 281) adds up to LIVES rounds of every seat
//   at the last level. R at one level of one seat at a time.
import { readFileSync } from "node:fs";
import ageGroupsJson from "../../app/data/age-groups.json" with { type: "json" };
import bundlesJson from "../../app/data/bundles.json" with { type: "json" };
import { LIVES, rangesFor, resolveChoice } from "../../app/client/src/engine/choice.ts";
import { availableFor, sessionSupply, supply } from "../../app/client/src/engine/game.ts";
import { parseAgeGroups, parseBundles, type LevelRanges, type PoolQuestion } from "../../app/client/src/engine/pool.ts";
import * as selection from "../../app/client/src/engine/selection.ts";
import { emptySave, engineData, type EngineData } from "../../app/client/src/engine/state.ts";
import type { Choice, Supply } from "../../app/client/src/lib/types.ts";

type Media = "image" | "audio" | "video" | null;
interface Cand {
  id: string;
  subcategory: string;
  category: string;
  media: Media;
  /** Approved in every launch locale; else pending (missing translations). */
  full: boolean;
  /** Per locale: the translation's difficulty, else the source's. */
  difficulty: Record<string, number>;
}
interface Input {
  cmd: "sizes" | "propose" | "check";
  candidates: Cand[];
  locales: string[];
  /** Approved base pool: share per category, audio + video share. */
  shares: { categories: Record<string, number>; av: number };
  seats?: number;
  max_seats?: number;
  ids?: string[];
}
type Kind = "game" | "rr-competitive" | "timed";
interface Config { kind: Kind; groups: string[]; media: boolean }

const RESERVE_EXTRA = 4;
const groups = parseAgeGroups(ageGroupsJson);
const groupIds = groups.map((g) => g.id);
const bundles = parseBundles(bundlesJson);
const save = emptySave();
const byId = (a: { id: string }, b: { id: string }) => a.id.localeCompare(b.id, "en", { numeric: true });
const isAV = (c: Cand) => c.media === "audio" || c.media === "video";

const dataFor = (list: Cand[], locale: string): EngineData =>
  engineData(list.map((c) => ({
    id: c.id, status: "approved", difficulty: c.difficulty[locale], subcategory: c.subcategory, bundle: "base", media: { type: c.media },
  }) as unknown as PoolQuestion), [], bundles, groups, "es");

const choiceOf = (data: EngineData, group: string, media: boolean): Choice =>
  resolveChoice(data, { age_group: group, bundles: ["base"], video: media, audio: media });

function name(c: Config): string {
  const what = c.kind === "game" ? `solo / gamemaster / rr-coop, ${c.groups[0]}`
    : c.kind === "timed" ? `timed, ${c.groups.length} × ${c.groups[0]}` : `rr-competitive, ${c.groups.join(" + ")}`;
  return c.media ? what : `${what}, media off`;
}

/** Multisets of `n` age groups, groups.json order. */
function multisets(n: number, from = 0): string[][] {
  if (n === 0) return [[]];
  return groupIds.slice(from).flatMap((g, i) => multisets(n - 1, from + i).map((rest) => [g, ...rest]));
}

/** Every configuration up to `seats` seats; `mixed` false: rr-competitive with one age group per session only. */
function configs(seats: number, media: boolean[], mixed = true): Config[] {
  const out: Config[] = [];
  for (const m of media) {
    for (const g of groupIds) out.push({ kind: "game", groups: [g], media: m });
    for (let n = 2; n <= seats; n++) {
      for (const gs of multisets(n)) if (mixed || new Set(gs).size === 1) out.push({ kind: "rr-competitive", groups: gs, media: m });
      for (const g of groupIds) out.push({ kind: "timed", groups: Array<string>(n).fill(g), media: m });
    }
  }
  return out;
}

const cardsOf = (c: Config, choice: Choice) => (c.kind === "timed" ? c.groups.length : choice.cards);
const reserveOf = (c: Config, choice: Choice) => (c.kind === "timed" ? 0 : choice.cards + RESERVE_EXTRA);

/** The engine's own check of a session start (newGame / newSession). */
function engineCheck(c: Config, data: EngineData): Supply {
  const choice = choiceOf(data, c.groups[0], c.media);
  if (c.kind === "game") return supply(save, data, choice);
  return sessionSupply(save, data, c.kind, choice, c.groups.length, c.groups);
}

type Range = readonly [number, number];

/** One range per slot: every seat's levels × cards, timed's sudden death, R more of range `reserve`. */
function slots(c: Config, data: EngineData, reserve?: Range): LevelRanges {
  const choice = choiceOf(data, c.groups[0], c.media);
  const cards = cardsOf(c, choice);
  const seats = c.kind === "timed" ? [c.groups[0]] : c.groups;
  const out: Range[] = [];
  for (const g of seats) {
    const ranges = rangesFor(data, { ...choice, age_group: g });
    ranges.forEach((r, i) => {
      const n = cards + (c.kind === "timed" && i === ranges.length - 1 ? LIVES * c.groups.length : 0);
      for (let k = 0; k < n; k++) out.push(r);
    });
  }
  if (reserve) for (let k = 0; k < reserveOf(c, choice); k++) out.push(reserve);
  return out;
}

/** Ranges a reserve is checked at: the seats' level ranges that hold no other (a wider one passes when a narrower
 * one does: its slots take any question the narrower one's could); none in timed. */
function reserves(c: Config, data: EngineData): Range[] {
  if (c.kind === "timed") return [];
  const all = [...new Map(c.groups.flatMap((g) => rangesFor(data, { age_group: g, difficulty: null, levels: selection.LEVELS }))
    .map((r) => [r.join(), r] as const)).values()];
  return all.filter(([lo, hi]) => !all.some(([a, b]) => lo <= a && b <= hi && (a !== lo || b !== hi)));
}

/** Ranges of the slots the matching leaves empty (selection.supply, one slot per level). */
function short(c: Config, data: EngineData, reserve?: Range): [number, number][] {
  const avail = availableFor(save, data, choiceOf(data, c.groups[0], c.media));
  return selection.supply(avail, slots(c, data, reserve), 1).flatMap((l) => (l.missing ? [l.range] : []));
}

interface Row { config: string; locale: string; engine: boolean; reserve: boolean; reserve_short: number }

function checkOne(c: Config, data: EngineData, locale: string): Row {
  const engine = engineCheck(c, data).ok;
  let worst = 0;
  for (const r of reserves(c, data)) worst = Math.max(worst, short(c, data, r).length);
  if (c.kind === "timed") worst = short(c, data).length;
  return { config: name(c), locale, engine, reserve: engine && worst === 0, reserve_short: worst };
}

/** Rows per configuration (media on and off) × locale; a media-on row is skipped when its media-off row passes. */
function check(list: Cand[], locales: string[], seats: number): Row[] {
  const out: Row[] = [];
  for (const locale of locales) {
    const data = dataFor(list, locale);
    const off = configs(seats, [false]).map((c) => checkOne(c, data, locale));
    const on = configs(seats, [true]).map((c, i) => (off[i].reserve ? { ...off[i], config: name(c) } : checkOne(c, data, locale)));
    out.push(...on, ...off);
  }
  return out;
}

/** The list for `seats`: per configuration (media off, which covers media on) and locale the matching's minimum,
 * then the reserves, then audio and video up to the pool's share; candidates by `Picker.key`. */
class Picker {
  list: Cand[] = [];
  private inList = new Set<string>();
  private perDifficulty = new Map<string, number>();
  private perSub = new Map<string, Cand[]>();
  private perCategory = new Map<string, number>();
  added = new Map<string, number>();
  unmet = new Set<string>();

  private cands: Cand[];
  private input: Input;
  private k: number;

  constructor(cands: Cand[], input: Input, k: number) {
    this.cands = cands;
    this.input = input;
    this.k = k;
  }

  add(c: Cand, by: string): void {
    this.list.push(c);
    this.inList.add(c.id);
    for (const [l, d] of Object.entries(c.difficulty)) this.perDifficulty.set(`${l}:${d}`, (this.perDifficulty.get(`${l}:${d}`) ?? 0) + 1);
    this.perSub.set(c.subcategory, [...(this.perSub.get(c.subcategory) ?? []), c]);
    this.perCategory.set(c.category, (this.perCategory.get(c.category) ?? 0) + 1);
    this.added.set(by, (this.added.get(by) ?? 0) + 1);
  }

  /** Full first; subcategories under k; the difficulty furthest below the group's level_weights; the category
   * furthest below its pool share; the emptiest subcategory, a «Bájale» partner (other difficulty) as good as a new one;
   * id (candidates come sorted). */
  private key(c: Cand, locale: string, weights: Readonly<Record<string, number>> | null): number[] {
    const d = c.difficulty[locale];
    const subs = this.perSub.get(c.subcategory) ?? [];
    const pair = subs.some((x) => x.difficulty[locale] !== d);
    return [
      c.full ? 0 : 1, subs.length >= this.k ? 1 : 0,
      weights ? (this.perDifficulty.get(`${locale}:${d}`) ?? 0) / (weights[d] ?? 1) : 0,
      ((this.perCategory.get(c.category) ?? 0) + 0.5) / (this.input.shares.categories[c.category] || 1e-9),
      subs.length - (pair ? 1 : 0),
    ];
  }

  best(ok: (c: Cand) => boolean, locale: string, weights: Readonly<Record<string, number>> | null): Cand | null {
    let top: Cand | null = null, topKey: number[] = [];
    for (const c of this.cands) {
      if (this.inList.has(c.id) || !ok(c)) continue;
      const key = this.key(c, locale, weights);
      const cmp = top === null ? -1 : key.reduce((acc, v, i) => acc || v - topKey[i], 0);
      if (cmp < 0) [top, topKey] = [c, key];
    }
    return top;
  }

  /** Add candidates until `c` at `locale` leaves no slot empty (each one fills an empty slot). */
  fill(c: Config, locale: string, reserve?: Range): void {
    const weights = groups.find((g) => g.id === c.groups[0])!.level_weights;
    for (;;) {
      const missing = short(c, dataFor(this.list, locale), reserve);
      let n = 0;
      for (const [lo, hi] of missing) {
        const q = this.best((x) => !isAV(x) && lo <= x.difficulty[locale] && x.difficulty[locale] <= hi, locale, weights);
        if (q) this.add(q, name(c)), n++;
      }
      if (n < missing.length) this.unmet.add(name(c));
      if (!missing.length || !n) return;
    }
  }

  run(seats: number): void {
    const all = configs(seats, [false]);
    const homogeneous = configs(seats, [false], false);
    const order = [...homogeneous, ...all.filter((c) => !homogeneous.some((h) => name(h) === name(c)))];
    for (const locale of this.input.locales) for (const c of order) this.fill(c, locale);
    for (const locale of this.input.locales) for (const c of order) {
      for (const r of reserves(c, dataFor(this.list, locale))) this.fill(c, locale, r);
    }
    const { av } = this.input.shares;
    const want = Math.round((av * this.list.length) / (1 - av));
    for (let i = 0; i < want; i++) {
      const q = this.best(isAV, this.input.locales[0], null);
      if (!q) break;
      this.add(q, "audio and video share");
    }
  }
}

/** Two passes: the first sizes the list, the second caps a subcategory at k = ⌈size / subcategories⌉, at least 2
 * («Bájale» needs a pair). */
function propose(input: Input, seats: number): Picker {
  const cands = [...input.candidates].sort(byId);
  const first = new Picker(cands, input, Infinity);
  first.run(seats);
  const subs = new Set(cands.map((c) => c.subcategory)).size;
  const second = new Picker(cands, input, Math.max(2, Math.ceil(first.list.length / subs)));
  second.run(seats);
  return second;
}

/** Share of listed questions with an easier one of their subcategory in the list (per locale). */
function easierShare(list: Cand[], locale: string): number {
  if (!list.length) return 0;
  const has = list.filter((q) => list.some((x) => x.subcategory === q.subcategory && x.difficulty[locale] < q.difficulty[locale]));
  return has.length / list.length;
}

function summary(p: Picker, seats: number) {
  const list = [...p.list].sort(byId);
  const binding = [...p.added].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0]?.[0] ?? null;
  return {
    seats, size: list.length, full: list.filter((c) => c.full).length, pending: list.filter((c) => !c.full).length,
    binding, unmet: [...p.unmet].sort(), ids: list.map((c) => c.id), added: Object.fromEntries(p.added),
  };
}

function main(): unknown {
  const input = JSON.parse(readFileSync(0, "utf8")) as Input;
  const meta = {
    reserve: { cards: selection.PER_LEVEL, r: selection.PER_LEVEL + RESERVE_EXTRA, sudden_death_rounds: LIVES },
    groups: Object.fromEntries(groups.map((g) => [g.id, g.level_weights])),
  };
  if (input.cmd === "sizes") {
    return Array.from({ length: input.max_seats ?? 5 }, (_, i) => {
      const { ids: _ids, added: _added, ...rest } = summary(propose(input, i + 1), i + 1);
      return rest;
    });
  }
  const seats = input.seats ?? 1;
  if (input.cmd === "propose") {
    const p = propose(input, seats);
    return {
      ...summary(p, seats), ...meta, rows: check(p.list, input.locales, seats),
      easier: Object.fromEntries(input.locales.map((l) => [l, easierShare(p.list, l)])),
    };
  }
  const wanted = new Set(input.ids ?? []);
  const list = input.candidates.filter((c) => wanted.has(c.id)).sort(byId);
  const rows = check(list, input.locales, seats);
  return {
    ...meta, seats, size: list.length, rows, ok: rows.every((r) => r.reserve),
    easier: Object.fromEntries(input.locales.map((l) => [l, easierShare(list, l)])),
  };
}

console.log(JSON.stringify(main()));
