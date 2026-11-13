// Name and description of a career badge (plan 197, plans/24-career.md): catalog families + data names.
import { BADGE_NAMES, COLLEGE_NEED, GRADE_NEED, SUBJECTS, YEAR_GROUPS, YEAR_NEED } from "../engine/career.ts";
import { formatScore } from "./career-text.ts";
import { catalogFor } from "./i18n.ts";

export interface BadgeNames {
  /** Subject id → name (`names.<question locale>.json`). */
  subjects: Record<string, string>;
  /** Age group id → name (UI language). */
  age_groups: Record<string, string>;
}

const GRADES = ["elementary", "middle", "high"] as const;
type Grade = (typeof GRADES)[number];

const lowerFirst = (s: string) => s.charAt(0).toLowerCase() + s.slice(1);
const SMALL = new Set(["and", "the", "of", "in", "a", "an"]);
/** en names in title case («History and Humanities»). */
const titleCase = (s: string) => s.split(" ").map((w, i) => (i && SMALL.has(w.toLowerCase()) ? w.toLowerCase() : w.charAt(0).toUpperCase() + w.slice(1))).join(" ");

/** The text of badge `id` (`CAREER_…`, career.ts) in UI language `locale`, with the names of `names`; the id itself for an unknown id. */
export function badgeText(id: string, locale: string, names: BadgeNames): { name: string; description: string } {
  const c = catalogFor(locale).career;
  const fill = (text: string, params: Record<string, string | number>) =>
    text.replace(/\{(\w+)\}/g, (m, k: string) => { const v = params[k]; return v === undefined ? m : typeof v === "number" ? formatScore(v, locale) : v; });
  const en = locale === "en";
  const cased = (s: string) => (en ? titleCase(s) : s);
  const text = (t: { name: string; desc: string }, params: Record<string, string | number>) => ({ name: fill(t.name, params), description: fill(t.desc, params) });
  const rest = id.replace(/^CAREER_/, "");

  const sub = SUBJECTS.find((s) => rest.startsWith(`${s.toUpperCase()}_`));
  const grade = sub && GRADES.find((g) => rest === `${sub.toUpperCase()}_${g.toUpperCase()}`);
  if (sub && grade) {
    const subject = cased(names.subjects[sub] ?? sub);
    const gi = GRADES.indexOf(grade);
    const inText = locale.startsWith("es") ? lowerFirst(subject) : subject; // es: «de historia y humanidades»
    return { name: fill(c.subject.name, { grade: c.grade[grade], subject }), description: fill(c.subject.desc[grade], { subject: inText, n: GRADE_NEED[gi] }) };
  }
  const dip = GRADES.find((g) => rest === `DIPLOMA_${g.toUpperCase()}`) as Grade | undefined;
  if (dip) return text(c.diploma[dip], {});
  if (rest === "COLLEGE") return text(c.college, { n: COLLEGE_NEED });
  const year = YEAR_GROUPS.find((g) => rest === `YEAR_${g.toUpperCase()}`);
  if (year) return text(c.year, { group: cased(names.age_groups[year] ?? year), n: YEAR_NEED });
  const score = /^SCORE_(\d+)$/.exec(rest);
  if (score && BADGE_NAMES.includes(id)) return text(c.score, { n: Number(score[1]) });
  return { name: id, description: id };
}
