# 24 — Career: Subjects, Grades, Badges, Score and Rank

**Status:** agreed (design only; no code yet)

The career gives each player a long-term sense of progress: school-style subjects with grades that rise with harder questions, badges for it, a lifelong score and a rank with a name that follows the last ten games. It is the design of `plan 193: Career design: subjects, grades and badge list` (part 1 of `plan 192: masterplan`, `milestone 20: give a player a sense of progress`); parts 2 to 7 build on this file and need no other source.

- Decisions: `decision 517: Career subjects: which school subjects, and which categories in each?` (subjects), `decision 521: Career badge list, revised: 39 badges, score and rank: which score milestones?` (badges, score, rank, final).
- `decision 519: Career badge list: grades, rules, 29 badges with names and thresholds?` is superseded by decision 521; it still holds for grades and bands, «this band or harder», every correct answer, per-player counting. No longer holds: the order rule, the 29 count, the description suffixes «con primaria aprobada» / «after Elementary School» / «nach der Grundschule».
- Figures behind the thresholds: decisions 517, 519, 521 and `work/career/` (gitignored cache).

## Binding constraints (`plan 192: masterplan`)
- Every badge is also a Steam achievement; not the reverse.
- Qualifying games only (`decision 19: Default mode: presets, checkpoints and won levels (OQ-30)?`, `qualifies()` in `app/client/src/engine/achievements.ts`); gamemaster mode earns nothing (`decision 74: Gamemaster mode earns no achievements`); mods allowed (`decision 123: Achievements in games with mods on: allowed or off?`); demo earns nothing (`decision 346: Achievements in the demo: off, as Valve recommends?`, `decision 516: Do games played in the demo count toward the career after buying the full game?`).
- Existing (funny, per account) achievements stay; the career adds to them. Funny ones that stay: `SPECIALIST` (50 right in one category), `QUESTIONS_1000` (distinct questions seen), `WIN_ADULTS`, `WIN_ALL_AGES` (wins), `GAME_NIGHTS` (days played). None counts points or ranks, so no overlap.
- Career is per player (`PlayerRow`); Steam is per account: any player's badge unlocks for the account (`decision 285: Achievements from multiplayer sessions: every seat earns for the save; tower achievements need a win at the top level`).
- Each seat earns from its own answers (`history[].seat`, `rr-competitive` seat states); shared `rr-coop` answers: part 3's plan settles it, the simulation counts solo play.
- Enabled by default; a player can turn it off: still counted, hidden (`decision 515: Career turned off: what happens to a player's progress and badges?`); score and rank too.
- DLC adds no badges and changes none: fixed subject list, DLC categories map onto it, every badge reachable with the base bundle alone.

## Subjects
- 7 fixed subjects; every question counts for the subject of its category. Source: `decision 517`; machine form `work/career/subjects.json` (category → subject id; regional/topic categories as `<bundle>/<category>`), to be moved into the data by `plan 192: masterplan` part 2.
- Base categories (28):

| id | es | en | de | categories |
|---|---|---|---|---|
| `history` | Historia y humanidades | History and humanities | Geschichte und Geisteswissenschaften | history, myths-and-legends, languages-and-words, religion-and-philosophy |
| `geography` | Geografía y sociedad | Geography and society | Geografie und Gesellschaft | world-geography, architecture-and-landmarks, holidays-and-traditions, food-and-drink, money-and-currencies |
| `nature` | Ciencias naturales | Natural sciences | Naturkunde | animals, pets-and-farm, plants-and-environment, human-body, planet-earth, amazon |
| `science` | Ciencia y tecnología | Science and technology | Naturwissenschaft und Technik | science-and-maths, space, inventions-and-technology, transport |
| `arts` | Literatura y artes | Literature and the arts | Literatur und Kunst | art-and-literature, music, fashion-and-design |
| `media` | Comunicación audiovisual | Media studies | Medienkunde | film-tv-and-superheroes, video-games, brands-and-logos |
| `sport` | Deporte y juegos | Sport and games | Sport und Spiele | sports, football, games-and-curiosities |

