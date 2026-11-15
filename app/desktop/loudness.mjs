// EBU R128 levelling of shipped question audio and video sound (task 2058), used by stage-media.mjs.
// Target -18 LUFS: measured integrated loudness of every music loop in app/client/public/audio (SOUNDTRACKS), all -18.0 ±0.1;
// question media plays at media volume 1, the music at 0.3 × level, so it sits above the music. True peak ceiling -1.5 dBTP.
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const run = promisify(execFile);
export const TARGET_LUFS = -18;
export const TRUE_PEAK = -1.5;
const LRA = 11;
const BASE = `loudnorm=I=${TARGET_LUFS}:TP=${TRUE_PEAK}:LRA=${LRA}`;

/** Pass 1 on the (already cut) input: the measured values, or null when the sound is silent or missing. */
export async function measure(src, cut = []) {
  let stderr;
  try {
    ({ stderr } = await run("ffmpeg", ["-nostdin", "-hide_banner", "-i", src, ...cut, "-vn", "-af", `${BASE}:print_format=json`, "-f", "null", "-"]));
  } catch (e) {
    ({ stderr } = e);
    if (!stderr?.includes("input_i")) return null;
  }
  const m = /\{[^{}]*"input_i"[^{}]*\}/.exec(stderr);
  if (!m) return null;
  const j = JSON.parse(m[0]);
  return Number.isFinite(Number(j.input_i)) ? j : null;
}

/** Pass 2 filter: linear gain from the measured values (accurate, no dynamic pumping). */
export const filter = (m) =>
  `${BASE}:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true`;
