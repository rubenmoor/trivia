// loudness.mjs: quiet and loud generated tones end within ±1 LU of the target. `npm test`
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { after, test } from "node:test";
import { filter, measure, TARGET_LUFS } from "./loudness.mjs";

const tmp = mkdtempSync(path.join(tmpdir(), "trivia-loudness-"));
after(() => rmSync(tmp, { recursive: true, force: true }));
const ff = (...a) => execFileSync("ffmpeg", ["-nostdin", "-v", "error", "-y", ...a]);

for (const [name, volume] of [["quiet", 0.01], ["loud", 0.9]]) {
  test(`${name} tone levelled to the target`, async () => {
    const src = path.join(tmp, `${name}.wav`);
    const dst = path.join(tmp, `${name}.out.wav`);
    ff("-f", "lavfi", "-i", `sine=frequency=440:duration=8,volume=${volume}`, src);
    const m = await measure(src);
    ff("-i", src, "-af", filter(m), "-ar", "48000", dst);
    const after = await measure(dst);
    assert.ok(Math.abs(Number(after.input_i) - TARGET_LUFS) <= 1, `${name}: ${after.input_i}`);
  });
}

test("silence is not levelled", async () => {
  const src = path.join(tmp, "silence.wav");
  ff("-f", "lavfi", "-i", "anullsrc=duration=3", src);
  assert.equal(await measure(src), null);
});