- es-ES uses the es names.
- Add-on categories map onto the same subjects, no new subject:
  - Regional (colombia, mexico, spain, germany, uk, usa): geography, symbols, food-and-drink, festivals-and-traditions, daily-life → `geography`; nature → `nature`; history, ancient-mexico, east-germany, people, myths-and-legends, how-people-speak, how-colombia-speaks → `history`; music-and-dance, art-and-literature → `arts`; film-and-television, comedy → `media`; sports → `sport`
  - Topic bundles: `geography` bundle (all) → `geography`; `history` bundle → `history`; `movies` → `media`; `sports` → `sport`; `stem`: living-things, ecology, human-body, earth-science → `nature`; physics, chemistry, space, mathematics, technology-and-engineering, history-of-science → `science`
  - Unmapped category (a new bundle): no subject, counts for score and rank only; `qgen validate` should flag it (part 2)
- Rejected: 6 subjects (nature + science merged), 8 subjects (languages and philosophy split off; 48–84 questions per band, unreachable).

## Grades and bands
- Bands on the 1–15 difficulty scale (1 = a 6-year-old, 10 = a 16-year-old, 15 = specialists; `app/data/age-groups.json`). A grade counts its band **or harder**: an adult's answers at 5–15 also count for Primaria. Exact bands would lock adults out of Primaria (no 1–4 in their window).
- **No order between grades**: any badge as soon as its own count is reached, no lower grade needed.

| grade | id | band | es | es-ES | en | de |
|---|---|---|---|---|---|---|
| 1 | `elementary` | 1–4 | Primaria | Primaria | Elementary School | Grundschule |
| 2 | `middle` | 5–8 | Secundaria | ESO | Middle School | Mittelstufe |
| 3 | `high` | 9–12 | Bachillerato | Bachillerato | High School | Oberstufe |
| 4 | `college` | 13–15 | Universidad | Universidad | College | Universität |

- en is US English, so «College» stands alone, no «University».
- Grade 4 has no per-subject badge: 48–216 questions per subject at 13–15, 0.03–0.07 right per game; one badge across all subjects.

## Counting rules
- **Every correct answer**, not distinct questions: games differ by at most 7 at these thresholds; the save needs counters only, no id lists: per player × subject × grade (`elementary`, `middle`, `high`, `college`) correct answers, per player × age group finished games, per player the score and the last 10 rank values.
- An answer counts for every grade whose band it reaches: difficulty d counts for grades with band floor ≤ d (1+, 5+, 9+, 13+).
- Only qualifying games; demo and gamemaster mode excluded; counted per seat/player; add-on categories count for their subject.
- Counted and hidden while the career is off.
- A badge stays once earned (also a score badge when the score later drops).

## Badges: 39
- 21 subject × grade; 3 diplomas; 1 college; 4 school years; 10 score.
- Texts follow the existing achievement style (infinitive descriptions, `steam-achievements.vdf`); Steam texts (`steam-achievements.vdf`) are part 4's work, UI catalogs part 5's. Texts below are approved (decision 521); `<n>` thresholds can change, names and count can't once entered in Steamworks.
- Grade-specific descriptions: replace the grade word and number: es «de nivel primaria / secundaria / bachillerato o superior», en «elementary / middle school / high school level or harder», de «Grundschulniveau / Mittelstufenniveau / Oberstufenniveau oder schwerer».

### Subject × grade (21): `CAREER_<SUBJECT>_<GRADE>`
- Grade 1 `ELEMENTARY`: 15 right at difficulty 1+; grade 2 `MIDDLE`: 25 right at 5+; grade 3 `HIGH`: 15 right at 9+. Harder grades need fewer: the supply thins out.
- Subject ids upper case: `HISTORY`, `GEOGRAPHY`, `NATURE`, `SCIENCE`, `ARTS`, `MEDIA`, `SPORT`.
- Name: «`<grade>`: `<subject>`»; example `CAREER_HISTORY_ELEMENTARY`:
  - es «Primaria: Historia y humanidades» / «Acertar 15 preguntas de historia y humanidades de nivel primaria o superior.»
  - en «Elementary School: History and Humanities» / «Answer 15 History and Humanities questions right, elementary level or harder.»
  - de «Grundschule: Geschichte und Geisteswissenschaften» / «15 Fragen aus Geschichte und Geisteswissenschaften richtig beantworten, Grundschulniveau oder schwerer.»

