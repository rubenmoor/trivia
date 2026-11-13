import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { BADGE_NAMES } from "../engine/career.ts";
import { namesFiles } from "../engine/state.ts";
import { badgeText, type BadgeNames } from "./badge-text.ts";

const dir = join(import.meta.dirname, "../../../data");
const json = (f: string) => (existsSync(join(dir, f)) ? JSON.parse(readFileSync(join(dir, f), "utf8")) : {});
const groups: { id: string; name: string }[] = json("age-groups.json").groups;

function namesOf(locale: string): BadgeNames {
  const out: BadgeNames = { subjects: {}, age_groups: Object.fromEntries(groups.map((g) => [g.id, g.name])) };
  for (const f of namesFiles(locale)) {
    const n = json(f);
    Object.assign(out.subjects, n.subjects);
    Object.assign(out.age_groups, n.age_groups);
  }
  return out;
}
const text = (id: string, locale: string) => badgeText(id, locale, namesOf(locale));
const LOCALES = ["es", "es-ES", "en", "de"];

// Examples of plans/24-career.md: [id, locale, name, description]
const EXAMPLES: [string, string, string, string][] = [
  ["CAREER_HISTORY_ELEMENTARY", "es", "Primaria: Historia y humanidades", "Acertar 15 preguntas de historia y humanidades de nivel primaria o superior."],
  ["CAREER_HISTORY_ELEMENTARY", "en", "Elementary School: History and Humanities", "Answer 15 History and Humanities questions right, elementary level or harder."],
  ["CAREER_HISTORY_ELEMENTARY", "de", "Grundschule: Geschichte und Geisteswissenschaften", "15 Fragen aus Geschichte und Geisteswissenschaften richtig beantworten, Grundschulniveau oder schwerer."],
  ["CAREER_ARTS_MIDDLE", "en", "Middle School: Literature and the Arts", "Answer 25 Literature and the Arts questions right, middle school level or harder."],
  ["CAREER_SPORT_HIGH", "es", "Bachillerato: Deporte y juegos", "Acertar 15 preguntas de deporte y juegos de nivel bachillerato o superior."],
  ["CAREER_DIPLOMA_ELEMENTARY", "es", "Primaria completa", "Aprobar primaria en las 7 asignaturas."],
  ["CAREER_DIPLOMA_ELEMENTARY", "es-ES", "Primaria completa", "Aprobar primaria en las 7 asignaturas."],
  ["CAREER_DIPLOMA_ELEMENTARY", "en", "Elementary School Graduate", "Pass Elementary School in all 7 subjects."],
  ["CAREER_DIPLOMA_ELEMENTARY", "de", "Grundschulabschluss", "Die Grundschule in allen 7 Fächern bestehen."],
  ["CAREER_DIPLOMA_MIDDLE", "es", "Secundaria completa", "Aprobar secundaria en las 7 asignaturas."],
  ["CAREER_DIPLOMA_MIDDLE", "es-ES", "Graduado en ESO", "Aprobar secundaria (ESO) en las 7 asignaturas."],
  ["CAREER_DIPLOMA_MIDDLE", "en", "Middle School Graduate", "Pass Middle School in all 7 subjects."],
  ["CAREER_DIPLOMA_MIDDLE", "de", "Mittlere Reife", "Die Mittelstufe in allen 7 Fächern bestehen."],
  ["CAREER_DIPLOMA_HIGH", "es", "Título de bachiller", "Aprobar bachillerato en las 7 asignaturas."],
  ["CAREER_DIPLOMA_HIGH", "es-ES", "Título de bachiller", "Aprobar bachillerato en las 7 asignaturas."],
  ["CAREER_DIPLOMA_HIGH", "en", "High School Diploma", "Pass High School in all 7 subjects."],
  ["CAREER_DIPLOMA_HIGH", "de", "Abitur", "Die Oberstufe in allen 7 Fächern bestehen."],
  ["CAREER_COLLEGE", "es", "Universidad", "Acertar 15 preguntas de nivel universitario."],
  ["CAREER_COLLEGE", "es-ES", "Universidad", "Acertar 15 preguntas de nivel universitario."],
  ["CAREER_COLLEGE", "en", "College", "Answer 15 college-level questions right."],
  ["CAREER_COLLEGE", "de", "Universität", "15 Fragen auf Universitätsniveau richtig beantworten."],
  ["CAREER_YEAR_KIDS", "es", "Año escolar: Niños", "Jugar 20 partidas completas en el grupo de edad Niños."],
  ["CAREER_YEAR_KIDS", "es-ES", "Curso escolar: Niños", "Jugar 20 partidas completas en el grupo de edad Niños."],
  ["CAREER_YEAR_KIDS", "en", "School Year: Kids", "Finish 20 games in the Kids age group."],
  ["CAREER_YEAR_KIDS", "de", "Schuljahr: Kinder", "20 Spiele in der Altersgruppe Kinder zu Ende spielen."],
  ["CAREER_SCORE_1000", "es", "1000 puntos", "Llegar a 1000 puntos."],
  ["CAREER_SCORE_1000", "en", "1,000 Points", "Reach 1,000 points."],
  // de groups by locale (Intl: «1.000»), the plan's «1000 Punkte» is a plain-text example of the same
  ["CAREER_SCORE_1000", "de", "1.000 Punkte", "1.000 Punkte erreichen."],
];

test("badgeText matches the examples of plans/24-career.md", () => {
  for (const [id, locale, name, description] of EXAMPLES) assert.deepEqual(text(id, locale), { name, description }, `${id} ${locale}`);
});

test("every badge has its own text in every locale", () => {
  for (const locale of LOCALES) {
    const seen = new Set<string>();
    for (const id of BADGE_NAMES) {
      const { name, description } = text(id, locale);
      assert.ok(name && description && name !== id, `${id} ${locale}`);
      assert.ok(!/[{}⟦]/.test(name + description), `${id} ${locale}`);
      seen.add(name);
    }
    assert.equal(seen.size, BADGE_NAMES.length, locale);
  }
});
