// Dev servers only (task 2053): Chromium (so Electron) doesn't decode Theora .ogv or MPEG-1; the raw cache keeps the original
// and /media serves a WebM copy made on first request (media/playable/<stem>.webm). Packaged builds ship WebM already (stage-media.mjs).
// Same names and args as authoring/tools/media_cache.py playable_path.
import { execFile } from "node:child_process";
import { mkdir, rename, stat } from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";
import { VIDEO } from "./media-formats.mjs";

const run = promisify(execFile);
const NEEDS = new Set([".ogv", ".mpg", ".mpeg", ".mov", ".mkv", ".mp4"]);
const FAST = ["-deadline", "realtime", "-cpu-used", "8"]; // later flags win: a quick encode for a dev look

/** The playable copy's name under the media dir for a cache name, or null when the file plays as is. */
export const playableName = (cacheFile) => {
  const ext = path.extname(cacheFile);
  return NEEDS.has(ext) ? `playable/${cacheFile.slice(0, -ext.length)}.webm` : null;
};

const jobs = new Map();

/** Encodes src to dst once (concurrent requests share the job); a failed encode leaves nothing behind. */
export function ensurePlayable(src, dst) {
  if (!jobs.has(dst)) {
    jobs.set(
      dst,
      (async () => {
        if (await stat(dst).catch(() => null)) return;
        await mkdir(path.dirname(dst), { recursive: true });
        const tmp = `${dst}.part.webm`;
        await run("ffmpeg", ["-nostdin", "-v", "error", "-y", "-i", src, ...VIDEO, ...FAST, "-map_metadata", "-1", tmp]);
        await rename(tmp, dst);
      })().finally(() => jobs.delete(dst)),
    );
  }
  return jobs.get(dst);
}
