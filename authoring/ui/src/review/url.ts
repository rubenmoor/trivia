import type { QuestionFilter } from "../lib/api.ts";

// URL: ?batch=pilot&bundle=colombia&id=q-0123, plus the filters status, reviewer, subcategory and
// media=missing (RV-13), licence=replace (plan 53), played=outliers (plan 109); status=!approved is every question that isn't
// approved, across batches (RV-22, D-47). The id follows the current question, so a reload (or a bookmark) comes
// back to it. Decisions themselves live in authoring/data/questions.json.
// With batch: sample=1 is the blind spot check (plan 16), audit=flagged the audit's major findings.
// run=backaudit-<k>: a back-audit run's questions, with the same two (plan 57).
// locale=en|de: the translations next to their Spanish source; media and bundle stay on the source (plan 67).
export function reviewUrl() {
  const params = new URLSearchParams(location.search);
  const locale = params.get("locale") === "es" ? null : params.get("locale");
  const batch = params.get("batch");
  const run = params.get("run");
  /** Where spot checks are recorded: the batch or the back-audit run. */
  const checkGroup = batch ?? run;
  const sampleMode = !!checkGroup && params.get("sample") === "1";
  const bundle = params.get("bundle");
  const filter = {
    batch,
    run,
    bundle,
    status: params.get("status"),
    reviewer: params.get("reviewer"),
    subcategory: params.get("subcategory"),
    media: params.get("media"),
    sample: sampleMode ? "1" : null,
    audit: params.get("audit"),
    licence: params.get("licence"),
    played: params.get("played"),
    locale,
    stale: params.get("stale"),
  } as QuestionFilter;
  /** The licence queue (plan 53): searches ask every provider. */
  const licenceMode = filter.licence === "replace";
  /** Played difficulty outliers (plan 109): open until the difficulty changes or a decision. */
  const playedMode = filter.played === "outliers";
  /** The active filters in words, for the empty and summary screens. */
  const filterText = [
    batch && `batch “${batch}”`,
    run && `run “${run}”`,
    bundle && `bundle “${bundle}”`,
    filter.subcategory && `subcategory “${filter.subcategory}”`,
    filter.status && `status ${filter.status}`,
    filter.reviewer && `reviewed by ${filter.reviewer}`,
    filter.media === "missing" && "without media",
    sampleMode && "spot-check sample",
    filter.audit === "flagged" && "flagged by the audit",
    licenceMode && "licence to replace",
    playedMode && "played difficulty outliers",
    locale && `locale ${locale}`,
    filter.stale === "1" && "stale",
  ]
    .filter(Boolean)
    .join(", ");
  // /review/q-0123: just that one question (linked from the game's admin overlay).
  const singleId = decodeURIComponent(location.pathname.match(/^\/review\/([^/]+)/)?.[1] ?? "") || null;
  const startId = singleId ?? params.get("id");
  // ?debug=keys shows what the browser reports for each key press (for layout problems).
  const debugKeys = params.get("debug") === "keys";
  return { locale, checkGroup, sampleMode, filter, licenceMode, playedMode, filterText, singleId, startId, debugKeys };
}

/** This page in another locale, the other params kept. */
export function localeHref(l: string) {
  const url = new URL(location.href);
  if (l === "es") url.searchParams.delete("locale");
  else url.searchParams.set("locale", l);
  return url.pathname + url.search;
}
