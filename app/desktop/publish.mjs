// Publishing (plan 119): mod folder → Workshop item. Pure Node: no Electron, no binding import; the folder is only read and copied.
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { isDeepStrictEqual } from "node:util";
import { checkMod, errorText } from "./check-mod.mjs";
import { readManifest } from "./mods.mjs";
import { contained } from "./resolve.mjs";

// Decision 135's proposed list (unanswered): kinds + locales, as entered in Steamworks.
export const WORKSHOP_TAGS = ["bundle", "theme", "code", "conversion", "es", "en", "de"];
export const VISIBILITY = { public: 0, friends: 1, private: 2, unlisted: 3 };
const PREVIEWS = ["preview.png", "preview.jpg", "preview.gif"];
const MB = 1024 * 1024;
const COMMUNITY = 0; // EWorkshopFileType
const INVALID_HANDLE = 0xffffffffffffffffn;
const SUBMIT_WAIT_MS = 29_000; // the binding gives up after 30 s; Steam may still upload
const LEGAL = "https://steamcommunity.com/sharedfiles/workshoplegalagreement";
const STATUS = ["", "preparing config", "preparing content", "uploading", "uploading preview", "committing"];

export const itemUrl = (id) => `https://steamcommunity.com/sharedfiles/filedetails/?id=${id}`;
const legal = () => `legal agreement: the item stays hidden until you accept it at ${LEGAL}`;
const mb = (n) => (Number(n) / MB).toFixed(1);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Copies the folder's files into dest: no dot files/folders, symlinks only inside the folder. */
async function stage(src, dest, warnings) {
  const root = await fs.realpath(src);
  let files = 0;
  let bytes = 0;
  const walk = async (rel, chain) => {
    const entries = await fs.readdir(path.join(src, rel), { withFileTypes: true });
    for (const e of entries.sort((a, b) => (a.name < b.name ? -1 : 1))) {
      if (e.name.startsWith(".")) continue;
      const r = rel ? `${rel}/${e.name}` : e.name;
      const to = path.join(dest, r);
      let real = null;
      if (e.isSymbolicLink()) {
        real = await fs.realpath(path.join(src, r)).catch(() => null);
        if (!real || (real !== root && !real.startsWith(root + path.sep))) {
          warnings.push(`symlink ${r} points outside the mod folder, skipped`);
          continue;
        }
      }
      const s = await fs.stat(path.join(src, r));
      if (s.isDirectory()) {
        real ??= await fs.realpath(path.join(src, r));
        if (chain.has(real)) {
          warnings.push(`symlink ${r} loops, skipped`);
          continue;
        }
        await fs.mkdir(to);
        await walk(r, new Set([...chain, real]));
      } else if (s.isFile()) {
        const file = await contained(src, r);
        if (!file) continue;
        await fs.copyFile(file, to);
        files++;
        bytes += s.size;
      }
    }
  };
  await walk("", new Set([root]));
  return { files, bytes };
}

/**
 * Steps 1–5: validate, preview, stage, tags. → { error, warnings } or the prepared item;
 * `dispose()` removes the staged copy (already gone on error). `roots`: checkMod's `{ dist, data }`.
 */
export async function preparePublish(folder, gameVersion, roots) {
  const mod = await readManifest(folder, gameVersion);
  // --check-mod's findings (plan 120): warnings only, the manifest error below still stops.
  const warnings = [];
  await checkMod(folder, { ...roots, gameVersion }, (line, isError) => {
    if (isError) warnings.push(line.trim().replace(/^(error|warning): /, ""));
  });
  if (mod.error) return { error: errorText(mod.error), warnings };
  const m = mod.manifest;

  let preview = null;
  for (const name of PREVIEWS) {
    const file = await contained(mod.dir, name);
    if (!file) continue;
    const { size } = await fs.stat(file);
    if (size > MB) return { error: `${name} is ${mb(size)} MB, Steam's limit is 1 MB`, warnings };
    preview = { name, bytes: size };
    break;
  }
  if (!preview && !m.workshopId) warnings.push("no preview.png/.jpg/.gif: Steam shows a placeholder");

  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), "trivia-publish-"));
  const dispose = () => fs.rm(tmp, { recursive: true, force: true });
  const staged = path.join(tmp, "content");
  let size;
  try {
    await fs.mkdir(staged);
    size = await stage(mod.dir, staged, warnings);
  } catch (err) {
    await dispose();
    return { error: `staging failed: ${err.message}`, warnings };
  }

  const langs = (m.languages ?? []).map((l) => l.split("-")[0]);
  const tags = [];
  for (const tag of new Set([...mod.kind, ...langs]))
    if (WORKSHOP_TAGS.includes(tag)) tags.push(tag);
    else warnings.push(`tag "${tag}" isn't a Workshop tag, dropped`);

  return {
    error: null,
    warnings,
    folder: mod.dir,
    manifest: m,
    workshopId: m.workshopId ?? null,
    tags,
    preview: preview && { ...preview, file: path.join(staged, preview.name) },
    staged,
    ...size,
    dispose,
  };
}

