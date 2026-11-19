// Runs a build tool under `nice -n 19` so encodes don't starve the desktop (task 2284); used by stage-media.mjs and loudness.mjs.
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const exec = promisify(execFile);
export const run = (cmd, args) => exec("nice", ["-n", "19", cmd, ...args]);
// ffmpeg threads per process; workers × this ≈ cores (not hashed: the output doesn't depend on it)
export const FFMPEG_THREADS = 2;
