// Report text (plan 93): one block per flag, the first line machine-readable for `qgen flag`, the rest in the UI language.
import { buildInfo } from "../lib/build.ts";
import { loadEngineData } from "../lib/data.ts";
import type { ReportFields } from "../lib/desktop.ts";
import { t } from "../lib/i18n.ts";
import { questionLocale } from "../lib/names.svelte.ts";
import type { Flagged } from "../lib/types.ts";

const MARK = "\u00a1Trivia!"; // fixed, untranslated

/** The question language: the flag's locale, else es (decision 102). */
const langOf = (f: Flagged) => f.locale ?? "es";

export type Pools = Record<string, string | null>;

/** Pool hash per question language of `flags`: the last engine call's, else that locale's data, else null. */
export async function poolsFor(flags: Flagged[]): Promise<Pools> {
  const langs = [...new Set(flags.map(langOf))];
  const hashes = await Promise.all(langs.map((l) =>
    l === questionLocale() ? buildInfo().pool : loadEngineData(l).then((d) => d.poolHash, () => null)));
  return Object.fromEntries(langs.map((l, i) => [l, hashes[i]]));
}

/** `¡Trivia! #<id> · <lang> · v<version> · pool <hash|?> · <flag date>` */
function header(f: Flagged, pools: Pools): string {
  const pool = pools[langOf(f)] ?? "?";
  return `${MARK} #${f.question_id} · ${langOf(f)} · v${buildInfo().version} · pool ${pool} · ${f.flagged_on.slice(0, 10)}`;
}

/** The human lines without header and note: what `text` sends. */
function body(f: Flagged): string {
  return [`${t("flag.question")}: ${f.question ?? "—"}`, `${t("flag.answer")}: ${f.answer ?? t("flag.hidden")}`].join("\n");
}

function block(f: Flagged, pools: Pools): string {
  return [header(f, pools), body(f), ...(f.note ? [`${t("flag.note")}: ${f.note}`] : [])].join("\n");
}

export const reportText = (flags: Flagged[], pools: Pools) => flags.map((f) => block(f, pools)).join("\n\n");

export function reportFields(f: Flagged, pools: Pools): ReportFields {
  return {
    question: f.question_id,
    lang: langOf(f),
    text: body(f),
    ...(f.note ? { note: f.note } : {}),
    version: buildInfo().version,
    pool: pools[langOf(f)] ?? null,
  };
}

/** Privacy confirm shown once per session, before the first send. */
export const consent = { given: false };