### Diplomas (3): a grade's badge in all 7 subjects
| API | es | es-ES | en | de | trigger |
|---|---|---|---|---|---|
| `CAREER_DIPLOMA_ELEMENTARY` | «Primaria completa» / «Aprobar primaria en las 7 asignaturas.» | = es | «Elementary School Graduate» / «Pass Elementary School in all 7 subjects.» | «Grundschulabschluss» / «Die Grundschule in allen 7 Fächern bestehen.» | all 7 `*_ELEMENTARY` |
| `CAREER_DIPLOMA_MIDDLE` | «Secundaria completa» / «Aprobar secundaria en las 7 asignaturas.» | «Graduado en ESO» / «Aprobar secundaria (ESO) en las 7 asignaturas.» | «Middle School Graduate» / «Pass Middle School in all 7 subjects.» | «Mittlere Reife» / «Die Mittelstufe in allen 7 Fächern bestehen.» | all 7 `*_MIDDLE` |
| `CAREER_DIPLOMA_HIGH` | «Título de bachiller» / «Aprobar bachillerato en las 7 asignaturas.» | = es | «High School Diploma» / «Pass High School in all 7 subjects.» | «Abitur» / «Die Oberstufe in allen 7 Fächern bestehen.» | all 7 `*_HIGH` |

### College (1): `CAREER_COLLEGE`
- es, es-ES «Universidad» / «Acertar 15 preguntas de nivel universitario.»; en «College» / «Answer 15 college-level questions right.»; de «Universität» / «15 Fragen auf Universitätsniveau richtig beantworten.»
- Trigger: 15 right at difficulty 13+, any subject (no diploma needed).

### School years (4): `CAREER_YEAR_<AGEGROUP>`
- `KIDS`, `YOUNG_TEENS`, `YOUNG_ADULTS`, `ADULTS`; trigger: 20 qualifying games played to the end (won or lost) in that age group, per player. The lowest difficulty (Kids) earns one, as the milestone asks; played, not won: it rewards coming back (`WIN_ALL_AGES` rewards winning).
- Age group names from `app/data/names.<locale>.json` (es Niños/Adolescentes/Jóvenes/Adultos; en Kids/Teens/Young adults/Adults; de Kinder/Jugendliche/Junge Erwachsene/Erwachsene).
- Kids: es «Año escolar: Niños» (es-ES «Curso escolar: Niños») / «Jugar 20 partidas completas en el grupo de edad Niños.»; en «School Year: Kids» / «Finish 20 games in the Kids age group.»; de «Schuljahr: Kinder» / «20 Spiele in der Altersgruppe Kinder zu Ende spielen.»; the others the same pattern.