/** Dry-run summary lines (step 5). */
export function describe(p, opts = {}) {
  const visibility = opts.visibility ?? (p.workshopId ? "unchanged" : "private");
  return [
    `mod ${p.manifest.id} ${p.manifest.version}: ${p.workshopId ? `update item ${p.workshopId}` : "new item"}`,
    `title: ${p.manifest.name}`,
    `description: ${[...p.manifest.description].length} chars`,
    `visibility: ${visibility}`,
    `tags: ${p.tags.join(", ") || "none"}`,
    `preview: ${p.preview ? `${p.preview.name} (${mb(p.preview.bytes)} MB)` : "none"}`,
    `upload: ${p.files} files, ${mb(p.bytes)} MB${opts.contentOnly ? ", content only" : ""}`,
  ];
}

/** Sets `workshopId` in a mod.json: only that key, rest of the text as is; atomic. */
export async function writeWorkshopId(file, id) {
  const text = await fs.readFile(file, "utf8");
  const old = JSON.parse(text);
  const want = { ...old, workshopId: id };
  let next;
  if ("workshopId" in old) next = text.replace(/(^|[^\\])("workshopId"\s*:\s*)"[^"\\]*"/, `$1$2"${id}"`);
  else {
    const end = text.lastIndexOf("}");
    const eol = text.includes("\r\n") ? "\r\n" : "\n";
    const indent = /\n([ \t]+)"/.exec(text)?.[1] ?? "  ";
    next = `${text.slice(0, end).trimEnd()},${eol}${indent}"workshopId": "${id}"${eol}${text.slice(end)}`;
  }
  let ok = false;
  try {
    ok = isDeepStrictEqual(JSON.parse(next), want);
  } catch {}
  if (!ok) next = JSON.stringify(want, null, 2) + "\n";
  const tmp = path.join(path.dirname(file), `.mod.json.${process.pid}.tmp`);
  try {
    await fs.writeFile(tmp, next, "utf8");
    await fs.rename(tmp, file);
  } catch (err) {
    await fs.rm(tmp, { force: true });
    throw err;
  }
}

/** Progress line and its change key (status, 10 % step). */
function progress({ status, bytesProcessed, bytesTotal, percentComplete }) {
  status = Number(status);
  if (!STATUS[status]) return null;
  if (status !== 3) return { key: `${status}`, line: STATUS[status] };
  const step = Math.floor(percentComplete / 10) * 10;
  return { key: `3:${step}`, line: `uploading ${step} % (${mb(bytesProcessed)} / ${mb(bytesTotal)} MB)` };
}

/**
 * Steps 7–10. `ugc`: the binding's `steam.workshop`; opts { changenote, visibility, contentOnly };
 * out(line, isError). → { ok, workshopId, unconfirmed? }.
 */
export async function publish(ugc, appId, p, opts, out) {
  const interval = opts.interval ?? 500;
  const first = !p.workshopId;
  let id = p.workshopId;
  if (first) {
    const created = await ugc.createItem(appId, COMMUNITY);
    if (created == null) {
      out("creating the Workshop item failed", true);
      return { ok: false, workshopId: null };
    }
    id = String(created);
    await writeWorkshopId(path.join(p.folder, "mod.json"), id);
    await writeWorkshopId(path.join(p.staged, "mod.json"), id);
    out(`created item ${id}, ${itemUrl(id)}`);
    out(legal());
  }
  const fail = (line) => {
    out(line, true);
    return { ok: false, workshopId: id };
  };

  const handle = ugc.startItemUpdate(appId, BigInt(id));
  if (BigInt(handle) === INVALID_HANDLE) return fail(`Steam refused to update item ${id}`);
  const m = p.manifest;
  const visibility = opts.visibility ?? (first ? "private" : null);
  const steps = [["content", () => ugc.setItemContent(handle, p.staged)]];
  if (!opts.contentOnly) {
    steps.push(["title", () => ugc.setItemTitle(handle, m.name)]);
    steps.push(["description", () => ugc.setItemDescription(handle, m.description)]);
    steps.push(["tags", () => ugc.setItemTags(handle, p.tags)]);
    if (p.preview) steps.push(["preview", () => ugc.setItemPreview(handle, p.preview.file)]);
  }
  // First publish: private even with --content-only.
  if (visibility) steps.push(["visibility", () => ugc.setItemVisibility(handle, VISIBILITY[visibility])]);
  for (const [what, set] of steps) if (!set()) return fail(`Steam refused the item's ${what}`);

  let last = null;
  const tick = () => {
    const now = progress(ugc.getItemUpdateProgress(handle));
    if (now && now.key !== last) out(now.line);
    last = now?.key ?? last;
  };
  const timer = setInterval(tick, interval);
  const start = Date.now();
  try {
    const ok = await ugc.submitItemUpdate(handle, opts.changenote ?? "");
    if (!ok && Date.now() - start >= SUBMIT_WAIT_MS) {
      while (Number(ugc.getItemUpdateProgress(handle).status) !== 0) await sleep(interval);
      out(`submitted, check the item page: ${itemUrl(id)}`);
      out(legal());
      return { ok: true, workshopId: id, unconfirmed: true };
    }
    if (!ok) return fail(`submitting item ${id} failed`);
  } finally {
    clearInterval(timer);
  }
  out(`published ${itemUrl(id)}`);
  out(legal());
  return { ok: true, workshopId: id };
}