### Score (10): `CAREER_SCORE_<N>`
- Milestones: **100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000** (the developer's first list 10…10000 was replaced by this one: a typical adult takes the first in an evening and the last in about two years of weekly play).
- Trigger: score ≥ N once (a badge stays when the score drops).
- Names: es «1000 puntos» / «Llegar a 1000 puntos.»; en «1,000 Points» / «Reach 1,000 points.»; de «1000 Punkte» / «1000 Punkte erreichen.»; number format per locale.

### Live order (Steam)
- Fixed order, one flat list, grade-major: the 21 subject × grade (grade 1 subjects in the order of the subject table, then grade 2, then grade 3), 3 diplomas, `CAREER_COLLEGE`, 4 school years (kids first), 10 score (ascending). New badges are appended, never inserted.

## Score
- Per player, for good: right answer +difficulty² (1 → 1, 5 → 25, 10 → 100, 15 → 225); wrong answer −1; negative possible.
- Same games as the badges (qualifying, not demo, not gamemaster); counted while the career is off, hidden.
- Career on: shown after every answer (on the answer result screens), counting up (or down by 1 after a wrong answer) to the new total, animated; reaching a milestone triggers the badge celebration (see below).
- Points per game, slowest locale: kids typical 42 · strong 183; young teens 99 · 466; young adults 258 · 948; adults 335 · 1217.

## Rank
- Per finished game (12 right, or ended by a wrong answer; unfinished games don't count): one value, the difficulty of the hardest question answered right, 0 if the first was wrong. A game has 12 questions; the value is on the 1–15 scale.
- **A win counts as the top of the age group's window**: adults 15, young adults 13, young teens 10, kids 6. Without it the last level is a random draw and an always-winning adult sits at ≈ 14.
- Rank = weighted average over the last 10 finished games, weights 10 (newest) down to 1 (oldest) (newest ≈ 18 %, oldest ≈ 2 %); fewer than 10 games: the same weights over those games.
- Shown rounded half up, at least 1, with its name; none before the first finished game. Updated only when a game ends; animated (bar moves to the new value, the name changes when a whole number is crossed).
- Kids top out at rank 6, young teens 10, young adults 13, adults 15.
- Label: es «Rango», en «Rank», de «Rang».
- Where players settle (mean per game, all locales): kids typical 3 · strong 6; young teens 5 · 10; young adults 8 · 13; adults 9 · 15.

| rank | es, es-ES | en | de |
|---|---|---|---|
| 1 | Principiante | Beginner | Neuling |
| 2 | Aprendiz | Apprentice | Lehrling |
| 3 | Estudiante | Student | Schulkind |
| 4 | Aspirante | Contender | Prüfling |
| 5 | Promesa | Up-and-Comer | Nachwuchstalent |
| 6 | Talento | Talent | Talent |
| 7 | Prodigio | Prodigy | Wunderkind |
| 8 | Referente | Role Model | Vorbild |
| 9 | Lumbrera | Bright Mind | Kapazität |
| 10 | Autoridad | Authority | Autorität |
| 11 | Eminencia | Luminary | Koryphäe |
| 12 | Genio | Genius | Genie |
| 13 | Fenómeno | Phenomenon | Phänomen |
| 14 | Leyenda | Legend | Legende |
| 15 | Enciclopedia viviente | Walking Encyclopedia | Lebendes Lexikon |

- Person titles only where they work for everyone (de: no gendered masculine).

## Badge page and celebration (milestone 20)
- A badge page lists all badges (earned and open) per player; it opens with celebration, sound and animation when a new badge is earned. Design and screens: part 3 (`plan 192: masterplan`).

## Age-group reach
- Windows (`app/data/age-groups.json`): kids 1–6, young teens 1–10, young adults 4–13, adults 5–15.
- Games to the badge, slowest locale, typical player, 1 player (4 players on one save within 15 %):

| age group | grade 1 | grade 2 | grade 3 | diplomas 1 / 2 / 3 | college |
|---|---|---|---|---|---|
| kids | 16–31 | strong only (37–74) | – | 31 / – / – | – |
| young teens | 19–33 | 65–109 | strong only (36–68) | 33 / 109 / – | – |
| young adults | 21–34 | 38–69 | 68–154 | 34 / 69 / 154 | strong only (≈19) |
| adults | 19–28 | 30–54 | 44–84 | 28 / 54 / 84 | ≈120–165 |

- Strong players get each grade within a few weeks (adults: everything within ~20 games). Kids reach grade 2 only as strong players; typical young adults never reach college (13 is their window's top). Everyone grows into the next grade by moving up an age group.
- Slowest: grade 3 sport for typical young adults (154 games), grade 2 sport, arts, science for typical young teens (106–121).
- School years: 20 games, any age group, locale, player count. A year of family evenings ≈ 100–150 games per player.

## Steam budget
- Valve's limits (checked 2026-10-31): 5,000 achievements per app, 100 until the app is vetted; 40 sets per app; archived achievements count toward the limit; Achievement Sets are beta (Steam will not unlock an achievement in a DLC set for a player who can't play it), so career badges stay in the base set. Sources: Valve, "Step by Step: Achievements" (https://partner.steamgames.com/doc/features/achievements/ach_guide), "Stats and Achievements" (https://partner.steamgames.com/doc/features/achievements), "Profile Features" (https://partner.steamgames.com/doc/marketing/profile).
- Design for 5,000. The count is set by the design and the supply of questions, not by the 100.
- Until vetted, at most 100 live: the 39 existing achievements first (28 in `ACHIEVEMENTS` + 6 regional + 5 topic `BUNDLE_*`), then career badges in the fixed live order above, up to 100. Count live and pending together.
- Today: 39 + 39 = **78 of 100**, 22 left; a badge past 100 is earned and shown in game, its Steam achievement is added once vetted, the retroactive unlock on load (part 4) grants it.
- No trial badges: an archived achievement still counts, entered means for good. The old cap of 40 career badges is dropped (developer, `task 1890`).
- Rows for Steamworks: `plans/18-steam-integration.md` "Achievements in Steamworks"; the badge rows come from part 4.

## Supply figures
- `qgen report --career [--subjects FILE] [--locale …] [--json]` (needs Node, dev shell): per category × band supply and games-to-N from the engine sessions (`authoring/tools/sim/career.ts`); output of 2026-11-04 in `work/career/supply-categories.md`.

## Parts (`plan 192: masterplan`)
- Part 2 subjects in the data; part 3 and later: engine and save, badge page, Steam, UI texts; they read this file.
